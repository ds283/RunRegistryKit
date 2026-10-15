# The extraction campaign: verification

**Campaign:** [`prompts/extraction/README.md`](../prompts/extraction/README.md) ·
**Board:** [`prompts/extraction/IMPLEMENTATION_STATE.md`](../prompts/extraction/IMPLEMENTATION_STATE.md) ·
**Prompt:** [`prompts/extraction/08-verification-and-close-out.md`](../prompts/extraction/08-verification-and-close-out.md) ·
**Log:** [`prompts/extraction/logs/08-verification-and-close-out.md`](../prompts/extraction/logs/08-verification-and-close-out.md) ·
**Date:** 2026-10-15

**The package verified** is the release
[`v0.1.0`](https://github.com/ds283/RunRegistryKit/tree/v0.1.0): annotated tag object `fd5ce48`,
peeling to commit
[`9f8ebe4`](https://github.com/ds283/RunRegistryKit/commit/9f8ebe431503fb8c79ee1407cc460501f1ca2d92)
(`git rev-parse v0.1.0 v0.1.0^{}` gives `fd5ce4806a3c…` and `9f8ebe431503…`). At the commit that adds
this document, `git diff 9f8ebe4 -- runregistrykit pyproject.toml` is empty: the package and its
metadata are the tag's. Every `path:line` under `runregistrykit/` below is read at `9f8ebe4`; one in
`README.md` is read at the commit that adds this document, whose `README.md` is `aaab408`'s; one in a
client is read at that client's checklist commit.

This document is additive from the day it is committed (`CLAUDE.md`, rule 6): a later measurement is
a new subsection, and what is here stays correct for the tree it was taken on.

---

## 1. What this document is

**What the campaign set out to do.** SecondaryGWKit (SGK) built `RunRegistry/` for its long jobs;
on 2026-10-12 the user decided that it moves to a repository of its own (SGK's D1; campaign README
§0, §6.1), as the datastore layer had moved to DatastoreKit and the work queue to RayPoolKit. The
campaign was that move: SGK's three modules imported faithfully at SGK `a45aefc` (01, 02), made
generic one coupling at a time (03–05c), released once as `v0.1.0` (06), and measured against each
of the three clients in an adoption checklist (07) (campaign README §0.1, §1, §2). Two of the user's
rulings shaped the package: the fingerprint splits by layer, the client saying what goes into it,
DatastoreKit encoding and digesting it, the package deciding when and where it is taken (D3); and the
store layer requires a fingerprinter, with no degraded mode (D4).

**What it delivered**, each re-measured below:

- **One release, `v0.1.0`** (`9f8ebe4`), tagged after CI run
  [`38754093289`](https://github.com/ds283/RunRegistryKit/actions/runs/38754093289) passed all three
  jobs there (§2.2). Installed **as a client installs it**, from GitHub, at both tested ends and in
  the core-only form, it is `9f8ebe4`'s five modules byte for byte and ships no test (§5).
- **The suite at both ends**: `Ran 276 tests … OK` in `venv/` (Python 3.12.15, Ray 2.43.0,
  SQLAlchemy 2.0.39) and in a fresh high-end venv (3.13.16, 2.55.1, 2.0.46), the same 276 by module
  in both (§3).
- **The store layer end to end from the GitHub pin** (U23, U24): a self-contained script,
  [`docs/extraction/store_smoke_run.py`](extraction/store_smoke_run.py), builds a client root with
  its own registry module and fingerprinter and drives every `store` command, a fingerprinted run, a
  worktree run and two refusals: eleven steps pass at both ends, the same fingerprint digest at both,
  Ray never initialised; and it fails where it should, in three deliberate breakages (§4).
- **The checklists and E2**: `measure_client_registry.py`'s output equals each checklist's appendix
  byte for byte at its commit (§3); E2, SGK's gate on this campaign, holds: `v0.1.0` with
  [`docs/adoption/secondarygwkit.md`](adoption/secondarygwkit.md) (board §2).
- **Two issues open** at the close, both owner none and both a request to DatastoreKit (§6).

**What remains**: G2–G4, the three clients' adoptions, none made; what this campaign could not
verify (§10).

---

## 2. Reconciliation

### 2.1 Git history

`main` holds **45 commits** from `745c9d9` (the repository started) to `302faac`, the commit before
08's own (`git rev-list --count 302faac` is 45). Each is in one class, by its subject and its
content, counted by script (`git log --format=%s`, matched on the subject's form; log of 08,
Verification 9):

| Class | Commits | Count |
|---|---|---|
| The start | `745c9d9` | 1 |
| The plan | `9fe1690` | 1 |
| A prompt written, with the decisions it recorded | `ac46f1b`, `0fb6aff`, `090da27`, `2ecb99d`, `d035ffb`, `6ec0066`, `92f173c`, `4ec6406`, `dbefdb2`, `f7c1b15`, `7540efb` | 11 |
| An orchestration note | `91b7a60`, `1f9b5b0`, `f02abc7`, `9dc34a5`, `5177ffa`, `d2a3d85`, `bcc0c0a`, `bd83b3d`, `02c7ad7`, `4c01c78`, `302faac` | 11 |
| A prompt's own commit | `4e0d715`, `8155445`, `035e4b5`, `c81ad06`, `5302a6f`, `14af805`, `1120fb3`, `a7d93d5`, `9f8ebe4`, `aaab408` | 10 |
| An orchestrator's review | `bae5597`, `71f59ed`, `f9e0e60`, `8880cfa`, `dfcb884`, `c735acf`, `8766714`, `3372292`, `4ee947b`, `aaa1d6d` | 10 |
| The release record | `dca5ead` | 1 |
| | | **45** |

The prompt's §1.3 counts 43, to `aaa1d6d`; the two after it are 08's writing (`7540efb`) and 08's
orchestration note (`302faac`), both on `main` before 08's own commit. 08's commit is the 46th; the
orchestrator's review of 08 follows it and is not counted here.

| Prompt | Written | Note | Commit | Review | Suite after | Closed or opened |
|---|---|---|---|---|---|---|
| 01 | `ac46f1b` | `91b7a60` | `4e0d715` | `bae5597` | 3 | nothing |
| 02 | `0fb6aff` | `1f9b5b0` | `8155445` | `71f59ed` | 108 | opened `[02-the-ported-tests-name-sgk]`; its review opened `[02-the-sidecar-readers-guards-are-unpinned]` |
| 03 | `090da27` | `f02abc7` | `035e4b5` | `f9e0e60` | 135 | closed `[00-the-root-is-the-packages-parent]`, `[00-the-recorded-distributions-are-sgks]` |
| 04a | `2ecb99d` | `9dc34a5` | `c81ad06` | `8880cfa` | 186 | closed `[00-the-fingerprint-reads-a-clients-registry]`, `[00-the-store-layer-reads-inside-a-fingerprint]`, `[02-the-sidecar-readers-guards-are-unpinned]`; its review opened `[04a-the-loader-accepts-a-fingerprinter-class]` |
| 04b | `d035ffb` | `5177ffa` | `5302a6f` | `dfcb884` | 245 | its writing opened `[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]`; closed it and `[04a-the-loader-accepts-a-fingerprinter-class]`; narrowed `[00-a-refusal-matches-datastorekit-message-text]` |
| 05a | `6ec0066` | `d2a3d85` | `14af805` | `c735acf` | 275 | narrowed `[00-package-prose-names-sgk]`, `[02-the-ported-tests-name-sgk]` |
| 05b | `92f173c` | `bcc0c0a` | `1120fb3` | `8766714` | 276 | closed `[00-package-prose-names-sgk]` |
| 05c | `4ec6406` | `bd83b3d` | `a7d93d5` | `3372292` | 276 | closed `[02-the-ported-tests-name-sgk]`; opened `[05c-the-import-test-needs-datastorekit]` |
| 06 | `dbefdb2` | `02c7ad7` | `9f8ebe4` | `4ee947b` | 276 | closed `[05c-the-import-test-needs-datastorekit]`; its review opened `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]`; the release record `dca5ead` |
| 07 | `f7c1b15` | `4c01c78` | `aaab408` | `aaa1d6d` | 276 | closed `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]` |
| 08 | `7540efb` | `302faac` | this document's | — | 276 | nothing; closes the campaign |

The suite went 0 → 3 → 108 → 135 → 186 → 245 → 275 → 276 → 276 → 276 → 276 → 276, each count the
board's §1 and each log's own "before and after"; 08 changes no test.

### 2.2 The tag and CI

- **The tag.** `v0.1.0`, annotated, tag object `fd5ce48`, on `9f8ebe4` (`git rev-parse`, above;
  the orchestrator read the same from `origin` with `git ls-remote`, 08's brief). It was made after
  [run 38754093289](https://github.com/ds283/RunRegistryKit/actions/runs/38754093289) passed on
  `9f8ebe4` (board, 06's review, "The release").
- **CI**, read with `gh run view <id> --json` (nothing written), each `completed`/`success` in all
  three jobs, `suite (low)`, `suite (high)` and `core (no store layer)`:

  | Run | Commit |
  |---|---|
  | [38754093289](https://github.com/ds283/RunRegistryKit/actions/runs/38754093289) | `9f8ebe4` (06, the tag's) |
  | [38755672939](https://github.com/ds283/RunRegistryKit/actions/runs/38755672939) | `4ee947b` (06's review) |
  | [38768740409](https://github.com/ds283/RunRegistryKit/actions/runs/38768740409) | `dca5ead` (the release record) |
  | [38787646775](https://github.com/ds283/RunRegistryKit/actions/runs/38787646775) | `aaa1d6d` (07's review; the first run over `docs/adoption/measure_client_registry.py`) |

### 2.3 The environment of every measurement below

- macOS 27.0.1 (`arm64`), `git` 2.56.0, `uv` 0.12.20, interpreters `/opt/local/bin/python3.12`
  (3.12.15) and `/opt/local/bin/python3.13` (3.13.16).
- **`venv/`**, this repository's: Python 3.12.15, `runregistrykit` 0.1.0 editable from this checkout,
  `datastorekit` 0.4.0, Ray 2.43.0, SQLAlchemy 2.0.39, `black` 25.1.0. The suite (low end), `black`,
  `compare_with_source.py` and `measure_client_registry.py` ran here.
- **The high-end suite venv**: a fresh 3.13.16 `uv` venv with a `git clone` of this repository at
  `302faac` installed editable with the extra, `datastorekit` from `v0.4.0`, Ray 2.55.1, SQLAlchemy
  2.0.46; the suite run from the clone's root.
- **The three pin venvs** (§5): fresh `uv` venvs, `--no-cache`: low (3.12.15, Ray 2.43.0, SQLAlchemy
  2.0.39), high (3.13.16, 2.55.1, 2.0.46), core (3.12.15, the core form alone). The smoke script ran
  in these.
- `TMPDIR` named a directory in the session's scratchpad for every command that could make a
  temporary file; no Ray process was up before or after any run (`pgrep -lf
  'gcs_server|raylet|ray::|default_worker\.py'` found none, every time).

---

## 3. Each prompt's acceptance, at `v0.1.0`

| Prompt | Acceptance, in brief | What its review found | At `v0.1.0`, and how re-measured here |
|---|---|---|---|
| 01 | The three modules imported under D-name only; the check exits 0 and bites; the package imports with no client and loads nothing heavy (README §2) | Every check passed; nothing opened (board, 01's review) | **Holds.** The check at `8155445`, from a worktree of it with `venv/`'s Python: exit 0, `RESULT: OK`, its 467 lines equal to 02's log's byte for byte. `test_package_imports` 3 OK at both ends. In each pin venv `runregistrykit` imports from `site-packages` with `-I` from an empty directory, and the smoke script runs there (§4, §5) |
| 02 | 29 core and 76 shard-fixture tests ported under D-name, D-fix, D-fmt; the check exits 0 | Every check passed; one issue opened (board, 02's review) | **Holds.** The check's summary: "12 checked (4 by 01, 8 by 02): D-name 106, D-fix 5, D-fmt 12 in 3 hunks; 3 pending; 11 not imported and absent; 1 declared new". The ported modules pass at both ends (`test_run_registry` 29, `test_store_sidecar` 17, `test_store_copy_move` 27, `test_store_command_line` 2, `test_store_amend` 21, `test_store_amend_residuals` 9) |
| 03 | The client root from `runregistrykit.toml`; worktree runs under the main checkout; no config a refusal | Every check passed (board, 03's review) | **Holds.** `test_client_root` 27 OK at both ends; the smoke's step 10 (a worktree run recorded under the main checkout's `var/runs/`) and step 11 (`list` with no config exits 1, "No runregistrykit.toml") pass at both ends and in the core venv (§4) |
| 04a | The client fingerprinter named in the config; layer C deleted; the store layer refused without one (D4); the neutral store; SGK's fingerprint tests ported | Every check passed; one issue opened (board, 04a's review) | **Holds.** `test_fingerprinter` 31 and `test_store_fingerprint` 29 OK at both ends; the smoke's steps 2 and 5 take and compare a fingerprint through the client's own `DatastoreKitFingerprinter`, and step 11 shows the D4 refusal |
| 04b | SGK's retire tests ported; `store retire` loads the fingerprinter first; the loader refuses a class (U14) | Every check passed (board, 04b's review) | **Holds.** `test_store_retire` 41 and `test_store_retire_references` 10 OK at both ends; the smoke's step 9 retires a store; breakage (a) (the class named) fails `store retire` with and without `--dry-run`, every file kept (§4.3) |
| 05a | The no-client guard and its data; `slugify` and `__all__`; the licence header | Every check passed (board, 05a's review) | **Holds.** `test_package_is_generic` 22 and `test_public_names` 8 OK at both ends; the installed modules are `9f8ebe4`'s, header and `__all__` included (§5) |
| 05b | The package prose in its own terms; the citation scan widened (U17); the README's rules and public names | Every check passed (board, 05b's review) | **Holds.** The guard (in the suite) finds no package-module hit. "The rules" and "The public names" of `README.md` are unchanged from `1120fb3` (each section compared as text); each module's `__all__` in the low pin venv equals the README's list for it (20, 26, 4, 4, 1). The prose's faithfulness is read, not tested, as the review said; it is not re-read here |
| 05c | The tests' client names renamed and their prose rewritten; the known hits empty | Every check passed; one issue opened (board, 05c's review) | **Holds.** The guard's five scans find nothing (in the suite, both ends) |
| 06 | Versions declared; CI at both ends and a core job; `README.md`'s install and usage; `v0.1.0` tagged after CI | Every check passed; one README statement opened as an issue (board, 06's review) | **Holds.** The four CI runs (§2.2); the pin installs at both ends and the core form resolves with none of `datastorekit`, Ray and SQLAlchemy (§5); `./venv/bin/black --check runregistrykit docs`: 28 files unchanged (27 and the smoke script). The workflow is not re-run here: CI's own record is the measurement |
| 07 | The three checklists and their script; the README's worktree sentences (U20) | Every check passed; one stop, ruled by the user (board, 07's review) | **Holds.** `measure_client_registry.py sgk`, `cpbh` and `si`, each at its default commit (the checklist's: SGK `14bcac0`, ChamPBH `c21cdfb`, SI `5fb4a1d`, each the client's `HEAD` today), exit 0, and each output equals the checklist's appendix byte for byte (`cmp`; 399, 84 and 90 lines) |

---

## 4. The store layer end to end (U23)

### 4.1 The script

[`docs/extraction/store_smoke_run.py`](extraction/store_smoke_run.py) imports the standard library and
`runregistrykit`, and nothing of `runregistrykit.tests`. It makes a directory with `tempfile` and in
it a client root, a git repository with one commit holding `runregistrykit.toml`
(`distributions = ["datastorekit"]`, `[stores] fingerprinter = "smoke_registry:FINGERPRINTER"`),
`.gitignore` (`var/`), `job.py`, and `smoke_registry.py`, the client's registry and fingerprinter
module, written from a string the script holds: four factories on public `datastorekit` names (the
contract's version and tag tables, a replicated class `Grid` and a sharded class `Point` whose parent
is a `Grid`), a writer of a closed two-shard store, and `FINGERPRINTER =
DatastoreKitFingerprinter(FACTORIES, 1)`. It runs each command as `sys.executable -m runregistrykit …`
in the client root, prints `PASS` or `FAIL` per step with the commands, their exit codes and the lines
that show the outcome, and exits 0, 1 or 2. Its docstring gives the eleven steps.

Run, from this repository's root, in each pin venv (§5):

```bash
TMPDIR=<scratch>/tmp/smoke-low  <scratch>/pin-low/bin/python  docs/extraction/store_smoke_run.py
TMPDIR=<scratch>/tmp/smoke-high <scratch>/pin-high/bin/python docs/extraction/store_smoke_run.py
TMPDIR=<scratch>/tmp/smoke-core <scratch>/pin-core/bin/python docs/extraction/store_smoke_run.py
```

### 4.2 At both ends

**Exit 0 at both ends**, `RESULT: OK (11 steps passed)`; 8.4 s at the low end and 9.5 s at the high
end (the script's own clock; `time -p` real 8.64 s and 9.88 s). No Ray process before or after
either run; in each the script's last check found `ray` imported (by `datastorekit`) and **not
initialised**. The low end's output, whole, the scratchpad's path written `<scratch>`:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.1.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
directory       $SMOKE = <scratch>/tmp/smoke-low/store-smoke-pl6nvykz

PASS step 1: a store written by the client's module, and `store create --purpose`
  written: smoke-store-shard0000.sqlite, smoke-store-shard0001.sqlite, smoke-store.sqlite
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id 44b284c7596e4e97bd2db11f77ba19b3
PASS step 2: a run that takes a fingerprint of its results store
  begin(): smoke-02-fingerprinted-20261015T201343
  known(): ['u1']
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > manifest packages: ['datastorekit', 'runregistrykit']
PASS step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261015T201343  done            1/1       1s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished.
PASS step 4: `store show`: a registry sidecar, no problems, the run naming the store
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > kind:     registry
    > problems: none
    > smoke-02-fingerprinted-20261015T201343  done      finished  by results and results_store_id
PASS step 5: `store fingerprint`: the recorded fingerprint matched by a fresh one
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > digest:   e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > format:   1
    > recorded: matches the fingerprint taken 2026-10-15T20:13:43+01:00 by run smoke-02-fingerprinted-20261015T201343, at b17eed8dcbf66e4c067591d7b1d7bc9c56bdca84
PASS step 6: `store copy --purpose` of the store, and `store move` of the copy
  $ python -m runregistrykit store copy $SMOKE/client/var/datastores/smoke-store.sqlite $SMOKE/client/var/datastores/smoke-copy.sqlite --purpose a smoke copy   (in client/)
    exit 0
    > >> copy: $SMOKE/client/var/datastores/smoke-copy.manifest.json
  $ python -m runregistrykit store move $SMOKE/client/var/datastores/smoke-copy.sqlite $SMOKE/client/var/datastores/smoke-moved.sqlite   (in client/)
    exit 0
    > >> move: $SMOKE/client/var/datastores/smoke-moved.manifest.json
  moved: smoke-moved-shard0000.sqlite, smoke-moved-shard0001.sqlite, smoke-moved.sqlite
    > history: ['create', 'copy', 'move']
PASS step 7: `store amend --field x_note --remove` of a field written by hand
  wrote x_note into the moved copy's sidecar by hand
  $ python -m runregistrykit store amend $SMOKE/client/var/datastores/smoke-moved.sqlite --field x_note --remove --reason the smoke run removes a field it wrote   (in client/)
    exit 0
    > field:    x_note
    > before:   "written by hand"
    > after:    null
    > >> amended: $SMOKE/client/var/datastores/smoke-moved.manifest.json
PASS step 8: `store adopt` of a store whose sidecar is a legacy object
  wrote the legacy sidecar: {"datastore": "smoke-legacy.sqlite", "purpose": "a legacy smoke store"}
  $ python -m runregistrykit store adopt $SMOKE/client/var/datastores/smoke-legacy.sqlite   (in client/)
    exit 0
    > >> adopt: $SMOKE/client/var/datastores/smoke-legacy.manifest.json
    > sidecar_format 1, purpose 'a legacy smoke store', history ['adopt']
PASS step 9: `store retire --dry-run`, `store retire` and `store show` of the moved copy
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy --dry-run   (in client/)
    exit 0
    > dry run:  nothing was written or deleted
    > files to be deleted:
    > var/datastores/smoke-moved-shard0000.sqlite
    > var/datastores/smoke-moved-shard0001.sqlite
    > var/datastores/smoke-moved.sqlite
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy   (in client/)
    exit 0
    > matched: a fresh read-only fingerprint matched the recorded one, digest e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > files deleted:
    > var/datastores/smoke-moved-shard0000.sqlite
    > var/datastores/smoke-moved-shard0001.sqlite
    > var/datastores/smoke-moved.sqlite
    > >> retired: $SMOKE/client/var/datastores/smoke-moved.manifest.json
  left: no store file
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-moved.sqlite   (in client/)
    exit 0
    > state:     retired
    > completed: 2026-10-15T20:13:50+01:00
    > problems: none
PASS step 10: a run begun in a linked worktree, recorded under the main checkout
  git worktree add --detach worktree
  begin(): smoke-10-worktree-20261015T201350
    > run directory: $SMOKE/client/var/runs/smoke-10-worktree-20261015T201350
    > manifest script: $SMOKE/worktree/job.py
PASS step 11: the refusals: no fingerprinter named, and no config at all
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in no-fingerprinter/)
    exit 1
    > !! $SMOKE/no-fingerprinter/runregistrykit.toml names no fingerprinter, and the store layer requires one. Add [stores] with fingerprinter = "module:attribute", naming the client's Fingerprinter (runregistrykit.fingerprint), such as a DatastoreKitFingerprinter of its registry and its format number
  $ python -m runregistrykit list   (in elsewhere/)
    exit 1
    > !! No runregistrykit.toml in $SMOKE/elsewhere or any directory above it. Create one at the client's root; an empty file takes the defaults (runs_root = "var/runs", stores_root = "var/datastores", distributions = [])

ray: imported, initialised: False
digest (status.json): e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
digest (store fingerprint): e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
time: 8.4 s
left in place: <scratch>/tmp/smoke-low/store-smoke-pl6nvykz
RESULT: OK (11 steps passed)
```

**The high end's output** differs from it, by `diff`, only in the versions and paths of its first
seven lines (Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46, the `pin-high` venv), the new
`store_id`, the run ids and their timestamps, the commit of the client root (made fresh each run),
the retirement's time, the time (9.5 s) and the directory left in place. **The digest is the same at
both ends**: `e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069`, printed and not
asserted. It is not the prompt's `c62012bd…`: that was the digest of the tests' neutral store, which
the planner's probe copied into its client root (prompt §1.1); the script writes its own, smaller
registry and store, so its digest is its own. What matters, and holds, is that the two ends agree.

### 4.3 The breakage

Each is exactly what was run: (a) and (b) as diffs to the committed script, applied with `git apply`
in a scratch clone, run there in the low pin venv and reversed; (c) the committed script in the core
pin venv. The diffs are in 08's log, "The deliberate-breakage record".

- **(a) The config names the class.** `fingerprinter = "smoke_registry:DatastoreKitFingerprinter"`.
  Exit 1, `RESULT: FAIL (2, 5, 9)`. Step 2: the run is still `done`, exit code 0, and `status.json`
  carries `fingerprint_error`, the loader's `ConfigError` ("… is the class DatastoreKitFingerprinter,
  not an instance of it: name an instance …"), with no `fingerprint_sidecar`. Step 5: `store
  fingerprint` exits 1 with the same refusal. Step 9: `store retire --dry-run` exits 1 with it; run
  again in the left client root without `--dry-run`, `store retire` exits 1 with it, and the moved
  store's three files and its sidecar are all still there (U14). Steps 1, 3, 4, 6, 7 and 8, which
  need only that a fingerprinter is named (`create`, `show`, `copy`, `move`, `amend`, `adopt`), pass,
  as `README.md:143-145` says (the D4 check reads the config only) and `README.md:161` ("The config
  names an instance, not a class").
- **(b) One row changed after the fingerprint.** At the end of step 2, `UPDATE Point SET x = x + 0.25
  WHERE serial = 1` on shard 0 of the store, with `sqlite3`; at the start of step 5, `store retire`
  of that store. Exit 1, `RESULT: FAIL (5, 9)`. `store retire` of the changed store exits 1: "Cannot
  retire …: its content does not match the fingerprint its sidecar records, taken …: 1 difference(s):
  Point: tag set [] differs: 3 recorded, 3 now. Nothing was written or deleted", its three files
  kept. `store fingerprint` then exits 1 naming the class that differs (`!! Point: tag set []
  differs: 3 recorded, 3 now`). The copy, made by step 6 after the change, carries the recorded
  fingerprint verbatim (`copy_store` keeps every other field, `runregistrykit/stores.py:1142-1144`),
  so step 9's `store retire --dry-run` of the moved copy is refused the same way; run again without
  `--dry-run`, it is refused and its files kept. That is what `README.md:181-183` says: `retire`
  "refuses … one whose recorded fingerprint does not match its content".
- **(c) The core-only venv.** No `datastorekit`, Ray or SQLAlchemy installed. Exit 1, `RESULT: FAIL
  (1, 2, 4, 5, 6, 7, 8, 9)` in 1.1 s; `ray` never imported; no exception escaped a step. Step by
  step:

  | Step | Needs | Verdict, and what it saw |
  |---|---|---|
  | 1 | a store (the client's writer) | FAIL: `ModuleNotFoundError: No module named 'sqlalchemy'`, caught by the step |
  | 2 | a fingerprinter | FAIL: `begin()`, `record()`, `known()` and `finish()` ran (the results store does not exist, and `begin` does not refuse a primary with no sidecar); `status.json` `done` with `fingerprint_error`, the loader's `ConfigError` naming the module that could not be imported |
  | 3 | neither (the run of step 2) | PASS: `list` shows one run, finished |
  | 4 | a store | FAIL: `store show` exits 0 with `kind: absent` |
  | 5 | a store and a fingerprinter | FAIL: `store fingerprint` exits 1, the loader's refusal |
  | 6 | a store | FAIL: `store copy` exits 1, "is not a problem-free registry sidecar (there is none)" |
  | 7 | a store (step 6's) | FAIL: `FileNotFoundError` on the moved copy's sidecar, caught |
  | 8 | a store | FAIL: `ModuleNotFoundError: No module named 'sqlalchemy'`, caught |
  | 9 | a store | FAIL: `FileNotFoundError` on `var/datastores`, caught |
  | 10 | neither | PASS: the worktree run under the main checkout's `var/runs/` |
  | 11 | neither | PASS: both refusals, exit 1 each |

  The prompt's §4.5 names steps 10 and 11's `list` as the ones that pass; step 3 and the whole of
  step 11 pass as well, and need neither a store nor a fingerprinter (08's brief, correction 5).

The script also exits **2** when it cannot start: with `PATH=/nonexistent` ("CANNOT START: no git on
PATH"), and under an interpreter without the package (`/opt/local/bin/python3.12 -I`: "CANNOT START:
runregistrykit is not importable (No module named 'runregistrykit')").

---

## 5. The release from GitHub (U24)

**The installs**, each into a fresh venv made with `uv venv --python <interpreter>`, `TMPDIR` in the
scratchpad, so that the tag was fetched from GitHub and nothing was reused from `uv`'s cache:

```bash
uv pip install --no-cache --python <scratch>/pin-low/bin/python \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.43.0' 'sqlalchemy==2.0.39'
uv pip install --no-cache --python <scratch>/pin-high/bin/python \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
uv pip install --no-cache --python <scratch>/pin-core/bin/python \
  'runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.1.0'
```

| Venv | Python | Resolved | `runregistrykit` | `datastorekit` | Ray / SQLAlchemy |
|---|---|---|---|---|---|
| low | 3.12.15 | 23 packages | 0.1.0, from `9f8ebe431503…` | 0.4.0, from `c8570e849334…` | 2.43.0 / 2.0.39 |
| high | 3.13.16 | 21 packages | 0.1.0, from `9f8ebe431503…` | 0.4.0, from `c8570e849334…` | 2.55.1 / 2.0.46 |
| core | 3.12.15 | 1 package | 0.1.0, from `9f8ebe431503…` | not installed | not installed |

`uv` reported each tag's commit as it fetched it (`Updated https://github.com/ds283/RunRegistryKit
(9f8ebe431503fb8c79ee1407cc460501f1ca2d92)`; DatastoreKit `c8570e849334d09085bbd84876095fc9e22bd005`,
its [`v0.4.0`](https://github.com/ds283/DatastoreKit/tree/v0.4.0)).

**What was installed**, read in each venv by a scratch script run with `-I` from an empty directory:

- `importlib.metadata`: `runregistrykit` 0.1.0, `runregistrykit.__file__` under the venv's
  `site-packages`, `requires` `['datastorekit>=0.4.0; extra == "stores"']`; in the core venv
  `find_spec` finds none of `datastorekit`, `ray` and `sqlalchemy`.
- `direct_url.json`, the same in all three: `{"url": "https://github.com/ds283/RunRegistryKit",
  "vcs_info": {"commit_id": "9f8ebe431503fb8c79ee1407cc460501f1ca2d92", "requested_revision":
  "v0.1.0", "vcs": "git"}}`.
- **The five modules equal `9f8ebe4`'s byte for byte** in all three venvs (`git show
  9f8ebe4:runregistrykit/<module> | cmp - <site-packages>/runregistrykit/<module>`, each silent):
  `__init__.py`, `__main__.py`, `client.py`, `fingerprint.py`, `stores.py`.
- **No tests.** The installed `RECORD` has 14 entries, the five modules and nine under
  `runregistrykit-0.1.0.dist-info/` (the wheel's five, and `INSTALLER`, `REQUESTED`,
  `direct_url.json` and `uv_build.json`, which the installer adds); none names `tests`; `import
  runregistrykit.tests` raises `ModuleNotFoundError` (U19).

**The offline rebuild**, for the record: `git archive v0.1.0 | tar -x -C <scratch>/export-v010`, then
`uv build --wheel --offline --out-dir <scratch>/dist-offline <scratch>/export-v010`: exit 0, no
"absent from" in the build log, `runregistrykit-0.1.0-py3-none-any.whl`, **54,940 bytes, 10
entries**, as 06's log records (06's log, "3. The release check"); the five modules in it equal
`9f8ebe4`'s, `METADATA` as 06's (`Version: 0.1.0`, `Requires-Python: >=3.12`, `Provides-Extra:
stores`, `Requires-Dist: datastorekit>=0.4.0; extra == "stores"`). **Its SHA-256 is
`81a0ebb6b442917803df95413459cb6deaeea43c4e610051de38127d474339dd`**, neither 06's (`9c01e7c9…`) nor
the planner's (`0a69e125…`): `unzip -l` shows the five modules with the tag commit's time (14:31
UTC, which `git archive` gives its files) and the five `dist-info` entries with the build's (19:00
UTC on 2026-10-15), so every rebuild differs in its hash. A wheel is compared by its entries and their content, never by its hash.

---

## 6. Issues

Thirteen were opened on the board: seven at planning, from SGK's code at `a45aefc`; one by 02, one
by 02's review, one by 04a's review, one at 04b's writing, one by 05c and one by 06's review. Eleven
are resolved (board §4) and two are open (board §3); the index counts 2.

**Resolved**, each with the prompt and commit that closed it and what guards it:

| Issue | Opened | Closed | Guarded by |
|---|---|---|---|
| `[00-the-root-is-the-packages-parent]` | planning | 03, `035e4b5` | `test_client_root`'s `TestWalk`, `TestWorktree`, `TestStoresUnderTheRoot`, `TestCommandLine` |
| `[00-the-recorded-distributions-are-sgks]` | planning | 03, `035e4b5` | `test_run_registry.TestManifest.test_manifest_records_the_installed_packages`, `TestPackageProvenance.test_the_recorded_names_are_the_registry_and_the_configs`, `test_client_root.TestRecordedDistributions` |
| `[00-the-fingerprint-reads-a-clients-registry]` | planning | 04a, `c81ad06` | `test_fingerprinter`'s `TestProtocolAndLoader`, `TestTheStoreLayerRequiresOne`, `TestPrecedence`, `TestThroughTheFingerprinter`; the 29 of `test_store_fingerprint` |
| `[00-the-store-layer-reads-inside-a-fingerprint]` | planning | 04a, `c81ad06` | `test_fingerprinter.TestOpacity`; `TestThroughTheFingerprinter.test_what_the_client_fingerprinter_takes_is_recorded` and `test_a_recorded_fingerprint_without_encoding_format_is_not_compared` |
| `[02-the-sidecar-readers-guards-are-unpinned]` | 02's review, `71f59ed` | 04a, `c81ad06` | `test_fingerprinter.TestSidecarGuards` (two tests) |
| `[04a-the-loader-accepts-a-fingerprinter-class]` | 04a's review, `8880cfa` | 04b, `5302a6f` | `test_fingerprinter.TestProtocolAndLoader.test_a_class_is_refused_and_an_instance_of_it_loads`; the class cases of `TestRetireLoadsTheFingerprinterFirst` |
| `[04b-retire-without-fingerprint-deletes-on-a-broken-fingerprinter]` | 04b's writing, `d035ffb` | 04b, `5302a6f` | `test_fingerprinter.TestRetireLoadsTheFingerprinterFirst`, `TestRetirePrecedence` |
| `[00-package-prose-names-sgk]` | planning | 05b, `1120fb3` | the guard, `test_package_is_generic` (no package-module hit in any scan) |
| `[02-the-ported-tests-name-sgk]` | 02, `8155445` | 05c, `a7d93d5` | the guard (no hit in any file) |
| `[05c-the-import-test-needs-datastorekit]` | 05c, `a7d93d5` | 06, `9f8ebe4` (U18) | CI's `core (no store layer)` job, and `test_package_imports` in the two `suite` jobs |
| `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]` | 06's review, `4ee947b` | 07, `aaab408` (U20) | the document: `README.md`'s "Using it" (`README.md:93-100`, `:154-156`) |

**Open at the close**, both owner none, both requests to DatastoreKit (campaign README §8):

- **`[00-the-shard-fixtures-reach-into-shardedpool]`.** The carried shard fixture builds a pool with
  `object.__new__` and sets ten private `ShardedPool` attributes
  (`runregistrykit/tests/shard_store_fixtures.py:30-43`), and `store_fixtures.assertOpens`
  (`runregistrykit/tests/store_fixtures.py:160-167`) uses two more. It affects only this
  repository's tests, never a client; `datastorekit` is pinned to its tag in CI, so a change there
  is seen when the pin moves. It stays open because its remedy, a public way to write and reopen a
  small store, is DatastoreKit's to provide.
- **`[00-a-refusal-matches-datastorekit-message-text]`.** `retire_store` recognises an unreadable
  shards table by matching `_SHARDS_TABLE_UNREADABLE` (`runregistrykit/stores.py:1409-1410`, used at
  `:1677` and `:1727`) in DatastoreKit's message. A test reaches the match at both tested ends
  (`test_store_retire.TestWithoutFingerprint.test_an_unreadable_shards_table`,
  `runregistrykit/tests/test_store_retire.py:802`), so a rewording is seen; it is not prevented. It
  stays open because its remedy, a typed exception, is DatastoreKit's.

---

## 7. Decisions

Thirty-four, each taken as the record says. "Applied" is the commit that put it into effect.

**Made by the user, carried in from SGK** (campaign README §6.1; SGK, 2026-10-12):

| | Decided | Applied |
|---|---|---|
| D1 | a repository of its own | `745c9d9` |
| D3 | the fingerprint split by layer; the package takes a client's fingerprinter, the result opaque but for named fields | 04a, `c81ad06` |
| D4 | the store layer requires a fingerprinter | 04a, `c81ad06` (`require_fingerprinter`) |
| Q1 | names: `RunRegistryKit`, `runregistrykit`, `python -m runregistrykit` | 01, `4e0d715` |
| Q2 | a client config file at the client's root, read with `tomllib` | 03, `035e4b5` |
| Q3 | a worktree run recorded in the main checkout, with its own tree's provenance | 03, `035e4b5` |
| Q4 | one distribution, the store layer the extra `[stores]` | 01, `4e0d715`; its floor 06, `9f8ebe4` |
| Q5 | SGK builds a format guard; the checklists offer the pattern | 07, `aaab408` (the recipe, U22) |
| Q7 | no manifest format field during the extraction | not applicable (no field added; README §8) |

**Put to the user by this campaign** (README §6.1 for U1, §6.2 for the rest), each taken as
recommended:

| | Decided | Taken, for | Recorded | Applied |
|---|---|---|---|---|
| U1 | public `ds283/RunRegistryKit`, Apache 2.0 | 2026-10-14, set-up | `9fe1690` | `745c9d9` |
| U2 | the import faithful, only the name changed | 2026-10-14, 01 | `ac46f1b` | `4e0d715` |
| U3 | one release, `v0.1.0`, at 06; 01 sets `0.1.0.dev0` | 2026-10-14, 01 | `ac46f1b` | `4e0d715`, `9f8ebe4` |
| U4 | the shard fixtures carried as they are | 2026-10-14, 02 | `0fb6aff` | `8155445` |
| U5 | `runregistrykit.toml` and the walk; read at writing with the override spelled `client_root=` | 2026-10-14, 03 | `090da27` | `035e4b5` |
| U6 | a protocol and a shipped `DatastoreKitFingerprinter` (re-recommended at 04's writing) | 2026-10-14, 04 | `2ecb99d` | `c81ad06` |
| U7 | what is read of a fingerprint; its named exception to rule 9 | 2026-10-14, 04 | `2ecb99d` | `c81ad06` |
| U8 | the neutral store, public names only | 2026-10-14, 04 | `2ecb99d` | `c81ad06` |
| U9 | `runregistrykit` always in `packages` | 2026-10-14, 03 | `090da27` | `035e4b5` |
| U10 | the guard's measured vocabulary and import rule | 2026-10-15, 05 | `6ec0066` | `14af805` |
| U11 | public names before the release; amended at 05a's dispatch to `slugify` | 2026-10-15, 05 | `6ec0066`; the amendment `d2a3d85` | `14af805`, `1120fb3` |
| U12 | the licence header | 2026-10-15, 05 | `6ec0066` | `14af805` |
| U13 | Python ≥3.12, `datastorekit>=0.4.0`, two ends and a core job | 2026-10-15, 06 | `dbefdb2` | `9f8ebe4` |
| U14 | 04b loads the fingerprinter before a first retirement; the loader refuses a class | 2026-10-15, 04b | `d035ffb` | `5302a6f` |
| U15 | 05 split in three | 2026-10-15, 05 | `6ec0066` | `14af805`, `1120fb3`, `a7d93d5` |
| U16 | the guard scans the tests; their names renamed | 2026-10-15, 05 | `6ec0066` | `14af805`, `a7d93d5` |
| U17 | the citation scan widened | 2026-10-15, 05b | `92f173c` | `1120fb3` |
| U18 | the core job and the import test | 2026-10-15, 06 | `dbefdb2` | `9f8ebe4` |
| U19 | the tests out of the wheel | 2026-10-15, 06 | `dbefdb2` | `9f8ebe4` |
| U20 | 07 corrects the README's worktree sentences | 2026-10-15, 07 | `f7c1b15` | `aaab408` |
| U21 | no test support shipped; SGK keeps its helpers | 2026-10-15, 07 | `f7c1b15` | `aaab408` (SGK's checklist) |
| U22 | the Q5 recipe, with a sketch proved here | 2026-10-15, 07 | `f7c1b15` | `aaab408` |
| U23 | a self-contained smoke script | 2026-10-15, 08 | `7540efb` | this document's commit |
| U24 | the smoke against the pin from GitHub | 2026-10-15, 08 | `7540efb` | this document's commit (§5) |

**One ruling at a stop.** 07's agent stopped on six SGK `fingerprint_of` calls that do not bind
against DatastoreKit's signature. Ruled by the user, 2026-10-15: a call whose only binding failure is
the missing `fingerprint_format` is the move's documented effect, not a stop; any other binding
failure is still one. Applied in 07's commit, `aaab408` (the script's `MISSING_FORMAT`, SGK's
checklist items 4 and 7); recorded on the board in `aaa1d6d` (07's review, "The stop").

---

## 8. Deviations across the campaign

Every log classifies its deviations (`CLAUDE.md`, rule 2). The entries were counted from each log's
"Deviations from the prompt" section: a top-level numbered item is one entry, and the labels it
carries were read in it (a scratch script joined each entry's lines, so that a label broken across a
line is found, and every entry was then read; 08's log, Verification 9). An entry that carries two
labels is counted under each; an entry that carries none of the three is counted as *unlabelled*.

| Log | Entries | STRUCTURALLY REQUIRED | IMPLEMENTATION CHOICE | UNINTENDED DRIFT | Unlabelled |
|---|---|---|---|---|---|
| 01 | 13 | 1 | 11 | 1 | 0 |
| 02 | 10 | 2 | 8 | 0 | 0 |
| 03 | 21 | 8 | 13 | 0 | 0 |
| 04a | 22 | 6 | 17 | 0 | 0 |
| 04b | 17 | 5 | 9 | 0 | 3 |
| 05a | 20 | 3 | 11 | 0 | 6 |
| 05b | 17 | 7 | 10 | 0 | 0 |
| 05c | 15 | 6 | 9 | 0 | 1 |
| 06 | 17 | 10 | 7 | 0 | 0 |
| 07 | 25 | 13 | 11 | 2 | 0 |
| **All** | **177** | **61** | **106** | **3** | **10** |

Three entries carry two labels (04a 14, 05c 1, 07 6), so the class columns sum to 180. The ten
unlabelled entries say **"As found"** (04b 4, 7, 9; 05a 7, 8, 9, 10, 11, 20) or nothing (05c 15, a
count recorded "so that the count is not read as a miss"); each is a brief's correction found as the
brief said, and each review accepted it.

**Where this differs from the board.** The board's review of 04a says "22 deviations, each
classified (7 STRUCTURALLY REQUIRED, 15 IMPLEMENTATION CHOICE)"; read entry by entry, 04a's log
labels 6 entries STRUCTURALLY REQUIRED (1, 2, 3, 7, 10, 14) and 17 IMPLEMENTATION CHOICE, entry 14
both. The log is the record; this count is the log's. The other reviews' counts agree with this
table where they give one (02: 2 / 8 / 0; 03: 8 / 13; 04b: 5 / 9 / 3 as found; 07: 25 entries, two
UNINTENDED DRIFT). The prompt's figures in §1.3 are counts of the label **words**, not entries
(`grep -o` misses a label broken across lines, as in 02's entry 6 and 03's entries 9, 12 and 19).

**Every UNINTENDED DRIFT entry:**

- 01, deviation 13: RayPoolKit's `pyproject.toml` read, beyond the two files the brief allowed;
  read only, nothing copied.
- 07, deviation 23: `git -C <client> worktree list`, read-only, run once on each client; nothing
  changed (07's review, check 2).
- 07, deviation 24: one `tempfile` directory under the system temporary directory, and one stray
  `/tmp/x`, each removed at once.

08's own log, written with this document, is not in the table: it classifies 22 entries (7
STRUCTURALLY REQUIRED, 13 IMPLEMENTATION CHOICE, 2 UNINTENDED DRIFT). Its two UNINTENDED DRIFT
entries: a stray `VIRTUAL_ENV=` prefix on one install command, which changed nothing (deviation 20);
and `git -C <client> worktree list`, read-only, run on the clients at the start and the end, as
07's deviation 23 was, changing nothing (deviation 22).

**Every STRUCTURALLY REQUIRED entry that changed what a prompt delivered:**

- 03, 2: one docstring line of `retire_store` changed for the prompt's grep.
- 03, 3: `stores.py:1663` (at the time), a call site the prompt's list omitted, threaded too.
- 03, 5: the tests given the shapes four mutations needed.
- 03, 7: `CLAUDE.md`'s Tests bullet: exactly one test reads this checkout's commit.
- 04a, 2: two 03 tests changed (`test_the_fingerprinter_is_kept_and_another_stores_key_refused`,
  renamed; a tombstone test's config).
- 04a, 3: `fingerprint_store`'s `taken` built before the store is read, since the protocol hands it
  to `take`.
- 04a, 14: `describe` returns lines, the protocol's shape.
- 04b, 11: `black` reflowed two lines D-name lengthened, besides R-root's.
- 05a, 2: the public name `slugify`, not the prompt's `slug` (the user's ruling, U11).
- 05c, 1: two more renames (`a3` in two test method names).
- 05c, 2: `ported.QSI` and `ported.TKN` renamed as attributes too.
- 05c, 3: `FORBIDDEN` read from the guard, bringing `datastorekit` into the import test (an issue,
  closed by 06).
- 06, 1: every workflow step under `shell: bash` (`-eo pipefail`).
- 07, 3: the script binds only calls whose callee resolves to the registry.
- 07, 6 and 19: the script reports `Parent(..., types=...)` calls, and binds the staying tests' calls.
- 07, 12 and 13: the stop and its ruling; `TestGolden`'s base walked.

---

## 9. Observations not acted on

Fifty-seven, each log's section of that name item by item (01 5, 02 6, 03 7, 04a 7, 04b 5, 05a 5,
05b 6, 05c 4, 06 5, 07 7). The disposition at `v0.1.0` was decided from the later logs, the board,
the checklists and the code at `9f8ebe4`; nothing was changed to decide it.

| Log | Observation | At `v0.1.0` |
|---|---|---|
| 01 | A deletion beside a D-name line hides that line's class in the check's report | still an observation (the check, retired at 03, describes `8155445`) |
| 01 | The check's declared-file walk covers `.py` files only | still an observation of the retired check |
| 01 | `stores.py`'s "(prompt 01's log)" cites an SGK campaign's prompt | addressed by 05b (`1120fb3`) |
| 01 | `pip freeze` records the editable install at the `HEAD` of install time | still an observation (a development install; a client pins the tag) |
| 01 | The editable install creates `runregistrykit.egg-info/`, gitignored | still an observation (true; ignored) |
| 02 | `DEFAULT_STALE_AFTER` changed passes the suite | still an observation (no test names it at `9f8ebe4`) |
| 02 | Two sidecar-reader mutations pass the suite | opened as `[02-the-sidecar-readers-guards-are-unpinned]` (02's review); closed by 04a |
| 02 | `test_package_imports.py` names `StoreFixtures` and `RunRegistry` | addressed by 05c (`FORBIDDEN` read from the guard) |
| 02 | `test_store_copy_move.py`'s lines are no longer SGK's from `:73` | no longer the point: from 03 no package line is SGK's (board §3's preamble) |
| 02 | `pip freeze` and the editable install (01's) | still an observation |
| 02 | Another session's test run on the machine; no Ray started | still an observation (a fact of 02's run) |
| 03 | `finish(…, fingerprint=True)` takes `taken`'s provenance from the working directory at finish | still an observation (`runregistrykit/stores.py:1352`, `git_provenance(os.getcwd())`) |
| 03 | `test_store_command_line.py`'s `import runregistrykit` unused | still an observation (`runregistrykit/tests/test_store_command_line.py:15`) |
| 03 | `PROVENANCE.md`'s "Re-running the check" began "From the repository root" | addressed by 03's review (`f9e0e60`) |
| 03 | The package's prose about the old root | addressed by 05b (`1120fb3`) |
| 03 | The package's `git` inherits `GIT_DIR` and the like | still an observation (by design; no test covers it) |
| 03 | The retire and fingerprint paths reached by no 03 test | addressed by 04a and 04b's ported tests |
| 03 | A config that is a symbolic link to a file counts as a file | still an observation |
| 04a | `test_store_fingerprint.py`'s `import runregistrykit` unused | still an observation (`runregistrykit/tests/test_store_fingerprint.py:29`) |
| 04a | The ported module's docstring named `stores.fingerprint_of`; its list skipped item 4 | addressed by 05c (`a7d93d5`; the list made bullets) |
| 04a | `retire_store`'s and `amend_sidecar`'s docstrings and the D4 `ConfigError` | addressed by 05b (correction 3) |
| 04a | `load_fingerprinter` leaves each client root on `sys.path` | still an observation (the prompt's rule; `runregistrykit/fingerprint.py:192-193`) |
| 04a | The protocol check does not check the methods' signatures | still an observation; a class is refused since 04b |
| 04a | `store fingerprint --listing`: `write_listing` outside the CLI's `try` | still an observation (`runregistrykit/__main__.py:338`) |
| 04a | The neutral store's primary is not one the constructor reopens | still an observation (the carried fixture serves; `[00-the-shard-fixtures-reach-into-shardedpool]`) |
| 04b | `load_fingerprinter`'s docstring did not name the class refusal | addressed by 05b (correction 4) |
| 04b | The loader's `ConfigError` does not end "Nothing was written or deleted" | addressed by 05b (the docstrings made exact) |
| 04b | With a class named, `finish(fingerprint=True)` records the loader's `ConfigError` (by reading) | measured by 08's breakage (a), step 2 (§4.3) |
| 04b | The ported modules carry SGK's prose | addressed by 05c |
| 04b | The suite takes about 90 s | still an observation (86.6 s and 94.9 s here) |
| 05a | A code-name hit the trial did not list | addressed by 05c (renamed) |
| 05a | A repeated word on one line counts once | still an observation (the guard's rule, as DatastoreKit's) |
| 05a | The known-hits writer is outside the repository | addressed: 05b and 05c used it as 05a's review read it |
| 05a | `__all__` is read by the string scan | still an observation |
| 05a | The module docstrings' prose hits unchanged | addressed by 05b |
| 05b | `known_hits.json`'s `owners` string stale | addressed by 05c |
| 05b | `README.md`'s "Status" stale | addressed by 06 (`9f8ebe4`) |
| 05b | `PROVENANCE.md`'s earlier text says the prose "still cites" SGK | still an observation (below) |
| 05b | The widened scan finds this campaign's own decision ids in the tests | addressed by 05c |
| 05b | A hit is a (line, word) pair | still an observation (as 05a's) |
| 05b | The new test asserts the message's text in full | still an observation (by design) |
| 05c | The import test no longer imports without `datastorekit` | opened as `[05c-the-import-test-needs-datastorekit]`; closed by 06 (U18) |
| 05c | The brief's id count was nine; it is eight | no action (a count) |
| 05c | `PROVENANCE.md`'s preamble, "until prompt 05 rewrites them" | still an observation (below) |
| 05c | `known_hits.json` is a list of empty lists, its mechanism kept | still an observation (by design) |
| 06 | `test_fingerprinter` fails to import in the core venv on `sqlalchemy` | still an observation (the core job names its two modules) |
| 06 | `PROVENANCE.md`'s preamble (05c's observation) | still an observation (below) |
| 06 | `CLAUDE.md`'s "Supported versions will be stated" is now past | still an observation (`CLAUDE.md` is the user's) |
| 06 | The workflow validated as YAML only | addressed: CI ran it on GitHub, run 38754093289 and three more passed (§2.2) |
| 06 | `pip`'s ephemeral wheel under the system temporary directory | still an observation (a fact of 06's run) |
| 07 | SGK's two staying tests patch a deleted `DEFAULT_ROOT` | handed to SGK's checklist, item 7 |
| 07 | An SGK test asserts the spelling `"RunRegistry.begin"` | handed to SGK's checklist, item 7 |
| 07 | SGK's golden fingerprint lacks `encoding_format` | handed to SGK's checklist, item 7 |
| 07 | SGK's sidecars counted 14 by SGK and 18 by this campaign's README | still an observation (SGK's to measure) |
| 07 | `PROVENANCE.md`'s preamble | still an observation (below) |
| 07 | SGK's stage tracker once took a printed command for a stage | still an observation (SGK's tracker) |
| 07 | The script names SGK's frozen `a45aefc` | still an observation (by design; it reads the signatures before the move) |

Of the 57: 17 addressed (by a prompt, a review or CI), 2 opened as issues and since closed, 3 handed
to SGK's checklist, 1 measured here, 1 needing no action, 1 no longer the point, and 32 still
observations.

**`PROVENANCE.md`'s preamble** (`PROVENANCE.md:17-21`) says the package's docstrings and comments
"still cite" SGK "until prompt 05 rewrites them". 05c, 06 and 07 each left it for 08. 08 may not
change `PROVENANCE.md` (prompt §7), so it stays as written: true of the tree it was written on
(`4e0d715`), and corrected by its own later sections ("Since the import", 05b's and 05c's), as an
additive document is (05b's log, observation 3). It is not opened as an issue; the orchestrator may
put it to the user.

---

## 10. Known gaps

- **G2–G4 have not held.** No client has adopted `v0.1.0`: SGK in its `runregistry-extraction`
  05–08 (G2), ChamPBH in a campaign of its own (G3), StochasticInstantons after its
  `dk-and-rpk-migration` (G4) (README §7). The campaign closes without waiting for them; each is
  recorded on the board when it holds, in a records commit of its own.
- **The checklists are measured at commits that will move.** Each names its commit (SGK `14bcac0`,
  ChamPBH `c21cdfb`, SI `5fb4a1d`); each client's `HEAD` is that commit today (08's log), and a client
  re-measures at its own `HEAD` when it adopts (`docs/adoption/README.md`, "8. Re-measuring").
- **E2 holds**: `v0.1.0` (tag object `fd5ce48` on `9f8ebe4`) with
  [`docs/adoption/secondarygwkit.md`](adoption/secondarygwkit.md), from `aaab408` (board §2).
- **What remains unverified:**
  - **A client's own stores and run directories.** None was opened (README §3). Records written by
    SGK's `RunRegistry/` are read here only as the tests' fixtures stand for them (03's review read
    records `8155445` wrote; the C4 probe), never SGK's own `var/`.
  - **A client's own suite under the package.** No client's tests have run against `v0.1.0`; that is
    each adoption's (the checklists' item 9).
  - **Linux** only through CI (`ubuntu-24.04`, the four runs of §2.2); every local measurement is
    macOS.
  - **Above the high end.** Python 3.14, and Ray or SQLAlchemy newer than 2.55.1 and 2.0.46, are
    inside the declared range and untested (`README.md`, "Supported versions").
  - **Concurrency.** Concurrent runs and store operations on one client root: the registry records
    and does not lock, and no test or smoke step runs two at once.
- **The two open issues** (§6), each a request to DatastoreKit (README §8).

---

## 11. Reproduction

From a clean checkout of the commit that adds this document, at its root, with `S` a scratch
directory of your own (`mkdir -p "$S/tmp"`), `TMPDIR="$S/tmp"` exported, and the venv of
`README.md`'s "Developing" at `./venv`.

```bash
export S=<scratch>; export TMPDIR="$S/tmp"

# §3: the suite, low end, and per module
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

# §3: the suite, high end, from a clone
git clone -q . "$S/clone-high"
uv venv --python /opt/local/bin/python3.13 "$S/suite-high"
uv pip install --no-cache --python "$S/suite-high/bin/python" -e "$S/clone-high[stores]" \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
(cd "$S/clone-high" && "$S/suite-high/bin/python" -m unittest discover -s runregistrykit/tests -t .)

# §3: black, the equivalence check at 8155445, the adoption script
./venv/bin/black --check runregistrykit docs
git worktree add --detach "$S/check-02" 8155445
(cd "$S/check-02" && "$OLDPWD/venv/bin/python" docs/extraction/compare_with_source.py)
git worktree remove "$S/check-02" && git worktree prune
for c in sgk cpbh si; do ./venv/bin/python docs/adoption/measure_client_registry.py "$c" > "$S/$c.md"; done
# each equals the text of its checklist from its "### Measured: " line to the end:
#   docs/adoption/secondarygwkit.md, champbh.md, stochasticinstantons.md

# §5: the three pin venvs
uv venv --python /opt/local/bin/python3.12 "$S/pin-low"
uv pip install --no-cache --python "$S/pin-low/bin/python" \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.43.0' 'sqlalchemy==2.0.39'
uv venv --python /opt/local/bin/python3.13 "$S/pin-high"
uv pip install --no-cache --python "$S/pin-high/bin/python" \
  'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0' \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
uv venv --python /opt/local/bin/python3.12 "$S/pin-core"
uv pip install --no-cache --python "$S/pin-core/bin/python" \
  'runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.1.0'
for v in pin-low pin-high pin-core; do
  sp=$(ls -d "$S/$v"/lib/python3.1*/site-packages)
  for m in __init__ __main__ client fingerprint stores; do
    git show "9f8ebe4:runregistrykit/$m.py" | cmp - "$sp/runregistrykit/$m.py"
  done
  cat "$sp"/runregistrykit-0.1.0.dist-info/direct_url.json; echo
  grep -c tests "$sp"/runregistrykit-0.1.0.dist-info/RECORD
done

# §4: the smoke run, at both ends and in the core venv
pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'
"$S/pin-low/bin/python"  docs/extraction/store_smoke_run.py   # exit 0
"$S/pin-high/bin/python" docs/extraction/store_smoke_run.py   # exit 0, the same digest
"$S/pin-core/bin/python" docs/extraction/store_smoke_run.py   # exit 1
pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'
# (a) and (b): the diffs of 08's log, applied with `git apply` in a clone, run in pin-low

# §5: the offline rebuild
mkdir "$S/export-v010" && git archive v0.1.0 | tar -x -C "$S/export-v010"
uv build --wheel --offline --out-dir "$S/dist-offline" "$S/export-v010"
```

**The offline variant of the installs**, not the one run here (U24 took the pin from GitHub): a
wheel built as above, and `datastorekit` from `uv`'s cache, which an offline install reaches only by
the tag's full SHA (prompt §1.1: by the tag it fails, "Remote Git fetches are not allowed"):

```bash
uv pip install --offline --python <venv>/bin/python \
  "runregistrykit[stores] @ file://$S/dist-offline/runregistrykit-0.1.0-py3-none-any.whl" \
  'datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005' \
  'ray==2.43.0' 'sqlalchemy==2.0.39'
```

---

## 12. Summary for the board

- **Closed 2026-10-15 at 08.** All eleven prompts landed; 45 commits before 08's, classed (§2.1).
- **`v0.1.0`** (tag object `fd5ce48`, `9f8ebe4`), installed from GitHub at both ends and in the core
  form, is `9f8ebe4`'s five modules and ships no test; CI green on four runs (§2.2, §5).
- **The suite**: 276 OK in `venv/` and at the high end, the same by module (§3).
- **The store layer end to end** (U23, U24): eleven steps pass at both ends against the pin, digest
  `e56c6922…` at both, Ray never initialised; breakage (a)–(c) fail as they should (§4).
- **The equivalence check** at `8155445`: `RESULT: OK`; the three checklists' appendices reproduced
  byte for byte (§3).
- **Issues**: 13 opened, 11 resolved, **2 open** (DatastoreKit requests). **Decisions**: 34, all
  taken as recommended or ruled. **Deviations**: 177 entries (61 / 106 / 3, 10 unlabelled).
  **Observations**: 57, 32 still observations (§6–§9).
- **Open**: G2–G4; E2 holds (§10).
