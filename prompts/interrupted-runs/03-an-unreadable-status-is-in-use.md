# Prompt 03 — an unreadable status is in use

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 02c has landed and been reviewed (`35ce264`; the review `31933c4`; CI run `39072902589` green,
  recorded in `0c75dd3`).
- The user has taken **L6**, as (a) refined (README §6.2, 2026-10-18): this prompt is written for
  it.
- `git diff --stat 35ce264 HEAD -- runregistrykit pyproject.toml .github` is empty: the package is
  02c's.
- The suite is `Ran 329 tests … OK (skipped=1)` on macOS, and `git status` is clean in this
  repository.

**Closes:** `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`. **Opens:** only
what the work finds. **Narrows:** nothing planned. Not touched:
`[03-a-run-whose-manifest-cannot-be-read-names-no-store]`, opened at this prompt's writing (§"At
writing"), which has no owner.

**Recommended model:** **Sonnet**, as the plan says. The rule is one filter and its words; the
weight is in the tests, a table of thirteen status forms against six store operations, and in
keeping every existing refusal's text.

**Read first:**

1. [`README.md`](README.md): §0, §1, §5 (all of it; rules 6, 7, 8 and 10 especially), §6.2 L6 with
   its 2026-10-18 note, and L7–L9 (what 04 and 05 will build on this prompt).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md) §3:
   `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` in full, its "Measured at
   writing 03" paragraph above all, and `[03-a-run-whose-manifest-cannot-be-read-names-no-store]`.
3. `runregistrykit/__init__.py`: `TERMINAL_STATES` `:104`; `read_json` `:237-244`; the writer's
   base read `:375`; `liveness` `:595-639` (its empty payload `:619`); `Run.status` `:722-723`;
   `Run.finish` `:788`, `_fingerprint_results` `:825` (`taken_by=self` `:840`); `list_runs`
   `:1129-1184` (the manifest read `:1158`, the status read `:1159`).
4. `runregistrykit/stores.py`: the module docstring `:102-107`; `runs_naming` `:957-995` (its
   `has_manifest` skip `:973`); `_running_runs_naming` `:998-1018` (the filter `:1017`);
   `_describe_running` `:1021-1038`; `_refuse_if_in_use` `:1041-1053`; the four other callers and
   their remedy texts: fingerprint `:1350-1357`, retire `:1676-1682`, amend `:2029-2033`, copy and
   move through `_refuse_if_in_use` `:1114`.
5. `runregistrykit/__main__.py`: `store show`'s runs `:185-201`; `list` `:530-596` (the marker
   `:558`, the stale line `:578-585`).
6. `runregistrykit/tests/test_host_stores.py`, all of it (the model for the store tests);
   `test_store_retire.py` `RetireTestCase` and `a_full_store` (`:102-121`);
   `store_fixtures.py` `a_running_run` and `a_stale_run` (`:145-153`); `test_run_registry.py`
   `TestLister` (`:682-715`); `test_host.py`'s `list` test (`:631-677`);
   `.github/workflows/tests.yml` `:89`.
7. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers are the package's at `0c75dd3`, which are `35ce264`'s.

---

## 1. What is wanted

The store operations count a run as in use only when its `status.json` says `running`
(`stores.py:1017`). A run whose status says anything else, or nothing, is not counted, however
alive its process. `list_runs` reads the status as `read_json(…) or {}`, so a missing, torn or
non-JSON file is state `None`. Measured at writing (§"At writing"): with a live run on a full
store, in **10 of 13** unreadable or unrecognised forms of its `status.json`, copy, move,
fingerprint (and `--write`), retire's dry run and amend all proceeded, and `list` showed the run
with no marker. In the other **3**, a status that is JSON but not an object (`[1]`, `"x"`, `5`),
`list_runs` raises `AttributeError`, so `list` and every store operation on every store under that
runs root raise too, and `Run.finish`, the remedy the refusals name, raises on the same files.

