# Orchestrator — prompt 05a, the guard and the public names

Read [`../README.md`](../README.md) first: §0.2 (C8), §2 (05a–05c), §4 (after 05a), §5 (every rule;
5, 6, 9 and 10 especially), §6.2 (U10, U11 as amended at this dispatch, U12, U15, U16). The
conventions are [`prompt-04b.md`](prompt-04b.md)'s and its predecessors'; they are restated in §0
because the agent reads §0 and not this directory. Where this note and an earlier one differ, this
one is right for 05a.

**You do not write code.** You may:
- run the suite, `black --check`, the measuring script and the tests the log names;
- replay the log's mutation diffs with `git apply`, and revert them;
- export this repository's tree at any commit into the session scratchpad and run the package and
  the guard's functions there, never committing anything;
- read SGK at `14bcac0`, ChamPBH at `c21cdfb` and SI at `5fb4a1d` through `git -C … show`,
  `ls-tree`, `rev-parse` and `cat-file -e` only, to re-measure the vocabulary (§3 check 3); and
  DatastoreKit at `b01737f` and RayPoolKit at its `HEAD` the same way;
- fix small residue in a follow-up commit of your own (§4).

No client, DatastoreKit or RayPoolKit is run, imported or edited, and no working tree of theirs is
read.

**The prompt:** [`05a-the-guard-and-the-public-names.md`](../05a-the-guard-and-the-public-names.md)
**Closes:** nothing · **Narrows:** `[00-package-prose-names-sgk]` and `[02-the-ported-tests-name-sgk]`
(their hits listed by the guard, by file and word) · **Opens:** only what the work finds ·
**Model:** Sonnet, as the prompt recommends.

**Gate:**
- The prompt's gate, read as correction 1 says: 04b landed (`5302a6f`) and reviewed (`dfcb884`);
  `git diff --stat 6ec0066 HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md`
  empty; U10, U11 (amended), U12, U15 and U16 taken; the suite 245 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It writes a test that scans the package, its tests and itself, and pins about 210 hits that later
prompts remove.** Almost nothing the package does changes: one function's name, a header, `__all__`.
The weight of the review is therefore on three things:
- **the vocabulary is the clients'**, measured through `git` at the three fixed commits, and an
  independent re-measure gives the same file (§3 check 3);
- **the guard bites, in both directions**: a new hit fails, a known hit that is no longer found
  fails, a count that changes fails; each scan finds what its rule says and no more; the import
  rule pins the scope of `datastorekit`; and the guard, which scans itself, holds no forbidden word
  and no citation of its own;
- **the known hits are exactly what the scans find at the commit**, written by the scans and not by
  hand, split between the package modules (05b's) and the tests (05c's).

