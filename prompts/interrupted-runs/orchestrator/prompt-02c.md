# Orchestrator — prompt 02c, the writer's lock

Read [`../README.md`](../README.md) first: §0, §1 (no signal handling in the package), §5 (every
rule; 4, 6, 7 and 10 especially) and §6.2 (L5 with its amendment, and L11, taken (a)). The
conventions are those of [`prompt-02b.md`](prompt-02b.md), restated in §0 because the agent reads
§0 and not this directory. Where this note and the prompt differ, this note is right for 02c.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names, at 3.12, 3.13 and 3.14;
- replay the log's mutation diffs with `git apply` in a scratch clone, and revert them;
- build venvs, client roots and run directories of your own in the session scratchpad, and run the
  package in them, child processes that signal themselves included;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review. **Nothing is pushed** by the
agent, and nothing by the orchestrator without the user's clear yes (§4).

**The prompt:** [`02c-the-writers-lock.md`](../02c-the-writers-lock.md)
**Narrows** (L11 (a)): `[02b-a-raising-handler-can-leave-the-status-lock-held]`, closed at 3.12 and
3.13 and left open, with no owner, for the 3.14 `with` point · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: 02b landed and reviewed (`2959b78`, `c18ec34`, CI `39060913296` recorded in
  `9d26357`); **L11 taken 2026-10-17 as (a)** (`069f1d7`), so §2.4's (a) applies and
  `pyproject.toml` is not touched; `git diff --stat 2959b78 HEAD -- runregistrykit pyproject.toml
  .github` empty; the suite 328 OK with one skip; the tree clean; MacPorts' 3.13.16 and 3.14.8
  present.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**Two lines of code, three Pythons, and a hazard that only a raising handler at one kind of
instruction can show.** The obvious fix (a loop) has the same defect, the test must interrupt the
writer only where a real interpreter runs a handler, and the evidence that matters most is a real
signal at 3.13, which the venv cannot run. So the weight of the review is on:
- **the change is two lines and a docstring sentence**, and nothing else in the writer moves (§3
  check 1);
- **no `JUMP_BACKWARD` of the writer is outside its exception table** at 3.12, 3.13 and 3.14, by
  `dis` (§3 check 4);
- **a real signal leaves the lock held nowhere at 3.12 and 3.13**, and at 3.14 only at the `with`'s
  entry (§3 check 5);
- **the new test fails against `2959b78`**, at 3.12 too, so the venv's suite and CI's `suite (low)`
  catch a regression that would only hang at 3.13 (§3 checks 6, 8);
- **every existing test and 02b's sweeps are unchanged** (§3 checks 1, 2).

