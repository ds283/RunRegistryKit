# Campaign — interrupted-runs

**Written:** 2026-10-16 by Claude Opus 5.5, at the user's request, from the five issues on the
[`inherited-issues`](../inherited-issues/IMPLEMENTATION_STATE.md) board that bear on a long job that
may be interrupted, and from measurements made the same day (§0.2). SGK's stale-run brief
(`prompts/handover/runregistrykit-stale-run-brief.md`, committed in SGK `79434bf`) is evidence, not
a specification. The board holds each issue in full; this plan does not repeat them. The user took
the machine decision, L1–L4, on 2026-10-16, as recommended (§6.2). **Prompt 01 has landed and
been reviewed** ([`01-the-host.md`](01-the-host.md), `387c58f`). The user took L5 on 2026-10-17,
refined (§6.2), and **prompt 02 has landed and been reviewed**
([`02-status-writes.md`](02-status-writes.md), `2bf9c72`). Its review opened two issues in the
writer's bookkeeping; the user asked on 2026-10-17 for both to be fixed at the earliest sensible
opportunity, and **prompt 02b has landed and been reviewed** for them
([`02b-the-writers-bookkeeping.md`](02b-the-writers-bookkeeping.md), `2959b78`), ahead of 03. Its
review opened one issue, on 3.13, and **prompt 02c has landed and been reviewed** for it
([`02c-the-writers-lock.md`](02c-the-writers-lock.md), `35ce264`), under L11 (a). The user took L6 on
2026-10-18, refined (§6.2), and **prompt 03 has landed and been reviewed**
([`03-an-unreadable-status-is-in-use.md`](03-an-unreadable-status-is-in-use.md), `ab0cad9`). The user took L7
and L8 on 2026-10-18, each as (a) (§6.2), and **prompt 04 has landed and been reviewed**
([`04-end-a-run.md`](04-end-a-run.md), `5e20772`). The user took L9 on 2026-10-18, as (a), and asked
for `[04-a-pid-out-of-range-makes-pid-alive-raise]` to be fixed with it, and **prompt 05 has landed and been reviewed**
([`05-begin-refuses-a-second-writer.md`](05-begin-refuses-a-second-writer.md), `eb68583`). The user took
L10 on 2026-10-18, as (a), and **prompt 06 has landed and been reviewed**
([`06-release-v0.2.0.md`](06-release-v0.2.0.md), `0bae3a3`), CI green (run `39143681701`), and **`v0.2.0` is tagged** on it (tag object `895e3c7`).
The last is written after it (§2.1).

## 0. Why this campaign exists

A registry run is the record that a long job exists. SGK is about to launch a ~36-hour Ray build of
one store under `runregistrykit` 0.1.0, which may be interrupted and resumed. SGK has rehearsed an
interruption by `SIGTERM`, end to end. Reading the package against an interruption it did *not*
rehearse, and against the issues already on the inherited board, finds five that each change how
an interrupted run is recorded or what a person can then do:

| Issue | What goes wrong |
|---|---|
| `[04-runs-do-not-say-which-machine-produced-them]` | A run's pid is judged against this machine's process table, whichever machine the run was on, and a reboot can hand its pid to a new process |
| `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` | A signal inside a heartbeat write can leave `status.json` unparseable, or put a finished run back to `running` |
| `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` | A run whose `status.json` cannot be read is not counted as in use, so its store can be retired under it |
| `[a3-v2-a-hard-killed-run-blocks-its-store]` | A hard-killed run stays `running` for ever and blocks its store; the named remedy has no command and checks nothing |
| `[00-begin-does-not-refuse-a-second-writer]` | `begin` does not look for a run already on its store |

They share one design. Three of them judge, or would judge, another run's liveness by its pid,
which is evidence only on that pid's machine and only while the pid has not been reused. Two are a
cause and its consequence. So they are taken together, the machine decision first.

