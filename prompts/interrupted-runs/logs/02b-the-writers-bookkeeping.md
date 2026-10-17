# Log — prompt 02b: the writer's bookkeeping

**Subject:** Apply only newer in-flight writes, and never lower the landed record
**Commit:** this commit (on `main`, after `201e507`)
**Date:** 2026-10-17
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1–15). It stopped once, on (m3), and was resumed with
the user's decision of 2026-10-17 (deviation 4).
**Result:** **landed.**
- A re-entered write that composes from the newest landed payload applies only the in-flight
  writes numbered **above** that payload's number. Both measured cases now end `stage` `B` and
  `killed`.
- The record of what landed is a dict from sequence number to payload. The newest is its highest
  key. A write takes its deep copy, checks for a later write, records itself with one store, and
  prunes the lower keys over a snapshot. A handler that lands a later write at any instruction of
  this leaves its higher key in place, so the record is never lowered.
- A write's sequence number is now taken by one call, `next()` on a per-book `itertools.count`
  (deviation 2).
- Every un-re-entered write is as 02 wrote it: one read, one write, one `os.replace`, the same
  keys, mode and name. `write_json_atomic`, `stores.py` and `__main__.py` are not touched.
- The suite is **322 → 328**: 6 new tests in `test_status_writes`, all core. Two of them are
  sweeps that run a handler at every instruction the writer executes, by `sys.monitoring`, in
  eight modes. The 15 existing tests are unchanged.
- The core alone, in a scratch venv without `[stores]`, runs 86 tests (80 + 6), OK, with one skip.
- The twelve real-signal cases all end `killed`, 143, `units_done` 7, as at `2bf9c72`.
- (m1), (m2), (m3′), (m4) and (m5) each fail tests. (m3) fails none: under the by-number record it
  changes nothing. That was a stop, and the user took (A) (deviation 4).
- Both issues are closed and nothing is opened, so `docs/OPEN_ISSUES.md` counts **8**.
- **Nothing pushed, no tag made, no workflow dispatched.** The sweeps first run on Linux and on
  3.13 in CI (below).

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | The writer section and `Run._update`'s docstring only. `_STATUS_WRITES`'s comment (`:267-273`) now describes the record by number. A new helper, `_newest_landed` (`:294`). `_land_status` (`:308`): its discard check reads the newest through the helper (`:333`); after the replace it takes its deep copy (`:340`), then checks (`:341-344`, the put-back and its early `return`, kept), then makes one store (`:346`), then prunes over `list(landed)` (`:347-349`); its docstring gains a paragraph. `_write_status` (`:352`): the book is `{"numbers": itertools.count(), "in_flight": {}, "landed": {}}` (`:356-359`); the number is `next(book["numbers"])` (`:362`); `earlier` comes from `sorted(book["in_flight"])` (`:365`); the base is read through the helper (`:366`); a landed base keeps only `earlier` numbered above it (`:372`). `Run._update` (`:724-764`): the merge and the record stated, and the 121-character line rewrapped |
| `runregistrykit/tests/test_status_writes.py` | Additions only: four imports (`itertools`, `shutil`, `time`, `types`), then from `:491` the helpers and three classes. 6 tests (below) |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: `stores.py`, `__main__.py`, `client.py`, `pyproject.toml`, `.github/` (the core job
already names `test_status_writes`), `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption/`,
any other test module or fixture, the prompt, the campaign README and `orchestrator/`. In
`__init__.py`, `git diff 2bf9c72` has six hunks: five in the writer section (`:265-382` as
committed) and one in `_update`'s docstring. `write_json_atomic` (`:247-256`) is byte for byte as it
was, with its `<path>.tmp` (`:250`), its `os.replace` (`:256`) and its place in `__all__` (`:101`).
The test file's diff against `2bf9c72` removes no line.

### The writer

Under `_STATUS_LOCK`, `_write_status`:

1. takes the book for `os.path.realpath(path)` (`:357`), then a number with
   `next(book["numbers"])` (`:362`), and, as the first statement of its `try`, registers
   `dict(fields)` as in flight (`:364`);
2. composes. `earlier` is every in-flight number below its own, from `sorted(book["in_flight"])`
   (`:365`; `sorted` takes a snapshot of the keys in one C call). The newest landed number and
   payload come from `_newest_landed` (`:366`).
   - **If `earlier` is non-empty and a payload has landed**, a handler has re-entered a write. The
     base is a deep copy of that payload, and `earlier` keeps only the numbers above it (`:372`).
   - **Otherwise** the base is `read_json(path) or {}`, and every earlier write is applied, as in
     02.

   Then the kept in-flight fields are applied in order, then its own fields, then the heartbeat
   stamp;
3. calls `_land_status`, returns the payload, and in its `finally` removes its in-flight entry.

