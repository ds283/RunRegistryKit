# Orchestrator — prompt 06, release `v0.2.0`

Read [`../README.md`](../README.md) first: §0, §0.1, §1, §2, §4, §5 (rules 7, 8, 9 and 11
especially), §6.2 (L1–L11 with their notes) and §7. The conventions are those of
[`prompt-05.md`](prompt-05.md), and the release's are those of the extraction campaign's
[`prompt-06.md`](../../extraction/orchestrator/prompt-06.md); both are restated in §0, because the
agent reads §0 and not this directory. Where this note and the prompt differ, this note is right
for 06.

**You do not write code.** You may:
- run the suite, `black --check` and the release check, in `venv/` and in venvs of your own in the
  session scratchpad;
- export or clone this repository's tree at any commit or tag into the scratchpad, build wheels
  there and install them, never committing anything;
- run the package from such an export to build run directories, stores and sidecars of your own in
  the scratchpad, and start a child process there and send it `SIGKILL`, and no other process;
- replay the log's breakage diffs with `git apply` in a scratch clone, and revert them;
- read SGK, ChamPBH and SI **through `git` only**, at the commits the prompt names;
- fix small residue in a follow-up commit of your own (§4).

**Nothing is pushed and no tag is made** by the agent, and nothing by the orchestrator without the
user's clear yes, step by step (the prompt's §7).

**The prompt:** [`06-release-v0.2.0.md`](../06-release-v0.2.0.md) · **Closes:** nothing ·
**Opens:** only what the work finds · **Not touched:** the five open §3 entries, which the release
notes list · **Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: 05 landed and reviewed (`eb68583`, `4a10efb`, CI `39129061916` recorded in
  `80974e2`); **L10 taken 2026-10-18 as (a)** (`7f88787`); `git diff --stat eb68583 HEAD --
  runregistrykit pyproject.toml .github README.md docs` empty; the suite 410 OK with one skip; the
  tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**No behaviour changes, and nearly all of its proof is in documents a client will act on.** One
line of `pyproject.toml`; a dozen places in the README; two new sets of notes. No file under
`runregistrykit/` or `.github/` moves, and the suite stays at 410. The risk is a statement that is
true of the prompt and not of the code, a field the notes name that the registry does not write (or
one it writes that they miss), a mixed-version table measured on a run that was not what it was
called, or a client citation that does not hold at its commit. So the weight of the review is on:
- **the package as it will be tagged**: a wheel of ten entries, no tests, `Version: 0.2.0` and the
  extra's floor, importing from `site-packages` (§3 checks 2, 3);
- **every field the release notes name is written, and every field written is named**, at both
  tags, by the orchestrator's own measurement (§3 check 5);
- **the mixed-version table is true**, each row measured with a run that is what the row says,
  above all an alive one whose pid is alive (§3 check 6);
- **every statement in the README's changes is true of the code** at the commit, checked against
  the code and its `--help`, never against the prompt (§3 check 4);
- **the adoption notes' citations hold at the commits they name**, and the SGK route after a hard
  kill is what this package says (§3 check 7).

