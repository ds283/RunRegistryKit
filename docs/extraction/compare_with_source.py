#!/usr/bin/env python3
"""
The equivalence check of the extraction campaign (prompt 01 §2.6; README §4 and §5 rule 8).

The package ``runregistrykit`` is SecondaryGWKit's ``RunRegistry/`` at the import commit, changed
only by the classes of difference prompt 01 §2.4 allows. This script checks that, from the
repository root, with the venv's interpreter:

    ./venv/bin/python docs/extraction/compare_with_source.py

It reads the source only with ``git -C <SGK> ls-tree|rev-parse|show`` at the import commit, never
from the source's working tree, and imports nothing of the source or of this package. It writes
nothing.

**The frozen tree.** ``git ls-tree -r <commit> -- RunRegistry/`` must equal the rows of ``TABLE``
under ``RunRegistry/`` exactly, path and blob, with no row missing or extra; and every row outside
``RunRegistry/`` (the shard fixture) must be the blob ``git rev-parse <commit>:<path>`` gives.

**The fates.** Each row of ``TABLE`` has one fate:
- *imported*: the package file must exist, and is compared line by line (below);
- *pending, NN*: ported by a later prompt. While its package file is absent it is reported as
  pending. If it is present it fails: no rule here covers it, and the prompt that ports it extends
  this script to check it;
- *not imported*: no file of that name may exist under ``runregistrykit/``, neither at the path the
  source's name maps to nor anywhere else in the package with the same file name.

**Every file is declared.** Every ``.py`` file under ``runregistrykit/`` (outside ``__pycache__``)
is either the package file of a row of ``TABLE`` or one of ``NEW_FILES``, the files with no
source. Any other fails as NOT DECLARED, and a declared new file that is absent fails as MISSING.
A prompt that adds a file declares it here.

**How a line is classified.** The source and the package file are compared line by line
(``difflib``, no junk heuristic). Equal lines need no class. Where a run of source lines is
replaced by a run of package lines *of the same length*, the pairs are taken in turn; a pair is
**D-name** exactly when the D-name substitution applied to the source line gives the package line,
indentation and trailing text included:

    re.sub(r"\\bRunRegistry\\b", "runregistrykit", source_line) == package_line

That is a rule applied to the source line, not a pattern a package line may match, and no line
number appears in it. A pair it does not map, every added or deleted line, and every line of a
replaced run whose two sides differ in length, is UNCLASSIFIED.

There is **no D-fmt rule**: ``black`` 25.1.0 leaves the renamed modules unchanged, so formatting
accounts for no difference, and its count is reported as 0. A line ``black`` had changed would be
UNCLASSIFIED here.

**The rename is complete.** D-name renames *every* whole-word occurrence, so no line of an
imported package module may match ``\\bRunRegistry\\b``. A line on which the rename was not made
equals its source and passes the comparison above; this check fails it, naming file and line.

The script prints, for each imported file, its count per class and every line it could not
classify, and then the pending, absent and declared files. It exits 0 when every row of the frozen
tree is as the table says, every differing line is classified, the rename is complete, and every
file is present and declared, pending files notwithstanding; 1 when not; and 2 when it cannot run
(``git`` fails).
"""

import difflib
import re
import subprocess
import sys
from pathlib import Path

# --- the source -----------------------------------------------------------------------------------

SGK_PATH = "/Users/ds283/Documents/Code/SecondaryGWKit"
IMPORT_COMMIT = "a45aefc702de643c330372dd6d2d983f38bb8eed"
SOURCE_TREE = "RunRegistry/"

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "runregistrykit"

# --- the fate of every source file (prompt 01 §2.5) -----------------------------------------------

IMPORTED = "imported by 01"
NOT_IMPORTED = "not imported"


def pending(prompt):
    return f"pending, {prompt}"


