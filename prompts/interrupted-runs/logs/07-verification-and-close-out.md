# Log — prompt 07: verification and close-out

**Subject:** Verify the interrupted-runs campaign and close it
**Commit:** `c991b03` (on `main`, after `e4bf592`)
**Date:** 2026-10-18
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1–18). No stop condition fired.
**Result:** **landed.**
- **The document**, `docs/interrupted-runs-verification.md`, in the prompt's twelve sections: the
  campaign reconciled from 44 commits, ten CI runs and the tag; each prompt's acceptance re-measured
  at `v0.2.0`; the hard-kill route run from the GitHub pin; the release as installed; fourteen issues,
  L1–L11, 159 deviation entries and 46 observations, each counted from the records; the known gaps;
  the reproduction.
- **The script**, `docs/interrupted-runs/interrupted_run_smoke.py`: thirteen steps, a hard kill to a
  resumed and fingerprinted store. **Exit 0 at both ends against the pin installed from GitHub**,
  3.8 s and 6.3 s; Ray never started; no child left; every process it starts imports the pin.
  Breakage (a)–(c) fail as the prompt's §4.5 and section 0's corrections 8–9 say.
- **The release**: the pin installs from GitHub at both ends and in the core form, `commit_id`
  `0bae3a3`, its five modules `0bae3a3`'s byte for byte, no test in its `RECORD`.
- **The extraction's smoke run** against `v0.2.0`: 10 of 11 at both ends, step 3 on the summary
  clause 01 added, as the prompt's §1.2 says.
- **The suite**: `Ran 410 tests … OK (skipped=1)` in `venv/` before and after, and at the high end;
  `test_status_writes` at 3.14.8, 22, OK, no skip. `black --check runregistrykit docs`: 38 files.
- **The campaign is closed** on the board, in its README, in `prompts/INDEX.md` and in
  `docs/OPEN_ISSUES.md`. **Nothing is opened**; the index stays at 11.
- **Nothing under `runregistrykit/` changed. Nothing pushed, no tag made, no workflow dispatched.**

## What shipped

| File | What |
|---|---|
| `docs/interrupted-runs-verification.md` | new: the verification document, §1–§12 |
| `docs/interrupted-runs/interrupted_run_smoke.py` | new: the smoke script, formatted with `black` 25.1.0 |
| `prompts/interrupted-runs/logs/07-verification-and-close-out.md` | new: this log |
| `prompts/interrupted-runs/IMPLEMENTATION_STATE.md` | the header (**CLOSED**), §1's row for 07 and the suite sentence, Z1 ✅, §2's dated line, §3's count line and a dated line under each of its six entries |
| `prompts/interrupted-runs/README.md` | its header paragraph, §2's row for 07, a dated line under §7 |
| `prompts/INDEX.md` | the header, and the campaign's line: **closed**, 6 open issues |
| `docs/OPEN_ISSUES.md` | the header's date, and §1.3's heading: closed 2026-10-18, by 07; the count stays 11 |

Not touched: anything under `runregistrykit/` or `.github/`; `pyproject.toml`, `README.md`,
`PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`; `docs/releases/`, `docs/adoption/`,
`docs/extraction/`, `docs/extraction-verification.md`; the prompt, any other part of the campaign
README, `orchestrator/`. No client, DatastoreKit or RayPoolKit file. At the end, `git diff aeacba8 --
runregistrykit pyproject.toml README.md PROVENANCE.md docs/releases docs/adoption docs/extraction
docs/extraction-verification.md .github` is empty (§11 below).

## Deviations from the prompt

Each is classified. Corrections 1–18 are section 0's; those that changed nothing the prompt asks
are recorded where they bear on the work.

