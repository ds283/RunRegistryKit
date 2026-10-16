# Prompt 01 — the host

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- The campaign is planned (`b56ecc7`), and L1–L4 are taken (README §6.2, 2026-10-16), each as
  recommended.
- `git diff --stat 79015a7 HEAD -- runregistrykit pyproject.toml .github` is empty: the package is
  `v0.1.0`'s.
- The suite is `Ran 276 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[04-runs-do-not-say-which-machine-produced-them]`.
**Opens:** only what the work finds. **Narrows:** nothing planned.

**Recommended model:** **Opus**. This is the campaign's first change to what the registry writes.
It changes the judgement `list` and every store operation make about a `running` run, and the
prompts after it depend on that judgement.

**Read first:**

1. [`README.md`](README.md): §0 and §0.1, §0.2 (the identifier table above all), §5 (all of it;
   rules 7, 8 and 9 especially) and §6.2 (L1–L4, taken).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md) §3: `[04-runs-do-not-say-which-machine-produced-them]`
   in full, its four questions above all.
3. `runregistrykit/__init__.py`: `:64-104` (imports, `__all__`, `TERMINAL_STATES`), `:232-311`
   (`read_json`, `write_json_atomic`, `pid_alive`, `heartbeat_age`, `liveness`), `:395-430`
   (`Run.status`, `_update`, `heartbeat`), `:604-745` (`begin`), `:749-790` (`list_runs`).
4. `runregistrykit/stores.py` `:957-1040` (`runs_naming`, `_running_runs_naming`,
   `_describe_running`, `_refuse_if_in_use`); `runregistrykit/__main__.py` `:408-430` and `:528-570`
   (`list`).
5. `runregistrykit/tests/test_run_registry.py` `:116-160` (`RegistryTestCase`) and `:604-720`
   (`TestStatus`, `TestLiveness`, `TestLister`); `test_public_names.py` `:59-90`;
   `.github/workflows/tests.yml`.
6. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers below are the package's at `b56ecc7`, which are `v0.1.0`'s.

---

## 1. What is wanted

A run says which machine it is on and which boot of that machine, and the registry uses that before
it trusts a pid.
- A `running` run on **another host** is no longer judged by this machine's `kill -0`. It is
  reported as `foreign`, and still counted as in use by the store operations.
- A `running` run on **this host, from an earlier boot** is `stale` whatever `kill -0` says, since
  its pid cannot name a process of this boot.
- A record with **no host**, which is every record written before this prompt, is judged exactly
  as `v0.1.0` judged it, and `list` counts it.

The identity is read from the operating system through the standard library (L1, L3). It is
written to `status.json` beside the pid it qualifies, and to the manifest for provenance (L2). No
hardware identifier is written raw.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`, `runregistrykit`
editable. **Install nothing.**

### 2.2 Reading the host (L1, L3)

In `runregistrykit/__init__.py`, in the liveness section beside `pid_alive`, standard library only
(`ctypes`, `ctypes.util`, `platform` and `hashlib` are allowed; `subprocess` is not used for this).
Three private readers, each returning a string or `None` and **never raising**:

| Reader | macOS (`platform.system() == "Darwin"`) | Linux | Elsewhere |
|---|---|---|---|
| the raw machine identity | `gethostuuid(3)` through `ctypes`, a 16-byte buffer and a `timespec` wait of 1 s; the UUID as lowercase text | the first non-empty of `/etc/machine-id` and `/var/lib/dbus/machine-id`, stripped, lowercased | `None` |
| the boot identity | `sysctlbyname("kern.bootsessionuuid")` through `ctypes`, decoded, NUL stripped | `/proc/sys/kernel/random/boot_id`, stripped | `None` |
| the display name | the environment variable `RUNREGISTRYKIT_HOST_NAME` if set and non-empty, else `platform.node()`, else `None` | same | same |

A nonzero return, an `OSError`, a missing library, an empty or malformed value: each gives `None`.
Measured at writing on macOS 27: `gethostuuid` returns 0 in 31 µs and equals `ioreg`'s
`IOPlatformUUID`; `sysctlbyname` returns 0 in 51 µs with 37 bytes. **Do not use `kern.uuid`**,
which is the kernel build's UUID, the same on every machine running that kernel.

**The recorded id is a digest**, never the raw identity: the first 16 hex characters of
`hashlib.sha256(b"runregistrykit host\0" + raw.encode()).hexdigest()`, or `None` when the raw
identity is `None`. The boot identity is recorded as it is read; it is not a hardware identifier.

**One public function**, added to `__all__` (L2):

```python
def this_host() -> dict:
    """{"id", "boot", "name", "machine", "system", "release", "python"} for this machine now."""
