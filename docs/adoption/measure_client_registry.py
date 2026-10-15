#!/usr/bin/env python3
"""
Measure a client's use of its run registry against ``runregistrykit`` (extraction prompt 07,
section 2.1). Its Markdown output is the appendix of each adoption checklist in this directory.

Each client is read **only** through ``git rev-parse``, ``git log``, ``git ls-tree -r``,
``git show <commit>:<path>`` and ``git grep`` at one commit, never from its working tree. Nothing
of a client is imported, run or opened, and no store or run directory is read. Every tracked
``.py`` file is parsed with ``ast``. SecondaryGWKit's own registry, ``RunRegistry/``, is read too,
at the commit, but only for its staying tests (``STAYING``); and its frozen tree at ``a45aefc``
(``BASELINE``) gives each name's signature before the move.

What it reports, for the client at the commit:

1. every import of a ``RunRegistry`` module, at module level or nested (with the enclosing
   function or class), split into live code, the staying tests, and campaign records (files under
   ``prompts/`` or ``.prompts/``, counted by file only);
2. every name used from it: imported by name, reached as an attribute of an imported module or of
   an alias, assigned to as such an attribute, or patched (``patch.object(<module>, "<name>")``,
   ``patch("<dotted name>")``, ``setattr(<module>, "<name>", ...)``, and ``patch.object(<x>,
   "<name>")`` on any object, in a file that imports the registry, when ``<name>`` is a private
   attribute of SecondaryGWKit's ``Run`` at ``a45aefc``), with its sites;
3. each name's fate at ``v0.1.0``, from the package as installed: "kept" when it is in the
   ``__all__`` of the corresponding ``runregistrykit`` module; a rename, move or deletion from
   ``TABLE``, every row of which is checked against the package before anything is measured;
   "private" for a name with a leading underscore, present or absent, with its parameters at
   ``a45aefc`` and at ``v0.1.0``; "not shipped" or "the client's own" for a name from one of the
   registry's test modules; and otherwise "unknown";
4. every call of ``begin``, ``fingerprint_store``, ``copy_store``, ``move_store``,
   ``retire_store``, ``create_sidecar``, ``adopt_sidecar``, ``amend_sidecar`` or
   ``fingerprint_of`` whose callee resolves to the registry, with whether
   ``inspect.signature(<v0.1.0's function>).bind(...)`` accepts it, an ``object()`` standing for
   each argument (``bind_partial`` of the spelled arguments when the call unpacks ``*`` or
   ``**``, which may supply the rest). A ``fingerprint_of`` call whose one failure is the missing
   ``fingerprint_format`` is marked as the move's documented effect; any other failure to bind is
   for the person reading the report to stop on. And the calls of those names that do not resolve
   to the registry, which are not bound;
5. the string literals naming ``RunRegistry``, with ``-m RunRegistry`` commands flagged;
6. ``installed_package_provenance``: each definition against ``runregistrykit.package_provenance``
   by ``ast``, docstrings removed, and each call;
7. the tracked files other than ``.py`` matching ``RunRegistry|run registry|runregistrykit``,
   counted by top directory, with each line outside the campaign records listed;
8. whether ``.gitignore`` ignores ``var/``; the module-level registry mappings, the
   ``inventory_spec`` definitions, and the ``Parent(..., types=...)`` calls.

**How a callee is resolved.** A file's registry names are those its imports bind: ``import
RunRegistry``, ``import RunRegistry.stores [as x]``, ``from RunRegistry import begin``, ``from
RunRegistry import stores [as x]``, and so on, at module level or in a function. A name is looked up
as Python does near enough: the function's own bindings (any assignment or import in it makes the
name local throughout), then each enclosing function's, then the module's, with a class body seen
only from itself. A call or an attribute is the registry's only when its base name resolves to such
a binding; ``engine.begin()`` and a local ``begin`` are not.

Run it from the repository root with the venv's interpreter:

    ./venv/bin/python docs/adoption/measure_client_registry.py sgk  [--commit SHA] [--json]
    ./venv/bin/python docs/adoption/measure_client_registry.py cpbh [--commit SHA] [--json]
    ./venv/bin/python docs/adoption/measure_client_registry.py si   [--commit SHA] [--json]

The default commit is each checklist's. ``path --repository DIR --commit SHA`` measures any other
git repository by the same rules, with no staying tests; it exists to check the script on a
fixture, and the three client commands never read anything but their own repository and
SecondaryGWKit's ``a45aefc``.

Markdown by default, JSON with ``--json``; sorted, so that two runs at one commit give the same
bytes. Exits 0 on success; 1 when a row of ``TABLE`` disagrees with the package, before anything
is measured; 2 when it cannot read the client or the commit; 3 when a name is unknown, after the
report is printed.

It imports only the standard library, ``runregistrykit`` and ``datastorekit.store_fingerprint``.
It is not a test and does not run in CI.
"""

import argparse
import ast
import difflib
import importlib
import importlib.metadata
import inspect
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import datastorekit.store_fingerprint
import runregistrykit
import runregistrykit.__main__
import runregistrykit.stores

CODE_DIR = Path("/Users/ds283/Documents/Code")
REPO_ROOT = Path(__file__).resolve().parents[2]

CLIENTS = {
    "sgk": ("SecondaryGWKit (SGK)", "SecondaryGWKit", "14bcac0"),
    "cpbh": ("ChamPBH (CPBH)", "ChamPBH", "c21cdfb"),
    "si": ("StochasticInstantons (SI)", "StochasticInstantons", "5fb4a1d"),
}

# SecondaryGWKit's registry, frozen for the move: the signatures before it
BASELINE = ("SecondaryGWKit", "a45aefc")
REGISTRY = "RunRegistry"
RECORD_DIRS = ("prompts", ".prompts")

# SecondaryGWKit's tests that stay with it (its 101): the module, and the classes kept (None: all)
STAYING = {
    "RunRegistry/tests/test_build_rehearsal_scope.py": None,
    "RunRegistry/tests/test_killed_handler.py": None,
    "RunRegistry/tests/test_pipeline_adoption.py": None,
    "RunRegistry/tests/test_prune_on_resume.py": None,
    "RunRegistry/tests/test_quadsource_atol_sweep_prepare.py": None,
    "RunRegistry/tests/test_store_fingerprint.py": ("TestGolden", "TestDrivers"),
}

# the registry's modules that have a counterpart in the package
COUNTERPARTS = {
    "RunRegistry": "runregistrykit",
    "RunRegistry.stores": "runregistrykit.stores",
    "RunRegistry.__main__": "runregistrykit.__main__",
}