`_land_status` writes the temporary file as 02 did. Then:
- **The discard.** If `_newest_landed(book)[0] > number` (`:333`), it removes its file and returns.
  Otherwise it calls `os.replace`.
- **The record.** After the replace:
  - `recorded = copy.deepcopy(payload)` (`:340`);
  - if the newest landed number is higher than its own (`:341-342`), it puts that payload back under
    that number (`:343`) and returns (`:344`);
  - otherwise it stores `landed[number] = recorded` (`:346`), then pops every key below its number,
    iterating `list(landed)` (`:347-349`).

`_newest_landed(book)` (`:294`) is `max(landed, default=-1)` and `landed.get(number)`. If a
handler's prune removed that key between the two reads, it reads again.

**The shape is the prompt's §2.3 shape** (correction 8). It keeps the record's property because:
- every store adds a key, and only keys below the one just stored are ever removed;
- a handler's write lands with a higher number than every write it interrupts, so the store that a
  handler interrupts cannot hide the handler's key, and nor can that write's prune.

### The tests

From `runregistrykit/tests/test_status_writes.py:491`, all core:

| Class | Tests | What |
|---|---:|---|
| `TestTwoHandlerWritesInsideOne` (`:522`) | 3 | The cases 02's review measured, with `json.dump` patched to fire once (`made_inside`, built on 02's `Interruption` at half written; the inner writes go through the real function). `heartbeat(units_done=7, stage="A")` with a handler's `heartbeat(stage="B")`, then `finish("killed", 143)`: `killed`, 143, `units_done` 7, `stage` **B**, `pid` and `host` as begun, nothing left behind. `finish("done", exit_code=0)`, after a `heartbeat(units_done=7, …)`, with a handler's `finish("killed", 143)`, then `heartbeat()`: `killed`, 143, the heartbeat's fields, nothing left. The same with the one handler write: the same ending |
| `TestAPutBackThenALaterReenteredWrite` (`:562`) | 1 | (o2): a heartbeat whose replace is preceded by a returning handler's `finish("killed", 143)`. There are exactly three replaces onto `status.json` (the handler's, the heartbeat's, the put-back), and the end is `killed` with the heartbeat's fields. Then a `heartbeat(units_done=8)` whose `json.dump` makes a handler's `heartbeat()` ends `killed`, 143, `units_done` 8, nothing left |
| `TestAHandlerAtEveryInstruction` (`:920`) | 2 | The sweeps, below |

**The sweeps.** Each test starts a child process (`SWEEPER`, `:906`), which runs
`sweep_in_this_process` (`:829`) and prints a JSON report. The test asserts on that report. The
child is never signalled, and it runs under a 540 s timeout (`SWEEPER_TIMEOUT`).

In the child:
- **Setup.** A run is begun under the test's runs root. `the_writers_code()` (`:608`) finds every
  function the writer's section defines: those in `runregistrykit/__init__.py` whose first line
  lies between the section's opening comment and the next `# =====` rule. It adds every code object
  nested in one, through `co_consts`, recursively.
- **Monitoring.** `Instructions` (`:667`) takes the first free `sys.monitoring` tool id of 0–5,
  failing if none is free. It sets `INSTRUCTION` events on those code objects only, with
  `set_local_events`. Its `close`, run from `__exit__` and on a failed setup, clears the events,
  unregisters the callback and frees the id in a `finally`.
- **The callback.** It ignores everything while no attempt is active, while the handler runs and
  after the handler has fired. It never returns `DISABLE`. In the raising modes the handler's
  `SystemExit` propagates from the instruction (correction 4).
- **The four modes** (`MODES`, `:600`). The handler calls `finish("killed", exit_code=143)`, alone
  or followed by `heartbeat()`, then returns or raises `SystemExit(143)`.
- **The attempts.** Per mode, one uninterrupted write counts the instructions (bounded by
  `MOST_INSTRUCTIONS`, 2000). Then one attempt runs per instruction. Each is made on a fresh run:
  `shutil.copytree` of the begun run's directory to a new name (a new real path, so a book of its
  own), then one plain `heartbeat()`, so the book has a landed record as `begin` leaves one. The run
  is removed after the attempt.
- **The checks.** At each attempt: the handler ran; the write returned, or raised `SystemExit(143)`
  in a raising mode; and the judge's checks hold. The sweep of a mode stops, and fails, past
  `SWEEP_SECONDS` (120 s).
- **The heartbeat sweep** (`judge_a_heartbeat`, `:786`): after the interrupted
  `heartbeat(units_done=7)`, the file parses, says `killed`, 143, and no `status.json.*.tmp` is
  left. Then a later `heartbeat(units_done=8)` whose `json.dump` makes a handler's `heartbeat()`
  returns, and leaves `killed`, 143 and `units_done` 8.