1. **Correction 1: 44 commits, not 42.** The document's §2.1 classes every commit from `b56ecc7` to
   `e4bf592`, the commit before this one: the prompt's 42, then `c094811` (07 written) and `e4bf592`
   (07's orchestration note). Counted by script and read (§9 below). **STRUCTURALLY REQUIRED.**
2. **Correction 2: "`main` is pushed"** read as `origin/main` at `aeacba8` (`git ls-remote`), with
   `c094811` and `e4bf592` local, as they stay. Not a stop. **STRUCTURALLY REQUIRED.**
3. **Correction 3: every process imports the pin.** Each child and each `python -m runregistrykit`
   the script starts runs in the client root under `TMPDIR`, with `PYTHONPATH`, `PYTHONSAFEPATH`
   and the git environment removed from its environment. The script prints its own
   `runregistrykit.__file__`, what a command run in the client root imports, and each child's beside
   its run id, and checks that all are one file under `sysconfig.get_paths()["purelib"]`; a failure
   of that check fails the run, `RESULT: FAIL (site-packages)`. **STRUCTURALLY REQUIRED.**
4. **Correction 4: the two runs named apart.** Steps 8 and 9 end step 2's run, "the hard-killed
   run" (slug `hard-killed`); step 6's is "the signalled run" (slug `signalled`), which its own
   handler ends `killed` in step 7. **STRUCTURALLY REQUIRED.**
5. **Correction 5: step 6's "status unchanged"** is checked as: after both refused `end`s, `state`
   `running`, no `ended`, `exit_code` null, `pid` the child's, and the child still alive.
   **STRUCTURALLY REQUIRED.**
6. **Correction 6: the children synchronised and bounded.** Each child prints one JSON line once it
   has begun (step 6's once its handler is installed), read through `select` with a 30 s timeout;
   a child that does not say so is killed, reaped and that step's `FAIL` with its stderr. Every wait
   has a 30 s timeout, each command 120 s; the `finally` kills and reaps any child still alive, or
   reaps one that has exited, and says which. **STRUCTURALLY REQUIRED.**
7. **Correction 7: the signatures**, re-read at `0bae3a3` (`begin` `runregistrykit/__init__.py:987`,
   `Run.heartbeat` `:786`, `Run.finish` `:805`, `liveness` `:612`; `end`'s success line
   `__main__.py:470`; `_end_run` `:1259`, "already ended" `:1329`, "answers kill -0" `:1352`;
   `begin`'s `No run directory was created` `:1125`): as the note gives them. **STRUCTURALLY
   REQUIRED.**
8. **Correction 8: breakage (b) read whole.** Steps 2, 3, 8, 9, 10, 11, 12 and 13 fail; step 8 on
   "answers kill -0", 2 and 3 because the zombie answers `kill -0`, 9–13 because the run was never
   ended; the child is reaped by the `finally`, since step 8 stops before the moved reap. §"The
   deliberate-breakage record" gives `liveness` and `list`'s row before the reap. **STRUCTURALLY
   REQUIRED.** One choice of the script's makes the record cleaner: step 9 first checks that step 8
   left the run `lost`, and fails without running `end` when it did not, so that a run step 8 did
   not end is never ended by step 9. Without it, (a) would end the run at step 9 and step 11's
   `begin` would be accepted, against the prompt's §4.5 (a). **IMPLEMENTATION CHOICE.**
9. **Correction 9: (c) step by step.** Steps 1, 11 and 12 need the client's module (its writer, or
   the fingerprinter) and fail, each saying what it saw; steps 2–10 and 13 need none of it and pass,
   step 4 among them, since `fingerprint_store` refuses for the run before it loads the
   fingerprinter. No exception escaped a step; exit 1. **STRUCTURALLY REQUIRED.**
10. **Correction 10: the breakage diffs replayable.** (a) and (b) below carry the repository path,
    and were each checked with `git apply --check` and `git apply -R --check`, applied and reversed,
    in `bash`, in a scratch clone of this repository holding the script, never in this checkout;
    after each, the clone's script equalled this checkout's (`cmp`) and `git status` here was
    unchanged. **STRUCTURALLY REQUIRED.**
11. **Corrections 11 and 12: the high end and 3.14.8.** A `git clone` of `e4bf592` installed
    editable into a fresh 3.13.16 venv, the suite run from the clone's root; `test_status_writes` at
    `/opt/local/bin/python3.14` with `PYTHONPATH` the clone: 22 tests, OK, no skip. The document says
    that pass records nothing about L11's window. **STRUCTURALLY REQUIRED.**
12. **The headline's "four found and resolved along the way"** (the prompt's §2.1, row 1) is three on
    the board: `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]`,
    `[02-the-landed-record-is-unpinned-and-can-move-backwards]` and
    `[04-a-pid-out-of-range-makes-pid-alive-raise]`; board §4 holds eight, five of them assigned. The
    document says three, and names the fourth found, `[02b-a-raising-handler-can-leave-the-status-lock-held]`,
    as fixed at 3.12 and 3.13 and narrowed, open. The board is right. **STRUCTURALLY REQUIRED.**
13. **The deviation counts are entries, not words** (correction 16). The prompt's word table was
    re-counted (`grep -o`, one line) and agrees log by log; the document's table counts entries,
    and says where it differs from 03's and 05's reviews and why. **STRUCTURALLY REQUIRED.**
14. **The second store is only named.** Step 6's child begins on `smoke-second.sqlite`, which no step
    writes; `begin` reads its absent sidecar and proceeds, and nothing reads its content. So steps 6
    and 7 need no store, and pass in the core venv. **IMPLEMENTATION CHOICE.**
15. **The script writes no bytecode beside the extraction script.** Loading a file by path writes a
    `__pycache__/` beside it unless bytecode is off; the session's shell had
    `PYTHONDONTWRITEBYTECODE=1`, a reader's may not. The script sets `sys.dont_write_bytecode` while
    it loads the file, and a run with the variable unset, `--clean`, left `docs/` as it was (§4
    below). **IMPLEMENTATION CHOICE.**
16. **The user's `python` processes are recorded by pid and program**, not by their whole command
    lines: one of them, a file-sync client's helper, carries a machine identifier in its arguments.
    The full lists were compared in scratch. **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT.

## Verification performed

All in `/private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/f6f0f266-814e-488f-b098-ff9c465aac14/scratchpad/agent-07/`
("`<scratch>`" below), with `TMPDIR` in it for every command; no scratch file under `runregistrykit/`
or `docs/`.

### 1. The state at the start

`HEAD` `e4bf592`, `main`, clean; `git worktree list` this checkout alone; `origin/main` `aeacba8`
(`git ls-remote`), `refs/tags/v0.2.0` `895e3c70…`, `^{}` `0bae3a3c501a…`. `git diff --stat 0bae3a3
HEAD -- runregistrykit pyproject.toml README.md .github docs/releases docs/adoption docs/extraction`
empty; no `docs/interrupted-runs-verification.md` and no `docs/interrupted-runs/`. `git rev-list
--count b56ecc7^..aeacba8` 42, `b56ecc7^..HEAD` 44. `git status --short --ignored`:
`prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
`runregistrykit/tests/__pycache__/`, `var/`, `venv/`. `var/ledger.jsonl` SHA-256 `471d0859…`
(SHA-1 `93589747…`, the note's figure), unchanged at the end. No Ray process; `RAY_ADDRESS` unset;
the shell has `PYTHONDONTWRITEBYTECODE=1`. Tools: `venv/` Python 3.12.15, `runregistrykit` 0.2.0
editable, `datastorekit` 0.4.0 (`direct_url.json` `c8570e84…`, `v0.4.0`), Ray 2.43.0, SQLAlchemy
2.0.39, `black` 25.1.0; `uv` 0.12.20; `git` 2.56.0; macOS 27.0.1 `arm64`.

### 2. The suite

**In `venv/`, before:** `Ran 410 tests in 161.447s`, `OK (skipped=1)`, CLAUDE.md's command from the
repository root, output to `<scratch>/out/suite-before.txt`. **After** (on the tree as committed):
`Ran 410 tests in 161.096s`, `OK (skipped=1)`, output to `<scratch>/out/suite-after.txt`. No Ray process before or after either run; `git status --short --ignored` and
`var/ledger.jsonl` the same before and after.

**At the high end:** `<scratch>/suite-high`, `uv venv --python /opt/local/bin/python3.13`, `uv pip
install --no-cache -e "<scratch>/clone-high[stores]"` with `datastorekit @ …@v0.4.0`, `ray==2.55.1`,
`sqlalchemy==2.0.46` (21 packages; `runregistrykit` 0.2.0 from the clone; `datastorekit` from
`c8570e84…`), the clone a `git clone` of `e4bf592`; run from the clone's root, its
`runregistrykit.__file__` the clone's: `Ran 410 tests in 171.955s`, `OK (skipped=1)`. No Ray process
before or after; the clone clean after.

**By module**, by the loader (`unittest.defaultTestLoader.discover("runregistrykit/tests",
top_level_dir=".")`, each test's module counted), the same in both venvs (`diff` of the two lists
empty) and equal to section 0's facts:

```text
 27 runregistrykit.tests.test_client_root
 27 runregistrykit.tests.test_end
  4 runregistrykit.tests.test_end_stores
 31 runregistrykit.tests.test_fingerprinter
 28 runregistrykit.tests.test_host
  3 runregistrykit.tests.test_host_stores
  3 runregistrykit.tests.test_package_imports
 22 runregistrykit.tests.test_package_is_generic
  8 runregistrykit.tests.test_public_names
 29 runregistrykit.tests.test_run_registry
 23 runregistrykit.tests.test_second_writer
  9 runregistrykit.tests.test_second_writer_stores
 22 runregistrykit.tests.test_status_writes
 21 runregistrykit.tests.test_store_amend
  9 runregistrykit.tests.test_store_amend_residuals
  2 runregistrykit.tests.test_store_command_line
 27 runregistrykit.tests.test_store_copy_move
 29 runregistrykit.tests.test_store_fingerprint
 41 runregistrykit.tests.test_store_retire
 10 runregistrykit.tests.test_store_retire_references
 17 runregistrykit.tests.test_store_sidecar
 11 runregistrykit.tests.test_unreadable_status
  7 runregistrykit.tests.test_unreadable_status_stores
410 total
```

The one skip, in each, by `-v` of `test_host`: `test_the_readers_on_linux
(runregistrykit.tests.test_host.TestTheReaders.test_the_readers_on_linux) ... skipped "the Linux
readers run only on Linux, which CI's runner is; the macOS test runs on macOS"`.

**At 3.14.8:** from the clone's root, `PYTHONPATH=<scratch>/clone-high /opt/local/bin/python3.14 -m
unittest -v runregistrykit.tests.test_status_writes`: `Ran 22 tests in 16.114s`, `OK`, 22 lines
`... ok`, no skip, `TestARaisingHandlerAtEveryJump.test_the_lock_is_free_and_nothing_is_in_flight`
among them.

### 3. The installs

Each venv made with `uv venv --python <interpreter> <scratch>/<venv>`, then:

```bash
uv pip install --no-cache --python <scratch>/pin-low/bin/python \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.43.0' 'sqlalchemy==2.0.39'
uv pip install --no-cache --python <scratch>/pin-high/bin/python \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
uv pip install --no-cache --python <scratch>/pin-core/bin/python \
  'runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.2.0'
```

- **low** (3.12.15): exit 0, `Resolved 23 packages in 839ms`; `Updated
  https://github.com/ds283/RunRegistryKit (0bae3a3c501a8264ee4be5bc24f06422af38720f)`, `Updated
  https://github.com/ds283/DatastoreKit (c8570e849334d09085bbd84876095fc9e22bd005)`; installed
  `runregistrykit==0.2.0`, `datastorekit==0.4.0`, `ray==2.43.0`, `sqlalchemy==2.0.39` and 19 others;
  `time -p` real 5.99 s.
- **high** (3.13.16): exit 0, `Resolved 21 packages in 492ms`; the same two commits;
  `runregistrykit==0.2.0`, `datastorekit==0.4.0`, `ray==2.55.1`, `sqlalchemy==2.0.46` and 17 others;
  real 5.78 s.
- **core** (3.12.15): exit 0, `Resolved 1 package in 121ms`; `runregistrykit==0.2.0` from
  `0bae3a3c501a…`, alone; real 3.48 s.

Read in each with `<scratch>/out/what_installed.py`, run with `-I` from an empty directory, then
`git show 0bae3a3:runregistrykit/<module> | cmp - <site-packages>/runregistrykit/<module>` and `grep
-c tests` of `RECORD` (the core venv's output; the other two differ only in the Python, the path and
the three dependencies' versions, `find_spec` true):

```text
=== pin-core
python 3.12.15
runregistrykit 0.2.0 <scratch>/pin-core/lib/python3.12/site-packages/runregistrykit/__init__.py
requires ['datastorekit>=0.4.0; extra == "stores"']
datastorekit not installed find_spec: False
ray not installed find_spec: False
sqlalchemy not installed find_spec: False
direct_url {"url":"https://github.com/ds283/RunRegistryKit","vcs_info":{"vcs":"git","commit_id":"0bae3a3c501a8264ee4be5bc24f06422af38720f","requested_revision":"v0.2.0"}}
RECORD entries 14
   runregistrykit-0.2.0.dist-info/INSTALLER
   runregistrykit-0.2.0.dist-info/METADATA
   runregistrykit-0.2.0.dist-info/RECORD
   runregistrykit-0.2.0.dist-info/REQUESTED
   runregistrykit-0.2.0.dist-info/WHEEL
   runregistrykit-0.2.0.dist-info/direct_url.json
   runregistrykit-0.2.0.dist-info/licenses/LICENSE
   runregistrykit-0.2.0.dist-info/top_level.txt
   runregistrykit-0.2.0.dist-info/uv_build.json
   runregistrykit/__init__.py
   runregistrykit/__main__.py
   runregistrykit/client.py
   runregistrykit/fingerprint.py
   runregistrykit/stores.py
import runregistrykit.tests: ModuleNotFoundError
cmp __init__.py: equal
cmp __main__.py: equal
cmp client.py: equal
cmp fingerprint.py: equal
cmp stores.py: equal
__init__.py
__main__.py
__pycache__
client.py
fingerprint.py
stores.py
0
```

### 4. The smoke runs

Each from the repository root, through `<scratch>/out/smoke.sh <name> <venv>`, which records `pgrep
-lf 'gcs_server|raylet|ray::|default_worker\.py'` and `ps -o pid,ppid,stat,command -U <uid> | grep
-i '[p]ython'` before and after, and runs `TMPDIR=<scratch>/tmp/smoke-<name> <scratch>/<venv>/bin/python
docs/interrupted-runs/interrupted_run_smoke.py`. **Before and after every run below, `pgrep` found
nothing (exit 1), and the user's `python` processes were the same six**, by pid: 1994 (a software
manager's usage monitor), 38208 and 38498 (an editor's Python tools), 53842 (a file-sync client's
resource tracker), 90676 and 90678 (another file-sync client's helpers). None is a child of a run.

**Low end** (`pin-low`): exit 0; the script's time 3.8 s, `smoke.sh`'s wall 4.07 s, `time -p` real
4.49 s. Whole:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
client files    from /Users/ds283/Documents/Code/RunRegistryKit/docs/extraction/store_smoke_run.py
directory       $SMOKE = <scratch>/tmp/smoke-low/interrupted-smoke-zmkbcwlr
its commands    import <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
site-packages   <scratch>/pin-low/lib/python3.12/site-packages: the package is under it

PASS step 1: a store written by the client's module, and `store create --purpose`
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id ae3a93fd6d504f5bab9ca02fea00fa31
PASS step 2: a hard kill: a child begun on the store, heartbeating, sent SIGKILL and reaped
  started the hard-killed run's child: pid 46981
    > run smoke-02-hard-killed-20261018T181347, pid 46981
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  sent SIGKILL to pid 46981
    > reaped: returncode -9
    > status: state running, pid 46981, units_done 1, host keys ['boot', 'id'], host.id 8d2b247824882486, host.boot <36 characters>
    > liveness(status, 900): stale
PASS step 3: `list`: the hard-killed run marked `!!`, and stderr naming `end`
  $ python -m runregistrykit list   (in client/)
    exit 0
    > !! smoke-02-hard-killed-20261018T181347  running         1/?       1s  a smoke run that is hard-killed  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 stale; 0 with no host recorded.
    > !! 1 run(s) say they are running and are not: the pid does not answer kill -0, the heartbeat is older than 900 s, or this machine has rebooted since. Nothing here has killed or cleaned anything — go and look. Once you know one is over, end it with `python -m runregistrykit end RUN_ID --reason TEXT`.
PASS step 4: `store fingerprint` refused, naming the run and `end`
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    > !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181347 is running (stale, pid 46981) and names this store by its results and results_store_id. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
PASS step 5: a second `begin` on the store refused, with no run directory made
  begin(): RuntimeError: Cannot begin run smoke-05-second-20261018T181347 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181347 is running (stale, pid 46981) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
    > runs root before: ['smoke-02-hard-killed-20261018T181347']
    > runs root after:  ['smoke-02-hard-killed-20261018T181347']
PASS step 6: a live pid refused by `end`, with and without `--unverified`
  started the signalled run's child: pid 47001
    > run smoke-06-signalled-20261018T181347, pid 47001
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  $ python -m runregistrykit end smoke-06-signalled-20261018T181347 --reason the smoke run tries to end a live run   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181347: its pid 47001 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
  $ python -m runregistrykit end smoke-06-signalled-20261018T181347 --reason the smoke run tries to end a live run --unverified   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181347: its pid 47001 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
    > status: state running, ended absent, exit_code None, pid 47001
PASS step 7: a real SIGTERM: the child's handler records `killed`, 143, and exits
  sent SIGTERM to pid 47001
    > reaped: returncode 143
    > status: parses, state killed, exit_code 143
    > temporary files left: none
PASS step 8: `end` of the hard-killed run: no `--reason` refused by argparse, then the run `lost`
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181347   (in client/)
    exit 2
    > usage: runregistrykit end [-h] --reason TEXT [--unverified] [--root DIR]
    > runregistrykit end: error: the following arguments are required: --reason
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181347 --reason the smoke run's child was sent SIGKILL by the script   (in client/)
    exit 0
    > >> end: smoke-02-hard-killed-20261018T181347 is now lost, verified: its pid 46981 does not answer kill -0 on this host
    > status: state lost, exit_code None, ended.verified True, ended.evidence.pid_answers False, ended.reason "the smoke run's child was sent SIGKILL by the script"
PASS step 9: `end` of the hard-killed run again: refused, it has already ended
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181347 --reason the smoke run ends it twice   (in client/)
    exit 1
    > !! Cannot end smoke-02-hard-killed-20261018T181347: its status says it has already ended, as 'lost'; end records only a run whose end the registry never saw. Nothing was written
PASS step 10: `list`: the run `lost`, unmarked, and every run counted finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    >    smoke-02-hard-killed-20261018T181347  lost            1/?       2s  a smoke run that is hard-killed  · working
    > 2 run(s) under $SMOKE/client/var/runs: 2 finished; 0 with no host recorded.
PASS step 11: the resume: `begin` on the store accepted, and its fingerprint recorded
  begin(): smoke-11-resumed-20261018T181348
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
PASS step 12: `store fingerprint` matching, and `store retire --dry-run`, each exiting 0
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > digest:   e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > recorded: matches the fingerprint taken 2026-10-18T18:13:48+01:00 by run smoke-11-resumed-20261018T181348, at c5d5b134b45cae34f83d1fed9f4491a05b28b545
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-store.sqlite --reason the smoke run checks the store could be retired --dry-run   (in client/)
    exit 0
    > dry run:  nothing was written or deleted
PASS step 13: the resumed run's manifest `host.id` recorded, and its status's
    > manifest host.id 8d2b247824882486, status host.id 8d2b247824882486

children: 2 started; each reaped by its step
ray: imported, initialised: False
time: 3.8 s
left in place: <scratch>/tmp/smoke-low/interrupted-smoke-zmkbcwlr
RESULT: OK (13 steps passed)
```

**High end** (`pin-high`): exit 0; 6.3 s, wall 6.62 s, real 6.94 s. Whole:

```text
python          3.13.16 (<scratch>/pin-high/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-high/lib/python3.13/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.55.1
sqlalchemy      2.0.46
client files    from /Users/ds283/Documents/Code/RunRegistryKit/docs/extraction/store_smoke_run.py
directory       $SMOKE = <scratch>/tmp/smoke-high/interrupted-smoke-0w14td2y
its commands    import <scratch>/pin-high/lib/python3.13/site-packages/runregistrykit/__init__.py
site-packages   <scratch>/pin-high/lib/python3.13/site-packages: the package is under it

PASS step 1: a store written by the client's module, and `store create --purpose`
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id b7088b595980440d8fa429f7c4801996
PASS step 2: a hard kill: a child begun on the store, heartbeating, sent SIGKILL and reaped
  started the hard-killed run's child: pid 47087
    > run smoke-02-hard-killed-20261018T181352, pid 47087
    > its runregistrykit: <scratch>/pin-high/lib/python3.13/site-packages/runregistrykit/__init__.py
  sent SIGKILL to pid 47087
    > reaped: returncode -9
    > status: state running, pid 47087, units_done 1, host keys ['boot', 'id'], host.id 8d2b247824882486, host.boot <36 characters>
    > liveness(status, 900): stale
PASS step 3: `list`: the hard-killed run marked `!!`, and stderr naming `end`
  $ python -m runregistrykit list   (in client/)
    exit 0
    > !! smoke-02-hard-killed-20261018T181352  running         1/?       1s  a smoke run that is hard-killed  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 stale; 0 with no host recorded.
    > !! 1 run(s) say they are running and are not: the pid does not answer kill -0, the heartbeat is older than 900 s, or this machine has rebooted since. Nothing here has killed or cleaned anything — go and look. Once you know one is over, end it with `python -m runregistrykit end RUN_ID --reason TEXT`.
PASS step 4: `store fingerprint` refused, naming the run and `end`
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    > !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181352 is running (stale, pid 47087) and names this store by its results and results_store_id. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
PASS step 5: a second `begin` on the store refused, with no run directory made
  begin(): RuntimeError: Cannot begin run smoke-05-second-20261018T181353 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181352 is running (stale, pid 47087) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
    > runs root before: ['smoke-02-hard-killed-20261018T181352']
    > runs root after:  ['smoke-02-hard-killed-20261018T181352']
PASS step 6: a live pid refused by `end`, with and without `--unverified`
  started the signalled run's child: pid 47096
    > run smoke-06-signalled-20261018T181353, pid 47096
    > its runregistrykit: <scratch>/pin-high/lib/python3.13/site-packages/runregistrykit/__init__.py
  $ python -m runregistrykit end smoke-06-signalled-20261018T181353 --reason the smoke run tries to end a live run   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181353: its pid 47096 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
  $ python -m runregistrykit end smoke-06-signalled-20261018T181353 --reason the smoke run tries to end a live run --unverified   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181353: its pid 47096 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
    > status: state running, ended absent, exit_code None, pid 47096
PASS step 7: a real SIGTERM: the child's handler records `killed`, 143, and exits
  sent SIGTERM to pid 47096
    > reaped: returncode 143
    > status: parses, state killed, exit_code 143
    > temporary files left: none
PASS step 8: `end` of the hard-killed run: no `--reason` refused by argparse, then the run `lost`
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181352   (in client/)
    exit 2
    > usage: runregistrykit end [-h] --reason TEXT [--unverified] [--root DIR]
    > runregistrykit end: error: the following arguments are required: --reason
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181352 --reason the smoke run's child was sent SIGKILL by the script   (in client/)
    exit 0
    > >> end: smoke-02-hard-killed-20261018T181352 is now lost, verified: its pid 47087 does not answer kill -0 on this host
    > status: state lost, exit_code None, ended.verified True, ended.evidence.pid_answers False, ended.reason "the smoke run's child was sent SIGKILL by the script"
PASS step 9: `end` of the hard-killed run again: refused, it has already ended
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181352 --reason the smoke run ends it twice   (in client/)
    exit 1
    > !! Cannot end smoke-02-hard-killed-20261018T181352: its status says it has already ended, as 'lost'; end records only a run whose end the registry never saw. Nothing was written
PASS step 10: `list`: the run `lost`, unmarked, and every run counted finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    >    smoke-02-hard-killed-20261018T181352  lost            1/?       2s  a smoke run that is hard-killed  · working
    > 2 run(s) under $SMOKE/client/var/runs: 2 finished; 0 with no host recorded.
PASS step 11: the resume: `begin` on the store accepted, and its fingerprint recorded
  begin(): smoke-11-resumed-20261018T181354
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
PASS step 12: `store fingerprint` matching, and `store retire --dry-run`, each exiting 0
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > digest:   e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > recorded: matches the fingerprint taken 2026-10-18T18:13:54+01:00 by run smoke-11-resumed-20261018T181354, at 1efaf1ee44ee8279880d0483fa5fd15a35d86b6b
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-store.sqlite --reason the smoke run checks the store could be retired --dry-run   (in client/)
    exit 0
    > dry run:  nothing was written or deleted
PASS step 13: the resumed run's manifest `host.id` recorded, and its status's
    > manifest host.id 8d2b247824882486, status host.id 8d2b247824882486

children: 2 started; each reaped by its step
ray: imported, initialised: False
time: 6.3 s
left in place: <scratch>/tmp/smoke-high/interrupted-smoke-0w14td2y
RESULT: OK (13 steps passed)
```

Earlier runs of the same script gave `RESULT: OK (13 steps passed)` at both ends too: 6.0 s and
5.9 s before its last two edits (the `repr` of the marker in steps 3 and 10, and the bytecode
guard), and 6.1 s and 6.3 s before the second alone; the runs above are of the file as committed (SHA-256 `61bb25cf77c4e863…`).

**Two more runs**, for the record:
- with `venv/`'s Python, whose `runregistrykit` is this checkout's (editable): every step passes and
  `RESULT: FAIL (site-packages)`, exit 1, the check of correction 3 biting (`site-packages
  …/venv/lib/python3.12/site-packages: NOT`);
- with `PYTHONDONTWRITEBYTECODE` unset and `--clean`, in `pin-low`: `RESULT: OK (13 steps passed)`,
  its directory removed, and `git status --short --ignored docs` showing only the new
  `docs/interrupted-runs/`, no `__pycache__/` beside the extraction script.

**Exit 2**: `PATH=/nonexistent` → "CANNOT START: no git on PATH"; `/opt/local/bin/python3.12 -I` →
"CANNOT START: runregistrykit is not importable (No module named 'runregistrykit')"; the script
copied alone to `<scratch>/alone/` → "CANNOT START: the extraction's smoke script is not at
<scratch>/extraction/store_smoke_run.py". Nothing was made under `TMPDIR` by any of the three.

### 5. The extraction's smoke run against `v0.2.0`

`TMPDIR=<scratch>/tmp/extraction-<end> <scratch>/pin-<end>/bin/python docs/extraction/store_smoke_run.py`,
from the repository root. No Ray process before or after. Exit 1 at both ends, `RESULT: FAIL (3)`,
11.0 s and 10.5 s. Low end, whole:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
directory       $SMOKE = <scratch>/tmp/extraction-low/store-smoke-tricaq77

PASS step 1: a store written by the client's module, and `store create --purpose`
  written: smoke-store-shard0000.sqlite, smoke-store-shard0001.sqlite, smoke-store.sqlite
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id 8ab66f6b4e544929b47d40ad4c4ebed9
PASS step 2: a run that takes a fingerprint of its results store
  begin(): smoke-02-fingerprinted-20261018T180447
  known(): ['u1']
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > manifest packages: ['datastorekit', 'runregistrykit']
FAIL step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261018T180447  done            1/1       0s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished; 0 with no host recorded.
  !! expected the summary '1 run(s) ... 1 finished.'; saw 1 run(s) under $SMOKE/client/var/runs: 1 finished; 0 with no host recorded.
PASS step 4: `store show`: a registry sidecar, no problems, the run naming the store
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > kind:     registry
    > problems: none
    > smoke-02-fingerprinted-20261018T180447  done      finished  by results and results_store_id
PASS step 5: `store fingerprint`: the recorded fingerprint matched by a fresh one
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > digest:   e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > format:   1
    > recorded: matches the fingerprint taken 2026-10-18T18:04:47+01:00 by run smoke-02-fingerprinted-20261018T180447, at 9438b19108c4da9d4f09a2d4cbb3162c8c6a9f74
PASS step 6: `store copy --purpose` of the store, and `store move` of the copy
  $ python -m runregistrykit store copy $SMOKE/client/var/datastores/smoke-store.sqlite $SMOKE/client/var/datastores/smoke-copy.sqlite --purpose a smoke copy   (in client/)
    exit 0
    > >> copy: $SMOKE/client/var/datastores/smoke-copy.manifest.json
  $ python -m runregistrykit store move $SMOKE/client/var/datastores/smoke-copy.sqlite $SMOKE/client/var/datastores/smoke-moved.sqlite   (in client/)
    exit 0
    > >> move: $SMOKE/client/var/datastores/smoke-moved.manifest.json
  moved: smoke-moved-shard0000.sqlite, smoke-moved-shard0001.sqlite, smoke-moved.sqlite
    > history: ['create', 'copy', 'move']
PASS step 7: `store amend --field x_note --remove` of a field written by hand
  wrote x_note into the moved copy's sidecar by hand
  $ python -m runregistrykit store amend $SMOKE/client/var/datastores/smoke-moved.sqlite --field x_note --remove --reason the smoke run removes a field it wrote   (in client/)
    exit 0
    > field:    x_note
    > before:   "written by hand"
    > after:    null
    > >> amended: $SMOKE/client/var/datastores/smoke-moved.manifest.json
PASS step 8: `store adopt` of a store whose sidecar is a legacy object
  wrote the legacy sidecar: {"datastore": "smoke-legacy.sqlite", "purpose": "a legacy smoke store"}
  $ python -m runregistrykit store adopt $SMOKE/client/var/datastores/smoke-legacy.sqlite   (in client/)
    exit 0
    > >> adopt: $SMOKE/client/var/datastores/smoke-legacy.manifest.json
    > sidecar_format 1, purpose 'a legacy smoke store', history ['adopt']
PASS step 9: `store retire --dry-run`, `store retire` and `store show` of the moved copy
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy --dry-run   (in client/)
    exit 0
    > dry run:  nothing was written or deleted
    > files to be deleted:
    > var/datastores/smoke-moved-shard0000.sqlite
    > var/datastores/smoke-moved-shard0001.sqlite
    > var/datastores/smoke-moved.sqlite
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy   (in client/)
    exit 0
    > matched: a fresh read-only fingerprint matched the recorded one, digest e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > files deleted:
    > var/datastores/smoke-moved-shard0000.sqlite
    > var/datastores/smoke-moved-shard0001.sqlite
    > var/datastores/smoke-moved.sqlite
    > >> retired: $SMOKE/client/var/datastores/smoke-moved.manifest.json
  left: no store file
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-moved.sqlite   (in client/)
    exit 0
    > state:     retired
    > completed: 2026-10-18T18:04:54+01:00
    > problems: none
PASS step 10: a run begun in a linked worktree, recorded under the main checkout
  git worktree add --detach worktree
  begin(): smoke-10-worktree-20261018T180454
    > run directory: $SMOKE/client/var/runs/smoke-10-worktree-20261018T180454
    > manifest script: $SMOKE/worktree/job.py
PASS step 11: the refusals: no fingerprinter named, and no config at all
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in no-fingerprinter/)
    exit 1
    > !! $SMOKE/no-fingerprinter/runregistrykit.toml names no fingerprinter, and the store layer requires one. Add [stores] with fingerprinter = "module:attribute", naming the client's Fingerprinter (runregistrykit.fingerprint), such as a DatastoreKitFingerprinter of its registry and its format number
  $ python -m runregistrykit list   (in elsewhere/)
    exit 1
    > !! No runregistrykit.toml in $SMOKE/elsewhere or any directory above it. Create one at the client's root; an empty file takes the defaults (runs_root = "var/runs", stores_root = "var/datastores", distributions = [])

ray: imported, initialised: False
digest (status.json): e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
digest (store fingerprint): e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
time: 11.0 s
left in place: <scratch>/tmp/extraction-low/store-smoke-tricaq77
RESULT: FAIL (3)
```

High end, whole:

```text
python          3.13.16 (<scratch>/pin-high/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-high/lib/python3.13/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.55.1
sqlalchemy      2.0.46
directory       $SMOKE = <scratch>/tmp/extraction-high/store-smoke-a5gvje07

PASS step 1: a store written by the client's module, and `store create --purpose`
  written: smoke-store-shard0000.sqlite, smoke-store-shard0001.sqlite, smoke-store.sqlite
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id 2e45b5a42a104e1daf7f5bc0b0065fcd
PASS step 2: a run that takes a fingerprint of its results store
  begin(): smoke-02-fingerprinted-20261018T180457
  known(): ['u1']
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > manifest packages: ['datastorekit', 'runregistrykit']
FAIL step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261018T180457  done            1/1       1s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished; 0 with no host recorded.
  !! expected the summary '1 run(s) ... 1 finished.'; saw 1 run(s) under $SMOKE/client/var/runs: 1 finished; 0 with no host recorded.
PASS step 4: `store show`: a registry sidecar, no problems, the run naming the store
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > kind:     registry
    > problems: none
    > smoke-02-fingerprinted-20261018T180457  done      finished  by results and results_store_id
PASS step 5: `store fingerprint`: the recorded fingerprint matched by a fresh one
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > digest:   e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > format:   1
    > recorded: matches the fingerprint taken 2026-10-18T18:04:58+01:00 by run smoke-02-fingerprinted-20261018T180457, at 6812dd35a054799c0bac38f743b6a10310f9fa8d
PASS step 6: `store copy --purpose` of the store, and `store move` of the copy
  $ python -m runregistrykit store copy $SMOKE/client/var/datastores/smoke-store.sqlite $SMOKE/client/var/datastores/smoke-copy.sqlite --purpose a smoke copy   (in client/)
    exit 0
    > >> copy: $SMOKE/client/var/datastores/smoke-copy.manifest.json
  $ python -m runregistrykit store move $SMOKE/client/var/datastores/smoke-copy.sqlite $SMOKE/client/var/datastores/smoke-moved.sqlite   (in client/)
    exit 0
    > >> move: $SMOKE/client/var/datastores/smoke-moved.manifest.json
  moved: smoke-moved-shard0000.sqlite, smoke-moved-shard0001.sqlite, smoke-moved.sqlite
    > history: ['create', 'copy', 'move']
PASS step 7: `store amend --field x_note --remove` of a field written by hand
  wrote x_note into the moved copy's sidecar by hand
  $ python -m runregistrykit store amend $SMOKE/client/var/datastores/smoke-moved.sqlite --field x_note --remove --reason the smoke run removes a field it wrote   (in client/)
    exit 0
    > field:    x_note
    > before:   "written by hand"
    > after:    null
    > >> amended: $SMOKE/client/var/datastores/smoke-moved.manifest.json
PASS step 8: `store adopt` of a store whose sidecar is a legacy object
  wrote the legacy sidecar: {"datastore": "smoke-legacy.sqlite", "purpose": "a legacy smoke store"}
  $ python -m runregistrykit store adopt $SMOKE/client/var/datastores/smoke-legacy.sqlite   (in client/)
    exit 0
    > >> adopt: $SMOKE/client/var/datastores/smoke-legacy.manifest.json
    > sidecar_format 1, purpose 'a legacy smoke store', history ['adopt']
PASS step 9: `store retire --dry-run`, `store retire` and `store show` of the moved copy
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy --dry-run   (in client/)
    exit 0
    > dry run:  nothing was written or deleted
    > files to be deleted:
    > var/datastores/smoke-moved-shard0000.sqlite
    > var/datastores/smoke-moved-shard0001.sqlite
    > var/datastores/smoke-moved.sqlite
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy   (in client/)
    exit 0
    > matched: a fresh read-only fingerprint matched the recorded one, digest e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > files deleted:
    > var/datastores/smoke-moved-shard0000.sqlite
    > var/datastores/smoke-moved-shard0001.sqlite
    > var/datastores/smoke-moved.sqlite
    > >> retired: $SMOKE/client/var/datastores/smoke-moved.manifest.json
  left: no store file
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-moved.sqlite   (in client/)
    exit 0
    > state:     retired
    > completed: 2026-10-18T18:05:05+01:00
    > problems: none
PASS step 10: a run begun in a linked worktree, recorded under the main checkout
  git worktree add --detach worktree
  begin(): smoke-10-worktree-20261018T180505
    > run directory: $SMOKE/client/var/runs/smoke-10-worktree-20261018T180505
    > manifest script: $SMOKE/worktree/job.py
PASS step 11: the refusals: no fingerprinter named, and no config at all
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in no-fingerprinter/)
    exit 1
    > !! $SMOKE/no-fingerprinter/runregistrykit.toml names no fingerprinter, and the store layer requires one. Add [stores] with fingerprinter = "module:attribute", naming the client's Fingerprinter (runregistrykit.fingerprint), such as a DatastoreKitFingerprinter of its registry and its format number
  $ python -m runregistrykit list   (in elsewhere/)
    exit 1
    > !! No runregistrykit.toml in $SMOKE/elsewhere or any directory above it. Create one at the client's root; an empty file takes the defaults (runs_root = "var/runs", stores_root = "var/datastores", distributions = [])

ray: imported, initialised: False
digest (status.json): e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
digest (store fingerprint): e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
time: 10.5 s
left in place: <scratch>/tmp/extraction-high/store-smoke-a5gvje07
RESULT: FAIL (3)
```

Step 3 fails on its assertion that the summary contains `1 finished.`
(`docs/extraction/store_smoke_run.py:484-488`), and for no other reason: the run is listed, `done`,
and the summary says `1 finished; 0 with no host recorded.`, the clause 01 added
(`runregistrykit/__main__.py:660-663` at `0bae3a3`). The other ten steps pass at both ends.

### 6. `black`

`./venv/bin/black --check runregistrykit docs`: `38 files would be left unchanged.` (37 and the
script). The script was formatted with `./venv/bin/black` before every run above.

### 7. The documents' checks

- **Links**: `<scratch>/out/check_links.py docs/interrupted-runs-verification.md`, which drops fenced
  code, resolves each relative link from the document's directory, checks each anchor against the
  target's headings (GitHub's slug rule), and requires each external link to be
  `github.com/ds283/{RunRegistryKit,DatastoreKit}/` with a tag, a 40-hex commit or a run: 23 links, 1 bad.
- **`path:line`**: `<scratch>/out/check_citations.py` prints every `runregistrykit/…:N` the document
  cites as `git show 0bae3a3:<path> | sed -n`, and every `docs/…:N` at the tree; each was read and
  is the line the document says. Those the script's pattern does not catch were read by hand:
  `README.md:7-8`, `:126` and `:154-157`; `runregistrykit/stores.py:52` and `:1405-1418`;
  `smoke_registry.py:7` (the client's module, `REGISTRY_SOURCE`'s seventh line, `import sqlalchemy
  as sqla`); SGK's `requirements.txt:81` at `79434bf`.
- **The low end's output** in the document's §4.2 equals the run's (`diff` of the file and the
  document's block, empty).

### 8. The clients

Through `git -C <repository> rev-parse`, `log` and `status --porcelain` only, at the start and at the
end:

| Client | Branch | Start | End | `status --porcelain` |
|---|---|---|---|---|
| SGK | `handover-remedial` | `79434bf4f44d46905ba1f86bfa956e9be5880a34` | the same | 0 lines, and 0 at the end |
| CPBH | `main` | `3cd2be482c26d6c4b24b5d3a05c885fa304a9101` | the same | 22 lines, and 22 at the end |
| SI | `dk-and-rpk-migration` | `5fb4a1d71a016f1b23393923b9a3d59972415aa0` | the same | 0 lines, and 0 at the end |

SGK's newest commit of any branch is `79434bf` (`git log --all -1`). `git -C <SGK> show
79434bf:requirements.txt | sed -n 81p`: `runregistrykit[stores] @
git+https://github.com/ds283/RunRegistryKit@v0.1.0`. Nothing else of any client was read.

### 9. How each count was made

- **Commits**: `git log --reverse --format='%h %s' b56ecc7^..e4bf592` through a scratch classifier
  on the subject's form (`Plan the`; `Write the orchestration note`; `Review interrupted-runs`;
  `Record CI`; `Take `, `Assign ` or `Write interrupted-runs prompt`; else a prompt's own commit):
  1 / 10 / 9 / 8 / 8 / 8, 44. Each class was then read against the prompt's §1.3 list and section
  0: they agree, with `c094811` and `e4bf592` added.
- **CI**: `gh run view <id> --json …` for the ten runs, and `gh run list --limit 15`, which lists
  them and three earlier ones (`79015a7`, `caad864`, `aaa1d6d`), before the campaign's first prompt.
- **The suite**: the loader's counts, above; the board's §1 and each log's own before and after for
  the history.
- **Issues**: board §3 holds six `### ` entries and §4 eight; each entry's **Opened** line read for
  who opened it (five assigned, nine opened during the campaign, as the prompt lists them);
  `docs/OPEN_ISSUES.md`'s rows: 2 + 3 + 6 = 11.
- **Deviations and observations**: `<scratch>/out/count_deviations.py`, which takes each log's
  "Deviations from the prompt" and "Observations not acted on" sections, splits them into top-level
  numbered items (a line beginning `N. `; an unindented line after them, such as "No UNINTENDED
  DRIFT.", ends the list), joins each item's lines, and finds the three labels in it; and the
  labels' words with `re.findall` over the whole log, one line, as the prompt counted them. Then
  `-v` printed each entry's labels, and every entry was read against the log:

  ```text
  01: 1 SR+IC, 2 SR, 3 SR, 4 SR, 5 IC, 6 SR, 7 SR, 8 SR, 9 IC, 10 IC, 11 IC, 12 IC, 13 IC, 14 IC, 15 SR, 16 IC
    01-the-host: entries 16; SR 8 IC 9 UD 0 (UD in []); unlabelled []; two labels [1]; words (one line) [7, 7, 0]; observations 5
  02: 1 SR, 2 SR, 3 SR, 4 SR+IC, 5 SR, 6 SR, 7 SR, 8 SR, 9 SR, 10 SR, 11 SR, 12 SR, 13 IC, 14 IC, 15 IC, 16 IC, 17 SR, 18 IC, 19 IC, 20 IC, 21 IC, 22 IC, 23 IC, 24 IC
    02-status-writes: entries 24; SR 13 IC 12 UD 0 (UD in []); unlabelled []; two labels [4]; words (one line) [9, 11, 0]; observations 5
  02b: 1 SR, 2 SR, 3 SR, 4 SR, 5 SR, 6 SR, 7 SR+IC, 8 SR, 9 SR, 10 SR+IC, 11 SR, 12 SR, 13 SR, 14 SR, 15 SR, 16 SR, 17 SR, 18 SR, 19 SR, 20 IC, 21 IC, 22 IC, 23 IC, 24 UD
    02b-the-writers-bookkeeping: entries 24; SR 19 IC 6 UD 1 (UD in [24]); unlabelled []; two labels [7, 10]; words (one line) [14, 6, 1]; observations 4
  02c: 1 SR, 2 SR, 3 SR, 4 SR, 5 SR+IC, 6 IC, 7 SR, 8 SR, 9 SR, 10 SR, 11 SR, 12 IC, 13 SR, 14 SR, 15 SR, 16 SR, 17 SR, 18 IC, 19 IC, 20 IC
    02c-the-writers-lock: entries 20; SR 15 IC 6 UD 0 (UD in []); unlabelled []; two labels [5]; words (one line) [15, 4, 1]; observations 4
  03: 1 SR, 2 SR, 3 SR, 4 IC, 5 SR+IC, 6 -, 7 SR, 8 SR, 9 IC, 10 IC, 11 IC, 12 SR, 13 IC, 14 IC, 15 IC, 16 IC, 17 UD
    03-an-unreadable-status-is-in-use: entries 17; SR 7 IC 9 UD 1 (UD in [17]); unlabelled [6]; two labels [5]; words (one line) [7, 7, 1]; observations 6
  04: 1 SR, 2 SR, 3 SR, 4 SR, 5 SR, 6 SR, 7 IC, 8 IC, 9 SR, 10 SR, 11 SR, 12 IC, 13 SR, 14 IC, 15 SR, 16 IC, 17 IC, 18 IC, 19 SR
    04-end-a-run: entries 19; SR 12 IC 7 UD 0 (UD in []); unlabelled []; two labels []; words (one line) [11, 7, 0]; observations 7
  05: 1 SR, 2 SR, 3 IC, 4 IC, 5 SR, 6 SR, 7 SR, 8 SR, 9 SR, 10 SR, 11 SR, 12 SR, 13 SR, 14 -, 15 SR, 16 SR, 17 SR, 18 SR, 19 IC, 20 IC, 21 IC, 22 IC
    05-begin-refuses-a-second-writer: entries 22; SR 15 IC 6 UD 0 (UD in []); unlabelled [14]; two labels []; words (one line) [14, 6, 1]; observations 8
  06: 1 SR, 2 SR, 3 SR, 4 SR, 5 SR, 6 SR, 7 SR, 8 SR, 9 SR, 10 IC, 11 IC, 12 IC, 13 IC, 14 IC, 15 IC, 16 IC, 17 SR
    06-release-v0.2.0: entries 17; SR 10 IC 7 UD 0 (UD in []); unlabelled []; two labels []; words (one line) [9, 7, 1]; observations 7
  ```

  The words, `[7, 7, 0]` … `[9, 7, 1]`, are the prompt's §1.3 table exactly.
- **The observations' dispositions** (the document's §9): 2 addressed, 2 opened and since closed, 6
  opened and open, 3 already an open issue's, 6 recorded in the notes, 1 no action, 26 still
  observations, 46; counted from the table by hand twice.

### 10. Outside the scratch directory

Names in `/private/tmp` beginning `tmp` or `ray`, with their modification times, at the start:

```text
/private/tmp/ray 2026-10-16 00:15:43.281818962 +0100
/private/tmp/ray-cpbh 2026-10-18 00:00:00.783742600 +0100
/private/tmp/ray-cpbh-decoy 2026-10-17 00:00:01.516440545 +0100
/private/tmp/ray-decoy 2026-10-17 00:00:01.470173017 +0100
/private/tmp/ray-si 2026-10-17 00:00:01.640978523 +0100
(no name beginning tmp)
```

At the end:

```text
/private/tmp/ray 2026-10-16 00:15:43.281818962 +0100
/private/tmp/ray-cpbh 2026-10-18 00:00:00.783742600 +0100
/private/tmp/ray-cpbh-decoy 2026-10-17 00:00:01.516440545 +0100
/private/tmp/ray-decoy 2026-10-17 00:00:01.470173017 +0100
/private/tmp/ray-si 2026-10-17 00:00:01.640978523 +0100
(no name beginning tmp)
```

Unchanged (`diff` of the two lists empty). `ray-cpbh`'s time, 2026-10-18 00:00, predates this work, as section 0 says. None is this package's, and none was touched. `uv`'s `--no-cache` work went under
`TMPDIR`.

### 11. The final tree

`git diff aeacba8 -- runregistrykit pyproject.toml README.md PROVENANCE.md docs/releases docs/adoption docs/extraction docs/extraction-verification.md .github` is empty (`git diff --quiet`, exit 0). `git diff --cached --name-only` before committing names exactly the seven files of "What shipped". `git status --short --ignored` otherwise as at the start; `var/ledger.jsonl` unchanged; this checkout the only worktree; no commit landed on `main` after `e4bf592` while this work ran (`git log` before committing).

## The deliberate-breakage record

**(a) `end` skipped.** Applied with `git apply` in `<scratch>/clone-break` (a `git clone` of this
repository with the script copied in), run there in `pin-low`, reversed:

```diff
--- a/docs/interrupted-runs/interrupted_run_smoke.py
+++ b/docs/interrupted-runs/interrupted_run_smoke.py
@@ -736,7 +736,6 @@
     Smoke.step_5,
     Smoke.step_6,
     Smoke.step_7,
-    Smoke.step_8,
     Smoke.step_9,
     Smoke.step_10,
     Smoke.step_11,
```

Exit 1, `RESULT: FAIL (9, 10, 11, 12, 13)`, 2.7 s; no Ray process before or after; the `python`
processes the same. Whole:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
client files    from <scratch>/clone-break/docs/extraction/store_smoke_run.py
directory       $SMOKE = <scratch>/tmp/smoke-break-a/interrupted-smoke-wmi4tk24
its commands    import <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
site-packages   <scratch>/pin-low/lib/python3.12/site-packages: the package is under it

PASS step 1: a store written by the client's module, and `store create --purpose`
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id 964f6e1f58ea436fb9ecffbf855a8ddf
PASS step 2: a hard kill: a child begun on the store, heartbeating, sent SIGKILL and reaped
  started the hard-killed run's child: pid 47466
    > run smoke-02-hard-killed-20261018T181419, pid 47466
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  sent SIGKILL to pid 47466
    > reaped: returncode -9
    > status: state running, pid 47466, units_done 1, host keys ['boot', 'id'], host.id 8d2b247824882486, host.boot <36 characters>
    > liveness(status, 900): stale
PASS step 3: `list`: the hard-killed run marked `!!`, and stderr naming `end`
  $ python -m runregistrykit list   (in client/)
    exit 0
    > !! smoke-02-hard-killed-20261018T181419  running         1/?       1s  a smoke run that is hard-killed  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 stale; 0 with no host recorded.
    > !! 1 run(s) say they are running and are not: the pid does not answer kill -0, the heartbeat is older than 900 s, or this machine has rebooted since. Nothing here has killed or cleaned anything — go and look. Once you know one is over, end it with `python -m runregistrykit end RUN_ID --reason TEXT`.
PASS step 4: `store fingerprint` refused, naming the run and `end`
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    > !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181419 is running (stale, pid 47466) and names this store by its results and results_store_id. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
PASS step 5: a second `begin` on the store refused, with no run directory made
  begin(): RuntimeError: Cannot begin run smoke-05-second-20261018T181419 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181419 is running (stale, pid 47466) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
    > runs root before: ['smoke-02-hard-killed-20261018T181419']
    > runs root after:  ['smoke-02-hard-killed-20261018T181419']
PASS step 6: a live pid refused by `end`, with and without `--unverified`
  started the signalled run's child: pid 47475
    > run smoke-06-signalled-20261018T181419, pid 47475
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  $ python -m runregistrykit end smoke-06-signalled-20261018T181419 --reason the smoke run tries to end a live run   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181419: its pid 47475 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
  $ python -m runregistrykit end smoke-06-signalled-20261018T181419 --reason the smoke run tries to end a live run --unverified   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181419: its pid 47475 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
    > status: state running, ended absent, exit_code None, pid 47475
PASS step 7: a real SIGTERM: the child's handler records `killed`, 143, and exits
  sent SIGTERM to pid 47475
    > reaped: returncode 143
    > status: parses, state killed, exit_code 143
    > temporary files left: none
FAIL step 9: `end` of the hard-killed run again: refused, it has already ended
  !! expected the run lost by step 8, before it is ended again; saw running
FAIL step 10: `list`: the run `lost`, unmarked, and every run counted finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > !! smoke-02-hard-killed-20261018T181419  running         1/?       2s  a smoke run that is hard-killed  · working
    > 2 run(s) under $SMOKE/client/var/runs: 1 finished, 1 stale; 0 with no host recorded.
  !! expected the row unmarked; saw '!!'
FAIL step 11: the resume: `begin` on the store accepted, and its fingerprint recorded
  !! RuntimeError: Cannot begin run smoke-11-resumed-20261018T181420 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181419 is running (stale, pid 47466) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created (__init__.py:1119)
FAIL step 12: `store fingerprint` matching, and `store retire --dry-run`, each exiting 0
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    | !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181419 is running (stale, pid 47466) and names this store by its results and results_store_id. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
  !! exit 0 from `store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite`; saw exit 1
FAIL step 13: the resumed run's manifest `host.id` recorded, and its status's
  !! expected the resumed run of step 11; saw none: its step did not make it

children: 2 started; each reaped by its step
ray: imported, initialised: False
time: 2.7 s
left in place: <scratch>/tmp/smoke-break-a/interrupted-smoke-wmi4tk24
RESULT: FAIL (9, 10, 11, 12, 13)
```

Step 11's `begin` is refused, naming the hard-killed run and `python -m runregistrykit end`; step
12's `store fingerprint` is refused, exit 1; exit 1: as the prompt's §4.5 (a). Steps 9, 10 and 13 fail
for the same cause, the run left unended (deviation 8).

**(b) the hard-killed child not reaped before `end`.** Applied the same way:

```diff
--- a/docs/interrupted-runs/interrupted_run_smoke.py
+++ b/docs/interrupted-runs/interrupted_run_smoke.py
@@ -413,9 +413,6 @@
         )
         child.send_signal(signal.SIGKILL)
         self.say(f"  sent SIGKILL to pid {child.pid}")
-        returncode = self.reap(child)
-        self.say(f"    > reaped: returncode {returncode}")
-        self.check(returncode == -signal.SIGKILL, "returncode -9", returncode)
         status = self.status(said["id"])
         self.check(isinstance(status, dict), "a status that parses", repr(status))
         host = status.get("host")
@@ -600,6 +597,10 @@
             "ended.evidence.pid_answers false",
             evidence.get("pid_answers"),
         )
