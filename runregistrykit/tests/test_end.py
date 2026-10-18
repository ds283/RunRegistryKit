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

"""Ending a run whose end the registry never saw: `python -m runregistrykit end` and the private
function behind it, `runregistrykit._end_run`.

A run killed outright never reaches `Run.finish`, so its status says `running` for ever. `end`
records it as `lost`, with exit code null and an `ended` record of who, when, why, at what
`git_head`, on what host, and the evidence checked, once the evidence on this machine says the run
is over: on this host, a boot other than this one, or a pid that does not answer `kill -0`. A pid
that answers here is refused, `--unverified` or not. A run on another host, or whose status does
not say whether it is running, is ended only with `--unverified`. A run that has ended is refused.
Every refusal writes nothing, and an acceptance writes `status.json` alone.

The core only: nothing of the store layer is imported, so that the core job can run this module.
Every run is built in a temporary directory. One test starts a child process, which begins a run,
and sends it `SIGKILL` (`Popen.kill`), the only process any test here signals; it is reaped, and
a cleanup kills and reaps it whatever fails. No test here builds a process that has been killed
and not reaped: the live-pid refusal's words are pinned on a run begun in this process.
"""

import getpass
import json
import os
import subprocess
import sys
import unittest
from datetime import datetime
from unittest import mock

import runregistrykit
from runregistrykit.tests import test_host, test_run_registry
from runregistrykit.tests.client_fixtures import (
    PACKAGE_PARENT,
    git,
    temporary_directory,
)
from runregistrykit.tests.test_unreadable_status import FORMS, give_status_the_form

END = runregistrykit._END

ENDED_KEYS = {
    "by",
    "at",
    "reason",
    "git_head",
    "host",
    "verified",
    "not_verified_because",
    "evidence",
}
EVIDENCE_KEYS = {
    "state",
    "status_readable",
    "pid",
    "pid_answers",
    "host",
    "boot",
    "heartbeat",
    "heartbeat_age",
}
# the keys an acceptance writes, beside every key the status already held
WRITTEN = {"state", "exit_code", "ended", "heartbeat"}

REASON = "  killed by the OOM killer, checked by a person  "

# the live-pid refusal, in the words a person reads
LIVE_PID = (
    "answers kill -0, so a process with that pid exists on this host",
    "--unverified does not override this",
    "A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, "
    "until its parent waits for it or exits",
)

# the three forms that are readable and keep the full status, its pid among them
WITH_A_PID = ("null state", "paused", "state 5")

# a child that begins a run, heartbeats, says where its run is, and waits to be killed
CHILD = """\
import sys, time

sys.path.insert(0, sys.argv[1])
import runregistrykit

run = runregistrykit.begin(
    campaign="example",
    prompt="01",
    slug=sys.argv[5],
    purpose="a run that is killed outright",
    root=sys.argv[2],
    client_root=sys.argv[3],
    argv=["a-child"],
    results=sys.argv[4] or None,
)
run.heartbeat(units_done=1, stage="working")
print(run.path, flush=True)
time.sleep(600)
"""


def _reap(child) -> None:
    """Kill ``child`` if it is still running, and wait for it, whatever has happened."""
    if child.poll() is None:
        child.kill()
    child.wait(timeout=60)
    for pipe in (child.stdout, child.stderr):
        if pipe is not None:
            pipe.close()


def a_hard_killed_run(test, root, client, results=None, slug="hard-killed"):
    """A run begun by a child process, which heartbeats and is then sent `SIGKILL` and reaped.
    Returns (the run's path, the child's pid, its status's bytes before the kill)."""
    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            CHILD,
            PACKAGE_PARENT,
            root,
            client,
            results or "",
            slug,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=client,
    )
    test.addCleanup(_reap, child)
    path = child.stdout.readline().strip()
    if not path:
        child.kill()
        child.wait(timeout=60)
        test.fail(f"the child began no run: {child.stderr.read()}")
    with open(os.path.join(path, "status.json"), "rb") as handle:
        before = handle.read()
    child.kill()
    test.assertEqual(child.wait(timeout=60), -9)
    with open(os.path.join(path, "status.json"), "rb") as handle:
        test.assertEqual(handle.read(), before, "the kill changed the status")
    return path, child.pid, before


