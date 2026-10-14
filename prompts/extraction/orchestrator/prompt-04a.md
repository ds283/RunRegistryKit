# Orchestrator — prompt 04a, the client fingerprinter

Read [`../README.md`](../README.md) first: §0.1, §0.2 (C6, C7, the couplings the brief does not
list, layer C, DatastoreKit `v0.4.0`), §5 (every rule; 6, 7, 9, 10 and 11 especially), §6.1 (D3,
D4) and §6.2 (U6, U7, U8). The conventions are [`prompt-03.md`](prompt-03.md)'s and its
predecessors'; they are restated in §0 because the agent reads §0 and not this directory. Where
this note and an earlier one differ, this one is right for 04a.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names;
- replay the log's mutation diffs with `git apply`, and revert them;
- export this repository's tree at any commit into the session scratchpad, build scratch client
  roots and stores there, and run the package in them, never committing one;
- read SGK's `RunRegistry/tests/test_store_fingerprint.py` and `StoreFixtures/real_store_fixtures.py`
  at `a45aefc` through `git -C … show` only, to re-port the module (§3 check 3);
- fix small residue in a follow-up commit of your own (§4).

ChamPBH and SI are not read or run by this prompt or its review; SGK is read only as above.

**The prompt:** [`04a-the-client-fingerprinter.md`](../04a-the-client-fingerprinter.md)
**Closes:** `[00-the-fingerprint-reads-a-clients-registry]`,
`[00-the-store-layer-reads-inside-a-fingerprint]`, `[02-the-sidecar-readers-guards-are-unpinned]` ·
**Narrows:** `[02-the-ported-tests-name-sgk]` (the port adds its lines) · **Opens:** only what the
work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate, read as correction 1 says: 03 landed (`035e4b5`) and reviewed (`f9e0e60`);
  `git diff --stat 2ecb99d HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md`
  empty; U6, U7 and U8 taken; the suite 135 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It deletes the code that computes every fingerprint, and ports tests onto a store that does not
exist yet.** Three things are new at once: a protocol and a loader (`fingerprint.py`), a reader
that reads less (U7), and a neutral store on which SGK's largest fingerprint module is ported. So
the review has four halves:
- **the port is SGK's module**, changed only by §2.8's classes, every assertion intact but the two
  U7 variants, checked by re-porting it independently (§3 check 3);
- **the neutral store is public-names-only** and holds what each ported assertion counts;
- **the store layer's behaviour is the prompt's**: D4 refuses before anything is read, the
  fingerprinter is imported only where a fingerprint is taken, compared, described or listed, and
  `fingerprint_store`'s order and texts are kept;
- **every fingerprint already written reads as it did** (U7): one without `classes` or without
  `encoding_format` is no problem.

