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

import itertools
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import threading
import time
import types
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


# =================================================================================================
# the writer's bookkeeping: which in-flight writes a re-entered write applies, and the record of
# what landed, which is never lowered. A handler is still a call made from inside the write; the
# sweep below makes it at every instruction the writer executes, by `sys.monitoring`


def made_inside(run, write, handler) -> str:
    """Make ``write``, a write of ``run``'s status, with ``handler`` called once from inside its
    `json.dump`, half the payload written; say how it ended."""
    interruption = Interruption(run, HALF_WRITTEN, handler)
    with mock.patch("json.dump", new=interruption.dump):
        try:
            write()
        except SystemExit as exc:
            outcome = f"raised SystemExit({exc.code})"
        except BaseException as exc:
            outcome = f"raised {type(exc).__name__}: {exc}"
        else:
            outcome = "returned"
    if not interruption.fired:
        return "the handler never ran"
    return outcome


def a_later_reentered_heartbeat(run, units) -> str:
    """A `heartbeat(units_done=units)` whose `json.dump` makes a handler's `heartbeat()`: the
    handler's write composes from the record of what landed, so a lowered record shows here.
    """
    return made_inside(run, lambda: run.heartbeat(units_done=units), run.heartbeat)


class TestTwoHandlerWritesInsideOne(StatusTestCase):
    """Two handler writes inside one write, the cases 02's review measured: an older in-flight
    write's fields are not re-applied over a newer landed write's. And the same `finish` with one
    handler write."""

    def test_a_heartbeat_then_a_finish_inside_a_heartbeat(self):
        run = self.begin("two-inside-a-heartbeat")
        begun = run.status()

        def handler():
            run.heartbeat(stage="B")
            run.finish("killed", exit_code=143)

        outcome = made_inside(
            run, lambda: run.heartbeat(units_done=UNITS, stage="A"), handler
        )
        self.assertEqual(outcome, "returned")
        self.assertKilledWithTheHeartbeatsFields(run, begun, stage="B")

    def finish_inside_a_finish(self, handler_writes) -> None:
        run = self.begin("inside-a-finish")
        run.heartbeat(units_done=UNITS, stage=STAGE)
        begun = run.status()

        def handler():
            run.finish("killed", exit_code=143)
            if handler_writes == 2:
                run.heartbeat()

        outcome = made_inside(run, lambda: run.finish("done", exit_code=0), handler)
        self.assertEqual(outcome, "returned")
        self.assertKilledWithTheHeartbeatsFields(run, begun)

    def test_a_finish_then_a_heartbeat_inside_a_finish(self):
        self.finish_inside_a_finish(2)

    def test_a_finish_inside_a_finish(self):
        self.finish_inside_a_finish(1)


class TestAPutBackThenALaterReenteredWrite(StatusTestCase):
    """02's review, (o2): after a put-back, the record of what landed is the put-back's, so a
    later write that a handler re-enters composes from the terminal state."""

    def test_the_terminal_state_is_kept_throughout(self):
        run = self.begin("put-back-then-later")
        begun = run.status()
        interruption = Interruption(
            run, BEFORE_REPLACE, a_handler(run.finish, "returns")
        )
        self.assertEqual(interruption.heartbeat(), "returned")
        self.assertTrue(interruption.fired, "the handler never ran")
        # the heartbeat's replace clobbered `killed`, and it put the handler's payload back
        self.assertEqual(len(interruption.replaced), 3, interruption.replaced)
        self.assertKilledWithTheHeartbeatsFields(run, begun)

        self.assertEqual(a_later_reentered_heartbeat(run, UNITS + 1), "returned")
        with open(run.status_path) as handle:
            status = json.load(handle)
        self.assertEqual(
            (status["state"], status["exit_code"], status["units_done"]),
            ("killed", 143, UNITS + 1),
            "a later re-entered heartbeat put back a state the record should have left behind",
        )
        self.assertEqual(self.leftovers(run), [])


# the line that opens the writer's section of `runregistrykit/__init__.py`, and the rule that
# opens the next section
WRITER_SECTION = "# the writer of `status.json`"
SECTION_RULE = "# ====="

# the most instructions one uninterrupted write may execute in the writer, and the most seconds
# one sweep of one mode may take: bounds, not measurements (the log gives those)
MOST_INSTRUCTIONS = 2000
SWEEP_SECONDS = 120.0

