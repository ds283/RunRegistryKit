# Log — prompt 08: verification and close-out

**Subject:** Verify the extraction campaign and close it
**Commit:** this commit (on `main`, after `302faac`)
**Date:** 2026-10-15
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (`brief-08-section0.md`, corrections 1-10)
**Result:** **landed; the campaign is closed.**
- `docs/extraction-verification.md` is new: twelve sections, every count counted here from the
  records (Verification 9).
- `docs/extraction/store_smoke_run.py` is new (U23): exit 0 at both ends against the pin installed
  from GitHub (U24), eleven steps, the same digest at both
  (`e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069`), Ray never initialised; exit 1
  under (a), (b) and (c) as the prompt's §4.5 says, with correction 5; exit 2 when it cannot start.
- The pin installs at both ends and in the core-only form; its five modules are `9f8ebe4`'s byte for
  byte; its `RECORD` lists no test.
- The suite: **276 -> 276**, in `venv/` and at the high end, the same by module.
- The board, the campaign README, `prompts/INDEX.md` and `docs/OPEN_ISSUES.md` say the campaign is
  closed. Nothing opened; the index counts **2**.
- No file under `runregistrykit/` changed. **No tag made, nothing pushed.** No stop condition fired.
- **The run was interrupted once** by an API usage limit, after the smoke script was first written
  and before its first run; it resumed from the state it left (Verification 1).

## What shipped

| File | Change |
|---|---|
| `docs/extraction-verification.md` | new: the verification document, §2.1's twelve sections |
| `docs/extraction/store_smoke_run.py` | new: the store layer's smoke run (prompt §2.2), black-clean, not a test |
| `prompts/extraction/logs/08-verification-and-close-out.md` | new: this log |
| `prompts/extraction/IMPLEMENTATION_STATE.md` | the header (CLOSED), §1's row for 08, Z1, §2's dated line, §3's count sentence and its two dated lines |
| `prompts/extraction/README.md` | its header, §2's row for 08, a dated line under §7 |
| `prompts/INDEX.md` | the header and the campaign's line: closed, 2 open issues |
| `docs/OPEN_ISSUES.md` | §1.1's heading: closed 2026-10-15 (the header's date and count unchanged: 2026-10-15, 2) |

**The script** (`docs/extraction/store_smoke_run.py`) builds a client root in a `tempfile`
directory: a git repository with one commit holding `runregistrykit.toml`, `.gitignore`, `job.py`
and `smoke_registry.py`, the client's registry and fingerprinter module, written from the string
`REGISTRY_SOURCE` (the contract's version and tag tables, a replicated `Grid`, a sharded `Point`
whose parent is a `Grid`, a writer of a closed two-shard store, and `FINGERPRINTER =
DatastoreKitFingerprinter(FACTORIES, 1)`). Steps 2 and 10 call `begin()` in the script's own process,
so that its closing check that `ray` is not initialised sees whatever the fingerprinter imported;
every command runs as `sys.executable -m runregistrykit …` in the client root. It imports nothing of
`runregistrykit.tests` and `datastorekit` only through the client's module, inside the steps.

## Deviations from the prompt

Each classified. Corrections 1-10 are the brief's.

1. **The commits are 45, not 43** (correction 1). `git rev-list --count 302faac` is 45; the two after
   `aaa1d6d` are `7540efb` (08 written) and `302faac` (08's note). The document's §2.1 classes all
   45 (11 written, 11 notes). **STRUCTURALLY REQUIRED.**
2. **`known()` returns a dict** (correction 2): step 2 asserts `sorted(run.known()) == ["u1"]`. The
   other calls use the signatures the correction gives (`finish(state, exit_code=None, *,
   fingerprint=False)`, `record(unit, data=None)`, `heartbeat(units_done=…, units_total=…,
   stage=…)`), and the commands their required options (`--purpose` for `create` and `copy`,
   `--reason` for `retire` and `amend`, `--field` for `amend`). **STRUCTURALLY REQUIRED.**
3. **The digest is not the planner's** (correction 3): `e56c6922…` at both ends, not `c62012bd…`,
   because the script writes its own registry and store. Printed, never asserted. The document's §4.2
   says why. **STRUCTURALLY REQUIRED.**
4. **The high-end suite venv** (correction 4): `git clone` of this repository at `302faac` into the
   scratchpad, a fresh 3.13.16 `uv` venv, `uv pip install --no-cache -e "<clone>[stores]"` with
   `datastorekit` from `v0.4.0`, Ray 2.55.1 and SQLAlchemy 2.0.46, the suite run from the clone's
   root. `--no-cache` is this agent's, so that nothing came from `uv`'s cache. **IMPLEMENTATION
   CHOICE**, at the orchestrator's reading.
5. **(c) in the core-only venv** (correction 5): steps 3, 10 and 11 pass; steps 1, 2 and 4-9 fail,
   each caught by its step and reported with what it saw; exit 1. Step 3 needs only step 2's run,
   which `begin()` and `finish()` make without `datastorekit`; step 11 needs neither a store nor a
   fingerprinter. The step-by-step table is in the breakage record and the document's §4.3.
   **STRUCTURALLY REQUIRED** (the measured behaviour).
6. **The two indexes' headers** (correction 6): `prompts/INDEX.md` says "1 campaign: 1 closed
   (`extraction`, 2026-10-15)" and its line **closed** 2026-10-15; `docs/OPEN_ISSUES.md` §1.1 says
   "closed 2026-10-15". **IMPLEMENTATION CHOICE**, at the orchestrator's reading.
7. **The breakage diffs** (correction 7) are unified diffs to the committed script with the
   repository's paths, made with `diff -u --label a/docs/extraction/store_smoke_run.py --label
   b/docs/extraction/store_smoke_run.py`, applied with `git apply` in a scratch `git clone` of
   `302faac` with the script copied in (byte-identical to this commit's), never in this checkout.
   (b)'s `UPDATE` is this agent's own, on the script's store: `UPDATE Point SET x = x + 0.25 WHERE
   serial = 1` on shard 0, and (b) also runs `store retire` of the changed store at the start of
   step 5, to record what it does in the same run. **IMPLEMENTATION CHOICE.**
8. **The network beyond the installs** (correction 8): the four CI runs read with `gh run view <id>
   --json`; `git ls-remote` not repeated. Nothing else used the network but the five installs (three
   pin venvs, the high-end suite venv, and none for the offline rebuild). **IMPLEMENTATION CHOICE.**
9. **Outside the scratchpad** (correction 9). The offline rebuild read `uv`'s cache
   (`/Users/ds283/.cache/uv`), the one place allowed. It also made, and removed, its build
   environment there: `builds-v0/`, empty before and after, has the modification time 20:00:05, the
   time of the rebuild. Nothing is left in it. The names in `/private/tmp` beginning `tmp` or `ray`
   are the same at the end as at the start (`ray`, `ray-cpbh`, `ray-cpbh-decoy`, `ray-decoy`,
   `ray-si`; none beginning `tmp`), and `/private/tmp/ray`'s modification time is unchanged
   (2026-10-14 16:32:15). **STRUCTURALLY REQUIRED** (`uv build --offline` needs the cache, and puts
   its build environment beside it).
10. **The per-module counts** (correction 10) come from `unittest.defaultTestLoader.discover(
    "runregistrykit/tests", top_level_dir=".")`, each module suite's `countTestCases()`, named by the
    module of its first test, in a scratch script; equal in both venvs, before and after.
    **IMPLEMENTATION CHOICE**, at the orchestrator's reading.
11. **The interruption.** An API usage limit stopped this agent after the smoke script was first
    written and before it was first run (the suite before, the high-end suite, the installs, the
    release check and the offline rebuild were done). The orchestrator resumed it at 20:11:56. The
    state was re-checked first: `HEAD` `302faac`, the script the only change, the scratch outputs
    complete (each suite output ending in its verdict, `Ran 276 tests … OK`), no Ray process, this
    checkout the only worktree. Nothing was half-done. Both suites were run again at the end
    regardless (Verification 2 and 3). **STRUCTURALLY REQUIRED** (a fact of the run).
12. **Step 9 retires the moved copy**, not the store the run named: the prompt names the commands,
    not the store. The run's store stays for steps 4 and 5, and (b)'s copy, made after the change,
    is then refused at step 9, as the prompt's probe found. **IMPLEMENTATION CHOICE.**
13. **The script's report writes its directory `$SMOKE`**, and prints `$SMOKE = <path>` once at the
    top. **IMPLEMENTATION CHOICE.**
14. **Under (a) and (b) step 9 stops at the dry run's refusal**, so `store retire` without
    `--dry-run` was run once more by hand in each left client root, in the low pin venv; each exits
    1 with the same refusal, and every file is kept (the breakage record). **IMPLEMENTATION
    CHOICE.**
15. **(b) was run twice.** The first `UPDATE`, `x = x + 1`, made row 1 equal row 2 under the same
    grid, so the store also gained a duplicate problem; `x + 0.25` changes one value and nothing
    else, and is the one recorded. Both failed steps 5 and 9 only. **IMPLEMENTATION CHOICE.**
16. **Trial runs before the recorded ones.** Three trial runs at the low end and one in the core
    venv, in the scratchpad, while the script was written: the first passed; the second failed step
    9 on the script's own check (it looked for the deleted files' absolute paths, where `store
    retire` prints them relative to the record root), fixed in the script; the third passed. The
    recorded runs are Verification 10's. **IMPLEMENTATION CHOICE.**
17. **One `store show`, by hand**, in the first trial's left client root, to read how a tombstone
    lists its files (read only). **IMPLEMENTATION CHOICE.**
18. **The document's deviation count** (§8) counts an entry with two labels under each and adds a
    column for entries with none; 04a's log gives 6 / 17 by entry where the board's review of 04a says
    7 / 15. The document says the log is the record. **IMPLEMENTATION CHOICE.**
19. **The document's smoke output** writes the scratchpad's path `<scratch>`; this log has every run
    verbatim. **IMPLEMENTATION CHOICE.**
20. **The low pin install carried a stray `VIRTUAL_ENV=<scratch>/pin-low` prefix**, left from a
    draft of the command; `--python` names the venv, so it changed nothing (the install's own line,
    "Using Python 3.12.15 environment at: pin-low", and the release check). **UNINTENDED DRIFT.**
21. **`PROVENANCE.md`'s preamble is not changed**, though 05c's, 06's and 07's logs left it "for 08":
    the prompt's §7 forbids changing `PROVENANCE.md`. It is an observation below and in the
    document's §9. **STRUCTURALLY REQUIRED.**
22. **`git -C <client> worktree list`**, run on each of the five repositories at the start and at
    the end, for the brief's "Worktrees" column. It is read-only, but `worktree` is among the
    commands the brief says never to run in a client (07's deviation 23 was the same). It changed
    nothing: each `HEAD`, `status --porcelain` hash and stash count is the same at the end as at
    the start (Verification 1 and 12). **UNINTENDED DRIFT.**

No stop condition (§6) fired.

## Verification performed

### 1. The state at the start, and the interruption

At 19:57 (BST), before any work: `HEAD` `302faac`, clean, this checkout the only worktree; `git
status --short --ignored` shows `prompts/.DS_Store`, `runregistrykit.egg-info/`,
`runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/` and `venv/`; `docs/` holds
`adoption/` (five files), `extraction/` (two scripts) and `OPEN_ISSUES.md`. `black` 25.1.0; `uv`
0.12.20; no Ray process (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` exit 1);
`RAY_ADDRESS` unset. `/private/tmp`: `ray`, `ray-cpbh`, `ray-cpbh-decoy`, `ray-decoy`, `ray-si`, none
beginning `tmp`; `/private/tmp/ray` modified 2026-10-14 16:32:15.

