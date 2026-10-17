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

"""How `status.json` is written: through a temporary name of each write's own, with the mode a
plain `open` gives, and so that a handler which writes the status from inside a write leaves it
parseable, with the handler's state in it, however the handler ends.

The core only: nothing of the store layer is imported, so that the core job can run this module.
A handler is simulated in this process by calling `finish` from inside a patched `json.dump` or
`os.replace`, which is what a Python signal handler is: a call made at a bytecode boundary. The
patches fire once, for the interrupted write; every write made from inside them goes through the
real functions. One class sends a real `SIGTERM`, in a child process the test starts, which
signals only itself; each child runs under a timeout, so that a handler waiting for ever on the
write it interrupted fails the test instead of hanging it.
"""

import json
import os
import re
import stat
import subprocess
import sys
import threading
import unittest
from unittest import mock

import runregistrykit
from runregistrykit.tests import test_run_registry
from runregistrykit.tests.client_fixtures import PACKAGE_PARENT, temporary_directory

# what the interrupted heartbeat is given
UNITS = 7
STAGE = "the heartbeat's own stage"

# the four points at which a handler interrupts the heartbeat's write
HALF_WRITTEN = "inside json.dump, half the payload written"
ALL_WRITTEN = "inside json.dump, all of it written, before the flush"
BEFORE_REPLACE = "in os.replace, before the real replace"
AFTER_REPLACE = "in os.replace, after the real replace"
POINTS = (HALF_WRITTEN, ALL_WRITTEN, BEFORE_REPLACE, AFTER_REPLACE)

# a temporary name of the status writer's
TEMPORARY = re.compile(r"status\.json\..+\.tmp\Z")

# a child that begins a run, installs a SIGTERM handler that records `killed`, and sends itself
# SIGTERM from inside a heartbeat's `json.dump`, with half the payload or all of it written. The
# handler then raises, returns, or restores the default disposition and kills its own process
CHILD = """\
import json, os, signal, sys

sys.path.insert(0, {repo!r})
import runregistrykit

ending, written, root, client = sys.argv[1:5]
run = runregistrykit.begin(
    campaign="example",
    prompt="01",
    slug="a-handler-that-" + ending,
    purpose="a child that interrupts its own heartbeat",
    root=root,
    client_root=client,
    argv=["child", ending, written],
)
print(json.dumps({{"path": run.path, "status": run.status()}}), flush=True)


def handler(signum, frame):
    run.finish("killed", exit_code=128 + signum)
    if ending == "raises":
        raise SystemExit(128 + signum)
    if ending == "ends-the-process":
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)


signal.signal(signal.SIGTERM, handler)
real_dump = json.dump
fired = []


def dump(obj, fp, *args, **kwargs):
    if fired:
        return real_dump(obj, fp, *args, **kwargs)
    fired.append(True)
    text = json.dumps(obj, *args, **kwargs)
    cut = len(text) // 2 if written == "half" else len(text)
    fp.write(text[:cut])
    os.kill(os.getpid(), signal.SIGTERM)
    fp.write(text[cut:])


json.dump = dump
run.heartbeat(units_done={units}, stage={stage!r})
"""

# a child's timeout: ample for a begin and two writes, and short against a hang
CHILD_TIMEOUT = 60


class StatusTestCase(test_run_registry.RegistryTestCase):
    def leftovers(self, run) -> list:
        return sorted(n for n in os.listdir(run.path) if n.endswith(".tmp"))

    def assertKilledWithTheHeartbeatsFields(self, run, begun, stage=STAGE):
        """`status.json` parses, says `killed` with 143, keeps the heartbeat's fields and what
        `begin` wrote, and nothing is left behind."""
        with open(run.status_path) as handle:
            text = handle.read()
        try:
            status = json.loads(text)
        except ValueError:
            self.fail(f"status.json does not parse ({len(text)} characters)")
        # no message prints the host, whose boot is read from the machine
        shown = {key: value for key, value in status.items() if key != "host"}
        self.assertEqual(status["state"], "killed", shown)
        self.assertEqual(status["exit_code"], 143, shown)
        self.assertEqual(status["units_done"], UNITS, "the heartbeat's units were lost")
        self.assertEqual(status["stage"], stage, "the heartbeat's stage was lost")
        self.assertEqual(status["pid"], begun["pid"])
        self.assertTrue(
            status.get("host") == begun["host"], "the host is not as begin wrote it"
        )
        self.assertEqual(self.leftovers(run), [], "a temporary file was left behind")
        return status


