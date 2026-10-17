# Orchestrator — prompt 03, an unreadable status is in use

Read [`../README.md`](../README.md) first: §0, §1, §5 (every rule; 4, 6, 7, 8, 9 and 10
especially) and §6.2 (L6 with its 2026-10-18 note, and L7–L9, which build on this prompt). The
conventions are those of [`prompt-02c.md`](prompt-02c.md), restated in §0 because the agent reads
§0 and not this directory. Where this note and the prompt differ, this note is right for 03.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names, at 3.12, 3.13 and 3.14;
- replay the log's mutation diffs with `git apply` in a scratch clone, and revert them;
- build venvs, client roots, stores and run directories of your own in the session scratchpad, and
  run the package and the planner's probes in them;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review. **Nothing is pushed** by the
agent, and nothing by the orchestrator without the user's clear yes (§4).

**The prompt:** [`03-an-unreadable-status-is-in-use.md`](../03-an-unreadable-status-is-in-use.md)
**Closes:** `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` · **Opens:** only
what the work finds · **Not touched:** `[03-a-run-whose-manifest-cannot-be-read-names-no-store]` ·
**Model:** Sonnet, as the prompt recommends.

**Gate:**
- The prompt's gate: 02c landed and reviewed (`35ce264`, `31933c4`, CI `39072902589` recorded in
  `0c75dd3`); **L6 taken 2026-10-18 as (a) refined** (`88f93c3`); `git diff --stat 35ce264 HEAD --
  runregistrykit pyproject.toml .github` empty; the suite 329 OK with one skip; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**A one-line rule, three readers made total, and a table of thirteen forms against six
operations.** The change to the rule is a filter; the risk is in what surrounds it. A reader that
still raises on a non-object file breaks every store under the runs root, an existing refusal's
words that drift break every test that asserts them, and a test that lets one form's outcome leak
into the next can pass a mutation it should catch. So the weight of the review is on:
- **the probe passes as a test**: every form, every operation refused, nothing under the temporary
  directory changed (§3 checks 5, 8);
- **nothing written changes**: no key of `status.json`, the manifest, `checkpoint.jsonl` or a
  sidecar, and `write_json_atomic` untouched (§3 check 4);
- **the writer moves by its base read alone**, and 02b's and 02c's sweeps pass over it (§3 check
  3);
- **every existing refusal's words are kept** for a `running` run, and every existing test is
  unchanged (§3 checks 1, 6);
- **no run is treated as finished** that does not say so (README §5 rule 9; §3 check 6).