# (module, name) -> (fate, target, why): every rename, move and deletion. Each row is checked
# against the package when the script starts: the name is absent from the module's counterpart,
# it existed at a45aefc, and a target exists, with a signature when it is a function
TABLE = {
    ("RunRegistry", "_slug"): ("renamed", "runregistrykit.slugify", "U11"),
    ("RunRegistry", "REPO_ROOT"): (
        "deleted",
        None,
        "C1: the root is the client's, found from its runregistrykit.toml",
    ),
    ("RunRegistry", "DEFAULT_ROOT"): (
        "deleted",
        None,
        "C2: the runs root is the config's runs_root",
    ),
    ("RunRegistry", "RECORDED_DISTRIBUTIONS"): (
        "deleted",
        None,
        "C5: the config's distributions, besides runregistrykit (U9)",
    ),
    ("RunRegistry.stores", "DEFAULT_ROOT"): (
        "deleted",
        None,
        "C2: the runs root is the config's runs_root",
    ),
    ("RunRegistry.stores", "DEFAULT_STORES_ROOT"): (
        "deleted",
        None,
        "C3: the stores root is the config's stores_root",
    ),
    ("RunRegistry.stores", "FINGERPRINT_FORMAT"): (
        "deleted",
        None,
        "C7: the format is the client's, in its fingerprinter's module",
    ),
    ("RunRegistry.stores", "fingerprint_of"): (
        "moved",
        "datastorekit.store_fingerprint.fingerprint_of",
        "layer C, DatastoreKit's since v0.4.0",
    ),
    ("RunRegistry.stores", "compare_fingerprints"): (
        "moved",
        "datastorekit.store_fingerprint.compare_fingerprints",
        "layer C, DatastoreKit's since v0.4.0",
    ),
    ("RunRegistry.stores", "listing_lines"): (
        "moved",
        "datastorekit.store_fingerprint.listing_lines",
        "layer C, DatastoreKit's since v0.4.0",
    ),
}

# the calls whose arguments are bound against v0.1.0's function
CALLED = {
    ("RunRegistry", "begin"),
    ("RunRegistry.stores", "fingerprint_store"),
    ("RunRegistry.stores", "copy_store"),
    ("RunRegistry.stores", "move_store"),
    ("RunRegistry.stores", "retire_store"),
    ("RunRegistry.stores", "create_sidecar"),
    ("RunRegistry.stores", "adopt_sidecar"),
    ("RunRegistry.stores", "amend_sidecar"),
    ("RunRegistry.stores", "fingerprint_of"),
}

PATCH_OBJECT = {"patch.object", "mock.patch.object", "unittest.mock.patch.object"}
PATCH = {"patch", "mock.patch", "unittest.mock.patch"}

NON_PY_PATTERN = "RunRegistry|run registry|runregistrykit"
STRING_WORD = re.compile(r"\bRunRegistry\b")
COMMAND = re.compile(r"-m\s+RunRegistry\b")
HELPER = "installed_package_provenance"
# the one failure to bind that is the documented effect of a move (fingerprint_of's new argument)
MISSING_FORMAT = "missing a required argument: 'fingerprint_format'"
REGISTRY_NAMES = ("factories", "_factories")


class CannotRead(Exception):
    pass


class TableDisagrees(Exception):
    pass


# =================================================================================================
# git


