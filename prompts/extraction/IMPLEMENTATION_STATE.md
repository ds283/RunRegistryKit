# extraction campaign — implementation state

**Last updated:** 2026-10-15 · **Status: LIVE — 6 of 11 prompts written (01–03, 04a, 04b, 05a), 6 landed, 5 of
them reviewed (01, `4e0d715`, suite 3; 02, `8155445`, suite 108; 03, `035e4b5`, suite 135; 04a,
`c81ad06`, suite 186; 04b, `5302a6f`, suite 245; 05a, this commit, suite 275, awaiting review).** G1 holds
on the source side at SGK `a45aefc`, and on the package side for 01's and 02's files, the
equivalence check retired at 03 and describing `8155445`; E1 holds (DatastoreKit `v0.4.0`). U1
taken at set-up on 2026-10-14; U2 and U3 taken the same day, for 01, U4 for 02, U5 and U9 for 03,
U6, U7 and U8 for 04, U14 on 2026-10-15 for 04b, and U10, U11, U12, U15 and U16 the same day for
05, as recommended (README §6.2); 04 split into 04a and 04b, and 05 into 05a, 05b and 05c.

**Campaign:** [`README.md`](README.md) ·
**Source:** SecondaryGWKit's `RunRegistry/` at `a45aefc`, 25 files (G1) ·
**Brief:** SGK's `prompts/runregistry-extraction/runregistrykit-extraction-brief.md` ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.1

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Made by the user (README §6.1):**

| Decision | Decided |
|---|---|
| **D1** | a repository of its own (SGK, 2026-10-12) |
| **D3** | the fingerprint split by layer; this package takes a client fingerprinter and treats the result as opaque but for named fields (SGK, 2026-10-12) |
| **D4** | the store layer requires a fingerprinter (SGK, 2026-10-12) |
| **Q1–Q5, Q7** | names; config file at the root; worktree runs recorded in the main checkout; one distribution with `[stores]`; the Q5 pattern offered; no manifest format field (SGK, 2026-10-12) |
| **U1** | public `ds283/RunRegistryKit`, Apache 2.0 (2026-10-14) |

**Put to the user (README §6.2):**

| Decision | Recommendation | Status |
|---|---|---|
| **U2** the import | faithful: only the package's name changes; C1–C9 later | **taken** 2026-10-14 |
| **U3** the releases | one release, `v0.1.0`, at 06; 01 sets `0.1.0.dev0` | **taken** 2026-10-14 |
| **U4** shard fixtures | carry SGK's as they are; issue open | **taken** 2026-10-14 |
| **U5** config file | `runregistrykit.toml`; found from the script or the working directory; none is a refusal | **taken** 2026-10-14 (override spelled `client_root`, prompt 03 §2.3) |
| **U6** fingerprinter | a protocol and a shipped `DatastoreKitFingerprinter`, each client instantiating it; named by `[stores] fingerprinter = "module:attribute"` | **taken** 2026-10-14 (re-recommended at 04's writing) |
| **U7** what is read | versions, digest, `taken`, comparison `kind` and `text`; `encoding_format` not required to read | **taken** 2026-10-14 (two variants of one ported test removed) |
| **U8** neutral store | own factories and writer, public `datastorekit` names only | **taken** 2026-10-14 |
| **U9** self-record | `runregistrykit` always in `packages` | **taken** 2026-10-14 |
| **U10** guard | measured client vocabulary, and an import rule | **taken** 2026-10-15 (05a §2.2, §2.3; a citation scan besides) |
| **U11** public names | for `_slug` and the like, before the release | **taken** 2026-10-15 (`__all__`, 05a §2.4; the name `slugify`, amended at dispatch from the prompt's `slug`) |
| **U12** licence header | on every package module but the tests | **taken** 2026-10-15 (05a §2.5) |
| **U13** versions and CI | Python ≥3.12; `[stores]` `datastorekit>=0.4.0`; DatastoreKit's two ends, and a core job without it | open, for 06 |
| **U14** retire hazard | 04b loads the fingerprinter before a first retirement plans or fingerprints, and the loader refuses a class | **taken** 2026-10-15 |
| **U15** 05 split | three prompts: 05a the guard, names and header; 05b the package prose and the README's rules; 05c the tests' names | **taken** 2026-10-15 |
| **U16** tests in scope | the guard scans the tests; their SGK names renamed in 05c, rule 9 lifted for names only | **taken** 2026-10-15 |

## 1. Prompts

| # | Prompt | Model | Status | Commit | Suite |
|---|---|---|---|---|---|
| 01 | [`01-import-the-registry.md`](01-import-the-registry.md) | Opus | **landed and reviewed** 2026-10-14 ([log](logs/01-import-the-registry.md)) | `4e0d715` | 0 → 3 |
| 02 | [`02-port-the-core-and-shard-fixture-tests.md`](02-port-the-core-and-shard-fixture-tests.md) | Sonnet | **landed and reviewed** 2026-10-14 ([log](logs/02-port-the-core-and-shard-fixture-tests.md)) | `8155445` | 3 → 108 |
| 03 | [`03-the-root-and-the-client-config.md`](03-the-root-and-the-client-config.md) | Opus | **landed and reviewed** 2026-10-14 ([log](logs/03-the-root-and-the-client-config.md)) | `035e4b5` | 108 → 135 |
| 04a | [`04a-the-client-fingerprinter.md`](04a-the-client-fingerprinter.md) | Opus | **landed and reviewed** 2026-10-15 ([log](logs/04a-the-client-fingerprinter.md)) | `c81ad06` | 135 → 186 |
| 04b | [`04b-the-retire-tests.md`](04b-the-retire-tests.md) | Opus | **landed and reviewed** 2026-10-15 ([log](logs/04b-the-retire-tests.md)) | `5302a6f` | 186 → 245 |
| 05a | [`05a-the-guard-and-the-public-names.md`](05a-the-guard-and-the-public-names.md) | Sonnet | **landed** 2026-10-15, awaiting review ([log](logs/05a-the-guard-and-the-public-names.md)) | this commit | 245 → 275 |
| 05b | `05b-the-package-prose-and-the-rules.md` | Sonnet | not written | — | — |
| 05c | `05c-the-tests-own-names.md` | Sonnet | not written | — | — |
| 06 | `06-release-v0.1.0.md` | Sonnet | not written | — | — |
| 07 | `07-the-adoption-checklists.md` | Opus | not written | — | — |
| 08 | `08-verification-and-close-out.md` | Sonnet | not written | — | — |

**Written one at a time** (README §2.1), each after the one before it has landed and been reviewed.
The holds are for **method**, not scope: every charter is fixed in README §2.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`91b7a60`), used
for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`1f9b5b0`), used for 02;
[`orchestrator/prompt-03.md`](orchestrator/prompt-03.md) (`f02abc7`), used for 03;
[`orchestrator/prompt-04a.md`](orchestrator/prompt-04a.md) (`9dc34a5`), used for 04a;
[`orchestrator/prompt-04b.md`](orchestrator/prompt-04b.md) (`5177ffa`), used for 04b.

**Orchestrator review of prompt 01 (2026-10-14).** Dispatched from `91b7a60` to one Opus subagent,
with the note's §0: its facts, five corrections and readings of the prompt, its one addition (the
rename must be complete, shown by breakage (i)) and its two recommendations (D-name as a
substitution on equal-length `replace` blocks; no D-fmt rule). Reviewed against its commit
`4e0d715`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance 1–3
are met. No stop condition fired.

*At dispatch.* The note's gate held at `91b7a60`. The tree was clean, the only worktree was this
checkout, `runregistrykit` was not installed in `venv/` and there was no `var/`. SGK's `HEAD` was
`14bcac0`, clean, with `RunRegistry/` and `StoreFixtures/` unchanged since `a45aefc`; the 25 rows and
the shard fixture's blob as the table says. No Ray process was up; `RAY_ADDRESS` unset.

*The checks.*
1. **Scope.** `4e0d715` touches 11 files: the prompt's §6 list (`pyproject.toml`, the five files
   under `runregistrykit/`, `compare_with_source.py`, `PROVENANCE.md`), the log, this board and
   `prompts/INDEX.md`. No `venv/`, `*.egg-info`, `__pycache__` or scratch file; no `var/`.
2. **The files.** `git ls-files runregistrykit` is exactly the five. `pyproject.toml` is §2.2's:
   `0.1.0.dev0`, `>=3.12`, `dependencies = []`, `stores = ["datastorekit"]` unbounded,
   `include = ["runregistrykit*"]`; a description and `include-package-data = false` besides
   (log deviation 11).
3. **Equivalence, by running.** The check exits 0 with the expected counts (D-name 6, 13, 4, 0;
   D-fmt 0; 11 pending; 11 absent; 1 new), and its output is the log's verbatim. Independently,
   `perl -pe 's/\bRunRegistry\b/runregistrykit/g'` over each module exported from `a45aefc` gives
   the committed file byte for byte (`cmp`), all four.
4. **Equivalence, by reading.** `compare_with_source.py` read in full: the constants at its top;
   SGK read only through `git -C`; nothing of SGK or the package imported; the frozen tree an exact
   set equality, checked first; D-name the substitution on equal-length `replace` pairs only, no
   line numbers; the completeness rule present; `__pycache__` skipped; an undeclared `.py` fails; a
   pending file that is present fails (log deviation 8), so 02 must extend it.
5. **The check bites.** (a)–(i) extracted from the log and replayed in `bash` (`--check`, apply,
   `-R --check`, reverse), each exiting 1 and naming the line, file or row as the log records; the
   tree clean after each. The orchestrator's own, not in the log: `stores.py:120` and `:121`
   swapped fails as `ADDED package :120`, `DELETED source :121`.
6. **The import test.** `Ran 3 tests … OK`. Read in full: test 1 and test 3 run `sys.executable
   -I` from a `tempfile` directory with a 120 s timeout; test 1 checks the seven names in
   `sys.modules`; test 2 walks every statement but function and lambda bodies and names file, line
   and module; test 3 checks the usage line, an empty working directory and `REPO_ROOT/var`
   before and after.
7. **Isolation.** From an empty scratch directory, `env -u PYTHONPATH`: §3.1's import exits 0;
   `import RunRegistry` and `import config` each give `ModuleNotFoundError`.
8. **The probes.** The `json`, `numpy` and `ShardedPool` diffs and (d) replayed: `json` passes
   the suite; `numpy` fails tests 2 and 3 (correction 1); `ShardedPool` fails tests 1 (`datastorekit`,
   `ray`, `sqlalchemy` loaded) and 2; (d) fails test 3. The suite is 3 OK after each; no Ray
   process afterwards.
9. **The records.** The log has every section of README §5.1, `pip freeze`, the check's whole
   output, the D-name line citing an SGK path (`stores.py:197`), 0 → 3, and all twelve diffs. The
   six items of `PROVENANCE.md` are there, the hashes and subjects right. §3's package lines were
   spot-checked in the package (`DEFAULT_ROOT`'s and `DEFAULT_STORES_ROOT`'s uses, the
   `git_provenance()` calls, `fingerprint_store` `:1445`, `_repo_path` `:176`): true at `4e0d715`.
   The index counts 7, as its header says. `black --check runregistrykit docs`: 6 files unchanged.

