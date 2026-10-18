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

"""`begin` refuses a second writer, and `pid_alive` answers false for a pid out of range.

`begin` with `results` refuses, before it creates the run directory, a store that a run which has
not finished already names: `running` (alive, stale, or on another host) or a status that does not
say, by the manifest's `results`. A store whose runs have all finished, one no run names, a `begin`
with no `results` and a runs root that does not exist yet are accepted. A retired store is still
refused first, with its own words. The check reads only the runs root the run is created in, is not
a lock, and has no override. A pid outside the platform's range names no process.

The core only: nothing of the store layer is imported, so that the core job can run this module.
Every store here is a plain file in a temporary directory with no sidecar, so a run matches it by
path. Nothing is signalled.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import runregistrykit
from runregistrykit.tests import test_host, test_run_registry
from runregistrykit.tests.client_fixtures import PACKAGE_PARENT, temporary_directory
from runregistrykit.tests.test_end import a_status_of_its_own
from runregistrykit.tests.test_unreadable_status import (
    FORMS,
    REMEDY,
    give_status_the_form,
)

END = runregistrykit._END
FOREIGN = (
    f"A run on another host is ended by a person, with `{END}` on that host, or here with "
    f"`--unverified` once they have checked there"
)
STALE_REMEDY = (
    f"A stale run is ended by a person, with `{END}`, before another run is begun on its "
    f"store; the registry does not decide that a run is dead. "
)
STAMP = r"[0-9]{8}T[0-9]{6}"


def snapshot(root) -> dict:
    """Every file and directory under ``root``, with a file's bytes."""
    found = {}
    for here, directories, names in os.walk(root):
        for name in directories:
            found[os.path.relpath(os.path.join(here, name), root)] = None
        for name in names:
            path = os.path.join(here, name)
            with open(path, "rb") as handle:
                found[os.path.relpath(path, root)] = handle.read()
    return found


class SecondWriterTestCase(test_run_registry.RegistryTestCase):
    def a_plain_store(self, name="results.sqlite") -> str:
        """A file in the runs root, with no sidecar, which a manifest names by path."""
        store = os.path.join(self.root, name)
        with open(store, "wb") as handle:
            handle.write(b"not a datastore, and not JSON either\n")
        return store

    def an_earlier_run(self, store, slug="earlier"):
        """A run on ``store``. `begin` no longer makes two runs that have not finished on one
        store, so every run already under the runs root is moved aside while this one is begun and
        moved back after: the state a run begun before, or copied in, leaves."""
        holding = tempfile.mkdtemp(prefix="set-aside-")
        self.addCleanup(shutil.rmtree, holding, True)
        moved = []
        try:
            for name in sorted(os.listdir(self.root)):
                path = os.path.join(self.root, name)
                if os.path.isdir(path):
                    os.rename(path, os.path.join(holding, name))
                    moved.append(name)
            run = self.begin(slug, results=store)
        finally:
            for name in moved:
                os.rename(os.path.join(holding, name), os.path.join(self.root, name))
        return run

    def assertRefusedBegin(self, store, *fragments, slug="second") -> str:
        """`begin` on ``store`` is refused as the check refuses it, and the runs root is exactly
        as it was: no run directory, no file."""
        before = snapshot(self.root)
        with self.assertRaises(RuntimeError) as caught:
            self.begin(slug, results=store)
        message = str(caught.exception)
        self.assertRegex(
            message,
            re.escape("Cannot begin run example-01-")
            + slug
            + "-"
            + STAMP
            + " with results",
        )
        self.assertIn(f'with results "{store}": ', message)
        self.assertTrue(message.endswith("No run directory was created"), message)
        self.assertIn(STALE_REMEDY, message)
        for fragment in fragments:
            self.assertIn(fragment, message)
        self.assertEqual(snapshot(self.root), before, "a refusal left something")
        return message

    def an_elsewhere_status(self, run):
        here = runregistrykit.this_host()
        a_status_of_its_own(
            run, host={"id": test_host.another_id(here["id"]), "boot": "a-boot"}
        )


