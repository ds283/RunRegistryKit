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

"""The host a run is on: `this_host()` and its three private readers, what `begin` writes of it,
how `liveness` and `list_runs` judge a record by it, and what `list` prints.

The core only: nothing of the store layer is imported, so that the core job can run this module.
Every record judged here is built in the test, with a host of its own, and judged with `here=`
given or with the private readers patched, so that no assertion depends on which machine runs it.
The exceptions are the readers on this platform, which ask the machine itself and are skipped
where the platform is neither macOS nor Linux, and the test that no raw identity reaches a file.
No assertion prints an identity read from the machine, so that a failure's message holds none.
"""

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock

import runregistrykit
from runregistrykit.tests import test_run_registry

HEX16 = re.compile(r"[0-9a-f]{16}")
UUID_TEXT = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
MACHINE_ID = re.compile(r"[0-9a-f]{32}")

HOST_KEYS = {"id", "name", "machine", "system", "release", "python"}
STATUS_HOST_KEYS = {"id", "boot"}

# the values the patched readers give, none of them anything a machine reports
RAW = "a-raw-identity-made-up-for-a-test"
BOOT = "a-boot-made-up-for-a-test"
NAME = "a-name-made-up-for-a-test"

# two hosts of the tests' own: "here" is the machine judging, "elsewhere" another one
HERE = {"id": "1" * 16, "boot": "boot-one", "name": "here"}
ELSEWHERE = {"id": "2" * 16, "boot": "boot-two"}


def digest(raw) -> str:
    return hashlib.sha256(b"runregistrykit host\0" + raw.encode()).hexdigest()[:16]


def readers(machine=RAW, boot=BOOT, name=NAME):
    """The three private readers patched to give these values."""
    return mock.patch.multiple(
        runregistrykit,
        _read_machine_identity=mock.Mock(return_value=machine),
        _read_boot_identity=mock.Mock(return_value=boot),
        _read_host_name=mock.Mock(return_value=name),
    )


def stamp(seconds_ago=0.0) -> str:
    when = datetime.now(timezone.utc) - timedelta(seconds=seconds_ago)
    return when.astimezone().isoformat(timespec="seconds")


def a_status(pid, host=None, *, state="running", seconds_ago=0.0, with_host=True):
    """A `status.json` payload. With ``with_host`` false it has no `host` at all, as every
    status written before the host was recorded has not."""
    status = {
        "state": state,
        "units_done": 0,
        "units_total": None,
        "pid": pid,
        "exit_code": None,
        "heartbeat": stamp(seconds_ago),
    }
    if with_host:
        status["host"] = host
    return status


def another_id(than) -> str:
    """A 16-hex id that is not ``than``."""
    return "f" * 16 if than != "f" * 16 else "e" * 16


