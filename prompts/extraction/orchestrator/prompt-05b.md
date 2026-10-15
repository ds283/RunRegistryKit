# Orchestrator — prompt 05b, the package prose and the rules

Read [`../README.md`](../README.md) first: §0.2 (C8), §2 (05a–05c), §4 (after 05b), §5 (every rule;
4, 7, 9 and 10 especially), §6.2 (U11, U16, U17). The conventions are
[`prompt-05a.md`](prompt-05a.md)'s and its predecessors'; they are restated in §0 because the agent
reads §0 and not this directory. Where this note and an earlier one differ, this one is right for
05b.

**You do not write code.** You may:
- run the suite, `black --check`, the guard's scans and the tests the log names;
- replay the log's mutation diffs with `git apply`, and revert them;
- export this repository's tree at any commit into the session scratchpad and run the package and
  the guard's functions there, never committing anything;
- read SGK at `14bcac0` through `git -C … show`, and only its `CLAUDE.md` and
  `prompts/run-registry/README.md`, to check the README's rules against their source (§3 check 7);
- fix small residue in a follow-up commit of your own (§4).

No client, DatastoreKit or RayPoolKit is run, imported or edited, and no working tree of theirs is
read.

**The prompt:** [`05b-the-package-prose-and-the-rules.md`](../05b-the-package-prose-and-the-rules.md)
**Closes:** `[00-package-prose-names-sgk]` · **Narrows:** `[02-the-ported-tests-name-sgk]` (18 more
of the tests' hits listed by the widened scan) · **Opens:** only what the work finds ·
**Model:** Sonnet, as the prompt recommends.

**Gate:**
- The prompt's gate: 05a landed (`14af805`) and reviewed (`c735acf`); `git diff --stat c735acf HEAD
  -- runregistrykit docs/extraction pyproject.toml PROVENANCE.md CLAUDE.md README.md` empty; U17
  taken; the suite 275 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is a rewrite of prose under a guard that measures it.** About seventy docstring and comment
lines change, one message, two docstrings, and the README gains two sections; the only code that
changes is the guard's citation pattern and one string constant. The weight of the review is
therefore on four things:
- **the code is unchanged**: `ast` with docstrings removed equals `c735acf`'s, but the one constant
  (§3 check 2);
- **the widened scan bites, and no wider than §2.2**: each new form found, each near miss not, the
  guard still clean of its own pattern (§3 checks 4, 7);
- **the known hits are exactly the scans' at the commit**: no package-module entry, the tests' 05a's
  plus the widened scan's 18, written by 05a's writer (§3 check 5);
- **the prose keeps every reason and every fact**, read line by line against `c735acf`, and the
  README's rules are SGK's six with their failures, told in general terms (§3 checks 3, 7).

**What moves on purpose:** the five package modules' docstrings and comments, and the one string
constant of `DatastoreKitFingerprinter.describe` (`fingerprint.py:151`);
`runregistrykit/tests/test_package_is_generic.py` (the citation pattern, its docstring paragraph,
and `TestTheRules`' citation samples); one new test in `runregistrykit/tests/test_fingerprinter.py`;
`runregistrykit/tests/data/known_hits.json`; `README.md`; `PROVENANCE.md`; the log and the records.
**Nothing** in any other test module or fixture, `client_vocabulary.json`, the measuring script,
`compare_with_source.py`, `pyproject.toml`, `LICENSE`, `.gitignore`, `CLAUDE.md`, the campaign
README, the prompt or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The trial's widened forms, measured again at `92f173c`.** An independent scan of the guard's
   text sources (every string constant, every comment) with the three forms written as
   `\bPrompts? \d\d`, `\b[CDGQU]\d{1,2}\b` and `\[\d\d[a-z]?-[a-z0-9-]+\]` finds exactly the
   prompt's "At writing" figures: **package modules 11 hits in 7 entries**, at `__init__.py:25`
   (`D0`), `:682` (`D6`); `stores.py:64` (`D3`), `:431` (`D5`), `:1121` (`Prompt 02`), `:1447`
   (`D5`), `:1464` (the `[10-…]` tag), `:1565` (`D3`), `:1573` (`D4`), `:1581` (`D5`), `:1894`
   (`D5`); **tests 18 hits in 11 entries**, the prompt's list; none in the guard or
   `test_public_names.py`. A hit is a (line, word) pair, as 05a's scans count. A different count
   at the agent's widened pattern is explained in the log, and a stop only if a test file's entry
   differs from these (§5).
2. **Built from parts, and the self-scan still clean.** Each new form is assembled from fragments as
   `_DIRECTORY`, `_PROMPT` and `_SECTION_SIGN` are, so that the guard's own text holds no citation.
   The decision letters may appear as a character class (`[CDGQU]`), since no digit follows them in
   the source. The samples in `TestTheRules` are built from parts too (05a's log, deviation 5): a
   decision id from a letter and a digit string, a tag from its pieces. The near misses §2.2 asks
   for are each asserted to give no hit: a letter outside the five (for example `E` with a digit),
   three digits, a lower-case letter, and a tag without its digits. The module docstring describes
   the forms **in words**, and must itself hold no citation of any form:
   `test_this_module_holds_no_known_hit` is the check.
3. **The config's refusals (§2.5), exactly.** `ConfigError` is a subclass of `RuntimeError`
   (`client.py:84`), so "Every refusal is a `RuntimeError`" stays true; it is the ending that is
   inexact. At the top of `retire_store` (`stores.py:1594-1595`) and `amend_sidecar` (`:1970-1971`),
   `find_client_root`'s `ConfigError` (no config found, or one that cannot be used) and
   `require_fingerprinter`'s (none named) come before anything is read or written, in the config's
   own words; in `retire_store`, `load_fingerprinter`'s comes on a first retirement (step 3, already
   described at `:1577-1580`). Make each docstring say so: the config's refusals are `ConfigError`s
   in their own words, each before anything is written; every other refusal ends as stated. **No
   message changes.** IMPLEMENTATION CHOICE, logged.
4. **`load_fingerprinter`'s list (§2.5)** gains the class refusal at `fingerprint.py:210-216`, in the
   order the code checks it: after the missing attribute, before the protocol check.
5. **The README's durability rule is a rule for the client, not a refusal of the package.**
   `client.py:34-35`: an absolute `runs_root` or `stores_root` is kept as it is. So the README states
   rule 5 as what a client does (keep the runs root under its own root, ignored by git, never a
   scratchpad or `/tmp`), and does not say the package refuses another. Likewise rule 1's `list`
   is a habit the package supports, not one it enforces. IMPLEMENTATION CHOICE, logged.
6. **The README's public names.** List each module's `__all__` as it stands (20, 26, 4, 4 and 1
   names), not only the prompt's parenthesis: `runregistrykit.fingerprint`'s four are
   `DatastoreKitFingerprinter`, `Fingerprinter`, `load_fingerprinter` and `require_fingerprinter`.
   The lookups made at call time that §2.6's example means: `Run._fingerprint_results`
   (`__init__.py:467`) imports `.stores` and calls `fingerprint_store` when `finish(...,
   fingerprint=True)`, and `begin()` imports `.stores` when `results` is given (`:686`). A sentence
   that names the lazy import is enough; the README promises nothing about either.
7. **`PROVENANCE.md`'s table of citations.** The SGK record in each row is taken from the old prose
   as it stands at `c735acf` (`git show c735acf:runregistrykit/<module>`), which names it. The agent
   reads no SGK file to verify those rows: "Read first" item 6 limits SGK to `CLAUDE.md` and
   `prompts/run-registry/README.md`. Say "as cited at `c735acf`" in the section.
8. **The new test (§2.4) adds no hit.** Its name, docstring and literals cite nothing and name no
   client word; `read_inventory` and `datastorekit.store_inventory` are DatastoreKit's public names.
   A new entry in `known_hits.json` for `test_fingerprinter.py` is a stop. It is placed in the
   existing class that tests `describe` if there is one, else in a new class; the log says which.
9. **`known_hits.json`**, as the review of 05a read it: delete the file, then run 05a's writer
   (its text in 05a's log, "How `known_hits.json` was written"), copied into the agent's scratchpad
   subdirectory and run from the repository root with the venv's interpreter, once the guard and
   the five modules are final. The writer is unchanged, its `owners` string included. Expected
   after: **package modules 0 in every scan**; tests code names 29 (14 entries), strings 67 (36),
   comments 1 (1), citations **58 (43)**, imports 0: 05a's 137 in 83, plus 18 in 11. The log gives
   `git diff` of the file.
10. **§3.3's script** compares, for each module, `ast.dump` of the tree at the commit with every
    docstring (module, class and function: a first statement that is a string expression) removed,
    against the same of `git show c735acf:<path>`; and for `fingerprint.py` reports the one
    `Constant` that differs. Comments are not in the AST, so this pins the code and only the code.
    The script lives in the agent's scratchpad, and the log gives its text and output.
11. **§3.4's grep will find `prompt` many times** (the manifest key, `run_id`'s and `begin()`'s
    parameter, `prompt=` in the example). Account for lines, grouped by reason where many share it;
    a line kept is a manifest key, a parameter, a README section by its name, or a reason in general
    terms. `§` must be gone entirely (the citation scan finds it).
12. **The suite.** 275 OK in **90.6 s** at `92f173c`, per module by loader: `test_client_root` 27,
    `test_fingerprinter` 30, `test_package_imports` 3, `test_package_is_generic` 22,
    `test_public_names` 8, `test_run_registry` 29, `test_store_amend` 21,
    `test_store_amend_residuals` 9, `test_store_command_line` 2, `test_store_copy_move` 27,
    `test_store_fingerprint` 29, `test_store_retire` 41, `test_store_retire_references` 10,
    `test_store_sidecar` 17. Expect 275 + 1 (§2.4's test) if the new citation samples go into the
    existing citation test as subtests, or more if the agent adds test methods; the log says which.

**The facts, checked by the orchestrator on 2026-10-15 at `92f173c`.** Pass them on.
- **In-repository state.** `main` at `92f173c`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`.
  `venv/`: Python 3.12.15, `black` 25.1.0, as 05a's note; `black --check runregistrykit docs`: 26
  files unchanged.
- **The gate's diff** from `c735acf` is empty: no package file has changed since `14af805`, so the
  prompt's line numbers (taken at `c735acf`) hold.
- **The suite at `92f173c`:** `Ran 275 tests in 90.564s`, OK; `git status --short --ignored` the same
  after; no Ray process.
- **The lines the prompt names hold:** `describe`'s message `fingerprint.py:151`;
  `load_fingerprinter`'s list `:182-185`, its class refusal `:210-216`; `retire_store`'s "Every
  refusal" `stores.py:1562-1563`; `amend_sidecar`'s `:1934-1935`. Module lengths: `__init__.py` 786,
  `stores.py` 2062, `client.py` 273, `fingerprint.py` 222, `__main__.py` 575; `README.md` 25 lines,
  `PROVENANCE.md` 286.
- **No test asserts `describe`'s problems line** (`test_fingerprinter.py:73-74` is a stub's
  `describe`).
