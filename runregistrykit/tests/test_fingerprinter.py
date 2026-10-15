"""The client fingerprinter (`runregistrykit.fingerprint`): the protocol, the shipped
`DatastoreKitFingerprinter`, the loader and the config key; the store layer's need of one (D4); what
the package reads of a fingerprint (U7); the neutral store; and two guards of the sidecar reader.

Every directory is a `tempfile` one, and every client root is built in one (`client_fixtures`). A
module a test writes into a client root has a name no other test uses, and the test restores
`sys.path` and drops the module from `sys.modules` when it ends. No Ray is initialised.
"""

import ast
import errno
import importlib.util
import json
import os
import sys
import unittest
import uuid
from pathlib import Path
from unittest import mock

from runregistrykit import stores
from runregistrykit.client import CONFIG_FILE, ConfigError, find_client_root
from runregistrykit.fingerprint import (
    DatastoreKitFingerprinter,
    Fingerprinter,
    load_fingerprinter,
    require_fingerprinter,
)
from runregistrykit.tests import neutral_store
from runregistrykit.tests import test_store_fingerprint as ported
from runregistrykit.tests.client_fixtures import enter_client_root
from runregistrykit.tests.neutral_store import (
    FACTORIES,
    FINGERPRINTER,
    build_full_store,
)
from runregistrykit.tests.store_fixtures import (
    StoreTestCase,
    load,
    sweep_shaped,
    write_sidecar_json,
)
from runregistrykit.tests.test_store_command_line import CommandLineTestCase

from datastorekit.SQL.ShardedPool import ShardedPool
from datastorekit.SQL.schema import StoreSchemaMismatch
from datastorekit.store_fingerprint import ENCODING_FORMAT, fingerprint_of
from datastorekit.store_inventory import read_inventory

NEUTRAL_SPEC = "runregistrykit.tests.neutral_store:FINGERPRINTER"

# a fingerprinter of a client's own, written into a client root: it reads nothing, and records
# what the package hands it
STUB = """\
class Stub:
    def __init__(self):
        self.calls = []

    def take(self, primary, taken):
        self.calls.append(("take", str(primary), dict(taken)))
        fingerprint = {
            "fingerprint_format": 9,
            "digest": "e" * 64,
            "taken": taken,
            "the stub's own": ["opaque", {"to": "the package"}],
        }
        return fingerprint, "the stub's inventory"

    def compare(self, recorded, current):
        self.calls.append(("compare", recorded, current))
        return [{"kind": "stub", "text": "the stub compared them", "more": 1}]

    def describe(self, fingerprint):
        return ["described by the stub"]

    def listing(self, inventory, fingerprint):
        yield f"listed by the stub, from {inventory}"


STUB = Stub()
"""


def a_module_name(test) -> str:
    """A module name no other test uses. When ``test`` ends, `sys.path` is restored and the module
    dropped from `sys.modules`."""
    name = f"client_fingerprinter_{uuid.uuid4().hex}"
    saved = list(sys.path)

    def restore():
        sys.path[:] = saved
        sys.modules.pop(name, None)

    test.addCleanup(restore)
    return name


def write_module(directory, name, body) -> str:
    path = os.path.join(directory, f"{name}.py")
    with open(path, "w") as handle:
        handle.write(body)
    return path


def config_naming(spec) -> str:
    return f'[stores]\nfingerprinter = "{spec}"\n'


def a_tombstone(primary: Path) -> None:
    """Turn ``primary``'s registry sidecar into a completed tombstone, by hand, and remove the
    primary it lists."""
    fields = load(stores.sidecar_path(primary))
    create = fields["history"][0]
    fields["history"] = fields["history"] + [
        dict(create, operation="retire", **{"from": str(primary), "to": None})
    ]
    fields["retired"] = {
        "state": "retired",
        "when": create["when"],
        "git_head": create["git_head"],
        "git_dirty": False,
        "reason": "disposable: a test",
        "fingerprint": {"condition": "matched", "digest": "a" * 64},
        "files": [str(primary)],
        "files_present_only": False,
        "references": {
            "runs_root": "var/runs",
            "stores_root": "var/datastores",
            "runs": [],
            "sidecars": [],
        },
        "completed": create["when"],
    }
    write_sidecar_json(primary, fields)
    primary.unlink()


