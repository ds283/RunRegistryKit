# Orchestrator — prompt 03, the root and the client config

Read [`../README.md`](../README.md) first: §0.2 (C1–C5, C9), §4 (the check's retirement), §5 (every
rule; 6, 7, 9 and 10 especially), §6.1 (Q2, Q3) and §6.2 (U5, U9). The conventions are
[`prompt-01.md`](prompt-01.md)'s and [`prompt-02.md`](prompt-02.md)'s; they are restated in §0
because the agent reads §0 and not this directory. Where this note and an earlier one differ, this
one is right for 03.

**You do not write code.** You may:
- run the suite, the retired check from a worktree of `8155445`, `black --check` and the tests the
  log names;
- replay the log's mutation diffs with `git apply`, and revert them;
- export this repository's tree at any commit into the session scratchpad, and build scratch client
  roots, git repositories and worktrees there, and run the package in them, never committing one;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review.

**The prompt:** [`03-the-root-and-the-client-config.md`](../03-the-root-and-the-client-config.md)
**Closes:** `[00-the-root-is-the-packages-parent]`, `[00-the-recorded-distributions-are-sgks]` ·
**Narrows:** nothing planned · **Opens:** only what the work finds · **Model:** Opus, as the prompt
recommends.

**Gate:**
- The prompt's gate, read as correction 1 says: 02 landed (`8155445`) and reviewed (`71f59ed`);
  `git diff --stat 71f59ed HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md`
  empty; U5 and U9 taken; the suite 108 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that it
  could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the first prompt that changes what the package does, and the check no longer watches.**
01 and 02 were held line by line against SGK by `compare_with_source.py`; 03 retires it at its
start. From here a reviewer has only the prompt, the diff and the tests, so the review has three
halves:
- **the ported tests are 02's tests**, changed only by F-client, R-root, R-cwd, U9 and the import
  test's two edits, with one rename, every other assertion intact;
- **the new behaviour is the prompt's**: the walk, the override, the record root, provenance from
  the start directory, the root threaded through every call site, no fallback, nothing at import;
- **every record already written reads as it did** (C4). No test of the suite was written by code
  older than 03, so the review checks C4 itself, with records written by `8155445`'s package
  (§3 check 5).

