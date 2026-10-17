# (c) University of Sussex 2026
# Created by David Seery
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A record on disk that a long-running job exists, what it is for, and how far it has got.

The rules this package exists to support are in this repository's `README.md`, "The rules", and
each is told there with the failure it answers. The package is a convention with a little code
behind it, not a framework: it schedules nothing, supervises nothing and locks nothing. It also
creates, adopts, copies and moves the stores it manages, with their `<stem>.manifest.json`
sidecars (`runregistrykit.stores`), because managing stores is part of managing the registry. It
deletes nothing but a store's own files, and those only through `store retire`, which a person
runs and which leaves the store's sidecar behind as its record. It never deletes a run directory,
a sidecar or any other record.

The layout, under the client's runs root (`var/runs/` by default, `runs_root` in the client's
`runregistrykit.toml`), which a client keeps under its own root and ignores in git, and never in a
session scratchpad or in `/tmp` (a datastore written into a scratchpad is lost with it):

    var/runs/<campaign>-<prompt>-<slug>-<YYYYMMDDTHHMMSS>/
        manifest.json      written once at launch, never mutated
        status.json        the only mutable file; state, progress, heartbeat, pid, exit code
        checkpoint.jsonl   optional, append-only, one JSON object per completed unit
        stdout.log  stderr.log

The manifest keeps two different things in two different fields, because the registry is about a
job's existence and checkpointing is per job, and sometimes already solved: `checkpoint` is the
unit ledger above, which `record()` writes and `known()` reads; `results` names the durable thing
the job's results live in — a datastore the job's pipeline writes — which this package names and
never writes; it reads it only to take its fingerprint at `finish(..., fingerprint=True)`. A job
may have either, both or neither. `campaign` and `prompt` are the client's names for a body of work
and for a step of it, and `slug` names the run.

Usage is three calls. The launching process writes the manifest before any work starts, so that a
crash in the first second still leaves a record:

    run = runregistrykit.begin(
        campaign="example", prompt="01", slug="smoke",
        purpose="one line a stranger can read",
        script=__file__, unit="cell", expected_units=60, checkpoint=True,
    )
    known = run.known()                       # what a previous run already did
    for item in work:
        if key(item) in known:
            continue
        run.record(key(item), compute(item))   # appends, flushes, fsyncs, beats
    run.finish("done", exit_code=0)

