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

"""A run killed outright blocks its store until a person ends it, and then does not.

A child process begins a run on a full registered store, heartbeats, and is sent `SIGKILL` and
reaped. Copy, move, fingerprint, fingerprint `--write`, retire (a dry run) and amend each refuse
the store, naming the run and `python -m runregistrykit end`, and leave every file as it was. Once
`python -m runregistrykit end` has recorded the run as `lost`, a resumed run's
`finish(fingerprint=True)` records a fingerprint, and every operation proceeds.

The refusals' words: a run on another host adds one sentence, saying how it is ended, and a run
whose status does not say adds 03's, naming `--unverified`; a refusal naming only alive and stale
runs on this host is the old text with `Run.finish` replaced by the command, and nothing else.

Needs the store layer (`[stores]`). No Ray is initialised. The child is the only process signalled,
and it is reaped.
"""

import os
import unittest

import runregistrykit
from runregistrykit import stores
from runregistrykit.tests import test_host, test_store_retire
from runregistrykit.tests.test_end import a_hard_killed_run, a_status_of_its_own
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
TORN = dict((name, make) for name, make, _, _ in FORMS)["torn"]


class EndStoresTestCase(test_store_retire.RetireTestCase):
    def operations(self, primary, tag):
        """Each operation, by name, as a call on ``primary``, with destinations of ``tag``'s
        own."""
        elsewhere = self.top / f"C-{tag}"
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

    def refusals(self, primary, tag="refused") -> dict:
        """Each operation's refusal of ``primary``, by name; each leaves every file as it was."""
        messages = {}
        for operation, call in self.operations(primary, tag).items():
            with self.subTest(operation):
                before = self.state()
                with self.assertRaises(RuntimeError) as caught:
                    call()
                messages[operation] = str(caught.exception)
                self.assertEqual(self.state(), before, "a refusal changed a file")
        return messages


class TestEndingAHardKilledRun(EndStoresTestCase):
    def test_refused_until_it_is_ended_and_then_every_operation_proceeds(self):
        primary = self.a_full_store()
        path, _, _ = a_hard_killed_run(
            self, self.root, self.client, results=str(primary)
        )
        identifier = os.path.basename(path)
        (entry,) = runregistrykit.list_runs(root=self.root)
        self.assertEqual((entry["state"], entry["liveness"]), ("running", "stale"))

        for operation, message in self.refusals(primary, "before").items():
            with self.subTest(operation):
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
        (entry,) = runregistrykit.list_runs(root=self.root)
        self.assertEqual((entry["state"], entry["liveness"]), ("lost", "finished"))

        resumed = self.begin("resumed", results=str(primary))
        status = resumed.finish("done", exit_code=0, fingerprint=True)
        self.assertEqual((status["state"], status["exit_code"]), ("done", 0))
        self.assertIn("fingerprint", status)
        self.assertNotIn("fingerprint_error", status)

        operations = self.operations(primary, "after")
        for operation in (
            "fingerprint",
            "fingerprint --write",
            "retire --dry-run",
            "amend",
            "copy",
            "move",
        ):
            with self.subTest(operation):
                self.assertTrue(operations[operation]())
        self.assertTrue((self.top / "C-after" / "moved.sqlite").is_file())
        self.assertFalse(primary.exists())


class TestTheWords(EndStoresTestCase):
    def test_a_run_on_another_host_adds_the_sentence_once(self):
        primary = self.a_full_store()
        run = self.a_running_run("elsewhere", primary)
        a_status_of_its_own(
            run,
            host={
                "id": test_host.another_id(runregistrykit.this_host()["id"]),
                "boot": "a-boot",
            },
        )
        stale = self.a_stale_run("stale", primary)
        for operation, message in self.refusals(primary).items():
            with self.subTest(operation):
                self.assertIn(f"run {run.id} is running on another host", message)
                self.assertIn(f"run {stale.id} is running (stale, pid ", message)
                self.assertEqual(message.count(FOREIGN), 1, message)
                self.assertNotIn(REMEDY, message)
                self.assertNotIn("Run.finish", message)

    def test_a_run_whose_status_does_not_say_names_unverified(self):
        primary = self.a_full_store()
        run = self.a_running_run("torn", primary)
        give_status_the_form(run, TORN)
        for operation, message in self.refusals(primary).items():
            with self.subTest(operation):
                self.assertIn(f"run {run.id}'s status cannot be read", message)
                self.assertEqual(message.count(REMEDY), 1, message)
                self.assertIn(f"`{END} --unverified`", message)
                self.assertNotIn(FOREIGN, message)

    def test_alive_and_stale_here_give_the_old_text_with_the_command(self):
        primary = self.a_full_store()
        self.a_running_run("alive", primary)
        self.a_stale_run("stale", primary)
        client = runregistrykit.find_client_root(client_root=self.client)
        store_id = stores.read_sidecar(primary).store_id
        elsewhere = self.top / "C-refused"
        named = {
            "copy": [primary, elsewhere / "copy.sqlite"],
            "move": [primary, elsewhere / "moved.sqlite"],
        }
        command = "`" + END + "`"

        def described(operation):
            running = stores._running_runs_naming(
                operation.split()[0],
                named.get(operation, [primary]),
                store_id,
                self.root,
                client,
            )
            self.assertEqual(len(running), 2)
            return stores._describe_running(running)

        # the texts as they stood before this command existed, with `Run.finish` replaced
        expected = {
            "copy": f'Cannot copy "{primary}" to "{named["copy"][1]}": {described("copy")}. '
            f"A stale run is ended by a person, with {command}, before its store is moved; "
            f"the registry does not decide that a run is dead. Nothing was written",
            "move": f'Cannot move "{primary}" to "{named["move"][1]}": {described("move")}. '
            f"A stale run is ended by a person, with {command}, before its store is moved; "
            f"the registry does not decide that a run is dead. Nothing was written",
            "fingerprint": f'Cannot fingerprint "{primary}": {described("fingerprint")}. A '
            f"fingerprint of a store that is being written describes no instant; a stale run "
            f"is ended by a person, with {command}, first. Nothing was read or written",
            "retire --dry-run": f'Cannot retire "{primary}": {described("retire")}. A stale '
            f"run is ended by a person, with {command}, before its store is retired; the "
            f"registry does not decide that a run is dead. Once it is ended, `python -m "
            f'runregistrykit store fingerprint "{primary}" --write` records the fingerprint '
            f"that retirement needs. Nothing was written or deleted",
            "amend": f'Cannot amend "{primary}": {described("amend")}. A stale run is ended by '
            f"a person, with {command}, before its sidecar is amended; the registry does not "
            f"decide that a run is dead. Nothing was written",
        }
        expected["fingerprint --write"] = expected["fingerprint"]
        for operation, message in self.refusals(primary).items():
            with self.subTest(operation):
                self.assertEqual(message, expected[operation])
                self.assertNotIn(FOREIGN, message)
                self.assertNotIn("--unverified", message)


if __name__ == "__main__":
    unittest.main()