*Residue fixed in the follow-up.* "this commit" → `4e0d715` on this board and in the log; 01 marked
reviewed here, in README §2 and its header, and in `prompts/INDEX.md`; this notes line.

*Accepted as recorded.* The log's one UNINTENDED DRIFT (RayPoolKit's `pyproject.toml` read, read
only, beyond the two files the brief named) changed nothing. Its observations need no issue: the
`.py`-only walk is the prompt's rule, and 02 extends the check for whatever it adds;
`stores.py:1567`'s "(prompt 01's log)" is SGK's and is recorded under
`[00-package-prose-names-sgk]`, which 05 owns. **Nothing opened**; the index stays at 7.

**Orchestrator review of prompt 02 (2026-10-14).** Dispatched from `1f9b5b0` to one Sonnet
subagent, with the note's §0: its facts, six corrections and readings of the prompt ((m2) fails
more than the prompt names; `black` from the command line infers `py312`, `py313` where
`black.Mode()` does not; the instances overlap in `test_store_copy_move.py`; how to replay 01's
breakages; the suite's time; the pending mechanism kept) and its two recommendations (D-fmt counted
from T to `black(T)`; `black` under the cannot-run guard). Reviewed against its commit `8155445`,
with nothing landed after it. **Every check of the note's §3 passed**, and acceptance 1–3 are met.
No stop condition fired.

*At dispatch.* The note's gate and the prompt's held at `1f9b5b0`: the tree clean, this checkout
the only worktree, no `var/`; `git diff --stat 4e0d715 HEAD -- runregistrykit docs pyproject.toml
PROVENANCE.md` empty; the check exited 0 and the suite was 3. SGK's `HEAD` `14bcac0`, clean. No Ray
process; `RAY_ADDRESS` unset.

*The checks.*
1. **Scope.** `8155445` touches 15 files, the prompt's §6 list. The three modules,
   `tests/__init__.py`, `test_package_imports.py` and `pyproject.toml` are unchanged from
   `4e0d715`; `CLAUDE.md` changes in its Tests bullet only. No `venv/`, `*.egg-info`, scratch file
   or `var/`.
2. **The files.** `git ls-files runregistrykit` is 01's five and the eight. An independent re-port
   from `a45aefc` (`perl` for D-name and D-fix, `black.format_str(…, mode=black.Mode())`) gives
   all eight committed files byte for byte (`cmp`).
3. **Equivalence, by running.** From an `env -i` shell the check exits 0: 12 checked, D-name 106,
   D-fix 5, D-fmt 12 in 3 hunks, 3 pending, 11 absent, 1 new. Its 467 lines of output equal the
   log's (`diff`).
4. **Equivalence, by reading.** The check read in full: the table's eight rows *ported by 02*, the
   three 04 rows pending, every blob unchanged; SGK read only through `git -C`; `black` imported
   under the guard and pinned to `25.1.0`; T by the two substitutions on every line; the package
   compared with `black(T)`; D-fmt counted from T to `black(T)`; completeness on `RunRegistry` and
   `StoreFixtures`; no line number in a rule; the frozen tree, the walk and the pending mechanism
   as 01 made them; the docstring stating the rule and the pin.
5. **The check bites.** All 21 diffs of the log extracted and replayed in `bash` (`--check`,
   apply, `-R --check`, reverse), each exiting 1 and naming the line, row or file as the log
   records, the tree clean after each: 02's (a)–(g); 01's (a)–(i), (h) applying with an offset; and
   (m1)–(m3) and the two uncaught candidates. The orchestrator's own, not in the log:
   `test_store_copy_move.py` `:73-76` collapsed back to T's single line (the package equal to T,
   not to `black(T)`) exits 1; `import json` and `import os` swapped in `test_store_sidecar.py`
   exits 1; the pin edited to `25.1.1` exits 2, `CANNOT RUN`.
6. **The tests.** `Ran 108 tests in 14.0s`, OK; the per-module counts by loader are the note's.
   `git status --short --ignored` the same before and after but for `__pycache__/`; no `var/`; no
   Ray process before or after. `black --check runregistrykit docs`: 14 files unchanged.
7. **The mutations.** (m1) failures=2, errors=1, in `TestPackageProvenance`; (m2) failures=4,
   errors=8, across `test_store_copy_move`, `test_store_amend`, `test_store_sidecar` and
   `test_store_command_line` (correction 1); (m3), `amend_sidecar` dropping its `amend` history entry
   (`stores.py:2173`), failures=6, errors=9, in `test_store_amend` and
   `test_store_amend_residuals`. Each as the log records; the suite 108 OK after each.
8. **The issues.** `[02-the-ported-tests-name-sgk]` opened with impact and next step, owner 05; its
   lines spot-checked in the package (`test_run_registry.py:21, 102, 125, 482, 662`,
   `store_fixtures.py:36, 49-50, 53-54, 85`, `test_store_sidecar.py:36, 43, 349, 372, 500`,
   `test_store_amend.py:203`, `shard_store_fixtures.py:37-38, 91, 131, 135`). The four narrowed
   issues' package lines true at `8155445`; `[00-a-refusal-matches-datastorekit-message-text]`'s next
   step now 04's.
9. **The records.** The log has every section of README §5.1, the check's whole output, the
   per-class counts, the instances accounted for, 3 → 108, and every diff. `PROVENANCE.md` and
   `CLAUDE.md` as the prompt's §2.6. The index counted 8, as its header said.

*Residue fixed in the follow-up.* "this commit" → `8155445` on this board, in the log and in
`prompts/INDEX.md`; 02 marked reviewed here, in README §2 and its header, and in
`prompts/INDEX.md`; one prose line of `PROVENANCE.md` and this board's header rewrapped; this
paragraph and the notes line.

*Opened by the review.* The log's observation that two sidecar-reader mutations pass the suite
(`stores.py:579`, the `bool` guard on `sidecar_format`; `:589`, `fullmatch` → `match` on
`store_id`) is a gap in what pins the reader's acceptance rules, which are part of the registry's
interface, and 04 rewrites the reader's shape check. No test of 04's SGK sources pins either guard.
Opened as `[02-the-sidecar-readers-guards-are-unpinned]`, owner 04; the index goes to 9.

*Accepted as recorded.* The log's ten deviations (two STRUCTURALLY REQUIRED, eight IMPLEMENTATION
CHOICE, no UNINTENDED DRIFT) change nothing the prompt fixes. Its other observations need no issue:
`DEFAULT_STALE_AFTER` unpinned is the prompt's own note; `test_package_imports.py` naming
`RunRegistry` and `StoreFixtures` on purpose is for 05's guard (U10) to allow, and 05's prompt will
measure it.

**Orchestrator review of prompt 03 (2026-10-14).** Dispatched from `f02abc7` to one Opus subagent,
with the note's §0: its facts, ten corrections and readings of the prompt (the gate's diff read from
`71f59ed`; the one docstring the four-name grep needs changed; the call site §2.5 omits,
`stores.py:1663`, and an `ast` walk for every site no 03 test reaches; when `read_sidecar` locates;
the test shapes (m3), (m6), (m7) and (m8) need; which test reads this checkout's commit; the two
child processes; the suite's time; three small readings) and its two recommendations (`read_sidecar`
locates only for a tombstone; a test of the bare-repository refusal). Reviewed against its commit
`035e4b5`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance 1–3
are met. No stop condition fired.

*At dispatch.* The note's gate held at `f02abc7`, with the prompt's gate read from `71f59ed`
(correction 1): the tree clean, this checkout the only worktree, no `var/`; the suite 108 OK in
15.2 s; the check exited 0 from a worktree of `8155445`. No Ray process; `RAY_ADDRESS` unset.

*The checks.*
1. **Scope.** `035e4b5` touches 20 files, the prompt's §6 list. `pyproject.toml`, `README.md`,
   `LICENSE`, `.gitignore`, `tests/__init__.py`, `shard_store_fixtures.py` and
   `test_store_amend_residuals.py` are unchanged from `71f59ed`; `git ls-files runregistrykit` is 02's
   thirteen and the three new files. `CLAUDE.md` changes in its Tests bullet only. The check's module
   body after its docstring is the same by `ast.dump`, and the docstring gains one paragraph.
   `PROVENANCE.md` gains "Since the import" and changes its paragraph on the check only.
2. **The check retired.** From a fresh worktree of `8155445`, the check exits 0 with the log's
   summary line; the worktree removed, this checkout alone in `git worktree list`.
3. **The ported tests.** Every hunk of `git diff 8155445 035e4b5` over the seven ported files and the
   import test is F-client, R-root (11 calls; the alias at `test_store_amend.py:42` unchanged, log
   deviation 16), R-cwd, U9 or the import test's two edits; every changed assertion is R-root's or
   U9's. The loader's test ids are 02's 108 but for the one rename, plus `test_client_root`'s 27.
4. **By reading.** `client.py` as the prompt's §2.2–§2.4: the refusals naming the file, the walk to a
   file only, the override, §2.4's three steps with realpaths compared and `root = found` unchanged in
   the common case, nothing at import. `begin()` locates before reading the results sidecar or making
   a directory, with provenance from its start; `Run` locates only to resolve a relative recorded
   path; `list_runs` only without `root`. In `stores.py` the nine public functions take
   `client_root` and private helpers never locate; `read_sidecar` locates only for a well-formed
   tombstone. The `ast` walk finds 30 calls of `_repo_path`, `_resolve` and `git_provenance`, every
   one passing its argument, none of the three with a default. The CLI as §2.5. Layer C,
   `FINGERPRINT_FORMAT` and the `config.datastore` import (`stores.py:1525`) are untouched.
5. **By probing.** *C4:* a scratch client whose run, unit ledger, live sidecar and hand-built
   tombstone (listing a relative shard file) were written by `8155445`'s package, exported into it so
   that its `REPO_ROOT` was the client, with root-relative paths as SGK's records have; read with
   `035e4b5` and an empty config, `checkpoint_path`, `results_path`, `known()`, the live sidecar's
   fields and the tombstone's problem (read from a subdirectory) are what the old package gave, and
   `list` and `store show` find them. *Q3:* runs begun from a linked worktree and from one nested at
   `.claude/worktrees/` on another commit are recorded under the main checkout's `var/runs`, with the
   worktree's `git_head` and script hash, the script absolute and root-relative respectively.
   *Refusals:* from an empty directory, `--help` exits 0, `list` and `store show` exit 1 with the
   "No runregistrykit.toml" message, and a refused `begin(root=…)` leaves its runs root empty.
