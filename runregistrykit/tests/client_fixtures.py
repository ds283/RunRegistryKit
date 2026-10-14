"""A client root for a test: a `runregistrykit.toml`, in a git repository, in a `tempfile`
directory of its own.

Not a test module (no ``test_`` prefix); the test modules import it. Every `git` call here is
isolated from the user's and the system's configuration (`GIT_CONFIG_GLOBAL` is the null device,
`GIT_CONFIG_NOSYSTEM` is set, and the identity is given on the command line), so that no signing,
hook or template of theirs reaches a test's repository. Every directory is `os.path.realpath`'d:
on macOS `tempfile` gives `/var/…`, which is `/private/var/…`, and `git` prints the latter.
"""

import os
import subprocess
import tempfile

import runregistrykit

# where the package under test is imported from: the directory a child process puts first on
# `sys.path` (or in `PYTHONPATH`). It is not a records root of any kind
PACKAGE_PARENT = os.path.dirname(
    os.path.dirname(os.path.abspath(runregistrykit.__file__))
)

GIT_IDENTITY = (
    "-c",
    "user.name=runregistrykit tests",
    "-c",
    "user.email=tests@runregistrykit.invalid",
    "-c",
    "commit.gpgsign=false",
)


def git_environment() -> dict:
    """The environment every test `git` call runs in."""
    env = {
        name: value for name, value in os.environ.items() if not name.startswith("GIT_")
    }
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    return env


def git(cwd, *args) -> str:
    """Run ``git *args`` in ``cwd``, isolated; return its stdout, stripped. Raises on failure."""
    done = subprocess.run(
        ["git", *GIT_IDENTITY, *args],
        cwd=cwd,
        env=git_environment(),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if done.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} in {cwd} failed ({done.returncode}): {done.stderr}"
        )
    return done.stdout.strip()


def temporary_directory(test) -> str:
    """A new `tempfile` directory, realpath'd, removed when ``test`` ends."""
    holder = tempfile.TemporaryDirectory()
    test.addCleanup(holder.cleanup)
    return os.path.realpath(holder.name)


def write_client_root(directory, config="") -> str:
    """Make ``directory`` a client root: a `runregistrykit.toml` holding ``config``, a
    `.gitignore` holding `var/`, and a git repository with one commit of the two. Returns it.
    """
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, runregistrykit.CONFIG_FILE), "w") as handle:
        handle.write(config)
    with open(os.path.join(directory, ".gitignore"), "w") as handle:
        handle.write("var/\n")
    git(directory, "init", "-q", "-b", "main")
    git(directory, "add", runregistrykit.CONFIG_FILE, ".gitignore")
    git(directory, "commit", "-q", "-m", "a client root for a test")
    return directory


def enter_client_root(test, config="") -> str:
    """A client root in a `tempfile` directory of its own, made the working directory until
    ``test`` ends. Returns its path."""
    client = write_client_root(temporary_directory(test), config)
    previous = os.getcwd()
    os.chdir(client)
    # registered after the directory's own cleanup, so that it runs first
    test.addCleanup(os.chdir, previous)
    return client
