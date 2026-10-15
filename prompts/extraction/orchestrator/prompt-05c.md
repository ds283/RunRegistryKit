# Orchestrator — prompt 05c, the tests' own names

Read [`../README.md`](../README.md) first: §0.2, §2 (05a–05c, 06), §4 (after 05c), §5 (every rule;
4, 6, 9 and 10 especially), §6.2 (U10, U13, U16, U17). The conventions are
[`prompt-05b.md`](prompt-05b.md)'s and its predecessors'; they are restated in §0 because the agent
reads §0 and not this directory. Where this note and an earlier one differ, this one is right for
05c.

**You do not write code.** You may:
- run the suite, `black --check`, the guard's scans and the tests the log names;
- replay the log's mutation diffs with `git apply`, and revert them;
- export this repository's tree at any commit into the session scratchpad and run the package, the
  guard's functions and scripts of your own there, never committing anything;
- fix small residue in a follow-up commit of your own (§4).

No client, DatastoreKit or RayPoolKit is run, imported, read or edited. Everything 05c needs of SGK
is in the tests' own text.

**The prompt:** [`05c-the-tests-own-names.md`](../05c-the-tests-own-names.md)
**Closes:** `[02-the-ported-tests-name-sgk]` · **Opens:** `[05c-the-import-test-needs-datastorekit]`
(correction 3), and only what else the work finds · **Model:** Sonnet, as the prompt recommends.

