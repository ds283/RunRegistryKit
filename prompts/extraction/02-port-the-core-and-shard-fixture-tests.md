# Prompt 02 — port the core and shard-fixture tests

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 01 has landed (`4e0d715`) and been reviewed (`bae5597`, the board's §1). `git diff --stat 4e0d715
  HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md` is empty: the package, the check and
  `PROVENANCE.md` are 01's.
- G1 holds on the source side: SGK's `a45aefc` has §2.2's eight blobs (re-checked 2026-10-14 at this
  prompt's writing, with the 25-row tree and SGK's `HEAD` `14bcac0`).
- U4 is taken (README §6.2): the shard fixtures are **carried as they are**.
- `./venv/bin/python docs/extraction/compare_with_source.py` exits 0, and the suite is `Ran 3 tests
  … OK`.
- `git status` is clean in this repository.

**Closes:** nothing. **Opens:** `[02-the-ported-tests-name-sgk]` (§2.7). **Narrows:** four issues'
package lines (§2.7).

**Recommended model:** **Sonnet**. The port is mechanical and every class of difference is fixed
below by rule; the one design question, how the check accepts `black`'s three reflows, is settled
here (§2.4).

**Read first:**

1. [`README.md`](README.md): §0.2 (the tests), §4 (the module map and the equivalence check), §5
   (all of it; rules 6, 8, 9 and 10 especially) and §6.2 (U4).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §1's review of 01, and §3's seven issues.
3. [`logs/01-import-the-registry.md`](logs/01-import-the-registry.md): how the check was built, its
   breakages (a)–(i) as diffs, and "State handed to the next prompt".
4. `docs/extraction/compare_with_source.py` and `PROVENANCE.md` in full: this prompt extends both.
5. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`, "Repository mechanics".
6. In SGK at `a45aefc`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   a45aefc:<path>`**, never from SGK's working tree: the eight files of §2.2.

Line numbers below are SGK's at `a45aefc` unless they say "package".

---

## 1. What is wanted

The 29 core tests and the 76 shard-fixture tests are in `runregistrykit/tests/`, with the two
fixture modules they use, under their SGK names (the shard fixture under `tests/`). They are SGK's
files changed only by three rules: the package's name (D-name, as 01), the shard fixture's import
path (D-fix), and `black` (D-fmt). The check of 01 is extended to prove that, and still proves 01's
files. **The suite is 108**, all passing in `venv/`, and it pins the imported behaviour as it
stands, the couplings C1–C9 included.

**No behaviour changes**, in the package or in a test. A test that cannot keep its assertion is a
stop (README §5 rule 9), never a rewrite. The SGK names the tests carry are recorded as an issue for
05 (§2.7), not changed.

---

## 2. What to change

### 2.1 The venv

Unchanged from 01: Python 3.12.15, `ray==2.43.0`, `SQLAlchemy==2.0.39`, `datastorekit` at `v0.4.0`
(`c8570e8`), `black==25.1.0`, `runregistrykit` installed editable. **Install nothing.** The tests
need `datastorekit` and `ray` installed; Ray is never initialised.

### 2.2 The files

| SGK at `a45aefc` | Blob | Here |
|---|---|---|
| `RunRegistry/tests/test_run_registry.py` (711 lines) | `01c3ea3` | `runregistrykit/tests/test_run_registry.py` |
| `RunRegistry/tests/store_fixtures.py` (223) | `391f31f` | `runregistrykit/tests/store_fixtures.py` |
| `RunRegistry/tests/test_store_sidecar.py` (617) | `533d111` | `runregistrykit/tests/test_store_sidecar.py` |
| `RunRegistry/tests/test_store_copy_move.py` (601) | `4be78d9` | `runregistrykit/tests/test_store_copy_move.py` (610 after D-fmt) |
| `RunRegistry/tests/test_store_command_line.py` (183) | `6f111e2` | `runregistrykit/tests/test_store_command_line.py` |
| `RunRegistry/tests/test_store_amend.py` (641) | `8b7db11` | `runregistrykit/tests/test_store_amend.py` |
| `RunRegistry/tests/test_store_amend_residuals.py` (267) | `0c6e6a2` | `runregistrykit/tests/test_store_amend_residuals.py` |
| `StoreFixtures/shard_store_fixtures.py` (168) | `1375949` | `runregistrykit/tests/shard_store_fixtures.py` (U4) |

The full blobs are in the check's table. The test modules import the package absolutely
(`import RunRegistry`, `from RunRegistry.tests.store_fixtures import …`), which D-name turns into
`runregistrykit`; nothing becomes relative.

### 2.3 The differences allowed, and no others

Each is a substitution applied to a source line; T, the **renamed source**, is the source with
D-name and D-fix applied to every line.

- **D-name — the package's name**, as 01: `\bRunRegistry\b` → `runregistrykit`. It covers the
  imports, `runpy.run_module("RunRegistry", …)` and `sys.argv = ["RunRegistry"] + …`
  (`test_store_command_line.py:30, 33`), `-m RunRegistry` in child processes
  (`test_run_registry.py:681`), the `RunRegistry.<name>` references, and docstrings. **83 lines**:
  `test_run_registry.py` 31, `store_fixtures.py` 6, `test_store_sidecar.py` 15,
  `test_store_copy_move.py` 10, `test_store_command_line.py` 11, `test_store_amend.py` 8,
  `test_store_amend_residuals.py` 2, `shard_store_fixtures.py` 0.
- **D-fix — the shard fixture's new home.** `\bStoreFixtures\.shard_store_fixtures\b` →
  `runregistrykit.tests.shard_store_fixtures`, and `\bStoreFixtures/shard_store_fixtures\.py` →
  `runregistrykit/tests/shard_store_fixtures.py`. **5 lines**: the three imports
  (`store_fixtures.py:20`, `test_store_sidecar.py:28`, `test_store_copy_move.py:32`) and two
  docstrings (`store_fixtures.py:4`, `test_store_amend.py:15`). No line needs both D-name and
  D-fix.
- **D-fmt — `black` 25.1.0**, no configuration, applied to T. D-name lengthens a line by three
  characters, and in `test_store_copy_move.py` three code lines then exceed 88 columns: `:73` (1 line
  → 4, a dict split with a trailing comma `black` adds), `:135` (1 → 5) and `:211` (1 → 3). Package
  lines `:73-76`, `:138-142`, `:218-220`; the file goes from 601 lines to 610. Every other ported
  file, and every 01 file, is unchanged by `black`. **3 source lines, 12 package lines**, all in that
  file.

**Not allowed here:** renaming SGK's tables, stems, campaign citations or test classes (§2.7, 05);
a relative import in place of D-fix's absolute one; any edit to a test's body, name or assertion;
any change to the package's three modules; a neutral store (04).

### 2.4 The check, extended

`docs/extraction/compare_with_source.py` is extended, not rewritten: its constants, its frozen-tree
check, its fates, its walk and its exit codes stay as 01 made them.

- **The table.** The eight rows of §2.2 change fate from *pending, 02* to **ported by 02**, and are
  checked as 01's imported rows are. The three *pending, 04* rows stay pending. `NEW_FILES` is
  unchanged (02 adds no file without a source).
- **The rule, for every checked file, 01's and 02's alike:**
  1. T = the source with D-name and D-fix applied line by line (one line for one line). Count the
     lines D-name changed and the lines D-fix changed.
  2. **The package file must equal `black.format_str(T, mode=black.Mode())` exactly.** The lines
     where the package differs from T (the non-equal `difflib` opcodes between T and the package)
     are D-fmt; count them, and print each hunk with its T and package lines.
  3. If the package differs from `black(T)`, print every differing line (`difflib` between
     `black(T)` and the package, with package line numbers) as UNCLASSIFIED and fail.
  4. **Completeness:** no line of a checked package file matches `\bRunRegistry\b` or
     `\bStoreFixtures\b`; one that does fails, named by file and line.

  This replaces 01's per-pair classification of equal-length `replace` blocks: for 01's files the
  two are the same test (`black(T) == T` there, so the package must equal T, which 01's rule
  required line by line), and the counts printed for them must stay D-name 6, 13, 4, 0 and D-fmt 0.
  It is still a rule, not a list: nothing names a line number.
- **`black` is a dependency of the check, pinned.** The script imports `black` and exits 2
  (cannot run) unless `black.__version__ == "25.1.0"`, saying so. It still imports nothing of SGK
  or of the package.
- **The docstring** states the new rule, D-fix and D-fmt, and why `black` is pinned.

**Show that the check bites.** With the tree otherwise correct, make each change separately, show
that the check exits non-zero and names what is wrong, run the suite, then revert:
- (a) in `test_run_registry.py`, package `:639`, `stale_after=3600.0` → `stale_after=3601.0`: a
  change to a ported test that the suite does not notice;
- (b) the trailing comma `black` added at `test_store_copy_move.py` package `:75` removed (valid
  Python, the same behaviour, not what `black` gives);
- (c) `test_store_copy_move.py`'s fixture import made relative (`from .shard_store_fixtures import
  tree_state`), which behaves the same;
- (d) `store_fixtures.py:4`'s `runregistrykit/tests/shard_store_fixtures.py` reverted to
  `StoreFixtures/shard_store_fixtures.py` (completeness);
- (e) `shard_store_fixtures.py:25`, `KEY_TYPE = "wavenumber"` → `"wavenumbers"`: the suite passes
  (measured), and only the check sees it;
- (f) one test method deleted from `test_store_sidecar.py` (the suite falls to 107);
- (g) one 02 row's fate set back to *pending, 02* in the check's table, the file present (PRESENT,
  NOT CHECKED);
- (h) 01's (a)–(i), replayed from 01's log against the extended check: each must still fail. (h)
  of 01 edits the table; apply it to the table as it now stands.

### 2.5 The tests must catch behaviour

README §5 rule 10. Each mutation below is applied to the package, the suite run, and reverted; the
log records which tests fail:
- (m1) `runregistrykit/__init__.py:119`, `RECORDED_DISTRIBUTIONS = ("datastorekit",)`: fails
  `TestPackageProvenance` (measured: 2 failures, 1 error, including
  `test_the_recorded_names_are_the_two_packages`);
- (m2) `runregistrykit/stores.py:1101`, `_history_entry("copy", …)` → `_history_entry("copied", …)`:
  fails `test_store_copy_move` and `test_store_amend.TestCopyAndMove` (measured: 4 failures, 8
  errors);
- (m3) the agent's own: one mutation of `stores.py`'s sidecar reader or `amend_sidecar` that some
  ported test catches, chosen and named in the log.

Note for the log, not a mutation to make: `DEFAULT_STALE_AFTER = 901.0` (01's (a)) passes the
suite; no ported test pins it. Record it under "Observations not acted on".

### 2.6 `CLAUDE.md` and `PROVENANCE.md`

- **`CLAUDE.md`, "Repository mechanics", the Tests bullet**: the tests *live* in
  `runregistrykit/tests/`, and are run from the repository root with
  `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`; they need `datastorekit`
  and `ray` installed (never initialised), and the checkout to be a git work tree (two tests read
  the checkout's commit, §2.7). Change that bullet only.
- **`PROVENANCE.md`**: the eight rows' fate "ported by 02"; D-fix and D-fmt beside D-name in "The
  differences allowed", with D-fmt's three reflows; the check's rule as §2.4; and that the check now
  needs `black` 25.1.0. Nothing else in it changes.

### 2.7 The board's issues

**Opened: `[02-the-ported-tests-name-sgk]`**, owner 05. The ported tests and fixtures carry SGK's
names, besides the `RunRegistry` and `StoreFixtures` that D-name and D-fix handle. Measured at
writing in the eight files (the agent re-measures and lists every line in the log): SGK's table and
key type in the shard fixture (`SHARDED = {"GkSource": "k"}`, `KEY_TYPE = "wavenumber"`,
`REPLICATED`, `:25-27`); SGK's store stems (`handover-A3-baseline-lambdacdm`,
`handover-atol-sweep`: `store_fixtures.py:38`, `test_store_sidecar.py:43`); an SGK driver path
(`docs/gktk-remedial/scoped_pipeline_run.py`, `store_fixtures.py:50`); a test class named for SGK's
A3 store (`test_store_amend.TestLiveA3Shape`, `:203`); and docstrings citing SGK's campaigns and
prompts (about 30 lines across all eight files). *Impact:* the package's tests name a client, which
`CLAUDE.md` forbids, and 05's guard (U10), if it scans `tests/`, fails on them; renaming
`TestLiveA3Shape` touches README §5 rule 9. *Next step:* 05, with its prose rewrite; the class name
is put to the user there.

**Package lines, read in the package**, added to each issue as 01 did:
- `[00-the-root-is-the-packages-parent]`: the child processes that rely on `REPO_ROOT`
  (`test_run_registry.py:179, 226, 684`; `test_store_command_line.py:60-61, 172-173`;
  `test_store_amend.py:636-637`); and the two assertions that `git_head` is 40 characters
  (`test_run_registry.py:273`, `test_store_sidecar.py:288`), which read the checkout's commit
  through C9: from a `git archive` export with no `.git`, both fail (measured).
- `[00-the-recorded-distributions-are-sgks]`: the pinning test is
  `runregistrykit/tests/test_run_registry.py:393-396`
  (`test_the_recorded_names_are_the_two_packages`).
- `[00-the-shard-fixtures-reach-into-shardedpool]`: measured against the carried file.
  `bare_pool` (`shard_store_fixtures.py:30-43`) builds a pool with `object.__new__` and sets 10
  private attributes (`_db_name`, `_primary_file`, `_timeout`, `_ShardKeyType_name`,
  `_replicated_tables`, `_sharded_tables`, `_shard_db_files`, `_shard_records`, `_shard_keys`,
  `_engine`); `read_pool` and `write_new_store` call 3 private methods (`_create_engine`,
  `_read_shard_data`, `_write_shard_data`, `:46-71`); `store_fixtures.assertOpens` (`:158-165`)
  calls `_check_shard_files` and reads `_shard_db_files`. The agent confirms each and gives the
  package lines. The issue stays open, owner none.
- `[00-a-refusal-matches-datastorekit-message-text]`: **no 02 test reaches the match.**
  `_SHARDS_TABLE_UNREADABLE` is used at `stores.py:1818` and `:1863`, in `retire_store`, and SGK's
  only test of it is in `test_store_retire.py` (04). The next step becomes 04's; record that.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root, gives
   **`Ran 108 tests … OK`** (3 before). By module: `test_package_imports` 3, `test_run_registry` 29,
   `test_store_sidecar` 17, `test_store_copy_move` 27, `test_store_command_line` 2,
   `test_store_amend` 21, `test_store_amend_residuals` 9. It takes about 25–40 s. Count the tests by
   loader (not by `-v` lines; some tests print docstrings) and give the per-class counts in the log.
2. `compare_with_source.py` exits 0. Its whole output goes in the log. It should report 25 rows and
   the fixture blob equal; 12 files checked (4 by 01, 8 by 02); D-name 106 (01's 6, 13, 4, 0 and
   02's 31, 6, 15, 10, 11, 8, 2, 0); D-fix 5; D-fmt 12 package lines in 3 hunks, all in
   `test_store_copy_move.py`, and 0 elsewhere; 3 pending (04); 11 not imported and absent; 1
   declared new file. If a count differs, explain it.
3. **The suite writes nothing outside its temporary directories.** `git status --short --ignored`
   is the same before and after a run (but `__pycache__/`), and no `var/` appears at the root.
   No Ray process is up before or after (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'`).