class TestProtocolAndLoader(unittest.TestCase):
    """The protocol, the shipped fingerprinter, and `load_fingerprinter`."""

    def test_the_shipped_fingerprinter_is_a_fingerprinter(self):
        self.assertIsInstance(FINGERPRINTER, Fingerprinter)
        self.assertIsInstance(DatastoreKitFingerprinter({}, 3), Fingerprinter)
        self.assertIs(FINGERPRINTER.factories, FACTORIES)
        self.assertEqual(FINGERPRINTER.fingerprint_format, 1)
        self.assertNotIsInstance(FACTORIES, Fingerprinter)

    def test_the_constructor_refuses_a_bad_format_as_fingerprint_of_does(self):
        for bad, kind in (
            (True, TypeError),
            (False, TypeError),
            ("1", TypeError),
            (1.0, TypeError),
            (None, TypeError),
            (0, ValueError),
            (-1, ValueError),
        ):
            with self.subTest(fingerprint_format=bad):
                with self.assertRaises(kind) as refused:
                    DatastoreKitFingerprinter(FACTORIES, bad)
                self.assertIn("fingerprint_format", str(refused.exception))
                self.assertIn(repr(bad), str(refused.exception))
                with self.assertRaises(kind):
                    fingerprint_of(None, bad)

    def test_describe_points_a_problem_to_the_stores_inventory_reader(self):
        fingerprint = {
            "classes": {"Alpha": {"count": 3, "digest": "a" * 64, "tag_sets": []}},
            "problems": {"Alpha": {"unreadable": 2}},
        }
        lines = FINGERPRINTER.describe(fingerprint)
        self.assertIn(
            "problems: (counts only; the store's own text is in the store's inventory, "
            "which `datastorekit.store_inventory.read_inventory` returns)",
            lines,
        )
        self.assertIn("  !! Alpha: unreadable 2", lines)
        self.assertNotIn("problems: none", lines)
        self.assertFalse([line for line in lines if ".py" in line])

    def test_module_and_attribute_are_resolved(self):
        a_module_name(self)  # for its cleanup: the loader puts the root on sys.path
        enter_client_root(self)
        self.assertEqual(require_fingerprinter(find_client_root()), NEUTRAL_SPEC)
        self.assertIs(load_fingerprinter(find_client_root()), FINGERPRINTER)

    def test_a_dotted_attribute_is_resolved(self):
        name = a_module_name(self)
        client = enter_client_root(
            self, config_naming(f"{name}:Holder.Inner.fingerprinter")
        )
        write_module(
            client,
            name,
            "from runregistrykit.tests.neutral_store import FINGERPRINTER\n\n\n"
            "class Holder:\n"
            "    class Inner:\n"
            "        fingerprinter = FINGERPRINTER\n",
        )
        self.assertIs(load_fingerprinter(find_client_root()), FINGERPRINTER)

    def test_a_module_in_the_client_root_is_found_from_a_subdirectory(self):
        name = a_module_name(self)
        client = enter_client_root(self, config_naming(f"{name}:STUB"))
        write_module(client, name, STUB)
        sub = os.path.join(client, "a", "b")
        os.makedirs(sub)
        os.chdir(sub)  # the fixture's cleanup restores the working directory
        # nothing but the loader puts the client root on the path
        self.assertNotIn(client, sys.path)
        self.assertIsNone(importlib.util.find_spec(name))

        found = load_fingerprinter(find_client_root())

        self.assertIsInstance(found, Fingerprinter)
        self.assertEqual(type(found).__name__, "Stub")
        self.assertIs(found, sys.modules[name].STUB)
        # the tree that is running, first on the path, and left there
        self.assertEqual(sys.path[0], client)

    def test_each_refusal_is_a_config_error_naming_the_file(self):
        broken = a_module_name(self)
        cases = {
            "none named": ("", None, ["names no fingerprinter", "[stores]"]),
            "no such module": (
                config_naming("no_such_module_anywhere_04a:F"),
                None,
                ["no_such_module_anywhere_04a:F", "ModuleNotFoundError"],
            ),
            "a module that raises": (
                config_naming(f"{broken}:F"),
                'raise RuntimeError("broken on purpose")\n',
                [f"{broken}:F", "RuntimeError: broken on purpose"],
            ),
            "no such attribute": (
                config_naming("runregistrykit.tests.neutral_store:NO_SUCH"),
                None,
                ["neutral_store:NO_SUCH", "no attribute"],
            ),
            "not a fingerprinter": (
                config_naming("runregistrykit.tests.neutral_store:FACTORIES"),
                None,
                ["neutral_store:FACTORIES", "not a Fingerprinter"],
            ),
        }
        for label, (config, module, fragments) in cases.items():
            with self.subTest(label):
                client = enter_client_root(self, config)
                if module is not None:
                    write_module(client, broken, module)
                with self.assertRaises(ConfigError) as refused:
                    load_fingerprinter(find_client_root())
                message = str(refused.exception)
                self.assertIn(os.path.join(client, CONFIG_FILE), message)
                for fragment in fragments:
                    self.assertIn(fragment, message)

    def test_a_class_is_refused_and_an_instance_of_it_loads(self):
        """U14 (b): a class with the four methods passes the protocol's check, so the loader
        refuses a class before it; the shipped class, and a client's own."""
        name = a_module_name(self)
        for spec in (
            "runregistrykit.fingerprint:DatastoreKitFingerprinter",
            f"{name}:Stub",
        ):
            with self.subTest(spec):
                client = enter_client_root(self, config_naming(spec))
                write_module(client, name, STUB)
                with self.assertRaises(ConfigError) as refused:
                    load_fingerprinter(find_client_root())
                message = str(refused.exception)
                self.assertIn(os.path.join(client, CONFIG_FILE), message)
                self.assertIn(spec, message)
                self.assertIn("is the class", message)
                self.assertIn("not an instance of it", message)
        # a precondition: each class passes the protocol's check, which is why it is refused first
        self.assertIsInstance(DatastoreKitFingerprinter, Fingerprinter)
        self.assertIsInstance(sys.modules[name].Stub, Fingerprinter)

        enter_client_root(self, config_naming(f"{name}:STUB"))
        self.assertIs(load_fingerprinter(find_client_root()), sys.modules[name].STUB)

    def test_the_config_refuses_a_bad_fingerprinter_or_another_key_when_read(self):
        accepted = ("a:b", "a.b.c:d.e", "_x:_y", NEUTRAL_SPEC)
        for spec in accepted:
            with self.subTest(accepted=spec):
                client = enter_client_root(self, config_naming(spec))
                self.assertEqual(find_client_root().stores, {"fingerprinter": spec})
        refused = {
            "an integer": ("[stores]\nfingerprinter = 1\n", "fingerprinter", "1"),
            "empty": (config_naming(""), "fingerprinter", "''"),
            "no colon": (config_naming("module"), "fingerprinter", "'module'"),
            "two colons": (config_naming("a:b:c"), "fingerprinter", "'a:b:c'"),
            "no module": (config_naming(":b"), "fingerprinter", "':b'"),
            "no attribute": (config_naming("a:"), "fingerprinter", "'a:'"),
            "an empty part": (config_naming("a..b:c"), "fingerprinter", "'a..b:c'"),
            "a trailing dot": (config_naming("a:b."), "fingerprinter", "'a:b.'"),
            "whitespace": (config_naming("a b:c"), "fingerprinter", "'a b:c'"),
            "a space after the colon": (
                config_naming("a: b"),
                "fingerprinter",
                "'a: b'",
            ),
            "not an identifier": (config_naming("1a:b"), "fingerprinter", "'1a:b'"),
            "another key": ('[stores]\nother = "x"\n', "'other'", "'x'"),
        }
        for label, (config, key, value) in refused.items():
            with self.subTest(refused=label):
                client = enter_client_root(self, config)
                with self.assertRaises(ConfigError) as caught:
                    find_client_root()
                message = str(caught.exception)
                self.assertIn(os.path.join(client, CONFIG_FILE), message)
                self.assertIn(key, message)
                self.assertIn(value, message)


