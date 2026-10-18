#!/usr/bin/env python3
"""
A smoke run of an interrupted run, as a client meets one (interrupted-runs prompt 07, section 2.2).

It builds a client root in a new ``tempfile`` directory, as a client's repository would hold one,
and drives the registry there through what happens to a long job that is interrupted: a run
hard-killed by ``SIGKILL``, the refusals that then name ``end``, a live run that ``end`` refuses, a
run ended by its own ``SIGTERM`` handler, a person's ``end`` of the hard-killed run, and a run
resumed on its store that records a fingerprint. The client root is a git repository with one
commit, holding the files the extraction's smoke run writes (``docs/extraction/store_smoke_run.py``,
loaded by its path in the checkout this script lives in, and not changed): ``runregistrykit.toml``,
which names the client's fingerprinter; ``.gitignore``; ``job.py``, the script a run is given; and
``smoke_registry.py``, the client's registry and fingerprinter module, whose ``write_store`` writes
a closed store of two shards. That file is loaded with ``importlib.util.spec_from_file_location``,
which runs nothing of it but its definitions: its ``main`` is guarded.

It imports ``runregistrykit``, its public names and the standard library, and nothing of
``runregistrykit.tests``, so it runs against an installed release, which is what it is for. It never
imports ``datastorekit`` at module scope: the client's module imports it, inside the steps that
need it, so without the extra ``[stores]`` the script starts, the steps that need a store or a
fingerprinter fail, each saying what it saw, and the others run. It never initialises Ray, and
checks at the end that ``ray``, if something imported it, is not initialised.

Every process it starts runs in the client root, never in this repository, with ``PYTHONPATH``
unset, so that each imports the ``runregistrykit`` that ``sys.executable`` has installed: the
script prints its own ``runregistrykit.__file__``, each child prints its own beside its run id, and
the script checks that they are the same file, under the interpreter's ``site-packages``. Run with
a checkout importable instead, it runs its steps and fails that check.

Run it with the package importable, from the repository root, with ``TMPDIR`` naming where its
directory goes:

    TMPDIR=<scratch> python docs/interrupted-runs/interrupted_run_smoke.py [--clean]

Each command runs as ``sys.executable -m runregistrykit ...`` in the client root, as a client runs
it. The script prints the versions it runs with (Python, ``runregistrykit`` and where it was
imported from, and ``datastorekit``, Ray and SQLAlchemy where installed), then each step's ``PASS``
or ``FAIL`` with its commands, their exit codes, and the lines that show the outcome; a step that
raises, or whose command exits otherwise than it should, is that step's ``FAIL``, and the next step
runs where it can. Every value asserted is the script's own: states, exit codes, run ids, pids and
the runs root's listing.

The steps:

1. a store written by the client's module, and ``store create --purpose``;
2. **a hard kill**: a child process begins a run on the store, prints its run id, and heartbeats
   in a loop; the script sends it ``SIGKILL`` and reaps it (returncode -9). Its ``status.json``
   still says ``running``, with its ``host`` recorded, and ``liveness`` calls it ``stale``;
3. ``list``: the hard-killed run's row is marked ``!!``, and stderr names ``python -m
   runregistrykit end``;
4. ``store fingerprint`` is refused (exit 1), naming the run and ``python -m runregistrykit end``;
5. a second ``begin`` on the store is refused, naming the run and ``python -m runregistrykit end``
   and ending ``No run directory was created``; the runs root's listing is unchanged;
6. **a live pid is refused**: a second child begins a run on a second store, installs a ``SIGTERM``
   handler and heartbeats; ``end`` of it exits 1 saying its pid answers ``kill -0``, with and
   without ``--unverified``, and its status is still ``running``, with no ``ended``;
7. **a real ``SIGTERM``**: that child is sent ``SIGTERM`` while it heartbeats; its handler calls
   ``finish("killed", exit_code=128 + signum)`` and exits; returncode 143, status ``killed`` with
   exit code 143, parseable, and no ``status.json.*.tmp`` left;
8. **``end``** of the hard-killed run: with no ``--reason`` an argparse error (exit 2); with one,
   exit 0 and the run ``lost``, exit code ``null``, ``ended.verified`` true and
   ``ended.evidence.pid_answers`` false;
9. ``end`` of it again exits 1: its status says it has already ended (a run that step 8 did not
   end is not ended here: the step fails first);
10. ``list``: the run is ``lost``, unmarked, and the summary counts every run finished;
11. **the resume**: ``begin`` on the first store is accepted, then ``heartbeat`` and
    ``finish("done", exit_code=0, fingerprint=True)``: status ``done``, a fingerprint written into
    the sidecar, and no ``fingerprint_error``;
12. ``store fingerprint`` exits 0, matching, and ``store retire --reason ... --dry-run`` exits 0;
13. the resumed run's manifest records a ``host.id``, and it is its status's.

Its children are its own: it signals no other process, it reaps each child it starts, and a
``finally`` kills and reaps any child still alive, or reaps one that has exited, and says so. It
removes nothing it did not make. Its directory is left in place for inspection unless ``--clean``
is given, which removes that directory and nothing else. Exits 0 when every step passes, 1 when
one fails, and 2 when it cannot start (no ``git`` on ``PATH``, ``runregistrykit`` not importable,
or the extraction's smoke script not found). It is not a test: the suite does not collect it,
and CI only checks its formatting.
"""

