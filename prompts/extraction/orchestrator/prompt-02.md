# Orchestrator — prompt 02, port the core and shard-fixture tests

Read [`../README.md`](../README.md) first: §0.2 (the tests), §4, §5 (every rule; 6, 8, 9 and 10
especially) and §6.2 (U4). The conventions are [`prompt-01.md`](prompt-01.md)'s; they are restated
in §0 because the agent reads §0 and not this directory. Where this note and 01's differ, this one
is right for 02.

**You do not write code.** You may:
- run the suite, the equivalence check, `black --check` and the tests the log names;
- replay the log's deliberate-breakage and mutation diffs with `git apply`, and revert them;
- export SGK's files and this repository's tree into the session scratchpad, and run probes and
  breakages there, never committing one;
- read SGK only through `git -C /Users/ds283/Documents/Code/SecondaryGWKit
  show|ls-tree|rev-parse|log|status|diff`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-port-the-core-and-shard-fixture-tests.md`](../02-port-the-core-and-shard-fixture-tests.md)
**Closes:** nothing · **Narrows:** four issues' package lines · **Opens:**
`[02-the-ported-tests-name-sgk]`, and only what else the work finds · **Model:** Sonnet, as the
prompt recommends.

**Gate:**
- The prompt's gate: 01 landed (`4e0d715`) and reviewed (`bae5597`); `git diff --stat 4e0d715 HEAD
  -- runregistrykit docs pyproject.toml PROVENANCE.md` empty; SGK's `a45aefc` has the eight blobs;
  U4 taken; the check exits 0 and the suite is 3; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that it
  could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It pins the import's behaviour, and it changes the check's rule.** Every prompt from 03 changes
the package against the 108 tests 02 lands, so the review has two halves:
- **the tests are SGK's tests**, changed only by D-name, D-fix and D-fmt, every assertion intact;
- **the extended check still bites**, on 02's files and on 01's. 02 replaces 01's per-pair rule
  with "the package equals `black` of the renamed source". That is a stronger statement for 01's
  files, but a check rewritten in place can lose a property silently, so 01's (a)–(i) are replayed
  against it (the prompt's (h)).

**What moves on purpose:** eight new files under `runregistrykit/tests/`; the check extended (the
eight rows' fate, the new rule, `black` pinned, the docstring); `PROVENANCE.md`; `CLAUDE.md`'s Tests
bullet; the log and the records. Nothing in the package's three modules, `tests/__init__.py`,
`test_package_imports.py` or `pyproject.toml`.

**Two recommendations for the check**, consistent with the prompt's §2.4:
- **Count D-fmt from T to `black(T)`, not from T to the package.** When the check passes the two
  are the same; when a breakage makes the package differ, counting from `black(T)` keeps the D-fmt
  count (12, in 3 hunks) a property of the source, and every difference between `black(T)` and the
  package is reported once, as UNCLASSIFIED, with package line numbers. The D-name and D-fix counts
  are likewise properties of the source (T is computed from it alone), so unlike 01 a breakage does
  not move them; the failure lines say what is wrong.
- **`black` is imported under the cannot-run guard.** An `ImportError`, a version other than
  `25.1.0`, or `black` raising on T (T comes from the source, so it always parses at `a45aefc`)
  exits 2 with `CANNOT RUN: …`, as a `git` failure does now. Exit 1 stays "ran, and something is
  wrong".

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **(m2) fails more than the prompt names.** Measured: `Ran 108 … FAILED (failures=4,
   errors=8)`, as the prompt says, but the failing tests are in `test_store_copy_move` (`TestCopy`
   ×2, `TestRefusals.test_a_finished_run_does_not_refuse`, `TestInterruption.test_C5_complete` ×3
   subtests, `TestInterruption.test_C4_…` ×3 subtests), `test_store_amend.TestCopyAndMove`
   (`test_copy_carries_an_amended_field_and_its_entry`), **and also**
   `test_store_sidecar.TestUnknownFieldsSurvive.test_an_a3_shaped_sidecar_through_adopt_copy_and_move`
   and `test_store_command_line.TestStoreCommands.test_show_create_adopt_copy_and_move`. Record
   every failing test as seen, not only the modules the prompt predicts.
2. **`black` from the command line is not `black.Mode()`.** Run from the repository root,
   `black` finds `pyproject.toml` and infers `target_version: ['py312', 'py313']` from
   `requires-python` (shown by `black -v`); `black.format_str(T, mode=black.Mode())` infers target
   versions per file from its content. **On all twelve checked files the two give the same output**
   (measured, both ways, at writing). The check uses `black.Mode()`, as the prompt says; its
   docstring says the two could differ in principle and that §3.5's `black --check` would then show
   it. Do **not** add a `[tool.black]` table: `pyproject.toml` is not in the prompt's §6 list.
3. **The instances overlap in `test_store_copy_move.py`.** `black`'s three reflows (source `:73,
   :135, :211`) are reflowed *because* D-name lengthened them, so those 3 source lines are 3 of
   that file's 10 D-name lines as well as the 3 D-fmt instances. README §5 rule 9's accounting lists
   each instance under each class it belongs to, and says so. No line needs both D-name and D-fix
   (measured).
4. **Replaying 01's (a)–(i) (the prompt's (h)).** Take the diffs from 01's log
   (`logs/01-import-the-registry.md`, "The diffs") as they are. Eight edit 01's files, which 02
   leaves unchanged, so they apply. 01's (h) edits the check's `test_killed_handler.py` row; its
   context is that not-imported row, which 02 does not change, so it applies with a line offset as
   long as the agent does not reformat the table's unchanged rows. If it does not apply, re-record
   an equivalent diff and say so. Under the new rule the *output* differs from 01's log (for
   example (c) is one difference between `black(T)` and the package, and D-name stays 13): record
   what the extended check prints, not 01's text.
5. **The suite takes about 14 s here**, not the prompt's 25–40 s (measured: `Ran 108 tests in
   13.8s`). Record the time seen.
6. **The pending rows stay a mechanism.** The three 04 rows remain *pending, 04*, and a pending
   file that is present still fails as PRESENT, NOT CHECKED: the prompt's breakage (g) depends on
   it.

**The facts, checked by the orchestrator on 2026-10-14 at `0fb6aff`** (by `git`, and by a port of
the eight files into a `git archive` export of `0fb6aff` in the orchestrator's scratchpad, made a
git work tree there; no SGK code was run). Pass them on.
- **The source.** SGK's `HEAD` is `14bcac0`, clean; `git diff --stat a45aefc HEAD -- RunRegistry
  StoreFixtures` is empty; `ls-tree -r a45aefc -- RunRegistry/` has 25 rows. The eight files are
  §2.2's, blob and length: `test_run_registry.py` `01c3ea3…` 711, `store_fixtures.py` `391f31f…`
  223, `test_store_sidecar.py` `533d111…` 617, `test_store_copy_move.py` `4be78d9…` 601,
  `test_store_command_line.py` `6f111e2…` 183, `test_store_amend.py` `8b7db11…` 641,
  `test_store_amend_residuals.py` `0c6e6a2…` 267, `shard_store_fixtures.py` `1375949…` 168.
- **D-name** `\bRunRegistry\b` → `runregistrykit`: 31, 6, 15, 10, 11, 8, 2, 0 lines (83). No
  `RunRegistry` is a prefix of a longer word in the eight files.
- **D-fix**: `StoreFixtures` occurs on exactly 5 lines, all D-fix: `store_fixtures.py:4` (the path
  form) and `:20`, `test_store_sidecar.py:28`, `test_store_copy_move.py:32`, `test_store_amend.py:15`
  (the dotted form). So the completeness rule on `\bStoreFixtures\b` can pass.
- **D-fmt.** `black.format_str(T, mode=black.Mode())` changes only `test_store_copy_move.py`: three
  `replace` hunks, T `:73` → package `:73-76`, `:135` → `:138-142`, `:211` → `:218-220`; 601 → 610
  lines; package `:75` is `"datastore": runregistrykit._repo_path(src),` (the comma (b) removes).
  For the other eleven files, 01's four included, `black(T) == T` and the committed package equals
  it.
- **The prototype of the extended rule** over all twelve rows: D-name 6, 13, 4, 0, 31, 6, 15, 10,
  11, 8, 2, 0 (106); D-fix 0, 0, 0, 0, 0, 2, 1, 1, 0, 1, 0, 0 (5); D-fmt 12, all in
  `test_store_copy_move.py`; the package equal to `black(T)` for every row.
- **`black --check runregistrykit docs`** over the export with the eight files ported: 14 files
  unchanged.
- **The suite**, from the export's root as a git work tree, `runregistrykit` resolving to the
  export's own package: **`Ran 108 tests in 13.8s`, OK**. By loader: `test_package_imports` 3,
  `test_run_registry` 29, `test_store_sidecar` 17, `test_store_copy_move` 27,
  `test_store_command_line` 2, `test_store_amend` 21, `test_store_amend_residuals` 9. After it,
  `git status --short --ignored` showed nothing but `__pycache__/`, no `var/`, no Ray process.
- **Without `.git`** (the same export, `.git` moved aside): `FAILED (failures=2)`,
  `TestManifest.test_manifest_carries_the_provenance_triple` and
  `test_store_sidecar.TestCreate.test_the_fields_and_one_create_entry`, the two 40-character
  `git_head` assertions (package `test_run_registry.py:273`, `test_store_sidecar.py:288`).
- **The breakages and mutations, measured against the suite:** (a) `stale_after=3601.0` at package
  `test_run_registry.py:639`: 108 OK. (e) `KEY_TYPE = "wavenumbers"`: 108 OK. (m1)
  `RECORDED_DISTRIBUTIONS = ("datastorekit",)`: failures=2, errors=1, all in
  `TestPackageProvenance` (`test_the_recorded_names_are_the_two_packages`,
  `test_a_distribution_not_installed_is_none`, error in
  `test_a_vcs_install_records_its_commit_and_tag`). (m2): correction 1. `DEFAULT_STALE_AFTER =
  901.0`: 108 OK.
- **Package lines the prompt cites**, read in the ported export: `test_run_registry.py:393-396` the
  pinning test; `:179, 226` write the checker and crasher scripts with `repo=REPO_ROOT`; `:684`
  `cwd=REPO_ROOT`; `test_store_command_line.py:60-61, 172-173` and `test_store_amend.py:636-637`
  `cwd=REPO_ROOT` and `PYTHONPATH`; `shard_store_fixtures.py:25-27` `KEY_TYPE`, `REPLICATED`,
  `SHARDED`; `bare_pool` sets the ten private attributes the prompt lists and the fixture calls
  `_create_engine`, `_read_shard_data`, `_write_shard_data`; `store_fixtures.py:158-165`
  `assertOpens`, with `_check_shard_files` and `_shard_db_files`. No ported file names
  `_SHARDS_TABLE_UNREADABLE` or its text; the package uses it at `stores.py:1818, 1863`.
- **In-repository state.** `0fb6aff` on `main` before this note, clean; `git status --short
  --ignored` shows `runregistrykit.egg-info/`, `runregistrykit/__pycache__/` and `venv/`; the only
  worktree is this checkout; no `var/`. The check exits 0 and the suite is `Ran 3 tests … OK`.
  `venv/`: Python 3.12.15, `black` 25.1.0, `runregistrykit` editable (`pip freeze` prints it as
  `-e git+…@<HEAD>`, the commit at the time of asking).
- **Expected counts.** The suite: **3** before, **108** after. The check: 25 rows and the fixture
  blob equal; 12 checked (4 by 01, 8 by 02); D-name 106; D-fix 5; D-fmt 12 in 3 hunks; 3 pending
  (04); 11 not imported and absent; 1 declared new file. The index: **7** now, **8** after.
- **Ray.** No Ray process at writing; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** The eight files exist under their names, and nothing else new is in
  `runregistrykit/`; the three modules, `tests/__init__.py`, `test_package_imports.py` and
  `pyproject.toml` are unchanged.
- **(E2) Equivalence.** The check exits 0 with the expected counts, and by reading its rule is the
  prompt's: T by substitution, the package equal to `black(T)`, completeness on both names, `black`
  pinned; no line numbers.
- **(E3) The check bites**, on 02's (a)–(g) and on 01's (a)–(i).
- **(E4) The tests.** 108 pass; every ported test keeps its name and assertion (by the check); the
  suite writes nothing outside its temporary directories and starts no Ray.
- **(E5) The tests catch behaviour.** (m1)–(m3) fail the suite as recorded.
- **(E6) The records.** The log, the board (one issue opened, four narrowed), the index (8),
  `prompts/INDEX.md`, `PROVENANCE.md` and `CLAUDE.md`'s Tests bullet.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/` and `__pycache__/` are gitignored and
  must not be staged. Count, then paste. A log states only what the diff, the check and the tests
  show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** The prompt's §3.1 command, from the repository root. Write the output to a file in
  the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Breakage and mutation diffs** are recorded so that `git apply` replays them from a clean tree at
  the agent's commit. Check each **as recorded in the log** with `git apply --check` and `-R
  --check`, and replay in `bash`, not zsh. None is committed. After each, `git status` must be
  clean.
- **SGK is read only through `git -C … show|ls-tree|rev-parse a45aefc…`**. Never from SGK's working
  tree, never by importing it, never by running its code or tests (README §5 rule 5).
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`.
  Python's `tempfile` in tests is fine. **No scratch `.py` goes under `runregistrykit/` or
  `docs/`**, even for a moment: the check walks the one and `black` the other.
