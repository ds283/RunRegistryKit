# Prompt 02c — the writer's lock

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 02b has landed and been reviewed (`2959b78`; the review `c18ec34`; CI run `39060913296` green,
  recorded in `9d26357`).
- The user has taken **L11**, the `with` point at Python 3.14 (README §6.2). §2.4 is written for
  (a), the recommendation. Under (b), §2.4's alternative applies. Under any other answer this
  prompt is amended before it runs.
- `git diff --stat 2959b78 HEAD -- runregistrykit pyproject.toml .github` is empty: the package is
  02b's.
- The suite is `Ran 328 tests … OK (skipped=1)` on macOS, and `git status` is clean in this
  repository.
- `/opt/local/bin/python3.13` is 3.13.16 and `/opt/local/bin/python3.14` is 3.14.8, for §3's
  measurements. If 3.13 is missing, that is a stop, because the defect is measured there. If 3.14
  is missing or another version, say so in the log and go on.

**Closes:** `[02b-a-raising-handler-can-leave-the-status-lock-held]` at 3.12 and 3.13. Under L11
(a) it **narrows** that issue to its 3.14 `with` point, which stays open with no owner; under (b)
it closes the issue. **Opens:** only what the work finds.

**Recommended model:** **Opus**. The change is two lines, but the obvious form of it (a loop) has
the same defect, and the test has to reach a branch that only two handler writes inside one write
take.

**Read first:**

1. [`README.md`](README.md): §0, §1 (no signal handling in the package), §5 (all of it; rules 4, 6
   and 10 especially), §6.2 L5 with its amendment, and L11.
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §1's *Orchestrator review of prompt 02b*,
   check 6 and its *CI* paragraph; §3's `[02b-a-raising-handler-can-leave-the-status-lock-held]`
   in full, with its "Measured at writing 02c" paragraph.
3. [`02b-the-writers-bookkeeping.md`](02b-the-writers-bookkeeping.md) §2.5, and
   [`logs/02b-the-writers-bookkeeping.md`](logs/02b-the-writers-bookkeeping.md): deviation 3 and
   "Observations not acted on", 1.
4. `runregistrykit/__init__.py` at `2959b78`: `_write_status` `:352-382` (the `with` `:355`, the
   number `:362`, the two comprehensions `:365` and `:372`, the `finally` `:381-382`), and
   `Run._update`'s docstring `:725-763` (its "Not covered" paragraph `:756-762`).
5. `runregistrykit/tests/test_status_writes.py`, all of it: above all `made_inside` (`:497`),
   `the_writers_code` (`:608`), `Attempt`, `Instructions`, `ending_of`, and the sweeping child
   (`SWEEPER`, `:906`; `TestAHandlerAtEveryInstruction`, `:920`).
6. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

---

## 1. What is wanted

`_write_status` holds `_STATUS_LOCK` in a `with` (`:355`) and removes its in-flight entry in a
`finally` (`:381-382`). Both rely on the function's exception table covering every instruction
between them at which the interpreter can run a signal handler. Two lines break that:

```python
earlier = [n for n in sorted(book["in_flight"]) if n < number]   # :365
earlier = [n for n in earlier if n > landed]                     # :372
```

Each is a list comprehension, which CPython inlines into the function (PEP 709, from 3.12). In the
code compiled for each, the filter's false branch is a `POP_JUMP_IF_TRUE` then a `JUMP_BACKWARD`,
and the table has no entry for either, at 3.12, 3.13 and 3.14 alike (§"At writing"). At 3.13 and
3.14 a pending handler runs **at** that `JUMP_BACKWARD`. A handler that raises there leaves the
function with neither the `finally` nor the `with`'s exit. The lock stays held by the thread that
was writing, and the in-flight entry stays. 3.12 also has the gap, but no real signal was measured
to leave the lock there. 02 had a generator expression at `:365`. That is a code object of its
own, whose exception reaches `_write_status` at a covered `CALL`, so 02 did not have the defect.

