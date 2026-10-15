# Log — prompt 05b: the package prose and the rules

**Subject:** Rewrite the package's prose in its own terms, widen the citation scan, and state the rules in the README
**Commit:** `1120fb3` (on `main`, after `bcc0c0a`)
**Date:** 2026-10-15
**Agent:** Claude Sonnet 5.5, dispatched by the orchestrator with its brief and the orchestration
note's section 0 (`brief-05b-section0.md`)
**Result:** **landed.** The docstrings and comments of `runregistrykit/__init__.py`, `stores.py` and
`fingerprint.py` no longer name or cite any client, campaign, prompt, decision, issue tag, script,
store or incident date: `known_hits.json` has **no entry for a package module in any scan** (the
widened one included), and the package modules' code is unchanged (`ast` with docstrings removed
equals `c735acf`'s) but for the one string constant of `DatastoreKitFingerprinter.describe`, which now
points at `datastorekit.store_inventory.read_inventory` instead of a client's `main.py --inventory`.
The guard's citation pattern gains the three forms of U17 (a capital `Prompt NN`, a decision id, an
issue tag), which find **18 more hits in 11 entries of the tests**, listed for 05c. `README.md`
gains "The rules" and "The public names"; `PROVENANCE.md` gains 05b's section and "Where the
prose's citations pointed". The suite: **275 -> 276** (`275 + 1`, `Ran 276 tests ... OK`).
(m1)-(m8) each fail at least one test. No stop condition was met. `[00-package-prose-names-sgk]` is
closed; `[02-the-ported-tests-name-sgk]` is narrowed; nothing opened; `docs/OPEN_ISSUES.md` goes
from 4 to **3**.

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | docstrings and comments only (124 lines changed): the module docstring (rules by the README's name, the layout under the client's runs root, the two manifest fields, `campaign` and `prompt` as the client's names, the example's `campaign="example"`); the section comments; `now_iso`, `pid_alive`, `package_provenance`, `Run.results_path`, `heartbeat`, `record`, `known`, `begin` and the comment in `begin` |
| `runregistrykit/stores.py` | docstrings and comments only: the module docstring (owner, the legacy `datastore`, `amend_sidecar`, the fingerprint), `_FIELD_OWNERS`' comment, `_amend_slot_problems`, `_store_files`, the three section comments, `_SHARDS_TABLE_UNREADABLE`'s, `_find_references`, `_retire_failure`, `retire_store` and `amend_sidecar` (the two docstrings of section 2.5) |
| `runregistrykit/fingerprint.py` | the one message of `describe` (section 2.4) and `load_fingerprinter`'s list of refusals (the class refusal) |
| `runregistrykit/tests/test_package_is_generic.py` | the citation pattern's three new forms, built from parts; its docstring paragraph; the citation test's samples (as subtests) |
| `runregistrykit/tests/test_fingerprinter.py` | one test, `TestProtocolAndLoader.test_describe_points_a_problem_to_the_stores_inventory_reader` |
| `runregistrykit/tests/data/known_hits.json` | rewritten by 05a's writer: no package-module entry; the tests' 05a entries plus the widened scan's 18 hits in 11 entries |
| `README.md` | "The rules" and "The public names", before "Licence"; nothing else |
| `PROVENANCE.md` | 05b's section under "Since the import"; "Where the prose's citations pointed" |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

No file is added or removed under `runregistrykit/`. Not touched: any other test module or fixture,
`client_vocabulary.json`, `docs/extraction/measure_client_vocabulary.py`, `compare_with_source.py`,
`pyproject.toml`, `LICENSE`, `.gitignore`, `.idea/`, `CLAUDE.md`, the campaign README, the prompt,
`prompts/extraction/orchestrator/`.

**The widened forms** (section 2.2), each built from parts in the guard so that its own text holds no
citation: `_PROMPT.capitalize()` (`Prompt` or `Prompts`, a space, two digits, after `\b`);
`_DECISION_LETTERS = "[CDGQU]"` with `\d{1,2}\b` after `\b` (a decision id as a whole word); and
`_TAG_OPEN + r"\d\d[a-z]?-[a-z0-9-]+" + _TAG_CLOSE` (an issue tag). The module docstring describes
them in words. `TestTheRules`' citation test gains, as further samples of the same loop (subtests,
so no new test method), what it must find (a capital `Prompt` and `Prompts`, `D4`, `U9`, `C12`, a
decision in parentheses, two tags) and what it must not (`Prompt` with no number, a capital with
one digit or no space, `E4`, `D123`, `d4`, `xD4`, `D4x`, a bare `D`, a tag with no digits, one digit,
no letters after the hyphen, or no hyphen).

**The per-scan totals**, hits (file-word entries):