**What moves on purpose:** the five package modules (`__init__.py`, `stores.py`, `client.py`,
`fingerprint.py`, `__main__.py`), by the header, `__all__` and, in `__init__.py`, the rename of
correction 2 only; the new `runregistrykit/tests/test_package_is_generic.py`,
`runregistrykit/tests/test_public_names.py`, `runregistrykit/tests/data/client_vocabulary.json` and
`runregistrykit/tests/data/known_hits.json`; the new `docs/extraction/measure_client_vocabulary.py`;
`PROVENANCE.md`; the log and the records. **Nothing** in any existing test module or fixture,
`tests/__init__.py`, `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `CLAUDE.md` or
`docs/extraction/compare_with_source.py`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The gate's diff is not empty.** `git diff --stat dfcb884 HEAD -- runregistrykit docs
   pyproject.toml PROVENANCE.md CLAUDE.md` shows `docs/OPEN_ISSUES.md`, changed by `6ec0066` (the
   commit that wrote 05a), which moved the two prose issues' owners to 05b and 05c. Read the gate as
   the same diff from `6ec0066`, which is empty.
2. **The public name is `slugify`, not `slug`** (the user's ruling at dispatch, recorded in README
   §6.2 under U11). `run_id(campaign, prompt, slug, when=None)` (`__init__.py:82`) has a parameter
   named `slug`, which shadows a module function of that name inside `run_id`: as the prompt words
   it, `run_id` would call its own string argument and raise `TypeError`. And `slug` is `begin()`'s
   keyword, so a client's code nearly always holds a local of that name. Wherever the prompt says
   the function `slug`, read **`slugify`**: §2.4's rename and docstring, `__init__.py`'s
   `__all__`, `test_public_names.py`, the mutation (m8) (`_slug = slugify`), `PROVENANCE.md` and the
   records. `run_id`'s and `begin()`'s signatures do not change; `run_id` calls `slugify`, with no
   alias. STRUCTURALLY REQUIRED, logged.
3. **`run_id`'s test passes `when`.** With `when=None` the stamp is the current second, which a slow
   run can cross between the call and the expectation. Test `run_id("A b", "0 1", "c", when)` with a
   fixed `when` against the three `slugify`s joined with `time.strftime(_ID_STAMP,
   time.localtime(when))`. IMPLEMENTATION CHOICE, logged.
4. **`datastorekit.contract` defines five string values, not four.** Measured: `VERSION_TABLE`
   `"version"`, `VERSION_LABEL` and `TAG_LABEL` `"label"`, `TAG_TABLE` `"store_tag"`, `TAG_SERIAL`
   `"tag_serial"`, and `VERSION_SERIAL_KEY` `"_version_serial"`. *Recommended:* name the first five
   attributes in `PACKAGE_WORDS`, each with its reason, as DatastoreKit's `LAYER_WORDS` does, so that
   a word added to the contract later is not allowed silently; `VERSION_SERIAL_KEY` is not needed
   (it is no client's word) and is left out. Reading every string value instead is within §2.3 if
   the log says so. IMPLEMENTATION CHOICE, logged.
5. **The guard scans itself, so its own tests may not name a forbidden word.** DatastoreKit's
   `test_the_vocabulary_holds_the_registry_and_the_packages` asserts literal client words
   (`"BackgroundModel"`, `"CosmologyModels"`, …), and its `test_the_allow_list` refuses literal
   client modules (`"config.datastore"`, `"CosmologyModels.model_ids"`); DatastoreKit's guard does
   not scan its tests, this one does. Each such literal would be a hit in the guard itself, a known
   hit that 05c could not remove. So §2.3's "some named words of each kind present" is read as:
   words **read from the data file** (for example, each client's first registry key, first identifier
   column, first project package and first campaign, and every `listed` word, each asserted
   forbidden), and each part's size equal to what the data file's `summary` implies; and the allow
   list's refused cases are built from the vocabulary at run time (a project package of each client,
   with and without a submodule), plus a non-client third party such as `numpy`. The guard file must
   end with **no entry** in `known_hits.json`. Building a forbidden word from string fragments to
   dodge the scan is not allowed; the citation pattern alone is built from parts, as §2.3 says.
   IMPLEMENTATION CHOICE, logged.
6. **The import rule has a scope, and `test_the_allow_list` pins it.** `datastorekit` is allowed in a
   package module only inside a function body of `stores.py` or `fingerprint.py`, so the rule's
   function takes the file and whether the import is inside a function, and the allow-list test
   checks, both ways: module scope of `stores.py` refused; inside a function of `stores.py` and
   `fingerprint.py` allowed; inside a function of `client.py` or `__init__.py` refused; anywhere in a
   test allowed; `sqlalchemy` and `ray` allowed in a test and refused in a package module. Measured:
   the package modules import `datastorekit` only inside functions of `stores.py`
   (`datastorekit.SQL.ShardedPool`) and `fingerprint.py` (`store_fingerprint`, `store_inventory`);
   the tests import `datastorekit` and `sqlalchemy` at module scope and `ray` inside one function of
   `test_fingerprinter.py`. So the import scan finds nothing today.
7. **The header must add no hit.** It is a comment block, so the comment and citation scans read it.
   Expected: no hit. A hit inside the header is a **stop** (05b cannot reword it). Likewise `__all__`'s
   strings are read by the string scan: the code-name scan finds nothing in the package modules
   today, so the same names as strings are expected to add nothing.
8. **The trial's counts still apply.** No package file has changed since `dfcb884`, where the
   prompt's trial ran (`6ec0066` touched only `docs/OPEN_ISSUES.md` and `prompts/`). Expect about 209
   hits in all: package modules 0 code / 26 strings / 8 comments / 35 citations; tests 28 / 70 / 1 /
   41 (the prompt's "At writing" table). The new files are expected to add none. A different total is
   explained, not a stop, unless correction 7 applies.
9. **(m6) is caught as the prompt expects.** Measured: `store-retirement` is a campaign of SGK alone
   (SGK 26 campaigns, ChamPBH 10, SI 6; the only shared one is `dk-and-rpk-migration`, in all three),
   so removing it from SGK's list drops it from the forbidden set.
10. **Writing `known_hits.json`.** The writer is a script in your scratchpad that imports the guard's
    own scan functions from the package and dumps their counts; it is never under `runregistrykit/`
    or `docs/`. The log gives its text and its command. The file is not edited by hand afterwards;
    if a later change in this prompt moves a hit, re-run the writer, and the log says so.
11. **`__all__`, derived at dispatch** by §2.4's rule (module-level `def`, `class` and assigned names
    without a leading underscore, defined in the module): `__init__.py` 15 today (`DEFAULT_STALE_AFTER`,
    `Run`, `TERMINAL_STATES`, `begin`, `git_provenance`, `heartbeat_age`, `list_runs`, `liveness`,
    `now_iso`, `package_provenance`, `pid_alive`, `read_json`, `run_id`, `script_sha256`,
    `write_json_atomic`), plus `slugify` and the four `client` names: **20**; `stores.py` **26**
    (its names imported from `.` and `.fingerprint` are not its own); `client.py` 4; `fingerprint.py`
    4; `__main__.py` `["main"]`, which the rule also gives.
12. **The suite takes about 92 s** (91.6 s at `6ec0066`); the guard adds a few seconds at most.

**The facts, checked by the orchestrator on 2026-10-15 at `6ec0066`.** Pass them on.
- **In-repository state.** `main` at `6ec0066`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`.
  `venv/`: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit` at
  `c8570e8` (`v0.4.0`), `runregistrykit` editable; `git` 2.56.0.
- **The suite at `6ec0066`:** `Ran 245 tests in 91.568s`, OK; `git status --short --ignored` the
  same after; no Ray process.
- **The clients**, at the prompt's commits, each resolving (`git rev-parse --verify`): SGK
  `14bcac0eb73069131f8ce4f55d91e5fc3e7318cf`, ChamPBH `c21cdfb5613a3ed976a91a95431495dc8bfd49c8`, SI
  `5fb4a1d71a016f1b23393923b9a3d59972415aa0`. The registries (`config/datastore.py`,
  `config/datastore.py`, `Datastore/SQL/Datastore.py`), factory directories (`ObjectFactories`,
  `ObjectFactories`, `Datastore/SQL/ObjectFactories`) and campaign directories (`prompts`, `prompts`,
  `.prompts`) exist there. Top-level packages: SGK 14 (among them `RunRegistry`, `StoreFixtures`,
  `config`, `thirdparty`, `tools`), ChamPBH 11, SI 15 (among them `Datastore`, `RayTools`, `plotting`).
- **DatastoreKit** at `b01737f` (its `HEAD`) has `datastorekit/tests/test_layer_is_generic.py`
  and `docs/extraction/measure_client_vocabulary.py` (261 lines, no date in its output). Its guard
  matches words case-sensitively and splits a code name on `_`.
- **RayPoolKit** at its `HEAD` (`17029d9`): `raypoolkit/__init__.py`'s first fourteen lines are
  §2.5's, word for word. Each of the five package modules begins with its docstring today.
- **The prompt's package line numbers hold** at `6ec0066`: the imports `__init__.py:47-57`; `_slug`
  `:78`; `run_id` `:82`, its call `:86`; `begin()`'s call of `run_id` `:639`; the (m2) comment
  `# retirement (store-retirement prompt 03)` `stores.py:1356`. Module lengths: `__init__.py` 746,
  `stores.py` 2018, `client.py` 256, `fingerprint.py` 200, `__main__.py` 558.
