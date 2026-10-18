# Orchestrator — prompt 05, begin refuses a second writer

Read [`../README.md`](../README.md) first: §0, §1, §5 (every rule; 6, 7, 8, 9 and 10
especially) and §6.2 (L4, L6, L8, and L9 with its 2026-10-18 note). The conventions are those of
[`prompt-04.md`](prompt-04.md), restated in §0 because the agent reads §0 and not this directory.
Where this note and the prompt differ, this note is right for 05.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names, at 3.12, 3.13 and 3.14;
- replay the log's mutation diffs with `git apply` in a scratch clone, and revert them;
- build venvs, client roots, stores and run directories of your own in the session scratchpad, and
  run the package and the planner's probe in them;
- start a child process in the scratchpad and send it `SIGKILL`, and no other process;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review. **Nothing is pushed** by the
agent, and nothing by the orchestrator without the user's clear yes (§4).

**The prompt:** [`05-begin-refuses-a-second-writer.md`](../05-begin-refuses-a-second-writer.md) ·
**Closes:** `[00-begin-does-not-refuse-a-second-writer]` and
`[04-a-pid-out-of-range-makes-pid-alive-raise]` · **Opens:** only what the work finds · **Not
touched:** `[04-a-killed-process-not-yet-reaped-answers-kill-0]` and the four other open §3
entries · **Model:** Sonnet, as the prompt recommends.

**Gate:**
- The prompt's gate: 04 landed and reviewed (`5e20772`, `46e29b9`, CI `39122974980` recorded in
  `d8f8de4`); **L9 taken 2026-10-18 as (a)**, and the pid issue assigned to 05 at the user's
  request (`f3cc239`); `git diff --stat 5e20772 HEAD -- runregistrykit pyproject.toml .github`
  empty; the suite 378 OK with one skip; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**A dozen lines of package code, called from the one place that makes a second writer, and six
existing tests whose setup must change while nothing they assert does.** The check is the store
operations' own; the risk is in where it sits (a refusal that leaves a directory, or that comes
before the tombstone's), in what it is handed (a store id dropped, a runs root other than the one
the run is created in), in words that drift from 04's helpers, and in a fixture that changes more
than the order runs are begun in. So the weight of the review is on:
- **the check refuses exactly what the store operations refuse**, for the root the run is created
  in, and **nothing is created by a refusal** (§3 checks 4, 5);
- **the tombstone is still refused first**, by its own words, and a `begin` with no `results`, or
  on a store whose runs are all terminal, is untouched (§3 check 5);
- **the six tests change their setup only**, through one fixture that moves directories and
  writes nothing, and no other existing test changes (§3 checks 1, 7);
- **`pid_alive` returns false for a pid out of range**, at both coercions, and is otherwise
  unchanged (§3 checks 5, 8);
- **nothing the registry writes moves**, and `stores.py`, `__main__.py`, `liveness`, `Run.finish`,
  the writer and `__all__` are byte for byte 04's (§3 checks 1, 3, 4).