class TestTheReaders(unittest.TestCase):
    """`this_host()` and the readers behind it."""

    def assertAnIdentity(self, first, second):
        self.assertTrue(
            isinstance(first["id"], str) and HEX16.fullmatch(first["id"]),
            "this_host()'s id is not 16 hex characters",
        )
        self.assertTrue(
            isinstance(first["boot"], str) and first["boot"],
            "this_host()'s boot is not a non-empty string",
        )
        self.assertTrue(first == second, "two calls of this_host() disagree")

    @unittest.skipUnless(
        platform.system() == "Darwin",
        "the macOS readers run only on macOS; the Linux test runs on Linux, in CI",
    )
    def test_the_readers_on_macos(self):
        self.assertAnIdentity(runregistrykit.this_host(), runregistrykit.this_host())
        raw = runregistrykit._read_machine_identity()
        self.assertTrue(
            UUID_TEXT.fullmatch(raw or ""),
            "the macOS machine identity is not a UUID in lowercase text",
        )
        self.assertTrue(
            digest(raw) == runregistrykit.this_host()["id"],
            "this_host()'s id is not the digest of the machine identity",
        )
        boot = runregistrykit._read_boot_identity()
        self.assertTrue(
            UUID_TEXT.fullmatch((boot or "").lower()),
            "the macOS boot identity is not a UUID",
        )

    @unittest.skipUnless(
        platform.system() == "Linux",
        "the Linux readers run only on Linux, which CI's runner is; the macOS test runs on macOS",
    )
    def test_the_readers_on_linux(self):
        self.assertAnIdentity(runregistrykit.this_host(), runregistrykit.this_host())
        raw = runregistrykit._read_machine_identity()
        self.assertTrue(
            MACHINE_ID.fullmatch(raw or ""),
            "the Linux machine identity is not 32 lowercase hex characters",
        )
        self.assertTrue(
            digest(raw) == runregistrykit.this_host()["id"],
            "this_host()'s id is not the digest of the machine identity",
        )

    def test_the_keys_and_the_platform_fields(self):
        host = runregistrykit.this_host()
        self.assertEqual(set(host), HOST_KEYS | {"boot"})
        self.assertEqual(host["machine"], platform.machine())
        self.assertEqual(host["system"], platform.system())
        self.assertEqual(host["release"], platform.release())
        self.assertEqual(host["python"], platform.python_version())

    def test_the_id_is_a_digest_of_the_raw_identity(self):
        with readers():
            host = runregistrykit.this_host()
        self.assertEqual(host["id"], digest(RAW))
        self.assertTrue(HEX16.fullmatch(host["id"]))
        self.assertNotIn(RAW, json.dumps(host))
        self.assertEqual(host["boot"], BOOT)
        self.assertEqual(host["name"], NAME)

    def test_it_reads_afresh_on_each_call(self):
        with readers(boot="the-first-boot"):
            first = runregistrykit.this_host()
        with readers(boot="the-second-boot"):
            second = runregistrykit.this_host()
        self.assertEqual(
            (first["boot"], second["boot"]), ("the-first-boot", "the-second-boot")
        )

    def test_the_name(self):
        with mock.patch.dict(os.environ, {"RUNREGISTRYKIT_HOST_NAME": "set-by-hand"}):
            self.assertEqual(runregistrykit.this_host()["name"], "set-by-hand")
        with mock.patch.dict(os.environ, {"RUNREGISTRYKIT_HOST_NAME": ""}):
            with mock.patch("platform.node", return_value="the-node"):
                self.assertEqual(runregistrykit.this_host()["name"], "the-node")
        environment = {
            k: v for k, v in os.environ.items() if k != "RUNREGISTRYKIT_HOST_NAME"
        }
        with mock.patch.dict(os.environ, environment, clear=True):
            with mock.patch("platform.node", return_value="the-node"):
                self.assertEqual(runregistrykit.this_host()["name"], "the-node")
            with mock.patch("platform.node", return_value=""):
                self.assertIsNone(runregistrykit.this_host()["name"])
            with mock.patch("platform.node", side_effect=OSError("no node")):
                self.assertIsNone(runregistrykit.this_host()["name"])

    def test_a_reader_that_fails_gives_none_there(self):
        readers_and_keys = (
            ("_read_machine_identity", "id"),
            ("_read_boot_identity", "boot"),
            ("_read_host_name", "name"),
        )
        failures = {
            "raises OSError": mock.Mock(side_effect=OSError("injected")),
            "raises ValueError": mock.Mock(side_effect=ValueError("injected")),
            "returns None": mock.Mock(return_value=None),
            "returns nothing": mock.Mock(return_value=""),
            "returns a number": mock.Mock(return_value=7),
        }
        for reader, key in readers_and_keys:
            for label, failing in failures.items():
                with self.subTest(reader=reader, failure=label), readers():
                    with mock.patch.object(runregistrykit, reader, failing):
                        host = runregistrykit.this_host()
                    self.assertIsNone(host[key])
                    expected = {"id": digest(RAW), "boot": BOOT, "name": NAME}
                    for other in set(expected) - {key}:
                        self.assertEqual(host[other], expected[other])

    def test_a_platform_that_is_neither_gives_no_identity(self):
        with mock.patch("platform.system", return_value="Plan9"):
            self.assertIsNone(runregistrykit._read_machine_identity())
            self.assertIsNone(runregistrykit._read_boot_identity())
            host = runregistrykit.this_host()
        self.assertIsNone(host["id"])
        self.assertIsNone(host["boot"])

    def test_the_linux_files(self):
        """The Linux branch, on any platform, by its files in a temporary directory."""
        with tempfile.TemporaryDirectory() as directory:

            def put(name, text):
                path = os.path.join(directory, name)
                with open(path, "w") as handle:
                    handle.write(text)
                return path

            missing = os.path.join(directory, "missing")
            upper = put("upper", "0123456789ABCDEF0123456789ABCDEF\n")
            empty = put("empty", "\n")
            malformed = put("malformed", "not a machine id\n")
            boot = put("boot", "  a-boot-id-of-a-test\n")
            cases = {
                "the first file": ((upper, missing), "0123456789abcdef" * 2),
                "the second, the first missing": (
                    (missing, upper),
                    "0123456789abcdef" * 2,
                ),
                "the second, the first empty": ((empty, upper), "0123456789abcdef" * 2),
                "both missing": ((missing, missing), None),
                "both empty or malformed": ((empty, malformed), None),
            }
            with mock.patch("platform.system", return_value="Linux"):
                for label, (files, expected) in cases.items():
                    with (
                        self.subTest(label),
                        mock.patch.object(runregistrykit, "_MACHINE_ID_FILES", files),
                    ):
                        self.assertEqual(
                            runregistrykit._read_machine_identity(), expected
                        )
                for path, expected in (
                    (boot, "a-boot-id-of-a-test"),
                    (empty, None),
                    (missing, None),
                    (directory, None),
                ):
                    with (
                        self.subTest(boot=os.path.basename(path)),
                        mock.patch.object(runregistrykit, "_BOOT_ID_FILE", path),
                    ):
                        self.assertEqual(runregistrykit._read_boot_identity(), expected)

    def test_the_macos_calls_failing(self):
        """The macOS branch, on any platform, with the C library replaced."""

        class Function:
            def __init__(self, result):
                self.result = result

            def __call__(self, *args):
                return self.result

        class Library:
            def __init__(self, result):
                self.gethostuuid = Function(result)
                self.sysctlbyname = Function(result)

        cases = {
            "no C library found": dict(find=None),
            "the library does not load": dict(load=OSError("injected")),
            "a nonzero return": dict(library=Library(1)),
            "a zero return and nothing written": dict(library=Library(0)),
            "no such function": dict(library=object()),
        }
        for label, case in cases.items():
            with self.subTest(label):
                load = mock.Mock(
                    side_effect=case.get("load"), return_value=case.get("library")
                )
                with (
                    mock.patch("platform.system", return_value="Darwin"),
                    mock.patch(
                        "ctypes.util.find_library",
                        return_value=case.get("find", "libc"),
                    ),
                    mock.patch("ctypes.CDLL", load),
                ):
                    self.assertIsNone(runregistrykit._read_machine_identity())
                    self.assertIsNone(runregistrykit._read_boot_identity())


