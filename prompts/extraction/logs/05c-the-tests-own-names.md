# Log — prompt 05c: the tests' own names

**Subject:** Rename the tests' client names, make their fixture data neutral and rewrite their prose, so that the guard's known hits are empty
**Commit:** `a7d93d5` (on `main`, after `bd83b3d`)
**Date:** 2026-10-15
**Agent:** Claude Sonnet 5.5, dispatched by the orchestrator with its brief and the orchestration
note's section 0 (`brief-05c-section0.md`)
**Result:** **landed.** Sixteen names are renamed under U16 (the prompt's thirteen and the brief's
three), the fixtures' client data is neutral, `test_package_imports.py`'s `FORBIDDEN` is built from
the guard's `project_packages()`, and the docstrings and comments of 14 test modules and fixtures
are in the package's own terms. `known_hits.json` is written by 05a's writer with every scan's list
**empty** (155 hits in 94 entries before, 0 after), and the guard's docstring says so. The assertions
are unchanged (`ast` with docstrings removed equals `8766714`'s after the map and the neutral data,
for every file but `FORBIDDEN`'s assignment and its one import). The suite: **276 -> 276**
(`Ran 276 tests ... OK`, 88.5 s), the same per module. (m1)-(m6) each fail at least one test. No
stop condition was met. `[02-the-ported-tests-name-sgk]` is closed;
`[05c-the-import-test-needs-datastorekit]` is opened (owner 06); `docs/OPEN_ISSUES.md` stays at
**3**.

## What shipped

| File | What |
|---|---|
| `runregistrykit/tests/store_fixtures.py` | `a3_shaped` -> `hand_written_shaped`, `sweep_shaped` -> `script_written_shaped`; their values and docstrings neutral; the module docstring, the layouts' comment and `assertProperty`'s docstring in the package's terms |
| `runregistrykit/tests/shard_store_fixtures.py` | `KEY_TYPE`, `REPLICATED`, `SHARDED` neutral; `write_hand_built_primary`'s docstring |
| `runregistrykit/tests/neutral_store.py` | the three shared columns renamed (`producer_serial`, `tagged_serial`, `log10_step`) and `SOLVER_COLUMNS`' value; no prose beyond the names |
| `runregistrykit/tests/test_package_imports.py` | `FORBIDDEN` from `project_packages()`; one import |
| `runregistrykit/tests/test_store_amend.py`, `test_store_sidecar.py`, `test_store_fingerprint.py`, `test_store_copy_move.py`, `test_run_registry.py` | the renamed class, methods, helpers and constants; neutral data (stems, run directory, campaign, run id); prose |
| `runregistrykit/tests/test_fingerprinter.py`, `test_store_retire.py`, `test_store_command_line.py` | `QSI`/`TKN` and `sweep_shaped` renamed where used; prose; the raw SQL of `test_store_retire.py` |
| `runregistrykit/tests/test_client_root.py`, `test_store_amend_residuals.py`, `test_store_retire_references.py` | prose only |
| `runregistrykit/tests/test_package_is_generic.py` | the module docstring's paragraph "The known hits" only; its code is `ast`-identical to `8766714`'s |
| `runregistrykit/tests/data/known_hits.json` | rewritten by the writer: every scan empty |
| `PROVENANCE.md` | 05c's section under "Since the import", "The tests' renames" (16 rows with test ids) and "Where the tests' citations pointed" (as their own `##` sections, after 05b's "Where the prose's citations pointed") |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

