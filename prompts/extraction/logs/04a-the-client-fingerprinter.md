# Log — prompt 04a: the client fingerprinter

**Subject:** Name the client fingerprinter in the config and delete layer C
**Commit:** this commit (on `main`, after `9dc34a5`)
**Date:** 2026-10-15
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and the orchestration
note's §0 (`orchestrator-note-04a-section0.md`)
**Result:** **landed.** The package no longer computes a fingerprint. A client names its
fingerprinter in `runregistrykit.toml` (`[stores] fingerprinter = "module:attribute"`); the new
module `runregistrykit/fingerprint.py` holds the protocol `Fingerprinter`, the ready-made
`DatastoreKitFingerprinter(factories, fingerprint_format)` over DatastoreKit's functions, and the
loader. Every store operation and every `store` command refuses without one (D4), reading the
config only. Layer C, `FINGERPRINT_FORMAT` and the `config.datastore` import are deleted;
`fingerprint_store` keeps its order, refusals and writes. The sidecar reader reads only U7's fields.
A neutral store of the package's own (`runregistrykit/tests/neutral_store.py`, public `datastorekit`
names only) replaces SGK's `real_store_fixtures`, and SGK's `test_store_fingerprint` is ported onto
it, 29 tests. The suite: **135 → 186** (`135 + 29 + 22`), `Ran 186 tests … OK`. (m1)–(m11) each fail
at least one test. No stop condition was met. Three issues closed
(`[00-the-fingerprint-reads-a-clients-registry]`, `[00-the-store-layer-reads-inside-a-fingerprint]`,
`[02-the-sidecar-readers-guards-are-unpinned]`); `docs/OPEN_ISSUES.md` goes from 7 to 4.

## What shipped