import argparse
import importlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import select
import shutil
import signal
import subprocess
import sys
import sysconfig
import tempfile
import time
import traceback
from pathlib import Path

# the extraction's smoke script, beside this one's directory in the checkout
EXTRACTION_SCRIPT = (
    Path(__file__).resolve().parent.parent / "extraction" / "store_smoke_run.py"
)

# the git environment, and the Python path, a child must not inherit: it reads the client root's
# repository, and imports what its interpreter has installed
NOT_INHERITED = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_COMMON_DIR",
    "PYTHONPATH",
    "PYTHONSAFEPATH",
)

# how long a child has to say it has begun, to be reaped, and to have heartbeaten
TIMEOUT = 30.0

# the child of step 2: it begins a run on the store, says so, and heartbeats until it is killed
HARD_KILLED = """\
import json, os, sys, time
import runregistrykit

run = runregistrykit.begin(
    "smoke", "02", "hard-killed", "a smoke run that is hard-killed",
    script=sys.argv[1], results=sys.argv[2],
)
print(json.dumps({"id": run.id, "pid": os.getpid(), "file": runregistrykit.__file__}), flush=True)
done = 0
while True:
    done += 1
    run.heartbeat(units_done=done, stage="working")
    time.sleep(0.1)
"""

# the child of steps 6 and 7: it begins a run on a second store, installs a SIGTERM handler that
# records the run as killed and exits, as a client's driver does, says so, and heartbeats
SIGNALLED = """\
import json, os, signal, sys
import runregistrykit

run = runregistrykit.begin(
    "smoke", "06", "signalled", "a smoke run that is ended by its own SIGTERM handler",
    script=sys.argv[1], results=sys.argv[2],
)


def handler(signum, frame):
    run.finish("killed", exit_code=128 + signum)
    raise SystemExit(128 + signum)


signal.signal(signal.SIGTERM, handler)
print(
    json.dumps(
        {"id": run.id, "pid": os.getpid(), "file": runregistrykit.__file__, "handler": True}
    ),
    flush=True,
)
done = 0
while True:
    done += 1
    run.heartbeat(units_done=done, stage="heartbeating")
"""

# what the commands of the store layer and `end` name, as a person reads it
END_COMMAND = "python -m runregistrykit end"


class StepFailed(Exception):
    """A step's check that did not hold: what it expected, and what it saw."""


class CannotStart(Exception):
    """What keeps the script from starting."""