def git(repository: Path, *args: str) -> str:
    try:
        done = subprocess.run(
            ["git", "-C", str(repository), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as e:
        raise CannotRead(f"git could not be run: {e}") from None
    if done.returncode != 0:
        raise CannotRead(
            f"git -C {repository} {' '.join(args)}: {done.stderr.strip() or done.returncode}"
        )
    return done.stdout


def full_commit(repository: Path, commit: str) -> str:
    if not (repository / ".git").exists():
        raise CannotRead(f"{repository} is not a git repository")
    return git(
        repository, "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}"
    ).strip()


def tracked(repository: Path, commit: str) -> list:
    return sorted(git(repository, "ls-tree", "-r", "--name-only", commit).splitlines())


def show(repository: Path, commit: str, path: str) -> str:
    return git(repository, "show", f"{commit}:{path}")


# =================================================================================================
# the package's side


def signature_text(params) -> str:
    """``(a, b=, *, c=)``: names, kinds and whether each has a default, nothing else."""
    out, star = [], False
    for name, kind, default in params:
        if kind == "kwonly" and not star:
            out.append("*")
            star = True
        if kind == "varargs":
            out.append(f"*{name}")
            star = True
        elif kind == "varkw":
            out.append(f"**{name}")
        else:
            out.append(name + ("=" if default else ""))
    return "(" + ", ".join(out) + ")"


def params_of_function(function) -> list:
    kinds = {
        inspect.Parameter.POSITIONAL_ONLY: "posonly",
        inspect.Parameter.POSITIONAL_OR_KEYWORD: "positional",
        inspect.Parameter.VAR_POSITIONAL: "varargs",
        inspect.Parameter.KEYWORD_ONLY: "kwonly",
        inspect.Parameter.VAR_KEYWORD: "varkw",
    }
    return [
        (p.name, kinds[p.kind], p.default is not inspect.Parameter.empty)
        for p in inspect.signature(function).parameters.values()
    ]


def params_of_def(node: ast.FunctionDef) -> list:
    a = node.args
    positional = a.posonlyargs + a.args
    defaults = [False] * (len(positional) - len(a.defaults)) + [True] * len(a.defaults)
    out = [
        (arg.arg, "posonly" if arg in a.posonlyargs else "positional", d)
        for arg, d in zip(positional, defaults)
    ]
    if a.vararg:
        out.append((a.vararg.arg, "varargs", False))
    for arg, d in zip(a.kwonlyargs, a.kw_defaults):
        out.append((arg.arg, "kwonly", d is not None))
    if a.kwarg:
        out.append((a.kwarg.arg, "varkw", False))
    return out


def resolve_dotted(dotted: str):
    """The object a dotted name names, importing its longest module prefix."""
    parts = dotted.split(".")
    for cut in range(len(parts), 0, -1):
        try:
            found = importlib.import_module(".".join(parts[:cut]))
        except ImportError:
            continue
        for part in parts[cut:]:
            found = getattr(found, part)
        return found
    raise ImportError(dotted)


class Baseline:
    """SecondaryGWKit's registry at a45aefc, by ast: module-level names and function signatures."""

    def __init__(self):
        repository = CODE_DIR / BASELINE[0]
        self.commit = full_commit(repository, BASELINE[1])
        self.tree = [
            p for p in tracked(repository, self.commit) if p.startswith(REGISTRY + "/")
        ]
        self.modules = {}
        for path in self.tree:
            if path.endswith(".py"):
                dotted = path[: -len(".py")].replace("/", ".")
                if dotted.endswith(".__init__"):
                    dotted = dotted[: -len(".__init__")]
                self.modules[dotted] = path
        self.names = {}  # module -> set of module-level names
        self.defs = {}  # (module, "f" or "Class.f") -> FunctionDef
        self.classes = {}  # (module, "Class") -> set of attribute names
        for module in COUNTERPARTS:
            tree = ast.parse(show(repository, self.commit, self.modules[module]))
            names = set()
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.add(node.name)
                    self.defs[(module, node.name)] = node
                elif isinstance(node, ast.ClassDef):
                    names.add(node.name)
                    attributes = set()
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            attributes.add(item.name)
                            self.defs[(module, f"{node.name}.{item.name}")] = item
                    self.classes[(module, node.name)] = attributes
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        names.add((alias.asname or alias.name).split(".")[0])
                elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = (
                        node.targets if isinstance(node, ast.Assign) else [node.target]
                    )
                    for target in targets:
                        if isinstance(target, ast.Name):
                            names.add(target.id)
            self.names[module] = names

    def run_private(self) -> set:
        return {
            name
            for name in self.classes.get((REGISTRY, "Run"), ())
            if name.startswith("_")
        }

    def signature(self, module, name):
        node = self.defs.get((module, name))
        return None if node is None else signature_text(params_of_def(node))


def check_table(baseline: Baseline) -> dict:
    """Every row of TABLE against the package and a45aefc; each target's signature, by row."""
    problems, targets = [], {}
    for (module, name), (fate, target, _) in sorted(TABLE.items()):
        counterpart = importlib.import_module(COUNTERPARTS[module])
        if hasattr(counterpart, name):
            problems.append(
                f"{module}.{name} is {fate}, but {counterpart.__name__} has it"
            )
        if name not in baseline.names.get(module, ()):
            problems.append(
                f"{module}.{name} is not a name of {module} at {BASELINE[1]}"
            )
        if target is not None:
            try:
                found = resolve_dotted(target)
            except (ImportError, AttributeError):
                problems.append(
                    f"{module}.{name} is {fate} to {target}, which does not exist"
                )
                continue
            if fate == "renamed":
                head, _, tail = target.rpartition(".")
                if tail not in importlib.import_module(head).__all__:
                    problems.append(f"{target} is not in {head}.__all__")
            if callable(found):
                targets[(module, name)] = signature_text(params_of_function(found))
    if not (
        REPO_ROOT / "pyproject.toml"
    ).is_file() or "runregistrykit.tests" not in tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text()
    ).get(
        "tool", {}
    ).get(
        "setuptools", {}
    ).get(
        "packages", {}
    ).get(
        "find", {}
    ).get(
        "exclude", []
    ):
        problems.append(
            "pyproject.toml does not exclude runregistrykit.tests, so a name from the "
            "registry's tests cannot be called not shipped"
        )
    if problems:
        raise TableDisagrees("; ".join(problems))
    return targets


class Fates:
    def __init__(self, baseline: Baseline, targets: dict):
        self.baseline = baseline
        self.targets = targets

    def module_kind(self, module: str) -> str:
        if module in COUNTERPARTS:
            return "package"
        if module not in self.baseline.modules:
            return "unknown"
        if self.baseline.modules[module] in STAYING or module == f"{REGISTRY}.tests":
            return "own"
        return "not shipped"

    def fate(self, module: str, name: str) -> dict:
        kind = self.module_kind(module)
        out = {"private": name.split(".")[-1].startswith("_")}
        if kind == "unknown":
            return {
                **out,
                "fate": "unknown",
                "detail": f"{module} is not a registry module",
            }
        if kind == "own":
            return {
                **out,
                "fate": "the client's own",
                "detail": f"{module} is a staying test module, which moves with the tests",
            }
        if kind == "not shipped":
            return {
                **out,
                "fate": "not shipped",
                "detail": f"{module} is test support; v0.1.0 ships no runregistrykit.tests "
                f"(U19), and the client keeps its own copy (U21)",
            }
        before = self.baseline.signature(module, name)
        if (module, name) in TABLE:
            fate, target, why = TABLE[(module, name)]
            return {
                **out,
                "fate": fate,
                "detail": (
                    f"{target}{self.targets.get((module, name), '')}; "
                    if target
                    else ""
                )
                + why
                + (f"; at {BASELINE[1]} {before}" if before else ""),
            }
        counterpart = importlib.import_module(COUNTERPARTS[module])
        head, _, tail = name.partition(".")
        if head in counterpart.__all__:
            found = getattr(counterpart, head)
            if tail:
                present = hasattr(found, tail)
                return {
                    **out,
                    "fate": "private" if present else "unknown",
                    "detail": f"{counterpart.__name__}.{name} "
                    + (
                        f"present; {before} at {BASELINE[1]}, "
                        f"{signature_text(params_of_function(getattr(found, tail)))} at v0.1.0"
                        if present and callable(getattr(found, tail))
                        else ("present" if present else "absent")
                    ),
                }
            detail = f"{counterpart.__name__}.{name}"
            if callable(found) and not isinstance(found, type):
                after = signature_text(params_of_function(found))
                detail += (
                    f"{after}, the same parameters as at {BASELINE[1]}"
                    if after == before
                    else f"{after}; at {BASELINE[1]} {before}"
                )
            return {**out, "fate": "kept", "detail": detail}
        if name.startswith("_"):
            present = hasattr(counterpart, name)
            if not present:
                return {
                    **out,
                    "fate": "private",
                    "detail": f"absent from {counterpart.__name__}",
                }
            found = getattr(counterpart, name)
            detail = f"{counterpart.__name__}.{name} present"
            if callable(found):
                detail += (
                    f"; {before} at {BASELINE[1]}, "
                    f"{signature_text(params_of_function(found))} at v0.1.0"
                )
            return {**out, "fate": "private", "detail": detail}
        return {
            **out,
            "fate": "unknown",
            "detail": f"not in {counterpart.__name__}.__all__ and in no row of the table",
        }

    def callee(self, module: str, name: str):
        if (module, name) in TABLE:
            target = TABLE[(module, name)][1]
            return None if target is None else (target, resolve_dotted(target))
        target = f"{COUNTERPARTS[module]}.{name}"
        try:
            return target, resolve_dotted(target)
        except (ImportError, AttributeError):
            return None


# =================================================================================================
# the client's side: one file


class Scope:
    def __init__(self, kind, name, parent, bindings):
        self.kind, self.name, self.parent, self.bindings = kind, name, parent, bindings

    def qualified(self) -> str:
        names, scope = [], self
        while scope is not None and scope.kind != "module":
            names.append(scope.name)
            scope = scope.parent
        return ".".join(reversed(names)) or "module"


NOT_REGISTRY = ("other",)


def spelled(node) -> str:
    try:
        return ast.unparse(node)
    except Exception:  # an ast the unparser does not know
        return ""


def scope_nodes(body):
    """Every node of a scope's body, not descending into a nested function, lambda or class
    body (their decorators, defaults and bases are the enclosing scope's)."""
    stack = list(reversed(body))
    while stack:
        node = stack.pop()
        yield node
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            inner = node.decorator_list + node.args.defaults
            inner += [d for d in node.args.kw_defaults if d is not None]
        elif isinstance(node, ast.Lambda):
            inner = node.args.defaults + [
                d for d in node.args.kw_defaults if d is not None
            ]
        elif isinstance(node, ast.ClassDef):
            inner = node.decorator_list + node.bases + node.keywords
        else:
            inner = list(ast.iter_child_nodes(node))
        stack.extend(reversed(inner))


class FileAnalysis:
    def __init__(self, path, source, known_modules, run_private, keep_classes=None):
        self.path = path
        self.source = source
        self.tree = ast.parse(source, filename=path)
        self.known_modules = known_modules
        self.run_private = run_private
        self.keep_classes = keep_classes
        self.imports, self.uses, self.calls, self.alikes, self.strings = (
            [],
            [],
            [],
            [],
            [],
        )
        self.imports_registry = any(
            isinstance(node, (ast.Import, ast.ImportFrom))
            and self._names_registry(node)
            for node in ast.walk(self.tree)
        )
        if self.keep_classes is not None:
            self.keep_classes = self._with_bases(set(keep_classes))
        module = Scope("module", "", None, self._bindings(self.tree.body, None))
        for node in self.tree.body:
            self.visit(node, module)

    # --- bindings -----------------------------------------------------------------------------

    def _with_bases(self, keep):
        defined = {n.name: n for n in self.tree.body if isinstance(n, ast.ClassDef)}
        while True:
            more = {
                base.id
                for name in keep
                if name in defined
                for base in defined[name].bases
                if isinstance(base, ast.Name) and base.id in defined
            }
            if more <= keep:
                return keep
            keep |= more

    @staticmethod
    def _is_registry(module) -> bool:
        return module == REGISTRY or (module or "").startswith(REGISTRY + ".")

    def _names_registry(self, node) -> bool:
        if isinstance(node, ast.Import):
            return any(self._is_registry(a.name) for a in node.names)
        return node.level == 0 and self._is_registry(node.module)

    def _import_bindings(self, node):
        """(bound name, binding) for each alias; a binding is ("module", dotted) or ("name",
        module, name), or NOT_REGISTRY."""
        out = []
        if isinstance(node, ast.Import):
            for a in node.names:
                if not self._is_registry(a.name):
                    out.append(((a.asname or a.name).split(".")[0], NOT_REGISTRY))
                elif a.asname:
                    out.append((a.asname, ("module", a.name)))
                else:
                    out.append((a.name.split(".")[0], ("module", a.name.split(".")[0])))
        else:
            registry = node.level == 0 and self._is_registry(node.module)
            for a in node.names:
                bound = a.asname or a.name
                if not registry:
                    out.append((bound, NOT_REGISTRY))
                elif f"{node.module}.{a.name}" in self.known_modules:
                    out.append((bound, ("module", f"{node.module}.{a.name}")))
                else:
                    out.append((bound, ("name", node.module, a.name)))
        return out

    def _bindings(self, body, function) -> dict:
        found = {}

        def add(name, binding):
            found.setdefault(name, []).append(binding)

        if function is not None:
            a = function.args
            for arg in a.posonlyargs + a.args + a.kwonlyargs + [a.vararg, a.kwarg]:
                if arg is not None:
                    add(arg.arg, NOT_REGISTRY)
        skip = set()
        for node in scope_nodes(body):
            if isinstance(node, ast.comprehension):
                skip.update(id(n) for n in ast.walk(node.target))
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for name, binding in self._import_bindings(node):
                    add(name, binding)
            elif isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                add(node.name, NOT_REGISTRY)
            elif isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
                if id(node) not in skip:
                    add(node.id, NOT_REGISTRY)
            elif isinstance(node, ast.ExceptHandler) and node.name:
                add(node.name, NOT_REGISTRY)
        out = {}
        for name, bindings in found.items():
            registry = [b for b in bindings if b is not NOT_REGISTRY]
            out[name] = registry[0] if registry else NOT_REGISTRY
        return out

    def lookup(self, name, scope):
        first = True
        while scope is not None:
            if (first or scope.kind != "class") and name in scope.bindings:
                return scope.bindings[name]
            first = False
            scope = scope.parent
        return None

    # --- resolution ---------------------------------------------------------------------------

    def resolve(self, node, scope):
        """For a Name or an Attribute chain: ("module", dotted) or ("name", module, name), and
        the attributes left over; or None when its base is not the registry's."""
        attributes = []
        while isinstance(node, ast.Attribute):
            attributes.append(node.attr)
            node = node.value
        if not isinstance(node, ast.Name):
            return None
        binding = self.lookup(node.id, scope)
        if binding is None or binding is NOT_REGISTRY:
            return None
        attributes.reverse()
        if binding[0] == "name":
            return binding, attributes
        module = binding[1]
        while attributes and f"{module}.{attributes[0]}" in self.known_modules:
            module = f"{module}.{attributes.pop(0)}"
        if not attributes:
            return ("module", module), []
        return ("name", module, attributes[0]), attributes[1:]

    @staticmethod
    def _name(binding, rest) -> str:
        name = binding[2]
        if rest and rest[0].startswith("_"):
            name += "." + rest[0]
        return name

    def use(self, line, scope, module, name, kind):
        self.uses.append(
            {
                "path": self.path,
                "line": line,
                "scope": scope.qualified(),
                "module": module,
                "name": name,
                "kind": kind,
            }
        )

    def dotted_patch(self, text):
        parts = text.split(".")
        module, i = parts[0], 1
        while i < len(parts) and f"{module}.{parts[i]}" in self.known_modules:
            module = f"{module}.{parts[i]}"
            i += 1
        if i == len(parts):
            return module, None
        name = parts[i]
        if i + 1 < len(parts) and parts[i + 1].startswith("_"):
            name += "." + parts[i + 1]
        return module, name

    # --- the walk -----------------------------------------------------------------------------

    def visit(self, node, scope):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for child in node.decorator_list + node.args.defaults:
                self.visit(child, scope)
            for child in node.args.kw_defaults:
                if child is not None:
                    self.visit(child, scope)
            inner = Scope("function", node.name, scope, self._bindings(node.body, node))
            for child in node.body:
                self.visit(child, inner)
            return
        if isinstance(node, ast.Lambda):
            for child in node.args.defaults:
                self.visit(child, scope)
            inner = Scope(
                "function", "<lambda>", scope, self._bindings([node.body], node)
            )
            self.visit(node.body, inner)
            return
        if isinstance(node, ast.ClassDef):
            if (
                self.keep_classes is not None
                and scope.kind == "module"
                and node.name not in self.keep_classes
            ):
                return
            for child in node.decorator_list + node.bases + node.keywords:
                self.visit(child, scope)
            inner = Scope("class", node.name, scope, self._bindings(node.body, None))
            for child in node.body:
                self.visit(child, inner)
            return
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            self.record_import(node, scope)
            return
        if isinstance(node, ast.JoinedStr):
            text = "".join(
                v.value
                for v in node.values
                if isinstance(v, ast.Constant) and isinstance(v.value, str)
            )
            self.record_string(node, text, scope)
            for v in node.values:
                if isinstance(v, ast.FormattedValue):
                    self.visit(v, scope)
            return
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            self.record_string(node, node.value, scope)
            return
        skip = set()
        if isinstance(node, ast.Call):
            skip = self.record_call(node, scope)
        if isinstance(node, (ast.Attribute, ast.Name)):
            resolved = self.resolve(node, scope)
            if resolved is not None:
                binding, rest = resolved
                kind = (
                    "assigned"
                    if isinstance(node, ast.Attribute)
                    and not isinstance(node.ctx, ast.Load)
                    else "used"
                )
                if binding[0] == "module":
                    self.use(node.lineno, scope, binding[1], "", "module " + kind)
                else:
                    self.use(
                        node.lineno, scope, binding[1], self._name(binding, rest), kind
                    )
                return
            if isinstance(node, ast.Name):
                return
        for child in ast.iter_child_nodes(node):
            if id(child) not in skip:
                self.visit(child, scope)

    def record_import(self, node, scope):
        if not self._names_registry(node):
            return
        bindings = self._import_bindings(node)
        names = []
        for (bound, binding), alias in zip(bindings, node.names):
            if isinstance(node, ast.Import):
                names.append(
                    alias.name + (f" as {alias.asname}" if alias.asname else "")
                )
            else:
                names.append(
                    alias.name + (f" as {alias.asname}" if alias.asname else "")
                )
                if binding[0] == "name":
                    self.use(node.lineno, scope, binding[1], binding[2], "imported")
        self.imports.append(
            {
                "path": self.path,
                "line": node.lineno,
                "scope": scope.qualified(),
                "module": (
                    node.module
                    if isinstance(node, ast.ImportFrom)
                    else ", ".join(a.name for a in node.names)
                ),
                "statement": (
                    f"from {node.module} import {', '.join(names)}"
                    if isinstance(node, ast.ImportFrom)
                    else f"import {', '.join(names)}"
                ),
            }
        )

    def record_string(self, node, text, scope):
        if not STRING_WORD.search(text):
            return
        command = None
        if COMMAND.search(text):
            # the line the command is on, in the source of a literal that may span several
            segment = ast.get_source_segment(self.source, node) or ""
            found = COMMAND.search(segment)
            command = node.lineno + (
                segment[: found.start()].count("\n") if found else 0
            )
        self.strings.append(
            {
                "path": self.path,
                "line": node.lineno,
                "scope": scope.qualified(),
                "command": command,
                "text": " ".join(text.split())[:100],
            }
        )

    def record_call(self, node, scope) -> set:
        """Patches and the calls of CALLED; the ids of the arguments a patch consumed."""
        func = spelled(node.func)
        args = node.args
        consumed = set()
        named = len(args) >= 2 and isinstance(args[1], ast.Constant)
        named = named and isinstance(args[1].value, str)
        if (
            func in PATCH_OBJECT or func == "setattr" or func.endswith(".setattr")
        ) and named:
            resolved = self.resolve(args[0], scope)
            kind = (
                "patched (setattr)" if "setattr" in func else "patched (patch.object)"
            )
            if resolved is not None and resolved[0][0] == "module" and not resolved[1]:
                self.use(node.lineno, scope, resolved[0][1], args[1].value, kind)
                consumed.add(id(args[0]))
            elif (
                func in PATCH_OBJECT
                and resolved is None
                and self.imports_registry
                and args[1].value in self.run_private
            ):
                self.use(
                    node.lineno,
                    scope,
                    REGISTRY,
                    f"Run.{args[1].value}",
                    "patched on an object (patch.object, by name)",
                )
        if func in PATCH and args and isinstance(args[0], ast.Constant):
            text = args[0].value
            if isinstance(text, str) and self._is_registry(text.split(".")[0]):
                module, name = self.dotted_patch(text)
                self.use(node.lineno, scope, module, name or "", "patched (patch)")
        resolved = self.resolve(node.func, scope)
        target = None
        if resolved is not None and resolved[0][0] == "name" and not resolved[1]:
            target = (resolved[0][1], resolved[0][2])
        short = func.rsplit(".", 1)[-1]
        if target in CALLED:
            self.calls.append(
                {
                    "path": self.path,
                    "line": node.lineno,
                    "scope": scope.qualified(),
                    "module": target[0],
                    "name": target[1],
                    "spelled": func,
                    "positional": sum(not isinstance(a, ast.Starred) for a in args),
                    "starred": any(isinstance(a, ast.Starred) for a in args),
                    "keywords": sorted(
                        k.arg for k in node.keywords if k.arg is not None
                    ),
                    "double_starred": any(k.arg is None for k in node.keywords),
                }
            )
        elif short in {name for _, name in CALLED}:
            self.alikes.append(
                {
                    "path": self.path,
                    "line": node.lineno,
                    "scope": scope.qualified(),
                    "spelled": func,
                    "positional": len(args),
                }
            )
        return consumed


# =================================================================================================
# the measurement


def helper_report(path, tree) -> list:
    """Each definition of the helper in ``tree``, against runregistrykit.package_provenance."""

    def body_lines(function) -> list:
        body = function.body
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            body = body[1:]
        return "\n".join(ast.unparse(s) for s in body).splitlines()

    package = ast.parse(inspect.getsource(runregistrykit.package_provenance)).body[0]
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == HELPER:
            difference = [
                line
                for line in difflib.unified_diff(
                    body_lines(package), body_lines(node), lineterm="", n=0
                )
                if not line.startswith(("---", "+++", "@@"))
            ]
            out.append(
                {
                    "path": path,
                    "line": node.lineno,
                    "end": node.end_lineno,
                    "arguments": ast.unparse(node.args),
                    "package_arguments": ast.unparse(package.args),
                    "difference": difference,
                }
            )
    return out


def measure(label, repository: Path, commit: str, staying: bool, fates: Fates) -> dict:
    commit = full_commit(repository, commit)
    when, subject = (
        git(repository, "log", "-1", "--format=%cs%x00%s", commit).strip().split("\0")
    )
    paths = tracked(repository, commit)
    known_modules = set(fates.baseline.modules)
    run_private = fates.baseline.run_private()

    report = {
        "client": label,
        "repository": str(repository),
        "commit": commit,
        "date": when,
        "subject": subject,
        "package": {
            "runregistrykit": importlib.metadata.version("runregistrykit"),
            "datastorekit": importlib.metadata.version("datastorekit"),
        },
        "baseline": f"{BASELINE[0]} {fates.baseline.commit}",
    }

    files = {"live": [], "staying": [], "records": []}
    unparsed = []
    record_naming = []
    analyses = {"live": [], "staying": []}
    helpers, helper_calls, helper_imports, recorded = [], [], [], []
    registries, specs, parents = [], [], []
    python = [p for p in paths if p.endswith(".py")]
    for path in python:
        top = path.split("/")[0]
        if top == REGISTRY:
            if not (staying and path in STAYING):
                continue
            part = "staying"
        elif top in RECORD_DIRS:
            part = "records"
        else:
            part = "live"
        source = show(repository, commit, path)
        try:
            keep = STAYING.get(path) if part == "staying" else None
            analysis = FileAnalysis(path, source, known_modules, run_private, keep)
        except SyntaxError as e:
            unparsed.append({"path": path, "error": f"{e.msg} at line {e.lineno}"})
            continue
        if part == "records":
            if STRING_WORD.search(source):
                record_naming.append(path)
            if analysis.imports:
                files["records"].append(
                    {"path": path, "imports": len(analysis.imports)}
                )
            continue
        analyses[part].append(analysis)
        if part == "live":
            helpers.extend(helper_report(path, analysis.tree))
            for node in ast.walk(analysis.tree):
                if isinstance(node, ast.Call):
                    func = node.func
                    name = (
                        func.id
                        if isinstance(func, ast.Name)
                        else getattr(func, "attr", "")
                    )
                    if name == HELPER:
                        helper_calls.append(
                            {
                                "path": path,
                                "line": node.lineno,
                                "positional": len(node.args),
                                "keywords": sorted(
                                    k.arg or "**" for k in node.keywords
                                ),
                            }
                        )
                    if name == "Parent" and any(
                        k.arg == "types" for k in node.keywords
                    ):
                        value = next(k.value for k in node.keywords if k.arg == "types")
                        parents.append(
                            {
                                "path": path,
                                "line": node.lineno,
                                "types": " ".join(ast.unparse(value).split())[:80],
                            }
                        )
                if isinstance(node, ast.FunctionDef) and node.name == "inventory_spec":
                    specs.append({"path": path, "line": node.lineno})
                if isinstance(node, ast.ImportFrom) and any(
                    a.name == HELPER for a in node.names
                ):
                    helper_imports.append(
                        {
                            "path": path,
                            "line": node.lineno,
                            "module": node.module or ".",
                        }
                    )
            for node in analysis.tree.body:
                targets = []
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                for target in targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id in REGISTRY_NAMES
                        and isinstance(node.value, ast.Dict)
                    ):
                        registries.append(
                            {
                                "path": path,
                                "line": node.lineno,
                                "name": target.id,
                                "keys": len(node.value.keys),
                            }
                        )
                    if (
                        isinstance(target, ast.Name)
                        and target.id == "RECORDED_DISTRIBUTIONS"
                    ):
                        recorded.append(
                            {
                                "path": path,
                                "line": node.lineno,
                                "assigned": ast.unparse(node.value),
                            }
                        )

    for part in ("live", "staying"):
        for analysis in analyses[part]:
            if analysis.imports:
                files[part].append(analysis.path)

    def key(row):
        return (row["path"], row["line"], json.dumps(row, sort_keys=True))

    unknown = False
    for part in ("live", "staying"):
        imports = sorted((i for a in analyses[part] for i in a.imports), key=key)
        uses = sorted((u for a in analyses[part] for u in a.uses), key=key)
        names = {}
        for u in uses:
            if u["kind"].startswith("module"):
                continue
            entry = names.setdefault(
                f"{u['module']}.{u['name']}",
                {"module": u["module"], "name": u["name"], "sites": []},
            )
            entry["sites"].append(
                {
                    "path": u["path"],
                    "line": u["line"],
                    "scope": u["scope"],
                    "kind": u["kind"],
                }
            )
        for entry in names.values():
            entry.update(fates.fate(entry["module"], entry["name"]))
            unknown = unknown or entry["fate"] == "unknown"
        calls = sorted((c for a in analyses[part] for c in a.calls), key=key)
        for call in calls:
            callee = fates.callee(call["module"], call["name"])
            if callee is None:
                call["target"], call["verdict"] = None, "no function at v0.1.0"
                continue
            call["target"] = callee[0] + signature_text(params_of_function(callee[1]))
            # an unpacking may supply what is missing, so then only what is spelled is bound
            unpacks = call["starred"] or call["double_starred"]
            signature = inspect.signature(callee[1])
            bind = signature.bind_partial if unpacks else signature.bind
            placeholder = object()
            try:
                bind(
                    *[placeholder] * call["positional"],
                    **{k: placeholder for k in call["keywords"]},
                )
                verdict = "binds"
            except TypeError as e:
                verdict = f"does not bind: {e}"
                if call["name"] == "fingerprint_of" and str(e) == MISSING_FORMAT:
                    verdict += " (the move's new required `fingerprint_format`)"
            if unpacks:
                verdict += " (its spelled arguments; the unpacking is not expanded)"
            call["verdict"] = verdict
        report[part] = {
            "files": sorted(files[part]),
            "imports": imports,
            "module_level_imports": sum(i["scope"] == "module" for i in imports),
            "names": [names[k] for k in sorted(names)],
            "module_uses": [u for u in uses if u["kind"].startswith("module")],
            "calls": calls,
            "alikes": sorted((c for a in analyses[part] for c in a.alikes), key=key),
            "strings": sorted((s for a in analyses[part] for s in a.strings), key=key),
        }
    report["records"] = {
        "importing": sorted(files["records"], key=lambda r: r["path"]),
        "naming": sorted(record_naming),
    }
    report["unparsed"] = unparsed
    report["python_files"] = len(python)

    report["helper"] = {
        "definitions": sorted(helpers, key=key),
        "imports": sorted(helper_imports, key=key),
        "calls": sorted(helper_calls, key=key),
        "recorded_distributions": sorted(recorded, key=key),
    }
    report["staying_measured"] = staying

    lines = grep_other_files(repository, commit)
    counts, listed = {}, []
    for line in lines:
        rest = line[len(commit) + 1 :]
        path, number, text = rest.split(":", 2)
        top = path.split("/")[0]
        counts[top] = counts.get(top, 0) + 1
        if top not in RECORD_DIRS:
            listed.append(
                {
                    "path": path,
                    "line": int(number),
                    "text": " ".join(text.split())[:110],
                }
            )
    report["other_files"] = {
        "counts": {k: counts[k] for k in sorted(counts)},
        "lines": sorted(listed, key=key),
    }

    ignored = None
    if ".gitignore" in paths:
        ignored = []
        for number, text in enumerate(
            show(repository, commit, ".gitignore").splitlines(), 1
        ):
            if re.fullmatch(r"/?var(/|/\*\*?)?", text.strip()):
                ignored.append({"line": number, "text": text.strip()})
    report["gitignore_var"] = ignored
    report["registries"] = sorted(registries, key=key)
    report["inventory_specs"] = {
        "files": len({s["path"] for s in specs}),
        "definitions": sorted(specs, key=key),
    }
    report["polymorphic_parents"] = sorted(parents, key=key)

    requirements = []
    if "requirements.txt" in paths:
        for number, text in enumerate(
            show(repository, commit, "requirements.txt").splitlines(), 1
        ):
            if re.match(
                r"(?i)\s*(datastorekit|raypoolkit|runregistrykit|ray|sqlalchemy)\b",
                text,
            ):
                requirements.append({"line": number, "text": text.strip()})
    report["requirements"] = requirements
    report["unknown"] = unknown
    return report