6. **The suite.** `Ran 135 tests in 41.1s`, OK; the per-module counts the log's. `git status --short
   --ignored` the same before and after; no `var/`; this checkout the only worktree; no Ray process.
   The four-name grep finds nothing; `black --check runregistrykit docs`: 17 files unchanged. From a
   `git archive` export with no `.git` (its own package imported), exactly one test fails,
   `test_manifest_carries_the_provenance_triple`, as `CLAUDE.md` now says.
7. **The mutations.** (m1)–(m8) extracted from the log and replayed in `bash` (`--check`, apply,
   `-R --check`, the suite, reverse), each failing exactly the tests the log names, the tree clean
   after each. The orchestrator's own: (o1) a relative `runs_root` joined to `found` fails the two
   worktree tests; (o2) the subdirectory mapping dropped fails
   `test_a_config_in_a_subdirectory_maps_to_the_same_subdirectory`; (o3) the bare refusal removed
   fails `test_a_bare_repositorys_worktree_is_refused`; (o4) `find_client_root()` at `client.py`'s
   module scope breaks the package's import, and discovery fails; (o5) the CLI returning 0 on a
   `ConfigError` fails three subtests of
   `test_outside_any_client_a_store_command_exits_1_and_writes_nothing`; (o6) `Run`'s relative paths
   resolved against the working directory fails
   `test_a_run_reads_its_status_with_no_config_and_locates_only_to_resolve`.
8. **The issues.** The two closed in §4 with what resolved them and the tests that pin them; their
   rows gone from the index. Each of the other seven carries its 03 package lines, spot-checked in
   the package at `035e4b5` (`stores.py:202, 412, 573, 578, 588, 629, 1210, 1284, 1404, 1473, 1525,
   1550, 1598-1599, 1858, 1905`; `__main__.py:274, 297`; the moved test lines of
   `[02-the-ported-tests-name-sgk]`).
9. **The records.** The log has every section of README §5.1, the check's summary from 02's tree,
   every instance accounted for, the call-site table, 108 → 135 with the per-module counts and the
   time, all eight diffs, and 21 deviations, each classified (8 STRUCTURALLY REQUIRED, 13
   IMPLEMENTATION CHOICE). `PROVENANCE.md`, `CLAUDE.md`, the index (7, by counting) and
   `prompts/INDEX.md` as the prompt's §4.3.
10. **The interface.** No record changes form: the manifest's, `status.json`'s and the sidecar's
    keys are those at `8155445`, by the diff and by the C4 probe; only `packages`' content differs.

*Residue fixed in the follow-up.* "this commit" → `035e4b5` on this board, in the log, in
`prompts/INDEX.md` and in `PROVENANCE.md`; 03 marked reviewed here, in README §2 and its header, and
in `prompts/INDEX.md`; this paragraph and the notes line. `PROVENANCE.md`'s "Re-running the check"
opened with "From the repository root", which fails on any tree after `8155445`; its first line now
says the command is `8155445`'s and points to the section's end (the log's third observation).

*Accepted as recorded.* Log deviation 21 records that the note's dispatch said to read no client
while the prompt's §2.9 runs the check, which reads SGK through `git -C`; that was the note's error,
README §5 rule 5 allows the read, and the agent ran the check once, as the prompt requires. The
log's other observations need no issue: provenance at `finish(fingerprint=True)` is the prompt's rule
and 04 writes `taken` anew; the prose naming the old layout and `git_provenance()` is 05's
(`[00-package-prose-names-sgk]`); the unused `import runregistrykit` in `test_store_command_line.py`
is harmless and outside R-cwd; the package's `git` inheriting `GIT_DIR` is by design; and the retire
path's threading, checked here by the `ast` walk, is reached by 04's ported tests. **Nothing
opened**; the index stays at 7.

**Orchestrator review of prompt 04a (2026-10-15).** Dispatched from `9dc34a5` to one Opus subagent,
with the note's §0: its facts, ten corrections and readings of the prompt (the gate's diff read from
`2ecb99d`; the two 03 tests §2.3 and §2.4 overturn; `fingerprint_store`'s docstring and the `taken`
stamp now before the read; the test shapes (m5) and (m10) need; the loader, `sys.path` and
`sys.modules` in tests; (m3) and D4 already pinned by 02's tests; the class fixture; what the ported
literals assume of the neutral store; the suite's time) and its two recommendations (a type-and-text
check against the reader's own exception, with a `StoreSchemaMismatch` case; a refusal-precedence
test with an unimportable fingerprinter). Reviewed against its commit `c81ad06`, with nothing landed
after it. **Every check of the note's §3 passed**, and acceptance 1–3 are met. No stop condition
fired.

*At dispatch.* The note's gate held at `9dc34a5`, with the prompt's gate read from `2ecb99d`
(correction 1): the tree clean, this checkout the only worktree, no `var/`; the suite 135 OK in
39.1 s. No Ray process; `RAY_ADDRESS` unset.

*The checks.*
1. **Scope.** `c81ad06` touches 15 files, the note's §0 list and the records. `runregistrykit/__init__.py`,
   `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `CLAUDE.md`, `docs/extraction/`,
   `tests/__init__.py`, `store_fixtures.py`, `shard_store_fixtures.py` and the other 02 and 03 test
   files are unchanged from `2ecb99d`; `git ls-files runregistrykit` is 03's sixteen and the four new
   files. `test_package_imports.py` changes in `MODULES` only, `test_client_root.py` in correction 2's
   two tests only, `client_fixtures.py` in its default config and `enter_client_root_for_class` only.
2. **By reading.** `fingerprint.py` as §2.2: standard library at module scope, the protocol, the
   constructor's refusals, `take` returning the reader's exception untouched, `describe` the old
   `_print_fingerprint` text from `classes:` on line for line; the loader's four refusals, each a
   `ConfigError` naming the file and the spec. `client.py`'s `[stores]` holds `fingerprinter` only,
   checked by form at read time. In `stores.py` layer C, `FINGERPRINT_FORMAT`, `hashlib` and
   `Counter` are gone; `require_fingerprinter` follows the locate in all seven operations and in
   `write_listing`; `fingerprint_store`'s step 1 is unchanged, the loader follows it, then `taken`
   and `take`; the `malformed` entry keeps its six keys and text. Outside `fingerprint.py` no package
   module reads a fingerprint's `classes`, `tag_sets` or `problems` (by grep, each hit read). The CLI
   checks D4 in `_store` and loads the fingerprinter after `fingerprint_store`.