class Interruption:
    """A heartbeat whose write calls ``handler`` once, at ``point``. ``replaced`` lists the
    source of every real `os.replace` onto `status.json` while it is in force."""

    def __init__(self, run, point, handler):
        self.run, self.point, self.handler = run, point, handler
        self.fired = False
        self.replaced = []
        self.real_dump, self.real_replace = json.dump, os.replace

    def dump(self, obj, fp, *args, **kwargs):
        if self.fired or self.point not in (HALF_WRITTEN, ALL_WRITTEN):
            return self.real_dump(obj, fp, *args, **kwargs)
        self.fired = True
        text = json.dumps(obj, *args, **kwargs)
        cut = len(text) // 2 if self.point == HALF_WRITTEN else len(text)
        fp.write(text[:cut])
        self.handler()
        fp.write(text[cut:])

    def really_replace(self, source, destination):
        self.real_replace(source, destination)
        if destination == self.run.status_path:
            self.replaced.append(source)

    def replace(self, source, destination):
        if (
            self.fired
            or self.point not in (BEFORE_REPLACE, AFTER_REPLACE)
            or destination != self.run.status_path
        ):
            return self.really_replace(source, destination)
        self.fired = True
        if self.point == BEFORE_REPLACE:
            self.handler()
            self.really_replace(source, destination)
        else:
            self.really_replace(source, destination)
            self.handler()

    def heartbeat(self) -> str:
        """Make the heartbeat; say how it ended."""
        with (
            mock.patch("json.dump", new=self.dump),
            mock.patch("os.replace", new=self.replace),
        ):
            try:
                self.run.heartbeat(units_done=UNITS, stage=STAGE)
            except SystemExit as exc:
                return f"raised SystemExit({exc.code})"
            except BaseException as exc:
                return f"raised {type(exc).__name__}: {exc}"
        return "returned"


def a_handler(finish, ending):
    """A handler that calls ``finish``, then raises `SystemExit(143)` or returns."""

    def handler():
        finish("killed", exit_code=143)
        if ending == "raises":
            raise SystemExit(143)

    return handler


class TestAHandlerInsideAHeartbeat(StatusTestCase):
    """The reproduction: a heartbeat whose write makes a `finish` from inside it, at four points,
    the handler then raising and returning."""

    def test_each_point_each_ending(self):
        for point in POINTS:
            for ending in ("raises", "returns"):
                with self.subTest(point=point, ending=ending):
                    run = self.begin(f"point-{POINTS.index(point)}-{ending}")
                    begun = run.status()
                    interruption = Interruption(
                        run, point, a_handler(run.finish, ending)
                    )
                    outcome = interruption.heartbeat()
                    self.assertTrue(interruption.fired, "the handler never ran")
                    self.assertEqual(
                        outcome,
                        "raised SystemExit(143)" if ending == "raises" else "returned",
                    )
                    self.assertKilledWithTheHeartbeatsFields(run, begun)
                    if point in (HALF_WRITTEN, ALL_WRITTEN):
                        self.assertEqual(
                            len(interruption.replaced),
                            1,
                            "the interrupted heartbeat's write replaced status.json after "
                            "the handler's: a superseded write must be discarded",
                        )


class TestASecondRunObject(StatusTestCase):
    """The handler writes through a `Run` of its own for the same directory, as a person's or a
    handler's `Run(path)` does."""

    def check(self, point, path_of):
        run = self.begin(f"second-{POINTS.index(point)}")
        begun = run.status()
        second = runregistrykit.Run(path_of(run))
        interruption = Interruption(run, point, a_handler(second.finish, "returns"))
        self.assertEqual(interruption.heartbeat(), "returned")
        self.assertTrue(interruption.fired, "the handler never ran")
        self.assertKilledWithTheHeartbeatsFields(run, begun)

    def test_half_written(self):
        self.check(HALF_WRITTEN, lambda run: run.path)

    def test_before_the_replace(self):
        self.check(BEFORE_REPLACE, lambda run: run.path)

    def test_through_another_spelling_of_the_path(self):
        link = os.path.join(temporary_directory(self), "the-runs-by-another-name")
        os.symlink(self.root, link)
        self.check(HALF_WRITTEN, lambda run: os.path.join(link, run.id))


