#!/usr/bin/env python3
"""
The equivalence check of the extraction campaign (prompt 01 §2.6, extended by prompt 02 §2.4;
README §4 and §5 rule 8).

The package ``runregistrykit`` is SecondaryGWKit's ``RunRegistry/`` at the import commit (and, from
prompt 02, the tests and fixtures ported with it), changed only by the classes of difference
below. This script checks that, from the repository root, with the venv's interpreter:

    ./venv/bin/python docs/extraction/compare_with_source.py

It reads the source only with ``git -C <SGK> ls-tree|rev-parse|show`` at the import commit, never
from the source's working tree, and imports nothing of the source or of this package. It writes
nothing. It imports ``black``, pinned (below).

**The frozen tree.** ``git ls-tree -r <commit> -- RunRegistry/`` must equal the rows of ``TABLE``
under ``RunRegistry/`` exactly, path and blob, with no row missing or extra; and every row outside
``RunRegistry/`` (the shard fixture) must be the blob ``git rev-parse <commit>:<path>`` gives.

**The fates.** Each row of ``TABLE`` has one fate:
- *imported by 01* or *ported by 02*: the package file must exist, and is checked by the rule
  below, the same rule for both;
- *pending, NN*: ported by a later prompt. While its package file is absent it is reported as
  pending. If it is present it fails: no rule here covers it, and the prompt that ports it extends
  this script to check it;
- *not imported*: no file of that name may exist under ``runregistrykit/``, neither at the path the
  source's name maps to nor anywhere else in the package with the same file name.

**Every file is declared.** Every ``.py`` file under ``runregistrykit/`` (outside ``__pycache__``)
is either the package file of a row of ``TABLE`` or one of ``NEW_FILES``, the files with no
source. Any other fails as NOT DECLARED, and a declared new file that is absent fails as MISSING.
A prompt that adds a file declares it here.

**The rule for a checked file.** The differences allowed are three substitutions and no others:

- *D-name*, the package's name: ``\\bRunRegistry\\b`` becomes ``runregistrykit``;
- *D-fix*, the shard fixture's new home: ``\\bStoreFixtures\\.shard_store_fixtures\\b`` becomes
  ``runregistrykit.tests.shard_store_fixtures`` and ``\\bStoreFixtures/shard_store_fixtures\\.py``
  becomes ``runregistrykit/tests/shard_store_fixtures.py``;
- *D-fmt*, ``black`` 25.1.0 with no configuration.

The rule, in four steps, with no line number in it:

1. T, the *renamed source*, is the source with D-name and D-fix applied to every line, one line
   for one line. The lines D-name changes, and the lines D-fix changes, are counted (a line that
   needed both would be counted under each).
2. The package file must equal ``black.format_str(T, mode=black.Mode())`` exactly. The lines
   where ``black(T)`` differs from T (the non-equal ``difflib`` opcodes, no junk heuristic) are
   D-fmt: they are counted, as package lines and as hunks, and each hunk is printed with its T
   and package lines. D-fmt is a property of the source, so a breakage in the package does not
   move any of the three counts.
3. If the package differs from ``black(T)``, every differing line (``difflib`` between
   ``black(T)`` and the package, with package line numbers) is printed as UNCLASSIFIED and the
   check fails. Nothing is widened to accept a difference.
4. Completeness: no line of a checked package file may match ``\\bRunRegistry\\b`` or
   ``\\bStoreFixtures\\b``; one that does fails, named by file and line. A line left unrenamed
   equals T on that line only if the source did not need the rename, so it would otherwise pass.

For the files prompt 01 imported, ``black(T) == T``, so step 2 requires the package to equal T
line for line, which is what 01's per-pair rule required.

**``black`` is a dependency of this check, pinned.** The script exits 2 (cannot run) unless
``black.__version__ == "25.1.0"``, so the reflows it accepts are those of the version recorded
here. It uses ``black.Mode()``, which infers the target versions from each file's content. The
command ``black`` run at the repository root reads ``pyproject.toml`` and infers its target
versions from ``requires-python`` instead; on every file checked here the two give the same
output (measured, prompt 02), but they could differ in principle, and ``black --check
runregistrykit docs`` (prompt 02 §3.5) would then show it.

The script prints, for each checked file, its counts and every instance of each class and every
line it could not classify, and then the pending, absent and declared files. It exits 0 when every
row of the frozen tree is as the table says, every checked file equals ``black(T)``, the rename is
complete, and every file is present and declared, pending files notwithstanding; 1 when not; and 2
when it cannot run (``git`` fails, or ``black`` is missing, is not 25.1.0, or fails on T).
"""

