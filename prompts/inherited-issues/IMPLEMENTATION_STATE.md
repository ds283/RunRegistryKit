# inherited-issues — board

**Last updated:** 2026-10-16 · **Status: OPEN — no prompts; holds 8 issues: 5 handed over by SGK's
inherited-issues brief, 1 by its stale-run brief, and 2 found here reading the second, all on
2026-10-16, each until a campaign takes it over.**

**Plan:** [`README.md`](README.md) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.2

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

Code is cited at `caad864`, where each defect was read in the package on 2026-10-16. No file under
`runregistrykit/` and not `pyproject.toml` differs between the tag `v0.1.0` and `caad864`, so the
lines are also the tag's, which is what SGK reads. `datastorekit` is cited as installed, `0.4.0`.
Each entry names the SGK board entry it came from. SGK's measurements before 2026-10-15 were taken
on SGK's copy of the registry, before `runregistrykit` replaced it, and are restated here with the
package's names.

The three entries added later on 2026-10-16, from SGK's stale-run brief, cite the package at
`79015a7`. No file under `runregistrykit/` and not `pyproject.toml` differs between `v0.1.0` and
`79015a7` either (`git diff --stat v0.1.0 79015a7 -- runregistrykit pyproject.toml` is empty), so
their lines too are the tag's.

SGK's first brief also named two issues about registry behaviour that it keeps as its own:
`[00-a-sigterm-pipeline-run-is-recorded-as-failed]` and
`[04-a-sigterm-during-ray-init-meets-rays-handler-not-the-drivers]`. Both are in SGK's driver and
Ray. The package holds no signal handling (`git grep -n 'SIGTERM\|signal\.' caad864 --
runregistrykit` is empty), and `Run.finish` records the state its caller reports
(`runregistrykit/__init__.py:424-427`). Neither is held here.

---

## 3. Active and unresolved issues