| Scan | Package modules before (05a's guard) | with the widened scan, on the old tree | after | Tests before | after |
|---|---|---|---|---|---|
| code names | 0 | 0 | 0 | 29 (14) | 29 (14) |
| strings and docstrings | 26 (14) | 26 (14) | **0** | 67 (36) | 67 (36) |
| comments | 8 (6) | 8 (6) | **0** | 1 (1) | 1 (1) |
| citations | 35 (10) | 46 (17) | **0** | 40 (32) | **58 (43)** |
| imports | 0 | 0 | 0 | 0 | 0 |

At the prompt's "At writing": package 69 hits in 30 entries plus 11 in 7 for the widened forms, tests
137 in 83 plus 18 in 11. Measured here: package 69 + 11 = 80 hits before, 0 after; tests 137 in 83
before, **155 in 94** after (29 + 67 + 1 + 58; 14 + 36 + 1 + 43). The 18 are exactly the prompt's:
`test_client_root.py` `Q3`, `U9`; `test_fingerprinter.py` `D4` x2, `U14` x2, `U7` x2 and
`[02-the-sidecar-readers-guards-are-unpinned]`; `test_store_amend.py` `D5`;
`test_store_copy_move.py` `C3`; `test_store_retire.py` `D4` x3, `D6` x3;
`test_store_retire_references.py` `[10-store-retire-reports-every-tombstone-as-a-reference]`.

## Deviations from the prompt

The note's corrections and readings (1-12) are recorded as found; the rest are this agent's.

1. **Correction 1: the widened trial, measured again, agrees.** The guard's widened patterns, run
   over the 05a tree before any prose changed (a scan of the five modules and the tests, the
   package's citation hits going from 35 in 10 entries to 46 in 17), give the prompt's figures:
   package 11 hits in 7 entries, tests 18 in 11. No test file's entry differs from them.
   **STRUCTURALLY REQUIRED** (a reading, no change).
2. **Correction 2: the forms are built from parts; the self-scan is clean.** `_DECISION_LETTERS =
   "[CDGQU]"` is a character class with no digit after it in the source; the samples are built from
   a letter and a digit string, a tag from its pieces; the near misses the correction names are each
   asserted. `test_this_module_holds_no_known_hit` passes. **IMPLEMENTATION CHOICE.**
3. **Correction 3: the config's refusals, exactly.** `retire_store`'s and `amend_sidecar`'s
   docstrings say that every refusal is a `RuntimeError` and comes before anything is written, that
   the config's (`find_client_root`'s: no config found or one that cannot be used;
   `require_fingerprinter`'s: none named; and, in a first retirement, `load_fingerprinter`'s,
   step 3) are `ConfigError`s in the config's own words, and that every other refusal ends as
   stated. No message changed. **IMPLEMENTATION CHOICE.**
4. **Correction 4: the class refusal in `load_fingerprinter`'s list**, after the missing attribute
   and before the protocol check, as the code orders them. **STRUCTURALLY REQUIRED.**
5. **Correction 5: the README's durability rule is the client's.** Rule 5 says what a client does
   (keep its runs root under its own root, ignored by git, never a scratchpad or `/tmp`) and says
   that the package keeps an absolute `runs_root` or `stores_root` as it is and does not refuse
   another place (`client.py:34-35`); rule 1 says the package supports the habit of `list` and
   cannot enforce it. **IMPLEMENTATION CHOICE.**
6. **Correction 6: the public names, as the modules' `__all__` stand** (20, 26, 4, 4 and 1 names,
   each listed), and the two lookups made at call time: `Run.finish(..., fingerprint=True)`
   (through `_fingerprint_results`) importing `runregistrykit.stores` and calling
   `fingerprint_store`, and `begin()` with `results` importing it and calling `read_sidecar`. The
   README promises nothing about either. **IMPLEMENTATION CHOICE.**
7. **Correction 7: `PROVENANCE.md`'s table is "as cited at `c735acf`".** The SGK record in each row
   is the old prose's own citation; no SGK file was read to verify one, and only SGK's `CLAUDE.md`
   and `prompts/run-registry/README.md` were read at all (at `14bcac0`). **STRUCTURALLY REQUIRED.**
8. **Correction 8: the new test adds no hit.** It is placed in `TestProtocolAndLoader`, the existing
   class of the shipped fingerprinter (no existing class tests `describe`; the stub's `describe` at
   `test_fingerprinter.py:73-74` is a stub). It builds a fingerprint of one class and one problem
   from literals (`Alpha`, `unreadable`), and checks the problems line, the `!!` line, that
   `problems: none` is absent and that no line names a `.py` file. `known_hits.json` has no new entry
   for `test_fingerprinter.py` but the widened scan's. **IMPLEMENTATION CHOICE.**