**What moves on purpose:** `stores.py`, `__main__.py`, `client.py`; a new `fingerprint.py`; in the
tests, `client_fixtures.py` (the default config, and the class-level variant of correction 8),
`test_package_imports.py` (`MODULES` only), `test_client_root.py` (correction 2's two tests only),
and the new `neutral_store.py`, `test_store_fingerprint.py`, `test_fingerprinter.py`;
`PROVENANCE.md`; the log and the records. **Nothing** in `runregistrykit/__init__.py`,
`pyproject.toml`, `CLAUDE.md`, `docs/extraction/`, `tests/__init__.py`, `store_fixtures.py`,
`shard_store_fixtures.py` or any other 02 or 03 test file.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The gate's diff is not empty.** `git diff --stat f9e0e60 HEAD -- runregistrykit docs
   pyproject.toml PROVENANCE.md CLAUDE.md` shows `docs/OPEN_ISSUES.md`, changed by `2ecb99d` (the
   commit that wrote 04a), whose three rows' owner went from 04 to 04a. Read the gate as the same
   diff from `2ecb99d`, which is empty.
2. **Two 03 tests are overturned by §2.3 and §2.4.** Both in `test_client_root.py`:
   - (a) `TestConfig.test_the_stores_table_is_accepted_and_kept` (`:206-216`) asserts that
     `[stores.more]` is accepted and kept, which §2.3 now refuses. *Reading:* STRUCTURALLY
     REQUIRED. The test changes to pin §2.3: a `fingerprinter` accepted and kept, and another
     `[stores]` key refused with a `ConfigError` naming the file, the key and the value. It is a
     03 test, not a ported one, so rule 9's name rule does not bind it: rename it to say what it
     now asserts, and log the old and new names. `test_each_key_is_read` (`:121-135`) is
     unchanged: `"a.module:an_attribute"` is a valid form, and §2.3 checks form only, at read time,
     importing nothing.
   - (b) `TestWalk.test_a_live_sidecar_reads_with_no_config_and_a_tombstone_does_not` (`:315-318`)
     calls `create_sidecar(…, client_root=d)` under `a_config("")`, which D4 now refuses. This is
     the "03 test whose empty config F-client moves" of the prompt's §6: its config text gains the
     neutral fingerprinter, nothing else.

   Measured at `2ecb99d`: no other 02 or 03 test runs a store operation under a config other than
   the shared helper's default. The other `a_config` and explicit configs reach only `begin`,
   `list`, `list_runs`, `find_client_root`, or a store command outside any client, which is refused
   for want of a config before D4 is reached.
3. **`fingerprint_store`'s docstring, and the `taken` stamp.** §3.4's grep finds the docstring's
   step 2, "the registry `factories` from `config.datastore`" (`stores.py:1484`). Steps 2–4 of that
   docstring are rewritten to §2.5's: STRUCTURALLY REQUIRED. And under §2.5 `taken` is built
   **before** `take` reads the store, where today `now_iso()` and `git_provenance()` run after
   `read_inventory` (`:1527-1539`); the protocol hands `taken` to `take`, so this is STRUCTURALLY
   REQUIRED too. No other step moves; the log says so.
4. **(m5) needs a test that checks the text.** Every refusal DatastoreKit's reader raises is a
   `RuntimeError`: the journal refusal is a plain one (`store_reader._refuse`), and
   `StoreSchemaMismatch` subclasses it (`SQL/schema.py:513`). A wrapper raising `RuntimeError`
   keeps the journal case's type, and SGK's `test_a_refused_store_is_recorded_and_the_run_still_ends`
   asserts only that `-journal` is in the text. So §2.9's read-refusal test asserts `type(e) is
   type(direct)` **and** `str(e) == str(direct)`, where `direct` is what `read_inventory(primary,
   FACTORIES)` raises on the same store. *Recommended:* a second case whose type alone bites, a
   shard missing a table (`StoreSchemaMismatch`).
5. **(m10) needs a test of a particular shape.** Under a working fingerprinter, loading it earlier
   changes nothing a test sees. The test gives a config whose `fingerprinter` names a module that
   exists nowhere (D4 passes: the key is present), then (i) a tombstone and (ii) a running run
   naming the store, and asserts `fingerprint_store` raises the tombstone and the running-run
   refusals, not the `ConfigError`. *Reading:* the CLI's `_fingerprint` loads the fingerprinter
   for `describe` only after `fingerprint_store` returns, inside its `except RuntimeError`, so the
   command keeps the same precedence.
6. **The loader, `sys.path` and `sys.modules` in tests.** Measured: under `python -m unittest`,
   `sys.path[0]` is the repository root as an absolute path (`-m` inserts the start directory);
   under `-c` it is `''`. So in-process, a module in a test's client root is importable only
   through the loader, and (m6) bites, provided the module's name is used by no other test and is
   not already in `sys.modules`. Each test that loads a module from a client root uses a fresh
   name, and restores `sys.path` and drops the module from `sys.modules` in its cleanup. The CLI
   children run `-c` with `cwd=self.client`, so `''` already puts the root on their path; the
   in-process test is the one that bites. The loader leaving `found` on `sys.path` means the
   in-process suite gains one entry per client root that takes a fingerprint: harmless, recorded.
   Calling `importlib.invalidate_caches()` before the import is an IMPLEMENTATION CHOICE.
7. **(m3) and the D4 check are pinned by 02's tests already.**
   `test_store_command_line.TestStoreCommands.test_show_create_adopt_copy_and_move` asserts that
   `store show` loads neither `ray` nor `sqlalchemy`, and that `create` and `adopt` load no `ray`;
   and importing the neutral store loads both (measured: `datastorekit.SQL.factory_base` and
   `datastorekit.store_inventory` load `ray` and `sqlalchemy`). So the neutral store imports
   `datastorekit` at module scope, as its factories need, and the D4 check reads the config and
   imports nothing.
8. **The class fixture.** `enter_client_root(test, config)` registers its cleanups on a test.
   `_FullStores.setUpClass` needs them on the class: add the class-level variant beside it in
   `client_fixtures.py` (a cleanup argument, or a function of its own, using
   `cls.addClassCleanup`), changing nothing else there but the default config. IMPLEMENTATION
   CHOICE, logged.
9. **What the ported literals assume of the neutral store.**
   - `FIXED_TIMESTAMP` is SGK's, `datetime(2026, 9, 24, 12, 0, 0)`.
     `test_no_timestamp_is_in_any_record` checks the literal `"2026-09-24"`, and
     `test_adding_a_tag_to_one_record` inserts `'2026-09-24 12:00:00.000000'`; under another date
     the first would check nothing.
   - `build_full_store(directory, stem="store")`'s shard 1 is `store-shard0001.sqlite`, a literal of
     `test_a_difference_exits_one`; `shard_file_name` gives exactly that.
   - **`shard_keys`.** SGK writes them into the primary through a private table
     (`pool._shard_key_table`, `real_store_fixtures.py:217-238`). `read_inventory` reads the
     primary's `shards` and `replicated_tables` and the shards' own tables (`store_reader.py`).
     The neutral `build_full_store` accepts `shard_keys`, checks each names an existing shard, and
     either writes them nowhere or into a table of its own, by `sqlite3`; either way logged.
     `relabel_serials` relabels the keys as SGK's does (`:1322-1324`).
   - **Labels.** `TestNotContent` relabels only classes in `COMPUTE_TARGETS ∪ {"BackgroundModel"}`
     that have a `label` column. A `label` that is identity (the tag table's, the version table's)
     must be on no class of that set. Every row has a `timestamp`, and at least one solver column
     exists, or `changed`'s three counts are not all positive.
   - **`TestFormats`** compares two hand-built fingerprints that both lack `encoding_format`.
     DatastoreKit's comparison reads an absent key as `None` on both sides
     (`store_fingerprint.py:210-212`), so both tests pass unchanged through the shim. Measured by
     reading; the suite confirms it.
   - The test module keeps `QSI`, `TKN`, `COMPUTE_TARGETS` and `SOLVER_COLUMNS` as its own
     module-level names, at their places, with neutral values (literal, or bound to the neutral
     store's exports): IMPLEMENTATION CHOICE, logged, and §2.8's port script maps them accordingly.
10. **The suite will take longer.** It was 39.1 s at `2ecb99d`. Each CLI child that loads the
    fingerprinter imports `ray` (about a second or more), and every ported test case builds a
    client root (about 117 ms). Not a stop; record the time seen.

**The facts, checked by the orchestrator on 2026-10-15 at `2ecb99d`.** Pass them on.
- **In-repository state.** `main` at `2ecb99d`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`.
  `venv/`: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit` at
  `c8570e8` (`v0.4.0`), `runregistrykit` editable; `git` 2.56.0.
- **The suite at `2ecb99d`:** `Ran 135 tests in 39.1s`, OK.
- **The prompt's line numbers** hold at `2ecb99d` (its package files are `035e4b5`'s): the module
  docstring's fingerprint row `stores.py:32-35` and paragraph `:106-115`; `FINGERPRINT_FORMAT`'s
  history `:190-201`, the constant `:202`, `TAKEN_KEYS` `:203`; `_fingerprint_problems`
  `:412-432`; `_registry_problems` `:573`, its `bool` guard `:578`, `_STORE_ID.fullmatch` `:588`;
  layer C `:1180-1427`; `write_listing` `:1456-1462` (no `client_root` yet); `fingerprint_store`
  `:1473-1586`, its import `:1524-1525`, the `malformed` entry `:1547-1558`; `__main__`: `_show`
  `:136-182`, `_print_fingerprint` `:274-294` (`classes:` from `:277`), `_fingerprint`
  `:297-344`; `Run.finish` and `_fingerprint_results` `__init__.py:383-446`. `hashlib` and
  `Counter` are used only in layer C (`:1194`, `:1243`, `:1257`), so both imports go.
- **Where each store operation locates** (`find_client_root` at entry, at `2ecb99d`):
  `create_sidecar` `:807`, `adopt_sidecar` `:858`, `copy_store` `:1109`, `move_store` `:1147`,
  `fingerprint_store` `:1498`, `retire_store` `:1779`, `amend_sidecar` `:2151`. `write_listing`
  does not locate; §2.5 gives it `client_root=`. The D4 check goes right after each locate.
- **SGK's module** at `a45aefc` (875 lines): 33 tests, `TestGolden` 3 and `TestDrivers` 1 dropped,
  29 left, as §2.8 counts. Its SGK names: `QSI`, `TKN`, `COMPUTE_TARGETS` (9 classes),
  `SOLVER_COLUMNS` (3), `"BackgroundModel"`, `"TkNumericValue"`, and `_factories`; the two U7
  variants at `:504-505`. `_FullStores.setUpClass` `:141-147`.
- **DatastoreKit `v0.4.0`:** `fingerprint_of(inventory, fingerprint_format, taken=None)` refuses a
  `bool` or non-`int` format with `TypeError` and one below 1 with `ValueError`, before reading;
  `compare_fingerprints` gives `format` then `encoding` entries and stops there if either differs;
  `listing_lines` writes `# fingerprint_format <f> digest <d> encoding_format <e>`;
  `InventorySpec(leaves, parents, tags, values, validated, parent_sets)`, `Parent(column, of,
  type_column, types, nullable, cross_shard)`, `ParentSet(table, owner, members)`.
  `read_inventory` imports `store_reader`, which imports `ShardedPool`, so it loads `ray`
  (uninitialised).
- **The deletion grep of §3.4** finds, at `2ecb99d`, `stores.py:202, 1192, 1201, 1210, 1213, 1233,
  1238, 1240, 1248, 1255, 1284, 1404, 1421, 1484, 1525`; after 04a it must find only the test
  module's shim and `neutral_store.py`'s own names (correction 3 for `:1484`).
- **No `runregistrykit.toml`** above this checkout or the session scratchpad.
- **The index.** **7** open now; **4** after, unless the work opens one.
- **Ray.** No Ray process; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** §6's list as this section's "What moves on purpose" reads it; `runregistrykit/`
  gains exactly `fingerprint.py`, `tests/neutral_store.py`, `tests/test_store_fingerprint.py` and
  `tests/test_fingerprinter.py`.
- **(E2) The port.** An independent re-port of SGK's module differs from the committed one only by
  the shim lines, the F-client lines and the two U7 variants; the test ids are SGK's 29.
- **(E3) The neutral store.** Public `datastorekit` names only; no Ray; what every ported assertion
  counts.
- **(E4) The behaviour,** by reading and by probing: the protocol and the shipped fingerprinter;
  the loader and its refusals; the config key; D4 before anything is read, and nothing imported by
  it; layer C and the format gone; `fingerprint_store`'s order and texts; U7's reader; the CLI.
- **(E5) The suite.** 135 + 29 + N pass, write nothing outside `tempfile` directories, start no Ray.
- **(E6) The mutations.** (m1)–(m10) each fail a named test, and the orchestrator's own as §3 says.
- **(E7) The records.** The log, the board (three closed), the index (4), `prompts/INDEX.md`,
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
  replay in `bash`, not zsh. None is committed. After each, `git status` must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`.
  Python's `tempfile` in tests is fine. **No scratch `.py` goes under `runregistrykit/` or
  `docs/`**, even for a moment: discovery walks the one and `black` the other. The port script
  (§2.8) lives in the scratchpad. Scratch client roots and stores go in the scratchpad or a
  `tempfile` directory, never inside this checkout.
- **SGK is read only** through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show a45aefc:<path>`,
  for the two files of the prompt's "Read first" item 6. ChamPBH and SI are not read. No client
  is run.
- **Install nothing.** The venv is as 01 left it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A ported test that fails is a stop, never an edit outside §2.8's
  classes; a mutation no test catches is a stop, never a weakened mutation.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` at the root.
2. **The prompt's gate**, as correction 1: the diff from `2ecb99d` empty; the suite 135.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 7 now, 4 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, 03's log, `docs/OPEN_ISSUES.md`, `CLAUDE.md` and
  `PROVENANCE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and the two recommendations
of corrections 4 and 5 (a text-and-type check against the reader's own exception, with a
`StoreSchemaMismatch` case; a refusal-precedence test with an unimportable fingerprinter).

Tell it plainly:
- **One commit, at the end.** Its log is `logs/04a-the-client-fingerprinter.md`, in README §5.1's
  form, with the prompt's §4.3 additions.
- **The files it may add or change are §0's "What moves on purpose", and nothing else.** In
  particular it must not touch `runregistrykit/__init__.py`, `pyproject.toml`, `README.md`,
  `LICENSE`, `.gitignore`, `.idea/`, `CLAUDE.md`, `docs/extraction/`, `tests/__init__.py`,
  `store_fixtures.py`, `shard_store_fixtures.py`, any other 02 or 03 test file, the campaign
  README, the prompt, or anything under `orchestrator/`.
- **It edits no client repository, DatastoreKit or RayPoolKit; it reads SGK only as §0 says, and
  ChamPBH and SI not at all.**
- **It installs nothing, reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list, the log and the records. `git
   diff 2ecb99d <commit> --` `runregistrykit/__init__.py pyproject.toml README.md LICENSE
   .gitignore CLAUDE.md docs/extraction runregistrykit/tests/__init__.py` and every 02 test file and
   fixture but `client_fixtures.py` is empty. `git ls-files runregistrykit` is 03's sixteen and the
   four new files. `test_package_imports.py` changes in `MODULES` only; `test_client_root.py` in
   correction 2's two tests only; `client_fixtures.py` in its default config and the class-level
   variant only. No `venv/`, `*.egg-info`, scratch file or `var/`.
2. **E4, by reading.**
   - `fingerprint.py` in full: standard library only at module scope; the runtime-checkable
     protocol's four methods; `DatastoreKitFingerprinter`'s constructor refusals; `take`,
     `compare`, `listing` as DatastoreKit's functions, `take` returning `(fingerprint, inventory)`
     and letting the reader's exception through untouched; `describe` the old
     `_print_fingerprint` text from `classes:` on, line for line (diff it against `035e4b5`'s
     `__main__.py:277-294`), `main.py --inventory` included; `load_fingerprinter`'s refusals, each a
     `ConfigError` naming the config file and the spec, and `found` put on `sys.path` only if
     absent.
   - `client.py`: `[stores]` holds `fingerprinter` only; its form checked at read time; the
     docstring documents it and no longer calls the table reserved.
   - `stores.py`: layer C, `FINGERPRINT_FORMAT`, `hashlib`, `Counter` gone; `TAKEN_KEYS` kept; the
     D4 check right after each of the seven locates and in `write_listing`, before any read, and
     importing nothing; `fingerprint_store` as §2.5: step 1's code and texts unchanged (diff
     against `035e4b5`), the loader after them, `taken` then `take`, the `malformed` entry's six
     keys and text unchanged, the return keys unchanged; `_fingerprint_problems` as §2.6. **U7 by
     walk:** outside `fingerprint.py`, no package module subscripts or `.get`s a fingerprint's
     `classes`, `tag_sets` or `problems` (grep the three words in `stores.py` and `__main__.py`
     and read each hit).
   - `__main__.py`: `store show` loads no fingerprinter; `_print_fingerprint` prints `digest:`,
     `format:`, then `describe`; `_fingerprint` loads the fingerprinter after `fingerprint_store`
     (correction 5), and passes `client_root` to `write_listing`.
   - The module docstring of `stores.py` says what is now true at `:32-35` and its fingerprint
     paragraph, and nothing else in it changed.
