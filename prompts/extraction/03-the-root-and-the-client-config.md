# Prompt 03 — the root and the client config

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 02 has landed (`8155445`) and been reviewed (`71f59ed`, the board's §1). `git diff --stat 8155445
  HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` is empty.
- U5 and U9 are taken (README §6.2, 2026-10-14), as recommended.
- The suite is `Ran 108 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[00-the-root-is-the-packages-parent]`, `[00-the-recorded-distributions-are-sgks]`.
**Opens:** only what the work finds. **Narrows:** nothing planned.

**Recommended model:** **Opus**. This is the first prompt that changes the package's behaviour, and
it changes how every public function finds where it is: the root is threaded through the core, the
store layer and the command line, and the tests' fixtures change under it without their bodies
changing.

**Read first:**

1. [`README.md`](README.md): §0.2 (C1–C5, C9; the clients), §4 (the equivalence check's
   retirement), §5 (all of it; rules 6, 7, 9 and 10 especially), §6.1 (Q2, Q3) and §6.2 (U5, U9).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §1's reviews of 01 and 02, and §3's issues,
   the two this prompt closes above all.
3. [`logs/02-port-the-core-and-shard-fixture-tests.md`](logs/02-port-the-core-and-shard-fixture-tests.md),
   "State handed to the next prompt".
4. `runregistrykit/__init__.py` in full; `runregistrykit/stores.py` at every line §2.5 names;
   `runregistrykit/__main__.py` `:29` and `:366-480`; `runregistrykit/tests/test_run_registry.py`
   `:1-140`, `store_fixtures.py:112-125`, `test_store_command_line.py:1-80, 160-183`,
   `test_package_imports.py` in full.
5. `PROVENANCE.md` and `docs/extraction/compare_with_source.py`'s docstring.
6. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers below are the package's at `8155445`.

---

## 1. What is wanted

The package stops deciding where it lives from where it is installed. A client marks its root with
a config file, **`runregistrykit.toml`**; the package finds that root by walking up from where a
run starts, records a run launched from a git worktree under the main checkout, and takes the runs
root, the stores root and the recorded distributions from the config. `REPO_ROOT`, `DEFAULT_ROOT`,
`DEFAULT_STORES_ROOT` and `RECORDED_DISTRIBUTIONS` go. **No config found is a refusal, never a
fallback.** Every path already written in a record, relative to the client's root, reads as it did
(C4). `runregistrykit` itself is always recorded in a manifest's `packages` (U9).

The ported tests keep their names and what they assert; their fixtures build a client root of
their own in a `tempfile` directory and run inside it. New tests cover the config, the walk, the
worktree rule and U9 with temporary git repositories and worktrees.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15 (`tomllib` is in the standard library), `black` 25.1.0, `ray` 2.43.0,
`datastorekit` `v0.4.0`, `runregistrykit` editable. **Install nothing.** `git` 2.56.0 is on `PATH`;
§2.3 uses `rev-parse --path-format=absolute` (git ≥ 2.31).

### 2.2 The config file (U5)

`runregistrykit.toml` at the client's root, read with `tomllib`. Its keys, all optional:

| Key | Type | Default | Meaning |
|---|---|---|---|
| `runs_root` | non-empty string | `"var/runs"` | where run directories are made |
| `stores_root` | non-empty string | `"var/datastores"` | where `store retire` looks for sidecars that reference a store |
| `distributions` | list of non-empty strings, no duplicates | `[]` | what a manifest's `packages` records, besides `runregistrykit` (§2.6) |
| `[stores]` | table | `{}` | reserved for 04's fingerprinter key; 03 requires only that it be a table, and keeps it unread |

- A relative `runs_root` or `stores_root` is joined to the **record root** (§2.4) and normalised
  with `os.path.normpath`; an absolute one is kept as it is. No `~` expansion, no environment
  variables.
- An empty file takes every default.
- **Every refusal is a `ConfigError`**, naming the file: a file that is not valid TOML (with
  `tomllib`'s message), cannot be read, has a key not in the table above (named), or a value of the
  wrong type or shape (named, with the value).
- The file's form is documented in the new module's docstring (§2.3), which is where README §4 says
  it is documented.

### 2.3 Finding the root

A new module, **`runregistrykit/client.py`**, standard library only, imported by `__init__.py` at
module scope and re-exporting:

- `CONFIG_FILE = "runregistrykit.toml"`;
- `class ConfigError(RuntimeError)`;
- `@dataclass(frozen=True) class ClientRoot`, with `root` (the record root, §2.4), `found` (the
  directory whose `runregistrykit.toml` governs), `config_file`, `runs_root`, `stores_root` (both
  absolute), `distributions` (a tuple) and `stores` (the `[stores]` table, a dict);
- `find_client_root(start=None, client_root=None) -> ClientRoot`.

**The start directory** of a call is: for `begin()`, the directory of `script` when one is given,
and otherwise the working directory; for every other call, the working directory. (`begin()`'s
`cwd` argument is what the manifest records, as now; it does not move the start.)

**The walk.** From `os.path.abspath(start)`, through each parent up to the filesystem root, the
first directory holding a **file** named `runregistrykit.toml` is `found`. It stops nowhere else:
not at a git top level, not at the home directory. None found is a `ConfigError` that names the
start directory and says what to create: "No runregistrykit.toml in <start> or any directory above
it. Create one at the client's root; an empty file takes the defaults (runs_root = "var/runs",
stores_root = "var/datastores", distributions = [])."

**The override** (U5's "explicit root"). `client_root=` on every public function of §2.5, and
`--client-root DIR` on the command line, name `found` directly: no walk, and a directory without
`runregistrykit.toml` is a `ConfigError`. The override is spelled `client_root`, not `root`,
because `begin(root=…)`, `list_runs(root=…)` and `list --root` already name the **runs root**, and
keep doing so (SGK's `sigterm_handler_probe.py:159` passes `root=` a temporary runs root). A
`ClientRoot` already found may be passed as `client_root` and is used as it is.

**Nothing happens at import.** `import runregistrykit` reads no config and runs no `git`.

### 2.4 The record root and provenance (Q3)

**The record root.** A run launched from a git worktree is recorded under the main checkout:
1. Run `git -C <found> rev-parse --path-format=absolute --git-dir --git-common-dir
   --show-toplevel`. If it fails (not a repository, no `git`), `root = found`.
2. If `realpath(git-dir) == realpath(git-common-dir)`, `found` is in a main checkout (or a
   submodule): `root = found`, **unchanged, as `abspath` gave it**. This is the common case, and no
   path printed by `git` enters the root, so `_repo_path` relativises exactly as it did.
3. Otherwise `found` is in a linked worktree. If the common dir's base name is not `.git` (a bare
   repository's worktree), that is a `ConfigError`: there is no main checkout to record into. Else
   `root = normpath(join(dirname(common-dir), relpath(realpath(found), realpath(toplevel))))`, so
   that a config in a subdirectory of the worktree maps to the same subdirectory of the main
   checkout.

Measured at writing: for a linked worktree `git` prints `<main>/.git/worktrees/<name>` and
`<main>/.git`; in a `tempfile` directory on macOS it prints `/private/var/…` where `tempfile`
gives `/var/…`. So step 3 compares realpaths, and **the tests build their temporary directories
with `os.path.realpath`**.

The config that governs is `found`'s, even when `root` is the main checkout: it is the tree that is
running. The main checkout need not hold one. `runs_root` and `stores_root` are joined to `root`.

**Provenance is the start directory's.** `git_provenance(cwd)` takes its directory as a required
argument (no default), and every call passes the start directory of the public call it serves. So a
run's `git_head`, `git_dirty` and `script_sha256` are its own tree's (Q3), and a store operation's
history entry records the tree it was run from. Measured at `a45aefc`, SGK takes provenance at
`REPO_ROOT`, the package's own directory, which installed would be the venv's.

**Paths in records (C4)** stay relative to the record root where they lie under it, and absolute
otherwise. `_repo_path(path, root)` and `_resolve(path, root)` keep their names and their meaning
and take the root explicitly; `abspath`, not `realpath`, as now. A script in a worktree outside the
main checkout is recorded by its absolute path; one in a worktree nested in it (for example under
`.claude/worktrees/`) by its path relative to the main checkout.

### 2.5 Threading the root through the package

**Every public function that needs the root takes a keyword-only `client_root=None`**, and when it
is `None` calls `find_client_root(start=<its start directory>)`. It locates **at most once**, and
passes the `ClientRoot` to everything it calls. Private helpers take the `ClientRoot` (or its
`root`) as an argument and never locate. A function locates exactly when it needs the root: to
supply a default it was not given, to write or resolve a path relative to the root, or to take
provenance.

- **`__init__.py`.** Delete `REPO_ROOT` (`:57`), `DEFAULT_ROOT` (`:58`) and
  `RECORDED_DISTRIBUTIONS` (`:119`, with its comment `:115-118`). `git_provenance(cwd)` (`:98`)
  loses its default. `package_provenance(names)` (`:122`) loses its default; its behaviour is
  otherwise unchanged. `_repo_path` and `_resolve` (`:176-185`) take `root`.
  - `begin()` (`:542-660`): locates first, before reading the results sidecar or making any
    directory, so a refusal leaves nothing behind; the runs root is `root` if given, else the
    config's `runs_root`; `_repo_path` against the record root; provenance from the start
    directory; `packages` as §2.6; `read_sidecar(results, client_root=…)`. The run it returns
    carries its `ClientRoot`.
  - `Run(path, client_root=None)`: the client root is located **lazily**, from the working
    directory, the first time something needs it (`checkpoint_path`, `results_path`,
    `finish(fingerprint=True)`), so that `status()`, `heartbeat()` and the lister's reads need
    none. `_fingerprint_results` passes it to `read_sidecar` and `fingerprint_store`.
  - `list_runs(root=None, …)`: locates only when `root` is `None`, and then lists the config's
    `runs_root`. An explicit `root` needs no config.
- **`stores.py`.** Remove `DEFAULT_ROOT`, `REPO_ROOT` from the import (`:129-140`); delete
  `DEFAULT_STORES_ROOT` (`:185`). The public functions that gain `client_root=None`:
  `read_sidecar` (its tombstone check resolves listed files, `_present` `:514-522`),
  `create_sidecar` (`:797`), `adopt_sidecar` (`:839`), `runs_naming` (`:902`), `copy_store`
  (`:1070`), `move_store` (`:1109`), `fingerprint_store` (`:1445`), `retire_store` (`:1699`) and
  `amend_sidecar` (`:2052`). Every `_repo_path`, `_resolve`, `git_provenance()`, `DEFAULT_ROOT` and
  `DEFAULT_STORES_ROOT` use (the board's issue lists them, `:833, 893, 911, 919, 940, 1098, 1101,
  1140, 1499, 1596, 1648, 1666-1673, 1741-1742, 1841, 1869, 1921, 1950, 1990, 2013, 2164`, and
  `_history_entry` `:774-776`) takes the located root, runs root or stores root instead. Layer C,
  `FINGERPRINT_FORMAT` and the `from config.datastore import factories` at `:1494` are 04's and are
  not touched.
- **`__main__.py`.** A top-level `--client-root DIR` option. `list --root`, every `--runs-root` and
  `--stores-root` default to `None`, meaning the config's; their help says so instead of printing a
  path computed at import (`:376, 388-390, 452-455`). The CLI locates when a command needs the root
  (every `store` command; `list` without `--root`), from `--client-root` or the working directory,
  and passes the `ClientRoot` down. A `ConfigError` is printed to stderr as `!! <message>` and the
  command exits 1, writing nothing. **`--help` needs no config**: nothing is located while the
  parser is built. `list` prints the runs root it used, as now.

No record changes form: the manifest, `status.json`, `checkpoint.jsonl` and the sidecar carry the
same fields as at `8155445`, and only `packages`' content changes (§2.6; README §5 rule 7).

### 2.6 The recorded distributions (U9)

A manifest's `packages` is `package_provenance(names)` for `("runregistrykit",)` followed by the
config's `distributions`, with `runregistrykit` not repeated if the config lists it. The key order
does not matter (`write_json_atomic` sorts keys). With an empty config, `packages` holds
`runregistrykit` alone.

### 2.7 The ported tests: fixtures, and the changes allowed

README §5 rule 9 holds: every ported test keeps its module, class and method name and what it
asserts, except where this section says. The classes of change, each instance listed in the log:

- **F-client, the fixture builds a client root.** `RegistryTestCase.setUp`
  (`test_run_registry.py:116`) and `StoreTestCase.setUp` (`store_fixtures.py:117`, which does not
  call the former) each make, through one shared helper, a client root in **a `tempfile` directory
  of its own** (realpath'd): a `runregistrykit.toml` (empty), a `.gitignore` holding `var/`, and a
  git repository with one commit of those two files; then `os.chdir` into it, with
  `addCleanup(os.chdir, <previous>)`. `self.client` holds its path. Everything else stays where it
  was: `self.root` (the runs root) and `self.top` (the stores) are **outside** the client root, so
  every path a ported test records keeps the absolute form it had at `8155445`. `RegistryTestCase.begin`
  passes `client_root=self.client` (its tests pass `script=__file__`, whose walk would start in
  this repository, which has no config). The fixture's `git` runs with
  `GIT_CONFIG_GLOBAL=os.devnull`, `GIT_CONFIG_NOSYSTEM=1` and `-c user.name=… -c user.email=…`, so
  that no user's signing or hooks reach it. The helper lives in a new module,
  `runregistrykit/tests/client_fixtures.py`.
- **R-root, an implicit root made explicit.** A test-body call to `runregistrykit._repo_path(p)`
  (12 lines: `store_fixtures.py:181`; `test_store_amend.py:42, 83, 92`; `test_store_copy_move.py:75,
  81, 82, 113, 140, 141`; `test_store_sidecar.py:287, 369`) passes the test's client root. The
  value asserted is unchanged.
- **R-cwd, a child process runs in the client root.** `cwd=REPO_ROOT` becomes `cwd=self.client`, and
  `PYTHONPATH=REPO_ROOT` and the scripts' `sys.path.insert(0, repo)` (`test_run_registry.py:21, 179,
  226, 684`; `test_store_command_line.py:25, 60-61, 172-173`; `test_store_amend.py:37, 636-637`)
  become the **package's parent** directory, `os.path.dirname(os.path.dirname(runregistrykit.__file__))`,
  held in a test constant whose name does not say "root" (it is where the package under test is
  imported from, not a records root).
- **U9, the two tests of C5.** `test_manifest_records_the_installed_packages`
  (`test_run_registry.py:276-286`) expects `packages`' keys to be `{"runregistrykit"}` (the fixture's
  empty config) and its value `package_provenance(("runregistrykit",))`.
  `test_the_recorded_names_are_the_two_packages` (`:393-396`) becomes a test of the config: with
  `distributions = ["datastorekit", "raypoolkit"]` in the client's config, a manifest records
  exactly those and `runregistrykit`; it is **renamed**
  `test_the_recorded_names_are_the_registry_and_the_configs`, the one rename this prompt allows.
  `TestPackageProvenance.provenance` (`:305-319`) passes `("datastorekit", "raypoolkit")` to
  `package_provenance`, which has no default now; its tests' assertions are unchanged.
- **The import test** (`test_package_imports.py`, 01's, not ported). `MODULES` (`:22`) gains
  `client.py`. Test 3's `REPO_ROOT/var` check (`:121`) uses the package's parent directory, and the
  test still runs `--help` from an empty `tempfile` directory with no config, which must succeed.

A ported test that fails with only these changes is a **stop** (§5). So is one that would need a
change outside these classes.

### 2.8 The new tests

`runregistrykit/tests/test_client_root.py`. Every temporary directory realpath'd, every `git` call
isolated as in F-client, and nothing created outside `tempfile` directories. At least:

- **The config.** Defaults from an empty file; each key read; relative roots joined to the record
  root and absolute ones kept; each refusal of §2.2 (invalid TOML, unknown key, each wrong type, a
  duplicate distribution, `[stores]` not a table) a `ConfigError` naming the file; `[stores]`
  accepted and kept.
- **The walk.** Found from a script two directories below the root; the nearest config wins when
  two are nested; none found is a `ConfigError` naming the start; `client_root=` without a config
  is a `ConfigError`; `begin()` refused for want of a config creates no directory anywhere.
- **The worktree rule (Q3).** A main checkout and a linked worktree made with `git worktree add` on
  a **second commit**, so the two heads differ: `begin(script=<a script in the worktree>)` records
  under the main checkout's runs root, with the worktree's `git_head` and the worktree script's
  hash; a config in a subdirectory maps to the same subdirectory; a worktree nested inside the main
  checkout whose branch has no config walks up to the main checkout's; a directory outside any
  repository is its own root with `git_head` `"unknown"`.
- **The store layer and the CLI under the root.** A store under the client root, operated from a
  subdirectory of it, records root-relative paths, and a tombstone's relative file list is resolved
  against the root, not the working directory; `python -m runregistrykit --client-root <dir> list`
  and `list` from inside a client both list its runs root; a store command outside any client exits
  1 with the `ConfigError` on stderr and writes nothing.
- **U9.** `packages` holds `runregistrykit` and the config's distributions, once each.

### 2.9 The check retired; `PROVENANCE.md`; `CLAUDE.md`

- **The equivalence check is retired at this prompt's start** (README §4). Before changing
  anything, run it from a worktree of `8155445` made in the scratchpad (`git worktree add --detach
  <scratch>/check-02 8155445`), with the main checkout's venv: it must exit 0, and its summary line
  goes in the log. Remove the worktree afterwards (`git worktree remove`), and check `git worktree
  list` shows this checkout alone. Then add to the check's docstring one paragraph, and change
  nothing else in it: it was retired at prompt 03, it describes `8155445`, and it is run from a
  worktree of that commit.
- **`PROVENANCE.md`** gains a section **"Since the import"**, listing 03's changes (the config file,
  the root rule, the names deleted, U9), and the paragraph on the check (`:145-147`) says it is
  retired and how to run it. Nothing else in it changes.
- **`CLAUDE.md`, "Repository mechanics", the Tests bullet**: the tests need `git` on `PATH` (they
  build temporary repositories); one test (`test_manifest_carries_the_provenance_triple`) still
  reads this checkout's commit, so the checkout must still be a git work tree. Change that bullet
  only.

### 2.10 The board's issues

- **Closed: `[00-the-root-is-the-packages-parent]`** and
  **`[00-the-recorded-distributions-are-sgks]`**, each moved to §4 with what resolved it (this
  prompt's commit, the config, the walk, Q3, U9) and the tests that pin it; their rows deleted from
  `docs/OPEN_ISSUES.md` (9 → 7).
- The other issues' package lines move where 03's edits move them: give each its lines at this
  commit, read in the package, under a "Package lines (03, …)" note.

---

## 3. Verification

1. **The check from 02's tree** (§2.9): exit 0 from the worktree of `8155445`.
2. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root: **`Ran 108
   + N tests … OK`**, N the new tests of §2.8; 108 before. Count by loader and give the per-module
   counts. The suite takes about 15 s at 02; give the time seen.
3. **Nothing outside temporary directories.** `git status --short --ignored` is the same before and
   after a run (but `__pycache__/`); no `var/` at the root or beside the package; `git worktree
   list` shows this checkout alone after the run; no Ray process before or after.
4. **The import.** From an empty scratch directory, `env -u PYTHONPATH ./venv/bin/python -I -c
   "import runregistrykit, runregistrykit.stores, sys; assert not {'ray', 'sqlalchemy',
   'datastorekit'} & set(sys.modules)"` exits 0, and `-I -m runregistrykit --help` exits 0 there
   with no config anywhere above it; `-I -m runregistrykit list` exits 1 with the `ConfigError`.
   Check first that no `runregistrykit.toml` exists in any parent of the scratch directory.
