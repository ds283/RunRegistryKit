# Log — prompt 01: the host

**Subject:** Record the host and boot a run is on, and judge a run by them
**Commit:** `387c58f` (on `main`, after `8023e14`)
**Date:** 2026-10-16
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1-8)
**Result:** **landed.**
- A run records the machine and the boot its pid belongs to. `this_host()` is a new public name,
  and its three private readers use the standard library only, with no subprocess. `begin` writes
  `host` to the manifest and to the first `status.json`, and every later write keeps it.
- `liveness` answers `foreign` for a `running` record from another host without testing its pid,
  and `stale` for one from an earlier boot of this host. A record with no `host` is judged as
  `v0.1.0` judged it.
- `list` marks a `foreign` run `??`, names its host, and counts records with no host. The store
  operations refuse a store a `foreign` run names, and name its host.
- The suite is **276 → 307**: 28 new tests in `test_host`, 3 in `test_host_stores`. Every module
  that existed has the count it had, and no existing test changed.
- The core alone, in a scratch venv without `[stores]`, runs 65 tests, OK, with one skip (the Linux
  readers).
- Each of (m1)–(m8) fails at least one test. No stop condition fired.
- `[04-runs-do-not-say-which-machine-produced-them]` is closed, and nothing is opened, so
  `docs/OPEN_ISSUES.md` counts **9**.
- **Nothing pushed, no tag made, no workflow dispatched.** Here the Linux branch has run only
  with `platform.system` patched, against files in a temporary directory; the real Linux files are
  first read in CI (below).

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | `import platform`; `this_host` in `__all__`; the host section beside `pid_alive` (constants, `_first_line`, `_c_library`, `_read_machine_identity`, `_read_boot_identity`, `_read_host_name`, `_ask`, `this_host`); `liveness(..., *, here=None)` with the host and boot steps and a docstring stating the order; `begin` reading `this_host()` once and writing `host` to the manifest and the first status, its docstring saying so; `list_runs` reading this host once and giving `host`, `host_id`, `host_recorded` |
| `runregistrykit/stores.py` | `_describe_running` only: a `foreign` run named by its host |
| `runregistrykit/__main__.py` | `list` only: the `??` marker and the host in a foreign row, the summary's count of records with no host, the stale line's reboot clause, the foreign line on stderr; and `_host`, a helper of `list`'s (deviation 9) |
| `runregistrykit/tests/test_host.py` | new, core only: 28 tests, in five classes |
| `runregistrykit/tests/test_host_stores.py` | new, needs `[stores]`: 3 tests |
| `.github/workflows/tests.yml` | the core job's test line names `runregistrykit.tests.test_host` too; nothing else |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: `pyproject.toml`, `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/adoption/`, any other
test module, the prompt, the campaign README, `orchestrator/`. No client, DatastoreKit or RayPoolKit
file.

### What is written

The manifest gains one key, `host`, with exactly `id`, `name`, `machine`, `system`, `release` and
`python`. The first `status.json` gains one key, `host`, with exactly `id` and `boot`. Both come
from one `this_host()` call in `begin`, made after the tombstone refusal and before
`os.makedirs`. Both are written when every value is `null`. `Run._update` is unchanged: it merges
into the status it read, so `host` is carried by `heartbeat`, `heartbeat(pid=…)`, `record` and
`finish`. No other key of the manifest or `status.json` is added, removed or renamed.
`checkpoint.jsonl` and the sidecar are untouched.

- **`id`**: `hashlib.sha256(b"runregistrykit host\0" + raw.encode()).hexdigest()[:16]`, or `null`
  when the raw identity is `None`. The raw identity is never written or returned.
