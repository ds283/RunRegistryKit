# Prompt 06 — release `v0.2.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 05 has landed and been reviewed (`eb68583`; the review `4a10efb`; CI run `39129061916` green,
  recorded in `80974e2`).
- The user has taken **L10** as (a), `v0.2.0` (README §6.2, 2026-10-18): this prompt is written
  for it.
- `git diff --stat eb68583 HEAD -- runregistrykit pyproject.toml .github README.md docs` is empty:
  the package, the README and `docs/` are 05's.
- The suite is `Ran 410 tests … OK (skipped=1)` on macOS, and `git status` is clean in this
  repository.

**Closes:** nothing (no issue is assigned to 06). **Opens:** only what the work finds. **Narrows:**
nothing. The five open §3 entries are listed in the release notes as known issues (§2.4), and are
not changed.

**Recommended model:** **Opus**, as the plan says. Nothing under `runregistrykit/` changes. The
weight is in three documents that clients will act on: release notes that must say, field by
field, what every record now holds and what an older one means, and README and adoption text that
must be true of the package **as it will be tagged**. Every statement in them is checked against
the code and against a measurement, never against this prompt.

**Read first:**

1. [`README.md`](README.md): §0 and §0.1 (what changes in what the registry writes), §1, §2 (the
   rows 01–07), §4, §5 (rules 7, 8, 9 and 11 especially), §6.2 (L1–L11 with their notes) and §7.
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): the header, §1 with every orchestrator
   review, §3's five open entries, and §4's entries for the issues 01–05 closed.
3. The prompts 01–05 for the forms their decisions fixed, above all: 01's `host` records
   ([`01-the-host.md`](01-the-host.md)), 02's temporary name
   ([`02-status-writes.md`](02-status-writes.md)), 03's unreadable status
   ([`03-an-unreadable-status-is-in-use.md`](03-an-unreadable-status-is-in-use.md)), 04's §2.2,
   the `ended` record ([`04-end-a-run.md`](04-end-a-run.md)), and 05's refusal
   ([`05-begin-refuses-a-second-writer.md`](05-begin-refuses-a-second-writer.md)). Their logs
   say what shipped where it differs.
4. The repository as 05 left it: `pyproject.toml`; `README.md` in full; `PROVENANCE.md`'s opening;
   `.github/workflows/tests.yml`; `docs/adoption/README.md` and the three checklists beside it
   (§1, §4, §5 and §10 of each); the module docstrings of `runregistrykit/__init__.py`,
   `stores.py` and `__main__.py`; `python -m runregistrykit --help`, `list --help`, `end --help`
   and `store --help`.
5. [`prompts/extraction/06-release-v0.1.0.md`](../extraction/06-release-v0.1.0.md), the release
   prompt this one follows, for its release check (§2.4) and its record of how `v0.1.0` was tagged.
6. `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`, above all "Releases".
7. The clients, **read through `git` only, nothing run**, at the commits of §"At writing": SGK's
   `requirements.txt`, its drivers `docs/gktk-remedial/scoped_pipeline_run.py` and
   `docs/handover/quadsource_atol_sweep.py`, `RunDrivers/tests/` (the files that name
   `runregistrykit`), `docs/datastore-integrity-verification/interrupt_when.py`, and its stale-run
   brief `prompts/handover/runregistrykit-stale-run-brief.md`; CPBH's and SI's `requirements.txt`
   and a `git grep -i runregistrykit` of each.

Line numbers are at `80974e2`, whose package is `eb68583`'s.

---

## 1. What is wanted

06 makes the package ready to be released as **`v0.2.0`** (L10 (a)), the release the clients adopt
for an interrupted run. After it:

- `pyproject.toml` says `0.2.0`, and nothing else in it changes;
- `README.md` describes `v0.2.0`: the host, `foreign`, the earlier boot, an unreadable status,
  `end`, `lost`, and `begin`'s refusal, where its text for `v0.1.0` is now untrue or silent;
- **release notes**, `docs/releases/v0.2.0.md` (new), say field by field what the registry now
  writes, what a record written by `v0.1.0` means to `v0.2.0`, what a record written by `v0.2.0`
  means to `v0.1.0`, every change to the public interface, and the known issues;