def files(path) -> dict:
    """Every file in the run directory ``path``, by name, with its bytes."""
    found = {}
    for name in sorted(os.listdir(path)):
        with open(os.path.join(path, name), "rb") as handle:
            found[name] = handle.read()
    return found


def a_status_of_its_own(run, **fields) -> dict:
    """Give ``run``'s status ``fields``, written by hand as a test builds a record; return it."""
    status = dict(runregistrykit.read_json(run.status_path), **fields)
    runregistrykit.write_json_atomic(run.status_path, status)
    return status


class EndTestCase(test_run_registry.RegistryTestCase):
    def end(self, path, reason=REASON, **kwargs):
        return runregistrykit._end_run(path, reason, client_root=self.client, **kwargs)

    def here(self) -> dict:
        return runregistrykit.this_host()

    def assertRefused(self, path, *fragments, reason=REASON, **kwargs) -> str:
        """`_end_run` refuses ``path``, naming ``fragments``, and every file in it is as it
        was."""
        before = files(path) if os.path.isdir(path) else None
        with self.assertRaises(RuntimeError) as caught:
            self.end(path, reason, **kwargs)
        message = str(caught.exception)
        self.assertTrue(
            message.startswith(f"Cannot end {os.path.basename(path)}: "), message
        )
        self.assertTrue(message.endswith("Nothing was written"), message)
        for fragment in fragments:
            self.assertIn(fragment, message)
        if before is not None:
            self.assertEqual(files(path), before, "a refusal changed a file")
        return message

    def assertEnded(self, path, before, written, **evidence) -> dict:
        """``written`` is what `_end_run` returned for the run at ``path``, whose status was
        ``before`` (a dict, or None where it was not an object): it is the file, every field of
        ``before`` is kept but the four written, and `ended` holds exactly its keys, with
        ``evidence``'s values (and `verified` and `not_verified_because`, given in it too).
        """
        status = runregistrykit.read_json(os.path.join(path, "status.json"))
        self.assertEqual(status, written)
        kept = before if isinstance(before, dict) else {}
        self.assertEqual(set(status), set(kept) | WRITTEN)
        for key, value in kept.items():
            if key not in WRITTEN:
                self.assertEqual(status[key], value, key)
        self.assertEqual((status["state"], status["exit_code"]), ("lost", None))
        ended = status["ended"]
        self.assertEqual(set(ended), ENDED_KEYS)
        self.assertEqual(set(ended["evidence"]), EVIDENCE_KEYS)
        self.assertEqual(ended["by"], getpass.getuser())
        self.assertIsNotNone(datetime.fromisoformat(ended["at"]).tzinfo)
        self.assertEqual(ended["reason"], REASON.strip())
        self.assertEqual(ended["git_head"], git(self.client, "rev-parse", "HEAD"))
        here = self.here()
        self.assertEqual(
            ended["host"], {key: here[key] for key in ("id", "boot", "name")}
        )
        self.assertEqual(ended["verified"], evidence.pop("verified"))
        self.assertEqual(ended["not_verified_because"], evidence.pop("because"))
        for key, value in evidence.items():
            self.assertEqual(ended["evidence"][key], value, key)
        self.assertEqual(ended["evidence"]["status_readable"], isinstance(before, dict))
        self.assertEqual(ended["evidence"]["state"], kept.get("state"))
        self.assertEqual(ended["evidence"]["pid"], kept.get("pid"))
        self.assertEqual(ended["evidence"]["heartbeat"], kept.get("heartbeat"))
        age = ended["evidence"]["heartbeat_age"]
        if kept.get("heartbeat") is None:
            self.assertIsNone(age)
        else:
            self.assertIsInstance(age, float)
            self.assertGreaterEqual(age, 0.0)
        return status

    def this(self) -> tuple:
        """`evidence.host` and `evidence.boot` for a status `begin` wrote in this process."""
        here = self.here()
        if here["id"] is None:
            return "not recorded", None
        return "this", ("this" if here["boot"] is not None else "not recorded")

    def entry(self, path):
        (found,) = [
            e
            for e in runregistrykit.list_runs(root=self.root)
            if e["path"] == os.path.abspath(path)
        ]
        return found

    def an_identity_or_skip(self):
        here = self.here()
        if here["id"] is None or here["boot"] is None:
            self.skipTest("this platform offers no host or boot identity")
        return here


