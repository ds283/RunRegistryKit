# Orchestrator — prompt 02, status writes

Read [`../README.md`](../README.md) first: §0 and §0.2 (the heartbeat race), §1 (no signal handling
in the package), §5 (every rule; 6, 7, 8 and 10 especially) and §6.2 (L5, taken and refined). The
conventions are those of [`prompt-01.md`](prompt-01.md), restated in §0 because the agent reads §0
and not this directory. Where this note and the prompt differ, this note is right for 02.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names;
- replay the log's mutation diffs with `git apply` in a scratch clone, and revert them;
- build venvs, client roots and run directories of your own in the session scratchpad, and run the
  package in them, child processes that signal themselves included;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review. **Nothing is pushed** by the
agent, and nothing by the orchestrator without the user's clear yes (§4).

**The prompt:** [`02-status-writes.md`](../02-status-writes.md)
**Closes:** `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` · **Opens:**
only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: 01 landed and reviewed (`387c58f`, `5d71a6b`, CI `c2911d3`), L5 taken, `git
  diff --stat 387c58f HEAD -- runregistrykit pyproject.toml .github` empty, the suite 307 OK with
  one skip, the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It changes how every `status.json` is written, under re-entrance.** The diff will be small and the
cases many: a write re-entered at four points, ended three ways, from one `Run` or two, on one
thread or two. The weight of the review is on five things:
- **an un-re-entered write is exactly today's write**: the same keys, one read, one `os.replace`,
  the same mode (§3 checks 3, 4);
- **a terminal state is never undone** by a write that began before it, at any of the four points,
  however the handler ends (§3 checks 5, 6);
- **nothing waits on the write it interrupted** (§3 check 6, the `RLock`);
- **`write_json_atomic` and every sidecar write are untouched** (§3 check 1);
- **the tests bite**: ten mutations, one of which hangs any in-process re-entrance (§3 check 8).