3. **The port, independently.** The orchestrator's own re-port of SGK's module from `a45aefc` (D-name,
   X-drop by `ast`, N-fix, N-class from the log's mapping table, `black`) differs from the committed
   file only by the shim lines, the two F-client lines, the N-fix import of `_factories` and the two
   U7 variants (and `COMPUTE_TARGETS`' layout, a trailing comma of the re-port's). The loader's ids are
   SGK's 29, by class as §2.8 counts.
4. **The neutral store.** Nine factories on public names (`SQLAFactoryBase`, `build_schema`, the
   contract's `TAG_*` and `VERSION_*`, `shard_file_name`, `InventorySpec`, `Parent`); no
   `ShardedPool` attribute, no pool, no Ray; `FIXED_TIMESTAMP` SGK's; `shard_keys` written to a table
   of its own that nothing reads.
5. **By probing**, in a scratch client whose config names a module of its own root
   (`DatastoreKitFingerprinter(FACTORIES, 7)`), not otherwise importable, from a subdirectory under
   `-I`: `store create`; `finish(fingerprint=True)` records one fingerprint, format 7,
   `encoding_format` 1, in the status and the sidecar alike; `store fingerprint` matches and lists,
   the listing's word 6 `encoding_format`; `store show` loads neither `ray` nor `sqlalchemy`. An
   SGK-shaped fingerprint (format 6, no `encoding_format`) reads with no problem, and with `classes`
   removed too; `store fingerprint` then exits 1 with DatastoreKit's `format` and `encoding`
   entries; `encoding_format: "1"` is a problem. With `[stores]` removed, all eight `store` commands
   exit 1 naming the config file and change nothing; `list` and `begin` run, and `finish` records
   the `ConfigError`. The loader's refusals fire where §2.2 and §2.3 say (the form at read time).
6. **The suite.** `Ran 186 tests in 57.0s`, OK; the per-module counts the log's. `git status --short
   --ignored` the same before and after; no `var/`; this checkout the only worktree; no Ray process.
   §3.3's import check exits 0; §3.4's grep finds the log's three lines; `black --check runregistrykit
   docs`: 21 files unchanged.
7. **The mutations.** (m1)–(m11) extracted from the log and replayed in `bash` (`--check`, apply,
   `-R --check`, the suite, reverse), each failing exactly the tests the log names, the tree clean
   after each. The orchestrator's own: (o1) `create_sidecar` loading the fingerprinter in place of the
   D4 check fails `test_show_create_adopt_copy_and_move` and two `TestPrecedence` tests; (o2) no `bool`
   guard on `encoding_format` fails `TestOpacity.test_encoding_format_if_present_is_an_integer`; (o3)
   the loader without its `Fingerprinter` check fails the refusal test's "not a fingerprinter"; (o4)
   another `[stores]` key accepted fails the renamed 03 test and a `TestProtocolAndLoader` subtest;
   (o5) a spec with no colon accepted fails three subtests; (o6) `take` dropping `taken` fails seven
   tests; (o7) a `bool` format accepted fails the constructor test; (o8) a private `ShardedPool` call
   in the neutral store fails `TestNeutralStore.test_it_is_built_from_public_names_only`.
8. **The issues.** The three closed in §4 with what resolved them and the tests that pin them; their
   rows gone from the index. The other four carry their 04a package lines, spot-checked in the
   package at `c81ad06` (`stores.py:104, 109, 1181, 1365-1366, 1410, 1420, 1626, 1673, 1841`;
   `fingerprint.py:128`; the port's lines of `[02-the-ported-tests-name-sgk]`).
9. **The records.** The log has every section of README §5.1, the mapping table, every instance
   accounted for, the port's diff, 135 → 186 with the per-module counts and the times, all eleven
   diffs, and 22 deviations, each classified (7 STRUCTURALLY REQUIRED, 15 IMPLEMENTATION CHOICE).
   `PROVENANCE.md`, the index (4, by counting) and `prompts/INDEX.md` as the prompt's §4.3.
10. **The interface.** No record changes form: the manifest's, `status.json`'s and the sidecar's keys
    are those at `2ecb99d`, by the diff and by the probe's records; `taken`'s keys are `TAKEN_KEYS`;
    a fingerprint gains `encoding_format`, the one planned addition.

*Residue fixed in the follow-up.* "this commit" → `c81ad06` on this board, in the log, in
`prompts/INDEX.md` and in `PROVENANCE.md`; 04a marked reviewed here, in README §2 and its header, and
in `prompts/INDEX.md`; this paragraph and the notes line. 03's residue: §4's
`[00-the-recorded-distributions-are-sgks]` still read "by 03 (this commit)", now `035e4b5`.

*Opened by the review.* The loader accepts a **class** that has the four methods: a
runtime-checkable protocol checks only that the attributes exist, and a class has them. A config
naming `module:DatastoreKitFingerprinter` (the class, not an instance), the likeliest slip a client
makes, loads, and every fingerprint then fails at `take` with a `TypeError`, recorded by `finish` as
`fingerprint_error`, never a `ConfigError` naming the file (probed). The prompt's §2.2 asks for the
`isinstance` check only, so the agent built what it asked. Opened as
`[04a-the-loader-accepts-a-fingerprinter-class]`, owner to be put to the user; the index goes to 5.

*Accepted as recorded.* The log's observations need no issue: the ported module's unused `import
runregistrykit` and its docstring naming the deleted `stores.fingerprint_of` are rule 9's and 05's
(recorded under `[02-the-ported-tests-name-sgk]`); the D4 `ConfigError` not ending "Nothing was
written…" as `retire_store`'s and `amend_sidecar`'s docstrings promise is prose for 05
(`[00-package-prose-names-sgk]`'s rewrite); the loader leaving each client root on `sys.path` is the
prompt's rule.

**Orchestrator review of prompt 04b (2026-10-15).** Dispatched from `5177ffa` to one Opus session,
with the note's §0: its facts, ten corrections and readings of the prompt (the gate's diff read from
`d035ffb`; the load in `retire_store` a check whose result nothing uses, and the CLI needing no
change; the refusal order §2.3 states pinned by no test it asks for; the probe's "before"; the
class refusal before the protocol check; the `IMPORTS` child; the trial port's counts; the suite's
time; the SGK prose the port carries; `PROVENANCE.md`'s rows) and its one recommendation (a
five-case precedence test for the load). Reviewed against its commit `5302a6f`, with nothing landed
after it. **Every check of the note's §3 passed**, and acceptance 1–3 are met. No stop condition
fired.

*At dispatch.* The note's gate held at `5177ffa`, with the prompt's gate read from `d035ffb`
(correction 1): the tree clean, this checkout the only worktree, no `var/`; the suite 186 OK in
62.2 s. SGK at `14bcac0`, clean. No Ray process; `RAY_ADDRESS` unset. The orchestrator's trial port
into an export of `d035ffb` gave 51 OK in 28.9 s, and the hazard U14 answers reproduced there (a
store that could be fingerprinted retired under the flag, by a module that exists nowhere and by
the class).

*The checks.*
1. **Scope.** `5302a6f` touches 10 files, the note's §0 list and the records. `git diff d035ffb
   5302a6f` over `__init__.py`, `__main__.py`, `client.py`, `pyproject.toml`, `README.md`, `LICENSE`,
   `.gitignore`, `CLAUDE.md`, `docs/extraction/`, `tests/__init__.py`, the fixtures, every 02, 03 and
   04a test file but `test_fingerprinter.py`, the campaign README and the prompt is empty; `git
   ls-files runregistrykit` is 04a's twenty and the two new modules. `stores.py` changes in
   `retire_store` only (the load and its comment, one docstring sentence), `fingerprint.py` in
   `load_fingerprinter`'s class refusal and the module docstring's sentence only.
2. **By reading.** `load_fingerprinter(client)` sits at the head of the first-retirement branch
   (`stores.py:1675`), after steps 1 and 2 and before `closed_store_files`, outside every `try`; the
   completion branch does not reach it; no refusal's text changes; the flag branch still records
   `str(e)` and `type(e).__name__` of whatever `fingerprint_store` raises. The class refusal
   (`fingerprint.py:188-194`) is a `ConfigError` naming the file and the spec and saying to name an
   instance. The eight new tests are those the log lists, the precedence test's five cases among
   them.
3. **The port, independently.** The orchestrator's own re-port of SGK's two modules from `a45aefc`
   (D-name, D-fix, N-fix, N-class, R-root, R-cwd, `black`; the dispatch script) differs from the
   committed files only by the shim block's place and its comment's wording; the references module
   is identical. Its counts are the log's. The loader's ids are SGK's 51, by class as §3.3 counts.
4. **By probing**, in a scratch client in an export of `5302a6f`, a full neutral store with a
   registry sidecar and a recorded fingerprint: with the config naming a module that exists nowhere,
   and then the class `DatastoreKitFingerprinter`, `retire_store` plain, with the flag, in a dry run
   and with both each raised the loader's `ConfigError`, unwrapped, and `store retire
   --without-fingerprint` exited 1 with `!!` naming the config file and the spec; the six files hashed
   the same after every call. An empty reason was refused first; a `-wal` beside the primary gave
   the `ConfigError`, not the plan's refusal; a retirement interrupted at the second `os.unlink`
   under the neutral config completed under the broken one, deleting the four files left. Under the
   neutral fingerprinter the flag still applies: a corrupt shard is retired with the reader's error
   recorded, a `-wal` is refused, and a dropped `shards` table is refused "even under
   --without-fingerprint".
5. **The suite.** `Ran 245 tests in 92.4s`, OK; the per-module counts the log's. `git status
   --short --ignored` the same before and after; no `var/`; this checkout the only worktree; no Ray
   process. §3.4's grep finds `test_package_imports.py:32` alone; `black --check runregistrykit
   docs`: 23 files unchanged.
6. **The issues.** The two closed in §4 with what resolved them and the tests that pin them; their
   rows gone from the index. `[00-a-refusal-matches-datastorekit-message-text]` narrowed, owner
   none, its row kept; `[02-the-ported-tests-name-sgk]` gains the port's lines. The package lines
   spot-checked at `5302a6f` (`stores.py:1365-1366, 1630, 1675, 1680, 1848`; `fingerprint.py:129,
   188-194`; `test_store_retire.py:64, 404, 797, 956`).
7. **The mutations.** (m1)–(m10) extracted from the log and replayed in `bash` (`--check`, apply,
   `-R --check`, the suite, reverse), each failing the tests the log names with the counts it
   records, the tree clean after each. (m8)–(m10) are the note's (o1)–(o3). The orchestrator's own:
   (o5) the load removed and the flag branch re-raising a `ConfigError` fails six subtests of
   `TestRetireLoadsTheFingerprinterFirst` and `test_the_fingerprinter_comes_before_the_plan`; (o6) a
   load failure turned into the flag's condition fails both `TestRetireLoadsTheFingerprinterFirst`
   tests and the precedence test's plan case; (o7) the stores root compared by text fails
   `test_through_a_stores_root_that_is_a_symlink`. (o4), the class refusal moved after the protocol
   check, **passes**, and rightly: a class passes the protocol check, so it reaches the refusal
   either way, and the two orders behave alike. The note's correction 5 ("or it never fires") was
   wrong; the agent built the order it asked for, which is harmless.
8. **The records.** The log has every section of README §5.1, the port script's summary and diff,
   every instance accounted for, 186 → 245 with the per-module counts and the times, all ten diffs,
   and 17 deviations, each classified (5 STRUCTURALLY REQUIRED, 9 IMPLEMENTATION CHOICE, 3 as found;
   no UNINTENDED DRIFT). `PROVENANCE.md`, the index (4, by counting) and `prompts/INDEX.md` as the
   prompt's §4.3.
9. **The interface.** No record changes form: the diff touches no writer; the probe's tombstones
   carry the ten keys and a `fingerprint` condition of `condition` with `digest` or with `error` and
   `error_type`, as at `d035ffb`.
10. **The handover.** The log's last section says every test README §4 imports is ported, the suite
    is 245 in about 90 s, and lists the SGK prose and the two docstrings 05 rewrites.

*Residue fixed in the follow-up.* "this commit" → `5302a6f` on this board, in the log, in
`prompts/INDEX.md` and in `PROVENANCE.md`; 04b marked reviewed here, in README §2 and its header, and
in `prompts/INDEX.md`; this paragraph and the notes line.

*Accepted as recorded.* The log's observations need no issue: `load_fingerprinter`'s docstring not
naming the class refusal, and the loader's `ConfigError` not ending "Nothing was written or deleted"
as `retire_store`'s docstring says every refusal does, are prose for 05
(`[00-package-prose-names-sgk]`, where the board now records both); `Run.finish` recording the
loader's `ConfigError` for a class, where it recorded `take`'s `TypeError`, is the intended effect of
§2.4; the ported SGK prose is rule 9's and 05's. **Nothing opened**; the index stays at 4.

### 1.1 Items

| Item | Prompt | What | State |
|---|---|---|---|
| **I1** | 01 | the package skeleton; the three modules under D-name | ✅ 2026-10-14: D-name on 23 lines (6, 13, 4), D-fmt 0; the import test, 3 tests |
| **I2** | 01 | `PROVENANCE.md`; `compare_with_source.py` (G1, package side) | ✅ 2026-10-14: the check exits 0 and bites on (a)–(i) |
| **T1** | 02 | the 29 core and 76 shard-fixture tests, and their fixtures | ✅ 2026-10-14: the eight files ported; D-name 83, D-fix 5, D-fmt 12 lines in 3 hunks; the suite is 108, OK; the check extended and bites on (a)–(g), 01's (a)–(i) and (m1)–(m3) |
| **R1** | 03 | the config file and the root rule (C1–C3, C9; Q2, Q3) | ✅ 2026-10-14: `runregistrykit.toml` read by the new `runregistrykit/client.py`; the walk, `client_root=` and `--client-root`; a linked worktree recorded under the main checkout, a bare repository's refused; provenance from the start directory; `REPO_ROOT`, `DEFAULT_ROOT`, `DEFAULT_STORES_ROOT` deleted; no config a `ConfigError`; C4's relative paths kept; the check retired, exit 0 from `8155445`; 27 new tests, the suite 135; (m1)–(m8) caught |
| **R2** | 03 | the recorded distributions (C5, U9) | ✅ 2026-10-14: `RECORDED_DISTRIBUTIONS` deleted; `packages` is `runregistrykit` and the config's `distributions`; the pinning test renamed `test_the_recorded_names_are_the_registry_and_the_configs`; (m4) caught by three tests |
| **F1** | 04a | the fingerprinter protocol and the shipped fingerprinter; layer C and the format deleted (C6, C7) | ✅ 2026-10-15: `runregistrykit/fingerprint.py` (`Fingerprinter`, `DatastoreKitFingerprinter`, `load_fingerprinter`, `require_fingerprinter`); `[stores] fingerprinter` checked by form at read; every store operation and `store` command refused without one (D4), the check importing nothing; layer C, `FINGERPRINT_FORMAT`, `hashlib` and `Counter` gone from `stores.py`; `fingerprint_store`'s order, refusals and writes kept; (m3)–(m7), (m10), (m11) caught |
| **F2** | 04a | what the package reads of a fingerprint (U7) | ✅ 2026-10-15: the reader requires an integer format, a 64-hex digest, an object `taken`, and an integer `encoding_format` only if present; `classes` not read; the CLI prints the rest through `describe`; (m1), (m2) caught |
| **T2a** | 04a | the neutral store; `test_store_fingerprint`'s 27 and `TestFormats`' 2 ported | ✅ 2026-10-15: `runregistrykit/tests/neutral_store.py` on ten public `datastorekit` names; the 29 ported (SGK's ids less `TestGolden` 3 and `TestDrivers` 1), the port script's output differing from the committed file by the shims, the F-client lines and the two U7 variants only; `test_fingerprinter.py`, 22 tests; the suite 186 |
| **T2b** | 04b | the retire tests' 51 ported onto the neutral store | ✅ 2026-10-15: `test_store_retire` 41 and `test_store_retire_references` 10, SGK's ids by class; the port script's output differing from the committed files by the `compare_fingerprints` shim only; D-name 18, D-fix 1, N-fix 3, N-class 1, R-root 30, R-cwd 3, D-fmt 13 hunks; no F-client; `test_an_unreadable_shards_table` reaches the DatastoreKit text match, (m1) fails it; (m2), (m3), (m7) caught; the suite 245 |
| **F3** | 04b | U14: `store retire` loads the fingerprinter before it fingerprints; the loader refuses a class | ✅ 2026-10-15: `retire_store` loads the fingerprinter on a first retirement after steps 1 and 2 and before the plan, its `ConfigError` unwrapped and nothing written, under the flag or not, in a dry run and from the command; the completion path loads none; `load_fingerprinter` refuses a class before its protocol check; 8 tests in `test_fingerprinter.py`; (m4)–(m6), (m8)–(m10) caught |
| **P2** | 05a | the no-client guard, its vocabulary and its known hits (U10, U16) | ✅ 2026-10-15: `docs/extraction/measure_client_vocabulary.py` writes `runregistrykit/tests/data/client_vocabulary.json` through `git` at SGK `14bcac0`, ChamPBH `c21cdfb`, SI `5fb4a1d` (38 / 27 / 30 registry keys, 194 / 80 / 101 columns, 14 / 11 / 15 packages, 26 / 10 / 6 campaigns, 17 listed words); `test_package_is_generic.py` scans all 24 files, itself included, by four word scans and an import rule, 22 tests; `known_hits.json` holds 69 hits in the package modules (30 entries, 05b's) and 137 in the tests (83 entries, 05c's), written by the guard's own scans; the guard holds none; (m1)–(m11) caught |
| **N1** | 05a | the public names (`slugify`, `__all__`) and the licence header (U11, U12) | ✅ 2026-10-15: `_slug` is `slugify` (no alias; `run_id` and `begin()` signatures unchanged); each of the five modules declares a sorted `__all__` (20, 26, 4, 4, 1 names) and begins with the 14-line Apache header; `test_public_names.py`, 8 tests |
| **P1** | 05b | the package modules' prose, the output and the README's rules (C8) | ⬜ |
| **T3** | 05c | the tests' SGK names and prose renamed (U16) | ⬜ |
| **V1** | 06 | versions, CI, `v0.1.0` | ⬜ |
| **A1** | 07 | the three checklists and their script (SGK's E2) | ⬜ |
| **Z1** | 08 | the verification document; the close | ⬜ |

**Legend.** ⬜ not yet · ✅ done.

## 2. Gates (README §7)

| Gate | Status |
|---|---|
| **G1** | **source side holds** 2026-10-14: `git ls-tree -r a45aefc -- RunRegistry/` equals SGK's frozen table (its board §2.1), 25 rows; unchanged to SGK `14bcac0`. **Package side holds for 01's files** 2026-10-14 (`4e0d715`): `docs/extraction/compare_with_source.py` exits 0: the 25 rows and the shard fixture's blob equal; `__init__.py`, `stores.py`, `__main__.py` and `tests/__init__.py` equal their sources but for 23 D-name lines (6, 13, 4, 0), none unclassified, none left unrenamed; 11 files pending (8 for 02, 3 for 04); 11 not imported and absent; 1 declared new file. **Package side for 02's eight files holds** 2026-10-14 (`8155445`): the check, extended, exits 0: 12 files checked (4 by 01, 8 by 02); each equals `black` of its renamed source; D-name 106, D-fix 5, D-fmt 12 lines in 3 hunks (all in `test_store_copy_move.py`); 3 files pending (04); 11 not imported and absent; 1 declared new file |
| **E1** | **holds** 2026-10-14: DatastoreKit `v0.4.0` (`c8570e8`, tag object `8e7c1d7`) |
| **G2** | not yet (SGK adopts `v0.1.0` in its `runregistry-extraction` 05–08) |
| **G3** | not yet (CPBH adopts) |
| **G4** | not yet (SI adopts, after its `dk-and-rpk-migration`) |
| **E2** (SGK's) | not yet: `v0.1.0` (06) with SGK's checklist (07) |

## 3. Active and unresolved issues

Seven were opened at planning from README §0.2's measurements of SGK's code at `a45aefc`; 02
opened an eighth, and the orchestrator's review of 02 a ninth; 03 closed two (§4), leaving seven;
04a closed three (§4), leaving four; the orchestrator's review of 04a opened one, leaving five; 04b's writing opened one, leaving six; 04b closed two (§4), leaving four; 05a opened and closed none, and narrowed two. Line numbers are SGK's until 01 imports the code; 01 records
each issue's package lines. **From 01 they are the same numbers** for the three modules: D-name
replaced one line by one line and `black` changed nothing, so every line of them sits where it sat
in SGK at `a45aefc` (01's log; each line below read in the package). 02's package lines are for the
ported tests, read in `runregistrykit/tests/`. **From 03 the three modules' lines are no longer
SGK's**: each issue's *Package lines (03, …)* gives them at 03's commit, and *Package lines (04a,
…)* at 04a's, and *Package lines (04b, …)* at 04b's, and *Package lines (05a, …)* at 05a's, read in
the package.

### `[00-package-prose-names-sgk]`

**Opened:** 2026-10-14, at planning (C8). **Owner:** 05b.

**Assigned (2026-10-15):** to 05b by U15, when 05 was split: 05a's guard lists each of its hits in
the package modules as known, and 05b rewrites the prose and empties them.

49 docstring and comment lines cite SGK's campaigns (21 in `__init__.py`, 28 in `stores.py`), and
others name SGK's A3 store, `realistic_large_x`, `main.py` and SGK's classes (README §0.2). The CLI
prints "the store's own text is in `main.py --inventory`" (`__main__.py:281`), an SGK command.

*Impact.* A reader in this repository or a client cannot follow the citations, and CPBH and SI users
would be sent to a command they do not have.

*Next step.* 05: the prose in the package's own terms, SGK's history in `PROVENANCE.md`, the rules in
the README, and the guard (U10) so it stays that way.

*Package lines (01, 2026-10-14).* The SGK citations sit at README §0.2's C8 lines, now in
`runregistrykit/__init__.py` and `runregistrykit/stores.py`; the CLI text is
`runregistrykit/__main__.py:281`. D-name made one renamed comment cite a path that does not exist
here: `stores.py:197`, `runregistrykit/tests/data/full_store_fingerprint*.json` (01's log). And
`stores.py:1567`'s "(prompt 01's log)" means an SGK campaign's prompt 01 (the comment sits in the
section SGK's `store-retirement` campaign wrote), not this campaign's (01's log, observations).

*Package lines (03, 2026-10-14), read in the package.* The C8 lines README §0.2 names are now
`runregistrykit/__init__.py:70, 74, 369, 372, 454, 503, 511, 589, 624` and
`runregistrykit/stores.py:101, 194-201, 1643, 1653, 2073`; the renamed comment citing a path that
does not exist here is `stores.py:193`, and "(prompt 01's log)" is `stores.py:1598`. The CLI text
is `runregistrykit/__main__.py:288`. 03 rewrote one C8 sentence, `begin()`'s on `packages`, which
named the `dk-and-rpk-migration` campaign (03's log, deviation 15).

*Package lines (04a, 2026-10-15), read in the package.* `__init__.py` is unchanged, its lines as
03's. In `runregistrykit/stores.py` the C8 lines are now `:104` (03's `:101`), `:1410`, `:1420` and
`:1841` (03's `:1643`, `:1653`, `:2073`), and "(prompt 01's log)" is `:1365`. The format history
(03's `:194-201`) and the renamed comment citing a path that does not exist here (03's `:193`) are
deleted with `FINGERPRINT_FORMAT`. 04a's rewritten fingerprint paragraph and section comment keep
the citation "(store-fingerprint prompt 04)" (`:109`, `:1181`). The CLI text "the store's own text
is in `main.py --inventory`" moved, unchanged, from `__main__.py:288` into
`DatastoreKitFingerprinter.describe`, `runregistrykit/fingerprint.py:128`.

*Package lines (04b, 2026-10-15), read in the package.* `__init__.py` is unchanged. In
`runregistrykit/stores.py`, 04b added seven lines inside `retire_store` (`:1533-1536`, `:1673-1675`),
so the C8 lines before them are 04a's (`:104`, `:1410`, `:1420`; "(prompt 01's log)" `:1365`; the
citations `:109`, `:1181`) and 04a's `:1841` is now `:1848`. The CLI text is now
`runregistrykit/fingerprint.py:129` (04b added a docstring line above it). 04b's own prose names
nothing of SGK. Two docstrings 05 rewrites are 04b's observations: `load_fingerprinter`'s list of
refusals does not name the class refusal, and the loader's `ConfigError` in `retire_store` does not
end "Nothing was written or deleted" as the docstring says every refusal does.

**Narrowed (2026-10-15, by 05a, this commit):** every hit of the package modules is now listed by
the guard, by scan, file and word, in `runregistrykit/tests/data/known_hits.json`: 69 hits in 30
entries, all in `__init__.py`, `stores.py` and `fingerprint.py` (`client.py` and `__main__.py`
hold none): the words `A3`, `main.py`, `realistic_large_x`, `handover-A3-baseline-lambdacdm`,
`handover`, and the campaigns `run-registry`, `datastore-portability`, `store-fingerprint` and
`store-retirement` in strings and comments (26 and 8 hits), and 35 citations (`prompts/`, `prompt
01`, `prompt 03`, `prompt 04`, `§0`, `§2`, `§5`, `§6`). Each scan must find exactly its entries, so
a new hit fails and 05b's removal of one must update the file. 05a rewrote no prose.

*Package lines (05a, 2026-10-15), read in the package.* The header (15 lines) and `__all__` moved
every line: `__init__.py` by +15 up to its imports, +38 from `TERMINAL_STATES` to `slugify`, +40
after it; `stores.py` by +44; `fingerprint.py` by +22; `client.py` and `__main__.py` by +17. So
`stores.py`: "(prompt 01's log)" `:1409`, the section comments `:1225` and `:1400`, the docstring
citation `:124`; `fingerprint.py`: the CLI text naming `main.py --inventory` `:151`. Nothing of
05a's own names a client.

### `[00-the-shard-fixtures-reach-into-shardedpool]`

**Opened:** 2026-10-14, at planning. **Owner:** none; 02 carries the fixture (U4) and records the
attributes it touches in the package.

SGK's `StoreFixtures/shard_store_fixtures.py`, which the 76 shard-fixture tests use, builds a
`ShardedPool` with `object.__new__` and sets or calls about 13 private attributes (`:30-71`), and
`store_fixtures.assertOpens` uses two more (`:159-166`).

*Impact.* Only this package's tests are affected, never a client. A DatastoreKit release that renames
one of those internals breaks the suite here with no change in the package's behaviour.

*Next step.* Pin `datastorekit` exactly in CI (U13), so that a change is seen when the pin moves. A
public way to write and reopen a small store would be a request to DatastoreKit (README §8).

*Package lines (01, 2026-10-14).* None yet: the fixture is pending, 02
(`runregistrykit/tests/shard_store_fixtures.py`, `store_fixtures.py`).

*Package lines (02, 2026-10-14), read in the carried files.* `bare_pool`
(`runregistrykit/tests/shard_store_fixtures.py:30-43`) builds a pool with `object.__new__(ShardedPool)`
and sets ten private attributes: `_db_name`, `_primary_file`, `_timeout`, `_ShardKeyType_name`,
`_replicated_tables`, `_sharded_tables`, `_shard_db_files`, `_shard_records`, `_shard_keys` and
`_engine` (`:33-42`). `read_pool` calls `_create_engine` and `_read_shard_data` (`:46-54`);
`write_new_store` sets `_shard_db_files` and calls `_create_engine` and `_write_shard_data`
(`:57-71`). `store_fixtures.assertOpens` (`runregistrykit/tests/store_fixtures.py:158-165`) calls
`_check_shard_files` and reads `_shard_db_files`. The issue stays open, owner none.

*Package lines (03, 2026-10-14).* `shard_store_fixtures.py` is unchanged, its lines as 02's;
`store_fixtures.assertOpens` is now `runregistrykit/tests/store_fixtures.py:160-167` (03 added an
import and a line of `StoreTestCase.setUp` above it).

*Package lines (04a, 2026-10-15).* `shard_store_fixtures.py` and `store_fixtures.py` are unchanged,
their lines as 03's. The neutral store, `runregistrykit/tests/neutral_store.py`, touches no private
`ShardedPool` attribute and constructs no pool (pinned by
`test_fingerprinter.TestNeutralStore.test_it_is_built_from_public_names_only`); it is a second
fixture beside the carried one, not a replacement for it, since its primary is not one the
constructor reopens. The issue stays open, owner none.

*Package lines (04b, 2026-10-15).* `shard_store_fixtures.py` and `store_fixtures.py` are unchanged,
their lines as 03's. The ported `runregistrykit/tests/test_store_retire.py` imports
`stored_records`, `tree_state` and `write_new_store` from the carried fixture (`:49-53`), and calls
`write_new_store` (which sets `_shard_db_files` and calls `_create_engine` and `_write_shard_data`)
at `:956`, in `TestNeverReused.test_a_store_written_at_the_retired_name`; its full stores are the
neutral store's. The issue stays open, owner none.

*Package lines (05a, 2026-10-15).* `shard_store_fixtures.py` and `store_fixtures.py` are unchanged
by 05a, their lines as 03's. The carried fixture's names are among the tests' known hits
(`known_hits.json`: `wavenumber`, `GkSource` and the like in `shard_store_fixtures.py`), for 05c.
The issue stays open, owner none.

### `[00-a-refusal-matches-datastorekit-message-text]`

**Opened:** 2026-10-14, at planning. **Owner:** none.

The store layer recognises a store whose shards table cannot be read by matching the text
`_SHARDS_TABLE_UNREADABLE = "its shards table could not be read"` (`stores.py:1567-1568`) in
DatastoreKit's exception, raised by `ShardedPool._read_closed_store` (`SQL/ShardedPool.py:2779` at
`v0.4.0`).

*Impact.* A rewording in DatastoreKit would change how the store layer classifies a store, without
an error. The text is unchanged from `v0.2.2` to `v0.4.0`.

*Next step.* Keep a test that reaches the match at both tested ends (02 or 04, whichever ports it).
A typed exception would be a request to DatastoreKit (README §8).

*Package lines (01, 2026-10-14).* `_SHARDS_TABLE_UNREADABLE` `runregistrykit/stores.py:1567-1568`
(the comment and the assignment).

*Package lines (02, 2026-10-14).* **No 02 test reaches the match.** `_SHARDS_TABLE_UNREADABLE` is
used at `runregistrykit/stores.py:1818` and `:1863`, in `retire_store`, and the one SGK test of it is
in `test_store_retire.py`, which 04 ports. No ported file names the constant or its text. The next
step, a test that reaches the match, is therefore 04's.

**Assigned (2026-10-14):** its next step, a test that reaches the match, to 04b, when 04 was split:
the one SGK test of it, `test_store_retire.TestWithoutFingerprint.test_an_unreadable_shards_table`, is
04b's to port. The issue keeps owner none: its remedy is a request to DatastoreKit (README §8).

*Package lines (03, 2026-10-14), read in the package.* `_SHARDS_TABLE_UNREADABLE`
`runregistrykit/stores.py:1598-1599` (the comment and the assignment), used at `:1858` and `:1905`,
in `retire_store`. Still reached by no test.

*Package lines (04a, 2026-10-15), read in the package.* `_SHARDS_TABLE_UNREADABLE`
`runregistrykit/stores.py:1365-1366` (the comment and the assignment), used at `:1626` and `:1673`,
in `retire_store`. Still reached by no test; its test is 04b's.

**Narrowed (2026-10-15, by 04b, `5302a6f`):** a test now reaches the match.
`runregistrykit/tests/test_store_retire.py` `TestWithoutFingerprint.test_an_unreadable_shards_table`
(`:797`), ported unchanged, drops a full store's `shards` table and asserts, with
`without_fingerprint` true and false, the refusal naming "its shards table could not be read",
"refused even under --without-fingerprint" and "only by a person, outside the registry", texts only
the match produces. 04b's (m1), `_SHARDS_TABLE_UNREADABLE` reworded as a DatastoreKit rewording
would leave it, fails both subtests. The issue stays open, owner none: the test shows a rewording,
it does not prevent one, and the remedy, a typed exception, is a request to DatastoreKit (README
§8). The test runs at whichever ends CI tests (06, U13).

*Package lines (04b, 2026-10-15), read in the package.* `_SHARDS_TABLE_UNREADABLE`
`runregistrykit/stores.py:1365-1366` (the comment and the assignment), used at `:1630` and `:1680`,
in `retire_store`.

*Package lines (05a, 2026-10-15), read in the package.* `_SHARDS_TABLE_UNREADABLE`
`runregistrykit/stores.py:1409-1410` (the comment and the assignment), used at `:1674` and `:1724`,
in `retire_store` (05a's header and `__all__` moved the file by 44 lines). The issue stays open,
owner none.

### `[02-the-ported-tests-name-sgk]`

**Opened:** 2026-10-14, by 02. **Owner:** 05c.

**Assigned (2026-10-15):** to 05c by U15 and U16: the guard scans the tests (05a lists their hits
as known), and 05c renames the SGK names rule 9 kept, each mapped in `PROVENANCE.md`, and rewrites
the rest.

The ported tests and fixtures carry SGK's names, besides the `RunRegistry` and `StoreFixtures` that
D-name and D-fix handle. Measured in the eight files at `8155445` (package lines):

- *SGK's table and key type in the shard fixture:* `shard_store_fixtures.py:25-27`,
  `KEY_TYPE = "wavenumber"`, `REPLICATED = ["version", "wavenumber"]`, `SHARDED = {"GkSource": "k"}`,
  used at `:37-38, 131, 135`.
- *SGK's store stems:* `handover-A3-baseline-lambdacdm` (`store_fixtures.py:38`;
  `test_store_sidecar.py:43`) and `handover-atol-sweep` (`test_store_sidecar.py:36, 43`).
- *An SGK driver path:* `docs/gktk-remedial/scoped_pipeline_run.py` and the "post prompt 15 (measured
  curvature criterion)" beside it (`store_fixtures.py:49-50`); `scoped_pipeline_run.py --register`
  (`test_run_registry.py:482`).
- *SGK's A3 store and sweep, as helper and class names, and a run name:* the class
  `test_store_amend.TestLiveA3Shape` (`:203`; its comments `:7, :200`); the helpers `a3_shaped`
  (`store_fixtures.py:36`) and `sweep_shaped` (`:85`, whose docstring names
  `quadsource_atol_sweep.py`), and the tests named for them (`test_store_sidecar.py:349, 372,
  500`); the run directory `a3-pilot` (`test_run_registry.py:662-688`; `store_fixtures.py:53-54`);
  and `campaign="run-registry"` in the run helper (`test_run_registry.py:102, 125`).
- *Docstrings and comments citing SGK's campaigns and prompts* (`prompts/datastore-portability`,
  `prompts/run-registry`, `store-retirement`, "prompt 01" to "prompt 06", the "datastore-generic
  campaign"): `store_fixtures.py:1`; `test_run_registry.py:4, 148-153, 467`;
  `test_store_sidecar.py:2`; `test_store_copy_move.py:1-4, 234, 330, 402, 482`;
  `test_store_command_line.py:2`; `test_store_amend.py:1, 7`; `test_store_amend_residuals.py:1`;
  `shard_store_fixtures.py:91`. 31 lines of the eight files match `prompt` or `campaign` (`grep -i`),
  the code lines `campaign=` and `prompt=` among them.

*Impact.* The package's tests name a client, which `CLAUDE.md` forbids, and 05's guard (U10), if it
scans `tests/`, fails on them. Renaming `TestLiveA3Shape` touches README §5 rule 9 (a ported test
keeps its class name).

*Next step.* 05, with its prose rewrite; the class name is put to the user there.

*Package lines (03, 2026-10-14).* `shard_store_fixtures.py`, `test_store_sidecar.py`,
`test_store_command_line.py:2` and `test_store_amend_residuals.py` are as 02 recorded. Moved by 03:
`store_fixtures.py` `a3_shaped` `:37`, the A3 stem `:39`, the driver path `:50-51`, `a3-pilot`
`:54-55`, `sweep_shaped` `:86`; `test_run_registry.py` `campaign="run-registry"` `:105` (the
crasher) and `:129` (the run helper), the citations `:157-162` and `:492`,
`scoped_pipeline_run.py --register` `:507`, `a3-pilot` `:687-713`; `test_store_copy_move.py`
citations `:235, 331, 403, 483`; `test_store_amend.py` `TestLiveA3Shape` `:205`, its comment
`:202`. 03 added no SGK name to the tests (03's log, deviation 19).

*Package lines (04a, 2026-10-15).* The eight files of 02 and `test_client_root.py` are as 03
recorded (04a changed in the latter only one test's config and one test, neither naming SGK). The
port adds, in `runregistrykit/tests/test_store_fingerprint.py`: the citations "(store-fingerprint
prompt 04)" `:1`, "(prompt 02's test 1)" `:152` and "The discriminator of prompt 02" `:237`; the
method name `test_deleting_one_quadsourceintegral_row` `:218`, which rule 9 keeps; the constant
names `QSI` and `TKN` (`:68-69`), SGK's abbreviations, now bound to the neutral store's `Integral`
and `Solution`; and the run id `store-fingerprint-04-test-20260925T100000` `:420`, an SGK campaign's
name. Its docstring's first line names `runregistrykit.stores.fingerprint_of`, which the package no
longer has (SGK's text under D-name). `neutral_store.py` and `test_fingerprinter.py` name nothing of
SGK.

*Package lines (04b, 2026-10-15).* The files 04a recorded are unchanged but
`test_fingerprinter.py`, whose eight new tests name nothing of SGK. The port adds, in
`runregistrykit/tests/test_store_retire.py`: the citations "store-retirement prompt 03" `:1`, "the
log's interruption table" `:11` and `:528` (SGK's campaign log), SGK's store-retirement decisions
"D4" and "D6" (`:2`, `:12`, `:14`, `:713`, `:756`, `:883`), "the 2026-09-23 failure" `:345` (an SGK
incident); "real multi-shard fixture stores" `:18`, whose module path N-fix made
`runregistrykit.tests.neutral_store`; the constant name `QSI` `:64`, SGK's abbreviation, bound to
the neutral store's `Integral`; `sweep_shaped` `:38`, used at `:404`. In
`runregistrykit/tests/test_store_retire_references.py`: "a3-v2-readiness prompt 06" and
`[10-store-retire-reports-every-tombstone-as-a-reference]` `:1-2`, "the live A3 backup" `:8` and
`:136`. None is changed under README §5 rule 9.

**Narrowed (2026-10-15, by 05a, this commit):** every hit of the tests is now listed by the guard,
by scan, file and word, in `runregistrykit/tests/data/known_hits.json`: 137 hits in 83 entries,
in 14 of the test modules and fixtures. Code names 29 (14 entries: `sweep_shaped`, `a3_shaped`,
`TestLiveA3Shape`, `test_deleting_one_quadsourceintegral_row`, the neutral store's `log10_tol`, and
`test_tolerance_of_a_torn_line_stops_at_the_end_of_the_file`, whose `_`-split part `tolerance` is
an SGK registry key), strings 67 (36), comments 1 (1), citations 40 (32), among them
`test_package_imports.py`'s `FORBIDDEN` strings `ObjectFactories`, `StoreFixtures` and
`RunRegistry`. The guard and `test_public_names.py` hold none. 05a renamed nothing and changed no
test.

*Package lines (05a, 2026-10-15).* The tests are unchanged by 05a, their lines as 04b recorded; the
new `test_package_is_generic.py` and `test_public_names.py` name nothing of SGK (the guard's own
words are read from the vocabulary file at run time).

## 4. Resolved issues

### `[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]`

**Opened:** 2026-10-15, at 04b's writing. **Owner:** 04b. **Closed:** 2026-10-15, by 04b
(`5302a6f`).

**Assigned (2026-10-15):** to 04b by U14 (a), taken by the user: 04b's §2.3 loads the fingerprinter
before a first retirement plans or fingerprints, beside the port of the retire tests that exercise
the path.

`retire_store`'s step 3, under `without_fingerprint` (`runregistrykit/stores.py:1707-1723`), calls
`fingerprint_store` and records **any** exception as the tombstone's `{"condition": "without",
"error", "error_type"}`, then deletes the store. Since 04a, `fingerprint_store` loads the client's
fingerprinter (`:1305`), so a fingerprinter that cannot be loaded is caught there too. Probed at
writing: with the config naming `no_such_module_x:F`, a store with a registry sidecar and a
recorded fingerprint was retired under the flag, its condition recording the `ConfigError`; with
the config naming the class `DatastoreKitFingerprinter`
(`[04a-the-loader-accepts-a-fingerprinter-class]`), it was retired recording the `TypeError` from
`take`.

*Impact.* `--without-fingerprint` exists for a store that cannot be fingerprinted; this lets a
misconfigured client delete one that can, and the tombstone then says nothing about what it held,
which is what the fingerprint condition is for. No client runs this code yet, and it is in no
release.

*Next step.* 04b §2.3 and §2.5: the fingerprinter loaded before the files are planned, its
`ConfigError` unwrapped and nothing written; tests with an unimportable module and with the class,
each through the function and the command; (m4) and (m5) of 04b §3.5.

*Resolved (04b, 2026-10-15, `5302a6f`).* `retire_store` loads the client's fingerprinter on a
first retirement (`load_fingerprinter(client)`, `runregistrykit/stores.py:1675`) after the reason,
sidecar and in-use refusals and before `ShardedPool.closed_store_files` and either fingerprint
branch; a `ConfigError` from it comes through as the loader raised it, before anything is written,
with `without_fingerprint` or not and in a dry run, and `store retire` prints it with `!!` and exits
1. The completion of an incomplete retirement takes no fingerprint and loads none. The flag still
records, verbatim, a failure of the fingerprint itself, since the load has just succeeded when
`fingerprint_store` loads again. The docstring's step 3 says so. Pinned by
`test_fingerprinter.TestRetireLoadsTheFingerprinterFirst` (a module that exists nowhere and the class
`DatastoreKitFingerprinter`; `retire_store` with no flag, the flag, a dry run and both, and the
command, each a `ConfigError` naming the file and the spec, the tree and the sidecar's bytes
unchanged) and `TestRetirePrecedence` (the reason, a running run and a completed tombstone refused
first, the load before the plan, the completion loading none); 04b's (m4), (m5) and (m8)–(m10) each
fail them. The ported `TestWithoutFingerprint` (a corrupt shard, a missing shard, a journal) passes
unchanged with the neutral fingerprinter. No record changes form.

### `[04a-the-loader-accepts-a-fingerprinter-class]`

**Opened:** 2026-10-15, by the orchestrator's review of 04a. **Owner:** 04b. **Closed:**
2026-10-15, by 04b (`5302a6f`).

**Assigned (2026-10-15):** to 04b by U14 (a), taken by the user at 04b's writing: the class it lets
through also lets `store retire --without-fingerprint` delete a store that can be fingerprinted
(`[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]`), so the two are fixed
together (04b §2.4).

`load_fingerprinter` (`runregistrykit/fingerprint.py:158-192`) refuses an object that is not a
`Fingerprinter` by `isinstance` against the runtime-checkable protocol (`:187`), as the prompt's §2.2
asks. A runtime-checkable protocol checks only that the four attributes exist, and a **class**
defining the four methods has them. So a config naming `module:DatastoreKitFingerprinter`, the class
rather than an instance of it, loads (probed by the review).

*Impact.* It is the likeliest slip a client makes in its config. The store layer then fails at the
first fingerprint, with `TypeError: DatastoreKitFingerprinter.take() missing 1 required positional
argument: 'taken'`, which `Run.finish(…, fingerprint=True)` records as `fingerprint_error` and `store
fingerprint` and `store retire` raise, instead of a `ConfigError` naming the config file and the spec
at load. Nothing is written wrongly; the message misleads.

*Next step.* Refuse a class in the loader (`isinstance(found, type)`) with a `ConfigError` saying
to name an instance, and a test that fails without it. It changes no record. 04b §2.4.

*Resolved (04b, 2026-10-15, `5302a6f`).* `load_fingerprinter` refuses an object that is a class
(`isinstance(found, type)`), before its `Fingerprinter` check, which a class with the four methods
passes (`runregistrykit/fingerprint.py:188-194`): a `ConfigError` naming the config file and the
spec, saying the object is the class and not an instance of it, and to name an instance (for
`DatastoreKitFingerprinter`, one made with the client's registry and its format number). The module
docstring's sentence on the loader says so. Pinned by
`test_fingerprinter.TestProtocolAndLoader.test_a_class_is_refused_and_an_instance_of_it_loads` (the
shipped class and a client's own class with the four methods, each refused naming the file and the
spec, each passing the protocol's check, and an instance of the client's class loading) and by the
class cases of `TestRetireLoadsTheFingerprinterFirst`; 04b's (m6), the refusal removed, fails them.
No record changes.

### `[00-the-fingerprint-reads-a-clients-registry]`

**Opened:** 2026-10-14, at planning (C6, C7). **Owner:** 04a. **Closed:** 2026-10-15, by 04a
(`c81ad06`).

**Assigned (2026-10-14):** to 04a, when 04 was split: 04a deletes layer C and `FINGERPRINT_FORMAT` and
puts the client's fingerprinter in their place (U6), which is this issue's next step.

`fingerprint_store` imports `from config.datastore import factories` (`stores.py:1494`), SGK's
registry, and fingerprints with SGK's `FINGERPRINT_FORMAT = 6` (`:206`) through the package's own
copy of layer C (`:1152-1399`), which DatastoreKit holds since `v0.4.0`.

*Impact.* The store layer works only inside SGK; elsewhere `fingerprint_store`, `Run.finish(…,
fingerprint=True)` and `store retire` fail with `ModuleNotFoundError`. A second copy of layer C here
would drift from DatastoreKit's.

*Next step.* 04: the client fingerprinter (D3, U6), layer C and the format deleted.

*Package lines (01, 2026-10-14).* `from config.datastore import factories`
`runregistrykit/stores.py:1494`, inside `fingerprint_store` (`:1445`); `FINGERPRINT_FORMAT = 6`
`:206`, its history `:194-205`; layer C `:1152-1399` (`fingerprint_of` `:1182`, called `:1500`;
`compare_fingerprints` `:1256`, called `:1529`; `listing_lines` `:1376-1399`).

*Package lines (03, 2026-10-14), read in the package.* `from config.datastore import factories`
`runregistrykit/stores.py:1525`, inside `fingerprint_store` (`:1473`, which now takes
`client_root=`); `FINGERPRINT_FORMAT = 6` `:202`, its history `:190-201`; layer C `:1180-1427`
(`fingerprint_of` `:1210`, called `:1531`; `compare_fingerprints` `:1284`, called `:1560`;
`listing_lines` `:1404-1427`, called `:1460`).

*Resolved (04a, 2026-10-15, `c81ad06`).* The package no longer imports a client's registry or
carries a fingerprint format: `from config.datastore import factories`, `FINGERPRINT_FORMAT` and
its history, and layer C are deleted from `runregistrykit/stores.py`, with the `hashlib` and
`Counter` imports only it used. A client names its fingerprinter in `runregistrykit.toml`
(`[stores] fingerprinter = "module:attribute"`, checked by form in `runregistrykit/client.py`), and
`runregistrykit/fingerprint.py` holds the protocol `Fingerprinter`, the ready-made
`DatastoreKitFingerprinter(factories, fingerprint_format)` over DatastoreKit's functions, and the
loader, which puts the client root first on `sys.path`. `fingerprint_store` loads it after its
refusals (`stores.py:1305`), builds `taken`, and calls `take` and `compare`; `write_listing`
(`:1214`) calls `listing`; `store fingerprint` calls `describe`. Every store operation, and every
`store` command, refuses without one (D4), reading the config only. Pinned by
`test_fingerprinter.TestProtocolAndLoader`, `TestTheStoreLayerRequiresOne`, `TestPrecedence` and
`TestThroughTheFingerprinter`, and by the 29 ported `test_store_fingerprint` tests on the neutral
store; (m3)–(m7), (m10) and (m11) of 04a's log each fail at least one of them. The deletion grep
(prompt §3.4) finds only the ported module's shims.

### `[00-the-store-layer-reads-inside-a-fingerprint]`

**Opened:** 2026-10-14, at planning. **Owner:** 04a. **Closed:** 2026-10-15, by 04a (this
commit).

**Assigned (2026-10-14):** to 04a, when 04 was split: 04a settles what the package reads of a
fingerprint (U7) and moves every other reader behind the fingerprinter.

D3 has the package treat a fingerprint as opaque apart from its versions, its digest and the
comparison's entries. The imported code reads more: the sidecar reader requires `classes`
(`stores.py:416-436`, via `:630`); `fingerprint_store` calls layer C's private `_difference`
(`:1519`); `__main__._print_fingerprint` walks `classes`, `tag_sets` and `problems`
(`__main__.py:267-287`).

*Impact.* With layer C gone, those readers would bind the package to DatastoreKit's fingerprint
shape, which D3 rejected, and a DatastoreKit change to it would break `store show` here.

*Next step.* 04, under U7: the package reads only the named fields and `taken`; the rest is printed
through the fingerprinter.

*Package lines (01, 2026-10-14).* `_fingerprint_problems` `runregistrykit/stores.py:416-436`, called
by the sidecar reader at `:630`; `fingerprint_store` builds `taken` at `:1500-1508` and calls
`_difference` at `:1519`; `retire_store` reads `digest` and `taken.when` at `:1887-1894`;
`runregistrykit/__main__.py`: `_print_fingerprint` `:267-287`, `_fingerprint` reads `taken` and
`digest` at `:307-327`.

*Package lines (03, 2026-10-14), read in the package.* `_fingerprint_problems`
`runregistrykit/stores.py:412-432`, called by the sidecar reader at `:629`; `fingerprint_store`
builds `taken` at `:1531-1539` and calls `_difference` at `:1550`; `retire_store` reads `digest`
and `taken.when` at `:1931-1938`; `runregistrykit/__main__.py`: `_print_fingerprint` `:274-294`,
`_fingerprint` (`:297`) reads `taken` and `digest` at `:314-334`.

*Resolved (04a, 2026-10-15, `c81ad06`).* The package reads of a fingerprint exactly
`fingerprint_format`, `encoding_format` when present, `digest`, the `taken` it builds, and each
comparison entry's `kind` and `text` (U7). The sidecar reader's shape check, `_fingerprint_problems`
(`runregistrykit/stores.py:404-428`), requires an integer `fingerprint_format`, a 64-hex `digest`
and an object `taken`, and an integer `encoding_format` only if present; it no longer reads
`classes`. `fingerprint_store` no longer calls `_difference`: its own `malformed` entry is built by
`_malformed_entry` (`:1237`), with the same six keys and text. `__main__._print_fingerprint`
(`__main__.py:271`) prints `digest:` and `format:` and then the fingerprinter's `describe` lines;
the walk of `classes`, `tag_sets` and `problems` is `DatastoreKitFingerprinter.describe`
(`fingerprint.py:113`). `retire_store` and `_fingerprint` read only `digest` and `taken`, as
before. Pinned by `test_fingerprinter.TestOpacity` (a fingerprint of the three fields reads as no
problem; a string, boolean, float or null `encoding_format` is one),
`TestThroughTheFingerprinter.test_what_the_client_fingerprinter_takes_is_recorded` (a client's own
fingerprinter's opaque fingerprint, without `classes` or `encoding_format`, is recorded and read)
and `test_a_recorded_fingerprint_without_encoding_format_is_not_compared`; (m1) and (m2) of 04a's
log each fail them. The two variants of the ported
`TestSidecarField.test_each_malformed_fingerprint_is_a_problem` that asserted the `classes` check
(`"no classes"`, `"classes a list"`) are removed, U7's one named exception to README §5 rule 9.

### `[02-the-sidecar-readers-guards-are-unpinned]`

**Opened:** 2026-10-14, by the orchestrator's review of 02, from 02's log (observations and its
(m3) candidates). **Owner:** 04a. **Closed:** 2026-10-15, by 04a (`c81ad06`).

**Assigned (2026-10-14):** to 04a, when 04 was split: 04a rewrites the reader's shape check and adds
the two pins before it does (04a §2.6).

Two of the sidecar reader's acceptance rules are pinned by no test. In `_registry_problems`
(`runregistrykit/stores.py:574`), dropping the `isinstance(fmt, bool)` guard on `sidecar_format`
(`:579`) or weakening `_STORE_ID.fullmatch` to `.match` on `store_id` (`:589`) leaves the suite at
108 OK (02's log gives both as diffs). No test in SGK's three 04 modules at `a45aefc` pins either.

*Impact.* What the reader accepts is part of the registry's interface (`CLAUDE.md`). Without a pin,
a sidecar with `"sidecar_format": true` (equal to 1) or a `store_id` with trailing characters would
be accepted after a change and nothing would fail; 04 rewrites the reader's shape check (U7), the
place such a change would come from.

*Next step.* 04: a test of the reader that each mutation fails, added before the shape check
changes. Put to whoever writes 04.

*Package lines (03, 2026-10-14), read in the package.* `_registry_problems`
`runregistrykit/stores.py:573`; the `bool` guard on `sidecar_format` `:578`; `_STORE_ID.fullmatch`
on `store_id` `:588`. Still pinned by no test.

*Resolved (04a, 2026-10-15, `c81ad06`).* Both rules are pinned, by tests added before the shape
check changed: `test_fingerprinter.TestSidecarGuards.test_a_boolean_sidecar_format_is_a_problem` (a
registry sidecar whose `sidecar_format` is `true` reads with the problem "sidecar_format is True;
this reader knows format 1 only") and
`test_a_store_id_with_more_after_its_32_characters_is_a_problem` (32 hex characters followed by
`x`, and 33 hex characters, each read with the `store_id` problem). (m8), the `bool` guard dropped
(`runregistrykit/stores.py:574`), fails the first; (m9), `_STORE_ID.fullmatch` → `.match` on
`store_id` (`:584`), fails both subtests of the second. `_registry_problems` is `:569`.

### `[00-the-root-is-the-packages-parent]`

**Opened:** 2026-10-14, at planning (C1–C3, C9). **Owner:** 03. **Closed:** 2026-10-14, by 03
(`035e4b5`).

`REPO_ROOT` is the parent of the package's own directory (`__init__.py:57`); the runs root
(`DEFAULT_ROOT`, `:58`) and the stores root (`DEFAULT_STORES_ROOT`, `stores.py:185`) are `var/runs`
and `var/datastores` under it, and every `git_provenance()` call reads the git tree there (`:98`).

*Impact.* Installed in `site-packages`, the package would create `var/runs/` inside the venv, a
silent breach of the registry's durability rule, and record the venv's git state, if any, as the
run's. In SGK the same rule makes a run launched from a worktree record into the worktree (SGK's
`[00-a-run-launched-from-a-worktree-records-into-the-worktree]`).

*Next step.* 03: the root found from where the run starts and marked by the config file (SGK's Q2,
U5), records under the main checkout (Q3), provenance from the run's own tree.

*Package lines (01, 2026-10-14).* `REPO_ROOT` `runregistrykit/__init__.py:57`; `DEFAULT_ROOT` `:58`,
used at `:608, 681`, `runregistrykit/stores.py:911, 940, 1741` and as argparse defaults
`runregistrykit/__main__.py:376, 388-390`; `DEFAULT_STORES_ROOT` `stores.py:185`, used at `:1742` and
`__main__.py:452-455`; `_repo_path`/`_resolve` `__init__.py:176-185`; `git_provenance(cwd=REPO_ROOT)`
`__init__.py:98`, called with the default at `__init__.py:649` and `stores.py:833, 893, 1101, 1140,
1499, 1921, 2164`. In this repository's editable install `REPO_ROOT` is the repository's root.

*Package lines (02, 2026-10-14), in the ported tests.* Child processes that rely on `REPO_ROOT`: the
checker and crasher scripts are written with `repo=REPO_ROOT` at
`runregistrykit/tests/test_run_registry.py:179, 226`, and `-m runregistrykit` runs with
`cwd=REPO_ROOT` at `:684`; `test_store_command_line.py:60-61, 172-173` and
`test_store_amend.py:636-637` run `-m runregistrykit` with `cwd=REPO_ROOT` and `PYTHONPATH` set to
it (`REPO_ROOT = runregistrykit.REPO_ROOT`, `test_run_registry.py:21`,
`test_store_command_line.py:25`). Two assertions read the checkout's commit through C9 and that the
`git_head` is 40 characters: `test_run_registry.py:273` and `test_store_sidecar.py:288`. From a
`git archive` export with no `.git` both fail (measured by the orchestrator at dispatch:
`TestManifest.test_manifest_carries_the_provenance_triple` and
`test_store_sidecar.TestCreate.test_the_fields_and_one_create_entry`). `CLAUDE.md`'s Tests bullet
says so.

*Resolved (03, 2026-10-14, `035e4b5`).* The package no longer decides where it lives from where it
is installed. A client marks its root with `runregistrykit.toml`, read by the new
`runregistrykit/client.py` (`find_client_root`, `ClientRoot`, `ConfigError`); the root is found by
walking up from the start directory (the script's for `begin()`, else the working directory), or
named by `client_root=` / `--client-root`, and none found is a `ConfigError`, never a fallback. The
runs and stores roots are the config's, joined to the record root. A run launched from a linked
worktree is recorded under the main checkout (Q3), and its `git_head`, `git_dirty` and script hash
are its own tree's (`git_provenance(cwd)` has no default; every call passes the start directory).
`REPO_ROOT`, `DEFAULT_ROOT` and `DEFAULT_STORES_ROOT` are deleted; `_repo_path` and `_resolve` take
the root, so paths in records stay relative to it (C4, probed against records `8155445` wrote). The
child-process tests run in a client root of their own and import the package from its parent
directory. Pinned by `runregistrykit/tests/test_client_root.py`: `TestWalk` (the walk, the
override, no fallback, the refused `begin()` leaving nothing), `TestWorktree` (a linked worktree,
a config in a subdirectory, a nested worktree's provenance, a bare repository refused, no
repository), `TestStoresUnderTheRoot` and `TestCommandLine`; (m1)–(m3) and (m5)–(m8) of 03's log
each fail at least one of them. Only `TestManifest.test_manifest_carries_the_provenance_triple`
still reads this checkout's commit (03's log, deviation 7).

### `[00-the-recorded-distributions-are-sgks]`

**Opened:** 2026-10-14, at planning (C5). **Owner:** 03. **Closed:** 2026-10-14, by 03
(`035e4b5`).

`RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")` (`__init__.py:119`) is what every manifest's
`packages` records, and `test_run_registry.py:393-396` pins it.

*Impact.* A client that uses neither records two irrelevant entries, and one with other packages
cannot record them. The registry itself is not recorded.

*Next step.* 03: the config's `distributions`, with `runregistrykit` always recorded (U9); the
pinning test becomes a test of the config.

*Package lines (01, 2026-10-14).* `RECORDED_DISTRIBUTIONS` `runregistrykit/__init__.py:119`, the
default of `package_provenance` (`:122`). The pinning test is SGK's `test_run_registry.py:393-396`,
which 02 ports.

*Package lines (02, 2026-10-14).* The pinning test is
`runregistrykit/tests/test_run_registry.py:393-396`
(`TestPackageProvenance.test_the_recorded_names_are_the_two_packages`). Mutation (m1),
`RECORDED_DISTRIBUTIONS = ("datastorekit",)`, fails it, and two more tests of that class (the
02 log).

*Resolved (03, 2026-10-14, `035e4b5`).* `RECORDED_DISTRIBUTIONS` is deleted and
`package_provenance(names)` has no default. A manifest's `packages` is `runregistrykit`, always
(U9), followed by the client config's `distributions`, `runregistrykit` not repeated
(`_recorded_names`). Pinned by `test_run_registry.TestManifest.test_manifest_records_the_installed_packages`
(an empty config records `runregistrykit` alone), the renamed
`TestPackageProvenance.test_the_recorded_names_are_the_registry_and_the_configs` (a config naming
`datastorekit` and `raypoolkit` records exactly those and `runregistrykit`), and
`test_client_root.TestRecordedDistributions`; (m4) of 03's log fails all three.
