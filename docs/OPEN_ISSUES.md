# Open issues — project-wide index

One line per open issue, pointing at the board that holds it. The board is right if the two
disagree. See `CLAUDE.md` for the maintenance rule.

**Last updated:** 2026-10-14 · **7 open**, all on the `extraction` board.

## 1. By campaign

### 1.1 `extraction` ([board](../prompts/extraction/IMPLEMENTATION_STATE.md)) — live 2026-10-14

| Issue | Owner | Hook |
|---|---|---|
| `[00-the-fingerprint-reads-a-clients-registry]` | 04 | `fingerprint_store` imports SGK's registry and fingerprints with SGK's format and its own layer C |
| `[00-the-store-layer-reads-inside-a-fingerprint]` | 04 | The sidecar reader and the CLI walk `classes`, which D3 makes the fingerprinter's |
| `[02-the-sidecar-readers-guards-are-unpinned]` | 04 | No test pins the reader's `bool` guard on `sidecar_format` or its full match on `store_id` |
| `[00-package-prose-names-sgk]` | 05 | Docstrings cite SGK's campaigns, and the CLI points at SGK's `main.py --inventory` |
| `[02-the-ported-tests-name-sgk]` | 05 | The ported tests and shard fixtures carry SGK's tables, store stems, driver path, `TestLiveA3Shape` and campaign citations |
| `[00-the-shard-fixtures-reach-into-shardedpool]` | none | The carried shard fixtures set private `ShardedPool` attributes |
| `[00-a-refusal-matches-datastorekit-message-text]` | none | An unreadable store is recognised by matching DatastoreKit's message text |