5. `grep -rn "REPO_ROOT\|DEFAULT_ROOT\|DEFAULT_STORES_ROOT\|RECORDED_DISTRIBUTIONS" runregistrykit`
   finds none of the four names in the package or its tests.
6. **The mutation record**, §3.7, each a diff exactly as applied, with the suite's verdict and the
   failing tests. None is committed.
7. **The tests catch behaviour** (README §5 rule 10). Each mutation applied to the package, the
   suite run, and reverted:
   - (m1) the walk examines only the start directory, never its parents;
   - (m2) step 3 of §2.4 removed (`root = found` always);
   - (m3) provenance taken in `found` instead of the start directory;
   - (m4) `runregistrykit` left out of the recorded names;
   - (m5) unknown config keys accepted;
   - (m6) in `begin()`, the run directory made before the client root is located;
   - (m7) `_present` resolving a tombstone's files against the working directory instead of the
     root;
   - (m8) the agent's own: one mutation of the CLI's `--client-root` or `None` defaults that a test
     catches, named in the log.
   Each must fail at least one test, named in the log. A mutation no test catches is a stop: the
   test is missing, and §2.8 asked for it.
8. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2's changes are in, and `runregistrykit/` gains exactly `client.py`,
   `tests/client_fixtures.py` and `tests/test_client_root.py`.
