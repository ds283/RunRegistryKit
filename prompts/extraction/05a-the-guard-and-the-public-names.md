# Prompt 05a — the guard and the public names

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 04b has landed (`5302a6f`) and been reviewed (`dfcb884`, the board's §1). `git diff --stat dfcb884
  HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` is empty.
- U10, U11, U12, U15 and U16 are taken (README §6.2, 2026-10-15).
- The suite is `Ran 245 tests … OK`, and `git status` is clean in this repository.

**Closes:** nothing. **Narrows:** `[00-package-prose-names-sgk]` and `[02-the-ported-tests-name-sgk]`
(each hit they describe is now listed by the guard, by file and word, for 05b and 05c to remove).
**Opens:** only what the work finds.

**Recommended model:** **Sonnet**. The guard is DatastoreKit's, ported and adapted by rules this
prompt states. Its inputs were trial-measured at writing (§"At writing"), and nothing in the
package's behaviour changes except one name.

**Read first:**

1. [`README.md`](README.md): §0.2 (C8), §2 (05a, 05b and 05c), §4, §5 (all of it; rules 5, 6, 9 and
   10 especially), §6.2 (U10, U11, U12, U15, U16).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §3's `[00-package-prose-names-sgk]` and
   `[02-the-ported-tests-name-sgk]`, and §1's review of 04b.
3. [`logs/04b-the-retire-tests.md`](logs/04b-the-retire-tests.md): "Observations not acted on" and
   "State handed to the next prompt".
4. DatastoreKit's guard and its measuring script, through `git -C
   /Users/ds283/Documents/Code/DatastoreKit show b01737f:<path>` only:
   `datastorekit/tests/test_layer_is_generic.py` and `docs/extraction/measure_client_vocabulary.py`.
   They are the models for §2.2 and §2.3. Read `datastorekit/tests/data/client_vocabulary.json`
   for its form only; this prompt measures its own.
5. `runregistrykit/__init__.py` (`_slug`, `run_id`, the imports `:47-57`), the heads of
   `stores.py`, `client.py`, `fingerprint.py` and `__main__.py`, and
   `runregistrykit/tests/test_package_imports.py`.
6. `PROVENANCE.md`; `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers below are the package's at `dfcb884` (its package files are `5302a6f`'s).

---

## 1. What is wanted

`CLAUDE.md` says the package names no client, in code, strings, docstrings or comments, and that a
guard test enforces it. No such test exists yet. This prompt writes it, together with the two small
code-level decisions taken with it, U11 and U12. 05b and 05c then remove what it finds.

- **The vocabulary (U10)**, measured once from the three clients through `git` at fixed commits by
  a script, and held as data in the package's tests. The guard reads that file and never a
  client, so the suite runs with no client present.
- **The guard (U10, U16)** scans every Python file under `runregistrykit/`, its tests included. It
  has four word scans (code names, strings, comments, campaign citations) and an import rule. Each
  scan must find **exactly** its known hits, which are listed in a data file by file and word. A new
  hit fails, and so does a known hit that is no longer found. Today the list is long, about 210
  hits in all. 05b empties the package modules' share and 05c the tests'.
- **The public names (U11)**: `_slug` becomes `slug`, with no alias. Each of the five package modules
  declares `__all__`, pinned by a test.
- **The licence header (U12)**: the Apache 2.0 header RayPoolKit and the clients carry, on each of
  the five package modules, pinned by a test.

