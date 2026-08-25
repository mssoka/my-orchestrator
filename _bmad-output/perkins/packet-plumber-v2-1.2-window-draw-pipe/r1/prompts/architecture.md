# LENS: Architecture (source = `architecture`)

First load the shared context: read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/prompts/_shared.md` (lens-guards, output schema + contract, empirical gate status, canonical input paths). Follow it exactly.

## YOUR LENS — architectural fit
Given the diff and the surrounding codebase + the Odin architecture doc (`{worktree}/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`):
- Does it follow existing patterns and conventions (ODN spine, the §11.1 command-application convention, the §10.x golden tiers)?
- Does it introduce unnecessary coupling between modules — especially the ODN-1 core/app boundary? Does any `package core` type now depend on something it shouldn't (engine, OS, time)? Does the app reach into core internals it shouldn't?
- Is there a simpler alternative with the same outcome? Any premature abstraction (e.g. the `Edit_Result`/`Edit_Error` split, the `Command_Kind` union with one variant)?
- Does it respect module boundaries and separation of concerns — core (pure sim) / app (engine+view) / harness (golden runner)? Is the render package correctly read-only on the topology (ODN-1: the view never perturbs sim state)?
- Will it create technical debt or make future stories (1.3 flow, demolish, lane-weights) harder? The arch comments claim later commands append as new union variants — is that actually clean here?
- Does complexity match the problem? (e.g. is the `isqrt`+round-half-up integer metric justified vs. a simpler model? is the rlsw readback normalization sound?)
- The two `load_catalogs` procs (one in `app/main.odin`, one in `harness/catalogs.odin`) and the two `seed_fixture` procs (app + harness) — is that duplication a real coupling/debt risk, or acceptable (each layer owns its IO)?

## OUTPUT
Write ONE valid JSON array (schema + contract in `_shared.md`) to:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/architecture.json`

`source` = `"architecture"`. Only the JSON array in the file. `[]` is valid. Verify every claim by reading the actual code; quote exact lines in `evidence`. When done, stop.
