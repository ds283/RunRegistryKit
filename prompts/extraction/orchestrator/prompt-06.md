# Orchestrator — prompt 06, supported versions, CI, and ready for `v0.1.0`

Read [`../README.md`](../README.md) first: §1, §2 (05c–08), §4, §5 (rules 5, 6, 7, 10 and 12), §6.2
(U3, U13, U18, U19) and §7. The conventions are [`prompt-05c.md`](prompt-05c.md)'s and its
predecessors'; they are restated in §0 because the agent reads §0 and not this directory. Where this
note and an earlier one differ, this one is right for 06.

**You do not write code.** You may:
- run the suite, `black --check`, the release check and the workflow's steps, in venvs of your own
  in the session scratchpad;
- replay the log's breakage diffs with `git apply`, and revert them;
- clone or export this repository's tree at any commit into the session scratchpad, build wheels
  there and run them, never committing anything;
- fix small residue in a follow-up commit of your own (§4).

No client, DatastoreKit or RayPoolKit is run, imported, read or edited, beyond installing
`datastorekit` from its tag into scratch venvs and reading the two sibling workflows the prompt
names. **Nothing is pushed and no tag is made**, by the agent or by the orchestrator, without the
user's clear yes.

**The prompt:** [`06-release-v0.1.0.md`](../06-release-v0.1.0.md)
**Closes:** `[05c-the-import-test-needs-datastorekit]` (U18) · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: 05c landed (`a7d93d5`) and reviewed (`3372292`); U13, U18 and U19 taken;
  `git diff --stat 3372292 HEAD -- runregistrykit docs/extraction pyproject.toml PROVENANCE.md
  CLAUDE.md README.md .gitignore` empty; no `.github/`; the suite 276 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It changes no behaviour, and its proof is mostly outside the suite.** Three lines of
`pyproject.toml`, a new workflow, four new README sections, and the records. No file under
`runregistrykit/` moves, and the suite stays at 276. The weight of the review is on four things:
- **the package as it will be tagged**: a wheel of 10 entries, no tests, metadata `0.1.0` with the
  extra's floor, importing from `site-packages` with nothing heavy loaded (§3 checks 2, 3);
- **the workflow does what it says, and fails when it should**: three jobs, each step's checks
  real, every check of the core smoke able to fail its step (§3 checks 4, 7);
- **every statement in the README's new sections is true of the code** at the commit, checked
  against the code, not the prompt (§3 check 5);
- **the install form a client will copy resolves**, and fails without the client's own
  `datastorekit` line (§3 check 6).

