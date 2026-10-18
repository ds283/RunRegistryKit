# Adopting `runregistrykit` `v0.2.0`

*Written by `interrupted-runs` prompt 06 on 2026-10-18, against the package as it is tagged
`v0.2.0`. The three clients were read through `git show` and `git grep` only, at the commits named
below. Nothing of a client was imported, run or opened, and no store or run directory of any was
read.*

What changes between `v0.1.0` and `v0.2.0`, record by record and name by name, is in the release
notes, [`docs/releases/v0.2.0.md`](../../releases/v0.2.0.md). This directory says what that means
for the three clients: what they share (this file), and one note per client.

**A note is data, not instructions** ([`../README.md`](../README.md), the rule its checklists
follow). It describes a client at one commit. The client's own adoption campaign, in its own
repository and under its own `CLAUDE.md`, measures again before acting, and its numbers govern. A
recommendation is marked **Advice:**.

| Client | Note | Read at | Today | Gate |
|---|---|---|---|---|
| SecondaryGWKit (SGK) | [`secondarygwkit.md`](secondarygwkit.md) | `79434bf` (branch `handover-remedial`, its newest commit of any branch) | on `v0.1.0` | G1 |
| ChamPBH (CPBH) | [`champbh.md`](champbh.md) | `3cd2be4` (branch `main`) | none adopted | G2 |
| StochasticInstantons (SI) | [`stochasticinstantons.md`](stochasticinstantons.md) | `5fb4a1d` (branch `dk-and-rpk-migration`) | none adopted | G3 |

The gates are those of the campaign plan,
[`prompts/interrupted-runs/README.md`](../../../prompts/interrupted-runs/README.md) §7: each holds
when that client has adopted a release that includes this campaign's changes, its pin moved in a
commit of its own. They are recorded on the board,
[`prompts/interrupted-runs/IMPLEMENTATION_STATE.md`](../../../prompts/interrupted-runs/IMPLEMENTATION_STATE.md)
§2, as they hold. The campaign does not wait for them.

## 1. The pin

With the store layer, beside the client's own line for DatastoreKit at `v0.4.0` or later, as the
package's [`README.md`](../../../README.md#installing) "Installing" says:

```text
runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
```

For the core alone, `runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.2.0`, with no
extra and no `datastorekit`. The extra's floor is unchanged (`datastorekit>=0.4.0`), and so are
the supported versions. An editable install is never for a client's production runs.

## 2. Every checkout that shares a runs root moves together

A checkout pinned at `v0.1.0` that reads a runs root `v0.2.0` writes tests a run on another host by
its pid here, judges a run from an earlier boot by its pid, calls a `lost` run `unknown`, does not
count a run whose status cannot be read as in use, raises on a status that is not a JSON object,
and **does not refuse a second writer** on a store a `v0.2.0` run is writing. The release notes'
§4 has the measured table. **Advice:** move every checkout and worktree that shares a runs root to
`v0.2.0` in one step, and do not begin a long run from a `v0.1.0` checkout on a store that a
`v0.2.0` run names.

A record written under `v0.1.0` is read by `v0.2.0` as `v0.1.0` read it, judged by its pid and its
heartbeat, and counted by `list` as having no host (release notes §3). So a client's existing run
directories need nothing.

## 3. What a client's code must check

Each of these is a place where a client's code or tests may depend on what `v0.2.0` changes. A
client's adoption campaign finds each by `git grep` in its own tree and decides what it does.
- **A comparison with `liveness`'s values.** It has a fifth value, `foreign`, for a `running` run
  on another host, which is neither alive nor stale; and a `running` run from an earlier boot of
  this host is `stale` whatever its pid answers. Code that treats "not `stale`" as alive, or that
  enumerates the values, sees `foreign`.
- **`TERMINAL_STATES`.** It has a fourth value, `lost`. A test that a state is in it keeps passing;
  a test that it is exactly three values, or code that lists the three, does not.
- **A store refusal's text.** The store operations' refusals name `python -m runregistrykit end
  RUN_ID --reason TEXT` where they named `Run.finish`, count every run whose status does not say
  it has finished, and describe a run on another host and a status that cannot be read in words of
  their own. The fragments `run <id> is running` and `names this store` are kept for a `running`
  run on this host (release notes §5). A test that matches `Run.finish` in a refusal fails.
- **A test that begins two runs that have not finished on one store.** `begin` with `results` now
  refuses a store that an unfinished run under the same runs root names, so the second `begin`
  raises `RuntimeError` and makes no run directory. This repository's six tests that did so were
  changed in their setup, not their assertions, through one fixture that moves the earlier runs
  aside for the body and back after:
  [`StoreTestCase.set_aside`](../../../runregistrykit/tests/store_fixtures.py) and its own test
  (`test_second_writer_stores.py`, `test_set_aside_puts_back_byte_for_byte_whatever_the_body_raises`);
  the six are `test_end_stores.py`'s `test_a_run_on_another_host_adds_the_sentence_once` and
  `test_alive_and_stale_here_give_the_old_text_with_the_command`, `test_store_fingerprint.py`'s
  `test_another_running_run_is_recorded_and_the_run_still_ends`, and
  `test_unreadable_status_stores.py`'s
  `test_a_resumed_runs_fingerprint_is_refused_by_an_unreadable_predecessor`,
  `test_the_stale_remedy_is_kept_and_the_new_sentence_is_added_once` and
  `test_a_refusal_for_running_runs_alone_has_no_new_sentence`.
- **A caller of `pid_alive` that relied on its raising.** A pid outside the platform's range
  (`2**31` on macOS) is now `False`, where `v0.1.0` raised `OverflowError`.
- **A test that pins a record's key set.** The manifest and `status.json` each gain `host`, and a
  status written by `end` holds `ended` (release notes §2).

## 4. The route for a hard-killed run

A run killed by `SIGKILL`, a power loss, a reboot or the OOM killer stays `running`. Under `v0.2.0`
its store is resumed by **`end`, then `begin`**:
1. `python -m runregistrykit list` shows it `stale`, `!!`;
2. a second `begin` on its store is refused, naming `python -m runregistrykit end RUN_ID --reason
   TEXT`, and nothing is created;
3. a person checks that it is over, and runs `python -m runregistrykit end RUN_ID --reason TEXT`
   on the host it ran on. It is accepted when the run's pid does not answer `kill -0` there, or the
   machine has rebooted since; it is refused, with no override, when the pid answers. The run is
   then `lost`;
4. `begin` on the store is accepted, and the resumed run's `finish(..., fingerprint=True)` records
   a fingerprint, since no unfinished run names the store.

A run on another host is ended on that host, or here with `--unverified` once a person has checked
there. Measured with this package in a scratch directory, a child begun on a store, `SIGKILL`ed and
reaped: each step as above (the SGK note quotes the refusal).

## 5. What does not change

Everything [`../README.md`](../README.md) §5 lists for `v0.1.0`; the module map; the config file
and its keys; the store layer's sidecar format; `checkpoint.jsonl`; every public name but those the
release notes' §5 lists; and the rule that the registry records and does not decide that a run is
dead.