**Gate:**
- The prompt's gate: 05b landed (`1120fb3`) and reviewed (`8766714`); `git diff --stat 8766714 HEAD
  -- runregistrykit docs/extraction pyproject.toml PROVENANCE.md CLAUDE.md README.md` empty; U16
  taken; the suite 276 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is renames, neutral data and prose, under a guard that must end with nothing known.** Thirteen
names of a fixed map (sixteen with correction 1), data in four fixtures and tests, one constant made
from the guard's function, and about eighty lines of docstrings and comments. No assertion changes
and the suite stays at 276. The weight of the review is therefore on four things:
- **the assertions are unchanged**: `ast` with docstrings removed, after the map and the data
  replacements, equals `8766714`'s for every file but `test_package_imports.py` (§3 check 2);
- **the known hits are empty and the guard is otherwise unchanged**: its code identical, its
  docstring changed in the one paragraph (§3 checks 4, 5);
- **the prose keeps what each test checks and why**, read line by line against `8766714`, and §3.4's
  greps find only what the log accounts for (§3 check 3);
- **`PROVENANCE.md` maps every rename**, so a reader with SGK's tree can find each test's source
  (§3 check 7).

**What moves on purpose:** the test modules and fixtures under `runregistrykit/tests/` that hold a
client's name, data or citation; `runregistrykit/tests/test_package_is_generic.py`'s module
docstring, its paragraph "The known hits" only; `runregistrykit/tests/data/known_hits.json`;
`PROVENANCE.md`; the log and the records. **Nothing** in any package module,
`client_vocabulary.json`, the measuring script, `compare_with_source.py`, `pyproject.toml`,
`README.md`, `LICENSE`, `.gitignore`, `CLAUDE.md`, the campaign README, the prompt or
`orchestrator/`. `test_public_names.py` names nothing of a client and does not change.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The rename map misses three test methods.** A trial of §2.2's map (whole-word replacement over
   every test file but the guard, in an export of `4ec6406`), then the whole-file grep of §3.4,
   leaves only §2.3's data and §2.5's prose, **and two method names the guard does not flag**
   (`a3` alone is not a forbidden word): `test_store_sidecar.py:372`
   `test_an_a3_shaped_sidecar_keeps_every_unknown_field` and `:500`
   `test_an_a3_shaped_sidecar_through_adopt_copy_and_move`. §3.4 requires `a3` gone from the code,
   so they are renamed. An `ast` scan of every identifier finds one more name that cites a client's
   prompt, as `test_amend_backup_as_prompt_05_will` does: `test_store_copy_move.py:329`
   `test_prompt_02s_refusals_pass_through` (the refusal is DatastoreKit's, "Cannot copy sharded
   datastore … already exist", passed through). Three rows join the map:

   | Old | New | Where |
   |---|---|---|
   | `test_an_a3_shaped_sidecar_keeps_every_unknown_field` | `test_a_hand_written_shaped_sidecar_keeps_every_unknown_field` | `test_store_sidecar.py:372` |
   | `test_an_a3_shaped_sidecar_through_adopt_copy_and_move` | `test_a_hand_written_shaped_sidecar_through_adopt_copy_and_move` | `test_store_sidecar.py:500` |
   | `test_prompt_02s_refusals_pass_through` | `test_datastorekits_refusals_pass_through` | `test_store_copy_move.py:329` |

   Each new name was checked against the guard's 454 forbidden words, whole and split on `_`, and
   collides with nothing. So **nine** test methods are renamed, not six, and nine test ids change
   (the renamed class has one method, itself renamed). The first two are STRUCTURALLY REQUIRED (by
   §3.4), the third an IMPLEMENTATION CHOICE (by §2.5's rule and the map's own precedent), logged.
   No other identifier in the tests names a client (the scan's other matches are the neutral
   store's `INTEGRAL`, `_solver`, `SOLVER_COLUMNS`, which the prompt keeps, and `begin()`'s
   `campaign` and `prompt` parameters).
2. **`QSI` and `TKN` are also used as attributes**, at `test_fingerprinter.py:855-856`
   (`ported.QSI`, `ported.TKN`, in `test_the_baseline_has_no_problem_and_the_ported_names_are_its`).
   §2.2 lists only the definitions; "everywhere it occurs under `runregistrykit/tests/`" covers
   these, and they become `ported.INTEGRAL_CLASS` and `ported.SOLUTION_CLASS`. The guard does not
   flag `QSI` or `TKN`; §3.4's grep is what pins them.
3. **`FORBIDDEN` from the guard brings `datastorekit` into the import test.** The guard imports
   `from datastorekit import contract` at module scope (`test_package_is_generic.py:65`, for
   `PACKAGE_WORDS`). `test_package_imports.py` imports today only the standard library and the
   package. Importing `project_packages` from the guard, as §2.4 says, means that module no longer
   imports without `datastorekit` installed; U13 (open, for 06) plans a CI job running the core's
   tests with no `datastorekit`, and this is the core's own import test. Follow §2.4 as written
   (import the guard's function; the guard is not changed), record it in "Observations not acted
   on", and **open `[05c-the-import-test-needs-datastorekit]`** on the board's §3, owner **06**, with
   the measurement (the two import lines) and the next step (06 decides how its core job runs the
   import test). So the index counts **3** after this commit, not 2.
4. **What `FORBIDDEN` becomes.** The four kept names (`ray`, `sqlalchemy`, `datastorekit`,
   `config`) and every name of `project_packages()` (18 at `4ec6406`, `ObjectFactories`,
   `StoreFixtures` and `RunRegistry` among them), as a sorted tuple or set, so that
   `{FORBIDDEN!r}` in the child's code is a literal the child can evaluate. The comment above it
   says where the names come from. The log states that the check asserts 22 names for 7 and never
   fewer, and §3.3's script reports this file's difference as `FORBIDDEN`'s assignment and the one
   import.
5. **The guard: its docstring paragraph only.** "The known hits" keeps the mechanism (the file,
   its `[file, word, count]` entries, a scan must find exactly its entries, a new hit fails, a
   known hit not found fails) and says the list is now empty in every scan, so any hit in any file
   fails its scan. The sentence "Entries under `runregistrykit/tests/` are the tests' to remove, the
   rest the package modules'" goes. The paragraph cites nothing: `test_this_module_holds_no_known_hit`
   is the check. `ast.dump` of the guard with its docstring removed must equal `8766714`'s.
6. **`known_hits.json`**: delete the file, then run 05a's writer (its text in 05a's log, "How
   `known_hits.json` was written") from the agent's scratchpad subdirectory, with the venv's
   interpreter, from the repository root, once every test file is final. It refuses to overwrite.
   The one change is the `owners` string (§2.6), which names no prompt. Expected output: every scan
   `package 0 tests 0`; the file's five lists empty. The log gives the writer's text, the
   difference from 05a's, its output and `git diff` of the file.
7. **§3.3's script.** For every changed test module and fixture: `ast.dump` with every docstring
   removed (a first statement that is a string expression, of a module, class or function), at the
   commit, against the same of `git show 8766714:<path>` after applying the map (§2.2 and
   correction 1) to every `Name`, `Attribute`, `FunctionDef`, `ClassDef`, `arg`, `alias` and
   `keyword`, and §2.3's replacements (old string → new) to every string `Constant`, f-string parts
   included. Equal for every file but `test_package_imports.py`, whose differences are listed.
   Comments are not in the AST, so this pins the code. The script, its replacement table and its
   output go in the log. The test ids old and new, by loader, are the same 276 but the nine.
8. **§2.3's data, every value.** `hand_written_shaped`'s and `script_written_shaped`'s values are
   listed old → new in the log, every key kept. `assertEqual(len(unknown(legacy)), 10)`
   (`test_store_sidecar.py:379`) pins the key count. New data adds no `a3`, `sweep`, census,
   physics or client path; digests and timestamps stay as they are.
9. **§3.4's greps.** The prose grep is over docstrings and comments of every file under
   `runregistrykit/tests/` but the guard; it will find `campaign` and `prompt` as `begin()`'s
   parameters and manifest keys, which the log groups by reason. The whole-file grep (code
   included) is case-insensitive and over the same files, and must find **nothing**. Run both from
   a script or with `/usr/bin/grep` (this machine's `grep` may be `ugrep`, whose `--include` differs).
10. **The prose.** The rules are 05b's, as §2.5 says. Two lessons of 05b's review: **no line over 100
    columns** in a docstring or comment changed, and **no paragraph broken mid-sentence**; check
    both before committing. "Test N:" and "§3 test N" numbers go, the description stays; "the log's
    interruption table" is stated as what it is (the interruption cases, one method per row); "the
    2026-09-23 failure" as its mechanism (`test_store_retire.py:345`).
11. **`PROVENANCE.md`.** 05c's section goes under "Since the import", after 05b's; the two tables
    (§2.7) after it or as their own `##` section as 05b's "Where the prose's citations pointed" is,
    the log saying which. The renames table has all sixteen rows of the map (§2.2's thirteen and
    correction 1's three), and every changed test id `module.Class.method`, old and new. The
    citations table gives each module's SGK records **as cited at `8766714`**; no SGK file is read.
12. **The suite.** 276 OK in **92.7 s** at `4ec6406`; per module by loader: `test_client_root` 27,
    `test_fingerprinter` 31, `test_package_imports` 3, `test_package_is_generic` 22,
    `test_public_names` 8, `test_run_registry` 29, `test_store_amend` 21,
    `test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
    `test_store_fingerprint` 29, `test_store_retire` 41, `test_store_retire_references` 10,
    `test_store_sidecar` 17. Every count the same after.

**The facts, checked by the orchestrator on 2026-10-15 at `4ec6406`.** Pass them on.
- **In-repository state.** `main` at `4ec6406`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`.
  `venv/`: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39; `git` 2.56.0.
  `black --check runregistrykit docs`: 26 files unchanged.
- **The gate's diff** from `8766714` is empty: only `prompts/` changed since (the prompt's commit),
  so the prompt's line numbers hold.
