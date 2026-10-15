# Prompt 04b — the retire tests

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 04a has landed (`c81ad06`) and been reviewed (`8880cfa`, the board's §1). `git diff --stat 8880cfa
  HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` is empty.
- U14 is taken (README §6.2, 2026-10-15): this prompt makes the two fixes of §2.3 and §2.4.
- The suite is `Ran 186 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]`,
`[04a-the-loader-accepts-a-fingerprinter-class]`. **Narrows:**
`[00-a-refusal-matches-datastorekit-message-text]` (a test now reaches the match; the issue stays
open, its remedy a request to DatastoreKit), `[02-the-ported-tests-name-sgk]` (the port adds its
lines). **Opens:** only what the work finds.

**Recommended model:** **Opus**. The port is mechanical and was trial-run at writing (all 51 pass),
but the two fixes change what `store retire` deletes, and the review of the port is the only check
that SGK's 51 assertions survive.

**Read first:**

1. [`README.md`](README.md): §0.2 (the tests; the couplings the brief does not list, the
   DatastoreKit message text), §4, §5 (all of it; rules 6, 7, 9 and 10 especially), §6.1 (D4) and
   §6.2 (U7, U8, U14).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §1's review of 04a, and §3's issues, the
   two this prompt closes and `[00-a-refusal-matches-datastorekit-message-text]` above all.
3. [`logs/04a-the-client-fingerprinter.md`](logs/04a-the-client-fingerprinter.md): "What shipped",
   deviations 2, 8, 9, 17 and 18 (the classes and shims 04b follows), and "State handed to the next
   prompt".
4. `runregistrykit/stores.py`: `_find_references` (`:1400-1483`), `retire_store` (`:1504-1836`), its
   step 3 (`:1641-1723`); `runregistrykit/fingerprint.py` in full; `runregistrykit/tests/`:
   `neutral_store.py`, `test_store_fingerprint.py` (its imports and shims, `:1-70`),
   `test_store_command_line.py`, `store_fixtures.py`, `client_fixtures.py`, and
   `test_fingerprinter.py`'s fixtures (`:1-135`) and `TestPrecedence` (`:368-413`).
5. SGK's `RunRegistry/tests/test_store_retire.py` and `test_store_retire_references.py` at
   `a45aefc`, through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show a45aefc:<path>` only.
6. `PROVENANCE.md`; `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers below are the package's at `8880cfa` (its package files are `c81ad06`'s), and SGK's at
`a45aefc` where marked "SGK".

---

## 1. What is wanted

SGK's two retire test modules, ported onto 04a's neutral store: `test_store_retire` (41 tests) and
`test_store_retire_references` (10), each test keeping its module, class and method name and what
it asserts. Among them is `TestWithoutFingerprint.test_an_unreadable_shards_table`, the one test
that reaches the store layer's match on DatastoreKit's message text. With them, every test of SGK's
`RunRegistry/tests/` that this campaign imports is ported (README §4's module map).

And two fixes, U14's, because the port exercises the path they close. Since 04a,
`fingerprint_store` loads the client's fingerprinter, and `store retire --without-fingerprint`
records **any** exception from `fingerprint_store` as "this store cannot be fingerprinted" and then
deletes the store. So a config whose fingerprinter cannot be loaded, or names the class
`DatastoreKitFingerprinter` rather than an instance (which the loader accepts), lets a store that
**can** be fingerprinted be retired under the flag, with the load error recorded as the reason
(measured at writing, §"At writing"). §2.3 loads the fingerprinter before the attempt; §2.4 has the
loader refuse a class.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit`
`v0.4.0` (`c8570e8`), `runregistrykit` editable, `git` 2.56.0. **Install nothing.**

### 2.2 The port, and the changes allowed

`runregistrykit/tests/test_store_retire.py` and `test_store_retire_references.py`, from SGK's at
`a45aefc`. README §5 rule 9 holds: no test is dropped, renamed or weakened. The classes of change,
each instance listed in the log, are those 02, 03 and 04a used:

- **D-name**, as 02: `\bRunRegistry\b` → `runregistrykit`, on every line (18 lines: 11 and 7). It
  covers the one assertion that partitions on SGK's command text, `` Run `python -m RunRegistry store
  retire `` (SGK `test_store_retire.py:198`), whose package text is `python -m runregistrykit`.
- **D-fix**, as 02: `StoreFixtures.shard_store_fixtures` → `runregistrykit.tests.shard_store_fixtures`
  (SGK `:49`).