**What moves on purpose:** the three modules; a new `client.py`; seven ported test files and the
import test, as §2.7; two new test files; one paragraph of the check's docstring; `PROVENANCE.md`'s
new section and its paragraph on the check; `CLAUDE.md`'s Tests bullet; the log and the records.
Nothing in `pyproject.toml`, `tests/__init__.py`, `shard_store_fixtures.py` or
`test_store_amend_residuals.py`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The gate's diff is not empty.** `git diff --stat 8155445 HEAD -- runregistrykit docs
   pyproject.toml PROVENANCE.md CLAUDE.md` shows two files, both changed by `71f59ed`, the review
   of 02: `PROVENANCE.md` `:145-147` rewrapped (the same words) and `docs/OPEN_ISSUES.md` gaining
   `[02-the-sidecar-readers-guards-are-unpinned]`'s row. Read the gate as the same diff from
   `71f59ed`, which is empty. The paragraph §2.9 changes is still `PROVENANCE.md:145-147`.
2. **§3.5's grep needs one prose edit.** `stores.py:1728`, in `retire_store`'s docstring, says
   "``stores_root`` (default `DEFAULT_STORES_ROOT`)". The grep finds it, so the line must say the
   default is the config's `stores_root`: STRUCTURALLY REQUIRED, and the only docstring 03 changes
   for its grep. The test constant of R-cwd must not contain the substring `REPO_ROOT` either.
3. **§2.5's list of call sites omits one, and the retire path is reached by no 03 test.** The
   complete list at `8155445`:
   - `_repo_path` / `_resolve`: `__init__.py:321, 332, 639, 643, 644`; `stores.py:517` (two calls),
     `774, 776, 919, 1098, 1596, 1648, 1663, 1666, 1667, 1671, 1673, 1841, 1869, 1950, 1990, 2013`.
     §2.5 lists all but **`:1663`** (`_find_references`, `{"sidecar": _repo_path(path), …}`).
   - `git_provenance()`: `__init__.py:649`; `stores.py:833, 893, 1101, 1140, 1499, 1921, 2164`.
   - `_present`: called at `stores.py:530, 1682, 1849, 1989`.
   - `read_sidecar`: called at `__init__.py:412, 616`; `stores.py:810, 848, 1008, 1029, 1471, 1511,
     1754, 1966, 2113`; `__main__.py:137`.

   `fingerprint_store` imports `config.datastore` (`:1494`) before it takes provenance (`:1499`),
   and `_find_references`, `_retire_failure` and `retire_store` are tested by 04's modules. So a
   site missed at `:1499`, `:1663-1673`, `:1682`, `:1841-2013` would be a `TypeError` that no test
   sees until 04. `_repo_path(path, root)`, `_resolve(path, root)` and `git_provenance(cwd)` take
   those arguments with **no default**, as the prompt says, and the log lists every call site at
   this commit with what it passes, checked by an `ast` walk that every call of the three passes
   them. The review repeats the walk.
4. **When `read_sidecar` locates.** §2.5 says a function locates exactly when it needs the root,
   and private helpers never locate. `read_sidecar` needs the root only to resolve a tombstone's
   listed files (`_present`, through `_registry_problems` and `_tombstone_problems`).
   *Recommended:* it locates only when the fields it has read carry `retired`, before it calls
   `_registry_problems`, and passes the root down; a live sidecar then reads with no config. If the
   agent locates at entry instead, the log says so as an IMPLEMENTATION CHOICE. `runs_naming`
   locates even when given `runs_root`, since it resolves each manifest's recorded `results`
   (`:919`).
5. **Four mutations bite only on tests of a particular shape.** §2.8's tests must have these, or
   §3.7 stops:
   - **(m6)**: the refusal test passes `begin()` an explicit `root=`, an existing `tempfile` runs
     root, from a start with no config, and asserts that runs root is still empty. Without
     `root=` the mutant has no runs root to make a directory in, and nothing can fail.
   - **(m7)**: `_present` appends the primary whenever it exists, whatever the listing says
     (`stores.py:518-521`). So the tombstone must list, relative to the root, a file that is **not
     the primary** (a shard file, say), with the primary itself absent, and be read from a
     subdirectory of the client root. Build the tombstone by hand, as `a_tombstone` does
     (`test_store_amend.py:75-100`): `retire_store` cannot run here before 04 (C6).
   - **(m3)**: provenance from `found` equals provenance from the start whenever the two are in
     one tree. Only §2.8's nested-worktree case separates them, and only if the nested worktree's
     head differs from the main checkout's. The fixture commits the config, so every branch from
     that commit carries it; in that test the main checkout's config must be **untracked**, and the
     nested worktree on another commit.
   - **(m8)**: the `--client-root` test runs from a working directory with no config above it, so
     that a mutant ignoring the option is not rescued by the walk.
6. **A test of the bare-repository refusal.** §2.4 step 3 refuses a bare repository's worktree, and
   §2.8 lists no test of it. *Recommended:* add one; §2.8 says "at least". Measured: `git init
   --bare <t>/bare.git`, a push, and `git -C <t>/bare.git worktree add <t>/bwt main` give a common
   dir whose base name is `bare.git`.
7. **Which test reads this checkout's commit.** `RegistryTestCase.begin` passes `client_root`, so
   its 11 `script=__file__` calls never walk, but their start is this checkout's `tests/`
   directory, and provenance is the start's: `test_manifest_carries_the_provenance_triple`
   (`test_run_registry.py:269-273`) reads this checkout's `HEAD`. `test_store_sidecar`'s 40-character
   assertion (`:288`) now reads the fixture's repository (the working directory), so it no longer
   needs this checkout. That is the prompt's §2.9 claim; the review tests it without `.git`.
8. **Two child processes need nothing but what R-cwd says.** The `list --root` child at
   `test_run_registry.py:680-686` has no `PYTHONPATH`; run with `cwd=self.client` it imports
   `runregistrykit` through the venv's editable finder (`__editable___runregistrykit_0_1_0_dev0_finder`),
   which points at this checkout. Do not add a `PYTHONPATH` there: that is outside R-cwd. The
   crasher (`:224-230`) has no `cwd=` and inherits the fixture's `os.chdir`, which is how its
   `begin()` finds a config; only its `repo=` changes.
9. **The suite will take about twice as long.** A client root (`git init`, `add`, `commit`, and the
   record root's `rev-parse`) costs about 117 ms (measured, 20 trials), and some 105 tests build
   one: expect about 30 s, not 15. Not a stop; record the time seen.
10. **Small readings.** `Run(path, *, client_root=None)`, keyword-only like the others. Register
    `addCleanup(os.chdir, previous)` after the temporary directory's cleanup, so that it runs
    first. The `ClientRoot` is frozen and holds a dict (`stores`), so it is never hashed; that is
    fine.

**The facts, checked by the orchestrator on 2026-10-14 at `090da27`.** Pass them on.
- **In-repository state.** `main` at `090da27`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`.
  `venv/`: Python 3.12.15, `black` 25.1.0, `runregistrykit` editable; `git` 2.56.0.
