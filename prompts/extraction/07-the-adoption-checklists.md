# Prompt 07 — the adoption checklists

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 06 landed (`9f8ebe4`), its review is recorded (`4ee947b`), and **`v0.1.0`** is tagged on
  `9f8ebe4` (tag object `fd5ce48`) after CI run `38754093289` passed there; the release is recorded
  (`dca5ead`), whose CI run `38768740409` also passed.
- U20, U21 and U22 are taken (README §6.2, 2026-10-15, as recommended).
- `git diff --stat dca5ead HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md
  README.md .github` is empty, and no `docs/adoption/` exists.
- The suite is `Ran 276 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]` (U20).
**Narrows:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code is one measuring script and one README paragraph. The weight is in four documents that
  three other repositories' campaigns will act on, each fact of which must be true of a client at a
  named commit and of the package at `v0.1.0`, cited by `path:line`, and measured, not inferred.
- Two facts below change what SGK must do and were found only by reading its tests (§0.3: the
  helpers its staying tests import, which `v0.1.0` does not ship; `fingerprint_of`'s new required
  argument). The agent has to look for more of the same.

**Read first:**

1. [`README.md`](README.md): §0.1, §0.2 (the clients, the couplings, the tests), §1, §2 (rows
   06–08), §3, §4, §5 (rules 5, 6, 7 and 9) and §6.2 (U5–U9, U11, U13, U16, U19, U20, U21, U22), and
   §7 (E2, G2–G4).
2. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`, above all "What this repository is" and
   "Releases".
3. The board: §1's review of 06 and *The release*; §3's open issues; §4 (every resolved issue whose
   fix a client meets on adoption: C1–C9's, U7's, U14's).
4. The package as tagged: `README.md` (every section), `PROVENANCE.md` (the module map, "Since the
   import"), the module docstrings of `runregistrykit/__init__.py`, `client.py`, `fingerprint.py` and
   `stores.py`, every module's `__all__`, and `python -m runregistrykit --help`, `list --help` and
   `store <command> --help`.
5. **SGK's side of E2**, read only through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   14bcac0:<path>`: `prompts/runregistry-extraction/runregistrykit-extraction-brief.md` §8 (what SGK
   asked for), `prompts/runregistry-extraction/README.md` §2.2 (the charters of its 05–08, which
   apply the checklist) and `docs/runregistry-extraction-audit.md` §2.1, §3.5 and §7.
6. **The precedent**, RayPoolKit's checklists, read only through `git -C
   /Users/ds283/Documents/Code/RayPoolKit show HEAD:<path>`: `prompts/extraction/06-the-adoption-checklists.md`
   and `docs/adoption/README.md` and `secondarygwkit.md`, for the form. Do not copy their content;
   their client facts are about the pool.

Facts below are at this repository's `dca5ead` and at the client commits named in §0, measured
read-only on 2026-10-15.

---

## 0. The clients, as measured

Each client was read through `git ls-tree` and `git show` at its commit, never from its working
tree, by a planner's script that parsed each tracked `.py` file with `ast`. None was imported, run
or edited, and no store or run directory of any was opened.

| Client | Repository | Commit (branch) | Tree | Python (`venv/pyvenv.cfg`) | `requirements.txt` |
|---|---|---|---|---|---|
| SGK | `SecondaryGWKit/` | `14bcac0` (`handover-remedial`) | clean | 3.12.15 | `datastorekit … @v0.4.0` (`:17`), `ray==2.43.0` (`:75`), `raypoolkit … @v0.2.0` (`:76`), `SQLAlchemy==2.0.39` (`:87`) |
| CPBH | `ChamPBH/` | `c21cdfb` (`main`) | **22 uncommitted changes**, not read | 3.13.16 | `datastorekit … @v0.4.0` (`:17`), `ray==2.53.0` (`:79`), `raypoolkit … @v0.2.0` (`:80`), `SQLAlchemy==2.0.46` (`:91`) |
| SI | `StochasticInstantons/` | `5fb4a1d` (`dk-and-rpk-migration`) | clean | `version = 3.13.13` (the version at creation; its interpreter is MacPorts' 3.13) | **no `datastorekit` or `raypoolkit`**; `ray==2.55.1` (`:57`), `SQLAlchemy==2.0.46` (`:65`) |

These are the commits 05a measured the guard's vocabulary at, and each is its client's `HEAD`.
SGK's `RunRegistry/` and `StoreFixtures/` are unchanged from `a45aefc` (README §0.2, G1). Each
client has one worktree. Only SGK's `.gitignore` ignores `var/` (`:3`).

### 0.1 SGK's live callers

Outside `RunRegistry/` and `prompts/`, **13 import statements in 10 files**, 4 at module level and
9 inside a function:

| File | Line(s) | Scope | Imports |
|---|---|---|---|
| `ObjectFactories/tests/test_quadsource_policy_key.py` | 411 | a test | `from RunRegistry.stores import fingerprint_of` |
| `docs/a3-v2-readiness/fingerprint_time_probe.py` | 83 | `main` | `FINGERPRINT_FORMAT, fingerprint_store` from `.stores` |
| `docs/a3-v2-readiness/sigterm_handler_probe.py` | 150, 151 | `child` | `RunRegistry`; `RunRegistry.stores as registry_stores` |
| `docs/datastore-integrity-verification/compare_stores.py` | 21 | module | `FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_store` |
| `docs/datastore-integrity-verification/interrupt_when.py` | 61 | module | `RunRegistry` |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py` | 29 | module | as `compare_stores.py` |
| `docs/dk-and-rpk-migration/rehearsal/stage_counts.py` | 26 | module | `RunRegistry` (uses `_slug`, twice) |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 526 | `register` | `RunRegistry` |
| `docs/handover/quadsource_atol_sweep.py` | 554, 760, 862 | `run_build`, `prepare`, `sweep` | `RunRegistry`; `RunRegistry.stores`; `RunRegistry` |
| `docs/runregistry-extraction/fingerprint_both_ways.py` | 110 | `check_store` | `stores as sgk_stores` |