No prose is rewritten here (05b), and no test is renamed (05c). The only behaviour that changes is
the name `slug`.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit`
`v0.4.0` (`c8570e8`), `runregistrykit` editable, `git` 2.56.0. **Install nothing.**

### 2.2 The measuring script

`docs/extraction/measure_client_vocabulary.py`, modelled on DatastoreKit's. It uses the standard
library only and reads each client **only** through `git -C <repository> show`, `ls-tree`,
`rev-parse` and `cat-file -e`, at these commits. No client is imported, run or opened, and no
working tree is read (ChamPBH's has uncommitted changes, which must not matter):

| Client | Repository | Commit | Registry | Name | Factory directory | Campaigns |
|---|---|---|---|---|---|---|
| `SGK` | `SecondaryGWKit` | `14bcac0` | `config/datastore.py` | `factories` | `ObjectFactories` | `prompts` |
| `CPBH` | `ChamPBH` | `c21cdfb` | `config/datastore.py` | `factories` | `ObjectFactories` | `prompts` |
| `SI` | `StochasticInstantons` | `5fb4a1d` | `Datastore/SQL/Datastore.py` | `_factories` | `Datastore/SQL/ObjectFactories` | `.prompts` |

The script records the following for each client:
- the **commit**, in full;
- the **registry's keys**: the string keys of the dict literal assigned at module level to the
  registry's name, in the order written;
- the **columns**: the first argument of each `Column(…)` call (bare or as an attribute) whose first
  argument is a string literal, in every `.py` module of the factory directory, recursively, but
  `base.py` and `__init__.py`. They are sorted and unique, with the count of modules read;
- the **packages**: each top-level directory holding an `__init__.py`, sorted;
- the **campaigns**: the directory names directly under the campaigns directory, sorted.

Besides, under the key `listed`, it records the words that cannot be measured this way. Each comes
with where this repository's records name it:
- the clients' own names: `SecondaryGWKit`, `ChamPBH`, `StochasticInstantons`, `SGK`, `CPBH` (README
  §0; `SI` is not listed, being a common abbreviation);
- SGK's driver and store names that the package and its tests cite: `realistic_large_x`,
  `quadsource_atol_sweep`, `scoped_pipeline_run`, `handover-A3-baseline-lambdacdm`,
  `handover-atol-sweep`, `a3-pilot`, `A3` and `main.py` (`[00-package-prose-names-sgk]`,
  `[02-the-ported-tests-name-sgk]`);
- SGK's names as identifiers in the ported tests: `TestLiveA3Shape`, `a3_shaped`, `sweep_shaped`
  and `test_deleting_one_quadsourceintegral_row` (`[02-the-ported-tests-name-sgk]`).

The script writes `runregistrykit/tests/data/client_vocabulary.json`, or the path `--output`
names. It refuses to overwrite a file that exists (exit 1), exits 2 when it cannot read a client,
and exits 0 when it wrote the file. Two runs give the same bytes. The file holds the measurement and
a `summary` of counts, before any rule; which words are forbidden is the guard's business. `docs/`
is `black`-checked, so the script is `black`-clean. It is not a package module, so it carries no
header and is not scanned.

### 2.3 The guard

`runregistrykit/tests/test_package_is_generic.py`, ported from DatastoreKit's
`test_layer_is_generic.py` and adapted as follows. Its module docstring states what it scans, what
it forbids, what it allows and where the known hits live. **It is scanned too**, so it must state
its rules without containing a forbidden word or a citation. Build the citation pattern from
parts, and describe it in words.

- **The files.** `package_files()` returns every `*.py` under `runregistrykit/`, tests included, from
  the filesystem, with `__pycache__` skipped, sorted and relative to the repository root. A test pins
  that the derived set holds every `*.py` that `git ls-files runregistrykit` lists at this commit,
  so a derivation that came out empty or narrow fails.
- **The vocabulary.** `VOCABULARY` is `runregistrykit/tests/data/client_vocabulary.json`. The
  forbidden words are the union of:
  - the registries' keys;
  - the **identifier** columns: a column with an underscore, or with a capital and more than one
    character, as DatastoreKit's rule;
  - the packages, less `NOT_PROJECT_PACKAGES = {"config", "tools", "thirdparty", "plotting"}`
    (English words);
  - the campaigns;
  - the `listed` words;

  less `PACKAGE_WORDS`. These are the string values `datastorekit.contract` defines (`version`,
  `store_tag`, `tag_serial`, `label`), read from the module at run time, each with its reason. A
  test pins that the vocabulary is non-empty in each part (some named words of each kind present)
  and that no package word is forbidden.
- **A word.** In a string or comment, a word is a match of
  `[A-Za-z_][A-Za-z0-9_]*(?:[.-][A-Za-z0-9_]+)*`. It is checked whole, each of its dot-separated
  parts, and, when it has a hyphen, each of its hyphen-separated parts. So `docs/handover/x.py`
  finds `handover`, and `handover-A3-baseline-lambdacdm` finds itself, `handover` and `A3`. A code
  name is checked whole and split on `_`, as DatastoreKit's.
- **The scans.** Each is a test method that reports `file:line word` for every hit in every file:
  - `test_no_code_name`: names, attributes, definitions, arguments, keywords and imported names;
  - `test_no_string_or_docstring`: every string constant, docstrings and f-string text included;
  - `test_no_comment`: every comment, by `tokenize`;
  - `test_no_citation`: in strings and comments, a path under a `prompts` directory (the
    directory name followed by `/`), the word `prompt` or `prompts` followed by a space and two
    digits, or `§` followed by a digit (optionally after a space). The package's history lives in
    `PROVENANCE.md` and the campaign's records, not in its prose;
  - `test_every_import_is_allowed`: for the five package modules, the standard library
    (`sys.stdlib_module_names`) and `runregistrykit` anywhere, and `datastorekit` only inside a
    function body of `stores.py` or `fingerprint.py`. For the tests, the standard library,
    `runregistrykit`, `datastorekit`, `sqlalchemy` and `ray`. Nothing else, and no client
    package anywhere. `test_the_allow_list` pins the rule both ways, without a mutation.
- **The known hits.** `runregistrykit/tests/data/known_hits.json` is a data file, not a constant
  in the guard, because the guard scans itself. For each scan it lists entries `[file, word,
  count]`, sorted, and each scan's hits, counted by file and word, must equal its entries exactly.
  Counts by file and word, not by line, so that 05b and 05c can edit a file without renumbering
  the rest. On a mismatch the test prints each hit `file:line word` that is not known, and each
  known entry whose count differs or is no longer found. The file has a top-level `owners` saying
  that entries under `runregistrykit/tests/` are 05c's and the rest 05b's. It holds exactly what
  the guard finds at this commit, written once by running the guard's own scans (the log says
  how) and never edited by hand. `test_package_imports.py`'s `FORBIDDEN` strings are among the
  entries, for 05c.

The guard initialises no Ray, opens no store and reads no client.

### 2.4 The public names (U11)

- `runregistrykit._slug` becomes **`slug`**, with a one-sentence docstring saying it is what
  `run_id` applies to each of its three parts, so that a client can recover a run id's parts from a
  manifest. There is no alias, and `run_id` calls `slug`.
- Each of `runregistrykit/__init__.py`, `stores.py`, `client.py`, `fingerprint.py` and
  `__main__.py` gains a sorted `__all__` after its imports. It holds the module's public names:
  every module-level `def`, `class` and assigned name without a leading underscore, defined in the
  module. For `__init__.py` it also holds `slug` and the four names it imports from `client`
  (`CONFIG_FILE`, `ClientRoot`, `ConfigError`, `find_client_root`), which the tests and `__main__`
  already reach through `runregistrykit`. For `__main__.py` it is `["main"]`. No name becomes public
  or private beyond `slug`. The fingerprint names stay in `runregistrykit.fingerprint` and are not
  re-exported.
- `runregistrykit/tests/test_public_names.py`: for each of the five modules, `__all__` is sorted,
  equals the set the rule above derives by `ast`, and each name resolves. `runregistrykit` has no
  attribute `_slug`, and `run_id("A b", "0 1", "c")` equals the three `slug`s joined with its stamp.

### 2.5 The licence header (U12)

These fourteen lines, exactly as RayPoolKit's `raypoolkit/__init__.py` has them at its `HEAD`, go
first in each of the five package modules, then a blank line, then the module docstring:

```
# (c) University of Sussex 2026
# Created by David Seery
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