`python -m runregistrykit list` prints every run, newest first, and says loudly which of them claim
to be running but are not.
"""

import copy
import hashlib
import importlib.metadata
import itertools
import json
import os
import platform
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone

from .client import CONFIG_FILE, ClientRoot, ConfigError, find_client_root

__all__ = [
    "CONFIG_FILE",
    "ClientRoot",
    "ConfigError",
    "DEFAULT_STALE_AFTER",
    "Run",
    "TERMINAL_STATES",
    "begin",
    "find_client_root",
    "git_provenance",
    "heartbeat_age",
    "list_runs",
    "liveness",
    "now_iso",
    "package_provenance",
    "pid_alive",
    "read_json",
    "run_id",
    "script_sha256",
    "slugify",
    "this_host",
    "write_json_atomic",
]

TERMINAL_STATES = ("done", "failed", "killed")

# The lister's default staleness window. `liveness()` itself takes the window from its caller;
# fifteen minutes is a convention for the command line, overridable with --stale-after, and is
# chosen to be long against a heartbeat written once per completed unit.
DEFAULT_STALE_AFTER = 900.0

_ID_STAMP = "%Y%m%dT%H%M%S"


# =================================================================================================
# identity and provenance: the run's id, and what was running, as it stood at launch


def now_iso() -> str:
    """Local time with an offset, to the second (`YYYY-MM-DDTHH:MM:SS+hh:mm`): the format that
    manifests written by hand, before this registry existed, used."""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def slugify(text) -> str:
    """What `run_id` applies to each of its three parts, so that a client can recover a run id's
    parts from a manifest."""
    return re.sub(r"[^A-Za-z0-9._]+", "-", str(text)).strip("-")


def run_id(campaign, prompt, slug, when=None) -> str:
    """`<campaign>-<prompt>-<slug>-<YYYYMMDDTHHMMSS>`: it sorts, and a stranger reading
    `ls var/runs/` learns who owns each directory without asking anyone."""
    stamp = time.strftime(_ID_STAMP, time.localtime(when))
    return "-".join((slugify(campaign), slugify(prompt), slugify(slug), stamp))


def script_sha256(path) -> str:
    """SHA-256 of a script's source. Taken once, at `begin()`: that is the source the running
    interpreter actually holds, and re-taking it later would read a file the process is not
    running."""
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def git_provenance(cwd) -> dict:
    """`git rev-parse HEAD` and whether the tree was clean, as they stood at launch."""

    def run(args):
        try:
            return subprocess.run(
                args, cwd=cwd, capture_output=True, text=True, timeout=30, check=False
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ""

    return {
        "git_head": run(["git", "rev-parse", "HEAD"]) or "unknown",
        "git_dirty": bool(run(["git", "status", "--porcelain"])),
    }


def package_provenance(names) -> dict:
    """What is installed of each named distribution, as it stands at `begin()`.

    Maps each name to `None` when it is not installed, and otherwise to a dict with exactly:
    - `version`: the installed distribution's version;
    - `url`: `url` in the distribution's PEP 610 `direct_url.json`, or `None`;
    - `commit`: its `vcs_info.commit_id`, or `None`;
    - `requested_revision`: its `vcs_info.requested_revision` (the tag or branch asked for), or
      `None`;
    - `editable`: `True` when `dir_info.editable` is true, and `False` otherwise.

    It is read from the installed distribution's metadata with the standard library only; no
    package being described is imported. For a VCS install, `commit` is the commit the tag
    resolved to when pip installed it, and that is what makes the record reproducible: a tag can
    move, a commit cannot. An absent `direct_url.json`, or one that is not a JSON object, or a
    `vcs_info` or `dir_info` that is not one, gives `None` for the three fields and `False` for
    `editable`; it never raises, because `begin()` must not fail on odd metadata.

    An editable install is recorded, not refused: the registry records (the README's rules).
    """
    packages = {}
    for name in names:
        try:
            distribution = importlib.metadata.distribution(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
            continue
        origin = None
        try:
            origin = json.loads(distribution.read_text("direct_url.json"))
        except (TypeError, ValueError, OSError):
            origin = None
        if not isinstance(origin, dict):
            origin = {}
        vcs_info = origin.get("vcs_info")
        if not isinstance(vcs_info, dict):
            vcs_info = {}
        dir_info = origin.get("dir_info")
        if not isinstance(dir_info, dict):
            dir_info = {}
        packages[name] = {
            "version": distribution.version,
            "url": origin.get("url"),
            "commit": vcs_info.get("commit_id"),
            "requested_revision": vcs_info.get("requested_revision"),
            "editable": dir_info.get("editable") is True,
        }
    return packages


def _recorded_names(client) -> tuple:
    """What a manifest's `packages` records: `runregistrykit` itself, always, then the client
    config's `distributions`, without repeating `runregistrykit`."""
    return ("runregistrykit",) + tuple(
        name for name in client.distributions if name != "runregistrykit"
    )


# =================================================================================================
# files


def _repo_path(path, root) -> str:
    """A path relative to the record root ``root`` where that is meaningful, an absolute one
    otherwise."""
    absolute = os.path.abspath(path)
    if absolute.startswith(root + os.sep):
        return os.path.relpath(absolute, root)
    return absolute


def _resolve(path, root) -> str:
    return path if os.path.isabs(path) else os.path.join(root, path)


def read_json(path):
    """The file's contents, or `None` if it is absent, unreadable or not JSON. A lister that
    raises on one bad directory tells you about none of the others."""
    try:
        with open(path, "r") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def write_json_atomic(path, payload) -> None:
    """Write via a temporary file **in the same directory** and `os.replace`, so that a reader
    either sees the previous contents or the new ones and never a half-written file."""
    tmp = path + ".tmp"
    with open(tmp, "w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


# =================================================================================================
# the writer of `status.json`, which a handler may re-enter (`Run._update` is its one caller)

# held across a whole status write. Re-entrant, so that a handler that interrupts a write on its
# own thread and writes again is not blocked by the write it interrupted; a plain lock would
# leave that handler waiting for ever. Two threads' writes are serialised by it
_STATUS_LOCK = threading.RLock()

# per `status.json`, keyed by its real path, so that every `Run` object for one run directory in
# this process is one writer: its sequence numbers, the fields of each write still in flight,
# and what has landed, sequence number → payload, of which the highest number is the newest.
# A write records itself with one store under its own number and then prunes the lower numbers,
# so that a handler landing a later write at any instruction of it adds a key that no lower one
# hides: the newest number held never goes down
_STATUS_WRITES = {}

# a per-process counter, one of the three parts of a temporary name
_STATUS_NAMES = itertools.count()


def _status_temporary_name(path) -> str:
    """A temporary name for one write of the `status.json` at ``path``, beside it: it begins
    `status.json.`, ends `.tmp`, and is never `status.json.tmp`, the name `write_json_atomic`
    uses. The pid, a per-process counter and random hex make it one write's own, in one process or
    two."""
    return f"{path}.{os.getpid()}-{next(_STATUS_NAMES)}-{os.urandom(4).hex()}.tmp"


def _remove_quietly(name) -> None:
    try:
        os.remove(name)
    except OSError:
        pass


def _newest_landed(book) -> tuple:
    """The number and payload of the newest write landed for ``book``, or `(-1, None)` if none
    has. A handler's write that prunes the number read here before its payload is read makes it
    read again, so a number is never returned without its payload."""
    landed = book["landed"]
    while True:
        number = max(landed, default=-1)
        if number < 0:
            return number, None
        payload = landed.get(number)
        if payload is not None:
            return number, payload


def _land_status(path, book, number, payload) -> None:
    """Write ``payload``, the payload of write ``number``, to the `status.json` at ``path``,
    through a temporary file of its own, unless a later write has landed first.

    The file is created with `os.open(…, 0o666)`, so that the umask applies to it exactly as it
    does to `open(path, "w")`, and written as `write_json_atomic` writes. Any exception before the
    replace, `BaseException` included, removes it and is re-raised. A write that finds a later
    write landed is discarded: its file is removed and nothing is replaced. A later write that
    lands between the check and the replace (a handler can run at the bytecode boundary before
    the `os.replace` call) is put back afterwards, by a write of its payload under its own number,
    which is itself checked in the same way.

    Otherwise the write records itself: its deep copy is taken first, then the check for a later
    write, then one store under its own number, then the lower numbers are pruned, over a
    snapshot of the keys. A handler that interrupts any of these and lands a later write leaves
    its own, higher, number in the record, which neither the store nor the prune removes.
    """
    name = _status_temporary_name(path)
    try:
        descriptor = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
        with open(descriptor, "w") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        if _newest_landed(book)[0] > number:
            os.remove(name)
            return
        os.replace(name, path)
    except BaseException:
        _remove_quietly(name)
        raise
    recorded = copy.deepcopy(payload)
    newest, newest_payload = _newest_landed(book)
    if newest > number:
        _land_status(path, book, newest, newest_payload)
        return
    landed = book["landed"]
    landed[number] = recorded
    for n in list(landed):
        if n < number:
            landed.pop(n, None)


def _write_status(path, fields) -> dict:
    """Merge ``fields`` into the `status.json` at ``path``, stamp the heartbeat, write it, and
    return the payload composed. `Run._update` says what is and is not covered."""
    with _STATUS_LOCK:
        book = _STATUS_WRITES.setdefault(
            os.path.realpath(path),
            {"numbers": itertools.count(), "in_flight": {}, "landed": {}},
        )
        # one call, so that a handler cannot take the same number: the merge below skips an
        # in-flight write numbered at or below the landed payload's, which a shared number breaks
        number = next(book["numbers"])
        try:
            book["in_flight"][number] = dict(fields)
            # generators: a handler raising at a comprehension or loop filter leaves the lock held
            earlier = list(n for n in sorted(book["in_flight"]) if n < number)
            landed, payload = _newest_landed(book)
            if earlier and payload is not None:
                # a handler has re-entered a write: the file may hold what that write read. The
                # newest landed payload already holds the fields of every in-flight write older
                # than it, and may have set the same keys since, so only the newer are applied
                status = copy.deepcopy(payload)
                earlier = list(n for n in earlier if n > landed)
            else:
                status = read_json(path) or {}
            for n in earlier:
                status.update(book["in_flight"][n])
            status.update(fields)
            status["heartbeat"] = now_iso()
            _land_status(path, book, number, status)
            return status
        finally:
            book["in_flight"].pop(number, None)


# =================================================================================================
# liveness, by pid and heartbeat and never by a command-line match (the README's rule on liveness)


def pid_alive(pid) -> bool:
    """Whether a process exists, by `os.kill(pid, 0)`.

    **Never identify a process by matching a pattern against command lines.** `pgrep -f <name>`
    also matches the *polling shell's own* command line, so "wait until no process matches" can
    never be satisfied; that mistake left nineteen immortal poll loops, fifteen of them waiting on
    a job that was already dead (the README's rule on liveness).
    """
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:  # exists, owned by somebody else
        return True
    except OSError:
        return False
    return True


def heartbeat_age(status, now=None):
    """Seconds since the heartbeat, or `None` if there is no readable one."""
    try:
        beat = datetime.fromisoformat(status.get("heartbeat"))
    except (AttributeError, TypeError, ValueError):
        return None
    if beat.tzinfo is None:  # a naive stamp is local time
        beat = beat.astimezone()
    return ((now or datetime.now(timezone.utc)) - beat).total_seconds()


# A pid means something only on the machine that issued it, and only during the boot that issued
# it. So a run records which machine and which boot its pid belongs to, read from the operating
# system through the standard library. Each reader returns a string or None and never raises: a
# platform that offers no identity records null, which is judged here, as a record with no host
# is. The machine's own identity is a hardware identifier and is never written; what is written
# is a digest of it.

# the variable that names this machine for reading, in place of `platform.node()`, which on a
# laptop is often a name the network assigned. It is never used to judge
_HOST_NAME_VARIABLE = "RUNREGISTRYKIT_HOST_NAME"

# what the machine identity is hashed with, so that the recorded id is this package's own
_HOST_DIGEST_PREFIX = b"runregistrykit host\0"

# where Linux keeps the machine identity, the first non-empty one used (machine-id(5)), and the
# identity of the current boot
_MACHINE_ID_FILES = ("/etc/machine-id", "/var/lib/dbus/machine-id")
_BOOT_ID_FILE = "/proc/sys/kernel/random/boot_id"


def _first_line(path):
    """The file's text, stripped, or None if it cannot be read or is empty."""
    try:
        with open(path, "r", encoding="ascii") as handle:
            text = handle.read().strip()
    except (OSError, ValueError):
        return None
    return text or None


def _c_library():
    """The C library through `ctypes`, or None. Imported here, so that importing the package
    loads no `ctypes`, and only on macOS, the one platform whose readers call it."""
    import ctypes
    import ctypes.util

    path = ctypes.util.find_library("c")
    if not path:
        return None
    return ctypes.CDLL(path, use_errno=True)


def _read_machine_identity():
    """This machine's own identity, raw, or None: on macOS `gethostuuid(3)` as a UUID in
    lowercase text, on Linux the first non-empty machine-id file, lowercased. Never written; see
    `this_host`."""
    try:
        system = platform.system()
        if system == "Darwin":
            import ctypes

            class Timespec(ctypes.Structure):
                _fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]

            library = _c_library()
            if library is None:
                return None
            call = library.gethostuuid
            call.argtypes = [ctypes.c_void_p, ctypes.POINTER(Timespec)]
            call.restype = ctypes.c_int
            buffer = (ctypes.c_ubyte * 16)()
            wait = Timespec(1, 0)
            if call(buffer, ctypes.byref(wait)) != 0:
                return None
            raw = bytes(buffer)
            if not any(raw):
                return None
            text = raw.hex()
            return "-".join((text[:8], text[8:12], text[12:16], text[16:20], text[20:]))
        if system == "Linux":
            for path in _MACHINE_ID_FILES:
                text = (_first_line(path) or "").lower()
                if re.fullmatch(r"[0-9a-f]{32}", text):
                    return text
            return None
    except Exception:
        return None
    return None


def _read_boot_identity():
    """The identity of this boot of this machine, or None: on macOS the sysctl
    `kern.bootsessionuuid` (not `kern.uuid`, which is the kernel build's and the same on every
    machine running it), on Linux the kernel's `boot_id`. It changes at every boot."""
    try:
        system = platform.system()
        if system == "Darwin":
            import ctypes

            library = _c_library()
            if library is None:
                return None
            call = library.sysctlbyname
            call.argtypes = [
                ctypes.c_char_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_size_t),
                ctypes.c_void_p,
                ctypes.c_size_t,
            ]
            call.restype = ctypes.c_int
            buffer = ctypes.create_string_buffer(64)
            size = ctypes.c_size_t(len(buffer))
            if call(b"kern.bootsessionuuid", buffer, ctypes.byref(size), None, 0) != 0:
                return None
            text = buffer.raw[: size.value].decode("ascii").strip("\0").strip()
            return text or None
        if system == "Linux":
            return _first_line(_BOOT_ID_FILE)
    except Exception:
        return None
    return None