**What moves on purpose:** `pyproject.toml` (one line); `README.md` (the prompt's §2.3 rows only);
`docs/releases/v0.2.0.md` (new); `docs/adoption/v0.2.0/README.md`, `secondarygwkit.md`,
`champbh.md` and `stochasticinstantons.md` (new); `docs/adoption/README.md` (one section at its
end); the new log `prompts/interrupted-runs/logs/06-release-v0.2.0.md`; the board; the campaign
README's §2 row for 06 only; `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` only if the work opens an
issue. **Nothing else**: nothing under `runregistrykit/` or `.github/`, not `PROVENANCE.md`,
`CLAUDE.md`, `LICENSE`, `.gitignore`, the three `v0.1.0` checklists,
`docs/adoption/measure_client_registry.py`, `docs/extraction/`, `docs/extraction-verification.md`,
the prompt, any other part of the campaign README, or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **L10 is (a)** (README §6.2, the board's decisions table, `7f88787`). Nothing in the prompt is
   conditional on it.
2. **The suite's time.** `Ran 410 tests in 148.666s` at the gate. Run the suite in the foreground
   with a Bash timeout of at least 600 000 ms, output to a file in your scratch, and grep the
   verdict from the file. A slow run is not a stop; a failing one is.
3. **§2.1's reinstall, and what it shows.** `venv/` has no `setuptools`, so `./venv/bin/python -m
   pip install --no-deps -e .` builds in isolation and fetches `setuptools` from PyPI or `pip`'s
   cache. That is allowed, as at extraction 06, and is **not** the prompt's §5 "download other than
   §3.2's". `pip freeze`'s line for the package is `-e
   git+https://github.com/ds283/RunRegistryKit.git@<HEAD>#egg=runregistrykit`: it names the commit,
   not the version, so **`pip freeze` is expected identical before and after**, which is what "only
   `runregistrykit`'s line changes" protects (extraction 06's correction 3). So record as well
   `importlib.metadata.version("runregistrykit")` before (`0.1.0`) and after (`0.2.0`), **twice
   each**: from the repository root, where `''` on `sys.path` finds the checkout's ignored
   `runregistrykit.egg-info/` first, and from a scratch directory, where the venv's own `dist-info`
   answers. Both must say `0.2.0` after. The reinstall rewrites the ignored egg-info and renames
   the venv's `__editable___runregistrykit_0_1_0_finder.py`; nothing tracked changes, and no
   `build/` is left in the repository (check).
4. **The release check's venv** (§3.2). `uv build --offline --wheel` from an export works here
   (measured: 66 257 bytes, ten entries). `--offline` cannot fetch a **tag** from GitHub, but it
   resolves DatastoreKit **by its commit** from `uv`'s cache: `v0.4.0` is the tag object `8e7c1d7`,
   peeled to `c8570e849334d09085bbd84876095fc9e22bd005` (`git ls-remote
   https://github.com/ds283/DatastoreKit 'refs/tags/v0.4.0*'`; record it). So: `uv venv -p
   /opt/local/bin/python3.13 <scratch>/release`, then `uv pip install --offline -p
   <scratch>/release/bin/python "runregistrykit[stores] @ file://<wheel's absolute path>"
   "datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005"
   "ray==2.55.1" "sqlalchemy==2.0.46"` (measured here with the orchestrator's wheel: it installs
   offline, 21 packages, and `-I` from an empty directory imports the package from `site-packages`
   at `0.2.0`). Record the deviation. The check then runs with `-I` from an empty scratch directory, as the prompt
   says. Remove the venv afterwards.
5. **Which tree a measurement ran.** `-I` ignores `PYTHONPATH`; use it for the installed wheel
   only. §3.3's scripts run `git archive v0.1.0` and `git archive` of the working tree's commit
   (each in a new, empty scratch directory) by `PYTHONPATH`, **without** `-I`, with `venv/`'s
   Python (it has `datastorekit` 0.4.0), from a scratch working directory, never the repository
   root (where `''` would find the checkout). `venv/`'s editable finder is appended to
   `sys.meta_path`, so a tree on `PYTHONPATH` wins, but every script **prints
   `runregistrykit.__file__` and asserts it lies under the export it means**; the log shows it.
   A manifest's `packages.runregistrykit.version` comes from the installed metadata, not from the
   tree that wrote it, so it is no evidence of the writer: record that, and compare shapes, not
   that value.
6. **The mixed-version rows** (§3.3, §2.4.4). At writing, the planner's "alive" run had a pid of a
   child that had exited, so it read as stale in both trees. **An alive row's pid is alive in the
   reading process**: a child the script starts (`[sys.executable, "-c", "import time;
   time.sleep(600)"]`) and keeps alive while both trees read, then kills and reaps, and the log
   shows `pid_alive` true for it at the moment of reading. A dead pid is a child started and
   reaped, as `RegistryTestCase.a_dead_pid` makes one. Each tree's own test fixtures, imported from
   that tree, build its stores, client roots and runs. **Two rows each** for `foreign` and an
   earlier boot, one with the live pid and one with the dead: `v0.1.0` judges both by `kill -0`
   here, so with a live pid it calls them `alive`, and the table must show it. `foreign` is
   written as `test_host.another_id` makes it (another `host.id`), an earlier boot by another
   `host.boot` with this host's `id`, an unreadable status by `test_unreadable_status.FORMS` (a
   torn form at least, and one JSON non-object), `lost` by `end` on the dead pid. For each row:
   `liveness`, `list`'s exit code and the run's marker, `fingerprint_store` on the store it names
   (refused or not, and the refusal's first line), and a second `begin` on that store (begun or
   refused). Every child the script starts is reaped by it; none outlives it.
