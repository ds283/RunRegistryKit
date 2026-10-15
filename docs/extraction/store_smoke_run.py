#!/usr/bin/env python3
"""
A smoke run of the store layer end to end, as a client uses it (extraction prompt 08, section 2.2;
README section 6.2, U23 and U24).

It builds a client root in a new ``tempfile`` directory, as a client's repository would hold one,
and drives the registry there: every ``store`` command, a run that takes a fingerprint, a run
launched from a linked git worktree, and two refusals. The client root is a git repository with
one commit, holding

- ``runregistrykit.toml``, recording the distribution ``datastorekit`` and naming the fingerprinter
  ``smoke_registry:FINGERPRINTER``;
- ``.gitignore``, ignoring ``var/``;
- ``job.py``, the script a run's ``begin()`` is given;
- ``smoke_registry.py``, the client's registry and fingerprinter module, written from
  ``REGISTRY_SOURCE`` below: four factories on public ``datastorekit`` names (the version and tag
  tables of ``datastorekit.contract``, one replicated class and one sharded class with a parent),
  a writer of a closed store of two shards, and ``FINGERPRINTER``, a
  ``DatastoreKitFingerprinter`` over them.

It imports ``runregistrykit``, the standard library, and nothing of ``runregistrykit.tests``, so it
runs against an installed release as well as a checkout. It never imports ``datastorekit`` at
module scope: the client's module imports it, inside the steps that need it, so without the extra
``[stores]`` the script starts, the steps that need a store or a fingerprinter fail, each saying
what it saw, and the others run. It never initialises Ray, and checks at the end that ``ray``, if
something imported it, is not initialised.

Run it with the package importable, from anywhere, with ``TMPDIR`` naming where its directory goes:

    TMPDIR=<scratch> python docs/extraction/store_smoke_run.py [--clean]

Each command runs as ``sys.executable -m runregistrykit ...`` in the client root, as a client runs
it. The script prints the versions it runs with (Python, ``runregistrykit`` and where it was
imported from, and ``datastorekit``, Ray and SQLAlchemy where installed), then each step's
``PASS`` or ``FAIL`` with its commands, their exit codes, and the lines that show the outcome; a
step that raises, or whose command exits otherwise than it should, is that step's ``FAIL``, and the
next step runs. The fingerprint's digest is printed, never asserted: it is the client's module's.
Every value asserted is the script's own.

The steps:

1. a store written by the client's module, and ``store create --purpose``;
2. ``begin()`` naming the store as ``results``, with a unit ledger; ``heartbeat``, ``record``,
   ``known`` and ``finish("done", exit_code=0, fingerprint=True)``: the status ``done`` with a
   fingerprint written into the sidecar and no ``fingerprint_error``, and the manifest recording
   ``runregistrykit`` and ``datastorekit``;
3. ``list``: one run, finished;
4. ``store show``: a registry sidecar with no problem, and the run naming the store;
5. ``store fingerprint``: a fresh fingerprint matching the recorded one;
6. ``store copy --purpose`` of the store, then ``store move`` of the copy;
7. ``store amend --field x_note --remove --reason`` of an unknown field written into the moved
   copy's sidecar by hand;
8. ``store adopt`` of a second store whose sidecar is a legacy object, with no ``sidecar_format``;
9. ``store retire --dry-run``, ``store retire`` and ``store show`` of the moved copy: its files
   gone, its sidecar kept as a completed tombstone;
10. a linked worktree of the client root (``git worktree add``), and a run begun with its script in
    the worktree, recorded under the main checkout's runs root;
11. the refusals: ``store show`` in a client root whose config names no fingerprinter, and ``list``
    in a directory with no ``runregistrykit.toml`` above it, each exiting 1.

It removes nothing it did not make. Its directory is left in place for inspection unless
``--clean`` is given, which removes that directory and nothing else. Exits 0 when every step
passes, 1 when one fails, and 2 when it cannot start (no ``git`` on ``PATH``, or ``runregistrykit``
not importable). It is not a test and does not run in CI.
"""

import argparse
import importlib
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

CONFIG = """\
distributions = ["datastorekit"]

[stores]
fingerprinter = "smoke_registry:FINGERPRINTER"
"""