- **The suite at `4ec6406`:** `Ran 276 tests in 92.731s`, OK; the tree the same after; no Ray.
- **The known hits at `4ec6406`:** code names 29 (14 entries), strings 67 (36), comments 1 (1),
  citations 58 (43), imports 0: **155 in 94**, all under `runregistrykit/tests/`.
- **The map's sites hold** as §2.2 gives them: `store_fixtures.py:37, 86`; `test_store_amend.py:205,
  206`; `test_store_sidecar.py:349`; `test_run_registry.py:566`; `test_store_fingerprint.py:68-70,
  218, 296`; `test_store_retire.py:64`; `neutral_store.py:80, 94, 179, 188, 243, 254, 282` (and the
  column names' uses at `:12-17, 288-289, 307, 329, 342-343, 350`); the raw SQL at
  `test_store_fingerprint.py:224, 254` and `test_store_retire.py:465, 479`. None of the sixteen new
  names occurs anywhere under `runregistrykit/` today.
- **§2.3's sites hold:** `shard_store_fixtures.py:25-27`; `store_fixtures.py:38-83, 87-95`;
  `test_store_sidecar.py:36, 43`; `test_run_registry.py:105, 129, 687-713`;
  `test_store_fingerprint.py:420`.
- **`project_packages()`** returns 18 names at `4ec6406`: `AdaptiveLevin`, `Caching`,
  `CodeComparisonTools`, `ComputeTargets`, `CosmologyConcepts`, `CosmologyModels`, `Datastore`,
  `InflationConcepts`, `Interpolation`, `LiouvilleGreen`, `MetadataConcepts`, `Numerics`,
  `ObjectFactories`, `Quadrature`, `RayTools`, `RunRegistry`, `StoreFixtures`, `Units`.
- **The index.** **3** open now; **3** after (`[02-the-ported-tests-name-sgk]` closed,
  `[05c-the-import-test-needs-datastorekit]` opened), unless the work opens another.
- **Ray.** No Ray process; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** Only §0's list changes; no file added or removed under `runregistrykit/`.
- **(E2) The assertions.** Every test module's and fixture's code equal to `8766714`'s under the
  map and the data replacements, but `FORBIDDEN`; the guard's code unchanged.
- **(E3) The guard.** `known_hits.json` empty in every scan, written by the writer; the paragraph
  reworded and nothing else.
- **(E4) The prose.** What each test checks and why, kept; no client, citation, incident date or
  vanished name left, by reading and by §3.4's greps.
- **(E5) `PROVENANCE.md`.** 05c's section; the sixteen renames with their test ids; the citations
  table.
- **(E6) The suite.** 276, the same per module, writing nothing outside `tempfile` directories,
  starting no Ray.
- **(E7) The mutations.** (m1)–(m6) each fail a named test, and the orchestrator's own as §3 says.
- **(E8) The records.** The log, the board (one closed, one opened), the index (3),
  `prompts/INDEX.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff and the tests
  show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** The prompt's §3.1 command, from the repository root. Write the output to a file in
  the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Mutation diffs** are recorded so that `git apply` replays them from a clean tree at the agent's
  commit. Check each **as recorded in the log** with `git apply --check` and `-R --check`, and
  replay in `bash`, not zsh. None is committed. After each, `git status` must be clean. A mutation of
  a data file is a diff of that file like any other.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-05c/`), never
  `/tmp`. Python's `tempfile` in tests is fine. **No scratch `.py` goes under `runregistrykit/` or
  `docs/`**, even for a moment: discovery walks the one, `black` the other, and the guard's file
  set is derived from the filesystem. The writer and §3.3's script live in the scratchpad.
- **No client is read.** No SGK, ChamPBH, StochasticInstantons, DatastoreKit or RayPoolKit file is
  read, run or imported; the installed `datastorekit` is imported by the tests as before.
- **Install nothing.** The venv is as 01 left it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A word rule, package word or allowance is a stop, never a widened
  rule; a mutation no test catches is a stop, never a weakened mutation; a test that fails after a
  rename for a reason other than the known hits is a stop, never a changed assertion; a name beyond
  the map and correction 1 that needs renaming is a stop.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` at the root.
