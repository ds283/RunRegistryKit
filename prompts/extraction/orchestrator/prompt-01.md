# Orchestrator — prompt 01, import the registry

Read [`../README.md`](../README.md) first: §0.2, §1, §4, §5 (every rule) and §6.2 (U2, U3). This is
the campaign's first note, so it states the conventions in full. They are RayPoolKit's `extraction`
notes' (`RayPoolKit/prompts/extraction/orchestrator/prompt-01.md`), adapted to a package of three
modules imported under one rename, with no store touched and, until this prompt lands, no suite.

**You do not write code.** You may:
- run the suite, the equivalence check, `black --check` and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- export SGK's files and this repository's tree into the session scratchpad, and run probes,
  scratch venvs (`uv … --offline`) and breakages there, never committing one;
- read SGK only through `git -C /Users/ds283/Documents/Code/SecondaryGWKit
  show|ls-tree|rev-parse|log|status|diff`, and RayPoolKit's two files the prompt names;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`01-import-the-registry.md`](../01-import-the-registry.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- G1 holds on the source side: SGK's `git ls-tree -r a45aefc -- RunRegistry/` equals the prompt's
  §2.5 table, 25 rows, path and blob; `StoreFixtures/shard_store_fixtures.py` there is `1375949…`.
  U1–U3 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the campaign's foundation, and its only code is a move.** Every later prompt and every
client's adoption stands on two things it delivers: the package as imported, and
`compare_with_source.py`, the check that the package still *is* SGK's registry (README §5 rule 8)
through 02. The review therefore has two halves:
- **the package is SGK's registry**, under README §4's names, changed only by D-name;
- **the equivalence check would catch a real difference**, not only pass on this one. A check that
  accepts everything is worse than none, because 02 extends it and 03 cites the tree it describes.

**What moves on purpose:** nothing that behaves. New files only: `pyproject.toml`,
`PROVENANCE.md`, `runregistrykit/` (`__init__.py`, `stores.py`, `__main__.py`, `tests/__init__.py`,
`tests/test_package_imports.py`), `docs/extraction/compare_with_source.py`, the log, and the
records.

**The equivalence check: the hard part.** The prompt asks for rules, not line lists. Two
recommendations, consistent with RayPoolKit's check:
- **D-name is a substitution applied to the source line.** A differing pair is D-name exactly when
  `re.sub(r"\bRunRegistry\b", "runregistrykit", source_line) == package_line`, indentation and
  trailing text included, and the pair sits in a `difflib` `replace` opcode whose two sides have
  equal length. An insertion or deletion is never classified.
- **No D-fmt rule.** `black` 25.1.0 leaves the renamed modules unchanged (measured below), so the
  class is empty. The check reports `D-fmt: 0` and has no rule that accepts a line under it; a line
  `black` did change is a stop (prompt §5) in any case. If the agent does add one, it compares
  token for token (`tokenize`, ignoring `NL`/`NEWLINE`/`INDENT`/`DEDENT`/`COMMENT` position) and
  the log says why it exists.