class _NoFingerprinterCase(CommandLineTestCase):
    """Stores made under a config that names the neutral fingerprinter, then a client root whose
    config names none, made the working directory."""

    def setUp(self):
        super().setUp()
        self.registry = self.a_registry_store("R")
        self.bare = self.a_store("N")
        self.legacy = self.a_store("L")
        write_sidecar_json(self.legacy, sweep_shaped(self.top / "X"))
        self.client = enter_client_root(self, "")
        self.config = os.path.join(self.client, CONFIG_FILE)

    def assertNamesNoFingerprinter(self, message):
        self.assertIn(self.config, message)
        self.assertIn("names no fingerprinter", message)


class TestTheStoreLayerRequiresOne(_NoFingerprinterCase):
    """D4: every store operation, and every store command, refuses before anything else."""

    def test_each_store_operation_is_refused_and_writes_nothing(self):
        listing = self.top / "listing.txt"
        cases = {
            "create": lambda: stores.create_sidecar(self.bare, "a purpose"),
            "adopt": lambda: stores.adopt_sidecar(self.legacy, "a purpose"),
            "copy": lambda: stores.copy_store(
                self.registry, self.top / "C" / "c.sqlite", "p", runs_root=self.root
            ),
            "move": lambda: stores.move_store(
                self.registry, self.top / "D" / "d.sqlite", runs_root=self.root
            ),
            "fingerprint": lambda: stores.fingerprint_store(
                self.registry, runs_root=self.root
            ),
            "fingerprint --write": lambda: stores.fingerprint_store(
                self.registry, write=True, runs_root=self.root
            ),
            "retire": lambda: stores.retire_store(
                self.registry, "a reason", runs_root=self.root
            ),
            "retire --without-fingerprint": lambda: stores.retire_store(
                self.registry, "a reason", runs_root=self.root, without_fingerprint=True
            ),
            "amend": lambda: stores.amend_sidecar(
                self.registry, "note", "a reason", value=1, runs_root=self.root
            ),
            "write_listing": lambda: stores.write_listing(
                None, None, listing, self.registry
            ),
        }
        for label, call in cases.items():
            with self.subTest(label):
                before = self.state()
                with self.assertRaises(ConfigError) as refused:
                    call()
                self.assertNamesNoFingerprinter(str(refused.exception))
                self.assertEqual(self.state(), before, f"a refused {label} wrote")
        self.assertFalse(listing.exists())

    def test_every_store_command_is_refused(self):
        runs = ("--runs-root", self.root)
        registry = self.registry
        for argv in (
            ("show", registry, *runs),
            ("create", self.bare, "--purpose", "p"),
            ("adopt", self.legacy, "--purpose", "p"),
            ("copy", registry, self.top / "C" / "c.sqlite", "--purpose", "p", *runs),
            ("move", registry, self.top / "D" / "d.sqlite", *runs),
            ("fingerprint", registry, *runs),
            ("retire", registry, "--reason", "r", "--without-fingerprint", *runs),
            ("amend", registry, "--field", "n", "--json", "1", "--reason", "r", *runs),
        ):
            with self.subTest(argv[0]):
                self.assertNamesNoFingerprinter(self.refused("store", *argv))

    def test_the_core_needs_none(self):
        reading = stores.read_sidecar(self.registry)
        self.assertTrue(reading.ok, reading.problems)
        sidecar = stores.sidecar_path(self.registry).read_bytes()

        run = self.begin("no-fingerprinter", results=str(self.registry))
        self.assertEqual(run.manifest["results_store_id"], reading.store_id)
        status = run.finish("done", exit_code=0, fingerprint=True)

        self.assertEqual((status["state"], status["exit_code"]), ("done", 0))
        self.assertNotIn("fingerprint", status)
        self.assertTrue(status["fingerprint_error"].startswith("ConfigError: "))
        self.assertNamesNoFingerprinter(status["fingerprint_error"])
        self.assertEqual(stores.sidecar_path(self.registry).read_bytes(), sidecar)


