# interrupted-runs campaign — implementation state

**Last updated:** 2026-10-17 · **Status: OPEN — 01 landed (`387c58f`) and reviewed, CI green
(run `38911075984`); 02 landed (`2bf9c72`) and reviewed, CI green
(run `39049728089`); 02b landed (`2959b78`) and reviewed, CI green (run
`39060913296`), closing the two issues 02's
review opened; 02c written, not run, for the one 02b's review opened. L1–L4 (the machine decision)
taken by the user on 2026-10-16, as recommended; L5 taken 2026-10-17, refined, and amended the same
day; L11 taken 2026-10-17 for 02c, as recommended (README §6.2).** Holds the five issues that bear on a
long job that may be interrupted, assigned here from the `inherited-issues` board on 2026-10-16:
three open (§3), two resolved (§4), by 01 and 02. Two more, found by 02's review, were resolved by
02b (§4). One, found by 02b's review, is open in §3, assigned to 02c.

**Campaign:** [`README.md`](README.md) ·
**Evidence:** SGK's `prompts/handover/runregistrykit-stale-run-brief.md` (SGK `79434bf`) and the
`inherited-issues` board ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.3

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

Code is cited as each entry says: at `caad864` for the two entries opened on the inherited board's
first day, at `79015a7` for the three from SGK's stale-run brief. No file under `runregistrykit/`
and not `pyproject.toml` differs between `v0.1.0`, `caad864` and `79015a7`, so every line is the
tag's.

### Decisions

| | Needed by | State |
|---|---|---|
| **L1** what identifies a machine | 01 | **taken** 2026-10-16: (a); the user picks a machine per job, often a Mac Studio, so the package records an identity wherever the platform offers one |
| **L2** where the host is recorded | 01 | **taken** 2026-10-16: (a) |
| **L3** what identifies a boot | 01 | **taken** 2026-10-16: (a) |
| **L4** what `liveness` and `list` say | 01 | **taken** 2026-10-16: (a) |
| **L5** how `status.json` is written | 02, 02b | **taken** 2026-10-17: (a), refined: superseded per `status.json` in the process, not per `Run`; the later write keeps an in-flight write's fields; an `RLock`. **Amended** 2026-10-17 after 02's review: only in-flight writes newer than the landed base are re-applied, and the record of what landed is never lowered (02b) |
| **L6** an unreadable status in the in-use check | 03 | put, recommended (a) |
| **L7** what `end` writes | 04 | put, recommended (a) |
| **L8** what `end` checks | 04 | put, recommended (a) |
| **L9** what `begin` refuses | 05 | put, recommended (a) |
| **L10** the release | 06 | put, recommended (a) |
| **L11** the `with` point at Python 3.14 | 02c | **taken** 2026-10-17: (a); the window recorded in `_update`'s docstring, the issue narrowed to it, not fixed |

## 1. Prompts

| # | Prompt | Model | Status | Commit | Suite |
|---|---|---|---|---|---|
| 01 | [`01-the-host.md`](01-the-host.md) | Opus | **landed and reviewed** 2026-10-16 ([log](logs/01-the-host.md)); CI green, run `38911075984` | `387c58f` | 276 → 307 |
| 02 | [`02-status-writes.md`](02-status-writes.md) | Opus | **landed and reviewed** 2026-10-17 ([log](logs/02-status-writes.md)); CI green, run `39049728089` | `2bf9c72` | 307 → 322 |
| 02b | [`02b-the-writers-bookkeeping.md`](02b-the-writers-bookkeeping.md) | Opus | **landed and reviewed** 2026-10-17 ([log](logs/02b-the-writers-bookkeeping.md)); CI green, run `39060913296`; one issue opened by the review | `2959b78` | 322 → 328 |
| 02c | [`02c-the-writers-lock.md`](02c-the-writers-lock.md) | Opus | written 2026-10-17, not run; L11 taken (a) | — | |
| 03 | `03-an-unreadable-status-is-in-use.md` | Sonnet | not written | — | |
| 04 | `04-end-a-run.md` | Opus | not written | — | |
| 05 | `05-begin-refuses-a-second-writer.md` | Sonnet | not written | — | |
| 06 | `06-release-v0.2.0.md` | Opus | not written | — | |
| 07 | `07-verification-and-close-out.md` | Opus | not written | — | |

The suite is 276 at `79015a7` (extraction 08's count; no file under `runregistrykit/` changed
from then until 01), 307 after 01, 322 after 02, and 328 after 02b.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`8023e14`), used
for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`b52cc01`), used for 02;
[`orchestrator/prompt-02b.md`](orchestrator/prompt-02b.md) (`201e507`), used for 02b.

**Orchestrator review of prompt 01 (2026-10-16).** Dispatched from `8023e14` to one Opus subagent,
with the note's §0 as a copy in the session scratchpad: its facts, its eight corrections and
readings of the prompt, and its conventions. Reviewed against its commit `387c58f`, with nothing
landed after it. **Every check of the note's §3 passed**, and acceptance 1–3 are met; the CI half
of check 9 waits for a push. No stop condition fired, and no issue is opened.

*At dispatch.* The note's gate held at `8023e14`: `main`, clean, nothing staged, this checkout the
only worktree; `git diff --stat 79015a7 HEAD -- runregistrykit pyproject.toml .github` empty;
`Ran 276 tests in 155.000s`, OK, with `TMPDIR` in the scratchpad; no Ray process, `RAY_ADDRESS`
unset; the index at 10.

*The checks.*
1. **Scope (H1).** `387c58f` touches §0's ten files and no others. The diff from `8023e14` of
   `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption`, the campaign
   README, the prompt and `orchestrator/` is empty. The workflow's diff is the core job's one line,
   now naming `test_host`. `runregistrykit/tests/` gains exactly `test_host.py` and
   `test_host_stores.py`; `stores.py` changes in `_describe_running` only, `__main__.py` in `list`
   and its helper `_host` only.
2. **The suite, re-run.** `Ran 307 tests in 132.606s`, `OK (skipped=1)`, in `venv/` at
   `387c58f`. By the loader, per module, the log's table exactly: `test_host` 28,
   `test_host_stores` 3, every other module as at `8023e14`. The skip is
   `test_the_readers_on_linux`. `black --check runregistrykit docs`: 30 files. `git status --short
   --ignored` the same before and after; no `var/`; no Ray process before or after. The core run of
   correction 2, in the orchestrator's own scratch venv (`uv`, offline, editable, no `[stores]`):
   `datastorekit`, `ray` and `sqlalchemy` not findable, `Ran 65 tests in 7.962s`, `OK
   (skipped=1)`; the venv removed.
3. **The old tests stand.** `git diff 8023e14 387c58f -- runregistrykit/tests` adds two files and
   changes none; check 2 runs every older test, passing.
4. **What is written (H2, H5).** In a scratch client root with `RUNREGISTRYKIT_HOST_NAME=scratch-host`:
   `begin`, `heartbeat`, `heartbeat(pid=<a live child>)`, `finish("done")`. The manifest's `host`
   is `{id, machine, name, python, release, system}` and the status's `{boot, id}`, exactly; the
   status's `host` is the same after every step, and the pid moves to the child's. `id` is
   `8d2b247824882486`, equal to the orchestrator's own digest of `gethostuuid` read by correction
   5's calls; `boot` equals `kern.bootsessionuuid` read the same way (a 36-character UUID, not
   shown). Neither the raw identity (dashed or not, either case) nor `platform.node()` is in any
   file of the run directory; the digest is in both. With the readers patched to fail, `begin` and
   a `heartbeat` write `host` with `null` values, `machine`, `system`, `release` and `python` kept.
5. **The judgement (H3), by hand records.** Five payloads with no `host` (this shell's pid with a
   fresh heartbeat; a reaped pid; a two-hour-old heartbeat; `done`; `paused`), run through
   `liveness` at `387c58f` and through `79015a7`'s, extracted with `git archive` into the
   scratchpad: `alive`, `stale`, `stale`, `finished`, `unknown`, the same from both. At `387c58f`:
   `host.id` null, or `host` a string, → judged here (`alive`); another host's id with a live pid
   and a fresh heartbeat, a dead pid, or an old heartbeat → `foreign`, `done` → `finished`; with
   `pid_alive` patched to raise, a foreign record and one from another boot still answer, so the
   pid is not tested; this host from another boot with a live pid → `stale`; this host and boot →
   `alive`, `stale` for a dead pid or an old heartbeat; this host with a null boot → `alive`; with
   the machine reader patched to `None`, a record carrying any id, this machine's own included, →
   `foreign`, and one with no `host` → `alive`. `list_runs` over the same records in a scratch runs
   root agrees with `liveness` on every entry, and gives `host`, `host_id` and `host_recorded` as
   §2.4 says (false for no `host` and for a `host` that is not a dict).
6. **The reporting (H4).** `python -m runregistrykit list --root <that root>`: `??` on the three
   foreign rows, each `on far-host · `; `!!` on every stale row; "2 finished, 3 foreign, 10 stale,
   1 unknown; 6 with no host recorded."; the stale line with "or this machine has rebooted since";
   the foreign line naming `far-host`; every column kept. A registered store named by a foreign
   `running` run, built with `test_host_stores`' own fixture: `store fingerprint`, `store copy` and
   `store retire --dry-run` each exit 1 with "is running on another host, far-host (pid N, not
   tested here)", and the sidecar's SHA-256 is unchanged by each.
7. **The log (H5, H7).** Every section of README §5.1 and the prompt's §4.3 additions; sixteen
   deviations, each classified, corrections 1–8 among them (none UNINTENDED DRIFT); the suite
   before and after; the core run; the hand run with `scratch-host`, the id digest and
   `<36-char uuid>`. The commit, its message and the log hold neither the raw identity nor the boot
   UUID (dashed or not) nor `platform.node()` nor its first label, by the orchestrator's own search.
   **Residue fixed here:** the log and the board cited `runregistrykit/__init__.py` at `387c58f`
   two lines short from `Run.status` on (`_update` `:593` for `:595`, `begin` `:799` for `:801`,
   `list_runs` `:960` for `:962`, and so on); the citations before `:490`, and every one in
   `stores.py` and `__main__.py`, were right.
8. **The mutations (H6).** (m1)–(m8) extracted from the log by a script and replayed in `bash` in a
   `git clone` of `387c58f`, with `PYTHONPATH` on the clone so that child processes run it:
   `--check`, apply, `test_host` and `test_host_stores` (and, for (m5), `test_run_registry` and the
   four store modules the log names), `-R --check`, reverse, the clone clean. Each failed exactly
   as the log says, counts included ((m1) 12; (m2) 2; (m3) 2; (m4) 7 and 6 errors; (m5) 17 and 9
   errors; (m6) 20; (m7) 13; (m8) 2). The orchestrator's own, in a second clone:
   - (o1) the digest's prefix dropped: 20 failures, `test_the_id_is_a_digest_of_the_raw_identity`
     among them, so the prefix is pinned;
   - (o2) `list_runs` reading `this_host()` per entry: caught, by
     `test_list_runs_reads_this_host_once`. Timed on 200 entries: 68 ms with the host read once,
     119 ms per entry. It would not matter to a person reading `list`;
   - (o3) step 3 firing when either boot is null: caught, by
     `test_this_host_and_this_boot_are_judged_by_pid_and_heartbeat`.

   No mutation, suite or core output holds the raw identity or `platform.node()`.