- **The raw identity** (`_read_machine_identity`). On macOS, `gethostuuid(3)` through `ctypes`,
  with a 16-byte buffer and a `timespec` of `(1, 0)`. A nonzero return gives `None`, and so does an
  all-zero buffer. The UUID is formatted by hand as lowercase 8-4-4-4-12 text. On Linux, the first
  of `/etc/machine-id` and `/var/lib/dbus/machine-id` whose stripped, lowercased text is 32 hex
  characters. Elsewhere, `None`.
- **`boot`** (`_read_boot_identity`). On macOS, `sysctlbyname("kern.bootsessionuuid")` with a
  64-byte buffer, decoded as ASCII, NUL and whitespace stripped, `None` if empty. On Linux,
  `/proc/sys/kernel/random/boot_id`, stripped. Elsewhere, `None`. `kern.uuid` is not used.
- **`name`** (`_read_host_name`): `RUNREGISTRYKIT_HOST_NAME` if set and non-empty, else
  `platform.node()`, else `None`.
- Each reader catches `Exception` and returns `None`. `this_host` also calls each through `_ask`,
  which turns a raise, or anything that is not a non-empty string, into `None`, so a patched
  reader that raises gives `None` too. `ctypes` is imported only inside the macOS branches, so
  importing the package loads no `ctypes` (checked: `'ctypes' in sys.modules` is `False` after
  `import runregistrykit` under `-I`).
- `this_host()` reads afresh on every call. Measured here: a mean of **343 µs** over 1000 calls,
  in `venv/`, after one warm-up call.

### How a record is judged

`liveness(status, stale_after, now=None, *, here=None)`:
1. no status → `unknown`; a terminal state → `finished`; any state but `running` → `unknown`, as
   before;
2. `status["host"]` a dict with `id` not `None`, and `id != here["id"]` (`here["id"]` `None`
   included) → `foreign`, with no `pid_alive` call and no heartbeat read;
3. ids equal, both boots not `None` and different → `stale`;
4. otherwise `pid_alive`, then the heartbeat age, as before.

`here` is read with `this_host()` only when a record reaches step 2 and `here` was not given. A
status with no `host`, a `host` that is not a dict, or a `host.id` of `None` goes to step 4 without
reading the host at all. `list_runs` reads `this_host()` once per call (after `os.listdir`
succeeds) and passes it to every `liveness`.

### What `list` prints

A foreign row's marker is `??`, and its PURPOSE · STAGE column begins `on <name or id> · `. The
other columns are unchanged. The summary line ends `; N with no host recorded.`, and N is printed
when it is 0 as well. The stale line now reads "the pid does not answer kill -0, the heartbeat is
older than N s, or this machine has rebooted since". When any run is `foreign`, stderr gets one
more line after the stale one, in the prompt's words, with the hosts in the rows' order,
de-duplicated. The hand run below shows all of it.

## Deviations from the prompt

Each classified. Corrections 1–8 are section 0's.

1. **The suite is slow** (correction 1). Every run wrote its output to a file, and the verdict was
   grepped from it: 197.913 s before; 202.283 s and 119.710 s after; the mutation runs as recorded
   below. The runs after were in the foreground, with a 600 s timeout. The run before, and the eight
   mutation runs, were background commands, with no timeout; the longest took 496 s. **STRUCTURALLY
   REQUIRED** for the files and the times. Running in the background is an **IMPLEMENTATION
   CHOICE**.
2. **The core run** (correction 2): `uv venv -p /opt/local/bin/python3.12` and `uv pip install
   --offline -e` of this checkout, in `agent-01/core`, `TMPDIR` in the scratchpad. It was removed
   afterwards. **STRUCTURALLY REQUIRED.**
3. **The hand run** (correction 3) set `RUNREGISTRYKIT_HOST_NAME=scratch-host`. The log shows the
   `id` digest and writes the boot as `<36-char uuid>`. No raw identity, boot UUID or machine name
   appears in this log, the code, the tests or the commit message. **STRUCTURALLY REQUIRED.**
