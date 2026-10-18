# Log — prompt 03: an unreadable status is in use

**Subject:** Count a run whose status does not say it has finished as in use
**Commit:** `ab0cad9` (on `main`, after `75eab12`)
**Date:** 2026-10-18
**Agent:** Claude Sonnet 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (corrections and readings 1–16). No stop condition fired.
**Result:** **landed.**
- `_running_runs_naming` keeps every run that names the store and whose state is **not in
  `TERMINAL_STATES`** (`runregistrykit/stores.py:1023`), where it kept only `running`. A status
  that is missing, empty, torn, not JSON, not a JSON object, has no state, a `null` state, a state
  that is not a string, or a string the registry never writes, is in use as a `running` one is.
  The five refusals say which, and that the registry cannot tell whether the run is running.
- `list` marks such a run `!!` when it has a manifest, with one line on stderr that counts them.
- A status, or a manifest, that is JSON but not an object is read as unreadable and never raised
  on: `list_runs`, `liveness`, `Run.status()` and the writer's base read go through one helper,
  `_json_object` (`runregistrykit/__init__.py:247`). So `list` lists, the store operations refuse
  where they raised, and `Run.finish`, the remedy the refusals name, ends the run.
- The planner's probe, as a test: for each of the thirteen forms of `status.json`, copy, move,
  fingerprint, fingerprint `--write`, retire's dry run and amend each refuse, naming the run and
  the form's words, and every file under the temporary directory is as it was. Against `35ce264`
  the same probe found all six operations proceeding in ten forms and raising in three.
- **Nothing written changes:** no key of `status.json`, the manifest, `checkpoint.jsonl` or a
  sidecar is added, removed or renamed; `write_json_atomic` (`:255`) is byte for byte as it was.
  `list_runs`' entries gain one key, `status_readable`: a return value, not a file.
- The suite is **329 → 347**: 18 new tests, 11 in the core module `test_unreadable_status` and 7 in
  the store module `test_unreadable_status_stores`. The core alone runs 98 (87 + 11), OK, one skip,
  with `datastorekit`, `ray` and `sqlalchemy` not findable. `test_unreadable_status` also passes at
  3.13.16 and 3.14.8.
- Eight mutations, each caught by the tests named in §5 below.
- The issue `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` is **closed**.
  One issue is **opened**, found by the work (deviation 15). The index counts **10 → 9 → 10**.
- **Nothing pushed, no tag made, no workflow dispatched.**

## What shipped

| File | What |
|---|---|
| `runregistrykit/__init__.py` | The helper `_json_object` (`:247`), beside `read_json` (`:237`), outside the writer's section. `_write_status`' base read (`:383`) through it. `liveness` (`:603`): `if not isinstance(status, dict) or not status` (`:627`), and step 1 of its docstring. `Run.status()` (`:730`) through the helper. `list_runs` (`:1137`): the two raw reads (`:1172-1173`), `has_manifest` as `isinstance(raw_manifest, dict)`, every manifest field read from the helper's payload, the new key `status_readable` (`:1197`), and the docstring's two paragraphs |
| `runregistrykit/stores.py` | The module docstring (`:102-109`). `TERMINAL_STATES` imported from the core (`:152`). `_running_runs_naming` (`:1001`): its docstring and the filter (`:1023`). `_describe_running` (`:1028`): two new descriptions, unreadable first, then readable-but-not-`running`, then today's two. `_unsure_remedy` (`:1063`), new. `_refuse_if_in_use`'s docstring (`:1074`), and the remedy sentence in its refusal (`:1085-1090`), in fingerprint's (`:1387-1398`), retire's (`:1716-1725`) and amend's (`:2071-2078`) |
| `runregistrykit/__main__.py` | The module docstring's four phrases (`--help`'s description). `_unsaid` (`:72`), new. The marker (`:565-567`), the row's state formatted with `str` (`:573`), and the stderr line (`:595-603`), after the stale line and before the foreign one |
| `runregistrykit/tests/test_unreadable_status.py` | New, core, 11 tests: the thirteen-form table `FORMS`, which the store module imports |
| `runregistrykit/tests/test_unreadable_status_stores.py` | New, store layer, 7 tests, on `test_store_retire.RetireTestCase` |
| `.github/workflows/tests.yml` | The core job's line (`:89`): `runregistrykit.tests.test_unreadable_status` added |
| this log, `IMPLEMENTATION_STATE.md`, the campaign README's §2 row for 03, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: `pyproject.toml`, `client.py`, `fingerprint.py`, the repository `README.md`,
`PROVENANCE.md`, `CLAUDE.md`, `docs/` (but `docs/OPEN_ISSUES.md`), any existing test module or
fixture, the prompt, any other part of the campaign README, `orchestrator/`, and the 02c log.
`Run.__init__`'s manifest read (`:675`) and `Run.finish` are not changed.

