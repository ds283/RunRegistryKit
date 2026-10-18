# Prompt 07 — verification and close-out

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 06 landed (`0bae3a3`) and was reviewed (`74f85a2`).
- `v0.2.0` is tagged: on `origin`, tag object `895e3c7`, peeling to `0bae3a3`. CI passed all three
  jobs on `0bae3a3` itself (run `39143681701`) and on `aeacba8`, the records commit after it (run
  `39144321994`).
- `main` is pushed, and `git status` is clean in this repository.
- `git diff --stat 0bae3a3 HEAD -- runregistrykit pyproject.toml README.md .github docs/releases
  docs/adoption docs/extraction` is empty. No `docs/interrupted-runs-verification.md` and no
  `docs/interrupted-runs/` exist.
- The suite gives `Ran 410 tests … OK (skipped=1)` on macOS.

**Closes:** the campaign. **Narrows:** nothing. **Changes:** nothing of the package. **Opens:**
only what the work finds. The six open §3 entries stay open at the close, each with a dated line.

**Recommended model:** **Opus**, as the plan says.
- This is the campaign's verification prompt, and its document is where a later reader starts. It
  is built from eight logs, eight reviews, a release and 42 commits, and every count in it has to
  be counted, not copied.
- It changes no line of the package. It writes one document and one script, and closes the board.
- For the first time in this campaign it drives an interrupted run **as a client meets one**,
  against the release installed from GitHub: a process hard-killed, ended by a person, and its
  store resumed and fingerprinted.

**Read first:**