- **SGK at `14bcac0`** resolves; `CLAUDE.md` has "Long-running jobs — the run registry" at its line
  77 (six rules, lines 87-104), and `prompts/run-registry/README.md` §0 (lines 3-55) its five failures,
  §0.1, §0.2 and §0.3, as the prompt's "At writing" says.
- **The index.** **4** open now; **3** after (`[00-package-prose-names-sgk]` closed), unless the
  work opens one.
- **Ray.** No Ray process; `RAY_ADDRESS` unset.

**What the review exists to establish.**
- **(E1) The files.** Only §0's list changes; no file added or removed under `runregistrykit/`.
- **(E2) The code.** The five modules' code unchanged but the one constant; the guard's code
  changed in its citation pattern only.
- **(E3) The guard.** The three new forms, built from parts, as §2.2 says, and no wider; the
  self-scan clean; the known hits equal to an independent scan of the commit.
- **(E4) The prose.** Every reason and fact kept, no client and no citation left, by reading and by
  §3.4's grep; the two docstrings exact; the message replaced.
- **(E5) The README and `PROVENANCE.md`.** The six rules, each with its failure, true to SGK's text
  and naming no client's script, store or campaign; the public names; 05b's section and the
  citations table.
- **(E6) The suite.** 275 + N pass, write nothing outside `tempfile` directories, start no Ray.
- **(E7) The mutations.** (m1)–(m8) each fail a named test, and the orchestrator's own as §3 says.
- **(E8) The records.** The log, the board (one closed, one narrowed), the index (3),
  `prompts/INDEX.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff and the tests
  show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** The prompt's §3.1 command, from the repository root. Write the output to a file in
  the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Mutation diffs** are recorded so that `git apply` replays them from a clean tree at the agent's
  commit. Check each **as recorded in the log** with `git apply --check` and `-R --check`, and
  replay in `bash`, not zsh. None is committed. After each, `git status` must be clean. A mutation of
  a data file is a diff of that file like any other.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`.
  Python's `tempfile` in tests is fine. **No scratch `.py` goes under `runregistrykit/` or
  `docs/`**, even for a moment: discovery walks the one, `black` the other, and the guard's file
  set is derived from the filesystem. The known-hits writer and §3.3's script live in the
  scratchpad.