Under L6 (a) refined:
- **a run whose manifest names the store is in use unless its status says a terminal state.** A
  status that cannot be read (missing, not JSON, not a JSON object), one with no state, a `null`
  state, a state that is not a string, or a string the registry never writes, is in use, as a
  `running` one is. The refusal says which, and that the registry cannot tell whether the run is
  running;
- **`list` marks such a run `!!`**, when it has a manifest, with a line on stderr;
- **a status or a manifest that is JSON but not an object is read as unreadable, never raised
  on**: `list_runs`, `liveness` and the status writer read it as an empty status, so `list` lists,
  the store operations refuse instead of raising, and `Run.finish` ends the run.

The registry still does not decide that a run is dead (README §5 rule 9). A person who knows the
run is over ends it with `Run.finish`, as for a stale run, and 04 gives that a command.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`, `runregistrykit`
editable. **Install nothing** into `venv/`.

### 2.2 Reading a status (`runregistrykit/__init__.py`)

- **One private helper, beside `read_json`**, that takes what `read_json` returned for a
  `status.json` and gives the payload the registry reads: the object itself if it is a `dict`,
  and `{}` for anything else (`None`, a list, a string, a number, `true`). The agent names it.
- **`list_runs`** reads each status through it (`:1159`), and each entry gains one key,
  **`status_readable`**: true iff `status.json` parsed as a JSON object. A `manifest.json` that
  parses but is not an object is read as no manifest: `has_manifest` false, and every manifest
  field read from `{}` (`:1158` and the `(manifest or {})` reads after it). `list_runs`' docstring
  says both.
- **`liveness`**: a status that is not a `dict` is `unknown`, by the same rule as an empty one
  (`:619`), so the public function never raises on one. Its docstring's step 1 says so.
- **`Run.status()`** (`:723`) returns the helper's payload.
- **The writer's base read** (`:375`, `read_json(path) or {}`) reads through the helper, so that
  `Run.finish` (and every write) on a non-object file composes from `{}`, as it does for a missing
  or torn one today. This is the only change in the writer's section. 02b's and 02c's sweeps run
  over it unchanged: if the helper is defined inside the section, they sweep it too, and it must
  pass them; defined outside, they do not. The agent says which in the log.

Nothing written changes: no key of `status.json`, the manifest, `checkpoint.jsonl` or a sidecar is
added, removed or renamed (README §5 rule 7). `list_runs`' entries are a return value, not a file;
the new key is for 06's release notes.

### 2.3 The in-use rule (`runregistrykit/stores.py`)

- **`_running_runs_naming`** (`:998`) keeps every entry naming the store whose `state` is **not
  in `TERMINAL_STATES`**, instead of only `running` (`:1017`), with the `exclude` rule unchanged.
  Its docstring, and its name if the agent renames it (then every caller), say that the set is
  "every run that names the store and has not finished": `running` (alive, stale or foreign), or
  a status that does not say. `TERMINAL_STATES` is imported from the core, never spelled again.
- **`_describe_running`** (`:1021`) describes such an entry in its own words, keeping today's
  words for a `running` one exactly (every existing refusal test asserts them):
  - `status_readable` false: `run <id>'s status cannot be read (status.json is missing, is not
    JSON, or is not a JSON object), so whether it is running cannot be told; it names this store
    by its <matched>`;
  - readable, its state not `running` and not terminal: `run <id>'s status says neither running
    nor finished (state <repr of the state, or "none">), so whether it is running cannot be told;
    it names this store by its <matched>`.
  The agent may reword these within the same facts; the tests assert the fragments it chooses,
  and the log quotes them.
- **The remedy sentences** of the five refusals (copy and move `:1050-1052`, fingerprint `:1355`,
  retire `:1679-1682`, amend `:2032-2033`) keep their present words for a stale run, and gain, when
  any entry is not `running`, one sentence: a run whose status does not say whether it is running
  is ended by a person, with `Run.finish`, once they have checked that it is not. 04 replaces
  "with `Run.finish`" by its command in all of them; keep the words in one place if that is
  simple.
- **The module docstring** (`:102-107`) says that copy, move, fingerprint, retire and amend refuse
  a store that any run names whose status does not say it has finished: `running`, alive, stale or
  on another host, or a status that cannot be read or names no state the registry writes.
- **`runs_naming`** (`:957`) is not changed: it already skips an entry with no manifest (`:973`),
  which after §2.2 includes a manifest that is not an object. `store show` (`__main__.py:188`) lists
  what `runs_naming` returns, as now.
- **A resumed run's `finish(fingerprint=True)`** (`_fingerprint_results`, `taken_by=self`) is
  refused by a predecessor whose status cannot be read, as by a stale one: it records
  `fingerprint_error` naming it. No code changes for that; a test pins it.

### 2.4 `list` (`runregistrykit/__main__.py`)

- A row whose `liveness` is `unknown` **and** whose entry `has_manifest` is marked **`!!`**
  (`:558`). A directory with no manifest (a run that predates the registry) is not marked, as now.
- After the existing stale line (`:578`), when any row is so marked, one line on stderr beginning
  `!! ` that counts them and says the registry cannot tell whether they are running, that the store
  operations count them as in use, and that a person looks and ends one with `Run.finish` once it
  is known not to be running. The agent chooses the words; a test asserts them.
- The summary line and every other column are unchanged.

### 2.5 What does not change

- Every existing test, in what it asserts. `git diff 35ce264 -- runregistrykit/tests` adds files
  and changes none, except `.github/workflows/tests.yml`'s core line (§2.6).
- The writer, except the one base read (§2.2). `write_json_atomic`. `begin` (05 changes it).
- `liveness`' values: still `alive`, `stale`, `foreign`, `finished`, `unknown`.
- Every refusal's present text for a `running` run, and for the runs root not being a directory.

### 2.6 The new tests

Two new modules, as 01's were: a core one, added to the workflow's core job (`tests.yml:89`), and
a store one.

**`runregistrykit/tests/test_unreadable_status.py`** (core; no store layer imported):
- `list_runs` over a runs root holding one run per form of §"At writing"'s table (missing, empty
  file, torn, not JSON, `null`, `[]`, `[1]`, `"x"`, `5`, `{}`, state `null`, state `"paused"`,
  state `5`) and one finished run: it returns every entry, `status_readable` as the form says,
  `liveness` `unknown` for each form, and the finished run `finished`;
- a manifest that is `[1]`: `list_runs` returns the entry with `has_manifest` false;
- `liveness([1], …)`, `liveness("x", …)`, `liveness(5, …)`: `unknown`;
- **the remedy**: `Run(path).finish("killed", exit_code=137)` on a run with each form: it returns,
  and the file then parses, says `killed` and 137;
- `list --root`: each form's row starts `!! `, the finished run's does not, a directory with no
  manifest does not, and stderr has the new line once with the count; exit 0;
- **an old record** (README §5 rule 8): a `v0.1.0`-form status (no `host`), `running` and
  `done`, built in the test: `status_readable` true, judged as `v0.1.0` judged it.

**`runregistrykit/tests/test_unreadable_status_stores.py`** (store layer; on
`test_store_retire.RetireTestCase`, as `test_host_stores` is):
- **the planner's probe as a test**: for each of the thirteen forms, a live run begun in the test's
  own process on a full store, its `status.json` then given that form; copy, move, fingerprint,
  fingerprint `--write`, retire `--dry-run` and amend each refuse with `RuntimeError`, naming the
  run and the form's words, and `tree_state` of the temporary directory is unchanged by each;
- **a real retire** is refused for a torn status, and the store's primary and shards still exist
  (the board's measurement, where it deleted them);
- **the resumed run**: a second run on the store, whose predecessor's status is torn,
  `finish("done", exit_code=0, fingerprint=True)`: `done`, no `fingerprint`, a `fingerprint_error`
  naming the predecessor;
- **a store whose runs have all finished** (`done`, `failed`, `killed`) is accepted by fingerprint
  and by retire's dry run; a terminal `v0.1.0`-form status (no `host`) likewise;
- the stale and foreign refusals' existing fragments still appear when such a run and an unreadable
  one both name the store (the remedy sentence added once).

Both modules build everything in `tempfile` directories through the existing fixtures, and signal
nothing.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root, `TMPDIR`
   in your scratch: **`Ran 329 + N tests … OK (skipped=1)`**. Give the per-module counts and the
   time.
2. **The core alone**, in a fresh scratch venv without `[stores]`, as 02c's §3.2, with
   `test_unreadable_status` added to the four core modules: 87 + N₁ tests pass, with
   `datastorekit`, `ray` and `sqlalchemy` absent. Remove the venv afterwards.
3. **The planner's probe, re-run** from §"At writing" in your scratch against the change: every
   form, every operation refused; `list_runs` raises on none. And against `35ce264` (by `git
   archive`): the table of §"At writing". Give both tables. Not committed.
4. **The writer's sweeps** (`test_status_writes`) pass unchanged; say whether the helper is in the
   swept section, and the sweeps' instruction counts before and after.
5. **The tests catch behaviour** (README §5 rule 10). Each mutation applied in a scratch clone, the
   named tests run, and reverted:
   - (m1) the filter back to `entry["state"] == "running"`;
   - (m2) the filter counting a run in use when `status_readable` is false or the state is
     `running`, and no other (L6 (a) as first planned, not refined): the `{}`, state `null`,
     `"paused"` and `5` cases must fail;
   - (m3) `list_runs` reading the status as `read_json(…) or {}` again;
   - (m4) the writer's base read back to `read_json(path) or {}`: the remedy test must fail;
   - (m5) `list`'s `!!` for an `unknown` row with a manifest removed;
   - (m6) the agent's own: one more change to the rule, its words or `list`, that a test catches.

   Each must fail at least one test, named in the log. A mutation no test catches is a stop.
6. **Nothing outside temporary directories**, as 02c's §3.9; `git grep -n 'signal' --
   'runregistrykit/*.py' ':!runregistrykit/tests'` finds only `finish`'s docstring.
7. `./venv/bin/black --check runregistrykit docs` is clean, at **33** files (two new modules).
8. **CI.** Pushing is the user's. The new core module first runs in the core job and on Linux;
   record that the review is to read its result there.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` changes `__init__.py`, `stores.py`, `__main__.py`, and
   adds the two test modules; `.github/workflows/tests.yml` changes on its core line only.
