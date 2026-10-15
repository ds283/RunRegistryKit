# Orchestrator — prompt 04b, the retire tests

Read [`../README.md`](../README.md) first: §0.2 (the tests; the couplings the brief does not list;
the DatastoreKit message text), §4 (the module map), §5 (every rule; 6, 7, 9, 10 and 11
especially), §6.1 (D4) and §6.2 (U7, U8, U14). The conventions are [`prompt-04a.md`](prompt-04a.md)'s
and its predecessors'; they are restated in §0 because the agent reads §0 and not this directory.
Where this note and an earlier one differ, this one is right for 04b.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names;
- replay the log's mutation diffs with `git apply`, and revert them;
- export this repository's tree at any commit into the session scratchpad, build scratch client
  roots and stores there, and run the package in them, never committing one;
- read SGK's `RunRegistry/tests/test_store_retire.py` and `test_store_retire_references.py` at
  `a45aefc` through `git -C … show` only, to re-port the modules (§3 check 3);
- fix small residue in a follow-up commit of your own (§4).

ChamPBH and SI are not read or run by this prompt or its review; SGK is read only as above.

**The prompt:** [`04b-the-retire-tests.md`](../04b-the-retire-tests.md)
**Closes:** `[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]`,
`[04a-the-loader-accepts-a-fingerprinter-class]` · **Narrows:**
`[00-a-refusal-matches-datastorekit-message-text]` (a test reaches the match; owner still none),
`[02-the-ported-tests-name-sgk]` (the port adds its lines) · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate, read as correction 1 says: 04a landed (`c81ad06`) and reviewed (`8880cfa`);
  `git diff --stat d035ffb HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md`
  empty; U14 taken; the suite 186 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the last port, and it changes what `store retire` deletes.** The port is mechanical and was
trial-run twice, at writing and at dispatch (both 51 OK, no F-client); the two fixes are a few
lines each. The weight of the review is therefore on three things:
- **the port is SGK's two modules**, changed only by §2.2's classes, every assertion intact,
  checked by re-porting them independently (§3 check 3); with them every test README §4 imports is
  ported, and the one test of `_SHARDS_TABLE_UNREADABLE` reaches its match;
- **a fingerprinter that cannot be loaded is a refusal of a first retirement, before anything is
  written, under the flag or not** (U14 (a)), and the loader refuses a class (U14 (b)); and the
  refusal order §2.3 states, which §2.5's tests do not reach on their own (correction 3);
- **no record changes form**: the tombstone's `fingerprint` condition keeps its three keys and its
  two values, and a `"without"` condition still records, verbatim, a failure of the fingerprint
  itself.