- **The finish sweep** (`judge_a_finish`, `:806`): after the interrupted
  `finish("done", exit_code=0)`, the file is `killed`, 143, with nothing left. There is one
  exception, taken only where the handler returns. Inside the handler, `seen_by_the_handler`
  (`:761`) reads, without changing anything, whether the interrupted write's fields are in the
  book's `in_flight`, or whether the file already says `done`. Where neither holds, the handler's
  write is the earlier one, and `done`, 0 is accepted, and counted.

The book is read nowhere else by a test (correction 6).

## Deviations from the prompt

Each classified. Corrections 1–15 are section 0's.

1. **(m3) is not caught by any test, and is recorded as a mutant that changes nothing under this
   shape.** The prompt says "The early `return` after a put-back stays, and is pinned (§2.5)",
   and §5 makes an uncaught mutation a stop. The agent stopped. With (m3) applied, the three
   modules ran `Ran 78 tests … OK (skipped=1)`, and both sweeps found 0 wrong instructions in all
   eight modes (the deliberate-breakage record).
   - **Why.** Under the by-number record, falling through after a put-back stores the overtaken
     write's lower number beside the put-back's higher one, and prunes keys below that. The
     highest key is never lowered. The only effect is a dead entry, which the next write's prune
     removes. Measured in scratch: after (o2)'s put-back the record is `{2: killed}`, and under
     (m3) it is `{2: killed, 1: running}`. After the next write both are `{3: killed}`.
   - **Any shape with the property makes the `return` redundant.** A store that falls through
     after a put-back and lowers the record would also be lowered by a handler landing between the
     check and the store.
   - **The user's decision (2026-10-17): (A).** Record (m3) as such, with the run as evidence, keep
     the `return`, and add (m3′): the put-back's re-landing call removed, the `return` kept. The
     record's property is pinned instead by the heartbeat sweep's later re-entered heartbeat,
     which catches (m2) and (m5). **STRUCTURALLY REQUIRED.**
2. **The sequence number is taken by `next(book["numbers"])`**, on an `itertools.count` in the
   book, not by 02's `number = book["next"]; book["next"] = number + 1`.
   - **The cause.** The new merge skips an in-flight write numbered at or below the landed base, so
     it needs numbers to be unique. Read-then-increment is not: a handler between the read and the
     increment takes the same number, and the interrupted write then sets `next` back below a
     number the handler's second write used.
   - **Measured** on this tree with read-then-increment and the sweep's `units_done` 8 check. In the
     "finish, then heartbeat" mode, returning, 7 instructions (`_write_status` lines 360–361 at the
     time, the read through the increment) end with the later re-entered heartbeat's `units_done`
     lost. The state stays `killed`. With `next()`, none.
   - The prompt's "At writing" found read-then-increment harmless for the state, which holds; it did
     not check the later write's fields. 2bf9c72's merge, which applies every earlier write, did
     not need the uniqueness. **STRUCTURALLY REQUIRED.**
3. **The sweeps run in a child process the test starts.** The child is never signalled.
   - **The cause.** Run in the test process, a raising handler at some instructions left
     `_STATUS_LOCK` held by the main thread. `TestTwoThreads.test_a_heartbeat_thread_and_a_finish`
     then failed: "the thread never got going".
   - **What it is.** These are instructions at which the interpreter itself never raises, and its
     exception table does not cover them (observation 1). An exception that a monitoring callback
     raises there leaves the frame without the `with` statement's `__exit__`.
   - In a child, what such an attempt leaves (the lock held, the interrupted write's in-flight
     entry kept) ends with the child. Each attempt's run is still a fresh book. **STRUCTURALLY
     REQUIRED.**
4. **(m3′) added**, at the user's decision of 2026-10-17 (deviation 1). **STRUCTURALLY
   REQUIRED.**
5. **The suite's time** (correction 1). Every suite run was in the foreground with a timeout of at
   least 600 s, its output in a file, the verdict grepped from it: 110.431 s before, 119.142 s on
   the final package tree, and 125.237 s on the tree as committed. The module alone takes 16.936 s,
   and the sweep class alone 14.167 s, well under 60 s. **STRUCTURALLY REQUIRED.**
6. **The core run** (correction 2): `uv venv -p /opt/local/bin/python3.12` and `uv pip install
   --offline -e` of this checkout, in `agent-02b/core`, with `TMPDIR` in the scratchpad. Removed
   afterwards. **STRUCTURALLY REQUIRED.**
