# extraction campaign — implementation state

**Last updated:** 2026-10-14 · **Status: LIVE — 3 of 8 prompts written (01–03), 3 landed (01,
`4e0d715`, suite 3, and 02, `8155445`, suite 108, reviewed; 03, this commit, suite 135).** G1 holds
on the source side at SGK `a45aefc`, and on the package side for 01's and 02's files, the
equivalence check retired at 03 and describing `8155445`; E1 holds (DatastoreKit `v0.4.0`). U1
taken at set-up on 2026-10-14; U2 and U3 taken the same day, for 01, U4 for 02, and U5 and U9 for
03, as recommended (README §6.2).

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
| **U6** fingerprinter | a protocol; named by `module:attribute`; each client writes its own | open, for 04 |
| **U7** what is read | versions, digest, `taken`, comparison `kind` and `text`; `encoding_format` not required to read | open, for 04 |
| **U8** neutral store | own factories and writer, public `datastorekit` names only | open, for 04 |
| **U9** self-record | `runregistrykit` always in `packages` | **taken** 2026-10-14 |
| **U10** guard | measured client vocabulary, and an import rule | open, for 05 |
| **U11** public names | for `_slug` and the like, before the release | open, for 05 |
| **U12** licence header | on every package module but the tests | open, for 05 |
| **U13** versions and CI | Python ≥3.12; `[stores]` `datastorekit>=0.4.0`; DatastoreKit's two ends, and a core job without it | open, for 06 |

## 1. Prompts

| # | Prompt | Model | Status | Commit | Suite |
|---|---|---|---|---|---|
| 01 | [`01-import-the-registry.md`](01-import-the-registry.md) | Opus | **landed and reviewed** 2026-10-14 ([log](logs/01-import-the-registry.md)) | `4e0d715` | 0 → 3 |
| 02 | [`02-port-the-core-and-shard-fixture-tests.md`](02-port-the-core-and-shard-fixture-tests.md) | Sonnet | **landed and reviewed** 2026-10-14 ([log](logs/02-port-the-core-and-shard-fixture-tests.md)) | `8155445` | 3 → 108 |
| 03 | [`03-the-root-and-the-client-config.md`](03-the-root-and-the-client-config.md) | Opus | **landed** 2026-10-14 ([log](logs/03-the-root-and-the-client-config.md)) | this commit | 108 → 135 |
| 04 | `04-the-client-fingerprinter.md` | Opus | not written | — | — |
| 05 | `05-the-package-prose-and-the-guard.md` | Sonnet | not written | — | — |
| 06 | `06-release-v0.1.0.md` | Sonnet | not written | — | — |
| 07 | `07-the-adoption-checklists.md` | Opus | not written | — | — |
| 08 | `08-verification-and-close-out.md` | Sonnet | not written | — | — |

**Written one at a time** (README §2.1), each after the one before it has landed and been reviewed.
The holds are for **method**, not scope: every charter is fixed in README §2.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`91b7a60`), used
for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`1f9b5b0`), used for 02.

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

### 1.1 Items

