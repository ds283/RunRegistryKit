# Log — prompt 03: the root and the client config

**Subject:** Find the client root from runregistrykit.toml and record under it
**Commit:** this commit (on `main`, after `f02abc7`)
**Date:** 2026-10-14
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief (`brief-03-section0.md`,
the orchestrator's note §0)
**Result:** **landed.** The package finds its client root from `runregistrykit.toml` instead of from
where it is installed: a new module `runregistrykit/client.py` reads the config and walks to it,
a run launched from a linked worktree is recorded under the main checkout (Q3) with its own tree's
provenance, and the runs root, the stores root and the recorded distributions come from the config,
`runregistrykit` always recorded (U9). `REPO_ROOT`, `DEFAULT_ROOT`, `DEFAULT_STORES_ROOT` and
`RECORDED_DISTRIBUTIONS` are gone; no config found is a `ConfigError`, never a fallback. The suite:
**108 → 135**, `Ran 135 tests … OK`. The equivalence check exits 0 from a worktree of `8155445` and
is retired. (m1)–(m8) each fail at least one test. No stop condition was met. Two issues closed
(`[00-the-root-is-the-packages-parent]`, `[00-the-recorded-distributions-are-sgks]`);
`docs/OPEN_ISSUES.md` goes from 9 to 7.

## What shipped

| File | What |
|---|---|
| `runregistrykit/client.py` | **new**, standard library only: `CONFIG_FILE`, `ConfigError(RuntimeError)`, the frozen dataclass `ClientRoot` (`root`, `found`, `config_file`, `runs_root`, `stores_root`, `distributions`, `stores`), `find_client_root(start=None, client_root=None)`; the walk, the config reader (`tomllib`), the record root (§2.4). Its docstring documents the file's form (README §4) |
| `runregistrykit/__init__.py` | `REPO_ROOT`, `DEFAULT_ROOT`, `RECORDED_DISTRIBUTIONS` (and its comment) deleted; re-exports `CONFIG_FILE`, `ClientRoot`, `ConfigError`, `find_client_root` from `.client`; `git_provenance(cwd)` and `package_provenance(names)` lose their defaults; `_repo_path(path, root)`, `_resolve(path, root)`; `_recorded_names(client)` (U9); `Run(path, *, client_root=None)` with a lazy `client_root` property; `begin(…, *, client_root=None)` locates first; `list_runs(…, *, client_root=None)` locates only without `root` |
| `runregistrykit/stores.py` | `DEFAULT_ROOT`, `REPO_ROOT` dropped from the import, `DEFAULT_STORES_ROOT` deleted; `client_root=None` (keyword-only) on `read_sidecar`, `create_sidecar`, `adopt_sidecar`, `runs_naming`, `copy_store`, `move_store`, `fingerprint_store`, `retire_store`, `amend_sidecar`; the private helpers take the located `ClientRoot` or its `root`; every `_repo_path`, `_resolve` and `git_provenance` call passes its argument (listed below). Layer C, `FINGERPRINT_FORMAT` and the `config.datastore` import untouched |
| `runregistrykit/__main__.py` | a top-level `--client-root DIR`; `list --root`, every `--runs-root` and `--stores-root` default to `None` (the config's), their help saying so; the CLI locates after parsing, only for a `store` command or `list` without `--root`; a `ConfigError` is `!! <message>` on stderr, exit 1 |
| `runregistrykit/tests/client_fixtures.py` | **new**: `PACKAGE_PARENT`, the isolated `git`, `temporary_directory`, `write_client_root`, `enter_client_root` (the F-client helper) |
| `runregistrykit/tests/test_client_root.py` | **new**: 27 tests (§2.8) |
| `runregistrykit/tests/test_run_registry.py`, `store_fixtures.py`, `test_store_command_line.py`, `test_store_amend.py`, `test_store_copy_move.py`, `test_store_sidecar.py`, `test_package_imports.py` | §2.7's classes only, every instance listed below |
| `docs/extraction/compare_with_source.py` | one docstring paragraph: retired at 03, describes `8155445`, run from a worktree of it |
| `PROVENANCE.md` | the paragraph on the check (`:145-147`) says it is retired and how to run it; a new section "Since the import" |
| `CLAUDE.md` | the Tests bullet only |
| this log, `IMPLEMENTATION_STATE.md`, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md` | the records |

`runregistrykit/` gains exactly `client.py`, `tests/client_fixtures.py` and
`tests/test_client_root.py`. Not touched: `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`,
`.idea/`, `tests/__init__.py`, `shard_store_fixtures.py`, `test_store_amend_residuals.py`, the
campaign README, the prompt, `prompts/extraction/orchestrator/`.

**How the root is found, as built.** `find_client_root(start, client_root)`: a `ClientRoot` given as
`client_root` is returned as it is; a path given as `client_root` is `found`, with no walk, and is a
`ConfigError` if it holds no `runregistrykit.toml`; otherwise the walk from `abspath(start or
getcwd())` up to `/` takes the first directory holding a **file** of that name (`os.path.isfile`).
Then the config is read and checked, and the record root is computed by §2.4's three steps
(`git -C <found> rev-parse --path-format=absolute --git-dir --git-common-dir --show-toplevel`; equal
realpaths → `found` unchanged; else `.git` common dir → `normpath(join(dirname(common),
relpath(realpath(found), realpath(toplevel))))`, any other base name → `ConfigError`). `runs_root`
and `stores_root` are joined to the record root and `normpath`'d if relative, kept as they are if
absolute.

**Where each public function locates.**
- `begin()`: first, before the results sidecar is read or any directory made; start = the script's
  directory, else the working directory; provenance `git_provenance(start)`.
- `Run`: lazily, through its `client_root` property, only to resolve a **relative** recorded
  `checkpoint` or `results` (deviation 10) and in `_fingerprint_results`; `status()`, `heartbeat()`,
  `record()` with an absolute ledger, and the lister need none.
- `list_runs`: only when `root` is not given.
- `read_sidecar`: only when the fields read are a registry sidecar carrying a well-formed `retired`,
  just before `_tombstone_problems`, which resolves the listed files (deviation 4).
- `runs_naming`: at entry, even with `runs_root` given (it resolves each manifest's `results`).
- `create_sidecar`, `adopt_sidecar`, `move_store`, `fingerprint_store`, `retire_store`,
  `amend_sidecar`: at entry; `copy_store`: after its purpose refusal, which needs no root, before
  everything else (deviation 12). Each locates once and passes the `ClientRoot` down; provenance is
  `git_provenance(os.getcwd())`, the working directory being their start directory.
- The CLI: after parsing, once, from `--client-root` or the working directory, for every `store`
  command and for `list` without `--root`.

## Deviations from the prompt

The brief's ten corrections and readings are recorded as found (1–9 below and 11); the rest are
this agent's.

1. **The gate's diff is not empty** (brief correction 1, found as it says). `git diff --stat
   8155445 HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` shows
   `PROVENANCE.md` (6 lines, the rewrap of `:145-147`) and `docs/OPEN_ISSUES.md` (3 lines, the row
   of `[02-the-sidecar-readers-guards-are-unpinned]`), both from `71f59ed`; the same diff from
   `71f59ed` is empty. The gate was read from `71f59ed`. **STRUCTURALLY REQUIRED.**
2. **One docstring line changed for §3.5's grep** (brief correction 2): `retire_store`'s
   "``stores_root`` (default `DEFAULT_STORES_ROOT`)" now says "(default the client config's
   `stores_root`)". The R-cwd test constant is `PACKAGE_PARENT`, which does not contain `REPO_ROOT`.
   **STRUCTURALLY REQUIRED.**
3. **The call sites, all of them, including `stores.py:1663`** (brief correction 3, found as it
   says: §2.5's list omits `_find_references`' `{"sidecar": _repo_path(path), …}`). Every call of
   `_repo_path`, `_resolve` and `git_provenance` passes its argument, none of the three has a
   default, and the `ast` walk below shows it. **STRUCTURALLY REQUIRED.**
4. **`read_sidecar` locates only when it is about to resolve a tombstone's files** (brief
   correction 4, recommendation followed, read narrowly): it locates inside the registry branch
   when the fields carry `retired` **and** `retired` is well-formed (`_retired_problems` empty),
   which is exactly when `_tombstone_problems` → `_present` runs. A malformed `retired` resolves
   nothing, so it needs no root. A live sidecar, a legacy one, an absent or unreadable one, and a
   malformed tombstone read with no config (pinned by
   `TestWalk.test_a_live_sidecar_reads_with_no_config_and_a_tombstone_does_not`). `runs_naming`
   locates at entry even when given `runs_root`, as the brief says. **IMPLEMENTATION CHOICE.**
5. **The tests have the shapes four mutations need** (brief correction 5): (m6)'s test passes
   `begin()` an existing `tempfile` runs root from a start with no config and asserts it stays
   empty; (m7)'s tombstone, built by hand, lists a shard (not the primary) relative to the root,
   with the primary absent, read from a subdirectory of the client root; (m3)'s main checkout has an
   **untracked** config and the nested worktree is on another commit; (m8)'s `--client-root` test
   runs from a directory with no config above it. **STRUCTURALLY REQUIRED.**
6. **A test of the bare-repository refusal** (brief correction 6, recommendation followed):
   `TestWorktree.test_a_bare_repositorys_worktree_is_refused`, with `git init --bare`, a push, and
   `git -C bare.git worktree add`. It also checks that `begin()` is refused there leaving its runs
   root empty, so it fails (m6) as well. **IMPLEMENTATION CHOICE.**
7. **Exactly one test reads this checkout's commit** (brief correction 7, measured): from a copy of
   `runregistrykit/` in the scratch directory, with no `.git` above it (and `runregistrykit.__file__`
   the copy's), the suite is `Ran 135 tests … FAILED (failures=1)`, the one
   `TestManifest.test_manifest_carries_the_provenance_triple`. `test_store_sidecar`'s 40-character
   assertion now reads the fixture's repository. `CLAUDE.md`'s Tests bullet says so.
   **STRUCTURALLY REQUIRED** (the measured behaviour).
8. **The two child processes need only R-cwd** (brief correction 8, as found): the `list --root`
   child (`test_run_registry.py:705-711`) runs with `cwd=self.client` and no `PYTHONPATH`, importing
   the package through the venv's editable finder; the crasher has no `cwd=` and inherits the
   fixture's `os.chdir`, from which its `begin()` walks to the fixture's config; only its `repo=`
   changed. **STRUCTURALLY REQUIRED.**
9. **The suite takes about 37 s**, not 15 (brief correction 9): `Ran 108 tests in 32.4s` with only
   §2.7's changes, `Ran 135 tests in 37.0s` after (the replays: 36.0–41.0 s). **STRUCTURALLY
   REQUIRED** (the machine).
10. **`Run` locates only to resolve a relative recorded path.** The prompt names `checkpoint_path`
    and `results_path` as where the lazy locate happens; an absolute recorded path is returned as
    it is, with no config (as `_resolve` would return it), so a run whose ledger is absolute
    records and reads it from anywhere. One private helper, `Run._recorded_path`, serves both
    properties, so `__init__.py` has one `_resolve` call where it had two (`:321`, `:332`).
    **IMPLEMENTATION CHOICE.**
11. **`Run(path, *, client_root=None)` is keyword-only**, like the others, and the fixture registers
    `addCleanup(os.chdir, previous)` after the temporary directory's cleanup, so that it runs first
    (brief correction 10). `ClientRoot` holds a dict and is never hashed. **IMPLEMENTATION CHOICE.**
12. **Where the store functions locate.** At entry in `create_sidecar`, `adopt_sidecar`,
    `move_store`, `fingerprint_store`, `retire_store` and `amend_sidecar`, before their refusals
    (so a `ConfigError` comes before, say, "a reason is required"); in `copy_store` after its
    purpose refusal, which came first in that function before anything else. Each needs the root on
    every path that writes (`_history_entry`, `git_provenance`, the runs root). **IMPLEMENTATION
    CHOICE.**
13. **The CLI fills an omitted `--runs-root` or `--stores-root` from the config** before calling
    the store function, so that `store show` prints the runs root it searched ("runs naming this
    store, under …"), as it printed the default before. **IMPLEMENTATION CHOICE.**
14. **`list_runs` locates when `root` is falsy**, `None` or `""`, as `root or DEFAULT_ROOT` treated
    both before; the CLI's `list` locates only when `--root` is absent. **IMPLEMENTATION CHOICE.**
15. **Prose that 03's changes made wrong was rewritten, and only that.** `begin()`'s docstring: the
    `packages` paragraph said it records "each package the `dk-and-rpk-migration` campaign adopts";
    it now says `runregistrykit` and the config's `distributions` (which drops that SGK citation, a
    C8 line, as a side effect); one paragraph added on `root`, the walk, `client_root` and
    provenance. The docstrings of `read_sidecar`, `runs_naming`, `_present`, `_names_one_of`,
    `_running_runs_naming`, `_repo_path` and `list_runs` say what they locate or resolve against.
    Nothing else in the package's prose changed (05). **IMPLEMENTATION CHOICE.**
16. **R-root at `test_store_amend.py:42`.** That line is the module alias `_repo_path =
    runregistrykit._repo_path`, which is left as it is; its two calls, `:83` and `:92` (now `:85`
    and `:94`), pass `self.client`. So 11 of the 12 named lines change and the twelfth is the alias
    they call through. **IMPLEMENTATION CHOICE.**
17. **`PACKAGE_PARENT` is defined once**, in `client_fixtures.py`, as
    `os.path.dirname(os.path.dirname(os.path.abspath(runregistrykit.__file__)))` (the prompt's
    expression with an `abspath`), and imported by `test_run_registry.py` and
    `test_store_command_line.py`; `test_store_amend.py` imports it from `test_store_command_line`,
    as it imported `REPO_ROOT`. **IMPLEMENTATION CHOICE.**
18. **The fixture's `git`** runs with `GIT_CONFIG_GLOBAL=os.devnull`, `GIT_CONFIG_NOSYSTEM=1` and
    `-c user.name=… -c user.email=…` as §2.7 says, and besides drops every inherited `GIT_*`
    variable, passes `-c commit.gpgsign=false`, and makes the branch `main` (`init -b main`) so
    that no user default changes it. **IMPLEMENTATION CHOICE.**
19. **The renamed U9 test** (`TestPackageProvenance`, a plain `TestCase`) builds its own client
    root with `enter_client_root(self, 'distributions = ["datastorekit", "raypoolkit"]\n')` and a
    `tempfile` runs root, and calls `begin()` with `campaign="client-config"` rather than the run
    helper's SGK campaign name (`[02-the-ported-tests-name-sgk]` is not grown). **IMPLEMENTATION
    CHOICE.**
20. **"Non-empty string" is read as non-blank** (`value.strip()` true) for `runs_root`,
    `stores_root` and each of `distributions`. **IMPLEMENTATION CHOICE.**
21. **The equivalence check reads SGK.** The dispatch says to read none of the clients; §2.9 has
    the check run from 02's tree, and the check reads SGK's objects through `git -C … ls-tree |
    rev-parse | show` (read-only, its working tree never). It was run once, as §2.9 and the
    dispatch's expected summary line require, and nothing else of any client was read or run.
    **STRUCTURALLY REQUIRED.**

No ported test failed with only §2.7's changes (`Ran 108 tests in 32.352s`, OK, before any new test
was written), and none needed a change outside its classes. No record changes form. No stop
condition (§5) was met.

## Verification performed

**At dispatch** (§0 of the gate). `main` at `f02abc7`, clean; this checkout the only worktree; no
`var/`; `git status --short --ignored` showed `prompts/.DS_Store`, `runregistrykit.egg-info/`, the
two `__pycache__/` and `venv/`. `venv/`: Python 3.12.15, `black` 25.1.0; `git` 2.56.0. No Ray
process (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` exit 1); `RAY_ADDRESS` unset.
The gate's diff as deviation 1.

**§3.1, the check from 02's tree, run first, before anything was changed.** `git worktree add
--detach <scratch>/agent-03/check-02 8155445`, then from there
`/Users/ds283/Documents/Code/RunRegistryKit/venv/bin/python docs/extraction/compare_with_source.py`:
**exit 0**, 467 lines, ending

```
Summary: 12 checked (4 by 01, 8 by 02): D-name 106, D-fix 5, D-fmt 12 in 3 hunks; 3 pending; 11 not imported and absent; 1 declared new
RESULT: OK
```

`git worktree remove` then left `git worktree list` showing this checkout alone
(`/Users/ds283/Documents/Code/RunRegistryKit f02abc7 [main]`). No other `git worktree` command was
run against this checkout.

**§3.2, the suite**, `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .` from the
root, output to a scratch file:

| | Verdict |
|---|---|
| before (at `f02abc7`) | `Ran 108 tests in 16.007s`, OK |
| §2.7's changes only, no new test | `Ran 108 tests in 32.352s`, OK |
| after | `Ran 135 tests in 37.011s`, OK; the final run, on the tree committed: `Ran 135 tests in 37.353s`, OK |

**108 → 135**, N = 27. By loader at this commit: `test_client_root` 27 (new),
`test_package_imports` 3, `test_run_registry` 29, `test_store_amend` 21,
`test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
`test_store_sidecar` 17; every ported module's count is 02's.

**§3.3, nothing outside temporary directories.** `git status --short --ignored` the same before and
after the run (`diff` empty); no `var/` at the root or under `runregistrykit/`; `git worktree list`
this checkout alone after it; no Ray process before or after (`pgrep` exit 1, every time it was
run, through the mutations too).

**§3.4, the import.** No `runregistrykit.toml` in the empty scratch directory `agent-03/empty` or
any parent of it (a walk to `/`). From there, with `env -u PYTHONPATH`: the `-I -c "import
runregistrykit, runregistrykit.stores, sys; assert not {…} & set(sys.modules)"` exits 0; `-I -m
runregistrykit --help` exits 0 (`usage: runregistrykit [-h] [--client-root DIR] {list,store} ...`);
`-I -m runregistrykit list` exits 1 with `!! No runregistrykit.toml in …/agent-03/empty or any
directory above it. Create one at the client's root; an empty file takes the defaults (runs_root =
"var/runs", stores_root = "var/datastores", distributions = [])`. The directory was still empty
afterwards.

**§3.5.** `grep -rn "REPO_ROOT\|DEFAULT_ROOT\|DEFAULT_STORES_ROOT\|RECORDED_DISTRIBUTIONS"
runregistrykit` finds nothing (exit 1).

**§3.8.** `./venv/bin/black --check runregistrykit docs`: 17 files would be left unchanged.

**The call sites (brief correction 3)**, by an `ast` walk (a scratch script, run with `python -I`
over `runregistrykit/`): every `ast.Call` whose function is the name or attribute `_repo_path`,
`_resolve` or `git_provenance` is listed with its arguments, and fails unless it passes exactly two
positional arguments (one for `git_provenance`), no keyword and no starred argument; each
definition fails if it has a default. Result: **41 calls, 0 bad**; `git_provenance(cwd)`
(`__init__.py:97`), `_repo_path(path, root)` (`:176`) and `_resolve(path, root)` (`:185`) have no
default. The package's 30 calls, with the line each sat at in `8155445`:

| At this commit | Call | At `8155445` |
|---|---|---|
| `__init__.py:313` | `_resolve(recorded, self.client_root.root)` | `:321` and `:332` (deviation 10) |
| `__init__.py:671` | `_repo_path(script, client.root)` | `:639` |
| `__init__.py:675` | `_repo_path(checkpoint, client.root)` | `:643` |
| `__init__.py:676` | `_repo_path(results, client.root)` | `:644` |
| `__init__.py:681` | `git_provenance(start)` | `:649` |
| `stores.py:515` (two) | `_resolve(f, root)` | `:517` |
| `stores.py:780` | `_repo_path(source, root)` | `:774` |
| `stores.py:782` | `_repo_path(destination, root)` | `:776` |
| `stores.py:842` | `git_provenance(os.getcwd())` | `:833` |
| `stores.py:906` | `git_provenance(os.getcwd())` | `:893` |
| `stores.py:939` | `_resolve(results, client.root)` | `:919` |
| `stores.py:1125` | `_repo_path(src, client.root)` | `:1098` |
| `stores.py:1128` | `git_provenance(os.getcwd())` | `:1101` |
| `stores.py:1168` | `git_provenance(os.getcwd())` | `:1140` |
| `stores.py:1530` | `git_provenance(os.getcwd())` | `:1499` |
| `stores.py:1628` | `_resolve(text, root)` | `:1596` |
| `stores.py:1684` | `_repo_path(path, client.root)` | `:1648` |
| `stores.py:1700` | `_repo_path(path, client.root)` | `:1663` (the one §2.5 omits) |
| `stores.py:1704`, `:1705` | `_repo_path(runs_root, client.root)`, `_repo_path(stores_root, client.root)` | `:1666`, `:1667` |
| `stores.py:1709`, `:1711` | `_repo_path(stores_root, client.root)`, `_repo_path(runs_root, client.root)` | `:1671`, `:1673` |
| `stores.py:1882` | `_repo_path(p, client.root)` | `:1841` |
| `stores.py:1911` | `_repo_path(p, client.root)` | `:1869` |
| `stores.py:1967` | `git_provenance(os.getcwd())` | `:1921` |
| `stores.py:1996` | `_repo_path(p, client.root)` | `:1950` |
| `stores.py:2038` | `_repo_path(p, client.root)` | `:1990` |
| `stores.py:2062` | `_repo_path(p, client.root)` | `:2013` |
| `stores.py:2221` | `git_provenance(os.getcwd())` | `:2164` |

The tests' 11 calls: `store_fixtures.py:184`; `test_store_amend.py:85, 94`;
`test_store_copy_move.py:75, 81, 82, 114, 141, 142`; `test_store_sidecar.py:287, 369`; each
`_repo_path(<path>, self.client)`. `_present(files, primary, root)` is called at `stores.py:529`
(`root`, from `_tombstone_problems`, from `read_sidecar`'s located root), `:1720` (`root`, from
`_retire_failure`, which `retire_store` passes `client.root`), `:1891` and `:2037`
(`client.root`). Every `read_sidecar` call in the package passes `client_root=client`
(`__init__.py:430, 648`; `stores.py:817, 860, 1034, 1055, 1502, 1542, 1794, 2012, 2170`;
`__main__.py:137`). `fingerprint_store`, `_find_references`, `_retire_failure` and most of
`retire_store` are reached by no test until 04 (correction 3), so for them this walk is the check.

**The ported tests' changes, every instance (README §5 rule 9).** Lines are this commit's.

- **F-client (5).** `test_run_registry.py:20-24` imports `enter_client_root` (and `PACKAGE_PARENT`,
  R-cwd; `temporary_directory`, U9); `RegistryTestCase.setUp` gains `self.client =
  enter_client_root(self)` (`:123`); `RegistryTestCase.begin` passes `client_root=self.client`
  (`:133`; `black` reflowed the call to one argument per line, `:128-135`); `store_fixtures.py:17`
  imports `enter_client_root`; `StoreTestCase.setUp` gains `self.client = enter_client_root(self)`
  (`:125`), not calling `RegistryTestCase.setUp`, as before. `self.root` and `self.top` stay where
  they were, outside the client root.
- **R-root (12 named lines).** `store_fixtures.py:181` → `:183-184`; `test_store_amend.py:42`
  (the alias, unchanged, deviation 16), `:83` → `:83-85`, `:92` → `:94`;
  `test_store_copy_move.py:75`, `:81`, `:82`, `:113` → `:113-114`, `:140` → `:141`, `:141` →
  `:142`; `test_store_sidecar.py:287`, `:369`. Each passes `self.client`; each value asserted is
  unchanged (every path asserted lies under `self.top`, outside the client root, so `_repo_path`
  returns it absolute, as at `8155445`).
- **R-cwd (13 lines).** `test_run_registry.py:21` (the constant, now imported, `:21`), `:179` →
  `:188` (`CHECKER.format(repo=PACKAGE_PARENT)`), `:226` → `:235` (`CRASHER.format(repo=PACKAGE_PARENT,
  …)`), `:684` → `:709` (`cwd=self.client`); `test_store_command_line.py:25` (the constant removed;
  imported at `:18`), `:60-61` → `:59-60`, `:172-173` → `:171-172` (`cwd=self.client`,
  `PYTHONPATH=PACKAGE_PARENT`); `test_store_amend.py:37` (imports `PACKAGE_PARENT`), `:636-637` →
  `:638-639`.
- **U9 (3).** `test_manifest_records_the_installed_packages` (`:285-298`): its three assertions after
  `assertIn("packages", …)` now expect the keys `{"runregistrykit"}` and the value
  `package_provenance(("runregistrykit",))`, in the manifest and on disk;
  `TestPackageProvenance.provenance` (`:331`) passes `("datastorekit", "raypoolkit")`; the pinning
  test is renamed `test_the_recorded_names_are_the_registry_and_the_configs` (`:405-421`) and
  asserts that with `distributions = ["datastorekit", "raypoolkit"]` the manifest's `packages`
  keys are exactly those and `runregistrykit` (deviation 19). The one rename.
- **The import test (2).** `MODULES` (`:22`) gains `client.py`; test 3's `var` (`:121`) is
  `os.path.join(os.path.dirname(PACKAGE_DIR), "var")`, the package's parent; test 3 still runs
  `--help` from an empty `tempfile` directory with no config, and passes.

No other line of the seven files changed (`git diff --cached -U0` read hunk by hunk).

**C4, records written by `8155445` read as they did** (a probe, not committed). `git archive
8155445 runregistrykit/__init__.py runregistrykit/stores.py` into `agent-03/c4/old`; with that
package (its `REPO_ROOT` the export's directory) `create_sidecar` on a store under
`var/datastores/S/`, then `begin(script=docs/job.py, checkpoint=True, results=<the store>)` and
one `record`. Its manifest holds `docs/job.py`, `var/runs/<id>/checkpoint.jsonl`,
`var/datastores/S/store.sqlite` and `packages` `datastorekit`, `raypoolkit`. Then, with this
commit's package and an empty `runregistrykit.toml` put in that directory: `Run(path,
client_root=…)`'s `checkpoint_path` and `results_path` resolve to the files; `known()` gives
`['a']`; `list_runs(client_root=…)` lists the run; `read_sidecar` is `ok` with history `to`
`var/datastores/S/store.sqlite`; `runs_naming` matches the run by `results` and
`results_store_id`.

**Isolation.** Nothing was installed; no client, DatastoreKit or RayPoolKit was edited or run, and
none was read but the check's `git -C` reads of SGK (deviation 21). Every scratch file, repository
and worktree was in `agent-03/` or a `tempfile` directory; no scratch `.py` went under
`runregistrykit/` or `docs/`.

## The deliberate-breakage record

Each diff below is exactly as applied, to this commit's tree: it was made by editing the staged
file and taking `git diff` against the index (whose blobs are this commit's), then restoring the
file. A `bash` script then replayed each from its diff file: `git apply --check`, `git apply`,
`git apply -R --check`, the suite (§3.2's command), `git apply -R`, and `git status --short`
compared with the clean state. All eight checked both ways, and the tree was clean after each.
None is committed. The suite's verdict and every failing test:

| # | Mutation | The suite | Failing tests |
|---|---|---|---|
| (m1) | the walk examines only the start directory | `Ran 135 … FAILED (failures=1, errors=9)` | all in `test_client_root`: ERROR `TestWalk.test_found_from_a_script_two_directories_below_the_root`, `TestWalk.test_the_nearest_config_wins`, `TestWalk.test_only_a_file_marks_a_root`, `TestWalk.test_client_root_without_a_config_is_a_config_error_and_no_walk`, `TestWorktree.test_a_run_in_a_linked_worktree_records_under_the_main_checkout`, `TestWorktree.test_a_config_in_a_subdirectory_maps_to_the_same_subdirectory`, `TestWorktree.test_a_nested_worktree_without_a_config_walks_up_to_the_main_checkouts`, `TestStoresUnderTheRoot.test_a_store_under_the_root_records_root_relative_paths`, `TestStoresUnderTheRoot.test_a_tombstones_relative_files_are_resolved_against_the_root`; FAIL `TestCommandLine.test_list_from_inside_a_client_lists_its_runs_root` |
| (m2) | `root = found` always | `Ran 135 … FAILED (failures=3)` | FAIL `TestWorktree.test_a_run_in_a_linked_worktree_records_under_the_main_checkout`, `TestWorktree.test_a_config_in_a_subdirectory_maps_to_the_same_subdirectory`, `TestWorktree.test_a_bare_repositorys_worktree_is_refused` |
| (m3) | provenance in `found` | `Ran 135 … FAILED (failures=1)` | FAIL `TestWorktree.test_a_nested_worktree_without_a_config_walks_up_to_the_main_checkouts` |
| (m4) | `runregistrykit` not recorded | `Ran 135 … FAILED (failures=3)` | FAIL `test_run_registry.TestManifest.test_manifest_records_the_installed_packages`, `test_run_registry.TestPackageProvenance.test_the_recorded_names_are_the_registry_and_the_configs`, `test_client_root.TestRecordedDistributions.test_packages_holds_the_registry_and_the_configs_distributions_once_each` |
| (m5) | unknown keys accepted | `Ran 135 … FAILED (failures=1)` | FAIL `TestConfig.test_each_refusal_is_a_config_error_naming_the_file`, subtest `[an unknown key]` |
| (m6) | run directory made before locating | `Ran 135 … FAILED (failures=2)` | FAIL `TestWalk.test_a_refused_begin_creates_no_directory_anywhere`, `TestWorktree.test_a_bare_repositorys_worktree_is_refused` |
| (m7) | `_present` against the working directory | `Ran 135 … FAILED (failures=1)` | FAIL `TestStoresUnderTheRoot.test_a_tombstones_relative_files_are_resolved_against_the_root` |
| (m8) | the CLI ignores `--client-root` | `Ran 135 … FAILED (failures=1)` | FAIL `TestCommandLine.test_client_root_names_the_root_from_anywhere` |

Test names without a module are `test_client_root`'s. The ported tests catch only (m4): every one
of them runs inside its fixture's client root or passes `client_root`, so a mutation of the walk, the
record root or the CLI's override does not reach them. (m1)–(m8) were first applied, with the same
results, to the tree before one later change (the bare-worktree refusal's message, `client.py`
`:184-188`, lost a suggestion that did not hold); the diffs were then regenerated against the final
tree and all eight replayed again, and the table is that replay.

### The diffs

#### (m1) the walk examines only the start directory, never its parents (`client.py`, `_walk`)

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index e45d16f..79cb0a7 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -95,10 +95,7 @@ def _walk(start) -> str:
     while True:
         if os.path.isfile(os.path.join(directory, CONFIG_FILE)):
             return directory
-        parent = os.path.dirname(directory)
-        if parent == directory:
-            raise _no_config(start)
-        directory = parent
+        raise _no_config(start)
 
 
 def _read_config(path) -> dict:
```

#### (m2) step 3 of §2.4 removed: `root = found` always (`client.py`, `_record_root`)

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index e45d16f..0efa934 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -179,6 +179,7 @@ def _record_root(found) -> str:
         # a main checkout (or a submodule): the root is `found` as it was given, and no path
         # printed by git enters it
         return found
+    return found
     common_dir = os.path.normpath(common_dir)
     if os.path.basename(common_dir) != ".git":
         raise ConfigError(
```

#### (m3) provenance taken in `found` instead of the start directory (`begin()`)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 0b0308c..7987560 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -678,7 +678,7 @@ def begin(
         "scope": scope,
         "heartbeat_means": heartbeat_means,
     }
-    manifest.update(git_provenance(start))
+    manifest.update(git_provenance(client.found))
     manifest["packages"] = package_provenance(_recorded_names(client))
     write_json_atomic(os.path.join(path, "manifest.json"), manifest)
     run = Run(path, client_root=client)
```

#### (m4) `runregistrykit` left out of the recorded names (`_recorded_names`)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 0b0308c..d2a2684 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -164,7 +164,7 @@ def package_provenance(names) -> dict:
 def _recorded_names(client) -> tuple:
     """What a manifest's `packages` records: `runregistrykit` itself, always, then the client
     config's `distributions`, without repeating `runregistrykit`."""
-    return ("runregistrykit",) + tuple(
+    return () + tuple(
         name for name in client.distributions if name != "runregistrykit"
     )
 
```

#### (m5) unknown config keys accepted (`client.py`, `_read_config`)

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index e45d16f..a91dc65 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -111,7 +111,7 @@ def _read_config(path) -> dict:
     except ValueError as e:  # tomllib.TOMLDecodeError, or bytes that are not UTF-8
         raise ConfigError(f"{path} is not valid TOML: {e}") from None
 
-    unknown = sorted(set(data) - set(_DEFAULTS))
+    unknown = []
     if unknown:
         raise ConfigError(
             f"{path} has the key(s) {unknown}, which {CONFIG_FILE} does not have; its keys "
```

#### (m6) in `begin()`, the run directory made before the client root is located

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 0b0308c..1fec56d 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -634,6 +634,8 @@ def begin(
     """
     # the client root is located first, so that a refusal leaves nothing behind. The walk starts
     # from the script, else the working directory; provenance is that start directory's
+    if root:
+        os.makedirs(os.path.join(root, run_id(campaign, prompt, slug, when)), exist_ok=True)
     start = os.path.dirname(os.path.abspath(script)) if script else os.getcwd()
     client = find_client_root(start=start, client_root=client_root)
     identifier = run_id(campaign, prompt, slug, when)
```

#### (m7) `_present` resolving a tombstone's files against the working directory instead of the root

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index cfe2f7c..fdc4713 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -512,7 +512,7 @@ def _present(files, primary: Path, root) -> List[Path]:
     it exists and is not among them. A relative listed file is resolved against the record root
     ``root``."""
     present = [
-        Path(_resolve(f, root)) for f in files if os.path.lexists(_resolve(f, root))
+        Path(_resolve(f, os.getcwd())) for f in files if os.path.lexists(_resolve(f, os.getcwd()))
     ]
     if os.path.lexists(primary) and os.path.realpath(primary) not in {
         os.path.realpath(p) for p in present
```

#### (m8) the agent's own: the CLI ignores `--client-root` (`find_client_root()` in `main`)

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 82ebfac..d777834 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -516,7 +516,7 @@ def main(argv=None) -> int:
     root = args.root if args.command == "list" else None
     if args.command == "store" or root is None:
         try:
-            client = find_client_root(client_root=args.client_root)
+            client = find_client_root()
         except ConfigError as e:
             print(f"!! {e}", file=sys.stderr)
             return 1
```

## Observations not acted on

- **`Run.finish(…, fingerprint=True)` takes its provenance from the working directory at finish**,
  as §2.4 says (its start directory), not from the directory `begin()` started in. A run begun with
  `script=` in a worktree and finished from another working directory records the latter's
  `git_head` in its fingerprint's `taken`. As the prompt specifies; recorded for 04, which writes
  `taken` anew.
- **`test_store_command_line.py:16` still imports `runregistrykit`**, which nothing in that module
  now uses (it was used only for `REPO_ROOT`). Left: removing it is outside R-cwd, and it is
  harmless.
- **`PROVENANCE.md`'s "Re-running the check" section still begins "From the repository root"**:
  only its last paragraph was to change (§2.9), and that paragraph now says the check is retired and
  how to run it from a worktree of `8155445`. A reader of the section's top half could run it at the
  root and see it fail.
- **Prose the package still carries about the old root**: the module docstring of `__init__.py`
  (the layout "under `var/runs/` (gitignored, in the repository…)"), and `stores.py:44` and the
  step list of `fingerprint_store` (`:1480-1495`) naming `git_provenance()` with no argument. True
  enough for a client with the default config; 05 rewrites the prose.
- **The package's own `git` calls inherit the environment.** `git_provenance` and the record root's
  `rev-parse` run with the caller's environment, so a `GIT_DIR` or `GIT_WORK_TREE` set by a hook or
  a shell redirects them. The tests' own `git` is isolated; the package's is not, by design (it must
  read the user's real tree), and no test covers a redirected environment.
- **`fingerprint_store`, `_find_references`, `_retire_failure` and `retire_store`'s writes are
  reached by no test of 03** (correction 3): their threading is checked by the `ast` walk and by
  reading. 04's ported tests will reach them.
- **A config that is a symbolic link to a file counts as a file** (`os.path.isfile` follows links),
  and a directory named `runregistrykit.toml` does not (pinned). Not specified by the prompt.

No §3 issue is opened: none of these is a defect in what 03 was asked to do, and each is either
the prompt's rule, 04's or 05's.

## State handed to the next prompt

- The package finds its root from `runregistrykit.toml` (`runregistrykit/client.py`, whose
  docstring documents the file). `[stores]` is accepted as any table and kept in
  `ClientRoot.stores`, unread: **04 adds the fingerprinter's key** there and validates it.
- Every public function that needs the root takes `client_root=` (a path or a `ClientRoot`);
  `begin()`'s `root` and `list_runs`' `root` still name the runs root. `fingerprint_store(…,
  client_root=…)` takes provenance from the working directory and passes the `ClientRoot` to
  `read_sidecar`; its `from config.datastore import factories` (`stores.py:1525`) is 04's.
- **The suite is 135**; 04's count starts there. The ported tests run in a client root of their own
  (`client_fixtures.enter_client_root`), so a test 04 ports onto `StoreTestCase` or
  `CommandLineTestCase` gets one, with `self.client`; a ported assertion that computed a path
  relative to `REPO_ROOT` (`test_store_retire.py:241`, `test_store_retire_references.py:68, 112,
  124, 141`, README §0.2) will pass `self.client` to `_repo_path` instead, an R-root instance. A
  child process runs with `cwd=self.client` and `PYTHONPATH=PACKAGE_PARENT` (`test_store_retire.py:1215`).
- The equivalence check is retired; it describes `8155445` and exits 0 from a worktree of it.
  `PROVENANCE.md` has a "Since the import" section, to which each prompt from 04 adds its changes.
- The board's §3 has seven issues; their package lines at this commit are recorded there.
- Not touched: `pyproject.toml`, `tests/__init__.py`, `shard_store_fixtures.py`,
  `test_store_amend_residuals.py`; no client, DatastoreKit or RayPoolKit was edited or run; nothing
  installed; nothing pushed or tagged.
