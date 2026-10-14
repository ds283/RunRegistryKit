# Prompt 01 — import the registry

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- G1 holds on the source side. SGK's `RunRegistry/` at **`a45aefc`**
  (`a45aefc702de643c330372dd6d2d983f38bb8eed`, "Freeze RunRegistry/ for its move to
  RunRegistryKit"), the **import commit**, has the 25 files and blobs of §2.5's table, which is
  SGK's frozen-tree table (its `prompts/runregistry-extraction/IMPLEMENTATION_STATE.md` §2.1),
  re-checked 2026-10-14 at this prompt's writing.
- U1–U3 are taken (README §6.1, §6.2): the import is **faithful** (U2), and the only release is
  `v0.1.0`, at 06 (U3).
- `git status` is clean in this repository.

**Closes:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus**. The work is small and mechanical, but every later prompt and every
client's adoption stands on it, and the equivalence check (§2.6) must be written so that it would
catch a real difference, not only pass on this one.

**Read first:**

1. [`README.md`](README.md): §0.2, §1, §4 (the module map and the equivalence check), §5 (all of
   it, rule 8 especially) and §6.2 (U2, U3).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md) §3, the seven issues, whose SGK line
   numbers this prompt converts to package lines (§4.3).
3. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`, in particular "What this repository is"
   and "Repository mechanics".
4. In SGK at `a45aefc`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   a45aefc:<path>`**, never from SGK's working tree: `RunRegistry/__init__.py` (710 lines),
   `RunRegistry/stores.py` (2185), `RunRegistry/__main__.py` (515) and `RunRegistry/tests/__init__.py`
   (empty). Skim the test modules only to fill §2.5's fates; 02 ports them.
5. RayPoolKit's `docs/extraction/compare_with_source.py` and `PROVENANCE.md`
   (`/Users/ds283/Documents/Code/RayPoolKit`), the precedent for §2.6 and §2.8. Read them; do not
   copy RayPoolKit's rules, which are for a different source.

Line numbers below are SGK's at `a45aefc`.

---

## 1. What is wanted

The package `runregistrykit` exists in this repository. Its three modules are SGK's at `a45aefc`,
changed only by the package's name (§2.4). A script proves that line by line, and checks that SGK's
source is still the frozen tree and that every one of its 25 files has a declared fate. The package
imports with no client on the path, and loads neither `ray`, `sqlalchemy` nor `datastorekit` when
it does.

**No behaviour changes.** The couplings C1–C9 (README §0.2) are imported as they are, including the
lazy `from config.datastore import factories` at `stores.py:1494`: they are the board's §3 issues,
owned by 03–05. A further defect noticed in SGK's code is recorded, not fixed (README §5 rules 4
and 8).

---

## 2. What to change

### 2.1 The venv

`venv/` exists from set-up and is gitignored: Python 3.12.15 (`/opt/local/bin/python3.12`),
`ray==2.43.0`, `SQLAlchemy==2.0.39`, `datastorekit` from
`git+https://github.com/ds283/DatastoreKit@v0.4.0` (commit `c8570e8`), `black==25.1.0`. Do not
recreate it. Install the package into it editable (`./venv/bin/python -m pip install -e .`), so the
tests import the package as a client will. Record `pip freeze` in the log.

### 2.2 The package skeleton

- `pyproject.toml`: a setuptools build, as RayPoolKit's (`setuptools>=64`,
  `setuptools.build_meta`); name `runregistrykit`; version **`0.1.0.dev0`** (U3);
  `requires-python = ">=3.12"`; **no core dependency**; one optional-dependency group, `stores`,
  holding `datastorekit` with no version bound (06 sets the floor, U13). Packages are found by
  `include = ["runregistrykit*"]`; the test package is included for now (06 decides whether the
  wheel carries it).
- `runregistrykit/tests/__init__.py`: SGK's `RunRegistry/tests/__init__.py`, which is empty.

