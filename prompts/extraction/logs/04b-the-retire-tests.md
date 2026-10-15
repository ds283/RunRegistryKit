# Log — prompt 04b: the retire tests

**Subject:** Port the retire tests and load the fingerprinter before a retirement
**Commit:** this commit (on `main`, after `5177ffa`)
**Date:** 2026-10-15
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and the orchestration
note's §0 (`orchestrator-section-0.md`)
**Result:** **landed.** SGK's `test_store_retire` (41 tests) and `test_store_retire_references` (10)
are ported onto 04a's neutral store, each test keeping its module, class and method name and what it
asserts; with them every SGK test README §4 imports is ported, and
`TestWithoutFingerprint.test_an_unreadable_shards_table` reaches the match on DatastoreKit's message
text. U14's two fixes: `retire_store` loads the client's fingerprinter on a first retirement before
it plans the files, so a fingerprinter that cannot be loaded is a `ConfigError`, unwrapped, before
anything is written, under `--without-fingerprint` or not; and `load_fingerprinter` refuses a class.
The suite: **186 → 245** (`186 + 51 + 8`), `Ran 245 tests … OK`. (m1)–(m10) each fail at least one
test. No stop condition was met. Two issues closed
(`[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]`,
`[04a-the-loader-accepts-a-fingerprinter-class]`), two narrowed
(`[00-a-refusal-matches-datastorekit-message-text]`, `[02-the-ported-tests-name-sgk]`);
`docs/OPEN_ISSUES.md` goes from 6 to 4.

## What shipped