9. **The records (H7) and CI.** The board's header, 01's row (276 → 307), H1 ✅, the entry in §4
   with its four answers and the tests that pin each, and the other four entries' "Package lines"
   notes are in. `docs/OPEN_ISSUES.md` counts 9 by its rows, the row gone, the date 2026-10-16.
   `prompts/INDEX.md`'s line is updated. **CI is not read yet:** nothing is pushed, and the Linux
   readers, `test_the_readers_on_linux` above all, run first on CI's `ubuntu-24.04` runners.

**Verdict:** 01 is accepted, **pending CI**: all three jobs green, and `test_the_readers_on_linux`
run and passed, not skipped, in the `core` and `suite` jobs, read from the run's log after the
user pushes `main`.

*CI (2026-10-16).* The user said yes, and `main` was pushed, `79015a7..5d71a6b`. Run
`38911075984` (`tests`, on the push of `5d71a6b`) passed all three jobs, each on `ubuntu-24.04`:
`core (no store layer)` ran `test_run_registry`, `test_public_names` and `test_host` by name, `Ran
65 tests in 1.757s`, `OK (skipped=1)`; `suite (low)` `Ran 307 tests in 47.987s` and `suite (high)`
`Ran 307 tests in 36.036s`, each `OK (skipped=1)`. The workflow runs `unittest` without `-v`, so
the log names no test, and the note's grep for `test_the_readers_on_linux` finds nothing. The
result follows from the counts. `test_the_readers_on_macos` is skipped unless the platform is
Darwin, so on Linux it is the one skip. So `test_the_readers_on_linux` ran and passed in all three
jobs: a 16-hex `id`, a non-empty `boot`, the same on two calls, and a raw identity of 32 lowercase
hex characters whose digest is the `id`. `test_no_raw_identity_reaches_a_file`, which skips when
the platform offers no identity, did not skip, so it ran against the Linux identity too. **01's
review is complete; check 9 holds.**

**Orchestrator review of prompt 02 (2026-10-17).** Dispatched from `b52cc01` to one Opus subagent,
with the note's §0 as a copy in the session scratchpad: its facts, its eleven corrections and
readings of the prompt, and its conventions. Reviewed against its commit `2bf9c72`, with nothing
landed after it. **Every check of the note's §3 passed**, and acceptance 1–3 are met; the CI half
of check 9 waits for a push. No stop condition fired. **Two issues are opened** from checks 6 and 8
(below), neither a defect in what the prompt's tests or acceptance ask.