4. **The Linux readers** (correction 4) are not exercised for real here.
   `test_host.TestTheReaders.test_the_readers_on_linux` is skipped on macOS with its reason, and
   the macOS test runs. The test was not weakened. **STRUCTURALLY REQUIRED.**
5. **`gethostuuid` and `sysctlbyname` through `ctypes`** (correction 5), as the orchestrator called
   them, with `argtypes` and `restype` set. Two differences, each an **IMPLEMENTATION CHOICE**:
   - the buffer is passed as a `c_void_p`, not a typed pointer;
   - the UUID is formatted from the 16 bytes by hand rather than through `uuid.UUID`. A scratch probe
     showed the two agree here: the probe compared them and printed only the comparison, `True`.
6. **`test_public_names.py` not edited** (correction 6). It passes with `this_host` in `__all__`.
   **STRUCTURALLY REQUIRED.**
7. **`black --check runregistrykit docs`**: 30 files (correction 7). **STRUCTURALLY REQUIRED.**
8. **No Orchestrator notes line** added to the board (correction 8). **STRUCTURALLY REQUIRED.**
9. **`_host`, a module-level helper in `__main__.py`**, beside `_purpose` and `_progress`. It is
   used only by `list`: the host a row and the stderr line name, as the name or else the id.
   `__main__.__all__` is unchanged (`["main"]`). **IMPLEMENTATION CHOICE.**
10. **What is "malformed".**
    - A Linux machine-id must be 32 hex characters, its documented form. Otherwise the reader
      tries the next file, then gives `None`.
    - An all-zero `gethostuuid` buffer gives `None`.
    - A boot is malformed only when it is empty or not ASCII.

    **IMPLEMENTATION CHOICE.**
11. **`here` read lazily.** `liveness` calls `this_host()` only when a record carries an id and no
    `here` was given, so a record with no host costs no read. **IMPLEMENTATION CHOICE.**
12. **The `list` layout.**
    - The host goes at the head of the PURPOSE · STAGE column of a foreign row, as `on <host> · `,
      so every existing column keeps its place.
    - The summary's "N with no host recorded" is printed when N is 0 too.
    - The stale line's reboot clause is in the list of causes, not after it.

    **IMPLEMENTATION CHOICE.**
13. **`begin`'s docstring** now says "Every manifest field but three", and has a paragraph for
    `host`. `list_runs`' docstring lists the three new keys, as the prompt asks. **IMPLEMENTATION
    CHOICE** for the first; the prompt asks for the second.
14. **Tests beyond §2.7's list**, each an **IMPLEMENTATION CHOICE**:
    - the Linux branch, run on any platform against files in a temporary directory, with
      `platform.system` patched;
    - the macOS branch, run on any platform with `ctypes.CDLL` and `find_library` patched to fail;
    - `begin` and `list_runs` each read the host once;
    - a status `host` that is null, a list, or a dict with no `id`, judged here;
    - `here` defaulting to a fresh read;
    - `list` with no foreign run prints no `??`;
    - in `test_host_stores`, a foreign run that has finished does not hold its store.
15. **The new test modules' licence header.** The prompt asks for it. The other test modules have
    none: `test_public_names` checks only the five package modules. **STRUCTURALLY REQUIRED.**
16. **No assertion prints an identity read from the machine.** The tests that compare a real id or
    boot use `assertTrue(a == b, message)`, so a failure's message holds no identifier. That
    mattered for (m6), whose failures would otherwise have printed the raw identity. The (m6)
    output was searched afterwards (below). **IMPLEMENTATION CHOICE.**

## Verification performed

### 1. The state at the start