class TestPrecedence(CommandLineTestCase):
    """The config check imports nothing, and the fingerprinter is loaded only after a tombstone
    and a running run have been refused: a config naming a module that exists nowhere.
    """

    def setUp(self):
        super().setUp()
        self.spec = f"no_such_module_{uuid.uuid4().hex}:FINGERPRINTER"
        self.client = enter_client_root(self, config_naming(self.spec))

    def test_the_check_imports_nothing(self):
        primary = self.a_registry_store("S")
        self.assertTrue(stores.read_sidecar(primary).ok)
        report, out, err = self.command(
            "store", "show", primary, "--runs-root", self.root
        )
        self.assertEqual(report["code"], 0, err)
        self.assertIn("kind:     registry", out)

    def test_a_tombstone_and_a_running_run_come_before_the_fingerprinter(self):
        primary = self.a_registry_store("S")
        # with nothing to refuse first, the fingerprinter is loaded, and cannot be
        with self.assertRaises(ConfigError) as refused:
            stores.fingerprint_store(primary, runs_root=self.root)
        self.assertIn(self.spec, str(refused.exception))
        self.assertIn("ModuleNotFoundError", str(refused.exception))

        run = self.a_running_run("in-use", primary)
        with self.assertRaises(RuntimeError) as refused:
            stores.fingerprint_store(primary, runs_root=self.root)
        self.assertNotIsInstance(refused.exception, ConfigError)
        self.assertIn(run.id, str(refused.exception))
        err = self.refused("store", "fingerprint", primary, "--runs-root", self.root)
        self.assertIn(run.id, err)
        self.assertNotIn(self.spec, err)
        run.finish("killed")

        gone = self.a_registry_store("T")
        a_tombstone(gone)
        self.assertTrue(stores.read_sidecar(gone).retired)
        with self.assertRaises(RuntimeError) as refused:
            stores.fingerprint_store(gone, runs_root=self.root)
        self.assertNotIsInstance(refused.exception, ConfigError)
        self.assertIn("is a tombstone", str(refused.exception))


