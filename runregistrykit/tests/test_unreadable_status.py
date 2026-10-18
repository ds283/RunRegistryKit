# (c) University of Sussex 2026
# Created by David Seery
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A status the registry cannot read says nothing, and is never raised on.

A `status.json` that is missing, empty, torn, not JSON, JSON that is not an object, an object with
no state, a null state, a state that is not a string, or a string the registry never writes, is
read as a status that does not say whether its run is running. `list_runs` reports it with
`liveness` `unknown` and `status_readable` false when it is not a JSON object; `liveness` itself
never raises on one; `Run.finish`, the remedy a refusal names, ends such a run; and `list` marks
the row of a run that has a manifest `!!`, with a line on stderr. A `manifest.json` that is JSON
but not an object is read as no manifest.

The core only: nothing of the store layer is imported, so that the core job can run this module.
Every file is built in a temporary directory and nothing is signalled. The forms below are the
module's own table, which the store layer's test of the same rule imports.
"""

import json
import os
import subprocess
import sys
import unittest

import runregistrykit
from runregistrykit.tests import test_host, test_run_registry
from runregistrykit.tests.client_fixtures import PACKAGE_PARENT

# the thirteen forms a status can take: (name, how the file is written from a full status, whether
# it parses as a JSON object, and what a store refusal says of it)
UNREADABLE = (
    "status cannot be read (status.json is missing, is not JSON, or is not a JSON object), so "
    "whether it is running cannot be told"
)
NO_STATE = "status says neither running nor finished (state "
FORMS = (
    ("missing", lambda full: None, False, UNREADABLE),
    ("empty file", lambda full: b"", False, UNREADABLE),
    (
        "torn",
        lambda full: json.dumps(full, indent=2).encode()[: len(json.dumps(full)) // 2],
        False,
        UNREADABLE,
    ),
    ("not JSON", lambda full: b"not json at all\n", False, UNREADABLE),
    ("null", lambda full: b"null\n", False, UNREADABLE),
    ("empty list", lambda full: b"[]\n", False, UNREADABLE),
    ("list of one", lambda full: b"[1]\n", False, UNREADABLE),
    ("string", lambda full: b'"running"\n', False, UNREADABLE),
    ("number", lambda full: b"5\n", False, UNREADABLE),
    ("empty object", lambda full: b"{}\n", True, NO_STATE + "none)"),
    (
        "null state",
        lambda full: json.dumps(dict(full, state=None)).encode(),
        True,
        NO_STATE + "none)",
    ),
    (
        "paused",
        lambda full: json.dumps(dict(full, state="paused")).encode(),
        True,
        NO_STATE + "'paused')",
    ),
    (
        "state 5",
        lambda full: json.dumps(dict(full, state=5)).encode(),
        True,
        NO_STATE + "5)",
    ),
)

REMEDY = "is ended by a person, with Run.finish, once they have checked that it is not"


def give_status_the_form(run, make) -> None:
    """Replace run's `status.json` with what make writes, from the full status it has."""
    full = runregistrykit.read_json(run.status_path)
    data = make(full)
    if data is None:
        os.remove(run.status_path)
    else:
        with open(run.status_path, "wb") as handle:
            handle.write(data)


class UnreadableStatusTestCase(test_run_registry.RegistryTestCase):
    def a_run_in_the_form(self, slug, make):
        run = self.begin(slug)
        give_status_the_form(run, make)
        return run

    def entry(self, run):
        (found,) = [
            e for e in runregistrykit.list_runs(root=self.root) if e["id"] == run.id
        ]
        return found


class TestTheLister(UnreadableStatusTestCase):
    def test_every_form_is_listed_unknown_and_none_raises(self):
        runs = {
            name: self.a_run_in_the_form(f"form-{i}", make)
            for i, (name, make, _, _) in enumerate(FORMS)
        }
        finished = self.begin("finished")
        finished.finish("done", exit_code=0)
        entries = runregistrykit.list_runs(root=self.root)
        self.assertEqual(len(entries), len(FORMS) + 1)
        for name, make, readable, _ in FORMS:
            with self.subTest(name):
                entry = self.entry(runs[name])
                self.assertIs(entry["status_readable"], readable)
                self.assertEqual(entry["liveness"], "unknown")
                self.assertTrue(entry["has_manifest"])
        entry = self.entry(finished)
        self.assertEqual(entry["liveness"], "finished")
        self.assertTrue(entry["status_readable"])

    def test_a_manifest_that_is_not_an_object_is_read_as_no_manifest(self):
        for i, text in enumerate(["[1]", '"x"', "5", "null", "true"]):
            with self.subTest(text):
                run = self.begin(f"manifest-{i}")
                with open(run.manifest_path, "w") as handle:
                    handle.write(text)
                entry = self.entry(run)
                self.assertFalse(entry["has_manifest"])
                self.assertIsNone(entry["purpose"])
                self.assertTrue(entry["status_readable"])

    def test_an_empty_manifest_object_is_still_a_manifest(self):
        run = self.begin("empty-manifest")
        with open(run.manifest_path, "w") as handle:
            handle.write("{}")
        entry = self.entry(run)
        self.assertTrue(entry["has_manifest"])
        self.assertIsNone(entry["purpose"])

    def test_a_directory_with_no_manifest_and_no_status_is_listed_unreadable(self):
        os.mkdir(os.path.join(self.root, "predates-the-registry"))
        (entry,) = runregistrykit.list_runs(root=self.root)
        self.assertFalse(entry["has_manifest"])
        self.assertFalse(entry["status_readable"])
        self.assertEqual(entry["liveness"], "unknown")