- **Install nothing.** The venv is as 01 left it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A difference that fits no class is a stop, never a widened rule; a
  test that fails is a stop, never an edit.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` at the root.
2. **The prompt's gate.** The `git diff --stat 4e0d715 HEAD -- …` above is empty; the check exits 0;
   the suite is 3.
3. **SGK.** Record its `HEAD` and status, and the eight blobs at `a45aefc`.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
5. **The index.** 7 now, 8 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Sonnet**, in this checkout. Give it:
- the prompt, the campaign README, the board, 01's log, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md` and the check;
- `HEAD`, SGK's `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and its two recommendations (D-fmt counted
from T to `black(T)`; `black` under the cannot-run guard).

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-port-the-core-and-shard-fixture-tests.md`, in
  README §5.1's form, with the prompt's §4.3 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** In particular it
  must not touch the package's three modules, `tests/__init__.py`, `test_package_imports.py`,
  `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `.idea/`, the campaign README, the
  prompt, anything under `orchestrator/`, or any part of `CLAUDE.md` but the Tests bullet.
- **It edits no client repository, DatastoreKit or RayPoolKit, and runs none of their code.**
- **It installs nothing, reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list: the eight files, the
   check, `PROVENANCE.md`, `CLAUDE.md`, the log, the board, `prompts/INDEX.md`,
   `docs/OPEN_ISSUES.md`. `git diff 4e0d715 <commit> -- runregistrykit/__init__.py
   runregistrykit/stores.py runregistrykit/__main__.py runregistrykit/tests/__init__.py
   runregistrykit/tests/test_package_imports.py pyproject.toml` is empty. `git diff <commit>~1
   <commit> -- CLAUDE.md` touches the Tests bullet only. No `venv/`, `*.egg-info`, scratch file or
   `var/`.
