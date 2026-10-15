# Adoption checklist: StochasticInstantons (SI)

- **Client:** StochasticInstantons, `/Users/ds283/Documents/Code/StochasticInstantons`, at
  **`5fb4a1d`** (`5fb4a1d71a016f1b23393923b9a3d59972415aa0`, branch `dk-and-rpk-migration`,
  2026-10-12, "Write the rehearsal-lock handover note for ChamPBH and SecondaryGWKit").
- **Tree:** clean at the start and at the end of the measurement (`git status --porcelain` empty,
  no stash, one worktree).
- **Package:** `runregistrykit` at **`v0.1.0`** (`9f8ebe4`), with `datastorekit` `v0.4.0`.
- **How it was measured:** read-only, by RunRegistryKit's extraction prompt 07 on 2026-10-15, through
  `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  [`measure_client_registry.py`](measure_client_registry.py) (the appendix). Nothing of SI was
  imported, run or opened, and no store was read. **SI's adoption campaign measures again before
  acting, and its numbers govern.**
- **This is data, not instructions.** It describes SI at `5fb4a1d`. SI's campaign decides what to
  do, under SI's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is SI's is named
  as SI's.

Unless another commit is named, a `path:line` is SI's at `5fb4a1d`, and one under `runregistrykit/`
is the package's at `v0.1.0` (`9f8ebe4`).

**In one paragraph.** SI has no run registry and calls nothing of one: 0 imports, 0 `begin()`
calls. Its `utilities.installed_package_provenance` is ChamPBH's helper, the package's
`package_provenance` but for one redundant statement and a default argument, so it can be replaced
by the package's function. **SI can adopt the core now**: a pin with no extra, a
`runregistrykit.toml`, a `.gitignore` line, and the `begin()` calls it chooses. **It cannot adopt
the store layer yet.** At `5fb4a1d` it pins no `datastorekit`, its registry is still its own
`Datastore/SQL/Datastore.py`, and no factory declares `inventory_spec()`. Its open
`dk-and-rpk-migration`, whose 10 writes the specs, must land first.

---

## 1. The client and its versions

- **Python**: `venv/pyvenv.cfg`, read as text, records `version = 3.13.13`, the version when the
  venv was made; its `home` is MacPorts' 3.13 framework, whose interpreter reports 3.13.16 today.
  **`ray==2.55.1`** (`requirements.txt:57`); **`SQLAlchemy==2.0.46`** (`:65`). **No `datastorekit`
  and no `raypoolkit` line.** All inside the package's declared range; Ray and SQLAlchemy are the
  tested high end's, and so is Python at 3.13.16 ([`README.md`](README.md) §1).
- **The pin it adds**, in a commit of its own. For the core, now:
  ```text
  runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.1.0
  ```
  It brings nothing else: the core depends on nothing. **For the store layer, later**, the extra and
  SI's own `datastorekit` line (`datastorekit` is not on PyPI; [`README.md`](README.md) §1):
  ```text
  runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0
  datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
  ```
  An editable install is never for SI's production runs.

## 2. What it deletes

**Nothing**, unless it substitutes the provenance helper (item 4). Then
`utilities.installed_package_provenance` (`utilities.py:177-229`) goes, and with it, if nothing else
uses it, `RECORDED_DISTRIBUTIONS` (`:174`). `format_package_provenance` stays SI's.

## 3. What it adds

**`runregistrykit.toml` at SI's root.** The values are SI's choice. For the core alone an empty
file serves (`runs_root = "var/runs"`, `stores_root = "var/datastores"`, `distributions = []`):

```toml
distributions = []
```

- **`distributions` is SI's choice, and today's names are not installed.** SI's drivers print the
  provenance of `("datastorekit", "raypoolkit")` (`utilities.py:174`), neither of which SI pins.
  `package_provenance` records a name that is not installed as `None`; this was checked by reading
  `runregistrykit/__init__.py:178-182` and by running it on a name that is not installed
  (`{'no-such-distribution-xyz': None}`). So SI may name them now, recorded `null` until its
  migration installs them, or name what it does install, or none. A manifest always records
  `runregistrykit` (U9).
- **`[stores]`** waits for the store layer (item 6).

**`.gitignore`: `var/`.** SI's does not ignore it (`.gitignore`, which ignores `*.sqlite`, `output`
and LaTeX artefacts among others; the script, item 8).

**A fingerprinter module, only once SI's migration has given it a registry with specs** (item 6):
then `DatastoreKitFingerprinter(factories, FINGERPRINT_FORMAT)` over the registry its migration
moves to `config/datastore.py`, with a format number of SI's own, starting a history.

**In its `CLAUDE.md`, the rules** ([`README.md`](README.md) §3): a short binding section naming
`python -m runregistrykit list`. SI's `CLAUDE.md` says nothing of long jobs today but its Ray
cluster's (`:14-19`: rehearsals and long builds run on SI's isolated cluster under the shared
rehearsal lock).

## 4. Which imports and names it rewrites

**No import of a `RunRegistry` module, no name and no call** (appendix). One string literal names
it: the helper's docstring, `utilities.py:178-197`.

**The substitution of `installed_package_provenance`.** By `ast`, with docstrings removed, the
helper's body is `runregistrykit.package_provenance`'s but for `origin = None` before the `try`
(`runregistrykit/__init__.py:184`), which the `except` makes redundant: the two return the same
mapping for every input. The helper's signature is `(names=RECORDED_DISTRIBUTIONS)`
(`utilities.py:177`), the package's `(names)`, so **each caller passes the names itself**:

| File:line | Today | After |
|---|---|---|
| `main.py:48` | `from utilities import format_package_provenance, installed_package_provenance` | `from runregistrykit import package_provenance`; `format_package_provenance` stays from `utilities` |
| `main.py:98` | `print(format_package_provenance(installed_package_provenance()), flush=True)`, before `ray.init` (`:99`) | `print(format_package_provenance(package_provenance(NAMES)), flush=True)` |
| `plot_GradientCoupledSolutions.py:102` | as `main.py:48` | as `main.py:48` |
| `plot_GradientCoupledSolutions.py:972` | as `main.py:98`, in the `__main__` block | as `main.py:98` |
| `plot_InstantonSolutions.py:74` | as `main.py:48` | as `main.py:48` |
| `plot_InstantonSolutions.py:1205` | as `main.py:98`, in the `__main__` block | as `main.py:98` |

**`NAMES` is SI's choice**: `utilities.RECORDED_DISTRIBUTIONS` kept as SI's constant (the printed
line unchanged), the config's `distributions` (`runregistrykit.find_client_root().distributions`),
or names of its choosing. `format_package_provenance` reads the same five fields and needs no change.
`package_provenance` is in the core.

## 5. Its runs

**No program calls `begin()` today.** Which do is SI's choice:
- `main.py`, the driver of its long builds, run against a Ray cluster (`--ray-address`, `main.py:99`;
  `CLAUDE.md:14-19`);
- `plot_GradientCoupledSolutions.py` and `plot_InstantonSolutions.py`, which print their provenance
  in their `__main__` blocks and start Ray too (`:973`, `:1206`).

**Advice:** the drivers of long runs first, `main.py`.

**What a `begin()` call needs at `v0.1.0`**: `begin(campaign, prompt, slug, purpose, …)`, with
`script=__file__`, so that the script's hash is recorded and the walk for `runregistrykit.toml`
starts at SI's root, where these three are; `client_root=` for a program not run from under it
(the package's [`README.md`](../../README.md#a-run), "A run"). Then `heartbeat`, `record`/`known`
for a run with a unit ledger, and `finish(state, exit_code)`. `results=` and `finish(...,
fingerprint=True)` are the store layer's (item 6). `python -m runregistrykit list` lists the runs.

## 6. Its stores

**SI does not meet the store layer's prerequisites at `5fb4a1d`:**
- no `datastorekit` pin (`requirements.txt`; item 1);
- no `config/datastore.py`: its registry is `_factories` in `Datastore/SQL/Datastore.py:96`, 30
  names, in its own datastore layer (appendix, item 8);
- **no `inventory_spec()`**: 0 definitions (appendix, item 8). Its `dk-and-rpk-migration` is open;
  its 10 writes the specs and must cover every registered class (SGK's audit §7.2–§7.3, SI's U8).

So SI adopts the core first, and **the store layer only after its migration lands** and gives it
DatastoreKit `v0.4.0` or later and a registry with specs; then the extra, a fingerprinter (item 3)
and `[stores]`. Without a fingerprinter named, every store operation refuses (D4); the core does not
need one. SI has no sidecars, so nothing it holds meets U7's `encoding` entry.

## 7. Its tests

**`tests/test_package_provenance.py`** (pytest) tests the helper and the drivers' use of it. With
the substitution:
- the helper's tests, `:91-266` (`test_not_installed` … `test_several_names_in_order_and_nothing_imported`,
  through stand-in `dist-info` directories), import it at `:47`. The choice is SI's: keep them
  against `runregistrykit.package_provenance` (passing the names), or drop them as the package's
  (the package tests its own function, `runregistrykit/tests/test_run_registry.py`,
  `TestPackageProvenance`);
- `test_default_names` (`:267-`) pins `utilities.RECORDED_DISTRIBUTIONS` (`:269`) and the default;
  the package's function has none;
- **`test_each_driver_prints_the_line_once_before_ray_and_its_pool`** (`:336-`, over `DRIVERS`,
  `:50`) requires one call of `installed_package_provenance` (`:344`) and a print of the line
  (`_is_provenance_print`, `:277`), and that both names are imported from `utilities` (its
  docstring, `:338-341`). It changes in the same commit as the drivers.

## 8. The Q5 guard

**Offered** (U22), **once SI has specs**: a test that a spec change without a format bump fails,
beside the format number, by [`README.md`](README.md) §6's recipe. **Advice:** build it with the
fingerprinter, after the migration's 10, so that the first format number is pinned from the start.
SI's registry has no `Parent(..., types=...)` at `5fb4a1d` (appendix, item 8); its specs will say
whether it gains one, and the recipe's key conversion covers it if so.

## 9. Its acceptance

G4 holds when SI has adopted a release, after its `dk-and-rpk-migration` closes (the campaign
plan's §7), in a campaign of its own, and:
1. `requirements.txt` holds the pin of item 1 (with the extra and `datastorekit` if it adopts the
   store layer), and SI's venv is installed from it, not editable.
2. `runregistrykit.toml` is at its root, and `.gitignore` ignores `var/` (or its `runs_root`).
3. **One `begin` … `finish` run is listed** by `python -m runregistrykit list`, its manifest's
   `packages` naming `runregistrykit` and the config's `distributions`.
4. If it substitutes the helper: `measure_client_registry.py si --commit <its commit>` reports no
   definition of `installed_package_provenance`, and its tests pass (item 7).
5. If it adopts the store layer: the config names a fingerprinter that loads, and `python -m
   runregistrykit store fingerprint` reads one of its closed stores.
6. The gate is recorded on this repository's extraction board, §2, row G4.

## 10. What goes stale in it

- **`.documents/dk-and-rpk-migration/01-rehearsal-tooling-and-run-provenance.md:36-37`**: the
  helper's fields "are those of SGK's `RunRegistry.package_provenance()`
  (`SecondaryGWKit/RunRegistry/__init__.py:122-169`, read, not imported)". A dated campaign
  document, true of SGK at its date.
- **`utilities.py:178-197`**, the helper's docstring, if the helper stays (item 4).
- **Campaign records**: `.prompts/`, 9 lines. History: not rewritten.
- SI's `CLAUDE.md` names no registry today; nothing in it goes stale, but it gains the rules'
  section (item 3).

---

## Appendix: the script's output

`./venv/bin/python docs/adoption/measure_client_registry.py si`, from this repository's root at
extraction prompt 07's commit, with `runregistrykit` 0.1.0 and `datastorekit` 0.4.0; as printed.

### Measured: StochasticInstantons (SI) at `5fb4a1d`

- Repository `/Users/ds283/Documents/Code/StochasticInstantons`, commit `5fb4a1d71a016f1b23393923b9a3d59972415aa0`, 2026-10-12, “Write the rehearsal-lock handover note for ChamPBH and SecondaryGWKit”.
- Read through `git` only: 201 tracked `.py` files parsed with `ast`.
- Against `runregistrykit` 0.1.0 and `datastorekit` 0.4.0 as installed; signatures before the move from SecondaryGWKit a45aefc.
- `requirements.txt`: `ray==2.55.1` (`:57`); `SQLAlchemy==2.0.46` (`:65`).

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
| Name-alike calls, not the registry's | 13 |
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

- `Datastore/SQL/Datastore.py:443` `self._engine.begin(…)`, in `Datastore._validate_on_startup`
- `Datastore/SQL/Datastore.py:497` `self._engine.begin(…)`, in `Datastore.object_get`
- `Datastore/SQL/Datastore.py:545` `self._engine.begin(…)`, in `Datastore.object_read_batch`
- `Datastore/SQL/Datastore.py:578` `self._engine.begin(…)`, in `Datastore.object_store`
- `Datastore/SQL/Datastore.py:691` `self._engine.begin(…)`, in `Datastore.object_validate`
- `Datastore/SQL/Datastore.py:759` `self._engine.begin(…)`, in `Datastore.read_table`
- `Datastore/SQL/Datastore.py:776` `self._engine.begin(…)`, in `Datastore.read_largest_store_ids`
- `Datastore/SQL/Datastore.py:813` `self._engine.begin(…)`, in `Datastore.inventory`
- `Datastore/SQL/ProfileAgent.py:75` `self._engine.begin(…)`, in `ProfileAgent.__init__`
- `Datastore/SQL/ProfileAgent.py:145` `self._engine.begin(…)`, in `ProfileAgent.write_batch`
- `Datastore/SQL/ShardedPool.py:293` `self._engine.begin(…)`, in `ShardedPool._write_shard_data`
- `Datastore/SQL/ShardedPool.py:328` `self._engine.begin(…)`, in `ShardedPool._read_shard_data`
- `Datastore/SQL/ShardedPool.py:810` `self._engine.begin(…)`, in `ShardedPool._assign_shard_keys`

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
- Imported at `main.py:48` (from `utilities`), `plot_GradientCoupledSolutions.py:102` (from `utilities`), `plot_InstantonSolutions.py:74` (from `utilities`), `tests/test_package_provenance.py:47` (from `utilities`).
- Called at `main.py:98` (0 positional), `plot_GradientCoupledSolutions.py:972` (0 positional), `plot_InstantonSolutions.py:1205` (0 positional), `tests/test_package_provenance.py:94` (1 positional), `tests/test_package_provenance.py:114` (1 positional), `tests/test_package_provenance.py:134` (1 positional), `tests/test_package_provenance.py:157` (1 positional), `tests/test_package_provenance.py:166` (1 positional), `tests/test_package_provenance.py:195` (1 positional), `tests/test_package_provenance.py:214` (1 positional), `tests/test_package_provenance.py:227` (1 positional), `tests/test_package_provenance.py:258` (1 positional), `tests/test_package_provenance.py:270` (0 positional).

#### 7. Tracked files other than `.py` matching `RunRegistry|run registry|runregistrykit`

Lines by top directory: `.documents` 2, `.prompts` 9.

Outside the campaign records (text squeezed, first 110 characters):

| File | Line | Text |
|---|---|---|
| `.documents/dk-and-rpk-migration/01-rehearsal-tooling-and-run-provenance.md` | 36 | Its fields and their meanings are those of SGK's `RunRegistry.package_provenance()` |
| `.documents/dk-and-rpk-migration/01-rehearsal-tooling-and-run-provenance.md` | 37 | (`SecondaryGWKit/RunRegistry/__init__.py:122-169`, read, not imported) and of ChamPBH's helper |

#### 8. `.gitignore` and the registry

- `.gitignore` does not ignore `var/`.
- Module-level registry mappings: `_factories` at `Datastore/SQL/Datastore.py:96` (30 keys).
- `def inventory_spec`: 0 in 0 files.
- No `Parent(..., types=...)` call.