7. **Nested code objects** (correction 3). The sweep sets events on every code object reachable
   through `co_consts`, recursively.
   - **The new writer has none.** Its two list comprehensions are inlined at 3.12 and 3.13 (PEP 709),
     and the 02 generator expression is gone: `earlier` is built from `sorted(book["in_flight"])`,
     a snapshot, rather than a generator over the live dict. The code objects swept are
     `_status_temporary_name`, `_remove_quietly`, `_newest_landed`, `_land_status` and
     `_write_status`.
   - **At `2bf9c72`** the sweep also covers `<genexpr>:336`, with 10 instructions in each write.
     None of them raised a `RuntimeError`. The 49 genexpr points in the two-write finish modes end
     `done` by the merge, which §2.2 removes.
   - **STRUCTURALLY REQUIRED**; the snapshot is an **IMPLEMENTATION CHOICE**.
8. **The sweep's handler runs from the callback, and raises from it** (correction 4). The callback
   never returns `DISABLE`, and `close` runs however the block ends. The sweep is not measured on
   3.13.16. **STRUCTURALLY REQUIRED.**
9. **What the sweep does not reach** (correction 5): instructions inside `json.dump`,
   `copy.deepcopy`, `read_json`, `now_iso`, `os.fsync`, `max`, `sorted` and the dict methods. A
   handler inside one of them sees the bookkeeping as at the `CALL` before it, which the sweep
   reaches. A real signal's handler runs only at eval-breaker checks, a subset of instruction
   boundaries. **STRUCTURALLY REQUIRED.**
10. **A fresh run per attempt** (correction 6): one `begin` per sweep, then per attempt a
    `copytree` to a new name and one plain `heartbeat()`. The plain write gives the book a landed
    record, as `begin` gives a run begun in this process; without it every re-entered write would
    base on the file, and the record's paths would not be exercised. The book is never cleared or
    edited. It is read in the finish sweep's handler only. **STRUCTURALLY REQUIRED**; the plain
    write is an **IMPLEMENTATION CHOICE**.
11. **The two measured cases and (o2)** (correction 7) use 02's `Interruption`, firing once, and
    assert the whole ending. **STRUCTURALLY REQUIRED.**
12. **No "signal" in the package's new text** (correction 8). The comments and `_update`'s
    docstring say "handler" and "interrupt". §3.3's grep finds `finish`'s docstring only, now
    `:796`. **STRUCTURALLY REQUIRED.**
13. **`_update`'s line of 121 characters** is rewrapped (correction 9). The four other lines over
    100 characters, now `:653`, `:860`, `:904` and `:913` (101, 101, 101, 103 characters; `:620`,
    `:819`, `:863`, `:872` at `2bf9c72`), are left alone. **STRUCTURALLY REQUIRED.**
14. **`black --check runregistrykit docs`**: 31 files (correction 10). **STRUCTURALLY
    REQUIRED.**
15. **Line citations** (correction 11) in this log and on the board were taken with `grep -n` from
    the files as committed, and re-checked before committing. The board's §3 entries for 03, 04 and
    05 gain a "Package lines (02b, this commit)" sentence. **STRUCTURALLY REQUIRED.**
16. **Mutation diffs** (correction 12) were taken after `black`, in a scratch clone holding this
    tree. The blob of `runregistrykit/__init__.py` is `009bec9` in both. **STRUCTURALLY
    REQUIRED.**
17. **The sweeps against `2bf9c72`** (correction 13): the new test file copied into a scratch clone
    of `2bf9c72`. Every new test runs there; none errors. **STRUCTURALLY REQUIRED.**
18. **The board's Orchestrator notes line** is not edited (correction 14). **STRUCTURALLY
    REQUIRED.**
19. **`var/`** (correction 15) is not touched. `var/ledger.jsonl`'s SHA-256 is `471d0859…` before
    and after. **STRUCTURALLY REQUIRED.**
20. **The finish sweep's exception is narrower than §2.5's.** It accepts `done` only where the
    interrupted write's fields are not in flight **and** the file does not already say `done`. The
    points after the write's `finally` has removed its entry, where it has landed and the handler's
    write is the later one, must then be `killed`. **IMPLEMENTATION CHOICE.**
21. **The heartbeat sweep also checks the later heartbeat's `units_done`**, beyond "leaves
    `killed`". It is what found deviation 2. **IMPLEMENTATION CHOICE.**
22. **The (o2) test also counts three replaces**, so that the put-back is shown to have happened,
    not assumed. **IMPLEMENTATION CHOICE.**
23. **The sweep finds the writer's functions by the section's bounds in the source file**, not by a
    list of names. So it runs unchanged against `2bf9c72`, and a function added to the section is
    swept without editing the test. It asserts that `_write_status` and `_land_status` are among
    them. **IMPLEMENTATION CHOICE.**
24. **A first draft cited an issue by its board name in a test docstring.**
    `test_package_is_generic.TestThePackageNamesNoClient.test_no_citation` failed on it, and the
    docstring was reworded before any record was written. **UNINTENDED DRIFT**, corrected; the final
    suite passes.