2. **The prompt's gate:** the diff from `8766714` empty; the suite 276.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 3 now, 3 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Sonnet**, in this checkout. Give it:
- the prompt, the campaign README, the board, 05a's and 05b's logs, `docs/OPEN_ISSUES.md`,
  `CLAUDE.md`, `README.md` and `PROVENANCE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/05c-the-tests-own-names.md`, in README §5.1's form,
  with the prompt's §4.3 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It reads, runs and edits no client repository, DatastoreKit or RayPoolKit.**
- **It installs nothing, reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list, the log and the records. `git diff
   4ec6406 <commit> --` over the package modules, `test_public_names.py`, `client_vocabulary.json`,
   the measuring script, `compare_with_source.py`, `pyproject.toml`, `README.md`, `CLAUDE.md`, the
   campaign README and the prompt is empty. `git ls-files runregistrykit` is the same 26.
2. **E2, the assertions, independently.** A script of the orchestrator's own, written from §2.2,
   correction 1 and §2.3 (not copied from the log): for each changed test module and fixture,
   `ast.dump` with docstrings removed at the commit, against `8766714`'s with the map applied to
   identifiers and the data replacements to string constants; equal for all but
   `test_package_imports.py`, whose difference is `FORBIDDEN` and its import. The guard's `ast`
   without docstrings equals `8766714`'s. The loader's test ids, old and new: 276 each, differing by
   exactly the nine renamed methods.
3. **E4, the prose, by reading.** `git diff 8766714 <commit>` of every test file read hunk by hunk:
   what each test checks and why, kept; a number dropped, its description kept; each incident's
   reason in general terms; no name the package no longer has; DatastoreKit's names, the carried
   fixture's `ShardedPool` attributes, the README by section name and `PROVENANCE.md` the only
   outside names. Then §3.4's two greps, re-run by the orchestrator's own script over the commit:
   the prose grep's every line in the log's accounting, its reason holding; the whole-file grep
   empty. And: no changed docstring or comment line over 100 columns; no paragraph broken
   mid-sentence.