# the handler's four modes: what it writes, then whether it raises `SystemExit(143)`
MODES = (
    ("finish", "returns"),
    ("finish", "raises"),
    ("finish, then heartbeat", "returns"),
    ("finish, then heartbeat", "raises"),
)


def the_writers_code() -> list:
    """Every code object of the writer's section of `runregistrykit/__init__.py`: each function
    the section defines, and every code object nested in one (a generator expression is one),
    found through `co_consts`, recursively."""
    with open(runregistrykit.__file__) as handle:
        lines = handle.read().splitlines()
    start = next(
        number
        for number, line in enumerate(lines, 1)
        if line.startswith(WRITER_SECTION)
    )
    end = next(
        number
        for number, line in enumerate(lines, 1)
        if number > start and line.startswith(SECTION_RULE)
    )
    functions = sorted(
        (
            value
            for value in vars(runregistrykit).values()
            if isinstance(value, types.FunctionType)
            and value.__module__ == runregistrykit.__name__
            and start < value.__code__.co_firstlineno < end
        ),
        key=lambda function: function.__code__.co_firstlineno,
    )
    codes = []

    def add(code):
        codes.append(code)
        for constant in code.co_consts:
            if isinstance(constant, types.CodeType):
                add(constant)

    for function in functions:
        add(function.__code__)
    return codes


def line_of(code, offset):
    for begin, end, line in code.co_lines():
        if begin <= offset < end:
            return line
    return None


class Attempt:
    """One interrupted write: ``handler`` is called at the ``at``-th instruction the writer
    executes (never, if ``at`` is 0), once. Instructions executed while it runs are not counted.
    """

    def __init__(self, at, handler=None):
        self.at, self.handler = at, handler
        self.seen = 0
        self.busy = self.fired = False
        self.where = None
        self.per_code = {}


class Instructions:
    """`sys.monitoring` `INSTRUCTION` events on ``codes``, and on nothing else, under a tool id
    that was free; the events cleared and the id freed however the block ends."""

    def __init__(self, codes):
        self.codes = codes
        self.attempt = None
        self.tool = None

    def __enter__(self):
        monitoring = sys.monitoring
        for tool in range(6):
            try:
                monitoring.use_tool_id(tool, "runregistrykit's status-writer sweep")
            except ValueError:
                continue
            self.tool = tool
            break
        else:
            raise AssertionError("no sys.monitoring tool id is free")
        try:
            monitoring.register_callback(
                self.tool, monitoring.events.INSTRUCTION, self.on_instruction
            )
            for code in self.codes:
                monitoring.set_local_events(
                    self.tool, code, monitoring.events.INSTRUCTION
                )
        except BaseException:
            self.close()
            raise
        return self

    def __exit__(self, *exc_info):
        self.close()

    def close(self):
        monitoring = sys.monitoring
        try:
            for code in self.codes:
                monitoring.set_local_events(self.tool, code, 0)
            monitoring.register_callback(self.tool, monitoring.events.INSTRUCTION, None)
        finally:
            monitoring.free_tool_id(self.tool)

    def on_instruction(self, code, offset):
        # never `sys.monitoring.DISABLE`, which would silence this instruction for every later
        # attempt. In a raising mode the handler's exception propagates from the instruction
        attempt = self.attempt
        if attempt is None or attempt.busy or attempt.fired:
            return None
        attempt.seen += 1
        attempt.per_code[code] = attempt.per_code.get(code, 0) + 1
        if attempt.seen == attempt.at:
            attempt.fired = True
            attempt.where = (code, offset)
            attempt.busy = True
            try:
                attempt.handler()
            finally:
                attempt.busy = False
        return None

    def run(self, attempt, write) -> str:
        """Make ``write`` under ``attempt``; say how it ended."""
        self.attempt = attempt
        try:
            write()
        except SystemExit as exc:
            return f"raised SystemExit({exc.code})"
        except BaseException as exc:
            return f"raised {type(exc).__name__}: {exc}"
        finally:
            self.attempt = None
        return "returned"