class _RetireCase(CommandLineTestCase):
    """A full four-shard store under a stores root of its own, with a registry sidecar and a
    fingerprint recorded while the config named the neutral fingerprinter. `enter_config` then
    makes a client root whose config names another fingerprinter, by default one that cannot be
    loaded, the working directory.
    """

    REASON = "disposable: a test"

    def setUp(self):
        super().setUp()
        self.stores_root = str(self.top / "datastores")
        os.makedirs(self.stores_root)
        self.primary = self.a_full_store("S")

    def a_full_store(self, directory):
        parent = Path(self.stores_root) / directory
        parent.mkdir()
        primary = build_full_store(parent, stem="store", shards=4).primary
        stores.create_sidecar(primary, "a full store in a temporary directory")
        stores.fingerprint_store(primary, write=True, runs_root=self.root)
        return primary

    def enter_config(self, spec=None):
        """A config naming ``spec``, by default a module that exists nowhere: a fresh name, whose
        cleanup restores `sys.path`, which the loader changes."""
        self.spec = spec or f"{a_module_name(self)}:FINGERPRINTER"
        if spec is not None:
            a_module_name(self)  # for its cleanup alone
        self.client = enter_client_root(self, config_naming(self.spec))
        self.config = os.path.join(self.client, CONFIG_FILE)

    def retire(self, primary=None, reason=REASON, **kwargs):
        return stores.retire_store(
            primary or self.primary,
            reason,
            runs_root=self.root,
            stores_root=self.stores_root,
            **kwargs,
        )

    def sidecar_bytes(self, primary=None):
        return stores.sidecar_path(primary or self.primary).read_bytes()


class TestRetireLoadsTheFingerprinterFirst(_RetireCase):
    """U14 (a): on a first retirement a fingerprinter that cannot be loaded is a refusal, a
    `ConfigError` as the loader raised it, before anything is written, with the flag or without;
    never the `--without-fingerprint` condition. The store could be fingerprinted with the right
    config."""

    CASES = {
        "a module that exists nowhere": (None, "ModuleNotFoundError"),
        "the class": (
            "runregistrykit.fingerprint:DatastoreKitFingerprinter",
            "not an instance of it",
        ),
    }

    def test_retire_store_raises_the_config_error_and_changes_nothing(self):
        for label, (spec, fragment) in self.CASES.items():
            self.enter_config(spec)
            for kwargs in (
                {},
                {"without_fingerprint": True},
                {"dry_run": True},
                {"without_fingerprint": True, "dry_run": True},
            ):
                with self.subTest(label, **kwargs):
                    before, sidecar = self.state(), self.sidecar_bytes()
                    with self.assertRaises(ConfigError) as refused:
                        self.retire(**kwargs)
                    message = str(refused.exception)
                    self.assertIn(self.config, message)
                    self.assertIn(self.spec, message)
                    self.assertIn(fragment, message)
                    self.assertNotIn("a fresh fingerprint could not be taken", message)
                    self.assertEqual(self.state(), before)
                    self.assertEqual(self.sidecar_bytes(), sidecar)
        self.assertTrue(stores.read_sidecar(self.primary).ok)

    def test_store_retire_without_fingerprint_exits_1_naming_the_config_file(self):
        for label, (spec, fragment) in self.CASES.items():
            with self.subTest(label):
                self.enter_config(spec)
                before, sidecar = self.state(), self.sidecar_bytes()
                report, _, err = self.command(
                    "store",
                    "retire",
                    self.primary,
                    "--reason",
                    self.REASON,
                    "--without-fingerprint",
                    "--runs-root",
                    self.root,
                    "--stores-root",
                    self.stores_root,
                )
                self.assertEqual(report["code"], 1, err)
                self.assertIn("!!", err)
                self.assertIn(self.config, err)
                self.assertIn(self.spec, err)
                self.assertIn(fragment, err)
                self.assertEqual(self.state(), before)
                self.assertEqual(self.sidecar_bytes(), sidecar)


