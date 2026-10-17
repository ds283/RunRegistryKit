# Log — prompt 02c: the writer's lock

**Subject:** Make the status writer's filters generator expressions
**Commit:** this commit (on `main`, after `e4a2b6c`)
**Date:** 2026-10-17
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1–16). No stop condition fired.
**Result:** **landed.**
- `_write_status`'s two filters are generator expressions, `list(n for n in … if …)`, at
  `runregistrykit/__init__.py:366` and `:373`, with a one-line comment at `:365`. A handler that
  raises at a filter's jump now leaves that generator's own frame and reaches `_write_status` at
  the `CALL` of `list`, which its exception table covers. So the `finally` and the `with`'s exit
  both run.
- By `dis`, no `JUMP_BACKWARD` of `_write_status` is outside its exception table at 3.12.15, 3.13.16
  or 3.14.8. At `2959b78` the two filters' jumps were outside it at all three.
- A real signal, 45 s per row with the handler raising, left the lock held **0** times at 3.12.15
  and at 3.13.16, and 0 times in 36 506 interruptions at 3.13.16 over 120 s. At 3.14.8 it left it
  held once, at the `with`'s entry. Against `2959b78`, 1 at 3.13.16, at `:365`.
- `Run._update`'s "Not covered" paragraph gains §2.4's sentence on the 3.14 `with` point (L11 (a)).
  `pyproject.toml` is not touched.
- The suite is **328 → 329**: one new test in `test_status_writes`, core,
  `TestARaisingHandlerAtEveryJump`. Its three subtests are the three writes. It fails against
  `2959b78` at 3.12.15 and at 3.13.16, and (m1)–(m4) each fail it.
- The core alone runs 87 tests (86 + 1), OK, one skip. `test_status_writes` and `test_host` at
  3.13.16 and 3.14.8 run 50 (49 + 1), OK, one skip.
- The twelve real-signal cases all end `killed`, 143, `units_done` 7, at 3.12 and at 3.13.
- The issue is **narrowed, not closed**: it stays in the board's §3, its owner none again, its
  hook in `docs/OPEN_ISSUES.md` narrowed to 3.14. The index still counts **9**.
- **Nothing pushed, no tag made, no workflow dispatched.**

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | In `_write_status` (`:352`): the comment `:365`, the first filter `:366`, the second `:373`. In `Run._update`'s docstring (`:726-766`), one sentence at the end of the "Not covered" paragraph (`:763-765`). Nothing else: `git diff 2959b78` is these two hunks, 6 lines added and 3 removed |
| `runregistrykit/tests/test_status_writes.py` | Additions only (283 lines, none removed): `import dis` (`:29`), then from `:965`, after 02b's sweep class, the helpers and one test class (below) |
| this log, `IMPLEMENTATION_STATE.md`, the campaign README's §2 row for 02c, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: `pyproject.toml` (L11 is (a)), `stores.py`, `__main__.py`, `client.py`, `.github/`,
`README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption/`, any other test module or fixture, the
prompt, any other part of the campaign README, and `orchestrator/`. `write_json_atomic`
(`:247-256`) is byte for byte as it was. No key of `status.json` is added, removed or renamed. The
merge, the discard, the put-back, the record, the temporary name and the mode are unchanged.

### The writer

```python
            # generators: a handler raising at a comprehension or loop filter leaves the lock held
            earlier = list(n for n in sorted(book["in_flight"]) if n < number)
            ...
                earlier = list(n for n in earlier if n > landed)
```

The first still iterates `sorted(book["in_flight"])`, a list made by one C call, and never the live
dict. `number` and `landed` become cell variables of `_write_status` (two `MAKE_CELL`s at its
start, before the `with`).

### The test

From `runregistrykit/tests/test_status_writes.py:965`, all core:

| Name | What |
|---|---|
| `JUMP_BACK`, `JUMP_SWEEP_SECONDS` (60 s per write), `MOST_RELEASES` (100) (`:972-977`) | the opname attempted, and two bounds |
| `CountedInOrder` (`:980`) | a subclass of 02b's `Instructions`. While its `order` is a list, it records the `(code, offset)` of each instruction an attempt counts, in the order counted, then defers to `Instructions.on_instruction` |
| `InsideTheSweptWrite` (`:999`) | a subclass of 02's `Interruption`, half written, firing once. It passes through while the sweep's handler is busy, so the inner writes are made only from inside the write swept |
| `the_jumps_writes` (`:1015`) | the three writes. (1) `heartbeat(units_done=7)`. (2) `heartbeat(units_done=8)` whose `json.dump` makes a handler's `heartbeat()`. (3) `heartbeat(units_done=8)` whose `json.dump` makes a handler's `heartbeat(stage="B")` and then `heartbeat(stage="C")` |
| `the_lock_is_free` (`:1050`), `free_the_lock` (`:1067`), `in_flight_for` (`:1079`) | another thread's `_STATUS_LOCK.acquire(blocking=False)`, released at once if it succeeds, joined with a 10 s timeout. `release()` on the writing thread until that succeeds, at most 100 times. The book's `in_flight` keys for the run, read only |
| `jumps_in_this_process` (`:1086`) | the sweep, below |
| `JUMP_SWEEPER` (`:1181`), `JUMP_SWEEPER_TIMEOUT` (240 s) | the child's script and its timeout |
| `TestARaisingHandlerAtEveryJump.test_the_lock_is_free_and_nothing_is_in_flight` (`:1195`, `:1205`) | starts the child, never signals it, and asserts on its report, one subtest per write |

**The sweep, in the child.** A run is begun under the test's runs root. The code objects are
`the_writers_code()`, so the two new `<genexpr>`s are swept, and opnames come from
`dis.get_instructions` on each. Monitoring is `CountedInOrder`, a free tool id, with events cleared
and the id freed however the block ends (02b's `close`). Then, for each write:
- **The count.** On a fresh run (02b's shape: a `copytree` of the begun run to a new real path, so
  a book of its own, then one plain `heartbeat()`), one uninterrupted write under `Attempt(0)`
  records the order. The report keeps its outcome, its ending, whether the inner handler's writes
  were made, and the count.
- **The targets.** Every index in the order whose instruction is `JUMP_BACKWARD`.
- **One attempt per target**, each on a fresh run. The handler is 02b's
  `the_handler(run, "finish", "raises")`: `finish("killed", exit_code=143)`, then
  `raise SystemExit(143)`. While it runs, `Attempt.busy` keeps its instructions uncounted.
- **The checks after each attempt:**
  - the handler ran, at the `(code, offset)` intended;
  - the write raised `SystemExit(143)`;
  - no in-flight entry is left for the run;
  - the lock is free. If not, `free_the_lock` releases it on this thread, and the count is
    reported;
  - `ending_of(run)` is `["killed", 143]`: it parses, and nothing is left behind.
- Any check that fails is reported with the index, code name, line and offset.

**The test asserts:**
- the child exits 0;
- `_write_status` and `_land_status` are among the codes;
- there are three writes. For each: the uninterrupted write returned and left `running`; the inner
  writes were made in (2) and (3) and not in (1); the count is within `MOST_INSTRUCTIONS`; **at
  least one attempt** was made;
- **nothing went wrong**. The failure message gives the count, every attempt, and what went wrong
  at each.

The new test alone runs in 0.411 s in `venv/`. The attempts take 0.01–0.05 s per write.

## Deviations from the prompt

Each is classified. Corrections 1–16 are section 0's.

1. **L11 is (a)** (correction 1). The user took it on 2026-10-17 (`069f1d7`). §2.4's (a) is
   applied:
   - the docstring sentence is added;
   - `pyproject.toml` is not changed;
   - the issue is **narrowed**: it stays in §3 with owner none, its index hook is narrowed to 3.14,
     and the count stays 9.

   Every "under (b)" in the prompt is inert. **STRUCTURALLY REQUIRED.**
2. **The suite's time** (correction 2). Each suite run was in the foreground with a 600 000 ms
   timeout, its output in a file, the verdict grepped from it: 101.727 s before, 101.480 s after,
   and 104.497 s on the tree as committed (§10 below). **STRUCTURALLY REQUIRED.**
3. **The core run** (correction 3): `uv venv -p /opt/local/bin/python3.12 agent-02c/core`, then
   `uv pip install --offline -p agent-02c/core/bin/python -e` this checkout, with `TMPDIR` in the
   scratch. The venv was removed afterwards. **STRUCTURALLY REQUIRED.**
4. **3.13 and 3.14** (correction 4). MacPorts' interpreters ran the checkout, and the scratch
   clones, through `PYTHONPATH`. No `-m pip`, and nothing installed. **STRUCTURALLY REQUIRED.**
5. **Two meanings of "handler"** (correction 5). The class docstring and `the_jumps_writes`' say
   so:
   - the writes made from inside `json.dump` are part of the write swept, and their jumps are
     attempted;
   - the sweep's own handler's writes are not, since `Attempt.busy` leaves them uncounted.

   `InsideTheSweptWrite` also stops the inner handler firing inside the sweep's handler's own
   write, which happens when the sweep's handler runs before the outer write reaches its
   `json.dump`. **STRUCTURALLY REQUIRED**; the pass-through is an **IMPLEMENTATION CHOICE**.
6. **Targeting `JUMP_BACKWARD`** (correction 6). The order is recorded by a subclass of
   `Instructions` that wraps its callback, and `dis.get_instructions(code)` is matched on offset.
   Each attempt checks `attempt.where` against the target and fails if they differ. None differed
   at any version. `Attempt`, `Instructions` and 02b's other names are not edited. **IMPLEMENTATION
   CHOICE.**
7. **The lock check uses no private method of the lock** (correction 7). It reaches the lock as
   `runregistrykit._STATUS_LOCK`, a private name of the module, and uses `acquire(blocking=False)`
   and `release()`. The book is read through `runregistrykit._STATUS_WRITES`, read only, as 02b's
   `seen_by_the_handler` does. **STRUCTURALLY REQUIRED.**
8. **The counts** (correction 8). The writes made 3, 7 and 12 attempts at 3.12.15, 3.13.16 and
   3.14.8, out of 327 / 626 / 985 instructions (3.12), 327 / 632 / 991 (3.13) and 346 / 672 / 1054
   (3.14). These are the planner's counts. **STRUCTURALLY REQUIRED.**
9. **The static check covers every code object of `the_writers_code()`** (correction 9): the table
   in §4 below, per code object and version, against both trees.
   - **`JUMP_BACKWARD`s outside a table are left in three places**, at every version and in both
     trees: the generator expressions' own filter jumps, `_land_status`'s two prune-loop jumps
     (`:348-349`, after its `try`), and `_newest_landed`'s loop (`:299`; that function has no
     table at all).
   - **None of them can leave the lock held.** An exception there leaves that frame, which holds
     no lock and has no handler for it in force. It reaches `_write_status` at a `CALL` its table
     covers: of `list`, `_land_status` or `_newest_landed`.
   - **The new test attempts every one of them that a write reaches, and none goes wrong.**
     `_newest_landed`'s loop is never reached: its first pass returns.

   So the prompt's §5 condition, a writer `JUMP_BACKWARD` that §2.2's form does not remove, is read
   as `_write_status`'s own (§3.4 names it). **STRUCTURALLY REQUIRED.**
