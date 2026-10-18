# Prompt 04 — end a run

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 03 has landed and been reviewed (`ab0cad9`; the review `4b55750`; CI run `39083674030` green,
  recorded in `9e38581`).
- The user has taken **L7** and **L8**, each as (a) (README §6.2, 2026-10-18): this prompt is
  written for them.
- `git diff --stat ab0cad9 HEAD -- runregistrykit pyproject.toml .github` is empty: the package is
  03's.
- The suite is `Ran 347 tests … OK (skipped=1)` on macOS, and `git status` is clean in this
  repository.

**Closes:** `[a3-v2-a-hard-killed-run-blocks-its-store]`. **Opens:** only what the work finds.
**Narrows:** nothing planned. Not touched: `[04-a-killed-process-not-yet-reaped-answers-kill-0]`,
opened at this prompt's writing (§"At writing"), which has no owner; nor the four other open §3
entries.

**Recommended model:** **Opus**, as the plan says. The command is small; the weight is in fixing a
record that every client will read (README §5 rule 7), in a check whose every branch is a person's
safety, in rewording five refusals and two `list` lines whose words nine existing assertions pin,
and in a test that hard-kills a child.

**Read first:**

1. [`README.md`](README.md): §0 (the boundary: the registry does not decide that a run is dead),
   §0.1, §1, §5 (all of it; rules 6, 7, 8, 9 and 10 especially), §6.2 L3, L4, L7 and L8 with their
   2026-10-18 notes, and L9 (what 05 builds on this prompt).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md) §3:
   `[a3-v2-a-hard-killed-run-blocks-its-store]` in full, its "Measured at writing 04" paragraph
   above all, and `[04-a-killed-process-not-yet-reaped-answers-kill-0]`.
3. `runregistrykit/__init__.py`: `__all__` `:80-102`; `TERMINAL_STATES` `:104`; `now_iso` `:118`;
   `git_provenance` `:145`; `read_json` `:237`, `_json_object` `:247`; `pid_alive` `:398`;
   `heartbeat_age` `:423`; `this_host` `:569`; `liveness` `:603-651` (its host rule `:633-640`);
   `Run` `:669`, `Run.status` `:730`, `Run._update` `:733`; `Run.finish` `:796` (its docstring
   `:797-798`, its check `:813`); `_fingerprint_results` `:833` (`taken_by=self` `:848`); `begin`
   `:976`; `list_runs` `:1137`.
4. `runregistrykit/stores.py`: the module docstring `:102-109`; `_running_runs_naming` `:1001`;
   `_describe_running` `:1028`; `_unsure_remedy` `:1063-1071`; `_refuse_if_in_use` `:1074-1091`;
   the remedy texts of fingerprint `:1391-1398`, retire `:1716-1725` and amend `:2071-2078`.
5. `runregistrykit/__main__.py`: the module docstring `:16-37`; `main` `:419`, its subparsers
   `:428-534`, where it locates the client root `:536-547`; `list`'s stale line `:587-593`, the
   line 03 added `:595-603`, the foreign line `:604-613`.
6. The tests: `test_run_registry.py` `RegistryTestCase` (`begin` `:125`, `a_dead_pid` `:137`,
   `a_dead_run` `:147`); `test_host.py` (`a_status`, `HERE`, `ELSEWHERE`); `test_unreadable_status.py`
   (`FORMS`, `give_status_the_form`) and `test_unreadable_status_stores.py`, the models for the two
   new modules; `test_store_retire.py` `RetireTestCase`; `store_fixtures.py` `a_running_run`,
   `a_stale_run`; and the nine assertions of §2.4's table; `.github/workflows/tests.yml:89`.
7. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers are the package's at `9e38581`, which are `ab0cad9`'s.

---

## 1. What is wanted

A run killed by `SIGKILL`, power loss, a reboot or the OOM killer never reaches `Run.finish`, so
its `status.json` says `running` for ever. `list` calls it stale, rightly, and since 03 every store
operation refuses its store, as does a resumed run's `finish(fingerprint=True)`. The refusals name
the remedy, "ended by a person, with Run.finish". There is no command, and `Run.finish` checks
nothing: measured at writing, it ends the record of a live run as readily as a dead one's (§"At
writing").

