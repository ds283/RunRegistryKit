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

"""A run whose status does not say that it has finished is in use: the store operations refuse.

For each of the thirteen forms of a `status.json` (`test_unreadable_status.FORMS`: missing, empty,
torn, not JSON, JSON that is not an object, no state, a null state, a state of `"paused"`, a
state of 5), a run is begun in this process on a full registered store and its status is then
given the form. Copy, move, fingerprint, fingerprint `--write`, retire (a dry run) and amend each
refuse with a `RuntimeError` that names the run and says what its status says, and leaves every
file under the temporary directory as it was. A store whose runs have all finished is not refused.

Each form has a store, a run and a destination of its own, so that no form's outcome can depend on
an earlier one's. Needs the store layer (`[stores]`). No Ray is initialised and nothing is
signalled.
"""

import unittest
from pathlib import Path

import runregistrykit
from runregistrykit import stores
from runregistrykit.tests import test_host, test_store_retire
from runregistrykit.tests.test_unreadable_status import (
    FORMS,
    REMEDY,
    UNREADABLE,
    give_status_the_form,
)

TORN = dict((name, make) for name, make, _, _ in FORMS)["torn"]


class TestAnUnreadableStatusIsInUse(test_store_retire.RetireTestCase):
    def refusals(self, primary, i):
        """Each operation, by name, as a call that should refuse primary, with a destination
        of this form's own."""
        elsewhere = self.top / f"C{i}"
        return {
            "copy": lambda: stores.copy_store(
                primary, elsewhere / "copy.sqlite", "a copy", runs_root=self.root
            ),
            "move": lambda: stores.move_store(
                primary, elsewhere / "moved.sqlite", runs_root=self.root
            ),
            "fingerprint": lambda: stores.fingerprint_store(
                primary, runs_root=self.root
            ),
            "fingerprint --write": lambda: stores.fingerprint_store(
                primary, write=True, runs_root=self.root
            ),
            "retire --dry-run": lambda: self.retire(primary, dry_run=True),
            "amend": lambda: stores.amend_sidecar(
                primary, "note", "a reason", value=1, runs_root=self.root
            ),
        }

    def assertEachRefuses(self, primary, i, *fragments):
        for operation, call in self.refusals(primary, i).items():
            with self.subTest(operation):
                before = self.state()
                with self.assertRaises(RuntimeError) as caught:
                    call()
                message = str(caught.exception)
                for fragment in fragments:
                    self.assertIn(fragment, message)
                self.assertEqual(self.state(), before, "a refusal changed a file")

    def test_each_form_is_refused_by_each_operation(self):
        for i, (name, make, readable, words) in enumerate(FORMS):
            with self.subTest(form=name):
                primary = self.a_full_store(directory=f"S{i}")
                run = self.a_running_run(f"form-{i}", primary)
                give_status_the_form(run, make)
                self.assertEachRefuses(
                    primary,
                    i,
                    f"run {run.id}'s",
                    words,
                    "so whether it is running cannot be told",
                    "names this store by its results",
                    REMEDY,
                )
                self.assertTrue(Path(primary).is_file())

    def test_a_real_retire_is_refused_and_the_store_survives(self):
        primary = self.a_full_store()
        run = self.a_running_run("torn", primary)
        give_status_the_form(run, TORN)
        files = self.store_files(primary)
        before = self.state()
        with self.assertRaises(RuntimeError) as caught:
            self.retire(primary)
        self.assertIn(run.id, str(caught.exception))
        self.assertIn(UNREADABLE, str(caught.exception))
        for path in files:
            self.assertTrue(path.is_file(), path)
        self.assertEqual(self.state(), before)

    def test_the_command_refuses_for_a_torn_status(self):
        primary = self.a_full_store()
        run = self.a_running_run("torn-command", primary)
        give_status_the_form(run, TORN)
        err = self.refused("store", "fingerprint", primary, "--runs-root", self.root)
        self.assertIn(run.id, err)
        self.assertIn(UNREADABLE, err)

    def test_a_resumed_runs_fingerprint_is_refused_by_an_unreadable_predecessor(self):
        primary = self.a_full_store()
        predecessor = self.a_running_run("predecessor", primary)
        give_status_the_form(predecessor, TORN)
        run = self.begin("resumed", results=str(primary))
        status = run.finish("done", exit_code=0, fingerprint=True)
        self.assertEqual((status["state"], status["exit_code"]), ("done", 0))
        self.assertNotIn("fingerprint", status)
        self.assertIn(predecessor.id, status["fingerprint_error"])
        self.assertIn(UNREADABLE, status["fingerprint_error"])
        self.assertNotIn(run.id, status["fingerprint_error"])

    def test_a_store_whose_runs_have_all_finished_is_not_refused(self):
        primary = self.a_full_store()
        for state, code in (("done", 0), ("failed", 1), ("killed", 137)):
            self.a_running_run(f"ended-{state}", primary).finish(state, exit_code=code)
        # a status written before the host was recorded, and finished
        old = self.a_running_run("ended-old", primary)
        runregistrykit.write_json_atomic(
            old.status_path,
            test_host.a_status(old.status()["pid"], with_host=False, state="done"),
        )
        result = stores.fingerprint_store(primary, runs_root=self.root)
        self.assertTrue(result["fingerprint"])
        report = self.retire(primary, dry_run=True)
        self.assertTrue(report)
        for path in self.store_files(primary):
            self.assertTrue(path.is_file(), path)

    def test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once(self):
        primary = self.a_full_store()
        stale = self.a_stale_run("stale", primary)
        torn = self.a_running_run("torn-too", primary)
        give_status_the_form(torn, TORN)
        unnamed = self.a_running_run("no-state", primary)
        give_status_the_form(
            unnamed, dict((n, m) for n, m, _, _ in FORMS)["empty object"]
        )
        for operation, call in self.refusals(primary, 0).items():
            with self.subTest(operation):
                with self.assertRaises(RuntimeError) as caught:
                    call()
                message = str(caught.exception)
                self.assertIn(f"run {stale.id} is running (stale, pid ", message)
                self.assertIn(f"run {torn.id}'s status cannot be read", message)
                self.assertIn(
                    f"run {unnamed.id}'s status says neither running", message
                )
                self.assertIn(
                    "tale run is ended by a person, with Run.finish, ", message
                )
                self.assertEqual(message.count(REMEDY), 1, message)

    def test_a_refusal_for_running_runs_alone_has_no_new_sentence(self):
        primary = self.a_full_store()
        self.a_running_run("alive", primary)
        self.a_stale_run("stale", primary)
        for operation, call in self.refusals(primary, 0).items():
            with self.subTest(operation):
                with self.assertRaises(RuntimeError) as caught:
                    call()
                self.assertNotIn("does not say whether", str(caught.exception))
                self.assertNotIn("cannot be told", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
