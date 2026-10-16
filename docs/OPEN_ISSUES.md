# Open issues — project-wide index

One line per open issue, pointing at the board that holds it. The board is right if the two
disagree. See `CLAUDE.md` for the maintenance rule.

**Last updated:** 2026-10-16 · **7 open**: 2 on the `extraction` board (§1.1) and 5 on the
`inherited-issues` board (§1.2).

## 1. By campaign

### 1.1 `extraction` ([board](../prompts/extraction/IMPLEMENTATION_STATE.md)) — closed 2026-10-15

| Issue | Owner | Hook |
|---|---|---|
| `[00-the-shard-fixtures-reach-into-shardedpool]` | none | The carried shard fixtures set private `ShardedPool` attributes |
| `[00-a-refusal-matches-datastorekit-message-text]` | none | An unreadable store is recognised by matching DatastoreKit's message text |

### 1.2 `inherited-issues` ([board](../prompts/inherited-issues/IMPLEMENTATION_STATE.md)): issues handed over by SGK, 2026-10-16

Opened in SGK while the registry was SGK's code, or found by SGK adopting `v0.1.0`, and handed to
this repository by SGK's `runregistry-extraction` prompt 09 (its brief, SGK `e96c1ea`). The board
holds each in full, read against the package at `caad864`. None is assigned to a campaign.

| Issue | Owner | Hook |
|---|---|---|
| `[00-a-copy-carries-its-sources-present-tense-fields]` | none | `copy` carries unknown sidecar fields verbatim, so a copy can name the source's backup and a restart into the source store; a decision about `copy`'s design |
| `[01-cross-filesystem-move-advice-says-delete-by-hand]` | none | `store move` relays DatastoreKit's "delete the source by hand" for a registered store, which is retired instead |
| `[04-runs-do-not-say-which-machine-produced-them]` | none | No run records its machine, so `list` judges a copied record's pid against the wrong process table; a decision for every client |
| `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` | none | Heartbeat and `finish` share `status.json.tmp`, so a signal mid-heartbeat can corrupt `status.json` or lose the terminal state |
| `[06-runregistrykit-list-into-a-closed-pipe-ends-in-a-traceback]` | none | `list \| head` can end in a `BrokenPipeError` traceback; cosmetic, nothing lost |
