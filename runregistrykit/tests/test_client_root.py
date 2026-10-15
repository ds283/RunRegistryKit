"""The client root: `runregistrykit.toml`, the walk that finds it, the record root a linked
worktree maps to, and the paths and provenance a run and a store operation record under it.

Every directory is a `tempfile` directory, `os.path.realpath`'d, and every test starts in an empty
one with no `runregistrykit.toml` above it (checked), so that nothing is found by accident. Every
git repository and worktree is made in one of them, with `git` isolated from the user's
configuration (`client_fixtures`). No Ray is initialised.
"""

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

import runregistrykit
from runregistrykit import stores
from runregistrykit.client import CONFIG_FILE, ClientRoot, ConfigError, find_client_root
from runregistrykit.tests.client_fixtures import (
    PACKAGE_PARENT,
    enter_client_root,
    git,
    git_environment,
    temporary_directory,
    write_client_root,
)

from datastorekit.shard_paths import shard_file_name
from runregistrykit.tests.shard_store_fixtures import write_new_store


def write(path, text="") -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        handle.write(text)
    return path


def sha256(path) -> str:
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def configs_at_or_above(directory) -> list:
    found = []
    while True:
        if os.path.lexists(os.path.join(directory, CONFIG_FILE)):
            found.append(os.path.join(directory, CONFIG_FILE))
        parent = os.path.dirname(directory)
        if parent == directory:
            return found
        directory = parent


def in_a_repository(directory) -> bool:
    done = subprocess.run(
        ["git", "-C", directory, "rev-parse", "--git-dir"],
        env=git_environment(),
        capture_output=True,
        text=True,
        timeout=60,
    )
    return done.returncode == 0


def commit_all(repository, message) -> str:
    git(repository, "add", "-A")
    git(repository, "commit", "-q", "-m", message)
    return git(repository, "rev-parse", "HEAD")


class ClientRootTestCase(unittest.TestCase):
    """Each test starts in ``self.nowhere``, an empty directory with no config at or above it."""

    def setUp(self):
        self.nowhere = temporary_directory(self)
        self.assertEqual(
            configs_at_or_above(self.nowhere),
            [],
            "a runregistrykit.toml above the temporary directory: these tests cannot mean "
            "anything here",
        )
        previous = os.getcwd()
        os.chdir(self.nowhere)
        self.addCleanup(os.chdir, previous)

    def a_config(self, text="") -> str:
        """A directory holding a `runregistrykit.toml` with ``text``, in no repository."""
        directory = temporary_directory(self)
        write(os.path.join(directory, CONFIG_FILE), text)
        self.assertFalse(in_a_repository(directory), directory)
        return directory

    def begin(self, **kwargs):
        kwargs.setdefault("campaign", "client-root")
        kwargs.setdefault("prompt", "03")
        kwargs.setdefault("slug", "test")
        kwargs.setdefault("purpose", "a test run, in a temporary directory")
        kwargs.setdefault("argv", ["unittest"])
        return runregistrykit.begin(**kwargs)


