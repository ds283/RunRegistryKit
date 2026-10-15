# Orchestrator — prompt 07, the adoption checklists

Read [`../README.md`](../README.md) first: §0.2, §1, §2 (06–08), §3, §4, §5 (rules 5, 6, 7, 9 and
10), §6.2 (U5–U9, U11, U19–U22) and §7. The conventions are [`prompt-06.md`](prompt-06.md)'s and its
predecessors'; they are restated in §0 because the agent reads §0 and not this directory. Where this
note and an earlier one differ, this one is right for 07.

**You do not write code.** You may:
- run the suite, `black --check`, the agent's script and the Q5 sketch, in `venv/` or in venvs of
  your own in the session scratchpad;
- replay the log's breakage diffs with `git apply`, and revert them;
- build fixture repositories of your own in the session scratchpad;
- read the clients **through `git` only**, at the commits named, as the prompt does;
- fix small residue in a follow-up commit of your own (§4).

No client, DatastoreKit or RayPoolKit is run, imported or edited, and no client's working tree,
index, stash, `venv/` (but `pyvenv.cfg` as text), store or run directory is touched. **Nothing is
pushed and no tag is made**, by the agent or by the orchestrator, without the user's clear yes.

**The prompt:** [`07-the-adoption-checklists.md`](../07-the-adoption-checklists.md)
**Closes:** `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]` (U20) · **Opens:**
only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- The prompt's gate, as corrected by §0 correction 1: 06 landed (`9f8ebe4`) and reviewed
  (`4ee947b`); `v0.1.0` tagged on `9f8ebe4` (tag object `fd5ce48`); the release recorded
  (`dca5ead`); U20, U21 and U22 taken; no `docs/adoption/`; the suite 276 OK; the tree clean.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/`. If a
  later commit touches anything else, re-check every fact below that it could move, and hand the
  agent the corrections as an addendum.
- Each client's `HEAD` is still §0's commit. If one has moved, that is the prompt's stop (§5), put
  to the user before dispatch.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It changes no behaviour, and nearly all of its output is about other repositories.** One
measuring script, four documents and one README paragraph. No file under `runregistrykit/` moves,
and the suite stays at 276. The weight of the review is on four things:
- **every fact about a client is true at its commit**, cited by `path:line` and read there, and the
  script's figures are the planner's or explained (§3 checks 3, 6);
- **the script measures what it says, and fails when it should**: the fates checked against the
  package as it runs, every call resolved through the registry's names before it is bound, the
  output deterministic, the client read through `git` alone (§3 checks 3–5);
- **every statement about the package is true of `v0.1.0`**, checked against the code, not against
  the prompt (§3 check 7);
- **the Q5 sketch runs as written on public names, and each breakage it names fails** (§3 check 8).

**What moves on purpose:** `docs/adoption/README.md`, `secondarygwkit.md`, `champbh.md`,
`stochasticinstantons.md` and `measure_client_registry.py` (all new); `README.md` ("Using it"
only, U20); `PROVENANCE.md` (07's section under "Since the import"); the log, the board,
`prompts/INDEX.md` and `docs/OPEN_ISSUES.md`. **Nothing** under `runregistrykit/`,
`docs/extraction/` or `.github/`; not `pyproject.toml`, `CLAUDE.md`, `LICENSE`, `.gitignore`, the
campaign README, the prompt or `orchestrator/`.

**Corrections and readings of the prompt.** Pass them on. Each is recorded in the log as found.
1. **The gate's diff is not empty.** `git diff --stat dca5ead HEAD -- runregistrykit docs
   pyproject.toml PROVENANCE.md CLAUDE.md README.md .github` shows `docs/OPEN_ISSUES.md`, one line:
   `f7c1b15`, the commit that wrote the prompt, set U20's owner to 07 in the index, as `CLAUDE.md`'s
   rule requires. Read the gate as: that diff touches `docs/OPEN_ISSUES.md` alone, and that line
   alone. Everything else in the gate holds.
2. **"At `v0.1.0`" is checked through `venv/`'s editable install.** `venv/` holds `runregistrykit`
   editable from this checkout, and `git diff 9f8ebe4 HEAD -- runregistrykit pyproject.toml` is
   empty, so what the script imports is the tag's code; `importlib.metadata.version
   ("runregistrykit")` is `0.1.0`. The log records that diff empty, before and after. Nothing is
   installed. A `path:line` under `runregistrykit/` is read at `9f8ebe4`
   (`git show 9f8ebe4:<path>`), which equals the working tree there.
3. **A call is "reached through the registry" only when its callee resolves to a registry name.**
   Matched by function name alone, SGK at `14bcac0` has **six more `begin()` calls**, none the
   registry's (SQLAlchemy's, no argument): `ObjectFactories/tests/test_quadsource_parent_key.py:445`,
   `ObjectFactories/tests/test_wkb_numeric_parent_key.py:983`,
   `StoreFixtures/real_store_fixtures.py:229, 270, 1159`, `docs/datastore-generic-audit/
   str_e_misfire_probe.py:45`. Bound against the registry's `begin`, each would fail and trip the
   stop falsely. So the script resolves a call's callee through the names each file binds from the
   registry (`import RunRegistry`, `import RunRegistry.stores as x`, `from RunRegistry import
   begin`, `from RunRegistry import stores`, nested or not), with scope as Python has it near enough
   for these files, and binds only those. The log lists the excluded name-alike calls it saw, with
   why. `fingerprint_of` is resolved the same way (imported from `RunRegistry.stores`).
4. **Two more forms of patching.**
   - **A plain assignment.** `docs/a3-v2-readiness/sigterm_handler_probe.py:210` monkeypatches with
     `registry_stores.fingerprint_store = slow_fingerprint` (saved at `:187`), where
     `registry_stores` is `RunRegistry.stores` (`:151`). The script reports an assignment to an
     attribute of a registry module or alias as a patch. At `v0.1.0` the patch still takes effect,
     since `Run._fingerprint_results` imports `fingerprint_store` from `.stores` when it is called
     (`runregistrykit/__init__.py:468`), but it is not promised (README, "The public names"); SGK's
     checklist says both.
   - **An instance.** `mock.patch.object(run, "_fingerprint_results", …)`
     (`RunRegistry/tests/test_killed_handler.py:333, 432`) patches a `Run` returned by `begin`, which
     the module-based rules cannot reach without type inference. None is wanted. The checklist cites
     these two lines as read (prompt §0.3), and the log says whether the script reports them; a rule
     that matches the attribute name against the package's private names of `Run` is the agent's
     choice, recorded.
5. **The campaign records: 7 files name it, 6 import it.** `git grep -l RunRegistry 14bcac0 --
   'prompts/*.py'` gives 7 files; 6 import `fingerprint_of` from `RunRegistry.stores`, and
   `prompts/datastore-generic/orchestrator/measure-08/scripts/phaseB_edit_tests.py` names it only in
   a string (`:110`). The prompt's "7 campaign-record files" is the first count. The script's item 1
   counts files that import; item 7 (non-`.py`) is separate. The log gives both figures and says
   which each report shows.
6. **SGK's and CPBH's registries have a polymorphic `Parent.types` with `int` keys** (the prompt's
   "not measured", measured here):
   - SGK: `ObjectFactories/cosmology_types.py:17`, `COSMOLOGY_TYPES: Dict[int, str]`, used in the
     specs at `ObjectFactories/BackgroundModel.py:903` and `ObjectFactories/wavenumber.py:399`;
   - CPBH: three, `ObjectFactories/ScalarModel.py:236, 241, 252` (the `type_column`s `cosmology_type`, `potential_type`,
     `coupling_type`), keyed by constants such as `XAV_IMPROVED_EOS_IDENTIFIER = 3`
     (`CosmologyModels/model_ids.py:19`) and `INVERSE_POWER_POTENTIAL = 0`
     (`CosmologyConcepts/Potentials/model_ids.py:16`).

   So item 8 names the case for SGK and for CPBH, by `path:line`, read by the agent. **The sketch's
   key conversion must keep two keys distinct that differ in type** (`1` and `"1"`): a bare
   `str(k)` makes them alike, and the guard would then miss a change of a key's type. The README
   says how the sketch converts a key, and the stand-in registry of §2.2 §6 has keys that show it
   (an `int` and a `str` of the same text, kept apart). How is the agent's choice.
7. **The neutral store's `FACTORIES` holds nine classes; `inventory_specs(FACTORIES)` gives six**,
   the classes with a spec. The prompt's "6 classes" is the latter; the README says so if it gives
   a count. The orchestrator's trial of the recipe (dataclass fields made plain recursively,
   `canonical_json` of `[name, spec]` pairs in registry order, SHA-256) ran on public names and gave
   a 64-hex digest at `NEUTRAL_FORMAT = 1`; the figure is not normative and the agent's sketch need
   not reproduce it.
8. **U20: `:81-82` and `:93-95` are true of the code; `:149-150` is the sentence that is wrong.** A
   relative `runs_root` or `stores_root` is joined to the **record root** (`client.py:34`, `:269-270`
   at `9f8ebe4`), which for a linked worktree is the main checkout; a worktree run is recorded under
   the main checkout. What the README lacks is the distinction between the record root
   (`ClientRoot.root`) and the directory whose config governs (`ClientRoot.found`), and `:149-150`
   says the fingerprinter's module is imported with "the client's root" first on `sys.path`, where
   the code puts `ClientRoot.found` there (`fingerprint.py:52-54`, `:191-193`). So the correction
   keeps `:81-82`'s meaning, names the two directories once, and makes `:149-150` say the tree
   that is running. A rewrite that moved the relative roots to the worktree would be a finding.
9. **CPBH's and SI's `RECORDED_DISTRIBUTIONS`.** Each `utilities.py:174` reads
   `RECORDED_DISTRIBUTIONS = ("datastorekit", "raypoolkit")`, the helper's default. SI pins
   neither. After the substitution the names a client records are its config's `distributions`
   (U9), its own choice; the checklist says what `package_provenance` records for a name that is
   not installed (read from the code at `9f8ebe4`, and run on a name that is not installed), so SI
   can choose.
10. **The script is black-checked by CI** (`black --check runregistrykit docs`,
    `.github/workflows/tests.yml:61`), and run locally under `venv/`'s Python 3.12.15; the guard
    scans only `runregistrykit/`, so the script's client names are allowed there. It is not
    collected by the suite: discovery is `-s runregistrykit/tests`.
11. **The fixture is the agent's, the orchestrator's is its own.** The orchestrator builds an
    independent fixture repository for the review (§3 check 4), through the override the log
    documents. The agent's override must be usable from the command line or a documented function,
    and must not change what the three client commands read.

**The facts, checked by the orchestrator on 2026-10-15 at `f7c1b15`.** Pass them on.
- **In-repository state.** `main` at `f7c1b15`, clean; `git status --short --ignored` shows
  `prompts/.DS_Store`, `runregistrykit.egg-info/`, `runregistrykit/__pycache__/`,
  `runregistrykit/tests/__pycache__/` and `venv/`; this checkout the only worktree; no `var/`; no
  `docs/adoption/` (`docs/` holds `extraction/` and `OPEN_ISSUES.md`). `v0.1.0` is tag object
  `fd5ce48` on `9f8ebe4`. `git diff 9f8ebe4 HEAD -- runregistrykit pyproject.toml README.md` empty.
  The suite `Ran 276 tests in 94.0s`, OK. `black` 25.1.0, `black --check runregistrykit docs`: 26
  files unchanged. No Ray process; `RAY_ADDRESS` unset.
- **The clients, through `git` only.**

  | Repository | Branch | `HEAD` | `status --porcelain` lines / `shasum` | Stash | Worktrees |
  |---|---|---|---|---|---|
  | `SecondaryGWKit` | `handover-remedial` | `14bcac0eb73069131f8ce4f55d91e5fc3e7318cf` | 0 / `da39a3ee…` | 0 | 1 |
  | `ChamPBH` | `main` | `c21cdfb5613a3ed976a91a95431495dc8bfd49c8` | 22 / `fbd525ec…` | 0 | 1 |
  | `StochasticInstantons` | `dk-and-rpk-migration` | `5fb4a1d71a016f1b23393923b9a3d59972415aa0` | 0 / `da39a3ee…` | 0 | 1 |
  | `DatastoreKit` | `main` | `b01737f` | 0 | 0 | 1 |
  | `RayPoolKit` | `main` | `17029d9` | 0 | 0 | 1 |

  SGK: `git ls-tree -r 14bcac0 -- RunRegistry/` 25 rows, `git diff a45aefc 14bcac0 -- RunRegistry
  StoreFixtures` empty; `.gitignore:3` is `var/`. CPBH and SI: no `var` in `.gitignore`.
- **The orchestrator's trial scan** (an `ast` walk of every tracked `.py` at `14bcac0` through `git
  show`), which agrees with the prompt's §0: SGK's live code **13 imports in 10 files, 4 at module
  level**, file by file as §0.1; the staying tests **12 imports in 5 modules**; **18** string
  literals naming `RunRegistry` outside `RunRegistry/` and `prompts/`; the 4 registry `begin` calls
  at §0.1's lines, with keywords `campaign, prompt, slug, purpose, argv, script, results, root`
  (`sigterm_handler_probe.py:159`) and `campaign, prompt, slug, purpose, script, results, scope,
  heartbeat_means` (the other three), each a parameter of `v0.1.0`'s `begin`, whose signature is
  `(campaign, prompt, slug, purpose, argv=None, cwd=None, script=None, unit=None,
  expected_units=None, checkpoint=None, results=None, scope=None, heartbeat_means=None, pid=None,
  root=None, when=None, *, client_root=None)`. `_slug` is reached at `stage_counts.py:37, 38`.
- **The package's names at `9f8ebe4`.** `runregistrykit.__all__` 20 names (`slugify` and
  `package_provenance` among them; no `REPO_ROOT`, `DEFAULT_ROOT`, `RECORDED_DISTRIBUTIONS` or
  `_slug`); `runregistrykit.stores.__all__` 26 (no `fingerprint_of`, `compare_fingerprints`,
  `listing_lines`, `FINGERPRINT_FORMAT`, `DEFAULT_ROOT` or `DEFAULT_STORES_ROOT`); `fingerprint`
  4; `client` 4. `_repo_path(path, root)`; `package_provenance(names)`;
  `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format: int, taken=None)`.
- **The provenance helpers.** CPBH's and SI's `installed_package_provenance`, `utilities.py:177-229`,
  signature `(names=RECORDED_DISTRIBUTIONS)`; by `ast` with docstrings removed, each body is
  `package_provenance`'s less `origin = None`, and nothing else differs.
- **Specs.** SGK: `config/datastore.py:91` `factories = {`, 22 tracked `def inventory_spec`; CPBH:
  `config/datastore.py:101`, 17. SI: none (prompt §0.4).
- **SGK's brief** at `14bcac0` has §8 "What SGK needs back (its gate E2)". RayPoolKit's
  `docs/adoption/` at `17029d9` holds `README.md`, three checklists and `measure_client_pools.py`.
- **The index.** **3** open now; **2** after (`[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]`
  closed), unless the work opens another.

**What the review exists to establish.**
- **(E1) The files.** Only §0's list changes; nothing under `runregistrykit/`.
- **(E2) The script.** As prompt §2.1 with corrections 3–5; deterministic; read through `git`
  alone; its fates checked against the package when it runs; exits 0, 2 and 3 when it should.
- **(E3) The figures.** The script's equal §0's and the prompt's, or each difference explained.
- **(E4) The checklists.** Ten items each, in order and under the same names; every `path:line`
  true at its commit; every package statement true of `v0.1.0`; choices named and not made;
  **Advice:** marked.
- **(E5) The README of `docs/adoption/`.** §1–§8 as prompt §2.2; the Q5 sketch proved, with
  correction 6's key case.
- **(E6) U20.** `README.md` differs in "Using it" only, as correction 8.
- **(E7) The breakage.** (a)–(e) as prompt §3.8.
- **(E8) The records.** The log, the board (A1, the gates, E2, the issue moved), the index (2),
  `prompts/INDEX.md`, `PROVENANCE.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/`, `*.egg-info/`, `__pycache__/` and `.DS_Store` are
  ignored and must not be staged. Count, then paste. A log states only what the diff, the commands
  and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** CLAUDE.md's command, from the repository root, in `venv/`. Write the output to a
  file in the scratchpad and grep the verdict from it. Run it **in the foreground**, within the
  turn; it takes about 95 s.
- **Breakage diffs** are recorded so that `git apply` replays them from a clean tree at the agent's
  commit. Check each **as recorded in the log** with `git apply --check` and `-R --check`, in
  `bash`, not zsh. None is committed. After each, `git status` must be clean.
- **Scratch.** The agent uses its own subdirectory of the session scratchpad (`agent-07/`), never
  `/tmp`; its fixture repositories, scripts, outputs and the Q5 sketch live there. **No scratch
  file goes under `runregistrykit/` or `docs/`**.
- **The clients.** Read through `git -C <repository> ls-tree`, `show`, `grep`, `log`, `rev-parse`,
  `status --porcelain` and `stash list` only, and `venv/pyvenv.cfg` as text through `cat`. Never
  `cd` into a client to run anything, never `checkout`, `stash`, `fetch` or `worktree` there, never
  `import` a client's module, never open its `var/`. DatastoreKit and RayPoolKit: the prompt's
  "Read first" item 6 through `git show`, and `datastorekit` as installed in `venv/`.
- **Installs and network.** None. Nothing is downloaded or installed.
- **GitHub.** Nothing is pushed, no tag is made, no repository setting changes, no workflow is
  dispatched. Read-only `gh api` calls are fine.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A call that does not bind, or an unknown name, is a stop, never a
  widened table; a checklist statement the package does not bear out is a stop, never a softened
  statement that hides it.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must be
   empty, and `git worktree list` must show this checkout alone. No `var/` or `docs/adoption/`.
2. **The prompt's gate**, as correction 1; the suite 276 in `venv/`.
3. **The clients.** Each `HEAD`, `status --porcelain | shasum` and `stash list | wc -l` as §0's
   table, recorded for check 2.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` and `RAY_ADDRESS`.
5. **The index.** 3 now, 2 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, 06's log, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `README.md` and `PROVENANCE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections and readings.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/07-the-adoption-checklists.md`, in README §5.1's
  form, with the prompt's §4.5 additions.
- **The files it may change are §0's "What moves on purpose", and nothing else.**
- **It reads the clients through `git` only, and runs, imports and edits none of them**, nor
  DatastoreKit or RayPoolKit.
- **It installs nothing, and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only §0's list. `git diff f7c1b15 <commit> --
   runregistrykit docs/extraction .github pyproject.toml CLAUDE.md LICENSE .gitignore
   prompts/extraction/README.md prompts/extraction/07-the-adoption-checklists.md
   prompts/extraction/orchestrator` is empty; `docs/adoption/` holds exactly the five files. `git
   ls-files runregistrykit` the same 26.
2. **The clients are untouched.** Each client's `HEAD`, `status --porcelain | shasum`, `stash list
   | wc -l` and `worktree list` equal §0's table, and the log's before and after.
3. **E2, E3: the script, run by the orchestrator.** Each client twice at its commit, `cmp` of the
   two outputs, exit 0; `--json` parsed; a commit the client lacks exits 2. Its figures against
   §0's facts and the prompt's §0, item by item (imports and their scopes, names and fates, the
   four `begin` verdicts, `fingerprint_of`'s two sites, string literals and the three printed
   commands, the provenance helper's one-line difference and its callers, §0.5's counts, `.gitignore`
   and the registry). The six name-alike `begin()` calls of correction 3 absent from the bind
   table; correction 4's assignment reported as a patch. Then **by reading**: it imports only the
   standard library, `runregistrykit` and `datastorekit.store_fingerprint`; it reads only through
   `git`; each fate-table row is checked when it runs; its output is sorted.
4. **The orchestrator's own fixture.** A repository of the orchestrator's, built in the scratchpad
   with one commit, holding prompt §3.3's items **and** an assignment patch
   (`RunRegistry.stores.fingerprint_store = f`), a `begin()` on a non-registry object (`session.begin()`),
   an aliased `import RunRegistry.stores as rs` with `rs.copy_store(...)`, and `RunRegistry._repo_path(p)`.
   Run through the agent's override: each reported with the fate and verdict expected, the
   non-registry `begin()` not bound, `_repo_path` flagged private with both signatures, and exit 3
   for the unknown name.
5. **E7, the breakage.** Replay (a)–(e) from the log's diffs, one at a time, in `bash` (`--check`,
   apply, the failure, `-R --check`, reverse); each fails as the log says; the tree clean after
   each. Then the orchestrator's own:
   - (o1) the callee resolution replaced by a match on the function's name: the SGK run binds the
     SQLAlchemy `begin()` calls, which fail, and the run stops (exit non-zero or a "does not bind");
   - (o2) the assignment-patch rule removed: `sigterm_handler_probe.py:210` is no longer reported;
   - (o3) the private-signature comparison made to read `v0.1.0`'s signature for both sides:
     `_repo_path`'s change is no longer reported.
   An uncaught breakage is opened on the board (owner to be put to the user), not a stop.
6. **E4, the checklists, by reading and checking.** Each opens with its client, path, full SHA,
   branch, date, subject and tree state; the ten items in order under the same names; the appendix
   is the script's output, byte-equal to the orchestrator's run. **Every `path:line`** in the three
   checklists extracted by a script of the orchestrator's and read at its commit (client lines
   through `git show <commit>:<path>`, package lines at `9f8ebe4`): the line exists and says what
   the checklist says it does; a sample of at least twenty, spread across the three, also compared
   with the log's quoted text. Choices the client's are named with what each touches, not made;
   every recommendation marked **Advice:**. The facts of corrections 4, 6 and 9 present where they
   belong. No campaign record rewritten.
7. **E4, E5: the package statements.** Every statement about `v0.1.0` in the four documents
   checked by the orchestrator against the code in `venv/`: names against `__all__`, signatures
   against `inspect.signature`, commands and options against `--help`, config keys and defaults by
   writing a `runregistrykit.toml` in a temporary directory and reading it with
   `runregistrykit.client`, `package_provenance` run on a name not installed (correction 9). The
   pin lines equal the package README's "Installing". Every relative link resolves to a tracked
   file or a section; every external link is to `github.com/ds283/…` at a named tag or commit.
8. **E5, the Q5 sketch.** The README's sketch, copied out of the README by a script (not retyped),
   run by the orchestrator in the scratchpad: on the neutral store's `FACTORIES`; on a stand-in
   registry of the orchestrator's with a polymorphic `Parent.types` keyed by `int`, and a second
   with an `int` and a `str` of the same text; and the three breakages (a leaf added with no bump;
   a bump with no new pin; a class added), each failing as stated. A conversion that makes two keys
   alike is a finding.
9. **E6, U20.** `git diff f7c1b15 <commit> -- README.md` touches "Using it" only; every changed
   sentence checked against `client.py` and `fingerprint.py` at `9f8ebe4`, as correction 8: the
   relative roots still joined to the record root, the config and the fingerprinter's import the
   running tree's.
10. **E8, the suite and the records.** In `venv/` at the commit: `Ran 276 tests … OK`; `black --check
    runregistrykit docs` clean (27 files); `git status --short --ignored` the same before and after
    but for `__pycache__/`; no `var/`; this checkout the only worktree; no Ray process.
    - The log has every section of README §5.1 and the prompt's §4.5 additions: each client's
      commit, tree state and untouched-check before and after; the script's output for each client,
      whole, with its `cmp`; the fixture's output; every `path:line` with its text; every package
      statement with how it was checked; the Q5 sketch and its runs; (a)–(e); 276 → 276; the
      deviations classified (corrections 1–11 among them).
    - The board: the header; 07's row (landed, "this commit", 276 → 276); A1 ✅; G2–G4 each pointing
      at its checklist; E2 saying `v0.1.0` with `docs/adoption/secondarygwkit.md`;
      `[06-the-readme-places-the-fingerprinter-import-in-the-main-checkout]` moved to §4 with this
      commit; §3's opening count sentence. `docs/OPEN_ISSUES.md`: the row deleted, **2** by counting,
      the date. `prompts/INDEX.md`'s row says 07 landed. `PROVENANCE.md`: 07's section, after 06's,
      nothing above it changed.
    - The handover: E2's tag, commit and checklist path, for the orchestrator to report to the user;
      08 next.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 07* paragraph, in the form of
  06's (*At dispatch*, *The checks*, verdict). Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md` and in
    `PROVENANCE.md`;
  - "reviewed" for 07 in the board's header and row, README §2's status column and its header,
    and `prompts/INDEX.md`;
  - the **Orchestrator notes** line on the board, with this note marked "used for 07".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed, and the count, 276 → 276;
  - the script and its figures for each client, and what the corrections changed;
  - the facts in the checklists that change what a client must do (SGK's test helpers and deleted
    names, `fingerprint_of`'s format, the polymorphic keys, the unpromised patch);
  - the README's corrected worktree sentences;
  - the breakage, the agent's and the orchestrator's;
  - the issue closed, and the index at 2;
  - **E2**: `v0.1.0` (`9f8ebe4`, tag object `fd5ce48`) with `docs/adoption/secondarygwkit.md`, for
    SGK's `runregistry-extraction` 05–09 (README §7);
  - nothing pushed, and whether to push `main`.
