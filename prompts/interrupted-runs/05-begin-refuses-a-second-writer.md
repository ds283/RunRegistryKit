# Prompt 05 — begin refuses a second writer

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 04 has landed and been reviewed (`5e20772`; the review `46e29b9`; CI run `39122974980` green,
  recorded in `d8f8de4`).
- The user has taken **L9** as (a) (README §6.2, 2026-10-18), and has asked for
  `[04-a-pid-out-of-range-makes-pid-alive-raise]` to be fixed in this prompt (the same day): this
  prompt is written for both.
- `git diff --stat 5e20772 HEAD -- runregistrykit pyproject.toml .github` is empty: the package is
  04's.
- The suite is `Ran 378 tests … OK (skipped=1)` on macOS, and `git status` is clean in this
  repository.

**Closes:** `[00-begin-does-not-refuse-a-second-writer]` and
`[04-a-pid-out-of-range-makes-pid-alive-raise]`. **Opens:** only what the work finds.
**Narrows:** nothing planned. Not touched: `[04-a-killed-process-not-yet-reaped-answers-kill-0]`
(a killed child not yet reaped still answers `kill -0`, so `begin` refuses its store as alive; that
is the issue's, and errs towards in use), nor the four other open §3 entries.

**Recommended model:** **Sonnet**, as the plan says. The check is the store operations' own,
called from one more place; `pid_alive`'s fix is one `except`. The weight is in keeping every
existing test's assertions as they are while six of them change how they build their runs (§2.4),
and in a refusal whose words 04 fixed.

**Read first:**

1. [`README.md`](README.md): §0 (the boundary), §1, §5 (all of it; rules 6, 7, 8, 9 and 10
   especially), §6.2 L4, L6, L8 and L9 with its 2026-10-18 note.
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md) §3: `[00-begin-does-not-refuse-a-second-writer]`
   in full, its "Measured at writing 05" paragraph above all, and
   `[04-a-pid-out-of-range-makes-pid-alive-raise]` with its **Assigned** line.
3. `runregistrykit/__init__.py`: `TERMINAL_STATES` `:105`; `_END` `:109`; `pid_alive` `:403` (its
   `int()` `:412-413`, its `os.kill` `:418`); `liveness` `:608`; `begin` `:983`, its docstring, the
   client root located `:1069`, the tombstone check `:1074-1086` (the lazy import from `.stores`
   `:1077`, the refusal `:1080-1085`), `this_host()` `:1088`, the run directory made `:1089`;
   `list_runs` `:1144`; `_end_run` `:1219`.
4. `runregistrykit/stores.py`: the module docstring `:104-109`; `runs_naming` `:961`;
   `_running_runs_naming` `:1002`; `_describe_running` `:1029`; `_unsure_remedy` `:1064`;
   `_foreign_remedy` `:1075`; `_refuse_if_in_use` `:1087`, its text `:1096-1105`.
5. The tests: `test_run_registry.py` `RegistryTestCase` (`begin` `:125`, `a_dead_pid` `:137`,
   `a_dead_run` `:147`, `a_pipeline_run` `:505`); `store_fixtures.py` `StoreTestCase`, its runs
   section `:143-153` (`a_running_run`, `a_stale_run`); `test_host.py` (`a_status`, `another_id`);
   `test_unreadable_status.py` (`FORMS`, `give_status_the_form`); `test_end.py` and
   `test_end_stores.py`, 04's, the models for the two new modules; the six tests of §2.4's table;
   `.github/workflows/tests.yml:89`.
6. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers are the package's at `d8f8de4`, which are `5e20772`'s.

---

## 1. What is wanted