1. [`README.md`](README.md): every section; §0.1, §5 and §6.2 (L1–L11 with their notes) in full.
2. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`: every section.
3. The board, every section. In §1, every orchestrator review in full, and the CI and tag record
   under 06's review.
4. Every log, `logs/01-…` to `logs/06-…`, eight in all: at least "What shipped", the deviations, the
   observations not acted on, and the state handed on.
5. The repository `README.md`, `docs/releases/v0.2.0.md`, `docs/adoption/v0.2.0/README.md`,
   `docs/OPEN_ISSUES.md`.
6. The precedent, for the form only:
   [`prompts/extraction/08-verification-and-close-out.md`](../extraction/08-verification-and-close-out.md),
   [`docs/extraction-verification.md`](../../docs/extraction-verification.md) and
   [`docs/extraction/store_smoke_run.py`](../../docs/extraction/store_smoke_run.py). Their content
   is about the extraction; do not copy it.

Facts below are at `aeacba8`, whose `runregistrykit/` and `pyproject.toml` are `0bae3a3`'s
(`v0.2.0`), measured on 2026-10-18 in the session scratchpad.

---

## 1. What is wanted

07 verifies the campaign, from the package as tagged `v0.2.0` and the records of 01–06, in **one
document**, `docs/interrupted-runs-verification.md`. It runs **one script**,
`docs/interrupted-runs/interrupted_run_smoke.py`, against the pin installed from GitHub. Then it
**closes the campaign**.

**The package does not change.** Nothing under `runregistrykit/` is touched, the suite stays at
**410**, and no tag is made (README §5 rule 11). 07 pushes nothing.

### 1.1 The smoke run, probed

The planner probed it on this machine, in the session scratchpad, with a prototype that is not
committed. The script follows that prototype.

**The installs.** In a fresh `uv` venv at each end, `uv pip install --no-cache` of the README's
"Installing" lines, with the end's Ray and SQLAlchemy:

```text
runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
ray==2.43.0  sqlalchemy==2.0.39      (low:  /opt/local/bin/python3.12, 3.12.15; 7.6 s)
ray==2.55.1  sqlalchemy==2.0.46      (high: /opt/local/bin/python3.13, 3.13.16; 5.8 s)
```

Each resolved and installed. The probe found:
- `importlib.metadata`: `runregistrykit` 0.2.0, `datastorekit` 0.4.0, and the end's Ray and
  SQLAlchemy;
- `direct_url.json`: `requested_revision` `v0.2.0`, `commit_id`
  `0bae3a3c501a8264ee4be5bc24f06422af38720f`;
- the five modules in `site-packages/runregistrykit/` are byte-identical to `git show
  v0.2.0:runregistrykit/<module>`;
- the distribution's `RECORD` lists no `tests/`.

**The client root**, in a `tempfile` directory, is a git repository with one commit. It holds the
extraction smoke script's own `CONFIG`, `GITIGNORE`, `JOB` and `REGISTRY_SOURCE`. The probe took
them by loading `docs/extraction/store_smoke_run.py` with `importlib.util.spec_from_file_location`,
which runs nothing: its `main` is guarded. The store is written by the client module's
`write_store`, a closed store of two shards.

**The steps.** Each passed at both ends against the installed pin, in about 8 s each. No Ray
process ran, before or after.
1. a store written, and `store create --purpose …`;
2. **a hard kill.** A child process (`sys.executable -c …`) calls `begin(…, results=<store>)`,
   prints its run id, and heartbeats in a loop. The parent sends it `SIGKILL` and reaps it, with
   returncode −9. Its `status.json` still says `running`, with `host` `{id, boot}` recorded, and
   `liveness(status, 900)` is `stale`;
3. `list` exits 0. The run's row begins `!!`, and stderr names `python -m runregistrykit end`;
4. `store fingerprint` exits 1. Its refusal names the run and `python -m runregistrykit end`;
5. **a second `begin`** on the store raises `RuntimeError`. Its text names the run and `python -m
   runregistrykit end`, and ends `No run directory was created`. The runs root's listing is
   unchanged;
6. **a live pid is refused.** A second child begins on a second store and stays alive. `end
   <its id> --reason …` exits 1 saying "answers kill -0", the same with `--unverified`, and its
   status is unchanged;
7. **a real `SIGTERM`.** That child's handler calls `run.finish("killed", exit_code=128 +
   signum)` and exits. It is sent `SIGTERM` while heartbeating. Its returncode is 143, its status
   `killed` with `exit_code` 143 and parseable, and no `status.json.*.tmp` is left;
8. **`end`.**
   - `end <the killed run's id>` with no `--reason` exits 2 (argparse);
   - `end <id> --reason …` exits 0, printing `>> end: <id> is now lost, verified: its pid <pid>
     does not answer kill -0 on this host`;
   - its status is `lost`, `exit_code` `null`, `ended.verified` true, and
     `ended.evidence.pid_answers` false;
9. `end` again exits 1: "its status says it has already ended";
10. `list`: the run is `lost`, with no marker, and the summary counts it finished;
11. **the resume.** `begin` on the first store is accepted, then `heartbeat`, then `finish("done",
    exit_code=0, fingerprint=True)`. Its status is `done`, with `fingerprint`, and
    `fingerprint_sidecar` is `"written"`, with no `fingerprint_error`;
12. `store fingerprint` exits 0, and `store retire --reason … --dry-run` exits 0;
13. the resumed run's manifest `host.id` is not null and equals its status's `host.id`.

### 1.2 The extraction's smoke run, against `v0.2.0`

`docs/extraction/store_smoke_run.py`, unchanged, in the same two venvs: **10 of its 11 steps
pass. Step 3 fails at both ends**, and the script exits 1. It asserts that `list`'s summary ends
`1 finished.`. `v0.2.0` prints `1 run(s) under …: 1 finished; 0 with no host recorded.`, the
clause 01 added and the release notes' §5 names. The package is right, and so is the script, for
`v0.1.0`, the tree it was written against.

The script is not changed (`CLAUDE.md` rule 6). The document records the result in §5 and §10.
07's own script covers the store layer that the hard-kill route touches. This is not an issue:
nothing is wrong at either tag. If the review or the user judges otherwise, it is opened then.

