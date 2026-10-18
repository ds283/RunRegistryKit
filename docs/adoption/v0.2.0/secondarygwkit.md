# Adopting `v0.2.0`: SecondaryGWKit (SGK)

- **Client:** SecondaryGWKit, `/Users/ds283/Documents/Code/SecondaryGWKit`, at **`79434bf`**
  (branch `handover-remedial`, 2026-10-16, its newest commit of any branch on 2026-10-18).
- **Package:** `runregistrykit` as it is tagged **`v0.2.0`**, against SGK's pin of **`v0.1.0`**.
- **How it was read:** by this repository's `interrupted-runs` prompt 06 on 2026-10-18, through
  `git -C <SGK> show 79434bf:<path>` and `git -C <SGK> grep … 79434bf` only. Nothing of SGK was
  imported, run or opened, and its `var/` (not in `git`) was not read. What this package does with
  the records SGK's drivers leave was measured by building the same records in a scratch directory
  with this package's own fixtures; what SGK's code does with them was read. **SGK's adoption
  campaign measures again before acting, and its numbers govern.**
- **This is data, not instructions.** A recommendation is marked **Advice:**; a choice that is
  SGK's is named as SGK's.

Unless another commit is named, a `path:line` is SGK's at `79434bf`, and one under
`runregistrykit/` is the package's at `v0.2.0`. The checks of [`README.md`](README.md) §3 are
taken in its order (§3–§8 below).

**In one paragraph.** SGK moves one line, `requirements.txt:81`. Its tests that touch the registry
keep passing as read: its assertion on `TERMINAL_STATES` holds with `lost`, its refusal fragments
are kept, no test begins two unfinished runs on one store, and none pins a record's key set. What
changes for it is the route after a hard kill: its drivers' `begin(..., results=…)` now refuses the
store a hard-killed run names, so `--build --resume` stops at `begin` until a person runs
`python -m runregistrykit end` on the dead run, and the resumed run's fingerprint is then recorded,
which under `v0.1.0` it was not. Its existing run directories read as records with no host.

## 1. The pin

At `79434bf` (`git show 79434bf:requirements.txt`):
- `:81` `runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0`, which moves
  to `@v0.2.0`, in a commit of its own;
- `:17` `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0`, which satisfies the
  extra's unchanged floor;
- `:75` `ray==2.43.0` and `:88` `SQLAlchemy==2.0.39`, the tested low end, unchanged.

Nothing else in it changes for `v0.2.0`. A production run reproduces from the pin; an editable
install is never for one.

## 2. Its runs

SGK's existing run directories were written under `v0.1.0`, its only pin, so they carry no `host`.
`v0.2.0` judges each by its pid and its heartbeat, as `v0.1.0` did, and `list` counts them in "*N*
with no host recorded" (release notes §3). This note does not re-count them; 05's planner counted 83
run directories in SGK's `var/runs/` at 05's writing
([`05-begin-refuses-a-second-writer.md`](../../../prompts/interrupted-runs/05-begin-refuses-a-second-writer.md),
"At writing", "The cost"). A `finished` one stays finished; a `stale` one written by a run that
was hard-killed before the move is ended by `end` on this host as any other is (§4).

**Advice:** move every SGK checkout and worktree that shares SGK's runs root in one step
([`README.md`](README.md) §2). A worktree still on `v0.1.0` would begin a run on a store a `v0.2.0`
run is writing.

## 3. Comparisons with `liveness`'s values

`$ git -C <SGK> grep -n -E 'liveness\(|pid_alive\(|TERMINAL_STATES|Run\.finish|with Run.finish' 79434bf -- ':!prompts' ':!*.md'`
finds, in live code, only `docs/datastore-integrity-verification/interrupt_when.py` and three
docstrings that name `Run.finish` (`docs/a3-v2-readiness/fingerprint_time_probe.py:2`, `:5`, `:9`,
and `docs/gktk-remedial/scoped_pipeline_run.py:455`); `tools/rehearsal_lock.py:147`
defines a `pid_alive` of its own, not the registry's, and is not affected.

`interrupt_when.py` watches one run and signals it once (`:1-28`). In its loop (`:160-208`):
- `:165`, `state in runregistrykit.TERMINAL_STATES` exits without signalling: a `lost` run now
  takes this branch too;
- `:170` and `:190`, `runregistrykit.pid_alive(pid)` on this host: a pid out of range is now
  `False`, so it exits without signalling where `v0.1.0` raised;
