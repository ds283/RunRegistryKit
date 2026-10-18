# Orchestrator — prompt 07, verification and close-out

Read [`../README.md`](../README.md) first: every section, §0.1, §5 and §6.2 (L1–L11 with their notes)
in full, and §7. The conventions are those of [`prompt-06.md`](prompt-06.md), and the close-out's
are those of the extraction campaign's [`prompt-08.md`](../../extraction/orchestrator/prompt-08.md);
both are restated in §0, because the agent reads §0 and not this directory. Where this note and the
prompt differ, this note is right for 07.

**You do not write code.** You may:
- run the suite, `black --check`, the agent's script and the extraction's smoke script, in `venv/`
  and in venvs of your own in the session scratchpad;
- install the pin from GitHub into venvs of your own, as the prompt's §2.3 does;
- replay the log's breakage diffs with `git apply` in a scratch clone, and run your own there;
- start a child process of your own in scratch and send it `SIGKILL` or `SIGTERM`, and no other
  process;
- read SGK, ChamPBH and SI **through `git` only**, as the prompt does;
- fix small residue in a follow-up commit of your own (§4).

No client, DatastoreKit or RayPoolKit is run, imported or edited, and no client's working tree,
index, stash, `venv/`, store or run directory is touched. **Nothing is pushed and no tag is made**,
by the agent or by the orchestrator, without the user's clear yes.

**The prompt:** [`07-verification-and-close-out.md`](../07-verification-and-close-out.md) ·
**Closes:** the campaign · **Opens:** only what the work finds · **Not touched:** the six open §3
entries, which gain a dated line each · **Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: 06 landed (`0bae3a3`) and reviewed (`74f85a2`); `v0.2.0` tag object `895e3c7`
  on `0bae3a3`, on `origin`; CI green on `0bae3a3` (`39143681701`) and `aeacba8` (`39144321994`);
  the gate's diff empty; no `docs/interrupted-runs-verification.md` and no `docs/interrupted-runs/`;
  the suite 410 OK with one skip; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It changes no line of the package, and it is the last prompt.** It writes one long document, one
script, and the campaign's close. For the first time in the campaign it drives an interrupted run as
a client meets one, against the release installed from GitHub. The weight of the review is on:
- **the smoke script is a client's route, against the pin, and fails when it should**: every
  process it runs imports the pin and not this checkout; its thirteen steps assert values of their
  own; it leaves no child; (a)–(c) bite (§3 checks 3–5);
- **every count and fact in the document is true and sourced**: recounted by the orchestrator from
  the records, never taken from the prompt or the log (§3 checks 7, 8);
- **the release is what the tag says**: installed from GitHub, its modules `0bae3a3`'s, no tests
  (§3 check 6);
- **the close is recorded everywhere it must be, and nothing else moves** (§3 checks 1, 10).