GITIGNORE = "var/\n"

JOB = '''\
"""The script a smoke run's begin() is given; it is hashed, never run."""

print("smoke job")
'''

REGISTRY_SOURCE = '''\
"""The smoke client's registry and fingerprinter, on public datastorekit names only."""

import sqlite3
from datetime import datetime
from pathlib import Path

import sqlalchemy as sqla

from datastorekit.SQL.factory_base import SQLAFactoryBase
from datastorekit.SQL.schema import build_schema
from datastorekit.contract import (
    TAG_LABEL,
    TAG_SERIAL,
    TAG_TABLE,
    VERSION_LABEL,
    VERSION_TABLE,
)
from datastorekit.shard_paths import shard_file_name
from datastorekit.store_inventory import InventorySpec, Parent

from runregistrykit.fingerprint import DatastoreKitFingerprinter

FORMAT = 1
TIMESTAMP = datetime(2026, 10, 15, 12, 0, 0)
REPLICATED = (VERSION_TABLE, TAG_TABLE, "Grid")


class _Factory(SQLAFactoryBase):
    @staticmethod
    def register():
        raise NotImplementedError

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        raise NotImplementedError("the smoke store's rows are written directly")


class VersionFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [sqla.Column(VERSION_LABEL, sqla.String(64), nullable=False)],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(leaves=(VERSION_LABEL,))


class TagFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [sqla.Column(TAG_LABEL, sqla.String(64), nullable=False)],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(leaves=(TAG_LABEL,))


class GridFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [sqla.Column("k", sqla.Float, nullable=False)],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(leaves=("k",))


class PointFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [
                sqla.Column("grid_serial", sqla.Integer, sqla.ForeignKey("Grid.serial")),
                sqla.Column("x", sqla.Float, nullable=False),
                sqla.Column("label", sqla.String(64), nullable=True),
            ],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("x",), parents={"grid": Parent("grid_serial", of="Grid")}
        )


FACTORIES = {
    VERSION_TABLE: VersionFactory,
    TAG_TABLE: TagFactory,
    "Grid": GridFactory,
    "Point": PointFactory,
}

FINGERPRINTER = DatastoreKitFingerprinter(FACTORIES, FORMAT)

REPLICATED_ROWS = {
    VERSION_TABLE: [{"serial": 1, VERSION_LABEL: "smoke-1"}],
    TAG_TABLE: [{"serial": 1, TAG_LABEL: "smoke"}],
    "Grid": [{"serial": 1, "k": 0.5}, {"serial": 2, "k": 2.0}],
}

# shard serial -> its points: grid 1 on shard 0, grid 2 on shard 1
SHARDED_ROWS = {
    0: [{"serial": 1, "grid_serial": 1, "x": 1.5}, {"serial": 2, "grid_serial": 1, "x": 2.5}],
    1: [{"serial": 3, "grid_serial": 2, "x": 3.5}],
}


def write_store(directory, stem):
    """Write a closed store of two shards in ``directory``; return its primary's path."""
    primary = (Path(directory) / f"{stem}.sqlite").resolve()
    primary.parent.mkdir(parents=True, exist_ok=True)
    metadata = sqla.MetaData()
    tables = build_schema(metadata, FACTORIES).tables
    shard_files = {}
    for serial, points in SHARDED_ROWS.items():
        path = primary.parent / shard_file_name(primary, serial)
        engine = sqla.create_engine(f"sqlite:///{path}", future=True)
        try:
            metadata.create_all(engine)
            with engine.begin() as conn:
                for name, rows in list(REPLICATED_ROWS.items()) + [("Point", points)]:
                    rows = [dict(row, timestamp=TIMESTAMP) for row in rows]
                    conn.execute(sqla.insert(tables[name]), rows)
        finally:
            engine.dispose()
        shard_files[serial] = path
    conn = sqlite3.connect(primary)
    try:
        with conn:
            conn.execute(
                "CREATE TABLE shards (serial INTEGER NOT NULL PRIMARY KEY, "
                "filename VARCHAR NOT NULL)"
            )
            conn.execute(
                'CREATE TABLE replicated_tables (serial INTEGER NOT NULL PRIMARY KEY, '
                '"table" VARCHAR NOT NULL)'
            )
            conn.executemany(
                "INSERT INTO shards (serial, filename) VALUES (?, ?)",
                [(serial, path.name) for serial, path in sorted(shard_files.items())],
            )
            conn.executemany(
                'INSERT INTO replicated_tables (serial, "table") VALUES (?, ?)',
                list(enumerate(REPLICATED)),
            )
    finally:
        conn.close()
    return primary
'''