*At dispatch.* The note's gate held at `b52cc01`: `main`, clean, nothing staged, this checkout the
only worktree; `git diff --stat 387c58f HEAD -- runregistrykit pyproject.toml .github` empty; `Ran
307 tests in 99.007s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad; no Ray process,
`RAY_ADDRESS` unset; the index at 9.

*The checks.*
1. **Scope (W1).** `2bf9c72` touches §0's seven files and no others. The diff from `b52cc01` of
   `stores.py`, `__main__.py`, `client.py`, `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `CLAUDE.md`, `docs/adoption`, the campaign README, the prompt and `orchestrator/` is empty. The
   workflow's diff is the core job's one line, now naming `test_status_writes`.
   `runregistrykit/tests/` gains exactly `test_status_writes.py`. In `__init__.py` the diff is
   `import copy`, `itertools` and `threading`, the writer's section after `write_json_atomic`
   (`:259-349`), and `_update`'s body and docstring; `write_json_atomic` is byte for byte as it was.
   `git grep -n 'signal'` in the package finds `finish`'s docstring only (`:755`); no `import
   signal`, no `tempfile`.
2. **The suite, re-run.** `Ran 322 tests in 111.343s`, `OK (skipped=1)`, in `venv/` at `2bf9c72`.
   By the loader, per module, the log's table exactly: `test_status_writes` 15, every other module
   as at `b52cc01`. `black --check runregistrykit docs`: 31 files. `git status --short --ignored`
   the same before and after; no `var/`; no Ray process; no child left. The core run of correction
   2, in the orchestrator's own scratch venv (`uv`, offline, editable, no `[stores]`):
   `datastorekit`, `ray` and `sqlalchemy` not findable, `Ran 80 tests in 13.801s`, `OK
   (skipped=1)`; the venv removed.
3. **The plain write (W2).** In a scratch client root, the same calls (`begin`, `heartbeat`,
   `heartbeat(pid=…)`, `record`, `finish`, and a heartbeat under umask `0o077`) made through
   `34afe6d`'s package (by `git archive`; its package is `387c58f`'s) and through `2bf9c72`'s: the
   same keys after every call, the same number of reads of `status.json` (one; two for `record`, in
   both), one `os.replace` per call in both, the same modes (`0o644`, then `0o600`). The source of
   each replace was `status.json.tmp` before and `status.json.<pid>-…` after. Nothing left behind.
   The old record's keys are pinned by `TestAnOldRecord`, run in check 2.
4. **`write_json_atomic` and the sidecars.** Unchanged (check 1); pinned by
   `test_write_json_atomic_still_replaces_from_its_tmp_name` and the sidecar tests that name
   `<sidecar>.tmp`, all passing in check 2, and caught by (m10) in check 8.
5. **The re-entered write (W3), by the orchestrator's own probe.** A child process per case, a real
   `SIGTERM` sent by the child to itself from inside a heartbeat's write (`units_done=7`), at four
   points (half the payload written, all of it, inside `os.replace` before and after the real
   replace), the handler calling `finish("killed", exit_code=143)` and then raising, returning or
   ending the process: twelve cases. **Against `2bf9c72`, all twelve parse, `killed`, 143,
   `units_done` 7, the heartbeat's stage kept**, the heartbeat raising `SystemExit` or returning;
   nothing left behind but, where the process ends before the heartbeat's replace, one
   `status.json.<unique>.tmp`, the documented leftover. Against `34afe6d` the same probe reproduces
   the prompt's "fixed (today)" rows: raising, half written, `killed` with `exit_code` null and
   `units_done` 0; raising, all written, `running`; returning, `running` and a `FileNotFoundError`
   from the heartbeat (`killed` but the same error before the replace); ending the process,
   `killed`, 143, `units_done` 0.
6. **The edges (W3, W4).**
   - **(P3) and (P4) by a real signal**: in check 5's twelve.
   - **Two processes**: a launcher's `Run(path).heartbeat(pid=…)` from another process lands and is
     read by the next write here; a heartbeat in a child after the parent's `finish` keeps
     `killed`, 143.
   - **A worker thread and a handler on the main thread**: a thread heartbeating in a loop, the main
     thread sending itself `SIGTERM` twenty times, the handler calling `finish`: the thread joined,
     `killed`, 143, nothing left behind.
   - **Correction 6's case, measured**, in one process: a `heartbeat(units_done=7, stage="A")`
     whose write makes a handler's `heartbeat(stage="B")`, which lands, and then a handler's
     `finish("killed", 143)` lands `stage` `A`. **Its state variant also reproduces**, as the log's
     observation 1 says: a `finish("done", exit_code=0)` whose write makes a handler's
     `finish("killed", exit_code=143)` and then a handler's `heartbeat` ends `done`, 0, so the
     handler's terminal state is replaced by the interrupted one's. With one handler write
     (`finish("killed")` alone) it ends `killed`, as it should. The note asked that a lost state go
     to the user: it does, and it is opened as
     `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]`. No state goes back to
     `running` by it, and the prompt's tests and acceptance stand.
7. **The log (W6).** Every section of README §5.1 and the prompt's §4.3 additions; twenty-four
   deviations, each classified, corrections 1–11 among them (none UNINTENDED DRIFT); the suite
   before and after; the core run; the §3.4 table; every mutation as a diff; the documented
   leftover. Every line citation in the log and in the board's notes checked by `grep -n` at
   `2bf9c72`: right. **Residue fixed here:** "this commit" → `2bf9c72`. **Residue not fixed:**
   `_update`'s docstring has one line of 121 characters (`__init__.py:696`), which `black` does not
   reflow; left, so that the package is not changed after its review.
8. **The mutations (W5).** (m1)–(m10) extracted from the log by a script and replayed in `bash` in a
   `git clone` of `2bf9c72`, with `PYTHONPATH` on the clone: `--check`, apply, `test_status_writes`
   with `test_run_registry` (for (m10), `test_status_writes`, `test_store_copy_move` and
   `test_store_retire`; for (m9), the three real-signal tests by name), `-R --check`, reverse, the
   clone clean. Each failed exactly as the log says, the same tests and subtests ((m1) 13 and 1
   error; (m2) 2; (m3) 3; (m4) 15; (m5) 1; (m6) 3; (m7) 5; (m8) 1; (m9) 3, each child timing out at
   60 s, `Ran 3 tests in 180.431s`; (m10) 6 and 3 errors); no child left. The orchestrator's own,
   in the same clone:
   - (o1) the file opened with `open(name, "w")` instead of `O_EXCL`: no test fails, as expected.
     The name is the write's own (pid, counter and random hex), so two writes cannot share one, and
     `O_EXCL` only makes that certain;
   - (o2) step 6's record made after a put-back too (its `return` removed), so the record moves
     back to the overtaken write's number and payload: **no test fails**. Measured, it matters:
     after a put-back, a later heartbeat re-entered by a handler's heartbeat composes from the
     stale `running` payload and lands `running` over `killed`; at `2bf9c72` it stays `killed`. The
     shipped code is right here, but unpinned, and the same backward move has a one-statement window
     in it (between the check at `:318` and the record at `:321`). Opened as
     `[02-the-landed-record-is-unpinned-and-can-move-backwards]`;
   - (o3) the `RLock` made one per `Run` object: no test fails. The threads test uses one `Run`; two
     `Run` objects for one directory on two threads would update the shared bookkeeping unlocked.
     Recorded, not opened: the prompt's §2.3 asks for one writer per path, which `2bf9c72` is.
9. **The records (W6) and CI.** The board's header, 02's row (307 → 322), W1 ✅, the entry in §4
   with its five answers and the tests that pin each, the other three entries' "Package lines (02,
   …)" notes, and the unreadable-status entry's sentence are in. `docs/OPEN_ISSUES.md` counted 8 by
   its rows at `2bf9c72`, the row gone, the date. `prompts/INDEX.md`'s line is updated. **CI is not
   read yet:** nothing is pushed, and `test_status_writes` first runs on Linux in CI, the real-signal
   children above all.

The agent's other observations are recorded in its log and not opened: a fork made while another
thread holds `_STATUS_LOCK` leaves the child's lock held (the standard hazard of a lock across a
fork); a handler that raises inside `_write_status`'s `finally` leaves an in-flight entry for the
life of the process; the bookkeeping lasts the process; and the leftover's name, for 04 and 06.

**Verdict:** 02 is accepted, **pending CI**: all three jobs green, the core job's count 80, read
from the run's log after the user pushes `main`. The two issues opened here are put to the user.

*CI (2026-10-17).* The user said yes, and `main` was pushed, `c2911d3..a38022f`. Run
`39049728089` (`tests`, on the push of `a38022f`) passed all three jobs, each on `ubuntu-24.04`:
`core (no store layer)` ran `test_run_registry`, `test_public_names`, `test_host` and
`test_status_writes` by name, `Ran 80 tests in 2.905s`, `OK (skipped=1)`; `suite (low)` `Ran 322
tests in 28.855s` and `suite (high)` `Ran 322 tests in 40.277s`, each `OK (skipped=1)`. The one
skip in each is `test_host`'s macOS readers, as at 01; `test_status_writes` has no skip, so all 15
of its tests ran and passed on Linux in all three jobs, the three real-signal children among them.
**02's review is complete; check 9 holds.**

**Orchestrator review of prompt 02b (2026-10-17).** Dispatched from `201e507` to one Opus
subagent, with the note's §0 as a copy in the session scratchpad: its facts, its fifteen
corrections and readings of the prompt, and its conventions. The agent stopped once, before
committing, on the prompt's §5: (m3), the early `return` after a put-back removed, was caught by
no test. The user took (A) the same day: record (m3) as a mutant that changes nothing under the
by-number record, keep the `return`, and add (m3′), the put-back's re-landing call removed. Reviewed
against its commit `2959b78`, with nothing landed after it. **Every check of the note's §3 passed**
on 3.12.15, and acceptance 1–3 are met; the CI half of check 9 waits for a push. **One issue is
opened**, from a measurement on 3.13.16 that the note's check 5 led to (below): a regression on a
supported Python, not a failure of what the prompt's tests or acceptance ask.

*At dispatch.* The note's gate held at `201e507`: `main`, clean, nothing staged, this checkout the
only worktree; `git diff --stat 2bf9c72 HEAD -- runregistrykit pyproject.toml .github` empty; `Ran
322 tests in 134.049s`, `OK (skipped=1)`, with `TMPDIR` in the scratchpad; no Ray process,
`RAY_ADDRESS` unset; the index at 10; `var/ledger.jsonl` (left by 02's review) `471d0859…`.

*The checks.*
1. **Scope (B1).** `2959b78` touches §0's six files and no others; the diff from `201e507` of
   `stores.py`, `__main__.py`, `client.py`, `pyproject.toml`, `.github`, `README.md`,
   `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption`, the campaign README, the prompt and
   `orchestrator/` is empty. `test_status_writes.py` gains lines and loses none. `__init__.py`
   changes in six hunks, all in the writer section (`:259-380`) and `_update`'s docstring;
   `write_json_atomic` is byte for byte as it was. No new import in the package; `git grep -n
   'signal'` finds `finish`'s docstring only (`:796`).
2. **The suite, re-run.** `Ran 328 tests in 120.485s`, `OK (skipped=1)`, in `venv/` at `2959b78`;
   `test_status_writes` alone `Ran 21 tests in 18.846s`, OK. `git status --short --ignored` the same
   before and after; `var/ledger.jsonl` unchanged; no Ray process; no child left. The core run of
   correction 2, in the orchestrator's own scratch venv (`uv`, offline, editable, no `[stores]`):
   `datastorekit`, `ray` and `sqlalchemy` not findable, `Ran 86 tests in 21.466s`, `OK
   (skipped=1)`; the venv removed.
3. **The plain write (B2).** The orchestrator's probe, through `2bf9c72`'s package (by `git
   archive`) and `2959b78`'s: `heartbeat`, `heartbeat(pid=…)`, `record`, a heartbeat under umask
   `0o077`, `finish`. The output of the two is identical: the same keys, one read of `status.json`
   (two for `record`), one `os.replace` from `status.json.<unique>.tmp` per call, modes `0o644` and
   `0o600`, nothing left.
4. **The merge (B3).** In one process, `json.dump` patched to fire once, the handler's writes made
   from inside it. `2959b78` / `2bf9c72`: a heartbeat `stage=A` with a handler's `heartbeat(stage=B)`
   then `finish("killed")`: `killed`, `stage` **B** / `stage` A; a `finish("done")` with a handler's
   `finish("killed")` then `heartbeat`: **`killed`, 143** / `done`, 0; with `finish("killed")` alone:
   `killed` / `killed`; a heartbeat (`units_done` 7) discarded by a handler's `heartbeat(stage=B)`:
   units 7 kept / kept. **Three handler writes**, which no test names (`heartbeat(stage=B)`,
   `heartbeat(stage=C)`, `finish("killed")`): `killed`, `stage` **C** / `stage` A. And a
   `finish("done")` with `heartbeat(B)`, `finish("killed")`, `heartbeat(C)`: `killed`, C / `done`.
5. **The record (B4) and the sweep (B5).**
   - *By reading.* A key is stored only by a write whose check found no higher one, and a prune
     removes only keys below the pruning write's own number, so the highest key can be neither
     lowered by a store nor removed by a prune, whatever instruction a handler interrupts; a handler
     landing a higher key between the check and the store keeps it. `_newest_landed` reads `max` and
     then the payload, and re-reads if the key went. Payloads stored are deep copies of dicts, never
     `None`.
   - *The sweep's reach.* `sweep_in_this_process` run by the orchestrator's own script on
     `2959b78`, both sweeps, all eight modes: 323 instructions per write, in `_write_status` 104,
     `_land_status` 118, `_newest_landed` 78, `_status_temporary_name` 23 (`_remove_quietly` runs
     only on an error); 0 wrong in every mode; the finish sweep accepts 24 points in each returning
     mode. Afterwards no `sys.monitoring` tool id is in use and every writer code object has no
     local events. On 3.13.16, the same: 320 instructions, 0 wrong, 25 accepted.
   - *The (o2) sequence and the `return`:* pinned by
     `TestAPutBackThenALaterReenteredWrite.test_the_terminal_state_is_kept_throughout`, which (m3′)
     fails; (m3) changes nothing (check 8).
6. **The real signal.** The orchestrator's twelve-case probe (a child per case, its own `SIGTERM`
   from inside a heartbeat's write, `units_done=7`), against `2959b78` and `2bf9c72`: every case
   parses, `killed`, 143, `units_done` 7, the stage kept; one `status.json.<unique>.tmp` left only
   where the process ends before the replace. The two tables are identical, and equal to the log's
   and 02's review's. The threads edge (a worker heartbeating in a loop, the main thread sending
   itself `SIGTERM` twenty times): joined, `killed`, 143, nothing left.

   **The log's observation 1, measured by a real signal.** The agent recorded seven instructions,
   uncovered by `_write_status`'s exception table, at which the sweep's raising handler left
   `_STATUS_LOCK` held, and reasoned that a real signal cannot reach them; it said this was not
   measured on 3.13. Measured here: a child that signals only itself, `SIGALRM` by a one-shot
   interval timer of 20 µs–2 ms, re-armed after each, its handler raising, through heartbeats of
   one run for 45 s (about 27 000 interrupted writes per row), counting writes after which the
   lock was still owned:

   | Tree | 3.12.15 | 3.13.16 | 3.14.8 |
   |---|---|---|---|
   | `2bf9c72` | 0 | 0 | 16, at the `with` (`:327`, offset 24) |
   | `2959b78` | 0 | **14, at `:365`, offset 282** | 16: 11 at the `with` (`:355`), 5 at `:365` |

   At 3.13.16 offset 282 is the `JUMP_BACKWARD` of the filter in `earlier = [n for n in
   sorted(book["in_flight"]) if n < number]`, a comprehension 3.13 inlines; `dis` shows its
   exception table with no entry for offsets 278–286. An exception raised by a handler run at that
   jump's eval-breaker check leaves `_write_status` without its `finally` or its `with` exit. At
   `2bf9c72` the same line was a generator expression, a frame of its own, which never left the lock
   held at 3.13. Its consequence, measured at 3.13.16 with a handler that records `killed` and then
   raises: the file says `killed`; the in-flight entry stays; a heartbeat from another thread does
   not complete; and with that thread non-daemon, a `sys.exit(143)` from the main thread did not end
   the process within 200 s. **Opened as
   `[02b-a-raising-handler-can-leave-the-status-lock-held]`.** The 3.14 rows at the `with` are
   02's, and recorded in the same entry; 3.14 is not a client's version and is not in CI.
7. **The log (B7).** Every section of README §5.1 and the prompt's §4.3 additions; the deviations
   classified, corrections 1–15 among them, the (m3) decision first, one UNINTENDED DRIFT (a test
   docstring that named an issue, caught by the citation guard and reworded before committing); the
   suite before and after; the core run; the §3.4 table; the sweeps against `2bf9c72` (15, 0, 15, 0;
   0, 0, 167, 167) and after (0 in every mode); the shape of the record; every mutation as a diff.
   Every line citation in the log's "State handed to the next prompt" checked by `grep -n` at
   `2959b78`: right. **Residue fixed here:** "this commit" → `2959b78`.
8. **The mutations (B6).** (m1)–(m5) and (m3′) extracted from the log by a script and replayed in
   `bash` in a `git clone` of `2959b78`, `PYTHONPATH` on the clone: `--check`, apply,
   `test_status_writes`, `test_run_registry` and `test_host` (78 tests), `-R --check`, reverse, the
   clone clean. Each ended exactly as the log says: (m1) 4 failures, 281 of 323 twice; (m2) 2, 24 of
   244 twice; (m3) OK; (m3′) 8, 17 of 323 four times; (m4) 4, 21 of 334 four times; (m5) 2, 22 of
   323 twice. The orchestrator's own, in the same clone:
   - (o1) the merge applying **no** in-flight write from a landed base: 21 failures, the real-signal
     children and every point of `test_each_point_each_ending` among them, so the "above `L`" half
     is pinned. The comparison made `>=`: no test fails, as expected (the base holds its own
     write's fields);
   - (o2) `_newest_landed`'s re-read removed: no test fails. By reading, the window (a handler
     between `max` and the payload read that lands a higher write and prunes the key read) gives
     `None` only to a write the handler's higher write then discards, so it is defensive. Recorded,
     not opened;
   - (o3) the prune made before the store, not after: no test fails, and by reading it keeps the
     property (a prune removes only lower keys either way). The note's (o3), the prune removing
     every key but its own, is the agent's (m5), caught.
9. **The records (B7) and CI.** The board's header, 02b's row (322 → 328), W2 ✅, both entries in
   §4 with what resolved each and the tests that pin it, the three "Package lines (02b, …)"
   sentences and the §3 count line are in. `docs/OPEN_ISSUES.md` counted 8 by its rows at
   `2959b78`, the two rows gone, the date. `prompts/INDEX.md`'s line is updated. **CI is not read
   yet:** nothing is pushed, and the sweeps first run on Linux and in `suite (high)` on 3.13.16.

**Verdict:** 02b is accepted, **pending CI**: all three jobs green, the core job's count 86, read
from the run's log after the user pushes `main`. Its two fixes hold and are pinned. The issue its
review opens is put to the user.

*CI (2026-10-17).* The user said yes, and `main` was pushed, `a38022f..c18ec34`. Run
`39060913296` (`tests`, on the push of `c18ec34`) passed all three jobs, each on `ubuntu-24.04`:
`core (no store layer)`, on 3.12.15, with `datastorekit`, `ray` and `sqlalchemy` absent, ran the
four core modules by name, `Ran 86 tests in 24.001s`, `OK (skipped=1)`; `suite (low)`, on 3.12.15,
`Ran 328 tests in 50.746s` and `suite (high)`, on 3.13.16, `Ran 328 tests in 42.989s`, each `OK
(skipped=1)`; `black` 31 files unchanged. The one skip in each is `test_host`'s macOS readers, as at
01 and 02, so both sweeps ran and passed on Linux, at 3.12 and at 3.13, in all eight modes. The
3.13 hazard opened above is not something these tests look for, and a green run does not narrow
it. **02b's review is complete; check 9 holds.**

### 1.1 Items

| Item | Prompt | What | Closes | State |
|---|---|---|---|---|
| **H1** | 01 | the host's identity and boot, in the manifest and `status.json`; `foreign`; a run from an earlier boot `stale`; `list` | `[04-runs-do-not-say-which-machine-produced-them]` | ✅ `387c58f` |
| **W1** | 02 | `status.json`'s own temporary name; a superseded write discarded | `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` | ✅ `2bf9c72` |
| **W2** | 02b | the merge re-applying only newer in-flight writes; the record of what landed never lowered; the instruction sweep | `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]`, `[02-the-landed-record-is-unpinned-and-can-move-backwards]` | ✅ `2959b78` |
| **W3** | 02c | the writer's two filters as generator expressions; a sweep at every `JUMP_BACKWARD` of the writer, the lock and the in-flight entry checked after a raising handler; the 3.14 `with` point under L11 | `[02b-a-raising-handler-can-leave-the-status-lock-held]` (under L11 (a), narrowed to 3.14) | ⬜ |
| **C1** | 03 | an unreadable status counted as in use; `list` flags it | `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` | ⬜ |
| **E1** | 04 | `python -m runregistrykit end`, what it checks and writes | `[a3-v2-a-hard-killed-run-blocks-its-store]` | ⬜ |
| **B1** | 05 | `begin` refuses a store a `running` run names | `[00-begin-does-not-refuse-a-second-writer]` | ⬜ |
| **V1** | 06 | `v0.2.0`, its release notes, the adoption notes | — | ⬜ |
| **Z1** | 07 | the verification document; the close | — | ⬜ |

**Legend.** ⬜ not yet · ✅ done.

## 2. Gates (README §7)

| Gate | Status |
|---|---|
| **G1** | not yet (SGK adopts `v0.2.0`) |
| **G2** | not yet (CPBH adopts) |
| **G3** | not yet (SI adopts) |

---

## 3. Active and unresolved issues

Four: three of the five assigned here, and one found by 02b's review, at the end of this section,
assigned to 02c.
The two found by 02's review were closed by 02b (`2959b78`), and are in §4. Five were assigned here from the `inherited-issues` board on 2026-10-16, when this campaign
was planned, each with its text unchanged except for an **Assigned** line. One moved with a
correction: `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`'s next step
does not keep a terminal state when the handler returns (README §0.2), so its entry gains a
**Corrected at planning** paragraph. `[04-runs-do-not-say-which-machine-produced-them]` was closed
by 01 (`387c58f`), and `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`
by 02 (`2bf9c72`); both are in §4. In the README's order:

### `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`

**Opened:** 2026-10-16 here, reading SGK's stale-run brief against
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`; measured. **Owner:**
none.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 03: the in-use check counting
a run whose status cannot be read, under L6 (its README §2). Moved here from the `inherited-issues`
board the same day, unchanged above and below but for this line. It is one of the five that bear on
a long job that may be interrupted, and the campaign takes them together.