| File | What |
|---|---|
| `runregistrykit/fingerprint.py` | **new**, standard library and the package only at module scope: `Fingerprinter` (a `runtime_checkable` `Protocol`: `take`, `compare`, `describe`, `listing`); `DatastoreKitFingerprinter(factories, fingerprint_format)`, which refuses a bad format as `fingerprint_of` does and imports DatastoreKit inside its methods (`take`: `read_inventory` then `fingerprint_of(inventory, fingerprint_format, taken)`, the reader's refusal unwrapped; `compare`: `compare_fingerprints`; `describe`: the text `_print_fingerprint` printed from `classes:` on, as lines; `listing`: `listing_lines`); `require_fingerprinter(client)` (the D4 check: the spec, or a `ConfigError` naming the file and what to add; imports nothing); `load_fingerprinter(client)` |
| `runregistrykit/client.py` | `[stores]` holds one key, `fingerprinter`, checked by form when the file is read (`_is_fingerprinter_spec`); any other `[stores]` key, or another type or form, a `ConfigError` naming the file, the key and the value; the docstring's `[stores]` row and one parenthesis |
| `runregistrykit/stores.py` | layer C (`:1180-1427` at `035e4b5`, but its section heading, kept with a new three-line comment), `FINGERPRINT_FORMAT` and its history (`:189-202`), the `hashlib` and `Counter` imports deleted; `TAKEN_KEYS` kept; `from .fingerprint import load_fingerprinter, require_fingerprinter`; `require_fingerprinter(client)` right after the locate in `create_sidecar`, `adopt_sidecar`, `copy_store`, `move_store`, `fingerprint_store`, `retire_store`, `amend_sidecar` and `write_listing`; `_fingerprint_problems` as U7; `write_listing(…, *, client_root=None)`; `fingerprint_store`'s steps 2–4 and its comparison through the fingerprinter, its `malformed` entry from `_malformed_entry`; the module docstring's fingerprint row and paragraph |
| `runregistrykit/__main__.py` | `_print_fingerprint(fingerprint, fingerprinter)`: `digest:`, `format:`, then `describe`; `_fingerprint` loads the fingerprinter after `fingerprint_store` returns, inside its `except RuntimeError`, and passes `client_root` to `write_listing`; `_store` makes the D4 check first; `_short` moved to `fingerprint.py` |
| `runregistrykit/tests/neutral_store.py` | **new**: the neutral registry `FACTORIES` (nine factories), `NEUTRAL_FORMAT = 1`, `FINGERPRINTER`, the content, and the names the ported test imports (`FIXED_TIMESTAMP`, `_schema_tables`, `build_full_store`, `file_state`, `full_rows`, `relabel_serials`), `COMPUTE_TARGETS`, `SOLVER_COLUMNS` and the class names |
| `runregistrykit/tests/test_store_fingerprint.py` | **new**, ported from SGK's at `a45aefc` by §2.8's classes (below): 29 tests |
| `runregistrykit/tests/test_fingerprinter.py` | **new**: 22 tests (§2.9) |
| `runregistrykit/tests/client_fixtures.py` | `DEFAULT_CONFIG` (the neutral fingerprinter), the default of `write_client_root` and `enter_client_root`; `enter_client_root_for_class` (correction 8) |
| `runregistrykit/tests/test_client_root.py` | correction 2's two tests only |
| `runregistrykit/tests/test_package_imports.py` | `MODULES` gains `fingerprint.py` |
| `PROVENANCE.md` | the file-map row of `test_store_fingerprint.py`, the paragraph on `real_store_fixtures.py`, and 04a's section under "Since the import" |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

`runregistrykit/` gains exactly `fingerprint.py`, `tests/neutral_store.py`,
`tests/test_store_fingerprint.py` and `tests/test_fingerprinter.py`. Not touched:
`runregistrykit/__init__.py`, `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `.idea/`,
`CLAUDE.md`, `docs/extraction/`, `tests/__init__.py`, `store_fixtures.py`,
`shard_store_fixtures.py`, every other 02 or 03 test file, the campaign README, the prompt,
`prompts/extraction/orchestrator/`.

**`fingerprint_store`, as built.** Locate; the D4 check (`ConfigError`, nothing read); then step 1
exactly as before (the tombstone refusal, then the running-run refusal, texts unchanged); step 2
`load_fingerprinter(client)`; step 3 `taken` (`when`, `git_head`, `git_dirty` from
`git_provenance(os.getcwd())`, `run_id`), built as before but now **before** the store is read;
step 4 `fingerprint, inventory = fingerprinter.take(primary, taken)`; step 5 `read_sidecar`, then
`_malformed_entry` for a malformed recorded fingerprint or `fingerprinter.compare(recorded,
fingerprint)`; step 6 exactly as before. The return value's keys are unchanged; `inventory` is the
fingerprinter's.

**What the package reads of a fingerprint (U7), as built.** `_fingerprint_problems`: an object; an
integer (not `bool`) `fingerprint_format`; if present, an integer (not `bool`) `encoding_format`; a
64-hex lowercase `digest`; an object `taken`. `retire_store` reads `digest` and `taken.when` and
each entry's `text`; `__main__._fingerprint` reads `digest`, `taken` and each entry's `text`;
`_print_fingerprint` reads `digest` and `fingerprint_format`. Nothing else in the package reads a
fingerprint's keys.

**The loader, as built.** `require_fingerprinter`; `module:attribute` split at the colon;
`client.found` inserted at `sys.path[0]` if not already on `sys.path` (string equality), and left;
`importlib.invalidate_caches()`; `importlib.import_module`; `getattr` along the dotted attribute;
`isinstance(…, Fingerprinter)`. Any `Exception` from the import is a `ConfigError` naming the
config file, the spec, and the exception's type and text; a missing attribute and a non-fingerprinter
likewise name the file and the spec.

### The mapping of SGK's names to the neutral store's

| SGK (`real_store_fixtures`, `test_store_fingerprint`) | Neutral (`neutral_store.py`) | What the ported tests need of it |
|---|---|---|
| `QuadSourceIntegral` (`QSI`) | `Integral` (`INTEGRAL`) | sharded, tagged, a leaf class (nothing references it); 3 rows, serials 1 and 2 on shard 0, 3 on shard 1; tag sets `[Run_fixture]` ×2 (serial 3 among them) and `[Run_fixture, grid-A]` ×1 |
| `QuadSourceIntegral_tags` | `Integral_tags` | `(timestamp, parent_serial, tag_serial)`, no serial |
| `TkNumericIntegration` (`TKN`) | `Solution` (`SOLUTION`) | sharded, tagged, `validated` (serial 3 on shard 0 not validated), a value table; serials 1, 3 on shard 0 and 2 on shard 1 |
| `TkNumeric_tags` | `Solution_tags` | `(timestamp, solution_serial, tag_serial)` |
| `TkNumericValue` | `SolutionValue` (`SOLUTION_VALUE`) | serials 11–13, 31–32 on shard 0; 21–24 on shard 1, serial 24 belonging to solution 2 |
| `BackgroundModel` | `Background` (`BACKGROUND`) | replicated; `label` and `solver_serial` outside identity; a `Parent` of `version` |
| `wavenumber` (the shard key) | `mode` (`MODE`) | replicated; `shard_keys` and `relabel_serials`' keys are mode serials (`{1: 0, 2: 1}`) |
| `COMPUTE_TARGETS`, nine classes | `("Solution", "Integral")` | the labelled set with `"Background"` |
| `SOLVER_COLUMNS = ("solver_serial", "phase_solver_serial", "friction_solver_serial")` | `("solver_serial",)` | on `Background`, `Solution` and `Integral`, outside identity |
| `version`, `store_tag` | the same (`VERSION_TABLE`, `TAG_TABLE` of `datastorekit.contract`) | identity is the label; neither in the labelled set |
| tag labels `Run_fixture`, `grid-A`, `unused-tag` | the same, serials 1, 2, 3 | `unused-tag` on no row |
| `config.datastore.factories` (`_factories`) | `FACTORIES` | nine factories, six with an `inventory_spec` |
| `FINGERPRINT_FORMAT = 6` | `NEUTRAL_FORMAT = 1` | — |
| `FIXED_TIMESTAMP = datetime(2026, 9, 24, 12, 0, 0)` | the same | every row's `timestamp` unless given |
| `build_full_store(…, stem="full-store", shards=2, …, missing_tables, missing_columns, extra_sql)` | `build_full_store(directory, stem="full-store", shards=2, replicated=None, sharded=None, shard_keys=None, extra_sql=None)`, returning `NeutralStore(primary, shard_files)` | no `missing_*`: the ported tests pass none |

Every row's `timestamp` is outside identity, every reference is a foreign key to the target's
`serial` (from which `relabel_serials`' `references()` is derived), and every reference that is
identity is a `Parent`. Measured on the built store: the six inventory classes in the order
`version, store_tag, mode, Background, Solution, Integral`; `problems == {}`;
`inventory[Integral].earliest_timestamp == FIXED_TIMESTAMP`; about 30 ms a build; `ray` imported
and never initialised.

## Deviations from the prompt

The note's ten corrections and readings are recorded as found (1–10); the rest are this agent's.

1. **The gate's diff is not empty** (correction 1, found as it says). `git diff --stat f9e0e60 HEAD
   -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` shows `docs/OPEN_ISSUES.md`,
   changed by `2ecb99d`; the same diff from `2ecb99d` is empty, and the gate was read from there.
   **STRUCTURALLY REQUIRED.**
2. **Two 03 tests changed** (correction 2), both in `test_client_root.py`, and no other 02 or 03
   test: (a) `TestConfig.test_the_stores_table_is_accepted_and_kept` is renamed
   **`test_the_fingerprinter_is_kept_and_another_stores_key_refused`**: a config holding only
   `fingerprinter = "a.module:an_attribute"` is accepted and kept, and the old config, with
   `[stores.more] n = 1`, is a `ConfigError` naming the file, `'more'` and `{'n': 1}`.
   `test_each_key_is_read` is unchanged. (b)
   `TestWalk.test_a_live_sidecar_reads_with_no_config_and_a_tombstone_does_not`: its `a_config("")`
   becomes `a_config` of the neutral fingerprinter's `[stores]` table, nothing else. With only §2.8's
   changes (no new test yet), the suite was `Ran 164 tests … OK`. **STRUCTURALLY REQUIRED.**
3. **`fingerprint_store`'s docstring and its `taken`** (correction 3). Its steps 2–4 are rewritten
   to §2.5's; step 5's docstring names "the fingerprinter's `compare`" for `compare_fingerprints`,
   because §2.5 changes what step 5 calls; one sentence before step 1 says the D4 refusal comes
   first; the return paragraph says `inventory` is the fingerprinter's. `taken` is now built before
   the store is read (`git_provenance` and `now_iso()` ran after `read_inventory`), because the
   protocol hands it to `take`. No other step moved, and no refusal's text changed.
   **STRUCTURALLY REQUIRED.**
4. **The read-refusal test checks the type and the text** (correction 4, recommendation followed):
   `TestThroughTheFingerprinter.test_a_read_refusal_comes_through_as_the_readers_own` asserts
   `type(e) is type(direct)` and `str(e) == str(direct)`, `direct` being what `read_inventory(primary,
   FACTORIES)` raises on the same store, for a journal beside shard 0 (a plain `RuntimeError`) and for
   a shard missing `Integral_tags` (`StoreSchemaMismatch`). (m5) is the hardest wrap,
   `raise RuntimeError(str(e)) from e`, which keeps the text: only the second case fails it.
   **IMPLEMENTATION CHOICE.**
5. **The precedence test** (correction 5, recommendation followed):
   `TestPrecedence.test_a_tombstone_and_a_running_run_come_before_the_fingerprinter`, with a config
   naming `no_such_module_<hex>:FINGERPRINTER`: with nothing to refuse first, `fingerprint_store`
   raises the `ConfigError` (`ModuleNotFoundError`); with a running run naming the store it raises
   the running-run refusal, in process and through `store fingerprint` (whose stderr names the run
   and not the spec); with a tombstone, the tombstone refusal; neither a `ConfigError`. The CLI's
   `_fingerprint` loads the fingerprinter for `describe` after `fingerprint_store` returns, inside
   its `except RuntimeError`, as the note reads it. (m10) moves the load before the running-run
   refusal; (m11), the agent's besides, loads it in `_fingerprint` before `fingerprint_store`. Both
   fail this test. **IMPLEMENTATION CHOICE.**
6. **The loader in tests** (correction 6, as found). Every test that loads a module from a client
   root uses a fresh name (`client_fingerprinter_<hex>`), restores `sys.path` and drops the module
   from `sys.modules` in a cleanup (`a_module_name`). The (m6) test checks
   `importlib.util.find_spec(name) is None` before the load, from a subdirectory of the root. The
   loader calls `importlib.invalidate_caches()` before the import (IMPLEMENTATION CHOICE), and leaves
   `found` on `sys.path`, so the in-process suite gains one entry per client root whose fingerprinter
   is loaded (each a deleted `tempfile` directory): harmless, as the note says. **IMPLEMENTATION
   CHOICE.**
7. **(m3) and the D4 check** (correction 7, as found): the neutral store imports `datastorekit` at
   module scope, so loading its fingerprinter loads `ray` and `sqlalchemy`, and 02's
   `test_show_create_adopt_copy_and_move` and the ported `test_read_only_then_write_then_matches`
   both fail (m3). `require_fingerprinter` reads `client.stores` and imports nothing; the CLI's check
   is in `_store`, before any command runs. **STRUCTURALLY REQUIRED.**
8. **The class fixture** (correction 8): `enter_client_root_for_class(cls, config=DEFAULT_CONFIG)`
   beside `enter_client_root`, registering the directory's cleanup and then the `os.chdir` back with
   `cls.addClassCleanup`. `DEFAULT_CONFIG` is the default of **both** `write_client_root` and
   `enter_client_root`, so that every client root a 02 or 03 test makes, the worktree tests' main
   checkouts included, names a fingerprinter; no test that passes its own config changed. **IMPLEMENTATION
   CHOICE.**
9. **What the ported literals assume** (correction 9, each as found):
   - `FIXED_TIMESTAMP` is SGK's, so `test_no_timestamp_is_in_any_record` checks `"2026-09-24"` and
     `test_adding_a_tag_to_one_record` inserts a timestamp the store holds;
   - `build_full_store(directory, stem="store")`'s shard 1 is `store-shard0001.sqlite`, by
     `shard_file_name`;
   - **`shard_keys`** are checked (each must name an existing shard, else `ValueError`) and written,
     by `sqlite3`, into a `shard_keys (key_serial, shard_id)` table of the primary, which nothing
     reads; `relabel_serials` relabels them by the `mode` mapping, as SGK's by `wavenumber`'s;
   - **labels**: the labelled set is `Solution`, `Integral` and `Background`; the identity labels
     are `version`'s and `store_tag`'s, in neither; every row has a `timestamp` and three classes a
     `solver_serial`, so `changed`'s three counts are positive;
   - **`TestFormats`** passes unchanged through the shim: both hand-built fingerprints lack
     `encoding_format`, and DatastoreKit's comparison reads `None` on both sides (measured: both
     tests pass);
   - `QSI`, `TKN`, `COMPUTE_TARGETS` and `SOLVER_COLUMNS` stay module-level names of the ported
     module at their places, as **literals**; `test_fingerprinter.TestNeutralStore`'s third test
     checks they equal the neutral store's names, and that the ported `_factories` is `FACTORIES`.
   **IMPLEMENTATION CHOICE.**
10. **The suite takes longer** (correction 10): 34.1 s before, 44.9 s with the port only, 53.0–60.9 s
    after (every run listed below). **STRUCTURALLY REQUIRED** (the machine).
11. **The fingerprinter's form is read as "each part an identifier"**: `_is_fingerprinter_spec`
    requires one colon and every dotted part of both sides to be `str.isidentifier()`, which
    excludes whitespace, empty parts and a leading digit. A module that is not a dotted identifier
    cannot be imported by name anyway. **IMPLEMENTATION CHOICE.**
12. **`require_fingerprinter` is a public function of `fingerprint.py`**, used by the store layer's
    operations, the CLI's `_store`, and `load_fingerprinter`, so that the D4 refusal has one text.
    **IMPLEMENTATION CHOICE.**
13. **`write_listing`'s order**: locate, the D4 check, `check_listing_path` (unchanged), then
    `load_fingerprinter`, then the file opened `"x"`: a fingerprinter that cannot be loaded leaves no
    empty listing behind. **IMPLEMENTATION CHOICE.**
14. **`describe` returns lines** where `_print_fingerprint` printed them (the protocol's shape), each
    line's text as before, the `main.py --inventory` line included; `_short`, used only there, moved
    with it. **STRUCTURALLY REQUIRED** (the lines), **IMPLEMENTATION CHOICE** (`_short`).
15. **Prose.** `stores.py`'s module docstring: the `fingerprint` row and the fingerprint paragraph
    say what is now true, keeping the citation "(store-fingerprint prompt 04)", and the import
    paragraph names the fingerprinter; layer C's section heading stays, with a three-line comment.
    `client.py`'s `[stores]` row and one parenthesis. No other prose changed; in particular the
    docstrings of `retire_store` and `amend_sidecar` still say every refusal ends "Nothing was
    written…", which the D4 `ConfigError` does not (observations). **IMPLEMENTATION CHOICE.**
16. **X-drop of the module docstring's items 4 and 12**: the items are removed and the rest are
    **not renumbered** (1–3, 5–11), so that the class docstrings' "Test 5" and so on still match;
    item 11 keeps its trailing `;`. **IMPLEMENTATION CHOICE.**
17. **N-fix is a substitution on every line**, as 02's D-fix was: `StoreFixtures.real_store_fixtures`
    also becomes `runregistrykit.tests.neutral_store` in the module docstring (`:18`). **IMPLEMENTATION
    CHOICE.**
18. **The shims' lines**: `from runregistrykit.stores import (…)` becomes `from
    runregistrykit.stores import fingerprint_store`; after the fixture imports, a two-line comment,
    `from datastorekit.store_fingerprint import fingerprint_of as _fingerprint_of`, `from
    runregistrykit.tests.neutral_store import FINGERPRINTER, NEUTRAL_FORMAT`, then
    `FINGERPRINT_FORMAT = NEUTRAL_FORMAT`, `compare_fingerprints = FINGERPRINTER.compare` and
    `def fingerprint_of(inventory, taken=None)`. **IMPLEMENTATION CHOICE.**
19. **`PROVENANCE.md`'s file map has no row for `real_store_fixtures.py`**: it is the paragraph after
    the table, which now says it is replaced by `neutral_store.py`, 04a. **IMPLEMENTATION CHOICE.**
20. **The neutral store's shape**: nine factories (`SQLAFactoryBase` classes whose `build` raises),
    the names of the mapping table, `build_full_store` refusing fewer than two shards as SGK's did,
    every shard made by `create_all` (no cached empty shard; about 30 ms a store). **IMPLEMENTATION
    CHOICE.**
21. **`DatastoreKitFingerprinter`'s refusals** use their own wording ("DatastoreKitFingerprinter():
    fingerprint_format must be an int, not bool True"), with `fingerprint_of`'s types, which the
    test checks against `fingerprint_of`'s for each value. **IMPLEMENTATION CHOICE.**
22. **Mutations beyond the prompt's**: (m11) (deviation 5). **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT. No ported test failed with only §2.8's changes, and none needed a change outside
its classes. No record changes form: the manifest, `status.json`, `checkpoint.jsonl` and the
sidecar's fields are as before; a fingerprint recorded now carries DatastoreKit's `encoding_format`,
the one addition README §1 plans. DatastoreKit behaved as §2.2 assumes. No stop condition (§5) was
met.

## Verification performed

**At dispatch.** `main` at `9dc34a5`, clean; `git status --short --ignored` showed
`prompts/.DS_Store`, `runregistrykit.egg-info/`, the two `__pycache__/` and `venv/`; this checkout
the only worktree; no `var/`. `venv/`: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy
2.0.39; `git` 2.56.0. No Ray process (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` exit
1); `RAY_ADDRESS` unset. The gate's diff as deviation 1.

