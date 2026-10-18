# Adopting `v0.2.0`: StochasticInstantons (SI)

- **Client:** StochasticInstantons, `/Users/ds283/Documents/Code/StochasticInstantons`, at
  **`5fb4a1d`** (branch `dk-and-rpk-migration`, 2026-10-12, "Write the rehearsal-lock handover note
  for ChamPBH and SecondaryGWKit"), its newest commit of any branch on 2026-10-18 and the commit its
  `v0.1.0` checklist was measured at.
- **Package:** `runregistrykit` as it is tagged **`v0.2.0`**.
- **How it was read:** by this repository's `interrupted-runs` prompt 06 on 2026-10-18, through
  `git -C <SI> show 5fb4a1d:<path>` and `git -C <SI> grep … 5fb4a1d` only. Nothing of SI was
  imported, run or opened. **SI's adoption campaign measures again before acting, and its numbers
  govern.** This is data, not instructions.

**SI has adopted no release.** It adopts after its `dk-and-rpk-migration` campaign, and it adopts
**`v0.2.0` directly**: there is no `v0.1.0` step to take first.

## 1. Its checklist still describes the move

[`../stochasticinstantons.md`](../stochasticinstantons.md), written against `v0.1.0` at `5fb4a1d`,
still describes what SI deletes, adds and rewrites, its runs, stores and tests, its Q5 guard and
its acceptance, with two changes:
- **the pin is `v0.2.0`** in place of `v0.1.0`, everywhere the checklist writes one: for the core,
  `runregistrykit @ git+https://github.com/ds283/RunRegistryKit@v0.2.0`; for the store layer,
  later, `runregistrykit[stores] @ git+https://github.com/ds283/RunRegistryKit@v0.2.0` beside a
  `datastorekit` line of SI's own;
- **the checks of [`README.md`](README.md) §3 are added**: any comparison of its own with
  `liveness`'s values, `TERMINAL_STATES`, a store refusal's text, a test that begins two unfinished
  runs on one store, a caller of `pid_alive` that relied on its raising, and a test that pins a
  record's key set. SI has no such code today (§2), so each applies to what it writes when it
  adopts.

The checklist itself is not rewritten (documents under `docs/` are additive). As it says (its
"In one paragraph" and §1), **SI pins no `datastorekit`** at `5fb4a1d`, so it can adopt the core
now and the store layer only once its `dk-and-rpk-migration` has landed and it adds that line;
`v0.2.0` changes none of that, since the extra's floor is still `datastorekit>=0.4.0`.

## 2. What it holds at `5fb4a1d`

`git show 5fb4a1d:requirements.txt`: `:57` `ray==2.55.1`; `:65` `SQLAlchemy==2.0.46`. No
`runregistrykit`, `datastorekit` or `raypoolkit` line.

`$ git -C <SI> grep -n -i runregistrykit 5fb4a1d` finds three lines, none of them code:
- `.prompts/dk-and-rpk-migration/IMPLEMENTATION_STATE.md:179`, `:180`;
- `.prompts/dk-and-rpk-migration/README.md:1156`.

`$ git -C <SI> grep -n -i -E '^\s*(import|from) runregistrykit' 5fb4a1d` finds nothing: SI's
tracked code imports nothing of the registry and begins no run. Its `var/`, if it has one, is
not in `git` and was not read; 05's planner found no run directory under it
([`05-begin-refuses-a-second-writer.md`](../../../prompts/interrupted-runs/05-begin-refuses-a-second-writer.md),
"At writing", "The cost"). So, as far as `git` shows, no record of SI's needs reading under
`v0.2.0`.
