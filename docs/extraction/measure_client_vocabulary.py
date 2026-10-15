#!/usr/bin/env python3
"""
Measure the three clients' vocabulary for the package's guard (extraction prompt 05a, section 2.2;
README section 6.2, U10).

The guard, ``runregistrykit/tests/test_package_is_generic.py``, forbids the package and its tests
to name anything of a client. What a client's words are is measured here, once, from the clients'
own repositories, and held as data in ``runregistrykit/tests/data/client_vocabulary.json``. The
guard reads that file and never a client, so the suite runs with no client present.

Each client is read **only** through ``git rev-parse``, ``git cat-file -e``, ``git ls-tree`` and
``git show`` at a fixed commit. Nothing of a client is imported, run or opened, and no client's
working tree is read. For each client the file holds:

- the commit, in full;
- the registry's keys: the string keys of the dict literal assigned at module level to the
  registry's name in the registry's module, in the order written;
- the columns: the first argument of each ``Column(...)`` call (``sqla.Column`` or a bare
  ``Column``) whose first argument is a string literal, in every ``.py`` module of the factory
  directory, recursively, but ``base.py`` and ``__init__.py``, sorted and unique, with the modules
  read;
- the top-level packages: each top-level directory holding an ``__init__.py``, sorted;
- the campaigns: the directory names directly under the client's campaigns directory, sorted.

Under the key ``listed`` it also holds the words that cannot be measured this way, each group with
where this repository's records name it.

The file holds the measurement only. Which of these words the guard forbids is the guard's rule.
The ``summary`` counts what was read, before any rule.

Run it from the repository root with the venv's interpreter:

    ./venv/bin/python docs/extraction/measure_client_vocabulary.py [--output PATH]

It writes ``runregistrykit/tests/data/client_vocabulary.json``, or ``PATH``, and refuses to
overwrite a file that exists: the committed measurement is never edited. Two runs at the same
commits give the same bytes. The script exits 0 when it wrote the file, 1 when it refused to
overwrite one, and 2 when it cannot read a client.
"""

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

CODE_DIR = Path("/Users/ds283/Documents/Code")
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    REPO_ROOT / "runregistrykit" / "tests" / "data" / "client_vocabulary.json"
)

NOT_FACTORIES = {"base.py", "__init__.py"}

# client -> (repository, commit, registry module, registry name, factory directory, campaigns)
CLIENTS = {
    "SGK": (
        "SecondaryGWKit",
        "14bcac0",
        "config/datastore.py",
        "factories",
        "ObjectFactories",
        "prompts",
    ),
    "CPBH": (
        "ChamPBH",
        "c21cdfb",
        "config/datastore.py",
        "factories",
        "ObjectFactories",
        "prompts",
    ),
    "SI": (
        "StochasticInstantons",
        "5fb4a1d",
        "Datastore/SQL/Datastore.py",
        "_factories",
        "Datastore/SQL/ObjectFactories",
        ".prompts",
    ),
}

# the words that cannot be measured: each group with where this repository's records name it
LISTED = {
    "the clients' own names": {
        "where": "README section 0; SI is not listed, being a common abbreviation",
        "words": ["SecondaryGWKit", "ChamPBH", "StochasticInstantons", "SGK", "CPBH"],
    },
    "SGK's driver and store names that the package and its tests cite": {
        "where": "[00-package-prose-names-sgk], [02-the-ported-tests-name-sgk]",
        "words": [
            "realistic_large_x",
            "quadsource_atol_sweep",
            "scoped_pipeline_run",
            "handover-A3-baseline-lambdacdm",
            "handover-atol-sweep",
            "a3-pilot",
            "A3",
            "main.py",
        ],
    },
    "SGK's names as identifiers in the ported tests": {
        "where": "[02-the-ported-tests-name-sgk]",
        "words": [
            "TestLiveA3Shape",
            "a3_shaped",
            "sweep_shaped",
            "test_deleting_one_quadsourceintegral_row",
        ],
    },
}


class CannotRead(Exception):
    pass


def git(repository: str, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(CODE_DIR / repository), *args], capture_output=True
    )
    if result.returncode != 0:
        raise CannotRead(
            f"git {' '.join(args)} failed in {repository}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout.decode("utf-8")


def show(repository: str, commit: str, path: str) -> ast.Module:
    text = git(repository, "show", f"{commit}:{path}")
    try:
        return ast.parse(text, filename=f"{repository}:{commit}:{path}")
    except SyntaxError as e:
        raise CannotRead(f"{repository}:{commit}:{path} does not parse: {e}")


def module_assignment(tree: ast.Module, name: str) -> ast.expr:
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return node.value
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == name
            and node.value is not None
        ):
            return node.value
    raise CannotRead(f"no module-level assignment to {name}")


def registry_keys(tree: ast.Module, name: str) -> List[str]:
    value = module_assignment(tree, name)
    if not isinstance(value, ast.Dict):
        raise CannotRead(f"{name} is not a dict literal")
    keys = []
    for key in value.keys:
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
            raise CannotRead(f"{name} has a key that is not a string literal")
        keys.append(key.value)
    return keys


