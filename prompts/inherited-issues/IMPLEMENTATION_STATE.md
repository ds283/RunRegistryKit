# inherited-issues — board

**Last updated:** 2026-10-16 · **Status: OPEN — no prompts; holds 3 issues, each until a campaign
takes it over.** Eight were held on 2026-10-16: 5 handed over by SGK's inherited-issues brief, 1 by
its stale-run brief, and 2 found here reading the second. The 5 that bear on a long job were
assigned the same day to the [`interrupted-runs`](../interrupted-runs/IMPLEMENTATION_STATE.md)
campaign, and their entries moved to its board.

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

**Assigned (2026-10-16): the five to the `interrupted-runs` campaign**
([README](../interrupted-runs/README.md), [board](../interrupted-runs/IMPLEMENTATION_STATE.md)),
which takes them in that order: the machine (its 01), the heartbeat write (02), the unreadable
status (03), the hard-killed run (04) and the second writer (05). Their entries moved to that
board's §3 the same day, unchanged but for an **Assigned** line each, and nothing of them is kept
here. Three remain below.

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