## Verification performed

### 1. The state at the start

`HEAD` `201e507`, `main`, clean, the only worktree. `git diff --stat 2bf9c72 HEAD -- runregistrykit
pyproject.toml .github` was empty. `RAY_ADDRESS` was unset. `venv/` has Python 3.12.15 and black
25.1.0. `git status --short --ignored` showed `prompts/.DS_Store`, `runregistrykit.egg-info/`, both
`__pycache__/`, `var/` and `venv/`, before and after every run. The §3.3 grep found `:755` only.

### 2. The suite, before and after

`TMPDIR=<agent-02b>/tmp ./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from
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
| `test_status_writes` | 15 | **21** |
| `test_store_amend` | 21 | 21 |
| `test_store_amend_residuals` | 9 | 9 |
| `test_store_command_line` | 2 | 2 |
| `test_store_copy_move` | 27 | 27 |
| `test_store_fingerprint` | 29 | 29 |
| `test_store_retire` | 41 | 41 |
| `test_store_retire_references` | 10 | 10 |
| `test_store_sidecar` | 17 | 17 |
| **total** | **322**, `Ran 322 tests in 110.431s`, `OK (skipped=1)` | **328**, `Ran 328 tests in 119.142s`, `OK (skipped=1)` |

N = 6. The skip is `test_host`'s Linux readers, as before. The 15 tests that existed at `2bf9c72`
are unchanged: the diff of the module removes no line. The final suite was run again on the tree as
committed (§9).

### 3. The core alone

In `agent-02b/core`, built as correction 2. `importlib.util.find_spec` found none of
`datastorekit`, `ray` or `sqlalchemy`. From the repository root:

```
python -m unittest runregistrykit.tests.test_run_registry runregistrykit.tests.test_public_names runregistrykit.tests.test_host runregistrykit.tests.test_status_writes
Ran 86 tests in 24.741s
OK (skipped=1)
```

29 + 8 + 28 + 21. Importing `test_status_writes` there under `-I` loaded none of the three. The venv
was removed afterwards.

### 4. Nothing outside temporary directories

`git status --short --ignored` was the same before and after every run. The sweeps' children write
under the test's `tempfile` runs root, and remove each attempt's copy. `git grep -n 'signal' --
'runregistrykit/*.py' ':!runregistrykit/tests'` finds `runregistrykit/__init__.py:796` only, and
`git grep -n 'SIGTERM\|signal\.' -- runregistrykit ':!runregistrykit/tests'` finds nothing. No
`import signal` and no `tempfile` in the package. The sweep sends no signal. The real-signal
children of `TestARealSignal` and of the probe signal only themselves.

### 5. 02's real-signal probe, written again

`agent-02b/probe/signal/`, not committed: a child per case that begins a run, installs a `SIGTERM`
handler calling `run.finish("killed", exit_code=128 + signum)`, and sends itself `SIGTERM` from
inside a heartbeat (`units_done=7`) at one of four points: inside `json.dump` with half the payload
written or all of it; inside `os.replace` before the real replace or after it. The handler then
raises `SystemExit`, returns, or restores `SIG_DFL` and kills its own process. Against this tree:

| Point | Handler | Exit | Heartbeat | Parses | `state` | `exit_code` | `units_done` | stage kept | Left behind |
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

What is left behind is the documented `status.json.<unique>.tmp`, of the heartbeat that the process
died inside. Against `2bf9c72`'s writer, in the scratch clone, the twelve rows are identical. No
child was left (`pgrep -lf probe/signal/child.py`, exit 1).

### 6. The sweeps, on this tree and against `2bf9c72`

Measured in children, by `agent-02b/probe/report.py`, which runs the test module's `SWEEPER` and
prints its report.

**This tree.** 323 instructions per write: `_write_status` 104, `_land_status` 118,
`_newest_landed` 78, `_status_temporary_name` 23, `_remove_quietly` 0 (it runs only on an exception,
so never in an uninterrupted write).

| Sweep | Handler | Ending | Instructions | Wrong | `done` accepted | Seconds |
|---|---|---|---:|---:|---:|---:|
| heartbeat | finish | returns | 323 | 0 | — | 1.361 |
| heartbeat | finish | raises | 323 | 0 | — | 1.295 |
| heartbeat | finish, then heartbeat | returns | 323 | 0 | — | 1.391 |
| heartbeat | finish, then heartbeat | raises | 323 | 0 | — | 1.246 |
| finish | finish | returns | 323 | 0 | 24 | 1.052 |
| finish | finish | raises | 323 | 0 | 0 | 0.967 |
| finish | finish, then heartbeat | returns | 323 | 0 | 24 | 1.170 |
| finish | finish, then heartbeat | raises | 323 | 0 | 0 | 0.925 |

The 24 accepted points are instructions 1–24 of the interrupted `finish`: from the first
instruction of `_write_status` to the `CALL` of `next(book["numbers"])` (`:362`). A handler there
takes the lower number, and `done` landing last is right. Each child, with its begin, took 4–6 s.

**`2bf9c72`'s writer**, with the new test file in the scratch clone. 212 instructions per write:
`_write_status` 93, `<genexpr>:336` 10, `_land_status` 86, `_status_temporary_name` 23.

| Sweep | Handler | Ending | Wrong | `done` accepted | What goes wrong |
|---|---|---|---:|---:|---|
| heartbeat | finish | returns | **15** | — | instructions 180–194, `_land_status` line 318 (3) and line 321 (12): `running` after the later re-entered heartbeat |
| heartbeat | finish | raises | 0 | — | |
| heartbeat | finish, then heartbeat | returns | **15** | — | the same 15 |
| heartbeat | finish, then heartbeat | raises | 0 | — | |
| finish | finish | returns | 0 | 28 | |
| finish | finish | raises | 0 | 0 | |
| finish | finish, then heartbeat | returns | **167** | 21 | `done`, 0 |
| finish | finish, then heartbeat | raises | **167** | 0 | `done`, 0 |

These agree with the prompt's "At writing" where it measured the same thing: the same 15 heartbeat
points (`:318` to `:321`'s `copy.deepcopy`) of 202. 202 is 212 without the genexpr's 10, which the
planner did not sweep (correction 3). With two handler writes, 188 and 167 points end other than
`killed`, the planner's 178 and 157 plus the genexpr's 10. **Not reconciled:** the planner's 43
(returning) and 7 (raising) for a `finish` with one handler write. Here that mode has no wrong
point and 28 accepted. The planner's harness is not in the prompt.

Running `test_status_writes` in that clone: `Ran 21 tests in 13.171s`, `FAILED (failures=6)`.
- **Failing:** `TestTwoHandlerWritesInsideOne.test_a_heartbeat_then_a_finish_inside_a_heartbeat`
  (`'A' != 'B'`); `test_a_finish_then_a_heartbeat_inside_a_finish` (`'done' != 'killed'`);
  `TestAHandlerAtEveryInstruction.test_an_interrupted_heartbeat` [finish, returns; finish then
  heartbeat, returns: 15 each]; `test_an_interrupted_finish` [finish then heartbeat, returns and
  raises: 167 each, 21 more accepted when returning].
- **Passing there:** `test_a_finish_inside_a_finish` and
  `TestAPutBackThenALaterReenteredWrite`, since `2bf9c72` keeps the `return`.

No test errored there.

### 7. `black`

`./venv/bin/black --check runregistrykit docs`: "31 files would be left unchanged". The two Python
files were formatted with `./venv/bin/black` first.

### 8. CI

Nothing was pushed. The sweeps first run on Linux, on 3.12.15 (`suite (low)`, `core`) and on
3.13.16 (`suite (high)`). **The review is to read their result there.** The sweep is not measured on
3.13 here: instruction counts, exception-table gaps and comprehension inlining may differ there,
while the property asserted should not.

### 9. The final tree

The suite was run once more on the tree as committed, just before the commit: `Ran 328 tests in
125.237s`, `OK (skipped=1)`. `black --check runregistrykit docs`: 31 files. No Ray process before
or after. `git status --short --ignored` was unchanged by it.

## The deliberate-breakage record

Each diff below was generated in a scratch clone (`agent-02b/new`) holding this tree, after
`black`. Each was replayed there **as recorded below**, in `bash`, by a script: `git apply --check`,
`git apply`, then `test_status_writes`, `test_run_registry` and `test_host` (78 tests), then
`git apply -R --check` and `git apply -R`. `PYTHONPATH` was the clone, so that the tests and their
children ran it. After each, the clone's `git status --short` was empty. This checkout was never
mutated. `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` found nothing before and after
each run.

| # | Mutation | Run | Failing tests (subtests in brackets) |
|---|---|---|---|
| (m1) | the merge applying every earlier in-flight write again (02's step 2) | `Ran 78 tests in 27.966s`, `FAILED (failures=4, skipped=1)` | `TestAHandlerAtEveryInstruction.test_an_interrupted_finish` [finish then heartbeat, returns: **281 of 323**; raises: **281 of 323**]; `TestTwoHandlerWritesInsideOne.test_a_finish_then_a_heartbeat_inside_a_finish`; `test_a_heartbeat_then_a_finish_inside_a_heartbeat` |
| (m2) | the record a single number and payload again, set after the deep copy (02's step 6) | `Ran 78 tests in 21.732s`, `FAILED (failures=2, skipped=1)` | `TestAHandlerAtEveryInstruction.test_an_interrupted_heartbeat` [finish, returns: **24 of 244**; finish then heartbeat, returns: **24 of 244**], `running` after the later re-entered heartbeat |
| (m3) | the early `return` after a put-back removed (02's review, (o2)) | `Ran 78 tests in 23.407s`, **`OK (skipped=1)`** | **none**: a mutant that changes nothing under the by-number record (deviation 1). Both sweeps: 0 wrong in all eight modes |
| (m3′) | the put-back's re-landing call removed, the `return` kept (the user's, 2026-10-17) | `Ran 78 tests in 22.892s`, `FAILED (failures=8, skipped=1)` | `TestAHandlerAtEveryInstruction.test_an_interrupted_heartbeat` [finish, returns: **17 of 323**; finish then heartbeat, returns: **17 of 323**]; `test_an_interrupted_finish` [finish, returns: **17 of 323**; finish then heartbeat, returns: **17 of 323**]; `TestAPutBackThenALaterReenteredWrite.test_the_terminal_state_is_kept_throughout` (2 replaces, not 3); `TestAHandlerInsideAHeartbeat.test_each_point_each_ending` [before the replace, returns]; `TestASecondRunObject.test_before_the_replace`; `TestAHandlerDuringThePutBack.test_a_second_handler_inside_the_put_back` |
| (m4) | the prune iterating the live dict, not a snapshot | `Ran 78 tests in 23.445s`, `FAILED (failures=4, skipped=1)` | `TestAHandlerAtEveryInstruction.test_an_interrupted_heartbeat` [finish, returns; finish then heartbeat, returns: **21 of 334** each]; `test_an_interrupted_finish` [the same two modes: **21 of 334** each]; each `raised RuntimeError: dictionary changed size during iteration` |
| (m5) | the agent's own: the prune removing every number but its own, not only the lower | `Ran 78 tests in 25.198s`, `FAILED (failures=2, skipped=1)` | `TestAHandlerAtEveryInstruction.test_an_interrupted_heartbeat` [finish, returns; finish then heartbeat, returns: **22 of 323** each], `running` after the later re-entered heartbeat |

Notes:
- Under (m4) the raising modes pass: the handler's `SystemExit` leaves the comprehension before the
  dict's next step. A mutation changes the instruction count, so each count is over that tree's
  instructions.
- Under (m3) the scratch probe of deviation 1 shows the dead entry, `{2: killed, 1: running}` after
  the put-back, and `{3: killed}` after the next write, as without it.
- No existing test changed.

### The diffs

#### (m1)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 009bec9..4e963dc 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -369,7 +369,6 @@ def _write_status(path, fields) -> dict:
                 # newest landed payload already holds the fields of every in-flight write older
                 # than it, and may have set the same keys since, so only the newer are applied
                 status = copy.deepcopy(payload)
-                earlier = [n for n in earlier if n > landed]
             else:
                 status = read_json(path) or {}
             for n in earlier:
```

