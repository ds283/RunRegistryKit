# Prompt 02b — the writer's bookkeeping

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 02 has landed and been reviewed (`2bf9c72`; the review `a38022f`; CI run `39049728089` green,
  recorded in `91e8e9c`).
- The user has asked for both issues 02's review opened to be fixed: the first "at the earliest
  sensible opportunity", the second with a test (2026-10-17).
- `git diff --stat 2bf9c72 HEAD -- runregistrykit pyproject.toml .github` is empty: the package is
  02's.
- The suite is `Ran 322 tests … OK (skipped=1)` on macOS, and `git status` is clean in this
  repository.

**Closes:** `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]` and
`[02-the-landed-record-is-unpinned-and-can-move-backwards]`. **Opens:** only what the work finds.
**Narrows:** nothing planned.

**Recommended model:** **Opus**. The change is a dozen lines of 02's writer, and its tests have to
interrupt that writer at every instruction it executes.

**Read first:**

1. [`README.md`](README.md): §0, §1 (no signal handling in the package), §5 (all of it; rules 7, 8
   and 10 especially), §6.2 L5 with its 2026-10-17 amendment.
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §1's *Orchestrator review of prompt 02*,
   checks 6 and 8; §3's two `[02-…]` entries in full, with their "Measured at writing 02b"
   paragraphs; §4's `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`.
3. [`02-status-writes.md`](02-status-writes.md) §2.2–§2.4, and
   [`logs/02-status-writes.md`](logs/02-status-writes.md): "The writer", deviations 13–18, and
   "Observations not acted on".
4. `runregistrykit/__init__.py` at `2bf9c72`: `:259-349` (the writer: `_STATUS_LOCK` `:265`,
   `_STATUS_WRITES` `:270`, `_status_temporary_name` `:276`, `_remove_quietly` `:284`,
   `_land_status` `:291`, `_write_status` `:324`) and `Run._update` `:691-723`.
5. `runregistrykit/tests/test_status_writes.py`, all of it.
6. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

---

## 1. What is wanted

02's writer keeps a terminal state through one handler write made at any of the four points its
tests use. Its review found two ways the bookkeeping behind that can still lose a state:

- **An older in-flight write re-applied over a newer landed one.** A re-entered write composes from
  the newest landed payload, then the fields of *every* earlier write still in flight
  (`:337-343`). A landed write made inside an earlier in-flight one already carries that write's
  fields, and may have set the same keys anew; re-applying the older fields puts them back. With
  two handler writes inside one write, a `stage` goes back, and, when the interrupted write is the
  run's own `finish("done")`, the handler's `killed` is replaced by `done`.
- **The record of what landed moving backwards.** After its replace, a write checks for a later
  landed write (`:318`) and then records its own number and payload (`:321`). A handler that lands
  a later write in between (and `copy.deepcopy`, called on `:321` before the store, is pure Python,
  so a real signal can arrive inside it) is hidden from the bookkeeping. The file is right, but a
  later re-entered write composes from the stale record and lands `running` over the terminal
  state. And no test pins the early `return` after a put-back (`:320`): with it removed, the same
  thing happens and every test passes.

So:
- **a re-entered write re-applies only the in-flight writes newer than the payload it composes
  from**;
- **the record of what landed is never lowered**, whatever instruction a handler interrupts;
- **a test interrupts the writer at every instruction it executes**, and pins both.

Nothing else about 02's writer changes: the temporary name, the mode, the discard, the put-back,
the lock, the leftover, and every un-re-entered write.

---

## 2. What to change

### 2.1 The venv

