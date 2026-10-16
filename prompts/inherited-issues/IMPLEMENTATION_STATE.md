# inherited-issues — board

**Last updated:** 2026-10-16 · **Status: OPEN — no prompts; holds 5 issues handed over by SGK on
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

SGK's brief also named two issues about registry behaviour that it keeps as its own:
`[00-a-sigterm-pipeline-run-is-recorded-as-failed]` and
`[04-a-sigterm-during-ray-init-meets-rays-handler-not-the-drivers]`. Both are in SGK's driver and
Ray. The package holds no signal handling (`git grep -n 'SIGTERM\|signal\.' caad864 --
runregistrykit` is empty), and `Run.finish` records the state its caller reports
(`runregistrykit/__init__.py:424-427`). Neither is held here.

---

## 3. Active and unresolved issues

Five, handed over by SGK on 2026-10-16. Four were recorded against SGK's `RunRegistry/`; the fifth
SGK found while adopting `v0.1.0`. Three of the brief's next steps are corrected below, each marked
**Corrected on hand-over**: the next step of `[00-a-copy-carries-its-sources-present-tense-fields]`,
that of `[01-cross-filesystem-move-advice-says-delete-by-hand]`, and that of
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`, whose impact is also
widened. `[04-runs-do-not-say-which-machine-produced-them]` gains three questions its decision has
to answer.

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

---

## 4. Resolved issues

None.
