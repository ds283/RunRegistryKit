"""Where a client's records go: its root, which a `runregistrykit.toml` marks, and that file.

**The file.** A client marks its root with a file named `runregistrykit.toml`, read with
`tomllib`. Every key is optional, and an empty file takes every default:

    runs_root      a non-empty string, default "var/runs": where run directories are made
    stores_root    a non-empty string, default "var/datastores": where `store retire` looks for
                   the sidecars that reference the store it retires
    distributions  a list of non-empty strings with no duplicates, default []: the installed
                   distributions a run's manifest records under `packages`, besides
                   `runregistrykit`, which is always recorded
    [stores]       a table, default empty: the store layer's settings. Its one key is
                   `fingerprinter`, a string "module:attribute" naming the client's fingerprinter
                   (`runregistrykit.fingerprint`): a non-empty dotted module path, one colon and a
                   non-empty dotted attribute path, with no whitespace. Only its form is checked
                   here, and nothing is imported. The core (`begin()`, `Run`, `list_runs`, `list`)
                   needs none; every store operation refuses without one

A relative `runs_root` or `stores_root` is joined to the **record root** (below) and normalised
with `os.path.normpath`; an absolute one is kept as it is. Neither `~` nor an environment variable
is expanded. Anything else is a `ConfigError` that names the file: a file that is not valid TOML,
or cannot be read, a key not in the list above (a key of `[stores]` other than `fingerprinter`
among them), or a value of the wrong type or shape.

**Finding it.** `find_client_root(start)` walks from `start` (made absolute) through each parent
up to the filesystem root, and the first directory holding a *file* named `runregistrykit.toml`
is the one whose file governs (`ClientRoot.found`). The walk stops nowhere else: not at a git top
level and not at the home directory. None found is a `ConfigError` that says what to create; no
location is ever assumed in its place. `client_root=` names that directory directly instead, with
no walk, and one holding no `runregistrykit.toml` is a `ConfigError` too.

Each public function of the package that needs the root takes `client_root=`, and otherwise walks
from its **start directory**: for `begin()`, the directory of the `script` it is given, and the
working directory when it is given none; for everything else, and for the command line, the
working directory.

**The record root** (`ClientRoot.root`) is where records go and what the paths in them are
relative to. It is `found`, except that a run launched from a linked git worktree is recorded
under the **main checkout**: `found`'s path relative to the worktree's top level, taken from the
parent of `git rev-parse --git-common-dir`. A config in a subdirectory of a worktree so maps to
the same subdirectory of the main checkout. The config that governs is still `found`'s, the tree
that is running, and the main checkout need not hold one. A worktree of a bare repository has no
main checkout to record into, and is a `ConfigError`. Outside any repository, or without `git`,
the record root is `found`.

Importing this module reads no file and runs no `git`.
"""

import os
import subprocess
import tomllib
from dataclasses import dataclass

CONFIG_FILE = "runregistrykit.toml"

# every key the file may hold, with its default
_DEFAULTS = {
    "runs_root": "var/runs",
    "stores_root": "var/datastores",
    "distributions": [],
    "stores": {},
}

_GIT_TIMEOUT = 30


class ConfigError(RuntimeError):
    """A client root that cannot be found, or a `runregistrykit.toml` that cannot be used."""


@dataclass(frozen=True)
class ClientRoot:
    """A client root, found and read.

    ``root`` is the record root; ``found`` the directory whose `runregistrykit.toml` governs, and
    ``config_file`` that file; ``runs_root`` and ``stores_root`` are absolute; ``distributions``
    is a tuple; ``stores`` is the `[stores]` table, as read.
    """

    root: str
    found: str
    config_file: str
    runs_root: str
    stores_root: str
    distributions: tuple
    stores: dict


def _no_config(start) -> ConfigError:
    return ConfigError(
        f"No {CONFIG_FILE} in {start} or any directory above it. Create one at the client's "
        f'root; an empty file takes the defaults (runs_root = "var/runs", stores_root = '
        f'"var/datastores", distributions = [])'
    )


def _walk(start) -> str:
    """The first directory from ``start`` upwards that holds a file named `CONFIG_FILE`."""
    directory = start
    while True:
        if os.path.isfile(os.path.join(directory, CONFIG_FILE)):
            return directory
        parent = os.path.dirname(directory)
        if parent == directory:
            raise _no_config(start)
        directory = parent


