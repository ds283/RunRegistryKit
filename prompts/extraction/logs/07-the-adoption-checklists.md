# Log — prompt 07: the adoption checklists

**Subject:** Write the adoption checklists and correct the README's worktree sentences
**Commit:** `aaab408` (on `main`, after `4c01c78`)
**Date:** 2026-10-15
**Agent:** Claude Opus 5.5, dispatched by the orchestrator with its brief and section 0 of the
orchestration note (`note-07-section0.md`, corrections 1-11)
**Result:** **landed.**
- `docs/adoption/` is new: a README, three checklists (SecondaryGWKit at `14bcac0`, ChamPBH at
  `c21cdfb`, StochasticInstantons at `5fb4a1d`), and `measure_client_registry.py`, whose Markdown
  output is each checklist's appendix.
- `README.md` differs in "Using it" only (U20); `PROVENANCE.md` gains 07's section.
- No file under `runregistrykit/` changed, and the suite is **276 -> 276**.
- **One stop condition fired** (§5's first: calls that do not bind at SGK's commit). It was put to
  the user, who ruled it on 2026-10-15 (below); nothing else fired.
- The script's figures equal the prompt's §0 and the note's, or each difference is explained
  (deviations 5, 13, 16, 17).
- The Q5 sketch runs on public names, and each breakage it names fails. (a)-(e) each fail as §3.8
  says.
- `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]` is closed (U20) and nothing
  is opened, so `docs/OPEN_ISSUES.md` counts **2**.
- **No tag made, nothing pushed.**

**E2** (SGK's gate on this campaign) is `v0.1.0` (tag object `fd5ce48` on `9f8ebe4`) with
`docs/adoption/secondarygwkit.md`, at `aaab408`.

## What shipped

| File | What |
|---|---|
| `docs/adoption/measure_client_registry.py` | new: the measuring script (section 2.1), black-clean, not a test |
| `docs/adoption/README.md` | new: what the three share, §1-§8 as section 2.2, and the ten item names |
| `docs/adoption/secondarygwkit.md` | new: SGK's checklist, ten items and the appendix (E2) |
| `docs/adoption/champbh.md` | new: CPBH's checklist, ten items and the appendix |
| `docs/adoption/stochasticinstantons.md` | new: SI's checklist, ten items and the appendix |
| `README.md` | "Using it": the worktree sentences (U20), three hunks, nothing else |
| `PROVENANCE.md` | 07's section under "Since the import" |
| this log, `IMPLEMENTATION_STATE.md`, `docs/OPEN_ISSUES.md`, `prompts/INDEX.md` | the records |

Not touched: anything under `runregistrykit/`, `docs/extraction/` or `.github/`; `pyproject.toml`,
`CLAUDE.md`, `LICENSE`, `.gitignore`, the campaign README, the prompt, `orchestrator/`. No client,
DatastoreKit or RayPoolKit file.

### The script

`measure_client_registry.py {sgk,cpbh,si} [--commit SHA] [--json]`, and
`path --repository DIR --commit SHA` for a fixture (deviation 11).
- **What it reads.** Each tracked `.py` file at the commit, through `git ls-tree -r` and
  `git show <commit>:<path>`, parsed with `ast`; the non-`.py` files through `git grep` at the commit;
  `git rev-parse` and `git log -1` for the commit. SGK's `RunRegistry/` is read at the commit only for
  the staying tests (`STAYING`). Its frozen tree at `a45aefc` (`BASELINE`) is read for the signatures
  before the move and to check the fate table.
- **How a callee is resolved.** Correction 3: through the names each file's imports bind, with
  Python's scoping near enough (function scopes, enclosing functions, the module, a class body seen
  only from itself), so that `engine.begin()` is not the registry's.
- **The fate table** (`TABLE`, ten rows: one rename, three moves, six deletions) is checked against
  the package before anything is measured. Each name is absent from its module's counterpart; it
  existed at `a45aefc`; each target exists, a rename's in its module's `__all__`; and
  `pyproject.toml` excludes `runregistrykit.tests`, which is what "not shipped" rests on. A failed row
  exits 1 (deviation 14).
- **Bind verdicts** come from `inspect.signature(<v0.1.0's function>).bind`, with `object()`
  placeholders. A call that unpacks `*` or `**` gets `bind_partial` of its spelled arguments
  (deviation 15). A `fingerprint_of` call whose only failure is the missing format carries the
  ruling's reason (deviation 12).
- **The output** is Markdown or JSON, sorted. Exit codes: 0; 1 for a table that disagrees with the
  package; 2 when the client or commit cannot be read; 3 for an unknown name.
- It imports only the standard library, `runregistrykit` (and its `stores` and `__main__`) and
  `datastorekit.store_fingerprint`.

### The README's correction (U20)

`git diff README.md` has three hunks, all in "Using it" (`:67-191` after the change):

```diff
@@ -81,3 +81,3 @@ optional, and an empty file takes every default:
-A relative `runs_root` or `stores_root` is relative to the root (for a run in a linked worktree,
-the main checkout, below); an absolute one is kept as it is. Any other key, or a value of the wrong
-type or shape, is a `ConfigError` that names the file.
+A relative `runs_root` or `stores_root` is relative to the record root (the root, or for a run in a
+linked worktree the main checkout, below); an absolute one is kept as it is. Any other key, or a
+value of the wrong type or shape, is a `ConfigError` that names the file.
@@ -95 +95,6 @@
-in. A worktree of a bare repository is refused. The client's `.gitignore` ignores its runs root.
+in. So two directories are named here, and for a worktree they differ. Records, and the paths in
+them, are under the **record root** (`ClientRoot.root`): the main checkout. The
+`runregistrykit.toml` that governs is the one the walk found, or the one in the directory
+`client_root=` names (`ClientRoot.found`): in the tree that is running, the worktree's own,
+whatever the main checkout holds, and the main checkout need not hold one. A worktree of a bare
+repository is refused. The client's `.gitignore` ignores its runs root.
@@ -149,6 +154,8 @@ fingerprinter = "module:attribute"
-The attribute is an object in a module of the client's own, imported with the client's root first
-on `sys.path`. Usually it is a `DatastoreKitFingerprinter(factories, fingerprint_format)`
-(`runregistrykit.fingerprint`), …
+The attribute is an object in a module of the client's own, imported with the directory whose
+config governs first on `sys.path`: the tree that is running, which for a run in a linked worktree
+is the worktree, not the main checkout. Usually it is a
+`DatastoreKitFingerprinter(factories, fingerprint_format)` (`runregistrykit.fingerprint`), made …
```

The rest of the third hunk is the same paragraph rewrapped, with no word changed.

**Each changed sentence was checked against the code** (`runregistrykit/client.py` and
`fingerprint.py` at `9f8ebe4`, equal to the working tree):
- *A relative root is joined to the record root*: `client.py:34` ("joined to the **record root**"),
  `:264` (`root = _record_root(found)`) and `:269-270` (`_under(root, …)`).
- *The record root is the main checkout; the config that governs is `found`'s, and the main checkout
  need not hold one*: `client.py:52-59` and `:252-262`.
- *The fingerprinter's module is imported with `found` first*: `fingerprint.py:52-54` and `:191-193`.

They were also checked by running, in a scratch repository with a linked worktree whose
`runregistrykit.toml` and fingerprinter module differ from the main checkout's (output below,
"Verification", 6). Correction 8's reading holds: the relative roots stay joined to the record root,
and only the import sentence was wrong.

## Deviations from the prompt

Each classified. Corrections 1-11 are the note's; the ruling is the user's.

1. **The gate's diff** (correction 1): `git diff --stat dca5ead HEAD -- runregistrykit docs
   pyproject.toml PROVENANCE.md CLAUDE.md README.md .github` shows `docs/OPEN_ISSUES.md`, one line,
   U20's owner set to 07 by `f7c1b15`. Everything else in the gate held. **STRUCTURALLY REQUIRED.**
2. **"At `v0.1.0`" through `venv/`'s editable install** (correction 2): `git diff 9f8ebe4 HEAD --
   runregistrykit pyproject.toml` is empty before and after (0 lines), and
   `importlib.metadata.version("runregistrykit")` is `0.1.0`. A `path:line` under `runregistrykit/` is
   at `9f8ebe4`, which equals the working tree. Nothing was installed. **STRUCTURALLY REQUIRED.**
3. **Callees resolved through registry names** (correction 3). The excluded name-alike calls the
   script saw are listed in each appendix ("Not the registry's"):
   - SGK: 26. The six SQLAlchemy `begin()` calls the note names, at
     `ObjectFactories/tests/test_quadsource_parent_key.py:445`,
     `test_wkb_numeric_parent_key.py:983`, `StoreFixtures/real_store_fixtures.py:229, 270, 1159` and
     `docs/datastore-generic-audit/str_e_misfire_probe.py:45`. Nineteen `copy_store` calls in three
     probes, of each probe's own function of that name: `reader_writes_probe.py` 3 (its `:427`),
     `fault_copies.py` 5 (its `:50`), and `readonly_open_probe.py` 11 (`rw.copy_store`, the first
     probe's, loaded as a module). And `package.fingerprint_of` (DatastoreKit's) at
     `fingerprint_both_ways.py:128`.
   - CPBH: 7 and SI: 13, all `<engine>.begin()`.

   Why each is excluded: its callee's base name (`engine`, `pool._engine`, `rw`, `package`,
   `self._engine`) is not bound by a registry import. Nor is a bare `copy_store` that the file
   defines itself (`reader_writes_probe.py:427`, `fault_copies.py:50`).
   **STRUCTURALLY REQUIRED.**
4. **Two more forms of patching** (correction 4). An assignment to an attribute of a registry
   module or alias is reported as `assigned`: `sigterm_handler_probe.py:210`. `patch.object(<x>,
   "<name>")` on an object that is not a module is reported, in a file that imports the registry,
   when `<name>` is a private attribute of SGK's `Run` at `a45aefc` (`_update`,
   `_fingerprint_results`): `test_killed_handler.py:333, 432`, as `RunRegistry.Run._fingerprint_results`,
   "private", present, `(self)` at both. **IMPLEMENTATION CHOICE** (the rule by name).
5. **Campaign records** (correction 5): the script reports **6** files under `prompts/` that import
   the registry and **7** that name it, the seventh
   `prompts/datastore-generic/orchestrator/measure-08/scripts/phaseB_edit_tests.py`. Item 1's count is
   the 6; the appendix's line "Campaign records: 6 … import it, 7 name it" shows both, and SGK's
   checklist, item 4, says which is which. **STRUCTURALLY REQUIRED.**
6. **Polymorphic `Parent.types`** (correction 6). The script reports `Parent(..., types=...)` calls
   (item 8): SGK `BackgroundModel.py:900`, `wavenumber.py:396`; CPBH `ScalarModel.py:234, 239, 250`;
   SI none. The line is the call's first; the note's CPBH lines `:236, 241, 252` are the
   `type_column` keywords inside them. The checklists cite the call ranges, read
   (`:234-238`, `:239-249`, `:250-254`). The sketch converts each mapping key with `json.dumps`, so
   `1` and `"1"` stay apart; the stand-in's keys show it, and its breakage B4 is a key whose type
   changes. The key conversion is an **IMPLEMENTATION CHOICE**; the measurement is **STRUCTURALLY
   REQUIRED**.
7. **The neutral store's nine classes and six specs** (correction 7): the README says "nine classes
   of which six declare a spec, so six digests". **STRUCTURALLY REQUIRED.**
8. **U20 as correction 8**: the relative roots' sentence keeps its meaning and names the record
   root; the worktree paragraph names the two directories once; the import sentence names the tree
   that is running. **STRUCTURALLY REQUIRED.**
9. **`RECORDED_DISTRIBUTIONS`** (correction 9). Each client's `utilities.py:174` is
   `("datastorekit", "raypoolkit")`. SI's checklist (item 3) says that `package_provenance` records
   `None` for a name that is not installed. This was read at `runregistrykit/__init__.py:178-182` and
   run on `no-such-distribution-xyz`, giving `{'no-such-distribution-xyz': None}`. The choice is left
   to SI. **STRUCTURALLY REQUIRED.**
10. **The script under `black` and CI** (correction 10): `black --check runregistrykit docs`, 27 files
    unchanged; not collected by the suite. **STRUCTURALLY REQUIRED.**
11. **The fixture override** (correction 11): the client name `path`, which requires `--repository
    DIR --commit SHA`. `--repository` is refused for `sgk`, `cpbh` and `si` (usage error, exit 2), so
    the three client commands read only their own repository and SGK's `a45aefc`. The rules for
    `path` are the clients' less the staying tests. **IMPLEMENTATION CHOICE.**
12. **The stop, and the user's ruling.** §5's first stop condition fired. At SGK `14bcac0` six
    `fingerprint_of` calls do not bind against `datastorekit.store_fingerprint.fingerprint_of`, each
    "missing a required argument: 'fingerprint_format'":
    - live code: `ObjectFactories/tests/test_quadsource_policy_key.py:413, 416, 419` and
      `docs/runregistry-extraction/fingerprint_both_ways.py:127`;
    - staying tests: `RunRegistry/tests/test_store_fingerprint.py:147, 162` (in `_FullStores`,
      `TestGolden`'s base).

    Nothing was committed. The agent reported them and asked; the ruling, relayed by the
    orchestrator as the user's, 2026-10-15, quoted:

    > Ruling on your STOP, taken by the user on 2026-10-15: your option (a), as you recommended.
    > […] A `fingerprint_of` call whose only binding failure is the missing `fingerprint_format`
    > counts as the documented effect of the move (prompt §0.2, §2.3 item 4). It is not a stop. The
    > script keeps the verdict "does not bind" and adds the reason "(the move's new required
    > `fingerprint_format`)". Any call that fails to bind for any other reason, or any unknown name,
    > is still a stop. […] SGK's checklist lists all six, with the rewrite
    > `fingerprint_of(inventory, FINGERPRINT_FORMAT[, taken])`. It also lists
    > `test_store_fingerprint.py:378`, `fingerprint_of(self.baseline_inventory, taken)`, flagged by
    > hand: it binds, but its positional `taken` now lands on `fingerprint_format`, a silent change of
    > meaning.

    Done as ruled. The script adds the reason (constant `MISSING_FORMAT`), and its summary counts
    "not binding: the move's new `fingerprint_format` only" apart from "not binding for any other
    reason", which is 0 at every client. SGK's checklist, items 4 and 7, lists the six and `:378`.
    **STRUCTURALLY REQUIRED.**
13. **`TestGolden`'s scope, and the prompt's citation of it.** The script walks `TestGolden` and
    `TestDrivers` with their in-module bases (`_FullStores`, `:138`) and the module's other
    statements, skipping only the module's other classes. The prompt's §0.3 cites "`fingerprint_of(inventory)`
    without a format (`TestGolden`, `test_store_fingerprint.py:347-383`)". In that range the one call
    is `:378`, which binds (deviation 12); the calls without the format are `:147` and `:162` in the
    base class. The ruling notes the cite as imprecise. **STRUCTURALLY REQUIRED.**
14. **Exit 1** for a fate table that disagrees with the package, before anything is measured. The
    prompt names 0, 2 and 3; a wrong row is neither an unreadable client nor an unknown name, and
    breakage (a) is its test. **IMPLEMENTATION CHOICE.**
15. **`bind_partial` for a call that unpacks `*` or `**`**: the unpacking may supply what is missing
    (`test_pipeline_adoption.py:74`, whose `**kwargs` carries `purpose`, set at `:72`). The verdict
    says "(its spelled arguments; the unpacking is not expanded)". **IMPLEMENTATION CHOICE.**
16. **The printed commands' lines.** The prompt's §0.1 has `scoped_pipeline_run.py:579`,
    `quadsource_atol_sweep.py:594, 905`. Each command is in a three-line f-string literal, which
    starts at `:578`, `:593`, `:904`, and the command itself is at `:580`, `:595`, `:906` (read). The
    script reports a literal at `ast`'s line (its first) and, for a `-m RunRegistry` command, the
    command's own line. The checklist cites both. The count, 3, is the prompt's.
    **IMPLEMENTATION CHOICE** (what the script reports).
17. **`def inventory_spec` at SGK: 21 in 20 files**, where the note has "22 tracked `def
    inventory_spec`". The 22nd is a string in a campaign record,
    `prompts/datastore-generic/orchestrator/measure-08/scripts/phaseA_edit_factories.py:18`
    (`git grep -c` counts it; the script counts `FunctionDef`s outside the records).
    `ObjectFactories/wavenumber.py` has two, `:126` and `:385`. The campaign README's "21 of 38
    classes" agrees. CPBH 17 in 17, as the note. **STRUCTURALLY REQUIRED** (explained).
18. **The script reports more than §2.1 lists**, each mechanical and sorted:
    - the name-alike calls it does not bind (deviation 3);
    - `requirements.txt`'s pins of `datastorekit`, `raypoolkit`, `runregistrykit`, Ray and SQLAlchemy;
    - the helper's imports besides its calls, so CPBH's `main.py:77` and SI's `main.py:48` are seen;
    - `RECORDED_DISTRIBUTIONS`;
    - the module-level `_factories` as well as `factories`, so SI's registry is named;
    - the `Parent(..., types=...)` calls.

    The baseline signature before the move is read for every client, from SGK's `a45aefc`.
    **IMPLEMENTATION CHOICE.**
19. **The staying tests' calls are bound too**, since §2.1 item 4 does not restrict to live code: 8
    calls, 6 binding (one partially) and the 2 of deviation 12. **STRUCTURALLY REQUIRED.**
20. **SGK's item 4 points at item 7** for the staying tests' helpers and deleted names, which item 7
    lists file by file with U21's **Advice:**. The script showed that of the five helpers only
    `StoreTestCase` is used by a test that stays (`test_quadsource_atol_sweep_prepare.py:61`). The
    other four are imported at `test_store_fingerprint.py:41, 47` for classes this package ported.
    The **Advice:** is therefore to copy `StoreTestCase` with its base `RegistryTestCase`.
    **IMPLEMENTATION CHOICE.**
21. **The Q5 sketch pins a list of `[class, digest]`** in registry order, not one digest, so that a
    failure names the class (SGK's 07 acceptance 2 asks that). The README says a client may pin the
    list's own digest instead. It is 19 lines of code (24 with blanks): "about twenty".
    **IMPLEMENTATION CHOICE.**
22. **SI's Python** was read from `pyvenv.cfg` (`version = 3.13.13`). The note's "MacPorts' 3.13" was
    checked by `--version` of `/opt/local/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`,
    the `pyvenv.cfg`'s `home`, a system interpreter, not SI's venv: `Python 3.13.16`.
    **IMPLEMENTATION CHOICE.**
23. **`git worktree list` on the clients.** The agent's first state check ran `git -C <client>
    worktree list`, which is read-only but not among the commands the note allows (it names
    `worktree` among those never to run there). It changed nothing: each client's `HEAD`, `status
    --porcelain` hash and stash count are the same before and after (Verification, 2). The
    orchestrator's message calls it harmless. It was not run again. **UNINTENDED DRIFT.**
24. **One temporary directory outside the scratchpad.** A package check (Verification, 7) used
    `tempfile.mkdtemp()`, which made a directory holding one empty `runregistrykit.toml` under the
    system temporary directory (`/var/folders/…/T/tmpc31kdc05`), not under `agent-07/`. It was
    removed at once (its listing showed the one empty file). And at the final check of the clients,
    a stray redirection wrote the first-state listing (the clients' `HEAD`s and status hashes, no
    client content) to `/tmp/x`; it was removed at once. Nothing else was written outside the
    scratchpad and the repository. **UNINTENDED DRIFT.**
25. **A shell form refused.** A first replay of (a)-(e) as one `bash -c '…'` script was refused by a
    safety check that could not parse it. The same steps were then run one breakage at a time, each
    `git apply` step in `bash -c "…"`, the rest in the tool's shell; nothing in them removes a file.
    **IMPLEMENTATION CHOICE.**

## Verification performed

### 1. The suite

- Before, at `4c01c78`, clean tree: `Ran 276 tests in 85.241s`, `OK`.
- After, with this commit's changes in the tree: `Ran 276 tests in 85.730s`, `OK`.

Both runs were `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, in the
foreground, with the output to a scratch file and the verdict grepped from it. **276 -> 276.**
`black --check runregistrykit docs`: 27 files would be left unchanged (26 and the script).
`git status --short --ignored` after, but for this commit's files: `prompts/.DS_Store`,
`runregistrykit.egg-info/`, `runregistrykit/__pycache__/`, `runregistrykit/tests/__pycache__/`,
`venv/`, as before. No `var/`. This checkout is the only worktree. No Ray process (`pgrep -x raylet`
and `pgrep -f gcs_server`: none); `RAY_ADDRESS` unset.