class TestEveryRefusal(SecondWriterTestCase):
    def test_an_alive_run_in_this_process(self):
        store = self.a_plain_store()
        earlier = self.an_earlier_run(store)
        self.assertRefusedBegin(
            store,
            f"run {earlier.id} is running (alive, pid {os.getpid()}) and names this store "
            f"by its results",
        )

    def test_a_stale_run(self):
        store = self.a_plain_store()
        earlier = self.a_stale_run_on(store)
        message = self.assertRefusedBegin(
            store, f"run {earlier.id} is running (stale, pid "
        )
        self.assertNotIn(FOREIGN, message)
        self.assertNotIn(REMEDY, message)

    def a_stale_run_on(self, store, slug="stale"):
        """`running`, with a fresh heartbeat and a pid that is gone, naming ``store``."""
        dead = self.a_dead_pid()
        run = self.an_earlier_run(store, slug)
        run.heartbeat(pid=dead)
        return run

    def test_a_run_from_an_earlier_boot_of_this_host_is_stale(self):
        here = runregistrykit.this_host()
        if here["id"] is None or here["boot"] is None:
            self.skipTest("this platform offers no host or boot identity")
        store = self.a_plain_store()
        earlier = self.an_earlier_run(store)
        a_status_of_its_own(
            earlier, host={"id": here["id"], "boot": here["boot"] + "-earlier"}
        )
        self.assertEqual(
            runregistrykit.list_runs(root=self.root)[0]["liveness"], "stale"
        )
        self.assertRefusedBegin(store, f"run {earlier.id} is running (stale, pid ")

    def test_a_run_on_another_host_is_foreign(self):
        here = runregistrykit.this_host()
        if here["id"] is None:
            self.skipTest("this platform offers no host identity")
        store = self.a_plain_store()
        earlier = self.an_earlier_run(store)
        self.an_elsewhere_status(earlier)
        message = self.assertRefusedBegin(
            store, f"run {earlier.id} is running on another host, "
        )
        self.assertIn("not tested here", message)
        self.assertEqual(message.count(FOREIGN), 1, message)
        self.assertNotIn(REMEDY, message)

    def test_each_of_the_thirteen_unreadable_forms(self):
        for name, make, _, fragment in FORMS:
            with self.subTest(name):
                store = self.a_plain_store(f"{name.replace(' ', '-')}.sqlite")
                earlier = self.an_earlier_run(store, f"form-{name.replace(' ', '-')}")
                give_status_the_form(earlier, make)
                message = self.assertRefusedBegin(
                    store, f"run {earlier.id}'s {fragment}", slug="second"
                )
                self.assertEqual(message.count(REMEDY), 1, message)

    def test_a_v010_status_judged_by_its_pid(self):
        for label, pid, liveness in (
            ("dead", None, "stale"),
            ("live", os.getpid(), "alive"),
        ):
            with self.subTest(label):
                store = self.a_plain_store(f"{label}.sqlite")
                earlier = self.an_earlier_run(store, f"v010-{label}")
                pid = self.a_dead_pid() if pid is None else pid
                runregistrykit.write_json_atomic(
                    earlier.status_path,
                    test_host.a_status(pid, with_host=False),
                )
                (entry,) = [
                    e
                    for e in runregistrykit.list_runs(root=self.root)
                    if e["id"] == earlier.id
                ]
                self.assertEqual(entry["liveness"], liveness)
                self.assertRefusedBegin(
                    store, f"run {earlier.id} is running ({liveness}, pid {pid})"
                )


