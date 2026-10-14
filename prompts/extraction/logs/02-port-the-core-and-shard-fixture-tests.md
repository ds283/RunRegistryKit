# Log — prompt 02: port the core and shard-fixture tests

**Subject:** Port the core and shard-fixture tests, and extend the equivalence check
**Commit:** `8155445` (on `main`, after `1f9b5b0`)
**Date:** 2026-10-14
**Agent:** Claude Sonnet 5.5, dispatched by the orchestrator with its brief (the orchestrator's note
§0)
**Result:** **landed.** The 29 core and 76 shard-fixture tests are in `runregistrykit/tests/`, with
their two fixture modules, as SGK's files changed only by D-name (83 lines), D-fix (5) and D-fmt (12
package lines, 3 source lines, 3 hunks). The suite: **3 → 108**, `Ran 108 tests … OK`.
`compare_with_source.py` exits 0 and bites on 02's (a)–(g), on 01's (a)–(i) replayed, and the suite
catches (m1)–(m3). No stop condition was met. One issue opened (`[02-the-ported-tests-name-sgk]`),
four given package lines; `docs/OPEN_ISSUES.md` goes from 7 to 8.

## What shipped

| File | What |
|---|---|
| `runregistrykit/tests/test_run_registry.py` | SGK's blob `01c3ea3`, 711 lines; D-name on 31 lines |
| `runregistrykit/tests/store_fixtures.py` | blob `391f31f`, 223 lines; D-name 6, D-fix 2 |
| `runregistrykit/tests/test_store_sidecar.py` | blob `533d111`, 617 lines; D-name 15, D-fix 1 |
| `runregistrykit/tests/test_store_copy_move.py` | blob `4be78d9`, 601 lines, 610 after D-fmt; D-name 10, D-fix 1, D-fmt 3 source lines (12 package lines) |
| `runregistrykit/tests/test_store_command_line.py` | blob `6f111e2`, 183 lines; D-name 11 |
| `runregistrykit/tests/test_store_amend.py` | blob `8b7db11`, 641 lines; D-name 8, D-fix 1 |
| `runregistrykit/tests/test_store_amend_residuals.py` | blob `0c6e6a2`, 267 lines; D-name 2 |
| `runregistrykit/tests/shard_store_fixtures.py` | `StoreFixtures/shard_store_fixtures.py`, blob `1375949`, 168 lines (U4); no difference |
| `docs/extraction/compare_with_source.py` | extended: the eight rows *ported by 02*, the rule of prompt §2.4, `black` pinned, the docstring |
| `PROVENANCE.md` | the eight rows' fate (already "ported by 02"), D-fix and D-fmt beside D-name, the check's rule, `black` 25.1.0 |
| `CLAUDE.md` | the Tests bullet only |
| this log, `IMPLEMENTATION_STATE.md`, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` | the records |

Nothing else in `runregistrykit/` is new or changed: the three modules, `tests/__init__.py`,
`tests/test_package_imports.py` and `pyproject.toml` are as 01 left them.

**How the files were made.** Each was exported with `git -C SGK show a45aefc:<path>` into the
scratch directory (blob and length as the prompt's §2.2: all eight read as it says), then written by
a scratch script run with `python -I` (outside the repository) that applies D-fix, then D-name, to
the whole text and then `black.format_str(text, mode=black.Mode())`. `black --check runregistrykit
docs` then reports 14 files unchanged.

**The check, extended** (`docs/extraction/compare_with_source.py`). Its constants, frozen-tree check,
fates, walk and exit codes are as 01 made them. Changed:
- `PORTED = "ported by 02"`: the eight rows of §2.2 take it; the three *pending, 04* rows keep the
  `pending("04")` mechanism, and a pending file that is present still fails as PRESENT, NOT CHECKED
  (breakage (g));
- `compare_module` is the rule of prompt §2.4 for every checked row, 01's and 02's alike: T is the
  source with D-name and D-fix applied line by line (`renamed_source`: counts the lines each
  changed); the package must equal `black.format_str(T, mode=black.Mode())`; D-fmt is the opcodes
  between T and `black(T)` (counted in lines and in hunks, each hunk printed with its T and package
  lines); any line where the package differs from `black(T)` is printed, with its package line
  number, and fails; and no checked line may match `\bRunRegistry\b` or `\bStoreFixtures\b`. It names
  no line number;
- `black` is imported under the cannot-run guard (`require_black`): not importable, a version other
  than `25.1.0`, or `black` raising on T, each exits 2 with `CANNOT RUN: …` (the first two shown
  below);
- the docstring states the new rule, D-fix and D-fmt, why `black` is pinned, and that `black.Mode()`
  and the command line's `black` could differ in principle.

The two cannot-run paths, run once (not committed): `sys.modules["black"] = None` gives `CANNOT RUN:
black is not importable; this check needs black 25.1.0 (pip install black==25.1.0)`, exit 2; with
`black.__version__ = "25.0.0"`, `CANNOT RUN: black is 25.0.0; this check is pinned to black 25.1.0,
whose reflows it accepts`, exit 2.

## Deviations from the prompt

1. **(m2) fails more than the prompt names** (brief correction 1, found as the brief said). The
   prompt names `test_store_copy_move` and `test_store_amend.TestCopyAndMove`; the 4 failures and 8
   errors are in those and also in `test_store_sidecar.TestUnknownFieldsSurvive.test_an_a3_shaped_sidecar_through_adopt_copy_and_move`
   and `test_store_command_line.TestStoreCommands.test_show_create_adopt_copy_and_move` (every
   failing test is listed below). **STRUCTURALLY REQUIRED** (the measured behaviour).
2. **`black.Mode()` is not the command line's `black`** (brief correction 2). The check uses
   `black.Mode()`, as the prompt says; on all twelve files it gives the same output as `black` run
   at the root with `pyproject.toml`'s inferred `py312`, `py313` (§3.5's `black --check` is clean
   on the files as committed). No `[tool.black]` table was added. The docstring and `PROVENANCE.md`
   say the two could differ in principle. **IMPLEMENTATION CHOICE**, at the orchestrator's reading.
3. **The instances overlap in `test_store_copy_move.py`** (brief correction 3). The three source
   lines `black` reflows (`:73`, `:135`, `:211`) are three of that file's ten D-name lines as well as
   the three D-fmt instances; the accounting below lists each under both. No line needs both D-name
   and D-fix (measured: the check's D-name and D-fix lines are disjoint in every file).
   **IMPLEMENTATION CHOICE**, at the orchestrator's reading.
4. **D-fmt is counted from T to `black(T)`, not to the package** (brief recommendation 1). When the
   check passes the two are the same; in a breakage the count stays a property of the source (12, 3
   hunks) and every difference between `black(T)` and the package is reported once as UNCLASSIFIED.
   So unlike 01 a breakage does not move D-name, D-fix or D-fmt, and the failure lines say what is
   wrong. **IMPLEMENTATION CHOICE**, at the orchestrator's reading.
5. **`black` is imported under the cannot-run guard, exit 2** (brief recommendation 2); a `black`
   that raises on T is also exit 2. **IMPLEMENTATION CHOICE**, at the orchestrator's reading.
6. **The suite takes 13.6 to 14.2 s here**, not the prompt's 25–40 s (brief correction 5). Seen:
   `Ran 108 tests in 14.224s` and `Ran 108 tests in 13.634s`. Under the breakage replays 14 to 19 s
   (another session's unrelated test run was on the machine for part of it). **STRUCTURALLY
   REQUIRED** (the machine).
7. **The check's report gained lines.** For each checked file it now prints `D-name`, `D-fix`,
   `D-fmt`, `D-fmt hunks` and `identical` (lines unchanged by every class), then the instances; the
   summary line reads `12 checked (4 by 01, 8 by 02): D-name 106, D-fix 5, D-fmt 12 in 3 hunks; …`.
   The prompt fixes the counts, not the layout. **IMPLEMENTATION CHOICE.**
8. **(m3) is `amend_sidecar` no longer appending its `amend` history entry**
   (`stores.py:2173`). Two mutations tried first were not caught by any test: dropping the `bool`
   guard on `sidecar_format` (`stores.py:579`) and `_STORE_ID.fullmatch` → `.match` (`:589`, the sidecar reader's own `store_id` check); both
   leave the suite at 108 OK and are recorded below and under "Observations". The prompt leaves the
   choice to the agent. **IMPLEMENTATION CHOICE.**
9. **The breakage diffs were taken against the index**, with the eight ported files and the
   extended check staged (not committed) while they were made, so a diff's `index` line for those
   files is the blob `8155445` holds. Each was replayed and reversed as recorded with `git apply`
   in `bash`. **IMPLEMENTATION CHOICE.**
10. **01's (h) (the table row) applied unchanged**, with no re-recording: its context is the
    *not imported* `test_killed_handler.py` row, which 02 does not change. 01's (a)–(i) all applied
    as in 01's log. **IMPLEMENTATION CHOICE** (none made); recorded because the brief asked.

No difference between a ported file and `black(T)` fell outside D-name, D-fix and D-fmt; `black`
changed no line of 01's files. No stop condition (prompt §5) was met.

## Verification performed

**The source (G1, source side), re-read 2026-10-14.** SGK `HEAD` `14bcac0`, working tree clean;
`git ls-tree -r a45aefc -- RunRegistry/` has 25 rows; the blobs and lengths of the eight files are
§2.2's (`01c3ea3` 711, `391f31f` 223, `533d111` 617, `4be78d9` 601, `6f111e2` 183, `8b7db11` 641,
`0c6e6a2` 267, `1375949` 168). SGK was read only through `git -C`.

**The toolchain.** `venv/` as 01 left it; nothing installed. No Ray process before or after (`pgrep
-lf 'gcs_server|raylet|ray::|default_worker\.py'` empty, exit 1); `RAY_ADDRESS` unset; no `var/` at
the root.

**§3.1, the suite.** Before: `Ran 3 tests in 0.195s`, `OK`. After, `./venv/bin/python -m unittest
discover -s runregistrykit/tests -t .` from the root, output to a scratch file:

```
Ran 108 tests in 13.634s

