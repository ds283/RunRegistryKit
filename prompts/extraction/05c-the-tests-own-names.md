# Prompt 05c — the tests' own names

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 05b has landed (`1120fb3`) and been reviewed (`8766714`, the board's §1). `git diff --stat 8766714
  HEAD -- runregistrykit docs/extraction pyproject.toml PROVENANCE.md CLAUDE.md README.md` is empty.
- U16 is taken (README §6.2, 2026-10-15): from this prompt, a ported test's module, class, method or
  helper name that names a client may be renamed, each rename mapped in `PROVENANCE.md`; what it
  asserts is kept (README §5 rule 9).
- The suite is `Ran 276 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[02-the-ported-tests-name-sgk]`. **Opens:** only what the work finds.

**Recommended model:** **Sonnet**. The work is renames under a fixed map, fixture data made
neutral, and about eighty lines of test docstrings and comments, under rules this prompt states. The
renames were trialled at writing: the suite passes with them, the guard aside (§"At writing").

**Read first:**

1. [`README.md`](README.md): §0.2, §2 (05a, 05b, 05c, 06), §4, §5 (all of it; rules 4, 6, 9 and 10
   especially), §6.2 (U10, U16, U17).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §3's `[02-the-ported-tests-name-sgk]` in
   full, and §1's reviews of 05a and 05b.
3. [`logs/05a-the-guard-and-the-public-names.md`](logs/05a-the-guard-and-the-public-names.md), "How
   `known_hits.json` was written" (the writer's text), and
   [`logs/05b-the-package-prose-and-the-rules.md`](logs/05b-the-package-prose-and-the-rules.md),
   "Observations not acted on" and "State handed to the next prompt".
4. `runregistrykit/tests/test_package_is_generic.py` in full, and
   `runregistrykit/tests/data/known_hits.json`.
5. Every test module and fixture under `runregistrykit/tests/` but the guard and
   `test_public_names.py`, which name nothing of a client: their docstrings and comments above all,
   and `store_fixtures.py`, `shard_store_fixtures.py` and `neutral_store.py` in full.
6. `PROVENANCE.md` ("Since the import", and 05b's "Where the prose's citations pointed"),
   `README.md` and `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

No client is read: everything this prompt needs of SGK is in the tests' own text, which names it.
Line numbers below are the tests' at `8766714`, which are `1120fb3`'s.

---

## 1. What is wanted

The ported tests still speak their first client's language: its store stems and run names, its
classes and tables in the fixtures, its helper and class names (`a3_shaped`, `TestLiveA3Shape`), its
campaigns, prompts, decisions, issue tags and incidents in their docstrings and comments. 02 and 04
kept them so that the port could be traced to SGK line by line (README §5 rule 9); the port is
complete and reviewed, and U16 lifts the rule for names. This prompt makes the tests the package's
own, so that the guard's known hits are empty and the package and its tests name no client.

- **Names** that name a client are renamed by §2.2's map: helpers, a class, six test methods,
  constants and the neutral store's three shared columns. Every rename is mapped in `PROVENANCE.md`.
- **Fixture data** that names a client is made neutral, keeping its shape (§2.3).
- **`test_package_imports.py`'s `FORBIDDEN`** names the clients' packages by reading the
  vocabulary, not by writing three of them (§2.4).
- **The tests' prose** is rewritten in the package's own terms, keeping what each test checks and
  why (§2.5).
- **`known_hits.json`** is empty in every scan, and the guard's docstring says so (§2.6).

**No assertion changes.** Every test keeps what it asserts; the only differences in a test body are
the renamed names and the neutral data, used consistently. The suite's count stays 276.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit`
`v0.4.0` (`c8570e8`), `runregistrykit` editable, `git` 2.56.0. **Install nothing.**

### 2.2 The renames

Each old name is replaced everywhere it occurs under `runregistrykit/tests/` (definition, imports,
uses, and the prose that names it), and nowhere else. Each new name was checked at writing against
the guard's forbidden words, whole and split on `_` and `-`.

| Old | New | Where it is defined | Why it names a client |
|---|---|---|---|
| `a3_shaped` | `hand_written_shaped` | `store_fixtures.py:37` | SGK's A3 store |
| `sweep_shaped` | `script_written_shaped` | `store_fixtures.py:86` | SGK's sweep script |
| `TestLiveA3Shape` | `TestHandWrittenShape` | `test_store_amend.py:205` | SGK's live A3 sidecar |
| `test_amend_backup_as_prompt_05_will` | `test_amend_backup_once_it_is_retired` | `test_store_amend.py:206` | an SGK campaign's prompt |
| `test_a_sweep_shaped_legacy_sidecar` | `test_a_script_written_shaped_legacy_sidecar` | `test_store_sidecar.py:349` | follows `sweep_shaped` |
| `test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file` | `test_a_torn_line_is_tolerated_only_at_the_end_of_the_file` | `test_run_registry.py:566` | `tolerance` is an SGK registry key (a code name is checked split on `_`) |
| `test_deleting_one_quadsourceintegral_row` | `test_deleting_one_integral_row` | `test_store_fingerprint.py:218` | SGK's class |
| `test_timestamps_labels_and_solver_serials` | `test_timestamps_labels_and_producer_serials` | `test_store_fingerprint.py:296` | follows `solver_serial` |
| `QSI` | `INTEGRAL_CLASS` | `test_store_fingerprint.py:68`, `test_store_retire.py:64` | SGK's abbreviation of its class |
| `TKN` | `SOLUTION_CLASS` | `test_store_fingerprint.py:69` | SGK's abbreviation of its class |
| the column `solver_serial` (and `SOLVER_COLUMNS`' value) | `producer_serial` | `neutral_store.py:80, 94` | a column of the clients' |
| the column `parent_serial` | `tagged_serial` | `neutral_store.py:243, 254` | a column of the clients' |
| the column `log10_tol` (and `_solution`'s parameter) | `log10_step` | `neutral_store.py:179, 188, 282` | a column of the clients' |

`SOLVER_COLUMNS` keeps its name (the guard does not flag it, and it says what the column is for);
its value changes with the column, in `neutral_store.py:80` and `test_store_fingerprint.py:70`
alike. The raw SQL that names a renamed column (`test_store_fingerprint.py:224, 254`;
`test_store_retire.py:465, 479`) changes with it. **Nothing else is renamed**: a name the guard does
not flag and that names no client stays.

### 2.3 Fixture data made neutral

Data in a fixture or a test that names a client is replaced by neutral data of the **same shape**:
the same keys, the same JSON types, the same nesting, paths with the same number of components and
the same relative or absolute form, strings with the same hyphens, dots, capitals and digits where a
test could depend on them. Timestamps and digests in data stay (a date in data is not an
incident). Found at writing:

- `shard_store_fixtures.py:25-27`: `KEY_TYPE = "mode"`, `REPLICATED = ["version", "mode"]`, `SHARDED
  = {"Solution": "k"}` (the neutral store's names; these are only names written into a primary's
  metadata, and no table of that name is created).
- `store_fixtures.py`, `hand_written_shaped`'s values: `purpose` without "census"; `grid_criterion`
  without "prompt 15"; `driver` as `docs/example/driver.py (NOT the other copy)`; `scope` without
  SGK's physics; `status_files` under `var/runs/pilot-run/`; `stages_complete` without
  `GKSOURCE`. `script_written_shaped`'s values likewise. Every key stays.
- `test_store_sidecar.py:36, 43`: the stems `handover-A3-baseline-lambdacdm` and
  `handover-atol-sweep` become `example-B2-baseline-run` and `example-working-copy` (each keeps
  hyphens; the first a capital and a digit).
- `test_run_registry.py:105, 129`: `campaign="run-registry"` becomes `campaign="example"`; `:687-713`:
  the directory `a3-pilot` becomes `pilot-run`, at every use.
- `test_store_fingerprint.py:420`: the run id `store-fingerprint-04-test-20260925T100000` becomes
  `example-04-test-20260925T100000` (the guard does not see a campaign inside a longer hyphenated
  word, so it is listed here).

### 2.4 `test_package_imports.py`'s `FORBIDDEN`

`FORBIDDEN` (`:26-34`) names three SGK packages, `ObjectFactories`, `StoreFixtures` and
`RunRegistry`, beside `ray`, `sqlalchemy`, `datastorekit` and `config`. Replace the three by the
clients' project packages as the guard defines them, `test_package_is_generic.project_packages()`,
read from the vocabulary file (18 names at writing, the three among them): the check is then the
same for every client, and the module names none. `config` and the three heavy packages stay as
they are. The comment above `FORBIDDEN` says where the names come from. Import the guard's function
rather than restating its rule. This asserts more than before (eighteen packages for three), never
less; the log says so.

### 2.5 The tests' prose

Every docstring and comment under `runregistrykit/tests/` that names or cites a client is rewritten
in the package's own terms. **The guard is the floor, not the ceiling**: when its known hits are
empty, these must be gone too:
- a client's name, script, driver, store, table, class, run or abbreviation (`A3`, the backup "of
  A3", `quadsource_atol_sweep.py`, `scoped_pipeline_run.py`, `prepare()` as a client script's,
  `QSI`, "the audit tool or the sweep script's check");
- a campaign, a prompt, a section, a property or test number, a log, a decision or an issue of any
  repository, this one's included (`prompts/…`, "prompt 03 §2 P11 and §3 tests 5-8", "Test 1:",
  "P12:", "the log's interruption table", `D4`, `U14`, `Q3`, `[10-…]`), and an incident's date
  ("the 2026-09-23 failure");
- a name that no longer exists: `runregistrykit.stores.fingerprint_of` (`test_store_fingerprint.py:1`)
  and "real multi-shard fixture stores" where the stores are the neutral store's
  (`test_store_retire.py:18`, `test_store_retire_references.py:18`).

The rules of the rewrite are 05b's §2.3, for tests:
1. **Keep what each test checks and why.** A docstring that numbered a test after another
   repository's prompt ("Test 3: …") keeps its description and drops the number. A reason given by
   an incident is stated in general terms ("a store whose `shards` rows are absolute paths to
   another store's files").
2. **Keep every fact.** A comment that explains an assertion keeps explaining it.
3. **What may be named:** the package's names; DatastoreKit's public names, and the private
   `ShardedPool` attributes the carried fixture uses (they are the fixture's subject,
   `[00-the-shard-fixtures-reach-into-shardedpool]`); this repository's `README.md` by section name
   and `PROVENANCE.md`; the manifest's and the sidecar's keys; the renamed names of §2.2.
4. **No code changes** but §2.2, §2.3 and §2.4.
5. **Width.** Lines within 100 columns, and no paragraph broken mid-sentence; `black` on every file
   changed.

### 2.6 `known_hits.json` and the guard's docstring

Rewritten by 05a's writer, never by hand: delete the file and run the writer whose text 05a's log
gives, from the session scratchpad (never under `runregistrykit/` or `docs/`), once every test file
is final. **One change to the writer:** its `owners` string, which named 05b's and 05c's shares,
becomes a statement that no hit is known: for example, "none: the package and its tests hold no
known hit, and a hit in any file fails its scan". The log gives the writer's text and the diff of
the file. Expected: **every scan's list empty**.

The guard keeps its mechanism, as DatastoreKit's guard did when its list emptied: a scan must find
exactly its known hits, now none. Its module docstring's paragraph **"The known hits"** is
reworded to say that the list is empty and that a hit in any file fails its scan; the sentence on
whose entries are whose goes. **No other change to the guard**: no rule, word, allowance, test or
line of code.

### 2.7 `PROVENANCE.md`

"Since the import" gains 05c's section: the renames, the neutral data, `FORBIDDEN`, the prose, the
empty known hits. And two tables:
- **The renames**: every row of §2.2, with the test ids that changed (`module.Class.method`, old and
  new), so that a reader with SGK's tree can find each test's source.
- **Where the tests' citations pointed**: one row per test module or fixture, the SGK records its
  docstrings and comments cited **as cited at `8766714`** (the text names them; no SGK file is read),
  and what the module now says it tests.

### 2.8 What else moves

Nothing: no package module, `client_vocabulary.json`, measuring script, `compare_with_source.py`,
`pyproject.toml`, `README.md` or `CLAUDE.md` changes. The board's package lines for the open issues
are re-read at this commit and recorded (§4.3).

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root: **`Ran 276
   tests … OK`**. Count by loader and give the per-module counts and the time; the counts equal
   05b's, module by module.
2. **Nothing outside temporary directories**: `git status --short --ignored` the same before and
   after a run (but `__pycache__/`); no `var/`; `git worktree list` this checkout alone; no Ray
   process before or after.
3. **The assertions are unchanged.** A script compares, for each changed test module and fixture,
   `ast.dump` with docstrings removed at `8766714` and at the commit, after applying §2.2's map to
   the old tree's names and §2.3's replacements to its string constants: equal for every file but
   `test_package_imports.py`, whose one difference is `FORBIDDEN`. The log gives the script and its
   output. The test ids, old and new, by loader: the same 276 but the six renamed methods and the
   methods of the renamed class, each mapped.
4. **The prose, by the guard and by grep.** The guard's scans find nothing in any file. Then, over
   the docstrings and comments of every file under `runregistrykit/tests/` but the guard, a
   case-insensitive grep for `prompt`, `campaign`, `README`, `CLAUDE`, `log's`, `\bA3\b`, `a3`,
   `sweep`, `handover`, `quadsource`, `scoped_pipeline`, `QSI`, `TKN`, `GkSource`, `wavenumber`,
   `census`, `\bP[0-9]+\b`, `\btest [0-9]+\b`, `2026-` and `§`: every line it finds is listed in the
   log with why it stays (a manifest key, a parameter, a date in data, a name of §2.2, a reason in
   general terms), or it is rewritten. And over the whole of each file, code included, the grep for
   `a3`, `QSI`, `TKN`, `GkSource`, `wavenumber`, `quadsource`, `handover`, `run-registry` and
   `store-fingerprint` finds nothing.
5. **The known hits.** The file as §2.6 says, its diff in the log; every list empty.
6. **The tests catch behaviour** (README §5 rule 10). Each mutation is applied, the suite run, then
   reverted, and recorded as a diff with the tests that fail:
   - (m1) `TestLiveA3Shape = TestHandWrittenShape` added after the renamed class;
   - (m2) one renamed column reverted in `neutral_store.py` alone (`tagged_serial` back to its old
     name in the spec and the table): the raw SQL of the tests no longer matches;
   - (m3) `(D4)` added to a comment of `test_store_retire.py`;
   - (m4) one old entry restored to `known_hits.json` (`runregistrykit/tests/store_fixtures.py`,
     `a3_shaped`, 1, under `test_no_code_name`);
   - (m5) `FORBIDDEN` with a package that the child interpreter does load (for example `json`)
     added: the import test fails, so the check of `FORBIDDEN` against `sys.modules` still runs;
   - (m6) the agent's own, of a renamed fixture's data.

   Each must fail at least one test. A mutation no test catches is a **stop**.
7. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2's changes are in. Under `runregistrykit/` only test modules, fixtures, the guard's docstring
   and `known_hits.json` change; no file is added or removed. `PROVENANCE.md` changes as §2.7 says.
2. §3.1–§3.7 hold. `known_hits.json` has no entry in any scan.
3. **The records**, in the same commit:
   - the log, `logs/05c-the-tests-own-names.md`, per README §5.1. It holds: the rename map as
     applied, with every site count; the neutral data, old and new; the per-scan totals before (155
     in 94) and after (0); the writer, its one difference and the file's diff; §3.3's script and
     output; §3.4's grep and its accounting; the suite before (276) and after, with the test ids
     mapped; every mutation as a diff;
   - this board: the header, §1's row for 05c, §1.1's T3, §3 (`[02-the-ported-tests-name-sgk]`
     closed into §4 with this commit and what resolved it; the other two open issues with *Package
     lines (05c, …)*, the carried fixture's among them);
   - `docs/OPEN_ISSUES.md`: the row deleted, the count 2, the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `PROVENANCE.md`: §2.7.

---

## 5. Stop conditions — stop and ask the user

- A test would need to assert something different, or fails after a rename for a reason other than
  the guard's known hits.
- The suite's count changes, or a module's count changes.
- A hit cannot be removed without changing an assertion, or a reason the old prose gave cannot be
  stated without naming a client.
- A word rule, package word or allowance would be needed for a scan to pass, or any change to the
  guard beyond §2.6's paragraph.
- A name of §2.2's map turns out to be a forbidden word or to collide with an existing name.
- A mutation of §3.6 is caught by no test.
- Any record would change form (README §5 rule 7), or a package module would need to change.
- The suite needs a Ray cluster, starts Ray, imports a client, writes outside a `tempfile`
  directory, or leaves a worktree registered here.
- Anything would require editing, running or reading SGK, ChamPBH, StochasticInstantons,
  DatastoreKit or RayPoolKit, or installing anything.

---

## 6. What this prompt does not do

- **Files it changes:** the test modules and fixtures under `runregistrykit/tests/` that hold a
  client's name, data or citation (§2.2–§2.5); the guard's module docstring (§2.6);
  `runregistrykit/tests/data/known_hits.json`; `PROVENANCE.md`; the log, this board,
  `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It changes no package module, no assertion, no guard rule, `client_vocabulary.json`, the
  measuring script, `pyproject.toml`, `README.md` or `CLAUDE.md`.
- It does not touch the carried fixture's private `ShardedPool` attributes
  (`[00-the-shard-fixtures-reach-into-shardedpool]`, owner none).
- It adds no CI and makes no tag.

---

## 7. The log and the board

`logs/05c-the-tests-own-names.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 05c, §1.1's T3, and §3 and §4 as §4.3.

---

## At writing (2026-10-15, at `8766714`)

Measured read-only, for the README's row and the orchestrator:
- **The tests' known hits** (the guard at 05b): **155 hits in 94 entries**: code names 29 (14),
  strings 67 (36), comments 1 (1), citations 58 (43), imports 0; in 14 test modules and fixtures;
  none in the guard or `test_public_names.py`.
- **A trial of §2.2–§2.4** in a clone of this repository at `8766714`, in the session scratchpad
  (the renames of §2.2; of §2.3's data the shard fixture's names, `driver`, `grid_criterion`,
  `stages_complete`, the `a3-pilot` paths, the run id, the campaign and the first stem, the second
  stem as `example-step-sweep`, and not `purpose` or `scope`; `FORBIDDEN` from `project_packages()`;
  no prose): 11 files, 110 lines in and 105 out; `Ran 276 tests in 90.9s`,
  with three failures only, the guard's `test_no_code_name`, `test_no_string_or_docstring` and
  `test_no_citation`, each because known hits are no longer found. After the trial the guard finds
  **75 hits, all in docstrings and comments**: strings 17 (15 entries), comments 1, citations 57
  (42); code names 0. No test pins a neutral-store digest, and `datastorekit` fixes none of the
  three column names (`datastorekit.contract` defines only `version`, `label`, `store_tag`,
  `tag_serial` and a private key).
- **The candidate names** of §2.2 and §2.3, checked against the guard's 454 forbidden words, whole
  and by their `_` and `-` parts: none forbidden. `test_tolerance_…` is flagged only because
  `tolerance` is an SGK registry key; renaming it is cheaper than a word allowance, which U10's
  rules do not provide.
- **`FORBIDDEN`'s three SGK names** are among the 18 project packages the guard derives
  (`ObjectFactories`, `StoreFixtures`, `RunRegistry`), so §2.4 asserts a superset.
- **Beyond the guard**, by grep: the run id `store-fingerprint-04-test-…`
  (`test_store_fingerprint.py:420`); `QSI` and `TKN` (`test_store_fingerprint.py:68-69`,
  `test_store_retire.py:64`, `test_fingerprinter.py:855-856`); the property and test numbers of
  SGK's prompts (`P9`–`P12`, "Test 1:" to "Test 11:" in `test_store_fingerprint.py`, "§3 test 2");
  "the log's interruption table" (`test_store_copy_move.py:350`, `test_store_retire.py:11, 528`);
  "the 2026-09-23 failure" (`test_store_retire.py:345`); "the audit tool or the sweep script's
  check" (`shard_store_fixtures.py:93`); "census" (`store_fixtures.py:45`); `prepare()` in
  `test_store_sidecar.py`'s stem comment; "real multi-shard fixture stores"
  (`test_store_retire.py:18`, `test_store_retire_references.py:18`); and
  `runregistrykit.stores.fingerprint_of` (`test_store_fingerprint.py:1`), a name the package no
  longer has. About eighty prose lines in all, with the guard's.
- **DatastoreKit's guard** (`b01737f`, `datastorekit/tests/test_layer_is_generic.py`) kept its
  known-hits mechanism with an empty list once its rewrite was done; §2.6 follows it.