**What moves on purpose:** `docs/interrupted-runs-verification.md` and
`docs/interrupted-runs/interrupted_run_smoke.py` (both new); the log
`prompts/interrupted-runs/logs/07-verification-and-close-out.md` (new); the board; the campaign
README (its header, §2's row for 07 and a dated line under §7); `prompts/INDEX.md`;
`docs/OPEN_ISSUES.md`. Seven files. **Nothing else**: nothing under `runregistrykit/` or `.github/`;
not `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`,
`docs/releases/`, `docs/adoption/`, `docs/extraction/`, `docs/extraction-verification.md`, the
prompt, any other part of the campaign README, or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The commits the document reconciles are 44, not 42.** The prompt's §1.3 counts `b56ecc7` to
   `aeacba8`: 42, checked (`git rev-list --count b56ecc7^..aeacba8`; the classes add up, 1 + 9 + 8 +
   8 + 8 + 8, 02c's two writing commits among the nine). After it come `c094811` (07 written) and
   the commit that adds this note, both on `main` before 07's own. The document's §2 runs "to the
   commit before 07's", so it classes those two as well: one more prompt written, one more
   orchestration note. The orchestrator's review of 07 lands after the document and is not in it.
   The agent checks the classes against `git log`, not against this list.
2. **The gate's "`main` is pushed"** reads as: `origin/main` is `aeacba8`, and `c094811` and this
   note's commit are local, as they stay. It is not a stop.
3. **Every process of the smoke run imports the pin, and shows it.** The script runs from the
   repository root, where `''` (for `-c` and `-m`) would find this checkout's `runregistrykit/`.
   So every child and every `python -m runregistrykit …` the script starts runs with its working
   directory the client root under `TMPDIR`, never the repository, and with `PYTHONPATH` unset. The
   script prints its own `runregistrykit.__file__`, each child prints its own beside its run id, and
   the script asserts they are equal and under the venv's `site-packages`; the log shows them. The
   parent itself imports from `site-packages`, since `sys.path[0]` is the script's directory.
4. **"The killed run" in steps 8 and 9 is the hard-killed run of step 2**, not step 7's, which is
   `killed` by its own handler and so already terminal. Step 8's `end` is of step 2's run; step 9
   ends it again. Name the two runs apart in the script's output.
5. **Step 6's "its status is unchanged"** cannot mean byte-identical, since that child goes on
   heartbeating for step 7. It reads as: after both refused `end`s, its `state` is still `running`,
   it has no `ended`, its `exit_code` is `null`, and its `pid` is the child's.
6. **Children are synchronised and bounded.** A child prints one line once it has begun (and, for
   step 7's, once its handler is installed), and the parent reads it with a timeout; a child that
   fails to begin, or never says so, is that step's `FAIL` with its stderr, never a hang. This
   matters for (c), where `begin` may fail in the child. Every wait has a timeout; the `finally`
   kills and reaps any child still alive, and says so.
7. **The signatures the steps use**, at `0bae3a3`: `begin(campaign, prompt, slug, purpose, argv=None,
   cwd=None, script=None, unit=None, expected_units=None, checkpoint=None, results=None, scope=None,
   heartbeat_means=None, pid=None, root=None, when=None, *, client_root=None)`, its `pid` defaulting to
   `os.getpid()`; `Run.heartbeat(self, units_done=None, units_total=None, pid=None, stage=None)`;
   `Run.finish(self, state, exit_code=None, *, fingerprint=False)`; `liveness(status, stale_after,
   now=None, *, here=None)`. The commands: `store create PRIMARY --purpose TEXT`; `store fingerprint
   PRIMARY [--write] [--listing PATH] [--runs-root DIR]`; `store retire PRIMARY --reason TEXT
   [--without-fingerprint] [--dry-run] [--runs-root DIR] [--stores-root DIR]`; `end RUN_ID --reason
   TEXT [--unverified] [--root DIR]`. `end`'s success line is `__main__.py:470`; its refusals are
   `_end_run`'s (`__init__.py:1259`, "already ended" at `:1329`, "answers kill -0" at `:1352`);
   `begin`'s refusal ends `No run directory was created` (`:1125`). Read them again; the code
   governs.
8. **Breakage (b), read whole.** With the `wait()` moved after step 8, the unreaped child is a
   zombie that answers `kill -0`, so with a fresh heartbeat it reads `alive`, not `stale`. So more
   than step 8 may fail: step 2's returncode and `stale`, step 3's `!!` and step 4's naming of `end`
   may each fail, and once the reap lands after step 8, step 9's `end` may succeed and fail its
   check. The prompt's "Step 8 fails" reads as: step 8 fails on "answers kill -0"; every other step
   that fails does so because the zombie answers `kill -0` or because the run was ended late, and
   the log says which and why, with `liveness` and `list`'s row for the run before the reap. A
   further failure with that cause is not a stop; one with another cause is.
9. **(c) in the core-only venv**, as extraction 08's correction 5 read its own. The client module
   imports `sqlalchemy` and `datastorekit`, so no step that needs it, or a store written by it, or
   the fingerprinter, can pass. Read §4.5 (c) as: no step that needs those passes; each that fails
   says what it saw; no exception escapes a step; any step that needs none of them may pass; exit
   1. The log says, step by step, what each needed and why it passed or failed. A step that passes
   needing none of them is not a stop.
10. **The breakage diffs are replayable.** (a) and (b) are recorded in the log as unified diffs
    with the repository path (`a/docs/interrupted-runs/interrupted_run_smoke.py`), so that `git
    apply` replays them in a `git clone` of the agent's commit; the agent applies them to a scratch
    copy only, never in this checkout, and checks each as recorded with `git apply --check` and
    `-R --check`, in `bash`, in a scratch clone of its working tree. (c) is a command and its
    output.
11. **The high-end suite venv** (hazard 8). `git clone` this repository at `HEAD` into the scratch
    directory, install **that clone** editable (`-e "<clone>[stores]"`) with `datastorekit` from
    `v0.4.0`, `ray==2.55.1` and `sqlalchemy==2.0.46` into a fresh 3.13.16 venv, and run the suite
    from the clone's root, so that the package the suite imports, the tests and the git work tree
    are one. The package does not change, so `HEAD`'s clone is the tree under test.
12. **`test_status_writes` at 3.14.8** runs from that clone's root with
    `/opt/local/bin/python3.14`, `PYTHONPATH` the clone, `TMPDIR` set, and the module named
    (`-m unittest -v runregistrykit.tests.test_status_writes`). Measured by the orchestrator at
    `c094811` from this checkout: `Ran 22 tests`, `OK`, **no skip**: 02c's sweep passes at 3.14.8,
    which records nothing about L11's `with` window, since that sweep is at the writer's
    `JUMP_BACKWARD`s. The document says so, and what remains unverified at 3.14 (prompt §2.1, §10).
13. **The suite's per-module counts** come from the loader (`unittest.defaultTestLoader.discover`
    with `-t .`, each module's `countTestCases()`), recorded in both venvs, equal to §0's facts, and
    the one skip named by test in each.
14. **The two indexes' headers.** `prompts/INDEX.md`'s header reads "3 campaigns: 1 closed …, 1 open
    board with no prompts … and 1 open (`interrupted-runs`, 2026-10-16)"; at the close it says 2
    closed, with each date, and the open board. `docs/OPEN_ISSUES.md` §1.3's heading reads "open
    2026-10-16, 01, … and 06 landed"; it says closed 2026-10-18, by 07. Both are within §2.4. The
    count stays **11** unless the work opens an issue.
15. **Outside the scratch directory.** `--no-cache` installs keep `uv`'s work under `TMPDIR`. Before
    and after the work, the log records the names in `/private/tmp` beginning `tmp` or `ray` (at
    dispatch: `ray`, `ray-cpbh`, `ray-cpbh-decoy`, `ray-decoy`, `ray-si`; none of them this
    package's, none to be touched) and their modification times, and explains any change.
    `ray-cpbh` was modified 2026-10-18 00:00 by something not of this repository; a change there is
    recorded, not investigated beyond its time.
16. **The deviation counts.** The label words in the prompt's §1.3 table were recounted by the
    orchestrator (`grep -o`) and agree, log by log. Every log has one "Observations not acted on"
    heading. Entries are the agent's to count, and the log says how (a closing line that says
    "none was UNINTENDED DRIFT" is not an entry).
17. **The document cites the orchestration notes by commit only**, from the board's notes line;
    the agent does not read `orchestrator/`. This note's commit is classed in §2 (correction 1);
    its use for 07 is recorded on the board by the review, not by the agent.
18. **`black`.** `black --check runregistrykit docs`: 37 files at the gate, **38** after (the
    script); the script is formatted before committing.

**The facts, checked by the orchestrator on 2026-10-18 at `c094811`.** Pass them on.
- **In-repository state.** `main` at `c094811`, clean (`origin/main` at `aeacba8`; `c094811` and
  this note's commit unpushed). `git status --short --ignored` shows `prompts/.DS_Store`,
  `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
  `var/` and `venv/`. `var/ledger.jsonl` (`93589747…`) is an earlier review's, and is not touched;
  the suite left it unchanged. This checkout is the only worktree. Tags: `v0.1.0` (tag object
  `fd5ce48`, on `9f8ebe4`) and `v0.2.0` (tag object `895e3c7`, on `0bae3a3`), here and on
  `origin` (`git ls-remote`). `docs/` holds `adoption/` (five files and `v0.2.0/`), `extraction/`
  (three scripts), `releases/v0.2.0.md`, `extraction-verification.md` and `OPEN_ISSUES.md`.
- **The suite.** `Ran 410 tests in 175.358s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad;
  `git status --short --ignored` and the ledger the same after it. No Ray process; `RAY_ADDRESS`
  unset. `black` 25.1.0, `black --check runregistrykit docs`: 37 files. By the loader (06's
  facts, unchanged since: no file under `runregistrykit/` moved): `test_client_root` 27,
  `test_end` 27, `test_end_stores` 4, `test_fingerprinter` 31, `test_host` 28, `test_host_stores`
  3, `test_package_imports` 3, `test_package_is_generic` 22, `test_public_names` 8,
  `test_run_registry` 29, `test_second_writer` 23, `test_second_writer_stores` 9,
  `test_status_writes` 22, `test_store_amend` 21, `test_store_amend_residuals` 9,
  `test_store_command_line` 2, `test_store_copy_move` 27, `test_store_fingerprint` 29,
  `test_store_retire` 41, `test_store_retire_references` 10, `test_store_sidecar` 17,
  `test_unreadable_status` 11, `test_unreadable_status_stores` 7. Run it in the foreground with a
  Bash timeout of at least 600 000 ms, output to a file, and grep the verdict.
- **The tag and CI.** `git ls-remote origin`: `refs/tags/v0.2.0` `895e3c70…`, `^{}`
  `0bae3a3c501a8264ee4be5bc24f06422af38720f`. `gh run list`: the ten runs of the prompt's §1.3
  table, each `success`, on the commits it names.
- **The commits.** 42 to `aeacba8`, classed as the prompt's §1.3 lists them, checked against `git
  log`; then `c094811` and this note's (correction 1).
- **The logs' label words** (`grep -o`), as the prompt's §1.3 table (correction 16).
- **The issues.** Board §3 holds 6, §4 holds 8; the index counts 11 (2 + 3 + 6).
- **The clients, through `git` only.** SGK `handover-remedial` `79434bf4f44d…` (its newest commit
  of any branch), `status --porcelain` 0 lines; CPBH `main` `3cd2be482c26…`, 22 lines; SI
  `dk-and-rpk-migration` `5fb4a1d71a01…`, 0 lines. SGK's `requirements.txt:81` at `79434bf` is
  `runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0`.
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39,
  `datastorekit` at `c8570e8`, `runregistrykit` editable, version `0.2.0`.
  `/opt/local/bin/python3.12` (3.12.15), `python3.13` (3.13.16), `python3.14` (3.14.8); `uv` 0.12.20
  at `/opt/local/bin/uv`. Never give MacPorts' Pythons `-m pip`.

**What the review exists to establish.**
- **(Z1) The files.** Only §0's seven; nothing of the package, the release or adoption notes, the
  extraction's documents or scripts, or the workflow.
- **(Z2) The script.** As prompt §2.2 with corrections 3–7: self-contained but for the client's
  module, client-free, no `runregistrykit.tests`; every process on the pin; Ray never initialised;
  exit 0 at both ends against the pin, 1 in the core-only venv, 2 when it cannot start; no child
  left; its assertions able to fail.
- **(Z3) The release.** The installs, `direct_url.json`, the five modules `0bae3a3`'s, no tests in
  `RECORD`; the extraction's smoke run 10 of 11, step 3 on the summary clause only.
- **(Z4) The document.** §2.1's twelve sections; every fact sourced; every count recounted; every
  link and `path:line` true; the reproduction runnable.
- **(Z5) The re-measurements.** The suite at both ends (410, by module, one skip), 3.14.8's
  `test_status_writes`, `black` (38).
- **(Z6) The breakage.** (a)–(c) as prompt §4.5 with corrections 8–10.
- **(Z7) The close.** The board, the README, `prompts/INDEX.md`, the index, each as §2.4 with
  correction 14; the count 11.
- **(Z8) Nothing outside.** The clients untouched; nothing written outside the scratchpad and this
  repository but what correction 15 allows; no Ray; no child left; this checkout the only worktree.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `var/`, `*.egg-info/`, `__pycache__/` and `.DS_Store`
  are ignored and must not be staged. Count, then paste. A log states only what the diff, the
  commands and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set,
  before and after; the high end as correction 11; 3.14.8 as correction 12. Output to a file in the
  scratch directory, the verdict grepped from it.
- **Breakage diffs** as correction 10. None is committed. After each, `git status` here must be
  clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-07/`), never
  `/tmp`, and sets `TMPDIR` to a directory inside it for every command. Its venvs, clones, client
  roots, copies and outputs live there. **No scratch file goes under `runregistrykit/` or
  `docs/`**, and the smoke script's client roots are made under `TMPDIR`, never in this checkout.
- **Installs and network.** The two pin venvs of §2.3, the core-only venv of (c), and the high-end
  suite venv of correction 11; nothing else is installed, and nothing into `venv/`. Reading CI with
  `gh run view` or `gh run list`, and the tag with `git ls-remote`, is allowed.
- **Signals.** The script and the agent's own probes send `SIGKILL` and `SIGTERM` only to children
  they started, and reap each. Nothing signals this shell, the agent's own process or any other.
  Before and after each smoke run, `ps -o pid,ppid,stat,command` of the user's `python` processes.
- **Ray.** The agent starts no Ray, and records `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` before and after every suite and smoke run. Another
  project's cluster, if running, is left alone.
- **The clients.** Read through `git -C <repository> log`, `rev-parse`, `show` and `status
  --porcelain` only: their newest commits at the start and the end, and SGK's `requirements.txt` at
  its newest commit. Never `cd` into a client to run anything, never `checkout`, `stash`, `fetch` or
  `worktree` there, never import a client's module, never open its `var/`. DatastoreKit only as
  installed from its tag.
- **GitHub.** Nothing is pushed, no tag is made, no workflow is dispatched.
- **Stop conditions are real** (the prompt's §6). A stop goes to the user through the
  orchestrator: do not commit; end with a STOP report. A defect found in the package is opened on
  the board, never fixed and never worked around in the script; a smoke step that fails against the
  pin is a stop before the write-up.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone.
2. **The prompt's gate**; the suite 410 in `venv/`.
3. **The clients.** Each `HEAD` and `status --porcelain | wc -l`, as §0's facts, for check 2.
4. **Ray**, `RAY_ADDRESS`, and `/private/tmp`'s `tmp*` and `ray*` names with their times.
5. **The pin venvs of the orchestrator's own** (`pin-low`, `pin-high`, `pin-core`), installed from
   GitHub as the prompt's §2.3 and (c), for check 4. May be done while the agent works.
6. **The index.** 11 now, 11 after unless the work opens one. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, every log, `docs/OPEN_ISSUES.md`,
  `prompts/INDEX.md`, `CLAUDE.md`, the repository `README.md`, `docs/releases/v0.2.0.md`,
  `docs/adoption/v0.2.0/README.md`, and the precedent's three files (prompt §"Read first" 6);
- `HEAD`, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and plainly: one commit at the
end, its log in README §5.1's form with the prompt's §5 item 6 additions; the seven files of §0
only; the installs of §0 only; `TMPDIR` for every command; no Ray; signals to its own children only;
the clients through `git` only; push nothing, tag nothing; stop and ask on the prompt's §6.

## 3. The review — ten checks

1. **Scope (Z1).** `git show --stat <commit>` touches only §0's seven files, three of them new.
   `git diff <note's commit> <commit> -- runregistrykit pyproject.toml README.md PROVENANCE.md
   docs/releases docs/adoption docs/extraction docs/extraction-verification.md .github CLAUDE.md
   LICENSE .gitignore prompts/interrupted-runs/07-verification-and-close-out.md
   prompts/interrupted-runs/orchestrator` is empty; `git diff 0bae3a3 <commit> -- runregistrykit
   pyproject.toml` is empty; `docs/` gains exactly one document and one script. The campaign
   README's diff is its header, 07's row and §7's line.
2. **Nothing outside (Z8).** Each client's `HEAD` and `status --porcelain | wc -l` equal §0's, and
   the log's at the start and the end. `git worktree list` here shows this checkout alone.
   `/private/tmp`'s names as at dispatch, or each change explained (correction 15). No Ray; no
   `python` process left of the agent's.
3. **Z2, the script by reading.** Imports: the standard library and `runregistrykit` at module
   scope; nothing of `runregistrykit.tests`; `datastorekit` and `sqlalchemy` only in the client
   module's source. The four constants taken from the extraction script by path, that file
   unchanged. **No client name**: scanned by a scratch script of the orchestrator's against the
   forbidden words of `runregistrykit/tests/data/client_vocabulary.json`, by the guard's own
   functions where they can be imported, else by a word match. Each step isolated; every value
   asserted the script's own; every child and command run with its working directory the client
   root and `PYTHONPATH` unset, and each child's `runregistrykit.__file__` checked (correction 3);
   every wait bounded; the `finally` reaping; signals only to its own children; the Ray check at
   the end; `--clean` removing only its directory; exits 0, 1 and 2 as §2.2.
4. **Z2, the script run by the orchestrator** against `pin-low`, `pin-high` and `pin-core`, from
   the repository root at the commit, `TMPDIR` set, Ray and the user's `python` processes recorded
   before and after each:
   - `pin-low` and `pin-high`: exit 0, thirteen `PASS`, every child's `runregistrykit.__file__`
     under that venv's `site-packages`, no child left;
   - `pin-core`: exit 1, each step's verdict as the log says, no traceback outside a step;
   - exit 2: with an interpreter that cannot import the package (`/opt/local/bin/python3.12 -I`),
     with `PATH` lacking `git`, and with the extraction script out of reach (a copy of the script
     alone in a scratch directory);
   - `--clean`: its directory gone, nothing else; without it, its directory left.
5. **Z6, the breakage.** (a) and (b) extracted from the log by a script and replayed in `bash` in a
   `git clone` of the commit (`--check`, apply, the run in `pin-low`, `-R --check`, reverse), each
   failing as the log says, (b) as correction 8. Then the orchestrator's own, each in the clone:
   - (o1) step 7's child's handler made to exit `128 + signum` without calling `run.finish`: the
     returncode is still 143, so step 7 must fail on the status, which stays `running`;
   - (o2) step 4's `store fingerprint` pointed at the second store, which no run names yet: it
     exits 0, and step 4 must fail;
   - (o3) step 5's second `begin` given the second store in place of the first: it is accepted and
     makes a run directory, and step 5 must fail, on the missing refusal and on the runs root's
     listing both (the script's `finally` and `--clean` deal with the extra run).
   For (o2) and (o3), "the second store" is the script's own if it exists by then, else a store
   written for the purpose by the client module, which no run names.
   An assertion that does not bite is opened on the board (owner to be put to the user), not a
   stop.
6. **Z3, the release.** In the orchestrator's pin venvs: `direct_url.json` `commit_id`
   `0bae3a3c501a…`, `requested_revision` `v0.2.0`; the five modules of
   `site-packages/runregistrykit/` `cmp`-equal to `git show 0bae3a3:runregistrykit/<module>`;
   `RECORD` naming no `tests/`; `import runregistrykit.tests` a `ModuleNotFoundError`;
   `datastorekit`, `ray` and `sqlalchemy` absent from `pin-core`. The log's installs agree. The
   extraction's smoke run in `pin-low`: 10 of 11, step 3 failing on the summary clause and nothing
   else, output equal in its verdicts to the log's.
7. **Z4, the document by checking.** The twelve sections of §2.1, in order, and its head as §2.1
   says. A scratch script of the orchestrator's checks every relative link and anchor resolves and
   every external link is to `github.com/ds283/…` naming a tag, a commit or a run. Every `path:line`
   extracted and read at its tree (package lines at `0bae3a3`, campaign files at the commit cited,
   SGK's at `79434bf`): a sample of at least twenty-five, spread over the sections, compared by
   text. §11's reproduction: a sample of its commands run verbatim from a fresh `git clone` of the
   commit, `TMPDIR` set.
8. **Z4, the counts, recounted by the orchestrator.** The 44 commits and their classes (correction
   1) against `git log`; the ten CI runs against `gh run list`; the suite's progression against each
   log's "before and after"; the fourteen issues against §3 and §4 (six open, eight closed, each
   with the prompt and commit that closed it); L1–L11, each with its date and prompt; the deviation
   entries per class in at least four logs (06, 05 and 02c among them) counted independently;
   every UNINTENDED DRIFT entry the document lists against the logs; the observations of at least
   three logs, each item's disposition checked against the later records. Any disagreement with the
   document is a finding; a disagreement with a log is the document's to explain (prompt §2.1, last
   paragraph).
9. **Z5, the re-measurements.** In `venv/` at the commit: `Ran 410 tests … OK (skipped=1)`, per
   module as §0's facts; `black --check runregistrykit docs` 38 files; `git status --short
   --ignored` the same before and after; the ledger unchanged; no Ray. The log's high-end and 3.14.8
   runs agree with §0's facts and correction 12.
10. **Z7, the records.** The log has every section of README §5.1 and the prompt's §5 item 6
    additions, the deviations classified (corrections 1–18 among them). The board: header
    **CLOSED** (2026-10-18, by 07), 07's row ("this commit", 410 → 410), Z1 ✅, §2's dated line,
    §3's six dated lines and nothing else of §3 changed. The campaign README's header, §2 row and §7
    line. `prompts/INDEX.md`: closed, 6 open issues, its header (correction 14).
    `docs/OPEN_ISSUES.md`: **11** by counting its rows, the date, §1.3's heading closed.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 07* paragraph, in the form of
  06's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in the document if it names its own commit,
    in the campaign README and in `prompts/INDEX.md`;
  - "reviewed" for 07 in the board's header and row, README §2's status column and its header, and
    `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 07".
  The document is additive from its commit (`CLAUDE.md` rule 6): the follow-up substitutes the SHA
  and corrects nothing else in it; a finding about it is recorded on the board, and in a new
  subsection of the document only if the user asks.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed, 410 → 410, and the campaign closed;
  - the smoke run at both ends against the GitHub pin, the core-only run, and the breakage, the
    agent's and the orchestrator's;
  - the release re-checked: the installs, the modules, no tests; the extraction's smoke run;
  - the document's headline counts, and anything the recount changed;
  - what remains: G1–G3, the six open issues, and the document's known gaps;
  - nothing pushed, and whether to push `main`.