A comment before the docstring leaves the docstring the module's own (`ast.get_docstring`). No test
module gets it (U12). `test_public_names.py` gains a test that each of the five begins with exactly
these lines, and that its docstring is still read as the module's.

### 2.6 What else moves

Nothing. In particular no docstring, comment or message is reworded, `CLAUDE.md` and `README.md`
are untouched, and no existing test changes. Adding the header moves every line of the five modules
by 15. The board's package lines for the four open issues are re-read at this commit and recorded
(§4.3).

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root: **`Ran 245 +
   N tests … OK`**, N the new tests. Count by loader and give the per-module counts and the time.
2. **Nothing outside temporary directories**: `git status --short --ignored` the same before and
   after a run (but `__pycache__/`); no `var/`; `git worktree list` this checkout alone; no Ray
   process before or after.
3. **The measurement.** The script run twice into the scratchpad gives the same bytes (`cmp`), and
   the committed file equals them. Run with the committed file present and no `--output`, it exits
   1 and changes nothing. Its summary counts are compared with §"At writing"'s, and any difference
   is explained.
4. **The known hits.** The guard's own scans, run on the committed tree, give exactly
   `known_hits.json`. The per-scan totals, split between the package modules and the tests, are
   compared with §"At writing"'s, and any difference is explained.