Unchanged from 02: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`,
`runregistrykit` editable. **Install nothing** into `venv/`. The core run of §3.2 builds its own
scratch venv.

### 2.2 The merge (02's §2.3 step 2, amended)

All in `runregistrykit/__init__.py`. A write composes its payload from a base, then the fields of
earlier writes to this path still in flight in this process, in sequence order, then its own
fields, then the heartbeat stamp, as in 02. **What changes is which in-flight writes are applied:**

- **base is the file** (no earlier write in flight, or none has landed): every earlier in-flight
  write, as now;
- **base is the newest landed payload**, numbered `L`: only the earlier in-flight writes numbered
  **above `L`**. Those numbered below `L` began before `L` and were in flight throughout it, so
  `L`'s payload already holds their fields, and any key `L` set since is newer.

A discarded heartbeat still loses nothing: its fields are in the landed payload that overtook it.

### 2.3 The record of what landed (02's §2.3 step 6, amended)

**The property, which the tests pin:** at every instruction boundary of the writer, the highest
number the bookkeeping holds as landed, and its payload, is the newest write that has landed for
this path in this process. Recording one write never hides a later one.

**One shape that has it, measured at writing (§"At writing"):**
- the landed record is a dict per path, sequence number → payload, and "the newest" is its highest
  key, read through one helper;
- a write takes its deep copy first, then checks for a later landed write (the put-back, as in 02),
  and otherwise records itself with **one store**, `landed[number] = copy`. A handler landing a
  later write anywhere around that store adds its own key, which a lower one cannot hide;
- older entries are then pruned, iterating **a snapshot** of the keys (`list(...)`, one C call),
  never the live dict. A handler that adds a key during a Python-level iteration raises
  `RuntimeError: dictionary changed size during iteration`, which the planner's first draft did;
- the helper reads the highest key and its payload, and reads again if a handler's prune removed
  that key in between, so it never returns a number with no payload.

The agent may choose another shape with the same property. It states the shape in the log, and the
sweep of §2.5 is its test either way. The early `return` after a put-back stays, and is pinned
(§2.5).

### 2.4 What does not change

- Every un-re-entered write: one read of the file, one write, one `os.replace`, the same keys, the
  same mode, a name `status.json.<unique>.tmp`.
- 02's discard, put-back, `RLock`, keying by real path, leftover and documented windows, except
  where §2.2 and §2.3 change them.
- `write_json_atomic`, every sidecar write, `stores.py`, `__main__.py`. What is written: no key of
  `status.json` added, removed or renamed (README §5 rule 7).
- `test_status_writes.py`'s 15 existing tests, in what they assert. They pass unchanged.
- **`Run._update`'s docstring** is changed only to state the amended merge and record, and its line
  of 121 characters (`:696`, noted by 02's review) is rewrapped to the file's 100 columns.

### 2.5 The new tests

Added to `runregistrykit/tests/test_status_writes.py`, core only, as 02's are.

**The two measured cases of `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]`**, in
this process, `json.dump` patched to fire once:
- a `heartbeat(units_done=7, stage="A")` whose write makes a handler's `heartbeat(stage="B")` and
  then a handler's `finish("killed", exit_code=143)`: `killed`, 143, `units_done` 7, `stage` **B**;
- a `finish("done", exit_code=0)` whose write makes a handler's `finish("killed",
  exit_code=143)` and then a handler's `heartbeat`: **`killed`**, 143;
- the same `finish("done")` with one handler write, `finish("killed")`: `killed`, 143.

**The put-back, then a later re-entered write** (02's review, (o2)): a heartbeat whose replace is
preceded by a returning handler's `finish("killed", exit_code=143)` (so the heartbeat puts it back);
then a later `heartbeat(units_done=8)` whose `json.dump` makes a handler's `heartbeat`. `killed`,
143 throughout.

**The sweep.** A handler run at every instruction the writer executes, one instruction per attempt,
by `sys.monitoring` (`INSTRUCTION` events, set with `set_local_events` on the writer's own code
objects only: every function the writer section defines). `sys.settrace` does not do: at 3.12.15
its `opcode` events were never delivered for these frames, at the planner's measurement. Python
`>=3.12` is the package's floor (`pyproject.toml`), so `sys.monitoring` is always there.
- Take a free tool id (try each of `sys.monitoring`'s ids until `use_tool_id` succeeds; fail if
  none is free), and in a `finally` clear the local events and free the id.
- The callback ignores instructions while the handler runs, so the handler's own write is not
  counted or interrupted.
- First count the instructions of one uninterrupted write, then make one attempt per instruction,
  each on a fresh run.

Two sweeps, each with the handler in four modes: `finish("killed", exit_code=143)` alone or followed
by a `heartbeat`, then **returning** or **raising** `SystemExit(143)`:
- **an interrupted heartbeat** (`units_done=7`): at every instruction and in every mode, the file
  parses, says `killed` and 143, and leaves no `status.json.*.tmp`. Then a later heartbeat whose
  `json.dump` makes a handler's `heartbeat` leaves `killed` (this is what catches a lowered record);
- **an interrupted `finish("done", exit_code=0)`**: with the handler **raising**, `killed` and 143
  at every instruction. With it **returning**, `killed` and 143 at every instruction after the
  interrupted write has registered its fields as in flight. Before that the handler's write is the
  earlier one, and `done` landing last is right. The test tells the two apart by reading, inside
  the handler, whether the interrupted write's fields are in flight in the writer's bookkeeping,
  and accepts either state only where they are not.

Bound each sweep's time, and give its instruction count and time in the log. At writing, a sweep of
one mode took a few seconds here.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root, `TMPDIR`
   in your scratch: **`Ran 322 + N tests … OK (skipped=1)`**. Give the per-module counts and the
   time.
2. **The core alone**, in a fresh scratch venv without `[stores]`, as 02's §3.2: `python -m
   unittest runregistrykit.tests.test_run_registry runregistrykit.tests.test_public_names
   runregistrykit.tests.test_host runregistrykit.tests.test_status_writes` passes, 80 + N tests,
   with `datastorekit`, `ray` and `sqlalchemy` absent. Remove the venv afterwards.
3. **Nothing outside temporary directories**, as 02's §3.3. `git grep -n 'signal' --
   'runregistrykit/*.py' ':!runregistrykit/tests'` finds only `finish`'s docstring.
4. **02's real-signal probe**, written again in your scratch from 02's §"At writing" and its
   review's check 5: twelve cases, four points × three endings, each in a child process. All parse
   with `killed`, 143, `units_done` 7. Give the table. Not committed.
5. **The sweeps against `2bf9c72`'s writer**, in a scratch clone: the new tests fail there, and
   the log gives which and how many instructions fail in each mode.
6. **The tests catch behaviour** (README §5 rule 10). Each mutation applied in a scratch clone, the
   named tests run, and reverted:
   - (m1) the merge applying every earlier in-flight write again (02's step 2);
   - (m2) the record a single number and payload again, set after the deep copy (02's step 6);
   - (m3) the early `return` after a put-back removed (02's review, (o2));
   - (m4) the prune iterating the live dict, not a snapshot;
   - (m5) the agent's own: one more mutation of the record or the merge that a test catches, named
     in the log.

   Each must fail at least one test, named in the log, with the sweep's failing instruction count
   where the sweep is what fails. A mutation no test catches is a stop.
7. `./venv/bin/black --check runregistrykit docs` is clean, at 31 files.
8. **CI.** Pushing is the user's. The sweeps first run on Linux and on 3.13 in CI; record that the
   review is to read their result there.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` changes `__init__.py` and `tests/test_status_writes.py`
   only; the workflow is not changed (the core job already names the module).