- **adoption notes** for `v0.2.0`, in `docs/adoption/v0.2.0/` (new): what the three clients
  share, and one note per client measured at the commit it is read at; `docs/adoption/README.md`
  gains one section pointing at them, and nothing else in it changes;
- **the release check has passed on this machine**: a wheel built from an export of the commit
  installs, imports, says `0.2.0`, and ships no test module.

**No behaviour of the package changes.** No file under `runregistrykit/` or `.github/` is touched.
The suite stays at **410**.

**06 makes no tag and pushes nothing** (README §5 rule 11). After its review, the orchestrator puts
to the user, in this order (§7): pushing 06's commit **alone** to `main`, so that CI runs on that
commit itself; once all three jobs pass there, making the annotated tag `v0.2.0` **on 06's commit**
and pushing it; then pushing the review's records. If CI fails, a fix prompt lands first, since no
tag is made on a commit whose CI is red and none is moved.

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, `datastorekit` `v0.4.0`, `runregistrykit`
editable. **One change is allowed**, after §2.2: `./venv/bin/python -m pip install --no-deps -e .`,
so that the venv's metadata says `0.2.0` (a manifest records it, `package_provenance`). Record `pip
freeze` before and after: only `runregistrykit`'s line changes. Nothing else is installed into
`venv/`.

### 2.2 `pyproject.toml`

`version = "0.1.0"` → `version = "0.2.0"`. Nothing else: the range, the extra, the exclusion of
the tests and `include-package-data = false` are `v0.1.0`'s and stay. `git diff` of the file is one
line.

### 2.3 The README

Its opening paragraph, "Supported versions" (but for the sentence below), "Installing" (but for the
tag), "The rules" (but for rule 2's one sentence), "The public names" (but for `this_host`) and
"Licence" keep their text. Each change below is written **as of the tag**, read from the code, and
checked (§3.5). At `80974e2`:

| Where | Today | It becomes |
|---|---|---|
| `:12-18`, Status | "`v0.1.0`", the extraction, and the extraction campaign's links | `v0.2.0`: `v0.1.0`, the extraction, plus what an interrupted run needs (one sentence: the host and boot recorded, an unreadable status counted as in use, `end`, `begin`'s refusal); a link to the release notes; the extraction's links kept, and this campaign's README and board added |
| `:40-41` | "such as Python 3.14 and Ray 2.59.0 today" | the newest Ray on PyPI when this is written, if it can be read (`https://pypi.org/pypi/ray/json`), else unchanged; the sentence otherwise as it is |
| `:51`, `:62` | `@v0.1.0` | `@v0.2.0` |
| `:104-115`, A run | `begin` refuses a tombstone | also: it refuses a `results` store that a run which has not finished names, under the runs root it is created in, by path or `results_store_id` (05's words: `running` alive, stale or on another host, or a status that does not say), with no override; a check and not a lock. It records the host in the manifest and `id` and `boot` in `status.json` (`this_host()`; `RUNREGISTRYKIT_HOST_NAME` for the display name, read only) |
| `:123-126` | "`state` one of `done`, `failed` or `killed`" | the three a caller reports; `lost` is in `TERMINAL_STATES` and is the state `end` records (`finish`'s docstring) |
| after `:129` | — | one sentence: `status.json` is written through a temporary name of each write's own beside it (`status.json.<pid>-<n>-<hex>.tmp`), so a process killed mid-write can leave one; it is never read, and `status.json` is never torn |
| `:131-135`, `list` | alive iff pid and heartbeat; stale `!!` | the liveness values as `liveness` defines them (`alive`, `stale`, `foreign`, `finished`, `unknown`): a run on another host is `foreign`, marked `??`, its pid not tested; one on this host from an earlier boot is `stale`; a run with a manifest whose status cannot be read or does not say is marked `!!`; the summary counts records with no host; the remedy lines name `end` |
| new, after `list` | — | **Ending a run whose end was never recorded**: `python -m runregistrykit end RUN_ID --reason TEXT [--unverified] [--root DIR]`, from its `--help` and 04's checks: what it accepts and refuses (a live pid here refused with no override; another host or a status that does not say only with `--unverified`; a terminal run never), what it writes (`lost`, exit code `null`, an `ended` record, through the status writer; nothing else), and that the registry does not decide that a run is dead |
| `:180-184`, store layer | "refuses a store that a `running` run names" | a store that any run names whose status does not say it has finished, as `store --help` says |
| `:218-220`, rule 2 | the liveness rule | one sentence added after its first: it judges a run on the run's own host; a run recorded on another host is not judged here, and one from an earlier boot of this host is stale. The rule's *failure it answers* is unchanged |
| `:274-277`, the public names | the core's list | `this_host` added, in its place in the alphabetical list |
| `:292-296`, patch targets | `begin()` "calls `read_sidecar`" | `begin()` with `results` imports `runregistrykit.stores` and calls `read_sidecar` and the store operations' in-use check; the promise unchanged |
| `:186-191`, the interface | — | one sentence added: each release that changes a record says so in its release notes, `docs/releases/` |
| `:315-319`, CI | "the two test modules that need nothing else, `test_run_registry` and `test_public_names`" | the core's test modules the workflow names (seven at `80974e2`), by name |

**Nothing else in the README changes.** It names no client's script, store or campaign. Where the
table and the code disagree, the code is right: record the difference as a deviation.

### 2.4 The release notes, `docs/releases/v0.2.0.md`

A new file, written as of the tag. Its sections, in this order:

1. **What it is.** `v0.2.0`, on `v0.1.0`; the campaign that made it (this campaign's README and
   board, by link); the supported versions unchanged (a link to the README's section). One
   sentence on how a client adopts it: by moving its pin, in a commit of its own, after reading the
   adoption notes (§2.5).
2. **What the registry writes**, field by field, each with its type, when it is written, by what,
   and the prompt that added it. Measured, not copied from this prompt (§3.3):
   - the manifest's `host`: `id`, `name`, `machine`, `system`, `release`, `python`;
   - `status.json`'s `host`: `id`, `boot`, written by `begin` and carried by every later write;
   - `status.json` written by `end`: `state` `lost`, `exit_code` `null`, and `ended` with every key
     of 04's §2.2 (`at`, `by`, `reason`, `git_head`, `host`, `verified`,
     `not_verified_because`, `evidence` and its keys), each key's type and meaning as 04 fixes it,
     and the form written on a status that could not be read;
   - `status.json`'s temporary names (02), and that `status.json.tmp` is not one of them;
   - **unchanged**, said so explicitly: `checkpoint.jsonl`, the sidecar, the run directory's file
     set, and every key `v0.1.0` wrote, with its meaning.
   What `id` is (a digest, never the raw identity), what `boot` is, and what a `null` in either
   means, from `this_host()`'s docstring and 01's file, for macOS and Linux.
3. **What a record written by `v0.1.0` means to `v0.2.0`** (README §5 rule 8): with no `host`, or
   `host.id` `null`, judged by pid and heartbeat as `v0.1.0` judged it, and counted by `list` as
   having no host; `checkpoint.jsonl` and the sidecar read as before. And what changed in
   judgement on old records: a run whose status cannot be read, or does not say, now counts as in
   use (03); a status or manifest that is JSON but not an object is read as unreadable rather than
   raised on.
4. **What a record written by `v0.2.0` means to `v0.1.0`**, measured (§3.3): a client pinned at
   `v0.1.0` in one checkout may read a runs root `v0.2.0` writes in another. A table of what
   `v0.1.0`'s `liveness`, `list` and store operations make of: a `lost` run; a `foreign` run; a
   run from an earlier boot of this host; a run with an unreadable status; and what `v0.1.0`'s
   `begin` does on a store a `v0.2.0` run names. Say plainly what is lost: `v0.1.0` tests a
   `foreign` run's pid here, calls a `lost` run `unknown`, and does not refuse a second writer. The
   advice: every checkout that shares a runs root moves to `v0.2.0` together.
5. **The public interface**, every change, each named from `__all__` and its signature at both
   tags (§3.3): `TERMINAL_STATES` gains `lost`; `liveness` gains the value `foreign` and the
   keyword `here=`; `this_host` is new; `pid_alive` returns `False` for a pid outside the
   platform's range, where it raised; `list_runs`' entries gain `host`, `host_id`,
   `host_recorded` and `status_readable`; `begin` raises `RuntimeError` on a store a run that has
   not finished names; the store operations' refusals count every run whose status does not say
   it has finished, and their remedy names `end` in place of `Run.finish`; `list`'s markers and
   lines; the `end` command. And what a caller who compared refusal texts must re-read: the store
   operations' texts changed in their remedy sentence (04) and in what they count (03).
6. **Known issues**: the five open §3 entries of the board, one line each, with a link to the
   board's entry, and nothing that the board does not say.

**What the earlier prompts left for these notes.** Each log's "State handed to the next prompt" has
a "For 06" line, and every one is honoured; the log of 06 lists them, each with where the notes
say it:
- 01's (`logs/01-the-host.md:509`): `liveness` gains `foreign`, `this_host` is public, and what
  `host` means in each file: absent, written before 01; `null` values, the platform offered none;
- 02's (`logs/02-status-writes.md:586`) and 02b's (`:629`): "`write_json_atomic`: unchanged" (it
  keeps `<path>.tmp`, which every sidecar write uses), and `status.json` written through a name
  of its own with the mode `0666` less the umask;
- 03's (`03-an-unreadable-status-is-in-use.md:109`): `list_runs`' new key;
- 04's (`logs/04-end-a-run.md:608`): `lost`, `ended` and `TERMINAL_STATES`; the README's usage
  of `end`;
- 05's (`logs/05-begin-refuses-a-second-writer.md:617`): `pid_alive`'s value for a pid out of
  range, from raising to `False`.

No client is named in the release notes. The notes describe the package; the adoption notes
describe the clients.

### 2.5 The adoption notes, `docs/adoption/v0.2.0/`

**A note is data, not instructions** (`docs/adoption/README.md`'s rule): it describes a client at
one commit, read through `git`, and the client's own adoption campaign measures again. Four files:

- **`README.md`**, what the three share: the pin (`runregistrykit[stores] @
  git+…@v0.2.0` beside the client's own `datastorekit` line, as the README's "Installing"); that
  every checkout sharing a runs root moves together (§2.4.4); what a client's code must check —
  any comparison with `liveness`'s values, `TERMINAL_STATES`, a store refusal's text, a test that
  begins two unfinished runs on one store (05's six tests and their fixture are this repository's
  example, by link), and any caller of `pid_alive` that relied on its raising; the new route for a
  hard-killed run, `end` and then `begin`; the table of the three clients and the commit each was
  read at; the gates G1–G3 (README §7).
- **`secondarygwkit.md`**: SGK is on `v0.1.0` (`requirements.txt:81` at `79434bf`). Every place
  in its live code and tests that §2.5's README lists, found by `git grep` at the commit and cited
  `path:line`, with what `v0.2.0` changes for it, measured where this repository can measure it
  without running SGK (by building the same records in a scratch directory with this package) and
  read otherwise. At least: its drivers' `begin(..., results=…)` (`scoped_pipeline_run.py:544`,
  `quadsource_atol_sweep.py:556`, `:869`) and what `--build --resume` meets after a hard kill;
  its signal handlers' `finish("killed", …)`; `RunDrivers/tests/test_pipeline_adoption.py:252`'s
  assertion on `TERMINAL_STATES`; `test_quadsource_atol_sweep_prepare.py:194`'s refusal fragments
  against 05's texts; `interrupt_when.py`'s use of `liveness` and `pid_alive`; and each point of
  its stale-run brief, with the prompt of this campaign that answered it, or that none did. Its
  existing run directories read as having no host.
- **`champbh.md`** and **`stochasticinstantons.md`**: neither has adopted any release (each
  adopts after its `dk-and-rpk-migration` campaign). Each says that it adopts `v0.2.0` directly,
  that its `v0.1.0` checklist beside it (`../champbh.md`, `../stochasticinstantons.md`) still
  describes the move, with the pin `v0.2.0` in place of `v0.1.0` and §2.5's README's checks added,
  and what `git grep -i runregistrykit` finds at the commit read. SI's missing `datastorekit` line
  is restated from its checklist, not re-derived.

**`docs/adoption/README.md`** gains one section at its end, "`v0.2.0`", of a few lines: the new
directory, by link, and that the checklists above it were written against `v0.1.0` and are not
rewritten. Nothing above it changes (CLAUDE.md rule 6: documents under `docs/` are additive).

### 2.6 What does not change

- Every file under `runregistrykit/`, in the package and its tests; `.github/`; `PROVENANCE.md`
  (it records the import, and this campaign does not touch it); `CLAUDE.md`; `LICENSE`;
  `.gitignore`; the three `v0.1.0` checklists and `docs/adoption/measure_client_registry.py`;
  `docs/extraction/`; `docs/OPEN_ISSUES.md` unless the work opens an issue.
- What the registry writes: nothing (README §5 rule 7). The suite: 410.

---

## 3. Verification

1. **The suite**, `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the
   root, `TMPDIR` in your scratch: `Ran 410 tests … OK (skipped=1)` before §2.1's reinstall and
   after it. Per-module counts unchanged. No Ray process before or after.
2. **The release check**, as extraction 06's §2.4: a `git archive` of the working tree's commit
   into a new, empty scratch directory, the working `pyproject.toml` copied over it, `uv build
   --wheel` into a scratch `dist`, never a build in the repository. The wheel is
   `runregistrykit-0.2.0-py3-none-any.whl`, ten entries (the five modules, `LICENSE`, `METADATA`,
   `WHEEL`, `top_level.txt`, `RECORD`), `METADATA` `Version: 0.2.0` and `Requires-Dist:
   datastorekit>=0.4.0; extra == "stores"`. Installed (not editable) into a fresh 3.13.16 venv in
   scratch with `datastorekit` from `v0.4.0`, `ray==2.55.1` and `sqlalchemy==2.0.46` (offline from
   `uv`'s cache if it can be, else downloaded from PyPI and DatastoreKit's tag, and nothing else),
   and run with `-I` from an empty directory: the five modules import from `site-packages`;
   `importlib.metadata.version` is `0.2.0`; `this_host` is a name of the package; `import
   runregistrykit.tests` raises `ModuleNotFoundError`; `python -m runregistrykit --help` and `end
   --help` exit 0. Record the wheel's name, size, entry count, SHA-256 and file list. Remove the
   venv after.
3. **The release notes' measurements**, by scratch scripts against `git archive v0.1.0` and `git
   archive` of the working tree's commit (not committed):
   - the shape (keys, nested keys, types) of the manifest, `status.json` while running and after
     `finish`, `status.json` after `end` (verified, and with `--unverified` on an unreadable
     status), a ledger line, the sidecar, and the run directory's file set, at both;
   - `__all__` and each public name's signature at both, and `list_runs`' entry keys at both;
   - `--help` of the command and each subcommand at both;
   - **mixed versions**: records written by each tree read by the other, in one runs root: an alive
     run (pid alive in the reading process), a stale one, a `done` one, and, written by `v0.2.0`,
     a `lost` one, a `foreign` one, one from an earlier boot and one with an unreadable status:
     `liveness`, `list` (exit code and markers), `fingerprint_store` on the store each names, and a
     second `begin` on it. The table is §2.4.4's.
   Every field, value and change §2.4 states traces to a line of these outputs or of the code; the
   log pairs each with its source.
4. **The clients**, read through `git` at the commits the notes name, `git grep` commands as run
   and their hits in the log; nothing of a client run, imported or opened. For SGK, the records its
   drivers would leave after a hard kill are built in scratch with this package (04's
   `a_hard_killed_run` pattern) to show what `begin` then says.
5. **Every statement and name** in the README's changes, the release notes and the adoption notes
   is checked: each importable name by importing it, each argument by `inspect.signature`, each
   command and option by `--help`, each record field by §3.3's outputs, each refusal fragment by
   raising it in scratch, each `path:line` by `sed -n`, each link by finding its target. The log
   lists them, each with how it was checked.
6. **The breakage record.** Each change applied in a scratch export or clone, what fails, and
   reverted; none committed, `git status` here clean after each:
   - (a) `version` left at `0.1.0`: the release check fails at `METADATA` and at
     `importlib.metadata.version`;
   - (b) the tests' `exclude` removed from the export's `pyproject.toml`: the wheel lists
     `runregistrykit/tests/` and `import runregistrykit.tests` succeeds;
   - (c) a field dropped from the release notes' table of §2.4.2 (`host.boot`), and one added that
     is not written (`host.uptime`): the agent's scratch script that compares the notes' fields
     with §3.3's shapes reports both;
   - (d) a name in the README's changes misspelled (`this_hosts`): §3.5's name check reports it.
7. `./venv/bin/black --check runregistrykit docs`: clean, 37 files (no Python file changes).
8. `git status --short --ignored` the same before and after, but for the `egg-info` that §2.1's
   reinstall rewrites (ignored); no `build/` or `dist/` in the repository.

---

## 4. Acceptance

1. `pyproject.toml` is §2.2's; `README.md` is §2.3's; `docs/releases/v0.2.0.md` is §2.4's;
   `docs/adoption/v0.2.0/` holds §2.5's four files; `docs/adoption/README.md` gains §2.5's section
   and nothing else. No other file changes but §4.3's records.
2. §3.1–§3.8 hold. The suite is 410 before and after.
3. **The records**, in the same commit:
   - the log, `logs/06-release-v0.2.0.md`, per README §5.1, with: the suite before and after;
     `pip freeze` of `venv/` before and after; the release check in full; §3.3's outputs (or their
     tables) for both trees, the mixed-version table among them; the clients' `git grep`s; every
     statement of §3.5 with its check; (a)–(d) as applied;
   - the board: the header, §1's row for 06 ("landed, not yet reviewed", "this commit", 410 →
     410), §1.1's V1 ✅ "this commit", and a line in the header saying that `v0.2.0` is ready to be
     tagged on 06's commit once CI passes on that commit, all three jobs, with no tag made;
   - `prompts/INDEX.md`: the campaign's line;
   - this campaign's README §2: 06's status.
   `docs/OPEN_ISSUES.md` changes only if the work opens an issue.

---

## 5. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 410, before or after the reinstall.
- A statement §2.3–§2.5 must make is not true of the code, or cannot be checked. The documents are
  corrected to the code, never the code to the documents: a change under `runregistrykit/` is a
  stop.
- §3.3 finds that the registry writes something the campaign's prompts and logs do not account for
  (README §5 rule 7).
- The release check fails in a way (a) or (b) does not explain.
- A download other than §3.2's would be needed.
- Anything would push to GitHub, make or move a tag, start Ray, or edit, run or import SGK,
  ChamPBH, StochasticInstantons, DatastoreKit or RayPoolKit, or read any of them other than
  through `git` at the commits named.

---

## 6. What this prompt does not do

- **Files it creates or changes:** `pyproject.toml`; `README.md`; `docs/releases/v0.2.0.md`
  (new); `docs/adoption/v0.2.0/README.md`, `secondarygwkit.md`, `champbh.md`,
  `stochasticinstantons.md` (new); `docs/adoption/README.md` (one section); the log, the board,
  the campaign README's §2 row for 06, `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` only as §4.3 says.
- No file under `runregistrykit/` or `.github/` changes, and nothing the registry writes.
- It makes no tag and pushes nothing (§7).
- It edits no client. A client adopts `v0.2.0` in a campaign of its own (G1–G3).
- It writes no verification document (07).

---

## 7. After the review: the push and the tag

Not the agent's work; recorded here so that the review and the user see the whole route. Each step
is the user's yes, put by the orchestrator:

1. Push 06's commit alone: `git push origin <06's SHA>:refs/heads/main`, so that the workflow runs
   on that commit. The review's records commit stays local until step 4.
2. Read the run: all three jobs green, the core job's count 148, the suite 410 at both ends, one
   skip in each, `black` 37 files.
3. Make the tag, annotated, on 06's commit, and push it: `git tag -a v0.2.0 <06's SHA> -m
   "runregistrykit 0.2.0"`, then `git push origin v0.2.0`. Record the tag object's SHA. It is never
   moved or deleted (rule 11).
4. Push `main` with the review's records and a records commit saying the tag is made.

07 then verifies against the pin installed from GitHub.

---

## At writing (2026-10-18, at `80974e2`)

Measured for the README's row and the orchestrator, in the session scratchpad with `TMPDIR` there,
by scratch scripts (not committed) against `git archive v0.1.0` and `git archive HEAD`. Nothing of
a client was run.

**What the registry writes, `v0.1.0` → now.** The manifest gains `host` {`id`, `machine`, `name`,
`python`, `release`, `system`}, each a string here; `status.json` gains `host` {`boot`, `id`} while
running and after `finish`; `end`'s `status.json` holds `state` `lost`, `exit_code` `null` and
`ended` {`at`, `by`, `evidence` {`boot`, `heartbeat`, `heartbeat_age`, `host`, `pid`,
`pid_answers`, `state`, `status_readable`}, `git_head`, `host` {`boot`, `id`, `name`},
`not_verified_because`, `reason`, `verified`}, with the status's other fields kept. A ledger line,
the sidecar and the run directory's file set are **unchanged** in shape. `list_runs`' entries gain
`host`, `host_id`, `host_recorded` and `status_readable`.

**The public interface.** By `inspect.signature` over every module's `__all__`: `TERMINAL_STATES`
`('done', 'failed', 'killed')` → `(…, 'lost')`; `liveness(status, stale_after, now=None)` →
`(…, *, here=None)`; `this_host() -> dict` new. Every other public name's signature unchanged. The
command line gains `end` (`--reason TEXT`, `--unverified`, `--root DIR`, `RUN_ID`); `store
--help`'s text says "any run names whose status does not say it has finished" where it said "a
`running` run names, alive or stale".

**Mixed versions** (a first measurement; the "alive" run's pid was a child that had exited, so it
read as stale in both). Records written now, read by `v0.1.0`: a `lost` run is `unknown`; a
`foreign` run and one from an earlier boot are judged by `kill -0` here (both `stale`, marked
`!!`); `list` exits 0 and counts "1 unknown". Records written by `v0.1.0`, read now: judged as
before, and `list` adds "3 with no host recorded". So a checkout on `v0.1.0` sharing a runs root
with one on `v0.2.0` judges the newer records by the old rules.

**The README** at `80974e2` was last changed by extraction 07 (`aaab408`), before this campaign:
its Status, its pins (`:51`, `:62`),
`finish`'s three states (`:123`), `list`'s liveness (`:131-135`), the store layer's "a `running`
run" (`:182`), the core's public names without `this_host` (`:274-277`), the patch-target sentence
(`:295`) and CI's "two test modules" (`:317`) are each now untrue or incomplete. No release notes
exist; `docs/adoption/` holds `v0.1.0`'s checklists only.

**The wheel**, from an export with `version = "0.2.0"`: `runregistrykit-0.2.0-py3-none-any.whl`,
66 257 bytes, ten entries (the five modules and five of `dist-info`), `Version: 0.2.0`,
`Requires-Dist: datastorekit>=0.4.0; extra == "stores"`. No file under `runregistrykit/` names a
version but three test docstrings that name `v0.1.0`'s records, which stay.

**The clients**, read through `git`:
- **SGK** at `79434bf` (branch `handover-remedial`, the newest commit of any branch): pinned at
  `v0.1.0` (`requirements.txt:81`). It begins runs with `results` in three driver places
  (`scoped_pipeline_run.py:544`, `quadsource_atol_sweep.py:556`, `:869`) and in one test
  (`RunDrivers/tests/test_quadsource_atol_sweep_prepare.py:194`, one run, whose copy refusal it
  checks by "is running" and "names this store", fragments 05's and 04's texts keep). It asserts a
  driver's states are in `TERMINAL_STATES` (`test_pipeline_adoption.py:252`), which `lost` keeps
  passing. `docs/datastore-integrity-verification/interrupt_when.py` calls `liveness` and
  `pid_alive` (`:165-190`). A `git grep` of its tests for `.keys()`, `sorted(manifest`, `set(manifest` and the like
  found no test that pins a record's key set. SGK's `var/runs/` held 83
  run directories at 05's writing, all without `host`.
- **CPBH** at `3cd2be4` (`main`, three commits after its checklist's `c21cdfb`): no import of
  `runregistrykit`; one docstring names it (`ObjectFactories/tests/test_inventory_specs.py:27`).
  `datastorekit` `@v0.4.0`, `ray==2.53.0`, `SQLAlchemy==2.0.46`.
- **SI** at `5fb4a1d` (`dk-and-rpk-migration`, its checklist's commit): no mention of
  `runregistrykit`; no `datastorekit` line; `ray==2.55.1`, `SQLAlchemy==2.0.46`.
- DatastoreKit's newest tag is `v0.4.0`, the floor and both CI ends.

The suite at `80974e2`: `Ran 410 tests`, `OK (skipped=1)`; `black --check runregistrykit docs`, 37
files.