9. **Correction 9: `known_hits.json` by 05a's writer, unchanged.** The file was deleted, then the
   writer (below, text as in 05a's log, `owners` string included) was run once the guard and the
   five modules were final. **STRUCTURALLY REQUIRED.**
10. **Correction 10: section 3.3's script** compares `ast.dump` with every docstring removed
    (module, class, function) against `git show c735acf:<path>`, and reports the `Constant` that
    differs. Below. **STRUCTURALLY REQUIRED.**
11. **Correction 11: section 3.4's grep** is accounted for line by line below; `section` has no
    match (the section sign is gone). **STRUCTURALLY REQUIRED.**
12. **Correction 12: the suite.** 275 + 1 = **276**, because the new citation samples are subtests
    of the existing citation test and the only new method is section 2.4's. **IMPLEMENTATION
    CHOICE.**
13. **`now_iso` and the checkpoint prose use general terms for pedigree.** "The choice of a script
    that checkpoints its own cells, generalised" replaces the citation of that script's
    `load_checkpoint`, and "a manifest written by hand" replaces the hand-written manifest's file
    name; the files themselves are in `PROVENANCE.md`'s table. No reason or fact is dropped.
    **IMPLEMENTATION CHOICE.**
14. **The legacy `datastore` sentence** says "the rule for a legacy shard record's path, applied to
    JSON" where it said "prompt 01's rule for legacy shard records", the rule itself ("read by its
    final component, never as a path") being stated in the same sentence. **IMPLEMENTATION
    CHOICE.**
15. **`_store_files`' docstring** says it copies or moves the store's files with a `ShardedPool`
    method, its refusals coming through unchanged, for "Prompt 02's interface" (the module
    docstring says copy and move call `ShardedPool.copy_store` and `move_store`).
    **IMPLEMENTATION CHOICE.**
16. **`PROVENANCE.md`'s section says "this commit"** where earlier sections give a SHA; the
    orchestrator substitutes it. **STRUCTURALLY REQUIRED.**
17. **A second mutation of the agent's own was prepared and not run.** (m8b), dropping the issue
    tag's optional letter, failed to apply (its search string did not match the source's spacing
    of the pattern) and was discarded; (m8) is the agent's own. **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT.

## Verification performed

**1. The suite.** Before (at `bcc0c0a`, the orchestrator's measure at `92f173c`): `Ran 275 tests in
90.564s`, OK. After: `Ran 276 tests in 89.235s`, **OK** (`./venv/bin/python -m unittest discover -s
runregistrykit/tests -t .`, from the root, in the foreground). Per module, counted by the loader:
`test_client_root` 27, `test_fingerprinter` 31 (30 + 1), `test_package_imports` 3,
`test_package_is_generic` 22, `test_public_names` 8, `test_run_registry` 29, `test_store_amend` 21,
`test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
`test_store_fingerprint` 29, `test_store_retire` 41, `test_store_retire_references` 10,
`test_store_sidecar` 17: **276**.

**2. Nothing outside temporary directories.** `git status --short --ignored` was the same before and
after the run (apart from the files this work changes, none of them new): `prompts/.DS_Store`,
`runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
`venv/`. No `var/`; `git worktree list` this checkout alone; no Ray process (`ps` for `raylet`,
`gcs_server` and `ray::`); `RAY_ADDRESS` unset.

**3. The code is unchanged.** `ast_check.py`, in the scratchpad (`agent-05b/`), run from the
repository root with the venv's interpreter:

```python
"""For each package module: ast.dump of the working tree's module with every docstring removed,
against the same of `git show c735acf:<path>`; reports the Constants that differ."""
import ast, subprocess, sys

MODULES = ["__init__", "stores", "client", "fingerprint", "__main__"]


def strip(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return tree


def consts(tree):
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant)]


bad = 0
for m in MODULES:
    path = f"runregistrykit/{m}.py"
    new = strip(ast.parse(open(path).read()))
    old = strip(ast.parse(subprocess.run(["git", "show", f"c735acf:{path}"], capture_output=True, text=True, check=True).stdout))
    same = ast.dump(new) == ast.dump(old)
    print(path, "IDENTICAL" if same else "DIFFERS")
    if not same:
        a, b = consts(old), consts(new)
        assert len(a) == len(b), (len(a), len(b))
        for x, y in zip(a, b):
            if x != y:
                print("   was:", repr(x)); print("   now:", repr(y))
        bad += 1
print("modules differing:", bad)
```

Its output:

```
runregistrykit/__init__.py IDENTICAL
runregistrykit/stores.py IDENTICAL
runregistrykit/client.py IDENTICAL
runregistrykit/fingerprint.py DIFFERS
   was: "problems: (counts only; the store's own text is in `main.py --inventory`)"
   now: "problems: (counts only; the store's own text is in the store's inventory, which `datastorekit.store_inventory.read_inventory` returns)"