class TestAHardKilledRun(EndTestCase):
    def test_a_child_killed_outright_is_ended_verified(self):
        path, pid, before = a_hard_killed_run(self, self.root, self.client)
        before = json.loads(before)
        self.assertEqual(self.entry(path)["liveness"], "stale")
        written = self.end(path)
        status = self.assertEnded(
            path,
            before,
            written,
            verified=True,
            because=None,
            pid_answers=False,
        )
        self.assertEqual(status["ended"]["evidence"]["pid"], pid)
        self.assertEqual(status["ended"]["evidence"]["heartbeat"], before["heartbeat"])
        self.assertEqual((status["units_done"], status["stage"]), (1, "working"))
        entry = self.entry(path)
        self.assertEqual((entry["state"], entry["liveness"]), ("lost", "finished"))
        self.an_identity_or_skip()
        self.assertEqual(status["ended"]["evidence"]["host"], "this")
        self.assertEqual(status["ended"]["evidence"]["boot"], "this")


class TestRefusals(EndTestCase):
    def test_a_live_pid_is_refused_with_or_without_unverified(self):
        run = self.begin("alive")
        for unverified in (False, True):
            with self.subTest(unverified=unverified):
                self.assertRefused(
                    run.path,
                    f"its pid {os.getpid()} answers kill -0",
                    *LIVE_PID,
                    unverified=unverified,
                )

    def test_a_run_that_has_ended_is_refused(self):
        for state in runregistrykit.TERMINAL_STATES:
            with self.subTest(state):
                if state == "lost":
                    run, _ = self.a_dead_run(f"ended-{state}")
                    self.end(run.path)
                else:
                    run = self.begin(f"ended-{state}")
                    run.finish(state, exit_code=0)
                for unverified in (False, True):
                    self.assertRefused(
                        run.path,
                        f"its status says it has already ended, as {state!r}",
                        unverified=unverified,
                    )

    def test_a_run_on_another_host_is_refused_without_unverified(self):
        elsewhere = test_host.another_id(self.here()["id"])
        for named in (True, False):
            with self.subTest(named=named):
                run = self.begin(f"elsewhere-{named}")
                a_status_of_its_own(run, host={"id": elsewhere, "boot": "a-boot"})
                manifest = runregistrykit.read_json(run.manifest_path)
                manifest["host"]["name"] = "far-host" if named else None
                runregistrykit.write_json_atomic(run.manifest_path, manifest)
                with mock.patch.object(
                    runregistrykit, "pid_alive", side_effect=AssertionError("tested")
                ):
                    self.assertRefused(
                        run.path,
                        f"it is running on another host, "
                        f"{'far-host' if named else elsewhere} (pid {os.getpid()}, not "
                        f"tested here)",
                        f"It is ended with `{END}` on that host, or here with "
                        f"`--unverified` once a person has checked there",
                    )

    def test_each_form_is_refused_without_unverified(self):
        for i, (name, make, _, words) in enumerate(FORMS):
            with self.subTest(name):
                run, _ = self.a_dead_run(f"form-{i}")
                give_status_the_form(run, make)
                self.assertRefused(
                    run.path,
                    f"its {words}",
                    "so whether it is running cannot be told here",
                    f"Once a person has checked that it is not, `{END} --unverified` ends "
                    f"it, recorded as not verified",
                )

    def test_a_readable_status_of_no_state_with_a_live_pid_is_refused_with_unverified(
        self,
    ):
        for i, name in enumerate(WITH_A_PID):
            make = dict((n, m) for n, m, _, _ in FORMS)[name]
            for unverified in (True, False):
                with self.subTest(name, unverified=unverified):
                    run = self.begin(f"live-{i}-{unverified}")
                    give_status_the_form(run, make)
                    self.assertRefused(
                        run.path,
                        f"its pid {os.getpid()} answers kill -0",
                        *LIVE_PID,
                        unverified=unverified,
                    )

    def test_an_empty_reason_is_refused(self):
        run, _ = self.a_dead_run("no-reason")
        for reason in ("", "   ", "\n\t", None):
            with self.subTest(reason=reason):
                self.assertRefused(
                    run.path,
                    "a reason is required, saying why the run is ended",
                    reason=reason,
                    unverified=True,
                )

    def test_a_directory_holding_neither_file_is_refused(self):
        predates = os.path.join(self.root, "predates-the-registry")
        os.mkdir(predates)
        with open(os.path.join(predates, "notes.txt"), "w") as handle:
            handle.write("a directory the registry did not write\n")
        self.assertRefused(
            predates,
            "holds neither a manifest.json nor a status.json",
            unverified=True,
        )
        self.assertEqual(os.listdir(predates), ["notes.txt"])
        loose = os.path.join(self.root, "a-loose-file")
        with open(loose, "w") as handle:
            handle.write("not a directory\n")
        self.assertRefused(loose, "is not a directory", unverified=True)