class TestRetirePrecedence(_RetireCase):
    """Where `retire_store` loads the fingerprinter: after the reason and sidecar refusals and the
    in-use refusal, before the plan of the files, and not on the completion of an incomplete
    retirement, which takes no fingerprint. A config naming a module that exists nowhere.
    """

    FLAGS = (False, True)

    def assertRefusedNotForTheConfig(self, *fragments, **kwargs):
        before = self.state()
        with self.assertRaises(RuntimeError) as refused:
            self.retire(**kwargs)
        self.assertNotIsInstance(refused.exception, ConfigError)
        message = str(refused.exception)
        self.assertNotIn(self.spec, message)
        self.assertTrue(message.endswith("Nothing was written or deleted"), message)
        self.assertNamesAndNothingChanged(before, refused.exception, *fragments)

    def test_the_reason_comes_first(self):
        self.enter_config()
        for flag in self.FLAGS:
            with self.subTest(without_fingerprint=flag):
                self.assertRefusedNotForTheConfig(
                    "a reason is required", reason="  ", without_fingerprint=flag
                )

    def test_a_running_run_comes_first(self):
        run = self.a_running_run("in-use", self.primary)
        self.enter_config()
        for flag in self.FLAGS:
            with self.subTest(without_fingerprint=flag):
                self.assertRefusedNotForTheConfig(run.id, without_fingerprint=flag)
        run.finish("killed")

    def test_a_completed_tombstone_comes_first(self):
        self.retire()
        self.enter_config()
        for flag in self.FLAGS:
            with self.subTest(without_fingerprint=flag):
                self.assertRefusedNotForTheConfig(
                    "already retired", without_fingerprint=flag
                )

    def test_the_fingerprinter_comes_before_the_plan(self):
        """A `-wal` beside the primary, which the plan refuses: the load comes first."""
        Path(str(self.primary) + "-wal").write_bytes(b"")
        self.enter_config()
        for flag in self.FLAGS:
            with self.subTest(without_fingerprint=flag):
                before = self.state()
                with self.assertRaises(ConfigError) as refused:
                    self.retire(without_fingerprint=flag)
                self.assertIn(self.spec, str(refused.exception))
                self.assertNotIn("-wal", str(refused.exception))
                self.assertEqual(self.state(), before)

    def test_a_completion_loads_no_fingerprinter(self):
        """An incomplete retirement made under the neutral fingerprinter completes under the
        broken config, with the flag and without, deleting what remained."""
        for flag in self.FLAGS:
            with self.subTest(without_fingerprint=flag):
                self.enter_config(NEUTRAL_SPEC)
                primary = self.a_full_store(f"I{flag}")
                real, calls = os.unlink, []

                def second_fails(path, *args, **kwargs):
                    calls.append(path)
                    if len(calls) == 2:
                        raise OSError(errno.EIO, "injected failure", str(path))
                    return real(path, *args, **kwargs)

                with mock.patch("os.unlink", second_fails):
                    with self.assertRaises(RuntimeError):
                        self.retire(primary)
                self.assertIsNotNone(stores.read_sidecar(primary).incomplete_retirement)

                self.enter_config()
                result = self.retire(primary, without_fingerprint=flag)
                self.assertTrue(result["completing"])
                self.assertEqual(len(result["deleted"]), 4)
                reading = stores.read_sidecar(primary)
                self.assertTrue(reading.retired)
                self.assertEqual(reading.problems, [])
                self.assertEqual(os.listdir(primary.parent), ["store.manifest.json"])


class TestOpacity(StoreTestCase):
    """U7: the sidecar reader reads a fingerprint's format, digest and `taken`, and its
    `encoding_format` only if present."""

    def with_fingerprint(self, primary, value):
        fields = load(stores.sidecar_path(primary))
        fields["fingerprint"] = value
        write_sidecar_json(primary, fields)

    def test_format_digest_and_taken_are_enough(self):
        minimal = {"fingerprint_format": 3, "digest": "a" * 64, "taken": {}}
        for label, value in {
            "the three": minimal,
            "with encoding_format": dict(minimal, encoding_format=1),
            "with anything else": dict(minimal, classes=[], problems="x", more=[1]),
        }.items():
            with self.subTest(label):
                primary = self.a_registry_store(label.replace(" ", "-"))
                self.with_fingerprint(primary, value)
                reading = stores.read_sidecar(primary)
                self.assertTrue(reading.ok, reading.problems)

    def test_encoding_format_if_present_is_an_integer(self):
        minimal = {"fingerprint_format": 3, "digest": "a" * 64, "taken": {}}
        for index, value in enumerate(("1", True, 1.0, None)):
            with self.subTest(encoding_format=value):
                primary = self.a_registry_store(f"E{index}")
                self.with_fingerprint(primary, dict(minimal, encoding_format=value))
                reading = stores.read_sidecar(primary)
                self.assertFalse(reading.ok)
                self.assertIn(
                    f"fingerprint's encoding_format {value!r} is not an integer",
                    reading.problems,
                )