# (source path at the import commit, its blob, its fate, the package file or None)
TABLE = (
    (
        "RunRegistry/__init__.py",
        "0228a1a066793332191affe90c4b309a153aa60c",
        IMPORTED,
        "runregistrykit/__init__.py",
    ),
    (
        "RunRegistry/__main__.py",
        "88cf6ddd2b7603fc718fd6b3d7ed9722261a874f",
        IMPORTED,
        "runregistrykit/__main__.py",
    ),
    (
        "RunRegistry/stores.py",
        "a0f18ba49a25fe795af79baa8f82ce0e09cf3b25",
        IMPORTED,
        "runregistrykit/stores.py",
    ),
    (
        "RunRegistry/tests/__init__.py",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
        IMPORTED,
        "runregistrykit/tests/__init__.py",
    ),
    (
        "RunRegistry/tests/store_fixtures.py",
        "391f31fc2155c1f2d8f2350d306272ee6e0ae54e",
        pending("02"),
        "runregistrykit/tests/store_fixtures.py",
    ),
    (
        "RunRegistry/tests/test_run_registry.py",
        "01c3ea37d8491c63300667f5a181f3bad91000ab",
        pending("02"),
        "runregistrykit/tests/test_run_registry.py",
    ),
    (
        "RunRegistry/tests/test_store_sidecar.py",
        "533d1118447527cfef65a833525516fcadbbc2e7",
        pending("02"),
        "runregistrykit/tests/test_store_sidecar.py",
    ),
    (
        "RunRegistry/tests/test_store_copy_move.py",
        "4be78d983aa83d5d7d39fc440519347cc87386bd",
        pending("02"),
        "runregistrykit/tests/test_store_copy_move.py",
    ),
    (
        "RunRegistry/tests/test_store_command_line.py",
        "6f111e29e9b695340a88bf19eb18a50e89a9ea05",
        pending("02"),
        "runregistrykit/tests/test_store_command_line.py",
    ),
    (
        "RunRegistry/tests/test_store_amend.py",
        "8b7db110f76ae74bfb4716fe12d7192bac38265e",
        pending("02"),
        "runregistrykit/tests/test_store_amend.py",
    ),
    (
        "RunRegistry/tests/test_store_amend_residuals.py",
        "0c6e6a2ca5d59b74dcb960111a5cd05ed2d991f4",
        pending("02"),
        "runregistrykit/tests/test_store_amend_residuals.py",
    ),
    (
        "RunRegistry/tests/test_store_retire.py",
        "3cf05cc02d6b00849a4eff4972ccbedd0a4fa51d",
        pending("04"),
        "runregistrykit/tests/test_store_retire.py",
    ),
    (
        "RunRegistry/tests/test_store_retire_references.py",
        "9a3264a7f5977311161f724651b4e1d27cfa0866",
        pending("04"),
        "runregistrykit/tests/test_store_retire_references.py",
    ),
    (
        "RunRegistry/tests/test_store_fingerprint.py",
        "5039b4792210c1227230ec09b48da641b6f62e9f",
        pending("04"),
        "runregistrykit/tests/test_store_fingerprint.py",
    ),
    (
        "RunRegistry/tests/test_build_rehearsal_scope.py",
        "8b3c8519d3956b97cce84ea8224c621f37d88cd0",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/test_killed_handler.py",
        "213f2a8d7d017f845b85ea209f8e87886539988b",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/test_pipeline_adoption.py",
        "f3205799afa5626fe440e409fce37c1cb9fa04c7",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/test_prune_on_resume.py",
        "23533e68f7682a172ecf7246b84bbd749b1e5ff8",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/test_quadsource_atol_sweep_prepare.py",
        "527a9878d588309fd6f82f214bc655be627cea5d",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/data/full_store_fingerprint.json",
        "58b35c3677f40e5421c7390ac282f1e6e808cd68",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-07.json",
        "2fea28b072cd9f4cdb15062ab355c9c08a45d57e",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-08.json",
        "511ff2d3873437480cbb6af028ba8fbdc5699b87",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09a.json",
        "bd6a855c9d109a8da654ab790eadfc681ad5cea8",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09b.json",
        "01d7ef02e88c53a4160e5660711f0746f3ae4a90",
        NOT_IMPORTED,
        None,
    ),
    (
        "RunRegistry/tests/data/full_store_fingerprint_datastore-integrity-09c.json",
        "6cf0a39496c0e96bd3b2640324482e7d51686908",
        NOT_IMPORTED,
        None,
    ),
    (
        "StoreFixtures/shard_store_fixtures.py",
        "1375949aacde2263de991785055cd7dfabc57251",
        pending("02"),
        "runregistrykit/tests/shard_store_fixtures.py",
    ),
)