### 1.3 The records to collect

- **Commits.** There are 42 on `main` from `b56ecc7` (the plan) to `aeacba8`, each in one class:
  - the plan, `b56ecc7`;
  - each prompt written, with the decisions it recorded: 01 `1fd8e1c`, 02 `34afe6d`, 02b `5ed97a5`,
    02c `149918f` and `069f1d7` (L11), 03 `88f93c3`, 04 `c3aa52a`, 05 `f3cc239`, 06 `7f88787`;
  - each orchestration note: `8023e14`, `b52cc01`, `201e507`, `e4a2b6c`, `75eab12`, `5d8a97b`,
    `5d0fa78`, `c4f2abc`;
  - each prompt's own commit: 01 `387c58f`, 02 `2bf9c72`, 02b `2959b78`, 02c `35ce264`, 03
    `ab0cad9`, 04 `5e20772`, 05 `eb68583`, 06 `0bae3a3`;
  - each review: `5d71a6b`, `a38022f`, `c18ec34`, `31933c4`, `4b55750`, `46e29b9`, `4a10efb`,
    `74f85a2`;
  - each CI or tag record: `c2911d3`, `91e8e9c`, `9d26357`, `0c75dd3`, `9e38581`, `d8f8de4`,
    `80974e2`, `aeacba8`.

  Then 07's writing commit, and any commit after it. Check the classes against `git log`; do not
  take them from this list.
- **The tag and CI.** `v0.2.0` is tag object `895e3c7`, on `0bae3a3`, after run `39143681701`. Ten
  runs since 01, each green, read with `gh run view` (nothing written):

  | Run | Commit |
  |---|---|
  | `38911075984` | `5d71a6b` |
  | `38929845135` | `c2911d3` |
  | `39049728089` | `a38022f` |
  | `39060913296` | `c18ec34` |
  | `39072902589` | `31933c4` |
  | `39083674030` | `4b55750` |
  | `39122974980` | `46e29b9` |
  | `39129061916` | `4a10efb` |
  | `39143681701` | `0bae3a3` |
  | `39144321994` | `aeacba8` |
- **The suite.** 276 at `79015a7` → 307 (01) → 322 (02) → 328 (02b) → 329 (02c) → 347 (03) → 378
  (04) → 410 (05) → 410 (06). Each log records its count before and after.
- **Issues.** Fourteen were on this board:
  - five assigned from `inherited-issues` on 2026-10-16, **all five resolved**;
  - nine opened during the campaign: two by 02's review, one by 02b's, one at 03's writing, one by
    03's work, one by 03's review, one at 04's writing, one by 04's work and one by 06's review;
  - **eight resolved** (§4) and **six open** (§3), each owner none. The index counts **11**: these
    six, two on the closed `extraction` board and three on `inherited-issues`.
