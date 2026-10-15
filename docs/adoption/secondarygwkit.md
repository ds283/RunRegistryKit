# Adoption checklist: SecondaryGWKit (SGK)

- **Client:** SecondaryGWKit, `/Users/ds283/Documents/Code/SecondaryGWKit`, at **`14bcac0`**
  (`14bcac0eb73069131f8ce4f55d91e5fc3e7318cf`, branch `handover-remedial`, 2026-10-14, "Say in the
  runregistry-extraction plan what 08 repeats of W1").
- **Tree:** clean at the start and at the end of the measurement (`git status --porcelain` empty,
  no stash, one worktree).
- **Package:** `runregistrykit` at **`v0.1.0`** (`9f8ebe4`), with `datastorekit` `v0.4.0`.
- **How it was measured:** read-only, by RunRegistryKit's extraction prompt 07 on 2026-10-15, through
  `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  [`measure_client_registry.py`](measure_client_registry.py) (the appendix). Nothing of SGK was
  imported, run or opened, and no store or run directory was read. **SGK's adoption campaign
  measures again before acting, and its numbers govern.**
- **This is data, not instructions.** It describes SGK at `14bcac0`. SGK's campaign
  (`runregistry-extraction` 05–08) decides what to do, under SGK's `CLAUDE.md`. A recommendation is
  marked **Advice:**; a choice that is SGK's is named as SGK's.

Unless another commit is named, a `path:line` is SGK's at `14bcac0`; one under `runregistrykit/` is
the package's at `v0.1.0` (`9f8ebe4`); and one under `RunRegistry/` is the same at `a45aefc` and
`14bcac0` (`git diff a45aefc 14bcac0 -- RunRegistry StoreFixtures` is empty).

**This checklist with `v0.1.0` is SGK's gate E2** on RunRegistryKit (its brief
`prompts/runregistry-extraction/runregistrykit-extraction-brief.md:134-155`). It covers what the
brief's §8.2 asks for (`:139-145`): the config file with SGK's values (item 3), the fingerprinter's
protocol and SGK's module (item 3), the public name for each call site (item 4), the commands
(items 4, 5 and 9), and how to build Q5's guard (item 8).

**In one paragraph.** SGK's `RunRegistry/` is the source of the package, so the names SGK's live
code uses are nearly all kept: 15 names in 13 imports in 10 files, of which one is renamed
(`_slug` → `slugify`), three moved to DatastoreKit (`fingerprint_of`, `compare_fingerprints`,
`listing_lines`) and one deleted (`FINGERPRINT_FORMAT`, which becomes SGK's). Every one of the
four `begin()` calls, and every call of a store operation, binds at `v0.1.0`. The four
`fingerprint_of` calls do not: DatastoreKit's `fingerprint_of` requires the format, which SGK's did
not take. The weight is in the 101 staying tests (item 7): they reach deleted names (`REPO_ROOT`,
`DEFAULT_ROOT`, `stores.DEFAULT_ROOT`), a private function whose signature changed (`_repo_path`),
a helper the wheel does not ship (`StoreTestCase`), and SGK's golden fingerprint, which lacks
`encoding_format`. Two of them redirect the drivers' runs root by patching a deleted name, and
need a decision of SGK's (item 7).

---

## 1. The client and its versions

- **Python 3.12.15** (`venv/pyvenv.cfg`, read as text: `version = 3.12.15`, MacPorts' 3.12
  framework); **`ray==2.43.0`** (`requirements.txt:75`); **`SQLAlchemy==2.0.39`** (`:87`);
  **`datastorekit @ …@v0.4.0`** (`:17`); `raypoolkit @ …@v0.2.0` (`:76`). Python, Ray and
  SQLAlchemy are exactly the package's tested low end, inside `requires-python = ">=3.12"` and
  `[stores]` = `datastorekit>=0.4.0` ([`README.md`](README.md) §1).
- **The pin it adds** (SGK's 05, in a commit of its own), with the extra, since SGK uses the store
  layer:
  ```text
  runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0
  ```
  SGK's `datastorekit` line at `:17` already satisfies the extra's floor, and stays as it is. An
  editable install of `runregistrykit` is never for SGK's production runs.

## 2. What it deletes

**`RunRegistry/`, 25 files** (SGK's 06), whose blobs at `14bcac0` equal those at `a45aefc` and the
frozen-tree table this repository's board records (its G1 row; `git ls-tree -r`, compared):

| File | Blob | Lines |
|---|---|---|
| `RunRegistry/__init__.py` | `0228a1a066793332191affe90c4b309a153aa60c` | 710 |
| `RunRegistry/__main__.py` | `88cf6ddd2b7603fc718fd6b3d7ed9722261a874f` | 515 |
| `RunRegistry/stores.py` | `a0f18ba49a25fe795af79baa8f82ce0e09cf3b25` | 2185 |
| `RunRegistry/tests/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | 0 |
| `RunRegistry/tests/data/full_store_fingerprint.json` | `58b35c3677f40e5421c7390ac282f1e6e808cd68` | |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-07.json` | `2fea28b072cd9f4cdb15062ab355c9c08a45d57e` | |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-08.json` | `511ff2d3873437480cbb6af028ba8fbdc5699b87` | |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09a.json` | `bd6a855c9d109a8da654ab790eadfc681ad5cea8` | |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09b.json` | `01d7ef02e88c53a4160e5660711f0746f3ae4a90` | |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09c.json` | `6cf0a39496c0e96bd3b2640324482e7d51686908` | |
| `RunRegistry/tests/store_fixtures.py` | `391f31fc2155c1f2d8f2350d306272ee6e0ae54e` | 223 |
| `RunRegistry/tests/test_build_rehearsal_scope.py` | `8b3c8519d3956b97cce84ea8224c621f37d88cd0` | 356 |
| `RunRegistry/tests/test_killed_handler.py` | `213f2a8d7d017f845b85ea209f8e87886539988b` | 578 |
| `RunRegistry/tests/test_pipeline_adoption.py` | `f3205799afa5626fe440e409fce37c1cb9fa04c7` | 386 |
| `RunRegistry/tests/test_prune_on_resume.py` | `23533e68f7682a172ecf7246b84bbd749b1e5ff8` | 387 |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | `527a9878d588309fd6f82f214bc655be627cea5d` | 319 |
| `RunRegistry/tests/test_run_registry.py` | `01c3ea37d8491c63300667f5a181f3bad91000ab` | 711 |
| `RunRegistry/tests/test_store_amend.py` | `8b7db110f76ae74bfb4716fe12d7192bac38265e` | 641 |
| `RunRegistry/tests/test_store_amend_residuals.py` | `0c6e6a2ca5d59b74dcb960111a5cd05ed2d991f4` | 267 |
| `RunRegistry/tests/test_store_command_line.py` | `6f111e29e9b695340a88bf19eb18a50e89a9ea05` | 183 |
| `RunRegistry/tests/test_store_copy_move.py` | `4be78d983aa83d5d7d39fc440519347cc87386bd` | 601 |
| `RunRegistry/tests/test_store_fingerprint.py` | `5039b4792210c1227230ec09b48da641b6f62e9f` | 875 |
| `RunRegistry/tests/test_store_retire.py` | `3cf05cc02d6b00849a4eff4972ccbedd0a4fa51d` | 1220 |
| `RunRegistry/tests/test_store_retire_references.py` | `9a3264a7f5977311161f724651b4e1d27cfa0866` | 192 |
| `RunRegistry/tests/test_store_sidecar.py` | `533d1118447527cfef65a833525516fcadbbc2e7` | 617 |

Before deleting, SGK's 06 moves out what stays SGK's (its README §2.2, 06): the five driver-test
modules and `TestDrivers` to `RunDrivers/tests/`, and `TestGolden` with the six golden files to
`ObjectFactories/tests/` (item 7). The format history in `RunRegistry/stores.py:194-205` moves to
`config/fingerprint.py` (item 3). The other 185 tests are this package's now, and are deleted with
the directory.

**`StoreFixtures/` is not deleted.** It is SGK's: `shard_store_fixtures.py` is what a copy of
`store_fixtures.py` builds on (`RunRegistry/tests/store_fixtures.py:20`), and
`real_store_fixtures.py` builds the store `TestGolden` fingerprints
(`RunRegistry/tests/test_store_fingerprint.py:50-57`).

## 3. What it adds

**`runregistrykit.toml` at SGK's root**, with the values SGK's brief asks for (`:140-142`) and its
06 charter names (its README §2.2, 06):

```toml
runs_root = "var/runs"
stores_root = "var/datastores"
distributions = ["datastorekit", "raypoolkit"]

[stores]
fingerprinter = "config.fingerprint:fingerprinter"
```

- `runs_root` and `stores_root` are the defaults; writing them is SGK's choice, and it says where
  SGK's 29 runs and its sidecars are.
- `distributions` gives every manifest `packages` = `runregistrykit`, `datastorekit`,
  `raypoolkit`, in that order (U9). Checked: this file, written in a temporary directory and read by
  `runregistrykit.find_client_root(client_root=…)`, gives `runs_root` and `stores_root` under that
  directory, `distributions` `('datastorekit', 'raypoolkit')`, `stores`
  `{'fingerprinter': 'config.fingerprint:fingerprinter'}`, and the recorded names
  `('runregistrykit', 'datastorekit', 'raypoolkit')`.
- **The attribute's name is SGK's choice**; `fingerprinter` above is a placeholder. The config is
  read for its form only; the module is imported when a fingerprint is taken, compared, described
  or listed (`runregistrykit/fingerprint.py:56-59`). `store show` works without importing it, but
  refuses if the config names no fingerprinter at all (checked: with an empty `runregistrykit.toml`,
  `store show` exits 1 with "names no fingerprinter, and the store layer requires one").

**`.gitignore`**: nothing to add. `:3` is `var/`, which ignores the runs root and the stores root.

**`config/fingerprint.py`** (SGK's 06), the module the config names, holding:
- **`FINGERPRINT_FORMAT = 6`**, from `RunRegistry/stores.py:206`;
- **the history of formats 1–6, moved verbatim** from the comment at `RunRegistry/stores.py:194-205`.
  That comment names `RunRegistry/tests/data/full_store_fingerprint*.json` and
  `test_store_fingerprint.GOLDEN` (`:197`), which move with `TestGolden` (item 7). Whether the moved
  text keeps them as they were or names the new paths is SGK's choice;
- **the fingerprinter**: `DatastoreKitFingerprinter(factories, FINGERPRINT_FORMAT)` from
  `runregistrykit.fingerprint`, over `config.datastore.factories` (`config/datastore.py:91`, a
  mapping of 38 names to factory classes, `"version": sqla_version_factory,` at `:92`). An instance,
  not the class: the loader refuses a class (U14);
- **Q5's pin** beside the format, when SGK's 07 adds it (item 8).

The protocol a fingerprinter meets is `runregistrykit.fingerprint.Fingerprinter`: `take(primary,
taken)`, `compare(recorded, current)`, `describe(fingerprint)` and `listing(inventory, fingerprint)`
(`runregistrykit/fingerprint.py:27-39`, `:81-92`). `DatastoreKitFingerprinter` implements it over
DatastoreKit's `read_inventory`, `fingerprint_of`, `compare_fingerprints` and `listing_lines`
(`:99-164`). SGK needs nothing else.

**`CLAUDE.md`** (SGK's 06): the registry section becomes the binding rules and a pointer to the
package's [`README.md`](../../README.md#the-rules), with `python -m runregistrykit list` as the
discovery command (item 10).

## 4. Which imports and names it rewrites

**Live code: 13 import statements in 10 files** (4 at module level). Each name's fate is the
script's, from the package as installed (appendix).

| File:line | Today | After |
|---|---|---|
| `ObjectFactories/tests/test_quadsource_policy_key.py:411` | `from RunRegistry.stores import fingerprint_of` (in `test_the_fingerprint_moves_with_the_policy`) | `from datastorekit.store_fingerprint import fingerprint_of`, and the format at each call (below) |
| `docs/a3-v2-readiness/fingerprint_time_probe.py:83` | `from RunRegistry.stores import FINGERPRINT_FORMAT, fingerprint_store` (in `main`) | `from runregistrykit.stores import fingerprint_store`; `from config.fingerprint import FINGERPRINT_FORMAT` |
| `docs/a3-v2-readiness/sigterm_handler_probe.py:150` | `import RunRegistry` (in `child`) | `import runregistrykit` |
| `docs/a3-v2-readiness/sigterm_handler_probe.py:151` | `import RunRegistry.stores as registry_stores` | `import runregistrykit.stores as registry_stores` |
| `docs/datastore-integrity-verification/compare_stores.py:21` | `from RunRegistry.stores import (FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_store)` | `from runregistrykit.stores import fingerprint_store`; `from datastorekit.store_fingerprint import compare_fingerprints`; `from config.fingerprint import FINGERPRINT_FORMAT` |
| `docs/datastore-integrity-verification/interrupt_when.py:61` | `import RunRegistry` | `import runregistrykit`; its names (`now_iso` `:68`, `read_json` `:87`, `:101`, `:161`, `TERMINAL_STATES` `:165`, `pid_alive` `:170`, `:190`, `liveness` `:175`, `DEFAULT_STALE_AFTER` `:230`) are all kept, with the same parameters |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:29` | as `compare_stores.py:21` | as `compare_stores.py:21` |
| `docs/dk-and-rpk-migration/rehearsal/stage_counts.py:26` | `import RunRegistry` | `import runregistrykit` |
| `docs/gktk-remedial/scoped_pipeline_run.py:526` | `import RunRegistry` (in `register`) | `import runregistrykit` |
| `docs/handover/quadsource_atol_sweep.py:554` | `import RunRegistry` (in `run_build`) | `import runregistrykit` |
| `docs/handover/quadsource_atol_sweep.py:760` | `import RunRegistry.stores` (in `prepare`) | `import runregistrykit.stores` |
| `docs/handover/quadsource_atol_sweep.py:862` | `import RunRegistry` (in `sweep`) | `import runregistrykit` |
| `docs/runregistry-extraction/fingerprint_both_ways.py:110` | `from RunRegistry import stores as sgk_stores` (in `check_store`) | SGK's 06 rewrites the script (below) |

Then the uses:

- **`_slug` → `slugify`** (U11; the brief's advice, `:143-144`): `stage_counts.py:37` and `:38`,
  `RunRegistry._slug(manifest["campaign"])` and `…["prompt"]`, become `runregistrykit.slugify(…)`.
  `slugify`'s body is `_slug`'s at `a45aefc`, statement for statement (`ast`, docstrings removed),
  and it is what `run_id` applies (`runregistrykit/__init__.py:119-129`). It is public: in
  `runregistrykit.__all__`.
- **`fingerprint_of` needs the format.** `datastorekit.store_fingerprint.fingerprint_of(inventory,
  fingerprint_format, taken=None)`, where SGK's was `fingerprint_of(inventory, taken=None)`. The
  script's verdict for each of these calls is "does not bind: missing a required argument:
  'fingerprint_format' (the move's new required `fingerprint_format`)", which is the move's
  documented effect, ruled not a stop (extraction prompt 07's log). Each becomes
  `fingerprint_of(inventory, FINGERPRINT_FORMAT[, taken])`, with `FINGERPRINT_FORMAT` from
  `config.fingerprint`:
  - `test_quadsource_policy_key.py:413`, `:416` and `:419`, `fingerprint_of(self.read_the_store(n))`.
    The test compares one class's entry (`["classes"]["QuadSourceIntegral"]`), which the format does
    not enter; the overall digest does;
  - `fingerprint_both_ways.py:127`, `sgk_stores.fingerprint_of(inventory)`. That script compares SGK's
    implementation with DatastoreKit's (W1), and the first is deleted. SGK's plan already says 06
    rewrites it to compare with the recorded fingerprints (`--against <run dir>`), through
    `config/fingerprint.py`'s fingerprinter (its README `:351-372`). Its other names are
    `sgk_stores.FINGERPRINT_FORMAT` (`:128`), `listing_lines` (`:203`), `compare_fingerprints`
    (`:227`, `:247`) and `read_sidecar` (`:240`): moved, moved, moved and kept;
  - for the staying tests' three, see item 7.
- **`FINGERPRINT_FORMAT`** (deleted, C7) becomes `config.fingerprint.FINGERPRINT_FORMAT` where it
  is read: `fingerprint_time_probe.py:86`, `compare_stores.py:48`, `compare_with_recorded.py:71`.
- **`compare_fingerprints`** (moved, the same parameters): `compare_stores.py:51`,
  `compare_with_recorded.py:80`.
- **The patch by assignment**, `sigterm_handler_probe.py:210`, `registry_stores.fingerprint_store =
  slow_fingerprint` (the original saved at `:187`, and restored by no line of the probe, which runs
  in a child process). At `v0.1.0` it still takes effect, because `Run._fingerprint_results`
  imports `fingerprint_store` from `runregistrykit.stores` when it runs
  (`runregistrykit/__init__.py:468`); but **no patch target is promised**
  ([`README.md`](../../README.md#the-public-names)). Whether the probe keeps it is SGK's choice;
  it is a dated readiness probe (item 10).
- **The printed commands**, three, each `PYTHONPATH=. ./venv/bin/python -m RunRegistry list`:
  `scoped_pipeline_run.py:580` (in the literal starting at `:578`), `quadsource_atol_sweep.py:595`
  (`:593`) and `:906` (`:904`). Each becomes `./venv/bin/python -m runregistrykit list`: with the
  package installed, `PYTHONPATH=.` is no longer needed for the command, though it does no harm.
  The script's appendix reports each literal at its first line and the command's own line.
- **The other string literals naming `RunRegistry`** in live code, 18 in all with the three above
  (appendix, item 5): the refusal at `scoped_pipeline_run.py:529` ("--register needs RunRegistry
  on the path"), which becomes untrue once the package is installed, and the `--register` help at
  `:611`; module and function docstrings (`fingerprint_time_probe.py:1`, `sigterm_handler_probe.py:1`,
  `interrupt_when.py:1`, `:96`, `compare_with_recorded.py:1`, `stage_counts.py:31`,
  `store_soundness.py:1`, `scoped_pipeline_run.py:1`, `quadsource_atol_sweep.py:412`, `:740`,
  `fingerprint_both_ways.py:1`); the message at `quadsource_atol_sweep.py:752`; and the timing label
  at `fingerprint_time_probe.py:85`. SGK's 06 acceptance 1 asks that none remain outside `prompts/`
  and dated `docs/` prose (its README §2.2, 06); which of the docstrings are dated prose is SGK's
  call.
- **Campaign records**: 6 files under `prompts/` import `fingerprint_of` from `RunRegistry.stores`,
  and 7 name `RunRegistry` (the seventh,
  `prompts/datastore-generic/orchestrator/measure-08/scripts/phaseB_edit_tests.py`, in a string).
  History: counted, not rewritten.
- **For the staying tests**, each helper and deleted name, with U21's **Advice:**, is item 7.

## 5. Its runs

**The programs that call `begin()`**, four calls, all binding at `v0.1.0` (the script's verdicts):

| Call | Program | Keywords |
|---|---|---|
| `docs/gktk-remedial/scoped_pipeline_run.py:541` | the pipeline driver A3 v2 will use, `register` | `campaign, prompt, slug, purpose, script, results, scope, heartbeat_means` |
| `docs/handover/quadsource_atol_sweep.py:556` | the sweep driver, `run_build` | as above |
| `docs/handover/quadsource_atol_sweep.py:864` | the sweep driver, `sweep` | as above |
| `docs/a3-v2-readiness/sigterm_handler_probe.py:159` | rehearsal tooling, a probe, `child` | `campaign, prompt, slug, purpose, argv, script, results, root` |

- **Each passes `script=__file__`**, so `begin()` walks for `runregistrykit.toml` from the script's
  own directory, two below SGK's root, and finds SGK's file there. None needs `client_root=`; a
  program run from outside the root, or a test that wants a root of its own, passes it.
- **`root=`** keeps its meaning, the runs root: the probe's temporary one (`:167`) still keeps its
  runs out of `var/runs`.
- **`results=`** names the store; `begin()` reads its sidecar and refuses a tombstone, and
  `finish(..., fingerprint=True)` imports `config.fingerprint` through the config to take the
  fingerprint.
- **From a linked worktree**, a run is recorded under the main checkout's `var/runs/`, in the same
  place relative to it, while its config, its fingerprinter and its git provenance are the
  worktree's own (SGK's 06 acceptance 4; the package's
  [`README.md`](../../README.md#the-clients-root), corrected by this prompt, U20).
- **SGK's 29 existing runs** are read by `python -m runregistrykit list` as they are (item 6): the
  manifest, `status.json` and `checkpoint.jsonl` keep their form.
- **The commands**, after adoption: `python -m runregistrykit list` (`--root DIR`, `--stale-after
  SECONDS`), and `python -m runregistrykit store {show,create,adopt,copy,move,fingerprint,retire,amend}`,
  each taking `--client-root DIR` before the command ([`README.md`](../../README.md#the-store-layer)).

## 6. Its stores

- **The store layer's prerequisites**: the extra `[stores]` (item 1's pin), `datastorekit` at
  `v0.4.0` or later (SGK has `v0.4.0`, `requirements.txt:17`), and a fingerprinter named in the
  config (item 3). At `14bcac0` SGK meets the first two once the pin is in; the third is its 06.
- **The one store operation SGK's live code calls** is `copy_store`, at
  `quadsource_atol_sweep.py:763`, `RunRegistry.stores.copy_store(BASELINE_STORE, SWEEP_STORE,
  purpose=…)`. It binds; at `v0.1.0` its runs root, for the refusal of a store a `running` run
  names, is the config's (it was `DEFAULT_ROOT`), and it refuses without a fingerprinter named.
  `fingerprint_store(primary, write=False)` is called by three scripts (`fingerprint_time_probe.py:93`,
  `compare_stores.py:32`, `compare_with_recorded.py:64`); it binds and returns the same keys as at
  `a45aefc` (`primary`, `fingerprint`, `recorded`, `comparison`, `wrote`, `sidecar`, `inventory`).
- **SGK's recorded fingerprints lack `encoding_format`**, so each, compared with a fresh one through
  the package, gives exactly one `encoding` entry and nothing else (U7). This is SGK's own
  `[00-recorded-fingerprints-lack-the-encoding-format]` and its D6 (its README `:277-279`,
  `:328-330`, `:534`). So `compare_stores.py:46` and `compare_with_recorded.py`, run against a
  sidecar SGK's code wrote, report a difference where today they report a match; SGK's plan
  already runs `compare_with_recorded.py` only on R2's own stores at 08 (`:372-374`).
- **Existing sidecars and run directories are read as they are.** The sidecar reader does not
  require `encoding_format` (U7), so `store show` reads each of SGK's tombstones as it did, and the
  paths in records stay relative to the record root (C4), which is SGK's root. No reader of an
  older form was added.

## 7. Its tests

**SGK's 101 staying tests** sit under `RunRegistry/tests/` at `14bcac0`: five modules, and
`TestGolden` and `TestDrivers` of `test_store_fingerprint.py`. SGK's 06 moves the driver tests and
`TestDrivers` to `RunDrivers/tests/` and `TestGolden` with the six golden files to
`ObjectFactories/tests/` (its README §2.2, 06). They import **12 statements in 5 modules**
(`test_prune_on_resume.py` none), and use 26 names (appendix). What each needs at `v0.1.0`:

**`test_build_rehearsal_scope.py`**
- `:39`, `from RunRegistry.tests.test_prune_on_resume import parsed_arguments`: SGK's own, a
  staying module; the import follows it to its new place.
- **`:317` asserts the driver's spelling**: `ast.unparse(node.func) == "RunRegistry.begin"`, over
  `run_build` in `quadsource_atol_sweep.py` (whose call is `:556`). When the driver's call becomes
  `runregistrykit.begin(…)`, this string changes in the same commit, or the test finds no call.

**`test_killed_handler.py`**
- `:26` `import RunRegistry`; `:27` from `test_pipeline_adoption` (`DRIVER`, `REPO_ROOT`,
  `load_driver`): SGK's own.
- `:90`, `RunRegistry.begin(campaign, prompt, slug, purpose, argv, root=self._tmp.name)`: binds. It
  gives no `script` and no `client_root`, so at `v0.1.0` the walk starts from the working
  directory: run from SGK's root, it finds SGK's config, and `root=` keeps the run out of
  `var/runs`.
- `:186`, `:336`, `:435`, `read_json`: kept.
- **`:333` and `:432` patch a private method on a `Run`**: `mock.patch.object(run,
  "_fingerprint_results", interrupted)`. `Run._fingerprint_results` is still there at `v0.1.0`, with
  the same parameters (`(self)`), so the patch still takes effect; but it is private, and no patch
  target is promised.

**`test_pipeline_adoption.py`**
- `:27` `import RunRegistry`; `:29` its own `REPO_ROOT`, SGK's root computed from `__file__`, which
  moves with it (and which `test_killed_handler.py:27` imports).
- `:74`, in `a_run`, `RunRegistry.begin(campaign, prompt, slug, root=self.root, **kwargs)`, with
  `purpose` and `argv` set by default in `kwargs` (`:72-73`): binds (the script binds its spelled
  arguments only, the `**kwargs` unexpanded).
- `:142` `list_runs(root=self.root)`, `:252` `TERMINAL_STATES`, `:179`, `:183`, `:347` `read_json`:
  kept.
- `:146` and `:158` run `[sys.executable, "-m", "RunRegistry", "list", "--root", self.root]` with
  `cwd=REPO_ROOT`: the module name becomes `"runregistrykit"`; from SGK's root, `list` finds SGK's
  config, and `--root` names the runs root.
- **`:278`, `root = RunRegistry.DEFAULT_ROOT`** (deleted, C2), the real runs root, whose listing the
  test compares before and after a refused run. Its replacement is
  `runregistrykit.find_client_root(client_root=REPO_ROOT).runs_root` (`ClientRoot.runs_root`,
  public).
- **`:330`, `mock.patch.object(RunRegistry, "DEFAULT_ROOT", self.root)`** (deleted), around
  `self.driver.register(…)`, so that the driver's `begin()` (`scoped_pipeline_run.py:541`) writes its
  run into the test's directory. **At `v0.1.0` there is no such name to patch**: the driver's
  `begin()` walks from its script to SGK's config, and would record its run under SGK's real
  `var/runs/`. The choice is SGK's, and each option touches a different file:
  - the driver's `register` takes a runs root (passed on as `begin(root=…)`) or a client root
    (`begin(client_root=…)`), and the test passes the temporary one: a change to the driver;
  - the test builds a client root of its own in a `tempfile` directory, with an absolute
    `runs_root`, and the driver is given it as `client_root=`: the same change to the driver, and a
    fixture in the test;
  - the test patches `runregistrykit.begin` with one that adds `root=self.root`: the driver
    unchanged, but a patch target the package does not promise.
  **Advice:** the first; the driver then says where its run goes, and the test needs no patch.

**`test_quadsource_atol_sweep_prepare.py`**
- `:25` `import RunRegistry`, `:26` `from RunRegistry import stores`.
- **`:27`, `from RunRegistry.tests.store_fixtures import StoreTestCase`**: the class is the base
  of `SweepPrepareTestCase` (`:61`). **`v0.1.0` ships no tests** (U19). `StoreTestCase`
  (`RunRegistry/tests/store_fixtures.py:114`) builds on `RegistryTestCase`
  (`RunRegistry/tests/test_run_registry.py:113`, whose `begin` calls `RunRegistry.begin` at `:124`)
  and on `StoreFixtures/shard_store_fixtures.py` (`store_fixtures.py:20`), and calls
  `stores.create_sidecar` (`:134`).
- **`:73`, `mock.patch.object(stores, "DEFAULT_ROOT", self.root)`** (deleted, C2), so that
  `prepare()`'s `copy_store` (`quadsource_atol_sweep.py:763`, no `runs_root`) looks for running runs
  in the test's runs root. At `v0.1.0` the runs root is the config's, so `copy_store` would read
  SGK's real `var/runs/` (read-only, for runs naming the store). The choice is SGK's, as for
  `test_pipeline_adoption.py:330`: `prepare()` takes a runs root or a client root and passes it to
  `copy_store(runs_root=…)` or `client_root=…`, or the test leaves the real runs root to be read.
  **Advice:** as there, the parameter.
- `:87`, `:96`, `:105`, `stores.create_sidecar(primary, purpose)`: bind. With no `client_root` they
  find SGK's config from the working directory, which must name a fingerprinter (it does, item 3).
  `:101` `sidecar_path`, `:115`, `:129` `read_sidecar`: kept.
- **`:134`, `RunRegistry._repo_path(baseline)`**: private, and its signature changed: `(path)` at
  `a45aefc`, `(path, root)` at `v0.1.0` (`runregistrykit/__init__.py:219-225`), the record root
  given. The expected value is the `copied_from.datastore` the package records. The baseline is in
  a `tempfile` directory, outside SGK's root, so it is recorded absolute; **Advice:** assert
  against `os.path.abspath(baseline)` (or compute it with `_repo_path(baseline, client.root)` for a
  `ClientRoot` the test holds, accepting a private name).

**`test_store_fingerprint.py`, `TestGolden` (`:347-382`) and `TestDrivers` (`:855-871`)**, with
`_FullStores` (`:138-162`), `TestGolden`'s base, and the module-level code they share:
- `:33` `import RunRegistry`, `:34` `from RunRegistry import stores`, `:35` `from RunRegistry.stores
  import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_of, fingerprint_store`, `:41` from
  `store_fixtures` (`StoreTestCase`, `load`, `sweep_shaped`, `write_sidecar_json`), `:47` from
  `test_store_command_line` (`CommandLineTestCase`). **Of these, `TestGolden`, `TestDrivers` and
  `_FullStores` use only `FINGERPRINT_FORMAT`, `fingerprint_of`, `compare_fingerprints` and
  `stores`** (the script's sites): the four helpers, `CommandLineTestCase` and `fingerprint_store`
  are imported for the classes this package ported, and go with them.
- **`:73`, `REPO_ROOT = Path(RunRegistry.REPO_ROOT)`** (deleted, C1), for `DRIVERS` (`:79-82`), the
  two drivers `TestDrivers` reads. **Advice:** the moved module computes its own root from
  `__file__`, as `test_pipeline_adoption.py:29` does.
- **`:147` and `:162`, `fingerprint_of(…)` without the format**, in `_FullStores.setUpClass` and
  `fingerprint`: the script's verdict "does not bind … (the move's new required
  `fingerprint_format`)". Each becomes `fingerprint_of(inventory, FINGERPRINT_FORMAT)`. (Extraction
  prompt 07 cites `TestGolden`, `:347-383`, for these; they are in its base class.)
- **`:378`, `fingerprint_of(self.baseline_inventory, taken)`, binds, but means something else**:
  its second positional argument now lands on `fingerprint_format`, and DatastoreKit refuses a
  `dict` there (`TypeError: fingerprint_of(): fingerprint_format must be an int, not dict …`, run
  here on a stand-in). The script's verdict says only that it binds; this is flagged by reading. It
  becomes `fingerprint_of(self.baseline_inventory, FINGERPRINT_FORMAT, taken)`.
- `:352`, `FINGERPRINT_FORMAT` (deleted): `config.fingerprint.FINGERPRINT_FORMAT`.
- **The golden fingerprint lacks `encoding_format`**, and DatastoreKit's `fingerprint_of` adds it
  (six keys: `fingerprint_format`, `encoding_format`, `classes`, `digest`, `problems`, `taken`).
  So `:354` and `:356`, `assertEqual(without_taken(…), without_taken(golden))`, and `:361`, the
  shape `{"fingerprint_format", "classes", "digest", "problems", "taken"}`, fail as written;
  `full_store_fingerprint_datastore-integrity-09c.json` (the `GOLDEN` of `:74-78`) has no
  `encoding_format`. How `TestGolden` meets this is SGK's choice: set `encoding_format` aside in the
  comparison and add it to the shape (the digest is unchanged, SGK's 04 W1), or record the key in a
  new golden file beside the old ones. It is the same fact as item 6's, on SGK's own golden data.
- `:374`, `stores._fingerprint_problems(dict(fp, taken={}))`: private, present, the same parameters
  (`(value)`); at `v0.1.0` it requires an integer format, a 64-hex digest, an object `taken`, and an
  integer `encoding_format` only if present (U7), so a fresh fingerprint still gives `[]`.
- `:381`, `compare_fingerprints(self.baseline, with_taken)`: moved; both fresh, so `[]` as before.

**The test helpers, U21.** `v0.1.0` ships no test support (U19), and **U21, taken 2026-10-15**:
the package will not ship one. What the staying tests take from the registry's own tests:

| Helper | Where (at `a45aefc`) | Used by a staying test |
|---|---|---|
| `StoreTestCase` | `RunRegistry/tests/store_fixtures.py:114`, on `RegistryTestCase` (`test_run_registry.py:113`) | `test_quadsource_atol_sweep_prepare.py:27`, `:61` |
| `load`, `sweep_shaped`, `write_sidecar_json` | `store_fixtures.py:105`, `:85`, `:97` | none: imported at `test_store_fingerprint.py:41` for ported classes |
| `CommandLineTestCase` | `RunRegistry/tests/test_store_command_line.py:53` | none: imported at `test_store_fingerprint.py:47` for ported classes |

**Advice:** SGK keeps the helpers it uses as its own code, copied from its frozen `a45aefc` beside
the moved tests: `StoreTestCase` and `RegistryTestCase`, the two `test_store_fingerprint` imports
dropped. Adapt the copy to a client root built in a `tempfile` directory, so that a test's runs and
sidecars never reach SGK's own config or `var/`. This package's
`runregistrykit/tests/client_fixtures.py` is a worked example: a `runregistrykit.toml` in a fresh git
repository in a `tempfile` directory, entered for the test (read, not imported; it is not in the
wheel). Its `RegistryTestCase` passes `client_root=` to `begin`
(`runregistrykit/tests/test_run_registry.py:116-135`).

**The test roots** change with SGK's 06: `CLAUDE.md:144`'s `-s RunRegistry/tests` gives way to
`RunDrivers/tests` (item 10).

## 8. The Q5 guard

SGK's 07 builds it: a test in `ObjectFactories/tests/` that pins, for format 6, the digests of
every `inventory_spec()` in the registry, in registry order, with the pin in `config/fingerprint.py`
beside the number (its README §2.2, 07; its audit §3.5). The recipe and a sketch, proved on public
names, are [`README.md`](README.md) §6; nothing of it is shipped (U22). The three breakages its 07
names (a leaf added with no bump, a bump with no new pin, a class added) each fail there.

**SGK's registry has a polymorphic `Parent.types` with `int` keys**, so the key conversion matters:
- `ObjectFactories/cosmology_types.py:17-20`, `COSMOLOGY_TYPES: Dict[int, str] = {LAMBDACDM_IDENTIFIER:
  "LambdaCDM", QCD_EOS_IDENTIFIER: "QCD_Cosmology"}`, with `LAMBDACDM_IDENTIFIER = 0` and
  `QCD_EOS_IDENTIFIER = 1` (`CosmologyModels/model_ids.py:1-2`);
- used by two specs: `ObjectFactories/BackgroundModel.py:900-904` (`"cosmology": Parent(
  "cosmology_serial", type_column="cosmology_type", types=COSMOLOGY_TYPES)`) and
  `ObjectFactories/wavenumber.py:396-400`, the same.

`canonical_json` refuses those keys as they are. The sketch writes each key as its own JSON, so
that `0` and `"0"` stay apart and a change of a key's type fails the guard. 21 `inventory_spec`
definitions in 20 files (`wavenumber.py` has two, `:126` and `:385`), over a registry of 38 names
(`config/datastore.py:91`; appendix, item 8).

## 9. Its acceptance

G2 holds when SGK has adopted `v0.1.0` in its own campaign (`runregistry-extraction` 05–08), and its
06's acceptance (its README §2.2, 06) shows:
1. **No `RunRegistry` import, string literal or `python -m RunRegistry`** outside `prompts/` and
   dated `docs/` prose; and **`measure_client_registry.py sgk --commit <its commit>` reports 0
   imports** in live code (and the staying tests are no longer under `RunRegistry/`).
2. Its roots pass, `RunDrivers` with the moved driver tests and `ObjectFactories` with `TestGolden`.
3. **`python -m runregistrykit list` gives its 29 runs**, with the same states and purposes as its
   01's baseline, and **`store show` reads each of its sidecars** as that baseline does.
4. **A run begun from a linked worktree is recorded under the main checkout's `var/runs/`.**
5. **A fingerprint taken through the new path carries `encoding_format`** beside the digest, and
   its digest equals `fingerprint_of`'s on 06's test store.
6. `requirements.txt` holds item 1's pin, installed from it, not editable; and every new
   manifest's `packages` names `runregistrykit`, `datastorekit` and `raypoolkit` (its 08,
   acceptance 2).

SGK's 08 records G2 on SGK's board, and its 09 drafts the record for this repository's board,
§2, row G2 (README §7). E2 (this checklist with `v0.1.0`) is recorded there when 07 lands.

## 10. What goes stale in it

- **`CLAUDE.md`, 10 lines** (appendix, item 7):
  - the registry section, `:77-104`, "Long-running jobs — the run registry": `RunRegistry/`
    records (`:79`), `python -m RunRegistry list` (`:87`). After adoption it states the rules
    briefly, names `python -m runregistrykit list`, and points at the package's README
    ([`README.md`](README.md) §3);
  - the freeze section, `:106-116`, "`RunRegistry/` is frozen": it ends with the adoption (SGK's
    06 removes it);
  - the test roots, `:144`, `-s RunRegistry/tests`: `RunDrivers/tests` in its place.
- **`docs/`, 158 lines in 19 files**, all listed with their text in the appendix. Most are dated
  audits, verifications and recorded command output, which describe the registry as it was:
  `runregistry-extraction-audit.md` (48), `runregistry-extraction-verification.md` (24),
  `dk-and-rpk-migration-verification.md` (26), `a3-v2-readiness-verification.md` (10),
  `datastore-integrity-verification.md` (10), `store-retirement-audit.md` (7),
  `a3-v2-readiness-audit.md` (3), `datastore-generic-audit.md` (3), `datastore-integrity-audit.md`
  (2), `store-fingerprint-audit.md` (2), and seven recorded outputs and checks
  (`a3-v2-readiness/rehearsal/prelaunch_checks.txt` (4) and `interrupter_firings.txt` (1),
  `datastore-integrity-verification/interrupter_firings.txt` (2),
  `a3-v2-readiness/fingerprint_time_probe.txt` (1),
  `dk-and-rpk-migration/rehearsal/prelaunch_checks_08.txt` (2),
  `runregistry-extraction/rehearsal/prelaunch_checks_02.txt` (3) and `_04.txt` (3)). Two are not
  dated records:
  - `docs/OPEN_ISSUES.md`, 6 lines (`:661`, `:666`, `:692`, `:746`, `:838`, `:893`), SGK's own
    index of its open issues, which SGK's rules keep;
  - `docs/a3-v2-readiness/interrupter_build_dummy_test.sh:6`, a comment naming `RunRegistry.begin`.
  **Advice:** do not rewrite the dated records; each describes the registry at its date.
- **Campaign records**: `prompts/`, 2078 lines, and the 7 `.py` files of item 4. History: not
  rewritten.

---

## Appendix: the script's output

`./venv/bin/python docs/adoption/measure_client_registry.py sgk`, from this repository's root at
extraction prompt 07's commit, with `runregistrykit` 0.1.0 and `datastorekit` 0.4.0; as printed.

### Measured: SecondaryGWKit (SGK) at `14bcac0`

- Repository `/Users/ds283/Documents/Code/SecondaryGWKit`, commit `14bcac0eb73069131f8ce4f55d91e5fc3e7318cf`, 2026-10-14, “Say in the runregistry-extraction plan what 08 repeats of W1”.
- Read through `git` only: 428 tracked `.py` files parsed with `ast`.
- Against `runregistrykit` 0.1.0 and `datastorekit` 0.4.0 as installed; signatures before the move from SecondaryGWKit a45aefc.
- `requirements.txt`: `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0` (`:17`); `ray==2.43.0` (`:75`); `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0` (`:76`); `SQLAlchemy==2.0.39` (`:87`).

| Figure | Live code | Staying tests |
|---|---|---|
| Import statements | 13 | 12 |
| … at module level | 4 | 12 |
| Files importing it | 10 | 5 |
| Names used | 15 | 26 |
| Calls bound | 12 | 8 |
| … binding | 8 | 6 |
| … not binding: the move's new `fingerprint_format` only | 4 | 2 |
| … not binding for any other reason | 0 | 0 |
| Name-alike calls, not the registry's | 26 | 0 |
| String literals naming it | 18 | 6 |
| … holding `-m RunRegistry` | 3 | 1 |

Campaign records: **6** `.py` files import it, 7 name it.

#### 1. Imports: live code

| File | Line | Scope | Statement |
|---|---|---|---|
| `ObjectFactories/tests/test_quadsource_policy_key.py` | 411 | `TestTheInventoryIdentityIncludesIt.test_the_fingerprint_moves_with_the_policy` | `from RunRegistry.stores import fingerprint_of` |
| `docs/a3-v2-readiness/fingerprint_time_probe.py` | 83 | `main` | `from RunRegistry.stores import FINGERPRINT_FORMAT, fingerprint_store` |
| `docs/a3-v2-readiness/sigterm_handler_probe.py` | 150 | `child` | `import RunRegistry` |
| `docs/a3-v2-readiness/sigterm_handler_probe.py` | 151 | `child` | `import RunRegistry.stores as registry_stores` |
| `docs/datastore-integrity-verification/compare_stores.py` | 21 | `module` | `from RunRegistry.stores import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_store` |
| `docs/datastore-integrity-verification/interrupt_when.py` | 61 | `module` | `import RunRegistry` |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py` | 29 | `module` | `from RunRegistry.stores import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_store` |
| `docs/dk-and-rpk-migration/rehearsal/stage_counts.py` | 26 | `module` | `import RunRegistry` |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 526 | `register` | `import RunRegistry` |
| `docs/handover/quadsource_atol_sweep.py` | 554 | `run_build` | `import RunRegistry` |
| `docs/handover/quadsource_atol_sweep.py` | 760 | `prepare` | `import RunRegistry.stores` |
| `docs/handover/quadsource_atol_sweep.py` | 862 | `sweep` | `import RunRegistry` |
| `docs/runregistry-extraction/fingerprint_both_ways.py` | 110 | `check_store` | `from RunRegistry import stores as sgk_stores` |

#### 2–3. Names and their fates at `v0.1.0`: live code

| Name | Fate | At `v0.1.0` | Sites |
|---|---|---|---|
| `RunRegistry.DEFAULT_STALE_AFTER` | kept | runregistrykit.DEFAULT_STALE_AFTER | `docs/datastore-integrity-verification/interrupt_when.py:230` (used) |
| `RunRegistry.TERMINAL_STATES` | kept | runregistrykit.TERMINAL_STATES | `docs/datastore-integrity-verification/interrupt_when.py:165` (used) |
| `RunRegistry._slug` | renamed (private) | runregistrykit.slugify(text); U11; at a45aefc (text) | `docs/dk-and-rpk-migration/rehearsal/stage_counts.py:37` (used), `docs/dk-and-rpk-migration/rehearsal/stage_counts.py:38` (used) |
| `RunRegistry.begin` | kept | runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=); at a45aefc (campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=) | `docs/a3-v2-readiness/sigterm_handler_probe.py:159` (used), `docs/gktk-remedial/scoped_pipeline_run.py:541` (used), `docs/handover/quadsource_atol_sweep.py:556` (used), `docs/handover/quadsource_atol_sweep.py:864` (used) |
| `RunRegistry.liveness` | kept | runregistrykit.liveness(status, stale_after, now=), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:175` (used) |
| `RunRegistry.now_iso` | kept | runregistrykit.now_iso(), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:68` (used) |
| `RunRegistry.pid_alive` | kept | runregistrykit.pid_alive(pid), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:170` (used), `docs/datastore-integrity-verification/interrupt_when.py:190` (used) |
| `RunRegistry.read_json` | kept | runregistrykit.read_json(path), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:87` (used), `docs/datastore-integrity-verification/interrupt_when.py:101` (used), `docs/datastore-integrity-verification/interrupt_when.py:161` (used) |
| `RunRegistry.stores.FINGERPRINT_FORMAT` | deleted | C7: the format is the client's, in its fingerprinter's module | `docs/a3-v2-readiness/fingerprint_time_probe.py:83` (imported), `docs/a3-v2-readiness/fingerprint_time_probe.py:86` (used), `docs/datastore-integrity-verification/compare_stores.py:21` (imported), `docs/datastore-integrity-verification/compare_stores.py:48` (used), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:29` (imported), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:71` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:128` (used) |
| `RunRegistry.stores.compare_fingerprints` | moved | datastorekit.store_fingerprint.compare_fingerprints(recorded, current); layer C, DatastoreKit's since v0.4.0; at a45aefc (recorded, current) | `docs/datastore-integrity-verification/compare_stores.py:21` (imported), `docs/datastore-integrity-verification/compare_stores.py:51` (used), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:29` (imported), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:80` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:227` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:247` (used) |
| `RunRegistry.stores.copy_store` | kept | runregistrykit.stores.copy_store(src, dst, purpose, runs_root=, *, client_root=); at a45aefc (src, dst, purpose, runs_root=) | `docs/handover/quadsource_atol_sweep.py:763` (used) |
| `RunRegistry.stores.fingerprint_of` | moved | datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=); layer C, DatastoreKit's since v0.4.0; at a45aefc (inventory, taken=) | `ObjectFactories/tests/test_quadsource_policy_key.py:411` (imported), `ObjectFactories/tests/test_quadsource_policy_key.py:413` (used), `ObjectFactories/tests/test_quadsource_policy_key.py:416` (used), `ObjectFactories/tests/test_quadsource_policy_key.py:419` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:127` (used) |
| `RunRegistry.stores.fingerprint_store` | kept | runregistrykit.stores.fingerprint_store(primary, *, write=, runs_root=, taken_by=, client_root=); at a45aefc (primary, *, write=, runs_root=, taken_by=) | `docs/a3-v2-readiness/fingerprint_time_probe.py:83` (imported), `docs/a3-v2-readiness/fingerprint_time_probe.py:93` (used), `docs/a3-v2-readiness/sigterm_handler_probe.py:187` (used), `docs/a3-v2-readiness/sigterm_handler_probe.py:210` (assigned), `docs/datastore-integrity-verification/compare_stores.py:21` (imported), `docs/datastore-integrity-verification/compare_stores.py:32` (used), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:29` (imported), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:64` (used) |
| `RunRegistry.stores.listing_lines` | moved | datastorekit.store_fingerprint.listing_lines(inventory, fingerprint); layer C, DatastoreKit's since v0.4.0; at a45aefc (inventory, fingerprint) | `docs/runregistry-extraction/fingerprint_both_ways.py:203` (used) |
| `RunRegistry.stores.read_sidecar` | kept | runregistrykit.stores.read_sidecar(primary, *, client_root=); at a45aefc (primary) | `docs/runregistry-extraction/fingerprint_both_ways.py:240` (used) |

#### 4. Calls: live code

| File:line | Call | Positional | Keywords | Unpacking | Verdict |
|---|---|---|---|---|---|
| `ObjectFactories/tests/test_quadsource_policy_key.py:413` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `ObjectFactories/tests/test_quadsource_policy_key.py:416` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `ObjectFactories/tests/test_quadsource_policy_key.py:419` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `docs/a3-v2-readiness/fingerprint_time_probe.py:93` | `fingerprint_store` | 1 | write | — | binds |
| `docs/a3-v2-readiness/sigterm_handler_probe.py:159` | `RunRegistry.begin` | 0 | argv, campaign, prompt, purpose, results, root, script, slug | — | binds |
| `docs/datastore-integrity-verification/compare_stores.py:32` | `fingerprint_store` | 1 | write | — | binds |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:64` | `fingerprint_store` | 1 | write | — | binds |
| `docs/gktk-remedial/scoped_pipeline_run.py:541` | `RunRegistry.begin` | 0 | campaign, heartbeat_means, prompt, purpose, results, scope, script, slug | — | binds |
| `docs/handover/quadsource_atol_sweep.py:556` | `RunRegistry.begin` | 0 | campaign, heartbeat_means, prompt, purpose, results, scope, script, slug | — | binds |
| `docs/handover/quadsource_atol_sweep.py:763` | `RunRegistry.stores.copy_store` | 2 | purpose | — | binds |
| `docs/handover/quadsource_atol_sweep.py:864` | `RunRegistry.begin` | 0 | campaign, heartbeat_means, prompt, purpose, results, scope, script, slug | — | binds |
| `docs/runregistry-extraction/fingerprint_both_ways.py:127` | `sgk_stores.fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |

Bound against `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=)`; `runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=)`; `runregistrykit.stores.copy_store(src, dst, purpose, runs_root=, *, client_root=)`; `runregistrykit.stores.fingerprint_store(primary, *, write=, runs_root=, taken_by=, client_root=)`.

Not the registry's (their callee does not resolve to it), so not bound:

- `ObjectFactories/tests/test_quadsource_parent_key.py:445` `engine.begin(…)`, in `TestCrossShardParentUnit._read`
- `ObjectFactories/tests/test_wkb_numeric_parent_key.py:983` `engine.begin(…)`, in `TestNullableParent._read`
- `StoreFixtures/real_store_fixtures.py:229` `pool._engine.begin(…)`, in `_write_primary`
- `StoreFixtures/real_store_fixtures.py:270` `engine.begin(…)`, in `_write_shard`
- `StoreFixtures/real_store_fixtures.py:1159` `engine.begin(…)`, in `_write_full_shard`
- `docs/a3-v2-readiness/reader_writes_probe.py:772` `copy_store(…)`, in `main`
- `docs/a3-v2-readiness/reader_writes_probe.py:830` `copy_store(…)`, in `main`
- `docs/a3-v2-readiness/reader_writes_probe.py:881` `copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:203` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:209` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:223` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:231` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:239` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:248` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:282` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:316` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:362` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:393` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:407` `rw.copy_store(…)`, in `main`
- `docs/datastore-generic-audit/str_e_misfire_probe.py:45` `engine.begin(…)`, in `module`
- `docs/datastore-integrity-verification/fault_copies.py:137` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:141` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:148` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:166` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:178` `copy_store(…)`, in `main`
- `docs/runregistry-extraction/fingerprint_both_ways.py:128` `package.fingerprint_of(…)`, in `check_store`

#### 5. String literals naming `RunRegistry`: live code

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `docs/a3-v2-readiness/fingerprint_time_probe.py` | 1 |  | S4 (a3-v2-readiness audit 00): how long the fingerprint that ``Run.finish(..., fingerprint=True)`` t |
| `docs/a3-v2-readiness/fingerprint_time_probe.py` | 85 |  | import RunRegistry.stores: s |
| `docs/a3-v2-readiness/sigterm_handler_probe.py` | 1 |  | a3-v2-readiness prompt 04: a SIGTERM to a pipeline driver blocked in ``ray.wait`` is recorded ``kill |
| `docs/datastore-integrity-verification/interrupt_when.py` | 1 |  | Send one SIGTERM to a registered pipeline run once it reaches a chosen point in a chosen stage. Writ |
| `docs/datastore-integrity-verification/interrupt_when.py` | 96 |  | The basename of the run's own driver, from its manifest's `argv[0]`, or `None`. `RunRegistry.begin`  |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py` | 1 |  | Compare closed stores' fingerprints with fingerprints recorded by earlier runs. PYTHONPATH=. ./venv/ |
| `docs/dk-and-rpk-migration/rehearsal/stage_counts.py` | 31 |  | The slug `RunRegistry.run_id` was given, recovered from the manifest's own fields. |
| `docs/dk-and-rpk-migration/rehearsal/store_soundness.py` | 1 |  | Integrity, foreign keys, version rows and the inventory of each closed store. PYTHONPATH=. ./venv/bi |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 1 |  | Run main.py's pipeline on a scoped wavenumber sample, against a locally bootstrapped Ray instance an |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 529 |  | scoped_pipeline_run: --register needs RunRegistry on the path; run this script from the repository r |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 578 | **`:580`** | ** scoped_pipeline_run: registered as ** manifest ** list it with: PYTHONPATH=. ./venv/bin/python -m |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 611 |  | record this run in var/runs/ through RunRegistry, under this slug. Without it nothing is registered  |
| `docs/handover/quadsource_atol_sweep.py` | 412 |  | `main.py`'s argv for either driver, `sys.argv` form (the program name first). `zend` is `--zend`'s v |
| `docs/handover/quadsource_atol_sweep.py` | 593 | **`:595`** | ** quadsource_atol_sweep --build: registered as ** manifest ** list it with: PYTHONPATH=. ./venv/bin |
| `docs/handover/quadsource_atol_sweep.py` | 740 |  | Make the sweep store from the baseline through one registry copy. `RunRegistry.stores.copy_store` co |
| `docs/handover/quadsource_atol_sweep.py` | 752 |  | quadsource_atol_sweep --prepare: --force no longer means "replace". RunRegistry.stores.copy_store ne |
| `docs/handover/quadsource_atol_sweep.py` | 904 | **`:906`** | ** quadsource_atol_sweep: registered as ** manifest ** list it with: PYTHONPATH=. ./venv/bin/python  |
| `docs/runregistry-extraction/fingerprint_both_ways.py` | 1 |  | The fingerprint both ways (runregistry-extraction prompt 04, W1; README §6.2 C3; 08 runs it again).  |

#### 1. Imports: the staying tests

| File | Line | Scope | Statement |
|---|---|---|---|
| `RunRegistry/tests/test_build_rehearsal_scope.py` | 39 | `module` | `from RunRegistry.tests.test_prune_on_resume import parsed_arguments` |
| `RunRegistry/tests/test_killed_handler.py` | 26 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_killed_handler.py` | 27 | `module` | `from RunRegistry.tests.test_pipeline_adoption import DRIVER, REPO_ROOT, load_driver` |
| `RunRegistry/tests/test_pipeline_adoption.py` | 27 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 25 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 26 | `module` | `from RunRegistry import stores` |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 27 | `module` | `from RunRegistry.tests.store_fixtures import StoreTestCase` |
| `RunRegistry/tests/test_store_fingerprint.py` | 33 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_store_fingerprint.py` | 34 | `module` | `from RunRegistry import stores` |
| `RunRegistry/tests/test_store_fingerprint.py` | 35 | `module` | `from RunRegistry.stores import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_of, fingerprint_store` |
| `RunRegistry/tests/test_store_fingerprint.py` | 41 | `module` | `from RunRegistry.tests.store_fixtures import StoreTestCase, load, sweep_shaped, write_sidecar_json` |
| `RunRegistry/tests/test_store_fingerprint.py` | 47 | `module` | `from RunRegistry.tests.test_store_command_line import CommandLineTestCase` |

#### 2–3. Names and their fates at `v0.1.0`: the staying tests

| Name | Fate | At `v0.1.0` | Sites |
|---|---|---|---|
| `RunRegistry.DEFAULT_ROOT` | deleted | C2: the runs root is the config's runs_root | `RunRegistry/tests/test_pipeline_adoption.py:278` (used), `RunRegistry/tests/test_pipeline_adoption.py:330` (patched (patch.object)) |
| `RunRegistry.REPO_ROOT` | deleted | C1: the root is the client's, found from its runregistrykit.toml | `RunRegistry/tests/test_store_fingerprint.py:73` (used) |
| `RunRegistry.Run._fingerprint_results` | private | runregistrykit.Run._fingerprint_results present; (self) at a45aefc, (self) at v0.1.0 | `RunRegistry/tests/test_killed_handler.py:333` (patched on an object (patch.object, by name)), `RunRegistry/tests/test_killed_handler.py:432` (patched on an object (patch.object, by name)) |
| `RunRegistry.TERMINAL_STATES` | kept | runregistrykit.TERMINAL_STATES | `RunRegistry/tests/test_pipeline_adoption.py:252` (used) |
| `RunRegistry._repo_path` | private | runregistrykit._repo_path present; (path) at a45aefc, (path, root) at v0.1.0 | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:134` (used) |
| `RunRegistry.begin` | kept | runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=); at a45aefc (campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=) | `RunRegistry/tests/test_killed_handler.py:90` (used), `RunRegistry/tests/test_pipeline_adoption.py:74` (used) |
| `RunRegistry.list_runs` | kept | runregistrykit.list_runs(root=, stale_after=, now=, *, client_root=); at a45aefc (root=, stale_after=, now=) | `RunRegistry/tests/test_pipeline_adoption.py:142` (used) |
| `RunRegistry.read_json` | kept | runregistrykit.read_json(path), the same parameters as at a45aefc | `RunRegistry/tests/test_killed_handler.py:186` (used), `RunRegistry/tests/test_killed_handler.py:336` (used), `RunRegistry/tests/test_killed_handler.py:435` (used), `RunRegistry/tests/test_pipeline_adoption.py:179` (used), `RunRegistry/tests/test_pipeline_adoption.py:183` (used), `RunRegistry/tests/test_pipeline_adoption.py:347` (used) |
| `RunRegistry.stores.DEFAULT_ROOT` | deleted | C2: the runs root is the config's runs_root | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:73` (patched (patch.object)) |
| `RunRegistry.stores.FINGERPRINT_FORMAT` | deleted | C7: the format is the client's, in its fingerprinter's module | `RunRegistry/tests/test_store_fingerprint.py:35` (imported), `RunRegistry/tests/test_store_fingerprint.py:352` (used) |
| `RunRegistry.stores._fingerprint_problems` | private | runregistrykit.stores._fingerprint_problems present; (value) at a45aefc, (value) at v0.1.0 | `RunRegistry/tests/test_store_fingerprint.py:374` (used) |
| `RunRegistry.stores.compare_fingerprints` | moved | datastorekit.store_fingerprint.compare_fingerprints(recorded, current); layer C, DatastoreKit's since v0.4.0; at a45aefc (recorded, current) | `RunRegistry/tests/test_store_fingerprint.py:35` (imported), `RunRegistry/tests/test_store_fingerprint.py:381` (used) |
| `RunRegistry.stores.create_sidecar` | kept | runregistrykit.stores.create_sidecar(primary, purpose, *, client_root=); at a45aefc (primary, purpose) | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:87` (used), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:96` (used), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:105` (used) |
| `RunRegistry.stores.fingerprint_of` | moved | datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=); layer C, DatastoreKit's since v0.4.0; at a45aefc (inventory, taken=) | `RunRegistry/tests/test_store_fingerprint.py:35` (imported), `RunRegistry/tests/test_store_fingerprint.py:147` (used), `RunRegistry/tests/test_store_fingerprint.py:162` (used), `RunRegistry/tests/test_store_fingerprint.py:378` (used) |
| `RunRegistry.stores.fingerprint_store` | kept | runregistrykit.stores.fingerprint_store(primary, *, write=, runs_root=, taken_by=, client_root=); at a45aefc (primary, *, write=, runs_root=, taken_by=) | `RunRegistry/tests/test_store_fingerprint.py:35` (imported) |
| `RunRegistry.stores.read_sidecar` | kept | runregistrykit.stores.read_sidecar(primary, *, client_root=); at a45aefc (primary) | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:115` (used), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:129` (used) |
| `RunRegistry.stores.sidecar_path` | kept | runregistrykit.stores.sidecar_path(primary), the same parameters as at a45aefc | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:101` (used) |
| `RunRegistry.tests.store_fixtures.StoreTestCase` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:27` (imported), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:61` (used), `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.store_fixtures.load` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.store_fixtures.sweep_shaped` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.store_fixtures.write_sidecar_json` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.test_pipeline_adoption.DRIVER` | the client's own | RunRegistry.tests.test_pipeline_adoption is a staying test module, which moves with the tests | `RunRegistry/tests/test_killed_handler.py:27` (imported), `RunRegistry/tests/test_killed_handler.py:479` (used), `RunRegistry/tests/test_killed_handler.py:559` (used) |
| `RunRegistry.tests.test_pipeline_adoption.REPO_ROOT` | the client's own | RunRegistry.tests.test_pipeline_adoption is a staying test module, which moves with the tests | `RunRegistry/tests/test_killed_handler.py:27` (imported), `RunRegistry/tests/test_killed_handler.py:29` (used) |
| `RunRegistry.tests.test_pipeline_adoption.load_driver` | the client's own | RunRegistry.tests.test_pipeline_adoption is a staying test module, which moves with the tests | `RunRegistry/tests/test_killed_handler.py:27` (imported), `RunRegistry/tests/test_killed_handler.py:80` (used) |
| `RunRegistry.tests.test_prune_on_resume.parsed_arguments` | the client's own | RunRegistry.tests.test_prune_on_resume is a staying test module, which moves with the tests | `RunRegistry/tests/test_build_rehearsal_scope.py:39` (imported), `RunRegistry/tests/test_build_rehearsal_scope.py:80` (used) |
| `RunRegistry.tests.test_store_command_line.CommandLineTestCase` | not shipped | RunRegistry.tests.test_store_command_line is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:47` (imported) |

#### 4. Calls: the staying tests

| File:line | Call | Positional | Keywords | Unpacking | Verdict |
|---|---|---|---|---|---|
| `RunRegistry/tests/test_killed_handler.py:90` | `RunRegistry.begin` | 0 | argv, campaign, prompt, purpose, root, slug | — | binds |
| `RunRegistry/tests/test_pipeline_adoption.py:74` | `RunRegistry.begin` | 0 | campaign, prompt, root, slug | ** | binds (its spelled arguments; the unpacking is not expanded) |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:87` | `stores.create_sidecar` | 2 | — | — | binds |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:96` | `stores.create_sidecar` | 2 | — | — | binds |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:105` | `stores.create_sidecar` | 2 | — | — | binds |
| `RunRegistry/tests/test_store_fingerprint.py:147` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `RunRegistry/tests/test_store_fingerprint.py:162` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `RunRegistry/tests/test_store_fingerprint.py:378` | `fingerprint_of` | 2 | — | — | binds |

Bound against `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=)`; `runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=)`; `runregistrykit.stores.create_sidecar(primary, purpose, *, client_root=)`.

#### 5. String literals naming `RunRegistry`: the staying tests

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `RunRegistry/tests/test_build_rehearsal_scope.py` | 317 |  | RunRegistry.begin |
| `RunRegistry/tests/test_pipeline_adoption.py` | 146 |  | RunRegistry |
| `RunRegistry/tests/test_pipeline_adoption.py` | 158 |  | RunRegistry |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 1 |  | `docs/handover/quadsource_atol_sweep.py` `prepare()` and `assert_store_is_self_consistent()`, for `s |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 62 |  | One temporary directory (`self.top`), a runs root inside it (`self.root`), and a fresh import of the |
| `RunRegistry/tests/test_store_fingerprint.py` | 1 | **`:3`** | The store fingerprint (store-fingerprint prompt 04): `RunRegistry.stores.fingerprint_of`, `compare_f |

#### 1. Campaign records

Importing it: `prompts/datastore-generic/orchestrator/measure-05/scripts/m4_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-06/scripts/m1_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-07/scripts/m1_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-08/scripts/m1_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-08/scripts/m4b_order_matters.py` (1), `prompts/datastore-generic/orchestrator/measure-09/scripts/m4_inventory.py` (1).

Naming it without importing it: `prompts/datastore-generic/orchestrator/measure-08/scripts/phaseB_edit_tests.py`.

#### 6. `installed_package_provenance`

Not defined.

#### 7. Tracked files other than `.py` matching `RunRegistry|run registry|runregistrykit`

Lines by top directory: `CLAUDE.md` 10, `docs` 158, `prompts` 2078.

Outside the campaign records (text squeezed, first 110 characters):

| File | Line | Text |
|---|---|---|
| `CLAUDE.md` | 77 | ## Long-running jobs — the run registry |
| `CLAUDE.md` | 79 | A job that takes hours must not be something a conversation owns. `RunRegistry/` records that one |
| `CLAUDE.md` | 87 | 1. **Discovery.** Run `python -m RunRegistry list` at the start of a session and before launching |
| `CLAUDE.md` | 106 | ## `RunRegistry/` is frozen — it is moving to RunRegistryKit |
| `CLAUDE.md` | 108 | Since prompt 01 of `runregistry-extraction` (`a45aefc`), `RunRegistry/` is frozen: RunRegistryKit |
| `CLAUDE.md` | 111 | `RunRegistry/` and nothing else. |
| `CLAUDE.md` | 113 | - **Nothing under `RunRegistry/` changes**, its tests included, until |
| `CLAUDE.md` | 114 | `prompts/runregistry-extraction` prompt 06 replaces it with the pinned `runregistrykit`. |
| `CLAUDE.md` | 116 | is fixed in RunRegistryKit, not here. If a fix cannot wait, stop and ask the user. |
| `CLAUDE.md` | 144 | PYTHONPATH=. ./venv/bin/python -m unittest discover -s RunRegistry/tests -t . |
| `docs/OPEN_ISSUES.md` | 661 | ### 1.11 The run registry campaign |
| `docs/OPEN_ISSUES.md` | 666 | was exercised for the first time and crashed. Prompt 01 landed the `RunRegistry/` package, the |
| `docs/OPEN_ISSUES.md` | 692 | Prompt 03 landed the same day: `RunRegistry/stores.py` owns the store sidecar, and `python -m RunRegistry stor |
| `docs/OPEN_ISSUES.md` | 746 | \| `[01-cross-filesystem-move-advice-says-delete-by-hand]` \| store-retirement \| **Narrowed 2026-10-12** by dk-a |
| `docs/OPEN_ISSUES.md` | 838 | \| `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` \| a3-v2-readiness \| A handler's ` |
| `docs/OPEN_ISSUES.md` | 893 | `RunRegistry/` moves to a repository of its own, RunRegistryKit, before the A3 v2 compute run, with |
| `docs/a3-v2-readiness-audit.md` | 7 | baseline, `mode=ro`, through `RunRegistry.stores.fingerprint_store(..., write=False)`, with the |
| `docs/a3-v2-readiness-audit.md` | 293 | - **The read.** `RunRegistry.stores.fingerprint_store(primary, write=False)` on |
| `docs/a3-v2-readiness-audit.md` | 295 | `RunRegistry.begin`, no `store` subcommand, no `ShardedPool`. The five store files and the sidecar |
| `docs/a3-v2-readiness-verification.md` | 75 | `running` with a pid answering `kill -0`, and that `RunRegistry list` showed it, and ended its turn. |
| `docs/a3-v2-readiness-verification.md` | 162 | - `python -m RunRegistry list` showed nothing `running`: 12 runs before `reference` (10 finished, |
| `docs/a3-v2-readiness-verification.md` | 209 | interrupter's from `RunRegistry.now_iso()`. Equal stamps bound the delay below 1 s; they do not |
| `docs/a3-v2-readiness-verification.md` | 309 | appeared. The refusal is raised before `RunRegistry.begin` and `ray.init`. |
| `docs/a3-v2-readiness-verification.md` | 638 | **Before the first run** (10:23–10:31): `python -m RunRegistry list` showed 16 runs, none |
| `docs/a3-v2-readiness-verification.md` | 722 | - [ ] **The pre-launch checks**, on that machine (§1.3): `RunRegistry list` shows nothing `running` |
| `docs/a3-v2-readiness-verification.md` | 728 | with a pid answering `kill -0`, and `RunRegistry list`. |
| `docs/a3-v2-readiness-verification.md` | 845 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/a3-v2-readiness-verification.md` | 847 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint --write \ |
| `docs/a3-v2-readiness-verification.md` | 849 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/a3-v2-readiness/fingerprint_time_probe.txt` | 15 | import RunRegistry.stores: 0.017 s |
| `docs/a3-v2-readiness/interrupter_build_dummy_test.sh` | 6 | # `argv[0]` is `docs/handover/quadsource_atol_sweep.py` (`RunRegistry.begin` records `sys.argv` |
| `docs/a3-v2-readiness/rehearsal/interrupter_firings.txt` | 3 | 2026-10-04T01:44:41+01:00 liveness alive; pid 41825; stage 'list it with: PYTHONPATH=. ./venv/bin/python -m Ru |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 9 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 48 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 88 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 129 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/datastore-generic-audit.md` | 183 | `RunRegistry.stores.copy_store`. **Keep** `_require_bare_name` and the "both resolve to one file" |
| `docs/datastore-generic-audit.md` | 230 | `RunRegistry/` has fallbacks for legacy store **sidecars** (no `sidecar_format`; `adopt_sidecar` is |
| `docs/datastore-generic-audit.md` | 233 | not stores; the registry never deletes a record, and `python -m RunRegistry list` lists the old run |
| `docs/datastore-integrity-audit.md` | 135 | design. `RunRegistry/tests/test_store_fingerprint.py:60` pins `full_store_fingerprint.json`. Every |
| `docs/datastore-integrity-audit.md` | 309 | **[probed]** Nothing was `running` (`python -m RunRegistry list`), no journal was present, and the |
| `docs/datastore-integrity-verification.md` | 64 | `PYTHONPATH=.` is not in the prompt's §1.3 command; the driver's `register()` imports `RunRegistry`, |
| `docs/datastore-integrity-verification.md` | 68 | Before each launch: `python -m RunRegistry list` showed nothing `running`; `ray status` found no |
| `docs/datastore-integrity-verification.md` | 71 | `status.json` says `running` with a pid answering `kill -0`, `RunRegistry list` shows the run), and |
| `docs/datastore-integrity-verification.md` | 169 | a person, `RunRegistry.Run(…).finish('killed', exit_code=None)`, after `kill -0 6384` failed: |
| `docs/datastore-integrity-verification.md` | 466 | - [ ] **`RunRegistry list` clean** — nothing `running`, nothing stale (§1.1, before every launch). |
| `docs/datastore-integrity-verification.md` | 546 | PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/datastore-integrity-verification.md` | 547 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store show var/datastores/datastore-integrity-10-<store>.sqlite |
| `docs/datastore-integrity-verification.md` | 549 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" var/datastores/datastore-int |
| `docs/datastore-integrity-verification.md` | 550 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint [--write] var/datastores/datastore-integrity-1 |
| `docs/datastore-integrity-verification.md` | 556 | PYTHONPATH=. ./venv/bin/python -c "import RunRegistry; RunRegistry.Run('var/runs/datastore-integrity-10-resume |
| `docs/datastore-integrity-verification/interrupter_firings.txt` | 3 | 2026-10-01T21:03:02+01:00 liveness alive; pid 1238; stage 'list it with: PYTHONPATH=. ./venv/bin/python -m Run |
| `docs/datastore-integrity-verification/interrupter_firings.txt` | 12 | 2026-10-01T23:08:13+01:00 liveness alive; pid 6384; stage 'list it with: PYTHONPATH=. ./venv/bin/python -m Run |
| `docs/dk-and-rpk-migration-verification.md` | 87 | answering `kill -0`, and that `RunRegistry list` showed it, and ended its turn. The orchestrator ran |
| `docs/dk-and-rpk-migration-verification.md` | 108 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/dk-and-rpk-migration-verification.md` | 110 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint --write \ |
| `docs/dk-and-rpk-migration-verification.md` | 112 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/dk-and-rpk-migration-verification.md` | 123 | - `python -m RunRegistry list` showed nothing `running`: 17 runs before `reference` (15 finished, 2 |
| `docs/dk-and-rpk-migration-verification.md` | 241 | interrupter's from `RunRegistry.now_iso()`. They bound the delay; they do not measure it. In |
| `docs/dk-and-rpk-migration-verification.md` | 516 | `RunRegistry.stores.fingerprint_store` does, and it reads the shards from the primary's `shards` |
| `docs/dk-and-rpk-migration-verification.md` | 716 | \| RunRegistry \| 286 \| OK \| 20.5 \| |
| `docs/dk-and-rpk-migration-verification.md` | 821 | - `RunRegistry list` showed the run. |
| `docs/dk-and-rpk-migration-verification.md` | 856 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: 21 runs before |
| `docs/dk-and-rpk-migration-verification.md` | 871 | - `RunRegistry.package_provenance()` gave the record above. |
| `docs/dk-and-rpk-migration-verification.md` | 1563 | \| RunRegistry \| 286 \| OK \| 40.5 \| |
| `docs/dk-and-rpk-migration-verification.md` | 1616 | \| 3 \| The six roots pass \| This prompt's suites at `6861a9f`, whose code is `0c9e2cf`'s: Datastore 320, RunReg |
| `docs/dk-and-rpk-migration-verification.md` | 1629 | comment in `RunRegistry/tests/test_pipeline_adoption.py`, and that file's `ast` is equal at the two |
| `docs/dk-and-rpk-migration-verification.md` | 1724 | - `RunRegistry list` showed the run. |
| `docs/dk-and-rpk-migration-verification.md` | 1761 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: 25 runs before |
| `docs/dk-and-rpk-migration-verification.md` | 1783 | - `RunRegistry.package_provenance()` gave the record above. |
| `docs/dk-and-rpk-migration-verification.md` | 2550 | \| RunRegistry \| 286 \| OK \| 19.8 \| |
| `docs/dk-and-rpk-migration-verification.md` | 2606 | \| 4 \| The six roots pass \| This prompt's suites at `5631f0e`, whose code is `643c3b2`'s but for one test comme |
| `docs/dk-and-rpk-migration-verification.md` | 2807 | \| RunRegistry \| 286 \| 286 \| OK \| 54.4 \| |
| `docs/dk-and-rpk-migration-verification.md` | 2822 | `pip check` reports no broken requirements. `RunRegistry.package_provenance()`, saved as |
| `docs/dk-and-rpk-migration-verification.md` | 2845 | at `:2704`); `RunRegistry.stores.move_store` (`RunRegistry/stores.py:1109-1123`) relays it through |
| `docs/dk-and-rpk-migration-verification.md` | 2861 | exactly the board's, and **0 after**. `import RunRegistry.stores` in a fresh `python -I` still loads neither |
| `docs/dk-and-rpk-migration-verification.md` | 2862 | `ray`, `sqlalchemy` nor `datastorekit.store_inventory` (`RunRegistry/stores.py:114`). |
| `docs/dk-and-rpk-migration-verification.md` | 2895 | \| **G2**: SGK adopted `v0.2.2` or later (U37; `actor-names` U3; `factory-defaults` U5), fingerprint reproduced |
| `docs/dk-and-rpk-migration-verification.md` | 2913 | \| **G2** \| **holds** 2026-10-12: SGK adopted `v0.2.0`, and its five parts of the checklist's item 8 hold. (1)  |
| `docs/dk-and-rpk-migration/rehearsal/prelaunch_checks_08.txt` | 127 | RunRegistry/tests/test_pipeline_adoption.py \| 9 +++++---- |
| `docs/dk-and-rpk-migration/rehearsal/prelaunch_checks_08.txt` | 131 | -- correction 1: ast of RunRegistry/tests/test_pipeline_adoption.py at 643c3b2 vs HEAD |
| `docs/runregistry-extraction-audit.md` | 1 | # RunRegistry extraction audit — moving the run registry into a package of its own |
| `docs/runregistry-extraction-audit.md` | 9 | **Why it exists.** `RunRegistry/` was built here, for this repository's long jobs |
| `docs/runregistry-extraction-audit.md` | 11 | both of their `dk-and-rpk-migration` plans record that they have "no run registry and no |
| `docs/runregistry-extraction-audit.md` | 16 | audit records the decisions taken on 2026-10-12, measures what in `RunRegistry/` belongs to this |
| `docs/runregistry-extraction-audit.md` | 30 | \| **D1** — where it goes \| **A repository of its own, `RunRegistryKit`** (package `runregistrykit`), beside Da |
| `docs/runregistry-extraction-audit.md` | 32 | \| **D3** — the fingerprint \| **Split by layer (§3).** The encoding and the digest algorithm go to DatastoreKit |
| `docs/runregistry-extraction-audit.md` | 33 | \| **D4** — a client with no fingerprinter \| **None is supported.** The store layer requires a fingerprinter. T |
| `docs/runregistry-extraction-audit.md` | 45 | ## 1. What `RunRegistry/` is today |
| `docs/runregistry-extraction-audit.md` | 47 | Measured at `d03a643`. `python -m RunRegistry list` reports 29 runs, 27 finished and 2 `unknown` |
| `docs/runregistry-extraction-audit.md` | 52 | \| `RunRegistry/__init__.py` \| 710 \| none at module scope; `RunRegistry.stores` lazily, for `Run.finish(fingerp |
| `docs/runregistry-extraction-audit.md` | 53 | \| `RunRegistry/stores.py` \| 2185 \| `datastorekit.SQL.ShardedPool` (×3) and `datastorekit.store_inventory` (×3) |
| `docs/runregistry-extraction-audit.md` | 54 | \| `RunRegistry/__main__.py` \| 515 \| none \| the CLI: `list` and the `store` subcommands \| |
| `docs/runregistry-extraction-audit.md` | 65 | `import RunRegistry` loads neither `ray` nor `sqlalchemy` (the docstring of `fingerprint_store`, |
| `docs/runregistry-extraction-audit.md` | 101 | \| C5 \| `RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")`, `:119` \| the packages SGK's `dk-and-rpk-migr |
| `docs/runregistry-extraction-audit.md` | 107 | **A hazard C1 already has here.** `REPO_ROOT` follows whichever copy of `RunRegistry/` was imported. |
| `docs/runregistry-extraction-audit.md` | 116 | **`main.py` does not.** It contains no reference to the registry (`grep -ci RunRegistry main.py` is |
| `docs/runregistry-extraction-audit.md` | 124 | \| `ObjectFactories/tests/test_quadsource_policy_key.py:411` \| `from RunRegistry.stores import fingerprint_of`  |
| `docs/runregistry-extraction-audit.md` | 125 | \| `docs/a3-v2-readiness/{sigterm_handler_probe,fingerprint_time_probe}.py`, `docs/datastore-integrity-verifica |
| `docs/runregistry-extraction-audit.md` | 144 | \| **C. Fingerprint** \| SHA-256 over each class's canonical record lines, newline-terminated; the same per dist |
| `docs/runregistry-extraction-audit.md` | 183 | \| when and where a fingerprint is taken and recorded \| **RunRegistryKit**: refused while a `running` run names |
| `docs/runregistry-extraction-audit.md` | 185 | RunRegistryKit reads a fingerprint only through `fingerprint_format`, `digest`, and the list of |
| `docs/runregistry-extraction-audit.md` | 194 | DatastoreKit's own subject; the sidecar is only where RunRegistryKit records it. |
| `docs/runregistry-extraction-audit.md` | 224 | in `RunRegistry/tests/data/` stops matching, and the author then bumps by hand. With layer A and its |
| `docs/runregistry-extraction-audit.md` | 237 | `RunRegistry/tests/` holds 286 tests in 14 modules **[agent; the per-module counts sum to the |
| `docs/runregistry-extraction-audit.md` | 250 | into RunRegistryKit's tests as it is. |
| `docs/runregistry-extraction-audit.md` | 253 | build a full SGK store from it and fingerprint it, through `stores.py:1494`. In RunRegistryKit |
| `docs/runregistry-extraction-audit.md` | 256 | no client, so the DatastoreKit release of §6 may offer such a fixture; if not, RunRegistryKit |
| `docs/runregistry-extraction-audit.md` | 260 | `RunRegistry/tests/` only because that is where registry adoption was tested. They need a test |
| `docs/runregistry-extraction-audit.md` | 261 | root of their own when `RunRegistry/` is deleted (§8, Q6). `RunRegistry/tests/data/` holds six |
| `docs/runregistry-extraction-audit.md` | 274 | ## 5. RunRegistryKit |
| `docs/runregistry-extraction-audit.md` | 279 | with setuptools, `requires-python = ">=3.12"`, the package found by `include = ["runregistrykit*"]` |
| `docs/runregistry-extraction-audit.md` | 295 | Which file — a `[tool.runregistrykit]` table in a `pyproject.toml`, or a file of its own — is §8 Q2. |
| `docs/runregistry-extraction-audit.md` | 302 | `runregistrykit[stores]`, needing `datastorekit` **by name and minimum version, not by git URL**. |
| `docs/runregistry-extraction-audit.md` | 304 | (`requirements.txt:17` here). A git-URL requirement inside RunRegistryKit would conflict with the |
| `docs/runregistry-extraction-audit.md` | 310 | The six rules in `CLAUDE.md` ("Long-running jobs — the run registry") are as much the product as |
| `docs/runregistry-extraction-audit.md` | 312 | Their full text, with the five failures of §0 that each one answers, moves to RunRegistryKit's |
| `docs/runregistry-extraction-audit.md` | 327 | moved from `RunRegistry/stores.py:1164-1390` into a DatastoreKit module beside |
| `docs/runregistry-extraction-audit.md` | 354 | migration, and both adopt RunRegistryKit after it closes (D4). |
| `docs/runregistry-extraction-audit.md` | 400 | Neither amendment brings RunRegistryKit into those campaigns' scope. |
| `docs/runregistry-extraction-audit.md` | 413 | \| **Q1** — names \| Repository `RunRegistryKit`, distribution and package `runregistrykit`, CLI `python -m runr |
| `docs/runregistry-extraction-audit.md` | 414 | \| **Q2** — the client config \| **A file of its own at the root**, read with the standard library's `tomllib`,  |
| `docs/runregistry-extraction-audit.md` | 417 | \| **Q5** — the spec-digest guard (§3.5) \| **Build it in SGK's adoption**, in the client fingerprint module's t |
| `docs/runregistry-extraction-audit.md` | 430 | from RunRegistryKit; RunRegistryKit's store layer needs it. |
| `docs/runregistry-extraction-audit.md` | 431 | 2. **RunRegistryKit `v0.1.0`: a fresh import** of `RunRegistry/` from a frozen SGK commit, as |
| `docs/runregistry-extraction-audit.md` | 435 | and the rules in its README. **SGK's `RunRegistry/` is frozen from the import commit until SGK |
| `docs/runregistry-extraction-audit.md` | 438 | release of step 1, in a commit of its own; `runregistrykit` is pinned at its tag; SGK's |
| `docs/runregistry-extraction-audit.md` | 440 | live callers of §2.1 are rewritten; the 101 tests get their root; `RunRegistry/` is deleted; |
| `docs/runregistry-extraction-audit.md` | 469 | `RunRegistry._slug` **[agent]**: the rewrite in step 3 should use a public name. |
| `docs/runregistry-extraction-verification.md` | 12 | - §3, R2: through both packages, after the RunRegistryKit swap (prompt 08); |
| `docs/runregistry-extraction-verification.md` | 37 | - `runregistrykit` is not installed. |
| `docs/runregistry-extraction-verification.md` | 132 | - `RunRegistry list` showed the run. |
| `docs/runregistry-extraction-verification.md` | 161 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/runregistry-extraction-verification.md` | 163 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint --write \ |
| `docs/runregistry-extraction-verification.md` | 165 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/runregistry-extraction-verification.md` | 179 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: |
| `docs/runregistry-extraction-verification.md` | 206 | - `pip show runregistrykit` found nothing. `pip check` was clean. |
| `docs/runregistry-extraction-verification.md` | 207 | - `RunRegistry.package_provenance()` gave the record above. It equals, as JSON, the `packages` of |
| `docs/runregistry-extraction-verification.md` | 216 | - `import runregistrykit` raises `ModuleNotFoundError`; |
| `docs/runregistry-extraction-verification.md` | 1000 | `stage`, not those fields. `RunRegistry list` shows `-` under PROGRESS for each. No field R2 |
| `docs/runregistry-extraction-verification.md` | 1043 | \| RunRegistry \| 286 \| OK \| 29.0 \| |
| `docs/runregistry-extraction-verification.md` | 1076 | - `RunRegistry list` shows 33 runs: 01's 29, and this rehearsal's four, all finished but the two |
| `docs/runregistry-extraction-verification.md` | 1132 | - `runregistrykit` is not installed. |
| `docs/runregistry-extraction-verification.md` | 1232 | - `RunRegistry list` showed the run; |
| `docs/runregistry-extraction-verification.md` | 1276 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: 33 runs before |
| `docs/runregistry-extraction-verification.md` | 1296 | - `pip show runregistrykit` found nothing. `pip check` was clean. |
| `docs/runregistry-extraction-verification.md` | 1297 | - `RunRegistry.package_provenance()` gave the record above, equal as JSON to the expected record, |
| `docs/runregistry-extraction-verification.md` | 1306 | - `import runregistrykit` raises `ModuleNotFoundError`; |
| `docs/runregistry-extraction-verification.md` | 1925 | (`docs/gktk-remedial/scoped_pipeline_run.py`, `RunRegistry/__init__.py` `Run.finish`'s docstring), |
| `docs/runregistry-extraction-verification.md` | 1948 | \| RunRegistry \| 286 \| OK \| 14.2 \| |
| `docs/runregistry-extraction-verification.md` | 1985 | - `RunRegistry list` shows 37 runs: R0's 33 and this rehearsal's four, all finished but the two |
| `docs/runregistry-extraction-verification.md` | 1993 | `config.datastore`), takes `sgk = RunRegistry.stores.fingerprint_of(inventory)` and |
| `docs/runregistry-extraction-verification.md` | 1994 | `pkg = datastorekit.store_fingerprint.fingerprint_of(inventory, RunRegistry.stores.FINGERPRINT_FORMAT)`, |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_02.txt` | 30 | -- pip show datastorekit raypoolkit runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_02.txt` | 53 | WARNING: Package(s) not found: runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_02.txt` | 83 | runregistrykit -> ModuleNotFoundError: No module named 'runregistrykit' |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_04.txt` | 38 | -- pip show datastorekit raypoolkit runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_04.txt` | 47 | WARNING: Package(s) not found: runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_04.txt` | 73 | runregistrykit -> ModuleNotFoundError: No module named 'runregistrykit' |
| `docs/store-fingerprint-audit.md` | 122 | registry's promise that `import RunRegistry` loads neither `ray` nor `sqlalchemy` |
| `docs/store-fingerprint-audit.md` | 123 | (`RunRegistry/stores.py:45-46`) therefore needs the reader to be imported inside the operation, |
| `docs/store-retirement-audit.md` | 13 | move and fingerprint each go through `RunRegistry.stores` and leave a `history` entry. A plain |
| `docs/store-retirement-audit.md` | 30 | Measured 2026-09-25 at `42d4910`. `RunRegistry list` shows nothing `running`. **[probed]** |
| `docs/store-retirement-audit.md` | 39 | `RunRegistry/stores.py:542-573`). **[probed]** |
| `docs/store-retirement-audit.md` | 95 | that is `None`, and `begin` does not refuse (`RunRegistry/__init__.py:549-553`). **[checked]** Both |
| `docs/store-retirement-audit.md` | 114 | `RunRegistry.stores.copy_store` call". Retirement is that reason. `copy_store` refuses because the |
| `docs/store-retirement-audit.md` | 141 | `RunRegistry/tests/test_store_fingerprint.py` test 12 (`:797-842`), and it counts only `run.finish(` |
| `docs/store-retirement-audit.md` | 165 | - The `RunRegistry/stores.py` docstring (`:47-49`), and the `RunRegistry/__main__.py` docstring |

#### 8. `.gitignore` and the registry

- `.gitignore` ignores `var/`: `:3` `var/`.
- Module-level registry mappings: `factories` at `config/datastore.py:91` (38 keys).
- `def inventory_spec`: 21 in 20 files: `ObjectFactories/BackgroundModel.py:881`, `ObjectFactories/GkNumericIntegration.py:634`, `ObjectFactories/GkSource.py:839`, `ObjectFactories/GkSourcePolicy.py:69`, `ObjectFactories/GkSourcePolicyData.py:177`, `ObjectFactories/GkWKBIntegration.py:960`, `ObjectFactories/LambdaCDM.py:93`, `ObjectFactories/OneLoopIntegral.py:341`, `ObjectFactories/QCD_Cosmology.py:128`, `ObjectFactories/QuadSource.py:542`, `ObjectFactories/QuadSourceIntegral.py:965`, `ObjectFactories/QuadSourcePolicy.py:106`, `ObjectFactories/TkNumericIntegration.py:636`, `ObjectFactories/TkWKBIntegration.py:959`, `ObjectFactories/integration_metadata.py:58`, `ObjectFactories/redshift.py:133`, `ObjectFactories/store_tag.py:47`, `ObjectFactories/tolerance.py:56`, `ObjectFactories/version.py:47`, `ObjectFactories/wavenumber.py:126`, `ObjectFactories/wavenumber.py:385`.
- `Parent(..., types=...)`: `ObjectFactories/BackgroundModel.py:900` (`COSMOLOGY_TYPES`), `ObjectFactories/wavenumber.py:396` (`COSMOLOGY_TYPES`).