class TestConfig(ClientRootTestCase):
    def test_an_empty_file_takes_every_default(self):
        d = self.a_config("")
        self.assertEqual(
            find_client_root(client_root=d),
            ClientRoot(
                root=d,
                found=d,
                config_file=os.path.join(d, CONFIG_FILE),
                runs_root=os.path.join(d, "var", "runs"),
                stores_root=os.path.join(d, "var", "datastores"),
                distributions=(),
                stores={},
            ),
        )

    def test_each_key_is_read(self):
        elsewhere = temporary_directory(self)
        d = self.a_config(
            'runs_root = "records/runs"\n'
            f'stores_root = "{elsewhere}"\n'
            'distributions = ["datastorekit", "raypoolkit"]\n'
            "\n"
            "[stores]\n"
            'fingerprinter = "a.module:an_attribute"\n'
        )
        client = find_client_root(client_root=d)
        self.assertEqual(client.runs_root, os.path.join(d, "records", "runs"))
        self.assertEqual(client.stores_root, elsewhere)
        self.assertEqual(client.distributions, ("datastorekit", "raypoolkit"))
        self.assertEqual(client.stores, {"fingerprinter": "a.module:an_attribute"})

    def test_a_relative_root_is_joined_and_normalised_and_an_absolute_one_kept(self):
        d = self.a_config('runs_root = "./a/../runs"\n' 'stores_root = "/x/./y/../z"\n')
        client = find_client_root(client_root=d)
        self.assertEqual(client.runs_root, os.path.join(d, "runs"))
        self.assertEqual(client.stores_root, "/x/./y/../z")
        # no ~ expansion, and no environment variables
        d = self.a_config('runs_root = "~/runs"\n' 'stores_root = "$HOME/stores"\n')
        client = find_client_root(client_root=d)
        self.assertEqual(client.runs_root, os.path.join(d, "~", "runs"))
        self.assertEqual(client.stores_root, os.path.join(d, "$HOME", "stores"))

    def test_each_refusal_is_a_config_error_naming_the_file(self):
        cases = {
            "invalid TOML": ('runs_root = "unterminated\n', ["is not valid TOML"]),
            "not UTF-8": (b'runs_root = "\xff"\n', ["is not valid TOML"]),
            "an unknown key": ('runs_roots = "var/runs"\n', ["'runs_roots'"]),
            "runs_root not a string": ("runs_root = 1\n", ["runs_root is 1"]),
            "runs_root empty": ('runs_root = ""\n', ["runs_root is ''"]),
            "stores_root not a string": (
                'stores_root = ["a"]\n',
                ["stores_root is ['a']"],
            ),
            "distributions not a list": (
                'distributions = "datastorekit"\n',
                ["distributions is 'datastorekit'"],
            ),
            "a distribution not a string": (
                "distributions = [1]\n",
                ["distributions is [1]"],
            ),
            "an empty distribution": (
                'distributions = [""]\n',
                ["distributions is ['']"],
            ),
            "a duplicate distribution": (
                'distributions = ["a", "b", "a"]\n',
                ["distributions is ['a', 'b', 'a']", "names ['a'] more than once"],
            ),
            "stores not a table": ('stores = "x"\n', ["stores is 'x'"]),
        }
        for label, (text, fragments) in cases.items():
            with self.subTest(label):
                d = temporary_directory(self)
                path = os.path.join(d, CONFIG_FILE)
                with open(path, "wb") as handle:
                    handle.write(text if isinstance(text, bytes) else text.encode())
                for call in (
                    lambda: find_client_root(client_root=d),
                    lambda: find_client_root(start=d),
                ):
                    with self.assertRaises(ConfigError) as refused:
                        call()
                    message = str(refused.exception)
                    self.assertIn(path, message)
                    for fragment in fragments:
                        self.assertIn(fragment, message)

    def test_an_unreadable_file_is_a_config_error_naming_it(self):
        d = self.a_config("")
        path = os.path.join(d, CONFIG_FILE)
        os.chmod(path, 0)
        self.addCleanup(os.chmod, path, 0o644)
        if os.access(path, os.R_OK):
            self.skipTest("this user can read a file with no permissions")
        with self.assertRaises(ConfigError) as refused:
            find_client_root(client_root=d)
        self.assertIn(path, str(refused.exception))
        self.assertIn("cannot be read", str(refused.exception))

    def test_the_fingerprinter_is_kept_and_another_stores_key_refused(self):
        d = self.a_config('[stores]\nfingerprinter = "a.module:an_attribute"\n')
        self.assertEqual(
            find_client_root(client_root=d).stores,
            {"fingerprinter": "a.module:an_attribute"},
        )
        d = self.a_config(
            "[stores]\n"
            'fingerprinter = "a.module:an_attribute"\n'
            "[stores.more]\n"
            "n = 1\n"
        )
        with self.assertRaises(ConfigError) as refused:
            find_client_root(client_root=d)
        message = str(refused.exception)
        self.assertIn(os.path.join(d, CONFIG_FILE), message)
        self.assertIn("'more'", message)
        self.assertIn("{'n': 1}", message)

    def test_a_client_root_already_found_is_used_as_it_is(self):
        client = find_client_root(client_root=self.a_config(""))
        self.assertIs(find_client_root(start="/", client_root=client), client)


