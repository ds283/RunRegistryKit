# Log — prompt 02: status writes

**Subject:** Write status.json through a name of its own, and discard a superseded write
**Commit:** `2bf9c72` (on `main`, after `b52cc01`)
**Date:** 2026-10-17
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1–11)
**Result:** **landed.**
- `status.json`, and only `status.json`, is written by a private writer that `Run._update` alone
  calls. Each write has a temporary name of its own, `status.json.<pid>-<counter>-<8 hex>.tmp`,
  created with `os.open(…, 0o666)` so that the umask applies as it did to `open(path, "w")`.
- The writes to one `status.json` in this process, through any `Run` object for it, are ordered by
  a sequence number, keyed by the file's real path, under a re-entrant lock. A write overtaken by a
  later one is discarded or, if the later one landed between its check and its replace, puts the
  later payload back. A write composes over the fields of every earlier write still in flight, so a
  discarded heartbeat's `units_done` and `stage` are kept.
- `write_json_atomic` is unchanged, and so is every sidecar write and `stores.py`.
- The suite is **307 → 322**: 15 new tests in `test_status_writes`, core only. Every module that
  existed has the count it had, and no existing test changed.
- The core alone, in a scratch venv without `[stores]`, runs 80 tests (65 + 15), OK, with one skip.
- The planner's probe, written again and run against this tree with a real `SIGTERM`: all six cases
  parse with `killed`, 143 and `units_done` 7.
- Each of (m1)–(m10) fails at least one test. No stop condition fired.
- `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` is closed, and nothing
  is opened, so `docs/OPEN_ISSUES.md` counts **8**.
- **Nothing pushed, no tag made, no workflow dispatched.** The new module first runs on Linux in
  CI (below).

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | `import copy`, `import itertools`, `import threading`; a section after `write_json_atomic` holding the writer: `_STATUS_LOCK` (`:265`, a `threading.RLock`), `_STATUS_WRITES` (`:270`), `_STATUS_NAMES` (`:273`), `_status_temporary_name` (`:276`), `_remove_quietly` (`:284`), `_land_status` (`:291`, steps 3–5) and `_write_status` (`:324`, steps 1, 2 and 6); `Run._update` (`:691-723`) given a docstring and made a call of `_write_status` |
| `runregistrykit/tests/test_status_writes.py` | new, core only: 15 tests in seven classes |
| `.github/workflows/tests.yml` | the core job's test line (`:89`) names `runregistrykit.tests.test_status_writes` too; nothing else |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: `stores.py`, `__main__.py`, `client.py`, `fingerprint.py`, `pyproject.toml`,
`README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption/`, any other test module or fixture, the
prompt, the campaign README, `orchestrator/`. No client, DatastoreKit or RayPoolKit file.
`write_json_atomic` (`:247-256`) is byte for byte as it was, its `<path>.tmp` at `:250` and its
`os.replace` at `:256`, and it is still in `__all__` (`:101`). `__all__` is otherwise unchanged:
every new name is private.

### The writer

`Run._update(**fields)` returns `_write_status(self.status_path, fields)`. Under `_STATUS_LOCK`
(`:327`), `_write_status`:

1. takes the book for `os.path.realpath(path)` (`:329`), `{"next", "in_flight", "landed",
   "payload"}`, made on first use with `landed` −1; takes the next number; and, as the first
   statement of its `try`, holds a copy of `fields` as in flight under it (`:335`);
2. composes: the base is the file (`read_json(path) or {}`, the read `Run.status()` makes, `:341`),
   unless an earlier write is in flight and a payload has landed, when it is a deep copy of the
   landed payload (`:337`); then the in-flight fields of every earlier number, in order; then its
   own fields; then `heartbeat = now_iso()`;
3. calls `_land_status(path, book, number, status)`, and returns `status`;
4. in its `finally`, removes its own in-flight entry (`:349`).

`_land_status(path, book, number, payload)`:

- names the file `_status_temporary_name(path)`, `f"{path}.{os.getpid()}-{next(_STATUS_NAMES)}-{os.urandom(4).hex()}.tmp"`;
- creates it with `os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)` (`:305`) and writes
  it as `write_json_atomic` writes (`json.dump(…, indent=2, sort_keys=True)`, a newline, `flush`,
  `fsync`), `json.dump` and `os.replace` looked up through their modules at call time;