# the git environment a child must not inherit, so that it reads the client root's repository
GIT_ENVIRONMENT = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR")


class StepFailed(Exception):
    """A step's check that did not hold: what it expected, and what it saw."""


class Smoke:
    def __init__(self, base: Path):
        self.base = base
        self.client = base / "client"
        self.worktree = base / "worktree"
        self.no_fingerprinter = base / "no-fingerprinter"
        self.elsewhere = base / "elsewhere"
        self.stores = self.client / "var" / "datastores"
        self.runs = self.client / "var" / "runs"
        self.primary = self.stores / "smoke-store.sqlite"
        self.copy = self.stores / "smoke-copy.sqlite"
        self.moved = self.stores / "smoke-moved.sqlite"
        self.legacy = self.stores / "smoke-legacy.sqlite"
        self.lines = []
        self.digests = []

    # --- helpers ---------------------------------------------------------------------------------

    def say(self, line=""):
        """Keep ``line`` for the step's report, with the smoke directory written ``$SMOKE``."""
        self.lines.append(line.replace(str(self.base), "$SMOKE"))

    def check(self, condition, expected, seen):
        if not condition:
            raise StepFailed(f"expected {expected}; saw {seen}")

    def env(self):
        env = {k: v for k, v in os.environ.items() if k not in GIT_ENVIRONMENT}
        env.pop("PYTHONSAFEPATH", None)
        return env

    def git(self, *args, cwd):
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=self.env(),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise StepFailed(
                f"git {' '.join(args)} to exit 0; saw exit {result.returncode}: "
                f"{result.stderr.strip()}"
            )
        return result.stdout

    def command(self, *args, cwd=None, expect=0):
        """Run ``python -m runregistrykit`` with ``args`` in ``cwd`` and check its exit code."""
        cwd = self.client if cwd is None else cwd
        argv = [sys.executable, "-m", "runregistrykit", *[str(a) for a in args]]
        result = subprocess.run(
            argv, cwd=cwd, env=self.env(), capture_output=True, text=True
        )
        shown = " ".join(str(a) for a in args)
        self.say(f"  $ python -m runregistrykit {shown}   (in {cwd.name}/)")
        self.say(f"    exit {result.returncode}")
        if result.returncode != expect:
            for line in (result.stdout + result.stderr).strip().splitlines()[-6:]:
                self.say(f"    | {line}")
            raise StepFailed(
                f"exit {expect} from `{shown}`; saw exit {result.returncode}"
            )
        return result

    def show_lines(self, text, *prefixes):
        """Say each line of ``text`` that starts with one of ``prefixes``; return them."""
        found = [
            line
            for line in text.splitlines()
            if line.strip().startswith(tuple(prefixes))
        ]
        for line in found:
            self.say(f"    > {line.strip()}")
        return found

    def registry(self):
        """The client's registry module, imported as the package's loader imports it."""
        if str(self.client) not in sys.path:
            sys.path.insert(0, str(self.client))
        return importlib.import_module("smoke_registry")

    def sidecar(self, primary):
        return primary.with_name(primary.stem + ".manifest.json")

    def store_files(self, primary):
        """The primary and the shard files beside it that share its stem."""
        return sorted(
            p
            for p in primary.parent.iterdir()
            if p.name == primary.name
            or (p.name.startswith(primary.stem + ".") and p.suffix == ".sqlite")
            or p.name.startswith(primary.stem + "-shard")
        )

    # --- the client root -------------------------------------------------------------------------

    def build_root(self):
        self.client.mkdir()
        (self.client / "runregistrykit.toml").write_text(CONFIG)
        (self.client / ".gitignore").write_text(GITIGNORE)
        (self.client / "job.py").write_text(JOB)
        (self.client / "smoke_registry.py").write_text(REGISTRY_SOURCE)
        self.git("init", "-q", cwd=self.client)
        self.git("add", "-A", cwd=self.client)
        self.git(
            "-c",
            "user.name=store smoke",
            "-c",
            "user.email=store-smoke@example.invalid",
            "commit",
            "-q",
            "-m",
            "The smoke client root",
            cwd=self.client,
        )
        self.no_fingerprinter.mkdir()
        (self.no_fingerprinter / "runregistrykit.toml").write_text("")
        self.elsewhere.mkdir()

    # --- the steps -------------------------------------------------------------------------------

    def step_1(self):
        """a store written by the client's module, and `store create --purpose`"""
        primary = self.registry().write_store(self.stores, self.primary.stem)
        self.check(
            Path(primary) == self.primary.resolve(),
            f"the writer to return {self.primary}",
            primary,
        )
        files = self.store_files(self.primary)
        self.say(f"  written: {', '.join(p.name for p in files)}")
        self.check(len(files) == 3, "a primary and two shards", len(files))
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
        """a run that takes a fingerprint of its results store"""
        import runregistrykit

        run = runregistrykit.begin(
            "smoke",
            "02",
            "fingerprinted",
            "a smoke run that fingerprints its results store",
            script=str(self.client / "job.py"),
            results=str(self.primary),
            unit="u",
            expected_units=1,
            checkpoint=True,
        )
        self.say(f"  begin(): {run.id}")
        self.check(
            Path(run.path).resolve().parent == self.runs.resolve(),
            f"the run under {self.runs}",
            run.path,
        )
        run.heartbeat(units_done=0, units_total=1, stage="working")
        run.record("u1", {"value": 1})
        known = run.known()
        self.say(f"  known(): {sorted(known)}")
        self.check(sorted(known) == ["u1"], '["u1"]', sorted(known))
        run.finish("done", exit_code=0, fingerprint=True)
        status = json.loads(Path(run.status_path).read_text())
        manifest = json.loads(Path(run.manifest_path).read_text())
        digest = (status.get("fingerprint") or {}).get("digest")
        self.say(
            f"    > status: state {status.get('state')}, exit_code "
            f"{status.get('exit_code')}, fingerprint_sidecar "
            f"{status.get('fingerprint_sidecar')!r}"
        )
        if "fingerprint_error" in status:
            self.say(f"    > fingerprint_error: {status['fingerprint_error']}")
        self.say(f"    > digest: {digest}")
        self.say(f"    > manifest packages: {sorted(manifest.get('packages') or {})}")
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
        sidecar = json.loads(self.sidecar(self.primary).read_text())
        recorded = (sidecar.get("fingerprint") or {}).get("digest")
        self.check(
            recorded == digest, "the sidecar to record the same digest", recorded
        )
        packages = manifest.get("packages") or {}
        self.check(
            {"runregistrykit", "datastorekit"} <= set(packages),
            "packages naming runregistrykit and datastorekit",
            sorted(packages),
        )
        self.digests.append(("status.json", digest))
        self.run_id = run.id

    def step_3(self):
        """`list`: one run, finished"""
        result = self.command("list")
        self.show_lines(result.stdout, "smoke-", "1 run(s)")
        rows = [line for line in result.stdout.splitlines() if "smoke-02-" in line]
        self.check(len(rows) == 1, "one run listed", len(rows))
        self.check(" done " in rows[0], "the run done", rows[0].strip())
        self.check(
            "1 run(s) under" in result.stdout and "1 finished." in result.stdout,
            "the summary '1 run(s) ... 1 finished.'",
            result.stdout.strip().splitlines()[-1],
        )

    def step_4(self):
        """`store show`: a registry sidecar, no problems, the run naming the store"""
        result = self.command("store", "show", self.primary)
        self.show_lines(result.stdout, "kind:", "problems:", "smoke-02-")
        self.check("kind:     registry" in result.stdout, "kind registry", "another")
        self.check("problems: none" in result.stdout, "problems: none", "problems")
        named = [
            line
            for line in result.stdout.splitlines()
            if line.strip().startswith("smoke-02-")
        ]
        self.check(len(named) == 1, "one run naming the store", len(named))

    def step_5(self):
        """`store fingerprint`: the recorded fingerprint matched by a fresh one"""
        result = self.command("store", "fingerprint", self.primary)
        found = self.show_lines(result.stdout, "digest:", "format:", "recorded:")
        digest = [line.split()[1] for line in found if line.startswith("digest:")]
        self.check(len(digest) == 1, "one digest line", len(digest))
        self.digests.append(("store fingerprint", digest[0]))
        self.check(
            "recorded: matches the fingerprint taken" in result.stdout,
            "'recorded: matches ...'",
            "no match",
        )

    def step_6(self):
        """`store copy --purpose` of the store, and `store move` of the copy"""
        result = self.command(
            "store", "copy", self.primary, self.copy, "--purpose", "a smoke copy"
        )
        self.show_lines(result.stdout, ">> copy")
        copied = self.store_files(self.copy)
        self.check(len(copied) == 3, "the copy's primary and two shards", len(copied))
        self.check(self.sidecar(self.copy).is_file(), "the copy's sidecar", "none")
        result = self.command("store", "move", self.copy, self.moved)
        self.show_lines(result.stdout, ">> move")
        moved = self.store_files(self.moved)
        self.say(f"  moved: {', '.join(p.name for p in moved)}")
        self.check(len(moved) == 3, "the moved primary and two shards", len(moved))
        self.check(
            not self.copy.exists() and not self.sidecar(self.copy).exists(),
            "nothing left at the copy's name",
            [p.name for p in self.store_files(self.copy)],
        )
        fields = json.loads(self.sidecar(self.moved).read_text())
        operations = [entry.get("operation") for entry in fields.get("history", [])]
        self.say(f"    > history: {operations}")
        self.check(
            operations[-2:] == ["copy", "move"],
            "history ending copy, move",
            operations,
        )

    def step_7(self):
        """`store amend --field x_note --remove` of a field written by hand"""
        path = self.sidecar(self.moved)
        fields = json.loads(path.read_text())
        fields["x_note"] = "written by hand"
        path.write_text(json.dumps(fields, indent=2, sort_keys=True) + "\n")
        self.say("  wrote x_note into the moved copy's sidecar by hand")
        result = self.command(
            "store",
            "amend",
            self.moved,
            "--field",
            "x_note",
            "--remove",
            "--reason",
            "the smoke run removes a field it wrote",
        )
        self.show_lines(result.stdout, "field:", "before:", "after:", ">> amended")
        fields = json.loads(path.read_text())
        self.check("x_note" not in fields, "x_note removed", fields.get("x_note"))
        last = fields["history"][-1].get("operation")
        self.check(last == "amend", "a last history entry 'amend'", last)

    def step_8(self):
        """`store adopt` of a store whose sidecar is a legacy object"""
        self.registry().write_store(self.stores, self.legacy.stem)
        legacy = {"datastore": self.legacy.name, "purpose": "a legacy smoke store"}
        self.sidecar(self.legacy).write_text(json.dumps(legacy, indent=2) + "\n")
        self.say(f"  wrote the legacy sidecar: {json.dumps(legacy, sort_keys=True)}")
        result = self.command("store", "adopt", self.legacy)
        self.show_lines(result.stdout, ">> adopt")
        fields = json.loads(self.sidecar(self.legacy).read_text())
        operations = [entry.get("operation") for entry in fields.get("history", [])]
        self.say(
            f"    > sidecar_format {fields.get('sidecar_format')}, purpose "
            f"{fields.get('purpose')!r}, history {operations}"
        )
        self.check(
            fields.get("sidecar_format") == 1,
            "sidecar_format 1",
            fields.get("sidecar_format"),
        )
        self.check(operations == ["adopt"], "history ['adopt']", operations)

    def step_9(self):
        """`store retire --dry-run`, `store retire` and `store show` of the moved copy"""
        reason = "the smoke run retires its moved copy"
        before = self.store_files(self.moved)
        result = self.command(
            "store", "retire", self.moved, "--reason", reason, "--dry-run"
        )
        self.show_lines(result.stdout, "dry run:", "files to be deleted:")
        # the files are printed relative to the record root, the client root here
        listed = os.path.relpath(self.moved.parent, self.client) + "/" + self.moved.stem
        planned = self.show_lines(result.stdout, listed)
        self.check(len(planned) == 3, "three files planned", len(planned))
        after = self.store_files(self.moved)
        self.check(
            before == after and len(after) == 3,
            "the dry run to delete nothing",
            [p.name for p in after],
        )
        result = self.command("store", "retire", self.moved, "--reason", reason)
        self.show_lines(result.stdout, "matched:", "files deleted:")
        deleted = self.show_lines(result.stdout, listed)
        self.show_lines(result.stdout, ">> retired")
        self.check(len(deleted) == 3, "three files deleted", len(deleted))
        left = self.store_files(self.moved)
        self.say(f"  left: {[p.name for p in left] or 'no store file'}")
        self.check(left == [], "the store's files gone", [p.name for p in left])
        self.check(self.sidecar(self.moved).is_file(), "the sidecar kept", "no sidecar")
        result = self.command("store", "show", self.moved)
        self.show_lines(result.stdout, "state:", "completed:", "problems:")
        self.check(
            "state:     retired" in result.stdout, "the tombstone retired", "another"
        )

    def step_10(self):
        """a run begun in a linked worktree, recorded under the main checkout"""
        import runregistrykit

        self.git(
            "worktree", "add", "-q", "--detach", str(self.worktree), cwd=self.client
        )
        self.say(f"  git worktree add --detach {self.worktree.name}")
        run = runregistrykit.begin(
            "smoke",
            "10",
            "worktree",
            "a smoke run launched from a linked worktree",
            script=str(self.worktree / "job.py"),
        )
        run.finish("done", exit_code=0)
        self.say(f"  begin(): {run.id}")
        self.say(f"    > run directory: {run.path}")
        self.check(
            Path(run.path).resolve().parent == self.runs.resolve(),
            f"the run under the main checkout's {self.runs}",
            run.path,
        )
        self.check(
            not (self.worktree / "var").exists(),
            "no var/ in the worktree",
            "a var/ in the worktree",
        )
        manifest = json.loads(Path(run.manifest_path).read_text())
        self.say(f"    > manifest script: {manifest.get('script')}")
        status = json.loads(Path(run.status_path).read_text())
        self.check(status.get("state") == "done", "state done", status.get("state"))

    def step_11(self):
        """the refusals: no fingerprinter named, and no config at all"""
        result = self.command(
            "store", "show", self.primary, cwd=self.no_fingerprinter, expect=1
        )
        self.show_lines(result.stderr, "!!")
        self.check(
            "fingerprinter" in result.stderr,
            "a refusal naming the fingerprinter",
            result.stderr.strip(),
        )
        above = [
            str(d / "runregistrykit.toml")
            for d in [self.elsewhere, *self.elsewhere.parents]
            if (d / "runregistrykit.toml").exists()
        ]
        self.check(not above, "no runregistrykit.toml above the directory", above)
        result = self.command("list", cwd=self.elsewhere, expect=1)
        self.show_lines(result.stderr, "!!")
        self.check(
            "No runregistrykit.toml" in result.stderr,
            "'No runregistrykit.toml'",
            result.stderr.strip(),
        )


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

    print(f"python          {platform.python_version()} ({sys.executable})")
    print(f"runregistrykit  {_version('runregistrykit')} ({runregistrykit.__file__})")
    for name in ("datastorekit", "ray", "sqlalchemy"):
        print(f"{name:15} {_version(name)}")

    base = Path(tempfile.mkdtemp(prefix="store-smoke-")).resolve()
    print(f"directory       $SMOKE = {base}")
    print()

    start = time.monotonic()
    smoke = Smoke(base)
    try:
        smoke.build_root()
    except Exception as e:
        print(f"CANNOT START: the client root could not be built: {e}", file=sys.stderr)
        return 2

    os.chdir(smoke.client)
    failed = []
    for number, step in enumerate(STEPS, start=1):
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
    os.chdir(base)
    elapsed = time.monotonic() - start

    print()
    ray = sys.modules.get("ray")
    if ray is None:
        print("ray: not imported")
    else:
        initialised = ray.is_initialized()
        print(f"ray: imported, initialised: {initialised}")
        if initialised:
            failed.append("ray")
    for source, digest in smoke.digests:
        print(f"digest ({source}): {digest}")
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
