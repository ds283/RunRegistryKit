# Prompt 04a — the client fingerprinter

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 03 has landed (`035e4b5`) and been reviewed (`f9e0e60`, the board's §1). `git diff --stat f9e0e60
  HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` is empty.
- U6, U7 and U8 are taken (README §6.2, 2026-10-14), as recommended.
- The suite is `Ran 135 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[00-the-fingerprint-reads-a-clients-registry]`,
`[00-the-store-layer-reads-inside-a-fingerprint]`, `[02-the-sidecar-readers-guards-are-unpinned]`.
**Opens:** only what the work finds. **Narrows:** `[02-the-ported-tests-name-sgk]` (this prompt's
port adds its own lines to it).

**Recommended model:** **Opus**. It changes the one place the package touches a store's content,
deletes code that today computes every fingerprint, and adds the module 07's checklists cite. The
port is SGK's largest test module but one, onto a store that does not exist yet.

**Read first:**

1. [`README.md`](README.md): §0.1, §0.2 (C6, C7, the couplings the brief does not list, layer C,
   the tests, DatastoreKit `v0.4.0`), §1, §4, §5 (all of it; rules 6, 7, 9, 10 and 11 especially),
   §6.1 (D3, D4) and §6.2 (U6, U7, U8).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §1's review of 03, and §3's issues, the
   three this prompt closes above all.
3. [`logs/03-the-root-and-the-client-config.md`](logs/03-the-root-and-the-client-config.md),
   "State handed to the next prompt".
4. `runregistrykit/stores.py`: the module docstring (`:1-116`), `:189-203`, `:412-432`, `:573-600`,
   `:1180-1587`; `runregistrykit/__main__.py:136-183, 270-345`; `runregistrykit/__init__.py:383-445`;
   `runregistrykit/client.py` in full; `runregistrykit/tests/client_fixtures.py` in full.
5. DatastoreKit `v0.4.0`'s `datastorekit/store_fingerprint.py` and `store_inventory.py`
   (`:179-500`, `:916-1045`), in the venv.
6. SGK's `RunRegistry/tests/test_store_fingerprint.py` and `StoreFixtures/real_store_fixtures.py` at
   `a45aefc`, through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show a45aefc:<path>` only.
7. `PROVENANCE.md`; `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers below are the package's at `f9e0e60` (its package files are `035e4b5`'s), and SGK's at
`a45aefc` where marked "SGK".

**04 is split** (README §2's allowance): **04a**, this prompt, the fingerprinter, the reader, the
neutral store and `test_store_fingerprint`'s 29 tests; **04b**, written after 04a lands, the 51
retire tests on the neutral store 04a builds.

---

## 1. What is wanted

The package stops computing fingerprints. A client names a **fingerprinter** in its
`runregistrykit.toml` (`[stores] fingerprinter = "module:attribute"`); the package imports it when
it needs a fingerprint taken, compared, described or listed, and otherwise treats a fingerprint as
opaque apart from the fields U7 names. Layer C and `FINGERPRINT_FORMAT` are deleted. The package
ships the protocol and a ready-made **`DatastoreKitFingerprinter(factories, fingerprint_format)`**
over DatastoreKit's functions, which a client instantiates in a module of its own (U6). The
sidecar reader stops requiring `classes` and never requires `encoding_format` (U7). A **neutral
store** of the package's own, on public `datastorekit` names only (U8), replaces SGK's
`real_store_fixtures`, and SGK's `test_store_fingerprint` is ported onto it: 27 tests and
`TestFormats`' 2, each keeping its module, class and method name and what it asserts, but for
§2.8's classes. `fingerprint_store`'s discipline (its order, its refusals, what it writes) is kept
exactly.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit`
`v0.4.0` (`c8570e8`), `runregistrykit` editable, `git` 2.56.0. **Install nothing.**

### 2.2 The protocol and the shipped fingerprinter (U6)

A new module, **`runregistrykit/fingerprint.py`**, standard library only at module scope (it
imports `datastorekit` inside methods, so that `import runregistrykit.fingerprint` loads none of
`ray`, `sqlalchemy` or `datastorekit`):

```python
@runtime_checkable
class Fingerprinter(Protocol):
    def take(self, primary: Path, taken: dict) -> Tuple[dict, Any]: ...
    def compare(self, recorded: dict, current: dict) -> List[dict]: ...
    def describe(self, fingerprint: dict) -> List[str]: ...
    def listing(self, inventory: Any, fingerprint: dict) -> Iterable[str]: ...
```

- **`take(primary, taken)`** reads the **closed** store `primary` read-only, with no Ray, and
  returns `(fingerprint, inventory)`: the fingerprint, a JSON object holding at least an integer
  `fingerprint_format`, a 64-hex `digest` and `taken` as given; and whatever `listing` needs,
  opaque to the package. A refusal of the read **comes through unwrapped**: its own type and text
  (04b's `--without-fingerprint` test records `str(e)` and `type(e).__name__` and compares them with
  the reader's).
- **`compare(recorded, current)`** returns a list of entries, each a dict with at least `kind` (a
  string) and `text` (one line a person reads); empty when the two describe the same content.
- **`describe(fingerprint)`** returns the lines `store fingerprint` prints after the package's own
  `digest:` and `format:` lines.
- **`listing(inventory, fingerprint)`** yields the lines of a listing file, without newlines.

**`DatastoreKitFingerprinter(factories, fingerprint_format)`**, in the same module, implements it:
- the constructor keeps `factories` (any mapping `read_inventory` accepts: SGK's holds classes,
  CPBH's and SI's instances) and refuses a `fingerprint_format` that is a `bool`, not an `int`, or
  below 1, with DatastoreKit's own `TypeError` / `ValueError` wording or its own;
- `take`: `read_inventory(primary, factories)`, then `fingerprint_of(inventory, fingerprint_format,
  taken)`;
- `compare`: `compare_fingerprints`;
- `describe`: the text `__main__._print_fingerprint` prints today from `classes:` on (`:277-294`),
  moved verbatim, its `main.py --inventory` line included (that is
  `[00-package-prose-names-sgk]`'s, for 05);
- `listing`: `listing_lines`.

**Loading it.** `load_fingerprinter(client)` in the same module, given a `ClientRoot`:
- reads `client.stores["fingerprinter"]`; absent is a `ConfigError` naming the config file and
  saying what to add (D4: no degraded mode);
- puts `client.found` (the tree that is running, 03's §2.4) at `sys.path[0]` if it is not on
  `sys.path`, and leaves it there, as a script run from the root has it;
- imports the module and resolves the attribute (a dotted attribute path is allowed);
- refuses, as a `ConfigError` naming the config file and the spec, an import that fails (with the
  exception's type and text), a missing attribute, or an object that is not a `Fingerprinter`
  (`isinstance` against the runtime-checkable protocol).

### 2.3 The config key

`client.py`'s `[stores]` table holds one key, **`fingerprinter`**: a string `"module:attribute"`,
a non-empty dotted module path, one colon, a non-empty dotted attribute path, no whitespace. Any
other `[stores]` key, or a `fingerprinter` of another type or form, is a `ConfigError` naming the
file, the key and the value, at read time. The key is optional **for the core**: `begin()`, `Run`,
`list_runs` and `list` need none. The module docstring documents it, where 03 documented the rest.

### 2.4 The store layer requires one (D4)

Every **store operation** refuses, with the `ConfigError` of §2.2 and before anything is read,
written or deleted, when the client's config names no fingerprinter: `create_sidecar`,
`adopt_sidecar`, `copy_store`, `move_store`, `fingerprint_store`, `retire_store`, `amend_sidecar`,
`write_listing`, and every `store` command of the CLI, `store show` included. The check reads the
config only; **it does not import the fingerprinter**. The fingerprinter is imported only by what
takes, compares, describes or lists a fingerprint: `fingerprint_store`, `write_listing`, and the
CLI's `store fingerprint`. So `store show` still loads neither `ray` nor `sqlalchemy`
(SGK's `test_read_only_then_write_then_matches` asserts it).

`read_sidecar` and `runs_naming` are readers the core also calls (`begin(results=…)`) and need no
fingerprinter. `Run.finish(…, fingerprint=True)` with none configured records the `ConfigError` as
its `fingerprint_error`, as it records any other: a finish never raises for a fingerprint's sake.
`retire_store --without-fingerprint` with none configured is refused by this check, never recorded
as a "without" condition.

### 2.5 Layer C and the format deleted (C6, C7)

- **`stores.py:1180-1427`** goes: the section comment, `_sha256_lines`, `_tag_sets`,
  `fingerprint_of`, `_tags_text`, `_difference`, `_presence`, `compare_fingerprints`,
  `listing_lines`. So does **`FINGERPRINT_FORMAT`** with its history comment (`:189-202`); SGK's
  format history stays in SGK (README §1), and `PROVENANCE.md` says where it was. `TAKEN_KEYS`
  (`:203`) stays: the package builds `taken`. Imports left unused (`hashlib`, `Counter`) go.
- **`fingerprint_store`** (`:1473-1586`) keeps steps 1, 5 and 6 and their texts exactly. Steps 2-4
  become: `load_fingerprinter(client)` (after step 1's refusals, as the import is now); `taken`
  built as now (`when`, `git_head`, `git_dirty`, `run_id`, provenance from the working directory);
  `fingerprint, inventory = fingerprinter.take(primary, taken)`. Step 5 compares with
  `fingerprinter.compare`. The package's own `malformed` entry (`:1550-1559`) is built by a small
  private helper of `fingerprint_store`'s, with the same six keys and text as now. The return
  value's keys are unchanged; `inventory` is the fingerprinter's, opaque.
- **`write_listing(inventory, fingerprint, path, primary, *, client_root=None)`** checks the path
  as now (`check_listing_path`, unchanged), then writes `fingerprinter.listing(…)`'s lines.
- **`__main__._print_fingerprint`** prints `digest:` and `format:` as now (`:275-276`) and then the
  fingerprinter's `describe` lines; `_fingerprint` passes it the fingerprinter it loads.
- `retire_store` and `Run._fingerprint_results` are unchanged but for what §2.4 says: they reach the
  fingerprinter only through `fingerprint_store`.
- **The module docstring** (`:32-35`, `:106-116`) says what is now true: the fingerprint is the
  client fingerprinter's, opaque but for U7's fields; nothing else in it changes (05's).

### 2.6 What the package reads of a fingerprint (U7)

Exactly: `fingerprint_format`, `encoding_format` (when present), `digest`, `taken` (which it
builds), and each comparison entry's `kind` and `text`. Measured at `f9e0e60`, the readers that go
further are `_fingerprint_problems` (`classes`), `fingerprint_store` (layer C's `_difference`) and
`_print_fingerprint` (`classes`, `tag_sets`, `problems`); after this prompt, none does.

**The sidecar reader's shape check** (`_fingerprint_problems`, `:412-432`) becomes: a JSON object;
an integer `fingerprint_format` (not a `bool`); a 64-hex lowercase `digest`; an object `taken`; and,
**if present**, an integer `encoding_format` (not a `bool`). It does not require `encoding_format`,
so every SGK tombstone and every fingerprint written before this prompt reads as it did, and it no
longer requires `classes`. Its problem texts keep the form `fingerprint's <key> … is not …`.

**The pins first.** Before `_fingerprint_problems` changes, add the reader tests
`[02-the-sidecar-readers-guards-are-unpinned]` asks for: a sidecar whose `sidecar_format` is `true`,
and one whose `store_id` is 32 hex characters followed by others, each read as a problem
(`_registry_problems`, `:578`, `:588`). Each must fail under its mutation (§3.6).

### 2.7 The neutral store (U8)

A new module, **`runregistrykit/tests/neutral_store.py`**, on **public `datastorekit` names only**:
`SQLAFactoryBase`, `InventorySpec`, `Parent` (and `ParentSet` if used), the `TAG_*` and `VERSION_*`
names of `datastorekit.contract`, `build_schema`, `shard_file_name`, `read_inventory`; no private
`ShardedPool` attribute or method, no `bare_pool`, no Ray. Shards are written with SQLAlchemy
(`build_schema(MetaData(), FACTORIES)`, `create_all`, inserts); the primary with `sqlite3`, holding
DatastoreKit's `shards (serial, filename)` and `replicated_tables (serial, "table")`, which is what
`read_inventory` and `ShardedPool`'s static `copy_store`, `move_store`, `closed_store_files` and
`delete_store` read (measured; the constructor cannot reopen such a store, and no test of 04a or
04b needs it to). It exports:

- `FACTORIES`, the neutral registry, and `NEUTRAL_FORMAT = 1`;
- **`FINGERPRINTER = DatastoreKitFingerprinter(FACTORIES, NEUTRAL_FORMAT)`**, the fixture's
  fingerprinter (`runregistrykit.tests.neutral_store:FINGERPRINTER`);
- the names `test_store_fingerprint` imports from SGK's fixture, with the signatures it uses:
  `FIXED_TIMESTAMP`; `_schema_tables()`; `build_full_store(directory, stem="full-store", shards=2,
  replicated=None, sharded=None, shard_keys=None, extra_sql=None)`, returning an object with
  `primary`; `file_state(directory)`; `full_rows()`; `relabel_serials(replicated, sharded,
  shard_keys, offset=100)`;
- `COMPUTE_TARGETS`, `SOLVER_COLUMNS` and the class names the ported test needs (§2.8).

**Its content** is designed so that every count, tag set and text SGK's assertions name holds with
only class and table names changed. It must have (SGK's names in brackets, the neutral ones the
agent's, recorded in the log's mapping table):
- a replicated `store_tag` whose serial 3 is `unused-tag`, and the labels `Run_fixture` and
  `grid-A` (tag labels are the fixture's, not a client's; they stay);
- a sharded, **tagged** class [`QuadSourceIntegral`, `QSI`] of 3 rows, its serial 3 on shard 1,
  tagged through `<class>_tags (timestamp, parent_serial, tag_serial)`; its tag sets
  `[Run_fixture]` ×2 (serial 3 among them) and `[Run_fixture, grid-A]` ×1;
- a sharded class [`TkNumericIntegration`, `TKN`] with a `validated` column, its serial 3 on
  shard 0 not validated, and a value table [`TkNumericValue`] whose serial 24 is on shard 1 and
  belongs to one of its rows;
- classes with a `label` column outside their identity [`COMPUTE_TARGETS`, and `BackgroundModel`],
  a solver-serial column outside identity [`SOLVER_COLUMNS`], and a `timestamp` on every row,
  outside identity; `inventory[QSI].earliest_timestamp` the fixture's timestamp;
- at least one `Parent` relation, and rows on shards 0 and 1 only, so that `shards=3` (the ported
  test) and `shards=4` (04b's retire tests) put nothing on the others;
- no problem in the baseline (`fingerprint["problems"] == {}`).

It must also serve 04b: the retire tests (SGK `test_store_retire.py`) delete `QSI` serial 3 on
shard 1, insert a `{QSI}_tags` row with `parent_serial` 999 and `tag_serial` 3, build with
`shards=4` and expect 5 files. 04a does not port them, but builds nothing they cannot use.

### 2.8 The port, and the changes allowed

`runregistrykit/tests/test_store_fingerprint.py`, from SGK's at `a45aefc`, **less** `TestGolden` (3)
and `TestDrivers` (1), which stay in SGK. 29 tests: `TestPhysical` 2, `TestLocalised` 5,
`TestNotContent` 2, `TestListing` 2, `TestFormats` 2, `TestSidecarField` 4,
`TestFingerprintCommand` 3, `TestRunningRefusal` 2, `TestFinish` 7. README §5 rule 9 holds; the
classes of change, each instance listed in the log:

- **D-name**, as 02: `\bRunRegistry\b` → `runregistrykit`.
- **X-drop**: `TestGolden`, `TestDrivers`, and what only they use: `GOLDEN`, `DRIVERS`, `REPO_ROOT`,
  `_HANDLERS`, `_finish_calls`, `import ast`, and the module docstring's items 4 and 12 (the rest
  of it renumbered or not, the agent's choice, logged).
- **N-fix, the imports**: `StoreFixtures.real_store_fixtures` → `runregistrykit.tests.neutral_store`;
  `from config.datastore import factories as _factories` → the neutral `FACTORIES` under the same
  name; `from runregistrykit.stores import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_of`
  replaced by **module-level shims of the same names**, so that no test body changes for them:
  `FINGERPRINT_FORMAT = NEUTRAL_FORMAT`; `fingerprint_of(inventory, taken=None)` calling
  DatastoreKit's `fingerprint_of(inventory, NEUTRAL_FORMAT, taken)`; `compare_fingerprints =
  FINGERPRINTER.compare`.
- **N-class**: an SGK class or table name in a constant or a string literal → the neutral store's
  (`QSI`, `TKN`, `COMPUTE_TARGETS`, `SOLVER_COLUMNS`, `"BackgroundModel"`, `"TkNumericValue"` in an
  `extra_sql` literal). **Method and class names do not change** (rule 9), so
  `test_deleting_one_quadsourceintegral_row` keeps its name; it is recorded under
  `[02-the-ported-tests-name-sgk]`, with the docstrings that cite SGK's campaigns.
- **F-client, the class fixture**: `_FullStores.setUpClass` (a plain `TestCase`, SGK `:142`) makes
  a client root with the shared helper (a class-level variant of it, `addClassCleanup` for the
  directory and the `os.chdir`), because `stores.write_listing` now locates one. The shared
  helper's default config gains `[stores] fingerprinter =
  "runregistrykit.tests.neutral_store:FINGERPRINTER"`, so every 02 and 03 test's client root has
  one; a test that needs an empty config writes its own.
- **U7, two variants**: `"no classes"` and `"classes a list"` are removed from
  `TestSidecarField.test_each_malformed_fingerprint_is_a_problem`'s table (SGK `:504-505`), the one
  exception to rule 9 this prompt allows: they assert the check U7 removes on purpose. Every other
  variant stays.
- **D-fmt**: `black`.

No other line changes. A ported test that fails with only these changes is a **stop** (§5), and so
is one that would need a change outside them. Verify the port as 02 did, outside the repository: a
scratch script applies D-name, X-drop, N-fix and N-class to SGK's file and `black`s it; its output
and the committed file differ only by the shim lines, the F-client lines and the two variants. The
log gives the script's diff summary.

### 2.9 The new tests

In `runregistrykit/tests/test_fingerprinter.py`, every directory a `tempfile` one, at least:
- **The protocol and the loader**: the shipped fingerprinter is a `Fingerprinter`; the loader
  resolves `module:attribute` and a dotted attribute; a fingerprinter module that lies **inside the
  client root** (not otherwise on `sys.path`) is found when the call runs from a subdirectory of
  the root; each refusal of §2.2 and §2.3 is a `ConfigError` naming the file; the constructor's
  refusals of a bad format.
- **D4**: each store operation of §2.4, and a `store` command, with a config that names no
  fingerprinter, is refused with that `ConfigError` and writes nothing; `begin(results=…)` and
  `read_sidecar` are not refused; `finish(…, fingerprint=True)` records the `ConfigError`.
- **Opacity**: a sidecar fingerprint holding only `fingerprint_format`, `digest` and `taken` reads
  as no problem; one with `encoding_format` a string or `true` is a problem; one without
  `encoding_format` (every SGK fingerprint) is not.
- **Through the fingerprinter**: `fingerprint_store` writes the fingerprinter's fingerprint, and a
  recorded fingerprint without `encoding_format` compared with a fresh one gives the
  fingerprinter's `encoding` entry (`store fingerprint` exits 1 and prints its text); a read refusal
  (a journal beside a shard) comes out of `fingerprint_store` as the reader's own exception type.
- **The neutral store**: it builds from public names only (an `ast` walk of `neutral_store.py`:
  every `datastorekit` name it imports is public, no attribute access on a name starting `_` of a
  `datastorekit` object); `ShardedPool.closed_store_files` and `delete_store` work on it with
  `shards=4`, giving 5 files.
- **The 02 guards**: §2.6's two pins.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root: **`Ran 135
   + 29 + N tests … OK`**, N §2.9's. 135 before. Count by loader and give the per-module counts and
   the time.
2. **Nothing outside temporary directories**: `git status --short --ignored` the same before and
   after a run (but `__pycache__/`); no `var/`; `git worktree list` this checkout alone; no Ray
   process before or after; `ray.is_initialized()` never true (the CLI children report it).
3. **The import.** From an empty scratch directory, `env -u PYTHONPATH ./venv/bin/python -I -c
   "import runregistrykit, runregistrykit.stores, runregistrykit.fingerprint, sys; assert not
   {'ray', 'sqlalchemy', 'datastorekit'} & set(sys.modules)"` exits 0. `test_package_imports`'s
   `MODULES` gains `fingerprint.py` (the one change to that file).
4. `grep -rn "FINGERPRINT_FORMAT\|_sha256_lines\|_tag_sets\|def fingerprint_of\|def
   compare_fingerprints\|def listing_lines\|config.datastore" runregistrykit --include=*.py` finds
   only the test module's shim and `neutral_store.py`'s own names, each listed in the log.
5. **The port**, §2.8's script: its diff from the committed file, summarised by class.
6. **The tests catch behaviour** (README §5 rule 10). Each applied, the suite run, reverted, and
   recorded as a diff with the tests that fail:
   - (m1) `_fingerprint_problems` requiring `classes` again;
   - (m2) `_fingerprint_problems` requiring `encoding_format`;
   - (m3) `store show` loading the fingerprinter;
   - (m4) `create_sidecar` without §2.4's check;
   - (m5) `DatastoreKitFingerprinter.take` wrapping the reader's exception in a `RuntimeError`;
   - (m6) the loader not putting `client.found` on `sys.path`;
   - (m7) `DatastoreKitFingerprinter.compare` ignoring `encoding_format` (comparing copies of the
     two with it removed);
   - (m8) `_registry_problems` without its `bool` guard on `sidecar_format`;
   - (m9) `_STORE_ID.fullmatch` → `.match` on `store_id`;
   - (m10) the agent's own, of `fingerprint_store`'s order: the fingerprinter loaded before the
     running-run refusal, or another named in the log.
   Each must fail at least one test. A mutation no test catches is a **stop**.
7. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` gains exactly `fingerprint.py`,
   `tests/neutral_store.py`, `tests/test_store_fingerprint.py` and `tests/test_fingerprinter.py`.
2. §3.1–§3.7 hold.
3. **The records**, in the same commit:
   - the log, `logs/04a-the-client-fingerprinter.md`, per README §5.1: the mapping table of SGK's
     names to the neutral store's; every D-name, X-drop, N-fix, N-class, F-client and U7 instance
     accounted for; the port script's summary; the suite before (135) and after; every mutation as
     a diff;
   - this board: the header, §1's row for 04a, §1.1's F1, F2 and T2a, §3 and §4 (the three issues
     closed, each with what resolved it and the tests that pin it; the others' package lines at
     this commit; `[02-the-ported-tests-name-sgk]` gaining the port's lines);
   - `docs/OPEN_ISSUES.md`: the three rows deleted (7 → 4), the count, the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `PROVENANCE.md`: "Since the import" gains 04a's section: the fingerprinter and its key, layer
     C and `FINGERPRINT_FORMAT` deleted (SGK's at `a45aefc` `stores.py:1152-1399` and `:194-206`;
     DatastoreKit's since `v0.4.0`), U7, the neutral store; and the file map's rows for
     `test_store_fingerprint.py` and `real_store_fixtures.py` say "ported by 04a" and "replaced by
     `neutral_store.py`, 04a".

---

## 5. Stop conditions — stop and ask the user

- A ported test fails with only §2.8's changes, or would need a change outside its classes.
- The neutral store would need a private `datastorekit` name, Ray, or a `ShardedPool` constructed.
- A mutation of §3.6 is caught by no test.
- Any record would change form beyond the fingerprint's own content (DatastoreKit's
  `encoding_format` is the one addition, README §1): a manifest, `status.json`, `checkpoint.jsonl`
  or sidecar field added, removed or renamed, or the tombstone's `fingerprint` condition changed.
- DatastoreKit's functions behave otherwise than §2.2 assumes (README §5 rule 11: record it, do not
  work around it).
- The suite needs a Ray cluster, starts Ray, imports a client, writes outside a `tempfile`
  directory, or leaves a worktree registered here.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `runregistrykit/stores.py`, `__main__.py`, `client.py`; new `fingerprint.py`;
  - `runregistrykit/tests/`: `client_fixtures.py` (the default config), `test_package_imports.py`
    (`MODULES`), and any 03 test whose empty config §2.8's F-client moves (listed); new
    `neutral_store.py`, `test_store_fingerprint.py`, `test_fingerprinter.py`;
  - `PROVENANCE.md`; the log, this board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It ports none of `test_store_retire.py` or `test_store_retire_references.py` (04b), and changes
  `retire_store` only as §2.4 says.
- It changes no prose but what its own changes need (05), names no client in the package, and
  writes no `README.md` usage (06). The `main.py --inventory` line moves with `describe`, unchanged.
- It changes `pyproject.toml` not at all (`[stores]` already holds `datastorekit`), adds no CI and
  makes no tag.

---

## 7. The log and the board

`logs/04a-the-client-fingerprinter.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 04a, §1.1's F1, F2 and T2a, §3 and §4 as §4.3.

---

## At writing (2026-10-14, at `f9e0e60`)

Measured read-only, for the README's row and the orchestrator:
- **SGK's three 04 modules** (through `git show a45aefc`): `test_store_fingerprint` 33 tests, of
  which `TestGolden` 3 and `TestDrivers` 1 stay; `test_store_retire` 41 and
  `test_store_retire_references` 10, every one through `RetireTestCase.a_full_store`, which calls
  `fingerprint_store(write=True)` at set-up (04b). No SGK test calls `listing_lines`, `_difference`
  or `_SHARDS_TABLE_UNREADABLE`; `test_store_fingerprint` calls `stores._fingerprint_problems` only
  in `TestGolden`. About 85 SGK names across the three, 70 of them in `test_store_fingerprint`.
- **SGK's `real_store_fixtures`** (1350 lines) writes its primaries through `bare_pool` and
  `_create_engine`, `_write_shard_data`, `_engine`, `_shard_key_table`; its full store has 13
  replicated and 15 sharded tables, two shards by default.
- **DatastoreKit `v0.4.0`**: `fingerprint_of(inventory, fingerprint_format, taken=None)` (the
  format required, validated), six keys, `encoding_format` outside the digest;
  `compare_fingerprints` gates on both versions, a fingerprint without `encoding_format` giving one
  `encoding` entry; `listing_lines`' header gains `encoding_format` as its sixth word, so SGK's
  listing parser (words 2 and 4) still reads it; the format-mismatch text holds "Recompute both".
  Its comparison loops, texts, `classes` and `problems` are layer C's, by diff and by running both
  on one inventory at format 6.
- **A neutral probe** (the orchestrator's scratchpad, 202 lines, its store part about 120): six
  factories, three shards, a primary of `shards` and `replicated_tables` written with `sqlite3`,
  public names only. `read_inventory`, all three functions and `ShardedPool`'s four static methods
  worked on it; about 18 ms a store, Ray never initialised.
- **The clients**: SGK's `config/datastore.py:91-131` maps 38 names to factory **classes**; CPBH's
  `config/datastore.py:101-129` 27 to **instances**; SI's registry is the private `_factories` of
  `Datastore/SQL/Datastore.py:96`, and SI has no `inventory_spec`. Each client has a top-level
  `config` package, so a fingerprinter at `config.fingerprint:fingerprinter` resolves inside the
  client, and the package must never ship a top-level `config`. Importing each registry loads the
  `ray` module without initialising it. SGK calls the names this prompt deletes from five scripts
  and one test (`ObjectFactories/tests/test_quadsource_policy_key.py:411` imports `fingerprint_of`;
  `FINGERPRINT_FORMAT` in three `docs/` scripts), for 07's checklist.