import difflib
import re
import subprocess
import sys
from pathlib import Path

try:
    import black
except ImportError:  # reported as CANNOT RUN, in main()
    black = None

BLACK_VERSION = "25.1.0"

# --- the source -----------------------------------------------------------------------------------

SGK_PATH = "/Users/ds283/Documents/Code/SecondaryGWKit"
IMPORT_COMMIT = "a45aefc702de643c330372dd6d2d983f38bb8eed"
SOURCE_TREE = "RunRegistry/"

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "runregistrykit"

# --- the fate of every source file (prompt 01 §2.5) -----------------------------------------------

IMPORTED = "imported by 01"
PORTED = "ported by 02"
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
        PORTED,
        "runregistrykit/tests/store_fixtures.py",
    ),
    (
        "RunRegistry/tests/test_run_registry.py",
        "01c3ea37d8491c63300667f5a181f3bad91000ab",
        PORTED,
        "runregistrykit/tests/test_run_registry.py",
    ),
    (
        "RunRegistry/tests/test_store_sidecar.py",
        "533d1118447527cfef65a833525516fcadbbc2e7",
        PORTED,
        "runregistrykit/tests/test_store_sidecar.py",
    ),
    (
        "RunRegistry/tests/test_store_copy_move.py",
        "4be78d983aa83d5d7d39fc440519347cc87386bd",
        PORTED,
        "runregistrykit/tests/test_store_copy_move.py",
    ),
    (
        "RunRegistry/tests/test_store_command_line.py",
        "6f111e29e9b695340a88bf19eb18a50e89a9ea05",
        PORTED,
        "runregistrykit/tests/test_store_command_line.py",
    ),
    (
        "RunRegistry/tests/test_store_amend.py",
        "8b7db110f76ae74bfb4716fe12d7192bac38265e",
        PORTED,
        "runregistrykit/tests/test_store_amend.py",
    ),
    (
        "RunRegistry/tests/test_store_amend_residuals.py",
        "0c6e6a2ca5d59b74dcb960111a5cd05ed2d991f4",
        PORTED,
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
        PORTED,
        "runregistrykit/tests/shard_store_fixtures.py",
    ),
)

# package files with no source, and the prompt that declared each
NEW_FILES = {
    "runregistrykit/tests/test_package_imports.py": "01 §2.7: the import test",
}

# --- the classes of difference (prompt 01 §2.4; prompt 02 §2.3) -----------------------------------

OLD_NAME = re.compile(r"\bRunRegistry\b")
NEW_NAME = "runregistrykit"

# the shard fixture's new home: the dotted form (imports), and the path form (docstrings)
FIX_DOTTED = re.compile(r"\bStoreFixtures\.shard_store_fixtures\b")
FIX_PATH = re.compile(r"\bStoreFixtures/shard_store_fixtures\.py")
OLD_FIXTURES = re.compile(r"\bStoreFixtures\b")


def d_name(source_line: str) -> str:
    """The image of ``source_line`` under D-name: every whole-word ``RunRegistry`` renamed."""
    return OLD_NAME.sub(NEW_NAME, source_line)


def d_fix(source_line: str) -> str:
    """The image of ``source_line`` under D-fix: the shard fixture's imports and path."""
    line = FIX_DOTTED.sub("runregistrykit.tests.shard_store_fixtures", source_line)
    return FIX_PATH.sub("runregistrykit/tests/shard_store_fixtures.py", line)


CLASSES = ("D-name", "D-fix", "D-fmt")


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


def renamed_source(source_text: str):
    """T: the source with D-name and D-fix applied to every line, one line for one line.

    Returns (T as text, the lines D-name changed, the lines D-fix changed), the last two as lists
    of (source line number, source line, renamed line).
    """
    name_lines, fix_lines, out = [], [], []
    for n, line in enumerate(source_text.split("\n"), start=1):
        named = d_name(line)
        fixed = d_fix(line)
        if named != line:
            name_lines.append((n, line, named))
        if fixed != line:
            fix_lines.append((n, line, fixed))
        out.append(d_fix(named))
    return "\n".join(out), name_lines, fix_lines


def black_of(text: str, what: str) -> str:
    """``black`` 25.1.0 with no configuration; a failure on T means the check cannot run."""
    try:
        return black.format_str(text, mode=black.Mode())
    except (
        Exception
    ) as e:  # black raises several types; T comes from the source, so none is ours
        raise CannotRun(f"black failed on the renamed source of {what}: {e!r}")