```

`machine`, `system`, `release` and `python` are `platform.machine()`, `platform.system()`,
`platform.release()` and `platform.python_version()`. It reads afresh on each call, with no cache,
so that a test can patch the private readers; each call costs well under a millisecond. Nothing
happens at import.

### 2.3 What is written (L2)

- **`begin`** (`:604`). The manifest (`:707-725`) gains `host`: `this_host()`'s `id`, `name`,
  `machine`, `system`, `release` and `python`, taken once, before the run directory is made. The
  first `status.json` (`:728-734`) gains `host: {"id": …, "boot": …}`, from the same call. Both are
  written even when every value is `None`: an absent `host` means "written before this field
  existed", and `null` values mean "this platform offered none". The two must stay distinguishable.
- **Every later write keeps it.** `Run._update` (`:398`) merges into the status it read, so `host`
  is carried as it is. No other write of `status.json` is changed. `heartbeat(pid=…)`, the launcher
  case, keeps the host: the child is on the launcher's machine.
- Nothing else changes form. `checkpoint.jsonl` and the sidecar are untouched, and so is the
  manifest's other fields. The `status.json` temporary name is 02's, not this prompt's.

### 2.4 How a record is judged (L3, L4)

`liveness(status, stale_after, now=None, *, here=None)`, where `here` is a `this_host()` dict and
defaults to one read afresh. In order:

1. no status → `unknown`; a terminal state → `finished`; a state other than `running` → `unknown`
   (as now, `:301-306`);
2. **the record is on another host** → `foreign`, without testing the pid or weighing the
   heartbeat. That is when `status["host"]["id"]` is not `None` and differs from `here["id"]`,
   including when `here["id"]` is `None`: this machine records `null`, so a record carrying an id
   was written elsewhere;
3. **the record is on this host, from another boot** → `stale`. That is when both ids match and are
   not `None`, both boots are not `None`, and they differ;
4. otherwise, as now: `pid_alive`, then the heartbeat age (`:307-311`).

A status with no `host`, a `host` that is not a dict, or `host.id` `null` reaches step 4: judged
here, as `v0.1.0` judged it (README §5 rule 8). The docstring states the order and says what
`foreign` means: not judged here, not that the run is alive.

**`list_runs`** (`:749`) reads `this_host()` **once** per call and passes it to every `liveness`.
Each entry gains:
- `host`: the manifest's `host.name`, or `None`;
- `host_id`: the status's `host.id`, or `None`;
- `host_recorded`: whether the status has a `host` dict.

The existing keys and their meaning are unchanged. The docstring lists the new keys.

### 2.5 What is reported

- **`list`** (`__main__.py:528-570`):
  - A `foreign` entry's marker is `??`, where `stale` keeps `!!`.
  - Its row shows the host name, or the id when there is no name, wherever the row has room. The
    layout is the agent's to choose; keep every existing column.
  - The summary counts `foreign` like every other liveness.
  - It says how many entries have `host_recorded` false, as "N with no host recorded" in the
    summary line.
  - When any entry is `foreign`, stderr gets one line: "?? N run(s) say they are running on another
    host (…names…): their pids are not tested here. Look on that host."
  - The `!!` line for `stale` gains "or this machine has rebooted since".
  - Nothing else in the output changes.
- **The store operations' refusal.** `_describe_running` (`stores.py:1021`) names a `foreign` run
  by its host: for example "run X is running on another host, <name or id> (pid N, not tested
  here), and names this store by its …". `_running_runs_naming` already counts every `running`
  entry, so a `foreign` run is in use without a change there. **Pin it by a test** (§2.7). The
  remedy text in each refusal is unchanged; `end` is 04's.

### 2.6 Public names and CI

- `__all__` gains `this_host`, sorted. `test_public_names.py` needs no change: it derives the
  expected names from the module's source (`_defined_public_names`, `:59`), so it passes with
  `this_host` declared and fails without it.
- `.github/workflows/tests.yml`'s core job runs its tests by name (`:89`). Add the new core test
  module (§2.7) to that line. Change nothing else in the workflow.

### 2.7 The new tests

Two new modules, each with the licence header and a docstring of its own.

**`runregistrykit/tests/test_host.py`**, core only, importing nothing of the store layer, so that
the core CI job can run it. Its tests build records with fake host dicts and pass `here=` explicitly,
or patch the private readers, so they never depend on which machine runs them. At least:
- **The readers on this platform.** On Darwin and on Linux, `this_host()` gives a 16-hex `id`, a
  non-empty `boot`, and the same values on two calls. Elsewhere the test is skipped, saying why.
  CI covers Linux and a local run covers macOS; the log records both.
- **No raw identifier is written.** Through the private reader, take the raw identity. After a
  `begin`, a `heartbeat` and a `finish`, the raw text appears in no file of the run directory, and
  the digest does.
- **A reader that fails.** With each reader patched to raise or to return nothing, `this_host()`
  gives `None` there, and `begin`, `heartbeat`, `finish` and `list_runs` still work. `status.json`
  then holds `host` with `null` values, not no `host`.
- **What is written.** The manifest's and the first status's `host`, their keys exactly. `host`
  survives a `heartbeat`, a `heartbeat(pid=…)` with another pid, and a `finish`.
- **The judgement**, one test per step of §2.4:
  - another host's running record is `foreign`, even with a live pid (this process's) and a fresh
    heartbeat, and even with a dead pid;
  - a record with an id read where `here["id"]` is `None` is `foreign`;
  - this host from another boot is `stale`, even with this process's pid and a fresh heartbeat;
  - this host and this boot is judged by pid and heartbeat as before;
  - a terminal record from another host is `finished`.
- **An old record** (README §5 rule 8). A `status.json` of `v0.1.0`'s form, with no `host` at all,
  built in the test, is judged exactly as `v0.1.0` judges it: alive with this process's pid and a
  fresh heartbeat, stale with a reaped pid. `list_runs` reports `host_recorded` false.
- **The command line.** `list` over a runs root holding a `foreign` run, a stale run and a record
  with no host prints `??` and `!!` on the right rows, the foreign line on stderr, and the count of
  records with no host. Use a child process, as `TestLister` does.

**`runregistrykit/tests/test_host_stores.py`**, which needs `[stores]`: a `running` run whose status
names another host, recorded against a registered store, makes `copy_store`, `move_store`,
`fingerprint_store`, `retire_store(dry_run=True)` and `amend_sidecar` refuse. Each refusal names
the run, says "another host" and names the host, and the store is untouched. Use the existing
fixtures (`store_fixtures`, `RetireTestCase`) as the planner's probe did (README §0.2).

### 2.8 The board's issue

**Closed: `[04-runs-do-not-say-which-machine-produced-them]`**, moved to §4. Say what resolved each
of its four questions:
- a manifest with no `machine` → no `host`, judged here and counted;
- what names a machine → the OS identity's digest, with a display name;
- where it is recorded → `status.json` and the manifest;
- a reused pid → the boot.

Name the tests that pin each. Delete its row from `docs/OPEN_ISSUES.md` (10 → 9). The other four
entries on the board: give each its package lines at this commit where 01's edits moved them,
under a "Package lines (01, …)" note.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root: **`Ran 276
   + N tests … OK`**, N the new tests of §2.7. Give the per-module counts and the time.
2. **The core alone**, as CI's core job runs it: in a fresh scratch venv with the package installed
   without `[stores]`, `python -m unittest runregistrykit.tests.test_run_registry
   runregistrykit.tests.test_public_names runregistrykit.tests.test_host` passes, and `datastorekit`,
   `ray` and `sqlalchemy` are absent. Remove the scratch venv afterwards.
3. **Nothing outside temporary directories.** `git status --short --ignored` is the same before and
   after a run (but `__pycache__/`); no Ray process before or after.
4. **What is written, by hand.** In a scratch client root, `begin`, `heartbeat`, `finish`; give the
   manifest's and the status's `host` in the log with the `id` shown and the raw identity **not**
   shown. Then `list` there and give its output.
5. **The mutation record**, §3.6, each a diff exactly as applied, with the suite's verdict and the
   failing tests. None is committed.
6. **The tests catch behaviour** (README §5 rule 10). Each mutation applied, the suite run, and
   reverted:
   - (m1) step 2 of §2.4 removed: another host's record judged by pid;
   - (m2) step 3 removed: another boot judged by pid;
   - (m3) a record carrying an id treated as this host's when `here["id"]` is `None`;
   - (m4) `begin` writing no `host` to `status.json`;
   - (m5) `_update` writing only the fields it was given, so a heartbeat drops `host`;
   - (m6) the raw identity recorded in place of its digest;
   - (m7) `_running_runs_naming` skipping `foreign` entries;
   - (m8) the agent's own: one mutation of `list`'s markers or counts that a test catches, named in
     the log.

   Each must fail at least one test, named in the log. A mutation no test catches is a stop.
7. `./venv/bin/black --check runregistrykit docs` is clean.
8. **CI.** After pushing is the user's to do; record in the log that the Linux readers are exercised
   only there, and that the orchestrator's review is to read the CI run's `test_host` result.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` gains exactly `tests/test_host.py` and
   `tests/test_host_stores.py`, and changes `__init__.py`, `stores.py` and `__main__.py`; the
   workflow changes on one line.
