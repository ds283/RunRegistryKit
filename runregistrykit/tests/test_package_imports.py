"""The package imports on its own, lightly, and its command line answers to its name.

Each test that starts an interpreter starts a fresh one, isolated (`-I`: no user site, no
`PYTHON*` variables, no working directory on `sys.path`), from an empty `tempfile` directory, so
that only what is installed can be imported: never a client's module from the working directory.
"""

import ast
import json
import os
import subprocess
import sys
import tempfile
import unittest

import runregistrykit

PACKAGE_DIR = os.path.dirname(os.path.abspath(runregistrykit.__file__))
PACKAGE_NAME = "runregistrykit"

# The modules whose import statements at module scope are checked.
MODULES = ("__init__.py", "stores.py", "__main__.py")

# Not one of these may be loaded by importing the package and its store layer: the heavy
# dependencies of the store layer, and the client modules the imported code was written beside.
FORBIDDEN = (
    "ray",
    "sqlalchemy",
    "datastorekit",
    "config",
    "ObjectFactories",
    "StoreFixtures",
    "RunRegistry",
)

# A subprocess that is not broken takes a fraction of a second; one that imports `ray` by mistake
# takes several.
TIMEOUT = 120


def _run(args, cwd):
    return subprocess.run(
        [sys.executable, "-I", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def _module_scope_imports(tree):
    """Every import statement that runs when the module is imported.

    The walk descends into every statement (`if`, `try`, `with`, a class body, ...) but not into
    the body of a function or a lambda, which runs only when called.
    """
    found = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            found.append(node)
            continue
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                continue
            stack.append(child)
    return sorted(found, key=lambda n: n.lineno)


def _top_level(name):
    return name.split(".")[0]


class TestPackageImports(unittest.TestCase):
    def test_import_loads_nothing_heavy(self):
        code = (
            "import json, sys\n"
            "import runregistrykit, runregistrykit.stores\n"
            f"print(json.dumps(sorted(set({FORBIDDEN!r}) & set(sys.modules))))\n"
        )
        with tempfile.TemporaryDirectory() as cwd:
            result = _run(["-c", code], cwd)
        self.assertEqual(
            result.returncode,
            0,
            f"importing the package failed:\n{result.stdout}{result.stderr}",
        )
        loaded = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(
            loaded,
            [],
            f"`import runregistrykit, runregistrykit.stores` loaded {loaded}",
        )

    def test_module_scope_is_the_standard_library_and_the_package(self):
        allowed = set(sys.stdlib_module_names)
        problems = []
        for module in MODULES:
            path = os.path.join(PACKAGE_DIR, module)
            with open(path, encoding="utf-8") as handle:
                tree = ast.parse(handle.read(), filename=path)
            for node in _module_scope_imports(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.level > 0:
                        continue  # relative: the package itself
                    names = [node.module]
                else:
                    names = [alias.name for alias in node.names]
                for name in names:
                    top = _top_level(name)
                    if top == PACKAGE_NAME or top in allowed:
                        continue
                    problems.append(
                        f"{PACKAGE_NAME}/{module}:{node.lineno} imports {name} at module "
                        "scope, which is neither the standard library nor the package"
                    )
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_command_line_answers_to_its_name(self):
        var = os.path.join(runregistrykit.REPO_ROOT, "var")
        var_before = sorted(os.listdir(var)) if os.path.isdir(var) else None
        with tempfile.TemporaryDirectory() as cwd:
            result = _run(["-m", PACKAGE_NAME, "--help"], cwd)
            left_behind = sorted(os.listdir(cwd))
        self.assertEqual(
            result.returncode,
            0,
            f"`-m {PACKAGE_NAME} --help` failed:\n{result.stdout}{result.stderr}",
        )
        lines = result.stdout.splitlines()
        first = lines[0] if lines else ""
        self.assertTrue(
            first.startswith(f"usage: {PACKAGE_NAME} "),
            f"the first line of usage does not name {PACKAGE_NAME}: {first!r}",
        )
        self.assertEqual(left_behind, [], "`--help` wrote into its working directory")
        var_after = sorted(os.listdir(var)) if os.path.isdir(var) else None
        if var_before is None:
            self.assertIsNone(var_after, f"`--help` created {var}")
        else:
            self.assertEqual(var_after, var_before, f"`--help` changed {var}")


if __name__ == "__main__":
    unittest.main()