**What moves on purpose:** `pyproject.toml` (§2.1's three changes only);
`.github/workflows/tests.yml` (new); `README.md` (Status replaced; Supported versions, Installing,
Using it and Developing added); `PROVENANCE.md` (06's section under "Since the import"); the log,
the board, `prompts/INDEX.md` and `docs/OPEN_ISSUES.md`. **Nothing** under `runregistrykit/`,
nothing under `docs/` but `OPEN_ISSUES.md`, not `CLAUDE.md`, `LICENSE`, `.gitignore`, the campaign
README, the prompt or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **GitHub's default shell does not fail a pipeline.** A `run:` step with no `shell:` runs as
   `bash -e {0}`: `-e` but not `-o pipefail`, so `python … | tee out.txt` succeeds when `python`
   fails. With `shell: bash` the step runs as `bash --noprofile --norc -eo pipefail {0}`. Give every
   multi-line `run:` step `shell: bash` (simplest: `defaults: run: shell: bash` at the top of the
   workflow), or begin the step with `set -euo pipefail`, and make every check of the core smoke an
   explicit test whose failure exits non-zero (an `assert` in Python, an `if …; then exit 1; fi` or
   a `grep -q` in shell); a command expected to fail is tested with `if cmd; then …; exit 1; fi`, so
   that `-e` does not stop the step on the expected failure. **Replay each step as GitHub will run
   it**: its `run:` text, extracted from the YAML by a script (not retyped), written to a file and
   run with `bash --noprofile --norc -eo pipefail <file>` (or `bash -e <file>` if the step has no
   `shell: bash`), with the venv's `bin/` first on `PATH` and `pip` replaced by `uv pip` only where
   the step installs. The orchestrator's trial of a smoke written this way, in a 3.12.15 venv holding
   only the package: the five modules import with none of the three loaded, `--help` exits 0, `list`
   with no config exits 1 and says `No runregistrykit.toml`, and after `touch runregistrykit.toml`,
   `begin(campaign="smoke", prompt="01", slug="ci", purpose=…)` and `finish("done", exit_code=0)`,
   `list` exits 0 and shows the run `done`.
2. **Breakage (d) and (f) need fresh venvs.** An install without the `datastorekit` URL into the
   existing low venv **succeeds**, because `datastorekit` 0.4.0 is already installed there and
   satisfies the floor (measured: `uv pip install --dry-run -e ".[stores]" "ray==2.43.0"
   "sqlalchemy==2.0.39"` into the low venv: "Would install 1 package", `runregistrykit` alone). Into
   a new, empty 3.12 venv it refuses: "Because datastorekit was not found in the package registry
   and runregistrykit[stores]==0.1.0 depends on datastorekit>=0.4.0 …". So:
   - **(d)** is a `--dry-run` into a new, empty throwaway venv;
   - **(f)** is a new throwaway venv made exactly as the core's (`-e .`), then `datastorekit` from
     `v0.4.0` added (it brings `ray` and `sqlalchemy`; `uv`'s cache already holds them), and the
     core job's step 4 run in it. **Not a copy of the core venv**: a copied venv's scripts and
     `.pth` files point at the original.
   - (b) refuses even in the existing low venv, since it names `v0.3.0` explicitly (measured); a
     `--dry-run` there is enough. (c) is a `--dry-run` into the core venv.
   Throwaway venvs live in the agent's scratch directory and are named in the log.
3. **`pip freeze` of `venv/` does not show the version.** `venv/` holds `runregistrykit` as an
   editable install from this checkout, and its freeze line is `-e
   git+https://github.com/ds283/RunRegistryKit.git@<HEAD>#egg=runregistrykit`: the commit, not the
   version. Measured in a throwaway venv with `pip` 26: the line is byte-identical before and after
   `pip install --no-deps -e .` across the version change, while `importlib.metadata.version
   ("runregistrykit")` goes `0.1.0.dev0` → `0.1.0`. So the record is `pip freeze` before and after
   (expected **identical**, which is what "only `runregistrykit`'s line changes" protects: nothing
   else moves), **and** `importlib.metadata.version` before (`0.1.0.dev0`) and after (`0.1.0`). The
   reinstall's build isolation fetches `setuptools` from PyPI; that is a PyPI download and allowed.
4. **Breakage (e) fails the core job at step 5, not step 6.** `runregistrykit/__init__.py:74`
   imports `.client` at module scope, so with `import datastorekit` in `client.py` the core job's
   step 5 fails on loading `test_run_registry` and `test_public_names` (step 4 passes: `find_spec`
   imports nothing). A job stops at its first failed step; replay step 6 as well, to show that it
   fails at its first import too, and record both. In the low venv, record **every** test that
   fails, not only `test_package_imports`' (the guard's import rule is expected to fail as well).
5. **Order.** Change `pyproject.toml` first, then build the venvs, so that each venv's one resolve
   checks §2.3's pins against §2.1's range. The low, high and core venvs install from the
   repository root (`-e`), as §2.3 says; that rewrites the ignored `runregistrykit.egg-info/`, and
   nothing else in the tree.
6. **The README's Installing form is checked by resolving it.** The tag does not exist, so the
   form cannot be installed as written. Check it against a **scratch clone** of this repository
   with 06's change committed there (never a commit in this checkout before the one commit): in a
   new throwaway 3.13 venv, `uv pip install --dry-run "runregistrykit[stores] @
   git+file://<clone>@<sha>" "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0"
   "ray==2.55.1" "sqlalchemy==2.0.46"` resolves, and the same without the `datastorekit` line
   refuses. Record both. The orchestrator repeats this against the agent's commit itself.
7. **Facts the README may state without qualification.** On Python 3.13 Ray's floor is in effect
   2.45.0 **on every platform**: PyPI has `cp313` wheels first in `ray` 2.45.0 (macOS x86_64 and
   arm64, manylinux2014 x86_64 and aarch64), none in 2.43.0, 2.44.0 or 2.44.1. The two ends' Ray
   wheels exist for the CI runner: `ray-2.43.0-cp312-cp312-manylinux2014_x86_64.whl` and
   `ray-2.55.1-cp313-cp313-manylinux2014_x86_64.whl`.
8. **The README's statements are read from the code at the commit.** Where the prompt's §2.7
   describes the code (the config keys and defaults, the walk, `client_root=`, the worktree rule,
   `begin()`'s arguments, `Run`'s methods, the `store` commands), the code governs; a mismatch
   with the prompt is recorded, and a statement the README must make that the code does not bear
   out is a stop (§5). Each name is checked as §3.5 says, in the low venv, and listed in the log.
9. **The suite's per-module counts** (by the loader, unchanged since 05c): `test_client_root` 27,
   `test_fingerprinter` 31, `test_package_imports` 3, `test_package_is_generic` 22,
   `test_public_names` 8, `test_run_registry` 29, `test_store_amend` 21,
   `test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
   `test_store_fingerprint` 29, `test_store_retire` 41, `test_store_retire_references` 10,
   `test_store_sidecar` 17. Every count the same after, in every full-suite venv.
10. **`PROVENANCE.md`'s 06 section** says that no file under `runregistrykit/` changed, and names
    the version, range and exclusion, the workflow's three jobs, and the README's sections. It
    does not repeat the README.

**The facts, checked by the orchestrator on 2026-10-15 at `dbefdb2`.** Pass them on.
- **In-repository state.** `main` at `dbefdb2`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`, no
  `.github/`. The gate's diff from `3372292` is empty. `venv/`: Python 3.12.15, `pip` 26.2.1,
  `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit` at `c8570e8` (`v0.4.0`),
  `runregistrykit` editable, `importlib.metadata.version` `0.1.0.dev0`.
- **Tools.** `uv` 0.12.20 at `/opt/local/bin/uv`; `/opt/local/bin/python3.12` (3.12.15) and
  `python3.13` (3.13.16). `actionlint` is not installed; nothing is installed to get it.
- **The trial, in a `git clone` of `dbefdb2` in the scratchpad with §2.1's `pyproject.toml`
  applied** (a work tree, as a CI checkout is):
  - venvs made by §2.3's commands: low 3.12.15 / `runregistrykit` 0.1.0 / `datastorekit` 0.4.0 /
    `ray` 2.43.0 / SQLAlchemy 2.0.39; high 3.13.16 / 0.1.0 / 0.4.0 / 2.55.1 / 2.0.46; core 3.12.15 /
    0.1.0 and none of the three;
  - the suite: low `Ran 276 tests in 106.2s`, OK; high `Ran 276 tests in 106.2s`, OK (run side by
    side); no Ray process after;
  - the core: `python -m unittest runregistrykit.tests.test_run_registry
    runregistrykit.tests.test_public_names`, `Ran 37 tests`, OK; `find_spec` finds none of the
    three; the smoke as correction 1;
  - the wheel, from a `git archive` export with that `pyproject.toml`:
    `runregistrykit-0.1.0-py3-none-any.whl`, 54,940 bytes, 10 entries (the five modules,
    `dist-info/licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt`, `RECORD`); `METADATA` has
    `Version: 0.1.0`, `Requires-Python: >=3.12`, `Provides-Extra: stores`, `Requires-Dist:
    datastorekit>=0.4.0; extra == "stores"`;
  - the release check, that wheel in a 3.13.16 venv with `datastorekit` `v0.4.0`, `ray` 2.55.1,
    SQLAlchemy 2.0.46, from an empty directory with `-I` and `PYTHONPATH` unset: the five modules
    from `site-packages`; none of the three in `sys.modules`; `DatastoreKitFingerprinter` imports;
    version `0.1.0`, `requires` `['datastorekit>=0.4.0; extra == "stores"']`; `import
    runregistrykit.tests` raises `ModuleNotFoundError`; `-m runregistrykit --help` exits 0;
  - the resolver: (b) refuses naming `datastorekit>=0.4.0`; (d) as correction 2.
  - An **editable** install with the exclusion still imports `runregistrykit.tests` (setuptools'
    editable finder maps the top-level package to its directory), so the suite and
    `test_package_imports`' children are unaffected by U19; only the wheel drops the tests.
- **GitHub.** `ds283/RunRegistryKit` public, default branch `main`, **0 workflow runs**;
  `origin/main` at `dfcb884`. `actions/checkout` latest `v7.0.1`, `actions/setup-python` latest
  `v7.0.0`, each with a `v7` tag. `actions/python-versions`' manifest has
  `python-3.12.15-linux-24.04-x64` and `python-3.13.16-linux-24.04-x64`. DatastoreKit's and
  RayPoolKit's workflows have no `shell:` and no `defaults:`, and their steps have no pipeline whose
  failure matters; 06's smoke does (correction 1).
- **The index.** **3** open now; **2** after (`[05c-the-import-test-needs-datastorekit]` closed),
  unless the work opens another.
- **Ray.** No Ray process; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** Only §0's list changes; nothing under `runregistrykit/`.
- **(E2) The package as it will be tagged.** `pyproject.toml` as §2.1; the wheel of 10 entries with
  that metadata; the release check.
- **(E3) The workflow.** As §2.5, with correction 1; it parses; all three jobs replayed as GitHub
  runs them; every core-smoke check able to fail.
- **(E4) The README.** Status replaced, four sections added, nothing else changed; every name,
  argument, default, command and link true at the commit; the Installing form resolves.
- **(E5) The suite.** 276 in `venv/` before and after the reinstall, in low and high; 37 in core;
  per module as correction 9; no Ray; nothing outside `tempfile` directories.
- **(E6) The breakage.** (a)–(f) as the prompt and corrections 2 and 4 say.
- **(E7) The records.** The log, the board (V1, the issue closed, the two others' package lines,
  "ready to tag once CI passes"), the index (2), `prompts/INDEX.md`, `PROVENANCE.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff, the commands
  and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in each venv. Write the output to a
  file in the scratchpad and grep the verdict from it. Run it **in the foreground**, within the
  turn; each run takes about 100 s.
- **Breakage diffs** are recorded so that `git apply` replays them from a clean tree at the agent's
  commit. Check each **as recorded in the log** with `git apply --check` and `-R --check`, in
  `bash`, not zsh. None is committed. After each, `git status` must be clean. A breakage that is a
  command (an install, a dry-run) is recorded as the exact command and its output.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-06/`), never
  `/tmp`; its venvs, exports, wheels, clones and scripts live there. Python's `tempfile` and the
  smoke's `mktemp -d` are fine. **No scratch file goes under `runregistrykit/` or `docs/`**, and no
  build is made in the repository (hazard 3).
- **No client is read.** No SGK, ChamPBH, StochasticInstantons, DatastoreKit or RayPoolKit file is
  read, run or imported, beyond the prompt's "Read first" item 5 and `datastorekit` installed from
  its tag.
- **Installs and network.** Only §2.3's venvs and corrections 2 and 6's throwaway venvs, from PyPI
  and DatastoreKit's tag; `uv`'s and `pip`'s own caches are where they are. `venv/` gets only the
  `--no-deps -e .` reinstall. Nothing else is downloaded or installed.
- **GitHub.** Nothing is pushed, no tag is made, no repository setting changes, no workflow is
  dispatched. Read-only `gh api` calls are fine.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A test that fails at one end is a stop, never a changed test; a
  README statement the code does not bear out is a stop, never a softened statement that hides it.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` or `.github/` at the
   root.
2. **The prompt's gate:** the diff from `3372292` empty; the suite 276 in `venv/`.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 3 now, 2 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, 05c's log, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `README.md` and `PROVENANCE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/06-release-v0.1.0.md`, in README §5.1's form, with
  the prompt's §4.5 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It reads, runs and edits no client repository, DatastoreKit or RayPoolKit**, beyond what §0
  allows.
- **It installs only what §0 allows, and starts no Ray.**
- **It pushes nothing, makes no tag and dispatches no workflow.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list. `git diff 3372292 <commit> --
   runregistrykit docs/extraction CLAUDE.md LICENSE .gitignore prompts/extraction/README.md
   prompts/extraction/06-release-v0.1.0.md prompts/extraction/orchestrator` is empty; under `docs/`
   only `OPEN_ISSUES.md` changes. `git ls-files runregistrykit` is the same 26.
2. **E2, `pyproject.toml`.** Its diff is §2.1's three changes and nothing else.
3. **E2, the wheel, independently.** From a `git archive` export of the commit (no file copied
   over), `uv build --wheel` in the scratchpad: 10 entries, the metadata as §0's facts. Installed
   into the orchestrator's release venv (reinstalled), from an empty directory with `-I`: §2.2's
   release-check list, item by item.
4. **E3, the workflow.** By reading: triggers, `contents: read`, no secrets, cache or other action;
   the matrix exactly §2.3's low and high; the core job on 3.12.15; `shell: bash` or `set -euo
   pipefail` where a pipeline or a sequence of checks matters; the install naming the tag; black
   on low only; nothing reading a client. It parses with PyYAML. Then **replayed by the
   orchestrator**: each step's `run:` extracted from the YAML by a script and run as GitHub would
   (correction 1) — the suite steps in a fresh `git clone` of the commit with the orchestrator's
   low and high venvs (both 276 OK, side by side), and the core job's steps 3–6 in a fresh core venv
   made from that clone. Then the smoke made to fail, once per check, by a change of the
   orchestrator's own in a throwaway copy of the step's script (a check inverted, or the condition
   it tests made false): every check fails the step.
5. **E4, the README, by reading and checking.** `git diff 3372292 <commit> -- README.md`: the
   opening paragraph, the DatastoreKit paragraph, "The rules", "The public names" and "Licence"
   byte-identical; Status replaced; the four new sections in §2.7's order. Each statement checked
   by the orchestrator against the code at the commit, not against the log: every importable name
   imported in the low venv, every argument and default against `inspect.signature`, every
   command and option against its `--help`, every config key and default by writing a
   `runregistrykit.toml` in a temporary directory and reading it with `runregistrykit.client`'s
   reader, every link and path found. No client's script, store or campaign named. The log's list
   of names compared with the orchestrator's: any name in the README missing from the log's list is
   residue if true, a finding if false.
6. **E4, the install form.** In a new throwaway 3.13 venv: `uv pip install --dry-run
   "runregistrykit[stores] @ git+file:///Users/ds283/Documents/Code/RunRegistryKit@<commit>"
   "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0" "ray==2.55.1"
   "sqlalchemy==2.0.46"` resolves; without the `datastorekit` line it refuses; `runregistrykit @
   git+file://…@<commit>` alone (the core form) resolves with no `datastorekit`.
7. **E6, the breakage.** Replay (a), (c) and (e) from the log's diffs, one at a time, in `bash`
   (`--check`, apply, the failure, `-R --check`, reverse); each fails as the log says; the tree
   clean after each. (b) and (d) as the log's commands, (d) in a fresh venv; (f) in a fresh venv as
   correction 2. Then the orchestrator's own:
   - (o1) `--upgrade pip` and the install merged so that the `datastorekit` URL is dropped from the
     suite job's install, in a throwaway copy of the workflow, replayed into a fresh venv: the
     install step fails;
   - (o2) the core job's step 5 changed to discovery (`discover -s runregistrykit/tests -t .`) in
     the core venv: it fails, which is why U18 runs the two modules by name;
   - (o3) the `exclude` widened to `runregistrykit*` by mistake: the wheel has no modules, and the
     release check fails at the first import.
   An uncaught breakage is opened on the board (owner to be put to the user), not a stop.
8. **E5, the suite.** In `venv/` at the commit: `Ran 276 tests … OK`, per module as correction 9,
   the time recorded; `importlib.metadata.version("runregistrykit")` is `0.1.0`. `git status
   --short --ignored` the same before and after but for `__pycache__/`; no `var/`, `build/`,
   `dist/` or `.github/` other than the workflow; this checkout the only worktree; no Ray process
   before or after. `./venv/bin/black --check runregistrykit docs`: 26 files unchanged.
9. **E7, the records.**
   - The log has every section of README §5.1 and the prompt's §4.5 additions: each venv's
     versions and each suite's verdict and time; every install command as run, with the workflow
     step it stands for; the release check with the wheel's name, size, entry count, SHA-256, file
     list and each command's output; every README name with how it was checked; the six hazards;
     (a)–(f), as diffs or commands with their failures; `pip freeze` of `venv/` before and after,
     and the version before and after (correction 3); the deviations classified (corrections 1–10
     among them).
   - The board: the header, with the line that `v0.1.0` is ready to be tagged on 06's commit once
     CI passes there, all three jobs, and that no tag is made; 06's row (landed, "this commit",
     276 → 276); V1 ✅; `[05c-the-import-test-needs-datastorekit]` moved to §4 with this commit and
     U18's reasoning; the two others with *Package lines (06, …)*, saying CI pins `datastorekit` at
     `v0.4.0` at both ends, both still open, owner none; §3's opening count sentence.
     `docs/OPEN_ISSUES.md`: the row deleted, **2** by counting, the date. `prompts/INDEX.md`'s row
     says 06 landed. `PROVENANCE.md`: 06's section, after 05c's, nothing above it changed.
