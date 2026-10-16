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

"""A `running` run on another host is in use: the store operations refuse its store.

Its pid cannot be tested here, so the registry does not judge it, and a store it names is refused
by copy, move, fingerprint, retire (a dry run) and amend exactly as a store named by a run on this
host is. Each refusal names the run, says that it is on another host and names the host, by its
name or, when it records none, by its id, and leaves every file under the temporary directory as
it was. The run is built here: begun on a full registered store, with its status then saying that
another host wrote it and its pid one that is gone here, so that only the host keeps it from being
called stale.

Needs the store layer (`[stores]`). Stores are built by the retirement tests' fixture, in a
temporary directory with a runs root and a stores root of its own. No Ray is initialised.
"""

import unittest
from pathlib import Path

import runregistrykit
from runregistrykit import stores
from runregistrykit.tests import test_store_retire

ANOTHER_BOOT = "a-boot-of-another-host"


class TestARunOnAnotherHostIsInUse(test_store_retire.RetireTestCase):
    def a_foreign_run(self, slug, primary, name="far-host"):
        """A run on ``primary`` whose status names another host, and whose manifest names it
        ``name`` (None for none). Returns the run and the host's id."""
        run = self.a_running_run(slug, primary)
        here = runregistrykit.this_host()["id"]
        elsewhere = "f" * 16 if here != "f" * 16 else "e" * 16
        status = runregistrykit.read_json(run.status_path)
        status["host"] = {"id": elsewhere, "boot": ANOTHER_BOOT}
        status["pid"] = self.a_dead_pid()
        runregistrykit.write_json_atomic(run.status_path, status)
        manifest = runregistrykit.read_json(run.manifest_path)
        manifest["host"]["id"] = elsewhere
        manifest["host"]["name"] = name
        runregistrykit.write_json_atomic(run.manifest_path, manifest)
        (entry,) = [
            e for e in runregistrykit.list_runs(root=self.root) if e["id"] == run.id
        ]
        self.assertEqual(entry["liveness"], "foreign")
        return run, elsewhere

    def refusals(self, primary):
        """Each operation, by name, as a call that should refuse ``primary``."""
        return {
            "copy": lambda: stores.copy_store(
                primary, self.top / "C" / "copy.sqlite", "a copy", runs_root=self.root
            ),
            "move": lambda: stores.move_store(
                primary, self.top / "C" / "moved.sqlite", runs_root=self.root
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

    def assertEachRefuses(self, primary, *fragments):
        for operation, call in self.refusals(primary).items():
            with self.subTest(operation):
                before = self.state()
                with self.assertRaises(RuntimeError) as caught:
                    call()
                message = str(caught.exception)
                for fragment in fragments:
                    self.assertIn(fragment, message)
                self.assertEqual(self.state(), before, "a refusal changed a file")

    def test_each_operation_refuses_and_names_the_host(self):
        primary = self.a_full_store()
        run, elsewhere = self.a_foreign_run("far", primary)
        self.assertEachRefuses(
            primary,
            run.id,
            "is running on another host, far-host (pid ",
            "not tested here",
            "names this store by its results",
        )
        self.assertTrue(Path(primary).is_file())

    def test_a_host_with_no_name_is_named_by_its_id(self):
        primary = self.a_full_store()
        run, elsewhere = self.a_foreign_run("far-unnamed", primary, name=None)
        self.assertEachRefuses(
            primary, run.id, f"is running on another host, {elsewhere} (pid "
        )

    def test_a_foreign_run_that_has_finished_is_not_in_use(self):
        primary = self.a_full_store()
        run, _ = self.a_foreign_run("far-finished", primary)
        run.finish("done", exit_code=0)
        self.assertEqual(
            runregistrykit.read_json(run.status_path)["host"]["boot"], ANOTHER_BOOT
        )
        result = stores.fingerprint_store(primary, runs_root=self.root)
        self.assertTrue(result["fingerprint"])


if __name__ == "__main__":
    unittest.main()
