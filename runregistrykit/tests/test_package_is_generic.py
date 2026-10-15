"""
The package's guard: the package and its tests name nothing of any client, cite no campaign
record, and import only what they may.

**What it scans.** Every ``*.py`` under ``runregistrykit/``, the tests and this module included.
``package_files()`` derives the set from the filesystem, not from ``git ls-files`` and not from a
list, so that a module added anywhere is checked before it is committed. A test pins that the
derived set holds every ``*.py`` that ``git ls-files`` lists, so a derivation that came out empty
or narrow cannot pass.

**What it forbids.** The vocabulary of the three clients, measured through ``git`` at fixed
commits by ``docs/extraction/measure_client_vocabulary.py`` and held in
``tests/data/client_vocabulary.json`` (``VOCABULARY``). This module reads that file, never a
client, so it runs with no client present. The forbidden words are the union of the registries'
keys, the identifier columns (a column with an underscore, or with a capital and more than one
character), the clients' top-level packages less ``NOT_PROJECT_PACKAGES`` (English words), the
clients' campaigns and the ``listed`` words, less ``PACKAGE_WORDS`` (the contract's own words,
each with its reason). A word is checked case-sensitively. A code name is checked whole and split
on the underscore; a word in a string or comment is checked whole, by each of its dot-separated
parts and, when it has a hyphen, by each of its hyphen-separated parts. Four scans, each a test
that reports ``file:line word`` for every hit in every file:

1. ``test_no_code_name``: names, attributes, definitions, arguments, keywords and imported names;
2. ``test_no_string_or_docstring``: every string constant, docstrings and f-string text included;
3. ``test_no_comment``: every comment;
4. ``test_no_citation``: in strings and comments, a path under a directory of campaign prompts
   (that directory's name followed by a slash), the word for a prompt, singular or plural, followed
   by a space and two digits, and the section sign followed by a digit, with an optional space.
   The package's history is in ``PROVENANCE.md`` and the campaign's records, not in its prose.
   The pattern is built from parts below, so that this module holds no citation.

**What it allows.** ``test_every_import_is_allowed``: in the five package modules, the standard
library and the package itself anywhere, and ``datastorekit`` only inside a function body of the
store layer or the fingerprinter; in the tests, the standard library, the package itself,
``datastorekit``, ``sqlalchemy`` and ``ray``. Nothing else, and no client package anywhere.
``test_the_allow_list`` pins that rule both ways without a mutation.

**The known hits.** ``tests/data/known_hits.json`` lists, for each scan, the hits the package and
its tests are known to hold, as ``[file, word, count]`` entries, sorted, counted by file and word
and not by line, so that an edit does not renumber the rest. Each scan must find exactly its
entries: a new hit fails, and so does a known hit that is no longer found or whose count changed.
Entries under ``runregistrykit/tests/`` are the tests' to remove, the rest the package modules'.
The file is data and not a constant here because this module is scanned too. It holds no entry for
this module, and the words this module's own tests use are read from the vocabulary file at run
time, never written here.

No Ray is initialised, no store is opened and no client is read.
"""

import ast
import io
import json
import re
import subprocess
import sys
import tokenize
import unittest
from collections import Counter
from pathlib import Path

from datastorekit import contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = ("runregistrykit", "tests")

# the three clients' vocabulary, measured read-only (docs/extraction/measure_client_vocabulary.py)
VOCABULARY = Path(__file__).resolve().parent / "data" / "client_vocabulary.json"

# the hits the package and its tests are known to hold, by scan, written by running the scans
KNOWN_HITS = Path(__file__).resolve().parent / "data" / "known_hits.json"

# the five package modules; every other file the guard scans is a test
PACKAGE_MODULES = (
    "runregistrykit/__init__.py",
    "runregistrykit/__main__.py",
    "runregistrykit/client.py",
    "runregistrykit/fingerprint.py",
    "runregistrykit/stores.py",
)


def package_files() -> list:
    """Every ``*.py`` under ``runregistrykit/``, tests included, relative to the top of this
    repository, sorted."""
    found = set()
    for path in (REPO_ROOT / "runregistrykit").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        found.add(path.relative_to(REPO_ROOT).as_posix())
    return sorted(found)


def is_test(rel: str) -> bool:
    return Path(rel).parts[:2] == TESTS_DIR


