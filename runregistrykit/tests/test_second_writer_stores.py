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

"""`begin` refuses a second writer on a registered store, by path and by store id.

A run killed outright holds its store until a person ends it; a second `begin` on it is refused,
with no run directory left, and once `python -m runregistrykit end` has recorded the run as `lost`
the `begin` is accepted and its `finish(fingerprint=True)` records a fingerprint. A run is matched
to the new run's store by the manifest's `results`, and by its `results_store_id` when the store has
a problem-free registry sidecar. `begin` makes the check the store operations make, and refuses
exactly what they refuse. A retired store is refused first, by its tombstone's words.

Needs the store layer (`[stores]`). No Ray is initialised. The one process signalled is the child
`test_end.a_hard_killed_run` starts, with `SIGKILL`, and it is reaped.
"""

import json
import os
import re
import unittest

import runregistrykit
from runregistrykit import stores
from runregistrykit.tests import test_end_stores
from runregistrykit.tests.test_host import another_id
from runregistrykit.tests.store_fixtures import (
    script_written_shaped,
    write_sidecar_json,
)
from runregistrykit.tests.test_end import a_hard_killed_run, a_status_of_its_own
from runregistrykit.tests.test_second_writer import STAMP
from runregistrykit.tests.test_unreadable_status import FORMS, give_status_the_form

END = runregistrykit._END


class SecondWriterStoresTestCase(test_end_stores.EndStoresTestCase):
    def refused_begin(self, primary, slug="second") -> str:
        """`begin` on ``primary`` is refused, and nothing under the temporary directory moved."""
        before = self.state()
        with self.assertRaises(RuntimeError) as caught:
            self.begin(slug, results=str(primary))
        message = str(caught.exception)
        self.assertRegex(message, f"^Cannot begin run example-01-{slug}-{STAMP} with ")
        self.assertTrue(message.endswith("No run directory was created"), message)
        self.assertEqual(self.state(), before, "a refusal changed the tree")
        return message


class TestTheAcceptance(SecondWriterStoresTestCase):
    def test_a_hard_killed_run_blocks_begin_until_it_is_ended(self):
        primary = self.a_full_store()
        path, _, _ = a_hard_killed_run(
            self, self.root, self.client, results=str(primary)
        )
        identifier = os.path.basename(path)
        (entry,) = runregistrykit.list_runs(root=self.root)
        self.assertEqual((entry["state"], entry["liveness"]), ("running", "stale"))

        message = self.refused_begin(primary)
        self.assertIn(f"run {identifier} is running (stale, pid ", message)
        self.assertIn("runregistrykit end RUN_ID", message)

        report, out, err = self.command(
            "end",
            identifier,
            "--reason",
            "killed outright in a test",
            "--root",
            self.root,
        )
        self.assertEqual(report["code"], 0, err)
        self.assertIn(f">> end: {identifier} is now lost, verified", out)

        resumed = self.begin("resumed", results=str(primary))
        status = resumed.finish("done", exit_code=0, fingerprint=True)
        self.assertEqual((status["state"], status["exit_code"]), ("done", 0))
        self.assertIn("fingerprint", status)
        self.assertNotIn("fingerprint_error", status)

    def test_alive_stale_foreign_and_unreadable_are_refused_each_with_no_directory(
        self,
    ):
        here = runregistrykit.this_host()
        torn = dict((name, make) for name, make, _, _ in FORMS)["torn"]
        rows = {
            "alive": lambda run: None,
            "stale": lambda run: run.heartbeat(pid=self.a_dead_pid()),
            "unreadable": lambda run: give_status_the_form(run, torn),
        }
        if here["id"] is not None:
            rows["foreign"] = lambda run: a_status_of_its_own(
                run, host={"id": another_id(here["id"]), "boot": "a-boot"}
            )
        for name, make in rows.items():
            with self.subTest(name):
                primary = self.a_full_store(directory=f"S-{name}")
                run = self.a_running_run(f"earlier-{name}", primary)
                make(run)
                message = self.refused_begin(primary)
                self.assertIn(f"run {run.id}", message)

    def test_a_store_whose_runs_have_all_finished_is_accepted(self):
        primary = self.a_full_store()
        for state, code in (("done", 0), ("failed", 1), ("killed", None)):
            self.a_running_run(f"ended-{state}", primary).finish(state, exit_code=code)
        lost = self.a_stale_run("to-be-lost", primary)
        runregistrykit._end_run(lost.path, "ended in a test", client_root=self.client)
        run = self.begin("second", results=str(primary))
        self.assertTrue(os.path.isdir(run.path))