class TestTheWords(SecondWriterTestCase):
    def test_the_whole_text_for_an_alive_run(self):
        store = self.a_plain_store()
        earlier = self.an_earlier_run(store)
        with self.assertRaises(RuntimeError) as caught:
            self.begin("second", results=store)
        expected = (
            "Cannot begin run example-01-second-" + STAMP + f' with results "{store}": '
            f"run {earlier.id} is running (alive, pid {os.getpid()}) and names this store by "
            f"its results. A stale run is ended by a person, with "
            f"`python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun "
            f"on its store; the registry does not decide that a run is dead. "
            f"No run directory was created"
        )
        self.assertRegex(str(caught.exception), "^" + _escaped(expected) + "$")

    def test_the_whole_text_for_a_stale_run(self):
        store = self.a_plain_store()
        earlier = self.an_earlier_run(store)
        dead = self.a_dead_pid()
        earlier.heartbeat(pid=dead)
        with self.assertRaises(RuntimeError) as caught:
            self.begin("second", results=store)
        expected = (
            "Cannot begin run example-01-second-" + STAMP + f' with results "{store}": '
            f"run {earlier.id} is running (stale, pid {dead}) and names this store by its "
            f"results. A stale run is ended by a person, with "
            f"`python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun "
            f"on its store; the registry does not decide that a run is dead. "
            f"No run directory was created"
        )
        self.assertRegex(str(caught.exception), "^" + _escaped(expected) + "$")

    def test_the_stale_remedy_names_the_command_once(self):
        store = self.a_plain_store()
        self.an_earlier_run(store)
        message = self.assertRefusedBegin(store)
        self.assertEqual(
            message.count("`python -m runregistrykit end RUN_ID --reason TEXT`"), 1
        )
        self.assertEqual(message.count(END), 1)

    def test_the_foreign_sentence_is_once_with_two_foreign_runs_and_absent_with_none(
        self,
    ):
        here = runregistrykit.this_host()
        if here["id"] is None:
            self.skipTest("this platform offers no host identity")
        store = self.a_plain_store()
        first = self.an_earlier_run(store, "first")
        second = self.an_earlier_run(store, "second-earlier")
        message = self.assertRefusedBegin(store)
        self.assertNotIn(FOREIGN, message)
        for run in (first, second):
            self.an_elsewhere_status(run)
        message = self.assertRefusedBegin(store)
        self.assertEqual(message.count(FOREIGN), 1, message)
        self.assertIn(f"run {first.id} is running on another host", message)
        self.assertIn(f"run {second.id} is running on another host", message)

    def test_the_unverified_sentence_is_once_with_two_unreadable_runs_and_absent_with_none(
        self,
    ):
        store = self.a_plain_store()
        first = self.an_earlier_run(store, "first")
        message = self.assertRefusedBegin(store)
        self.assertNotIn(REMEDY, message)
        self.assertNotIn("does not say whether", message)
        torn = dict((name, make) for name, make, _, _ in FORMS)["torn"]
        second = self.an_earlier_run(store, "second-earlier")
        for run in (first, second):
            give_status_the_form(run, torn)
        message = self.assertRefusedBegin(store)
        self.assertEqual(message.count(REMEDY), 1, message)
        self.assertEqual(message.count("--unverified"), 1, message)

    def test_an_alive_and_a_stale_run_here_add_neither_sentence(self):
        store = self.a_plain_store()
        self.an_earlier_run(store, "alive")
        self.a_stale_run_on(store, "stale")
        message = self.assertRefusedBegin(store)
        self.assertNotIn(FOREIGN, message)
        self.assertNotIn("does not say whether", message)
        self.assertNotIn("cannot be told", message)

    a_stale_run_on = TestEveryRefusal.a_stale_run_on


def _escaped(expected: str) -> str:
    """``expected`` as a regular expression, with its `STAMP` left as the pattern."""
    parts = expected.split(STAMP)
    return STAMP.join(re.escape(part) for part in parts)


class TestEveryAcceptance(SecondWriterTestCase):
    def test_a_store_whose_earlier_runs_have_all_finished(self):
        store = self.a_plain_store()
        for state, code in (("done", 0), ("failed", 2), ("killed", None)):
            self.an_earlier_run(store, f"ended-{state}").finish(state, exit_code=code)
        lost_run = self.an_earlier_run(store, "lost-one")
        lost_run.heartbeat(pid=self.a_dead_pid())
        runregistrykit._end_run(
            lost_run.path, "ended in a test", client_root=self.client
        )
        entry = [
            e
            for e in runregistrykit.list_runs(root=self.root)
            if e["id"] == lost_run.id
        ][0]
        self.assertEqual(entry["state"], "lost")
        run = self.begin("second", results=store)
        self.assertEqual(runregistrykit.read_json(run.status_path)["state"], "running")

    def test_a_store_no_run_names(self):
        store = self.a_plain_store()
        other = self.a_plain_store("other.sqlite")
        self.an_earlier_run(other)
        run = self.begin("second", results=store)
        self.assertTrue(os.path.isdir(run.path))

    def test_a_begin_with_no_results_while_a_run_names_a_store(self):
        store = self.a_plain_store()
        self.an_earlier_run(store)
        run = self.begin("no-results")
        self.assertTrue(os.path.isdir(run.path))

    def test_a_runs_root_that_does_not_exist_yet_is_created(self):
        store = self.a_plain_store()
        self.an_earlier_run(store)
        root = os.path.join(temporary_directory(self), "not", "there", "yet")
        run = self.begin_under(root, results=store)
        self.assertTrue(os.path.isdir(run.path))
        self.assertEqual(os.path.dirname(run.path), root)

    def begin_under(self, root, slug="elsewhere", **kwargs):
        """`begin` under ``root``, with the keywords `RegistryTestCase.begin` gives."""
        return runregistrykit.begin(
            campaign="example",
            prompt="01",
            slug=slug,
            purpose="a test run, in a temporary directory",
            argv=["unittest", slug],
            root=root,
            client_root=self.client,
            **kwargs,
        )

    def test_a_run_under_another_runs_root_is_not_seen(self):
        store = self.a_plain_store()
        top = temporary_directory(self)
        elsewhere = os.path.join(top, "runs-a")
        alive = self.begin_under(elsewhere, "alive", results=store)
        (entry,) = runregistrykit.list_runs(root=elsewhere)
        self.assertEqual(entry["liveness"], "alive")
        run = self.begin("second", results=store)
        self.assertTrue(os.path.isdir(run.path))
        # and the other way: a run under this root does not refuse a begin under another
        third = self.begin_under(os.path.join(top, "runs-b"), "third", results=store)
        self.assertTrue(os.path.isdir(third.path))
        self.assertTrue(os.path.isdir(alive.path))


