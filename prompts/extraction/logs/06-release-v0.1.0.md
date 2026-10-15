# Log — prompt 06: supported versions, CI, and ready for `v0.1.0`

**Subject:** Declare the supported versions, add CI and make the package ready for v0.1.0
**Commit:** `9f8ebe4` (on `main`, after `02c7ad7`)
**Date:** 2026-10-15
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (`orchestrator-section-0.md`, corrections 1-10)
**Result:** **landed; `v0.1.0` is ready to be tagged on `9f8ebe4` once CI passes there, all three
jobs.** `pyproject.toml` says `0.1.0`, `[stores]` is `datastorekit>=0.4.0` and `runregistrykit.tests`
is excluded from the distribution; nothing else in it changed. `.github/workflows/tests.yml` is new,
with the jobs `suite (low)`, `suite (high)` and `core`, every `run:` step under `bash -eo pipefail`.
`README.md`'s Status is replaced and it gains "Supported versions", "Installing", "Using it" and
"Developing"; `PROVENANCE.md` gains 06's section. No file under `runregistrykit/` changed. The suite:
**276 -> 276** (`venv/` before and after the reinstall, and fresh low and high venvs), **37** in the
core venv. The wheel has 10 entries and passes the release check; the workflow was replayed here
step by step, all three jobs passing; (a)-(f) each fail as expected. No stop condition was met.
`[05c-the-import-test-needs-datastorekit]` is closed (U18); nothing is opened; `docs/OPEN_ISSUES.md`
is at **2**. **No tag made, nothing pushed.**

## What shipped

| File | What |
|---|---|
| `pyproject.toml` | `version = "0.1.0"`; `[stores]` `"datastorekit>=0.4.0"`; `[tool.setuptools.packages.find]` gains `exclude = ["runregistrykit.tests", "runregistrykit.tests.*"]` (U19) |
| `.github/workflows/tests.yml` | new: the `suite` matrix (`low`, `high`) and the `core` job (U13, U18) |
| `README.md` | Status replaced; "Supported versions", "Installing", "Using it" (four subsections) and "Developing" added |
| `PROVENANCE.md` | 06's section under "Since the import" |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: anything under `runregistrykit/`, anything under `docs/` but `OPEN_ISSUES.md`,
`CLAUDE.md`, `LICENSE`, `.gitignore`, the campaign README, the prompt, `orchestrator/`.

`pyproject.toml`'s diff, whole:

```diff
@@ -4,14 +4,14 @@ build-backend = "setuptools.build_meta"
 
 [project]
 name = "runregistrykit"
-version = "0.1.0.dev0"
+version = "0.1.0"
 description = "A run registry: run directories, manifests, heartbeats and datastore sidecars for long jobs"
 requires-python = ">=3.12"
 dependencies = []
 
 [project.optional-dependencies]
 stores = [
-    "datastorekit",
+    "datastorekit>=0.4.0",
 ]
 
 [tool.setuptools]
@@ -19,3 +19,4 @@ include-package-data = false
 
 [tool.setuptools.packages.find]
 include = ["runregistrykit*"]
+exclude = ["runregistrykit.tests", "runregistrykit.tests.*"]
```

### The workflow

Three jobs on `ubuntu-24.04`; triggers `push` to `main`, `pull_request`, `workflow_dispatch`;
`permissions: contents: read`; no secret, cache or artefact; `actions/checkout@v7` and
`actions/setup-python@v7` and no other action; `defaults: run: shell: bash` (correction 1).

- `suite (${{ matrix.end }})`, `fail-fast: false`, the matrix exactly `low` (3.12.15, Ray 2.43.0,
  SQLAlchemy 2.0.39) and `high` (3.13.16, 2.55.1, 2.0.46). Steps: checkout; setup-python with the
  matrix's Python; `python -m pip install --upgrade pip` then one install of
  `"datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0" -e ".[stores]"` and the two pins;
  the versions of Python, `runregistrykit`, `datastorekit`, `ray`, `sqlalchemy` and `git --version`;
  `python -m unittest discover -s runregistrykit/tests -t .`; on `low` only, `black==25.1.0` and
  `black --check runregistrykit docs`.
- `core (no store layer)`, Python 3.12.15. Steps: checkout; setup-python; `pip install --upgrade
  pip` then `pip install -e .`; a step that exits non-zero if `importlib.util.find_spec` finds any of
  `datastorekit`, `ray`, `sqlalchemy`; `python -m unittest runregistrykit.tests.test_run_registry
  runregistrykit.tests.test_public_names`; the smoke, below.

The smoke, as the step's `run:` text (extracted from the YAML by the replay script, so that it is
what GitHub runs; every check is a command whose failure exits non-zero, and the one command
expected to fail is tested with `if …; then …; exit 1; fi`):

```bash
cd "$(mktemp -d)"
out="$(mktemp)"
python -I - <<'EOF'
import sys
import runregistrykit, runregistrykit.__main__, runregistrykit.client
import runregistrykit.fingerprint, runregistrykit.stores
loaded = sorted({"datastorekit", "ray", "sqlalchemy"} & set(sys.modules))
if loaded:
    sys.exit(f"importing the package loaded {loaded}")
EOF
python -I -m runregistrykit --help > /dev/null
if python -I -m runregistrykit list > "$out" 2>&1; then
  cat "$out"; echo "list succeeded with no runregistrykit.toml"; exit 1
fi
cat "$out"
grep -q "No runregistrykit.toml" "$out"
touch runregistrykit.toml
id="$(python -I - <<'EOF'
import runregistrykit
run = runregistrykit.begin(campaign="smoke", prompt="01", slug="ci", purpose="the core job's smoke")
run.finish("done", exit_code=0)
print(run.id)
EOF
)"
python -I -m runregistrykit list > "$out"
cat "$out"
grep -F "$id" "$out" | grep -q " done "
```