# ------------------------------------------------------------------------------------------------
# the vocabulary the package and its tests may not use
# ------------------------------------------------------------------------------------------------

# the package's own words, each of which is also a registry key or a column of a client, and so
# would be flagged; each is allowed for a stated reason. They are the string values that the
# contract of the datastore layer defines for its version and tag tables, read from it at run
# time, so that a word added to the contract later is not allowed silently
PACKAGE_WORDS = {
    # the version table, which every client's registry holds under this key
    contract.VERSION_TABLE,
    # the label column of the version table and of the tag table: one word, defined twice
    contract.VERSION_LABEL,
    contract.TAG_LABEL,
    # the tag table
    contract.TAG_TABLE,
    # the serial column of the tag table
    contract.TAG_SERIAL,
}

# packages of a client that are English words, or a third party's: not a project's
NOT_PROJECT_PACKAGES = {"config", "tools", "thirdparty", "plotting"}

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:[.-][A-Za-z0-9_]+)*")

# the citation pattern, from parts, so that this module's own text holds no citation: a path under
# a directory of campaign prompts; the word for a prompt and two digits; a section sign and a digit
_DIRECTORY = "prompts"
_PROMPT = "prompts?"
_SECTION_SIGN = "\N{SECTION SIGN}"
CITATION = re.compile(
    r"|".join(
        (
            r"\b" + _DIRECTORY + "/",
            r"\b" + _PROMPT + r" \d\d",
            _SECTION_SIGN + r" ?\d",
        )
    )
)


def _vocabulary() -> dict:
    return json.loads(VOCABULARY.read_text())


def _clients() -> dict:
    """The measured vocabulary, per client, read from ``VOCABULARY``."""
    return _vocabulary()["clients"]


def _listed() -> set:
    return {w for group in _vocabulary()["listed"].values() for w in group["words"]}


def registry_words() -> set:
    """The registries' keys of the three clients, less the package's own words."""
    return {
        name for c in _clients().values() for name in c["registry"]["keys"]
    } - PACKAGE_WORDS


def identifier_columns() -> set:
    """The identifier columns of the three clients, less the package's own words.

    A column is an identifier if it has an underscore, or a capital and more than one character.
    A plain-word column cannot be told from English, and a one-letter column cannot either.
    """
    return {
        name
        for c in _clients().values()
        for name in c["columns"]["names"]
        if "_" in name or (name.lower() != name and len(name) > 1)
    } - PACKAGE_WORDS


def project_packages() -> set:
    """The clients' top-level packages, less the ones that are not a project's."""
    return {
        name
        for c in _clients().values()
        for name in c["packages"]
        if name not in NOT_PROJECT_PACKAGES
    } - PACKAGE_WORDS


def campaigns() -> set:
    return {
        name for c in _clients().values() for name in c["campaigns"]["names"]
    } - PACKAGE_WORDS


def forbidden_words() -> set:
    return (
        registry_words()
        | identifier_columns()
        | project_packages()
        | campaigns()
        | (_listed() - PACKAGE_WORDS)
    )


# ------------------------------------------------------------------------------------------------
# the imports that may be made
# ------------------------------------------------------------------------------------------------

_PACKAGE_ROOTS = set(sys.stdlib_module_names) | {"runregistrykit"}

# the store layer and the fingerprinter, the two package modules that may import the datastore
# layer, and then only inside a function, so that importing the package stays light
_DATASTORE_MODULES = ("runregistrykit/stores.py", "runregistrykit/fingerprint.py")

_TEST_ROOTS = _PACKAGE_ROOTS | {"datastorekit", "sqlalchemy", "ray"}


def import_allowed(module: str, rel: str, in_function: bool) -> bool:
    """Whether the file ``rel`` may import ``module``; ``in_function`` is whether the import
    statement is inside a function body."""
    root = module.split(".")[0]
    if is_test(rel):
        return root in _TEST_ROOTS
    if root in _PACKAGE_ROOTS:
        return True
    return root == "datastorekit" and in_function and rel in _DATASTORE_MODULES


# ------------------------------------------------------------------------------------------------
# the scans: each returns (file, line, word), in order
# ------------------------------------------------------------------------------------------------