*The defect.* The store operations' in-use check fails open on a run whose `status.json` cannot be
read. `list_runs` reads it as `read_json(…) or {}` (`runregistrykit/__init__.py:771`), so a
missing, torn or non-JSON `status.json` gives state `None`, and `liveness` answers `unknown` for an
empty payload (`:301`). `_running_runs_naming` keeps only entries whose state is `running`
(`runregistrykit/stores.py:1017`), so the run is not counted, however alive its process, and
fingerprint, copy, move, retire and amend proceed on its store. `list` prints it as `unknown`
without `!!` (`runregistrykit/__main__.py:550-556`; only `stale` is flagged).

*Measured* here at `79015a7`, 2026-10-16, by the scratch probe of
`[a3-v2-a-hard-killed-run-blocks-its-store]`, on a full four-shard registered store in a `tempfile`
directory. A run begun in the probe's own process named the store (liveness `alive`), and
`fingerprint_store`, `retire_store(dry_run=True)` and `copy_store` each refused, naming it. Its
`status.json` was then cut to its first half, as a torn write leaves it. The process still answered
`kill -0`; `list_runs` gave state `None`, liveness `unknown`; and all three operations proceeded. A
real `retire_store` then deleted the primary and all four shards, leaving the tombstone, while the
run's process was alive. Move and amend make the same check (`:1102`, `:2017`), read and not run.

*Impact.* The check is the store layer's one protection of a store being written (module docstring,
`stores.py:102-107`), and here it fails in the direction that loses data: it lets a person
retire, move or fingerprint a store under a live writer, with nothing in `list` to warn them. The
known cause is the race of
`[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`: rare in any one
heartbeat, but a ~36-hour run has thousands. A `status.json` lost any other way does the same.

*Next step.* Count a run whose manifest names the store and whose `status.json` cannot be read as
possibly running: refuse, saying that the status is unreadable and that the registry cannot tell
whether the run is alive. Such a run is then where a stale one is, and is resolved by
`[a3-v2-a-hard-killed-run-blocks-its-store]`'s route. Fixing the race removes the known cause, not
this failure of the check. The test is the probe's case, asserting the refusal for each operation.
Whether `list` flags an `unknown` run that has a manifest is a smaller, separate choice.

*Package lines (01, `387c58f`).* `list_runs`' status read `runregistrykit/__init__.py:771` →
`:992`; `liveness`'s answer for an empty payload `:301` → `:489`. `_running_runs_naming`'s filter
`stores.py:1017` is unmoved; move's check `:1102` → `:1114`, amend's `:2017` → `:2029`; the module
docstring `:102-107` is unmoved. `list`'s rows, `__main__.py:550-556`, are now `:555-566`; 01 adds
`??` for a `foreign` run there, and `unknown` is still printed without a marker.

*Package lines (02, `2bf9c72`).* `list_runs`' status read `runregistrykit/__init__.py:992` →
`:1115`; `liveness`'s answer for an empty payload `:489` → `:585`. `stores.py` and `__main__.py` are
not touched by 02, so their lines above stand. 02 removes the one known cause of an unreadable
`status.json`, a handler's write sharing the heartbeat's temporary file, and every other cause (a
disk error, a hand edit, a file truncated or lost by anything else) stands, as does this entry's
defect in the check.

*Package lines (02b, `2959b78`).* `list_runs`' status read `runregistrykit/__init__.py:1115` →
`:1156`; `liveness`'s answer for an empty payload `:585` → `:618`. `stores.py` and `__main__.py` are
not touched by 02b, so their lines above stand.

### `[a3-v2-a-hard-killed-run-blocks-its-store]`

**Opened:** 2026-10-16 in SGK's `handover` campaign, by a measurement ahead of its A3 v2 launch and
not by a prompt; handed over the same day (SGK `prompts/handover/runregistrykit-stale-run-brief.md`,
committed in SGK `79434bf`). **From:** SGK `prompts/handover/IMPLEMENTATION_STATE.md` §3.
**Owner:** none. Found by SGK in the package, not inherited from SGK's code; its name is SGK's, kept
so that SGK can find it here.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 04: the `end` command, under
L7 and L8 (its README §2). Moved here from the `inherited-issues` board the same day, unchanged
above and below but for this line. It is one of the five that bear on a long job that may be
interrupted, and the campaign takes them together.

*The defect.* A run killed by `SIGKILL`, power loss, a reboot or the OOM killer never reaches
`Run.finish`, so its `status.json` says `running` for ever. `list` reports it as stale, which is
right. Every store operation that checks for a running run counts it "alive **or stale**", so
fingerprint, copy, move, retire and amend refuse its store, and so does a resumed run's
`finish(fingerprint=True)`. The refusals name the remedy, "a stale run is ended by a person, with
Run.finish". No command applies it, and `Run.finish` checks nothing about the run it ends. The
rule the refusals keep, that the registry does not decide that a run is dead
(`runregistrykit/stores.py:1031-1032`), is not in question; SGK does not ask to weaken it.

*The package's lines (`79015a7`).*

- *The in-use check.* `_running_runs_naming` (`runregistrykit/stores.py:998`) keeps every entry
  whose state is `running` other than the excluded caller (`:1017`), whatever its liveness. Its
  callers are copy and move (`_refuse_if_in_use`, `:1029`, called at `:1102`), `fingerprint_store`
  (`:1338`), `retire_store` (`:1664`) and `amend_sidecar` (`:2017`). The module docstring says so
  (`:102-107`).
- *The remedy the refusals name.* At `:1038-1039` (copy, move), `:1344` (fingerprint), `:1667`
  (retire) and `:2020` (amend). `test_store_retire.TestRefusals.test_a_stale_running_run_and_its_remedy`
  (`runregistrykit/tests/test_store_retire.py:436`) asserts it, on `a_stale_run`
  (`runregistrykit/tests/store_fixtures.py:148`): a run given a reaped pid, not a killed process.
- *No command applies it.* `main` (`runregistrykit/__main__.py:408`) has `list` (`:418`) and `store
  show|create|adopt|copy|move|fingerprint|retire|amend` (`:433-522`). None writes a `status.json`.
- *The remedy checks nothing.* `Run.finish` (`runregistrykit/__init__.py:424`) checks only that the
  state is in `TERMINAL_STATES` (`:99`, `:441`). It does not consult `pid_alive` (`:258`), the
  heartbeat or `liveness` (`:294`). A person who ends the wrong directory ends a live run's record.
- *The resumed run.* `_fingerprint_results` passes `taken_by=self` (`:476`), the only exclusion
  (`stores.py:1338-1339`), so a later run on the same store is refused by its stale predecessor. It
  records `fingerprint_error` and writes no fingerprint.

*Measured.* By SGK, 2026-10-16 at SGK `f1a7de3` with `runregistrykit` 0.1.0, no Ray, on a throwaway
two-shard store (brief §1, steps 1-6). A child process that had called `begin` and `heartbeat` was
sent `SIGKILL` (returncode −9); its `status.json` was the same before and after, `running`, and
`liveness` gave `stale`. `list` flagged it `!!`. A second `begin` on the store returned normally,
and its `finish("done", exit_code=0, fingerprint=True)` wrote `done` with no fingerprint and a
`fingerprint_error` naming the killed run. `store fingerprint --write`, `store retire --dry-run`
(with and without `--without-fingerprint`) and `store copy` each exited 1, the sidecar's SHA-256
unchanged. Once `kill -0` showed the pid gone, `Run(…).finish("killed", exit_code=137)` by hand
cleared the `!!`, `store fingerprint` matched the recorded digest, and `store retire` completed.