def compare_module(source_path: str, package_path: str):
    """Check one file by the rule; returns (counts, classified, unclassified).

    ``counts`` has the three classes (D-fmt in package lines) and ``D-fmt hunks`` and
    ``identical`` (lines the source and package share, unchanged by every class).
    """
    source_text = git("show", f"{IMPORT_COMMIT}:{source_path}")
    package_text = (REPO_ROOT / package_path).read_text(encoding="utf-8")

    t_text, name_lines, fix_lines = renamed_source(source_text)
    expected = black_of(t_text, source_path)

    t = _lines(t_text)
    b = _lines(expected)
    pkg = _lines(package_text)

    classified = []
    unclassified = []
    counts = {name: 0 for name in CLASSES}
    counts["D-fmt hunks"] = 0

    for n, s, p in name_lines:
        counts["D-name"] += 1
        classified.append(f"D-name source :{n}\n    - {s}\n    + {p}")
    for n, s, p in fix_lines:
        counts["D-fix"] += 1
        classified.append(f"D-fix source :{n}\n    - {s}\n    + {p}")

    # D-fmt: where black(T) differs from T, a property of the source alone
    stable = set()  # T lines (numbered from 1) that black leaves as they are
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, t, b, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            stable.update(range(i1 + 1, i2 + 1))
            continue
        counts["D-fmt hunks"] += 1
        counts["D-fmt"] += j2 - j1
        body = [f"    - {line}" for line in t[i1:i2]] + [
            f"    + {line}" for line in b[j1:j2]
        ]
        classified.append(
            f"D-fmt source :{i1 + 1}-{i2} -> package :{j1 + 1}-{j2}\n" + "\n".join(body)
        )
    changed = {n for n, _, _ in name_lines} | {n for n, _, _ in fix_lines}
    counts["identical"] = len(stable - changed)

    # the package must equal black(T) exactly
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, b, pkg, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            continue
        for i in range(i1, i2):
            unclassified.append(
                f"DIFFERS FROM black(T) (black(T) line :{i + 1}, absent from the package)\n    - {b[i]}"
            )
        for j in range(j1, j2):
            unclassified.append(
                f"DIFFERS FROM black(T) (package :{j + 1}, not in black(T))\n    + {pkg[j]}"
            )

    # the rename is complete: no checked line keeps a source name
    for n, line in enumerate(pkg, start=1):
        for pattern, word in (
            (OLD_NAME, "RunRegistry"),
            (OLD_FIXTURES, "StoreFixtures"),
        ):
            if pattern.search(line):
                unclassified.append(
                    f"NOT RENAMED {package_path}:{n} still has the word {word}\n"
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


def require_black():
    if black is None:
        raise CannotRun(
            f"black is not importable; this check needs black {BLACK_VERSION} "
            "(pip install black==" + BLACK_VERSION + ")"
        )
    if black.__version__ != BLACK_VERSION:
        raise CannotRun(
            f"black is {black.__version__}; this check is pinned to black {BLACK_VERSION}, "
            "whose reflows it accepts"
        )


def main() -> int:
    require_black()
    print(
        f"Equivalence check: {PACKAGE} against SecondaryGWKit ({SGK_PATH}) "
        f"at {IMPORT_COMMIT}"
    )
    print()
    failed = bool(check_frozen_tree())

    checked = [row for row in TABLE if row[2] in (IMPORTED, PORTED)]
    pending_rows = [row for row in TABLE if row[2].startswith("pending")]
    not_imported = [row for row in TABLE if row[2] == NOT_IMPORTED]
    here = package_files()

    totals = {name: 0 for name in CLASSES}
    totals["D-fmt hunks"] = 0
    for src, _, fate, target in checked:
        print()
        print(f"{target}  <-  {src}  [{fate}]")
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
    by01 = sum(1 for row in checked if row[2] == IMPORTED)
    print(
        f"Summary: {len(checked)} checked ({by01} by 01, {len(checked) - by01} by 02): "
        f"D-name {totals['D-name']}, D-fix {totals['D-fix']}, "
        f"D-fmt {totals['D-fmt']} in {totals['D-fmt hunks']} hunks; "
        f"{len(pending_rows)} pending; {absent} not imported and absent; "
        f"{len(NEW_FILES)} declared new"
    )
    print("RESULT: " + ("FAIL" if failed else "OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CannotRun as e:
        print(f"CANNOT RUN: {e}")
        sys.exit(2)