5. **The tests catch behaviour** (README §5 rule 10). Each mutation is applied, the suite run, then
   reverted, and recorded as a diff with the tests that fail:
   - (m1) `StoreFixtures` added to `client.py`'s module docstring: a new hit;
   - (m2) one known package hit removed from the code without updating the data (`stores.py`'s
     section comment `# retirement (store-retirement prompt 03)` made `# retirement`): a known hit
     no longer found, in two scans;
   - (m3) `from datastorekit.SQL.ShardedPool import ShardedPool` at `stores.py`'s module scope;
   - (m4) `import numpy` inside a function of `client.py`;
   - (m5) `(prompt 07)` added to a comment of `client.py`;
   - (m6) one campaign (`store-retirement`) removed from SGK's campaigns in the committed data file:
     known hits no longer found;
   - (m7) a public function added to `fingerprint.py` without `__all__`;
   - (m8) `_slug = slug` added to `__init__.py`;
   - (m9) the header's `#    http://www.apache.org/licenses/LICENSE-2.0` line removed from
     `client.py`;
   - (m10) `package_files()` skipping `runregistrykit/tests/`;
   - (m11) the agent's own, of the import rule's allow list or the word rule.

   Each must fail at least one test. A mutation no test catches is a **stop**.
6. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` gains exactly `tests/test_package_is_generic.py`,
   `tests/test_public_names.py`, `tests/data/client_vocabulary.json` and
   `tests/data/known_hits.json`. `docs/extraction/` gains `measure_client_vocabulary.py`. The five
   package modules change only by §2.4 and §2.5.
2. §3.1–§3.6 hold.
3. **The records**, in the same commit:
   - the log, `logs/05a-the-guard-and-the-public-names.md`, per README §5.1. It holds: the
     script's summary; the per-scan totals of the known hits, package and tests; how
     `known_hits.json` was written; the suite before (245) and after; every mutation as a diff;
   - this board: the header, §1's row for 05a, §1.1's P2 and N1, and §3 (each open issue's
     *Package lines (05a, …)*, and the two narrowed issues pointing at `known_hits.json` for their
     hits);
   - `docs/OPEN_ISSUES.md`: the count stays 4 unless the work opens one; the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `PROVENANCE.md`: "Since the import" gains 05a's section (the guard and its data; `slug`;
     `__all__`; the header).

---

## 5. Stop conditions — stop and ask the user

- A client cannot be read at its commit through `git`, or the registry, factory directory or
  campaigns directory is not where §2.2 says.
- An existing test would need to change.
- A package word would need to be added beyond `datastorekit.contract`'s, or a word rule beyond
  §2.3's. Record the word or the rule and ask; do not widen the rules to make a scan pass.
- A mutation of §3.5 is caught by no test.
- Any record would change form (README §5 rule 7).
- The suite needs a Ray cluster, starts Ray, imports a client, writes outside a `tempfile`
  directory, or leaves a worktree registered here.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything.

---

## 6. What this prompt does not do

- **Files it creates or changes:** the four new files under `runregistrykit/tests/` (§4.1); the new
  `docs/extraction/measure_client_vocabulary.py`; the five package modules (§2.4 and §2.5 only);
  `PROVENANCE.md`; the log, this board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It rewrites no prose (05b) and renames no test, helper or fixture (05c). No hit is removed.
- It changes no existing test module, no fixture, `README.md`, `CLAUDE.md`, `pyproject.toml` or
  `docs/extraction/compare_with_source.py`.
- It adds no CI and makes no tag.

---

## 7. The log and the board

`logs/05a-the-guard-and-the-public-names.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 05a, §1.1's P2 and N1, and §3 as §4.3.