class TestTheRemedy(SecondWriterTestCase):
    def test_a_stale_run_is_ended_and_then_begin_is_accepted(self):
        store = self.a_plain_store()
        earlier = self.an_earlier_run(store)
        earlier.heartbeat(pid=self.a_dead_pid())
        self.assertRefusedBegin(store, f"run {earlier.id} is running (stale")
        ended = runregistrykit._end_run(
            earlier.path, "ended in a test", client_root=self.client
        )
        self.assertEqual(ended["state"], "lost")
        run = self.begin("second", results=store)
        status = run.finish("done", exit_code=0)
        self.assertEqual((status["state"], status["exit_code"]), ("done", 0))


class TestPidAlive(SecondWriterTestCase):
    def test_a_pid_out_of_range_is_false_and_does_not_raise(self):
        for pid in (2**31, 2**63, 10**30, float("inf")):
            with self.subTest(pid=pid):
                self.assertIs(runregistrykit.pid_alive(pid), False)

    def test_the_others_are_as_before(self):
        for pid in (-1, 0, None, "x", float("nan"), -(2**31) - 1):
            with self.subTest(pid=pid):
                self.assertIs(runregistrykit.pid_alive(pid), False)
        self.assertIs(runregistrykit.pid_alive(os.getpid()), True)
        self.assertIs(runregistrykit.pid_alive(str(os.getpid())), True)
        self.assertIs(runregistrykit.pid_alive(self.a_dead_pid()), False)

    def a_running_status_with_pid(self, slug, pid_text, store=None):
        """A run whose `status.json` says `running`, here, with a fresh heartbeat and a pid
        written as the text ``pid_text`` (which may be `Infinity`, as `json` writes it).
        """
        run = self.begin(slug, results=store) if store else self.begin(slug)
        status = runregistrykit.read_json(run.status_path)
        text = json.dumps(dict(status, pid="@@PID@@")).replace('"@@PID@@"', pid_text)
        with open(run.status_path, "w") as handle:
            handle.write(text)
        return run

    def test_through_the_readers_for_a_pid_out_of_range(self):
        for label, pid_text, expected in (
            ("2**31", str(2**31), 2**31),
            ("Infinity", "Infinity", float("inf")),
        ):
            with self.subTest(label):
                run = self.a_running_status_with_pid(f"huge-{label[0]}", pid_text)
                self.assertEqual(
                    runregistrykit.read_json(run.status_path)["pid"], expected
                )
                (entry,) = [
                    e
                    for e in runregistrykit.list_runs(root=self.root)
                    if e["id"] == run.id
                ]
                self.assertEqual(
                    (entry["state"], entry["liveness"]), ("running", "stale")
                )
                done = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "runregistrykit",
                        "list",
                        "--root",
                        self.root,
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.client,
                    env={**os.environ, "PYTHONPATH": PACKAGE_PARENT},
                    timeout=300,
                )
                self.assertEqual(done.returncode, 0, done.stderr)
                (row,) = [line for line in done.stdout.splitlines() if run.id in line]
                self.assertTrue(row.startswith("!! "), row)
                written = runregistrykit._end_run(
                    run.path, "ended in a test", client_root=self.client
                )
                self.assertEqual(written["state"], "lost")
                self.assertTrue(written["ended"]["verified"])
                self.assertIs(written["ended"]["evidence"]["pid_answers"], False)

    def test_a_record_with_such_a_pid_does_not_stop_a_begin_on_another_store(self):
        huge = self.a_plain_store("huge.sqlite")
        other = self.a_plain_store("other.sqlite")
        self.a_running_status_with_pid("huge", str(2**31), huge)
        run = self.begin("on-another", results=other)
        self.assertTrue(os.path.isdir(run.path))
        self.assertRefusedBegin(huge, "(stale, pid 2147483648)")

    def test_infinity_in_a_record_does_not_stop_a_begin_on_another_store(self):
        huge = self.a_plain_store("huge.sqlite")
        other = self.a_plain_store("other.sqlite")
        self.a_running_status_with_pid("huge", "Infinity", huge)
        run = self.begin("on-another", results=other)
        self.assertTrue(os.path.isdir(run.path))
        self.assertRefusedBegin(huge, "run ", "is running (stale")


if __name__ == "__main__":
    unittest.main()