7. **The README's `:40-41`.** PyPI's newest `ray` was `2.59.0` on 2026-10-18 (read by the
   orchestrator from `https://pypi.org/pypi/ray/json`), so the sentence is unchanged unless your
   read differs. Read it again, record the value, and change the sentence only if it differs.
8. **The prompt's README lines** were read at `7f88787` and are as it cites them (`:12-18`,
   `:40-41`, `:51`, `:62`, `:104-115`, `:123-126`, `:129`, `:131-135`, `:180-184`, `:186-191`,
   `:218-220`, `:274-277`, `:292-296`, `:315-319`; 323 lines). The README names clients in its
   Status already; the no-client guard (`test_package_is_generic`) scans the package only, not
   `README.md` or `docs/`. The release notes still name no client (prompt §2.4).
9. **The README's statements are read from the code at the commit.** Where the prompt's §2.3
   table describes the code (what `begin` refuses and in what words, `this_host()`,
   `RUNREGISTRYKIT_HOST_NAME`, the temporary name's form, the liveness values and `list`'s
   markers and summary lines, `end`'s options and refusals, `store --help`'s wording), the code
   governs; a mismatch with the prompt is recorded as a deviation, and a statement the README must
   make that the code does not bear out is a stop (prompt §5). In particular, take the temporary
   name's form from `_status_temporary_name`, `list`'s markers and lines from `__main__.py` as it
   prints them, and `end`'s from its `--help` and `_end_run`.
10. **The release notes' sources.** §2.4.2's types and meanings come from §3.3's shapes, from 04's
    §2.2 and from `this_host()`'s and `_end_run`'s docstrings, each cited in the log. "What a
    `null` means" is per key and per platform: macOS (measured here) and Linux (CI ran the
    readers there: board, 01's CI note); a `null` written elsewhere means the platform offered
    none. The "For 06" lines the prompt lists are at the cited places (checked: `01:509`,
    `02:586`, `02b:629`, the prompt `03-…:109`, `04:608`, `05:617`); 02c's and 03's logs have
    none. The log lists each with where the notes honour it.
11. **The known issues** are the five §3 headings of the board, by their names, each linked to its
    board entry (`../../prompts/interrupted-runs/IMPLEMENTATION_STATE.md#<anchor>`, GitHub's
    anchor: the heading text with backticks and brackets dropped) and with a line taken from its
    board entry, not from the index. A scratch script checks that the notes' list equals the
    board's §3 headings, and each anchor exists.
