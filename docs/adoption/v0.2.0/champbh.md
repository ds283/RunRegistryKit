# Adopting `v0.2.0`: ChamPBH (CPBH)

- **Client:** ChamPBH, `/Users/ds283/Documents/Code/ChamPBH`, at **`3cd2be4`** (branch `main`,
  2026-10-17, "Add the late-time matter fraction to the field-equations audit"), three commits after
  `c21cdfb`, the commit its `v0.1.0` checklist was measured at; the three add audit documents.
- **Package:** `runregistrykit` as it is tagged **`v0.2.0`**.
- **How it was read:** by this repository's `interrupted-runs` prompt 06 on 2026-10-18, through
  `git -C <CPBH> show 3cd2be4:<path>` and `git -C <CPBH> grep … 3cd2be4` only. Nothing of CPBH was
  imported, run or opened. **CPBH's adoption campaign measures again before acting, and its numbers
  govern.** This is data, not instructions.

**CPBH has adopted no release.** It adopts after its `dk-and-rpk-migration` campaign, and it
adopts **`v0.2.0` directly**: there is no `v0.1.0` step to take first.

## 1. Its checklist still describes the move

[`../champbh.md`](../champbh.md), written against `v0.1.0` at `c21cdfb`, still describes what CPBH
deletes, adds and rewrites, its runs, stores and tests, its Q5 guard and its acceptance, with two
changes:
- **the pin is `v0.2.0`** in place of `v0.1.0`, everywhere the checklist writes one: with the store
  layer `runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0`, beside
  CPBH's own `datastorekit` line; for the core only `runregistrykit @
  git+https://github.com/ds283/RunRegistryKit@v0.2.0`;
- **the checks of [`README.md`](README.md) §3 are added**: any comparison of its own with
  `liveness`'s values, `TERMINAL_STATES`, a store refusal's text, a test that begins two unfinished
  runs on one store, a caller of `pid_alive` that relied on its raising, and a test that pins a
  record's key set. CPBH has no such code today (§2), so each applies to what it writes when it
  adopts.

The checklist itself is not rewritten (documents under `docs/` are additive).

## 2. What it holds at `3cd2be4`

`git show 3cd2be4:requirements.txt`: `:17` `datastorekit @
git+https://github.com/ds283/DatastoreKit@v0.4.0`, which satisfies the extra's floor; `:79`
`ray==2.53.0`; `:80` `raypoolkit @ git+https://github.com/ds283/RayPoolKit@v0.2.0`; `:91`
`SQLAlchemy==2.0.46`. No `runregistrykit` line.

`$ git -C <CPBH> grep -n -i runregistrykit 3cd2be4` finds nine lines, none of them code:
- `ObjectFactories/tests/test_inventory_specs.py:27`, a docstring saying that the fingerprint of
  RunRegistryKit, which CPBH is expected to adopt, reads only what the specs declare;
- `prompts/dk-and-rpk-migration/09-port-the-inventory.md:47`, `:260`;
- `prompts/dk-and-rpk-migration/IMPLEMENTATION_STATE.md:47`;
- `prompts/dk-and-rpk-migration/README.md:1006`, `:1011`, `:1019`;
- `prompts/dk-and-rpk-migration/logs/09-port-the-inventory.md:714`;
- `prompts/dk-and-rpk-migration/orchestrator/prompt-09.md:36`.

`$ git -C <CPBH> grep -n -i -E '^\s*(import|from) runregistrykit' 3cd2be4` finds nothing: CPBH's
tracked code imports nothing of the registry and begins no run. Its `var/`, if it has one, is
not in `git` and was not read; 05's planner found no run directory under it
([`05-begin-refuses-a-second-writer.md`](../../../prompts/interrupted-runs/05-begin-refuses-a-second-writer.md),
"At writing", "The cost"). So, as far as `git` shows, no record of CPBH's needs reading under
`v0.2.0`, and the mixed-version table (release notes §4) bears on it only if a `v0.1.0` checkout
of CPBH ever shares a runs root with a `v0.2.0` one, which adopting `v0.2.0` directly avoids.
