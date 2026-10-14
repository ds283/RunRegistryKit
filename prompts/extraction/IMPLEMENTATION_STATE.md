# extraction campaign — implementation state

**Last updated:** 2026-10-14 · **Status: LIVE — 1 of 8 prompts written (01), 1 landed (01, this
commit; suite 3).** G1 holds on the source side at SGK `a45aefc`, and on the package side for 01's
files; E1 holds (DatastoreKit `v0.4.0`). U1 taken at set-up on 2026-10-14; U2 and U3 taken the same
day, for 01, as recommended (README §6.2).

**Campaign:** [`README.md`](README.md) ·
**Source:** SecondaryGWKit's `RunRegistry/` at `a45aefc`, 25 files (G1) ·
**Brief:** SGK's `prompts/runregistry-extraction/runregistrykit-extraction-brief.md` ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.1

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Made by the user (README §6.1):**

| Decision | Decided |
|---|---|
| **D1** | a repository of its own (SGK, 2026-10-12) |
| **D3** | the fingerprint split by layer; this package takes a client fingerprinter and treats the result as opaque but for named fields (SGK, 2026-10-12) |
| **D4** | the store layer requires a fingerprinter (SGK, 2026-10-12) |
| **Q1–Q5, Q7** | names; config file at the root; worktree runs recorded in the main checkout; one distribution with `[stores]`; the Q5 pattern offered; no manifest format field (SGK, 2026-10-12) |
| **U1** | public `ds283/RunRegistryKit`, Apache 2.0 (2026-10-14) |

**Put to the user (README §6.2):**

| Decision | Recommendation | Status |
|---|---|---|
| **U2** the import | faithful: only the package's name changes; C1–C9 later | **taken** 2026-10-14 |
| **U3** the releases | one release, `v0.1.0`, at 06; 01 sets `0.1.0.dev0` | **taken** 2026-10-14 |
| **U4** shard fixtures | carry SGK's as they are; issue open | open, for 02 |
| **U5** config file | `runregistrykit.toml`; found from the script or the working directory; none is a refusal | open, for 03 |
| **U6** fingerprinter | a protocol; named by `module:attribute`; each client writes its own | open, for 04 |
| **U7** what is read | versions, digest, `taken`, comparison `kind` and `text`; `encoding_format` not required to read | open, for 04 |
| **U8** neutral store | own factories and writer, public `datastorekit` names only | open, for 04 |
| **U9** self-record | `runregistrykit` always in `packages` | open, for 03 |
| **U10** guard | measured client vocabulary, and an import rule | open, for 05 |
| **U11** public names | for `_slug` and the like, before the release | open, for 05 |
| **U12** licence header | on every package module but the tests | open, for 05 |
| **U13** versions and CI | Python ≥3.12; `[stores]` `datastorekit>=0.4.0`; DatastoreKit's two ends, and a core job without it | open, for 06 |

## 1. Prompts

| # | Prompt | Model | Status | Commit | Suite |
|---|---|---|---|---|---|
| 01 | [`01-import-the-registry.md`](01-import-the-registry.md) | Opus | **landed** 2026-10-14 ([log](logs/01-import-the-registry.md)) | this commit | 0 → 3 |
| 02 | `02-port-the-core-and-shard-fixture-tests.md` | Sonnet | not written | — | — |
| 03 | `03-the-root-and-the-client-config.md` | Opus | not written | — | — |
| 04 | `04-the-client-fingerprinter.md` | Opus | not written | — | — |
| 05 | `05-the-package-prose-and-the-guard.md` | Sonnet | not written | — | — |
| 06 | `06-release-v0.1.0.md` | Sonnet | not written | — | — |
| 07 | `07-the-adoption-checklists.md` | Opus | not written | — | — |
| 08 | `08-verification-and-close-out.md` | Sonnet | not written | — | — |

**Written one at a time** (README §2.1), each after the one before it has landed and been reviewed.
The holds are for **method**, not scope: every charter is fixed in README §2.

### 1.1 Items