2. §3.1–§3.7 hold. Every test that existed at `b56ecc7` passes unchanged in what it asserts.
3. **The records**, in the same commit:
   - the log, `logs/01-the-host.md`, per README §5.1: the suite before (276) and after, the core
     run, the hand run of §3.4, and every mutation as a diff;
   - this board: the header, §1's row for 01, §1.1's H1, §3 and §4 as §2.8;
   - `docs/OPEN_ISSUES.md`: the row deleted, the count, the date;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- An existing test fails, or would need a change to what it asserts.
- A mutation of §3.6 is caught by no test.
- Any record would change form beyond §2.3: a field of the manifest or `status.json` other than
  `host` added, removed or renamed, or `checkpoint.jsonl` or a sidecar touched.
- A reader cannot be written without `subprocess`, or without a dependency outside the standard
  library, on macOS or Linux.
- The design would have the package conclude more than §2.4 says: that a `foreign` run is dead, or
  that a run on this host and boot is dead without `kill -0` or the heartbeat (README §5 rule 9).
- The suite needs a Ray cluster, starts Ray, imports a client, or writes outside a `tempfile`
  directory.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, or installing anything into `venv/`.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `runregistrykit/__init__.py`, `stores.py` (`_describe_running`
  only), `__main__.py` (`list` only); new `tests/test_host.py` and `tests/test_host_stores.py`; one
  line of `.github/workflows/tests.yml`; the log, this board, `prompts/INDEX.md`,
  `docs/OPEN_ISSUES.md`.
