# Log — prompt 04: end a run

**Subject:** Add the end command, which records a run whose end was never seen
**Commit:** this commit (on `main`, after `5d8a97b`)
**Date:** 2026-10-18
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1–20). No stop condition fired.
**Result:** **landed.**
- **`python -m runregistrykit end RUN_ID --reason TEXT [--unverified] [--root DIR]`** records a
  run as ended: the new terminal state **`lost`**, `exit_code` null, and an **`ended`** record of
  who, when, why, at what `git_head`, on what host, whether it was verified and why not, and the
  evidence checked. It writes `status.json` through the status writer, so every other field the
  status holds is kept; the manifest, `checkpoint.jsonl` and every sidecar are not written, and
  nothing is deleted.
- **It checks first, and refuses**: a directory holding neither file; an empty reason; a run that
  has ended (`lost` included); a pid that answers `kill -0` on this host, **with no override**,
  whatever state stands beside it; a run on another host, or whose status does not say whether it
  is running, unless `--unverified`, which the record then states. A boot other than this one, or
  a pid that does not answer, is accepted, verified.
- **`TERMINAL_STATES`** is `("done", "failed", "killed", "lost")`, so a `lost` run is `finished`
  and is in use by no store, with no other change. **`Run.finish`'s code is not changed**; its
  docstring gains one sentence.
- **The words.** The five store refusals and `_unsure_remedy` name
  `` `python -m runregistrykit end RUN_ID --reason TEXT` `` (with `--unverified` where the status
  does not say) where they named `Run.finish`, composed from one private constant `_END`; one
  sentence is added once per refusal when any run is on another host; `list`'s stale line gains one
  sentence and 03's line names the command. A refusal naming only alive and stale runs on this host
  is the old text with that one substitution, byte for byte (§6).
- **The acceptance test**: a child begun on a full registered store is sent `SIGKILL` and reaped;
  the six operations refuse, each leaving the tree as it was; `end` (the command) records `lost`,
  verified; a resumed run's `finish(fingerprint=True)` then records a fingerprint and no error;
  and fingerprint, fingerprint `--write`, retire's dry run, amend, copy and move proceed.
- The suite is **347 → 378**: 31 new tests, 27 in the core module `test_end` and 4 in the store
  module `test_end_stores`. The core alone runs 125 (98 + 27), OK, one skip, with `datastorekit`,
  `ray` and `sqlalchemy` not findable. `test_end` passes at 3.13.16.
- Eight mutations, (m1)–(m6), the agent's (m7) and one more, (m8), each caught (§5).
- The issue `[a3-v2-a-hard-killed-run-blocks-its-store]` is **closed**. One is **opened**, found by
  the work: `[04-a-pid-out-of-range-makes-pid-alive-raise]` (deviation 17). The index counts
  **12 → 11 → 12**. `[04-a-killed-process-not-yet-reaped-answers-kill-0]` stays open.
- **Nothing pushed, no tag made, no workflow dispatched.**

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | `import getpass` (`:65`). `TERMINAL_STATES` (`:105`) with `lost`. The private constant `_END` (`:109`), with a two-line comment. One sentence in `Run.finish`'s docstring (`:804-805`). A new section at the end of the module (`:1211` on): `_not_ended` (`:1215`), the refusal's form, and `_end_run` (`:1219`), the check and the write, steps 1–6 at `:1262`, `:1273`, `:1285`, `:1321`, `:1341`, `:1355`; the live-pid refusal `:1309`; `ended.by` `:1361`; the write `:1383-1385`. `__all__` is unchanged |
| `runregistrykit/stores.py` | `_END` imported (`:153`). `_unsure_remedy`'s sentence (`:1069-1072`) names `` `{_END} --unverified` ``. `_foreign_remedy` (`:1075`), new, beside it, with the same contract. `_refuse_if_in_use`'s docstring (`:1090-1091`) names the command. The remedy in copy and move (`:1096-1105`), fingerprint (`:1406-1415`), retire (`:1735-1744`) and amend (`:2092-2099`): `Run.finish` → `` `{_END}` ``, and the foreign sentence inserted before 03's |
| `runregistrykit/__main__.py` | The module docstring: one sentence on `end` (`:38-41`). `import os`; `_END` and `_end_run` imported. `_end` (`:432`), the handler. The `end` subparser (`:499-517`). The client root is located for `end` as for `store` (`:611-625`). `list`'s stale line (`:665-672`) gains one sentence; 03's line (`:673-681`) names the command with `--unverified` |
| `runregistrykit/tests/test_end.py` | New, core, 27 tests |
| `runregistrykit/tests/test_end_stores.py` | New, store layer, 4 tests, on `test_store_retire.RetireTestCase` |
| `runregistrykit/tests/test_store_retire.py`, `test_store_amend.py`, `test_store_copy_move.py`, `test_unreadable_status_stores.py`, `test_unreadable_status.py` | The nine assertion fragments of the prompt's §2.4, and nothing else (§2) |
| `.github/workflows/tests.yml` | The core job's line (`:89`): `runregistrykit.tests.test_end` added |
| this log, `IMPLEMENTATION_STATE.md`, the campaign README's §2 row for 04, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: `pyproject.toml`, `client.py`, `fingerprint.py`, the repository `README.md`,
`PROVENANCE.md`, `CLAUDE.md`, `docs/` but `docs/OPEN_ISSUES.md`, every fixture
(`store_fixtures.py`, `test_host.a_status`, `test_unreadable_status.FORMS`, imported only), the
prompt, any other part of the campaign README, `orchestrator/`. Not changed in code: `Run.finish`,
`liveness`, `pid_alive`, the writer (`_write_status`, `_land_status`, `write_json_atomic`), `begin`,
`list_runs`, the store rule (`_running_runs_naming`), `store show`.