`HEAD` `8023e14`, `main`, clean; `git worktree list` shows this checkout alone. `RAY_ADDRESS`
unset. `venv/`: Python 3.12.15, black 25.1.0. `git status --short --ignored`: `prompts/.DS_Store`,
`runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
`venv/`.

### 2. The suite, before and after

`TMPDIR=<agent-01>/tmp ./venv/bin/python -m unittest discover -s runregistrykit/tests -t . -v`, from
the root. `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` found nothing (exit 1) before
and after each run.

| Module | Before | After |
|---|---:|---:|
| `test_client_root` | 27 | 27 |
| `test_fingerprinter` | 31 | 31 |
| `test_host` | — | **28** (1 skipped: the Linux readers) |
| `test_host_stores` | — | **3** |
| `test_package_imports` | 3 | 3 |
| `test_package_is_generic` | 22 | 22 |
| `test_public_names` | 8 | 8 |
| `test_run_registry` | 29 | 29 |
| `test_store_amend` | 21 | 21 |
| `test_store_amend_residuals` | 9 | 9 |
| `test_store_command_line` | 2 | 2 |
| `test_store_copy_move` | 27 | 27 |
| `test_store_fingerprint` | 29 | 29 |
| `test_store_retire` | 41 | 41 |
| `test_store_retire_references` | 10 | 10 |
| `test_store_sidecar` | 17 | 17 |
| **total** | **276**, `Ran 276 tests in 197.913s`, `OK` | **307**, `Ran 307 tests in 119.710s`, `OK (skipped=1)` |

N = 31. The suite after was run twice:
- `Ran 307 tests in 202.283s`, `OK (skipped=1)`, before a change to two assertions in
  `test_host`. `test_the_readers_on_macos` and `test_the_readers_on_linux` had compared the digest
  with `assertEqual`, which a failure would print. They now use `assertTrue(…, message)`
  (deviation 16).
- `Ran 307 tests in 119.710s`, `OK (skipped=1)`, on the tree committed. The table's counts are
  this run's, and are the same in both. No test that existed at `b56ecc7` was changed (`git diff --stat` touches no test module).
`git status --short --ignored` after the suite was the same as before it, `__pycache__/`
included.

### 3. The core alone

In `agent-01/core`, built as correction 2 (`runregistrykit==0.1.0` from this checkout, editable,
offline). `importlib.util.find_spec` found none of `datastorekit`, `ray`, `sqlalchemy`. From the
repository root:

```
python -m unittest -v runregistrykit.tests.test_run_registry runregistrykit.tests.test_public_names runregistrykit.tests.test_host
Ran 65 tests in 24.189s
OK (skipped=1)
```

29 + 8 + 28 tests; the skip is `test_the_readers_on_linux`. Importing
`runregistrykit.tests.test_host` there under `-I` loaded none of the three. That run, too, was
before the change to the two assertions. So the venv was built again in the same way and the run
repeated on the tree committed: `Ran 65 tests in 14.784s`, `OK (skipped=1)`, the same counts, and
none of the three findable or loaded. Each time the venv was removed afterwards, and `git status
--short --ignored` was unchanged by the run.

### 4. The hand run

A scratch client root, `agent-01/hand/client` with an empty `runregistrykit.toml`, and
`RUNREGISTRYKIT_HOST_NAME=scratch-host`. `begin`, `heartbeat(units_done=1, stage="half way")`,
`finish("done", exit_code=0)`, in `venv/`. The script printed the status's boot only as its length:

```
manifest host: {"id": "8d2b247824882486", "machine": "arm64", "name": "scratch-host", "python": "3.12.15", "release": "27.0.0", "system": "Darwin"}
status host:   {"boot": "<36-char uuid>", "id": "8d2b247824882486"}
status state:  done 0
raw identity in a file: False
id is the digest of the raw identity: True
```

`python -m runregistrykit list` there:

```
   RUN                           STATE      PROGRESS      AGE  PURPOSE · STAGE
   hand-01-host-20261016T135002  done            1/?       0s  the hand run of the host  · half way