+        child = self.killed
+        returncode = self.reap(child)
+        self.say(f"    > reaped: returncode {returncode}")
+        self.check(returncode == -signal.SIGKILL, "returncode -9", returncode)
 
     def step_9(self):
         """`end` of the hard-killed run again: refused, it has already ended"""
```

Exit 1, `RESULT: FAIL (2, 3, 8, 9, 10, 11, 12, 13)`, 2.8 s; no Ray process before or after; the
`python` processes the same. Whole:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
client files    from <scratch>/clone-break/docs/extraction/store_smoke_run.py
directory       $SMOKE = <scratch>/tmp/smoke-break-b/interrupted-smoke-k9gvlluy
its commands    import <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
site-packages   <scratch>/pin-low/lib/python3.12/site-packages: the package is under it

PASS step 1: a store written by the client's module, and `store create --purpose`
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id 0e128df7e9264c8a9a9d939e1a846324
FAIL step 2: a hard kill: a child begun on the store, heartbeating, sent SIGKILL and reaped
  started the hard-killed run's child: pid 47560
    > run smoke-02-hard-killed-20261018T181422, pid 47560
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  sent SIGKILL to pid 47560
    > status: state running, pid 47560, units_done 1, host keys ['boot', 'id'], host.id 8d2b247824882486, host.boot <36 characters>
    > liveness(status, 900): alive
  !! expected liveness stale; saw alive
FAIL step 3: `list`: the hard-killed run marked `!!`, and stderr naming `end`
  $ python -m runregistrykit list   (in client/)
    exit 0
    >    smoke-02-hard-killed-20261018T181422  running         1/?       1s  a smoke run that is hard-killed  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 alive; 0 with no host recorded.
  !! expected the row marked !!; saw '  '
PASS step 4: `store fingerprint` refused, naming the run and `end`
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    > !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181422 is running (alive, pid 47560) and names this store by its results and results_store_id. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
PASS step 5: a second `begin` on the store refused, with no run directory made
  begin(): RuntimeError: Cannot begin run smoke-05-second-20261018T181423 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181422 is running (alive, pid 47560) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
    > runs root before: ['smoke-02-hard-killed-20261018T181422']
    > runs root after:  ['smoke-02-hard-killed-20261018T181422']
PASS step 6: a live pid refused by `end`, with and without `--unverified`
  started the signalled run's child: pid 47582
    > run smoke-06-signalled-20261018T181423, pid 47582
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  $ python -m runregistrykit end smoke-06-signalled-20261018T181423 --reason the smoke run tries to end a live run   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181423: its pid 47582 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
  $ python -m runregistrykit end smoke-06-signalled-20261018T181423 --reason the smoke run tries to end a live run --unverified   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181423: its pid 47582 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
    > status: state running, ended absent, exit_code None, pid 47582
PASS step 7: a real SIGTERM: the child's handler records `killed`, 143, and exits
  sent SIGTERM to pid 47582
    > reaped: returncode 143
    > status: parses, state killed, exit_code 143
    > temporary files left: none
FAIL step 8: `end` of the hard-killed run: no `--reason` refused by argparse, then the run `lost`
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181422   (in client/)
    exit 2
    > usage: runregistrykit end [-h] --reason TEXT [--unverified] [--root DIR]
    > runregistrykit end: error: the following arguments are required: --reason
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181422 --reason the smoke run's child was sent SIGKILL by the script   (in client/)
    exit 1
    | !! Cannot end smoke-02-hard-killed-20261018T181422: its pid 47560 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
  !! exit 0 from `end smoke-02-hard-killed-20261018T181422 --reason the smoke run's child was sent SIGKILL by the script`; saw exit 1