No file is added or removed under `runregistrykit/`. Not touched: any package module,
`client_vocabulary.json`, `docs/extraction/measure_client_vocabulary.py`, `compare_with_source.py`,
`pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `CLAUDE.md`, the campaign README, the prompt,
`prompts/extraction/orchestrator/`, `test_public_names.py` and `client_fixtures.py` (both equal
`8766714`'s byte for byte).

## The renames, as applied

Applied by a script (`rename.py`, whole-word replacement over every test file but the guard and
`test_public_names.py`, longest names first), then `black`. Sites are occurrences (definitions,
imports, uses, and the prose that named the name) counted in the tree at `8766714`:

```
test_an_a3_shaped_sidecar_keeps_every_unknown_field -> test_a_hand_written_shaped_sidecar_keeps_every_unknown_field 1 test_store_sidecar.py:1
test_an_a3_shaped_sidecar_through_adopt_copy_and_move -> test_a_hand_written_shaped_sidecar_through_adopt_copy_and_move 1 test_store_sidecar.py:1
test_prompt_02s_refusals_pass_through -> test_datastorekits_refusals_pass_through 1 test_store_copy_move.py:1
test_amend_backup_as_prompt_05_will -> test_amend_backup_once_it_is_retired 1 test_store_amend.py:1
test_a_sweep_shaped_legacy_sidecar -> test_a_script_written_shaped_legacy_sidecar 1 test_store_sidecar.py:1
test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file -> test_a_torn_line_is_tolerated_only_at_the_end_of_the_file 1 test_run_registry.py:1
test_deleting_one_quadsourceintegral_row -> test_deleting_one_integral_row 1 test_store_fingerprint.py:1
test_timestamps_labels_and_solver_serials -> test_timestamps_labels_and_producer_serials 1 test_store_fingerprint.py:1
TestLiveA3Shape -> TestHandWrittenShape 1 test_store_amend.py:1
a3_shaped -> hand_written_shaped 7 store_fixtures.py:1, test_store_amend.py:2, test_store_sidecar.py:4
sweep_shaped -> script_written_shaped 17 store_fixtures.py:1, test_fingerprinter.py:2, test_store_amend.py:2, test_store_command_line.py:2, test_store_fingerprint.py:2, test_store_retire.py:2, test_store_sidecar.py:6
QSI -> INTEGRAL_CLASS 24 test_fingerprinter.py:1, test_store_fingerprint.py:17, test_store_retire.py:6
TKN -> SOLUTION_CLASS 7 test_fingerprinter.py:1, test_store_fingerprint.py:6
solver_serial -> producer_serial 8 neutral_store.py:7, test_store_fingerprint.py:1
parent_serial -> tagged_serial 10 neutral_store.py:6, test_store_fingerprint.py:2, test_store_retire.py:2
log10_tol -> log10_step 6 neutral_store.py:6
```

Every new name occurs nowhere else under `runregistrykit/` at `bd83b3d` and none is a forbidden word
of the guard (its scans find nothing). `SOLVER_COLUMNS` and `_solver()` keep their names, their value
and column changed. The raw SQL of `test_store_fingerprint.py` and `test_store_retire.py` names the
renamed columns. The test ids that changed, old to new (by loader, 276 before and after; **eight**
change, `diff` of the two sorted lists):

```
> test_run_registry.TestLedgerIsNotTheResultsStore.test_a_torn_line_is_tolerated_only_at_the_end_of_the_file
< test_run_registry.TestLedgerIsNotTheResultsStore.test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file
> test_store_amend.TestHandWrittenShape.test_amend_backup_once_it_is_retired
< test_store_amend.TestLiveA3Shape.test_amend_backup_as_prompt_05_will
< test_store_copy_move.TestRefusals.test_prompt_02s_refusals_pass_through
> test_store_copy_move.TestRefusals.test_datastorekits_refusals_pass_through
< test_store_fingerprint.TestLocalised.test_deleting_one_quadsourceintegral_row
> test_store_fingerprint.TestLocalised.test_deleting_one_integral_row
< test_store_fingerprint.TestNotContent.test_timestamps_labels_and_solver_serials
> test_store_fingerprint.TestNotContent.test_timestamps_labels_and_producer_serials
> test_store_sidecar.TestAdopt.test_a_hand_written_shaped_sidecar_keeps_every_unknown_field
< test_store_sidecar.TestAdopt.test_a_sweep_shaped_legacy_sidecar
< test_store_sidecar.TestAdopt.test_an_a3_shaped_sidecar_keeps_every_unknown_field
> test_store_sidecar.TestAdopt.test_a_script_written_shaped_legacy_sidecar
< test_store_sidecar.TestUnknownFieldsSurvive.test_an_a3_shaped_sidecar_through_adopt_copy_and_move
> test_store_sidecar.TestUnknownFieldsSurvive.test_a_hand_written_shaped_sidecar_through_adopt_copy_and_move
```

The brief says nine ids change; the arithmetic is five of the prompt's map plus three of correction
1 = eight, the renamed class having one method, which is the map's `test_amend_backup_...` (a
count that took the class as a ninth). The counts by loader, before (at `bd83b3d`) and after: every
module's equal: test_client_root 27 test_fingerprinter 31 test_package_imports 3 test_package_is_generic 22 test_public_names 8 test_run_registry 29 test_store_amend 21 test_store_amend_residuals 9 test_store_command_line 2 test_store_copy_move 27 test_store_fingerprint 29 test_store_retire 41 test_store_retire_references 10 test_store_sidecar 17 .

## Neutral data, old and new

Every key, type, nesting and path shape kept. In `store_fixtures.py`, `hand_written_shaped`:

| Key | Old | New |
|---|---|---|
| `purpose` | `Baseline datastore for a census. The before-picture. Keep.` | `Baseline datastore for an example. The before-picture. Keep.` |
| `grid_criterion` | `post prompt 15 (measured curvature criterion)` | `post refinement 15 (measured criterion)` |
| `driver` | `docs/gktk-remedial/scoped_pipeline_run.py (NOT the other copy)` | `docs/example/driver.py (NOT the other copy)` |
| `scope` | `8 log-spaced k over 1e5-3e8 /Mpc, --zend 0.1` | `8 log-spaced points over 1e5-3e8 /unit, --limit 0.1` |
| `status_files.stdout`, `.pid` | `var/runs/a3-pilot/run.out`, `.../run.pid` | `var/runs/pilot-run/run.out`, `.../run.pid` |
| `run_history[0].stages_complete[1]` | `APPLY GKSOURCE POLICIES` | `APPLY EXAMPLE POLICIES` |

Unchanged in it (the dates, digests and sizes are data; `note`, `restart`, `backup` name no client):
`name`, `datastore`, `created`, `git_head`, `git_dirty`, `note`, `run_history` (`started`, `elapsed`,
`size_at_stop`, `ratio`, `count`, `nothing`, `outcome`, `datastore_state`), `restart`, `backup`. Its
ten unknown fields are still ten (`test_store_sidecar.py`'s `assertEqual(len(unknown(legacy)), 10)`
passes, and (m6) below removes one key and fails it). `script_written_shaped`: `purpose` `Working
copy for a sweep. Disposable.` -> `Working copy for an example. Disposable.`; its other values name
nothing. Elsewhere:

| File | Old | New |
|---|---|---|
| `shard_store_fixtures.py` | `KEY_TYPE = "wavenumber"`; `REPLICATED = ["version", "wavenumber"]`; `SHARDED = {"GkSource": "k"}` | `"mode"`; `["version", "mode"]`; `{"Solution": "k"}` |
| `test_store_sidecar.py` | stems `handover-A3-baseline-lambdacdm`, `handover-atol-sweep` (and the path `/x/handover-atol-sweep.sqlite`) | `example-B2-baseline-run`, `example-working-copy` (`/x/example-working-copy.sqlite`) |
| `test_run_registry.py` | `campaign="run-registry"` (the crasher's source and the run helper); the directory `a3-pilot` (7 uses) | `campaign="example"`; `pilot-run` |
| `test_store_fingerprint.py` | run id `store-fingerprint-04-test-20260925T100000` | `example-04-test-20260925T100000` |

The prompt's trial named the second stem `example-step-sweep`; its section 2.3 and this commit say
`example-working-copy`. The prompt's section 2.3 left `purpose` and `scope` to this prompt; the
values above are this commit's choice (deviation 8).

## `FORBIDDEN`

```python
# Not one of these may be loaded by importing the package and its store layer: the heavy
# dependencies of the store layer, `config`, and the clients' project packages, which the guard
# reads from the vocabulary file (`test_package_is_generic.project_packages`), so that the check
# is the same for every client and this module names none.
FORBIDDEN = tuple(
    sorted({"ray", "sqlalchemy", "datastorekit", "config"} | project_packages())
)
```

with `from runregistrykit.tests.test_package_is_generic import project_packages`. It is a sorted tuple
of **22** names (the 18 project packages and the four kept), a literal `{FORBIDDEN!r}` in the child's
code evaluates. The check asserts **22 names for 7, and never fewer** (the three SGK packages were
among the 18). The module now imports the guard, which imports `datastorekit` at module scope, so it
no longer imports without `datastorekit` installed: observation 1, issue
`[05c-the-import-test-needs-datastorekit]`.

## The guard's docstring and `known_hits.json`

The module docstring's paragraph "The known hits" loses the sentence "Entries under
`runregistrykit/tests/` are the tests' to remove, the rest the package modules'" and gains "The list
is empty in every scan, so a hit in any file fails its scan"; the paragraph is rewrapped within 100
columns; it keeps the file, the `[file, word, count]` form, the exactness rule and "the file is
data". Nothing else of the guard changes: `ast.dump` of it with its docstring removed equals
`8766714`'s (the script's `EQUAL test_package_is_generic.py`).

The file was deleted and written by 05a's writer, from `agent-05c/` of the session scratchpad, with
the venv's interpreter, from the repository root, once every test file was final. **Its one
change** from 05a's text is the `owners` string, here "none: the package and its tests hold no known
hit, and a hit in any file fails its scan". The writer's text, whole:

```python
"""Writes runregistrykit/tests/data/known_hits.json from the guard's own scans (05a, correction 10).
Run from the repository root: ./venv/bin/python <this file>. Refuses to overwrite."""
import json, sys
from pathlib import Path
from runregistrykit.tests import test_package_is_generic as g