Its consequence, measured by 02b's review at 3.13.16: with a handler that records `killed` and
then raises, the file says `killed`, but another thread's `heartbeat` never completes. With that
thread non-daemon, the process did not exit. And every later write in the process composes from
the landed payload rather than the file, since an in-flight entry is always present. SGK's handlers
raise `SystemExit(128 + signum)`. CPBH and SI run 3.13.

So:
- **the writer's two filters become forms whose exception tables are complete** on 3.12 and 3.13,
  measured;
- **a test catches the hazard deterministically**, on every version the suite runs, 3.12 among
  them;
- **the `with` point at 3.14** is handled as L11 says.

Nothing else about the writer changes.

---

## 2. What to change

### 2.1 The venv

Unchanged from 02b: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`,
`runregistrykit` editable. **Install nothing** into `venv/`. §3 also runs MacPorts' 3.13 and 3.14
on the checkout through `PYTHONPATH`, and installs nothing into them.

### 2.2 The two filters

In `runregistrykit/__init__.py`, as measured at writing:

```python
earlier = list(n for n in sorted(book["in_flight"]) if n < number)
...
earlier = list(n for n in earlier if n > landed)
```

A generator expression's filter runs in the generator's own frame. An exception raised there
leaves the generator and reaches `_write_status` at the `CALL` of `list`, which the table covers.
The first still iterates `sorted(...)`, a list made by one C call, never the live dict.
`number` and `landed` become cell variables of `_write_status` (a `MAKE_CELL` at its start). That
was measured, and is harmless.

**What does not do:**
- a list, set or dict comprehension. Every inlined comprehension with a filter has the gap;
- **a `for` loop with an `if`**, which the board's next step offered. Measured, its `if`'s false
  branch compiles to the same uncovered `POP_JUMP_IF_TRUE`/`JUMP_BACKWARD` pair, at 3.12, 3.13 and
  3.14. At 3.13 a real signal left the lock held 4 times at its `JUMP_BACKWARD` (§"At writing").

The agent may choose another form. Whatever it chooses, §3.4's static check must find no
`JUMP_BACKWARD` of `_write_status` outside its exception table at 3.12, 3.13 and 3.14, and §2.5's
test must pass. A one-line comment at the first of the two lines says why it is not a
comprehension or a loop, without naming an issue (the citation guard).

### 2.3 What does not change

- Every write's behaviour, re-entered or not: the merge, the discard, the put-back, the record of
  what landed, the temporary name, the mode, the leftover. What is written: no key of
  `status.json` added, removed or renamed (README §5 rule 7). `write_json_atomic`, the sidecars,
  `stores.py`, `__main__.py`.
- **The `with _STATUS_LOCK:` statement** (L11). It is not replaced by a hand-written acquire and
  release: that form was measured worse (§"At writing").
- **Every existing test, and 02b's two sweeps, in what they assert.**
  `git diff 2959b78 -- runregistrykit/tests` adds lines and removes none. `Attempt`,
  `Instructions`, `the_writers_code`, `made_inside`, `ending_of`, `MODES`, `SWEEPS`,
  `sweep_in_this_process`, `SWEEPER` and `TestAHandlerAtEveryInstruction` are not edited. The new
  test may call them, subclass or wrap them, or use its own.
- The workflow: `test_status_writes` is already in the core job, and `suite (high)` runs 3.13.16.

### 2.4 The `with` point at 3.14 (L11)

At 3.14 the `with` statement calls `__enter__` with a `CALL`, and the interpreter runs a pending
handler after that call returns, at an offset before the table's first entry. A handler raising
there leaves the lock acquired and nothing to release it. No in-flight entry is left, since the
write has not taken its number. A bare `with lock:` around any work, with no registry code, has the
same point at 3.14.8 and none at 3.12 or 3.13 (§"At writing"). So the point is the interpreter's.

**Under L11 (a), the recommendation:** `Run._update`'s "Not covered" paragraph gains one sentence.
At Python 3.14, a handler that raises just after the lock is taken, at the `with` statement's
entry, leaves it held, as it would any lock taken by a `with` on that version. No client runs
3.14, and CI does not. Nothing else changes, and the board narrows the issue to that point (§4.3).

**Under L11 (b):** instead, `pyproject.toml`'s `requires-python` becomes `">=3.12,<3.14"`, the
docstring sentence is not added, and the issue closes. `pyproject.toml` is then among the files
changed (§4.1), and the release notes (06) will say so.

### 2.5 The new test

Added to `runregistrykit/tests/test_status_writes.py`, core only, after 02b's sweep class. It
runs in a child process the test starts and does not signal, as 02b's sweeps do, under a timeout,
because a failure leaves the lock held in the process that made it.

**The sweep, restricted to `JUMP_BACKWARD`.** In the child, `sys.monitoring` `INSTRUCTION` events
on the writer's code objects (`the_writers_code()`, nested generator expressions included), under
a free tool id, cleared and freed however it ends, as 02b's are. For each write below, first count
one uninterrupted write, recording the `(code, offset)` of each instruction. Then, on a fresh run
each time, make one attempt at each instruction whose opname (by `dis.get_instructions` on that
code) is **`JUMP_BACKWARD`**. The handler records `finish("killed", exit_code=143)` and then
raises `SystemExit(143)`, and the callback ignores instructions while it runs. **After each
attempt:**
- **the lock is free**: another thread's `_STATUS_LOCK.acquire(blocking=False)` returns true, and
  that thread releases it at once. Use no private method of the lock;
- **no in-flight entry is left** in the book for the run's path;
- the file parses, says `killed` and 143, and leaves no `status.json.*.tmp` (`ending_of`).

If the lock is found held, the child records the attempt and then releases the lock on its own
thread until it is free, so that the later attempts mean something.

**The three writes**, each a heartbeat on a fresh run:
1. a plain `heartbeat(units_done=7)`;
2. a `heartbeat(units_done=8)` whose `json.dump` makes a handler's `heartbeat()` (`made_inside`).
   That handler's write is re-entered and composes from a landed base;
3. a `heartbeat(units_done=8)` whose `json.dump` makes a handler's `heartbeat(stage="B")` and then
   `heartbeat(stage="C")`. The second composes from B's landed payload with an older write still in
   flight. That is the only way to take `:372`'s false branch, and the only write that catches a
   comprehension at `:372` alone (§"At writing").

In (2) and (3) the handler's writes are part of the write swept: the sweep counts and interrupts
their instructions too.

**Why `JUMP_BACKWARD` only.** An `INSTRUCTION` event fires before its instruction runs, so a raise
from it models a handler run at a check that comes before the instruction's effect. At 3.13 and
3.14 a `JUMP_BACKWARD` is such a check. The other place a handler runs, after a `CALL` returns,
cannot be modelled this way. 3.14's `with` point is one such place, which is why §3.5 measures it
by a real signal and the test does not. An unrestricted sweep raises where the interpreter never
does: the `NOP` of `try:`, the `finally`'s body before its `pop`, and the `with`'s exit. Measured,
13 such instructions (14 at 3.14) in a candidate that is correct, so the unrestricted sweep cannot
assert the lock. `RESUME` added no attempt when measured: `INSTRUCTION` events did not fire for
it. At 3.12 the test is stricter than a real signal, since it raises at the `JUMP_BACKWARD` that
3.12 does not raise at. That is what lets the venv's suite catch a comprehension that would hang a
process at 3.13.

The test asserts that each write made at least one attempt. It gives the attempts and what failed,
with code name, line and offset, in its failure message. At writing the three writes made 3, 7
and 12 attempts, in well under a second.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root, `TMPDIR`
   in your scratch: **`Ran 328 + N tests … OK (skipped=1)`**. Give the per-module counts and the
   time.
2. **The core alone**, in a fresh scratch venv without `[stores]`, as 02b's §3.2: the four core
   modules pass, 86 + N tests, with `datastorekit`, `ray` and `sqlalchemy` absent. Remove the venv
   afterwards.
3. **At 3.13 and 3.14.** From the root, `TMPDIR` in your scratch, `PYTHONPATH` the checkout:
   `/opt/local/bin/python3.13 -m unittest runregistrykit.tests.test_status_writes
   runregistrykit.tests.test_host` passes, 49 + N tests, `OK (skipped=1)`; the same with 3.14.
   Without `PYTHONPATH` two of `test_host`'s command-line tests fail with `No module named
   runregistrykit`, which is the environment, not the package.
4. **The static check**, a scratch script: for `_write_status` at 3.12, 3.13 and 3.14, list the
   instructions between its first and last exception-table entries that no entry covers. After the
   change, at each version, they are the `NOP` of `try:` and the `with`'s exit sequence (and at
   3.14 the `with`'s entry and a `NOT_TAKEN`), and **no `JUMP_BACKWARD`**. Give the table, and
   the same against `2959b78`.
5. **The real signal**, re-run from §"At writing" in your scratch: a child that signals only
   itself, `SIGALRM` from a one-shot `setitimer` of 20 µs–2 ms armed inside the `try` and re-armed
   after each, the handler raising, through heartbeats of one run for 45 s, counting interruptions
   after which the lock is owned or an in-flight entry is left, and where. Run at 3.12 (`venv/`),
   3.13 and 3.14, against the change and against `2959b78` (by `git archive` into scratch). At 3.13
   also run 120 s, and once with the handler recording `finish("killed", exit_code=143)` before it
   raises. **0 at 3.12 and 3.13 after the change.** At 3.14, the `with`'s `CALL` only. Give the
   table, with the number of interruptions per row. Not committed.
6. **02's real-signal probe**, as 02b's §3.4: twelve cases, each in a child. All parse with
   `killed`, 143, `units_done` 7. Give the table. Not committed.
7. **The new test against `2959b78`'s writer**, in a scratch clone with the new test copied in: it
   fails, at 3.12 and at 3.13. Give the failing attempts per write.
8. **The tests catch behaviour** (README §5 rule 10). Each mutation applied in a scratch clone, the
   new test and `test_status_writes` run, and reverted:
   - (m1) `:365`'s line back to the list comprehension of `2959b78`;
   - (m2) the second line back to its list comprehension, the first kept;
   - (m3) the first line as a `for` loop with an `if`;
   - (m4) the agent's own: one more change to the two lines, or to the lock's handling, that the
     new test catches, named in the log.

   Each must fail the new test, named in the log, with the failing attempts. At writing, (m2) was
   caught by write (3) alone. A mutation no test catches is a stop.
9. **Nothing outside temporary directories**, as 02b's §3.3. `git grep -n 'signal' --
   'runregistrykit/*.py' ':!runregistrykit/tests'` finds only `finish`'s docstring.
10. `./venv/bin/black --check runregistrykit docs` is clean, at 31 files.
11. **CI.** Pushing is the user's. The new test first runs on Linux, and at 3.13 in `suite (high)`;
    record that the review is to read its result there.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` changes `__init__.py` and `tests/test_status_writes.py`
   only, and under L11 (b) `pyproject.toml` changes as well. The workflow is not changed.
