# Log — prompt 06, release `v0.2.0`

- **Subject:** Prepare the v0.2.0 release: version, README and notes
- **Commit:** this commit, on `main` after `c4f2abc` (the orchestration note's commit)
- **Result:** landed, not yet reviewed. `pyproject.toml` says `0.2.0`; the README describes
  `v0.2.0`; the release notes and the adoption notes are new; the release check passed on this
  machine. No file under `runregistrykit/` or `.github/` changed. The suite is 410 before and
  after. **No tag is made and nothing is pushed**: `v0.2.0` is ready to be tagged on this commit
  once CI has passed on it, all three jobs (the prompt's §7).
- **Model:** Claude Opus 5.5. The session was interrupted once by a usage limit after breakage (a)
  and (b) had run, and resumed; on resuming, no child process of this work was running, no scratch
  venv was left mid-install, no Ray process was running, and `git status` showed `pyproject.toml`
  alone modified.

## What shipped

- **`pyproject.toml`**: `version = "0.1.0"` → `version = "0.2.0"`, one line (`git diff --numstat`:
  `1 1`). Nothing else in it changed.
- **`README.md`**, the prompt's §2.3 rows and nothing else:
  - Status (`:12-25`): `v0.2.0`, with `v0.1.0`'s sentences kept, one sentence on what an
    interrupted run needs, a link to the release notes, the extraction's links kept, and this
    campaign's plan and board added;
  - the prompt's `:40-41` (now `:47-48`) unchanged: PyPI's newest `ray` is still 2.59.0 (read 2026-10-18, below);
  - the two pins (`:58`, `:69`) at `@v0.2.0`;
  - "A run": `begin`'s refusal of a store a run that has not finished names (`:119-129`), and a
    paragraph on the host it records (`:131-137`); `finish`'s three states and `lost` (`:145-148`);
    the temporary name of `status.json` (`:154-157`);
  - `list` (`:159-178`): the five liveness values, `??` and `!!`, the summary's host count, a
    record with no host, and the stderr lines that name `end`;
  - new, "Ending a run whose end was never recorded" (`:180-206`);
  - the store layer's refusal (`:253-254`), the interface sentence on release notes (`:262-263`),
    rule 2's added sentence (`:291-292`), `this_host` among the public names (`:351`), the
    patch-target sentence (`:367-370`) and CI's seven core modules (`:392-394`).
- **`docs/releases/v0.2.0.md`** (new): §1 what it is; §2 what the registry writes, with the field
  table (§2.1), `end`'s status in its three measured forms (§2.2), the temporary names (§2.3), the
  two forms of `host` (§2.4), what is unchanged (§2.5), and what `id`, `boot` and a `null` mean
  (§2.6); §3 a `v0.1.0` record read by `v0.2.0`; §4 a `v0.2.0` record read by `v0.1.0`, with the
  measured table; §5 the public interface; §6 the five known issues. It names no client.
- **`docs/adoption/v0.2.0/`** (new): `README.md` (what the three share: the pin, moving together,
  the six checks, the route for a hard-killed run, the table of clients and commits, the gates
  G1–G3); `secondarygwkit.md`; `champbh.md`; `stochasticinstantons.md`.
- **`docs/adoption/README.md`**: one section at its end, "`v0.2.0`", and nothing above it changed.
- **The records**: this log; the board (header, §1's row for 06, V1); the campaign README's §2 row
  for 06; `prompts/INDEX.md`'s line. `docs/OPEN_ISSUES.md` is unchanged (the work opens no issue;
  it stays at 10).

## Deviations from the prompt

Each correction of the brief is recorded where it departs from the prompt.

1. **L10 is (a)** (correction 1). Nothing in the prompt was conditional on it. *STRUCTURALLY
   REQUIRED* (a reading; no departure).
2. **`pip freeze` is identical before and after the reinstall** (correction 3), where the prompt
   expected `runregistrykit`'s line to change: the editable line names the commit
   (`-e git+https://github.com/ds283/RunRegistryKit.git@c4f2abc…#egg=runregistrykit`), not the
   version, and the commit did not move. The version is recorded instead by
   `importlib.metadata.version` from the repository root and from a scratch directory: `0.1.0`
   at both before, `0.2.0` at both after. *STRUCTURALLY REQUIRED.*
3. **The release check resolves DatastoreKit by its commit, offline** (correction 4):
   `datastorekit @ git+…@c8570e849334d09085bbd84876095fc9e22bd005`, the commit the tag `v0.4.0`
   peels to (`git ls-remote`: tag object `8e7c1d77…`, `v0.4.0^{}` `c8570e84…`), since `--offline`
   cannot fetch a tag. Nothing was downloaded. *STRUCTURALLY REQUIRED.*
4. **The measurements import each tree by `PYTHONPATH`, without `-I`** (correction 5), from a
   scratch working directory, with `venv/`'s Python; every script prints `runregistrykit.__file__`
   and asserts that it lies under its export. A manifest's `packages.runregistrykit.version` comes
   from the installed metadata (here `0.2.0` for both trees, since the measurements ran after the
   reinstall), so it is no evidence of the writer; shapes are compared, not that value.
   *STRUCTURALLY REQUIRED.*
5. **The mixed-version rows** (correction 6): an "alive" pid is a child the driver starts
   (`time.sleep(600)`) and keeps alive while both trees read, then kills and reaps; both readers
   recorded `pid_alive` true for it at the start and at the end of their reading. A dead pid is
   each writer's `RegistryTestCase.a_dead_pid()`; both readers recorded it false. `foreign` and an
   earlier boot each have a live-pid and a dead-pid row. *STRUCTURALLY REQUIRED.*
6. **The status `[1]` row is measured in a runs root of its own.** In one runs root with the others,
   `v0.1.0`'s `list_runs` raised `AttributeError` on it, so `v0.1.0`'s reader could read no row at
   all. It is measured beside one alive run of each tree, and the release notes' table says so.
   *STRUCTURALLY REQUIRED* (found by the measurement).
7. **"as `store --help` says"** (§2.3's store-layer row): `store --help` lists the subcommands and
   carries no description at either tag; the wording "any run names whose status does not say it
   has finished" is the top-level `--help` (the module docstring of `__main__.py`). The README states
   the rule without citing a help text, and the release notes (§5) name the top-level `--help`.
   *STRUCTURALLY REQUIRED* (correction 9: the code governs).
8. **"the remedy lines name `end`"** (§2.3's `list` row): of `list`'s three stderr lines, the stale
   one and the one for a status that does not say name `end`; the one for runs on another host says
   "Look on that host" (`__main__.py:682-691`). The README says "the first two lines name `end`".
   *STRUCTURALLY REQUIRED.*
9. **The clients' `git grep -i runregistrykit`** finds more than the prompt's "At writing" says: at
   CPBH `3cd2be4`, nine lines (one docstring, eight in its campaign records), where it said one
   docstring; at SI `5fb4a1d`, three lines in its campaign records, where it said none. None is
   code (`git grep -n -i -E '^\s*(import|from) runregistrykit'` finds nothing at either). The notes
   report the hits as found. *STRUCTURALLY REQUIRED.*
10. **The README's Status** keeps `v0.1.0`'s sentences by opening "`v0.1.0` was the `RunRegistry/`
    package…", and adds the `v0.2.0` sentence after them. *IMPLEMENTATION CHOICE.*
11. **The host paragraph** in "A run" is its own paragraph after `begin`'s, rather than inside it,
    and names `RUNREGISTRYKIT_HOST_NAME` and `platform.node()` for `name`. *IMPLEMENTATION CHOICE.*
12. **`end`'s section** is a `###` subsection after "A run", before "The store layer", as the
    prompt's "new, after `list`" places it. *IMPLEMENTATION CHOICE.*
13. **The release notes' §2** has six subsections (the table, `end`'s forms, the temporary names,
    the two forms of `host`, what is unchanged, `id`/`boot`/`null`) where the prompt lists the
    content without dividing it. *IMPLEMENTATION CHOICE.*
14. **The release notes' §4 table** shows both tags' readings side by side, the `v0.2.0` columns for
    comparison. *IMPLEMENTATION CHOICE.*
15. **The name check (d) covers the README's changes**, as the prompt's (d) says. The release and
    adoption notes' names, fields and citations are checked by the field check (c), the document
    check (links, anchors, package citations, the known issues), the measurement scripts and the
    `git show`/`sed -n` reads listed under §3.5 below. *IMPLEMENTATION CHOICE.*
16. **Breakage (a) and (b) were installed into the release check's venv** (the one other venv),
    each by `uv pip install --offline --reinstall-package runregistrykit` with the same four
    requirements; the good wheel was reinstalled after and the check passed again; then the venv was
    removed. A first attempt that named only the broken wheel failed to resolve offline
    (`datastorekit` not in the cache by name) and installed nothing. *IMPLEMENTATION CHOICE.*
17. **The board's sentence counting the suite after each prompt** (`IMPLEMENTATION_STATE.md`
    §1, "The suite is 276 at `79015a7` …") is not extended to 06: correction 17 allows 06's row and
    the header only. The row says 410 → 410. *STRUCTURALLY REQUIRED.*

None is UNINTENDED DRIFT.

## Verification performed

All in `/private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/ff3563ad-f02f-4fbd-91de-b84e2835fb6b/scratchpad/agent-06/`
("scratch" below), with `TMPDIR` in it; no scratch file under `runregistrykit/` or `docs/`, no
build in the repository.

### §3.1 The suite

| | Before the reinstall | After |
|---|---|---|
| `Ran` | **410 tests in 144.700s** | **410 tests in 147.499s** |
| Verdict | `OK (skipped=1)` | `OK (skipped=1)` |
| `pgrep -lf 'gcs_server\|raylet\|ray::\|default_worker\.py'` before / after | none / none | none / none |

`RAY_ADDRESS` unset. By the loader (after): `test_client_root` 27, `test_end` 27, `test_end_stores`
4, `test_fingerprinter` 31, `test_host` 28, `test_host_stores` 3, `test_package_imports` 3,
`test_package_is_generic` 22, `test_public_names` 8, `test_run_registry` 29, `test_second_writer`
23, `test_second_writer_stores` 9, `test_status_writes` 22, `test_store_amend` 21,
`test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
`test_store_fingerprint` 29, `test_store_retire` 41, `test_store_retire_references` 10,
`test_store_sidecar` 17, `test_unreadable_status` 11, `test_unreadable_status_stores` 7 — the
brief's counts, unchanged. `var/ledger.jsonl` `471d0859…` before and after.

### §2.1 The venv

- `./venv/bin/python -m pip install --no-deps -e .`: exit 0, "Successfully uninstalled
  runregistrykit-0.1.0 … Successfully installed runregistrykit-0.2.0". `setuptools` came from
  `pip`'s isolated build (correction 3).
- `pip freeze` before and after: **identical** (deviation 2); its line `-e
  git+https://github.com/ds283/RunRegistryKit.git@c4f2abc38e27d351b8460287d7de1af1cc52d89b#egg=runregistrykit`.
- `importlib.metadata.version("runregistrykit")`: before `0.1.0` from the repository root and
  `0.1.0` from scratch; after `0.2.0` from the root (twice) and `0.2.0` from scratch (twice, with
  `runregistrykit.__file__` the checkout's).
- `site-packages`: `__editable___runregistrykit_0_1_0_finder.py`, `__editable__.runregistrykit-0.1.0.pth`
  and `runregistrykit-0.1.0.dist-info` → the same three at `0_2_0` / `0.2.0`; the ignored
  `runregistrykit.egg-info/PKG-INFO` says `Version: 0.2.0`. No `build/` or `dist/` in the
  repository.

### §3.8 `git status --short --ignored`

Before: `!! prompts/.DS_Store`, `!! runregistrykit.egg-info/`, `!! runregistrykit/__pycache__/`,
`!! runregistrykit/tests/__pycache__/`, `!! var/`, `!! venv/`. After the reinstall and both suite
runs: the same six, plus ` M pyproject.toml`. Before committing, the same ignored six plus this
commit's files.

### §3.2 The release check

- **Export:** `git archive c4f2abc38e27d351b8460287d7de1af1cc52d89b` into an empty `scratch/export`,
  this checkout's `pyproject.toml` copied over it (identical by `diff`), then `uv build --offline
  --wheel --out-dir scratch/dist .` (`uv` 0.12.20): exit 0.
- **The wheel:** `runregistrykit-0.2.0-py3-none-any.whl`, **66 257 bytes**, SHA-256
  **`1a169488accff8357108e66c314b97c8544d1269ba46b9d39c13a65a602144c9`**, **ten entries**:
  `runregistrykit/__init__.py`, `runregistrykit/__main__.py`, `runregistrykit/client.py`,
  `runregistrykit/fingerprint.py`, `runregistrykit/stores.py`,
  `runregistrykit-0.2.0.dist-info/licenses/LICENSE`, `…/METADATA`, `…/WHEEL`, `…/top_level.txt`,
  `…/RECORD`. `METADATA`: `Metadata-Version: 2.4`, `Name: runregistrykit`, **`Version: 0.2.0`**,
  `Requires-Python: >=3.12`, `License-File: LICENSE`, `Provides-Extra: stores`,
  **`Requires-Dist: datastorekit>=0.4.0; extra == "stores"`**, `Dynamic: license-file`.
  `scratch/scripts/wheel_check.py`: every check PASS.
- **The venv:** `uv venv -p /opt/local/bin/python3.13 scratch/release` (3.13.16); `uv pip install
  --offline -p scratch/release/bin/python "runregistrykit[stores] @ file://<wheel>" "datastorekit @
  git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005"
  "ray==2.55.1" "sqlalchemy==2.0.46"`: "Resolved 21 packages … Installed 21 packages", among them
  `datastorekit==0.4.0 (from git+…@c8570e8…)`, `ray==2.55.1`, `sqlalchemy==2.0.46` and
  `runregistrykit==0.2.0 (from file://…/runregistrykit-0.2.0-py3-none-any.whl)`.
- **The check**, `scratch/scripts/release_check.py`, run as `scratch/release/bin/python -I` from the
  empty `scratch/empty`: the five modules import from `scratch/release/lib/python3.13/site-packages/`;
  `importlib.metadata.version` `0.2.0`; `this_host` in `__all__`, callable, `() -> dict`; `import
  runregistrykit.tests` raises `ModuleNotFoundError: No module named 'runregistrykit.tests'`;
  `python -I -m runregistrykit --help` exit 0 (it lists `{list,end,store}`) and `end --help` exit 0
  (`usage: runregistrykit end [-h] --reason TEXT [--unverified] [--root DIR] RUN_ID`); the
  installed files are the five modules and the `dist-info`. **RESULT PASS.** The venv was removed
  after the breakage below.

### §3.3 The release notes' measurements

**Shapes** (`scratch/scripts/lifecycle.py`, at `git archive v0.1.0` and `git archive c4f2abc`, each
tree's `test_store_retire.RetireTestCase` methods on a full store with a registry sidecar,
`client_fixtures.write_client_root` for the client root; outputs `scratch/out/lifecycle-*.json`,
compared by `scratch/scripts/compare_shapes.py` into `scratch/out/shapes-compare.txt`):

| What | `v0.1.0` | `v0.2.0` |
|---|---|---|
| manifest | `argv`, `campaign`, `checkpoint`, `created`, `cwd`, `expected_units`, `git_dirty`, `git_head`, `heartbeat_means`, `packages` {`runregistrykit` {`commit`, `editable`, `requested_revision`, `url`, `version`}}, `prompt`, `purpose`, `results`, `results_store_id`, `run_id`, `scope`, `script`, `script_sha256`, `unit` | the same, plus **`host` {`id`, `machine`, `name`, `python`, `release`, `system`}**, each a string here |
| `status.json` after `begin` | `exit_code`, `heartbeat`, `pid`, `state`, `units_done`, `units_total` | the same, plus **`host` {`boot`, `id`}**, strings here |
| after `heartbeat(stage=…)` | the above and `stage` | the same, with `host` |
| after `finish("done", 0, fingerprint=True)` | the above, `exit_code` int, `fingerprint` {…}, `fingerprint_sidecar` `"written"` | the same, with `host` |
| after `end`, verified | — | every running key kept (`exit_code`, `heartbeat`, `host`, `pid`, `state`, `units_done`, `units_total`), `state` `"lost"`, `exit_code` null, **`ended`** {`at`, `by`, `evidence` {`boot`, `heartbeat`, `heartbeat_age`, `host`, `pid`, `pid_answers`, `state`, `status_readable`}, `git_head`, `host` {`boot`, `id`, `name`}, `not_verified_because` null, `reason`, `verified` true}; evidence `host` `"this"`, `boot` `"this"`, `pid_answers` false |
| after `end --unverified`, torn status | — | **only** `ended`, `exit_code` null, `heartbeat`, `state` `"lost"`; `verified` false, `not_verified_because` `"status does not say"`; evidence `status_readable` false, `host` `"not recorded"`, the rest null |
| after `end --unverified`, another host | — | `verified` false, `"another host"`; evidence `host` `"another"`, `boot` null, `pid_answers` null |
| a ledger line | `data`, `git_dirty`, `git_head`, `recorded`, `script_sha256`, `unit` | **identical** |
| the sidecar, before and after a fingerprint | `created`, `datastore`, (`fingerprint`), `history` [{`from`, `git_dirty`, `git_head`, `operation`, `to`, `when`}], `name`, `purpose`, `sidecar_format`, `store_id` | **identical** |
| the run directory | `checkpoint.jsonl`, `manifest.json`, `status.json` | **identical**; after `end`, `manifest.json`, `status.json` (no ledger asked) |
| `os.replace`s | `manifest.json.tmp`, `status.json.tmp` (every status write), `store.manifest.json.tmp` (the sidecar's fingerprint) | `manifest.json.tmp`, **`status.json.<pid>-<n>-<hex>.tmp`** (e.g. `status.json.73491-0-8cde4be9.tmp`) for every status write including `end`'s, `store.manifest.json.tmp` |
| `status.json`'s mode, umask `0o22` | `0o644` | `0o644` |
| `list_runs` entry keys | `created_epoch`, `has_manifest`, `id`, `liveness`, `path`, `pid`, `purpose`, `stage`, `state`, `units_done`, `units_total` | the same, plus **`host`, `host_id`, `host_recorded`, `status_readable`** |
| `this_host()` | — | `id` (16 hex), `boot`, `name`, `machine` `arm64`, `system` `Darwin`, `release` `27.0.0`, `python` `3.12.15` |

So the registry writes nothing the campaign's prompts and logs do not account for (README §5 rule
7): the two `host` records (01), `lost` and `ended` (04), and the temporary name (02).

**The public interface** (`inspect.signature` over every `__all__`, and `Run`'s public methods, at
both trees): `TERMINAL_STATES` `('done', 'failed', 'killed')` → `(…, 'lost')`; `liveness(status,
stale_after, now=None) -> str` → `(status, stale_after, now=None, *, here=None) -> str`;
`this_host() -> dict` new. Every other name identical (`amend_sidecar`'s signature differed in one
run only by the address in its `_NO_VALUE` sentinel's repr, and not in another; not a change).
`Run.finish`'s code is identical at both trees by its syntax tree with the docstring removed
(`scratch/scripts/finish_source.py`), and so are `_fingerprint_results`, `heartbeat` and `record`.
`pid_alive(2**31)`: `v0.1.0` raises `OverflowError: signed integer is greater than maximum`;
`v0.2.0` returns `False` (`scratch/out/fragments.txt`). A manifest or status `[1]`: `v0.1.0`'s
`list_runs` and `liveness` raise `AttributeError: 'list' object has no attribute 'get'`; `v0.2.0`'s
read the manifest as none (`has_manifest` false) and the status as `unknown`
(`scratch/out/nonobject.txt`).

**`--help`** (`scratch/scripts/helps.sh`, the command and every subcommand, `scratch/out/help-*.txt`):
the top-level usage `{list,store}` → `{list,end,store}`, its description's store sentences "a
store that any `running` run names, alive or stale" → "a store that any run names whose status does
not say it has finished" / "such a run", and a new paragraph on `end`; `end --help` new (exit 2 at
`v0.1.0`: "invalid choice: 'end'"); `list --help`, `store --help` and each `store` subcommand's help
identical.

**Mixed versions** (`scratch/scripts/mixed/driver.py`, `writer.py`, `reader.py`, `table.py`; outputs
`scratch/out/mixed-*.json`, `scratch/out/mixed-table.txt`). One runs root; each writer, with its
own tree's fixtures, makes its client root, a full store per row, and its runs. Live child pid
74591 (main) and 74883 (non-object root), each killed and reaped at the end (returncode −9); dead
pids 74616 and 74662 (main), false in both readers. Each reader: `list_runs`' liveness, `list`
(exit code and marker), `fingerprint_store` on the row's store, and a second `begin` on it (a run
so begun is removed at once, so that it changes no later reading).

| Written by | Row | pid alive when read | Read by | liveness | `list` marker | `fingerprint_store` | second `begin` |
|---|---|---|---|---|---|---|---|
| v0.1.0 | alive | true | v0.1.0 | alive | none | refused (alive) | begun |
| v0.1.0 | alive | true | v0.2.0 | alive | none | refused (alive) | refused (alive) |
| v0.1.0 | stale | false | v0.1.0 | stale | `!!` | refused (stale) | begun |
| v0.1.0 | stale | false | v0.2.0 | stale | `!!` | refused (stale) | refused (stale) |
| v0.1.0 | done | — | v0.1.0 | finished | none | proceeded | begun |
| v0.1.0 | done | — | v0.2.0 | finished | none | proceeded | begun |
| v0.2.0 | alive | true | v0.1.0 | alive | none | refused (alive) | begun |
| v0.2.0 | alive | true | v0.2.0 | alive | none | refused (alive) | refused |
| v0.2.0 | stale | false | v0.1.0 | stale | `!!` | refused (stale) | begun |
| v0.2.0 | stale | false | v0.2.0 | stale | `!!` | refused (stale) | refused |
| v0.2.0 | done | — | v0.1.0 | finished | none | proceeded | begun |
| v0.2.0 | done | — | v0.2.0 | finished | none | proceeded | begun |
| v0.2.0 | lost | false | v0.1.0 | **unknown** | none | proceeded | begun |
| v0.2.0 | lost | false | v0.2.0 | finished | none | proceeded | begun |
| v0.2.0 | foreign, live pid | true | v0.1.0 | **alive** | none | refused (alive) | begun |
| v0.2.0 | foreign, live pid | true | v0.2.0 | foreign | `??` | refused (another host) | refused |
| v0.2.0 | foreign, dead pid | false | v0.1.0 | **stale** | `!!` | refused (stale) | begun |
| v0.2.0 | foreign, dead pid | false | v0.2.0 | foreign | `??` | refused (another host) | refused |
| v0.2.0 | earlier boot, live pid | true | v0.1.0 | **alive** | none | refused (alive) | begun |
| v0.2.0 | earlier boot, live pid | true | v0.2.0 | stale | `!!` | refused (stale) | refused |
| v0.2.0 | earlier boot, dead pid | false | v0.1.0 | stale | `!!` | refused (stale) | begun |
| v0.2.0 | earlier boot, dead pid | false | v0.2.0 | stale | `!!` | refused (stale) | refused |
| v0.2.0 | status torn | — | v0.1.0 | unknown | **none** | **proceeded** | begun |
| v0.2.0 | status torn | — | v0.2.0 | unknown | `!!` | refused (cannot be read) | refused |
| v0.2.0 | status `[1]` (own root) | — | v0.1.0 | **`list_runs` raised** | `list` exit 1, traceback | **raised `AttributeError`** | begun |
| v0.2.0 | status `[1]` (own root) | — | v0.2.0 | unknown | `!!` | refused (cannot be read) | refused |

In the `[1]` root, `v0.1.0`'s `fingerprint_store` raised `AttributeError` for the alive runs'
stores too, and its `list` exited 1; `v0.2.0`'s `list` exited 0, "3 run(s) … 2 alive, 1 unknown; 2
with no host recorded.". In the main root, `list` exited 0 at both: `v0.1.0` "12 run(s) … 4 alive,
2 finished, 4 stale, 2 unknown." and one stderr line (stale); `v0.2.0` "12 run(s) … 2 alive, 3
finished, 2 foreign, 4 stale, 1 unknown; 4 with no host recorded." (the three `v0.1.0` runs and the
torn one) and three stderr lines (stale, does not say, another host). `v0.2.0`'s second `begin`
refusals begin `Cannot begin run second-v0.2.0-x-… with results "<store>": run <id> is running
(alive, pid 74591) and names this store by its results and results_store_id. A stale run is ended
by a person, with `python -m runregistrykit end RUN_ID --reason TEXT`, …`, "running on another
host, <name> (pid …, not tested here)" for the `foreign` rows, and "status cannot be read
(status.json is missing, is not JSON, or is not a JSON object)" for the torn one. No child outlived
the driver (`pgrep -lf 'time.sleep\(600\)'` empty after).

### §3.4 The clients

Read with `git -C <repo> show <commit>:<path>` and `git -C <repo> grep … <commit>` only.
- **Newest commits** (`git log --all -1`): SGK `79434bf` (`handover-remedial`, 2026-10-16); CPBH
  `3cd2be4` (`main`, 2026-10-17; `c21cdfb..3cd2be4` is three commits, audit documents); SI
  `5fb4a1d` (`dk-and-rpk-migration`, 2026-10-12).
- **`requirements.txt`**: SGK `:17` `datastorekit …@v0.4.0`, `:75` `ray==2.43.0`, `:76`
  `raypoolkit …@v0.2.0`, **`:81` `runregistrykit[stores] …@v0.1.0`**, `:88` `SQLAlchemy==2.0.39`;
  CPBH `:17` `datastorekit …@v0.4.0`, `:79` `ray==2.53.0`, `:80` `raypoolkit …@v0.2.0`, `:91`
  `SQLAlchemy==2.0.46`; SI `:57` `ray==2.55.1`, `:65` `SQLAlchemy==2.0.46`, no `datastorekit`.
- **SGK** `git grep -n -i runregistrykit 79434bf` (outside `prompts/`): `CLAUDE.md` (the pin, the
  rules), `ObjectFactories/tests/test_fingerprint_format_guard.py:11`,
  `test_store_fingerprint_golden.py:7-143`, `RunDrivers/tests/registry_fixtures.py:4-45`,
  `test_build_rehearsal_scope.py:317`, `test_killed_handler.py:26-435`,
  `test_pipeline_adoption.py:26-356`, `test_quadsource_atol_sweep_prepare.py:4`, `:25`,
  `config/fingerprint.py`, `docs/OPEN_ISSUES.md`, and the probes and drivers under `docs/`.
  `git grep -n -E 'runregistrykit|begin\(|results=|finish\(|liveness|pid_alive|TERMINAL_STATES|--resume|signal\.signal' 79434bf -- <the two drivers>`:
  `scoped_pipeline_run.py:398`, `:476-496`, `:544`, `:555`, `:563`; `quadsource_atol_sweep.py:556`,
  `:562`, `:575`, `:869`, `:875`, `:894`, `:957-966`, `:996`.
  `git grep -n -E 'liveness\(|pid_alive\(|TERMINAL_STATES|Run\.finish|with Run.finish' 79434bf -- ':!prompts' ':!*.md'`:
  `test_pipeline_adoption.py:252`; `fingerprint_time_probe.py:2`, `:5`, `:9`; `interrupt_when.py:18`,
  `:165`, `:170`, `:175`, `:190`; `scoped_pipeline_run.py:455`; `tools/rehearsal_lock.py:147`,
  `:332`, `:363`, `:400` (its own `pid_alive`); two lines of `docs/runregistry-extraction/rehearsal/g2_measure_08.txt`.
  `git grep -n -E 'TERMINAL_STATES|names this store|is running"|Run\.finish|with Run.finish|"alive"|"stale"|"foreign"|liveness|pid_alive|results=' 79434bf -- RunDrivers/tests`:
  `test_pipeline_adoption.py:180` (the manifest's `heartbeat_means` text), `:252`;
  `test_quadsource_atol_sweep_prepare.py:194`, `:201`, `:202`.
  `git grep -n -E 'self\.begin\(|runregistrykit\.begin\(|register_main|--register' 79434bf -- RunDrivers/tests`:
  `registry_fixtures.py:45`, `test_build_rehearsal_scope.py:239`, `test_killed_handler.py:90`,
  `test_pipeline_adoption.py:4`, `:73`, `:257`, `:271`, `:282`,
  `test_quadsource_atol_sweep_prepare.py:194`; `self.register(`: `test_pipeline_adoption.py:349`
  only. `git grep -n -E '\.keys\(\)|sorted\(manifest|set\(manifest|sorted\(status|set\(status|assertEqual\(set\(' 79434bf -- RunDrivers/tests ObjectFactories/tests`:
  `test_backgroundmodelvalue_roundtrip.py:203-205`, `test_factory_select_columns.py:1019`,
  `test_quadsource_integral_parent_key.py:295`, `test_value_reads_parent_key.py:481`, all datastore
  columns and work lists. The stale-run brief, `prompts/handover/runregistrykit-stale-run-brief.md`,
  181 lines, read in full. SGK's `var/` was not read.
- **CPBH** `git grep -n -i runregistrykit 3cd2be4`: `ObjectFactories/tests/test_inventory_specs.py:27`;
  `prompts/dk-and-rpk-migration/09-port-the-inventory.md:47`, `:260`; `IMPLEMENTATION_STATE.md:47`;
  `README.md:1006`, `:1011`, `:1019`; `logs/09-port-the-inventory.md:714`;
  `orchestrator/prompt-09.md:36`. `git grep -n -i -E '^\s*(import|from) runregistrykit' 3cd2be4`:
  nothing.
- **SI** `git grep -n -i runregistrykit 5fb4a1d`: `.prompts/dk-and-rpk-migration/IMPLEMENTATION_STATE.md:179`,
  `:180`; `.prompts/dk-and-rpk-migration/README.md:1156`. The import grep: nothing.
- **SGK's route after a hard kill** (correction 13; `scratch/scripts/route.py`, `scratch/out/route.txt`),
  at `c4f2abc`'s tree with its fixtures: a child begun on a full store by
  `test_end.a_hard_killed_run`, `SIGKILL`ed and reaped (pid 75436, `pid_alive` false, liveness
  `stale`); the second `begin` refused, as raised: `Cannot begin run example-01-resume-20261018T162739
  with results "<store>": run example-01-hard-killed-20261018T162739 is running (stale, pid 75436)
  and names this store by its results and results_store_id. A stale run is ended by a person, with
  `python -m runregistrykit end RUN_ID --reason TEXT`, before another run is begun on its store; the
  registry does not decide that a run is dead. No run directory was created`, the runs root holding
  only the killed run; `python -m runregistrykit end <id> --reason … --root <runs root>`: exit 0,
  `>> end: example-01-hard-killed-20261018T162739 is now lost, verified: its pid 75436 does not
  answer kill -0 on this host`; `begin` again begun; its `finish("done", exit_code=0,
  fingerprint=True)`: `done`, 0, a `fingerprint` with a `digest`, `fingerprint_sidecar` `"written"`,
  the sidecar's `fingerprint.taken.run_id` the resumed run's. (A first run of the script called
  `end` without `--root`, which refused, "there is no run directory …", since the scratch runs root
  is not the config's; the script's mistake, corrected.) What `--build --resume` meets is read from
  `quadsource_atol_sweep.py:533-580` at `79434bf`: the pre-check, then `begin` at `:556`.
- **SGK's test fragments** (`scratch/scripts/fragments.py`, at both trees): a live run on a full
  store, `copy_store` refused at both, each message holding `run <id> is running` and `names this
  store`; `list`'s row for a stage-only run matches `running\s+-\s` and prints `92.31%` and the
  stage at both; `TERMINAL_STATES` holds `done`, `failed`, `killed` at both; `Run._fingerprint_results`
  exists at both, and `finish("killed", 143, fingerprint=True)` with no results records "the manifest
  names no results store to fingerprint" at both.

### §3.5 Every statement and name, and how each was checked

- **`ray`'s newest release** (correction 7): `https://pypi.org/pypi/ray/json`, `info.version`
  **2.59.0**, uploaded 2026-10-02: the README's `:40-41` unchanged.
- **The README's changes**: `scratch/scripts/name_check.py` over the backticked tokens on the lines
  `git diff -U0 HEAD -- README.md` adds, against `git archive c4f2abc`: 77 tokens, each a public name
  imported, a `Run` member, an argument found by `inspect.signature`, a command, option or metavar
  in `--help`, a liveness value produced by running `liveness`, a state, a record field or
  `this_host()` key, the environment variable the code reads, a test module of the tree on the
  workflow's core line, a pin naming `pyproject.toml`'s version, or a listed plain word. **RESULT
  CLEAN** (`scratch/out/name-check.txt`). The statements, against the code at the commit:
  `begin`'s refusal against `begin` (`__init__.py:1089-1126`) and its docstring, and measured (the
  mixed table, the route); the host paragraph against `this_host()` (`:578-609`) and `begin`
  (`:1127-1170`), and the shapes; `finish`'s sentence against its docstring (`:805-809`) and
  `TERMINAL_STATES` (`:105`); the temporary name against `_status_temporary_name` (`:292-297`) and
  the measured `os.replace`s; `list` against `liveness` (`:612-656`) and `__main__.py:627-691`, and
  the mixed table's markers and lines; `end` against `end --help`, `_end_run` (`:1259-1425`) and
  `__main__._end` (`:432-471`), and the route and the shapes; the store-layer sentence against
  `_running_runs_naming` (`stores.py:1002-1026`) and the top-level `--help`; rule 2 against
  `liveness`'s steps 2 and 3; the patch targets against `begin`'s import (`__init__.py:1091-1098`);
  CI's modules against `.github/workflows/tests.yml:89`.
- **The release notes' fields**: `scratch/scripts/field_check.py`, the table of §2.1 against the
  shapes at both trees: 32 rows; `manifest.json` 7 new fields, 7 named and written; `status.json`
  23 new fields, 25 named (with `state` and `exit_code`), all written. **RESULT CLEAN.** Types and
  meanings from the shapes, 04's §2.2 (`04-end-a-run.md:92-140`), `this_host()`'s docstring
  (`__init__.py:579-595`) and `_end_run`'s (`:1260-1295`); `ended.git_head` from `git_provenance`
  (`:150-164`, `"unknown"` when not a repository) on `ClientRoot.found`.
- **The release notes' §3–§5** against the mixed table, the shapes, the interface comparison and
  the `--help` diff above, each value traced to a row; the stale line's words against `__main__.py`
  at both tags; "no client named": `grep -n -i -E 'secondarygwkit|champbh|stochasticinstantons|\bSGK\b|\bCPBH\b|\bSI\b|A3 v2'`
  on the notes is empty.
- **The known issues**: `scratch/scripts/docs_check.py` reads the notes' §6 list and the board's §3
  headings: the same five, in order; each link's anchor is the heading's GitHub slug and exists.
  Each line is taken from its board entry (the defect and impact paragraphs).
- **Links and package citations**: `docs_check.py` over the seven documents: every relative link's
  target exists, every anchor exists (`#supported-versions`, `#installing`,
  `#ending-a-run-whose-end-was-never-recorded`, the five board anchors), and each
  `runregistrykit/…:N` citation printed and read: `__init__.py:1259` `def _end_run`, `:292` `def
  _status_temporary_name`, `:260` `def write_json_atomic`, `:578` `def this_host`. **RESULT CLEAN.**
- **The adoption notes' client citations**: every `path:line` re-read by `git -C <repo> show
  <commit>:<path> | sed -n` just before committing (SGK: `quadsource_atol_sweep.py:533-580`,
  `:855-880`, `:990-1002`; `scoped_pipeline_run.py:380-400`, `:452-456`, `:494-497`, `:515-530`,
  `:540-570`, `:675`; `interrupt_when.py:1-30`, `:155-230`; `test_pipeline_adoption.py:70-80`,
  `:130-170`, `:240-258`, `:340-365`; `test_quadsource_atol_sweep_prepare.py:180-215`;
  `test_killed_handler.py:86-100`, `:327`, `:338`, `:426`, `:437`;
  `fingerprint_time_probe.py:2`, `:5`, `:9`; `registry_fixtures.py:36-60`; CPBH
  `test_inventory_specs.py:25-29`; SI `IMPLEMENTATION_STATE.md:178-181`). Two citations were
  corrected while writing (`test_pipeline_adoption.py:150` → `:151`, `:163-164` → `:164-165`), and
  the loop of `interrupt_when.py` is `:160-208`.
- **05's six tests and their fixture**, named in the shared note, found by `grep -n 'with
  self.set_aside('` and the enclosing `def test_`: `test_end_stores.py:140`, `:171`;
  `test_store_fingerprint.py:737`; `test_unreadable_status_stores.py:120`, `:150`, `:177`; the
  fixture `store_fixtures.py:157`; its test `test_second_writer_stores.py:225`.
- **`black --check runregistrykit docs`**: "37 files would be left unchanged."

### The "For 06" lines, and where the notes honour each

| Line | Where |
|---|---|
| 01 (`logs/01-the-host.md:509`): `liveness` gains `foreign`; `this_host` public; `host` absent = written before 01, `null` = the platform offered none | release notes §5 (`liveness`, `this_host`), §2.4 and §2.6 (absent and `null`), §3 |
| 02 (`logs/02-status-writes.md:586`): "`write_json_atomic`: unchanged"; `status.json` through a name of its own, mode `0666` less the umask | release notes §2.3 |
| 02b (`logs/02b-the-writers-bookkeeping.md:629`): "`write_json_atomic`: unchanged"; the form not changed by 02b | release notes §2.3, §2.5 |
| 03 (`03-an-unreadable-status-is-in-use.md:109`): `list_runs`' new key | release notes §5 (`status_readable`), §3 |
| 04 (`logs/04-end-a-run.md:608`): `lost`, `ended`, `TERMINAL_STATES`; the README's usage of `end` | release notes §2.1–§2.2, §5; README "Ending a run whose end was never recorded" |
| 05 (`logs/05-begin-refuses-a-second-writer.md:617`): `pid_alive` from raising to `False`; the README's usage for `begin`'s refusal | release notes §5; README "A run" |

02c's and 03's logs have no "For 06" line.

## The deliberate-breakage record

None committed; `git status` here showed only this work's files after each.

**(a) `version` left at `0.1.0`**, applied to a fresh export (`scratch/export-a`, `git archive
c4f2abc` with this checkout's `pyproject.toml`) by `git apply`:

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -6,3 +6,3 @@
 name = "runregistrykit"
-version = "0.2.0"
+version = "0.1.0"
 description = "A run registry: run directories, manifests, heartbeats and datastore sidecars for long jobs"
```

The wheel is `runregistrykit-0.1.0-py3-none-any.whl`; `wheel_check.py`: FAIL at the name and at
`METADATA Version: 0.2.0`. Installed into the release venv: `release_check.py` prints `version
0.1.0` and FAIL at `importlib.metadata.version == 0.2.0`; RESULT FAIL.

**(b) the tests' `exclude` removed**, on `scratch/export-b` likewise:

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -21,2 +21,1 @@
 include = ["runregistrykit*"]
-exclude = ["runregistrykit.tests", "runregistrykit.tests.*"]
```

The wheel has 38 entries, `runregistrykit/tests/__init__.py` … `test_unreadable_status_stores.py`
among them; `wheel_check.py`: FAIL at "ten entries" and "no runregistrykit/tests/ entry". Installed:
`release_check.py` FAIL at `import runregistrykit.tests raises ModuleNotFoundError` (the import
succeeded); RESULT FAIL. The good wheel reinstalled after: RESULT PASS.

**(c) a field dropped from the notes' table and one added that is not written**, applied by `git
apply` to a scratch copy of the notes (`scratch/breakage/c-copy`; the diff `scratch/breakage/c.diff`):

```diff
--- a/docs/releases/v0.2.0.md
+++ b/docs/releases/v0.2.0.md
@@ -46,7 +46,7 @@
 | `manifest.json` | `host.python` | string | by `begin`: `platform.python_version()` | 01 |
 | `status.json` | `host` | object | by `begin`'s first write, from the same reading as the manifest's; kept by every later write (`heartbeat`, `heartbeat(pid=…)`, `record`, `finish`, `end`), except one on a status that could not be read, which has nothing to keep (§2.2) | 01 |
 | `status.json` | `host.id` | string or `null` | as `host` | 01 |
-| `status.json` | `host.boot` | string or `null` | as `host`: `this_host()["boot"]` | 01 |
+| `status.json` | `host.uptime` | number | as `host` | 01 |
 | `status.json` | `state` | the string `"lost"` | by `end` | 04 |
 | `status.json` | `exit_code` | `null` | by `end`: nothing observed an exit code | 04 |
 | `status.json` | `ended` | object | by `end`, once | 04 |
```

`field_check.py` on the document as written: RESULT CLEAN. On the copy: `MISSING status.json
host.boot: written at v0.2.0, not at v0.1.0, and not in the table` and `NOT WRITTEN status.json
host.uptime: in the table, and v0.2.0 does not write it`; RESULT 2 PROBLEM(S).

**(d) a name in the README's changes misspelled**, applied by `git apply` to a scratch copy of the
README (`scratch/breakage/d-copy`; `scratch/breakage/d.diff`):

```diff
--- a/README.md
+++ b/README.md
@@ -348,7 +348,7 @@ Each module's `__all__` is its public interface, and nothing else is:
 - `runregistrykit`, the core: `CONFIG_FILE`, `ClientRoot`, `ConfigError`, `DEFAULT_STALE_AFTER`,
   `Run`, `TERMINAL_STATES`, `begin`, `find_client_root`, `git_provenance`, `heartbeat_age`,
   `list_runs`, `liveness`, `now_iso`, `package_provenance`, `pid_alive`, `read_json`, `run_id`,
-  `script_sha256`, `slugify`, `this_host` and `write_json_atomic`;
+  `script_sha256`, `slugify`, `this_hosts` and `write_json_atomic`;
 - `runregistrykit.stores`, the store layer (it needs the extra `[stores]`): `AMEND_KEYS`,
   `AMEND_OPERATION`, `HISTORY_KEYS`, `IDENTITY_OPERATIONS`, `INCOMPLETE_MOVE_SUFFIX`,
   `KNOWN_FIELDS`, `RELOCATION_OPERATIONS`, `REQUIRED_FIELDS`, `RETIREMENT_STATES`,
```

`name_check.py` on the README as written: RESULT CLEAN. On the copy (its own `git diff -U0` against
`HEAD`'s README): `FAIL 'this_hosts': unclassified: not a name, argument, option, value, field or
plain word`; RESULT 1 PROBLEM(S).

## Observations not acted on

1. **Four lines of `stores.py` prose still describe the old in-use rule**, "a `running` run …,
   alive or stale": `fingerprint_store`'s docstring (`:1366`), `retire_store`'s (`:1640`), the
   comment at `:1727` and `amend_sidecar`'s docstring (`:2025`). The behaviour, which the README and
   the release notes state, counts every run whose status does not say it has finished. 03's log
   (observation 2) and 04's (observation 5) recorded three of them and opened no issue, as
   documentation only; this prompt changes nothing under `runregistrykit/`, so it follows them and
   opens none. `retire_store`'s `:1640` was not in their lists. 01's observation 3, which left the
   same lists for 06's README, is answered in the README alone.
2. **The README's opening paragraph** still says `list` judges a run "by its pid and its heartbeat"
   (`:7-8`). The prompt keeps that paragraph's text; "A run" and rule 2 say what the host adds.
3. **SGK's `interrupt_when.py:161`** reads the status as `read_json(…) or {}` and calls `.get`, so a
   status that is JSON but not an object raises in SGK's own code at either release. SGK's, and
   the registry writes no such status; recorded in SGK's note.
4. **`end` on a status that could not be read writes no `host`**: the writer composes from an empty
   status (01's observation 1, 04's design). The record is `lost`, so `finished`, and is judged by
   no pid; the release notes say so (§2.2).
5. **A `v0.1.0` reader of a runs root that holds a status that is not an object raises for every
   store under it.** It is `v0.1.0`'s behaviour, which 03 fixed; the release notes' §4 records it as
   a reason to move every checkout together. No issue.
6. **The board's suite sentence** (§1, "The suite is 276 … 410 after 05.") is not extended to 06
   (deviation 17); the review's records may.
7. **The reinstall rewrote the ignored `runregistrykit.egg-info/`** (`PKG-INFO` `0.2.0`) and renamed
   the editable finder in `venv/`; nothing tracked changed.

## State handed to the next prompt

- **`v0.2.0` is ready to be tagged on this commit** once CI has passed on it, pushed alone, all three
  jobs (the prompt's §7); no tag is made, nothing is pushed. The wheel from an export of this
  commit's tree is 66 257 bytes, ten entries, SHA-256 `1a169488…44c9`.
- **For 07:** the release notes (`docs/releases/v0.2.0.md`) and the adoption notes
  (`docs/adoption/v0.2.0/`) are what the verification cites; the mixed-version table and the hard-kill
  route are measured here against the tree, and 07 measures the route again against the pin
  installed from GitHub.
- The five open §3 issues are unchanged; `docs/OPEN_ISSUES.md` counts 10. The suite is 410, with one
  skip on macOS.