if g.KNOWN_HITS.exists():
    sys.exit("refusing to overwrite " + str(g.KNOWN_HITS))
hits = g.scan_all()
data = {
    "owners": "none: the package and its tests hold no known hit, and a hit in any file fails its scan",
    "known hits": {name: g.count_hits(h) for name, h in hits.items()},
}
g.KNOWN_HITS.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
for name, h in hits.items():
    pk = [x for x in h if not g.is_test(x[0])]
    ts = [x for x in h if g.is_test(x[0])]
    print(name, "package", len(pk), "tests", len(ts))
```

Its output:

```
test_no_code_name package 0 tests 0
test_no_string_or_docstring package 0 tests 0
test_no_comment package 0 tests 0
test_no_citation package 0 tests 0
test_every_import_is_allowed package 0 tests 0
```

The per-scan totals, hits (file-word entries), before and after:

| Scan | Package modules before | after | Tests before | after |
|---|---|---|---|---|
| code names | 0 | 0 | 29 (14) | **0** |
| strings and docstrings | 0 | 0 | 67 (36) | **0** |
| comments | 0 | 0 | 1 (1) | **0** |
| citations | 0 | 0 | 58 (43) | **0** |
| imports | 0 | 0 | 0 | 0 |
| **all** | 0 | 0 | **155 (94)** | **0** |

The file after, whole (`git diff --stat` of it: 5 insertions, 479 deletions; the deleted lines are
the 94 entries, which `git show bd83b3d:runregistrykit/tests/data/known_hits.json` shows):

```json
{
  "owners": "none: the package and its tests hold no known hit, and a hit in any file fails its scan",
  "known hits": {
    "test_no_code_name": [],
    "test_no_string_or_docstring": [],
    "test_no_comment": [],
    "test_no_citation": [],
    "test_every_import_is_allowed": []
  }
}
```

## Deviations from the prompt

Each classified. Corrections 1-12 are the brief's.

1. **Three more renames** (brief, correction 1): `test_an_a3_shaped_sidecar_keeps_every_unknown_field`
   and `test_an_a3_shaped_sidecar_through_adopt_copy_and_move` (`a3` is in the code and section 3.4
   requires it gone) and `test_prompt_02s_refusals_pass_through` -> `test_datastorekits_refusals_pass_through`
   (it names a campaign's prompt, as `test_amend_backup_as_prompt_05_will` does; the refusal is
   DatastoreKit's). The first two **STRUCTURALLY REQUIRED**, the third an **IMPLEMENTATION CHOICE**.
2. **`QSI` and `TKN` as attributes** (correction 2): `ported.QSI` and `ported.TKN` in
   `test_fingerprinter.py:855-856` become `ported.INTEGRAL_CLASS` and `ported.SOLUTION_CLASS`.
   **STRUCTURALLY REQUIRED** (they are uses of the renamed names; section 2.2 says "everywhere").
3. **`FORBIDDEN` brings `datastorekit` into the import test** (correction 3): done as section 2.4
   says (import the guard's function; the guard is not changed); issue
   `[05c-the-import-test-needs-datastorekit]` opened, owner 06. **STRUCTURALLY REQUIRED** by the
   prompt's own instruction.
4. **`FORBIDDEN` as a sorted tuple of 22** (correction 4). **IMPLEMENTATION CHOICE** (the form the
   prompt left open; a tuple so that its `repr` is a literal).
5. **The guard's docstring paragraph** (correction 5): as the brief says. **STRUCTURALLY REQUIRED**.
6. **The writer's `owners` string** (correction 6, prompt section 2.6): **STRUCTURALLY REQUIRED**.
7. **One more replacement in the AST script's table** (correction 7): the table adds
   `campaign="run-registry"` inside a code string (the crasher in `test_run_registry.py`, the same
   replacement as the run helper's keyword), which the prompt's list names only for the helper. **IMPLEMENTATION CHOICE** (the replacement is the
   same, applied to a string that holds code).
8. **The values of `purpose`, `grid_criterion`, `scope`, `stages_complete`** (section 2.3 says
   "without" and gives no replacement for `purpose` and `scope`): the table above. **IMPLEMENTATION
   CHOICE**.
9. **A fact dropped from `write_hand_built_primary`'s docstring.** The old text listed, among the
   readers of such a primary that never read `replication_in_flight`, "the audit tool or the sweep
   script's check": two client programs. The new text lists `read_pool` and the closed-store
   operations only, which are this package's and DatastoreKit's. What the docstring is for (the
   constructor refuses what the helper builds, and nothing that uses it reads that table) is kept.
   **IMPLEMENTATION CHOICE**; the old sentence's reason cannot be kept without naming client
   programs.
10. **Incident counts stated in general terms.** `TestSelfMatch`'s "Nineteen such loops accumulated
    in one session ... fifteen were waiting on a job that had already been killed" and "with
    nineteen of them each matched the other eighteen" became "Such loops accumulated, and none of
    them could ever exit, though many were waiting on a job that had already been killed" and "with
    many of them each matched all the others"; `prompts/run-registry/README.md` section 0 item 3
    is gone (recorded in `PROVENANCE.md`). **IMPLEMENTATION CHOICE** (prompt section 2.5, rule 1:
    "a reason given by an incident is stated in general terms").
11. **`test_store_copy_move.py`'s "which works since prompt 01"** is dropped, not restated: the old
    clause named the campaign prompt that made a store movable by hand, and its mechanism is not in
    this repository's text. The test's docstring says the directory was moved by hand and the
    `results` path names somewhere else, which is what the test builds. **IMPLEMENTATION CHOICE**.
12. **Two numbered module lists.** `test_store_fingerprint.py`'s list numbered after another
    repository's test numbers (1-3, 5-11, with 4 missing) becomes bullets, the descriptions kept;
    `test_store_retire.py`'s and `test_store_amend.py`'s lists are kept numbered, for they number
    the sections that the files' own `# 1.` ... headers mirror (item 4 of the first and 3 of the
    second lose only the client and campaign names). **IMPLEMENTATION CHOICE**.