Seven `.py` files under `prompts/` name it: campaign records, counted, not rewritten. There are
**4 `begin(...)` calls** (`sigterm_handler_probe.py:159`, `scoped_pipeline_run.py:541`,
`quadsource_atol_sweep.py:556, 864`), every keyword one `v0.1.0`'s `begin` still takes, with the
same meaning (`root=` is still the runs root; `client_root=` is new and keyword-only). **18 string
literals** name `RunRegistry`: docstrings, a refusal (`scoped_pipeline_run.py:529`), and three
printed commands `PYTHONPATH=. ./venv/bin/python -m RunRegistry list` (`scoped_pipeline_run.py:579`,
`quadsource_atol_sweep.py:594, 905`).

### 0.2 What each name SGK uses is at `v0.1.0`

Each name, checked against `runregistrykit`'s `__all__` and `inspect.signature` at `v0.1.0`, and
against SGK's `RunRegistry/` at `a45aefc` by `ast`:

| SGK's name | At `v0.1.0` |
|---|---|
| `begin`, `liveness`, `pid_alive`, `read_json`, `now_iso`, `run_id`, `list_runs`, `DEFAULT_STALE_AFTER`, `TERMINAL_STATES` | the same public name; `begin` and `list_runs` gain keyword-only `client_root=`, nothing else changes |
| `stores.copy_store`, `move_store`, `create_sidecar`, `read_sidecar`, `sidecar_path`, `fingerprint_store`, `write_listing`, `KNOWN_FIELDS`, `TAKEN_KEYS` | the same public name in `runregistrykit.stores`; each function that needs the root gains keyword-only `client_root=` |
| `_slug` | **renamed** `slugify(text)` (U11) |
| `stores.fingerprint_of`, `compare_fingerprints`, `listing_lines` | **moved** to `datastorekit.store_fingerprint` (layer C, README §0.2). **`fingerprint_of` now requires `fingerprint_format`**: `fingerprint_of(inventory, fingerprint_format, taken=None)`, where SGK's was `fingerprint_of(inventory, taken=None)`. `compare_fingerprints` compares `encoding_format` first, so an SGK-recorded fingerprint against a fresh one gives one `encoding` entry (U7) |
| `stores.FINGERPRINT_FORMAT` | **deleted** (C7); it becomes SGK's, in its `config/fingerprint.py` (SGK's 06) |
| `REPO_ROOT`, `DEFAULT_ROOT`, `stores.DEFAULT_ROOT`, `stores.DEFAULT_STORES_ROOT`, `RECORDED_DISTRIBUTIONS` | **deleted** (C1–C5); the root and its settings come from `runregistrykit.toml` |
| `_repo_path` | still there, **private**, and its signature changed: `_repo_path(path)` at `a45aefc`, `_repo_path(path, root)` at `v0.1.0`, the root now given (C4's meaning kept) |
| `Run._fingerprint_results`, `stores._fingerprint_problems` | still there, **private**, unchanged in signature |

No private name or patch target is promised (README, "The public names").

### 0.3 SGK's staying tests

SGK's 101 tests that stay in SGK (README §0.2's last table row) sit under `RunRegistry/tests/` at
`14bcac0`, in five modules and two classes of a sixth, and SGK's 06 moves them out
(`RunDrivers/tests/` and `ObjectFactories/tests/`, its README §2.2). They import **12 statements in
5 modules** (`test_prune_on_resume.py` none), and among what they use:

- **test helpers `v0.1.0` does not ship** (U19 excluded `runregistrykit.tests` from the wheel):
  `RunRegistry.tests.store_fixtures` (`StoreTestCase`, `load`, `sweep_shaped`,
  `write_sidecar_json`; `test_quadsource_atol_sweep_prepare.py:27`, `test_store_fingerprint.py:41`),
  `RunRegistry.tests.test_store_command_line.CommandLineTestCase` (`test_store_fingerprint.py:47`),
  and each other (`test_killed_handler.py:27` from `test_pipeline_adoption`,
  `test_build_rehearsal_scope.py:39` from `test_prune_on_resume`);
- **deleted names**: `RunRegistry.REPO_ROOT` (`test_store_fingerprint.py:73`),
  `RunRegistry.DEFAULT_ROOT` (`test_pipeline_adoption.py:278`, and patched at `:330`),
  `stores.DEFAULT_ROOT` (patched, `test_quadsource_atol_sweep_prepare.py:73`),
  `FINGERPRINT_FORMAT` and `fingerprint_of(inventory)` without a format (`TestGolden`,
  `test_store_fingerprint.py:347-383`);
- **private names whose signature changed**: `RunRegistry._repo_path(baseline)`
  (`test_quadsource_atol_sweep_prepare.py:134`), now `_repo_path(path, root)`;
- **a private method patched**: `Run._fingerprint_results` (`test_killed_handler.py:333, 432`).

The texts these tests assert that are also in `RunRegistry/` at `a45aefc` are all still in
`runregistrykit` at `v0.1.0` (25 checked), but for one in a part of `test_store_fingerprint.py`
that this package ported (`:451`, not `TestGolden` or `TestDrivers`).

**U21, taken 2026-10-15:** `runregistrykit` ships no test support. SGK's checklist lists every
helper and deleted name its staying tests use, file by file, and advises (**Advice:**) that SGK
keep the helpers it uses as its own code, copied from its frozen `a45aefc` beside the moved tests
and adapted to a client root built in a `tempfile` directory, as this package's
`runregistrykit/tests/client_fixtures.py` does (read, not imported).

### 0.4 ChamPBH and StochasticInstantons

Neither imports or calls the registry: **0 imports, 0 `begin` calls** at their commits. Each has:

- **`utilities.installed_package_provenance`** (`utilities.py:177-229` in both), written in the
  shape of SGK's `package_provenance` so that adoption is a substitution. By `ast`, with docstrings
  removed, its body is `runregistrykit.package_provenance`'s but for one statement the package has
  and the helper lacks (`origin = None` before the `try`, which the `except` makes redundant); the
  helper's signature is `(names=RECORDED_DISTRIBUTIONS)`, the package's `(names)`. Its callers:
  CPBH `main.py:81, 95`, `plot_ScalarModel.py:79, 89`, `plot_by_beta.py:78, 108`; SI `main.py:48,
  98`, `plot_GradientCoupledSolutions.py:102, 972`, `plot_InstantonSolutions.py:74, 1205`, each with
  `format_package_provenance`, which stays the client's. Each has a test of it
  (CPBH `ObjectFactories/tests/test_package_provenance.py`, SI `tests/test_package_provenance.py`).
- **No `var/` in `.gitignore`.**
- **`CLAUDE.md`**: CPBH's says "There is no run registry in this repository" and that production
  runs are the user's, made on another machine (`:115-117`); SI's says nothing of long jobs but its
  Ray cluster's.

**Their store layer.** The store layer needs a fingerprinter over the client's registry:
- **CPBH is ready for it**: `datastorekit` at `v0.4.0`; `config/datastore.py` holds `factories`
  (`:101`); 17 factories declare `inventory_spec()`; and `ObjectFactories/tests/test_inventory_specs.py`
  checks coverage (every registered class has a spec, is read through an owner, or is excluded by
  name).
- **SI is not**: at `5fb4a1d` it has no `datastorekit` pin, no `config/datastore.py`, and no
  `inventory_spec()`; its registry is still its own `Datastore/SQL/Datastore.py`. Its
  `dk-and-rpk-migration` (open; its 10 writes the specs) must land first. SI can adopt the core
  before then.