### The record `end` writes

One example, from the probe of §3 (the killed child, reaped, then `end` on the command line); the
host's boot and name are elided here, as 01's review asked:

```json
{
  "ended": {
    "at": "2026-10-18T11:47:54+01:00",
    "by": "ds283",
    "evidence": {
      "boot": "this",
      "heartbeat": "2026-10-18T11:47:54+01:00",
      "heartbeat_age": 0.758109,
      "host": "this",
      "pid": 47625,
      "pid_answers": false,
      "state": "running",
      "status_readable": true
    },
    "git_head": "<the scratch client root's HEAD>",
    "host": {"boot": "<the boot, 36 characters>", "id": "<16-hex digest>", "name": "<platform.node()>"},
    "not_verified_because": null,
    "reason": "killed outright, probe",
    "verified": true
  },
  "exit_code": null,
  "heartbeat": "2026-10-18T11:47:54+01:00",
  "host": {"boot": "<the boot>", "id": "<16-hex digest>"},
  "pid": 47625,
  "stage": "working",
  "state": "lost",
  "units_done": 1,
  "units_total": null
}
```

`ended` has exactly the prompt's eight keys and `evidence` its eight; the status's other keys
(`host`, `pid`, `stage`, `units_done`, `units_total`) are the child's, kept. `heartbeat` is the
writer's stamp of the `end` write; the child's last heartbeat is `evidence.heartbeat`.
`TestAcceptances` and `TestAnOldRecord` assert the key sets exactly, every value, and that every
other field of the status is kept (`EndTestCase.assertEnded`).

### The words, as shipped

`_END` is `python -m runregistrykit end RUN_ID --reason TEXT`. In what follows `` `END` `` is that
text in backticks.

- copy, move: `… {described}. A stale run is ended by a person, with `END`, before its store is
  moved; the registry does not decide that a run is dead. [FOREIGN. ][UNSURE. ]Nothing was written`
- fingerprint: `… describes no instant; a stale run is ended by a person, with `END`, first.
  [FOREIGN. ][UNSURE. ]Nothing was read or written`
- retire: `… A stale run is ended by a person, with `END`, before its store is retired; the
  registry does not decide that a run is dead. [FOREIGN. ][UNSURE. ]Once it is ended, …`
- amend: `… A stale run is ended by a person, with `END`, before its sidecar is amended; the
  registry does not decide that a run is dead[. FOREIGN][. UNSURE]. Nothing was written`
