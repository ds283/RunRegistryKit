# RunRegistryKit

A registry for long-running jobs. A job that takes hours must not be something a conversation, a
terminal or a person's memory owns. RunRegistryKit records that each one exists: a run directory
with a manifest written before the job starts, a heartbeat and a status while it runs, a
checkpoint log, and the provenance of the code that ran it (git SHA, dirty flag, script hash and
the versions of named distributions). `list` shows every run and whether it is alive, judged by
its pid and its heartbeat, never by matching a command line. An optional store layer keeps a
sidecar beside each datastore, saying which runs made it and recording its fingerprint, and
creates, adopts, copies, moves, fingerprints and retires stores under that record.

**Status: `v0.1.0`.** This is the `RunRegistry/` package of
[SecondaryGWKit](https://github.com/ds283/SecondaryGWKit), moved here and made generic: a client's
root and settings come from the `runregistrykit.toml` at that root, and the store layer takes the
client's own fingerprinter. SecondaryGWKit, ChamPBH and StochasticInstantons adopt it from here.
Where each part came from, and what changed on the way, is in [`PROVENANCE.md`](PROVENANCE.md).
The plan for the move is [`prompts/extraction/README.md`](prompts/extraction/README.md), and its
status board is [`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md).

The core depends on nothing beyond the Python standard library. The store layer depends on
[DatastoreKit](https://github.com/ds283/DatastoreKit), the datastore layer extracted from the same
projects, which encodes and digests a store's fingerprint; what goes into the fingerprint is the
client's.

## Supported versions

What `pyproject.toml` declares, and the three configurations CI tests (`.github/workflows/tests.yml`):

| | Declared | Tested: low | Tested: high | Tested: core |
|---|---|---|---|---|
| Python | `>=3.12` | 3.12.15 | 3.13.16 | 3.12.15 |
| `datastorekit` (the extra `[stores]`) | `>=0.4.0` | 0.4.0, from the tag `v0.4.0` | 0.4.0, from the tag `v0.4.0` | not installed |
| Ray | through `datastorekit` (`>=2.43`) | 2.43.0 | 2.55.1 | not installed |
| SQLAlchemy | through `datastorekit` (`>=2.0.39,<2.1`) | 2.0.39 | 2.0.46 | not installed |

- The core depends on nothing; the extra `[stores]` adds `datastorekit`, and through it Ray and
  SQLAlchemy. The low and high configurations run the whole suite; the core one runs the core's
  tests and a smoke of the imports and the command line, with none of the three installed.
- On Python 3.13 Ray's floor is in effect 2.45.0: no earlier Ray release has a wheel for 3.13.
- Releases inside the declared range but newer than the high end, such as Python 3.14 and Ray
  2.59.0 today, are allowed and not tested.
- SQLAlchemy is held below 2.1 by DatastoreKit, not by this package.
- A client pins its own `datastorekit`, `ray` and `sqlalchemy`; this package pins none of them.

## Installing

In a client's `requirements.txt`, the release, with the extra, beside the client's own pin of
DatastoreKit at `v0.4.0` or later:

```
runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.1.0
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
```

Both lines are needed. `datastorekit` is not on PyPI, and the extra names it only by name and floor
(`datastorekit>=0.4.0`), so that the tag the client pins, `v0.4.0` or later, satisfies it; without
the client's own line the install fails to resolve, since no package index has a `datastorekit` to
offer. That line is also what makes `datastorekit` come from DatastoreKit's tag and from nowhere
else.

A client that uses only the core writes `runregistrykit @
git+https://github.com/ds283/RunRegistryKit@v0.1.0`, with no extra and no `datastorekit`.

An editable install (`pip install -e`) is for developing this package, never for a client's
production runs.

## Using it

### The client's root

A client marks its root with a file named `runregistrykit.toml`, read with `tomllib`. Every key is
optional, and an empty file takes every default:

- `runs_root`, default `"var/runs"`: where run directories are made;
- `stores_root`, default `"var/datastores"`: where `store retire` looks for the sidecars that
  reference the store it retires;
- `distributions`, default `[]`: the installed distributions a run's manifest records, besides
  `runregistrykit`, which it always records;
- `[stores]`, default empty, whose one key is `fingerprinter` (below).

A relative `runs_root` or `stores_root` is relative to the record root (the root, or for a run in a
linked worktree the main checkout, below); an absolute one is kept as it is. Any other key, or a
value of the wrong type or shape, is a `ConfigError` that names the file.

The root is found by walking up from a start directory to the first directory holding a
`runregistrykit.toml`: for `begin()`, the directory of the `script` it is given, or the working
directory when it is given none; for everything else, and for the command line, the working
directory. None found is a `ConfigError` that says what to create; no location is ever assumed in
its place. `begin()`, `list_runs()`, `Run` and each function of the store layer that needs the root
take `client_root=` to name it instead, and the command line takes `--client-root DIR`, before its
command.

A run launched from a linked git worktree is recorded under the main checkout, in the same place
relative to it, while its git commit, dirty flag and script hash are those of the worktree it ran
in. So two directories are named here, and for a worktree they differ. Records, and the paths in
them, are under the **record root** (`ClientRoot.root`): the main checkout. The
`runregistrykit.toml` that governs is the one the walk found, or the one in the directory
`client_root=` names (`ClientRoot.found`): in the tree that is running, the worktree's own,
whatever the main checkout holds, and the main checkout need not hold one. A worktree of a bare
repository is refused. The client's `.gitignore` ignores its runs root.

### A run

`begin(campaign, prompt, slug, purpose, ...)` is called by the launching process **before** the work
starts. `campaign`, `prompt` and `slug` name the run, and `purpose` is one line a stranger can
read; the rest are optional keywords: `argv`, `cwd`, `script` (`__file__`, whose hash is recorded),
`unit` and `expected_units`, `checkpoint` (the unit ledger: `True` for one inside the run
directory, or a path), `results` (the store the job's results live in, which the registry names
and never writes), `scope`, `heartbeat_means`, `pid` (default the calling process), `root` (the
runs root, default the config's `runs_root`), `when`, and `client_root`.

It finds the client root first, so that a refusal leaves nothing behind, and refuses a `results`
store whose sidecar is a tombstone. Then it makes the run directory,
`<runs_root>/<campaign>-<prompt>-<slug>-<YYYYMMDDTHHMMSS>`, writes `manifest.json` in it, once,
and `status.json` with the state `running`, and returns a `Run`. A job then calls:

- `heartbeat(units_done=None, units_total=None, pid=None, stage=None)`, to say it is alive and how
  far it has got; a launcher that spawns a detached child passes the child's `pid` here;
- `record(unit, data=None)`, to append one completed unit to the ledger, stamped with the script
  hash, git commit and dirty flag taken at launch;
- `known()`, to read the units already recorded, dropping (with a notice) any written by a
  different version of the script;
- `finish(state, exit_code=None, *, fingerprint=False)` at the end, with `state` one of `done`,
  `failed` or `killed`; with `fingerprint=True` it first takes the fingerprint of the `results`
  store (the store layer, below), and a fingerprint that fails is recorded, never a reason to
  change how the run ended.

The run directory also names `stdout.log` and `stderr.log` (`Run.stdout_path`,
`Run.stderr_path`), for a launcher to send the job's output to; `begin()` does not redirect it.

`python -m runregistrykit list` prints every run under the runs root, newest first, with its state,
progress, age and purpose. A run is alive if and only if its pid answers `kill -0` and its heartbeat
is inside the staleness window (`--stale-after SECONDS`, default 900); one whose state is still
`running` but which fails either test is **stale**, and is marked `!!`. `--root DIR` names another
runs root.

### The store layer

The store layer (`runregistrykit.stores`) keeps a sidecar, `<stem>.manifest.json`, beside a
datastore's primary file, saying what the store is for, which runs made it, and its fingerprint.
Importing it needs nothing beyond the core, but copying, moving and retiring a store import
`datastorekit` when they run, and so does `DatastoreKitFingerprinter` when it takes, compares or
lists a fingerprint; a client that uses the store layer installs the extra `[stores]`. And the store
layer requires a fingerprinter: every store operation, and every `store` command, refuses before
it reads, writes or deletes anything when the config names none.

A client names its fingerprinter in `runregistrykit.toml`:

```toml
[stores]
fingerprinter = "module:attribute"
```

The attribute is an object in a module of the client's own, imported with the directory whose
config governs first on `sys.path`: the tree that is running, which for a run in a linked worktree
is the worktree, not the main checkout. Usually it is a
`DatastoreKitFingerprinter(factories, fingerprint_format)` (`runregistrykit.fingerprint`), made
from the client's registry (a mapping of names to factory classes or instances) and its fingerprint
format number (an `int`, at least 1); a client with other needs writes its own `Fingerprinter`, an
object with the methods `take`, `compare`, `describe` and `listing`, which
`runregistrykit.fingerprint` documents. The config names an instance, not a class.
[`runregistrykit/tests/neutral_store.py`](runregistrykit/tests/neutral_store.py) in this repository
is a worked example over a small registry (its `FACTORIES` and `FINGERPRINTER`); it is not
installed with the package.

The commands, `python -m runregistrykit store <command>`:

- `show PRIMARY`: the sidecar and the runs naming the store;
- `create PRIMARY --purpose TEXT`: a registry sidecar for a store with none;
- `adopt PRIMARY [--purpose TEXT]`: upgrade a legacy sidecar in place;
- `copy SRC DST --purpose TEXT`: copy a closed store and its sidecar;
- `move SRC DST`: move a closed store and its sidecar;
- `fingerprint PRIMARY [--write] [--listing PATH]`: the content fingerprint of a closed store,
  compared with the recorded one; `--write` records it in the sidecar;
- `retire PRIMARY --reason TEXT [--without-fingerprint] [--dry-run]`: delete a closed store's files,
  keeping its sidecar as a tombstone;
- `amend PRIMARY --field NAME (--json VALUE | --remove) --reason TEXT`: replace or remove one
  unknown field of the sidecar, recording the old value.

Those that read runs take `--runs-root DIR`, and `retire` takes `--stores-root DIR`; each defaults
to the config's. `retire` alone deletes, and only a store's own files, its shards and then its
primary; it keeps the sidecar, and it refuses a store that a `running` run names and one whose
recorded fingerprint does not match its content. No command deletes a sidecar, a run directory or
any other record.

### What the registry writes is part of its interface

A client holds run directories and sidecars written by earlier releases, and reads them with the
current one. The run directory's `manifest.json`, `status.json` and `checkpoint.jsonl`, and a
store's sidecar, are therefore part of this package's interface: a change to any of them is made
only in a release of its own, which says so.

## The rules

The registry records. It does not schedule, supervise, restart or lock. It deletes nothing but a
store's own files, and those only through `store retire`, which a person runs and which leaves the
store's sidecar behind as the store's record; it never deletes a run directory, a sidecar or any
other record.

The package supports six rules for a client's long-running jobs, and each ends with the failure it
answers. All of the failures happened in one working session of the project the registry was
extracted from (see [`PROVENANCE.md`](PROVENANCE.md)), and none of them is exotic: each is an
ordinary consequence of treating a long-running job as something a conversation owns. A client
states these rules in its own instructions, so that they bind its agents and its people; the
runs root below is the one the client's `runregistrykit.toml` names (`runs_root`, default
`var/runs`), which the client's `.gitignore` must ignore.

1. **Discovery.** Run `python -m runregistrykit list` at the start of a session and before
   launching anything long, and report anything `running` or stale. A job's existence must not
   depend on a conversation remembering it. The package supports the habit; it cannot enforce it.

   *The failure it answers.* A run was orphaned from the agent that started it, became a child of
   process 1, and left nothing on disk saying what it was, who owned it, what it was for or how far
   along it was; reconstructing that took `ps`, `lsof` and a stderr file, and happened only
   because someone went looking. And a registry that nobody reads is worse than none, because it
   looks like coverage: the discovery rule matters as much as the file format.

2. **Liveness.** A run is alive if and only if its pid answers `kill -0` **and** its heartbeat is
   inside the staleness window. Never decide by matching a command line: `pgrep -f <name>` also
   matches the shells polling for the job, so a wait on it can never end.

   *The failure it answers.* Nineteen poll loops accumulated and none of them could ever exit,
   because each polled with `pgrep -f` on the script's name, which matches the waiting shell's own
   command line. Fifteen were waiting on a measurement that had already been killed; two had been
   spinning for five hours on a script that finished in its first minute; one was waiting for a
   file to reach seventeen lines that its dead producer had left at sixteen.

3. **Launch.** Detached (`nohup` and `disown`; `setsid` is not on macOS), with the manifest
   written first, stdout and stderr in the run directory, and the pid recorded: a launcher that
   spawns a detached child passes the child's pid to `Run.heartbeat(pid=...)` once it has one.

   *The failure it answers.* The same orphaned run as in rule 1: a job that begins without its
   record first leaves nothing saying what it is, and a crash in its first second leaves nothing
   at all.

4. **Do not babysit.** Launch, verify in **one** check that the job started, and end the turn.
   Polling a long job re-sends an entire context per poll and learns nothing; that, not
   wall-clock time, is what makes waiting expensive. Resume once, when it is done.

   *The failure it answers.* The nineteen poll loops of rule 2 were each a full conversational
   turn that re-sent an entire context and learned nothing.

5. **Durability.** A client keeps its runs root under its own root, ignored by git, and never in
   a session scratchpad or in `/tmp`. The package keeps an absolute `runs_root` or `stores_root`
   as it is, and does not refuse another place; this is a rule for the client.

   *The failures it answers.* A three-hour measurement accumulated its results in memory and
   printed its tables after the last cell; killed at 4 h 57 m, it left one line of output. A
   datastore was written into a session scratchpad and is gone, and the 462-row census in it
   cannot be re-examined: scratchpads are per session.

6. **Provenance.** The script hash and the git commit are taken at launch and stamped on every
   checkpoint record. A record whose script hash does not match the running script is discarded
   and recomputed, never blended, and never re-stamped: re-stamping falsifies the thing the stamp
   exists to prove.

   *The failures it answers.* The stamp paid for itself on its first outing: re-running a script
   after its commit reported the same hash and reused all sixty cells, which proved in four
   seconds that the committed script was byte-identical to the one that produced the published
   numbers. And resumption had been assumed rather than exercised: when a pipeline run of
   10 h 33 m was finally resumed, it replayed every earlier stage correctly and then crashed on a
   read-back path that had never been taken.

The registry is about existence, not computation. It records that a job exists, what it is for,
who started it, what tree it ran against, whether it is alive and how far it has got; that is what
lets a run survive a session ending, a quota interruption or a switch between accounts.
Checkpointing is per job, and is sometimes already solved: a job whose results live in a
datastore needs only to be registered.

## The public names

Each module's `__all__` is its public interface, and nothing else is:

- `runregistrykit`, the core: `CONFIG_FILE`, `ClientRoot`, `ConfigError`, `DEFAULT_STALE_AFTER`,
  `Run`, `TERMINAL_STATES`, `begin`, `find_client_root`, `git_provenance`, `heartbeat_age`,
  `list_runs`, `liveness`, `now_iso`, `package_provenance`, `pid_alive`, `read_json`, `run_id`,
  `script_sha256`, `slugify` and `write_json_atomic`;
- `runregistrykit.stores`, the store layer (it needs the extra `[stores]`): `AMEND_KEYS`,
  `AMEND_OPERATION`, `HISTORY_KEYS`, `IDENTITY_OPERATIONS`, `INCOMPLETE_MOVE_SUFFIX`,
  `KNOWN_FIELDS`, `RELOCATION_OPERATIONS`, `REQUIRED_FIELDS`, `RETIREMENT_STATES`,
  `RETIRE_OPERATION`, `SIDECAR_FORMAT`, `SidecarReading`, `TAKEN_KEYS`, `adopt_sidecar`,
  `amend_sidecar`, `check_listing_path`, `copy_store`, `create_sidecar`, `fingerprint_store`,
  `move_store`, `new_store_id`, `read_sidecar`, `retire_store`, `runs_naming`, `sidecar_path` and
  `write_listing`;
- `runregistrykit.client`: `CONFIG_FILE`, `ClientRoot`, `ConfigError` and `find_client_root`;
- `runregistrykit.fingerprint`: `DatastoreKitFingerprinter`, `Fingerprinter`, `load_fingerprinter`
  and `require_fingerprinter`;
- `python -m runregistrykit`: the command line, whose module exports `main`.

Everything else is private and may change in any release, a leading underscore or not.

**No patch target is promised.** Where the package looks a name up at call time, a client that
patches that name does so at its own risk. The two places are `Run.finish` with `fingerprint=True`,
which imports `runregistrykit.stores` when it runs and calls `fingerprint_store`, and `begin()`
with `results`, which imports `runregistrykit.stores` and calls `read_sidecar`; the package
promises nothing about the objects it finds there, nor about the module-level names behind them.

## Developing

In a checkout of this repository, a venv with DatastoreKit from its tag and this package editable,
with the extra:

```
python3.12 -m venv venv
./venv/bin/python -m pip install "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0" -e ".[stores]"
./venv/bin/python -m unittest discover -s runregistrykit/tests -t .
```

The suite needs `git` on `PATH` and the checkout to be a git work tree (its tests build temporary
git repositories and worktrees, and one reads the checkout's commit). It needs Ray installed, which
`datastorekit` brings, and never a Ray cluster: Ray is never initialised. It creates nothing outside
`tempfile` directories. The code is formatted with `black` 25.1.0 (`black --check runregistrykit
docs`).

CI (`.github/workflows/tests.yml`) runs the suite at both ends of the supported range and `black` at
the low end, and the core alone in a job with none of `datastorekit`, `ray` and `sqlalchemy`
installed: the two test modules that need nothing else, `test_run_registry` and
`test_public_names`, and a smoke of the imports and the command line. The checks under
`docs/extraction/` read the client repositories through `git`, and run locally only.

## Licence

Apache License 2.0; see [`LICENSE`](LICENSE).