**Re-measured here** at `79015a7`, 2026-10-16, by a scratch probe (not committed) on the suite's
own fixtures (`RetireTestCase`, a full four-shard store) in a `tempfile` directory: a child process
that called `begin` and `heartbeat(stage=…)` on the store was sent `SIGKILL` (returncode −9).
`status.json` was unchanged by the kill; `list_runs` gave state `running`, liveness `stale`.
`fingerprint_store`, `retire_store(dry_run=True)` and `copy_store` each refused, naming the run. A
resumed run's `finish("done", exit_code=0, fingerprint=True)` wrote `done`, no `fingerprint`, and a
`fingerprint_error` naming the stale run.

*Impact.* For SGK's A3 v2, a ~36-hour Ray build that may be interrupted and resumed: after a hard
kill nothing is lost, and the documented route works, but it is the API by hand and unguarded, on
the build that matters most. For any client: a stale entry stays `!!` in `list` until someone ends
it through the API, and every store operation on its store is refused meanwhile. A `SIGTERM`'d run
whose terminal state was lost to `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`
meets the same block. SGK does not ask for a release before A3 v2 (brief §2).

*Next step.* Choose a route; SGK offers three and prefers the first (brief §1):

1. **A person-run command that records a stale run as terminal**, for example `python -m
   runregistrykit end RUN_ID --reason TEXT`. It refuses unless the run's state is `running` and its
   pid fails `kill -0`, and writes a terminal state, a `null` exit code (nothing observed one) and
   who ended it, when, why and at what `git_head`. It never writes the manifest and deletes nothing.
   The open point is the state: `killed` is a terminal state already, but `finish`'s docstring calls
   it "something a caller reports, not something observed" (`__init__.py:425-426`); a new `lost`
   says the registry never saw how the run ended, at the cost of a fourth terminal state that
   `liveness` and `list` learn. Either is a change to what the registry writes. The same check could
   guard `Run.finish` when called on a run that is not the caller's own.
2. **An explicit exclusion on the store operations**, for example `--stale-run RUN_ID`, accepted
   only for a named run whose pid fails `kill -0` and recorded in the sidecar's `history` or the
   tombstone. It unblocks the store and leaves the run `running`, with its `!!`.
3. **`begin` and `finish` learning about predecessors** (`supersedes: [RUN_ID]`). It decides at
   `begin` that a stale run is dead, the line the package has chosen not to cross; listed by SGK
   for completeness.

*Added on hand-over.* Any route that tests `kill -0` tests evidence that holds only on the machine
that owns the pid, and only while the pid has not been reused, which a reboot, one of this entry's
causes, makes likely. So the route depends on `[04-runs-do-not-say-which-machine-produced-them]`
(its fourth question), and that decision is taken first, or with this one. The test SGK proposes
stands: begin a run in a child process, `SIGKILL` it, and assert what the new route does; the
probe above is its shape. `a_stale_run` fakes the pid and never exercises a kill.

*Split on hand-over.* The brief's point that `begin` does not look for a run already on its store
is held as its own entry, `[00-begin-does-not-refuse-a-second-writer]`: it holds whether or not the
first run is dead, and its fix is none of the three routes.

*Package lines (01, `387c58f`).* In `runregistrykit/stores.py`: `_running_runs_naming` `:998` and
its filter `:1017` are unmoved; `_refuse_if_in_use` `:1029` → `:1041`, called at `:1102` → `:1114`;
`fingerprint_store`'s check `:1338-1339` → `:1350-1351`; `retire_store`'s `:1664` → `:1676`;
`amend_sidecar`'s `:2017` → `:2029`; the module docstring `:102-107` is unmoved. The remedy text
`:1038-1039` → `:1050-1051` (copy, move), `:1344` → `:1356` (fingerprint), `:1667` → `:1679`
(retire), `:2020` → `:2032` (amend), unchanged in its words; `stores.py:1031-1032` → `:1043-1044`.
In `runregistrykit/__main__.py`: `main` `:408` → `:413`, `list` `:418` → `:423`, the store
subcommands `:433-522` → `:438-527`. In `runregistrykit/__init__.py`: `Run.finish` `:424` → `:621`
(its docstring `:425-426` → `:622-623`), `TERMINAL_STATES` `:99` → `:101`, its check `:441` →
`:638`; `pid_alive` `:258` → `:260` (`PermissionError` `:276` → `:278`); `liveness` `:294` →
`:465`; `_fingerprint_results`' `taken_by=self` `:476` → `:673`.

*Package lines (02, `2bf9c72`).* Only `runregistrykit/__init__.py` moved: `Run.finish` `:621` →
`:744` (its docstring `:622-623` → `:745-746`), `TERMINAL_STATES` `:101` → `:104`, its check
`:638` → `:761`; `pid_alive` `:260` → `:356` (`PermissionError` `:278` → `:374`); `liveness`
`:465` → `:561`; `_fingerprint_results`' `taken_by=self` `:673` → `:796`. `stores.py` and
`__main__.py` are not touched by 02, so their lines above stand.

*Package lines (02b, `2959b78`).* Only `runregistrykit/__init__.py` moved: `Run.finish` `:744` →
`:785` (its docstring `:745-746` → `:786-787`), its check `:761` → `:802`; `TERMINAL_STATES` `:104`
is unmoved; `pid_alive` `:356` → `:389` (`PermissionError` `:374` → `:407`); `liveness` `:561` →
`:594`; `_fingerprint_results`' `taken_by=self` `:796` → `:837`. `stores.py` and `__main__.py` are
not touched by 02b, so their lines above stand.

### `[00-begin-does-not-refuse-a-second-writer]`

**Opened:** 2026-10-16, split on hand-over from SGK's `[a3-v2-a-hard-killed-run-blocks-its-store]`
(its brief §1, "*`begin` does not look*"), and measured here for a live first run. **Owner:**
none.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 05: `begin`'s refusal, under
L9 (its README §2). Moved here from the `inherited-issues` board the same day, unchanged above and
below but for this line. It is one of the five that bear on a long job that may be interrupted, and
the campaign takes them together.

*The defect.* `begin` (`runregistrykit/__init__.py:604`) reads the results store's sidecar only to
refuse a tombstone (`:686-698`, the refusal at `:692`). It does not ask whether a `running` run,
alive or stale, already names that store, so a second run on a store that a live run is writing is
begun without a word. The store operations make that check (`_running_runs_naming`,
`runregistrykit/stores.py:998`), and the module docstring calls it "a check and not a lock: a run
begun after it is not seen" (`:106-107`); `begin` does not make it at all.

*Measured* here at `79015a7`, 2026-10-16, by the scratch probe of
`[a3-v2-a-hard-killed-run-blocks-its-store]`: with a run begun in the probe's own process on a
registered store (liveness `alive`), a second `begin` with the same `results` returned a run, and
the two manifests carry the same `results_store_id`. SGK measured the stale case (brief §1, step
4).

*Impact.* The registry does not schedule or lock, so nothing here can stop two writers; but a
resume after an interruption is when a person begins a second run on a store, and the case that
does harm is the one where the first run is not dead: a detached child still working, a `SIGTERM`
not yet acted on, or a run on another machine whose pid this machine cannot test
(`[04-runs-do-not-say-which-machine-produced-them]`). Then two jobs write one SQLite store, and
nothing records that they did.

*Next step.* `begin` names the `running` runs whose manifest names its `results`, by path or by
`results_store_id` as `runs_naming` matches them (`stores.py:957`), and refuses, before the run
directory is created, if any is alive. What a stale one gets is the decision of
`[a3-v2-a-hard-killed-run-blocks-its-store]`: refusing it too is the reading consistent with "the
registry does not decide that a run is dead", and leaves a person to end it first by that entry's
route. A refusal writes nothing new, so it is not a change to what the registry writes. The test:
begin a run, begin a second on its store, and assert that the refusal names the first and that no
second run directory exists.

*Package lines (01, `387c58f`).* `begin` `runregistrykit/__init__.py:604` → `:801`; its tombstone
check `:686-698` → `:892-904`, the refusal `:692` → `:898`; it now reads `this_host()` at `:906`,
after that check and before the run directory is made. `_running_runs_naming` `stores.py:998`, the
module docstring `:106-107` and `runs_naming` `:957` are unmoved.

*Package lines (02, `2bf9c72`).* `begin` `runregistrykit/__init__.py:801` → `:924`; its tombstone
check `:892-904` → `:1015-1027`, the refusal `:898` → `:1021`; `this_host()` `:906` → `:1029`.
`stores.py` is not touched by 02, so its lines above stand.

*Package lines (02b, `2959b78`).* `begin` `runregistrykit/__init__.py:924` → `:965`; its
tombstone check `:1015-1027` → `:1056-1068`, the refusal `:1021` → `:1062`; `this_host()` `:1029` →
`:1070`. `stores.py` is not touched by 02b, so its lines above stand.

### `[02b-a-raising-handler-can-leave-the-status-lock-held]`

**Opened:** 2026-10-17 by the orchestrator's review of 02b, from the log's observation 1 and the
review's check 6; measured. **Owner:** none.

**Assigned (2026-10-17):** to prompt 02c of this campaign, which follows 02b at once, ahead of 03,
as 02b followed 02: it fixes the writer while it is the last thing changed. 02c makes the two
filters generator expressions, and pins them with a sweep at every `JUMP_BACKWARD`. The `with`
point at 3.14 is put to the user as L11 (README §6.2), recommended (a): recorded in `_update`'s
docstring, and this entry narrowed to it, not fixed. *Taken 2026-10-17: (a).*

*The defect.* `_write_status` (`runregistrykit/__init__.py:352`) holds `_STATUS_LOCK` in a `with`
(`:355`) and removes its in-flight entry in a `finally`. At 3.13.16 the exception table of its
code leaves offsets 278–286 uncovered: the filter of the comprehension `earlier = [n for n in
sorted(book["in_flight"]) if n < number]` (`:365`), which 3.13 inlines, and whose
`JUMP_BACKWARD` (offset 282) checks the eval breaker. A handler run there that raises leaves the
function without the `finally` or the `with` exit: the lock stays held by the thread that was
writing, and the in-flight entry stays. 02's `:336` was a generator expression, a frame of its
own, and its exception surfaced at a covered `CALL`; 02b made it a list comprehension. The second
comprehension, `:372`, has the same shape and was not reached in the measurement. At 3.14.8 the
`with` statement itself (`:355`; `:327` at `2bf9c72`) has such a point, at both commits; 3.14 is
in no client's use and not in CI.

*Measured* at `2959b78`, 2026-10-17 (scratch, not committed): a child that signals only itself,
`SIGALRM` from a one-shot timer of 20 µs–2 ms re-armed after each, the handler raising, through
45 s of heartbeats on one run (about 27 000 interrupted writes): the lock left held after 0 writes
at 3.12.15 (both commits), **14 at 3.13.16** (all at `:365`, offset 282; 0 at `2bf9c72`), and 16 at
3.14.8 (11 at the `with`, 5 at `:365`; 16 at the `with` at `2bf9c72`). With a handler that
records `finish("killed", exit_code=143)` and then raises, at 3.13.16: the file says `killed`; the
in-flight entry stays; another thread's `heartbeat` does not complete in 5 s; and with that thread
non-daemon, `sys.exit(143)` from the main thread did not end the process within 200 s.