OK
```

By module, counted by the loader (not `-v` lines): `test_package_imports` 3, `test_run_registry` 29,
`test_store_sidecar` 17, `test_store_copy_move` 27, `test_store_command_line` 2, `test_store_amend`
21, `test_store_amend_residuals` 9. By class:

```
108
test_package_imports 3
test_run_registry 29
test_store_amend 21
test_store_amend_residuals 9
test_store_command_line 2
test_store_copy_move 27
test_store_sidecar 17

test_package_imports TestPackageImports 3
test_run_registry TestCheckpoint 4
test_run_registry TestLedgerIsNotTheResultsStore 7
test_run_registry TestLister 2
test_run_registry TestLiveness 3
test_run_registry TestManifest 5
test_run_registry TestPackageProvenance 5
test_run_registry TestSelfMatch 1
test_run_registry TestStatus 2
test_store_amend TestAmend 1
test_store_amend TestCommandLine 2
test_store_amend TestCopyAndMove 2
test_store_amend TestHistoryRule 2
test_store_amend TestLiveA3Shape 1
test_store_amend TestRefusals 11
test_store_amend TestRemove 1
test_store_amend TestTwoAmendments 1
test_store_amend_residuals TestCommandLineTypeChange 1
test_store_amend_residuals TestMarkerShapedValue 1
test_store_amend_residuals TestStillRefusedWithTheTreeUnchanged 2
test_store_amend_residuals TestTypeStrictComparison 5
test_store_command_line TestImports 1
test_store_command_line TestStoreCommands 1
test_store_copy_move TestCopy 2
test_store_copy_move TestInterruption 13
test_store_copy_move TestMove 1
test_store_copy_move TestRefusals 11
test_store_sidecar TestAdopt 4
test_store_sidecar TestCreate 3
test_store_sidecar TestName 2
test_store_sidecar TestReader 4
test_store_sidecar TestRunManifests 3
test_store_sidecar TestUnknownFieldsSurvive 1
```

(The first line is the total; the module counts, a blank line, then module and class and the count.)

**§3.2, the check.** `./venv/bin/python docs/extraction/compare_with_source.py`, exit 0; its whole
output:

```
Equivalence check: runregistrykit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at a45aefc702de643c330372dd6d2d983f38bb8eed

RunRegistry/ at the import commit: 25 rows; the table: 25 rows
  equal, path for path and blob for blob (25 rows)
StoreFixtures/shard_store_fixtures.py at the import commit: blob 1375949aacde2263de991785055cd7dfabc57251 (as the table says)