The clients, through `git` only (`rev-parse --abbrev-ref HEAD`, `rev-parse HEAD`, `status
--porcelain | wc -l`, `status --porcelain | shasum`, `stash list | wc -l`, `worktree list | wc -l`):

Taken Thu Oct 15 19:57:19 BST 2026:

| Repository | Branch | HEAD | status lines | status shasum | stash | worktrees |
|---|---|---|---|---|---|---|
| SecondaryGWKit | handover-remedial | 14bcac0eb73069131f8ce4f55d91e5fc3e7318cf | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |
| ChamPBH | main | c21cdfb5613a3ed976a91a95431495dc8bfd49c8 | 22 | fbd525ec2b83137d7cd2d40b515a612919485205 | 0 | 1 |
| StochasticInstantons | dk-and-rpk-migration | 5fb4a1d71a016f1b23393923b9a3d59972415aa0 | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |
| DatastoreKit | main | b01737f139e5d8785ff915a929b9bd1b384ec840 | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |
| RayPoolKit | main | 17029d99bb2635ff7ce9b99b11e9c5f77d8b6967 | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |

**The interruption** (deviation 11): resumed at 20:11:56; `HEAD` `302faac`; `git status --short`
showed only `?? docs/extraction/store_smoke_run.py`; this checkout the only worktree; no Ray process.

### 2. The suite in `venv/`

Before (19:59) and after (20:30, with every change of this commit in the tree), each with `TMPDIR`
a fresh directory in the scratchpad, which held nothing afterwards; no Ray process before or after
either:

```text
$ TMPDIR=<scratch>/tmp/suite-before ./venv/bin/python -m unittest discover -s runregistrykit/tests -t .
....................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 276 tests in 86.592s

OK
$ TMPDIR=<scratch>/tmp/suite-after ./venv/bin/python -m unittest discover -s runregistrykit/tests -t .
....................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 276 tests in 96.662s

OK
```

By module, before and after the same (`diff` empty):

```text
  27  runregistrykit.tests.test_client_root
  31  runregistrykit.tests.test_fingerprinter
   3  runregistrykit.tests.test_package_imports
  22  runregistrykit.tests.test_package_is_generic
   8  runregistrykit.tests.test_public_names
  29  runregistrykit.tests.test_run_registry
  21  runregistrykit.tests.test_store_amend
   9  runregistrykit.tests.test_store_amend_residuals
   2  runregistrykit.tests.test_store_command_line
  27  runregistrykit.tests.test_store_copy_move
  29  runregistrykit.tests.test_store_fingerprint
  41  runregistrykit.tests.test_store_retire
  10  runregistrykit.tests.test_store_retire_references
  17  runregistrykit.tests.test_store_sidecar
 276  total
```

`git status --short --ignored` after: this commit's seven files and the same ignored entries as at
the start; no `var/`.

### 3. The suite at the high end

The venv (deviation 4), `git clone` of `302faac`:

```text
+(eval):1> git clone -q /Users/ds283/Documents/Code/RunRegistryKit <scratch>/clone-high
+(eval):1> git -C <scratch>/clone-high log --oneline -1
302faac Write the orchestration note for extraction prompt 08
+(eval):1> uv venv --python /opt/local/bin/python3.13 <scratch>/suite-high
Using CPython 3.13.16 interpreter at: /opt/local/bin/python3.13
Creating virtual environment at: suite-high
Activate with: source suite-high/bin/activate
+(eval):1> uv pip install --no-cache --python <scratch>/suite-high/bin/python -e '<scratch>/clone-high[stores]' 'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
Using Python 3.13.16 environment at: suite-high
Resolved 21 packages in 887ms
   Building runregistrykit @ file://<scratch>/clone-high
   Updating https://github.com/ds283/DatastoreKit (v0.4.0)
Downloading sqlalchemy (2.1MiB)
Downloading ray (62.7MiB)
 Downloaded sqlalchemy
      Built runregistrykit @ file://<scratch>/clone-high
    Updated https://github.com/ds283/DatastoreKit (c8570e849334d09085bbd84876095fc9e22bd005)
   Building datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005
      Built datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005
 Downloaded ray
Prepared 21 packages in 3.47s
Installed 21 packages in 52ms
 + attrs==26.1.0
 + certifi==2026.7.22
 + charset-normalizer==3.5.2
 + click==8.5.0
 + datastorekit==0.4.0 (from git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005)
 + filelock==4.2.0
 + idna==3.20
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + msgpack==1.2.3
 + packaging==26.3
 + protobuf==7.36.2
 + pyyaml==6.0.3
 + ray==2.55.1
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + runregistrykit==0.1.0 (from file://<scratch>/clone-high)
 + sqlalchemy==2.0.46
 + typing-extensions==4.16.0
 + urllib3==2.8.0
+(eval):1> echo 'EXIT 0'
EXIT 0
```

From the clone's root, `runregistrykit.__file__` the clone's (3.13.16), twice: before the
interruption and after it, no Ray process before or after either:

```text
$ TMPDIR=<scratch>/tmp/suite-high <scratch>/suite-high/bin/python -m unittest discover -s runregistrykit/tests -t .
....................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 276 tests in 94.913s

OK
$ TMPDIR=<scratch>/tmp/suite-high-after <scratch>/suite-high/bin/python -m unittest discover -s runregistrykit/tests -t .
....................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 276 tests in 98.918s

OK
```

By module, equal to `venv/`'s (`diff` empty):

```text
  27  runregistrykit.tests.test_client_root
  31  runregistrykit.tests.test_fingerprinter
   3  runregistrykit.tests.test_package_imports
  22  runregistrykit.tests.test_package_is_generic
   8  runregistrykit.tests.test_public_names
  29  runregistrykit.tests.test_run_registry
  21  runregistrykit.tests.test_store_amend
   9  runregistrykit.tests.test_store_amend_residuals
   2  runregistrykit.tests.test_store_command_line
  27  runregistrykit.tests.test_store_copy_move
  29  runregistrykit.tests.test_store_fingerprint
  41  runregistrykit.tests.test_store_retire
  10  runregistrykit.tests.test_store_retire_references
  17  runregistrykit.tests.test_store_sidecar
 276  total
```

### 4. `black`

`./venv/bin/black --check runregistrykit docs`: "28 files would be left unchanged" (27 before, and
the script, formatted with `./venv/bin/black` 25.1.0).

### 5. `compare_with_source.py` at `8155445`

```bash
git worktree add --detach <scratch>/check-02 8155445
(cd <scratch>/check-02 && TMPDIR=<scratch>/tmp /Users/ds283/Documents/Code/RunRegistryKit/venv/bin/python docs/extraction/compare_with_source.py)
git worktree remove <scratch>/check-02; git worktree prune
```

Exit 0; afterwards `git worktree list` shows this checkout alone. The output, 467 lines, equals the
one in 02's log byte for byte (its one fenced block holding "Summary: 12 checked", compared as
text). Whole:

```text
Equivalence check: runregistrykit against SecondaryGWKit (/Users/ds283/Documents/Code/SecondaryGWKit) at a45aefc702de643c330372dd6d2d983f38bb8eed

RunRegistry/ at the import commit: 25 rows; the table: 25 rows
  equal, path for path and blob for blob (25 rows)
StoreFixtures/shard_store_fixtures.py at the import commit: blob 1375949aacde2263de991785055cd7dfabc57251 (as the table says)

runregistrykit/__init__.py  <-  RunRegistry/__init__.py  [imported by 01]
  D-name: 6
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 704
  unclassified: 0
    D-name source :7
        - `<stem>.manifest.json` sidecars (`RunRegistry.stores`), because the user decided that managing
        + `<stem>.manifest.json` sidecars (`runregistrykit.stores`), because the user decided that managing
    D-name source :31
        -     run = RunRegistry.begin(
        +     run = runregistrykit.begin(
    D-name source :43
        - `python -m RunRegistry list` prints every run, newest first, and says loudly which of them claim
        + `python -m runregistrykit list` prints every run, newest first, and says loudly which of them claim
    D-name source :371
        -         store (`RunRegistry.stores.fingerprint_store`, read-only, with this run as `taken_by` so
        +         store (`runregistrykit.stores.fingerprint_store`, read-only, with this run as `taken_by` so
    D-name source :581
        -     When `results` has a problem-free registry sidecar beside it (`RunRegistry.stores`), it holds
        +     When `results` has a problem-free registry sidecar beside it (`runregistrykit.stores`), it holds
    D-name source :587
        -     (`RunRegistry.stores.retire_store`) is refused before the run directory is created, because a
        +     (`runregistrykit.stores.retire_store`) is refused before the run directory is created, because a

runregistrykit/__main__.py  <-  RunRegistry/__main__.py  [imported by 01]
  D-name: 4
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 511
  unclassified: 0
    D-name source :1
        - """`python -m RunRegistry list` — one line per run, newest first.
        + """`python -m runregistrykit list` — one line per run, newest first.
    D-name source :6
        - `python -m RunRegistry store {show,create,adopt,copy,move,fingerprint,retire,amend}` manages a
        + `python -m runregistrykit store {show,create,adopt,copy,move,fingerprint,retire,amend}` manages a
    D-name source :7
        - datastore and its `<stem>.manifest.json` sidecar (`RunRegistry.stores`). `show` is read-only.
        + datastore and its `<stem>.manifest.json` sidecar (`runregistrykit.stores`). `show` is read-only.
    D-name source :373
        -     parser = argparse.ArgumentParser(prog="RunRegistry", description=__doc__)
        +     parser = argparse.ArgumentParser(prog="runregistrykit", description=__doc__)

runregistrykit/stores.py  <-  RunRegistry/stores.py  [imported by 01]
  D-name: 13
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 2172
  unclassified: 0
    D-name source :115
        - like `import RunRegistry`, loads neither `ray` nor `sqlalchemy`.
        + like `import runregistrykit`, loads neither `ray` nor `sqlalchemy`.
    D-name source :197
        - # (`RunRegistry/tests/data/full_store_fingerprint*.json`; `test_store_fingerprint.GOLDEN` names the
        + # (`runregistrykit/tests/data/full_store_fingerprint*.json`; `test_store_fingerprint.GOLDEN` names the
    D-name source :544
        -             f'. Run `python -m RunRegistry store retire "{primary}" --reason <the recorded '
        +             f'. Run `python -m runregistrykit store retire "{primary}" --reason <the recorded '
    D-name source :1025
        -             f"registry sidecar ({why}). Run `python -m RunRegistry store create` or `store "
        +             f"registry sidecar ({why}). Run `python -m runregistrykit store create` or `store "
    D-name source :1196
        -     # here, not at module scope: that module imports sqlalchemy, and `import RunRegistry` must not
        +     # here, not at module scope: that module imports sqlalchemy, and `import runregistrykit` must not
    D-name source :1455
        -        that `import RunRegistry` loads neither ray nor sqlalchemy;
        +        that `import runregistrykit` loads neither ray nor sqlalchemy;
    D-name source :1538
        -                 f"RunRegistry store create` or `store adopt` on it first; a fingerprint never "
        +                 f"runregistrykit store create` or `store adopt` on it first; a fingerprint never "
    D-name source :1694
        -         f"[{present}].{left} Once the failure is understood, run `python -m RunRegistry store "
        +         f"[{present}].{left} Once the failure is understood, run `python -m runregistrykit store "
    D-name source :1758
        -             f"({_sidecar_refusal(reading)}). Run `python -m RunRegistry store create` or `store "
        +             f"({_sidecar_refusal(reading)}). Run `python -m runregistrykit store create` or `store "
    D-name source :1810
        -             f'it is ended, `python -m RunRegistry store fingerprint "{primary}" --write` records '
        +             f'it is ended, `python -m runregistrykit store fingerprint "{primary}" --write` records '
    D-name source :1876
        -                     f'retirement deleted. Run `python -m RunRegistry store fingerprint "{primary}" '
        +                     f'retirement deleted. Run `python -m runregistrykit store fingerprint "{primary}" '
    D-name source :1907
        -                     f'`python -m RunRegistry store fingerprint "{primary}" --write`, then `store '
        +                     f'`python -m runregistrykit store fingerprint "{primary}" --write`, then `store '
    D-name source :2119
        -             f"({_sidecar_refusal(reading)}). Run `python -m RunRegistry store create` or `store "
        +             f"({_sidecar_refusal(reading)}). Run `python -m runregistrykit store create` or `store "