**What moves on purpose:** `stores.py` (`retire_store`'s step 3 and one docstring sentence),
`fingerprint.py` (`load_fingerprinter` and one docstring sentence); in the tests,
`test_fingerprinter.py` (§2.5's tests, and correction 3's if followed) and the new
`test_store_retire.py` and `test_store_retire_references.py`; `PROVENANCE.md`; the log and the
records. **Nothing** in `neutral_store.py`, `client_fixtures.py`, `store_fixtures.py`,
`shard_store_fixtures.py`, `test_store_fingerprint.py`, `__init__.py`, `__main__.py`, `client.py`,
`pyproject.toml`, `CLAUDE.md`, `docs/extraction/`, `tests/__init__.py` or any other 02, 03 or 04a
test file.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The gate's diff is not empty.** `git diff --stat 8880cfa HEAD -- runregistrykit docs
   pyproject.toml PROVENANCE.md CLAUDE.md` shows `docs/OPEN_ISSUES.md`, changed by `d035ffb` (the
   commit that wrote 04b), which assigned the loader issue to 04b and opened the retire one. Read
   the gate as the same diff from `d035ffb`, which is empty.
2. **The load in `retire_store` is a check, not a hand-over.** `fingerprint_store` takes no
   fingerprinter and loads its own (`stores.py:1305`), so the object §2.3's call returns is used
   by nothing; the second load comes from `sys.modules`. Call it for its refusal and keep or drop
   the result as you please: IMPLEMENTATION CHOICE, logged. The CLI needs no change for the
   refusal to print: `ConfigError` subclasses `RuntimeError` (`client.py:67`), and `_retire`'s
   `except RuntimeError` (`__main__.py:197`) prints `!!` and returns 1, which is what §2.5's
   command case asserts.
3. **§2.3's order is pinned by no test the prompt asks for.** §2.5 reaches the load only on a store
   with a problem-free sidecar, no run naming it and a sound plan, so a load placed **before**
   step 1 (a `ConfigError` where the reason or sidecar refusal should come), or **after** the plan
   (the plan's refusal where the `ConfigError` should), or **on the completion path too**, passes
   every test of §2.5 and every ported one (the neutral fingerprinter loads). *Recommended:* a
   precedence test in `test_fingerprinter.py`, in the shape of 04a's `TestPrecedence`, with the
   config naming a module that exists nowhere and a full store with a registry sidecar and a
   recorded fingerprint (taken while the config named the neutral fingerprinter): `retire_store`,
   with and without `without_fingerprint=True`, (i) with an empty reason raises the reason refusal,
   a `RuntimeError` that is not a `ConfigError`; (ii) with a running run naming the store, the
   in-use refusal naming the run; (iii) on a completed tombstone, "already retired"; (iv) with a
   `-wal` file beside the primary, as SGK's `test_a_journal_is_refused` makes one (`:758-762`),
   the `ConfigError`, the load coming before the plan; and (v) an interrupted retirement, made
   under the neutral fingerprinter as `TestInterruption` makes one (`mock.patch("os.unlink",
   _fail_on_call(os.unlink, n))`), completes under the broken config, deleting what remained,
   since the completion path takes no fingerprint and §2.3 leaves it unchanged. Each is a few
   lines on §2.5's fixtures, and §2.5 says "at least". The orchestrator's (o1)–(o3) mutate each
   placement (§3 check 7); an uncaught one is opened on the board, not a stop. Measured at
   dispatch, before the fix: (i)–(iii) already hold (the load sits inside `fingerprint_store`,
   after steps 1 and 2), and under the flag a `-wal` is refused by the plan before the fingerprint
   is tried.
4. **What the probe sees before the fix, for the review's "after".** In a scratch client whose
   config named `no_such_module_probe:F`, a full neutral store with a registry sidecar and a
   recorded fingerprint, `retire_store(…, without_fingerprint=True)` **retired it**, leaving the
   sidecar alone of six files, the condition `{"condition": "without", "error": "<the
   ConfigError's text, naming the config file and the spec>", "error_type": "ConfigError"}`; with
   the config naming `runregistrykit.fingerprint:DatastoreKitFingerprinter`, the same, the error
   `TypeError: DatastoreKitFingerprinter.take() missing 1 required positional argument: 'taken'`.
   Without the flag, each is the wrapped "a fresh fingerprint could not be taken (…)" refusal,
   whose remedy names the flag; with `dry_run=True` and the flag, a result whose `fingerprint` is
   the `"without"` condition. After §2.3 all of these are the unwrapped `ConfigError` and the
   six files are byte-identical.
5. **§2.4 goes before the `Fingerprinter` check** (`fingerprint.py:187`): a class with the four
   methods passes `isinstance(found, Fingerprinter)`, so the `isinstance(found, type)` refusal must
   come first, or it never fires. 04a's `test_each_refusal_is_a_config_error_naming_the_file`
   (`test_fingerprinter.py:204-240`) is a `subTest` per refusal; §2.5's class cases fit it as two
   more, or as a test of their own, as the agent prefers (logged).
6. **R-cwd's `IMPORTS` child.** `test_import_loads_neither_ray_nor_sqlalchemy` (SGK `:1210-1218`)
   runs `-c` with `IMPORTS` from `test_store_command_line`, which the package has (`:45-49`); with
   `cwd=self.client`, `''` on the child's path is the client root, which holds the config and
   `.gitignore` only, and `PYTHONPATH` = `PACKAGE_PARENT` gives the package. `PACKAGE_PARENT` is
   imported from `test_store_command_line` as `test_store_amend.py:37` does (it is defined in
   `client_fixtures.py` and imported there at `:18`). Measured: the child exits 0 with both false.
7. **The trial port, repeated at dispatch**, by a script of the orchestrator's over SGK's files from
   `a45aefc`, into an export of `d035ffb` (its own package imported): D-name 18, D-fix 1, N-fix 4
   lines (the two the prompt counts, `compare_fingerprints` dropped from the `stores` import, and the
   shim block after the `_repo_path` alias), N-class 1, R-cwd 3, R-root 30 (24 `_repo_path` calls,
   the five `REPO_ROOT` paths, the import removed), then `black`: **`Ran 51 tests in 28.9s`, OK**,
   the ids SGK's 51 by class as §3.3 counts. No F-client; every `_repo_path` call is inside a method,
   so `self.client` is in scope. The R-root form for a path against `REPO_ROOT` is
   `os.path.join(self.client, recorded)` (references `:68`) and `os.path.relpath(…, self.client)`
   (the other four). Expect the log's counts to match; a different count is explained, not a stop.
8. **The suite will take longer.** 62.2 s at `d035ffb` (57.0 s at 04a's review); the 51 take
   about 29 s alone, each full store built with four shards and fingerprinted. Not a stop; record
   the time seen.
9. **SGK's prose the port carries**, for `[02-the-ported-tests-name-sgk]`: "store-retirement prompt
   03" (`test_store_retire.py:1`), "real multi-shard fixture stores" (`:18`, whose module path
   N-fix rewrites), "a3-v2-readiness prompt 06",
   `[10-store-retire-reports-every-tombstone-as-a-reference]` and "the live A3 backup"
   (`test_store_retire_references.py:1-20`), `sweep_shaped` (`:38`, used at `:392`). The log lists
   them under that issue for 05; none is changed.
10. **`PROVENANCE.md`'s file map** rows for the two modules read "ported by 04" (`:42-43`); the
    prompt's §4.3 says "ported by 04b", and "Since the import" gains 04b's section.

**The facts, checked by the orchestrator on 2026-10-15 at `d035ffb`.** Pass them on.
- **In-repository state.** `main` at `d035ffb`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`.
  `venv/`: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit` at
  `c8570e8` (`v0.4.0`), `runregistrykit` editable; `git` 2.56.0.
- **The suite at `d035ffb`:** `Ran 186 tests in 62.2s`, OK; `git status --short --ignored` the
  same after.
- **SGK** at `14bcac0`, clean; `RunRegistry/tests/test_store_retire.py` at `a45aefc` 1220 lines,
  41 tests in nine classes; `test_store_retire_references.py` 192 lines, 10 in two; the prompt's
  SGK line numbers hold (the `_repo_path` calls, `REPO_ROOT` at `:41, 241, 1215-1216` and `:29,
  68, 112, 124, 141`, `QSI` at `:58`, the command text at `:198`, the SQL on `{QSI}` at `:448-477`,
  `DROP TABLE shards` at `:784`).
- **The prompt's package line numbers** hold at `d035ffb` (its package files are `c81ad06`'s):
  `_find_references` `stores.py:1400-1482`, its stores-root condition `:1431-1432`;
  `_retire_failure` `:1484`; `retire_store` `:1504`, its `require_fingerprinter` `:1547`, the
  `ShardedPool` import `:1622`, step 3 from `if completing:` `:1641`, the first-retirement branch
  `else:` `:1668`, the plan `:1671`, `if not without_fingerprint:` `:1681`, the flag branch's
  `except Exception` `:1712`, `# 4. the references` `:1725`; `_SHARDS_TABLE_UNREADABLE` `:1366`,
  used at `:1626` and `:1673`; `load_fingerprinter` `fingerprint.py:158-192`, its `Fingerprinter`
  check `:187`; `test_fingerprinter.py` fixtures `:1-135`, `TestPrecedence` `:368-413`.
- **The neutral store serves the port as 04a handed it:** `build_full_store(…, shards=4)` gives
  five files to `closed_store_files` and `delete_store`; `Integral` serial 3 on shard 1 with tag
  rows; `Integral_tags (timestamp, parent_serial, tag_serial)`. The trial port's 51 confirm it.
- **§3.4's grep at `d035ffb`** finds only `test_package_imports.py:32` (`"StoreFixtures"` in
  `FORBIDDEN`); it is case-sensitive, so `test_deleting_one_quadsourceintegral_row` is no hit.