# package files with no source, and the prompt that declared each
NEW_FILES = {
    "runregistrykit/tests/test_package_imports.py": "01 §2.7: the import test",
}

# --- the classes of difference (prompt 01 §2.4) ---------------------------------------------------

OLD_NAME = re.compile(r"\bRunRegistry\b")
NEW_NAME = "runregistrykit"


def d_name(source_line: str) -> str:
    """The image of ``source_line`` under D-name: every whole-word ``RunRegistry`` renamed."""
    return OLD_NAME.sub(NEW_NAME, source_line)


CLASSES = ("D-name", "D-fmt")  # D-fmt has no rule: its count is always 0


# --- git ------------------------------------------------------------------------------------------


class CannotRun(Exception):
    pass


def git(*args) -> str:
    result = subprocess.run(
        ["git", "-C", SGK_PATH, *args], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise CannotRun(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


# --- the checks -----------------------------------------------------------------------------------


def check_frozen_tree():
    """Compare the source tree and the fixture with ``TABLE``; returns a list of failures."""
    failures = []
    in_tree = {}
    for row in git("ls-tree", "-r", IMPORT_COMMIT, "--", SOURCE_TREE).splitlines():
        meta, path = row.split("\t", 1)
        _mode, _kind, blob = meta.split()
        in_tree[path] = blob
    in_table = {src: blob for src, blob, _, _ in TABLE if src.startswith(SOURCE_TREE)}

    print(
        f"{SOURCE_TREE} at the import commit: {len(in_tree)} rows; "
        f"the table: {len(in_table)} rows"
    )
    for path in sorted(in_table.keys() - in_tree.keys()):
        failures.append(f"FROZEN TREE: {path} is in the table but not in the tree")
    for path in sorted(in_tree.keys() - in_table.keys()):
        failures.append(
            f"FROZEN TREE: {path} (blob {in_tree[path]}) is in the tree but not in the table"
        )
    for path in sorted(in_tree.keys() & in_table.keys()):
        if in_tree[path] != in_table[path]:
            failures.append(
                f"FROZEN TREE: {path} is blob {in_tree[path]} at the import commit, "
                f"the table says {in_table[path]}"
            )
    if not failures:
        print(f"  equal, path for path and blob for blob ({len(in_tree)} rows)")

    for src, blob, _, _ in TABLE:
        if src.startswith(SOURCE_TREE):
            continue
        actual = git("rev-parse", f"{IMPORT_COMMIT}:{src}").strip()
        if actual == blob:
            print(f"{src} at the import commit: blob {actual} (as the table says)")
        else:
            failures.append(
                f"FROZEN TREE: {src} is blob {actual} at the import commit, "
                f"the table says {blob}"
            )
    for failure in failures:
        print(f"  !! {failure}")
    return failures


def _lines(text: str):
    """The lines of ``text``, without their newlines; a missing final newline is marked."""
    if text == "":
        return []
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    else:
        lines[-1] += "  <no newline at end of file>"
    return lines


def compare_module(source_path: str, package_path: str):
    """Compare one imported file line by line; returns (counts, classified, unclassified)."""
    src = _lines(git("show", f"{IMPORT_COMMIT}:{source_path}"))
    pkg = _lines((REPO_ROOT / package_path).read_text(encoding="utf-8"))

    counts = {"identical": 0}
    counts.update({name: 0 for name in CLASSES})
    classified = []
    unclassified = []

    matcher = difflib.SequenceMatcher(None, src, pkg, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            counts["identical"] += i2 - i1
            continue

        if tag == "replace" and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                s, p = src[i1 + k], pkg[j1 + k]
                where = f"source :{i1 + k + 1} / package :{j1 + k + 1}"
                if s == p:
                    counts["identical"] += 1
                elif d_name(s) == p:
                    counts["D-name"] += 1
                    classified.append(f"D-name {where}\n    - {s}\n    + {p}")
                else:
                    unclassified.append(
                        f"CHANGED (no rule maps it) {where}\n    - {s}\n    + {p}"
                    )
            continue

        # an insertion, a deletion, or a replacement of a different length: never classified
        for i in range(i1, i2):
            unclassified.append(f"DELETED source :{i + 1}\n    - {src[i]}")
        for j in range(j1, j2):
            unclassified.append(f"ADDED   package :{j + 1}\n    + {pkg[j]}")

    # the rename is complete: no imported line keeps the source's name
    for n, line in enumerate(pkg, start=1):
        if OLD_NAME.search(line):
            unclassified.append(
                f"NOT RENAMED {package_path}:{n} still has the word RunRegistry\n"
                f"    = {line}"
            )

    return counts, classified, unclassified


def package_files():
    root = REPO_ROOT / PACKAGE
    if not root.is_dir():
        return []
    return sorted(
        p.relative_to(REPO_ROOT).as_posix()
        for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )


def main() -> int:
    print(
        f"Equivalence check: {PACKAGE} against SecondaryGWKit ({SGK_PATH}) "
        f"at {IMPORT_COMMIT}"
    )
    print()
    failed = bool(check_frozen_tree())

    imported = [row for row in TABLE if row[2] == IMPORTED]
    pending_rows = [row for row in TABLE if row[2].startswith("pending")]
    not_imported = [row for row in TABLE if row[2] == NOT_IMPORTED]
    here = package_files()

    totals = {name: 0 for name in CLASSES}
    for src, _, _, target in imported:
        print()
        print(f"{target}  <-  {src}  [{IMPORTED}]")
        if not (REPO_ROOT / target).is_file():
            print("  !! MISSING: the package file does not exist")
            failed = True
            continue
        counts, classified, unclassified = compare_module(src, target)
        for name, n in counts.items():
            print(f"  {name}: {n}")
            if name in totals:
                totals[name] += n
        print(f"  unclassified: {len(unclassified)}")
        for line in classified:
            print("    " + line.replace("\n", "\n    "))
        for line in unclassified:
            print("  !! " + line.replace("\n", "\n  "))
        if unclassified:
            failed = True

    print()
    print(f"Pending, ported by a later prompt: {len(pending_rows)}")
    for src, _, fate, target in pending_rows:
        if (REPO_ROOT / target).exists():
            print(
                f"  !! PRESENT, NOT CHECKED: {target} ({fate}, from {src}) exists, and no "
                "rule here covers it; the prompt that ports it extends this check"
            )
            failed = True
        else:
            print(f"  {fate}: {target}  <-  {src}")

    print()
    absent = 0
    for src, _, _, _ in not_imported:
        mapped = PACKAGE + "/" + src[len(SOURCE_TREE) :]
        name = src.rsplit("/", 1)[-1]
        found = sorted({p for p in here if p == mapped or p.rsplit("/", 1)[-1] == name})
        if found:
            for path in found:
                print(f"  !! NOT IMPORTED, BUT PRESENT: {path} (the source's {src})")
            failed = True
        else:
            absent += 1
    print(f"Not imported, and absent from {PACKAGE}/: {absent} of {len(not_imported)}")

    print()
    print(f"Files with no source (declared): {len(NEW_FILES)}")
    for path, why in NEW_FILES.items():
        present = (REPO_ROOT / path).is_file()
        print(f"  {path}: {'present' if present else 'MISSING'} ({why})")
        if not present:
            failed = True

    targets = {target for _, _, _, target in TABLE if target is not None}
    undeclared = [
        p for p in here if p.endswith(".py") and p not in targets and p not in NEW_FILES
    ]
    print()
    print(f"Undeclared files under {PACKAGE}/: {len(undeclared)}")
    for path in undeclared:
        print(f"  !! NOT DECLARED: {path}")
    if undeclared:
        failed = True

    print()
    print(
        f"Summary: {len(imported)} imported (D-name {totals['D-name']}, "
        f"D-fmt {totals['D-fmt']}); {len(pending_rows)} pending; "
        f"{absent} not imported and absent; {len(NEW_FILES)} declared new"
    )
    print("RESULT: " + ("FAIL" if failed else "OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CannotRun as e:
        print(f"CANNOT RUN: {e}")
        sys.exit(2)