class TestMatching(SecondWriterStoresTestCase):
    def test_by_store_id_alone(self):
        primary = self.a_full_store()
        store_id = stores.read_sidecar(primary).store_id
        self.assertIsNotNone(store_id)
        gone = self.top / "gone" / "other.sqlite"
        earlier = self.a_running_run("earlier", gone)
        manifest_path = os.path.join(earlier.path, "manifest.json")
        manifest = runregistrykit.read_json(manifest_path)
        self.assertIsNone(manifest["results_store_id"])
        manifest["results_store_id"] = store_id
        with open(manifest_path, "w") as handle:
            json.dump(manifest, handle)
        message = self.refused_begin(primary)
        self.assertIn(
            f"run {earlier.id} is running (alive, pid {os.getpid()}) and names this store "
            f"by its results_store_id",
            message,
        )
        self.assertNotIn("its results and", message)

        # a legacy sidecar has no store id, so the same run no longer names this store
        write_sidecar_json(primary, script_written_shaped(self.top / "X"))
        self.assertIsNone(stores.read_sidecar(primary).store_id)
        run = self.begin("second", results=str(primary))
        self.assertTrue(os.path.isdir(run.path))

    def test_by_path_alone_when_there_is_no_sidecar(self):
        primary = self.a_full_store(sidecar=False)
        self.assertFalse(stores.sidecar_path(primary).exists())
        earlier = self.a_running_run("earlier", primary)
        message = self.refused_begin(primary)
        self.assertIn(f"run {earlier.id} is running (alive, pid ", message)
        self.assertIn("names this store by its results", message)
        self.assertNotIn("results_store_id", message)


class TestOneRule(SecondWriterStoresTestCase):
    def test_begin_and_each_store_operation_refuse_naming_the_same_run(self):
        primary = self.a_full_store()
        earlier = self.a_running_run("earlier", primary)
        described = (
            f"run {earlier.id} is running \\(alive, pid {os.getpid()}\\) and names this "
            f"store by its results"
        )
        messages = dict(self.refusals(primary))
        messages["begin"] = self.refused_begin(primary)
        self.assertEqual(len(messages), 7)
        for operation, message in messages.items():
            with self.subTest(operation):
                self.assertEqual(len(re.findall(described, message)), 1, message)
                self.assertEqual(message.count(END), 1, message)


class TestTheOrder(SecondWriterStoresTestCase):
    def test_a_tombstone_is_refused_by_its_own_words_before_the_check(self):
        primary = self.a_full_store()
        earlier = self.a_running_run("earlier", primary)
        # the state an older record leaves: a run that has not finished, naming a retired store
        with self.set_aside(earlier):
            self.retire(primary)
        self.assertTrue(stores.read_sidecar(primary).retired)
        message = self.refused_begin(primary)
        self.assertIn("is a tombstone: the store was retired", message)
        self.assertIn("Give the new store a name of its own", message)
        self.assertNotIn(earlier.id, message)
        self.assertNotIn("A stale run is ended", message)


class TestPidAliveThroughTheStoreOperations(SecondWriterStoresTestCase):
    def test_a_pid_out_of_range_is_stale_and_blocks_only_its_own_store(self):
        own = self.a_full_store(directory="S-own")
        other = self.a_full_store(directory="S-other")
        run = self.a_running_run("huge-pid", own)
        status = runregistrykit.read_json(run.status_path)
        status["pid"] = 2**31
        runregistrykit.write_json_atomic(run.status_path, status)

        self.assertTrue(stores.fingerprint_store(other, runs_root=self.root))
        with self.assertRaises(RuntimeError) as caught:
            stores.fingerprint_store(own, runs_root=self.root)
        self.assertIn(
            f"run {run.id} is running (stale, pid {2**31})", str(caught.exception)
        )


def contents(path) -> dict:
    """Every file in the run directory ``path``, by name, with its bytes."""
    found = {}
    for name in sorted(os.listdir(path)):
        with open(os.path.join(path, name), "rb") as handle:
            found[name] = handle.read()
    return found


class TestTheFixture(SecondWriterStoresTestCase):
    def runs_state(self) -> dict:
        """The tree, but for the runs root's own mtime, which any rename into it moves."""
        return {k: v for k, v in self.state().items() if k != "runs"}

    def test_set_aside_puts_back_byte_for_byte_whatever_the_body_raises(self):
        primary = self.a_full_store()
        first = self.a_running_run("first", primary)
        with self.set_aside(first):
            second = self.a_running_run("second", primary)
        before = self.runs_state()
        kept = {run.id: contents(run.path) for run in (first, second)}
        with self.assertRaises(ZeroDivisionError):
            with self.set_aside(first, second):
                self.assertEqual(os.listdir(self.root), [])
                1 / 0
        self.assertEqual(self.runs_state(), before)
        self.assertEqual({run.id: contents(run.path) for run in (first, second)}, kept)
        self.assertEqual(sorted(os.listdir(self.root)), sorted([first.id, second.id]))
        self.assertEqual(
            [n for n in os.listdir(self.top) if n.startswith("set-aside-")], []
        )


if __name__ == "__main__":
    unittest.main()
