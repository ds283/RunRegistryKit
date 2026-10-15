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

"""The client's fingerprinter: the protocol the store layer calls, a ready-made one over
DatastoreKit, and the loader that finds the one a client's config names.

**Who does what.** What goes into a store's fingerprint is the client's: its factories' inventory
specs, its registry and its format number. How the content is encoded and digested is
DatastoreKit's (`datastorekit.store_fingerprint`). When a fingerprint is taken and where it is
recorded is this package's (`runregistrykit.stores.fingerprint_store`). The package is handed a
`Fingerprinter` and treats what it returns as opaque, apart from a fingerprint's
`fingerprint_format`, `encoding_format` (when present), `digest` and `taken`, and each comparison
entry's `kind` and `text`.

**The protocol** (`Fingerprinter`):

    take(primary, taken)        reads the closed store ``primary`` read-only, with no Ray, and
                                returns ``(fingerprint, inventory)``: the fingerprint, a JSON object
                                holding at least an integer `fingerprint_format`, a 64-hex
                                `digest` and `taken` as given; and whatever `listing` needs. A
                                refusal of the read comes through unwrapped, its own type and text
    compare(recorded, current)  a list of entries, each a dict with at least `kind` (a string) and
                                `text` (one line a person reads); empty when the two describe the
                                same content
    describe(fingerprint)       the lines `store fingerprint` prints after its own `digest:` and
                                `format:` lines
    listing(inventory, fp)      the lines of a listing file, without newlines

**The ready-made one**, `DatastoreKitFingerprinter(factories, fingerprint_format)`, implements it
over DatastoreKit's `read_inventory`, `fingerprint_of`, `compare_fingerprints` and
`listing_lines`. A client instantiates it in a module of its own, with its registry (a mapping of
names to factory classes or instances) and its format number, and names that object in its config.

**Naming it.** A client's `runregistrykit.toml` names its fingerprinter as

    [stores]
    fingerprinter = "module:attribute"

a dotted module path, one colon and a dotted attribute path (`runregistrykit.client` checks the
form when it reads the file). `load_fingerprinter` puts the directory whose config governs
(`ClientRoot.found`) first on `sys.path` if it is not already there, as running a script from the
client's root does, and leaves it there; imports the module; resolves the attribute; and checks
that the object is a `Fingerprinter` and not a class (a class with the four methods passes the
protocol's check; the config names an instance). `require_fingerprinter` checks only that the
config names one, and imports nothing: every store operation makes that check before it reads,
writes or deletes anything (no degraded mode without one), and only what takes, compares,
describes or lists a fingerprint imports it.

This module imports only the standard library and the package at module scope; DatastoreKit is
imported inside `DatastoreKitFingerprinter`'s methods, so that importing it loads none of `ray`,
`sqlalchemy` or `datastorekit`.
"""

import importlib
import sys
from pathlib import Path
from typing import Any, Iterable, List, Protocol, Tuple, runtime_checkable

from .client import ConfigError

__all__ = [
    "DatastoreKitFingerprinter",
    "Fingerprinter",
    "load_fingerprinter",
    "require_fingerprinter",
]


@runtime_checkable
class Fingerprinter(Protocol):
    """What the store layer calls to take, compare, describe and list a store's fingerprint (the
    module docstring)."""

    def take(self, primary: Path, taken: dict) -> Tuple[dict, Any]: ...

    def compare(self, recorded: dict, current: dict) -> List[dict]: ...

    def describe(self, fingerprint: dict) -> List[str]: ...

    def listing(self, inventory: Any, fingerprint: dict) -> Iterable[str]: ...


def _short(digest) -> str:
    return str(digest)[:12]