4. **E3, the guard, by reading.** Its diff is the one paragraph, which keeps the mechanism, says the
   list is empty, and names no owner, prompt or citation.
5. **E3, the known hits, independently.** The guard's scans run over an export of the commit, by the
   orchestrator: every scan returns nothing. `known_hits.json`'s five lists empty; its `owners`
   string as §2.6.
6. **E6, the suite.** The prompt's §3.1 command: `Ran 276 tests … OK`, the per-module counts the
   same as correction 12's, the time recorded. `git status --short --ignored` the same before and
   after but for `__pycache__/`; no `var/`; this checkout the only worktree; no Ray process before
   or after. `./venv/bin/black --check runregistrykit docs` is clean.
7. **E5, `PROVENANCE.md`, by reading.** 05c's section names the renames, the neutral data,
   `FORBIDDEN`, the prose and the empty known hits; the renames table's sixteen rows each with its
   test ids, every id real at `8766714` (old) and at the commit (new); the citations table's rows
   one per changed module or fixture, each SGK record as the old text cited it at `8766714`.
8. **E7, the mutations.** Replay (m1)–(m6) from the log, one at a time, in `bash`; each fails the
   tests the log names; the suite OK after each; the tree clean. Then the orchestrator's own, not in
   the log:
   - (o1) `a3_shaped = hand_written_shaped` added after the helper in `store_fixtures.py`: the code
     name scan;
   - (o2) `KEY_TYPE` back to its old value in `shard_store_fixtures.py`, `REPLICATED` with it: the
     string scan;
   - (o3) "(store-fingerprint prompt 04)" restored to `test_store_fingerprint.py`'s first line: the
     citation scan (and the string scan for the campaign);
   - (o4) `FORBIDDEN` restored to its seven literal names: the string scan;
   - (o5) a citation (`prompt 05c`) added to the guard's paragraph: the citation scan and
     `test_this_module_holds_no_known_hit`;
   - (o6) `test_a_hand_written_shaped_sidecar_keeps_every_unknown_field` renamed back to its old
     name, and `INTEGRAL_CLASS` back to `QSI` in `test_store_retire.py`: **no** test fails, since
     `a3` and `QSI` are not forbidden words; recorded as what §3.4's grep pins and the guard does
     not.
   An uncaught (o1)–(o5) is opened on the board (owner to be put to the user), not a stop.
9. **E8, the records.**
   - The log has every section of README §5.1 and the prompt's §4.3 additions: the map as applied
     with every site count, corrections 1 and 2 included; the neutral data old and new; the per-scan
     totals before (155 in 94) and after (0); the writer, its one difference, its output and the
     file's diff; §3.3's script and output; §3.4's greps and their accounting; the suite before and
     after with the test ids mapped; every mutation as a diff, with the tests that fail it; the
     deviations classified (corrections 1–12 among them).
   - The board: the header; 05c's row (landed, "this commit", 276 → 276); T3 ✅; §3's
     `[02-the-ported-tests-name-sgk]` moved to §4 with this commit and what resolved it; the two
     other open issues with *Package lines (05c, …)*; `[05c-the-import-test-needs-datastorekit]`
     opened, owner 06; §3's opening count sentence. `docs/OPEN_ISSUES.md`: the row deleted, the new
     one added, **3** by counting, the date. `prompts/INDEX.md`'s row says 05c landed.
10. **The interface and the handover.** No record changes form: the diff touches no package module.
    The log's "State handed to the next prompt" gives 06 the empty known hits, the suite count, the
    new issue, the README's "Status" paragraph still 06's, and that nothing was installed, pushed or
    tagged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 05c* paragraph, in the form of
  05b's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md` and in
    `PROVENANCE.md`;
  - "reviewed" for 05c in the board's header and row, README §2's status column and its header,
    and `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 05c".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 276 → 276;
  - the renames, the three the map missed, and the neutral data;
  - `FORBIDDEN` and the issue it opens for 06;
  - the known hits now empty, and the guard's paragraph;
  - the prose, and `PROVENANCE.md`'s two tables;
  - the mutations, the agent's and the orchestrator's, and what is not pinned (a client name that is
    not a forbidden word is caught by grep, not by the guard; the prose's faithfulness is read);
  - the issue closed and the one opened;
  - that 06 can now be written, against the tree 05c left;
  - and whether to push `main`.