10. **The real signal, one row at a time** (correction 10). There were nine rows, run one after
    another (§5 below). The counts against `2959b78` are lower than the planner's, who ran
    fourteen children at once: 1 against 5 at 3.13.16, and 0 against 30 at 3.14.8. The event is
    rare, and timing under load differs. **STRUCTURALLY REQUIRED.**
11. **The twelve-case probe at 3.12 and at 3.13** (correction 11): two tables, identical (§6).
    **STRUCTURALLY REQUIRED.**
12. **The one-line comment** (correction 12) is `# generators: a handler raising at a comprehension
    or loop filter leaves the lock held`, 98 characters with its indent.
    - **What it leaves out.** One line under 100 characters cannot also carry "outside the
      exception table" and "skips the `with`'s exit and the `finally`". It names the consequence
      instead, and this log and the board give the mechanism.
    - **The guards.** It says "handler", not "signal", and names no issue. §3.9's grep and
      `test_no_citation` pass.

    **IMPLEMENTATION CHOICE.**
13. **The docstring sentence** is §2.4's, word for word, at the end of the "Not covered" paragraph.
    It says "handler". **STRUCTURALLY REQUIRED.**
14. **Line citations** (correction 13) were taken by `grep -n` on the files after `black`, and
    re-checked just before committing. The three §3 entries of 03, 04 and 05 each gain one
    "Package lines (02c, this commit)" sentence, and are otherwise unchanged. The narrowed entry
    gains its own sentence, inside its new "Narrowed" paragraph. **STRUCTURALLY REQUIRED.**
15. **Mutation diffs** (correction 14) were taken after `black` in a scratch clone (`agent-02c/new`)
    of this tree. Its `runregistrykit/__init__.py` blob is `57f820d`, the same as this commit's.
    They were replayed as recorded. **STRUCTURALLY REQUIRED.**
16. **`black`** (correction 15): `black --check runregistrykit docs` passes on this tree, 31 files,
    the count section 0 gives for `2959b78`; no file is added under `runregistrykit` or `docs`.
    **STRUCTURALLY REQUIRED.**