- FOREIGN (`_foreign_remedy`, when any entry's liveness is `foreign`): `A run on another host is
  ended by a person, with `END` on that host, or here with `--unverified` once they have checked
  there`
- UNSURE (`_unsure_remedy`, 03's, when any entry is not `running`): `A run whose status does not say
  whether it is running is ended by a person, with `END --unverified`, once they have checked that
  it is not`
- `list`'s stale line: `… Nothing here has killed or cleaned anything — go and look. Once you know
  one is over, end it with `END`.`
- `list`'s 03 line: `… Go and look; once you know one is not running, end it with `END
  --unverified`.`

`end`'s own texts, each `Cannot end <run id>: <why>. Nothing was written`:

- not a directory: `<path> is not a directory`
- neither file: `<path> holds neither a manifest.json nor a status.json, so nothing the registry
  wrote is there; a directory that predates the registry names no store and blocks none`
- no reason: `a reason is required, saying why the run is ended, which only a person can say`
- ended: `its status says it has already ended, as '<state>'; end records only a run whose end the
  registry never saw`
- a live pid: `its pid <pid> answers kill -0, so a process with that pid exists on this host, and
  a run whose process may be alive is not ended; --unverified does not override this. A process
  that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its
  parent waits for it or exits`
- does not say: `its status cannot be read (status.json is missing, is not JSON, or is not a JSON
  object), so whether it is running cannot be told here. Once a person has checked that it is not,
  `END --unverified` ends it, recorded as not verified`; or `its status says neither running nor
  finished (state <repr, or none>), so …`, the same
- another host: `it is running on another host, <manifest's host.name, else the status's host.id>
  (pid <pid>, not tested here), and a pid means nothing off its own host. It is ended with `END` on
  that host, or here with `--unverified` once a person has checked there`

The command adds `!! Cannot end '<RUN_ID>': RUN_ID is a run id, the name of a directory under the
runs root, not a path. Nothing was written`, `!! Cannot end <RUN_ID>: there is no run directory
<path>. Nothing was written`, and prints a refusal as `!! <message>`, exit 1. Success is one line
on stdout, exit 0: `>> end: <RUN_ID> is now lost, ` and then `verified: its pid <pid> does not
answer kill -0 on this host`, `verified: its status was written on this host in an earlier boot`,
or `not verified (<another host | status does not say>): on a person's word, with --unverified`.

## Deviations from the prompt

Each is classified. Corrections 1–20 are section 0's.

1. **L7 and L8 are (a)** (correction 1), as the prompt states them. **STRUCTURALLY REQUIRED.**
2. **The suite's time** (correction 2): each run in the foreground, its output in a file, the
   verdict grepped from it: 136.251 s on the tree as committed (§2). **STRUCTURALLY REQUIRED.**
3. **The core run** (correction 3): `uv venv -p /opt/local/bin/python3.12 agent-04/core`, `uv pip
   install --offline -p agent-04/core/bin/python -e` this checkout, the six modules by name,
   removed afterwards; `test_end` at `/opt/local/bin/python3.13` with `PYTHONPATH` on the checkout.
   **STRUCTURALLY REQUIRED.**
4. **The thirteen forms with `--unverified`** (correction 4): each acceptance gives the run a dead
   pid first (`a_dead_run`, then `give_status_the_form`); for "null state", "paused" and "state 5"
   `pid_answers` is false (tested), for the other ten null. The refusal of a readable status of no
   state with this process's pid is made for each of the three, with and without `--unverified`,
   its message the live-pid refusal's. The refusal of each form **without** `--unverified` is made
   on a dead pid too, so that each gives the "does not say" words; with a live pid the three
   readable forms give the live-pid words instead, which the previous test pins. **STRUCTURALLY
   REQUIRED.**
5. **"Gives a pid"** (correction 5): readable and `pid` not null; `pid_answers` is `pid_alive`'s.
   In step 6 a `running` status here whose `pid` is null is tested, does not answer, and is
   accepted (`test_a_running_status_with_no_pid_is_tested_and_accepted`); the docstring says so.
   **STRUCTURALLY REQUIRED.**
6. **The host a refusal names** (correction 6): the manifest's `host.name` through `_json_object`,
   else the status's `host.id`; both pinned (`test_a_run_on_another_host_is_refused_without_unverified`,
   `named` true and false). **STRUCTURALLY REQUIRED.**
7. **The client root is located first** (correction 7), before every check, as `begin` locates
   it: `find_client_root` is `_end_run`'s first call, so no client root means `ConfigError` and
   nothing read or written. The command locates it in `main`, as for `store`, and prints `!! …`,
   exit 1 (`test_no_client_root_is_refused`, by `--client-root` on a directory with no config).
   **IMPLEMENTATION CHOICE.**
8. **`ended.git_head`** is `git_provenance(client.found)["git_head"]`: the directory whose
   `runregistrykit.toml` governs, which in a linked worktree is the worktree, not its main
   checkout's record root. The prompt says "of the client root". **IMPLEMENTATION CHOICE.**
9. **`ended.by`** (correction 8): `getpass.getuser()`, `None` on any `Exception`. Not mocked in a
   test; the tests assert it equals `getpass.getuser()`. **STRUCTURALLY REQUIRED.**
10. **The write** (correction 9): `Run(path, client_root=client)._update(state="lost",
    exit_code=None, ended=…)`. Nothing on the path reads `Run.manifest`. The check-to-write window
    is recorded below, not closed. **STRUCTURALLY REQUIRED.**
11. **The words** (correction 10): `_END` beside `TERMINAL_STATES`, imported by `stores.py` and
    `__main__.py`; every text that names the command is composed from it, the one exception being
    `_refuse_if_in_use`'s docstring, which names `python -m runregistrykit end` in prose. The
    foreign sentence is a helper, `_foreign_remedy`, beside `_unsure_remedy`, inserted after the
    stale sentence and before 03's, once per refusal. No new text uses the word the §3.6 grep looks
    for. **STRUCTURALLY REQUIRED.**
