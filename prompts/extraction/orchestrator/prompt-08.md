# Orchestrator — prompt 08, verification and close-out

Read [`../README.md`](../README.md) first: every section, and §6.2 (U1–U24) in full. The
conventions are [`prompt-07.md`](prompt-07.md)'s and its predecessors'; they are restated in §0
because the agent reads §0 and not this directory. Where this note and an earlier one differ, this
one is right for 08.

**You do not write code.** You may:
- run the suite, `black --check`, the agent's script, `compare_with_source.py` and
  `measure_client_registry.py`, in `venv/` or in venvs of your own in the session scratchpad;
- install the pin from GitHub into venvs of your own, as the prompt's §2.3 does;
- replay the log's breakage diffs with `git apply` in a scratch clone, and run your own there;
- read the clients **through `git` only**, at the commits named, as the prompt does;
- fix small residue in a follow-up commit of your own (§4).

No client, DatastoreKit or RayPoolKit is run, imported or edited, and no client's working tree,
index, stash, `venv/`, store or run directory is touched. **Nothing is pushed and no tag is made**,
by the agent or by the orchestrator, without the user's clear yes.

**The prompt:** [`08-verification-and-close-out.md`](../08-verification-and-close-out.md)
**Closes:** the campaign · **Opens:** only what the work finds · **Model:** Opus, as the prompt
recommends (the user's change, 2026-10-15).

**Gate:**
- The prompt's gate: 07 landed (`aaab408`) and reviewed (`aaa1d6d`); CI green in all three jobs on
  `aaa1d6d`; the gate's diff empty; `v0.1.0` tag object `fd5ce48` on `9f8ebe4`; the tree clean; the
  suite 276 OK; U23 and U24 taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- Each client's `HEAD` is still §0's. If one has moved, the checklists' commits still govern
  (prompt §1.3); record it and pass it on, it is not a stop.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It changes no line of the package, and it is the last prompt.** It writes one long document, one
script, and the campaign's close. The weight of the review is on four things:
- **every count and fact in the document is true and sourced**: recounted by the orchestrator from
  the records, never taken from the prompt or the log (§3 checks 7, 8);
- **the smoke script is a client's path, and fails when it should**: self-contained, run by the
  orchestrator against the GitHub pin at both ends and in the core-only form, its assertions shown
  to bite (§3 checks 3–5);
- **the release is what the tag says**: installed from GitHub, its modules `9f8ebe4`'s, no tests
  (§3 check 6);
- **the close is recorded everywhere it must be and nothing else moves** (§3 checks 1, 10).

**What moves on purpose:** `docs/extraction-verification.md` and
`docs/extraction/store_smoke_run.py` (both new); the log
`prompts/extraction/logs/08-verification-and-close-out.md` (new); the board; the campaign README
(its header, §2's row for 08 and a dated line under §7); `prompts/INDEX.md`; `docs/OPEN_ISSUES.md`.
**Nothing** under `runregistrykit/`, `docs/adoption/` or `.github/`; not
`docs/extraction/compare_with_source.py` or `measure_client_vocabulary.py`; not `pyproject.toml`,
`README.md`, `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`, the prompt or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The commits the document reconciles are 45, not 43.** The prompt's §1.3 counts `745c9d9` to
   `aaa1d6d` (43, checked: `git rev-list --count aaa1d6d` is 43 and the classes add up, 2 + 10 + 10
   + 10 + 10 + 1). After it come `7540efb` (08 written, U23 and U24 recorded) and the commit that
   adds this note, both on `main` before 08's own. The document's §2 runs "to the commit before
   08's", so it classes those two as well: one more prompt written, one more orchestration note. The
   orchestrator's review of 08 lands after the document and is not in it.
2. **`known()` returns a dict, keyed by unit.** `Run.known(self, notice=sys.stderr) -> dict`; step
   2's "`known()` giving `["u1"]`" reads as `sorted(run.known()) == ["u1"]`. The other signatures
   the steps use, at `9f8ebe4`: `finish(self, state, exit_code=None, *, fingerprint=False)`;
   `record(self, unit, data=None)`; `heartbeat(self, units_done=None, units_total=None, pid=None,
   stage=None)`; `DatastoreKitFingerprinter(factories, fingerprint_format: int)`. `store retire`
   requires `--reason`; `store create` and `store copy` require `--purpose`; `store adopt`'s
   `--purpose` is optional; `store amend` requires `--field` and `--reason`.
3. **The digest will not be the planner's.** The prompt's `c62012bd…` is the digest of the tests'
   neutral store, which the planner's probe copied into the client root. The script writes a
   smaller module of its own, so its digest is its own. What is checked is that **the two ends print
   the same digest**, the script printing it and not asserting it (prompt §2.2); the log and the
   document give it, and say why it differs from the prompt's figure. A different digest from the
   prompt's is not a stop; different digests at the two ends are, under §6's third condition.
4. **The high-end suite venv** (hazard 7). "A `git archive` of your tree installed editable … run
   it from a `git clone`" reads as: `git clone` this repository at `HEAD` into the scratch
   directory, install **that clone** editable (`-e "<clone>[stores]"`) with `datastorekit` from
   `v0.4.0`, `ray==2.55.1` and `sqlalchemy==2.0.46` into a fresh 3.13.16 venv, and run the suite
   from the clone's root, so that the package the suite imports, the tests and the git work tree
   are one. The package does not change, so `HEAD`'s clone is the tree under test. The clone and the
   venv stay in the scratch directory.
5. **(c) in the core-only venv.** At `9f8ebe4`, `begin(results=…)` reads the store's sidecar before
   it creates anything, and a primary with no sidecar is not a refusal; `finish(fingerprint=True)`
   records a fingerprint it cannot take as `fingerprint_error` and stays `done`. So without
   `datastorekit` step 2's run may begin and finish, and the step fails on `fingerprint_error`'s
   presence. Step 11's two refusals need neither a store nor a fingerprinter, so step 11 may pass
   whole. Read §4.5 (c) as: no step that needs a store or a fingerprinter passes; each that fails
   says what it saw; no exception escapes a step; the steps that need neither pass; exit 1. A step
   that passes beyond those the prompt names is not a stop if it needs neither; the log says, step
   by step, what each needed and why it passed or failed.
6. **The two indexes' headers.** `prompts/INDEX.md`'s header reads "1 campaign: 1 live"; at the
   close it says the campaign is closed, with its date. `docs/OPEN_ISSUES.md` §1.1's heading reads
   "— live 2026-10-15"; it says "closed 2026-10-15". Both are within §2.4.
7. **The breakage diffs are replayable.** (a) and (b) are diffs to the committed script, recorded in
   the log as unified diffs with the repository paths (`a/docs/extraction/store_smoke_run.py`), so
   that `git apply` replays them in a `git clone` of the agent's commit. The agent applies them in a
   scratch copy only, never in this checkout. (b)'s `UPDATE` is the agent's own: its store has its
   own tables, so the prompt's `Solution … log10_step` is the neutral store's and stands only as a
   model.
8. **The network, beyond the installs.** The orchestrator has read the tag on `origin` (`git
   ls-remote`: `fd5ce48`, peeling to `9f8ebe4`) and the four CI runs (`gh run view`, each
   `success`, the three jobs on `aaa1d6d`); the agent need not repeat the first, and may confirm
   CI with `gh run view` or read-only `gh api`, as the prompt allows. Nothing else uses the network.
9. **Outside the scratch directory.** `--no-cache` installs keep `uv`'s work under `TMPDIR`. The
   offline rebuild (§1.2) reads `uv`'s own cache, which is the one place outside the scratchpad
   and this repository that may be read; the log says so. `/private/tmp` is busy with other
   programs' files, so the check is narrow: before and after the work, the log records the names
   in `/private/tmp` beginning `tmp` or `ray` (at dispatch: `ray`, `ray-cpbh`, `ray-cpbh-decoy`,
   `ray-decoy`, `ray-si`, all older than 2026-10-15, none of them this package's) and the
   modification time of `/private/tmp/ray`, and explains any change.
10. **The suite's per-module counts** come from the loader (`unittest.defaultTestLoader.discover`
    with `-t .`, each module's `countTestCases()`), as 06's correction 9 had it; the per-module
    figures are recorded in both venvs and must agree.

**The facts, checked by the orchestrator on 2026-10-15 at `7540efb`.** Pass them on.
- **In-repository state.** `main` at `7540efb`, clean (`origin/main` at `aaa1d6d`); `git status
  --short --ignored` shows `prompts/.DS_Store`, `runregistrykit.egg-info/`,
  `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the
  only worktree; no `var/`; `docs/` holds `adoption/` (five files), `extraction/` (two scripts) and
  `OPEN_ISSUES.md`; no `docs/extraction-verification.md`. `git diff aaa1d6d HEAD -- runregistrykit
  docs pyproject.toml PROVENANCE.md CLAUDE.md README.md .github` empty; `git diff 9f8ebe4 HEAD --
  runregistrykit pyproject.toml` empty. The suite, with `TMPDIR` set to the scratchpad: `Ran 276
  tests in 92.419s`, OK. `black` 25.1.0, `black --check runregistrykit docs`: 27 files unchanged.
  No Ray process; `RAY_ADDRESS` unset.
- **The tag and CI.** `git ls-remote origin`: `refs/tags/v0.1.0` `fd5ce48…`, `^{}` `9f8ebe431503…`.
  Runs, all `success`: `38754093289` (`9f8ebe4`), `38755672939` (`4ee947b`), `38768740409`
  (`dca5ead`), `38787646775` (`aaa1d6d`: `core (no store layer)`, `suite (low)`, `suite (high)`).
- **The pin, installed by the orchestrator** (uv 0.12.20, `--no-cache`, `TMPDIR` the scratchpad):
  `[stores]` with the `datastorekit` line at 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 and at
  3.13.16 / 2.55.1 / 2.0.46, and the core-only form at 3.12.15. Each resolved; `runregistrykit`
  0.1.0, `direct_url.json` `commit_id` `9f8ebe431503fb8c79ee1407cc460501f1ca2d92`,
  `requested_revision` `v0.1.0`; `datastorekit` 0.4.0 in the two `[stores]` venvs; none of
  `datastorekit`, `ray`, `sqlalchemy` in the core venv.
- **The commits.** 43 to `aaa1d6d`, classed as the prompt's §1.3 lists them, checked against `git
  log`; then `7540efb` and this note's (correction 1).
- **The logs' label words** (`grep -o`), as the prompt's §1.3: 01 1 / 11 / 1, 02 1 / 8 / 0, 03 7 /
  11 / 0, 04a 6 / 14 / 1, 04b 5 / 9 / 1, 05a 2 / 10 / 1, 05b 7 / 8 / 1, 05c 6 / 8 / 1, 06 10 / 7 /
  0, 07 12 / 11 / 2. Every log has one "Observations not acted on" heading. Entries are the agent's
  to count.
- **The issues.** Board §3 holds 2, §4 holds 11; the index counts 2.
- **The clients, through `git` only.**

  | Repository | Branch | `HEAD` | `status --porcelain` lines / `shasum` | Stash | Worktrees |
  |---|---|---|---|---|---|
  | `SecondaryGWKit` | `handover-remedial` | `14bcac0eb73069131f8ce4f55d91e5fc3e7318cf` | 0 / `da39a3ee…` | 0 | 1 |
  | `ChamPBH` | `main` | `c21cdfb5613a3ed976a91a95431495dc8bfd49c8` | 22 / `fbd525ec…` | 0 | 1 |
  | `StochasticInstantons` | `dk-and-rpk-migration` | `5fb4a1d71a016f1b23393923b9a3d59972415aa0` | 0 / `da39a3ee…` | 0 | 1 |
  | `DatastoreKit` | `main` | `b01737f139e5…` | 0 | 0 | 1 |
  | `RayPoolKit` | `main` | `17029d99bb26…` | 0 | 0 | 1 |

  Each is the checklists' commit, so `measure_client_registry.py` runs at its default.
- **The interpreters.** `/opt/local/bin/python3.12` (3.12.15) and `/opt/local/bin/python3.13`
  (3.13.16); `uv` 0.12.20 at `/opt/local/bin/uv`. `list` in a directory under the scratchpad exits
  1 with `!! No runregistrykit.toml in … or any directory above it.`

**What the review exists to establish.**
- **(V1) The files.** Only §0's list changes; nothing of the package, the adoption documents, the
  other scripts or the workflow.
- **(V2) The script.** As prompt §2.2: self-contained, client-free, no `runregistrykit.tests`, no
  module-scope `datastorekit`; Ray never initialised; exit 0 at both ends against the pin, 1 in the
  core-only venv, 2 when it cannot start; its assertions able to fail.
- **(V3) The release.** The three installs, the five modules `9f8ebe4`'s, no tests in `RECORD`, the
  offline rebuild's entries.
- **(V4) The document.** §2.1's twelve sections; every fact sourced; every count recounted; every
  link and `path:line` true; the reproduction runnable.
- **(V5) The re-measurements.** The suite at both ends (276, by module), `black` (28),
  `compare_with_source.py` at `8155445` (`RESULT: OK`), the three appendices byte-equal.
- **(V6) The breakage.** (a)–(c) as prompt §4.5 with correction 5.
- **(V7) The close.** The board, the README, `prompts/INDEX.md`, the index, each as §2.4 with
  correction 6; the count 2.
- **(V8) Nothing outside.** The clients untouched; nothing written outside the scratchpad and this
  repository but what correction 9 allows; no Ray; this checkout the only worktree after.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff, the commands
  and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set.
  Write the output to a file in the scratch directory and grep the verdict from it. Run it **in the
  foreground**, within the turn; it takes about 95 s. The high end as correction 4.
- **Breakage diffs** as correction 7. Check each **as recorded in the log** with `git apply
  --check` and `-R --check`, in `bash`, not zsh, in a scratch clone. None is committed. After each,
  `git status` here must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-08/`), never
  `/tmp`, and sets `TMPDIR` to a directory inside it for every command. Its venvs, clones, client
  roots, worktrees, wheels and outputs live there. **No scratch file goes under `runregistrykit/`
  or `docs/`**, and the smoke script's client roots are made under `TMPDIR`, never in this
  checkout.
- **This repository's worktrees.** `compare_with_source.py` runs from a `git worktree add --detach`
  of `8155445` in `agent-08/`, with `venv/`'s Python by absolute path, and the worktree is removed
  (`git worktree remove`, then `git worktree prune`) before the commit; `git worktree list` shows
  this checkout alone at the end.
- **The clients.** Read through `git -C <repository> ls-tree`, `show`, `grep`, `log`, `rev-parse`,
  `status --porcelain` and `stash list` only, and by `compare_with_source.py` and
  `measure_client_registry.py`. Never `cd` into a client to run anything, never `checkout`,
  `stash`, `fetch` or `worktree` there, never `import` a client's module, never open its `var/`.
  DatastoreKit only as installed from its tag; RayPoolKit's precedents through `git show`.
- **Installs and network.** The three pin venvs of §2.3, the high-end suite venv of correction 4,
  and the offline rebuild; nothing else is installed, and nothing into `venv/`.
- **GitHub.** Nothing is pushed, no tag is made, no repository setting changes, no workflow is
  dispatched. `gh run view` and read-only `gh api` calls are fine.
- **Ray.** The agent starts no Ray, and records `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` before and after every suite and smoke run. Another
  project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A defect found in the package is opened on the board, never fixed and
  never worked around in the script; a smoke step that fails against the pin is a stop before the
  write-up.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` and no
   `docs/extraction-verification.md`.
2. **The prompt's gate**; the suite 276 in `venv/`.
3. **The clients.** Each `HEAD`, `status --porcelain | shasum` and `stash list | wc -l` as §0's
   table, recorded for check 2.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
5. **The index.** 2 now, 2 after unless the work opens one. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, every log, `docs/OPEN_ISSUES.md`,
  `prompts/INDEX.md`, `CLAUDE.md`, `README.md`, `PROVENANCE.md` and `docs/adoption/README.md`;
- `HEAD`, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/` (the document cites the notes by commit only, from the
  board's notes line).

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/08-verification-and-close-out.md`, in README §5.1's
  form, with the prompt's §5 item 6 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It reads the clients through `git` only, and runs, imports and edits none of them**, nor
  DatastoreKit or RayPoolKit.
- **It installs only what §0 lists, sets `TMPDIR` for every command, and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list (seven files, two of them new
   documents and one the new log). `git diff 7540efb <commit> -- runregistrykit pyproject.toml
   README.md PROVENANCE.md docs/adoption docs/extraction/compare_with_source.py
   docs/extraction/measure_client_vocabulary.py .github CLAUDE.md LICENSE .gitignore
   prompts/extraction/08-verification-and-close-out.md prompts/extraction/orchestrator` is empty;
   `git ls-files runregistrykit` the same 26; `docs/` holds exactly one new document and one new
   script.
2. **Nothing outside.** Each client's `HEAD`, `status --porcelain | shasum`, `stash list | wc -l`
   and `worktree list` equal §0's table, and the log's before and after. `git worktree list` here
   shows this checkout alone. `/private/tmp`'s `tmp*` and `ray*` names, and `/private/tmp/ray`'s
   modification time, as at dispatch (correction 9), or each change explained.
3. **V2, the script by reading.** Its imports: the standard library and `runregistrykit` at module
   scope; `datastorekit` only inside the client module's source string or a step's function;
   nothing of `runregistrykit.tests`. Its client module on the public names the prompt lists, with
   a replicated class, a sharded class with a parent, the tag and version tables. **No client
   name**: the script scanned by a scratch script of the orchestrator's against the forbidden words
   of `runregistrykit/tests/data/client_vocabulary.json`, by the guard's own functions where they
   can be imported, else by a word match. Each step isolated; every asserted value the script's
   own; the digest printed, not asserted; the Ray check at the end; `--clean` removing only its
   root; exits 0, 1 and 2 as §2.2.
4. **V2, the script run by the orchestrator** against the orchestrator's own pin venvs (`pin-low`,
   `pin-high`, `pin-core`, installed at dispatch from GitHub as §0's facts), from the repository
   root at the commit, `TMPDIR` set, Ray checked before and after each:
   - `pin-low` and `pin-high`: exit 0, eleven `PASS`, the same digest at both ends and equal to the
     log's;
   - `pin-core`: exit 1, each step's verdict as the log says, no traceback outside a step;
   - exit 2: run with an interpreter that cannot import the package (`/opt/local/bin/python3.12
     -I`), and with `PATH` lacking `git`;
   - `--clean`: the root gone, nothing else; without it, the root left.
5. **V6, the breakage.** (a) and (b) extracted from the log by a script and replayed in `bash` in a
   `git clone` of the commit (`--check`, apply, the run in `pin-low`, `-R --check`, reverse), each
   failing as the log says: (a) the steps that load the fingerprinter fail on the class refusal and
   the store's files survive step 9; (b) step 5 names the class that differs and `store retire`
   refuses with every file kept. Then the orchestrator's own, each in the clone:
   - (o1) step 2's check of `fingerprint_error`'s absence removed, with (a)'s config: step 2 then
     passes, so that check is what catches a fingerprinter that cannot load at `finish`;
   - (o2) step 10's check made to expect the run under the **worktree's** `var/runs/`: step 10
     fails, so the step shows Q3's rule;
   - (o3) the client module's format bumped (`DatastoreKitFingerprinter(FACTORIES, 2)`) between
     steps 2 and 5: step 5 fails on the version entry.
   An assertion that does not bite is opened on the board (owner to be put to the user), not a
   stop.
6. **V3, the release.** In the orchestrator's pin venvs: the five modules of
   `site-packages/runregistrykit/` `cmp`-equal to `git show 9f8ebe4:runregistrykit/<module>`;
   `RECORD` naming no `tests/`; `import runregistrykit.tests` a `ModuleNotFoundError`. The log's
   three installs agree with §0's facts (`commit_id`, versions, the core venv's three absent). The
   offline rebuild's entry list and module contents compared with the log's, by entries, never by
   hash.
7. **V4, the document by checking.** The twelve sections of §2.1, in order. A scratch script of the
   orchestrator's checks every relative link and anchor resolves and every external link is to
   `github.com/ds283/…` naming a tag, a commit or a run. Every `path:line` extracted and read at its
   tree (package lines at `9f8ebe4`, client lines at the checklists' commits, campaign files at the
   commit cited): a sample of at least twenty-five, spread over the sections, compared by text.
8. **V4, the counts, recounted by the orchestrator.** The 45 commits and their classes (correction
   1) against `git log`; the suite's progression against each log's "before and after"; the
   thirteen issues against §3 and §4 (two open, eleven closed, each with the prompt and commit that
   closed it); the decisions (D1, D3, D4, Q1–Q5, Q7, U1–U24, 07's ruling); the deviation entries
   per class in at least four logs (07 and 06 among them) counted independently; the observations
   of at least three logs, each item's disposition checked against the later records. Any
   disagreement with the document is a finding; a disagreement with a log is the document's to
   explain (prompt §2.1, last paragraph).
9. **V5, the re-measurements, run by the orchestrator.** `compare_with_source.py` from a detached
   worktree of `8155445`, output equal to the log's, the worktree removed after; the three
   `measure_client_registry.py` outputs `cmp`-equal to the appendices; a sample of §11's
   reproduction commands run verbatim from a fresh `git clone` of the commit.
10. **V5, V7, the suite and the records.** In `venv/` at the commit: `Ran 276 tests … OK`, per module
    as the log's; `black --check runregistrykit docs` 28 files unchanged; `git status --short
    --ignored` the same before and after but for `__pycache__/`; no `var/`; no Ray process. The log
    has every section of README §5.1 and the prompt's §5 item 6 additions, the deviations
    classified (corrections 1–10 among them). The board: header **CLOSED**, 08's row ("this
    commit", 276 → 276), Z1 ✅, §2's dated line, §3's two dated lines. The campaign README's header,
    §2 row and §7 line. `prompts/INDEX.md` closed, 2 open issues, its header (correction 6).
    `docs/OPEN_ISSUES.md`: **2** by counting, the date, §1.1's heading closed.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 08* paragraph, in the form of
  07's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in the document if it names its own commit,
    in the campaign README and in `prompts/INDEX.md`;
  - "reviewed" for 08 in the board's header and row, README §2's status column and its header, and
    `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 08".
  The document is additive from its commit (`CLAUDE.md` rule 6): the follow-up substitutes the SHA
  and corrects nothing else in it; a finding about it is recorded on the board, and in a new
  subsection of the document only if the user asks.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed, 276 → 276, and the campaign closed;
  - the smoke run at both ends against the GitHub pin, its digest, the core-only run, and the
    breakage, the agent's and the orchestrator's;
  - the release re-checked: the installs, the modules, no tests, the offline rebuild;
  - the document's headline counts, and anything the recount changed;
  - what remains: G2–G4, the two open issues (requests to DatastoreKit), and the document's known
    gaps;
  - nothing pushed, and whether to push `main`.