- **The check from 02's tree.** `git worktree add --detach <scratch>/check-02 8155445`, then the
  check run there with this checkout's venv: **exit 0**, 467 lines, ending `Summary: 12 checked (4
  by 01, 8 by 02): D-name 106, D-fix 5, D-fmt 12 in 3 hunks; 3 pending; 11 not imported and absent;
  1 declared new` and `RESULT: OK`. `git worktree remove` left this checkout alone in `git worktree
  list`.
- **The suite at `090da27`:** `Ran 108 tests in 15.2s`, OK. By loader at 02: `test_package_imports`
  3, `test_run_registry` 29, `test_store_sidecar` 17, `test_store_copy_move` 27,
  `test_store_command_line` 2, `test_store_amend` 21, `test_store_amend_residuals` 9. `git status
  --short --ignored` the same before and after; no `var/`; no Ray process.
- **The four names**, read in the package: `REPO_ROOT` `__init__.py:57`, used `:98, 179-180, 185`,
  imported `stores.py:132`; `DEFAULT_ROOT` `__init__.py:58`, used `:608, 681`, `stores.py:130`
  (import), `911, 940, 1741`, `__main__.py:29` (import), `376, 388, 390`; `DEFAULT_STORES_ROOT`
  `stores.py:185`, `1728` (docstring, correction 2), `1742`, `__main__.py:452, 455`;
  `RECORDED_DISTRIBUTIONS` `__init__.py:119, 122`. In the tests: `REPO_ROOT` at
  `test_run_registry.py:21, 179, 226, 684`, `test_store_command_line.py:25, 60-61, 172-173`,
  `test_store_amend.py:37, 636-637`, `test_package_imports.py:121`; `RECORDED_DISTRIBUTIONS` at
  `test_run_registry.py:282, 395`.
- **§2.7's instances, counted.** `script=__file__` at 11 sites of `test_run_registry.py` (`:247,
  269, 402, 417, 444, 454, 486, 519, 529, 535, 545`). R-root: the 12 lines the prompt names, each
  a `_repo_path` of a path under `self.top`, outside the client root. U9: `:276-286`, the pinning
  test `:393-396`, and `TestPackageProvenance.provenance` calling `package_provenance()` at `:319`.
  `StoreTestCase.setUp` (`store_fixtures.py:117-123`) does not call `RegistryTestCase.setUp`; it
  sets `self.top` resolved and `self.root = self.top / "runs"`. Every ported store call passes
  `runs_root` or `--runs-root`. Two `mock.patch` targets are package names (`stores._update_sidecar`,
  `stores.write_json_atomic`); 03 need not change either's signature.
- **`git`'s paths** (a scratch main checkout with two commits, under `tempfile.mkdtemp()`, which
  gave `/var/folders/…`). For the main checkout, `rev-parse --path-format=absolute --git-dir
  --git-common-dir --show-toplevel` prints `/private/var/…/main/.git` twice and
  `/private/var/…/main`; for a linked worktree, `…/main/.git/worktrees/wt`, `…/main/.git`,
  `/private/var/…/wt`, and the same from its subdirectory; for a worktree nested at
  `main/.claude/worktrees/nest`, `…/main/.git/worktrees/nest`, `…/main/.git` and the nested path;
  for a bare repository's worktree, `…/bare.git/worktrees/bwt`, `…/bare.git`, `…/bwt`; outside any
  repository, exit 128. So the prompt's §2.4 holds as written.
- **No config anywhere above.** No `runregistrykit.toml` in this checkout, any parent of it, any
  parent of the session scratchpad or of the system temporary directory, or any sibling under
  `Documents/Code/`.
- **The user's global git config** sets no signing, hooks, template or `init` options. The
  fixture's isolation (§2.7 F-client) is still required.
- **The index.** **9** open now; **7** after.
- **Ray.** No Ray process; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** §6's list only; `runregistrykit/` gains exactly `client.py`,
  `tests/client_fixtures.py` and `tests/test_client_root.py`; the check changes in its docstring
  only.
- **(E2) The check retired.** It exits 0 from a worktree of `8155445`, and its docstring and
  `PROVENANCE.md` say how to run it.
- **(E3) The ported tests.** Every change to them is an instance of §2.7's classes, accounted for in
  the log; the test ids are 02's but for the one rename.
- **(E4) The behaviour**, by reading and by probing: the config, the walk, the override, the record
  root, provenance, every call site threaded, no fallback, nothing at import; and C4, records written
  by `8155445`'s package read as they did.
- **(E5) The suite.** 108 + N pass, write nothing outside `tempfile` directories, register no
  worktree here, start no Ray; without `.git`, exactly one test fails.
- **(E6) The mutations.** (m1)–(m8) each fail a named test, and the orchestrator's own as §3 says.
- **(E7) The records.** The log, the board (two closed, the rest's package lines at 03), the index
  (7), `prompts/INDEX.md`, `PROVENANCE.md`, `CLAUDE.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff and the tests
  show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** The prompt's §3.2 command, from the repository root. Write the output to a file in
  the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Mutation diffs** are recorded so that `git apply` replays them from a clean tree at the agent's
  commit. Check each **as recorded in the log** with `git apply --check` and `-R --check`, and
  replay in `bash`, not zsh. None is committed. After each, `git status` must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`.
  Python's `tempfile` in tests is fine. **No scratch `.py` goes under `runregistrykit/` or
  `docs/`**, even for a moment: discovery walks the one and `black` the other. Scratch git
  repositories and worktrees go in the scratchpad or a `tempfile` directory, never inside this
  checkout, and the only `git worktree` command run against this checkout is §2.9's, removed
  afterwards.
- **No client is read or run.** The prompt needs nothing of SGK, CPBH or SI; their facts are its
  "At writing".
- **Install nothing.** The venv is as 01 left it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A ported test that fails is a stop, never an edit outside §2.7's
  classes; a mutation no test catches is a stop, never a weakened mutation.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` at the root.
