# Story 7.5 card + decision-log 2026-08-19 (extracted verbatim from the reviewed tree)

## stories-v2.md §Story 7.5
### Story 7.5 — Wire aesthetics (routing + junction shaping, shipped as infrastructure)

- **Slice:** 7 · **Epic(s):** E8.1 · **Systems:** View draw pass `[ODN-1]`.
- **Goal.** The network LOOKS engineered, not scribbled (user ruling 2026-08-17: "want it"):
  the drawn wire path is a presentation-only, deterministic polyline that (1) detours around
  crossings with other pipes (preferring to SLIDE alongside), node/terminal sprites, and the
  map edge, (2) attaches at router puck-rim anchors allocated evenly around the disc (the
  clean 4-pipe ✕/＋ read), and (3) renders parallel-pipe bundles as ONE ribbon that fans open
  at each end into the member anchors — with graceful degradation to STRAIGHT whenever a
  detour would be longer/uglier than the crossing.

**Given/When/Then:**
- **Given** the view layer + topology + bundles;
- **When** the game renders;
- **Then** every drawn pipe follows a deterministic polyline (same map → same paths, no RNG,
  no seed, no sim mutation — ODN-1); pipe cost stays on the LOGICAL straight A→B geometry
  (`pipe_span × cost_per_tile`), never the drawn detour (T1 state-hashes + replay logs
  byte-identical `[E10]`); a router with n incident pipes shows n anchors evenly spread on
  the puck (n=4 → 90°); a count>1 bundle draws as one ribbon fanning into its member anchors;
  and a detour longer than straight × `WIRE_DETOUR_MAX_LEN_RATIO` falls back to straight.

- **Edge-case contracts:** view-reads-snapshot `[ODN-1]`, cost-immunity + determinism pins
  (the wire_path_test suite), degradation thresholds (`WIRE_DETOUR_MAX_LEN_RATIO` /
  `WIRE_DETOUR_MAX_BENDS` / `WIRE_SLIDE_GUTTER` / `WIRE_STUB_TILES` — render-side constants,
  never catalog-poisoned), no-transcendentals (CIRCLE16 rotation only — §10.4). Terrain-aware
  routing (rivers) = named follow-up, FLAG not build.
- **SHIPPED VERDICT (lavish gate 2026-08-19, recorded verbatim):** r1 *"straight looks better
  for a network topology"*; r2 **"Ship pure straight (routing OFF, anchors OFF) — Story 7.5
  becomes routing-only infrastructure."** The mechanism ships complete + tested + cost-immune
  behind two View flags (`route_wires`, `wire_anchors`); the shipped render keeps both OFF, so
  **T2 goldens are byte-identical — NO re-bless** (the harness run proves it; the strongest
  cost-immunity evidence).
- **Golden:** none needed (verdict C: shipped flags off → the blessed T2 frames are untouched;
  T1 + replay byte-identical by construction).
- **Launchable increment:** the wire-draw layer carries the full routing/junction-shaping
  machinery, one flag from a future aesthetic ruling; today's look is unchanged.
- **Status:** implemented 2026-08-19 — the pure path module `app/render/wire_path.odin`
  (detour scan + bend insertion + anchor allocation + ribbon fan + arc-length sampling), the
  View flags + legacy-byte-identical branches in `draw_bundles`/`draw_packets`/
  `draw_selection`/`draw_crisis_outlines`/`draw_glow_edge`, the cost-immunity +
  determinism + degradation + junction-shaping pins (`app/render/wire_path_test.odin`,
  6 tests green), the gate tool `harness wire-preview` (routed / anchors / straight frames +
  close-ups), the lavish-gated verdict recorded verbatim above, and the local CI 10/10.

**→ Slice 7 exit: the FUN-TEST GATE (the E1–E9 core is complete).** Run the playtest (both
audiences). **Pass → greenlight slice 8+ + content; fail → iterate via the data catalogs

## decision-log.md 2026-08-19 entry
## 2026-08-19 — Wire aesthetics (Story 7.5): the mechanism ships as infrastructure; the look stays straight

- **Decision:** the user ruling 2026-08-17 ("want it" — the network LOOKS engineered, not
  scribbled) ships as **Story 7.5**: a presentation-only, deterministic wire-path layer that
  detours around crossings/sprites/edges, spreads router anchors evenly around the puck rim,
  and renders parallel-pipe bundles as one ribbon that fans open at each end — with graceful
  degradation to straight. Cost stays on the LOGICAL straight segment (`pipe_span ×
  cost_per_tile`); T1 state-hashes + replay logs are byte-identical `[E10]`; the view never
  perturbs the sim `[ODN-1]`.
- **Style verdict (lavish gate, 2026-08-19, recorded verbatim):** r1 — *"straight looks better
  for a network topology"* (the detour look rejected); r2 — **"Ship pure straight (routing
  OFF, anchors OFF) — Story 7.5 becomes routing-only infrastructure."** The mechanism ships
  complete + tested + cost-immune behind two View flags (`route_wires`, `wire_anchors`); the
  shipped render keeps both OFF.
- **Consequences (applied in this job):** the pure path module `app/render/wire_path.odin` +
  the flags/branches in the view consumers + the 6-test pin suite (cost immunity, determinism,
  degradation, anchor even-spread, ribbon fan) + the `harness wire-preview` gate tool + the
  legacy-byte-identical draw branches. **NO T2 re-bless** (verdict C: shipped flags off →
  the blessed frames are untouched; the harness run proves zero golden shift). A future
  aesthetic ruling flips the flags; terrain-aware routing (rivers) stays a named follow-up.