class DatastoreKitFingerprinter:
    """A `Fingerprinter` over DatastoreKit's functions, for the registry ``factories`` (any
    mapping `read_inventory` accepts) at the client's ``fingerprint_format``, an `int` of at least
    1. The format is refused here as `fingerprint_of` refuses it: a `bool` or anything that is not
    an `int` with `TypeError`, an `int` below 1 with `ValueError`."""

    def __init__(self, factories, fingerprint_format: int):
        if isinstance(fingerprint_format, bool) or not isinstance(
            fingerprint_format, int
        ):
            raise TypeError(
                f"DatastoreKitFingerprinter(): fingerprint_format must be an int, not "
                f"{type(fingerprint_format).__name__} {fingerprint_format!r}"
            )
        if fingerprint_format < 1:
            raise ValueError(
                f"DatastoreKitFingerprinter(): fingerprint_format must be at least 1, not "
                f"{fingerprint_format!r}"
            )
        self.factories = factories
        self.fingerprint_format = fingerprint_format

    def take(self, primary, taken):
        """`read_inventory(primary, factories)`, then `fingerprint_of(inventory,
        fingerprint_format, taken)`. A refusal of the read comes through as the reader raised it.
        """
        from datastorekit.store_fingerprint import fingerprint_of
        from datastorekit.store_inventory import read_inventory

        inventory = read_inventory(primary, self.factories)
        return fingerprint_of(inventory, self.fingerprint_format, taken), inventory

    def compare(self, recorded, current):
        from datastorekit.store_fingerprint import compare_fingerprints

        return compare_fingerprints(recorded, current)

    def describe(self, fingerprint):
        """Each class's count and digest, then each of its tag sets', and the problems counted."""
        lines = ["classes:  (count, digest; then each tag set)"]
        width = max((len(name) for name in fingerprint["classes"]), default=0)
        for name, entry in fingerprint["classes"].items():
            lines.append(
                f"  {name:{width}} {entry['count']:>8}  {_short(entry['digest'])}"
            )
            for tag_set in entry["tag_sets"]:
                lines.append(
                    f"  {'':{width}} {tag_set['count']:>8}  {_short(tag_set['digest'])}  "
                    f"[{', '.join(tag_set['tags'])}]"
                )
        if fingerprint["problems"]:
            lines.append(
                "problems: (counts only; the store's own text is in `main.py --inventory`)"
            )
            for name, kinds in fingerprint["problems"].items():
                counted = ", ".join(f"{kind} {n}" for kind, n in kinds.items())
                lines.append(f"  !! {name}: {counted}")
        else:
            lines.append("problems: none")
        return lines

    def listing(self, inventory, fingerprint):
        from datastorekit.store_fingerprint import listing_lines

        return listing_lines(inventory, fingerprint)


def require_fingerprinter(client) -> str:
    """The `[stores] fingerprinter` the config of ``client`` (a `ClientRoot`) names, as written.
    Reads the config only, and imports nothing. None named is a `ConfigError` naming the config
    file and saying what to add: the store layer has no mode without a fingerprinter."""
    spec = client.stores.get("fingerprinter")
    if spec is None:
        raise ConfigError(
            f"{client.config_file} names no fingerprinter, and the store layer requires one. Add "
            f'[stores] with fingerprinter = "module:attribute", naming the client\'s '
            f"Fingerprinter (runregistrykit.fingerprint), such as a DatastoreKitFingerprinter of "
            f"its registry and its format number"
        )
    return spec


def load_fingerprinter(client) -> Fingerprinter:
    """The fingerprinter the config of ``client`` (a `ClientRoot`) names, imported (the module
    docstring). Every refusal is a `ConfigError` naming the config file and the spec: none named;
    an import that fails, with the exception's type and text; a missing attribute; an object that
    is not a `Fingerprinter`."""
    spec = require_fingerprinter(client)
    module_name, _, attribute = spec.partition(":")
    where = f"{client.config_file}: [stores] fingerprinter {spec!r}"

    # the tree that is running, first, as a script run from the root has it; left there
    if client.found not in sys.path:
        sys.path.insert(0, client.found)
    importlib.invalidate_caches()
    try:
        found = importlib.import_module(module_name)
    except Exception as e:
        raise ConfigError(
            f"{where}: the module {module_name!r} could not be imported "
            f"({type(e).__name__}: {e})"
        ) from e

    for part in attribute.split("."):
        try:
            found = getattr(found, part)
        except AttributeError:
            raise ConfigError(
                f"{where}: {module_name} has no attribute {attribute!r} (no {part!r})"
            ) from None

    # before the protocol check, which a class with the four methods passes
    if isinstance(found, type):
        raise ConfigError(
            f"{where} is the class {found.__qualname__}, not an instance of it: name an "
            f"instance, made in a module of the client's (for DatastoreKitFingerprinter, one "
            f"made with the client's registry and its format number)"
        )
    if not isinstance(found, Fingerprinter):
        raise ConfigError(
            f"{where} is {found!r}, which is not a Fingerprinter: it needs the methods take, "
            f"compare, describe and listing (runregistrykit.fingerprint)"
        )
    return found