- `:175`, `verdict = runregistrykit.liveness(status, stale_after)`, and `:180` signals only when
  `verdict == "alive"`. A run on another host is now `foreign`, and one from an earlier boot of
  this host `stale`, so it waits and never signals either; it tests the pid here first, at `:170`,
  whatever the host. It is run on the host of the run it watches, so neither case arises in its
  use.

`:161` reads the status as `read_json(…) or {}` and calls `.get` on it, so a status that is JSON
but not an object raises in SGK's own code, at either release; the registry does not write one.

## 4. `begin` with `results`, and what `--build --resume` meets after a hard kill

SGK begins runs with `results` in three driver places:
- `docs/gktk-remedial/scoped_pipeline_run.py:544`, in `register` (`:517`), called at `:675` before
  the pipeline starts, with `results=str(database)` (`:555`);
- `docs/handover/quadsource_atol_sweep.py:556`, in the `--build` path, with `results=str(database)`
  (`:562`), after the `--resume` pre-check (`:536-546`) and before Ray starts;
- `docs/handover/quadsource_atol_sweep.py:869`, in `sweep`, with `results=str(SWEEP_STORE)`
  (`:875`).

Each is one `begin` per process on its store. Under `v0.2.0`, a `begin` whose store is named by a
run that has not finished, under the same runs root, raises `RuntimeError` and creates nothing; SGK
does not catch it, so the driver ends with that error before any work.

