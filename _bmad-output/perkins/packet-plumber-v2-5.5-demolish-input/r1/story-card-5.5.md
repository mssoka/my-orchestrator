### Story 5.5 — Demolish input surface (restore from prototype)

- **Slice:** 5 · **Epic(s):** E7.2, E7.4 · **Systems:** Input surface `[ODN-12]` (mechanic: 2.3).
- **Goal.** The demolish MECHANIC (2.3 — `Cmd_Demolish_Pipe`/`Cmd_Demolish_Node`, merged #27)
  finally reachable from the input surface: click-select a pipe or junction on every left
  release, see a demolish popover + the X/DEL key, and watch the topology respond
  (bundle shrink, atomic junction batch). The missing third step of 3.5's launchable
  ("place routers, connect them, demolish and redesign").
- **Status:** implemented 2026-08-17 — PR open, in review (the demolish surface rides the 5.4 intent
  layer: release-based click-select (junction → pipe → clear on every left release), the demolish
  popover button + X/DEL, the shared `popover_demolish_hit` positive path pinned (W1-r4 — junction
  button → `Cmd_Demolish_Node`, pipe twin → `Cmd_Demolish_Pipe`, mouse == touch == pad on the node
  leg), the controller leg (dpad select → X confirm), the CLI arg-validation leg pinned (r3-N7),
  `pipe_anchor` single-sourced in render (N2-r4 fold); existing commands only — no new command
  kinds, no `LOG_VERSION` bump, replay byte-identical; the 2.3 demos/goldens (`demolish_bundle`,
  `demolish_node`) carry the T1+T2 pins).

**Given/When/Then:**
- **Given** the release-based click-select surface (prototype Perkins r2 B2 pattern: node
  → pipe → clear, on EVERY left release);
- **When** the player selects a pipe or junction and demolishes it (popover button or
  X/DEL);
- **Then** the EXISTING `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node` submits through the
  validated edit fast-path + action log (replay byte-identical `[E10]`; **no new command
  kinds, no `LOG_VERSION` bump**); a pipe demolish shrinks its bundle gracefully (traffic
  continues — only full-bundle-loss drops the route `[E1]`); a junction demolish runs the
  atomic batch (incident pipes in edge-id order, then the vertex `[E27]`); terminals never
  show a demolish affordance (`.Terminal_Demolish` mirrored in the UI `[E2]`); demolish is
  disabled while placing (no collision with the 1/2 lane keys, the right-click dial, or
  placement mode).

- **Edge-case contracts:** `[E1]` `[E2]` `[E10]` `[E27]` `[E29]`. **Golden:** T1 + T2 of
  pipe-demolish under a bundle (capacity shrink) + T1 + T2 of the junction-demolish batch
  (the E27 batch ORDER is pinned by the core's 2.3 tests — the golden pins the batch's
  end state); existing goldens MUST NOT shift (app-layer-only change).
- **Launchable increment:** build a net, demolish a pipe of a bundle (watch the capacity
  shrink), demolish a whole junction (atomic batch).
- **Assumption:** no economy — no refund, no inventory (the prototype's "refund banked"
  copy does NOT apply; refunds land with the economy story).
- **Slice:** 5 · **Epic(s):** E1.3, E1.4 · **Systems:** Input `[ODN-12]`, Topology demolish (S1).
- **Goal.** The 2.3 demolish mechanic was core-built and tested but never reachable in play —
  restore the prototype's select→demolish interaction: click-select a pipe/junction (on every
  left release), demolish via a popover button and/or X/DEL; rejects surface the existing
