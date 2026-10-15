"""A neutral store: a small, closed, fingerprintable ShardedPool store of this package's own, on
public `datastorekit` names only, for the tests of the store layer. No Ray, no pool, no client.

Not a test module (no ``test_`` prefix); the test modules import it, and the client root every test
builds names its ``FINGERPRINTER`` (`client_fixtures.DEFAULT_CONFIG`).

**The registry** (`FACTORIES`) holds nine classes, each a `SQLAFactoryBase` whose `register()`
declares its table and whose `inventory_spec()` declares its identity:

- replicated: `version` and `store_tag` (the tables `datastorekit.contract` names), whose labels
  are their identity; ``mode``, the shard key, whose identity is its ``k``; and ``Background``,
  whose identity is its ``omega`` and its version, and whose ``label`` and ``solver_serial`` are
  not;
- sharded: ``Solution``, tagged through ``Solution_tags``, with a validated flag and a value table
  ``SolutionValue``, whose identity is its ``log10_tol``, its mode and its background; and
  ``Integral``, tagged through ``Integral_tags`` ``(timestamp, parent_serial, tag_serial)``, whose
  identity is its ``q`` and its solution. Neither's ``label`` or ``solver_serial`` is identity.

Every row has a ``timestamp``, which is never identity. A reference is a column with a foreign key
to its target's ``serial``, and a reference that is identity is a `Parent` of the spec, so the
identity of a row never holds a serial.

**The content** (`full_rows`). The tags are ``Run_fixture`` (serial 1), ``grid-A`` (2) and
``unused-tag`` (3), which no row carries. Shard 0 holds the solutions of mode 1, serials 1 and 3
(serial 3 not validated), with values 11-13 and 31-32, and the integrals 1 (tagged ``Run_fixture``
and ``grid-A``) and 2 (``Run_fixture``); shard 1 holds the solution of mode 2, serial 2, with values
21-24, and the integral 3 (``Run_fixture``). No other shard holds a sharded row, and the store has
no problem.

**The files.** Each shard is a SQLite file made with SQLAlchemy (`build_schema`, `create_all`,
inserts); the primary is written with `sqlite3`, and holds DatastoreKit's ``shards (serial,
filename)`` and ``replicated_tables (serial, "table")``, which `read_inventory` and `ShardedPool`'s
static `copy_store`, `move_store`, `closed_store_files` and `delete_store` read, and ``shard_keys
(key_serial, shard_id)``, the mode each shard holds, which nothing reads. A `ShardedPool`
constructor cannot reopen such a store, and no test needs it to.
"""

import copy
import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Tuple

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

RowSet = Dict[str, List[Dict[str, object]]]

# the client format of the neutral store's fingerprints
NEUTRAL_FORMAT = 1

FIXED_TIMESTAMP = datetime(2026, 9, 24, 12, 0, 0)

MODE = "mode"
BACKGROUND = "Background"
SOLUTION = "Solution"
SOLUTION_TAGS = "Solution_tags"
SOLUTION_VALUE = "SolutionValue"
INTEGRAL = "Integral"
INTEGRAL_TAGS = "Integral_tags"

# the classes whose rows are computed, and whose labels are not their identity
COMPUTE_TARGETS = (SOLUTION, INTEGRAL)
# the columns naming a solver, which are not identity
SOLVER_COLUMNS = ("solver_serial",)

REPLICATED_TABLES = (VERSION_TABLE, TAG_TABLE, MODE, BACKGROUND)


def _label():
    return sqla.Column("label", sqla.String(64), nullable=True)


def _reference(name, target):
    return sqla.Column(name, sqla.Integer, sqla.ForeignKey(f"{target}.serial"))


def _solver():
    return sqla.Column("solver_serial", sqla.Integer, nullable=True)


class _Factory(SQLAFactoryBase):
    """A factory whose rows this module writes directly: nothing builds an object from them."""

    @staticmethod
    def register():
        raise NotImplementedError

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        raise NotImplementedError(
            "the neutral store's rows are written directly, never built"
        )


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


class ModeFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [sqla.Column("k", sqla.Float, nullable=False)],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(leaves=("k",))


class BackgroundFactory(_Factory):
    @staticmethod
    def register():
        return {
            "version": True,
            "timestamp": True,
            "columns": [
                _label(),
                sqla.Column("omega", sqla.Float, nullable=False),
                _solver(),
            ],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("omega",), parents={"version": Parent("version", of=VERSION_TABLE)}
        )


class SolutionFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [
                _label(),
                _reference("mode_serial", MODE),
                _reference("background_serial", BACKGROUND),
                sqla.Column("log10_tol", sqla.Float, nullable=False),
                _solver(),
                sqla.Column("validated", sqla.Boolean, nullable=True),
            ],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("log10_tol",),
            parents={
                "mode": Parent("mode_serial", of=MODE),
                "background": Parent("background_serial", of=BACKGROUND),
            },
            tags=(SOLUTION_TAGS, "solution_serial"),
            values=(SOLUTION_VALUE, "solution_serial"),
            validated="validated",
        )


class SolutionTagsFactory(_Factory):
    @staticmethod
    def register():
        return {
            "serial": False,
            "timestamp": True,
            "columns": [
                _reference("solution_serial", SOLUTION),
                _reference(TAG_SERIAL, TAG_TABLE),
            ],
        }


class SolutionValueFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [
                _reference("solution_serial", SOLUTION),
                sqla.Column("z", sqla.Float, nullable=False),
                sqla.Column("value", sqla.Float, nullable=False),
            ],
        }


class IntegralFactory(_Factory):
    @staticmethod
    def register():
        return {
            "timestamp": True,
            "columns": [
                _label(),
                _reference("solution_serial", SOLUTION),
                sqla.Column("q", sqla.Float, nullable=False),
                _solver(),
            ],
        }

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("q",),
            parents={"solution": Parent("solution_serial", of=SOLUTION)},
            tags=(INTEGRAL_TAGS, "parent_serial"),
        )


class IntegralTagsFactory(_Factory):
    @staticmethod
    def register():
        return {
            "serial": False,
            "timestamp": True,
            "columns": [
                _reference("parent_serial", INTEGRAL),
                _reference(TAG_SERIAL, TAG_TABLE),
            ],
        }


# the neutral registry, as a client's: class name -> factory
FACTORIES = {
    VERSION_TABLE: VersionFactory,
    TAG_TABLE: TagFactory,
    MODE: ModeFactory,
    BACKGROUND: BackgroundFactory,
    SOLUTION: SolutionFactory,
    SOLUTION_TAGS: SolutionTagsFactory,
    SOLUTION_VALUE: SolutionValueFactory,
    INTEGRAL: IntegralFactory,
    INTEGRAL_TAGS: IntegralTagsFactory,
}

# the fixture's fingerprinter, which every test's client root names
FINGERPRINTER = DatastoreKitFingerprinter(FACTORIES, NEUTRAL_FORMAT)


# ---------------------------------------------------------------------------------------------
# the content
# ---------------------------------------------------------------------------------------------


def _solution(serial, mode, log10_tol, validated) -> dict:
    return {
        "serial": serial,
        "label": f"fixture-solution-{serial}",
        "mode_serial": mode,
        "background_serial": 1,
        "log10_tol": log10_tol,
        "solver_serial": 1,
        "validated": validated,
    }


def _values(solution, serials) -> list:
    return [
        {"serial": s, "solution_serial": solution, "z": float(s % 10), "value": 1.0 / s}
        for s in serials
    ]


def _integral(serial, solution, q) -> dict:
    return {
        "serial": serial,
        "label": f"fixture-integral-{serial}",
        "solution_serial": solution,
        "q": q,
        "solver_serial": 1,
    }


def _tags(column, parent, tags) -> list:
    return [{column: parent, TAG_SERIAL: tag} for tag in tags]


FULL_REPLICATED_ROWS: RowSet = {
    VERSION_TABLE: [{"serial": 1, VERSION_LABEL: "neutral-1"}],
    TAG_TABLE: [
        {"serial": 1, TAG_LABEL: "Run_fixture"},
        {"serial": 2, TAG_LABEL: "grid-A"},
        {"serial": 3, TAG_LABEL: "unused-tag"},
    ],
    MODE: [{"serial": 1, "k": 0.1}, {"serial": 2, "k": 1.0}],
    BACKGROUND: [
        {
            "serial": 1,
            "version": 1,
            "label": "fixture-background",
            "omega": 0.31,
            "solver_serial": 1,
        }
    ],
}