2. **E1, the files.** `git ls-files runregistrykit` is 01's five and the eight, no more.
   Independently, re-port the eight from `a45aefc` in the scratchpad (perl for D-name and D-fix,
   `black.format_str(…, mode=black.Mode())`) and `cmp` each against the committed file.
3. **E2, by running.** In a fresh shell the check exits 0, its counts §0's, its whole output equal
   to the log's.
4. **E2, by reading.** Read the check in full. The constants and table at its top; SGK read only
   through `git -C`; nothing of SGK or the package imported; `black` imported under the guard and
   pinned to `25.1.0`; T by substitution of the two regular expressions on every line; the package
   compared with `black(T)` as whole text; the D-fmt count from T to `black(T)`; completeness on
   `\bRunRegistry\b` and `\bStoreFixtures\b` over every checked file; no line number in any rule;
   the pending mechanism kept; the frozen-tree check and the walk as 01 made them. The docstring
   states the rule, D-fix, D-fmt and why `black` is pinned.
5. **E3, the check bites.** Replay 02's (a)–(g) and 01's (a)–(i) from the log, one at a time, in
   `bash`. Each must exit 1 and name the file and line, row or file. Then the orchestrator's own,
   not in the log:
   - `test_store_copy_move.py` package `:73-76` collapsed back to T's single line (the renamed
     source line, unformatted): the package then equals T but not `black(T)`, and must fail;
   - two adjacent import lines of a ported test swapped, a change no line's class can excuse;
   - `black` reported as another version (a one-line edit of the pin in the check): exit 2.
   Revert each, and check `git status` is clean.