There is no new `runregistrykit/__init__.py`: SGK's `RunRegistry/__init__.py` **is** the package's
`__init__.py`, the core.

### 2.3 The files, under README §4's names

| SGK at `a45aefc` | Here |
|---|---|
| `RunRegistry/__init__.py` (blob `0228a1a`) | `runregistrykit/__init__.py` |
| `RunRegistry/stores.py` (blob `a0f18ba`) | `runregistrykit/stores.py` |
| `RunRegistry/__main__.py` (blob `88cf6dd`) | `runregistrykit/__main__.py` |
| `RunRegistry/tests/__init__.py` (blob `e69de29`, empty) | `runregistrykit/tests/__init__.py` |
| — | `runregistrykit/tests/test_package_imports.py`, new (§2.7) |

The three modules import each other relatively only (`from . import …`, `from .stores import …`),
so no import statement changes.

### 2.4 The differences allowed, and no others

- **D-name — the package's name.** On a changed line, every whole-word occurrence of `RunRegistry`
  (the regular expression `\bRunRegistry\b`) becomes `runregistrykit`, and nothing else on the line
  changes. It applies wherever the word occurs: the CLI's `prog="RunRegistry"`
  (`__main__.py:373`), the `python -m RunRegistry …` text of nine error messages in `stores.py`,
  and the docstrings and comments, 23 lines in all (6 in `__init__.py`, 13 in `stores.py`, 4 in
  `__main__.py`). The rule is uniform, so a few renamed lines now cite SGK paths that do not exist
  here, such as `runregistrykit/tests/data/full_store_fingerprint*.json` in the format history
  (`stores.py:197`, deleted at 04). List those lines in the log; their prose is 05's.