`begin` reads its `results` store's sidecar only to refuse a tombstone. It does not ask whether a
run already names that store, so a second run is begun on a store a live run is writing, without a
word (the board's entry, measured again at writing). The store operations make that check;
`begin` does not.

Under L9 (a):
- **`begin` refuses**, before the run directory is created, when any run under its runs root that
  has not finished names its `results` store, by path or by `results_store_id`: `running` (alive,
  stale or `foreign`), or a status that does not say (03's sense). It is the store operations'
  rule (`_running_runs_naming`), called from one more place, and **there is no override**. A stale
  run is ended with `end` first, and then `begin` is called again.
- **The refusal names the remedy** in 04's words: `end` for a stale run, with the sentences for a
  run on another host and a status that does not say when they apply.
- **A store whose runs have all finished** (`lost` included) is accepted, as is one no run names,
  and a `begin` with no `results`: nothing changes for them.

And, at the user's request, **`pid_alive` returns false for a pid outside the platform's range**
instead of raising, so that one such record under a runs root no longer makes `begin`, `list`,
`end` and every store operation under it raise.

The registry still does not decide that a run is dead (README §5 rule 9), and still takes no
lock: two `begin`s racing each other can both pass the check, as the store operations' docstring
says of them.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`, `runregistrykit`
editable. **Install nothing** into `venv/`.

### 2.2 The check (`runregistrykit/__init__.py`, `begin`)

- **Where.** In `begin`, inside `if results:`, **after** the tombstone check and before
  `this_host()` and `os.makedirs`: a retired store is still refused first, with its own words, and
  nothing is created by a refusal. The lazy import from `.stores` (`:1077`) gains the names the
  check needs; `begin` imports nothing new at module scope, and the core still imports no store
  dependency (the core job proves it).
- **What.** `_running_runs_naming("begin", [os.path.abspath(results)], results_store_id,
  runs_root, client)`, where `runs_root` is `root or client.runs_root`, the root this run is about
  to be created in. `os.path.abspath(results)` is the path `read_sidecar` reads and `_repo_path`
  records; `runs_naming` `realpath`s both sides. Nothing is excluded: the run being begun does not
  exist yet.
- **A runs root that does not exist yet** is not refused: `begin` creates it, and no run can name
  the store from it. So the check is made only when `os.path.isdir(runs_root)`.
  `_running_runs_naming`'s own refusal of a runs root that is not a directory is for the store
  operations, and is not reached from `begin`.
- **What is matched** is exactly what the store operations match: the manifest's `results` by
  path, and its `results_store_id` when the new run's store has a problem-free registry sidecar.
  A legacy sidecar, or none, matches by path alone.
- **`begin`'s docstring** gains one paragraph: the refusal, what it counts, that `end` is the
  remedy for a stale run, that it is a check and not a lock (a run begun at the same moment is
  not seen), and that only the runs root this run is created in is read.

`begin`'s signature, its manifest, its first `status.json`, `this_host()`'s reading and every other
line of it are unchanged.

### 2.3 The refusal's words

`RuntimeError`, in the form of the tombstone refusal beside it and of copy's remedy:

```
Cannot begin run <id> with results "<results>": <_describe_running(running)>. A stale run is
ended by a person, with `<_END>`, before another run is begun on its store; the registry does not
decide that a run is dead. [<_foreign_remedy(running)>. ][<_unsure_remedy(running)>. ]No run
directory was created
```

`<results>` is `results` as it was given, as the tombstone refusal prints it. The two optional
sentences are 04's helpers, called as the store refusals call them, each once and only when it
applies, the foreign one first. No word of the command is spelled by hand; it comes from `_END`.
No new text uses the word `signal` (§3.6).

### 2.4 The six tests that build two unfinished runs on one store

Measured at writing (§"At writing"): with the check in, six existing tests error, each at a
`begin` that is refused. None of them tests `begin`. Each builds, through `begin`, two runs that
have not finished on one store, which `begin` no longer makes; each then tests a store refusal's
words, or a resumed run's fingerprint refused by a predecessor.

| Test module | Test | The second `begin` |
|---|---|---|
| `test_end_stores.py` | `TestTheWords.test_a_run_on_another_host_adds_the_sentence_once` | `a_stale_run` after a `running` run moved to another host |
| `test_end_stores.py` | `TestTheWords.test_alive_and_stale_here_give_the_old_text_with_the_command` | `a_stale_run` after `a_running_run` |
| `test_store_fingerprint.py` | `TestFinish.test_another_running_run_is_recorded_and_the_run_still_ends` | `self.begin("second", …)` after `a_running_run` |
| `test_unreadable_status_stores.py` | `TestAnUnreadableStatusIsInUse.test_a_refusal_for_running_runs_alone_has_no_new_sentence` | `a_stale_run` after `a_running_run` |
| `test_unreadable_status_stores.py` | `TestAnUnreadableStatusIsInUse.test_a_resumed_runs_fingerprint_is_refused_by_an_unreadable_predecessor` | `self.begin("resumed", …)` after a torn predecessor |
| `test_unreadable_status_stores.py` | `TestAnUnreadableStatusIsInUse.test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once` | `a_running_run` twice after `a_stale_run` |

What they test still matters: a run begun before 05, or begun under another runs root, or on
another machine and copied in, leaves exactly that state, and the store operations and
`finish(fingerprint=True)` must still refuse it. So their **setup** changes and nothing they
assert does:

- **One fixture is added**, in `store_fixtures.py`'s runs section, beside `a_running_run` and
  `a_stale_run`, as a method of `StoreTestCase`: a context manager (for example
  `set_aside(*runs)`) that moves each given run's directory out of the runs root, to a sibling
  directory in the test's temporary directory, for the duration of its body, and moves it back
  after, **byte for byte**, whatever the body raises. A run begun in the body does not see the runs
  set aside; afterwards both are under the runs root. It writes no record and changes no field.
  Its docstring says why it exists: `begin` no longer makes two unfinished runs on one store, and
  these tests need the state an older or a copied record leaves.
- **Each of the six** wraps its later `begin` (or `a_running_run`, `a_stale_run`) in the fixture,
  setting aside the runs begun before it, and changes nothing else. `git diff -w 5e20772 --
  runregistrykit/tests` on those three modules shows only the `with` lines and the fixture; with
  `-w` dropped, the re-indented lines of the wrapped calls and nothing else.

This is the one change to existing tests this prompt makes. Any other existing test that fails is
a stop.

### 2.5 `pid_alive` (`runregistrykit/__init__.py:403`)

- **The fix.** A pid that `int()` cannot convert because it is out of range (`float("inf")`, which
  `json` parses from `Infinity`), and one that `os.kill` rejects as outside a C `int` (`2**31` and
  above), each return **false**: no process has such a pid. `OverflowError` is caught beside the
  existing exceptions at both places, and nothing else changes: a pid `<= 0`, `None`, `"x"` and a
  live or dead pid give what they give today.
- **The docstring** gains one sentence: a pid outside the platform's range names no process.
- `pid_alive` is public (`__all__`); its value for such a pid goes from raising to `False`. 06's
  release notes say so. `liveness`, `list_runs`, `list`, `end` and the store operations are not
  changed: they stop raising because `pid_alive` does.

### 2.6 What does not change

- Every existing test, in what it asserts. `git diff 5e20772 -- runregistrykit/tests` adds two
  files and changes `store_fixtures.py` by the fixture and the six tests by §2.4's wrapping, and
  nothing else.
- `Run.finish`, `liveness`' code, `list_runs`, `_end_run`, the writer (`_write_status`,
  `_land_status`, `write_json_atomic`), `runs_naming`, `_running_runs_naming`, `_describe_running`,
  `_unsure_remedy`, `_foreign_remedy`, every store operation and its words, `store show`, `list`,
  `end`, `__main__.py`.
- The manifest, `status.json`, `checkpoint.jsonl` and every sidecar: nothing the registry writes
  changes (README §5 rule 7). A refusal writes nothing.
- `__all__`.

### 2.7 The new tests

Two new modules: a core one, added to the workflow's core job (`tests.yml:89`), and a store one.

**`runregistrykit/tests/test_second_writer.py`** (core; no store layer imported by the test, on
`test_run_registry.RegistryTestCase`; its stores are plain files with no sidecar, as
`a_pipeline_run` makes them, so they match by path):
- **every refusal**, each leaving the runs root's listing exactly as it was (no run directory, no
  file), the message naming the earlier run's id, its words (§2.3) and "No run directory was
  created": an earlier run alive (begun in the test's own process); stale (`a_dead_run`); from an
  earlier boot of this host (`host.boot` changed, a live pid: stale by L3, refused); on another host
  (`host.id` another, `foreign`, its pid not tested); each of 03's thirteen forms
  (`test_unreadable_status.FORMS`); a `v0.1.0`-form status, `running` with no `host`
  (`test_host.a_status(…, with_host=False)`), with a dead pid (README §5 rule 8: judged by its pid,
  stale, refused) and with a live one;
- **the words**: the stale remedy naming `` `python -m runregistrykit end RUN_ID --reason TEXT` ``
  once; the foreign sentence once with two foreign runs, absent with none; 03's sentence with
  `--unverified` once with two unreadable runs, absent with none; with an alive and a stale run here
  only, neither;
- **every acceptance**: a store whose earlier runs are `done`, `failed`, `killed` and `lost`; a
  store no run names; a `begin` with no `results` while a run names some store; a runs root that
  does not exist yet (`root=` a path under the temporary directory), created by `begin`;
- **the order**: a store with a tombstone and a stale run naming it is refused by the tombstone's
  words, not the check's;
- **the remedy**: a stale run on the store, `begin` refused; `_end_run` on it; `begin` again
  accepted, and its `finish("done", exit_code=0)` ends it. (The resumed run's fingerprint is the
  store module's.);
- **the runs root it reads**: an alive run under another runs root, naming the same store, does not
  refuse a `begin` with `root=` this one; the docstring's statement, pinned;
- **`pid_alive`**: `2**31`, `2**63`, `10**30` and `float("inf")` give false and do not raise; `-1`,
  `0`, `None`, `"x"`, this process's pid and a dead pid as before. Through the readers: a `running`
  status here whose `pid` is `2**31` is `stale` by `liveness`, `list_runs` returns it, `python -m
  runregistrykit list` exits 0 and marks it `!!`, and `_end_run` ends it, verified, `pid_answers`
  false; a status whose `pid` is the JSON `Infinity`, the same. And a `begin` with `results` on
  **another** store, under a runs root holding such a record, is accepted; on its own store,
  refused as stale.

**`runregistrykit/tests/test_second_writer_stores.py`** (store layer; on
`test_store_retire.RetireTestCase`):
- **the acceptance test**: on a full registered store, a child begins a run and heartbeats; it is
  sent `SIGKILL` and reaped (04's `test_end.a_hard_killed_run`). A second `begin` on the store is
  refused, naming the killed run and `runregistrykit end RUN_ID`, the temporary directory's tree
  unchanged; `end`, by the command; `begin` again accepted; its `finish("done", exit_code=0,
  fingerprint=True)` records a `fingerprint` and no `fingerprint_error`. This is SGK's resume
  after a hard kill (README §0.2), end to end;
- **matched by store id alone**: an earlier, alive run whose manifest's `results` names another
  path (set by hand in the test's temporary directory) and whose `results_store_id` is the store's:
  refused, the description saying `results_store_id`; with a legacy sidecar on the new run's store
  (no store id), the same earlier run does not refuse;
- **matched by path alone**: an alive run on a store whose sidecar is absent: refused;
- **one rule**: for one store with an alive run, `begin` and each of the six store operations
  refuse, each naming the same run;
- **`pid_alive` through the store operations**: with a `running` status whose `pid` is `2**31`
  naming one store, `fingerprint_store` on **another** store proceeds, and on its own store refuses
  it as stale.

Both modules build everything in `tempfile` directories through the existing fixtures. The only
signal sent is `SIGKILL`, to a child the test started, which it reaps.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root, `TMPDIR`
   in your scratch: **`Ran 378 + N tests … OK (skipped=1)`**. Give the per-module counts and the
   time.
2. **The core alone**, in a fresh scratch venv without `[stores]`, as 04's §3.2, with
   `test_second_writer` added to the six core modules: 125 + N₁ tests pass, with `datastorekit`,
   `ray` and `sqlalchemy` absent. Remove the venv afterwards. `test_second_writer` at
   `/opt/local/bin/python3.13` (3.13.16) with `PYTHONPATH` on the checkout.
3. **The planner's probe, re-run** from §"At writing" in your scratch, against `5e20772` (by `git
   archive`) and against the change: its table both times.
4. **What is written.** A scratch lifecycle (`begin` on a registered store with a ledger,
   `heartbeat`, `record`, `finish("done", fingerprint=True)`) at `5e20772` and at the change: the
   shape of `status.json`, the manifest, a ledger line and the sidecar identical, archive against
   archive.
5. **The six tests' setup.** `git diff -w 5e20772 -- runregistrykit/tests/test_end_stores.py
   runregistrykit/tests/test_store_fingerprint.py runregistrykit/tests/test_unreadable_status_stores.py`
   pasted in the log, showing only the `with` lines; and each of the six, run against the change
   with its `with` removed, errors at its `begin` (the reason it changed).
6. **The tests catch behaviour** (README §5 rule 10). Each mutation applied in a scratch clone, the
   named tests run, and reverted:
   - (m1) `begin`'s check removed;
   - (m2) the check counting only `alive` runs (`liveness == "alive"`);
   - (m3) the check made after `os.makedirs`, so a refusal leaves a run directory;
   - (m4) the check passed `None` for the store id, so a run named by `results_store_id` alone is
     not seen;
   - (m5) a runs root that does not exist refused (`_running_runs_naming` called unconditionally);
   - (m6) `pid_alive`'s `OverflowError` at `os.kill` not caught;
   - (m7) the remedy sentence not naming `_END`;
   - (m8) the agent's own: one more change to the check, the words or `pid_alive` that a test
     catches.

   Each must fail at least one test, named in the log. A mutation no test catches is a stop.
7. **Nothing outside temporary directories**: `git status --short --ignored` the same before and
   after the suite, and no child left (a test reaps what it starts). `git grep -n 'signal' --
   'runregistrykit/*.py' ':!runregistrykit/tests'` finds only `finish`'s docstring.
8. `./venv/bin/black --check runregistrykit docs` is clean, at **37** files (two new modules).
9. **CI.** Pushing is the user's. The new core module first runs in the core job and on Linux;
   record that the review is to read its result there.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` changes `__init__.py` (`pid_alive` and `begin` only),
   `store_fixtures.py` by the fixture, the six tests of §2.4 by their wrapping, and adds the two
   new test modules; `.github/workflows/tests.yml` changes on its core line only. `stores.py` and
   `__main__.py` do not change.
2. §3.1–§3.8 hold. Every test that existed at `5e20772` passes, unchanged in what it asserts.
3. **The acceptance test passes**: a second `begin` refused on a live run's store, a stale run's
   store, a `foreign` run's store and a store named by an unreadable status, each with no run
   directory left; a store whose runs are all terminal accepted; and the hard-killed run, ended,
   then `begin` accepted and its fingerprint recorded.
4. **The records**, in the same commit:
   - the log, `logs/05-begin-refuses-a-second-writer.md`, per README §5.1: the suite before (378)
     and after, the core run, both probe tables, §3.5's diff, every mutation as a diff, and the
     refusal text as shipped;
   - this board: the header, §1's row for 05, §1.1's B1, §3/§4 (both issues moved to §4 with what
     resolved them and the tests that pin them), and a "Package lines (05, this commit)" sentence
     on each §3 entry whose cited lines 05 moves;
   - `docs/OPEN_ISSUES.md`: the two rows deleted, the count (12 → 10), the date;
   - `prompts/INDEX.md`: the campaign's line;
   - this campaign's README §2: 05's status.

---

## 5. Stop conditions — stop and ask the user

- An existing test fails, or would need a change to what it asserts, or a change to its setup other
  than §2.4's; 02b's or 02c's sweeps fail.
- A mutation of §3.6 is caught by no test.
- Anything the registry writes would change: a key of the manifest or `status.json`,
  `checkpoint.jsonl`, a sidecar; `write_json_atomic` or the writer changed.
- The design would give `begin` an override, a parameter that skips the check, or a lock; or would
  have the package end, skip or override a run without a person's command (README §5 rule 9; L9).
- `begin`'s signature, `Run.finish`'s code, `liveness`' code, the store operations' rule or words,
  or `__all__` would change.
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory; a test signals any process but a child it started, or leaves one unreaped.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything into `venv/`.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `runregistrykit/__init__.py`;
  `runregistrykit/tests/test_second_writer.py` and `test_second_writer_stores.py`;
  `runregistrykit/tests/store_fixtures.py` (the fixture); the six tests of §2.4 in
  `test_end_stores.py`, `test_store_fingerprint.py` and `test_unreadable_status_stores.py`;
  `.github/workflows/tests.yml`'s core line; the log, this board, the campaign README's §2 row,
  `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It does not change the store operations, `end`, `list` or `store show`, nor what any of them
  says.
- It does not tell a zombie from a live process
  (`[04-a-killed-process-not-yet-reaped-answers-kill-0]`): `begin` refuses a killed child's store
  until the child is reaped.
- It does not make a run whose manifest cannot be read name a store
  (`[03-a-run-whose-manifest-cannot-be-read-names-no-store]`): `begin` does not see such a run, as
  the store operations do not.
- It does not read any runs root but the one the run is created in, and is not a lock.
- It writes no README usage or release notes (06), and makes no tag.

---

## At writing (2026-10-18, at `d8f8de4`)

Measured for the README's row and the orchestrator, in the session scratchpad with `TMPDIR` there,
by scratch probes (not committed) on `test_store_retire.RetireTestCase`, against this tree and
against a **candidate** of §2.2 in a scratch clone (the check as `_running_runs_naming`, made only
when the runs root is a directory, after the tombstone check; its words not §2.3's). The candidate
is evidence for the design, not the design.

**A second `begin` on a store an earlier run names** (each row its own full store; "no dir left":
the runs root's listing unchanged by the refusal):

| The earlier run | Today | The candidate |
|---|---|---|
| alive, in the probe's own process | **begun** | refused, no dir left |
| stale (a dead pid) | **begun** | refused, no dir left |
| `foreign` (`host.id` another) | **begun** | refused, no dir left |
| a torn `status.json` | **begun** | refused, no dir left |
| state `"paused"` | **begun** | refused, no dir left |
| every one terminal (`done`, `failed`, `killed`, `lost`) | begun | begun |
| none | begun | begun |
| stale, its `pid` set to `2**31` | **begun** | raised `OverflowError` |
| on **another** store, its `pid` `2**31` | **begun** | raised `OverflowError` |
| none, the runs root absent | begun | begun |

**The suite against the candidate:** `Ran 378 tests`, `FAILED (errors=6, skipped=1)`, the six of
§2.4, each at a refused `begin`. No other test failed.

**The cost.** `begin` with `results`, best of five, with N finished runs under the root: 0 runs,
53 ms (55 today); 100, 78 ms (81); 1000, 298 ms (51). SGK's `var/runs/` holds 83 run directories;
CPBH's and SI's none.

**`pid_alive`.** `os.kill` raises `OverflowError` for `2**31`, `2**63`, `10**30` and `-2**31 - 1`
(the last never reached: `pid <= 0` returns first); `int(float("inf"))` raises `OverflowError`
too, and `json` parses `Infinity` to `float("inf")`. Today one such record under a runs root makes
`list`, `end` and every store operation under it raise (04's issue; `fingerprint_store` measured
at 04's review); with the candidate, every `begin` that names a results store raises as well,
which is why the user asked for the fix here. A `pid` of JSON `true` is `int` 1, which answers
`kill -0` (`PermissionError`, `launchd`): such a run is `alive`. No writer records one; not this
prompt's, and erring towards in use.

**The clients**, read through `git` at SGK `79434bf` and nothing run: SGK begins a run in three
drivers, `docs/gktk-remedial/scoped_pipeline_run.py:544` and
`docs/handover/quadsource_atol_sweep.py:556` (`--build`) and `:869` (the sweep's parent). The
sweep's children are started with `--child` and never call `begin`, so each process begins at most
one run on a store. `--build --resume` begins a new run on a store an earlier build wrote: after a
`SIGTERM`, whose handler records `killed`, it is accepted; after a hard kill, it is refused until
`end`. That is L9's intent, and SGK's adoption campaign meets it. CPBH and SI call nothing of the
registry yet.

The suite at `d8f8de4`: `Ran 378 tests`, `OK (skipped=1)`; `black --check runregistrykit docs`, 35
files.
