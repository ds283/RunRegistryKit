# Campaign — extraction

**Written:** 2026-10-14 by Claude Opus 5.5, at the user's request, from SecondaryGWKit's brief
[`runregistrykit-extraction-brief.md`](https://github.com/ds283/SecondaryGWKit/blob/handover-remedial/prompts/runregistry-extraction/runregistrykit-extraction-brief.md)
(SGK `prompts/runregistry-extraction/`, written 2026-10-12 at SGK `c8a7f14`) and from read-only
measurements made the same day (§0.2). The brief is evidence, not a specification: where it and
§0.2 disagree, §0.2 says so and is right for this tree. The user's rulings carried in from SGK are
§6.1; the decisions this campaign needs are §6.2. The user took U2 and U3 on 2026-10-14, as
recommended, for 01, U4 for 02, U5 and U9 for 03, U6, U7 and U8 for 04, U14 for 04b, U10, U11, U12, U15 and U16 for 05, and U17 for 05b. **Prompts 01
(`4e0d715`), 02 (`8155445`), 03 (`035e4b5`), 04a (`c81ad06`), 04b (`5302a6f`), 05a (`14af805`), 05b
(`1120fb3`) and 05c (`a7d93d5`) have landed and been reviewed; 04 is split into 04a and 04b, and
05 into 05a, 05b and 05c** (§2.1).

## 0. Why this campaign exists

SecondaryGWKit (SGK) built `RunRegistry/` for its long jobs. A job that takes hours must not be
something a conversation owns, and SGK's `prompts/run-registry` README §0 records the five
failures, in one working session, that each of its rules answers. The registry grew from there:
a sidecar beside each datastore saying which runs made it, the store operations that keep that
record true (create, adopt, copy, move, retire, amend), and a fingerprint of a store's content taken
when a run finishes and checked before a store is retired.

ChamPBH (CPBH) and StochasticInstantons (SI) need the same thing and have nothing like it (§0.2).
On 2026-10-12 the user decided that the registry moves to a repository of its own (SGK's D1), as
the datastore layer moved to DatastoreKit and the work queue to RayPoolKit. This campaign is that
move: SGK's `RunRegistry/` imported as the package `runregistrykit`, made generic, released, and
measured against each client in an adoption checklist.

### 0.1 What "extraction" means here

The move is not a copy. SGK's audit (`docs/runregistry-extraction-audit.md` §2) found nine places
where the registry assumes it lives in SGK (C1–C9, §0.2), and the user settled the one design
question they raise, the fingerprint (SGK's D3):
- **what goes into a fingerprint** stays in the client: its factories' `inventory_spec()`s, its
  registry, and its format number, in one client module;
- **how it is encoded and digested** is DatastoreKit's, since `v0.4.0`
  (`datastorekit.store_fingerprint`, with `ENCODING_FORMAT` recorded beside the digest);
- **when and where a fingerprint is taken and recorded** is this package's. It is handed a
  client-provided fingerprinter and treats the fingerprint as opaque, apart from a few named
  fields (§6.2, U7). A client without a fingerprinter cannot use the store layer (SGK's D4).

The plan imports SGK's code **faithfully first** (01, 02), so that the import is checked against
SGK's frozen tree line by line (G1), and then makes it generic **one coupling at a time**, each in a
prompt of its own whose diff is reviewable against a pinned baseline (03–05). Only the generic
package is released (06, `v0.1.0`): the faithful import cannot run installed (C1 would write run
records into the venv, and C6 imports a client), so it is never tagged (U3). The checklists (07) are
measured against that release, and SGK's E2 is that release with SGK's checklist.

### 0.2 Measurements taken by the planner (2026-10-14, read-only)

Taken by reading SGK, DatastoreKit, ChamPBH and SI through `git` and their working trees, and by two
probes in a scratch directory. Nothing in any of the four was changed or run beyond `--version`,
`pip freeze` and unittest discovery counts.

**The source.** SGK's `RunRegistry/` at the **import commit `a45aefc`**
(`a45aefc702de643c330372dd6d2d983f38bb8eed`, SGK's `runregistry-extraction` prompt 01, which froze
it). `git ls-tree -r a45aefc -- RunRegistry/` has 25 rows and equals SGK's frozen-tree table
(`prompts/runregistry-extraction/IMPLEMENTATION_STATE.md` §2.1) path for path and blob for blob, and
`RunRegistry/` and `StoreFixtures/` are unchanged from SGK `c8a7f14` (where the brief was measured)
through `a45aefc` to SGK's HEAD, `14bcac0`. So **G1 holds on the source side** (§7), and every line
number the brief took at `c8a7f14` holds at `a45aefc`. The tree is black-clean under 25.1.0.

| File | Lines | What it is |
|---|---|---|
| `RunRegistry/__init__.py` | 710 | the core: `begin`, `Run` (`heartbeat`, `finish`, `record`, `known`), `list_runs`, liveness, provenance |
| `RunRegistry/stores.py` | 2185 | the store layer: the sidecar; create, adopt, copy, move, fingerprint, retire, amend |
| `RunRegistry/__main__.py` | 515 | the CLI: `list`, and `store show / create / adopt / copy / move / fingerprint / retire / amend` |
| `RunRegistry/tests/` | 14 test modules, `store_fixtures.py`, six golden files | 286 tests by discovery |

The three modules refer to each other only relatively (`from . import …`, `from .stores import …`).
`RunRegistry` appears as a word in 23 lines: docstrings, error messages that say
`python -m RunRegistry …` (`stores.py:544, 1025, 1537-1538, 1694, 1758, 1810, 1876, 1907, 2119`),
and `prog="RunRegistry"` (`__main__.py:373`).

**Imports.** `__main__.py` imports only the standard library and the package. `__init__.py` imports
`.stores` lazily, twice: in `Run._fingerprint_results` (`:410`) and in `begin()` when `results` is
given (`:614`; the brief names only the first). `stores.py` imports nothing outside the standard
library at module scope, and lazily: `datastorekit.SQL.ShardedPool` (`:1084, 1121, 1814`),
`datastorekit.store_inventory.canonical_json` (`:1197, 1383`) and `read_inventory` (`:1493`), and
**`config.datastore.factories`** (`:1494`). `import RunRegistry` loads neither `ray` nor
`sqlalchemy`.

**The couplings to SGK** (the brief's C1–C9, each re-read at `a45aefc`; the brief's lines hold):

| # | Where | What it assumes |
|---|---|---|
| C1 | `REPO_ROOT`, `__init__.py:57`; used at `:98, 179-180, 185`, `stores.py:132, 185` | the root is the package's parent directory. Installed in `site-packages`, that is inside the venv |
| C2 | `DEFAULT_ROOT`, `__init__.py:58`; used at `__init__.py:608, 681`, `stores.py:911, 940, 1741`, and as argparse defaults evaluated at import, `__main__.py:376, 388-390` | `var/runs` under C1 |
| C3 | `DEFAULT_STORES_ROOT`, `stores.py:185`; used at `:1742`, `__main__.py:452-455` | `var/datastores` under C1 |
| C4 | `_repo_path`, `_resolve`, `__init__.py:176-185`; used at 5 sites in `__init__.py` and 16 in `stores.py` | paths in records are relative to C1. **Unchanged in meaning, this keeps every existing record readable** |
| C5 | `RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")`, `__init__.py:119`; pinned by `test_run_registry.py:393-396` | SGK's two packages |
| C6 | `from config.datastore import factories`, `stores.py:1494` | SGK's registry |
| C7 | `FINGERPRINT_FORMAT = 6` and its history, `stores.py:194-206` | SGK's format |
| C8 | docstrings and comments citing SGK: 21 lines in `__init__.py`, 28 in `stores.py`; and SGK's A3 store, `realistic_large_x`, `main.py` and SGK class names in prose (`__init__.py:71, 75, 352, 355, 435, 484, 492, 568, 596`; `stores.py:101, 198-205, 1609, 1619, 2024`) | SGK's `prompts/` is at hand |
| C9 | `git_provenance(cwd=REPO_ROOT)`, `__init__.py:98`; every call takes the default (`__init__.py:649`; `stores.py:833, 893, 1101, 1140, 1499, 1921, 2164`) | the package's own git tree |

**Couplings the brief does not list** (measured 2026-10-14):
- **SGK's `main.py` in output.** `__main__.py:281` prints "the store's own text is in
  `main.py --inventory`".
- **DatastoreKit's message text.** `stores.py:1567-1568` recognises an unreadable store by matching
  `_SHARDS_TABLE_UNREADABLE = "its shards table could not be read"`, the text of DatastoreKit's
  `ShardedPool._read_closed_store` (`SQL/ShardedPool.py:2779` at `v0.4.0`). A rewording there would
  change behaviour here without an error.
- **The store layer reads inside a fingerprint.** The brief (§3) has this package read only the
  format, the version, the digest and the comparison's entries. Today it reads more:
  `_fingerprint_problems` (`stores.py:416-436`, called by the sidecar reader at `:630`) requires a
  `classes` object and a `taken` object; `fingerprint_store` builds `taken` (`:1500-1508`) and calls
  the private `_difference` of layer C (`:1519`); `retire_store` reads `digest` and `taken.when`
  (`:1887-1894`); `__main__._print_fingerprint` (`:267-287`) walks `classes`, `tag_sets` and
  `problems`; `__main__._fingerprint` (`:307-327`) reads `taken` and `digest`.
- **Every SGK sidecar's fingerprint lacks `encoding_format`.** SGK's 18 sidecars are all tombstones
  (SGK board §3, 2026-10-14), and a tombstone is never fingerprinted again. But `store show` must
  still read each "as it did" (SGK's prompt 06, acceptance 3), so the sidecar reader must not
  require `encoding_format` (U7).

**Layer C**, the code DatastoreKit took over at `v0.4.0`, is `stores.py:1152-1399` (the brief says
`1164-1390`; `listing_lines` ends at `:1399`): `_sha256_lines`, `_tag_sets`, `fingerprint_of`,
`_tags_text`, `_difference`, `_presence`, `compare_fingerprints`, `listing_lines`. Inside the
registry, `fingerprint_of` is called at `:1500`, `compare_fingerprints` at `:1529`, `_difference` at
`:1519`, and `listing_lines` at `:1432` (`write_listing`, which `__main__.py:330` calls).

**The tests**, at `a45aefc` (discovery: 286; the brief's §5 counts hold):

| Class | Tests | Modules | Needs |
|---|---|---|---|
| **Core** | 29 | `test_run_registry` | the standard library and the package |
| **Store, shard fixtures** | 76 | `test_store_sidecar` 17, `test_store_copy_move` 27, `test_store_command_line` 2, `test_store_amend` 21, `test_store_amend_residuals` 9 | `store_fixtures.py` and SGK's `StoreFixtures/shard_store_fixtures.py` (168 lines), which import `datastorekit` and **set or call about 13 private `ShardedPool` attributes** (`:30-71`; `store_fixtures.assertOpens` two more, `:159-166`). `ray` must be installed; it is never initialised |
| **Store, a full SGK store** | 78 | `test_store_retire` 41, `test_store_retire_references` 10, `test_store_fingerprint` 27 | SGK's `StoreFixtures/real_store_fixtures.py` (1350 lines), which imports SGK's `config` and `ObjectFactories` at module scope; so every test in these modules needs SGK to import, though 9 of them build no full store |
| **Fingerprint formats** | 2 | `test_store_fingerprint.TestFormats` | as the 78, by module |
| **SGK's own** | 101 | `test_build_rehearsal_scope` 28, `test_killed_handler` 26, `test_pipeline_adoption` 15, `test_prune_on_resume` 18, `test_quadsource_atol_sweep_prepare` 10; `TestGolden` 3, `TestDrivers` 1 | SGK's `docs/` drivers, `main.py`, SGK's golden fingerprint. **Not imported**: they stay in SGK (its prompt 06) |

The base classes chain: `store_fixtures.StoreTestCase` builds on
`test_run_registry.RegistryTestCase`, and `test_store_command_line.CommandLineTestCase` is the base
of the amend, retire and fingerprint tests. Tests that start a child process use `cwd=REPO_ROOT`
and `PYTHONPATH=REPO_ROOT` (`test_run_registry.py:179, 226, 681`; `test_store_command_line.py:57-62,
172`; `test_store_amend.py:636`; `test_store_retire.py:1215`), and five assertions compute paths
relative to `REPO_ROOT` (`test_store_retire.py:241`; `test_store_retire_references.py:68, 112, 124,
141`). One assertion partitions on the text `` Run `python -m RunRegistry store retire ``
(`test_store_retire.py:198`).

**DatastoreKit `v0.4.0`** (`c8570e8`, tag object `8e7c1d7`; DatastoreKit's HEAD `b01737f` differs
only under `prompts/`):
- `datastorekit.store_fingerprint`: `ENCODING_FORMAT = 1`;
  `fingerprint_of(inventory, fingerprint_format, taken=None) -> dict`, whose six keys are
  `fingerprint_format`, `encoding_format`, `classes`, `digest`, `problems`, `taken`, with only the
  first and `classes` inside the digest; `compare_fingerprints(recorded, current) -> list` of
  `{kind, class, tags, recorded, current, text}`, which compares the two versions first and, if
  either differs or is absent on one side, returns only that entry; `listing_lines(inventory,
  fingerprint)`, which raises `KeyError` on a fingerprint without `encoding_format`. No name is
  exported from `datastorekit/__init__.py`.
- `datastorekit.store_inventory.read_inventory(primary, factories) -> StoreInventory` reads a
  **closed** store read-only, given a plain mapping of factories. It needs no open pool and starts
  no Ray, though `ray` must be installed.
- **The wheel ships no test code**: no neutral client, no stand-in pool, no store fixture. SGK's
  brief asked, as advice, for a fixture this package could use; DatastoreKit's `fingerprint` README
  §1 declined it ("RunRegistryKit … can write its own small neutral factories"; "If it asks, that is
  a separate request").
- **A fingerprintable store needs no client and no private API.** A 96-line scratch probe built one
  from public names only (`SQLAFactoryBase`, `InventorySpec`, `Parent`, the `TAG_*` names of
  `datastorekit.contract`, `build_schema`, `shard_file_name`): four neutral factories, shards made
  with `create_all`, a primary written with `sqlite3` holding `shards` and `replicated_tables`.
  `read_inventory`, `fingerprint_of`, `compare_fingerprints` and `listing_lines` all ran on it, Ray
  was never initialised, the same content under other serials compared empty, and a fingerprint
  without `encoding_format` gave one `encoding` entry. Such a primary is not one `ShardedPool`'s
  constructor reopens.
- The entry points the store layer calls are unchanged from `v0.2.2` to `v0.4.0`
  (`ShardedPool.copy_store`, `move_store`, `closed_store_files`, `delete_store`, all static).
- CI tests two ends: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, and 3.13.16 / 2.55.1 / 2.0.46.
  Its guard against naming a client reads a vocabulary measured from the three clients
  (`datastorekit/tests/data/client_vocabulary.json`), in which `RunRegistry` is one of SGK's
  packages.

**The clients:**

| Client | HEAD (2026-10-14) | Python | `datastorekit` / `raypoolkit` | Specs | Registry | Its migration |
|---|---|---|---|---|---|---|
| SGK | `14bcac0` (`handover-remedial`) | 3.12.15 | `v0.4.0` / `v0.2.0` | 21 of 38 classes, the rest read through an owner | `RunRegistry/`, frozen | `runregistry-extraction`, 01–04 landed; 05–09 held on this campaign's release (its E2) |
| CPBH | `61e0c42` (`surfing-temperature`) | 3.13.16 | `v0.4.0` / `v0.2.0` | 17 factories with `inventory_spec()`, coverage tested (`ObjectFactories/tests/test_inventory_specs.py`) | none; `CLAUDE.md:115-117` says so | `dk-and-rpk-migration` closed 2026-10-13 |
| SI | `5fb4a1d` (`dk-and-rpk-migration`) | 3.13.16 | neither pinned yet | none (20 old-style `inventory()` hooks) | none | `dk-and-rpk-migration` open: 01 and 01a landed; 10, which writes the specs, not yet written |

CPBH and SI each carry `utilities.installed_package_provenance` (`utilities.py:177`), written in
the shape of SGK's `package_provenance()` so that adopting this package is a substitution. Neither
has a `pyproject.toml` with a `[project]` table (SI's holds only pytest settings).

## 1. Scope

**In scope:**
- the package `runregistrykit`: SGK's three modules, imported at `a45aefc` (01);
- `pyproject.toml`, with the store layer as the extra `[stores]` (SGK's Q4); `PROVENANCE.md`;
- the 105 core and shard-fixture tests ported (02), and the 80 that need a fingerprintable store
  ported onto a neutral one of this package's own (04);
- the root found from where a run starts, and a client config file at that root (03: C1–C5, C9;
  SGK's Q2, Q3);
- the client fingerprinter, layer C deleted, and the fields the package reads of a fingerprint
  (04: C6, C7; SGK's D3, D4);
- the package's prose and output made its own, the rules of the registry stated in its README, and
  a guard that the package names no client (05a–05c: C8);
- the supported versions, CI, and the release `v0.1.0` (06);
- the three clients' adoption checklists, measured against `v0.1.0` (07);
- a verification document, and the campaign closed (08).

**Out of scope:**
- **any edit to SGK, CPBH, SI, DatastoreKit or RayPoolKit.** Each client adopts in a campaign of its
  own; SGK's is `runregistry-extraction` 05–09. A defect found in DatastoreKit is recorded here and
  reported there (§5 rule 11);
- **any change to what the registry writes.** The manifest, `status.json`, `checkpoint.jsonl` and
  `sidecar_format` 1 are carried as they are. Two records gain content, both ruled (SGK's brief §4):
  a fingerprint carries DatastoreKit's `encoding_format`, which DatastoreKit's function puts there;
  and `packages` names what the config says (U5, U9). **No manifest format field** (SGK's Q7), and
  **no reader of an older form** (SGK's standing rule): an old record is read as it is, or not at
  all;
- **SGK's 101 tests, SGK's golden fingerprints and SGK's format history.** They stay in SGK;
- **a fingerprint algorithm.** It is DatastoreKit's; this package calls a client's fingerprinter;
- **new features**: a manifest format field (proposed after the move, SGK's Q7), locking,
  scheduling, supervising or restarting a run. The registry records; it does not act.

## 2. Prompts

| # | Prompt | Covers | Model | Status |
|---|---|---|---|---|
| 01 | [`01-import-the-registry.md`](01-import-the-registry.md) | The package skeleton (`pyproject.toml`, `runregistrykit/`). SGK's `__init__.py`, `stores.py` and `__main__.py` at `a45aefc`, changed only by **D-name**: the word `RunRegistry` → `runregistrykit` in strings, docstrings and `prog` (U2). The client couplings C1–C9 are imported as they are, recorded on the board. `PROVENANCE.md`: the import commit, the file map, the fate of each of the 25 source files (imported now, ported by 02 or 04, or left in SGK), the differences allowed. `docs/extraction/compare_with_source.py` checks G1: SGK's 25 blobs against the frozen table, and every line of the three modules against its source, by rule. A test that `import runregistrykit` and `import runregistrykit.stores` load neither `ray`, `sqlalchemy` nor `datastorekit`. **Acceptance:** the check exits 0 and bites on named mutations; the package imports in a fresh interpreter with no client on the path. *(At writing: §2.5 of the prompt gives all 25 source files and the shard fixture a fate (4 imported by 01, 8 ported by 02, 3 by 04, 11 left in SGK); D-name touches 23 lines (6, 13, 4), and the renamed modules are black-clean; the import test has three tests.)* | Opus | landed and reviewed 2026-10-14 (`4e0d715`) |
| 02 | [`02-port-the-core-and-shard-fixture-tests.md`](02-port-the-core-and-shard-fixture-tests.md) | The 29 core and 76 shard-fixture tests, with `store_fixtures.py` and SGK's `StoreFixtures/shard_store_fixtures.py` carried into `runregistrykit/tests/` (U4). The changes allowed are D-name and the fixture's import path; the check of 01 is extended to them. The tests pin the imported behaviour, C1 and C5 included, as they stand. **Acceptance:** 105 tests (+01's) pass at the venv's versions; the check exits 0; `[00-the-shard-fixtures-reach-into-shardedpool]` measured against the carried file. *(At writing: in a git work tree, the eight files under D-name (83 lines), D-fix (5, the fixture's import path) and `black` give 108 tests OK; `black` reflows three lines of `test_store_copy_move.py`, so the check gains a D-fmt rule, the package equal to `black` of the renamed source; no 02 test reaches `[00-a-refusal-matches-datastorekit-message-text]`, which 04 inherits; the tests name SGK's tables, stores and campaigns, opened for 05.)* | Sonnet | landed and reviewed 2026-10-14 (`8155445`) |
| 03 | [`03-the-root-and-the-client-config.md`](03-the-root-and-the-client-config.md) | C1–C5 and C9. The **client config file** at the client's root, read with `tomllib`, which also marks the root (SGK's Q2; its form, U5). The **root rule** (SGK's Q3): a run is recorded under the main checkout, the parent of `git rev-parse --git-common-dir`, while its git SHA, dirty flag and script hash are its own tree's. The runs root, the stores root and the recorded distributions from the config, `runregistrykit` always recorded besides (U9). No config found is a refusal, never a fallback. C4's relative paths are kept, so every existing record reads as before. The child-process tests stop depending on the package's location; `test_run_registry.py:393` becomes a config test. Tests with temporary git repositories and worktrees. Closes `[00-the-root-is-the-packages-parent]` and `[00-the-recorded-distributions-are-sgks]`. *(At writing: no client has a `runregistrykit.toml`, and each has one worktree; every SGK `begin()` caller is two directories below SGK's root and passes `script=__file__`, one passing `root=` a temporary runs root, and no client imports `REPO_ROOT`, `DEFAULT_ROOT` or `DEFAULT_STORES_ROOT`; so the override is spelled `client_root=` / `--client-root`, `root=` keeping its meaning, the runs root. Provenance is the start directory's (the script's, else the working directory). The ported tests' fixtures build a client root in a `tempfile` directory, as a git repository, and run inside it, so no test body changes but 12 `_repo_path` calls, 4 child processes' `cwd`, and the two C5 tests, one renamed; `git` reports a worktree's paths realpath'd, so §2.4 compares realpaths. CPBH and SI do not ignore `var/`, for 07.)* | Opus | landed and reviewed 2026-10-14 (`035e4b5`) |
| 04a | [`04a-the-client-fingerprinter.md`](04a-the-client-fingerprinter.md) | C6 and C7, under SGK's D3 and D4. The **fingerprinter protocol** and a shipped `DatastoreKitFingerprinter`, named by `[stores] fingerprinter` (U6); the store layer refused without one (D4); layer C (`stores.py:1180-1427` at `f9e0e60`) and `FINGERPRINT_FORMAT` deleted; `fingerprint_store`'s discipline kept exactly. **What the package reads of a fingerprint** (U7), the reader's `classes` check dropped. The **neutral store** (U8). SGK's `test_store_fingerprint`, less `TestGolden` and `TestDrivers`: 27 tests and `TestFormats`' 2, each keeping its name and what it asserts, two variants of one test removed under U7. Closes `[00-the-fingerprint-reads-a-clients-registry]`, `[00-the-store-layer-reads-inside-a-fingerprint]` and `[02-the-sidecar-readers-guards-are-unpinned]`. *(At writing: DatastoreKit's comparison loops, texts, `classes` and `problems` are layer C's, by diff and by running both; its `fingerprint_of` requires the format, and its comparison gates on `encoding_format`, so every SGK fingerprint compared with a fresh one gives one `encoding` entry. A 120-line neutral store on public names was read by `read_inventory` and `ShardedPool`'s four static methods, at about 18 ms. The clients' registries are each a plain mapping, SGK's of classes, CPBH's and SI's of instances, and each client has a top-level `config` package. `store show` must not import the fingerprinter, which loads `ray` and `sqlalchemy`. SGK's test bodies name SGK's classes and tables, so the port renames them in constants and literals only, through a neutral store whose content keeps every asserted count and text.)* | Opus | landed and reviewed 2026-10-15 (`c81ad06`) |
| 04b | [`04b-the-retire-tests.md`](04b-the-retire-tests.md) | SGK's `test_store_retire` (41) and `test_store_retire_references` (10) on 04a's neutral store, each keeping its name and what it asserts, by the change classes of 02, 03 and 04a; among them the test that reaches `[00-a-refusal-matches-datastorekit-message-text]`'s match (`test_an_unreadable_shards_table`). And U14's two fixes: `store retire` loads the client's fingerprinter before it plans or fingerprints a first retirement, so a fingerprinter that cannot be loaded is a refusal and never a `--without-fingerprint` condition; and the loader refuses a class. Closes `[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]` and `[04a-the-loader-accepts-a-fingerprinter-class]`. *(At writing: a trial port, D-name 18, D-fix 1, N-fix 2 with a `compare_fingerprints` shim, N-class 1 (`QSI`), R-root 30, R-cwd 3 and `black`, into an export of `8880cfa`, gave `Ran 51 tests in 29.8s`, OK, with no F-client; rewording `_SHARDS_TABLE_UNREADABLE` fails `test_an_unreadable_shards_table`. Probed: with the config's fingerprinter naming a module that does not exist, or the class `DatastoreKitFingerprinter`, `retire_store(…, without_fingerprint=True)` retired a store that could be fingerprinted, recording the load error as the reason; hence U14.)* | Opus | landed and reviewed 2026-10-15 (`5302a6f`) |
| 05a | [`05a-the-guard-and-the-public-names.md`](05a-the-guard-and-the-public-names.md) | The **guard** that the package names no client (U10, U16): the three clients' vocabulary measured through `git` at fixed commits by `docs/extraction/measure_client_vocabulary.py` into a data file; a guard over every `*.py` under `runregistrykit/`, tests included, with four word scans (code names, strings, comments, campaign citations) and an import rule, each required to find exactly its known hits, listed by file and word in a second data file. **Public names** (U11): `_slug` becomes `slugify` (amended at dispatch from the prompt's `slug`, §6.2), and each module declares `__all__`, pinned. **The licence header** (U12) on the five package modules. No prose rewritten, no hit removed. *(At writing: SGK `14bcac0`, ChamPBH `c21cdfb`, SI `5fb4a1d` measured by a trial script (registry keys 38, 27, 30; columns 194, 80, 101; campaigns 26, 10, 6); a trial guard found 454 forbidden words and about 210 hits, 69 in the package modules (26 strings, 8 comments, 35 citations) and 140 in the tests; `version`, `store_tag`, `tag_serial` and `label` are `datastorekit.contract`'s and allowed; the imports conform; `_slug` is SGK's one private use.)* | Sonnet | landed and reviewed 2026-10-15 (`14af805`) |
| 05b | [`05b-the-package-prose-and-the-rules.md`](05b-the-package-prose-and-the-rules.md) | C8 and the SGK output in the five package modules: every docstring, comment and message rewritten in the package's own terms, SGK's history left to `PROVENANCE.md`; `main.py --inventory` replaced; the two docstrings 04b's log names. `README.md` gains **the rules of the registry**, each with the failure it answers (SGK's brief §6), and says that no patch target is promised (U11). The guard's citation scan widened (U17). Empties the package modules' known hits. Closes `[00-package-prose-names-sgk]`. *(At writing: 69 known hits in 30 entries on 44 lines of `__init__.py`, `stores.py` and `fingerprint.py`; a trial of U17's three forms (capital `Prompt NN`, a decision id, an issue tag) finds 11 more hits in the package modules and 18 in 11 entries in the tests, for 05c; the package's prose also cites a client's `README` 19 times and `CLAUDE.md` twice; about seventy lines in all; the one message is `describe`'s problems line, asserted by no test, and DatastoreKit `v0.4.0` has no inventory command; the README's stale "Status" paragraph is left to 06 by the user's ruling.)* | Sonnet | landed and reviewed 2026-10-15 (`1120fb3`) |
| 05c | [`05c-the-tests-own-names.md`](05c-the-tests-own-names.md) | The tests' SGK names and prose (U16): `TestLiveA3Shape`, `a3_shaped`, `sweep_shaped`, SGK's store stems and run names, the shard fixture's tables, the neutral store's shared columns, `test_package_imports.py`'s `FORBIDDEN`, and the citations; each rename mapped in `PROVENANCE.md`, every assertion kept. Empties the known hits. Closes `[02-the-ported-tests-name-sgk]`. *(At writing: 155 known hits in 94 entries in 14 test modules and fixtures; a fixed rename map of thirteen names (two helpers, a class, six test methods, two constants, three neutral-store columns), each checked against the guard's forbidden words; a trial of the renames, the neutral data and `FORBIDDEN` read from the guard's `project_packages()` (18 names, SGK's three among them) gave 276 tests with only the guard's three known-hit scans failing, leaving 75 hits, all in docstrings and comments; beyond the guard, an SGK campaign inside a run id, `QSI` and `TKN`, SGK's prompt property and test numbers, and a name the package no longer has; `known_hits.json` emptied with the mechanism kept, as DatastoreKit's guard did.)* | Sonnet | landed and reviewed 2026-10-15 (`a7d93d5`) |
| 06 | `06-release-v0.1.0.md` | Dependency ranges in `pyproject.toml` (`[stores]`: `datastorekit>=0.4.0` by name, SGK's brief §7). The suite at both ends locally, and with no `datastorekit` installed for the core (U13). A GitHub Actions workflow. `README.md` gains usage and installing. **Tag `v0.1.0`** on its commit once CI is green at both ends. | Sonnet | not written |
| 07 | `07-the-adoption-checklists.md` | `docs/adoption/`: a README and one checklist per client, measured read-only at a named client commit against `v0.1.0`. SGK's is E2's (SGK's brief §8.2): the config file with SGK's values, the fingerprinter's protocol and SGK's module, the public name for each SGK call site, the commands, and how to build SGK's Q5 guard. CPBH's and SI's (§8.3), each offering the Q5 pattern, and the substitution of `installed_package_provenance`. A script measures every client's call sites through `git` and `ast`. | Opus | not written |
| 08 | `08-verification-and-close-out.md` | `docs/extraction-verification.md` from the package at `v0.1.0` and the records of 01–07; a smoke run of the store layer end to end in a temporary client root at both ends; the campaign closed, with G2–G4 open. | Sonnet | not written |

**Order.** 01 → 02 → 03 → 04a → 04b → 05a → 05b → 05c → 06 → 07 → 08. 02 follows 01 so that the behaviour every later
prompt changes is pinned by tests first, as imported. 03 precedes 04 because the fingerprinter is
named in the config file that 03 creates. 05 follows 04 because the guard can pass only once C6
is gone. 07 is measured against `v0.1.0`, the release the clients adopt.

### 2.1 When each prompt file is written

One at a time, each after the one before it has landed and been reviewed, against the tree it left,
as RayPoolKit's and DatastoreKit's were. The charters above fix every prompt's task now; holding the
file back holds back only its method. Each prompt's file records what it found at writing in its row
above, in italics.

## 3. Datastores

**No prompt opens a client's store**, and no client code is imported or run. A measurement of a
client reads its files through `git` (07's checklists). The suite builds every store it needs in a
`tempfile` directory: from 02, through the carried shard fixtures; from 04, the neutral store too.
08's smoke run does the same.

## 4. The interfaces between prompts

**Fixed by this plan:**
- **The package** is `runregistrykit`, distributed as `runregistrykit` from this repository, with
  the extra `[stores]`; the CLI is `python -m runregistrykit` (SGK's Q1, Q4).
- **The module map:**

  | SGK at `a45aefc` | `runregistrykit` | By |
  |---|---|---|
  | `RunRegistry/__init__.py` | `runregistrykit/__init__.py` | 01 |
  | `RunRegistry/stores.py` | `runregistrykit/stores.py` | 01 |
  | `RunRegistry/__main__.py` | `runregistrykit/__main__.py` | 01 |
  | `RunRegistry/tests/__init__.py` | `runregistrykit/tests/__init__.py` | 01 |
  | `RunRegistry/tests/test_run_registry.py`, `store_fixtures.py`, and the five shard-fixture modules | `runregistrykit/tests/`, the same names | 02 |
  | `StoreFixtures/shard_store_fixtures.py` (not under `RunRegistry/`) | `runregistrykit/tests/shard_store_fixtures.py` | 02 |
  | `RunRegistry/tests/test_store_retire.py`, `test_store_retire_references.py`, `test_store_fingerprint.py` (less `TestGolden` and `TestDrivers`) | `runregistrykit/tests/`, the same names, on the neutral store | 04 |
  | `StoreFixtures/real_store_fixtures.py` | not imported: the neutral store replaces it | 04 |
  | the five driver-test modules, `TestGolden`, `TestDrivers`, `tests/data/*.json` | not imported: SGK's | — |
  | layer C, `stores.py:1152-1399`; `FINGERPRINT_FORMAT` and its history | deleted: DatastoreKit's functions, through the client's fingerprinter | 04 |

- **After 01:** `PROVENANCE.md`; `docs/extraction/compare_with_source.py`; the import test.
- **After 02:** the ported tests and fixtures; the check covering them. The suite count from here
  is recorded before and after every prompt.
- **After 03:** the config file's form, documented in the package; the root rule; the functions a
  client calls to find its root. 04 adds the fingerprinter's key to the same file.
- **After 04:** the fingerprinter protocol, in a module 07's checklists cite; the neutral store
  under `runregistrykit/tests/`.
- **After 05a:** the guard and its data; the public names the checklists use (`slugify`, `__all__`).
- **After 05b:** the package's prose its own; the README's rules.
- **After 05c:** the tests' names their own; the guard's known hits empty.
- **After 06:** `pyproject.toml` at `0.1.0`; `.github/workflows/tests.yml`; the tag `v0.1.0`.
- **After 07:** `docs/adoption/` and its script, which 08 cites. **E2 for SGK** is the tag with
  SGK's checklist.

**The equivalence check.** `compare_with_source.py` checks the package against SGK at `a45aefc`
through 02, when the package is the import. From 03 the package changes in its own right, so the
check is retired at 03's start and describes 02's tree, as RayPoolKit's was retired at its `v0.1.0`:
it is re-run from a worktree of 02's commit. `PROVENANCE.md` gains a "Since the import" section that
lists each prompt's changes from 03 on.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
4. **Do not fix things the prompt did not ask for.** A defect found in the imported code is
   recorded, with a §3 issue, and fixed by the prompt that owns it or by a later campaign.
5. **No prompt edits a client, DatastoreKit or RayPoolKit.** Reading them through `git` is allowed.
   Running a client's code or tests is not.
6. **No test needs a Ray cluster, imports a client, or creates anything outside a `tempfile`
   directory.** `ray` is installed with `datastorekit` and must never be initialised; the suite
   checks this. The suite count is recorded before and after each prompt; a count that falls, other
   than by a move the prompt names, is a stop.
7. **What the registry writes is an interface** (`CLAUDE.md`). No prompt changes the manifest,
   `status.json`, `checkpoint.jsonl` or the sidecar's form unless it says so; only U9's
   `packages` entry and the fingerprint's own `encoding_format` are planned.
8. **Equivalence with the source, through 02** (§4). Any difference outside the declared classes is
   a stop.
9. **Ported tests keep their module, class and method names and what they assert.** The changes
   allowed are listed by the prompt, as classes, and each instance is accounted for in its log. A
   test that cannot keep its assertion is a stop, not a rewrite. *From 05c (U16):* a ported test's
   module, class, method or helper name that names a client may be renamed, each rename mapped in
   `PROVENANCE.md`; what it asserts is still kept.
10. **Deliberate breakage.** Each prompt that adds code or a test names mutations its tests must
    catch. The log records each as a diff, exactly as applied, so the orchestrator can replay it
    with `git apply`. Mutations are never committed.
11. **A defect in DatastoreKit is not patched or worked around here.** The prompt stops and records
    it; the user reports it to DatastoreKit, where it is fixed in a release.
12. **No tag except where a prompt says so** (06: `v0.1.0`), made on the prompt's commit once CI is
    green there; none is moved or deleted.

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified;
- **Verification performed**: the suite count before and after; through 02, the output of
  `compare_with_source.py`;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Made by the user, and not reopened here

From SGK's audit §0 and §8 (2026-10-12), as carried by the brief, and this repository's set-up:

| | Decided |
|---|---|
| **D1** | The registry moves to **a repository of its own**, RunRegistryKit, not into DatastoreKit (whose charter is the standard library, `ray`, `sqlalchemy` and itself) |
| **D3** | **The fingerprint splits by layer.** The client says what goes into a fingerprint (its specs, its registry, its format number, in one client module); DatastoreKit encodes and digests it under a version of its own (`v0.4.0`); this package decides when and where a fingerprint is taken and recorded, is handed a client-provided fingerprinter, and treats the result as opaque apart from the format, the version, the overall digest and the differences a comparison returns |
| **D4** | **The store layer requires a fingerprinter.** No degraded mode without one. The core/store split is a dependency split only |
| **Q1** | Repository `RunRegistryKit`; distribution and package `runregistrykit`; CLI `python -m runregistrykit` |
| **Q2** | A client config file of its own at the client's root, read with `tomllib`, which also marks the root |
| **Q3** | A run launched from a git worktree is recorded in the main checkout (the parent of `git rev-parse --git-common-dir`); its git SHA, dirty flag and script hash are still the worktree's |
| **Q4** | One distribution, with the store layer as the optional extra `[stores]` |
| **Q5** | SGK builds a guard that a spec change without a format bump fails a test (SGK's prompt 07); this package's checklists offer the pattern to the other two clients |
| **Q7** | No format field is added to the run manifest during the extraction; proposed separately, after it |
| **U1** (2026-10-14) | The repository: `ds283/RunRegistryKit` on GitHub, **public**, as DatastoreKit and RayPoolKit (taken when the user asked for it to be created; a client installs the pin over plain `https`), checked out at `/Users/ds283/Documents/Code/RunRegistryKit`, Apache 2.0 |

### 6.2 Decisions this campaign needs

Each is put with a recommendation, the recommended option first. **U2 and U3 were taken by the user
on 2026-10-14, for 01, U4 the same day, for 02, U5 and U9, for 03, U6, U7 and U8, for 04, U14 on
2026-10-15, for 04b, U10, U11, U12, U15 and U16 the same day, for 05, and U17, for 05b, each as recommended**; the recommendation below is the decision. The others are put when the prompt that needs them is written.

- **U2: the import** *(for 01)*. (a) **Faithful**: SGK's three modules at `a45aefc`, changed only by
  the package's name (D-name), with C1–C9 left as they are and opened as §3 issues, each owned by a
  later prompt; or (b) **generic at import**, C1–C9 resolved in the import commit, as DatastoreKit's
  01 internalised its two client dependencies. *Recommended:* (a). G1 is then checked line by line
  by a script, as RayPoolKit's was; every generic change (03–05) is a diff from a tested baseline
  that a reviewer can read against SGK's code; and C1–C9 are design changes, not internalisations,
  so they deserve prompts of their own. *Taken 2026-10-14, for 01: (a).*
- **U3: the releases** *(for 01, since it sets the version)*. (a) **One release, `v0.1.0`, at 06**,
  the generic package; 01 sets `0.1.0.dev0`; or (b) RayPoolKit's two: `v0.1.0` the faithful import,
  then `v0.2.0` generic. *Recommended:* (a). The faithful import cannot run installed: C1 puts
  `var/runs/` inside the venv, and C6 imports a client. A tag no client can use would only be a
  second baseline, and 02's suite already pins the import's behaviour. *Taken 2026-10-14, for 01:
  (a).*
- **U4: the shard fixtures** *(for 02)*. SGK's `shard_store_fixtures.py` builds and reopens stores
  through about 13 private `ShardedPool` attributes. (a) **Carry it as it is**, with
  `[00-the-shard-fixtures-reach-into-shardedpool]` open, and DatastoreKit pinned exactly in CI so
  that a change there is seen; or (b) rewrite it on public names in 02. *Recommended:* (a), for 02's
  faithfulness. The coupling affects only this package's tests, never a client; whether to ask
  DatastoreKit for a public way to write and reopen a small store is §8's. *Taken 2026-10-14, for 02:
  (a).*
- **U5: the config file** *(for 03)*. *Recommended:* `runregistrykit.toml` at the client's root,
  with `runs_root` (default `var/runs`), `stores_root` (default `var/datastores`) and
  `distributions` (default none), and a `[stores]` table that 04 gives the fingerprinter's key.
  The root is found by walking up from the script `begin()` is given, or from the working directory
  for the CLI, to the first directory holding the file; an explicit `root` argument and `--root`
  option override it. No file found is a refusal that says what to create. Then Q3's rule. To be
  re-measured against the three clients' layouts when 03 is written. *Taken 2026-10-14, for 03, as
  recommended; re-measured at 03's writing, with one reading: the explicit override is spelled
  `client_root=` and `--client-root`, because `begin(root=…)`, `list_runs(root=…)` and `list
  --root` already name the runs root and keep that meaning (prompt 03 §2.3).*
- **U6: the fingerprinter** *(for 04)*. *Recommended (re-measured at 04's writing):* a
  `typing.Protocol` in the package, with operations to take a closed store's fingerprint given the
  `taken` stamp, compare two, describe one as lines for `store fingerprint`, and yield a listing;
  and a ready-made `DatastoreKitFingerprinter(factories, fingerprint_format)` over DatastoreKit's
  functions, in `[stores]`, which each client instantiates in a module of its own, named in the
  config by `[stores] fingerprinter = "module:attribute"` and imported with the client's root first
  on `sys.path`. At planning the recommendation was the protocol alone, each client writing its own
  about thirty lines. Measured at 04's writing: the three clients' registries are each a plain
  mapping (SGK's of classes, CPBH's and SI's of instances), so the wiring would be the same three
  times; the package's tests need exactly that object as their stand-in, so shipping it means the
  suite tests the code clients run; and it reads no `StoreInventory` shape the protocol does not
  already hand it, the object stays client-provided (D3), and a client with other needs writes its
  own. *Taken 2026-10-14, for 04 (prompt 04a §2.2), as re-recommended.*
- **U7: what the package reads of a fingerprint** *(for 04)*. *Recommended:* `fingerprint_format`,
  `encoding_format` and `digest`; `taken`, which the package builds and hands to the fingerprinter;
  and each comparison entry's `kind` and `text`. The sidecar reader's shape check becomes: an
  object, an integer format, a 64-hex digest, an object `taken`. **It does not require
  `encoding_format`**, so that every SGK tombstone reads as it did; a comparison that meets a
  fingerprint without one gets the fingerprinter's `encoding` entry, which is DatastoreKit's
  behaviour, not a reader of an older form. `classes`, `tag_sets` and `problems` are printed only
  through the fingerprinter's description. Measured at 04's writing: SGK's
  `test_each_malformed_fingerprint_is_a_problem` asserts that a fingerprint without `classes`, or
  with `classes` a list, is a problem; its two variants are removed, the one named exception to §5
  rule 9 this decision makes, because they assert the check U7 removes. *Taken 2026-10-14, for 04
  (prompt 04a §2.6), as recommended, with that exception.*
- **U8: the neutral store** *(for 04)*. *Recommended:* a small set of neutral factories and a store
  writer of this package's own, on public `datastorekit` names only (as §0.2's probe), under
  `runregistrykit/tests/`. Where a ported test needs a store that `ShardedPool` reopens, the carried
  shard fixtures provide it (U4). Measured at 04's writing: a store so built is read by
  `read_inventory` and by `ShardedPool`'s static `copy_store`, `move_store`, `closed_store_files` and
  `delete_store`, which is all the 80 tests need; none reopens one with the constructor. *Taken
  2026-10-14, for 04 (prompt 04a §2.7), as recommended.*
- **U9: `runregistrykit` in `packages`** *(for 03)*. *Recommended:* always recorded, besides the
  config's `distributions` (SGK's brief, advice on C5), so that every manifest says which release
  of the registry wrote it. *Taken 2026-10-14, for 03.*
- **U10: the guard's vocabulary** *(for 05)*. *Recommended:* the three clients' top-level packages
  and modules, SGK's run-registry words (`RunRegistry`, `StoreFixtures`, SGK's campaign and store
  names found in §0.2's C8), measured by a script into a data file as DatastoreKit's is, plus an
  import rule: the standard library and the package, and `datastorekit` only inside `stores.py`'s
  functions. *Taken 2026-10-15, for 05a (prompt 05a §2.2, §2.3), as recommended, measured at that
  prompt's writing: registry keys, identifier columns, packages and campaigns of the three clients,
  the words that cannot be measured listed with their source, `datastorekit.contract`'s words
  allowed; a citation scan; the import rule.*
- **U11: public names for what clients reach into** *(for 05)*. SGK's `stage_counts.py` uses the
  private `_slug`; SGK's `sigterm_handler_probe.py` monkeypatches `stores.fingerprint_store` through
  the lazy import at `__init__.py:410`. *Recommended:* export what a client needs under a public
  name before the release, and state in 07's checklists what a client should use for each; no
  promise about patch targets. *Taken 2026-10-15: `_slug` becomes `slug` and each module declares
  `__all__` (05a §2.4); the fingerprint names stay in `runregistrykit.fingerprint`; the README says
  no patch target is promised (05b). **Amended 2026-10-15, at 05a's dispatch, by the user:** the
  public name is `slugify`, not `slug`. `run_id(campaign, prompt, slug, when=None)` has a parameter
  named `slug`, which would shadow a function of that name inside `run_id`, and `slug` is
  `begin()`'s keyword, so a client's code nearly always has a local of that name. No signature
  changes; the prompt's `slug` is read as `slugify` (orchestrator note, correction 2).*
- **U12: the licence header** *(for 05)*. *Recommended:* the Apache 2.0 header CPBH and SI carry, on
  every package module but the tests, as RayPoolKit's U11. *Taken 2026-10-15, for 05a (§2.5).*
- **U13: supported versions and CI** *(for 06)*. *Recommended:* `requires-python = ">=3.12"`; no
  core dependency; `[stores]` = `datastorekit>=0.4.0`. Tested at DatastoreKit's two ends (Python
  3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, and 3.13.16 / 2.55.1 / 2.0.46), each with `datastorekit`
  installed from the tag `v0.4.0`; and a third job, the core's tests in a venv with no `datastorekit`,
  `ray` or `sqlalchemy`.
- **U14: the retire hazard and the loader's class check** *(for 04b)*. Measured at 04b's writing:
  since 04a `fingerprint_store` loads the client's fingerprinter, and `store retire
  --without-fingerprint` records any exception from it as the store's "without" condition and then
  deletes the store. So a config whose fingerprinter cannot be imported, or names the class
  `DatastoreKitFingerprinter` rather than an instance (which the loader accepts, the review of 04a's
  `[04a-the-loader-accepts-a-fingerprinter-class]`), lets a store that can be fingerprinted be
  retired under the flag. (a) **04b fixes both**, beside the port: `retire_store` loads the
  fingerprinter before it plans or fingerprints a first retirement, so a load failure is a refusal;
  and the loader refuses a class; each with a test and a mutation; or (b) a separate prompt 04c
  after 04b; or (c) 04b fixes the retire path only, the class check left for 05. *Recommended:* (a):
  both fixes are a few lines, the retire tests 04b ports are the ones that exercise the path, and
  no client runs the code yet. *Taken 2026-10-15, for 04b (prompt 04b §2.3, §2.4): (a).*
- **U15: 05 split** *(for 05)*. Measured at 05's writing, the charter is five parts (the guard and
  its vocabulary, the package's prose, the README's rules, the public names, the header), and with
  U16 the tests' names besides, about 210 guard hits in all. (a) **Three prompts**: 05a the guard,
  with today's hits listed as known, the public names and the header; 05b the package modules' prose
  and the README's rules, emptying their known hits; 05c the tests' names and prose, emptying the
  rest; or (b) two, the prose of both in one; or (c) one, on Opus. *Recommended:* (a): the guard
  first makes each later rewrite measurable, as DatastoreKit's 04b and 09 did, and each prompt is
  one kind of work. *Taken 2026-10-15: (a).*
- **U16: the tests in the guard's scope** *(for 05)*. The tests ship in the package, and carry SGK's
  names (`[02-the-ported-tests-name-sgk]`), some of which rule 9 keeps. (a) **The guard scans the
  tests, and their SGK names are renamed**: rule 9 is lifted for names only, from 05c, each rename
  mapped in `PROVENANCE.md`, every assertion kept; or (b) the guard scans the tests with a standing
  list of the names rule 9 keeps; or (c) it scans the package modules only, as DatastoreKit's.
  *Recommended:* (a): `CLAUDE.md` says the package names no client, and the port, now complete and
  reviewed, no longer needs SGK's names to be traced. *Taken 2026-10-15: (a).*
- **U17: the citation scan widened** *(for 05b)*. Measured at 05b's writing, 05a's citation scan
  misses three forms the package's prose uses: `Prompt` with a capital, a decision id (`D3`, `U14`)
  and an issue tag (`[10-…]`); 11 hits in the package modules and 18 in the tests. (a) **05b widens
  the scan**, with tests and mutations, removes the package's new hits in the same prompt, and
  lists the tests' 18 as known, for 05c; or (b) no widening, 05b's rewrite checked by a grep in its
  log; or (c) 05c widens it once both shares are empty. *Recommended:* (a): the rewrite of 05b and
  05c is then measured by the guard, not only read, and the gap does not outlive the campaign.
  *Taken 2026-10-15, for 05b (§2.2): (a).*

## 7. Gates outside this repository

| Gate | Holds when | Needed by |
|---|---|---|
| **G1** | The import equals SGK's frozen tree at `a45aefc`, file by file, apart from the differences this campaign allows and records. **Source side holds (2026-10-14):** SGK's 25 blobs equal its frozen table. The package side is 01's acceptance, and 02's for the tests it ports | 01, 02 |
| **E1** | DatastoreKit's fingerprint release, the floor of `[stores]`. **Holds (2026-10-14):** `v0.4.0`, `c8570e8`; SGK pinned it (its prompt 03) and rehearsed through it (its prompt 04, R1) | 04 |
| **G2** | SGK has adopted `v0.1.0` (its `runregistry-extraction` 05–08): `RunRegistry/` deleted, the pin installed, its roots pass, `list` gives its 29 runs, and its rehearsal R2 reproduces `39809dca…`. SGK's prompt 08 records it; its 09 drafts this board's record | — |
| **G3** | CPBH has adopted a release in a campaign of its own (07's checklist) | — |
| **G4** | SI has adopted a release, after its `dk-and-rpk-migration` closes (07's checklist) | — |

The campaign closes at 08. G2–G4 are recorded on this board as they hold, each in a records commit
of its own; the campaign does not wait for them. **E2**, SGK's gate on this campaign, is `v0.1.0`
with SGK's checklist (after 07): the tag, its commit and the checklist's path are reported to the
user then.

## 8. Later units of work

None is in this campaign's scope:
- **A manifest format field** (SGK's Q7), proposed once the three clients share the package.
- **A public way to write and reopen a small store** in DatastoreKit, which would let the carried
  shard fixtures drop their private `ShardedPool` attributes (U4), and **a typed exception** for an
  unreadable store, in place of matching its message
  (`[00-a-refusal-matches-datastorekit-message-text]`). Each is a request to DatastoreKit.
