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
| `RunRegistry/tests/test_store_retire.py` | `3cf05cc02d6b00849a4eff4972ccbedd0a4fa51d` | ported by 04 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_retire_references.py` | `9a3264a7f5977311161f724651b4e1d27cfa0866` | ported by 04 | `runregistrykit/tests/`, same name |
| `RunRegistry/tests/test_store_fingerprint.py` | `5039b4792210c1227230ec09b48da641b6f62e9f` | ported by 04, less `TestGolden` and `TestDrivers`, which stay in SGK | `runregistrykit/tests/`, same name |
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
imported: it imports SGK's `config` and `ObjectFactories`, and prompt 04's neutral store replaces
it.

**New here, with no source:**

- `pyproject.toml`: the distribution `runregistrykit`, version `0.1.0.dev0` (decision U3), with no
  core dependency and the store layer's `datastorekit` in the optional extra `stores`;
- `runregistrykit/tests/test_package_imports.py`: the import test (prompt 01 §2.7);
- `docs/extraction/compare_with_source.py`: the equivalence check, below;
- this file.

## The differences allowed

The three modules and `tests/__init__.py` equal their sources at `a45aefc` except for these classes
of difference (prompt 01 §2.4). Nothing else differs.

- **D-name, the package's name.** Every whole-word occurrence of `RunRegistry` (the regular
  expression `\bRunRegistry\b`) becomes `runregistrykit`, and nothing else on the line changes: the
  CLI's `prog`, the `python -m RunRegistry …` text of the error messages, and the docstrings and
  comments; 23 lines in all (6 in `__init__.py`, 13 in `stores.py`, 4 in `__main__.py`). The rule
  is uniform, so one renamed comment, `stores.py:197`, now cites a path that does not exist here
  (`runregistrykit/tests/data/full_store_fingerprint*.json`, SGK's golden fingerprints).
- **D-fmt, formatting.** `black` 25.1.0, with no configuration. It changes nothing: the source is
  black-clean, and every renamed line is inside a docstring, comment or string, which `black` does
  not split. So the check has no D-fmt rule, and every line of the package sits at its line number
  in SGK.

**Imported unchanged:** the couplings to SGK that README §0.2 lists as C1–C9 (the root as the
package's parent, the runs and stores roots under it, SGK's recorded distributions, the lazy
`from config.datastore import factories` in `fingerprint_store`, SGK's fingerprint format and its
own copy of layer C, the prose citing SGK) and the further couplings measured there. They are the
`extraction` board's §3 issues, owned by prompts 03–05. As imported, the package cannot run
installed: `REPO_ROOT` is the package's parent (in this repository's editable install, this
repository's root, whose `var/` the gitignore covers), and `fingerprint_store` imports SGK's
`config`.

## Re-running the check

From the repository root, with the repository's venv:

```bash
./venv/bin/python docs/extraction/compare_with_source.py
```

It reads SGK only with `git -C /Users/ds283/Documents/Code/SecondaryGWKit ls-tree|rev-parse|show
a45aefc…`, never SGK's working tree, and imports nothing of SGK or of this package. It checks that
`RunRegistry/` at the import commit is still the 25 rows of the table above, path and blob, and the
shard fixture its blob; that every imported file exists here and every other file under
`runregistrykit/` is declared; that no file left in SGK is here; and, line by line, that every line
on which a package module differs from its source is the D-name substitution applied to the source
line, and that no line still holds the word `RunRegistry`. A line no rule maps, and any line added
or deleted, fails the check. Files ported by a later prompt are reported as pending while absent.
It exits 0 only when all of that holds; the rules are stated in its docstring.

The check holds through prompt 02, while the package is the import. It is retired at prompt 03's
start, when the package begins to change in its own right; from then it describes 02's tree and is
re-run from a worktree of 02's commit (README §4).

## The freeze

SGK froze its `RunRegistry/` at the import commit, by its own `CLAUDE.md`, until it adopts this
package (gate G2 of `prompts/extraction/README.md` §7). A fix wanted in SGK's registry is made here,
and reaches SGK when it adopts a release. The import edited no client: SGK was read only through
`git`.
