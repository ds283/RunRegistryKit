# Orchestrator — prompt 04, end a run

Read [`../README.md`](../README.md) first: §0, §1, §5 (every rule; 4, 6, 7, 8, 9 and 10
especially) and §6.2 (L3, L4, L7 and L8 with their 2026-10-18 notes, and L9, which builds on this
prompt). The conventions are those of [`prompt-03.md`](prompt-03.md), restated in §0 because the
agent reads §0 and not this directory. Where this note and the prompt differ, this note is right
for 04.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names, at 3.12, 3.13 and 3.14;
- replay the log's mutation diffs with `git apply` in a scratch clone, and revert them;
- build venvs, client roots, stores and run directories of your own in the session scratchpad, and
  run the package and the planner's probe in them;
- start a child process in the scratchpad and send it `SIGKILL`, and no other process;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review. **Nothing is pushed** by the
agent, and nothing by the orchestrator without the user's clear yes (§4).

**The prompt:** [`04-end-a-run.md`](../04-end-a-run.md) · **Closes:**
`[a3-v2-a-hard-killed-run-blocks-its-store]` · **Opens:** only what the work finds · **Not
touched:** `[04-a-killed-process-not-yet-reaped-answers-kill-0]` and the four other open §3
entries · **Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: 03 landed and reviewed (`ab0cad9`, `4b55750`, CI `39083674030` recorded in
  `9e38581`); **L7 and L8 taken 2026-10-18, each as (a)** (`c3aa52a`); `git diff --stat ab0cad9
  HEAD -- runregistrykit pyproject.toml .github` empty; the suite 347 OK with one skip; the tree
  clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**A small command whose every branch is a person's safety, a new record every client will read,
and seven texts whose words nine assertions pin.** The command is a few dozen lines; the risk is in
a branch that accepts what it should refuse, a record whose keys drift from §2.2, and refusal texts
that change more than the one substitution. So the weight of the review is on:
- **no route accepts a live pid on this host**, `--unverified` or not, whatever the state beside
  it (README §5 rule 9, L8; §3 checks 5, 8);
- **the record is exactly §2.2's**, written through the status writer, every other field of a
  readable status kept, and nothing else written: not the manifest, `checkpoint.jsonl`, a sidecar
  or a stray file (§3 check 4);
- **the acceptance test is real**: a child begun on a store, hard-killed and reaped, then `end`,
  then every store operation and a resumed run's fingerprint succeeding (§3 checks 2, 5);
- **every existing refusal's words are kept** but for the one substitution, and only §2.4's nine
  assertion fragments change (§3 checks 1, 6);
- **`Run.finish`'s code, `liveness`' code, the writer and `__all__` do not move** (§3 checks 1, 3).