- **`git ls-files runregistrykit`**: 22 files, all `*.py`.
- **No `runregistrykit.toml`** above this checkout or the session scratchpad.
- **The index.** **4** open now; **4** after, unless the work opens one.
- **Ray.** No Ray process; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** `runregistrykit/` gains exactly the four files; `docs/extraction/` the script;
  the five modules change only by the header, `__all__` and `slugify`.
- **(E2) The vocabulary.** An independent re-measure through `git` at the three commits equals the
  committed file in content; the script is deterministic and refuses as §2.2 says.
- **(E3) The guard,** by reading and by running: the word, split and citation rules as §2.3 states;
  the self-scan clean; the known hits equal to an independent scan of the commit.
- **(E4) The public names and the header,** by reading and by `ast`: `slugify` and no `_slug`; the
  signatures of `run_id` and `begin()` unchanged; `__all__` as correction 11; the header exact.
- **(E5) The suite.** 245 + N pass, write nothing outside `tempfile` directories, start no Ray.
- **(E6) The mutations.** (m1)–(m11) each fail a named test, and the orchestrator's own as §3 says.
- **(E7) The records.** The log, the board (two narrowed), the index (4), `prompts/INDEX.md`,
  `PROVENANCE.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff and the tests
  show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** The prompt's §3.1 command, from the repository root. Write the output to a file in
  the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Mutation diffs** are recorded so that `git apply` replays them from a clean tree at the agent's
  commit. Check each **as recorded in the log** with `git apply --check` and `-R --check`, and
  replay in `bash`, not zsh. None is committed. After each, `git status` must be clean. A mutation of
  a data file is a diff of that file like any other.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`.
  Python's `tempfile` in tests is fine. **No scratch `.py` goes under `runregistrykit/` or
  `docs/`**, even for a moment: discovery walks the one, `black` the other, and the guard's file
  set is derived from the filesystem. The known-hits writer (correction 10) lives in the scratchpad.