| File | What |
|---|---|
| `runregistrykit/stores.py` | `retire_store`'s step 3: on a first retirement (the `else:` of `if completing:`), `load_fingerprinter(client)` before `ShardedPool.closed_store_files`, its result unused, with a two-line comment; one sentence at the end of the docstring's step 3. Nothing else |
| `runregistrykit/fingerprint.py` | `load_fingerprinter`: `isinstance(found, type)` refused before the `Fingerprinter` check, as a `ConfigError` naming the config file and the spec, saying the object is the class and to name an instance (for `DatastoreKitFingerprinter`, one made with the client's registry and its format number), with a one-line comment; the module docstring's sentence on the loader, and the rest of its paragraph rewrapped |
| `runregistrykit/tests/test_store_retire.py` | **new**, ported from SGK's at `a45aefc` by §2.2's classes: 41 tests |
| `runregistrykit/tests/test_store_retire_references.py` | **new**, ported likewise: 10 tests |
| `runregistrykit/tests/test_fingerprinter.py` | 8 tests: `TestProtocolAndLoader.test_a_class_is_refused_and_an_instance_of_it_loads`; the fixture `_RetireCase`; `TestRetireLoadsTheFingerprinterFirst` (2); `TestRetirePrecedence` (5); the imports `errno` and `mock` |
| `PROVENANCE.md` | the file map's two rows "ported by 04b, onto the neutral store"; 04b's section under "Since the import" |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

`runregistrykit/` gains exactly `tests/test_store_retire.py` and `tests/test_store_retire_references.py`.
Not touched: `neutral_store.py`, `client_fixtures.py`, `store_fixtures.py`, `shard_store_fixtures.py`,
`test_store_fingerprint.py`, `runregistrykit/__init__.py`, `__main__.py`, `client.py`,
`pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `.idea/`, `CLAUDE.md`, `docs/extraction/`,
`tests/__init__.py`, every other 02, 03 or 04a test file, the campaign README, the prompt,
`prompts/extraction/orchestrator/`.

**`retire_store`, as built.** Locate; the D4 check; step 1 (the reason, the sidecar, the reason of
an incomplete retirement, a `.tmp`) and step 2 (the runs root, a running run) unchanged; then, on a
**first** retirement only, `load_fingerprinter(client)`, whose `ConfigError` comes through as the
loader raised it; then the plan, the fingerprint branches, the references, the writes, all
unchanged. The completion path is unchanged and loads nothing. No refusal's text changed. The
tombstone's `fingerprint` condition is built as before: `{"condition": "matched", "digest"}`, or
`{"condition": "without", "error", "error_type"}` from `fingerprint_store`'s own exception, which
is now never a load failure, since the same load has just succeeded (the second comes from
`sys.modules`).

**The loader, as built.** `require_fingerprinter`; the split; `sys.path`; the import; the attribute
walk; **then the class refusal**; then the `Fingerprinter` check. Every refusal a `ConfigError`
naming the file and the spec, as before.

## Deviations from the prompt

The note's ten corrections and readings are recorded as found (1–10); the rest are this agent's.

1. **The gate's diff is not empty** (correction 1, found as it says). `git diff --stat 8880cfa HEAD
   -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` shows `docs/OPEN_ISSUES.md` (5
   lines), changed by `d035ffb`; the same diff from `d035ffb` is empty, and the gate was read from
   there. `HEAD` was `5177ffa`, which touches only `prompts/extraction/orchestrator/prompt-04b.md`.
   **STRUCTURALLY REQUIRED.**
2. **The load is a check, not a hand-over** (correction 2). `load_fingerprinter(client)` is called
   for its refusal and its result dropped; `fingerprint_store` loads its own, from `sys.modules`. The
   CLI needed no change: `ConfigError` is a `RuntimeError`, and `_retire`'s `except RuntimeError`
   prints `!!` and returns 1, which `TestRetireLoadsTheFingerprinterFirst.test_store_retire_without_fingerprint_exits_1_naming_the_config_file`
   asserts. **IMPLEMENTATION CHOICE.**
3. **The precedence test** (correction 3, recommendation followed): `TestRetirePrecedence`, five
   tests on `_RetireCase` with a config naming a module that exists nowhere, each with and without
   `without_fingerprint=True` (subtests): (i) `test_the_reason_comes_first`, a blank reason, the
   reason refusal, a `RuntimeError` that is not a `ConfigError` and does not name the spec; (ii)
   `test_a_running_run_comes_first`, the in-use refusal naming the run; (iii)
   `test_a_completed_tombstone_comes_first`, "already retired" (the store retired under the
   neutral config first); (iv) `test_the_fingerprinter_comes_before_the_plan`, a `-wal` beside the
   primary (as SGK's `test_a_journal_is_refused`), the `ConfigError`, which does not name the
   `-wal`; (v) `test_a_completion_loads_no_fingerprinter`, a retirement interrupted at the second
   `os.unlink` under the neutral config completes under the broken one, deleting the four files
   that remained. Each of (i)–(iii) also checks the whole tree unchanged and the text ending
   "Nothing was written or deleted". (m8), (m9) and (m10) are the three placements the note names
   (before step 1; after the plan; on the completion path too), and each fails these tests (below).
   As the note measured: with the fix removed ((m4)), (i)–(iii) and (v) pass and (iv) fails.
   **IMPLEMENTATION CHOICE.**
4. **The probe's "after"** (correction 4) is what `TestRetireLoadsTheFingerprinterFirst` asserts,
   for a module that exists nowhere and for the class `DatastoreKitFingerprinter`: `retire_store`
   with no flag, with `without_fingerprint=True`, with `dry_run=True` and with both, each raises a
   `ConfigError` naming the config file and the spec (and `ModuleNotFoundError`, or "not an instance
   of it"), not the "a fresh fingerprint could not be taken" text, and the tree under the test's
   temporary directory and the sidecar's bytes are unchanged; the store's sidecar still reads `ok`
   at the end; `store retire --without-fingerprint` exits 1, `!!` naming the file and the spec, and
   changes nothing. The "before" is (m4)'s failures: the flag case retires the store (the final
   `read_sidecar(…).ok` fails), and the plain case raises the wrapped refusal. **As found.**
5. **The class refusal before the `Fingerprinter` check** (correction 5): as built. The class cases
   are a **test of their own**, `TestProtocolAndLoader.test_a_class_is_refused_and_an_instance_of_it_loads`,
   not two more subtests of `test_each_refusal_is_a_config_error_naming_the_file`, so that it can
   also check the precondition (each class passes `isinstance(…, Fingerprinter)`) and that an
   instance of the client's class (`STUB`, in the same fresh module) loads. The client's class is
   04a's `Stub`, written into the client root under a fresh name from `a_module_name`.
   **IMPLEMENTATION CHOICE.**
6. **R-cwd's `IMPORTS` child** (correction 6, as found): `PACKAGE_PARENT` imported from
   `test_store_command_line`, as `test_store_amend.py` has it; the child runs with
   `cwd=self.client` and `PYTHONPATH` `PACKAGE_PARENT`, and
   `TestCommandLine.test_import_loads_neither_ray_nor_sqlalchemy` passes. **STRUCTURALLY REQUIRED.**
7. **The port's counts** (correction 7), from the script's summary below: D-name 18 lines (11 and
   7), D-fix 1, N-fix 3 substitution lines (`:18`, `:48`, `:54`) and the shim (the
   `runregistrykit.stores` import, and six added lines, two of them blank), N-class 1, R-root 30
   (24 `_repo_path` calls on 24 lines, the five `REPO_ROOT` paths, the import removed), R-cwd 3;
   then `black`.
   `Ran 51 tests in 27.875s`, OK, before either fix; the ids SGK's 51 by class. Two readings of the
   count: references' `:29` (`from RunRegistry.tests.test_store_command_line import REPO_ROOT`) holds
   `RunRegistry` and is removed by R-root, so the script, which removes it before renaming, reports
   6 D-name lines for that module, and 7 match `\bRunRegistry\b` in SGK's file; and the note's
   "N-fix 4" counts the import change and the shim block as two of N-fix's lines, where this log
   counts N-fix's three substitutions and lists the shim lines apart. No F-client was needed; every
   `_repo_path` call is inside a method. **As found.**
8. **The suite takes longer** (correction 8): 53.3 s before, 87.6 s after (every run below); the 51
   alone 27.9 s; the 59 added cost about 34 s together, each test building and fingerprinting a
   four-shard store. **STRUCTURALLY REQUIRED** (the machine).
9. **SGK's prose the port carries** (correction 9), unchanged under rule 9, listed under
   `[02-the-ported-tests-name-sgk]` for 05: "store-retirement prompt 03"
   (`test_store_retire.py:1`); "real multi-shard fixture stores" (`:18`, its module path now
   `runregistrykit.tests.neutral_store` by N-fix); "a3-v2-readiness prompt 06" and
   `[10-store-retire-reports-every-tombstone-as-a-reference]` (`test_store_retire_references.py:1-2`),
   "the live A3 backup" (`:8`, `:136`), "the real multi-shard fixture stores of `test_store_retire`"
   (`:18`); `sweep_shaped` (`test_store_retire.py:38`, used at `:404`). **As found.**
10. **`PROVENANCE.md`'s file map** (correction 10): the two rows now read "ported by 04b, onto the
    neutral store", and "Since the import" gains 04b's section. **STRUCTURALLY REQUIRED.**
11. **D-fmt reflows lines D-name lengthened as well as R-root's.** The prompt says `black` "reflows
    the lines R-root lengthens"; it also reflows `test_store_retire.py` SGK `:198` (the
    `text.partition(". Run `python -m runregistrykit store retire")` line, three characters longer)
    and `:422` (`runregistrykit.list_runs(…)`). 13 hunks in all, 7 and 6 (the summary below), each
    a line one of the classes lengthened past 88 columns. **STRUCTURALLY REQUIRED.**
12. **The shim's place and form**: as 04a's, after the fixture imports: a two-line comment, `from
    runregistrykit.tests.neutral_store import FINGERPRINTER`, a blank line and
    `compare_fingerprints = FINGERPRINTER.compare`; and `compare_fingerprints` dropped from the
    `runregistrykit.stores` import. Only `test_store_retire.py` needs it; the references module
    imports nothing the package lost. **IMPLEMENTATION CHOICE.**
13. **The port script writes two trees**: `out/port/`, the classes and `black`, and `out/final/`, the
    same with the shim, which the committed files equal byte for byte (`cmp`). The diff of the two is
    the shim alone (below). **IMPLEMENTATION CHOICE.**
14. **The docstring sentences.** `retire_store`'s is appended to the end of step 3, so that no
    existing line is rewrapped; it says the load comes before the files are planned. In
    `fingerprint.py` the loader's sentence gains "and not a class (a class with the four methods
    passes the protocol's check; the config names an instance)", and the four lines after it in the
    paragraph are rewrapped. `load_fingerprinter`'s own docstring, which lists its refusals, is
    unchanged (§2.4: nothing else of the loader changes; observations). **IMPLEMENTATION CHOICE.**
15. **The new tests' fixture is their own**, `_RetireCase` (a four-shard neutral store with a
    registry sidecar and a recorded fingerprint, under a stores root of its own), not the ported
    `RetireTestCase`: the ported `refused_retire` requires the text to end "Nothing was written or
    deleted", which the loader's `ConfigError` does not, and `test_fingerprinter.py` stays
    independent of the ported module's helpers. `enter_config` registers `a_module_name`'s cleanup
    for every config it enters, since the loader puts each client root on `sys.path`.
    **IMPLEMENTATION CHOICE.**
16. **Mutations beyond the prompt's**: (m8)–(m10), deviation 3. **(m7)** is the tombstone marked
    `retired` (written) before the check that no listed file remains: the other variant the prompt
    names, the primary deleted before its shards, is the order of DatastoreKit's
    `ShardedPool.delete_store`, not of the package. **(m5)** removes §2.3's load and puts it inside
    the flag branch's `try`, before `fingerprint_store`. **IMPLEMENTATION CHOICE.**
17. **The mutation diffs are taken against the index**: `stores.py` and `fingerprint.py` were staged
    once final, each mutation made by a checked replacement in the working file, `git diff` taken,
    and the file written back; the index blobs (`526b64d`, `8bbcae4`) are this commit's.
    **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT. No ported test failed with only §2.2's changes, and none needed a change
outside its classes; the neutral store needed no change. No record changes form: the manifest,
`status.json`, `checkpoint.jsonl`, the sidecar and the tombstone (its `fingerprint` condition's
three keys and two values among them) are written by unchanged code; the only change on the retire
path is a refusal that writes nothing. DatastoreKit behaved as the port assumes (the trial's
`closed_store_files`, `delete_store` and the shards-table text). No stop condition (§5) was met.

## Verification performed

**At dispatch.** `main` at `5177ffa`, clean; `git status --short --ignored` showed
`prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
`runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`. `venv/`:
Python 3.12.15, `black` 25.1.0; `git` 2.56.0. No Ray process (`pgrep -lf
'gcs_server|raylet|ray::|default_worker\.py'` exit 1); `RAY_ADDRESS` unset. No `runregistrykit.toml`
in any parent of this checkout or the scratchpad. SGK at `14bcac0`, clean. The gate as deviation 1.

**§3.1, the suite**, `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .` from the
root, in the foreground, output to a scratch file:

| | Verdict |
|---|---|
| before (at `5177ffa`) | `Ran 186 tests in 53.250s`, OK |
| the port only (§2.2), its two modules alone | `Ran 51 tests in 27.875s`, OK |
| after | `Ran 245 tests in 87.570s`, OK; the final run, on the tree committed: `Ran 245 tests in 91.328s`, OK |

**186 → 245**, `186 + 51 + 8`. By loader, after: `test_client_root` 27, `test_fingerprinter` 30
(22 + 8), `test_package_imports` 3, `test_run_registry` 29, `test_store_amend` 21,
`test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
`test_store_fingerprint` 29, `test_store_retire` 41 (new), `test_store_retire_references` 10 (new),
`test_store_sidecar` 17. Every module but the three named had the same count before.
`test_fingerprinter`'s 30: `TestProtocolAndLoader` 8 (7 + 1), `TestTheStoreLayerRequiresOne` 3,
`TestPrecedence` 2, `TestRetireLoadsTheFingerprinterFirst` 2 (new), `TestRetirePrecedence` 5 (new),
`TestOpacity` 2, `TestThroughTheFingerprinter` 3, `TestNeutralStore` 3, `TestSidecarGuards` 2.

**§3.2, nothing outside temporary directories.** `git status --short --ignored` the same before and
after each run but for the changes of this commit (and after each mutation's run, `git status
--short` the same as before it); no `var/` at the root or under `runregistrykit/`; `git worktree
list` this checkout alone; no Ray process before or after the suite or any mutation's run.
`CommandLineTestCase.command` asserts that no CLI child initialised Ray.

**§3.3, the port.** The script, `agent04b/port/port.py` in the session scratchpad (outside the
repository), reads each of SGK's two files with `git -C /Users/ds283/Documents/Code/SecondaryGWKit
show a45aefc:RunRegistry/tests/<name>`, checks that each is `black`-clean, applies D-name, D-fix,
N-fix, N-class, R-root (the `_repo_path` calls by balanced parentheses, the `REPO_ROOT` paths by exact
text, the import by its exact line) and R-cwd line by line, counting the lines each changes, then
`black.format_str(…, mode=black.Mode())` (black 25.1.0 asserted), and checks that no
`RunRegistry`, `StoreFixtures`, `REPO_ROOT`, `config.datastore` or `QuadSource` remains. Its summary,
verbatim (line numbers SGK's):

```
test_store_retire.py: 1220 source lines -> 1234 ported, 1240 with the shim
  D-name    11 lines: 1, 3, 34, 35, 36, 37, 38, 39, 59, 198, 422
  D-fix      1 lines: 49
  N-fix      3 lines: 18, 48, 54
  N-class    1 lines: 58
  R-root    18 lines: 166, 241, 281, 293, 294, 295, 305, 306, 307, 312, 318, 321, 541, 723, 773, 810, 859, 1109
  R-cwd      3 lines: 41, 1215, 1216
  R-root    17 _repo_path calls
  D-fmt      7 hunks: @@ -198 +198,3 @@ @@ -294,2 +296,6 @@ @@ -422 +428,3 @@ @@ -541 +549,3 @@ @@ -723 +733,2 @@ @@ -810 +821,2 @@ @@ -859 +871,3 @@
test_store_retire_references.py: 192 source lines -> 208 ported, 208 with the shim
  D-name     6 lines: 4, 25, 26, 27, 28, 31
  D-fix      0 lines: 
  N-fix      0 lines: 
  N-class    0 lines: 
  R-root    12 lines: 29 (import removed), 68, 71, 112, 124, 128, 141, 149, 155, 163, 179, 189
  R-cwd      0 lines: 
  R-root     7 _repo_path calls
  D-fmt      6 hunks: @@ -70 +70,3 @@ @@ -127 +129,2 @@ @@ -154 +157,3 @@ @@ -162 +167,6 @@ @@ -178 +188,6 @@ @@ -188 +203,3 @@
```

`diff` of the script's `out/port/test_store_retire.py` and the committed file, complete (the
references module: identical, `cmp`):

```
37c37
< from runregistrykit.stores import compare_fingerprints, fingerprint_store, retire_store
---
> from runregistrykit.stores import fingerprint_store, retire_store
54a55,58
> 
> # a shim for the name the package no longer has: the comparison is the client fingerprinter's,
> # here the neutral store's
> from runregistrykit.tests.neutral_store import FINGERPRINTER
55a60,61
> compare_fingerprints = FINGERPRINTER.compare
> 
```

The test ids, by an `ast` walk of SGK's files and the committed ones: **equal**, in order;
`test_store_retire` 41 (`TestRetirement` 1, `TestAnotherStoresShards` 1, `TestRefusals` 12,
`TestInterruption` 8, `TestWithoutFingerprint` 6, `TestDryRun` 3, `TestNeverReused` 3,
`TestHistoryRule` 3, `TestCommandLine` 4); `test_store_retire_references` 10
(`TestTheStoresRootIsNotATarget` 5, `TestADirectoryIsStillATarget` 5).

**Every instance (README §5 rule 9).** Lines are SGK's, then the committed file's where they moved.

- **D-name (18).** `test_store_retire.py`: the docstring `:1` (`runregistrykit.stores.retire_store`)
  and `:3` (`python -m runregistrykit store retire`); the imports `:34`–`:39`; the alias `:59`
  (`_repo_path = runregistrykit._repo_path`, committed `:65`); the partition text `:198` (committed
  `:204-206`, `". Run `python -m runregistrykit store retire"`); `runregistrykit.list_runs` `:422`
  (committed `:434-436`). `test_store_retire_references.py`: the docstring `:4`; the imports
  `:25`–`:28`; the alias `:31` (committed `:30`); and `:29`, removed by R-root.
- **D-fix (1).** `from runregistrykit.tests.shard_store_fixtures import (` `:49`.
- **N-fix (3, and the shim).** The docstring `:18` (`StoreFixtures.real_store_fixtures` →
  `runregistrykit.tests.neutral_store`); `from runregistrykit.tests.neutral_store import
  build_full_store` `:48`; `from runregistrykit.tests.neutral_store import FACTORIES as _factories`
  `:54`. The shim: committed `:37` and `:55-60` (deviation 12).
- **N-class (1).** `QSI = "Integral"` `:58` (committed `:64`). Every body reaches the class through
  `QSI`: the SQL at `:450-451` and `:465` (`Integral`, `Integral_tags`, `parent_serial`) and the
  texts at `:457` and `:477`. Method and class names unchanged.
- **R-root (30).** `test_store_retire.py`, 17 `_repo_path(…)` calls → `_repo_path(…, self.client)`
  at `:166, 281, 293, 294, 295, 305, 306, 307, 312, 318, 321, 541, 723, 773, 810, 859, 1109`, and
  `os.path.relpath(primary.parent, REPO_ROOT)` → `self.client` at `:241`.
  `test_store_retire_references.py`, 7 calls at `:71, 128, 149, 155, 163, 179, 189`;
  `os.path.join(REPO_ROOT, recorded)` → `os.path.join(self.client, recorded)` at `:68`;
  `os.path.relpath(…, REPO_ROOT)` → `self.client` at `:112, 124, 141`; the import of `REPO_ROOT` at
  `:29` removed. The aliases keep their form under D-name. The values asserted are unchanged: the
  stores and runs are under the test's temporary directory, outside the client root, so
  `_repo_path(…, self.client)` is the absolute path, and a path relative to the client root
  resolves, through `_resolve` against `client.root`, to the same realpath.
- **R-cwd (3).** `PACKAGE_PARENT` for `REPO_ROOT` in the import from `test_store_command_line`
  `:41`; `cwd=self.client` `:1215`; `"PYTHONPATH": PACKAGE_PARENT` `:1216` (committed `:1235-1236`).
- **D-fmt (13 hunks).** As the summary; deviation 11.

**§3.4, the grep.** `grep -rn "REPO_ROOT\|StoreFixtures\|config.datastore\|QuadSource" runregistrykit
--include=*.py` finds one line, `runregistrykit/tests/test_package_imports.py:32` (`"StoreFixtures",`,
its `FORBIDDEN` list), as at `8880cfa`.

**§3.6.** `./venv/bin/black --check runregistrykit docs`: 23 files would be left unchanged.

**Isolation.** Nothing was installed; no client, DatastoreKit or RayPoolKit was edited or run. SGK
was read only by `git -C /Users/ds283/Documents/Code/SecondaryGWKit show a45aefc:<path>`, for
`RunRegistry/tests/test_store_retire.py` and `test_store_retire_references.py` (and `rev-parse` and
`status` to record its `HEAD`); ChamPBH and StochasticInstantons were not read. Every scratch file was
in `agent04b/` of the session scratchpad; no scratch `.py` went under `runregistrykit/` or `docs/`.
Nothing pushed or tagged.

## The deliberate-breakage record

Each diff below is exactly as applied, against this commit's `stores.py` (blob `526b64d`) and
`fingerprint.py` (`8bbcae4`), made as deviation 17 says. A `bash` script, `agent04b/mut/replay.sh`,
replayed each from its diff file: `git apply --check`, `git apply`, `git apply -R --check`, the suite
(§3.1's command), `git apply -R`, and `git status --short` compared with the state before. All ten
checked both ways, and the status was the same after each. None is committed. The verdicts, and
every failing test (module `test_fingerprinter` unless named; a subtest's label in brackets or
parentheses):

| # | Mutation | The suite | Failing tests |
|---|---|---|---|
| (m1) | `_SHARDS_TABLE_UNREADABLE` reworded, `"its shards table was unreadable"` | `Ran 245 … FAILED (failures=2)` | FAIL `test_store_retire.TestWithoutFingerprint.test_an_unreadable_shards_table` (without_fingerprint=True), (without_fingerprint=False) |
| (m2) | `_find_references` taking the stores root as a target | `Ran 245 … FAILED (failures=5)` | FAIL `test_store_retire_references.TestTheStoresRootIsNotATarget`: `test_a_sidecar_that_is_not_a_tombstone_naming_the_root`, `test_the_same_sidecar_is_reported_for_a_field_naming_the_primary`, `test_three_stores_in_the_root_retired_in_turn`, `test_through_a_primary_that_is_reached_by_a_symlink`, `test_through_a_stores_root_that_is_a_symlink` |
| (m3) | `retire_store` recording `matched` without refusing a comparison's differences | `Ran 245 … FAILED (failures=2)` | FAIL `test_store_retire.TestRefusals.test_a_mismatch_in_problems_alone`, `test_a_row_changed_after_fingerprinting` |
| (m4) | §2.3's load removed | `Ran 245 … FAILED (failures=4, errors=9)` | `TestRetireLoadsTheFingerprinterFirst.test_retire_store_raises_the_config_error_and_changes_nothing`: ERROR [a module that exists nowhere], (dry_run=True), (without_fingerprint=True, dry_run=True); ERROR [the class], (without_fingerprint=True), (dry_run=True), (without_fingerprint=True, dry_run=True); FAIL [a module that exists nowhere] (without_fingerprint=True); FAIL the test itself (the store was retired: `read_sidecar(…).ok` false). FAIL `test_store_retire_without_fingerprint_exits_1_naming_the_config_file` [a module that exists nowhere], [the class]. ERROR `TestRetirePrecedence.test_the_fingerprinter_comes_before_the_plan` (without_fingerprint=False), (without_fingerprint=True) |
| (m5) | §2.3's load moved after the plan, into the flag branch's `try` | `Ran 245 … FAILED (failures=4, errors=9)` | the same thirteen as (m4) |
| (m6) | §2.4's class refusal removed | `Ran 245 … FAILED (failures=5, errors=3)` | FAIL `TestProtocolAndLoader.test_a_class_is_refused_and_an_instance_of_it_loads` [runregistrykit.fingerprint:DatastoreKitFingerprinter], [client_fingerprinter_…:Stub]; `TestRetireLoadsTheFingerprinterFirst.test_retire_store_raises_the_config_error_and_changes_nothing`: ERROR [the class], (dry_run=True), (without_fingerprint=True, dry_run=True); FAIL [the class] (without_fingerprint=True); FAIL the test itself; FAIL `test_store_retire_without_fingerprint_exits_1_naming_the_config_file` [the class] |
| (m7) | the agent's, of the deletion order: the tombstone written `retired` before the check that no listed file remains | `Ran 245 … FAILED (failures=1, errors=3)` | FAIL `test_store_retire.TestInterruption.test_I5_the_deletion_reports_success_and_leaves_a_listed_file`; ERROR `test_store_retire.TestInterruption.test_I6_the_completion_write_fails`, `test_I6t_the_completion_write_is_killed_and_leaves_its_tmp`, `test_a_listed_file_that_remains_with_no_primary` |
| (m8) | the agent's: the load before step 1 | `Ran 245 … FAILED (failures=6, errors=2)` | `TestRetirePrecedence`: FAIL `test_the_reason_comes_first`, `test_a_running_run_comes_first`, `test_a_completed_tombstone_comes_first`, each (without_fingerprint=False), (without_fingerprint=True); ERROR `test_a_completion_loads_no_fingerprinter` (without_fingerprint=False), (without_fingerprint=True) |
| (m9) | the agent's: the load after the plan, unwrapped | `Ran 245 … FAILED (errors=2)` | ERROR `TestRetirePrecedence.test_the_fingerprinter_comes_before_the_plan` (without_fingerprint=False), (without_fingerprint=True) |
| (m10) | the agent's: the load on the completion path too | `Ran 245 … FAILED (errors=2)` | ERROR `TestRetirePrecedence.test_a_completion_loads_no_fingerprinter` (without_fingerprint=False), (without_fingerprint=True) |

(m1) is what a rewording in DatastoreKit would leave: the refusal falls through to the plan's
generic one ("the plan of its files was refused"), which lacks "refused even under
--without-fingerprint" and "only by a person, outside the registry". (m8) also fails (v), because
the completion path passes through the load placed before step 1.

### The diffs

#### (m1) `_SHARDS_TABLE_UNREADABLE` reworded (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..81fb9bb 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1363,7 +1363,7 @@ def fingerprint_store(
 # remains, or a completed tombstone; and `store retire` again completes an incomplete one.
 
 # the text `ShardedPool._read_closed_store` gives a `shards` table it cannot read (prompt 01's log)
-_SHARDS_TABLE_UNREADABLE = "its shards table could not be read"
+_SHARDS_TABLE_UNREADABLE = "its shards table was unreadable"
 
 
 def _json_path(where: str, key) -> str:
```

#### (m2) `_find_references` taking the stores root as a target (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..66806ab 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1428,8 +1428,7 @@ def _find_references(
 
     targets = {os.path.realpath(p) for p in [primary, *planned]}
     directory = os.path.realpath(primary.parent)
-    if directory != os.path.realpath(stores_root):
-        targets.add(directory)
+    targets.add(directory)
     own = os.path.realpath(own)
     # the sidecar suffix, taken from `sidecar_path`, where alone the pattern is spelled
     suffix = sidecar_path(Path("x.sqlite")).name[len("x") :]
```

#### (m3) `retire_store` not refusing a comparison's differences (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..701640b 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1704,7 +1704,7 @@ def retire_store(
                     f"`--without-fingerprint` retires it and records this error"
                 ) from e
             differences = list(taken["comparison"])
-            if differences:
+            if False:
                 raise refuse(
                     f"its content does not match the fingerprint its sidecar records, taken "
                     f"{(recorded.get('taken') or {}).get('when')}: {len(differences)} "
```

#### (m4) §2.3's load removed (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..aae6f98 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1670,9 +1670,6 @@ def retire_store(
                 )
         new_fields = _copy.deepcopy(fields)
     else:
-        # the fingerprinter first: one that cannot be loaded is a refusal, never the reason a
-        # store cannot be fingerprinted
-        load_fingerprinter(client)
         resume = False
         try:
             planned = ShardedPool.closed_store_files(primary)
```

#### (m5) §2.3's load moved into the flag branch's `try` (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..9dd7128 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1670,9 +1670,6 @@ def retire_store(
                 )
         new_fields = _copy.deepcopy(fields)
     else:
-        # the fingerprinter first: one that cannot be loaded is a refusal, never the reason a
-        # store cannot be fingerprinted
-        load_fingerprinter(client)
         resume = False
         try:
             planned = ShardedPool.closed_store_files(primary)
@@ -1713,6 +1710,7 @@ def retire_store(
             condition = {"condition": "matched", "digest": recorded["digest"]}
         else:
             try:
+                load_fingerprinter(client)
                 fingerprint_store(
                     primary, write=False, runs_root=runs_root, client_root=client
                 )
```

#### (m6) §2.4's class refusal removed (`fingerprint.py`)

```diff
diff --git a/runregistrykit/fingerprint.py b/runregistrykit/fingerprint.py
index 8bbcae4..26c15dc 100644
--- a/runregistrykit/fingerprint.py
+++ b/runregistrykit/fingerprint.py
@@ -185,13 +185,6 @@ def load_fingerprinter(client) -> Fingerprinter:
                 f"{where}: {module_name} has no attribute {attribute!r} (no {part!r})"
             ) from None
 
-    # before the protocol check, which a class with the four methods passes
-    if isinstance(found, type):
-        raise ConfigError(
-            f"{where} is the class {found.__qualname__}, not an instance of it: name an "
-            f"instance, made in a module of the client's (for DatastoreKitFingerprinter, one "
-            f"made with the client's registry and its format number)"
-        )
     if not isinstance(found, Fingerprinter):
         raise ConfigError(
             f"{where} is {found!r}, which is not a Fingerprinter: it needs the methods take, "
```

#### (m7) the tombstone written `retired` before the check that no listed file remains (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..33a4019 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1808,6 +1808,11 @@ def retire_store(
                 primary, step, e, files, reading.path, client.root
             ) from e
 
