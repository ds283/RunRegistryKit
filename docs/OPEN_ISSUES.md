# Open issues — project-wide index

One line per open issue, pointing at the board that holds it. The board is right if the two
disagree. See `CLAUDE.md` for the maintenance rule.

**Last updated:** 2026-10-18 · **11 open**: 2 on the `extraction` board (§1.1), 3 on the
`inherited-issues` board (§1.2) and 6 on the `interrupted-runs` board (§1.3).

## 1. By campaign

### 1.1 `extraction` ([board](../prompts/extraction/IMPLEMENTATION_STATE.md)) — closed 2026-10-15

| Issue | Owner | Hook |
|---|---|---|
| `[00-the-shard-fixtures-reach-into-shardedpool]` | none | The carried shard fixtures set private `ShardedPool` attributes |
| `[00-a-refusal-matches-datastorekit-message-text]` | none | An unreadable store is recognised by matching DatastoreKit's message text |

### 1.2 `inherited-issues` ([board](../prompts/inherited-issues/IMPLEMENTATION_STATE.md)): issues handed over by SGK, 2026-10-16

Five opened in SGK while the registry was SGK's code, or found by SGK adopting `v0.1.0`, and handed
to this repository by SGK's `runregistry-extraction` prompt 09 (its brief, SGK `e96c1ea`), read
against the package at `caad864`. Three more from SGK's stale-run brief (SGK `79434bf`): one SGK's,
two found here reading it, read at `79015a7`. The five that bear on a long job were assigned to
`interrupted-runs` on 2026-10-16 (§1.3); the three left are assigned to no campaign.

| Issue | Owner | Hook |
|---|---|---|
| `[00-a-copy-carries-its-sources-present-tense-fields]` | none | `copy` carries unknown sidecar fields verbatim, so a copy can name the source's backup and a restart into the source store; a decision about `copy`'s design |
| `[01-cross-filesystem-move-advice-says-delete-by-hand]` | none | `store move` relays DatastoreKit's "delete the source by hand" for a registered store, which is retired instead |
| `[06-runregistrykit-list-into-a-closed-pipe-ends-in-a-traceback]` | none | `list \| head` can end in a `BrokenPipeError` traceback; cosmetic, nothing lost |

### 1.3 `interrupted-runs` ([board](../prompts/interrupted-runs/IMPLEMENTATION_STATE.md)): open 2026-10-16, 01, 02, 02b, 02c and 03 landed

Assigned from the `inherited-issues` board on 2026-10-16: the five that bear on a long job that
may be interrupted, taken in this order, one prompt each (the campaign's README §2). The first,
`[04-runs-do-not-say-which-machine-produced-them]`, was closed by 01 on 2026-10-16, and the second,
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`, by 02 on 2026-10-17. Two more were opened by 02's review on 2026-10-17, on the bookkeeping of the
`status.json` writer, and closed by 02b the same day. One was opened by 02b's review, the same day,
and assigned to 02c, which fixed it at Python 3.12 and 3.13 and narrowed it to its 3.14 `with`
point, now with no owner. One was opened at the writing of 03, on 2026-10-18, with no owner. 03 closed `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` the same day, and its work opened one more, with no owner; its review opened another, with no owner.

| Issue | Owner | Hook |
|---|---|---|
| `[a3-v2-a-hard-killed-run-blocks-its-store]` | 04 | A `SIGKILL`'d run stays `running`, and the store operations count a stale run as in use, so fingerprint, copy, move, retire, amend and a resumed run's fingerprint are refused; the named remedy, `Run.finish`, has no command and checks no pid |
| `[00-begin-does-not-refuse-a-second-writer]` | 05 | `begin` does not look for a `running` run on its results store, so a second writer on a live run's store is begun silently |
| `[02b-a-raising-handler-can-leave-the-status-lock-held]` | none | At Python 3.14 only, a handler raising just after `with` takes the writer's lock leaves it held, as at any `with` on that version; no client or CI runs 3.14 |
| `[03-a-run-whose-manifest-cannot-be-read-names-no-store]` | none | A live run whose manifest is torn or missing names no store, so the store operations proceed on the store it is writing |
| `[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]` | none | `Run(path)` on a manifest that is JSON but not an object constructs, then `checkpoint_path` and `results_path` raise `AttributeError`; low impact |
| `[03-store-show-raises-on-a-state-that-is-a-list-or-an-object]` | none | `store show` ends in a `TypeError` traceback when a run's status `state` is a JSON list or object; predates 03; low impact |