**What moves on purpose:** `runregistrykit/__init__.py` (the helper beside `read_json`; `liveness`'s
first test and its docstring's step 1; `Run.status()`; the writer's base read `:375`, and nothing
else in the writer's section; `list_runs`, its two reads, the `status_readable` key and its
docstring); `runregistrykit/stores.py` (the module docstring `:102-107`; `_running_runs_naming`'s
filter and docstring, and its name if renamed; `_describe_running`; the remedy sentences of the five
refusals; `_refuse_if_in_use`'s docstring); `runregistrykit/__main__.py` (the module docstring, as
correction 8; `list`'s marker, and one stderr line); the two new test modules; the core line of
`.github/workflows/tests.yml` (`:89`); the new log `prompts/interrupted-runs/logs/03-an-unreadable-status-is-in-use.md`;
the board; the campaign README's §2 row for 03 only; `docs/OPEN_ISSUES.md`; `prompts/INDEX.md`.
**Nothing else**: not `pyproject.toml`, `client.py`, `fingerprint.py`, the repository `README.md`
(its usage is 06's), `PROVENANCE.md`, `CLAUDE.md`, `docs/`, any existing test module or fixture, the
prompt, any other part of the campaign README, or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **L6 is (a) refined**, as the prompt states it (README §6.2, the board's decisions table,
   `88f93c3`). Nothing in the prompt is conditional on it.
2. **The suite's time.** The gate run is given below. Run the suite in the foreground with a Bash
   timeout of at least 600 000 ms, output to a file in your scratch, and grep the verdict from the
   file. A slow run is not a stop; a failing one is.
3. **The core run of §3.2** is 02c's: `uv venv -p /opt/local/bin/python3.12 <scratch>/core`, then
   `uv pip install --offline -p <scratch>/core/bin/python -e <this checkout>`, `TMPDIR` in scratch,
   `datastorekit`, `ray` and `sqlalchemy` shown not findable, the **five** core modules by name
   (the workflow's four and `test_unreadable_status`): 87 at `35ce264`, 87 + N₁ after. This is the
   one install allowed; nothing goes into `venv/` or MacPorts' Pythons. Remove the venv afterwards.
   Also run `test_unreadable_status` at `/opt/local/bin/python3.13` (3.13.16, the version CPBH and
   SI run) with `PYTHONPATH` on the checkout and the standard library only; it imports no store
   layer, so it needs nothing else. Never give MacPorts' Pythons `-m pip`.
4. **One helper, two reads.** The helper lives beside `read_json` (`:237-244`), in the "files"
   section (`:220-258`), **outside** the writer's section (`:260` to the rule at `:386`). It serves
   the status and the manifest alike: an object is itself, anything else `{}`. It has no loop and
   no comprehension. In `list_runs`:
   - `status_readable` is `isinstance(raw, dict)` of what `read_json` returned for `status.json`,
     so `{}` is readable (it is then a status with no state, in use by §2.3's second wording);
   - `has_manifest` becomes `isinstance(raw, dict)` of the manifest's raw read, so a manifest `{}`
     still counts as a manifest, as it does today (`manifest is not None`), and `[1]`, `"x"`, `5`,
     `null` do not;
   - every manifest field, `_created_epoch`'s argument (`:1175`) included, is read from the
     helper's payload.
   `runs_naming` (`:957`) is not changed: its skip of an entry without a manifest (`:973`) now skips
   a non-object manifest too, and its own re-read (`:974`) is then never reached for one.
5. **The sweeps.** Because the helper is outside the writer's section, `the_writers_code()` does
   not include it, and 02b's and 02c's sweeps do not interrupt inside it; they do interrupt the
   writer at the new `CALL`. Give each sweep's instruction counts (per mode, as 02b's log gave
   them) at `35ce264` and after, measured by a scratch script on the test module's own helpers, not
   by editing it. A changed count is expected and is not a stop; a failing sweep is. Say in the log
   that the helper is outside the section, and why that is safe: an exception in its frame surfaces
   at the covered `CALL`.
6. **`liveness`.** A status that is not a `dict` is `unknown`, tested first; `[]` and `{}` stay
   `unknown` as now. Its values do not change.
7. **The store test module does not subclass `test_host_stores.TestARunOnAnotherHostIsInUse`.**
   A subclass inherits and re-runs its three tests (the planner's probe did so, being scratch). It
   subclasses `test_store_retire.RetireTestCase`, as the prompt says, and reuses `refusals` and
   `assertEachRefuses` by calling them as plain functions
   (`TestARunOnAnotherHostIsInUse.refusals(self, primary)`) or by a copy; `test_host_stores.py` is
   not edited. **Each form's outcome must not depend on an earlier form's**: either a fresh store
   and run per form, or a destination per form (the planner's probe used `C{i}`), so that an
   operation that wrongly proceeds for one form cannot make a later form refuse for another reason
   (an existing destination, a moved store). The fragments asserted include the run's id and the
   form's words, never only `RuntimeError`.
8. **`__main__.py`'s module docstring is `--help`'s description** (`:414`), and states the old rule
   four times: copy and move refuse "a store that any `running` run names, alive or stale" (`:24-25`),
   fingerprint (`:26-27`), retire (`:30`), amend (`:34`). Bring those four phrases into line with
   `stores.py`'s new module docstring, in the fewest words, and change nothing else in it. No test
   asserts them (`grep -n 'alive or stale' runregistrykit/tests/*.py` finds two test docstrings,
   which stay). Classify it IMPLEMENTATION CHOICE, "the orchestrator's correction 8".
9. **The words.** For a `running` entry every existing text is kept **byte for byte**, the remedy
   sentences included: `git diff -U0` of `stores.py` must show no existing f-string fragment for a
   running run changed. The new remedy sentence is added **once** per refusal, however many entries
   are not `running`, and not at all when every entry is `running`. Order in `_describe_running`:
   unreadable first, then readable-but-not-`running`, then today's two branches.
10. **`list`.** The new `!!` marker is for a row whose `liveness` is `unknown` and whose
    `has_manifest` is true; its stderr line counts only those rows, not stale ones, and comes after
    the stale line and before the foreign line, each of which is unchanged. `TestLister`'s and
    `test_host`'s `list` tests stay as they are and pass.
11. **The planner's probes** are given to you, in your scratch directory (§2): `probe.py` (the
    thirteen forms against `list_runs`, `list` and the six operations), `probe_finish.py` (the
    remedy), `probe_manifest.py` (the manifest). Each takes a checkout's path as its first argument
    and puts it first on `sys.path`; add a line that prints `runregistrykit.__file__`, so the log
    shows which tree ran. Run them with `venv/`'s Python against this checkout after the change and
    against `git archive 35ce264` extracted in your scratch. They are not committed, and nothing
    under `runregistrykit/` is changed to run them. `probe_manifest.py`'s torn and missing rows are
    `[03-a-run-whose-manifest-cannot-be-read-names-no-store]` and still proceed after the change:
    record that, do not fix it.
12. **Line citations.** Take every citation in the log and on the board from `grep -n` on the files
    as committed, after `black`, and re-check them just before committing. Add a "Package lines
    (03, this commit)" sentence to each §3 entry whose cited `__init__.py`, `stores.py` or
    `__main__.py` lines 03 moves, and change nothing else in those entries. The entry 03 closes
    moves to §4 with a *Resolved* paragraph: what changed and the tests that pin it.
13. **Mutation diffs** are taken after `black`, from the tree as it will be committed, and replayed
    as recorded (`git apply --check`, apply, the named tests, `-R --check`, reverse, the clone
    clean). (m4) is caught by the remedy test; say which forms fail.
14. **`black`.** 31 files at `35ce264`, 33 after: the two new test modules.
15. **The records.** The board has an Orchestrator notes line, and the campaign README's row for 03
    a status column. The agent does not edit the notes line, the README's header paragraph, or any
    row but 03's; it sets 03's status to "landed, not yet reviewed" in the board's §1 row, the
    README's §2 row and `prompts/INDEX.md`, as 02c did. The board's §3 count line goes from five to
    four; `docs/OPEN_ISSUES.md` from 10 to 9, counted by its rows; C1 ✅ "this commit".
16. **Observations, not fixes.** `Run.__init__`'s manifest read (`:667`) is not changed (the
    prompt's §6). If `Run(path)` on a non-object manifest raises where the manifest is used
    (`:707`, `:717`, `:870`, `:887-889`, `:931`), record it under "Observations not acted on" and
    open a §3 issue only if it is measured, with the board's and the index's counts adjusted.

**The facts, checked by the orchestrator on 2026-10-18 at `88f93c3`.** Pass them on.
- **In-repository state.** `main` at `88f93c3`, clean (`origin/main` at `31933c4`; `0c75dd3` and
  `88f93c3` unpushed). `git status --short --ignored` shows `prompts/.DS_Store`,
  `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
  `var/` and `venv/`. `var/ledger.jsonl` (`93589747…`) is an earlier review's, and is not touched.
  This checkout is the only worktree. `git diff --stat 35ce264 HEAD -- runregistrykit pyproject.toml
  .github` is empty.
- **The suite.** `Ran 329 tests in 124.542s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad. No
  Ray process; `RAY_ADDRESS` unset. `black --check runregistrykit docs`: 31 files.
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0. `/opt/local/bin/python3.12` (3.12.15),
  `python3.13` (3.13.16), `python3.14` (3.14.8); `uv` at `/opt/local/bin/uv`.
- **The lines the prompt cites** were read at `88f93c3` and are as it says. `__init__.py`:
  `TERMINAL_STATES` `:104`, `read_json` `:237-244`, the base read `:375`, `liveness` `:595-639`
  (`if not status:` `:619`), `Run.__init__`'s manifest read `:667`, `Run.status` `:722-723`,
  `finish` `:788` (its docstring's "signal" `:799`, the only one outside the tests),
  `_fingerprint_results` `:825` (`taken_by=self` `:840`), `_created_epoch` `:1122`, `list_runs`
  `:1129-1184` (manifest `:1158`, status `:1159`). `stores.py`: the module docstring `:102-107`;
  `runs_naming` `:957` (skip `:973`); `_running_runs_naming` `:998`, filter `:1017`;
  `_describe_running` `:1021`; `_refuse_if_in_use` `:1041` (remedy `:1050-1052`), called at
  `:1114`; fingerprint `:1350-1357`; retire `:1676-1682`; amend `:2029-2033`. `__main__.py`: the
  docstring `:16-37`, `store show`'s runs `:188-201`, `list` from `:545`, the marker `:558`, the
  stale line `:578-585`, the foreign line `:586-596`. Tests: `test_host_stores.py`
  (`refusals` `:61`, `assertEachRefuses` `:82`); `RetireTestCase` `test_store_retire.py:91`,
  `a_full_store` `:102-121`; `a_running_run` and `a_stale_run` `store_fixtures.py:145-153`,
  `state()` (`tree_state`) after them; `TestLister` `test_run_registry.py:682`; `test_host.py`'s
  `list` tests from `:631`; the workflow's core line `.github/workflows/tests.yml:89`.
- **The issue index** counts 10. After 03: 9.

**What the review exists to establish.**
- **(K1) The files.** Only §0's list; no existing test module changed; the workflow by one line.
- **(K2) Nothing written changes.** The four records' keys and forms the same before and after;
  `write_json_atomic` untouched.
- **(K3) The probe.** Every form, every operation refused, the store untouched; `list_runs` and
  `Run.finish` raise on none; `list` marks each.
- **(K4) The words and the rule.** Existing texts byte-identical; the new ones say the registry
  cannot tell; nothing treats an unreadable run as finished.
- **(K5) Nothing else moved.** Existing tests; the writer by its base read; 02b's and 02c's sweeps.
- **(K6) The tests bite.** (m1)–(m6), and the orchestrator's.
- **(K7) The records**, with the issue closed and the manifest issue left open.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `var/`, `*.egg-info/`, `__pycache__/` and `.DS_Store`
  are ignored and must not be staged. Count, then paste. A log states only what the diff, the
  commands and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 2.
- **Mutation diffs.** As correction 13. None is committed. After each, `git status` here must be
  clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-03/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. **No scratch file goes under
  `runregistrykit/` or `docs/`.** The probes live there and are not committed.
- **Signals.** The new tests signal nothing. A probe signals nothing. Nothing signals this shell,
  the agent's own process or any other.
- **Ray.** The agent starts no Ray, and records `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` before and after every suite run.
- **GitHub.** Nothing is pushed, no tag is made, no workflow is dispatched.
- **Stop conditions are real** (the prompt's §5). A stop goes to the user through the orchestrator:
  do not commit; end with a STOP report. A defect found elsewhere in the package is opened on the
  board, never fixed.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone.
2. **The prompt's gate**, and the suite: 329, one skip, in `venv/`, its time recorded.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 10 now, 9 after. Tell the agent.
5. **The probes.** Copy the planner's three probes (the 03 planning session's `plan03/` scratch)
   into the agent's `agent-03/probes/`, and keep a copy of your own.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Sonnet**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and
  `CLAUDE.md`;
- `HEAD`, the suite count and time, and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad,
  and the probes' directory. The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and plainly: one commit at the
end; the files of §0 only; the core venv of correction 3 the only install; `TMPDIR` for every
command; no Ray; signal nothing; push nothing, tag nothing; stop and ask on the prompt's §5.

## 3. The review — nine checks

1. **Scope (K1).** `git show --stat <commit>` touches only §0's list. `git diff <note's commit>
   <commit> -- pyproject.toml runregistrykit/client.py runregistrykit/fingerprint.py README.md
   PROVENANCE.md CLAUDE.md docs prompts/interrupted-runs/03-an-unreadable-status-is-in-use.md
   prompts/interrupted-runs/orchestrator` is empty; `git diff --stat <note's commit> <commit> --
   runregistrykit/tests` shows the two new files only; the workflow's diff is its core line; the
   campaign README's diff is 03's row only. `__main__.py`'s docstring diff is correction 8's four
   phrases.
2. **The suite (K5).** In `venv/` at the commit: `Ran 329 + N tests … OK (skipped=1)`, per module
   by the loader. `black --check runregistrykit docs`: 33 files. The core run of correction 3 in the
   orchestrator's own scratch venv, five modules, 87 + N₁; `test_unreadable_status` at 3.13.16 and
   3.14.8 by `PYTHONPATH`. `git status --short --ignored` and `var/ledger.jsonl` the same before and
   after; no Ray; no child left.
3. **The writer (K5).** `git diff -U0 <note's commit> <commit> -- runregistrykit/__init__.py`
   within the writer's section (`:260` to its closing rule) is the base read line alone.
   `test_status_writes` and `test_host` at 3.13.16 and 3.14.8 by `PYTHONPATH`: as at `35ce264`
   (50, one skip). 02c's review's `bombard.py`, 45 s at 3.13.16 against the commit, one row: 0 lock
   held, 0 in-flight kept.
4. **Nothing written changes (K2).** A scratch lifecycle at `35ce264` (by `git archive`) and at the
   commit, each in its own client root: `begin` on a registered store, `heartbeat`, `record`,
   `finish("done", fingerprint=True)`; the key sets of `status.json` (with `host`), the manifest,
   one `checkpoint.jsonl` line and the sidecar compared: identical. `git diff <note's commit>
   <commit>` shows `write_json_atomic` and `_land_status` untouched.
5. **The probe (K3).** The planner's three probes from the orchestrator's own copy, against the
   commit and against `35ce264`, each printing the `runregistrykit.__file__` it ran. After: every
   form `refused` by all six operations, `list_runs` raising on none, `list` marking each row `!!`;
   `probe_finish.py` ending every form `killed`; `probe_manifest.py`'s `[1]` no longer raising, its
   torn and missing rows still proceeding (the open manifest issue, untouched). Before: §"At
   writing"'s table.
6. **The words and the rule (K4).** Every f-string in `stores.py` that today describes or remedies a
   `running` run unchanged (`git diff -U0`, read hunk by hunk). The new texts in the code match the
   log's quotation. A refusal for running runs only carries no new sentence; a refusal with two
   unreadable runs carries it once (a scratch check). `TERMINAL_STATES` imported, not respelled
   (`grep -n '"done", "failed"'` in `stores.py` empty). `git grep -n 'signal' -- 'runregistrykit/*.py'
   ':!runregistrykit/tests'`: `finish`'s docstring only.
7. **The log (K7).** Every section of README §5.1 and the prompt's §4.4 additions; the deviations
   classified, corrections 1–16 among them; the suite before (329) and after; the core and 3.13
   runs; both probe tables; the sweeps' counts; every mutation as a diff; the refusal texts as
   shipped; line citations right at the commit by `grep -n`.
8. **The mutations (K6).** (m1)–(m6) extracted from the log by a script and replayed in a `git
   clone` of the commit, the two new modules and the module each names, in `venv/`'s Python with
   `PYTHONPATH` on the clone. Each fails as the log says. Then the orchestrator's own:
   - (o1) `_describe_running`'s unreadable branch removed, so an unreadable entry gets the running
     words: a test must fail by the form's words;
   - (o2) the new remedy sentence added to every refusal, `running` runs only included: record
     whether any test catches it (the prompt asks for the sentence "when any entry is not
     `running`"; no test may assert its absence);
   - (o3) `liveness`'s non-dict guard removed, `list_runs` keeping the helper: the
     `liveness([1], …)` test must fail;
   - (o4) `list`'s new `!!` given to every `unknown` row, manifest or not: the no-manifest row's
     test must fail;
   - (o5) `has_manifest` back to `manifest is not None`, the fields still read through the helper:
     the manifest-`[1]` test must fail.
9. **The records (K7).** The board: the header, 03's row ("this commit", 329 → 329 + N), C1, the
   issue moved from §3 to §4 with its *Resolved* paragraph, the §3 count line (four), the
   "Package lines (03, …)" sentences, `[03-a-run-whose-manifest-cannot-be-read-names-no-store]`
   still in §3. The campaign README's 03 row. `docs/OPEN_ISSUES.md`: 9 by counting, the row deleted,
   the date. `prompts/INDEX.md`: the campaign's line. **CI is read after the push (§4)**: all three
   jobs green, the core job's count 87 + N₁ with `test_unreadable_status` on its line. Until then
   the verdict says "pending CI".

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 03* paragraph (*At dispatch*,
  *The checks*, verdict), and add this note to the board's **Orchestrator notes** line, marked
  "used for 03". Fix small residue in a follow-up commit of its own: "this commit" → the SHA on the
  board, in the log, in the README's §2 row and in `prompts/INDEX.md`; "reviewed" for 03 in the
  board's header and row, the README's header paragraph and §2 status column, and
  `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Ask the user whether to push `main`.** The new core module first runs on Linux in CI. Once it
  has, read the result (check 9) and record it on the board in a records commit of its own.
- **Report to the user:** what landed, 329 → 329 + N, and the issue closed; the probe's table,
  before and after; the mutations; CI, or that it is pending a push; that 04 is next, needs L7 and
  L8, and is written only after this review.
