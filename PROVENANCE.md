# Provenance

`runregistrykit` was imported from **SecondaryGWKit** (SGK):

- **Repository:** <https://github.com/ds283/SecondaryGWKit>, checked out at
  `/Users/ds283/Documents/Code/SecondaryGWKit`.
- **Import commit:** `a45aefc` (`a45aefc702de643c330372dd6d2d983f38bb8eed`), "Freeze RunRegistry/
  for its move to RunRegistryKit". It changes none of the modules imported; the last commit to
  change each before it is:

  | Module | Last changed by |
  |---|---|
  | `RunRegistry/__init__.py` (710 lines) | `f54f1c5`, 2026-10-11, "Record the installed packages in each run's manifest" |
  | `RunRegistry/stores.py` (2185 lines) | `5943492`, 2026-10-12, "Close the dk-and-rpk-migration campaign" |
  | `RunRegistry/__main__.py` (515 lines) | `66617c9`, 2026-09-25, "Add amend_sidecar and store amend, for one unknown field" |

This is a fresh import (decision U2 of `prompts/extraction/README.md` §6.2): SGK's history is not
carried here. How the registry came to be is SGK's history, reachable through the import commit;
the package's docstrings and comments still cite it (SGK's campaigns, prompts and logs) until
prompt 05 rewrites them in the package's own terms. The import was made by
`prompts/extraction/01-import-the-registry.md`.

## The file map, and the fate of every source file

Each of SGK's 25 files under `RunRegistry/` at the import commit, and the shard fixture outside it,
has exactly one fate. `docs/extraction/compare_with_source.py` holds this table as data and checks
it.

| SGK file at `a45aefc` | Blob | Fate | Here |
|---|---|---|---|
| `RunRegistry/__init__.py` | `0228a1a066793332191affe90c4b309a153aa60c` | imported by 01 | `runregistrykit/__init__.py` |
| `RunRegistry/__main__.py` | `88cf6ddd2b7603fc718fd6b3d7ed9722261a874f` | imported by 01 | `runregistrykit/__main__.py` |
| `RunRegistry/stores.py` | `a0f18ba49a25fe795af79baa8f82ce0e09cf3b25` | imported by 01 | `runregistrykit/stores.py` |
| `RunRegistry/tests/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | imported by 01 (empty) | `runregistrykit/tests/__init__.py` |
| `RunRegistry/tests/store_fixtures.py` | `391f31fc2155c1f2d8f2350d306272ee6e0ae54e` | ported by 02 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_run_registry.py` | `01c3ea37d8491c63300667f5a181f3bad91000ab` | ported by 02 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_sidecar.py` | `533d1118447527cfef65a833525516fcadbbc2e7` | ported by 02 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_copy_move.py` | `4be78d983aa83d5d7d39fc440519347cc87386bd` | ported by 02 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_command_line.py` | `6f111e29e9b695340a88bf19eb18a50e89a9ea05` | ported by 02 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_amend.py` | `8b7db110f76ae74bfb4716fe12d7192bac38265e` | ported by 02 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_amend_residuals.py` | `0c6e6a2ca5d59b74dcb960111a5cd05ed2d991f4` | ported by 02 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_retire.py` | `3cf05cc02d6b00849a4eff4972ccbedd0a4fa51d` | ported by 04b, onto the neutral store | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_retire_references.py` | `9a3264a7f5977311161f724651b4e1d27cfa0866` | ported by 04b, onto the neutral store | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_fingerprint.py` | `5039b4792210c1227230ec09b48da641b6f62e9f` | ported by 04a, onto the neutral store, less `TestGolden` and `TestDrivers`, which stay in SGK | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_build_rehearsal_scope.py` | `8b3c8519d3956b97cce84ea8224c621f37d88cd0` | not imported: SGK's | — |
| `RunRegistry/tests/test_killed_handler.py` | `213f2a8d7d017f845b85ea209f8e87886539988b` | not imported: SGK's | — |
| `RunRegistry/tests/test_pipeline_adoption.py` | `f3205799afa5626fe440e409fce37c1cb9fa04c7` | not imported: SGK's | — |
| `RunRegistry/tests/test_prune_on_resume.py` | `23533e68f7682a172ecf7246b84bbd749b1e5ff8` | not imported: SGK's | — |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | `527a9878d588309fd6f82f214bc655be627cea5d` | not imported: SGK's | — |
| `RunRegistry/tests/data/full_store_fingerprint.json` | `58b35c3677f40e5421c7390ac282f1e6e808cd68` | not imported: SGK's | — |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-07.json` | `2fea28b072cd9f4cdb15062ab355c9c08a45d57e` | not imported: SGK's | — |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-08.json` | `511ff2d3873437480cbb6af028ba8fbdc5699b87` | not imported: SGK's | — |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09a.json` | `bd6a855c9d109a8da654ab790eadfc681ad5cea8` | not imported: SGK's | — |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09b.json` | `01d7ef02e88c53a4160e5660711f0746f3ae4a90` | not imported: SGK's | — |
| `RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09c.json` | `6cf0a39496c0e96bd3b2640324482e7d51686908` | not imported: SGK's | — |
| `StoreFixtures/shard_store_fixtures.py` (outside `RunRegistry/`) | `1375949aacde2263de991785055cd7dfabc57251` | ported by 02 (U4) | `runregistrykit/tests/shard_store_fixtures.py` |