2. **The prompt's gate**, as correction 1: the diff from `71f59ed` empty; the suite 108.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 9 now, 7 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, 02's log, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md` and the check;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and its two recommendations
(`read_sidecar` locates only for a tombstone; a test of the bare-repository refusal).

Tell it plainly:
- **One commit, at the end.** Its log is `logs/03-the-root-and-the-client-config.md`, in README
  §5.1's form, with the prompt's §4.3 additions and the call-site list of correction 3.
- **The files it may add or change are the prompt's §6 list, and nothing else.** In particular it
  must not touch `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `.idea/`,
  `tests/__init__.py`, `shard_store_fixtures.py`, `test_store_amend_residuals.py`, the campaign
  README, the prompt, anything under `orchestrator/`, or any part of `CLAUDE.md` but the Tests
  bullet; and in the check, anything but its docstring.
- **It edits no client repository, DatastoreKit or RayPoolKit, and reads or runs none of them.**
- **It installs nothing, reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list. `git diff 71f59ed
   <commit> -- pyproject.toml README.md LICENSE .gitignore runregistrykit/tests/__init__.py
   runregistrykit/tests/shard_store_fixtures.py runregistrykit/tests/test_store_amend_residuals.py`
   is empty. `git ls-files runregistrykit` is 02's thirteen and the three new files. `CLAUDE.md`
   changes in its Tests bullet only. The check changes in its docstring only: `ast.dump` of its
   module body after the docstring is the same at `71f59ed` and at the commit, and the docstring
   gains one paragraph. `PROVENANCE.md` gains "Since the import" and changes `:145-147`, nothing
   else. No `venv/`, `*.egg-info`, scratch file or `var/`.