- **SGK is read only** through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
  14bcac0:<path>`, for `CLAUDE.md` and `prompts/run-registry/README.md`, and nothing else of SGK; no
  other client, DatastoreKit or RayPoolKit is read. No client is imported or run, and no working
  tree is read.
- **Install nothing.** The venv is as 01 left it.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A word rule, package word or allowance beyond §2.2 is a stop, never a
  widened rule; a mutation no test catches is a stop, never a weakened mutation; a change to a test
  file's known entries other than the widened scan's is a stop; a fact the prose and the code
  disagree on is a stop, never a code change.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` at the root.
2. **The prompt's gate:** the diff from `c735acf` empty; the suite 275.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
4. **The index.** 4 now, 3 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Sonnet**, in this checkout. Give it:
- the prompt, the campaign README, the board, 05a's and 04b's logs, `docs/OPEN_ISSUES.md`,
  `CLAUDE.md`, `README.md` and `PROVENANCE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/05b-the-package-prose-and-the-rules.md`, in README
  §5.1's form, with the prompt's §4.3 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It edits no client repository, DatastoreKit or RayPoolKit, and reads SGK only as §0 says.**
- **It installs nothing, reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list, the log and the records. `git diff
   92f173c <commit> --` over every test module but the guard and `test_fingerprinter.py`, the
   fixtures, `client_vocabulary.json`, the measuring script, `compare_with_source.py`,
   `pyproject.toml`, `CLAUDE.md`, the campaign README and the prompt is empty. `git ls-files
   runregistrykit` is the same 26. `test_fingerprinter.py`'s diff is one test, added.