**Addition (i), the orchestrator's: the rename must be complete.** As the prompt's §2.6 is written,
a package line *equal* to its source is never examined, so a line on which the rename was not made
(say `stores.py:544` left as SGK's `` `python -m RunRegistry store retire `` text) would pass, and
the D-name count would silently drop from 13 to 12. D-name says "every whole-word occurrence"
becomes `runregistrykit`. So the check also requires that **no line of an imported package module
matches `\bRunRegistry\b`**, and fails naming file and line if one does. Add **breakage (i)**:
`stores.py:544`'s `python -m runregistrykit store retire` reverted to `python -m RunRegistry store
retire`; the check must exit non-zero and name `stores.py:544`. Record it with (a)–(h), as an
IMPLEMENTATION CHOICE made at the orchestrator's direction.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The `numpy` probe (§3.4) fails test 3 too.** `numpy` is not installed in `venv/`, so an
   `import numpy` at module scope of `__main__.py` fails §2.7 test 2 (naming the line, as the
   prompt says) **and** test 3, whose `-m runregistrykit --help` then dies with
   `ModuleNotFoundError`; and the check fails it as an added line. Record every failure seen, not
   only the one the prompt predicts.
2. **The `import json` probe (§3.4) duplicates `__main__.py:25`**, which already imports `json`.
   It still shows what it is meant to (a standard-library import passes test 2). The check fails
   it as an added line; that is expected and recorded.
3. **Test 2's "module scope" is everything that runs at import.** Walk the module's statements
   recursively but do not descend into `FunctionDef`, `AsyncFunctionDef` or `Lambda` bodies; do
   descend into `if`, `try`, `with` and `ClassDef` bodies, which run at import. At `a45aefc` every
   module-scope import is a top-level statement, so this changes no result today; it closes the
   gap a `try: import x` would open. Take a dotted module's first component
   (`importlib.metadata` → `importlib`); `__future__` is in `sys.stdlib_module_names` at 3.12.15.
   A relative import (`level > 0`) and an absolute `runregistrykit…` import are the package's.
4. **Test 3's "no `var/` beside the package".** `.gitignore` excludes `var/` ("a run root made by
   hand while developing"), so `git status` would not show one, and one may exist legitimately in
   a developer's checkout. The test records whether `<REPO_ROOT>/var` exists before the run, and
   asserts that it does not appear if it was absent (or that its listing is unchanged if present).
   `REPO_ROOT` is read from the package (`runregistrykit.REPO_ROOT`), not recomputed.
5. **Subprocess timeouts.** Each subprocess the tests start gets a timeout of at least 120 s:
   unbroken they take a fraction of a second, but under the §3.4 `ShardedPool` probe the child
   imports `ray` (several seconds in this venv).

**The facts, checked by the orchestrator on 2026-10-14 at `ac46f1b`** (by `git` and an export of
SGK's files to the orchestrator's scratchpad; no SGK code was run, the renamed export was imported
from the scratchpad only). Pass them on.
- **The source.** SGK's `HEAD` is `14bcac0` (branch `handover-remedial`), its tree clean;
  `git diff --stat a45aefc HEAD -- RunRegistry StoreFixtures` is empty. `a45aefc` is
  `a45aefc702de643c330372dd6d2d983f38bb8eed`, "Freeze RunRegistry/ for its move to RunRegistryKit".
  `git ls-tree -r a45aefc -- RunRegistry/` has 25 rows and equals §2.5's table path for path and
  blob for blob (parsed from the prompt and compared by script); the shard fixture is `1375949…`
  and `real_store_fixtures.py` `a6d90b8…`. §2.5's 26 rows split 4 imported by 01, 8 ported by 02,
  3 by 04, 11 not imported.
- **The modules.** 710, 2185 and 515 lines; `tests/__init__.py` is empty (`e69de29`). The last
  commits to change each before `a45aefc` are the prompt's: `f54f1c5` (2026-10-11, "Record the
  installed packages in each run's manifest"), `5943492` (2026-10-12, "Close the
  dk-and-rpk-migration campaign"), `66617c9` (2026-09-25, "Add amend_sidecar and store amend, for
  one unknown field").
- **D-name.** `RunRegistry` occurs only as a whole word: 6 lines in `__init__.py`, 13 in
  `stores.py`, 4 in `__main__.py`, every occurrence substring and word alike. Applied with
  `\bRunRegistry\b`, it changes exactly those 23 lines, one line for one line.
  - `__init__.py`: `:7, 31, 43, 371, 581, 587`;
  - `stores.py`: `:115, 197, 544, 1025, 1196, 1455, 1538, 1694, 1758, 1810, 1876, 1907, 2119`;
  - `__main__.py`: `:1, 6, 7, 373`.
  The one renamed line that cites a path that does not exist here is `stores.py:197`
  (`runregistrykit/tests/data/full_store_fingerprint*.json`, with `test_store_fingerprint.GOLDEN`).
  The agent reads the rest and lists any others it judges to cite SGK.
- **`black` 25.1.0** leaves SGK's three modules and the renamed three unchanged ("8 files would be
  left unchanged", the four of each tree).
- **Package line numbers equal SGK's.** D-name replaces one line with one line and `black` changes
  nothing, so every line sits where it sat in SGK, and the board's §3 lines will be the planner's.
  Read in the renamed export: `REPO_ROOT` `__init__.py:57`, `DEFAULT_ROOT` `:58`,
  `DEFAULT_STALE_AFTER = 900.0` `:65`, `git_provenance` `:98`, `RECORDED_DISTRIBUTIONS` `:119`;
  `stores.py`: `DEFAULT_STORES_ROOT` `:185`, `FINGERPRINT_FORMAT = 6` `:206`, `_fingerprint_problems`
  `:416-436`, its call `:630`, layer C `:1152` (the section comment) to `:1399` (`listing_lines`
  ends; `check_listing_path` at `:1402`), `from config.datastore import factories` `:1494`,
  `fingerprint_of` called `:1500`, `_difference` `:1519`, `compare_fingerprints` `:1529`,
  `_SHARDS_TABLE_UNREADABLE` `:1567-1568`; `__main__.py`: `_print_fingerprint` `:267-287`, the
  `main.py --inventory` text `:281`, `prog` `:373`. The agent still reads each from the package,
  and the log says so.
- **`ShardedPool`'s lazy imports** are `stores.py:1084` (in `copy_store`, `def` at `:1070`), `:1121`
  (in `move_store`) and `:1814`. §3.4's probe moves `:1084`.
- **Module-scope imports**, all standard library or relative: `__init__.py:47-55`,
  `stores.py:118-129` (`from . import (` at `:129`), `__main__.py:24-30`.
- **The import probe.** The renamed export, put on `sys.path` in a `-I` interpreter from an empty
  scratch directory: `import runregistrykit, runregistrykit.stores, runregistrykit.__main__` took
  0.2 s, and none of `ray`, `sqlalchemy`, `datastorekit`, `config`, `ObjectFactories`,
  `StoreFixtures`, `RunRegistry` was in `sys.modules`. `--help` (through `runpy`) printed
  `usage: runregistrykit [-h] {list,store} ...`, exit 0, and created nothing in the working
  directory or beside the package.
- **What `venv/` can import** with `-I`: `RunRegistry`, `config`, `ObjectFactories`,
  `StoreFixtures` and `numpy` each give `ModuleNotFoundError`; **`datastorekit` imports** (it is
  installed). So test 1 checks `sys.modules` after the import, never importability.
- **The editable install**, prototyped in a scratch venv (`uv`, offline) with §2.2's
  `pyproject.toml`: `runregistrykit.__file__` is the checkout's file, so `REPO_ROOT` is the
  checkout's root; `-I -m runregistrykit --help` works from any directory; `import docs` fails, so
  `include = ["runregistrykit*"]` keeps `docs/` out; `runregistrykit.egg-info/` appears at the root
  (gitignored). `-I` drops the working directory from `sys.path`, so before the install,
  `-I -m runregistrykit` from anywhere fails. That is expected, not a fault.
- **The toolchain.** `venv/`: Python 3.12.15, pip 26.2.1, `black==25.1.0`, `ray==2.43.0`,
  `SQLAlchemy==2.0.39`, `datastorekit @ git+…@c8570e8…`, 26 lines of `pip freeze`, no
  `runregistrykit`, **no `setuptools`**. So `pip install -e .` builds in an isolated environment
  and fetches `setuptools` from PyPI, which answered at writing (HTTP 200); pip's cache is warm.
  That one fetch is the only network the agent uses. `pip freeze` afterwards gains the editable
  `runregistrykit` line; record it as printed.
- **In-repository state.** `ac46f1b` on `main`, clean; `git status --short --ignored` shows `venv/`
  only; this checkout is the only worktree. `.gitignore` excludes `venv/`, `*.egg-info/`,
  `__pycache__/`, `*.pyc`, `build/`, `dist/`, `.idea`, `.DS_Store` and `var/`. There is no
  `runregistrykit/`, `pyproject.toml`, `PROVENANCE.md` or `docs/extraction/` yet, and no `var/`.
- **Expected counts.** The suite: **0** before (there is none), **3** after. The check: 25 rows and
  the fixture blob equal; 4 imported (D-name 6, 13, 4, 0; D-fmt 0); 11 pending (8 for 02, 3 for
  04); 11 not imported and absent; 1 declared new file. The index: **7** now, 7 after unless the
  work opens an issue.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'`
  empty), and `RAY_ADDRESS` is unset.

**What the review exists to establish.**
- **(E1) The files.** Every file of the prompt's §2.2 and §2.3 exists under its name, and nothing
  else is in `runregistrykit/`.
- **(E2) Equivalence.** `compare_with_source.py` exits 0, and by reading, its rules are narrow:
  D-name is the substitution applied to the source, not a pattern that accepts a class of line,
  and the rename is complete (addition (i)).
- **(E3) The check bites.** (a)–(i) each exit non-zero and name what is wrong.
- **(E4) The import test.** 3 tests pass; test 1 and test 3 run a fresh `-I` interpreter from a
  `tempfile` directory; test 2 reads every import that runs at import.
- **(E5) No client is reachable.** The prompt's §3.1 holds from a clean shell.
- **(E6) The probes.** §3.4's `json`, `numpy` and `ShardedPool` probes, and (d) against test 3,
  fail as recorded.
- **(E7) The records.** The log in README §5.1's form with the prompt's §4.3 additions; the board,
  `prompts/INDEX.md`, the index (7) and `PROVENANCE.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/` and `__pycache__/` are gitignored and
  must not be staged. Count, then paste. A log states only what the diff, the check and the tests
  show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** The prompt's §3.2 command, from the repository root. Write the output to a file in
  the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Breakage diffs** are recorded so that `git apply` replays them from a clean tree at the
  agent's commit. Check each **as recorded in the log** with `git apply --check` and `-R --check`,
  and replay in `bash`, not zsh. None is committed. After each, `git status` must be clean.
  Breakage (g) adds an untracked file: record it as a `git apply`-able new-file diff, and delete
  the file after. Breakage (h) edits the check itself; record it as a diff of
  `docs/extraction/compare_with_source.py`.
- **SGK is read only through `git -C … show|ls-tree|rev-parse a45aefc…`**, and RayPoolKit only by
  reading its two files. Never from SGK's working tree, never by importing either, never by running
  their code or tests (README §5 rule 5).
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`. The
  prompt's §3.1 runs "from a scratch directory"; the scratchpad is one. Python's `tempfile` in
  tests is fine. **No scratch `.py` goes under `runregistrykit/` or `docs/`**, even for a moment:
  the check walks the one and `black` the other.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A difference that fits no class is a stop, never a widened rule.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. `venv/` must hold no
   `runregistrykit`, and there must be no `var/` at the root.
2. **G1.** Re-run `git -C SecondaryGWKit ls-tree -r a45aefc -- RunRegistry/ | wc -l` (25) and the
   shard fixture's `rev-parse`. Record SGK's `HEAD` and status, and whether `RunRegistry/` or
   `StoreFixtures/` moved after `a45aefc` (not a stop, since the prompt reads `a45aefc`, but
   reported).
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 7 now, 7 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md` and `CLAUDE.md`;
- `HEAD`, SGK's `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections, its one addition (completeness and
breakage (i)) and its two recommendations (D-name as a substitution; no D-fmt rule).

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-import-the-registry.md`, in README §5.1's form,
  with the prompt's §4.3 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else.** In particular it
  must not touch `README.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`, `.idea/`, the campaign README,
  the prompt, or anything under `orchestrator/`.
- **It edits no client repository, DatastoreKit or RayPoolKit, and runs none of their code.**
- **It runs no build beyond `pip install -e .`, reaches no network but that install's, and starts
  no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No
   file under `venv/`, no `*.egg-info`, no `.idea/`, no scratch file; no `var/` at the root.
2. **E1, the files.** `git ls-files runregistrykit` lists exactly `__init__.py`, `stores.py`,
   `__main__.py`, `tests/__init__.py` and `tests/test_package_imports.py`. `pyproject.toml` is
   §2.2's: version `0.1.0.dev0`, `requires-python = ">=3.12"`, no `dependencies` entry, `stores =
   ["datastorekit"]` unbounded, `include = ["runregistrykit*"]`.
3. **E2, by running.** In a fresh shell, `./venv/bin/python docs/extraction/compare_with_source.py`
   exits 0, its counts the log's and §0's, and its whole output equal to the log's. Independently,
   `perl -pe 's/\bRunRegistry\b/runregistrykit/g'` over each module exported from `a45aefc` gives
   the committed file byte for byte (`cmp`).
4. **E2, by reading.** Read `compare_with_source.py` in full. The SGK path, the full import hash
   and the table are constants at its top; it reads SGK only through `git -C`; it imports nothing
   of SGK or of the package. The frozen tree is checked first, as an exact set equality. D-name is
   the substitution on equal-length `replace` blocks only; no rule is a list of line numbers, and
   none accepts a line because it merely contains `runregistrykit`. The completeness rule
   (addition (i)) is there. The walk skips `__pycache__` and fails on an undeclared `.py`. Pending
   files exit 0; "not imported" files are checked absent.
5. **E3, the check bites.** Replay (a)–(i) from the log, one at a time, in `bash`. Each must exit
   non-zero and name the line or file. Then one of the orchestrator's own, not in the log: swap
   `stores.py:120` and `:121` (`import json`, `import os`), a change no single line's
   classification can excuse; it must fail. Revert each, and check `git status` is clean.
6. **E4, the import test, by running and reading.** The prompt's §3.2 command gives `Ran 3 tests …
   OK`. Read `test_package_imports.py`: test 1 runs `sys.executable -I` from a `tempfile`
   directory and checks all seven names; test 2 reads every import that runs at import
   (correction 3) and names file, line and module; test 3 checks the usage line, an empty working
   directory and no new `var/` (correction 4). Timeouts as correction 5.
7. **E5, isolation.** From the scratchpad, with `env -u PYTHONPATH`, run the prompt's §3.1: the
   package import succeeds, and `import RunRegistry` and `import config` each fail with
   `ModuleNotFoundError`.
8. **E6, the probes.** Replay §3.4's `json`, `numpy` and `ShardedPool` diffs and (d), each in
   `bash`, and check that the failures are the log's (correction 1 for `numpy`). The suite is 3
   again after each.
9. **E7, the records.**
   - The log has every section of README §5.1; `pip freeze` (Python 3.12.15, the 26 lines of §0
     and the editable `runregistrykit`); the check's whole output; the D-name lines that cite SGK
     paths; the count before (0) and after (3); every breakage as a diff.
   - `PROVENANCE.md` has the six items of the prompt's §2.8, with `a45aefc`'s full hash and subject
     and the three last-change commits right.
   - The board: the header; 01's row (landed, "this commit", suite 3); I1 and I2 ✅; G1's package
     side for 01's files; and §3's seven issues each pointing at `runregistrykit/` lines that are
     true at the commit. `prompts/INDEX.md`'s row says 01 landed. The index counts 7 by counting,
     matching its header.
   - `./venv/bin/black --check runregistrykit docs` is clean.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  RayPoolKit's `extraction` board (*At dispatch*, *The checks*, verdict). Fix small residue in a
  follow-up commit of its own. That includes:
  - "this commit" → the SHA, on the board, in the log, in `PROVENANCE.md` if it uses the phrase,
    and in `prompts/INDEX.md`;
  - "reviewed" for 01 in the board's header and row, README §2's status column and
    `prompts/INDEX.md`;
  - an **Orchestrator notes** line on the board, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 3;
  - the equivalence check's design, its counts per class, and (a)–(i) plus the orchestrator's own
    breakage failing it;
  - where the seven issues now sit in the package;
  - anything opened;
  - that 02 can now be written, against the tree 01 left, with U4 to put to the user;
  - and whether to push `main`.
