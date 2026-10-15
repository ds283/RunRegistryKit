# Prompt 06 — supported versions, CI, and ready for `v0.1.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 05c landed (`a7d93d5`) and was reviewed (`3372292`, the board's §1).
- U13, U18 and U19 are taken (README §6.2, 2026-10-15, as recommended).
- `git diff --stat 3372292 HEAD -- runregistrykit docs/extraction pyproject.toml PROVENANCE.md
  CLAUDE.md README.md .gitignore` is empty, and no `.github/` exists.
- The suite is `Ran 276 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[05c-the-import-test-needs-datastorekit]` (U18). **Narrows:** nothing. **Opens:** only
what the work finds.

**Recommended model:** **Opus.**
- The code is small: `pyproject.toml`, one workflow file, the README.
- Its weight is in two places. The suite runs in four venvs it has never run in, and then, after
  the push, on Linux; each fails in its own way if it is set up wrongly. And the README's new
  sections are what a client reads when it adopts: every statement in them must be true of the
  package as it will be tagged, checked against the code and not against this prompt.

**Read first:**

1. [`README.md`](README.md): §1, §2 (rows 05c–08), §4, §5 (rules 5, 6, 7, 10 and 12), §6.2 (U3,
   U5, U6, U9, U11, U13, U18 and U19) and §7.
2. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`, above all "Releases" and "Repository
   mechanics".
3. The board: the header, §3's three open issues in full, and the review of 05c.
4. The repository as 05c left it: `pyproject.toml`, `.gitignore`, `README.md`, `PROVENANCE.md`
   ("Since the import"); the module docstrings of `runregistrykit/__init__.py`, `client.py`,
   `fingerprint.py`, `stores.py` and `__main__.py`, and `python -m runregistrykit --help` with
   `list --help` and `store <command> --help`; `runregistrykit/tests/test_package_imports.py`,
   `client_fixtures.py` (how the tests isolate `git`) and `test_package_is_generic.py:1-70`.
5. For comparison only: RayPoolKit's `prompts/extraction/03-supported-versions-and-ci.md` and
   DatastoreKit's and RayPoolKit's `.github/workflows/tests.yml`, read with `git -C
   /Users/ds283/Documents/Code/<repository> show HEAD:<path>`. They solved the same problem; nothing
   is copied from them without checking it here.

Facts below are at `3372292`, whose `runregistrykit/` is `a7d93d5`'s, measured on 2026-10-15.

---

## 1. What is wanted

06 makes the package ready to be released as **`v0.1.0`** (U3), the release the clients adopt.
After it:

- `pyproject.toml` says `0.1.0`, declares U13's range, and builds a wheel without the test package
  (U19);
- a GitHub Actions workflow runs the suite at both ends of U13's range with `datastorekit` installed
  from its tag, and the core alone in a third job with no `datastorekit`, `ray` or `sqlalchemy`
  (U13, U18);
- `README.md` says what `v0.1.0` is, what it supports, how a client installs it, how a client uses
  it, and how to develop it;
- **the suite has run, and passed, in fresh venvs at each end and in the core job's venv, and the
  package imports from an installed wheel**, all on this machine, before anything reaches GitHub.

**06 makes no tag and pushes nothing** (README §5 rule 12). After its review, pushing `main` is put
to the user. CI must then pass, all three jobs, on 06's commit, and only then is `v0.1.0` made,
annotated, on that commit, and pushed, by the user or on the user's instruction. If CI fails, a fix
prompt lands first: no tag is ever made on a commit whose CI is red, since rule 12 forbids moving
one. The tag is not this prompt's work.

**No behaviour of the package changes.** No file under `runregistrykit/` is touched: not a module,
not a test, not the guard. The suite stays at **276**.

---

## 2. What to change

### 2.1 `pyproject.toml` (U13, U19)

At `3372292` it reads, in full:

```toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"

[project]
name = "runregistrykit"
version = "0.1.0.dev0"
description = "A run registry: run directories, manifests, heartbeats and datastore sidecars for long jobs"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
stores = [
    "datastorekit",
]