def _read_config(path) -> dict:
    """The file's keys, checked, with every default filled in."""
    try:
        with open(path, "rb") as handle:
            data = tomllib.load(handle)
    except OSError as e:
        raise ConfigError(f"{path} cannot be read: {type(e).__name__}: {e}") from None
    except ValueError as e:  # tomllib.TOMLDecodeError, or bytes that are not UTF-8
        raise ConfigError(f"{path} is not valid TOML: {e}") from None

    unknown = sorted(set(data) - set(_DEFAULTS))
    if unknown:
        raise ConfigError(
            f"{path} has the key(s) {unknown}, which {CONFIG_FILE} does not have; its keys "
            f"are {sorted(_DEFAULTS)}"
        )

    for key in ("runs_root", "stores_root"):
        if key in data:
            value = data[key]
            if not (isinstance(value, str) and value.strip()):
                raise ConfigError(
                    f"{path}: {key} is {value!r}, which is not a non-empty string"
                )

    if "distributions" in data:
        value = data["distributions"]
        if not (
            isinstance(value, list)
            and all(isinstance(name, str) and name.strip() for name in value)
        ):
            raise ConfigError(
                f"{path}: distributions is {value!r}, which is not a list of non-empty "
                f"strings"
            )
        repeated = sorted({name for name in value if value.count(name) > 1})
        if repeated:
            raise ConfigError(
                f"{path}: distributions is {value!r}, which names {repeated} more than once"
            )

    if "stores" in data:
        if not isinstance(data["stores"], dict):
            raise ConfigError(
                f"{path}: stores is {data['stores']!r}, which is not a table ([stores])"
            )
        for key, value in data["stores"].items():
            if key != "fingerprinter":
                raise ConfigError(
                    f"{path}: [stores] has the key {key!r} (= {value!r}), which "
                    f"{CONFIG_FILE} does not have; its one key is 'fingerprinter'"
                )
            if not _is_fingerprinter_spec(value):
                raise ConfigError(
                    f"{path}: [stores] fingerprinter is {value!r}, which is not a string "
                    f'"module:attribute": a dotted module path, one colon and a dotted attribute '
                    f"path, with no whitespace"
                )

    return {**_DEFAULTS, **data}


def _is_fingerprinter_spec(value) -> bool:
    """Whether ``value`` has the form of `[stores] fingerprinter`: a string, a non-empty dotted
    module path, one colon, a non-empty dotted attribute path, each part an identifier (so no
    whitespace). The form only: nothing is imported."""
    if not isinstance(value, str) or value.count(":") != 1:
        return False
    module, attribute = value.split(":")
    return all(part.isidentifier() for part in module.split(".") + attribute.split("."))


def _record_root(found) -> str:
    """`found`, or for a linked worktree the same place in its main checkout."""
    try:
        done = subprocess.run(
            [
                "git",
                "-C",
                found,
                "rev-parse",
                "--path-format=absolute",
                "--git-dir",
                "--git-common-dir",
                "--show-toplevel",
            ],
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return found
    lines = done.stdout.splitlines()
    if done.returncode != 0 or len(lines) != 3:
        return found
    git_dir, common_dir, toplevel = lines
    if os.path.realpath(git_dir) == os.path.realpath(common_dir):
        # a main checkout (or a submodule): the root is `found` as it was given, and no path
        # printed by git enters it
        return found
    common_dir = os.path.normpath(common_dir)
    if os.path.basename(common_dir) != ".git":
        raise ConfigError(
            f"{found} is in a worktree of the bare repository {common_dir}, which has no main "
            f"checkout to record runs into. Run from a checkout that is not a bare repository's "
            f"worktree"
        )
    within = os.path.relpath(os.path.realpath(found), os.path.realpath(toplevel))
    return os.path.normpath(os.path.join(os.path.dirname(common_dir), within))


def _under(root, value) -> str:
    return (
        value if os.path.isabs(value) else os.path.normpath(os.path.join(root, value))
    )


def find_client_root(start=None, client_root=None) -> ClientRoot:
    """The client root for a call whose start directory is ``start`` (the working directory when
    `None`), or the one ``client_root`` names (no walk). A `ClientRoot` given as ``client_root``
    is returned as it is. Raises `ConfigError`; never falls back to a location of its own.
    """
    if isinstance(client_root, ClientRoot):
        return client_root
    if client_root is not None:
        found = os.path.abspath(client_root)
        if not os.path.isfile(os.path.join(found, CONFIG_FILE)):
            raise ConfigError(
                f"The client root {found} holds no {CONFIG_FILE}. Create one there; an empty "
                f'file takes the defaults (runs_root = "var/runs", stores_root = '
                f'"var/datastores", distributions = [])'
            )
    else:
        found = _walk(os.path.abspath(os.getcwd() if start is None else start))

    config_file = os.path.join(found, CONFIG_FILE)
    config = _read_config(config_file)
    root = _record_root(found)
    return ClientRoot(
        root=root,
        found=found,
        config_file=config_file,
        runs_root=_under(root, config["runs_root"]),
        stores_root=_under(root, config["stores_root"]),
        distributions=tuple(config["distributions"]),
        stores=dict(config["stores"]),
    )
