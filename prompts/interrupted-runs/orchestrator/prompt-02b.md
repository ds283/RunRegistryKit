# Orchestrator — prompt 02b, the writer's bookkeeping

Read [`../README.md`](../README.md) first: §0, §1 (no signal handling in the package), §5 (every
rule; 6, 7, 8 and 10 especially) and §6.2 (L5, with its 2026-10-17 amendment). The conventions are
those of [`prompt-02.md`](prompt-02.md), restated in §0 because the agent reads §0 and not this
directory. Where this note and the prompt differ, this note is right for 02b.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names;
- replay the log's mutation diffs with `git apply` in a scratch clone, and revert them;
- build venvs, client roots and run directories of your own in the session scratchpad, and run the
  package in them, child processes that signal themselves included;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review. **Nothing is pushed** by the
agent, and nothing by the orchestrator without the user's clear yes (§4).

**The prompt:** [`02b-the-writers-bookkeeping.md`](../02b-the-writers-bookkeeping.md)
**Closes:** `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]` and
`[02-the-landed-record-is-unpinned-and-can-move-backwards]` · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: 02 landed and reviewed (`2bf9c72`, `a38022f`, CI `91e8e9c`), the user's
  request recorded (L5's amendment), `git diff --stat 2bf9c72 HEAD -- runregistrykit pyproject.toml
  .github` empty, the suite 322 OK with one skip, the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**The diff is a dozen lines and the test is every instruction.** 02 pinned the writer at four
points; 02b's sweep interrupts it at each of the ~200–250 instructions it executes, eight ways. So
the weight of the review is on five things:
- **the plain write is still 02's plain write**: one read, one write, one `os.replace`, the same
  keys and mode (§3 check 3);
- **the two amendments do what L5's amendment says, and nothing else moves**: the merge applies
  only in-flight writes above the landed base's number; the landed record is never lowered (§3
  checks 4, 5);
- **the sweep tests what it claims**: it reaches every instruction of every writer code object,
  ignores the handler's own write, frees its tool id, and fails against `2bf9c72` (§3 checks 5, 6);
- **02's real-signal behaviour is unchanged** (§3 check 6);
- **the tests bite**: (m1)–(m5), the orchestrator's own besides (§3 check 8).

**What moves on purpose:** `runregistrykit/__init__.py` (the writer section `:259-349` and
`Run._update`'s docstring only); `runregistrykit/tests/test_status_writes.py` (additions only); the
new log `prompts/interrupted-runs/logs/02b-the-writers-bookkeeping.md`; the board;
`docs/OPEN_ISSUES.md`; `prompts/INDEX.md`. **Nothing else**: not `stores.py`, `__main__.py`,
`client.py`, `pyproject.toml`, `.github/` (the core job already names `test_status_writes`),
`README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption/`, any other test module or fixture, the
prompt, the campaign README or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The suite's time.** 02's review saw 111 s, and the gate run here is given below. The sweeps add
   to it. Run the suite in the foreground with a timeout of at least 600 s, write its output to a
   file, and grep the verdict from the file. Record the time seen, and the module's time alone. A
   slow run is not a stop; a failing one is.
2. **The core run of §3.2** is 02's: `uv venv -p /opt/local/bin/python3.12 <scratch>/core`, then
   `uv pip install --offline -p <scratch>/core/bin/python -e <this checkout>`, with `TMPDIR` in the
   scratchpad, and `datastorekit`, `ray` and `sqlalchemy` shown not findable. At `2bf9c72` it ran 80
   tests with one skip; after 02b it is 80 + N, every new test being core. This is the one install
   allowed, and nothing is installed into `venv/`. The venv is removed afterwards.
3. **"Every function the writer section defines" includes nested code objects.** `_write_status`'s
   `sorted(n for n in book["in_flight"] if n < number)` is a generator expression, which at 3.12
   is a code object of its own, in `_write_status.__code__.co_consts`, and a Python-level iteration
   of the live `in_flight` dict. The sweep sets local events on every code object reachable through
   `co_consts` from the writer's functions (the new helper included), recursively, and the log says
   which code objects those are and how many of the counted instructions fall in each. If the new
   writer has no nested code object, the log says so. The "At writing" counts (202, 254) may then
   differ; the property, not the count, is what is pinned. **An instruction inside the generator at
   which a state is lost, or a `RuntimeError` raised, is a §5 stop**, not something to engineer
   around in the test.
4. **The sweep's handler runs from the `INSTRUCTION` callback, and in the raising modes raises
   from it.** At 3.12.15 an exception raised by a `sys.monitoring` callback propagates from the
   instruction, which is what the planner's raising counts measured. Two rules follow: the callback
   never returns `sys.monitoring.DISABLE` (it would silence that instruction for every later
   attempt), and the `finally` that clears the local events and frees the tool id runs however an
   attempt ends. The sweep first runs on 3.13.16 in CI's `suite (high)`; the log says it is not
   measured there.
5. **What the sweep does not reach**, stated in the log and not engineered around: instructions
   inside the library functions the writer calls (`json.dump`, `copy.deepcopy`, `read_json`,
   `now_iso`, `os.fsync`), which are not the writer's code objects. A handler inside one of them
   sees the bookkeeping as at the `CALL` instruction before it returns, which the sweep does reach.
   And a real signal's handler runs only at the interpreter's eval-breaker checks, a subset of the
   instruction boundaries, so the sweep is the stronger test.
6. **A fresh run per attempt** may be made by the cheapest means that gives a run directory at a
   new real path with `begin`'s `status.json` and manifest in it (for example `begin` once per
   sweep, and copy its directory to a new name per attempt). A new real path is a new book in
   `_STATUS_WRITES`. **The bookkeeping is never cleared or edited by a test**; it is read only, and
   only in the `finish` sweep's handler (the prompt's §2.5). The log says which means was used and
   gives each sweep's time and instruction count. If the module's time passes 60 s here, say so;
   it is not a stop.
7. **The two measured cases and the (o2) sequence** use 02's `Interruption`-style patching of
   `json.dump` (fire once, the inner writes through the real function), and assert the whole
   ending: state, `exit_code`, `units_done`, `stage` where the prompt names it, no leftover.
8. **The new helper and the shape.** The prompt's §2.3 shape (a dict per path, number → payload,
   one store, a snapshot prune, a helper that re-reads if its key was pruned) is a description of
   the candidate that measured clean. If the agent chooses it, the log says so; if another, the log
   states the shape and why it has the property. Either way the docstring of `Run._update` and the
   section's comments state the amended merge and the record **in words that say "handler" and
   "interrupt", not "signal"**: §3.3's `git grep -n 'signal' -- 'runregistrykit/*.py'
   ':!runregistrykit/tests'` must still find `finish`'s docstring only (`:755` at `2bf9c72`).
9. **`_update`'s line of 121 characters** (`__init__.py:696`) is rewrapped to 100 columns as the
   prompt says. The four other lines over 100 in the file (`:620`, `:819`, `:863`, `:872` at
   `2bf9c72`, 101–103 characters, in code `black` leaves alone or in other docstrings) are not 02b's,
   and are left; the log lists them as observed.
10. **`black`.** `black --check runregistrykit docs` reports 31 files at `2bf9c72`, and after 02b
    still 31: no file is added under either.
11. **Line citations.** Take every citation in the log and on the board from `grep -n` on the file
    as committed, after `black`, and re-check them just before committing. The board's "Package
    lines" notes for 03, 04 and 05's entries cite `__init__.py` lines that 02b moves (`list_runs`,
    `liveness`, `Run.finish`, `begin` …): add a "Package lines (02b, this commit)" sentence to each
    entry that cites one, as 02 did, and change nothing else in those entries.
12. **Mutation diffs** are taken after `black`, from the tree as it will be committed, so that each
    applies to the commit as recorded. (m1)–(m3) restore 02's code in the amended places, so each is
    a diff against the new tree, not a revert to `2bf9c72`.
13. **§3.5, the sweeps against `2bf9c72`,** is run by copying the new `test_status_writes.py` into
    a scratch clone of `2bf9c72` and running the new tests there. A test that cannot run there
    because it reads a bookkeeping name the old writer does not have (the `finish` sweep's
    in-flight check reads `in_flight`, which both have) is reported as an error, not counted as a
    catch; the log gives the failing instruction counts per mode for what does run.
14. **The board has an Orchestrator notes line.** The agent does not edit it; the review adds this
    note to it (§4).
15. **`var/`.** An ignored `var/ledger.jsonl` (two `record` lines of `{"x": 1}`, `git_head`
    `2bf9c72`, written 2026-10-17 17:14) is in the checkout, left by hand during 02's review. It is
    not the agent's and is not touched; `git status --short --ignored` lists it before and after.

**The facts, checked by the orchestrator on 2026-10-17 at `5ed97a5`.** Pass them on.
- **In-repository state.** `main` at `5ed97a5`, clean (`origin/main` at `a38022f`; `91e8e9c` and
  `5ed97a5` unpushed). `git status --short --ignored` shows `prompts/.DS_Store`,
  `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
  `var/` and `venv/`. This checkout is the only worktree. `git diff --stat 2bf9c72 HEAD --
  runregistrykit pyproject.toml .github` is empty.
- **The suite.** `Ran 322 tests in 134.049s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad;
  `var/ledger.jsonl` unchanged by it (SHA-256 `471d0859…`). No Ray process before or after;
  `RAY_ADDRESS` unset.
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0. `uv` at `/opt/local/bin/uv`;
  `/opt/local/bin/python3.12`. `requires-python = ">=3.12"` (`pyproject.toml:9`). CI runs the suite
  on 3.12.15 (`low`) and 3.13.16 (`high`), and the core job on 3.12.15, all on `ubuntu-24.04`.
- **The package lines the prompt cites** were read at `5ed97a5` and are as it says: `import copy`
  `:64`, `itertools` `:67`, `threading` `:74`; the writer section from `:259`; `_STATUS_LOCK`
  `:265`; `_STATUS_WRITES` `:270`; `_status_temporary_name` `:276`; `_remove_quietly` `:284`;
  `_land_status` `:291`, its discard check `:311`, its put-back check `:318`, the `return` `:320`,
  the record `:321`; `_write_status` `:324`, `earlier` `:336`, the merge `:337-343`; `Run._update`
  `:691`, its long line `:696`, its body `:723`; `finish`'s "signal" `:755`.
- **`test_status_writes.py`** at `2bf9c72`: 488 lines, 15 tests in eight classes
  (`TestAHandlerInsideAHeartbeat`, `TestASecondRunObject`, `TestAHandlerDuringThePutBack`,
  `TestARealSignal`, `TestTwoThreads`, `TestThePlainWrite`, `TestAnOldRecord`, on the base
  `StatusTestCase`, with the helpers `Interruption` and `a_handler`). The real-signal children run
  under `CHILD_TIMEOUT = 60`.
- **The issue index** counts 10. After 02b it is 8, unless the work opens one.

**What the review exists to establish.**
- **(B1) The files.** Only §0's list changes; outside the writer section and `_update`'s
  docstring, `__init__.py` is byte-identical; the 15 existing tests are unchanged.
- **(B2) The plain write.** As 02's: one read, one write, one `os.replace`, the same keys, mode and
  name.
- **(B3) The merge.** Both measured cases end `stage` `B` and `killed`; one handler write still
  `killed`; a discarded heartbeat's fields still kept.
- **(B4) The record.** Never lowered: the put-back's early `return` pinned, the (o2) sequence
  `killed`, the 15 points of the heartbeat sweep gone.
- **(B5) The sweep.** Every writer instruction reached, nested code objects included; the handler
  not counted; the tool id freed; failing against `2bf9c72`; bounded in time.
- **(B6) The tests bite.** (m1)–(m5), and the orchestrator's.
- **(B7) The records.** The log, the board, the index and the campaign line.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `var/`, `*.egg-info/`, `__pycache__/` and `.DS_Store`
  are ignored and must not be staged. Count, then paste. A log states only what the diff, the
  commands and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 1.
- **Mutation diffs.** Recorded in the log as unified diffs with repository paths, checked **as
  recorded** with `git apply --check` and `-R --check`, in `bash`, in a scratch clone. None is
  committed. After each, `git status` here must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-02b/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. **No scratch file goes under
  `runregistrykit/` or `docs/`.** The §3.4 probe lives there and is not committed.
- **Signals.** A test, the probe and a mutation run signal only a child process they started, and
  the child signals only itself. The sweep sends no signal at all. Nothing signals this shell, the
  agent's own process or any other.
- **Ray.** The agent starts no Ray, and records `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` before and after every suite run.
- **GitHub.** Nothing is pushed, no tag is made, no workflow is dispatched.
- **Stop conditions are real** (the prompt's §5). A stop goes to the user through the orchestrator,
  and the agent resumes with `SendMessage`. A defect found elsewhere in the package is opened on the
  board, never fixed.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone.
2. **The prompt's gate**, and the suite: 322, one skip, in `venv/`, its time recorded (correction 1).
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 10 now, 8 after unless the work opens one. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and
  `CLAUDE.md`;
- `HEAD`, the suite count and time, and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02b-the-writers-bookkeeping.md`, in README §5.1's
  form, with the prompt's §4.3 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It installs only the core venv of correction 2, sets `TMPDIR` for every command, and starts no
  Ray.**
- **It signals only children it started** (§0, "Signals").
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **Scope (B1).** `git show --stat <commit>` touches only §0's list. `git diff <note's commit>
   <commit> -- runregistrykit/stores.py runregistrykit/__main__.py runregistrykit/client.py
   pyproject.toml .github README.md PROVENANCE.md CLAUDE.md docs/adoption
   prompts/interrupted-runs/README.md prompts/interrupted-runs/02b-the-writers-bookkeeping.md
   prompts/interrupted-runs/orchestrator` is empty. `runregistrykit/tests/` changes only
   `test_status_writes.py`, and its diff adds lines only (no existing test's line changed or
   removed, the module docstring aside if it says what the new classes do). In `__init__.py`,
   nothing outside the writer section and `_update`'s docstring changes: `write_json_atomic`'s body
   byte-identical, `_update`'s body still the one call. No new import outside the standard library;
   no `import signal`; `git grep -n 'signal'` as correction 8.
2. **The suite, re-run by the orchestrator.** In `venv/` at the commit: `Ran 322 + N tests … OK
   (skipped=1)`, N as the log's, per module by the loader; the module's time alone. `black --check
   runregistrykit docs`: 31 files. `git status --short --ignored` the same before and after but for
   `__pycache__/`; `var/` unchanged (its one file, same SHA-256); no Ray process; no child left. The
   core run of correction 2, repeated in the orchestrator's own scratch venv, passes the four
   modules, 80 + N, with the store layer's dependencies absent.
3. **The plain write (B2), by the orchestrator's own run.** As 02's check 3, against `2bf9c72`'s
   package by `git archive` and the commit's: `begin`, `heartbeat`, `heartbeat(pid=…)`, `record`,
   `finish`, and a heartbeat under umask `0o077`. The same keys after every call, the same number
   of reads of `status.json` and of `os.replace` calls, the same modes, a source named
   `status.json.<unique>.tmp`, nothing left behind.
4. **The merge (B3), by the orchestrator's own probe.** In one process, `json.dump` patched to fire
   once, against the commit and against `2bf9c72`: the two measured cases, the one-write case, and
   a heartbeat discarded by a handler's `heartbeat(stage=…)` then overtaken (its `units_done`
   kept). The commit: `stage` `B` with `killed`; `killed` 143; `killed` 143; the units kept.
   `2bf9c72`: `stage` `A`; `done` 0; `killed`; kept. Then **three handler writes** inside one
   heartbeat (a heartbeat `stage=B`, a heartbeat `stage=C`, a `finish("killed")`), which no test
   names: the commit ends `stage` `C` and `killed`. Record the result either way; a lost state is
   a finding against acceptance and goes to the user.
5. **The record (B4) and the sweep's reach (B5), by reading and by the orchestrator's own sweep.**
   - Read the helper and every place the record is read or written: no lower number can be the
     highest key after any store or prune, whatever instruction a handler interrupts, and the
     helper never returns a number with no payload. Say how in the verdict.
   - Re-run the sweep's two tests by name with a counting wrapper of the orchestrator's own (in
     scratch, not committed) that reports, per code object, the instructions reached and attempts
     made: every writer code object is reached, nested ones included (correction 3); the handler's
     own write is not counted; after the module, `sys.monitoring.get_tool` is `None` for the id the
     test used, and no local events remain on the writer's code objects
     (`sys.monitoring.get_local_events`).
   - The (o2) sequence and the put-back's `return`: pinned by a test the log names; check it by
     (m3).
6. **The real signal, unchanged.** The orchestrator's own probe from 02's check 5, written again in
   the scratchpad against the commit: twelve cases, four points × three endings, a child per case.
   Every case parses, `killed`, 143, `units_done` 7; nothing left but, for ending the process
   before the replace, one `status.json.<unique>.tmp`. The table matches the log's §3.4 table and
   02's review's. And 02's threads edge (a worker heartbeating in a loop, the main thread sending
   itself `SIGTERM` twenty times): joined, `killed`, 143, nothing left.
7. **The log (B7).** Every section of README §5.1 and the prompt's §4.3 additions; the deviations
   classified, corrections 1–15 among them; the suite before and after; the core run; the §3.4
   table; the sweeps against `2bf9c72` per mode (and, for the heartbeat sweep, the 15 points of the
   "At writing", or the log's reason for a different count); the sweeps after, with counts and
   times; the shape of the record; every mutation as a diff; every line citation right at the
   commit (`grep -n`).
8. **The mutations (B6).** (m1)–(m5) extracted from the log by a script and replayed in `bash` in a
   `git clone` of the commit, with `PYTHONPATH` on the clone: `--check`, apply, the named tests,
   `-R --check`, reverse, the clone clean. Each fails as the log says, the sweep's failing counts
   included. Then the orchestrator's own, each in a second clone:
   - (o1) the merge applying **no** in-flight write when the base is the landed payload (only its
     own fields): a test must fail, or the "above `L`" half of §2.2 is unpinned. It matters only
     when a write is in flight above the landed base, which needs a handler re-entered inside a
     handler's write; say whether a test reaches it, and open it on the board if none does, not a
     stop. And the comparison made `>=` the landed number: expected harmless (the base already holds
     its own write's fields); record it;
   - (o2) the helper's re-read removed (it returns whatever the first read gave): say whether a test
     fails; if none does and the reading of check 5 shows a reachable window, open it on the board;
   - (o3) the prune made to remove every key but the write's **own** (instead of every key below
     the highest): a handler that lands a later write around the store then has its key pruned by
     the earlier write, and the record is lowered. The heartbeat sweep must fail; record its count.
9. **The records (B7).** The board: the header, 02b's row ("this commit", 322 → 322 + N), W2 ✅,
   both entries moved to §4, each with what resolved it and the tests that pin it, the other
   entries' "Package lines (02b, …)" sentences (correction 11), the §3 count line.
   `docs/OPEN_ISSUES.md`: 8 by counting its rows (or as the work opened), the two rows gone, the
   date. `prompts/INDEX.md`: the campaign's line. **CI is read after the push (§4)**: all three jobs
   green, the core job's count 80 + N, the `suite (high)` job running the sweeps on 3.13.16. Until
   then the verdict says "pending CI".

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02b* paragraph (*At dispatch*,
  *The checks*, verdict), and add this note to the board's **Orchestrator notes** line, marked
  "used for 02b". Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the campaign README's §2 row and in
    `prompts/INDEX.md`;
  - "reviewed" for 02b in the board's header and row, the README's §2 status column and
    `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Ask the user whether to push `main`.** The sweeps first run on Linux and on 3.13 in CI. Once
  they have run, read the result (check 9) and record it on the board in a records commit of its
  own.
- **Report to the user:**
  - what landed, 322 → 322 + N, and the two issues closed;
  - the sweeps before and after, per mode;
  - check 4's cases, the three-write case among them;
  - the mutations, the agent's and the orchestrator's;
  - CI, or that it is pending a push;
  - that 03 is next, and is written only after this review.