def grep_other_files(repository, commit) -> list:
    """``git grep`` of the tracked files other than ``.py``; it exits 1 when nothing matches,
    which is a finding, not a failure."""
    command = [
        "git",
        "-C",
        str(repository),
        "grep",
        "-I",
        "-n",
        "-E",
        "-e",
        NON_PY_PATTERN,
    ]
    command += [commit, "--", ".", ":(exclude)*.py"]
    try:
        done = subprocess.run(command, capture_output=True, text=True, check=False)
    except OSError as e:
        raise CannotRead(f"git could not be run: {e}") from None
    if done.returncode not in (0, 1):
        raise CannotRead(f"git grep in {repository}: {done.stderr.strip()}")
    return done.stdout.splitlines()


# =================================================================================================
# Markdown


def cell(text) -> str:
    return str(text).replace("|", "\\|")


def markdown(r) -> str:
    out = []
    add = out.append
    add(f"### Measured: {r['client']} at `{r['commit'][:7]}`")
    add("")
    add(
        f"- Repository `{r['repository']}`, commit `{r['commit']}`, {r['date']}, “{r['subject']}”."
    )
    add(
        f"- Read through `git` only: {r['python_files']} tracked `.py` files parsed with `ast`"
        + (f", {len(r['unparsed'])} not parseable" if r["unparsed"] else "")
        + "."
    )
    add(
        f"- Against `runregistrykit` {r['package']['runregistrykit']} and `datastorekit` "
        f"{r['package']['datastorekit']} as installed; signatures before the move from "
        f"{r['baseline'][:len(BASELINE[0]) + 8]}."
    )
    if r["requirements"]:
        add(
            "- `requirements.txt`: "
            + "; ".join(f"`{q['text']}` (`:{q['line']}`)" for q in r["requirements"])
            + "."
        )
    add("")

    live, staying = r["live"], r["staying"]
    parts = [("live", "Live code")]
    if r["staying_measured"]:
        parts.append(("staying", "Staying tests"))
    rows = (
        ("Import statements", lambda p: len(p["imports"])),
        ("… at module level", lambda p: p["module_level_imports"]),
        ("Files importing it", lambda p: len(p["files"])),
        ("Names used", lambda p: len(p["names"])),
        ("Calls bound", lambda p: len(p["calls"])),
        (
            "… binding",
            lambda p: sum(c["verdict"].startswith("binds") for c in p["calls"]),
        ),
        (
            "… not binding: the move's new `fingerprint_format` only",
            lambda p: sum("the move's new" in c["verdict"] for c in p["calls"]),
        ),
        (
            "… not binding for any other reason",
            lambda p: sum(
                not c["verdict"].startswith("binds")
                and "the move's new" not in c["verdict"]
                for c in p["calls"]
            ),
        ),
        ("Name-alike calls, not the registry's", lambda p: len(p["alikes"])),
        ("String literals naming it", lambda p: len(p["strings"])),
        (
            "… holding `-m RunRegistry`",
            lambda p: sum(bool(s["command"]) for s in p["strings"]),
        ),
    )
    add("| Figure | " + " | ".join(title for _, title in parts) + " |")
    add("|---|" + "---|" * len(parts))
    for label, count in rows:
        add(
            f"| {label} | "
            + " | ".join(str(count(r[part])) for part, _ in parts)
            + " |"
        )
    add("")
    add(
        f"Campaign records: **{len(r['records']['importing'])}** `.py` files import it, "
        f"{len(r['records']['naming'])} name it."
    )
    add("")

    for part, title in (("live", "Live code"), ("staying", "The staying tests")):
        p = r[part]
        if part == "staying" and not r["staying_measured"]:
            continue
        add(f"#### 1. Imports: {title.lower()}")
        add("")
        if p["imports"]:
            add("| File | Line | Scope | Statement |")
            add("|---|---|---|---|")
            for i in p["imports"]:
                add(
                    f"| `{i['path']}` | {i['line']} | `{i['scope']}` | `{cell(i['statement'])}` |"
                )
        else:
            add("None.")
        add("")
        add(f"#### 2–3. Names and their fates at `v0.1.0`: {title.lower()}")
        add("")
        if p["names"]:
            add("| Name | Fate | At `v0.1.0` | Sites |")
            add("|---|---|---|---|")
            for n in p["names"]:
                sites = ", ".join(
                    f"`{s['path']}:{s['line']}` ({s['kind']})" for s in n["sites"]
                )
                flag = " (private)" if n["private"] and n["fate"] != "private" else ""
                add(
                    f"| `{n['module']}.{n['name']}` | {n['fate']}{flag} | {cell(n['detail'])} "
                    f"| {sites} |"
                )
        else:
            add("None.")
        if p["module_uses"]:
            add("")
            add(
                "A module used as a value: "
                + ", ".join(
                    f"`{u['module']}` at `{u['path']}:{u['line']}`"
                    for u in p["module_uses"]
                )
                + "."
            )
        add("")
        add(f"#### 4. Calls: {title.lower()}")
        add("")
        if p["calls"]:
            add("| File:line | Call | Positional | Keywords | Unpacking | Verdict |")
            add("|---|---|---|---|---|---|")
            for c in p["calls"]:
                unpack = ", ".join(
                    x
                    for x, y in (("*", c["starred"]), ("**", c["double_starred"]))
                    if y
                )
                add(
                    f"| `{c['path']}:{c['line']}` | `{c['spelled']}` | {c['positional']} | "
                    f"{', '.join(c['keywords']) or '—'} | {unpack or '—'} | {cell(c['verdict'])} |"
                )
            targets = sorted({c["target"] for c in p["calls"] if c["target"]})
            add("")
            add("Bound against " + "; ".join(f"`{t}`" for t in targets) + ".")
        else:
            add("None.")
        if p["alikes"]:
            add("")
            add(
                "Not the registry's (their callee does not resolve to it), so not bound:"
            )
            add("")
            for c in p["alikes"]:
                add(
                    f"- `{c['path']}:{c['line']}` `{c['spelled']}(…)`, in `{c['scope']}`"
                )
        add("")
        add(f"#### 5. String literals naming `RunRegistry`: {title.lower()}")
        add("")
        if p["strings"]:
            add("| File | Line | Command at | Text (first 100 characters) |")
            add("|---|---|---|---|")
            for s in p["strings"]:
                command = f"**`:{s['command']}`**" if s["command"] else ""
                add(f"| `{s['path']}` | {s['line']} | {command} | {cell(s['text'])} |")
        else:
            add("None.")
        add("")

    add("#### 1. Campaign records")
    add("")
    if r["records"]["importing"]:
        add(
            "Importing it: "
            + ", ".join(
                f"`{x['path']}` ({x['imports']})" for x in r["records"]["importing"]
            )
            + "."
        )
        add("")
    others = sorted(
        set(r["records"]["naming"]) - {x["path"] for x in r["records"]["importing"]}
    )
    if others:
        add(
            "Naming it without importing it: "
            + ", ".join(f"`{x}`" for x in others)
            + "."
        )
        add("")
    if not r["records"]["naming"]:
        add("None.")
        add("")

    h = r["helper"]
    add(f"#### 6. `{HELPER}`")
    add("")
    if not h["definitions"]:
        add("Not defined.")
    for d in h["definitions"]:
        add(
            f"- Defined at `{d['path']}:{d['line']}-{d['end']}`, arguments `({d['arguments']})`; "
            f"the package's `package_provenance({d['package_arguments']})`."
        )
        if d["difference"]:
            add(
                "- Its body against the package's, docstrings removed (`-` the package's only, "
                "`+` the client's only):"
            )
            add("")
            add("  ```")
            for line in d["difference"]:
                add(f"  {line}")
            add("  ```")
        else:
            add("- Its body equals the package's, docstrings removed.")
    for c in h["recorded_distributions"]:
        add(
            f"- `RECORDED_DISTRIBUTIONS = {c['assigned']}` at `{c['path']}:{c['line']}`."
        )
    if h["imports"]:
        add(
            "- Imported at "
            + ", ".join(
                f"`{c['path']}:{c['line']}` (from `{c['module']}`)"
                for c in h["imports"]
            )
            + "."
        )
    if h["calls"]:
        add(
            "- Called at "
            + ", ".join(
                f"`{c['path']}:{c['line']}` ({c['positional']} positional"
                + (f", {', '.join(c['keywords'])}" if c["keywords"] else "")
                + ")"
                for c in h["calls"]
            )
            + "."
        )
    add("")

    o = r["other_files"]
    add(f"#### 7. Tracked files other than `.py` matching `{NON_PY_PATTERN}`")
    add("")
    if o["counts"]:
        add(
            "Lines by top directory: "
            + ", ".join(f"`{k}` {v}" for k, v in o["counts"].items())
            + "."
        )
        add("")
    else:
        add("None.")
        add("")
    if o["lines"]:
        add("Outside the campaign records (text squeezed, first 110 characters):")
        add("")
        add("| File | Line | Text |")
        add("|---|---|---|")
        for x in o["lines"]:
            add(f"| `{x['path']}` | {x['line']} | {cell(x['text'])} |")
        add("")

    add("#### 8. `.gitignore` and the registry")
    add("")
    if r["gitignore_var"] is None:
        add("- No `.gitignore`.")
    elif r["gitignore_var"]:
        add(
            "- `.gitignore` ignores `var/`: "
            + ", ".join(f"`:{g['line']}` `{g['text']}`" for g in r["gitignore_var"])
            + "."
        )
    else:
        add("- `.gitignore` does not ignore `var/`.")
    if r["registries"]:
        add(
            "- Module-level registry mappings: "
            + ", ".join(
                f"`{g['name']}` at `{g['path']}:{g['line']}` ({g['keys']} keys)"
                for g in r["registries"]
            )
            + "."
        )
    else:
        add("- No module-level `factories` or `_factories` mapping.")
    s = r["inventory_specs"]
    add(
        f"- `def inventory_spec`: {len(s['definitions'])} in {s['files']} files"
        + (
            ": "
            + ", ".join(f"`{d['path']}:{d['line']}`" for d in s["definitions"])
            + "."
            if s["definitions"]
            else "."
        )
    )
    if r["polymorphic_parents"]:
        add(
            "- `Parent(..., types=...)`: "
            + ", ".join(
                f"`{p['path']}:{p['line']}` (`{cell(p['types'])}`)"
                for p in r["polymorphic_parents"]
            )
            + "."
        )
    else:
        add("- No `Parent(..., types=...)` call.")
    if r["unparsed"]:
        add("")
        add(
            "Not parseable: "
            + ", ".join(f"`{u['path']}` ({u['error']})" for u in r["unparsed"])
            + "."
        )
    if r["unknown"]:
        add("")
        add("**A name is unknown** (exit 3).")
    return "\n".join(out) + "\n"