class TestAcceptances(EndTestCase):
    def test_a_dead_pid(self):
        run, dead = self.a_dead_run("dead")
        run.heartbeat(units_done=3, stage="the third stage")
        run._update(fingerprint_error="a field the status already held")
        before = runregistrykit.read_json(run.status_path)
        host, boot = self.this()
        status = self.assertEnded(
            run.path,
            before,
            self.end(run.path),
            verified=True,
            because=None,
            pid_answers=False,
            host=host,
            boot=boot,
        )
        self.assertEqual(status["ended"]["evidence"]["pid"], dead)
        self.assertEqual(self.entry(run.path)["liveness"], "finished")

    def test_a_running_status_with_no_pid_is_tested_and_accepted(self):
        run = self.begin("no-pid")
        before = a_status_of_its_own(run, pid=None)
        self.assertEqual(self.entry(run.path)["liveness"], "stale")
        self.assertEnded(
            run.path,
            before,
            self.end(run.path),
            verified=True,
            because=None,
            pid_answers=False,
        )

    def test_a_live_pid_from_an_earlier_boot_is_accepted_untested(self):
        here = self.an_identity_or_skip()
        run = self.begin("earlier-boot")
        before = a_status_of_its_own(
            run, host={"id": here["id"], "boot": here["boot"] + "-earlier"}
        )
        self.assertEqual(self.entry(run.path)["liveness"], "stale")
        with mock.patch.object(
            runregistrykit, "pid_alive", side_effect=AssertionError("tested")
        ):
            written = self.end(run.path)
        self.assertEnded(
            run.path,
            before,
            written,
            verified=True,
            because=None,
            pid_answers=None,
            host="this",
            boot="earlier",
        )

    def test_another_host_with_unverified(self):
        run = self.begin("elsewhere")
        before = a_status_of_its_own(
            run,
            host={"id": test_host.another_id(self.here()["id"]), "boot": "a-boot"},
        )
        with mock.patch.object(
            runregistrykit, "pid_alive", side_effect=AssertionError("tested")
        ):
            written = self.end(run.path, unverified=True)
        self.assertEnded(
            run.path,
            before,
            written,
            verified=False,
            because="another host",
            pid_answers=None,
            host="another",
            boot=None,
        )

    def test_each_form_with_unverified(self):
        here = self.this()
        for i, (name, make, readable, _) in enumerate(FORMS):
            with self.subTest(name):
                run, _ = self.a_dead_run(f"form-{i}")
                give_status_the_form(run, make)
                raw = runregistrykit.read_json(run.status_path)
                before = raw if isinstance(raw, dict) else None
                names = sorted(os.listdir(run.path))
                tested = name in WITH_A_PID
                host, boot = here if tested else ("not recorded", None)
                self.assertEnded(
                    run.path,
                    before,
                    self.end(run.path, unverified=True),
                    verified=False,
                    because="status does not say",
                    pid_answers=False if tested else None,
                    host=host,
                    boot=boot,
                )
                self.assertEqual(
                    sorted(os.listdir(run.path)),
                    sorted(set(names) | {"status.json"}),
                )
                self.assertEqual(self.entry(run.path)["liveness"], "finished")

    def test_unverified_where_it_is_not_needed_changes_nothing(self):
        run, _ = self.a_dead_run("not-needed")
        before = runregistrykit.read_json(run.status_path)
        self.assertEnded(
            run.path,
            before,
            self.end(run.path, unverified=True),
            verified=True,
            because=None,
            pid_answers=False,
        )


