# Log — prompt 05: begin refuses a second writer

**Subject:** Make begin refuse a store a run that has not finished names, and pid_alive false out of range
**Commit:** this commit (on `main`, after `5d0fa78`)
**Date:** 2026-10-18
**Agent:** Claude Sonnet 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1–18). No stop condition fired.
**Result:** **landed.**
- **`begin` refuses** a `results` store that any run under the runs root it is created in, that
  has not finished, names: `running` (alive, stale or `foreign`) or a status that does not say, by
  the manifest's `results` or its `results_store_id` (the store operations' rule,
  `_running_runs_naming`, called from one more place). It is made after the tombstone check and
  before the run directory is created, only when the runs root is a directory. **There is no
  override**, and it is a check and not a lock. A refusal creates nothing and writes nothing.
- **The words** are 04's: the description of the runs, the stale remedy naming `_END`, 04's
  foreign and unverified sentences each once and only where they apply, then
  `No run directory was created` (§"The refusal, as shipped").
- **`pid_alive`** returns false for a pid outside the platform's range (`2**31` and above, `inf`)
  instead of raising `OverflowError`, at both coercions and nowhere else.
- **A store whose runs have all finished** (`lost` included), a store no run names, a `begin` with
  no `results`, and a runs root that does not exist yet are accepted, as before.
- **Six existing tests change their setup, through one new fixture, and none of their
  assertions.** `StoreTestCase.set_aside(*runs)` moves run directories out of the runs root for
  the duration of a body and back, byte for byte.
- The suite is **378 → 410**: 32 new tests, 23 in the core module `test_second_writer` and 9 in
  the store module `test_second_writer_stores`. The core alone runs 148 (125 + 23), OK, one skip,
  with `datastorekit`, `ray` and `sqlalchemy` not findable. `test_second_writer` passes at 3.13.16.
- Ten mutations, (m1)–(m7), the agent's (m8)–(m10), each caught (§5).
- `[00-begin-does-not-refuse-a-second-writer]` and `[04-a-pid-out-of-range-makes-pid-alive-raise]`
  are **closed**. Nothing is opened. The index counts **12 → 10**.
  `[04-a-killed-process-not-yet-reaped-answers-kill-0]` stays open.
- **Nothing pushed, no tag made, no workflow dispatched.**

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | `pid_alive` (`:403`): one sentence in the docstring (`:411`), `OverflowError` in the `int()` clause (`:415`), and an `except OverflowError: return False` beside the `os.kill` clauses (`:423`). `begin` (`:987`): a docstring paragraph (`:1037-1045`); the lazy import from `.stores` gains `_describe_running`, `_foreign_remedy`, `_running_runs_naming` and `_unsure_remedy` (`:1091-1098`); the check and its refusal after `results_store_id = reading.store_id` (`:1107`), at `:1108-1126`; `this_host()` `:1128` and `os.makedirs` `:1129` follow it unchanged. `__all__` is unchanged |
| `runregistrykit/tests/store_fixtures.py` | `import contextlib`; `StoreTestCase.set_aside` (`:157`), in the runs section |
| `runregistrykit/tests/test_end_stores.py`, `test_store_fingerprint.py`, `test_unreadable_status_stores.py` | The six tests of the prompt's §2.4, by `with self.set_aside(…):` lines, the re-indented call inside each, and two bindings (deviation 2) |
| `runregistrykit/tests/test_second_writer.py` | New, core, 23 tests |
| `runregistrykit/tests/test_second_writer_stores.py` | New, store layer, 9 tests, on `test_end_stores.EndStoresTestCase` (a `RetireTestCase`) |
| `.github/workflows/tests.yml` | The core job's line (`:89`): `runregistrykit.tests.test_second_writer` added |
| this log, `IMPLEMENTATION_STATE.md`, the campaign README's §2 row for 05, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: `stores.py`, `__main__.py`, `client.py`, `fingerprint.py`, `pyproject.toml`, the
repository `README.md`, `PROVENANCE.md`, `CLAUDE.md`, `docs/` but `docs/OPEN_ISSUES.md`, the
prompt, any other part of the campaign README, `orchestrator/`. Not changed in code: `Run.finish`,
`liveness`, `list_runs`, `_end_run`, the writer, `runs_naming`, `_running_runs_naming`,
`_describe_running`, `_unsure_remedy`, `_foreign_remedy`, every store operation and its words,
`store show`, `list`, `end`, `__all__`. `test_run_registry.RegistryTestCase`, `test_host.a_status`,
`test_unreadable_status.FORMS`, `test_end.a_hard_killed_run` and `test_store_retire.RetireTestCase`
are imported, not edited.

### The refusal, as shipped