**§3.1, the suite**, `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .` from the
root, in the foreground, output to a scratch file:

| | Verdict |
|---|---|
| before (at `9dc34a5`) | `Ran 135 tests in 34.124s`, OK |
| §2.8's changes only, no new test | `Ran 164 tests in 44.868s`, OK |
| after | `Ran 186 tests in 53.022s`, OK; the final run, on the tree committed: `Ran 186 tests in 59.082s`, OK |

**135 → 186**, `135 + 29 + 22`. By loader, after: `test_client_root` 27, `test_fingerprinter` 22
(new), `test_package_imports` 3, `test_run_registry` 29, `test_store_amend` 21,
`test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
`test_store_fingerprint` 29 (new), `test_store_sidecar` 17. Before, every one of those but the two
new modules had the same count. The test ids are 135's but for the one rename (deviation 2), plus
the 51 new. `test_store_fingerprint`'s 29 are SGK's 33 less `TestGolden`'s 3 and `TestDrivers`' 1,
by an `ast` comparison of the two files' `Class.test_method` names: `TestPhysical` 2,
`TestLocalised` 5, `TestNotContent` 2, `TestListing` 2, `TestFormats` 2, `TestSidecarField` 4,
`TestFingerprintCommand` 3, `TestRunningRefusal` 2, `TestFinish` 7. `test_fingerprinter`'s 22:
`TestProtocolAndLoader` 7, `TestTheStoreLayerRequiresOne` 3, `TestPrecedence` 2, `TestOpacity` 2,
`TestThroughTheFingerprinter` 3, `TestNeutralStore` 3, `TestSidecarGuards` 2.

**§3.2, nothing outside temporary directories.** `git status --short --ignored`, less
`__pycache__/`, the same before and after the final run (`diff` empty); no `var/` at the root or
under `runregistrykit/`; `git worktree list` this checkout alone; no Ray process before or after
(`pgrep` exit 1), and none after any mutation's run. `ray.is_initialized()` is never true: every CLI
child reports it (`CommandLineTestCase.command` asserts it false), and
`TestNeutralStore.test_shardedpool_plans_and_deletes_it_with_four_shards` asserts it in process.

**§3.3, the import.** From the empty scratch directory `agent04a/empty` (no `runregistrykit.toml`
in it or above it), `env -u PYTHONPATH ./venv/bin/python -I -c "import runregistrykit,
runregistrykit.stores, runregistrykit.fingerprint, sys; assert not {'ray', 'sqlalchemy',
'datastorekit'} & set(sys.modules)"` exits 0. `test_package_imports`'s `MODULES` gains
`fingerprint.py`, its one change; its module-scope test passes on `fingerprint.py`.

