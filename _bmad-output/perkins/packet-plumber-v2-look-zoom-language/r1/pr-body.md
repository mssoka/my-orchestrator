# look(zoom-language): the ruled half — scale covenant, laneless links, toward-space ladder, breathing camera

Implements the ruled half of the LOOK-SPEC (`_bmad-output/implementation-artifacts/look-node-legibility/LOOK-SPEC.md`, DESIGN LOCKS = `[ADOPTED 2026-08-26 user ruling]`): stories L1–L4 of the briefing's story ladder, one commit per story, green between. The sim is untouched — every commit is provably LOOK-layer (see Golden re-bless).

Skill note (the standing waiver): bmad-build's renderer is waived in this repo (no `_bmad/scripts/render_skill.py`; the 2026-08-21/23 sanctioned path). The briefing + LOOK-SPEC were the spec; bmad-build step-04 ran as the two-hunter review swarm (adversarial-general + edge-case-hunter) before this PR opened.

## The story ladder (spec citations per story)

### L1 — the scale covenant + the laneless link ladder (LOOK-SPEC §3)
- Links are SINGLE SOLID LANELESS strokes (the 3.3 spatial-lane stripes superseded — queues are ingress/egress on ROUTERS; the road doesn't gossip). The lane-detail reveal (7.1) retires with them.
- ONE ratio law at every tier: `link_width_capped` clamps every bundle at `LINK_RATIO_CAP` (0.5) of the SMALLER ENDPOINT node's drawn size — per bundle, at draw time, so a fat wide bundle serving a house clamps to that house. The stroke, its congestion halo, the selection halo, and the rider lattice share ONE width derivation.
- Per-rung width tables from the ruled storyboard mock (halved for the 26px tile): ACCESS/DISTRIBUTION uniform 4.5/3.5 (HUE carries the tier — copper/steel/gold tokens unchanged), CORE {3.5, 3.5, 6.0} — the skeleton at min stroke weight, only the wide backbone fattening (the mock's gold 12px).
- `LINK_FINISH :: Link_Finish.A_SOLID` (§3 fork 1b): finish A ships behind the compile-time switch; B/C are deliberately unimplemented — flipping the constant fails the COMPILE until the future ruling lands (byte-cheap-reversal).
- The casing retires (finish A is one stroke). Congestion halo / crisis recede / tie / drop marks keep their tokens (the encoding-table KEEPS).

### L2 — the toward-space zoom ladder (LOOK-SPEC §1)
- Rung machinery: `Zoom_Rung` + `zoom_rung_of` (cuts 1.6/1.25, stepped tables, no transcendentals); rides `camera_update` (app) and a new harness `zoom <z>` demo directive (view-only run setup — T1/replay never see it).
- Buildings/pucks shrink honestly per rung — nothing swaps for a symbol: `BUILDING_RUNG_FACTOR` 1.00/0.62/0.42, `HOST_RUNG_FACTOR` 1.00/0.78/0.41 (the DC landmark holds more size), `PUCK_RUNG_BASE` 1.05/0.80/0.50 × the rung-invariant tier bbox ratio.
- The dusk dial: warm dots (255,214,120) under every settlement building, the DC's cool anchor (120,190,255); alphas {0,120,200}/{0,140,210} — the ACCESS diorama is dark, DISTRIBUTION lights come on (small, dim), CORE burns. Radius rides the building's LIVE footprint (0.75/0.90) so the halo RINGS the silhouette. Static fills (rlsw-safe; quiet-at-rest).
- State travels up — the minimal honest encoder: a congested building's light shifts 50% toward the state token (amber/red). The full estate encoder stays a PARKED fork.

### L3 — the camera auto-breath (LOOK-SPEC §2)
- The shipped pullback machinery already keys the estate-seed event (`pullback_feed` → `camera_spawn_is_seed`), the wheel ALWAYS overrides (`camera_zoom_at` ends any pullback), the breath resumes only on the next seed, and boot lands INTIMATE (`DEFAULT_ZOOM` 2.0 home).
- NEW: reduced motion PINS the breath (7.3/E9.2) — `pullback_feed` gates on `a11y.reduced_motion` (composing with the N11 toggle), and `set_reduced_motion` ends an in-flight breath with the toggle. The player's own camera inputs are never touched. The dusk dots are static — "pins the light animations" is inherently satisfied.

### L4 — the node ladder, sprites-only Dublin, the ring floor (LOOK-SPEC §4)
- The ACCESS anchors move to the ruled ladder: home 1.00 · biz 1.10 · campus 1.22 · DC 1.35 (puck 1.05). The mock cross-check now reproduces the ruled DIST/CORE numbers from these anchors exactly (house 0.62/0.42, host 1.05/0.55 at the mock's 2-dp, puck 0.80/0.50).
- REAL Blender sprites ONLY — on BOTH maps: the Dublin street-aligned block path retires wholesale (block draw, street-segment grid + cache, `dublin_node_street`, `dublin_screen_tile` — a render function never called is not a feature). The type chip + family wash carry over.
- The Dublin family wash rides `DUBLIN_WASH_SCALE` 0.45 — ~55% lighter than the retired Dublin fill, so the sculpting reads. The procedural map keeps the shipped full-strength wash.
- Router tier rings: `tier_ring_thickness = max(2.0, 0.055 × tile_px × scale)` — the ≈2px SCREEN-SPACE floor (the D1 bump); token hues unchanged. The stroke-factor retune beyond this floor stays a PARKED fork.

## The rung-by-rung golden inventory

All T2 goldens re-blessed per story (deliberate, cause-documented). Every capture renders at the FIT = the CORE rung (thumbnails: houses 0.42 tiles, dusk glow on, skeleton links) except where a demo pins otherwise. T1 manifests + `.log.bin` replay logs are BYTE-IDENTICAL to the base in all three re-blesses (`git status` proves it — zero non-PNG golden changes, 110 + 113 + 113 PNGs): the sim, the action log, and the replay gate never saw a byte (ODN-1).

Per-rung pixel truths (palcheck section 2, fresh renders at ACCESS z=2.6 / DISTRIBUTION z=1.4 / CORE z=1.0):
- Stroke width == the ladder table at every rung (measured vs `link_base_world × scale`, ±2px): ACCESS 10.0 vs 10.8, CORE 4.0 vs 3.2.
- Toward-space shrink is monotone + honest: house roof presence 1299 > 161 > 41 px (ACCESS > DISTRIBUTION > CORE), ≥ 5× ACCESS:CORE.
- The dusk dial: ACCESS dark (0 px), DIST warm blend present (128 px), CORE warm (43 px) + the DC cool anchor (107 px) — the predicted land-tint composites.
- Laneless: zero lane-stripe tokens at every rung (against a fixture carrying express-heavy WFQ weights — the fixture that WOULD have painted them).
- Covenant at pixels: the measured stroke never exceeds 0.5 × the live house footprint.
- State up: a congested building's light reads the amber-shifted blend (present) and NOT the pure warm blend (absent).

## Mutation proofs (RED-then-GREEN, all run)

| # | Mutation | Fails |
|---|---|---|
| M1 | lane stripe reintroduction (express amber on the wire) | palcheck laneless zero-count at BOTH rungs (4645/652 px) |
| M2 | link base ×3 (ratio-law break) | table pin (13.5≠4.5) + covenant band + pixel width (the clamp visibly engaged: the drawn stroke measured 22px ≈ the derived cap 31.2×scale-ratio region — the RED is the table mismatch, the clamp engagement is the visible mechanism) |
| M3 | covenant clamp deletion | `covenant_clamp_engages_on_fat_bundles` + the sweep (Core/wide/4-member breaks) |
| M4 | symbol swap (flat disc above ACCESS) | shrink-monotone (1331 > 0 > 0) + CORE dusk/state legs |
| M5 | dusk dial off | all four dusk legs |
| M6 | reduced-motion gate deleted from the feed | `reduced_motion_pins_the_breath` |
| M7 | primitive block on Dublin | both Dublin sprite pins |
| M8 | ring floor 2.0 → 1.0 | the floor pin (1.32 ≠ 2.0) |
| M9 | house base 1.00 → 0.72 | three ladder pins |

## Parked-fork fence statement

NO work (not even preliminary) landed on: link finish 1b B/C variants (beyond the `LINK_FINISH` compile-time seam — B/C enum arms are comments; flipping the constant fails the compile), the router queue encoder, the tier-ring final spec beyond the 2px floor (`TIER_RING_FACTOR` stays 0.055), the quiet-board PRODUCTION swap (no board asset change; `dublin_board`'s golden shifts only from the node ladder), packet shapes/class colors (§6 — riders keep the existing lateral lattice, collapsed by the thinner stroke), HUD occlusion (§7), and the state-up-ladder encoder's final form (the shipped warm-amber node shift is the spec's minimal honest version).

## Verification

- 49/49 demos green (T1 + T2 + replay gate) after each re-bless; `harness run` 3×.
- 468 unit tests: core 280, app 51, app/render 114, input 13, audio 18, harness 2.
- palcheck all green (sections 1–7), drift-check 353/353 rejected, preview-check 7/7, motion-pixel PASS, stats byte-identity, input-parity 27/27, PP_DEBUG builds + smoke, font-guard, lint.
- Zero CI-relevant flake: local ground truth (remote CI billing-block noted once, per briefing).

## Decisions & rationale

- **Covenant reference = the tier's endpoint class** (the mock's own reading): access-tier strokes measure against the house; the wide backbone against the DC host. The mock's gold backbone is 0.55 of a house BY RULING and comfortably in-law vs its routers/host endpoints. `link_width_capped` enforces the same endpoint-relative law at draw time (a wide pipe serving a house clamps to the house).
- **CORE mid tier flattened to 3.5** (not the mock's point-measured steel 8px→4.0): "links stay the visible skeleton at MIN stroke weight" — only the backbone fattens at CORE. Also avoids a transient covenant edge pre-L4. No demo uses mid pipes; zero golden impact.
- **DC = the Content_Host role** (the mock's "dc" position pastes the host sprite; the dc sprite stays unwired as shipped). The §4 "DC 1.35" anchor lands on `sprite_host_target`.
- **Dusk dot radius rides the live footprint** (0.75/0.90), not absolute tiles: our blit trims to the content bbox (the mock's paste carried transparent padding), so any smaller under-dot is invisible — the read is the halo RINGING the silhouette, and it survives the L4 base changes automatically.
- **Rider lattice unchanged in shape** (Fork 2 is open/parked): the lattice width derives from the clamped stroke, so riders compress toward the centerline on thin strokes — the natural fallout of the covenant, no packet-side work.
- **`lane_detail` deleted, not kept dead**: the 7.1 focus-reveal canon is superseded by the laneless ruling; `zoom_rung` subsumes the tiering. The zoomed-lane palcheck leg became the laneless + covenant pixel gate.
- **All demos capture at the fit (CORE)** — any zoom > 1.0 clips the 40-tile juice cluster. The sprite-presence canaries that degenerated at thumbnail scale re-pinned to measured counts (~50%) or tone bands (LED, campus brick), with the measured values in the comments. The strong exact-hex presence pins live where the sprites are big: the ACCESS-leg fresh renders (section 2) + the blessed corpus's own crop-canary geometry.
- **The seed-7 fixture sits ON LAND** (the map is water+islands; the dusk-blend predictions composite over the land tint (239,228,186) — measured, documented in the constants).
- **bmad-build renderer waived** (the standing 08-21/23 path: no `render_skill.py` in-repo); the briefing + LOOK-SPEC were the spec; step-04 ran as the two-hunter swarm.

## Review

step-04 review swarm (mandatory): bmad-review-adversarial-general + bmad-review-edge-case-hunter on glm-5.3 (thinking max), launched synchronously against the full code diff; findings triaged per the step-04 classify rules and folded in this PR:

- **Folded (patch)** — adversarial r1: the covenant sweep + fat-bundle test were VACUOUS (the unit fixture never loaded sprite bboxes → every router endpoint's drawn size was 0 → cap 0 → the sweep passed crushed; the hunter probed cap=0.000, natural=10.5). Fix: real puck bboxes in the fixtures (the loader's documented defaults), the fat fixture moved to a 16-port router_high (needs ≥5 members to pass the REAL cap 13.0), the sweep's doc states its honest scope (it detects clamp deletion + derivation drift; the table pins catch fattening); the crisis OUTLINE still drew the UNCAPPED width (the halo/selection/riders were migrated, the outline missed) → `link_width_capped` threaded; the pixel width leg's tolerance tightened 2.0→1.0 (always-ACCESS rung-deafness passed at ±2 — deltas 1.29/0.92px) with the comment corrected; a leftover debug PNG export removed; stale canvas→land blend comment. Edge-case r1: `set_reduced_motion` cleared the pullback FLAG but left the breath's targets — camera_update's ease runs unconditionally, so the map kept gliding to the abandoned target at the FASTER normal rate (BLOCKER) → the targets freeze at the live values and the test asserts zero residual motion; the assist candidate halo kept the retired ×2.2 band factor (the commit frame popped ~2.2× the stroke) → glow margin only; the assist route glow + `wire_paths_compute`/fan stubs now ride the capped width (the flags-on path obeys the covenant where it bites); the NaN-zoom parse guard; the tie-glow rung companion; the cut pins use the named camera constants with coupling pins.
- **Rejected with rationale** — "the covenant pixel leg cannot fail on a clamp regression": true by contract — the leg pins width==table; the clamp has its own dedicated unit test (`covenant_clamp_engages_on_fat_bundles`) whose M3 deletion the hunter verified RED.
- **Deferred** — the primitive fallback path (documented unreachable) ignores the rung tables; and the pre-existing N11 auto-pullback toggle shares the latent ease-continues behavior (pre-dates this story; `set_reduced_motion` shows the fix shape) → both filed for a focused follow-up.