class TestWhatIsNotWritten(EndTestCase):
    def test_the_manifest_the_ledger_and_no_other_file(self):
        run = self.begin("with-a-ledger", checkpoint=True)
        run.record("unit-1", {"value": 1})
        run.heartbeat(pid=self.a_dead_pid())
        before = files(run.path)
        self.assertEqual(
            sorted(before), ["checkpoint.jsonl", "manifest.json", "status.json"]
        )
        self.end(run.path)
        after = files(run.path)
        self.assertEqual(sorted(after), sorted(before))
        self.assertEqual(after["manifest.json"], before["manifest.json"])
        self.assertEqual(after["checkpoint.jsonl"], before["checkpoint.jsonl"])
        self.assertNotEqual(after["status.json"], before["status.json"])

    def test_a_run_with_no_manifest_is_judged_by_its_status(self):
        run, _ = self.a_dead_run("no-manifest")
        os.remove(run.manifest_path)
        before = runregistrykit.read_json(run.status_path)
        self.assertEnded(
            run.path,
            before,
            self.end(run.path),
            verified=True,
            because=None,
            pid_answers=False,
        )
        self.assertEqual(os.listdir(run.path), ["status.json"])


class TestAnOldRecord(EndTestCase):
    """A status written by `v0.1.0`, with no `host`, is judged by its pid, as `liveness` judges
    it, and ended without one being added."""

    def test_a_dead_pid_is_ended_and_a_live_one_refused(self):
        dead = self.begin("old-dead")
        before = test_host.a_status(self.a_dead_pid(), with_host=False)
        runregistrykit.write_json_atomic(dead.status_path, before)
        status = self.assertEnded(
            dead.path,
            before,
            self.end(dead.path),
            verified=True,
            because=None,
            pid_answers=False,
            host="not recorded",
            boot=None,
        )
        self.assertNotIn("host", status)

        alive = self.begin("old-alive")
        runregistrykit.write_json_atomic(
            alive.status_path, test_host.a_status(os.getpid(), with_host=False)
        )
        self.assertEqual(self.entry(alive.path)["liveness"], "alive")
        self.assertRefused(alive.path, *LIVE_PID, unverified=True)


class TestTheState(unittest.TestCase):
    def test_lost_is_terminal_and_finished_here_and_from_another_host(self):
        self.assertEqual(
            runregistrykit.TERMINAL_STATES, ("done", "failed", "killed", "lost")
        )
        for host in (test_host.HERE, test_host.ELSEWHERE, None):
            with self.subTest(host=host):
                status = test_host.a_status(
                    os.getpid(), host, state="lost", with_host=host is not None
                )
                self.assertEqual(
                    runregistrykit.liveness(status, 900.0, here=test_host.HERE),
                    "finished",
                )


class TestFinishIsNotChanged(EndTestCase):
    def test_finish_accepts_lost_as_any_terminal_state_and_writes_no_record(self):
        run = self.begin("finished-lost")
        status = run.finish("lost")
        self.assertEqual((status["state"], status["exit_code"]), ("lost", None))
        self.assertNotIn("ended", status)
        with self.assertRaises(ValueError):
            self.begin("paused").finish("paused")