12. **`--unverified` in backticks in the foreign sentence**, as the prompt writes it; `end`'s own
    another-host refusal does the same; the live-pid refusal and the success line write it bare.
    **IMPLEMENTATION CHOICE.**
13. **No test builds a zombie** (correction 11); the live-pid refusal's words, the zombie sentence
    among them, are pinned on a run begun in the test's process; the probe shows `end` refused on
    the killed child before its reap (§3). **STRUCTURALLY REQUIRED.**
14. **The acceptance test's order** (correction 12): the child, `SIGKILL` by `Popen.kill`, the
    reap (−9); the six refusals; `end`, **by the command** (`CommandLineTestCase.command`), not the
    function; the resumed run begun and finished; then the six operations, move last to a
    destination of its own. The child is started with `sys.executable`, the checkout first on its
    `sys.path`, and `addCleanup` kills and reaps it whatever fails. The helper that starts it,
    `test_end.a_hard_killed_run`, is shared by both modules. **IMPLEMENTATION CHOICE** (the command
    rather than the function).
15. **The nine assertions** (correction 14): exactly the table's. Black re-wrapped the two in
    `test_store_amend.py`, the one at `test_unreadable_status.py:231` (now `:234-237`) and the one
    in `test_unreadable_status_stores.py`; `REMEDY` (`test_unreadable_status.py:84-87`) is written
    by hand as two string literals in parentheses, since black leaves a long string on one line. Its value is the new sentence from `is ended by a person` to its
    end. **STRUCTURALLY REQUIRED.**
16. **`TestFinishIsNotChanged`** pins that `Run.finish("lost")` is accepted and writes no `ended`
    (L8: `Run.finish` not changed, and now accepting `lost` through `TERMINAL_STATES`).
    **IMPLEMENTATION CHOICE.**
17. **One issue opened** (correction 16): `[04-a-pid-out-of-range-makes-pid-alive-raise]`,
    measured (§3, "a pid out of range"). The board's §3 count goes 7 → 7 (6 once this prompt's
    issue is closed, then 7), and the index's 12 → 12 (11, then 12), where the brief expected 6 and
    11. **IMPLEMENTATION CHOICE** (the brief says to open one when measured).
18. **Mutations** (correction 17): (m1)–(m6) as the prompt names them, (m7) the agent's, and (m8)
    one more of the agent's, on the command's argument. **IMPLEMENTATION CHOICE.**
19. **`list`'s stale line** names the command without `--unverified` (a stale `running` run here is
    ended without it), and 03's line with it. **STRUCTURALLY REQUIRED** (§2.4).

## Verification performed

### 1. The state at the start

- `HEAD` `5d8a97b`, `main`, clean, the only worktree; `git diff --stat ab0cad9 HEAD --
  runregistrykit pyproject.toml .github` empty. `RAY_ADDRESS` unset; `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` found nothing before and after every suite run.
- `venv/`: Python 3.12.15, black 25.1.0. `var/ledger.jsonl` `471d0859…` before and after.
- `git status --short --ignored` before: `prompts/.DS_Store`, `runregistrykit.egg-info/`, both
  `__pycache__/`, `var/`, `venv/`; the same ignored entries after the suite.

### 2. The suite, before and after