**What moves on purpose:** `runregistrykit/__init__.py`; new
`runregistrykit/tests/test_status_writes.py`; one line of `.github/workflows/tests.yml` (the core
job's test list); the new log `prompts/interrupted-runs/logs/02-status-writes.md`; the board;
`docs/OPEN_ISSUES.md`; `prompts/INDEX.md`. **Nothing else**: not `stores.py`, `__main__.py`,
`client.py`, `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption/`, any
other test module or fixture, the prompt, the campaign README or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The suite's time.** 01's review saw 132–155 s, and the gate run here 99 s. Run it in
   the foreground with a timeout of at least 600 s, write its output to a file, and grep the
   verdict from the file. Record the time seen. A slow run is not a stop; a failing one is.
2. **The core run of §3.2** is 01's: `uv venv -p /opt/local/bin/python3.12 <scratch>/core`, then
   `uv pip install --offline -p <scratch>/core/bin/python -e <this checkout>`, with `TMPDIR` in the
   scratchpad, and `datastorekit`, `ray` and `sqlalchemy` shown not findable. At `387c58f` it ran
   65 tests with one skip; after 02 it is 65 + N, every new test being core. This is the one install
   allowed, and nothing is installed into `venv/`. The venv is removed afterwards.
3. **`begin`'s first status goes through `Run._update`** (`__init__.py:940`), so it is written by
   the new writer too. `_update` is the package's only writer of `status.json`
   (`grep -n 'status_path\|"status.json"\|_update(' runregistrykit/*.py` at `34afe6d`: `_update`'s
   write `:599`, its callers `:619`, `:650`, `:656`, `:940`; the read in `list_runs` `:992`). So
   "status.json, and only status.json" and "used by `Run._update` and by nothing else" are one
   rule, and no `status.json.tmp` is written by anything after 02.
4. **The children of §2.6's real-signal test** import the package as `CHECKER` and `CRASHER` do
   (`test_run_registry.py:31-34`, `:98-102`): a script written into the test's temporary directory
   that does `sys.path.insert(0, PACKAGE_PARENT)` before `import runregistrykit`, `PACKAGE_PARENT`
   from `client_fixtures`. A child then runs the tree the test imported, so a mutation replayed in a
   clone is seen by it. Each child runs under `subprocess.run(..., timeout=…)`; a timeout of 60 s
   or less is ample, and `TimeoutExpired` (which kills the child) is how (m9) fails. The child's
   client root and runs root are the test's, in its `tempfile` directory.
5. **Patching.** The writer looks up `json.dump` and `os.replace` through their modules at call time,
   as `write_json_atomic` does, so `mock.patch("json.dump", …)` and `mock.patch("os.replace", …)`
   reach it; `TestStatus`'s replace test already patches `"os.replace"` that way
   (`test_run_registry.py:607`). "Fire once, for the heartbeat's write only" is the test's to
   arrange; the inner `finish` goes through the real functions.
6. **Step 2 is implemented as the prompt writes it**, and not refined. The orchestrator notes one
   case it does not cover, for the log's "Observations not acted on" if the agent agrees, and for
   the review to measure: a heartbeat `stage=A` in flight; a first handler's `heartbeat(stage=B)`
   lands; a second handler's `finish` then composes from the landed `B` payload, re-applies the
   still-in-flight `stage=A` over it, and lands `A`. A field set by an earlier in-flight write is
   re-applied over a newer landed one. It needs two handler writes inside one heartbeat's write,
   and no test of the prompt meets it. Do not change the rule, and do not open an issue for it; the
   review decides (§3 check 6).
7. **(m9) and the in-process tests.** Under (m9) every in-process re-entrance blocks for ever. Run
   only the real-signal child tests by name under (m9), each with its timeout, and never the whole
   module or suite. Kill nothing but those children.
8. **`black`.** `black --check runregistrykit docs` reports 30 files at `34afe6d`; after 02 it is
   31.
9. **Line citations.** 01's log and board cited `__init__.py` two lines short from `Run.status` on,
   and the review fixed it. Take every citation in the log and on the board from `grep -n` on the
   file as committed, after `black`, and re-check them just before committing.
10. **Mutation diffs** are taken after `black`, from the tree as it will be committed, so that each
    applies to the commit as recorded.
11. **The board has an Orchestrator notes line.** The agent does not edit it; the review adds this
    note to it (§4).

**The facts, checked by the orchestrator on 2026-10-17 at `34afe6d`.** Pass them on.
- **In-repository state.** `main` at `34afe6d`, clean (`origin/main` at `c2911d3`, the two
  planning commits unpushed). `git status --short --ignored` shows `prompts/.DS_Store`,
  `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`
  and `venv/`. This checkout is the only worktree. `git diff --stat 387c58f HEAD -- runregistrykit
  pyproject.toml .github` is empty.
- **The suite.** `Ran 307 tests in 99.007s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad.
  No Ray process before or after; `RAY_ADDRESS` unset.
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0. `uv` at `/opt/local/bin/uv`;
  `/opt/local/bin/python3.12`.
- **The package lines the prompt cites** were read at `34afe6d` and are as the prompt says:
  imports `:64-75`, `__all__` from `:77`; `read_json` `:234`; `write_json_atomic` `:244-253`;
  `class Run` `:531`, `__init__` `:534`; `status` `:592`; `_update` `:595-600`; `heartbeat` `:602`;
  `finish` `:621`, its docstring's "signal" `:632`, its interrupted-fingerprint `_update` `:650`;
  `record` `:688`; `begin`'s manifest write `:938`, its first status `:940-947`; `stores._tmp_path`
  `:255`. `TestStatus` `test_run_registry.py:604`, the replace test `:605`, the torn-read test
  `:621`. The core job's test line `.github/workflows/tests.yml:89`.
- **`git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'`** finds `:632` only.
- **The issue index** counts 9. After 02 it is 8, unless the work opens one.

**What the review exists to establish.**
- **(W1) The files.** Only §0's list changes; `write_json_atomic`'s body and every sidecar write
  are unchanged.
- **(W2) The plain write.** No re-entrance: the same keys and values, one read, one `os.replace`,
  the mode `0666` less the umask, a name `status.json.<unique>.tmp`; a `v0.1.0` record kept as it
  was, with no `host` added.
- **(W3) The re-entered write.** The eight cases of the reproduction, the second `Run`, the
  put-back's own re-entry, and the real signal three ways: parseable, terminal, the heartbeat's
  fields kept, nothing left behind but the documented leftover.
- **(W4) Threads.** The `RLock`; two threads serialised; no handler waits on its own write.
- **(W5) The tests bite.** (m1)–(m10).
- **(W6) The records.** The log, the board, the index and the campaign line.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff, the commands
  and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 1.
- **Mutation diffs.** Recorded in the log as unified diffs with repository paths, checked **as
  recorded** with `git apply --check` and `-R --check`, in `bash`, in a scratch clone. None is
  committed. After each, `git status` here must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-02/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. **No scratch file goes under
  `runregistrykit/` or `docs/`.** The §3.4 probe lives there and is not committed.
- **Signals.** A test, the probe and a mutation run signal only a child process they started, and
  the child signals only itself. Nothing signals this shell, the agent's own process or any other.
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
2. **The prompt's gate**, and the suite: 307, one skip, in `venv/`, its time recorded (correction 1).
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 9 now, 8 after unless the work opens one. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and
  `CLAUDE.md`;
- `HEAD`, the suite count and time, and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-status-writes.md`, in README §5.1's form, with
  the prompt's §4.3 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It installs only the core venv of correction 2, sets `TMPDIR` for every command, and starts no
  Ray.**
- **It signals only children it started** (§0, "Signals").
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **Scope (W1).** `git show --stat <commit>` touches only §0's list. `git diff <note's commit>
   <commit> -- runregistrykit/stores.py runregistrykit/__main__.py runregistrykit/client.py
   pyproject.toml README.md PROVENANCE.md CLAUDE.md docs/adoption prompts/interrupted-runs/README.md
   prompts/interrupted-runs/02-status-writes.md prompts/interrupted-runs/orchestrator` is empty, and
   the workflow's diff is the one line. `runregistrykit/tests/` gains exactly
   `test_status_writes.py`, and no existing module changes. In `__init__.py`,
   `write_json_atomic`'s body is byte-identical (`git diff` of `:244-253` empty in substance), its
   place in `__all__` kept, and nothing but `_update`, the new private writer, its bookkeeping, an
   `import threading` and docstrings that cite the write changes. `git grep -n 'signal'` as the
   prompt's §3.3; no `import signal`, no `tempfile`.
2. **The suite, re-run by the orchestrator.** In `venv/` at the commit: `Ran 307 + N tests … OK
   (skipped=1)`, N as the log's, per module by the loader. `black --check runregistrykit docs`: 31
   files. `git status --short --ignored` the same before and after but for `__pycache__/`; no
   `var/`; no Ray process; no stray process left by a child (`pgrep -f` for the child scripts'
   names). The core run of correction 2, repeated in the orchestrator's own scratch venv, passes the
   four modules with the store layer's dependencies absent.
3. **The plain write (W2), by the orchestrator's own run.** In a scratch client root: `begin`, then
   `heartbeat` with `os.replace` and `open` wrapped. One `os.replace` from
   `status.json.<unique>.tmp` in the run directory, one read of `status.json`; the keys after
   `begin`, `heartbeat`, `heartbeat(pid=…)`, `record` and `finish` exactly those `387c58f` writes for
   the same calls, compared against a run made by `git archive 387c58f`'s package in a second
   scratch directory. The mode under umask `0o022` and `0o077` equal to `write_json_atomic`'s. A
   `v0.1.0`-form status (no `host`) heartbeated and finished keeps its keys and gains no `host`;
   `liveness` the same from both trees.
4. **`write_json_atomic` and the sidecars.** `write_json_atomic` still replaces from `<path>.tmp`
   (a direct call, `os.replace` wrapped). The sidecar tests that name `<sidecar>.tmp` pass
   unchanged (check 2 covers them).
5. **The re-entered write (W3), by the orchestrator's own probe.** In the scratchpad, against the
   commit, a child process per case with a real `SIGTERM` from inside a heartbeat's `json.dump`
   (`units_done=7`), half the payload or all of it written, the handler raising, returning or
   ending the process: the prompt's §3.4 table, written again by the orchestrator. Every case
   parses, `killed`, 143, `units_done` 7; nothing left behind but, for ending the process, one
   `status.json.<unique>.tmp`. Then the same six against `34afe6d`'s package, which must reproduce
   the "At writing" table's fixed-name rows.
6. **The edges (W3, W4).**
   - **(P3) and (P4) by a real signal**: the probe's handler sent from inside `os.replace`, before
     and after the real replace, raising and returning: `killed` and 143 each time.
   - **Two `Run` objects in different processes are not ordered** (the prompt's §2.3): a launcher's
     `heartbeat(pid=…)` from another process still reads the file. A heartbeat in a child after the
     parent's `finish` keeps `killed`.
   - **A handler on the main thread while a worker thread holds the lock**: a worker thread
     heartbeating in a loop, the main thread sent `SIGTERM` by itself, the handler calling
     `finish`. It completes within a timeout, `killed`.
   - **Correction 6's case**, measured: if it lands `A`, record it on the board's §3 as an issue
     (a stage regressed, never a state), unless the agent's log shows a state can be lost by it, in
     which case it is a finding against acceptance and goes to the user.
7. **The log (W6).** Every section of README §5.1 and the prompt's §4.3 additions; the deviations
   classified, corrections 1–11 among them; the suite before and after; the core run; the §3.4
   table; every mutation as a diff; the documented leftover stated; every line citation right at
   the commit (`grep -n`).
8. **The mutations (W5).** (m1)–(m10) extracted from the log by a script and replayed in `bash` in a
   `git clone` of the commit (`--check`, apply, the named tests, `-R --check`, reverse, the clone
   clean), each failing as the log says. (m9) by name, the real-signal tests only, each child
   timing out. Then the orchestrator's own, each in a second clone:
   - (o1) the writer's file opened with `open(name, "w")` instead of `O_EXCL`: no test need fail;
     say whether two writes can then share a name (they cannot if the name is unique), and record
     it;
   - (o2) step 6's record of what landed made unconditional (a lower number may overwrite a higher
     one): a test must fail, or the put-back's base is unpinned. Open it on the board if none does,
     not a stop;
   - (o3) the `RLock` made per `Run` object rather than per path or module: say whether a test
     fails; record it.
9. **The records (W6).** The board: the header, 02's row ("this commit", 307 → 307 + N), W1 ✅, the
   entry moved to §4 with its five answers and their tests, the other three entries' "Package lines
   (02, …)" notes, and the unreadable-status entry's one sentence. `docs/OPEN_ISSUES.md`: 8 by
   counting (or as the work opened), the row gone, the date. `prompts/INDEX.md`: the campaign's
   line. **CI is read after the push (§4)**: all three jobs green, the core job's count 65 + N.
   Until then the verdict says "pending CI".

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph (*At dispatch*,
  *The checks*, verdict), and add this note to the board's **Orchestrator notes** line, marked
  "used for 02". Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the campaign README's §2 row and in
    `prompts/INDEX.md`;
  - "reviewed" for 02 in the board's header and row, the README's §2 status column and
    `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Ask the user whether to push `main`.** The new module first runs on Linux in CI. Once it has
  run, read it (check 9) and record the result on the board in a records commit of its own.
- **Report to the user:**
  - what landed, 307 → 307 + N, and the issue closed;
  - the probe's table, before and after;
  - the mutations, the agent's and the orchestrator's;
  - correction 6's case, measured, and what was done with it;
  - CI, or that it is pending a push;
  - that 03 is next, and is written only after this review.