2. §3.1–§3.7 hold. Every test that existed at `35ce264` passes unchanged in what it asserts.
3. **The planner's probe passes as a test**: for each of the thirteen forms each operation
   refuses, and the store is untouched.
4. **The records**, in the same commit:
   - the log, `logs/03-an-unreadable-status-is-in-use.md`, per README §5.1: the suite before (329)
     and after, the core run, both probe tables, the sweeps, every mutation as a diff, and the
     refusal texts as shipped;
   - this board: the header, §1's row for 03, §1.1's C1, §3/§4 (the issue moved to §4 with what
     resolved it and the tests that pin it), and a "Package lines (03, this commit)" sentence on
     each §3 entry whose cited lines 03 moves;
   - `docs/OPEN_ISSUES.md`: the row deleted, the count (10 → 9), the date;
   - `prompts/INDEX.md`: the campaign's line;
   - this campaign's README §2: 03's status.

---

## 5. Stop conditions — stop and ask the user

- An existing test fails, or would need a change to what it asserts; 02b's or 02c's sweeps fail.
- A mutation of §3.5 is caught by no test.
- Any record would change form: a key of `status.json` added, removed or renamed, or the manifest,
  `checkpoint.jsonl` or a sidecar written differently. `write_json_atomic` changed.
- The design would have the package end, skip or override a run without a person's command, or
  treat a run with an unreadable status as finished anywhere (README §5 rule 9).