2. §3.1–§3.7 hold. Every test that existed at `2bf9c72` passes unchanged in what it asserts.
3. **The records**, in the same commit:
   - the log, `logs/02b-the-writers-bookkeeping.md`, per README §5.1: the suite before (322) and
     after, the core run, the probe's table, the sweeps against `2bf9c72` and after, and every
     mutation as a diff;
   - this board: the header, §1's row for 02b, §1.1's W2, §3 and §4 (both issues moved to §4, each
     with what resolved it and the tests that pin it);
   - `docs/OPEN_ISSUES.md`: the two rows deleted, the count (10 → 8), the date;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- An existing test fails, or would need a change to what it asserts.
- A mutation of §3.6 is caught by no test.
- The sweep finds an instruction at which a terminal state is lost, or a file left, that §2.2 and
  §2.3 do not remove.
- Any record would change form: a key of `status.json` added, removed or renamed, or the manifest,
  `checkpoint.jsonl` or a sidecar touched. `write_json_atomic` changed.
- The design needs the package to install, mask or inspect a signal, to use anything outside the
  standard library, or a lock a handler's write could wait on.
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory; a test signals any process but a child it started.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything into `venv/`.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `runregistrykit/__init__.py`;
  `runregistrykit/tests/test_status_writes.py`; the log, this board, `prompts/INDEX.md`,
  `docs/OPEN_ISSUES.md`.