#### (m2)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 009bec9..8ef09c8 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -295,14 +295,7 @@ def _newest_landed(book) -> tuple:
     """The number and payload of the newest write landed for ``book``, or `(-1, None)` if none
     has. A handler's write that prunes the number read here before its payload is read makes it
     read again, so a number is never returned without its payload."""
-    landed = book["landed"]
-    while True:
-        number = max(landed, default=-1)
-        if number < 0:
-            return number, None
-        payload = landed.get(number)
-        if payload is not None:
-            return number, payload
+    return book["landed"], book["payload"]
 
 
 def _land_status(path, book, number, payload) -> None:
@@ -337,16 +330,11 @@ def _land_status(path, book, number, payload) -> None:
     except BaseException:
         _remove_quietly(name)
         raise
-    recorded = copy.deepcopy(payload)
     newest, newest_payload = _newest_landed(book)
     if newest > number:
         _land_status(path, book, newest, newest_payload)
         return
-    landed = book["landed"]
-    landed[number] = recorded
-    for n in list(landed):
-        if n < number:
-            landed.pop(n, None)
+    book["landed"], book["payload"] = number, copy.deepcopy(payload)
 
 
 def _write_status(path, fields) -> dict:
@@ -355,7 +343,7 @@ def _write_status(path, fields) -> dict:
     with _STATUS_LOCK:
         book = _STATUS_WRITES.setdefault(
             os.path.realpath(path),
-            {"numbers": itertools.count(), "in_flight": {}, "landed": {}},
+            {"numbers": itertools.count(), "in_flight": {}, "landed": -1, "payload": None},
         )
         # one call, so that a handler cannot take the same number: the merge below skips an
         # in-flight write numbered at or below the landed payload's, which a shared number breaks