runregistrykit/__main__.py IDENTICAL
modules differing: 1
```

**4. The prose, by the guard and by grep.** The guard's scans over the five modules alone find
nothing (package 0 in every scan, above). Then the case-insensitive grep over the five modules
(`prompt`, `campaign`, `README`, `CLAUDE`, `log's`, `A3`, `backup`, `pipeline`, `main.py`,
`realistic`, `handover`, `scratchpad`, `2026-`, `§`; it matches code lines too, and the 29 lines it
finds are all listed), each kept for the reason after it:

```
__init__.py:18:The rules this package exists to support are in this repository's `README.md`, "The rules", and
__init__.py:29:session scratchpad or in `/tmp` (a datastore written into a scratchpad is lost with it):
__init__.py:31:    var/runs/<campaign>-<prompt>-<slug>-<YYYYMMDDTHHMMSS>/
__init__.py:40:the job's results live in — a datastore the job's pipeline writes — which this package names and
__init__.py:42:may have either, both or neither. `campaign` and `prompt` are the client's names for a body of work
__init__.py:49:        campaign="example", prompt="01", slug="smoke",
__init__.py:125:def run_id(campaign, prompt, slug, when=None) -> str:
__init__.py:126:    """`<campaign>-<prompt>-<slug>-<YYYYMMDDTHHMMSS>`: it sorts, and a stranger reading
__init__.py:129:    return "-".join((slugify(campaign), slugify(prompt), slugify(slug), stamp))
__init__.py:175:    An editable install is recorded, not refused: the registry records (the README's rules).
__init__.py:255:# liveness, by pid and heartbeat and never by a command-line match (the README's rule on liveness)
__init__.py:264:    a job that was already dead (the README's rule on liveness).
__init__.py:385:        """The durable thing this job's results live in — a datastore the job's pipeline writes —
__init__.py:386:        which the registry names. A datastore once written into a session scratchpad was lost with
__init__.py:411:        `stage` is for a job that has no total to count against — a pipeline reports progress per
__init__.py:495:        launch and never re-taken (the README's rule on provenance), so that a resume can tell
__init__.py:499:        by name: the caller who reaches here is usually one who copied the pipeline pattern — whose
__init__.py:553:        is the failure a resume then acts on by recomputing everything, which for one pipeline run
__init__.py:605:    campaign,
__init__.py:606:    prompt,
__init__.py:632:    `results` is the **durable thing the job's results live in** — for a registered pipeline run,
__init__.py:636:    and is sometimes already solved, as a pipeline's datastore already is). It exists because a
__init__.py:637:    datastore written into a session scratchpad was lost with it, with nothing on disk saying where
__init__.py:642:    have caught something in the failures the README's rules answer; there are no others.
__init__.py:674:    units, something weaker for a Ray-parallel pipeline whose parent may be blocked inside
__init__.py:683:    identifier = run_id(campaign, prompt, slug, when)
__init__.py:711:        "campaign": campaign,
__init__.py:712:        "prompt": str(prompt),
__main__.py:66:        # reporting a stage instead (a pipeline run, which has no denominator) or has not got to
```

- **A manifest key, a parameter or the run id's form** (a name the package keeps): `__init__.py`
  31, 49, 125, 126, 129, 605, 606, 683, 711, 712 (`campaign`, `prompt`; the layout, the example's
  `campaign="example"`, `run_id`'s and `begin()`'s parameters and the manifest's keys); `:42` says
  what they are, the client's names for a body of work and for a step of it.
- **This repository's README, by section name** (the rules, never a section number): `__init__.py`
  18 ("The rules"), 175, 255, 264, 495, 642 ("the README's rule on liveness", "on provenance",
  "the README's rules").
- **A reason, in general terms**: `__init__.py` 29, 386, 637 (a datastore written into a session
  scratchpad is lost with it, with nothing on disk saying where the results went; the README's rule
  on durability); 40, 385, 411, 499, 553, 632, 636 and `__main__.py` 66 (`pipeline`: a job's
  pipeline, a pipeline's datastore, a run of 10 h 33 m, as general terms, no client's); 674 (a
  Ray-parallel pipeline whose parent may block inside `ray.get`, the existing text).
- **Gone**: every `§`, `2026-`, `A3`, `backup`, `main.py`, `realistic`, `handover`, `CLAUDE`,
  `log's` (no match above). `.manifest.json` is in no non-docstring string but `sidecar_path`'s.

**5. The known hits.** The file was deleted and rewritten by 05a's writer, run from the repository
root:

```
./venv/bin/python /private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/842ac11b-b80e-4b23-b3f1-090e7c5cd35f/scratchpad/agent-05b/write_known_hits.py
```

Its output: `test_no_code_name package 0 tests 29`, `test_no_string_or_docstring package 0 tests 67`,
`test_no_comment package 0 tests 1`, `test_no_citation package 0 tests 58`,
`test_every_import_is_allowed package 0 tests 0`. The writer's text, **unchanged** from 05a's log
(extracted from it with `awk`; its `owners` string included):

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
    "owners": "entries under runregistrykit/tests/ are the tests' to remove (prompt 05c); the rest are the package modules' (prompt 05b)",
    "known hits": {name: g.count_hits(h) for name, h in hits.items()},
}
g.KNOWN_HITS.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
for name, h in hits.items():
    pk = [x for x in h if not g.is_test(x[0])]
    ts = [x for x in h if g.is_test(x[0])]
    print(name, "package", len(pk), "tests", len(ts))