`StoreFixtures/real_store_fixtures.py` (blob `a6d90b86f2517c4e7cc798897534be8ed4b3d7c6`) is not
imported: it imports SGK's `config` and `ObjectFactories`. It is replaced by
`runregistrykit/tests/neutral_store.py`, 04a.

**New here, with no source:**

- `pyproject.toml`: the distribution `runregistrykit`, version `0.1.0.dev0` (decision U3), with no
  core dependency and the store layer's `datastorekit` in the optional extra `stores`;
- `runregistrykit/tests/test_package_imports.py`: the import test (prompt 01 §2.7);
- `docs/extraction/compare_with_source.py`: the equivalence check, below;
- this file.

## The differences allowed

The three modules and `tests/__init__.py` (prompt 01), and the eight test and fixture files
(prompt 02), equal their sources at `a45aefc` except for these classes of difference (prompt 01
§2.4, prompt 02 §2.3). Nothing else differs.

- **D-name, the package's name.** Every whole-word occurrence of `RunRegistry` (the regular
  expression `\bRunRegistry\b`) becomes `runregistrykit`, and nothing else on the line changes: the
  CLI's `prog`, the `python -m RunRegistry …` text of the error messages, the docstrings and
  comments, and in the tests the imports, `runpy.run_module("RunRegistry", …)`, `sys.argv` and the
  `-m RunRegistry` of the child processes. 106 lines in all: 23 in the package (6 in `__init__.py`,
  13 in `stores.py`, 4 in `__main__.py`) and 83 in the tests (31, 6, 15, 10, 11, 8, 2 and 0, in the
  order of the table: `test_run_registry.py`, `store_fixtures.py`, `test_store_sidecar.py`,
  `test_store_copy_move.py`, `test_store_command_line.py`, `test_store_amend.py`,
  `test_store_amend_residuals.py`, `shard_store_fixtures.py`). The rule is uniform, so one renamed
  comment, `stores.py:197`, now cites a path that does not exist here
  (`runregistrykit/tests/data/full_store_fingerprint*.json`, SGK's golden fingerprints).
- **D-fix, the shard fixture's new home.** `\bStoreFixtures\.shard_store_fixtures\b` becomes
  `runregistrykit.tests.shard_store_fixtures`, and `\bStoreFixtures/shard_store_fixtures\.py`
  becomes `runregistrykit/tests/shard_store_fixtures.py` (decision U4: the fixture is carried as it
  is, under `tests/`). 5 lines: the three imports (`store_fixtures.py:20`,
  `test_store_sidecar.py:28`, `test_store_copy_move.py:32`) and two docstrings
  (`store_fixtures.py:4`, `test_store_amend.py:15`). The imports are absolute, as SGK's were.
- **D-fmt, formatting.** `black` 25.1.0, with no configuration, applied to the renamed source. It
  changes nothing in the three modules and the other eleven files, but D-name lengthens three code
  lines of `test_store_copy_move.py` past 88 columns and `black` reflows them: source `:73` (1 line
  becomes 4, a dict split with a trailing comma `black` adds, package `:73-76`), `:135` (1 becomes
  5, package `:138-142`) and `:211` (1 becomes 3, package `:218-220`). **3 source lines, 12 package
  lines, in 3 hunks, all in that file**, which goes from 601 lines to 610. From `:73` on, that
  file's package line numbers are no longer SGK's; every other file's are.

The three reflowed lines are three of that file's ten D-name lines as well, since they were reflowed
because D-name lengthened them. No line needs both D-name and D-fix.

**Imported unchanged:** the couplings to SGK that README §0.2 lists as C1–C9 (the root as the
package's parent, the runs and stores roots under it, SGK's recorded distributions, the lazy
`from config.datastore import factories` in `fingerprint_store`, SGK's fingerprint format and its
own copy of layer C, the prose citing SGK) and the further couplings measured there. They are the
`extraction` board's §3 issues, owned by prompts 03–05. As imported, the package cannot run
installed: `REPO_ROOT` is the package's parent (in this repository's editable install, this
repository's root, whose `var/` the gitignore covers), and `fingerprint_store` imports SGK's
`config`.

## Re-running the check

At `8155445`, from the repository root, with the repository's venv (the check is retired: from
prompt 03 on, run it from a worktree of that commit, as the end of this section says):