```

#### (m3)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 009bec9..4e82a76 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -341,7 +341,6 @@ def _land_status(path, book, number, payload) -> None:
     newest, newest_payload = _newest_landed(book)
     if newest > number:
         _land_status(path, book, newest, newest_payload)
-        return
     landed = book["landed"]
     landed[number] = recorded
     for n in list(landed):
```

#### (m3′)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 009bec9..21367a5 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -340,7 +340,6 @@ def _land_status(path, book, number, payload) -> None:
     recorded = copy.deepcopy(payload)
     newest, newest_payload = _newest_landed(book)
     if newest > number:
-        _land_status(path, book, newest, newest_payload)
         return
     landed = book["landed"]
     landed[number] = recorded
```

#### (m4)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 009bec9..418d2e5 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -344,9 +344,8 @@ def _land_status(path, book, number, payload) -> None:
         return
     landed = book["landed"]
     landed[number] = recorded
-    for n in list(landed):
-        if n < number:
-            landed.pop(n, None)
+    for n in [n for n in landed if n < number]:
+        landed.pop(n, None)
 
 
 def _write_status(path, fields) -> dict:
```

#### (m5)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 009bec9..c362b11 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -345,7 +345,7 @@ def _land_status(path, book, number, payload) -> None:
     landed = book["landed"]
     landed[number] = recorded
     for n in list(landed):
