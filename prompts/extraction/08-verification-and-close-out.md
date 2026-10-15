# Prompt 08 — verification and close-out

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 07 landed (`aaab408`) and was reviewed (`aaa1d6d`).
- `main` is pushed, and **CI passed all three jobs on `aaa1d6d`**: run `38787646775` (`suite
  (low)`, `suite (high)`, `core (no store layer)`), the first run over
  `docs/adoption/measure_client_registry.py`, which its `black` step checks.
- `git diff --stat aaa1d6d HEAD -- runregistrykit docs pyproject.toml PROVENANCE.md CLAUDE.md
  README.md .github` is empty; no `docs/extraction-verification.md` exists.
- The tag `v0.1.0` on `origin` is tag object `fd5ce48`, peeling to `9f8ebe4`.
- `git status` is clean in this repository, and the suite gives `Ran 276 tests … OK`.
- U23 and U24 are taken (README §6.2, 2026-10-15, as recommended).

**Closes:** the campaign. **Narrows:** nothing. **Changes:** nothing of the package. **Opens:**
only what the work finds.

**Recommended model:** **Opus.** *(The plan said Sonnet; the user changed it on 2026-10-15, at
writing.)*
- This is the campaign's verification prompt, and its document is where a later reader starts. It
  is built from ten logs, ten reviews, a release and 43 commits, and every count in it has to be
  counted.
- It changes no line of the package. It writes one document and one script, and closes the board.
- For the first time in this campaign it installs the release **as a client does**, from GitHub
  (U24), and drives the whole store layer end to end against it (U23).

**Read first:**

1. [`README.md`](README.md): every section, and §6.2 (U1–U24) in full.
2. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`: every section.
3. The board, every section. In §1, every orchestrator review in full, the release record under
   06's review, and the stop recorded in 07's.
4. Every log, `logs/01-…` to `logs/07-…`: at least "What shipped", the deviations, the
   observations not acted on, and the state handed on.
5. `README.md`, `PROVENANCE.md`, `docs/OPEN_ISSUES.md`, `docs/adoption/README.md`.
6. The precedents, for the form only, read through `git show`: RayPoolKit's
   `prompts/extraction/07-verification-and-close-out.md` and `docs/extraction-verification.md` at
   `HEAD` (`git -C /Users/ds283/Documents/Code/RayPoolKit show HEAD:<path>`). Their content is about
   the pool; do not copy it.

Facts below are at `aaa1d6d`, whose `runregistrykit/` and `pyproject.toml` are `9f8ebe4`'s
(`v0.1.0`), measured read-only on 2026-10-15.

---

## 1. What is wanted

08 verifies the campaign, from the package as tagged `v0.1.0` and the records of 01–07, in **one
document**, `docs/extraction-verification.md`, and **closes the campaign**.

**The package does not change.** Nothing under `runregistrykit/` is touched, the suite stays at
**276**, and no tag is made (README §5 rule 12). 08 pushes nothing.

Two things are done for the first time in this campaign, because the user decided so on
2026-10-15:
- **U23: the store layer end to end, as a client uses it.** Until now each store operation has run
  only inside the suite, through the tests' fixtures. 08 runs every `store` command, a run that
  takes a fingerprint, a worktree run and the refusals, in a temporary client root that holds its
  own registry module and fingerprinter, with a script kept in `docs/extraction/`.
- **U24: the release from GitHub.** 06 resolved the install form against a scratch clone, before
  the tag existed; CI installs the checkout. 08 installs the pin a client writes, from GitHub, at
  both tested ends, and runs the smoke script against it.

### 1.1 The smoke run (U23, U24), probed

The planner probed both on this machine, from the session scratchpad.
- **The installs** (U24). In a fresh `uv` venv at each end, `uv pip install --no-cache` of the two
  lines of the README's "Installing", with the end's Ray and SQLAlchemy:

  ```text
  runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0
  datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
  ray==2.43.0  sqlalchemy==2.0.39      (low:  /opt/local/bin/python3.12, 3.12.15)
  ray==2.55.1  sqlalchemy==2.0.46      (high: /opt/local/bin/python3.13, 3.13.16)
  ```

  Each resolved and installed. `importlib.metadata`: `runregistrykit` 0.1.0, `datastorekit` 0.4.0,
  the end's Ray and SQLAlchemy; `runregistrykit.__file__` under the venv's `site-packages`; the
  distribution's `direct_url.json` names `https://github.com/ds283/RunRegistryKit`,
  `requested_revision` `v0.1.0`, `commit_id` `9f8ebe431503fb8c79ee1407cc460501f1ca2d92`; `import
  runregistrykit.tests` raises `ModuleNotFoundError` (U19).