12. **The clients**, re-checked by the orchestrator at writing: SGK's newest commit of any branch
    is still `79434bf` (`handover-remedial`, 2026-10-16); CPBH's `main` `3cd2be4`; SI's
    `dk-and-rpk-migration` `5fb4a1d`. SGK's `requirements.txt:81` is the `v0.1.0` pin, and the
    driver and test lines the prompt cites hold (`scoped_pipeline_run.py:544`,
    `quadsource_atol_sweep.py:556`, `:869`, `test_pipeline_adoption.py:252`,
    `test_quadsource_atol_sweep_prepare.py:194`; `interrupt_when.py` calls `pid_alive` and
    `liveness` in `:165-192`). **SGK's `var/` is not in `git`, and is not read**: the adoption
    note says that SGK's existing run directories were written under `v0.1.0`, its only pin, and so
    carry no `host`, and may cite 05's planner's count by link as that planner's; it does not
    re-count them. Every `git grep` is run as `git -C <client> grep … <commit>`, never in a working
    tree, and its command and hits go in the log.
13. **SGK's route after a hard kill**, built in scratch with this package at the commit, as 04's
    `a_hard_killed_run` builds one (a child begun on a store, `SIGKILL`, reaped): the second
    `begin` refused in 05's words naming `runregistrykit end`; `end` accepted; `begin` again
    accepted; its `finish("done", exit_code=0, fingerprint=True)` with a fingerprint. Quote the
    refusal as raised. And what SGK's `--build --resume` meets is read from its driver at
    `79434bf`, not run.
14. **Breakage (c) and (d)** need the agent's own checking scripts, kept in its scratch and not
    committed: (c) a script that reads the notes' field table and compares it with §3.3's shapes;
    (d) one that collects every importable name, argument and option the README's changes name and
    checks each. Each run once on the documents as committed (clean) and once on a scratch copy
    with the break, reporting it. (a) and (b) are applied to a scratch export's `pyproject.toml`,
    never this checkout's.