- The rule would need a manifest that cannot be read to name a store (that is
  `[03-a-run-whose-manifest-cannot-be-read-names-no-store]`, not this prompt's).
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory; a test signals any process.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything into `venv/`.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `runregistrykit/__init__.py`, `runregistrykit/stores.py`,
  `runregistrykit/__main__.py`; `runregistrykit/tests/test_unreadable_status.py` and
  `test_unreadable_status_stores.py`; `.github/workflows/tests.yml`'s core line; the log, this
  board, the campaign README's §2 row, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It does not add `end` (04) or change `begin` (05). It does not change `Run.finish`, which ends
  whatever run it is called on, as now.
- It does not make a run whose manifest cannot be read name a store, and does not change
  `Run.__init__`'s manifest read (`:667`).
- It writes no README usage or release notes (06), and makes no tag.

---

## At writing (2026-10-18, at `0c75dd3`)

Measured for the README's row and the orchestrator, in the session scratchpad with `TMPDIR` there,
by a scratch probe (not committed) on `test_host_stores`' fixtures: per form, a full four-shard
registered store, a run begun on it in the probe's own process (its pid alive), and its
`status.json` then replaced; `list_runs`, `list --root`, and the six operations of
`test_host_stores.refusals` with a destination per case. After each case the status was put back
to `done`, so that one case's file could not affect the next.

| Form of `status.json` | `list_runs` | `list` row | the six operations |
|---|---|---|---|
| missing | state `None`, `unknown` | no marker | **all proceed** (copy, move, `--write` and amend change files) |
| empty file | the same | no marker | **all proceed** |
| torn (the first half) | the same | no marker | **all proceed** |
| not JSON | the same | no marker | **all proceed** |
| `null` | the same | no marker | **all proceed** |
| `[]` | the same | no marker | **all proceed** |
| `[1]` | **raises** `AttributeError: 'list' object has no attribute 'get'` | `list` raises | **all raise** `AttributeError` |
| `"x"` | **raises** (`'str'`) | `list` raises | **all raise** |
| `5` | **raises** (`'int'`) | `list` raises | **all raise** |
| `{}` | state `None`, `unknown` | no marker | **all proceed** |
| state `null` | the same | no marker | **all proceed** |
| state `"paused"` | state `'paused'`, `unknown` | no marker | **all proceed** |
| state `5` | state `5`, `unknown` | no marker | **all proceed** |

A non-object status breaks more than its own run. The first draft of the probe left the `[1]` file
in place, and the next case's `a_full_store` raised `AttributeError` from its own
`fingerprint_store(write=True)`, through `runs_naming` and `list_runs`: one bad directory stops
every fingerprint of every store under that runs root.

**The remedy on each form**, `Run(path).finish("killed", exit_code=137)` on a fresh run (core
only): missing, torn, `null`, `{}` and `"paused"` end `killed` (the keys `exit_code`, `heartbeat`,
`state`, and `pid` for `"paused"`); **`[1]`, `"x"` and `5` raise** `AttributeError: … has no
attribute 'update'`, from the writer's base read (`__init__.py:375`).

**The manifest.** With the status left `running` and the pid alive: a torn manifest and a missing
one give `has_manifest` false, and `fingerprint_store` **proceeds** on the store the run is writing;
a manifest that is `[1]` makes `list_runs` raise. The first is
`[03-a-run-whose-manifest-cannot-be-read-names-no-store]`, opened with this prompt and not its to
fix; the second is fixed here, by §2.2.

**Existing tests that see the change**: none found by reading. `TestLister` and the `list` test of
`test_run_registry` use a directory with **no** manifest, which stays unmarked; `test_host`'s `list`
test has no `unknown` row; every store refusal test names a `running` run, whose words are kept.
The suite at `0c75dd3`: `Ran 329 tests`, `OK (skipped=1)`; `black --check runregistrykit docs`, 31
files.