**What moves on purpose:** `runregistrykit/__init__.py` (the two filter lines `:365`, `:372`, a
one-line comment, and one sentence of `Run._update`'s "Not covered" paragraph `:756-762`);
`runregistrykit/tests/test_status_writes.py` (additions only, after 02b's sweep class); the new log
`prompts/interrupted-runs/logs/02c-the-writers-lock.md`; the board; the campaign README's §2 row for
02c only; `docs/OPEN_ISSUES.md`; `prompts/INDEX.md`. **Nothing else**: not `pyproject.toml` (L11 is
(a)), `stores.py`, `__main__.py`, `client.py`, `.github/`, `README.md`, `PROVENANCE.md`,
`CLAUDE.md`, `docs/adoption/`, any other test module or fixture, the prompt, any other part of the
campaign README, or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **L11 is (a).** The user took it on 2026-10-17 (`069f1d7`; README §6.2, the board's decisions
   table). §2.4's (a) applies: the docstring sentence is added, `pyproject.toml` is not changed, and
   the issue is **narrowed**, not closed: it stays in §3 with owner none, its hook narrowed to the
   3.14 `with` point, and the index count stays 9. Every "under (b)" in the prompt is inert.
2. **The suite's time.** The gate run is given below; 02b's review saw 120 s. Run the suite in the
   foreground with a Bash timeout of at least 600 000 ms, output to a file in your scratch, and
   grep the verdict from the file. A slow run is not a stop; a failing one is.
3. **The core run of §3.2** is 02b's: `uv venv -p /opt/local/bin/python3.12 <scratch>/core`, then
   `uv pip install --offline -p <scratch>/core/bin/python -e <this checkout>`, `TMPDIR` in scratch,
   `datastorekit`, `ray` and `sqlalchemy` shown not findable, the four core modules by name: 86 at
   `2959b78`, 86 + N after. This is the one install allowed; nothing goes into `venv/` or MacPorts'
   Pythons. Remove the venv afterwards.
4. **Running 3.13 and 3.14 (§3.3, §3.5).** `/opt/local/bin/python3.13` and `python3.14` run the
   checkout through `PYTHONPATH=<this checkout>` and the standard library only: `test_status_writes`
   and `test_host` need nothing else. They are never given `-m pip`. A scratch clone is run the same
   way with `PYTHONPATH` on the clone, so that its children run it too.
5. **Two meanings of "handler" in §2.5.** In writes (2) and (3) the writes made from inside
   `json.dump` by `made_inside` (the inner heartbeats) are **part of the write swept**: their
   instructions are counted and interrupted. The **sweep's** handler, `finish("killed",
   exit_code=143)` then `raise SystemExit(143)`, is the one whose own instructions are not counted
   (02b's `Attempt.busy`). Say so in the test's docstring.
6. **Targeting `JUMP_BACKWARD`.** 02b's `Attempt` fires at the `at`-th instruction counted. The
   new test may record, in its uninterrupted run, the `(code, offset)` of each instruction in order,
   and then make one attempt at each index whose opname, by `dis.get_instructions(code)` matched on
   offset, is `JUMP_BACKWARD`. Subclassing or wrapping `Attempt` and `Instructions` is allowed;
   editing them is not (the prompt's §2.3). The order of instructions is deterministic for a fresh
   run, so the index identifies the same instruction in each attempt; the test checks that the
   instruction it interrupted is the one it meant (code and offset), and fails if not.
7. **The lock check uses no private method.** Another thread's `_STATUS_LOCK.acquire(blocking=
   False)`, released at once if it succeeds, joined with a timeout. If it fails, the child releases
   the lock on the thread that holds it (the child's main thread, where the write ran) by `release()`
   until another thread's check succeeds, bounded in count, so later attempts mean something.
   Reading `runregistrykit._STATUS_WRITES` for the in-flight entry is read-only, as 02b's finish
   sweep does.
8. **"Each write made at least one attempt"**, and the counts 3, 7 and 12 of the "At writing" are
   the planner's: give the counts seen at each version in the log; a different count is not a stop
   if every `JUMP_BACKWARD` reached was attempted and the test's assertions hold.
9. **The static check of §3.4** covers every code object of `the_writers_code()`, not only
   `_write_status`: the generator expressions are new nested code objects, and their own tables
   must cover their `JUMP_BACKWARD`s (or say why an uncovered one cannot leave the lock held: an
   exception there leaves the generator's frame and surfaces at the covered `CALL` of `list`). Give
   the table per code object and version, against the change and against `2959b78`.
10. **The real signal of §3.5.** Run the rows **one at a time**, not as fourteen children at once,
    so the counts are not measured under load; give the interruptions per row and how many fell
    inside the writer. The child signals only itself; nothing else is signalled. **In zsh**, a loop
    over `"python tree"` pairs does not split words: write each command out, or use `${=spec}`.
    `print(..., flush=True)` before any `os._exit`.
11. **The twelve-case probe of §3.6** at 3.12 (venv) and at 3.13 (MacPorts, `PYTHONPATH`); give
    both tables.
12. **The one-line comment** at `:365` says why the filters are generator expressions (an inlined
    comprehension's or a loop's filter is outside the exception table, so a handler raising at its
    jump would skip the `with`'s exit and the `finally`), in words that say "handler" and not
    "signal" and name no issue: §3.9's grep must still find `finish`'s docstring only (`:796`), and
    `test_package_is_generic`'s citation guard must pass. The docstring sentence of §2.4 says
    "handler" too.
13. **Line citations.** Take every citation in the log and on the board from `grep -n` on the files
    as committed, after `black`, and re-check them just before committing. Add a "Package lines
    (02c, this commit)" sentence to each §3 entry whose cited `__init__.py` lines 02c moves, and
    change nothing else in those entries.
14. **Mutation diffs** are taken after `black`, from the tree as it will be committed, and replayed
    as recorded (`git apply --check`, apply, the named tests at 3.12 and, for (m1), at 3.13 too,
    `-R --check`, reverse, the clone clean).
15. **`black`.** 31 files at `2959b78`, and 31 after: no file is added under `runregistrykit` or
    `docs`.
16. **The board has an Orchestrator notes line**, and the campaign README's row for 02c a status
    column. The agent does not edit the notes line; it sets 02c's status to "landed, not yet
    reviewed" in both rows, as 02b did.

**The facts, checked by the orchestrator on 2026-10-17 at `069f1d7`.** Pass them on.
- **In-repository state.** `main` at `069f1d7`, clean (`origin/main` at `c18ec34`; `9d26357`,
  `149918f` and `069f1d7` unpushed). `git status --short --ignored` shows `prompts/.DS_Store`,
  `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
  `var/` and `venv/`. `var/ledger.jsonl` (`471d0859…`) is 02's review's, and is not touched. This
  checkout is the only worktree. `git diff --stat 2959b78 HEAD -- runregistrykit pyproject.toml
  .github` is empty.
- **The suite.** `Ran 328 tests in 120.555s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad. No Ray process; `RAY_ADDRESS` unset.
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0. `/opt/local/bin/python3.12` (3.12.15),
  `python3.13` (3.13.16), `python3.14` (3.14.8); `uv` at `/opt/local/bin/uv`.
- **The lines the prompt cites** were read at `069f1d7` and are as it says: `_write_status` `:352`,
  the `with` `:355`, `next()` `:362`, the comprehensions `:365` and `:372`, the `finally`
  `:381-382`; `_update`'s docstring from `:725`, "Not covered" `:756-762`; in the test module
  (965 lines, 21 tests), `made_inside` `:497`, `WRITER_SECTION` `:591`, `the_writers_code` `:608`,
  `Attempt` `:654`, `Instructions` `:667`, `ending_of` `:773`, `SWEEPER` `:906`,
  `TestAHandlerAtEveryInstruction` `:920`.
- **The issue index** counts 9, the row's owner 02c. After 02c, under (a): 9, the owner none, the
  hook narrowed to 3.14.

**What the review exists to establish.**
- **(K1) The files and the lines.** Only §0's list; in `__init__.py` the two lines, the comment and
  the sentence; the tests additions only.
- **(K2) The table.** No writer `JUMP_BACKWARD` uncovered at 3.12, 3.13, 3.14.
- **(K3) The real signal.** 0 held at 3.12 and 3.13; at 3.14 the `with`'s entry only.
- **(K4) The test.** Deterministic, at `JUMP_BACKWARD` only, lock and in-flight checked, failing
  against `2959b78` at 3.12 and 3.13.
- **(K5) Nothing else moved.** Existing tests, 02b's sweeps, the twelve cases, the plain write.
- **(K6) The tests bite.** (m1)–(m4), and the orchestrator's.
- **(K7) The records**, with the issue narrowed, not closed.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `var/`, `*.egg-info/`, `__pycache__/` and `.DS_Store`
  are ignored and must not be staged. Count, then paste. A log states only what the diff, the
  commands and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 2.
- **Mutation diffs.** As correction 14. None is committed. After each, `git status` here must be
  clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-02c/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. **No scratch file goes under
  `runregistrykit/` or `docs/`.** The probes live there and are not committed.
- **Signals.** A test, a probe and a mutation run signal only a child process they started, and the
  child signals only itself. The new test sends no signal at all. Nothing signals this shell, the
  agent's own process or any other.
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
2. **The prompt's gate**, and the suite: 328, one skip, in `venv/`, its time recorded.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 9 now, 9 after under (a). Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and
  `CLAUDE.md`;
- `HEAD`, the suite count and time, and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and plainly: one commit at the
end; the files of §0 only; the core venv of correction 3 the only install; `TMPDIR` for every
command; no Ray; signal only children it started; push nothing, tag nothing; stop and ask on the
prompt's §5.

## 3. The review — nine checks

1. **Scope (K1).** `git show --stat <commit>` touches only §0's list. `git diff <note's commit>
   <commit> -- pyproject.toml runregistrykit/stores.py runregistrykit/__main__.py
   runregistrykit/client.py .github README.md PROVENANCE.md CLAUDE.md docs/adoption
   prompts/interrupted-runs/02c-the-writers-lock.md prompts/interrupted-runs/orchestrator` is
   empty; the campaign README's diff is 02c's row only. In `__init__.py`, the diff is the two lines,
   the comment and the docstring sentence (`git diff -U0`, counted); the test module adds lines and
   removes none, and 02b's named helpers are byte-identical.
2. **The suite (K5).** In `venv/` at the commit: `Ran 328 + N tests … OK (skipped=1)`, per module by
   the loader. At 3.13.16 and 3.14.8, `test_status_writes` and `test_host` by `PYTHONPATH`: `OK
   (skipped=1)`, 49 + N. `black --check runregistrykit docs`: 31 files. The core run of correction
   3 in the orchestrator's own scratch venv. `git status --short --ignored` and `var/` the same
   before and after; no Ray; no child left.
3. **The plain write and the re-entered writes (K5).** The orchestrator's probes of 02b's review,
   against the commit: the plain-write probe's output identical to `2959b78`'s; the merge probe's
   six cases as at `2959b78` (`stage` B and `killed`; `killed`; `killed`; units kept; `stage` C;
   `killed`, C); the threads edge.
4. **The table (K2).** The orchestrator's own `dis` script over `the_writers_code()` at 3.12.15,
   3.13.16 and 3.14.8, against the commit and `2959b78`: the uncovered instructions per code object
   between the first and last table entries. No `JUMP_BACKWARD` uncovered in `_write_status` at
   any version after the change; the generator expressions' own as correction 9 says.
5. **The real signal (K3).** The orchestrator's `bombard.py` and `consequence.py` (02b's review),
   one row at a time: 45 s at 3.12, 3.13 and 3.14 against the commit; 120 s at 3.13; the
   `finish`-then-raise variant at 3.13. 0 lock held and 0 in-flight kept at 3.12 and 3.13; at 3.14
   held only at the `with` (`:355`), no in-flight entry kept. Any other row is a finding against
   acceptance and goes to the user.
6. **The twelve cases (K5).** The orchestrator's `signals.py` at 3.12 and 3.13 against the commit:
   `killed`, 143, `units_done` 7 in all twelve; one `.tmp` only where the process ends before the
   replace.
7. **The log (K7).** Every section of README §5.1 and the prompt's §4.3 additions; the deviations
   classified, corrections 1–16 among them; the suite, core, 3.13 and 3.14 runs; the static table;
   the real-signal table with interruptions per row; the twelve cases; the new test against
   `2959b78`; every mutation as a diff; line citations right at the commit by `grep -n`.
8. **The mutations (K6).** (m1)–(m4) extracted from the log by a script and replayed in a `git
   clone` of the commit, the new test and `test_status_writes` at 3.12, and (m1) at 3.13 too. Each
   fails as the log says. Then the orchestrator's own:
   - (o1) `:372` as a `for` loop with an `if`, the first line kept: the new test must fail (write
     (3)); if it does not, the second line is unpinned against the loop form;
   - (o2) `:365` as `sorted({n for n in book["in_flight"] if n < number})`, a set comprehension:
     the new test must fail;
   - (o3) the new test's lock check disabled (it always reports free), against `2959b78`'s writer:
     the test must still fail by its in-flight check, or the lock check is the only thing that
     catches a hang; record which.
9. **The records (K7).** The board: the header, 02c's row ("this commit", 328 → 328 + N), W3, the
   issue's entry in §3 narrowed to the 3.14 `with` point with owner none, what 02c resolved and the
   test that pins it, the "Package lines (02c, …)" sentences, the §3 count line. The campaign
   README's 02c row. `docs/OPEN_ISSUES.md`: 9 by counting, the row's owner none and its hook
   narrowed, the date. `prompts/INDEX.md`: the campaign's line. **CI is read after the push (§4)**:
   all three jobs green, the core job's count 86 + N, the new test in `suite (high)` at 3.13.16.
   Until then the verdict says "pending CI".

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02c* paragraph (*At dispatch*,
  *The checks*, verdict), and add this note to the board's **Orchestrator notes** line, marked
  "used for 02c". Fix small residue in a follow-up commit of its own: "this commit" → the SHA on the
  board, in the log, in the README's §2 row and in `prompts/INDEX.md`; "reviewed" for 02c in the
  board's header and row, the README's §2 status column and `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Ask the user whether to push `main`.** The new test first runs on Linux and at 3.13 in CI. Once
  it has, read the result (check 9) and record it on the board in a records commit of its own.
- **Report to the user:** what landed, 328 → 328 + N, and the issue narrowed; the static table and
  the real-signal table, before and after; the mutations; CI, or that it is pending a push; that 03
  is next, and is written only after this review.