+    new_fields = _copy.deepcopy(new_fields)
+    new_fields["retired"]["state"] = "retired"
+    new_fields["retired"]["completed"] = now_iso()
+    _update_sidecar(reading.path, new_fields, primary)
+
     step = "check that no listed file remains"
     remaining = _present(files, primary, client.root)
     unlisted = [str(p) for p in deleted if _repo_path(p, client.root) not in files]
```

#### (m8) the load before step 1 (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..05c8b6d 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1558,6 +1558,7 @@ def retire_store(
             f'Cannot retire "{primary}": {why}. Nothing was written or deleted'
         )
 
+    load_fingerprinter(client)
     # 1. the reason and the sidecar
     if not _nonempty_string(reason):
         raise refuse(
@@ -1670,9 +1671,6 @@ def retire_store(
                 )
         new_fields = _copy.deepcopy(fields)
     else:
-        # the fingerprinter first: one that cannot be loaded is a refusal, never the reason a
-        # store cannot be fingerprinted
-        load_fingerprinter(client)
         resume = False
         try:
             planned = ShardedPool.closed_store_files(primary)
```

#### (m9) the load after the plan, unwrapped (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..126b11d 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1670,9 +1670,6 @@ def retire_store(
                 )
         new_fields = _copy.deepcopy(fields)
     else:
-        # the fingerprinter first: one that cannot be loaded is a refusal, never the reason a
-        # store cannot be fingerprinted
-        load_fingerprinter(client)
         resume = False
         try:
             planned = ShardedPool.closed_store_files(primary)
@@ -1684,6 +1681,7 @@ def retire_store(
             planned = plan(True)
             resume = True
         files = [_repo_path(p, client.root) for p in planned]
+        load_fingerprinter(client)
 
         if not without_fingerprint:
             recorded = fields.get("fingerprint")
```

#### (m10) the load on the completion path too (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 526b64d..aae4af8 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1643,6 +1643,7 @@ def retire_store(
             raise plan_refusal(e) from e
 
     if completing:
+        load_fingerprinter(client)
         tombstone = _copy.deepcopy(fields["retired"])
         files = tombstone["files"]
         condition = tombstone["fingerprint"]
```

## Observations not acted on

- **`load_fingerprinter`'s docstring** lists its refusals ("none named; an import that fails …; a
  missing attribute; an object that is not a `Fingerprinter`") and does not name the class
  refusal. Left: §2.4 changes the module docstring's sentence and nothing else of the loader; a class
  is, as the config names it, not a fingerprinter. A one-line change for 05's prose.
- **The load's `ConfigError` does not end "Nothing was written or deleted"**, which `retire_store`'s
  docstring says every refusal does; the same holds for the D4 refusal since 04a (its log's
  observations). Left: the text is the loader's, which §2.3 has come through as itself; 05's prose.
- **By reading, not measured:** with the loader refusing a class, `Run.finish(…, fingerprint=True)`
  under a config naming the class now records the loader's `ConfigError` as `fingerprint_error`
  (from `fingerprint_store`'s load), not `take`'s `TypeError`, and `store fingerprint` refuses with
  it. No test of this prompt asserts it.
- **The ported modules carry SGK's prose** (deviation 9), recorded under
  `[02-the-ported-tests-name-sgk]` for 05; nothing is changed under rule 9.
- **The suite is now about 90 s** (deviation 8); the retire tests build and fingerprint a four-shard
  store per test, as SGK's did.

No §3 issue is opened: none of these is a defect in what 04b was asked to do, and each is the
prompt's rule, a ported line rule 9 keeps, or 05's prose.

## State handed to the next prompt

- **Every SGK test README §4 imports is ported**: 29 core, 76 shard-fixture, 29 fingerprint and 51
  retire tests; with the package's own 60 (`test_package_imports` 3, `test_client_root` 27,
  `test_fingerprinter` 30) the suite is **245**, about 90 s. 05's count starts there.
- **`store retire`** loads the client's fingerprinter on a first retirement after the reason, sidecar
  and in-use refusals and before the plan; a load failure is the loader's `ConfigError`, before
  anything is written, with the flag or not, in a dry run, and from the command (exit 1); the
  completion path loads none. `--without-fingerprint` records only a failure of the fingerprint
  itself. `load_fingerprinter` refuses a class.
- **`_SHARDS_TABLE_UNREADABLE`** (`stores.py:1365-1366`, used at `:1630` and `:1680`) is reached by
  `test_store_retire.TestWithoutFingerprint.test_an_unreadable_shards_table`, which (m1) fails; the
  issue stays open, its remedy a request to DatastoreKit.
- The board's §3 has four issues, their package lines at this commit recorded there;
  `docs/OPEN_ISSUES.md` counts 4. The prose 05 rewrites includes the ported modules' SGK citations
  (deviation 9) and the two docstring observations above.
- Not touched: `runregistrykit/__init__.py`, `__main__.py`, `client.py`, `pyproject.toml`,
  `CLAUDE.md`, `docs/extraction/`, `tests/__init__.py`, the fixtures; no client, DatastoreKit or
  RayPoolKit was edited or run; nothing installed; nothing pushed or tagged.
