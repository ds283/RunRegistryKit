# Prompt 02 — status writes

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 01 has landed and been reviewed (`387c58f`; the review `5d71a6b`; CI run `38911075984` green,
  recorded in `c2911d3`).
- L5 is taken (README §6.2, 2026-10-17): (a), refined, as this prompt's §2 states it.
- `git diff --stat 387c58f HEAD -- runregistrykit pyproject.toml .github` is empty: the package is
  01's.
- The suite is `Ran 307 tests … OK (skipped=1)` on macOS, and `git status` is clean in this
  repository.

**Closes:** `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`.
**Opens:** only what the work finds. **Narrows:** nothing planned.

**Recommended model:** **Opus**. The change is small in lines and large in cases: a write that a
signal handler re-enters, at four points, ended three ways, from one `Run` or two, on one thread or
two. Every later prompt's judgement of a run reads the file this prompt writes.

**Read first:**

1. [`README.md`](README.md): §0 and §0.2 (the heartbeat race), §1 (out of scope: signal handling
   in the package), §5 (all of it; rules 7, 8 and 10 especially), §6.2 L5 (taken).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md) §3:
   `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` in full, its two
   corrections and its "Measured at writing 02" paragraph above all.
3. `runregistrykit/__init__.py`: `:64-99` (imports, `__all__`), `:234-253` (`read_json`,
   `write_json_atomic`), `:531-541` (`Run.__init__`), `:590-656` (`Run.status`, `_update`,
   `heartbeat`, `finish`), `:688-732` (`record`), `:938-947` (`begin`'s manifest and first status).
4. `runregistrykit/stores.py` `:255-257` (`_tmp_path`), and the board entry's list of its callers.
5. `runregistrykit/tests/test_run_registry.py` `:116-160` (`RegistryTestCase`) and `:604-653`
   (`TestStatus`: the replace test and the torn-read test); `.github/workflows/tests.yml` (the core
   job's test line).
6. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers are the package's at `387c58f`, which `c2911d3` has unchanged.

---

## 1. What is wanted

A signal handler that writes `status.json` while a heartbeat is writing it leaves the file
parseable, with the handler's state in it, however the handler ends, and loses nothing the
heartbeat was given.

Today every write of `status.json` goes through the one name `status.json.tmp`, so the handler's
write reopens and truncates the heartbeat's open file. Measured at writing (§"At writing"), a
handler that **raises** can leave the run `running`, or `killed` with its exit code `null`. A
handler that **returns** leaves it `running` and makes the heartbeat raise `FileNotFoundError` into
the caller. A handler that **ends the process** (SGK's `terminal`) survives. A unique name per
write fixes the raising case and not the returning one: the heartbeat's `os.replace` then lands
after the handler's and puts `running` back.

So, under L5 (a) as the user refined it:
- **`status.json`, and only `status.json`, is written through a temporary name of its own** in the
  same directory, with the mode the fixed name gave;
- **a write superseded by a later write to the same `status.json` from the same process is
  discarded**, not replaced, whichever `Run` object made it;
- **the later write keeps the earlier one's fields**, so a discarded heartbeat's `units_done` and
  `stage` are not lost.

`write_json_atomic` is not changed. Sidecars and the manifest keep `<path>.tmp` and every check
built on it.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`, `runregistrykit`
editable. **Install nothing** into `venv/`. The core run of §3.2 builds its own scratch venv.

### 2.2 The status writer

All in `runregistrykit/__init__.py`, standard library only (`threading` is allowed; `tempfile` is
not needed and **`signal` is not used**: the package installs, masks and inspects no signal,
README §1). A private writer used by `Run._update` and by nothing else:

- **The name.** `<status path>.<unique>.tmp`, in the run directory: it begins `status.json.`, ends
  `.tmp`, and is never `status.json.tmp`. Two writes never share one, in one process or two (for
  example the pid, a per-process counter and a few random hex characters). `TestStatus`'s replace
  test (`test_run_registry.py:605`) then passes unchanged: it asks only for a `.tmp` suffix, the
  same directory, and one `os.replace` per heartbeat.
- **The mode.** Created with `os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)`, so that
  the umask applies exactly as it does to `open(path, "w")` today. **Not** `tempfile.mkstemp`
  (`0600`, kept by `os.replace`), and **not** a read of `os.umask`, which is process-wide and can
  only be read by setting it.
- **The write.** As `write_json_atomic` writes: `json.dump(payload, handle, indent=2,
  sort_keys=True)`, a newline, `flush`, `fsync`, then `os.replace` onto `status.json`, subject to
  §2.3.
- **Its own leftovers.** Any exception before the replace, `BaseException` included (a handler's
  `SystemExit` arrives as one), removes the temporary file, best-effort and without hiding the
  exception, and re-raises. A process that dies between creating the file and replacing it
  (`SIGKILL`, or a handler that restores `SIG_DFL` and kills itself) leaves a
  `status.json.<unique>.tmp` in the run directory. Nothing reads it, and `list` and the store
  operations do not look at a run directory's other files. Say so in `_update`'s docstring and in
  the log. Nothing removes it, and nothing is added that does.

### 2.3 Supersession (L5 (a), refined)

Bookkeeping kept by the module, per `status.json` in this process, **keyed by
`os.path.realpath(status_path)`**, so that `Run(path)` made in a handler and the `Run` that `begin`
returned are one writer. Each `_update`:

1. **takes a sequence number** for that path, and registers the fields it was given as in flight
   under it;
2. **composes its payload** from a base, then the fields of every earlier write to this path still
   in flight in this process, in sequence order, then its own fields, then the heartbeat stamp. The
   base is the file, read as now, **unless an earlier write to this path is in flight in this
   process**. A handler has then re-entered a write, and the base is the newest payload this
   process has landed for this path, or the file if it has landed none;
3. writes its temporary file (§2.2);
4. **discards** it, removing the temporary file and replacing nothing, if a write with a higher
   sequence number for this path has landed since it began;
5. otherwise replaces, and then, **if a write with a higher number landed between its check and its
   replace**, puts that write's payload back: a fresh temporary file with that payload, replaced
   onto `status.json`. A handler can run at the bytecode boundary before the `os.replace` call. The
   put-back is itself a write under steps 4 and 5, with the sequence number of the payload it puts
   back, so a handler that re-enters the put-back is not undone by it;
6. records what landed (the highest sequence number and its payload), and in a `finally` removes
   its own in-flight entry.

`_update` returns the payload it composed, as today. A plain heartbeat with no write in flight reads
the file, writes once and calls `os.replace` once, so the launcher's case is unchanged: a
`heartbeat(pid=…)` and a `finish` made in another process still read what is on disk. **Writes from
two processes at once are not this prompt's subject** (README §1), and nothing here orders them.

**Threads.** SGK's pipeline heartbeats from its `sys.stdout` stream (`scoped_pipeline_run.py:233`,
`:571`, at SGK `79434bf`). That runs on whichever thread prints, so a heartbeat on one thread and a
handler's `finish` on the main thread can overlap. Hold a **`threading.RLock`** across steps 1–6.
Two threads' writes are then serialised, and a handler that re-enters a write on its own thread
takes the lock again and is not blocked. **A `threading.Lock` deadlocks that handler**: the
interrupted write holds it, and the handler waits for a write that cannot resume.

**What is not covered, and is said in the docstring and the log:** a handler that re-enters between
a write taking its number and registering its fields loses those fields, never the terminal state.
Writes from two processes at once are not ordered at all.

### 2.4 What does not change

- **`write_json_atomic`**: its body, its `<path>.tmp` and its place in `__all__`. Every sidecar
  write, the manifest's write in `begin`, and `stores._tmp_path` and each leftover check built on it
  are untouched. A test pins `write_json_atomic`'s name (§2.6).
- **What is written.** `status.json`'s keys and values are as before for every call that is not
  re-entered. The manifest, `checkpoint.jsonl` and the sidecar are untouched (README §5 rule 7).
- **How a record is read and judged.** `read_json`, `Run.status`, `liveness` and `list_runs` are
  not changed. A `status.json` written by `v0.1.0` (no `host`) is updated by a heartbeat and a
  `finish` with its keys kept and no `host` added (rule 8; pinned in §2.6).
- **`Run.heartbeat`, `Run.finish`, `Run.record`**: their signatures, their docstrings except where
  they cite the write, and their returns.

### 2.5 CI

`.github/workflows/tests.yml`'s core job runs its tests by name. Add the new module (§2.6) to that
line. Change nothing else in the workflow.

### 2.6 The new tests

One new module, **`runregistrykit/tests/test_status_writes.py`**, with the licence header and a
docstring of its own, **core only**: it imports nothing of the store layer, so the core CI job runs
it. A handler is simulated in the test process by calling `finish` from inside a patched function,
which is what a Python signal handler is: a call at a bytecode boundary. One test also uses a real
signal in a child process.

**The reproduction**, the board's next step widened. A run begun with `begin`; a `heartbeat(units_done=7,
stage=…)` whose write calls `run.finish("killed", exit_code=143)` from inside it, at each of four
points:
- (P1) inside `json.dump`, half the payload written to the handle;
- (P2) inside `json.dump`, all of it written, before the flush;
- (P3) in `os.replace` for the heartbeat's file, before the real replace;
- (P4) in `os.replace` for the heartbeat's file, after the real replace.

Each point is run with the "handler" then **raising** `SystemExit(143)` and then **returning**. In
all eight:
- `status.json` parses;
- `state` is `killed` and `exit_code` 143;
- `units_done` is 7 and the heartbeat's `stage` is there (the merge);
- `pid` and `host` are as `begin` wrote them;
- no `status.json.*.tmp` is left in the run directory;
- the heartbeat raised `SystemExit` in the raising case and returned in the returning case, never
  `FileNotFoundError`.

Patch `json.dump` and `os.replace` so that they fire once, for the heartbeat's write only. The
`finish` inside goes through the real ones.

**At least, besides:**
- **A second `Run` object.** As the reproduction at (P1) and (P3), returning, with the "handler"
  calling `runregistrykit.Run(run.path).finish(…)`: the same result.
- **A handler during the put-back.** At (P3), returning, where the put-back's own `os.replace`
  makes a second re-entry, `run.heartbeat(stage="from the second handler")`, from inside it, before
  the real replace. When that re-entry composes its payload, the file holds the clobbering
  heartbeat's `running`. `status.json` must end parseable, `killed` with 143, with that `stage`,
  and with nothing left behind. This pins step 2's base and the put-back's own supersession.
- **A real signal, in a child process** the test starts and nothing else (README §5 rule 6). The
  child begins a run, installs a `SIGTERM` handler that calls `finish("killed", exit_code=143)`,
  and sends itself `SIGTERM` from inside a heartbeat's `json.dump`. The handler raises, returns or
  ends the process (`SIG_DFL` and `os.kill` itself, as SGK's `terminal` does), one child each. All
  three leave `status.json` parseable with `killed` and 143. The first two leave no temporary file;
  the third may leave exactly one, `status.json.<unique>.tmp`, and the test says that it is the
  documented leftover. Each child runs under a `timeout`, so that a handler that waits for ever on
  the write it interrupted fails the test instead of hanging it.
- **Two threads.** A thread making heartbeats in a loop while the main thread calls `finish`: when
  both are done, `status.json` parses, says `killed`, and nothing is left behind. Bound the loop,
  and join the thread with a timeout so that a deadlock fails the test instead of hanging it.
- **The name.** The temporary name is in the run directory, begins `status.json.`, ends `.tmp`, is
  not `status.json.tmp`, and differs between two heartbeats.
- **The mode.** With the umask set to `0o022`, then `0o077`, and restored in a `finally`:
  `status.json`'s mode after a heartbeat equals the mode `write_json_atomic` gives a file in the
  same directory (`0o644`, `0o600`).
- **A failed write.** A heartbeat whose `json.dump` raises (for example a `stage` that is not
  JSON-serialisable) raises, leaves `status.json` as it was, and leaves no temporary file. The next
  heartbeat works.
- **`write_json_atomic` unchanged.** It still replaces from exactly `<path>.tmp`.
- **An old record** (README §5 rule 8). A `status.json` of `v0.1.0`'s form, with no `host`, built in
  the test, then `heartbeat` and `finish`: every key it had is kept, `host` is not added, and
  `liveness` judges it as before.
- **A heartbeat with nothing in flight** calls `os.replace` once and reads the file once.

### 2.7 The board's issue

**Closed: `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`**, moved to §4.
Say what resolved each of its parts, and name the tests that pin each:
- the shared temporary name → §2.2;
- the lost terminal state when the handler returns → §2.3 steps 4 and 5;
- the `FileNotFoundError` into the caller → §2.2's unique name;
- the mode → §2.2;
- `write_json_atomic` and the sidecars → unchanged (§2.4), so 06's release notes say
  "`write_json_atomic`: unchanged".

The other three entries on the board: give each its package lines at this commit where 02's edits
moved them, under a "Package lines (02, …)" note. `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`
gains one sentence: 02 removes the one known cause of an unreadable `status.json`, and every other
cause stands.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root, `TMPDIR`
   in your scratch: **`Ran 307 + N tests … OK (skipped=1)`**, N the new tests. Give the per-module
   counts (by the loader) and the time.
2. **The core alone**, as CI's core job runs it, in a fresh scratch venv with the package installed
   without `[stores]`: `python -m unittest runregistrykit.tests.test_run_registry
   runregistrykit.tests.test_public_names runregistrykit.tests.test_host
   runregistrykit.tests.test_status_writes` passes, with `datastorekit`, `ray` and `sqlalchemy`
   absent. Remove the venv afterwards.
3. **Nothing outside temporary directories.** `git status --short --ignored` is the same before and
   after a run (but `__pycache__/`). No Ray process before or after. `git grep -n 'signal' --
   'runregistrykit/*.py' ':!runregistrykit/tests'` finds only `finish`'s docstring, as at
   `387c58f` (`__init__.py:632`).
4. **The planner's probe, written again in your scratch** from §"At writing"'s description and run
   against the tree after the change, with nothing patched but the `json.dump` that sends the
   signal. Run the six cases (raise, return, end the process × half or all of the payload written),
   each in a child process. Every case parses with `killed` and 143, and `units_done` 7; give the
   table in the log. Not committed.
5. **The mutation record**, each a diff exactly as applied, with the failing tests named. None is
   committed.
6. **The tests catch behaviour** (README §5 rule 10). Each mutation applied, the suite or the named
   modules run, and reverted:
   - (m1) status written through `<path>.tmp` again (the writer's name fixed);
   - (m2) step 4 removed: a superseded write replaces (L5 (b));
   - (m3) step 5's put-back removed;
   - (m4) step 2's merge of in-flight fields removed;
   - (m5) step 2's base always the file;
   - (m6) the bookkeeping keyed by the `Run` object, not the path;
   - (m7) the temporary file not removed on an exception;
   - (m8) the file created by `tempfile.mkstemp` (`0600`);
   - (m9) the `RLock` replaced by a `threading.Lock`. Run the real-signal child tests alone, by
     name. Under (m9) an in-process re-entrance blocks for ever, which is the defect, so those
     tests are not run. The children's timeout must make the named tests fail;
   - (m10) the agent's own: one mutation of `write_json_atomic` that a test catches, named in the
     log.

   Each must fail at least one test, named in the log. A mutation no test catches is a stop.
7. `./venv/bin/black --check runregistrykit docs` is clean, at 31 files.
8. **CI.** Pushing is the user's. Record that the new module first runs on Linux in CI, and that the
   review is to read its result there.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` gains exactly `tests/test_status_writes.py`, and changes
   `__init__.py` only; the workflow changes on one line.
2. §3.1–§3.7 hold. Every test that existed at `387c58f` passes unchanged in what it asserts.
3. **The records**, in the same commit:
   - the log, `logs/02-status-writes.md`, per README §5.1: the suite before (307) and after, the
     core run, the probe's table of §3.4, and every mutation as a diff;
   - this board: the header, §1's row for 02, §1.1's W1, §3 and §4 as §2.7;
   - `docs/OPEN_ISSUES.md`: the row deleted, the count (9 → 8), the date;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- An existing test fails, or would need a change to what it asserts. `TestStatus`'s two tests above
  all.
- A mutation of §3.6 is caught by no test.
- Any record would change form: a key of `status.json` added, removed or renamed for a call that is
  not re-entered, or the manifest, `checkpoint.jsonl` or a sidecar touched.
- `write_json_atomic`'s name, body or behaviour would change, or any sidecar write would.
- The design needs the package to install, mask or inspect a signal (README §1), or to use
  anything outside the standard library.
- A design in which a handler's `finish` can wait on the write it interrupted.
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory; a test signals any process but a child it started.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything into `venv/`.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `runregistrykit/__init__.py`; new
  `runregistrykit/tests/test_status_writes.py`; one line of `.github/workflows/tests.yml`; the log,
  this board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It does not change how an unreadable `status.json` is treated (03), `end` (04) or `begin`'s
  refusals (05).
- It removes no leftover temporary file, and orders no writes between two processes.
- It writes no README usage or release notes (06), changes `pyproject.toml` not at all, and makes
  no tag.

---

## 7. The log and the board

`logs/02-status-writes.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 02, §1.1's W1, §3 and §4 as §2.7.

---

## At writing (2026-10-17, at `c2911d3`)

Measured for the README's row and the orchestrator:
- **The race, by a planner's probe** (scratch, not committed), at `c2911d3`. A child process began a
  run, installed a `SIGTERM` handler that called `run.finish("killed", exit_code=143)`, and sent
  itself `SIGTERM` from inside a heartbeat's `json.dump` (`units_done=7`), after half the payload
  or all of it had been written to the handle. "Unique" replaced `write_json_atomic` for the
  status with a `mkstemp`-named write, L5 (b), and nothing else:

  | Name | Handler | Half written | All written |
  |---|---|---|---|
  | fixed (today) | raises `SystemExit` | parses: `killed`, `exit_code` `null`, `units_done` 0 | parses: **`running`**, `units_done` 7 |
  | fixed (today) | returns | heartbeat raises `FileNotFoundError`; **`running`** | the same |
  | fixed (today) | ends the process (`SIG_DFL`, `os.kill`) | `killed`, 143 | `killed`, 143 |
  | unique | raises | `killed`, 143 | `killed`, 143 |
  | unique | returns | **`running`**, `units_done` 7 | the same |
  | unique | ends the process | `killed`, 143; one `status.json.<x>.tmp` left | the same |

  In every case that kept `killed`, `units_done` was 0: the `finish` read the file before the
  heartbeat landed. That is what §2.3 step 2's merge keeps.
- **SGK**, read through `git` at `79434bf`. Its handlers close over the `Run` that `begin` returned:
  `make_killed_handler` (`docs/gktk-remedial/scoped_pipeline_run.py:352`) raises `SystemExit`; the
  two `terminal` handlers (`:561`; `docs/handover/quadsource_atol_sweep.py:574`, `:893`) call
  `finish`, restore `SIG_DFL` and kill their own process. The pipeline heartbeats from its
  `sys.stdout` stream (`:233`, installed `:571`), on whichever thread prints.
- **The tests.** `TestStatus.test_status_is_replaced_atomically_from_the_same_directory`
  (`test_run_registry.py:605`) asserts a `.tmp` suffix, the same directory, one `os.replace` and no
  `.tmp` left; a `status.json.<unique>.tmp` satisfies all four. No other test patches
  `write_json_atomic` for a status write or names `status.json.tmp`. The sidecar tests that name
  `<sidecar>.tmp` (`test_store_copy_move`, `test_store_retire`, `test_store_sidecar`) are unaffected,
  because `write_json_atomic` is unchanged.
- **`Run(path)`** is public (`__init__.py:531`; the README's usage). SGK's documented manual remedy
  calls `Run.finish` through it, so a second object for one directory in one process is real.
- **The package** uses no `signal` (`git grep` finds only `finish`'s docstring, `:632`). The suite
  is 307 with one skip on macOS; `black --check runregistrykit docs` reports 30 files.
