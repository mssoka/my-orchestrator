# Lens: Codebase Fit (Perkins r1 — packet-plumber-v2-2.1-bundles)

Reality check against the ACTUAL codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match (e.g. `pp.Bundles`, `pp.node_slot`, `tier_pipe_color`, `tier_pipe_width`, `pipe_slot`, `topology_apply_edit`, `record_run`, `clone_log`, `flow_seed_demand`, `test_seed_fixture`, `run_init`/`run_destroy`, `step_n`, `draw`)?
- Are naming conventions and style consistent with the rest of the project (Odin stdlib style: types `Ada_Case`, procs/vars `snake_case`, files `snake_case.odin`)?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.) Specifically: is `bundles_rebuild`'s pair-keying / linear-scan duplicating a pattern already in `routing.odin` or `topology.odin`?
- Are new dependencies/imports available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them.)
- Does it leave orphan code — functions/exports/types no longer referenced after this change (e.g. is the old `draw_pipes` fully replaced by `draw_bundles`? any stale `pipe_lb_mode`/`Lb_Mode` references left behind)?
- Does the call-site update of `draw_world` / `capture_frame` cover ALL callers? (grep the whole repo — app + harness.)

## Inputs
- **Diff:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/diff.patch`
- **Worktree (verify here — grep/read the real files):** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.1-bundles-r1`
- **Context:** `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-2.1-bundles-r1.md` (lens-guards) and worktree `project-context.md`.

## ⚠️ Lens-guards (prevent false positives)
- The new `Bundles` type and its procs are INTENDED additions — do not flag them as "orphan" just because they're new; verify whether they're actually wired in (they should be, via `Run_State.bundles` + `step` + `flow` + render).
- **NO LB is correct** — absence of `Lb_Mode`/`pipe_lb_mode` is the PROTO→FULL transition the architecture mandates (~line 860). If those symbols are GONE, that's correct, not an orphan/dangling-reference bug. (If a stale reference to a deleted `Lb_Mode` REMAINS and would fail to compile, THAT is a real finding — but `odin test core` is green, so verify carefully.)
- **Derived (not serialized) bundle state is by design.**
- Don't flag em-dashes / the `v2` base / re-open 1.1–1.4.

## OUTPUT
Write ONLY a valid JSON array to: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/codebase.json`
Schema:
```
{ "source":"codebase", "severity":"blocker"|"warning"|"note", "category":"<tag, e.g. orphan, dup, convention>",
  "title":"<one-line>", "location":"<file:line|hunk|N/A>",
  "evidence":"<exact lines READ from worktree/diff, verbatim>",
  "detail":"<≤40 words>", "recommended_fix":"<≤40 words>" }
```
ONLY the JSON array in the file. `[]` is valid. Accuracy > volume — grep the repo to confirm each claim. When done: "codebase lens done — N findings".