Under L7 (a) and L8 (a):
- **`python -m runregistrykit end RUN_ID --reason TEXT [--unverified]`**, run by a person, records a
  run as ended: the new terminal state **`lost`** (the registry never saw how the run ended), exit
  code `null`, and an **`ended`** record of who, when, why, at what `git_head`, on what host, and
  the evidence checked. The manifest is not written and nothing is deleted.
- **It checks first, and refuses** unless the evidence on this machine says the run is over: on
  this host, a boot other than this one, or a pid that does not answer `kill -0`. A live pid is
  refused, with no override. A run on another host, or one whose status does not say whether it is
  running, is refused unless the person passes `--unverified`, saying they have checked by other
  means; the record then says it was not verified, and why. A run that has finished is refused.
- **The refusals name it.** The five store refusals and two of `list`'s lines name `end` where they
  now name `Run.finish`.
- **`Run.finish` is not changed** (L8): it ends whatever run it is called on, as now.

The registry still does not decide that a run is dead (README §5 rule 9). `end` concludes nothing
by itself: it records a person's decision, after checking that the evidence here does not
contradict it.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`, `runregistrykit`
editable. **Install nothing** into `venv/`.

### 2.2 The state and the record (`runregistrykit/__init__.py`)

- **`TERMINAL_STATES`** becomes `("done", "failed", "killed", "lost")`. Nothing else spells the set:
  `liveness` (`:629`), `Run.finish` (`:813`) and the store rule (`stores.py:1023`) read it, so a
  `lost` run is `finished`, and is in use by no store, with no other change.
- **`Run.finish`'s code is not changed.** It checks `TERMINAL_STATES`, so it now accepts `lost`
  too; that is not refused (L8: `Run.finish` is not changed). Its docstring gains one sentence:
  `lost` is the state `end` records for a run whose end the registry never saw, and a caller
  reporting how its own run ended uses one of the other three.
- **What `end` writes**, through the status writer (`Run._update`), so that every other field the
  status holds (`pid`, `host`, `units_done`, `stage`, a `fingerprint`, …) is kept, and a status
  that cannot be read is composed from `{}`, as 03 made the writer do. The writer stamps
  `heartbeat` with the time of the write, as every write does; the run's last heartbeat is kept in
  the evidence. The fields, exactly:

  ```
  "state": "lost",
  "exit_code": null,
  "ended": {
    "by": getpass.getuser(), or null if it raises,
    "at": now_iso(),
    "reason": the --reason text, stripped,
    "git_head": git_provenance(<client root>)["git_head"],
    "host": {"id": this_host()["id"], "boot": this_host()["boot"], "name": this_host()["name"]},
    "verified": true | false,
    "not_verified_because": null | "another host" | "status does not say",
    "evidence": {
      "state": the state the status said (any JSON value), or null,
      "status_readable": whether status.json parsed as a JSON object,
      "pid": the pid the status said, or null,
      "pid_answers": true | false | null,
      "host": "this" | "another" | "not recorded",
      "boot": "this" | "earlier" | "not recorded" | null,
      "heartbeat": the heartbeat the status said, or null,
      "heartbeat_age": seconds, a float, or null
    }
  }
  ```

  `evidence.host` is `another` exactly when `liveness`' step 2 would call a `running` record
  foreign (its `host.id` not null and not this host's), `not recorded` when the status has no
  `host` object or its `id` is null, and `this` otherwise. `evidence.boot` is `null` unless
  `evidence.host` is `this`; then `earlier` when both boots are not null and differ, `this` when
  both are not null and equal, and `not recorded` otherwise. `pid_answers` is `pid_alive(pid)` when
  the pid was tested (§2.3), and `null` when it was not. `heartbeat_age` is `heartbeat_age(status)`.

  No other key of `status.json` is added, removed or renamed, and the manifest, `checkpoint.jsonl`
  and every sidecar are written exactly as before (README §5 rule 7; §0.1 plans these two).

### 2.3 The check (`runregistrykit/__init__.py`)

**One private function** does the check and the write; the command calls it, and the tests call
both. The planner's choice: `end` is a command a person runs (L8), so it is not a public name and
`__all__` does not change; 06 may make it one. The agent names it (for example `_end_run(path,
reason, *, unverified=False, client_root=None) -> dict`, returning the payload written). It raises
`RuntimeError` for a refusal, with a message that begins `Cannot end <run id>:`, says why, and ends
`Nothing was written`. **Every check is made before anything is written.** In this order:

1. **The run.** The path is a directory holding a `manifest.json` or a `status.json`. Otherwise it
   is refused: nothing the registry wrote is there (a directory that predates the registry, which
   blocks no store). A manifest that is missing, torn or not an object does not refuse: the status
   is what is judged, and `evidence` does not record the manifest.
2. **The reason.** Not empty once stripped.
3. **The state.** A terminal state, `lost` included, is refused: the run has already ended, and
   says how. The refusal names the state.
4. **A status that does not say** (03's sense: not readable, or a state that is neither `running`
   nor terminal): refused unless `--unverified`, then `verified: false`, `not_verified_because:
   "status does not say"`. *But* if the status is readable and gives a pid, and `evidence.host` is
   `this` or `not recorded` and `evidence.boot` is not `earlier`, the pid is tested, and a live pid
   is refused as in step 6, `--unverified` or not. (The planner's reading of L8 (a): a live pid
   here is refused with no override, whatever the state beside it.)
5. **`running` on another host** (`evidence.host` `another`): refused unless `--unverified`, then
   `verified: false`, `not_verified_because: "another host"`. Its pid is not tested
   (`pid_answers` `null`), as `liveness` does not test it. The refusal names the host, as the store
   refusals do (`entry["host"] or entry["host_id"]`'s rule), and says that `end` is run on that
   host, or here with `--unverified` once a person has checked there.
6. **`running` here.** `evidence.boot` `earlier`: accepted, `verified: true`, the pid not tested (a
   pid of an earlier boot names no process of this one, L3). Otherwise the pid is tested:
   **answers** → refused, with no override; `--unverified` does not change it, and the refusal says
   so. The refusal says that a process with that pid exists on this host, and that a process that
   was killed and not yet reaped by its parent (a zombie) answers `kill -0` until its parent waits
   for it or exits (§"At writing"). **Does not answer** → accepted, `verified: true`.

`--unverified` where every check passes without it is accepted and changes nothing: the record says
`verified: true`. A `running` status with no `host` (every record written before 01, or on a
platform with no identity) is judged by its pid, as `liveness` judges it (L4).

`end` takes no lock and is not a lock: a run whose process is alive is refused, and a run that is
not judged here is ended on a person's word.

### 2.4 The command, and the words that name it

- **`end`** in `runregistrykit/__main__.py`: a subparser beside `list` and `store`. `RUN` is a run
  id: a directory name under the runs root, not a path (refused if it contains a separator or is
  `.` or `..`, or if no such directory exists, `Nothing was written`). `--reason TEXT`, required.
  `--unverified`, a flag. `--root DIR`, the runs root, defaulting to the client config's
  `runs_root`, as `list`'s does. The client root is always located (its `git_head` is recorded),
  as the store commands locate it (`:536-547`); not finding one prints `!! …` and exits 1. A
  refusal prints `!! <message>` on stderr and exits 1; success prints one line on stdout naming the
  run, `lost`, and whether it was verified and by what (the agent's words; a test asserts them),
  and exits 0. The module docstring gains one sentence on `end`, and its four statements of the
  store rule are unchanged.
- **One place for the command's words.** A private constant in `runregistrykit/__init__.py` (for
  example `_END = "python -m runregistrykit end RUN_ID --reason TEXT"`), imported by `stores.py` and
  `__main__.py`, so that 05 reuses it.
- **The refusals.** Each text keeps its present form, with `Run.finish` replaced by the command:
  - copy and move (`stores.py:1085-1090`), retire (`:1719-1725`), amend (`:2074-2078`): "A stale run
    is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before …";
  - fingerprint (`:1393-1398`): "… a stale run is ended by a person, with `python -m runregistrykit
    end RUN_ID --reason TEXT`, first.";
  - `_unsure_remedy` (`:1063-1071`): "A run whose status does not say whether it is running is
    ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT --unverified`, once
    they have checked that it is not";
  - **one sentence added**, once per refusal, when any entry is `foreign`, beside 03's: "A run on
    another host is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT` on
    that host, or here with `--unverified` once they have checked there". No sentence is added
    when no entry is foreign;
  - `_refuse_if_in_use`'s docstring (`:1076-1078`) names the command.

  The backticks around the command are part of the words. For a refusal naming only alive and
  stale `running` runs on this host, the text is the present one with that one substitution and no
  other change.
- **`list`.** The stale line (`:587-593`) gains one sentence at its end: a run that is over is
  ended with the command. The line 03 added (`:595-603`) names `… end RUN_ID --reason TEXT
  --unverified` where it names `Run.finish`. The foreign line, the rows and the summary are
  unchanged; a `lost` run is `finished` and has no marker.
- **The existing assertions that pin `Run.finish` in these words.** Each changes its fragment to the
  new words, and nothing else in its test changes. Measured at writing (`grep -n 'Run.finish'
  runregistrykit/tests/*.py`, the docstrings left out):

  | Test file | Line | Fragment now | Fragment after |
  |---|---|---|---|
  | `test_store_retire.py` | 434 | `"Run.finish"` | `"runregistrykit end RUN_ID"` |
  | `test_store_retire.py` | 446 | `"A stale run is ended by a person, with Run.finish"` | ``"A stale run is ended by a person, with `python -m runregistrykit end"`` |
  | `test_store_retire.py` | 776 | the same | the same |
  | `test_store_amend.py` | 329 | `"Run.finish"` | `"runregistrykit end RUN_ID"` |
  | `test_store_amend.py` | 334 | `"Run.finish"` | `"runregistrykit end RUN_ID"` |
  | `test_store_copy_move.py` | 229 | `"Run.finish"` | `"runregistrykit end RUN_ID"` |
  | `test_unreadable_status_stores.py` | 169 | `"tale run is ended by a person, with Run.finish, "` | ``"tale run is ended by a person, with `python -m runregistrykit end RUN_ID"`` |
  | `test_unreadable_status.py` | 84 | `REMEDY`, 03's sentence | the new `_unsure_remedy` sentence's last clause, from `is ended by a person` |
  | `test_unreadable_status.py` | 231 | `"end it with Run.finish"` | the new words of that line's ending |

  This is the one change to an existing test's assertions this prompt makes. Any other existing
  assertion that fails is a stop.

### 2.5 What does not change

- Every existing test, in what it asserts, except §2.4's nine fragments. `git diff ab0cad9 --
  runregistrykit/tests` adds two files and changes those nine lines (and black's re-wrapping of
  them, if any) and nothing else.
- `Run.finish`'s code; the writer (`_write_status`, `_land_status`, `write_json_atomic`); `begin`
  (05 changes it); `liveness`' code and its values (`lost` is `finished` through
  `TERMINAL_STATES`); `list_runs`; the store rule; `store show`.
- The manifest, `checkpoint.jsonl` and every sidecar; every key of `status.json` but `state`'s new
  value, `exit_code`, which already exists, and `ended`.
- `__all__`.

### 2.6 The new tests

Two new modules: a core one, added to the workflow's core job (`tests.yml:89`), and a store one.

**`runregistrykit/tests/test_end.py`** (core; no store layer imported):
- **a hard-killed child**: a child process (started by the test, the only process it signals)
  begins a run in the test's runs root and client root, heartbeats, prints its run's path, and
  waits; the test sends it `SIGKILL` and **reaps it** (`wait()`, return code −9). `end` then
  writes `lost`, `exit_code` null, `ended.verified` true, `evidence.pid_answers` false,
  `evidence.host` `this` (where the platform has an identity; skip that assertion with a reason
  where `this_host()["id"]` is None), `evidence.boot` `this`, `evidence.heartbeat` the child's
  last heartbeat; and `list_runs` then gives `finished`;
- **every refusal**, and that each leaves `status.json` and the manifest byte for byte as they were:
  a live pid (a run begun in the test's own process), with and without `--unverified`; a run
  already `done`, `failed`, `killed` and `lost`; `running` on another host without `--unverified`;
  each of 03's thirteen forms without `--unverified` (`test_unreadable_status.FORMS`); a readable
  status of no state with this process's pid, with `--unverified`; an empty reason; a directory
  holding neither file;
- **every acceptance**, and exactly what is written (§2.2's keys, and the status's other fields
  kept): a dead pid (`a_dead_pid`); a live pid from an earlier boot (the status's `host.boot`
  changed to another value, `host.id` this host's), not tested; another host with `--unverified`
  (`verified` false, `not_verified_because` `"another host"`, `pid_answers` null); each of the
  thirteen forms with `--unverified` (`"status does not say"`); `--unverified` where it was not
  needed (`verified` true);
- **what is not written**: the manifest byte for byte, `checkpoint.jsonl` byte for byte, and no
  file left in the run directory but those that were there (no temporary file);
- **an old record** (README §5 rule 8): a `v0.1.0`-form status (`test_host.a_status(…,
  with_host=False)`), `running`, built in the test: with a dead pid, ended, `evidence.host` `not
  recorded`, `boot` null, verified; with a live pid, refused;
- **`TERMINAL_STATES`** holds `lost`, and `liveness` of a `lost` status is `finished`, on this host
  and from another;
- **the command**: `python -m runregistrykit end` in a subprocess with `PYTHONPATH` on the checkout
  (as 03's `list` tests do), `cwd` the client root: success, its line and exit 0; a refusal, `!! `
  on stderr and exit 1; `RUN` as a path, refused; no such run, refused; `--root`; and `list`
  afterwards, the `lost` row unmarked and the stale line's new sentence present for another, stale
  run.

**`runregistrykit/tests/test_end_stores.py`** (store layer; on `test_store_retire.RetireTestCase`):
- **the acceptance test**: a child begins a run on a full registered store and heartbeats; it is
  sent `SIGKILL` and reaped. Before `end`: copy, move, fingerprint, fingerprint `--write`, retire
  `--dry-run` and amend each refuse, naming the run and `runregistrykit end RUN_ID`, the
  temporary directory's tree unchanged by each. After `end`: fingerprint and fingerprint `--write`,
  retire `--dry-run`, amend, copy, and move (last, to a destination of its own) each succeed; and
  a resumed run on the store, begun after the kill, whose `finish("done", exit_code=0,
  fingerprint=True)` is called after `end`, records a `fingerprint` and no `fingerprint_error`;
- **the words**: a refusal for a foreign run carries the new foreign sentence once, and one for an
  unreadable run 03's sentence with `--unverified`; a refusal for alive and stale runs on this host
  only carries neither, and its text is the old text with the one substitution.

Both modules build everything in `tempfile` directories through the existing fixtures. The only
signal sent is `SIGKILL`, to a child the test started.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root, `TMPDIR`
   in your scratch: **`Ran 347 + N tests … OK (skipped=1)`** (or more skips only where §2.6 allows
   one for a platform with no host identity, which macOS is not). Give the per-module counts and
   the time.
2. **The core alone**, in a fresh scratch venv without `[stores]`, as 03's §3.2, with `test_end`
   added to the five core modules: 98 + N₁ tests pass, with `datastorekit`, `ray` and `sqlalchemy`
   absent. Remove the venv afterwards. `test_end` at `/opt/local/bin/python3.13` (3.13.16) with
   `PYTHONPATH` on the checkout.
3. **The planner's probe, re-run** from §"At writing" in your scratch, against `ab0cad9` (by `git
   archive`): its table. Against the change: the same child, killed and reaped, then `end`; every
   operation succeeding and the resumed run's fingerprint recorded; `end` refused on the zombie
   before the reap. Give both. Not committed.
4. **What is written.** A scratch lifecycle (`begin` on a registered store with a ledger,
   `heartbeat`, `record`, `finish("done", fingerprint=True)`) at `ab0cad9` and at the change: the
   shape of `status.json`, the manifest, a ledger line and the sidecar identical, archive against
   archive. And a status written by `end`: its keys, and `ended`'s and `evidence`'s, exactly §2.2's.
5. **The tests catch behaviour** (README §5 rule 10). Each mutation applied in a scratch clone, the
   named tests run, and reverted:
   - (m1) `end` not testing the pid of a `running` run here (accepting it whatever `kill -0` says);
   - (m2) `end` accepting a run on another host without `--unverified`;
   - (m3) `end` accepting a run already terminal;
   - (m4) `lost` left out of `TERMINAL_STATES` (`end` still writing it): the store module's
     after-`end` operations must fail;
   - (m5) `verified` written `true` whatever was checked;
   - (m6) `--unverified` overriding a live pid here;
   - (m7) the agent's own: one more change to the check, the record or the words, that a test
     catches.

   Each must fail at least one test, named in the log. A mutation no test catches is a stop.
6. **Nothing outside temporary directories**: `git status --short --ignored` the same before and
   after the suite, and no child left (`pgrep -f` is not used to judge a process: a test reaps what
   it starts). `git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'` finds only
   `finish`'s docstring.
7. `./venv/bin/black --check runregistrykit docs` is clean, at **35** files (two new modules).
8. **CI.** Pushing is the user's. The new core module first runs in the core job and on Linux;
   record that the review is to read its result there.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` changes `__init__.py`, `stores.py`, `__main__.py`, the
   nine assertions of §2.4 in four test modules, and adds the two new test modules;
   `.github/workflows/tests.yml` changes on its core line only.
2. §3.1–§3.7 hold. Every test that existed at `ab0cad9` passes, unchanged in what it asserts but for
   §2.4's nine fragments.
3. **The acceptance test passes**: a child begun on a store and sent `SIGKILL`, then `end`, then
   every store operation and a resumed run's fingerprint succeeding; `end` refused for a live pid,
   for a run on another host without `--unverified`, and for a run already terminal.
4. **The records**, in the same commit:
   - the log, `logs/04-end-a-run.md`, per README §5.1: the suite before (347) and after, the core
     run, both probe tables, the record as written, every mutation as a diff, and the refusal and
     `list` texts as shipped;
   - this board: the header, §1's row for 04, §1.1's E1, §3/§4 (the issue moved to §4 with what
     resolved it and the tests that pin it), and a "Package lines (04, this commit)" sentence on
     each §3 entry whose cited lines 04 moves;
   - `docs/OPEN_ISSUES.md`: the row deleted, the count (12 → 11), the date;
   - `prompts/INDEX.md`: the campaign's line;
   - this campaign's README §2: 04's status.

---

## 5. Stop conditions — stop and ask the user

- An existing test fails, or would need a change to what it asserts beyond §2.4's nine fragments;
  02b's or 02c's sweeps fail.
- A mutation of §3.5 is caught by no test.
- Any record would change form beyond §2.2: a key of `status.json` other than `ended`, or a state
  other than `lost`; the manifest, `checkpoint.jsonl` or a sidecar written differently;
  `write_json_atomic` or the writer changed.
- The design would have the package end, skip or override a run without a person's command, or
  accept a live pid on this host by any route (README §5 rule 9; L8).
- `Run.finish`'s code would change, or `__all__`.
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory; a test signals any process but a child it started, or leaves one unreaped.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything into `venv/`.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `runregistrykit/__init__.py`, `runregistrykit/stores.py`,
  `runregistrykit/__main__.py`; `runregistrykit/tests/test_end.py` and `test_end_stores.py`; the
  nine assertions of §2.4 in `test_store_retire.py`, `test_store_amend.py`,
  `test_store_copy_move.py`, `test_unreadable_status_stores.py` and `test_unreadable_status.py`;
  `.github/workflows/tests.yml`'s core line; the log, this board, the campaign README's §2 row,
  `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It does not change `begin` (05), `Run.finish`'s code, `liveness`' code, `pid_alive`, or `store
  show`.
- It does not tell a zombie from a live process
  (`[04-a-killed-process-not-yet-reaped-answers-kill-0]`): `end` refuses one and says why.
- It does not make a run whose manifest cannot be read name a store, nor read `Run.__init__`'s
  manifest differently (the two `[03-…]` manifest issues).
- It writes no README usage or release notes (06), and makes no tag.

---

## At writing (2026-10-18, at `9e38581`)

Measured for the README's row and the orchestrator, in the session scratchpad with `TMPDIR` there,
by a scratch probe (not committed) on `test_store_retire.RetireTestCase`: a full four-shard
registered store; a child process, started by the probe with `PYTHONPATH` on the checkout, that
called `begin` with the store as `results` and `heartbeat(units_done=1, stage="working")`, printed
its run's path and slept; then `SIGKILL` to that child, and only to it.

| What | Result |
|---|---|
| The killed child, **before `wait()`** | `pid_alive` **true**, `list_runs` liveness **`alive`**: a zombie answers `kill -0` |
| After `wait()` | return code −9; `pid_alive` false; `status.json` byte-identical to before the kill (keys `exit_code`, `heartbeat`, `host`, `pid`, `stage`, `state`, `units_done`, `units_total`); state `running`, liveness `stale` |
| The six store operations | each **refused**, naming the run and "A stale run is ended by a person, with Run.finish" (fingerprint: "a stale run is ended by a person, with Run.finish, first") |
| A resumed run's `finish("done", exit_code=0, fingerprint=True)` | `done`, **no `fingerprint`**, a `fingerprint_error` naming the stale run |
| `list` | the stale line on stderr, "Nothing here has killed or cleaned anything — go and look." |
| `python -m runregistrykit end …` | argparse error, exit 2: no such command |
| `Run(path).finish("killed", exit_code=137)` on a run begun in the probe's own process, **alive** | ends it, `killed`: today's remedy checks nothing |
| The same on the killed run, by hand | copy, fingerprint, fingerprint `--write`, retire `--dry-run` and amend then proceed |
| `getpass.getuser()` | returns a name here |

**The zombie.** A process that has been killed but not reaped by its parent answers `kill -0`
(measured here on macOS; Linux's `kill(2)` documents the same), and `liveness` calls its run
`alive`. A run's process is reaped by its parent
when the parent waits or exits; a launcher that started a detached child, passed its pid with
`heartbeat(pid=…)` and then neither waits nor exits leaves a killed child a zombie. `end` refuses
such a run, rightly by L8's rule, and its refusal says why; telling a zombie from a live process
would need `ps` on macOS, a subprocess per pid. Opened as
`[04-a-killed-process-not-yet-reaped-answers-kill-0]`, with no owner. The tests reap every child
they kill.

**The words.** `Run.finish` is named as a remedy in five texts in `stores.py` (`:1070`, `:1086`,
`:1395`, `:1720`, `:2075`) and a docstring (`:1078`), and in `list`'s line 03 added
(`__main__.py:601`). Nine assertions in five test modules pin those words (§2.4's table); the
other mentions of `Run.finish` in the tests are docstrings, and `stores.py:52` describes
`finish(fingerprint=True)`, not the remedy.

**Existing tests that see `lost`**: `test_host.py:517` iterates `TERMINAL_STATES` and asserts each
is `finished` from another host, which holds for `lost`. No other test enumerates the states.

The suite at `9e38581`: `Ran 347 tests`, `OK (skipped=1)`; `black --check runregistrykit docs`, 33
files.