### 2. The clients, untouched (§3.4)

`git -C <client> rev-parse HEAD`, `status --porcelain | wc -l`, `status --porcelain | shasum`,
`stash list | wc -l`, before (at dispatch) and after (at the end, before committing):

| Repository | `HEAD` | Status lines | `shasum` | Stash | Before = after |
|---|---|---|---|---|---|
| `SecondaryGWKit` | `14bcac0eb73069131f8ce4f55d91e5fc3e7318cf` (`handover-remedial`) | 0 | `da39a3ee5e6b…` | 0 | yes |
| `ChamPBH` | `c21cdfb5613a3ed976a91a95431495dc8bfd49c8` (`main`) | 22 | `fbd525ec2b83…` | 0 | yes |
| `StochasticInstantons` | `5fb4a1d71a016f1b23393923b9a3d59972415aa0` (`dk-and-rpk-migration`) | 0 | `da39a3ee5e6b…` | 0 | yes |
| `DatastoreKit` | `b01737f139e5d8785ff915a929b9bd1b384ec840` | 0 | `da39a3ee5e6b…` | 0 | yes |
| `RayPoolKit` | `17029d99bb2635ff7ce9b99b11e9c5f77d8b6967` | 0 | `da39a3ee5e6b…` | 0 | yes |

SGK: `git ls-tree -r 14bcac0 -- RunRegistry/` and `a45aefc`'s are equal, 25 rows (blob for blob,
compared). `git diff a45aefc 14bcac0 -- RunRegistry StoreFixtures` is empty. CPBH's 22 uncommitted
changes were not read. Each client's `venv/` was used only to read `pyvenv.cfg` with `cat`: SGK
`version = 3.12.15`, CPBH `version = 3.13.16`, SI `version = 3.13.13`.

### 3. The script (§3.2)

- Each client run twice at its commit: **byte-identical** (`cmp`), exit 0. SHA-256 of the Markdown:
  SGK `49e23b44685c4033…` (399 lines), CPBH `0e5660b6e1793015…` (84), SI `0a58ddb89c431d13…` (90).
- `--json`: exit 0; `json.loads` parses each, 21 top-level keys. Two `--json` runs are
  byte-identical for each client.
- `--commit 0000000`: **exit 2** for each client, "cannot read: git -C … rev-parse --verify --quiet
  0000000^{commit}: 1".
- `path --repository <scratch>/no-such-repository --commit HEAD`: exit 2, "… is not a git
  repository". `sgk --repository <fixture>`: exit 2, "--repository is for the client 'path' only".
- Each checklist's appendix equals that client's output byte for byte (`cmp` of the checklist with
  its text before the appendix plus a fresh run).

**The figures against the prompt's §0 and the note** (the outputs are whole below):

| Figure | Prompt / note | Script | |
|---|---|---|---|
| SGK live imports (files; module level) | 13 (10; 4) | 13 (10; 4) | equal, line for line as §0.1 |
| SGK `begin` calls, binding | 4, all | 4, all | equal; keywords as the note |
| SGK string literals naming it (commands) | 18 (3) | 18 (3) | equal; lines, deviation 16 |
| SGK campaign-record files | 7 | 6 import, 7 name | correction 5 |
| SGK staying tests' imports (modules) | 12 (5) | 12 (5) | equal |
| `_slug` the one private name of live code | yes | yes (`stage_counts.py:37, 38`) | equal |
| CPBH, SI imports | 0, 0 | 0, 0 | equal |
| Helper difference, CPBH and SI | `origin = None` | `-    origin = None`, each | equal |
| Non-`.py` lines, SGK | `prompts` 2078, `docs` 158, `CLAUDE.md` 10 | the same | equal |
| Non-`.py` lines, CPBH | `prompts` 19, `CLAUDE.md` 1, `.documents` 1 | the same | equal |
| Non-`.py` lines, SI | `.prompts` 9, `.documents` 2 | the same | equal |
| `.gitignore` `var/` | SGK only (`:3`) | SGK only (`:3`) | equal |
| Registry, SGK; CPBH | `config/datastore.py:91`; `:101` | the same | equal |
| `def inventory_spec`, SGK; CPBH; SI | 22; 17; none | 21 in 20 files; 17 in 17; 0 | deviation 17 |
| `fingerprint_of` calls not binding | not counted | 4 live, 2 staying | deviation 12 |
| Unknown names | none expected | 0 at each client | equal |

### 4. The fixture (§3.3)