**What does not change.** The registry records; it does not schedule, supervise, restart or lock.
**It does not decide that a run is dead.** Where a run's end was never recorded, a person decides,
and the package checks the evidence and records the decision (SGK's option 1, brief §1). The one
thing the package newly *concludes* is narrow and is not a judgement: a pid recorded before this
machine last booted belongs to a process that no longer exists (§6.2, L3).

### 0.1 What changes in what the registry writes

This campaign changes the interface (`CLAUDE.md`, "Releases"), on purpose and in named prompts.
The planned changes are as follows, the forms to be fixed by the decisions in §6.2:

- the manifest and `status.json` gain a `host` record (01, L1–L3);
- `liveness` gains a value for a run on another machine, and `list` reports it (01, L4);
- `status.json` is written through a temporary name of its own (02, L5);
- `status.json` may record a run ended by a person: a terminal state and an `ended` record (04,
  L7).

No reader of an older form is added. A record without `host` has a meaning in the current form
(L4), so every existing run directory reads as it does today.

### 0.2 Measurements taken by the planner (2026-10-16)

Taken at `79015a7` (the package lines are `v0.1.0`'s; `git diff --stat v0.1.0 79015a7 --
runregistrykit pyproject.toml` is empty), on macOS 27 (`arm64`), Python 3.12 from `venv/`. SGK was
read through `git` at `79434bf`, and nothing in it was run.

**The five defects, measured by a scratch probe** (not committed) on the suite's own fixtures in a
`tempfile` directory. The board's entries give each result in full. In short:
- a child process that called `begin` and `heartbeat` was sent `SIGKILL`. Its `status.json` was
  unchanged and stayed `running`/`stale`, and fingerprint, retire and copy refused its store, as
  did a resumed run's `finish(fingerprint=True)`;
- a second `begin` on a live run's store returned a run;
- with a live run's `status.json` cut in half, fingerprint, retire and copy proceeded, and a real
  `retire_store` deleted the store's primary and four shards under it.

**The heartbeat race is wider than its recorded next step.** Read, not measured. `Run._update`
(`runregistrykit/__init__.py:398`) reads the status, writes it through `<path>.tmp` and replaces.
If a signal handler calls `finish` while a heartbeat is inside `json.dump`:
- *with the fixed name*, the two writes share one temporary file;
- *with a unique name per write*, the board's recorded next step, `finish`'s write lands, and if
  the handler then **returns**, the heartbeat's `os.replace` lands after it with the payload it
  read before `finish`. The terminal state is lost exactly as before.

So the unique name fixes the unparseable file and not the lost state. 02 needs both (L5); the moved
entry says so.

**Identifying a machine and a boot, on macOS, from the standard library.** The core may import only
the standard library, `ctypes` and `subprocess` among it.

| What | How | Cost | Note |
|---|---|---|---|
| host UUID | `gethostuuid(3)` through `ctypes` | 31 µs | equals `IOPlatformUUID` from `ioreg` (29 ms by subprocess); stable across reboots and networks; a hardware identifier, so not to be written raw |
| boot session | `sysctlbyname("kern.bootsessionuuid")` through `ctypes` | 51 µs | a UUID, new each boot; `sysctl -n` by subprocess, 30 ms |
| boot time | `sysctl -n kern.boottime` | 7.5 ms | seconds and microseconds |
| process start | `ps -o lstart= -p PID` | one subprocess per pid | to the second |
| `platform.node()` | | | here, a DNS name the network assigned, not the machine's own `LocalHostName` (`scutil`); it changes with the network, as the board's machine entry warned |

`kern.uuid` is the kernel's UUID, the same on every machine running one kernel build, and is not a
machine identity. On Linux the counterparts are `/etc/machine-id` and
`/proc/sys/kernel/random/boot_id`. **Linux is not measured**, and nor are containers, where
`/etc/machine-id` can be shared by every container made from one image. Where the clients' long jobs
run is the user's to say (L1).

**How SGK uses what changes**, read at SGK `79434bf`:
- SGK's drivers are `docs/gktk-remedial/scoped_pipeline_run.py` (`begin` at `:544`) and
  `docs/handover/quadsource_atol_sweep.py` (`:556`, `:869`).
- Their signal handlers call `run.finish("killed", exit_code=128 + signum)` (`:398`, `:563`,
  `:575`, `:894`).
- The pipeline's heartbeat comes from its stdout tee (`_observe`, `scoped_pipeline_run.py:253`).
  Its handler can therefore interrupt a heartbeat.
- SGK asserts that every state its driver returns is in `runregistrykit.TERMINAL_STATES`
  (`RunDrivers/tests/test_pipeline_adoption.py:252`). Adding a state keeps that passing; removing
  or renaming one would not.
- No SGK caller is known to begin two runs on one store at once. 05 re-measures this at writing.
- CPBH and SI call nothing of the registry yet (extraction 07's checklists).

## 1. Scope

**In scope:**
- the machine and the boot a run is on, recorded and used by `liveness` and `list` (01);
- `status.json` writes that neither corrupt the file nor lose a terminal state under a signal (02,
  02b), nor leave the writer's lock held (02c);
- the store operations' in-use check made to refuse when a run's status cannot be read (03);
- a person-run command that records an unrecorded end as terminal, after checking the evidence
  (04);
- `begin` refusing a store that a `running` run names (05);
- the release `v0.2.0`, its notes on what the registry now writes, and adoption notes for the three
  clients (06);
- a verification document, and the campaign closed (07).

**Out of scope:**
- **any edit to SGK, CPBH, SI, DatastoreKit or RayPoolKit.** Each client adopts `v0.2.0` in a
  campaign of its own. SGK's A3 v2 runs on `v0.1.0` and does not wait for this campaign (SGK's
  brief §2);
- **signal handling in the package.** It has none (`git grep -n 'SIGTERM\|signal\.' --
  runregistrykit` is empty) and gains none: 02 makes `status.json` writes safe *under* a client's
  handler, and does not install one;
- **the registry deciding that a run is dead**, killing, reaping, restarting or locking. 05's
  refusal is a check at `begin`, as the store operations' is, and not a lock;
- **the other three inherited issues** (`copy`'s carried fields, the cross-filesystem move advice,
  the closed pipe). They stay on the inherited board.

## 2. Prompts

| # | Prompt | Covers | Model | Status |
|---|---|---|---|---|
| 01 | [`01-the-host.md`](01-the-host.md) | `[04-runs-do-not-say-which-machine-produced-them]`, under L1–L4: a host identity and a boot identity read from the standard library, recorded in the manifest and `status.json` by `begin`, kept by every later write. `liveness` answers for a run on another machine without testing its pid, and calls a run on this machine `stale` when its boot is not this one; `list` shows both, and counts records with no host. The store operations' refusal names a run on another machine as such. Tests: a record from another host, from an earlier boot, and with no host; the identity functions on this platform, and their absence handled. **Acceptance:** every existing test passes unchanged in what it asserts; a record from another host is never judged by `kill -0`; a record with no `host` is judged as today and counted. | Opus | landed and reviewed 2026-10-16, `387c58f`; CI green (run `38911075984`) |
| 02 | [`02-status-writes.md`](02-status-writes.md) | `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`, under L5 as refined: `status.json` written through a temporary name of its own, with the mode the fixed name gave, and a write superseded by a later write to the same `status.json` from the same process discarded, whichever `Run` made it, the later write keeping the earlier one's fields, so a terminal state is never replaced by the payload a heartbeat read before it. Sidecar writes keep `<path>.tmp` and their leftover checks. **Acceptance:** the reproduction the board names, a heartbeat whose `json.dump` makes a `finish` from inside it, run once raising and once returning, leaves a parseable `status.json` with the terminal state both times. *At writing (2026-10-17, `c2911d3`), measured by a probe with a real signal: today a raising handler can leave `running`, or `killed` with `exit_code` `null`; a returning one leaves `running` and a `FileNotFoundError` in the caller; one that ends the process survives. A unique name alone still loses the state when the handler returns.* | Opus | landed and reviewed 2026-10-17, `2bf9c72`; CI green (run `39049728089`); two issues opened by the review |
| 02b | [`02b-the-writers-bookkeeping.md`](02b-the-writers-bookkeeping.md) | `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]` and `[02-the-landed-record-is-unpinned-and-can-move-backwards]`, opened by 02's review, under L5 as amended 2026-10-17: a re-entered write re-applies only the in-flight writes newer than the payload it composes from; the record of what landed never lowered, whatever instruction a handler interrupts. Tests: both measured cases; a put-back followed by a later re-entered write; and a sweep that runs a handler at every instruction the writer executes (`sys.monitoring`), for an interrupted heartbeat and an interrupted `finish`, the handler returning or raising. **Acceptance:** both sweeps keep the terminal state at every instruction where it is the later write; 02's 15 tests unchanged. *At writing (2026-10-17, `91e8e9c`): against `2bf9c72` the heartbeat sweep finds 15 of 202 instructions where a later re-entered write puts `running` back, line 318's check through `:321`'s `copy.deepcopy`, which is pure Python and so reachable by a real signal; the `finish` sweep, 43, 7, 178 and 157 in its four modes. A candidate of the design found none in the heartbeat sweep and only the points where the handler's write is the earlier in the `finish` sweep.* | Opus | landed and reviewed 2026-10-17, `2959b78`; CI green (run `39060913296`); one issue opened by the review |
| 02c | [`02c-the-writers-lock.md`](02c-the-writers-lock.md) | `[02b-a-raising-handler-can-leave-the-status-lock-held]`, opened by 02b's review, under L11: the writer's two filters (`:365`, `:372`), list comprehensions that CPython inlines, made generator expressions, whose exception tables are complete at 3.12 and 3.13, so a handler that raises inside a write never leaves `_STATUS_LOCK` held or an in-flight entry kept; the `with` point at 3.14 as L11 says. Test: a sweep, in a child, that runs a raising handler at every `JUMP_BACKWARD` of the writer for a plain, a re-entered and a twice re-entered heartbeat, and asserts after each that the lock is free and no in-flight entry is left. **Acceptance:** the sweep passes at 3.12, 3.13 and 3.14, and fails against `2959b78`; a real signal leaves the lock held at 3.12 and 3.13 nowhere; every existing test and 02b's sweeps unchanged. *At writing (2026-10-17, `9d26357`): a real signal, 45 s per row, left the lock held 5 times at 3.13.16 at `:365`'s jump, 0 at 3.12.15, and 30 at 3.14.8 (24 at the `with`). 3.12 inlines the comprehension too, with the same gap. A `for` loop with an `if` has it as well (4 at 3.13). The generator expressions: 0 at 3.12 and 3.13, 0 in 232 531 interruptions at 3.13 over 360 s, and only the `with` at 3.14. A bare `with` over an `RLock`, with no registry code, leaves it held at 3.14.8 and not before.* | Opus | landed and reviewed 2026-10-17 (`35ce264`; [log](logs/02c-the-writers-lock.md)); CI green (run `39072902589`); L11 taken 2026-10-17, (a), the issue narrowed to 3.14 |
| 03 | [`03-an-unreadable-status-is-in-use.md`](03-an-unreadable-status-is-in-use.md) | `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`, under L6 as taken 2026-10-18, refined: a run whose manifest names the store is counted as in use by copy, move, fingerprint, retire and amend unless its status says a terminal state (a status that cannot be read, or that names no state the registry writes, is in use as a `running` one is), and refused in words that say the registry cannot tell whether it is running; `list` marks such a run `!!`; a status or manifest that is JSON but not an object is read as unreadable, so `list_runs`, `liveness` and the writer never raise on one, and `Run.finish` ends the run. **Acceptance:** the planner's probe as a test: for each of thirteen forms of `status.json`, each operation refuses, and the store is untouched. *At writing (2026-10-18, `0c75dd3`), with a live run on a full store: in 10 of 13 forms all six operations proceeded and `list` showed no marker; in the other 3 (`[1]`, `"x"`, `5`) `list_runs` raised `AttributeError`, so `list` and every store operation under the runs root raised, and `Run.finish` raised on the same files. A live run whose manifest is torn or missing names no store, and its store's operations proceed: opened as `[03-a-run-whose-manifest-cannot-be-read-names-no-store]`, not this prompt's.* | Sonnet | landed and reviewed 2026-10-18 (`ab0cad9`; [log](logs/03-an-unreadable-status-is-in-use.md)); CI green (run `39083674030`); one issue opened by the review |
| 04 | [`04-end-a-run.md`](04-end-a-run.md) | `[a3-v2-a-hard-killed-run-blocks-its-store]`, under L7 and L8 as taken 2026-10-18, each (a): `python -m runregistrykit end RUN_ID --reason TEXT [--unverified]`, which records a run as ended, in the new terminal state `lost` with exit code `null` and an `ended` record (who, when, why, `git_head`, host, whether verified, the evidence), when the evidence on this machine says it is over: a boot other than this one, or a pid that does not answer `kill -0`. A live pid here is refused with no override; a run on another host, or whose status does not say, only with `--unverified`; a run already terminal always. The store operations' refusals and two of `list`'s lines name it in place of `Run.finish`, nine existing assertions changing their fragment; `Run.finish`'s code unchanged. **Acceptance:** a child process begun on a store and sent `SIGKILL`, then `end`, then every store operation and a resumed run's fingerprint succeeding; `end` refused for a live pid, for a run on another host, and for a run already terminal. *At writing (2026-10-18, `9e38581`): a child begun on a full store and `SIGKILL`'d left `status.json` byte-identical and `running`, `stale` once reaped; all six operations refused, naming `Run.finish`; a resumed run's fingerprint was refused; there is no `end` command; `Run.finish` ended a live run's record as readily as the dead one's. Before it is reaped, a killed child answers `kill -0` and is called `alive`: opened as `[04-a-killed-process-not-yet-reaped-answers-kill-0]`, not this prompt's.* | Opus | landed and reviewed 2026-10-18 (`5e20772`; [log](logs/04-end-a-run.md)); CI green (run `39122974980`); one issue closed, one opened by the work |
| 05 | [`05-begin-refuses-a-second-writer.md`](05-begin-refuses-a-second-writer.md) | `[00-begin-does-not-refuse-a-second-writer]`, under L9 as taken 2026-10-18, (a), and `[04-a-pid-out-of-range-makes-pid-alive-raise]`, at the user's request the same day: `begin` refuses, after the tombstone check and before creating the run directory, when any run under its runs root that has not finished names its `results` store, by path or `results_store_id` (the store operations' rule, `_running_runs_naming`), in words naming `end` for a stale one, with 04's sentences for a run on another host and a status that does not say; no override, and not a lock. `pid_alive` returns false for a pid outside the platform's range instead of raising. Six existing tests that build two unfinished runs on one store through `begin` change their setup, through one new fixture, and none of their assertions. **Acceptance:** a second `begin` on a live run's store, a stale run's store, a `foreign` run's store and a store named by an unreadable status, each refused with no run directory left; a store whose runs are all terminal accepted; a hard-killed run ended, then `begin` accepted and its fingerprint recorded. *At writing (2026-10-18, `d8f8de4`): today a second `begin` is begun on a store whatever its earlier run is; a candidate of the check refused alive, stale, `foreign`, torn and `"paused"` runs with no directory left, accepted all-terminal stores, and made six existing tests error at a refused `begin`, none of them testing `begin`; with it, one `pid` of `2**31` under the runs root made every `begin` with `results` raise. SGK begins at most one run per store per process.* | Sonnet | landed and reviewed 2026-10-18 (`eb68583`; [log](logs/05-begin-refuses-a-second-writer.md); suite 378 → 410); CI green (run `39129061916`); two issues closed |
| 06 | [`06-release-v0.2.0.md`](06-release-v0.2.0.md) | `pyproject.toml` at `0.2.0`; the README's rules and usage for the host, `end` and the new refusals; release notes saying field by field what the registry now writes and what an older record means; an adoption note per client in `docs/adoption/`. CI green, then **tag `v0.2.0`** (L10). *At writing (2026-10-18, `80974e2`): against `v0.1.0`, the manifest and `status.json` each gain `host`, and `end`'s status holds `lost`, `exit_code` `null` and `ended`; a ledger line, the sidecar and the run directory's files are unchanged in shape; the public names gain `this_host`, `TERMINAL_STATES` gains `lost` and `liveness` the keyword `here=`, the command line `end`. `v0.1.0` reading records written now judges a `foreign` run and one from an earlier boot by `kill -0` here and calls a `lost` run `unknown`. The README is untrue or silent in eight places; no release notes exist; a `0.2.0` wheel from an export has ten entries and no test module. SGK is on `v0.1.0`; CPBH and SI use nothing of the registry.* | Opus | landed and reviewed 2026-10-18 (`0bae3a3`; [log](logs/06-release-v0.2.0.md); suite 410 → 410); CI green (run `39143681701`); `v0.2.0` tagged, tag object `895e3c7`; one issue opened by the review |
| 07 | `07-verification-and-close-out.md` | `docs/interrupted-runs-verification.md`, from the package at `v0.2.0` and the logs; a smoke run against the pin installed from GitHub that hard-kills a run, ends it, resumes on its store and fingerprints it; the campaign closed. | Opus | not written |

**Order.** 01 → 02 → 02b → 02c → 03 → 04 → 05 → 06 → 07.
- 01 is first because 04's and 05's guards judge a run's liveness by its pid, and they mean what
  they say only once the host and boot are recorded.
- 02 precedes 03 so that the known cause of an unreadable status is gone before the check that
  catches every cause is changed.
- 02b follows 02 at once, at the user's request (2026-10-17): it fixes 02's writer while it is the
  last thing changed, and 03 touches no part of it.
- 02c follows 02b at once, for the issue 02b's review opened (2026-10-17), on the same grounds.
- 04 follows 01 and 03 because `end` handles a run on another host and a run with an unreadable
  status.
- 05 follows 04 because its refusal of a stale run names `end` as the remedy.

### 2.1 When each prompt file is written

One at a time, each after the one before it has landed and been reviewed, against the tree it left,
as the extraction campaign's were. The charters above fix each prompt's task now; holding the file
back holds back only its method. **01 is written once the user has taken L1–L4.** Each prompt's file
records what it found at writing in its row above, in italics.

## 3. Datastores

**No prompt opens a client's store**, and no client code is imported or run. The suite builds every
store it needs in a `tempfile` directory through the carried fixtures and the neutral store. Every
test that hard-kills a process kills a child the test started, and nothing else.

## 4. The interfaces between prompts

- **After 01:** `host` in the manifest and in `status.json`; the identity functions, public if L2
  says so; the liveness value for another host. 03, 04 and 05 use them.
- **After 02:** `Run._update`'s supersession rule; `write_json_atomic` either unchanged or changed
  in a way the release notes state.
- **After 02b:** the supersession rule with its amended merge and a record of what landed that is
  never lowered, and the instruction sweep that pins both.
- **After 02c:** the writer's filters as generator expressions, and a sweep at every
  `JUMP_BACKWARD` of the writer that asserts the lock free and no in-flight entry after a raising
  handler; the 3.14 `with` point as L11 decides.
- **After 03:** the in-use check's rule for an unreadable status, used by 05's `begin` check.
- **After 04:** the `end` command, its record in `status.json`, and the state it writes; the
  refusal texts that name it, which 05 reuses.
- **After 06:** `v0.2.0`, its release notes and the adoption notes, which 07 cites.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus `docs/OPEN_ISSUES.md`
   and `prompts/INDEX.md`.
4. **Do not fix things the prompt did not ask for.** Record them, with a §3 issue.
5. **No prompt edits a client, DatastoreKit or RayPoolKit.** Reading them through `git` is allowed.
   Running a client's code or tests is not.
6. **No test needs a Ray cluster, imports a client, or creates anything outside a `tempfile`
   directory.** A test may start a child process and signal it, and nothing else. The suite count
   is recorded before and after each prompt; a count that falls is a stop.
7. **What the registry writes is an interface.** Only the changes in §0.1 are planned, each by the
   prompt named there, in the form its decision fixes. Any other change to the manifest,
   `status.json`, `checkpoint.jsonl` or a sidecar is a stop.
8. **An existing record reads as before.** Every prompt that changes what is written adds a test
   that a record written by `v0.1.0`'s code (built in the test, not read from a client) is read and
   judged as `v0.1.0` judged it, except where its decision says otherwise.
9. **The registry does not decide that a run is dead** (§0). A prompt whose design would have the
   package end, skip or override a run without a person's command is a stop.
10. **Deliberate breakage.** Each prompt that adds code or a test names mutations its tests must
    catch. The log records each as a diff, exactly as applied, so the orchestrator can replay it
    with `git apply`. Mutations are never committed.
11. **No tag except where a prompt says so** (06: `v0.2.0`), made on the prompt's commit once CI is
    green there; none is moved or deleted.

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified;
- **Verification performed**: the suite count before and after;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Made already, and not reopened here

| | Decided |
|---|---|
| **The boundary** | The registry records; it does not schedule, supervise, restart or lock, and it does not decide that a run is dead (`CLAUDE.md`; `runregistrykit/stores.py:1031-1032`). SGK does not ask to weaken it (its brief §0) |
| **The interface rule** | What the registry writes is an interface, changed only by a prompt that says so, and no reader of an older form is added (`CLAUDE.md`, "Releases") |
| **SGK's launch** | A3 v2 runs on `v0.1.0`; no release is asked for before it (SGK's brief §2) |

### 6.2 Decisions this campaign needs

Each is put with a recommendation, the recommended option first. L1–L4 were needed before 01 was
written, and **the user took them on 2026-10-16, each as recommended**; the recommendation below is
the decision. The others are put when the prompt that needs them is written.

- **L1: what identifies a machine** *(for 01)*.
  (a) **The OS's own machine identity, as a digest**: macOS `gethostuuid(3)`, Linux
  `/etc/machine-id`, each hashed with a fixed prefix and truncated (for example 16 hex characters),
  so that no hardware identifier is written raw. A display name beside it, `platform.node()` by
  default and overridable by an environment variable, used only for reading, never for judging.
  (b) A name a person sets, from an environment variable or a per-machine file outside the client's
  committed `runregistrykit.toml`, with no record when it is unset. (c) `platform.node()`.
  *Recommended:* (a). It needs nothing from a person, survives renaming and the network, and costs
  31 µs here. (c) changed with the network on the planner's machine. (b) leaves the field empty
  wherever nobody set it. **To be answered by the user with it:** where the long jobs run: this
  Mac, another Mac, a Linux machine, a cluster, a container. Linux and containers are not measured,
  and a container's `/etc/machine-id` may not be its own; a platform with no identity records
  `null`, which L4 gives a meaning. *Taken 2026-10-16: (a). Where the jobs run, the user decides per
  job, by what each machine is doing: often a Mac Studio, not always. So the package does not choose
  a platform. It reads an identity wherever the platform offers one (macOS, measured here; Linux,
  from its documented files, run in CI on `ubuntu-24.04`) and records `null` elsewhere. Runs on more
  than one Mac make `foreign` records real from the start.*
- **L2: where the host is recorded** *(for 01)*.
  (a) **Both**: `status.json` gains `host: {id, boot}`, beside the pid it qualifies, written by
  `begin` and carried by every later write. The manifest gains `host: {id, name, machine, system,
  release, python}` for provenance, answering the board's point that rows computed on different
  hardware can differ in their last bits. (b) `status.json` only. *Recommended:* (a). The pid
  `liveness` tests lives in `status.json`, so the identity used for judging must too. The
  manifest is the record of what ran, and is written once. Whether the identity functions are
  public names is decided with 01's file. *Taken 2026-10-16: (a).
  01's file makes one public name, `this_host()`.*
- **L3: what identifies a boot, and what the package concludes from it** *(for 01)*.
  (a) **The boot session identifier** (macOS `kern.bootsessionuuid`, Linux `boot_id`), recorded
  in `status.json`'s `host`. On this host, a `running` run whose boot is not the current one is
  `stale` without asking `kill -0`, since its pid cannot name a process of this boot. That settles
  the reboot case of pid reuse. (b) As (a), and the process's start time beside the pid, so a pid
  reused within one boot is told apart as well. (c) Neither. *Recommended:* (a). A reboot is the
  common cause both of a run ending unrecorded and of pid reuse. Reuse within one boot needs the
  pid space to wrap during the run. A start time costs a subprocess per pid on macOS, and differs
  in form between platforms. If (b) is wanted later, it is an addition to the same record.
  *Taken 2026-10-16: (a).*
- **L4: what `liveness` and `list` say** *(for 01)*.
  (a) **A new liveness value, `foreign`**, for a `running` run whose `host.id` is not this one's.
  It is not judged: its pid is not tested and its heartbeat age is shown, not weighed. `list`
  marks it and counts it apart, and the store operations still count it as in use, naming its
  host. **A record with no `host`**, or whose `id` is `null` (every record written before 01, or
  on a platform with no identity), is judged here as today, and `list` counts it as "host not
  recorded". (b) Refuse to judge a record with no `host`. *Recommended:* (a). Every existing
  record has no `host`, and (b) would turn every `running` one into `foreign`. That includes SGK's
  A3 v2 if it is hard-killed while still on `v0.1.0`, which then needs `end` (04) on the machine
  that ran it. Adding a value to `liveness` changes the public function's output, and the release
  notes say so. *Taken 2026-10-16: (a).*
- **L5: how `status.json` is written** *(for 02)*.
  (a) **A unique temporary name in the same directory for `status.json` only**, with the mode the
  fixed name gave (`0666` less the umask, not `mkstemp`'s `0600`). And **a superseded write
  discarded**: each `Run._update` takes a sequence number, and one that finds a later write from
  the same `Run` landed while it was writing removes its temporary file instead of replacing.
  `write_json_atomic` keeps `<path>.tmp` for every other caller, sidecars included. (b) The unique
  name alone, the board's recorded next step. It does not keep a terminal state when the handler
  returns (§0.2). *Recommended:* (a). *Taken 2026-10-17: (a), refined, as 02's file states it. The
  supersession is kept per `status.json` within the process, keyed by its real path, so a second
  `Run(path)` object is covered. The later write merges the fields of an earlier one still in
  flight, so a discarded heartbeat loses nothing. Two threads are serialised by an `RLock`, which
  a handler re-entering on its own thread does not wait on. 02's planner probe measured the race
  first, with a real signal (02's "At writing").* *Amended 2026-10-17, after 02's review: the user
  asked for both issues it opened to be fixed, the merge "at the earliest sensible opportunity" and
  the record with a test. As 02b states it: a re-entered write re-applies only the in-flight writes
  newer than the landed payload it composes from (they are already in it), and the record of what
  landed is never lowered. A discarded heartbeat still loses nothing.*
- **L6: an unreadable status in the in-use check** *(for 03)*.
  (a) **Counted as in use**, and refused in words saying the status cannot be read, so whether the
  run is alive cannot be told, with `end` (after 04) or a person's repair as the remedy. `list`
  marks an `unknown` run that has a manifest with `!!`. (b) Counted as in use, `list` unchanged.
  *Recommended:* (a). An `unknown` run with a manifest is the case that hides a live writer, and
  `list` is where a person looks. *Taken 2026-10-18: (a), refined, as 03's file states it. A run
  whose manifest names the store is in use unless its status says a terminal state, so a status
  with no state, or one the registry never writes, counts as one that cannot be read. And a status
  or manifest that is JSON but not an object is read as unreadable, never raised on: at writing it
  made `list_runs`, and so every store operation and `Run.finish`, raise.*
- **L7: what `end` writes** *(for 04)*.
  (a) **A new terminal state, `lost`**: the registry never saw how the run ended. Exit code `null`.
  An `ended` record: who (`getpass.getuser()`), when, why (`--reason`, required), at what
  `git_head` of the client root, on what host, and the evidence checked (pid answer, boot, heartbeat
  age). The manifest is not written and nothing is deleted. (b) `killed`, with the same record.
  `finish`'s docstring calls `killed` "something a caller reports, not something observed"
  (`runregistrykit/__init__.py:425-426`), and nothing observed a kill. *Recommended:* (a). `lost`
  is added to `TERMINAL_STATES`, which keeps SGK's assertion passing (§0.2), and `liveness` and
  `list` treat it as finished. *Taken 2026-10-18: (a). 04's file fixes the `ended` record's keys,
  among them `verified`, `not_verified_because` and an `evidence` object; `end` writes through the
  status writer, so the status's other fields are kept.*
- **L8: what `end` checks** *(for 04)*.
  (a) **It refuses** unless the run's state is `running`. On this host, it accepts when the boot
  differs or the pid fails `kill -0`, and refuses a live pid, with no override. **A run on another
  host, or one whose status cannot be read**, is refused unless the person passes `--unverified`,
  saying they checked on its host or by other means; the `ended` record then says
  `verified: false` and why. `Run.finish` is not changed. (b) As (a) with no `--unverified`, so a
  run whose machine is gone can never be ended. (c) As (a), and `Run.finish` refuses on a run that
  is not the caller's. *Recommended:* (a). (b) strands a record for ever; (c) breaks launchers that
  finish a detached child's run from the parent. *Taken 2026-10-18: (a). As 04's file reads it, a
  status that does not say (03's sense) is treated as one that cannot be read, and a live pid here is
  refused whatever state stands beside it. `end` is a command, its function private, so `__all__`
  does not change.*
- **L9: what `begin` refuses** *(for 05)*.
  (a) **Every `running` run naming its store**: alive, stale, `foreign`, or with an unreadable
  status (after 03). A stale one is ended with `end` first, and there is no override. (b) Only an
  alive one. *Recommended:* (a). It is the store operations' own rule, applied at the one moment a
  second writer is made, and it turns SGK's resume after a hard kill into `end`, then `begin`.
  The resumed run's `finish(fingerprint=True)` then finds no stale predecessor, and the brief's
  "resumed run's fingerprint" point closes with 04. 05 re-measures that no client begins two runs
  on one store by design. *Taken 2026-10-18: (a). 05's file re-measured it (SGK begins at most one
  run on a store per process) and states the check as the store operations' rule, called from
  `begin`. Six existing tests build two unfinished runs on one store through `begin`; their setup
  changes, through one fixture that sets the earlier runs aside, and none of their assertions. At
  the same time the user asked for `[04-a-pid-out-of-range-makes-pid-alive-raise]` to be fixed in
  05, since the check widens its reach to `begin`.*
- **L10: the release** *(for 06)*. (a) **`v0.2.0`**: what the registry writes changes, and the
  `liveness` output gains a value. (b) `v0.1.1`. *Recommended:* (a). *Taken 2026-10-18: (a). 06's file
  writes the release notes in `docs/releases/v0.2.0.md` and the adoption notes in
  `docs/adoption/v0.2.0/`, and tags nothing itself: the tag is made on 06's commit once CI is green
  on that commit, pushed alone (06 §7).*
- **L11: the `with` point at Python 3.14** *(for 02c; put 2026-10-17)*. At 3.14 the interpreter can
  run a handler just after `with _STATUS_LOCK:` has taken the lock, before the statement's cleanup
  is in force. A handler that raises there leaves the lock held. A bare `with` over an `RLock`,
  with no registry code, does the same at 3.14.8, and not at 3.12 or 3.13 (02c's "At writing"), so
  the window is the interpreter's, not the writer's. (a) **Recorded, not fixed**: `Run._update`'s
  docstring names the window, and the issue is narrowed to it and stays open with no owner until a
  client or CI moves to 3.14. (b) **3.14 excluded**: `requires-python = ">=3.12,<3.14"`, so the
  package does not install there, and the issue closes. (c) A hand-written acquire and release in
  place of the `with`: measured worse, since its `finally` has a window of its own at 3.12, 3.13
  and 3.14. *Recommended:* (a). No client runs 3.14, and CI does not. Every `with` over a lock in a
  3.14 process has the same window, in a client's own code and the standard library's, so (b)
  would not make a 3.14 process safe. It would only block a client's move to 3.14 over a window
  that is not the package's. Whether to report it to CPython is the user's. *Taken 2026-10-17: (a).*

## 7. Gates outside this repository

| Gate | Holds when | Needed by |
|---|---|---|
| **G1** | SGK has adopted `v0.2.0` in a campaign of its own, its pin moved in a commit of its own | — |
| **G2** | CPBH has adopted a release that includes this campaign's changes | — |
| **G3** | SI has adopted a release that includes this campaign's changes | — |

The campaign closes at 07 without waiting for them. Each is recorded on the board when it holds, in
a records commit of its own. SGK's A3 v2 is not a gate (§6.1). If it is hard-killed before SGK
adopts `v0.2.0`, the documented route stays SGK's: `Run.finish` by hand after `kill -0` (brief §1,
step 6).

## 8. Later units of work

None is in this campaign's scope:
- a process start time beside the pid (L3 (b)), if pid reuse within one boot is ever seen;
- `list` reading run directories copied between machines in bulk, beyond marking them `foreign`;
- the other three issues on the inherited board.
