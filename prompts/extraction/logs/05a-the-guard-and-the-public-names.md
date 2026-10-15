# Log — prompt 05a: the guard and the public names

**Subject:** Add the no-client guard, its vocabulary and known hits, the public names and the licence header
**Commit:** this commit (on `main`, after `d2a3d85`)
**Date:** 2026-10-15
**Agent:** Claude Sonnet 5.5, dispatched by the orchestrator with its brief and the orchestration
note's section 0 (`note-05a-section0.md`)
**Result:** **landed.** The guard `runregistrykit/tests/test_package_is_generic.py` scans all 24
Python files under `runregistrykit/` (itself and `test_public_names.py` included) with four word
scans (code names, strings, comments, citations) and an import rule, each against
`runregistrykit/tests/data/known_hits.json`, which holds exactly what the scans find: **69 hits in
the package modules (30 file-word entries) and 137 in the tests (83 entries)**. The vocabulary is
measured by `docs/extraction/measure_client_vocabulary.py` through `git` at the three fixed
commits and held in `runregistrykit/tests/data/client_vocabulary.json`. `_slug` is public as
**`slugify`** (the user's ruling, correction 2), with no alias; each of the five package modules
declares a sorted `__all__` and begins with the Apache 2.0 header; `test_public_names.py` pins
both. The suite: **245 -> 275** (`245 + 22 + 8`), `Ran 275 tests ... OK`. (m1)-(m11) each fail at
least one test. No stop condition was met. Nothing closed or opened; the two prose issues are
narrowed (their hits are listed by file and word in `known_hits.json`); `docs/OPEN_ISSUES.md` stays
at 4.

## What shipped

| File | What |
|---|---|
| `docs/extraction/measure_client_vocabulary.py` | **new**, 326 lines, standard library only, modelled on DatastoreKit's: reads each client only through `git rev-parse`, `cat-file -e`, `ls-tree` and `show` at the three commits; writes `client_vocabulary.json`, refusing to overwrite (exit 1), exit 2 when a client or a path in it cannot be read, 0 when it wrote |
| `runregistrykit/tests/data/client_vocabulary.json` | **new**, 23453 bytes, written by the script: per client the commit, the registry's keys, the columns (and the modules read), the packages and the campaigns; the `listed` words (17, in three groups with where the records name them); the `summary` |
| `runregistrykit/tests/test_package_is_generic.py` | **new**, 22 tests: the guard (docstring, `package_files()`, `VOCABULARY`, `PACKAGE_WORDS`, `NOT_PROJECT_PACKAGES`, the five scans, `import_allowed(module, rel, in_function)`), and tests of the files, the vocabulary, the rules, the known-hits file, the self-scan and the allow list |
| `runregistrykit/tests/data/known_hits.json` | **new**, written by the guard's own scans (below), never by hand |
| `runregistrykit/tests/test_public_names.py` | **new**, 8 tests: `__all__` of each of the five modules, `slugify`, `run_id`, the header |
| `runregistrykit/__init__.py` | the 14-line header and a blank line; `__all__` (20 names) after the imports; `_slug` -> `slugify` with a two-line docstring, and its three calls in `run_id` |
| `runregistrykit/stores.py`, `client.py`, `fingerprint.py`, `__main__.py` | the header and `__all__` only (26, 4, 4 and 1 names) |
| `PROVENANCE.md` | 05a's section under "Since the import" |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

`runregistrykit/` gains exactly the four files; `docs/extraction/` the script. The five modules
change only by the header, `__all__` and `slugify` (`git diff` of each: insertions of the header
and of the `__all__` block, and in `__init__.py` the rename and three call sites). Not touched: any
existing test module or fixture, `tests/__init__.py`, `pyproject.toml`, `README.md`, `LICENSE`,
`.gitignore`, `.idea/`, `CLAUDE.md`, `compare_with_source.py`, the campaign README, the prompt,
`prompts/extraction/orchestrator/`.

**The guard, as built.** The forbidden words are 454, as the trial's: the registries' keys (80),
the identifier columns (300), the project packages (18), the campaigns (40) and the `listed` words
(17), less `PACKAGE_WORDS` (the five attributes of `datastorekit.contract`, read at run time) and
with overlaps merged. A word of a string or comment is checked whole, by each dot part and, when
hyphenated, each hyphen part; a code name whole and split on `_`; each scan reports `file:line
word`, and a hit is one (line, word) pair, as DatastoreKit's. The citation pattern is built from
three parts (a directory name and a slash; the word for a prompt, singular or plural, a space and
two digits; the section sign, an optional space and a digit). The import rule: package modules may
import the standard library and `runregistrykit` anywhere and `datastorekit` only inside a function
of `stores.py` or `fingerprint.py`; tests the standard library, the package, `datastorekit`,
`sqlalchemy` and `ray`. The imports scan finds nothing in either today.

## Deviations from the prompt

The note's corrections and readings are recorded as found (1-12); the rest are this agent's.

1. **The gate's diff is not empty** (correction 1, found as it says). `git diff --stat dfcb884 HEAD
   -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md` shows `docs/OPEN_ISSUES.md`,
   changed by `6ec0066`; the same diff from `6ec0066` is empty, and the gate was read from there.
   `HEAD` was `d2a3d85`, which touches only `prompts/`. **STRUCTURALLY REQUIRED.**
2. **The public name is `slugify`, not `slug`** (correction 2; the user's ruling, README section
   6.2, U11). `run_id`'s and `begin()`'s parameter `slug` would shadow a module function of that
   name inside `run_id`. Applied in the rename and docstring, `__init__.py`'s `__all__`,
   `test_public_names.py`, (m8) as `_slug = slugify` and `PROVENANCE.md`; `run_id`'s and `begin()`'s
   signatures are unchanged (pinned by `TestSlugify.test_the_signatures_of_run_id_and_begin_are_unchanged`);
   `run_id` calls `slugify`, no alias. **STRUCTURALLY REQUIRED.**
3. **`run_id`'s test passes `when`** (correction 3): `TestSlugify.test_run_id_joins_three_slugs_and_a_stamp`
   compares `run_id("A b", "0 1", "c", when)` with the three `slugify`s joined with
   `time.strftime(_ID_STAMP, time.localtime(when))`, `when` a fixed time; a second assertion checks
   the shape of the stamp with `when=None`. **IMPLEMENTATION CHOICE.**
4. **`PACKAGE_WORDS` names the contract's five attributes** (correction 4, recommendation followed):
   `VERSION_TABLE`, `VERSION_LABEL`, `TAG_LABEL`, `TAG_TABLE`, `TAG_SERIAL`, each with its reason;
   `VERSION_SERIAL_KEY` (`"_version_serial"`) is left out, being no client's word.
   `test_the_package_words_are_the_contracts_and_are_not_forbidden` pins the set, that none is
   forbidden, and that at least one is a measured registry key (so the rule is doing work).
   **IMPLEMENTATION CHOICE.**
5. **The guard scans itself, so its tests name no forbidden word** (correction 5): the words its
   tests use are read from the data file at run time (each client's first registry key that is not a
   package word, first identifier column, first project package and first campaign, and every
   `listed` word, each asserted forbidden); each part's size equals the file's `summary`; the rule
   tests are built on words chosen from the vocabulary at run time (a plain word whose case-swapped
   form is not forbidden; a hyphenated `listed` word with two forbidden parts; a project package of
   each client, with and without a submodule, and `numpy` for the allow list). The guard file ends
   with **no entry** in `known_hits.json`, pinned by `TestTheKnownHits.test_this_module_holds_no_known_hit`
   and shown by scanning the guard and `test_public_names.py` alone (no hit in any scan). No
   forbidden word is built from fragments. The one place fragments are used besides the pattern is
   `test_a_citation_is_a_path_a_numbered_prompt_or_a_section`, whose samples are made from the
   pattern's own parts, so that the module holds no citation. **IMPLEMENTATION CHOICE.**
6. **The import rule's scope** (correction 6): `import_allowed(module, rel, in_function)`;
   `test_the_allow_list` checks, both ways: module scope of `stores.py` refused; inside a function
   of `stores.py` and `fingerprint.py` allowed; inside a function of `client.py`, `__init__.py` or
   `__main__.py` refused; anywhere in a test allowed; `sqlalchemy` and `ray` allowed in a test and
   refused in each package module; a third party refused everywhere; a project package of each
   client refused everywhere. `test_the_scan_sees_where_an_import_is` pins the function-body walk
   (class bodies are module scope; `lambda` and `def` bodies are function scope). Measured as the
   note says: the import scan finds nothing today. **IMPLEMENTATION CHOICE.**
7. **The header adds no hit** (correction 7, as expected): the comment and citation scans over the
   header, and the string scan over each `__all__`, add nothing; the package totals are the trial's
   exactly. **As found.**
8. **The trial's counts** (correction 8). The package modules equal the prompt's "At writing"
   exactly (0 / 26 / 8 / 35). **The tests differ**: 29 / 67 / 1 / 40 against 28 / 70 / 1 / 41, with
   file-word entries 14 / 36 / 1 / 32 against 13 / 36 / 1 / 32. The entries differ by one: a code
   name the trial did not list, `test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file`
   (`test_run_registry.py:566`), whose `_`-split part `tolerance` is a registry key of SGK; the
   rule is §2.3's. The string and citation hit counts are lower by 3 and 1 with the same entries:
   the guard counts a hit once per (line, word), as DatastoreKit's; the cause of the trial's higher
   counts was not traced. Neither is a stop (correction 8). **As found, explained in part.**
9. **(m6) is caught as the prompt expects** (correction 9): `store-retirement` is a campaign of SGK
   alone, so removing it from SGK's list drops it from the forbidden set, and the two scans that
   hold it fail; the file's own summary check fails too. **As found.**
10. **Writing `known_hits.json`** (correction 10): by the writer below, in the scratchpad, never
    under `runregistrykit/` or `docs/`. The file was not edited afterwards, and the guard's final
    form (a later edit to a test-only selection, deviation 17) produced no hit, so it was not
    re-run. **As found.**
11. **`__all__`** (correction 11): derived by an `ast` rule, then compared: `__init__.py` 20,
    `stores.py` 26, `client.py` 4, `fingerprint.py` 4, `__main__.py` 1 (`["main"]`), as the note
    derived them. **As found.**
12. **The suite takes about 90 s** (correction 12): 89.3 s and 96.6 s after (below). **STRUCTURALLY
    REQUIRED.**
13. **The script's file** (this agent's): under each client's `columns` it also records the
    `directory` read, and `campaigns` is `{"directory", "names"}`; `listed` is three groups, each
    `{"where", "words"}` (the prompt names the groups and where the records name them); a path that
    `cat-file -e` does not find in the commit (the registry module, the factory directory, the
    campaigns directory) is `CannotRead`, exit 2. The `ls-tree -r` of the factory directory is
    recursive, as the prompt says. **IMPLEMENTATION CHOICE.**
14. **`known_hits.json`'s form** (this agent's): `{"owners": <a sentence>, "known hits": {<scan's
    test name>: [[file, word, count], ...]}}`, each list sorted; for the four word scans and
    `test_every_import_is_allowed` (empty). The prompt left the key names open. **IMPLEMENTATION
    CHOICE.**
15. **`slugify`'s docstring is two lines**, one sentence, to keep within the repository's 100
    columns. **IMPLEMENTATION CHOICE.**
16. **`__all__`'s placement and spelling** (this agent's): a blank line, then the list after the
    last top-level import (`__init__.py` after `from .client import ...`; `stores.py` after its
    imports, `:144` of the file as it was), written by a scratch script from the `ast` rule and
    formatted by `black`; sorted by Python's string order (capitals first). The test compares the
    list with `sorted()`. **IMPLEMENTATION CHOICE.**
17. **Tests beyond the prompt's**, all in the two new modules: the rule tests on synthetic source
    (`TestTheRules`, 7), the known-hits file's form and the self-scan, `TestTheFiles`'s second
    test, the vocabulary tests, the `begin`/`run_id` signature pin, the package's `__all__` holding
    the four client names (identity with `runregistrykit.client`'s), and that the fingerprint names
    are not re-exported. The selection of the hyphenated `listed` word in the rule tests was
    corrected once (the first choice, `a3-pilot`, has no forbidden part), before the final run.
    **IMPLEMENTATION CHOICE.**
18. **The first registry key of SGK is `version`**, a package word, so the vocabulary test takes
    each client's first key that is not one. **IMPLEMENTATION CHOICE.**
19. **Mutation diffs are taken against the index**: the files were staged once final, each
    mutation applied to the working file by a scratch script, `git diff` taken, the suite run, and
    `git checkout -- .` restoring the staged blob. The index blobs are this commit's. (m6) edits the
    data file by loading it, removing the word and dumping it in the script's own form, which gives
    a one-line diff. **IMPLEMENTATION CHOICE.**
20. **(m3), (m4) and (m10) fail more than the guard**: (m3) also fails the older import tests and
    the child-interpreter tests that now load `datastorekit`; (m4)'s `numpy` is not installed, so
    every test that locates a client root errors; (m10) fails the guard's file, vocabulary-free
    tests and the four word scans. In each, the guard's own test is among the failures
    (`test_every_import_is_allowed`; `test_the_derived_files_hold_every_tracked_python_file`).
    **As found.**

No UNINTENDED DRIFT. No existing test or fixture changed. No record's form changed: the manifest,
`status.json`, `checkpoint.jsonl` and the sidecar are written by unchanged code; the only code
changes are the header, `__all__` and a rename of a function used by `run_id` alone.

## Verification performed

**At dispatch** (the orchestrator's, relied on): `main` at `d2a3d85`, clean; `Ran 245 tests in
91.568s`, OK; the gate as deviation 1. I did not re-run the 245 before my changes.

**3.1, the suite**, `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the
root, in the foreground, to a scratch file:

| | Verdict |
|---|---|
| before | `Ran 245 tests in 91.568s`, OK (the orchestrator's, at dispatch) |
| after, first run | `Ran 275 tests in 89.333s`, OK |
| after, final run (the tree as committed, but for the records) | `Ran 275 tests in 96.576s`, OK |

**245 -> 275**, `245 + 22 + 8`. By loader, new: `test_package_is_generic` 22 (`TestTheFiles` 2,
`TestTheVocabulary` 4, `TestTheRules` 7, `TestTheKnownHits` 2, `TestThePackageNamesNoClient` 4,
`TestThePackageImportsNoClient` 3), `test_public_names` 8 (`TestAll` 4, `TestSlugify` 3,
`TestTheHeader` 1). The other modules' counts are unchanged (04b's log).

**3.2, nothing outside temporary directories.** `git status --short --ignored` the same before and
after the first run (but `__pycache__/`); no `var/`; `git worktree list` this checkout alone; no
Ray process (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` exit 1) after the runs.

**3.3, the measurement.** The script, run into the scratchpad twice, gives the same bytes (`cmp`),
and the committed file equals them (`cmp`). Run with the committed file present and no `--output`,
it prints `!! ... exists; a re-measure writes a new file` and exits 1; `git status` unchanged.
Its summary, verbatim:

```
wrote .../runregistrykit/tests/data/client_vocabulary.json (23453 bytes)
  SGK: SecondaryGWKit at 14bcac0eb73069131f8ce4f55d91e5fc3e7318cf: 38 registry keys, 194 column names in 36 modules, 14 packages, 26 campaigns
  CPBH: ChamPBH at c21cdfb5613a3ed976a91a95431495dc8bfd49c8: 27 registry keys, 80 column names in 26 modules, 11 packages, 10 campaigns
  SI: StochasticInstantons at 5fb4a1d71a016f1b23393923b9a3d59972415aa0: 30 registry keys, 101 column names in 22 modules, 15 packages, 6 campaigns
  all clients: 82 registry keys, 329 column names, 22 packages, 40 campaigns; 17 listed words
```

Against "At writing": registry keys 38 / 27 / 30, columns 194 / 80 / 101, factory modules 36 / 26 /
22, packages 14 / 11 / 15, campaigns 26 / 10 / 6 are **equal**; the commits are the prompt's three.
The `listed` words are 5 + 8 + 4 = 17.

**3.4, the known hits.** The guard's own scans on the committed tree give exactly
`known_hits.json` (the five scanning tests pass, each asserting equality of the counted entries
and an empty `problems`). Totals, hits (file-word entries):

| Scan | Package modules | Tests | At writing, package / tests |
|---|---|---|---|
| code names | 0 | 29 (14) | 0 / 28 (13) |
| strings and docstrings | 26 (14) | 67 (36) | 26 (14) / 70 (36) |
| comments | 8 (6) | 1 (1) | 8 (6) / 1 (1) |
| citations | 35 (10) | 40 (32) | 35 (10) / 41 (32) |
| imports | 0 | 0 | 0 / 0 |

The differences are deviation 8. The package modules' words: `A3`, `main.py`, `realistic_large_x`,
`handover-A3-baseline-lambdacdm`, `handover`, `datastore-portability`, `run-registry`,
`store-fingerprint` and `store-retirement`, and the citations `prompts/`, `prompt 01`, `prompt 03`,
`prompt 04`, and the sections `§0`, `§2`, `§5`, `§6`. The tests' include `test_package_imports.py`'s
`FORBIDDEN` strings (`ObjectFactories`, `StoreFixtures`, `RunRegistry`), for 05c. The guard and
`test_public_names.py` hold no hit in any scan.

**How `known_hits.json` was written.** By this script, `write_known_hits.py`, in the session
scratchpad (`agent-05a/`, outside the repository), run from the repository root with the venv's
interpreter once the guard and the five modules were final:

```
./venv/bin/python /private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/42d51d0c-0157-430f-9e49-30c1200577d3/scratchpad/agent-05a/write_known_hits.py
```

Its output: `test_no_code_name package 0 tests 29`, `test_no_string_or_docstring package 26 tests 67`,
`test_no_comment package 8 tests 1`, `test_no_citation package 35 tests 40`,
`test_every_import_is_allowed package 0 tests 0`. Its text, whole:

```python
"""Writes runregistrykit/tests/data/known_hits.json from the guard's own scans (05a, correction 10).
Run from the repository root: ./venv/bin/python <this file>. Refuses to overwrite."""
import json, sys
from pathlib import Path
from runregistrykit.tests import test_package_is_generic as g

if g.KNOWN_HITS.exists():
    sys.exit("refusing to overwrite " + str(g.KNOWN_HITS))
hits = g.scan_all()
data = {
    "owners": "entries under runregistrykit/tests/ are the tests' to remove (prompt 05c); the rest are the package modules' (prompt 05b)",
    "known hits": {name: g.count_hits(h) for name, h in hits.items()},
}
g.KNOWN_HITS.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
for name, h in hits.items():
    pk = [x for x in h if not g.is_test(x[0])]
    ts = [x for x in h if g.is_test(x[0])]
    print(name, "package", len(pk), "tests", len(ts))
```

**3.5, the mutations**: the record below. **3.6.** `./venv/bin/black --check runregistrykit docs`:
26 files would be left unchanged.

**The header, by reading and by `ast`.** The five modules begin with the fourteen lines of the
prompt (the text of the prompt; RayPoolKit was not read by this agent), then a blank line, then
the docstring, which `ast.get_docstring` still reads and which equals `module.__doc__` cleaned
(`TestTheHeader`).

**Isolation.** Nothing was installed. SGK, ChamPBH and StochasticInstantons were read only by the
script, through `git -C /Users/ds283/Documents/Code/<repository>` `rev-parse`, `cat-file -e`,
`ls-tree` and `show`, at the three commits; no client was imported, run or edited and no client
working tree was read. DatastoreKit was read through `git show b01737f:<path>` for its guard, its
script and the head of its vocabulary file. Every scratch file was in `agent-05a/` of the session
scratchpad; no scratch `.py` went under `runregistrykit/` or `docs/`. Nothing pushed or tagged.

## The deliberate-breakage record

Each diff below is exactly as applied, against this commit's blobs (deviation 19). Each was checked
in `bash` with `git apply --check`, `git apply`, `git apply -R --check` and `git apply -R`, and
`git status` was clean after each; the suite was run on each as mutated. None is committed.

| # | Mutation | The suite | Failing tests |
|---|---|---|---|
| (m1) | `StoreFixtures` added to `client.py`'s module docstring: a new hit | `Ran 275 ... FAILED (failures=1)` | FAIL `test_package_is_generic.TestThePackageNamesNoClient.test_no_string_or_docstring` |
| (m2) | `stores.py`'s section comment `# retirement (store-retirement prompt 03)` made `# retirement`, the data unchanged: a known hit no longer found, in two scans | `Ran 275 ... FAILED (failures=2)` | FAIL `TestThePackageNamesNoClient.test_no_comment`, `test_no_citation` |
| (m3) | `from datastorekit.SQL.ShardedPool import ShardedPool` at `stores.py`'s module scope | `Ran 275 ... FAILED (failures=10)` | FAIL `test_package_is_generic.TestThePackageImportsNoClient.test_every_import_is_allowed`; `test_package_imports.TestPackageImports.test_import_loads_nothing_heavy`, `test_module_scope_is_the_standard_library_and_the_package`; and, by the child interpreters that now load `datastorekit`, `test_store_amend.TestCommandLine.test_import_loads_neither_ray_nor_sqlalchemy`, `test_json_remove_bad_json_and_exit_codes`; `test_store_command_line.TestImports.test_import_and_list_load_neither_ray_nor_sqlalchemy`, `TestStoreCommands.test_show_create_adopt_copy_and_move`; `test_store_fingerprint.TestFingerprintCommand.test_read_only_then_write_then_matches`; `test_store_retire.TestCommandLine.test_import_loads_neither_ray_nor_sqlalchemy`, `test_retire_its_exit_codes_and_what_it_prints` |
| (m4) | `import numpy` inside a function (`_under`) of `client.py` | `Ran 275 ... FAILED (failures=4, errors=289)` | FAIL `TestThePackageImportsNoClient.test_every_import_is_allowed`; and, because `numpy` is not installed, `ModuleNotFoundError` in 289 tests that locate a client root, and 3 further failures among them (`test_run_registry.TestManifest.test_manifest_is_on_disk_before_the_work_starts`, `test_store_command_line.TestStoreCommands.test_show_create_adopt_copy_and_move`, `test_store_fingerprint.TestFingerprintCommand.test_write_is_refused_on_an_absent_legacy_or_problem_sidecar`); the full list is in the scratch output, not reproduced |
| (m5) | `(prompt 07)` added as a comment of `client.py` | `Ran 275 ... FAILED (failures=1)` | FAIL `TestThePackageNamesNoClient.test_no_citation` |
| (m6) | `store-retirement` removed from SGK's campaigns in the committed data file | `Ran 275 ... FAILED (failures=4)` | FAIL `TestThePackageNamesNoClient.test_no_comment`, `test_no_string_or_docstring` (known hits no longer found); `TestTheVocabulary.test_every_part_holds_the_words_the_file_summarises` [part='campaigns, all clients'], [client='SGK'] (the file's own summary no longer matches its lists). `store-retirement` is a campaign of SGK alone, so removing it drops the word from the forbidden set (note, correction 9). The diff removes one line: the script's `json.dumps` of the edited data gives the file's own form |
| (m7) | a public function added to `fingerprint.py` without `__all__` | `Ran 275 ... FAILED (failures=1)` | FAIL `test_public_names.TestAll.test_each_module_declares_a_sorted_all_of_its_public_names` [module='runregistrykit.fingerprint'] |
| (m8) | `_slug = slugify` added to `__init__.py` (correction 2: the prompt's `_slug = slug`) | `Ran 275 ... FAILED (failures=1)` | FAIL `test_public_names.TestSlugify.test_the_private_name_is_gone_and_slugify_is_public` |
| (m9) | the header's `#    http://www.apache.org/licenses/LICENSE-2.0` line removed from `client.py` | `Ran 275 ... FAILED (failures=1)` | FAIL `test_public_names.TestTheHeader.test_each_module_begins_with_the_header_and_keeps_its_docstring` [module='runregistrykit.client'] |
| (m10) | `package_files()` skipping `runregistrykit/tests/` | `Ran 275 ... FAILED (failures=10)` | FAIL `TestTheFiles.test_the_derived_files_hold_every_tracked_python_file`, `test_the_tests_and_this_module_are_scanned`; `TestTheKnownHits.test_the_file_is_in_form` x4 (the entries' files are no longer scanned); `TestThePackageNamesNoClient.test_no_code_name`, `test_no_string_or_docstring`, `test_no_comment`, `test_no_citation` |
| (m11a) | the agent's, of the import rule's allow list: `in_function` dropped from the `datastorekit` clause of `import_allowed` | `Ran 275 ... FAILED (failures=2)` | FAIL `TestThePackageImportsNoClient.test_the_allow_list`, `test_the_scan_sees_where_an_import_is` |
| (m11b) | the agent's, of the word rule: hyphen-separated parts no longer checked | `Ran 275 ... FAILED (failures=3)` | FAIL `TestThePackageNamesNoClient.test_no_string_or_docstring` (`A3` and `handover` of the hyphenated store names are no longer found); `TestTheRules.test_a_hyphenated_word_finds_itself_and_each_forbidden_part`, `test_a_word_of_a_string_is_whole_or_a_dot_part_or_a_hyphen_part` |

### The diffs

#### (m1) `StoreFixtures` added to `client.py`'s module docstring: a new hit

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..1efb1a2 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -13,7 +13,7 @@
 # See the License for the specific language governing permissions and
 # limitations under the License.
 
-"""Where a client's records go: its root, which a `runregistrykit.toml` marks, and that file.
+"""Where a client's StoreFixtures records go: its root, which a `runregistrykit.toml` marks, and that file.
 
 **The file.** A client marks its root with a file named `runregistrykit.toml`, read with
 `tomllib`. Every key is optional, and an empty file takes every default:
```

#### (m2) `stores.py`'s section comment `# retirement (store-retirement prompt 03)` made `# retirement`, the data unchanged: a known hit no longer found, in two scans

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index bed6b42..ef00635 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1397,7 +1397,7 @@ def fingerprint_store(
 
 
 # =================================================================================================
-# retirement (store-retirement prompt 03)
+# retirement
 #
 # `retire_store` deletes a closed store's own files through `ShardedPool.delete_store` and keeps
 # its sidecar as a tombstone. The order of the writes is the point: the tombstone, with the list of
```

#### (m3) `from datastorekit.SQL.ShardedPool import ShardedPool` at `stores.py`'s module scope

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index bed6b42..3eed85a 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -158,6 +158,8 @@ from . import (
 )
 from .fingerprint import load_fingerprinter, require_fingerprinter
 
+from datastorekit.SQL.ShardedPool import ShardedPool
+
 __all__ = [
     "AMEND_KEYS",
     "AMEND_OPERATION",
```

#### (m4) `import numpy` inside a function (`_under`) of `client.py`

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..74e7fc1 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -236,6 +236,7 @@ def _record_root(found) -> str:
 
 
 def _under(root, value) -> str:
+    import numpy
     return (
         value if os.path.isabs(value) else os.path.normpath(os.path.join(root, value))
     )
```

#### (m5) `(prompt 07)` added as a comment of `client.py`

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..b0608e9 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -68,6 +68,7 @@ from dataclasses import dataclass
 
 __all__ = ["CONFIG_FILE", "ClientRoot", "ConfigError", "find_client_root"]
 
+# (prompt 07)
 CONFIG_FILE = "runregistrykit.toml"
 
 # every key the file may hold, with its default
```

#### (m6) `store-retirement` removed from SGK's campaigns in the committed data file

```diff
diff --git a/runregistrykit/tests/data/client_vocabulary.json b/runregistrykit/tests/data/client_vocabulary.json
index af27d49..bee5142 100644
--- a/runregistrykit/tests/data/client_vocabulary.json
+++ b/runregistrykit/tests/data/client_vocabulary.json
@@ -327,7 +327,6 @@
           "source-remediation",
           "spec-transcription",
           "store-fingerprint",
-          "store-retirement",
           "test-suite-runtime",
           "tolerance-convergence",
           "transfer-remedial"
```

#### (m7) a public function added to `fingerprint.py` without `__all__`

```diff
diff --git a/runregistrykit/fingerprint.py b/runregistrykit/fingerprint.py
index ceb3711..bd172f8 100644
--- a/runregistrykit/fingerprint.py
+++ b/runregistrykit/fingerprint.py
@@ -220,3 +220,7 @@ def load_fingerprinter(client) -> Fingerprinter:
             f"compare, describe and listing (runregistrykit.fingerprint)"
         )
     return found
+
+
+def an_added_public_function():
+    return 1
```

#### (m8) `_slug = slugify` added to `__init__.py` (correction 2: the prompt's `_slug = slug`)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index d2105f1..d0d806a 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -119,6 +119,9 @@ def slugify(text) -> str:
     return re.sub(r"[^A-Za-z0-9._]+", "-", str(text)).strip("-")
 
 
+_slug = slugify
+
+
 def run_id(campaign, prompt, slug, when=None) -> str:
     """`<campaign>-<prompt>-<slug>-<YYYYMMDDTHHMMSS>`: it sorts, and a stranger reading
     `ls var/runs/` learns who owns each directory without asking anyone."""
```

#### (m9) the header's `#    http://www.apache.org/licenses/LICENSE-2.0` line removed from `client.py`

```diff
diff --git a/runregistrykit/client.py b/runregistrykit/client.py
index c44d484..75303c9 100644
--- a/runregistrykit/client.py
+++ b/runregistrykit/client.py
@@ -5,7 +5,6 @@
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
-#    http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
```

#### (m10) `package_files()` skipping `runregistrykit/tests/`

```diff
diff --git a/runregistrykit/tests/test_package_is_generic.py b/runregistrykit/tests/test_package_is_generic.py
index 8e6c0c1..dc8b06d 100644
--- a/runregistrykit/tests/test_package_is_generic.py
+++ b/runregistrykit/tests/test_package_is_generic.py
@@ -86,7 +86,10 @@ def package_files() -> list:
     for path in (REPO_ROOT / "runregistrykit").rglob("*.py"):
         if "__pycache__" in path.parts:
             continue
-        found.add(path.relative_to(REPO_ROOT).as_posix())
+        rel = path.relative_to(REPO_ROOT).as_posix()
+        if is_test(rel):
+            continue
+        found.add(rel)
     return sorted(found)
 
 
```

#### (m11a) the agent's, of the import rule's allow list: `in_function` dropped from the `datastorekit` clause of `import_allowed`

```diff
diff --git a/runregistrykit/tests/test_package_is_generic.py b/runregistrykit/tests/test_package_is_generic.py
index 8e6c0c1..ca31b88 100644
--- a/runregistrykit/tests/test_package_is_generic.py
+++ b/runregistrykit/tests/test_package_is_generic.py
@@ -216,7 +216,7 @@ def import_allowed(module: str, rel: str, in_function: bool) -> bool:
         return root in _TEST_ROOTS
     if root in _PACKAGE_ROOTS:
         return True
-    return root == "datastorekit" and in_function and rel in _DATASTORE_MODULES
+    return root == "datastorekit" and rel in _DATASTORE_MODULES
 
 
 # ------------------------------------------------------------------------------------------------
```

#### (m11b) the agent's, of the word rule: hyphen-separated parts no longer checked

```diff
diff --git a/runregistrykit/tests/test_package_is_generic.py b/runregistrykit/tests/test_package_is_generic.py
index 8e6c0c1..f3707a0 100644
--- a/runregistrykit/tests/test_package_is_generic.py
+++ b/runregistrykit/tests/test_package_is_generic.py
@@ -228,8 +228,6 @@ def _candidates(word: str) -> list:
     """A word of a string or comment, whole, by its dot-separated parts and, when it has a hyphen,
     by its hyphen-separated parts."""
     found = [word, *word.split(".")]
-    if "-" in word:
-        found += word.split("-")
     return found
 
 
```

## Observations not acted on

- **A hit the trial did not list.** `test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file` (`test_run_registry.py:566`)
  is a code-name hit (`tolerance`, a registry key of SGK) that the prompt's trial did not list; it
  is among the tests' known hits, for 05c to rename.
- **A repeated word on one line counts once.** A scan's hit is a (line, word) pair, as
  DatastoreKit's, so a second occurrence of a known word on a line that already holds it leaves
  the count unchanged and is not seen. A word on a new line is. This is the rule the prompt ports.
- **The writer is outside the repository.** `known_hits.json` is written by a scratch script whose
  text is in this log; 05b and 05c, which empty its entries, update the file by their own means
  (the writer refuses to overwrite, so it needs the file removed first) and say how in their logs.
- **`__all__` is read by the string scan.** Its names are strings in the package modules; none is
  a forbidden word today, but a public name that is a client's word would be a string hit as well
  as a code-name hit.
- **The module docstrings of `client.py`, `fingerprint.py` and the others are unchanged**, and so
  are the prose hits in them; 05b owns them.

## State handed to the next prompt

- **05b** empties the package modules' share of `known_hits.json`: 69 hits, 30 entries, in
  `__init__.py`, `stores.py` and `fingerprint.py` (`client.py` and `__main__.py` hold none).
  Lines moved by 05a's header and `__all__`: `__init__.py` by +15 up to its imports, +38 from
  `TERMINAL_STATES` (`:97`) to `slugify`, +40 after it (`run_id` is `:122`, `begin` `:601`);
  `stores.py` by +44 throughout (`_SHARDS_TABLE_UNREADABLE` `:1409-1410`, used `:1674`, `:1724`;
  "(prompt 01's log)" `:1409`; the section comments `:1225`, `:1400`; the docstring citation
  `:124`); `fingerprint.py` by +22 (the CLI text naming `main.py --inventory` is `:151`);
  `client.py` +17; `__main__.py` +17. No word rule or package word was added beyond the prompt's.
- **05c** empties the tests' share: 137 hits, 83 entries, in 14 test modules and fixtures
  (`test_package_imports.py`'s `FORBIDDEN` strings among them); the rename of
  `test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file` is one of its code-name hits. No
  existing test module changed here.
- **The guard** holds no known hit of its own and must stay so; a word its tests need is read from
  `client_vocabulary.json`.
- **`slugify`** is public and in `__all__`; SGK's `stage_counts.py` called `_slug` (`At writing`),
  and moves to `slugify` when SGK adopts a release.
- **The suite** is 275 in about 90 s.