3. **E2, the port, independently.** Export SGK's module from `a45aefc` into the scratchpad and
   write a re-port of the orchestrator's own: D-name; X-drop (the two classes, `GOLDEN`, `DRIVERS`,
   `REPO_ROOT`, `_HANDLERS`, `_finish_calls`, `import ast`, the docstring's items 4 and 12 as the
   log says it treated them); N-fix (the imports); N-class from the log's mapping table; then
   `black`. `diff` it against the committed file: every hunk is a shim line, an F-client line or one
   of the two variants. The loader's test ids are SGK's 29, by class as §2.8 counts.
4. **E3, the neutral store.** Read `neutral_store.py` in full: every `datastorekit` import public,
   no `_`-attribute of a `datastorekit` object, no `ShardedPool` constructed, no Ray; the content
   §2.7 lists; the exports with SGK's signatures; `FIXED_TIMESTAMP` SGK's (correction 9). Build its
   store in the scratchpad: `read_inventory` gives `problems` none; `QSI` tag sets
   `[Run_fixture]` ×2 and `[Run_fixture, grid-A]` ×1, serial 3 on shard 1; `TKN` serial 3 on shard
   0 unvalidated; the value row 24 on shard 1; with `shards=4`, `closed_store_files` lists 5 files
   and `delete_store` removes them. And 04b's three edits (delete `QSI` serial 3 on shard 1; insert
   a `QSI` tag row with `parent_serial` 999, `tag_serial` 3) build without error.