# shard serial -> sharded rows: mode 1 on shard 0, mode 2 on shard 1
FULL_SHARDED_ROWS: Dict[int, RowSet] = {
    0: {
        SOLUTION: [_solution(1, 1, -5.0, True), _solution(3, 1, -7.0, False)],
        SOLUTION_TAGS: _tags("solution_serial", 1, (1,))
        + _tags("solution_serial", 3, (1,)),
        SOLUTION_VALUE: _values(1, (11, 12, 13)) + _values(3, (31, 32)),
        INTEGRAL: [_integral(1, 1, 0.5), _integral(2, 1, 0.25)],
        INTEGRAL_TAGS: _tags("parent_serial", 1, (1, 2))
        + _tags("parent_serial", 2, (1,)),
    },
    1: {
        SOLUTION: [_solution(2, 2, -5.0, True)],
        SOLUTION_TAGS: _tags("solution_serial", 2, (1, 2)),
        SOLUTION_VALUE: _values(2, (21, 22, 23, 24)),
        INTEGRAL: [_integral(3, 2, 0.5)],
        INTEGRAL_TAGS: _tags("parent_serial", 3, (1,)),
    },
}

# mode serial -> shard serial
FULL_SHARD_KEYS: Dict[int, int] = {1: 0, 2: 1}


def full_rows() -> Tuple[RowSet, Dict[int, RowSet], Dict[int, int]]:
    """Fresh copies of the full store's replicated rows, sharded rows and shard keys."""
    return (
        copy.deepcopy(FULL_REPLICATED_ROWS),
        copy.deepcopy(FULL_SHARDED_ROWS),
        dict(FULL_SHARD_KEYS),
    )


# ---------------------------------------------------------------------------------------------
# the writer
# ---------------------------------------------------------------------------------------------

_SCHEMA: Dict[str, object] = {}


def _schema():
    """``(metadata, tables)`` from `build_schema`, built once per process."""
    if "tables" not in _SCHEMA:
        metadata = sqla.MetaData()
        _SCHEMA["metadata"] = metadata
        _SCHEMA["tables"] = build_schema(metadata, FACTORIES).tables
    return _SCHEMA["metadata"], _SCHEMA["tables"]


def _schema_tables() -> Mapping[str, sqla.Table]:
    """The ``build_schema`` tables, built once per process. Read, never created from."""
    return _schema()[1]


def _filled(table: sqla.Table, rows) -> list:
    """``rows`` with every column the table declares: a missing ``timestamp`` is
    `FIXED_TIMESTAMP`, as the datastore fills it with the time, and any other missing column is
    ``None``, so that one insert takes one set of columns. A missing serial is left to SQLite.
    """
    out = []
    for row in rows:
        row = dict(row)
        for column in table.columns:
            if column.name in row or column.primary_key:
                continue
            row[column.name] = FIXED_TIMESTAMP if column.name == "timestamp" else None
        out.append(row)
    return out


def _write_shard(path: Path, row_sets, extra_sql) -> None:
    metadata, tables = _schema()
    engine = sqla.create_engine(f"sqlite:///{path}", future=True)
    try:
        metadata.create_all(engine)
        with engine.begin() as conn:
            for rows in row_sets:
                for name, table_rows in rows.items():
                    if len(table_rows) > 0:
                        conn.execute(
                            sqla.insert(tables[name]),
                            _filled(tables[name], table_rows),
                        )
    finally:
        engine.dispose()

    if len(extra_sql) > 0:
        conn = sqlite3.connect(path)
        try:
            with conn:
                for statement in extra_sql:
                    conn.execute(statement)
        finally:
            conn.close()


def _write_primary(
    primary: Path, shard_files: Mapping[int, Path], shard_keys: Mapping[int, int]
) -> None:
    conn = sqlite3.connect(primary)
    try:
        with conn:
            conn.execute(
                "CREATE TABLE shards (serial INTEGER NOT NULL PRIMARY KEY, "
                "filename VARCHAR NOT NULL)"
            )
            conn.execute(
                'CREATE TABLE replicated_tables (serial INTEGER NOT NULL PRIMARY KEY, "table" '
                "VARCHAR NOT NULL)"
            )
            conn.execute(
                "CREATE TABLE shard_keys (key_serial INTEGER NOT NULL PRIMARY KEY, "
                "shard_id INTEGER NOT NULL REFERENCES shards (serial))"
            )
            conn.executemany(
                "INSERT INTO shards (serial, filename) VALUES (?, ?)",
                [(serial, path.name) for serial, path in sorted(shard_files.items())],
            )
            conn.executemany(
                'INSERT INTO replicated_tables (serial, "table") VALUES (?, ?)',
                list(enumerate(REPLICATED_TABLES)),
            )
            conn.executemany(
                "INSERT INTO shard_keys (key_serial, shard_id) VALUES (?, ?)",
                sorted(shard_keys.items()),
            )
    finally:
        conn.close()


@dataclass(frozen=True)
class NeutralStore:
    """A store built by `build_full_store`: its primary and its shard files, by serial."""

    primary: Path
    shard_files: Dict[int, Path]