def _read_host_name():
    """A name for this machine, for a person to read and never to judge by:
    `RUNREGISTRYKIT_HOST_NAME` if it is set and not empty, else `platform.node()`, else None.
    """
    try:
        name = os.environ.get(_HOST_NAME_VARIABLE) or platform.node()
    except Exception:
        return None
    return name or None


def _ask(reader):
    """What ``reader`` gives, if it is a non-empty string, and otherwise None, whatever happens
    inside it."""
    try:
        value = reader()
    except Exception:
        return None
    return value if isinstance(value, str) and value else None


def this_host() -> dict:
    """{"id", "boot", "name", "machine", "system", "release", "python"} for this machine now.

    - `id`: the first 16 hex characters of the SHA-256 of a fixed prefix and the machine's own
      identity (macOS `gethostuuid(3)`, Linux `/etc/machine-id`), or None where the platform
      offers none. The identity itself, a hardware identifier, is never returned or written;
    - `boot`: the identity of the current boot (macOS `kern.bootsessionuuid`, Linux `boot_id`),
      as it is read, or None;
    - `name`: `RUNREGISTRYKIT_HOST_NAME` if set and not empty, else `platform.node()`, else None.
      It is for reading only: the registry judges by `id` and `boot`, never by a name;
    - `machine`, `system`, `release`, `python`: `platform.machine()`, `platform.system()`,
      `platform.release()` and `platform.python_version()`.

    Read afresh on each call, with no cache, from the standard library and without a subprocess;
    a call costs well under a millisecond. It never raises for a reader's sake: a reader that
    fails gives None there. `begin` records `id`, `name` and the platform fields in the manifest
    and `id` and `boot` in `status.json`, and `liveness` judges a record by them.
    """
    raw = _ask(_read_machine_identity)
    return {
        "id": (
            None
            if raw is None
            else hashlib.sha256(_HOST_DIGEST_PREFIX + raw.encode()).hexdigest()[:16]
        ),
        "boot": _ask(_read_boot_identity),
        "name": _ask(_read_host_name),
        "machine": platform.machine(),
        "system": platform.system(),
        "release": platform.release(),
        "python": platform.python_version(),
    }