2. §3.1–§3.8 hold.
3. **The records**, in the same commit:
   - the log, `logs/03-the-root-and-the-client-config.md`, per README §5.1: the check's summary
     from 02's tree, every F-client, R-root, R-cwd and U9 instance accounted for (README §5 rule 9),
     the suite before (108) and after, and every mutation as a diff;
   - this board: the header, §1's row for 03, §1.1's R1 and R2, §3 and §4 as §2.10;
   - `docs/OPEN_ISSUES.md`: the two rows deleted, the count, the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `PROVENANCE.md`, `CLAUDE.md` and the check's docstring as §2.9.

---

## 5. Stop conditions — stop and ask the user

- The check fails from the worktree of `8155445`.
- A ported test fails with only §2.7's changes, or would need a change outside its classes.
- A mutation of §3.7 is caught by no test.
- Any record would change form: a manifest, `status.json`, `checkpoint.jsonl` or sidecar field
  added, removed or renamed (only `packages`' content changes).
- `begin()`, a store function or the CLI would need to fall back to a location when no config is
  found.
- The suite needs a Ray cluster, starts Ray, imports a client, writes outside a `tempfile`
  directory, or leaves a worktree registered in this repository.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `runregistrykit/__init__.py`, `stores.py`, `__main__.py`; new `client.py`;
  - `runregistrykit/tests/`: `test_run_registry.py`, `store_fixtures.py`,
    `test_store_command_line.py`, `test_store_amend.py`, `test_store_copy_move.py`,
    `test_store_sidecar.py`, `test_package_imports.py`, as §2.7 only; new `client_fixtures.py` and
    `test_client_root.py`;
  - `docs/extraction/compare_with_source.py`'s docstring; `PROVENANCE.md`; `CLAUDE.md`'s Tests
    bullet;
  - the log, this board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It touches nothing of layer C, `FINGERPRINT_FORMAT` or `fingerprint_store`'s client import (04),
  and reads nothing of `[stores]` (04).
- It changes no prose but what its own changes need (05), names no client, and writes no
  `README.md` usage (06).
- It changes `pyproject.toml` not at all, adds no CI and makes no tag.

---

## 7. The log and the board

`logs/03-the-root-and-the-client-config.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 03, §1.1's R1 and R2, §3 and §4 as §2.10.

---

## At writing (2026-10-14, at `71f59ed`)

Measured read-only, for the README's row and the orchestrator:
- **The clients** (through `git` and their tracked files): none has a `runregistrykit.toml`; each
  has one worktree. Every SGK `begin()` caller is two directories below SGK's root
  (`docs/gktk-remedial/scoped_pipeline_run.py:541`, `docs/handover/quadsource_atol_sweep.py:556,
  864`, `docs/a3-v2-readiness/sigterm_handler_probe.py:159`), passes `script=__file__`, and only
  the last passes `root=` (a temporary runs root); no SGK file imports `REPO_ROOT`, `DEFAULT_ROOT`
  or `DEFAULT_STORES_ROOT` from the package. SGK keeps its records and sidecars under `var/runs` and
  `var/datastores`, gitignored. CPBH and SI have no runs root, and neither ignores `var/` (07's
  checklists); SI has a `pyproject.toml` with no `[project]` table, and a diagnostics harness that
  imports a hard-coded main-checkout path (07).
- **The package**: `REPO_ROOT`'s uses and the store layer's are the board's issue lines; the tests
  pass `script=__file__` at 11 sites of `test_run_registry.py`, call `_repo_path` at 12 lines,
  start children with `cwd=REPO_ROOT` at 4 and put it on `sys.path` in 2 child scripts.
  `StoreTestCase.setUp` does not call `RegistryTestCase.setUp`.
- **`git`**: §2.4's paths, as stated there.