def build_full_store(
    directory: Path,
    stem: str = "full-store",
    shards: int = 2,
    replicated: Optional[RowSet] = None,
    sharded: Optional[Dict[int, RowSet]] = None,
    shard_keys: Optional[Mapping[int, int]] = None,
    extra_sql: Optional[Mapping[int, List[str]]] = None,
) -> NeutralStore:
    """
    Build the full store, or one with the rows given, in ``directory`` (which must exist) and
    return it. ``replicated`` rows go into every shard with the same serials; ``sharded[n]`` rows
    into shard ``n`` only; both default to `full_rows`'. ``shard_keys`` (mode serial -> shard)
    goes into the primary, and each must name a shard. ``extra_sql[n]`` lists SQL statements run
    on shard ``n`` last, with `sqlite3`.
    """
    base_replicated, base_sharded, base_keys = full_rows()
    replicated = copy.deepcopy(base_replicated if replicated is None else replicated)
    sharded = copy.deepcopy(base_sharded if sharded is None else sharded)
    shard_keys = dict(base_keys if shard_keys is None else shard_keys)
    extra_sql = {} if extra_sql is None else extra_sql

    if shards < 2:
        raise ValueError("a neutral store has at least two shards")
    unknown = sorted(set(sharded) - set(range(shards)))
    if unknown:
        raise ValueError(f"sharded rows name shards {unknown} that do not exist")
    unknown = sorted({s for s in shard_keys.values() if s not in range(shards)})
    if unknown:
        raise ValueError(f"shard keys name shards {unknown} that do not exist")

    primary = (Path(directory) / f"{stem}.sqlite").resolve()
    shard_files = {
        serial: primary.parent / shard_file_name(primary, serial)
        for serial in range(shards)
    }
    for serial, path in shard_files.items():
        _write_shard(
            path, [replicated, sharded.get(serial, {})], list(extra_sql.get(serial, ()))
        )
    _write_primary(primary, shard_files, shard_keys)
    return NeutralStore(primary=primary, shard_files=shard_files)


def file_state(directory: Path) -> Tuple[List[str], Dict[str, Tuple[str, int, int]]]:
    """The directory listing, and each file's (SHA-256, size, st_mtime_ns)."""
    listing = sorted(p.name for p in Path(directory).iterdir())
    state = {}
    for name in listing:
        path = Path(directory) / name
        st = path.lstat()
        state[name] = (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            st.st_size,
            st.st_mtime_ns,
        )
    return listing, state


# ---------------------------------------------------------------------------------------------
# the same content under other serials
# ---------------------------------------------------------------------------------------------


def references() -> Dict[str, Dict[str, str]]:
    """table -> column -> the table whose serial it holds: the schema's foreign keys."""
    return {
        name: {
            column.name: fk.column.table.name
            for column in table.columns
            for fk in column.foreign_keys
        }
        for name, table in _schema_tables().items()
    }


def relabel_serials(
    replicated: RowSet,
    sharded: Dict[int, RowSet],
    shard_keys: Mapping[int, int],
    offset: int = 100,
) -> Tuple[RowSet, Dict[int, RowSet], Dict[int, int]]:
    """
    The same content under different serials. In every table the serials are reversed in order
    and moved by a per-table offset, and every reference follows them; so do the shard keys.
    Replicated rows get the same new serials on every shard, as `ShardedPool` replicates them.
    """
    replicated = copy.deepcopy(replicated)
    sharded = copy.deepcopy(sharded)
    row_sets = [replicated] + [sharded[n] for n in sorted(sharded)]

    olds: Dict[str, List[int]] = {}
    for rows in row_sets:
        for table, table_rows in rows.items():
            for row in table_rows:
                if "serial" in row:
                    olds.setdefault(table, []).append(row["serial"])

    mapping: Dict[str, Dict[int, int]] = {}
    for index, table in enumerate(sorted(olds)):
        serials = sorted(set(olds[table]))
        base = offset * (index + 1)
        mapping[table] = {
            old: base + len(serials) - position for position, old in enumerate(serials)
        }

    refs = references()
    for rows in row_sets:
        for table, table_rows in rows.items():
            for row in table_rows:
                if "serial" in row:
                    row["serial"] = mapping[table][row["serial"]]
                for column, target in refs.get(table, {}).items():
                    if column in row:
                        row[column] = mapping.get(target, {}).get(
                            row[column], row[column]
                        )

    new_keys = {mapping[MODE].get(key, key): shard for key, shard in shard_keys.items()}
    return replicated, sharded, new_keys