`TMPDIR=<agent-04>/tmp ./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from
the root, in the foreground. Per module, by `unittest.defaultTestLoader.discover`:

| Module | Before | After |
|---|---:|---:|
| `test_client_root` | 27 | 27 |
| `test_end` | — | **27** |
| `test_end_stores` | — | **4** |
| `test_fingerprinter` | 31 | 31 |
| `test_host` | 28 | 28 |
| `test_host_stores` | 3 | 3 |
| `test_package_imports` | 3 | 3 |
| `test_package_is_generic` | 22 | 22 |
| `test_public_names` | 8 | 8 |
| `test_run_registry` | 29 | 29 |
| `test_status_writes` | 22 | 22 |
| `test_store_amend` | 21 | 21 |
| `test_store_amend_residuals` | 9 | 9 |
| `test_store_command_line` | 2 | 2 |
| `test_store_copy_move` | 27 | 27 |
| `test_store_fingerprint` | 29 | 29 |
| `test_store_retire` | 41 | 41 |
| `test_store_retire_references` | 10 | 10 |
| `test_store_sidecar` | 17 | 17 |
| `test_unreadable_status` | 11 | 11 |
| `test_unreadable_status_stores` | 7 | 7 |
| **total** | **347**, `Ran 347 tests in 122.681s` (the orchestrator's gate run), `OK (skipped=1)` | **378**, `Ran 378 tests in 136.251s`, `OK (skipped=1)` |

N = 31 (N₁ = 27 core, 4 store). The skip is `test_host`'s readers on Linux, as before; no new
skip ran here, since macOS gives an id and a boot. 02b's and 02c's sweeps (`test_status_writes`)
pass unchanged. `git diff ab0cad9 -- runregistrykit/tests` adds `test_end.py` and
`test_end_stores.py` and changes the nine fragments, and nothing else.

### 3. The probes, against `ab0cad9` and this tree

The planner's `probe.py`, run by `venv/`'s Python with `agent-04/old` (`git archive ab0cad9`) as
its argument; and the agent's copy, `probe-end.py`, extended as the brief asks, with this checkout.
Both print `runregistrykit.__file__` and import the tree given. Not committed.

| What | `ab0cad9` (`probe.py`) | this tree (`probe-end.py`) |
|---|---|---|
| the killed child before `wait()` | `pid_alive` true, liveness `alive` | the same |
| `end` on it before `wait()`, plain and with `--unverified` | no such command: argparse, exit 2 | **refused**, exit 1, both: "its pid … answers kill -0, so a process with that pid exists on this host … --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, …"; `status.json` byte-identical |
| after `wait()` | −9; `pid_alive` false; `status.json` byte-identical (keys `exit_code`, `heartbeat`, `host`, `pid`, `stage`, `state`, `units_done`, `units_total`); `running`, `stale` | the same |
| the six operations | each refused, "A stale run is ended by a person, with Run.finish" (fingerprint: "…, with Run.finish, first") | each refused, "…, with `` `python -m runregistrykit end RUN_ID --reason TEXT` ``, …" |
| `list`'s stderr | the stale line, ending "go and look." | the same, then "Once you know one is over, end it with `` `python -m runregistrykit end RUN_ID --reason TEXT` ``." |
| `end` after the reap | — | exit 0, `>> end: <id> is now lost, verified: its pid <pid> does not answer kill -0 on this host`; `lost`, `finished` |
| `end` again | — | refused: "its status says it has already ended, as 'lost'" |
| a resumed run's `finish("done", exit_code=0, fingerprint=True)` | `done`, no `fingerprint`, a `fingerprint_error` naming the stale run | `done`, **`fingerprint` recorded**, no `fingerprint_error` |
| the operations after | (after `Run.finish` by hand) copy, fingerprint, `--write`, retire `--dry-run`, amend proceeded | fingerprint, `--write`, retire `--dry-run`, amend, copy and move **proceeded**; `list` prints nothing on stderr |
| `Run(path).finish("killed")` on a live run | ends it | not run: `Run.finish` is unchanged |

"Before" is the prompt's table, reproduced: every row is as it states.

**A pid out of range** (`probes/bigpid.py`, scratch): a status whose `pid` is `2**31`, written by
hand. `pid_alive(2**31)` raises `OverflowError: signed integer is greater than maximum` (and at
`ab0cad9`); so `liveness` raises, `list_runs` raises, `list` exits 1 with a traceback, and `end`
exits 1 with a traceback, the status unchanged. `pid_alive(-1)`, `'x'`, `None` give false. Opened
as `[04-a-pid-out-of-range-makes-pid-alive-raise]` (deviation 17).

### 4. What is written

**The lifecycle** (`probes/lifecycle.py`, scratch): `begin` on a full registered store with a
ledger, `heartbeat`, `record`, `finish("done", exit_code=0, fingerprint=True)`, then the shape of
each record (keys, recursively, and value types): `status.json` (`exit_code`, `fingerprint`,
`fingerprint_sidecar`, `heartbeat`, `host`, `pid`, `stage`, `state`, `units_done`, `units_total`),
the manifest's twenty keys, a ledger line's six, the sidecar's eight, and the run directory's three
files. Run with `agent-04/old` (`ab0cad9`) and with `agent-04/new`, a copy of this tree's
`runregistrykit/` outside the checkout: **identical**. (Run from the checkout itself, one value's
type differs, `packages.runregistrykit.url`, str against null: `importlib.metadata` finds the
checkout's `runregistrykit.egg-info`, which has no `direct_url.json`, before the venv's
`dist-info`. It is where the tree is imported from, not the change.)

**The status `end` writes**: §"The record `end` writes" above; `ended`'s and `evidence`'s keys are
exactly the prompt's §2.2, asserted by `assertEnded` in every acceptance. `write_json_atomic`,
`_write_status` and `_land_status` are byte for byte as at `ab0cad9` (`git diff ab0cad9 --
runregistrykit/__init__.py` touches the import, `TERMINAL_STATES`, the constant, `finish`'s
docstring and the new section, and nothing else).

### 5. The deliberate-breakage record

Each mutation was applied in a scratch `git clone` of this repository (`agent-04/mut`), whose tree
was made equal to the files as they are committed (`cmp` on all eleven) and committed there (in the
clone only). For each: the diff below (from `git diff` after `black`) was checked with `git apply
--check`, applied, `./venv/bin/python -m unittest runregistrykit.tests.test_end
runregistrykit.tests.test_end_stores` run from the clone (31 tests; the clone's package, and its
children's through `PYTHONPATH` and `sys.path`), then `git apply -R --check` and `git apply -R`;
the clone's `git status --short` was empty after each, and this checkout's was never changed by
one.

**(m1)** `end` not testing the pid of a `running` run here. 4 failures:
`TestRefusals.test_a_live_pid_is_refused_with_or_without_unverified` (both),
`TestAnOldRecord.test_a_dead_pid_is_ended_and_a_live_one_refused`,
`TestTheCommand.test_a_refusal_prints_it_and_exits_1`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index e4439dd..9a4aa6b 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1353,7 +1353,7 @@ def _end_run(path, reason, *, unverified=False, client_root=None) -> dict:
         because = "another host"
     elif boot != "earlier":
         # 6. running here
-        answers = pid_alive(pid)
+        answers = False
         if answers:
             refuse_a_live_pid()
 
```