- It does not change how `status.json` is written (02), the in-use check's treatment of an
  unreadable status (03), `end` or the refusals' remedy text (04), or `begin`'s refusals (05).
- It adds no process start time (L3 (b); README §8).
- It writes no README usage or release notes (06), changes `pyproject.toml` not at all, and makes
  no tag.

---

## 7. The log and the board

`logs/01-the-host.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 01, §1.1's H1, §3 and §4 as §2.8.

---

## At writing (2026-10-16, at `b56ecc7`)

Measured for the README's row and the orchestrator:
- **The identifiers** on macOS 27, `arm64`, Python 3.12: README §0.2's table. `platform.node()`
  here is a DNS name the network assigned, which is why it is a display name only. Linux is not
  measured here; CI's `ubuntu-24.04` runner is where the Linux readers first run.
- **Where the jobs run** (L1): the user decides per job, often a Mac Studio, not always. So two
  Macs at least, and `foreign` is the common case for a record read on the other one.
- **The tests**: no test asserts the key set of a manifest or a `status.json` (`grep` for
  `assertEqual(set(` and `sorted(` over `runregistrykit/tests/` finds only `packages`' keys,
  `test_run_registry.py:289`, unaffected). `TestLiveness` (`:655`) and `TestLister` (`:682`) build
  their runs with `begin`, which will record this host, so their assertions stand. The core CI job
  names its two modules at `tests.yml:89`.
- **The public names**: `__all__` (`__init__.py:76-97`) has 20 names. `test_public_names.py`
  derives the expected set from the module's source, so `this_host` is declared in `__all__` and
  the test is not edited.
- **SGK** reads `liveness` only through `list`, and asserts `TERMINAL_STATES`
  (`RunDrivers/tests/test_pipeline_adoption.py:252`), which this prompt leaves alone (README §0.2).