class TestWalk(ClientRootTestCase):
    def test_found_from_a_script_two_directories_below_the_root(self):
        d = self.a_config("")
        script = write(os.path.join(d, "docs", "sub", "job.py"), "print('job')\n")
        self.assertEqual(find_client_root(start=os.path.dirname(script)).found, d)

        # begun from a working directory with no config above it: the walk starts at the script
        run = self.begin(script=script)
        self.assertEqual(run.client_root.found, d)
        self.assertEqual(os.path.dirname(run.path), os.path.join(d, "var", "runs"))
        self.assertEqual(run.manifest["script"], os.path.join("docs", "sub", "job.py"))
        self.assertEqual(run.manifest["cwd"], self.nowhere)

    def test_the_nearest_config_wins(self):
        outer = self.a_config('runs_root = "outer-runs"\n')
        inner = os.path.join(outer, "inner")
        write(os.path.join(inner, CONFIG_FILE), 'runs_root = "inner-runs"\n')
        start = os.path.join(inner, "a", "b")
        os.makedirs(start)
        client = find_client_root(start=start)
        self.assertEqual(client.found, inner)
        self.assertEqual(client.runs_root, os.path.join(inner, "inner-runs"))

    def test_only_a_file_marks_a_root(self):
        outer = self.a_config("")
        os.makedirs(os.path.join(outer, "inner", CONFIG_FILE))
        self.assertEqual(
            find_client_root(start=os.path.join(outer, "inner")).found, outer
        )

    def test_none_found_is_a_config_error_naming_the_start(self):
        start = os.path.join(self.nowhere, "a", "b")
        os.makedirs(start)
        for call, named in (
            (lambda: find_client_root(start=start), start),
            (lambda: find_client_root(), self.nowhere),
        ):
            with self.assertRaises(ConfigError) as refused:
                call()
            message = str(refused.exception)
            self.assertIn(
                f"No {CONFIG_FILE} in {named} or any directory above it", message
            )
            self.assertIn("Create one at the client's root", message)
            self.assertIn('runs_root = "var/runs"', message)

    def test_client_root_without_a_config_is_a_config_error_and_no_walk(self):
        d = self.a_config("")
        sub = os.path.join(d, "sub")
        os.makedirs(sub)
        self.assertEqual(find_client_root(start=sub).found, d)
        with self.assertRaises(ConfigError) as refused:
            find_client_root(client_root=sub)
        self.assertIn(sub, str(refused.exception))
        self.assertIn(f"holds no {CONFIG_FILE}", str(refused.exception))

    def test_a_refused_begin_creates_no_directory_anywhere(self):
        runs = temporary_directory(self)
        with self.assertRaises(ConfigError):
            self.begin(root=runs)
        script = write(os.path.join(self.nowhere, "job.py"), "print('job')\n")
        with self.assertRaises(ConfigError):
            self.begin(root=runs, script=script)
        self.assertEqual(os.listdir(runs), [], "a refused begin() made a run directory")
        self.assertEqual(os.listdir(self.nowhere), ["job.py"])

    def test_a_run_reads_its_status_with_no_config_and_locates_only_to_resolve(self):
        d = self.a_config("")
        run = self.begin(client_root=d, checkpoint=True)
        self.assertEqual(
            run.manifest["checkpoint"],
            os.path.join("var", "runs", run.id, "checkpoint.jsonl"),
        )
        # from a directory with no config: what needs no root works
        again = runregistrykit.Run(run.path)
        self.assertEqual(again.status()["state"], "running")
        again.heartbeat(units_done=1)
        (listed,) = runregistrykit.list_runs(root=os.path.dirname(run.path))
        self.assertEqual(listed["id"], run.id)
        # a relative recorded path needs the root, and none is found from here
        with self.assertRaises(ConfigError):
            again.checkpoint_path
        with self.assertRaises(ConfigError):
            runregistrykit.list_runs()
        # given the client root, it resolves against the record root
        self.assertEqual(
            runregistrykit.Run(run.path, client_root=d).checkpoint_path,
            os.path.join(run.path, "checkpoint.jsonl"),
        )
        (listed,) = runregistrykit.list_runs(client_root=d)
        self.assertEqual(listed["id"], run.id)

    def test_a_live_sidecar_reads_with_no_config_and_a_tombstone_does_not(self):
        d = self.a_config(
            "[stores]\n"
            'fingerprinter = "runregistrykit.tests.neutral_store:FINGERPRINTER"\n'
        )
        primary = Path(write(os.path.join(d, "S", "store.sqlite")))
        fields = stores.create_sidecar(primary, "a store", client_root=d)
        self.assertTrue(stores.read_sidecar(primary).ok)

        create = fields["history"][0]
        retired = dict(
            fields,
            history=fields["history"]
            + [
                dict(
                    create, operation="retire", **{"from": "S/store.sqlite", "to": None}
                )
            ],
            retired={
                "state": "retired",
                "when": create["when"],
                "git_head": create["git_head"],
                "git_dirty": False,
                "reason": "disposable: a test",
                "fingerprint": {"condition": "matched", "digest": "a" * 64},
                "files": ["S/store.sqlite"],
                "files_present_only": False,
                "references": {
                    "runs_root": "var/runs",
                    "stores_root": "var/datastores",
                    "runs": [],
                    "sidecars": [],
                },
                "completed": create["when"],
            },
        )
        write(str(stores.sidecar_path(primary)), json.dumps(retired))
        primary.unlink()
        with self.assertRaises(ConfigError):
            stores.read_sidecar(primary)
        reading = stores.read_sidecar(primary, client_root=d)
        self.assertTrue(reading.retired)
        self.assertEqual(reading.problems, [])