### 0.5 What goes stale

Tracked files other than `.py` that match `RunRegistry|run registry|runregistrykit`
(case-sensitive, `git grep -I`), by top directory: **SGK** `prompts/` 2078, `docs/` 158,
`CLAUDE.md` 10 (the registry section, `:77-104`; the freeze section, `:106-116`; and the test roots,
`:144`); **CPBH** `prompts/` 19, `CLAUDE.md` 1, `.documents/` 1; **SI** `.prompts/` 9,
`.documents/` 2. Campaign records and dated documents are history: counted, not rewritten.

### 0.6 The Q5 guard (U22)

A client's guard that a spec change without a format bump fails a test (SGK's Q5, its 07; audit
§3.5) needs nothing of this package: `datastorekit.store_inventory.inventory_specs(factories)` in
registry order, each `InventorySpec` (fields `leaves`, `parents`, `tags`, `values`, `validated`,
`parent_sets`) made plain recursively, a polymorphic `Parent.types` given string keys explicitly
(`canonical_json` refuses others), the whole through `canonical_json`, its SHA-256 pinned beside
the format number. The planner's trial of that recipe on this package's neutral store
(`runregistrykit/tests/neutral_store.py`'s `FACTORIES`, format 1, 6 classes) ran on public names
only. **U22, taken 2026-10-15:** the checklists' README describes the recipe with a short sketch,
proved here; each client writes its own test; nothing is shipped.

---

## 1. What is wanted

07 writes **`docs/adoption/`**: one checklist per client, a README holding what the three share,
and the script that measures them; and corrects one paragraph of `README.md` (U20). After it, each
client's adoption campaign, in its own repository, can be planned from its checklist (README §7,
G2–G4), and **E2**, SGK's gate on this campaign, is `v0.1.0` with SGK's checklist.

- **A checklist is data, not instructions.** It describes the client at one commit; the client's
  campaign measures again before acting, and its numbers govern. A choice that is the client's is
  named with what each option touches, and not made; a recommendation is marked **Advice:**.
- **Every fact carries a `path:line`** at the client's commit (named once at the head of the
  checklist), or at `v0.1.0` (`9f8ebe4`) for a line under `runregistrykit/`, or comes from the
  script, whose Markdown output is each checklist's appendix.
- **No behaviour of the package changes.** No file under `runregistrykit/` is touched; the suite
  stays at **276**.
- **No client is edited, imported or run**, and no store or run directory of any is opened (README
  §3, §5 rule 5; `CLAUDE.md`).

---

## 2. What to write

### 2.1 `docs/adoption/measure_client_registry.py`

```bash
./venv/bin/python docs/adoption/measure_client_registry.py sgk  [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_registry.py cpbh [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_registry.py si   [--commit SHA] [--json]
```

- **Reads** the client at `/Users/ds283/Documents/Code/<repository>` through `git ls-tree -r` and
  `git show <commit>:<path>` only, never its working tree; the default commit is §0's. Parses each
  tracked `.py` file with `ast`. For SGK, `RunRegistry/` is read too, at the commit, to measure the
  staying tests (§0.3): the five modules and `TestGolden` and `TestDrivers` of
  `test_store_fingerprint.py`, named in the script, and nothing else under `RunRegistry/`.
- **Reports:**
  1. every import of a `RunRegistry` module, at module level or nested (with the enclosing
     function or class), with file, line and names, split into live code, the staying tests, and
     campaign records (`prompts/`, `.prompts/`, counted by file only);
  2. every name used from it: imported by name, or reached as an attribute of an imported module
     or of an alias, or patched (`mock.patch.object(<module>, "<name>")`, `mock.patch("<dotted
     name>")`, `setattr(<module>, "<name>", …)`), with its sites;
  3. **for each name, its fate at `v0.1.0`, from the package itself**: "kept" when it is in the
     `__all__` of the corresponding `runregistrykit` module (import it); otherwise from a table in
     the script of the renames, moves and deletions of §0.2, **each row checked when the script
     runs** (a rename's and a move's target exists, with `inspect.signature`; a deletion's name is
     absent from the module); a private name (leading `_`) is "private", flagged, and reported
     present or absent at `v0.1.0`, with its signature there against `a45aefc`'s (read by `ast`
     from SGK's `RunRegistry/` at that commit) when it is a function; any other name is reported
     "unknown" and the run exits 3;
  4. every call of `begin`, `fingerprint_store`, `copy_store`, `move_store`, `retire_store`,
     `create_sidecar`, `adopt_sidecar` and `amend_sidecar` reached through the registry, and of
     `fingerprint_of`: file and line, positional count, keywords, `**kwargs`, and **whether
     `inspect.signature(<v0.1.0's function>).bind(...)` accepts it** (placeholders for every
     argument; for `fingerprint_of`, `datastorekit.store_fingerprint.fingerprint_of`). The verdict
     says only that the call binds;
  5. string literals that name `RunRegistry`, with `python -m RunRegistry` commands flagged;
  6. for CPBH and SI, `installed_package_provenance`: its definition, by `ast`, against
     `runregistrykit.package_provenance` (docstrings removed; the difference, if any, as unparsed
     lines), and every call of it;
  7. tracked files other than `.py` matching §0.5's pattern, counted by top directory, with each
     line outside the campaign-record directories listed;
  8. whether `.gitignore` ignores `var/`; and the client's registry, for the fingerprinter: the
     file holding a top-level `factories` mapping, and how many tracked `.py` files define
     `inventory_spec`.
