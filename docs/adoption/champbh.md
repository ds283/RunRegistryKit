# Adoption checklist: ChamPBH (CPBH)

- **Client:** ChamPBH, `/Users/ds283/Documents/Code/ChamPBH`, at **`c21cdfb`**
  (`c21cdfb5613a3ed976a91a95431495dc8bfd49c8`, branch `main`, 2026-10-15, "Commit audit document for
  Jordan-frame normalization").
- **Tree:** **22 uncommitted changes** in its working tree (`git status --porcelain`, 22 lines),
  **not read**; this checklist describes the commit `c21cdfb`. No stash, one worktree.
- **Package:** `runregistrykit` at **`v0.1.0`** (`9f8ebe4`), with `datastorekit` `v0.4.0`.
- **How it was measured:** read-only, by RunRegistryKit's extraction prompt 07 on 2026-10-15, through
  `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  [`measure_client_registry.py`](measure_client_registry.py) (the appendix). Nothing of CPBH was
  imported, run or opened, and no store was read. **CPBH's adoption campaign measures again before
  acting, and its numbers govern.**
- **This is data, not instructions.** It describes CPBH at `c21cdfb`. CPBH's campaign decides what to
  do, under CPBH's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is CPBH's is
  named as CPBH's.

Unless another commit is named, a `path:line` is CPBH's at `c21cdfb`, and one under
`runregistrykit/` is the package's at `v0.1.0` (`9f8ebe4`).

**In one paragraph.** CPBH has no run registry (`CLAUDE.md:117`) and calls nothing of one: 0
imports, 0 `begin()` calls. So adopting is adding: a pin, a `runregistrykit.toml`, a `.gitignore`
line, and the `begin()` calls CPBH chooses to make. One helper is already shaped for it:
`utilities.installed_package_provenance` is the package's `package_provenance` but for one redundant
statement and a default argument, so it can be replaced by the package's function. CPBH is ready
for the store layer: it has `datastorekit` `v0.4.0`, a registry of 27 classes with 17 specs, and a
test of their coverage.

---

## 1. The client and its versions

- **Python 3.13.16** (`venv/pyvenv.cfg`, read as text: `version = 3.13.16`, MacPorts' 3.13
  framework); **`ray==2.53.0`** (`requirements.txt:79`); **`SQLAlchemy==2.0.46`** (`:91`);
  **`datastorekit @ …@v0.4.0`** (`:17`); `raypoolkit @ …@v0.2.0` (`:80`). All inside the package's
  declared range. Python and SQLAlchemy are the tested high end's; Ray 2.53.0 lies between the two
  tested ends, above Python 3.13's effective floor of 2.45.0, and is not itself tested
  ([`README.md`](README.md) §1).
- **The pin it adds**, in a commit of its own. With the store layer:
  ```text
  runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0
  ```
  CPBH's `datastorekit` line at `:17` satisfies the extra's floor. For the core only,
  `runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.1.0`. Which is CPBH's choice
  (item 6). An editable install is never for CPBH's production runs.

## 2. What it deletes

**Nothing**, unless it substitutes the provenance helper (item 4). Then
`utilities.installed_package_provenance` (`utilities.py:177-229`) goes, and with it, if nothing
else uses it, `RECORDED_DISTRIBUTIONS` (`:174`; item 4 says what reads it).
`format_package_provenance` (`:232`) stays CPBH's.

## 3. What it adds

**`runregistrykit.toml` at CPBH's root.** The values are CPBH's choice; the defaults, with the
distributions its drivers record today and a fingerprinter, would be:

```toml
distributions = ["datastorekit", "raypoolkit"]

[stores]
fingerprinter = "config.fingerprint:fingerprinter"
```

- An empty file takes `runs_root = "var/runs"` and `stores_root = "var/datastores"`.
- `distributions` gives every manifest `packages` = `runregistrykit`, `datastorekit`, `raypoolkit`
  (U9). The names are CPBH's choice: the same two its drivers print today (`utilities.py:174`), or
  others.
- `[stores]` is needed only for the store layer (item 6). The module path and the attribute's name
  are CPBH's choice; `config.fingerprint:fingerprinter` is a placeholder in CPBH's existing `config`
  package (`config/__init__.py`).

**`.gitignore`: `var/`.** CPBH's does not ignore it (`.gitignore:1-5`; the script, item 8). The
runs root must not be committed, and a run's records survive the session that started it only if
they are on disk under the root.

**For the store layer, a fingerprinter module**, `config/fingerprint.py` say, holding a format
number of CPBH's own choosing, the first of a history, and
`DatastoreKitFingerprinter(factories, FINGERPRINT_FORMAT)` from `runregistrykit.fingerprint`, over
`config.datastore.factories` (`config/datastore.py:101`, 27 names mapped to factory **instances**,
`"version": sqla_version_factory(),` at `:102`). `DatastoreKitFingerprinter` takes any mapping
`read_inventory` accepts. The protocol is `runregistrykit.fingerprint.Fingerprinter`
(`runregistrykit/fingerprint.py:27-39`); the config names an instance, not the class.

**In its `CLAUDE.md`, the rules** ([`README.md`](README.md) §3): a short binding section naming
`python -m runregistrykit list`. Today `CLAUDE.md:115-117` says production runs are the user's, on
another machine, and that "There is no run registry in this repository" (item 10).

## 4. Which imports and names it rewrites

**No import of a `RunRegistry` module, no name and no call** (appendix). One string literal names
it: the helper's docstring, `utilities.py:178-197`, which says the helper has the fields of SGK's
`RunRegistry.package_provenance()` "which ChamPBH may one day import in place of this helper"
(`:190-192`).

**The substitution of `installed_package_provenance`.** By `ast`, with docstrings removed, the
helper's body is `runregistrykit.package_provenance`'s but for one statement the package has and the
helper lacks, `origin = None` before the `try` (`runregistrykit/__init__.py:184`), which the
`except` makes redundant: both return the same mapping for every input. The signatures differ: the
helper's is `(names=RECORDED_DISTRIBUTIONS)` (`utilities.py:177`, with `RECORDED_DISTRIBUTIONS =
("datastorekit", "raypoolkit")` at `:174`), the package's `(names)`, with no default. So **each
caller passes the names itself**:

| File:line | Today | After |
|---|---|---|
| `main.py:77-82` | `from utilities import (…, format_package_provenance, installed_package_provenance)` (`:81`) | `from runregistrykit import package_provenance`; `format_package_provenance` stays from `utilities` |
| `main.py:95` | `print(format_package_provenance(installed_package_provenance()), flush=True)` | `print(format_package_provenance(package_provenance(NAMES)), flush=True)` |
| `plot_ScalarModel.py:79` | `from utilities import format_package_provenance, installed_package_provenance` | as `main.py` |
| `plot_ScalarModel.py:89` | as `main.py:95` | as `main.py:95` |
| `plot_by_beta.py:78` | as `plot_ScalarModel.py:79` | as `main.py` |
| `plot_by_beta.py:108` | as `main.py:95` | as `main.py:95` |

**`NAMES` is CPBH's choice**:
- `utilities.RECORDED_DISTRIBUTIONS`, kept as CPBH's constant: the line printed is unchanged;
- the config's `distributions`, `runregistrykit.find_client_root().distributions` (a tuple): one
  list of names for the printed line and the manifest, at the cost of reading the config at import
  of each driver;
- or `("runregistrykit", …)`, to print the registry's release too.

`package_provenance` records a name that is not installed as `None` (`runregistrykit/__init__.py:157-204`,
and checked on a name that is not installed: `{'no-such-distribution-xyz': None}`), as the helper
does (`utilities.py:202-204`). `format_package_provenance`, which reads the same five fields, needs no
change. `package_provenance` is in the core: it needs no extra.

## 5. Its runs

**No program calls `begin()` today.** Which do is CPBH's choice:
- `main.py`, the pipeline driver: the long runs, which `CLAUDE.md:115-116` says are the user's,
  made on another machine. That is where a run's record helps most: the registry records on the
  machine that runs, under that checkout's root.
- `plot_ScalarModel.py` and `plot_by_beta.py`, which read a store read-only (`CLAUDE.md:118`) and
  print their provenance as `main.py` does.

**Advice:** the drivers of long runs first, `main.py`; a plot script only if its runs are long.

**What a `begin()` call needs at `v0.1.0`**: `begin(campaign, prompt, slug, purpose, …)`, with
`script=__file__` so that the script's hash is recorded and the walk for `runregistrykit.toml` starts
from the script's directory, CPBH's root for these three (`runregistrykit/__init__.py:604`; the
package's [`README.md`](../../README.md#a-run), "A run"). `results=` names the store a run writes,
which the store layer can fingerprint at `finish(..., fingerprint=True)` (item 6); `client_root=` is
for a program not run from under the root. Then `heartbeat`, `record`/`known` for a run with a unit
ledger, and `finish(state, exit_code)`. `python -m runregistrykit list` lists the runs.

## 6. Its stores

**CPBH meets the store layer's prerequisites at `c21cdfb`**, but for the config:
- the extra: item 1's pin, with `[stores]`;
- `datastorekit` at `v0.4.0` or later: `requirements.txt:17`;
- a registry with specs: `factories` (`config/datastore.py:101`, 27 names), 17 `def
  inventory_spec` in 17 files (appendix, item 8), and `ObjectFactories/tests/test_inventory_specs.py`,
  which checks coverage: every registered class declares a spec, is read through an owner's spec, or
  is excluded by name with a reason (its docstring, `:25-29`);
- a fingerprinter named in `runregistrykit.toml`: item 3, not there yet.

Whether CPBH adopts the store layer, or the core only, is its choice. Without a fingerprinter named,
every store operation and `store` command refuses (D4); the core (`begin`, `Run`, `list`) does not
need one. CPBH has no sidecars and no recorded fingerprints, so nothing it holds meets U7's
`encoding` entry.

## 7. Its tests

**`ObjectFactories/tests/test_package_provenance.py`** tests the helper and the drivers' use of it.
With the substitution:
- `TestInstalledPackageProvenance` (`:91-277`), nine tests of the helper's results, through real
  stand-in `dist-info` directories (`:21-27`), import it at `:46`. The choice is CPBH's: keep the
  tests against `runregistrykit.package_provenance` (each passes the names, since there is no
  default), or drop them as the package's (the package tests its own function,
  `runregistrykit/tests/test_run_registry.py`, `TestPackageProvenance`).
- `test_default_names` (`:270-277`) pins `utilities.RECORDED_DISTRIBUTIONS` and the helper's
  default; the package's function has no default, so it goes, or pins whatever CPBH chooses as
  `NAMES` (item 4).
- **`TestDriversPrintProvenance`** (`:316-`) reads each driver of `DRIVERS` (`:49`: `main.py`,
  `plot_by_beta.py`, `plot_ScalarModel.py`) with `ast`, and requires one call of
  `installed_package_provenance` with **no arguments** inside the printed line
  (`_is_provenance_print`, `:280-300`, at `:298-299`; `:325-327`), and the two names imported from
  `utilities` (its docstring, `:318-320`). Each of these changes in the same commit as the drivers.

No other CPBH test names the helper (appendix, item 6).

## 8. The Q5 guard

**Offered** (U22): a test that a spec change without a format bump fails, beside the format number,
by [`README.md`](README.md) §6's recipe. **Advice:** build it with the fingerprinter (item 3), in
the same campaign, so that the first format number is pinned from the start.

**CPBH's registry has polymorphic `Parent.types` with `int` keys**, three, in
`ObjectFactories/ScalarModel.py`'s spec (`:230-256`):
- `:234-238`, `"cosmology": Parent("cosmology_serial", type_column="cosmology_type",
  types={XAV_IMPROVED_EOS_IDENTIFIER: "QCD_Cosmology"})`, with `XAV_IMPROVED_EOS_IDENTIFIER = 3`
  (`CosmologyModels/model_ids.py:19`);
- `:239-249`, `potential_type`, five types keyed by `INVERSE_POWER_POTENTIAL = 0` …
  `RECLINER_POTENTIAL = 4` (`CosmologyConcepts/Potentials/model_ids.py:16-20`);
- `:250-254`, `coupling_type`, keyed by `EXPONENTIAL_COUPLING = 0`
  (`CosmologyConcepts/ConformalCouplings/model_ids.py:16`).

`canonical_json` refuses those keys as they are; the recipe's key conversion keeps `0` and `"0"`
apart, so that a change of a key's type fails the guard.

## 9. Its acceptance

G3 holds when CPBH has adopted a release in a campaign of its own, and:
1. `requirements.txt` holds the pin of item 1, and CPBH's venv is installed from it, not editable.
2. `runregistrykit.toml` is at its root, and `.gitignore` ignores `var/` (or its `runs_root`).
3. **One `begin` … `finish` run is listed** by `python -m runregistrykit list`, with its manifest's
   `packages` naming `runregistrykit` and the config's `distributions`.
4. If it substitutes the helper: `measure_client_registry.py cpbh --commit <its commit>` reports no
   definition of `installed_package_provenance`, and its tests pass (item 7).
5. If it adopts the store layer: the config names a fingerprinter that loads, and `python -m
   runregistrykit store fingerprint` reads one of its closed stores.
6. The gate is recorded on this repository's extraction board, §2, row G3.

## 10. What goes stale in it

- **`CLAUDE.md:115-117`**: "There is no run registry in this repository" (`:117`), in the paragraph
  on long-running jobs. It becomes the rules' section (item 3).
- **`.documents/architecture-summary.md:299`**: DatastoreKit's fingerprint module "is there for the
  RunRegistry component, which needs this release" (`:297-299`). Dated architecture prose.
- **`utilities.py:190-192`**, the helper's docstring, if the helper stays (item 4).
- **Campaign records**: `prompts/`, 19 lines. History: not rewritten.

---

## Appendix: the script's output

`./venv/bin/python docs/adoption/measure_client_registry.py cpbh`, from this repository's root at
extraction prompt 07's commit, with `runregistrykit` 0.1.0 and `datastorekit` 0.4.0; as printed.

### Measured: ChamPBH (CPBH) at `c21cdfb`

- Repository `/Users/ds283/Documents/Code/ChamPBH`, commit `c21cdfb5613a3ed976a91a95431495dc8bfd49c8`, 2026-10-15, “Commit audit document for Jordan-frame normalization”.
- Read through `git` only: 219 tracked `.py` files parsed with `ast`.
- Against `runregistrykit` 0.1.0 and `datastorekit` 0.4.0 as installed; signatures before the move from SecondaryGWKit a45aefc.
- `requirements.txt`: `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0` (`:17`); `ray==2.53.0` (`:79`); `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0` (`:80`); `SQLAlchemy==2.0.46` (`:91`).

| Figure | Live code |
|---|---|
| Import statements | 0 |
| … at module level | 0 |
| Files importing it | 0 |
| Names used | 0 |
| Calls bound | 0 |
| … binding | 0 |
| … not binding: the move's new `fingerprint_format` only | 0 |
| … not binding for any other reason | 0 |
| Name-alike calls, not the registry's | 7 |
| String literals naming it | 1 |
| … holding `-m RunRegistry` | 0 |

Campaign records: **0** `.py` files import it, 0 name it.

#### 1. Imports: live code

None.

#### 2–3. Names and their fates at `v0.1.0`: live code

None.

#### 4. Calls: live code

None.

Not the registry's (their callee does not resolve to it), so not bound:

- `ObjectFactories/tests/test_first_bounce_round_trip.py:161` `store._engine.begin(…)`, in `TestFirstBounceRoundTrip._raw_columns`
- `ObjectFactories/tests/test_fixed_T_values_round_trip.py:90` `store._engine.begin(…)`, in `TestFixedTValuesRoundTrip._raw_columns`
- `ObjectFactories/tests/test_scalarmodel_failure_reason.py:90` `store._engine.begin(…)`, in `_write`
- `ObjectFactories/tests/test_version_keyed_lookups.py:112` `store._engine.begin(…)`, in `_insert`
- `ObjectFactories/tests/test_version_keyed_lookups.py:400` `store._engine.begin(…)`, in `TestVersionKeyedLookups.test_d_keyed_build_without_the_serial_raises`
- `ObjectFactories/tests/test_version_keyed_lookups.py:443` `store_b._engine.begin(…)`, in `TestVersionKeyedLookups.test_e_parameter_tables_are_not_keyed`
- `tools/tests/test_inventory_report.py:100` `store._engine.begin(…)`, in `_InventoryStoreCase.insert`

#### 5. String literals naming `RunRegistry`: live code

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `utilities.py` | 178 |  | What is installed of each named distribution, read from its metadata. Maps each name to `None` when  |

#### 1. Campaign records

None.

#### 6. `installed_package_provenance`

- Defined at `utilities.py:177-229`, arguments `(names=RECORDED_DISTRIBUTIONS)`; the package's `package_provenance(names)`.
- Its body against the package's, docstrings removed (`-` the package's only, `+` the client's only):

  ```
  -    origin = None
  ```
- `RECORDED_DISTRIBUTIONS = ('datastorekit', 'raypoolkit')` at `utilities.py:174`.
- Imported at `ObjectFactories/tests/test_package_provenance.py:46` (from `utilities`), `main.py:77` (from `utilities`), `plot_ScalarModel.py:79` (from `utilities`), `plot_by_beta.py:78` (from `utilities`).
- Called at `ObjectFactories/tests/test_package_provenance.py:95` (1 positional), `ObjectFactories/tests/test_package_provenance.py:117` (1 positional), `ObjectFactories/tests/test_package_provenance.py:141` (1 positional), `ObjectFactories/tests/test_package_provenance.py:160` (1 positional), `ObjectFactories/tests/test_package_provenance.py:171` (1 positional), `ObjectFactories/tests/test_package_provenance.py:200` (1 positional), `ObjectFactories/tests/test_package_provenance.py:220` (1 positional), `ObjectFactories/tests/test_package_provenance.py:232` (1 positional), `ObjectFactories/tests/test_package_provenance.py:262` (1 positional), `ObjectFactories/tests/test_package_provenance.py:276` (0 positional), `main.py:95` (0 positional), `plot_ScalarModel.py:89` (0 positional), `plot_by_beta.py:108` (0 positional).

#### 7. Tracked files other than `.py` matching `RunRegistry|run registry|runregistrykit`

Lines by top directory: `.documents` 1, `CLAUDE.md` 1, `prompts` 19.

Outside the campaign records (text squeezed, first 110 characters):

| File | Line | Text |
|---|---|---|
| `.documents/architecture-summary.md` | 299 | it is there for the RunRegistry component, which needs this release. |
| `CLAUDE.md` | 117 | longer than a few PRyMordial solves. There is no run registry in this repository. |

#### 8. `.gitignore` and the registry

- `.gitignore` does not ignore `var/`.
- Module-level registry mappings: `factories` at `config/datastore.py:101` (27 keys).
- `def inventory_spec`: 17 in 17 files: `ObjectFactories/AdiabaticHistory.py:125`, `ObjectFactories/BBNData.py:120`, `ObjectFactories/DimensionfulQuantity.py:43`, `ObjectFactories/DimensionlessQuantity.py:41`, `ObjectFactories/ExponentialCoupling.py:45`, `ObjectFactories/ExponentialPotential.py:53`, `ObjectFactories/InversePowerPotential.py:53`, `ObjectFactories/QCD_Cosmology.py:43`, `ObjectFactories/ReclinerPotential.py:52`, `ObjectFactories/ReflectingPotential.py:52`, `ObjectFactories/ScalarModel.py:222`, `ObjectFactories/Starobinsky.py:52`, `ObjectFactories/integration_metadata.py:38`, `ObjectFactories/redshift.py:44`, `ObjectFactories/store_tag.py:35`, `ObjectFactories/tolerance.py:37`, `ObjectFactories/version.py:35`.
- `Parent(..., types=...)`: `ObjectFactories/ScalarModel.py:234` (`{XAV_IMPROVED_EOS_IDENTIFIER: 'QCD_Cosmology'}`), `ObjectFactories/ScalarModel.py:239` (`{INVERSE_POWER_POTENTIAL: 'InversePowerPotential', EXPONENTIAL_POTENTIAL: 'Expon`), `ObjectFactories/ScalarModel.py:250` (`{EXPONENTIAL_COUPLING: 'ExponentialCoupling'}`).