class TestAHandlerDuringThePutBack(StatusTestCase):
    def test_a_second_handler_inside_the_put_back(self):
        """At the point before the heartbeat's replace, the handler returns, so the heartbeat's
        replace clobbers the handler's `killed` and the heartbeat puts it back. The put-back's own
        replace is interrupted by a second handler's heartbeat, which composes while the file
        holds the clobbering `running`."""
        run = self.begin("put-back")
        begun = run.status()
        later = "from the second handler"
        real_replace = os.replace
        seen = []

        def replace(source, destination):
            if destination != run.status_path:
                return real_replace(source, destination)
            seen.append(source)
            if len(seen) == 1:
                # the heartbeat's replace: the first handler, then the real replace
                run.finish("killed", exit_code=143)
                return real_replace(source, destination)
            if len(seen) == 3:
                # the put-back's replace: the file holds the heartbeat's `running`
                with open(run.status_path) as handle:
                    self.assertEqual(json.load(handle)["state"], "running")
                run.heartbeat(stage=later)
            return real_replace(source, destination)

        with mock.patch("os.replace", new=replace):
            returned = run.heartbeat(units_done=UNITS, stage=STAGE)
        self.assertEqual(
            returned["state"], "running", "the heartbeat composed otherwise"
        )
        self.assertGreaterEqual(len(seen), 4, "the second handler never ran")
        self.assertKilledWithTheHeartbeatsFields(run, begun, stage=later)