*Impact.* The terminal state is kept, and the file parses. But a driver whose handler raises (as
SGK's do, `SystemExit(128 + signum)`), on 3.13, with a second thread that writes the status (a
heartbeat thread, a stdout tee), can hang instead of exiting, about once in 2 000 interrupted
writes here; and a process that goes on after the raise composes every later write from its
landed payload rather than the file, since an in-flight entry is always present, so a launcher's
`heartbeat(pid=…)` from another process is overwritten. SGK runs 3.12, where it was not seen; CPBH
and SI run 3.13 and call nothing of the registry yet. 02b's sweep did not see it because it raises
at every instruction, uncovered ones included, and so runs in a child process; it does not check
the lock after an attempt.

*Next step.* Make the writer's two comprehensions forms whose exception tables are complete on 3.12
and 3.13 (a generator expression, as 02 had, or a loop), and measure them as above. A test: the
real-signal bombardment, bounded in time, in a child, asserting the lock not owned and no in-flight
entry after each interrupted write; or the sweep restricted to the instructions that check the eval
breaker, with the same assertions. The `with` point at 3.14 is for the same prompt to decide.

*Measured at writing 02c (2026-10-17, at `9d26357`).* 02c's "At writing" holds the tables. In
short:
- **3.12 inlines the comprehension too.** Its table has the same gap (offsets 278 and 398), and a
  real signal did not leave the lock held there. At 3.13 and 3.14 the handler runs at the
  `JUMP_BACKWARD` itself.
- **A `for` loop with an `if`, the next step's other form, has the same gap** at 3.12, 3.13 and
  3.14, and a real signal left the lock held 4 times at 3.13.16 in 45 s.
- **Generator expressions close it.** 0 at 3.12.15 and 3.13.16 in 45 s, and 0 in 232 531
  interruptions at 3.13.16 over 3 × 120 s, against 5 for `2959b78` in 45 s.
- **The `with` point at 3.14** remains after the change, 15 in 45 s. A bare `with` over an `RLock`,
  with no registry code, left it held after 5 228 of 34 704 interruptions at 3.14.8, and never at
  3.12 or 3.13. A hand-written acquire and release instead leaks at its `finally` at every version
  (10, 11 and 6).
- **The sweep restricted to `JUMP_BACKWARD`**, a plain, a re-entered and a twice re-entered
  heartbeat (3, 7 and 12 attempts), catches `2959b78` at 3.12 as well as at 3.13: 1, 2 and 4
  attempts leave the lock held and the in-flight entry. `:372` is reached only by the twice
  re-entered write. The generator expressions: 0 at every version.

---

## 4. Resolved issues

### `[04-runs-do-not-say-which-machine-produced-them]`

**Opened:** 2026-09-24 in SGK, from a cross-machine question, not by a prompt; handed over
2026-10-16. **From:** SGK `prompts/run-registry/IMPLEMENTATION_STATE.md` §3. **Owner:** none. **A
decision, not a defect.** SGK decided the change for its own runs (user decision of 2026-09-24) and
never built it; whether the package makes it for every client is this repository's decision.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 01: the host, its identity and
its boot, recorded and used by `liveness` and `list`, under L1–L4 (its README §2). Moved here from
the `inherited-issues` board the same day, unchanged above and below but for this line. It is one of
the five that bear on a long job that may be interrupted, and the campaign takes them together.

*What is asked.* SGK's decision: a `machine` field in the manifest; `list` refusing to judge the
liveness of a record whose machine is not this one; and a rule that only terminal-state run
directories are transferred between machines. ChamPBH and StochasticInstantons may or may not run
one registry across machines.

