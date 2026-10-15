"""The package's public names are declared, and each module carries its licence header.

Each of the five package modules declares a sorted ``__all__``, which holds exactly the public
names the module defines (every module-level function, class and assigned name without a leading
underscore) and, for the package itself, the function that slugs a run id's parts and the four
names it imports from ``runregistrykit.client``. ``slugify`` is public; the name it replaced is
gone, with no alias. Each module begins with the same fourteen-line Apache licence header, ahead
of its docstring, which is still the module's own.
"""

import ast
import importlib
import inspect
import re
import time
import unittest
from pathlib import Path

import runregistrykit

PACKAGE_DIR = Path(runregistrykit.__file__).resolve().parent

MODULES = (
    "runregistrykit",
    "runregistrykit.stores",
    "runregistrykit.client",
    "runregistrykit.fingerprint",
    "runregistrykit.__main__",
)

# the names the package imports from its client module and exports with its own
IMPORTED_AND_EXPORTED = {"CONFIG_FILE", "ClientRoot", "ConfigError", "find_client_root"}

HEADER = """\
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
"""


def _path(module_name: str) -> Path:
    leaf = module_name.split(".")[-1]
    return PACKAGE_DIR / (
        "__init__.py" if module_name == "runregistrykit" else leaf + ".py"
    )


def _defined_public_names(tree) -> set:
    """Every module-level def, class and assigned name without a leading underscore."""
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                names |= {n.id for n in ast.walk(target) if isinstance(n, ast.Name)}
    return {name for name in names if not name.startswith("_")}


class TestAll(unittest.TestCase):
    def test_each_module_declares_a_sorted_all_of_its_public_names(self):
        for name in MODULES:
            with self.subTest(module=name):
                module = importlib.import_module(name)
                declared = module.__all__
                self.assertIsInstance(declared, list)
                self.assertEqual(sorted(declared), declared)
                self.assertEqual(len(declared), len(set(declared)))
                tree = ast.parse(_path(name).read_text())
                expected = _defined_public_names(tree)
                if name == "runregistrykit":
                    expected |= {"slugify"} | IMPORTED_AND_EXPORTED
                    self.assertIn("slugify", _defined_public_names(tree))
                self.assertEqual(expected, set(declared))
                for public in declared:
                    self.assertTrue(hasattr(module, public), public)

    def test_the_main_module_exports_main_alone(self):
        main = importlib.import_module("runregistrykit.__main__")
        self.assertEqual(["main"], main.__all__)
        self.assertTrue(callable(main.main))

    def test_the_packages_own_all_has_the_imported_client_names(self):
        self.assertTrue(IMPORTED_AND_EXPORTED <= set(runregistrykit.__all__))
        for name in IMPORTED_AND_EXPORTED:
            self.assertIs(
                getattr(importlib.import_module("runregistrykit.client"), name),
                getattr(runregistrykit, name),
            )

    def test_the_fingerprint_names_are_not_reexported(self):
        for name in importlib.import_module("runregistrykit.fingerprint").__all__:
            self.assertNotIn(name, runregistrykit.__all__)


class TestSlugify(unittest.TestCase):
    def test_the_private_name_is_gone_and_slugify_is_public(self):
        self.assertFalse(hasattr(runregistrykit, "_slug"))
        self.assertIn("slugify", runregistrykit.__all__)
        self.assertEqual("a-b", runregistrykit.slugify("a b"))
        self.assertEqual("1-2", runregistrykit.slugify(" 1 2 "))
        self.assertEqual("x.y_z", runregistrykit.slugify("x.y_z"))
        self.assertEqual("a-b", runregistrykit.slugify("--a/b--"))
        self.assertEqual("12", runregistrykit.slugify(12))
        self.assertTrue(inspect.getdoc(runregistrykit.slugify))

    def test_run_id_joins_three_slugs_and_a_stamp(self):
        # a fixed time, so that a slow run cannot cross a second between the call and the check
        when = 1_700_000_000.0
        stamp = time.strftime(runregistrykit._ID_STAMP, time.localtime(when))
        slugs = [runregistrykit.slugify(x) for x in ("A b", "0 1", "c")]
        self.assertEqual(
            "-".join([*slugs, stamp]), runregistrykit.run_id("A b", "0 1", "c", when)
        )
        self.assertEqual(["A-b", "0-1", "c"], slugs)
        self.assertTrue(
            re.fullmatch(
                r"A-b-0-1-c-\d{8}T\d{6}", runregistrykit.run_id("A b", "0 1", "c")
            )
        )

    def test_the_signatures_of_run_id_and_begin_are_unchanged(self):
        self.assertEqual(
            ["campaign", "prompt", "slug", "when"],
            list(inspect.signature(runregistrykit.run_id).parameters),
        )
        self.assertIn("slug", inspect.signature(runregistrykit.begin).parameters)


class TestTheHeader(unittest.TestCase):
    def test_each_module_begins_with_the_header_and_keeps_its_docstring(self):
        for name in MODULES:
            with self.subTest(module=name):
                text = _path(name).read_text()
                self.assertTrue(text.startswith(HEADER + "\n"), name)
                self.assertEqual(14, len(HEADER.splitlines()))
                tree = ast.parse(text)
                docstring = ast.get_docstring(tree)
                self.assertTrue(docstring)
                # the docstring is the first statement, straight after the header and a blank line
                self.assertTrue(text[len(HEADER) + 1 :].startswith('"""'))
                self.assertEqual(
                    docstring, inspect.cleandoc(importlib.import_module(name).__doc__)
                )


if __name__ == "__main__":
    unittest.main()