- **Offline is not enough** for this, and is not the route U24 takes: `uv pip install --offline`
  of `datastorekit @ git+…@v0.4.0` fails ("Remote Git fetches are not allowed"); it succeeds only
  with the tag's full SHA, `c8570e849334d09085bbd84876095fc9e22bd005`, from the cache. Recorded for
  the document's reproduction section; not used.
- **The client root.** A `tempfile` directory made a git repository with one commit, holding:
  `runregistrykit.toml` (`distributions = ["datastorekit"]`, `[stores] fingerprinter =
  "smoke_registry:FINGERPRINTER"`); `.gitignore` (`var/`); a `job.py` for `begin()`'s `script`; and
  **`smoke_registry.py`, the client's registry and fingerprinter module**: factories on public
  `datastorekit` names, a store writer, and `FINGERPRINTER = DatastoreKitFingerprinter(FACTORIES,
  1)`. The probe used a copy of `runregistrykit/tests/neutral_store.py` as that module (it imports
  only `datastorekit`'s public names and `runregistrykit.fingerprint`); the script writes a smaller
  one of its own (§2.2).
- **The steps**, each passing at both ends against the installed pin, Ray never initialised:
  1. a store built, and `store create --purpose …`;
  2. `begin(…, script=…, results=<primary>, unit="u", expected_units=1, checkpoint=True)`,
     `heartbeat`, `record("u1", {…})`, `known()` giving `["u1"]`, `finish("done", exit_code=0,
     fingerprint=True)`; `status.json` `done`, with `fingerprint` and `fingerprint_sidecar`
     `written`, and **no `fingerprint_error`** (a fingerprint that cannot be taken does not fail
     `finish`: it is recorded as `fingerprint_error`, and the run is still `done`, so the step must
     assert the key's absence, not the state); the manifest's `packages` `datastorekit` and
     `runregistrykit`;
  3. `list`: one run, finished;
  4. `store show`: a registry sidecar, no problems, the run naming the store;
  5. `store fingerprint`: the recorded fingerprint matched by a fresh one, digest
     `c62012bd1e2c2cd43d24192f4aff593f24946af5d9c1f89821602f0b951e3949` at **both** ends;
  6. `store copy --purpose …` and `store move` of the copy;
  7. `store amend --field x_note --remove --reason …` of an unknown field written into the copy's
     sidecar by hand;
  8. `store adopt` of a second store whose sidecar is a legacy object (`{"datastore": …,
     "purpose": …}`, no `sidecar_format`);
  9. `store retire --dry-run`, then `store retire`, then `store show` of the tombstone: the store's
     files gone, the sidecar left;
  10. a linked worktree of the client root (`git worktree add`), a `begin()` with its `script` in
      the worktree, recorded under the **main checkout's** `var/runs/`;
  11. the refusals: `store show` in a client root whose config names no fingerprinter exits 1; `list`
      in a directory with no `runregistrykit.toml` above it exits 1 and says `No
      runregistrykit.toml`.

  About 5 s at each end. No Ray process before or after (`pgrep -lf 'gcs_server|raylet|ray::'`).
- **One trap.** `tempfile` uses the system temporary directory unless `TMPDIR` says otherwise; 07's
  agent wrote outside the scratchpad that way (its deviation 24). Every run of the script, and every
  scratch command, sets `TMPDIR` to the agent's scratch directory.

### 1.2 The release, re-checked

- **The installed modules.** The five modules in each pin venv's `site-packages/runregistrykit/`
  must equal `git show 9f8ebe4:runregistrykit/<module>` byte for byte, and the distribution's
  `RECORD` must list no `tests/`.
- **The core-only form**, `runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.1.0`
  alone, into a third fresh venv (3.12.15, no Ray, no SQLAlchemy, no `datastorekit`): it resolves
  with none of the three, and the smoke script there runs the core steps and fails each store step
  as a refusal (§4.5 (c)).
- **The offline rebuild**, for the record only: `uv build --wheel --offline` of `git archive
  v0.1.0` gives `runregistrykit-0.1.0-py3-none-any.whl`, **54,940 bytes, 10 entries**, as 06's log,
  with no "absent from" in the build log, its five modules equal to `9f8ebe4`'s. **Its SHA-256 is
  not 06's** (`0a69e125…` at writing against 06's `9c01e7c9…`): the `dist-info` entries carry the
  build's time. A wheel is compared by its entries and their content, never by its hash.

### 1.3 The records to collect

- **Commits.** 43 on `main` from `745c9d9` (the repository started) to `aaa1d6d`, each in one class:
  - the start, `745c9d9`; the plan, `9fe1690`;
  - each prompt written, with the decisions it recorded: 01 `ac46f1b`, 02 `0fb6aff`, 03 `090da27`,
    04a `2ecb99d`, 04b `d035ffb`, 05a `6ec0066`, 05b `92f173c`, 05c `4ec6406`, 06 `dbefdb2`, 07
    `f7c1b15`;
  - each orchestration note: `91b7a60`, `1f9b5b0`, `f02abc7`, `9dc34a5`, `5177ffa`, `d2a3d85`,
    `bcc0c0a`, `bd83b3d`, `02c7ad7`, `4c01c78`;
  - each prompt's own commit: 01 `4e0d715`, 02 `8155445`, 03 `035e4b5`, 04a `c81ad06`, 04b
    `5302a6f`, 05a `14af805`, 05b `1120fb3`, 05c `a7d93d5`, 06 `9f8ebe4`, 07 `aaab408`;
  - each review: `bae5597`, `71f59ed`, `f9e0e60`, `8880cfa`, `dfcb884`, `c735acf`, `8766714`,
    `3372292`, `4ee947b`, `aaa1d6d`;
  - the release record, `dca5ead`.

  Then 08's writing commit, and any records commit after it. Check the classes against `git log`;
  do not take them from this list.
- **The tag and CI.** `v0.1.0`, tag object `fd5ce48`, on `9f8ebe4`, after
  [run 38754093289](https://github.com/ds283/RunRegistryKit/actions/runs/38754093289); also green:
  `38755672939` (`4ee947b`), `38768740409` (`dca5ead`), `38787646775` (`aaa1d6d`). Read with `gh run
  view`, nothing written.
- **The suite** went 0 → 3 (01) → 108 (02) → 135 (03) → 186 (04a) → 245 (04b) → 275 (05a) → 276
  (05b) → 276 (05c) → 276 (06) → 276 (07). Each log records its count before and after.
- **Issues.** Thirteen were opened on the board: eleven resolved (§4), two open, both owner none
  and both a request to DatastoreKit (README §8): `[00-the-shard-fixtures-reach-into-shardedpool]`
  and `[00-a-refusal-matches-datastorekit-message-text]`. They stay open at the close; the index
  counts **2**.
- **Decisions.** D1, D3, D4, Q1–Q5 and Q7 (made by the user, README §6.1); U1–U24, every one taken
  as recommended, U5 and U6 with a reading at writing, U11 amended at 05a's dispatch, U7 with its
  named exception to rule 9 (README §6.2). And one ruling made at a stop: 07's, on the
  `fingerprint_of` calls (board, 07's review).
- **Deviations.** Every log classifies its deviations. A count of the three labels' **words** at
  writing gives (STRUCTURALLY REQUIRED / IMPLEMENTATION CHOICE / UNINTENDED DRIFT): 01 1 / 11 / 1,
  02 1 / 8 / 0, 03 7 / 11 / 0, 04a 6 / 14 / 1, 04b 5 / 9 / 1, 05a 2 / 10 / 1, 05b 7 / 8 / 1, 05c 6
  / 8 / 1, 06 10 / 7 / 0, 07 12 / 11 / 2. **A word is not an entry**: a label is also used in
  prose, and one entry can class several items. Count the entries yourself.
- **Observations not acted on**: each log has a section of that name.
- **The equivalence check at `8155445`**, as `PROVENANCE.md`'s "Re-running the check" (a `git
  worktree --detach` of `8155445` in the scratchpad, run with `venv/`'s Python, removed after):
  exit 0, `RESULT: OK`, "12 checked (4 by 01, 8 by 02): D-name 106, D-fix 5, D-fmt 12 in 3 hunks; 3
  pending; 11 not imported and absent; 1 declared new". It reads SGK through `git show` only.
- **The adoption checklists.** `measure_client_registry.py sgk|cpbh|si` at their commits: its
  output must equal each checklist's appendix byte for byte (07's review did so at `aaab408`). The
  clients' `HEAD`s are recorded first; if one has moved, the script is run at the checklist's
  commit (the default), never at the new `HEAD`.

---

## 2. What to write

### 2.1 `docs/extraction-verification.md`

A new file, named as the siblings'. It is additive from the day it is committed (`CLAUDE.md` rule
6). Its head names the campaign, the board, this prompt, the date, and the package it verifies:
`v0.1.0`, `9f8ebe4`, and that `git diff 9f8ebe4 -- runregistrykit pyproject.toml` is empty at the
commit that adds it.

| § | Section | What it holds |
|---|---|---|
| 1 | What this document is | What the campaign set out to do (README §0, §1, D1, D3, D4), what it delivered, and the headline: one release, the suite at both ends, the store layer end to end from the GitHub pin, the checklists and E2, two issues open, and what remains. |
| 2 | Reconciliation | **Git history:** a table of every prompt, its writing commit, note, commit, review, the suite count after it, and what it closed or opened; every other commit on `main` from `745c9d9` to the commit before 08's, classed. **The tag and CI**, as §1.3, each run linked. **The environment** of every measurement below. |
| 3 | Each prompt's acceptance, at `v0.1.0` | A table: the prompt; its acceptance in brief (README §2 and the prompt's own); what its review found; what holds at `v0.1.0`, with how it was re-measured here or why it cannot be. Re-measure here: the suite in `venv/` and at the high end; the guard and the import test (in the suite); `black`; the equivalence check at `8155445`; the adoption script's three outputs against the appendices. |
| 4 | The store layer end to end (U23) | §2.2's script: the command, the two ends, every step's output, the time, and Ray's processes before and after. The breakage (a)–(c). |
| 5 | The release from GitHub (U24) | The three installs as run, with what each resolved; `direct_url.json`; the five modules equal to `9f8ebe4`'s; no tests in `RECORD`; the core-only form; the offline rebuild and why its hash differs (§1.2). |
| 6 | Issues | The eleven resolved, one line each, with the prompt and commit that closed it and the test that guards it (or the document, for a README issue). The two open, with why they stay open at the close and where they go (README §8). |
| 7 | Decisions | D1, D3, D4, Q1–Q5, Q7; U1–U24; 07's ruling at its stop. One line each: what was decided, when, for which prompt, and where it is applied (a commit, or "not applicable"). |
| 8 | Deviations across the campaign | A table of entry counts per log and class. Then every UNINTENDED DRIFT entry in one line each, with its log, and every STRUCTURALLY REQUIRED entry that changed what a prompt delivered. |
| 9 | Observations not acted on | Every item of every log's section, one line each, with its log, and its disposition at `v0.1.0`: addressed (by which prompt, review or decision), opened as an issue, handed to a client's checklist, still an observation, or no longer true. Decide from the later logs, the board and the checklists, never by changing anything. |
| 10 | Known gaps | **G2–G4**: no client has adopted; the checklists are measured at commits that will move. **E2** holds (`v0.1.0` with `docs/adoption/secondarygwkit.md`). **What remains unverified**: a client's own stores and run directories (none was opened, README §3), so records written by SGK's `RunRegistry/` are read only as the tests' fixtures stand for them; a client's own suite under the package; Linux only through CI; Python 3.14 and Ray or SQLAlchemy above the high end, inside the declared range and untested; concurrent runs and store operations on one root (the registry records and does not lock). **The two open issues.** |
| 11 | Reproduction | Every command of §3–§5, verbatim, runnable from a clean checkout of the commit that adds this document, with `TMPDIR` set; the offline variant of the installs (§1.1), named as not the one run. |
| 12 | Summary for the board | Five to ten lines. |

Every fact carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section. Where the document and a log disagree, the document
says which is right and why; it does not rewrite the log.

### 2.2 `docs/extraction/store_smoke_run.py` (U23)

A script, not a test. The suite never collects it (discovery is `-s runregistrykit/tests`). Write it
in the form of `docs/extraction/compare_with_source.py` and `docs/adoption/measure_client_registry.py`:
a module docstring saying what it is, how it is run and what it prints; `black`-clean (CI checks
`docs/`).
- **It is self-contained.** It imports `runregistrykit` and its public names, `datastorekit`'s
  public names, and the standard library, and **nothing of `runregistrykit.tests`**, so it runs
  against an installed wheel. It names no client, in code, strings or comments, as the package does
  not.
- **It builds the client root itself**, in a `tempfile` directory: §1.1's files, with
  `smoke_registry.py` written from a source string the script holds. That module is the client's:
  a few factories on public `datastorekit` names (`SQLAFactoryBase`, `InventorySpec`, `Parent`,
  `build_schema`, `shard_file_name`, `datastorekit.contract`'s table and tag names), a writer of a
  closed store with at least two shards that `read_inventory` and `ShardedPool`'s static
  `copy_store` and `move_store` read, and `FINGERPRINTER`. It may follow
  `runregistrykit/tests/neutral_store.py`, read as a model, and should be much smaller: at least
  one replicated class, one sharded class with a parent, and the tag and version tables the
  contract requires.
- **How it is run:** `python docs/extraction/store_smoke_run.py`, with the package importable,
  from anywhere; it changes into the client root it makes, and runs each command as `sys.executable
  -m runregistrykit …`. It prints Python's, `runregistrykit`'s and `datastorekit`'s versions and
  `runregistrykit.__file__`, and Ray's and SQLAlchemy's versions if installed, so a run shows which
  package it ran.
- **The steps are §1.1's eleven**, each isolated: an exception or an unexpected exit code is that
  step's `FAIL`, with what it saw, and the next step runs where it can. Each prints `PASS` or
  `FAIL` with the command, its exit code and the line that shows the outcome. Every value it
  asserts is the script's own (counts, states, the runs root, files left), never a figure read
  from a log; the fingerprint's digest is printed, not asserted.
- **Without the extra**, the steps that need a store or a fingerprinter fail, each caught by its
  step and reported with what it saw (§4.5 (c)); the script never imports `datastorekit` at module
  scope, so it starts, and the steps that need neither still run.
- **It never initialises Ray**, and checks at the end that `ray`, if imported, is not initialised.
- **It removes nothing it did not make**, and leaves its client root in place for inspection unless
  `--clean` is given, which removes only that directory.
- **Its exit code** is 0 only if every step passes, 1 if one fails, 2 if it cannot start (no
  `git`, or the package not importable).

### 2.3 The release (U24)

As §1.1 and §1.2: three fresh venvs in the scratchpad, each made with `uv venv --python <the
interpreter>` and filled with `uv pip install --no-cache` of the forms given, so that the tag is
fetched from GitHub and nothing is reused from `uv`'s cache. The offline rebuild as §1.2. Nothing
of it is committed.

### 2.4 Closing the campaign

- **The board.**
  - Its header says **CLOSED** (2026-10-15, by prompt 08), with all eleven prompts landed.
  - §1's row for 08; Z1 ✅.
  - §2's gates are unchanged: G2–G4 have not held, and the campaign does not wait for them
    (README §7). Add a dated line under §2: after the close, a gate is recorded on this board when
    it holds, in a records commit of its own.
  - §3 keeps its two open issues, each with a dated line that they stay open at the close, owner
    none, requests to DatastoreKit (README §8).
- **The campaign README.** Its header, §2's row for 08, and a dated line under §7: the campaign
  closed at 08, with G2–G4 open and E2 held.
- **`prompts/INDEX.md`**: the campaign's line, **closed**, with its open-issue count, 2.
- **`docs/OPEN_ISSUES.md`**: the header's date; §1.1's heading says the campaign is closed. Its
  count stays 2 unless 08 opens an issue.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **`TMPDIR`.** Set it to your scratch directory for every command that may make a temporary
   directory: the smoke script, the suite, `uv`. Nothing is written outside the scratchpad and
   this repository (07's deviation 24).
2. **The network, once per venv** (U24). The three installs fetch from GitHub and PyPI; that is
   the only network use. No `git fetch`, `git push` or `gh` call that writes. Reading CI with `gh
   run view` is allowed.
3. **Ray is never started.** The store layer does not start it, and neither does the script. Before
   and after every smoke run and every suite run, record `pgrep -lf
   'gcs_server|raylet|ray::|default_worker\.py'`. If one is up, find whose it is from its path; if it
   is another project's, leave it alone and say so.
4. **The package does not change.** `git diff aaa1d6d -- runregistrykit pyproject.toml README.md
   PROVENANCE.md docs/adoption docs/extraction/compare_with_source.py
   docs/extraction/measure_client_vocabulary.py .github` is empty at the end. A finding is recorded,
   not fixed (rule 4). The breakage edits scratch copies only.
5. **Additive documents.** Under `docs/`, 08 adds two files and changes only `docs/OPEN_ISSUES.md`.
6. **No client is touched.** SGK is read only through `git show`, by `compare_with_source.py` at
   `8155445` and by `measure_client_registry.py`; CPBH and SI only by the latter. No client is
   written, run, imported or opened; no store or run directory of any client is read.
7. **The suite runs in `venv/` and at the high end.** For the high end, a fresh scratch venv
   (3.13.16, `ray==2.55.1`, `sqlalchemy==2.0.46`, `datastorekit` from `v0.4.0`) with a `git
   archive` of your tree installed editable, as 06's high venv was; the suite needs
   `runregistrykit/tests` and a git work tree (`CLAUDE.md`), so run it from a `git clone` of your
   tree, not a bare export. The pin venvs hold no tests and do not run the suite.
8. **The document is long.** Its tables are built from the records with scripts or by counting,
   never from memory. Each count it states is one you counted, and the log says how.

---

## 4. Verification

1. **The suite.** In `venv/`: `Ran 276 tests … OK` before and after, by module. At the high end, as
   hazard 7: `Ran 276 tests … OK`, by module.
2. **The checks.**
   - `./venv/bin/black --check runregistrykit docs` (25.1.0) leaves **28** files unchanged (27 and
     the script).
   - `compare_with_source.py` at `8155445`, as §1.3, the worktree removed after; output whole.
   - `measure_client_registry.py` for each client at its checklist's commit, each output equal to
     its appendix (`cmp` against the appendix extracted by a script).
3. **The smoke run** at both ends, against the pin venvs of §2.3, from the repository root, with
   `TMPDIR` set. The script exits 0. Record its whole output, its time, and Ray's processes before
   and after.
4. **The release**, as §1.2 and §2.3.
5. **The breakage record.** Each item is exactly what was run or changed, in a scratch copy; never
   the repository, never a committed file.
   - **(a)** the script's `runregistrykit.toml` naming the class (`smoke_registry:<the class>`)
     instead of the instance. Probed at writing: the steps that load the fingerprinter fail, each
     on the loader's refusal naming the class: step 2 (`status.json` carries `fingerprint_error`, a
     `ConfigError`, and the run is still `done`), step 5 (`store fingerprint`, exit 1) and step 9
     (`store retire`, with and without `--dry-run`, exit 1, **and the store's files are not
     deleted**, U14); the steps that only check that one is named (`create`, `show`, `copy`,
     `move`, `amend`, `adopt`) pass, as the package's README says; exit 1. Recorded as the diff to
     a scratch copy of the script, with the list of steps that failed.
   - **(b)** one row of the store changed after step 2's fingerprint (an `UPDATE` with `sqlite3` on
     a shard, in a scratch copy of the script between steps 2 and 5): `store fingerprint` reports a
     difference, and step 5 fails; record what `store retire` then does with that store in the same
     run, and say whether it is what the package's README says. Probed at writing (`UPDATE
     Solution SET log10_step = log10_step + 1 WHERE serial = 1` on shard 0 of the tests' store):
     `store fingerprint` exit 1 naming the class that differs; `store retire` of the store exit 1,
     "its content does not match the fingerprint …", every file kept; and the copy, made after the
     change, refused the same way at step 9.
   - **(c)** the script in the core-only venv of §1.2. There is no `datastorekit`, so the client's
     registry module cannot be imported and no store can be built: the steps that need one fail,
     each with what it saw (an `ImportError` caught by the step, or a command's refusal); the steps
     that need none (step 10, the worktree run, and step 11's `list` refusal) pass; no exception
     escapes a step; exit 1. Not probed at writing: the log lists which steps passed and which
     failed, and why each.
6. **The documents.**
   - Every relative link and anchor in `docs/extraction-verification.md` resolves, checked by a
     scratch script; every external link is to `github.com/ds283/…` and names a tag, a commit or a
     run.
   - Every `path:line` the document cites at `v0.1.0` is read at `9f8ebe4`; at a client, at the
     checklist's commit.
   - Every count it states is recounted, and the log says how.
7. **The clients.** Record each client's `HEAD`, `git status --porcelain | shasum` and `git stash
   list | wc -l`, at the start and the end, unchanged.

---

## 5. Acceptance

1. `docs/extraction-verification.md` holds §2.1's twelve sections, and every fact in it carries its
   source.
2. `docs/extraction/store_smoke_run.py` exits 0 at both ends against the GitHub pin, never starts
   Ray, and (a)–(c) fail as §4.5 says.
3. The pin installs at both ends and in the core-only form, its modules are `9f8ebe4`'s, and it
   ships no tests.
4. The campaign is closed on the board, in the README, in `prompts/INDEX.md` and in the index.
5. §4.1–§4.7 hold.
6. **The records**, in the same commit:
   - the log, `logs/08-verification-and-close-out.md`, per README §5.1. It has:
     - the suite in both venvs, by module;
     - `compare_with_source.py` at `8155445`, whole;
     - the three `measure_client_registry.py` comparisons;
     - the installs, each command and what it resolved;
     - the smoke runs, whole, with Ray's processes before and after each;
     - the offline rebuild;
     - (a)–(c);
     - the documents' checks, and how each count was made;
     - the clients' states, at the start and the end;
   - the board, as §2.4;
   - `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and the campaign README, as §2.4.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 276, in either venv.
- An install of §2.3 fails to resolve, or installs a commit other than `9f8ebe4`, or modules that
  differ from `9f8ebe4`'s.
- The smoke script fails a step at either end against the pin. A defect found is opened, not
  fixed; stop before writing it up, and report.
- A breakage does not fail as §4.5 says, or (b)'s `store retire` does something the README does not
  say.
- `measure_client_registry.py`'s output differs from an appendix at the checklist's commit.
- Anything would change a file under `runregistrykit/`, `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `docs/adoption/`, the other scripts of `docs/extraction/`, the workflow, or any
  file not in §7.
- Anything would push, make or move a tag, start Ray, or write, run, import or open anything of a
  client or of DatastoreKit, beyond installing `datastorekit` from its tag.

---

## 7. What this prompt changes, and what it does not

- **Files it adds:** `docs/extraction-verification.md`, `docs/extraction/store_smoke_run.py` and
  the log.
- **Files it changes:** `docs/OPEN_ISSUES.md`; the board, the campaign README (its header, §2's
  row for 08 and §7's line), and `prompts/INDEX.md`.
- **It changes nothing else:** no file under `runregistrykit/`; not `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/compare_with_source.py`,
  `docs/extraction/measure_client_vocabulary.py` or the workflow; not `CLAUDE.md`, `LICENSE` or
  `.gitignore`.
- **It touches no client repository, and not DatastoreKit**, beyond reading through `git` and
  installing `datastorekit` from its tag.
- **It makes no tag and pushes nothing.**

---

## 8. The log and the board

`logs/08-verification-and-close-out.md`, using README §5.1, with §5 item 6's additions.

`IMPLEMENTATION_STATE.md`: the header (**CLOSED**), §1's row for 08, Z1, §2's dated line, and §3's
two dated lines.

---

## At writing (2026-10-15, at `aaa1d6d`)

Measured, for the README's row and the orchestrator; §1 holds the detail.
- **CI** passed all three jobs on `aaa1d6d` (run `38787646775`).
- **The pin from GitHub** installs at both ends, `commit_id` `9f8ebe4`, no tests; offline it needs
  the tag's full SHA.
- **The store layer end to end**, in a client root with its own registry module: eleven steps, every
  `store` command, a fingerprinted run, a worktree run and two refusals, pass at both ends in about
  5 s each, the same fingerprint digest at both, Ray never initialised.
- **The equivalence check** at `8155445`: `RESULT: OK`.
- **The offline wheel** from `v0.1.0`: 54,940 bytes and 10 entries as 06's, its modules
  `9f8ebe4`'s, its hash not 06's (build times in `dist-info`).
- **43 commits** to `aaa1d6d`; the suite 0 → 276 over ten prompts; 13 issues, 11 resolved and 2
  open; U1–U24 taken.
- **Not measured**: the entries of each log's deviations and observations (the agent counts them).