def liveness(status, stale_after, now=None, *, here=None) -> str:
    """`alive`, `stale`, `foreign`, `finished` or `unknown` for one `status.json` payload.

    In this order:

    1. no status is `unknown`; a terminal state is **finished**; any state other than `running`
       is `unknown`;
    2. a `running` record **on another host** is **foreign**: its `host.id` is not null and is not
       ``here``'s, which includes ``here`` having no id, since a record that carries one was
       written where there was one. Its pid is not tested and its heartbeat is not weighed:
       `foreign` means "not judged here", and **never** that the run is alive, or that it is
       dead. A person looks on its host;
    3. a `running` record **on this host, from another boot** is **stale**: both ids are not null
       and match, both boots are not null and differ. Its pid cannot name a process of this boot,
       whatever `kill -0` says;
    4. otherwise a run is **alive** iff its pid answers `kill -0` *and* its heartbeat is inside
       the window the caller supplies, and **stale** if it fails either: a crashed job pretending
       to be alive, which is the thing worth shouting about.

    A record with no `host`, which is every record written before the field existed, or with a
    `host` that is not an object or whose `id` is null, goes straight to step 4: it is judged
    here, by pid and heartbeat, exactly as before. ``here`` is a `this_host()` dict, read afresh
    when it is not given and a record needs it.
    """
    if not status:
        return "unknown"
    if status.get("state") in TERMINAL_STATES:
        return "finished"
    if status.get("state") != "running":
        return "unknown"
    host = status.get("host")
    if isinstance(host, dict) and host.get("id") is not None:
        if here is None:
            here = this_host()
        if host["id"] != here.get("id"):
            return "foreign"
        boot, current = host.get("boot"), here.get("boot")
        if boot is not None and current is not None and boot != current:
            return "stale"
    if not pid_alive(status.get("pid")):
        return "stale"
    age = heartbeat_age(status, now)
    if age is None or age > stale_after:
        return "stale"
    return "alive"


# =================================================================================================
# the run