5. **E4, by probing**, in the scratchpad, with this checkout's venv, never inside the repository:
   - **A client of its own.** A scratch client root, a git repository, whose config names
     `fp.client:FINGERPRINTER`, a module of that root, not otherwise on `sys.path`, making
     `DatastoreKitFingerprinter(neutral_store.FACTORIES, 7)`. From a subdirectory: a neutral store
     created with `store create`; `begin(results=…)`, `finish("done", fingerprint=True)`: the status
     and the sidecar hold one fingerprint, format 7, `encoding_format` 1, `taken.run_id` the run's;
     `store fingerprint` exits 0 and says it matches; `--listing` writes a file whose first line has
     `encoding_format 1` as word 6; `store show` exits 0 and its child loads neither `ray` nor
     `sqlalchemy`.
   - **U7: fingerprints already written.** Into that store's sidecar, a hand-built SGK-shaped
     fingerprint (format 6, `classes`, `problems`, `taken`, no `encoding_format`): `store show`
     reads it with problems none; `store fingerprint` exits 1 with a `format` entry and no content
     entry (DatastoreKit stops at the versions). Then the same with `classes` removed: still no
     problem. Then `encoding_format: "1"`: a problem naming `encoding_format`.
   - **D4.** The same root with `[stores]` removed: `store show`, `create`, `adopt`, `copy`,
     `move`, `fingerprint`, `retire`, `amend` each exit 1 with `!!` and the `ConfigError` naming the
     config file, and the store directory and the sidecar are byte-identical before and after; `list`
     and `begin` are not refused; `finish(fingerprint=True)` records `ConfigError: …` as
     `fingerprint_error` and ends the run.
   - **The loader's refusals.** A spec of the wrong form, a module that cannot be imported, a
     missing attribute, an object that is not a `Fingerprinter`: each a `ConfigError` naming the
     file and the spec; the form refused at read time, the others only when a fingerprint is
     taken.