class TestThroughTheFingerprinter(CommandLineTestCase):
    """`fingerprint_store`, `write_listing` and `store fingerprint` go through the client's
    fingerprinter, and nothing else."""

    def a_full_store(self, directory="F"):
        (self.top / directory).mkdir()
        primary = build_full_store(self.top / directory, stem="store").primary
        stores.create_sidecar(primary, "a full store in a temporary directory")
        return primary

    def test_what_the_client_fingerprinter_takes_is_recorded(self):
        name = a_module_name(self)
        self.client = enter_client_root(self, config_naming(f"{name}:STUB"))
        write_module(self.client, name, STUB)
        primary = self.a_registry_store("S")

        result = stores.fingerprint_store(primary, write=True, runs_root=self.root)

        stub = sys.modules[name].STUB
        ((call, taken_from, taken),) = stub.calls
        self.assertEqual((call, taken_from), ("take", str(primary)))
        self.assertEqual(set(taken), set(stores.TAKEN_KEYS))
        self.assertEqual(result["fingerprint"]["taken"], taken)
        self.assertEqual(result["inventory"], "the stub's inventory")
        self.assertIsNone(result["comparison"])
        recorded = load(stores.sidecar_path(primary))["fingerprint"]
        self.assertEqual(recorded, result["fingerprint"])
        self.assertEqual(recorded["the stub's own"], ["opaque", {"to": "the package"}])
        # no classes and no encoding_format: the reader asks for neither
        self.assertTrue(stores.read_sidecar(primary).ok)

        again = stores.fingerprint_store(primary, runs_root=self.root)
        self.assertEqual(stub.calls[-1], ("compare", recorded, again["fingerprint"]))
        self.assertEqual(
            again["comparison"],
            [{"kind": "stub", "text": "the stub compared them", "more": 1}],
        )

        listing = self.top / "listing.txt"
        stores.write_listing(
            result["inventory"], result["fingerprint"], listing, primary
        )
        self.assertEqual(
            listing.read_text(), "listed by the stub, from the stub's inventory\n"
        )

    def test_a_recorded_fingerprint_without_encoding_format_is_not_compared(self):
        primary = self.a_full_store()
        stores.fingerprint_store(primary, write=True, runs_root=self.root)
        fields = load(stores.sidecar_path(primary))
        self.assertEqual(fields["fingerprint"]["encoding_format"], ENCODING_FORMAT)
        del fields["fingerprint"]["encoding_format"]
        write_sidecar_json(primary, fields)
        self.assertTrue(stores.read_sidecar(primary).ok)

        (entry,) = stores.fingerprint_store(primary, runs_root=self.root)["comparison"]
        self.assertEqual(entry["kind"], "encoding")
        self.assertEqual((entry["recorded"], entry["current"]), (None, ENCODING_FORMAT))

        report, out, err = self.command(
            "store", "fingerprint", primary, "--runs-root", self.root
        )
        self.assertEqual(report["code"], 1, err)
        self.assertIn("recorded: 1 difference(s) from the recorded fingerprint:", out)
        self.assertIn(f"  !! {entry['text']}", out)

    def test_a_read_refusal_comes_through_as_the_readers_own(self):
        journal = self.a_full_store("J")
        Path(str(journal.parent / "store-shard0000.sqlite") + "-journal").write_bytes(
            b""
        )
        (self.top / "M").mkdir()
        mismatched = build_full_store(
            self.top / "M",
            stem="store",
            extra_sql={1: [f'DROP TABLE "{neutral_store.INTEGRAL_TAGS}"']},
        ).primary
        for label, primary in (("a journal", journal), ("a missing table", mismatched)):
            with self.subTest(label):
                with self.assertRaises(Exception) as caught:
                    read_inventory(primary, FACTORIES)
                direct = caught.exception
                if label == "a missing table":
                    self.assertIsInstance(direct, StoreSchemaMismatch)
                with self.assertRaises(Exception) as caught:
                    stores.fingerprint_store(primary, runs_root=self.root)
                self.assertIs(type(caught.exception), type(direct))
                self.assertEqual(str(caught.exception), str(direct))