```bash
./venv/bin/python docs/extraction/compare_with_source.py
```

It reads SGK only with `git -C /Users/ds283/Documents/Code/SecondaryGWKit ls-tree|rev-parse|show
a45aefc…`, never SGK's working tree, and imports nothing of SGK or of this package. It checks that
`RunRegistry/` at the import commit is still the 25 rows of the table above, path and blob, and the
shard fixture its blob; that every imported or ported file exists here and every other file under
`runregistrykit/` is declared; that no file left in SGK is here; and, for each of the twelve files
checked, that:

1. T, the *renamed source* (the source with D-name and D-fix applied to every line, one line for
   one line), is formed, counting the lines each changed;
2. the package file equals `black.format_str(T, mode=black.Mode())` exactly; the lines where
   `black(T)` differs from T are D-fmt, counted and printed hunk by hunk;
3. any line where the package differs from `black(T)` is printed as UNCLASSIFIED, with its package
   line number, and fails the check; nothing is widened to accept a difference;
4. no line of the package file still holds the word `RunRegistry` or `StoreFixtures`.

Files ported by a later prompt are reported as pending while absent, and fail if present. The rule
names no line number. **The check needs `black` 25.1.0**: it imports it and exits 2 (cannot run)
if it is missing or another version, so the reflows it accepts are those of the version recorded
here. It uses `black.Mode()`, which infers target versions from each file's content; `black` run at
the root reads `pyproject.toml` instead and infers `py312`, `py313` from `requires-python`. On all
twelve files the two give the same output (measured), and `black --check runregistrykit docs` would
show it if they ever differed. It exits 0 only when all of that holds; the rules are stated in its
docstring.

The check held through prompt 02, while the package was the import and the ported tests. **It was
retired at prompt 03's start**, when the package began to change in its own right (README §4). It
describes 02's tree, `8155445`, and fails by design on any later one. To re-run it, make a worktree
of that commit outside this checkout, run the check there with this checkout's venv, and remove the
worktree:

```bash
git worktree add --detach <scratch>/check-02 8155445
(cd <scratch>/check-02 && /Users/ds283/Documents/Code/RunRegistryKit/venv/bin/python \
    docs/extraction/compare_with_source.py)
git worktree remove <scratch>/check-02
```

It exits 0 there (measured at prompt 03's start, 2026-10-14). Changes since are listed below,
under "Since the import".

## The freeze

SGK froze its `RunRegistry/` at the import commit, by its own `CLAUDE.md`, until it adopts this
package (gate G2 of `prompts/extraction/README.md` §7). A fix wanted in SGK's registry is made here,
and reaches SGK when it adopts a release. The import edited no client: SGK was read only through
`git`.

## Since the import

The package has changed in its own right since `8155445`, the tree the equivalence check describes.
Each prompt's changes, from 03 on:

**Prompt 03, the root and the client config** (`prompts/extraction/03-the-root-and-the-client-config.md`,
`035e4b5`):

- **The config file.** A client marks its root with `runregistrykit.toml`, read with `tomllib`:
  `runs_root` (default `var/runs`), `stores_root` (default `var/datastores`), `distributions`
  (default none) and a `[stores]` table, reserved for prompt 04. Its form is documented in the new
  module `runregistrykit/client.py`, which holds `CONFIG_FILE`, `ConfigError`, `ClientRoot` and
  `find_client_root`, standard library only.
- **The root rule.** The root is found by walking up from where a call starts (for `begin()`, the
  script's directory, else the working directory; for everything else, and the command line, the
  working directory) to the first directory holding the file, or is named by `client_root=` or
  `--client-root`. None found is a `ConfigError`, never a fallback. A run launched from a linked
  git worktree is recorded under the main checkout (SGK's Q3), with its own tree's `git_head`,
  `git_dirty` and script hash; a bare repository's worktree is refused. Paths in records stay
  relative to the record root where they lie under it, so records written before read as they did.
- **The names deleted.** `REPO_ROOT`, `DEFAULT_ROOT`, `DEFAULT_STORES_ROOT` and
  `RECORDED_DISTRIBUTIONS`. `git_provenance(cwd)` and `package_provenance(names)` lose their
  defaults, and `_repo_path` and `_resolve` take the root. Every public function that needs the
  root takes `client_root=`; the command line's `list --root`, `--runs-root` and `--stores-root`
  default to the config's.
- **U9.** A manifest's `packages` records `runregistrykit` always, then the config's
  `distributions`.
- **The tests.** The ported tests' fixtures build a client root of their own in a `tempfile`
  directory (`runregistrykit/tests/client_fixtures.py`, new); their bodies change only as that
  prompt's §2.7 lists, and `test_the_recorded_names_are_the_two_packages` is renamed
  `test_the_recorded_names_are_the_registry_and_the_configs`. `runregistrykit/tests/test_client_root.py`
  is new.

**Prompt 04a, the client fingerprinter** (`prompts/extraction/04a-the-client-fingerprinter.md`,
`c81ad06`):

- **The fingerprinter.** A new module, `runregistrykit/fingerprint.py`, standard library only at
  module scope: the runtime-checkable protocol `Fingerprinter` (`take`, `compare`, `describe`,
  `listing`); `DatastoreKitFingerprinter(factories, fingerprint_format)`, a ready-made one over
  DatastoreKit's `read_inventory`, `fingerprint_of`, `compare_fingerprints` and `listing_lines`,
  which a client instantiates with its registry and its format number; and `load_fingerprinter`
  and `require_fingerprinter`. A client names its fingerprinter in `runregistrykit.toml` as
  `[stores] fingerprinter = "module:attribute"`, whose form is checked when the file is read; it is
  imported, with the client root first on `sys.path`, only where a fingerprint is taken, compared,
  described or listed (`fingerprint_store`, `write_listing`, `store fingerprint`). Every store
  operation, and every `store` command, refuses without one, before anything is read, written or
  deleted (SGK's D4); the core needs none.
- **Layer C and the format deleted.** The package's own copy of the fingerprint functions, SGK's at
  `a45aefc` `stores.py:1152-1399` (`_sha256_lines`, `_tag_sets`, `fingerprint_of`, `_tags_text`,
  `_difference`, `_presence`, `compare_fingerprints`, `listing_lines`), and `FINGERPRINT_FORMAT = 6`
  with its history, SGK's `:194-206`, are deleted. DatastoreKit holds the functions since `v0.4.0`
  (`datastorekit.store_fingerprint`); SGK's format and its history (formats 2 to 6) stay in SGK,
  which names its format in its own fingerprinter. `fingerprint_store` keeps its order, its
  refusals and what it writes; its `taken` stamp is built before the fingerprinter reads the store.
  The text `store fingerprint` printed of the classes and problems is now the
  `DatastoreKitFingerprinter`'s `describe`.
- **What the package reads of a fingerprint** (U7): `fingerprint_format`, `encoding_format` when
  present, `digest`, the `taken` it builds, and each comparison entry's `kind` and `text`. The
  sidecar reader no longer requires `classes`, and never requires `encoding_format`, so every
  fingerprint written before reads as it did.
- **The tests.** `runregistrykit/tests/neutral_store.py`, new, is a small fingerprintable store on
  public `datastorekit` names only, with the neutral registry and its fingerprinter, which every
  test's client root names; it replaces SGK's `real_store_fixtures`. SGK's `test_store_fingerprint`
  is ported onto it, 29 tests, its classes and table names neutral in constants and literals only,
  the removed names reached through shims in the test module, and two variants of
  `test_each_malformed_fingerprint_is_a_problem` (`"no classes"`, `"classes a list"`) removed under
  U7. `runregistrykit/tests/test_fingerprinter.py` is new. In `test_client_root.py`,
  `test_the_stores_table_is_accepted_and_kept` is renamed
  `test_the_fingerprinter_is_kept_and_another_stores_key_refused`, and one test's config names the
  neutral fingerprinter.

**Prompt 04b, the retire tests** (`prompts/extraction/04b-the-retire-tests.md`, `5302a6f`):

- **The tests.** SGK's `test_store_retire` (41 tests) and `test_store_retire_references` (10) are
  ported onto the neutral store, each keeping its module, class and method name and what it
  asserts: the package's name, the fixtures' new homes, the neutral registry and class name
  (`QSI = "Integral"`) in a constant only, the test's client root for SGK's `REPO_ROOT` (in the
  `_repo_path` calls, the paths computed against it, and the child process's working directory and
  path), and `black`; `compare_fingerprints`, which `runregistrykit.stores` no longer has, is a shim
  in the test module, the neutral fingerprinter's `compare`. With them every SGK test this
  campaign imports is ported, and the one test that reaches the store layer's match on
  DatastoreKit's message text, `TestWithoutFingerprint.test_an_unreadable_shards_table`, runs here.
- **`store retire` loads the fingerprinter first.** On a first retirement `retire_store` loads the
  client's fingerprinter after its reason, sidecar and in-use refusals and before it plans the
  store's files, so a fingerprinter that cannot be loaded is a `ConfigError`, before anything is
  written, with `--without-fingerprint` or not; the flag records only a failure of the fingerprint
  itself. The completion of an incomplete retirement loads none. No record changes form.
- **The loader refuses a class.** `load_fingerprinter` refuses a class (such as
  `DatastoreKitFingerprinter` named in place of an instance of it), which a runtime-checkable
  protocol's check would let through, as a `ConfigError` naming the config file and the spec.
- `runregistrykit/tests/test_fingerprinter.py` gains eight tests of the two.