| Item | Prompt | What | State |
|---|---|---|---|
| **I1** | 01 | the package skeleton; the three modules under D-name | ✅ 2026-10-14: D-name on 23 lines (6, 13, 4), D-fmt 0; the import test, 3 tests |
| **I2** | 01 | `PROVENANCE.md`; `compare_with_source.py` (G1, package side) | ✅ 2026-10-14: the check exits 0 and bites on (a)–(i) |
| **T1** | 02 | the 29 core and 76 shard-fixture tests, and their fixtures | ⬜ |
| **R1** | 03 | the config file and the root rule (C1–C3, C9; Q2, Q3) | ⬜ |
| **R2** | 03 | the recorded distributions (C5, U9) | ⬜ |
| **F1** | 04 | the fingerprinter protocol; layer C and the format deleted (C6, C7) | ⬜ |
| **F2** | 04 | what the package reads of a fingerprint (U7) | ⬜ |
| **T2** | 04 | the neutral store; the 78 and `TestFormats`' 2 ported | ⬜ |
| **P1** | 05 | the prose, the output and the README's rules (C8) | ⬜ |
| **P2** | 05 | the no-client guard | ⬜ |
| **V1** | 06 | versions, CI, `v0.1.0` | ⬜ |
| **A1** | 07 | the three checklists and their script (SGK's E2) | ⬜ |
| **Z1** | 08 | the verification document; the close | ⬜ |

**Legend.** ⬜ not yet · ✅ done.

## 2. Gates (README §7)

| Gate | Status |
|---|---|
| **G1** | **source side holds** 2026-10-14: `git ls-tree -r a45aefc -- RunRegistry/` equals SGK's frozen table (its board §2.1), 25 rows; unchanged to SGK `14bcac0`. **Package side holds for 01's files** 2026-10-14 (this commit): `docs/extraction/compare_with_source.py` exits 0: the 25 rows and the shard fixture's blob equal; `__init__.py`, `stores.py`, `__main__.py` and `tests/__init__.py` equal their sources but for 23 D-name lines (6, 13, 4, 0), none unclassified, none left unrenamed; 11 files pending (8 for 02, 3 for 04); 11 not imported and absent; 1 declared new file. Package side for the ported tests: 02 |
| **E1** | **holds** 2026-10-14: DatastoreKit `v0.4.0` (`c8570e8`, tag object `8e7c1d7`) |
| **G2** | not yet (SGK adopts `v0.1.0` in its `runregistry-extraction` 05–08) |
| **G3** | not yet (CPBH adopts) |
| **G4** | not yet (SI adopts, after its `dk-and-rpk-migration`) |
| **E2** (SGK's) | not yet: `v0.1.0` (06) with SGK's checklist (07) |

## 3. Active and unresolved issues

All seven were opened at planning from README §0.2's measurements of SGK's code at `a45aefc`. Line
numbers are SGK's until 01 imports the code; 01 records each issue's package lines. **From 01 they
are the same numbers:** D-name replaced one line by one line and `black` changed nothing, so every
line of `runregistrykit/` sits where it sat in SGK at `a45aefc` (01's log; each line below read in
the package).

### `[00-the-root-is-the-packages-parent]`

**Opened:** 2026-10-14, at planning (C1–C3, C9). **Owner:** 03.

`REPO_ROOT` is the parent of the package's own directory (`__init__.py:57`); the runs root
(`DEFAULT_ROOT`, `:58`) and the stores root (`DEFAULT_STORES_ROOT`, `stores.py:185`) are `var/runs`
and `var/datastores` under it, and every `git_provenance()` call reads the git tree there (`:98`).

*Impact.* Installed in `site-packages`, the package would create `var/runs/` inside the venv, a
silent breach of the registry's durability rule, and record the venv's git state, if any, as the
run's. In SGK the same rule makes a run launched from a worktree record into the worktree (SGK's
`[00-a-run-launched-from-a-worktree-records-into-the-worktree]`).

*Next step.* 03: the root found from where the run starts and marked by the config file (SGK's Q2,
U5), records under the main checkout (Q3), provenance from the run's own tree.

*Package lines (01, 2026-10-14).* `REPO_ROOT` `runregistrykit/__init__.py:57`; `DEFAULT_ROOT` `:58`,
used at `:608, 681`, `runregistrykit/stores.py:911, 940, 1741` and as argparse defaults
`runregistrykit/__main__.py:376, 388-390`; `DEFAULT_STORES_ROOT` `stores.py:185`, used at `:1742` and
`__main__.py:452-455`; `_repo_path`/`_resolve` `__init__.py:176-185`; `git_provenance(cwd=REPO_ROOT)`
`__init__.py:98`, called with the default at `__init__.py:649` and `stores.py:833, 893, 1101, 1140,
1499, 1921, 2164`. In this repository's editable install `REPO_ROOT` is the repository's root.

### `[00-the-recorded-distributions-are-sgks]`

**Opened:** 2026-10-14, at planning (C5). **Owner:** 03.

`RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")` (`__init__.py:119`) is what every manifest's
`packages` records, and `test_run_registry.py:393-396` pins it.

*Impact.* A client that uses neither records two irrelevant entries, and one with other packages
cannot record them. The registry itself is not recorded.

*Next step.* 03: the config's `distributions`, with `runregistrykit` always recorded (U9); the
pinning test becomes a test of the config.

*Package lines (01, 2026-10-14).* `RECORDED_DISTRIBUTIONS` `runregistrykit/__init__.py:119`, the
default of `package_provenance` (`:122`). The pinning test is SGK's `test_run_registry.py:393-396`,
which 02 ports.

### `[00-the-fingerprint-reads-a-clients-registry]`

**Opened:** 2026-10-14, at planning (C6, C7). **Owner:** 04.

`fingerprint_store` imports `from config.datastore import factories` (`stores.py:1494`), SGK's
registry, and fingerprints with SGK's `FINGERPRINT_FORMAT = 6` (`:206`) through the package's own
copy of layer C (`:1152-1399`), which DatastoreKit holds since `v0.4.0`.

*Impact.* The store layer works only inside SGK; elsewhere `fingerprint_store`, `Run.finish(…,
fingerprint=True)` and `store retire` fail with `ModuleNotFoundError`. A second copy of layer C here
would drift from DatastoreKit's.

*Next step.* 04: the client fingerprinter (D3, U6), layer C and the format deleted.

*Package lines (01, 2026-10-14).* `from config.datastore import factories`
`runregistrykit/stores.py:1494`, inside `fingerprint_store` (`:1445`); `FINGERPRINT_FORMAT = 6`
`:206`, its history `:194-205`; layer C `:1152-1399` (`fingerprint_of` `:1182`, called `:1500`;
`compare_fingerprints` `:1256`, called `:1529`; `listing_lines` `:1376-1399`).

### `[00-the-store-layer-reads-inside-a-fingerprint]`

**Opened:** 2026-10-14, at planning. **Owner:** 04.

D3 has the package treat a fingerprint as opaque apart from its versions, its digest and the
comparison's entries. The imported code reads more: the sidecar reader requires `classes`
(`stores.py:416-436`, via `:630`); `fingerprint_store` calls layer C's private `_difference`
(`:1519`); `__main__._print_fingerprint` walks `classes`, `tag_sets` and `problems`
(`__main__.py:267-287`).

*Impact.* With layer C gone, those readers would bind the package to DatastoreKit's fingerprint
shape, which D3 rejected, and a DatastoreKit change to it would break `store show` here.

*Next step.* 04, under U7: the package reads only the named fields and `taken`; the rest is printed
through the fingerprinter.

*Package lines (01, 2026-10-14).* `_fingerprint_problems` `runregistrykit/stores.py:416-436`, called
by the sidecar reader at `:630`; `fingerprint_store` builds `taken` at `:1500-1508` and calls
`_difference` at `:1519`; `retire_store` reads `digest` and `taken.when` at `:1887-1894`;
`runregistrykit/__main__.py`: `_print_fingerprint` `:267-287`, `_fingerprint` reads `taken` and
`digest` at `:307-327`.

### `[00-package-prose-names-sgk]`

**Opened:** 2026-10-14, at planning (C8). **Owner:** 05.

49 docstring and comment lines cite SGK's campaigns (21 in `__init__.py`, 28 in `stores.py`), and
others name SGK's A3 store, `realistic_large_x`, `main.py` and SGK's classes (README §0.2). The CLI
prints "the store's own text is in `main.py --inventory`" (`__main__.py:281`), an SGK command.

*Impact.* A reader in this repository or a client cannot follow the citations, and CPBH and SI users
would be sent to a command they do not have.

*Next step.* 05: the prose in the package's own terms, SGK's history in `PROVENANCE.md`, the rules in
the README, and the guard (U10) so it stays that way.

*Package lines (01, 2026-10-14).* The SGK citations sit at README §0.2's C8 lines, now in
`runregistrykit/__init__.py` and `runregistrykit/stores.py`; the CLI text is
`runregistrykit/__main__.py:281`. D-name made one renamed comment cite a path that does not exist
here: `stores.py:197`, `runregistrykit/tests/data/full_store_fingerprint*.json` (01's log). And
`stores.py:1567`'s "(prompt 01's log)" means an SGK campaign's prompt 01 (the comment sits in the
section SGK's `store-retirement` campaign wrote), not this campaign's (01's log, observations).

### `[00-the-shard-fixtures-reach-into-shardedpool]`

**Opened:** 2026-10-14, at planning. **Owner:** none; 02 carries the fixture (U4) and records the
attributes it touches in the package.

SGK's `StoreFixtures/shard_store_fixtures.py`, which the 76 shard-fixture tests use, builds a
`ShardedPool` with `object.__new__` and sets or calls about 13 private attributes (`:30-71`), and
`store_fixtures.assertOpens` uses two more (`:159-166`).

*Impact.* Only this package's tests are affected, never a client. A DatastoreKit release that renames
one of those internals breaks the suite here with no change in the package's behaviour.

*Next step.* Pin `datastorekit` exactly in CI (U13), so that a change is seen when the pin moves. A
public way to write and reopen a small store would be a request to DatastoreKit (README §8).

*Package lines (01, 2026-10-14).* None yet: the fixture is pending, 02
(`runregistrykit/tests/shard_store_fixtures.py`, `store_fixtures.py`).

### `[00-a-refusal-matches-datastorekit-message-text]`

**Opened:** 2026-10-14, at planning. **Owner:** none.

The store layer recognises a store whose shards table cannot be read by matching the text
`_SHARDS_TABLE_UNREADABLE = "its shards table could not be read"` (`stores.py:1567-1568`) in
DatastoreKit's exception, raised by `ShardedPool._read_closed_store` (`SQL/ShardedPool.py:2779` at
`v0.4.0`).

*Impact.* A rewording in DatastoreKit would change how the store layer classifies a store, without
an error. The text is unchanged from `v0.2.2` to `v0.4.0`.

*Next step.* Keep a test that reaches the match at both tested ends (02 or 04, whichever ports it).
A typed exception would be a request to DatastoreKit (README §8).

*Package lines (01, 2026-10-14).* `_SHARDS_TABLE_UNREADABLE` `runregistrykit/stores.py:1567-1568`
(the comment and the assignment).

## 4. Resolved issues

None.