2. **E2, the check retired.** From a fresh `git worktree add --detach <scratch>/check-02 8155445`
   the check exits 0 and its summary line is the log's; the worktree removed, `git worktree list`
   shows this checkout alone.
3. **E3, the ported tests, by diff.** `git diff 8155445 <commit> --` the seven ported files and
   `test_package_imports.py`: classify every hunk as F-client, R-root, R-cwd, U9 or the import
   test's two edits; count R-root (12 lines) and R-cwd (the sites of §0's facts) and match the
   log's accounting. Every changed line holding an `assert` is R-root's or U9's. Then list the test
   ids by loader at `8155445` and at the commit: the same set but for
   `test_the_recorded_names_are_the_two_packages` →
   `test_the_recorded_names_are_the_registry_and_the_configs`, plus `test_client_root`'s.
4. **E4, by reading.** Read `client.py` in full: `CONFIG_FILE`, `ConfigError(RuntimeError)`, the
   frozen `ClientRoot` and its seven fields; `tomllib` reading in binary; every refusal of §2.2 a
   `ConfigError` naming the file, the key or the value; the walk from `abspath(start)` to the
   filesystem root, a **file** only, no other stop; the "none found" message as §2.3 gives it; the
   override with no walk; §2.4's three steps, realpaths compared, `root = found` unchanged in the
   common case, the bare refusal, the subdirectory mapping; relative roots joined to `root` and
   `normpath`'d, no `~` or variables; nothing at module scope but definitions. In `__init__.py`:
   `begin()` locates before `read_sidecar` and `makedirs`; its start is the script's directory, else
   the working directory, and `cwd` does not move it; provenance from the start; `packages` as §2.6;
   the run carries its `ClientRoot`; `Run` locates lazily; `list_runs` only without `root`. In
   `stores.py`: the nine public functions take `client_root`, locate at most once and pass it down;
   private helpers never locate. **Repeat correction 3's `ast` walk**: every call of `_repo_path`,
   `_resolve` and `git_provenance` in the package passes the root or the start directory, and none
   is left at a default. In `__main__.py`: `--client-root`; every default `None`, its help naming
   the config; `--help` locating nothing; a `ConfigError` printed `!! …`, exit 1.
5. **E4, by probing**, in the scratchpad, with this checkout's venv, never inside the repository:
   - **C4.** Build an "old" client: a directory made a git repository, holding `runregistrykit/`
     exported from `8155445`, so that its `REPO_ROOT` is that directory. With `PYTHONPATH` set to
     it, begin a run with `checkpoint=True` and with `results=` a placeholder store under it that
     has a sidecar from the old `create_sidecar` (built as the shard fixtures build one), and record
     a unit. Its manifest and sidecar then hold root-relative paths (`var/runs/…`), as SGK's do.
     Delete the exported package, add an empty `runregistrykit.toml`, and with the committed package:
     `list` from inside the directory lists the run; `Run(path).checkpoint_path` and `.results_path`
     are the paths the old package gave; `known()` returns the unit; `read_sidecar` reads the
     sidecar with no problem and the same fields; `store show` prints it and the run naming it.
   - **Q3.** A scratch main checkout with a config and two commits, and a linked worktree on the
     other commit holding the config and a script: `begin(script=…)` from the worktree records under
     the main checkout's `var/runs`, with the worktree's `git_head` and the script's absolute path
     (the worktree is outside the main checkout); the same from a worktree nested under
     `.claude/worktrees/` records the script relative to the main checkout.
   - **Refusals.** From an empty scratch directory with no config above it: `-m runregistrykit
     --help` exits 0; `list` exits 1 with `!! No runregistrykit.toml in …`; `store show <path>`
     exits 1 and writes nothing; `begin(root=<scratch runs root>)` raises `ConfigError` and leaves
     the runs root empty.