4. **The breakage record.** §2.4's (a)–(h) and §2.5's (m1)–(m3), each a diff exactly as applied,
   with the check's exit and naming and the suite's verdict and failing tests. None is committed.
5. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2.2's eight files exist under their names, and `runregistrykit/` holds nothing else new.
2. §3.1–§3.5 hold.
3. **The records**, in the same commit:
   - the log, `logs/02-port-the-core-and-shard-fixture-tests.md`, per README §5.1, with the check's
     output, the per-class test counts, the 83 D-name, 5 D-fix and 3 D-fmt instances accounted for
     (README §5 rule 9), the suite count before (3) and after (108), and every breakage as a diff;
   - this board: the header, §1's row for 02, §1.1's T1, §2's G1 (the package side for 02's files),
     §3 as §2.7 says (one issue opened, four given package lines);
   - `docs/OPEN_ISSUES.md`: the new issue under 05's rows, the count 8, the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `CLAUDE.md` and `PROVENANCE.md` as §2.6.

---

## 5. Stop conditions — stop and ask the user

- A blob of §2.2 reads differently at `a45aefc`.
- A ported test fails in `venv/` with only §2.3's differences applied (measured at writing: none
  does, in a git work tree). Do not change a test, the package or the fixture to make it pass.
- A ported file differs from `black(T)` in a way §2.3 does not cover, or `black` would change a line
  of 01's files.
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory.
- The suite count is not 108, other than by a test this prompt names.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - the eight files of §2.2;
  - `docs/extraction/compare_with_source.py`;
  - `PROVENANCE.md`; `CLAUDE.md`'s Tests bullet;
  - the log, this board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It changes nothing in `runregistrykit/__init__.py`, `stores.py`, `__main__.py`,
  `tests/__init__.py` or `tests/test_package_imports.py`, nor `pyproject.toml`.
- It ports none of 04's three test modules and builds no neutral store.
- It resolves none of C1–C9, and renames no SGK name in the tests (§2.7: 05).
- It adds no CI, sets no dependency range and makes no tag (06).

---

## 7. The log and the board

`logs/02-port-the-core-and-shard-fixture-tests.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 02, §1.1's T1, §2's G1 and §3 as §2.7.