def _not_a_ledger(path, number, line) -> ValueError:
    """The error `known()` raises rather than reporting "nothing done" for a file it cannot read.

    It names the other field, because the caller who gets here has almost always put the durable
    thing their results live in where the unit ledger goes.
    """
    return ValueError(
        f"checkpoint {path}: line {number} is not a JSON record, so this file is not a unit "
        f"ledger: {line[:60]!r}. known() will not report it as 'nothing done yet' — a resume that "
        f"believed that would recompute work that is already on disk. If this path is where the "
        f"job's results live, name it in the manifest's results field instead of checkpoint; "
        f"record() and known() read only the ledger."
    )


class Run:
    """One run directory. Construct it with `begin()`."""

    def __init__(self, path, *, client_root=None):
        self.path = os.path.abspath(path)
        self.id = os.path.basename(self.path)
        self.manifest = read_json(self.manifest_path) or {}
        # a `ClientRoot`, a directory to find one in, or None: located the first time a relative
        # recorded path is resolved, or a fingerprint taken, and never before
        self._client_root = client_root

    @property
    def client_root(self) -> ClientRoot:
        """This run's client root, located from the working directory (or the ``client_root``
        it was given) the first time it is needed."""
        if not isinstance(self._client_root, ClientRoot):
            self._client_root = find_client_root(client_root=self._client_root)
        return self._client_root

    def _recorded_path(self, recorded):
        if os.path.isabs(recorded):
            return recorded
        return _resolve(recorded, self.client_root.root)

    # --- paths ---------------------------------------------------------------------------------

    @property
    def manifest_path(self) -> str:
        return os.path.join(self.path, "manifest.json")

    @property
    def status_path(self) -> str:
        return os.path.join(self.path, "status.json")

    @property
    def stdout_path(self) -> str:
        return os.path.join(self.path, "stdout.log")

    @property
    def stderr_path(self) -> str:
        return os.path.join(self.path, "stderr.log")

    @property
    def checkpoint_path(self):
        """The unit ledger, and nothing else. `record()` appends to this and `known()` reads it;
        neither ever looks at `results_path`."""
        recorded = self.manifest.get("checkpoint")
        return self._recorded_path(recorded) if recorded else None

    @property
    def results_path(self):
        """The durable thing this job's results live in — a datastore the job's pipeline
        writes — which the registry names. A datastore once written into a session scratchpad was
        lost with it, with nothing on disk saying where the results had gone, and a resume must
        know what it is resuming into. The registry never writes it. It reads it, read-only, in one
        place: `finish(..., fingerprint=True)` takes its content fingerprint."""
        recorded = self.manifest.get("results")
        return self._recorded_path(recorded) if recorded else None

    # --- status --------------------------------------------------------------------------------

    def status(self) -> dict:
        return read_json(self.status_path) or {}

    def _update(self, **fields) -> dict:
        """Merge ``fields`` into `status.json`, stamp the heartbeat, write it, and return the
        payload composed. Every write of `status.json` comes through here.

        A handler that interrupts the process, a driver's `finish` made on an interrupt, may write
        the status while a write is in progress on the same thread, and may then raise, return or
        end the process. So the status is written through a temporary name of its own per write,
        `status.json.<unique>.tmp` beside it, created with the mode `open(path, "w")` gives, and
        never through `write_json_atomic`'s shared `<path>.tmp`. And the writes to one
        `status.json` in this process, through any `Run` object for it, are ordered by a sequence
        number:

        - a write takes the next number, and its fields are held as in flight until it ends;
        - it composes its payload from the file, then the fields of every earlier write still in
          flight, in order, then its own. When an earlier write is in flight, a handler has
          re-entered one, and the base is instead the newest payload this process has landed, or
          the file if it has landed none: the file may then hold what the interrupted write read.
          From a landed payload, only the in-flight writes numbered above it are applied: those
          below it were in flight throughout it, so it holds their fields already, and any key it
          set since is newer;
        - a write that finds a later one landed while it was writing is discarded, and replaces
          nothing; one that a later write overtakes between its check and its replace puts the
          later payload back. So a terminal state is never replaced by a payload read before it,
          and the fields of a discarded heartbeat are kept by the write that overtook it;
        - what has landed is held by number, and the newest is the highest number held. A write
          records itself with one store under its own number and then prunes the lower ones, so
          a handler that interrupts it and lands a later write is never hidden from a later
          write's composition: the record of what landed never goes back.

        A re-entrant lock is held across the whole write. Two threads' writes are serialised, and
        a handler that re-enters a write on its own thread is not blocked by it.

        Not covered: a handler that re-enters between a write taking its number and holding its
        fields as in flight loses those fields, never the terminal state; and writes from two
        processes at once are not ordered at all. A process that dies between creating its
        temporary file and replacing it (`SIGKILL`, or a handler that restores the default
        disposition and kills its own process) leaves a `status.json.<unique>.tmp` in the run
        directory. Nothing reads it, `list` and the store operations do not look at a run
        directory's other files, and nothing removes it. At Python 3.14, a handler that raises just
        after the lock is taken, at the `with` statement's entry, leaves it held, as it would any
        lock taken by a `with` on that version.
        """
        return _write_status(self.status_path, fields)

    def heartbeat(
        self, units_done=None, units_total=None, pid=None, stage=None
    ) -> dict:
        """Refresh the heartbeat, and with it whatever is now known. A launcher that spawns a
        detached child passes the child's `pid` here once it has one.

        `stage` is for a job that has no total to count against — a pipeline reports progress per
        stage and per work queue, never as one number, and inventing a denominator would be worse
        than saying where it has got to. It is the field a manifest written by hand carried as
        `stage_reached`, reconstructed by hand from a stdout file after the fact.
        """
        fields = {
            "units_done": units_done,
            "units_total": units_total,
            "pid": pid,
            "stage": stage,
        }
        return self._update(**{k: v for k, v in fields.items() if v is not None})

    def finish(self, state, exit_code=None, *, fingerprint=False) -> dict:
        """Set the terminal state and the exit code. The registry records; it does not kill,
        restart or reap, so `killed` is something a caller reports, not something observed.

        With ``fingerprint=True``, and a manifest that names `results`, it first fingerprints that
        store (`runregistrykit.stores.fingerprint_store`, read-only, with this run as `taken_by` so
        that it does not refuse its own caller) and puts the fingerprint in `status.json` under
        `fingerprint`. Where the store's sidecar is a problem-free registry sidecar the fingerprint
        is also written there, replacing only its `fingerprint` field, so that a run that changed
        its store never leaves a stale one in the place a reader looks; otherwise
        `fingerprint_sidecar` says why it was not. Pass it only once the store is closed: a
        driver's signal handler, which runs with the pool still open, does not.

        **A fingerprint never changes how a run ended.** Any refusal or error is recorded as
        `fingerprint_error`, a string, and the state and exit code given are written regardless.
        It never raises for the fingerprint's sake. The manifest is never touched.
        """
        if state not in TERMINAL_STATES:
            raise ValueError(
                f"terminal state must be one of {TERMINAL_STATES}: {state!r}"
            )
        taken = {}
        if fingerprint:
            try:
                taken = self._fingerprint_results()
            except Exception as e:
                taken = {"fingerprint_error": f"{type(e).__name__}: {e}"}
            except BaseException as e:
                # an interrupt while fingerprinting: the state is still written, then it goes on
                self._update(
                    state=state,
                    exit_code=exit_code,
                    fingerprint_error=f"interrupted: {type(e).__name__}",
                )
                raise
        return self._update(state=state, exit_code=exit_code, **taken)

    def _fingerprint_results(self) -> dict:
        """The `status.json` fields `finish(..., fingerprint=True)` records. May raise."""
        results = self.results_path
        if results is None:
            return {
                "fingerprint_error": "the manifest names no results store to fingerprint"
            }
        from .stores import _sidecar_refusal, fingerprint_store, read_sidecar

        client = self.client_root
        reading = read_sidecar(results, client_root=client)
        taken = fingerprint_store(
            results,
            write=reading.ok,
            runs_root=os.path.dirname(self.path),
            taken_by=self,
            client_root=client,
        )
        return {
            "fingerprint": taken["fingerprint"],
            "fingerprint_sidecar": (
                "written"
                if taken["wrote"]
                else f"not written: {reading.path} is not a problem-free registry "
                f"sidecar ({_sidecar_refusal(reading)})"
            ),
        }

    # --- the checkpoint ------------------------------------------------------------------------

    def record(self, unit, data=None) -> dict:
        """Append one completed unit to `checkpoint.jsonl`, `flush`, `fsync`, and beat.

        The record carries the provenance triple — script hash, git head, dirty flag — taken at
        launch and never re-taken (the README's rule on provenance), so that a resume can tell
        which version of the script wrote each record.

        It appends to the **ledger** and to nothing else. A run that declares no ledger is refused,
        by name: the caller who reaches here is usually one who copied the pipeline pattern — whose
        results are a datastore — and then gave their job units, and the fix they need is a ledger
        of their own, not a method that writes JSON-Lines into whatever the manifest happens to
        name.
        """
        path = self.checkpoint_path
        if path is None:
            store = self.manifest.get("results")
            names = (
                f"It names a results store ({store}), which this method will never write to: "
                f"the registry names where a job's results live, it does not write them. "
                if store
                else ""
            )
            raise ValueError(
                f"run {self.id} declares no checkpoint ledger in its manifest, so record() has "
                f"nothing to append to. {names}"
                f"A job with units to record needs a ledger of its own: pass checkpoint=True to "
                f"begin() (or a path to a .jsonl file), which is the field record() and known() "
                f"read."
            )
        record = {
            "unit": unit,
            "recorded": now_iso(),
            "script_sha256": self.manifest.get("script_sha256"),
            "git_head": self.manifest.get("git_head"),
            "git_dirty": self.manifest.get("git_dirty"),
            "data": data,
        }
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "a") as handle:
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        done = self.status().get("units_done") or 0
        self.heartbeat(units_done=done + 1)
        return record

    def known(self, notice=sys.stderr) -> dict:
        """Every completed unit already on disk, keyed by unit, so a resume recomputes only what
        it lacks.

        **Policy on a script-hash mismatch: discard, with a notice.** A record written by a
        different version of the script is dropped and its unit recomputed, rather than the run
        refusing to start — an edited script is then self-healing instead of stranding the operator
        on a file they must know to delete, and the notice is what makes the discard visible. This
        is the choice of a script that checkpoints its own cells, generalised. Records are never
        blended across script versions, and an existing record is **never re-stamped** with the
        running hash: that would falsify the provenance the stamp exists to provide. Where the
        manifest records no script hash there is nothing to gate on and every record is reused.

        A malformed trailing line is ignored: the file is appended to as each unit lands, so a kill
        can truncate the last record. **A file that is not a ledger at all is a different thing and
        raises.** Answering `{}` — "nothing has been done yet" — for a file this method cannot read
        is the failure a resume then acts on by recomputing everything, which for one pipeline run
        was 10 h 33 m of work. The two are told apart by where the unreadable line is and what it
        looks like: a torn record is the **last** line and is a prefix of a JSON object, so it
        begins `{`. Anything else — a line that does not, or a readable line after one that did
        not, or a file that is not even text — means the path names something that is not a unit
        ledger.

        A ledger that does not exist yet is not an error, and returns nothing quietly: that is
        every first run.
        """
        path = self.checkpoint_path
        units, stale = {}, {}
        if path is None or not os.path.exists(path):
            return units
        wanted = self.manifest.get("script_sha256")
        try:
            with open(path, "r") as handle:
                torn = None
                for number, line in enumerate(handle, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    if torn is not None:  # the torn line was not the final one
                        raise _not_a_ledger(path, torn[0], torn[1])
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        if not line.startswith("{"):
                            raise _not_a_ledger(path, number, line) from None
                        torn = (number, line)
                        continue
                    unit = record.get("unit")
                    if wanted and record.get("script_sha256") != wanted:
                        stale[unit] = record.get("script_sha256") or "unstamped"
                        units.pop(unit, None)
                        continue
                    units[unit] = record
        except UnicodeDecodeError:
            raise _not_a_ledger(path, 1, "<not text>") from None
        if stale and notice is not None:
            hashes = ", ".join(sorted({str(h)[:12] for h in stale.values()}))
            print(
                f"checkpoint {path}: discarding {len(stale)} record(s) written by a different "
                f"version of the script ({hashes}); this script is {str(wanted)[:12]}. Those "
                f"units will be recomputed.",
                file=notice,
                flush=True,
            )
        return units


def begin(
    campaign,
    prompt,
    slug,
    purpose,
    argv=None,
    cwd=None,
    script=None,
    unit=None,
    expected_units=None,
    checkpoint=None,
    results=None,
    scope=None,
    heartbeat_means=None,
    pid=None,
    root=None,
    when=None,
    *,
    client_root=None,
):
    """Create the run directory, write the immutable manifest, and write `status.json` as
    `running`. Call this **before** the work starts.

    `checkpoint` is the **unit ledger** and only that: the append-only JSON-Lines file `record()`
    writes and `known()` reads. `checkpoint=True` puts one inside the run directory; a path puts it
    wherever the job's own convention says, which is how a resume in a new run directory reads the
    previous run's units.

    `results` is the **durable thing the job's results live in** — for a registered pipeline run,
    its SQLite datastore — which the registry names and never writes. It is a different field from
    `checkpoint` because it is a different thing, and conflating them let `record()` append
    JSON-Lines to a datastore (the registry records a job's *existence*; checkpointing is per job
    and is sometimes already solved, as a pipeline's datastore already is). It exists because a
    datastore written into a session scratchpad was lost with it, with nothing on disk saying where
    the results had gone, and because a resume must know what it is resuming into.

    `pid` defaults to the calling process; a launcher that spawns a detached child passes the
    child's pid to `heartbeat()` once it has one. Every manifest field but three is one that would
    have caught something in the failures the README's rules answer; there are no others.

    The first is `results_store_id`, which comes with managing stores: it is how a run and its store
    are matched. When `results` has a problem-free registry sidecar beside it
    (`runregistrykit.stores`), it holds that sidecar's `store_id`, and otherwise `null`: no store,
    no sidecar, a legacy sidecar, or a sidecar with a problem. It matches a run to its store after
    the store has moved, which a path cannot, and it is how `store copy` / `store move` recognise a
    store a running run is using. The sidecar is read here and never written. Manifests written
    before the field existed lack it, and are read exactly as before. A `results` whose sidecar is a
    tombstone (`runregistrykit.stores.retire_store`) is refused before the run directory is created,
    because a retired name is never reused.

    The second is `packages`, which is `package_provenance()` of `runregistrykit` and of the client
    config's `distributions`: what was installed of each when the run began. It exists so that a
    run says which package release it ran, instead of that being implied by `requirements.txt` at
    its `HEAD`; none of those failures asked for it.

    The third is `host`, `this_host()`'s `id`, `name`, `machine`, `system`, `release` and
    `python`, read once before the run directory is created: what ran the job, as `git_head` says
    what code it ran, since rows computed on different hardware can differ in their last bits. The
    first `status.json` records `host` too, as `{"id", "boot"}` from the same reading, beside the
    pid it qualifies, and every later write keeps it, `heartbeat(pid=…)` included: a launcher's
    child is on the launcher's machine. Both are written even when every value is null, which
    means "this platform offered none"; a record with no `host` at all was written before the
    field existed. `liveness` reads the status's.

    `root` is the runs root, and defaults to the client config's `runs_root`. The client root is
    found by walking up from the directory of `script`, or from the working directory when no
    script is given (`runregistrykit.client`), unless `client_root` names it; none found is a
    `ConfigError`, raised before anything is created. Paths in the manifest are relative to the
    record root where they lie under it, and `git_head` and `git_dirty` are those of the tree the
    walk started in.

    `scope` is one line saying what the run covers, and is what tells a stranger whether the run
    is still relevant — a manifest written by hand carried it, because `argv` alone is exact and
    unreadable. Derive it from the job's own arguments rather than typing it: a field somebody
    must remember to update is a field that goes stale.

    `heartbeat_means` is one line saying what a fresh heartbeat on *this* job actually asserts.
    It exists because the honest answer differs per job — "a unit was recorded" for a script with
    units, something weaker for a Ray-parallel pipeline whose parent may be blocked inside
    `ray.get` — and a heartbeat that implies a guarantee it does not give is worse than none.
    `None` means this package's default: the heartbeat is refreshed by `record()` and by an
    explicit `heartbeat()`, so it means "a unit completed", and nothing else.
    """
    # the client root is located first, so that a refusal leaves nothing behind. The walk starts
    # from the script, else the working directory; provenance is that start directory's
    start = os.path.dirname(os.path.abspath(script)) if script else os.getcwd()
    client = find_client_root(start=start, client_root=client_root)
    identifier = run_id(campaign, prompt, slug, when)
    path = os.path.join(root or client.runs_root, identifier)
    # the results store's sidecar is read before anything is created: a retired store is refused,
    # complete or not, because a retired name is never reused, and no run directory is left behind
    results_store_id = None
    if results:
        # here, because `stores` imports this module
        from .stores import _tombstone_text, read_sidecar

        reading = read_sidecar(results, client_root=client)
        if reading.retired:
            raise RuntimeError(
                f'Cannot begin run {identifier} with results "{results}": '
                f"{_tombstone_text(reading)}. Give the new store a name of its own. No run "
                f"directory was created"
            )
        results_store_id = reading.store_id
    # the machine and the boot this run's pid belongs to, read once, before anything is created
    host = this_host()
    os.makedirs(path, exist_ok=True)
    if os.path.exists(os.path.join(path, "manifest.json")):
        raise FileExistsError(
            f"{path} already holds a manifest; a manifest is written once"
        )
    if checkpoint is True:
        checkpoint = os.path.join(path, "checkpoint.jsonl")
    manifest = {
        "run_id": identifier,
        "created": now_iso(),
        "purpose": purpose,
        "campaign": campaign,
        "prompt": str(prompt),
        "argv": list(sys.argv if argv is None else argv),
        "cwd": cwd or os.getcwd(),
        "script": _repo_path(script, client.root) if script else None,
        "script_sha256": script_sha256(script) if script else None,
        "unit": unit,
        "expected_units": expected_units,
        "checkpoint": _repo_path(checkpoint, client.root) if checkpoint else None,
        "results": _repo_path(results, client.root) if results else None,
        "results_store_id": results_store_id,
        "scope": scope,
        "heartbeat_means": heartbeat_means,
        "host": {
            key: host[key]
            for key in ("id", "name", "machine", "system", "release", "python")
        },
    }
    manifest.update(git_provenance(start))
    manifest["packages"] = package_provenance(_recorded_names(client))
    write_json_atomic(os.path.join(path, "manifest.json"), manifest)
    run = Run(path, client_root=client)
    run._update(
        state="running",
        units_done=0,
        units_total=expected_units,
        pid=os.getpid() if pid is None else pid,
        exit_code=None,
        host={"id": host["id"], "boot": host["boot"]},
    )
    return run


# =================================================================================================
# the lister


def _created_epoch(entry_path, manifest):
    try:
        return datetime.fromisoformat(manifest["created"]).timestamp()
    except (KeyError, TypeError, ValueError):
        return os.path.getmtime(entry_path)


def list_runs(
    root=None, stale_after=DEFAULT_STALE_AFTER, now=None, *, client_root=None
) -> list:
    """Every run under `root`, newest first; with no `root`, under the client config's
    `runs_root`, which is the one case that locates the client root.

    A directory with no manifest is reported, not skipped and not repaired: `var/runs/` holds run
    directories that predate this package, and they are evidence. Loose files beside the run
    directories are ignored. Nothing here writes or deletes anything.

    Each entry's `liveness` is `liveness()`'s, with this host read once per call. Besides the
    status's and the manifest's fields, each entry has:
    - `host`: the manifest's `host.name`, or None;
    - `host_id`: the status's `host.id`, or None;
    - `host_recorded`: whether the status has a `host` object at all. False is a record written
      before the field existed (or a directory with no readable status), judged here as before.
    """
    if not root:
        root = find_client_root(client_root=client_root).runs_root
    entries = []
    try:
        names = os.listdir(root)
    except OSError:
        return entries
    here = this_host()
    for name in names:
        path = os.path.join(root, name)
        if not os.path.isdir(path):
            continue
        manifest = read_json(os.path.join(path, "manifest.json"))
        status = read_json(os.path.join(path, "status.json")) or {}
        recorded = status.get("host")
        described = (manifest or {}).get("host")
        entries.append(
            {
                "id": name,
                "path": path,
                "has_manifest": manifest is not None,
                "purpose": (manifest or {}).get("purpose"),
                "state": status.get("state"),
                "pid": status.get("pid"),
                "units_done": status.get("units_done"),
                "units_total": status.get("units_total")
                or (manifest or {}).get("expected_units"),
                "stage": status.get("stage"),
                "liveness": liveness(status, stale_after, now=now, here=here),
                "created_epoch": _created_epoch(path, manifest or {}),
                "host": (
                    described.get("name") if isinstance(described, dict) else None
                ),
                "host_id": recorded.get("id") if isinstance(recorded, dict) else None,
                "host_recorded": isinstance(recorded, dict),
            }
        )
    entries.sort(key=lambda entry: entry["created_epoch"], reverse=True)
    return entries