Eight. Five were handed over by SGK on 2026-10-16 by its first brief. Four were recorded against
SGK's `RunRegistry/`; the fifth SGK found while adopting `v0.1.0`. Three of the brief's next steps
are corrected below, each marked **Corrected on hand-over**: the next step of
`[00-a-copy-carries-its-sources-present-tense-fields]`, that of
`[01-cross-filesystem-move-advice-says-delete-by-hand]`, and that of
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`, whose impact is also
widened. `[04-runs-do-not-say-which-machine-produced-them]` gains three questions its decision has
to answer.

Three more were added later on 2026-10-16, from SGK's second brief
(`prompts/handover/runregistrykit-stale-run-brief.md`, committed in SGK `79434bf`), which SGK
wrote ahead of its ~36-hour A3 v2 build: `[a3-v2-a-hard-killed-run-blocks-its-store]`, SGK's,
accepted with one point split out as `[00-begin-does-not-refuse-a-second-writer]`; and
`[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`, found here reading the brief
against `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`. Reading it also
gave `[04-runs-do-not-say-which-machine-produced-them]` a fourth question and widened the signal
entry's impact again.

*The ones that bear on a long job.* Five of the eight bear on a long job that may be interrupted
and resumed: the hard-killed run, the second writer, the unreadable status, the machine and the
signal inside a heartbeat write. They share their design: the first two judge another run's
liveness by its pid, which means something only on that pid's machine and only while the pid has
not been reused, and the third and fifth are one cause and one consequence. They are best taken by
one campaign, the machine decision first. The other three (`copy`'s fields, the move advice, the
closed pipe) do not affect a run.

### `[00-a-copy-carries-its-sources-present-tense-fields]`

**Opened:** 2026-09-25 by SGK's audit of store retirement (SGK `docs/store-retirement-audit.md`
§2.12); handed over 2026-10-16. **From:** SGK `prompts/store-retirement/IMPLEMENTATION_STATE.md`
§3. **Owner:** none. A decision about `copy`'s design, not a defect in what it was designed to do.

*The defect.* `copy_store` (`runregistrykit/stores.py:1138`) deep-copies the source's sidecar
(`:1160`), replaces seven fields (`store_id`, `datastore`, `name`, `purpose`, `created`,
`copied_from`, `history`, `:1161-1172`) and writes the rest verbatim (`_write_new_sidecar`,
`:1173`). That is its design: "Every other field, unknown ones included, is the source's,
verbatim" (docstring, `:1139-1145`), and the sidecar schema says unknown fields "are carried and
never interpreted, even ones holding paths" (`:81-83`). Some unknown fields make claims about the
store they sit in. A copy of SGK's live A3 store carries three: `backup`, whose `"retained": true`
describes a backup *of the source*; `restart.command`, whose `--database` is the source's path; and
`run_history`, the source's runs. `move_store` (`:1179`) keeps the sidecar's fields, which is right
for a move: the store is the same store.

*Measured* (SGK `store-fingerprint` log 05, Phase C): a copy of the live A3 store's sidecar carried
all three. Still so at `caad864`: the lines above.

*Impact.* Nothing in the package reads these fields, so no code misbehaves. A person who followed a
copy's `restart` would resume a pipeline into the source store, the accident of SGK's 2026-09-23
(SGK `2ebb7b6`, 54 rows written into the live A3 store) by another route. `store amend` is the
remedy for a given copy.

*Corrected on hand-over: what the package can and cannot do about it.* The three fields are SGK's.
To the package they are unknown fields, and the package may not name a client's field (`CLAUDE.md`,
enforced by the no-client guard). So "flag such fields", the brief's third option, has to be done
without naming them. Two ways that keep to the rule:

1. **Report, change nothing written.** `copy` reports the unknown fields of the new sidecar whose
   strings name the source, with the machinery `retire` already uses to find references to a store:
   `_strings` (`:1421`) walks a payload into JSON paths and strings, `_names_one_of` (`:1433`)
   tests a string against target paths, both used by `_find_references` (`:1444`). This finds
   `$.restart.command` and a `backup` path, but not `backup.retained` or a `run_history` entry that
   names no path of the source. It changes only what `copy` prints, so it is not a change to what
   the registry writes.
2. **The client says which fields belong to one store.** A key in the client's
   `runregistrykit.toml` lists top-level unknown fields that `copy` drops, or replaces with a
   marker. The client knows its fields; the package still names none. It changes what a copied
   sidecar contains, which is a change to the interface (`CLAUDE.md`, "Releases"), made only by a
   prompt that says so.

The first is a first step under either decision. The tests' sidecar fixture already carries
`run_history`, `restart` and `backup` objects with paths in them
(`runregistrykit/tests/store_fixtures.py:39-40`, `:58`, `:74`, `:78`), so neither needs a new
fixture.

*Next step.* Decide `copy`'s design: keep carrying every unknown field and report the ones that
name the source (1), or let the client declare per-store fields (2, which includes 1's report for
what the client has not declared).

### `[01-cross-filesystem-move-advice-says-delete-by-hand]`

**Opened:** 2026-09-25 by SGK's `store-retirement` prompt 01; narrowed 2026-10-12 by SGK's
`dk-and-rpk-migration` 09, which handed the advice's text to DatastoreKit; this half handed over
2026-10-16. **From:** SGK `prompts/store-retirement/IMPLEMENTATION_STATE.md` §3. **Owner:** none.

*Two halves; this is the second.* DatastoreKit's half is the advice itself: on `EXDEV`,
`ShardedPool._failure_message` appends "copy it instead, and then delete the source by hand"
(installed `datastorekit/SQL/ShardedPool.py:3026-3030`; `move_store`'s docstring says the same at
`:2684`), though the package has `ShardedPool.delete_store` (`:2704`). It is DatastoreKit's
`[01-cross-filesystem-move-advice-says-delete-by-hand]`, on its `inherited-issues` board, and is
not held here.

*The defect.* `store move` relays that advice for a registered store. `move_store`
(`runregistrykit/stores.py:1179`) calls `_store_files("move", ShardedPool.move_store, src, dst)`
(`:1195`). `_store_files` (`:1119-1129`) catches any exception from the pool and re-raises
`RuntimeError(f"{e}. No sidecar was written or moved: sidecar files at the destination [...]; at
the source [...]")` (`:1125-1128`), so DatastoreKit's text reaches the person verbatim. A
registered store is retired with `store retire`, which leaves its sidecar as a tombstone; deleting
its files by hand leaves a sidecar describing nothing, with no tombstone. DatastoreKit cannot know
that a store is registered, so the place to say so is here, where it is known.

*Measured.* Read from the code, 2026-10-16. Not run: it needs a cross-filesystem move that fails. No
test here asserts the advice (`git grep -n 'by hand' caad864 -- runregistrykit` finds nothing about
a deleted source).

*Impact.* Low, and only on a failed cross-filesystem move. Nothing acts on the advice; a person who
follows it makes the broken case.

*Corrected on hand-over.* The brief offered two routes, recognising the cross-filesystem failure by
DatastoreKit's message text (fragile, the hazard of
`[00-a-refusal-matches-datastorekit-message-text]`) or waiting for DatastoreKit's reword and letting
this entry close with it. Neither is needed, and the second would not close it:

- **No text need be matched.** DatastoreKit raises `RuntimeError(ShardedPool._failure_message(plan,
  step, e)) from e` (installed `ShardedPool.py:2997`), and `_failure_message` adds the advice only
  when `isinstance(e, OSError) and e.errno == errno.EXDEV` (`:3026`). So in `_store_files`, the
  caught exception's `__cause__` is that `OSError`, and `errno.EXDEV` can be tested on it. That
  depends on DatastoreKit's exception chaining, not its wording; a test that makes the move raise
  `OSError(errno.EXDEV, ...)` pins it.
- **DatastoreKit's reword does not close this half.** Its next step is to name
  `ShardedPool.delete_store`. For a registered store that is still the wrong instruction: it deletes
  the files and leaves no tombstone. The relay has to say `store retire` whatever DatastoreKit
  says.

*Next step.* In `_store_files`, for `operation == "move"`, when the cause is an `OSError` with
`errno.EXDEV`, add that the store is registered, so the source is retired with `store retire` after
the copy, never deleted by hand or with `ShardedPool.delete_store`.

### `[04-runs-do-not-say-which-machine-produced-them]`

**Opened:** 2026-09-24 in SGK, from a cross-machine question, not by a prompt; handed over
2026-10-16. **From:** SGK `prompts/run-registry/IMPLEMENTATION_STATE.md` §3. **Owner:** none. **A
decision, not a defect.** SGK decided the change for its own runs (user decision of 2026-09-24) and
never built it; whether the package makes it for every client is this repository's decision.

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

### `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`

**Opened:** 2026-10-03 by SGK's `a3-v2-readiness` prompt 04, from the orchestrator's reading;
handed over 2026-10-16. **From:** SGK `prompts/a3-v2-readiness/IMPLEMENTATION_STATE.md` §3.
**Owner:** none. Read, not measured.

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

### `[06-runregistrykit-list-into-a-closed-pipe-ends-in-a-traceback]`

**Opened:** 2026-10-15 in SGK's `runregistry-extraction` 06 review, by its orchestrator, at the
user's request; handed over 2026-10-16. **From:** SGK
`prompts/runregistry-extraction/IMPLEMENTATION_STATE.md` §3. **Owner:** none.

*The defect.* `python -m runregistrykit list` flushes `stdout` unguarded after its summary line
(`runregistrykit/__main__.py:563`, after the `print` at `:562`; `main` is `:408`). When the reader
closes the pipe first, as `list | head -4` does, the flush raises `BrokenPipeError`: a traceback,
then Python's "Exception ignored … BrokenPipeError" at exit. Nothing in the file catches
`BrokenPipeError`, and every other `print` in `main` is equally unguarded, so other commands (`store
show` prints a whole sidecar, `:404-405`) can probably do it too; only `list` was seen.

*Measured* (SGK, at SGK `7af17bd`): 1 of 30 runs of `list | head -4`, on a 17 kB listing. A race.
Inherited: SGK's `RunRegistry/__main__.py:503` at `a45aefc` had the same flush, and this package
imported it.

*Impact.* Nothing is lost or written; what the reader saw is complete up to where it stopped. A
shell with `pipefail`, or a script that treats output on stderr as failure, would see a routine
`list` fail. Cosmetic otherwise.

*Next step.* Catch `BrokenPipeError` around `main`'s work, for every command, point `stdout`'s file
descriptor at `os.devnull` so the flush at exit does not raise again, and exit non-zero. A test: a
reader that closes first, with the exit code and stderr asserted.

### `[a3-v2-a-hard-killed-run-blocks-its-store]`

**Opened:** 2026-10-16 in SGK's `handover` campaign, by a measurement ahead of its A3 v2 launch and
not by a prompt; handed over the same day (SGK `prompts/handover/runregistrykit-stale-run-brief.md`,
committed in SGK `79434bf`). **From:** SGK `prompts/handover/IMPLEMENTATION_STATE.md` §3.
**Owner:** none. Found by SGK in the package, not inherited from SGK's code; its name is SGK's, kept
so that SGK can find it here.

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

### `[00-begin-does-not-refuse-a-second-writer]`

**Opened:** 2026-10-16, split on hand-over from SGK's `[a3-v2-a-hard-killed-run-blocks-its-store]`
(its brief §1, "*`begin` does not look*"), and measured here for a live first run. **Owner:**
none.

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

### `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`

**Opened:** 2026-10-16 here, reading SGK's stale-run brief against
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`; measured. **Owner:**
none.

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

---

## 4. Resolved issues

None.