6. **E5, the suite.** The prompt's §3.2 command: `Ran 108 + N tests … OK`, the per-module counts
   the log's, the time recorded. `git status --short --ignored` the same before and after but for
   `__pycache__/`; no `var/`; `git worktree list` this checkout alone; no Ray process before or
   after. §3.4's import checks and §3.5's grep, as the prompt gives them. **Without `.git`:** a
   `git archive` export of the commit in the scratchpad, `runregistrykit.__file__` checked to be
   the export's, gives exactly one failure, `test_manifest_carries_the_provenance_triple`
   (correction 7). `./venv/bin/black --check runregistrykit docs` is clean.
7. **E6, the mutations.** Replay (m1)–(m8) from the log, one at a time, in `bash`; each fails the
   tests the log names; the suite 108 + N OK after each; the tree clean. Then the orchestrator's
   own, not in the log:
   - (o1) a relative `runs_root` joined to `found` instead of the record root: must fail (the
     worktree test);
   - (o2) the subdirectory mapping of §2.4 step 3 dropped (`root = dirname(common-dir)`): must fail;
   - (o3) the bare-repository refusal removed: fails if the agent added the test of §0
     recommendation 6; if it did not, record it as uncaught;
   - (o4) `find_client_root()` called at `client.py`'s module scope: must fail the import test;
   - (o5) the CLI printing a `ConfigError` and returning 0: must fail;
   - (o6) `Run.checkpoint_path` resolving against the working directory instead of the root: record
     whether any test fails. §2.8 asks for none, so an uncaught (o6) is opened on the board (owner to
     be put to the user), not a stop.
8. **The issues.** `[00-the-root-is-the-packages-parent]` and
   `[00-the-recorded-distributions-are-sgks]` in §4, each with this commit, what resolved it and the
   tests that pin it; their rows gone from the index. The other seven issues each carry "Package
   lines (03, …)"; spot-check each in the package at the commit, including
   `[02-the-ported-tests-name-sgk]`'s lines in the edited test files and
   `[02-the-sidecar-readers-guards-are-unpinned]`'s `stores.py` lines.
9. **E7, the records.**
   - The log has every section of README §5.1; the check's summary from 02's tree; every F-client,
     R-root, R-cwd and U9 instance accounted for; correction 3's call-site list; 108 → 108 + N with
     the per-module counts and the time; every mutation as a diff, with the tests that fail it; the
     deviations classified (corrections 1 and 2 among them).
   - `PROVENANCE.md`: "Since the import" lists the config file, the root rule, the four names
     deleted and U9; `:145-147` says the check is retired and how to run it.
   - `CLAUDE.md`'s Tests bullet: `git` on `PATH`; the one test that reads this checkout's commit.
   - The board: the header; 03's row (landed, "this commit", 108 → 108 + N); R1 and R2 ✅; §3 and §4
     as above. `prompts/INDEX.md`'s row says 03 landed. The index counts 7 by counting, matching its
     header and date.
10. **The interface.** No record changes form: the keys `begin()` writes to the manifest and
    `status.json`, and the sidecar's fields, are those at `8155445` (read from the diff, and from
    the probe's records in check 5); only `packages`' content differs.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 03* paragraph, in the form of
  02's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - "reviewed" for 03 in the board's header and row, README §2's status column and its header, and
    `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 03".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 108 → 108 + N;
  - the config file's form, the root rule and the override as built, and what a client must now
    have (a `runregistrykit.toml`; no config is a refusal);
  - C4: records written by `8155445`'s package read as they did;
  - the mutations, the agent's and the orchestrator's, and what is not pinned;
  - the two issues closed, and anything opened;
  - that 04 can now be written, against the tree 03 left, with U6, U7 and U8 to put to the user;
  - and whether to push `main`.