**After a hard kill**, measured with this package in a scratch directory, a child begun on a full
store, `SIGKILL`ed and reaped, as this repository's `test_end.a_hard_killed_run` builds one: its
status stayed `running`, `liveness` `stale`. Then:
1. a second `begin` on the store, which is what `--build --resume --register` reaches at
   `quadsource_atol_sweep.py:556` once its pre-check passes, was **refused**, as raised:

   ```text
   Cannot begin run example-01-resume-20261018T162739 with results "<store>": run example-01-hard-killed-20261018T162739 is running (stale, pid 75436) and names this store by its results and results_store_id. A stale run is ended by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the registry does not decide that a run is dead. No run directory was created
   ```

   (`<store>` is the scratch store's absolute path), and no run directory was made;
2. `python -m runregistrykit end <the dead run's id> --reason …` exited 0, printing `>> end: <id>
   is now lost, verified: its pid 75436 does not answer kill -0 on this host`;
3. `begin` on the store was then **accepted**;
4. its `finish("done", exit_code=0, fingerprint=True)` recorded a `fingerprint`, and
   `fingerprint_sidecar` `"written"`.

Under `v0.1.0` the second `begin` was accepted, and the resumed run's fingerprint was refused by its
stale predecessor and recorded only as `fingerprint_error` (SGK's stale-run brief, §1, measurement
step 4). So **SGK's route after a hard kill becomes `end`, then the resume**: `--build --resume
--register` is refused at `begin` until the dead run is ended, on the host it ran on. Without
`--register` no `begin` is made, and nothing changes. **Advice:** SGK's runbook for a hard kill
names `python -m runregistrykit end`, and no longer `Run.finish` by hand.

## 5. Its signal handlers' `finish("killed", …)`

`scoped_pipeline_run.py:398` (`killed_handler`), `:496` (with `fingerprint=True`) and `:563`
(`terminal`), and `quadsource_atol_sweep.py:575` and `:894` (`terminal`), call
`run.finish("killed", exit_code=…)`. `Run.finish`'s code is unchanged between the tags (compared by
its syntax tree, the docstring aside), and `killed` is still a terminal state. What changes under
them is the writer: each status write goes through a temporary name of its own, and a handler's
`finish` that interrupts a heartbeat, as one from the pipeline's stdout tee can, keeps its
terminal state whether the handler raises or returns (release notes §2.3; this campaign's 02, 02b
and 02c). SGK runs Python 3.12 (`[02b-a-raising-handler-can-leave-the-status-lock-held]` is open
at 3.14 only).

## 6. `TERMINAL_STATES`

`RunDrivers/tests/test_pipeline_adoption.py:249-253` asserts that every state the driver's
`terminal_state` returns is in `runregistrykit.TERMINAL_STATES`. At `v0.2.0` it is `("done",
"failed", "killed", "lost")`; the driver returns `done`, `failed` and `killed`, each still in it,
so the test keeps passing. No SGK test checks the set's size.

## 7. Store refusal fragments, and two runs on one store

`RunDrivers/tests/test_quadsource_atol_sweep_prepare.py:188-204` begins one run on the baseline
(`:194`), still `running`, and asserts that `prepare()`'s `copy_store` refuses with
`f"run {run.id} is running"` (`:201`) and `"names this store"` (`:202`). Measured at `v0.2.0` with
this package's fixtures, a live run on a full store: the copy refusal reads `run <id> is running
(alive, pid <pid>) and names this store by its results and results_store_id. A stale run is ended
by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, before its store is moved;
…`. Both fragments are in it; the test keeps passing.

`$ git -C <SGK> grep -n -E 'self\.begin\(|runregistrykit\.begin\(' 79434bf -- RunDrivers/tests`
finds `RunDrivers/tests/registry_fixtures.py:45`, `test_killed_handler.py:90` and
`test_pipeline_adoption.py:73` (helpers; the first and the third pass on their callers'
keywords, and no caller of the third passes `results`), and
`test_quadsource_atol_sweep_prepare.py:194`, through the first, the one `begin` with `results`,
once in its test. No
test begins two unfinished runs on one store, so none meets `begin`'s new refusal.
`test_pipeline_adoption.py:347-365` registers the driver once on its store (`:349`, the one
`self.register(` in the tests).

`test_pipeline_adoption.py:151` asserts `list`'s row matches `running\s+-\s` for a stage-only run;
measured at `v0.2.0`, it does, and `:164-165`'s fragments are still printed. `test_killed_handler.py:327` and
`:426` patch the private `Run._fingerprint_results`, which `v0.2.0` keeps unchanged, and assert its
`"names no results store"` (`:338`, `:437`), which `v0.2.0` keeps.

## 8. `pid_alive`, and record key sets

No SGK code relies on `pid_alive` raising: its two calls (§3) treat a false answer as "gone".
`$ git -C <SGK> grep -n -E '\.keys\(\)|sorted\(manifest|set\(manifest|sorted\(status|set\(status|assertEqual\(set\(' 79434bf -- RunDrivers/tests ObjectFactories/tests`
finds only datastore columns and work lists (`ObjectFactories/tests/test_backgroundmodelvalue_roundtrip.py:203-205`,
`test_factory_select_columns.py:1019`, `test_quadsource_integral_parent_key.py:295`,
`test_value_reads_parent_key.py:481`): no test pins the manifest's or the status's key set, so the
new `host` and `ended` break none.

## 9. Its stale-run brief, point by point

SGK's `prompts/handover/runregistrykit-stale-run-brief.md` (at `79434bf`), with the prompt of this
campaign that answered each point, or that none did:

| Brief | Point | Answered by |
|---|---|---|
| §1, the defect | a hard-killed run stays `running`, and no command ends it | **04**: `python -m runregistrykit end` |
| §1, the in-use check | the store operations count a stale `running` run as in use | kept by design; **03** widened it to a status that does not say; **05** applies it at `begin` |
| §1, the remedy's words | the refusals name `Run.finish` | **04**: they name `end` |
| §1, no command | no command writes a `status.json` | **04** |
| §1, the remedy checks nothing | `Run.finish` checks no pid | **04**: `end` checks the pid, the host and the boot; `Run.finish` is unchanged (L8), and still checks nothing when called by hand |
| §1, the resumed run's fingerprint | refused by its stale predecessor | **04** with **05**: the predecessor is ended first, and the fingerprint is then recorded (§4) |
| §1, `begin` does not look | a second writer is not refused | **05** |
| §1, related | a signal inside a heartbeat write can lose the terminal state | **02**, **02b**, **02c** |
| §1, option 1 | a person-run command, `lost` | **04**, as SGK preferred |
| §1, option 1, guarding `Run.finish` on a run not the caller's | | none: not taken (L8 (c)) |
| §1, option 2 | an exclusion on the store operations | none: not taken |
| §1, option 3 | `begin` naming and superseding a stale run | none, but its second-writer guard by **05**, which refuses alive and stale alike and records no supersession |
| §1, the test | a real `SIGKILL`, not a faked pid | **04** (`test_end.a_hard_killed_run`) and **05** |
| §2, asked | read, index and tell SGK | the issue was indexed and closed by 04 (the board's §4); telling SGK is the user's |
| §2, not asked | no release before A3 v2 | none needed: A3 v2 runs on `v0.1.0`; if it is hard-killed before SGK moves its pin, `Run.finish` by hand after `kill -0` stays SGK's route (the brief's §1, step 6) |