**§3.4, the deletion grep.** `grep -rn "FINGERPRINT_FORMAT\|_sha256_lines\|_tag_sets\|def
fingerprint_of\|def compare_fingerprints\|def listing_lines\|config.datastore" runregistrykit
--include=*.py` finds three lines, all the ported module's shim and its use:
`tests/test_store_fingerprint.py:57` (`FINGERPRINT_FORMAT = NEUTRAL_FORMAT`), `:61` (`def
fingerprint_of(inventory, taken=None) -> dict:`) and `:343` (a test body's
`self.assertEqual(listing["format"], FINGERPRINT_FORMAT)`, through the shim). `neutral_store.py`
holds none of the names (its format is `NEUTRAL_FORMAT`).

**§3.5, the port.** The port script, `agent04a/port/port.py` (outside the repository), reads SGK's
file with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
a45aefc:RunRegistry/tests/test_store_fingerprint.py` (875 lines), applies X-drop by exact blocks,
each checked by its first line, then D-name, N-fix and N-class as substitutions on every kept line,
then `black.format_str(…, mode=black.Mode())`. Its counts: **X-drop 105 source lines** in 10 blocks;
**D-name 7 lines**; **N-fix 3 lines**; **N-class 5 lines**, and `COMPUTE_TARGETS`' 11 lines to 1;
`black` changed nothing; 770 lines kept, 760 out. `diff` of its output and the committed file (768
lines), complete:

```
31,36c31
< from runregistrykit.stores import (
<     FINGERPRINT_FORMAT,
<     compare_fingerprints,
<     fingerprint_of,
<     fingerprint_store,
< )
---
> from runregistrykit.stores import fingerprint_store
54a50,55
> from runregistrykit.tests.client_fixtures import enter_client_root_for_class
> 
> # shims for the names the package no longer has: the fingerprint is the client fingerprinter's,
> # here the neutral store's
> from datastorekit.store_fingerprint import fingerprint_of as _fingerprint_of
> from runregistrykit.tests.neutral_store import FINGERPRINTER, NEUTRAL_FORMAT
55a57,64
> FINGERPRINT_FORMAT = NEUTRAL_FORMAT
> compare_fingerprints = FINGERPRINTER.compare
> 
> 
> def fingerprint_of(inventory, taken=None) -> dict:
>     return _fingerprint_of(inventory, NEUTRAL_FORMAT, taken)
> 
> 
118a128
>         cls.client = enter_client_root_for_class(cls)
443,444d452
<             "no classes": {k: v for k, v in good.items() if k != "classes"},
<             "classes a list": dict(good, classes=[]),
```

By class: the **shim** lines (the `runregistrykit.stores` import, 6 lines to 1; the comment, the two
imports and the three definitions after the fixture imports); the **F-client** lines (the import of
`enter_client_root_for_class`, `:50`, and `cls.client = enter_client_root_for_class(cls)` in
`_FullStores.setUpClass`, `:128`); the two **U7** variants. Nothing else.

**Every instance (README §5 rule 9).** Lines are the committed file's.

- **D-name (7).** The module docstring `:1` (`runregistrykit.stores.fingerprint_of`) and `:3`
  (`python -m runregistrykit store fingerprint`); `import runregistrykit` `:29`; `from
  runregistrykit import stores` `:30`; `from runregistrykit.stores import …` `:31` (then the shim);
  `from runregistrykit.tests.store_fixtures import (` `:32`; `from
  runregistrykit.tests.test_store_command_line import CommandLineTestCase` `:38`.
- **X-drop (105 source lines, 10 blocks, SGK's lines).** Docstring item 4 (`:8`) and item 12
  (`:18-19`); `import ast` (`:25`); `REPO_ROOT` (`:73`); `GOLDEN` (`:74-78`); `DRIVERS` (`:79-82`);
  `TestGolden` and the two blank lines after it (`:347-383`); `_HANDLERS`, its comment and the blank
  lines (`:820-825`); `_finish_calls` and the blank lines after it (`:826-854`); `TestDrivers` and the
  blank lines after it (`:855-873`).
- **N-fix (3, and the shims).** The docstring `:18` (`StoreFixtures.real_store_fixtures` →
  `runregistrykit.tests.neutral_store`, deviation 17); the fixture import `:41`; `from config.datastore
  import factories as _factories` → `from runregistrykit.tests.neutral_store import FACTORIES as
  _factories` `:49`. The shims, `:31` and `:52-62`, as the diff above.
- **N-class (6 places).** `COMPUTE_TARGETS = ("Solution", "Integral")` `:66`; `QSI = "Integral"`
  `:68`; `TKN = "Solution"` `:69`; `SOLVER_COLUMNS = ("solver_serial",)` `:70`; `{"Background"}`
  `:300`; `"DELETE FROM SolutionValue WHERE serial = 24"` `:274`. Every other SGK class in a body is
  reached through `QSI` or `TKN`; `"version"` in `TestSidecarField.FINGERPRINT` (`:413`) is the
  contract's table, unchanged. Method and class names unchanged:
  `test_deleting_one_quadsourceintegral_row` (`:218`) keeps its name, recorded under
  `[02-the-ported-tests-name-sgk]` with the docstrings citing SGK's campaigns (`:1`, `:152`, `:237`)
  and the run id at `:420`.
- **F-client (2 in the module, and the helper).** `:50` and `:128`; `enter_client_root_for_class`
  and `DEFAULT_CONFIG` in `client_fixtures.py` (deviation 8).
- **U7 (2).** `"no classes"` and `"classes a list"` removed from
  `TestSidecarField.test_each_malformed_fingerprint_is_a_problem`'s table (SGK `:504-505`); its other
  12 variants stay.
- **D-fmt.** `black` changed nothing in the port; the committed file is `black`-clean.
- **Correction 2's 03 tests**: deviation 2.

**§3.7.** `./venv/bin/black --check runregistrykit docs`: 21 files would be left unchanged.

**Isolation.** Nothing was installed; no client, DatastoreKit or RayPoolKit was edited or run. SGK
was read only by `git -C /Users/ds283/Documents/Code/SecondaryGWKit show a45aefc:<path>`, for
`RunRegistry/tests/test_store_fingerprint.py` and `StoreFixtures/real_store_fixtures.py`; ChamPBH
and StochasticInstantons were not read. Every scratch file, store and client root was in
`agent04a/` or a `tempfile` directory; no scratch `.py` went under `runregistrykit/` or `docs/`.

## The deliberate-breakage record

Each diff below is exactly as applied, to this commit's tree: it was made by a checked replacement
in the staged file and `git diff` against the index (whose blobs are this commit's), then the file
was restored from the index. A `bash` script then replayed each from its diff file: `git apply
--check`, `git apply`, `git apply -R --check`, the suite (§3.1's command), `git apply -R`, and `git
status --short` compared with the state before. All eleven checked both ways, and the status was
the same after each. None is committed. The suite's verdict and every failing test (a subtest's
label in brackets):

| # | Mutation | The suite | Failing tests |
|---|---|---|---|
| (m1) | `_fingerprint_problems` requiring `classes` again | `Ran 186 … FAILED (failures=3, errors=1)` | FAIL `TestOpacity.test_format_digest_and_taken_are_enough` [the three], [with encoding_format], [with anything else]; ERROR `TestThroughTheFingerprinter.test_what_the_client_fingerprinter_takes_is_recorded` |
| (m2) | `_fingerprint_problems` requiring `encoding_format` | `Ran 186 … FAILED (failures=4, errors=2)` | FAIL `TestOpacity.test_format_digest_and_taken_are_enough` [the three], [with anything else]; FAIL `TestThroughTheFingerprinter.test_a_recorded_fingerprint_without_encoding_format_is_not_compared`; ERROR `TestThroughTheFingerprinter.test_what_the_client_fingerprinter_takes_is_recorded`; FAIL `test_store_fingerprint.TestSidecarField.test_a_well_formed_fingerprint_is_not_a_problem`; ERROR `test_store_fingerprint.TestSidecarField.test_copy_and_move_carry_it_verbatim` |
| (m3) | `store show` loading the fingerprinter | `Ran 186 … FAILED (failures=3)` | FAIL `TestPrecedence.test_the_check_imports_nothing`; FAIL `test_store_fingerprint.TestFingerprintCommand.test_read_only_then_write_then_matches`; FAIL `test_store_command_line.TestStoreCommands.test_show_create_adopt_copy_and_move` |
| (m4) | `create_sidecar` without §2.4's check | `Ran 186 … FAILED (failures=1)` | FAIL `TestTheStoreLayerRequiresOne.test_each_store_operation_is_refused_and_writes_nothing` [create] |
| (m5) | `DatastoreKitFingerprinter.take` wrapping the reader's exception in a `RuntimeError` (of the same text) | `Ran 186 … FAILED (failures=1)` | FAIL `TestThroughTheFingerprinter.test_a_read_refusal_comes_through_as_the_readers_own` [a missing table] |
| (m6) | the loader not putting `client.found` on `sys.path` | `Ran 186 … FAILED (failures=1, errors=3)` | ERROR `TestProtocolAndLoader.test_a_dotted_attribute_is_resolved`, `TestProtocolAndLoader.test_a_module_in_the_client_root_is_found_from_a_subdirectory`, `TestThroughTheFingerprinter.test_what_the_client_fingerprinter_takes_is_recorded`; FAIL `TestProtocolAndLoader.test_each_refusal_is_a_config_error_naming_the_file` [a module that raises] |
| (m7) | `DatastoreKitFingerprinter.compare` comparing copies without `encoding_format` | `Ran 186 … FAILED (errors=1)` | ERROR `TestThroughTheFingerprinter.test_a_recorded_fingerprint_without_encoding_format_is_not_compared` |
| (m8) | `_registry_problems` without its `bool` guard on `sidecar_format` | `Ran 186 … FAILED (failures=1)` | FAIL `TestSidecarGuards.test_a_boolean_sidecar_format_is_a_problem` |
| (m9) | `_STORE_ID.fullmatch` → `.match` on `store_id` | `Ran 186 … FAILED (failures=2)` | FAIL `TestSidecarGuards.test_a_store_id_with_more_after_its_32_characters_is_a_problem` (`'a' * 32 + 'x'`), (`'a' * 33`) |
| (m10) | the agent's, of `fingerprint_store`'s order: the fingerprinter loaded before the running-run refusal (after the tombstone's) | `Ran 186 … FAILED (failures=1)` | FAIL `TestPrecedence.test_a_tombstone_and_a_running_run_come_before_the_fingerprinter` |
| (m11) | the agent's besides: the CLI's `_fingerprint` loading the fingerprinter before `fingerprint_store` | `Ran 186 … FAILED (failures=1)` | FAIL `TestPrecedence.test_a_tombstone_and_a_running_run_come_before_the_fingerprinter` |

Test names without a module are `test_fingerprinter`'s. (m5) is the wrap that keeps the reader's
text, so the journal case passes it and only the type check of the missing-table case fails it
(correction 4); a wrap that changed the text would fail the journal case too.

### The diffs

#### (m1) `_fingerprint_problems` requiring `classes` again (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 420c29f..1ebc358 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -412,6 +412,10 @@ def _fingerprint_problems(value) -> List[str]:
     fmt = value.get("fingerprint_format")
     if isinstance(fmt, bool) or not isinstance(fmt, int):
         problems.append(f"fingerprint's fingerprint_format {fmt!r} is not an integer")
+    if not isinstance(value.get("classes"), dict):
+        problems.append(
+            f"fingerprint's classes {value.get('classes')!r} is not an object"
+        )
     if "encoding_format" in value:
         encoding = value["encoding_format"]
         if isinstance(encoding, bool) or not isinstance(encoding, int):
```

#### (m2) `_fingerprint_problems` requiring `encoding_format` (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 420c29f..18a3153 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -412,8 +412,8 @@ def _fingerprint_problems(value) -> List[str]:
     fmt = value.get("fingerprint_format")
     if isinstance(fmt, bool) or not isinstance(fmt, int):
         problems.append(f"fingerprint's fingerprint_format {fmt!r} is not an integer")
-    if "encoding_format" in value:
-        encoding = value["encoding_format"]
+    if True:
+        encoding = value.get("encoding_format")
         if isinstance(encoding, bool) or not isinstance(encoding, int):
             problems.append(
                 f"fingerprint's encoding_format {encoding!r} is not an integer"
```

#### (m3) `store show` loading the fingerprinter (`__main__.py`, `_show`)

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 2fda31a..6b3e793 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -135,6 +135,7 @@ def _print_retirement(retired) -> None:
 
 
 def _show(args, client) -> int:
+    load_fingerprinter(client)
     reading = stores.read_sidecar(args.primary, client_root=client)
     if reading.retired:
         _print_retirement(reading.fields.get("retired"))
```

#### (m4) `create_sidecar` without the D4 check (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 420c29f..880dd05 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -801,7 +801,6 @@ def create_sidecar(primary, purpose, *, client_root=None) -> dict:
     it. It does not open the primary: whether the store is sound is the constructor's question,
     not the note's."""
     client = find_client_root(client_root=client_root)
-    require_fingerprinter(client)
     primary = Path(os.path.abspath(primary))
     path = sidecar_path(primary)
 
```

#### (m5) `DatastoreKitFingerprinter.take` wrapping the reader's exception (`fingerprint.py`)

```diff
diff --git a/runregistrykit/fingerprint.py b/runregistrykit/fingerprint.py
index 1c94e96..60b3e84 100644
--- a/runregistrykit/fingerprint.py
+++ b/runregistrykit/fingerprint.py
@@ -102,7 +102,10 @@ class DatastoreKitFingerprinter:
         from datastorekit.store_fingerprint import fingerprint_of
         from datastorekit.store_inventory import read_inventory
 
-        inventory = read_inventory(primary, self.factories)
+        try:
+            inventory = read_inventory(primary, self.factories)
+        except Exception as e:
+            raise RuntimeError(str(e)) from e
         return fingerprint_of(inventory, self.fingerprint_format, taken), inventory
 
     def compare(self, recorded, current):
```

#### (m6) the loader not putting `client.found` on `sys.path` (`fingerprint.py`)

```diff
diff --git a/runregistrykit/fingerprint.py b/runregistrykit/fingerprint.py
index 1c94e96..04e9f5e 100644
--- a/runregistrykit/fingerprint.py
+++ b/runregistrykit/fingerprint.py
@@ -165,8 +165,6 @@ def load_fingerprinter(client) -> Fingerprinter:
     where = f"{client.config_file}: [stores] fingerprinter {spec!r}"
 
     # the tree that is running, first, as a script run from the root has it; left there
-    if client.found not in sys.path:
-        sys.path.insert(0, client.found)
     importlib.invalidate_caches()
     try:
         found = importlib.import_module(module_name)
```

#### (m7) `DatastoreKitFingerprinter.compare` ignoring `encoding_format` (`fingerprint.py`)

```diff
diff --git a/runregistrykit/fingerprint.py b/runregistrykit/fingerprint.py
index 1c94e96..7635e71 100644
--- a/runregistrykit/fingerprint.py
+++ b/runregistrykit/fingerprint.py
@@ -108,6 +108,8 @@ class DatastoreKitFingerprinter:
     def compare(self, recorded, current):
         from datastorekit.store_fingerprint import compare_fingerprints
 
+        recorded = {k: v for k, v in recorded.items() if k != "encoding_format"}
+        current = {k: v for k, v in current.items() if k != "encoding_format"}
         return compare_fingerprints(recorded, current)
 
     def describe(self, fingerprint):
```

#### (m8) `_registry_problems` without its `bool` guard (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 420c29f..94e9471 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -571,7 +571,7 @@ def _registry_problems(fields: dict, primary: Path) -> List[str]:
     reader, and by every writer on what it is about to write."""
     problems = []
     fmt = fields.get("sidecar_format")
-    if isinstance(fmt, bool) or fmt != SIDECAR_FORMAT:
+    if fmt != SIDECAR_FORMAT:
         problems.append(
             f"sidecar_format is {fmt!r}; this reader knows format {SIDECAR_FORMAT} only"
         )
```

#### (m9) `_STORE_ID.fullmatch` → `.match` on `store_id` (`stores.py`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 420c29f..354fbec 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -581,7 +581,7 @@ def _registry_problems(fields: dict, primary: Path) -> List[str]:
 
     if "store_id" in fields:
         value = fields["store_id"]
-        if not (isinstance(value, str) and _STORE_ID.fullmatch(value)):
+        if not (isinstance(value, str) and _STORE_ID.match(value)):
             problems.append(
                 f"store_id {value!r} is not 32 lowercase hexadecimal characters"
             )
```

#### (m10) the fingerprinter loaded before the running-run refusal (`stores.py`, `fingerprint_store`)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 420c29f..2e0cac2 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1286,6 +1286,7 @@ def fingerprint_store(
             f'Cannot fingerprint "{primary}": {_tombstone_text(first)}. Nothing was read or '
             f"written"
         )
+    fingerprinter = load_fingerprinter(client)
     store_id = (
         (first.fields or {}).get("store_id") if first.kind == "registry" else None
     )
@@ -1302,7 +1303,6 @@ def fingerprint_store(
         )
 
     # 2. the client's fingerprinter
-    fingerprinter = load_fingerprinter(client)
 
     # 3, 4. the fingerprint, and the inventory, read-only
     provenance = git_provenance(os.getcwd())
```

#### (m11) the CLI loading the fingerprinter before `fingerprint_store` (`__main__.py`, `_fingerprint`)

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 2fda31a..de26883 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -280,6 +280,7 @@ def _fingerprint(args, client) -> int:
     try:
         if args.listing is not None:
             stores.check_listing_path(args.listing, args.primary)
+        load_fingerprinter(client)
         result = stores.fingerprint_store(
             args.primary, write=args.write, runs_root=args.runs_root, client_root=client
         )
```

## Observations not acted on

- **The ported module's `import runregistrykit` is now unused** (`test_store_fingerprint.py:29`): it
  served `REPO_ROOT`, which X-drop removed. Left: removing it is outside §2.8's classes, and it is
  harmless.
- **The ported module's docstring names `runregistrykit.stores.fingerprint_of`** (`:1`), which the
  package no longer has, and its item 11 ends in `;` after items 4 and 12 went (deviation 16). Left,
  as rule 9 has it; recorded under `[02-the-ported-tests-name-sgk]` for 05.
- **`retire_store`'s and `amend_sidecar`'s docstrings** say every refusal is a `RuntimeError` ending
  "Nothing was written or deleted" / "Nothing was written"; the D4 refusal is a `ConfigError` (a
  `RuntimeError`) whose text does not end so. Left: §6 limits the prose to what 04a's changes need,
  and the module docstring states D4; 05 rewrites the prose.
- **`load_fingerprinter` leaves the client root on `sys.path`** (as §2.2 specifies), so a
  long-lived process that locates several client roots accumulates entries, and a module in one
  root can shadow a module of the same name for a later one. Within one client, as a script run
  from its root has it, this is the intended behaviour.
- **The protocol check is `isinstance` against a `runtime_checkable` protocol**, which checks that
  the four methods exist, not their signatures; an object with methods of the wrong arity passes
  the loader and fails when called. As §2.2 specifies.
- **`store fingerprint --listing`**: `write_listing` is called outside the CLI's `try`, as before
  04a, so a listing path made between the check and the write raises a traceback rather than an
  `!!` line. Unchanged behaviour.
- **The neutral store's primary is not one `ShardedPool`'s constructor reopens** (it lacks the
  pool's other primary tables), as §2.7 says; the carried shard fixtures still serve the tests that
  reopen a store.

No §3 issue is opened: none of these is a defect in what 04a was asked to do, and each is the
prompt's rule, a ported line rule 9 keeps, or 05's prose.

## State handed to the next prompt

- **The fingerprinter** is `runregistrykit/fingerprint.py`: `Fingerprinter`,
  `DatastoreKitFingerprinter`, `require_fingerprinter`, `load_fingerprinter`, which 07's checklists
  cite. A client's `runregistrykit.toml` names its fingerprinter as `[stores] fingerprinter =
  "module:attribute"`; every store operation and `store` command refuses without one; the core
  needs none. `runregistrykit/__init__.py` does not re-export these names (05's, with U11).
- **The neutral store** is `runregistrykit/tests/neutral_store.py`, and every test's client root
  names its `FINGERPRINTER` (`client_fixtures.DEFAULT_CONFIG`). For **04b**: `build_full_store(…,
  shards=4)` gives 5 files to `ShardedPool.closed_store_files` and `delete_store` (pinned); the retire
  tests' `{QSI}` is `Integral`, its serial 3 on shard 1, and `Integral_tags` takes `(timestamp,
  parent_serial, tag_serial)`, so a row with `parent_serial` 999 and `tag_serial` 3 is an orphan
  tag; `RetireTestCase.a_full_store` can call `fingerprint_store(write=True)` in its client root, and
  `enter_client_root_for_class` serves a class-level fixture. `_SHARDS_TABLE_UNREADABLE` is
  `stores.py:1365-1366`, still reached by no test.
- **The suite is 186**; 04b's count starts there. It takes about a minute.
- The board's §3 has four issues, their package lines at this commit recorded there;
  `docs/OPEN_ISSUES.md` counts 4.
- Not touched: `runregistrykit/__init__.py`, `pyproject.toml`, `CLAUDE.md`, `docs/extraction/`,
  `tests/__init__.py`, `store_fixtures.py`, `shard_store_fixtures.py`; no client, DatastoreKit or
  RayPoolKit was edited or run; nothing installed; nothing pushed or tagged.