Nothing in the workflow reads a client: `docs` appears only as an argument of `black --check`
(hazard 5).

### The README's new sections

- **Status** (replacing "Status: being extracted"): `v0.1.0` is SecondaryGWKit's `RunRegistry/`
  moved here and made generic (the root and settings from `runregistrykit.toml`, the store layer
  taking the client's fingerprinter); the three clients adopt it from here; `PROVENANCE.md`, the
  campaign README and the board linked. The DatastoreKit paragraph after it is unchanged.
- **Supported versions**: a table of the declared range and the low, high and core configurations;
  Ray's effective floor of 2.45.0 on Python 3.13; newer releases inside the range allowed and not
  tested (Python 3.14, Ray 2.59.0); SQLAlchemy held below 2.1 by DatastoreKit; a client pins its own
  `datastorekit`, `ray` and `sqlalchemy`.
- **Installing**: the two `requirements.txt` lines and why both; the core-only form; editable
  installs for developing only.
- **Using it**: "The client's root", "A run", "The store layer", "What the registry writes is part
  of its interface". No client is written; no client's script, store or campaign is named;
  `runregistrykit/tests/neutral_store.py` is pointed at as a worked fingerprinter, not installed.
- **Developing** (before "Licence"): the venv, the install, the suite's command, what it needs, CI's
  three jobs, and that the checks under `docs/extraction/` run locally only.

The opening paragraph, "The rules", "The public names" (with its "(it needs the extra
`[stores]`)") and "Licence" are unchanged (`git diff` of `README.md` has two hunks: one from the
Status paragraph through the new sections after the DatastoreKit paragraph, which it leaves as it
was, and one before "Licence"; the only lines removed are the old Status paragraph's five).

## Deviations from the prompt

Each classified. Corrections 1-10 are the brief's.

1. **The shell** (correction 1): `defaults: run: shell: bash` at the workflow's top, so every `run:`
   step runs as `bash --noprofile --norc -eo pipefail {0}`; every check of the core smoke is an
   explicit test (`sys.exit` with a message in Python, `grep -q` or `if …; exit 1; fi` in shell); the
   replay ran each step's extracted `run:` text with `bash --noprofile --norc -eo pipefail`.
   **STRUCTURALLY REQUIRED.**
2. **(d) and (f) in fresh throwaway venvs** (correction 2): (d) a `--dry-run` into the new, empty
   `venv-d` (3.12.15); (f) the new `venv-f`, made as the core's (`-e .`), then `datastorekit` from
   `v0.4.0` added. (b) a `--dry-run` into the low venv; (c) into the core venv. The same
   install as (d) into the existing low venv **succeeds** ("Would install 1 package",
   `runregistrykit` alone), as the brief measured. **STRUCTURALLY REQUIRED.**
3. **`pip freeze` of `venv/`** (correction 3): identical before and after the reinstall (27 lines;
   the package's line is `-e git+https://github.com/ds283/RunRegistryKit.git@02c7ad7d…#egg=runregistrykit`
   both times), and `importlib.metadata.version("runregistrykit")` went `0.1.0.dev0` -> `0.1.0`. The
   reinstall's build isolation fetched `setuptools`. **STRUCTURALLY REQUIRED.**
4. **(e) fails the core job at step 5** (correction 4): step 4 passes (`find_spec` imports nothing),
   step 5 fails on loading the two modules (`Ran 2 tests`, `FAILED (errors=2)`), and step 6, replayed
   too, fails at its first import. In the low venv every failing test is recorded: three, not one.
   **STRUCTURALLY REQUIRED.**
5. **Order** (correction 5): `pyproject.toml` was changed first, then the venvs were built, each
   with one resolve from the repository root. **STRUCTURALLY REQUIRED.**
6. **The Installing form checked by resolving it** (correction 6): against a scratch clone of this
   repository with 06's four product files committed there (`fce080c` in the clone), in the new
   throwaway `venv-install` (3.13.16). **STRUCTURALLY REQUIRED.**
7. **Ray's floor on 3.13 stated without qualification** (correction 7), and re-checked here by
   `uv pip compile --only-binary ray --python-version 3.13` (below). **IMPLEMENTATION CHOICE.**
8. **The README read from the code** (correction 8): every statement checked (90 checks, below). No
   statement the prompt's section 2.7 asks for differs from the code. **STRUCTURALLY REQUIRED.**
9. **Per-module counts** (correction 9): the same in `venv/` before and after, and in the low and
   high venvs. **STRUCTURALLY REQUIRED.**
10. **`PROVENANCE.md`'s 06 section** (correction 10): says no file under `runregistrykit/` changed,
    and names the version, range and exclusion, the three jobs and the README's sections, without
    repeating the README. **STRUCTURALLY REQUIRED.**
11. **Steps with no local counterpart.** `actions/checkout` (the checkout is this repository) and
    `actions/setup-python` (the venv's interpreter) in every job, and `python -m pip install
    --upgrade pip` in every install step (a `uv` venv has no `pip`; the line was dropped from the
    replayed script, as a comment). Every other `python -m pip install` became `uv pip install`;
    nothing else in any step changed (checked by script: the replayed files equal the YAML's `run:`
    text, with the matrix substituted, but for those lines). **STRUCTURALLY REQUIRED.**
12. **The workflow's names and the step forms**: the job names `suite (low)`, `suite (high)` and
    `core (no store layer)`, the steps' names, step 4 as a here-document under `python -I`, and the
    smoke's output kept in a `mktemp` file rather than the client root. **IMPLEMENTATION CHOICE.**
13. **Each core-smoke check shown able to fail** (n1)-(n4), beyond the prompt's (a)-(f), and (e) and
    (f) for its first and the job's step 4 (below). **IMPLEMENTATION CHOICE**, for the note's E3.
14. **(a) installed into a throwaway venv**, `venv-a` (3.13.16, the wheel with `--no-deps`), so that
    the release venv keeps the good wheel. **IMPLEMENTATION CHOICE.**
15. **(f)'s `datastorekit` install was unpinned**, as correction 2 words it, so `uv` resolved `ray`
    2.59.0 and SQLAlchemy 2.0.54 from PyPI (64.3 MiB and 2.1 MiB downloaded into `uv`'s cache), not
    the two pins already cached. PyPI packages only; the result does not depend on the versions.
    **IMPLEMENTATION CHOICE.**
16. **The README's Ray and SQLAlchemy ranges** (`>=2.43`; `>=2.0.39,<2.1`) were read from the
    installed `datastorekit`'s metadata (`importlib.metadata.requires("datastorekit")` in the low
    venv: `['ray>=2.43', 'sqlalchemy<2.1,>=2.0.39']`), not from DatastoreKit's repository.
    **IMPLEMENTATION CHOICE.**
17. **The README's layout**: "Supported versions", "Installing" and "Using it" between the
    DatastoreKit paragraph and "The rules"; "Developing" between "The public names" and "Licence";
    "Using it" in four `###` subsections; a two-line TOML block for `[stores]`; "Developing" also
    names `black` 25.1.0, which CI's low job runs. **IMPLEMENTATION CHOICE.**

## Verification performed

### 1. The venvs

All under `<scratch>` = the session scratchpad's `agent-06/`, each made with `uv venv -p <python>`
(uv 0.12.20) and one `uv pip install --python <venv>/bin/python …` from the repository root, after
`pyproject.toml` was changed:

| Venv | Command (after `uv venv -p`) | Stands for | Result |
|---|---|---|---|
| `venv-low` | `/opt/local/bin/python3.12`; `uv pip install "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0" -e ".[stores]" "ray==2.43.0" "sqlalchemy==2.0.39" "black==25.1.0"` | `suite (low)` step 3 and the black step's install | 27 installed, `datastorekit` from `c8570e8` |
| `venv-high` | `/opt/local/bin/python3.13`; the same with `"ray==2.55.1" "sqlalchemy==2.0.46"` | `suite (high)` step 3 | 25 installed |
| `venv-core` | `/opt/local/bin/python3.12`; `uv pip install -e .` | `core` step 3 | 1 installed |
| `venv-release` | `/opt/local/bin/python3.13`; `uv pip install <scratch>/dist-1/runregistrykit-0.1.0-py3-none-any.whl "datastorekit @ git+…@v0.4.0" "ray==2.55.1" "sqlalchemy==2.0.46"` (from `<scratch>`) | none: the release check | 21 installed |

Each resolve checked the pins against the new range: none was refused. Versions
(`<venv>/bin/python -I` of a script printing `sys.version` and `importlib.metadata.version`):

| Venv | `sys.version` | `runregistrykit` | `datastorekit` | `ray` | `sqlalchemy` |
|---|---|---|---|---|---|
| low | 3.12.15 (main, Oct 3 2026, 08:34:37) [Clang 21.0.0] | 0.1.0 | 0.4.0 | 2.43.0 | 2.0.39 |
| high | 3.13.16 (main, Oct 3 2026, 08:14:15) [Clang 21.0.0] | 0.1.0 | 0.4.0 | 2.55.1 | 2.0.46 |
| core | 3.12.15 | 0.1.0 | absent | absent | absent |
| release | 3.13.16 | 0.1.0 (the wheel) | 0.4.0 | 2.55.1 | 2.0.46 |
| `venv/` before / after | 3.12.15 | 0.1.0.dev0 / 0.1.0 | 0.4.0 | 2.43.0 | 2.0.39 |

`venv/`'s reinstall: `./venv/bin/python -m pip install --no-deps -e .` ("Successfully uninstalled
runregistrykit-0.1.0.dev0 … Successfully installed runregistrykit-0.1.0"). `pip freeze` before and
after: identical, 27 lines (correction 3).

### 2. The suite, five times

Each run in the foreground from the repository root, output to a file and the verdict grepped;
`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` found nothing before and after every run
(exit 1); `RAY_ADDRESS` unset.

| Where | Command | Verdict |
|---|---|---|
| `venv/`, before (at `02c7ad7`, nothing changed) | `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .` | `Ran 276 tests in 97.106s`, `OK` |
| low | `<scratch>/venv-low/bin/python -m unittest discover -s runregistrykit/tests -t .` | `Ran 276 tests in 105.508s`, `OK` |
| high | the same in `venv-high` | `Ran 276 tests in 97.440s`, `OK` |
| core | `<scratch>/venv-core/bin/python -m unittest runregistrykit.tests.test_run_registry runregistrykit.tests.test_public_names` | `Ran 37 tests in 5.375s`, `OK` |
| `venv/`, after the reinstall | as before | `Ran 276 tests in 93.689s`, `OK` |

Per module, by the loader, the same in `venv/` before and after and in low and high: test_client_root
27, test_fingerprinter 31, test_package_imports 3, test_package_is_generic 22, test_public_names 8,
test_run_registry 29, test_store_amend 21, test_store_amend_residuals 9, test_store_command_line 2,
test_store_copy_move 27, test_store_fingerprint 29, test_store_retire 41,
test_store_retire_references 10, test_store_sidecar 17 (276, no loader error). In the core venv,
discovery loads 37 tests in `test_public_names` (8) and `test_run_registry` (29) and fails to
import the other twelve modules: eleven on `datastorekit` and `test_fingerprinter` on `sqlalchemy`
(observation 1).

`git status --short --ignored` was the same after every run as before it (only this prompt's
changes and the ignored `venv/`, `runregistrykit.egg-info/`, `__pycache__/`, `prompts/.DS_Store`);
no `var/`, no `build/`, no `dist/`; this checkout the only worktree. `./venv/bin/black --check
runregistrykit docs`: "26 files would be left unchanged". `black` was not run on the workflow or the
README.

### 3. The release check

Built from a fresh export: `git archive HEAD | tar -x -C <scratch>/export-1` (a new directory), the
working tree's `pyproject.toml` copied over the export's, `uv build --wheel --out-dir <scratch>/dist-1
<scratch>/export-1` (exit 0; the build's own environment was Python 3.14, by the egg-info name in
its output).

- **Name:** `runregistrykit-0.1.0-py3-none-any.whl`
- **Size:** 54,940 bytes
- **SHA-256:** `9c01e7c99efdb5c7c3cd79660465f842dc62fe9618020825bfd871049e95f57d`
- **Entries:** 10:

  ```
  runregistrykit/__init__.py 35289
  runregistrykit/__main__.py 22237
  runregistrykit/client.py 11651
  runregistrykit/fingerprint.py 10568
  runregistrykit/stores.py 93300
  runregistrykit-0.1.0.dist-info/licenses/LICENSE 11357
  runregistrykit-0.1.0.dist-info/METADATA 304
  runregistrykit-0.1.0.dist-info/WHEEL 91
  runregistrykit-0.1.0.dist-info/top_level.txt 15
  runregistrykit-0.1.0.dist-info/RECORD 849
  ```
- **`METADATA`:** `Version: 0.1.0`, `Requires-Python: >=3.12`, `License-File: LICENSE`,
  `Provides-Extra: stores`, `Requires-Dist: datastorekit>=0.4.0; extra == "stores"`.

Installed (not editable) in `venv-release`; then, from the new empty directory
`<scratch>/empty-release`, with `env -u PYTHONPATH` and `-I`:

```
$ venv-release/bin/python -I release_check.py
sys.version 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]
cwd <scratch>/empty-release listing []
import runregistrykit -> <scratch>/venv-release/lib/python3.13/site-packages/runregistrykit/__init__.py True
import runregistrykit.client -> <scratch>/venv-release/lib/python3.13/site-packages/runregistrykit/client.py True
import runregistrykit.fingerprint -> <scratch>/venv-release/lib/python3.13/site-packages/runregistrykit/fingerprint.py True
import runregistrykit.stores -> <scratch>/venv-release/lib/python3.13/site-packages/runregistrykit/stores.py True
import runregistrykit.__main__ -> <scratch>/venv-release/lib/python3.13/site-packages/runregistrykit/__main__.py True
heavy loaded after imports: []
DatastoreKitFingerprinter <class 'runregistrykit.fingerprint.DatastoreKitFingerprinter'>
version 0.1.0
requires ['datastorekit>=0.4.0; extra == "stores"']
import runregistrykit.tests -> ModuleNotFoundError: No module named 'runregistrykit.tests'
$ venv-release/bin/python -I -m runregistrykit --help
usage: runregistrykit [-h] [--client-root DIR] {list,store} ...      (exit 0)
```

The directory was empty after. `git status` showed no `build/`, `dist/` or new `*.egg-info` in the
repository (hazard 3).

### 4. The workflow

**Parsed** with PyYAML from the low venv (`venv-low/bin/python -c "import yaml, sys;
print(yaml.safe_load(open(sys.argv[1])))" .github/workflows/tests.yml`, exit 0; `on` reads as `True`).
A script then asserted: the matrix is exactly `[{end: low, python: "3.12.15", ray: "2.43.0",
sqlalchemy: "2.0.39"}, {end: high, python: "3.13.16", ray: "2.55.1", sqlalchemy: "2.0.46"}]`;
`fail-fast` false; the core job's `python-version` `"3.12.15"`; `permissions` `{contents: read}`;
the triggers; `defaults` `{run: {shell: bash}}`; the only actions `actions/checkout@v7` and
`actions/setup-python@v7`; both jobs `ubuntu-24.04`. `actionlint` is not installed and was not.

**Replayed** by `replay.py` (in `<scratch>/scripts/`): for each step, its `run:` text extracted
from the YAML, `${{ matrix.* }}` substituted, an `if:` evaluated, written to a file and run with
`bash --noprofile --norc -eo pipefail <file>` from the repository root, with the venv's `bin/` first
on `PATH`, `VIRTUAL_ENV` the venv, `PYTHONPATH` unset and `TMPDIR` a scratch directory; a failed
step stops the job, as on GitHub. Only the install lines change (deviation 11).

| Job | Step | Local command | Result |
|---|---|---|---|
| `core` (in `venv-core`) | 1, 2 | none | no local counterpart |
| | 3 | `uv pip install -e .` | exit 0 (re-installed, `~ runregistrykit==0.1.0`) |
| | 4 | as written | exit 0, `absent: datastorekit, ray, sqlalchemy` |
| | 5 | as written | exit 0, `Ran 37 tests in 5.060s`, `OK` |
| | 6 | as written | exit 0: `list` with no config printed `!! No runregistrykit.toml in <tmp> or any directory above it. …`; then `smoke-01-ci-20261015T151339  done  -  1s  the core job's smoke` and `1 run(s) under <tmp>/var/runs: 1 finished.` |
| `suite (low)` (in `venv-low`) | 1, 2 | none | no local counterpart |
| | 3 | `uv pip install "datastorekit @ git+…@v0.4.0" -e ".[stores]" "ray==2.43.0" "sqlalchemy==2.0.39"` | exit 0 |
| | 4 | as written | exit 0: python 3.12.15, runregistrykit 0.1.0, datastorekit 0.4.0, ray 2.43.0, sqlalchemy 2.0.39, git version 2.56.0 |
| | 5 | as written | exit 0, `Ran 276 tests in 110.118s`, `OK` |
| | 6 (`black`) | `uv pip install black==25.1.0`, then as written | exit 0, `26 files would be left unchanged.` |
| `suite (high)` (in `venv-high`) | 1, 2 | none | no local counterpart |
| | 3 | as low, with `"ray==2.55.1" "sqlalchemy==2.0.46"` | exit 0 |
| | 4 | as written | exit 0: python 3.13.16, 0.1.0, 0.4.0, 2.55.1, 2.0.46, git 2.56.0 |
| | 5 | as written | exit 0, `Ran 276 tests in 98.244s`, `OK` |
| | 6 | skipped: `if: matrix.end == 'low'` is false | as on GitHub |

No Ray process before or after either suite job.

**Each check of the smoke able to fail** (deviation 13): the extracted step-6 script, changed as
below, run the same way in `venv-core`:

| # | Change | Exit |
|---|---|---|
| (n1) | `grep -q "No runregistrykit.toml"` -> `grep -q "No such text"` | 1 |
| (n2) | `grep -q " done "` -> `grep -q " failed "` (the end of the `grep -F "$id" … \| grep -q` pipeline) | 1 |
| (n3) | unchanged script, `TMPDIR` a directory below one holding `runregistrykit.toml`, so `list` finds a config | 1, `list succeeded with no runregistrykit.toml` |
| (n4) | `--help` -> `--no-such-option` | 2 |

The import check fails under (e) and step 4 under (f) (the breakage record).

### 5. The README, every name and statement

`readme_check.py` (in `<scratch>/scripts/`), run in the low venv from an empty directory with `-I`,
checks each statement of the new sections against the code: importable names by importing them,
arguments and defaults by `inspect.signature`, config keys and defaults by `find_client_root` on a
`runregistrykit.toml` written in a temporary directory, behaviour by calling it in temporary
directories (a temporary git repository and linked worktree for the worktree rule, a bare clone's
worktree for its refusal, a hand-written tombstone sidecar for `begin()`'s refusal), and commands
by running them. Its output, whole (`<tempdir>` a `tempfile` directory):

```
OK   import runregistrykit.begin  [import]
OK   import runregistrykit.list_runs  [import]
OK   import runregistrykit.Run  [import]
OK   import runregistrykit.ConfigError  [import]
OK   import runregistrykit.stores  [import]
OK   import runregistrykit.fingerprint.DatastoreKitFingerprinter  [import]
OK   import runregistrykit.fingerprint.Fingerprinter  [import]
OK   CONFIG_FILE == 'runregistrykit.toml'  [value]
OK   Run.heartbeat exists  [getattr]
OK   Run.record exists  [getattr]
OK   Run.known exists  [getattr]
OK   Run.finish exists  [getattr]
OK   Run.status exists  [getattr]
OK   Run.stdout_path exists  [getattr]
OK   Run.stderr_path exists  [getattr]
OK   Fingerprinter methods take, compare, describe, listing  [getattr]
OK   begin required = campaign, prompt, slug, purpose  [inspect.signature]
OK   begin optional = argv cwd script unit expected_units checkpoint results scope heartbeat_means pid root when client_root  [inspect.signature]
OK   begin client_root keyword-only  [inspect.signature]
OK   Run.heartbeat, units_done=None, units_total=None, pid=None, stage=None)  [inspect.signature: (self, units_done=None, units_total=None, pid=None, stage=None)]
OK   Run.record, unit, data=None)  [inspect.signature: (self, unit, data=None)]
OK   Run.finish, state, exit_code=None, *, fingerprint=False)  [inspect.signature: (self, state, exit_code=None, *, fingerprint=False)]
OK   Run(path, *, client_root=None)  [inspect.signature]
OK   list_runs takes client_root=  [inspect.signature]
OK   DatastoreKitFingerprinter(factories, fingerprint_format)  [inspect.signature]
OK   DatastoreKitFingerprinter refuses format 0  [call]
OK   DatastoreKitFingerprinter refuses format True  [call]
OK   DatastoreKitFingerprinter refuses format '1'  [call]
OK   runregistrykit.TERMINAL_STATES == done, failed, killed  [value]
OK   store-layer functions that need the root take client_root=  [inspect.signature over adopt_sidecar, amend_sidecar, copy_store, create_sidecar, fingerprint_store, move_store, read_sidecar, retire_store, runs_naming, write_listing]
OK   store-layer functions without client_root need no root (check_listing_path, new_store_id, sidecar_path)  [inspect.signature]
OK   empty config: runs_root = <root>/var/runs  [find_client_root on an empty runregistrykit.toml]
OK   empty config: stores_root = <root>/var/datastores  [same]
OK   empty config: distributions = () and stores = {}  [same]
OK   the walk finds the root from a subdirectory  [find_client_root(sub)]
OK   ConfigError naming the file: unknown key  [find_client_root on a written config]
OK   ConfigError naming the file: wrong type  [find_client_root on a written config]
OK   ConfigError naming the file: wrong shape (empty)  [find_client_root on a written config]
OK   ConfigError naming the file: wrong shape (repeated)  [find_client_root on a written config]
OK   ConfigError naming the file: [stores] other key  [find_client_root on a written config]
OK   ConfigError naming the file: fingerprinter not module:attribute  [find_client_root on a written config]
OK   absolute runs_root kept; relative stores_root under the root  [find_client_root]
OK   [stores] fingerprinter kept as written  [find_client_root]
OK   none found is a ConfigError that says what to create  [find_client_root on a directory with none above]
OK   client_root= naming a directory with no config is a ConfigError  [find_client_root(client_root=)]
OK   client_root= names the root with no walk  [find_client_root(client_root=root)]
OK   begin walks from the script's directory (working directory has no config)  [begin(script=...) from a cwd with no config]
OK   run directory <runs_root>/<campaign>-<prompt>-<slug>-<YYYYMMDDTHHMMSS>  [<tempdir>/client/var/runs/c-01-s-19700101T010000]
OK   manifest.json and status.json written; state running  [files]
OK   pid defaults to the calling process  [status.json]
OK   checkpoint=True puts the ledger inside the run directory  [Run.checkpoint_path]
OK   stdout.log / stderr.log named, not created by begin  [paths]
OK   packages records runregistrykit always  [manifest]
OK   record stamps script hash, git head and dirty flag  [record()]
OK   known() returns recorded units  [known()]
OK   a manifest is written once  [second begin, same id]
OK   begin with no config found refuses, leaving nothing  [begin from a cwd with no config]
OK   finish refuses a state not in done/failed/killed  [finish('bogus')]
OK   finish(fingerprint=True) records a failure, state still written  [finish: the manifest names no results store to fingerprint]
OK   list marks a stale run !! and exits 0  [!! c-02-stale-19700101T010010  running           -       0s  p]
OK   --client-root DIR before the command  [cli]
OK   list --root DIR needs no config  [cli]
OK   list with no config exits 1 and says No runregistrykit.toml  [cli]
OK   list newest first  [cli]
OK   store show refuses with no fingerprinter named  [cli]
OK   store create refuses with no fingerprinter named  [cli]
OK   store adopt refuses with no fingerprinter named  [cli]
OK   store copy refuses with no fingerprinter named  [cli]
OK   store move refuses with no fingerprinter named  [cli]
OK   store fingerprint refuses with no fingerprinter named  [cli]
OK   store retire refuses with no fingerprinter named  [cli]
OK   store amend refuses with no fingerprinter named  [cli]
OK   the config names an instance, not a class  [load_fingerprinter]
OK   a module of the client's own, imported with the root first on sys.path  [load_fingerprinter]
OK   a run in a linked worktree is recorded under the main checkout  [<tempdir>/main/var/runs/c-03-wt-20261015T152557]
OK   its git commit and dirty flag are the worktree's  [manifest vs git -C worktree]
OK   a worktree of a bare repository is refused  [find_client_root]
OK   begin refuses a results store whose sidecar is a tombstone  [begin(results=tombstone)]
OK   exists: PROVENANCE.md  [os.path.exists]
OK   exists: prompts/extraction/README.md  [os.path.exists]
OK   exists: prompts/extraction/IMPLEMENTATION_STATE.md  [os.path.exists]
OK   exists: runregistrykit/tests/neutral_store.py  [os.path.exists]
OK   exists: .github/workflows/tests.yml  [os.path.exists]
OK   exists: pyproject.toml  [os.path.exists]
OK   exists: runregistrykit/tests/test_run_registry.py  [os.path.exists]
OK   exists: runregistrykit/tests/test_public_names.py  [os.path.exists]
OK   exists: docs/extraction  [os.path.exists]
OK   neutral_store defines FACTORIES and FINGERPRINTER  [read]
OK   the suite command is CLAUDE.md's  [read]
OK   CLAUDE.md's pinned install form  [read]
90 of 90 checks pass
```

Checked otherwise:

| Statement | How |
|---|---|
| each command and option in "The store layer"'s list, and `list`'s `--root`, `--stale-after` (default 900) and `--client-root DIR` before the command | `python -m runregistrykit --help`, `list --help`, `store --help` and `store <command> --help` for all eight; `amend`'s one-of `--json`/`--remove` from `amend_sidecar`'s docstring (refusal 2, "both `value` and `remove`, or neither") |
| "Those that read runs take `--runs-root DIR`" | `--help`: `show`, `copy`, `move`, `fingerprint`, `retire`, `amend` have it; `create` and `adopt` have not, and neither reads runs |
| copying, moving and retiring import `datastorekit`; `DatastoreKitFingerprinter` does when it takes, compares or lists | `grep`: `from datastorekit.SQL.ShardedPool import ShardedPool` inside `copy_store`, `move_store`, `retire_store` (`stores.py:1154, 1193, 1673`); `load_fingerprinter` in `write_listing` and `fingerprint_store` (`:1266, 1349`); `fingerprint.py`'s `take`, `compare`, `listing` import inside the method |
| `retire` deletes shards then primary, keeps the sidecar, refuses a running store and a mismatched fingerprint; no command deletes a sidecar or run directory | `store retire --help`; `stores.py`'s and `__main__.py`'s docstrings |
| the declared ranges | `pyproject.toml`; installed `datastorekit`'s `Requires-Dist` (deviation 16) |
| Ray's floor on 3.13 is 2.45.0 | `uv pip compile - --python-version 3.13 --only-binary ray`: `ray==2.44.1` "has no wheels with a matching Python ABI tag (e.g., `cp313`)", the same for `x86_64-manylinux_2_28` and `aarch64-apple-darwin`; `ray==2.45.0` resolves |
| Ray 2.59.0 is the newest today | (f)'s unpinned resolve chose `ray==2.59.0` |
| the tested configurations | the workflow (section 4 above) |
| the Installing form, both lines needed | correction 6, below |
| `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0` | installed in every venv, `c8570e8` |
| the links `PROVENANCE.md`, `prompts/extraction/README.md`, `prompts/extraction/IMPLEMENTATION_STATE.md`, `runregistrykit/tests/neutral_store.py`, `.github/workflows/tests.yml` | `os.path.exists`, in the output above |
| `neutral_store.py` is not installed | the wheel's entry list (section 3) |
| the suite's command and needs | `CLAUDE.md`, "Repository mechanics"; `test_manifest_carries_the_provenance_triple` (`test_run_registry.py:276`) asserts a 40-character `git_head` for `begin(script=__file__)` |

**The Installing form** (correction 6). `git clone -q <this repository> <scratch>/clone`; the four
product files (`pyproject.toml`, `README.md`, `PROVENANCE.md`, `.github/workflows/tests.yml`) copied in
and committed there as `fce080cba40021fef9ea6676412d5f94f767dc1f`; a new throwaway venv
`venv-install` (3.13.16):

```
$ uv pip install --dry-run --python venv-install/bin/python "runregistrykit[stores] @ git+file://<scratch>/clone@fce080c…" "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0" "ray==2.55.1" "sqlalchemy==2.0.46"
Resolved 21 packages in 1.77s
Would download 1 package
Would install 21 packages
 + datastorekit==0.4.0 (from git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005)
 + ray==2.55.1
 + runregistrykit @ git+file://<scratch>/clone@fce080cba40021fef9ea6676412d5f94f767dc1f
 + sqlalchemy==2.0.46
 … (17 more)                                                            exit 0
$ … the same without the datastorekit line
error: No solution found when resolving dependencies
  cause: Because datastorekit was not found in the package registry and runregistrykit[stores]==0.1.0 depends on datastorekit>=0.4.0, we can conclude that runregistrykit[stores]==0.1.0 cannot be used.
         And because only runregistrykit[stores]==0.1.0 is available and you require runregistrykit[stores], we can conclude that your requirements are unsatisfiable.
                                                                        exit 1
$ … "runregistrykit @ git+file://<scratch>/clone@fce080c…" alone (the core form)
Would install 1 package                                                 exit 0
```

### 6. The six hazards

1. **A git work tree and `git`.** `actions/checkout` makes a work tree (fetch depth 1, which has a
   `HEAD` for `test_manifest_carries_the_provenance_triple`) and `ubuntu-24.04` has `git`. Every
   test `git` call goes through `client_fixtures.git`, which sets `GIT_CONFIG_GLOBAL=/dev/null` and
   `GIT_CONFIG_NOSYSTEM=1` and passes the identity with `-c`, so the runner needs no identity; the
   tests use `git init -b` and `git worktree add`. Nothing to change; not measured on Linux.
2. **The package installed.** Every venv here installs it (editable, but the release venv's wheel),
   and every CI job installs it editable (`-e ".[stores]"`, `-e .`). `test_package_imports` passed
   in low, high and `venv/`.
3. **A stale build.** Each wheel was built from a new export, one per build (`export-1`, `export-a`),
   never in the repository; `git status --short --ignored` shows no `build/`, `dist/` or new
   `*.egg-info` (the ignored `runregistrykit.egg-info/` is the one the editable installs rewrite,
   correction 5).
4. **Linux is not measured.** Everything above ran on macOS 27 (arm64). CI is the suite's first
   Linux run; nothing here stands in for it, which is why the tag waits.
5. **The checks cannot run in CI.** The workflow runs neither `measure_client_vocabulary.py` nor
   `compare_with_source.py`; `docs` appears in it only as `black --check`'s argument.
6. **A by-name extra.** `datastorekit` is not on PyPI ((d) and correction 6 show the refusal);
   the README's Installing says the client pins `datastorekit` itself, and why; every CI install
   names the tag.

## The deliberate-breakage record

None committed. After each, `git status --short` was this prompt's changes only (` M README.md`,
` M pyproject.toml`, `?? .github/`, and later the records), and `git diff` of `runregistrykit/`
empty. Diffs to tracked files are below, each checked in `bash` with `git apply --check`, applied,
checked with `git apply -R --check`, and reversed.

| # | Change | What failed |
|---|---|---|
| (a) | `exclude` removed from `pyproject.toml`, in the new export `export-a`, built to `dist-a` | the release check: the wheel has **29 entries, 19 under `runregistrykit/tests/`** (151,874 bytes); installed with `--no-deps` in the throwaway `venv-a` (3.13.16), `import runregistrykit.tests` **succeeds** from an empty directory with `-I` |
| (b) | the low venv's install with `datastorekit` from `v0.3.0`, `--dry-run` | refused: "Because only datastorekit<0.4.0 is available and runregistrykit[stores]==0.1.0 depends on datastorekit>=0.4.0, …", exit 1 |
| (c) | `requires-python = ">=3.13"`, applied in the repository; the core venv's install, `--dry-run` | refused: "Because the current Python version (3.12.15) does not satisfy Python>=3.13 and runregistrykit==0.1.0 depends on Python>=3.13, …", exit 1 |
| (d) | the `suite` job's install without the `datastorekit` URL, `--dry-run`, into the new empty `venv-d` (3.12.15) | refused: "Because datastorekit was not found in the package registry and runregistrykit[stores]==0.1.0 depends on datastorekit>=0.4.0, …", exit 1 (into the existing low venv it succeeds: correction 2) |
| (e) | `import datastorekit` at module scope of `runregistrykit/client.py`, applied in the repository | `core` in `venv-core`: step 4 exit 0; **step 5 exit 1** (`Ran 2 tests`, `FAILED (errors=2)`, each `ModuleNotFoundError: No module named 'datastorekit'` at `client.py:69`, through `__init__.py:74`); step 6, replayed too, **exit 1** at its first import, the same traceback. The low venv's suite: `Ran 276 tests in 106.924s`, `FAILED (failures=3)`: `test_package_imports.TestPackageImports.test_import_loads_nothing_heavy` (`['datastorekit'] != []`), `test_package_imports.TestPackageImports.test_module_scope_is_the_standard_library_and_the_package` (`runregistrykit/client.py:69 imports datastorekit at module scope, …`) and `test_package_is_generic.TestThePackageImportsNoClient.test_every_import_is_allowed` (`not known: runregistrykit/client.py:69 datastorekit`) |
| (f) | the new throwaway `venv-f` (3.12.15), made as the core's (`uv pip install -e .`), then `uv pip install "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0"` (bringing `ray` 2.59.0, SQLAlchemy 2.0.54) | `core` step 4, replayed: **exit 1**, `installed, and the core job must run without them: ['datastorekit', 'ray', 'sqlalchemy']` |

### The diffs

#### (a), in the export

```diff
diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -19,4 +19,3 @@
 
 [tool.setuptools.packages.find]
 include = ["runregistrykit*"]
-exclude = ["runregistrykit.tests", "runregistrykit.tests.*"]
```

#### (c)

```diff
diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -7,7 +7,7 @@
 name = "runregistrykit"
 version = "0.1.0"
 description = "A run registry: run directories, manifests, heartbeats and datastore sidecars for long jobs"
-requires-python = ">=3.12"
+requires-python = ">=3.13"
 dependencies = []
 
 [project.optional-dependencies]
```

#### (e)

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..a82c867 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -66,6 +66,8 @@ import subprocess
 import tomllib
 from dataclasses import dataclass
 
+import datastorekit
+
 __all__ = ["CONFIG_FILE", "ClientRoot", "ConfigError", "find_client_root"]
 
 CONFIG_FILE = "runregistrykit.toml"
```

#### (b), (d) and (f), as commands

```
(b) uv pip install --dry-run --python <scratch>/venv-low/bin/python "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.3.0" -e ".[stores]" "ray==2.43.0" "sqlalchemy==2.0.39" "black==25.1.0"
(d) uv venv -q -p /opt/local/bin/python3.12 <scratch>/venv-d
    uv pip install --dry-run --python <scratch>/venv-d/bin/python -e ".[stores]" "ray==2.43.0" "sqlalchemy==2.0.39"
(f) uv venv -q -p /opt/local/bin/python3.12 <scratch>/venv-f
    uv pip install --python <scratch>/venv-f/bin/python -e .
    uv pip install --python <scratch>/venv-f/bin/python "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0"
    replay.py .github/workflows/tests.yml core - <scratch>/venv-f <outdir> 4
```

each run from the repository root.

## Observations not acted on

1. **`test_fingerprinter` fails to import in the core venv on `sqlalchemy`**, not on `datastorekit`
   as the prompt's section 2.2 has every one of the twelve: it imports `neutral_store`, whose first
   third-party import is `sqlalchemy`. Nothing depends on which name it fails on; the core job runs
   the two modules by name.
2. **`PROVENANCE.md`'s preamble** still says the package's prose "still cite[s]" SGK until prompt
   05 rewrites it (05c's observation 3); left for 08, as 05c's log says.
3. **`CLAUDE.md`'s "Supported versions will be stated in `pyproject.toml`"** is now true in the past
   tense; the file is the user's, and 06 does not change it (the prompt's "At writing").
4. **The workflow is validated as YAML only.** `actionlint` is not installed and nothing was
   installed to get it; GitHub's reading of the expressions (`${{ matrix.* }}`, the `if:`) and of the
   here-documents is first seen when CI runs (hazard 4).
5. **`pip`'s editable reinstall in `venv/`** wrote its ephemeral wheel under the system temporary
   directory (`/private/var/folders/…/T/pip-ephem-wheel-cache-…`): `pip`'s own cache, as the brief
   allows.

Nothing is opened: no issue was found that the prompt did not already own.

## State handed to the next prompt

- `pyproject.toml` at `0.1.0`, `[stores]` `datastorekit>=0.4.0`, the tests out of the wheel; the
  wheel has 10 entries.
- `.github/workflows/tests.yml` with `suite (low)`, `suite (high)` and `core`, **never run on
  GitHub**. After this commit's review, pushing `main` is put to the user; CI must pass on this
  commit, all three jobs, before `v0.1.0` is made, annotated, on it. If CI fails, a fix prompt lands
  first (README section 5 rule 12). **No tag made; nothing pushed.**
- The README's install and usage sections, for 07's checklists to cite.
- The suite is **276**, `Ran 276 tests in 93.7s … OK` in `venv/`, per module as above; `venv/` holds
  `runregistrykit` 0.1.0, editable.
- Open issues: **2** (`[00-the-shard-fixtures-reach-into-shardedpool]`, none;
  `[00-a-refusal-matches-datastorekit-message-text]`, none), each with *Package lines (06, …)*.