**(m2)** `end` accepting a run on another host without `--unverified`. 3 failures:
`TestRefusals.test_a_run_on_another_host_is_refused_without_unverified` (`named` true and false),
`TestTheCommand.test_unverified_says_so`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index e4439dd..bf2c0bc 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1339,7 +1339,7 @@ def _end_run(path, reason, *, unverified=False, client_root=None) -> dict:
         because = "status does not say"
     elif where == "another":
         # 5. running on another host
-        if not unverified:
+        if False:
             manifest = _json_object(read_json(manifest_path))
             described = manifest.get("host")
             name = described.get("name") if isinstance(described, dict) else None
```

**(m3)** `end` accepting a run already terminal. 4 failures:
`TestRefusals.test_a_run_that_has_ended_is_refused`, `done`, `failed`, `killed` (each then meets
the live-pid refusal, with other words) and `lost` (accepted with `--unverified`).

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index e4439dd..8c8cf10 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1283,7 +1283,7 @@ def _end_run(path, reason, *, unverified=False, client_root=None) -> dict:
     state = status.get("state")
 
     # 3. the state
-    if state in TERMINAL_STATES:
+    if False:
         raise _not_ended(
             identifier,
             f"its status says it has already ended, as {state!r}; end records only a run whose "
```

**(m4)** `lost` left out of `TERMINAL_STATES`, `end` still writing it. 18 failures and 1 error:
`test_end_stores.TestEndingAHardKilledRun.test_refused_until_it_is_ended_and_then_every_operation_proceeds`
(its first assertion after `end`: `('lost', 'unknown') != ('lost', 'finished')`);
`TestAHardKilledRun`, `TestAcceptances.test_a_dead_pid`, `test_each_form_with_unverified` (13
forms), `TestTheCommand.test_list_afterwards`, `TestTheState` (each a `lost` run not
`finished`), and `TestFinishIsNotChanged` (error: `finish("lost")` raises `ValueError`). **The
after-`end` operations**, measured by running `probe-end.py` against the clone with (m4) applied:
the resumed run's fingerprint refused (`fingerprint_error`: "run …'s status says neither running
nor finished (state 'lost')"), and fingerprint, fingerprint `--write`, retire `--dry-run`, amend,
copy and move **each refused**.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index e4439dd..c473c84 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -102,7 +102,7 @@ __all__ = [
     "write_json_atomic",
 ]
 
-TERMINAL_STATES = ("done", "failed", "killed", "lost")
+TERMINAL_STATES = ("done", "failed", "killed")
 
 # the command a person runs to record that a run whose end the registry never saw has ended, as
 # the store operations' refusals and `list` name it (`_end_run` checks and writes)
```

**(m5)** `verified` written `true` whatever was checked. 15 failures:
`TestAcceptances.test_another_host_with_unverified`, `test_each_form_with_unverified` (13 forms),
`TestTheCommand.test_unverified_says_so`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index e4439dd..829d6c0 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1367,7 +1367,7 @@ def _end_run(path, reason, *, unverified=False, client_root=None) -> dict:
         "reason": reason.strip(),
         "git_head": git_provenance(client.found)["git_head"],
         "host": {key: here[key] for key in ("id", "boot", "name")},
-        "verified": because is None,
+        "verified": True,
         "not_verified_because": because,
         "evidence": {
             "state": state,
```