class TestWorktree(ClientRootTestCase):
    """Q3: a run in a linked worktree is recorded under the main checkout, with its own tree's
    provenance."""

    def a_main_checkout_and_a_worktree(self):
        """A main checkout on one commit, and a linked worktree beside it on a second commit, so
        that the two heads, and the script in each, differ."""
        top = temporary_directory(self)
        main = write_client_root(os.path.join(top, "main"))
        write(os.path.join(main, "tools", "job.py"), "print('the main checkout')\n")
        main_head = commit_all(main, "a script")
        worktree = os.path.join(top, "wt")
        git(main, "branch", "side")
        git(main, "worktree", "add", "-q", worktree, "side")
        write(os.path.join(worktree, "tools", "job.py"), "print('the worktree')\n")
        worktree_head = commit_all(worktree, "the worktree's script")
        self.assertNotEqual(main_head, worktree_head)
        self.assertEqual(git(main, "rev-parse", "HEAD"), main_head)
        return main, worktree, worktree_head

    def test_a_run_in_a_linked_worktree_records_under_the_main_checkout(self):
        main, worktree, worktree_head = self.a_main_checkout_and_a_worktree()
        script = os.path.join(worktree, "tools", "job.py")

        run = self.begin(script=script)

        self.assertEqual(run.client_root.found, worktree)
        self.assertEqual(run.client_root.root, main)
        self.assertEqual(os.path.dirname(run.path), os.path.join(main, "var", "runs"))
        self.assertFalse(os.path.exists(os.path.join(worktree, "var")))
        # the worktree's own provenance, and its own script
        self.assertEqual(run.manifest["git_head"], worktree_head)
        self.assertIs(run.manifest["git_dirty"], False)
        self.assertEqual(run.manifest["script_sha256"], sha256(script))
        self.assertNotEqual(
            run.manifest["script_sha256"],
            sha256(os.path.join(main, "tools", "job.py")),
        )
        # outside the main checkout, so recorded by its absolute path
        self.assertEqual(run.manifest["script"], script)

    def test_a_config_in_a_subdirectory_maps_to_the_same_subdirectory(self):
        main, worktree, _ = self.a_main_checkout_and_a_worktree()
        write(os.path.join(worktree, "sub", CONFIG_FILE), 'runs_root = "runs"\n')
        start = os.path.join(worktree, "sub", "deeper")
        os.makedirs(start)

        client = find_client_root(start=start)

        self.assertEqual(client.found, os.path.join(worktree, "sub"))
        self.assertEqual(client.config_file, os.path.join(worktree, "sub", CONFIG_FILE))
        self.assertEqual(client.root, os.path.join(main, "sub"))
        self.assertEqual(client.runs_root, os.path.join(main, "sub", "runs"))

    def test_a_nested_worktree_without_a_config_walks_up_to_the_main_checkouts(self):
        top = temporary_directory(self)
        main = os.path.join(top, "main")
        os.makedirs(main)
        git(main, "init", "-q", "-b", "main")
        write(os.path.join(main, ".gitignore"), "var/\n")
        write(os.path.join(main, "job.py"), "print('the main checkout')\n")
        main_head = commit_all(main, "a script, and no config")
        nested = os.path.join(main, ".claude", "worktrees", "nest")
        git(main, "worktree", "add", "-q", "-b", "nest", nested)
        write(os.path.join(nested, "job.py"), "print('the nested worktree')\n")
        nested_head = commit_all(nested, "the nested worktree's script")
        # the main checkout's config is untracked, so no branch carries it
        write(os.path.join(main, CONFIG_FILE), "")
        self.assertFalse(os.path.exists(os.path.join(nested, CONFIG_FILE)))
        self.assertNotEqual(main_head, nested_head)
        script = os.path.join(nested, "job.py")

        run = self.begin(script=script)

        self.assertEqual(run.client_root.found, main)
        self.assertEqual(run.client_root.root, main)
        self.assertEqual(os.path.dirname(run.path), os.path.join(main, "var", "runs"))
        # nested in the main checkout, so recorded relative to it
        self.assertEqual(
            run.manifest["script"],
            os.path.join(".claude", "worktrees", "nest", "job.py"),
        )
        # provenance is the start directory's, the nested worktree, not the config's tree
        self.assertEqual(run.manifest["git_head"], nested_head)
        self.assertIs(run.manifest["git_dirty"], False)
        self.assertEqual(run.manifest["script_sha256"], sha256(script))

    def test_a_bare_repositorys_worktree_is_refused(self):
        top = temporary_directory(self)
        source = write_client_root(os.path.join(top, "source"))
        bare = os.path.join(top, "bare.git")
        git(top, "init", "-q", "--bare", "-b", "main", bare)
        git(source, "push", "-q", bare, "main")
        worktree = os.path.join(top, "bwt")
        git(bare, "worktree", "add", "-q", worktree, "main")
        self.assertTrue(os.path.isfile(os.path.join(worktree, CONFIG_FILE)))

        with self.assertRaises(ConfigError) as refused:
            find_client_root(start=worktree)
        self.assertIn(bare, str(refused.exception))
        self.assertIn("no main checkout", str(refused.exception))

        runs = temporary_directory(self)
        script = write(os.path.join(worktree, "job.py"), "print('job')\n")
        with self.assertRaises(ConfigError):
            self.begin(script=script, root=runs)
        self.assertEqual(os.listdir(runs), [])

    def test_a_directory_outside_any_repository_is_its_own_root(self):
        d = self.a_config("")
        script = write(os.path.join(d, "job.py"), "print('job')\n")

        run = self.begin(script=script)

        self.assertEqual(run.client_root.root, d)
        self.assertEqual(os.path.dirname(run.path), os.path.join(d, "var", "runs"))
        self.assertEqual(run.manifest["script"], "job.py")
        self.assertEqual(run.manifest["git_head"], "unknown")
        self.assertIs(run.manifest["git_dirty"], False)