| Item | Prompt | What | State |
|---|---|---|---|
| **I1** | 01 | the package skeleton; the three modules under D-name | ✅ 2026-10-14: D-name on 23 lines (6, 13, 4), D-fmt 0; the import test, 3 tests |
| **I2** | 01 | `PROVENANCE.md`; `compare_with_source.py` (G1, package side) | ✅ 2026-10-14: the check exits 0 and bites on (a)–(i) |
| **T1** | 02 | the 29 core and 76 shard-fixture tests, and their fixtures | ✅ 2026-10-14: the eight files ported; D-name 83, D-fix 5, D-fmt 12 lines in 3 hunks; the suite is 108, OK; the check extended and bites on (a)–(g), 01's (a)–(i) and (m1)–(m3) |
| **R1** | 03 | the config file and the root rule (C1–C3, C9; Q2, Q3) | ✅ 2026-10-14: `runregistrykit.toml` read by the new `runregistrykit/client.py`; the walk, `client_root=` and `--client-root`; a linked worktree recorded under the main checkout, a bare repository's refused; provenance from the start directory; `REPO_ROOT`, `DEFAULT_ROOT`, `DEFAULT_STORES_ROOT` deleted; no config a `ConfigError`; C4's relative paths kept; the check retired, exit 0 from `8155445`; 27 new tests, the suite 135; (m1)–(m8) caught |
| **R2** | 03 | the recorded distributions (C5, U9) | ✅ 2026-10-14: `RECORDED_DISTRIBUTIONS` deleted; `packages` is `runregistrykit` and the config's `distributions`; the pinning test renamed `test_the_recorded_names_are_the_registry_and_the_configs`; (m4) caught by three tests |
| **F1** | 04 | the fingerprinter protocol; layer C and the format deleted (C6, C7) | ⬜ |
| **F2** | 04 | what the package reads of a fingerprint (U7) | ⬜ |
| **T2** | 04 | the neutral store; the 78 and `TestFormats`' 2 ported | ⬜ |
| **P1** | 05 | the prose, the output and the README's rules (C8) | ⬜ |
| **P2** | 05 | the no-client guard | ⬜ |
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
opened an eighth, and the orchestrator's review of 02 a ninth; 03 closed two (§4), leaving seven.
Line numbers are SGK's until 01 imports the code; 01 records each issue's package lines. **From 01
they are the same numbers** for the three modules: D-name replaced one line by one line and `black`
changed nothing, so every line of them sits where it sat in SGK at `a45aefc` (01's log; each line
below read in the package). 02's package lines are for the ported tests, read in
`runregistrykit/tests/`. **From 03 the three modules' lines are no longer SGK's**: each issue's
*Package lines (03, …)* gives them at 03's commit, read in the package.

### `[00-the-fingerprint-reads-a-clients-registry]`

**Opened:** 2026-10-14, at planning (C6, C7). **Owner:** 04.

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

### `[00-the-store-layer-reads-inside-a-fingerprint]`

**Opened:** 2026-10-14, at planning. **Owner:** 04.

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

### `[00-package-prose-names-sgk]`

**Opened:** 2026-10-14, at planning (C8). **Owner:** 05.

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

*Package lines (03, 2026-10-14), read in the package.* `_SHARDS_TABLE_UNREADABLE`
`runregistrykit/stores.py:1598-1599` (the comment and the assignment), used at `:1858` and `:1905`,
in `retire_store`. Still reached by no test.

### `[02-the-ported-tests-name-sgk]`

**Opened:** 2026-10-14, by 02. **Owner:** 05.

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

### `[02-the-sidecar-readers-guards-are-unpinned]`

**Opened:** 2026-10-14, by the orchestrator's review of 02, from 02's log (observations and its
(m3) candidates). **Owner:** 04.

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

## 4. Resolved issues

### `[00-the-root-is-the-packages-parent]`

**Opened:** 2026-10-14, at planning (C1–C3, C9). **Owner:** 03. **Closed:** 2026-10-14, by 03
(this commit).

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

*Resolved (03, 2026-10-14, this commit).* The package no longer decides where it lives from where it
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

**Opened:** 2026-10-14, at planning (C5). **Owner:** 03. **Closed:** 2026-10-14, by 03 (this
commit).

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

*Resolved (03, 2026-10-14, this commit).* `RECORDED_DISTRIBUTIONS` is deleted and
`package_provenance(names)` has no default. A manifest's `packages` is `runregistrykit`, always
(U9), followed by the client config's `distributions`, `runregistrykit` not repeated
(`_recorded_names`). Pinned by `test_run_registry.TestManifest.test_manifest_records_the_installed_packages`
(an empty config records `runregistrykit` alone), the renamed
`TestPackageProvenance.test_the_recorded_names_are_the_registry_and_the_configs` (a config naming
`datastorekit` and `raypoolkit` records exactly those and `runregistrykit`), and
`test_client_root.TestRecordedDistributions`; (m4) of 03's log fails all three.