6. **E5, the suite.** The prompt's §3.1 command: `Ran 135 + 29 + N tests … OK`, the per-module
   counts the log's, the time recorded. `git status --short --ignored` the same before and after but
   for `__pycache__/`; no `var/`; this checkout the only worktree; no Ray process before or after.
   §3.3's import check and §3.4's grep, as the prompt gives them, the grep's hits as the log lists.
   `./venv/bin/black --check runregistrykit docs` is clean.
7. **E6, the mutations.** Replay (m1)–(m10) from the log, one at a time, in `bash`; each fails the
   tests the log names; the suite OK after each; the tree clean. Then the orchestrator's own, not
   in the log:
   - (o1) `create_sidecar`'s D4 check replaced by `load_fingerprinter(client)`: must fail (a
     `create` child loads `ray`);
   - (o2) `_fingerprint_problems` without the `bool` guard on `encoding_format`: must fail;
   - (o3) `load_fingerprinter` without its `isinstance(…, Fingerprinter)` check: must fail;
   - (o4) `client.py` accepting any other `[stores]` key: must fail (correction 2a);
   - (o5) `client.py` accepting a `fingerprinter` with no colon: must fail;
   - (o6) `DatastoreKitFingerprinter.take` passing `taken=None` to `fingerprint_of`: must fail;
   - (o7) `DatastoreKitFingerprinter(…, True)` accepted: must fail;
   - (o8) `neutral_store.py` gaining `from datastorekit.SQL.ShardedPool import ShardedPool` and a
     call of `ShardedPool._journal_paths`: must fail the `ast` walk.
   An uncaught (o) mutation is opened on the board (owner to be put to the user), not a stop.