2. §3.1–§3.10 hold. Every test that existed at `2959b78` passes unchanged in what it asserts.
3. **The records**, in the same commit:
   - the log, `logs/02c-the-writers-lock.md`, per README §5.1: the suite before (328) and after,
     the core run, the 3.13 and 3.14 runs, the static table, the real-signal table, the twelve
     cases, the new test against `2959b78`, and every mutation as a diff;
   - this board: the header, §1's row for 02c, §1.1's W3, and §3/§4. Under (a), the entry stays in
     §3, narrowed to the 3.14 `with` point, its owner none again, with what 02c resolved and the
     test that pins it. Under (b), it moves to §4;
   - `docs/OPEN_ISSUES.md`: under (a), the row's owner back to none and its hook narrowed to 3.14,
     the count unchanged (9); under (b), the row deleted and the count 8. The date either way;
   - `prompts/INDEX.md`: the campaign's line;
   - this campaign's README §2: 02c's status.

---

## 5. Stop conditions — stop and ask the user

- An existing test fails, or would need a change to what it asserts; 02b's sweeps would need an
  edit.
- A mutation of §3.8 is caught by no test.
- The real signal leaves the lock held, or an in-flight entry, at 3.12 or 3.13 after the change;
  or at 3.14 anywhere but the `with`'s entry.
