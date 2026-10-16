# Orchestrator — prompt 01, the host

Read [`../README.md`](../README.md) first: §0 and §0.1, §0.2 (the identifier table), §5 (every
rule; 7, 8, 9 and 10 especially) and §6.2 (L1–L4, taken). The conventions are those of the
`extraction` campaign's notes (`prompts/extraction/orchestrator/`), restated in §0 because the agent
reads §0 and not this directory. Where this note and the prompt differ, this note is right for 01.

**You do not write code.** You may:
- run the suite, `black --check` and the tests the log names;
- replay the log's mutation diffs with `git apply` in a scratch clone, and revert them;
- build venvs, client roots and run directories of your own in the session scratchpad, and run the
  package in them;
- fix small residue in a follow-up commit of your own (§4).

SGK, ChamPBH and SI are not read or run by this prompt or its review. **Nothing is pushed** by the
agent, and nothing by the orchestrator without the user's clear yes (§4).

**The prompt:** [`01-the-host.md`](../01-the-host.md)
**Closes:** `[04-runs-do-not-say-which-machine-produced-them]` · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate: the campaign planned (`b56ecc7`), L1–L4 taken, the package `v0.1.0`'s, the
  suite 276 OK, the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the campaign's first change to what the registry writes**, and it changes the judgement that
`list` and every store operation make about a `running` run. The weight of the review is on four
things:
- **an old record is judged exactly as before** (README §5 rule 8): a `status.json` with no `host`
  goes through `v0.1.0`'s rule unchanged (§3 checks 4, 5);
- **the package concludes no more than the prompt's §2.4 allows**: `foreign` is "not judged here",
  and only an earlier boot on this host is `stale` without `kill -0` (§3 check 5);
- **no raw hardware identifier reaches a file**, the log included (§3 checks 4, 7);
- **the Linux readers are exercised only in CI**, which runs only after a push (§3 check 9; §4).