15. **Line citations.** Every `path:line` in the README's changes, the notes and the log is taken
    from `grep -n` or `sed -n` on the file at the commit it names (this repository's at the commit,
    a client's by `git show <commit>:<path>`), and re-checked just before committing.
16. **`black`.** `black --check runregistrykit docs`: 37 files at the gate, 37 after (no Python
    file changes; the new documents are Markdown).
17. **The records.** The board has an Orchestrator notes line, and the campaign README's row for 06
    a status column. The agent does not edit the notes line, the README's header paragraph, or any
    row but 06's; it sets 06's status to "landed, not yet reviewed" in the board's §1 row ("this
    commit", 410 → 410), the README's §2 row and `prompts/INDEX.md`, and V1 ✅ "this commit". The
    board's header gains one sentence: `v0.2.0` is ready to be tagged on 06's commit once CI has
    passed on that commit, all three jobs, and no tag is made. `docs/OPEN_ISSUES.md` stays at 10
    unless the work opens an issue.

**The facts, checked by the orchestrator on 2026-10-18 at `7f88787`.** Pass them on.
- **In-repository state.** `main` at `7f88787`, clean (`origin/main` at `4a10efb`; `80974e2` and
  `7f88787` unpushed, and this note's commit after them). `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/` (its `PKG-INFO` says `0.1.0`),
  `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`, `var/` and `venv/`.
  `var/ledger.jsonl` (`471d0859…`) is an earlier review's, and is not touched; the suite left it
  unchanged. This checkout is the only worktree. Tags: `v0.1.0` (tag object `fd5ce48`, on
  `9f8ebe4`), here and on `origin`.
- **The suite.** `Ran 410 tests in 148.666s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad;
  `git status --short --ignored` and the ledger the same after it. No Ray process; `RAY_ADDRESS`
  unset. `black --check runregistrykit docs`: 37 files. By the loader: `test_client_root` 27,
  `test_end` 27, `test_end_stores` 4, `test_fingerprinter` 31, `test_host` 28, `test_host_stores`
  3, `test_package_imports` 3, `test_package_is_generic` 22, `test_public_names` 8,
  `test_run_registry` 29, `test_second_writer` 23, `test_second_writer_stores` 9,
  `test_status_writes` 22, `test_store_amend` 21, `test_store_amend_residuals` 9,
  `test_store_command_line` 2, `test_store_copy_move` 27, `test_store_fingerprint` 29,
  `test_store_retire` 41, `test_store_retire_references` 10, `test_store_sidecar` 17,
  `test_unreadable_status` 11, `test_unreadable_status_stores` 7. The workflow's core line
  (`.github/workflows/tests.yml:89`) names seven modules: `test_run_registry`, `test_public_names`,
  `test_host`, `test_status_writes`, `test_unreadable_status`, `test_end`, `test_second_writer`
  (148 tests).
- **Tools.** `venv/`: Python 3.12.15, `pip` 26.2.1, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39,
  `datastorekit` at `c8570e8`, `runregistrykit` editable, version `0.1.0`, no `setuptools`.
  `/opt/local/bin/python3.12` (3.12.15), `python3.13` (3.13.16), `python3.14` (3.14.8); `uv` 0.12.20
  at `/opt/local/bin/uv`. Never give MacPorts' Pythons `-m pip`.
- **The wheel**, built by the orchestrator from `git archive 7f88787` with `version = "0.2.0"`, by
  `uv build --offline --wheel`: `runregistrykit-0.2.0-py3-none-any.whl`, 66 257 bytes, ten entries
  (`runregistrykit/__init__.py`, `__main__.py`, `client.py`, `fingerprint.py`, `stores.py`;
  `runregistrykit-0.2.0.dist-info/licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt`,
  `RECORD`).
- **The index** counts 10. After 06: 10, unless the work opens an issue.

**What the review exists to establish.**
- **(R1) The files.** Only §0's list; nothing under `runregistrykit/` or `.github/`.
- **(R2) The package as it will be tagged.** `pyproject.toml` one line; the wheel of ten entries
  with that metadata; the release check; the venv's version `0.2.0`, from both places.
- **(R3) The README.** The §2.3 rows changed and nothing else; every statement true at the commit.
- **(R4) The release notes.** Every field written named, and none named that is not; the types,
  meanings and `null`s right; both directions of reading right, the mixed-version table among
  them; every public change named from `__all__` and signatures at both tags; the five known
  issues and nothing else; no client named.
- **(R5) The adoption notes.** Every citation true at its commit; every check of the shared
  README's list carried into SGK's note with what it finds; the route after a hard kill true of
  the package; CPBH's and SI's as §2.5 says; `docs/adoption/README.md` gains one section only.
- **(R6) The breakage.** (a)–(d) as recorded, and the orchestrator's.
- **(R7) The records**, with 06 "landed, not yet reviewed" and the tag not made.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `var/`, `*.egg-info/`, `__pycache__/` and `.DS_Store`
  are ignored and must not be staged. Count, then paste. A log states only what the diff, the
  commands and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 2: once before §2.1's reinstall and
  once after.
- **Breakage diffs** are recorded so that `git apply` replays them on a scratch export or clone;
  a breakage that is a command is recorded as the exact command and its output. None is
  committed. After each, `git status` here must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-06/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. Its exports, wheels, venvs, clones and
  scripts live there. **No scratch file goes under `runregistrykit/` or `docs/`**, and no build is
  made in the repository.
- **Installs and network.** `venv/` gets only §2.1's reinstall (correction 3). The one other venv is
  the release check's (correction 4). Read-only network: `pypi.org`'s JSON for `ray`, and `git
  ls-remote` of DatastoreKit. Nothing else is downloaded or installed.
- **Signals.** The measurement scripts send `SIGKILL` to a child they started, and nothing else,
  and reap it. Nothing signals this shell, the agent's own process or any other.
- **Ray.** The agent starts no Ray, and records `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` before and after every suite run.
- **The clients.** SGK, ChamPBH and StochasticInstantons are read through `git -C <repo> show` and
  `git -C <repo> grep` at the commits named, and nothing else: no working tree, no `var/`, nothing
  run or imported. DatastoreKit and RayPoolKit are not read, beyond `datastorekit` installed from
  its commit.
- **GitHub.** Nothing is pushed, no tag is made, no workflow is dispatched.
- **Stop conditions are real** (the prompt's §5). A stop goes to the user through the orchestrator:
  do not commit; end with a STOP report. A statement the code does not bear out is a stop, never a
  softened statement that hides it; a defect found in the package is opened on the board, never
  fixed.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone.
2. **The prompt's gate**, and the suite: 410, one skip, in `venv/`, its time recorded.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 10 now, 10 after unless the work opens one. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md`,
  `CLAUDE.md`, the repository `README.md`, and the logs 01–05;
- `HEAD`, the suite count and time, and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings, and plainly: one commit at the
end; the files of §0 only; `venv/`'s reinstall and the release venv the only installs; `TMPDIR` for
every command; no Ray; `SIGKILL` to its own children only; the clients through `git` only; push
nothing, tag nothing; stop and ask on the prompt's §5.

## 3. The review — ten checks

1. **Scope (R1).** `git show --stat <commit>` touches only §0's list. `git diff <note's commit>
   <commit> -- runregistrykit .github PROVENANCE.md CLAUDE.md LICENSE .gitignore
   docs/adoption/secondarygwkit.md docs/adoption/champbh.md docs/adoption/stochasticinstantons.md
   docs/adoption/measure_client_registry.py docs/extraction docs/extraction-verification.md
   prompts/interrupted-runs/06-release-v0.2.0.md prompts/interrupted-runs/orchestrator` is empty.
   `git diff` of `pyproject.toml` is one line; of `docs/adoption/README.md`, one section appended
   and nothing above it; of the campaign README, 06's row.
2. **The suite (R2).** In `venv/` at the commit: `Ran 410 tests … OK (skipped=1)`, per module as
   §0's facts. `black --check runregistrykit docs`: 37 files. `importlib.metadata.version` `0.2.0`
   from the root and from a scratch directory. `git status --short --ignored` the same as at the
   gate; the ledger unchanged; no `build/` or `dist/`; no Ray.
3. **The wheel, independently (R2).** From a `git archive` of the commit (nothing copied over),
   `uv build --offline --wheel` in the scratchpad: ten entries, `Version: 0.2.0`, `Requires-Dist:
   datastorekit>=0.4.0; extra == "stores"`, no `runregistrykit/tests`. Installed in a fresh 3.13.16
   venv as correction 4 and run with `-I` from an empty directory: the five modules from
   `site-packages`; the version; `this_host` in `runregistrykit.__all__`; `import
   runregistrykit.tests` raising `ModuleNotFoundError`; `--help` and `end --help` exiting 0;
   `DatastoreKitFingerprinter` importing. And the log's wheel: its entry list equal to mine.
4. **The README (R3).** `git diff <note's commit> <commit> -- README.md`, row by row against the
   prompt's §2.3: the opening paragraph, "Supported versions" (but for `:40-41` if Ray moved),
   "Installing" (but for the tag), "The rules" (but for rule 2's sentence), "The public names" (but
   for `this_host`) and "Licence" byte-identical otherwise. Each changed statement checked by the
   orchestrator against the code at the commit: each name imported, each argument against
   `inspect.signature`, each command and option against `--help`, `begin`'s refusal and `end`'s
   outcomes raised in scratch, the temporary name's form against a `status.json.*.tmp` left by a
   writer killed in scratch or against `_status_temporary_name`, `list`'s markers and summary
   lines against a `list` of a runs root holding one run of each kind. The log's list of names
   compared with mine.
5. **The release notes' fields (R4).** The orchestrator's own `lifecycle.py` against `git archive
   v0.1.0` and `git archive <commit>`: the shapes of the manifest, `status.json` while running and
   after `finish`, after `end` (verified, and `--unverified` on an unreadable status), a ledger
   line, the sidecar and the run directory's files. Every key in the notes' §2 is in a shape, and
   every key added since `v0.1.0` is in the notes; the unchanged files said unchanged; the types
   right; `id` a digest and `boot` as `this_host()` says. `__all__` and every public signature at
   both tags against the notes' §5; `list_runs`' keys at both.
6. **The mixed-version table (R4).** The orchestrator's own `mixed.py`, as correction 6, an alive
   row's pid shown alive at reading: every row of the notes' table equal to what I measure, in
   both directions. Any row that differs is a finding.
7. **The adoption notes (R5).** Every `path:line` and commit in the four files checked by `git -C
   <client> show <commit>:<path> | sed -n`; every `git grep` the log records re-run; the shared
   README's list of checks each carried into SGK's note; SGK's route after a hard kill reproduced
   in scratch as correction 13, the refusal's text equal to the note's quotation; CPBH's and SI's
   as §2.5; the `v0.1.0` checklists byte-identical; the stale-run brief's points each answered or
   said unanswered (read at `79434bf`).
8. **The log (R7).** Every section of README §5.1 and the prompt's §4.3 additions: the suite
   before and after; `pip freeze` before and after and the version from both places; the release
   check in full (name, size, entry count, SHA-256, file list); §3.3's outputs or tables for both
   trees, with `runregistrykit.__file__`; the clients' `git grep`s; every statement with its check;
   (a)–(d); the "For 06" lines each with where honoured; the deviations classified, corrections
   1–17 among them.
9. **The breakage (R6).** (a)–(d) replayed from the log: (a) and (b) in a scratch export, the
   release check failing as recorded; (c) and (d) by the agent's scripts as the log records them,
   and failing. Then the orchestrator's own:
   - (o1) the `exclude` widened to `runregistrykit*`: the wheel has no modules, and the release
     check fails at the first import;
   - (o2) one known issue dropped from a scratch copy of the notes: the agent's check of
     correction 11 must report it, or record the gap;
   - (o3) a scratch copy of the notes' table with `host.id` typed `int`: the field check must
     report it if it checks types; if it checks names only, record the gap.
10. **The records (R7).** The board: the header, with the line that `v0.2.0` is ready to be tagged
    on 06's commit once CI is green there and no tag made; 06's row ("this commit", 410 → 410); V1
    ✅; the five §3 entries unchanged. The campaign README's 06 row. `docs/OPEN_ISSUES.md`
    unchanged unless an issue was opened (then the counts by its rows). `prompts/INDEX.md`'s line.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 06* paragraph (*At dispatch*,
  *The checks*, verdict), and add this note to the board's **Orchestrator notes** line, marked
  "used for 06". Fix small residue in a follow-up commit of its own: "this commit" → the SHA on the
  board, in the log, in the README's §2 row and in `prompts/INDEX.md`; "reviewed" for 06 in the
  board's header and row, the README's header paragraph and §2 status column, and
  `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index; a
  document statement that is untrue is a fix prompt before the tag, never residue silently
  corrected in the review's commit, unless it is a wording slip whose correction changes no claim.
- **The release sequence** (the prompt's §7), each step the user's yes:
  1. push 06's commit **alone**: `git push origin <06>:refs/heads/main`, a fast-forward from
     `4a10efb` carrying `80974e2`, `7f88787`, this note's commit and 06's; the review's commit
     stays local;
  2. read the run: all three jobs green, the core job's count 148, the suite 410 at both ends, one
     skip in each, `black` 37 files;
  3. `git tag -a v0.2.0 <06> -m "runregistrykit 0.2.0"` and `git push origin v0.2.0`; record the tag
     object's SHA; never moved or deleted;
  4. push `main` with the review's records and a records commit saying the tag is made.
  If CI fails, a fix prompt lands first; no tag on a red commit.
- **Report to the user:** what landed, 410 → 410; the version line and the wheel; the README's
  changes and that each was checked against the code; the release notes' field table and the
  mixed-version table, as I measured them; the adoption notes; the breakage; and the release
  sequence, asking whether to push 06's commit alone.