def _candidates(word: str) -> list:
    """A word of a string or comment, whole, by its dot-separated parts and, when it has a hyphen,
    by its hyphen-separated parts."""
    found = [word, *word.split(".")]
    if "-" in word:
        found += word.split("-")
    return found


def _text_hits(text: str, forbidden: set) -> list:
    """(line offset in ``text``, word) of every forbidden word."""
    hits = []
    for m in _WORD.finditer(text):
        for candidate in _candidates(m.group(0)):
            if candidate in forbidden:
                hits.append((m.start(), candidate))
    return [(text.count("\n", 0, at), w) for at, w in hits]


def _citation_hits(text: str) -> list:
    return [
        (text.count("\n", 0, m.start()), m.group(0)) for m in CITATION.finditer(text)
    ]


def _strings(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            yield node.lineno, node.value


def _comments(source: str):
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            yield token.start[0], token.string


def _code_names(node) -> list:
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        return [node.attr]
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return [node.name]
    if isinstance(node, ast.arg):
        return [node.arg]
    if isinstance(node, ast.keyword) and node.arg is not None:
        return [node.arg]
    if isinstance(node, ast.alias):
        return [n for n in (node.name.split(".")[-1], node.asname) if n]
    return []


def scan_code_names(rel: str, source: str, tree, forbidden: set) -> list:
    found = set()
    for node in ast.walk(tree):
        for name in _code_names(node):
            if {name, *name.split("_")} & forbidden:
                found.add((node.lineno, name))
    return [(rel, line, name) for line, name in sorted(found)]


def scan_strings(rel: str, source: str, tree, forbidden: set) -> list:
    found = set()
    for lineno, text in _strings(tree):
        # the line within a multi-line string is exact for a docstring, approximate for a
        # string with escaped or joined lines
        found |= {(lineno + off, w) for off, w in _text_hits(text, forbidden)}
    return [(rel, line, w) for line, w in sorted(found)]


def scan_comments(rel: str, source: str, tree, forbidden: set) -> list:
    found = set()
    for lineno, text in _comments(source):
        found |= {(lineno + off, w) for off, w in _text_hits(text, forbidden)}
    return [(rel, line, w) for line, w in sorted(found)]


def scan_citations(rel: str, source: str, tree, forbidden: set) -> list:
    found = set()
    for lineno, text in [*_strings(tree), *_comments(source)]:
        found |= {(lineno + off, w) for off, w in _citation_hits(text)}
    return [(rel, line, w) for line, w in sorted(found)]


def _absolute(rel: str, node: ast.ImportFrom) -> str:
    """The module a ``from`` import names, with a relative import resolved against ``rel``."""
    if not node.level:
        return node.module
    package = Path(rel).parent.parts
    base = package[: len(package) - (node.level - 1)]
    return ".".join(base + ((node.module,) if node.module else ()))


def _imports(rel: str, node, in_function: bool):
    """Every import statement under ``node``: (line, module, inside a function)."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Import):
            for alias in child.names:
                yield child.lineno, alias.name, in_function
        elif isinstance(child, ast.ImportFrom):
            yield child.lineno, _absolute(rel, child), in_function
        else:
            inside = in_function or isinstance(
                child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
            )
            yield from _imports(rel, child, inside)


def scan_imports(rel: str, source: str, tree, forbidden: set) -> list:
    return [
        (rel, line, module)
        for line, module, in_function in _imports(rel, tree, False)
        if not import_allowed(module, rel, in_function)
    ]


# the scanning tests' names, and what each calls
SCANS = {
    "test_no_code_name": scan_code_names,
    "test_no_string_or_docstring": scan_strings,
    "test_no_comment": scan_comments,
    "test_no_citation": scan_citations,
    "test_every_import_is_allowed": scan_imports,
}


def scan_all(files=None, forbidden=None) -> dict:
    """Every scan's hits over ``files`` (all of them by default), by the scanning test's name."""
    files = package_files() if files is None else files
    forbidden = forbidden_words() if forbidden is None else forbidden
    sources = {rel: (REPO_ROOT / rel).read_text() for rel in files}
    trees = {rel: ast.parse(src) for rel, src in sources.items()}
    return {
        name: [
            hit
            for rel in files
            for hit in scan(rel, sources[rel], trees[rel], forbidden)
        ]
        for name, scan in SCANS.items()
    }


def count_hits(hits: list) -> list:
    """``[file, word, count]`` entries, sorted, of a scan's hits."""
    counted = Counter((rel, word) for rel, _, word in hits)
    return [[rel, word, n] for (rel, word), n in sorted(counted.items())]


def problems(known: list, hits: list) -> list:
    """What differs between a scan's known entries and its hits, in words; empty when equal."""
    counted = {(rel, word): n for rel, word, n in count_hits(hits)}
    expected = {(rel, word): n for rel, word, n in known}
    out = []
    for rel, line, word in hits:
        if counted[(rel, word)] > expected.get((rel, word), 0):
            out.append(f"not known: {rel}:{line} {word}")
    for (rel, word), n in sorted(expected.items()):
        if counted.get((rel, word), 0) < n:
            out.append(
                f"known but found {counted.get((rel, word), 0)} time(s), not {n}: "
                f"{rel} {word}"
            )
    return out


def _known() -> dict:
    return json.loads(KNOWN_HITS.read_text())


class _GuardTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = package_files()
        cls.forbidden = forbidden_words()
        cls.hits = scan_all(cls.files, cls.forbidden)

    def assertKnownHits(self):
        # exactly the known hits of the calling test, in both directions
        name = self._testMethodName
        known = _known()["known hits"][name]
        self.assertEqual([], problems(known, self.hits[name]), name)
        self.assertEqual(known, count_hits(self.hits[name]))


class TestTheFiles(unittest.TestCase):
    def test_the_derived_files_hold_every_tracked_python_file(self):
        listed = subprocess.run(
            ["git", "ls-files", "runregistrykit"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
        tracked = {path for path in listed if path.endswith(".py")}
        self.assertTrue(tracked)
        self.assertLessEqual(tracked, set(package_files()))

    def test_the_tests_and_this_module_are_scanned(self):
        files = package_files()
        self.assertTrue(set(PACKAGE_MODULES) <= set(files))
        self.assertIn(Path(__file__).relative_to(REPO_ROOT).as_posix(), files)
        self.assertTrue(any(is_test(rel) for rel in files))
        self.assertFalse(any("__pycache__" in rel for rel in files))
        self.assertEqual(sorted(files), files)


class TestTheVocabulary(unittest.TestCase):
    def test_every_part_holds_the_words_the_file_summarises(self):
        data = _vocabulary()
        read = data["summary"]["read, before any rule of the guard"]
        clients = data["clients"]
        self.assertEqual(3, len(clients))
        # each part, before any rule, is the size the file's own summary gives
        parts = {
            "registry keys, all clients": set().union(
                *(c["registry"]["keys"] for c in clients.values())
            ),
            "column names, all clients": set().union(
                *(c["columns"]["names"] for c in clients.values())
            ),
            "packages, all clients": set().union(
                *(c["packages"] for c in clients.values())
            ),
            "campaigns, all clients": set().union(
                *(c["campaigns"]["names"] for c in clients.values())
            ),
        }
        for key, words in parts.items():
            with self.subTest(part=key):
                self.assertTrue(words)
                self.assertEqual(read[key], len(words))
        self.assertEqual(read["listed words"], len(_listed()))
        for name, c in clients.items():
            with self.subTest(client=name):
                counts = data["summary"]["per client"][name]
                self.assertEqual(counts["registry keys"], len(c["registry"]["keys"]))
                self.assertEqual(
                    counts["factory modules"], len(c["columns"]["modules"])
                )
                self.assertEqual(counts["column names"], len(c["columns"]["names"]))
                self.assertEqual(counts["packages"], len(c["packages"]))
                self.assertEqual(counts["campaigns"], len(c["campaigns"]["names"]))
                self.assertEqual(40, len(c["commit"]))

    def test_the_words_of_each_kind_are_forbidden(self):
        # a vocabulary that came out empty would pass every scan
        forbidden = forbidden_words()
        for name, c in _clients().items():
            with self.subTest(client=name):
                keys = [k for k in c["registry"]["keys"] if k not in PACKAGE_WORDS]
                self.assertIn(keys[0], registry_words())
                columns = [
                    k
                    for k in c["columns"]["names"]
                    if "_" in k or (k.lower() != k and len(k) > 1)
                ]
                self.assertIn(columns[0], identifier_columns())
                packages = [p for p in c["packages"] if p not in NOT_PROJECT_PACKAGES]
                self.assertIn(packages[0], project_packages())
                self.assertIn(c["campaigns"]["names"][0], campaigns())
                for word in (
                    keys[0],
                    columns[0],
                    packages[0],
                    c["campaigns"]["names"][0],
                ):
                    self.assertIn(word, forbidden)
        for word in _listed():
            with self.subTest(listed=word):
                self.assertIn(word, forbidden)

    def test_the_package_words_are_the_contracts_and_are_not_forbidden(self):
        self.assertEqual(
            5, len(PACKAGE_WORDS) + 1
        )  # the label column is one word, twice
        self.assertEqual(
            {
                contract.VERSION_TABLE,
                contract.VERSION_LABEL,
                contract.TAG_LABEL,
                contract.TAG_TABLE,
                contract.TAG_SERIAL,
            },
            PACKAGE_WORDS,
        )
        self.assertFalse(PACKAGE_WORDS & forbidden_words())
        # and they are the clients' words as well: without the rule they would be flagged
        measured = {k for c in _clients().values() for k in c["registry"]["keys"]}
        self.assertTrue(PACKAGE_WORDS & measured)

    def test_the_words_that_are_not_a_projects_are_not_forbidden(self):
        packages = {p for c in _clients().values() for p in c["packages"]}
        self.assertTrue(NOT_PROJECT_PACKAGES <= packages)
        self.assertFalse(NOT_PROJECT_PACKAGES & project_packages())


class TestTheRules(unittest.TestCase):
    """Each rule finds what it says, and no more, on source built from the vocabulary."""

    @classmethod
    def setUpClass(cls):
        cls.forbidden = forbidden_words()
        c = next(iter(_clients().values()))
        cls.package = sorted(project_packages())[0]
        cls.other = sorted(project_packages())[1]
        cls.hyphenated = sorted(
            w
            for w in _listed()
            if "-" in w and sum(part in cls.forbidden for part in w.split("-")) > 1
        )[0]
        cls.plain = sorted(
            w
            for w in cls.forbidden
            if w.isalpha() and w.swapcase() not in cls.forbidden
        )[0]

    def scan(self, scanner, source):
        return [
            w for _, _, w in scanner("x.py", source, ast.parse(source), self.forbidden)
        ]

    def test_a_code_name_is_checked_whole_and_split_on_the_underscore(self):
        w = self.plain
        for source in (
            f"{w} = 1",
            f"x.{w}",
            f"def {w}(): pass",
            f"class {w}: pass",
            f"def g({w}): pass",
            f"g({w}=1)",
            f"import os as {w}",
            f"from os import path as {w}",
            f"from os import {w}",
        ):
            with self.subTest(source=source):
                self.assertEqual([w], self.scan(scan_code_names, source))
        self.assertEqual([f"{w}_more"], self.scan(scan_code_names, f"{w}_more = 1"))
        self.assertEqual(
            [f"more_{w}_more"], self.scan(scan_code_names, f"more_{w}_more = 1")
        )
        self.assertEqual([], self.scan(scan_code_names, f"{w}more = 1"))
        self.assertEqual([], self.scan(scan_code_names, f"more{w} = 1"))
        # case-sensitive
        self.assertEqual([], self.scan(scan_code_names, f"{w.swapcase()} = 1"))
        # a string is not a code name
        self.assertEqual([], self.scan(scan_code_names, f"x = '{w}'"))

    def test_a_word_of_a_string_is_whole_or_a_dot_part_or_a_hyphen_part(self):
        w = self.plain
        self.assertEqual([w], self.scan(scan_strings, f"x = 'a {w} b'"))
        self.assertEqual([w], self.scan(scan_strings, f'"""\n{w}\n"""'))
        self.assertEqual([w], self.scan(scan_strings, f"x = f'{{y}} {w}'"))
        self.assertEqual([w], self.scan(scan_strings, f"x = 'docs/{w}/x.py'"))
        self.assertEqual([w], self.scan(scan_strings, f"x = '{w}.suffix'"))
        self.assertEqual([w], self.scan(scan_strings, f"x = 'prefix.{w}'"))
        self.assertEqual([w], self.scan(scan_strings, f"x = '{w}-after'"))
        self.assertEqual([w], self.scan(scan_strings, f"x = 'before-{w}'"))
        self.assertEqual([], self.scan(scan_strings, f"x = '{w}after'"))
        self.assertEqual([], self.scan(scan_strings, f"x = 'before{w}'"))
        self.assertEqual([], self.scan(scan_strings, f"x = '{w}_after'"))
        self.assertEqual([], self.scan(scan_strings, f"x = '{w.swapcase()}'"))
        # a name is not a string, and a comment is not a string
        self.assertEqual([], self.scan(scan_strings, f"{w} = 1"))
        self.assertEqual([], self.scan(scan_strings, f"x = 1  # {w}"))

    def test_a_hyphenated_word_finds_itself_and_each_forbidden_part(self):
        word = self.hyphenated
        expected = [word] + [p for p in word.split("-") if p in self.forbidden]
        found = self.scan(scan_strings, f"x = '{word}'")
        self.assertEqual(sorted(set(expected)), sorted(found))
        self.assertIn(word, found)
        self.assertGreater(len(found), 1)

    def test_a_comment_is_checked_as_a_string_is(self):
        w = self.plain
        self.assertEqual([w], self.scan(scan_comments, f"x = 1  # a {w} b"))
        self.assertEqual([w], self.scan(scan_comments, f"# {w}.suffix"))
        self.assertEqual([], self.scan(scan_comments, f"# {w}after"))
        self.assertEqual([], self.scan(scan_comments, f"x = '{w}'"))
        self.assertEqual([], self.scan(scan_comments, f"{w} = 1"))

    def test_a_citation_is_a_path_a_numbered_prompt_or_a_section(self):
        directory, prompt, section = "prompts", "prompt", "\N{SECTION SIGN}"
        digits = "".join(("0", "7"))
        for text in (
            f"{directory}/x/y.md",
            f".{directory}/x",
            f"{prompt} {digits}",
            f"{directory} {digits}",
            f"{section}{digits[1]}",
            f"{section} {digits[1]}",
        ):
            for source in (f"x = '{text}'", f"x = 1  # {text}"):
                with self.subTest(source=source):
                    self.assertEqual(1, len(self.scan(scan_citations, source)), source)
        for text in (
            f"a {prompt} is a thing",
            f"the {prompt} {digits[1]}",
            f"{directory}",
            f"{section}",
            f"{section} x",
            f"x{directory}/y",
            f"{prompt}{digits}",
        ):
            for source in (f"x = '{text}'", f"x = 1  # {text}"):
                with self.subTest(source=source):
                    self.assertEqual([], self.scan(scan_citations, source), source)
        # a name is not a citation
        self.assertEqual([], self.scan(scan_citations, f"{directory} = 1"))

    def test_a_hit_is_reported_with_its_line(self):
        w = self.plain
        found = scan_strings(
            "x.py", f"a = 1\nb = '{w}'\n", ast.parse(f"a = 1\nb = '{w}'\n"), {w}
        )
        self.assertEqual([("x.py", 2, w)], found)

    def test_counting_and_comparing_the_hits(self):
        hits = [("a.py", 3, "w"), ("a.py", 9, "w"), ("b.py", 1, "v")]
        counted = count_hits(hits)
        self.assertEqual([["a.py", "w", 2], ["b.py", "v", 1]], counted)
        self.assertEqual([], problems(counted, hits))
        # a new hit, a changed count and a known hit no longer found each fail
        self.assertTrue(problems(counted, hits + [("c.py", 1, "u")]))
        self.assertTrue(problems(counted, hits + [("a.py", 12, "w")]))
        self.assertTrue(problems(counted, hits[:1] + hits[2:]))
        self.assertTrue(problems(counted, hits[:2]))
        self.assertTrue(problems([], hits))
        self.assertEqual(
            ["not known: c.py:1 u"], problems(counted, hits + [("c.py", 1, "u")])
        )


class TestTheKnownHits(unittest.TestCase):
    def test_the_file_is_in_form(self):
        data = _known()
        self.assertEqual({"owners", "known hits"}, set(data))
        self.assertEqual(set(SCANS), set(data["known hits"]))
        files = set(package_files())
        for name, entries in data["known hits"].items():
            with self.subTest(scan=name):
                self.assertEqual(sorted(entries), entries)
                for rel, word, n in entries:
                    self.assertIn(rel, files)
                    self.assertIsInstance(word, str)
                    self.assertIsInstance(n, int)
                    self.assertGreater(n, 0)
                self.assertEqual(
                    len(entries), len({(rel, word) for rel, word, _ in entries})
                )

    def test_this_module_holds_no_known_hit(self):
        # the guard scans itself, and was written to be clean: no entry may be added for it
        me = Path(__file__).relative_to(REPO_ROOT).as_posix()
        for name, entries in _known()["known hits"].items():
            with self.subTest(scan=name):
                self.assertEqual([], [e for e in entries if e[0] == me])
        scanned = scan_all([me])
        for name, hits in scanned.items():
            with self.subTest(scan=name):
                self.assertEqual([], hits)


class TestThePackageNamesNoClient(_GuardTestCase):
    def test_no_code_name(self):
        self.assertKnownHits()

    def test_no_string_or_docstring(self):
        self.assertKnownHits()

    def test_no_comment(self):
        self.assertKnownHits()

    def test_no_citation(self):
        self.assertKnownHits()


class TestThePackageImportsNoClient(_GuardTestCase):
    def test_every_import_is_allowed(self):
        self.assertKnownHits()

    def test_the_allow_list(self):
        # an allow-list that grew silently would pass every scan above
        stores, fingerprint, client, init, main = (
            "runregistrykit/stores.py",
            "runregistrykit/fingerprint.py",
            "runregistrykit/client.py",
            "runregistrykit/__init__.py",
            "runregistrykit/__main__.py",
        )
        a_test = "runregistrykit/tests/test_anything.py"
        for module in (
            "os",
            "sys.path",
            "tomllib",
            "runregistrykit",
            "runregistrykit.stores",
        ):
            for rel in (stores, fingerprint, client, init, main, a_test):
                for in_function in (False, True):
                    with self.subTest(module=module, rel=rel, in_function=in_function):
                        self.assertTrue(import_allowed(module, rel, in_function))
        # datastorekit: in a package module only inside a function of the two that may
        for module in ("datastorekit", "datastorekit.SQL.ShardedPool"):
            self.assertFalse(import_allowed(module, stores, False), module)
            self.assertTrue(import_allowed(module, stores, True), module)
            self.assertFalse(import_allowed(module, fingerprint, False), module)
            self.assertTrue(import_allowed(module, fingerprint, True), module)
            for rel in (client, init, main):
                for in_function in (False, True):
                    self.assertFalse(import_allowed(module, rel, in_function), rel)
            # anywhere in a test
            for in_function in (False, True):
                self.assertTrue(import_allowed(module, a_test, in_function))
        # sqlalchemy and ray: allowed in a test, refused in a package module
        for module in ("sqlalchemy", "sqlalchemy.exc", "ray", "ray.util"):
            for in_function in (False, True):
                self.assertTrue(import_allowed(module, a_test, in_function), module)
                for rel in (stores, fingerprint, client, init, main):
                    self.assertFalse(import_allowed(module, rel, in_function), module)
        # a third party is refused everywhere
        for rel in (stores, fingerprint, client, init, main, a_test):
            for in_function in (False, True):
                self.assertFalse(import_allowed("numpy", rel, in_function))
                self.assertFalse(import_allowed("numpy.linalg", rel, in_function))
        # a package of each client, with and without a submodule, is refused everywhere
        for name in sorted(project_packages()):
            for module in (name, f"{name}.submodule"):
                for rel in (stores, fingerprint, client, init, main, a_test):
                    for in_function in (False, True):
                        with self.subTest(module=module, rel=rel):
                            self.assertFalse(import_allowed(module, rel, in_function))

    def test_the_scan_sees_where_an_import_is(self):
        source = (
            "import os\n"
            "def f():\n"
            "    import datastorekit\n"
            "    from . import x\n"
            "class C:\n"
            "    import numpy\n"
            "    def g(self):\n"
            "        import numpy as np\n"
            "from datastorekit import y\n"
        )
        rel = "runregistrykit/stores.py"
        found = scan_imports(rel, source, ast.parse(source), set())
        self.assertEqual(
            [(rel, 6, "numpy"), (rel, 8, "numpy"), (rel, 9, "datastorekit")], found
        )


if __name__ == "__main__":
    unittest.main()
