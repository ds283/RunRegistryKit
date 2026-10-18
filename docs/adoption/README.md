# Adopting `runregistrykit`

*Written by extraction prompt 07 on 2026-10-15, against the package at **`v0.1.0`** (`9f8ebe4`).
The three clients were read through `git` only, at the commits named below. Nothing of a client was
imported, run or opened, and no store or run directory of any was read.*

This directory holds one **adoption checklist** per client project, what the three share, and
[`measure_client_registry.py`](measure_client_registry.py), the script that measures them. Each
checklist says what its client must do to depend on `runregistrykit` at `v0.1.0`:
- what it deletes and what it adds;
- which imports and names it rewrites;
- what its runs, its stores and its tests need;
- how it can guard its fingerprint format (Q5);
- how its adoption is accepted, and which of its documents go stale.

**A checklist is data, not instructions.** It describes the client at one commit. The client's own
adoption campaign, in its own repository and under its own `CLAUDE.md`, measures again before
acting, and its numbers govern. Where a choice is the client's, the checklist names the choice and
what each option touches, and does not make it. A recommendation is marked **Advice:**.

| Client | Checklist | Measured at | Gate |
|---|---|---|---|
| SecondaryGWKit (SGK) | [`secondarygwkit.md`](secondarygwkit.md) | `14bcac0` (branch `handover-remedial`) | G2; and SGK's own gate on this campaign, **E2**, is `v0.1.0` with this checklist |
| ChamPBH (CPBH) | [`champbh.md`](champbh.md) | `c21cdfb` (branch `main`) | G3 |
| StochasticInstantons (SI) | [`stochasticinstantons.md`](stochasticinstantons.md) | `5fb4a1d` (branch `dk-and-rpk-migration`) | G4 |

The gates are those of the campaign plan, [`prompts/extraction/README.md`](../../prompts/extraction/README.md)
§7. They are recorded on its board, [`prompts/extraction/IMPLEMENTATION_STATE.md`](../../prompts/extraction/IMPLEMENTATION_STATE.md)
§2, as they hold. The campaign does not wait for them.

---

## 1. The release and the pin