### The rule

```python
        if entry["state"] not in TERMINAL_STATES
        and os.path.realpath(entry["path"]) != excluded
```

`entry["state"]` is the status's `state`, or `None` where the status is unreadable, so `None`, a
number and a string the registry never writes are all outside the tuple. `TERMINAL_STATES` is
imported, not spelled again. The name `_running_runs_naming` is kept (deviation 10).

### The helper

```python
def _json_object(raw) -> dict:
    return raw if isinstance(raw, dict) else {}
```

No loop and no comprehension. It serves the status and the manifest alike. In `list_runs`:
`status_readable` is `isinstance(raw_status, dict)`, so a status `{}` is readable (and then has no
state); `has_manifest` is `isinstance(raw_manifest, dict)`, so a manifest `{}` still counts as a
manifest and `[1]`, `"x"`, `5` and `null` do not. `runs_naming` is unchanged: its skip of an entry
with no manifest (`:976`) now skips a non-object manifest too.

### The words, as shipped

For a `running` run every existing text is byte for byte as it was (§6). The new ones:

- status unreadable: `run <id>'s status cannot be read (status.json is missing, is not JSON, or is
  not a JSON object), so whether it is running cannot be told; it names this store by its <matched>`
- readable, state neither `running` nor terminal: `run <id>'s status says neither running nor
  finished (state <repr of the state, or none>), so whether it is running cannot be told; it names
  this store by its <matched>`, for example `(state 'paused')`, `(state 5)`, `(state none)`
- the remedy sentence, added **once**, and only when some entry is not `running`: `A run whose
  status does not say whether it is running is ended by a person, with Run.finish, once they have
  checked that it is not.` It follows the existing remedy sentence in copy, move, fingerprint and
  retire, and ends amend's refusal after `dead`.