class TestTheCommand(EndTestCase):
    def command(self, *argv, cwd=None):
        return subprocess.run(
            [sys.executable, "-m", "runregistrykit", *[str(a) for a in argv]],
            capture_output=True,
            text=True,
            cwd=cwd or self.client,
            env={**os.environ, "PYTHONPATH": PACKAGE_PARENT},
            timeout=300,
        )

    def assertCommandRefused(self, run, *argv, fragment, **kwargs) -> str:
        before = files(run.path)
        done = self.command(*argv, **kwargs)
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertEqual(done.stdout, "")
        self.assertTrue(done.stderr.startswith("!! Cannot end "), done.stderr)
        self.assertTrue(done.stderr.rstrip("\n").endswith("Nothing was written"))
        self.assertIn(fragment, done.stderr)
        self.assertEqual(files(run.path), before, "a refused command wrote something")
        return done.stderr

    def test_success_prints_one_line_and_exits_0(self):
        run, dead = self.a_dead_run("by-command")
        done = self.command("end", run.id, "--reason", REASON, "--root", self.root)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(
            done.stdout,
            f">> end: {run.id} is now lost, verified: its pid {dead} does not answer "
            f"kill -0 on this host\n",
        )
        status = run.status()
        self.assertEqual((status["state"], status["ended"]["verified"]), ("lost", True))

    def test_the_runs_root_defaults_to_the_client_configs(self):
        dead = self.a_dead_pid()
        run = runregistrykit.begin(
            campaign="example",
            prompt="01",
            slug="default-root",
            purpose="a run under the client's own runs root",
            argv=["unittest"],
            client_root=self.client,
        )
        run.heartbeat(pid=dead)
        done = self.command("end", run.id, "--reason", REASON)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn(f">> end: {run.id} is now lost, verified", done.stdout)

    def test_unverified_says_so(self):
        run = self.begin("elsewhere")
        a_status_of_its_own(
            run, host={"id": test_host.another_id(self.here()["id"]), "boot": "b"}
        )
        args = ("end", run.id, "--reason", REASON, "--root", self.root)
        self.assertCommandRefused(run, *args, fragment="running on another host")
        done = self.command(*args, "--unverified")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(
            done.stdout,
            f">> end: {run.id} is now lost, not verified (another host): on a person's "
            f"word, with --unverified\n",
        )

    def test_a_refusal_prints_it_and_exits_1(self):
        run = self.begin("alive")
        self.assertCommandRefused(
            run,
            "end",
            run.id,
            "--reason",
            REASON,
            "--unverified",
            "--root",
            self.root,
            fragment=LIVE_PID[1],
        )

    def test_a_run_id_that_is_a_path_is_refused(self):
        run, _ = self.a_dead_run("a-path")
        for name in (run.path, f"{run.id}/", f"../{run.id}", "a/b", ".", "..", ""):
            with self.subTest(name=name):
                self.assertCommandRefused(
                    run,
                    "end",
                    name,
                    "--reason",
                    REASON,
                    "--root",
                    self.root,
                    fragment="is a run id, the name of a directory under the runs root, "
                    "not a path",
                )

    def test_no_such_run_is_refused(self):
        run, _ = self.a_dead_run("there")
        self.assertCommandRefused(
            run,
            "end",
            "no-such-run",
            "--reason",
            REASON,
            "--root",
            self.root,
            fragment=f"there is no run directory {os.path.join(self.root, 'no-such-run')}",
        )

    def test_no_client_root_is_refused(self):
        run, _ = self.a_dead_run("no-client")
        before = files(run.path)
        nowhere = temporary_directory(self)
        done = self.command(
            "--client-root",
            nowhere,
            "end",
            run.id,
            "--reason",
            REASON,
            "--root",
            self.root,
        )
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertTrue(done.stderr.startswith("!! "), done.stderr)
        self.assertIn(runregistrykit.CONFIG_FILE, done.stderr)
        self.assertEqual(files(run.path), before)

    def test_list_afterwards(self):
        ended, _ = self.a_dead_run("ended")
        stale, _ = self.a_dead_run("still-stale")
        done = self.command("end", ended.id, "--reason", REASON, "--root", self.root)
        self.assertEqual(done.returncode, 0, done.stderr)
        listed = self.command("list", "--root", self.root)
        self.assertEqual(listed.returncode, 0, listed.stderr)
        (row,) = [line for line in listed.stdout.splitlines() if ended.id in line]
        self.assertTrue(row.startswith("   "), row)
        self.assertIn(" lost ", row)
        (row,) = [line for line in listed.stdout.splitlines() if stale.id in line]
        self.assertTrue(row.startswith("!! "), row)
        lines = [line for line in listed.stderr.splitlines() if line.startswith("!! ")]
        self.assertEqual(len(lines), 1, listed.stderr)
        self.assertTrue(lines[0].startswith("!! 1 run(s) say they are running"))
        self.assertTrue(
            lines[0].endswith(
                "Nothing here has killed or cleaned anything — go and look. Once you know "
                f"one is over, end it with `{END}`."
            ),
            lines[0],
        )
        self.assertIn("1 finished, 1 stale", listed.stdout)


if __name__ == "__main__":
    unittest.main()
