# Lens: codebase (Codebase Fit) — Perkins r1

**OUTPUT FILE:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/codebase.json`

First read the common context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/_lens_common.md`

## Your lens
Reality check against the ACTUAL codebase (read files to verify — do not
assume):
- Do files, functions, types, and imports referenced in the diff actually exist
  and match? (e.g. `pipe_slot`, `pipe_other`, `node_slot`, `node_slot_raw`,
  `pipe_tier_index`, `node_type_index`, `routing_next_hop`, `routing_has_path`,
  `routing_rebuild`, `flow_step`, `flow_seed_demand`, `packet_progress_frac`,
  `event_emit`, `EVENT_TAG_PACKET_ARRIVED`, `state_hash`, `record_run`)
- Are naming conventions and style consistent with the rest of the project
  (Odin stdlib style: `Ada_Case` types, `snake_case` procs)?
- Does the diff duplicate logic that already exists elsewhere? (e.g. is there
  already a `pipe_slot`/`pipe_other`/neighbor primitive it should reuse?)
- Are new symbols orphaned (defined but never called)? Check `Spawn_Intent`,
  `spawn_tick`, `load_demo_spawns`, `routing_has_path`, `EVENT_TAG_PACKET_ARRIVED`.
- Do the new tests (`flow_test.odin`) reference helpers that exist
  (`test_seed_fixture`, `pipe_tier_index`, `run_init`, `run_destroy`)?
- `spawn_tick` (demo.odin) vs `lower_spawns` (run.odin) — both compute the spawn
  tick; verify they AGREE (both `floor(at_ms*hz/1000)`, no +1) or flag the
  inconsistency.

## Output
Write ONE valid JSON array to your OUTPUT FILE (source = `"codebase"`). `[]` is
valid. Accuracy > volume. Then print `LENS DONE: codebase` and stop.