13. **`R14` and `R15`** in `test_store_amend_residuals.py` (labels of review residuals, not forms
    the guard finds) are removed with the "prompt 06" citation, the descriptions kept.
    **IMPLEMENTATION CHOICE** (prompt section 2.5's "an issue of any repository").
14. **`this repository's` own decisions** (`Q3`, `U9`, `U7`, `U14`, `D4`, `D5`, `D6`, `C3`, the
    tag `[02-the-sidecar-readers-guards-are-unpinned]`) removed from the class docstrings, each
    docstring keeping what the class checks. Prompt section 2.5 lists them; recorded for the count.
    **STRUCTURALLY REQUIRED** (the guard's citation scan).
15. **The brief's id count** (nine): eight ids change (see "The renames"). Not a change to the
    work; recorded so that the count is not read as a miss.

No **UNINTENDED DRIFT**.

## Verification performed

**1. The suite.** Before, at `bd83b3d`: `Ran 276 tests in 92.731s`, OK (the orchestrator's, and this
agent's `Ran 276 tests in 99.746s` on the tree after the renames and the data, before the last
prose edit). After, on the commit's test files, run in the foreground from the repository root
(`./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, output to a file):
**`Ran 276 tests in 88.501s`, `OK`**. By loader, before and after (module by module the same):
test_client_root 27 test_fingerprinter 31 test_package_imports 3 test_package_is_generic 22 test_public_names 8 test_run_registry 29 test_store_amend 21 test_store_amend_residuals 9 test_store_command_line 2 test_store_copy_move 27 test_store_fingerprint 29 test_store_retire 41 test_store_retire_references 10 test_store_sidecar 17 .

**2. Nothing outside temporary directories.** `git status --short --ignored` (the `__pycache__/`
lines left out) the same before and after the run (compared, `same`); no `var/`; `git worktree list`
shows this checkout alone; `pgrep -f "raylet|gcs_server|ray::"` finds 0 processes; `RAY_ADDRESS`
unset. No Ray was started.

**3. The assertions are unchanged.** `ast_check.py`, in the scratchpad (outside the repository),
compares for each file of `runregistrykit/tests/` the `ast.dump` with every module, class and
function docstring removed, at `bd83b3d` (whose tests are `8766714`'s) after the old tree is
transformed: the map of section 2.2 and correction 1 applied to every `Name`, `Attribute`,
`FunctionDef`, `ClassDef`, `arg`, `alias` and `keyword`, and the map and section 2.3's replacements
to every string constant (f-string parts included). Its output:

```
EQUAL       __init__.py
EQUAL       client_fixtures.py
EQUAL       neutral_store.py
EQUAL       shard_store_fixtures.py
EQUAL       store_fixtures.py
EQUAL       test_client_root.py
EQUAL       test_fingerprinter.py
DIFFERENT   test_package_imports.py (1 statement(s) only in the mapped old tree, 2 only in the new)
   old only: Assign(targets=[Name(id='FORBIDDEN', ctx=Store())], value=Tuple(elts=[Constant(value='ray'), Constant(value='sqlalchemy'), Constant(value='datastorekit'), Const
   new only: ImportFrom(module='runregistrykit.tests.test_package_is_generic', names=[alias(name='project_packages')], level=0)
   new only: Assign(targets=[Name(id='FORBIDDEN', ctx=Store())], value=Call(func=Name(id='tuple', ctx=Load()), args=[Call(func=Name(id='sorted', ctx=Load()), args=[BinOp(lef
EQUAL       test_package_is_generic.py
EQUAL       test_public_names.py
EQUAL       test_run_registry.py
EQUAL       test_store_amend.py
EQUAL       test_store_amend_residuals.py
EQUAL       test_store_command_line.py
EQUAL       test_store_copy_move.py
EQUAL       test_store_fingerprint.py
EQUAL       test_store_retire.py
EQUAL       test_store_retire_references.py
EQUAL       test_store_sidecar.py
files with a difference: 1
```

The one difference is `test_package_imports.py`'s: the `FORBIDDEN` assignment and the one import
of `project_packages`. The script's text, whole (with the replacement table; `rename.py` is the
map of the previous section):

```python
"""Prompt 05c section 3.3: the code of each test module and fixture at 8766714 (read here from the
working tree's git HEAD, bd83b3d, whose tests are 8766714's) against the tree at the commit, with
docstrings removed, after the rename map (section 2.2 and correction 1) is applied to every Name,
Attribute, FunctionDef, ClassDef, arg, alias and keyword of the old tree, and the rename map and
section 2.3's replacements to every string Constant of the old tree. Run from the repository root:
./venv/bin/python <this file> <old tests dir> <new tests dir>"""
import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from rename import MAP, apply_map

# section 2.3's replacements, old substring -> new, over string constants (in this order)
DATA = [
    ("Baseline datastore for a census.", "Baseline datastore for an example."),
    ("post prompt 15 (measured curvature criterion)", "post refinement 15 (measured criterion)"),
    ("docs/gktk-remedial/scoped_pipeline_run.py (NOT the other copy)", "docs/example/driver.py (NOT the other copy)"),
    ("8 log-spaced k over 1e5-3e8 /Mpc, --zend 0.1", "8 log-spaced points over 1e5-3e8 /unit, --limit 0.1"),
    ("var/runs/a3-pilot/", "var/runs/pilot-run/"),
    ("APPLY GKSOURCE POLICIES", "APPLY EXAMPLE POLICIES"),
    ("Working copy for a sweep. Disposable.", "Working copy for an example. Disposable."),
    ("wavenumber", "mode"),
    ("GkSource", "Solution"),
    ("handover-A3-baseline-lambdacdm", "example-B2-baseline-run"),
    ("handover-atol-sweep", "example-working-copy"),
    ("a3-pilot", "pilot-run"),
    ("store-fingerprint-04-test-20260925T100000", "example-04-test-20260925T100000"),
]
EXACT = [("run-registry", "example")]  # a string constant that equals the old text, whole
DATA.append(("campaign=\"run-registry\"", "campaign=\"example\""))  # inside a code string


def strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return tree


def transform_old(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            node.id = apply_map(node.id)
        elif isinstance(node, ast.Attribute):
            node.attr = apply_map(node.attr)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.name = apply_map(node.name)
        elif isinstance(node, ast.arg):
            node.arg = apply_map(node.arg)
        elif isinstance(node, ast.alias):
            node.name = apply_map(node.name)
            if node.asname:
                node.asname = apply_map(node.asname)
        elif isinstance(node, ast.keyword) and node.arg:
            node.arg = apply_map(node.arg)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            for a, b in EXACT:
                if v == a:
                    v = b
            for a, b in DATA:
                v = v.replace(a, b)
            node.value = apply_map(v)
    return tree


def dump(tree):
    return ast.dump(tree, include_attributes=False)


def top_level(tree):
    return [ast.dump(s) for s in tree.body]


old_dir, new_dir = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for new in sorted(new_dir.glob("*.py")):
    old = old_dir / new.name
    to = transform_old(strip_docstrings(ast.parse(old.read_text())))
    tn = strip_docstrings(ast.parse(new.read_text()))
    if dump(to) == dump(tn):
        print("EQUAL      ", new.name)
        continue
    # list the differing top-level statements
    a, b = top_level(to), top_level(tn)
    only_old = [s for s in a if s not in b]
    only_new = [s for s in b if s not in a]
    print("DIFFERENT  ", new.name, f"({len(only_old)} statement(s) only in the mapped old tree, {len(only_new)} only in the new)")
    for s in only_old:
        print("   old only:", s[:160])
    for s in only_new:
        print("   new only:", s[:160])
    bad += 1
print("files with a difference:", bad)
```

```python
import re, sys
from pathlib import Path

MAP = [
    ("test_an_a3_shaped_sidecar_keeps_every_unknown_field", "test_a_hand_written_shaped_sidecar_keeps_every_unknown_field"),
    ("test_an_a3_shaped_sidecar_through_adopt_copy_and_move", "test_a_hand_written_shaped_sidecar_through_adopt_copy_and_move"),
    ("test_prompt_02s_refusals_pass_through", "test_datastorekits_refusals_pass_through"),
    ("test_amend_backup_as_prompt_05_will", "test_amend_backup_once_it_is_retired"),
    ("test_a_sweep_shaped_legacy_sidecar", "test_a_script_written_shaped_legacy_sidecar"),
    ("test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file", "test_a_torn_line_is_tolerated_only_at_the_end_of_the_file"),
    ("test_deleting_one_quadsourceintegral_row", "test_deleting_one_integral_row"),
    ("test_timestamps_labels_and_solver_serials", "test_timestamps_labels_and_producer_serials"),
    ("TestLiveA3Shape", "TestHandWrittenShape"),
    ("a3_shaped", "hand_written_shaped"),
    ("sweep_shaped", "script_written_shaped"),
    ("QSI", "INTEGRAL_CLASS"),
    ("TKN", "SOLUTION_CLASS"),
    ("solver_serial", "producer_serial"),
    ("parent_serial", "tagged_serial"),
    ("log10_tol", "log10_step"),
]


def apply_map(s):
    for a, b in MAP:
        s = re.sub(r"(?<![A-Za-z0-9_])" + re.escape(a) + r"(?![A-Za-z0-9_])", b, s)
    return s


if __name__ == "__main__":
    root = Path(sys.argv[1])
    for p in sorted(root.glob("*.py")):
        if p.name in ("test_package_is_generic.py", "test_public_names.py"):
            continue
        s = p.read_text()
        n = apply_map(s)
        if n != s:
            p.write_text(n)
            print("changed", p.name)
```

**4. The prose, by the guard and by grep.** The guard's scans find **nothing** in any file
(`hits.py`: all five scans 0, the output above). The grep over the docstrings and comments of every
file under `runregistrykit/tests/` but the guard, case-insensitive, for `prompt`, `campaign`,
`README`, `CLAUDE`, `log's`, `\bA3\b`, `a3`, `sweep`, `handover`, `quadsource`, `scoped_pipeline`,
`QSI`, `TKN`, `GkSource`, `wavenumber`, `census`, `\bP[0-9]+\b`, `\btest [0-9]+\b`, `2026-` and
`§` (`prosegrep.py`, which reads each docstring's lines and each comment token): **0 lines** (it finds
51 on `8766714`'s tree). The whole-file grep (code included) for `a3`, `QSI`, `TKN`, `GkSource`,
`wavenumber`, `quadsource`, `handover`, `run-registry` and `store-fingerprint`: **0 lines**. The same
patterns over **whole files**, code and strings included (`/usr/bin/grep -n -i -E`), find 22 lines,
all code and data, none prose, accounted for:

| Lines | Why they stay |
|---|---|
| `store_fixtures.py` (4): `"created"`, `"started"` timestamps `2026-09-20...`, `2026-09-21T09:11`, `2026-09-23T...` | timestamps in data (a date in data is not an incident) |
| `test_store_fingerprint.py` (4), `test_store_retire.py` (1): `2026-09-24 12:00:00...`, `"2026-09-24"`, `"when": "2026-09-25T10:00:00+01:00"` | timestamps in data, equal to `FIXED_TIMESTAMP` or the sidecar's `when` |
| `test_store_amend.py`: `reason="the backup was retired 2026-09-25 (store retire)"` | a reason string in data, asserted as given |
| `test_run_registry.py` (6), `test_client_root.py` (4), `test_public_names.py` (1): `campaign=`/`prompt=` keywords and `setdefault("campaign", ...)`, the values `"example"`, `"client-config"`, `"client-root"`, `"01"`, `"03"` | `begin()`'s parameters and the manifest's keys, with the tests' own values; `test_public_names.py` pins the signature |
| `test_client_root.py` (2): `".claude", "worktrees", "nest"` | a path, the worktree layout of the coding tool; matched by `CLAUDE` case-insensitively; names no client |

The prose lines the grep and the guard do not match were read, file by file, against `8766714`'s
(each file's diff read); no client, campaign, prompt, section, test or property number, log, decision,
issue, incident date or vanished name (`runregistrykit.stores.fingerprint_of`, "real multi-shard
fixture stores") is left. Width: no changed docstring or comment line is over 100 columns (checked
by a script against the old file's lines, none new), and no paragraph is broken mid-sentence (the
three paragraphs rewrapped are `test_run_registry.py`'s `TestLedgerIsNotTheResultsStore`,
`test_store_amend_residuals.py`'s module docstring and `test_store_retire.py`'s
`TestAnotherStoresShards`'s, and the guard's).

**5. The known hits.** As above: the file, its writer and output, every list empty.

**6. The tests catch behaviour.** (m1)-(m6), below, each applied from a tree with the commit's
test files staged, the suite run, then reverted (`git checkout --`), `git status` clean after each.
None is committed. After the commit each diff was checked as recorded in this log with `git apply
--check` and `git apply -R --check`, in `bash`.

**7. `black --check runregistrykit docs`:** `26 files would be left unchanged`.

## The deliberate-breakage record

| # | Mutation | The suite | Failing tests |
|---|---|---|---|
| (m1) | `TestLiveA3Shape = TestHandWrittenShape` added after the renamed class | `Ran 277 ... FAILED (failures=1)` | FAIL `test_package_is_generic.TestThePackageNamesNoClient.test_no_code_name` (277 because the alias is a second class that discovery loads) |
| (m2) | `neutral_store.py` alone: `tagged_serial` back to `parent_serial` in the spec, the table and the rows | `Ran 276 ... FAILED (failures=1, errors=4)` | ERROR `test_store_fingerprint.TestLocalised.test_adding_a_tag_to_one_record`, `test_deleting_one_integral_row`; `test_store_retire.TestRefusals.test_a_mismatch_in_problems_alone`, `test_a_row_changed_after_fingerprinting` (the raw SQL names `tagged_serial`); FAIL `TestThePackageNamesNoClient.test_no_string_or_docstring` (the old name is a known hit no more) |
| (m3) | `(D4)` added to a comment of `test_store_retire.py` | `Ran 276 ... FAILED (failures=1)` | FAIL `TestThePackageNamesNoClient.test_no_citation` |
| (m4) | one old entry restored to `known_hits.json` (`store_fixtures.py`, `a3_shaped`, 1, under `test_no_code_name`) | `Ran 276 ... FAILED (failures=1)` | FAIL `TestThePackageNamesNoClient.test_no_code_name` (known but found 0 times) |
| (m5) | `json` added to `FORBIDDEN`: the child interpreter does load it | `Ran 276 ... FAILED (failures=1)` | FAIL `test_package_imports.TestPackageImports.test_import_loads_nothing_heavy` |
| (m6) | the agent's: the `note` key removed from `hand_written_shaped` (a key of the neutral data) | `Ran 276 ... FAILED (failures=1)` | FAIL `test_store_sidecar.TestAdopt.test_a_hand_written_shaped_sidecar_keeps_every_unknown_field` (`len(unknown(legacy)) == 10`) |

### The diffs

Each exactly as applied, against this commit's blobs.

#### (m1)

```diff
diff --git a/runregistrykit/tests/test_store_amend.py b/runregistrykit/tests/test_store_amend.py
index bda9fb2..2fec7d8 100644
--- a/runregistrykit/tests/test_store_amend.py
+++ b/runregistrykit/tests/test_store_amend.py
@@ -239,6 +239,9 @@ class TestHandWrittenShape(AmendTestCase):
         self.assertTrue(reading.fields["history"][-1]["before"]["value"]["retained"])
 
 
+TestLiveA3Shape = TestHandWrittenShape
+
+
 # =================================================================================================
 # 4. every refusal, each leaving the whole temporary tree unchanged
 
```

#### (m2)

```diff
diff --git a/runregistrykit/tests/neutral_store.py b/runregistrykit/tests/neutral_store.py
index 710d80e..118e25f 100644
--- a/runregistrykit/tests/neutral_store.py
+++ b/runregistrykit/tests/neutral_store.py
@@ -13,7 +13,7 @@ declares its table and whose `inventory_spec()` declares its identity:
   not;
 - sharded: ``Solution``, tagged through ``Solution_tags``, with a validated flag and a value table
   ``SolutionValue``, whose identity is its ``log10_step``, its mode and its background; and
-  ``Integral``, tagged through ``Integral_tags`` ``(timestamp, tagged_serial, tag_serial)``, whose
+  ``Integral``, tagged through ``Integral_tags`` ``(timestamp, parent_serial, tag_serial)``, whose
   identity is its ``q`` and its solution. Neither's ``label`` or ``producer_serial`` is identity.
 
 Every row has a ``timestamp``, which is never identity. A reference is a column with a foreign key
@@ -240,7 +240,7 @@ class IntegralFactory(_Factory):
         return InventorySpec(
             leaves=("q",),
             parents={"solution": Parent("solution_serial", of=SOLUTION)},
-            tags=(INTEGRAL_TAGS, "tagged_serial"),
+            tags=(INTEGRAL_TAGS, "parent_serial"),
         )
 
 
@@ -251,7 +251,7 @@ class IntegralTagsFactory(_Factory):
             "serial": False,
             "timestamp": True,
             "columns": [
-                _reference("tagged_serial", INTEGRAL),
+                _reference("parent_serial", INTEGRAL),
                 _reference(TAG_SERIAL, TAG_TABLE),
             ],
         }
@@ -339,15 +339,15 @@ FULL_SHARDED_ROWS: Dict[int, RowSet] = {
         + _tags("solution_serial", 3, (1,)),
         SOLUTION_VALUE: _values(1, (11, 12, 13)) + _values(3, (31, 32)),
         INTEGRAL: [_integral(1, 1, 0.5), _integral(2, 1, 0.25)],
-        INTEGRAL_TAGS: _tags("tagged_serial", 1, (1, 2))
-        + _tags("tagged_serial", 2, (1,)),
+        INTEGRAL_TAGS: _tags("parent_serial", 1, (1, 2))
+        + _tags("parent_serial", 2, (1,)),
     },
     1: {
         SOLUTION: [_solution(2, 2, -5.0, True)],
         SOLUTION_TAGS: _tags("solution_serial", 2, (1, 2)),
         SOLUTION_VALUE: _values(2, (21, 22, 23, 24)),
         INTEGRAL: [_integral(3, 2, 0.5)],
-        INTEGRAL_TAGS: _tags("tagged_serial", 3, (1,)),
+        INTEGRAL_TAGS: _tags("parent_serial", 3, (1,)),
     },
 }
 
```

#### (m3)

```diff
diff --git a/runregistrykit/tests/test_store_retire.py b/runregistrykit/tests/test_store_retire.py
index 979dbce..e107748 100644
--- a/runregistrykit/tests/test_store_retire.py
+++ b/runregistrykit/tests/test_store_retire.py
@@ -175,7 +175,7 @@ class RetireTestCase(CommandLineTestCase):
             (entry["operation"], entry["from"], entry["to"]),
             ("retire", _repo_path(primary, self.client), None),
         )
-        # every other field, the recorded fingerprint among them, value-identical
+        # every other field, the recorded fingerprint among them, value-identical (D4)
         self.assertEqual(fields.get("fingerprint"), before.get("fingerprint"))
         self.assertEqual(
             {k: v for k, v in fields.items() if k not in ("retired", "history")},
```

#### (m4)

```diff
diff --git a/runregistrykit/tests/data/known_hits.json b/runregistrykit/tests/data/known_hits.json
index 5ec8026..da09b50 100644
--- a/runregistrykit/tests/data/known_hits.json
+++ b/runregistrykit/tests/data/known_hits.json
@@ -1,7 +1,13 @@
 {
   "owners": "none: the package and its tests hold no known hit, and a hit in any file fails its scan",
   "known hits": {
-    "test_no_code_name": [],
+    "test_no_code_name": [
+      [
+        "runregistrykit/tests/store_fixtures.py",
+        "a3_shaped",
+        1
+      ]
+    ],
     "test_no_string_or_docstring": [],
     "test_no_comment": [],
     "test_no_citation": [],
```

#### (m5)

```diff
diff --git a/runregistrykit/tests/test_package_imports.py b/runregistrykit/tests/test_package_imports.py
index 3f66661..eee601a 100644
--- a/runregistrykit/tests/test_package_imports.py
+++ b/runregistrykit/tests/test_package_imports.py
@@ -27,7 +27,7 @@ MODULES = ("__init__.py", "stores.py", "__main__.py", "client.py", "fingerprint.
 # reads from the vocabulary file (`test_package_is_generic.project_packages`), so that the check
 # is the same for every client and this module names none.
 FORBIDDEN = tuple(
-    sorted({"ray", "sqlalchemy", "datastorekit", "config"} | project_packages())
+    sorted({"ray", "sqlalchemy", "datastorekit", "config", "json"} | project_packages())
 )
 
 # A subprocess that is not broken takes a fraction of a second; one that imports `ray` by mistake
```

#### (m6)

```diff
diff --git a/runregistrykit/tests/store_fixtures.py b/runregistrykit/tests/store_fixtures.py
index bc9ad88..6568a05 100644
--- a/runregistrykit/tests/store_fixtures.py
+++ b/runregistrykit/tests/store_fixtures.py
@@ -54,7 +54,6 @@ def hand_written_shaped(directory: Path) -> dict:
             "stdout": "var/runs/pilot-run/run.out",
             "pid": "var/runs/pilot-run/run.pid",
         },
-        "note": "Pilot: measure cost first.",
         "run_history": [
             {
                 "started": "2026-09-20T21:03:04+01:00",
```

## Observations not acted on

1. **`test_package_imports.py` no longer imports without `datastorekit`.** It now has
   `from runregistrykit.tests.test_package_is_generic import project_packages` (line 17), and the
   guard has `from datastorekit import contract` at module scope (`test_package_is_generic.py:64`).
   The module held only the standard library and the package before. U13 (open, for 06) plans a CI
   job running the core's tests with no `datastorekit`; this is the core's own import test. Opened
   as `[05c-the-import-test-needs-datastorekit]`, owner 06; the prompt and the brief say to follow
   section 2.4 as written.
2. **The brief's id count** (nine) is eight (deviation 15).
3. **`PROVENANCE.md`'s preamble** says the package's docstrings and comments "still
   cite" SGK until prompt 05 rewrites them, which 05b made untrue for the package and this prompt
   for the tests. Not in 05c's scope (the prompt changes `PROVENANCE.md` as section 2.7 says); left
   for 08's close-out.
4. **`known_hits.json`'s mechanism is now a list of empty lists**, as DatastoreKit's guard kept
   after its rewrite: the 05a writer and its refusal to overwrite remain the way a future known
   hit would be recorded.

## State handed to the next prompt

- The package and its tests name no client: the guard's five scans find 0 hits in 24 Python files, and
  `known_hits.json` holds no entry in any scan. A new hit in any file fails its scan.
- The suite is **276**, `Ran 276 tests in 88.5s ... OK`, per module as above; `black --check
  runregistrykit docs` is clean at 26 files.
- 06 (the release) owns `[05c-the-import-test-needs-datastorekit]`: how its core job, with no
  `datastorekit`, runs `test_package_imports.py` (the module imports the guard, which imports
  `datastorekit`), with U13.
- Open issues: **3** (`[00-the-shard-fixtures-reach-into-shardedpool]`, none;
  `[00-a-refusal-matches-datastorekit-message-text]`, none; `[05c-the-import-test-needs-datastorekit]`, 06).
- The carried fixture's private `ShardedPool` attributes are untouched (their lines are in the
  board's section 3).
- No tag, no push.