runregistrykit/tests/__init__.py  <-  RunRegistry/tests/__init__.py  [imported by 01]
  D-name: 0
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 0
  unclassified: 0

runregistrykit/tests/store_fixtures.py  <-  RunRegistry/tests/store_fixtures.py  [ported by 02]
  D-name: 6
  D-fix: 2
  D-fmt: 0
  D-fmt hunks: 0
  identical: 215
  unclassified: 0
    D-name source :15
        - import RunRegistry
        + import runregistrykit
    D-name source :16
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :17
        - from RunRegistry.tests.test_run_registry import RegistryTestCase
        + from runregistrykit.tests.test_run_registry import RegistryTestCase
    D-name source :143
        -     def a_running_run(self, slug: str, results) -> "RunRegistry.Run":
        +     def a_running_run(self, slug: str, results) -> "runregistrykit.Run":
    D-name source :146
        -     def a_stale_run(self, slug: str, results) -> "RunRegistry.Run":
        +     def a_stale_run(self, slug: str, results) -> "runregistrykit.Run":
    D-name source :181
        -             reading.fields["history"][-1]["to"], RunRegistry._repo_path(primary)
        +             reading.fields["history"][-1]["to"], runregistrykit._repo_path(primary)
    D-fix source :4
        - built in one temporary directory: stores with `StoreFixtures/shard_store_fixtures.py` (a real
        + built in one temporary directory: stores with `runregistrykit/tests/shard_store_fixtures.py` (a real
    D-fix source :20
        - from StoreFixtures.shard_store_fixtures import (
        + from runregistrykit.tests.shard_store_fixtures import (

runregistrykit/tests/test_run_registry.py  <-  RunRegistry/tests/test_run_registry.py  [ported by 02]
  D-name: 31
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 680
  unclassified: 0
    D-name source :1
        - """Tests for `RunRegistry`. No Ray, no datastore, no network; every run directory these build is
        + """Tests for `runregistrykit`. No Ray, no datastore, no network; every run directory these build is
    D-name source :19
        - import RunRegistry
        + import runregistrykit
    D-name source :21
        - REPO_ROOT = RunRegistry.REPO_ROOT
        + REPO_ROOT = runregistrykit.REPO_ROOT
    D-name source :31
        - import RunRegistry
        + import runregistrykit
    D-name source :34
        - status = RunRegistry.read_json(os.path.join(run_dir, "status.json"))
        + status = runregistrykit.read_json(os.path.join(run_dir, "status.json"))
    D-name source :80
        -             "verdict": RunRegistry.liveness(status, stale_after=3600.0),
        +             "verdict": runregistrykit.liveness(status, stale_after=3600.0),
    D-name source :99
        - import RunRegistry
        + import runregistrykit
    D-name source :101
        - RunRegistry.begin(
        + runregistrykit.begin(
    D-name source :124
        -         return RunRegistry.begin(
        +         return runregistrykit.begin(
    D-name source :133
        -             RunRegistry.pid_alive(corpse.pid),
        +             runregistrykit.pid_alive(corpse.pid),
    D-name source :239
        -         manifest = RunRegistry.read_json(os.path.join(path, "manifest.json"))
        +         manifest = runregistrykit.read_json(os.path.join(path, "manifest.json"))
    D-name source :243
        -         status = RunRegistry.read_json(os.path.join(path, "status.json"))
        +         status = runregistrykit.read_json(os.path.join(path, "status.json"))
    D-name source :271
        -             run.manifest["script_sha256"], RunRegistry.script_sha256(__file__)
        +             run.manifest["script_sha256"], runregistrykit.script_sha256(__file__)
    D-name source :282
        -             set(run.manifest["packages"]), set(RunRegistry.RECORDED_DISTRIBUTIONS)
        +             set(run.manifest["packages"]), set(runregistrykit.RECORDED_DISTRIBUTIONS)
    D-name source :284
        -         self.assertEqual(run.manifest["packages"], RunRegistry.package_provenance())
        +         self.assertEqual(run.manifest["packages"], runregistrykit.package_provenance())
    D-name source :285
        -         on_disk = RunRegistry.read_json(run.manifest_path)
        +         on_disk = runregistrykit.read_json(run.manifest_path)
    D-name source :286
        -         self.assertEqual(on_disk["packages"], RunRegistry.package_provenance())
        +         self.assertEqual(on_disk["packages"], runregistrykit.package_provenance())
    D-name source :307
        -         name the module calls (`RunRegistry.importlib.metadata.distribution`, which is the same
        +         name the module calls (`runregistrykit.importlib.metadata.distribution`, which is the same
    D-name source :317
        -             RunRegistry.importlib.metadata, "distribution", distribution
        +             runregistrykit.importlib.metadata, "distribution", distribution
    D-name source :319
        -             return RunRegistry.package_provenance()
        +             return runregistrykit.package_provenance()
    D-name source :395
        -             RunRegistry.RECORDED_DISTRIBUTIONS, ("datastorekit", "raypoolkit")
        +             runregistrykit.RECORDED_DISTRIBUTIONS, ("datastorekit", "raypoolkit")
    D-name source :421
        -             "recorded": RunRegistry.now_iso(),
        +             "recorded": runregistrykit.now_iso(),
    D-name source :574
        -             RunRegistry.read_json(run.manifest_path)["results"],
        +             runregistrykit.read_json(run.manifest_path)["results"],
    D-name source :638
        -         self.assertLess(RunRegistry.heartbeat_age(status), 60.0)
        +         self.assertLess(runregistrykit.heartbeat_age(status), 60.0)
    D-name source :639
        -         self.assertEqual(RunRegistry.liveness(status, stale_after=3600.0), "stale")
        +         self.assertEqual(runregistrykit.liveness(status, stale_after=3600.0), "stale")
    D-name source :644
        -         self.assertTrue(RunRegistry.pid_alive(status["pid"]))
        +         self.assertTrue(runregistrykit.pid_alive(status["pid"]))
    D-name source :645
        -         self.assertEqual(RunRegistry.liveness(status, stale_after=1e9), "alive")
        +         self.assertEqual(runregistrykit.liveness(status, stale_after=1e9), "alive")
    D-name source :646
        -         self.assertEqual(RunRegistry.liveness(status, stale_after=-1.0), "stale")
        +         self.assertEqual(runregistrykit.liveness(status, stale_after=-1.0), "stale")
    D-name source :652
        -             RunRegistry.liveness(run.status(), stale_after=1e9), "finished"
        +             runregistrykit.liveness(run.status(), stale_after=1e9), "finished"
    D-name source :668
        -         entries = RunRegistry.list_runs(root=self.root)
        +         entries = runregistrykit.list_runs(root=self.root)
    D-name source :681
        -             [sys.executable, "-m", "RunRegistry", "list", "--root", self.root],
        +             [sys.executable, "-m", "runregistrykit", "list", "--root", self.root],

runregistrykit/tests/test_store_sidecar.py  <-  RunRegistry/tests/test_store_sidecar.py  [ported by 02]
  D-name: 15
  D-fix: 1
  D-fmt: 0
  D-fmt hunks: 0
  identical: 601
  unclassified: 0
    D-name source :6
        - and one of them names a different store from the one it sits beside. `RunRegistry.stores` now
        + and one of them names a different store from the one it sits beside. `runregistrykit.stores` now
    D-name source :17
        - import RunRegistry
        + import runregistrykit
    D-name source :18
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :19
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :51
        -         package = Path(RunRegistry.__file__).parent
        +         package = Path(runregistrykit.__file__).parent
    D-name source :287
        -         self.assertEqual(entry["to"], RunRegistry._repo_path(primary))
        +         self.assertEqual(entry["to"], runregistrykit._repo_path(primary))
    D-name source :369
        -         self.assertEqual(entry["to"], RunRegistry._repo_path(primary))
        +         self.assertEqual(entry["to"], runregistrykit._repo_path(primary))
    D-name source :539
        -             RunRegistry.read_json(run.manifest_path)["results_store_id"],
        +             runregistrykit.read_json(run.manifest_path)["results_store_id"],
    D-name source :566
        -                 manifest = RunRegistry.read_json(run.manifest_path)
        +                 manifest = runregistrykit.read_json(run.manifest_path)
    D-name source :588
        -             "created": RunRegistry.now_iso(),
        +             "created": runregistrykit.now_iso(),
    D-name source :592
        -         RunRegistry.write_json_atomic(os.path.join(old, "manifest.json"), manifest)
        +         runregistrykit.write_json_atomic(os.path.join(old, "manifest.json"), manifest)
    D-name source :593
        -         RunRegistry.write_json_atomic(
        +         runregistrykit.write_json_atomic(
    D-name source :598
        -                 "heartbeat": RunRegistry.now_iso(),
        +                 "heartbeat": runregistrykit.now_iso(),
    D-name source :601
        -         (entry,) = RunRegistry.list_runs(root=self.root)
        +         (entry,) = runregistrykit.list_runs(root=self.root)
    D-name source :604
        -         self.assertEqual(RunRegistry.Run(old).results_path, str(primary))
        +         self.assertEqual(runregistrykit.Run(old).results_path, str(primary))
    D-fix source :28
        - from StoreFixtures.shard_store_fixtures import tree_state, write_placeholder
        + from runregistrykit.tests.shard_store_fixtures import tree_state, write_placeholder

runregistrykit/tests/test_store_copy_move.py  <-  RunRegistry/tests/test_store_copy_move.py  [ported by 02]
  D-name: 10
  D-fix: 1
  D-fmt: 12
  D-fmt hunks: 3
  identical: 590
  unclassified: 0
    D-name source :5
        - its sidecar. `RunRegistry.stores.copy_store` / `move_store` call them, then carry the sidecar: a
        + its sidecar. `runregistrykit.stores.copy_store` / `move_store` call them, then carry the sidecar: a
    D-name source :21
        - import RunRegistry
        + import runregistrykit
    D-name source :22
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :23
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :73
        -             {"store_id": source["store_id"], "datastore": RunRegistry._repo_path(src)},
        +             {"store_id": source["store_id"], "datastore": runregistrykit._repo_path(src)},
    D-name source :78
        -         self.assertEqual(entry["from"], RunRegistry._repo_path(src))
        +         self.assertEqual(entry["from"], runregistrykit._repo_path(src))
    D-name source :79
        -         self.assertEqual(entry["to"], RunRegistry._repo_path(dst))
        +         self.assertEqual(entry["to"], runregistrykit._repo_path(dst))
    D-name source :110
        -             third["copied_from"]["datastore"], RunRegistry._repo_path(middle)
        +             third["copied_from"]["datastore"], runregistrykit._repo_path(middle)
    D-name source :135
        -                     ("move", RunRegistry._repo_path(src), RunRegistry._repo_path(dst)),
        +                     ("move", runregistrykit._repo_path(src), runregistrykit._repo_path(dst)),
    D-name source :211
        -         self.assertEqual(RunRegistry.list_runs(root=self.root)[0]["liveness"], "stale")
        +         self.assertEqual(runregistrykit.list_runs(root=self.root)[0]["liveness"], "stale")
    D-fix source :32
        - from StoreFixtures.shard_store_fixtures import tree_state
        + from runregistrykit.tests.shard_store_fixtures import tree_state
    D-fmt source :73-73 -> package :73-76
        -             {"store_id": source["store_id"], "datastore": runregistrykit._repo_path(src)},
        +             {
        +                 "store_id": source["store_id"],
        +                 "datastore": runregistrykit._repo_path(src),
        +             },
    D-fmt source :135-135 -> package :138-142
        -                     ("move", runregistrykit._repo_path(src), runregistrykit._repo_path(dst)),
        +                     (
        +                         "move",
        +                         runregistrykit._repo_path(src),
        +                         runregistrykit._repo_path(dst),
        +                     ),
    D-fmt source :211-211 -> package :218-220
        -         self.assertEqual(runregistrykit.list_runs(root=self.root)[0]["liveness"], "stale")
        +         self.assertEqual(
        +             runregistrykit.list_runs(root=self.root)[0]["liveness"], "stale"
        +         )

runregistrykit/tests/test_store_command_line.py  <-  RunRegistry/tests/test_store_command_line.py  [ported by 02]
  D-name: 11
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 172
  unclassified: 0
    D-name source :1
        - """`python -m RunRegistry store …`, and what importing the registry loads.
        + """`python -m runregistrykit store …`, and what importing the registry loads.
    D-name source :5
        - RunRegistry` does (`runpy.run_module("RunRegistry", run_name="__main__", alter_sys=True)`), and
        + runregistrykit` does (`runpy.run_module("runregistrykit", run_name="__main__", alter_sys=True)`), and
    D-name source :16
        - import RunRegistry
        + import runregistrykit
    D-name source :17
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :18
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :25
        - REPO_ROOT = RunRegistry.REPO_ROOT
        + REPO_ROOT = runregistrykit.REPO_ROOT
    D-name source :30
        - sys.argv = ["RunRegistry"] + sys.argv[1:]
        + sys.argv = ["runregistrykit"] + sys.argv[1:]
    D-name source :33
        -     runpy.run_module("RunRegistry", run_name="__main__", alter_sys=True)
        +     runpy.run_module("runregistrykit", run_name="__main__", alter_sys=True)
    D-name source :47
        - import RunRegistry
        + import runregistrykit
    D-name source :48
        - import RunRegistry.stores
        + import runregistrykit.stores
    D-name source :55
        -         """Run ``python -m RunRegistry *argv`` in a child; return (report, stdout, stderr)."""
        +         """Run ``python -m runregistrykit *argv`` in a child; return (report, stdout, stderr)."""

runregistrykit/tests/test_store_amend.py  <-  RunRegistry/tests/test_store_amend.py  [ported by 02]
  D-name: 8
  D-fix: 1
  D-fmt: 0
  D-fmt hunks: 0
  identical: 632
  unclassified: 0
    D-name source :2
        - `RunRegistry.stores.amend_sidecar`, the `amend` history entry and its markers, the D5 guards, and
        + `runregistrykit.stores.amend_sidecar`, the `amend` history entry and its markers, the D5 guards, and
    D-name source :3
        - `python -m RunRegistry store amend`.
        + `python -m runregistrykit store amend`.
    D-name source :26
        - import RunRegistry
        + import runregistrykit
    D-name source :27
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :28
        - from RunRegistry.stores import KNOWN_FIELDS, amend_sidecar
        + from runregistrykit.stores import KNOWN_FIELDS, amend_sidecar
    D-name source :29
        - from RunRegistry.tests.store_fixtures import (
        + from runregistrykit.tests.store_fixtures import (
    D-name source :35
        - from RunRegistry.tests.test_store_command_line import (
        + from runregistrykit.tests.test_store_command_line import (
    D-name source :42
        - _repo_path = RunRegistry._repo_path
        + _repo_path = runregistrykit._repo_path
    D-fix source :15
        - Stores are the lightweight placeholder fixture (`StoreFixtures.shard_store_fixtures`), because
        + Stores are the lightweight placeholder fixture (`runregistrykit.tests.shard_store_fixtures`), because

runregistrykit/tests/test_store_amend_residuals.py  <-  RunRegistry/tests/test_store_amend_residuals.py  [ported by 02]
  D-name: 2
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 265
  unclassified: 0
    D-name source :21
        - from RunRegistry import stores
        + from runregistrykit import stores
    D-name source :22
        - from RunRegistry.tests.test_store_amend import AmendTestCase, REASON
        + from runregistrykit.tests.test_store_amend import AmendTestCase, REASON

runregistrykit/tests/shard_store_fixtures.py  <-  StoreFixtures/shard_store_fixtures.py  [ported by 02]
  D-name: 0
  D-fix: 0
  D-fmt: 0
  D-fmt hunks: 0
  identical: 168
  unclassified: 0

Pending, ported by a later prompt: 3
  pending, 04: runregistrykit/tests/test_store_retire.py  <-  RunRegistry/tests/test_store_retire.py
  pending, 04: runregistrykit/tests/test_store_retire_references.py  <-  RunRegistry/tests/test_store_retire_references.py
  pending, 04: runregistrykit/tests/test_store_fingerprint.py  <-  RunRegistry/tests/test_store_fingerprint.py

Not imported, and absent from runregistrykit/: 11 of 11

Files with no source (declared): 1
  runregistrykit/tests/test_package_imports.py: present (01 §2.7: the import test)

Undeclared files under runregistrykit/: 0

Summary: 12 checked (4 by 01, 8 by 02): D-name 106, D-fix 5, D-fmt 12 in 3 hunks; 3 pending; 11 not imported and absent; 1 declared new
RESULT: OK
```

### 6. `measure_client_registry.py`, against the appendices

Each client's `HEAD` is its checklist's commit (Verification 1), so the script ran at its default.
Each appendix was extracted by a scratch script (the checklist's text after "## Appendix: the
script's output", from its first "### Measured: " line to the end) and compared with `cmp`:

```text
$ ./venv/bin/python docs/adoption/measure_client_registry.py sgk > <scratch>/out/measure-sgk.md
exit 0; 399 lines; stderr 0 bytes
$ cmp <scratch>/out/measure-sgk.md <scratch>/out/appendix-sgk.md   # docs/adoption/secondarygwkit.md's appendix
exit 0 (equal); SHA-256 49e23b44685c4033be2c2ac5177f03429fa2f845d0a2955aac482c7a75072657
$ ./venv/bin/python docs/adoption/measure_client_registry.py cpbh > <scratch>/out/measure-cpbh.md
exit 0; 84 lines; stderr 0 bytes
$ cmp <scratch>/out/measure-cpbh.md <scratch>/out/appendix-cpbh.md   # docs/adoption/champbh.md's appendix
exit 0 (equal); SHA-256 0e5660b6e1793015f0ce63f330adc5aa8d438542034e03055eba65d9d59c73e4
$ ./venv/bin/python docs/adoption/measure_client_registry.py si > <scratch>/out/measure-si.md
exit 0; 90 lines; stderr 0 bytes
$ cmp <scratch>/out/measure-si.md <scratch>/out/appendix-si.md   # docs/adoption/stochasticinstantons.md's appendix
exit 0 (equal); SHA-256 0a58ddb89c431d1336d3a1fb6403405507835776f68f60d43db4a415d81bbf85
```

### 7. The installs and the release check

Each venv made with `uv venv --python <interpreter>`, `TMPDIR=<scratch>/tmp/uv`. The commands and
what they resolved, whole:

```text
+(eval):3> uv venv --python /opt/local/bin/python3.12 <scratch>/pin-low
Using CPython 3.12.15 interpreter at: /opt/local/bin/python3.12
Creating virtual environment at: pin-low
Activate with: source pin-low/bin/activate
+(eval):4> VIRTUAL_ENV=<scratch>/pin-low uv pip install --no-cache --python <scratch>/pin-low/bin/python 'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0' 'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.43.0' 'sqlalchemy==2.0.39'
Using Python 3.12.15 environment at: pin-low
Resolved 23 packages in 911ms
   Updating https://github.com/ds283/DatastoreKit (v0.4.0)
   Updating https://github.com/ds283/RunRegistryKit (v0.1.0)
Downloading sqlalchemy (2.0MiB)
Downloading ray (62.1MiB)
 Downloaded sqlalchemy
    Updated https://github.com/ds283/RunRegistryKit (9f8ebe431503fb8c79ee1407cc460501f1ca2d92)
   Building runregistrykit @ git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92
    Updated https://github.com/ds283/DatastoreKit (c8570e849334d09085bbd84876095fc9e22bd005)
   Building datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005
      Built runregistrykit @ git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92
      Built datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005
 Downloaded ray
Prepared 23 packages in 3.40s
Installed 23 packages in 47ms
 + aiosignal==1.4.0
 + attrs==26.1.0
 + certifi==2026.7.22
 + charset-normalizer==3.5.2
 + click==8.5.0
 + datastorekit==0.4.0 (from git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005)
 + filelock==4.2.0
 + frozenlist==1.8.0
 + idna==3.20
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + msgpack==1.2.3
 + packaging==26.3
 + protobuf==7.36.2
 + pyyaml==6.0.3
 + ray==2.43.0
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + runregistrykit==0.1.0 (from git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92)
 + sqlalchemy==2.0.39
 + typing-extensions==4.16.0
 + urllib3==2.8.0
+(eval):5> echo 'EXIT low 0'
EXIT low 0
+(eval):6> uv venv --python /opt/local/bin/python3.13 <scratch>/pin-high
Using CPython 3.13.16 interpreter at: /opt/local/bin/python3.13
Creating virtual environment at: pin-high
Activate with: source pin-high/bin/activate
+(eval):7> uv pip install --no-cache --python <scratch>/pin-high/bin/python 'runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0' 'datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0' 'ray==2.55.1' 'sqlalchemy==2.0.46'
Using Python 3.13.16 environment at: pin-high
Resolved 21 packages in 542ms
   Updating https://github.com/ds283/RunRegistryKit (v0.1.0)
   Updating https://github.com/ds283/DatastoreKit (v0.4.0)
Downloading ray (62.7MiB)
Downloading sqlalchemy (2.1MiB)
 Downloaded sqlalchemy
    Updated https://github.com/ds283/RunRegistryKit (9f8ebe431503fb8c79ee1407cc460501f1ca2d92)
   Building runregistrykit @ git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92
    Updated https://github.com/ds283/DatastoreKit (c8570e849334d09085bbd84876095fc9e22bd005)
   Building datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005
      Built runregistrykit @ git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92
      Built datastorekit @ git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005
 Downloaded ray
Prepared 21 packages in 4.00s
Installed 21 packages in 65ms
 + attrs==26.1.0
 + certifi==2026.7.22
 + charset-normalizer==3.5.2
 + click==8.5.0
 + datastorekit==0.4.0 (from git+https://github.com/ds283/DatastoreKit@c8570e849334d09085bbd84876095fc9e22bd005)
 + filelock==4.2.0
 + idna==3.20
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + msgpack==1.2.3
 + packaging==26.3
 + protobuf==7.36.2
 + pyyaml==6.0.3
 + ray==2.55.1
 + referencing==0.37.0
 + requests==2.34.2
 + rpds-py==2026.9.1
 + runregistrykit==0.1.0 (from git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92)
 + sqlalchemy==2.0.46
 + typing-extensions==4.16.0
 + urllib3==2.8.0
+(eval):8> echo 'EXIT high 0'
EXIT high 0
+(eval):9> uv venv --python /opt/local/bin/python3.12 <scratch>/pin-core
Using CPython 3.12.15 interpreter at: /opt/local/bin/python3.12
Creating virtual environment at: pin-core
Activate with: source pin-core/bin/activate
+(eval):10> uv pip install --no-cache --python <scratch>/pin-core/bin/python 'runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.1.0'
Using Python 3.12.15 environment at: pin-core
Resolved 1 package in 196ms
   Updating https://github.com/ds283/RunRegistryKit (v0.1.0)
    Updated https://github.com/ds283/RunRegistryKit (9f8ebe431503fb8c79ee1407cc460501f1ca2d92)
   Building runregistrykit @ git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92
      Built runregistrykit @ git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92
Prepared 1 package in 2.56s
Installed 1 package in 2ms
 + runregistrykit==0.1.0 (from git+https://github.com/ds283/RunRegistryKit@9f8ebe431503fb8c79ee1407cc460501f1ca2d92)
+(eval):11> echo 'EXIT core 0'
EXIT core 0
```

What was installed, by `check_release.py` (a scratch script) run with `-I` from an empty
directory:

```text
=== pin-low
python 3.12.15
runregistrykit 0.1.0 <scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py
datastorekit 0.4.0
ray 2.43.0
sqlalchemy 2.0.39
direct_url {"url": "https://github.com/ds283/RunRegistryKit", "vcs_info": {"commit_id": "9f8ebe431503fb8c79ee1407cc460501f1ca2d92", "requested_revision": "v0.1.0", "vcs": "git"}}
RECORD entries 14
   runregistrykit-0.1.0.dist-info/INSTALLER
   runregistrykit-0.1.0.dist-info/METADATA
   runregistrykit-0.1.0.dist-info/RECORD
   runregistrykit-0.1.0.dist-info/REQUESTED
   runregistrykit-0.1.0.dist-info/WHEEL
   runregistrykit-0.1.0.dist-info/direct_url.json
   runregistrykit-0.1.0.dist-info/licenses/LICENSE
   runregistrykit-0.1.0.dist-info/top_level.txt
   runregistrykit-0.1.0.dist-info/uv_build.json
   runregistrykit/__init__.py
   runregistrykit/__main__.py
   runregistrykit/client.py
   runregistrykit/fingerprint.py
   runregistrykit/stores.py
tests in RECORD: []
import runregistrykit.tests: ModuleNotFoundError No module named 'runregistrykit.tests'
requires ['datastorekit>=0.4.0; extra == "stores"']
=== pin-high
python 3.13.16
runregistrykit 0.1.0 <scratch>/pin-high/lib/python3.13/site-packages/runregistrykit/__init__.py
datastorekit 0.4.0
ray 2.55.1
sqlalchemy 2.0.46
direct_url {"url": "https://github.com/ds283/RunRegistryKit", "vcs_info": {"commit_id": "9f8ebe431503fb8c79ee1407cc460501f1ca2d92", "requested_revision": "v0.1.0", "vcs": "git"}}
RECORD entries 14
   runregistrykit-0.1.0.dist-info/INSTALLER
   runregistrykit-0.1.0.dist-info/METADATA
   runregistrykit-0.1.0.dist-info/RECORD
   runregistrykit-0.1.0.dist-info/REQUESTED
   runregistrykit-0.1.0.dist-info/WHEEL
   runregistrykit-0.1.0.dist-info/direct_url.json
   runregistrykit-0.1.0.dist-info/licenses/LICENSE
   runregistrykit-0.1.0.dist-info/top_level.txt
   runregistrykit-0.1.0.dist-info/uv_build.json
   runregistrykit/__init__.py
   runregistrykit/__main__.py
   runregistrykit/client.py
   runregistrykit/fingerprint.py
   runregistrykit/stores.py
tests in RECORD: []
import runregistrykit.tests: ModuleNotFoundError No module named 'runregistrykit.tests'
requires ['datastorekit>=0.4.0; extra == "stores"']
=== pin-core
python 3.12.15
runregistrykit 0.1.0 <scratch>/pin-core/lib/python3.12/site-packages/runregistrykit/__init__.py
datastorekit absent find_spec: None
ray absent find_spec: None
sqlalchemy absent find_spec: None
direct_url {"url": "https://github.com/ds283/RunRegistryKit", "vcs_info": {"commit_id": "9f8ebe431503fb8c79ee1407cc460501f1ca2d92", "requested_revision": "v0.1.0", "vcs": "git"}}
RECORD entries 14
   runregistrykit-0.1.0.dist-info/INSTALLER
   runregistrykit-0.1.0.dist-info/METADATA
   runregistrykit-0.1.0.dist-info/RECORD
   runregistrykit-0.1.0.dist-info/REQUESTED
   runregistrykit-0.1.0.dist-info/WHEEL
   runregistrykit-0.1.0.dist-info/direct_url.json
   runregistrykit-0.1.0.dist-info/licenses/LICENSE
   runregistrykit-0.1.0.dist-info/top_level.txt
   runregistrykit-0.1.0.dist-info/uv_build.json
   runregistrykit/__init__.py
   runregistrykit/__main__.py
   runregistrykit/client.py
   runregistrykit/fingerprint.py
   runregistrykit/stores.py
tests in RECORD: []
import runregistrykit.tests: ModuleNotFoundError No module named 'runregistrykit.tests'
requires ['datastorekit>=0.4.0; extra == "stores"']
```

The five modules against `9f8ebe4` (`git show 9f8ebe4:runregistrykit/<m>.py | cmp - <site-packages>/runregistrykit/<m>.py`, each silent; the first 16 hex digits of each file's SHA-256):

```text
pin-low __init__.py equal f6e672b15f647c68
pin-low __main__.py equal 485d08ec66419624
pin-low client.py equal b5caa644d7e2a147
pin-low fingerprint.py equal 6c1df435eacc0bae
pin-low stores.py equal 2187d6034cdf120f
__init__.py
__main__.py
__pycache__
client.py
fingerprint.py
stores.py
pin-high __init__.py equal f6e672b15f647c68
pin-high __main__.py equal 485d08ec66419624
pin-high client.py equal b5caa644d7e2a147
pin-high fingerprint.py equal 6c1df435eacc0bae
pin-high stores.py equal 2187d6034cdf120f
__init__.py
__main__.py
__pycache__
client.py
fingerprint.py
stores.py
pin-core __init__.py equal f6e672b15f647c68
pin-core __main__.py equal 485d08ec66419624
pin-core client.py equal b5caa644d7e2a147
pin-core fingerprint.py equal 6c1df435eacc0bae
pin-core stores.py equal 2187d6034cdf120f
__init__.py
__main__.py
__pycache__
client.py
fingerprint.py
stores.py
```

`git rev-parse 9f8ebe4 v0.1.0^{} v0.1.0`: `9f8ebe431503fb8c79ee1407cc460501f1ca2d92` twice, then
`fd5ce4806a3cea09a27d92d5d811600c62dac376`. `git diff --stat 9f8ebe4 HEAD -- runregistrykit
pyproject.toml`: empty, before and after.

**CI**, read only:

```text
$ gh run view <id> --json databaseId,headSha,conclusion,status,event,jobs --jq …
38754093289 9f8ebe4 push completed/success core (no store layer)=success, suite (high)=success, suite (low)=success
38755672939 4ee947b push completed/success suite (low)=success, core (no store layer)=success, suite (high)=success
38768740409 dca5ead push completed/success core (no store layer)=success, suite (high)=success, suite (low)=success
38787646775 aaa1d6d push completed/success core (no store layer)=success, suite (low)=success, suite (high)=success
```

**`README.md`'s public names** against each module's `__all__`, in the low pin venv (a scratch
script parsing "The public names"):

```text
runregistrykit 20 README equals __all__: True
runregistrykit.stores 26 README equals __all__: True
runregistrykit.client 4 README equals __all__: True
runregistrykit.fingerprint 4 README equals __all__: True
runregistrykit.__main__ 1 README equals __all__: True
```

### 8. The offline rebuild

```bash
git archive v0.1.0 | tar -x -C <scratch>/export-v010
TMPDIR=<scratch>/tmp/uv uv build --wheel --offline --out-dir <scratch>/dist-offline <scratch>/export-v010
```

Exit 0; no "absent from" in the log (`grep -c` 0); the build environment's Python was 3.14 (its
egg-info, `runregistrykit-0.1.0-py3.14.egg-info`). `runregistrykit-0.1.0-py3-none-any.whl`, 54,940
bytes, SHA-256 `81a0ebb6b442917803df95413459cb6deaeea43c4e610051de38127d474339dd`; `unzip -l`:

```text
Archive:  <scratch>/dist-offline/runregistrykit-0.1.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
    35289  10-15-2026 14:31   runregistrykit/__init__.py
    22237  10-15-2026 14:31   runregistrykit/__main__.py
    11651  10-15-2026 14:31   runregistrykit/client.py
    10568  10-15-2026 14:31   runregistrykit/fingerprint.py
    93300  10-15-2026 14:31   runregistrykit/stores.py
    11357  10-15-2026 19:00   runregistrykit-0.1.0.dist-info/licenses/LICENSE
      304  10-15-2026 19:00   runregistrykit-0.1.0.dist-info/METADATA
       91  10-15-2026 19:00   runregistrykit-0.1.0.dist-info/WHEEL
       15  10-15-2026 19:00   runregistrykit-0.1.0.dist-info/top_level.txt
      849  10-15-2026 19:00   runregistrykit-0.1.0.dist-info/RECORD
---------                     -------
   185661                     10 files
```

Its five modules equal `9f8ebe4`'s (`zipfile` against `git show`, each `True`); `METADATA` as 06's
(`Version: 0.1.0`, `Requires-Python: >=3.12`, `License-File: LICENSE`, `Provides-Extra: stores`,
`Requires-Dist: datastorekit>=0.4.0; extra == "stores"`). The hash differs from 06's `9c01e7c9…`:
the modules carry the tag commit's time (14:31 UTC, 2026-10-15 15:31:31 +0100) and the `dist-info`
entries the build's (19:00 UTC).

### 9. The records, and how each count was made

- **Commits**: `git log --reverse --format='%h %ad %s'` (45 lines); classed by a scratch `awk` on
  the subject's form ("Write extraction prompt" 11, "Write the orchestration note" 11, "Record the
  orchestrator's review" 10, "Record the CI run" 1, the start and the plan 2, the other 10 the
  prompts' own, each of the ten listed and checked against §1 of the board). Total 45.
- **Deviation entries**: a scratch script split each log's "Deviations from the prompt" section at
  its top-level numbered items and found the labels in each with its lines joined; then every entry
  of every log was read, and the script's two misreadings corrected by reading (05c's "No
  **UNINTENDED DRIFT**", after its entry 15, is not a label of 15; the "As found" entries carry no
  label). Per log (entries; SR / IC / UD; unlabelled): 01 13; 1 / 11 / 1. 02 10; 2 / 8 / 0. 03 21;
  8 / 13 / 0. 04a 22; 6 / 17 / 0 (entry 14 both). 04b 17; 5 / 9 / 0; 3 (4, 7, 9). 05a 20; 3 / 11 /
  0; 6 (7-11, 20). 05b 17; 7 / 10 / 0. 05c 15; 6 / 9 / 0 (entry 1 both); 1 (15). 06 17; 10 / 7 / 0.
  07 25; 13 / 11 / 2 (entry 6 both). Total 177 entries; 61 / 106 / 3; 10 unlabelled; 3 with two
  labels (61 + 106 + 3 + 10 - 3 = 177).
- **Observations**: each log's section, item by item, read: 01 5, 02 6, 03 7, 04a 7, 04b 5, 05a 5,
  05b 6, 05c 4, 06 5, 07 7 = 57. Each disposition checked against the later logs, the board and, for
  "still an observation", the code at `9f8ebe4` (`DEFAULT_STALE_AFTER` named by no test;
  `import runregistrykit` still at `test_store_command_line.py:15` and `test_store_fingerprint.py:29`
  and used by neither; `git_provenance(os.getcwd())` at `stores.py:1352`; `write_listing` at
  `__main__.py:338`, outside the `try`). Tallied from the document's table: 17 addressed, 2 opened
  and closed, 3 handed to SGK's checklist, 1 measured here, 1 no action, 1 no longer the point, 32
  still observations.
- **Issues**: 13, from the board's §3 (2) and §4 (11), each entry's "Opened" and "Closed" lines; 7
  at planning (the §3 preamble). The index counts 2.
- **Decisions**: 9 of the user's carried from SGK (D1, D3, D4, Q1-Q5, Q7), U1-U24 (24), and 07's
  ruling: 34. Each "taken" date and prompt from README §6.2; each "recorded" commit is the prompt's
  writing commit that recorded it (`git show --stat` of each touches the campaign README).
- **The suite's history**: the board's §1 column, each checked against its log's result line.
- **Lines**: every `path:line` the document cites was printed by a scratch script at its tree
  (`9f8ebe4` for `runregistrykit/`, this commit's tree for `README.md` and `PROVENANCE.md`) and read
  against what the document says of it (Verification 11).

### 10. The smoke runs

From this repository's root, each in its pin venv with its own `TMPDIR`; the script's SHA-256
`1e0eafa5e667890d3ae3ac26fe21759c7ba23be2327e46174efec1dad5fa7fcf`, the committed file's;
`pgrep` before and after each, recorded in the output's `##` lines (exit 1: no process). Verbatim.

**Low end**, exit 0:

```text
## ray before: exit 1 
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
real 8.64
user 6.29
sys 1.55
## exit 0
## ray after: exit 1 
```

**High end**, exit 0:

```text
## ray before: exit 1 
python          3.13.16 (<scratch>/pin-high/bin/python)
runregistrykit  0.1.0 (<scratch>/pin-high/lib/python3.13/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.55.1
sqlalchemy      2.0.46
directory       $SMOKE = <scratch>/tmp/smoke-high/store-smoke-o71yox9n

PASS step 1: a store written by the client's module, and `store create --purpose`
  written: smoke-store-shard0000.sqlite, smoke-store-shard0001.sqlite, smoke-store.sqlite
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id 17e0fca38331460bbbafea028e743c4f
PASS step 2: a run that takes a fingerprint of its results store
  begin(): smoke-02-fingerprinted-20261015T201353
  known(): ['u1']
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > manifest packages: ['datastorekit', 'runregistrykit']
PASS step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261015T201353  done            1/1       1s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished.
PASS step 4: `store show`: a registry sidecar, no problems, the run naming the store
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > kind:     registry
    > problems: none
    > smoke-02-fingerprinted-20261015T201353  done      finished  by results and results_store_id
PASS step 5: `store fingerprint`: the recorded fingerprint matched by a fresh one
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > digest:   e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > format:   1
    > recorded: matches the fingerprint taken 2026-10-15T20:13:53+01:00 by run smoke-02-fingerprinted-20261015T201353, at 04906ee07005e15bb550a6cd42ecc7122f0fc055
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
    > completed: 2026-10-15T20:14:00+01:00
    > problems: none
PASS step 10: a run begun in a linked worktree, recorded under the main checkout
  git worktree add --detach worktree
  begin(): smoke-10-worktree-20261015T201400
    > run directory: $SMOKE/client/var/runs/smoke-10-worktree-20261015T201400
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
time: 9.5 s
left in place: <scratch>/tmp/smoke-high/store-smoke-o71yox9n
RESULT: OK (11 steps passed)
real 9.88
user 6.46
sys 1.48
## exit 0
## ray after: exit 1 
```

**Core-only venv**, exit 1 (breakage (c)):

```text
## ray before: exit 1 
python          3.12.15 (<scratch>/pin-core/bin/python)
runregistrykit  0.1.0 (<scratch>/pin-core/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    not installed
ray             not installed
sqlalchemy      not installed
directory       $SMOKE = <scratch>/tmp/smoke-core/store-smoke-9d5w7b11

FAIL step 1: a store written by the client's module, and `store create --purpose`
  !! ModuleNotFoundError: No module named 'sqlalchemy' (smoke_registry.py:7)
FAIL step 2: a run that takes a fingerprint of its results store
  begin(): smoke-02-fingerprinted-20261015T201401
  known(): ['u1']
    > status: state done, exit_code 0, fingerprint_sidecar None
    > fingerprint_error: ConfigError: $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:FINGERPRINTER': the module 'smoke_registry' could not be imported (ModuleNotFoundError: No module named 'sqlalchemy')
    > digest: None
    > manifest packages: ['datastorekit', 'runregistrykit']
  !! expected no fingerprint_error; saw ConfigError: $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:FINGERPRINTER': the module 'smoke_registry' could not be imported (ModuleNotFoundError: No module named 'sqlalchemy')
PASS step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261015T201401  done            1/1       1s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished.
FAIL step 4: `store show`: a registry sidecar, no problems, the run naming the store
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > kind:     absent
    > problems: none
    > smoke-02-fingerprinted-20261015T201401  done      finished  by results
  !! expected kind registry; saw another
FAIL step 5: `store fingerprint`: the recorded fingerprint matched by a fresh one
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    | !! $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:FINGERPRINTER': the module 'smoke_registry' could not be imported (ModuleNotFoundError: No module named 'sqlalchemy')
  !! exit 0 from `store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite`; saw exit 1
FAIL step 6: `store copy --purpose` of the store, and `store move` of the copy
  $ python -m runregistrykit store copy $SMOKE/client/var/datastores/smoke-store.sqlite $SMOKE/client/var/datastores/smoke-copy.sqlite --purpose a smoke copy   (in client/)
    exit 1
    | !! Cannot copy "$SMOKE/client/var/datastores/smoke-store.sqlite": its sidecar "$SMOKE/client/var/datastores/smoke-store.manifest.json" is not a problem-free registry sidecar (there is none). Run `python -m runregistrykit store create` or `store adopt` on it first; copy never upgrades a sidecar implicitly. Nothing was written
  !! exit 0 from `store copy $SMOKE/client/var/datastores/smoke-store.sqlite $SMOKE/client/var/datastores/smoke-copy.sqlite --purpose a smoke copy`; saw exit 1
FAIL step 7: `store amend --field x_note --remove` of a field written by hand
  !! FileNotFoundError: [Errno 2] No such file or directory: '$SMOKE/client/var/datastores/smoke-moved.manifest.json' (pathlib.py:1013)
FAIL step 8: `store adopt` of a store whose sidecar is a legacy object
  !! ModuleNotFoundError: No module named 'sqlalchemy' (smoke_registry.py:7)
FAIL step 9: `store retire --dry-run`, `store retire` and `store show` of the moved copy
  !! FileNotFoundError: [Errno 2] No such file or directory: '$SMOKE/client/var/datastores' (pathlib.py:1056)
PASS step 10: a run begun in a linked worktree, recorded under the main checkout
  git worktree add --detach worktree
  begin(): smoke-10-worktree-20261015T201402
    > run directory: $SMOKE/client/var/runs/smoke-10-worktree-20261015T201402
    > manifest script: $SMOKE/worktree/job.py
PASS step 11: the refusals: no fingerprinter named, and no config at all
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in no-fingerprinter/)
    exit 1
    > !! $SMOKE/no-fingerprinter/runregistrykit.toml names no fingerprinter, and the store layer requires one. Add [stores] with fingerprinter = "module:attribute", naming the client's Fingerprinter (runregistrykit.fingerprint), such as a DatastoreKitFingerprinter of its registry and its format number
  $ python -m runregistrykit list   (in elsewhere/)
    exit 1
    > !! No runregistrykit.toml in $SMOKE/elsewhere or any directory above it. Create one at the client's root; an empty file takes the defaults (runs_root = "var/runs", stores_root = "var/datastores", distributions = [])

ray: not imported
time: 1.1 s
left in place: <scratch>/tmp/smoke-core/store-smoke-9d5w7b11
RESULT: FAIL (1, 2, 4, 5, 6, 7, 8, 9)
real 1.21
user 0.58
sys 0.39
## exit 1
## ray after: exit 1 
```

**It cannot start**, exit 2:

```text
$ env PATH=/nonexistent TMPDIR=… pin-low/bin/python docs/extraction/store_smoke_run.py
CANNOT START: no git on PATH
exit 2
$ TMPDIR=… /opt/local/bin/python3.12 -I docs/extraction/store_smoke_run.py
CANNOT START: runregistrykit is not importable (No module named 'runregistrykit')
exit 2
```

### 11. The documents' checks

- **Links** (a scratch script: every Markdown link outside fenced blocks; a relative one resolved
  from `docs/`, its anchor matched against the target's headings; an external one required to start
  `https://github.com/ds283/` and name a tag, a commit or a run):

  ```text
  ok  ../prompts/extraction/README.md
  ok  ../prompts/extraction/IMPLEMENTATION_STATE.md
  ok  ../prompts/extraction/08-verification-and-close-out.md
  ok  ../prompts/extraction/logs/08-verification-and-close-out.md
  ok  https://github.com/ds283/RunRegistryKit/tree/v0.1.0
  ok  https://github.com/ds283/RunRegistryKit/commit/9f8ebe431503fb8c79ee1407cc460501f1ca2d92
  ok  https://github.com/ds283/RunRegistryKit/actions/runs/38754093289
  ok  extraction/store_smoke_run.py
  ok  adoption/secondarygwkit.md
  ok  https://github.com/ds283/RunRegistryKit/actions/runs/38754093289
  ok  https://github.com/ds283/RunRegistryKit/actions/runs/38754093289
  ok  https://github.com/ds283/RunRegistryKit/actions/runs/38755672939
  ok  https://github.com/ds283/RunRegistryKit/actions/runs/38768740409
  ok  https://github.com/ds283/RunRegistryKit/actions/runs/38787646775
  ok  extraction/store_smoke_run.py
  ok  https://github.com/ds283/DatastoreKit/tree/v0.4.0
  ok  adoption/secondarygwkit.md
  17 links: 8 relative, 9 external; 0 bad
  ```

- **`path:line`**: every citation in the document printed at its tree and read (README `:93-100`,
  `:143-145`, `:154-156`, `:161`, `:181-183`; `PROVENANCE.md:17-21`; `stores.py:1142-1144`,
  `:1352`, `:1409-1410`, with `:1677` and `:1727` by `grep`; `__main__.py:338`;
  `fingerprint.py:192-193`; `shard_store_fixtures.py:30-43`; `store_fixtures.py:160-167`;
  `test_store_retire.py:802`; `test_store_command_line.py:15`; `test_store_fingerprint.py:29`).
  `stores.py:1663` is cited as 03's line at the time, from 03's log.
- **The guard's word scans over the script** (`scan_code_names`, `scan_strings`, `scan_comments`
  and `scan_citations` of `test_package_is_generic`, run on the file by a scratch script; the guard
  itself covers only `runregistrykit/`): no code-name, string or comment hit; the citation scan finds
  the script's own citations of this campaign (`prompt 08`, `U23`, `U24`, lines 3-4), as the two
  sibling scripts cite theirs. No client is named.

### 12. The state at the end

The clients, by the same commands, unchanged from the start (`diff` of the two tables, less their time lines, empty):

Taken Thu Oct 15 20:34:43 BST 2026:

| Repository | Branch | HEAD | status lines | status shasum | stash | worktrees |
|---|---|---|---|---|---|---|
| SecondaryGWKit | handover-remedial | 14bcac0eb73069131f8ce4f55d91e5fc3e7318cf | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |
| ChamPBH | main | c21cdfb5613a3ed976a91a95431495dc8bfd49c8 | 22 | fbd525ec2b83137d7cd2d40b515a612919485205 | 0 | 1 |
| StochasticInstantons | dk-and-rpk-migration | 5fb4a1d71a016f1b23393923b9a3d59972415aa0 | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |
| DatastoreKit | main | b01737f139e5d8785ff915a929b9bd1b384ec840 | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |
| RayPoolKit | main | 17029d99bb2635ff7ce9b99b11e9c5f77d8b6967 | 0 | da39a3ee5e6b4b0d3255bfef95601890afd80709 | 0 | 1 |

This repository: `git worktree list` shows this checkout alone; no Ray process; `/private/tmp`'s
names beginning `tmp` or `ray` and `/private/tmp/ray`'s modification time as at the start
(deviation 9). The scratch clones, venvs, client roots and outputs are under
`<scratch>` (`agent-08/`), not removed.

## The deliberate-breakage record

Each (a) and (b) diff below was applied with `git apply` in `<scratch>/breakage/clone` (a `git clone`
of `302faac` with this commit's script copied in), run there in the low pin venv, and reversed; the
script compared equal to this commit's after each reverse (`cmp`), and `git status` here was
unchanged. Each diff, as recorded here, was extracted from this log by a scratch script and checked
with `git apply --check` and `git apply -R --check` (the latter after applying), in `bash`, in a
fresh scratch clone (below, "The diffs, checked as recorded").

### (a) The config names the class

```diff
--- a/docs/extraction/store_smoke_run.py
+++ b/docs/extraction/store_smoke_run.py
@@ -82,7 +82,7 @@
 distributions = ["datastorekit"]
 
 [stores]
-fingerprinter = "smoke_registry:FINGERPRINTER"
+fingerprinter = "smoke_registry:DatastoreKitFingerprinter"
 """
 
 GITIGNORE = "var/\n"
```

Exit 1, `RESULT: FAIL (2, 5, 9)`. Verbatim:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.1.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
directory       $SMOKE = <scratch>/tmp/break-a/store-smoke-vo_l8joh

PASS step 1: a store written by the client's module, and `store create --purpose`
  written: smoke-store-shard0000.sqlite, smoke-store-shard0001.sqlite, smoke-store.sqlite
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id ce42034140264496a6ed642ec37aee58
FAIL step 2: a run that takes a fingerprint of its results store
  begin(): smoke-02-fingerprinted-20261015T201439
  known(): ['u1']
    > status: state done, exit_code 0, fingerprint_sidecar None
    > fingerprint_error: ConfigError: $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:DatastoreKitFingerprinter' is the class DatastoreKitFingerprinter, not an instance of it: name an instance, made in a module of the client's (for DatastoreKitFingerprinter, one made with the client's registry and its format number)
    > digest: None
    > manifest packages: ['datastorekit', 'runregistrykit']
  !! expected no fingerprint_error; saw ConfigError: $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:DatastoreKitFingerprinter' is the class DatastoreKitFingerprinter, not an instance of it: name an instance, made in a module of the client's (for DatastoreKitFingerprinter, one made with the client's registry and its format number)
PASS step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261015T201439  done            1/1       1s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished.
PASS step 4: `store show`: a registry sidecar, no problems, the run naming the store
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > kind:     registry
    > problems: none
    > smoke-02-fingerprinted-20261015T201439  done      finished  by results and results_store_id
FAIL step 5: `store fingerprint`: the recorded fingerprint matched by a fresh one
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    | !! $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:DatastoreKitFingerprinter' is the class DatastoreKitFingerprinter, not an instance of it: name an instance, made in a module of the client's (for DatastoreKitFingerprinter, one made with the client's registry and its format number)
  !! exit 0 from `store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite`; saw exit 1
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
FAIL step 9: `store retire --dry-run`, `store retire` and `store show` of the moved copy
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy --dry-run   (in client/)
    exit 1
    | !! $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:DatastoreKitFingerprinter' is the class DatastoreKitFingerprinter, not an instance of it: name an instance, made in a module of the client's (for DatastoreKitFingerprinter, one made with the client's registry and its format number)
  !! exit 0 from `store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy --dry-run`; saw exit 1
PASS step 10: a run begun in a linked worktree, recorded under the main checkout
  git worktree add --detach worktree
  begin(): smoke-10-worktree-20261015T201444
    > run directory: $SMOKE/client/var/runs/smoke-10-worktree-20261015T201444
    > manifest script: $SMOKE/worktree/job.py
PASS step 11: the refusals: no fingerprinter named, and no config at all
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in no-fingerprinter/)
    exit 1
    > !! $SMOKE/no-fingerprinter/runregistrykit.toml names no fingerprinter, and the store layer requires one. Add [stores] with fingerprinter = "module:attribute", naming the client's Fingerprinter (runregistrykit.fingerprint), such as a DatastoreKitFingerprinter of its registry and its format number
  $ python -m runregistrykit list   (in elsewhere/)
    exit 1
    > !! No runregistrykit.toml in $SMOKE/elsewhere or any directory above it. Create one at the client's root; an empty file takes the defaults (runs_root = "var/runs", stores_root = "var/datastores", distributions = [])

ray: imported, initialised: False
time: 6.8 s
left in place: <scratch>/tmp/break-a/store-smoke-vo_l8joh
RESULT: FAIL (2, 5, 9)
```

`store retire` without `--dry-run`, by hand in the left client root (deviation 14):

```text
== (a) in $SMOKE/client: before: smoke-moved-shard0000.sqlite smoke-moved-shard0001.sqlite smoke-moved.manifest.json smoke-moved.sqlite 
!! $SMOKE/client/runregistrykit.toml: [stores] fingerprinter 'smoke_registry:DatastoreKitFingerprinter' is the class DatastoreKitFingerprinter, not an instance of it: name an instance, made in a module of the client's (for DatastoreKitFingerprinter, one made with the client's registry and its format number)
exit 1
after: smoke-moved-shard0000.sqlite smoke-moved-shard0001.sqlite smoke-moved.manifest.json smoke-moved.sqlite 
```

The steps that load the fingerprinter fail on the loader's refusal naming the class: step 2 (the
run `done`, `fingerprint_error` the `ConfigError`), step 5 (`store fingerprint`, exit 1) and step 9
(`store retire`, with and without `--dry-run`, exit 1, nothing deleted). The steps that only check
that one is named (`create`, `show`, `copy`, `move`, `amend`, `adopt`) pass. As §4.5 says.

### (b) One row changed after the fingerprint

```diff
--- a/docs/extraction/store_smoke_run.py
+++ b/docs/extraction/store_smoke_run.py
@@ -473,7 +473,16 @@
         )
         self.digests.append(("status.json", digest))
         self.run_id = run.id
+        # breakage (b): one row of the store changed after its fingerprint was taken
+        shard = self.primary.with_name(self.primary.stem + "-shard0000.sqlite")
+        import sqlite3
 
+        conn = sqlite3.connect(shard)
+        with conn:
+            conn.execute("UPDATE Point SET x = x + 0.25 WHERE serial = 1")
+        conn.close()
+        self.say(f"  (b) UPDATE Point SET x = x + 0.25 WHERE serial = 1 on {shard.name}")
+
     def step_3(self):
         """`list`: one run, finished"""
         result = self.command("list")
@@ -502,6 +511,14 @@
 
     def step_5(self):
         """`store fingerprint`: the recorded fingerprint matched by a fresh one"""
+        # breakage (b): what `store retire` does with the changed store
+        before = self.store_files(self.primary)
+        result = self.command(
+            "store", "retire", self.primary, "--reason", "breakage (b)", expect=1
+        )
+        self.show_lines(result.stderr, "!!")
+        kept = self.store_files(self.primary)
+        self.say(f"  (b) files kept: {before == kept}, {[p.name for p in kept]}")
         result = self.command("store", "fingerprint", self.primary)
         found = self.show_lines(result.stdout, "digest:", "format:", "recorded:")
         digest = [line.split()[1] for line in found if line.startswith("digest:")]
```

Exit 1, `RESULT: FAIL (5, 9)`. Verbatim:

```text
python          3.12.15 (<scratch>/pin-low/bin/python)
runregistrykit  0.1.0 (<scratch>/pin-low/lib/python3.12/site-packages/runregistrykit/__init__.py)
datastorekit    0.4.0
ray             2.43.0
sqlalchemy      2.0.39
directory       $SMOKE = <scratch>/tmp/break-b/store-smoke-iihbd1c6

PASS step 1: a store written by the client's module, and `store create --purpose`
  written: smoke-store-shard0000.sqlite, smoke-store-shard0001.sqlite, smoke-store.sqlite
  $ python -m runregistrykit store create $SMOKE/client/var/datastores/smoke-store.sqlite --purpose the smoke run's store   (in client/)
    exit 0
    > >> create: $SMOKE/client/var/datastores/smoke-store.manifest.json
    > sidecar_format 1, store_id 85c8ab077a694c3e97de724f9c342b7f
PASS step 2: a run that takes a fingerprint of its results store
  begin(): smoke-02-fingerprinted-20261015T201513
  known(): ['u1']
    > status: state done, exit_code 0, fingerprint_sidecar 'written'
    > digest: e56c6922d9b7027eaa0b7e7272ccea4743f85d373fdc164d8c771b334da94069
    > manifest packages: ['datastorekit', 'runregistrykit']
  (b) UPDATE Point SET x = x + 0.25 WHERE serial = 1 on smoke-store-shard0000.sqlite
PASS step 3: `list`: one run, finished
  $ python -m runregistrykit list   (in client/)
    exit 0
    > smoke-02-fingerprinted-20261015T201513  done            1/1       1s  a smoke run that fingerprints its results store  · working
    > 1 run(s) under $SMOKE/client/var/runs: 1 finished.
PASS step 4: `store show`: a registry sidecar, no problems, the run naming the store
  $ python -m runregistrykit store show $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 0
    > kind:     registry
    > problems: none
    > smoke-02-fingerprinted-20261015T201513  done      finished  by results and results_store_id
FAIL step 5: `store fingerprint`: the recorded fingerprint matched by a fresh one
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-store.sqlite --reason breakage (b)   (in client/)
    exit 1
    > !! Cannot retire "$SMOKE/client/var/datastores/smoke-store.sqlite": its content does not match the fingerprint its sidecar records, taken 2026-10-15T20:15:13+01:00: 1 difference(s): Point: tag set [] differs: 3 recorded, 3 now. Nothing was written or deleted
  (b) files kept: True, ['smoke-store-shard0000.sqlite', 'smoke-store-shard0001.sqlite', 'smoke-store.sqlite']
  $ python -m runregistrykit store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite   (in client/)
    exit 1
    |                    2  c7ffdb8b669a  []
    |   Point            3  a8aaa6c87e8e
    |                    3  a8aaa6c87e8e  []
    | problems: none
    | recorded: 1 difference(s) from the recorded fingerprint:
    |   !! Point: tag set [] differs: 3 recorded, 3 now
  !! exit 0 from `store fingerprint $SMOKE/client/var/datastores/smoke-store.sqlite`; saw exit 1
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
FAIL step 9: `store retire --dry-run`, `store retire` and `store show` of the moved copy
  $ python -m runregistrykit store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy --dry-run   (in client/)
    exit 1
    | !! Cannot retire "$SMOKE/client/var/datastores/smoke-moved.sqlite": its content does not match the fingerprint its sidecar records, taken 2026-10-15T20:15:13+01:00: 1 difference(s): Point: tag set [] differs: 3 recorded, 3 now. Nothing was written or deleted
  !! exit 0 from `store retire $SMOKE/client/var/datastores/smoke-moved.sqlite --reason the smoke run retires its moved copy --dry-run`; saw exit 1
PASS step 10: a run begun in a linked worktree, recorded under the main checkout
  git worktree add --detach worktree
  begin(): smoke-10-worktree-20261015T201520
    > run directory: $SMOKE/client/var/runs/smoke-10-worktree-20261015T201520
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
time: 8.3 s
left in place: <scratch>/tmp/break-b/store-smoke-iihbd1c6
RESULT: FAIL (5, 9)
```

`store retire` of the moved copy without `--dry-run`, by hand in the left client root:

```text
== (b) in $SMOKE/client: before: smoke-moved-shard0000.sqlite smoke-moved-shard0001.sqlite smoke-moved.manifest.json smoke-moved.sqlite 
!! Cannot retire "$SMOKE/client/var/datastores/smoke-moved.sqlite": its content does not match the fingerprint its sidecar records, taken 2026-10-15T20:15:13+01:00: 1 difference(s): Point: tag set [] differs: 3 recorded, 3 now. Nothing was written or deleted
exit 1
after: smoke-moved-shard0000.sqlite smoke-moved-shard0001.sqlite smoke-moved.manifest.json smoke-moved.sqlite 
```

`store retire` of the changed store exits 1, "its content does not match the fingerprint its
sidecar records … Nothing was written or deleted", every file kept; `store fingerprint` exits 1
naming the class that differs (`Point`); the copy, made after the change and carrying the recorded
fingerprint, is refused the same way at step 9, with and without `--dry-run`. That is what
`README.md:181-183` says `retire` does. As §4.5 says.

### (c) The core-only venv

The committed script, unchanged, in `pin-core` (Verification 10, "Core-only venv"). Exit 1, `RESULT:
FAIL (1, 2, 4, 5, 6, 7, 8, 9)`; no exception escaped a step; `ray` never imported.

| Step | Needs | Verdict |
|---|---|---|
| 1 | a store: the client's writer imports SQLAlchemy | FAIL, `ModuleNotFoundError: No module named 'sqlalchemy'`, caught |
| 2 | a fingerprinter | FAIL: the run `done`, `fingerprint_error` the loader's `ConfigError` (the module could not be imported) |
| 3 | neither: step 2's run | PASS |
| 4 | a store | FAIL: `store show` exit 0, `kind: absent` |
| 5 | a store and a fingerprinter | FAIL: exit 1, the loader's refusal |
| 6 | a store | FAIL: `store copy` exit 1, no registry sidecar |
| 7 | step 6's store | FAIL: `FileNotFoundError`, caught |
| 8 | a store | FAIL: `ModuleNotFoundError`, caught |
| 9 | a store | FAIL: `FileNotFoundError` on `var/datastores`, caught |
| 10 | neither | PASS |
| 11 | neither | PASS |

### The diffs, checked as recorded

The two `diff` blocks above, extracted from this file by a scratch script (each equal, by `cmp`, to the diff applied for the runs), in a fresh `git clone` of `302faac` with this commit's script copied in, in `bash`:

```text
$ git apply --check from-log-a.diff
exit 0
applied: exit 0
$ git apply -R --check from-log-a.diff
exit 0
reversed: exit 0
the script equal to this commit's again
$ git apply --check from-log-b.diff
exit 0
applied: exit 0
$ git apply -R --check from-log-b.diff
exit 0
reversed: exit 0
the script equal to this commit's again
```

## Observations not acted on

1. **The board's §4 still says `[00-the-store-layer-reads-inside-a-fingerprint]` was closed "by 04a
   (this commit)"** (its "Closed" line); its "Resolved" paragraph gives `c81ad06`, which is right.
   Residue of 04a's follow-up; not in this prompt's §2.4, so left. The document gives `c81ad06`.
2. **The board's review of 04a counts 7 / 15**; 04a's log labels 6 / 17 by entry (deviation 18).
   Left; the document says which is right.
3. **`PROVENANCE.md:17-21`** still says the package's prose cites SGK "until prompt 05 rewrites
   them"; 05c, 06 and 07 left it for 08, which may not change the file (deviation 21). No issue
   opened: the document is written additively and its later sections say the prose was rewritten.
   For the orchestrator to put to the user if it should change.
4. **Ten deviation entries carry no class** (04b's three and 05a's six "As found", 05c's 15), where
   `CLAUDE.md` rule 2 asks for one of three; each review accepted them. Recorded in the document's §8.
5. **The planner's "about 5 s" is 8.4 s and 9.5 s here**, for the script's own store and a fresh git
   repository per run; nothing depends on it.
6. **In the core venv the manifest's `packages` names `datastorekit`** though it is not installed
   (the config names it; `package_provenance` records `None` for it, as 07's checklist for SI says).
   As designed.
7. **`store show` exits 0 for an absent sidecar** (`kind: absent`), as `__main__.py`'s comment says
   ("Any other sidecar exits 0 whatever it reads as"); the script's step 4 checks the kind.
8. **`uv build --offline` writes its build environment under `uv`'s cache** (deviation 9), the one
   write outside the scratchpad, made and removed by `uv`.

Nothing is opened: no defect of the package was found, and the count stays 2.

## State handed on

The campaign is **closed** (2026-10-15). Nothing follows 08 in it.
- The package is `v0.1.0`'s: `git diff 9f8ebe4 -- runregistrykit pyproject.toml` is empty. The suite
  is **276**.
- G2-G4 are open; each is recorded on the board when it holds, in a records commit of its own. E2
  holds.
- Open issues: **2** (`[00-the-shard-fixtures-reach-into-shardedpool]`,
  `[00-a-refusal-matches-datastorekit-message-text]`), owner none, requests to DatastoreKit.
- `docs/extraction/store_smoke_run.py` is the way to re-check the store layer against a release:
  with the release installed, `python docs/extraction/store_smoke_run.py`.
- **No tag made; nothing pushed.**