class TestWhatIsWritten(test_run_registry.RegistryTestCase):
    """The manifest's `host` and the status's, and every later write keeping the status's."""

    def test_the_manifest_and_the_first_status(self):
        with readers():
            run = self.begin("written")
        manifest = runregistrykit.read_json(run.manifest_path)
        status = runregistrykit.read_json(run.status_path)
        self.assertEqual(set(manifest["host"]), HOST_KEYS)
        self.assertEqual(
            manifest["host"],
            {
                "id": digest(RAW),
                "name": NAME,
                "machine": platform.machine(),
                "system": platform.system(),
                "release": platform.release(),
                "python": platform.python_version(),
            },
        )
        self.assertEqual(set(status["host"]), STATUS_HOST_KEYS)
        self.assertEqual(status["host"], {"id": digest(RAW), "boot": BOOT})

    def test_the_host_is_read_once_by_begin(self):
        with (
            readers(),
            mock.patch.object(
                runregistrykit, "this_host", wraps=runregistrykit.this_host
            ) as asked,
        ):
            self.begin("once")
        self.assertEqual(asked.call_count, 1)

    def test_every_later_write_keeps_the_status_host(self):
        with readers():
            run = self.begin("kept", checkpoint=True)
        written = {"id": digest(RAW), "boot": BOOT}
        other = self.a_dead_pid()
        # what the readers now say is not what the run recorded, and must not replace it
        with readers(machine="another-raw-identity", boot="another-boot"):
            for label, write in (
                ("a heartbeat", lambda: run.heartbeat(units_done=1)),
                ("a heartbeat with a stage", lambda: run.heartbeat(stage="stage two")),
                ("a launcher's heartbeat", lambda: run.heartbeat(pid=other)),
                ("a recorded unit", lambda: run.record("u1", {"x": 1})),
                ("a finish", lambda: run.finish("done", exit_code=0)),
            ):
                with self.subTest(label):
                    write()
                    self.assertEqual(run.status()["host"], written)
        self.assertEqual(run.status()["pid"], other)
        self.assertEqual(run.status()["state"], "done")

    def test_no_raw_identity_reaches_a_file(self):
        raw = runregistrykit._read_machine_identity()
        if raw is None:
            self.skipTest("this platform offers no machine identity to leak")
        forms = {raw, raw.lower(), raw.upper(), raw.replace("-", "")}
        run = self.begin("no-raw", checkpoint=True)
        run.heartbeat(units_done=0, stage="started")
        run.record("u1", {"x": 1})
        run.finish("done", exit_code=0)
        texts = {}
        for directory, _, files in os.walk(run.path):
            for name in files:
                with open(os.path.join(directory, name), "rb") as handle:
                    texts[name] = handle.read().decode("utf-8", errors="replace")
        self.assertIn("manifest.json", texts)
        self.assertIn("status.json", texts)
        for name, text in texts.items():
            self.assertFalse(
                any(form in text for form in forms),
                f"{name} holds the raw machine identity",
            )
        self.assertTrue(
            digest(raw) in texts["manifest.json"], "no digest in the manifest"
        )
        self.assertTrue(digest(raw) in texts["status.json"], "no digest in the status")

    def test_a_failing_reader_writes_null_and_nothing_fails(self):
        def fail():
            raise OSError("injected")

        for index, (machine, boot, name) in enumerate(
            (
                (fail, fail, fail),
                (lambda: None, lambda: None, lambda: None),
                (lambda: "", lambda: "", lambda: ""),
            )
        ):
            with (
                self.subTest(index),
                mock.patch.multiple(
                    runregistrykit,
                    _read_machine_identity=machine,
                    _read_boot_identity=boot,
                    _read_host_name=name,
                ),
            ):
                run = self.begin(f"failing-{index}")
                run.heartbeat(units_done=1)
                status = runregistrykit.read_json(run.status_path)
                self.assertIn("host", status)
                self.assertEqual(status["host"], {"id": None, "boot": None})
                manifest = runregistrykit.read_json(run.manifest_path)
                self.assertEqual(set(manifest["host"]), HOST_KEYS)
                self.assertIsNone(manifest["host"]["id"])
                self.assertIsNone(manifest["host"]["name"])
                # judged here, as a record with no host is
                (entry,) = [
                    e
                    for e in runregistrykit.list_runs(root=self.root)
                    if e["id"] == run.id
                ]
                self.assertEqual(entry["liveness"], "alive")
                self.assertTrue(entry["host_recorded"])
                self.assertIsNone(entry["host_id"])
                self.assertIsNone(entry["host"])
                run.finish("done", exit_code=0)
                self.assertEqual(
                    runregistrykit.read_json(run.status_path)["host"],
                    {"id": None, "boot": None},
                )

    def test_list_runs_reports_the_host(self):
        with readers():
            run = self.begin("listed")
            entries = runregistrykit.list_runs(root=self.root)
        (entry,) = entries
        self.assertEqual(entry["host"], NAME)
        self.assertEqual(entry["host_id"], digest(RAW))
        self.assertTrue(entry["host_recorded"])
        self.assertEqual(entry["liveness"], "alive")
        self.assertEqual(entry["id"], run.id)

    def test_list_runs_reads_this_host_once(self):
        with readers():
            for slug in ("one", "two", "three"):
                self.begin(slug)
            with mock.patch.object(
                runregistrykit, "this_host", wraps=runregistrykit.this_host
            ) as asked:
                entries = runregistrykit.list_runs(root=self.root)
        self.assertEqual(len(entries), 3)
        self.assertEqual(asked.call_count, 1)