8. **The issues.** The three closed in §4, each with this commit, what resolved it and the tests
   that pin it; their rows gone from the index. `[02-the-ported-tests-name-sgk]` gains the port's
   lines (the kept method `test_deleting_one_quadsourceintegral_row`, the docstrings citing SGK's
   campaigns). The other three carry their 04a package lines; spot-check each in the package at
   the commit, `[00-a-refusal-matches-datastorekit-message-text]`'s `stores.py` lines among them.
9. **E7, the records.**
   - The log has every section of README §5.1; the mapping table; every D-name, X-drop, N-fix,
     N-class, F-client and U7 instance accounted for; correction 2's two tests; the port script's
     summary; 135 → 135 + 29 + N with the per-module counts and the time; every mutation as a diff,
     with the tests that fail it; the deviations classified (corrections 1–3 among them).
   - `PROVENANCE.md`: "Since the import" gains 04a's section (the fingerprinter and its key; layer C
     and `FINGERPRINT_FORMAT` deleted, with SGK's lines and DatastoreKit's release; U7; the neutral
     store); the file map's two rows as §4.3.
   - The board: the header; 04a's row (landed, "this commit", 135 → …); F1, F2 and T2a ✅; §3 and
     §4 as above. `prompts/INDEX.md`'s row says 04a landed. The index counts 4 by counting (or more,
     each opened issue on the board), matching its header and date.
10. **The interface.** No record changes form but the fingerprint's own content: the manifest's,
    `status.json`'s, `checkpoint.jsonl`'s and the sidecar's keys are those at `2ecb99d` (from the
    diff, and from the probe's records in check 5); `taken`'s keys are `TAKEN_KEYS`; the
    fingerprint gains `encoding_format`; the tombstone's `fingerprint` condition is untouched.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 04a* paragraph, in the form of
  03's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md` and in
    `PROVENANCE.md`;
  - "reviewed" for 04a in the board's header and row, README §2's status column and its header,
    and `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 04a";
  - 03's residue: the board's §4 `[00-the-recorded-distributions-are-sgks]` still reads "Closed:
    2026-10-14, by 03 (this commit)"; it becomes `035e4b5`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 135 → 135 + 29 + N;
  - the protocol, the shipped fingerprinter and the config key as built, and what a client must
    now have (`[stores] fingerprinter`; without it every store operation is refused);
  - U7: fingerprints already written read as they did;
  - the neutral store, and what 04b will need of it;
  - the mutations, the agent's and the orchestrator's, and what is not pinned;
  - the three issues closed, and anything opened;
  - that 04b can now be written, against the tree 04a left;
  - and whether to push `main`.