runregistrykit/__init__.py  <-  RunRegistry/__init__.py  [imported by 01]
  D-name: 6
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 704
  unclassified: 0
    D-name source :7
        - `<stem>.manifest.json` sidecars (`RunRegistry.stores`), because the user decided that managing
        + `<stem>.manifest.json` sidecars (`runregistrykit.stores`), because the user decided that managing
    D-name source :31
        -     run = RunRegistry.begin(
        +     run = runregistrykit.begin(
    D-name source :43
        - `python -m RunRegistry list` prints every run, newest first, and says loudly which of them claim
        + `python -m runregistrykit list` prints every run, newest first, and says loudly which of them claim
    D-name source :371
        -         store (`RunRegistry.stores.fingerprint_store`, read-only, with this run as `taken_by` so
        +         store (`runregistrykit.stores.fingerprint_store`, read-only, with this run as `taken_by` so
    D-name source :581
        -     When `results` has a problem-free registry sidecar beside it (`RunRegistry.stores`), it holds
        +     When `results` has a problem-free registry sidecar beside it (`runregistrykit.stores`), it holds
    D-name source :587
        -     (`RunRegistry.stores.retire_store`) is refused before the run directory is created, because a
        +     (`runregistrykit.stores.retire_store`) is refused before the run directory is created, because a

runregistrykit/__main__.py  <-  RunRegistry/__main__.py  [imported by 01]
  D-name: 4
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 511
  unclassified: 0
    D-name source :1
        - """`python -m RunRegistry list` — one line per run, newest first.
        + """`python -m runregistrykit list` — one line per run, newest first.
    D-name source :6
        - `python -m RunRegistry store {show,create,adopt,copy,move,fingerprint,retire,amend}` manages a
        + `python -m runregistrykit store {show,create,adopt,copy,move,fingerprint,retire,amend}` manages a
    D-name source :7
        - datastore and its `<stem>.manifest.json` sidecar (`RunRegistry.stores`). `show` is read-only.
        + datastore and its `<stem>.manifest.json` sidecar (`runregistrykit.stores`). `show` is read-only.
    D-name source :373
        -     parser = argparse.ArgumentParser(prog="RunRegistry", description=__doc__)
        +     parser = argparse.ArgumentParser(prog="runregistrykit", description=__doc__)

runregistrykit/stores.py  <-  RunRegistry/stores.py  [imported by 01]
  D-name: 13
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 2172
  unclassified: 0
    D-name source :115
        - like `import RunRegistry`, loads neither `ray` nor `sqlalchemy`.
        + like `import runregistrykit`, loads neither `ray` nor `sqlalchemy`.
    D-name source :197
        - # (`RunRegistry/tests/data/full_store_fingerprint*.json`; `test_store_fingerprint.GOLDEN` names the
        + # (`runregistrykit/tests/data/full_store_fingerprint*.json`; `test_store_fingerprint.GOLDEN` names the
    D-name source :544
        -             f'. Run `python -m RunRegistry store retire "{primary}" --reason <the recorded '
        +             f'. Run `python -m runregistrykit store retire "{primary}" --reason <the recorded '
    D-name source :1025
        -             f"registry sidecar ({why}). Run `python -m RunRegistry store create` or `store "
        +             f"registry sidecar ({why}). Run `python -m runregistrykit store create` or `store "
    D-name source :1196
        -     # here, not at module scope: that module imports sqlalchemy, and `import RunRegistry` must not
        +     # here, not at module scope: that module imports sqlalchemy, and `import runregistrykit` must not
    D-name source :1455
        -        that `import RunRegistry` loads neither ray nor sqlalchemy;
        +        that `import runregistrykit` loads neither ray nor sqlalchemy;
    D-name source :1538
        -                 f"RunRegistry store create` or `store adopt` on it first; a fingerprint never "
        +                 f"runregistrykit store create` or `store adopt` on it first; a fingerprint never "
    D-name source :1694
        -         f"[{present}].{left} Once the failure is understood, run `python -m RunRegistry store "
        +         f"[{present}].{left} Once the failure is understood, run `python -m runregistrykit store "
    D-name source :1758
        -             f"({_sidecar_refusal(reading)}). Run `python -m RunRegistry store create` or `store "
        +             f"({_sidecar_refusal(reading)}). Run `python -m runregistrykit store create` or `store "
    D-name source :1810
        -             f'it is ended, `python -m RunRegistry store fingerprint "{primary}" --write` records '
        +             f'it is ended, `python -m runregistrykit store fingerprint "{primary}" --write` records '
    D-name source :1876
        -                     f'retirement deleted. Run `python -m RunRegistry store fingerprint "{primary}" '
        +                     f'retirement deleted. Run `python -m runregistrykit store fingerprint "{primary}" '
    D-name source :1907
        -                     f'`python -m RunRegistry store fingerprint "{primary}" --write`, then `store '
        +                     f'`python -m runregistrykit store fingerprint "{primary}" --write`, then `store '
    D-name source :2119
        -             f"({_sidecar_refusal(reading)}). Run `python -m RunRegistry store create` or `store "
        +             f"({_sidecar_refusal(reading)}). Run `python -m runregistrykit store create` or `store "

runregistrykit/tests/__init__.py  <-  RunRegistry/tests/__init__.py  [imported by 01]
  D-name: 0
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 0
  unclassified: 0

runregistrykit/tests/store_fixtures.py  <-  RunRegistry/tests/store_fixtures.py  [ported by 02]
  D-name: 6
  D-fix: 2
  D-fmt: 0
  D-fmt hunks: 0
  identical: 215
  unclassified: 0
    D-name source :15
        - import RunRegistry
        + import runregistrykit
    D-name source :16
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :17
        - from RunRegistry.tests.test_run_registry import RegistryTestCase
        + from runregistrykit.tests.test_run_registry import RegistryTestCase
    D-name source :143
        -     def a_running_run(self, slug: str, results) -> "RunRegistry.Run":
        +     def a_running_run(self, slug: str, results) -> "runregistrykit.Run":
    D-name source :146
        -     def a_stale_run(self, slug: str, results) -> "RunRegistry.Run":
        +     def a_stale_run(self, slug: str, results) -> "runregistrykit.Run":
    D-name source :181
        -             reading.fields["history"][-1]["to"], RunRegistry._repo_path(primary)
        +             reading.fields["history"][-1]["to"], runregistrykit._repo_path(primary)
    D-fix source :4
        - built in one temporary directory: stores with `StoreFixtures/shard_store_fixtures.py` (a real
        + built in one temporary directory: stores with `runregistrykit/tests/shard_store_fixtures.py` (a real
    D-fix source :20
        - from StoreFixtures.shard_store_fixtures import (
        + from runregistrykit.tests.shard_store_fixtures import (

runregistrykit/tests/test_run_registry.py  <-  RunRegistry/tests/test_run_registry.py  [ported by 02]
  D-name: 31
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 680
  unclassified: 0
    D-name source :1
        - """Tests for `RunRegistry`. No Ray, no datastore, no network; every run directory these build is
        + """Tests for `runregistrykit`. No Ray, no datastore, no network; every run directory these build is
    D-name source :19
        - import RunRegistry
        + import runregistrykit
    D-name source :21
        - REPO_ROOT = RunRegistry.REPO_ROOT
        + REPO_ROOT = runregistrykit.REPO_ROOT
    D-name source :31
        - import RunRegistry
        + import runregistrykit
    D-name source :34
        - status = RunRegistry.read_json(os.path.join(run_dir, "status.json"))
        + status = runregistrykit.read_json(os.path.join(run_dir, "status.json"))
    D-name source :80
        -             "verdict": RunRegistry.liveness(status, stale_after=3600.0),
        +             "verdict": runregistrykit.liveness(status, stale_after=3600.0),
    D-name source :99
        - import RunRegistry
        + import runregistrykit
    D-name source :101
        - RunRegistry.begin(
        + runregistrykit.begin(
    D-name source :124
        -         return RunRegistry.begin(
        +         return runregistrykit.begin(
    D-name source :133
        -             RunRegistry.pid_alive(corpse.pid),
        +             runregistrykit.pid_alive(corpse.pid),
    D-name source :239
        -         manifest = RunRegistry.read_json(os.path.join(path, "manifest.json"))
        +         manifest = runregistrykit.read_json(os.path.join(path, "manifest.json"))
    D-name source :243
        -         status = RunRegistry.read_json(os.path.join(path, "status.json"))
        +         status = runregistrykit.read_json(os.path.join(path, "status.json"))
    D-name source :271
        -             run.manifest["script_sha256"], RunRegistry.script_sha256(__file__)
        +             run.manifest["script_sha256"], runregistrykit.script_sha256(__file__)
    D-name source :282
        -             set(run.manifest["packages"]), set(RunRegistry.RECORDED_DISTRIBUTIONS)
        +             set(run.manifest["packages"]), set(runregistrykit.RECORDED_DISTRIBUTIONS)
    D-name source :284
        -         self.assertEqual(run.manifest["packages"], RunRegistry.package_provenance())
        +         self.assertEqual(run.manifest["packages"], runregistrykit.package_provenance())
    D-name source :285
        -         on_disk = RunRegistry.read_json(run.manifest_path)
        +         on_disk = runregistrykit.read_json(run.manifest_path)
    D-name source :286
        -         self.assertEqual(on_disk["packages"], RunRegistry.package_provenance())
        +         self.assertEqual(on_disk["packages"], runregistrykit.package_provenance())
    D-name source :307
        -         name the module calls (`RunRegistry.importlib.metadata.distribution`, which is the same
        +         name the module calls (`runregistrykit.importlib.metadata.distribution`, which is the same
    D-name source :317
        -             RunRegistry.importlib.metadata, "distribution", distribution
        +             runregistrykit.importlib.metadata, "distribution", distribution
    D-name source :319
        -             return RunRegistry.package_provenance()
        +             return runregistrykit.package_provenance()
    D-name source :395
        -             RunRegistry.RECORDED_DISTRIBUTIONS, ("datastorekit", "raypoolkit")
        +             runregistrykit.RECORDED_DISTRIBUTIONS, ("datastorekit", "raypoolkit")
    D-name source :421
        -             "recorded": RunRegistry.now_iso(),
        +             "recorded": runregistrykit.now_iso(),
    D-name source :574
        -             RunRegistry.read_json(run.manifest_path)["results"],
        +             runregistrykit.read_json(run.manifest_path)["results"],
    D-name source :638
        -         self.assertLess(RunRegistry.heartbeat_age(status), 60.0)
        +         self.assertLess(runregistrykit.heartbeat_age(status), 60.0)
    D-name source :639
        -         self.assertEqual(RunRegistry.liveness(status, stale_after=3600.0), "stale")
        +         self.assertEqual(runregistrykit.liveness(status, stale_after=3600.0), "stale")
    D-name source :644
        -         self.assertTrue(RunRegistry.pid_alive(status["pid"]))
        +         self.assertTrue(runregistrykit.pid_alive(status["pid"]))
    D-name source :645
        -         self.assertEqual(RunRegistry.liveness(status, stale_after=1e9), "alive")
        +         self.assertEqual(runregistrykit.liveness(status, stale_after=1e9), "alive")
    D-name source :646
        -         self.assertEqual(RunRegistry.liveness(status, stale_after=-1.0), "stale")
        +         self.assertEqual(runregistrykit.liveness(status, stale_after=-1.0), "stale")
    D-name source :652
        -             RunRegistry.liveness(run.status(), stale_after=1e9), "finished"
        +             runregistrykit.liveness(run.status(), stale_after=1e9), "finished"
    D-name source :668
        -         entries = RunRegistry.list_runs(root=self.root)
        +         entries = runregistrykit.list_runs(root=self.root)
    D-name source :681
        -             [sys.executable, "-m", "RunRegistry", "list", "--root", self.root],
        +             [sys.executable, "-m", "runregistrykit", "list", "--root", self.root],

runregistrykit/tests/test_store_sidecar.py  <-  RunRegistry/tests/test_store_sidecar.py  [ported by 02]
  D-name: 15
  D-fix: 1
  D-fmt: 0
  D-fmt hunks: 0
  identical: 601
  unclassified: 0
    D-name source :6
        - and one of them names a different store from the one it sits beside. `RunRegistry.stores` now
        + and one of them names a different store from the one it sits beside. `runregistrykit.stores` now
    D-name source :17
        - import RunRegistry
        + import runregistrykit
    D-name source :18
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :19
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :51
        -         package = Path(RunRegistry.__file__).parent
        +         package = Path(runregistrykit.__file__).parent
    D-name source :287
        -         self.assertEqual(entry["to"], RunRegistry._repo_path(primary))
        +         self.assertEqual(entry["to"], runregistrykit._repo_path(primary))
    D-name source :369
        -         self.assertEqual(entry["to"], RunRegistry._repo_path(primary))
        +         self.assertEqual(entry["to"], runregistrykit._repo_path(primary))
    D-name source :539
        -             RunRegistry.read_json(run.manifest_path)["results_store_id"],
        +             runregistrykit.read_json(run.manifest_path)["results_store_id"],
    D-name source :566
        -                 manifest = RunRegistry.read_json(run.manifest_path)
        +                 manifest = runregistrykit.read_json(run.manifest_path)
    D-name source :588
        -             "created": RunRegistry.now_iso(),
        +             "created": runregistrykit.now_iso(),
    D-name source :592
        -         RunRegistry.write_json_atomic(os.path.join(old, "manifest.json"), manifest)
        +         runregistrykit.write_json_atomic(os.path.join(old, "manifest.json"), manifest)
    D-name source :593
        -         RunRegistry.write_json_atomic(
        +         runregistrykit.write_json_atomic(
    D-name source :598
        -                 "heartbeat": RunRegistry.now_iso(),
        +                 "heartbeat": runregistrykit.now_iso(),
    D-name source :601
        -         (entry,) = RunRegistry.list_runs(root=self.root)
        +         (entry,) = runregistrykit.list_runs(root=self.root)
    D-name source :604
        -         self.assertEqual(RunRegistry.Run(old).results_path, str(primary))
        +         self.assertEqual(runregistrykit.Run(old).results_path, str(primary))
    D-fix source :28
        - from StoreFixtures.shard_store_fixtures import tree_state, write_placeholder
        + from runregistrykit.tests.shard_store_fixtures import tree_state, write_placeholder

runregistrykit/tests/test_store_copy_move.py  <-  RunRegistry/tests/test_store_copy_move.py  [ported by 02]
  D-name: 10
  D-fix: 1
  D-fmt: 12
  D-fmt hunks: 3
  identical: 590
  unclassified: 0
    D-name source :5
        - its sidecar. `RunRegistry.stores.copy_store` / `move_store` call them, then carry the sidecar: a
        + its sidecar. `runregistrykit.stores.copy_store` / `move_store` call them, then carry the sidecar: a
    D-name source :21
        - import RunRegistry
        + import runregistrykit
    D-name source :22
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :23
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :73
        -             {"store_id": source["store_id"], "datastore": RunRegistry._repo_path(src)},
        +             {"store_id": source["store_id"], "datastore": runregistrykit._repo_path(src)},
    D-name source :78
        -         self.assertEqual(entry["from"], RunRegistry._repo_path(src))
        +         self.assertEqual(entry["from"], runregistrykit._repo_path(src))
    D-name source :79
        -         self.assertEqual(entry["to"], RunRegistry._repo_path(dst))
        +         self.assertEqual(entry["to"], runregistrykit._repo_path(dst))
    D-name source :110
        -             third["copied_from"]["datastore"], RunRegistry._repo_path(middle)
        +             third["copied_from"]["datastore"], runregistrykit._repo_path(middle)
    D-name source :135
        -                     ("move", RunRegistry._repo_path(src), RunRegistry._repo_path(dst)),
        +                     ("move", runregistrykit._repo_path(src), runregistrykit._repo_path(dst)),
    D-name source :211
        -         self.assertEqual(RunRegistry.list_runs(root=self.root)[0]["liveness"], "stale")
        +         self.assertEqual(runregistrykit.list_runs(root=self.root)[0]["liveness"], "stale")
    D-fix source :32
        - from StoreFixtures.shard_store_fixtures import tree_state
        + from runregistrykit.tests.shard_store_fixtures import tree_state
    D-fmt source :73-73 -> package :73-76
        -             {"store_id": source["store_id"], "datastore": runregistrykit._repo_path(src)},
        +             {
        +                 "store_id": source["store_id"],
        +                 "datastore": runregistrykit._repo_path(src),
        +             },
    D-fmt source :135-135 -> package :138-142
        -                     ("move", runregistrykit._repo_path(src), runregistrykit._repo_path(dst)),
        +                     (
        +                         "move",
        +                         runregistrykit._repo_path(src),
        +                         runregistrykit._repo_path(dst),
        +                     ),
    D-fmt source :211-211 -> package :218-220
        -         self.assertEqual(runregistrykit.list_runs(root=self.root)[0]["liveness"], "stale")
        +         self.assertEqual(
        +             runregistrykit.list_runs(root=self.root)[0]["liveness"], "stale"
        +         )

runregistrykit/tests/test_store_command_line.py  <-  RunRegistry/tests/test_store_command_line.py  [ported by 02]
  D-name: 11
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 172
  unclassified: 0
    D-name source :1
        - """`python -m RunRegistry store …`, and what importing the registry loads.
        + """`python -m runregistrykit store …`, and what importing the registry loads.
    D-name source :5
        - RunRegistry` does (`runpy.run_module("RunRegistry", run_name="__main__", alter_sys=True)`), and
        + runregistrykit` does (`runpy.run_module("runregistrykit", run_name="__main__", alter_sys=True)`), and
    D-name source :16
        - import RunRegistry
        + import runregistrykit
    D-name source :17
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :18
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :25
        - REPO_ROOT = RunRegistry.REPO_ROOT
        + REPO_ROOT = runregistrykit.REPO_ROOT
    D-name source :30
        - sys.argv = ["RunRegistry"] + sys.argv[1:]
        + sys.argv = ["runregistrykit"] + sys.argv[1:]
    D-name source :33
        -     runpy.run_module("RunRegistry", run_name="__main__", alter_sys=True)
        +     runpy.run_module("runregistrykit", run_name="__main__", alter_sys=True)
    D-name source :47
        - import RunRegistry
        + import runregistrykit
    D-name source :48
        - import RunRegistry.stores
        + import runregistrykit.stores
    D-name source :55
        -         """Run ``python -m RunRegistry *argv`` in a child; return (report, stdout, stderr)."""
        +         """Run ``python -m runregistrykit *argv`` in a child; return (report, stdout, stderr)."""

runregistrykit/tests/test_store_amend.py  <-  RunRegistry/tests/test_store_amend.py  [ported by 02]
  D-name: 8
  D-fix: 1
  D-fmt: 0
  D-fmt hunks: 0
  identical: 632
  unclassified: 0
    D-name source :2
        - `RunRegistry.stores.amend_sidecar`, the `amend` history entry and its markers, the D5 guards, and
        + `runregistrykit.stores.amend_sidecar`, the `amend` history entry and its markers, the D5 guards, and
    D-name source :3
        - `python -m RunRegistry store amend`.
        + `python -m runregistrykit store amend`.
    D-name source :26
        - import RunRegistry
        + import runregistrykit
    D-name source :27
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :28
        - from RunRegistry.stores import KNOWN_FIELDS, amend_sidecar
        + from runregistrykit.stores import KNOWN_FIELDS, amend_sidecar
    D-name source :29
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :35
        - from RunRegistry.tests.test_store_command_line import (
        + from runregistrykit.tests.test_store_command_line import (
    D-name source :42
        - _repo_path = RunRegistry._repo_path
        + _repo_path = runregistrykit._repo_path
    D-fix source :15
        - Stores are the lightweight placeholder fixture (`StoreFixtures.shard_store_fixtures`), because
        + Stores are the lightweight placeholder fixture (`runregistrykit.tests.shard_store_fixtures`), because

runregistrykit/tests/test_store_amend_residuals.py  <-  RunRegistry/tests/test_store_amend_residuals.py  [ported by 02]
  D-name: 2
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 265
  unclassified: 0
    D-name source :21
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :22
        - from RunRegistry.tests.test_store_amend import AmendTestCase, REASON
        + from runregistrykit.tests.test_store_amend import AmendTestCase, REASON

runregistrykit/tests/shard_store_fixtures.py  <-  StoreFixtures/shard_store_fixtures.py  [ported by 02]
  D-name: 0
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 168
  unclassified: 0

Pending, ported by a later prompt: 3
  pending, 04: runregistrykit/tests/test_store_retire.py  <-  RunRegistry/tests/test_store_retire.py
  pending, 04: runregistrykit/tests/test_store_retire_references.py  <-  RunRegistry/tests/test_store_retire_references.py
  pending, 04: runregistrykit/tests/test_store_fingerprint.py  <-  RunRegistry/tests/test_store_fingerprint.py

Not imported, and absent from runregistrykit/: 11 of 11

Files with no source (declared): 1
  runregistrykit/tests/test_package_imports.py: present (01 §2.7: the import test)

Undeclared files under runregistrykit/: 0

Summary: 12 checked (4 by 01, 8 by 02): D-name 106, D-fix 5, D-fmt 12 in 3 hunks; 3 pending; 11 not imported and absent; 1 declared new
RESULT: OK
```

The counts are the prompt's: 25 rows and the fixture blob equal; 12 files checked (4 by 01, 8 by
02); D-name 106 (01's 6, 13, 4, 0 and 02's 31, 6, 15, 10, 11, 8, 2, 0); D-fix 5; D-fmt 12 package
lines in 3 hunks, all in `test_store_copy_move.py`, 0 elsewhere; 3 pending (04); 11 not imported and
absent; 1 declared new file. Nothing differs from the prompt's counts.

**The accounting of every instance** (README §5 rule 9; the check's report above lists each line):
- **D-name, 83 lines in the ported tests:** 31, 6, 15, 10, 11, 8, 2, 0 = 83. They are the imports
  (`import runregistrykit`, `from runregistrykit.tests.store_fixtures import …`), the
  `runregistrykit.<name>` references, `runpy.run_module("runregistrykit", …)` and `sys.argv =
  ["runregistrykit"] + …` (`test_store_command_line.py:30, 33`), `-m runregistrykit` in the child
  processes, and docstrings and comments. With 01's 23, 106 in all.
- **D-fix, 5 lines:** the three imports (`store_fixtures.py:20`, `test_store_sidecar.py:28`,
  `test_store_copy_move.py:32`) and the two docstrings (`store_fixtures.py:4`,
  `test_store_amend.py:15`).
- **D-fmt, 3 source lines, 12 package lines, 3 hunks, all in `test_store_copy_move.py`:** source
  `:73` becomes package `:73-76` (a dict split, a trailing comma added at `:75`), `:135` becomes
  `:138-142`, `:211` becomes `:218-220`; 601 lines become 610. Those three source lines are three of
  that file's 10 D-name lines (deviation 3).

**§3.3, the suite writes nothing outside its temporary directories.** `git status --short
--ignored` before and after a run is the same but for `__pycache__/` (compared before and after the
final run, and before and after the first run of the ported suite): `runregistrykit.egg-info/`,
`runregistrykit/__pycache__/` (and now `runregistrykit/tests/__pycache__/`), `venv/`. No `var/`
appeared. No Ray process was up before or after, and `RAY_ADDRESS` was unset: the suite starts no
Ray. Without `.git`, the orchestrator measured two failures, the 40-character `git_head`
assertions (`test_run_registry.py:273`, `test_store_sidecar.py:288`); not repeated here.

**§3.5.** `./venv/bin/black --check runregistrykit docs`: "All done! … 14 files would be left
unchanged."

## The deliberate-breakage record

Each diff is exactly as applied, to the tree of `8155445`, by a script that checked it with `git
apply --check`, applied it, confirmed `git apply -R --check`, ran the check and the suite, reversed
it with `git apply -R` and confirmed `git status --short` was as before. All were replayed in
`bash`. None is committed. For (g) of 01, the file is new, so `-R` removes it.

### 02's breakages (prompt §2.4 (a)–(g))

| # | Breakage | The check | The suite |
|---|---|---|---|
| (a) | `stale_after=3601.0`, `test_run_registry.py:639` | exit 1: `DIFFERS FROM black(T)`, `black(T) line :639` / `package :639` | 108 **OK**: the suite does not notice |
| (b) | `black`'s trailing comma at `test_store_copy_move.py:75` removed | exit 1: `black(T) line :75` / `package :75` | 108 OK |
| (c) | fixture import made relative (`:32`) | exit 1: `black(T) line :32` / `package :32` | 108 OK |
| (d) | `store_fixtures.py:4` reverted to `StoreFixtures/…` | exit 1: `DIFFERS FROM black(T)` at `:4`, and `NOT RENAMED runregistrykit/tests/store_fixtures.py:4 still has the word StoreFixtures` | 108 OK |
| (e) | `KEY_TYPE = "wavenumbers"`, `shard_store_fixtures.py:25` | exit 1: `black(T) line :25` / `package :25` | 108 **OK**: only the check sees it |
| (f) | `test_it_does_not_open_the_primary` deleted from `test_store_sidecar.py` | exit 1: seven `black(T)` lines `:295-301` absent from the package | **Ran 107 tests, OK** |
| (g) | `test_store_amend_residuals.py` set back to *pending, 02* | exit 1: `PRESENT, NOT CHECKED: runregistrykit/tests/test_store_amend_residuals.py (pending, 02, …)`; summary `11 checked (4 by 01, 7 by 02): D-name 104` | 108 OK |

In (a)–(f) the summary line stays `D-name 106, D-fix 5, D-fmt 12 in 3 hunks`: the counts are the
source's, not the package's (deviation 4).

### (h) 01's (a)–(i), replayed from 01's log against the extended check

The diffs are 01's, as they stand in `logs/01-import-the-registry.md`; each applied as recorded. The
check's output differs from 01's log, as the brief said it would.

| # | Breakage | The check | The suite |
|---|---|---|---|
| (a) | `DEFAULT_STALE_AFTER = 901.0` | exit 1: `black(T) line :65` / `package :65` | 108 OK |
| (b) | extra `import os` in `__main__.py` | exit 1: `package :26, not in black(T)` | 108 OK |
| (c) | `stores.py:198` deleted | exit 1: `black(T) line :198, absent from the package` (one difference, not three; D-name stays 106) | 108 OK |
| (d) | `prog="RunRegistryKit"` | exit 1: `black(T) line :373` / `package :373` | **FAIL**, 1 failure: `test_package_imports.TestPackageImports.test_command_line_answers_to_its_name` |
| (e) | `"var", "run"` on `DEFAULT_ROOT` | exit 1: `black(T) line :58` / `package :58` | 108 OK |
| (f) | "oldest first" on `__main__.py:1` | exit 1: `black(T) line :1` / `package :1` | 108 OK |
| (g) | undeclared `runregistrykit/extra.py` | exit 1: `NOT DECLARED: runregistrykit/extra.py` | 108 OK |
| (h) | wrong blob for `test_killed_handler.py` in the table | exit 1: `FROZEN TREE: RunRegistry/tests/test_killed_handler.py is blob 213f2a8…8b at the import commit, the table says 213f2a8…8c` | 108 OK |
| (i) | `stores.py:544` left unrenamed | exit 1: `black(T) line :544` / `package :544`, and `NOT RENAMED runregistrykit/stores.py:544 still has the word RunRegistry` | 108 OK |

### (m1)–(m3), the tests catch behaviour (prompt §2.5)

Each applied to the package, the suite run, reverted.

- **(m1)** `RECORDED_DISTRIBUTIONS = ("datastorekit",)`: `Ran 108 … FAILED (failures=2, errors=1)`, all
  in `test_run_registry.TestPackageProvenance`: FAIL `test_the_recorded_names_are_the_two_packages`,
  FAIL `test_a_distribution_not_installed_is_none`, ERROR `test_a_vcs_install_records_its_commit_and_tag`.
- **(m2)** `_history_entry("copied", …)`: `Ran 108 … FAILED (failures=4, errors=8)`. ERROR
  `test_store_amend.TestCopyAndMove.test_copy_carries_an_amended_field_and_its_entry`; ERROR
  `test_store_copy_move.TestCopy.test_a_copy_of_a_copy_names_its_immediate_parent`; ERROR
  `test_store_copy_move.TestCopy.test_the_destination_is_a_new_store_and_the_source_is_untouched`; ERROR
  `test_store_copy_move.TestInterruption.test_C5_complete` ×3 subtests; ERROR
  `test_store_copy_move.TestRefusals.test_a_finished_run_does_not_refuse`; ERROR
  `test_store_sidecar.TestUnknownFieldsSurvive.test_an_a3_shaped_sidecar_through_adopt_copy_and_move`;
  FAIL `test_store_command_line.TestStoreCommands.test_show_create_adopt_copy_and_move`; FAIL
  `test_store_copy_move.TestInterruption.test_C4_the_sidecar_is_written_to_its_tmp_name_and_the_replace_fails`
  ×3 subtests.
- **(m3)** `amend_sidecar` without its `amend` history entry: `Ran 108 … FAILED (failures=6,
  errors=9)`. ERROR `test_store_amend.TestRemove.test_remove_an_unknown_field`; ERROR
  `test_store_amend_residuals.TestMarkerShapedValue.test_add_replace_remove_and_read_back` ×3 subtests
  (add, replace, remove); ERROR `test_store_amend_residuals.TestTypeStrictComparison` `test_1_to_1_0`,
  `test_1_to_true`, `test_dict_value_1_to_true`, `test_list_value_1_to_true`, `test_true_to_1`; FAIL
  `test_store_amend.TestAmend.test_replace_an_unknown_field`; FAIL
  `test_store_amend.TestCopyAndMove.test_copy_carries_an_amended_field_and_its_entry` and
  `test_move_carries_an_amended_field_and_its_entry`; FAIL
  `test_store_amend.TestLiveA3Shape.test_amend_backup_as_prompt_05_will`; FAIL
  `test_store_amend.TestTwoAmendments.test_two_amendments_of_one_field_read_back_as_a_sequence`; FAIL
  `test_store_amend_residuals.TestMarkerShapedValue.test_add_replace_remove_and_read_back` (the
  `read back` subtest).
- **Not caught, tried for (m3):** dropping the `bool` guard on `sidecar_format`
  (`isinstance(fmt, bool) or …`) and `_STORE_ID.fullmatch` → `.match`: both 108 OK.

### The diffs

#### (a) `stale_after=3601.0` at `test_run_registry.py:639`

```diff
diff --git a/runregistrykit/tests/test_run_registry.py b/runregistrykit/tests/test_run_registry.py
index 37de925..0497701 100644
--- a/runregistrykit/tests/test_run_registry.py
+++ b/runregistrykit/tests/test_run_registry.py
@@ -636,7 +636,7 @@ class TestLiveness(RegistryTestCase):
         self.assertEqual(status["pid"], dead)
         # The heartbeat is fresh, so only kill -0 can tell, which is the point.
         self.assertLess(runregistrykit.heartbeat_age(status), 60.0)
-        self.assertEqual(runregistrykit.liveness(status, stale_after=3600.0), "stale")
+        self.assertEqual(runregistrykit.liveness(status, stale_after=3601.0), "stale")
 
     def test_a_live_process_with_an_old_heartbeat_is_stale(self):
         run = self.begin()  # pid is this process, which is certainly alive
```

#### (b) the trailing comma `black` added at `test_store_copy_move.py:75` removed

```diff
diff --git a/runregistrykit/tests/test_store_copy_move.py b/runregistrykit/tests/test_store_copy_move.py
index 36e9cdb..7d96f5d 100644
--- a/runregistrykit/tests/test_store_copy_move.py
+++ b/runregistrykit/tests/test_store_copy_move.py
@@ -72,7 +72,7 @@ class TestCopy(StoreTestCase):
             fields["copied_from"],
             {
                 "store_id": source["store_id"],
-                "datastore": runregistrykit._repo_path(src),
+                "datastore": runregistrykit._repo_path(src)
             },
         )
         self.assertEqual(fields["history"][:-1], source["history"])
```

#### (c) `test_store_copy_move.py`'s fixture import made relative

```diff
diff --git a/runregistrykit/tests/test_store_copy_move.py b/runregistrykit/tests/test_store_copy_move.py
index 36e9cdb..f7a4808 100644
--- a/runregistrykit/tests/test_store_copy_move.py
+++ b/runregistrykit/tests/test_store_copy_move.py
@@ -29,7 +29,7 @@ from runregistrykit.tests.store_fixtures import (
 
 from datastorekit.SQL.ShardedPool import ShardedPool
 from datastorekit.shard_paths import shard_file_name
-from runregistrykit.tests.shard_store_fixtures import tree_state
+from .shard_store_fixtures import tree_state
 
 
 def _fail_when(real, predicate, error=None):
```

#### (d) `store_fixtures.py:4` reverted to `StoreFixtures/shard_store_fixtures.py`

```diff
diff --git a/runregistrykit/tests/store_fixtures.py b/runregistrykit/tests/store_fixtures.py
index 0212caf..8be2a7b 100644
--- a/runregistrykit/tests/store_fixtures.py
+++ b/runregistrykit/tests/store_fixtures.py
@@ -1,7 +1,7 @@
 """Shared set-up for the store-sidecar tests (`prompts/datastore-portability` prompt 03).
 
 Not a test module (no ``test_`` prefix); the test modules import it. Every store and every run is
-built in one temporary directory: stores with `runregistrykit/tests/shard_store_fixtures.py` (a real
+built in one temporary directory: stores with `StoreFixtures/shard_store_fixtures.py` (a real
 primary with the five tables, placeholder shard files), runs with the `RegistryTestCase` pattern in
 a runs root inside the same directory, so that one `tree_state` covers both. No Ray is
 initialised, the `ShardedPool` constructor is never called, and nothing under `var/` is opened.
```

#### (e) `shard_store_fixtures.py:25`, `KEY_TYPE = "wavenumbers"`

```diff
diff --git a/runregistrykit/tests/shard_store_fixtures.py b/runregistrykit/tests/shard_store_fixtures.py
index 1375949..0ce0698 100644
--- a/runregistrykit/tests/shard_store_fixtures.py
+++ b/runregistrykit/tests/shard_store_fixtures.py
@@ -22,7 +22,7 @@ from typing import Dict, Iterable, Tuple
 from datastorekit.SQL.ShardedPool import ShardedPool
 from datastorekit.shard_paths import shard_file_name
 
-KEY_TYPE = "wavenumber"
+KEY_TYPE = "wavenumbers"
 REPLICATED = ["version", "wavenumber"]
 SHARDED = {"GkSource": "k"}
 
```

#### (f) one test method deleted from `test_store_sidecar.py` (`test_it_does_not_open_the_primary`, with its trailing blank line)

```diff
diff --git a/runregistrykit/tests/test_store_sidecar.py b/runregistrykit/tests/test_store_sidecar.py
index 597efd0..e582387 100644
--- a/runregistrykit/tests/test_store_sidecar.py
+++ b/runregistrykit/tests/test_store_sidecar.py
@@ -293,13 +293,6 @@ class TestCreate(StoreTestCase):
             fields["store_id"],
         )
 
-    def test_it_does_not_open_the_primary(self):
-        primary = self.top / "B" / "junk.sqlite"
-        write_placeholder(primary)  # not a database at all
-        before = primary.read_bytes(), primary.stat().st_mtime_ns
-        stores.create_sidecar(primary, "a note beside a file that is not a store")
-        self.assertEqual((primary.read_bytes(), primary.stat().st_mtime_ns), before)
-
     def test_each_refusal(self):
         primary = self.a_store()
         path = stores.sidecar_path(primary)
```

#### (g) one 02 row (`test_store_amend_residuals.py`) set back to *pending, 02* in the check's table

```diff
diff --git a/docs/extraction/compare_with_source.py b/docs/extraction/compare_with_source.py
index 0bed22e..74ba0f3 100644
--- a/docs/extraction/compare_with_source.py
+++ b/docs/extraction/compare_with_source.py
@@ -172,7 +172,7 @@ TABLE = (
     (
         "RunRegistry/tests/test_store_amend_residuals.py",
         "0c6e6a2ca5d59b74dcb960111a5cd05ed2d991f4",
-        PORTED,
+        pending("02"),
         "runregistrykit/tests/test_store_amend_residuals.py",
     ),
     (
```

#### (h-a) 01's (a): `DEFAULT_STALE_AFTER = 901.0` in `__init__.py`

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 4e91677..55ce188 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -62,7 +62,7 @@ TERMINAL_STATES = ("done", "failed", "killed")
 # The lister's default staleness window. `liveness()` itself takes the window from its caller;
 # fifteen minutes is a convention for the command line, overridable with --stale-after, and is
 # chosen to be long against a heartbeat written once per completed unit.
-DEFAULT_STALE_AFTER = 900.0
+DEFAULT_STALE_AFTER = 901.0
 
 _ID_STAMP = "%Y%m%dT%H%M%S"
 
```

#### (h-b) 01's (b): an extra `import os` in `__main__.py`

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 5a9b61b..d49ffab 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -23,6 +23,7 @@ sidecar, a run directory or any other record, and every other command refuses a
 
 import argparse
 import json
+import os
 import sys
 import time
 
```

#### (h-c) 01's (c): one deleted line in `stores.py`

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index a70cfbd..05c2881 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -195,7 +195,6 @@ _DIGEST = re.compile(r"[0-9a-f]{64}")
 # what the inventory records, or to how a digest is formed, bumps this and captures a new golden
 # fingerprint in the same commit, beside the old ones and never over them
 # (`runregistrykit/tests/data/full_store_fingerprint*.json`; `test_store_fingerprint.GOLDEN` names the
-# current one). Format 2: prompts/datastore-integrity prompt 07 put the WKB rows' numeric parent in
 # their key. Format 3: prompt 08 put the QuadSourcePolicy in the QuadSourceIntegral rows' key.
 # Format 4: prompt 09a put the two TkNumericIntegrations, Tq and Tr, in the QuadSource rows' key.
 # Format 5: prompt 09b put the set of Gk numeric and WKB rows each GkSource is assembled from in its
```

#### (h-d) 01's (d): `prog="runregistrykit"` changed to `prog="RunRegistryKit"`

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 5a9b61b..24bad6e 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -370,7 +370,7 @@ def _store(args) -> int:
 
 
 def main(argv=None) -> int:
-    parser = argparse.ArgumentParser(prog="runregistrykit", description=__doc__)
+    parser = argparse.ArgumentParser(prog="RunRegistryKit", description=__doc__)
     sub = parser.add_subparsers(dest="command", required=True)
     lister = sub.add_parser("list", help="every run, newest first")
     lister.add_argument("--root", default=DEFAULT_ROOT, help=f"default {DEFAULT_ROOT}")
```

#### (h-e) 01's (e): `"var", "runs"` changed to `"var", "run"` on the `DEFAULT_ROOT` line

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 4e91677..4137904 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -55,7 +55,7 @@ import time
 from datetime import datetime, timezone
 
 REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
-DEFAULT_ROOT = os.path.join(REPO_ROOT, "var", "runs")
+DEFAULT_ROOT = os.path.join(REPO_ROOT, "var", "run")
 
 TERMINAL_STATES = ("done", "failed", "killed")
 
```

#### (h-f) 01's (f): a word other than `RunRegistry` changed on a D-name line

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 5a9b61b..014242c 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -1,4 +1,4 @@
-"""`python -m runregistrykit list` — one line per run, newest first.
+"""`python -m runregistrykit list` — one line per run, oldest first.
 
 Run it at the start of a session and before launching anything long. A registry nobody reads is
 worse than none, because it looks like coverage.
```

#### (h-g) 01's (g): an undeclared `runregistrykit/extra.py`

```diff
diff --git a/runregistrykit/extra.py b/runregistrykit/extra.py
new file mode 100644
index 0000000..58af570
--- /dev/null
+++ b/runregistrykit/extra.py
@@ -0,0 +1 @@
+"""A module no row of the table and no declared new file names."""
```

#### (h-h) 01's (h): a wrong blob in the check's table for a "not imported" row

```diff
diff --git a/docs/extraction/compare_with_source.py b/docs/extraction/compare_with_source.py
index 47a452b..ff804af 100644
--- a/docs/extraction/compare_with_source.py
+++ b/docs/extraction/compare_with_source.py
@@ -175,7 +175,7 @@ TABLE = (
     ),
     (
         "RunRegistry/tests/test_killed_handler.py",
-        "213f2a8d7d017f845b85ea209f8e87886539988b",
+        "213f2a8d7d017f845b85ea209f8e87886539988c",
         NOT_IMPORTED,
         None,
     ),
```

#### (h-i) 01's (i): `stores.py:544` left unrenamed

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index a70cfbd..66fbdd3 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -541,7 +541,7 @@ def _tombstone_problems(
                 f"but its completion was not recorded"
             )
         text += (
-            f'. Run `python -m runregistrykit store retire "{primary}" --reason <the recorded '
+            f'. Run `python -m RunRegistry store retire "{primary}" --reason <the recorded '
             f"reason>` again to complete it"
         )
         return [text], text
```

#### (m1) `RECORDED_DISTRIBUTIONS = ("datastorekit",)`

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 4e91677..dab057a 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -116,7 +116,7 @@ def git_provenance(cwd=REPO_ROOT) -> dict:
 # adopts (README §0, U4). From prompt 04 on a run executes code that is not in this repository's
 # tree, so the manifest records which release of it was installed, and R0, R1 and R2 each say what
 # they ran.
-RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")
+RECORDED_DISTRIBUTIONS = ("datastorekit",)
 
 
 def package_provenance(names=RECORDED_DISTRIBUTIONS) -> dict:
```

#### (m2) `_history_entry("copy", …)` changed to `"copied"` in `copy_store`

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index a70cfbd..d508f62 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1098,7 +1098,7 @@ def copy_store(src, dst, purpose, runs_root=None) -> dict:
             "datastore": _repo_path(src),
         }
         fields["history"] = list(fields["history"]) + [
-            _history_entry("copy", src, dst, git_provenance())
+            _history_entry("copied", src, dst, git_provenance())
         ]
         _write_new_sidecar(dst_sidecar, fields, dst)
     except Exception as e:
```

#### (m3) `amend_sidecar` no longer appends its `amend` history entry

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index a70cfbd..3a28899 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -2170,7 +2170,7 @@ def amend_sidecar(
         del new_fields[field]
     else:
         new_fields[field] = new_value
-    new_fields["history"] = list(new_fields["history"]) + [entry]
+    new_fields["history"] = list(new_fields["history"])
 
     _update_sidecar(reading.path, new_fields, primary)
 
```

#### Tried for (m3), not caught: the sidecar reader's `bool` guard on `sidecar_format` dropped

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index a70cfbd..30ab0b3 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -576,7 +576,7 @@ def _registry_problems(fields: dict, primary: Path) -> List[str]:
     reader, and by every writer on what it is about to write."""
     problems = []
     fmt = fields.get("sidecar_format")
-    if isinstance(fmt, bool) or fmt != SIDECAR_FORMAT:
+    if fmt != SIDECAR_FORMAT:
         problems.append(
             f"sidecar_format is {fmt!r}; this reader knows format {SIDECAR_FORMAT} only"
         )
```

#### Tried for (m3), not caught: `_STORE_ID.fullmatch` changed to `.match`

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index a70cfbd..d5ee742 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -586,7 +586,7 @@ def _registry_problems(fields: dict, primary: Path) -> List[str]:
 
     if "store_id" in fields:
         value = fields["store_id"]
-        if not (isinstance(value, str) and _STORE_ID.fullmatch(value)):
+        if not (isinstance(value, str) and _STORE_ID.match(value)):
             problems.append(
                 f"store_id {value!r} is not 32 lowercase hexadecimal characters"
             )
```

## Observations not acted on

- **`DEFAULT_STALE_AFTER = 901.0` (01's (a)) passes the suite**: no ported test pins it. Recorded as
  the prompt asks; no issue.
- **No ported test catches two reader mutations** (the `bool` guard on `sidecar_format`, and
  `fullmatch` against `match` on the `store_id`). `TestTypeStrictComparison` covers the amend path's
  `True`/`1`, but not the reader's. Not an issue opened: the prompt's rule is "pin what is
  imported", and 04's neutral-store tests are where a sidecar-reader test would be added.
- **`test_package_imports.py` names `StoreFixtures` and `RunRegistry`** as the module names it
  checks are *not* loaded (`:32-33`), so those two words are in the package's tests on purpose. It is
  not a checked file (no source), so the check's completeness rule does not cover it; 05's guard
  (U10) must allow that file or scan with that in mind.
- **From `test_store_copy_move.py:73` on, that file's package line numbers are no longer SGK's**
  (601 → 610 lines); every other file's, and every module's, are. PROVENANCE says so.
- **The brief's note that `pip freeze` prints the editable install at the `HEAD` of the time of
  asking** (01's observation) is unchanged; nothing was installed.
- **Another session's test run (a different project, a different interpreter) was on the machine
  during the breakage replays**, and no Ray process was ever started by this work: the final
  `pgrep` is empty.

## State handed to the next prompt

- The package is the import (01) plus 108 tests: `runregistrykit/tests/` holds the eight ported
  files and 01's import test. The suite is **108**; 03's count starts there, and every prompt from 03
  records it before and after (README §5 rule 6).
- `docs/extraction/compare_with_source.py` exits 0 with 3 pending files (04's); it needs `black`
  25.1.0 in the interpreter (`venv/` has it). **It is retired at 03's start** (README §4): from 03
  the package changes in its own right, and the check describes `8155445`'s tree, re-run from a
  worktree of it. 03 must not edit the ported tests beyond what its prompt says: the pinning test
  `test_the_recorded_names_are_the_two_packages` (`test_run_registry.py:393-396`) is the one 03's
  `[00-the-recorded-distributions-are-sgks]` changes.
- `CLAUDE.md`'s Tests bullet and `PROVENANCE.md` are written. The board's §3 has eight issues; the
  new one is 05's.
- Not touched: the three modules, `tests/__init__.py`, `test_package_imports.py`, `pyproject.toml`;
  no client, DatastoreKit or RayPoolKit was edited or run; nothing was installed; nothing was
  pushed or tagged.