- **Decisions.** L1–L11, each with its date, its prompt and how it was taken (README §6.2; the
  board's decisions table): L5 refined and then amended; L6 refined; L9 with the pid issue
  assigned at the user's request; L11 for 02c.
- **Deviations.** Every log classifies its deviations. A count of the three labels' **words** at
  writing gives (STRUCTURALLY REQUIRED / IMPLEMENTATION CHOICE / UNINTENDED DRIFT):

  | Log | Count |
  |---|---|
  | 01 | 7 / 7 / 0 |
  | 02 | 9 / 11 / 0 |
  | 02b | 14 / 6 / 1 |
  | 02c | 15 / 4 / 1 |
  | 03 | 7 / 7 / 1 |
  | 04 | 11 / 7 / 0 |
  | 05 | 14 / 6 / 1 |
  | 06 | 9 / 7 / 1 |

  **A word is not an entry**: a label also appears in prose, and in a closing line that says
  "none was UNINTENDED DRIFT". Count the entries yourself.
- **Observations not acted on**: each log has a section of that name.

---

## 2. What to write

### 2.1 `docs/interrupted-runs-verification.md`

A new file, named as its sibling `docs/extraction-verification.md`. It is additive from the day
it is committed (`CLAUDE.md` rule 6). Its head names:
- the campaign, the board and this prompt;
- the date;
- the package it verifies: `v0.2.0` (tag object `895e3c7`) on `0bae3a3`, and that `git diff
  0bae3a3 -- runregistrykit pyproject.toml` is empty at the commit that adds it.

| § | Section | What it holds |
|---|---|---|
| 1 | What this document is | What the campaign set out to do (README §0, §1), what it delivered, and the headline: five issues resolved and four found and resolved along the way; one release; the suite at both ends; the hard-kill route from the GitHub pin; six issues open; and what remains (G1–G3). |
| 2 | Reconciliation | **Git history:** a table of every prompt with its writing commit, note, commit, review, CI record, the suite count after it, and what it closed or opened. Every other commit on `main` from `b56ecc7` to the commit before 07's, classed. **The tag and CI**, as §1.3, each run linked. **The environment** of every measurement below. |
| 3 | Each prompt's acceptance, at `v0.2.0` | A table: the prompt; its acceptance in brief (README §2 and the prompt's own); what its review found; and what holds at `v0.2.0`, with how it was re-measured here or why it cannot be. Re-measure the suite in `venv/` and at the high end, and `test_status_writes` at 3.14.8 by `PYTHONPATH` (02c's sweep, L11's window: its skip or its pass, as found). 04's and 05's acceptances are re-measured by §4's run. |
| 4 | An interrupted run from the GitHub pin | §2.2's script: the command, the two ends, every step's output, the time, and Ray's processes before and after. The breakage (a)–(c). |
| 5 | The release from GitHub | The installs as run, with what each resolved; `direct_url.json`; the five modules equal to `0bae3a3`'s; no tests in `RECORD`. The extraction's smoke run against `v0.2.0` (§1.2): its output, and why step 3 fails. |
| 6 | Issues | The eight resolved, one line each, with the prompt and commit that closed it and the tests that guard it. The six open, each with why it stays open at the close (from its board entry) and what would take it up. |
| 7 | Decisions | L1–L11. One line each: what was decided, when, for which prompt, how it was refined or amended, and the commit where it is applied. |
| 8 | Deviations across the campaign | A table of entry counts per log and class. Then every UNINTENDED DRIFT entry in one line each, with its log and what the review did with it, and every STRUCTURALLY REQUIRED entry that changed what a prompt delivered. |
| 9 | Observations not acted on | Every item of every log's section, one line each, with its log and its disposition at `v0.2.0`: addressed (by which prompt, review or decision), opened as an issue, recorded in the release or adoption notes, still an observation, or no longer true. Decide from the later logs, the board and the notes, never by changing anything. |
| 10 | Known gaps | See the list below this table. |
| 11 | Reproduction | Every command of §3–§5, verbatim, runnable from a clean checkout of the commit that adds this document, with `TMPDIR` set. |
| 12 | Summary for the board | Five to ten lines. |

§10, the known gaps:
- **G1–G3:** no client has adopted `v0.2.0`, and SGK is still pinned at `v0.1.0`
  (`requirements.txt:81` at its newest commit, read through `git show`).
- **What remains unverified:**
  - a real reboot (an earlier boot is tested only by a status written with another `boot`), and a
    real run on another machine (`foreign` only by another `host.id`);
  - Linux only through CI, and containers not at all;
  - a pid reused within one boot (L3 (b), README §8);
  - Python 3.14 beyond the 02c sweep's skip or pass, and L11's window;
  - a client's own stores and run directories: none was opened (README §3);
  - two `begin`s at the same moment (a check, not a lock).
- **The extraction's smoke run** at `v0.2.0` (§1.2).
- **The six open issues.**