# =================================================================================================


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0].strip())
    parser.add_argument("client", choices=sorted(CLIENTS) + ["path"])
    parser.add_argument(
        "--commit", help="the commit to measure (default: the checklist's)"
    )
    parser.add_argument(
        "--repository",
        help="with the client 'path' only: the git repository to measure (a fixture)",
    )
    parser.add_argument("--json", action="store_true", help="JSON in place of Markdown")
    args = parser.parse_args(argv)

    if args.client == "path":
        if not (args.repository and args.commit):
            parser.error("path needs --repository and --commit")
        label, repository, commit = (
            f"the repository at {args.repository}",
            Path(args.repository).resolve(),
            args.commit,
        )
    else:
        if args.repository:
            parser.error("--repository is for the client 'path' only")
        label, name, commit = CLIENTS[args.client]
        repository, commit = CODE_DIR / name, args.commit or commit

    try:
        baseline = Baseline()
        fates = Fates(baseline, check_table(baseline))
        report = measure(label, repository, commit, args.client == "sgk", fates)
    except CannotRead as e:
        print(f"measure_client_registry: cannot read: {e}", file=sys.stderr)
        return 2
    except TableDisagrees as e:
        print(
            f"measure_client_registry: the table disagrees with the package: {e}",
            file=sys.stderr,
        )
        return 1

    if args.json:
        sys.stdout.write(json.dumps(report, indent=1, sort_keys=True) + "\n")
    else:
        sys.stdout.write(markdown(report))
    return 3 if report["unknown"] else 0


if __name__ == "__main__":
    sys.exit(main())