*The package's lines.* The manifest is built in `begin` (`runregistrykit/__init__.py:604`): `run_id`,
`created`, `purpose`, `campaign`, `prompt`, `argv`, `cwd`, `script`, `script_sha256`, `unit`,
`expected_units`, `checkpoint`, `results`, `results_store_id`, `scope`, `heartbeat_means`
(`:707-723`), then `git_provenance`'s `git_head` and `git_dirty` (`:724`, defined `:140`) and
`packages` (`:725`). No machine, platform or hostname is recorded. Liveness is `pid_alive` (`:258`,
`os.kill(pid, 0)` against this machine's process table) and `liveness(status, stale_after, now)`
(`:294`), called by `list_runs` (`:749`, `:784`); neither takes a machine.

*Measured.* `git grep -n -i 'machine\|platform\|node()' caad864 -- runregistrykit` finds only an
unrelated comment about path separators (`stores.py:240`) and a comment in a test
(`tests/test_run_registry.py:169`). Read 2026-10-16.

*Impact.* Two. *Provenance:* SGK is to run its A3 rebuild on a second machine, and rows computed on
different hardware can differ in their last bits; `git_head` says what code ran, not what ran it.
*Liveness:* once run directories are copied between machines, `list` tests a pid from another
machine against this one's process table. A terminal-state record is harmless; one still marked
`running` gets a confident wrong answer, a false "dead" or, if the pid is reused here, a false
"alive".

*Added on hand-over: three questions the decision has to answer.*

- **A manifest with no `machine`.** Every client holds manifests written before the field would
  exist, and no reader of an older form is added (`CLAUDE.md`, "Releases"). So the rule has to give
  the field's absence a meaning in the current form, for example "not recorded: liveness is judged
  here, as today", and `list` has to say which it did.
- **What names a machine.** `platform.node()`, as the brief proposes, is the hostname, and on macOS
  it can change with the network. A machine's own runs would then read as foreign. A name a person
  sets (an environment variable or a per-machine config file, not the client's committed
  `runregistrykit.toml`, which every machine shares), with `platform.machine()` beside it for the
  architecture, would be steadier.
- **Where it is recorded.** The pid that liveness tests is in `status.json`, written by `heartbeat`
  (`:405`), which a launcher calls with a detached child's pid. The machine that matters for
  liveness is the one that pid belongs to, so the field belongs beside the pid, in `status.json`,
  whether or not the manifest records it too for provenance.

*Next step.* Decide whether the registry records the machine for every client, and if so answer the
three questions above. `list` reporting a record from another machine as *foreign*, rather than
judging its liveness, is still recording, inside the registry's "it records; it does not supervise"
boundary. SGK has nothing live to migrate: none of its 43 run directories was `running` on
2026-10-16 (SGK's reading).

*Added 2026-10-16, reading SGK's stale-run brief: a fourth question, and why this decision comes
first.*

- **A pid reused on this machine.** A reboot, one of the ways a run ends without `finish`, ends
  every run on the machine, and afterwards the pids in their `status.json` can belong to new
  processes. `pid_alive` (`runregistrykit/__init__.py:258`) then answers `True`, as it does for
  another user's process (`PermissionError`, `:276`). `liveness` still calls such a run stale when
  its heartbeat is old (`:310`), so `list` is right, but a guard that refuses unless the pid fails
  `kill -0` refuses wrongly. Something recorded beside the pid that changes when the machine
  reboots (a boot identifier) or that names the process (its start time) would let a check tell a
  reused pid from the run's own. Like the machine, it belongs beside the pid, in `status.json`.
- **The other long-job entries depend on it.** The routes proposed for
  `[a3-v2-a-hard-killed-run-blocks-its-store]` and `[00-begin-does-not-refuse-a-second-writer]`
  judge another run's liveness by its pid. Their guards mean what they say only once this decision
  is made, so it is taken first, or with them.

**Resolved (2026-10-16, by 01, `387c58f`).** The package records the machine and the boot a run is
on, for every client, under L1–L4 (README §6.2) as the user took them. `this_host()` is a new public
name (`runregistrykit/__init__.py:431`). Its three private readers (`:338`, `:376`, `:410`) use the
standard library only, with no subprocess. `begin` writes the manifest's `host` (`:931`) and the
first status's (`:946`), and every later write keeps the status's. `liveness` (`:465`) is ordered as
01's §2.4 says. `list_runs` (`:962`) reads this host once per call and gives `host`, `host_id` and
`host_recorded`. `list` marks a `foreign` run `??` and counts records with no host; the store
operations' refusal names a `foreign` run by its host. The log is
[`logs/01-the-host.md`](logs/01-the-host.md). What resolved each of the four questions:

- **A manifest with no `machine`.** A record with no `host` was written before the field existed.
  So were a `host` that is not an object and a `host.id` of null, which is what a platform with no
  identity records. Each is judged here, by `kill -0` and the heartbeat, exactly as `v0.1.0` judged
  it, and `list` counts it as "N with no host recorded". Pinned by
  `test_host.TestAnOldRecord.test_a_status_with_no_host_is_judged_by_pid_and_heartbeat` and
  `test_list_runs_judges_it_here_and_says_no_host_is_recorded`;
  `test_host.TestTheJudgement.test_a_host_that_names_no_id_is_judged_here`; and
  `test_host.TestTheCommandLine.test_foreign_and_stale_rows_and_the_count_of_records_with_no_host`.
- **What names a machine.** The OS's own identity, as a digest: macOS `gethostuuid(3)`, Linux
  `/etc/machine-id` (then `/var/lib/dbus/machine-id`). The id is the first 16 hex characters of the
  SHA-256 of `b"runregistrykit host\0"` and the identity, and the identity itself is never written.
  A display name sits beside it, `RUNREGISTRYKIT_HOST_NAME` or `platform.node()`, and is for
  reading only. Pinned by `test_host.TestTheReaders` (the readers on macOS, run locally, and on
  Linux, run only in CI; the digest; the name; each reader failing; the Linux files and the macOS
  calls failing, on any platform) and by
  `test_host.TestWhatIsWritten.test_no_raw_identity_reaches_a_file`.
- **Where it is recorded.** Both. `status.json` gets `host: {id, boot}` beside the pid it
  qualifies, and every later write keeps it, `heartbeat(pid=…)` included. The manifest gets `host:
  {id, name, machine, system, release, python}` for provenance. Both are written with null values
  when a reader fails. Pinned by `test_host.TestWhatIsWritten` (the manifest and the first status;
  every later write; a failing reader writing null).
- **A reused pid.** A `running` record on this host from another boot is `stale` whatever `kill -0`
  says. A `running` record on another host is `foreign`: its pid is not tested here and its
  heartbeat is not weighed, it is never called dead, and the store operations count it as in use.
  Pinned by `test_host.TestTheJudgement` (another host, live pid or dead; an id read where this host
  has none; another boot; this host and boot; a terminal record from another host; `here` read
  afresh) and `test_host_stores.TestARunOnAnotherHostIsInUse` (copy, move, fingerprint, retire's
  dry run and amend each refuse and name the host). A pid reused within one boot is not told apart
  (L3 (b), README §8).

SGK's third point, that only terminal-state run directories are moved between machines, is a rule
for a client's people and not something the package enforces. A `running` record moved anyway is
reported `foreign`, which is what keeps the package from judging it.

### `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`

**Opened:** 2026-10-03 by SGK's `a3-v2-readiness` prompt 04, from the orchestrator's reading;
handed over 2026-10-16. **From:** SGK `prompts/a3-v2-readiness/IMPLEMENTATION_STATE.md` §3.
**Owner:** none. Read, not measured.

**Assigned (2026-10-16):** to the `interrupted-runs` campaign, prompt 02: `status.json` written
through a name of its own, and a superseded write discarded, under L5 (its README §2). Moved here
from the `inherited-issues` board the same day, unchanged above and below but for this line and the
correction at the end. It is one of the five that bear on a long job that may be interrupted, and
the campaign takes them together.

*The defect.* Every write of `status.json` goes through one fixed temporary name.
`write_json_atomic` (`runregistrykit/__init__.py:242-251`) sets `tmp = path + ".tmp"` (`:245`),
opens it `"w"`, `json.dump`s, flushes, `fsync`s and `os.replace`s it onto `path` (`:251`).
`Run._update` (`:398-403`) calls it for `status.json` (`:402`), and `heartbeat` (`:405`) and
`finish` (`:424`) both go through `_update`. A heartbeat's write and a `finish`'s write share
`status.json.tmp`, and so share its inode while both are open.

*The sequence.* A driver's signal handler runs while a heartbeat is inside `with open(tmp, "w")`,
before its flush. The handler's `finish` reopens `status.json.tmp`, truncating the heartbeat's
inode, writes its payload, flushes, and renames it onto `status.json`. That inode is now
`status.json`, and the heartbeat's handle is still open on it with its payload buffered.

*Corrected on hand-over: both ways the handler can end corrupt it.* The brief described the handler
raising. It does not have to:

- **The handler raises** (SGK's does). Unwinding closes the heartbeat's handle, which writes its
  buffered partial JSON at offset 0 of `status.json`'s inode: the file is a prefix of the heartbeat's
  payload followed by the rest of `finish`'s, and does not parse.
- **The handler returns.** The heartbeat finishes its dump and flushes it at offset 0 of the same
  inode. The two payloads have the same keys (`begin` writes `state` and `exit_code` from the
  start, `:728-734`), and `finish` changes `state` from `running` to a shorter word and
  `exit_code` from `null` to a number, so the heartbeat's is often the longer. Then it overwrites
  all of `finish`'s, the file parses, and it says `running`, the state the heartbeat read before
  `finish`: the terminal state is lost silently, and `list` later shows the run `stale`. If the
  heartbeat's is shorter, the tail of `finish`'s remains and the file does not parse. Either way its
  `os.replace` then raises `FileNotFoundError`, because `status.json.tmp` was renamed away.

So the defect is the package's whatever the client's handler does. SGK's `finish_after_exec` makes a
second `finish`, which reads the unparseable file as `{}` and rewrites it valid but without `pid`,
`stage` or `units_*`; a `SIGKILL` between the two leaves it unparseable, and `list` shows the run as
`unknown`.

*Measured.* Read, not measured. The window is one `json.dump`, once per heartbeat (at most every 30 s
in SGK's driver). SGK has not reproduced it.

*Corrected on hand-over: the fix is not a change to `write_json_atomic`'s name for everyone.* The
brief proposed a unique temporary name per write (`tempfile.mkstemp` in the same directory), inside
`write_json_atomic`. The store layer depends on the fixed name. `_tmp_path`
(`runregistrykit/stores.py:255`, "The temporary name `write_json_atomic` writes through") is how a
leftover from an interrupted sidecar write is found and refused: by `_write_new_sidecar` (`:789`),
`_update_sidecar` (`:809`), `create_sidecar` (`:863`), `copy` and `move`'s preparation (`:1105-1108`),
`retire`'s failure message (`:1532`) and its refusal to complete (`:1650`). Tests pin it:
`test_run_registry.TestStatus.test_status_is_replaced_atomically_from_the_same_directory` asserts
the `.tmp` suffix (`runregistrykit/tests/test_run_registry.py:612`), and `test_store_copy_move`'s
`test_C4_the_sidecar_is_written_to_its_tmp_name_and_the_replace_fails` (`:427`) the sidecar's
`.tmp`. A unique name inside `write_json_atomic` would make every one of those checks look for a
file that is never written, and no test of a refusal would notice unless it builds the leftover
under the old name. Two more points:

- `tempfile.mkstemp` creates the file with mode `0600`, and `os.replace` keeps it; today's
  `open(tmp, "w")` gives `0666` less the umask. `status.json` would become readable only by its
  owner unless the mode is set.
- `write_json_atomic` is in `__all__` (`runregistrykit/__init__.py:96`), so a client may call it
  and may rely on its `.tmp` name.

*Next step.* Give `status.json` writes, and only those, a unique temporary name in the same
directory, with the mode the old name had: through `Run._update`, or an argument to
`write_json_atomic` whose default keeps `<path>.tmp`. Sidecar writes keep the fixed name and its
leftover checks. The reproduction is a test that writes `status.json` twice through a patched
`json.dump` which makes the second write from inside the first, run once with the inner write
raising and once returning. Say in the release notes whether `write_json_atomic` changed.

*Widened (2026-10-16), reading SGK's stale-run brief.* Both outcomes of the race now have measured
consequences beyond `list`. A `status.json` that does not parse hides a run that is still alive
from the store operations' in-use check, which then lets fingerprint, copy, move, retire and amend
proceed: `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`, where a retirement
deleted a live run's store. A terminal state lost silently leaves the run `running` for ever, and
it then blocks its store as a hard-killed run does: `[a3-v2-a-hard-killed-run-blocks-its-store]`.
The window is still one `json.dump` per heartbeat, but a ~36-hour run with a heartbeat every 30 s
has over four thousand of them.

*Corrected at planning (2026-10-16, `interrupted-runs` README §0.2).* The next step above fixes the
unparseable file and not the lost terminal state. With a unique temporary name per write, a `finish`
made from inside a heartbeat's `json.dump` lands first; if the handler then returns, the heartbeat's
`os.replace` lands after it with the payload it read before `finish`, and the run reads `running`
again. Read, not measured. The fix is the unique name **and** a rule that a write superseded by a
later write from the same `Run` is discarded, not replaced (that README's L5). The reproduction's
returning case is the one that tells the two apart.

*Measured at writing 02 (2026-10-17, at `c2911d3`).* Measured, no longer only read, by a planner's
probe (scratch, not committed; 02's "At writing" gives its table). A child process began a run,
installed a `SIGTERM` handler calling `run.finish("killed", exit_code=143)`, and sent itself
`SIGTERM` from inside a heartbeat's `json.dump` (`units_done=7`), with half the payload or all of it
written to the handle. With today's fixed name:
- **a handler that raises** (`SystemExit`, as SGK's `make_killed_handler` does) left the file
  parseable both times. With half written it said `killed` with `exit_code` `null`, a mixture of the
  two payloads. With all written it said **`running`**: the terminal state was lost though the
  handler raised, which the entry above did not expect;
- **a handler that returns** left **`running`** both times, and `heartbeat` raised
  `FileNotFoundError` into its caller;
- **a handler that ends the process**, as SGK's two `terminal` handlers do (`SIG_DFL`, then `os.kill`
  itself), left `killed` and 143 both times. The heartbeat's buffered bytes died with the process.

With a `mkstemp`-named write and nothing else (L5 (b)), raising and ending the process kept `killed`
and 143, and returning left `running` both times, which confirms the correction above. Ending the
process left one `status.json.<x>.tmp` behind. In every case that kept `killed`, `units_done` was 0,
not 7: the `finish` read the file before the heartbeat landed. Two more points bear on the fix (02's
§2.3). `Run(path)` is public, and SGK's manual remedy goes through it. SGK's pipeline heartbeats from
its `sys.stdout` stream, so on whichever thread prints.

*Package lines (01, `387c58f`).* 01 moved these lines of `runregistrykit/__init__.py` and
`runregistrykit/stores.py`; nothing above is otherwise changed by it. `write_json_atomic` `:242-251`
→ `:244-253` (`tmp` `:245` → `:247`, `os.replace` `:251` → `:253`); `Run._update` `:398-403` →
`:595-600` (its write `:402` → `:599`); `heartbeat` `:405` → `:602`; `finish` `:424` → `:621`;
`begin`'s first status `:728-734` → `:940-947`, which now writes `host` besides; `write_json_atomic`
in `__all__` `:96` → `:98`. In the store layer `_tmp_path` `:255`, `_write_new_sidecar` `:789`,
`_update_sidecar` `:809` and `create_sidecar` `:863` are unmoved; copy and move's preparation
`:1105-1108` → `:1117-1120`; retire's failure message `:1532` → `:1544`; its refusal to complete
`:1650` → `:1662`. The tests cited are unchanged.

**Resolved (2026-10-17, by 02, `2bf9c72`).** Under L5 (a), refined (README §6.2), as 02's §2
states it. `status.json`, and only `status.json`, is written by a private writer in
`runregistrykit/__init__.py`, and `Run._update` (`:691-723`) is its one caller: `_write_status`
(`:324`) and `_land_status` (`:291`), with `_status_temporary_name` (`:276`) and
`_remove_quietly` (`:284`). The bookkeeping is `_STATUS_WRITES` (`:270`), per `status.json` in the
process, keyed by `os.path.realpath` (`:329`), under the re-entrant `_STATUS_LOCK` (`:265`, held
from `:327`). `begin`'s first status (`:1063-1070`) goes through `_update`, so nothing writes
`status.json.tmp` any more. The log is [`logs/02-status-writes.md`](logs/02-status-writes.md). What
resolved each part:

- **The shared temporary name.** Each write has a name of its own, `status.json.<pid>-<counter>-<8
  hex>.tmp` beside the file (`:276`), created with `os.open(…, O_WRONLY | O_CREAT | O_EXCL, 0o666)`
  (`:305`). A handler's write no longer reopens or truncates the heartbeat's file. Pinned by
  `test_status_writes.TestThePlainWrite.test_the_temporary_name` and by the reproduction,
  `test_status_writes.TestAHandlerInsideAHeartbeat.test_each_point_each_ending` (four points, the
  handler raising and returning: eight cases).
- **The lost terminal state when the handler returns.** A write that finds a later write landed
  while it was writing is discarded, its file removed and nothing replaced (`:311`). One that a later
  write overtakes between its check and its replace puts the later payload back (`:318-319`), under
  the later write's number, so a handler that re-enters the put-back is not undone by it. A write
  composes from the file, then the fields of every earlier write still in flight, then its own; when
  an earlier write is in flight the base is the newest payload landed (`:337-341`). So the
  discarded heartbeat's `units_done` and `stage` are kept. Pinned by the reproduction (with the
  count of replaces at the two points inside `json.dump`), by
  `test_status_writes.TestASecondRunObject` (three tests, one through a symlinked spelling of the
  run directory), by
  `test_status_writes.TestAHandlerDuringThePutBack.test_a_second_handler_inside_the_put_back`, by
  `test_status_writes.TestARealSignal` (a real `SIGTERM` in a child; the handler raises, returns, or
  ends the process) and by `test_status_writes.TestTwoThreads.test_a_heartbeat_thread_and_a_finish`.
- **The `FileNotFoundError` into the caller.** Gone with the shared name: the heartbeat's
  `os.replace` renames its own file, which nothing else has renamed away. Pinned by the reproduction
  (the heartbeat returns, or raises `SystemExit`, and never anything else) and by
  `test_status_writes.TestARealSignal.test_a_handler_that_returns`.
- **The mode.** `0666` less the umask, as `open(path, "w")` gave, not `mkstemp`'s `0600`. Pinned by
  `test_status_writes.TestThePlainWrite.test_the_mode_is_the_one_a_plain_open_gives` (umask `0o022`
  and `0o077`).
- **`write_json_atomic` and the sidecars.** Unchanged: its body, its `<path>.tmp` (`:250`), its
  `os.replace` (`:256`) and its place in `__all__` (`:101`); `stores.py` is not touched, so
  `_tmp_path` and every leftover check built on it stand. Pinned by
  `test_status_writes.TestThePlainWrite.test_write_json_atomic_still_replaces_from_its_tmp_name`
  and the store tests that name `<sidecar>.tmp`. **06's release notes say "`write_json_atomic`:
  unchanged".**

A plain write, with nothing in flight, reads the file once and calls `os.replace` once, and writes
the keys it wrote before (`test_status_writes.TestThePlainWrite.test_a_heartbeat_with_nothing_in_flight_reads_once_and_replaces_once`);
a failed write leaves `status.json` as it was and nothing behind
(`test_a_failed_write_leaves_the_status_as_it_was`); a `v0.1.0` record keeps its keys and gains no
`host` (`test_status_writes.TestAnOldRecord`). **Not covered, and said in `_update`'s docstring:**
a handler that re-enters between a write taking its number and holding its fields as in flight
loses those fields, never the terminal state; writes from two processes at once are not ordered;
and a process that dies between creating its temporary file and replacing it (`SIGKILL`, or a
handler that restores `SIG_DFL` and kills its own process) leaves one `status.json.<unique>.tmp`,
which nothing reads and nothing removes.

### `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]`

**Opened:** 2026-10-17 by the orchestrator's review of 02, from the note's correction 6 and the
agent's log (observation 1); measured. **Owner:** none.

**Assigned (2026-10-17):** to prompt 02b of this campaign. The user asked for it to be fixed "at the
earliest sensible opportunity"; 02b follows 02 at once, ahead of 03, which touches no part of the
writer. Under L5 as amended the same day (README §6.2): a re-entered write re-applies only the
in-flight writes newer than the landed payload it composes from.

*The defect.* `_write_status` (`runregistrykit/__init__.py:324`) composes a re-entered write from
the newest landed payload, then the fields of **every** earlier write still in flight, then its
own (`:337-345`), as 02's §2.3 step 2 says. A landed write that was itself made inside an earlier
in-flight write already carries that write's fields, and may have set the same keys anew. A third
write then re-applies the oldest in-flight write's fields over it, so a field goes back to an older
value.

*Measured* at `2bf9c72`, 2026-10-17, in one process with `json.dump` patched to make two handler
writes from inside the first write (scratch, not committed):
- a `heartbeat(units_done=7, stage="A")` whose write makes a handler's `heartbeat(stage="B")`
  (which lands) and then a handler's `finish("killed", exit_code=143)` ends `killed`, 143, `stage`
  `A`;
- a `finish("done", exit_code=0)` whose write makes a handler's `finish("killed", exit_code=143)`
  and then a handler's `heartbeat` ends **`done`, 0**: the handler's terminal state is replaced by
  the interrupted write's;
- the same `finish("done")` with one handler write, `finish("killed")`, ends `killed`, 143.

*Impact.* Small. It needs two handler writes inside one write of the same `status.json`, and a
state is lost only when the interrupted write is itself a `finish`, at the very end of a run. No
state goes back to `running` by it, and the file always parses. But 02's §1 asks that the file hold
the handler's state however the handler ends, and a handler that writes twice (a `finish`, then a
print that a driver's stdout tee turns into a heartbeat) is the case where it does not.

*Measured at writing 02b (2026-10-17, at `91e8e9c`).* By a sweep that runs a handler at every
instruction the writer executes (02b's "At writing"), with the interrupted write a `finish("done")`
and the handler's `finish("killed")` followed by a heartbeat: 178 of 202 instructions end other than
`killed` with the handler returning, 157 with it raising. A candidate that applies only the
in-flight writes numbered above the landed base's number leaves none raising, and with the handler
returning only the points before the interrupted write takes its number, where the handler's write
is the earlier and `done` is right. Both measured cases above then end `stage` `B` and `killed`.

*Next step.* Apply an in-flight write's fields only to the keys that no later landed write has set,
which needs the bookkeeping to remember which write set which key (the agent's suggestion); or
compose a re-entered write from the newest landed payload and its own fields alone, once a write
has landed since the oldest in-flight one began. Either is a change to 02's step 2, so it is the
user's to take, with a test of both measured cases.

**Resolved (2026-10-17, by 02b, `2959b78`).** Under L5 as amended (README §6.2), as 02b's §2.2
states it. In `_write_status` (`runregistrykit/__init__.py:352`), a write that composes from the
newest landed payload, numbered `L`, applies only the earlier in-flight writes numbered above `L`
(`:372`). Those at or below `L` were in flight throughout it, so its payload holds their fields
already, and any key it set since is newer. A write whose base is the file applies every earlier
in-flight write, as in 02, and a discarded heartbeat's fields are still kept. The merge needs
sequence numbers to be unique, so a write now takes its number with one call,
`next(book["numbers"])` (`:362`); 02's read-then-increment let a handler take the same number,
which under the new merge loses a later write's fields (02b's log, deviation 2). Pinned by:
- `test_status_writes.TestTwoHandlerWritesInsideOne`: both measured cases, which end `killed`, 143,
  `units_done` 7 and `stage` **B**, and `killed`, 143; and the one-write `finish`, `killed`, 143;
- `test_status_writes.TestAHandlerAtEveryInstruction.test_an_interrupted_finish`: a handler at each
  of the 323 instructions an interrupted `finish("done")` executes in the writer, in four modes.
  Every point ends `killed`, 143, except, with the handler returning, the 24 at or before the
  `CALL` that takes the interrupted write's number, where the handler's write is the earlier and
  `done` is right. At `2bf9c72` the same sweep finds 167 of 212 wrong in both two-write modes.
  Mutation (m1), the merge applying every in-flight write again, fails it (281 of 323) and both
  measured two-write cases.

The log is [`logs/02b-the-writers-bookkeeping.md`](logs/02b-the-writers-bookkeeping.md).

### `[02-the-landed-record-is-unpinned-and-can-move-backwards]`

**Opened:** 2026-10-17 by the orchestrator's review of 02, from its mutation (o2); measured.
**Owner:** none.

**Assigned (2026-10-17):** to prompt 02b of this campaign, with
`[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]`. The user asked for a test; the
measurement below shows the window is reachable as well, so 02b also makes the record one that is
never lowered.

*The defect.* `_land_status` records the write that landed as `book["landed"]` and its payload
(`runregistrykit/__init__.py:321`), and returns early after a put-back (`:318-320`), so the record
never moves to a lower number. Two things leave that unguarded:
- **no test pins it.** With the early `return` removed (the review's (o2)), the record moves back
  to the overtaken write after every put-back, and all 44 tests of `test_status_writes` and
  `test_run_registry` pass;
- **the shipped code has a one-statement window.** A handler that lands a later write between the
  check at `:318` and the record at `:321` is overwritten in the book by the earlier write's number
  and payload. Read, not measured.

*Measured* under (o2), at `2bf9c72`'s tree with the one line removed, 2026-10-17 (scratch, not
committed): a heartbeat whose replace is preceded by a returning handler's `finish("killed")` ends
`killed`, by the put-back. A later heartbeat, re-entered by a handler's `heartbeat`, then composes
from the book's stale `running` payload and lands **`running`** over `killed`. At `2bf9c72` the same
sequence ends `killed`.

*Impact.* At `2bf9c72`, none measured; the window is one statement, and needs a handler to write
twice to matter (once in the window, once later re-entered). Its weight is that a later edit could
drop the `return` and lose a terminal state to `running` with every test passing.

*Measured at writing 02b (2026-10-17, at `91e8e9c`): wider than one statement, and reachable by a
real signal.* The sweep of 02b's "At writing" runs a handler, `finish("killed")` then returning, at
each of the 202 instructions an interrupted heartbeat executes in the writer, then makes a later
heartbeat re-entered by a handler's heartbeat. At 15 instructions the file says `killed` after the
first heartbeat and `running` after the later one. They run from line 318's check to line 321's
call of `copy.deepcopy`, before the store; `copy.deepcopy` is pure Python, and a signal's handler
runs at the instruction boundaries of Python code, so a real signal can land a write there. With
the handler raising, none. A candidate that keeps landed payloads by number, records with one store
after the deep copy, and prunes over a snapshot of the keys leaves none in any mode.

*Next step.* A test of the measured sequence: a put-back, then a later re-entered write, which must
keep the terminal state. And make the record monotonic, for example by recording only a number
higher than the one recorded, or by keeping landed payloads per number and reading the highest.

**Resolved (2026-10-17, by 02b, `2959b78`).** As 02b's §2.3 states it, in the prompt's own shape.
The record of what landed is a dict per book, sequence number → payload, and the newest is its
highest key, read through `_newest_landed` (`runregistrykit/__init__.py:294`). After its replace,
`_land_status` (`:308`) takes its deep copy (`:340`), then checks for a later landed write and
puts it back (`:341-344`, the early `return` kept), then records itself with one store (`:346`),
then prunes the lower keys over a snapshot, `list(landed)` (`:347-349`). Every store adds a key,
and only keys below the one just stored are removed, so a handler that lands a later write at any
instruction leaves its higher key, and the record is never lowered. Pinned by:
- `test_status_writes.TestAPutBackThenALaterReenteredWrite.test_the_terminal_state_is_kept_throughout`:
  the (o2) sequence, a put-back (three replaces) and then a later re-entered heartbeat, `killed`,
  143, `units_done` 8 throughout;
- `test_status_writes.TestAHandlerAtEveryInstruction.test_an_interrupted_heartbeat`: a handler at
  each of the 323 instructions an interrupted heartbeat executes, in four modes, then a later
  heartbeat re-entered by a handler's heartbeat: `killed`, 143 and its `units_done` at every point.
  At `2bf9c72` it finds the 15 measured above in both returning modes. Mutations (m2), the record a
  single number again (24 of 244), (m3′), the put-back's call removed (17 of 323, with five other
  tests), (m4), the prune over the live dict (21 of 334, a `RuntimeError`), and (m5), the prune
  removing higher numbers (22 of 323), each fail it.

**The early `return` after a put-back is kept, and is no longer what keeps the record.** Under the
by-number record, removing it (02b's (m3)) only leaves a dead lower entry beside the put-back's,
which the next prune removes: all 78 tests of `test_status_writes`, `test_run_registry` and
`test_host` pass, both sweeps with 0 wrong in all eight modes. The user's decision of 2026-10-17
took this as a mutant that changes nothing, with (m3′) in its place (02b's log, deviation 1).

The sweeps run in a child process, never signalled: a handler raising at an instruction the
interpreter's exception table leaves uncovered left the writer's lock held in the test process
(02b's log, deviation 3 and observation 1, read and not measured for a real signal; no issue
opened). The log is [`logs/02b-the-writers-bookkeeping.md`](logs/02b-the-writers-bookkeeping.md).