1 run(s) under <agent-01>/hand/client/var/runs: 1 finished; 0 with no host recorded.
```

Two more runs were then begun there and edited by hand:
- one whose status says another host (`id` `ffffffffffffffff`, a made-up boot, pid 999999, which
  `pid_alive` answers `False` for here), its manifest's name `far-host`;
- one whose status has no `host`, as `v0.1.0` wrote it, with pid 999999.

`list --root var/runs`, exit 0:

```
   RUN                           STATE      PROGRESS      AGE  PURPOSE · STAGE
?? hand-01-far-20261016T135014   running           -       1s  on far-host · a record from another host, built by hand
!! hand-01-old-20261016T135014   running           -       1s  a record in the form written before the host was recorded
   hand-01-host-20261016T135002  done            1/?      13s  the hand run of the host  · half way

3 run(s) under var/runs: 1 finished, 1 foreign, 1 stale; 1 with no host recorded.
!! 1 run(s) say they are running and are not: the pid does not answer kill -0, the heartbeat is older than 900 s, or this machine has rebooted since. Nothing here has killed or cleaned anything — go and look.
?? 1 run(s) say they are running on another host (far-host): their pids are not tested here. Look on that host.
```

The foreign run has the same dead pid as the stale one and is not called stale. Its pid is not
tested.

### 5. `black`

`./venv/bin/black --check runregistrykit docs`: "30 files would be left unchanged." The five
changed or new Python files were formatted with `./venv/bin/black` first.

### 6. CI

Nothing was pushed. The Linux readers, `/etc/machine-id` and `/proc/sys/kernel/random/boot_id`,
are exercised for real only on CI's `ubuntu-24.04` runners: by `test_the_readers_on_linux` in both
`suite` jobs, and in the `core` job, which now runs `test_host` by name. Locally the Linux branch
ran only against files in a temporary directory (`test_the_linux_files`). **The orchestrator's
review is to read the CI run's `test_host` result**, `test_the_readers_on_linux` above all, once
the user has pushed.

## The deliberate-breakage record

| # | Mutation | Suite | Failing tests (subtests in brackets) |
|---|---|---|---|
| (m1) | step 2 of `liveness` removed: another host's record judged by pid | `Ran 307 tests in 198.686s`, `FAILED (failures=12, skipped=1)` | `test_host.TestTheCommandLine.test_foreign_and_stale_rows_and_the_count_of_records_with_no_host`; `test_host.TestTheJudgement.test_a_record_with_an_id_where_this_host_has_none_is_foreign` [2]; `test_host.TestTheJudgement.test_another_hosts_running_record_is_foreign_and_its_pid_is_not_tested` [5]; `test_host.TestTheJudgement.test_here_defaults_to_this_host_read_afresh`; `test_host_stores.TestARunOnAnotherHostIsInUse.test_a_foreign_run_that_has_finished_is_not_in_use`; `test_host_stores.TestARunOnAnotherHostIsInUse.test_a_host_with_no_name_is_named_by_its_id`; `test_host_stores.TestARunOnAnotherHostIsInUse.test_each_operation_refuses_and_names_the_host` |
| (m2) | step 3 removed: another boot judged by pid | `Ran 307 tests in 293.939s`, `FAILED (failures=2, skipped=1)` | `test_host.TestTheJudgement.test_here_defaults_to_this_host_read_afresh`; `test_host.TestTheJudgement.test_this_host_from_another_boot_is_stale_whatever_its_pid_says` |
| (m3) | a record carrying an id treated as this host's when `here["id"]` is `None` | `Ran 307 tests in 262.377s`, `FAILED (failures=2, skipped=1)` | `test_host.TestTheJudgement.test_a_record_with_an_id_where_this_host_has_none_is_foreign` [2] |
| (m4) | `begin` writing no `host` to `status.json` | `Ran 307 tests in 222.874s`, `FAILED (failures=7, errors=6, skipped=1)` | `test_host.TestTheCommandLine.test_foreign_and_stale_rows_and_the_count_of_records_with_no_host`; `test_host.TestTheCommandLine.test_no_foreign_run_no_foreign_line`; `test_host.TestWhatIsWritten.test_a_failing_reader_writes_null_and_nothing_fails` [3]; `test_host.TestWhatIsWritten.test_every_later_write_keeps_the_status_host` [5]; `test_host.TestWhatIsWritten.test_list_runs_reports_the_host`; `test_host.TestWhatIsWritten.test_no_raw_identity_reaches_a_file`; `test_host.TestWhatIsWritten.test_the_manifest_and_the_first_status` |
| (m5) | `_update` writing only the fields it was given, so a heartbeat drops `host` | `Ran 307 tests in 324.100s`, `FAILED (failures=17, errors=9, skipped=1)` | `test_host.TestTheCommandLine.test_foreign_and_stale_rows_and_the_count_of_records_with_no_host`; `test_host.TestTheCommandLine.test_no_foreign_run_no_foreign_line`; `test_host.TestWhatIsWritten.test_a_failing_reader_writes_null_and_nothing_fails` [3]; `test_host.TestWhatIsWritten.test_every_later_write_keeps_the_status_host` [6]; `test_host.TestWhatIsWritten.test_no_raw_identity_reaches_a_file`; `test_host_stores.TestARunOnAnotherHostIsInUse.test_a_foreign_run_that_has_finished_is_not_in_use`; `test_run_registry.TestLister.test_the_command_line_prints_every_run_and_shouts_about_stale_ones`; `test_run_registry.TestLiveness.test_a_run_whose_process_is_gone_is_stale_not_alive`; `test_run_registry.TestManifest.test_manifest_is_not_mutated_afterwards`; `test_run_registry.TestSelfMatch.test_a_poller_named_after_the_target_does_not_report_it_alive`; `test_store_amend.TestRefusals.test_an_alive_and_a_stale_running_run`; `test_store_copy_move.TestRefusals.test_a_running_run_that_is_stale_still_refuses`; `test_store_fingerprint.TestRunningRefusal.test_refused_alive_or_stale_by_path_or_store_id` [4]; `test_store_retire.TestDryRun.test_refusals_are_the_real_runs`; `test_store_retire.TestRefusals.test_a_stale_running_run_and_its_remedy`; `test_store_retire.TestWithoutFingerprint.test_a_running_run_is_still_refused` |
| (m6) | the raw identity recorded in place of its digest | `Ran 307 tests in 496.243s`, `FAILED (failures=20, skipped=1)` | `test_host.TestTheReaders.test_a_reader_that_fails_gives_none_there` [10]; `test_host.TestTheReaders.test_the_id_is_a_digest_of_the_raw_identity`; `test_host.TestTheReaders.test_the_readers_on_macos`; `test_host.TestWhatIsWritten.test_every_later_write_keeps_the_status_host` [5]; `test_host.TestWhatIsWritten.test_list_runs_reports_the_host`; `test_host.TestWhatIsWritten.test_no_raw_identity_reaches_a_file`; `test_host.TestWhatIsWritten.test_the_manifest_and_the_first_status` |
| (m7) | `_running_runs_naming` skipping `foreign` entries | `Ran 307 tests in 268.257s`, `FAILED (failures=13, skipped=1)` | `test_host_stores.TestARunOnAnotherHostIsInUse.test_a_host_with_no_name_is_named_by_its_id` [6]; `test_host_stores.TestARunOnAnotherHostIsInUse.test_each_operation_refuses_and_names_the_host` [7] |
| (m8) | the agent's own: `list` counting the entries that **have** a host as "with no host recorded" | `Ran 307 tests in 168.736s`, `FAILED (failures=2, skipped=1)` | `test_host.TestTheCommandLine.test_foreign_and_stale_rows_and_the_count_of_records_with_no_host`; `test_host.TestTheCommandLine.test_no_foreign_run_no_foreign_line` |

Each failed at least one test. Some notes on the runs:
- `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` found nothing (exit 1) before and after
  each run, and `git status --short` after each reversal was the same as before the first.
- The times vary, from 168 s to 496 s; no run timed out.
- Under (m5) existing tests fail too. They assert what the mutation breaks (a heartbeat's merge
  keeps `state` and `pid`), and none of them was changed.
- The outputs of all eight runs, the suites before and after, the core run and this log were
  searched for this machine's raw identity (in lowercase, uppercase and undashed forms) and for
  its boot UUID. The search printed only whether each was found, and neither was found in any
  file.


### The diffs

Each was generated in a scratch clone of this repository, with this prompt's tree committed there,
and checked there **as recorded below** with `git apply --check` (on the clean tree) and, once
applied, `git apply -R --check`, in `bash`; then reversed. In the repository each was applied with
`git apply`, the suite run, and reversed with `git apply -R`. After each, `git status --short` was
this prompt's changes and nothing else. None is committed.

#### (m1)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index df214f7..2f659fa 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -496,8 +496,6 @@ def liveness(status, stale_after, now=None, *, here=None) -> str:
     if isinstance(host, dict) and host.get("id") is not None:
         if here is None:
             here = this_host()
-        if host["id"] != here.get("id"):
-            return "foreign"
         boot, current = host.get("boot"), here.get("boot")
         if boot is not None and current is not None and boot != current:
             return "stale"
```