`<scratch>/fixture`, a `git init` with one commit (`8681254`, "A fixture for
measure_client_registry.py"), holding five files:
- `driver.py`, with every case of §3.3:
  - a module-level `import RunRegistry` and `import RunRegistry.stores as rs`;
  - in `run`, a nested `from RunRegistry.stores import fingerprint_of, copy_store`,
    `fingerprint_of(inventory)`, `fingerprint_of(inventory, 6)`, `copy_store(...)`,
    `engine.begin()` and `RunRegistry._slug("a b")`;
  - a local `def begin`;
  - in `launch`, a `begin(...root=root)` that binds, a `begin(..., bogus=1)` that does not, a call of
    the local `begin`, and `RunRegistry.no_such_name`;
  - in `patches`, `mock.patch.object(RunRegistry, "DEFAULT_ROOT", …)`,
    `mock.patch("RunRegistry.stores.DEFAULT_STORES_ROOT", …)`, `setattr(RunRegistry, "REPO_ROOT", …)`,
    `rs.fingerprint_store = value`, and the string `python -m RunRegistry list`;
- `utilities.py`, CPBH's `utilities.py` at `c21cdfb` as `git show` gave it;
- `other/utilities.py`, the same with one line changed (`"editable": bool(dir_info.get("editable")),`
  for `… is True,`);
- `notes.md`, naming `RunRegistry`;
- `prompts/old/record.py`, a campaign record importing `fingerprint_of`.

`./venv/bin/python docs/adoption/measure_client_registry.py path --repository <fixture> --commit
HEAD`: **exit 3**. Every case is reported with the fate and verdict expected:
- the nested import with its scope `run`;
- `_slug` renamed to `slugify`;
- `DEFAULT_ROOT` patched by `patch.object`, `DEFAULT_STORES_ROOT` by `patch`, `REPO_ROOT` by
  `setattr`, each deleted;
- `fingerprint_store` assigned;
- `fingerprint_of(inventory)` "does not bind … (the move's new required `fingerprint_format`)",
  `fingerprint_of(inventory, 6)` binds;
- `begin(... root=...)` binds, `begin(..., bogus=1)` "does not bind: got an unexpected keyword
  argument 'bogus'";
- `engine.begin` and the local `begin` not the registry's;
- `no_such_name` unknown;
- the command flagged at `:43`;
- each helper copy against the package: the copy `-    origin = None` only, the changed copy that
  and its changed dictionary line;
- `notes.md:3` listed;
- the record counted.

The output is whole below.

### 5. The Q5 sketch (§3.5)

The sketch is `docs/adoption/README.md` §6's code block. Extracted from the README, it equals
`<scratch>/q5/spec_guard.py` (`diff`: none). It is proved by `<scratch>/q5/prove_spec_guard.py`,
run as `./venv/bin/python prove_spec_guard.py` from `<scratch>/q5`. It uses public names only:
`datastorekit.store_inventory`'s `InventorySpec`, `Parent`, `canonical_json` and `inventory_specs`;
the neutral store's `FACTORIES` is the input. The test classes:
- `TheGuard`: the neutral store's digests against their pin, format 1;
- `B1LeafAddedNoBump`: `Background`'s spec with a leaf `extra_leaf` added;
- `B2BumpWithNoNewPin`: format 2, no pin;
- `B3ClassAdded`: a class `Extra` with a spec;
- `StandIn`: a registry of `Alpha`, `Beta` and `Owner`, whose
  `Parent("of_serial", type_column="kind", types={1: "Alpha", 2: "Beta"})` is keyed by `int`;
- `B4KeyTypeChanged`: the same with the key `1` changed to `"1"`.

Its output, whole:

```
neutral FACTORIES: 9 classes; 6 with a spec
  version      02929e9353a2d7ed737e0c5336dd29b1bc64bf84693f865600ba6c66f455ec10
  store_tag    02929e9353a2d7ed737e0c5336dd29b1bc64bf84693f865600ba6c66f455ec10
  mode         6efba459e3f4ca4196696529b6e72330c2b035f73ac64607dc2ee99ba095cad8
  Background   22fe0c5346091598f66675e31c0756a43b8747a3e6445eaff145dae466927c57
  Solution     f300ba51ad75dcf0ec4ac0cbbb9655b27ef9368eeeb48681eead925a9ac92483
  Integral     c0996a3e5e0176a4c69c3ede3b41669ac724dc1173e9b99d8b9b6ef3c8044985
stand-in: [['Alpha', 'c46c0140ec3a3e6d60a9641e244943f1b9954f3aca82ef482584e29d1f5a12b7'], ['Beta', '7e7351fe581cacc4b960ae885b7ac3c40dac49b5c36748bac7370672779608a9'], ['Owner', '80f31887c8a376e0bd517e049a35eb107aa48b2fb0982b15b83bf49874c016e9']]
canonical_json of the raw spec, int keys: TypeError: canonical_json(): a key must be a string, not 1
plain(Owner).parents: {"\"of\"": {"column": "of_serial", "cross_shard": false, "nullable": false, "of": null, "type_column": "kind", "types": {"1": "Alpha", "2": "Beta"}}}
str(k) keys see B4's key-type change: False
plain() keys see B4's key-type change: True
a map holding 1 and '1': entries kept by plain(): 2 by str(k): 1
test_the_spec_digests_are_pinned_for_the_format (__main__.B1LeafAddedNoBump.test_the_spec_digests_are_pinned_for_the_format) ... FAIL
test_the_spec_digests_are_pinned_for_the_format (__main__.B2BumpWithNoNewPin.test_the_spec_digests_are_pinned_for_the_format) ... ERROR
test_the_spec_digests_are_pinned_for_the_format (__main__.B3ClassAdded.test_the_spec_digests_are_pinned_for_the_format) ... FAIL
test_the_spec_digests_are_pinned_for_the_format (__main__.B4KeyTypeChanged.test_the_spec_digests_are_pinned_for_the_format) ... FAIL
test_the_spec_digests_are_pinned_for_the_format (__main__.StandIn.test_the_spec_digests_are_pinned_for_the_format) ... ok
test_the_spec_digests_are_pinned_for_the_format (__main__.TheGuard.test_the_spec_digests_are_pinned_for_the_format) ... ok

======================================================================
ERROR: test_the_spec_digests_are_pinned_for_the_format (__main__.B2BumpWithNoNewPin.test_the_spec_digests_are_pinned_for_the_format)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/216541e8-6d82-4715-944d-1f8df5d629b8/scratchpad/agent-07/q5/prove_spec_guard.py", line 58, in test_the_spec_digests_are_pinned_for_the_format
    self.assertEqual(spec_digests(self.factories), self.pinned[self.fmt])
                                                   ~~~~~~~~~~~^^^^^^^^^^
KeyError: 2

======================================================================
FAIL: test_the_spec_digests_are_pinned_for_the_format (__main__.B1LeafAddedNoBump.test_the_spec_digests_are_pinned_for_the_format)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/216541e8-6d82-4715-944d-1f8df5d629b8/scratchpad/agent-07/q5/prove_spec_guard.py", line 58, in test_the_spec_digests_are_pinned_for_the_format
    self.assertEqual(spec_digests(self.factories), self.pinned[self.fmt])
AssertionError: Lists differ: [['ve[249 chars]d', '55af9536cbe3d2fdfe23c33dc0c9d98b6cdb2667c[185 chars]85']] != [['ve[249 chars]d', '22fe0c5346091598f66675e31c0756a43b8747a3e[185 chars]85']]

First differing element 3:
['Background', '55af9536cbe3d2fdfe23c33dc0c9d98b6cdb2667c[20 chars]263']
['Background', '22fe0c5346091598f66675e31c0756a43b8747a3e[20 chars]c57']

  [['version',
    '02929e9353a2d7ed737e0c5336dd29b1bc64bf84693f865600ba6c66f455ec10'],
   ['store_tag',
    '02929e9353a2d7ed737e0c5336dd29b1bc64bf84693f865600ba6c66f455ec10'],
   ['mode', '6efba459e3f4ca4196696529b6e72330c2b035f73ac64607dc2ee99ba095cad8'],
   ['Background',
-   '55af9536cbe3d2fdfe23c33dc0c9d98b6cdb2667cecf9f7c6510e11035e5d263'],
+   '22fe0c5346091598f66675e31c0756a43b8747a3e6445eaff145dae466927c57'],
   ['Solution',
    'f300ba51ad75dcf0ec4ac0cbbb9655b27ef9368eeeb48681eead925a9ac92483'],
   ['Integral',
    'c0996a3e5e0176a4c69c3ede3b41669ac724dc1173e9b99d8b9b6ef3c8044985']]

======================================================================
FAIL: test_the_spec_digests_are_pinned_for_the_format (__main__.B3ClassAdded.test_the_spec_digests_are_pinned_for_the_format)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/216541e8-6d82-4715-944d-1f8df5d629b8/scratchpad/agent-07/q5/prove_spec_guard.py", line 58, in test_the_spec_digests_are_pinned_for_the_format
    self.assertEqual(spec_digests(self.factories), self.pinned[self.fmt])
AssertionError: Lists differ: [['ve[479 chars]985'], ['Extra', '3e69e5a912303825acefccda1d94[34 chars]fb']] != [['ve[479 chars]985']]

First list contains 1 additional elements.
First extra element 6:
['Extra', '3e69e5a912303825acefccda1d940e339b9c295f1546be999265b5b63af82ffb']

Diff is 831 characters long. Set self.maxDiff to None to see it.

======================================================================
FAIL: test_the_spec_digests_are_pinned_for_the_format (__main__.B4KeyTypeChanged.test_the_spec_digests_are_pinned_for_the_format)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/216541e8-6d82-4715-944d-1f8df5d629b8/scratchpad/agent-07/q5/prove_spec_guard.py", line 58, in test_the_spec_digests_are_pinned_for_the_format
    self.assertEqual(spec_digests(self.factories), self.pinned[self.fmt])
AssertionError: Lists differ: [['Al[159 chars]r', '70998cfe584618f716721a7b34578801a7bff14f5[21 chars]0e']] != [['Al[159 chars]r', '80f31887c8a376e0bd517e049a35eb107aa48b2fb[21 chars]e9']]

First differing element 2:
['Owner', '70998cfe584618f716721a7b34578801a7bff14f5df97762a27663ae0180f00e']
['Owner', '80f31887c8a376e0bd517e049a35eb107aa48b2fb0982b15b83bf49874c016e9']

  [['Alpha', 'c46c0140ec3a3e6d60a9641e244943f1b9954f3aca82ef482584e29d1f5a12b7'],
   ['Beta', '7e7351fe581cacc4b960ae885b7ac3c40dac49b5c36748bac7370672779608a9'],
-  ['Owner', '70998cfe584618f716721a7b34578801a7bff14f5df97762a27663ae0180f00e']]
+  ['Owner', '80f31887c8a376e0bd517e049a35eb107aa48b2fb0982b15b83bf49874c016e9']]

----------------------------------------------------------------------
Ran 6 tests in 0.002s

FAILED (failures=3, errors=1)
```

`TheGuard` and `StandIn` pass. B1, B3 and B4 fail, each naming the class (`Background`, `Extra`,
`Owner`); B2 errors with `KeyError: 2`, a test failure. Every breakage SGK's 07 names fails, and so
does the key-type change. A bare `str(k)` conversion would not see that change ("str(k) keys see
B4's key-type change: False"), and it collapses a map holding `1` and `"1"` to one entry.
`canonical_json` refuses the raw spec's `int` keys. The neutral store gives 6 digests for its 9
classes.

### 6. The README's worktree sentences, by running (U20)

In `<scratch>/u20`, a repository `main` was made with a `runregistrykit.toml` naming
`fpmod:FP` and `fpmod.py` (`WHO = "main"`), and a linked worktree `wt` was added. The worktree's
`fpmod.py` was set to `WHO = "worktree"`, and its own `runregistrykit.toml` to
`runs_root = "elsewhere/runs"`. From `wt`, with `-I`:

```
found (config that governs): True
root (record root): True
runs_root from the worktree's config, joined to the record root: True
fingerprinter module imported from: wt/fpmod.py worktree
sys.path[0] is found: True
no config in the main checkout; root True found True
```

The last line is after the main checkout's `runregistrykit.toml` was removed: the worktree's config
still governs, and the record root is still the main checkout.

### 7. The statements about the package

Each was checked against `v0.1.0` (`9f8ebe4`, the working tree); `<scratch>` is `agent-07/`.
- **`__all__` and signatures**: from the venv, `runregistrykit.__all__` has 20 names,
  `runregistrykit.stores` 26, `client` 4, `fingerprint` 4, `__main__` 1. `inspect.signature` of
  `begin`, `list_runs`, `package_provenance`, `slugify`, `_repo_path`, `run_id`, `liveness`,
  `pid_alive`, `read_json`, `now_iso`, `Run._fingerprint_results`, the eight store functions,
  `read_sidecar`, `sidecar_path`, `write_listing` and `_fingerprint_problems`. Each was compared with
  `a45aefc`'s parameters by `ast`. Every public function SGK uses differs only by the keyword-only
  `client_root=`. `git_provenance` and `package_provenance` lost their defaults. `_repo_path` gained
  `root`. `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format: int,
  taken=None)`, `ENCODING_FORMAT = 1`. The script prints each of these in its appendices.
- **The fate table**: checked by the script at every run (section 2.1), and by breakage (a0) below.
- **`slugify` is `_slug`**: `ast` of the bodies, docstrings removed, equal (`True`).
- **The config SGK would write** (the TOML of its checklist, item 3), in `<scratch>/pkgcheck/sgkroot`,
  read by `find_client_root(client_root=…)`: `runs_root` and `stores_root` under it,
  `distributions` `('datastorekit', 'raypoolkit')`, `stores`
  `{'fingerprinter': 'config.fingerprint:fingerprinter'}`. `_recorded_names` gives
  `('runregistrykit', 'datastorekit', 'raypoolkit')`.
- **A name not installed**: `package_provenance(["no-such-distribution-xyz"])` is
  `{'no-such-distribution-xyz': None}`; the code is `runregistrykit/__init__.py:178-182`.
- **The store layer without a fingerprinter**: with an empty `runregistrykit.toml`,
  - `read_sidecar` reads;
  - `fingerprint_store` and `copy_store` raise `ConfigError` "… names no fingerprinter, and the
    store layer requires one …";
  - `python -m runregistrykit --client-root <empty> store show <primary>` exits 1 with the same
    text.

  With `[stores] fingerprinter = "config.fingerprint:fingerprinter"` named but not importable,
  `store show` exits 0 and prints the sidecar `kind: absent`: it does not import the fingerprinter
  (`runregistrykit/fingerprint.py:56-59`).
- **`fingerprint_of` with a dict as the format**: `TypeError: fingerprint_of(): fingerprint_format
  must be an int, not dict {'when': None}` (the meaning of SGK's `:378`). DatastoreKit's
  `fingerprint_of` returns six keys, `encoding_format` among them, and `compare_fingerprints` compares
  the versions first (its source, read).
- **`fingerprint_store`'s return** has the same seven keys at `a45aefc` (`RunRegistry/stores.py:1546-1554`)
  and at `v0.1.0` (`runregistrykit/stores.py:1388-1396`).
- **`--help`**: `python -m runregistrykit --help`, `list --help` and `store --help`, as SGK's checklist
  item 5 names them (`--client-root DIR` before the command; `list --root DIR --stale-after SECONDS`;
  `store {show,create,adopt,copy,move,fingerprint,retire,amend}`).
- **The README's sections cited by link** (Installing, Supported versions, Using it and its
  subsections, The rules, The public names, What the registry writes …) were read at this commit.
  Each statement the adoption README draws from them is in them: the two pin lines and why, the core
  form, the editable warning, the three configurations, Ray's 3.13 floor, the config keys and
  defaults, the store layer's refusal, no patch target promised (with `runregistrykit/__init__.py:468`
  read).
- **The lazy import**: `runregistrykit/__init__.py:468`, `from .stores import _sidecar_refusal,
  fingerprint_store, read_sidecar`, inside `Run._fingerprint_results`.
- **The loader**: `runregistrykit/fingerprint.py:191-193` puts `client.found` first on `sys.path`;
  `:211-217` refuses a class.
- **Links** (§3.7): 37 relative links in `docs/adoption/`, each to a tracked file (or one of this
  commit's) and, where it has an anchor, to a heading of that file (GitHub's anchor rule), 0 bad.
  External links: the pin lines' `github.com/ds283/RunRegistryKit@v0.1.0`,
  `DatastoreKit@v0.4.0` and `RayPoolKit@v0.2.0`, each at a named tag.

### 8. Every `path:line` the checklists cite, read at its commit

Read through `git show <commit>:<path>` (the text squeezed and cut at 110 characters). The
package's lines are under 7. The appendices' lines are the script's own. A range cited in a
checklist (`:72-73`, `:234-238`) was read whole; its first line is listed here.


`SecondaryGWKit` `14bcac0` `.gitignore`:

- `:3` var/

`SecondaryGWKit` `14bcac0` `requirements.txt`:

- `:17` datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
- `:75` ray==2.43.0
- `:76` raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
- `:87` SQLAlchemy==2.0.39

`SecondaryGWKit` `14bcac0` `CLAUDE.md`:

- `:77` ## Long-running jobs — the run registry
- `:87` 1. **Discovery.** Run `python -m RunRegistry list` at the start of a session and before launching
- `:106` ## `RunRegistry/` is frozen — it is moving to RunRegistryKit
- `:113` - **Nothing under `RunRegistry/` changes**, its tests included, until
- `:144` PYTHONPATH=. ./venv/bin/python -m unittest discover -s RunRegistry/tests -t .

`SecondaryGWKit` `14bcac0` `config/datastore.py`:

- `:91` factories = {
- `:92` "version": sqla_version_factory,

`SecondaryGWKit` `14bcac0` `ObjectFactories/cosmology_types.py`:

- `:17` COSMOLOGY_TYPES: Dict[int, str] = {
- `:18` LAMBDACDM_IDENTIFIER: "LambdaCDM",
- `:19` QCD_EOS_IDENTIFIER: "QCD_Cosmology",

`SecondaryGWKit` `14bcac0` `CosmologyModels/model_ids.py`:

- `:1` LAMBDACDM_IDENTIFIER = 0
- `:2` QCD_EOS_IDENTIFIER = 1

`SecondaryGWKit` `14bcac0` `ObjectFactories/BackgroundModel.py`:

- `:900` "cosmology": Parent(
- `:903` types=COSMOLOGY_TYPES,

`SecondaryGWKit` `14bcac0` `ObjectFactories/wavenumber.py`:

- `:126` def inventory_spec():
- `:385` def inventory_spec():
- `:396` "cosmology": Parent(
- `:399` types=COSMOLOGY_TYPES,

`SecondaryGWKit` `14bcac0` `ObjectFactories/tests/test_quadsource_policy_key.py`:

- `:411` from RunRegistry.stores import fingerprint_of
- `:413` under_1 = fingerprint_of(self.read_the_store(1))["classes"][
- `:416` under_2 = fingerprint_of(self.read_the_store(2))["classes"][
- `:419` again_2 = fingerprint_of(self.read_the_store(2))["classes"][

`SecondaryGWKit` `14bcac0` `docs/a3-v2-readiness/fingerprint_time_probe.py`:

- `:83` from RunRegistry.stores import FINGERPRINT_FORMAT, fingerprint_store
- `:85` print(f"\nimport RunRegistry.stores: {time.perf_counter() - t:.3f} s")
- `:86` print(f"FINGERPRINT_FORMAT at HEAD: {FINGERPRINT_FORMAT}")
- `:93` taken = fingerprint_store(STORE, write=False)

`SecondaryGWKit` `14bcac0` `docs/a3-v2-readiness/sigterm_handler_probe.py`:

- `:150` import RunRegistry
- `:151` import RunRegistry.stores as registry_stores
- `:159` run = RunRegistry.begin(
- `:167` root=root,
- `:187` real_fingerprint = registry_stores.fingerprint_store
- `:210` registry_stores.fingerprint_store = slow_fingerprint

`SecondaryGWKit` `14bcac0` `docs/datastore-integrity-verification/compare_stores.py`:

- `:21` from RunRegistry.stores import ( # noqa: E402
- `:32` result = fingerprint_store(primary, write=False)
- `:46` ok = ok and not result["comparison"]
- `:48` ok and fp["fingerprint_format"] == FINGERPRINT_FORMAT and not fp["problems"]
- `:51` differences = compare_fingerprints(taken["reference"], taken["resumed"])

`SecondaryGWKit` `14bcac0` `docs/datastore-integrity-verification/interrupt_when.py`:

- `:61` import RunRegistry # noqa: E402
- `:68` return RunRegistry.now_iso()
- `:87` manifest = RunRegistry.read_json(str(run_dir / "manifest.json")) or {}
- `:101` manifest = RunRegistry.read_json(str(run_dir / "manifest.json")) or {}
- `:161` status = RunRegistry.read_json(str(run_dir / "status.json")) or {}
- `:165` if state in RunRegistry.TERMINAL_STATES:
- `:170` if state == "running" and not RunRegistry.pid_alive(pid):
- `:175` verdict = RunRegistry.liveness(status, stale_after)
- `:190` if not RunRegistry.pid_alive(pid):
- `:230` "--stale-after", type=float, default=RunRegistry.DEFAULT_STALE_AFTER

`SecondaryGWKit` `14bcac0` `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py`:

- `:29` from RunRegistry.stores import ( # noqa: E402
- `:64` result = fingerprint_store(primary, write=False)
- `:71` if fp["fingerprint_format"] != FINGERPRINT_FORMAT or fp["problems"]:
- `:80` diffs = compare_fingerprints(rec, fp)

`SecondaryGWKit` `14bcac0` `docs/dk-and-rpk-migration/rehearsal/stage_counts.py`:

- `:26` import RunRegistry # noqa: E402
- `:31` """The slug `RunRegistry.run_id` was given, recovered from the manifest's own fields."""
- `:37` RunRegistry._slug(manifest["campaign"]),
- `:38` RunRegistry._slug(manifest["prompt"]),

`SecondaryGWKit` `14bcac0` `docs/gktk-remedial/scoped_pipeline_run.py`:

- `:526` import RunRegistry
- `:529` "scoped_pipeline_run: --register needs RunRegistry on the path; run this script "
- `:541` run = RunRegistry.begin(
- `:546` script=__file__,
- `:578` f"** scoped_pipeline_run: registered as {run.id}\n"
- `:580` f"** list it with: PYTHONPATH=. ./venv/bin/python -m RunRegistry list"
- `:611` help="record this run in var/runs/ through RunRegistry, under this slug. Without it "

`SecondaryGWKit` `14bcac0` `docs/handover/quadsource_atol_sweep.py`:

- `:412` """`main.py`'s argv for either driver, `sys.argv` form (the program name first).
- `:554` import RunRegistry
- `:556` run = RunRegistry.begin(
- `:593` f"** quadsource_atol_sweep --build: registered as {run.id}\n"
- `:595` f"** list it with: PYTHONPATH=. ./venv/bin/python -m RunRegistry list"
- `:740` """Make the sweep store from the baseline through one registry copy.
- `:752` 'quadsource_atol_sweep --prepare: --force no longer means "replace". '
- `:760` import RunRegistry.stores
- `:763` RunRegistry.stores.copy_store(
- `:862` import RunRegistry
- `:864` run = RunRegistry.begin(
- `:904` f"** quadsource_atol_sweep: registered as {run.id}\n"
- `:906` f"** list it with: PYTHONPATH=. ./venv/bin/python -m RunRegistry list"

`SecondaryGWKit` `14bcac0` `docs/runregistry-extraction/fingerprint_both_ways.py`:

- `:110` from RunRegistry import stores as sgk_stores
- `:127` sgk = sgk_stores.fingerprint_of(inventory)
- `:128` pkg = package.fingerprint_of(inventory, sgk_stores.FINGERPRINT_FORMAT)
- `:203` sgk_lines = list(sgk_stores.listing_lines(inventory, sgk))
- `:227` ss = sgk_stores.compare_fingerprints(sgk, sgk)
- `:240` reading = sgk_stores.read_sidecar(str(primary))
- `:247` rs = sgk_stores.compare_fingerprints(recorded, sgk)

`SecondaryGWKit` `14bcac0` `docs/OPEN_ISSUES.md`:

- `:661` ### 1.11 The run registry campaign

`SecondaryGWKit` `14bcac0` `docs/a3-v2-readiness/interrupter_build_dummy_test.sh`:

- `:6` # `argv[0]` is `docs/handover/quadsource_atol_sweep.py` (`RunRegistry.begin` records `sys.argv`

`SecondaryGWKit` `14bcac0` `RunRegistry/stores.py`:

- `:194` # the fingerprint's format. A fingerprint is compared only with one of the same format; a change to
- `:197` # (`RunRegistry/tests/data/full_store_fingerprint*.json`; `test_store_fingerprint.GOLDEN` names the
- `:205` # own identity, across shards where it is held on another
- `:206` FINGERPRINT_FORMAT = 6

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/store_fixtures.py`:

- `:20` from StoreFixtures.shard_store_fixtures import (
- `:85` def sweep_shaped(other: Path) -> dict:
- `:97` def write_sidecar_json(primary: Path, payload) -> Path:
- `:105` def load(path: Path):
- `:114` class StoreTestCase(RegistryTestCase):
- `:134` stores.create_sidecar(primary, "a store in a temporary directory")

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/test_run_registry.py`:

- `:113` class RegistryTestCase(unittest.TestCase):
- `:124` return RunRegistry.begin(

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/test_store_command_line.py`:

- `:53` class CommandLineTestCase(StoreTestCase):

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/test_build_rehearsal_scope.py`:

- `:39` from RunRegistry.tests.test_prune_on_resume import parsed_arguments
- `:317` and ast.unparse(node.func) == "RunRegistry.begin"

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/test_killed_handler.py`:

- `:26` import RunRegistry
- `:27` from RunRegistry.tests.test_pipeline_adoption import DRIVER, REPO_ROOT, load_driver
- `:90` return RunRegistry.begin(
- `:186` status = RunRegistry.read_json(run.status_path)
- `:333` with mock.patch.object(run, "_fingerprint_results", interrupted):
- `:336` status = RunRegistry.read_json(run.status_path)
- `:432` with mock.patch.object(run, "_fingerprint_results", interrupted):
- `:435` status = RunRegistry.read_json(run.status_path)

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/test_pipeline_adoption.py`:

- `:27` import RunRegistry
- `:29` REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
- `:72` kwargs.setdefault("purpose", "a test run, in a temporary directory")
- `:73` kwargs.setdefault("argv", ["unittest"])
- `:74` return RunRegistry.begin(
- `:142` entry = RunRegistry.list_runs(root=self.root)[0]
- `:146` [sys.executable, "-m", "RunRegistry", "list", "--root", self.root],
- `:158` [sys.executable, "-m", "RunRegistry", "list", "--root", self.root],
- `:179` said = RunRegistry.read_json(run.manifest_path)["heartbeat_means"]
- `:252` self.assertIn(self.driver.terminal_state(code), RunRegistry.TERMINAL_STATES)
- `:278` root = RunRegistry.DEFAULT_ROOT
- `:330` with mock.patch.object(RunRegistry, "DEFAULT_ROOT", self.root):

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py`:

- `:25` import RunRegistry
- `:26` from RunRegistry import stores
- `:27` from RunRegistry.tests.store_fixtures import StoreTestCase
- `:61` class SweepPrepareTestCase(StoreTestCase):
- `:73` patcher = mock.patch.object(stores, "DEFAULT_ROOT", self.root)
- `:87` stores.create_sidecar(
- `:101` return stores.sidecar_path(self.sweep_store)
- `:115` baseline_id = stores.read_sidecar(baseline).fields["store_id"]
- `:129` reading = stores.read_sidecar(self.sweep_store)
- `:134` {"store_id": baseline_id, "datastore": RunRegistry._repo_path(baseline)},

`SecondaryGWKit` `14bcac0` `RunRegistry/tests/test_store_fingerprint.py`:

- `:33` import RunRegistry
- `:34` from RunRegistry import stores
- `:35` from RunRegistry.stores import (
- `:41` from RunRegistry.tests.store_fixtures import (
- `:47` from RunRegistry.tests.test_store_command_line import CommandLineTestCase
- `:50` from StoreFixtures.real_store_fixtures import (
- `:73` REPO_ROOT = Path(RunRegistry.REPO_ROOT)
- `:74` GOLDEN = (
- `:138` class _FullStores(unittest.TestCase):
- `:147` cls.baseline = fingerprint_of(cls.baseline_inventory)
- `:162` return fingerprint_of(read_inventory(cls.store(**kwargs).primary, _factories))
- `:347` class TestGolden(_FullStores):
- `:352` self.assertEqual(golden["fingerprint_format"], FINGERPRINT_FORMAT)
- `:354` self.assertEqual(without_taken(self.baseline), without_taken(golden))
- `:356` self.assertEqual(without_taken(self.fingerprint()), without_taken(golden))
- `:361` set(fp), {"fingerprint_format", "classes", "digest", "problems", "taken"}
- `:374` self.assertEqual(stores._fingerprint_problems(dict(fp, taken={})), [])
- `:378` with_taken = fingerprint_of(self.baseline_inventory, taken)
- `:381` self.assertEqual(compare_fingerprints(self.baseline, with_taken), [])
- `:855` class TestDrivers(unittest.TestCase):

`SecondaryGWKit` `14bcac0` `prompts/runregistry-extraction/runregistrykit-extraction-brief.md`:

- `:134` ## 8. What SGK needs back (its gate E2)
- `:139` 2. **An SGK adoption checklist** (`docs/adoption/secondarygwkit.md`, as the siblings'), which SGK's
- `:143` `RunRegistry.*` at each SGK call site (audit §2.1 lists them; `stage_counts.py` uses the private

`SecondaryGWKit` `14bcac0` `prompts/runregistry-extraction/README.md`:

- `:268` 3. `python -m runregistrykit list` gives 01's baseline: the same 29 runs, states and purposes.
- `:270` 4. **From a worktree** of this repository, `begin()` of a throwaway run records it under the main
- `:277` 7. Closes `[00-recorded-fingerprints-lack-the-encoding-format]`: before any call of the package's
- `:328` - **R0's and R1's four are retired after 04's review** (the user's ruling D6, 2026-10-14, §6.1). Their
- `:351` - **04 ships** `docs/runregistry-extraction/fingerprint_both_ways.py <primary>...` (W1). It compares
- `:372` - **`compare_with_recorded.py` is not 08's comparison with R1 and R0.** After 06 it compares
- `:534` \| **D6** — the fingerprints SGK holds, which lack `encoding_format` \| **Option (c): retire R0's and R1's four 

`ChamPBH` `c21cdfb` `requirements.txt`:

- `:17` datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
- `:79` ray==2.53.0
- `:80` raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0
- `:91` SQLAlchemy==2.0.46

`ChamPBH` `c21cdfb` `CLAUDE.md`:

- `:115` - **Long-running jobs.** Production pipeline runs (`main.py` with a datastore) are the user's and
- `:117` longer than a few PRyMordial solves. There is no run registry in this repository.
- `:118` - **The plot scripts** (`plot_by_beta.py`, `plot_ScalarModel.py`) read a store read-only, through

`ChamPBH` `c21cdfb` `utilities.py`:

- `:174` RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")
- `:177` def installed_package_provenance(names=RECORDED_DISTRIBUTIONS) -> dict:
- `:190` These are the fields, with the same meaning, of SecondaryGWKit's
- `:202` except importlib.metadata.PackageNotFoundError:
- `:204` continue
- `:232` def format_package_provenance(provenance: dict) -> str:

`ChamPBH` `c21cdfb` `main.py`:

- `:77` from utilities import (
- `:81` installed_package_provenance,
- `:95` print(format_package_provenance(installed_package_provenance()), flush=True)

`ChamPBH` `c21cdfb` `plot_ScalarModel.py`:

- `:79` from utilities import format_package_provenance, installed_package_provenance
- `:89` print(format_package_provenance(installed_package_provenance()), flush=True)

`ChamPBH` `c21cdfb` `plot_by_beta.py`:

- `:78` from utilities import format_package_provenance, installed_package_provenance
- `:108` print(format_package_provenance(installed_package_provenance()), flush=True)

`ChamPBH` `c21cdfb` `config/datastore.py`:

- `:101` factories = {
- `:102` "version": sqla_version_factory(),

`ChamPBH` `c21cdfb` `ObjectFactories/ScalarModel.py`:

- `:230` return InventorySpec(
- `:234` "cosmology": Parent(
- `:237` types={XAV_IMPROVED_EOS_IDENTIFIER: "QCD_Cosmology"},
- `:239` "potential": Parent(
- `:250` "coupling": Parent(
- `:253` types={EXPONENTIAL_COUPLING: "ExponentialCoupling"},

`ChamPBH` `c21cdfb` `CosmologyModels/model_ids.py`:

- `:19` XAV_IMPROVED_EOS_IDENTIFIER = 3

`ChamPBH` `c21cdfb` `CosmologyConcepts/Potentials/model_ids.py`:

- `:16` INVERSE_POWER_POTENTIAL = 0
- `:20` RECLINER_POTENTIAL = 4

`ChamPBH` `c21cdfb` `CosmologyConcepts/ConformalCouplings/model_ids.py`:

- `:16` EXPONENTIAL_COUPLING = 0

`ChamPBH` `c21cdfb` `ObjectFactories/tests/test_inventory_specs.py`:

- `:25` - **coverage** (campaign README §6.5, the user's ruling): every registered class declares a spec,

`ChamPBH` `c21cdfb` `ObjectFactories/tests/test_package_provenance.py`:

- `:46` from utilities import format_package_provenance, installed_package_provenance
- `:49` DRIVERS = ("main.py", "plot_by_beta.py", "plot_ScalarModel.py")
- `:91` class TestInstalledPackageProvenance(_StandInCase):
- `:270` def test_default_names(self):
- `:273` utilities.RECORDED_DISTRIBUTIONS, ("datastorekit", "raypoolkit")
- `:280` def _is_provenance_print(node) -> bool:
- `:298` and inner.args[0].func.id == "installed_package_provenance"
- `:316` class TestDriversPrintProvenance(unittest.TestCase):
- `:325` helper_calls = _calls(tree, "installed_package_provenance")

`ChamPBH` `c21cdfb` `.documents/architecture-summary.md`:

- `:299` it is there for the RunRegistry component, which needs this release.

`StochasticInstantons` `5fb4a1d` `requirements.txt`:

- `:57` ray==2.55.1
- `:65` SQLAlchemy==2.0.46

`StochasticInstantons` `5fb4a1d` `CLAUDE.md`:

- `:14` `--ray-address` is required by `main.py` and both plot scripts; there is no
- `:16` cluster's GCS address. Rehearsals and long builds run on SI's isolated cluster

`StochasticInstantons` `5fb4a1d` `utilities.py`:

- `:174` RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")
- `:177` def installed_package_provenance(names=RECORDED_DISTRIBUTIONS) -> dict:

`StochasticInstantons` `5fb4a1d` `main.py`:

- `:48` from utilities import format_package_provenance, installed_package_provenance
- `:98` print(format_package_provenance(installed_package_provenance()), flush=True)
- `:99` ray.init(address=args.ray_address)

`StochasticInstantons` `5fb4a1d` `plot_GradientCoupledSolutions.py`:

- `:102` from utilities import format_package_provenance, installed_package_provenance
- `:972` print(format_package_provenance(installed_package_provenance()), flush=True)
- `:973` ray.init(address=args.ray_address, ignore_reinit_error=True)

`StochasticInstantons` `5fb4a1d` `plot_InstantonSolutions.py`:

- `:74` from utilities import format_package_provenance, installed_package_provenance
- `:1205` print(format_package_provenance(installed_package_provenance()), flush=True)
- `:1206` ray.init(address=args.ray_address, ignore_reinit_error=True)

`StochasticInstantons` `5fb4a1d` `Datastore/SQL/Datastore.py`:

- `:96` _factories = {

`StochasticInstantons` `5fb4a1d` `tests/test_package_provenance.py`:

- `:47` from utilities import format_package_provenance, installed_package_provenance
- `:50` DRIVERS = ("main.py", "plot_InstantonSolutions.py", "plot_GradientCoupledSolutions.py")
- `:91` def test_not_installed(stand_in):
- `:267` def test_default_names():
- `:269` assert utilities.RECORDED_DISTRIBUTIONS == ("datastorekit", "raypoolkit")
- `:277` def _is_provenance_print(node) -> bool:
- `:336` @pytest.mark.parametrize("driver", DRIVERS)
- `:344` assert len(_calls(tree, "installed_package_provenance")) == 1

`StochasticInstantons` `5fb4a1d` `.documents/dk-and-rpk-migration/01-rehearsal-tooling-and-run-provenance.md`:

- `:36` Its fields and their meanings are those of SGK's `RunRegistry.package_provenance()`
- `:37` (`SecondaryGWKit/RunRegistry/__init__.py:122-169`, read, not imported) and of ChamPBH's helper


## The deliberate-breakage record

None committed. Each diff is against the script as committed (SHA-256
`159e0b80060f5f98b5cdfc17ca6865128efc83b79fb3e636eb30e19b62530f80`) and was applied from the
repository's root:
1. `git apply --check` (in `bash`);
2. `git apply`;
3. the run;
4. `git apply -R --check`;
5. `git apply -R`.

After each, the script's SHA-256 was the same as before and `git status --short` showed this
commit's changes only (` M PROVENANCE.md`, ` M README.md`, `?? docs/adoption/`). The fixture's
`git status --porcelain` was empty after (c).

| # | Change | What failed |
|---|---|---|
| (a0) | a deletion row for `liveness`, which `v0.1.0` has, **with** the row check | the script refuses before measuring: `sgk` **exit 1**, "the table disagrees with the package: RunRegistry.liveness is deleted, but runregistrykit has it" |
| (a) | the same row, and the row check's `raise` removed | `sgk` exit 0, and `RunRegistry.liveness` reported **"deleted"** at `interrupt_when.py:175`, which is wrong: (a0) shows the check refusing it |
| (b) | nested scopes not walked: a function's body not visited (module level only) | the fixture: **2 imports, not 3**; the nested `from RunRegistry.stores import fingerprint_of, copy_store` missing (0 rows); exit 0, since `RunRegistry.no_such_name`, inside `launch`, is missed too. SGK: **4 imports in 4 files, not 13 in 10** |
| (c) | the working tree read in place of `git show` (`(repository / path).read_text()`) | with the fixture clean, the output equals the committed script's; after an uncommitted edit (a function `extra` calling `RunRegistry.liveness`, appended to `driver.py`), **the output changes**: "Names used" 9 → 10, and `RunRegistry.liveness` at `driver.py:47`. The committed script, on the same dirty fixture, gives its committed output byte for byte (the control) |
| (d) | the bind verdict replaced by a check of the keywords against a hard-coded list | the fixture's `fingerprint_of(inventory)` at `driver.py:12` reports **"binds"** (so do `:13`, `:14`, `:26`); only `begin(..., bogus=1)` "does not bind" |
| (e) | the sort of the names removed (`list(names.values())`, first-seen order) | two runs at one commit are still byte-identical (`git ls-tree` and the walk are in a fixed order), but the output's order **differs from the committed run**: the names table begins `RunRegistry.stores.fingerprint_of`, `…FINGERPRINT_FORMAT`, `…fingerprint_store`, where the committed run's begins `RunRegistry.DEFAULT_STALE_AFTER` |

### The diffs, as applied

`<scratch>/breakage/<name>.diff`, from `diff -u` with `a/` and `b/` labels; `git apply` reads them
with its default `-p1`.

#### (a0)

```diff
--- a/docs/adoption/measure_client_registry.py
+++ b/docs/adoption/measure_client_registry.py
@@ -170,6 +170,7 @@
         "datastorekit.store_fingerprint.listing_lines",
         "layer C, DatastoreKit's since v0.4.0",
     ),
+    ("RunRegistry", "liveness"): ("deleted", None, "a wrong row, for breakage (a)"),
 }
 
 # the calls whose arguments are bound against v0.1.0's function
```

#### (a)

```diff
--- a/docs/adoption/measure_client_registry.py
+++ b/docs/adoption/measure_client_registry.py
@@ -170,6 +170,7 @@
         "datastorekit.store_fingerprint.listing_lines",
         "layer C, DatastoreKit's since v0.4.0",
     ),
+    ("RunRegistry", "liveness"): ("deleted", None, "a wrong row, for breakage (a)"),
 }
 
 # the calls whose arguments are bound against v0.1.0's function
@@ -412,8 +413,6 @@
             "pyproject.toml does not exclude runregistrykit.tests, so a name from the "
             "registry's tests cannot be called not shipped"
         )
-    if problems:
-        raise TableDisagrees("; ".join(problems))
     return targets
 
 
```

#### (b)

```diff
--- a/docs/adoption/measure_client_registry.py
+++ b/docs/adoption/measure_client_registry.py
@@ -755,9 +755,6 @@
             for child in node.args.kw_defaults:
                 if child is not None:
                     self.visit(child, scope)
-            inner = Scope("function", node.name, scope, self._bindings(node.body, node))
-            for child in node.body:
-                self.visit(child, inner)
             return
         if isinstance(node, ast.Lambda):
             for child in node.args.defaults:
```

#### (c)

```diff
--- a/docs/adoption/measure_client_registry.py
+++ b/docs/adoption/measure_client_registry.py
@@ -1029,7 +1029,7 @@
             part = "records"
         else:
             part = "live"
-        source = show(repository, commit, path)
+        source = (repository / path).read_text()
         try:
             keep = STAYING.get(path) if part == "staying" else None
             analysis = FileAnalysis(path, source, known_modules, run_private, keep)
```

#### (d)

```diff
--- a/docs/adoption/measure_client_registry.py
+++ b/docs/adoption/measure_client_registry.py
@@ -1159,21 +1159,13 @@
                 call["target"], call["verdict"] = None, "no function at v0.1.0"
                 continue
             call["target"] = callee[0] + signature_text(params_of_function(callee[1]))
-            # an unpacking may supply what is missing, so then only what is spelled is bound
             unpacks = call["starred"] or call["double_starred"]
-            signature = inspect.signature(callee[1])
-            bind = signature.bind_partial if unpacks else signature.bind
-            placeholder = object()
-            try:
-                bind(
-                    *[placeholder] * call["positional"],
-                    **{k: placeholder for k in call["keywords"]},
-                )
+            known = {"campaign", "prompt", "slug", "purpose", "argv", "script", "root", "results"}
+            known |= {"scope", "heartbeat_means", "write", "purpose", "taken"}
+            if set(call["keywords"]) <= known:
                 verdict = "binds"
-            except TypeError as e:
-                verdict = f"does not bind: {e}"
-                if call["name"] == "fingerprint_of" and str(e) == MISSING_FORMAT:
-                    verdict += " (the move's new required `fingerprint_format`)"
+            else:
+                verdict = "does not bind"
             if unpacks:
                 verdict += " (its spelled arguments; the unpacking is not expanded)"
             call["verdict"] = verdict
```

#### (e)

```diff
--- a/docs/adoption/measure_client_registry.py
+++ b/docs/adoption/measure_client_registry.py
@@ -1181,7 +1181,7 @@
             "files": sorted(files[part]),
             "imports": imports,
             "module_level_imports": sum(i["scope"] == "module" for i in imports),
-            "names": [names[k] for k in sorted(names)],
+            "names": list(names.values()),
             "module_uses": [u for u in uses if u["kind"].startswith("module")],
             "calls": calls,
             "alikes": sorted((c for a in analyses[part] for c in a.alikes), key=key),
```

## Observations not acted on

1. **Two of SGK's staying tests redirect a driver's runs root by patching a deleted name.**
   `test_pipeline_adoption.py:330` patches `RunRegistry.DEFAULT_ROOT` around the driver's
   `register`, and `test_quadsource_atol_sweep_prepare.py:73` patches `stores.DEFAULT_ROOT` around
   `prepare()`'s `copy_store`. At `v0.1.0` there is nothing to patch. As written, the first would
   record its run under SGK's real `var/runs/`, and the second would scan it. SGK's checklist, item 7,
   names the options with **Advice:**. The decision, and the change to the driver, are SGK's; nothing
   in the package changes.
2. **`test_build_rehearsal_scope.py:317` asserts the driver's spelling, `"RunRegistry.begin"`**, so
   the rewrite of `quadsource_atol_sweep.py:556` and this string must land together (SGK's
   checklist, item 7).
3. **SGK's golden fingerprint lacks `encoding_format`**
   (`full_store_fingerprint_datastore-integrity-09c.json`, no such key), so `TestGolden`'s
   comparisons and its shape assertion fail as written once `fingerprint_of` is DatastoreKit's. It is
   U7's fact on SGK's own data. SGK's checklist, item 7, names the choice.
4. **SGK's plan and this campaign's README count SGK's sidecars differently**: SGK's
   `prompts/runregistry-extraction/README.md:67` and `:269` say 14; this campaign's README §0.2 says
   "SGK's 18 sidecars are all tombstones (SGK board §3, 2026-10-14)". The checklist says "each of its
   sidecars" without a number; the count is SGK's to measure, and this repository's README is not
   07's to change.
5. **`PROVENANCE.md`'s preamble** still says the package's prose cites SGK "until prompt 05 rewrites
   them" (`:19-20`); 06's log left it for 08, and so does this one.
6. **The printed command was once read as a stage.** SGK's recorded interrupter output
   (`docs/a3-v2-readiness/rehearsal/interrupter_firings.txt:3`,
   `docs/datastore-integrity-verification/interrupter_firings.txt:3, 12`) shows a stage `'list it with:
   PYTHONPATH=. ./venv/bin/python -m Ru…'`: SGK's stage tracker took the drivers' printed command line
   for a stage. It is SGK's tracker, and the text changes with the command (item 4); nothing for
   this package.
7. **The script names SGK's frozen `a45aefc` in its constants** (`BASELINE`), and reads it for every
   client. The fates need the signatures before the move, which only SGK has. A client that has
   deleted `RunRegistry/` still has `a45aefc` in its history, so a re-measurement after adoption
   works (item 9 of each checklist asks for one).

Nothing is opened: no defect of the package was found. The U20 sentence is corrected here, and every
other difference between a client and `v0.1.0` is the client's to act on, by its checklist.

## State handed to the next prompt

- `docs/adoption/` holds the README, three checklists and `measure_client_registry.py`.
  **E2 is `v0.1.0` (tag object `fd5ce48`, `9f8ebe4`) with `docs/adoption/secondarygwkit.md`**, at
  `aaab408`; it is to be reported to the user with the tag, its commit and the checklist's path (SGK's
  brief §8, `:155`).
- `README.md`'s "Using it" distinguishes the record root from the directory whose config governs.
- No file under `runregistrykit/` changed. `git diff 9f8ebe4 -- runregistrykit pyproject.toml` is
  empty, so the package is `v0.1.0`'s. The suite is **276**, `Ran 276 tests in 85.730s … OK`.
- Open issues: **2** (`[00-the-shard-fixtures-reach-into-shardedpool]` and
  `[00-a-refusal-matches-datastorekit-message-text]`, owner none). Their package lines are 06's,
  unchanged.
- G2-G4 are open, each with its checklist; 08 writes the verification document and closes the
  campaign.
- **No tag made; nothing pushed.**

---

## The script's output, whole

Each as printed by `./venv/bin/python docs/adoption/measure_client_registry.py <client>` from this
repository's root, at this commit. Each run twice, `cmp` identical; each equal to its checklist's
appendix.

### Measured: SecondaryGWKit (SGK) at `14bcac0`

- Repository `/Users/ds283/Documents/Code/SecondaryGWKit`, commit `14bcac0eb73069131f8ce4f55d91e5fc3e7318cf`, 2026-10-14, “Say in the runregistry-extraction plan what 08 repeats of W1”.
- Read through `git` only: 428 tracked `.py` files parsed with `ast`.
- Against `runregistrykit` 0.1.0 and `datastorekit` 0.4.0 as installed; signatures before the move from SecondaryGWKit a45aefc.
- `requirements.txt`: `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0` (`:17`); `ray==2.43.0` (`:75`); `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0` (`:76`); `SQLAlchemy==2.0.39` (`:87`).

| Figure | Live code | Staying tests |
|---|---|---|
| Import statements | 13 | 12 |
| … at module level | 4 | 12 |
| Files importing it | 10 | 5 |
| Names used | 15 | 26 |
| Calls bound | 12 | 8 |
| … binding | 8 | 6 |
| … not binding: the move's new `fingerprint_format` only | 4 | 2 |
| … not binding for any other reason | 0 | 0 |
| Name-alike calls, not the registry's | 26 | 0 |
| String literals naming it | 18 | 6 |
| … holding `-m RunRegistry` | 3 | 1 |

Campaign records: **6** `.py` files import it, 7 name it.

#### 1. Imports: live code

| File | Line | Scope | Statement |
|---|---|---|---|
| `ObjectFactories/tests/test_quadsource_policy_key.py` | 411 | `TestTheInventoryIdentityIncludesIt.test_the_fingerprint_moves_with_the_policy` | `from RunRegistry.stores import fingerprint_of` |
| `docs/a3-v2-readiness/fingerprint_time_probe.py` | 83 | `main` | `from RunRegistry.stores import FINGERPRINT_FORMAT, fingerprint_store` |
| `docs/a3-v2-readiness/sigterm_handler_probe.py` | 150 | `child` | `import RunRegistry` |
| `docs/a3-v2-readiness/sigterm_handler_probe.py` | 151 | `child` | `import RunRegistry.stores as registry_stores` |
| `docs/datastore-integrity-verification/compare_stores.py` | 21 | `module` | `from RunRegistry.stores import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_store` |
| `docs/datastore-integrity-verification/interrupt_when.py` | 61 | `module` | `import RunRegistry` |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py` | 29 | `module` | `from RunRegistry.stores import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_store` |
| `docs/dk-and-rpk-migration/rehearsal/stage_counts.py` | 26 | `module` | `import RunRegistry` |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 526 | `register` | `import RunRegistry` |
| `docs/handover/quadsource_atol_sweep.py` | 554 | `run_build` | `import RunRegistry` |
| `docs/handover/quadsource_atol_sweep.py` | 760 | `prepare` | `import RunRegistry.stores` |
| `docs/handover/quadsource_atol_sweep.py` | 862 | `sweep` | `import RunRegistry` |
| `docs/runregistry-extraction/fingerprint_both_ways.py` | 110 | `check_store` | `from RunRegistry import stores as sgk_stores` |

#### 2–3. Names and their fates at `v0.1.0`: live code

| Name | Fate | At `v0.1.0` | Sites |
|---|---|---|---|
| `RunRegistry.DEFAULT_STALE_AFTER` | kept | runregistrykit.DEFAULT_STALE_AFTER | `docs/datastore-integrity-verification/interrupt_when.py:230` (used) |
| `RunRegistry.TERMINAL_STATES` | kept | runregistrykit.TERMINAL_STATES | `docs/datastore-integrity-verification/interrupt_when.py:165` (used) |
| `RunRegistry._slug` | renamed (private) | runregistrykit.slugify(text); U11; at a45aefc (text) | `docs/dk-and-rpk-migration/rehearsal/stage_counts.py:37` (used), `docs/dk-and-rpk-migration/rehearsal/stage_counts.py:38` (used) |
| `RunRegistry.begin` | kept | runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=); at a45aefc (campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=) | `docs/a3-v2-readiness/sigterm_handler_probe.py:159` (used), `docs/gktk-remedial/scoped_pipeline_run.py:541` (used), `docs/handover/quadsource_atol_sweep.py:556` (used), `docs/handover/quadsource_atol_sweep.py:864` (used) |
| `RunRegistry.liveness` | kept | runregistrykit.liveness(status, stale_after, now=), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:175` (used) |
| `RunRegistry.now_iso` | kept | runregistrykit.now_iso(), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:68` (used) |
| `RunRegistry.pid_alive` | kept | runregistrykit.pid_alive(pid), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:170` (used), `docs/datastore-integrity-verification/interrupt_when.py:190` (used) |
| `RunRegistry.read_json` | kept | runregistrykit.read_json(path), the same parameters as at a45aefc | `docs/datastore-integrity-verification/interrupt_when.py:87` (used), `docs/datastore-integrity-verification/interrupt_when.py:101` (used), `docs/datastore-integrity-verification/interrupt_when.py:161` (used) |
| `RunRegistry.stores.FINGERPRINT_FORMAT` | deleted | C7: the format is the client's, in its fingerprinter's module | `docs/a3-v2-readiness/fingerprint_time_probe.py:83` (imported), `docs/a3-v2-readiness/fingerprint_time_probe.py:86` (used), `docs/datastore-integrity-verification/compare_stores.py:21` (imported), `docs/datastore-integrity-verification/compare_stores.py:48` (used), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:29` (imported), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:71` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:128` (used) |
| `RunRegistry.stores.compare_fingerprints` | moved | datastorekit.store_fingerprint.compare_fingerprints(recorded, current); layer C, DatastoreKit's since v0.4.0; at a45aefc (recorded, current) | `docs/datastore-integrity-verification/compare_stores.py:21` (imported), `docs/datastore-integrity-verification/compare_stores.py:51` (used), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:29` (imported), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:80` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:227` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:247` (used) |
| `RunRegistry.stores.copy_store` | kept | runregistrykit.stores.copy_store(src, dst, purpose, runs_root=, *, client_root=); at a45aefc (src, dst, purpose, runs_root=) | `docs/handover/quadsource_atol_sweep.py:763` (used) |
| `RunRegistry.stores.fingerprint_of` | moved | datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=); layer C, DatastoreKit's since v0.4.0; at a45aefc (inventory, taken=) | `ObjectFactories/tests/test_quadsource_policy_key.py:411` (imported), `ObjectFactories/tests/test_quadsource_policy_key.py:413` (used), `ObjectFactories/tests/test_quadsource_policy_key.py:416` (used), `ObjectFactories/tests/test_quadsource_policy_key.py:419` (used), `docs/runregistry-extraction/fingerprint_both_ways.py:127` (used) |
| `RunRegistry.stores.fingerprint_store` | kept | runregistrykit.stores.fingerprint_store(primary, *, write=, runs_root=, taken_by=, client_root=); at a45aefc (primary, *, write=, runs_root=, taken_by=) | `docs/a3-v2-readiness/fingerprint_time_probe.py:83` (imported), `docs/a3-v2-readiness/fingerprint_time_probe.py:93` (used), `docs/a3-v2-readiness/sigterm_handler_probe.py:187` (used), `docs/a3-v2-readiness/sigterm_handler_probe.py:210` (assigned), `docs/datastore-integrity-verification/compare_stores.py:21` (imported), `docs/datastore-integrity-verification/compare_stores.py:32` (used), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:29` (imported), `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:64` (used) |
| `RunRegistry.stores.listing_lines` | moved | datastorekit.store_fingerprint.listing_lines(inventory, fingerprint); layer C, DatastoreKit's since v0.4.0; at a45aefc (inventory, fingerprint) | `docs/runregistry-extraction/fingerprint_both_ways.py:203` (used) |
| `RunRegistry.stores.read_sidecar` | kept | runregistrykit.stores.read_sidecar(primary, *, client_root=); at a45aefc (primary) | `docs/runregistry-extraction/fingerprint_both_ways.py:240` (used) |

#### 4. Calls: live code

| File:line | Call | Positional | Keywords | Unpacking | Verdict |
|---|---|---|---|---|---|
| `ObjectFactories/tests/test_quadsource_policy_key.py:413` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `ObjectFactories/tests/test_quadsource_policy_key.py:416` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `ObjectFactories/tests/test_quadsource_policy_key.py:419` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `docs/a3-v2-readiness/fingerprint_time_probe.py:93` | `fingerprint_store` | 1 | write | — | binds |
| `docs/a3-v2-readiness/sigterm_handler_probe.py:159` | `RunRegistry.begin` | 0 | argv, campaign, prompt, purpose, results, root, script, slug | — | binds |
| `docs/datastore-integrity-verification/compare_stores.py:32` | `fingerprint_store` | 1 | write | — | binds |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py:64` | `fingerprint_store` | 1 | write | — | binds |
| `docs/gktk-remedial/scoped_pipeline_run.py:541` | `RunRegistry.begin` | 0 | campaign, heartbeat_means, prompt, purpose, results, scope, script, slug | — | binds |
| `docs/handover/quadsource_atol_sweep.py:556` | `RunRegistry.begin` | 0 | campaign, heartbeat_means, prompt, purpose, results, scope, script, slug | — | binds |
| `docs/handover/quadsource_atol_sweep.py:763` | `RunRegistry.stores.copy_store` | 2 | purpose | — | binds |
| `docs/handover/quadsource_atol_sweep.py:864` | `RunRegistry.begin` | 0 | campaign, heartbeat_means, prompt, purpose, results, scope, script, slug | — | binds |
| `docs/runregistry-extraction/fingerprint_both_ways.py:127` | `sgk_stores.fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |

Bound against `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=)`; `runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=)`; `runregistrykit.stores.copy_store(src, dst, purpose, runs_root=, *, client_root=)`; `runregistrykit.stores.fingerprint_store(primary, *, write=, runs_root=, taken_by=, client_root=)`.

Not the registry's (their callee does not resolve to it), so not bound:

- `ObjectFactories/tests/test_quadsource_parent_key.py:445` `engine.begin(…)`, in `TestCrossShardParentUnit._read`
- `ObjectFactories/tests/test_wkb_numeric_parent_key.py:983` `engine.begin(…)`, in `TestNullableParent._read`
- `StoreFixtures/real_store_fixtures.py:229` `pool._engine.begin(…)`, in `_write_primary`
- `StoreFixtures/real_store_fixtures.py:270` `engine.begin(…)`, in `_write_shard`
- `StoreFixtures/real_store_fixtures.py:1159` `engine.begin(…)`, in `_write_full_shard`
- `docs/a3-v2-readiness/reader_writes_probe.py:772` `copy_store(…)`, in `main`
- `docs/a3-v2-readiness/reader_writes_probe.py:830` `copy_store(…)`, in `main`
- `docs/a3-v2-readiness/reader_writes_probe.py:881` `copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:203` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:209` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:223` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:231` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:239` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:248` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:282` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:316` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:362` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:393` `rw.copy_store(…)`, in `main`
- `docs/a3-v2-readiness/readonly_open_probe.py:407` `rw.copy_store(…)`, in `main`
- `docs/datastore-generic-audit/str_e_misfire_probe.py:45` `engine.begin(…)`, in `module`
- `docs/datastore-integrity-verification/fault_copies.py:137` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:141` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:148` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:166` `copy_store(…)`, in `main`
- `docs/datastore-integrity-verification/fault_copies.py:178` `copy_store(…)`, in `main`
- `docs/runregistry-extraction/fingerprint_both_ways.py:128` `package.fingerprint_of(…)`, in `check_store`

#### 5. String literals naming `RunRegistry`: live code

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `docs/a3-v2-readiness/fingerprint_time_probe.py` | 1 |  | S4 (a3-v2-readiness audit 00): how long the fingerprint that ``Run.finish(..., fingerprint=True)`` t |
| `docs/a3-v2-readiness/fingerprint_time_probe.py` | 85 |  | import RunRegistry.stores: s |
| `docs/a3-v2-readiness/sigterm_handler_probe.py` | 1 |  | a3-v2-readiness prompt 04: a SIGTERM to a pipeline driver blocked in ``ray.wait`` is recorded ``kill |
| `docs/datastore-integrity-verification/interrupt_when.py` | 1 |  | Send one SIGTERM to a registered pipeline run once it reaches a chosen point in a chosen stage. Writ |
| `docs/datastore-integrity-verification/interrupt_when.py` | 96 |  | The basename of the run's own driver, from its manifest's `argv[0]`, or `None`. `RunRegistry.begin`  |
| `docs/dk-and-rpk-migration/rehearsal/compare_with_recorded.py` | 1 |  | Compare closed stores' fingerprints with fingerprints recorded by earlier runs. PYTHONPATH=. ./venv/ |
| `docs/dk-and-rpk-migration/rehearsal/stage_counts.py` | 31 |  | The slug `RunRegistry.run_id` was given, recovered from the manifest's own fields. |
| `docs/dk-and-rpk-migration/rehearsal/store_soundness.py` | 1 |  | Integrity, foreign keys, version rows and the inventory of each closed store. PYTHONPATH=. ./venv/bi |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 1 |  | Run main.py's pipeline on a scoped wavenumber sample, against a locally bootstrapped Ray instance an |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 529 |  | scoped_pipeline_run: --register needs RunRegistry on the path; run this script from the repository r |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 578 | **`:580`** | ** scoped_pipeline_run: registered as ** manifest ** list it with: PYTHONPATH=. ./venv/bin/python -m |
| `docs/gktk-remedial/scoped_pipeline_run.py` | 611 |  | record this run in var/runs/ through RunRegistry, under this slug. Without it nothing is registered  |
| `docs/handover/quadsource_atol_sweep.py` | 412 |  | `main.py`'s argv for either driver, `sys.argv` form (the program name first). `zend` is `--zend`'s v |
| `docs/handover/quadsource_atol_sweep.py` | 593 | **`:595`** | ** quadsource_atol_sweep --build: registered as ** manifest ** list it with: PYTHONPATH=. ./venv/bin |
| `docs/handover/quadsource_atol_sweep.py` | 740 |  | Make the sweep store from the baseline through one registry copy. `RunRegistry.stores.copy_store` co |
| `docs/handover/quadsource_atol_sweep.py` | 752 |  | quadsource_atol_sweep --prepare: --force no longer means "replace". RunRegistry.stores.copy_store ne |
| `docs/handover/quadsource_atol_sweep.py` | 904 | **`:906`** | ** quadsource_atol_sweep: registered as ** manifest ** list it with: PYTHONPATH=. ./venv/bin/python  |
| `docs/runregistry-extraction/fingerprint_both_ways.py` | 1 |  | The fingerprint both ways (runregistry-extraction prompt 04, W1; README §6.2 C3; 08 runs it again).  |

#### 1. Imports: the staying tests

| File | Line | Scope | Statement |
|---|---|---|---|
| `RunRegistry/tests/test_build_rehearsal_scope.py` | 39 | `module` | `from RunRegistry.tests.test_prune_on_resume import parsed_arguments` |
| `RunRegistry/tests/test_killed_handler.py` | 26 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_killed_handler.py` | 27 | `module` | `from RunRegistry.tests.test_pipeline_adoption import DRIVER, REPO_ROOT, load_driver` |
| `RunRegistry/tests/test_pipeline_adoption.py` | 27 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 25 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 26 | `module` | `from RunRegistry import stores` |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 27 | `module` | `from RunRegistry.tests.store_fixtures import StoreTestCase` |
| `RunRegistry/tests/test_store_fingerprint.py` | 33 | `module` | `import RunRegistry` |
| `RunRegistry/tests/test_store_fingerprint.py` | 34 | `module` | `from RunRegistry import stores` |
| `RunRegistry/tests/test_store_fingerprint.py` | 35 | `module` | `from RunRegistry.stores import FINGERPRINT_FORMAT, compare_fingerprints, fingerprint_of, fingerprint_store` |
| `RunRegistry/tests/test_store_fingerprint.py` | 41 | `module` | `from RunRegistry.tests.store_fixtures import StoreTestCase, load, sweep_shaped, write_sidecar_json` |
| `RunRegistry/tests/test_store_fingerprint.py` | 47 | `module` | `from RunRegistry.tests.test_store_command_line import CommandLineTestCase` |

#### 2–3. Names and their fates at `v0.1.0`: the staying tests

| Name | Fate | At `v0.1.0` | Sites |
|---|---|---|---|
| `RunRegistry.DEFAULT_ROOT` | deleted | C2: the runs root is the config's runs_root | `RunRegistry/tests/test_pipeline_adoption.py:278` (used), `RunRegistry/tests/test_pipeline_adoption.py:330` (patched (patch.object)) |
| `RunRegistry.REPO_ROOT` | deleted | C1: the root is the client's, found from its runregistrykit.toml | `RunRegistry/tests/test_store_fingerprint.py:73` (used) |
| `RunRegistry.Run._fingerprint_results` | private | runregistrykit.Run._fingerprint_results present; (self) at a45aefc, (self) at v0.1.0 | `RunRegistry/tests/test_killed_handler.py:333` (patched on an object (patch.object, by name)), `RunRegistry/tests/test_killed_handler.py:432` (patched on an object (patch.object, by name)) |
| `RunRegistry.TERMINAL_STATES` | kept | runregistrykit.TERMINAL_STATES | `RunRegistry/tests/test_pipeline_adoption.py:252` (used) |
| `RunRegistry._repo_path` | private | runregistrykit._repo_path present; (path) at a45aefc, (path, root) at v0.1.0 | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:134` (used) |
| `RunRegistry.begin` | kept | runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=); at a45aefc (campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=) | `RunRegistry/tests/test_killed_handler.py:90` (used), `RunRegistry/tests/test_pipeline_adoption.py:74` (used) |
| `RunRegistry.list_runs` | kept | runregistrykit.list_runs(root=, stale_after=, now=, *, client_root=); at a45aefc (root=, stale_after=, now=) | `RunRegistry/tests/test_pipeline_adoption.py:142` (used) |
| `RunRegistry.read_json` | kept | runregistrykit.read_json(path), the same parameters as at a45aefc | `RunRegistry/tests/test_killed_handler.py:186` (used), `RunRegistry/tests/test_killed_handler.py:336` (used), `RunRegistry/tests/test_killed_handler.py:435` (used), `RunRegistry/tests/test_pipeline_adoption.py:179` (used), `RunRegistry/tests/test_pipeline_adoption.py:183` (used), `RunRegistry/tests/test_pipeline_adoption.py:347` (used) |
| `RunRegistry.stores.DEFAULT_ROOT` | deleted | C2: the runs root is the config's runs_root | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:73` (patched (patch.object)) |
| `RunRegistry.stores.FINGERPRINT_FORMAT` | deleted | C7: the format is the client's, in its fingerprinter's module | `RunRegistry/tests/test_store_fingerprint.py:35` (imported), `RunRegistry/tests/test_store_fingerprint.py:352` (used) |
| `RunRegistry.stores._fingerprint_problems` | private | runregistrykit.stores._fingerprint_problems present; (value) at a45aefc, (value) at v0.1.0 | `RunRegistry/tests/test_store_fingerprint.py:374` (used) |
| `RunRegistry.stores.compare_fingerprints` | moved | datastorekit.store_fingerprint.compare_fingerprints(recorded, current); layer C, DatastoreKit's since v0.4.0; at a45aefc (recorded, current) | `RunRegistry/tests/test_store_fingerprint.py:35` (imported), `RunRegistry/tests/test_store_fingerprint.py:381` (used) |
| `RunRegistry.stores.create_sidecar` | kept | runregistrykit.stores.create_sidecar(primary, purpose, *, client_root=); at a45aefc (primary, purpose) | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:87` (used), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:96` (used), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:105` (used) |
| `RunRegistry.stores.fingerprint_of` | moved | datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=); layer C, DatastoreKit's since v0.4.0; at a45aefc (inventory, taken=) | `RunRegistry/tests/test_store_fingerprint.py:35` (imported), `RunRegistry/tests/test_store_fingerprint.py:147` (used), `RunRegistry/tests/test_store_fingerprint.py:162` (used), `RunRegistry/tests/test_store_fingerprint.py:378` (used) |
| `RunRegistry.stores.fingerprint_store` | kept | runregistrykit.stores.fingerprint_store(primary, *, write=, runs_root=, taken_by=, client_root=); at a45aefc (primary, *, write=, runs_root=, taken_by=) | `RunRegistry/tests/test_store_fingerprint.py:35` (imported) |
| `RunRegistry.stores.read_sidecar` | kept | runregistrykit.stores.read_sidecar(primary, *, client_root=); at a45aefc (primary) | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:115` (used), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:129` (used) |
| `RunRegistry.stores.sidecar_path` | kept | runregistrykit.stores.sidecar_path(primary), the same parameters as at a45aefc | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:101` (used) |
| `RunRegistry.tests.store_fixtures.StoreTestCase` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:27` (imported), `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:61` (used), `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.store_fixtures.load` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.store_fixtures.sweep_shaped` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.store_fixtures.write_sidecar_json` | not shipped | RunRegistry.tests.store_fixtures is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:41` (imported) |
| `RunRegistry.tests.test_pipeline_adoption.DRIVER` | the client's own | RunRegistry.tests.test_pipeline_adoption is a staying test module, which moves with the tests | `RunRegistry/tests/test_killed_handler.py:27` (imported), `RunRegistry/tests/test_killed_handler.py:479` (used), `RunRegistry/tests/test_killed_handler.py:559` (used) |
| `RunRegistry.tests.test_pipeline_adoption.REPO_ROOT` | the client's own | RunRegistry.tests.test_pipeline_adoption is a staying test module, which moves with the tests | `RunRegistry/tests/test_killed_handler.py:27` (imported), `RunRegistry/tests/test_killed_handler.py:29` (used) |
| `RunRegistry.tests.test_pipeline_adoption.load_driver` | the client's own | RunRegistry.tests.test_pipeline_adoption is a staying test module, which moves with the tests | `RunRegistry/tests/test_killed_handler.py:27` (imported), `RunRegistry/tests/test_killed_handler.py:80` (used) |
| `RunRegistry.tests.test_prune_on_resume.parsed_arguments` | the client's own | RunRegistry.tests.test_prune_on_resume is a staying test module, which moves with the tests | `RunRegistry/tests/test_build_rehearsal_scope.py:39` (imported), `RunRegistry/tests/test_build_rehearsal_scope.py:80` (used) |
| `RunRegistry.tests.test_store_command_line.CommandLineTestCase` | not shipped | RunRegistry.tests.test_store_command_line is test support; v0.1.0 ships no runregistrykit.tests (U19), and the client keeps its own copy (U21) | `RunRegistry/tests/test_store_fingerprint.py:47` (imported) |

#### 4. Calls: the staying tests

| File:line | Call | Positional | Keywords | Unpacking | Verdict |
|---|---|---|---|---|---|
| `RunRegistry/tests/test_killed_handler.py:90` | `RunRegistry.begin` | 0 | argv, campaign, prompt, purpose, root, slug | — | binds |
| `RunRegistry/tests/test_pipeline_adoption.py:74` | `RunRegistry.begin` | 0 | campaign, prompt, root, slug | ** | binds (its spelled arguments; the unpacking is not expanded) |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:87` | `stores.create_sidecar` | 2 | — | — | binds |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:96` | `stores.create_sidecar` | 2 | — | — | binds |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:105` | `stores.create_sidecar` | 2 | — | — | binds |
| `RunRegistry/tests/test_store_fingerprint.py:147` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `RunRegistry/tests/test_store_fingerprint.py:162` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `RunRegistry/tests/test_store_fingerprint.py:378` | `fingerprint_of` | 2 | — | — | binds |

Bound against `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=)`; `runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=)`; `runregistrykit.stores.create_sidecar(primary, purpose, *, client_root=)`.

#### 5. String literals naming `RunRegistry`: the staying tests

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `RunRegistry/tests/test_build_rehearsal_scope.py` | 317 |  | RunRegistry.begin |
| `RunRegistry/tests/test_pipeline_adoption.py` | 146 |  | RunRegistry |
| `RunRegistry/tests/test_pipeline_adoption.py` | 158 |  | RunRegistry |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 1 |  | `docs/handover/quadsource_atol_sweep.py` `prepare()` and `assert_store_is_self_consistent()`, for `s |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py` | 62 |  | One temporary directory (`self.top`), a runs root inside it (`self.root`), and a fresh import of the |
| `RunRegistry/tests/test_store_fingerprint.py` | 1 | **`:3`** | The store fingerprint (store-fingerprint prompt 04): `RunRegistry.stores.fingerprint_of`, `compare_f |

#### 1. Campaign records

Importing it: `prompts/datastore-generic/orchestrator/measure-05/scripts/m4_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-06/scripts/m1_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-07/scripts/m1_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-08/scripts/m1_fingerprint.py` (1), `prompts/datastore-generic/orchestrator/measure-08/scripts/m4b_order_matters.py` (1), `prompts/datastore-generic/orchestrator/measure-09/scripts/m4_inventory.py` (1).

Naming it without importing it: `prompts/datastore-generic/orchestrator/measure-08/scripts/phaseB_edit_tests.py`.

#### 6. `installed_package_provenance`

Not defined.

#### 7. Tracked files other than `.py` matching `RunRegistry|run registry|runregistrykit`

Lines by top directory: `CLAUDE.md` 10, `docs` 158, `prompts` 2078.

Outside the campaign records (text squeezed, first 110 characters):

| File | Line | Text |
|---|---|---|
| `CLAUDE.md` | 77 | ## Long-running jobs — the run registry |
| `CLAUDE.md` | 79 | A job that takes hours must not be something a conversation owns. `RunRegistry/` records that one |
| `CLAUDE.md` | 87 | 1. **Discovery.** Run `python -m RunRegistry list` at the start of a session and before launching |
| `CLAUDE.md` | 106 | ## `RunRegistry/` is frozen — it is moving to RunRegistryKit |
| `CLAUDE.md` | 108 | Since prompt 01 of `runregistry-extraction` (`a45aefc`), `RunRegistry/` is frozen: RunRegistryKit |
| `CLAUDE.md` | 111 | `RunRegistry/` and nothing else. |
| `CLAUDE.md` | 113 | - **Nothing under `RunRegistry/` changes**, its tests included, until |
| `CLAUDE.md` | 114 | `prompts/runregistry-extraction` prompt 06 replaces it with the pinned `runregistrykit`. |
| `CLAUDE.md` | 116 | is fixed in RunRegistryKit, not here. If a fix cannot wait, stop and ask the user. |
| `CLAUDE.md` | 144 | PYTHONPATH=. ./venv/bin/python -m unittest discover -s RunRegistry/tests -t . |
| `docs/OPEN_ISSUES.md` | 661 | ### 1.11 The run registry campaign |
| `docs/OPEN_ISSUES.md` | 666 | was exercised for the first time and crashed. Prompt 01 landed the `RunRegistry/` package, the |
| `docs/OPEN_ISSUES.md` | 692 | Prompt 03 landed the same day: `RunRegistry/stores.py` owns the store sidecar, and `python -m RunRegistry stor |
| `docs/OPEN_ISSUES.md` | 746 | \| `[01-cross-filesystem-move-advice-says-delete-by-hand]` \| store-retirement \| **Narrowed 2026-10-12** by dk-a |
| `docs/OPEN_ISSUES.md` | 838 | \| `[04-a-signal-inside-a-heartbeat-write-can-leave-status-json-unparseable]` \| a3-v2-readiness \| A handler's ` |
| `docs/OPEN_ISSUES.md` | 893 | `RunRegistry/` moves to a repository of its own, RunRegistryKit, before the A3 v2 compute run, with |
| `docs/a3-v2-readiness-audit.md` | 7 | baseline, `mode=ro`, through `RunRegistry.stores.fingerprint_store(..., write=False)`, with the |
| `docs/a3-v2-readiness-audit.md` | 293 | - **The read.** `RunRegistry.stores.fingerprint_store(primary, write=False)` on |
| `docs/a3-v2-readiness-audit.md` | 295 | `RunRegistry.begin`, no `store` subcommand, no `ShardedPool`. The five store files and the sidecar |
| `docs/a3-v2-readiness-verification.md` | 75 | `running` with a pid answering `kill -0`, and that `RunRegistry list` showed it, and ended its turn. |
| `docs/a3-v2-readiness-verification.md` | 162 | - `python -m RunRegistry list` showed nothing `running`: 12 runs before `reference` (10 finished, |
| `docs/a3-v2-readiness-verification.md` | 209 | interrupter's from `RunRegistry.now_iso()`. Equal stamps bound the delay below 1 s; they do not |
| `docs/a3-v2-readiness-verification.md` | 309 | appeared. The refusal is raised before `RunRegistry.begin` and `ray.init`. |
| `docs/a3-v2-readiness-verification.md` | 638 | **Before the first run** (10:23–10:31): `python -m RunRegistry list` showed 16 runs, none |
| `docs/a3-v2-readiness-verification.md` | 722 | - [ ] **The pre-launch checks**, on that machine (§1.3): `RunRegistry list` shows nothing `running` |
| `docs/a3-v2-readiness-verification.md` | 728 | with a pid answering `kill -0`, and `RunRegistry list`. |
| `docs/a3-v2-readiness-verification.md` | 845 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/a3-v2-readiness-verification.md` | 847 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint --write \ |
| `docs/a3-v2-readiness-verification.md` | 849 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/a3-v2-readiness/fingerprint_time_probe.txt` | 15 | import RunRegistry.stores: 0.017 s |
| `docs/a3-v2-readiness/interrupter_build_dummy_test.sh` | 6 | # `argv[0]` is `docs/handover/quadsource_atol_sweep.py` (`RunRegistry.begin` records `sys.argv` |
| `docs/a3-v2-readiness/rehearsal/interrupter_firings.txt` | 3 | 2026-10-04T01:44:41+01:00 liveness alive; pid 41825; stage 'list it with: PYTHONPATH=. ./venv/bin/python -m Ru |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 9 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 48 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 88 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/a3-v2-readiness/rehearsal/prelaunch_checks.txt` | 129 | --- PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/datastore-generic-audit.md` | 183 | `RunRegistry.stores.copy_store`. **Keep** `_require_bare_name` and the "both resolve to one file" |
| `docs/datastore-generic-audit.md` | 230 | `RunRegistry/` has fallbacks for legacy store **sidecars** (no `sidecar_format`; `adopt_sidecar` is |
| `docs/datastore-generic-audit.md` | 233 | not stores; the registry never deletes a record, and `python -m RunRegistry list` lists the old run |
| `docs/datastore-integrity-audit.md` | 135 | design. `RunRegistry/tests/test_store_fingerprint.py:60` pins `full_store_fingerprint.json`. Every |
| `docs/datastore-integrity-audit.md` | 309 | **[probed]** Nothing was `running` (`python -m RunRegistry list`), no journal was present, and the |
| `docs/datastore-integrity-verification.md` | 64 | `PYTHONPATH=.` is not in the prompt's §1.3 command; the driver's `register()` imports `RunRegistry`, |
| `docs/datastore-integrity-verification.md` | 68 | Before each launch: `python -m RunRegistry list` showed nothing `running`; `ray status` found no |
| `docs/datastore-integrity-verification.md` | 71 | `status.json` says `running` with a pid answering `kill -0`, `RunRegistry list` shows the run), and |
| `docs/datastore-integrity-verification.md` | 169 | a person, `RunRegistry.Run(…).finish('killed', exit_code=None)`, after `kill -0 6384` failed: |
| `docs/datastore-integrity-verification.md` | 466 | - [ ] **`RunRegistry list` clean** — nothing `running`, nothing stale (§1.1, before every launch). |
| `docs/datastore-integrity-verification.md` | 546 | PYTHONPATH=. ./venv/bin/python -m RunRegistry list |
| `docs/datastore-integrity-verification.md` | 547 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store show var/datastores/datastore-integrity-10-<store>.sqlite |
| `docs/datastore-integrity-verification.md` | 549 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" var/datastores/datastore-int |
| `docs/datastore-integrity-verification.md` | 550 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint [--write] var/datastores/datastore-integrity-1 |
| `docs/datastore-integrity-verification.md` | 556 | PYTHONPATH=. ./venv/bin/python -c "import RunRegistry; RunRegistry.Run('var/runs/datastore-integrity-10-resume |
| `docs/datastore-integrity-verification/interrupter_firings.txt` | 3 | 2026-10-01T21:03:02+01:00 liveness alive; pid 1238; stage 'list it with: PYTHONPATH=. ./venv/bin/python -m Run |
| `docs/datastore-integrity-verification/interrupter_firings.txt` | 12 | 2026-10-01T23:08:13+01:00 liveness alive; pid 6384; stage 'list it with: PYTHONPATH=. ./venv/bin/python -m Run |
| `docs/dk-and-rpk-migration-verification.md` | 87 | answering `kill -0`, and that `RunRegistry list` showed it, and ended its turn. The orchestrator ran |
| `docs/dk-and-rpk-migration-verification.md` | 108 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/dk-and-rpk-migration-verification.md` | 110 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint --write \ |
| `docs/dk-and-rpk-migration-verification.md` | 112 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/dk-and-rpk-migration-verification.md` | 123 | - `python -m RunRegistry list` showed nothing `running`: 17 runs before `reference` (15 finished, 2 |
| `docs/dk-and-rpk-migration-verification.md` | 241 | interrupter's from `RunRegistry.now_iso()`. They bound the delay; they do not measure it. In |
| `docs/dk-and-rpk-migration-verification.md` | 516 | `RunRegistry.stores.fingerprint_store` does, and it reads the shards from the primary's `shards` |
| `docs/dk-and-rpk-migration-verification.md` | 716 | \| RunRegistry \| 286 \| OK \| 20.5 \| |
| `docs/dk-and-rpk-migration-verification.md` | 821 | - `RunRegistry list` showed the run. |
| `docs/dk-and-rpk-migration-verification.md` | 856 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: 21 runs before |
| `docs/dk-and-rpk-migration-verification.md` | 871 | - `RunRegistry.package_provenance()` gave the record above. |
| `docs/dk-and-rpk-migration-verification.md` | 1563 | \| RunRegistry \| 286 \| OK \| 40.5 \| |
| `docs/dk-and-rpk-migration-verification.md` | 1616 | \| 3 \| The six roots pass \| This prompt's suites at `6861a9f`, whose code is `0c9e2cf`'s: Datastore 320, RunReg |
| `docs/dk-and-rpk-migration-verification.md` | 1629 | comment in `RunRegistry/tests/test_pipeline_adoption.py`, and that file's `ast` is equal at the two |
| `docs/dk-and-rpk-migration-verification.md` | 1724 | - `RunRegistry list` showed the run. |
| `docs/dk-and-rpk-migration-verification.md` | 1761 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: 25 runs before |
| `docs/dk-and-rpk-migration-verification.md` | 1783 | - `RunRegistry.package_provenance()` gave the record above. |
| `docs/dk-and-rpk-migration-verification.md` | 2550 | \| RunRegistry \| 286 \| OK \| 19.8 \| |
| `docs/dk-and-rpk-migration-verification.md` | 2606 | \| 4 \| The six roots pass \| This prompt's suites at `5631f0e`, whose code is `643c3b2`'s but for one test comme |
| `docs/dk-and-rpk-migration-verification.md` | 2807 | \| RunRegistry \| 286 \| 286 \| OK \| 54.4 \| |
| `docs/dk-and-rpk-migration-verification.md` | 2822 | `pip check` reports no broken requirements. `RunRegistry.package_provenance()`, saved as |
| `docs/dk-and-rpk-migration-verification.md` | 2845 | at `:2704`); `RunRegistry.stores.move_store` (`RunRegistry/stores.py:1109-1123`) relays it through |
| `docs/dk-and-rpk-migration-verification.md` | 2861 | exactly the board's, and **0 after**. `import RunRegistry.stores` in a fresh `python -I` still loads neither |
| `docs/dk-and-rpk-migration-verification.md` | 2862 | `ray`, `sqlalchemy` nor `datastorekit.store_inventory` (`RunRegistry/stores.py:114`). |
| `docs/dk-and-rpk-migration-verification.md` | 2895 | \| **G2**: SGK adopted `v0.2.2` or later (U37; `actor-names` U3; `factory-defaults` U5), fingerprint reproduced |
| `docs/dk-and-rpk-migration-verification.md` | 2913 | \| **G2** \| **holds** 2026-10-12: SGK adopted `v0.2.0`, and its five parts of the checklist's item 8 hold. (1)  |
| `docs/dk-and-rpk-migration/rehearsal/prelaunch_checks_08.txt` | 127 | RunRegistry/tests/test_pipeline_adoption.py \| 9 +++++---- |
| `docs/dk-and-rpk-migration/rehearsal/prelaunch_checks_08.txt` | 131 | -- correction 1: ast of RunRegistry/tests/test_pipeline_adoption.py at 643c3b2 vs HEAD |
| `docs/runregistry-extraction-audit.md` | 1 | # RunRegistry extraction audit — moving the run registry into a package of its own |
| `docs/runregistry-extraction-audit.md` | 9 | **Why it exists.** `RunRegistry/` was built here, for this repository's long jobs |
| `docs/runregistry-extraction-audit.md` | 11 | both of their `dk-and-rpk-migration` plans record that they have "no run registry and no |
| `docs/runregistry-extraction-audit.md` | 16 | audit records the decisions taken on 2026-10-12, measures what in `RunRegistry/` belongs to this |
| `docs/runregistry-extraction-audit.md` | 30 | \| **D1** — where it goes \| **A repository of its own, `RunRegistryKit`** (package `runregistrykit`), beside Da |
| `docs/runregistry-extraction-audit.md` | 32 | \| **D3** — the fingerprint \| **Split by layer (§3).** The encoding and the digest algorithm go to DatastoreKit |
| `docs/runregistry-extraction-audit.md` | 33 | \| **D4** — a client with no fingerprinter \| **None is supported.** The store layer requires a fingerprinter. T |
| `docs/runregistry-extraction-audit.md` | 45 | ## 1. What `RunRegistry/` is today |
| `docs/runregistry-extraction-audit.md` | 47 | Measured at `d03a643`. `python -m RunRegistry list` reports 29 runs, 27 finished and 2 `unknown` |
| `docs/runregistry-extraction-audit.md` | 52 | \| `RunRegistry/__init__.py` \| 710 \| none at module scope; `RunRegistry.stores` lazily, for `Run.finish(fingerp |
| `docs/runregistry-extraction-audit.md` | 53 | \| `RunRegistry/stores.py` \| 2185 \| `datastorekit.SQL.ShardedPool` (×3) and `datastorekit.store_inventory` (×3) |
| `docs/runregistry-extraction-audit.md` | 54 | \| `RunRegistry/__main__.py` \| 515 \| none \| the CLI: `list` and the `store` subcommands \| |
| `docs/runregistry-extraction-audit.md` | 65 | `import RunRegistry` loads neither `ray` nor `sqlalchemy` (the docstring of `fingerprint_store`, |
| `docs/runregistry-extraction-audit.md` | 101 | \| C5 \| `RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")`, `:119` \| the packages SGK's `dk-and-rpk-migr |
| `docs/runregistry-extraction-audit.md` | 107 | **A hazard C1 already has here.** `REPO_ROOT` follows whichever copy of `RunRegistry/` was imported. |
| `docs/runregistry-extraction-audit.md` | 116 | **`main.py` does not.** It contains no reference to the registry (`grep -ci RunRegistry main.py` is |
| `docs/runregistry-extraction-audit.md` | 124 | \| `ObjectFactories/tests/test_quadsource_policy_key.py:411` \| `from RunRegistry.stores import fingerprint_of`  |
| `docs/runregistry-extraction-audit.md` | 125 | \| `docs/a3-v2-readiness/{sigterm_handler_probe,fingerprint_time_probe}.py`, `docs/datastore-integrity-verifica |
| `docs/runregistry-extraction-audit.md` | 144 | \| **C. Fingerprint** \| SHA-256 over each class's canonical record lines, newline-terminated; the same per dist |
| `docs/runregistry-extraction-audit.md` | 183 | \| when and where a fingerprint is taken and recorded \| **RunRegistryKit**: refused while a `running` run names |
| `docs/runregistry-extraction-audit.md` | 185 | RunRegistryKit reads a fingerprint only through `fingerprint_format`, `digest`, and the list of |
| `docs/runregistry-extraction-audit.md` | 194 | DatastoreKit's own subject; the sidecar is only where RunRegistryKit records it. |
| `docs/runregistry-extraction-audit.md` | 224 | in `RunRegistry/tests/data/` stops matching, and the author then bumps by hand. With layer A and its |
| `docs/runregistry-extraction-audit.md` | 237 | `RunRegistry/tests/` holds 286 tests in 14 modules **[agent; the per-module counts sum to the |
| `docs/runregistry-extraction-audit.md` | 250 | into RunRegistryKit's tests as it is. |
| `docs/runregistry-extraction-audit.md` | 253 | build a full SGK store from it and fingerprint it, through `stores.py:1494`. In RunRegistryKit |
| `docs/runregistry-extraction-audit.md` | 256 | no client, so the DatastoreKit release of §6 may offer such a fixture; if not, RunRegistryKit |
| `docs/runregistry-extraction-audit.md` | 260 | `RunRegistry/tests/` only because that is where registry adoption was tested. They need a test |
| `docs/runregistry-extraction-audit.md` | 261 | root of their own when `RunRegistry/` is deleted (§8, Q6). `RunRegistry/tests/data/` holds six |
| `docs/runregistry-extraction-audit.md` | 274 | ## 5. RunRegistryKit |
| `docs/runregistry-extraction-audit.md` | 279 | with setuptools, `requires-python = ">=3.12"`, the package found by `include = ["runregistrykit*"]` |
| `docs/runregistry-extraction-audit.md` | 295 | Which file — a `[tool.runregistrykit]` table in a `pyproject.toml`, or a file of its own — is §8 Q2. |
| `docs/runregistry-extraction-audit.md` | 302 | `runregistrykit[stores]`, needing `datastorekit` **by name and minimum version, not by git URL**. |
| `docs/runregistry-extraction-audit.md` | 304 | (`requirements.txt:17` here). A git-URL requirement inside RunRegistryKit would conflict with the |
| `docs/runregistry-extraction-audit.md` | 310 | The six rules in `CLAUDE.md` ("Long-running jobs — the run registry") are as much the product as |
| `docs/runregistry-extraction-audit.md` | 312 | Their full text, with the five failures of §0 that each one answers, moves to RunRegistryKit's |
| `docs/runregistry-extraction-audit.md` | 327 | moved from `RunRegistry/stores.py:1164-1390` into a DatastoreKit module beside |
| `docs/runregistry-extraction-audit.md` | 354 | migration, and both adopt RunRegistryKit after it closes (D4). |
| `docs/runregistry-extraction-audit.md` | 400 | Neither amendment brings RunRegistryKit into those campaigns' scope. |
| `docs/runregistry-extraction-audit.md` | 413 | \| **Q1** — names \| Repository `RunRegistryKit`, distribution and package `runregistrykit`, CLI `python -m runr |
| `docs/runregistry-extraction-audit.md` | 414 | \| **Q2** — the client config \| **A file of its own at the root**, read with the standard library's `tomllib`,  |
| `docs/runregistry-extraction-audit.md` | 417 | \| **Q5** — the spec-digest guard (§3.5) \| **Build it in SGK's adoption**, in the client fingerprint module's t |
| `docs/runregistry-extraction-audit.md` | 430 | from RunRegistryKit; RunRegistryKit's store layer needs it. |
| `docs/runregistry-extraction-audit.md` | 431 | 2. **RunRegistryKit `v0.1.0`: a fresh import** of `RunRegistry/` from a frozen SGK commit, as |
| `docs/runregistry-extraction-audit.md` | 435 | and the rules in its README. **SGK's `RunRegistry/` is frozen from the import commit until SGK |
| `docs/runregistry-extraction-audit.md` | 438 | release of step 1, in a commit of its own; `runregistrykit` is pinned at its tag; SGK's |
| `docs/runregistry-extraction-audit.md` | 440 | live callers of §2.1 are rewritten; the 101 tests get their root; `RunRegistry/` is deleted; |
| `docs/runregistry-extraction-audit.md` | 469 | `RunRegistry._slug` **[agent]**: the rewrite in step 3 should use a public name. |
| `docs/runregistry-extraction-verification.md` | 12 | - §3, R2: through both packages, after the RunRegistryKit swap (prompt 08); |
| `docs/runregistry-extraction-verification.md` | 37 | - `runregistrykit` is not installed. |
| `docs/runregistry-extraction-verification.md` | 132 | - `RunRegistry list` showed the run. |
| `docs/runregistry-extraction-verification.md` | 161 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/runregistry-extraction-verification.md` | 163 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store fingerprint --write \ |
| `docs/runregistry-extraction-verification.md` | 165 | PYTHONPATH=. ./venv/bin/python -m RunRegistry store create --purpose "<one line>" \ |
| `docs/runregistry-extraction-verification.md` | 179 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: |
| `docs/runregistry-extraction-verification.md` | 206 | - `pip show runregistrykit` found nothing. `pip check` was clean. |
| `docs/runregistry-extraction-verification.md` | 207 | - `RunRegistry.package_provenance()` gave the record above. It equals, as JSON, the `packages` of |
| `docs/runregistry-extraction-verification.md` | 216 | - `import runregistrykit` raises `ModuleNotFoundError`; |
| `docs/runregistry-extraction-verification.md` | 1000 | `stage`, not those fields. `RunRegistry list` shows `-` under PROGRESS for each. No field R2 |
| `docs/runregistry-extraction-verification.md` | 1043 | \| RunRegistry \| 286 \| OK \| 29.0 \| |
| `docs/runregistry-extraction-verification.md` | 1076 | - `RunRegistry list` shows 33 runs: 01's 29, and this rehearsal's four, all finished but the two |
| `docs/runregistry-extraction-verification.md` | 1132 | - `runregistrykit` is not installed. |
| `docs/runregistry-extraction-verification.md` | 1232 | - `RunRegistry list` showed the run; |
| `docs/runregistry-extraction-verification.md` | 1276 | - **The registry.** `python -m RunRegistry list` showed nothing `running`: 33 runs before |
| `docs/runregistry-extraction-verification.md` | 1296 | - `pip show runregistrykit` found nothing. `pip check` was clean. |
| `docs/runregistry-extraction-verification.md` | 1297 | - `RunRegistry.package_provenance()` gave the record above, equal as JSON to the expected record, |
| `docs/runregistry-extraction-verification.md` | 1306 | - `import runregistrykit` raises `ModuleNotFoundError`; |
| `docs/runregistry-extraction-verification.md` | 1925 | (`docs/gktk-remedial/scoped_pipeline_run.py`, `RunRegistry/__init__.py` `Run.finish`'s docstring), |
| `docs/runregistry-extraction-verification.md` | 1948 | \| RunRegistry \| 286 \| OK \| 14.2 \| |
| `docs/runregistry-extraction-verification.md` | 1985 | - `RunRegistry list` shows 37 runs: R0's 33 and this rehearsal's four, all finished but the two |
| `docs/runregistry-extraction-verification.md` | 1993 | `config.datastore`), takes `sgk = RunRegistry.stores.fingerprint_of(inventory)` and |
| `docs/runregistry-extraction-verification.md` | 1994 | `pkg = datastorekit.store_fingerprint.fingerprint_of(inventory, RunRegistry.stores.FINGERPRINT_FORMAT)`, |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_02.txt` | 30 | -- pip show datastorekit raypoolkit runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_02.txt` | 53 | WARNING: Package(s) not found: runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_02.txt` | 83 | runregistrykit -> ModuleNotFoundError: No module named 'runregistrykit' |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_04.txt` | 38 | -- pip show datastorekit raypoolkit runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_04.txt` | 47 | WARNING: Package(s) not found: runregistrykit |
| `docs/runregistry-extraction/rehearsal/prelaunch_checks_04.txt` | 73 | runregistrykit -> ModuleNotFoundError: No module named 'runregistrykit' |
| `docs/store-fingerprint-audit.md` | 122 | registry's promise that `import RunRegistry` loads neither `ray` nor `sqlalchemy` |
| `docs/store-fingerprint-audit.md` | 123 | (`RunRegistry/stores.py:45-46`) therefore needs the reader to be imported inside the operation, |
| `docs/store-retirement-audit.md` | 13 | move and fingerprint each go through `RunRegistry.stores` and leave a `history` entry. A plain |
| `docs/store-retirement-audit.md` | 30 | Measured 2026-09-25 at `42d4910`. `RunRegistry list` shows nothing `running`. **[probed]** |
| `docs/store-retirement-audit.md` | 39 | `RunRegistry/stores.py:542-573`). **[probed]** |
| `docs/store-retirement-audit.md` | 95 | that is `None`, and `begin` does not refuse (`RunRegistry/__init__.py:549-553`). **[checked]** Both |
| `docs/store-retirement-audit.md` | 114 | `RunRegistry.stores.copy_store` call". Retirement is that reason. `copy_store` refuses because the |
| `docs/store-retirement-audit.md` | 141 | `RunRegistry/tests/test_store_fingerprint.py` test 12 (`:797-842`), and it counts only `run.finish(` |
| `docs/store-retirement-audit.md` | 165 | - The `RunRegistry/stores.py` docstring (`:47-49`), and the `RunRegistry/__main__.py` docstring |

#### 8. `.gitignore` and the registry

- `.gitignore` ignores `var/`: `:3` `var/`.
- Module-level registry mappings: `factories` at `config/datastore.py:91` (38 keys).
- `def inventory_spec`: 21 in 20 files: `ObjectFactories/BackgroundModel.py:881`, `ObjectFactories/GkNumericIntegration.py:634`, `ObjectFactories/GkSource.py:839`, `ObjectFactories/GkSourcePolicy.py:69`, `ObjectFactories/GkSourcePolicyData.py:177`, `ObjectFactories/GkWKBIntegration.py:960`, `ObjectFactories/LambdaCDM.py:93`, `ObjectFactories/OneLoopIntegral.py:341`, `ObjectFactories/QCD_Cosmology.py:128`, `ObjectFactories/QuadSource.py:542`, `ObjectFactories/QuadSourceIntegral.py:965`, `ObjectFactories/QuadSourcePolicy.py:106`, `ObjectFactories/TkNumericIntegration.py:636`, `ObjectFactories/TkWKBIntegration.py:959`, `ObjectFactories/integration_metadata.py:58`, `ObjectFactories/redshift.py:133`, `ObjectFactories/store_tag.py:47`, `ObjectFactories/tolerance.py:56`, `ObjectFactories/version.py:47`, `ObjectFactories/wavenumber.py:126`, `ObjectFactories/wavenumber.py:385`.
- `Parent(..., types=...)`: `ObjectFactories/BackgroundModel.py:900` (`COSMOLOGY_TYPES`), `ObjectFactories/wavenumber.py:396` (`COSMOLOGY_TYPES`).

### Measured: ChamPBH (CPBH) at `c21cdfb`

- Repository `/Users/ds283/Documents/Code/ChamPBH`, commit `c21cdfb5613a3ed976a91a95431495dc8bfd49c8`, 2026-10-15, “Commit audit document for Jordan-frame normalization”.
- Read through `git` only: 219 tracked `.py` files parsed with `ast`.
- Against `runregistrykit` 0.1.0 and `datastorekit` 0.4.0 as installed; signatures before the move from SecondaryGWKit a45aefc.
- `requirements.txt`: `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0` (`:17`); `ray==2.53.0` (`:79`); `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0` (`:80`); `SQLAlchemy==2.0.46` (`:91`).

| Figure | Live code |
|---|---|
| Import statements | 0 |
| … at module level | 0 |
| Files importing it | 0 |
| Names used | 0 |
| Calls bound | 0 |
| … binding | 0 |
| … not binding: the move's new `fingerprint_format` only | 0 |
| … not binding for any other reason | 0 |
| Name-alike calls, not the registry's | 7 |
| String literals naming it | 1 |
| … holding `-m RunRegistry` | 0 |

Campaign records: **0** `.py` files import it, 0 name it.

#### 1. Imports: live code

None.

#### 2–3. Names and their fates at `v0.1.0`: live code

None.

#### 4. Calls: live code

None.

Not the registry's (their callee does not resolve to it), so not bound:

- `ObjectFactories/tests/test_first_bounce_round_trip.py:161` `store._engine.begin(…)`, in `TestFirstBounceRoundTrip._raw_columns`
- `ObjectFactories/tests/test_fixed_T_values_round_trip.py:90` `store._engine.begin(…)`, in `TestFixedTValuesRoundTrip._raw_columns`
- `ObjectFactories/tests/test_scalarmodel_failure_reason.py:90` `store._engine.begin(…)`, in `_write`
- `ObjectFactories/tests/test_version_keyed_lookups.py:112` `store._engine.begin(…)`, in `_insert`
- `ObjectFactories/tests/test_version_keyed_lookups.py:400` `store._engine.begin(…)`, in `TestVersionKeyedLookups.test_d_keyed_build_without_the_serial_raises`
- `ObjectFactories/tests/test_version_keyed_lookups.py:443` `store_b._engine.begin(…)`, in `TestVersionKeyedLookups.test_e_parameter_tables_are_not_keyed`
- `tools/tests/test_inventory_report.py:100` `store._engine.begin(…)`, in `_InventoryStoreCase.insert`

#### 5. String literals naming `RunRegistry`: live code

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `utilities.py` | 178 |  | What is installed of each named distribution, read from its metadata. Maps each name to `None` when  |

#### 1. Campaign records

None.

#### 6. `installed_package_provenance`

- Defined at `utilities.py:177-229`, arguments `(names=RECORDED_DISTRIBUTIONS)`; the package's `package_provenance(names)`.
- Its body against the package's, docstrings removed (`-` the package's only, `+` the client's only):

  ```
  -    origin = None
  ```
- `RECORDED_DISTRIBUTIONS = ('datastorekit', 'raypoolkit')` at `utilities.py:174`.
- Imported at `ObjectFactories/tests/test_package_provenance.py:46` (from `utilities`), `main.py:77` (from `utilities`), `plot_ScalarModel.py:79` (from `utilities`), `plot_by_beta.py:78` (from `utilities`).
- Called at `ObjectFactories/tests/test_package_provenance.py:95` (1 positional), `ObjectFactories/tests/test_package_provenance.py:117` (1 positional), `ObjectFactories/tests/test_package_provenance.py:141` (1 positional), `ObjectFactories/tests/test_package_provenance.py:160` (1 positional), `ObjectFactories/tests/test_package_provenance.py:171` (1 positional), `ObjectFactories/tests/test_package_provenance.py:200` (1 positional), `ObjectFactories/tests/test_package_provenance.py:220` (1 positional), `ObjectFactories/tests/test_package_provenance.py:232` (1 positional), `ObjectFactories/tests/test_package_provenance.py:262` (1 positional), `ObjectFactories/tests/test_package_provenance.py:276` (0 positional), `main.py:95` (0 positional), `plot_ScalarModel.py:89` (0 positional), `plot_by_beta.py:108` (0 positional).

#### 7. Tracked files other than `.py` matching `RunRegistry|run registry|runregistrykit`

Lines by top directory: `.documents` 1, `CLAUDE.md` 1, `prompts` 19.

Outside the campaign records (text squeezed, first 110 characters):

| File | Line | Text |
|---|---|---|
| `.documents/architecture-summary.md` | 299 | it is there for the RunRegistry component, which needs this release. |
| `CLAUDE.md` | 117 | longer than a few PRyMordial solves. There is no run registry in this repository. |

#### 8. `.gitignore` and the registry

- `.gitignore` does not ignore `var/`.
- Module-level registry mappings: `factories` at `config/datastore.py:101` (27 keys).
- `def inventory_spec`: 17 in 17 files: `ObjectFactories/AdiabaticHistory.py:125`, `ObjectFactories/BBNData.py:120`, `ObjectFactories/DimensionfulQuantity.py:43`, `ObjectFactories/DimensionlessQuantity.py:41`, `ObjectFactories/ExponentialCoupling.py:45`, `ObjectFactories/ExponentialPotential.py:53`, `ObjectFactories/InversePowerPotential.py:53`, `ObjectFactories/QCD_Cosmology.py:43`, `ObjectFactories/ReclinerPotential.py:52`, `ObjectFactories/ReflectingPotential.py:52`, `ObjectFactories/ScalarModel.py:222`, `ObjectFactories/Starobinsky.py:52`, `ObjectFactories/integration_metadata.py:38`, `ObjectFactories/redshift.py:44`, `ObjectFactories/store_tag.py:35`, `ObjectFactories/tolerance.py:37`, `ObjectFactories/version.py:35`.
- `Parent(..., types=...)`: `ObjectFactories/ScalarModel.py:234` (`{XAV_IMPROVED_EOS_IDENTIFIER: 'QCD_Cosmology'}`), `ObjectFactories/ScalarModel.py:239` (`{INVERSE_POWER_POTENTIAL: 'InversePowerPotential', EXPONENTIAL_POTENTIAL: 'Expon`), `ObjectFactories/ScalarModel.py:250` (`{EXPONENTIAL_COUPLING: 'ExponentialCoupling'}`).

### Measured: StochasticInstantons (SI) at `5fb4a1d`

- Repository `/Users/ds283/Documents/Code/StochasticInstantons`, commit `5fb4a1d71a016f1b23393923b9a3d59972415aa0`, 2026-10-12, “Write the rehearsal-lock handover note for ChamPBH and SecondaryGWKit”.
- Read through `git` only: 201 tracked `.py` files parsed with `ast`.
- Against `runregistrykit` 0.1.0 and `datastorekit` 0.4.0 as installed; signatures before the move from SecondaryGWKit a45aefc.
- `requirements.txt`: `ray==2.55.1` (`:57`); `SQLAlchemy==2.0.46` (`:65`).

| Figure | Live code |
|---|---|
| Import statements | 0 |
| … at module level | 0 |
| Files importing it | 0 |
| Names used | 0 |
| Calls bound | 0 |
| … binding | 0 |
| … not binding: the move's new `fingerprint_format` only | 0 |
| … not binding for any other reason | 0 |
| Name-alike calls, not the registry's | 13 |
| String literals naming it | 1 |
| … holding `-m RunRegistry` | 0 |

Campaign records: **0** `.py` files import it, 0 name it.

#### 1. Imports: live code

None.

#### 2–3. Names and their fates at `v0.1.0`: live code

None.

#### 4. Calls: live code

None.

Not the registry's (their callee does not resolve to it), so not bound:

- `Datastore/SQL/Datastore.py:443` `self._engine.begin(…)`, in `Datastore._validate_on_startup`
- `Datastore/SQL/Datastore.py:497` `self._engine.begin(…)`, in `Datastore.object_get`
- `Datastore/SQL/Datastore.py:545` `self._engine.begin(…)`, in `Datastore.object_read_batch`
- `Datastore/SQL/Datastore.py:578` `self._engine.begin(…)`, in `Datastore.object_store`
- `Datastore/SQL/Datastore.py:691` `self._engine.begin(…)`, in `Datastore.object_validate`
- `Datastore/SQL/Datastore.py:759` `self._engine.begin(…)`, in `Datastore.read_table`
- `Datastore/SQL/Datastore.py:776` `self._engine.begin(…)`, in `Datastore.read_largest_store_ids`
- `Datastore/SQL/Datastore.py:813` `self._engine.begin(…)`, in `Datastore.inventory`
- `Datastore/SQL/ProfileAgent.py:75` `self._engine.begin(…)`, in `ProfileAgent.__init__`
- `Datastore/SQL/ProfileAgent.py:145` `self._engine.begin(…)`, in `ProfileAgent.write_batch`
- `Datastore/SQL/ShardedPool.py:293` `self._engine.begin(…)`, in `ShardedPool._write_shard_data`
- `Datastore/SQL/ShardedPool.py:328` `self._engine.begin(…)`, in `ShardedPool._read_shard_data`
- `Datastore/SQL/ShardedPool.py:810` `self._engine.begin(…)`, in `ShardedPool._assign_shard_keys`

#### 5. String literals naming `RunRegistry`: live code

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `utilities.py` | 178 |  | What is installed of each named distribution, read from its metadata. Maps each name to `None` when  |

#### 1. Campaign records

None.

#### 6. `installed_package_provenance`

- Defined at `utilities.py:177-229`, arguments `(names=RECORDED_DISTRIBUTIONS)`; the package's `package_provenance(names)`.
- Its body against the package's, docstrings removed (`-` the package's only, `+` the client's only):

  ```
  -    origin = None
  ```
- `RECORDED_DISTRIBUTIONS = ('datastorekit', 'raypoolkit')` at `utilities.py:174`.
- Imported at `main.py:48` (from `utilities`), `plot_GradientCoupledSolutions.py:102` (from `utilities`), `plot_InstantonSolutions.py:74` (from `utilities`), `tests/test_package_provenance.py:47` (from `utilities`).
- Called at `main.py:98` (0 positional), `plot_GradientCoupledSolutions.py:972` (0 positional), `plot_InstantonSolutions.py:1205` (0 positional), `tests/test_package_provenance.py:94` (1 positional), `tests/test_package_provenance.py:114` (1 positional), `tests/test_package_provenance.py:134` (1 positional), `tests/test_package_provenance.py:157` (1 positional), `tests/test_package_provenance.py:166` (1 positional), `tests/test_package_provenance.py:195` (1 positional), `tests/test_package_provenance.py:214` (1 positional), `tests/test_package_provenance.py:227` (1 positional), `tests/test_package_provenance.py:258` (1 positional), `tests/test_package_provenance.py:270` (0 positional).

#### 7. Tracked files other than `.py` matching `RunRegistry|run registry|runregistrykit`

Lines by top directory: `.documents` 2, `.prompts` 9.

Outside the campaign records (text squeezed, first 110 characters):

| File | Line | Text |
|---|---|---|
| `.documents/dk-and-rpk-migration/01-rehearsal-tooling-and-run-provenance.md` | 36 | Its fields and their meanings are those of SGK's `RunRegistry.package_provenance()` |
| `.documents/dk-and-rpk-migration/01-rehearsal-tooling-and-run-provenance.md` | 37 | (`SecondaryGWKit/RunRegistry/__init__.py:122-169`, read, not imported) and of ChamPBH's helper |

#### 8. `.gitignore` and the registry

- `.gitignore` does not ignore `var/`.
- Module-level registry mappings: `_factories` at `Datastore/SQL/Datastore.py:96` (30 keys).
- `def inventory_spec`: 0 in 0 files.
- No `Parent(..., types=...)` call.

### The fixture

`./venv/bin/python docs/adoption/measure_client_registry.py path --repository <scratch>/fixture --commit HEAD`, exit 3, as printed (the scratch path in full):

### Measured: the repository at /private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/216541e8-6d82-4715-944d-1f8df5d629b8/scratchpad/agent-07/fixture at `8681254`

- Repository `/private/tmp/claude-35086/-Users-ds283-Documents-Code-RunRegistryKit/216541e8-6d82-4715-944d-1f8df5d629b8/scratchpad/agent-07/fixture`, commit `86812545ce7e83dc81c921eb159682f21018c038`, 2026-10-15, “A fixture for measure_client_registry.py”.
- Read through `git` only: 4 tracked `.py` files parsed with `ast`.
- Against `runregistrykit` 0.1.0 and `datastorekit` 0.4.0 as installed; signatures before the move from SecondaryGWKit a45aefc.

| Figure | Live code |
|---|---|
| Import statements | 3 |
| … at module level | 2 |
| Files importing it | 1 |
| Names used | 9 |
| Calls bound | 5 |
| … binding | 3 |
| … not binding: the move's new `fingerprint_format` only | 1 |
| … not binding for any other reason | 1 |
| Name-alike calls, not the registry's | 2 |
| String literals naming it | 4 |
| … holding `-m RunRegistry` | 1 |

Campaign records: **1** `.py` files import it, 1 name it.

#### 1. Imports: live code

| File | Line | Scope | Statement |
|---|---|---|---|
| `driver.py` | 5 | `module` | `import RunRegistry` |
| `driver.py` | 6 | `module` | `import RunRegistry.stores as rs` |
| `driver.py` | 10 | `run` | `from RunRegistry.stores import fingerprint_of, copy_store` |

#### 2–3. Names and their fates at `v0.1.0`: live code

| Name | Fate | At `v0.1.0` | Sites |
|---|---|---|---|
| `RunRegistry.DEFAULT_ROOT` | deleted | C2: the runs root is the config's runs_root | `driver.py:37` (patched (patch.object)) |
| `RunRegistry.REPO_ROOT` | deleted | C1: the root is the client's, found from its runregistrykit.toml | `driver.py:41` (patched (setattr)) |
| `RunRegistry._slug` | renamed (private) | runregistrykit.slugify(text); U11; at a45aefc (text) | `driver.py:17` (used) |
| `RunRegistry.begin` | kept | runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=); at a45aefc (campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=) | `driver.py:26` (used), `driver.py:29` (used) |
| `RunRegistry.no_such_name` | unknown | not in runregistrykit.__all__ and in no row of the table | `driver.py:33` (used) |
| `RunRegistry.stores.DEFAULT_STORES_ROOT` | deleted | C3: the stores root is the config's stores_root | `driver.py:39` (patched (patch)) |
| `RunRegistry.stores.copy_store` | kept | runregistrykit.stores.copy_store(src, dst, purpose, runs_root=, *, client_root=); at a45aefc (src, dst, purpose, runs_root=) | `driver.py:10` (imported), `driver.py:14` (used) |
| `RunRegistry.stores.fingerprint_of` | moved | datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=); layer C, DatastoreKit's since v0.4.0; at a45aefc (inventory, taken=) | `driver.py:10` (imported), `driver.py:12` (used), `driver.py:13` (used) |
| `RunRegistry.stores.fingerprint_store` | kept | runregistrykit.stores.fingerprint_store(primary, *, write=, runs_root=, taken_by=, client_root=); at a45aefc (primary, *, write=, runs_root=, taken_by=) | `driver.py:42` (assigned) |

#### 4. Calls: live code

| File:line | Call | Positional | Keywords | Unpacking | Verdict |
|---|---|---|---|---|---|
| `driver.py:12` | `fingerprint_of` | 1 | — | — | does not bind: missing a required argument: 'fingerprint_format' (the move's new required `fingerprint_format`) |
| `driver.py:13` | `fingerprint_of` | 2 | — | — | binds |
| `driver.py:14` | `copy_store` | 3 | — | — | binds |
| `driver.py:26` | `RunRegistry.begin` | 0 | campaign, prompt, purpose, root, slug | — | binds |
| `driver.py:29` | `RunRegistry.begin` | 0 | bogus, campaign, prompt, purpose, slug | — | does not bind: got an unexpected keyword argument 'bogus' |

Bound against `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=)`; `runregistrykit.begin(campaign, prompt, slug, purpose, argv=, cwd=, script=, unit=, expected_units=, checkpoint=, results=, scope=, heartbeat_means=, pid=, root=, when=, *, client_root=)`; `runregistrykit.stores.copy_store(src, dst, purpose, runs_root=, *, client_root=)`.

Not the registry's (their callee does not resolve to it), so not bound:

- `driver.py:15` `engine.begin(…)`, in `run`
- `driver.py:32` `begin(…)`, in `launch`

#### 5. String literals naming `RunRegistry`: live code

| File | Line | Command at | Text (first 100 characters) |
|---|---|---|---|
| `driver.py` | 39 |  | RunRegistry.stores.DEFAULT_STORES_ROOT |
| `driver.py` | 43 | **`:43`** | list it with: python -m RunRegistry list |
| `other/utilities.py` | 178 |  | What is installed of each named distribution, read from its metadata. Maps each name to `None` when  |
| `utilities.py` | 178 |  | What is installed of each named distribution, read from its metadata. Maps each name to `None` when  |

#### 1. Campaign records

Importing it: `prompts/old/record.py` (1).

#### 6. `installed_package_provenance`

- Defined at `other/utilities.py:177-229`, arguments `(names=RECORDED_DISTRIBUTIONS)`; the package's `package_provenance(names)`.
- Its body against the package's, docstrings removed (`-` the package's only, `+` the client's only):

  ```
  -    origin = None
  -    packages[name] = {'version': distribution.version, 'url': origin.get('url'), 'commit': vcs_info.get('commit_id'), 'requested_revision': vcs_info.get('requested_revision'), 'editable': dir_info.get('editable') is True}
  +    packages[name] = {'version': distribution.version, 'url': origin.get('url'), 'commit': vcs_info.get('commit_id'), 'requested_revision': vcs_info.get('requested_revision'), 'editable': bool(dir_info.get('editable'))}
  ```
- Defined at `utilities.py:177-229`, arguments `(names=RECORDED_DISTRIBUTIONS)`; the package's `package_provenance(names)`.
- Its body against the package's, docstrings removed (`-` the package's only, `+` the client's only):

  ```
  -    origin = None
  ```
- `RECORDED_DISTRIBUTIONS = ('datastorekit', 'raypoolkit')` at `other/utilities.py:174`.
- `RECORDED_DISTRIBUTIONS = ('datastorekit', 'raypoolkit')` at `utilities.py:174`.

#### 7. Tracked files other than `.py` matching `RunRegistry|run registry|runregistrykit`

Lines by top directory: `notes.md` 1.

Outside the campaign records (text squeezed, first 110 characters):

| File | Line | Text |
|---|---|---|
| `notes.md` | 3 | The RunRegistry is what records a run. |

#### 8. `.gitignore` and the registry

- No `.gitignore`.
- No module-level `factories` or `_factories` mapping.
- `def inventory_spec`: 0 in 0 files.
- No `Parent(..., types=...)` call.

**A name is unknown** (exit 3).