2. **E2, the code, independently.** A script of the orchestrator's own: for each of the five
   modules, `ast.dump` with docstrings removed, at the commit and at `c735acf`; equal but
   `fingerprint.py`'s one constant. For the guard, the same comparison shows only the citation
   pattern's assignments and `TestTheRules`' citation test changed. `run_id`'s ids, and
   `inspect.signature` of every name in each `__all__`, equal `c735acf`'s.
3. **E4, the prose, by reading.** `git diff c735acf <commit>` of the five modules read in full,
   hunk by hunk, against the old text: each reason kept in general terms; each fact kept (what is
   refused, written, deleted, read and returned, in order), none made vaguer; each citation's rule
   stated where the citation stood alone (prompt §2.3 rule 2, "prompt 01's rule for legacy shard
   records" among them); the example neutral; `.manifest.json` only in `sidecar_path`'s strings. The
   two docstrings exact as corrections 3 and 4. `describe`'s line keeps `problems:` and "counts
   only" and names `read_inventory`. Then the prompt's §3.4 grep, re-run: every line found is in the
   log's accounting, and its reason holds.
4. **E3, the guard, by reading.** The pattern's six forms, each from parts; the decision ids whole
   words over exactly `C`, `D`, `G`, `Q`, `U` with one or two digits; the tag as §2.2; the capital
   form as the lower-case; the docstring's paragraph in words; the new samples and near misses as
   §2.2 and correction 2; nothing else of the guard changed.
5. **E3, the known hits, independently.** The orchestrator's scanner of 05a's review, given the
   widened pattern, over an export of the commit: its counts by scan, file and word equal
   `known_hits.json` exactly; no package-module entry; the tests' entries equal `c735acf`'s file
   plus exactly the 11 citation entries of correction 1. The guard's scans over the five modules
   alone return nothing.
6. **E6, the suite.** The prompt's §3.1 command: `Ran 275 + N tests … OK`, the per-module counts the
   log's, the time recorded. `git status --short --ignored` the same before and after but for
   `__pycache__/`; no `var/`; this checkout the only worktree; no Ray process before or after.
   `./venv/bin/black --check runregistrykit docs` is clean.
7. **E5, the README and `PROVENANCE.md`, by reading.** Against SGK's `CLAUDE.md` section and
   `prompts/run-registry/README.md` §0 at `14bcac0`: the opening paragraph's five claims; the six
   rules, each with this package's commands and the config's runs root, and correction 5's reading;
   each failure true to its source and in general terms (the numbers kept, nineteen and fifteen;
   the scratchpad census; the orphaned run; the three-hour measurement held in memory; the resume
   that crashed on an untaken path; the provenance stamp that proved a script unchanged; a registry
   nobody reads), with the log's rule-to-failure mapping; the origin named once; no client's script,
   store or campaign. The public names as correction 6. Nothing else of the README changed (its
   "Status" paragraph stays). `PROVENANCE.md`'s 05b section and the citations table, every topic
   §2.7 lists present, each row's SGK record as cited at `c735acf` and its new home real.
8. **E7, the mutations.** Replay (m1)–(m8) from the log, one at a time, in `bash`; each fails the
   tests the log names; the suite OK after each; the tree clean. Then the orchestrator's own, not in
   the log:
   - (o1) a decision id outside the five (`E1`) added to a comment of `client.py`: **no** test
     fails (the rule is not wider than §2.2);
   - (o2) a decision id of the five added to the guard's own docstring: fails the self-scan test
     and the citation scan;
   - (o3) the issue-tag form dropped from the pattern: the tests' known tag entries no longer
     found, and a rule test;
   - (o4) the decision id's trailing word boundary dropped: a rule test (the three-digit near miss);
   - (o5) a section sign and a digit restored in a docstring of `stores.py`: the citation scan;
   - (o6) `read_inventory` dropped from `describe`'s line: §2.4's test;
   - (o7) `realistic_large_x` restored in a comment of `__init__.py`: the comment scan;
   - (o8) one count in a tests' entry of `known_hits.json` raised by one: that scan.
   An uncaught (o) mutation (but (o1), which must pass) is opened on the board (owner to be put to
   the user), not a stop.
9. **E8, the records.**
   - The log has every section of README §5.1 and the prompt's §4.3 additions: the widened forms;
     the per-scan totals before and after, package and tests; the writer's text and the file's
     diff; §3.3's script and output; §3.4's grep and its accounting; the rule-to-failure mapping;
     275 → 275 + N with the per-module counts and the time; every mutation as a diff, with the
     tests that fail it; the deviations classified (corrections 1–12 among them).
   - The board: the header; 05b's row (landed, "this commit", 275 → …); P1 ✅; §3's
     `[00-package-prose-names-sgk]` moved to §4 with this commit and what resolved it;
     `[02-the-ported-tests-name-sgk]` narrowed by the 18, with *Package lines (05b, …)*; the other
     two with theirs; §3's opening count sentence. `docs/OPEN_ISSUES.md`: the row deleted, **3** by
     counting, the date. `prompts/INDEX.md`'s row says 05b landed.
10. **The interface and the handover.** No record changes form: the diff touches no writer and no
    message but `describe`'s, which is printed, not recorded. The log's "State handed to the next
    prompt" gives 05c its share (155 hits in 94 entries, by scan), how to re-write
    `known_hits.json`, the suite count, and that nothing was installed, pushed or tagged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 05b* paragraph, in the form of
  05a's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md` and in
    `PROVENANCE.md`;
  - "reviewed" for 05b in the board's header and row, README §2's status column and its header,
    and `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 05b".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Nothing is pushed** without the user's clear yes; ask in the report.
- **Report to the user:**
  - what landed, and the count, 275 → 275 + N;
  - the widened scan and what it found; the known hits now, all the tests';
  - the prose: what was rewritten, the message, the two docstrings;
  - the README's rules and public names, and `PROVENANCE.md`'s table;
  - the mutations, the agent's and the orchestrator's, and what is not pinned (the prose's
    faithfulness is read, not tested);
  - the issue closed and the one narrowed, and anything opened;
  - that 05c can now be written, against the tree 05b left;
  - and whether to push `main`.