FAIL step 9: `end` of the hard-killed run again: refused, it has already ended
  !! expected the run lost by step 8, before it is ended again; saw running
FAIL step 10: `list`: the run `lost`, unmarked, and every run counted finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    >    smoke-02-hard-killed-20261018T181422  running         1/?       2s  a smoke run that is hard-killed  · working
    > 2 run(s) under $SMOKE/client/var/runs: 1 alive, 1 finished; 0 with no host recorded.
  !! expected the run lost; saw smoke-02-hard-killed-20261018T181422  running         1/?       2s  a smoke run that is hard-killed  · working
FAIL step 11: the resume: `begin` on the store accepted, and its fingerprint recorded
  !! RuntimeError: Cannot begin run smoke-11-resumed-20261018T181424 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181422 is running (alive, pid 47560) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created (__init__.py:1119)
FAIL step 12: `store fingerprint` matching, and `store retire --dry-run`, each exiting 0
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    | !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181422 is running (alive, pid 47560) and names this store by its results and results_store_id. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
  !! exit 0 from `store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite`; saw exit 1
FAIL step 13: the resumed run's manifest `host.id` recorded, and its status's
  !! expected the resumed run of step 11; saw none: its step did not make it

children: 2 started; reaped pid 47560, which had exited (returncode -9)
ray: imported, initialised: False
time: 2.8 s
left in place: <scratch>/tmp/smoke-break-b/interrupted-smoke-k9gvlluy
RESULT: FAIL (2, 3, 8, 9, 10, 11, 12, 13)
```

Before the reap, **`liveness` gives `alive`** (step 2) and **`list`'s row is unmarked, `running`**,
the summary `1 alive; 0 with no host recorded.` and no stale line (step 3). Step 8's `end` is refused,
"answers kill -0 … (a zombie) answers kill -0 too", and the step stops before the moved reap, so the
`finally` reaps the child: "reaped pid …, which had exited (returncode -9)". Steps 9–13 fail because
the run was never ended. Steps 4 and 5 pass: each refusal counts the run as in use and names `end`
whatever its liveness. As section 0's correction 8 reads the prompt's §4.5 (b); every failure has
one of its two causes.

**(c) the core-only venv.** `TMPDIR=<scratch>/tmp/smoke-core <scratch>/pin-core/bin/python
docs/interrupted-runs/interrupted_run_smoke.py`: exit 1, `RESULT: FAIL (1, 11, 12)`, 2.3 s, wall 2.45
s; no Ray process before or after; the `python` processes the same; `ray: not imported`. Whole:

```text
python          3.12.15 (<scratch>/pin-core/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-core/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    not installed
ray             not installed
sqlalchemy      not installed
client files    from /Users/ds283/Documents/Code/RunRegistryKit/docs/extraction/store_smoke_run.py
directory       $SMOKE = <scratch>/tmp/smoke-core/interrupted-smoke-hcuad06i
its commands    import <scratch>/pin-core/lib/python3.12/site-packages/runregistrykit/__init__.py
site-packages   <scratch>/pin-core/lib/python3.12/site-packages: the package is under it

FAIL step 1: a store written by the client's module, and `store create --purpose`
  !! ModuleNotFoundError: No module named 'sqlalchemy' (smoke_registry.py:7)
PASS step 2: a hard kill: a child begun on the store, heartbeating, sent SIGKILL and reaped
  started the hard-killed run's child: pid 47191
    > run smoke-02-hard-killed-20261018T181358, pid 47191
    > its runregistrykit: <scratch>/pin-core/lib/python3.12/site-packages/runregistrykit/__init__.py
  sent SIGKILL to pid 47191
    > reaped: returncode -9
    > status: state running, pid 47191, units_done 1, host keys ['boot', 'id'], host.id 8d2b247824882486, host.boot <36 characters>
    > liveness(status, 900): stale
PASS step 3: `list`: the hard-killed run marked `!!`, and stderr naming `end`
  $ python -m runregistrykit list   (in client/)
    exit 0
    > !! smoke-02-hard-killed-20261018T181358  running         1/?       0s  a smoke run that is hard-killed  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 stale; 0 with no host recorded.
    > !! 1 run(s) say they are running and are not: the pid does not answer kill -0, the heartbeat is older than 900 s, or this machine has rebooted since. Nothing here has killed or cleaned anything — go and look. Once you know one is over, end it with `python -m runregistrykit end RUN_ID --reason TEXT`.
PASS step 4: `store fingerprint` refused, naming the run and `end`
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    > !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181358 is running (stale, pid 47191) and names this store by its results. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
PASS step 5: a second `begin` on the store refused, with no run directory made
  begin(): RuntimeError: Cannot begin run smoke-05-second-20261018T181358 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181358 is running (stale, pid 47191) and names this store by its results. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
    > runs root before: ['smoke-02-hard-killed-20261018T181358']
    > runs root after:  ['smoke-02-hard-killed-20261018T181358']
PASS step 6: a live pid refused by `end`, with and without `--unverified`
  started the signalled run's child: pid 47200
    > run smoke-06-signalled-20261018T181358, pid 47200
    > its runregistrykit: <scratch>/pin-core/lib/python3.12/site-packages/runregistrykit/__init__.py
  $ python -m runregistrykit end smoke-06-signalled-20261018T181358 --reason the smoke run tries to end a live run   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181358: its pid 47200 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
  $ python -m runregistrykit end smoke-06-signalled-20261018T181358 --reason the smoke run tries to end a live run --unverified   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181358: its pid 47200 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
    > status: state running, ended absent, exit_code None, pid 47200
PASS step 7: a real SIGTERM: the child's handler records `killed`, 143, and exits
  sent SIGTERM to pid 47200
    > reaped: returncode 143
    > status: parses, state killed, exit_code 143
    > temporary files left: none
PASS step 8: `end` of the hard-killed run: no `--reason` refused by argparse, then the run `lost`
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181358   (in client/)
    exit 2
    > usage: runregistrykit end [-h] --reason TEXT [--unverified] [--root DIR]
    > runregistrykit end: error: the following arguments are required: --reason
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181358 --reason the smoke run's child was sent SIGKILL by the script   (in client/)
    exit 0
    > >> end: smoke-02-hard-killed-20261018T181358 is now lost, verified: its pid 47191 does not answer kill -0 on this host
    > status: state lost, exit_code None, ended.verified True, ended.evidence.pid_answers False, ended.reason "the smoke run's child was sent SIGKILL by the script"
PASS step 9: `end` of the hard-killed run again: refused, it has already ended
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181358 --reason the smoke run ends it twice   (in client/)
    exit 1
    > !! Cannot end smoke-02-hard-killed-20261018T181358: its status says it has already ended, as 'lost'; end records only a run whose end the registry never saw. Nothing was written
PASS step 10: `list`: the run `lost`, unmarked, and every run counted finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    >    smoke-02-hard-killed-20261018T181358  lost            1/?       2s  a smoke run that is hard-killed  · working
    > 2 run(s) under $SMOKE/client/var/runs: 2 finished; 0 with no host recorded.
FAIL step 11: the resume: `begin` on the store accepted, and its fingerprint recorded
  begin(): smoke-11-resumed-20261018T181359
    > status: state done, exit_code 0, fingerprint_sidecar None
    > fingerprint_error: ConfigError: $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:FINGERPRINTER': the module 'smoke_registry' could not be imported (ModuleNotFoundError: No module named 'sqlalchemy')
    > digest: None
  !! expected no fingerprint_error; saw ConfigError: $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:FINGERPRINTER': the module 'smoke_registry' could not be imported (ModuleNotFoundError: No module named 'sqlalchemy')
FAIL step 12: `store fingerprint` matching, and `store retire --dry-run`, each exiting 0
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    | !! $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:FINGERPRINTER': the module 'smoke_registry' could not be imported (ModuleNotFoundError: No module named 'sqlalchemy')
  !! exit 0 from `store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite`; saw exit 1
PASS step 13: the resumed run's manifest `host.id` recorded, and its status's
    > manifest host.id 8d2b247824882486, status host.id 8d2b247824882486

children: 2 started; each reaped by its step
ray: not imported
time: 2.3 s
left in place: <scratch>/tmp/smoke-core/interrupted-smoke-hcuad06i
RESULT: FAIL (1, 11, 12)
```

Step by step: 1 needs the client's module (`write_store`) and fails on `No module named 'sqlalchemy'`;
2–10 need none of it (`begin` reads an absent sidecar, `list` and `end` are the core, the in-use
check precedes the fingerprinter) and pass; 11 needs the fingerprinter and records the loader's
`ConfigError` as `fingerprint_error`; 12's `store fingerprint` loads it and exits 1; 13 reads the
manifest and status only and passes (deviation 9).

## Observations not acted on

1. **The extraction's smoke run fails its step 3 at `v0.2.0`**, on `list`'s summary clause (§5). As
   the prompt's §1.2 says, nothing is wrong at either tag, and the script is not changed; the
   document records it in §5.2 and §10. Not opened; the review or the user may judge otherwise.
2. **In the core form, the whole hard-kill route works** (breakage (c)): `begin`'s refusal, `end` and
   the resume need no `[stores]`, only the fingerprint does. The README and adoption notes say what
   the core form is; neither says this, and neither needs to.
3. **The script's step 4 and step 5 cannot tell a stale run from an alive one**: both refusals name
   `end` in a sentence that applies to a stale run whatever the liveness of the runs they describe.
   It is the package's wording (`stores.py:1405-1415`, `__init__.py:1119-1126`), and the script's
   steps 2 and 3 check the liveness.

## State handed to the next prompt

- **The campaign is closed.** There is no next prompt. After the close, a gate (G1–G3) is recorded on
  the board when it holds, in a records commit of its own (board §2, README §7).
- **The six open issues** stay on this board's §3, each owner none, each with a dated line: open at
  the close. A later campaign takes any of them over with an **Assigned** line, as the index's rule
  says.
- **For a client's adoption**: the pin installs from GitHub at both ends, and
  `docs/interrupted-runs/interrupted_run_smoke.py` runs against it; a client can run it in its own
  venv to see the route its adoption notes describe.
- **For the orchestrator**: "this commit" in this log, the board, the campaign README,
  `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` and the document stands for 07's commit's SHA.
- The suite is 410, with one skip on macOS.