def column_names(tree: ast.Module) -> set:
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        called = (
            func.id
            if isinstance(func, ast.Name)
            else func.attr if isinstance(func, ast.Attribute) else None
        )
        first = node.args[0]
        if (
            called == "Column"
            and isinstance(first, ast.Constant)
            and isinstance(first.value, str)
        ):
            found.add(first.value)
    return found


def require_path(repository: str, commit: str, path: str, what: str) -> None:
    """Refuse, as unreadable, a path that is not in the commit."""
    result = subprocess.run(
        ["git", "-C", str(CODE_DIR / repository), "cat-file", "-e", f"{commit}:{path}"],
        capture_output=True,
    )
    if result.returncode != 0:
        raise CannotRead(f"{what} {path} is not in {repository} at {commit}")


def measure(
    repository: str,
    commit: str,
    registry_path: str,
    registry_name: str,
    factories_dir: str,
    campaigns_dir: str,
):
    full = git(repository, "rev-parse", f"{commit}^{{commit}}").strip()
    require_path(repository, full, registry_path, "the registry")
    require_path(repository, full, factories_dir, "the factory directory")
    require_path(repository, full, campaigns_dir, "the campaigns directory")
    keys = registry_keys(show(repository, full, registry_path), registry_name)

    listed = git(repository, "ls-tree", "-r", "--name-only", full, f"{factories_dir}/")
    modules = sorted(
        path
        for path in listed.splitlines()
        if path.endswith(".py") and Path(path).name not in NOT_FACTORIES
    )
    columns = set()
    for path in modules:
        columns |= column_names(show(repository, full, path))

    every = git(repository, "ls-tree", "-r", "--name-only", full)
    packages = sorted(
        {
            parts[0]
            for parts in (path.split("/") for path in every.splitlines())
            if len(parts) == 2 and parts[1] == "__init__.py"
        }
    )

    # `ls-tree` of a directory with a trailing slash lists its entries: "<mode> <type> <sha>\t<path>"
    campaigns = sorted(
        Path(line.split("\t", 1)[1]).name
        for line in git(repository, "ls-tree", full, f"{campaigns_dir}/").splitlines()
        if line.split("\t", 1)[0].split()[1] == "tree"
    )
    return {
        "repository": repository,
        "commit": full,
        "registry": {"module": registry_path, "name": registry_name, "keys": keys},
        "columns": {
            "directory": factories_dir,
            "modules": modules,
            "names": sorted(columns),
        },
        "packages": packages,
        "campaigns": {"directory": campaigns_dir, "names": campaigns},
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    if args.output.exists():
        print(
            f"!! {args.output} exists; a re-measure writes a new file", file=sys.stderr
        )
        return 1

    clients: Dict[str, dict] = {}
    try:
        for client, spec in CLIENTS.items():
            clients[client] = measure(*spec)
    except CannotRead as e:
        print(f"!! {e}", file=sys.stderr)
        return 2

    tables = set().union(*(set(c["registry"]["keys"]) for c in clients.values()))
    columns = set().union(*(set(c["columns"]["names"]) for c in clients.values()))
    packages = set().union(*(set(c["packages"]) for c in clients.values()))
    campaigns = set().union(*(set(c["campaigns"]["names"]) for c in clients.values()))
    summary = {
        "read, before any rule of the guard": {
            "registry keys, all clients": len(tables),
            "column names, all clients": len(columns),
            "packages, all clients": len(packages),
            "campaigns, all clients": len(campaigns),
            "listed words": sum(len(g["words"]) for g in LISTED.values()),
        },
        "per client": {
            client: {
                "registry keys": len(c["registry"]["keys"]),
                "factory modules": len(c["columns"]["modules"]),
                "column names": len(c["columns"]["names"]),
                "packages": len(c["packages"]),
                "campaigns": len(c["campaigns"]["names"]),
            }
            for client, c in clients.items()
        },
    }
    data = {
        "written by": "docs/extraction/measure_client_vocabulary.py",
        "what": "the three clients' vocabulary, read by git at fixed commits, for the "
        "package's guard (extraction prompt 05a, U10)",
        "clients": clients,
        "listed": LISTED,
        "summary": summary,
    }
    text = json.dumps(data, indent=2, ensure_ascii=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)

    print(f"wrote {args.output} ({len(text.encode('utf-8'))} bytes)")
    for client, c in clients.items():
        counts = summary["per client"][client]
        print(
            f"  {client}: {c['repository']} at {c['commit']}: "
            f"{counts['registry keys']} registry keys, "
            f"{counts['column names']} column names in {counts['factory modules']} modules, "
            f"{counts['packages']} packages, {counts['campaigns']} campaigns"
        )
    read = summary["read, before any rule of the guard"]
    print(
        f"  all clients: {read['registry keys, all clients']} registry keys, "
        f"{read['column names, all clients']} column names, "
        f"{read['packages, all clients']} packages, "
        f"{read['campaigns, all clients']} campaigns; "
        f"{read['listed words']} listed words"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