**What moves on purpose:** `runregistrykit/__init__.py` (`pid_alive`: its two `except` clauses and
one docstring sentence; `begin`: the lazy import's names, the check and its refusal, one docstring
paragraph); `runregistrykit/tests/store_fixtures.py` (the fixture, in its runs section); the six
tests of the prompt's §2.4 table in `test_end_stores.py`, `test_store_fingerprint.py` and
`test_unreadable_status_stores.py`, by their `with` lines, the re-indented calls inside them, and
correction 6's two bindings; the two new modules `test_second_writer.py` and
`test_second_writer_stores.py`; the core line of `.github/workflows/tests.yml` (`:89`); the new log
`prompts/interrupted-runs/logs/05-begin-refuses-a-second-writer.md`; the board; the campaign
README's §2 row for 05 only; `docs/OPEN_ISSUES.md`; `prompts/INDEX.md`. **Nothing else**: not
`stores.py`, `__main__.py`, `client.py`, `fingerprint.py`, `pyproject.toml`, the repository
`README.md` (its usage is 06's), `PROVENANCE.md`, `CLAUDE.md`, `docs/` other than the index, any
existing test module or fixture beyond the lines named here (`test_run_registry.RegistryTestCase`,
`test_host.a_status`, `test_unreadable_status.FORMS`, `test_end.a_hard_killed_run` and
`test_store_retire.RetireTestCase` are imported, not edited), the prompt, any other part of the
campaign README, or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **L9 is (a)**, and the pid fix is the user's request (README §6.2, the board's decisions table
   and the issue's **Assigned** line, `f3cc239`). Nothing in the prompt is conditional on them.
2. **The suite's time.** The gate run is given below. Run the suite in the foreground with a Bash
   timeout of at least 600 000 ms, output to a file in your scratch, and grep the verdict from the
   file. A slow run is not a stop; a failing one is.
3. **The core run of §3.2** is 04's: `uv venv -p /opt/local/bin/python3.12 <scratch>/core`, then
   `uv pip install --offline -p <scratch>/core/bin/python -e <this checkout>`, `TMPDIR` in scratch,
   `datastorekit`, `ray` and `sqlalchemy` shown not findable, the **seven** core modules by name
   (the workflow's six and `test_second_writer`): 125 at `5e20772`, 125 + N₁ after. This is the
   one install allowed; nothing goes into `venv/` or MacPorts' Pythons. Remove the venv afterwards.
   Also run `test_second_writer` at `/opt/local/bin/python3.13` (3.13.16) with `PYTHONPATH` on the
   checkout and the standard library only. Never give MacPorts' Pythons `-m pip`.
4. **Where the check sits, exactly.** Inside `if results:`, after `results_store_id =
   reading.store_id` (`:1086`) and before the comment and `host = this_host()` (`:1087-1088`).
   `reading.store_id` is already `None` for a legacy sidecar, an absent one and one with problems
   (`SidecarReading.store_id`, `stores.py:307`), so it is passed as it is: that is the prompt's
   "matches by path alone". The runs root is `root or client.runs_root`, the expression `path` is
   built from at `:1071`; compute it once and use it for both if you like, but `path`'s value must
   not change. `os.path.isdir` guards the call (prompt §2.2), so `_running_runs_naming`'s own
   not-a-directory refusal is unreachable from `begin`; its `operation` argument is `"begin"`
   anyway. The refusal is raised before anything is created; nothing is excluded.
5. **The words** (prompt §2.3), composed as `_refuse_if_in_use` composes them (`stores.py:1093-
   1105`): `described`, `foreign`, `unsure` each computed once; the stale sentence with
   `` `{_END}` ``; then `{foreign + '. ' if foreign else ''}{unsure + '. ' if unsure else ''}`;
   then `No run directory was created`, with no full stop after it, as the tombstone refusal
   beside it ends. `_END` is already a name of this module (`:109`): use it, do not import it. The
   lazy import gains `_describe_running`, `_foreign_remedy`, `_running_runs_naming` and
   `_unsure_remedy`. The review composes the expected text from the helpers at the commit and
   compares byte for byte (§3 check 6), so a test that pins the full text for one alive and one
   stale run is welcome.
6. **The fixture, and the two unbound runs.** The fixture is a `contextlib.contextmanager` method
   of `StoreTestCase`, named `set_aside`, taking `Run`s. It makes a new directory under
   `self.top` (for example `tempfile.mkdtemp(dir=self.top, prefix="set-aside-")`), `os.rename`s
   each run's directory into it, yields, and in a `finally` renames each back to its own path and
   removes the now-empty directory. So `tree_state(self.top)` after the `with` is the tree before
   it plus what the body made, and nested use works. `os.rename` moves the directory itself:
   bytes, names and mtimes are kept, and nothing is copied. It fails loudly if a path to move back
   to exists. Its docstring says why it exists (prompt §2.4). One test of the fixture itself, in
   `test_second_writer_stores.py` (a body that raises; every file of the runs set aside
   byte-identical afterwards, and the top's tree as before), is in scope.
   - **Each `with` covers only the statement that begins a run** (the `begin`, `a_running_run` or
     `a_stale_run` call, and the assignment it is in), and sets aside **every** run under the root
     that has not finished and names that store at that moment. In
     `test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once` that is two `with`s:
     `stale` for `torn`'s `a_running_run`, then `stale` and `torn` for `unnamed`'s;
     `give_status_the_form` calls stay outside them, where they are.
   - **Two of the six do not bind the run they set aside**:
     `test_end_stores.TestTheWords.test_alive_and_stale_here_give_the_old_text_with_the_command`
     and `test_unreadable_status_stores.…test_a_refusal_for_running_runs_alone_has_no_new_sentence`
     each call `self.a_running_run("alive", primary)` as a bare statement. Bind it (`alive = …`);
     that line, in each, is the one change beyond the `with` lines, classified STRUCTURALLY
     REQUIRED. §3.5's `git diff -w` then shows the `with` lines, the fixture and those two
     bindings, and nothing else. This is not a stop.
7. **`begin`'s `root`.** `RegistryTestCase.begin` passes `root=self.root` itself, so a test that
   begins under another runs root (prompt §2.7: "a runs root that does not exist yet", "the runs
   root it reads") calls `runregistrykit.begin` directly, with the keywords `RegistryTestCase.begin`
   gives (`campaign`, `prompt`, `slug`, `purpose`, `argv`, `client_root=self.client`) and its own
   `root=`, or through a small helper of the new module's own. `RegistryTestCase` is not edited.
8. **The core module's stores.** In `RegistryTestCase` the runs root is the temporary directory
   itself, and `a_pipeline_run` writes `results.sqlite` **in the runs root**. That is fine for the
   check (`list_runs` lists directories), but the "runs root's listing unchanged" comparison is
   then `set(os.listdir(self.root))` before and after the refused `begin`, and a second store for
   "another store" rows is a plain file of the module's own beside it, with no sidecar. A store a
   test needs elsewhere goes under a subdirectory of `self.root`.
9. **An earlier boot, another host, and the platform.** The earlier-boot refusal needs
   `this_host()`'s `id` and `boot` not `None`, and skips with a reason where either is (04's rule).
   macOS here has both, so no new skip runs here, and the suite stays at one skip. Record that the
   review reads the skip count in CI.
10. **`pid_alive`.** `except (TypeError, ValueError, OverflowError)` at `int()`, and `except
    OverflowError: return False` at `os.kill`, beside the existing clauses (it is not an
    `OSError`). Nothing broader: not `except Exception`. The docstring's sentence says a pid
    outside the platform's range names no process. Measured here on 2026-10-18 at the venv's
    3.12.15: `os.kill` raises `OverflowError` for `2**31` ("signed integer is greater than
    maximum"), `2**63` and `10**30` ("Python int too large to convert to C long"); `int(inf)`
    raises `OverflowError`; `int(nan)` raises `ValueError`, already caught. Your (m8) may be
    `int()`'s `OverflowError` left uncaught; if it is not, the review makes it (§3 check 8, (o1)).
11. **Through the readers** (prompt §2.7's `pid_alive` bullet). The `list` run is
    `python -m runregistrykit list`, run as `test_end.py`'s command-line tests run it (its client
    root and `--root`), `sys.executable`, the checkout first on the child's path; exit 0 and the
    run's line marked `!!`. `_end_run` on the `2**31` run: accepted, `ended.verified` true,
    `evidence.pid_answers` false. For the JSON `Infinity` form, write the status's bytes by hand
    (`json.dumps` with the default `allow_nan`, or the text `Infinity`), and assert that
    `read_json` gives `float("inf")` before relying on it. What `_end_run` then writes back for
    `evidence.pid` is 04's, and not this prompt's to change; record it in the log.
12. **The stores module's base.** On `test_store_retire.RetireTestCase`, or on
    `test_end_stores.EndStoresTestCase` (a `RetireTestCase`) to reuse its `refusals` helper for
    "one rule". **Import the module, not the class** (`from runregistrykit.tests import
    test_end_stores`), so the loader runs no test twice; the per-module counts show it.
13. **The acceptance test's order** (`test_second_writer_stores`). `test_end.a_hard_killed_run(self,
    self.root, self.client, results=str(primary))` returns once the child is killed and reaped (−9).
    Then: `before = self.state()`; the second `begin`, refused, naming the killed run's id and
    `runregistrykit end RUN_ID`; `self.state() == before`; `end` by the command, as
    `test_end_stores.TestEndingAHardKilledRun` runs it; `begin` again, accepted; its
    `finish("done", exit_code=0, fingerprint=True)`: a `fingerprint`, no `fingerprint_error`. No
    zombie is built (04's correction 11), and nothing is signalled but the helper's child.
14. **Observations, not fixes.** Record in the log, and open a §3 issue only where measured, with
    the board's and the index's counts adjusted:
    - the race: two `begin`s at the same moment both pass (the docstring says so; not a lock);
    - a run under another runs root is not seen (stated, pinned);
    - the cost of the check, re-measured by the planner's `cost.py` (optional);
    - anything found in `liveness`, `list_runs`, `store show`, `end` or the store operations,
      which this prompt does not change.
15. **Mutation diffs** are taken after `black`, from the tree as it will be committed, and replayed
    as recorded (`git apply --check`, apply, the named tests, `-R --check`, reverse, the clone
    clean). For (m3), name the test that sees the directory left; for (m5), the test of the runs
    root that does not exist.
16. **Line citations.** Take every citation in the log and on the board from `grep -n` on the files
    as committed, after `black`, and re-check them just before committing. Add a "Package lines
    (05, this commit)" sentence to each §3 entry whose cited `__init__.py` lines 05 moves (every
    line after `pid_alive`'s clauses moves), and change nothing else in those entries. The two
    entries 05 closes move to §4, each with a *Resolved* paragraph: what changed and the tests
    that pin it.
17. **`black`.** 35 files at `5e20772`, 37 after: the two new test modules.
18. **The records.** The board has an Orchestrator notes line, and the campaign README's row for 05
    a status column. The agent does not edit the notes line, the README's header paragraph, or any
    row but 05's; it sets 05's status to "landed, not yet reviewed" in the board's §1 row (378 →
    378 + N), the README's §2 row and `prompts/INDEX.md`, as 04 did. B1 ✅ "this commit". The
    board's §3 count line goes from seven to five, its sentence about the owners corrected to the
    five that remain; `docs/OPEN_ISSUES.md` from 12 to 10, counted by its rows, §1.3's count from
    7 to 5, the date.

**The facts, checked by the orchestrator on 2026-10-18 at `f3cc239`.** Pass them on.
- **In-repository state.** `main` at `f3cc239`, clean (`origin/main` at `46e29b9`; `d8f8de4` and
  `f3cc239` unpushed, and this note's commit after them). `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/`, `var/` and `venv/`. `var/ledger.jsonl` (`93589747…`) is an
  earlier review's, and is not touched. This checkout is the only worktree. `git diff --stat
  5e20772 HEAD -- runregistrykit pyproject.toml .github` is empty.
- **The suite.** `Ran 378 tests in 139.779s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad;
  `git status --short --ignored` and the ledger the same after it. No Ray process; `RAY_ADDRESS`
  unset. `black --check runregistrykit docs`: 35 files. By the loader: `test_run_registry` 29,
  `test_public_names` 8, `test_host` 28, `test_status_writes` 22, `test_unreadable_status` 11,
  `test_end` 27 (the core's 125).
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` 0.4.0.
  `/opt/local/bin/python3.12` (3.12.15), `python3.13` (3.13.16), `python3.14` (3.14.8); `uv` at
  `/opt/local/bin/uv`.
- **The lines the prompt cites** were read at `f3cc239` and are as it says. `__init__.py`:
  `__all__` `:81`, `TERMINAL_STATES` `:105`, `_END` `:109`, `_repo_path` `:229`, `_resolve`
  `:238`, `pid_alive` `:403` (`int()` `:412-413`, `os.kill` `:418`, `except OSError` `:423`),
  `liveness` `:608`, `begin` `:983` (client located `:1068-1069`, `path` `:1071`, the tombstone
  block `:1074-1086`, the lazy import `:1077`, `this_host()` `:1088`, `os.makedirs` `:1089`, the
  manifest's `results` through `_repo_path` `:1109`), `list_runs` `:1144`, `_end_run` `:1219`.
  `stores.py`: the module docstring's check `:104-109`, `SidecarReading.store_id` `:307`,
  `read_sidecar` `:691` (it reads `os.path.abspath(primary)`), `runs_naming` `:961` (a relative
  manifest `results` resolved against the client root, as `_repo_path` records it, so begin's
  `os.path.abspath(results)` matches it), `_running_runs_naming` `:1002`, `_describe_running`
  `:1029`, `_unsure_remedy` `:1064`, `_foreign_remedy` `:1075`, `_refuse_if_in_use` `:1087`.
  Tests: `RegistryTestCase` `test_run_registry.py:116` (`begin` `:125`, `a_dead_pid` `:137`,
  `a_dead_run` `:147`, `a_pipeline_run` `:505`); `StoreTestCase` `store_fixtures.py:115` (its runs
  section `:143-153`: `a_running_run` `:145`, `a_stale_run` `:148`); `test_host.a_status` `:78`,
  `another_id` `:94`; `test_unreadable_status.FORMS` `:48`, `REMEDY` `:84`,
  `give_status_the_form` `:90`; `RetireTestCase` `test_store_retire.py:91` (`a_full_store` `:102`,
  which fingerprints with `runs_root=self.root`); `test_end.a_hard_killed_run` `:123`;
  `test_end_stores.EndStoresTestCase` `:53` (`refusals` `:77`); the workflow's core line
  `.github/workflows/tests.yml:89`. `git grep -n 'signal' -- 'runregistrykit/*.py'
  ':!runregistrykit/tests'` finds `__init__.py:814`, `finish`'s docstring, alone.
- **The planner's probe at `5e20772`** (by `git archive`, in the orchestrator's scratch): every row
  `BEGUN`, as the prompt's "Today" column.
- **The issue index** counts 12. After 05: 10.

**What the review exists to establish.**
- **(K1) The files.** Only §0's list; the six tests changed by their `with` lines, the re-indented
  calls and correction 6's two bindings alone; the workflow by one line.
- **(K2) The record.** Nothing the registry writes changes: the lifecycle's records identical in
  shape; a refusal writes nothing.
- **(K3) The check.** Every row of the prompt's §2.7 as written: refused with no directory, or
  accepted; the tombstone first; the runs root this run is created in, and only it.
- **(K4) The words.** §2.3's text, composed from 04's helpers, byte for byte; each optional
  sentence once, where it belongs; `_END` the only spelling.
- **(K5) Nothing else moved.** `stores.py`, `__main__.py`, `Run.finish`, `liveness`, `list_runs`,
  `_end_run`, the writer, `__all__`; `begin` outside the check; `pid_alive` outside its clauses;
  every existing test.
- **(K6) The tests bite.** (m1)–(m8), and the orchestrator's.
- **(K7) The records**, with both issues closed and the zombie issue left open.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `var/`, `*.egg-info/`, `__pycache__/` and `.DS_Store`
  are ignored and must not be staged. Count, then paste. A log states only what the diff, the
  commands and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 2.
- **Mutation diffs.** As correction 15. None is committed. After each, `git status` here must be
  clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-05/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. **No scratch file goes under
  `runregistrykit/` or `docs/`.** The probe lives there and is not committed.
- **Signals.** The new tests send `SIGKILL` to a child they started, and nothing else, and reap it
  (through `test_end.a_hard_killed_run`). Nothing signals this shell, the agent's own process or
  any other.
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
2. **The prompt's gate**, and the suite: 378, one skip, in `venv/`, its time recorded.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 12 now, 10 after. Tell the agent.
5. **The probe.** Copy the planner's probe and cost script (the 05 planning session's
   `plan05/probe.py` and `cost.py`) into the agent's `agent-05/probes/`, and keep a copy of your
   own. The probe takes a checkout's path as its first argument and prints the tree it ran. Its
   rows stay as they are; the agent may add rows of its own in its copy, marked as its own.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Sonnet**, in this checkout. Give it:
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
   <commit> -- runregistrykit/stores.py runregistrykit/__main__.py runregistrykit/client.py
   runregistrykit/fingerprint.py pyproject.toml README.md PROVENANCE.md CLAUDE.md
   prompts/interrupted-runs/05-begin-refuses-a-second-writer.md prompts/interrupted-runs/orchestrator`
   is empty, and under `docs/` only the index moves. `git diff -w 5e20772 <commit> --
   runregistrykit/tests` adds the two new modules and shows, in the three existing modules, the
   `with` lines and correction 6's two bindings, and in `store_fixtures.py` the fixture, and
   nothing else; without `-w`, the re-indented calls besides. The workflow's diff is its core line;
   the campaign README's diff is 05's row. `git diff -U0 5e20772 <commit> --
   runregistrykit/__init__.py` shows hunks only inside `pid_alive` and `begin`; and `__all__`,
   `Run.finish`, `liveness`, `list_runs`, `_end_run` and the writer's section
   (`_status_temporary_name` through `_write_status`) are byte for byte as at `5e20772`, by
   extracting each function's source with `inspect` at both trees.
2. **The suite (K5).** In `venv/` at the commit: `Ran 378 + N tests … OK (skipped=1)`, per module
   by the loader, the six existing core modules at their counts above and no module's count
   lowered. `black --check runregistrykit docs`: 37 files. The core run of correction 3 in the
   orchestrator's own scratch venv, seven modules, 125 + N₁; `test_second_writer` at 3.13.16 and
   3.14.8 by `PYTHONPATH`. `git status --short --ignored` and `var/ledger.jsonl` the same before
   and after; no Ray; no child left (`ps -o pid,ppid,stat,command` shows no `python` child of the
   runner after it).
3. **The writer and the six (K5).** Each of the six tests, run at the commit with its `with`
   removed (by a scratch patch in a clone), errors at its `begin` with the new refusal; with it,
   passes. The fixture: a scratch test that sets aside two runs, raises in the body, and compares
   every file's bytes and mtime, and `tree_state(self.top)`, before and after. 02b's and 02c's
   sweeps pass, at 3.13.16 and 3.14.8 by `PYTHONPATH` as part of `test_status_writes`.
4. **The record (K2).** The orchestrator's `lifecycle.py` against `git archive 5e20772` and `git
   archive <commit>`: identical shapes of `status.json`, the manifest, a ledger line, the sidecar
   and the run directory's files. A refused `begin` leaves `tree_state` of the temporary top
   unchanged, the runs root's listing included, on every row of check 5.
5. **The probe and the check (K3).** The planner's probe from the orchestrator's own copy, against
   `5e20772` and the commit, each printing its tree: before, every row `BEGUN`; after, the
   candidate's column, but the two `2**31` rows: refused as stale on its store, `BEGUN` on another.
   Then the orchestrator's own `check.py` at the commit, a table of every row of the prompt's §2.7
   (alive here; stale; earlier boot; foreign; each of the thirteen forms; `v0.1.0` form, live and
   dead pid; all four terminal states; no run; no `results`; the runs root absent, and created;
   another runs root; the tombstone with a stale run, refused by the tombstone's words; a legacy
   sidecar, matched by path alone; a store id alone; a pid of `2**31` and of `Infinity`, on its
   store and on another), each refusal compared with what `_refuse_if_in_use` refuses for a copy
   of the same store and runs: the same runs, by id, in both. And the remedy: the hard-killed
   child's store refused, `end`, accepted.
6. **The words (K4).** For each refusal of check 5, the message equals §2.3's text composed at the
   commit from `_describe_running`, `_foreign_remedy` and `_unsure_remedy` on
   `_running_runs_naming`'s list, byte for byte. With two foreign runs, the foreign sentence once;
   with two unreadable runs, 03's sentence once; with an alive and a stale run here, neither.
   `grep -n 'runregistrykit end'` in the three package files finds the constant and no other
   literal; `git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'`: `finish`'s
   docstring only. `begin`'s docstring paragraph says the five things §2.2 lists.
7. **The log (K7).** Every section of README §5.1 and the prompt's §4.4 additions; the deviations
   classified, corrections 1–18 among them, correction 6's bindings STRUCTURALLY REQUIRED; the
   suite before (378) and after; the core and 3.13 runs; both probe tables; the record as written;
   §3.5's diff; every mutation as a diff; the refusal text as shipped; line citations right at the
   commit by `grep -n`.
8. **The mutations (K6).** (m1)–(m8) extracted from the log by a script and replayed in a `git
   clone` of the commit, the two new modules and the module each names, in `venv/`'s Python with
   `PYTHONPATH` on the clone. Each fails as the log says. Then the orchestrator's own:
   - (o1) `int()`'s `OverflowError` not caught (only `os.kill`'s): the `Infinity` tests must fail;
   - (o2) the check before the tombstone's: the order test must fail;
   - (o3) the check made against `client.runs_root` always, not `root or client.runs_root`: the
     tests that begin under a `root=` of their own must fail;
   - (o4) the foreign sentence and 03's swapped in order: a test pinning both, or the full text,
     must fail; if none pins both, record the gap;
   - (o5) the fixture copying (`shutil.copytree`, then `rmtree`) instead of renaming, without
     restoring mtimes: the fixture's own test must fail, or record that it compares bytes only;
   - (o6) the fixture not moving the runs back when the body raises (no `finally`): the fixture's
     own test must fail.
9. **The records (K7).** The board: the header, 05's row ("this commit", 378 → 378 + N), B1, both
   issues moved from §3 to §4 with their *Resolved* paragraphs, the §3 count line (five), the
   "Package lines (05, …)" sentences, `[04-a-killed-process-not-yet-reaped-answers-kill-0]` still
   in §3. The campaign README's 05 row. `docs/OPEN_ISSUES.md`: 10 by counting, §1.3 at 5, the two
   rows deleted, the date. `prompts/INDEX.md`: the campaign's line. **CI is read after the push
   (§4)**: all three jobs green, the core job's count 125 + N₁ with `test_second_writer` on its
   line, the skip count one in each. Until then the verdict says "pending CI".

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 05* paragraph (*At dispatch*,
  *The checks*, verdict), and add this note to the board's **Orchestrator notes** line, marked
  "used for 05". Fix small residue in a follow-up commit of its own: "this commit" → the SHA on the
  board, in the log, in the README's §2 row and in `prompts/INDEX.md`; "reviewed" for 05 in the
  board's header and row, the README's header paragraph and §2 status column, and
  `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Ask the user whether to push `main`.** The new core module first runs on Linux in CI. Once it
  has, read the result (check 9) and record it on the board in a records commit of its own.
- **Report to the user:** what landed, 378 → 378 + N, and the two issues closed; the probe's
  table, before and after; the check's table; the mutations; CI, or that it is pending a push; that
  06, the release, is next, needs L10, and is written only after this review.