- `list`'s line on stderr: `!! <n> run(s) have a manifest and a status that does not say whether the
  run is running, or that cannot be read: the registry cannot tell whether they are running, and
  the store operations count them as in use. Go and look; once you know one is not running, end it
  with Run.finish.`

## Deviations from the prompt

Each is classified. Corrections 1–16 are section 0's.

1. **L6 is (a) refined** (correction 1), as the prompt states it. **STRUCTURALLY REQUIRED.**
2. **The suite's time** (correction 2). Each suite run was in the foreground, its output in a file,
   the verdict grepped from it: 124.542 s was the orchestrator's gate run; here 121.261 s and
   117.761 s (before the last additions) and 123.614 s on the tree as committed (§2).
   **STRUCTURALLY REQUIRED.**
3. **The core run** (correction 3): `uv venv -p /opt/local/bin/python3.12 agent-03/core`, then `uv
   pip install --offline -p agent-03/core/bin/python -e` this checkout, `TMPDIR` in scratch,
   removed afterwards, run twice. **STRUCTURALLY REQUIRED.**
4. **3.13 and 3.14** (correction 3). `test_unreadable_status` ran at `/opt/local/bin/python3.13`
   (3.13.16) and `python3.14` (3.14.8) with `PYTHONPATH` on the checkout. No `-m pip`.
   **IMPLEMENTATION CHOICE:** 3.14 is beyond the brief's request, and costs four seconds.
5. **One helper, two reads** (correction 4). The helper is named `_json_object`, an
   **IMPLEMENTATION CHOICE** (the prompt leaves it to the agent). **STRUCTURALLY REQUIRED**
   otherwise.
6. **The helper is outside the swept section** (correction 5): see §4.
7. **`liveness`** (correction 6): the test is `not isinstance(status, dict) or not status`; `[]`
   and `{}` stay `unknown`. **STRUCTURALLY REQUIRED.**
8. **The store module does not subclass `TestARunOnAnotherHostIsInUse`** (correction 7). It
   subclasses `test_store_retire.RetireTestCase`, and carries its own `refusals`, a copy of
   `test_host_stores`' with a destination `C<i>` per form; and each form has a full store
   `S<i>`, a run and a destination of its own, so no outcome depends on an earlier form's. The
   fragments asserted are the run's id, the form's words, `so whether it is running cannot be told`,
   `names this store by its results` and the remedy sentence. **STRUCTURALLY REQUIRED.**
9. **`__main__.py`'s module docstring** (correction 8, "the orchestrator's correction 8"). Its four
   phrases are brought into line with `stores.py`'s. The paragraph is re-wrapped to ~100 columns,
   which makes the diff larger than four phrases; nothing else in it changes. **IMPLEMENTATION
   CHOICE.**
10. **The name `_running_runs_naming` is kept**, and its docstring says the set is every run that
    names the store and has not finished. A rename would touch five callers for a word.
    **IMPLEMENTATION CHOICE.**
11. **The words** (correction 9). The remedy sentence is built once by `_unsure_remedy` and added
    once per refusal. The f-string fragments around the insertion point are split differently
    (`...dead. ` / the new sentence / `Nothing was written`); the text for a `running` run is
    byte for byte the same (§6). **IMPLEMENTATION CHOICE.**
12. **`list`** (correction 10): the marker, and the stderr line counting only the `unknown` rows
    that have a manifest, after the stale line and before the foreign one. `TestLister` and
    `test_host`'s `list` tests pass unchanged. **STRUCTURALLY REQUIRED.**
13. **`list`'s row formats the state with `str`** (`:573`). A status whose state is a JSON list or
    object made `list` raise `TypeError: unsupported format string passed to list.__format__` at
    `35ce264` (measured, §3), which the prompt's rule "never raised on" does not allow, though it
    is not one of its thirteen forms. A string state is unchanged; a number state `5` is now left-
    aligned like a string, not right-aligned. One test pins it (`test_a_state_that_is_a_list_or_an_
    object_is_listed_not_raised_on`), and the mutation (m8) removing the `str` fails it. **IMPLEMENTATION
    CHOICE.**
14. **The two `list` tests run `python -m runregistrykit` with `PYTHONPATH` set to the checkout**
    (as `test_store_command_line.CommandLineTestCase` does). Found at the mutations: without it the
    child imports the editable install, which is the original checkout and not a scratch clone,
    so (m5) could not have been caught there. **IMPLEMENTATION CHOICE.**
15. **One issue opened** (correction 16): `[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]`,
    measured (§3). The board's §3 count stays five and the index's goes 10 → 10 (9 after closing
    the prompt's issue, then 10), where the brief expected 9. **IMPLEMENTATION CHOICE** (the brief
    says to open it when measured).
16. **Mutations** (correction 13). The prompt asks for (m1)–(m5) and one of the agent's own; (m6),
    (m7) and (m8) are the agent's own, three. **IMPLEMENTATION CHOICE.**
17. **`stores.py` prose not brought into line.** Three docstring or comment lines still say a
    `running` run, "alive or stale" (`:1350`, `:1709`, `:2005`). The prompt names the module
    docstring, `_running_runs_naming`, `_describe_running` and `_refuse_if_in_use`'s only (rule 4):
    see "Observations not acted on". **UNINTENDED DRIFT** avoided, by leaving it.

## Verification performed

### 1. The state at the start

- `HEAD` `75eab12`, `main`, clean, the only worktree. `RAY_ADDRESS` unset; `pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` found nothing before and after every suite run.
- `venv/`: Python 3.12.15, black 25.1.0. `/opt/local/bin/python3.12` 3.12.15, `python3.13` 3.13.16,
  `python3.14` 3.14.8. `var/ledger.jsonl` `471d0859…` before and after.
- `git status --short --ignored` before: `prompts/.DS_Store`, `runregistrykit.egg-info/`, both
  `__pycache__/`, `var/`, `venv/`.

### 2. The suite, before and after

`TMPDIR=<agent-03>/tmp ./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from
the root, in the foreground. Per module, by `unittest.defaultTestLoader.discover`:

| Module | Before | After |
|---|---:|---:|
| `test_client_root` | 27 | 27 |
| `test_fingerprinter` | 31 | 31 |
| `test_host` | 28 | 28 |
| `test_host_stores` | 3 | 3 |
| `test_package_imports` | 3 | 3 |
| `test_package_is_generic` | 22 | 22 |
| `test_public_names` | 8 | 8 |
| `test_run_registry` | 29 | 29 |
| `test_status_writes` | 22 | 22 |
| `test_store_amend` | 21 | 21 |
| `test_store_amend_residuals` | 9 | 9 |
| `test_store_command_line` | 2 | 2 |
| `test_store_copy_move` | 27 | 27 |
| `test_store_fingerprint` | 29 | 29 |
| `test_store_retire` | 41 | 41 |
| `test_store_retire_references` | 10 | 10 |
| `test_store_sidecar` | 17 | 17 |
| `test_unreadable_status` | — | **11** |
| `test_unreadable_status_stores` | — | **7** |
| **total** | **329**, `Ran 329 tests in 124.542s` (the orchestrator's gate run), `OK (skipped=1)` | **347**, `Ran 347 tests in 123.614s`, `OK (skipped=1)` |

N = 18 (N₁ = 11 core, 7 store). The skip is `test_host`'s macOS readers, as before. No existing
test module or fixture is modified: `git status --short` lists only the three package files and
the workflow as modified, and the two test modules as new. Every test that existed at `35ce264`
passes unchanged. `test_package_is_generic` (the guard) passes with the new files.

### 3. The probes, against `35ce264` and this tree

The planner's `probe.py`, `probe_finish.py` and `probe_manifest.py`, each with one line added that
prints `runregistrykit.__file__`, run by `venv/`'s Python with the checkout as first argument.
`TREE` was `<agent-03>/old/runregistrykit/__init__.py` (`git archive 35ce264`) for "before", and
`/Users/ds283/Documents/Code/RunRegistryKit/runregistrykit/__init__.py` for "after". Not committed.

**The thirteen forms** (a live run begun in the probe's process on a full four-shard store, its
`status.json` replaced; the six operations with a destination per form):

| Form | before: `list_runs` | before: `list` | before: the six operations | after: `list_runs` | after: `list` | after: the six operations |
|---|---|---|---|---|---|---|
| missing | state `None`, `unknown` | no marker | **all proceed** | state `None`, `unknown` | `!!` | refused (6) |
| empty file | the same | no marker | **all proceed** | the same | `!!` | refused (6) |
| torn | the same | no marker | **all proceed** | the same | `!!` | refused (6) |
| not JSON | the same | no marker | **all proceed** | the same | `!!` | refused (6) |
| `null` | the same | no marker | **all proceed** | the same | `!!` | refused (6) |
| `[]` | the same | no marker | **all proceed** | the same | `!!` | refused (6) |
| `[1]` | **raises** `AttributeError` | **raises** | **all raise** | state `None`, `unknown` | `!!` | refused (6) |
| `"x"` | **raises** | **raises** | **all raise** | the same | `!!` | refused (6) |
| `5` | **raises** | **raises** | **all raise** | the same | `!!` | refused (6) |
| `{}` | state `None`, `unknown` | no marker | **all proceed** | state `None`, `unknown` | `!!` | refused (6) |
| state `null` | the same | no marker | **all proceed** | the same | `!!` | refused (6) |
| state `"paused"` | state `'paused'`, `unknown` | no marker | **all proceed** | state `'paused'`, `unknown` | `!!` | refused (6) |
| state `5` | state `5`, `unknown` | no marker | **all proceed** | state `5`, `unknown` | `!!` | refused (6) |

"Before" is the prompt's table, reproduced: every row is as it states. `list` exited 0 in every
"after" row, and `list_runs` raised on none.

**The remedy** (`probe_finish.py`, `Run(path).finish("killed", exit_code=137)` on a fresh run):

| Form | before | after |
|---|---|---|
| missing, torn, `null`, `{}` | `killed`, keys `exit_code`, `heartbeat`, `state` | the same |
| `"paused"` | `killed`, keys with `pid` | the same |
| `[1]`, `"x"`, `5` | **raises** `AttributeError: … has no attribute 'update'` | `killed`, keys `exit_code`, `heartbeat`, `state` |

**The manifest** (`probe_manifest.py`; status left `running`, pid alive):

| Form | before | after |
|---|---|---|
| torn | `has_manifest` false, `alive`, `fingerprint_store` **proceeds** | the same |
| `[1]` | `list_runs` **raises** `AttributeError`; `fingerprint_store` raises | `has_manifest` false, `alive`, `fingerprint_store` **proceeds** |
| missing | `has_manifest` false, `alive`, `fingerprint_store` **proceeds** | the same |

The torn and missing rows are `[03-a-run-whose-manifest-cannot-be-read-names-no-store]`, still
proceeding as the brief says; not this prompt's to fix. The `[1]` row no longer raises, and now
proceeds as the torn one does.

**A state that is a list or an object** (`list --root`, a scratch script): at `35ce264`, state
`["a"]` and `{"a": 1}` make `list` exit 1 with `TypeError: unsupported format string passed to
list.__format__` (`dict.__format__`); state `5` lists. After: all three list, `!!`, exit 0.

**`Run(path)` on a manifest that is not an object** (scratch, this tree, deviation 15): `[1]`,
`"x"` and `5` construct, with `Run.manifest` the value itself (`:675`, `read_json(…) or {}`);
`checkpoint_path` (`:715`) and `results_path` (`:725`) then raise `AttributeError`; `finish("killed")`
without `fingerprint` returns. `null` constructs with `{}` and nothing raises.

### 4. The writer's sweeps

`test_status_writes` passes unchanged: 22 tests, in the suite and in the core run.

**The helper is outside the section.** `_json_object` is at `:247`, in the "files" section (`:220`
on), before the writer's section (`:260` on at `35ce264`, `:268` now). `the_writers_code()` finds
the writer's code objects by the section's bounds, so the sweeps do not include the helper and do
not interrupt inside it. They do interrupt the writer at the new `CALL`. That is safe: the helper
has no loop, no lock and no state, and an exception raised in its frame surfaces in `_write_status`
at the covered `CALL`, inside the `try` and the `with`, so the `finally` and the `with`'s exit run.

The sweeps' instruction counts, by `agent-03/sweepcount.py`, which calls the test module's own
`sweep_in_this_process` and `jumps_in_this_process` on each tree (the jump sweep in a process of its
own, as the test runs it), per mode:

| | 3.12.15, `35ce264` | 3.12.15, now | 3.13.16, `35ce264` | 3.13.16, now |
|---|---:|---:|---:|---:|
| heartbeat and finish sweeps, each of 4 modes | 327 | 327 | 327 | **326** |
| `_write_status` (per write) | 98 | 98 | 101 | **100** |
| `_newest_landed`, `_land_status`, `_status_temporary_name`, the generator | 78, 118, 23, 10 | the same | 75, 116, 25, 10 | the same |
| jump sweep: instructions, jumps attempted | 327 / 626 / 985; 3 / 7 / 12 | the same | 327 / 632 / 991; 3 / 7 / 12 | **326 / 631 / 990**; 3 / 7 / 12 |
| wrong, every mode | 0 | 0 | 0 | 0 |
| `done` accepted (finish sweep, "returns" modes) | 24 | 24 | 25 | 25 |

At 3.12 the swapped read `read_json(path) or {}` and `_json_object(read_json(path))` execute the
same number of instructions; at 3.13 one fewer. A changed count is expected and is not a stop.
(Run in one process after the other sweeps, the jump sweep's first write reports one wrong
attempt on either tree: the leaked state the test's child process exists to contain.)

### 5. The deliberate-breakage record

Each mutation was applied in a scratch `git clone` of this repository (`agent-03/mut`), whose tree
was first made equal to the files as they are committed (`cmp` on all six). For each: the diff
(from `git diff` after `black`) was saved, `git apply -R --check` accepted it, `./venv/bin/python
-m unittest runregistrykit.tests.test_unreadable_status
runregistrykit.tests.test_unreadable_status_stores` ran (17 tests, 18 with (m8)'s module), and
`git checkout .` reverted it; the clone's `git status` was clean after each, and this checkout's
`git status` was never changed by one. The clone's tests ran this tree's code (the child
processes' `PYTHONPATH`, deviation 14).

**(m1)** the filter back to `entry["state"] == "running"`. 100 failures: `test_each_form_is_refused_by_each_operation`
(all 13 forms, every operation), `test_a_real_retire_is_refused_and_the_store_survives`,
`test_a_resumed_runs_fingerprint_is_refused_by_an_unreadable_predecessor`,
`test_the_command_refuses_for_a_torn_status`, and `test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once`
(six operations).

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index e5def9b..d59f1bc 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1020,7 +1020,7 @@ def _running_runs_naming(
         for entry in runs_naming(
             primaries, store_id, runs_root=root, client_root=client
         )
-        if entry["state"] not in TERMINAL_STATES
+        if entry["state"] == "running"
         and os.path.realpath(entry["path"]) != excluded
     ]
 
```

**(m2)** the filter counting a run in use when `status_readable` is false or the state is `running`,
and no other (L6 (a) as first planned). 34 failures: `test_each_form_is_refused_by_each_operation` for
exactly the four readable forms, `{}` (`empty object`), state `null`, `"paused"` and state `5`, each
for the form and its six operations (28), and `test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once`
(its unnamed-state run, six operations).

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index e5def9b..df8cf99 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1020,7 +1020,7 @@ def _running_runs_naming(
         for entry in runs_naming(
             primaries, store_id, runs_root=root, client_root=client
         )
-        if entry["state"] not in TERMINAL_STATES
+        if not entry["status_readable"] or entry["state"] == "running"
         and os.path.realpath(entry["path"]) != excluded
     ]
 
```

**(m3)** `list_runs` reading the status as `raw_status or {}` again. 14: `test_each_form_is_refused_by_each_operation`
(12 subtests: the forms `[1]`, `"x"` and `5`, with `AttributeError`),
`test_every_form_is_listed_unknown_and_none_raises` (error), and
`test_each_form_is_marked_and_the_line_on_stderr_counts_them` (the `list` child exits 1).

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 212ae60..39e9296 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -1172,7 +1172,7 @@ def list_runs(
         raw_manifest = read_json(os.path.join(path, "manifest.json"))
         raw_status = read_json(os.path.join(path, "status.json"))
         manifest = _json_object(raw_manifest)
-        status = _json_object(raw_status)
+        status = raw_status or {}
         recorded = status.get("host")
         described = manifest.get("host")
         entries.append(
```

**(m4)** the writer's base read back to `read_json(path) or {}`. 3 errors, all in
`test_finish_ends_a_run_in_every_form`: the forms `[1]` (`list of one`), `"x"` (`string`) and `5`
(`number`), which raise `AttributeError` from the base read.

```diff
diff --git a/runregistrykit/__init__.py b/runregistrykit/__init__.py
index 212ae60..54c5c99 100644
--- a/runregistrykit/__init__.py
+++ b/runregistrykit/__init__.py
@@ -380,7 +380,7 @@ def _write_status(path, fields) -> dict:
                 status = copy.deepcopy(payload)
                 earlier = list(n for n in earlier if n > landed)
             else:
-                status = _json_object(read_json(path))
+                status = read_json(path) or {}
             for n in earlier:
                 status.update(book["in_flight"][n])
             status.update(fields)
```

**(m5)** `list`'s `!!` for an `unknown` row with a manifest removed. 1: `test_each_form_is_marked_and_the_line_on_stderr_counts_them`.

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 377a43b..e296fc8 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -563,8 +563,6 @@ def main(argv=None) -> int:
         # and which has a manifest; `??` one on another host, whose pid is not tested here, and
         # whose row names that host
         marker = {"stale": "!!", "foreign": "??"}.get(entry["liveness"], "")
-        if _unsaid(entry):
-            marker = "!!"
         purpose = _purpose(entry)
         if entry["liveness"] == "foreign":
             purpose = f"on {_host(entry)} · {purpose}"
```

**(m6)** (the agent's own) the remedy sentence added whenever any run is refused, not only when
one is not `running`. 6 failures, one per operation, in
`test_a_refusal_for_running_runs_alone_has_no_new_sentence`.

```diff
diff --git a/runregistrykit/stores.py b/runregistrykit/stores.py
index e5def9b..a2c40cc 100644
--- a/runregistrykit/stores.py
+++ b/runregistrykit/stores.py
@@ -1063,7 +1063,7 @@ def _describe_running(running) -> str:
 def _unsure_remedy(running) -> str:
     """The sentence a refusal adds, without its full stop, when any of ``running`` is not a
     `running` run: its status does not say, and only a person can. Empty otherwise."""
-    if all(entry["state"] == "running" for entry in running):
+    if not running:
         return ""
     return (
         "A run whose status does not say whether it is running is ended by a person, with "
```

**(m7)** (the agent's own) `list`'s marker without `has_manifest`: a directory that predates the
registry would be marked. 2: `test_each_form_is_marked_and_the_line_on_stderr_counts_them` and
`test_no_such_run_no_such_line`.

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 377a43b..f1d4f35 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -72,7 +72,7 @@ def _progress(entry) -> str:
 def _unsaid(entry) -> bool:
     """A run with a manifest whose status does not say whether it is running (`unknown`). A
     directory with no manifest, which predates the registry, is not one."""
-    return entry["liveness"] == "unknown" and entry["has_manifest"]
+    return entry["liveness"] == "unknown"
 
 
 def _host(entry) -> str:
```

**(m8)** (the agent's own) `list`'s row formatting the state without `str`. 1:
`test_a_state_that_is_a_list_or_an_object_is_listed_not_raised_on`.

```diff
diff --git a/runregistrykit/__main__.py b/runregistrykit/__main__.py
index 377a43b..6a74a90 100644
--- a/runregistrykit/__main__.py
+++ b/runregistrykit/__main__.py
@@ -570,7 +570,7 @@ def main(argv=None) -> int:
             purpose = f"on {_host(entry)} · {purpose}"
         print(
             f"{marker:2} {entry['id']:{width}}  "
-            f"{str(entry['state'] or 'unknown'):9} {_progress(entry):>9} "
+            f"{(entry['state'] or 'unknown'):9} {_progress(entry):>9} "
             f"{_age(now - entry['created_epoch']):>8}  {purpose}"
         )
 
```

Each fails at least one test. None was left in this tree.

### 6. The words, and nothing written

- `git diff -U0 35ce264 -- runregistrykit/stores.py` shows no existing refusal fragment changed in
  its text: the only changed fragments are the ones the new sentence is inserted into (`dead. Nothing
  was written` split in three, `first. Nothing was read or written` likewise, and `dead. Once ` and
  `it is ended, …` joined across the inserted `{unsure}`). With nothing to insert, the message is the
  same character for character, as every existing refusal test, unchanged, shows.
- `test_a_refusal_for_running_runs_alone_has_no_new_sentence`: a `running` alive and a stale run
  together: none of the six refusals contains the new sentence or `cannot be told`.
- `write_json_atomic` is `:255-263`, unchanged. No key is added to, removed from or renamed in a
  written file: the new key is in `list_runs`' entries only. `git diff 35ce264 --
  runregistrykit/__init__.py` touches the writer's section (`_write_status`) at one line, the base
  read (`:383`).

### 7. Nothing outside temporary directories, nothing signalled

`git grep -n 'signal' -- 'runregistrykit/*.py' ':!runregistrykit/tests'` finds one line,
`runregistrykit/__init__.py:807`, in `finish`'s docstring. The new tests build everything in
`tempfile` directories through the existing fixtures and send no signal. `pgrep` found no Ray
process before or after any run. The probes signalled nothing.

### 8. The core alone, and 3.13 and 3.14

A venv built as correction 3 (`uv venv -p /opt/local/bin/python3.12`, `uv pip install --offline -e`
this checkout). `importlib.util.find_spec` found none of `datastorekit`, `ray`, `sqlalchemy`
(`{'datastorekit': False, 'ray': False, 'sqlalchemy': False}`). The five core modules by name,
`test_run_registry`, `test_public_names`, `test_host`, `test_status_writes`, `test_unreadable_status`:
`Ran 98 tests in 25.875s`, `OK (skipped=1)` (87 + 11). The venv was removed afterwards.
`test_unreadable_status` at 3.13.16 and 3.14.8 with `PYTHONPATH` on the checkout: `Ran 11 tests`,
`OK`, each.

### 9. `black`

`./venv/bin/black --check runregistrykit docs`: 31 files at `35ce264`, **33** now (the two new
modules), unchanged. The four changed files and the two new ones were formatted.

### 10. CI

Nothing is pushed. The new core module first runs in the core job and on Linux, at 3.12.15, and at
3.13.16 in `suite (high)`; the review is to read the run's result there, and the core job's count,
which should be 98.

## Observations not acted on

1. **`Run(path)` on a manifest that is not an object** (§3, deviation 15): it constructs, and
   `checkpoint_path` and `results_path` raise `AttributeError`. The prompt's §6 leaves
   `Run.__init__`'s manifest read alone. Opened as
   `[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]`, owner none.
2. **Three lines of prose in `stores.py` still describe the old rule**: `fingerprint_store`'s
   docstring (`:1350`, "`running` run under ``runs_root``, alive or stale"), the comment at `:1709`
   ("any running run, alive or stale") and `amend_sidecar`'s docstring (`:2005`). They are
   docstrings and a comment, not behaviour, and the prompt names only four. No issue opened: a line
   for the next prompt that touches these functions (04 rewrites their remedy words).
3. **`list`'s `_progress`, `_purpose` and `_age` are not hardened** against a status or manifest
   whose fields have unexpected types (a `units_done` that is a string, a `purpose` that is a list).
   Not measured here beyond the state field; no issue opened.
4. **The core run's editable install rewrote the ignored `runregistrykit.egg-info/`**, as 02b's and
   02c's did. It is ignored and not staged.
5. **A status written between `begin` and the first heartbeat**: unchanged (`begin` is 05's).
6. **A run that predates the registry** (no manifest, no status) is still `unknown` with no marker,
   and counts as no store's user, as before.

## State handed to the next prompt

- **The interface after 03:**
  - `runregistrykit._json_object` (`:247`), private, beside `read_json` (`:237`);
  - `list_runs` (`:1137`) entries gain `status_readable` (`:1197`); `has_manifest` is
    `isinstance(manifest, dict)` (`:1182`);
  - `liveness` (`:603`) is `unknown` for a status that is not an object (`:627`);
  - `Run.status()` (`:730`) returns the helper's payload; `_write_status`' base read is `:383`;
  - `stores._running_runs_naming` (`:1001`, filter `:1023`) counts every run not terminal;
    `_describe_running` (`:1028`), `_unsure_remedy` (`:1063`), `_refuse_if_in_use` (`:1074`);
  - `list` (`__main__.py`) marks `!!` an `unknown` row with a manifest (`:565-567`) and prints one
    line on stderr (`:595-603`).
- **For 04 (`end`):** the refusals' remedy words are in four places in `stores.py` plus
  `_refuse_if_in_use` (`:1085-1090`, `:1387-1398`, `:1716-1725`, `:2071-2078`), and the new
  sentence in one, `_unsure_remedy` (`:1063`): 04 replaces "with Run.finish" in each. `list`'s
  stderr line (`__main__.py:595-603`) also names `Run.finish`. A run `end` is pointed at may have
  an unreadable status, and `Run.finish` ends it (`probe_finish`), so `end` needs no new case.
- **For 05 (`begin`):** `_running_runs_naming`'s set is now what a refusal by `begin` should use:
  a run that has not finished, not only `running` (L9).
- **The issues:** `[00-an-unreadable-status-hides-a-running-run-from-the-store-checks]` closed;
  `[03-a-run-whose-manifest-cannot-be-read-names-no-store]` open, owner none;
  `[03-a-run-on-a-manifest-that-is-not-an-object-raises-where-it-is-used]` opened, owner none.
- **CI:** the push is the user's. The core job's line now names five modules.
- The suite is 347, with one skip on macOS.