-        if n < number:
+        if n != number:
             landed.pop(n, None)
 
 
```

## Observations not acted on

1. **Exception-table gaps that the sweep's raising modes reach.** Read, not measured for a real
   signal. The orchestrator measures it in review. No issue opened.
   - **What was measured.** On the 02b draft, in the test process (before deviation 3), a raising
     handler at 7 instructions of `_write_status`, in the mode "finish, raises", left
     `_STATUS_LOCK` held by the main thread. The draft took its number by read-then-increment; its
     offsets were 152 (the `NOP` of `try:`), 240 (a `JUMP_BACKWARD` of the `earlier`
     comprehension's filter), and 598–606 (`SWAP`, three `LOAD_CONST`s and the `CALL` that is the
     `with` statement's normal exit).
   - **Why.** `dis` shows none of these offsets in the code object's exception table. An exception
     a monitoring callback raises there leaves the frame without the `with` statement's `__exit__`,
     and without the `finally` that removes the in-flight entry.
   - **Why a real signal should not reach them.** A Python signal handler runs at eval-breaker
     checks: `RESUME`, `JUMP_BACKWARD` and after a `CALL` returns, among others. The `NOP`, the
     `SWAP` and the `LOAD_CONST`s check none. The `CALL`'s check comes after `__exit__` has released the lock.
     `JUMP_BACKWARD` checks after jumping, and the exception is then attributed to the instruction
     before the jump's target, which the table covers.
   - **Not measured** on 3.13, nor by a real signal at those points. `2bf9c72` has the same `try:`
     and `with`-exit gaps; its genexpr's jump lies in a code object of its own, whose exception
     surfaces at a covered `CALL`.
2. **The sweep is the stronger test, not the same one** (correction 5). Its raising modes raise at
   instructions where nothing in CPython can (observation 1). That is why it runs in a child.
3. **02's documented window holds, and is now exactly the 24 accepted points of the finish sweep.**
   A handler between a write taking its number and registering its fields still loses those fields,
   never the terminal state. The points before the `CALL` of `next()` are where the handler's write
   is the earlier one.
4. **02's other observations stand:** a fork while the lock is held; a raise inside the `finally`
   (now also reachable at the gaps of observation 1, by the sweep only); the bookkeeping lasting the
   process. The record per book is now a dict holding one key after each write's prune.

## State handed to the next prompt

- **The interface after 02b:** `Run._update`'s rule, with the amended merge and a record of what
  landed that is never lowered, in `_write_status` (`runregistrykit/__init__.py:352`),
  `_land_status` (`:308`) and `_newest_landed` (`:294`), and stated in `_update`'s docstring
  (`:724-764`). `write_json_atomic` (`:247-256`) is unchanged, and so are `status.json`'s keys and
  values for every write that is not re-entered.
- **The sweep:** `test_status_writes.TestAHandlerAtEveryInstruction`. It finds the writer's
  functions by the section's bounds, so any function added to the section is swept. It runs in a
  child, in about 14 s here.
- **For 03:** `list_runs` (`:1126`, its status read `:1156`) and `liveness` (`:594`, the empty
  payload `:618`) are as they were.
- **For 06:** the release notes say "`write_json_atomic`: unchanged". `status.json`'s form is not
  changed by 02b.
- **CI:** the push is the user's. The sweeps first run on Linux and on 3.13.16 in the next CI run.
- The suite is 328, with one skip on macOS (the Linux readers).