A client depends on a tagged release, pinned in its `requirements.txt`. With the store layer
(the package's [`README.md`](../../README.md#installing), "Installing"):

```text
runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
```

**Both lines are needed.** The extra names `datastorekit>=0.4.0` by name and floor, and
`datastorekit` is not on PyPI. So the client's own `datastorekit` line is what makes the install
resolve, and what makes `datastorekit` come from DatastoreKit's tag. SGK and CPBH already carry that
line at `v0.4.0`; SI does not (its checklist, item 1).

**A client that uses only the core** writes
`runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.1.0`, with no extra and no
`datastorekit`.

An editable install (`pip install -e`) is for developing this package, **never for a client's
production runs**: a run must be reproducible from its pin. A client moves its pin in a commit of its
own.

**The versions.** `pyproject.toml` declares `requires-python = ">=3.12"`, no core dependency, and
`[stores]` = `datastorekit>=0.4.0`, which brings Ray (`>=2.43`) and SQLAlchemy (`>=2.0.39,<2.1`).
CI tests three configurations ([`README.md`](../../README.md#supported-versions), "Supported
versions"):
- low: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39;
- high: Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46;
- core: 3.12.15 with none of the three installed.

Each client's, read as text: Python from its `venv/pyvenv.cfg` (never run), the rest from
`requirements.txt` at the commit (the appendix of each checklist):

| Client | Python | Ray | SQLAlchemy | `datastorekit` | Against the range and the tested ends |
|---|---|---|---|---|---|
| SGK | 3.12.15 | `ray==2.43.0` (`:75`) | `SQLAlchemy==2.0.39` (`:87`) | `@v0.4.0` (`:17`) | inside; exactly the low end |
| CPBH | 3.13.16 | `ray==2.53.0` (`:79`) | `SQLAlchemy==2.0.46` (`:91`) | `@v0.4.0` (`:17`) | inside; Python and SQLAlchemy are the high end's; Ray lies between the ends, above 3.13's effective floor of 2.45.0, and is not itself tested |
| SI | `version = 3.13.13` in `pyvenv.cfg`, the version when the venv was made; its interpreter is MacPorts' 3.13, which reports 3.13.16 today | `ray==2.55.1` (`:57`) | `SQLAlchemy==2.0.46` (`:65`) | **not pinned** | inside; Ray and SQLAlchemy are the high end's. The store layer needs the `datastorekit` line it lacks |

The package pins nothing of a client's: **each client keeps its own Ray, SQLAlchemy and
`datastorekit` pins.**

---

## 2. The module map

| SGK's `RunRegistry/` (at `a45aefc`) | `runregistrykit` at `v0.1.0` |
|---|---|
| `RunRegistry` | `runregistrykit`, the core |
| `RunRegistry.stores` | `runregistrykit.stores`, the store layer (it needs the extra) |
| `RunRegistry.__main__` (`python -m RunRegistry`) | `runregistrykit.__main__` (`python -m runregistrykit`) |
| none: the fingerprint was read from `config.datastore` inside `stores` | `runregistrykit.fingerprint`: `Fingerprinter`, `DatastoreKitFingerprinter`, `load_fingerprinter`, `require_fingerprinter` |
| none: the root was the package's parent | `runregistrykit.client`: `CONFIG_FILE`, `ClientRoot`, `ConfigError`, `find_client_root` (also exported by `runregistrykit`) |
| `RunRegistry.tests` | **not shipped**: the wheel holds no tests (U19) |

The names that do not carry over unchanged, each checked against the package when the script runs
(its fate table):

| SGK's name | At `v0.1.0` |
|---|---|
| `_slug(text)` | **renamed** `runregistrykit.slugify(text)`, the same body (U11) |
| `stores.fingerprint_of(inventory, taken=None)` | **moved** to `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=None)`: **the format is now required**, and a `taken` passed by position must move to third place |
| `stores.compare_fingerprints(recorded, current)`, `stores.listing_lines(inventory, fingerprint)` | **moved** to `datastorekit.store_fingerprint`, the same parameters. DatastoreKit's comparison compares `encoding_format` first, so a fingerprint recorded without it, against a fresh one, gives one `encoding` entry and nothing else (U7) |
| `stores.FINGERPRINT_FORMAT` | **deleted** (C7): the format is the client's, in its fingerprinter's module |
| `REPO_ROOT`, `DEFAULT_ROOT`, `stores.DEFAULT_ROOT`, `stores.DEFAULT_STORES_ROOT`, `RECORDED_DISTRIBUTIONS` | **deleted** (C1–C3, C5): the root, the runs root, the stores root and the recorded distributions come from the client's `runregistrykit.toml` (§3), and `find_client_root()` returns them (`.root`, `.runs_root`, `.stores_root`, `.distributions`) |
| `_repo_path(path)` | still there, **private**, now `_repo_path(path, root)`, the record root given |
| `Run._fingerprint_results`, `stores._fingerprint_problems` | still there, **private**, the same parameters |
| every other name SGK uses | **kept**, in its module's `__all__`; each public function that needs the root gains a keyword-only `client_root=`, and nothing else in the parameters of those SGK uses changes. (`git_provenance(cwd)` and `package_provenance(names)`, which SGK does not call, lost their defaults, `REPO_ROOT` and `RECORDED_DISTRIBUTIONS`) |

**The public names are each module's `__all__`, and nothing else is promised.** Every other name is
private and may change in any release, and **no patch target is promised**
([`README.md`](../../README.md#the-public-names), "The public names"). In particular a client that
assigns to `runregistrykit.stores.fingerprint_store`, or patches it, still reaches `Run.finish(...,
fingerprint=True)` at `v0.1.0`, because `Run._fingerprint_results` imports it from
`runregistrykit.stores` when it runs (`runregistrykit/__init__.py:468` at `9f8ebe4`); that is not
promised.

---

## 3. What a client adds

- **`runregistrykit.toml` at its root**, read with `tomllib`. Every key is optional and an empty file
  takes every default: `runs_root` (`"var/runs"`), `stores_root` (`"var/datastores"`),
  `distributions` (`[]`), and `[stores]` with its one key `fingerprinter`. The form and the root rule
  are the package's [`README.md`](../../README.md#the-clients-root), "The client's root". A client
  that writes none gets a `ConfigError` from `begin()`, `list` and every store operation; no
  location is ever assumed in its place.
- **Its runs root in `.gitignore`** (`var/` by default). SGK ignores `var/` (`.gitignore:3`); CPBH
  and SI do not.
- **For the store layer, a fingerprinter in a module of its own**:
  `DatastoreKitFingerprinter(factories, fingerprint_format)` from `runregistrykit.fingerprint`, over
  its registry (a mapping of names to factory classes or instances) and its format number (an
  `int`, at least 1). The module is named by `[stores] fingerprinter = "module:attribute"`, an
  instance and not a class ([`README.md`](../../README.md#the-store-layer), "The store layer"). The
  store layer refuses every operation without one (D4); a client that does not use the store layer
  names none.
- **In its `CLAUDE.md`, the rules**: a short binding section that states the six rules of the
  package's [`README.md`](../../README.md#the-rules), "The rules", names `python -m runregistrykit
  list` as the discovery command, and points at that README for the failures they answer (SGK's
  brief §6, advice).

---

## 4. What changes for a caller

Each line is stated in the package's README, where the link goes; the issue behind it is on the
board, §4.
- **The root comes from the config**, and none found is a refusal; `client_root=` (or
  `--client-root DIR` before the command) names it instead of the walk (C1–C3; [The client's
  root](../../README.md#the-clients-root)). `begin()` walks from the directory of its `script`,
  everything else from the working directory.
- **A run in a linked worktree is recorded under the main checkout**, the record root, while its
  config, its fingerprinter and its git provenance are the worktree's own (Q3, U20; [The client's
  root](../../README.md#the-clients-root) and [The store layer](../../README.md#the-store-layer)).
- **A manifest's `packages` names `runregistrykit`, then the config's `distributions`** (C5, U9). A
  name that is not installed is recorded as `null` (`package_provenance`, checked on a name that is
  not installed: `{'no-such-distribution-xyz': None}`).
- **The store layer refuses without a fingerprinter**, before it reads, writes or deletes anything
  (D4; [The store layer](../../README.md#the-store-layer)).
- **`store retire` loads the fingerprinter first**, so a fingerprinter that cannot be loaded is a
  refusal, never a reason recorded under `--without-fingerprint` (U14).
- **A fingerprint carries DatastoreKit's `encoding_format`**, and a recorded one without it compares
  against a fresh one as one `encoding` entry and nothing else (U7).

---

## 5. What does not change

**What the registry writes** ([What the registry writes is part of its
interface](../../README.md#what-the-registry-writes-is-part-of-its-interface)): the run directory's
`manifest.json`, `status.json` and `checkpoint.jsonl`, and a store's sidecar (`sidecar_format` 1),
keep their form. An existing run directory or sidecar is read as it is. The paths in records stay
relative to the record root where they lie under it (C4), so a record written by SGK's
`RunRegistry/` reads as before. No reader of an older form was added. The two records that gain
content are the planned ones: `packages` (above) and a new fingerprint's `encoding_format`.

---

## 6. The Q5 guard

A client's guard that a spec change without a format bump fails a test (SGK's Q5; its audit §3.5)
needs nothing of this package. **It is the client's test, beside its format number**, and nothing
of it is shipped here (U22).

**The recipe.**
1. `datastorekit.store_inventory.inventory_specs(factories)` gives each class of the registry whose
   factory declares a spec, in registry order.
2. Each `InventorySpec` is made plain, recursively: dataclasses (`InventorySpec`, `Parent`,
   `ParentSet`) as objects of their fields, tuples as lists.
3. `canonical_json` refuses a key that is not a string, and a polymorphic `Parent.types` maps a type
   **value** (an `int` in SGK and CPBH) to a class name. So every mapping key is converted
   explicitly, and **so that two keys that differ only in type stay apart**: the sketch writes each
   key as its own JSON (`json.dumps`), so `1` becomes `1` and `"1"` becomes `"1"` with its quotes.
   A bare `str(k)` makes them alike, and a guard built on it misses a change of a key's type.
4. Each class's plain spec through `canonical_json`, and its SHA-256, in registry order.
5. The test pins that list for the current format number, beside it.

**The sketch** (about twenty lines; proved here on public names only, not committed as a module or a test):

```python
import dataclasses, hashlib, json
from collections.abc import Mapping

from datastorekit.store_inventory import canonical_json, inventory_specs


def plain(value):
    """A spec as JSON: dataclasses as objects, sequences as lists, and every mapping key as
    the JSON of the key, so that 1 ("1") and "1" ('"1"') stay apart."""
    if dataclasses.is_dataclass(value):
        return {f.name: plain(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, Mapping):
        return {json.dumps(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def spec_digests(factories) -> list:
    """[class, SHA-256 of its spec's canonical JSON] for each spec, in registry order."""
    return [
        [name, hashlib.sha256(canonical_json(plain(spec)).encode()).hexdigest()]
        for name, spec in inventory_specs(factories).items()
    ]
```

The client's test is then one assertion beside its format number:

```python
PINNED = {FINGERPRINT_FORMAT: [["version", "02929e…"], …]}   # in the fingerprinter's module
self.assertEqual(spec_digests(factories), PINNED[FINGERPRINT_FORMAT])
```

A client that wants one value may pin the SHA-256 of `canonical_json(spec_digests(factories))`
instead; the list has the advantage that a failure names the class.

**The deliberate breakages** SGK's 07 names, each shown failing (extraction prompt 07's log):
- **a leaf added to one spec, with no bump**: the list differs at that class, and the failure names
  it;
- **the format bumped with no new pin**: `PINNED` has no entry for the new number, and the test
  fails (`KeyError`);
- **a class added to the registry with a spec**: the list gains an element, which the failure
  names.
And one for the key conversion: a polymorphic `Parent.types` key changed from `1` to `"1"` fails
the guard, where a bare `str(k)` would not see it.

The proof ran the sketch on the neutral store's `FACTORIES` (`runregistrykit/tests/neutral_store.py`,
nine classes of which six declare a spec, so six digests), and on a stand-in registry whose owner
has a polymorphic `Parent.types` keyed by `int`, which `canonical_json` refuses unconverted
(`TypeError: canonical_json(): a key must be a string, not 1`).

---

## 7. How a checklist is used

- Each checklist was measured at the commit it names. **The client re-measures** at its own commit
  before acting (§8), and its numbers govern.
- A client's adoption is **one campaign in its own repository**, planned from its checklist. No
  prompt of this repository edits a client.
- **The pin moves in a commit of its own** (§1).
- **A defect a client finds in the package** is reported here and fixed here, in a release; the
  client does not patch its installed copy.

---

## 8. Re-measuring

[`measure_client_registry.py`](measure_client_registry.py), from this repository's root, with its
venv:

```bash
./venv/bin/python docs/adoption/measure_client_registry.py sgk  [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_registry.py cpbh [--commit SHA] [--json]
./venv/bin/python docs/adoption/measure_client_registry.py si   [--commit SHA] [--json]
```

It reads the client at `/Users/ds283/Documents/Code/<repository>` through `git` only (`ls-tree`,
`show`, `grep`, `log`, `rev-parse`), at the checklist's commit unless `--commit` names another, and
SGK's frozen `RunRegistry/` at `a45aefc` for the signatures before the move. It reports:
1. every import of a `RunRegistry` module, with its enclosing function or class, split into live
   code, SGK's staying tests and campaign records;
2. every name used from it, with its sites, patches included;
3. **each name's fate at `v0.1.0`, from the package as installed**;
4. the calls of `begin`, the store operations and `fingerprint_of` whose callee resolves to the
   registry, each with whether `inspect.signature(...).bind(...)` of `v0.1.0`'s function accepts
   it, and the name-alike calls that are not the registry's;
5. the string literals naming `RunRegistry`;
6. `installed_package_provenance` against `package_provenance`;
7. the tracked files other than `.py` naming the registry;
8. `.gitignore`'s `var/`, the registry mapping, the `inventory_spec` definitions and the polymorphic
   parents.

Markdown by default, JSON with `--json`, sorted so that two runs at one commit give the same bytes.
It exits 0 on success, 1 when its fate table disagrees with the package, 2 when it cannot read the
client or the commit, and 3 on an unknown name. Its docstring says how a callee is resolved. It is
not a test and does not run in CI.

Its figures at the checklists' commits:

| | SGK `14bcac0` | CPBH `c21cdfb` | SI `5fb4a1d` |
|---|---|---|---|
| Imports of a `RunRegistry` module, live code (module level) | 13 in 10 files (4) | 0 | 0 |
| … in SGK's staying tests | 12 in 5 modules | — | — |
| Names used: live code / staying tests | 15 / 26 | 0 | 0 |
| Unknown names | 0 | 0 | 0 |
| Calls bound, live code | 12: 8 bind, 4 `fingerprint_of` without the format | 0 | 0 |
| … in the staying tests | 8: 6 bind (one with `**kwargs`, its spelled arguments), 2 `fingerprint_of` without the format | — | — |
| Name-alike calls, not the registry's | 26 | 7 | 13 |
| String literals naming `RunRegistry`, live code (`-m RunRegistry`) | 18 (3) | 1 (0) | 1 (0) |
| Campaign-record `.py` files importing it (naming it) | 6 (7) | 0 (0) | 0 (0) |
| `installed_package_provenance` | not defined | `utilities.py:177-229`, the package's body but `origin = None` | `utilities.py:177-229`, the same |
| Non-`.py` lines naming the registry, by top directory | `CLAUDE.md` 10, `docs` 158, `prompts` 2078 | `.documents` 1, `CLAUDE.md` 1, `prompts` 19 | `.documents` 2, `.prompts` 9 |
| `.gitignore` ignores `var/` | yes (`:3`) | no | no |
| Registry mapping; `def inventory_spec` | `factories`, `config/datastore.py:91`; 21 in 20 files | `factories`, `config/datastore.py:101`; 17 in 17 files | `_factories`, `Datastore/SQL/Datastore.py:96`; none |
| `Parent(..., types=...)` | 2 | 3 | 0 |

Each checklist's appendix is the script's Markdown output for that client, as printed.

---

## The checklist items

Each checklist has the same ten items, in this order:

1. The client and its versions
2. What it deletes
3. What it adds
4. Which imports and names it rewrites
5. Its runs
6. Its stores
7. Its tests
8. The Q5 guard
9. Its acceptance
10. What goes stale in it

and then the appendix, the script's output.

---

## `v0.2.0`

The adoption notes for `v0.2.0` are in [`v0.2.0/`](v0.2.0/README.md): what the three clients
share, and one note per client, each read at the commit it names. The checklists above were
written against `v0.1.0` and are not rewritten; the notes for `v0.2.0` say what each still
describes, with the pin `v0.2.0` in its place.