**What moves on purpose:** `runregistrykit/__init__.py`, `stores.py` (`_describe_running` only),
`__main__.py` (`list` only); new `runregistrykit/tests/test_host.py` and `test_host_stores.py`; one
line of `.github/workflows/tests.yml` (the core job's test list); the new log
`prompts/interrupted-runs/logs/01-the-host.md`; the board; `docs/OPEN_ISSUES.md`;
`prompts/INDEX.md`. **Nothing else**: not `pyproject.toml`, `README.md`, `PROVENANCE.md`,
`CLAUDE.md`, `docs/adoption/`, any other test module, the prompt, the campaign README or
`orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The suite is slow today.** `Ran 276 tests in 307.014s`, OK, at `1fd8e1c` with `TMPDIR` in the
   scratchpad, against about 95 s at extraction 08. Run it in the foreground with a timeout of at
   least 600 s, write its output to a file, and grep the verdict from the file. Record the time
   seen. A slow run is not a stop; a failing one is.
2. **The core run of §3.2.** "A fresh scratch venv with the package installed without `[stores]`"
   reads as: `uv venv -p /opt/local/bin/python3.12 <scratch>/core`, then `uv pip install --offline
   -p <scratch>/core/bin/python -e <this checkout>`, with `TMPDIR` in the scratchpad. The
   orchestrator built exactly that offline at `1fd8e1c`, with none of `datastorekit`, `ray` and
   `sqlalchemy` findable (`pyproject.toml`'s core `dependencies = []`). This is the one install
   allowed, and nothing is installed into `venv/`. The venv is removed afterwards.
3. **The hand run of §3.4 and the public repository.** The repository is public, and
   `platform.node()` on this machine is a DNS name the campus network assigned. For the hand run,
   set `RUNREGISTRYKIT_HOST_NAME=scratch-host`, so the log shows that name and not the machine's.
   Show the `id` digest; never show the raw identity, nor the boot UUID (`boot: <36-char uuid>` is
   enough). The same holds for any output pasted into the log.
4. **The Linux readers.** CI's `ubuntu-24.04` runner is where they first run. The test of §2.7's
   first bullet expects a 16-hex `id` and a non-empty `boot` on Linux. If CI shows either absent,
   that is a finding for the review, not a reason to weaken the test now. Locally, the macOS branch
   runs, and the Linux branch is skipped with its reason.
5. **`gethostuuid` through `ctypes`.** As the orchestrator called it at writing:
   `libc = ctypes.CDLL(ctypes.util.find_library("c"))`; a buffer `(ctypes.c_ubyte * 16)()`; a
   `timespec` structure of two `c_long`s, `(1, 0)`; `libc.gethostuuid(buf, ctypes.byref(ts))`
   returned 0; `str(uuid.UUID(bytes=bytes(buf)))` equalled `ioreg`'s `IOPlatformUUID` lowercased.
   `sysctlbyname(b"kern.bootsessionuuid", buf, byref(size), None, 0)` with a 64-byte buffer
   returned 0 and size 37 (36 characters and a NUL). Set `argtypes` and `restype` explicitly.
6. **`test_public_names.py` is not edited** (the prompt's §2.6): it derives the expected names from
   the source. Its run after the change is the check that `this_host` is declared.
7. **`black`.** `black --check runregistrykit docs` reports 28 files at `1fd8e1c`; after 01 it is
   30.
8. **The board has no Orchestrator notes line yet.** The agent does not add one; the review does
   (§4).

**The facts, checked by the orchestrator on 2026-10-16 at `1fd8e1c`.** Pass them on.
- **In-repository state.** `main` at `1fd8e1c`, clean (`origin/main` behind, unpushed since
  `79015a7`). `git status --short --ignored` shows `prompts/.DS_Store`, `runregistrykit.egg-info/`,
  `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/` and `venv/`. This checkout is
  the only worktree. `git diff --stat 79015a7 HEAD -- runregistrykit pyproject.toml .github` is
  empty.
- **Tools.** `venv/`: Python 3.12.15, `black` 25.1.0. `uv` 0.12.20 at `/opt/local/bin/uv`;
  `/opt/local/bin/python3.12` (3.12.15) and `python3.13`. No Ray process before or after the suite;
  `RAY_ADDRESS` unset.
- **The package lines the prompt cites** were read at `1fd8e1c`: `__all__` `__init__.py:76-97` (20
  names); `liveness` `:294`, its early returns `:301-306`, pid and heartbeat `:307-311`;
  `Run._update` `:398`; `begin` `:604`, its manifest `:707-725`, its first status `:728-734`;
  `list_runs` `:749`, its status read `:771`; `_running_runs_naming` `stores.py:998`, its filter
  `:1017`; `_describe_running` `:1021`; `list` `__main__.py:528-570`; the core job's test list
  `.github/workflows/tests.yml:89`.
- **The issue index** counts 10. After 01 it is 9.

**What the review exists to establish.**
- **(H1) The files.** Only §0's list changes.
- **(H2) What is written.** The manifest's `host` and the first status's `host`, with their keys
  exactly; `host` present with `null` values when a reader fails; `host` carried by every later
  write.
- **(H3) The judgement.** §2.4's order, each step tested; a record with no `host` judged as
  `v0.1.0` judged it; `foreign` never judged by pid.
- **(H4) The reporting.** `list`'s markers, counts and stderr lines; the store refusals naming the
  host.
- **(H5) No raw identifier** in any file the package writes, or in the log.
- **(H6) The tests bite.** (m1)–(m8).
- **(H7) The records.** The log, the board, the index and the campaign line.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff, the commands
  and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`, with `TMPDIR` set to a
  directory in the agent's scratch subdirectory, as correction 1.
- **Mutation diffs.** Recorded in the log as unified diffs with repository paths, checked **as
  recorded** with `git apply --check` and `-R --check`, in `bash`, in a scratch clone. None is
  committed. After each, `git status` here must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-01/`), never
  `/tmp`, and sets `TMPDIR` inside it for every command. **No scratch file goes under
  `runregistrykit/` or `docs/`.**
- **Ray.** The agent starts no Ray, and records `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` before and after every suite run.
- **GitHub.** Nothing is pushed, no tag is made, no workflow is dispatched.
- **Stop conditions are real** (the prompt's §5). A stop goes to the user through the orchestrator,
  and the agent resumes with `SendMessage`. A defect found elsewhere in the package is opened on the
  board, never fixed.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone.
2. **The prompt's gate**, and the suite: 276 in `venv/`, its time recorded (correction 1).
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 10 now, 9 after unless the work opens one. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` and
  `CLAUDE.md`;
- `HEAD`, the suite count and time, and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-the-host.md` (the directory is new), in README
  §5.1's form, with the prompt's §4.3 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It installs only the core venv of correction 2, sets `TMPDIR` for every command, and starts no
  Ray.**
- **It writes no raw identifier and no machine name anywhere** (correction 3).
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **Scope (H1).** `git show --stat <commit>` touches only §0's list. `git diff <note's commit>
   <commit> -- pyproject.toml README.md PROVENANCE.md CLAUDE.md docs/adoption
   prompts/interrupted-runs/README.md prompts/interrupted-runs/01-the-host.md
   prompts/interrupted-runs/orchestrator` is empty, and the workflow's diff is the one line.
   `runregistrykit/tests/` gains exactly the two new modules, and no existing test module changes.
2. **The suite, re-run by the orchestrator.** In `venv/` at the commit: `Ran 276 + N tests … OK`,
   N as the log's, per module by the loader. `black --check runregistrykit docs`: 30 files. `git
   status --short --ignored` the same before and after but for `__pycache__/`; no `var/`; no Ray
   process. The core run of correction 2, repeated by the orchestrator in its own scratch venv,
   passes the three modules with the store layer's dependencies absent.
3. **The old tests stand.** `git diff <note's commit> <commit> -- runregistrykit/tests` shows only
   new files. Every test at the note's commit passes at the agent's commit (check 2 covers it), with
   its assertion untouched.
4. **What is written (H2, H5), by the orchestrator's own run.** In a scratch client root, with
   `RUNREGISTRYKIT_HOST_NAME` set: `begin`, `heartbeat`, `heartbeat(pid=<another live pid>)`,
   `finish`. Read the manifest's and the status's `host` after each step: keys as the prompt's
   §2.3, `host` kept throughout. Then grep every file in the run directory for the raw identity,
   which the orchestrator reads itself (correction 5's calls) and does not paste anywhere: no hit.
   Then patch the readers to fail, `begin` again, and see `host` with `null` values.
5. **The judgement (H3), by hand records.** The orchestrator writes `status.json` payloads into a
   scratch runs root and calls `liveness` and `list_runs` on them:
   - **no `host`**, this process's pid, fresh heartbeat → `alive`; a reaped pid → `stale`; an old
     heartbeat → `stale`, each exactly as `liveness` at `79015a7` gives for the same payload. Run
     the same payloads through `git show 79015a7:runregistrykit/__init__.py`'s `liveness` in a
     scratch copy and compare;
   - **another host's id**, live pid and fresh heartbeat → `foreign`; dead pid → `foreign`;
     terminal → `finished`;
   - **this host's id, another boot**, live pid → `stale`;
   - **this host and boot** → as before;
   - **an id when this machine reads none** (readers patched) → `foreign`.

   Any other answer is a finding.
6. **The reporting (H4).** `python -m runregistrykit list --root <that runs root>`: `??` on the
   foreign rows, `!!` on the stale, the count of records with no host, the foreign line and the
   amended stale line on stderr, and every existing column kept. Then a registered store named by a
   foreign `running` run: `store fingerprint`, `store copy` and `store retire --dry-run` each exit 1
   naming "another host" and the host, with the sidecar's SHA-256 unchanged.
7. **The log (H5, H7).** Every section of README §5.1 and the prompt's §4.3 additions; the
   deviations classified, corrections 1–8 among them; the suite before and after; the core run; the
   hand run with `scratch-host` and no raw identity or boot UUID; no machine name of this Mac
   anywhere (`grep` the log for `platform.node()`'s value, which the orchestrator reads itself).
8. **The mutations (H6).** (m1)–(m8) extracted from the log by a script and replayed in `bash` in a
   `git clone` of the commit (`--check`, apply, the suite or the named module, `-R --check`,
   reverse), each failing as the log says. Then the orchestrator's own, each in the clone:
   - (o1) the digest's prefix bytes dropped (`sha256(raw)`): a test must fail, or the prefix is
     unpinned. Open it on the board if none does, not a stop;
   - (o2) `list_runs` reading `this_host()` per entry, not once: no test need fail. Record the
     timing on a runs root of 200 entries, and say whether it matters;
   - (o3) step 3 of §2.4 made to fire when either boot is `None`: a test must fail.
9. **The records (H7) and CI.** The board: the header, 01's row ("this commit", 276 → 276 + N), H1
   ✅, the entry moved to §4 with its four answers and their tests, the other four entries' "Package
   lines (01, …)" notes. `docs/OPEN_ISSUES.md`: 9 by counting, the row gone, the date.
   `prompts/INDEX.md`: the campaign's line. **CI is read after the push (§4)**: all three jobs
   green, and in the `core` and `suite` jobs the `test_host` Linux reader test **ran and passed**,
   not skipped (`gh run view --log` grepped for the test's name). Until then the review's verdict
   says "pending CI".

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph (*At dispatch*,
  *The checks*, verdict), and add the board's **Orchestrator notes** line, with this note marked
  "used for 01". Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the campaign README's §2 row and in
    `prompts/INDEX.md`;
  - "reviewed" for 01 in the board's header and row, the README's §2 status column and
    `prompts/INDEX.md`.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Ask the user whether to push `main`.** CI runs the Linux readers only after a push. Once it has
  run, read it (check 9) and record the result on the board in a records commit of its own.
- **Report to the user:**
  - what landed, 276 → 276 + N, and the issue closed;
  - what is now written, with the orchestrator's hand-run `host` (digest shown, raw identity not);
  - the old-record comparison against `79015a7`'s `liveness`;
  - the mutations, the agent's and the orchestrator's;
  - CI, or that it is pending a push;
  - that 02 is next, and is written only after this review.