**(m6)** `--unverified` overriding a live pid here, at both places a pid is tested. 6 failures:
`TestRefusals.test_a_live_pid_is_refused_with_or_without_unverified` (`unverified=True`),
`test_a_readable_status_of_no_state_with_a_live_pid_is_refused_with_unverified` (three forms,
`unverified=True`), `TestAnOldRecord.test_a_dead_pid_is_ended_and_a_live_one_refused`,
`TestTheCommand.test_a_refusal_prints_it_and_exits_1`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index e4439dd..f0caff7 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1321,7 +1321,7 @@ def _end_run(path, reason, *, unverified=False, client_root=None) -> dict:
         # 4. a status that does not say
         if readable and pid is not None and where != "another" and boot != "earlier":
             answers = pid_alive(pid)
-            if answers:
+            if answers and not unverified:
                 refuse_a_live_pid()
         if not unverified:
             said = (
@@ -1354,7 +1354,7 @@ def _end_run(path, reason, *, unverified=False, client_root=None) -> dict:
     elif boot != "earlier":
         # 6. running here
         answers = pid_alive(pid)
-        if answers:
+        if answers and not unverified:
             refuse_a_live_pid()
 
     try:
```

**(m7)** (the agent's own) the foreign sentence added to every refusal, not only when a run is on
another host. 12 failures: `test_end_stores.TestTheWords.test_a_run_whose_status_does_not_say_names_unverified`
and `test_alive_and_stale_here_give_the_old_text_with_the_command`, six operations each.

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 59ca6cf..7d69e49 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1076,7 +1076,7 @@ def _foreign_remedy(running) -> str:
     """The sentence a refusal adds, without its full stop, when any of ``running`` is a `running`
     run on another host: its pid is not tested here, and a person checks there. Empty otherwise.
     """
-    if not any(entry["liveness"] == "foreign" for entry in running):
+    if not running:
         return ""
     return (
         f"A run on another host is ended by a person, with `{_END}` on that host, or here "
```

**(m8)** (the agent's own) the command's `RUN_ID` check without the separators: a path given as
`RUN_ID` is joined to the runs root, and an absolute one replaces it, so `end /any/run/dir` would
end that directory. 4 failures: `TestTheCommand.test_a_run_id_that_is_a_path_is_refused`, for the
absolute path, `<id>/`, `../<id>` and `a/b`.

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index b7aecff..f7c68cf 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -432,9 +432,7 @@ def _store(args, client) -> int:
 def _end(args, client) -> int:
     """`end`: ``args.run`` is a run id, a directory name under the runs root, never a path."""
     name = args.run
-    if name in ("", ".", "..") or any(
-        sep and sep in name for sep in (os.sep, os.altsep)
-    ):
+    if name in ("", ".", ".."):
         print(
             f"!! Cannot end {name!r}: RUN_ID is a run id, the name of a directory under the runs "
             f"root, not a path. Nothing was written",
```

Each fails at least one test. None was left in this tree.

### 6. The words, and nothing else written

- **The one substitution.** `test_end_stores.TestTheWords.test_alive_and_stale_here_give_the_old_text_with_the_command`
  builds each of the six refusals for an alive and a stale run on this host from ab0cad9's
  templates, with `Run.finish` replaced by `` `{_END}` ``, and compares them with the messages,
  equal. The same test, with the replacement text set back to `Run.finish` and run against
  `agent-04/oldcheck` (`git archive ab0cad9`), passes: the templates are `ab0cad9`'s texts byte for
  byte.
- **The new sentences once.** `test_a_run_on_another_host_adds_the_sentence_once` (a foreign and
  a stale run: the foreign sentence once in each of the six, 03's absent);
  `test_a_run_whose_status_does_not_say_names_unverified` (a torn status: 03's sentence once, with
  `` `{_END} --unverified` ``, the foreign one absent).
- **`list`**: `TestTheCommand.test_list_afterwards` (the `lost` row unmarked, `1 finished, 1
  stale`, the stale line ending with the new sentence); `test_unreadable_status`' line 231, the
  03 line naming the command with `--unverified`.
- No key of `status.json` but `ended` is added, and `state` gains one value (§4).

### 7. Nothing outside temporary directories, nothing else signalled

`git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'` finds one line,
`runregistrykit/__init__.py:814`, in `finish`'s docstring. The two new modules build everything in
`tempfile` directories through the existing fixtures. The only process signalled is the child
`a_hard_killed_run` starts, by `Popen.kill`, which it then reaps (`wait()`, −9); a cleanup kills
and reaps it if it is still running. The probes signal only the child they start, and reap it.
`git status --short --ignored` lists the same ignored entries before and after the suite.

### 8. The core alone, and 3.13

The venv of correction 3. `importlib.util.find_spec` found none of `datastorekit`, `ray`,
`sqlalchemy` (`{'datastorekit': False, 'ray': False, 'sqlalchemy': False}`); Python 3.12.15. The six
core modules by name, `test_run_registry`, `test_public_names`, `test_host`, `test_status_writes`,
`test_unreadable_status`, `test_end`: `Ran 125 tests in 38.831s`, `OK (skipped=1)` (98 + 27). The
venv was removed afterwards. `test_end` at `/opt/local/bin/python3.13` (3.13.16) with `PYTHONPATH`
on the checkout: `Ran 27 tests in 11.568s`, `OK`.

### 9. `black`

`./venv/bin/black --check runregistrykit docs`: 33 files at `ab0cad9`, **35** now (the two new
modules), unchanged. Every changed file was formatted.

### 10. CI

Nothing is pushed. `test_end` first runs in the core job and on Linux, at 3.12.15, and at 3.13.16
in `suite (high)`; the review is to read the run's result there: the core job's count, which
should be 125, and the skip count, since on Linux `this_host()` gives an id and a boot too and the
two identity skips in `test_end` should not run.

## Observations not acted on

1. **The window between the check and the write** (correction 9). `_end_run` reads the status,
   judges it, and then writes through `Run._update`, which reads the file again and composes from
   it. A write between the two (a heartbeat from a process that was not dead after all, from
   another host's run directory on a shared filesystem) is composed into the `lost` payload, and
   the check judged the earlier one. `end` takes no lock and is not one (§2.3); not closed.
2. **A pid reused within one boot** by a live process makes a hard-killed run on this host
   un-endable until that process exits or the machine reboots: `end` refuses a pid that answers,
   with no override (L8 (a)), and L3 (b)'s start time is not taken. Read, not measured; no issue.
3. **A pid out of range** (`2**31` or more, or less than `-2**31`) makes `pid_alive` raise
   `OverflowError`, so `liveness`, `list_runs`, `list` and `end` raise on a status that holds
   one, measured (§3), and every store operation under the runs root with them, read (`runs_naming`
   calls `list_runs`), not run. No writer of the registry records
   such a pid; a hand edit would. `pid_alive` is not this prompt's. Opened as
   `[04-a-pid-out-of-range-makes-pid-alive-raise]`, owner none.
4. **`Run.__init__`'s manifest read** (`:680`, `read_json(…) or {}`) is still raw
   (`[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]`): `end` constructs a
   `Run` only to write, and nothing on that path reads `Run.manifest`, so a manifest `[1]` does not
   stop `end` (`TestWhatIsNotWritten.test_a_run_with_no_manifest_is_judged_by_its_status` covers a
   missing one).
5. **`stores.py` prose**: the comment at `:1727` ("any running run, alive or stale") and
   `fingerprint_store`'s and `amend_sidecar`'s docstrings (`:1366`, `:2025`) still say a `running`
   run, as 03's observation 2 recorded; and the module docstring at `:52` names `Run.finish(...,
   fingerprint=True)`, which is not a remedy. Not the prompt's words.
6. **The core run's editable install rewrote the ignored `runregistrykit.egg-info/`**, as before.
   Ignored and not staged.
7. **A run directory that predates the registry** (neither file) is refused by `end`, and blocks no
   store, as before.

## State handed to the next prompt

- **The interface after 04:**
  - `TERMINAL_STATES` (`__init__.py:105`) is `("done", "failed", "killed", "lost")`;
  - `runregistrykit._END` (`:109`), private, the command's words; `_end_run(path, reason, *,
    unverified=False, client_root=None) -> dict` (`:1219`), private, the check and the write;
  - `status.json` may hold `state` `lost` and an `ended` object (§"The record `end` writes");
  - `stores._foreign_remedy` (`:1075`) beside `_unsure_remedy` (`:1064`), each empty when it does
    not apply; the five refusals compose `` `{_END}` ``;
  - `python -m runregistrykit end` (`__main__._end`, `:432`).
- **For 05 (`begin`):** its refusal of a stale run names `` `{_END}` `` as the store refusals do,
  and can add `_foreign_remedy(running)` and `_unsure_remedy(running)` as they do. A `lost` run is
  terminal, so `_running_runs_naming` does not return it.
- **For 06:** the release notes say that `status.json` may now hold `lost` and `ended`, and that
  `TERMINAL_STATES` gained a value; the README's usage of `end`.
- **The issues:** `[a3-v2-a-hard-killed-run-blocks-its-store]` closed;
  `[04-a-killed-process-not-yet-reaped-answers-kill-0]` open, owner none, `end` refusing such a run
  with the zombie sentence; `[04-a-pid-out-of-range-makes-pid-alive-raise]` opened, owner none.
- **CI:** the push is the user's. The core job's line now names six modules.
- The suite is 378, with one skip on macOS.