class TestStoresUnderTheRoot(unittest.TestCase):
    """A store under the client root, operated on from a subdirectory of it."""

    def setUp(self):
        self.client = enter_client_root(self)
        self.sub = os.path.join(self.client, "sub")
        os.makedirs(self.sub)
        os.chdir(self.sub)  # the fixture's cleanup restores the working directory

    def a_store(self, name) -> Path:
        primary = Path(self.client) / "var" / "datastores" / name / "store.sqlite"
        write_new_store(primary, shards=2)
        stores.create_sidecar(primary, "a store under the client root")
        return primary

    def test_a_store_under_the_root_records_root_relative_paths(self):
        primary = self.a_store("S")
        relative = os.path.join("var", "datastores", "S", "store.sqlite")
        (entry,) = stores.read_sidecar(primary).fields["history"]
        self.assertEqual(entry["to"], relative)
        self.assertEqual(entry["git_head"], git(self.client, "rev-parse", "HEAD"))

        run = runregistrykit.begin(
            campaign="client-root",
            prompt="03",
            slug="under-the-root",
            purpose="a run whose results are under the client root",
            argv=["unittest"],
            results=str(primary),
        )
        self.assertEqual(run.manifest["results"], relative)
        self.assertEqual(
            os.path.dirname(run.path), os.path.join(self.client, "var", "runs")
        )
        run.finish("done", exit_code=0)
        # the recorded relative path is resolved against the root, not the working directory
        (named,) = stores.runs_naming([primary])
        self.assertEqual(named["id"], run.id)
        self.assertIn("results", named["matched_by"])

        copy = Path(self.client) / "var" / "datastores" / "T" / "copy.sqlite"
        fields = stores.copy_store(primary, copy, "a copy under the client root")
        self.assertEqual(fields["copied_from"]["datastore"], relative)
        entry = fields["history"][-1]
        self.assertEqual(
            (entry["from"], entry["to"]),
            (relative, os.path.join("var", "datastores", "T", "copy.sqlite")),
        )

    def test_a_tombstones_relative_files_are_resolved_against_the_root(self):
        primary = self.a_store("R")
        shards = [primary.parent / shard_file_name(primary, i) for i in range(2)]
        listed = [os.path.relpath(path, self.client) for path in shards + [primary]]
        self.assertFalse(any(os.path.isabs(path) for path in listed))
        fields = json.loads(stores.sidecar_path(primary).read_text())
        create = fields["history"][0]
        tombstone = dict(
            fields,
            history=fields["history"]
            + [dict(create, operation="retire", **{"from": listed[-1], "to": None})],
            retired={
                "state": "retired",
                "when": create["when"],
                "git_head": create["git_head"],
                "git_dirty": False,
                "reason": "disposable: a test",
                "fingerprint": {"condition": "matched", "digest": "a" * 64},
                "files": listed,
                "files_present_only": False,
                "references": {
                    "runs_root": "var/runs",
                    "stores_root": "var/datastores",
                    "runs": [],
                    "sidecars": [],
                },
                "completed": create["when"],
            },
        )
        stores.sidecar_path(primary).write_text(json.dumps(tombstone))
        # every file gone but one shard, which is not the primary
        primary.unlink()
        shards[1].unlink()

        reading = stores.read_sidecar(primary)

        self.assertTrue(reading.retired)
        self.assertEqual(len(reading.problems), 1, reading.problems)
        self.assertIn(f'"{shards[0]}" exists again', reading.problems[0])

        shards[0].unlink()
        self.assertEqual(stores.read_sidecar(primary).problems, [])