class TestNeutralStore(unittest.TestCase):
    """The neutral store: public `datastorekit` names only, and what `ShardedPool` reads."""

    PUBLIC = {
        "datastorekit.SQL.factory_base.SQLAFactoryBase",
        "datastorekit.SQL.schema.build_schema",
        "datastorekit.contract.TAG_LABEL",
        "datastorekit.contract.TAG_SERIAL",
        "datastorekit.contract.TAG_TABLE",
        "datastorekit.contract.VERSION_LABEL",
        "datastorekit.contract.VERSION_TABLE",
        "datastorekit.shard_paths.shard_file_name",
        "datastorekit.store_inventory.InventorySpec",
        "datastorekit.store_inventory.Parent",
    }

    def test_it_is_built_from_public_names_only(self):
        with open(neutral_store.__file__, encoding="utf-8") as handle:
            tree = ast.parse(handle.read())
        bound = {}
        problems = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in ("datastorekit", "ray"):
                        problems.append(f":{node.lineno} imports {alias.name} whole")
            elif isinstance(node, ast.ImportFrom) and node.module:
                top = node.module.split(".")[0]
                if top == "ray" or node.module.endswith("shard_store_fixtures"):
                    problems.append(f":{node.lineno} imports from {node.module}")
                if top != "datastorekit":
                    continue
                for alias in node.names:
                    full = f"{node.module}.{alias.name}"
                    if any(part.startswith("_") for part in full.split(".")):
                        problems.append(f":{node.lineno} imports the private {full}")
                    bound[alias.asname or alias.name] = full
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                chain, root = [], node
                while isinstance(root, ast.Attribute):
                    chain.append(root.attr)
                    root = root.value
                if (
                    isinstance(root, ast.Name)
                    and root.id in bound
                    and any(attr.startswith("_") for attr in chain)
                ):
                    problems.append(f":{node.lineno} reads {root.id}.{'.'.join(chain)}")
            if isinstance(node, ast.Name) and node.id in ("ShardedPool", "bare_pool"):
                problems.append(f":{node.lineno} names {node.id}")
        self.assertEqual(problems, [], "\n".join(problems))
        self.assertEqual(set(bound.values()), self.PUBLIC)

    def test_shardedpool_plans_and_deletes_it_with_four_shards(self):
        import tempfile

        import ray

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp).resolve()
            two = build_full_store(directory, stem="two").primary
            four = build_full_store(directory, stem="store", shards=4).primary
            self.assertEqual(
                fingerprint_of(read_inventory(four, FACTORIES), 1)["digest"],
                fingerprint_of(read_inventory(two, FACTORIES), 1)["digest"],
            )
            files = ShardedPool.closed_store_files(four)
            self.assertEqual(
                [p.name for p in files],
                [f"store-shard000{i}.sqlite" for i in range(4)] + ["store.sqlite"],
            )
            self.assertEqual(ShardedPool.delete_store(four), files)
            self.assertEqual(
                sorted(p.name for p in directory.iterdir()),
                ["two-shard0000.sqlite", "two-shard0001.sqlite", "two.sqlite"],
            )
        self.assertFalse(ray.is_initialized())

    def test_the_baseline_has_no_problem_and_the_ported_names_are_its(self):
        self.assertEqual(ported.QSI, neutral_store.INTEGRAL)
        self.assertEqual(ported.TKN, neutral_store.SOLUTION)
        self.assertEqual(ported.COMPUTE_TARGETS, neutral_store.COMPUTE_TARGETS)
        self.assertEqual(ported.SOLVER_COLUMNS, neutral_store.SOLVER_COLUMNS)
        self.assertIs(ported._factories, FACTORIES)
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            primary = build_full_store(Path(tmp)).primary
            fingerprint, _ = FINGERPRINTER.take(primary, None)
        self.assertEqual(fingerprint["problems"], {})
        self.assertEqual(fingerprint["fingerprint_format"], 1)


class TestSidecarGuards(StoreTestCase):
    """`[02-the-sidecar-readers-guards-are-unpinned]`: what the reader refuses of a registry
    sidecar's `sidecar_format` and `store_id`."""

    def with_field(self, name, value):
        self.made = getattr(self, "made", 0) + 1
        primary = self.a_registry_store(f"G{self.made}")
        fields = load(stores.sidecar_path(primary))
        fields[name] = value
        write_sidecar_json(primary, fields)
        return stores.read_sidecar(primary)

    def test_a_boolean_sidecar_format_is_a_problem(self):
        reading = self.with_field("sidecar_format", True)
        self.assertEqual(reading.kind, "registry")
        self.assertFalse(reading.ok)
        self.assertIn(
            "sidecar_format is True; this reader knows format 1 only", reading.problems
        )

    def test_a_store_id_with_more_after_its_32_characters_is_a_problem(self):
        for value in ("a" * 32 + "x", "a" * 33):
            with self.subTest(store_id=value):
                reading = self.with_field("store_id", value)
                self.assertFalse(reading.ok)
                self.assertIn(
                    f"store_id {value!r} is not 32 lowercase hexadecimal characters",
                    reading.problems,
                )


if __name__ == "__main__":
    unittest.main()
