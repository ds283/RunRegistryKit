# interrupted-runs campaign — implementation state

**Last updated:** 2026-10-16 · **Status: OPEN — 01 landed (this commit), not yet reviewed; 02 not
written. L1–L4 (the machine decision) taken by the user on 2026-10-16, as recommended (README
§6.2).** Holds the five issues that bear on a long job that may be interrupted, assigned here from
the `inherited-issues` board on 2026-10-16: four open (§3), one resolved by 01 (§4).

**Campaign:** [`README.md`](README.md) ·
**Evidence:** SGK's `prompts/handover/runregistrykit-stale-run-brief.md` (SGK `79434bf`) and the
`inherited-issues` board ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.3

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

Code is cited as each entry says: at `caad864` for the two entries opened on the inherited board's
first day, at `79015a7` for the three from SGK's stale-run brief. No file under `runregistrykit/`
and not `pyproject.toml` differs between `v0.1.0`, `caad864` and `79015a7`, so every line is the
tag's.

### Decisions

| | Needed by | State |
|---|---|---|
| **L1** what identifies a machine | 01 | **taken** 2026-10-16: (a); the user picks a machine per job, often a Mac Studio, so the package records an identity wherever the platform offers one |
| **L2** where the host is recorded | 01 | **taken** 2026-10-16: (a) |
| **L3** what identifies a boot | 01 | **taken** 2026-10-16: (a) |
| **L4** what `liveness` and `list` say | 01 | **taken** 2026-10-16: (a) |
| **L5** how `status.json` is written | 02 | put, recommended (a) |
| **L6** an unreadable status in the in-use check | 03 | put, recommended (a) |
| **L7** what `end` writes | 04 | put, recommended (a) |
| **L8** what `end` checks | 04 | put, recommended (a) |
| **L9** what `begin` refuses | 05 | put, recommended (a) |
| **L10** the release | 06 | put, recommended (a) |

## 1. Prompts

| # | Prompt | Model | Status | Commit | Suite |
|---|---|---|---|---|---|
| 01 | [`01-the-host.md`](01-the-host.md) | Opus | **landed** 2026-10-16, not yet reviewed ([log](logs/01-the-host.md)) | this commit | 276 → 307 |
| 02 | `02-status-writes.md` | Opus | not written | — | |
| 03 | `03-an-unreadable-status-is-in-use.md` | Sonnet | not written | — | |
| 04 | `04-end-a-run.md` | Opus | not written | — | |
| 05 | `05-begin-refuses-a-second-writer.md` | Sonnet | not written | — | |
| 06 | `06-release-v0.2.0.md` | Opus | not written | — | |
| 07 | `07-verification-and-close-out.md` | Opus | not written | — | |

The suite is 276 at `79015a7` (extraction 08's count; no file under `runregistrykit/` has changed
since).

### 1.1 Items

| Item | Prompt | What | Closes | State |
|---|---|---|---|---|
| **H1** | 01 | the host's identity and boot, in the manifest and `status.json`; `foreign`; a run from an earlier boot `stale`; `list` | `[04-runs-do-not-say-which-machine-produced-them]` | ✅ this commit |
| **W1** | 02 | `status.json`'s own temporary name; a superseded write discarded | `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` | ⬜ |
| **C1** | 03 | an unreadable status counted as in use; `list` flags it | `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` | ⬜ |
| **E1** | 04 | `python -m runregistrykit end`, what it checks and writes | `[a3-v2-a-hard-killed-run-blocks-its-store]` | ⬜ |
| **B1** | 05 | `begin` refuses a store a `running` run names | `[00-begin-does-not-refuse-a-second-writer]` | ⬜ |
| **V1** | 06 | `v0.2.0`, its release notes, the adoption notes | — | ⬜ |
| **Z1** | 07 | the verification document; the close | — | ⬜ |

**Legend.** ⬜ not yet · ✅ done.

## 2. Gates (README §7)

| Gate | Status |
|---|---|
| **G1** | not yet (SGK adopts `v0.2.0`) |
| **G2** | not yet (CPBH adopts) |
| **G3** | not yet (SI adopts) |

---

## 3. Active and unresolved issues