#### (m2)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index df214f7..659d325 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -499,8 +499,6 @@ def liveness(status, stale_after, now=None, *, here=None) -> str:
         if host["id"] != here.get("id"):
             return "foreign"
         boot, current = host.get("boot"), here.get("boot")
-        if boot is not None and current is not None and boot != current:
-            return "stale"
     if not pid_alive(status.get("pid")):
         return "stale"
     age = heartbeat_age(status, now)
```

#### (m3)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index df214f7..65816d0 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -496,7 +496,7 @@ def liveness(status, stale_after, now=None, *, here=None) -> str:
     if isinstance(host, dict) and host.get("id") is not None:
         if here is None:
             here = this_host()
-        if host["id"] != here.get("id"):
+        if here.get("id") is not None and host["id"] != here.get("id"):
             return "foreign"
         boot, current = host.get("boot"), here.get("boot")
         if boot is not None and current is not None and boot != current:
```

#### (m4)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index df214f7..c55b184 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -943,7 +943,6 @@ def begin(
         units_total=expected_units,
         pid=os.getpid() if pid is None else pid,
         exit_code=None,
-        host={"id": host["id"], "boot": host["boot"]},
     )
     return run
 
```

#### (m5)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index df214f7..0703569 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -593,8 +593,7 @@ class Run:
         return read_json(self.status_path) or {}
 
     def _update(self, **fields) -> dict:
-        status = self.status()
-        status.update(fields)
+        status = dict(fields)
         status["heartbeat"] = now_iso()
         write_json_atomic(self.status_path, status)
         return status
```