6. **E4, the tests.** The prompt's §3.1 command gives `Ran 108 tests … OK`; the per-module counts by
   loader are §0's. `git status --short --ignored` is unchanged across a run but for
   `__pycache__/`; no `var/`; no Ray process before or after.
7. **E5, the mutations.** Replay (m1)–(m3) from the log; each fails as recorded (correction 1 for
   (m2)); (m3) is in `stores.py`'s sidecar reader or `amend_sidecar`, as the prompt says. The suite
   is 108 OK after each.
8. **The issues.** `[02-the-ported-tests-name-sgk]` opened on the board with impact and next step,
   owner 05, its lines re-measured in the log; the four narrowed issues' package lines true at the
   commit (spot-check each in the package); `[00-a-refusal-matches-datastorekit-message-text]`'s next
   step now 04's.
9. **E6, the records.**
   - The log has every section of README §5.1; the check's whole output; the per-class test
     counts; the 83 D-name, 5 D-fix and 3 D-fmt instances accounted for (correction 3); 3 → 108;
     every breakage and mutation as a diff, with the check's and the suite's verdicts.
   - `PROVENANCE.md`: the eight rows "ported by 02"; D-fix and D-fmt beside D-name with the three
     reflows; the check's rule; `black` 25.1.0 needed. Nothing else changed.
   - `CLAUDE.md`'s Tests bullet: the command, `datastorekit` and `ray` installed but never
     initialised, the git work tree.
   - The board: the header; 02's row (landed, "this commit", 3 → 108); T1 ✅; G1's package side for
     02's files; §3 as above. `prompts/INDEX.md`'s row says 02 landed. The index counts 8 by
     counting, matching its header and date.
   - `./venv/bin/black --check runregistrykit docs` is clean.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - "reviewed" for 02 in the board's header and row, README §2's status column and its header, and
    `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 02".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 3 → 108;
  - the check's new rule, its counts per class, and the breakages (02's, 01's and the
    orchestrator's) failing it;
  - the mutations and what they show; what the suite does not pin (`DEFAULT_STALE_AFTER`, the
    fixture's `KEY_TYPE`);
  - the issue opened and the four narrowed;
  - that 03 can now be written, against the tree 02 left, with U5 and U9 to put to the user, and
    that the check is retired at 03's start;
  - and whether to push `main`.
