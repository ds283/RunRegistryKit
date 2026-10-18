# The interrupted-runs campaign: verification

**Campaign:** [`prompts/interrupted-runs/README.md`](../prompts/interrupted-runs/README.md) ·
**Board:** [`prompts/interrupted-runs/IMPLEMENTATION_STATE.md`](../prompts/interrupted-runs/IMPLEMENTATION_STATE.md) ·
**Prompt:** [`prompts/interrupted-runs/07-verification-and-close-out.md`](../prompts/interrupted-runs/07-verification-and-close-out.md) ·
**Log:** [`prompts/interrupted-runs/logs/07-verification-and-close-out.md`](../prompts/interrupted-runs/logs/07-verification-and-close-out.md) ·
**Date:** 2026-10-18

**The package verified** is the release
[`v0.2.0`](https://github.com/ds283/RunRegistryKit/tree/v0.2.0): annotated tag object `895e3c7`,
peeling to commit
[`0bae3a3`](https://github.com/ds283/RunRegistryKit/commit/0bae3a3c501a8264ee4be5bc24f06422af38720f)
(`git ls-remote origin` gives `refs/tags/v0.2.0` `895e3c7013ae…` and `refs/tags/v0.2.0^{}`
`0bae3a3c501a…`). At the commit that adds this document, `git diff 0bae3a3 -- runregistrykit
pyproject.toml` is empty: the package and its metadata are the tag's. Every `path:line` under
`runregistrykit/` below is read at `0bae3a3` (`git show 0bae3a3:<path> | sed -n`); one under `docs/`
is read at the commit that adds this document, whose `docs/extraction/` is `3aab658`'s and whose
`docs/releases/` and `docs/adoption/` are `0bae3a3`'s; one in a client is read through `git show` at
the commit named.

This document is additive from the day it is committed (`CLAUDE.md`, rule 6): a later measurement is
a new subsection, and what is here stays correct for the tree it was taken on.

---

## 1. What this document is

**What the campaign set out to do.** A registry run is the record that a long job exists, and a
long job may be interrupted. SecondaryGWKit (SGK) was about to launch a ~36-hour build under
`v0.1.0`, and reading the package against an interruption it had not rehearsed, beside the
`inherited-issues` board, found five issues that each change how an interrupted run is recorded or
what a person can then do (campaign README §0). They share one design: three judge another run's
liveness by its pid, which is evidence only on that pid's machine and only while it has not been
reused. The campaign took them together, the machine decision first (L1–L4), within the boundary
that the registry records and **does not decide that a run is dead** (README §0, §1, §6.1).

**What it delivered**, each re-measured below:

- **Five issues resolved**, the five assigned from `inherited-issues` on 2026-10-16: the host and
  boot recorded and judged by (01), `status.json` writes safe under a signal handler (02), an
  unreadable status counted as in use (03), `python -m runregistrykit end` (04), and `begin`
  refusing a store an unfinished run names (05). **Three more were found and resolved along the
  way**: two in the status writer's bookkeeping, opened by 02's review and closed by 02b, and a pid
  out of range, opened by 04 and closed by 05. A fourth, the writer's lock left held by a raising
  handler, opened by 02b's review, was fixed at Python 3.12 and 3.13 by 02c and narrowed to its 3.14
  `with` point, where it stays open (§6).
- **One release, `v0.2.0`** (`0bae3a3`), tagged after CI run
  [`39143681701`](https://github.com/ds283/RunRegistryKit/actions/runs/39143681701) passed all three
  jobs on that commit (§2.2). Installed **as a client installs it**, from GitHub, at both tested
  ends and in the core-only form, it is `0bae3a3`'s five modules byte for byte and ships no test
  (§5).
- **The suite at both ends**: `Ran 410 tests … OK (skipped=1)` in `venv/` (Python 3.12.15, Ray
  2.43.0, SQLAlchemy 2.0.39) and in a fresh high-end venv (3.13.16, 2.55.1, 2.0.46), the same 410 by
  module, the one skip the Linux readers in both; `test_status_writes` at 3.14.8, 22 tests, OK, no
  skip (§3).
- **The hard-kill route from the GitHub pin**: a script,
  [`docs/interrupted-runs/interrupted_run_smoke.py`](interrupted-runs/interrupted_run_smoke.py),
  hard-kills a run, meets the refusals that name `end`, has `end` refuse a live pid, ends a run by a
  real `SIGTERM`, ends the hard-killed run with `end`, resumes on its store and fingerprints it:
  thirteen steps pass at both ends against the installed pin, in 3.8 s and 6.3 s, Ray never
  started and no child left; and it fails where it should, in three deliberate breakages (§4).
- **Six issues open** at the close, each with no owner (§6).

**What remains**: G1–G3, the three clients' adoptions, none made (SGK is pinned at `v0.1.0`); and
what this campaign could not verify (§10).

---

## 2. Reconciliation

### 2.1 Git history

`main` holds **44 commits** from `b56ecc7` (the plan) to `e4bf592`, the commit before 07's own
(`git rev-list --count b56ecc7^..e4bf592` is 44). Each is in one class, by its subject's form and
then by reading it, counted by script (`git log --reverse --format='%h %s' b56ecc7^..e4bf592`; log
of 07, "Verification performed", §9):

| Class | Commits | Count |
|---|---|---|
| The plan | `b56ecc7` | 1 |
| A prompt written, with the decisions it recorded | `1fd8e1c`, `34afe6d`, `5ed97a5`, `149918f`, `069f1d7`, `88f93c3`, `c3aa52a`, `f3cc239`, `7f88787`, `c094811` | 10 |
| An orchestration note | `8023e14`, `b52cc01`, `201e507`, `e4a2b6c`, `75eab12`, `5d8a97b`, `5d0fa78`, `c4f2abc`, `e4bf592` | 9 |
| A prompt's own commit | `387c58f`, `2bf9c72`, `2959b78`, `35ce264`, `ab0cad9`, `5e20772`, `eb68583`, `0bae3a3` | 8 |
| An orchestrator's review | `5d71a6b`, `a38022f`, `c18ec34`, `31933c4`, `4b55750`, `46e29b9`, `4a10efb`, `74f85a2` | 8 |
| A CI or tag record | `c2911d3`, `91e8e9c`, `9d26357`, `0c75dd3`, `9e38581`, `d8f8de4`, `80974e2`, `aeacba8` | 8 |
| | | **44** |

The prompt's §1.3 counts 42, to `aeacba8`; the two after it are 07's writing (`c094811`) and 07's
orchestration note (`e4bf592`), both on `main` before 07's own commit. 02c has two writing commits,
`149918f` (the prompt) and `069f1d7` (L11 taken). 07's commit is the 45th; the orchestrator's review
of 07 follows it and is not counted here. The orchestration notes are cited by commit only, as the
board's notes line names them.

| Prompt | Written | Note | Commit | Review | CI run (on) and record | Suite after | Closed or opened |
|---|---|---|---|---|---|---|---|
| 01 | `1fd8e1c` | `8023e14` | `387c58f` | `5d71a6b` | `38911075984` (`5d71a6b`); `c2911d3` | 307 | closed `[04-runs-do-not-say-which-machine-produced-them]` |
| 02 | `34afe6d` | `b52cc01` | `2bf9c72` | `a38022f` | `39049728089` (`a38022f`); `91e8e9c` | 322 | closed `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`; its review opened `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]` and `[02-the-landed-record-is-unpinned-and-can-move-backwards]` |
| 02b | `5ed97a5` | `201e507` | `2959b78` | `c18ec34` | `39060913296` (`c18ec34`); `9d26357` | 328 | closed both of 02's review's; its review opened `[02b-a-raising-handler-can-leave-the-status-lock-held]` |
| 02c | `149918f`, `069f1d7` | `e4a2b6c` | `35ce264` | `31933c4` | `39072902589` (`31933c4`); `0c75dd3` | 329 | narrowed `[02b-a-raising-handler-can-leave-the-status-lock-held]` to Python 3.14 (L11 (a)) |
| 03 | `88f93c3` | `75eab12` | `ab0cad9` | `4b55750` | `39083674030` (`4b55750`); `9e38581` | 347 | its writing opened `[03-a-run-whose-manifest-cannot-be-read-names-no-store]`; closed `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]`; its work opened `[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]`; its review opened `[03-store-show-raises-on-a-state-that-is-a-list-or-an-object]` |
| 04 | `c3aa52a` | `5d8a97b` | `5e20772` | `46e29b9` | `39122974980` (`46e29b9`); `d8f8de4` | 378 | its writing opened `[04-a-killed-process-not-yet-reaped-answers-kill-0]`; closed `[a3-v2-a-hard-killed-run-blocks-its-store]`; its work opened `[04-a-pid-out-of-range-makes-pid-alive-raise]` |
| 05 | `f3cc239` | `5d0fa78` | `eb68583` | `4a10efb` | `39129061916` (`4a10efb`); `80974e2` | 410 | closed `[00-begin-does-not-refuse-a-second-writer]` and `[04-a-pid-out-of-range-makes-pid-alive-raise]` |
| 06 | `7f88787` | `c4f2abc` | `0bae3a3` | `74f85a2` | `39143681701` (`0bae3a3`) and `39144321994` (`aeacba8`); `aeacba8`, with the tag | 410 | `v0.2.0` tagged on it; its review opened `[06-three-store-docstrings-and-a-comment-state-the-old-in-use-rule]` |
| 07 | `c094811` | `e4bf592` | this document's | — | — | 410 | nothing; closes the campaign |

The suite went 276 (at `79015a7`, extraction 08's count) → 307 → 322 → 328 → 329 → 347 → 378 →
410 → 410 → 410, each count the board's §1 and each log's own "before and after"; 07 changes no
test.

### 2.2 The tag and CI

- **The tag.** `v0.2.0`, annotated, tag object `895e3c7`, on `0bae3a3` (`git ls-remote origin`,
  above; here `git rev-parse v0.2.0^{}` gives the same). It was made after
  [run 39143681701](https://github.com/ds283/RunRegistryKit/actions/runs/39143681701) passed on
  `0bae3a3`, pushed alone (board, 06's review, "CI and the tag").
- **CI**, read with `gh run view <id> --json databaseId,headSha,status,conclusion,event,jobs`
  (nothing written): ten runs since 01, each a `push`, each `completed`/`success` in all three jobs,
  `core (no store layer)`, `suite (low)` and `suite (high)`:

  | Run | Commit |
  |---|---|
  | [38911075984](https://github.com/ds283/RunRegistryKit/actions/runs/38911075984) | `5d71a6b` (01's review) |
  | [38929845135](https://github.com/ds283/RunRegistryKit/actions/runs/38929845135) | `c2911d3` (01's CI record) |
  | [39049728089](https://github.com/ds283/RunRegistryKit/actions/runs/39049728089) | `a38022f` (02's review) |
  | [39060913296](https://github.com/ds283/RunRegistryKit/actions/runs/39060913296) | `c18ec34` (02b's review) |
  | [39072902589](https://github.com/ds283/RunRegistryKit/actions/runs/39072902589) | `31933c4` (02c's review) |
  | [39083674030](https://github.com/ds283/RunRegistryKit/actions/runs/39083674030) | `4b55750` (03's review) |
  | [39122974980](https://github.com/ds283/RunRegistryKit/actions/runs/39122974980) | `46e29b9` (04's review) |
  | [39129061916](https://github.com/ds283/RunRegistryKit/actions/runs/39129061916) | `4a10efb` (05's review) |
  | [39143681701](https://github.com/ds283/RunRegistryKit/actions/runs/39143681701) | `0bae3a3` (06, the tag's) |
  | [39144321994](https://github.com/ds283/RunRegistryKit/actions/runs/39144321994) | `aeacba8` (06's CI and tag record) |

  The commits from `c094811` on are not pushed; `origin/main` is `aeacba8`.

### 2.3 The environment of every measurement below

- macOS 27.0.1 (`arm64`), `git` 2.56.0, `uv` 0.12.20 (`/opt/local/bin/uv`), interpreters
  `/opt/local/bin/python3.12` (3.12.15), `python3.13` (3.13.16) and `python3.14` (3.14.8). The shell
  had `PYTHONDONTWRITEBYTECODE=1` and no `RAY_ADDRESS`.
- **`venv/`**, this repository's: Python 3.12.15, `runregistrykit` 0.2.0 editable from this
  checkout, `datastorekit` 0.4.0 from `c8570e8` (its `v0.4.0`), Ray 2.43.0, SQLAlchemy 2.0.39,
  `black` 25.1.0. The suite (low end) and `black` ran here.
- **The high-end suite venv**: a fresh 3.13.16 `uv` venv with a `git clone` of this repository at
  `e4bf592` installed editable with the extra, `datastorekit` from `v0.4.0`, Ray 2.55.1, SQLAlchemy
  2.0.46; the suite run from the clone's root, so that the package, the tests and the work tree are
  one. `test_status_writes` at 3.14.8 ran from the same clone, by `PYTHONPATH`.
- **The three pin venvs** (§5): fresh `uv` venvs, `--no-cache`: low (3.12.15, Ray 2.43.0,
  SQLAlchemy 2.0.39), high (3.13.16, 2.55.1, 2.0.46), core (3.12.15, the core form alone). The two
  smoke scripts ran in these.
- `TMPDIR` named a directory in the session's scratchpad for every command that could make a
  temporary file. No Ray process was up before or after any suite or smoke run (`pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` found none, every time).

---

## 3. Each prompt's acceptance, at `v0.2.0`

The suite's counts per module are the loader's (`unittest.defaultTestLoader.discover` with `-t .`),
the same in `venv/` and at the high end: `test_client_root` 27, `test_end` 27, `test_end_stores` 4,
`test_fingerprinter` 31, `test_host` 28, `test_host_stores` 3, `test_package_imports` 3,
`test_package_is_generic` 22, `test_public_names` 8, `test_run_registry` 29, `test_second_writer` 23,
`test_second_writer_stores` 9, `test_status_writes` 22, `test_store_amend` 21,
`test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
`test_store_fingerprint` 29, `test_store_retire` 41, `test_store_retire_references` 10,
`test_store_sidecar` 17, `test_unreadable_status` 11, `test_unreadable_status_stores` 7; 410. The one
skip in each is `test_host.TestTheReaders.test_the_readers_on_linux`.

| Prompt | Acceptance, in brief (README §2 and the prompt) | What its review found | At `v0.2.0`, and how re-measured here |
|---|---|---|---|
| 01 | The host and boot recorded in the manifest and `status.json`; a record from another host never judged by `kill -0`; one with no `host` judged as before and counted | Every check passed; nothing opened; CI ran the Linux readers (board, 01's review) | **Holds.** `test_host` 28 and `test_host_stores` 3 OK at both ends. The smoke run's step 2 finds the hard-killed run's status `host` exactly `{boot, id}`, each recorded, and step 13 the resumed run's manifest `host.id` equal to its status's (§4). Another host and an earlier boot are measured only by the suite's records (§10) |
| 02 | `status.json` through a temporary name of its own; a superseded write discarded; the reproduction leaves the terminal state, the handler raising or returning | Every check passed; two issues opened (board, 02's review) | **Holds.** `test_status_writes` 22 OK at both ends and at 3.14.8 (its three real-signal children among them). The smoke run's step 7: a real `SIGTERM` to a child heartbeating in a tight loop, its handler recording `killed` and raising `SystemExit(143)`: returncode 143, the status parses, `killed`, 143, and no `status.json.*.tmp` left, at both ends |
| 02b | Only newer in-flight writes re-applied; the landed record never lowered; both sweeps keep the terminal state | Every check passed; one issue opened, measured at 3.13 (board, 02b's review) | **Holds.** `TestAHandlerAtEveryInstruction` and the measured cases pass in `test_status_writes` at both ends and at 3.14.8. Not otherwise re-measured: the sweep is the measurement |
| 02c | The writer's filters generator expressions; a sweep at every `JUMP_BACKWARD` leaves the lock free at 3.12, 3.13 and 3.14 | Every check passed; the issue narrowed to 3.14 (board, 02c's review) | **Holds.** `TestARaisingHandlerAtEveryJump.test_the_lock_is_free_and_nothing_is_in_flight` passes at 3.12.15 and 3.13.16 (the two suite runs) and at 3.14.8 (`Ran 22 tests`, `OK`, no skip). That pass is 02c's sweep at the writer's jumps; it says nothing about L11's `with` window, which the sweep cannot model (§10) |
| 03 | A run whose status does not say it has finished counted as in use by copy, move, fingerprint, retire and amend, for thirteen forms; `list` marks it `!!` | Every check passed; one issue opened (board, 03's review) | **Holds.** `test_unreadable_status` 11 and `test_unreadable_status_stores` 7 OK at both ends. The smoke run makes no unreadable status; not re-measured beyond the suite |
| 04 | A child begun on a store, `SIGKILL`'d, then `end`, then every store operation and a resumed run's fingerprint succeeding; `end` refused for a live pid, another host and a run already ended | Every check passed; nothing opened, two test gaps recorded (board, 04's review) | **Holds, from the GitHub pin.** `test_end` 27 and `test_end_stores` 4 OK at both ends. The smoke run's steps 2–4 and 8–12 at both ends: the hard-killed child stale, `!!`, `store fingerprint` refused naming `end`; `end` without `--reason` exit 2, with it exit 0, `lost`, `exit_code` null, verified, `pid_answers` false; a second `end` refused; then the resume's fingerprint, `store fingerprint` and `store retire --dry-run` exit 0. Step 6: a live pid refused, with and without `--unverified`. Another host is not re-measured (§10) |
| 05 | A second `begin` refused on a live, stale, `foreign` and unreadable run's store with no run directory left; all-terminal accepted; a hard-killed run ended, then `begin` accepted and its fingerprint recorded | Every check passed; nothing opened, one test gap recorded (board, 05's review) | **Holds, from the GitHub pin.** `test_second_writer` 23 and `test_second_writer_stores` 9 OK at both ends. The smoke run's step 5 at both ends: `begin` on the hard-killed run's store raises `RuntimeError` naming it and `python -m runregistrykit end`, ending `No run directory was created`, the runs root's listing unchanged; step 11: after `end`, `begin` accepted and its fingerprint recorded |
| 06 | `pyproject.toml` at `0.2.0`; the README, release notes and adoption notes; CI green; `v0.2.0` tagged | Every check passed but one gap; one issue opened (board, 06's review) | **Holds.** The ten CI runs (§2.2); the pin installs from GitHub at both ends and in the core form, its `commit_id` `0bae3a3`, its five modules `0bae3a3`'s and no test in it (§5). `./venv/bin/black --check runregistrykit docs`: 38 files unchanged (37 and the smoke script). The route the adoption notes give for a hard-killed run (`docs/adoption/v0.2.0/README.md:92-108`) is the one §4 drives, step for step |

---

## 4. An interrupted run from the GitHub pin

### 4.1 The script

[`docs/interrupted-runs/interrupted_run_smoke.py`](interrupted-runs/interrupted_run_smoke.py)
imports the standard library and `runregistrykit`, and nothing of `runregistrykit.tests`. It takes
the client root's files, `CONFIG`, `GITIGNORE`, `JOB` and `REGISTRY_SOURCE`, from
[`docs/extraction/store_smoke_run.py`](extraction/store_smoke_run.py), loaded by its path with
`importlib.util.spec_from_file_location` (its `main` is guarded, so nothing of it runs but its
definitions, and no bytecode cache is written beside it), and changes nothing in that file. It
makes a directory with `tempfile` and in it a client root, a git repository with one commit holding
`runregistrykit.toml` (`[stores] fingerprinter = "smoke_registry:FINGERPRINTER"`), `.gitignore`,
`job.py` and `smoke_registry.py`, whose `write_store` writes a closed store of two shards.

**Every process it starts runs in the client root, with `PYTHONPATH` unset**, never in this
repository, so that each imports the release the interpreter has installed. The script prints its
own `runregistrykit.__file__`, what a command run in the client root imports, and each child's,
and checks that all are one file under the interpreter's `site-packages`; run with this checkout
importable instead (`venv/`'s editable install), it runs its steps and ends `RESULT: FAIL
(site-packages)`, exit 1 (log of 07). It runs each command as `sys.executable -m runregistrykit …`,
prints `PASS` or `FAIL` per step with the commands, their exit codes and the lines that show the
outcome, and exits 0, 1 or 2. Its two children are its own: step 2's, which begins a run on the
store and heartbeats every 0.1 s until it is killed, and step 6's, which begins a run on a second
store (named, never written), installs a `SIGTERM` handler that calls `run.finish("killed",
exit_code=128 + signum)` and raises `SystemExit(128 + signum)`, and heartbeats in a tight loop. Each
says on one line, read with a 30 s timeout, that it has begun. A `finally` kills and reaps any child
still alive, or reaps one that has exited, and says which. Its docstring gives the thirteen steps.

Run, from this repository's root, in each pin venv (§5):

```bash
TMPDIR=<scratch>/tmp/smoke-low  <scratch>/pin-low/bin/python  docs/interrupted-runs/interrupted_run_smoke.py
TMPDIR=<scratch>/tmp/smoke-high <scratch>/pin-high/bin/python docs/interrupted-runs/interrupted_run_smoke.py
TMPDIR=<scratch>/tmp/smoke-core <scratch>/pin-core/bin/python docs/interrupted-runs/interrupted_run_smoke.py
```

### 4.2 At both ends

**Exit 0 at both ends**, `RESULT: OK (13 steps passed)`; 3.8 s at the low end and 6.3 s at the high
end (the script's own clock; `time -p` real 4.49 s and 6.94 s). No Ray process before or after
either run, and in each the script's last check found `ray` imported (by `datastorekit`) and **not
initialised**. The user's `python` processes (`ps -o pid,ppid,stat,command -U <uid>`) were the same
six before and after each run, none of them a run's (log of 07). The low end's output, whole, the
scratchpad's path written `<scratch>`:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.2.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
client files    from /Users/ds283/Documents/Code/RunRegistryKit/docs/extraction/store_smoke_run.py
directory       $SMOKE = <scratch>/tmp/smoke-low/interrupted-smoke-zmkbcwlr
its commands    import <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
site-packages   <scratch>/pin-low/lib/python3.12/site-packages: the package is under it

PASS step 1: a store written by the client's module, and `store create --purpose`
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id ae3a93fd6d504f5bab9ca02fea00fa31
PASS step 2: a hard kill: a child begun on the store, heartbeating, sent SIGKILL and reaped
  started the hard-killed run's child: pid 46981
    > run smoke-02-hard-killed-20261018T181347, pid 46981
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  sent SIGKILL to pid 46981
    > reaped: returncode -9
    > status: state running, pid 46981, units_done 1, host keys ['boot', 'id'], host.id 8d2b247824882486, host.boot <36 characters>
    > liveness(status, 900): stale
PASS step 3: `list`: the hard-killed run marked `!!`, and stderr naming `end`
  $ python -m runregistrykit list   (in client/)
    exit 0
    > !! smoke-02-hard-killed-20261018T181347  running         1/?       1s  a smoke run that is hard-killed  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 stale; 0 with no host recorded.
    > !! 1 run(s) say they are running and are not: the pid does not answer kill -0, the heartbeat is older than 900 s, or this machine has rebooted since. Nothing here has killed or cleaned anything — go and look. Once you know one is over, end it with `python -m runregistrykit end RUN_ID --reason TEXT`.
PASS step 4: `store fingerprint` refused, naming the run and `end`
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    > !! Cannot fingerprint "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181347 is running (stale, pid 46981) and names this store by its results and results_store_id. A fingerprint of a store that is being written describes no instant; a stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, first. Nothing was read or written
PASS step 5: a second `begin` on the store refused, with no run directory made
  begin(): RuntimeError: Cannot begin run smoke-05-second-20261018T181347 with results "$SMOKE/client/var/datastores/smoke-store.sqlite": run smoke-02-hard-killed-20261018T181347 is running (stale, pid 46981) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
    > runs root before: ['smoke-02-hard-killed-20261018T181347']
    > runs root after:  ['smoke-02-hard-killed-20261018T181347']
PASS step 6: a live pid refused by `end`, with and without `--unverified`
  started the signalled run's child: pid 47001
    > run smoke-06-signalled-20261018T181347, pid 47001
    > its runregistrykit: <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
  $ python -m runregistrykit end smoke-06-signalled-20261018T181347 --reason the smoke run tries to end a live run   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181347: its pid 47001 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
  $ python -m runregistrykit end smoke-06-signalled-20261018T181347 --reason the smoke run tries to end a live run --unverified   (in client/)
    exit 1
    > !! Cannot end smoke-06-signalled-20261018T181347: its pid 47001 answers kill -0, so a process with that pid exists on this host, and a run whose process may be alive is not ended; --unverified does not override this. A process that was killed and not yet reaped by its parent (a zombie) answers kill -0 too, until its parent waits for it or exits. Nothing was written
    > status: state running, ended absent, exit_code None, pid 47001
PASS step 7: a real SIGTERM: the child's handler records `killed`, 143, and exits
  sent SIGTERM to pid 47001
    > reaped: returncode 143
    > status: parses, state killed, exit_code 143
    > temporary files left: none
PASS step 8: `end` of the hard-killed run: no `--reason` refused by argparse, then the run `lost`
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181347   (in client/)
    exit 2
    > usage: runregistrykit end [-h] --reason TEXT [--unverified] [--root DIR]
    > runregistrykit end: error: the following arguments are required: --reason
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181347 --reason the smoke run's child was sent SIGKILL by the script   (in client/)
    exit 0
    > >> end: smoke-02-hard-killed-20261018T181347 is now lost, verified: its pid 46981 does not answer kill -0 on this host
    > status: state lost, exit_code None, ended.verified True, ended.evidence.pid_answers False, ended.reason "the smoke run's child was sent SIGKILL by the script"
PASS step 9: `end` of the hard-killed run again: refused, it has already ended
  $ python -m runregistrykit end smoke-02-hard-killed-20261018T181347 --reason the smoke run ends it twice   (in client/)
    exit 1
    > !! Cannot end smoke-02-hard-killed-20261018T181347: its status says it has already ended, as 'lost'; end records only a run whose end the registry never saw. Nothing was written
PASS step 10: `list`: the run `lost`, unmarked, and every run counted finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    >    smoke-02-hard-killed-20261018T181347  lost            1/?       2s  a smoke run that is hard-killed  · working
    > 2 run(s) under $SMOKE/client/var/runs: 2 finished; 0 with no host recorded.
PASS step 11: the resume: `begin` on the store accepted, and its fingerprint recorded
  begin(): smoke-11-resumed-20261018T181348
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
PASS step 12: `store fingerprint` matching, and `store retire --dry-run`, each exiting 0
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > digest:   e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > recorded: matches the fingerprint taken 2026-10-18T18:13:48+01:00 by run smoke-11-resumed-20261018T181348, at c5d5b134b45cae34f83d1fed9f4491a05b28b545
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-store.sqlite --reason the smoke run checks the store could be retired --dry-run   (in client/)
    exit 0
    > dry run:  nothing was written or deleted
PASS step 13: the resumed run's manifest `host.id` recorded, and its status's
    > manifest host.id 8d2b247824882486, status host.id 8d2b247824882486

children: 2 started; each reaped by its step
ray: imported, initialised: False
time: 3.8 s
left in place: <scratch>/tmp/smoke-low/interrupted-smoke-zmkbcwlr
RESULT: OK (13 steps passed)
```

`host.id` is the digest the registry writes, never the machine's identity; the boot is shown by its
length only. **The high end's output** differs from it, by `diff`, only in the versions and paths of
its first nine lines (Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46, the `pin-high` venv), the new
`store_id`, the pids, the run ids and their timestamps, the commit of the client root (made fresh
each run), the time of the fingerprint, the time (6.3 s) and the directory left in place. The
fingerprint's digest, `e56c6922…`, is the same at both ends, and the same as the extraction's smoke
run gives at `v0.1.0` (`docs/extraction-verification.md`, §4.2) and at `v0.2.0` (§5.2): the client's
module and its store are the same.

Each text the run shows is the code's at `0bae3a3`: `begin`'s refusal
(`runregistrykit/__init__.py:1108-1126`), `_end_run`'s "already ended" (`:1327-1331`) and live-pid
refusals (`:1349-1356`), `end`'s success line (`runregistrykit/__main__.py:470`), `list`'s summary
and stale line (`:660-672`), and `fingerprint_store`'s refusal (`runregistrykit/stores.py:1405-1415`).

### 4.3 The breakage

Each is exactly what was run: (a) and (b) as diffs to the committed script, checked with `git apply
--check`, applied with `git apply` in a scratch clone of this repository holding the script, run
there in the low pin venv, then checked with `git apply -R --check`, reversed, and the file compared
with the committed one; (c) the committed script in the core pin venv. The diffs are in 07's log,
"The deliberate-breakage record". In each, no Ray process before or after, and the user's `python`
processes the same before and after.

- **(a) `end` skipped**: step 8 removed from the steps run. Exit 1, `RESULT: FAIL (9, 10, 11, 12,
  13)`, 2.7 s. Steps 1–7 pass as at both ends. **Step 11's `begin` is refused**, its `RuntimeError`
  naming the hard-killed run, `is running (stale, pid …)`, and `python -m runregistrykit end`;
  **step 12's `store fingerprint` is refused**, exit 1, naming the same run. Step 9 fails first on
  its own precondition (it ends nothing that step 8 did not: "expected the run lost by step 8,
  before it is ended again; saw running"), step 10 finds the run's row `!!`, `running`, and the
  summary `1 finished, 1 stale`, and step 13 has no resumed run. Each failure is the run left
  unended.
- **(b) the hard-killed child not reaped before `end`**: step 2's reap moved to the end of step 8.
  Exit 1, `RESULT: FAIL (2, 3, 8, 9, 10, 11, 12, 13)`, 2.8 s. This is
  `[04-a-killed-process-not-yet-reaped-answers-kill-0]`, measured against the release. Before the
  reap, the killed child is a zombie and answers `kill -0`, and its heartbeat is fresh, so:
  - step 2: `liveness(status, 900)` is **`alive`**, where it should be `stale` (state `running`,
    `host` `{boot, id}`);
  - step 3: `list`'s row is **unmarked**, `running`, and the summary `1 alive; 0 with no host
    recorded.`, with no stale line on stderr;
  - step 8: `end` without `--reason` still exits 2; **`end` with it exits 1**: "its pid … answers
    kill -0, so a process with that pid exists on this host … A process that was killed and not yet
    reaped by its parent (a zombie) answers kill -0 too". The step stops there, before the moved
    reap, so the child is reaped by the `finally`: "reaped pid …, which had exited (returncode -9)";
  - steps 9–13 fail because the run was never ended: 9 on its precondition, 10 on the row
    (`running`; the summary `1 alive, 1 finished`), 11 and 12 refused (`is running (alive, pid …)`),
    13 with no resumed run.

  Steps 4 and 5 pass: the store refusal and `begin`'s each count the zombie's run as in use, and
  each names `end` in its stale sentence whatever the run's liveness.
- **(c) the core-only venv** (§5): no `datastorekit`, Ray or SQLAlchemy. Exit 1, `RESULT: FAIL (1,
  11, 12)`, 2.3 s; `ray` never imported; no exception escaped a step; both children reaped by their
  steps. Step by step:

  | Step | Needs the client's module (a store or the fingerprinter) | Verdict, and what it saw |
  |---|---|---|
  | 1 | yes: its `write_store` | FAIL: `ModuleNotFoundError: No module named 'sqlalchemy'` (`smoke_registry.py:7`), caught by the step |
  | 2 | no: `begin` with `results` reads the sidecar, absent here | PASS: the child begun on the absent store, killed, reaped (−9), `running`, `stale` |
  | 3 | no | PASS: `!!`, and the stale line naming `end` |
  | 4 | no: the in-use check comes before the fingerprinter is loaded (`stores.py:1405-1418`) | PASS: refused, exit 1, the run named "by its results" only (no sidecar, so no store id) |
  | 5 | no | PASS: refused, no directory made |
  | 6, 7 | no | PASS: the live pid refused twice; `SIGTERM`, 143, `killed` |
  | 8, 9, 10 | no | PASS: `end` exit 2 then 0, `lost`; refused again; `list` `2 finished` |
  | 11 | yes: `finish(fingerprint=True)` loads the fingerprinter | FAIL: `done`, exit code 0, `fingerprint_sidecar` absent and `fingerprint_error` the loader's `ConfigError` naming the module that could not be imported (`No module named 'sqlalchemy'`) |
  | 12 | yes: `store fingerprint` loads it | FAIL: exit 1, the same `ConfigError` |
  | 13 | no: the manifest and status only | PASS |

  So the hard-kill route itself, `end` and `begin`'s refusal among it, needs only the core.

The script also exits **2** when it cannot start: with `PATH=/nonexistent` ("CANNOT START: no git on
PATH"); under `/opt/local/bin/python3.12 -I`, which has no package ("CANNOT START: runregistrykit is
not importable (No module named 'runregistrykit')"); and copied alone into a scratch directory
("CANNOT START: the extraction's smoke script is not at …").

---

## 5. The release from GitHub

### 5.1 The installs

Each into a fresh venv made with `uv venv --python <interpreter>`, `TMPDIR` in the scratchpad, so
that the tag was fetched from GitHub and nothing was reused from `uv`'s cache:

```bash
uv pip install --no-cache --python <scratch>/pin-low/bin/python \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.43.0' 'sqlalchemy==2.0.39'
uv pip install --no-cache --python <scratch>/pin-high/bin/python \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
uv pip install --no-cache --python <scratch>/pin-core/bin/python \
  'runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.2.0'
```

| Venv | Python | Resolved | `runregistrykit` | `datastorekit` | Ray / SQLAlchemy | Time (`time -p` real) |
|---|---|---|---|---|---|---|
| low | 3.12.15 | 23 packages | 0.2.0, from `0bae3a3c501a…` | 0.4.0, from `c8570e849334…` | 2.43.0 / 2.0.39 | 5.99 s |
| high | 3.13.16 | 21 packages | 0.2.0, from `0bae3a3c501a…` | 0.4.0, from `c8570e849334…` | 2.55.1 / 2.0.46 | 5.78 s |
| core | 3.12.15 | 1 package | 0.2.0, from `0bae3a3c501a…` | not installed | not installed | 3.48 s |

`uv` reported each tag's commit as it fetched it (`Updated https://github.com/ds283/RunRegistryKit
(0bae3a3c501a8264ee4be5bc24f06422af38720f)`; DatastoreKit `c8570e849334d09085bbd84876095fc9e22bd005`,
its [`v0.4.0`](https://github.com/ds283/DatastoreKit/tree/v0.4.0)).

**What was installed**, read in each venv by a scratch script run with `-I` from an empty directory:

- `importlib.metadata`: `runregistrykit` 0.2.0, `runregistrykit.__file__` under the venv's
  `site-packages`, `requires` `['datastorekit>=0.4.0; extra == "stores"']`; in the core venv
  `find_spec` finds none of `datastorekit`, `ray` and `sqlalchemy`.
- `direct_url.json`, the same in all three: `{"url":"https://github.com/ds283/RunRegistryKit",
  "vcs_info":{"vcs":"git","commit_id":"0bae3a3c501a8264ee4be5bc24f06422af38720f",
  "requested_revision":"v0.2.0"}}`.
- **The five modules equal `0bae3a3`'s byte for byte** in all three venvs (`git show
  0bae3a3:runregistrykit/<module> | cmp - <site-packages>/runregistrykit/<module>`, each silent):
  `__init__.py`, `__main__.py`, `client.py`, `fingerprint.py`, `stores.py`.
- **No tests.** The installed `RECORD` has 14 entries, the five modules and nine under
  `runregistrykit-0.2.0.dist-info/` (`INSTALLER`, `METADATA`, `RECORD`, `REQUESTED`, `WHEEL`,
  `direct_url.json`, `licenses/LICENSE`, `top_level.txt`, `uv_build.json`); none names `tests`
  (`grep -c tests` gives 0); `import runregistrykit.tests` raises `ModuleNotFoundError`.

### 5.2 The extraction's smoke run, against `v0.2.0`

[`docs/extraction/store_smoke_run.py`](extraction/store_smoke_run.py), unchanged since `3aab658`, run
from this repository's root in the low and high pin venvs: **10 of its 11 steps pass at both ends,
and step 3 fails at both**; exit 1, `RESULT: FAIL (3)`, 11.0 s and 10.5 s. No Ray process before or
after; `ray: imported, initialised: False`; the digest `e56c6922…` in `status.json` and from `store
fingerprint`, at both ends, as at `v0.1.0`. Its step 3, at the low end, whole:

```text
FAIL step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261018T180447  done            1/1       0s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished; 0 with no host recorded.
  !! expected the summary '1 run(s) ... 1 finished.'; saw 1 run(s) under $SMOKE/client/var/runs: 1 finished; 0 with no host recorded.
```

**Why.** The step asserts that `list`'s summary contains `1 finished.`
(`docs/extraction/store_smoke_run.py:484-488`), which `v0.1.0` printed. `v0.2.0` prints the clause
01 added, `; N with no host recorded.` (`runregistrykit/__main__.py:660-663`; 01's log, "What `list`
prints"; the release notes' §5, `docs/releases/v0.2.0.md:267-269`), so the line ends `1 finished; 0
with no host recorded.`. The run is listed, `done`, `1 finished`: the package is right, and so is the
script, for `v0.1.0`, the tree it was written against. The script is not changed (`CLAUDE.md`, rule
6); this interrupted-run script covers the store layer that the hard-kill route touches. Every other
step, `store create`, a fingerprinted run, `store show`, `fingerprint`, `copy`, `move`, `amend`,
`adopt`, `retire`, a worktree run and the two refusals, passes against `v0.2.0` at both ends.

---

## 6. Issues

Fourteen were on this board: **five assigned** from `inherited-issues` on 2026-10-16, all five
resolved; and **nine opened** during the campaign, two by 02's review, one by 02b's review, one at
03's writing, one by 03's work, one by 03's review, one at 04's writing, one by 04's work and one by
06's review. **Eight are resolved** (board §4) and **six are open** (board §3), each with no owner.
The index counts 11: these six, two on the closed `extraction` board and three on
`inherited-issues`.

**Resolved**, each with the prompt and commit that closed it and what guards it (board §4, each
entry's "Pinned by"):

| Issue | Opened | Closed | Guarded by |
|---|---|---|---|
| `[04-runs-do-not-say-which-machine-produced-them]` | SGK, 2026-09-24; assigned | 01, `387c58f` | `test_host`'s `TestAnOldRecord`, `TestTheJudgement`, `TestTheReaders`, `TestWhatIsWritten`, `TestTheCommandLine`; `test_host_stores.TestARunOnAnotherHostIsInUse` |
| `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` | SGK, 2026-10-03; assigned | 02, `2bf9c72` | `test_status_writes`' `TestAHandlerInsideAHeartbeat`, `TestASecondRunObject`, `TestAHandlerDuringThePutBack`, `TestARealSignal`, `TestTwoThreads`, `TestThePlainWrite`, `TestAnOldRecord` |
| `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]` | 02's review, `a38022f` | 02b, `2959b78` | `test_status_writes.TestTwoHandlerWritesInsideOne`; `TestAHandlerAtEveryInstruction.test_an_interrupted_finish` |
| `[02-the-landed-record-is-unpinned-and-can-move-backwards]` | 02's review, `a38022f` | 02b, `2959b78` | `test_status_writes.TestAPutBackThenALaterReenteredWrite`; `TestAHandlerAtEveryInstruction.test_an_interrupted_heartbeat` |
| `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` | here, 2026-10-16; assigned | 03, `ab0cad9` | `test_unreadable_status_stores.TestAnUnreadableStatusIsInUse` (thirteen forms, six operations); `test_unreadable_status`' `TestTheLister`, `TestLiveness`, `TestTheRemedy`, `TestTheListCommand`, `TestAnOldRecord` |
| `[a3-v2-a-hard-killed-run-blocks-its-store]` | SGK, 2026-10-16; assigned | 04, `5e20772` | `test_end_stores.TestEndingAHardKilledRun`, `TestTheWords`; `test_end`'s eight classes; and here, the smoke run's steps 2–12 against the pin (§4) |
| `[00-begin-does-not-refuse-a-second-writer]` | here, 2026-10-16; assigned | 05, `eb68583` | `test_second_writer_stores.TestTheAcceptance`, `TestMatching`, `TestOneRule`, `TestTheOrder`; `test_second_writer`'s `TestEveryRefusal`, `TestTheWords`, `TestEveryAcceptance`, `TestTheRemedy`; and here, the smoke run's steps 5 and 11 |
| `[04-a-pid-out-of-range-makes-pid-alive-raise]` | 04, `5e20772` | 05, `eb68583` | `test_second_writer.TestPidAlive`; `test_second_writer_stores.TestPidAliveThroughTheStoreOperations` |

**Open at the close**, each owner none (board §3), with why it stays open and what would take it up:

- **`[02b-a-raising-handler-can-leave-the-status-lock-held]`.** At Python 3.14 only, a handler that
  raises just after `with _STATUS_LOCK:` has taken the lock leaves it held; a bare `with` over an
  `RLock` does the same at 3.14.8, so the window is the interpreter's. Fixed at 3.12 and 3.13 by 02c.
  It stays open under L11 (a), recorded in `_update`'s docstring: no client and no CI job runs 3.14.
  *Taken up* when a client or CI moves to 3.14: measure it there again. 07's 3.14.8 run of
  `test_status_writes` passes, and says nothing about this window (§3).
- **`[03-a-run-whose-manifest-cannot-be-read-names-no-store]`.** A live run whose `manifest.json` is
  torn or missing names no store, so the store operations and `begin` proceed on the store it is
  writing. It stays open because no known cause tears a manifest in a run's life (it is written once,
  through `write_json_atomic`, before the first status), and what such a run should mean is a
  decision. *Taken up* by a prompt that decides it (in use for every store, reported, or left), with
  a test of the planner's case.
- **`[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]`.** `Run(path)` on a
  manifest that parses but is not an object constructs, and `checkpoint_path` and `results_path`
  raise. Low impact; no writer makes one. *Taken up* by whichever prompt next touches
  `Run.__init__`: one line, through `_json_object`, and a test of the three forms.
- **`[03-store-show-raises-on-a-state-that-is-a-list-or-an-object]`.** `store show` ends in a
  `TypeError` when a run's `state` is a JSON list or object. Low impact; it predates 03. *Taken up*
  by whichever prompt next touches `store show`: `str(...)` as `list` does, and a test.
- **`[04-a-killed-process-not-yet-reaped-answers-kill-0]`.** A killed process its parent has not
  reaped answers `kill -0`, so `liveness` calls its run `alive`, `end` refuses it and `begin` refuses
  its store. Left, with `end`'s refusal saying why; the registry errs towards in use. **Measured here
  against the release** by breakage (b) (§4.3). *Taken up* beside L3 (b)'s process start time
  (README §8), if a client meets it: telling a zombie apart needs `ps -o stat=` on macOS or
  `/proc/<pid>/stat` on Linux.
- **`[06-three-store-docstrings-and-a-comment-state-the-old-in-use-rule]`.** Three public docstrings
  and a comment in `stores.py` still say a `running` run, "alive or stale", is in use, where the code
  counts every run whose status does not say it has finished (`runregistrykit/stores.py:1366`,
  `:1640`, `:1727`, `:2025`). Prose only; the README and the release notes state the rule as the code
  applies it. *Taken up* by a docstring-only change in a later release, made by a prompt that says
  so.

---

## 7. Decisions

Eleven, L1–L11, each put with a recommendation and each taken as recommended, some refined (campaign
README §6.2; the board's decisions table). "Recorded" is the commit that took it into the plan;
"Applied" the commit that put it into effect.

| | Decided | Taken, for | Refined or amended | Recorded | Applied |
|---|---|---|---|---|---|
| L1 | (a) a machine is identified by the OS's own identity, as a 16-hex digest, never written raw; a display name beside it, for reading only. The user picks a machine per job, often a Mac Studio, so the package records an identity wherever the platform offers one | 2026-10-16, 01 | — | `1fd8e1c` | `387c58f` |
| L2 | (a) both: `status.json` `host: {id, boot}`, the manifest `host: {id, name, machine, system, release, python}`; one public name, `this_host()` | 2026-10-16, 01 | — | `1fd8e1c` | `387c58f` |
| L3 | (a) the boot session id; a `running` run here from another boot is `stale` without `kill -0` | 2026-10-16, 01 | — | `1fd8e1c` | `387c58f` |
| L4 | (a) a new liveness value, `foreign`, not judged; a record with no `host` judged as before and counted | 2026-10-16, 01 | — | `1fd8e1c` | `387c58f` |
| L5 | (a) `status.json` through a unique temporary name with the old mode, and a superseded write discarded | 2026-10-17, 02 | refined at taking: per `status.json` in the process, an in-flight write's fields kept, an `RLock`; **amended** 2026-10-17 after 02's review (`5ed97a5`): only newer in-flight writes re-applied, the landed record never lowered | `34afe6d`; amended `5ed97a5` | `2bf9c72`; amended `2959b78` |
| L6 | (a) an unreadable status counted as in use, refused in its own words; `list` marks it `!!` | 2026-10-18, 03 | refined: in use unless the status says a terminal state; a non-object status or manifest read as unreadable | `88f93c3` | `ab0cad9` |
| L7 | (a) `end` writes the terminal state `lost`, exit code `null`, and an `ended` record whose keys 04 fixes | 2026-10-18, 04 | — | `c3aa52a` | `5e20772` |
| L8 | (a) `end` refuses a live pid here with no override, and a run on another host or whose status does not say unless `--unverified`; `Run.finish` unchanged | 2026-10-18, 04 | — | `c3aa52a` | `5e20772` |
| L9 | (a) `begin` refuses every unfinished run naming its store, no override; and, at the user's request the same day, `[04-a-pid-out-of-range-makes-pid-alive-raise]` fixed with it | 2026-10-18, 05 | six existing tests' setup changes, through one fixture, not their assertions | `f3cc239` | `eb68583` |
| L10 | (a) the release is `v0.2.0`, tagged on 06's commit once CI is green there | 2026-10-18, 06 | — | `7f88787` | `0bae3a3`; the tag `895e3c7` |
| L11 | (a) the 3.14 `with` window recorded in `_update`'s docstring, the issue narrowed to it, not fixed | 2026-10-17, 02c | — | `069f1d7` | `35ce264` |

---

## 8. Deviations across the campaign

Every log classifies its deviations (`CLAUDE.md`, rule 2). The entries were counted from each log's
"Deviations from the prompt" section: a top-level numbered item is one entry, and the labels it
carries were read in it (a scratch script joined each entry's lines, so that a label broken across
lines or set in italics is found, and every entry was then read; 07's log, "Verification
performed", §9). An entry that carries two labels is counted under each; an entry that carries none
of the three is counted as *unlabelled*. A closing line that says "No UNINTENDED DRIFT" or "None is
UNINTENDED DRIFT" (02c, 05, 06) is not an entry.

| Log | Entries | STRUCTURALLY REQUIRED | IMPLEMENTATION CHOICE | UNINTENDED DRIFT | Unlabelled |
|---|---|---|---|---|---|
| 01 | 16 | 8 | 9 | 0 | 0 |
| 02 | 24 | 13 | 12 | 0 | 0 |
| 02b | 24 | 19 | 6 | 1 | 0 |
| 02c | 20 | 15 | 6 | 0 | 0 |
| 03 | 17 | 7 | 9 | 1 | 1 |
| 04 | 19 | 12 | 7 | 0 | 0 |
| 05 | 22 | 15 | 6 | 0 | 1 |
| 06 | 17 | 10 | 7 | 0 | 0 |
| **All** | **159** | **99** | **62** | **2** | **2** |

Six entries carry two labels (01 1, 02 4, 02b 7 and 10, 02c 5, 03 5), so the class columns sum to
163. The two unlabelled entries are 03's 6 (the helper outside the swept section, "see §4") and 05's
14 (its correction 14, "observations, not fixes"), each a reading recorded as found.

**Where this differs from the prompt and the board.** The prompt's §1.3 table counts the labels'
**words** on one line (`grep -o`): 7 / 7 / 0 for 01, and so on. Those counts were re-run and agree,
log by log, but a word is not an entry: a label broken across lines (01's entries 1 and 13) is
missed, and a closing line (02c, 05, 06) is counted. Each review's count agrees with this table
where it gives one (01 sixteen; 02 twenty-four; 02b one UNINTENDED DRIFT; 02c, 04, 06 none; 04
nineteen; 06 seventeen) but two:
- **03's review** says "seventeen deviations classified … none UNINTENDED DRIFT (the seventeenth,
  prose left in `stores.py`, is an observation rather than a deviation)". The log labels its entry
  17 "**UNINTENDED DRIFT** avoided, by leaving it". Counted here as the log labels it; the review's
  reading is right on the substance, since nothing drifted, and the prose was opened as an issue by
  06's review.
- **05's review** says "fourteen STRUCTURALLY REQUIRED, six IMPLEMENTATION CHOICE". Read entry by
  entry, fifteen carry the first label (1, 2, 5–13, 15–18); entry 1 says of itself "the prompt as
  written already says so; recorded as found", which the review may have set aside. The log is the
  record; this count is the log's.

**Every UNINTENDED DRIFT entry:**

- 02b, deviation 24: a first draft cited an issue by its board name in a test docstring;
  `test_no_citation` failed on it and it was reworded before any record was written. The review
  accepted it ("one UNINTENDED DRIFT (a test docstring that named an issue, caught by the citation
  guard and reworded before committing)").
- 03, deviation 17: three lines of `stores.py` prose left stating the old in-use rule, labelled
  "UNINTENDED DRIFT avoided, by leaving it". The review read it as an observation; 06's review opened
  the prose, with a fourth line, as `[06-three-store-docstrings-and-a-comment-state-the-old-in-use-rule]`.

07's own log, written with this document, is not in the table: it classifies 16 entries (13
STRUCTURALLY REQUIRED, 4 IMPLEMENTATION CHOICE, no UNINTENDED DRIFT; its entry 8 carries two
labels).

**Every STRUCTURALLY REQUIRED entry that changed what a prompt delivered:**

- 02, 3: `begin`'s first status goes through the new writer, so nothing writes `status.json.tmp`.
- 02b, 1 and 4: (m3) recorded as a mutant that changes nothing under the by-number record, and
  (m3′) added in its place (the user's decision (A), 2026-10-17).
- 02b, 2: a write's sequence number taken by `next()` on a per-book counter, which the new merge
  needs.
- 02b, 3: the sweeps run in a child process.
- 02c, 1: L11 (a): the docstring sentence, `pyproject.toml` unchanged, the issue narrowed, not closed.
- 02c, 9: the prompt's `JUMP_BACKWARD` condition read as `_write_status`'s own.
- 03, 7: `liveness` unknown for any status that is not a non-empty object.
- 03, 8: the store module built on `RetireTestCase`, with a store per form.
- 03, 12: `list`'s marker, and its stderr line placed after the stale line.
- 04, 4 and 5: each form's `--unverified` acceptance made on a dead pid; a `running` status with a
  `null` pid tested and accepted.
- 04, 6: the host a refusal names, the manifest's `host.name` or the status's `host.id`.
- 04, 15: the nine changed assertions; `REMEDY` written as two literals.
- 04, 19: `list`'s stale line names `end` without `--unverified`.
- 05, 2: the `set_aside` fixture, and two bare runs bound so they can be set aside.
- 05, 5: where `begin`'s check sits: after the tombstone check, only when the runs root exists.
- 05, 9: the earlier-boot and foreign tests skip where the platform gives no boot or id.
- 05, 11: what `_end_run` writes back for an out-of-range `evidence.pid`, recorded, not changed.
- 06, 6: the release notes' `[1]` row measured in a runs root of its own.
- 06, 7 and 8: the README states the store rule without citing a help text, and says "the first two
  lines name `end`".
- 06, 9: the adoption notes report the clients' `git grep` hits as found, more than the prompt's.

---

## 9. Observations not acted on

Forty-six, each log's section of that name item by item (01 5, 02 5, 02b 4, 02c 4, 03 6, 04 7, 05 8,
06 7). The disposition at `v0.2.0` was decided from the later logs, the board, the release and
adoption notes and the code at `0bae3a3`; nothing was changed to decide it.

| Log | Observation | At `v0.2.0` |
|---|---|---|
| 01 | A write that reads an unreadable status drops `host` | recorded in the release notes (§2.1's `status.json` `host` row; §2.2) |
| 01 | Containers share an image's `/etc/machine-id` | recorded in the release notes (§2.6); unverified (§10) |
| 01 | Store docstrings list "alive or stale" | opened as `[06-three-store-docstrings-and-a-comment-state-the-old-in-use-rule]` (06's review); open. The README's rules were brought into line by 06 |
| 01 | The refusals' remedy for a `foreign` run says `Run.finish` | addressed by 04 (`5e20772`: `_END`, `_foreign_remedy`) |
| 01 | `this_host()` costs 343 µs | still an observation |
| 02 | A field of an earlier in-flight write re-applied over a newer landed one | opened as `[02-an-in-flight-write-is-re-applied-over-a-newer-landed-one]` (02's review); closed by 02b |
| 02 | A fork while `_STATUS_LOCK` is held leaves the child's lock held | still an observation (02b's and 02c's logs carry it; read, not measured) |
| 02 | A handler raising inside `_write_status`'s `finally` leaves an in-flight entry | still an observation |
| 02 | The bookkeeping lasts the process | still an observation (not a defect) |
| 02 | A killed process leaves `status.json.<unique>.tmp` | recorded in the README (`README.md:154-157`) and the release notes (§2.3) |
| 02b | Exception-table gaps the sweep's raising modes reach | opened as `[02b-a-raising-handler-can-leave-the-status-lock-held]` (02b's review, measured at 3.13); narrowed by 02c; open |
| 02b | The sweep is the stronger test, so it runs in a child | still an observation (by design) |
| 02b | 02's documented window is the finish sweep's 24 accepted points | still an observation (stated in `_update`'s docstring) |
| 02b | 02's other observations stand | still observations (02's above) |
| 02c | The 3.14 `with` point stays | the open issue `[02b-a-raising-handler-can-leave-the-status-lock-held]`, under L11 (a) |
| 02c | Uncovered `JUMP_BACKWARD`s outside `_write_status` | still an observation (none holds the lock; 02c's review, check 4) |
| 02c | The core run's editable install rewrote the ignored `runregistrykit.egg-info/` | still an observation (true of every editable install; 07 installed from a clone and from the pin) |
| 02c | 02's and 02b's other observations stand | still observations |
| 03 | `Run(path)` on a manifest that is not an object raises where it is used | opened as `[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]`; open |
| 03 | Three lines of `stores.py` prose state the old rule | opened as `[06-three-store-docstrings-and-a-comment-state-the-old-in-use-rule]` (06's review); open |
| 03 | `list`'s `_progress`, `_purpose` and `_age` not hardened against odd types | still an observation (not measured) |
| 03 | The editable install rewrote `runregistrykit.egg-info/` | still an observation |
| 03 | A status written between `begin` and the first heartbeat | still an observation (05 changed `begin`'s check, not its first status) |
| 03 | A run that predates the registry is `unknown`, unmarked, no store's user | still an observation (by design) |
| 04 | The window between `end`'s check and its write | still an observation (`_end_run`'s docstring: "This takes no lock and is not one") |
| 04 | A pid reused within one boot makes a hard-killed run un-endable | still an observation; a known gap, L3 (b) (§10) |
| 04 | A pid out of range makes `pid_alive` raise | opened as `[04-a-pid-out-of-range-makes-pid-alive-raise]`; closed by 05 |
| 04 | `Run.__init__`'s manifest read is still raw | the open issue `[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]` |
| 04 | `stores.py` prose; the module docstring names `Run.finish(..., fingerprint=True)` | the prose opened as `[06-three-store-docstrings-and-a-comment-state-the-old-in-use-rule]` (06's review); open. The docstring at `stores.py:52` describes who writes a fingerprint, which is true |
| 04 | The editable install rewrote `runregistrykit.egg-info/` | still an observation |
| 04 | `end` refuses a run directory that predates the registry | still an observation (by design; its refusal says it blocks no store) |
| 05 | Two `begin`s at the same moment both pass the check | still an observation (`README.md:126`; `begin`'s docstring); a known gap (§10) |
| 05 | A run under another runs root is not seen | still an observation (docstring; pinned by a test) |
| 05 | `begin`'s check costs about 250 ms with 1000 runs | still an observation |
| 05 | `_end_run` copies an out-of-range pid into `evidence.pid` as it is | still an observation |
| 05 | A `pid` of JSON `true` is 1 and answers `kill -0` | still an observation |
| 05 | The editable install regenerated `runregistrykit.egg-info/` | still an observation |
| 05 | `begin` refuses a killed child not yet reaped | the open issue `[04-a-killed-process-not-yet-reaped-answers-kill-0]`; measured here against the release (§4.3 (b)) |
| 05 | Nothing found in `liveness`, `list_runs`, `store show`, `end` or the store operations | no action (a finding of nothing) |
| 06 | Four lines of `stores.py` prose | opened as `[06-three-store-docstrings-and-a-comment-state-the-old-in-use-rule]` (06's review); open |
| 06 | The README's opening paragraph says `list` judges by pid and heartbeat | still an observation (`README.md:7-8`, unchanged; "A run" and rule 2 say what the host adds) |
| 06 | SGK's `interrupt_when.py:161` raises on a non-object status | recorded in SGK's adoption note (`docs/adoption/v0.2.0/secondarygwkit.md:72`) |
| 06 | `end` on an unreadable status writes no `host` | recorded in the release notes (§2.2) |
| 06 | A `v0.1.0` reader raises on a runs root with a non-object status | recorded in the release notes (§4) |
| 06 | The board's suite sentence not extended to 06 | addressed by 06's review (`74f85a2`: "… 410 after 05, and 410 after 06") |
| 06 | The reinstall rewrote `runregistrykit.egg-info/` | still an observation |

Of the 46: 2 addressed (by a prompt or a review), 2 opened as issues and since closed, 6 opened as
issues still open, 3 already the subject of an open issue, 6 recorded in the release, README or
adoption notes, 1 needing no action, and 26 still observations.

---

## 10. Known gaps

- **G1–G3 have not held.** No client has adopted `v0.2.0`. SGK is pinned at `v0.1.0`:
  `requirements.txt:81` at its newest commit, `79434bf` (branch `handover-remedial`, its newest of
  any branch; `git -C <SGK> show 79434bf:requirements.txt | sed -n 81p`), is `runregistrykit[stores]
  @ git+https://github.com/ds283/RunRegistryKit@v0.1.0`. ChamPBH and StochasticInstantons use
  nothing of the registry (06's adoption notes). The campaign closes without waiting for them (README
  §7); each is recorded on the board when it holds, in a records commit of its own.
- **What remains unverified:**
  - **A real reboot.** An earlier boot is tested only by a status written with another `boot`
    (`test_host`, `test_end`); no machine was rebooted under a run. **A real run on another
    machine** likewise: `foreign` is tested only by a status with another `host.id`.
  - **Linux** only through CI (`ubuntu-24.04`, the ten runs of §2.2); every local measurement is
    macOS. **Containers** not at all.
  - **A pid reused within one boot** (L3 (b), README §8): such a pid answers `kill -0`, and `end`
    refuses it with no override (04's observation 2).
  - **Python 3.14** beyond 02c's sweep, which passes at 3.14.8 (§3), and L11's `with` window, which
    the sweep cannot model and a real signal hit at 3.14.8 in 02c's measurement; no client or CI
    runs 3.14.
  - **A client's own stores and run directories**: none was opened (README §3). The smoke run builds
    its own client root.
  - **Two `begin`s at the same moment**: `begin`'s refusal is a check, not a lock, and no test or
    smoke step runs two at once.
- **The extraction's smoke run at `v0.2.0`** fails its step 3 on `list`'s summary clause, which 01
  added; the script is right for `v0.1.0` and is not changed (§5.2).
- **The six open issues** (§6).

---

## 11. Reproduction

From a clean checkout of the commit that adds this document, at its root, with `S` a scratch
directory of your own, `TMPDIR="$S/tmp"` exported, and the venv of `README.md`'s "Developing" at
`./venv`. The installs fetch from GitHub and PyPI.

```bash
export S=<scratch>; mkdir -p "$S/tmp"; export TMPDIR="$S/tmp"

# §2: the commits, the tag and CI
git rev-list --count b56ecc7^..e4bf592
git log --reverse --format='%h %s' b56ecc7^..e4bf592
git ls-remote origin refs/tags/v0.2.0 'refs/tags/v0.2.0^{}'
for r in 38911075984 38929845135 39049728089 39060913296 39072902589 \
         39083674030 39122974980 39129061916 39143681701 39144321994; do
  gh run view "$r" --json databaseId,headSha,status,conclusion,jobs \
    --jq '"\(.databaseId) \(.headSha[0:7]) \(.conclusion) " + ([.jobs[] | "\(.name)=\(.conclusion)"] | join(", "))'
done

# §3: the suite, low end, and per module
pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'
./venv/bin/python -m unittest discover -s runregistrykit/tests -t .
./venv/bin/python - <<'EOF'
import unittest
def tests(s):
    for t in s:
        yield from tests(t) if isinstance(t, unittest.TestSuite) else [t]
counts = {}
for t in tests(unittest.defaultTestLoader.discover("runregistrykit/tests", top_level_dir=".")):
    counts[type(t).__module__] = counts.get(type(t).__module__, 0) + 1
for name in sorted(counts): print(counts[name], name)
EOF
./venv/bin/python -m unittest -v runregistrykit.tests.test_host 2>&1 | grep skipped

# §3: the suite, high end, from a clone; test_status_writes at 3.14.8
git clone -q . "$S/clone-high"
uv venv --python /opt/local/bin/python3.13 "$S/suite-high"
uv pip install --no-cache --python "$S/suite-high/bin/python" -e "$S/clone-high[stores]" \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
(cd "$S/clone-high" && "$S/suite-high/bin/python" -m unittest discover -s runregistrykit/tests -t .)
(cd "$S/clone-high" && PYTHONPATH="$S/clone-high" /opt/local/bin/python3.14 \
  -m unittest -v runregistrykit.tests.test_status_writes)

# §3: black
./venv/bin/black --check runregistrykit docs

# §5: the three pin venvs
uv venv --python /opt/local/bin/python3.12 "$S/pin-low"
uv pip install --no-cache --python "$S/pin-low/bin/python" \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.43.0' 'sqlalchemy==2.0.39'
uv venv --python /opt/local/bin/python3.13 "$S/pin-high"
uv pip install --no-cache --python "$S/pin-high/bin/python" \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
uv venv --python /opt/local/bin/python3.12 "$S/pin-core"
uv pip install --no-cache --python "$S/pin-core/bin/python" \
  'runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.2.0'
for v in pin-low pin-high pin-core; do
  sp=$(ls -d "$S/$v"/lib/python3.1*/site-packages)
  for m in __init__ __main__ client fingerprint stores; do
    git show "0bae3a3:runregistrykit/$m.py" | cmp - "$sp/runregistrykit/$m.py"
  done
  cat "$sp"/runregistrykit-0.2.0.dist-info/direct_url.json; echo
  grep -c tests "$sp"/runregistrykit-0.2.0.dist-info/RECORD
  (cd "$S/tmp" && "$S/$v/bin/python" -I -c 'import runregistrykit.tests') 2>&1 | tail -1
done

# §4: the interrupted run, at both ends and in the core venv
pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'
"$S/pin-low/bin/python"  docs/interrupted-runs/interrupted_run_smoke.py   # exit 0
"$S/pin-high/bin/python" docs/interrupted-runs/interrupted_run_smoke.py   # exit 0
"$S/pin-core/bin/python" docs/interrupted-runs/interrupted_run_smoke.py   # exit 1: steps 1, 11, 12
pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'
# (a) and (b): the diffs of 07's log, saved as $S/a.diff and $S/b.diff
git clone -q . "$S/clone-break"
for x in a b; do
  (cd "$S/clone-break" && git apply --check "$S/$x.diff" && git apply "$S/$x.diff" &&
   "$S/pin-low/bin/python" docs/interrupted-runs/interrupted_run_smoke.py;   # exit 1
   git apply -R --check "$S/$x.diff" && git apply -R "$S/$x.diff" && git status --porcelain)
done
PATH=/nonexistent "$S/pin-low/bin/python" docs/interrupted-runs/interrupted_run_smoke.py   # exit 2

# §5.2: the extraction's smoke run against v0.2.0
"$S/pin-low/bin/python"  docs/extraction/store_smoke_run.py   # exit 1: step 3
"$S/pin-high/bin/python" docs/extraction/store_smoke_run.py   # exit 1: step 3
```

---

## 12. Summary for the board

- **Closed 2026-10-18 at 07.** All nine prompts landed; 44 commits before 07's, classed (§2.1).
- **`v0.2.0`** (tag object `895e3c7`, `0bae3a3`), installed from GitHub at both ends and in the core
  form, is `0bae3a3`'s five modules and ships no test; CI green on ten runs since 01 (§2.2, §5).
- **The suite**: 410 OK, one skip, in `venv/` and at the high end, the same by module;
  `test_status_writes` at 3.14.8, 22 OK, no skip (§3).
- **The hard-kill route from the pin**: thirteen steps pass at both ends (3.8 s, 6.3 s), Ray never
  started, no child left; breakage (a)–(c) fail as they should, (b) measuring
  `[04-a-killed-process-not-yet-reaped-answers-kill-0]` against the release (§4).
- **The extraction's smoke run** at `v0.2.0`: 10 of 11, step 3 on 01's summary clause (§5.2).
- **Issues**: 14 on the board, 8 resolved (the five assigned and three found), **6 open**, none with
  an owner. **Decisions**: L1–L11, all taken as recommended, L5 and L6 refined, L5 amended.
  **Deviations**: 159 entries (99 / 62 / 2, 2 unlabelled). **Observations**: 46, 26 still
  observations (§6–§9).
- **Open**: G1–G3 (§10).