- **Output:** Markdown by default (the checklists' appendices), JSON with `--json`. Sorted, so two
  runs at one commit give the same bytes. Exits 0 on success, 2 when it cannot read the client or
  the commit, 3 on an unknown name.
- **Imports** only the standard library, `runregistrykit` and `datastorekit.store_fingerprint`. It
  names the clients, as `docs/extraction/compare_with_source.py` names SGK; nothing under
  `runregistrykit/` does (`CLAUDE.md`). It is not a test, is not collected by the suite, and does
  not run in CI. `black` clean (CI checks `docs/`).

**Its figures must equal §0's**, or the log says which differs and why: SGK's 13 imports in 10
files (4 module-level), 4 `begin` calls all binding, 18 string literals, 7 campaign-record files;
the staying tests' 12 imports in 5 modules; CPBH's and SI's 0 imports and their helper's one-line
difference; §0.5's counts. A difference in the agent's favour (a site the planner missed) is
recorded and the checklists use the script's figure; a call that does **not** bind, or an unknown
name, is a stop (§5).

### 2.2 `docs/adoption/README.md`

What the three share, in RayPoolKit's form but not its content:
- **Head:** written by extraction prompt 07, against `v0.1.0` (`9f8ebe4`); the clients read through
  `git` only, at the commits named; a checklist is data, not instructions.
- **The table** of the three checklists, each with its client commit and its gate (README §7: G2,
  G3, G4; and E2 for SGK's).
- **§1 The release and the pin**: the two `requirements.txt` lines of the package README's
  "Installing", and why both (`datastorekit` is not on PyPI); the core-only form; the
  editable-install warning; the declared range and the three tested configurations; each client's
  Python, Ray, SQLAlchemy and `datastorekit` against them (§0's table); each client keeps its own
  pins.
- **§2 The module map**: `RunRegistry` → `runregistrykit`, `RunRegistry.stores` →
  `runregistrykit.stores`, the fingerprinter in `runregistrykit.fingerprint`, the config in
  `runregistrykit.client`; the names of §0.2's table that are renamed, moved or deleted, with their
  replacements; that the public names are each module's `__all__`, and no private name or patch
  target is promised (README, "The public names").
- **§3 What a client adds**: `runregistrykit.toml` at its root (the keys and defaults, by link to
  the package README's "Using it"); `var/` (or its `runs_root`) in `.gitignore`; for the store
  layer, a fingerprinter in a module of its own, `DatastoreKitFingerprinter(factories,
  fingerprint_format)` over its registry, named by `[stores] fingerprinter`; and in its `CLAUDE.md`,
  the rules (the package README's "The rules") as a short binding section naming `python -m
  runregistrykit list` and pointing at the README (SGK's brief §6).
- **§4 What changes for a caller**: one line each, linked to where the package states it: the root
  from the config and none a refusal (C1–C3); a linked worktree recorded under the main checkout
  while its config and fingerprinter are its own (Q3, U20); `packages` names `runregistrykit` and
  the config's `distributions` (C5, U9); the store layer refuses without a fingerprinter (D4);
  `store retire` loads it first (U14); a fingerprint carries DatastoreKit's `encoding_format`, and a
  recorded one without it compares as one `encoding` entry (U7).
- **§5 What does not change**: what the registry writes (`CLAUDE.md`, "Releases"): an existing run
  directory or sidecar is read as it is (C4's relative paths kept); with the package README's
  section linked.
- **§6 The Q5 guard**: §0.6's recipe, in prose and a sketch of at most about twenty lines; that it
  is the client's test, beside its format number; the deliberate breakages SGK's 07 names (a leaf
  added with no bump; a bump with no new pin; a class added). The sketch is **proved here**: the log
  shows it run, from the scratchpad, on the neutral store's `FACTORIES`, and on a stand-in registry
  with a polymorphic `Parent.types` whose keys are not strings, each breakage failing as stated.
  The sketch is not committed as a module or a test.
- **§7 How a checklist is used**: measured at the named commit and re-measured by the client; a
  client's adoption is one campaign in its own repository; the pin moves in a commit of its own; a
  defect the client finds in the package is reported and fixed here, in a release.
- **§8 Re-measuring**: the script's commands, what it reports, and its figures at the checklists'
  commits.
- The checklist items, by number and name (§2.3).

### 2.3 The three checklists

`docs/adoption/secondarygwkit.md`, `docs/adoption/champbh.md`, `docs/adoption/stochasticinstantons.md`.
Each opens with the client, its repository path, its commit (full SHA, branch, date and subject),
and the state of its tree (CPBH: the 22 uncommitted changes were not read; the checklist describes
`c21cdfb`). Each then has the **same ten items, in the same order and under the same names**:

1. **The client and its versions**: Python, Ray, SQLAlchemy and `datastorekit` against `v0.1.0`'s
   range and tested configurations; the pin lines it adds (with or without the extra).
2. **What it deletes**: SGK: `RunRegistry/` (25 files, their blobs as the board's G1 row); CPBH and
   SI: nothing, or `installed_package_provenance` if it substitutes (item 4).
3. **What it adds**: `runregistrykit.toml`, with the values this client would write (SGK: `var/runs`,
   `var/datastores`, `distributions = ["datastorekit", "raypoolkit"]`, and `[stores] fingerprinter`
   naming SGK's `config/fingerprint.py`, as its brief §8.2 and its 06 charter say; the attribute's
   name is SGK's choice); the `.gitignore` line where missing; the fingerprinter module where the
   store layer is adopted: SGK's `config/fingerprint.py` holding `FINGERPRINT_FORMAT = 6`, the
   history of formats moved verbatim from `RunRegistry/stores.py:194-205` at `a45aefc`, and the
   `DatastoreKitFingerprinter` over `config.datastore.factories`; CPBH's over its
   `config/datastore.py` (`:101`) with a format of its own choosing, starting a history; SI's,
   **only once its migration has given it a registry with specs** (§0.4).
4. **Which imports and names it rewrites**: every import and name of §0.1–§0.3 (SGK) with its
   replacement from §0.2, by `path:line`; for SGK's staying tests, each helper and deleted name with
   U21's **Advice:**; `_slug` → `slugify`; `fingerprint_of`'s format argument at
   `test_quadsource_policy_key.py:411` and in `TestGolden`; the printed commands. For CPBH and SI:
   the substitution of `installed_package_provenance` by `runregistrykit.package_provenance`, with
   the default argument the client passes itself, and what happens to its test (the choice the
   client's: keep the test against the package function, or drop it as the package's).
5. **Its runs**: which of its programs would call `begin()` (SGK: its two drivers and its rehearsal
   tooling, §0.1; CPBH and SI: the drivers that print their provenance, `main.py` and the plot
   scripts, each a choice the client makes, **Advice:** the drivers of long runs first); what each
   `begin` call needs at `v0.1.0` (the script's bind verdicts); `client_root=` for a program not run
   from the root.
6. **Its stores**: the store layer's prerequisites for this client (the extra, `datastorekit`, a
   fingerprinter), and whether it meets them at its commit (§0.4); for SGK, that its recorded
   fingerprints lack `encoding_format` and compare as one `encoding` entry (its own
   `[00-recorded-fingerprints-lack-the-encoding-format]` and its D6), and that its existing sidecars
   and run directories are read as they are.
7. **Its tests**: SGK: the 101 staying tests, where its 06 moves them, and every helper and name of
   §0.3 they need, by `path:line`, with U21's **Advice:**; CPBH and SI: the provenance helper's test.
8. **The Q5 guard**: SGK: its 07, with §0.6's recipe linked to the README's §6, its `Parent.types`
   case named if its registry has one (read its specs at the commit to say); CPBH and SI: offered,
   with **Advice:** to build it with the fingerprinter.
9. **Its acceptance**: what shows the adoption landed: SGK, its 06's acceptance (no `RunRegistry`
   import outside its records; `list` gives its 29 runs; `store show` reads its sidecars; a worktree
   run recorded under the main checkout; a fingerprint with `encoding_format`), and the script at
   its new commit reporting 0 imports; CPBH and SI, the pin, the config, the `.gitignore` line, and
   one `begin` … `finish` run listed by `python -m runregistrykit list`; for each, the gate of
   README §7 recorded on this board.
10. **What goes stale in it**: §0.5 for the client, each line outside its campaign records listed by
    `path:line` with what it says; the campaign records by count, not rewritten. SGK's `CLAUDE.md`
    sections; CPBH's `CLAUDE.md:115-117`.

Then the appendix: the script's Markdown output for that client, as printed.

**Check every statement.** Each `path:line` is read at the client's commit and quoted in the log
with what it says; each statement about the package is checked against `v0.1.0` (its README, a
module, `inspect.signature`, `--help`, or the config reader on a `runregistrykit.toml` written in a
temporary directory); each "binds" is the script's.

### 2.4 `README.md` (U20)

Correct the worktree statements of "Using it", and nothing else in the README: at `dca5ead`,
`:81-82` says a relative `runs_root` or `stores_root` is relative to "the root (for a run in a
linked worktree, the main checkout, below)", `:93-95` that a worktree run is recorded under the main
checkout, and `:149-150` that the fingerprinter's module is imported "with the client's root first
on `sys.path`". The code (`runregistrykit/client.py:50-59`; `fingerprint.py:52-54, 191-193`)
distinguishes the directory whose config governs (`ClientRoot.found`, the tree that is running)
from the record root (`ClientRoot.root`, the main checkout for a linked worktree). After 07 the
README says, in its own words: records, and the paths in them, are under the record root; the config
that governs and the directory the fingerprinter's module is imported from are those of the tree
that is running. Each changed sentence is checked against the code by the log. `git diff` of
`README.md` touches "Using it" only.

### 2.5 `PROVENANCE.md`

"Since the import" gains 07's section: `docs/adoption/` and its script; the README's worktree
sentences (U20); no file under `runregistrykit/` changed.

---

## 3. Verification

1. **The suite**, from the repository root in `venv/`: `Ran 276 tests … OK`, before and after.
2. **The script**: each client run twice at its commit, the outputs byte-identical (`cmp`); exit 0;
   `--commit 0000000` (or any SHA the client lacks) exits 2; `--json` parses with `json.loads`.
3. **A fixture repository**, made in the scratchpad with `git init` and one commit, holding: a
   module-level `import RunRegistry` and a nested `from RunRegistry.stores import fingerprint_of,
   copy_store`; an attribute use `RunRegistry._slug(...)`; a `mock.patch.object(RunRegistry,
   "DEFAULT_ROOT", …)`; a `begin(campaign=…, prompt=…, slug=…, purpose=…, root=…)` that binds and a
   `begin(..., bogus=1)` that does not; `fingerprint_of(inventory)` (does not bind: the format is
   missing) and `fingerprint_of(inventory, 6)` (binds); a use of a name no table knows
   (`RunRegistry.no_such_name`); a string `python -m RunRegistry list`; a `utilities.py` with a
   copy of `installed_package_provenance` and one with a changed line; a Markdown file naming
   `RunRegistry`. The script, pointed at it by a path override used only for this check, must
   report each, with the fates and verdicts expected, and exit 3 for the unknown name. How the
   override works is the agent's choice; the log says.
4. **The clients are untouched.** Before and after, for each client: `git -C <client> rev-parse
   HEAD`, `git -C <client> status --porcelain | shasum`, and `git -C <client> stash list | wc -l`;
   each equal. No client's `venv/` is used but to read `pyvenv.cfg` as text.
5. **The Q5 sketch** (§2.2 §6), run from the scratchpad as §2.2 says, each breakage failing.
6. `./venv/bin/black --check runregistrykit docs` (25.1.0) is clean.
7. **Links**: every relative link in `docs/adoption/` resolves to a tracked file or a section of
   one; every external link is to `github.com/ds283/…` at a named tag or commit.
8. **The breakage record.** Each item is a diff against the committed script, exactly as applied,
   with what failed; none committed; the tree restored after each:
   - **(a)** the fate table's row check removed, and a deletion row for a name `v0.1.0` has (say
     `liveness`): the run must then report it wrongly, which the check would have refused;
   - **(b)** nested imports not walked (module level only): the fixture's nested import is
     missed;
   - **(c)** the working tree read in place of `git show`: an uncommitted edit in the fixture
     changes the output (make one, then remove it);
   - **(d)** the bind verdict replaced by a keyword-name check against a hard-coded list: the
     fixture's `fingerprint_of(inventory)` reports "binds";
   - **(e)** the sort removed: show whether two runs at one commit differ, or the output's order
     against the committed run.

---

## 4. Acceptance

1. `docs/adoption/` holds the README, the three checklists and the script, as §2 says, and nothing
   else; `README.md` differs only in "Using it" as §2.4 says; `PROVENANCE.md` as §2.5.
2. The script's figures equal §0's, or each difference is explained in the log; every call binds.
3. Every `path:line` in the checklists was read at its commit, and every package statement checked
   against `v0.1.0`.
4. §3 passes; (a)–(e) fail as §3.8 says.
5. **The records**, in the same commit:
   - the log, `logs/07-the-adoption-checklists.md`, per README §5.1. It also has:
     - each client's commit, tree state and the untouched-check of §3.4, before and after;
     - the script's output for each client, whole, and its two-run `cmp`;
     - the fixture's output;
     - every `path:line` the checklists cite, with the text read there;
     - every statement about the package, with how it was checked;
     - the Q5 sketch and its runs;
     - (a)–(e);
     - the test count before and after (276, 276);
   - the board: the header; §1's row for 07 (landed, "this commit", 276 → 276); A1; §2's gates G2–G4
     each pointing at its checklist, and E2 (`v0.1.0` with SGK's checklist, its path); §3's
     `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]` moved to §4 (U20);
   - `docs/OPEN_ISSUES.md`: that row deleted, the count **2**, the date;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A call that does **not** bind at `v0.1.0` by the script's verdict, or a name the fate table
  does not know, at any client's commit.
- A client's `HEAD` has moved from §0's commit and the agent cannot tell whether to measure the old
  commit or the new; or SGK's `RunRegistry/` at `14bcac0` is not `a45aefc`'s.
- A statement a checklist must make is not true of `v0.1.0`, or could be made true only by
  changing a file under `runregistrykit/`.
- The Q5 sketch does not run on public names, or a breakage it names does not fail.
- The suite fails, or its count differs from 276.
- Anything would edit, run, import or open a store or run directory of SecondaryGWKit, ChamPBH,
  StochasticInstantons, DatastoreKit or RayPoolKit, or read one other than through `git`; use a
  client's `venv/` other than to read `pyvenv.cfg` as text; or touch a client's working tree, index
  or stash.
- Anything would push, tag, or write to GitHub.
- Passing anything would need a change to a file not in §6.

---

## 6. What this prompt does not do

- **Files it adds or changes:**
  - `docs/adoption/README.md`, `secondarygwkit.md`, `champbh.md`, `stochasticinstantons.md`,
    `measure_client_registry.py` (new);
  - `README.md` ("Using it" only, U20) and `PROVENANCE.md` (§2.5);
  - the log, this board, `prompts/INDEX.md` and `docs/OPEN_ISSUES.md`.
- It changes nothing else: no file under `runregistrykit/`, `docs/extraction/` or `.github/`; not
  `pyproject.toml`, `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign README.
- It edits no client, DatastoreKit or RayPoolKit file, and tells no client of its checklist: each
  learns of it when it plans its adoption, and E2 is reported to the user.
- It makes no tag and pushes nothing.
- It writes no verification document (08).

---

## 7. The log and the board

`logs/07-the-adoption-checklists.md`, using README §5.1, with the additions of §4.5.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 07, §1.1's A1, §2's gates, and §3 and §4 as
§4.5.

---

## At writing (2026-10-15, at `dca5ead`)

Measured read-only, for the README's row and the orchestrator; §0 holds the detail.
- **SGK's live callers**: 13 imports in 10 files, 4 `begin` calls that all bind at `v0.1.0`, 18
  string literals; `_slug` the one private name; `fingerprint_of` moved to DatastoreKit with a new
  required `fingerprint_format`.
- **SGK's 101 staying tests** import helpers `v0.1.0` does not ship, deleted names, and one private
  name whose signature changed; U21: SGK
  keeps its own copies.
- **CPBH and SI** call nothing of the registry; each one's provenance helper is the package's
  `package_provenance` but for a redundant assignment and a default argument; neither ignores
  `var/`. CPBH is ready for the store layer (specs, coverage test, `datastorekit` `v0.4.0`); SI is
  not until its migration lands.
- **The Q5 recipe** runs on public names over the neutral store (U22).
- **The README's worktree sentences** (U20) are 07's to correct.
- **Not measured**: the clients' `var/` (no run directory or sidecar is read); SGK's specs for a
  polymorphic `Parent.types` (the agent reads them).