- if `book["landed"] > number` (`:311`), removes the file and returns: discarded;
- else `os.replace(name, path)` (`:314`);
- on any `BaseException` before that point, removes the file (best-effort) and re-raises;
- after the replace, if `book["landed"] > number` (`:318`), puts back the landed payload by calling
  itself with the landed number (`:319`), which is checked in the same way; else records
  `landed = number` and a deep copy of the payload (`:321`).

A plain write, with nothing in flight, reads the file once, writes once and calls `os.replace` once,
and writes the keys it wrote before. `begin`'s first status (`:1063-1070`) goes through `_update`
(correction 3), so nothing in the package writes `status.json.tmp` any more.

`_update`'s docstring says what is not covered: a handler that re-enters between a write taking
its number and holding its fields loses those fields, never the terminal state; writes from two
processes at once are not ordered; and a process that dies between creating its temporary file and
replacing it leaves a `status.json.<unique>.tmp`, which nothing reads, which `list` and the store
operations do not look at, and which nothing removes.

### The tests

`runregistrykit/tests/test_status_writes.py`, with the licence header and a docstring of its own.
It imports `runregistrykit`, `test_run_registry` (for `RegistryTestCase`, as `test_host` does) and
`client_fixtures`; nothing of the store layer.

| Class | Tests | What |
|---|---:|---|
| `TestAHandlerInsideAHeartbeat` | 1 (8 subtests) | the reproduction: `heartbeat(units_done=7, stage=…)` whose write calls `run.finish("killed", exit_code=143)` once, at each of the four points, the handler raising `SystemExit(143)` and returning. Each case: parses, `killed`, 143, `units_done` 7, the stage, `pid` and `host` as `begin` wrote them, no `.tmp` left, the heartbeat raised `SystemExit(143)` or returned. At the two points inside `json.dump`, exactly one `os.replace` onto `status.json` (the handler's) |
| `TestASecondRunObject` | 3 | the same, the handler calling `runregistrykit.Run(run.path).finish(…)`, returning: half written; before the replace; and half written through a symlinked spelling of the runs root |
| `TestAHandlerDuringThePutBack` | 1 | before the replace, returning; the put-back's own `os.replace` makes a second re-entry, `run.heartbeat(stage="from the second handler")`, while the file holds the heartbeat's `running` (asserted) |
| `TestARealSignal` | 3 | a child that begins a run, installs a `SIGTERM` handler calling `finish("killed", exit_code=143)` and sends itself `SIGTERM` from inside a heartbeat's `json.dump`, half written; the handler raises (exit 143), returns (exit 0, no `FileNotFoundError` in stderr) or ends the process (`SIG_DFL`, `os.kill`; exit −15, at most one `status.json.<unique>.tmp`, the documented leftover). Each child under `subprocess.run(…, timeout=60)` |
| `TestTwoThreads` | 1 | a thread making 300 heartbeats while the main thread calls `finish`; joined with a 60 s timeout in a `finally` |
| `TestThePlainWrite` | 5 | the name; the mode under umask `0o022` and `0o077`; a failed write (a `stage` that is not JSON-serialisable); one read and one replace with nothing in flight, the keys unchanged through `finish`; `write_json_atomic` replacing from exactly `<path>.tmp` |
| `TestAnOldRecord` | 1 | a `v0.1.0`-form status (no `host`) through `heartbeat`, `heartbeat(pid=<dead>)` and `finish`: keys kept, no `host` added, judged `alive`, `stale`, `finished` |

## Deviations from the prompt

Each classified. Corrections 1–11 are section 0's.

1. **The suite's time** (correction 1). Every run was in the foreground with a 600 s timeout, its
   output written to a file and the verdict grepped from it: 98.327 s before, 104.281 s after, and
   94–105 s for each mutation run (below). **STRUCTURALLY REQUIRED.**
2. **The core run** (correction 2): `uv venv -p /opt/local/bin/python3.12` and `uv pip install
   --offline -e` of this checkout, in `agent-02/core`, `TMPDIR` in the scratchpad; removed
   afterwards. 65 + 15 = 80 tests. **STRUCTURALLY REQUIRED.**
3. **`begin`'s first status goes through the new writer** (correction 3). `_update` is the only
   caller of `_write_status`, and every write of `status.json` comes through `_update`, so "only
   `status.json`" and "used by `Run._update` and by nothing else" are one rule. **STRUCTURALLY
   REQUIRED.**
4. **The children** (correction 4) are a script written into the test's temporary directory that
   puts `PACKAGE_PARENT` first on `sys.path`, as `CHECKER` and `CRASHER` do, run with the test's
   client root as working directory and its runs root as `root`. Each runs under
   `subprocess.run(…, timeout=60)`. **STRUCTURALLY REQUIRED.** The `TimeoutExpired` is caught and
   turned into `self.fail`, with a message saying the handler waited on the write it interrupted:
   **IMPLEMENTATION CHOICE**.
5. **Patching** (correction 5). The writer calls `json.dump` and `os.replace` through their
   modules, so `mock.patch("json.dump", new=…)` and `mock.patch("os.replace", new=…)` reach it.
   The tests' patches fire once, for the interrupted write, and pass every other call to the real
   function. **STRUCTURALLY REQUIRED.**
6. **Step 2 as the prompt writes it** (correction 6), not refined. The case the orchestrator names
   was measured in scratch and is in "Observations not acted on" with a variant; no issue is
   opened for it. **STRUCTURALLY REQUIRED.**
7. **(m9)** (correction 7) was run on the three real-signal child tests alone, by name, each child
   under its timeout; never the module or the suite. **STRUCTURALLY REQUIRED.**
8. **`black --check runregistrykit docs`**: 31 files (correction 8). **STRUCTURALLY REQUIRED.**
9. **Line citations** (correction 9) in this log and on the board were taken with `grep -n` from
   the files as committed, after `black`, and re-checked just before committing. **STRUCTURALLY
   REQUIRED.**
10. **Mutation diffs** (correction 10) were generated after `black`, from a scratch clone holding
    `2bf9c72`'s tree (the blob of `runregistrykit/__init__.py` is `700e04c` in both). **STRUCTURALLY
    REQUIRED.**
11. **The board's Orchestrator notes line** (correction 11) is not edited. **STRUCTURALLY
    REQUIRED.**
12. **No "signal" in the package's new text.** §3.3's `git grep -n 'signal'` must still find only
    `finish`'s docstring (now `:755`), so the writer's comments and `_update`'s docstring say
    "handler" and "interrupt". The test module uses the word freely. **STRUCTURALLY REQUIRED.**
13. **The writer's shape.** Two module-level functions, `_write_status` (steps 1, 2, 6) and
    `_land_status` (steps 3–5, the put-back by recursion), two helpers and three module-level names,
    all private. The base read is `read_json(path) or {}`, the read `Run.status()` makes, not a call
    of `self.status()`, since the writer is not a method. **IMPLEMENTATION CHOICE.**
14. **The name**: the pid, a per-process `itertools.count()` and `os.urandom(4).hex()`.
    **IMPLEMENTATION CHOICE.**
15. **The in-flight entry is registered as the first statement of the `try`** whose `finally`
    removes it, so a handler that raises between a write taking its number and that statement
    leaves no entry behind. Its fields are then lost, which is the documented window.
    **IMPLEMENTATION CHOICE.**
16. **The temporary file is removed on any exception without a "created" flag.** The name is the
    write's own, so removing it cannot touch another write's file, and a flag would leave a window
    between `os.open` returning and the flag being set. **IMPLEMENTATION CHOICE.**
17. **The put-back cannot tell "between the check and the replace" from "after the replace".** A
    handler that writes after the heartbeat's `os.replace` has returned (the fourth point) also
    leaves `landed > number` when the heartbeat looks, so the heartbeat puts back a payload the file
    already holds. Measured in scratch: three replaces onto `status.json` at the fourth point,
    returning, and the file `killed`, 143, `units_done` 7. Harmless, and only under re-entrance.
    **STRUCTURALLY REQUIRED.**
18. **The landed payload is kept as a deep copy, and a re-entered base is a deep copy of it**, so
    that a caller mutating the dict `heartbeat` or `finish` returned cannot change the
    bookkeeping. Hence `import copy`; `itertools` is for the counter. **IMPLEMENTATION CHOICE.**
19. **Tests beyond §2.6's list**, each an **IMPLEMENTATION CHOICE**:
    - the second `Run` through a symlinked spelling of the runs root, which pins the real-path key;
    - at the two points inside `json.dump`, exactly one replace onto `status.json`. Without step 4
      the put-back restores `killed` in the end, so the final file alone cannot tell (m2) apart;
      the count can, and a concurrent reader would otherwise see `running` between the two;
    - the put-back test asserts that the file holds `running` when the second handler composes;
    - the real-signal children also assert `units_done` 7 and their exit codes (143, 0, −15);
    - the old record is also judged `stale` after `heartbeat(pid=<a reaped pid>)`;
    - the plain write's keys are checked through a `finish` too.
20. **No assertion message prints the status's `host`**, whose `boot` is read from the machine, as
    01's deviation 16 did for the identity: messages show the status without `host`, and the host
    is compared with `assertTrue(a == b, message)`. **IMPLEMENTATION CHOICE.**
21. **The threads test joins its thread in a `finally`.** A first draft did not, and against the
    old writer (below) its `finish` raised and the thread went on writing while the test's
    temporary directory was removed. **IMPLEMENTATION CHOICE.**
22. **"Half the payload"** is half of `json.dumps(obj, indent=2, sort_keys=True)`, written to the
    handle (its buffer) before the handler runs, as the planner's probe did. **IMPLEMENTATION
    CHOICE.**
23. **Extra measurements**, for the record: the new module and the probe were also run against
    `b52cc01`'s writer, in the scratch clone (below). **IMPLEMENTATION CHOICE.**
24. **The mutations' forms.** (m3) removes the put-back's call and keeps its `return`, so that step
    6 does not then lower the recorded number; (m5) replaces the base's `if`/`else` with the file's
    read; (m6) passes the `Run` object to the writer as its key; (m8) uses `tempfile.mkstemp` with
    the prefix `status.json.` and the suffix `.tmp`; (m10) gives `write_json_atomic` a pid-named
    temporary file, the brief's original proposal. (m1)–(m8) and (m10) were each run on the whole
    suite. **IMPLEMENTATION CHOICE.**

## Verification performed

### 1. The state at the start

`HEAD` `b52cc01`, `main`, clean; `git worktree list` shows this checkout alone; `git diff --stat
387c58f HEAD -- runregistrykit pyproject.toml .github` empty. `RAY_ADDRESS` unset. `venv/`: Python
3.12.15, black 25.1.0. `git status --short --ignored`: `prompts/.DS_Store`,
`runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
`venv/`. `git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'`:
`runregistrykit/__init__.py:632` only.

### 2. The suite, before and after

`TMPDIR=<agent-02>/tmp ./venv/bin/python -m unittest discover -s runregistrykit/tests -t . -v`, from
the root, in the foreground. `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` found nothing
(exit 1) before and after each run. Per module, by `unittest.defaultTestLoader.discover`:

| Module | Before | After |
|---|---:|---:|
| `test_client_root` | 27 | 27 |
| `test_fingerprinter` | 31 | 31 |
| `test_host` | 28 | 28 |
| `test_host_stores` | 3 | 3 |
| `test_package_imports` | 3 | 3 |
| `test_package_is_generic` | 22 | 22 |
| `test_public_names` | 8 | 8 |
| `test_run_registry` | 29 | 29 |
| `test_status_writes` | — | **15** |
| `test_store_amend` | 21 | 21 |
| `test_store_amend_residuals` | 9 | 9 |
| `test_store_command_line` | 2 | 2 |
| `test_store_copy_move` | 27 | 27 |
| `test_store_fingerprint` | 29 | 29 |
| `test_store_retire` | 41 | 41 |
| `test_store_retire_references` | 10 | 10 |
| `test_store_sidecar` | 17 | 17 |
| **total** | **307**, `Ran 307 tests in 98.327s`, `OK (skipped=1)` | **322**, `Ran 322 tests in 104.281s`, `OK (skipped=1)` |

N = 15. The skip is `test_host`'s Linux readers, as before. No test that existed at `b52cc01` was
changed (`git diff --stat` touches no existing test module); `TestStatus`'s replace test and
torn-read test pass unchanged. `git status --short --ignored` after the suite was the same as before
it, `__pycache__/` included.

### 3. The core alone

In `agent-02/core`, built as correction 2. `importlib.util.find_spec` found none of
`datastorekit`, `ray`, `sqlalchemy`. From the repository root:

```
python -m unittest -v runregistrykit.tests.test_run_registry runregistrykit.tests.test_public_names runregistrykit.tests.test_host runregistrykit.tests.test_status_writes
Ran 80 tests in 12.026s
OK (skipped=1)
```

29 + 8 + 28 + 15. Importing `runregistrykit.tests.test_status_writes` there under `-I` loaded none
of the three. The venv was removed afterwards, and `git status --short --ignored` was unchanged by
the run.

### 4. Nothing outside temporary directories

`git status --short --ignored` was the same before and after every suite run and the core run. No
Ray process before or after any run. `git grep -n 'signal' -- 'runregistrykit/*.py'
':!runregistrykit/tests'` finds `runregistrykit/__init__.py:755` only: `finish`'s docstring, the
line that was `:632`. The children signal only themselves; nothing else was signalled.

### 5. The planner's probe, written again

`agent-02/probe/probe.py`, not committed: a scratch client root (an empty `runregistrykit.toml`
in a git repository), and for each case a child that begins a run, installs a `SIGTERM` handler
calling `run.finish("killed", exit_code=143)`, and sends itself `SIGTERM` from inside a heartbeat's
`json.dump` (`units_done=7`), with half or all of the payload written to the handle. Nothing else is
patched. The handler then raises `SystemExit`, returns, or restores `SIG_DFL` and kills its own
process. Against this tree:

| Handler | Written | Child's exit | Heartbeat raised | Parses | `state` | `exit_code` | `units_done` | Left behind |
|---|---|---:|---|---|---|---:|---:|---|
| raises | half | 143 | `SystemExit` | yes | `killed` | 143 | 7 | nothing |
| raises | all | 143 | `SystemExit` | yes | `killed` | 143 | 7 | nothing |
| returns | half | 0 | nothing | yes | `killed` | 143 | 7 | nothing |
| returns | all | 0 | nothing | yes | `killed` | 143 | 7 | nothing |
| ends the process | half | −15 | — | yes | `killed` | 143 | 7 | one `status.json.<unique>.tmp` |
| ends the process | all | −15 | — | yes | `killed` | 143 | 7 | one `status.json.<unique>.tmp` |

The heartbeat's `stage` was kept in all six. The same probe against `b52cc01`'s writer, in the
scratch clone, gave the planner's "fixed (today)" rows: raises, half: `killed`, `exit_code` null,
`units_done` 0; raises, all: `running`; returns, half and all: `running`, and the child exited 1
with `FileNotFoundError`; ends the process: `killed`, 143, `units_done` 0.

### 6. The new tests against the old writer

`b52cc01`'s `runregistrykit/__init__.py` in the scratch clone, with `2bf9c72`'s tests:
`Ran 15 tests in 3.507s`, `FAILED (failures=14, errors=2)`. Passing: the mode, one read and one
replace, `write_json_atomic`'s name and the old record. Failing: six of the eight reproduction
cases (the fourth point's two pass), the three second-`Run` tests, all three real-signal tests, the
name and the failed write. Erroring: the put-back test, and the threads test, whose main-thread
`finish` raised `FileNotFoundError` from `os.replace` of the shared `status.json.tmp`, two threads'
writes racing for one name. A first run, with a draft of the tests, also errored in the threads
test's cleanup (deviation 21), and one of its messages printed a status with its `host`
(deviation 20); that output stayed in the scratchpad. No output of the final tests, the suites, the
core run or the mutation runs holds a boot UUID, by a search of each.

### 7. `black`

`./venv/bin/black --check runregistrykit docs`: "31 files would be left unchanged." The two changed
Python files were formatted with `./venv/bin/black` first.

### 8. CI

Nothing was pushed. `test_status_writes` first runs on Linux in CI: in both `suite` jobs, and in the
`core` job, which now names it. **The review is to read its result there**, the real-signal
children above all, once the user has pushed.

## The deliberate-breakage record

Each diff below was generated in a scratch clone of this repository holding `2bf9c72`'s tree, and
replayed there **as recorded below**, in `bash`, by a script: `git apply --check`, `git apply`, the
tests, `git apply -R --check`, `git apply -R`. `PYTHONPATH` was the clone, so that the tests and
their children ran it. After each, the clone's `git status --short` was empty; this checkout was
never mutated. `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` found nothing before and
after each run.

| # | Mutation | Run | Failing tests (subtests in brackets) |
|---|---|---|---|
| (m1) | the writer's name fixed at `<path>.tmp` | suite: `Ran 322 tests in 94.589s`, `FAILED (failures=13, errors=1, skipped=1)` | `test_status_writes.TestAHandlerInsideAHeartbeat.test_each_point_each_ending` [6: both endings at half written, all written and before the replace]; `TestAHandlerDuringThePutBack.test_a_second_handler_inside_the_put_back` (error); `TestARealSignal`: all three; `TestASecondRunObject`: all three; `TestThePlainWrite.test_the_temporary_name` |
| (m2) | step 4 removed: a superseded write replaces | suite: `Ran 322 tests in 102.439s`, `FAILED (failures=2, skipped=1)` | `test_status_writes.TestAHandlerInsideAHeartbeat.test_each_point_each_ending` [2: half written and all written, returning] |
| (m3) | step 5's put-back removed | suite: `Ran 322 tests in 97.977s`, `FAILED (failures=3, skipped=1)` | `test_status_writes.TestAHandlerInsideAHeartbeat.test_each_point_each_ending` [before the replace, returning]; `TestASecondRunObject.test_before_the_replace`; `TestAHandlerDuringThePutBack.test_a_second_handler_inside_the_put_back` |
| (m4) | step 2's merge of in-flight fields removed | suite: `Ran 322 tests in 97.053s`, `FAILED (failures=15, skipped=1)` | `test_status_writes.TestAHandlerInsideAHeartbeat.test_each_point_each_ending` [8: every case]; `TestAHandlerDuringThePutBack.test_a_second_handler_inside_the_put_back`; `TestARealSignal`: all three; `TestASecondRunObject`: all three |
| (m5) | step 2's base always the file | suite: `Ran 322 tests in 104.360s`, `FAILED (failures=1, skipped=1)` | `test_status_writes.TestAHandlerDuringThePutBack.test_a_second_handler_inside_the_put_back` |
| (m6) | the bookkeeping keyed by the `Run` object | suite: `Ran 322 tests in 99.053s`, `FAILED (failures=3, skipped=1)` | `test_status_writes.TestASecondRunObject.test_before_the_replace`; `test_half_written`; `test_through_another_spelling_of_the_path` |
| (m7) | the temporary file not removed on an exception | suite: `Ran 322 tests in 100.059s`, `FAILED (failures=5, skipped=1)` | `test_status_writes.TestAHandlerInsideAHeartbeat.test_each_point_each_ending` [3: raising, at half written, all written and before the replace]; `TestARealSignal.test_a_handler_that_raises`; `TestThePlainWrite.test_a_failed_write_leaves_the_status_as_it_was` |
| (m8) | the file created by `tempfile.mkstemp` | suite: `Ran 322 tests in 98.676s`, `FAILED (failures=1, skipped=1)` | `test_status_writes.TestThePlainWrite.test_the_mode_is_the_one_a_plain_open_gives` [umask `0o22`] |
| (m9) | the `RLock` replaced by a `threading.Lock` | the three real-signal tests by name: `Ran 3 tests in 180.468s`, `FAILED (failures=3)` | `test_status_writes.TestARealSignal.test_a_handler_that_raises`, `test_a_handler_that_returns`, `test_a_handler_that_ends_the_process`, each "did not end in 60 s: its handler waited on the write it interrupted" |
| (m10) | the agent's own: `write_json_atomic` writing through a pid-named temporary file | suite: `Ran 322 tests in 102.025s`, `FAILED (failures=6, errors=3, skipped=1)` | `test_status_writes.TestThePlainWrite.test_write_json_atomic_still_replaces_from_its_tmp_name`; `test_store_copy_move.TestInterruption.test_C4_the_sidecar_is_written_to_its_tmp_name_and_the_replace_fails` [3]; `test_store_copy_move.TestInterruption.test_M6_the_update_is_written_to_its_tmp_name_and_the_replace_fails` [3, errors]; `test_store_retire.TestInterruption.test_I0t_the_tombstone_write_is_killed_and_leaves_its_tmp`; `test_store_retire.TestInterruption.test_I6t_the_completion_write_is_killed_and_leaves_its_tmp` |

Each failed at least one test. Notes:
- Under (m2) the final file is `killed`: the heartbeat's replace lands `running`, and step 5 then
  puts `killed` back. What the two failing cases catch is the extra replace, three where there
  should be one, and with it the `running` a reader could see in between (deviation 19).
- Under (m9) no in-process test was run: each would block for ever on its own re-entrance. The
  three children were killed by `subprocess.run`'s timeout; `pgrep -lf child.py` found none left.
- No existing test changed. Under (m10) existing store tests fail, as they should: they pin the
  sidecar's `<path>.tmp`.

### The diffs

#### (m1)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..54ec444 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -278,7 +278,7 @@ def _status_temporary_name(path) -> str:
     `status.json.`, ends `.tmp`, and is never `status.json.tmp`, the name `write_json_atomic`
     uses. The pid, a per-process counter and random hex make it one write's own, in one process or
     two."""
-    return f"{path}.{os.getpid()}-{next(_STATUS_NAMES)}-{os.urandom(4).hex()}.tmp"
+    return path + ".tmp"
 
 
 def _remove_quietly(name) -> None:
```

#### (m2)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..0f61968 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -308,9 +308,6 @@ def _land_status(path, book, number, payload) -> None:
             handle.write("\n")
             handle.flush()
             os.fsync(handle.fileno())
-        if book["landed"] > number:
-            os.remove(name)
-            return
         os.replace(name, path)
     except BaseException:
         _remove_quietly(name)
```

#### (m3)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..43d2e30 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -316,7 +316,6 @@ def _land_status(path, book, number, payload) -> None:
         _remove_quietly(name)
         raise
     if book["landed"] > number:
-        _land_status(path, book, book["landed"], book["payload"])
         return
     book["landed"], book["payload"] = number, copy.deepcopy(payload)
 
```

#### (m4)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..e2db2c1 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -339,8 +339,6 @@ def _write_status(path, fields) -> dict:
                 status = copy.deepcopy(book["payload"])
             else:
                 status = read_json(path) or {}
-            for n in earlier:
-                status.update(book["in_flight"][n])
             status.update(fields)
             status["heartbeat"] = now_iso()
             _land_status(path, book, number, status)
```

#### (m5)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..8903bf2 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -334,11 +334,7 @@ def _write_status(path, fields) -> dict:
         try:
             book["in_flight"][number] = dict(fields)
             earlier = sorted(n for n in book["in_flight"] if n < number)
-            if earlier and book["payload"] is not None:
-                # a handler has re-entered a write: the file may hold what that write read
-                status = copy.deepcopy(book["payload"])
-            else:
-                status = read_json(path) or {}
+            status = read_json(path) or {}
             for n in earlier:
                 status.update(book["in_flight"][n])
             status.update(fields)
```

#### (m6)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..4ed6193 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -321,12 +321,12 @@ def _land_status(path, book, number, payload) -> None:
     book["landed"], book["payload"] = number, copy.deepcopy(payload)
 
 
-def _write_status(path, fields) -> dict:
+def _write_status(path, fields, owner) -> dict:
     """Merge ``fields`` into the `status.json` at ``path``, stamp the heartbeat, write it, and
     return the payload composed. `Run._update` says what is and is not covered."""
     with _STATUS_LOCK:
         book = _STATUS_WRITES.setdefault(
-            os.path.realpath(path),
+            owner,
             {"next": 0, "in_flight": {}, "landed": -1, "payload": None},
         )
         number = book["next"]
@@ -720,7 +720,7 @@ class Run:
         directory. Nothing reads it, `list` and the store operations do not look at a run
         directory's other files, and nothing removes it.
         """
-        return _write_status(self.status_path, fields)
+        return _write_status(self.status_path, fields, self)
 
     def heartbeat(
         self, units_done=None, units_total=None, pid=None, stage=None
```

#### (m7)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..bdd00c4 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -313,7 +313,6 @@ def _land_status(path, book, number, payload) -> None:
             return
         os.replace(name, path)
     except BaseException:
-        _remove_quietly(name)
         raise
     if book["landed"] > number:
         _land_status(path, book, book["landed"], book["payload"])
```

#### (m8)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..b4250c7 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -300,9 +300,12 @@ def _land_status(path, book, number, payload) -> None:
     the `os.replace` call) is put back afterwards, by a write of its payload under its own number,
     which is itself checked in the same way.
     """
-    name = _status_temporary_name(path)
+    import tempfile
+
+    descriptor, name = tempfile.mkstemp(
+        prefix=os.path.basename(path) + ".", suffix=".tmp", dir=os.path.dirname(path)
+    )
     try:
-        descriptor = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
         with open(descriptor, "w") as handle:
             json.dump(payload, handle, indent=2, sort_keys=True)
             handle.write("\n")
```

#### (m9)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..c5be625 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -262,7 +262,7 @@ def write_json_atomic(path, payload) -> None:
 # held across a whole status write. Re-entrant, so that a handler that interrupts a write on its
 # own thread and writes again is not blocked by the write it interrupted; a plain lock would
 # leave that handler waiting for ever. Two threads' writes are serialised by it
-_STATUS_LOCK = threading.RLock()
+_STATUS_LOCK = threading.Lock()
 
 # per `status.json`, keyed by its real path, so that every `Run` object for one run directory in
 # this process is one writer: the next sequence number, the fields of each write still in flight,
```

#### (m10)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 700e04c..15d71f4 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -247,7 +247,7 @@ def read_json(path):
 def write_json_atomic(path, payload) -> None:
     """Write via a temporary file **in the same directory** and `os.replace`, so that a reader
     either sees the previous contents or the new ones and never a half-written file."""
-    tmp = path + ".tmp"
+    tmp = f"{path}.{os.getpid()}.tmp"
     with open(tmp, "w") as handle:
         json.dump(payload, handle, indent=2, sort_keys=True)
         handle.write("\n")
```

## Observations not acted on

1. **Correction 6's case, measured.** In scratch (`agent-02/c6/`), in one process with `json.dump`
   patched: a `heartbeat(units_done=7, stage="A")` whose write makes, from inside it, a first
   handler's `heartbeat(stage="B")` (which lands; the file says `B`) and then a second handler's
   `finish("killed", exit_code=143)`. The `finish` composes from the landed `B` payload, re-applies
   the still-in-flight `stage="A"` over it, and lands `A`: the end is `killed`, 143, `units_done` 7,
   `stage` `A`, nothing left behind. So a field set by an earlier in-flight write is re-applied over
   a newer landed one. A variant with terminal states: a `finish("done", exit_code=0)` whose write
   makes a handler's `finish("killed", exit_code=143)` and then a handler's `heartbeat` ends `done`,
   0, because the second handler's write re-applies the in-flight `done` over the landed `killed`.
   Both need two handler writes inside one write; the second needs the run's own `finish` to be the
   write interrupted. In neither is a terminal state replaced by `running`. My view: the rule does
   what the prompt says, and what it buys (a discarded heartbeat's fields kept) is worth more than
   these cases cost. A refinement would apply an in-flight write's fields only where no later
   landed write set the same key, which needs the bookkeeping to remember which write set which key.
   Not changed, and no issue opened, as correction 6 says; the review decides.
2. **A fork.** `_STATUS_LOCK` and `_STATUS_WRITES` are module state, copied into a child made by
   `os.fork`. A fork made while another thread holds the lock leaves the child's lock held by a
   thread that does not exist there, so the child's first status write would wait for ever. Read,
   not measured; the standard hazard of any lock across a fork, and Python 3.12 already warns of
   forking a process with threads. `os.register_at_fork(after_in_child=…)` could renew the lock and
   empty the books. Not in the prompt, so not done, and no issue opened: the review decides whether
   it is one.
3. **A raise inside the `finally`.** If a handler raises (for example `KeyboardInterrupt` from
   Python's default `SIGINT` handler) at the bytecode boundary inside `_write_status`'s `finally`,
   before its one statement has removed the write's in-flight entry, the entry stays for the life of
   the process. Every later write to that `status.json` then takes itself as re-entered: its base is
   the landed payload rather than the file, and the stale fields are re-applied. Read, not measured;
   the window is one statement. Not acted on.
4. **The bookkeeping lasts the process.** One entry per `status.json` the process has written, with
   its last payload. A process that begins many runs keeps one small dict for each. Not a defect.
5. **The leftover.** A process killed between creating its temporary file and replacing it leaves a
   `status.json.<unique>.tmp`, as the prompt says; nothing removes it. 04's `end` and 06's release
   notes may want to name it for a person who finds one.

## State handed to the next prompt

- **The interface after 02:** `Run._update`'s supersession rule, in `_write_status` and
  `_land_status` (`runregistrykit/__init__.py:324`, `:291`), and its docstring (`:691-723`).
  `write_json_atomic` is unchanged (`:247-256`), and so are `status.json`'s keys and values for
  every write that is not re-entered.
- **For 03:** 02 removes the one known cause of an unreadable `status.json`. Every other cause
  stands, and `list_runs` (`:1085`, its read `:1115`) and `liveness` (`:561`, the empty payload
  `:585`) are as they were.
- **For 04:** `end` writes `status.json` through `Run._update` like everything else, so it inherits
  the writer: its own temporary name, and no `status.json.tmp`. A hard-killed process may have left
  a `status.json.<unique>.tmp` beside a stale run's status (observation 5).
- **For 06:** the release notes say "`write_json_atomic`: unchanged", and that `status.json` is
  written through `status.json.<unique>.tmp` with the mode `0666` less the umask.
- **CI:** the push is the user's. The first CI run is the first run of `test_status_writes` on
  Linux, the real-signal children above all.
- The suite is 322, with one skip on macOS (the Linux readers).