- **No `runregistrykit.toml`** above this checkout or the session scratchpad.
- **The index.** **6** open now; **4** after, unless the work opens one.
- **Ray.** No Ray process; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** `runregistrykit/` gains exactly `tests/test_store_retire.py` and
  `tests/test_store_retire_references.py`; `stores.py`, `fingerprint.py` and `test_fingerprinter.py`
  change as §2.3–§2.5 say; nothing else under `runregistrykit/` changes.
- **(E2) The port.** An independent re-port of SGK's two modules differs from the committed ones
  only by the shim lines; the test ids are SGK's 51.
- **(E3) The behaviour,** by reading and by probing: the load before the plan on a first
  retirement, its `ConfigError` unwrapped with nothing written, under the flag or not, in a dry
  run, and from the command; the completion path unchanged; the class refused at load; the flag
  still recording a failure of the fingerprint itself.
- **(E4) The suite.** 186 + 51 + N pass, write nothing outside `tempfile` directories, start no
  Ray.
- **(E5) The mutations.** (m1)–(m7) each fail a named test, and the orchestrator's own as §3 says.
- **(E6) The records.** The log, the board (two closed, two narrowed), the index (4),
  `prompts/INDEX.md`, `PROVENANCE.md`.
- **(E7) The interface.** No record changes form.

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
  replay in `bash`, not zsh. None is committed. After each, `git status` must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`.
  Python's `tempfile` in tests is fine. **No scratch `.py` goes under `runregistrykit/` or
  `docs/`**, even for a moment: discovery walks the one and `black` the other. The port script
  (§2.2) lives in the scratchpad. Scratch client roots and stores go in the scratchpad or a
  `tempfile` directory, never inside this checkout.
- **SGK is read only** through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show a45aefc:<path>`,
  for the two files of the prompt's "Read first" item 5. ChamPBH and SI are not read. No client
  is run.
