# RunRegistryKit

A registry for long-running jobs. A job that takes hours must not be something a conversation, a
terminal or a person's memory owns. RunRegistryKit records that each one exists: a run directory
with a manifest written before the job starts, a heartbeat and a status while it runs, a
checkpoint log, and the provenance of the code that ran it (git SHA, dirty flag, script hash and
the versions of named distributions). `list` shows every run and whether it is alive, judged by
its pid and its heartbeat, never by matching a command line. An optional store layer keeps a
sidecar beside each datastore, saying which runs made it and recording its fingerprint, and
creates, adopts, copies, moves, fingerprints and retires stores under that record.

**Status: being extracted.** The code does not live here yet. It is the `RunRegistry/` package of
[SecondaryGWKit](https://github.com/ds283/SecondaryGWKit), which ChamPBH and StochasticInstantons
will adopt from here. The plan for moving it, making it generic and releasing it is
[`prompts/extraction/README.md`](prompts/extraction/README.md); its status board is
[`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md).

The core depends on nothing beyond the Python standard library. The store layer depends on
[DatastoreKit](https://github.com/ds283/DatastoreKit), the datastore layer extracted from the same
projects, which encodes and digests a store's fingerprint; what goes into the fingerprint is the
client's.

## Licence

Apache License 2.0; see [`LICENSE`](LICENSE).
