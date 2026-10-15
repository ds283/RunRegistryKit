# Prompt 05b — the package prose and the rules

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 05a has landed (`14af805`) and been reviewed (`c735acf`, the board's §1). `git diff --stat c735acf
  HEAD -- runregistrykit docs/extraction pyproject.toml PROVENANCE.md CLAUDE.md README.md` is empty.
- U17 is taken (README §6.2, 2026-10-15).
- The suite is `Ran 275 tests … OK`, and `git status` is clean in this repository.

**Closes:** `[00-package-prose-names-sgk]`. **Narrows:** `[02-the-ported-tests-name-sgk]` (the
widened citation scan lists 18 more of the tests' hits, for 05c). **Opens:** only what the work
finds.

**Recommended model:** **Sonnet**. The work is prose: about seventy docstring and comment lines,
one message, and two README sections, under rules this prompt states. The one code change is to
the guard's citation pattern, whose new hits were trial-measured at writing (§"At writing").

**Read first:**

1. [`README.md`](README.md): §0.2 (C8), §2 (05a, 05b, 05c, 06), §4, §5 (all of it; rules 4, 7, 9 and
   10 especially), §6.2 (U11, U16, U17).
2. [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md): §3's `[00-package-prose-names-sgk]` and
   `[02-the-ported-tests-name-sgk]`, and §1's review of 05a.
3. [`logs/05a-the-guard-and-the-public-names.md`](logs/05a-the-guard-and-the-public-names.md): "How
   `known_hits.json` was written" (the writer's text), "Observations not acted on" and "State
   handed to the next prompt"; and [`logs/04b-the-retire-tests.md`](logs/04b-the-retire-tests.md),
   "Observations not acted on" (the two docstrings).
4. `runregistrykit/tests/test_package_is_generic.py` in full, and
   `runregistrykit/tests/data/known_hits.json`.
5. The five package modules' docstrings and comments, `__init__.py` and `stores.py` above all.
6. The rules and the failures they answer, in SGK, through `git -C
   /Users/ds283/Documents/Code/SecondaryGWKit show 14bcac0:<path>` only: `CLAUDE.md`, its section
   "Long-running jobs — the run registry", and `prompts/run-registry/README.md` §0. These are the
   source of §2.6. Nothing else of SGK is read, and no other client.
7. `README.md`, `PROVENANCE.md` and `/Users/ds283/Documents/Code/RunRegistryKit/CLAUDE.md`.

Line numbers below are the package's at `c735acf` (its package files are `14af805`'s).

---

## 1. What is wanted

The package's docstrings and comments still explain it in its first client's terms: that client's
campaigns, prompts, README sections, decisions, issue tags, scripts, stores and incidents. A reader
here, or in another client, cannot follow them. This prompt rewrites that prose in the package's own
terms, keeping every reason it gives, and moves the history to `PROVENANCE.md`. The rules the
package exists to support move into this repository's `README.md`, each with the failure it
answers (SGK's brief §6), so that the prose can point at them.

- **The guard is widened first (U17)**, so that the rewrite is measured, not only read. The
  citation scan gains three forms: `Prompt` with a capital, a decision id, and an issue tag.
- **The prose** of the five package modules is rewritten until their known hits are empty in every
  scan, the widened one included, and no other client reference is left (§2.3).
- **One message** names a client's command: `store fingerprint`'s problems line. It is replaced.
- **Two docstrings** that 04b's log found inexact are made exact.
- **`README.md`** gains the rules and a section on the public names (U11: no patch target is
  promised).
- **`PROVENANCE.md`** gains 05b's section and a record of where the rewritten prose's citations
  pointed.
- **`known_hits.json`** is rewritten by 05a's writer: the package modules' entries gone, the tests'
  entries 05a's plus the widened scan's.

No behaviour changes but the one message's text. No test is renamed and no test's prose is touched
(05c).

---

## 2. What to change

### 2.1 The venv

Unchanged: Python 3.12.15, `black` 25.1.0, `ray` 2.43.0, SQLAlchemy 2.0.39, `datastorekit`
`v0.4.0` (`c8570e8`), `runregistrykit` editable, `git` 2.56.0. **Install nothing.**

### 2.2 The citation scan, widened (U17)

In `runregistrykit/tests/test_package_is_generic.py`, the citation pattern gains three forms, each
built from parts as the existing three are, so that the guard still holds no citation:
- **the word for a prompt with a capital**: `Prompt` or `Prompts`, followed by a space and two
  digits, as the lower-case form;
- **a decision id**: one of the capitals `C`, `D`, `G`, `Q` and `U`, followed by one or two digits,
  as a whole word (`\b…\b`);
- **an issue tag**: `[`, two digits, an optional lower-case letter, a hyphen, lower-case letters,
  digits and hyphens, `]`.

The module docstring's description of the citation scan says so, in words. `TestTheRules`'s
citation test gains samples of each new form that it must find, and near misses it must not (a
decision letter outside the five, three digits, a lower-case letter; an issue tag without its
digits), built from parts. No other rule, word or allowance changes.

### 2.3 The package prose

Every docstring and comment of `__init__.py`, `stores.py`, `client.py`, `fingerprint.py` and
`__main__.py` that names or cites a client is rewritten in the package's own terms. **The guard is
the floor, not the ceiling**: when its known hits for the package modules are empty, these must be
gone too:
- a client's name, script, driver, store, table, class or run (`main.py`, the `A3` store and its
  backup, `realistic_large_x.py`, a pipeline run "of `main.py`");
- a campaign, a prompt, a README section, a log, a decision or an issue of any repository,
  this one's included (`prompts/…`, "README §0 item 3", "store-retirement README D6", "prompt 01's
  rule", "Prompt 02's interface", `[10-…]`), and an incident's date;
- `CLAUDE.md` as the home of the rules (they are the README's now, §2.6).

The rules of the rewrite:
1. **Keep every reason.** Where the prose explains a rule by a client's incident, state the reason
   in general terms, and where it is one of the README's rules, point at that rule by its name
   ("the README's rule on liveness"), never by a section number. For example: a `pgrep -f` match
   also matches the shells polling for the job, so a wait on it can never end.
2. **Keep every fact.** What a function refuses, writes, deletes, reads and returns, in what
   order, is unchanged; a docstring is reworded, never made vaguer. Where a fact was given only by
   a citation (for example "prompt 01's rule for legacy shard records"), state the rule itself.
3. **What may be named:** the package's own names; DatastoreKit's public names; this repository's
   `README.md` (by section name) and `PROVENANCE.md`; the manifest's and the sidecar's keys.
   `campaign`, `prompt` and `slug` are the manifest's keys and `run_id`'s and `begin()`'s parameters,
   so they stay; describe them as the client's names for a body of work, its step, and the run.
4. **The examples are neutral**: the module docstring's `begin(campaign="run-registry", …)` becomes
   a name of no repository (for example `campaign="example"`).
5. **No code changes.** Only docstrings and comments, with the one message of §2.4. `.manifest.json`
   stays out of every non-docstring string but `sidecar_path`'s
   (`test_store_sidecar.py:55-82` pins it).
6. **Width.** Lines within 100 columns, as the rest of the package; `black` is run on the five
   modules.

The lines found at writing are listed in §"At writing"; that list is a guide, and the two
conditions above are the test.

### 2.4 The message

`DatastoreKitFingerprinter.describe` (`fingerprint.py:151`) prints "problems: (counts only; the
store's own text is in `main.py --inventory`)", a client's command. DatastoreKit `v0.4.0` has no
inventory command, and `store fingerprint --listing` writes record lines, not problems. Replace the
pointer with DatastoreKit's public reader: the problems' text is in the store's inventory, which
`datastorekit.store_inventory.read_inventory` returns. The line keeps its leading `problems:` and
"counts only". `test_fingerprinter.py` gains one test that `describe` of a fingerprint with a
problem gives that line, naming `read_inventory`; no existing test asserts the old text.

### 2.5 The two docstrings 04b's log found

- `load_fingerprinter`'s list of refusals (`fingerprint.py:182-185`) names the class refusal: a
  class named where an instance is wanted.
- `retire_store`'s docstring says every refusal ends "Nothing was written or deleted"
  (`stores.py:1562-1563`), and `amend_sidecar`'s gives every refusal's form (`:1934-1935`). The
  config's refusals (`require_fingerprinter`'s and `load_fingerprinter`'s `ConfigError`) are the
  config's own text and do not end so, though each comes before anything is written. Make each
  docstring exact; **change no message**.

### 2.6 `README.md`: the rules, and the public names

Two sections are added after the opening paragraphs. Nothing else of the README changes: its
"Status" paragraph is stale, and is 06's to rewrite with usage and installing.

**The rules.** An opening paragraph: the registry records; it does not schedule, supervise, restart
or lock; it deletes nothing but a store's own files, and those only through `store retire`, which
a person runs and which leaves the sidecar as the store's record; it never deletes a run directory,
a sidecar or any other record. Then the six rules of SGK's `CLAUDE.md` section, each stated for any
client, with the commands this package gives (`python -m runregistrykit list`; `Run.heartbeat(pid=…)`)
and the runs root the client's `runregistrykit.toml` names (default `var/runs`, which the client's
`.gitignore` must ignore):

1. **Discovery**; 2. **Liveness** (pid and heartbeat, never a command-line match); 3. **Launch**
(detached, manifest first, output in the run directory, pid recorded); 4. **Do not babysit**;
5. **Durability** (under the client's root, never a session scratchpad or `/tmp`); 6. **Provenance**
(taken at launch, never re-stamped).

Each rule ends with **the failure it answers**, from SGK's `prompts/run-registry/README.md` §0 (its
five failures, §0.1's provenance stamp and §0.3's "a registry nobody reads is worse than none"),
told as what happened, in general terms, with the numbers that make the point (nineteen poll loops,
fifteen waiting on a dead job; a census lost with a scratchpad). The section says once where they
happened: in the project the registry was extracted from (`PROVENANCE.md`). It names no client's
script, store or campaign. The log gives the mapping of rule to failure that the README uses.

**The public names (U11).** Each module's `__all__` is its public interface: `runregistrykit`
(the core, with `slugify` and the config's names), `runregistrykit.stores`,
`runregistrykit.client`, `runregistrykit.fingerprint` (the protocol, `DatastoreKitFingerprinter`
and the loader), and `python -m runregistrykit`. Everything else is private and may change in any
release. **No patch target is promised**: where the package looks a name up at call time (for
example `Run.finish` importing `runregistrykit.stores` and calling `fingerprint_store`), a client
that patches it does so at its own risk.

`README.md` is not scanned by the guard; it may name SecondaryGWKit as the origin, as it does now.

### 2.7 `PROVENANCE.md`

"Since the import" gains 05b's section: the prose rewritten, the message replaced, the two
docstrings, the README's two sections, the widened scan. And a new section, **"Where the prose's
citations pointed"**: a table, one row per topic the old prose cited (the rules and the five
failures; managing stores as part of the registry; the sidecar's single owner; the legacy
sidecar's `datastore` read by its final component; retirement and its decisions; the reference
search and its issue; the fingerprint; amendment; the checkpoint pattern and the provenance stamp;
`now_iso`'s format and `stage_reached`), giving the SGK record each cited (repository path and
section, at `a45aefc` or SGK's `14bcac0`) and where the reason is stated now (the README's rule, or
the docstring that states it). `PROVENANCE.md` may name SGK's records; it is not scanned.

### 2.8 `known_hits.json`

Rewritten by 05a's writer, never by hand: delete the file, run the writer whose text 05a's log
gives (from the session scratchpad, never under `runregistrykit/` or `docs/`), with the guard and
the five modules final. The log gives the writer's text again (unchanged, or the difference
explained) and the diff of the file. Expected: **no entry for any package module in any scan**;
for the tests, 05a's entries unchanged, plus the widened scan's (§"At writing", 18 hits in 11
entries) under `test_no_citation`. Any other difference in a test's entry is a **stop**: 05b changes
no test's text.

### 2.9 What else moves

`test_fingerprinter.py` gains §2.4's test. Nothing else: no test is renamed, no test's prose,
fixture, `pyproject.toml`, `CLAUDE.md`, `client_vocabulary.json`, the measuring script or
`compare_with_source.py` changes. The board's package lines for the open issues are re-read at
this commit and recorded (§4.3).

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s runregistrykit/tests -t .`, from the root: **`Ran 275 +
   N tests … OK`**, N the new tests. Count by loader and give the per-module counts and the time.
2. **Nothing outside temporary directories**: `git status --short --ignored` the same before and
   after a run (but `__pycache__/`); no `var/`; `git worktree list` this checkout alone; no Ray
   process before or after.
3. **The code is unchanged.** For each of the five modules, `ast.dump` of the module with every
   docstring removed equals `c735acf`'s, but `fingerprint.py`'s one string constant (§2.4). The log
   gives the script and its output.
4. **The prose, by the guard and by grep.** The guard's scans over the five modules alone find
   nothing. Then, over the five modules' docstrings and comments, a case-insensitive grep for
   `prompt`, `campaign`, `README`, `CLAUDE`, `log's`, `A3`, `backup`, `pipeline`, `main.py`,
   `realistic`, `handover`, `scratchpad`, `2026-` and `§`: every line it finds is listed in the log
   with why it stays (a manifest key, a parameter, a README section by name, a rule's reason in
   general terms), or it is rewritten.
5. **The known hits.** The file as §2.8 says, its diff in the log; the per-scan totals, package and
   tests, against §"At writing"'s.
6. **The tests catch behaviour** (README §5 rule 10). Each mutation is applied, the suite run, then
   reverted, and recorded as a diff with the tests that fail:
   - (m1) `(Prompt 07)` added to a comment of `client.py`;
   - (m2) `(D4)` added to a comment of `client.py`;
   - (m3) an issue tag of the board's form added to a docstring of `client.py`;
   - (m4) the capital form dropped from the citation pattern;
   - (m5) one of the widened scan's known entries for the tests removed from `known_hits.json`;
   - (m6) `main.py --inventory` restored in `describe`'s line;
   - (m7) one SGK citation restored in `stores.py` (`# retirement (store-retirement prompt 03)`
     back above `_SHARDS_TABLE_UNREADABLE`'s section);
   - (m8) the agent's own, of the widened rule.

   Each must fail at least one test. A mutation no test catches is a **stop**.
7. `./venv/bin/black --check runregistrykit docs` is clean.

---

## 4. Acceptance

1. §2's changes are in. `runregistrykit/` changes in the five modules' docstrings and comments, the
   one message, the guard's citation pattern and its docstring and tests, `test_fingerprinter.py`'s
   new test, and `known_hits.json`; no file is added or removed under it. `README.md` and
   `PROVENANCE.md` change as §2.6 and §2.7 say.
2. §3.1–§3.7 hold. `known_hits.json` has no entry for a package module.
3. **The records**, in the same commit:
   - the log, `logs/05b-the-package-prose-and-the-rules.md`, per README §5.1. It holds: the
     widened forms; the per-scan totals before and after; the writer and the file's diff; §3.3's
     script and output; §3.4's grep and its accounting; the rule-to-failure mapping of §2.6; the
     suite before (275) and after; every mutation as a diff;
   - this board: the header, §1's row for 05b, §1.1's P1, §3 (`[00-package-prose-names-sgk]` closed
     into §4 with this commit and what resolved it; `[02-the-ported-tests-name-sgk]` narrowed by the
     widened scan's 18 hits, with *Package lines (05b, …)*; the other two with theirs);
   - `docs/OPEN_ISSUES.md`: `[00-package-prose-names-sgk]`'s row deleted, the count 3, the date;
   - `prompts/INDEX.md`: the campaign's line;
   - `PROVENANCE.md`: §2.7.

---

## 5. Stop conditions — stop and ask the user

- A reason the old prose gave cannot be stated without naming a client.
- A docstring's fact cannot be kept as it stands (the prose and the code disagree): record it and
  ask; do not change the code.
- `known_hits.json` would change for a test file other than by the widened scan's entries.
- A word rule, package word or allowance beyond §2.2 would be needed for a scan to pass.
- A mutation of §3.6 is caught by no test.
- An existing test would need to change.
- Any record would change form (README §5 rule 7).
- The suite needs a Ray cluster, starts Ray, imports a client, writes outside a `tempfile`
  directory, or leaves a worktree registered here.
- Anything would require editing or running SGK, ChamPBH, StochasticInstantons, DatastoreKit or
  RayPoolKit, reading a client other than as "Read first" item 6 says, or installing anything.

---

## 6. What this prompt does not do

- **Files it changes:** the five package modules (docstrings, comments, §2.4's message);
  `runregistrykit/tests/test_package_is_generic.py` (§2.2); `test_fingerprinter.py` (§2.4's test);
  `runregistrykit/tests/data/known_hits.json` (§2.8); `README.md`; `PROVENANCE.md`; the log, this
  board, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`.
- It changes no test's prose and renames nothing (05c). It rewrites the README's "Status" paragraph
  and adds usage and installing to it only in 06.
- It changes no code but one message, no record's form, `pyproject.toml`, `CLAUDE.md`,
  `client_vocabulary.json` or the measuring script.
- It adds no CI and makes no tag.

---

## 7. The log and the board

`logs/05b-the-package-prose-and-the-rules.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: the header, §1's row for 05b, §1.1's P1, and §3 and §4 as §4.3.

---

## At writing (2026-10-15, at `c735acf`)

Measured read-only, for the README's row and the orchestrator:
- **The package modules' known hits** (05a's guard): 69 hits in 30 entries, in `__init__.py` (43:
  strings 20, comments 3, citations 20, with `A3`, `main.py`, `realistic_large_x`,
  `handover-A3-baseline-lambdacdm`, `handover`, `run-registry`, `datastore-portability`,
  `store-fingerprint`, `store-retirement`, `prompts/`, `§0`, `§6`), `stores.py` (25: strings 5,
  comments 5, citations 15) and `fingerprint.py` (1, `main.py`). On 44 distinct lines: `__init__.py` 27, `stores.py` 16,
  `fingerprint.py` 1. `client.py` and `__main__.py` hold none.
- **What the guard misses**, by a trial of §2.2's three forms over the 05a tree: in the package
  modules, 11 hits in 7 entries (`__init__.py` `D0`, `D6`; `stores.py` `D3` ×2, `D4`, `D5` ×4,
  `Prompt 02`, `[10-store-retire-reports-every-tombstone-as-a-reference]`); in the tests, 18 hits in
  11 entries (`test_client_root.py` `Q3`, `U9`; `test_fingerprinter.py` `D4` ×2, `U14` ×2, `U7` ×2,
  `[02-the-sidecar-readers-guards-are-unpinned]`; `test_store_amend.py` `D5`;
  `test_store_copy_move.py` `C3`; `test_store_retire.py` `D4` ×3, `D6` ×3;
  `test_store_retire_references.py` `[10-store-retire-reports-every-tombstone-as-a-reference]`).
  None in the guard or `test_public_names.py`; no capital `Prompt NN` in the tests. Beyond any
  scan, the package's prose cites `README` 19 times (13 in `__init__.py`, 6 in `stores.py`, every
  one a client's README) and `CLAUDE.md` twice (`__init__.py:18`, `:172`).
- **The lines to rewrite**, found by the guard, the trial and a grep (a guide, §2.3):
  `__init__.py:18-29, 37-39, 47, 108, 112, 172, 252, 258-261, 382-386, 409-412, 494-497, 543,
  551, 629-641, 654, 664, 670, 682`; `stores.py:21-22, 30, 64, 100, 117-120, 124, 215, 431-432,
  1121, 1225, 1400, 1409, 1447, 1454-1455, 1464, 1530, 1565, 1573, 1581, 1889, 1892-1894`;
  `fingerprint.py:151` (the message) and `:182-185` (§2.5). About seventy lines.
- **The one message** naming a client is `fingerprint.py:151`; every other string hit is a
  docstring. No test asserts it, and no test reads a docstring but `test_store_sidecar.py:55-82`,
  which excludes docstrings from its `.manifest.json` check. DatastoreKit `v0.4.0` ships
  `datastorekit/tools/shard_key_audit.py` and `sharded_store.py`, neither an inventory command.
- **The two docstrings**: `load_fingerprinter` (`fingerprint.py:182-185`) lists four refusals and
  not the class refusal at `:210-216`; `retire_store` (`stores.py:1562-1563`) says every refusal ends
  "Nothing was written or deleted", which the loader's and `require_fingerprinter`'s `ConfigError`
  do not; `amend_sidecar` (`:1934-1935`) likewise.
- **The rules' source**, SGK `14bcac0`: `CLAUDE.md` "Long-running jobs — the run registry" (six
  rules), `prompts/run-registry/README.md` §0 (five failures, §0.1 the provenance stamp, §0.2
  existence against checkpointing, §0.3 a registry nobody reads). SGK's brief §6 advises the README
  state them in full with the failure each answers, and each client's `CLAUDE.md` keep a short
  binding section pointing there (07's checklists).
- **`README.md`** (25 lines) has no rules section; its "Status" paragraph says the code does not
  live here yet, stale since 01, and left to 06 by the user's ruling at this writing.