- **D-fmt — formatting.** `black` 25.1.0, no configuration. SGK's tree is black-clean under 25.1.0,
  and D-name lengthens a line by three characters per occurrence; but every renamed line is inside
  a docstring, comment or string, which `black` does not split, and the three modules with D-name
  applied by `sed` are black-clean (both probed at this prompt's writing). So this class should
  change nothing. Any line `black` changes is reported in the log and is a stop (§5).

**Not allowed here, though wanted later:** anything that resolves C1–C9 (03–05), a licence header
(U12, 05), a public name for `_slug` (U11, 05), any rewording beyond D-name. `REPO_ROOT` stays the
package's parent: in this repository's editable install that is this repository's root, which the
gitignore's `var/` covers.

### 2.5 The fate of every source file

The check of §2.6 holds this table as data. Each of SGK's 25 files under `RunRegistry/` at
`a45aefc`, plus the shard fixture 02 carries, has exactly one fate:

| SGK file | Blob | Fate |
|---|---|---|
| `RunRegistry/__init__.py` | `0228a1a066793332191affe90c4b309a153aa60c` | **imported by 01** |
| `RunRegistry/__main__.py` | `88cf6ddd2b7603fc718fd6b3d7ed9722261a874f` | **imported by 01** |
| `RunRegistry/stores.py` | `a0f18ba49a25fe795af79baa8f82ce0e09cf3b25` | **imported by 01** |
| `RunRegistry/tests/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | **imported by 01** |
| `RunRegistry/tests/store_fixtures.py` | `391f31fc2155c1f2d8f2350d306272ee6e0ae54e` | ported by 02 |
| `RunRegistry/tests/test_run_registry.py` | `01c3ea37d8491c63300667f5a181f3bad91000ab` | ported by 02 |
| `RunRegistry/tests/test_store_sidecar.py` | `533d1118447527cfef65a833525516fcadbbc2e7` | ported by 02 |
| `RunRegistry/tests/test_store_copy_move.py` | `4be78d983aa83d5d7d39fc440519347cc87386bd` | ported by 02 |
| `RunRegistry/tests/test_store_command_line.py` | `6f111e29e9b695340a88bf19eb18a50e89a9ea05` | ported by 02 |
| `RunRegistry/tests/test_store_amend.py` | `8b7db110f76ae74bfb4716fe12d7192bac38265e` | ported by 02 |
| `RunRegistry/tests/test_store_amend_residuals.py` | `0c6e6a2ca5d59b74dcb960111a5cd05ed2d991f4` | ported by 02 |
| `RunRegistry/tests/test_store_retire.py` | `3cf05cc02d6b00849a4eff4972ccbedd0a4fa51d` | ported by 04 |
| `RunRegistry/tests/test_store_retire_references.py` | `9a3264a7f5977311161f724651b4e1d27cfa0866` | ported by 04 |
| `RunRegistry/tests/test_store_fingerprint.py` | `5039b4792210c1227230ec09b48da641b6f62e9f` | ported by 04, less `TestGolden` and `TestDrivers`, which stay in SGK |
| `RunRegistry/tests/test_build_rehearsal_scope.py` | `8b3c8519d3956b97cce84ea8224c621f37d88cd0` | not imported: SGK's |
| `RunRegistry/tests/test_killed_handler.py` | `213f2a8d7d017f845b85ea209f8e87886539988b` | not imported: SGK's |
| `RunRegistry/tests/test_pipeline_adoption.py` | `f3205799afa5626fe440e409fce37c1cb9fa04c7` | not imported: SGK's |
| `RunRegistry/tests/test_prune_on_resume.py` | `23533e68f7682a172ecf7246b84bbd749b1e5ff8` | not imported: SGK's |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | `527a9878d588309fd6f82f214bc655be627cea5d` | not imported: SGK's |
| `RunRegistry/tests/data/full_store_fingerprint.json` | `58b35c3677f40e5421c7390ac282f1e6e808cd68` | not imported: SGK's |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-07.json` | `2fea28b072cd9f4cdb15062ab355c9c08a45d57e` | not imported: SGK's |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-08.json` | `511ff2d3873437480cbb6af028ba8fbdc5699b87` | not imported: SGK's |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09a.json` | `bd6a855c9d109a8da654ab790eadfc681ad5cea8` | not imported: SGK's |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09b.json` | `01d7ef02e88c53a4160e5660711f0746f3ae4a90` | not imported: SGK's |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09c.json` | `6cf0a39496c0e96bd3b2640324482e7d51686908` | not imported: SGK's |
| `StoreFixtures/shard_store_fixtures.py` (outside `RunRegistry/`) | `1375949aacde2263de991785055cd7dfabc57251` | ported by 02, as `runregistrykit/tests/shard_store_fixtures.py` (U4) |

`StoreFixtures/real_store_fixtures.py` (blob `a6d90b86f2517c4e7cc798897534be8ed4b3d7c6`) is not
imported: it imports SGK's `config` and `ObjectFactories`, and 04's neutral store replaces it.

### 2.6 The equivalence check

`docs/extraction/compare_with_source.py`, kept in the repository, run from the root as
`./venv/bin/python docs/extraction/compare_with_source.py`. The SGK path, the import commit (full
hash) and §2.5's table are constants at its top. It reads SGK only through `git -C <SGK> …` at the
import commit, never SGK's working tree, and imports nothing of SGK or of this package.

- **The frozen tree.** `git ls-tree -r <commit> -- RunRegistry/` must equal §2.5's 25 rows under
  `RunRegistry/` exactly, path and blob, with no row missing or extra; and
  `git rev-parse <commit>:StoreFixtures/shard_store_fixtures.py` must be its blob.
- **The fates.** Every file the table says is imported must exist here under §2.3's name. A file
  ported by a later prompt is reported as *pending, NN* while it is absent; if it is present, it
  must be checked (02 extends the rules to its files, §4 of the README). A file "not imported" must
  not exist under `runregistrykit/` by its source's name.
- **Every file here is declared.** It walks `runregistrykit/` and requires each `.py` file to be
  either the target of a table row or one of the declared new files (at 01, only
  `tests/test_package_imports.py`). An undeclared file fails, so a later prompt that adds one must
  declare it.
- **Line by line.** For each imported file, it diffs source and package line by line (`difflib`)
  and puts **every** differing line pair in exactly one class of §2.4, **by rule, not by a list of
  line numbers**: a pair is D-name only if applying the D-name substitution to the source line
  gives the package line exactly. An added or deleted line is never classified, and neither is a
  replaced block whose two sides differ in length.
- It prints, for each file, the count per class, every line it could not classify, and the pending
  files; and it exits non-zero if any line is unclassified, any blob differs, or any file is
  missing or undeclared. It exits 0 with pending files present.

**Show that the check bites.** With the tree otherwise correct, make each change separately, show
that the script exits non-zero and names what is wrong, then revert:
- (a) `DEFAULT_STALE_AFTER = 901.0` in `__init__.py`;
- (b) an extra `import os` added to `__main__.py`;
- (c) one deleted line in `stores.py`;
- (d) `prog="runregistrykit"` changed to `prog="RunRegistryKit"` (a rename D-name does not cover);
- (e) `"var", "runs"` changed to `"var", "run"` on the `DEFAULT_ROOT` line (a change on a line
  D-name does not touch);
- (f) a word other than `RunRegistry` changed on a line that D-name also changes;
- (g) an undeclared `runregistrykit/extra.py`;
- (h) a wrong blob in the script's table for one "not imported" row (the frozen-tree check must
  fail, naming the row).