#### (m6)

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index df214f7..ae58760 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -451,7 +451,7 @@ def this_host() -> dict:
         "id": (
             None
             if raw is None
-            else hashlib.sha256(_HOST_DIGEST_PREFIX + raw.encode()).hexdigest()[:16]
+            else raw
         ),
         "boot": _ask(_read_boot_identity),
         "name": _ask(_read_host_name),
```

#### (m7)

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index 7edee2b..0ff2719 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1014,7 +1014,9 @@ def _running_runs_naming(
         for entry in runs_naming(
             primaries, store_id, runs_root=root, client_root=client
         )
-        if entry["state"] == "running" and os.path.realpath(entry["path"]) != excluded
+        if entry["state"] == "running"
+        and entry["liveness"] != "foreign"
+        and os.path.realpath(entry["path"]) != excluded
     ]
 
 
```

#### (m8)

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index dccdd70..b91dad4 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -569,7 +569,7 @@ def main(argv=None) -> int:
     for entry in entries:
         counts[entry["liveness"]] = counts.get(entry["liveness"], 0) + 1
     summary = ", ".join(f"{n} {name}" for name, n in sorted(counts.items()))
-    unrecorded = sum(1 for entry in entries if not entry["host_recorded"])
+    unrecorded = sum(1 for entry in entries if entry["host_recorded"])
     print(
         f"\n{len(entries)} run(s) under {root}: {summary}; {unrecorded} with no host "
         f"recorded."
```

## Observations not acted on

1. **A write that reads an unreadable status drops `host`.** `Run._update` reads the status as
   `{}` when `status.json` cannot be read, and writes what it was given and a heartbeat. The host,
   like the pid and the progress, is then gone, and the record is judged here as one with no host.
   This is the consequence `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]`
   already records for SGK's second `finish` ("without `pid`, `stage` or `units_*`"), with one more
   field. It is that entry's defect and 02's, so no issue is opened. 02 should know that its fix
   also keeps `host`.
2. **Containers.** A container whose `/etc/machine-id` came with its image reads as the same host
   as every other container made from that image (README §0.2, not measured). The user runs the
   long jobs on Macs (L1), so nothing was done. If a client runs its jobs in containers, it can set
   `RUNREGISTRYKIT_HOST_NAME` for reading, but judging still goes by the id.
3. **Docstrings that list "alive or stale".** The store layer's docstrings and `__main__`'s module
   docstring say the in-use check counts a `running` run "alive or stale"
   (`stores.py:102-107`, `_running_runs_naming`, `_refuse_if_in_use`, `fingerprint_store`,
   `retire_store`, `amend_sidecar`). A `foreign` run is counted too: the behaviour they describe,
   "every `running` run", is unchanged, and only the list of liveness values is short. Outside
   this prompt's files, which allow `_describe_running` alone in `stores.py` and `list` alone in
   `__main__.py`. This is not a defect, so no issue is opened; 06, which writes the README's rules
   for the host, can bring them into line.
4. **The refusals' remedy text for a `foreign` run** still says "A stale run is ended by a person,
   with Run.finish". The prompt leaves the remedy text unchanged, and `end` and its wording are
   04's.
5. **The cost of `this_host()`** is 343 µs here, mostly `ctypes.util.find_library` and `CDLL`,
   called twice. Caching the library handle would cut it, but the prompt asks for no cache, and
   the cost is well under a millisecond.

## State handed to the next prompt

- **The interface after 01:**
  - the manifest's `host` (`id`, `name`, `machine`, `system`, `release`, `python`) and the status's
    (`id`, `boot`), written by `begin` (`runregistrykit/__init__.py:906`, `:931`, `:946`) and kept
    by `Run._update` (`:595`);
  - `this_host()` (`:431`), public;
  - `liveness(..., *, here=None)` (`:465`), whose values are now `alive`, `stale`, `foreign`,
    `finished`, `unknown`;
  - `list_runs` (`:962`), whose entries have `host`, `host_id` and `host_recorded`.
- **For 02:** `Run._update` is as it was. The `host` key is carried by its read-merge-write, so a
  supersession rule that discards a write keeps `host` as it keeps everything else.
- **For 03:** an unreadable status has `host_recorded` false and liveness `unknown`, as before.
- **For 04:** `end` can tell a run on another host (`liveness` `foreign`, `host_id` not this
  host's id) and a run from an earlier boot (`stale` with matching ids and differing boots) from
  the entry and the status. The refusals' remedy text is unchanged.
- **For 06:** the release notes say that `liveness` gains `foreign`, that `this_host` is public,
  and what `host` means in each file: absent means written before 01; null values mean the
  platform offered none. Observation 3 above.
- **CI:** the push is the user's. The first CI run is the first run of the Linux readers.
- The suite is 307, with one skip on macOS (the Linux readers) and, on Linux, one skip of the macOS
  test.