---

## At writing (2026-10-15, at `dfcb884`)

Measured read-only, for the README's row and the orchestrator:
- **The clients**, through `git` only, by a trial script with §2.2's rules (the planner's
  scratchpad). The three commits are those of §2.2: SGK `14bcac0` clean, SI `5fb4a1d` clean,
  ChamPBH `c21cdfb` with 22 uncommitted paths, which `git show` does not see. ChamPBH's `HEAD` moved
  during the measurement, from `5f68a56`, which is why the commits are fixed.

  | Client | Registry keys | Columns | Factory modules | Packages | Campaigns |
  |---|---|---|---|---|---|
  | SGK | 38 | 194 | 36 | 14 | 26 |
  | CPBH | 27 | 80 | 26 | 11 | 10 |
  | SI | 30 | 101 | 22 | 15 | 6 |

  DatastoreKit's measurement (SGK `6f7f291`, ChamPBH `52142d7`) read every client's factories from
  `Datastore/SQL/ObjectFactories` and ChamPBH's registry from `Datastore/SQL/Datastore.py`. Since
  then, SGK and ChamPBH have moved their factories to a top-level `ObjectFactories/`, and ChamPBH
  its registry to `config/datastore.py`, so DatastoreKit's file is not reused.
- **A trial guard** with §2.3's rules, over the 22 tracked `*.py` under `runregistrykit/` at
  `dfcb884`. It found 454 forbidden words and these hits:

  | Scan | Package modules | Tests |
  |---|---|---|
  | code names | 0 | 28 (13 file-word entries) |
  | strings and docstrings | 26 (14) | 70 (36) |
  | comments | 8 (6) | 1 (1) |
  | citations | 35 (10) | 41 (32) |

  The package modules' words are `A3`, `main.py`, `realistic_large_x`,
  `handover-A3-baseline-lambdacdm`, `handover`, and the campaigns `run-registry`,
  `datastore-portability`, `store-retirement` and `store-fingerprint`. The tests' include those, and
  also `sweep_shaped`, `a3_shaped`, `TestLiveA3Shape`, `a3-pilot`, `handover-atol-sweep`,
  `scoped_pipeline_run`, `quadsource_atol_sweep`, `GkSource`, `wavenumber`, `ObjectFactories`,
  `RunRegistry`, `StoreFixtures` (the last three in `test_package_imports.py`'s `FORBIDDEN`) and
  the neutral store's `parent_serial`, `solver_serial` and `log10_tol`. Those three are columns the
  neutral store shares with the clients' tag and solution tables; 05c renames or allows them. The
  substring of a name inside an identifier (`quadsourceintegral` in a method name) is not a rule:
  tried, it flagged `runregistrykit` itself (`RunRegistry`, case-insensitively), so the one such
  identifier is listed instead.
- **Without the contract's words**, `version` alone added 21 hits (it is a registry key of each
  client and DatastoreKit's version table). `store_tag`, `tag_serial` and `label` are the contract's
  too. No client name appears anywhere in the package today.
- **The imports** conform today. The package modules import only the standard library and the
  package at module scope, and `datastorekit` only inside functions of `stores.py` and
  `fingerprint.py`. The tests import `datastorekit`, `sqlalchemy` and, inside one function, `ray`.
- **`_slug`** is used only by `run_id` (`__init__.py:78`, `:86`). SGK's
  `docs/dk-and-rpk-migration/rehearsal/stage_counts.py:37-38` calls it, its only private use of
  the package, besides `sigterm_handler_probe.py` patching `stores.fingerprint_store`, which needs no
  name (U11). No module has `__all__` today.
- **The header** is RayPoolKit's and SI's, word for word. DatastoreKit's modules carry none.