### 2.7 The import test

New `runregistrykit/tests/test_package_imports.py`, three tests:

1. **The package loads nothing heavy.** In a fresh interpreter (`sys.executable -I`, run from a
   `tempfile` directory), `import runregistrykit, runregistrykit.stores` succeeds, and afterwards
   none of `ray`, `sqlalchemy`, `datastorekit`, `config`, `ObjectFactories`, `StoreFixtures` or
   `RunRegistry` is in `sys.modules`. This is SGK's property (`stores.py:1454-1455`, SGK's
   `test_store_command_line` checks it there), kept.
2. **Module scope is the standard library and the package.** It parses `__init__.py`,
   `stores.py` and `__main__.py` with `ast` and requires every import statement **at module scope**
   to name a standard-library module (`sys.stdlib_module_names`) or the package itself, relative or
   absolute. Imports inside functions are not checked here: as imported, `stores.py` has
   `datastorekit` and `config` there, which 04 and 05's guard deal with. The failure names file,
   line and module.
3. **The CLI answers to its name.** `sys.executable -I -m runregistrykit --help`, from a `tempfile`
   directory, exits 0 and its first line of usage names `runregistrykit`. It must not write
   anything: run it with the temporary directory as the working directory, and assert afterwards
   that the directory is still empty and that no `var/` was created beside the package.

### 2.8 `PROVENANCE.md`

At the repository root, after RayPoolKit's `PROVENANCE.md` in form:
- the source repository, its URL and local checkout; the import commit `a45aefc` with its full
  hash and subject; and the last commit to change each module before it (`__init__.py`:
  `f54f1c5`, 2026-10-11, "Record the installed packages in each run's manifest"; `stores.py`:
  `5943492`, 2026-10-12, "Close the dk-and-rpk-migration campaign"; `__main__.py`: `66617c9`,
  2026-09-25, "Add amend_sidecar and store amend, for one unknown field");
- that this is a fresh import (U2): SGK's history, which the docstrings cite until 05 rewrites
  them, is reachable through the import commit;
- §2.5's table, with its fates, and the new files with no source;
- §2.4's classes, and that C1–C9 are imported unchanged and owned by 03–05 (the board's §3);
- how to re-run §2.6;
- **SGK's freeze:** SGK froze `RunRegistry/` at the import commit, by its own `CLAUDE.md`, until it
  adopts this package (G2). A fix wanted there is made here. This prompt edits no client.

---

## 3. Verification

