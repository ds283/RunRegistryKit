# Campaign index

One line per campaign under `prompts/`. It is an index: the campaign's `README.md` holds the plan
and its `IMPLEMENTATION_STATE.md` the status; if this file and a board disagree, the board is
right.

**Last updated:** 2026-10-14 · 1 campaign: 1 live.

| Campaign | Status | Opened → last board update | Owns | Open issues |
|---|---|---|---|---|
| [`extraction`](extraction/IMPLEMENTATION_STATE.md) | **live** 2026-10-14: 3 of 8 prompts written (01–03), 3 landed (01, `4e0d715`: the package imported, suite 3, and 02, `8155445`: the 108-test suite ported, reviewed; 03, this commit: the client root and `runregistrykit.toml`, suite 135); G1 holds on the source side (SGK `a45aefc`) and on the package side for 01's and 02's files, the check retired at 03; E1 holds (DatastoreKit `v0.4.0`); U1–U5 and U9 taken 2026-10-14 | 2026-10-14 → 2026-10-14 | moving SGK's `RunRegistry/` into `runregistrykit`; the client config and root rule; the client fingerprinter; the release `v0.1.0`; the clients' adoption checklists (SGK's E2) | §1.1; 7 |