**What moves on purpose:** `runregistrykit/__init__.py` (`TERMINAL_STATES`; `Run.finish`'s
docstring, one sentence; the private `_END` constant and the private function that checks and
writes, with whatever private helpers it needs; the `getpass` import); `runregistrykit/stores.py`
(the five refusals' remedy words, `_unsure_remedy`'s sentence, the new foreign sentence,
`_refuse_if_in_use`'s docstring, and the import of the constant); `runregistrykit/__main__.py`
(the `end` subparser and its handler; the module docstring, one sentence; `list`'s stale line, one
sentence, and the line 03 added, its remedy); the nine assertion lines of §2.4's table in
`test_store_retire.py`, `test_store_amend.py`, `test_store_copy_move.py`,
`test_unreadable_status_stores.py` and `test_unreadable_status.py`; the two new test modules
`test_end.py` and `test_end_stores.py`; the core line of `.github/workflows/tests.yml` (`:89`); the
new log `prompts/interrupted-runs/logs/04-end-a-run.md`; the board; the campaign README's §2 row
for 04 only; `docs/OPEN_ISSUES.md`; `prompts/INDEX.md`. **Nothing else**: not `pyproject.toml`,
`client.py`, `fingerprint.py`, the repository `README.md` (its usage is 06's), `PROVENANCE.md`,
`CLAUDE.md`, `docs/` other than the index, any existing test module beyond its §2.4 lines, any
fixture (`store_fixtures.py`, `test_host.a_status`, `test_unreadable_status.FORMS` are imported, not
edited), the prompt, any other part of the campaign README, or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **L7 and L8 are (a)**, as the prompt states them (README §6.2, the board's decisions table,
   `c3aa52a`). Nothing in the prompt is conditional on them.
2. **The suite's time.** The gate run is given below. Run the suite in the foreground with a Bash
   timeout of at least 600 000 ms, output to a file in your scratch, and grep the verdict from the
   file. A slow run is not a stop; a failing one is.
3. **The core run of §3.2** is 03's: `uv venv -p /opt/local/bin/python3.12 <scratch>/core`, then
   `uv pip install --offline -p <scratch>/core/bin/python -e <this checkout>`, `TMPDIR` in scratch,
   `datastorekit`, `ray` and `sqlalchemy` shown not findable, the **six** core modules by name (the
   workflow's five and `test_end`): 98 at `ab0cad9`, 98 + N₁ after. This is the one install
   allowed; nothing goes into `venv/` or MacPorts' Pythons. Remove the venv afterwards. Also run
   `test_end` at `/opt/local/bin/python3.13` (3.13.16) with `PYTHONPATH` on the checkout and the
   standard library only. Never give MacPorts' Pythons `-m pip`.
4. **The thirteen forms with `--unverified` (§2.6) need a dead pid.** Three of
   `test_unreadable_status.FORMS` are readable and keep the full status's fields: "null state",
   "paused" and "state 5". A run begun in the test's own process records the test's pid, alive, on
   this host and boot; by §2.3 step 4 those three are then **refused** even with `--unverified`. So
   the acceptance of each form with `--unverified` gives the run a dead pid first
   (`run.heartbeat(pid=self.a_dead_pid())`, then `give_status_the_form`), and expects for those
   three `pid_answers` false (tested), `verified` false, `"status does not say"`; for "empty object"
   (no pid) and the nine unreadable forms, `pid_answers` null. And the refusal of a readable status
   with this process's pid and `--unverified` (§2.6) is made for **each** of those three forms, its
   message the live-pid refusal's. §2.3 is right and §2.6's bullet is read this way; it is not a
   stop.
5. **"Gives a pid"** (step 4) means the status is readable and its `pid` is not `null`. When the pid
   is tested, `pid_answers` is `pid_alive(pid)`, whose own coercion decides (a pid that is not an
   integer does not answer). In step 6, a `running` status here whose `pid` is `null` is tested and
   does not answer, so it is accepted, as `liveness` calls it `stale`; `evidence.pid` is then
   `null` and `pid_answers` false. Say so in the function's docstring.
6. **The host a refusal names** (step 5): the manifest's `host.name`, read through `_json_object`,
   or else the status's `host.id`, the rule of `list_runs`' `host`/`host_id` and `__main__._host`.
   The manifest is read for these words only; `evidence` does not record it (step 1). A manifest
   that is missing or not an object gives the id.
7. **The client root** is located before anything is written, as a check is. The function takes a
   `ClientRoot`, a directory to find one in, or `None` (the working directory), as `Run` does. Not
   finding one raises `ConfigError`, which the command prints as `!! …`, exit 1, and nothing is
   written. Whether it is located before or after §2.3's checks is the agent's choice, stated in
   the log; the tests cover a refusal with no client root findable only if it is cheap to.
8. **`ended.by`**: `getpass.getuser()`, or `null` if it raises anything (`except Exception`): its
   failures differ by version (`KeyError`, `OSError`). Not mocked in a test beyond one case, if any.
9. **The write.** `Run(path, client_root=…)._update(state="lost", exit_code=None, ended={…})`, so
   `exit_code` is written as `null` (`_update` does not drop `None`, unlike `heartbeat`). Not
   `Run.finish`, which would accept `lost` but writes no `ended` and may fingerprint. `Run.__init__`
   reads the manifest as it does today (`[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]`):
   nothing on the path to `_update` uses `Run.manifest`, and that stays so. The writer composes
   from the file again at write time, so the status the check read and the one the write composes
   from can differ if something writes between them; record that window under "Observations not
   acted on" and do not close it (`end` takes no lock, §2.3).
10. **The words.**
    - **The constant**: `_END = "python -m runregistrykit end RUN_ID --reason TEXT"` in
      `__init__.py`, beside `TERMINAL_STATES` or with the function; `stores.py` imports it in its
      existing `from . import (…)`; every text that names the command is composed from it, and
      `_END + " --unverified"` for the unverified forms. No text spells the command out by hand.
    - **The substitution**: for a refusal naming only alive and stale `running` runs on this host,
      the text is the present one with `Run.finish` replaced by `` `{_END}` `` and no other change.
      The review computes the old text with that one replacement and compares byte for byte.
    - **The foreign sentence**: once per refusal, when any entry's liveness is `foreign`, placed
      after the stale-run sentence and before 03's sentence, in the punctuation each refusal
      already uses (amend's text has no closing "Nothing was written" and no final full stop).
      Write it as one helper beside `_unsure_remedy`, with the same contract (empty when no entry
      is foreign), so 05 can reuse both.
    - **No word "signal"** in any new non-test text or docstring: §3.6's `git grep -n 'signal'`
      must still find `finish`'s docstring alone. Say "killed", "not yet reaped".
    - **`end`'s refusals** begin `Cannot end <run id>:` and end `Nothing was written` (no full stop
      after it, as the store refusals end). The live-pid refusal says a process with that pid
      exists on this host, that `--unverified` does not override it, and the zombie sentence.
11. **The zombie is the probe's, not a test's.** A deterministic unreaped child needs
    `os.waitid(…, WNOWAIT)`, which the venv's 3.12.15 lacks on macOS; any other wait races. So no
    test builds a zombie. The live-pid refusal's words, the zombie sentence among them, are pinned
    on a run begun in the test's own process. §3.3's probe shows `end` refused on the killed child
    before its reap.
12. **The acceptance test's order** (`test_end_stores`). A resumed run begun in the test's process
    is `running` and alive, and names the store, so every operation refuses it until it finishes.
    So: start the child, read its path, `SIGKILL`, `wait()` (−9); the six refusals before `end`,
    each with the tree unchanged; `end`; begin the resumed run (or begin it before the refusals, which
    then name it too) and call its `finish("done", exit_code=0, fingerprint=True)`; **then** the
    after-`end` operations, move last to a destination of its own. The child is started with
    `sys.executable`, the checkout first on its `sys.path` (from `runregistrykit.__file__`, as the
    planner's probe does), its stdout read for the path, and `addCleanup` kills and waits for it if
    it is still running, so no child is left whatever fails. It is sent `SIGKILL` by `child.kill()`
    or `os.kill(child.pid, signal.SIGKILL)`, and nothing else is signalled.
13. **An earlier boot, another host, and the platform.** The earlier-boot acceptance needs
    `this_host()`'s `id` and `boot` not `None`, and skips with a reason where either is; the
    hard-killed child's `evidence.host`/`boot` assertions likewise. macOS here has both, so no new
    skip runs here, and the suite stays at one skip. On Linux in CI both are read too; record that
    the review reads the skip count there.
14. **The nine assertions.** Exactly §2.4's table, nothing else in their tests. `git diff ab0cad9
    -- runregistrykit/tests` shows two new files and those nine lines (and black's re-wrapping of
    them). `test_unreadable_status.py`'s two docstrings that name `Run.finish` (`:22`, `:166`) and
    every other docstring stay. `REMEDY` (`:84`) becomes the new `_unsure_remedy` sentence's last
    clause from `is ended by a person`, with the backticked command and `--unverified`.
15. **The command's argument.** `RUN` is refused when it is empty, `.` or `..`, or contains
    `os.sep` or `os.altsep` (where not `None`), and when `<root>/RUN` is not a directory; each
    refusal ends `Nothing was written` and exits 1. `--root` defaults to the client config's
    `runs_root`. The top-level `--client-root` applies to `end` as to `store`.
16. **Observations, not fixes.** Record in the log, and open a §3 issue only where measured, with
    the board's and the index's counts adjusted:
    - the check-to-write window of correction 9;
    - a pid reused within one boot by a live process makes a hard-killed run on this host
      un-endable until that process exits or the machine reboots (L3 (b) is not taken; L8 (a)
      allows no override). Read, not measured: an observation, not an issue, unless the agent
      measures it;
    - anything found in `liveness`, `list_runs`, `store show` or `begin`, which this prompt does
      not change.
17. **Mutation diffs** are taken after `black`, from the tree as it will be committed, and replayed
    as recorded (`git apply --check`, apply, the named tests, `-R --check`, reverse, the clone
    clean). For (m4), name the after-`end` operations that fail.
18. **Line citations.** Take every citation in the log and on the board from `grep -n` on the files
    as committed, after `black`, and re-check them just before committing. Add a "Package lines
    (04, this commit)" sentence to each §3 entry whose cited `__init__.py`, `stores.py` or
    `__main__.py` lines 04 moves, and change nothing else in those entries. The entry 04 closes
    moves to §4 with a *Resolved* paragraph: what changed and the tests that pin it.
19. **`black`.** 33 files at `ab0cad9`, 35 after: the two new test modules.
20. **The records.** The board has an Orchestrator notes line, and the campaign README's row for 04
    a status column. The agent does not edit the notes line, the README's header paragraph, or any
    row but 04's; it sets 04's status to "landed, not yet reviewed" in the board's §1 row, the
    README's §2 row and `prompts/INDEX.md`, as 03 did. The board's §3 count line goes from seven to
    six; `docs/OPEN_ISSUES.md` from 12 to 11, counted by its rows; E1 ✅ "this commit".

**The facts, checked by the orchestrator on 2026-10-18 at `c3aa52a`.** Pass them on.
- **In-repository state.** `main` at `c3aa52a`, clean (`origin/main` at `4b55750`; `9e38581` and
  `c3aa52a` unpushed). `git status --short --ignored` shows `prompts/.DS_Store`,
  `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
  `var/` and `venv/`. `var/ledger.jsonl` (`471d0859…`) is an earlier review's, and is not touched.
  This checkout is the only worktree. `git diff --stat ab0cad9 HEAD -- runregistrykit pyproject.toml
  .github` is empty.
- **The suite.** `Ran 347 tests in 122.681s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad. No Ray process; `RAY_ADDRESS` unset.
  `black --check runregistrykit docs`: 33 files.
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0. `/opt/local/bin/python3.12` (3.12.15),
  `python3.13` (3.13.16), `python3.14` (3.14.8); `uv` at `/opt/local/bin/uv`. `getpass.getuser()`
  returns a name at all three; `os.waitid` is absent at 3.12.15 and present at 3.13 and 3.14.
- **The lines the prompt cites** were read at `c3aa52a` and are as it says. `__init__.py`:
  `__all__` `:80-102`, `TERMINAL_STATES` `:104`, `now_iso` `:118`, `git_provenance` `:145` (its
  `git_head` is `"unknown"` when git gives nothing), `read_json` `:237`, `_json_object` `:247`,
  `pid_alive` `:398`, `heartbeat_age` `:423`, `this_host` `:569`, `liveness` `:603` (its host rule
  `:633-640`), `Run` `:669`, `Run.status` `:730`, `Run._update` `:733`, `Run.finish` `:796` (check
  `:813`), `_fingerprint_results` `:833` (`taken_by=self` `:848`), `begin` `:976`, `list_runs`
  `:1137`; no `getpass` import yet. `stores.py`: the module docstring `:102-109`;
  `_running_runs_naming` `:1001` (filter `:1023`); `_describe_running` `:1028` (its foreign branch
  names `entry.get("host") or entry.get("host_id")`); `_unsure_remedy` `:1063-1071`;
  `_refuse_if_in_use` `:1074-1091`; fingerprint `:1391-1398`; retire `:1716-1725`; amend
  `:2071-2078`; `Run.finish` named at `:1070`, `:1078`, `:1086`, `:1395`, `:1720`, `:2075`, and
  `:52` (not a remedy). `__main__.py`: the docstring `:16-37`, `_host` `:78`, `main` `:419`, the
  client root `:536-547`, `list`'s stale line `:587-593`, 03's line `:595-603` (`Run.finish` at
  `:601`), the foreign line `:604-613`. Tests: `RegistryTestCase` `test_run_registry.py:116`
  (`begin` `:125`, `a_dead_pid` `:137`, `a_dead_run` `:147`); `test_host.py` `HERE` `:55`,
  `ELSEWHERE` `:56`, `a_status` `:78`, the `TERMINAL_STATES` loop `:517`;
  `test_unreadable_status.py` `FORMS` `:48`, `REMEDY` `:84`, `give_status_the_form` `:87`;
  `RetireTestCase` `test_store_retire.py:91` (`a_full_store` `:102`, `retire` `:134`);
  `a_running_run` and `a_stale_run` `store_fixtures.py:145`, `:148`; the nine assertions as §2.4's
  table gives them; the workflow's core line `.github/workflows/tests.yml:89`.
- **The issue index** counts 12. After 04: 11.

**What the review exists to establish.**
- **(K1) The files.** Only §0's list; the existing tests changed by §2.4's nine lines alone; the
  workflow by one line.
- **(K2) The record.** `end`'s status exactly §2.2's keys, and the status's other fields kept; the
  manifest, `checkpoint.jsonl`, a sidecar and the lifecycle's records unchanged in form; no stray
  file.
- **(K3) The check.** Every branch of §2.3 as written; a live pid here refused by every route.
- **(K4) The words.** The old texts with one substitution; the new sentences once, where they
  belong; `list`'s two lines.
- **(K5) Nothing else moved.** `Run.finish`'s code, `liveness`, the writer, `__all__`; every
  existing test.
- **(K6) The tests bite.** (m1)–(m7), and the orchestrator's.
- **(K7) The records**, with the issue closed and the zombie issue left open.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `var/`, `*.egg-info/`, `__pycache__/` and `.DS_Store`
  are ignored and must not be staged. Count, then paste. A log states only what the diff, the
  commands and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 2.
- **Mutation diffs.** As correction 17. None is committed. After each, `git status` here must be
  clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-04/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. **No scratch file goes under
  `runregistrykit/` or `docs/`.** The probe lives there and is not committed.
- **Signals.** The new tests send `SIGKILL` to a child they started, and nothing else, and reap it.
  The probe likewise. Nothing signals this shell, the agent's own process or any other.
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
2. **The prompt's gate**, and the suite: 347, one skip, in `venv/`, its time recorded.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 12 now, 11 after. Tell the agent.
5. **The probe.** Copy the planner's probe (the 04 planning session's `plan04/probe.py`) into the
   agent's `agent-04/probes/`, and keep a copy of your own. It takes a checkout's path as its first
   argument and prints the tree it ran. For §3.3 the agent adds, in its own copy, `end` on the
   killed child before the reap and after it; the planner's rows stay as they are.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and
  `CLAUDE.md`;
- `HEAD`, the suite count and time, and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad,
  and the probe's directory. The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and plainly: one commit at the
end; the files of §0 only; the core venv of correction 3 the only install; `TMPDIR` for every
command; no Ray; `SIGKILL` to its own children only; push nothing, tag nothing; stop and ask on the
prompt's §5.

## 3. The review — nine checks

1. **Scope (K1).** `git show --stat <commit>` touches only §0's list. `git diff <note's commit>
   <commit> -- pyproject.toml runregistrykit/client.py runregistrykit/fingerprint.py README.md
   PROVENANCE.md CLAUDE.md prompts/interrupted-runs/04-end-a-run.md
   prompts/interrupted-runs/orchestrator` is empty, and under `docs/` only the index moves. `git
   diff <note's commit> <commit> -- runregistrykit/tests` adds the two new modules and changes the
   nine lines of §2.4's table and nothing else; the workflow's diff is its core line; the campaign
   README's diff is 04's row. `__all__`, `Run.finish`'s code, `liveness`, `begin`, `list_runs` and
   the writer's section (`_status_temporary_name` through `_write_status`) are byte for byte as at
   `ab0cad9`, but for line numbers: compared by `git diff -U0` and by extracting each function's
   source with `inspect` at both trees.
2. **The suite (K5).** In `venv/` at the commit: `Ran 347 + N tests … OK (skipped=1)`, per module
   by the loader. `black --check runregistrykit docs`: 35 files. The core run of correction 3 in
   the orchestrator's own scratch venv, six modules, 98 + N₁; `test_end` at 3.13.16 and 3.14.8 by
   `PYTHONPATH`. `git status --short --ignored` and `var/ledger.jsonl` the same before and after;
   no Ray; no child left (the suite's children are reaped by the tests; `ps -o pid,ppid,stat,command`
   shows no `python` child of the runner after it).
3. **The writer (K5).** `git diff -U0 <note's commit> <commit> -- runregistrykit/__init__.py`
   shows nothing inside the writer's section. 02b's and 02c's sweeps pass, at 3.13.16 and 3.14.8 by
   `PYTHONPATH` as part of `test_status_writes`.
4. **The record (K2).** The orchestrator's `lifecycle.py` against `git archive ab0cad9` and `git
   archive <commit>`: identical shapes of `status.json`, the manifest, a ledger line, the sidecar
   and the run directory's files. And a scratch `end` at the commit: on a run with a full status
   (stage, units, a `fingerprint_error` field added by hand), every key it had kept with its value
   but `state`, `exit_code` and `heartbeat`; `ended`'s keys and `evidence`'s exactly §2.2's, with
   their types; the run directory's files the same set before and after; the manifest and
   `checkpoint.jsonl` byte-identical. On an unreadable status, the written status's keys exactly
   `ended`, `exit_code`, `heartbeat`, `state`.
5. **The probe and the check (K3).** The planner's probe from the orchestrator's own copy, against
   `ab0cad9` and the commit, each printing its tree: before, §"At writing"'s table; after, the six
   refusals naming the new words. Then the orchestrator's own `check.py` at the commit, a table of
   every branch of §2.3 (with and without `--unverified`): no run; empty reason; each terminal
   state; each of the thirteen forms, with a live pid, a dead pid and none; `running` on another
   host; on this host with an earlier boot, the pid live; on this host, live and dead pids; no
   `host`, live and dead pids; `host.id` null. Every live-pid row on this host refused by both
   forms; every other row as §2.3 says; every refusal leaving `status.json` and the manifest
   byte-identical. And the killed child, unreaped, refused with the zombie sentence; reaped,
   accepted.
6. **The words (K4).** For a refusal of alive and stale `running` runs here, each of the five texts
   equals the `ab0cad9` text with `Run.finish` → `` `python -m runregistrykit end RUN_ID --reason
   TEXT` ``, byte for byte (a scratch script raising each operation at both trees on the same
   store and runs, the run ids and paths normalised). A refusal with a foreign run carries the
   foreign sentence once; with two foreign runs, still once; with an unreadable run, 03's sentence
   with `--unverified`; with none of either, neither. `list`'s two lines as the log quotes them.
   `_END` is the only spelling of the command (`grep -n 'runregistrykit end'` in the three package
   files finds the constant and no other literal). `git grep -n 'signal' -- 'runregistrykit/*.py'
   ':!runregistrykit/tests'`: `finish`'s docstring only.
7. **The log (K7).** Every section of README §5.1 and the prompt's §4.4 additions; the deviations
   classified, corrections 1–20 among them; the suite before (347) and after; the core and 3.13
   runs; both probe tables; the record as written; every mutation as a diff; the refusal and `list`
   texts as shipped; line citations right at the commit by `grep -n`.
8. **The mutations (K6).** (m1)–(m7) extracted from the log by a script and replayed in a `git
   clone` of the commit, the two new modules and the module each names, in `venv/`'s Python with
   `PYTHONPATH` on the clone. Each fails as the log says. Then the orchestrator's own:
   - (o1) step 4's pid test removed, so a readable status that does not say, with a live pid here,
     is accepted with `--unverified`: a test must fail (correction 4's three forms);
   - (o2) step 6's earlier-boot branch removed, so the pid is always tested: the earlier-boot test
     must fail;
   - (o3) `evidence.host` computed as `this` whenever `host` is a dict: the no-`host` and
     `host.id`-null tests, or another-host, must fail;
   - (o4) `evidence.heartbeat` taken from the payload `_update` returns (the new stamp) instead
     of the status the check read: the hard-killed child's heartbeat assertion must fail;
   - (o5) the foreign sentence added once per foreign entry: the two-foreign-runs test, if any,
     must fail; if no test has two, record the gap;
   - (o6) `end` writing `exit_code` 137 instead of `null`: a test must fail.
9. **The records (K7).** The board: the header, 04's row ("this commit", 347 → 347 + N), E1, the
   issue moved from §3 to §4 with its *Resolved* paragraph, the §3 count line (six), the "Package
   lines (04, …)" sentences, `[04-a-killed-process-not-yet-reaped-answers-kill-0]` still in §3. The
   campaign README's 04 row. `docs/OPEN_ISSUES.md`: 11 by counting, the row deleted, the date.
   `prompts/INDEX.md`: the campaign's line. **CI is read after the push (§4)**: all three jobs
   green, the core job's count 98 + N₁ with `test_end` on its line, the skip count one in each.
   Until then the verdict says "pending CI".

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 04* paragraph (*At dispatch*,
  *The checks*, verdict), and add this note to the board's **Orchestrator notes** line, marked
  "used for 04". Fix small residue in a follow-up commit of its own: "this commit" → the SHA on the
  board, in the log, in the README's §2 row and in `prompts/INDEX.md`; "reviewed" for 04 in the
  board's header and row, the README's header paragraph and §2 status column, and
  `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Ask the user whether to push `main`.** The new core module first runs on Linux in CI. Once it
  has, read the result (check 9) and record it on the board in a records commit of its own.
- **Report to the user:** what landed, 347 → 347 + N, and the issue closed; the probe's table,
  before and after; the check's table; the mutations; CI, or that it is pending a push; that 05 is
  next, needs L9, and is written only after this review.