Four. Five were assigned here from the `inherited-issues` board on 2026-10-16, when this campaign
was planned, each with its text unchanged except for an **Assigned** line. One moved with a
correction: `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`'s next step
does not keep a terminal state when the handler returns (README §0.2), so its entry gains a
**Corrected at planning** paragraph. `[04-runs-do-not-say-which-machine-produced-them]` was closed
by 01 (this commit) and is in §4. In the README's order:

### `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`

**Opened:** 2026-10-03 by SGK's `a3-v2-readiness` prompt 04, from the orchestrator's reading;
handed over 2026-10-16. **From:** SGK `prompts/a3-v2-readiness/IMPLEMENTATION_STATE.md` §3.
**Owner:** none. Read, not measured.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 02: `status.json` written
through a name of its own, and a superseded write discarded, under L5 (its README §2). Moved here
from the `inherited-issues` board the same day, unchanged above and below but for this line and the
correction at the end. It is one of the five that bear on a long job that may be interrupted, and
the campaign takes them together.

*The defect.* Every write of `status.json` goes through one fixed temporary name.
`write_json_atomic` (`runregistrykit/__init__.py:242-251`) sets `tmp = path + ".tmp"` (`:245`),
opens it `"w"`, `json.dump`s, flushes, `fsync`s and `os.replace`s it onto `path` (`:251`).
`Run._update` (`:398-403`) calls it for `status.json` (`:402`), and `heartbeat` (`:405`) and
`finish` (`:424`) both go through `_update`. A heartbeat's write and a `finish`'s write share
`status.json.tmp`, and so share its inode while both are open.

*The sequence.* A driver's signal handler runs while a heartbeat is inside `with open(tmp, "w")`,
before its flush. The handler's `finish` reopens `status.json.tmp`, truncating the heartbeat's
inode, writes its payload, flushes, and renames it onto `status.json`. That inode is now
`status.json`, and the heartbeat's handle is still open on it with its payload buffered.

*Corrected on hand-over: both ways the handler can end corrupt it.* The brief described the handler
raising. It does not have to:

- **The handler raises** (SGK's does). Unwinding closes the heartbeat's handle, which writes its
  buffered partial JSON at offset 0 of `status.json`'s inode: the file is a prefix of the heartbeat's
  payload followed by the rest of `finish`'s, and does not parse.
- **The handler returns.** The heartbeat finishes its dump and flushes it at offset 0 of the same
  inode. The two payloads have the same keys (`begin` writes `state` and `exit_code` from the
  start, `:728-734`), and `finish` changes `state` from `running` to a shorter word and
  `exit_code` from `null` to a number, so the heartbeat's is often the longer. Then it overwrites
  all of `finish`'s, the file parses, and it says `running`, the state the heartbeat read before
  `finish`: the terminal state is lost silently, and `list` later shows the run `stale`. If the
  heartbeat's is shorter, the tail of `finish`'s remains and the file does not parse. Either way its
  `os.replace` then raises `FileNotFoundError`, because `status.json.tmp` was renamed away.

So the defect is the package's whatever the client's handler does. SGK's `finish_after_exec` makes a
second `finish`, which reads the unparseable file as `{}` and rewrites it valid but without `pid`,
`stage` or `units_*`; a `SIGKILL` between the two leaves it unparseable, and `list` shows the run as
`unknown`.

*Measured.* Read, not measured. The window is one `json.dump`, once per heartbeat (at most every 30 s
in SGK's driver). SGK has not reproduced it.

*Corrected on hand-over: the fix is not a change to `write_json_atomic`'s name for everyone.* The
brief proposed a unique temporary name per write (`tempfile.mkstemp` in the same directory), inside
`write_json_atomic`. The store layer depends on the fixed name. `_tmp_path`
(`runregistrykit/stores.py:255`, "The temporary name `write_json_atomic` writes through") is how a
leftover from an interrupted sidecar write is found and refused: by `_write_new_sidecar` (`:789`),
`_update_sidecar` (`:809`), `create_sidecar` (`:863`), `copy` and `move`'s preparation (`:1105-1108`),
`retire`'s failure message (`:1532`) and its refusal to complete (`:1650`). Tests pin it:
`test_run_registry.TestStatus.test_status_is_replaced_atomically_from_the_same_directory` asserts
the `.tmp` suffix (`runregistrykit/tests/test_run_registry.py:612`), and `test_store_copy_move`'s
`test_C4_the_sidecar_is_written_to_its_tmp_name_and_the_replace_fails` (`:427`) the sidecar's
`.tmp`. A unique name inside `write_json_atomic` would make every one of those checks look for a
file that is never written, and no test of a refusal would notice unless it builds the leftover
under the old name. Two more points:

- `tempfile.mkstemp` creates the file with mode `0600`, and `os.replace` keeps it; today's
  `open(tmp, "w")` gives `0666` less the umask. `status.json` would become readable only by its
  owner unless the mode is set.
- `write_json_atomic` is in `__all__` (`runregistrykit/__init__.py:96`), so a client may call it
  and may rely on its `.tmp` name.

*Next step.* Give `status.json` writes, and only those, a unique temporary name in the same
directory, with the mode the old name had: through `Run._update`, or an argument to
`write_json_atomic` whose default keeps `<path>.tmp`. Sidecar writes keep the fixed name and its
leftover checks. The reproduction is a test that writes `status.json` twice through a patched
`json.dump` which makes the second write from inside the first, run once with the inner write
raising and once returning. Say in the release notes whether `write_json_atomic` changed.

*Widened (2026-10-16), reading SGK's stale-run brief.* Both outcomes of the race now have measured
consequences beyond `list`. A `status.json` that does not parse hides a run that is still alive
from the store operations' in-use check, which then lets fingerprint, copy, move, retire and amend
proceed: `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`, where a retirement
deleted a live run's store. A terminal state lost silently leaves the run `running` for ever, and
it then blocks its store as a hard-killed run does: `[a3-v2-a-hard-killed-run-blocks-its-store]`.
The window is still one `json.dump` per heartbeat, but a ~36-hour run with a heartbeat every 30 s
has over four thousand of them.

*Corrected at planning (2026-10-16, `interrupted-runs` README §0.2).* The next step above fixes the
unparseable file and not the lost terminal state. With a unique temporary name per write, a `finish`
made from inside a heartbeat's `json.dump` lands first; if the handler then returns, the heartbeat's
`os.replace` lands after it with the payload it read before `finish`, and the run reads `running`
again. Read, not measured. The fix is the unique name **and** a rule that a write superseded by a
later write from the same `Run` is discarded, not replaced (that README's L5). The reproduction's
returning case is the one that tells the two apart.

*Package lines (01, this commit).* 01 moved these lines of `runregistrykit/__init__.py` and
`runregistrykit/stores.py`; nothing above is otherwise changed by it. `write_json_atomic` `:242-251`
→ `:244-253` (`tmp` `:245` → `:247`, `os.replace` `:251` → `:253`); `Run._update` `:398-403` →
`:593-598` (its write `:402` → `:597`); `heartbeat` `:405` → `:600`; `finish` `:424` → `:619`;
`begin`'s first status `:728-734` → `:938-945`, which now writes `host` besides; `write_json_atomic`
in `__all__` `:96` → `:98`. In the store layer `_tmp_path` `:255`, `_write_new_sidecar` `:789`,
`_update_sidecar` `:809` and `create_sidecar` `:863` are unmoved; copy and move's preparation
`:1105-1108` → `:1117-1120`; retire's failure message `:1532` → `:1544`; its refusal to complete
`:1650` → `:1662`. The tests cited are unchanged.

### `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`

**Opened:** 2026-10-16 here, reading SGK's stale-run brief against
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`; measured. **Owner:**
none.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 03: the in-use check counting
a run whose status cannot be read, under L6 (its README §2). Moved here from the `inherited-issues`
board the same day, unchanged above and below but for this line. It is one of the five that bear on
a long job that may be interrupted, and the campaign takes them together.

*The defect.* The store operations' in-use check fails open on a run whose `status.json` cannot be
read. `list_runs` reads it as `read_json(…) or {}` (`runregistrykit/__init__.py:771`), so a
missing, torn or non-JSON `status.json` gives state `None`, and `liveness` answers `unknown` for an
empty payload (`:301`). `_running_runs_naming` keeps only entries whose state is `running`
(`runregistrykit/stores.py:1017`), so the run is not counted, however alive its process, and
fingerprint, copy, move, retire and amend proceed on its store. `list` prints it as `unknown`
without `!!` (`runregistrykit/__main__.py:550-556`; only `stale` is flagged).

*Measured* here at `79015a7`, 2026-10-16, by the scratch probe of
`[a3-v2-a-hard-killed-run-blocks-its-store]`, on a full four-shard registered store in a `tempfile`
directory. A run begun in the probe's own process named the store (liveness `alive`), and
`fingerprint_store`, `retire_store(dry_run=True)` and `copy_store` each refused, naming it. Its
`status.json` was then cut to its first half, as a torn write leaves it. The process still answered
`kill -0`; `list_runs` gave state `None`, liveness `unknown`; and all three operations proceeded. A
real `retire_store` then deleted the primary and all four shards, leaving the tombstone, while the
run's process was alive. Move and amend make the same check (`:1102`, `:2017`), read and not run.

*Impact.* The check is the store layer's one protection of a store being written (module docstring,
`stores.py:102-107`), and here it fails in the direction that loses data: it lets a person
retire, move or fingerprint a store under a live writer, with nothing in `list` to warn them. The
known cause is the race of
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`: rare in any one
heartbeat, but a ~36-hour run has thousands. A `status.json` lost any other way does the same.

*Next step.* Count a run whose manifest names the store and whose `status.json` cannot be read as
possibly running: refuse, saying that the status is unreadable and that the registry cannot tell
whether the run is alive. Such a run is then where a stale one is, and is resolved by
`[a3-v2-a-hard-killed-run-blocks-its-store]`'s route. Fixing the race removes the known cause, not
this failure of the check. The test is the probe's case, asserting the refusal for each operation.
Whether `list` flags an `unknown` run that has a manifest is a smaller, separate choice.

*Package lines (01, this commit).* `list_runs`' status read `runregistrykit/__init__.py:771` →
`:990`; `liveness`'s answer for an empty payload `:301` → `:489`. `_running_runs_naming`'s filter
`stores.py:1017` is unmoved; move's check `:1102` → `:1114`, amend's `:2017` → `:2029`; the module
docstring `:102-107` is unmoved. `list`'s rows, `__main__.py:550-556`, are now `:555-566`; 01 adds
`??` for a `foreign` run there, and `unknown` is still printed without a marker.

### `[a3-v2-a-hard-killed-run-blocks-its-store]`

**Opened:** 2026-10-16 in SGK's `handover` campaign, by a measurement ahead of its A3 v2 launch and
not by a prompt; handed over the same day (SGK `prompts/handover/runregistrykit-stale-run-brief.md`,
committed in SGK `79434bf`). **From:** SGK `prompts/handover/IMPLEMENTATION_STATE.md` §3.
**Owner:** none. Found by SGK in the package, not inherited from SGK's code; its name is SGK's, kept
so that SGK can find it here.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 04: the `end` command, under
L7 and L8 (its README §2). Moved here from the `inherited-issues` board the same day, unchanged
above and below but for this line. It is one of the five that bear on a long job that may be
interrupted, and the campaign takes them together.

*The defect.* A run killed by `SIGKILL`, power loss, a reboot or the OOM killer never reaches
`Run.finish`, so its `status.json` says `running` for ever. `list` reports it as stale, which is
right. Every store operation that checks for a running run counts it "alive **or stale**", so
fingerprint, copy, move, retire and amend refuse its store, and so does a resumed run's
`finish(fingerprint=True)`. The refusals name the remedy, "a stale run is ended by a person, with
Run.finish". No command applies it, and `Run.finish` checks nothing about the run it ends. The
rule the refusals keep, that the registry does not decide that a run is dead
(`runregistrykit/stores.py:1031-1032`), is not in question; SGK does not ask to weaken it.

*The package's lines (`79015a7`).*

- *The in-use check.* `_running_runs_naming` (`runregistrykit/stores.py:998`) keeps every entry
  whose state is `running` other than the excluded caller (`:1017`), whatever its liveness. Its
  callers are copy and move (`_refuse_if_in_use`, `:1029`, called at `:1102`), `fingerprint_store`
  (`:1338`), `retire_store` (`:1664`) and `amend_sidecar` (`:2017`). The module docstring says so
  (`:102-107`).
- *The remedy the refusals name.* At `:1038-1039` (copy, move), `:1344` (fingerprint), `:1667`
  (retire) and `:2020` (amend). `test_store_retire.TestRefusals.test_a_stale_running_run_and_its_remedy`
  (`runregistrykit/tests/test_store_retire.py:436`) asserts it, on `a_stale_run`
  (`runregistrykit/tests/store_fixtures.py:148`): a run given a reaped pid, not a killed process.
- *No command applies it.* `main` (`runregistrykit/__main__.py:408`) has `list` (`:418`) and `store
  show|create|adopt|copy|move|fingerprint|retire|amend` (`:433-522`). None writes a `status.json`.
- *The remedy checks nothing.* `Run.finish` (`runregistrykit/__init__.py:424`) checks only that the
  state is in `TERMINAL_STATES` (`:99`, `:441`). It does not consult `pid_alive` (`:258`), the
  heartbeat or `liveness` (`:294`). A person who ends the wrong directory ends a live run's record.
- *The resumed run.* `_fingerprint_results` passes `taken_by=self` (`:476`), the only exclusion
  (`stores.py:1338-1339`), so a later run on the same store is refused by its stale predecessor. It
  records `fingerprint_error` and writes no fingerprint.

*Measured.* By SGK, 2026-10-16 at SGK `f1a7de3` with `runregistrykit` 0.1.0, no Ray, on a throwaway
two-shard store (brief §1, steps 1-6). A child process that had called `begin` and `heartbeat` was
sent `SIGKILL` (returncode −9); its `status.json` was the same before and after, `running`, and
`liveness` gave `stale`. `list` flagged it `!!`. A second `begin` on the store returned normally,
and its `finish("done", exit_code=0, fingerprint=True)` wrote `done` with no fingerprint and a
`fingerprint_error` naming the killed run. `store fingerprint --write`, `store retire --dry-run`
(with and without `--without-fingerprint`) and `store copy` each exited 1, the sidecar's SHA-256
unchanged. Once `kill -0` showed the pid gone, `Run(…).finish("killed", exit_code=137)` by hand
cleared the `!!`, `store fingerprint` matched the recorded digest, and `store retire` completed.

**Re-measured here** at `79015a7`, 2026-10-16, by a scratch probe (not committed) on the suite's
own fixtures (`RetireTestCase`, a full four-shard store) in a `tempfile` directory: a child process
that called `begin` and `heartbeat(stage=…)` on the store was sent `SIGKILL` (returncode −9).
`status.json` was unchanged by the kill; `list_runs` gave state `running`, liveness `stale`.
`fingerprint_store`, `retire_store(dry_run=True)` and `copy_store` each refused, naming the run. A
resumed run's `finish("done", exit_code=0, fingerprint=True)` wrote `done`, no `fingerprint`, and a
`fingerprint_error` naming the stale run.

*Impact.* For SGK's A3 v2, a ~36-hour Ray build that may be interrupted and resumed: after a hard
kill nothing is lost, and the documented route works, but it is the API by hand and unguarded, on
the build that matters most. For any client: a stale entry stays `!!` in `list` until someone ends
it through the API, and every store operation on its store is refused meanwhile. A `SIGTERM`'d run
whose terminal state was lost to `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`
meets the same block. SGK does not ask for a release before A3 v2 (brief §2).

*Next step.* Choose a route; SGK offers three and prefers the first (brief §1):

1. **A person-run command that records a stale run as terminal**, for example `python -m
   runregistrykit end RUN_ID --reason TEXT`. It refuses unless the run's state is `running` and its
   pid fails `kill -0`, and writes a terminal state, a `null` exit code (nothing observed one) and
   who ended it, when, why and at what `git_head`. It never writes the manifest and deletes nothing.
   The open point is the state: `killed` is a terminal state already, but `finish`'s docstring calls
   it "something a caller reports, not something observed" (`__init__.py:425-426`); a new `lost`
   says the registry never saw how the run ended, at the cost of a fourth terminal state that
   `liveness` and `list` learn. Either is a change to what the registry writes. The same check could
   guard `Run.finish` when called on a run that is not the caller's own.
2. **An explicit exclusion on the store operations**, for example `--stale-run RUN_ID`, accepted
   only for a named run whose pid fails `kill -0` and recorded in the sidecar's `history` or the
   tombstone. It unblocks the store and leaves the run `running`, with its `!!`.
3. **`begin` and `finish` learning about predecessors** (`supersedes: [RUN_ID]`). It decides at
   `begin` that a stale run is dead, the line the package has chosen not to cross; listed by SGK
   for completeness.

*Added on hand-over.* Any route that tests `kill -0` tests evidence that holds only on the machine
that owns the pid, and only while the pid has not been reused, which a reboot, one of this entry's
causes, makes likely. So the route depends on `[04-runs-do-not-say-which-machine-produced-them]`
(its fourth question), and that decision is taken first, or with this one. The test SGK proposes
stands: begin a run in a child process, `SIGKILL` it, and assert what the new route does; the
probe above is its shape. `a_stale_run` fakes the pid and never exercises a kill.

*Split on hand-over.* The brief's point that `begin` does not look for a run already on its store
is held as its own entry, `[00-begin-does-not-refuse-a-second-writer]`: it holds whether or not the
first run is dead, and its fix is none of the three routes.

*Package lines (01, this commit).* In `runregistrykit/stores.py`: `_running_runs_naming` `:998` and
its filter `:1017` are unmoved; `_refuse_if_in_use` `:1029` → `:1041`, called at `:1102` → `:1114`;
`fingerprint_store`'s check `:1338-1339` → `:1350-1351`; `retire_store`'s `:1664` → `:1676`;
`amend_sidecar`'s `:2017` → `:2029`; the module docstring `:102-107` is unmoved. The remedy text
`:1038-1039` → `:1050-1051` (copy, move), `:1344` → `:1356` (fingerprint), `:1667` → `:1679`
(retire), `:2020` → `:2032` (amend), unchanged in its words; `stores.py:1031-1032` → `:1043-1044`.
In `runregistrykit/__main__.py`: `main` `:408` → `:413`, `list` `:418` → `:423`, the store
subcommands `:433-522` → `:438-527`. In `runregistrykit/__init__.py`: `Run.finish` `:424` → `:619`
(its docstring `:425-426` → `:620-621`), `TERMINAL_STATES` `:99` → `:101`, its check `:441` →
`:636`; `pid_alive` `:258` → `:260` (`PermissionError` `:276` → `:278`); `liveness` `:294` →
`:465`; `_fingerprint_results`' `taken_by=self` `:476` → `:671`.

### `[00-begin-does-not-refuse-a-second-writer]`

**Opened:** 2026-10-16, split on hand-over from SGK's `[a3-v2-a-hard-killed-run-blocks-its-store]`
(its brief §1, "*`begin` does not look*"), and measured here for a live first run. **Owner:**
none.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 05: `begin`'s refusal, under
L9 (its README §2). Moved here from the `inherited-issues` board the same day, unchanged above and
below but for this line. It is one of the five that bear on a long job that may be interrupted, and
the campaign takes them together.

*The defect.* `begin` (`runregistrykit/__init__.py:604`) reads the results store's sidecar only to
refuse a tombstone (`:686-698`, the refusal at `:692`). It does not ask whether a `running` run,
alive or stale, already names that store, so a second run on a store that a live run is writing is
begun without a word. The store operations make that check (`_running_runs_naming`,
`runregistrykit/stores.py:998`), and the module docstring calls it "a check and not a lock: a run
begun after it is not seen" (`:106-107`); `begin` does not make it at all.

*Measured* here at `79015a7`, 2026-10-16, by the scratch probe of
`[a3-v2-a-hard-killed-run-blocks-its-store]`: with a run begun in the probe's own process on a
registered store (liveness `alive`), a second `begin` with the same `results` returned a run, and
the two manifests carry the same `results_store_id`. SGK measured the stale case (brief §1, step
4).

*Impact.* The registry does not schedule or lock, so nothing here can stop two writers; but a
resume after an interruption is when a person begins a second run on a store, and the case that
does harm is the one where the first run is not dead: a detached child still working, a `SIGTERM`
not yet acted on, or a run on another machine whose pid this machine cannot test
(`[04-runs-do-not-say-which-machine-produced-them]`). Then two jobs write one SQLite store, and
nothing records that they did.

*Next step.* `begin` names the `running` runs whose manifest names its `results`, by path or by
`results_store_id` as `runs_naming` matches them (`stores.py:957`), and refuses, before the run
directory is created, if any is alive. What a stale one gets is the decision of
`[a3-v2-a-hard-killed-run-blocks-its-store]`: refusing it too is the reading consistent with "the
registry does not decide that a run is dead", and leaves a person to end it first by that entry's
route. A refusal writes nothing new, so it is not a change to what the registry writes. The test:
begin a run, begin a second on its store, and assert that the refusal names the first and that no
second run directory exists.

*Package lines (01, this commit).* `begin` `runregistrykit/__init__.py:604` → `:799`; its tombstone
check `:686-698` → `:890-902`, the refusal `:692` → `:896`; it now reads `this_host()` at `:904`,
after that check and before the run directory is made. `_running_runs_naming` `stores.py:998`, the
module docstring `:106-107` and `runs_naming` `:957` are unmoved.

---

## 4. Resolved issues

### `[04-runs-do-not-say-which-machine-produced-them]`

**Opened:** 2026-09-24 in SGK, from a cross-machine question, not by a prompt; handed over
2026-10-16. **From:** SGK `prompts/run-registry/IMPLEMENTATION_STATE.md` §3. **Owner:** none. **A
decision, not a defect.** SGK decided the change for its own runs (user decision of 2026-09-24) and
never built it; whether the package makes it for every client is this repository's decision.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 01: the host, its identity and
its boot, recorded and used by `liveness` and `list`, under L1–L4 (its README §2). Moved here from
the `inherited-issues` board the same day, unchanged above and below but for this line. It is one of
the five that bear on a long job that may be interrupted, and the campaign takes them together.

*What is asked.* SGK's decision: a `machine` field in the manifest; `list` refusing to judge the
liveness of a record whose machine is not this one; and a rule that only terminal-state run
directories are transferred between machines. ChamPBH and StochasticInstantons may or may not run
one registry across machines.

*The package's lines.* The manifest is built in `begin` (`runregistrykit/__init__.py:604`): `run_id`,
`created`, `purpose`, `campaign`, `prompt`, `argv`, `cwd`, `script`, `script_sha256`, `unit`,
`expected_units`, `checkpoint`, `results`, `results_store_id`, `scope`, `heartbeat_means`
(`:707-723`), then `git_provenance`'s `git_head` and `git_dirty` (`:724`, defined `:140`) and
`packages` (`:725`). No machine, platform or hostname is recorded. Liveness is `pid_alive` (`:258`,
`os.kill(pid, 0)` against this machine's process table) and `liveness(status, stale_after, now)`
(`:294`), called by `list_runs` (`:749`, `:784`); neither takes a machine.

*Measured.* `git grep -n -i 'machine\|platform\|node()' caad864 -- runregistrykit` finds only an
unrelated comment about path separators (`stores.py:240`) and a comment in a test
(`tests/test_run_registry.py:169`). Read 2026-10-16.

*Impact.* Two. *Provenance:* SGK is to run its A3 rebuild on a second machine, and rows computed on
different hardware can differ in their last bits; `git_head` says what code ran, not what ran it.
*Liveness:* once run directories are copied between machines, `list` tests a pid from another
machine against this one's process table. A terminal-state record is harmless; one still marked
`running` gets a confident wrong answer, a false "dead" or, if the pid is reused here, a false
"alive".

*Added on hand-over: three questions the decision has to answer.*

- **A manifest with no `machine`.** Every client holds manifests written before the field would
  exist, and no reader of an older form is added (`CLAUDE.md`, "Releases"). So the rule has to give
  the field's absence a meaning in the current form, for example "not recorded: liveness is judged
  here, as today", and `list` has to say which it did.
- **What names a machine.** `platform.node()`, as the brief proposes, is the hostname, and on macOS
  it can change with the network. A machine's own runs would then read as foreign. A name a person
  sets (an environment variable or a per-machine config file, not the client's committed
  `runregistrykit.toml`, which every machine shares), with `platform.machine()` beside it for the
  architecture, would be steadier.
- **Where it is recorded.** The pid that liveness tests is in `status.json`, written by `heartbeat`
  (`:405`), which a launcher calls with a detached child's pid. The machine that matters for
  liveness is the one that pid belongs to, so the field belongs beside the pid, in `status.json`,
  whether or not the manifest records it too for provenance.

*Next step.* Decide whether the registry records the machine for every client, and if so answer the
three questions above. `list` reporting a record from another machine as *foreign*, rather than
judging its liveness, is still recording, inside the registry's "it records; it does not supervise"
boundary. SGK has nothing live to migrate: none of its 43 run directories was `running` on
2026-10-16 (SGK's reading).

*Added 2026-10-16, reading SGK's stale-run brief: a fourth question, and why this decision comes
first.*

- **A pid reused on this machine.** A reboot, one of the ways a run ends without `finish`, ends
  every run on the machine, and afterwards the pids in their `status.json` can belong to new
  processes. `pid_alive` (`runregistrykit/__init__.py:258`) then answers `True`, as it does for
  another user's process (`PermissionError`, `:276`). `liveness` still calls such a run stale when
  its heartbeat is old (`:310`), so `list` is right, but a guard that refuses unless the pid fails
  `kill -0` refuses wrongly. Something recorded beside the pid that changes when the machine
  reboots (a boot identifier) or that names the process (its start time) would let a check tell a
  reused pid from the run's own. Like the machine, it belongs beside the pid, in `status.json`.
- **The other long-job entries depend on it.** The routes proposed for
  `[a3-v2-a-hard-killed-run-blocks-its-store]` and `[00-begin-does-not-refuse-a-second-writer]`
  judge another run's liveness by its pid. Their guards mean what they say only once this decision
  is made, so it is taken first, or with them.

**Resolved (2026-10-16, by 01, this commit).** The package records the machine and the boot a run is
on, for every client, under L1–L4 (README §6.2) as the user took them. `this_host()` is a new public
name (`runregistrykit/__init__.py:431`). Its three private readers (`:338`, `:376`, `:410`) use the
standard library only, with no subprocess. `begin` writes the manifest's `host` (`:929`) and the
first status's (`:944`), and every later write keeps the status's. `liveness` (`:465`) is ordered as
01's §2.4 says. `list_runs` (`:960`) reads this host once per call and gives `host`, `host_id` and
`host_recorded`. `list` marks a `foreign` run `??` and counts records with no host; the store
operations' refusal names a `foreign` run by its host. The log is
[`logs/01-the-host.md`](logs/01-the-host.md). What resolved each of the four questions:

- **A manifest with no `machine`.** A record with no `host` was written before the field existed.
  So were a `host` that is not an object and a `host.id` of null, which is what a platform with no
  identity records. Each is judged here, by `kill -0` and the heartbeat, exactly as `v0.1.0` judged
  it, and `list` counts it as "N with no host recorded". Pinned by
  `test_host.TestAnOldRecord.test_a_status_with_no_host_is_judged_by_pid_and_heartbeat` and
  `test_list_runs_judges_it_here_and_says_no_host_is_recorded`;
  `test_host.TestTheJudgement.test_a_host_that_names_no_id_is_judged_here`; and
  `test_host.TestTheCommandLine.test_foreign_and_stale_rows_and_the_count_of_records_with_no_host`.
- **What names a machine.** The OS's own identity, as a digest: macOS `gethostuuid(3)`, Linux
  `/etc/machine-id` (then `/var/lib/dbus/machine-id`). The id is the first 16 hex characters of the
  SHA-256 of `b"runregistrykit host\0"` and the identity, and the identity itself is never written.
  A display name sits beside it, `RUNREGISTRYKIT_HOST_NAME` or `platform.node()`, and is for
  reading only. Pinned by `test_host.TestTheReaders` (the readers on macOS, run locally, and on
  Linux, run only in CI; the digest; the name; each reader failing; the Linux files and the macOS
  calls failing, on any platform) and by
  `test_host.TestWhatIsWritten.test_no_raw_identity_reaches_a_file`.
- **Where it is recorded.** Both. `status.json` gets `host: {id, boot}` beside the pid it
  qualifies, and every later write keeps it, `heartbeat(pid=…)` included. The manifest gets `host:
  {id, name, machine, system, release, python}` for provenance. Both are written with null values
  when a reader fails. Pinned by `test_host.TestWhatIsWritten` (the manifest and the first status;
  every later write; a failing reader writing null).
- **A reused pid.** A `running` record on this host from another boot is `stale` whatever `kill -0`
  says. A `running` record on another host is `foreign`: its pid is not tested here and its
  heartbeat is not weighed, it is never called dead, and the store operations count it as in use.
  Pinned by `test_host.TestTheJudgement` (another host, live pid or dead; an id read where this host
  has none; another boot; this host and boot; a terminal record from another host; `here` read
  afresh) and `test_host_stores.TestARunOnAnotherHostIsInUse` (copy, move, fingerprint, retire's
  dry run and amend each refuse and name the host). A pid reused within one boot is not told apart
  (L3 (b), README §8).

SGK's third point, that only terminal-state run directories are moved between machines, is a rule
for a client's people and not something the package enforces. A `running` record moved anyway is
reported `foreign`, which is what keeps the package from judging it.