- **Clients are read only** through `git -C /Users/ds283/Documents/Code/<repository>` `show`,
  `ls-tree`, `rev-parse` and `cat-file -e`, at the three commits, by the script and nothing else. No
  client is imported or run, and no working tree is read (ChamPBH's has uncommitted changes).
  DatastoreKit is read at `b01737f` and RayPoolKit at its `HEAD`, the same way.
- **Install nothing.** The venv is as 01 left it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A package word or a word rule beyond §2.3 is a stop, never a widened
  rule; a mutation no test catches is a stop, never a weakened mutation; a hit in the header is a
  stop (correction 7).
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` at the root.
2. **The prompt's gate**, as correction 1: the diff from `6ec0066` empty; the suite 245.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 4 now, 4 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Sonnet**, in this checkout. Give it:
- the prompt, the campaign README, the board, 04b's log, `docs/OPEN_ISSUES.md`, `CLAUDE.md` and
  `PROVENANCE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, the user's ruling of
correction 2 (`slugify`) and the recommendations of corrections 4 and 5.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/05a-the-guard-and-the-public-names.md`, in README
  §5.1's form, with the prompt's §4.3 additions.
- **The files it may add or change are §0's "What moves on purpose", and nothing else.** In
  particular it must not touch any existing test module or fixture, `tests/__init__.py`,
  `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `.idea/`, `CLAUDE.md`,
  `docs/extraction/compare_with_source.py`, the campaign README, the prompt, or anything under
  `orchestrator/`.
- **It edits no client repository, DatastoreKit or RayPoolKit, and reads them only as §0 says.**
- **It installs nothing, reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions, and on correction 7's.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list, the log and the records. `git
   diff 6ec0066 <commit> --` over every existing file under `runregistrykit/tests/`, `pyproject.toml`,
   `README.md`, `LICENSE`, `.gitignore`, `CLAUDE.md`, `docs/extraction/compare_with_source.py`, the
   campaign README and the prompt is empty. `git ls-files runregistrykit` is the 22 and the four new
   files; `git ls-files docs/extraction` gains the script. No `venv/`, `*.egg-info`, scratch file or
   `var/`.
2. **E4, the five modules.** For each, the diff against `6ec0066` with the header block and the
   `__all__` block removed is empty but, in `__init__.py`, the `def slugify` line, its docstring
   and `run_id`'s call line. By `ast`: `__all__` sorted and equal to correction 11's sets; every name
   resolves; `inspect.signature` of `run_id` and `begin` equal to `6ec0066`'s (from an export);
   `runregistrykit` has no `_slug`; `run_id` calls `slugify`; the first fourteen lines of each are
   RayPoolKit's header (`cmp` against `git -C …/RayPoolKit show HEAD:raypoolkit/__init__.py | head
   -14`), line 15 blank, and `ast.get_docstring` the docstring at `6ec0066`. No test module carries
   the header.
3. **E2, the vocabulary, independently.** Write a measurer of the orchestrator's own in the
   scratchpad, by §2.2's rules, reading the clients through `git` at the three commits; compare its
   output with the committed `client_vocabulary.json`, part by part (keys in order; columns and
   module counts; packages; campaigns; `listed` with its sources). Run the agent's script twice into
   the scratchpad: `cmp` equal to each other and to the committed file. With the committed file
   present and no `--output`: exit 1, the tree unchanged. With a client's commit made unreadable (an
   exported copy of the script pointing at a commit that does not exist): exit 2. Read the script:
   standard library only; `git` only, never a working tree; `black`-clean; no header.
4. **E3, the guard, by reading.** `test_package_is_generic.py` read in full: `package_files()`
   from the filesystem, `__pycache__` skipped, tests included; the `git ls-files` pin; the forbidden
   set as §2.3 (registry keys, identifier columns, packages less the four, campaigns, `listed`, less
   `PACKAGE_WORDS` read from `datastorekit.contract` as correction 4); the word pattern and its
   whole/dot/hyphen splits; code names whole and split on `_`; the citation pattern's three forms,
   built from parts; the import rule's scope as correction 6; the known hits compared by file, word
   and count, both ways, with the report §2.3 asks for; no Ray, no store, no client. Its docstring
   says what it scans, forbids and allows and where the known hits live, with no forbidden word and
   no citation (correction 5).
5. **E3, the known hits, independently.** A scanner of the orchestrator's own in the scratchpad, by
   §2.3's rules and the committed vocabulary, over an export of the commit: its counts by scan, file
   and word equal `known_hits.json` exactly. Totals by scan, package modules and tests, against
   correction 8's. No entry for `test_package_is_generic.py`, `test_public_names.py` or any header
   line. `owners` as §2.3.
6. **E5, the suite.** The prompt's §3.1 command: `Ran 245 + N tests … OK`, the per-module counts the
   log's, the time recorded. `git status --short --ignored` the same before and after but for
   `__pycache__/`; no `var/`; this checkout the only worktree; no Ray process before or after.
   `./venv/bin/black --check runregistrykit docs` is clean.
7. **E6, the mutations.** Replay (m1)–(m11) from the log, one at a time, in `bash`; each fails the
   tests the log names; the suite OK after each; the tree clean. Then the orchestrator's own, not in
   the log:
   - (o1) a forbidden word (a project package read from the data file) added to the guard's own
     module docstring: must fail the string scan;
   - (o2) `PACKAGE_WORDS` gaining `handover`: known hits no longer found;
   - (o3) the citation pattern losing its `§` form: known citation hits no longer found;
   - (o4) the hyphen split dropped from the word rule: the `handover` and `A3` hits inside
     `handover-A3-baseline-lambdacdm` lost;
   - (o5) the import rule allowing `datastorekit` at a package module's scope: must fail
     `test_the_allow_list`, without any import moved;
   - (o6) a known word written a second time in a file that already has it (a second `A3` in a
     `stores.py` docstring): must fail on the count;
   - (o7) one module's `__all__` unsorted, and separately one name dropped from it;
   - (o8) the header's year changed in `fingerprint.py`;
   - (o9) the identifier-column rule dropped (every column forbidden): new hits.
   An uncaught (o) mutation is opened on the board (owner to be put to the user), not a stop.
8. **E7, the records.**
   - The log has every section of README §5.1; the script's summary; the per-scan totals, package
     and tests; how `known_hits.json` was written (the writer's text and command); 245 → 245 + N
     with the per-module counts and the time; every mutation as a diff, with the tests that fail it;
     the deviations classified (corrections 1–5 among them).
   - `PROVENANCE.md`: "Since the import" gains 05a's section (the guard and its data; `slugify`;
     `__all__`; the header).
   - The board: the header; 05a's row (landed, "this commit", 245 → …); P2 and N1 ✅; §3's four
     issues each with *Package lines (05a, …)*, the two narrowed ones pointing at `known_hits.json`.
     `prompts/INDEX.md`'s row says 05a landed. The index counts 4 by counting (or more, each opened
     issue on the board), matching its header and date.
9. **The interface.** No record changes form: the diff touches no writer; `run_id` gives the same id
   for the same arguments as at `6ec0066` (an export, a fixed `when`, a few inputs with spaces,
   slashes and leading punctuation).
10. **The handover.** The log's "State handed to the next prompt" says what 05b and 05c need: the
    known hits by owner, with totals; how to re-write `known_hits.json` after a rewrite (05b and 05c
    remove entries; they never add one); the suite count; nothing installed, pushed or tagged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 05a* paragraph, in the form of
  04b's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md` and in
    `PROVENANCE.md`;
  - "reviewed" for 05a in the board's header and row, README §2's status column and its header,
    and `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 05a".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 245 → 245 + N;
  - the guard: what it scans and forbids, the known hits by scan and owner, and that it scans
    itself clean;
  - `slugify`, `__all__` and the header;
  - the mutations, the agent's and the orchestrator's, and what is not pinned;
  - the two issues narrowed, and anything opened;
  - that 05b can now be written, against the tree 05a left;
  - and whether to push `main`.