def load_extraction():
    """The extraction's smoke script as a module, run for its definitions only."""
    if not EXTRACTION_SCRIPT.is_file():
        raise CannotStart(
            f"the extraction's smoke script is not at {EXTRACTION_SCRIPT}"
        )
    spec = importlib.util.spec_from_file_location(
        "_extraction_store_smoke_run", EXTRACTION_SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    # no bytecode cache is written beside it: nothing is written into the checkout
    writing, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = writing
    missing = [
        name
        for name in ("CONFIG", "GITIGNORE", "JOB", "REGISTRY_SOURCE")
        if not isinstance(getattr(module, name, None), str)
    ]
    if missing:
        raise CannotStart(f"{EXTRACTION_SCRIPT} has no {', '.join(missing)}")
    return module


class Smoke:
    def __init__(self, base: Path, extraction, package_file: str):
        self.base = base
        self.extraction = extraction
        self.package_file = package_file
        self.client = base / "client"
        self.stores = self.client / "var" / "datastores"
        self.runs = self.client / "var" / "runs"
        self.primary = self.stores / "smoke-store.sqlite"
        # the second store is only named: no step writes it, and nothing reads its content
        self.second = self.stores / "smoke-second.sqlite"
        self.lines = []
        self.children = []
        self.killed = None  # step 2's child, and what it said
        self.killed_said = None
        self.signalled = None  # step 6's child, and what it said
        self.signalled_said = None
        self.resumed = None  # step 11's run

    # --- helpers ---------------------------------------------------------------------------------

    def say(self, line=""):
        """Keep ``line`` for the step's report, with the smoke directory written ``$SMOKE``."""
        self.lines.append(line.replace(str(self.base), "$SMOKE"))

    def check(self, condition, expected, seen):
        if not condition:
            raise StepFailed(f"expected {expected}; saw {seen}")

    def env(self):
        return {k: v for k, v in os.environ.items() if k not in NOT_INHERITED}

    def git(self, *args, cwd):
        result = subprocess.run(
            ["git", *args], cwd=cwd, env=self.env(), capture_output=True, text=True
        )
        if result.returncode != 0:
            raise StepFailed(
                f"git {' '.join(args)} to exit 0; saw exit {result.returncode}: "
                f"{result.stderr.strip()}"
            )
        return result.stdout

    def command(self, *args, expect=0):
        """Run ``python -m runregistrykit`` with ``args`` in the client root; check its exit."""
        argv = [sys.executable, "-m", "runregistrykit", *[str(a) for a in args]]
        result = subprocess.run(
            argv,
            cwd=self.client,
            env=self.env(),
            capture_output=True,
            text=True,
            timeout=120,
        )
        shown = " ".join(str(a) for a in args)
        self.say(f"  $ python -m runregistrykit {shown}   (in client/)")
        self.say(f"    exit {result.returncode}")
        if result.returncode != expect:
            for line in (result.stdout + result.stderr).strip().splitlines()[-6:]:
                self.say(f"    | {line}")
            raise StepFailed(
                f"exit {expect} from `{shown}`; saw exit {result.returncode}"
            )
        return result

    def show_lines(self, text, *needles):
        """Say each line of ``text`` that contains one of ``needles``; return them."""
        found = [line for line in text.splitlines() if any(n in line for n in needles)]
        for line in found:
            self.say(f"    > {line.rstrip()}")
        return found

    def registry(self):
        """The client's registry module, imported as the package's loader imports it."""
        if str(self.client) not in sys.path:
            sys.path.insert(0, str(self.client))
        return importlib.import_module("smoke_registry")

    def sidecar(self, primary):
        return primary.with_name(primary.stem + ".manifest.json")

    def status(self, run_id):
        """A run's status as the registry reads it (None when it cannot be read)."""
        import runregistrykit

        return runregistrykit.read_json(str(self.runs / run_id / "status.json"))

    def listing(self):
        return sorted(os.listdir(self.runs)) if self.runs.is_dir() else []

    def start(self, source, results, what):
        """Start a child running ``source`` in the client root; return it and its first line."""
        child = subprocess.Popen(
            [sys.executable, "-c", source, str(self.client / "job.py"), str(results)],
            cwd=self.client,
            env=self.env(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.children.append(child)
        self.say(f"  started {what}: pid {child.pid}")
        ready, _, _ = select.select([child.stdout], [], [], TIMEOUT)
        line = child.stdout.readline() if ready else ""
        if not line:
            self.reap(child, kill=True)
            stderr = child.stderr.read().strip().splitlines()
            for text in stderr[-6:]:
                self.say(f"    | {text}")
            seen = (
                "nothing" if not ready else f"its exit, returncode {child.returncode}"
            )
            raise StepFailed(
                f"{what} to say within {TIMEOUT:.0f} s that it had begun; saw {seen}"
            )
        said = json.loads(line)
        self.say(f"    > run {said['id']}, pid {said['pid']}")
        self.say(f"    > its runregistrykit: {said['file']}")
        self.check(said["pid"] == child.pid, f"its pid to be {child.pid}", said["pid"])
        self.check(
            said["file"] == self.package_file,
            f"the child to import {self.package_file}",
            said["file"],
        )
        return child, said

    def reap(self, child, kill=False):
        """Kill ``child`` if asked, wait for it, and return its returncode."""
        if kill and child.poll() is None:
            child.kill()
        try:
            return child.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            child.kill()
            return child.wait(timeout=TIMEOUT)

    def wait_for(self, run_id, condition, what):
        """Wait until ``condition`` holds of the run's status; fail after ``TIMEOUT``."""
        deadline = time.monotonic() + TIMEOUT
        while time.monotonic() < deadline:
            status = self.status(run_id)
            if isinstance(status, dict) and condition(status):
                return status
            time.sleep(0.05)
        raise StepFailed(f"{what} within {TIMEOUT:.0f} s; saw {self.status(run_id)!r}")

    def needs(self, said, which):
        self.check(said is not None, f"{which}", "none: its step did not make it")
        return said

    # --- the client root -------------------------------------------------------------------------

    def build_root(self):
        self.client.mkdir()
        (self.client / "runregistrykit.toml").write_text(self.extraction.CONFIG)
        (self.client / ".gitignore").write_text(self.extraction.GITIGNORE)
        (self.client / "job.py").write_text(self.extraction.JOB)
        (self.client / "smoke_registry.py").write_text(self.extraction.REGISTRY_SOURCE)
        self.git("init", "-q", cwd=self.client)
        self.git("add", "-A", cwd=self.client)
        self.git(
            "-c",
            "user.name=interrupted-run smoke",
            "-c",
            "user.email=interrupted-run-smoke@example.invalid",
            "commit",
            "-q",
            "-m",
            "The smoke client root",
            cwd=self.client,
        )

    # --- the steps -------------------------------------------------------------------------------

    def step_1(self):
        """a store written by the client's module, and `store create --purpose`"""
        primary = self.registry().write_store(self.stores, self.primary.stem)
        self.check(
            Path(primary) == self.primary.resolve(),
            f"the writer to return {self.primary}",
            primary,
        )
        result = self.command(
            "store", "create", self.primary, "--purpose", "the smoke run's store"
        )
        self.show_lines(result.stdout, ">> create")
        fields = json.loads(self.sidecar(self.primary).read_text())
        self.say(
            f"    > sidecar_format {fields.get('sidecar_format')}, "
            f"store_id {fields.get('store_id')}"
        )
        self.check(
            fields.get("sidecar_format") == 1,
            "sidecar_format 1",
            fields.get("sidecar_format"),
        )

    def step_2(self):
        """a hard kill: a child begun on the store, heartbeating, sent SIGKILL and reaped"""
        import runregistrykit

        child, said = self.start(
            HARD_KILLED, self.primary, "the hard-killed run's child"
        )
        self.killed, self.killed_said = child, said
        self.wait_for(
            said["id"],
            lambda status: (status.get("units_done") or 0) >= 1,
            "a heartbeat from the child",
        )
        child.send_signal(signal.SIGKILL)
        self.say(f"  sent SIGKILL to pid {child.pid}")
        returncode = self.reap(child)
        self.say(f"    > reaped: returncode {returncode}")
        self.check(returncode == -signal.SIGKILL, "returncode -9", returncode)
        status = self.status(said["id"])
        self.check(isinstance(status, dict), "a status that parses", repr(status))
        host = status.get("host")
        recorded = host if isinstance(host, dict) else {}
        boot = recorded.get("boot")
        # the boot is shown by its length: it identifies this machine's boot, and is not printed
        self.say(
            f"    > status: state {status.get('state')}, pid {status.get('pid')}, "
            f"units_done {status.get('units_done')}, host keys {sorted(recorded)}, "
            f"host.id {recorded.get('id')}, host.boot "
            f"{f'<{len(boot)} characters>' if isinstance(boot, str) else boot}"
        )
        judged = runregistrykit.liveness(status, runregistrykit.DEFAULT_STALE_AFTER)
        self.say(
            f"    > liveness(status, {runregistrykit.DEFAULT_STALE_AFTER:.0f}): {judged}"
        )
        self.check(
            status.get("state") == "running", "state running", status.get("state")
        )
        self.check(status.get("pid") == said["pid"], "its pid", status.get("pid"))
        self.check(
            isinstance(host, dict)
            and sorted(host) == ["boot", "id"]
            and host["id"] is not None
            and host["boot"] is not None,
            "host {id, boot}, each recorded",
            host,
        )
        self.check(judged == "stale", "liveness stale", judged)

    def step_3(self):
        """`list`: the hard-killed run marked `!!`, and stderr naming `end`"""
        said = self.needs(self.killed_said, "the hard-killed run of step 2")
        result = self.command("list")
        rows = self.show_lines(result.stdout, said["id"])
        self.show_lines(result.stdout, "run(s) under")
        self.show_lines(result.stderr, END_COMMAND)
        self.check(len(rows) == 1, "one row for the run", len(rows))
        self.check(rows[0].startswith("!! "), "the row marked !!", repr(rows[0][:2]))
        self.check(
            END_COMMAND in result.stderr,
            f"stderr naming `{END_COMMAND}`",
            result.stderr.strip(),
        )

    def step_4(self):
        """`store fingerprint` refused, naming the run and `end`"""
        said = self.needs(self.killed_said, "the hard-killed run of step 2")
        result = self.command("store", "fingerprint", self.primary, expect=1)
        refusal = self.show_lines(result.stderr, "!!")
        text = result.stderr
        self.check(said["id"] in text, f"the refusal naming {said['id']}", refusal)
        self.check(END_COMMAND in text, f"the refusal naming `{END_COMMAND}`", refusal)

    def step_5(self):
        """a second `begin` on the store refused, with no run directory made"""
        import runregistrykit

        said = self.needs(self.killed_said, "the hard-killed run of step 2")
        before = self.listing()
        try:
            run = runregistrykit.begin(
                "smoke",
                "05",
                "second",
                "a second run on the store, which is refused",
                script=str(self.client / "job.py"),
                results=str(self.primary),
            )
        except RuntimeError as e:
            text = str(e)
        else:
            raise StepFailed(f"a RuntimeError from begin(); saw run {run.id} begun")
        self.say(f"  begin(): RuntimeError: {text}")
        after = self.listing()
        self.say(f"    > runs root before: {before}")
        self.say(f"    > runs root after:  {after}")
        self.check(said["id"] in text, f"the refusal naming {said['id']}", "not named")
        self.check(END_COMMAND in text, f"the refusal naming `{END_COMMAND}`", "not")
        self.check(
            text.endswith("No run directory was created"),
            "the refusal ending 'No run directory was created'",
            text[-40:],
        )
        self.check(before == after, "the runs root unchanged", after)

    def step_6(self):
        """a live pid refused by `end`, with and without `--unverified`"""
        child, said = self.start(SIGNALLED, self.second, "the signalled run's child")
        self.signalled, self.signalled_said = child, said
        self.wait_for(
            said["id"],
            lambda status: (status.get("units_done") or 0) >= 1,
            "a heartbeat from the child",
        )
        reason = "the smoke run tries to end a live run"
        for extra in ((), ("--unverified",)):
            result = self.command(
                "end", said["id"], "--reason", reason, *extra, expect=1
            )
            self.show_lines(result.stderr, "!!")
            self.check(
                "answers kill -0" in result.stderr,
                "a refusal saying its pid answers kill -0",
                result.stderr.strip(),
            )
        self.check(child.poll() is None, "the child still running", child.returncode)
        status = self.status(said["id"])
        self.say(
            f"    > status: state {status.get('state')}, ended "
            f"{'present' if 'ended' in status else 'absent'}, exit_code "
            f"{status.get('exit_code')}, pid {status.get('pid')}"
        )
        self.check(
            status.get("state") == "running", "state running", status.get("state")
        )
        self.check("ended" not in status, "no ended", status.get("ended"))
        self.check(
            status.get("exit_code") is None, "exit_code null", status.get("exit_code")
        )
        self.check(status.get("pid") == said["pid"], "its pid", status.get("pid"))

    def step_7(self):
        """a real SIGTERM: the child's handler records `killed`, 143, and exits"""
        child = self.needs(self.signalled, "the signalled run's child of step 6")
        said = self.signalled_said
        self.check(child.poll() is None, "the child still running", child.returncode)
        child.send_signal(signal.SIGTERM)
        self.say(f"  sent SIGTERM to pid {child.pid}")
        returncode = self.reap(child)
        self.say(f"    > reaped: returncode {returncode}")
        status = self.status(said["id"])
        left = sorted(
            p.name for p in (self.runs / said["id"]).glob("status.json.*.tmp")
        )
        self.say(
            f"    > status: {'parses' if isinstance(status, dict) else 'does not parse'}, "
            f"state {status.get('state') if isinstance(status, dict) else None}, exit_code "
            f"{status.get('exit_code') if isinstance(status, dict) else None}"
        )
        self.say(f"    > temporary files left: {left or 'none'}")
        self.check(returncode == 143, "returncode 143", returncode)
        self.check(isinstance(status, dict), "a status that parses", repr(status))
        self.check(status.get("state") == "killed", "state killed", status.get("state"))
        self.check(
            status.get("exit_code") == 143, "exit_code 143", status.get("exit_code")
        )
        self.check(left == [], "no status.json.*.tmp left", left)

    def step_8(self):
        """`end` of the hard-killed run: no `--reason` refused by argparse, then the run `lost`"""
        said = self.needs(self.killed_said, "the hard-killed run of step 2")
        result = self.command("end", said["id"], expect=2)
        self.show_lines(result.stderr, "--reason")
        reason = "the smoke run's child was sent SIGKILL by the script"
        result = self.command("end", said["id"], "--reason", reason)
        self.show_lines(result.stdout, ">> end")
        expected = (
            f">> end: {said['id']} is now lost, verified: its pid {said['pid']} does not "
            f"answer kill -0 on this host"
        )
        self.check(result.stdout.strip() == expected, expected, result.stdout.strip())
        status = self.status(said["id"])
        ended = status.get("ended") or {}
        evidence = ended.get("evidence") or {}
        self.say(
            f"    > status: state {status.get('state')}, exit_code {status.get('exit_code')}, "
            f"ended.verified {ended.get('verified')}, ended.evidence.pid_answers "
            f"{evidence.get('pid_answers')}, ended.reason {ended.get('reason')!r}"
        )
        self.check(status.get("state") == "lost", "state lost", status.get("state"))
        self.check(
            "exit_code" in status and status["exit_code"] is None,
            "exit_code null",
            status.get("exit_code", "absent"),
        )
        self.check(
            ended.get("verified") is True, "ended.verified true", ended.get("verified")
        )
        self.check(
            evidence.get("pid_answers") is False,
            "ended.evidence.pid_answers false",
            evidence.get("pid_answers"),
        )

    def step_9(self):
        """`end` of the hard-killed run again: refused, it has already ended"""
        said = self.needs(self.killed_said, "the hard-killed run of step 2")
        status = self.status(said["id"]) or {}
        # a run that step 8 did not end is not ended here: this step is the refusal of a second end
        self.check(
            status.get("state") == "lost",
            "the run lost by step 8, before it is ended again",
            status.get("state"),
        )
        result = self.command(
            "end", said["id"], "--reason", "the smoke run ends it twice", expect=1
        )
        self.show_lines(result.stderr, "!!")
        self.check(
            "its status says it has already ended" in result.stderr,
            "a refusal saying its status says it has already ended",
            result.stderr.strip(),
        )

    def step_10(self):
        """`list`: the run `lost`, unmarked, and every run counted finished"""
        said = self.needs(self.killed_said, "the hard-killed run of step 2")
        result = self.command("list")
        rows = self.show_lines(result.stdout, said["id"])
        summary = self.show_lines(result.stdout, "run(s) under")
        listed = self.listing()
        self.check(len(rows) == 1, "one row for the run", len(rows))
        self.check(rows[0].startswith("   "), "the row unmarked", repr(rows[0][:2]))
        self.check(" lost " in rows[0], "the run lost", rows[0].strip())
        expected = f"{len(listed)} run(s) under {self.runs}: {len(listed)} finished;"
        self.check(
            len(summary) == 1 and summary[0].startswith(expected),
            f"the summary beginning {expected!r}".replace(str(self.base), "$SMOKE"),
            summary,
        )

    def step_11(self):
        """the resume: `begin` on the store accepted, and its fingerprint recorded"""
        import runregistrykit

        run = runregistrykit.begin(
            "smoke",
            "11",
            "resumed",
            "a smoke run resumed on the store after the hard kill",
            script=str(self.client / "job.py"),
            results=str(self.primary),
        )
        self.resumed = run
        self.say(f"  begin(): {run.id}")
        run.heartbeat(units_done=1, units_total=1, stage="resumed")
        run.finish("done", exit_code=0, fingerprint=True)
        status = json.loads(Path(run.status_path).read_text())
        digest = (status.get("fingerprint") or {}).get("digest")
        self.say(
            f"    > status: state {status.get('state')}, exit_code {status.get('exit_code')}, "
            f"fingerprint_sidecar {status.get('fingerprint_sidecar')!r}"
        )
        if "fingerprint_error" in status:
            self.say(f"    > fingerprint_error: {status['fingerprint_error']}")
        self.say(f"    > digest: {digest}")
        self.check(status.get("state") == "done", "state done", status.get("state"))
        self.check(
            "fingerprint_error" not in status,
            "no fingerprint_error",
            status.get("fingerprint_error"),
        )
        self.check(digest is not None, "a fingerprint in status.json", "none")
        self.check(
            status.get("fingerprint_sidecar") == "written",
            "fingerprint_sidecar 'written'",
            status.get("fingerprint_sidecar"),
        )

    def step_12(self):
        """`store fingerprint` matching, and `store retire --dry-run`, each exiting 0"""
        result = self.command("store", "fingerprint", self.primary)
        self.show_lines(result.stdout, "digest:", "recorded:")
        self.check(
            "recorded: matches the fingerprint taken" in result.stdout,
            "'recorded: matches ...'",
            "no match",
        )
        result = self.command(
            "store",
            "retire",
            self.primary,
            "--reason",
            "the smoke run checks the store could be retired",
            "--dry-run",
        )
        self.show_lines(result.stdout, "dry run:")
        self.check("dry run:" in result.stdout, "a dry run", result.stdout.strip())

    def step_13(self):
        """the resumed run's manifest `host.id` recorded, and its status's"""
        run = self.needs(self.resumed, "the resumed run of step 11")
        manifest = json.loads(Path(run.manifest_path).read_text())
        status = json.loads(Path(run.status_path).read_text())
        recorded = (manifest.get("host") or {}).get("id")
        written = (status.get("host") or {}).get("id")
        self.say(f"    > manifest host.id {recorded}, status host.id {written}")
        self.check(recorded is not None, "a manifest host.id", recorded)
        self.check(recorded == written, f"the status's host.id {written}", recorded)

    # --- the children, at the end --------------------------------------------------------------

    def reap_every_child(self):
        """Kill and reap any child still alive, reap any that has exited; say which."""
        said = []
        for child in self.children:
            if child.returncode is not None:
                continue
            if child.poll() is None:
                child.kill()
                returncode = child.wait(timeout=TIMEOUT)
                said.append(
                    f"killed and reaped pid {child.pid} (returncode {returncode})"
                )
            else:
                said.append(
                    f"reaped pid {child.pid}, which had exited (returncode {child.returncode})"
                )
        return said


STEPS = (
    Smoke.step_1,
    Smoke.step_2,
    Smoke.step_3,
    Smoke.step_4,
    Smoke.step_5,
    Smoke.step_6,
    Smoke.step_7,
    Smoke.step_8,
    Smoke.step_9,
    Smoke.step_10,
    Smoke.step_11,
    Smoke.step_12,
    Smoke.step_13,
)


def _version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument(
        "--clean",
        action="store_true",
        help="remove the smoke run's directory at the end (and nothing else)",
    )
    args = parser.parse_args(argv)

    if shutil.which("git") is None:
        print("CANNOT START: no git on PATH", file=sys.stderr)
        return 2
    try:
        import runregistrykit
    except ImportError as e:
        print(f"CANNOT START: runregistrykit is not importable ({e})", file=sys.stderr)
        return 2
    try:
        extraction = load_extraction()
    except Exception as e:
        print(f"CANNOT START: {e}", file=sys.stderr)
        return 2

    package_file = runregistrykit.__file__
    print(f"python          {platform.python_version()} ({sys.executable})")
    print(f"runregistrykit  {_version('runregistrykit')} ({package_file})")
    for name in ("datastorekit", "ray", "sqlalchemy"):
        print(f"{name:15} {_version(name)}")
    print(f"client files    from {EXTRACTION_SCRIPT}")

    base = Path(tempfile.mkdtemp(prefix="interrupted-smoke-")).resolve()
    print(f"directory       $SMOKE = {base}")

    start = time.monotonic()
    smoke = Smoke(base, extraction, package_file)
    try:
        smoke.build_root()
    except Exception as e:
        print(f"CANNOT START: the client root could not be built: {e}", file=sys.stderr)
        return 2

    # what a command run in the client root imports: the same file, under site-packages
    commands = subprocess.run(
        [sys.executable, "-c", "import runregistrykit; print(runregistrykit.__file__)"],
        cwd=smoke.client,
        env=smoke.env(),
        capture_output=True,
        text=True,
    ).stdout.strip()
    print(f"its commands    import {commands}")
    purelib = sysconfig.get_paths()["purelib"]
    on_the_pin = package_file == commands and Path(
        package_file
    ).resolve().is_relative_to(Path(purelib).resolve())
    print(
        f"site-packages   {purelib}: {'the package is under it' if on_the_pin else 'NOT'}"
    )
    print()

    failed = [] if on_the_pin else ["site-packages"]
    os.chdir(smoke.client)
    try:
        for step in STEPS:
            number = int(step.__name__.split("_")[1])
            smoke.lines = []
            title = step.__doc__.strip()
            try:
                step(smoke)
                verdict = "PASS"
            except StepFailed as e:
                verdict = "FAIL"
                smoke.say(f"  !! {e}")
            except Exception as e:
                verdict = "FAIL"
                where = traceback.extract_tb(e.__traceback__)[-1]
                smoke.say(
                    f"  !! {type(e).__name__}: {e} "
                    f"({Path(where.filename).name}:{where.lineno})"
                )
            if verdict == "FAIL":
                failed.append(number)
            print(f"{verdict} step {number}: {title}")
            for line in smoke.lines:
                print(line)
    finally:
        said = smoke.reap_every_child()
        os.chdir(base)
    elapsed = time.monotonic() - start

    print()
    print(
        f"children: {len(smoke.children)} started; "
        + ("; ".join(said) if said else "each reaped by its step")
    )
    ray = sys.modules.get("ray")
    if ray is None:
        print("ray: not imported")
    else:
        initialised = ray.is_initialized()
        print(f"ray: imported, initialised: {initialised}")
        if initialised:
            failed.append("ray")
    print(f"time: {elapsed:.1f} s")
    if args.clean:
        shutil.rmtree(base)
        print(f"removed {base}")
    else:
        print(f"left in place: {base}")
    if failed:
        print(f"RESULT: FAIL ({', '.join(str(n) for n in failed)})")
        return 1
    print(f"RESULT: OK ({len(STEPS)} steps passed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