10. **The interface and the handover.** No record changes form: no package module changed. The
    log's "State handed to the next prompt" says that `v0.1.0` waits on a push and a green CI on
    06's commit, that nothing was pushed or tagged, the suite count, the open issues (2), and that
    07 measures against the tag.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 06* paragraph, in the form of
  05c's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md` and in
    `PROVENANCE.md`;
  - "reviewed" for 06 in the board's header and row, README §2's status column and its header,
    and `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 06".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **The release sequence**, which is the user's (README §5 rule 12, prompt 06 §1):
  1. push `main` (the user's yes first);
  2. CI on the pushed head: all three jobs green. **The tag goes on 06's commit**, and CI must be
     green there. A push carries the review's follow-up commit too, and GitHub runs the workflow on
     the pushed head only (`workflow_dispatch` too runs on a branch head, not on a chosen commit).
     The follow-up touches only `prompts/`, so the head's tree under `runregistrykit/`,
     `pyproject.toml`, `README.md` and the workflow equals 06's commit; but the rule names the
     commit. **Recommended:** push up to 06's commit alone first (`git push origin <06>:main`, a
     fast-forward from `dfcb884`), let CI run on it, then push the follow-up;
  3. if CI fails, a fix prompt lands first; no tag on a red commit;
  4. the annotated tag `v0.1.0` on 06's commit, pushed, by the user or on the user's instruction.
- **Report to the user:**
  - what landed, and the count, 276 → 276;
  - `pyproject.toml`'s three changes, the wheel's 10 entries, and the release check;
  - the workflow's three jobs and the shell correction;
  - the README's new sections, and that every statement was checked against the code;
  - the install form a client copies, and why it has two lines;
  - the breakage, the agent's and the orchestrator's;
  - the issue closed, and the index at 2;
  - and the release sequence above, asking whether to push 06's commit.