class TestCommandLine(ClientRootTestCase):
    """`python -m runregistrykit` under a client root, and outside one."""

    def command(self, cwd, *argv):
        return subprocess.run(
            [sys.executable, "-m", "runregistrykit", *[str(a) for a in argv]],
            capture_output=True,
            text=True,
            cwd=cwd,
            env={**os.environ, "PYTHONPATH": PACKAGE_PARENT},
            timeout=300,
        )

    def a_client_with_a_run(self):
        client = write_client_root(
            os.path.join(temporary_directory(self), "client"), 'runs_root = "records"\n'
        )
        run = self.begin(client_root=client)
        self.assertEqual(os.path.dirname(run.path), os.path.join(client, "records"))
        return client, run

    def test_client_root_names_the_root_from_anywhere(self):
        client, run = self.a_client_with_a_run()
        done = self.command(self.nowhere, "--client-root", client, "list")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn(run.id, done.stdout)
        self.assertIn(f"run(s) under {os.path.join(client, 'records')}:", done.stdout)

    def test_list_from_inside_a_client_lists_its_runs_root(self):
        client, run = self.a_client_with_a_run()
        inside = os.path.join(client, "deep", "er")
        os.makedirs(inside)
        done = self.command(inside, "list")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn(run.id, done.stdout)
        self.assertIn(f"run(s) under {os.path.join(client, 'records')}:", done.stdout)

    def test_outside_any_client_a_store_command_exits_1_and_writes_nothing(self):
        primary = write(os.path.join(self.nowhere, "store.sqlite"))
        for argv in (
            ("store", "create", primary, "--purpose", "p"),
            ("store", "show", primary),
            ("list",),
        ):
            with self.subTest(argv[:2]):
                done = self.command(self.nowhere, *argv)
                self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
                self.assertTrue(
                    done.stderr.startswith(f"!! No {CONFIG_FILE} in {self.nowhere}"),
                    done.stderr,
                )
                self.assertEqual(os.listdir(self.nowhere), ["store.sqlite"])
        # an explicit runs root needs no config
        runs = temporary_directory(self)
        done = self.command(self.nowhere, "list", "--root", runs)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn(f"no runs under {runs}", done.stdout)


class TestRecordedDistributions(ClientRootTestCase):
    """U9: `runregistrykit` is always recorded, besides the config's distributions."""

    def test_packages_holds_the_registry_and_the_configs_distributions_once_each(self):
        d = self.a_config('distributions = ["datastorekit", "runregistrykit"]\n')
        run = self.begin(client_root=d, root=temporary_directory(self))
        self.assertEqual(
            sorted(run.manifest["packages"]), ["datastorekit", "runregistrykit"]
        )
        self.assertEqual(
            run.manifest["packages"],
            runregistrykit.package_provenance(("runregistrykit", "datastorekit")),
        )
        self.assertEqual(
            runregistrykit._recorded_names(find_client_root(client_root=d)),
            ("runregistrykit", "datastorekit"),
        )


class TestNothingAtImport(ClientRootTestCase):
    def test_import_reads_no_config(self):
        # a config that every read refuses, in the working directory of a fresh interpreter
        write(os.path.join(self.nowhere, CONFIG_FILE), "this is not TOML\n")
        done = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                "import runregistrykit, runregistrykit.stores, runregistrykit.__main__",
            ],
            capture_output=True,
            text=True,
            cwd=self.nowhere,
            timeout=120,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        with self.assertRaises(ConfigError):
            find_client_root()


if __name__ == "__main__":
    unittest.main()