class TestTheJudgement(test_run_registry.RegistryTestCase):
    """`liveness`, step by step: the state; another host; another boot of this one; then the
    pid and the heartbeat, as before."""

    def judge(self, status, here=HERE, stale_after=3600.0):
        return runregistrykit.liveness(status, stale_after, here=here)

    def test_another_hosts_running_record_is_foreign_and_its_pid_is_not_tested(self):
        dead = self.a_dead_pid()
        for label, status in (
            ("a live pid and a fresh heartbeat", a_status(os.getpid(), ELSEWHERE)),
            ("a dead pid", a_status(dead, ELSEWHERE)),
            ("an old heartbeat", a_status(os.getpid(), ELSEWHERE, seconds_ago=1e6)),
            ("no boot", a_status(dead, {"id": ELSEWHERE["id"], "boot": None})),
            (
                "this boot's text",
                a_status(dead, {"id": ELSEWHERE["id"], "boot": HERE["boot"]}),
            ),
        ):
            with self.subTest(label):
                self.assertEqual(self.judge(status), "foreign")
                with mock.patch.object(
                    runregistrykit,
                    "pid_alive",
                    side_effect=AssertionError("a foreign pid was tested here"),
                ):
                    self.assertEqual(self.judge(status), "foreign")

    def test_a_record_with_an_id_where_this_host_has_none_is_foreign(self):
        for here in (
            {"id": None, "boot": None},
            {"id": None, "boot": ELSEWHERE["boot"]},
        ):
            with self.subTest(here=here):
                self.assertEqual(
                    self.judge(a_status(os.getpid(), ELSEWHERE), here=here), "foreign"
                )

    def test_this_host_from_another_boot_is_stale_whatever_its_pid_says(self):
        status = a_status(os.getpid(), {"id": HERE["id"], "boot": "an-earlier-boot"})
        self.assertTrue(runregistrykit.pid_alive(os.getpid()))
        self.assertEqual(self.judge(status, stale_after=1e9), "stale")

    def test_this_host_and_this_boot_are_judged_by_pid_and_heartbeat(self):
        dead = self.a_dead_pid()
        mine = {"id": HERE["id"], "boot": HERE["boot"]}
        self.assertEqual(self.judge(a_status(os.getpid(), mine)), "alive")
        self.assertEqual(self.judge(a_status(dead, mine)), "stale")
        self.assertEqual(
            self.judge(a_status(os.getpid(), mine, seconds_ago=7200.0)), "stale"
        )
        # a boot missing on either side is no evidence of a reboot: judged by pid and heartbeat
        no_boot = {"id": HERE["id"], "boot": None}
        self.assertEqual(self.judge(a_status(os.getpid(), no_boot)), "alive")
        self.assertEqual(self.judge(a_status(dead, no_boot)), "stale")
        here_without_boot = {"id": HERE["id"], "boot": None}
        self.assertEqual(
            self.judge(a_status(os.getpid(), mine), here=here_without_boot), "alive"
        )

    def test_a_terminal_record_from_another_host_is_finished(self):
        for state in runregistrykit.TERMINAL_STATES:
            with self.subTest(state):
                self.assertEqual(
                    self.judge(a_status(os.getpid(), ELSEWHERE, state=state)),
                    "finished",
                )
        self.assertEqual(
            self.judge(a_status(os.getpid(), ELSEWHERE, state="queued")), "unknown"
        )
        self.assertEqual(self.judge({}), "unknown")

    def test_a_host_that_names_no_id_is_judged_here(self):
        dead = self.a_dead_pid()
        for label, host in (
            ("null", None),
            ("not a dict", "elsewhere"),
            ("a list", [ELSEWHERE["id"]]),
            ("an id of null", {"id": None, "boot": "an-earlier-boot"}),
            ("no id", {"boot": "an-earlier-boot"}),
        ):
            with self.subTest(label):
                self.assertEqual(self.judge(a_status(os.getpid(), host)), "alive")
                self.assertEqual(self.judge(a_status(dead, host)), "stale")

    def test_here_defaults_to_this_host_read_afresh(self):
        with readers():
            mine = runregistrykit.this_host()
            status = a_status(os.getpid(), {"id": mine["id"], "boot": mine["boot"]})
            self.assertEqual(runregistrykit.liveness(status, 3600.0), "alive")
        with readers(boot="the-boot-after-a-reboot"):
            self.assertEqual(runregistrykit.liveness(status, 3600.0), "stale")
        with readers(machine="another-machine"):
            self.assertEqual(runregistrykit.liveness(status, 3600.0), "foreign")