Every fact carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section. Where the document and a log disagree, the document
says which is right and why; it does not rewrite the log.

### 2.2 `docs/interrupted-runs/interrupted_run_smoke.py`

A script, not a test. The suite never collects it (discovery is `-s runregistrykit/tests`), and CI's
`black` step checks it. Write it in the form of `docs/extraction/store_smoke_run.py`: a module
docstring saying what it is, how it is run and what it prints.
- **It is self-contained but for the client's module.** It imports `runregistrykit` and its public
  names and the standard library. Nothing of `runregistrykit.tests`, so it runs against an
  installed wheel. It takes `CONFIG`, `GITIGNORE`, `JOB` and `REGISTRY_SOURCE` from
  `docs/extraction/store_smoke_run.py`, loaded by path from the checkout the script lives in, and
  changes nothing in that file. It names no client, in code, strings or comments.
- **The steps are §1.1's thirteen**, each isolated: an exception or an unexpected exit code is that
  step's `FAIL`, with what it saw, and the next step runs where it can. Each prints `PASS` or `FAIL`
  with the command, its exit code and the line that shows the outcome. Every value it asserts is
  its own (states, exit codes, ids, the runs root's listing), never a figure read from a log.
- **Its children.** Each child the script starts is reaped by it, whatever a step does. The script
  signals only its own children. It never leaves a child running: a `finally` kills and reaps any
  that is still alive, and the script says so.
- **How it is run:** `python docs/interrupted-runs/interrupted_run_smoke.py [--clean]`, with the
  package importable, from the repository root. It prints Python's, `runregistrykit`'s and
  `datastorekit`'s versions, `runregistrykit.__file__`, and Ray's and SQLAlchemy's versions if
  installed.
- **It never initialises Ray**, and checks at the end that `ray`, if imported, is not initialised.
- **It removes nothing it did not make**, and leaves its directory in place for inspection unless
  `--clean` is given, which removes only that directory.
- **Its exit code** is 0 only if every step passes, 1 if one fails, and 2 if it cannot start (no
  `git`, the package not importable, or the extraction script not found).

### 2.3 The release

As §1.1: two fresh venvs in the scratchpad, each made with `uv venv --python <the interpreter>` and
filled with `uv pip install --no-cache`, so that the tag is fetched from GitHub. Nothing of it is
committed.

### 2.4 Closing the campaign

- **The board.**
  - Its header says **CLOSED** (2026-10-18, by prompt 07), with all nine prompts landed.
  - §1's row for 07; Z1 ✅.
  - §2's gates are unchanged: G1–G3 have not held, and the campaign does not wait for them
    (README §7). Add a dated line under §2: after the close, a gate is recorded on this board when
    it holds, in a records commit of its own.
  - §3 keeps its six open issues, each with a dated line: open at the close, owner none.
- **The campaign README.** Its header, §2's row for 07, and a dated line under §7: the campaign
  closed at 07, with G1–G3 open.
- **`prompts/INDEX.md`**: the campaign's line, **closed**, with its open-issue count, 6.
- **`docs/OPEN_ISSUES.md`**: the header's date, and §1.3's heading saying the campaign is closed.
  Its count stays 11 unless 07 opens an issue.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **`TMPDIR`.** Set it to your scratch directory for every command that may make a temporary
   directory: the scripts, the suite, `uv`. Nothing is written outside the scratchpad and this
   repository.
2. **The network, once per venv.** The two installs fetch from GitHub and PyPI, and that is the
   only network use. No `git fetch`, `git push` or `gh` call that writes. Reading CI with `gh run
   view` is allowed.
3. **Signals.** The script sends `SIGKILL` and `SIGTERM` only to children it started, and reaps
   each. Before and after each run, record `ps -o pid,ppid,stat,command` for the user's `python`
   processes: no child of a run is left.
4. **Ray is never started.** Before and after every smoke run and every suite run, record `pgrep
   -lf 'gcs_server|raylet|ray::|default_worker\.py'`. If one is up, find whose it is from its
   path. If it is another project's, leave it alone and say so.
5. **The package does not change.** At the end, `git diff aeacba8 -- runregistrykit pyproject.toml
   README.md PROVENANCE.md docs/releases docs/adoption docs/extraction docs/extraction-verification.md
   .github` is empty. A finding is recorded, not fixed (rule 4). The breakage edits scratch copies
   only.
6. **Additive documents.** Under `docs/`, 07 adds two files and changes only `docs/OPEN_ISSUES.md`.
7. **No client is touched.** SGK's newest commit and its `requirements.txt` are read through `git`,
   for G1, and nothing else of any client is read.
8. **The suite runs in `venv/` and at the high end.** For the high end, use a fresh scratch venv
   (3.13.16, `ray==2.55.1`, `sqlalchemy==2.0.46`, `datastorekit` from `v0.4.0`) with a `git clone`
   of your tree installed editable, and run from the clone: the suite needs `runregistrykit/tests`
   and a git work tree (`CLAUDE.md`). The pin venvs hold no tests and do not run the suite.
9. **The document is long.** Its tables are built from the records with scripts or by counting,
   never from memory. Each count it states is one you counted, and the log says how.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 410 tests … OK (skipped=1)` before and after, by module. At the
   high end, as hazard 8, the same. `test_status_writes` at 3.14.8, as the §3 row of §2.1's table
   says.
2. **`black`.** `./venv/bin/black --check runregistrykit docs` (25.1.0) leaves **38** files
   unchanged: 37 and the script.
3. **The smoke run** at both ends, against the pin venvs of §2.3, from the repository root, with
   `TMPDIR` set. The script exits 0. Record its whole output, its time, and Ray's processes and the
   user's `python` processes before and after.
4. **The release**, as §1.1 and §2.3, and the extraction's smoke run as §1.2, its output whole.
5. **The breakage record.** Each item is exactly what was run or changed, in a scratch copy:
   never the repository, never a committed file.
   - **(a) `end` skipped:** step 8 removed from a scratch copy. Step 11's `begin` is refused, naming
     the hard-killed run; step 12's `store fingerprint` is refused; exit 1.
   - **(b) the hard-killed child not reaped** before `end`: in a scratch copy, step 2's `wait()`
     moved after step 8. The killed child is a zombie and answers `kill -0`, so `end` refuses it as
     a live pid. This is `[04-a-killed-process-not-yet-reaped-answers-kill-0]`, measured against
     the release. Step 8 fails, and the child is reaped by the `finally`. Not probed at writing:
     record what `liveness` and `list` say of it before the reap.
   - **(c) the script in a core-only venv**: `runregistrykit @
     git+https://github.com/ds283/RunRegistryKit@v0.2.0` alone, 3.12.15, no `datastorekit`, Ray or
     SQLAlchemy. The client's module cannot be imported, so the steps that need a store fail, each
     with what it saw. No exception escapes a step; exit 1. Not probed at writing: the log lists
     which steps passed and which failed, and why each.
6. **The documents.**
   - Every relative link and anchor in `docs/interrupted-runs-verification.md` resolves, checked by
     a scratch script. Every external link is to `github.com/ds283/…` and names a tag, a commit or
     a run.
   - Every `path:line` it cites at `v0.2.0` is read at `0bae3a3`.
   - Every count it states is recounted, and the log says how.
7. **The clients.** Record SGK's, CPBH's and SI's newest commits at the start and the end,
   unchanged.

---

## 5. Acceptance

1. `docs/interrupted-runs-verification.md` holds §2.1's twelve sections, and every fact in it
   carries its source.
2. `docs/interrupted-runs/interrupted_run_smoke.py` exits 0 at both ends against the GitHub pin,
   never starts Ray, leaves no child, and (a)–(c) fail as §4.5 says.
3. The pin installs at both ends, its modules are `0bae3a3`'s, and it ships no tests.
4. The campaign is closed on the board, in the README, in `prompts/INDEX.md` and in the index.
5. §4.1–§4.7 hold.
6. **The records**, in the same commit:
   - the log, `logs/07-verification-and-close-out.md`, per README §5.1, with:
     - the suite in both venvs by module, and the 3.14.8 run;
     - the installs, each command and what it resolved;
     - the smoke runs, whole, with the processes before and after each;
     - the extraction's smoke run against `v0.2.0`;
     - (a)–(c);
     - the documents' checks, and how each count was made;
     - the clients' commits at the start and the end;
   - the board, as §2.4;
   - `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and the campaign README, as §2.4.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 410, in either venv.
- An install of §2.3 fails to resolve, or installs a commit other than `0bae3a3`, or modules that
  differ from `0bae3a3`'s.
- The smoke script fails a step at either end against the pin. A defect found is opened, not
  fixed. Stop before writing it up, and report.
- A breakage does not fail as §4.5 says.
- The extraction's smoke run fails anything other than step 3, or step 3 for any reason other than
  the summary clause.
- A child of the script is left running, or anything other than its own child is signalled.
- Anything would change a file under `runregistrykit/`, `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `docs/releases/`, `docs/adoption/`, `docs/extraction/`,
  `docs/extraction-verification.md`, the workflow, or any file not in §7.
- Anything would push, make or move a tag, start Ray, or write, run, import or open anything of a
  client or of DatastoreKit, beyond installing `datastorekit` from its tag.

---

## 7. What this prompt changes, and what it does not

- **Files it adds:** `docs/interrupted-runs-verification.md`,
  `docs/interrupted-runs/interrupted_run_smoke.py` and the log.
- **Files it changes:** `docs/OPEN_ISSUES.md`; the board; the campaign README (its header, §2's row
  for 07 and §7's line); and `prompts/INDEX.md`.
- **It changes nothing else.** No file under `runregistrykit/`. Not `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `docs/releases/`, `docs/adoption/`, `docs/extraction/`,
  `docs/extraction-verification.md` or the workflow. Not `CLAUDE.md`, `LICENSE` or `.gitignore`.
- **It touches no client repository, and not DatastoreKit**, beyond reading SGK's, CPBH's and SI's
  newest commits through `git` and installing `datastorekit` from its tag.
- **It makes no tag and pushes nothing.**

---

## 8. The log and the board

`logs/07-verification-and-close-out.md`, using README §5.1, with §5 item 6's additions.

`IMPLEMENTATION_STATE.md`: the header (**CLOSED**), §1's row for 07, Z1, §2's dated line, and §3's
six dated lines.

---

## At writing (2026-10-18, at `aeacba8`)

Measured, for the README's row and the orchestrator; §1 holds the detail.
- **CI** passed all three jobs on `0bae3a3` (run `39143681701`) and on `aeacba8` (run
  `39144321994`); ten runs since 01, all green.
- **The pin from GitHub** installs at both ends, with `commit_id` `0bae3a3`, its modules the tag's
  and no tests in it.
- **An interrupted run** (a hard kill, the refusals, `end`, a real `SIGTERM` and the resume), in
  thirteen steps, passes at both ends against the pin in about 8 s each. No Ray process ran, and no
  child was left.
- **The extraction's smoke run** against `v0.2.0` passes 10 of 11 steps. Step 3 pins `v0.1.0`'s
  `list` summary, which 01 extended.
- **42 commits** from `b56ecc7` to `aeacba8`. The suite went 276 → 410 over eight prompts. Fourteen
  issues were on the board, eight resolved (the five assigned among them) and six open. L1–L11 are
  taken.
- **Not measured**: the entries of each log's deviations and observations (the agent counts them),
  and breakage (b)'s and (c)'s outcomes in full.