17. **The status rows** (correction 16). The board's row for 02c, and the campaign README's §2 row,
    say "landed, not yet reviewed". The board's Orchestrator notes line is not edited. Besides the
    row, the board's header, the 02c row's suite (328 → 329), the suite sentence, W3 (✅ this
    commit) and the §3 count line are updated (the prompt's §4.3). **STRUCTURALLY REQUIRED.**
18. **One test method with three subtests**, one per write, so N = 1. **IMPLEMENTATION CHOICE.**
19. **The new test checks more than §2.5 lists**, so that a pass means what it says:
    - that each attempt raised `SystemExit(143)` from the write;
    - that the uninterrupted write left `running`;
    - that the inner writes were made exactly in writes (2) and (3).

    **IMPLEMENTATION CHOICE.**
20. **The real-signal probe's handler returns, unmeasured, when the timer fires after the
    heartbeat is over.** A first version raised `SystemExit` outside the probe's `try`, and the
    probe ended. That happened when a pending handler ran at the loop's own jump after the
    heartbeat had returned. Such late fires are counted apart: 63–240 per row. **IMPLEMENTATION
    CHOICE** (scratch only).

No UNINTENDED DRIFT.

## Verification performed

### 1. The state at the start

- `HEAD` `e4a2b6c`, `main`, clean, the only worktree. `git diff --stat 2959b78 HEAD --
  runregistrykit pyproject.toml .github` was empty.
- `RAY_ADDRESS` unset; no Ray process.
- `venv/`: Python 3.12.15, black 25.1.0. `/opt/local/bin/python3.12` 3.12.15, `python3.13` 3.13.16,
  `python3.14` 3.14.8.
- `git status --short --ignored`: `prompts/.DS_Store`, `runregistrykit.egg-info/`, both
  `__pycache__/`, `var/` and `venv/`.
- `var/ledger.jsonl` `471d0859…`, before and after.

### 2. The suite, before and after

`TMPDIR=<agent-02c>/tmp ./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from
the root, in the foreground. `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` found nothing
(exit 1) before and after every run. Per module, by `unittest.defaultTestLoader.discover`:

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
| `test_status_writes` | 21 | **22** |
| `test_store_amend` | 21 | 21 |
| `test_store_amend_residuals` | 9 | 9 |
| `test_store_command_line` | 2 | 2 |
| `test_store_copy_move` | 27 | 27 |
| `test_store_fingerprint` | 29 | 29 |
| `test_store_retire` | 41 | 41 |
| `test_store_retire_references` | 10 | 10 |
| `test_store_sidecar` | 17 | 17 |
| **total** | **328**, `Ran 328 tests in 101.727s`, `OK (skipped=1)` | **329**, `Ran 329 tests in 101.480s`, `OK (skipped=1)` |

N = 1. The skip is `test_host`'s Linux readers, as before. Every test that existed at `2959b78` is
unchanged: `git diff 2959b78 --numstat -- runregistrykit/tests` is `283 0`. `git status --short
--ignored` was the same before and after.

### 3. The core alone, and 3.13 and 3.14

**The core alone**, built as correction 3. `importlib.util.find_spec` found none of
`datastorekit`, `ray` or `sqlalchemy`. From the root:

```
python -m unittest runregistrykit.tests.test_run_registry runregistrykit.tests.test_public_names runregistrykit.tests.test_host runregistrykit.tests.test_status_writes
Ran 87 tests in 21.056s
OK (skipped=1)
```

That is 29 + 8 + 28 + 22. The venv was removed afterwards.

**At 3.13 and 3.14**, from the root, with `TMPDIR` in the scratch and `PYTHONPATH` on the checkout,
`python -m unittest runregistrykit.tests.test_status_writes runregistrykit.tests.test_host`:

| Python | Run |
|---|---|
| 3.12.15 (`venv/`) | `Ran 50 tests in 16.781s`, `OK (skipped=1)` |
| 3.13.16 | `Ran 50 tests in 16.974s`, `OK (skipped=1)` |
| 3.14.8 | `Ran 50 tests in 17.474s`, `OK (skipped=1)` |
| 3.13.16, without `PYTHONPATH` | `Ran 50 tests`, `FAILED (failures=2, skipped=1)`: `test_host.TestTheCommandLine.test_foreign_and_stale_rows_and_the_count_of_records_with_no_host` and `test_no_foreign_run_no_foreign_line`, each `No module named runregistrykit`. This is the environment, as the prompt says |

### 4. The static check

`agent-02c/probe/static.py`, not committed. For each code object of `the_writers_code()`, it lists
the instructions that no entry of `dis.Bytecode(code).exception_entries` covers. It was run at
3.12.15 (`venv/`), 3.13.16 and 3.14.8, on this tree and on a `git archive` of `2959b78`.
Offsets are given; "the exit" is the `with`'s normal exit sequence (`SWAP`, the `LOAD_CONST`s, the
`CALL` of `__exit__`, `POP_TOP`, `RETURN_VALUE`). Every function also has uncovered instructions
after its last entry: the tail of the `with`'s exceptional exit (`POP_EXCEPT` … `RERAISE`), which
an exception never reaches with the lock to release. Those are not repeated below.

**`_write_status`**:

| Tree | 3.12.15 | 3.13.16 | 3.14.8 |
|---|---|---|---|
| `2959b78` | before the table: `RESUME`, `LOAD_GLOBAL`, `BEFORE_WITH` 12; `NOP` 190 (`try:`); **`JUMP_BACKWARD` 278 (`:365`), 398 (`:372`)**; the exit 636–654 | before: through `BEFORE_WITH` 12; `NOP` 192; **`POP_JUMP_IF_TRUE` 278 + `JUMP_BACKWARD` 282 (`:365`); 418 + 422 (`:372`)**; the exit 676–694 | the `with`'s entry, `LOAD_GLOBAL` 2 through `CALL` 22; `NOP` 220; **`POP_JUMP_IF_TRUE` 320, `NOT_TAKEN` 324, `JUMP_BACKWARD` 326 (`:365`); 464, 468, 470 (`:372`)**; `NOT_TAKEN` 526 (`:374`); the exit 750–770 |
| this commit | before the table: `MAKE_CELL` 0, 2, `RESUME`, `LOAD_GLOBAL`, `BEFORE_WITH` 16; `NOP` 194 (`try:`); the exit 636–654 | before: through `BEFORE_WITH` 16; `NOP` 196; the exit 668–686 | the `with`'s entry, `LOAD_GLOBAL` 6 through `CALL` 26; `NOP` 224; `NOT_TAKEN` 516 (`:375`); the exit 742–762 |

So no `JUMP_BACKWARD` of `_write_status` is uncovered after the change. Its one remaining
`JUMP_BACKWARD` is the `for n in earlier` loop's (`:376-377`), covered at every version: 500, 530 and 596.
At `2959b78` the comprehensions' second jumps (284/404, 290/430, 334/478) were covered, and the
filters' false branches were not.

**The other code objects.** `JUMP_BACKWARD`s with the table's entries; "uncovered" marks those
outside every entry:

| Code | 3.12.15 | 3.13.16 | 3.14.8 | Why an uncovered one cannot leave the lock held |
|---|---|---|---|---|
| `<genexpr>:366` (new) | 26 uncovered (the filter's false branch), 36 covered | `POP_JUMP_IF_TRUE` 24 + 28 uncovered, 40 covered | 22, `NOT_TAKEN` 26, 28 uncovered, 40 covered | the generator's frame holds no lock. Its only entry is the generator's own `StopIteration` guard. An exception at 28 leaves the frame and is raised in `_write_status` at the `CALL` of `list`, which `_write_status`'s table covers |
| `<genexpr>:373` (new) | the same offsets | the same | the same | the same |
| `_land_status:308` (both trees) | 686 (`:348`), 724 (`:349`) uncovered; 746 (`:328`) covered | 682, 722 uncovered | 746, 786 uncovered | the prune loop, after its `try`. The frame holds no lock, and its one handler removes the temporary file and covers only the write and the replace. An exception there reaches `_write_status` at the covered `CALL` of `_land_status` |
| `_newest_landed:294` (both trees) | 104 (`:299`), no table | 100 | 112 | the `while True` loop, in a function with no handler. Its callers' `CALL`s are covered (`_write_status` `:367`; `_land_status` `:333`, inside its `try`, and `:341`, which propagates as above). Never reached: its first pass returns |
| `_status_temporary_name`, `_remove_quietly` | no `JUMP_BACKWARD` | — | — | — |

The new test attempts every one of these that a write reaches, at every version: the genexprs'
26/28 and 36/40, `_land_status`'s two, and `_write_status`'s `:377`. None goes wrong.

### 5. The real signal

`agent-02c/probe/bombard.py`, not committed. It is a child that signals only itself:
- a `SIGALRM` handler that records where it ran (the innermost frame of the writer's code on the
  stack, its line and `f_lasti`) and raises `SystemExit(143)`;
- in the second variant, the handler first records `finish("killed", exit_code=143)`;
- a one-shot `setitimer(ITIMER_REAL, uniform(20 µs, 2 ms))` armed inside the `try`, before each
  `heartbeat(units_done=i)` of one run, and disarmed after each.

After each interrupted heartbeat it checks two things: whether an in-flight entry is left, which is
then cleared (probe only); and whether another thread's `acquire(blocking=False)` fails, in which
case the lock is released on the main thread until it succeeds. It also checks that the file
parses. Nothing else is signalled. The rows ran one at a time:

| Tree | Python | s | Handler | Heartbeats | Interrupted | In the writer | **Lock held** | **In flight left** | Where | Final |
|---|---|---:|---|---:|---:|---:|---:|---:|---|---|
| this commit | 3.12.15 | 45 | raises | 115 319 | 14 821 | 14 757 | **0** | **0** | — | `running` |
| this commit | 3.13.16 | 45 | raises | 124 684 | 13 869 | 13 775 | **0** | **0** | — | `running` |
| this commit | 3.14.8 | 45 | raises | 121 601 | 13 948 | 13 854 | 1 | 0 | `_write_status:355`, offset 26 (the `with`'s `CALL` of `__enter__`) | `running` |
| `2959b78` | 3.12.15 | 45 | raises | 118 520 | 13 859 | 13 788 | 0 | 0 | — | `running` |
| `2959b78` | 3.13.16 | 45 | raises | 123 977 | 13 516 | 13 443 | **1** | **1** | `_write_status:365`, offset 282 | `running` |
| `2959b78` | 3.14.8 | 45 | raises | 122 626 | 13 755 | 13 668 | 0 | 0 | — | `running` |
| this commit | 3.13.16 | 120 | raises | 331 587 | 36 506 | 36 287 | **0** | **0** | — | `running` |
| this commit | 3.13.16 | 45 | `killed`, then raises | 113 448 | 12 466 | 12 390 | **0** | **0** | — | `killed`, 143 |
| `2959b78` | 3.13.16 | 45 | `killed`, then raises | 110 854 | 12 422 | 12 356 | 1 | 1 | `_write_status:365`, offset 282 | `killed`, 143 |

"In the writer" counts interruptions whose stack held a writer frame; the rest fell in the
probe's own lines around the call.
- **After the change: 0 at 3.12 and 3.13** (§5's condition). **At 3.14.8, only the `with`'s entry**
  (§2.4). No in-flight entry was left there, since the write had not taken its number.
- `2959b78` at 3.14.8 gave no hit in this row. The planner's 30, under load, stand; the point is
  rare and depends on timing.

### 6. 02's real-signal probe: the twelve cases

`agent-02c/probe/signal/`, not committed. It is 02b's §3.4 probe, written again:
- a child per case begins a run and installs a `SIGTERM` handler calling
  `run.finish("killed", exit_code=128 + signum)`;
- it sends itself `SIGTERM` from inside a heartbeat (`units_done=7`, a stage) at one of four
  points: half the payload written, all of it, before the real replace, after it;
- the handler then raises `SystemExit`, returns, or restores `SIG_DFL` and kills its own process.

The table at 3.12.15 (`venv/`) and the table at 3.13.16 (`PYTHONPATH`) are **identical**:

| Point | Handler | Exit | Heartbeat | Parses | `state` | `exit_code` | `units_done` | Stage kept | Left behind |
|---|---|---:|---|---|---|---:|---:|---|---:|
| half written | raises | 143 | `SystemExit` | yes | `killed` | 143 | 7 | yes | 0 |
| half written | returns | 0 | returned | yes | `killed` | 143 | 7 | yes | 0 |
| half written | ends the process | −15 | — | yes | `killed` | 143 | 7 | yes | 1 |
| all written | raises | 143 | `SystemExit` | yes | `killed` | 143 | 7 | yes | 0 |
| all written | returns | 0 | returned | yes | `killed` | 143 | 7 | yes | 0 |
| all written | ends the process | −15 | — | yes | `killed` | 143 | 7 | yes | 1 |
| before the replace | raises | 143 | `SystemExit` | yes | `killed` | 143 | 7 | yes | 0 |
| before the replace | returns | 0 | returned | yes | `killed` | 143 | 7 | yes | 0 |
| before the replace | ends the process | −15 | — | yes | `killed` | 143 | 7 | yes | 1 |
| after the replace | raises | 143 | `SystemExit` | yes | `killed` | 143 | 7 | yes | 0 |
| after the replace | returns | 0 | returned | yes | `killed` | 143 | 7 | yes | 0 |
| after the replace | ends the process | −15 | — | yes | `killed` | 143 | 7 | yes | 0 |

These are also the rows of 02b's log. What is left behind is the documented
`status.json.<unique>.tmp`. No child was left (`pgrep -lf probe/signal/child.py`, exit 1).

### 7. The new test against `2959b78`'s writer

The new test file was copied into a scratch clone of `2959b78` (`agent-02c/old`), and
`python -m unittest runregistrykit.tests.test_status_writes` was run with `PYTHONPATH` on the clone:
- 3.12.15: `Ran 22 tests in 14.225s`, `FAILED (failures=3)`;
- 3.13.16: `Ran 22 tests in 13.298s`, `FAILED (failures=3)`.

The three failures are the new test's three subtests. Every other test passes there. The failing
attempts, by the child's report:

| Write | 3.12.15 | 3.13.16 | 3.14.8 (the report only) |
|---|---|---|---|
| (1) plain, 3 attempts | **1**: #51 (`:365` offset 278) | **1**: #52 (282) | **1**: #59 (326) |
| (2) re-entered once, 7 | **2**: #51, #229 (278) | **2**: #52, #231 (282) | **2**: #59, #252 (326) |
| (3) re-entered twice, 12 | **4**: #51, #229, #593 (278); #650 (`:372` offset 398) | **4**: #52, #231, #591 (282); #648 (`:372` offset 422) | **4**: #59, #252, #632 (326); #692 (`:372` offset 470) |

Each failure is the same, "in flight after it: [n]; the lock was held: 1 releases freed it". The
file said `killed`, 143, after each. The planner's 1, 2 and 4.

### 8. Nothing outside temporary directories

- `git status --short --ignored` was the same before and after every run.
- The sweep's child writes under the test's `tempfile` runs root, and removes each attempt's copy.
- The probes ran under `TMPDIR` in `agent-02c`.
- `git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'` finds
  `runregistrykit/__init__.py:799` only, `finish`'s docstring. `git grep -n 'SIGTERM\|signal\.' --
  runregistrykit ':!runregistrykit/tests'` finds nothing.
- The new test sends no signal.

### 9. `black`

`./venv/bin/black --check runregistrykit docs`: "31 files would be left unchanged". The two Python
files were formatted with `./venv/bin/black` first.

### 10. The final tree, and CI

Just before the commit, the suite ran once more on the tree as committed: `Ran 329 tests in
104.497s`, `OK (skipped=1)`, no Ray process before or after; `black --check runregistrykit docs`, 31
files. Nothing was pushed. The new test first runs on Linux, at 3.12.15
(`core`, `suite (low)`) and at 3.13.16 (`suite (high)`). **The review is to read its result
there.**

## The deliberate-breakage record

Each diff below was generated in `agent-02c/new`, a scratch clone holding this tree, after `black`.
Each was replayed there **as recorded below**, in `bash`, by a script:
- `git apply --check`, then `git apply`;
- `python -m unittest runregistrykit.tests.test_status_writes` (22 tests) at 3.12.15, and for (m1)
  at 3.13.16 too, with `PYTHONPATH` on the clone;
- `git apply -R --check`, then `git apply -R`.

After each, the clone's `git status --short` was empty. This checkout was never mutated. No Ray
process before or after.

| # | Mutation | Run | Failing (the new test's subtests; attempt #, line, offset) |
|---|---|---|---|
| (m1) | the first filter back to `2959b78`'s list comprehension | 3.12.15: `Ran 22 tests in 14.842s`, `FAILED (failures=3)`. 3.13.16: `Ran 22 tests in 13.494s`, `FAILED (failures=3)` | 3.12: (1) **1 of 3**, #51 `:366` 280; (2) **2 of 7**, #51, #229; (3) **3 of 12**, #51, #229, #598. 3.13: the same at offset 284 (#52, #232, #599) |
| (m2) | the second filter back to its list comprehension, the first kept | `Ran 22 tests in 14.117s`, `FAILED (failures=1)` | (3) alone: **1 of 12**, #664 `:373` offset 398 |
| (m3) | the first filter a `for` loop with an `if` | `Ran 22 tests in 13.665s`, `FAILED (failures=3)` | (1) **1 of 3**, #49 `:368` (the `if`) offset 276; (2) **2 of 7**, #49, #226; (3) **3 of 12**, #49, #226, #594 |
| (m4) | the agent's own: the first filter a **set** comprehension, `sorted({…})` | `Ran 22 tests in 13.955s`, `FAILED (failures=3)` | (1) **1 of 3**, #52 `:366` offset 290; (2) **2 of 7**, #52, #233; (3) **3 of 12**, #52, #233, #605 |

At every failing attempt the in-flight entry was left and the lock held, freed by one release. No
other test failed under any mutation. (m4) shows that an inlined set comprehension with a filter
has the gap too, as §2.2 says of every comprehension.

### The diffs

#### (m1)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 57f820d..8567ed7 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -363,7 +363,7 @@ def _write_status(path, fields) -> dict:
         try:
             book["in_flight"][number] = dict(fields)
             # generators: a handler raising at a comprehension or loop filter leaves the lock held
-            earlier = list(n for n in sorted(book["in_flight"]) if n < number)
+            earlier = [n for n in sorted(book["in_flight"]) if n < number]
             landed, payload = _newest_landed(book)
             if earlier and payload is not None:
                 # a handler has re-entered a write: the file may hold what that write read. The
```

#### (m2)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 57f820d..5ead44d 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -370,7 +370,7 @@ def _write_status(path, fields) -> dict:
                 # newest landed payload already holds the fields of every in-flight write older
                 # than it, and may have set the same keys since, so only the newer are applied
                 status = copy.deepcopy(payload)
-                earlier = list(n for n in earlier if n > landed)
+                earlier = [n for n in earlier if n > landed]
             else:
                 status = read_json(path) or {}
             for n in earlier:
```

#### (m3)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 57f820d..9cf0025 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -363,7 +363,10 @@ def _write_status(path, fields) -> dict:
         try:
             book["in_flight"][number] = dict(fields)
             # generators: a handler raising at a comprehension or loop filter leaves the lock held
-            earlier = list(n for n in sorted(book["in_flight"]) if n < number)
+            earlier = []
+            for n in sorted(book["in_flight"]):
+                if n < number:
+                    earlier.append(n)
             landed, payload = _newest_landed(book)
             if earlier and payload is not None:
                 # a handler has re-entered a write: the file may hold what that write read. The
```

#### (m4)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 57f820d..c6d1286 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -363,7 +363,7 @@ def _write_status(path, fields) -> dict:
         try:
             book["in_flight"][number] = dict(fields)
             # generators: a handler raising at a comprehension or loop filter leaves the lock held
-            earlier = list(n for n in sorted(book["in_flight"]) if n < number)
+            earlier = sorted({n for n in sorted(book["in_flight"]) if n < number})
             landed, payload = _newest_landed(book)
             if earlier and payload is not None:
                 # a handler has re-entered a write: the file may hold what that write read. The
```

## Observations not acted on

1. **The 3.14 `with` point stays**, as L11 (a) decides. It is recorded in `_update`'s docstring and
   in the narrowed entry. A real signal hit it once in 13 948 interruptions here, at offset 26. The
   sweep cannot model it: an `INSTRUCTION` event fires before an instruction, and this point
   follows the `CALL` of `__enter__`.
2. **Uncovered `JUMP_BACKWARD`s outside `_write_status`**: the generator expressions' own,
   `_land_status`'s prune loop and `_newest_landed`'s loop, at every version and at `2959b78` too
   (§4; deviation 9). None can leave the lock held, by reading, and the new test attempts every one
   a write reaches. No issue opened.
3. **The core run's editable install rewrote the ignored `runregistrykit.egg-info/`** in this
   checkout (its files' mtimes moved). It is ignored and not staged; 02b's run did the same.
4. **02's and 02b's other observations stand**: a fork made while the lock is held; a raise inside
   the `finally`; the bookkeeping lasting the process.

## State handed to the next prompt

- **The interface after 02c:**
  - the writer's filters are generator expressions (`runregistrykit/__init__.py:366`, `:373`) in
    `_write_status` (`:352`);
  - the `with _STATUS_LOCK:` (`:355`) and the `finally` (`:382-383`) are unchanged;
  - `_update`'s docstring (`:726-766`) names the 3.14 `with` point (`:763-765`);
  - `write_json_atomic` (`:247-256`) and `status.json`'s keys and values are unchanged.
- **The sweep:** `test_status_writes.TestARaisingHandlerAtEveryJump`, in a child, in under a second
  of attempts. It finds the writer's code by the section's bounds, as 02b's does, so a function or
  generator added to the section is swept.
- **For 03:** `list_runs` (`:1129`, its status read `:1159`) and `liveness` (`:595`, the empty
  payload `:619`) are as they were.
- **The issue** `[02b-a-raising-handler-can-leave-the-status-lock-held]` is open, narrowed to 3.14,
  with no owner.
- **CI:** the push is the user's. The new test first runs on Linux, and at 3.13.16 in `suite
  (high)`.
- The suite is 329, with one skip on macOS (the Linux readers).