def the_handler(run, writes, ending, seen=None):
    """The sweep's handler: `finish("killed", exit_code=143)`, alone or followed by a
    `heartbeat()`, then returning or raising `SystemExit(143)`. With a list ``seen``, it first
    appends whether the interrupted `finish` was in flight or had landed."""

    def handler():
        if seen is not None:
            seen.append(seen_by_the_handler(run))
        run.finish("killed", exit_code=143)
        if writes == "finish, then heartbeat":
            run.heartbeat()
        if ending == "raises":
            raise SystemExit(143)

    return handler


def seen_by_the_handler(run) -> bool:
    """Whether the interrupted `finish("done")` had, when the handler ran, registered its fields
    as in flight in the writer's bookkeeping, or landed. The bookkeeping is read, never changed.
    """
    book = runregistrykit._STATUS_WRITES.get(os.path.realpath(run.status_path))
    if book is not None and any(
        fields.get("state") == "done" for fields in list(book["in_flight"].values())
    ):
        return True
    return (runregistrykit.read_json(run.status_path) or {}).get("state") == "done"


def ending_of(run):
    """The file's state and exit code, or what is wrong with it."""
    try:
        with open(run.status_path) as handle:
            status = json.load(handle)
    except (OSError, ValueError) as exc:
        return f"status.json does not parse: {type(exc).__name__}"
    left = sorted(n for n in os.listdir(run.path) if n.endswith(".tmp"))
    if left:
        return f"left behind: {left}"
    return [status.get("state"), status.get("exit_code")]


def judge_a_heartbeat(run, ending, seen) -> list:
    """After an interrupted heartbeat: `killed` and 143, nothing left; and still so after a later
    heartbeat that a handler re-enters, which composes from the record of what landed, with the
    later heartbeat's `units_done` kept.
    """
    found = []
    ended = ending_of(run)
    if ended != ["killed", 143]:
        found.append(f"after the heartbeat: {ended}")
    later = a_later_reentered_heartbeat(run, UNITS + 1)
    if later != "returned":
        found.append(f"the later heartbeat {later}")
    ended = ending_of(run)
    if ended != ["killed", 143]:
        found.append(f"after a later re-entered heartbeat: {ended}")
    elif run.status().get("units_done") != UNITS + 1:
        found.append("a later re-entered heartbeat lost its units_done")
    return found


def judge_a_finish(run, ending, seen) -> list:
    """After an interrupted `finish("done")`: `killed` and 143, nothing left; except that where
    the handler returns and its write is the earlier one, because the interrupted write had
    neither registered its fields as in flight nor landed, `done` and 0 landing last is right.
    """
    ended = ending_of(run)
    if ended == ["killed", 143]:
        return []
    if ending == "returns" and not seen and ended == ["done", 0]:
        return ["accepted: the handler's write is the earlier"]
    return [f"after the finish: {ended}"]


# what each sweep interrupts, and how its ending is judged
SWEEPS = {
    "heartbeat": (
        lambda run: lambda: run.heartbeat(units_done=UNITS),
        judge_a_heartbeat,
    ),
    "finish": (lambda run: lambda: run.finish("done", exit_code=0), judge_a_finish),
}