- It does not change 02's documented windows other than the record's (a handler between a write
  taking its number and registering its fields still loses those fields, never the terminal
  state), order writes between processes, or remove leftover temporary files.
- It does not touch the agent's other observations of 02 (a fork while the lock is held; a raise
  inside the `finally`; the bookkeeping lasting the process).
- It writes no README usage or release notes (06), and makes no tag.

---

## At writing (2026-10-17, at `91e8e9c`)

Measured for the README's row and the orchestrator, in the session scratchpad, against a clone of
`2bf9c72` and a candidate of §2.2 and §2.3 (not committed):

- **`sys.settrace` delivers no opcode events here.** With `f_trace_opcodes` set in the global
  tracer and again in the local one, `_write_status` gave `line`, `exception` and `return` events
  only, at Python 3.12.15. `sys.monitoring` with `INSTRUCTION` events on the writer's code objects
  counted 129 instructions for one failing write, and works for the sweep.
- **The sweep against `2bf9c72`.** An interrupted heartbeat executes 202 instructions of the
  writer. With the handler's `finish` then **returning**, 15 points lose the state: the file says
  `killed` after the heartbeat, and a later heartbeat re-entered by a handler's heartbeat puts
  `running` back. They are line 318's check through line 321's `copy.deepcopy` call, before its
  store. With the handler raising, none do. Adding a handler `heartbeat` after the `finish` gives
  the same 15 and 0. An interrupted **`finish("done")`**: 43 (returning) and 7 (raising) points end
  other than `killed`; with the handler's second write, 178 and 157.
- **The candidate** (the record a dict by number with one store and a snapshot prune; the merge
  skipping in-flight writes at or below the base's number; `next()` on an `itertools.count` for the
  number). An interrupted heartbeat executes 254 instructions: **0 bad** in all four modes. An
  interrupted `finish("done")`: 0 bad raising, and with the handler returning, 24 points end `done`,
  each at or before the instruction that takes the interrupted write's number, where the handler's
  write is the earlier. Both measured cases end `stage` `B` and `killed`; the (o2) sequence keeps
  `killed`; 02's twelve real-signal cases are unchanged (`killed`, 143, `units_done` 7);
  `test_status_writes`, `test_run_registry` and `test_host` pass unchanged, 72 tests.
- **The candidate's first draft** pruned by iterating the live dict, and the sweep raised
  `RuntimeError: dictionary changed size during iteration` at the first point a handler landed
  inside the prune. So the sweep tests what it should.
- **Taking the number by read-then-increment** (`n = book["next"]; book["next"] = n + 1`) instead
  of `next()`, in the candidate, leaves the heartbeat sweep at 0 bad: a handler inside the window
  takes the same number, but the interrupted write then has no earlier write in flight and reads
  the file, which holds the handler's write. So the prompt does not require `next()`, and it is not
  a mutation.
- `requires-python = ">=3.12"` (`pyproject.toml:9`).