[tool.setuptools]
include-package-data = false

[tool.setuptools.packages.find]
include = ["runregistrykit*"]
```

Change exactly three things:
- `version = "0.1.0"`;
- `[stores]`: `"datastorekit>=0.4.0"`. **By name and floor, never a git URL** (SGK's brief §7):
  `datastorekit` is not on PyPI, each client installs it from its own pinned tag, and a URL here
  would conflict with that pin; a bare name with a floor is satisfied by whatever tag the client
  installed. The floor is E1's release;
- `[tool.setuptools.packages.find]` gains `exclude = ["runregistrykit.tests",
  "runregistrykit.tests.*"]` (U19).

Nothing else: `requires-python` and `dependencies = []` are already U13's, and
`include-package-data = false` stays (it is what keeps a stale `runregistrykit.egg-info/` from
shipping test files, hazard 3). No classifiers, URLs or licence field; `LICENSE` already reaches the
wheel's `dist-info/licenses/`.

### 2.2 What the planner measured

On this machine (macOS, arm64), in the session scratchpad, with nothing in the repository written:

- **The wheel as it stands**, built with `uv build --wheel` (`uv` 0.12.20) from a `git archive` of
  `3372292`: `runregistrykit-0.1.0.dev0-py3-none-any.whl`, **29 entries, 19 of them test modules**
  under `runregistrykit/tests/`, and **none of `tests/data/*.json`** (package data is off). The guard
  could not run from it, and no client should import it. Hence U19.
- **With §2.1's `pyproject.toml`**: `runregistrykit-0.1.0-py3-none-any.whl`, **10 entries** (the
  five modules, `dist-info/licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt`, `RECORD`),
  54,940 bytes. `METADATA`: `Version: 0.1.0`, `Requires-Python: >=3.12`, `Provides-Extra: stores`,
  `Requires-Dist: datastorekit>=0.4.0; extra == "stores"`. With the repository's stale
  `runregistrykit.egg-info/` (whose `SOURCES.txt` lists 19 test files) copied into the export, the
  same 10 entries.
- **The release check**, that wheel installed (not editable) into a fresh 3.13.16 venv with
  `datastorekit` from `v0.4.0`, `ray==2.55.1`, `sqlalchemy==2.0.46`, run with `-I` from an empty
  directory: the five modules import from `site-packages`; `ray`, `sqlalchemy` and `datastorekit`
  are not in `sys.modules` afterwards; `DatastoreKitFingerprinter` imports from
  `runregistrykit.fingerprint`; `importlib.metadata.version` is `0.1.0` and `requires` is
  `['datastorekit>=0.4.0; extra == "stores"']`; `import runregistrykit.tests` raises
  `ModuleNotFoundError`; `python -m runregistrykit --help` exits 0.
- **Both ends, fresh venvs**, each made with `uv venv -p /opt/local/bin/python3.1x` and one resolve,
  `uv pip install "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0" -e ".[stores]"
  "ray==…" "sqlalchemy==…" "black==25.1.0"`:

  | End | Python | Ray | SQLAlchemy | `datastorekit` | Suite |
  |---|---|---|---|---|---|
  | low | 3.12.15 | 2.43.0 | 2.0.39 | 0.4.0 | `Ran 276 tests in 102.8s`, OK |
  | high | 3.13.16 | 2.55.1 | 2.0.46 | 0.4.0 | `Ran 276 tests in 102.2s`, OK |

  No Ray process before or after; `git status` unchanged.
- **The core, in a fresh 3.12.15 venv** holding only `runregistrykit` (editable, `uv pip install
  -e .`): discovery loads **37 tests in two modules**, `test_run_registry` (29) and
  `test_public_names` (8), and fails to import the other twelve, each on `datastorekit`:
  `test_package_imports` through the guard (`[05c-the-import-test-needs-datastorekit]`),
  `test_client_root` on two module-level imports that only `TestStoresUnderTheRoot`'s two tests
  use, and the ten store and guard modules. `python -m unittest runregistrykit.tests.test_run_registry
  runregistrykit.tests.test_public_names` gives `Ran 37 tests … OK`.
- **The core's smoke**, in that venv, from an empty directory with `-I`: the five modules import,
  and none of `ray`, `sqlalchemy`, `datastorekit` is in `sys.modules`; `-m runregistrykit --help`
  exits 0; `-m runregistrykit list` exits 1 with `!! No runregistrykit.toml in <dir> or any
  directory above it. …`; after `touch runregistrykit.toml`, `list` exits 0 with `no runs under
  <dir>/var/runs`; `runregistrykit.begin(campaign=…, prompt=…, slug=…, purpose=…)` then
  `finish("done", exit_code=0)` makes one run, and `list` shows it `done` and exits 0;
  `store show x.sqlite` exits 1 because the config names no fingerprinter.
- **The resolver refuses outside the range**, by `uv pip install --dry-run` with §2.1's
  `pyproject.toml`: `datastorekit` from `v0.3.0` ("only datastorekit<0.4.0 is available and
  runregistrykit[stores]==0.1.0 depends on datastorekit>=0.4.0"); `requires-python = ">=3.13"` at
  3.12.15 ("the current Python version (3.12.15) does not satisfy Python>=3.13"); and `-e ".[stores]"`
  with no `datastorekit` given ("datastorekit was not found in the package registry").
- **PyPI.** `https://pypi.org/pypi/datastorekit/json` and `…/runregistrykit/json` are both 404.
  Newest releases: `ray` 2.59.0, SQLAlchemy 2.1.4 (outside DatastoreKit's `<2.1`). On Python 3.13,
  `uv pip compile --only-binary ray` resolves `ray==2.45.0` and not `ray==2.44.1`, so **on 3.13
  Ray's floor is in effect 2.45.0**.
- **CI.** `ds283/RunRegistryKit` is public, default branch `main`, Actions enabled with all actions
  allowed, **no workflow ever run**. `origin/main` is at `dfcb884`, behind local `main`. The latest
  releases are `actions/checkout` `v7.0.1` and `actions/setup-python` `v7.0.0`;
  `actions/python-versions`' manifest has `python-3.12.15-linux-24.04-x64` and
  `python-3.13.16-linux-24.04-x64`. DatastoreKit's and RayPoolKit's workflows use `@v7` of each.
- **`git` in CI.** Every test `git` call goes through `client_fixtures.git`, which passes the
  identity with `-c` and sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`, so a runner
  with no git identity needs none. The tests use `git init -b` (git ≥ 2.28) and `git worktree add`.

### 2.3 The venvs

Make four venvs **in the session scratchpad**, never under the repository, with `uv`:

| Venv | Interpreter | Installed, in one resolve |
|---|---|---|
| low | `/opt/local/bin/python3.12` | `"datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0"`, `-e ".[stores]"`, `ray==2.43.0`, `sqlalchemy==2.0.39`, `black==25.1.0` |
| high | `/opt/local/bin/python3.13` | the same, with `ray==2.55.1`, `sqlalchemy==2.0.46` |
| core | `/opt/local/bin/python3.12` | `-e .` and nothing else |
| release | `/opt/local/bin/python3.13` | the wheel of §2.4 (not editable), `datastorekit` from `v0.4.0`, `ray==2.55.1`, `sqlalchemy==2.0.46` |

- One resolve per venv is the workflow's install step (§2.5), and checks the pins against
  `pyproject.toml`'s range.
- Record each venv's `sys.version`, and in the first three `importlib.metadata.version` of
  `runregistrykit`, `datastorekit`, `ray` and `sqlalchemy` (or that each extra is absent), and
  `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` before and after every suite run.
- **Downloads**: PyPI packages, and `datastorekit` from its GitHub tag, into the scratchpad; nothing
  else.
- **The project's `venv/` is not rebuilt.** After §2.1, reinstall the package in it with
  `./venv/bin/python -m pip install --no-deps -e .`, so that its metadata says `0.1.0`, and run the
  suite there too. Record `pip freeze` before and after; only `runregistrykit`'s line changes.

### 2.4 The release check

Build from a fresh export: `git archive HEAD | tar -x -C <scratch>/export-<n>` into a new, empty
directory; copy the working tree's `pyproject.toml` over the export's (the one file 06 changes that
the build reads); then `uv build --wheel --out-dir <scratch>/dist-<n> <scratch>/export-<n>`. One
export per build, never a build in the repository (hazard 3). Install the wheel into the release
venv. Then, from a new empty directory, with `PYTHONPATH` unset and `-I`, check and record §2.2's
release-check list, item by item. Record the wheel's name, size, entry count, SHA-256 and file
list. The wheel's bytes are not reproducible; do not compare them with the planner's.

### 2.5 The workflow

`.github/workflows/tests.yml`:
- **A comment at the top**: the suite at both ends of the supported range, and the core alone
  without the store layer's dependencies (README "Supported versions"); the checks under
  `docs/extraction/` read the client repositories and run locally only.
- **Triggers:** `push` to `main`, `pull_request`, `workflow_dispatch`. **Permissions:** `contents:
  read`. No secrets, no cache, no artefact upload, no action but the two below.
- **Job `suite`**, `ubuntu-24.04`, `fail-fast: false`, a matrix of exactly two entries, `low` and
  `high`, holding §2.3's Python, Ray and SQLAlchemy versions, and a job name that shows the entry.
  Steps:
  1. `actions/checkout@v7`;
  2. `actions/setup-python@v7`, with the matrix's Python;
  3. `python -m pip install --upgrade pip`, then, in one command,
     `python -m pip install "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0" -e
     ".[stores]" "ray==…" "sqlalchemy==…"`;
  4. print `sys.version` and the versions of `runregistrykit`, `datastorekit`, `ray`, `sqlalchemy`
     and `git --version`;
  5. `python -m unittest discover -s runregistrykit/tests -t .`;
  6. on `low` only: `python -m pip install black==25.1.0` and `black --check runregistrykit docs`.
- **Job `core`**, `ubuntu-24.04`, Python 3.12.15 (the floor: the core has no dependency, so the
  lowest Python is its tightest test). Steps:
  1. and 2. as above;
  3. `python -m pip install --upgrade pip`, then `python -m pip install -e .`;
  4. **the extra is absent**: a step that fails if `importlib.util.find_spec` finds `datastorekit`,
     `ray` or `sqlalchemy`, so that the job cannot pass by accident with them installed;
  5. `python -m unittest runregistrykit.tests.test_run_registry
     runregistrykit.tests.test_public_names` (U18; the two modules by name, never discovery);
  6. **the smoke**, from a new temporary directory (`mktemp -d`), each command with `-I`, as
     §2.2's core smoke: the five modules import and none of the three is loaded; `--help` exits 0;
     `list` with no config exits non-zero and says `No runregistrykit.toml`; with an empty
     `runregistrykit.toml`, a `begin(...)` and `finish("done", exit_code=0)`, then `list` exits 0
     and names the run. Write it as shell and an inline `python -I -c` or here-document; keep it
     short, and make every check fail the step if it is not met.
- It runs nothing that reads a client (hazard 5).

**Replay it here.** GitHub cannot run it from this machine. Run each job's steps by hand in §2.3's
venvs, with `uv` in place of `pip`; the core job's steps 4–6 exactly as written in the file (copy
them, do not paraphrase). The log records each command as run and the workflow step it stands for,
and names any step with no local counterpart. Validate the file as YAML with PyYAML from the low
venv (Ray depends on it): `<venv>/bin/python -c "import yaml, sys;
print(yaml.safe_load(open(sys.argv[1])))" <file>` (PyYAML reads `on` as `True`; GitHub reads it
correctly). Check that the matrix equals §2.3's table and the core job's Python is 3.12.15.

### 2.6 U18: the import test and the core job

`[05c-the-import-test-needs-datastorekit]` is **closed by U18, with no change to a test**:
- `test_package_imports.test_import_loads_nothing_heavy` asserts that importing the package and its
  store layer loads none of `ray`, `sqlalchemy`, `datastorekit`. That is a check only where they are
  installed: in the core job nothing could load them. So it belongs to the `suite` jobs, which run
  it at both ends, and its importing the guard costs nothing there.
- What the core job alone can check, that the package imports and runs **without** them installed,
  is the core job's steps 4–6.
- The module-scope rule (`test_module_scope_is_the_standard_library_and_the_package`) runs in the
  `suite` jobs too, statically.

The board's issue is moved to §4 with this prompt's commit and that reasoning (§4.3).

### 2.7 The README

The repository's `README.md` keeps its opening paragraph, "The rules", "The public names" and
"Licence" exactly as they are. It changes as follows; each new section is written **as of the
tag**: the README is committed before `v0.1.0` exists, and must be true once it does.

- **Status** (`:12-16`, "Status: being extracted. The code does not live here yet. …") is replaced:
  `v0.1.0` is SecondaryGWKit's `RunRegistry/` package, moved here and made generic: the client's
  root and settings come from its `runregistrykit.toml`, and the store layer takes the client's
  fingerprinter; SecondaryGWKit, ChamPBH and StochasticInstantons adopt it from here. Point at
  `PROVENANCE.md` for where each part came from and what changed, and at the campaign README and
  board. The paragraph on DatastoreKit (`:18-21`) stays.
- **Supported versions**, a new section after Status: a table of the declared range (§2.1) and the
  three tested configurations (§2.3's low, high and core). Say: on Python 3.13 Ray's floor is in
  effect 2.45.0; releases inside the range but newer than the high end (Python 3.14, Ray 2.59.0
  today) are allowed and not tested; SQLAlchemy is held below 2.1 by DatastoreKit, not here; a
  client pins its own `datastorekit`, `ray` and `sqlalchemy`.
- **Installing**, a new section: in a client's `requirements.txt`, the pinned form `CLAUDE.md`
  gives, `runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0`, **beside**
  the client's own `datastorekit @ git+https://github.com/ds283/DatastoreKit@<tag>` at `v0.4.0` or
  later. Say why both lines: `datastorekit` is not on PyPI, the extra names it only by name and
  floor, and without the client's own pin the install fails to resolve. A client that uses only the
  core writes `runregistrykit @ git+…@v0.1.0`, with no extra. One sentence: an editable install is
  for developing this package, never for a client's production runs.
- **Using it**, a new section, in prose and short lists, not a worked program. Every statement is
  read from the code, and every name is checked (§3.5):
  - **the client's root**: a `runregistrykit.toml` at it, its keys and defaults (`runs_root`,
    `stores_root`, `distributions`, `[stores] fingerprinter`), how it is found (the walk, from
    `begin()`'s `script` or the working directory), `client_root=` and `--client-root`, and that a
    run in a linked worktree is recorded under the main checkout; the client's `.gitignore` ignores
    the runs root;
  - **a run**: `begin(...)`, its required and optional arguments as `inspect.signature` gives them,
    what it writes first and where (the run directory and its manifest); `Run`'s methods a job calls
    while it runs and at the end, as the module defines them; `python -m runregistrykit list` and
    what liveness it reports;
  - **the store layer**: that it needs the extra and a fingerprinter; how a client names one, a
    `DatastoreKitFingerprinter` built in a module of its own over its registry, as
    `runregistrykit.fingerprint` documents it; the `store` commands, one line each, from `--help`;
    that `retire` alone deletes, and only a store's own files;
  - **what the registry writes is part of its interface** (`CLAUDE.md`, "Releases"): the manifest,
    `status.json`, `checkpoint.jsonl` and the sidecar; a change to any is a release of its own.

  Do not write a client in the README, and name no client's script, store or campaign. Point at
  `runregistrykit/tests/neutral_store.py` in this repository as a worked fingerprinter over a small
  registry, and say it is not installed with the package.
- **Developing**, a new section before Licence: a venv, `pip install` of `datastorekit` from its
  tag with `-e ".[stores]"`, the suite's command from `CLAUDE.md`, and what it needs (`git` on
  `PATH`, a git work tree, no Ray cluster); that CI runs it at both ends and the core alone; that
  the checks under `docs/extraction/` read the clients' repositories through `git` and run locally
  only.

**Nothing else in the README changes.** In particular "The public names" keeps "(it needs the extra
`[stores]`)"; if the new sections say more precisely what needs the extra, they say it in their own
words.

### 2.8 `PROVENANCE.md`

"Since the import" gains 06's section, after 05c's: `pyproject.toml`'s version, range and
exclusion; the workflow and its three jobs; the README's new sections; that no file under
`runregistrykit/` changed. Nothing above it changes.

---

## 3. Hazards and verification

**Hazards.** Check each, and say in the log what you found.

1. **The guard needs a git work tree and the tests need `git`.** Both hold in CI (`actions/checkout`
   makes a work tree; `ubuntu-24.04` has `git`). `test_manifest_carries_the_provenance_triple` reads
   the checkout's commit; a shallow checkout has one. Nothing to change; record it.
2. **The tests need the package installed.** `test_package_imports` runs `sys.executable -I` from
   an empty directory, so it finds `runregistrykit` only through an installation. Every venv, and
   every CI job, installs it, editable.
3. **A stale build leaks files into a wheel.** Build every wheel from a fresh export, one per build,
   never in the repository; `git status` shows no `build/`, `dist/` or new `*.egg-info` after.
4. **Linux is not measured.** The suite has only run on macOS. CI is its first Linux run; nothing
   here stands in for it, which is why the tag waits.
5. **The checks cannot run in CI.** `docs/extraction/measure_client_vocabulary.py` and
   `compare_with_source.py` read the clients through `git`. The workflow runs neither.
6. **A by-name extra can resolve from PyPI.** `datastorekit` is not on PyPI today, so a `[stores]`
   install without the client's own pin fails; if the name were ever registered there by someone
   else, it would resolve to that. The README's Installing says the client pins `datastorekit`
   itself (§2.7), and every CI install names the tag.

**Verification.**

1. **The suite, five times**, each `Ran 276 tests … OK` but the core's: `venv/` before and after the
   reinstall; the low and high venvs; and in the core venv the two modules, `Ran 37 tests … OK`.
   Per-module counts in `venv/` after equal 05c's. No Ray process before or after any run.
2. **The release check** of §2.4 passes, with its record.
3. **The workflow**, replayed as §2.5 says, all three jobs; the file parses; the matrix and the core
   job's Python as §2.3.
4. `./venv/bin/black --check runregistrykit docs` is clean (26 files). `black` is not run on the
   workflow or the README.
5. **Every name and link in the README's new sections** is checked: each importable name by
   importing it in the low venv, each argument and default by `inspect.signature`, each command and
   option by its `--help`, each config key and default by `runregistrykit.client`'s reader (a
   `runregistrykit.toml` written in a temporary directory), each file and section link by finding
   it. The log lists them, each with how it was checked.
6. **The breakage record.** Each item is a change exactly as applied, in a scratch export or a
   throwaway venv, with what failed. None is committed, and `git status` is clean after each.
   Diffs to tracked files are recorded so that `git apply --check` replays them from the commit,
   checked with `--check` and `-R --check`.
   - **(a) The tests shipped:** §2.1's `exclude` removed. The release check fails: the wheel lists
     files under `runregistrykit/tests/`, and `import runregistrykit.tests` succeeds.
   - **(b) The floor:** the low venv's install with `datastorekit` from `v0.3.0`. The resolver
     refuses, naming `datastorekit>=0.4.0`.
   - **(c) The Python floor:** `requires-python = ">=3.13"`. The core venv's install refuses.
   - **(d) The extra alone:** the `suite` job's install without the `datastorekit` URL. The
     resolver refuses: `datastorekit` is not in the registry (hazard 6).
   - **(e) A heavy import in the core:** `import datastorekit` added at module scope of
     `runregistrykit/client.py`. The core job's step 6 fails at the first import; in the low venv,
     `test_package_imports` fails. Each kind of job catches it.
   - **(f) The extra present in the core job:** `datastorekit` installed into a throwaway copy of
     the core venv. The core job's step 4 fails.

---

## 4. Acceptance

1. `pyproject.toml` is §2.1's, and nothing else in it changed.
2. The workflow is §2.5's, parses, and was replayed, all three jobs.
3. `README.md` is §2.7's and every name in it exists; `PROVENANCE.md` is §2.8's.
4. §3's verification 1–6 holds, and each hazard is recorded.
5. **The records**, in the same commit:
   - the log, `logs/06-release-v0.1.0.md`, per README §5.1. It also has: each venv's versions and
     each suite's verdict line and time; every install command as run, and the workflow step each
     stands for; the release check (the wheel's name, size, entry count, SHA-256, file list, and
     each command's output); every README name, with how it was checked; the six hazards; (a)–(f);
     `pip freeze` of `venv/` before and after;
   - the board: the header, §1's row for 06 (landed, "this commit", 276 → 276), §1.1's V1, a line in
     the header saying that `v0.1.0` is ready to be tagged on 06's commit once CI passes there, all
     three jobs, with no tag made; §3's `[05c-the-import-test-needs-datastorekit]` moved to §4
     (U18, §2.6); `[00-the-shard-fixtures-reach-into-shardedpool]` and
     `[00-a-refusal-matches-datastorekit-message-text]` each gain *Package lines (06, …)*, saying
     that CI now pins `datastorekit` at `v0.4.0` at both ends (the first's next step, and where the
     second's test runs), and both stay open, owner none; §3's opening count sentence;
   - `docs/OPEN_ISSUES.md`: the row deleted, the count **2**, the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `PROVENANCE.md`: §2.8.

---

## 5. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 276 (37 in the core), in any venv. A failure at one end
  is not "fixed" in the package or the tests: record what fails, and ask.
- Passing anything would need a change under `runregistrykit/`, or to any file not in §6.
- A pin of §2.3 does not resolve, or §2.1's range cannot be satisfied by both ends.
- The release check fails in a way (a)–(f) do not explain.
- A statement the README must make (§2.7) is not true of the code, or cannot be checked.
- Anything would push to GitHub, make or move a tag, change the repository's settings, or start Ray;
  or would edit, run or import SecondaryGWKit, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or read any of them other than the files "Read first" item 5 names.
- A download other than §2.3's would be needed.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `pyproject.toml`; `.github/workflows/tests.yml` (new);
  `README.md`; `PROVENANCE.md`; the log, the board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It changes nothing else: no file under `runregistrykit/`, in the package or its tests; nothing
  under `docs/` but `OPEN_ISSUES.md`; not `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign
  README.
- It makes no tag, and pushes nothing.
- It writes no adoption checklist (07) and no verification document (08).

---

## 7. The log and the board

`logs/06-release-v0.1.0.md`, using README §5.1, with the additions of §4.5.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 06, §1.1's V1, and §3 and §4 as §4.5.

---

## At writing (2026-10-15, at `3372292`)

Measured read-only, for the README's row and the orchestrator; §2.2 holds the detail.
- **The wheel today** ships 19 test modules without their data; with §2.1 it has 10 entries, and a
  stale `egg-info` changes nothing (`include-package-data = false` already).
- **Both ends** pass in fresh venvs with `datastorekit` from `v0.4.0`: 276 OK in about 102 s each.
- **Without the extra**, 37 tests in two modules load and pass; the smoke of the core (imports,
  `--help`, `list` with and without a config, a `begin` and `finish`) behaves as §2.2 says.
- **The resolver** refuses `datastorekit` below `0.4.0`, a Python below the range, and `[stores]`
  with no `datastorekit` given, since the name is not on PyPI.
- **The repository** has never run a workflow; `origin/main` is behind local `main`.
- **Not measured**: Linux (the Docker daemon here was not running), and Python 3.14 or Ray 2.59.0,
  which the range admits.
- `CLAUDE.md` says "Supported versions will be stated in `pyproject.toml`"; after 06 they are. It is
  the user's file and 06 does not change it.