def sweep_in_this_process(which, root, client) -> dict:
    """The sweep ``which``, in this process: a run begun under ``root``; then for each of the
    handler's four modes, the instructions of one uninterrupted write counted, and the write
    interrupted at each in turn, each attempt on a fresh run (a copy of the begun run's directory,
    at a new real path and so with a book of its own, given one plain write first, as `begin`
    gives a run). Says, per mode, what went wrong at which instruction."""
    write_of, judge = SWEEPS[which]
    template = runregistrykit.begin(
        campaign="example",
        prompt="01",
        slug=f"every-instruction-of-a-{which}",
        purpose="a sweep of the status writer, in a temporary directory",
        root=root,
        client_root=client,
        argv=["sweep", which],
    )
    copies = itertools.count()

    def a_fresh_run():
        path = os.path.join(root, f"{template.id}-{next(copies)}")
        shutil.copytree(template.path, path)
        run = runregistrykit.Run(path)
        run.heartbeat()
        return run

    codes = the_writers_code()
    report = {
        "codes": [f"{code.co_name}:{code.co_firstlineno}" for code in codes],
        "modes": [],
    }
    with Instructions(codes) as instructions:
        for writes, ending in MODES:
            mode = {"handler": writes, "ending": ending, "wrong": [], "accepted": 0}
            report["modes"].append(mode)
            counting = Attempt(0)
            run = a_fresh_run()
            mode["uninterrupted"] = instructions.run(counting, write_of(run))
            mode["total"] = total = counting.seen
            mode["per_code"] = {
                f"{code.co_name}:{code.co_firstlineno}": count
                for code, count in counting.per_code.items()
            }
            shutil.rmtree(run.path)
            if not 0 < total <= MOST_INSTRUCTIONS:
                continue
            expected = "raised SystemExit(143)" if ending == "raises" else "returned"
            started = time.monotonic()
            for at in range(1, total + 1):
                run = a_fresh_run()
                seen = [] if which == "finish" else None
                attempt = Attempt(at, the_handler(run, writes, ending, seen))
                outcome = instructions.run(attempt, write_of(run))
                if not attempt.fired:
                    found = ["the handler never ran"]
                    where = ""
                else:
                    code, offset = attempt.where
                    where = f" ({code.co_name}, line {line_of(code, offset)}, offset {offset})"
                    found = [] if outcome == expected else [outcome]
                    found.extend(judge(run, ending, bool(seen and seen[0])))
                    if found and found[0].startswith("accepted:"):
                        mode["accepted"] += 1
                        found = []
                if found:
                    mode["wrong"].append(f"{at}{where}: {'; '.join(found)}")
                shutil.rmtree(run.path)
                if time.monotonic() - started > SWEEP_SECONDS:
                    mode["wrong"].append(f"the sweep passed {SWEEP_SECONDS} s at {at}")
                    break
            mode["seconds"] = round(time.monotonic() - started, 3)
    return report


# a child that runs one sweep and prints its report. The sweep runs in a child of its own so that
# what a raising handler leaves in the process at an instruction where the interpreter itself
# never raises (the writer's lock held, an in-flight entry kept: the log of 02b says which) ends
# with the child, and reaches no other test
SWEEPER = """\
import json, sys

sys.path.insert(0, {repo!r})
from runregistrykit.tests import test_status_writes

which, root, client = sys.argv[1:4]
print(json.dumps(test_status_writes.sweep_in_this_process(which, root, client)))
"""

# a sweeping child's timeout: its four sweeps' bounds, and a margin for starting
SWEEPER_TIMEOUT = 4 * SWEEP_SECONDS + 60


class TestAHandlerAtEveryInstruction(StatusTestCase):
    """A handler run at every instruction the writer executes, one instruction per attempt
    (`sweep_in_this_process`), in a child process the test starts and does not signal. The
    handler records `killed`, alone or followed by a heartbeat, then returns or raises
    `SystemExit(143)`."""

    def sweep(self, which) -> dict:
        script = os.path.join(temporary_directory(self), "sweeper.py")
        with open(script, "w") as handle:
            handle.write(SWEEPER.format(repo=PACKAGE_PARENT))
        try:
            done = subprocess.run(
                [sys.executable, script, which, self.root, self.client],
                cwd=self.client,
                capture_output=True,
                text=True,
                timeout=SWEEPER_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            self.fail(f"the {which} sweep did not end in {SWEEPER_TIMEOUT} s")
        self.assertEqual(done.returncode, 0, done.stderr[-2000:])
        report = json.loads(done.stdout.splitlines()[-1])
        names = {code.split(":")[0] for code in report["codes"]}
        self.assertLessEqual({"_write_status", "_land_status"}, names)
        self.assertEqual(len(report["modes"]), len(MODES))
        for mode in report["modes"]:
            with self.subTest(handler=mode["handler"], ending=mode["ending"]):
                self.assertEqual(mode["uninterrupted"], "returned")
                self.assertGreater(mode["total"], 0, "no instruction was seen")
                self.assertLessEqual(mode["total"], MOST_INSTRUCTIONS)
                self.assertEqual(
                    mode["wrong"],
                    [],
                    f"{len(mode['wrong'])} of {mode['total']} instructions went wrong",
                )
        return report

    def test_an_interrupted_heartbeat(self):
        self.sweep("heartbeat")

    def test_an_interrupted_finish(self):
        self.sweep("finish")


if __name__ == "__main__":
    unittest.main()