- **Install nothing.** The venv is as 01 left it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A ported test that fails is a stop, never an edit outside §2.2's
  classes; a mutation no test catches is a stop, never a weakened mutation.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` at the root.
2. **The prompt's gate**, as correction 1: the diff from `d035ffb` empty; the suite 186.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 6 now, 4 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, 04a's log, `docs/OPEN_ISSUES.md`, `CLAUDE.md` and
  `PROVENANCE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and the recommendation of
correction 3 (a precedence test for `retire_store`'s load, five cases).

Tell it plainly:
- **One commit, at the end.** Its log is `logs/04b-the-retire-tests.md`, in README §5.1's form,
  with the prompt's §4.3 additions.
- **The files it may add or change are §0's "What moves on purpose", and nothing else.** In
  particular it must not touch `neutral_store.py`, `client_fixtures.py`, `store_fixtures.py`,
  `shard_store_fixtures.py`, `test_store_fingerprint.py`, `runregistrykit/__init__.py`,
  `__main__.py`, `client.py`, `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `.idea/`,
  `CLAUDE.md`, `docs/extraction/`, `tests/__init__.py`, any other 02, 03 or 04a test file, the
  campaign README, the prompt, or anything under `orchestrator/`.
- **It edits no client repository, DatastoreKit or RayPoolKit; it reads SGK only as §0 says, and
  ChamPBH and SI not at all.**
- **It installs nothing, reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list, the log and the records. `git
   diff d035ffb <commit> --` over `runregistrykit/__init__.py __main__.py client.py pyproject.toml
   README.md LICENSE .gitignore CLAUDE.md docs/extraction runregistrykit/tests/__init__.py` and
   every 02, 03 and 04a test file and fixture but `test_fingerprinter.py` is empty. `git ls-files
   runregistrykit` is 04a's twenty and the two new files. `stores.py` changes in `retire_store`
   only (`git diff` shows hunks there and nowhere else), `fingerprint.py` in `load_fingerprinter`
   and its module docstring only. No `venv/`, `*.egg-info`, scratch file or `var/`.
2. **E3, by reading.**
   - `stores.py`: in `retire_store`'s first-retirement branch, `load_fingerprinter(client)` sits
     after step 2's refusal and before `closed_store_files`, outside every `try`; nothing wraps a
     `ConfigError` from it; the completion branch does not call it; no refusal's text changes
     (diff against `c81ad06`, every hunk the call and the docstring sentence); step 3's flag branch
     still records `str(e)` and `type(e).__name__` of whatever `fingerprint_store` raises.
   - `fingerprint.py`: the `isinstance(found, type)` refusal before the `Fingerprinter` check, a
     `ConfigError` naming the config file and the spec and saying to name an instance; nothing
     else of the loader moves; the module docstring says so.
   - The two ported modules: SGK's, line for line but §2.2's classes (check 3 is the proof; read
     the shim block and the R-root and R-cwd lines by eye as well).
3. **E2, the port, independently.** Export SGK's two modules from `a45aefc` into the scratchpad and
   write a re-port of the orchestrator's own (the dispatch script serves): D-name, D-fix, N-fix with
   the shim, N-class, R-root, R-cwd, then `black`. `diff` each against the committed file: every
   hunk is a shim line or a comment beside it. The loader's test ids are SGK's 51, by class as §3.3
   counts; `test_an_unreadable_shards_table` among them.
4. **E3, by probing**, in the scratchpad, with this checkout's venv, never inside the repository:
   a scratch client root, a full neutral store with a registry sidecar and a recorded fingerprint
   (taken under the neutral fingerprinter), its six files hashed. Then, with the config naming (i)
   a module that exists nowhere and (ii) the class `DatastoreKitFingerprinter`, each of
   `retire_store` plain, with `without_fingerprint=True`, and with `dry_run=True`, raises the
   `ConfigError` naming the config file and the spec, no `"without"` condition and no "a fresh
   fingerprint could not be taken" wrapper; `python -m runregistrykit store retire … --without-fingerprint`
   exits 1 with `!!` and the same text; the six files hash as before after every call. Then the
   precedence of correction 3, whether or not the agent pinned it: an empty reason, a running run,
   a completed tombstone, a `-wal` beside the primary, and an interrupted retirement (patch
   `os.unlink` to fail on the second call under the neutral config, then complete under the broken
   one). Then the flag where it applies: under the neutral fingerprinter, a shard overwritten with
   text is retired under the flag with `error_type` the reader's, the primary's `-wal` refused, and
   `DROP TABLE shards` refused "even under --without-fingerprint".
5. **E4, the suite.** The prompt's §3.1 command: `Ran 186 + 51 + N tests … OK`, the per-module
   counts the log's, the time recorded. `git status --short --ignored` the same before and after but
   for `__pycache__/`; no `var/`; this checkout the only worktree; no Ray process before or after.
   §3.4's grep as the prompt gives it, `test_package_imports.py:32` its only hit.
   `./venv/bin/black --check runregistrykit docs` is clean.
6. **The issues.** The two closed in §4, each with this commit, what resolved it and the tests that
   pin it; their rows gone from the index. `[00-a-refusal-matches-datastorekit-message-text]`
   narrowed: its *Package lines (04b)* name `test_an_unreadable_shards_table` and (m1), owner still
   none, its row kept. `[02-the-ported-tests-name-sgk]` gains the port's lines (correction 9). The
   other two carry their 04b package lines; spot-check each in the package at the commit.
7. **E5, the mutations.** Replay (m1)–(m7) from the log, one at a time, in `bash`; each fails the
   tests the log names; the suite OK after each; the tree clean. Then the orchestrator's own, not
   in the log:
   - (o1) the load moved before step 1 (before the reason check): must fail if correction 3's test
     is in, else it passes and is opened;
   - (o2) the load moved after `closed_store_files`, unwrapped: likewise;
   - (o3) the load added to the completion branch too: likewise;
   - (o4) the `isinstance(found, type)` check placed after the `Fingerprinter` check: must fail
     §2.5's class cases;
   - (o5) the flag branch's `except Exception` narrowed to `except ConfigError: raise` **and** the
     load removed (the refusal by another route, after the plan): must fail if (o2)'s test is in;
   - (o6) `retire_store` recording `"without"` for a `ConfigError` with the files unchanged (the
     condition written, nothing deleted): must fail §2.5's "sidecar's bytes unchanged";
   - (o7) `_find_references` comparing the stores root by text, not `realpath`: must fail
     `test_through_a_stores_root_that_is_a_symlink`.
   An uncaught (o) mutation is opened on the board (owner to be put to the user), not a stop.
8. **E6, the records.**
   - The log has every section of README §5.1; every D-name, D-fix, N-fix, N-class, R-root, R-cwd
     and D-fmt instance accounted for (correction 7's counts, or the difference explained); the
     port script's summary and diff; 186 → 186 + 51 + N with the per-module counts and the time;
     every mutation as a diff, with the tests that fail it; the deviations classified (corrections
     1–3 among them).
   - `PROVENANCE.md`: "Since the import" gains 04b's section (the two modules ported; the two
     fixes); the file map's two rows say "ported by 04b" (correction 10).
   - The board: the header; 04b's row (landed, "this commit", 186 → …); T2b and F3 ✅; §3 and §4
     as check 6. `prompts/INDEX.md`'s row says 04b landed. The index counts 4 by counting (or more,
     each opened issue on the board), matching its header and date.
9. **E7, the interface.** No record changes form: the tombstone's keys and its `fingerprint`
   condition's three keys and two values are those at `d035ffb` (from the diff, and from the
   probe's tombstones in check 4); the manifest's, `status.json`'s, `checkpoint.jsonl`'s and the
   sidecar's keys untouched (the diff touches no writer).
10. **The handover.** The log's "State handed to the next prompt" says what 05 needs: every test
    README §4 imports is ported; the SGK prose the tests carry, listed; the suite count; nothing
    installed, pushed or tagged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 04b* paragraph, in the form of
  04a's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md` and in
    `PROVENANCE.md`;
  - "reviewed" for 04b in the board's header and row, README §2's status column and its header,
    and `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 04b".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 186 → 186 + 51 + N;
  - the two fixes as built: what `store retire` now refuses, and when, and that the flag still
    records a failure of the fingerprint itself; the class refused at load;
  - the port: every test README §4 imports is now ported, and the match on DatastoreKit's text
    has its test;
  - the mutations, the agent's and the orchestrator's, and what is not pinned;
  - the two issues closed, the two narrowed, and anything opened;
  - that 05 can now be written, against the tree 04b left;
  - and whether to push `main`.