class TestAnOldRecord(test_run_registry.RegistryTestCase):
    """A record written before the host was recorded is judged as it was then: by `kill -0` and
    the heartbeat, here, whatever this host is."""

    def test_a_status_with_no_host_is_judged_by_pid_and_heartbeat(self):
        dead = self.a_dead_pid()
        for label, here in (
            ("this host", HERE),
            ("a host with no identity", {"id": None, "boot": None}),
            ("read afresh", None),
        ):
            with self.subTest(label):
                alive = a_status(os.getpid(), with_host=False)
                self.assertNotIn("host", alive)
                self.assertEqual(
                    runregistrykit.liveness(alive, 3600.0, here=here), "alive"
                )
                self.assertEqual(
                    runregistrykit.liveness(alive, -1.0, here=here), "stale"
                )
                self.assertEqual(
                    runregistrykit.liveness(
                        a_status(dead, with_host=False), 3600.0, here=here
                    ),
                    "stale",
                )
                with mock.patch.object(
                    runregistrykit, "pid_alive", wraps=runregistrykit.pid_alive
                ) as asked:
                    runregistrykit.liveness(alive, 3600.0, here=here)
                asked.assert_called_once_with(os.getpid())

    def test_list_runs_judges_it_here_and_says_no_host_is_recorded(self):
        dead = self.a_dead_pid()
        for slug, pid, expected in (
            ("old-alive", os.getpid(), "alive"),
            ("old-dead", dead, "stale"),
        ):
            run = self.begin(slug)
            # the form of a run directory written before the host was recorded, built here
            manifest = runregistrykit.read_json(run.manifest_path)
            del manifest["host"]
            runregistrykit.write_json_atomic(run.manifest_path, manifest)
            runregistrykit.write_json_atomic(
                run.status_path, a_status(pid, with_host=False)
            )
            (entry,) = [
                e for e in runregistrykit.list_runs(root=self.root) if e["id"] == run.id
            ]
            with self.subTest(slug):
                self.assertEqual(entry["liveness"], expected)
                self.assertFalse(entry["host_recorded"])
                self.assertIsNone(entry["host_id"])
                self.assertIsNone(entry["host"])
                self.assertEqual(entry["state"], "running")
                self.assertEqual(entry["pid"], pid)


