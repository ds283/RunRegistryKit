# Campaign index

One line per campaign under `prompts/`. It is an index: the campaign's `README.md` holds the plan
and its `IMPLEMENTATION_STATE.md` the status; if this file and a board disagree, the board is
right.

**Last updated:** 2026-10-15 · 1 campaign: 1 live.

| Campaign | Status | Opened → last board update | Owns | Open issues |
|---|---|---|---|---|
| [`extraction`](extraction/IMPLEMENTATION_STATE.md) | **live** 2026-10-15: 5 of 9 prompts written (01–03, 04a, 04b; 04 split into 04a and 04b), 5 landed and reviewed (01, `4e0d715`: the package imported, suite 3; 02, `8155445`: the 108-test suite ported; 03, `035e4b5`: the client root and `runregistrykit.toml`, suite 135; 04a, `c81ad06`: the client fingerprinter, layer C deleted, the neutral store, suite 186; 04b, `5302a6f`: the retire tests ported, `store retire` loading the fingerprinter first, the loader refusing a class, suite 245); G1 holds on the source side (SGK `a45aefc`) and on the package side for 01's and 02's files, the check retired at 03; E1 holds (DatastoreKit `v0.4.0`); U1–U9 taken 2026-10-14, U14 2026-10-15 | 2026-10-14 → 2026-10-15 | moving SGK's `RunRegistry/` into `runregistrykit`; the client config and root rule; the client fingerprinter; the release `v0.1.0`; the clients' adoption checklists (SGK's E2) | §1.1; 4 |