```

Checked in Python against the file before: the `owners` string is equal; in every scan the tests'
entries are 05a's with only additions, and only under `test_no_citation` (18 hits in 11 entries, the
list above); no entry for a package module in any scan. The diff of the file (`git diff` of the
rewrite against 05a's):

```diff
diff --git a/runregistrykit/tests/data/known_hits.json b/runregistrykit/tests/data/known_hits.json
index 70396cd..948d223 100644
--- a/runregistrykit/tests/data/known_hits.json
+++ b/runregistrykit/tests/data/known_hits.json
@@ -74,76 +74,6 @@
       ]
     ],
     "test_no_string_or_docstring": [
-      [
-        "runregistrykit/__init__.py",
-        "A3",
-        4
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "datastore-portability",
-        2
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "handover",
-        3
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "handover-A3-baseline-lambdacdm",
-        2
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "main.py",
-        2
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "realistic_large_x",
-        2
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "run-registry",
-        3
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "store-fingerprint",
-        1
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "store-retirement",
-        1
-      ],
-      [
-        "runregistrykit/fingerprint.py",
-        "main.py",
-        1
-      ],
-      [
-        "runregistrykit/stores.py",
-        "A3",
-        2
-      ],
-      [
-        "runregistrykit/stores.py",
-        "datastore-portability",
-        1
-      ],
-      [
-        "runregistrykit/stores.py",
-        "store-fingerprint",
-        1
-      ],
-      [
-        "runregistrykit/stores.py",
-        "store-retirement",
-        1
-      ],
       [
         "runregistrykit/tests/neutral_store.py",
         "log10_tol",
@@ -326,36 +256,6 @@
       ]
     ],
     "test_no_comment": [
-      [
-        "runregistrykit/__init__.py",
-        "handover",
-        1
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "realistic_large_x",
-        1
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "store-retirement",
-        1
-      ],
-      [
-        "runregistrykit/stores.py",
-        "A3",
-        1
-      ],
-      [
-        "runregistrykit/stores.py",
-        "store-fingerprint",
-        1
-      ],
-      [
-        "runregistrykit/stores.py",
-        "store-retirement",
-        3
-      ],
       [
         "runregistrykit/tests/test_store_amend.py",
         "A3",
@@ -364,83 +264,63 @@
     ],
     "test_no_citation": [
       [
-        "runregistrykit/__init__.py",
-        "prompts/",
-        5
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "\u00a70",
-        12
-      ],
-      [
-        "runregistrykit/__init__.py",
-        "\u00a76",
-        3
-      ],
-      [
-        "runregistrykit/stores.py",
-        "prompt 01",
-        2
+        "runregistrykit/tests/shard_store_fixtures.py",
+        "prompt 03",
+        1
       ],
       [
-        "runregistrykit/stores.py",
+        "runregistrykit/tests/store_fixtures.py",
         "prompt 03",
         1
       ],
       [
-        "runregistrykit/stores.py",
-        "prompt 04",
-        6
+        "runregistrykit/tests/store_fixtures.py",
+        "prompt 15",
+        1
       ],
       [
-        "runregistrykit/stores.py",
+        "runregistrykit/tests/store_fixtures.py",
         "prompts/",
         1
       ],
       [
-        "runregistrykit/stores.py",
+        "runregistrykit/tests/store_fixtures.py",
         "\u00a72",
-        2
-      ],
-      [
-        "runregistrykit/stores.py",
-        "\u00a75",
         1
       ],
       [
-        "runregistrykit/stores.py",
-        "\u00a76",
-        2
+        "runregistrykit/tests/store_fixtures.py",
+        "\u00a73",
+        1
       ],
       [
-        "runregistrykit/tests/shard_store_fixtures.py",
-        "prompt 03",
+        "runregistrykit/tests/test_client_root.py",
+        "Q3",
         1
       ],
       [
-        "runregistrykit/tests/store_fixtures.py",
-        "prompt 03",
+        "runregistrykit/tests/test_client_root.py",
+        "U9",
         1
       ],
       [
-        "runregistrykit/tests/store_fixtures.py",
-        "prompt 15",
-        1
+        "runregistrykit/tests/test_fingerprinter.py",
+        "D4",
+        2
       ],
       [
-        "runregistrykit/tests/store_fixtures.py",
-        "prompts/",
-        1
+        "runregistrykit/tests/test_fingerprinter.py",
+        "U14",
+        2
       ],
       [
-        "runregistrykit/tests/store_fixtures.py",
-        "\u00a72",
-        1
+        "runregistrykit/tests/test_fingerprinter.py",
+        "U7",
+        2
       ],
       [
-        "runregistrykit/tests/store_fixtures.py",
-        "\u00a73",
+        "runregistrykit/tests/test_fingerprinter.py",
+        "[02-the-sidecar-readers-guards-are-unpinned]",
         1
       ],
       [
@@ -463,6 +343,11 @@
         "\u00a70",
         2
       ],
+      [
+        "runregistrykit/tests/test_store_amend.py",
+        "D5",
+        1
+      ],
       [
         "runregistrykit/tests/test_store_amend.py",
         "prompt 04",
@@ -503,6 +388,11 @@
         "\u00a73",
         1
       ],
+      [
+        "runregistrykit/tests/test_store_copy_move.py",
+        "C3",
+        1
+      ],
       [
         "runregistrykit/tests/test_store_copy_move.py",
         "prompt 01",
@@ -543,11 +433,26 @@
         "prompt 04",
         1
       ],
+      [
+        "runregistrykit/tests/test_store_retire.py",
+        "D4",
+        3
+      ],
+      [
+        "runregistrykit/tests/test_store_retire.py",
+        "D6",
+        3
+      ],
       [
         "runregistrykit/tests/test_store_retire.py",
         "prompt 03",
         1
       ],
+      [
+        "runregistrykit/tests/test_store_retire_references.py",
+        "[10-store-retire-reports-every-tombstone-as-a-reference]",
+        1
+      ],
       [
         "runregistrykit/tests/test_store_retire_references.py",
         "prompt 06",
```

**6. The mutations.** Below (the deliberate-breakage record).

**7. `black`.** `./venv/bin/black --check runregistrykit docs`: 26 files would be left unchanged.

**Isolation.** Nothing was installed. SGK was read only through `git -C
/Users/ds283/Documents/Code/SecondaryGWKit show 14bcac0:<path>` for `CLAUDE.md` and
`prompts/run-registry/README.md`; no other client, DatastoreKit or RayPoolKit was read, and none was
edited, imported or run. Every scratch file was in `agent-05b/` of the session scratchpad; no scratch
`.py` went under `runregistrykit/` or `docs/`. Nothing pushed or tagged.

**The mapping of rule to failure** that the README uses (SGK's `CLAUDE.md` rules, and `prompts/run-registry/README.md` section 0):

| README rule | The failure it answers |
|---|---|
| 1 Discovery | failure 2 (a run orphaned from its agent, nothing on disk saying what it was) and section 0.3 (a registry nobody reads is worse than none) |
| 2 Liveness | failure 3 (nineteen poll loops, fifteen on a dead job, two for five hours on a script that ended in a minute, one for a file stuck at sixteen of seventeen lines) |
| 3 Launch | failure 2 again (a job without its record first leaves nothing, and a crash in its first second nothing at all) |
| 4 Do not babysit | failure 3's cost (each loop a full turn re-sending an entire context) |
| 5 Durability | failure 1 (a three-hour measurement held in memory, killed at 4 h 57 m, one line of output) and failure 4 (a datastore in a scratchpad, a 462-row census gone) |
| 6 Provenance | section 0.1 (the stamp reused all sixty cells and proved byte-identity in four seconds) and failure 5 (resumption assumed, a 10 h 33 m run resumed and crashed on a read-back path never taken) |

The README says once where they happened: in the project the registry was extracted from, with a
link to `PROVENANCE.md`, and it names no client's script, store or campaign.

## The deliberate-breakage record

Each diff below is exactly as applied, against this commit's blobs (the eight changed files staged
first, so that `git diff` shows only the mutation and its `index` lines are this commit's). Each was
checked in `bash` with `git apply -R --check` while applied and `git apply --check` after the
revert (a clean tree at this commit), and `git status` held only the staged work after each. The
suite was run on each as mutated. None is committed.

| # | Mutation | The suite | Failing tests |
|---|---|---|---|
| (m1) | `(Prompt 07)` added to a comment of `client.py` | `Ran 276 tests ... FAILED (failures=1)` | FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_citation` |
| (m2) | `(D4)` added to a comment of `client.py` | `Ran 276 tests ... FAILED (failures=1)` | FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_citation` |
| (m3) | an issue tag of the board's form added to `client.py`'s module docstring | `Ran 276 tests ... FAILED (failures=1)` | FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_citation` |
| (m4) | the capital form dropped from the citation pattern | `Ran 276 tests ... FAILED (failures=4)` | FAIL `runregistrykit.tests.test_package_is_generic.TestTheRules.test_a_citation_is_a_path_a_numbered_prompt_or_a_section` (source="x = 'Prompt 07'"); FAIL `runregistrykit.tests.test_package_is_generic.TestTheRules.test_a_citation_is_a_path_a_numbered_prompt_or_a_section` (source='x = 1  # Prompt 07'); FAIL `runregistrykit.tests.test_package_is_generic.TestTheRules.test_a_citation_is_a_path_a_numbered_prompt_or_a_section` (source="x = 'Prompts 07'"); FAIL `runregistrykit.tests.test_package_is_generic.TestTheRules.test_a_citation_is_a_path_a_numbered_prompt_or_a_section` (source='x = 1  # Prompts 07') |
| (m5) | one of the widened scan's known entries for the tests (`test_client_root.py`, `Q3`) removed from `known_hits.json` | `Ran 276 tests ... FAILED (failures=1)` | FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_citation` |
| (m6) | `main.py --inventory` restored in `describe`'s line | `Ran 276 tests ... FAILED (failures=2)` | FAIL `runregistrykit.tests.test_fingerprinter.TestProtocolAndLoader.test_describe_points_a_problem_to_the_stores_inventory_reader`; FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_string_or_docstring` |
| (m7) | `# retirement (store-retirement prompt 03)` restored above the retirement section in `stores.py` | `Ran 276 tests ... FAILED (failures=2)` | FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_citation`; FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_comment` |
| (m8) | the agent's own, of the widened rule: the decision letters made `[CDGQ]`, dropping `U` | `Ran 276 tests ... FAILED (failures=3)` | FAIL `runregistrykit.tests.test_package_is_generic.TestThePackageNamesNoClient.test_no_citation`; FAIL `runregistrykit.tests.test_package_is_generic.TestTheRules.test_a_citation_is_a_path_a_numbered_prompt_or_a_section` (source="x = 'U9'"); FAIL `runregistrykit.tests.test_package_is_generic.TestTheRules.test_a_citation_is_a_path_a_numbered_prompt_or_a_section` (source='x = 1  # U9') |

### The diffs

#### (m1) `(Prompt 07)` added to a comment of `client.py`

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..bd6bd6a 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -68,6 +68,7 @@ from dataclasses import dataclass
 
 __all__ = ["CONFIG_FILE", "ClientRoot", "ConfigError", "find_client_root"]
 
+# (Prompt 07)
 CONFIG_FILE = "runregistrykit.toml"
 
 # every key the file may hold, with its default
```

#### (m2) `(D4)` added to a comment of `client.py`

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..011b356 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -68,6 +68,7 @@ from dataclasses import dataclass
 
 __all__ = ["CONFIG_FILE", "ClientRoot", "ConfigError", "find_client_root"]
 
+# (D4)
 CONFIG_FILE = "runregistrykit.toml"
 
 # every key the file may hold, with its default
```

#### (m3) an issue tag of the board's form added to `client.py`'s module docstring

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..6fe05b0 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -13,7 +13,7 @@
 # See the License for the specific language governing permissions and
 # limitations under the License.
 
-"""Where a client's records go: its root, which a `runregistrykit.toml` marks, and that file.
+"""Where a client's records go [00-package-prose-names-sgk]: its root, which a `runregistrykit.toml` marks, and that file.
 
 **The file.** A client marks its root with a file named `runregistrykit.toml`, read with
 `tomllib`. Every key is optional, and an empty file takes every default:
```

#### (m4) the capital form dropped from the citation pattern

```diff
diff --git a/runregistrykit/tests/test_package_is_generic.py b/runregistrykit/tests/test_package_is_generic.py
index a7e094d..b938211 100644
--- a/runregistrykit/tests/test_package_is_generic.py
+++ b/runregistrykit/tests/test_package_is_generic.py
@@ -137,7 +137,6 @@ CITATION = re.compile(
         (
             r"\b" + _DIRECTORY + "/",
             r"\b" + _PROMPT + r" \d\d",
-            r"\b" + _PROMPT.capitalize() + r" \d\d",
             _SECTION_SIGN + r" ?\d",
             r"\b" + _DECISION_LETTERS + r"\d{1,2}\b",
             _TAG_OPEN + r"\d\d[a-z]?-[a-z0-9-]+" + _TAG_CLOSE,
```

#### (m5) one of the widened scan's known entries for the tests (`test_client_root.py`, `Q3`) removed from `known_hits.json`

```diff
diff --git a/runregistrykit/tests/data/known_hits.json b/runregistrykit/tests/data/known_hits.json
index 948d223..e329a34 100644
--- a/runregistrykit/tests/data/known_hits.json
+++ b/runregistrykit/tests/data/known_hits.json
@@ -293,11 +293,6 @@
         "\u00a73",
         1
       ],
-      [
-        "runregistrykit/tests/test_client_root.py",
-        "Q3",
-        1
-      ],
       [
         "runregistrykit/tests/test_client_root.py",
         "U9",
```

#### (m6) `main.py --inventory` restored in `describe`'s line

```diff
diff --git a/runregistrykit/fingerprint.py b/runregistrykit/fingerprint.py
index fbcd5b7..71dd819 100644
--- a/runregistrykit/fingerprint.py
+++ b/runregistrykit/fingerprint.py
@@ -148,8 +148,7 @@ class DatastoreKitFingerprinter:
                 )
         if fingerprint["problems"]:
             lines.append(
-                "problems: (counts only; the store's own text is in the store's inventory, "
-                "which `datastorekit.store_inventory.read_inventory` returns)"
+                "problems: (counts only; the store's own text is in `main.py --inventory`)"
             )
             for name, kinds in fingerprint["problems"].items():
                 counted = ", ".join(f"{kind} {n}" for kind, n in kinds.items())
```

#### (m7) `# retirement (store-retirement prompt 03)` restored above the retirement section in `stores.py`

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 6d669c4..598c421 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1397,7 +1397,7 @@ def fingerprint_store(
 
 
 # =================================================================================================
-# retirement
+# retirement (store-retirement prompt 03)
 #
 # `retire_store` deletes a closed store's own files through `ShardedPool.delete_store` and keeps
 # its sidecar as a tombstone. The order of the writes is the point: the tombstone, with the list of
```

#### (m8) the agent's own, of the widened rule: the decision letters made `[CDGQ]`, dropping `U`

```diff
diff --git a/runregistrykit/tests/test_package_is_generic.py b/runregistrykit/tests/test_package_is_generic.py
index a7e094d..13e8c7d 100644
--- a/runregistrykit/tests/test_package_is_generic.py
+++ b/runregistrykit/tests/test_package_is_generic.py
@@ -130,7 +130,7 @@ _WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:[.-][A-Za-z0-9_]+)*")
 _DIRECTORY = "prompts"
 _PROMPT = "prompts?"
 _SECTION_SIGN = "\N{SECTION SIGN}"
-_DECISION_LETTERS = "[CDGQU]"
+_DECISION_LETTERS = "[CDGQ]"
 _TAG_OPEN, _TAG_CLOSE = r"\[", r"\]"
 CITATION = re.compile(
     r"|".join(
```

## Observations not acted on

- **`known_hits.json`'s `owners` string is stale.** It says the package modules' entries are 05b's
  and the tests' 05c's. The writer's text was to be unchanged (correction 9), so the string still
  says it, though no package-module entry remains. 05c's rewrite, which empties the file, can
  restate it; the guard's docstring says the same ("Entries under `runregistrykit/tests/` are the
  tests' to remove, the rest the package modules'").
- **The README's "Status" paragraph is stale** (it says the code does not live here yet). It is 06's
  to rewrite with usage and installing, as the prompt says; it is untouched.
- **`PROVENANCE.md` earlier text still says the prose "still cites" SGK until prompt 05 rewrites
  it.** The document is additive (CLAUDE.md rule 6); 05b's section says it was done.
- **The widened scan finds this campaign's own decision ids in the tests** (`Q3`, `U9`, `U14`,
  `U7`, and the tags of an SGK and a package issue, among the 18): the tests cite the campaign's
  decisions as well as SGK's, and 05c rewrites them as it rewrites the rest.
- **A hit is a (line, word) pair**, as 05a recorded: a second occurrence of a known word on a line
  that already holds it is not seen.
- **The new test asserts the message's text in full**, so any reword of `describe`'s problems line
  fails it; that is the point of section 2.4, and the line is the package's own.

## State handed to the next prompt

- **05c** empties the tests' share of `known_hits.json`: **155 hits in 94 entries** (code names 29
  in 14, strings 67 in 36, comments 1 in 1, citations 58 in 43, imports 0), in 14 test modules and
  fixtures; `known_hits.json` is rewritten by 05a's writer (delete the file, run the writer whose
  text is above, from the scratchpad), never by hand, and 05c's log says so. The new
  `test_fingerprinter.py` test names nothing of a client.
- **The package modules** hold no known hit and must stay so; the guard fails on a new one in any of
  its four word scans, with the widened citation forms.
- **Lines moved by 05b** in `stores.py`: `retire_store`'s and `amend_sidecar`'s docstrings are
  longer, so `_SHARDS_TABLE_UNREADABLE`'s uses are `:1677` and `:1727` (assignment `:1410`);
  `fingerprint.py`'s message is `:151-152`; `__init__.py` moved by a few lines in its docstrings.
- **06** rewrites the README's "Status" paragraph and adds usage and installing; the README's two
  new sections are in place, and do not change.
- **The suite** is 276 in about 90 s.
