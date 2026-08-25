# LENS: Codebase Fit (source = `codebase`)

First load the shared context: read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/prompts/_shared.md` (lens-guards, output schema + contract, empirical gate status, canonical input paths). Follow it exactly.

## YOUR LENS — reality check against the actual codebase
Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (e.g. `pp.Catalogs`, `pp.Cmd_Draw_Pipe`, `pp.topology_apply_edit`, `pp.validate_draw`, `pp.span_between`, `pp.draw_cost`, `pp.node_slot`, `rnd.View`, `rnd.Drag_State`, `rnd.draw_world`, `rnd.from_screen`, `rnd.palette_load`, `rnd.view_compute`, `pp.pipe_tier_index`, `pp.node_type_index`, `pp.topology_spawn_node`, `replay_hashes`, `read_manifest`, `manifest_path`, `log_path`, `list_demos`, `write_file`, `free_all`.)
- Are naming conventions and style consistent with the rest of the project (Odin stdlib style: types `Ada_Case`, procs `snake_case`)?
- Does the diff DUPLICATE logic that already exists elsewhere? In particular: the `load_catalogs` proc is defined BOTH in `app/main.odin` and `harness/catalogs.odin` (near-identical file-IO), and `seed_fixture` is defined BOTH in `app/main.odin` and `harness/catalogs.odin` — is this intentional per-layer ownership or a copy-paste drift risk? Point to both in `location`.
- Are new dependencies (imports, packages) available? `vendor:raylib` in app/harness — present?
- Are there existing tests this diff likely breaks? (The 1.1 `determinism_test.odin` was rewritten — did anything in `core/rng_test.odin` or elsewhere break? `odin test core` is green — confirm the test set is coherent.)
- Does it leave orphan code — functions/exports/types no longer referenced after this change? (e.g. is `Applied_Cmd` fully removed? is `CMD_TAG_SET_ARG` fully gone? is the old harness `Catalogs`/`Balance_File`/`load_catalogs` fully removed?)
- **From-scratch check (lens-guard #7):** compare `app/render/view.odin` + `core/topology.odin` against the Godot prototype at `/Users/moses/code/packet-plumber-prototype-ref`. Flag any wholesale copy of the prototype's render/topology code (data-value reuse is allowed; line-for-line logic port from GDScript is not).

## OUTPUT
Write ONE valid JSON array (schema + contract in `_shared.md`) to:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/codebase.json`

`source` = `"codebase"`. Only the JSON array in the file. `[]` is valid. Verify every claim by reading the actual code; quote exact lines in `evidence`. When done, stop.