class TestLiveness(unittest.TestCase):
    def test_a_status_that_is_not_an_object_is_unknown(self):
        for status in ([1], "x", 5, True, None, [], {}, 0.5):
            with self.subTest(status=status):
                self.assertEqual(runregistrykit.liveness(status, 900.0), "unknown")


class TestTheRemedy(UnreadableStatusTestCase):
    """`Run.finish`, which every refusal names, ends a run in every form."""

    def test_finish_ends_a_run_in_every_form(self):
        for i, (name, make, _, _) in enumerate(FORMS):
            with self.subTest(name):
                run = self.a_run_in_the_form(f"remedy-{i}", make)
                runregistrykit.Run(run.path).finish("killed", exit_code=137)
                status = runregistrykit.read_json(run.status_path)
                self.assertIsInstance(status, dict)
                self.assertEqual(
                    (status["state"], status["exit_code"]), ("killed", 137)
                )
                self.assertEqual(self.entry(run)["liveness"], "finished")

    def test_the_status_method_reads_a_form_that_is_not_an_object_as_empty(self):
        for i, name in enumerate(
            ("null", "empty list", "list of one", "string", "number")
        ):
            with self.subTest(name):
                make = dict((n, m) for n, m, _, _ in FORMS)[name]
                run = self.a_run_in_the_form(f"method-{i}", make)
                self.assertEqual(run.status(), {})


class TestTheListCommand(UnreadableStatusTestCase):
    def test_each_form_is_marked_and_the_line_on_stderr_counts_them(self):
        runs = [
            self.a_run_in_the_form(f"row-{i}", make)
            for i, (_, make, _, _) in enumerate(FORMS)
        ]
        finished = self.begin("finished")
        finished.finish("done", exit_code=0)
        os.mkdir(os.path.join(self.root, "predates-the-registry"))
        done = subprocess.run(
            [sys.executable, "-m", "runregistrykit", "list", "--root", self.root],
            capture_output=True,
            text=True,
            cwd=self.client,
            env={**os.environ, "PYTHONPATH": PACKAGE_PARENT},
            timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        rows = {}
        for line in done.stdout.splitlines():
            for run in [*runs, finished]:
                if run.id in line:
                    rows[run.id] = line
            if "predates-the-registry" in line:
                rows["predates"] = line
        self.assertEqual(len(rows), len(FORMS) + 2, done.stdout)
        for run, (name, _, _, _) in zip(runs, FORMS):
            self.assertTrue(rows[run.id].startswith("!! "), (name, rows[run.id]))
        self.assertFalse(rows[finished.id].startswith("!!"), rows[finished.id])
        self.assertTrue(rows["predates"].startswith("   "), rows["predates"])
        lines = [line for line in done.stderr.splitlines() if line.startswith("!! ")]
        self.assertEqual(len(lines), 1, done.stderr)
        self.assertTrue(
            lines[0].startswith(
                f"!! {len(FORMS)} run(s) have a manifest and a status that does not say "
                f"whether the run is running, or that cannot be read: "
            ),
            lines[0],
        )
        self.assertIn("the registry cannot tell whether they are running", lines[0])
        self.assertIn("the store operations count them as in use", lines[0])
        self.assertIn("end it with Run.finish", lines[0])
        self.assertIn(f"{len(FORMS) + 2} run(s) under {self.root}", done.stdout)

    def test_a_state_that_is_a_list_or_an_object_is_listed_not_raised_on(self):
        runs = [
            self.a_run_in_the_form(
                f"odd-state-{i}",
                lambda full, state=state: json.dumps(dict(full, state=state)).encode(),
            )
            for i, state in enumerate((["a"], {"a": 1}))
        ]
        done = subprocess.run(
            [sys.executable, "-m", "runregistrykit", "list", "--root", self.root],
            capture_output=True,
            text=True,
            cwd=self.client,
            env={**os.environ, "PYTHONPATH": PACKAGE_PARENT},
            timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        for run in runs:
            (row,) = [line for line in done.stdout.splitlines() if run.id in line]
            self.assertTrue(row.startswith("!! "), row)
            self.assertEqual(self.entry(run)["liveness"], "unknown")

    def test_no_such_run_no_such_line(self):
        self.begin("here").finish("done", exit_code=0)
        os.mkdir(os.path.join(self.root, "predates-the-registry"))
        done = subprocess.run(
            [sys.executable, "-m", "runregistrykit", "list", "--root", self.root],
            capture_output=True,
            text=True,
            cwd=self.client,
            env={**os.environ, "PYTHONPATH": PACKAGE_PARENT},
            timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertNotIn("!!", done.stdout + done.stderr)


class TestAnOldRecord(UnreadableStatusTestCase):
    """A status written by `v0.1.0`, with no `host`, is judged as `v0.1.0` judged it."""

    def test_a_running_and_a_finished_status_without_a_host(self):
        running = self.begin("old-running")
        runregistrykit.write_json_atomic(
            running.status_path, test_host.a_status(os.getpid(), with_host=False)
        )
        done = self.begin("old-done")
        runregistrykit.write_json_atomic(
            done.status_path,
            test_host.a_status(os.getpid(), with_host=False, state="done"),
        )
        entry = self.entry(running)
        self.assertTrue(entry["status_readable"])
        self.assertFalse(entry["host_recorded"])
        self.assertEqual((entry["state"], entry["liveness"]), ("running", "alive"))
        entry = self.entry(done)
        self.assertTrue(entry["status_readable"])
        self.assertEqual((entry["state"], entry["liveness"]), ("done", "finished"))


if __name__ == "__main__":
    unittest.main()