1. In a **fresh shell with no `PYTHONPATH`**, from a scratch directory:
   ```bash
   /Users/ds283/Documents/Code/RunRegistryKit/venv/bin/python -I -c "import runregistrykit, runregistrykit.stores, sys; assert not {'ray', 'sqlalchemy', 'datastorekit'} & set(sys.modules)"
   ```
   succeeds. With `-c "import RunRegistry"`, and again with `-c "import config"`, it fails with
   `ModuleNotFoundError`, which shows that no SGK code is on the path.
2. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .` gives
   **`Ran 3 tests … OK`**: §2.7's three. The count before is 0 (there is no suite).
3. `compare_with_source.py` exits 0. Its whole output goes in the log. It should report 25 rows and
   the fixture blob equal; four files imported, of which `__init__.py` has 6 D-name lines,
   `stores.py` 13 and `__main__.py` 4, and `tests/__init__.py` none; 11 files pending (8 for 02, 3
   for 04); 11 not imported and absent; one declared new file. If a count differs, explain it.
4. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed.
   - §2.6's (a)–(h), each failing the check;
   - an `import json` added at module scope of `__main__.py` passes §2.7 test 2 (it is standard
     library), and `import numpy` there fails it, naming the line;
   - `from datastorekit.SQL.ShardedPool import ShardedPool` moved from inside `copy_store` to the
     module scope of `stores.py`, failing §2.7 tests 1 and 2 (and the check, as an added and a
     deleted line);
   - §2.6's (d), which must also fail §2.7 test 3.
5. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2.2's and §2.3's files exist under their names, with `pyproject.toml`, `PROVENANCE.md` and the
   check.
2. §3.1–§3.5 hold.
3. **The records**, in the same commit:
   - the log, `logs/01-import-the-registry.md`, per README §5.1, with `pip freeze`, the check's
     output, the D-name lines that now cite SGK paths (§2.4), and the suite count before (0) and
     after (3);
   - this board: the header, §1's row for 01 (landed, commit, suite 3), §1.1's I1 and I2, §2's G1
     (the package side for 01's files), and §3: for each of the seven issues, the lines in
     `runregistrykit/` where its code now sits, so 02–05 are pointed at the package rather than at
     SGK;
   - `prompts/INDEX.md`: the campaign's line;
   - `docs/OPEN_ISSUES.md`, if the work opens or changes anything.

---

## 5. Stop conditions — stop and ask the user

- G1 no longer holds on the source side: a blob of §2.5 reads differently at `a45aefc` (it cannot
  change for a fixed commit; if it does, something is wrong with the checkout).
- A package module differs from its source in a way neither D-name nor D-fmt covers, and making it
  fit would mean changing behaviour.
- `black` 25.1.0 would reformat any line of the three modules.
- `import runregistrykit` or `import runregistrykit.stores` loads `ray`, `sqlalchemy` or
  `datastorekit`, or needs a client module, without any change beyond §2.4: that would contradict
  README §0.2's measurement.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit. Reading SGK through `git show` / `git ls-tree` / `git rev-parse`, and reading
  RayPoolKit's two files, is the only access this prompt has.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `pyproject.toml`;
  - `runregistrykit/`, as §2.2, §2.3 and §2.7 list;
  - `docs/extraction/compare_with_source.py`;
  - `PROVENANCE.md`;
  - the log, this board, `prompts/INDEX.md`;
  - `docs/OPEN_ISSUES.md`, if needed.
- It ports no test from SGK (02, 04) and carries no fixture (02).
- It resolves none of C1–C9: no config file, no root rule, no fingerprinter (03, 04), no prose
  rewrite, no guard against naming a client (05).
- It sets no dependency range, adds no CI and makes no tag (06).
- It does not touch `README.md` or `CLAUDE.md` at the root. `CLAUDE.md`'s test command is added
  by 02, when there is a suite worth running.

---

## 7. The log and the board

`logs/01-import-the-registry.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 01, §1.1, §2's G1 and §3's package line numbers.