- **N-fix**, as 04a (its deviations 17 and 18), a substitution on every line:
  `StoreFixtures.real_store_fixtures` → `runregistrykit.tests.neutral_store` (the import, SGK `:48`,
  and the module docstring, `:18`); `from config.datastore import factories as _factories` → `from
  runregistrykit.tests.neutral_store import FACTORIES as _factories` (`:54`); and
  `compare_fingerprints`, which `runregistrykit.stores` no longer has, dropped from the import of
  `:37` and given by a **module-level shim** of the same name, `compare_fingerprints =
  FINGERPRINTER.compare`, as `test_store_fingerprint.py` has it, so that no test body changes for it.
- **N-class**, as 04a: `QSI = "QuadSourceIntegral"` → `QSI = "Integral"` (SGK `:58`), the one SGK
  class name in a constant or literal of either module. Method and class names do not change.
- **R-root**, as 03: a test-body call `_repo_path(p)` passes the test's client root,
  `_repo_path(p, self.client)` (SGK `test_store_retire.py:166, 281, 293-295, 305-307, 312, 318, 321,
  541, 723, 773, 810, 859, 1109`; `test_store_retire_references.py:71, 128, 149, 155, 163, 179,
  189`); the alias `_repo_path = RunRegistry._repo_path` (`:59`; `:31`) keeps its form under D-name;
  and a path computed against `REPO_ROOT` is computed against `self.client`
  (`test_store_retire.py:241`; `test_store_retire_references.py:68, 112, 124, 141`), the import of
  `REPO_ROOT` at `test_store_retire_references.py:29` going. The value asserted is unchanged: the
  stores and runs are outside the client root, as in 03.
- **R-cwd**, as 03 did in `test_store_amend.py`: `REPO_ROOT` in the import from
  `test_store_command_line` (`test_store_retire.py:41`) becomes `PACKAGE_PARENT`, and the IMPORTS
  child (`:1215-1216`) runs with `cwd=self.client` and `PYTHONPATH` the package's parent.
- **D-fmt**: `black` (it reflows the lines R-root lengthens; SGK's files are `black`-clean as they
  are).

**No F-client is needed.** `RetireTestCase` builds on `CommandLineTestCase`, whose
`StoreTestCase.setUp` makes the client root with 04a's default config, which names the neutral
fingerprinter.

No other line changes. A ported test that fails with only these changes is a **stop** (§5), and so
is one that would need a change outside them. Verify the port as 04a did, outside the repository:
a scratch script applies the classes to SGK's files and `black`s them; its output and the committed
files differ by nothing but the shim lines. The log gives the script's summary and the diff.

### 2.3 `store retire` loads the fingerprinter before it fingerprints (U14 (a))

In `retire_store`'s step 3, on a **first** retirement (the branch at `:1668`, not the completion of
an incomplete one, which takes no fingerprint), `load_fingerprinter(client)` is called **before the
files are planned** (`:1671`) and before either fingerprint branch. A `ConfigError` from it comes
through **unwrapped**, before anything is written: the store's files, its sidecar and the rest of
the tree are unchanged, as for every other refusal. So:
- under `--without-fingerprint`, a fingerprinter that cannot be loaded is a refusal, never a
  `"without"` condition; the flag still records, verbatim, any failure of the fingerprint itself
  (a journal, a corrupt shard, a schema mismatch), which is what D4's flag is for;
- without the flag, the same `ConfigError` comes through as itself, rather than inside the "a fresh
  fingerprint could not be taken" refusal, whose remedy points at the flag.

Precedence: the reason and sidecar refusals (step 1) and the in-use refusals (step 2) still come
first, as `fingerprint_store`'s own order has it (04a's `TestPrecedence`). The completion path is
unchanged. The docstring's step 3 gains one sentence saying so; nothing else of `retire_store`
changes, and no refusal's text changes.

### 2.4 The loader refuses a class (U14 (b))

`load_fingerprinter` (`fingerprint.py:158-192`) refuses, as a `ConfigError` naming the config file
and the spec, an object that is a class (`isinstance(found, type)`), before its `Fingerprinter`
check, with text saying that the config names a class and must name an instance of it (for
`DatastoreKitFingerprinter`, one made with the registry and the format number). A runtime-checkable
protocol checks only that the attributes exist, and a class has them; nothing else of the loader
changes. The module docstring's sentence on the loader says so.

### 2.5 The new tests