For one run that is alive in the process that asks (the temporary directory shown as `<root>`, the
ids' stamps as `<stamp>`, the pid as `N`):

```
Cannot begin run example-01-second-<stamp> with results "<root>/results.sqlite": run example-01-alive-<stamp> is running (alive, pid N) and names this store by its results. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
```

For an alive run, a run on another host and a run whose status cannot be read, together (the host's
name shown as `<host>`): every sentence is there once, the foreign one first.

```
Cannot begin run example-01-second-<stamp> with results "<root>/results.sqlite": run example-01-elsewhere-<stamp> is running on another host, <host> (pid N, not tested here), and names this store by its results; run example-01-torn-<stamp>'s status cannot be read (status.json is missing, is not JSON, or is not a JSON object), so whether it is running cannot be told; it names this store by its results; run example-01-alive-<stamp> is running (alive, pid N) and names this store by its results. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. A run on another host is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT` on that host, or here with `--unverified` once they have checked there. A run whose status does not say whether it is running is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT --unverified`, once they have checked that it is not. No run directory was created
```

It is composed as `_refuse_if_in_use` composes its own (`described`, `foreign`, `unsure` each
computed once), with `_END` from this module and `No run directory was created` last with no full
stop, as the tombstone refusal beside it ends. `test_the_whole_text_for_an_alive_run` and
`test_the_whole_text_for_a_stale_run` pin the full text for one alive and one stale run. No new
text uses the word `signal`.

## Deviations from the prompt

The orchestrator's corrections and readings of the prompt, recorded as found (1–18), then the
agent's own.

1. **Correction 1: L9 is (a), and the pid fix is the user's request** (README §6.2, the board's
   decisions table and the issue's **Assigned** line, `f3cc239`). Nothing in the prompt is
   conditional on them. STRUCTURALLY REQUIRED (the prompt as written already says so; recorded as
   found).
2. **Correction 6: the fixture, and the two unbound runs.** `set_aside` is a
   `contextlib.contextmanager` method of `StoreTestCase`, taking `Run`s; it makes
   `tempfile.mkdtemp(dir=self.top, prefix="set-aside-")`, `os.rename`s each run's directory into
   it, yields, and in a `finally` renames each back and removes the directory, failing loudly
   (`FileExistsError`) where the path to move back to exists. Each `with` covers only the statement
   that begins a run and sets aside every unfinished run naming the store at that moment (two
   `with`s in `test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once`). Two of the six
   (`test_alive_and_stale_here_give_the_old_text_with_the_command` and
   `test_a_refusal_for_running_runs_alone_has_no_new_sentence`) called `self.a_running_run("alive",
   primary)` as a bare statement; each is now bound (`alive = …`) so it can be set aside.
   STRUCTURALLY REQUIRED (the bindings; §3.5's diff shows them).
3. **Correction 2: the suite's time.** Run in the foreground with a timeout of 900 000 ms, output
   to a file, the verdict grepped. 140.6 s with the six tests wrapped and before the new modules,
   144.3 s and 147.0 s with them. IMPLEMENTATION CHOICE (a reading of the instructions; no
   departure).
4. **Correction 3: the core run.** `uv venv -p /opt/local/bin/python3.12`, `uv pip install
   --offline -e`, `TMPDIR` in scratch, the three dependencies shown not findable, the **seven**
   core modules by name: 125 → 148. Removed afterwards. Also `test_second_writer` at
   `/opt/local/bin/python3.13` with `PYTHONPATH` on the checkout. IMPLEMENTATION CHOICE.
   **A side effect, recorded:** `uv pip install -e` regenerated the checkout's ignored
   `runregistrykit.egg-info/` (its five files), which has no `direct_url.json`. With the
   checkout first on `sys.path`, `importlib.metadata` finds it before `venv/`'s dist-info, so a
   manifest's `packages.runregistrykit.url` read `null` where the `5e20772` archive's read a
   `file://` url. The lifecycle comparison of §4 was therefore taken from a copy of the tree
   without the egg-info (`git ls-files -co --exclude-standard`). The suite was re-run after the
   install (410, OK): no test is sensitive to it. The directory is ignored and untracked.
5. **Correction 4: where the check sits.** Inside `if results:`, after `results_store_id =
   reading.store_id` and before the comment and `this_host()`; `reading.store_id` passed as it is;
   `runs_root = root or client.runs_root` computed once for the check and `path`'s own expression
   left as it was (its value unchanged); `os.path.isdir` guards the call; the refusal is raised
   before anything is created; nothing is excluded. STRUCTURALLY REQUIRED.
6. **Correction 5: the words.** Composed as `_refuse_if_in_use` composes them, `_END` used and not
   imported, the lazy import extended by the four names. STRUCTURALLY REQUIRED. A test that pins
   the full text for one alive and one stale run is included.
7. **Correction 7: `begin`'s `root`.** `RegistryTestCase.begin` passes `root=self.root` itself, so
   the tests that begin under another runs root call `runregistrykit.begin` through a small helper
   of the new module's own (`begin_under`), with the keywords `RegistryTestCase.begin` gives.
   `RegistryTestCase` is not edited. STRUCTURALLY REQUIRED.
8. **Correction 8: the core module's stores.** In `RegistryTestCase` the runs root is the temporary
   directory; each store is a plain file of the module's own in the runs root, with no sidecar
   (`a_plain_store`), so a run matches it by path; "listing unchanged" is a full walk of the root
   with each file's bytes (`snapshot`). STRUCTURALLY REQUIRED.
9. **Correction 9: an earlier boot, another host, the platform.** The earlier-boot and foreign
   tests skip with a reason where `this_host()` gives no `boot` or `id`. macOS has both, so no new
   skip runs here and the suite stays at one skip. **The review reads the skip count in CI.**
   STRUCTURALLY REQUIRED.
10. **Correction 10: `pid_alive`.** `except (TypeError, ValueError, OverflowError)` at `int()` and
    `except OverflowError: return False` at `os.kill`; nothing broader. Measured here at 3.12.15:
    `os.kill` raises `OverflowError` for `2**31`, `2**63` and `10**30`, and `int(float("inf"))`
    raises `OverflowError`; `int(nan)` raises `ValueError`, already caught (the test includes
    `nan`). (m8) is `int()`'s clause left uncaught. STRUCTURALLY REQUIRED.
11. **Correction 11: through the readers.** `python -m runregistrykit list --root` as
    `test_unreadable_status`'s command-line tests run it; exit 0 and the row marked `!!`;
    `_end_run` accepts the `2**31` run, `ended.verified` true, `evidence.pid_answers` false. For
    the `Infinity` form the status's bytes are written by hand and `read_json` is asserted to give
    `float("inf")` first. **What `_end_run` writes back for `evidence.pid` is 04's, not changed
    here:** it copies the status's `pid`, so `2**31` is written as `2147483648` and `Infinity` is
    written by `json` as `Infinity` (parsed back as `inf`); recorded, not changed. STRUCTURALLY
    REQUIRED.
12. **Correction 12: the stores module's base.** `test_end_stores.EndStoresTestCase` (a
    `RetireTestCase`), imported as a module (`from runregistrykit.tests import test_end_stores`),
    so the loader runs no test twice; the per-module counts (§2) show it. STRUCTURALLY REQUIRED.
13. **Correction 13: the acceptance test's order.** `a_hard_killed_run` (killed, reaped); the
    second `begin` refused with the tree unchanged, naming the killed run and
    `runregistrykit end RUN_ID`; `end` by the command; `begin` again; `finish("done", exit_code=0,
    fingerprint=True)` records a `fingerprint` and no `fingerprint_error`. No zombie is built.
    STRUCTURALLY REQUIRED.
14. **Correction 14: observations, not fixes.** Recorded under "Observations not acted on".
15. **Correction 15: mutation diffs** taken after `black`, from the tree as it will be committed,
    and replayed as recorded (§5): `git apply --check`, apply, the two new modules, `git apply -R
    --check`, `git checkout`, `git status` clean in the clone. STRUCTURALLY REQUIRED.
16. **Correction 16: line citations** taken from `grep -n` on the files as left after `black`.
    STRUCTURALLY REQUIRED.
17. **Correction 17: `black`.** 35 files at `5e20772`, 37 after. STRUCTURALLY REQUIRED.
18. **Correction 18: the records.** 05's status is "landed, not yet reviewed" in the board's §1
    row, the README's §2 row and `prompts/INDEX.md`; the board's Orchestrator notes line and the
    README's header paragraph are not edited. STRUCTURALLY REQUIRED.
19. **The order test is in the store module, not the core's.** The prompt's §2.7 lists "the order"
    (a tombstone and a stale run naming it, refused by the tombstone's words) under the core
    module. A tombstone cannot be built without the store layer (`retire_store`), and the core
    module imports none. It is `test_second_writer_stores.TestTheOrder`: the run is set aside while
    the store is retired, put back, and `begin` is refused by the tombstone's words and not the
    check's. IMPLEMENTATION CHOICE.
20. **The core module's multi-run rows move the existing runs aside by hand.** `StoreTestCase`
    imports the store layer, so the core module cannot use `set_aside`. Its `an_earlier_run` moves
    each directory already under the runs root to a temporary directory, begins the run, and moves
    them back (the same `os.rename`). The foreign sentence "once with two foreign runs", the
    unverified sentence "once with two unreadable runs" and the 13-forms rows need two unfinished
    runs on one store, which `begin` no longer makes. IMPLEMENTATION CHOICE.
21. **Two store-module tests beyond the prompt's list.**
    `test_alive_stale_foreign_and_unreadable_are_refused_each_with_no_directory` and
    `test_a_store_whose_runs_have_all_finished_is_accepted` put the prompt's §4.3 acceptance rows
    (a live run's store, a stale run's, a `foreign` run's, an unreadable status's, each with no
    run directory left; all-terminal accepted) on registered stores, end to end, and
    `TestTheFixture` is the one fixture test correction 6 allows. IMPLEMENTATION CHOICE.
22. **The fixture test compares the tree but for the runs root's own mtime.** Any `os.rename` into a
    directory moves its mtime, and `tree_state` records directory mtimes; the test compares every
    other entry (files by hash and mtime, run directories by mtime), and the runs root's names.
    The first draft compared the whole tree and failed on that. IMPLEMENTATION CHOICE.

No UNINTENDED DRIFT.

## Verification performed

### 1. The state at the start

`HEAD` `5d0fa78`, `main`, clean, this checkout the only worktree; `git diff --stat 5e20772 HEAD --
runregistrykit pyproject.toml .github` empty. `Ran 378 tests … OK (skipped=1)` at the gate
(`Ran 378 tests in 139.779s`, the orchestrator's). `venv/`: Python 3.12.15, `black` 25.1.0. No Ray
process (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` empty before and after each suite
run); `RAY_ADDRESS` unset; Ray was never started.

### 2. The suite, before and after

Before: 378, as above. With the six tests wrapped and the fixture, before the new modules:
`Ran 378 tests in 140.602s`, `OK (skipped=1)`. After: **`Ran 410 tests in 144.314s`, `OK
(skipped=1)`**, and again after the core install of deviation 4, **`Ran 410 tests in 147.032s`,
`OK (skipped=1)`**. `git status --short --ignored` the same before and after; no child left.

By the loader (the new modules in bold): `test_client_root` 27, `test_end` 27, `test_end_stores`
4, `test_fingerprinter` 31, `test_host` 28, `test_host_stores` 3, `test_package_imports` 3,
`test_package_is_generic` 22, `test_public_names` 8, `test_run_registry` 29,
**`test_second_writer` 23**, **`test_second_writer_stores` 9**, `test_status_writes` 22,
`test_store_amend` 21, `test_store_amend_residuals` 9, `test_store_command_line` 2,
`test_store_copy_move` 27, `test_store_fingerprint` 29, `test_store_retire` 41,
`test_store_retire_references` 10, `test_store_sidecar` 17, `test_unreadable_status` 11,
`test_unreadable_status_stores` 7: 410. The skip is `test_the_readers_on_linux`.

**The core alone** (`uv venv -p /opt/local/bin/python3.12`, `uv pip install --offline -e`; the
three dependencies shown not findable by `importlib.util.find_spec`): the seven modules,
`Ran 148 tests in 44.241s`, `OK (skipped=1)` (125 + 23). Removed afterwards.
**3.13.16**: `test_second_writer`, `PYTHONPATH` on the checkout, `-I` for the version check,
`Ran 23 tests`, `OK`.

### 3. The probes, against `5e20772` and this tree

The planner's probe (`probes/probe.py`, scratch, unedited), a second `begin` on a full store, each
row its own store; "no dir left": the runs root's listing unchanged by the refusal. At `5e20772`
(by `git archive`) and at this tree:

| The earlier run | `5e20772` | This tree |
|---|---|---|
| alive, in the probe's own process | **begun** | refused, no dir left |
| stale (a dead pid) | **begun** | refused, no dir left |
| `foreign` (`host.id` another) | **begun** | refused, no dir left |
| a torn `status.json` | **begun** | refused, no dir left |
| state `"paused"` | **begun** | refused, no dir left |
| every one terminal (`done`, `failed`, `killed`, `lost`) | begun | begun |
| none | begun | begun |
| stale, its `pid` set to `2**31`, on its own store | **begun** | refused, no dir left |
| on **another** store, its `pid` `2**31` | **begun** | begun |
| none, the runs root absent | begun | begun |

Unlike the candidate of the prompt's "At writing", the `2**31` rows no longer raise `OverflowError`:
the record is read as stale, refused on its own store, and no obstacle to another.

**The cost** (`probes/cost.py`, best of five, `begin` with `results`, N finished runs under the
root): `5e20772`: 0 runs 54.9 ms, 100 runs 54.8 ms, 1000 runs 55.9 ms; this tree: 56.8 ms, 67.2 ms,
306.9 ms. SGK's `var/runs/` holds 83 run directories. (Observation 3.)

### 4. What is written

`probes/lifecycle.py` (scratch, mine): `begin` on a full registered store with `checkpoint=True`,
`heartbeat(units_done=1)`, `record`, `finish("done", exit_code=0, fingerprint=True)`; the shape (keys,
recursively, and the type of each value) of `status.json`, `manifest.json`, the ledger's line and the
sidecar, and the run directory's file list, taken from the `5e20772` archive and from a copy of this
tree: **`cmp` identical** (4708 bytes each). A refusal writes nothing (the runs root and the whole
tree are compared in every refusal test). The manifest, `status.json`, `checkpoint.jsonl` and every
sidecar are unchanged in form; `write_json_atomic` and the writer are untouched. See deviation 4 for
the egg-info.

### 5. The six tests' setup

`git diff -w 5e20772 -- runregistrykit/tests/test_end_stores.py runregistrykit/tests/test_store_fingerprint.py
runregistrykit/tests/test_unreadable_status_stores.py`: only the `with` lines and the two
bindings (the fixture is in `store_fixtures.py`):

```diff
diff --git a/runregistrykit/tests/test_end_stores.py b/runregistrykit/tests/test_end_stores.py
index 144bcab..8ecbafa 100644
--- a/runregistrykit/tests/test_end_stores.py
+++ b/runregistrykit/tests/test_end_stores.py
@@ -147,6 +147,7 @@ class TestTheWords(EndStoresTestCase):
                 "boot": "a-boot",
             },
         )
+        with self.set_aside(run):
             stale = self.a_stale_run("stale", primary)
         for operation, message in self.refusals(primary).items():
             with self.subTest(operation):
@@ -169,7 +170,8 @@ class TestTheWords(EndStoresTestCase):
 
     def test_alive_and_stale_here_give_the_old_text_with_the_command(self):
         primary = self.a_full_store()
-        self.a_running_run("alive", primary)
+        alive = self.a_running_run("alive", primary)
+        with self.set_aside(alive):
             self.a_stale_run("stale", primary)
         client = runregistrykit.find_client_root(client_root=self.client)
         store_id = stores.read_sidecar(primary).store_id
diff --git a/runregistrykit/tests/test_store_fingerprint.py b/runregistrykit/tests/test_store_fingerprint.py
index 8f05474..628c184 100644
--- a/runregistrykit/tests/test_store_fingerprint.py
+++ b/runregistrykit/tests/test_store_fingerprint.py
@@ -737,6 +737,7 @@ class TestFinish(_FullStoreCase):
     def test_another_running_run_is_recorded_and_the_run_still_ends(self):
         primary = self.a_full_store()
         other = self.a_running_run("other", primary)
+        with self.set_aside(other):
             run = self.begin("second", results=str(primary))
         status = run.finish("failed", exit_code=2, fingerprint=True)
         self.assertEqual((status["state"], status["exit_code"]), ("failed", 2))
diff --git a/runregistrykit/tests/test_unreadable_status_stores.py b/runregistrykit/tests/test_unreadable_status_stores.py
index 8a04e92..5cae1c2 100644
--- a/runregistrykit/tests/test_unreadable_status_stores.py
+++ b/runregistrykit/tests/test_unreadable_status_stores.py
@@ -121,6 +121,7 @@ class TestAnUnreadableStatusIsInUse(test_store_retire.RetireTestCase):
         primary = self.a_full_store()
         predecessor = self.a_running_run("predecessor", primary)
         give_status_the_form(predecessor, TORN)
+        with self.set_aside(predecessor):
             run = self.begin("resumed", results=str(primary))
         status = run.finish("done", exit_code=0, fingerprint=True)
         self.assertEqual((status["state"], status["exit_code"]), ("done", 0))
@@ -149,8 +150,10 @@ class TestAnUnreadableStatusIsInUse(test_store_retire.RetireTestCase):
     def test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once(self):
         primary = self.a_full_store()
         stale = self.a_stale_run("stale", primary)
+        with self.set_aside(stale):
             torn = self.a_running_run("torn-too", primary)
         give_status_the_form(torn, TORN)
+        with self.set_aside(stale, torn):
             unnamed = self.a_running_run("no-state", primary)
         give_status_the_form(
             unnamed, dict((n, m) for n, m, _, _ in FORMS)["empty object"]
@@ -173,7 +176,8 @@ class TestAnUnreadableStatusIsInUse(test_store_retire.RetireTestCase):
 
     def test_a_refusal_for_running_runs_alone_has_no_new_sentence(self):
         primary = self.a_full_store()
-        self.a_running_run("alive", primary)
+        alive = self.a_running_run("alive", primary)
+        with self.set_aside(alive):
             self.a_stale_run("stale", primary)
         for operation, call in self.refusals(primary, 0).items():
             with self.subTest(operation):
```

Each of the six, run against the change **with its `with` removed** (the three test modules taken
from `5e20772` in a scratch clone, the package and the fixture as they are), errors at its `begin`
(`Cannot begin run example-01-… with results …`): `test_a_run_on_another_host_adds_the_sentence_once`
at `stale`, `test_alive_and_stale_here_give_the_old_text_with_the_command` at `stale`,
`test_another_running_run_is_recorded_and_the_run_still_ends` at `second`,
`test_a_refusal_for_running_runs_alone_has_no_new_sentence` at `stale`,
`test_a_resumed_runs_fingerprint_is_refused_by_an_unreadable_predecessor` at `resumed` and
`test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once` at `torn-too`: `Ran 6 tests`,
`FAILED (errors=6)`, as the prompt measured. With the `with`s in, they pass, asserting what they
asserted.

### 6. Nothing outside temporary directories, nothing else signalled

`git status --short --ignored` the same before and after each suite run; no `var/` change. The only
signal is `SIGKILL` to the child `test_end.a_hard_killed_run` starts, which it reaps (`-9`); no
zombie is built. `git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'` finds
`__init__.py:818` alone, `Run.finish`'s docstring.

### 7. `black`

`black --check runregistrykit docs`: 37 files unchanged (35 at `5e20772`, and the two new modules).

### 8. CI

Pushing is the user's. `test_second_writer` first runs in the core job and on Linux; **the review
reads its result there**: the core job's count should be 148 with `test_second_writer` on its line,
and the skip count in each job (the earlier-boot and foreign tests skip only where the platform gives
no boot or host id).

## The deliberate-breakage record

Each applied in a scratch `git clone` of this repository holding the tree as it is committed (after
`black`), the two new modules run, then reverted, the clone clean after each. Diffs as applied
(`git apply --check` against the clone, then `git apply`).

**(m1)** `begin`'s check removed (the `if os.path.isdir(runs_root):` block, through the refusal).

Caught: 21 failures and 15 errors (of the 32 new tests): every refusal row of `test_second_writer` (`test_an_alive_run_in_this_process`, `test_a_stale_run`, `test_a_run_on_another_host_is_foreign`, `test_a_run_from_an_earlier_boot_of_this_host_is_stale`, `test_each_of_the_thirteen_unreadable_forms`, `test_a_v010_status_judged_by_its_pid`), the words (`test_the_whole_text_for_an_alive_run`, `…_for_a_stale_run`, `test_the_stale_remedy_names_the_command_once`, the foreign and unverified sentence tests), the remedy (`test_a_stale_run_is_ended_and_then_begin_is_accepted`), and in `test_second_writer_stores` the acceptance test `test_a_hard_killed_run_blocks_begin_until_it_is_ended`, `test_by_store_id_alone`, `test_by_path_alone_when_there_is_no_sidecar`, `test_begin_and_each_store_operation_refuse_naming_the_same_run`, `test_alive_stale_foreign_and_unreadable_are_refused_each_with_no_directory`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..672b655 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1108,22 +1108,6 @@ def begin(
         # a store a run that has not finished names is refused, as the store operations refuse
         # it: the registry takes no lock, and does not decide that a stale run is dead
         runs_root = root or client.runs_root
-        if os.path.isdir(runs_root):
-            running = _running_runs_naming(
-                "begin", [os.path.abspath(results)], results_store_id, runs_root, client
-            )
-            if running:
-                described = _describe_running(running)
-                foreign = _foreign_remedy(running)
-                unsure = _unsure_remedy(running)
-                raise RuntimeError(
-                    f'Cannot begin run {identifier} with results "{results}": {described}. '
-                    f"A stale run is ended by a person, with `{_END}`, before another run is "
-                    f"begun on its store; the registry does not decide that a run is dead. "
-                    f"{foreign + '. ' if foreign else ''}"
-                    f"{unsure + '. ' if unsure else ''}"
-                    f"No run directory was created"
-                )
     # the machine and the boot this run's pid belongs to, read once, before anything is created
     host = this_host()
     os.makedirs(path, exist_ok=True)
```

**(m2)** the check counting only `alive` runs.

Caught: 15 failures and 12 errors: `test_a_stale_run`, `test_a_run_from_an_earlier_boot_of_this_host_is_stale`, `test_a_run_on_another_host_is_foreign`, `test_each_of_the_thirteen_unreadable_forms`, `test_a_v010_status_judged_by_its_pid`, `test_the_whole_text_for_a_stale_run`, the foreign and unverified sentence tests, `test_a_stale_run_is_ended_and_then_begin_is_accepted`, `test_infinity_in_a_record_does_not_stop_a_begin_on_another_store`, `test_a_record_with_such_a_pid_does_not_stop_a_begin_on_another_store`, and in the store module `test_a_hard_killed_run_blocks_begin_until_it_is_ended` and `test_alive_stale_foreign_and_unreadable_are_refused_each_with_no_directory`. The alive-only rows (`test_an_alive_run_in_this_process`, `test_by_path_alone_when_there_is_no_sidecar`) pass, as they should.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..7c3b8a9 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1112,6 +1112,7 @@ def begin(
             running = _running_runs_naming(
                 "begin", [os.path.abspath(results)], results_store_id, runs_root, client
             )
+            running = [e for e in running if e["liveness"] == "alive"]
             if running:
                 described = _describe_running(running)
                 foreign = _foreign_remedy(running)
```

**(m3)** the check made after `os.makedirs`, so a refusal leaves a run directory.

Caught: 20 failures. The directory left is seen by `SecondWriterTestCase.assertRefusedBegin` (the runs root's listing unchanged: `test_an_alive_run_in_this_process`, `test_a_stale_run`, `test_each_of_the_thirteen_unreadable_forms`, the sentence tests and others of `test_second_writer`) and by `SecondWriterStoresTestCase.refused_begin` (`self.state()` unchanged: `test_a_hard_killed_run_blocks_begin_until_it_is_ended`, `test_by_store_id_alone`, `test_by_path_alone_when_there_is_no_sidecar`, `test_begin_and_each_store_operation_refuse_naming_the_same_run`).

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..d0b5666 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1105,6 +1105,10 @@ def begin(
                 f"directory was created"
             )
         results_store_id = reading.store_id
+    # the machine and the boot this run's pid belongs to, read once, before anything is created
+    host = this_host()
+    os.makedirs(path, exist_ok=True)
+    if results:
         # a store a run that has not finished names is refused, as the store operations refuse
         # it: the registry takes no lock, and does not decide that a stale run is dead
         runs_root = root or client.runs_root
@@ -1124,9 +1128,6 @@ def begin(
                     f"{unsure + '. ' if unsure else ''}"
                     f"No run directory was created"
                 )
-    # the machine and the boot this run's pid belongs to, read once, before anything is created
-    host = this_host()
-    os.makedirs(path, exist_ok=True)
     if os.path.exists(os.path.join(path, "manifest.json")):
         raise FileExistsError(
             f"{path} already holds a manifest; a manifest is written once"
```

**(m4)** the check passed `None` for the store id, so a run named by `results_store_id` alone is not seen.

Caught: 1 failure: `test_second_writer_stores.TestMatching.test_by_store_id_alone`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..e0c7cf6 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1110,7 +1110,7 @@ def begin(
         runs_root = root or client.runs_root
         if os.path.isdir(runs_root):
             running = _running_runs_naming(
-                "begin", [os.path.abspath(results)], results_store_id, runs_root, client
+                "begin", [os.path.abspath(results)], None, runs_root, client
             )
             if running:
                 described = _describe_running(running)
```

**(m5)** a runs root that does not exist refused (the `isdir` guard replaced by `if True:`, so `_running_runs_naming` is called unconditionally).

Caught: 2 errors: `test_second_writer.TestEveryAcceptance.test_a_runs_root_that_does_not_exist_yet_is_created` (the test of the runs root that does not exist) and `test_a_run_under_another_runs_root_is_not_seen` (its `runs-a` and `runs-b` do not exist before the first `begin` under them).

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..f7b0514 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1108,7 +1108,7 @@ def begin(
         # a store a run that has not finished names is refused, as the store operations refuse
         # it: the registry takes no lock, and does not decide that a stale run is dead
         runs_root = root or client.runs_root
-        if os.path.isdir(runs_root):
+        if True:
             running = _running_runs_naming(
                 "begin", [os.path.abspath(results)], results_store_id, runs_root, client
             )
```

**(m6)** `pid_alive`'s `OverflowError` at `os.kill` not caught.

Caught: 7 errors: `test_second_writer.TestPidAlive.test_a_pid_out_of_range_is_false_and_does_not_raise`, `test_through_the_readers_for_a_pid_out_of_range`, `test_a_record_with_such_a_pid_does_not_stop_a_begin_on_another_store`, and in the store module `test_a_pid_out_of_range_is_stale_and_blocks_only_its_own_store` (some of them in more than one subtest).

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..a677cc7 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -420,8 +420,6 @@ def pid_alive(pid) -> bool:
         os.kill(pid, 0)
     except ProcessLookupError:
         return False
-    except OverflowError:  # outside a C int or long: no process has such a pid
-        return False
     except PermissionError:  # exists, owned by somebody else
         return True
     except OSError:
```

**(m7)** the remedy sentence not naming `_END`.

Caught: 30 failures: every test that reads the sentence or the whole text, `test_the_whole_text_for_an_alive_run`, `…_for_a_stale_run` and `test_the_stale_remedy_names_the_command_once` among them, and the store module's acceptance test and `test_begin_and_each_store_operation_refuse_naming_the_same_run`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..e1ed21d 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1118,7 +1118,7 @@ def begin(
                 unsure = _unsure_remedy(running)
                 raise RuntimeError(
                     f'Cannot begin run {identifier} with results "{results}": {described}. '
-                    f"A stale run is ended by a person, with `{_END}`, before another run is "
+                    f"A stale run is ended by a person, with `end`, before another run is "
                     f"begun on its store; the registry does not decide that a run is dead. "
                     f"{foreign + '. ' if foreign else ''}"
                     f"{unsure + '. ' if unsure else ''}"
```

**(m8)** (the agent's own, correction 10's) `int()`'s `OverflowError` left uncaught in `pid_alive`.

Caught: 3 errors: `test_a_pid_out_of_range_is_false_and_does_not_raise` (the `float('inf')` subtest), `test_through_the_readers_for_a_pid_out_of_range` (the JSON `Infinity` subtest) and `test_infinity_in_a_record_does_not_stop_a_begin_on_another_store`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..e8694a9 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -412,7 +412,7 @@ def pid_alive(pid) -> bool:
     """
     try:
         pid = int(pid)
-    except (TypeError, ValueError, OverflowError):
+    except (TypeError, ValueError):
         return False
     if pid <= 0:
         return False
```

**(m9)** (the agent's own) the check reading `client.runs_root` instead of the root the run is created in.

Caught: 22 failures and 14 errors: the tests give `root=` a temporary directory that is not the client's `runs_root` (which does not exist), so the guard finds no directory and nothing is refused; the whole refusal set fails, `test_a_run_under_another_runs_root_is_not_seen` is not among them (it passes either way, by design of the guard).

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..17e2df4 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1107,7 +1107,7 @@ def begin(
         results_store_id = reading.store_id
         # a store a run that has not finished names is refused, as the store operations refuse
         # it: the registry takes no lock, and does not decide that a stale run is dead
-        runs_root = root or client.runs_root
+        runs_root = client.runs_root
         if os.path.isdir(runs_root):
             running = _running_runs_naming(
                 "begin", [os.path.abspath(results)], results_store_id, runs_root, client
```

**(m10)** (the agent's own) the foreign sentence dropped from the refusal.

Caught: 2 failures: `test_a_run_on_another_host_is_foreign` and `test_the_foreign_sentence_is_once_with_two_foreign_runs_and_absent_with_none`.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 8aa4ca9..65597b8 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1120,7 +1120,6 @@ def begin(
                     f'Cannot begin run {identifier} with results "{results}": {described}. '
                     f"A stale run is ended by a person, with `{_END}`, before another run is "
                     f"begun on its store; the registry does not decide that a run is dead. "
-                    f"{foreign + '. ' if foreign else ''}"
                     f"{unsure + '. ' if unsure else ''}"
                     f"No run directory was created"
                 )
```


## Observations not acted on

1. **The race.** Two `begin`s at the same moment both pass the check; `begin`'s docstring says so.
   A check, not a lock (README §5 rule 9; L9).
2. **A run under another runs root is not seen**, stated in the docstring and pinned by
   `test_a_run_under_another_runs_root_is_not_seen`.
3. **The cost grows with the runs root.** `begin` with `results` costs about 250 ms more with 1000
   runs under the root (306.9 ms against 55.9 ms), 12 ms more with 100; SGK's holds 83.
   `list_runs` reads every manifest and status. Not a defect at the sizes the clients have.
4. **`_end_run` copies the status's `pid` into `evidence.pid` as it is** (deviation 11): `2147483648`,
   or `Infinity`, which is not valid JSON and which `json` writes and reads back. 04's, and no
   writer of the registry records such a pid. Not opened.
5. **A `pid` of JSON `true` is `int` 1** and answers `kill -0` (`PermissionError`): such a run is
   `alive` (the prompt's "At writing"). No writer records one; erring towards in use.
6. **The checkout's ignored `runregistrykit.egg-info/`** was regenerated by the allowed core
   install (deviation 4). It does not enter the repository.
7. **`begin` still refuses a killed child not yet reaped**, as
   `[04-a-killed-process-not-yet-reaped-answers-kill-0]` records; unchanged.
8. Nothing was found in `liveness`, `list_runs`, `store show`, `end` or the store operations.

## State handed to the next prompt

- `begin` with `results` refuses what the store operations refuse, in 04's words, before it creates
  anything; there is no override, and the remedy for a stale run is `end`, then `begin` again.
  `pid_alive` is false for a pid out of range; 06's release notes say that its value for such a pid
  goes from raising to `False`.
- **06** (the release): the README's usage for `begin`'s refusal; the release notes' line on
  `pid_alive`; nothing the registry writes has changed since 04. The five open §3 issues are
  unchanged; `docs/OPEN_ISSUES.md` counts 10.
- The core job names seven modules; the suite is 410.