class TestTheCommandLine(test_run_registry.RegistryTestCase):
    """`python -m runregistrykit list` over a foreign run, a stale run and a record with no host,
    in a child process, as the lister's own test runs it."""

    def a_foreign_run(self, slug, name):
        """A run whose status says it is on another host, with a pid that is gone here, so that
        only the host keeps it from being called stale."""
        run = self.begin(slug)
        status = runregistrykit.read_json(run.status_path)
        status["host"] = {
            "id": another_id(runregistrykit.this_host()["id"]),
            "boot": "a-boot-of-another-host",
        }
        status["pid"] = self.a_dead_pid()
        runregistrykit.write_json_atomic(run.status_path, status)
        manifest = runregistrykit.read_json(run.manifest_path)
        manifest["host"]["name"] = name
        manifest["host"]["id"] = status["host"]["id"]
        runregistrykit.write_json_atomic(run.manifest_path, manifest)
        return run, status["host"]["id"]

    def test_foreign_and_stale_rows_and_the_count_of_records_with_no_host(self):
        named, _ = self.a_foreign_run("far-named", "far-host")
        unnamed, unnamed_id = self.a_foreign_run("far-unnamed", None)
        stale, _ = self.a_dead_run(slug="crashed")
        old = self.begin("old")
        runregistrykit.write_json_atomic(
            old.status_path, a_status(os.getpid(), with_host=False)
        )

        done = subprocess.run(
            [sys.executable, "-m", "runregistrykit", "list", "--root", self.root],
            capture_output=True,
            text=True,
            cwd=self.client,
            timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        rows = {}
        for line in done.stdout.splitlines():
            for run in (named, unnamed, stale, old):
                if run.id in line:
                    rows[run.id] = line
        self.assertEqual(len(rows), 4, done.stdout)
        self.assertTrue(rows[named.id].startswith("?? "), rows[named.id])
        self.assertIn("far-host", rows[named.id])
        self.assertTrue(rows[unnamed.id].startswith("?? "), rows[unnamed.id])
        self.assertIn(unnamed_id, rows[unnamed.id])
        self.assertTrue(rows[stale.id].startswith("!! "), rows[stale.id])
        self.assertTrue(rows[old.id].startswith("   "), rows[old.id])
        for row in rows.values():
            self.assertIn(" running ", row)

        self.assertIn(
            f"4 run(s) under {self.root}: 1 alive, 2 foreign, 1 stale; 1 with no host "
            f"recorded.",
            done.stdout,
        )
        self.assertIn("?? 2 run(s) say they are running on another host (", done.stderr)
        (foreign_line,) = [l for l in done.stderr.splitlines() if l.startswith("?? ")]
        self.assertIn("far-host", foreign_line)
        self.assertIn(unnamed_id, foreign_line)
        self.assertIn(
            "their pids are not tested here. Look on that host.", foreign_line
        )
        self.assertIn("!! 1 run(s) say they are running and are not", done.stderr)
        self.assertIn("or this machine has rebooted since", done.stderr)

    def test_no_foreign_run_no_foreign_line(self):
        self.begin("here").finish("done", exit_code=0)
        done = subprocess.run(
            [sys.executable, "-m", "runregistrykit", "list", "--root", self.root],
            capture_output=True,
            text=True,
            cwd=self.client,
            timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertNotIn("??", done.stdout + done.stderr)
        self.assertIn("1 finished; 0 with no host recorded.", done.stdout)


if __name__ == "__main__":
    unittest.main()