In `runregistrykit/tests/test_fingerprinter.py` (04a's, not a ported module), every directory a
`tempfile` one, at least:
- **The class refused**: a config naming `runregistrykit.fingerprint:DatastoreKitFingerprinter`,
  and one naming a class with the four methods in a module of the client root (a fresh module name,
  `sys.path` and `sys.modules` restored, as 04a's `a_module_name`), each a `ConfigError` naming the
  file and the spec, from `load_fingerprinter`.
- **Retire with a fingerprinter that cannot be loaded**: a fingerprintable store with a registry
  sidecar and a recorded fingerprint (taken while the config named the neutral fingerprinter);
  then the config names (i) a module that exists nowhere, (ii) the class. For each: `retire_store`
  with and without `without_fingerprint=True`, and with `dry_run=True`, raises `ConfigError`, and
  the store directory, the sidecar's bytes and the runs root are unchanged; `store retire
  --without-fingerprint` through `CommandLineTestCase.command` exits 1 with `!!` naming the config
  file and leaves the tree unchanged.
- The flag still applies where it should: SGK's `TestWithoutFingerprint` tests (a corrupt shard, a
  missing shard, a journal) pass unchanged with the neutral fingerprinter configured; no new test
  is needed for that.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root: **`Ran 186
   + 51 + N tests … OK`**, N §2.5's. 186 before. Count by loader and give the per-module counts and
   the time.
2. **Nothing outside temporary directories**: `git status --short --ignored` the same before and
   after a run (but `__pycache__/`); no `var/`; `git worktree list` this checkout alone; no Ray
   process before or after.
3. **The port**, §2.2's script: its diff from the committed files, summarised by class; the test ids
   are SGK's 51, by class: `TestRetirement` 1, `TestAnotherStoresShards` 1, `TestRefusals` 12,
   `TestInterruption` 8, `TestWithoutFingerprint` 6, `TestDryRun` 3, `TestNeverReused` 3,
   `TestHistoryRule` 3, `TestCommandLine` 4; `TestTheStoresRootIsNotATarget` 5,
   `TestADirectoryIsStillATarget` 5.
4. `grep -rn "REPO_ROOT\|StoreFixtures\|config.datastore\|QuadSource" runregistrykit
   --include=*.py` finds only `test_package_imports.py:32` (its `FORBIDDEN` list), as at `8880cfa`:
   D-fix and N-fix substitute every line, docstrings included.
5. **The tests catch behaviour** (README §5 rule 10). Each applied, the suite run, reverted, and
   recorded as a diff with the tests that fail:
   - (m1) `_SHARDS_TABLE_UNREADABLE`'s text reworded (as a DatastoreKit rewording would leave it):
     `test_an_unreadable_shards_table` must fail;
   - (m2) `_find_references` taking the stores root as a target (`:1431-1432`'s condition dropped);
   - (m3) `retire_store` recording `matched` without refusing a comparison's differences;
   - (m4) §2.3's load removed;
   - (m5) §2.3's load moved after the files are planned **and** wrapped in the flag branch's
     `except` (the hazard back by another route), or another of the agent's naming the same path;
   - (m6) §2.4's class refusal removed;
   - (m7) the agent's own, of the deletion order (the primary deleted before its shards, or the
     tombstone marked `retired` before the check that no listed file exists), or another named in
     the log.
   Each must fail at least one test. A mutation no test catches is a **stop**.
6. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` gains exactly `tests/test_store_retire.py` and
   `tests/test_store_retire_references.py`; `stores.py`, `fingerprint.py` and `test_fingerprinter.py`
   change as §2.3–§2.5 say.
2. §3.1–§3.6 hold.
3. **The records**, in the same commit:
   - the log, `logs/04b-the-retire-tests.md`, per README §5.1: every D-name, D-fix, N-fix, N-class,
     R-root, R-cwd and D-fmt instance accounted for; the port script's summary and diff; the suite
     before (186) and after; every mutation as a diff;
   - this board: the header, §1's row for 04b, §1.1's T2b and F3, §3 and §4 (the two issues closed,
     each with what resolved it and the tests that pin it;
     `[00-a-refusal-matches-datastorekit-message-text]` narrowed with the test that reaches the
     match, its owner still none; the others' package lines at this commit;
     `[02-the-ported-tests-name-sgk]` gaining the port's lines);
   - `docs/OPEN_ISSUES.md`: the two rows deleted (6 → 4), the count, the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `PROVENANCE.md`: "Since the import" gains 04b's section (the two modules ported; the two
     fixes); the file map's rows for the two modules say "ported by 04b".

---

## 5. Stop conditions — stop and ask the user

- A ported test fails with only §2.2's changes, or would need a change outside its classes.
- The neutral store would need a change to serve a ported test (it is 04a's; a change to it is
  outside this prompt).
- A mutation of §3.5 is caught by no test.
- Any record would change form: a manifest, `status.json`, `checkpoint.jsonl`, sidecar or tombstone
  field added, removed or renamed, or the tombstone's `fingerprint` condition changed in form.
- DatastoreKit behaves otherwise than the port assumes (README §5 rule 11: record it, do not work
  around it).
- The suite needs a Ray cluster, starts Ray, imports a client, writes outside a `tempfile`
  directory, or leaves a worktree registered here.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `runregistrykit/stores.py` (§2.3 and its docstring sentence only), `fingerprint.py` (§2.4 and its
    docstring sentence only);
  - `runregistrykit/tests/`: new `test_store_retire.py`, `test_store_retire_references.py`;
    `test_fingerprinter.py` (§2.5's tests only);
  - `PROVENANCE.md`; the log, this board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It changes nothing in `neutral_store.py`, `client_fixtures.py`, `store_fixtures.py`,
  `shard_store_fixtures.py`, `__init__.py`, `__main__.py`, `client.py`, or any other test module.
- It changes no prose but what its own changes need (05), and names no client in the package. The
  SGK citations the ported modules carry (their docstrings' campaign and prompt names, "the live A3
  backup", `sweep_shaped`) are recorded under `[02-the-ported-tests-name-sgk]` for 05.
- It changes `pyproject.toml` not at all, adds no CI and makes no tag.

---

## 7. The log and the board

`logs/04b-the-retire-tests.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 04b, §1.1's T2b and F3, §3 and §4 as §4.3.

---

## At writing (2026-10-15, at `8880cfa`)

Measured read-only, for the README's row and the orchestrator:
- **SGK's two modules** (through `git show a45aefc`): `test_store_retire.py` 1220 lines, 41 tests in
  nine classes; `test_store_retire_references.py` 192 lines, 10 tests in two, its base
  `test_store_retire.RetireTestCase`. Both `black`-clean. Every store is
  `build_full_store(…, shards=4)` with a registry sidecar and a recorded fingerprint
  (`RetireTestCase.a_full_store`, SGK `:92-111`). SGK names in their code: `QSI` alone; in prose,
  "store-retirement prompt 03", "a3-v2-readiness prompt 06",
  `[10-store-retire-reports-every-tombstone-as-a-reference]` and "the live A3 backup"; and
  `sweep_shaped`, 02's carried helper.
- **A trial port** (the planner's scratchpad), D-name, D-fix, N-fix with the `compare_fingerprints`
  shim, N-class, R-root, R-cwd and `black`, written into a `git archive` export of `8880cfa` (its
  own package imported): **`Ran 51 tests in 29.8s`, OK**. No F-client was needed. Substitutions
  counted: D-name 18, D-fix 1, N-fix 2 and the shim's 3, N-class 1, R-cwd 3, R-root 30 (the
  `_repo_path` calls and the five `REPO_ROOT` paths, and the import removed).
- **Three mutations, on the trial port** (applied cumulatively by mistake, so each is read by the
  tests it added): `_SHARDS_TABLE_UNREADABLE` reworded fails
  `TestWithoutFingerprint.test_an_unreadable_shards_table` (both subtests), which asserts the text
  "refused even under --without-fingerprint" that only the match produces; `_find_references`
  taking the stores root as a target adds five `TestTheStoresRootIsNotATarget` failures; skipping
  the refusal of differences adds `TestRefusals.test_a_row_changed_after_fingerprinting` and
  `test_a_mismatch_in_problems_alone`.
- **The hazard U14 answers**, probed on a neutral store with a registry sidecar, in a scratch
  client: with the config's fingerprinter then naming `no_such_module_x:F`, `retire_store(…,
  without_fingerprint=True)` **retired the store**, recording `{"condition": "without", "error":
  "…could not be imported (ModuleNotFoundError…)", "error_type": "ConfigError"}`; naming
  `runregistrykit.fingerprint:DatastoreKitFingerprinter` (the class), it retired it recording
  `TypeError: DatastoreKitFingerprinter.take() missing 1 required positional argument: 'taken'`.
  Only the sidecar was left. The store could have been fingerprinted with the right config. No
  client runs this code yet; it is in no release.
