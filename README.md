# RunRegistryKit

A registry for long-running jobs. A job that takes hours must not be something a conversation, a
terminal or a person's memory owns. RunRegistryKit records that each one exists: a run directory
with a manifest written before the job starts, a heartbeat and a status while it runs, a
checkpoint log, and the provenance of the code that ran it (git SHA, dirty flag, script hash and
the versions of named distributions). `list` shows every run and whether it is alive, judged by
its pid and its heartbeat, never by matching a command line. An optional store layer keeps a
sidecar beside each datastore, saying which runs made it and recording its fingerprint, and
creates, adopts, copies, moves, fingerprints and retires stores under that record.

**Status: being extracted.** The code does not live here yet. It is the `RunRegistry/` package of
[SecondaryGWKit](https://github.com/ds283/SecondaryGWKit), which ChamPBH and StochasticInstantons
will adopt from here. The plan for moving it, making it generic and releasing it is
[`prompts/extraction/README.md`](prompts/extraction/README.md); its status board is
[`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md).

The core depends on nothing beyond the Python standard library. The store layer depends on
[DatastoreKit](https://github.com/ds283/DatastoreKit), the datastore layer extracted from the same
projects, which encodes and digests a store's fingerprint; what goes into the fingerprint is the
client's.

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

## Licence

Apache License 2.0; see [`LICENSE`](LICENSE).