class TestARealSignal(StatusTestCase):
    """A real `SIGTERM`, sent by a child to itself from inside a heartbeat's `json.dump`, half
    the payload written; the child's handler records `killed` and raises, returns, or ends the
    process."""

    def child(self, ending):
        script = os.path.join(temporary_directory(self), "child.py")
        with open(script, "w") as handle:
            handle.write(CHILD.format(repo=PACKAGE_PARENT, units=UNITS, stage=STAGE))
        try:
            done = subprocess.run(
                [sys.executable, script, ending, "half", self.root, self.client],
                cwd=self.client,
                capture_output=True,
                text=True,
                timeout=CHILD_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            self.fail(
                f"the child whose handler {ending} did not end in {CHILD_TIMEOUT} s: its "
                f"handler waited on the write it interrupted"
            )
        first = done.stdout.splitlines()[0] if done.stdout else ""
        self.assertTrue(first, done.stderr)
        begun = json.loads(first)
        run = runregistrykit.Run(begun["path"])
        return done, run, begun["status"]

    def test_a_handler_that_raises(self):
        done, run, begun = self.child("raises")
        self.assertEqual(done.returncode, 143, done.stderr)
        self.assertKilledWithTheHeartbeatsFields(run, begun)

    def test_a_handler_that_returns(self):
        done, run, begun = self.child("returns")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertNotIn("FileNotFoundError", done.stderr)
        self.assertKilledWithTheHeartbeatsFields(run, begun)

    def test_a_handler_that_ends_the_process(self):
        done, run, begun = self.child("ends-the-process")
        self.assertEqual(done.returncode, -15, done.stderr)
        # the documented leftover: the interrupted heartbeat's own temporary file, which the
        # process died before it could replace or remove. Nothing reads it
        left = self.leftovers(run)
        self.assertLessEqual(len(left), 1, left)
        for name in left:
            self.assertRegex(name, TEMPORARY)
            self.assertNotEqual(name, "status.json.tmp")
            os.remove(os.path.join(run.path, name))
        self.assertKilledWithTheHeartbeatsFields(run, begun)


class TestTwoThreads(StatusTestCase):
    def test_a_heartbeat_thread_and_a_finish(self):
        run = self.begin("threads")
        going, errors = threading.Event(), []

        def beat():
            try:
                for index in range(300):
                    run.heartbeat(units_done=index, stage="the thread's")
                    if index == 20:
                        going.set()
            except BaseException as exc:
                errors.append(repr(exc))
            finally:
                going.set()

        thread = threading.Thread(target=beat, daemon=True)
        thread.start()
        try:
            self.assertTrue(going.wait(timeout=60), "the thread never got going")
            run.finish("killed", exit_code=143)
        finally:
            # the thread's loop is bounded: it ends before the run directory is removed
            thread.join(timeout=60)
        self.assertFalse(thread.is_alive(), "the heartbeat thread is stuck")
        self.assertEqual(errors, [])
        with open(run.status_path) as handle:
            status = json.load(handle)
        self.assertEqual(status["state"], "killed")
        self.assertEqual(status["exit_code"], 143)
        self.assertEqual(self.leftovers(run), [])


class TestThePlainWrite(StatusTestCase):
    def test_the_temporary_name(self):
        run = self.begin()
        with mock.patch("os.replace", wraps=os.replace) as replace:
            run.heartbeat(units_done=1)
            run.heartbeat(units_done=2)
        sources = [call.args[0] for call in replace.call_args_list]
        self.assertEqual(len(sources), 2)
        for source in sources:
            self.assertEqual(os.path.dirname(source), run.path)
            name = os.path.basename(source)
            self.assertTrue(name.startswith("status.json."), name)
            self.assertTrue(name.endswith(".tmp"), name)
            self.assertNotEqual(name, "status.json.tmp")
        self.assertNotEqual(sources[0], sources[1])

    def test_the_mode_is_the_one_a_plain_open_gives(self):
        run = self.begin()
        probe = os.path.join(run.path, "mode-probe.json")
        for umask, expected in ((0o022, 0o644), (0o077, 0o600)):
            with self.subTest(umask=oct(umask)):
                previous = os.umask(umask)
                try:
                    run.heartbeat(units_done=1)
                    runregistrykit.write_json_atomic(probe, {})
                finally:
                    os.umask(previous)
                mode = stat.S_IMODE(os.stat(run.status_path).st_mode)
                self.assertEqual(mode, stat.S_IMODE(os.stat(probe).st_mode))
                self.assertEqual(mode, expected, oct(mode))
                os.remove(probe)

    def test_a_failed_write_leaves_the_status_as_it_was(self):
        run = self.begin()
        run.heartbeat(units_done=2)
        with open(run.status_path, "rb") as handle:
            before = handle.read()
        with self.assertRaises(TypeError):
            run.heartbeat(stage=object())
        with open(run.status_path, "rb") as handle:
            self.assertEqual(handle.read(), before)
        self.assertEqual(self.leftovers(run), [])
        run.heartbeat(units_done=3)
        self.assertEqual(run.status()["units_done"], 3)

    def test_a_heartbeat_with_nothing_in_flight_reads_once_and_replaces_once(self):
        run = self.begin()
        keys = set(run.status())
        with (
            mock.patch.object(
                runregistrykit, "read_json", wraps=runregistrykit.read_json
            ) as read,
            mock.patch("os.replace", wraps=os.replace) as replace,
        ):
            returned = run.heartbeat(units_done=1, stage="plain")
        reads = [c for c in read.call_args_list if c.args[0] == run.status_path]
        self.assertEqual(len(reads), 1)
        replace.assert_called_once()
        self.assertEqual(set(returned), keys | {"stage"})
        self.assertTrue(
            runregistrykit.read_json(run.status_path) == returned,
            "the file is not the payload the heartbeat returned",
        )
        finished = run.finish("done", exit_code=0)
        self.assertEqual(set(finished), keys | {"stage"})

    def test_write_json_atomic_still_replaces_from_its_tmp_name(self):
        path = os.path.join(temporary_directory(self), "a-sidecar-like.json")
        with mock.patch("os.replace", wraps=os.replace) as replace:
            runregistrykit.write_json_atomic(path, {"a": 1})
        replace.assert_called_once_with(path + ".tmp", path)
        self.assertEqual(runregistrykit.read_json(path), {"a": 1})


class TestAnOldRecord(StatusTestCase):
    """A `status.json` in the form `v0.1.0` wrote, with no `host`, built here."""

    def test_its_keys_are_kept_and_no_host_is_added(self):
        run = self.begin("old")
        old = {
            "state": "running",
            "units_done": 0,
            "units_total": None,
            "pid": os.getpid(),
            "exit_code": None,
            "heartbeat": runregistrykit.now_iso(),
        }
        runregistrykit.write_json_atomic(run.status_path, old)
        self.assertEqual(runregistrykit.liveness(run.status(), 900.0), "alive")

        run.heartbeat(units_done=1, stage="an old record")
        status = run.status()
        self.assertEqual(set(status), set(old) | {"stage"})
        self.assertEqual(status["pid"], os.getpid())
        self.assertEqual(runregistrykit.liveness(status, 900.0), "alive")

        run.heartbeat(pid=self.a_dead_pid())
        self.assertEqual(runregistrykit.liveness(run.status(), 900.0), "stale")

        run.finish("done", exit_code=0)
        status = run.status()
        self.assertEqual(set(status), set(old) | {"stage"})
        self.assertNotIn("host", status)
        self.assertEqual(runregistrykit.liveness(status, 900.0), "finished")


if __name__ == "__main__":
    unittest.main()