- The static check finds a `JUMP_BACKWARD` outside the table that §2.2's form does not remove.
- Any record would change form: a key of `status.json` added, removed or renamed, or the manifest,
  `checkpoint.jsonl` or a sidecar touched. `write_json_atomic` changed.
- The design needs the package to install, mask or inspect a signal, to use anything outside the
  standard library, or a private method of the lock.
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory; a test signals any process but a child it started.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything into `venv/` or into MacPorts' Pythons.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `runregistrykit/__init__.py`;
  `runregistrykit/tests/test_status_writes.py`; under L11 (b), `pyproject.toml`; the log, this
  board, the campaign README's §2 row, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It does not change the `with`, the merge, the record, or any documented window other than adding
  the 3.14 sentence under (a).
- It does not touch 02's and 02b's other observations: a fork while the lock is held; a raise inside
  the `finally`; the bookkeeping lasting the process.
- It does not add 3.14 to CI or report anything upstream. Whether to report the `with` point to
  CPython is the user's.
- It writes no README usage or release notes (06), and makes no tag.

---

## At writing (2026-10-17, at `9d26357`)

Measured for the README's row and the orchestrator, in the session scratchpad with `TMPDIR`
there, against `git archive`s of `2959b78` (the package at `9d26357`) and `2bf9c72`, and three
candidates made from `2959b78` (none committed): **genexpr** (§2.2's two lines), **loop** (each
filter a `for` loop with an `if`) and **manual** (genexpr, with the `with` replaced by
`held = _STATUS_LOCK._recursion_count()`, then a `try` holding `acquire()` and the body, and a
`finally` that releases if the count rose). Pythons: 3.12.15 (`venv/`, and MacPorts' for the
static check), 3.13.16 and 3.14.8 (MacPorts').

- **The exception table** (`dis.Bytecode(...).exception_entries`). The uncovered instructions of
  `_write_status` between the lock's entry and exit:

  | Tree | 3.12.15 | 3.13.16 | 3.14.8 |
  |---|---|---|---|
  | `2959b78` | `NOP` (try); **`JUMP_BACKWARD` 278 (`:365`), 398 (`:372`)**; the `with` exit | `NOP`; **`POP_JUMP_IF_TRUE` + `JUMP_BACKWARD` 278/282 (`:365`), 418/422 (`:372`)**; the exit | the `with` entry through its `CALL` 22; `NOP`; **the same pairs, 326 and 470**; a `NOT_TAKEN`; the exit |
  | loop | `NOP`; **`JUMP_BACKWARD` 274, 416**; the exit | `NOP`; **the pairs at 276, 436**; the exit | the entry; `NOP`; **the pairs at 322, 488**; `NOT_TAKEN`; the exit |
  | genexpr | `NOP`; the exit | `NOP`; the exit | the entry; `NOP`; `NOT_TAKEN`; the exit |
  | manual | `NOP`; **the `finally`'s whole normal path** (`_recursion_count()`, the compare, `release()`) | the same | the same, and `NOT_TAKEN` |

  So 3.12 inlines the comprehension too (`LOAD_FAST_AND_CLEAR`, no nested code object), with the
  same gap. 02b's review attributed the inlining to 3.13.
- **The real signal**, §3.5's probe, 45 s per row with the handler raising. The first batch was
  fourteen children at once on ten cores, so a row is about 16 000 interruptions (about 98 % inside
  the writer). "Lock held" counts interruptions after which the lock was owned:

  | Tree | 3.12.15 | 3.13.16 | 3.14.8 |
  |---|---|---|---|
  | `2bf9c72` | 0 | 0 | 20, `:327` offset 24 (the `with`) |
  | `2959b78` | 0 | **5, `:365` offset 282**, each with the in-flight entry left | 30: 24 at the `with` (`:355`, offset 22), no entry left; 6 at `:365` offset 326, entry left |
  | loop | 0 | **4, at the loop's `JUMP_BACKWARD`** (offset 276) | 16: 13 at the `with`, 3 at the loop |
  | genexpr | **0** | **0** | 15, all at the `with` (offset 26) |
  | manual (second batch, ~23 700 per row) | **10** | **11** | 6, all at the `finally`'s `_recursion_count()` call |

  At 3.13, genexpr ran three more times for 120 s: **0 in 232 531 interruptions**, 229 990 inside
  the writer. With the handler recording `killed` before it raises, 45 s at 3.13: `2959b78` 4,
  genexpr 0; the file said `killed` in both.
- **A bare `with`**, no registry: `with lock: x = sum(range(50))` in a loop, an `RLock`, the same
  timer, 45 s. Lock left held after **5 228 of 34 704** interruptions at 3.14.8, and 0 at 3.12.15
  and 3.13.16. The 3.14 point belongs to the interpreter's `with`, not to the writer.
- **The sweep restricted to `JUMP_BACKWARD`**, §2.5's three writes, the handler recording `killed`
  and raising, lock and in-flight checked after each attempt. Attempts 3, 7 and 12 per write at
  every version. Failures:

  | Tree | 3.12.15 | 3.13.16 | 3.14.8 |
  |---|---|---|---|
  | `2959b78` | 1, 2, 4 (`:365` offset 278; in write 3 also `:372` offset 398) | 1, 2, 4 (282; 422) | 1, 2, 4 (326; 470) |
  | loop | 1, 2, 4 | 1, 2, 4 | 1, 2, 4 |
  | genexpr | **0, 0, 0** | **0, 0, 0** | **0, 0, 0** |
  | genexpr with `:372` a comprehension again ((m2)) | 0, 0, **1** (`:372`) | 0, 0, **1** | — |

  Each failure left both the lock and the in-flight entry. Each write took 0.01–0.05 s. Adding
  `RESUME` to the set added no attempt.
- **The unrestricted sweep on genexpr**, one plain heartbeat, the same checks: 13 of 327
  instructions fail at 3.12 and at 3.13, and 14 of 346 at 3.14. They are the `NOP` of `try:`
  (lock), the seven instructions of the `finally` before its `pop` completes (in-flight), and the
  five of the `with`'s exit, six at 3.14 (lock). None of them is a place where the interpreter
  runs a handler.
- **The existing tests** pass on genexpr: `test_status_writes` and `test_host`, 49 tests, `OK
  (skipped=1)`, at 3.12.15, 3.13.16 and 3.14.8, the last two with `PYTHONPATH` on the tree. Without
  it, at 3.13, two command-line tests of `test_host` failed: `No module named runregistrykit`.
  `2959b78`'s `test_status_writes` passes at 3.13.16 (21 tests), so the suite does not see the
  defect today, and CI's green run says nothing about it.
- `requires-python = ">=3.12"` (`pyproject.toml:9`). CI runs 3.12.15 and 3.13.16, not 3.14.
