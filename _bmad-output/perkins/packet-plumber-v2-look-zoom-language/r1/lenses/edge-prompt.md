You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your working directory IS the reviewed worktree (a detached checkout at the reviewed state) — read files here. You are a reviewer: do NOT modify, create (except your one output JSON), or fix anything in the repository.

--- PROJECT CONVENTIONS ---
none

--- DIFF ---
diff --git a/_bmad-output/implementation-artifacts/deferred-work.md b/_bmad-output/implementation-artifacts/deferred-work.md
index c4c2095..0eee7d9 100644
--- a/_bmad-output/implementation-artifacts/deferred-work.md
+++ b/_bmad-output/implementation-artifacts/deferred-work.md
@@ -15,3 +15,10 @@
 - source_spec: `_bmad-output/implementation-artifacts/spec-viscomm-crisis-duck.md`
   summary: dublin_node_block_draw's fill triangles are BACKFACE-CULLED for some street orientations (street-dependent winding renders CW quads as nothing in BOTH renderers — only the frontage edge + chip render there; pre-existing, the blessed dublin goldens carry the missing fills)
   evidence: crisis-duck B1 probe 2026-08-26: deleting the block FILL recede alone changes zero pixels at the palcheck fixture nodes (both culled), while the edge-line deletion flips the gate; the 08-23 field note names the winding rule (CCW front) — a cross-product orientation fix + golden re-bless belongs in its own job
+
+- source_spec: `packet-plumber-v2-look-zoom-language` (LOOK §1-§4, step-04 review defer)
+  summary: the primitive-fallback terminal draw (documented unreachable while the committed sprite sheet loads) ignores the LOOK rung tables — host 1.15 vs the ruled 1.35, no rung factors, unscaled fam wash on Dublin.
+  evidence: adversarial+edge-case review r1 (NOISE/defer class); app/render/view.odin draw_building fallback branch — inert unless the sheet goes missing, but it would render the pre-LOOK ladder if it ever ran.
+- source_spec: `packet-plumber-v2-look-zoom-language` (LOOK §2, step-04 review defer)
+  summary: the N11 auto_pullback settings toggle shares the latent ease-continues behavior set_reduced_motion had — flipping it OFF mid-flight clears the flag but leaves the breath's targets easing.
+  evidence: edge-case-hunter r1 finding 1's mechanism (camera_update's ease is unconditional; the flag only sets the rate). Pre-dates this story (shipped v2-camera-zoom behavior); set_reduced_motion's target-freeze is the fix shape. A player flipping N11 mid-breath sees the camera finish gliding at the normal rate.
diff --git a/_pr_body_look.md b/_pr_body_look.md
new file mode 100644
index 0000000..65f7276
--- /dev/null
+++ b/_pr_body_look.md
@@ -0,0 +1,87 @@
+# look(zoom-language): the ruled half — scale covenant, laneless links, toward-space ladder, breathing camera
+
+Implements the ruled half of the LOOK-SPEC (`_bmad-output/implementation-artifacts/look-node-legibility/LOOK-SPEC.md`, DESIGN LOCKS = `[ADOPTED 2026-08-26 user ruling]`): stories L1–L4 of the briefing's story ladder, one commit per story, green between. The sim is untouched — every commit is provably LOOK-layer (see Golden re-bless).
+
+Skill note (the standing waiver): bmad-build's renderer is waived in this repo (no `_bmad/scripts/render_skill.py`; the 2026-08-21/23 sanctioned path). The briefing + LOOK-SPEC were the spec; bmad-build step-04 ran as the two-hunter review swarm (adversarial-general + edge-case-hunter) before this PR opened.
+
+## The story ladder (spec citations per story)
+
+### L1 — the scale covenant + the laneless link ladder (LOOK-SPEC §3)
+- Links are SINGLE SOLID LANELESS strokes (the 3.3 spatial-lane stripes superseded — queues are ingress/egress on ROUTERS; the road doesn't gossip). The lane-detail reveal (7.1) retires with them.
+- ONE ratio law at every tier: `link_width_capped` clamps every bundle at `LINK_RATIO_CAP` (0.5) of the SMALLER ENDPOINT node's drawn size — per bundle, at draw time, so a fat wide bundle serving a house clamps to that house. The stroke, its congestion halo, the selection halo, and the rider lattice share ONE width derivation.
+- Per-rung width tables from the ruled storyboard mock (halved for the 26px tile): ACCESS/DISTRIBUTION uniform 4.5/3.5 (HUE carries the tier — copper/steel/gold tokens unchanged), CORE {3.5, 3.5, 6.0} — the skeleton at min stroke weight, only the wide backbone fattening (the mock's gold 12px).
+- `LINK_FINISH :: Link_Finish.A_SOLID` (§3 fork 1b): finish A ships behind the compile-time switch; B/C are deliberately unimplemented — flipping the constant fails the COMPILE until the future ruling lands (byte-cheap-reversal).
+- The casing retires (finish A is one stroke). Congestion halo / crisis recede / tie / drop marks keep their tokens (the encoding-table KEEPS).
+
+### L2 — the toward-space zoom ladder (LOOK-SPEC §1)
+- Rung machinery: `Zoom_Rung` + `zoom_rung_of` (cuts 1.6/1.25, stepped tables, no transcendentals); rides `camera_update` (app) and a new harness `zoom <z>` demo directive (view-only run setup — T1/replay never see it).
+- Buildings/pucks shrink honestly per rung — nothing swaps for a symbol: `BUILDING_RUNG_FACTOR` 1.00/0.62/0.42, `HOST_RUNG_FACTOR` 1.00/0.78/0.41 (the DC landmark holds more size), `PUCK_RUNG_BASE` 1.05/0.80/0.50 × the rung-invariant tier bbox ratio.
+- The dusk dial: warm dots (255,214,120) under every settlement building, the DC's cool anchor (120,190,255); alphas {0,120,200}/{0,140,210} — the ACCESS diorama is dark, DISTRIBUTION lights come on (small, dim), CORE burns. Radius rides the building's LIVE footprint (0.75/0.90) so the halo RINGS the silhouette. Static fills (rlsw-safe; quiet-at-rest).
+- State travels up — the minimal honest encoder: a congested building's light shifts 50% toward the state token (amber/red). The full estate encoder stays a PARKED fork.
+
+### L3 — the camera auto-breath (LOOK-SPEC §2)
+- The shipped pullback machinery already keys the estate-seed event (`pullback_feed` → `camera_spawn_is_seed`), the wheel ALWAYS overrides (`camera_zoom_at` ends any pullback), the breath resumes only on the next seed, and boot lands INTIMATE (`DEFAULT_ZOOM` 2.0 home).
+- NEW: reduced motion PINS the breath (7.3/E9.2) — `pullback_feed` gates on `a11y.reduced_motion` (composing with the N11 toggle), and `set_reduced_motion` ends an in-flight breath with the toggle. The player's own camera inputs are never touched. The dusk dots are static — "pins the light animations" is inherently satisfied.
+
+### L4 — the node ladder, sprites-only Dublin, the ring floor (LOOK-SPEC §4)
+- The ACCESS anchors move to the ruled ladder: home 1.00 · biz 1.10 · campus 1.22 · DC 1.35 (puck 1.05). The mock cross-check now reproduces the ruled DIST/CORE numbers from these anchors exactly (house 0.62/0.42, host 1.05/0.55 at the mock's 2-dp, puck 0.80/0.50).
+- REAL Blender sprites ONLY — on BOTH maps: the Dublin street-aligned block path retires wholesale (block draw, street-segment grid + cache, `dublin_node_street`, `dublin_screen_tile` — a render function never called is not a feature). The type chip + family wash carry over.
+- The Dublin family wash rides `DUBLIN_WASH_SCALE` 0.45 — ~55% lighter than the retired Dublin fill, so the sculpting reads. The procedural map keeps the shipped full-strength wash.
+- Router tier rings: `tier_ring_thickness = max(2.0, 0.055 × tile_px × scale)` — the ≈2px SCREEN-SPACE floor (the D1 bump); token hues unchanged. The stroke-factor retune beyond this floor stays a PARKED fork.
+
+## The rung-by-rung golden inventory
+
+All T2 goldens re-blessed per story (deliberate, cause-documented). Every capture renders at the FIT = the CORE rung (thumbnails: houses 0.42 tiles, dusk glow on, skeleton links) except where a demo pins otherwise. T1 manifests + `.log.bin` replay logs are BYTE-IDENTICAL to the base in all three re-blesses (`git status` proves it — zero non-PNG golden changes, 110 + 113 + 113 PNGs): the sim, the action log, and the replay gate never saw a byte (ODN-1).
+
+Per-rung pixel truths (palcheck section 2, fresh renders at ACCESS z=2.6 / DISTRIBUTION z=1.4 / CORE z=1.0):
+- Stroke width == the ladder table at every rung (measured vs `link_base_world × scale`, ±2px): ACCESS 10.0 vs 10.8, CORE 4.0 vs 3.2.
+- Toward-space shrink is monotone + honest: house roof presence 1299 > 161 > 41 px (ACCESS > DISTRIBUTION > CORE), ≥ 5× ACCESS:CORE.
+- The dusk dial: ACCESS dark (0 px), DIST warm blend present (128 px), CORE warm (43 px) + the DC cool anchor (107 px) — the predicted land-tint composites.
+- Laneless: zero lane-stripe tokens at every rung (against a fixture carrying express-heavy WFQ weights — the fixture that WOULD have painted them).
+- Covenant at pixels: the measured stroke never exceeds 0.5 × the live house footprint.
+- State up: a congested building's light reads the amber-shifted blend (present) and NOT the pure warm blend (absent).
+
+## Mutation proofs (RED-then-GREEN, all run)
+
+| # | Mutation | Fails |
+|---|---|---|
+| M1 | lane stripe reintroduction (express amber on the wire) | palcheck laneless zero-count at BOTH rungs (4645/652 px) |
+| M2 | link base ×3 (ratio-law break) | table pin (13.5≠4.5) + covenant band + pixel width (the clamp visibly engaged: the drawn stroke measured 22px ≈ the derived cap 31.2×scale-ratio region — the RED is the table mismatch, the clamp engagement is the visible mechanism) |
+| M3 | covenant clamp deletion | `covenant_clamp_engages_on_fat_bundles` + the sweep (Core/wide/4-member breaks) |
+| M4 | symbol swap (flat disc above ACCESS) | shrink-monotone (1331 > 0 > 0) + CORE dusk/state legs |
+| M5 | dusk dial off | all four dusk legs |
+| M6 | reduced-motion gate deleted from the feed | `reduced_motion_pins_the_breath` |
+| M7 | primitive block on Dublin | both Dublin sprite pins |
+| M8 | ring floor 2.0 → 1.0 | the floor pin (1.32 ≠ 2.0) |
+| M9 | house base 1.00 → 0.72 | three ladder pins |
+
+## Parked-fork fence statement
+
+NO work (not even preliminary) landed on: link finish 1b B/C variants (beyond the `LINK_FINISH` compile-time seam — B/C enum arms are comments; flipping the constant fails the compile), the router queue encoder, the tier-ring final spec beyond the 2px floor (`TIER_RING_FACTOR` stays 0.055), the quiet-board PRODUCTION swap (no board asset change; `dublin_board`'s golden shifts only from the node ladder), packet shapes/class colors (§6 — riders keep the existing lateral lattice, collapsed by the thinner stroke), HUD occlusion (§7), and the state-up-ladder encoder's final form (the shipped warm-amber node shift is the spec's minimal honest version).
+
+## Verification
+
+- 49/49 demos green (T1 + T2 + replay gate) after each re-bless; `harness run` 3×.
+- 468 unit tests: core 280, app 51, app/render 114, input 13, audio 18, harness 2.
+- palcheck all green (sections 1–7), drift-check 353/353 rejected, preview-check 7/7, motion-pixel PASS, stats byte-identity, input-parity 27/27, PP_DEBUG builds + smoke, font-guard, lint.
+- Zero CI-relevant flake: local ground truth (remote CI billing-block noted once, per briefing).
+
+## Decisions & rationale
+
+- **Covenant reference = the tier's endpoint class** (the mock's own reading): access-tier strokes measure against the house; the wide backbone against the DC host. The mock's gold backbone is 0.55 of a house BY RULING and comfortably in-law vs its routers/host endpoints. `link_width_capped` enforces the same endpoint-relative law at draw time (a wide pipe serving a house clamps to the house).
+- **CORE mid tier flattened to 3.5** (not the mock's point-measured steel 8px→4.0): "links stay the visible skeleton at MIN stroke weight" — only the backbone fattens at CORE. Also avoids a transient covenant edge pre-L4. No demo uses mid pipes; zero golden impact.
+- **DC = the Content_Host role** (the mock's "dc" position pastes the host sprite; the dc sprite stays unwired as shipped). The §4 "DC 1.35" anchor lands on `sprite_host_target`.
+- **Dusk dot radius rides the live footprint** (0.75/0.90), not absolute tiles: our blit trims to the content bbox (the mock's paste carried transparent padding), so any smaller under-dot is invisible — the read is the halo RINGING the silhouette, and it survives the L4 base changes automatically.
+- **Rider lattice unchanged in shape** (Fork 2 is open/parked): the lattice width derives from the clamped stroke, so riders compress toward the centerline on thin strokes — the natural fallout of the covenant, no packet-side work.
+- **`lane_detail` deleted, not kept dead**: the 7.1 focus-reveal canon is superseded by the laneless ruling; `zoom_rung` subsumes the tiering. The zoomed-lane palcheck leg became the laneless + covenant pixel gate.
+- **All demos capture at the fit (CORE)** — any zoom > 1.0 clips the 40-tile juice cluster. The sprite-presence canaries that degenerated at thumbnail scale re-pinned to measured counts (~50%) or tone bands (LED, campus brick), with the measured values in the comments. The strong exact-hex presence pins live where the sprites are big: the ACCESS-leg fresh renders (section 2) + the blessed corpus's own crop-canary geometry.
+- **The seed-7 fixture sits ON LAND** (the map is water+islands; the dusk-blend predictions composite over the land tint (239,228,186) — measured, documented in the constants).
+- **bmad-build renderer waived** (the standing 08-21/23 path: no `render_skill.py` in-repo); the briefing + LOOK-SPEC were the spec; step-04 ran as the two-hunter swarm.
+
+## Review
+
+step-04 review swarm (mandatory): bmad-review-adversarial-general + bmad-review-edge-case-hunter on glm-5.3 (thinking max), launched synchronously against the full code diff; findings triaged per the step-04 classify rules and folded in this PR:
+
+- **Folded (patch)** — adversarial r1: the covenant sweep + fat-bundle test were VACUOUS (the unit fixture never loaded sprite bboxes → every router endpoint's drawn size was 0 → cap 0 → the sweep passed crushed; the hunter probed cap=0.000, natural=10.5). Fix: real puck bboxes in the fixtures (the loader's documented defaults), the fat fixture moved to a 16-port router_high (needs ≥5 members to pass the REAL cap 13.0), the sweep's doc states its honest scope (it detects clamp deletion + derivation drift; the table pins catch fattening); the crisis OUTLINE still drew the UNCAPPED width (the halo/selection/riders were migrated, the outline missed) → `link_width_capped` threaded; the pixel width leg's tolerance tightened 2.0→1.0 (always-ACCESS rung-deafness passed at ±2 — deltas 1.29/0.92px) with the comment corrected; a leftover debug PNG export removed; stale canvas→land blend comment. Edge-case r1: `set_reduced_motion` cleared the pullback FLAG but left the breath's targets — camera_update's ease runs unconditionally, so the map kept gliding to the abandoned target at the FASTER normal rate (BLOCKER) → the targets freeze at the live values and the test asserts zero residual motion; the assist candidate halo kept the retired ×2.2 band factor (the commit frame popped ~2.2× the stroke) → glow margin only; the assist route glow + `wire_paths_compute`/fan stubs now ride the capped width (the flags-on path obeys the covenant where it bites); the NaN-zoom parse guard; the tie-glow rung companion; the cut pins use the named camera constants with coupling pins.
+- **Rejected with rationale** — "the covenant pixel leg cannot fail on a clamp regression": true by contract — the leg pins width==table; the clamp has its own dedicated unit test (`covenant_clamp_engages_on_fat_bundles`) whose M3 deletion the hunter verified RED.
+- **Deferred** — the primitive fallback path (documented unreachable) ignores the rung tables; and the pre-existing N11 auto-pullback toggle shares the latent ease-continues behavior (pre-dates this story; `set_reduced_motion` shows the fix shape) → both filed for a focused follow-up.
diff --git a/app/main.odin b/app/main.odin
index e811a35..09657af 100644
--- a/app/main.odin
+++ b/app/main.odin
@@ -1194,6 +1194,30 @@ effect_settings :: proc(user: rawptr, ictx: ^inp.Input) {
 // ±1 = step), reduced-motion toggle, ui-scale step (±1, clamped), audio
 // mute (toggle). Every change lands in the effective view + the settings
 // file. Presentation-only [ODN-1] — the sim never sees a byte of it.
+
+// set_reduced_motion — the MOTION row's body (the toggle + the view mirror +
+// the LOOK §2 breath pin: an in-flight auto-pullback ends with the toggle,
+// the N11 auto_pullback mirror — the player's own camera inputs are never
+// touched). Extracted so the pins drive the REAL semantics; the handler adds
+// only the settings persist.
+set_reduced_motion :: proc(app: ^App, on: bool) {
+	app.a11y.reduced_motion = on
+	app.view.reduced_motion = on
+	if on {
+		// The ease in camera_update runs UNCONDITIONALLY toward the targets
+		// (the flag only sets the rate) — clearing app.pullback alone would
+		// leave the map gliding to the abandoned breath target at the FASTER
+		// normal rate (the edge-case-hunter's BLOCKER). Freezing the targets
+		// at the live values stops the autonomous motion THIS FRAME; the
+		// player's next input re-targets normally, and the breath resumes
+		// only on the next seed (the §2 ruling).
+		app.pullback = false
+		app.cam_zoom_to = app.cam_zoom
+		app.cam_wx_to = app.cam_wx
+		app.cam_wy_to = app.cam_wy
+	}
+}
+
 effect_settings_adjust :: proc(user: rawptr, ictx: ^inp.Input, row: i32, delta: i32) {
 	app := cast(^App)user
 	switch row {
@@ -1205,8 +1229,7 @@ effect_settings_adjust :: proc(user: rawptr, ictx: ^inp.Input, row: i32, delta:
 		app.a11y.palette = rnd.Palette_Mode(cycle_palette(u8(app.a11y.palette), adjust_step(delta)))
 		rnd.palette_apply_mode(&app.palette_base, &app.palette, app.a11y.palette)
 	case rnd.SETTINGS_ROW_MOTION:
-		app.a11y.reduced_motion = !app.a11y.reduced_motion
-		app.view.reduced_motion = app.a11y.reduced_motion
+		set_reduced_motion(app, !app.a11y.reduced_motion)
 	case rnd.SETTINGS_ROW_SCALE:
 		// cycle with wrap (Perkins r1 B2 + r2 blocker 1): a delta-0 tap
 		// advances +1 (adjust_step) — 150% -> 100% on the next tap, and a
@@ -1834,8 +1857,8 @@ camera_focus_pair :: proc(app: ^App, lo, hi: u32) {
 
 // camera_update — the per-frame eased approach (a simple exponential ease; the
 // rasterized-path no-transcendentals rule is satisfied — no sin/cos). The view
-// scale/off derive from the animated camera; lane_detail flips at the 1.5x
-// threshold (the lanes reveal ON zoom-in — the user's camera model).
+// scale/off derive from the animated camera; the LOOK zoom ladder's rung
+// (zoom_rung_of) rides it (the stepped LOD tables key on the rung).
 // 2026-08-23 (DOCK-RIGHT): the horizontal center is the PLAYFIELD center
 // (play_w/2 — the NOC rail's left edge), so the world fits LEFT of the rail
 // while D is on; play_w == win_w when the overlay is off.
@@ -1866,7 +1889,9 @@ camera_update :: proc(app: ^App) {
 	v.scale = fit * app.cam_zoom
 	v.off_x = f32(v.play_w)/2 - app.cam_wx * v.scale
 	v.off_y = f32(v.win_h)/2 - app.cam_wy * v.scale
-	v.lane_detail = app.cam_zoom > 1.5
+	// LOOK §1: the toward-space ladder rung rides the eased camera (the
+	// stepped LOD tables key on it; zoom_rung_of is the single derivation).
+	v.zoom_rung = rnd.zoom_rung_of(app.cam_zoom)
 }
 
 // pullback_feed — the auto-pullback trigger (the mid-flight ruling): scan
@@ -1890,6 +1915,13 @@ pullback_feed :: proc(app: ^App, events: []pp.Event) {
 	if !app.a11y.auto_pullback {
 		return
 	}
+	// LOOK §2 (the 2026-08-26 camera ruling, 7.3/E9.2 doctrine): reduced
+	// motion PINS the breath — the map never moves on its own while the
+	// player asked for calm (the wheel keeps working; only the AUTOMATIC
+	// motion is gated).
+	if app.a11y.reduced_motion {
+		return
+	}
 	n_spawns: u32 = 0
 	for e in events {
 		if e.tag == pp.EVENT_TAG_NODE_SPAWNED {
diff --git a/app/pullback_test.odin b/app/pullback_test.odin
index 218e3bb..7b4eb6a 100644
--- a/app/pullback_test.odin
+++ b/app/pullback_test.odin
@@ -600,3 +600,64 @@ pullback_eases_no_snap_and_converges :: proc(t: ^testing.T) {
 	testing.expect(t, app.cam_zoom == app.cam_zoom_to, "the ease converges on the target")
 	testing.expect(t, !app.pullback, "the pullback clears on convergence")
 }
+
+// --- LOOK §2: reduced motion PINS the breath (the 2026-08-26 ruling) ------
+
+@(test)
+reduced_motion_pins_the_breath :: proc(t: ^testing.T) {
+	// the auto-breath is CAMERA MOTION: while reduced motion is on, a SEED
+	// spawn must not move the camera on its own (the wheel keeps working —
+	// only the AUTOMATIC motion is gated; the N11 toggle still works — the
+	// gates compose). Mutation: deleting the reduced_motion gate in
+	// pullback_feed arms the pullback and fails this pin.
+	app: App
+	pullback_test_app(&app)
+	defer pp.run_destroy(&app.state)
+	defer pp.catalogs_destroy(&app.cat)
+	app.a11y.reduced_motion = true
+	z_before := app.cam_zoom_to
+	cx_before := app.cam_wx_to
+	// a SEED at (23,10): >= 10 tiles from every live terminal (the fixture's
+	// estate sits at (10,10)/(13,10)) — the pullback's input slice
+	id := spawn_with_event(&app, {23, 10})
+	pullback_feed(&app, app.state.events[:])
+	testing.expect(t, app.cam_zoom_to == z_before, "reduced motion: a seed spawn does not breathe the camera")
+	testing.expect(t, app.cam_wx_to == cx_before, "reduced motion: the camera center holds")
+	testing.expect(t, !app.pullback, "reduced motion: no pullback armed")
+	_ = id
+}
+
+@(test)
+the_motion_toggle_ends_an_inflight_breath :: proc(t: ^testing.T) {
+	// flipping reduced motion ON ends an IN-FLIGHT pullback (the N11
+	// auto_pullback mirror); the view mirror rides the same proc; flipping
+	// OFF restores nothing (the feed re-arms on the NEXT seed — the breath
+	// resumes only on the next seed event, the §2 ruling).
+	app: App
+	pullback_test_app(&app)
+	defer pp.run_destroy(&app.state)
+	defer pp.catalogs_destroy(&app.cat)
+	// arm an in-flight pullback (the feed's own output shape)
+	app.pullback = true
+	app.cam_zoom_to = 2.0
+	testing.expect(t, app.view.reduced_motion == false, "SANITY: the fixture starts motion-on")
+	set_reduced_motion(&app, true)
+	testing.expect(t, !app.pullback, "the in-flight breath ends with the toggle")
+	// the TARGETS freeze at the live values: camera_update's ease runs
+	// unconditionally, so leaving the breath's targets would keep the map
+	// gliding to the abandoned seed target at the FASTER normal rate (the
+	// edge-case-hunter's BLOCKER — clearing the flag alone is not enough)
+	testing.expect(t, app.cam_zoom_to == app.cam_zoom, "the zoom target freezes at the live camera")
+	testing.expect(t, app.cam_wx_to == app.cam_wx && app.cam_wy_to == app.cam_wy, "the pan targets freeze at the live camera")
+	// and the residual motion is exactly zero one update later
+	rate_eased := app.cam_zoom
+	camera_update(&app)
+	testing.expect(t, app.cam_zoom == rate_eased, "zero residual camera motion after the freeze")
+	testing.expect(t, app.a11y.reduced_motion == true, "the settings struct is the single source")
+	testing.expect(t, app.view.reduced_motion == true, "the view mirror rides the toggle")
+	// OFF: the mirror clears; no pullback magically re-arms (it resumes on
+	// the next seed only)
+	set_reduced_motion(&app, false)
+	testing.expect(t, !app.pullback, "flipping OFF does not re-arm the breath")
+	testing.expect(t, app.view.reduced_motion == false, "the mirror clears with the toggle")
+}
diff --git a/app/render/assist.odin b/app/render/assist.odin
index 682ad5d..05e094f 100644
--- a/app/render/assist.odin
+++ b/app/render/assist.odin
@@ -422,7 +422,7 @@ draw_glow_edge :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, u, w:
 		}
 		a := node_screen(v, topo.node_pos[sa])
 		b := node_screen(v, topo.node_pos[sb])
-		halo := band_width(v, bundles.bundle_tier[bi], int(bundles.bundle_count[bi])) + 6.0 * v.scale // 7.1: the glow hugs the WIDE band (Perkins r2 W-A)
+		halo := link_width_capped(v, topo, bundles, bi) * v.scale + 6.0 * v.scale // LOOK §3: the glow hugs the covenant-capped stroke (Perkins r2 W-A)
 		// 7.5 shipped verdict: both flags off = the pre-7.5 inline glow; the
 		// routed/anchor variants follow the drawn path.
 		if !v.route_wires && !v.wire_anchors {
@@ -460,7 +460,11 @@ draw_glow_edge :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, u, w:
 	a := node_screen(v, topo.node_pos[sa])
 	b := node_screen(v, topo.node_pos[sb])
 	width := tier_pipe_width(v, cand_tier) * v.scale
-	halo := width * 2.2 + 6.0 * v.scale // 7.1: the candidate halo matches the band scale (Perkins r2 W-A)
+	// LOOK §3: band_width lost the x2.2 band factor with the laneless ladder
+	// — the halo keeps ONLY the glow margin so the commit frame does not pop
+	// (the edge-case-hunter's MAJOR: the restated x2.2 here ballooned the
+	// ghost to ~2.2x the committed stroke).
+	halo := width + 6.0 * v.scale
 	rl.DrawLineEx(a, b, halo, col)
 	rl.DrawCircleV(a, halo * 0.5, col)
 	rl.DrawCircleV(b, halo * 0.5, col)
diff --git a/app/render/camera.odin b/app/render/camera.odin
index f75d966..0ff3cab 100644
--- a/app/render/camera.odin
+++ b/app/render/camera.odin
@@ -256,6 +256,51 @@ camera_cluster_center :: proc(topo: ^pp.Topology, tile_px: f32) -> (f32, f32) {
 	return ax / f32(n), ay / f32(n)
 }
 
+// --- LOOK §1: the toward-space zoom ladder rungs (2026-08-26 user ruling) --
+//
+// The zoom-language ladder: ONE metaphor boot-to-thumbnail (ACCESS intimate
+// -> DISTRIBUTION mid -> CORE thumbnail). Nothing ever swaps for a symbol;
+// everything just gets smaller; links stay visible at every altitude; dusk
+// lights come on progressively as you pull away. The rung is a PURE function
+// of the effective camera zoom (v.scale / camera_fit == cam_zoom on the app
+// path) — stepped tables everywhere (§10.4: no transcendentals, no smooth
+// blends between rungs; the ladder is honest steps).
+//
+// Cut values: ACCESS holds the shipped resting band (DEFAULT_ZOOM 2.0 and
+// up — boot lands INTIMATE, §2), CORE is the fit neighborhood (the
+// thumbnail; CAM_ZOOM_MIN 1.0 sits inside it), DISTRIBUTION spans between.
+// The cuts are implementation-tunable constants (the spec rules the RUNGS,
+// not the cut points); pinned by the look-ladder tests.
+
+// ZOOM_RUNG_ACCESS_MIN — at/above this effective zoom the view is ACCESS.
+ZOOM_RUNG_ACCESS_MIN :: 1.6
+
+// ZOOM_RUNG_DIST_MIN — at/above this (but below ACCESS) it is DISTRIBUTION;
+// below it the view is CORE (the fit floor CAM_ZOOM_MIN = 1.0 is inside CORE).
+ZOOM_RUNG_DIST_MIN :: 1.25
+
+// Zoom_Rung — the toward-space ladder rung (LOOK §1). Order matters: the
+// width/size tables index [rung] with this enum (Access=0, Distribution=1,
+// Core=2).
+Zoom_Rung :: enum {
+	Access,
+	Distribution,
+	Core,
+}
+
+// zoom_rung_of — the rung for an effective zoom (pure, deterministic). One
+// derivation: camera_update (the app path) and the harness demo-zoom path
+// both call this — a restated copy would drift a rung cut.
+zoom_rung_of :: proc(zoom: f32) -> Zoom_Rung {
+	if zoom >= ZOOM_RUNG_ACCESS_MIN {
+		return .Access
+	}
+	if zoom >= ZOOM_RUNG_DIST_MIN {
+		return .Distribution
+	}
+	return .Core
+}
+
 // camera_clamp_center — keep the camera center inside the world rect at the
 // TARGET zoom (the zoomed-in view may never fly off into the paper void; the
 // visible half-extent is (win/2)/(fit*z) world px). When the viewport is
diff --git a/app/render/crisis.odin b/app/render/crisis.odin
index 291844d..b09ae1b 100644
--- a/app/render/crisis.odin
+++ b/app/render/crisis.odin
@@ -384,7 +384,10 @@ draw_crisis_outlines :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles,
 		if v.reduced_motion {
 			factor = 1.0
 		}
-		band := band_width(v, bundles.bundle_tier[b], int(bundles.bundle_count[b]))
+		// LOOK §3: the outline hugs the COVENANT-CAPPED stroke (the drawn
+		// ribbon), not the uncapped natural width — a clamped fat bundle's
+		// bottleneck highlight must not float past the pipe per side.
+		band := link_width_capped(v, topo, bundles, b) * v.scale
 		width := band + (4.0 + 5.0 * factor) * v.scale
 		// 7.5 shipped verdict: both flags off = the pre-7.5 inline outline
 		// (byte-for-byte — the blessed render); the routed/anchor variants
diff --git a/app/render/dublin.odin b/app/render/dublin.odin
index bd3ecbd..5e6533c 100644
--- a/app/render/dublin.odin
+++ b/app/render/dublin.odin
@@ -42,39 +42,15 @@ Dublin_Board_Render :: struct {
 	// street-only fallback — the harness gates on this)
 	underlay:    rl.Texture2D,
 	underlay_ok: bool,
-	// the street segment grid (node block orientation): flat segments +
-	// per-tile-cell index lists (cell = 1 tile)
-	segs:      [dynamic][4]f32,
-	seg_cells: [dynamic][dynamic]i32,
-	seg_w:     i32,
-	seg_h:     i32,
 }
-
-// DUBLIN_SEG_MAX_DIST — a node further than this from any street renders
-// an axis-aligned block + a one-shot log line (amendment #2: flag, never
-// silently float).
-DUBLIN_SEG_MAX_DIST :: 3.0
-
-// The node block footprint (world tiles — the approved mock's block size).
-// v2-camera-zoom-tiers (2026-08-23): the terminal blocks were rendering ~3x
-// SMALLER than the router pucks at the new 2.0x default — the user's "barely
-// see the buildings, the routers are big" directive. L 0.40 -> 0.55, W 0.22
-// -> 0.30 so the street-aligned blocks read clearly against the pucks (the
-// pucks are reigned in by the same change — sprite_puck_target). The blocks
-// stay street-aligned and sized against the street layout (a block at 0.55
-// long sits within a street lane with its neighbors; the mock's "buildings
-// ON streets" grammar — never a floating sprite).
-DUBLIN_NODE_BLOCK_L :: 0.55 // long axis (along the street)
-DUBLIN_NODE_BLOCK_W :: 0.30 // short axis
+// LOOK §4 retirement: the street-segment grid (segs/seg_cells +
+// DUBLIN_SEG_MAX_DIST + DUBLIN_NODE_BLOCK_L/W) served the node BLOCK
+// orientation — the block path retired with the sprites-only ruling
+// (draw_building renders the Blender sprites on BOTH maps now).
 
 // dublin_render_destroy — free the cache's buffers + the GPU texture
 // (called by view teardown / board change).
 dublin_render_destroy :: proc(d: ^Dublin_Board_Render) {
-	delete(d.segs)
-	for c in d.seg_cells {
-		delete(c)
-	}
-	delete(d.seg_cells)
 	if d.underlay_ok {
 		rl.UnloadTexture(d.underlay)
 	}
@@ -107,86 +83,6 @@ dublin_render_ensure :: proc(v: ^View) {
 	} else {
 		d.underlay_ok = false
 	}
-	dublin_seg_grid_build(d, d.board)
-}
-
-// dublin_seg_grid_build — the street segment grid: every arterial + local
-// polyline chopped into segments, bucketed by 1-tile cell (a segment lands
-// in every cell its bbox covers). Pure data prep — deterministic.
-dublin_seg_grid_build :: proc(d: ^Dublin_Board_Render, b: ^pp.Map_Board) {
-	d.seg_w = b.w_tiles + 1
-	d.seg_h = b.h_tiles + 1
-	d.seg_cells = make([dynamic][dynamic]i32, d.seg_w * d.seg_h)
-	seg_append :: proc(d: ^Dublin_Board_Render, polys: [][dynamic][2]f32) {
-		for poly in polys {
-			for i in 0..<len(poly) - 1 {
-				ax, ay := poly[i][0], poly[i][1]
-				bx, by := poly[i + 1][0], poly[i + 1][1]
-				if ax == bx && ay == by {
-					continue
-				}
-				idx := len(d.segs)
-				append(&d.segs, [4]f32{ax, ay, bx, by})
-				x0 := max(0, i32(min(ax, bx)))
-				x1 := min(d.seg_w - 1, i32(max(ax, bx)))
-				y0 := max(0, i32(min(ay, by)))
-				y1 := min(d.seg_h - 1, i32(max(ay, by)))
-				for cy in y0..=y1 {
-					for cx in x0..=x1 {
-						append(&d.seg_cells[cy * d.seg_w + cx], i32(idx))
-					}
-				}
-			}
-		}
-	}
-	seg_append(d, b.arterial[:])
-	seg_append(d, b.local[:])
-}
-
-// dublin_node_street — the nearest street segment to a node tile: returns
-// the segment's unit direction + the squared distance. found=false when no
-// segment is within DUBLIN_SEG_MAX_DIST (the axis-aligned fallback).
-// Pure f32 math (the §10.4 rule — no libm).
-dublin_node_street :: proc(v: ^View, tx, ty: f32) -> (dx, dy: f32, dist2: f32, found: bool) {
-	d := &v.dublin
-	cx := clamp(i32(tx), 0, d.seg_w - 1)
-	cy := clamp(i32(ty), 0, d.seg_h - 1)
-	best_d2 := f32(DUBLIN_SEG_MAX_DIST * DUBLIN_SEG_MAX_DIST)
-	bdx, bdy := f32(1.0), f32(0.0)
-	hit := false
-	for oy: i32 = -1; oy <= 1; oy += 1 {
-		for ox: i32 = -1; ox <= 1; ox += 1 {
-			gx := cx + ox
-			gy := cy + oy
-			if gx < 0 || gx >= d.seg_w || gy < 0 || gy >= d.seg_h {
-				continue
-			}
-			for si in d.seg_cells[gy * d.seg_w + gx] {
-				s := d.segs[si]
-				// the clamped projection foot (point-to-segment)
-				ex := s[2] - s[0]
-				ey := s[3] - s[1]
-				l2 := ex * ex + ey * ey
-				t := f32(0)
-				if l2 > 1e-12 {
-					t = clamp(((tx - s[0]) * ex + (ty - s[1]) * ey) / l2, 0, 1)
-				}
-				fx := s[0] + t * ex
-				fy := s[1] + t * ey
-				d2 := (tx - fx) * (tx - fx) + (ty - fy) * (ty - fy)
-				if d2 < best_d2 {
-					best_d2 = d2
-					l := math.sqrt(l2)
-					if l > 1e-9 {
-						bdx = ex / l
-						bdy = ey / l
-					}
-					hit = true
-				}
-			}
-		}
-	}
-	return bdx, bdy, best_d2, hit
 }
 
 // Dublin_Underlay_Ready — the harness capture gate: ensure the cache is
@@ -204,14 +100,6 @@ dublin_tile_screen :: proc(v: ^View, tx, ty: f32) -> rl.Vector2 {
 	return to_screen(v, tx * v.tile_px, ty * v.tile_px)
 }
 
-// dublin_screen_tile — the inverse (screen -> tile coords; the node block
-// path recovers the node's tile from its screen center — f32 rounding is
-// immaterial to the street lookup).
-dublin_screen_tile :: proc(v: ^View, sx, sy: f32) -> (f32, f32) {
-	s := v.tile_px * v.scale
-	return (sx - v.off_x) / s, (sy - v.off_y) / s
-}
-
 // dublin_map_draw — the board underlay (called from map_draw when the map
 // source = dublin; the procedural path is untouched). The approved look:
 // the Blender-baked base map, the ODbL attribution, and NOTHING else — no
@@ -329,48 +217,3 @@ dublin_draw_attribution :: proc(v: ^View, b: ^pp.Map_Board) {
 		draw_text_font_halo(v.font, b.attribution, x, y, size, v.palette.ink_faint, halo)
 	}
 }
-
-// dublin_node_block_draw — the terminal's street-aligned block (amendment
-// #2): a small building block centered on the node, ORIENTED along its
-// nearest street segment, family-washed, with the type chip riding the
-// top. `c` is the node's screen center; `reveal` scales the spawn reveal.
-// Returns the block's screen-space top y (the chip anchor).
-dublin_node_block_draw :: proc(v: ^View, c: rl.Vector2, fam: rl.Color, reveal_scale: f32, recede: f32 = 0.0) -> f32 {
-	tx, ty := dublin_screen_tile(v, c.x, c.y)
-	dx, dy, _d2, found := dublin_node_street(v, tx, ty)
-	if !found {
-		dx, dy = 1.0, 0.0 // axis-aligned fallback
-		// amendment #2: flag it — one log line, never silently float
-		fmt.printfln("[dublin] node at (%.1f, %.1f) has no street within %.0f tiles - axis-aligned block", tx, ty, DUBLIN_SEG_MAX_DIST)
-	}
-	// the block footprint (world tiles -> screen via the camera scale)
-	s := v.tile_px * v.scale * reveal_scale
-	hl := DUBLIN_NODE_BLOCK_L * s * 0.5
-	hw := DUBLIN_NODE_BLOCK_W * s * 0.5
-	// the corners: center ± dir*hl ± perp*hw (perp = (-dy, dx))
-	px, py := -dy, dx
-	q := [4]rl.Vector2{
-		{c.x - dx * hl + px * hw, c.y - dy * hl + py * hw},
-		{c.x + dx * hl + px * hw, c.y + dy * hl + py * hw},
-		{c.x + dx * hl - px * hw, c.y + dy * hl - py * hw},
-		{c.x - dx * hl - px * hw, c.y - dy * hl - py * hw},
-	}
-	// two CCW triangles (rlgl front face — the 08-23 field note). The
-	// recede rides the RGB MIX like the frontage edge below — the alpha
-	// twin alone was INERT under rlsw (triangles render opaque there, the
-	// Perkins r1 B1 probe: deleting it kept the corpus green; the GPU app
-	// would have blended it, a silent renderer divergence).
-	col := crisis_recede(v, recede, fam)
-	col.a = u8(f32(fam.a) * crisis_recede_scale(recede))
-	rl.DrawTriangle(q[2], q[1], q[0], col)
-	rl.DrawTriangle(q[0], q[3], q[2], col)
-	// the street-facing edge line (the block's frontage read). The recede
-	// rides the RGB mix (crisis_recede), NOT an alpha scale — line-alpha is
-	// inert under rlsw (the in-repo canon; a scale-only recede was a GPU-app
-	// no-op in the goldens — Perkins r1 N2).
-	edge := crisis_recede(v, recede, fam)
-	edge.a = 90
-	rl.DrawLineEx({q[0].x, q[0].y}, {q[1].x, q[1].y}, 1.5 * v.scale, edge)
-	// the block's top edge (screen-space) — the chip anchor
-	return min(min(q[0].y, q[1].y), min(q[2].y, q[3].y))
-}
diff --git a/app/render/look_l1_test.odin b/app/render/look_l1_test.odin
new file mode 100644
index 0000000..38f22b3
--- /dev/null
+++ b/app/render/look_l1_test.odin
@@ -0,0 +1,312 @@
+package render
+
+// look_l1_test.odin — LOOK §3 L1 durable pins (2026-08-26 user ruling): the
+// SCALE COVENANT (links never exceed ~1/2 of the smaller node they connect,
+// at EVERY rung) + the LANELESS single-stroke ladder (the ruled mock tables)
+// + the LINK_FINISH switch (fork 1b: A ships; B/C are parked behind the
+// compile-time seam). Math-only pins (the render-test convention); the
+// PIXEL truth (no lane-stripe colors on the wire, the ratio live-measured)
+// is palcheck's job — the mutation legs run there.
+//
+// Run: odin test app/render
+
+import "core:fmt"
+import "core:os"
+import "core:testing"
+import pp "../../core"
+
+// --- the rung derivation (zoom_rung_of) ---------------------------------------
+
+@(test)
+zoom_rung_cuts_are_pinned :: proc(t: ^testing.T) {
+	// the shipped band: boot/rest (DEFAULT_ZOOM) is ACCESS; the fit
+	// (CAM_ZOOM_MIN) is CORE; the mid band between the cuts. The named
+	// constants pin the COUPLING: a DEFAULT_ZOOM change below the access cut
+	// fails here (boot would silently leave the intimate rung), and a
+	// CAM_ZOOM_MIN above the distribution cut fails (the fit floor would
+	// leave the thumbnail).
+	testing.expect(t, zoom_rung_of(DEFAULT_ZOOM) == .Access, "the resting home is Access")
+	testing.expect(t, zoom_rung_of(CAM_ZOOM_MAX) == .Access, "max zoom is Access")
+	testing.expect(t, zoom_rung_of(ZOOM_RUNG_ACCESS_MIN) == .Access, "the access cut itself is Access")
+	testing.expect(t, zoom_rung_of(ZOOM_RUNG_ACCESS_MIN - 0.0001) == .Distribution, "just under the access cut is Distribution")
+	testing.expect(t, zoom_rung_of(ZOOM_RUNG_DIST_MIN) == .Distribution, "the distribution cut itself is Distribution")
+	testing.expect(t, zoom_rung_of(ZOOM_RUNG_DIST_MIN - 0.0001) == .Core, "just under the distribution cut is Core")
+	testing.expect(t, zoom_rung_of(CAM_ZOOM_MIN) == .Core, "the fit floor is Core")
+	// the coupling pins: the cuts sit BETWEEN the named camera anchors
+	testing.expect(t, CAM_ZOOM_MIN < ZOOM_RUNG_DIST_MIN && ZOOM_RUNG_DIST_MIN <= ZOOM_RUNG_ACCESS_MIN && ZOOM_RUNG_ACCESS_MIN <= DEFAULT_ZOOM, "the rung cuts bracket the fit..rest band coherently")
+}
+
+@(test)
+view_compute_defaults_the_rung_to_core :: proc(t: ^testing.T) {
+	// the fit view sits in CORE (the thumbnail altitude) — a fresh
+	// view_compute must never leave the rung stale at the zero value
+	// (.Access would silently render the intimate ladder at the fit).
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	look_l1_fill_catalogs(t, cat)
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	v.catalogs = cat
+	view_compute(&v, 1280, 720, &cat.balance)
+	look_l1_set_puck_bboxes(&v)
+	testing.expect(t, v.zoom_rung == .Core, "a freshly computed fit view is the Core rung")
+}
+
+// --- the laneless ladder tables (the ruled mock) -------------------------------
+
+@(test)
+laneless_width_ladder_is_the_ruled_mock_table :: proc(t: ^testing.T) {
+	// storyboard.py (the ruled ladder record), halved for the 26px design
+	// tile: ACCESS/DISTRIBUTION uniform (hue carries the tier); CORE fattens
+	// the wide backbone (the skeleton read). Any table edit fails HERE
+	// before it can shift a golden silently.
+	expect_f32(t, link_base_world(.Access, "standard"), 4.5)
+	expect_f32(t, link_base_world(.Access, "mid"), 4.5)
+	expect_f32(t, link_base_world(.Access, "wide"), 4.5)
+	expect_f32(t, link_base_world(.Distribution, "standard"), 3.5)
+	expect_f32(t, link_base_world(.Distribution, "mid"), 3.5)
+	expect_f32(t, link_base_world(.Distribution, "wide"), 3.5)
+	expect_f32(t, link_base_world(.Core, "standard"), 3.5)
+	expect_f32(t, link_base_world(.Core, "mid"), 3.5)
+	expect_f32(t, link_base_world(.Core, "wide"), 6.0)
+	// the defensive fallback (an unknown catalog id) takes the quiet base
+	expect_f32(t, link_base_world(.Access, "narrow"), 4.5)
+	expect_f32(t, link_base_world(.Core, "narrow"), 3.5)
+	// the pooled growth shrinks with the rung (a fat bundle must not dwarf
+	// the rung's nodes before the covenant clamp even engages)
+	extra := LINK_EXTRA_W // local copy — a constant cannot be indexed at test-runtime
+	expect_f32(t, extra[int(Zoom_Rung.Access)], 2.0)
+	expect_f32(t, extra[int(Zoom_Rung.Distribution)], 1.5)
+	expect_f32(t, extra[int(Zoom_Rung.Core)], 1.25)
+}
+
+@(test)
+link_finish_ships_a_solid :: proc(t: ^testing.T) {
+	// fork 1b (the link finish) is OPEN: A_SOLID ships behind the
+	// compile-time switch. The pin: the constant IS A (a future ruling
+	// flips ONE constant — and until B/C are implemented the flip fails the
+	// COMPILE, the byte-cheap-reversal doctrine's loud path).
+	testing.expect(t, LINK_FINISH == .A_SOLID, "the shipped link finish is A_SOLID (fork 1b pending)")
+}
+
+// --- the scale covenant --------------------------------------------------------
+
+@(test)
+covenant_holds_for_every_rung_and_tier :: proc(t: ^testing.T) {
+	// The law (LOOK §3): a link's width never exceeds LINK_RATIO_CAP of the
+	// smaller node it connects — at EVERY rung, for EVERY tier, including
+	// pooled bundles. This drives the REAL catalog + topology through the
+	// REAL derivation chain (link_width_capped over node_draw_size_world,
+	// with REAL puck bboxes — see look_l1_set_puck_bboxes). Honest scope:
+	// WITH the clamp present the cap absorbs any width fattening (the table
+	// pins above catch that), so this sweep detects CLAMP DELETION and
+	// derivation drift (node-size or endpoint wiring regressions) — the M3
+	// mutation proves that bite. The single-band test + the pixel leg close
+	// the law's other side.
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	look_l1_fill_catalogs(t, cat)
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	v.catalogs = cat
+	view_compute(&v, 1280, 720, &cat.balance)
+	look_l1_set_puck_bboxes(&v)
+
+	state: pp.Run_State
+	defer pp.run_destroy(&state)
+	pp.run_init(&state, 7, cat.hash, cat.balance.logic_hz)
+	res, _ := pp.node_type_index(cat, "residential")
+	host, _ := pp.node_type_index(cat, "content_host")
+	rtb, _ := pp.node_type_index(cat, "router_basic")
+	// two endpoint regimes: the tightest (a lone house on a basic router —
+	// the smallest legal pairing) and the wide tier's home (a host on a
+	// core-side router).
+	n0 := pp.topology_spawn_node(&state.topology, res, {4, 15}, cat)
+	n1 := pp.topology_spawn_node(&state.topology, rtb, {8, 15}, cat)
+	n2 := pp.topology_spawn_node(&state.topology, host, {4, 21}, cat)
+	n3 := pp.topology_spawn_node(&state.topology, rtb, {8, 21}, cat)
+	pairs := [2][2]u32{{n0, n1}, {n2, n3}}
+
+	for rung in Zoom_Rung {
+		v.zoom_rung = rung
+		for pair in pairs {
+			tier_names := [3]string{"standard", "mid", "wide"}
+			for tier_name in tier_names {
+				tier, _ := pp.pipe_tier_index(cat, tier_name)
+				for k in 1..=4 {
+					ids := make([dynamic]u32, 0, 4, context.temp_allocator)
+					for _ in 0..<k {
+						r, e := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = pair[0], b = pair[1], tier = u16(tier)}}, cat)
+						testing.expectf(t, e == .None, "PREMISE: draw %s x%d failed (err %v)", tier_name, k, e)
+						append(&ids, r.id)
+					}
+					pp.bundles_rebuild(&state.bundles, &state.topology, cat, state.era)
+					bi := look_l1_only_bundle(&state.bundles)
+					lo_slot, _ := pp.node_slot(&state.topology, state.bundles.bundle_lo[bi])
+					hi_slot, _ := pp.node_slot(&state.topology, state.bundles.bundle_hi[bi])
+					w := link_width_capped(&v, &state.topology, &state.bundles, bi)
+					cap_px := LINK_RATIO_CAP * min(node_draw_size_world(&v, &state.topology, lo_slot), node_draw_size_world(&v, &state.topology, hi_slot))
+					testing.expectf(t, w <= cap_px + 1e-4,
+						"COVENANT BREAK rung=%v tier=%s count=%d: width %.2f > cap %.2f", rung, tier_name, k, w, cap_px)
+					for id in ids {
+						pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Demolish_Pipe{pipe = id}}, cat)
+					}
+					delete(ids)
+				}
+			}
+		}
+	}
+}
+
+@(test)
+covenant_clamp_engages_on_fat_bundles :: proc(t: ^testing.T) {
+	// the clamp is not decorative: a fat enough pooled bundle MUST clamp to
+	// the smaller endpoint's cap (natural > cap -> capped == cap). Without
+	// this leg a deleted clamp (link_width_capped == link_width_world)
+	// passes only if no bundle ever fattens past the law — vacuous.
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	look_l1_fill_catalogs(t, cat)
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	v.catalogs = cat
+	view_compute(&v, 1280, 720, &cat.balance)
+	look_l1_set_puck_bboxes(&v)
+	v.zoom_rung = .Access
+
+	state: pp.Run_State
+	defer pp.run_destroy(&state)
+	pp.run_init(&state, 7, cat.hash, cat.balance.logic_hz)
+	res, _ := pp.node_type_index(cat, "residential")
+	rth, _ := pp.node_type_index(cat, "router_high")
+	wide, _ := pp.pipe_tier_index(cat, "wide")
+	n0 := pp.topology_spawn_node(&state.topology, res, {4, 15}, cat)
+	n1 := pp.topology_spawn_node(&state.topology, rth, {8, 15}, cat)
+	drawn := 0
+	for _ in 0..<12 { // fatten until the natural width passes the REAL cap (16 ports on the high router)
+		_, e := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = n0, b = n1, tier = u16(wide)}}, cat)
+		if e != .None {
+			break // ports full — the pool is as fat as this fixture allows
+		}
+		drawn += 1
+	}
+	testing.expectf(t, drawn >= 5, "PREMISE: need >= 5 members to pass the real cap (drew %d)", drawn)
+	pp.bundles_rebuild(&state.bundles, &state.topology, cat, state.era)
+	bi := look_l1_only_bundle(&state.bundles)
+	natural := link_width_world(&v, state.bundles.bundle_tier[bi], int(state.bundles.bundle_count[bi]))
+	lo_slot, _ := pp.node_slot(&state.topology, state.bundles.bundle_lo[bi])
+	hi_slot, _ := pp.node_slot(&state.topology, state.bundles.bundle_hi[bi])
+	cap_px := LINK_RATIO_CAP * min(node_draw_size_world(&v, &state.topology, lo_slot), node_draw_size_world(&v, &state.topology, hi_slot))
+	testing.expectf(t, natural > cap_px, "PREMISE: the fat bundle's natural width (%.2f) exceeds the cap (%.2f)", natural, cap_px)
+	capped := link_width_capped(&v, &state.topology, &state.bundles, bi)
+	testing.expectf(t, capped <= cap_px + 1e-4, "the clamp engages: %.2f <= %.2f", capped, cap_px)
+	testing.expectf(t, capped < natural, "the clamped width is strictly narrower than natural")
+}
+
+@(test)
+single_strokes_sit_in_the_covenant_band :: proc(t: ^testing.T) {
+	// the ~1/3-1/2 law's other side: the ruled tables put SINGLE strokes
+	// comfortably under the cap vs the rung's smallest node (the mock's
+	// measured quiet-stroke look) — a width regression that fattens the
+	// tables past the law fails here even before the fat-bundle clamp
+	// engages. Rides the LIVE sprite tables (the L2/L4 ladder changes keep
+	// it honest). Reference per tier class (the MOCK's endpoint reading, the
+	// same reading link_width_capped enforces at draw time): the access
+	// classes (standard/mid) serve houses — measured vs the house; the wide
+	// backbone connects routers/hosts (never houses — the mock's gold
+	// backbone is 0.55 of a house BY RULING and in-law vs its own
+	// endpoints) — measured vs the DC host.
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	look_l1_fill_catalogs(t, cat)
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	v.catalogs = cat
+	view_compute(&v, 1280, 720, &cat.balance)
+	look_l1_set_puck_bboxes(&v)
+	for rung in Zoom_Rung {
+		v.zoom_rung = rung
+		house := sprite_house_target(&v) / max(v.scale, 0.0001)
+		host := sprite_host_target(&v) / max(v.scale, 0.0001)
+		tier_names := [3]string{"standard", "mid", "wide"}
+		for tier_name in tier_names {
+			w := link_base_world(rung, tier_name)
+			ref := house
+			if tier_name == "wide" {
+				ref = host
+			}
+			testing.expectf(t, w <= LINK_RATIO_CAP*ref,
+				"single %s stroke at %v (%.2fpx) exceeds the covenant vs its endpoint class (%.2fpx)", tier_name, rung, w, ref)
+		}
+	}
+}
+
+// --- helpers -------------------------------------------------------------------
+
+// look_l1_set_puck_bboxes — hand-set the puck content widths (the sprite
+// sheet is not loaded in unit tests; WITHOUT these, sprite_puck_target
+// computes min(0/110, 1.30) = 0 and every ROUTER endpoint's drawn size —
+// and with it the covenant cap — silently zeroes: the sweep passed while
+// crushed to cap 0 (the adversarial r1 BLOCKER-class vacuity). The values
+// are the committed defaults the loader documents (110 base; the tier
+// ratios read through exactly as the real sheet).
+look_l1_set_puck_bboxes :: proc(v: ^View) {
+	v.sprites.bboxes[6][2] = 110 // puck_1 (basic) — the committed default
+	v.sprites.bboxes[7][2] = 126 // puck_2 (mid)
+	v.sprites.bboxes[8][2] = 143 // puck_3 (high)
+}
+
+// look_l1_fill_catalogs — the on-disk catalogs (the crisis-chain test's
+// self-contained load convention; the REAL tier table + node roster). Fills
+// the caller-owned struct; the source buffers free here (catalogs_load
+// copies everything it keeps — the tracking allocator stays quiet).
+look_l1_fill_catalogs :: proc(t: ^testing.T, cat: ^pp.Catalogs) {
+	read_cat :: proc(path: string) -> []u8 {
+		b, err := os.read_entire_file_from_path(path, context.allocator)
+		if err != nil {
+			fmt.eprintfln("look_l1_test: cannot read %s", path)
+		}
+		return b
+	}
+	src: pp.Catalog_Sources
+	src.node_types = read_cat("data/node_types.json")
+	src.pipe_tiers = read_cat("data/pipe_tiers.json")
+	src.balance = read_cat("data/balance.json")
+	src.packet_types = read_cat("data/packet_types.json")
+	src.demand = read_cat("data/demand.json")
+	src.eras = read_cat("data/eras.json")
+	src.crises = read_cat("data/crises.json")
+	if e := pp.catalogs_load(cat, &src); e.file != "" {
+		testing.expect(t, false, fmt.aprintf("catalog load failed: %s %s", e.file, e.rule))
+	}
+	delete(src.node_types)
+	delete(src.pipe_tiers)
+	delete(src.balance)
+	delete(src.packet_types)
+	delete(src.demand)
+	delete(src.eras)
+	delete(src.crises)
+}
+
+// look_l1_only_bundle — the bundle index of the fixture's single bundle
+// (the draw/demolish cycle leaves exactly one live bundle at a time).
+look_l1_only_bundle :: proc(bundles: ^pp.Bundles) -> u32 {
+	for bi in 0..<int(bundles.n) {
+		if bundles.bundle_count[bi] > 0 {
+			return u32(bi)
+		}
+	}
+	return 0
+}
+
+expect_f32 :: proc(t: ^testing.T, got, want: f32) {
+	testing.expectf(t, abs(got-want) < 1e-5, "f32 mismatch: got %v want %v", got, want)
+}
diff --git a/app/render/look_l2_test.odin b/app/render/look_l2_test.odin
new file mode 100644
index 0000000..92f60cb
--- /dev/null
+++ b/app/render/look_l2_test.odin
@@ -0,0 +1,122 @@
+package render
+
+// look_l2_test.odin — LOOK §1 L2 durable pins (2026-08-26 user ruling): the
+// toward-space LADDER — buildings/pucks shrink honestly per rung (nothing
+// swaps for a symbol), the dusk dial comes on with altitude (warm
+// settlement dots + the DC's cool anchor; intensity = the tunable alphas),
+// and state travels up (the minimal warm-amber shift on a congested
+// building's light). The PIXEL truth (dots present at DIST/CORE, absent at
+// ACCESS; the footprint shrink measured across rungs) lives in palcheck
+// section 2 — the mutation legs run there.
+//
+// Run: odin test app/render
+
+import "core:testing"
+import pp "../../core"
+
+@(test)
+rung_factor_tables_are_the_ruled_mock :: proc(t: ^testing.T) {
+	// storyboard.py (the ruled ladder): houses 1.00 -> 0.62 -> 0.42 tiles;
+	// the DC landmark holds more size (1.35 -> 1.05 -> 0.55 => factors
+	// 1.00/0.78/0.41 of its ACCESS base); puck bases 1.05 -> 0.80 -> 0.50.
+	// A table edit fails HERE before it can shift a golden silently.
+	expect_f32(t, BUILDING_RUNG_FACTOR[int(Zoom_Rung.Access)], 1.00)
+	expect_f32(t, BUILDING_RUNG_FACTOR[int(Zoom_Rung.Distribution)], 0.62)
+	expect_f32(t, BUILDING_RUNG_FACTOR[int(Zoom_Rung.Core)], 0.42)
+	expect_f32(t, HOST_RUNG_FACTOR[int(Zoom_Rung.Access)], 1.00)
+	expect_f32(t, HOST_RUNG_FACTOR[int(Zoom_Rung.Distribution)], 0.78)
+	expect_f32(t, HOST_RUNG_FACTOR[int(Zoom_Rung.Core)], 0.41)
+	expect_f32(t, PUCK_RUNG_BASE[int(Zoom_Rung.Access)], 1.05)
+	expect_f32(t, PUCK_RUNG_BASE[int(Zoom_Rung.Distribution)], 0.80)
+	expect_f32(t, PUCK_RUNG_BASE[int(Zoom_Rung.Core)], 0.50)
+}
+
+@(test)
+sprite_targets_shrink_honestly_per_rung :: proc(t: ^testing.T) {
+	// the REAL derivation chain: targets = base x rung factor, all four
+	// building classes + the puck (hand-set bboxes — the sprite sheet is
+	// not loaded in unit tests; the bbox ratio math is rung-invariant).
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	cat.balance.tile_px = 26
+	cat.balance.map_w_tiles = 40
+	cat.balance.map_h_tiles = 30
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	v.sprites.bboxes[6][2] = 110 // puck_1 content width (the committed default)
+	v.sprites.bboxes[7][2] = 126 // puck_2 (the tier ratio reads through)
+	v.sprites.bboxes[8][2] = 143 // puck_3 (<= PUCK_GROWTH_MAX x base)
+	view_compute(&v, 1280, 720, &cat.balance)
+	v.zoom_rung = .Access // view_compute defaults the fit view to CORE — pin the rung under test
+
+	fit := camera_fit(&v)
+	house_access := sprite_house_target(&v)
+	expect_f32(t, house_access, 1.00 * 26 * fit * 1.0) // the L4 ACCESS anchor
+	v.zoom_rung = .Distribution
+	house_dist := sprite_house_target(&v)
+	expect_f32(t, house_dist, 1.00 * 26 * fit * 0.62)
+	v.zoom_rung = .Core
+	house_core := sprite_house_target(&v)
+	expect_f32(t, house_core, 1.00 * 26 * fit * 0.42)
+	// the shrink is HONEST (strictly monotone down the ladder — nothing
+	// swaps, nothing stays)
+	testing.expect(t, house_access > house_dist && house_dist > house_core, "buildings shrink monotonically Access->Distribution->Core")
+	// the DC row shrinks SLOWER (the landmark holds more size)
+	v.zoom_rung = .Distribution
+	host_dist := sprite_host_target(&v)
+	testing.expectf(t, host_dist / (1.35 * 26 * fit) > BUILDING_RUNG_FACTOR[int(Zoom_Rung.Distribution)],
+		"the DC landmark holds more size at Distribution (%.2f > %.2f)", host_dist/(1.35*26*fit), BUILDING_RUNG_FACTOR[int(Zoom_Rung.Distribution)])
+	// the puck base rides the rung, the tier ratio reads through (puck_2's
+	// bbox ratio 126/110 survives every rung)
+	v.zoom_rung = .Access
+	puck1_access := sprite_puck_target(&v, 4)
+	expect_f32(t, puck1_access, 1.05 * 26 * fit)
+	v.zoom_rung = .Core
+	puck1_core := sprite_puck_target(&v, 4)
+	expect_f32(t, puck1_core, 0.50 * 26 * fit)
+	puck2_core := sprite_puck_target(&v, 8)
+	expect_f32(t, puck2_core / puck1_core, 126.0 / 110.0)
+}
+
+@(test)
+dusk_dial_tables_are_pinned :: proc(t: ^testing.T) {
+	// the ruling: DISTRIBUTION "lights coming on" (small, dim), CORE the
+	// full dusk glow; the intimate ACCESS diorama stays DARK (alpha 0).
+	// The DC reads cool against the warm field. Alphas are the INTENSITY
+	// dial — the values pin the shipped dial (a dial change is deliberate).
+	testing.expect(t, DUSK_ALPHA[int(Zoom_Rung.Access)] == 0, "ACCESS is dark (the intimate diorama)")
+	testing.expect(t, DUSK_ALPHA[int(Zoom_Rung.Distribution)] == 120, "DIST dots: small and dim (120)")
+	testing.expect(t, DUSK_ALPHA[int(Zoom_Rung.Core)] == 200, "CORE dots: the dusk glow (200)")
+	testing.expect(t, DUSK_DC_ALPHA[int(Zoom_Rung.Access)] == 0, "ACCESS: no DC glow")
+	testing.expect(t, DUSK_DC_ALPHA[int(Zoom_Rung.Distribution)] == 140, "DIST DC glow (140)")
+	testing.expect(t, DUSK_DC_ALPHA[int(Zoom_Rung.Core)] == 210, "CORE DC glow (210)")
+	expect_color(t, DUSK_WARM, {255, 214, 120, 255})
+	expect_color(t, DUSK_DC, {120, 190, 255, 255})
+	// the radii ride the building's footprint (the mock's halo proportion —
+	// the read survives every rung + the L4 base changes) and are ZERO at
+	// ACCESS (nothing draws)
+	testing.expect(t, DUSK_DOT_HOUSE_F[0] == 0 && DUSK_DC_HOST_F[0] == 0, "ACCESS radii are zero")
+	testing.expect(t, DUSK_DOT_HOUSE_F[1] < DUSK_DOT_HOUSE_F[2] && DUSK_DC_HOST_F[1] < DUSK_DC_HOST_F[2], "the halo grows toward CORE")
+	expect_f32(t, DUSK_DOT_HOUSE_F[int(Zoom_Rung.Core)], 0.90)
+	expect_f32(t, DUSK_DC_HOST_F[int(Zoom_Rung.Core)], 0.90)
+}
+
+@(test)
+dusk_state_shift_is_the_minimal_warm_amber_encoder :: proc(t: ^testing.T) {
+	// state travels up the ladder: a congested building's light shifts
+	// warm-amber (the minimal honest encoder — 50% toward the state token;
+	// critical toward red). Pure proc — both blends pinned byte-exact.
+	p := palette_load()
+	base := dusk_dot_color(&p, DUSK_WARM, .None)
+	expect_color(t, base, DUSK_WARM)
+	amber := dusk_dot_color(&p, DUSK_WARM, .Amber)
+	// 50/50 warm (255,214,120) toward state_congested (242,181,68)
+	expect_color(t, amber, {u8((255 + 242) / 2), u8((214 + 181) / 2), u8((120 + 68) / 2), 255})
+	crit := dusk_dot_color(&p, DUSK_WARM, .Red)
+	expect_color(t, crit, {u8((i32(255) + i32(p.state_critical.r)) / 2), u8((i32(214) + i32(p.state_critical.g)) / 2), u8((i32(120) + i32(p.state_critical.b)) / 2), 255})
+	// the DC's cool dot shifts through the SAME encoder (one definition)
+	dc_amber := dusk_dot_color(&p, DUSK_DC, .Amber)
+	expect_color(t, dc_amber, {u8((i32(120) + i32(242)) / 2), u8((i32(190) + i32(181)) / 2), u8((i32(255) + i32(68)) / 2), 255})
+}
diff --git a/app/render/look_l4_test.odin b/app/render/look_l4_test.odin
new file mode 100644
index 0000000..2db4656
--- /dev/null
+++ b/app/render/look_l4_test.odin
@@ -0,0 +1,112 @@
+package render
+
+// look_l4_test.odin — LOOK §4 L4 durable pins (2026-08-26 user ruling): the
+// RULED ACCESS node ladder (home 1.00 · biz 1.10 · campus 1.22 · DC 1.35 ·
+// puck 1.05), the mock cross-check (the rung factors reproduce the ruled
+// DIST/CORE numbers EXACTLY from these anchors), the Dublin wash held ~55%
+// lighter than the retired Dublin fill, and the ~2px screen-space tier-ring
+// floor (the D1 bump; token hues unchanged).
+//
+// Run: odin test app/render
+
+import "core:testing"
+import pp "../../core"
+
+@(test)
+access_node_ladder_is_the_ruled_ladder :: proc(t: ^testing.T) {
+	// the §4 ruled row, in tiles at ACCESS: home 1.00 · biz 1.10 · campus
+	// 1.22 · DC 1.35 (puck 1.05 — pinned by the puck base table). A base
+	// edit fails HERE before it can shift a golden silently.
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	cat.balance.tile_px = 26
+	cat.balance.map_w_tiles = 40
+	cat.balance.map_h_tiles = 30
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	view_compute(&v, 1280, 720, &cat.balance)
+	v.zoom_rung = .Access
+	fit := camera_fit(&v)
+	px := f32(cat.balance.tile_px) * fit
+	expect_f32(t, sprite_house_target(&v) / px, 1.00)
+	expect_f32(t, sprite_small_biz_target(&v) / px, 1.10)
+	expect_f32(t, sprite_campus_target(&v) / px, 1.22)
+	expect_f32(t, sprite_host_target(&v) / px, 1.35)
+	// the honest spectrum order survives (home < biz < campus < DC)
+	testing.expect(t, sprite_house_target(&v) < sprite_small_biz_target(&v) &&
+		sprite_small_biz_target(&v) < sprite_campus_target(&v) &&
+		sprite_campus_target(&v) < sprite_host_target(&v), "the role ORDER reads at a glance")
+}
+
+@(test)
+the_rung_factors_reproduce_the_ruled_mock :: proc(t: ^testing.T) {
+	// the mock cross-check (storyboard.py): DIST house 0.62 tiles, CORE
+	// house 0.42; the DC landmark 1.05 -> 0.55; the puck 1.05 -> 0.80 ->
+	// 0.50. The tables must reproduce the RULED numbers from the ruled
+	// ACCESS anchors — a factor or base drift breaks one of these equalities.
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	cat.balance.tile_px = 26
+	cat.balance.map_w_tiles = 40
+	cat.balance.map_h_tiles = 30
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	view_compute(&v, 1280, 720, &cat.balance)
+	px := f32(cat.balance.tile_px) * camera_fit(&v)
+	v.sprites.bboxes[6][2] = 110 // the puck_1 committed default content width
+	v.zoom_rung = .Distribution
+	expect_f32(t, sprite_house_target(&v) / px, 0.62)
+	// 1.35 x 0.78 = 1.053 — the mock's "1.05" at its 2-dp ruling precision
+	testing.expect(t, abs(sprite_host_target(&v)/px - 1.05) <= 0.01, "the DC landmark lands on the mock's 1.05 (2-dp)")
+	expect_f32(t, sprite_puck_target(&v, 4) / px, 0.80)
+	v.zoom_rung = .Core
+	expect_f32(t, sprite_house_target(&v) / px, 0.42)
+	// the mock's host numbers are ruled at 2-decimal precision: the 0.41
+	// factor reproduces 1.35 x 0.41 = 0.5535 (the mock's "0.55" rounding)
+	testing.expect(t, abs(sprite_host_target(&v)/px - 0.55) <= 0.01, "the DC landmark lands on the mock's 0.55 (2-dp)")
+	expect_f32(t, sprite_puck_target(&v, 4) / px, 0.50)
+}
+
+@(test)
+dublin_wash_is_lighter_than_the_retired_fill :: proc(t: ^testing.T) {
+	// the ruling: the family wash on Dublin sits ~55% LIGHTER than the
+	// retired solid block fill, so the sculpting reads. The scale is 0.45
+	// of the token alpha (the fill WAS the token at full strength).
+	expect_f32(t, DUBLIN_WASH_SCALE, 0.45)
+	p := palette_load()
+	// the computed wash alphas (f32->u8 truncation — the exact draw bytes:
+	// 204*0.45 = 91.7 -> 91; 184*0.45 = 82.8 -> 82)
+	expect_f32(t, f32(u8(f32(p.residential_family.a) * DUBLIN_WASH_SCALE)), 91)
+	expect_f32(t, f32(u8(f32(p.host_family.a) * DUBLIN_WASH_SCALE)), 82)
+}
+
+@(test)
+tier_ring_floor_is_two_screen_px :: proc(t: ^testing.T) {
+	// the D1 bump: the tier ring never thins below ~2px SCREEN-SPACE (the
+	// tier read survives at the thumbnail); above the floor it stays the
+	// shipped 0.055-tile factor (token hues unchanged — the colors are the
+	// router_tier_* tokens, untouched).
+	cat_storage: pp.Catalogs
+	cat := &cat_storage
+	defer pp.catalogs_destroy(cat)
+	cat.balance.tile_px = 26
+	cat.balance.map_w_tiles = 40
+	cat.balance.map_h_tiles = 30
+	v: View
+	pal := fallback_palette()
+	v.palette = &pal
+	view_compute(&v, 1280, 720, &cat.balance)
+	expect_f32(t, TIER_RING_FLOOR, 2.0)
+	// at the fit the factor gives 0.055 x 24 = 1.32px — the FLOOR governs
+	v.zoom_rung = .Core
+	expect_f32(t, tier_ring_thickness(&v), 2.0)
+	// zoomed in the factor clears the floor (2.0 x 24 x 0.055 = 2.64)
+	v.zoom_rung = .Access
+	v.scale = camera_fit(&v) * 2.6
+	testing.expect(t, tier_ring_thickness(&v) > TIER_RING_FLOOR, "the factor governs above the floor")
+	expect_f32(t, tier_ring_thickness(&v), 26.0 * camera_fit(&v) * 2.6 * TIER_RING_FACTOR)
+}
diff --git a/app/render/palette_polish_test.odin b/app/render/palette_polish_test.odin
index 6c0b390..5c08254 100644
--- a/app/render/palette_polish_test.odin
+++ b/app/render/palette_polish_test.odin
@@ -1,11 +1,10 @@
 package render
 
 // palette_polish_test.odin — the v2-look-polish durable pins (2026-08-21):
-// (a) the ribbon CASING color — the tier color darkened ~1/5 toward ink,
-// OPAQUE (alpha 255 — the rlsw line-primitive alpha trap: a translucent
-// casing would diverge between the GPU app and the goldens), and darker
-// than the band in every channel; (b) the SHIPPED canvas token — the
-// palette-load path (the embedded data/palette.json) must carry the
+// (a) [LOOK 2026-08-26] the ribbon CASING color pins were RETIRED with the
+// casing itself (finish A = one solid tier stroke; the laneless ladder
+// pins live in look_l1_test.odin + palcheck); (b) the SHIPPED canvas token —
+// the palette-load path (the embedded data/palette.json) must carry the
 // #EDE2C8 warm-paper lift, so a revert of the data token fails CI, not
 // playtesting. Pure data checks — no raylib draw calls (the render-test
 // convention: math only; the pixels are the harness's T2 surface).
@@ -19,38 +18,6 @@ import rl "vendor:raylib"
 
 import pp "../../core"
 
-@(test)
-casing_color_is_opaque_darker_and_deterministic :: proc(t: ^testing.T) {
-	p := palette_load()
-	bands := [3]rl.Color{p.pipe_copper, p.pipe_steel, p.pipe_fiber}
-	for band, i in bands {
-		c := casing_color(&p, band)
-		// OPAQUE — the rlsw divergence trap (line primitives render alpha
-		// as opaque; the casing must be a solid, never translucent).
-		testing.expect(t, c.a == 255, "casing must be opaque (alpha 255)")
-		// DARKER — the luminance invariant (rec.601 weights, pure integer
-		// math — no libm): blending toward ink NEUTRALIZES the tier color, so
-		// a channel can rise (copper's blue 46 < ink's blue 79); what must
-		// hold is the overall darker rim (the band reads brighter than its
-		// casing — the UE 'tube' read).
-		testing.expectf(t,
-			u32(c.r) * 299 + u32(c.g) * 587 + u32(c.b) * 114 <
-				u32(band.r) * 299 + u32(band.g) * 587 + u32(band.b) * 114,
-			"casing (%s) must be darker than the band (luminance)", fmt_tok(i))
-		// deterministic: two calls, identical bytes.
-		d := casing_color(&p, band)
-		testing.expect(t, c == d, "casing_color must be a pure function")
-	}
-	// the exact shipped blends (the PR's pixel-verify anchor): the blend is
-	// band*0.78 + ink*0.22, u8-truncated — the juice-golden rim pixels land
-	// on these exact values (the PR diff scan measured them ±0).
-	// v2-network-pop (2026-08-22): re-pinned to the vivid tier family —
-	// copper-orange {240,110,0} / cyan {0,150,240} / gold {255,215,0}.
-	expect_color(t, casing_color(&p, p.pipe_copper), {198, 100, 17, 255})
-	expect_color(t, casing_color(&p, p.pipe_steel), {11, 131, 204, 255})
-	expect_color(t, casing_color(&p, p.pipe_fiber), {210, 182, 17, 255})
-}
-
 @(test)
 shipped_canvas_token_is_the_warm_paper_lift :: proc(t: ^testing.T) {
 	p := palette_load() // the embedded data/palette.json — the shipped token
diff --git a/app/render/sprites.odin b/app/render/sprites.odin
index 6a24bea..b32232f 100644
--- a/app/render/sprites.odin
+++ b/app/render/sprites.odin
@@ -241,10 +241,38 @@ sprite_blit :: proc(sh: ^Sprite_Sheet, idx: int, c: rl.Vector2, target_w: f32, s
 // smaller in size compared to other big buildings" — house 0.90 -> 0.72 and
 // campus 1.40 -> 1.50, so house:campus moves 0.64 -> 0.48 (the MM read where
 // homes are tiny squares against the landmark blocks). Role ORDER preserved.
-sprite_house_target :: proc(v: ^View) -> f32 { return 0.72 * v.tile_px * v.scale }
-sprite_host_target :: proc(v: ^View) -> f32  { return 1.15 * v.tile_px * v.scale }
-sprite_small_biz_target :: proc(v: ^View) -> f32 { return 1.10 * v.tile_px * v.scale }
-sprite_campus_target :: proc(v: ^View) -> f32 { return 1.50 * v.tile_px * v.scale }
+// LOOK §4 (2026-08-26 user ruling): the ACCESS bases are the RULED ladder —
+// home 1.00 · biz 1.10 · campus 1.22 · DC 1.35 (the puck stays 1.05) —
+// superseding the scale-depth bases (the rung factors shrink honestly from
+// THESE anchors; the mock's DIST/CORE numbers reproduce exactly).
+//
+// LOOK §1 (2026-08-26 user ruling): the toward-space ladder — everything
+// just gets SMALLER with altitude, nothing swaps for a symbol. The ACCESS
+// bases below carry the §4 node ladder; the RUNG shrink rides the ruled
+// mock's factors (storyboard.py: houses 1.00 -> 0.62 -> 0.42 tiles; the DC
+// landmark holds more size 1.35 -> 1.05 -> 0.55; pucks 1.05 -> 0.80 -> 0.50
+// x the tier ratio). Stepped tables — no smooth blends (§10.4): the rung is
+// a discrete altitude, the factor applies whole.
+BUILDING_RUNG_FACTOR :: [3]f32{1.00, 0.62, 0.42} // [Access, Distribution, Core] — house/biz/campus
+HOST_RUNG_FACTOR :: [3]f32{1.00, 0.78, 0.41}     // the DC landmark row (holds more size)
+PUCK_RUNG_BASE :: [3]f32{1.05, 0.80, 0.50}       // the puck base (x the tier bbox ratio)
+
+sprite_house_target :: proc(v: ^View) -> f32 {
+	f := BUILDING_RUNG_FACTOR // local copy — a constant cannot be indexed by a runtime index
+	return 1.00 * v.tile_px * v.scale * f[int(v.zoom_rung)]
+}
+sprite_host_target :: proc(v: ^View) -> f32 {
+	f := HOST_RUNG_FACTOR // local copy — a constant cannot be indexed by a runtime index
+	return 1.35 * v.tile_px * v.scale * f[int(v.zoom_rung)]
+}
+sprite_small_biz_target :: proc(v: ^View) -> f32 {
+	f := BUILDING_RUNG_FACTOR // local copy — a constant cannot be indexed by a runtime index
+	return 1.10 * v.tile_px * v.scale * f[int(v.zoom_rung)]
+}
+sprite_campus_target :: proc(v: ^View) -> f32 {
+	f := BUILDING_RUNG_FACTOR // local copy — a constant cannot be indexed by a runtime index
+	return 1.22 * v.tile_px * v.scale * f[int(v.zoom_rung)]
+}
 // PUCK_GROWTH_MAX — the high-tier puck growth CAP (v2-camera-zoom-tiers,
 // 2026-08-23): the sprite's content-bbox ratio (bbox[idx]/base) clamps at
 // 1.30 so a high-tier puck stays just above a terminal block instead of ~3x
@@ -263,6 +291,8 @@ PUCK_GROWTH_MAX :: 1.30
 // CAPPED (PUCK_GROWTH_MAX) — the pucks stop dominating the terminal blocks
 // (the user's "routers are big — the scale is all messed up"). The tier
 // ladder still reads (mid/high stay above basic through the capped ratio).
+// LOOK §1: the base rides the rung (1.05 -> 0.80 -> 0.50 — the ruled mock;
+// "router pucks small but solid" at CORE), the tier ratio is rung-invariant.
 sprite_puck_target :: proc(v: ^View, port_capacity: i32) -> f32 {
 	sh := v.sprites
 	idx := sprite_index_puck(port_capacity)
@@ -271,5 +301,6 @@ sprite_puck_target :: proc(v: ^View, port_capacity: i32) -> f32 {
 		base = 110 // the committed default (defensive — bboxes parsed at load)
 	}
 	// preserve the canon tier scale: sizes relative to the basic puck's content.
-	return 1.05 * v.tile_px * v.scale * min(sh.bboxes[idx][2] / base, PUCK_GROWTH_MAX)
+	rung_base := PUCK_RUNG_BASE // local copy — a constant cannot be indexed by a runtime index
+	return rung_base[int(v.zoom_rung)] * v.tile_px * v.scale * min(sh.bboxes[idx][2] / base, PUCK_GROWTH_MAX)
 }
diff --git a/app/render/view.odin b/app/render/view.odin
index 7b2bfae..0d76aa5 100644
--- a/app/render/view.odin
+++ b/app/render/view.odin
@@ -60,10 +60,14 @@ View :: struct {
 	// Loaded at init by the app AND the harness; ok=false falls back to the
 	// pre-7.1 primitive draws (the font fallback precedent).
 	sprites: Sprite_Sheet,
-	// 7.1 camera canon (user, 2026-08-17): the focus-zoom reveals lane detail.
-	// lane_detail=false (the bird's-eye fit — what the harness captures) draws
-	// the lane stripes at hint alpha; true (zoomed in) draws them full.
-	lane_detail: bool,
+	// LOOK §1 (2026-08-26 user ruling): the toward-space zoom ladder rung —
+	// which altitude the world renders at (Access intimate / Distribution
+	// mid / Core thumbnail). A pure function of the effective camera zoom
+	// (zoom_rung_of) — set by camera_update (app) / the demo-zoom run setup
+	// (harness); view_compute defaults it to .Core (the fit). The lane-detail
+	// reveal it supersedes (the 7.1 focus-zoom lane stripes) was removed with
+	// the laneless ruling (LOOK §3 — the road doesn't gossip).
+	zoom_rung: Zoom_Rung,
 	// 7.5: wire aesthetics — the DRAWN wire path may route (detours) and/or
 	// shape junctions (puck-rim anchors + one-ribbon bundle fans). SHIPPED
 	// VERDICT (lavish gate 2026-08-19, verbatim): "Ship pure straight (routing
@@ -460,6 +464,11 @@ view_compute :: proc(v: ^View, win_w, win_h: i32, bal: ^pp.Balance) {
 	v.world_w = f32(bal.map_w_tiles) * v.tile_px
 	v.world_h = f32(bal.map_h_tiles) * v.tile_px
 	view_refit(v)
+	// LOOK §1: the fit view sits in the CORE rung (the thumbnail altitude) —
+	// the app's camera_update and the harness's demo-zoom directive re-derive
+	// it whenever the effective zoom moves. Defaulting here keeps a freshly
+	// computed View honest (a zero Value would read .Access).
+	v.zoom_rung = .Core
 	// 7.3: the UI-scale default — every View starts at ×1.00 (a zero-inited
 	// View would make hud() return 0). The app/harness override per settings.
 	if v.ui_scale <= 0 {
@@ -650,54 +659,156 @@ fceil :: proc(f: f32) -> i32 {
 	return t
 }
 
-// BUNDLE_EXTRA_WIDTH — how much wider a bundle grows per extra member pipe
-// (the "fatter pooled link" read). A single-member bundle adds 0, so a lone
-// pipe renders at exactly its tier width; each additional parallel pipe
-// fattens the pooled edge.
-BUNDLE_EXTRA_WIDTH :: f32(2.5)
-
-// CASING_OVERHANG — the ribbon casing's TOTAL extra width over the tier band
-// (screen px at scale 1: ~2.25px rim per side). The v2-look-polish ribbon
-// read: the UE slice-1 "casing border (wider, rounded) + fill" recipe
-// (look-parity checklist axis 2) — a slightly wider, darker under-stroke
-// with round caps so the tier band reads as an engineered ribbon against the
-// map instead of a chalk line. The congestion halo (+5*scale) and the
-// selection halo (+6*scale) both clear it, so warning overlays still read.
-CASING_OVERHANG :: 4.5
-
-// casing_color — the ribbon rim: the tier color darkened ~1/5 toward ink
-// (the rim must never fight the lane read — it is the band's OUTER edge
-// only). OPAQUE by construction: rlsw line primitives render alpha as
-// opaque (the 7.1 field-note divergence trap — the GPU app alpha-blends,
-// the goldens would not), so the casing is a solid color, never a
-// translucent one. Pure f32 blend, deterministic (the T2 spine).
-casing_color :: proc(p: ^Palette, col: rl.Color) -> rl.Color {
-	return rl.Color{
-		u8(f32(col.r) * 0.78 + f32(p.ink.r) * 0.22),
-		u8(f32(col.g) * 0.78 + f32(p.ink.g) * 0.22),
-		u8(f32(col.b) * 0.78 + f32(p.ink.b) * 0.22),
-		255,
+// --- LOOK §3: the scale covenant + the laneless link language (ruled) ----
+//
+// [ADOPTED 2026-08-26 user ruling] Links are SINGLE SOLID LANELESS strokes
+// (the 3.3 spatial-lane stripes are superseded — queues are ingress/egress
+// on ROUTERS, the road doesn't gossip), and ONE ratio law holds at every
+// tier: links never exceed ~1/3-1/2 of node size (the Mini Metro
+// observation; PP broke it at 56-67%+ — the root complaint). Tier identity
+// reads by HUE at a glance (copper/steel/gold — CVD-verified tokens,
+// unchanged); width is a quiet per-rung table from the ruled ladder mock
+// (storyboard.py, strips/ladder_final_ruled.png), halved for the 26px
+// design tile (the mock board renders 52px/tile):
+//
+//   rung         standard  mid     wide    (world px at scale 1 — the REAL
+//                                           catalog tier ids; the mock's
+//                                           access/backbone classes map
+//                                           onto the tier ladder)
+//   ACCESS         4.5      4.5     4.5    — the mock's uniform 9px stroke
+//   DISTRIBUTION   3.5      3.5     3.5    — everything smaller, lights on
+//   CORE           3.5      3.5     6.0    — the skeleton at MIN stroke
+//                                            weight; only the backbone
+//                                            fattens toward its router
+//                                            endpoints (gold 12px mock)
+//
+// Pooled bundles fatten by LINK_EXTRA_W per extra member (the pooled-
+// capacity read survives the laneless ruling) — and the COVENANT clamps
+// the final width at LINK_RATIO_CAP of the SMALLER ENDPOINT node's drawn
+// size (per bundle, at draw time: the law is about a road vs ITS
+// buildings, so a fat wide bundle serving a house clamps to that house).
+
+// LINK_RATIO_CAP — the covenant ceiling: a link's visible width may never
+// exceed this fraction of the smaller node it connects (the "~1/2" side of
+// the ~1/3-1/2 law, pinned hard; the tables sit well under it — the cap is
+// the law for degenerate fat bundles).
+LINK_RATIO_CAP :: f32(0.5)
+
+// LINK_EXTRA_W — the per-extra-member pooled growth (world px) per rung
+// (scales down with the stroke so a fat bundle never dwarfs the rung's
+// nodes before the covenant clamp even engages).
+LINK_EXTRA_W :: [3]f32{2.0, 1.5, 1.25} // [Access, Distribution, Core]
+
+// link_base_world — the single-stroke base width for (rung, tier id)
+// (world px; tier id keyed, catalog-order-immune). ACCESS/DISTRIBUTION are
+// uniform across tiers (hue carries the tier — the ruled mock); CORE
+// fattens the tiers up the ladder (the backbone skeleton read). The shipped
+// catalog carries standard/mid/wide; any other id takes the quiet base
+// class (the defensive fallback — the narrowest read, never a loud guess).
+link_base_world :: proc(rung: Zoom_Rung, tier_id: string) -> f32 {
+	switch tier_id {
+	case "wide": // the backbone class (gold — the fattest skeleton at CORE)
+		switch rung {
+		case .Access:       return 4.5
+		case .Distribution: return 3.5
+		case .Core:         return 6.0
+		}
+	case "mid": // the middle class
+		switch rung {
+		case .Access:       return 4.5
+		case .Distribution: return 3.5
+		case .Core:         return 3.5
+		}
+	case: // standard (the basic access tier) + the defensive fallback
+		switch rung {
+		case .Access:       return 4.5
+		case .Distribution: return 3.5
+		case .Core:         return 3.5
+		}
 	}
+	return 4.5 // unreachable: the case: arm above is total (belt-and-braces for the string switch)
 }
 
-// band_width — the 7.1 tier-band render width (the tier wire width + the
-// bundle member extra, scaled, then the x2.2 band factor). ONE definition —
-// the pipe bands, the packet riders, the selection halo, and the crisis
-// outline all derive from it (a restated copy drifts and miscenters riders).
-band_width :: proc(v: ^View, tier: u16, count: int) -> f32 {
-	return (tier_pipe_width(v, tier) + f32(max(0, count - 1)) * BUNDLE_EXTRA_WIDTH) * v.scale * 2.2
+// link_width_world — the UNCLAMPED pooled link width (world px): the base
+// stroke + the per-member growth. band_width (screen) and wire_path's
+// band_world derive from this ONE definition.
+link_width_world :: proc(v: ^View, tier: u16, count: int) -> f32 {
+	base: f32 = 4.5 // defensive: an unknown catalog tier id renders at the ACCESS base
+	if int(tier) < len(v.catalogs.pipe_tiers) {
+		base = link_base_world(v.zoom_rung, v.catalogs.pipe_tiers[tier].id)
+	}
+	extra := LINK_EXTRA_W // local copy — a constant cannot be indexed by a runtime index
+	return base + f32(max(0, count - 1)) * extra[int(v.zoom_rung)]
 }
 
-// lane_gutter — the canvas separator between lane stripes (7.1): wider when
-// the focus-zoom reveals the full lane read. ONE definition — draw_bundles
-// and the packet riders both use it (a divergent copy would miscenter riders).
-lane_gutter :: proc(v: ^View) -> f32 {
-	if v.lane_detail {
-		return 3.2
-	}
-	return 2.0
+// node_draw_size_world — a node's drawn footprint WIDTH in world px (the
+// sprite target / view scale — pure read of the live ladder tables, so the
+// covenant rides L2/L4's table changes automatically).
+node_draw_size_world :: proc(v: ^View, topo: ^pp.Topology, slot: u32) -> f32 {
+	if node_kind_of(topo, slot) == .Junction {
+		nt := node_type_of(topo, slot)
+		if int(nt) < len(v.catalogs.node_types) {
+			return sprite_puck_target(v, v.catalogs.node_types[nt].port_capacity) / max(v.scale, 0.0001)
+		}
+		return sprite_puck_target(v, 4) / max(v.scale, 0.0001)
+	}
+	t := sprite_house_target(v)
+	#partial switch node_role_of(topo, slot) {
+	case .Content_Host: t = sprite_host_target(v)
+	case .Small_Biz:    t = sprite_small_biz_target(v)
+	case .Campus:       t = sprite_campus_target(v)
+	}
+	return t / max(v.scale, 0.0001)
+}
+
+// link_width_capped — the covenant law: the bundle's drawn width (world
+// px), clamped at LINK_RATIO_CAP of the SMALLER endpoint node's drawn size.
+// Called by every consumer that knows the endpoints (draw_bundles, the
+// selection halo, the packet riders) so the visible stroke, its halo, and
+// the rider lattice all agree on ONE width per bundle.
+link_width_capped :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, bi: u32) -> f32 {
+	w := link_width_world(v, bundles.bundle_tier[bi], int(bundles.bundle_count[bi]))
+	sa, oka := pp.node_slot(topo, bundles.bundle_lo[bi])
+	sb, okb := pp.node_slot(topo, bundles.bundle_hi[bi])
+	if oka && okb {
+		cap_px := LINK_RATIO_CAP * min(node_draw_size_world(v, topo, sa), node_draw_size_world(v, topo, sb))
+		w = min(w, cap_px)
+	}
+	return w
+}
+
+// Link_Finish — fork 1b (the link FINISH, OPEN at spec time): A_SOLID
+// ships (Sally's rec, the ruled direction); B (asphalt band + dashed tier
+// marking) and C (asphalt + solid marking) land HERE when ruled — the
+// byte-cheap-reversal doctrine: a future ruling flips ONE constant, never a
+// rewrite. B/C are deliberately UNIMPLEMENTED (the parked-fork fence): the
+// draw's `when LINK_FINISH == .A_SOLID` chain has no other arm yet, so
+// flipping the constant fails the COMPILE (loud, immediate) until the
+// ruled finish is written.
+Link_Finish :: enum {
+	A_SOLID,
+	// B_ASPHALT_DASHED,   (fork 1b B — parked, not implemented)
+	// C_ASPHALT_SOLID,    (fork 1b C — parked, not implemented)
+}
+
+// LINK_FINISH — the shipped link finish (fork 1b ruling pending: A ships).
+LINK_FINISH :: Link_Finish.A_SOLID
+
+// band_width — the bundle's drawn width in SCREEN px (the tier base + the
+// member extra, scaled). ONE definition — the pipe strokes, the packet
+// riders, the selection halo, and the crisis outline all derive from it (a
+// restated copy drifts and miscenters riders). Endpoint-aware consumers
+// (draw_bundles / draw_selection / riders) pass through link_width_capped
+// instead — this is the endpoint-blind natural width.
+band_width :: proc(v: ^View, tier: u16, count: int) -> f32 {
+	return link_width_world(v, tier, count) * v.scale
 }
 
+// RIDER_GUTTER — the canvas margin the rider lattice keeps inside the
+// stroke (screen px; mirrors the old lane_gutter's fit value — the zoomed
+// 3.2 variant died with the lane stripes it separated).
+RIDER_GUTTER :: f32(2.0)
+
 // bundle_lane_caps_view — Σ member pipe lane_caps for a bundle slot (the
 // pooled link's lane allocation — the spatial-lane canon: stroke widths +
 // packet lateral offsets are proportional to these). Mirrors core's
@@ -849,9 +960,12 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 		if recede_bundle {
 			col = crisis_recede(v, desat, col)
 		}
-		caps := bundle_lane_caps_view(topo, bundles, flow, u32(bi))
-		band := band_width(v, tier, int(count))
-		// direction + perpendicular (the lateral axis the lanes stack along)
+		_ = flow // the lane caps died with the lane stripes (LOOK §3); riders read them per-pipe
+		// LOOK §3: the covenant width (world px -> screen) — clamped at the
+		// smaller endpoint's drawn size. ONE width for the stroke, its halo,
+		// and the riders (link_width_capped is the single derivation).
+		band := link_width_capped(v, topo, bundles, u32(bi)) * v.scale
+		// direction + perpendicular (the lateral axis the riders stack along)
 		dx, dy := b.x - a.x, b.y - a.y
 		len_ := rl.Vector2Length({dx, dy})
 		if len_ <= 0 {
@@ -865,50 +979,14 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 		// The routed/anchored variants engage only when a future aesthetic
 		// ruling flips a flag.
 		if !v.route_wires && !v.wire_anchors {
-			ux, uy := dx / len_, dy / len_
-			nx, ny := -uy, ux // unit normal (one consistent side)
-			// 8.x ribbon casing: the slightly wider, darker OPAQUE under-stroke
-			// with round caps (the UE slice-1 "casing border + fill" read). The
-			// tier band draws ON TOP of it, so the rim peeks ~2.25px per side.
-			casing := band + CASING_OVERHANG * v.scale
-			cc := casing_color(p, col)
-			rl.DrawLineEx(a, b, casing, cc)
-			rl.DrawCircleV(a, casing * 0.5, cc)
-			rl.DrawCircleV(b, casing * 0.5, cc)
-			// 7.1 pipe canon: the TIER COLOR owns a wide flat band; the three
-			// QoS lanes ride INSIDE it as saturated stripes separated by canvas
-			// gutters. Lane width = the WFQ share (3.3 canon).
-			rl.DrawLineEx(a, b, band, col)
-			rl.DrawCircleV(a, band * 0.5, col)
-			rl.DrawCircleV(b, band * 0.5, col)
-			gutter := lane_gutter(v)
-			inner := band - 2*gutter*v.scale
-			bands := lane_bands(caps, inner)
-			lane_cols := [3]rl.Color{p.lane_express, p.lane_standard, p.lane_best_effort}
-			if recede_bundle {
-				for i in 0..<3 {
-					lane_cols[i] = crisis_recede(v, desat, lane_cols[i])
-				}
-			}
-			if !v.lane_detail {
-				for i in 0..<3 {
-					lane_cols[i] = rl.Color{
-						u8(f32(col.r) * 0.72 + f32(lane_cols[i].r) * 0.28),
-						u8(f32(col.g) * 0.72 + f32(lane_cols[i].g) * 0.28),
-						u8(f32(col.b) * 0.72 + f32(lane_cols[i].b) * 0.28),
-						255,
-					}
-				}
-			}
-			for lane in 0..<3 {
-				if bands.widths[lane] <= 0 {
-					continue
-				}
-				pa := rl.Vector2{a.x + nx*bands.centers[lane]*inner, a.y + ny*bands.centers[lane]*inner}
-				pb := rl.Vector2{b.x + nx*bands.centers[lane]*inner, b.y + ny*bands.centers[lane]*inner}
-				rl.DrawLineEx(pa, pb, bands.widths[lane], lane_cols[lane])
-				rl.DrawCircleV(pa, bands.widths[lane] * 0.5, lane_cols[lane])
-				rl.DrawCircleV(pb, bands.widths[lane] * 0.5, lane_cols[lane])
+			// LOOK §3, finish A (LINK_FINISH == .A_SOLID): ONE solid
+			// tier-colored stroke, round-capped — no casing, no lane stripes
+			// (the laneless ruling; the finish seam compiles only this arm
+			// until fork 1b B/C are ruled + implemented).
+			when LINK_FINISH == .A_SOLID {
+				rl.DrawLineEx(a, b, band, col)
+				rl.DrawCircleV(a, band * 0.5, col)
+				rl.DrawCircleV(b, band * 0.5, col)
 			}
 			// 4.1 pipe-congestion halo (pre-7.5 inline)
 			lvl := bundle_congestion_level(topo, bundles, crisis, u32(bi))
@@ -953,37 +1031,11 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 		if path.n < 2 {
 			continue
 		}
-		// the casing mirrors the straight branch: the wider darker under-stroke
-		// first, the tier band on top (the 7.5 variant must render the same
-		// ribbon read when a future gate flips a flag).
-		cc := casing_color(p, col)
-		draw_path_band(v, &path, band + CASING_OVERHANG * v.scale, cc)
-		draw_path_band(v, &path, band, col)
-		gutter := lane_gutter(v)
-		inner := band - 2*gutter*v.scale
-		bands := lane_bands(caps, inner)
-		lane_cols := [3]rl.Color{p.lane_express, p.lane_standard, p.lane_best_effort}
-		if recede_bundle {
-			for i in 0..<3 {
-				lane_cols[i] = crisis_recede(v, desat, lane_cols[i])
-			}
-		}
-		if !v.lane_detail {
-			for i in 0..<3 {
-				lane_cols[i] = rl.Color{
-					u8(f32(col.r) * 0.72 + f32(lane_cols[i].r) * 0.28),
-					u8(f32(col.g) * 0.72 + f32(lane_cols[i].g) * 0.28),
-					u8(f32(col.b) * 0.72 + f32(lane_cols[i].b) * 0.28),
-					255,
-				}
-			}
-		}
-		for lane in 0..<3 {
-			if bands.widths[lane] <= 0 {
-				continue
-			}
-			lateral := bands.centers[lane] * inner / max(v.scale, 0.0001)
-			draw_path_offset_band(v, &path, lateral, bands.widths[lane], lane_cols[lane])
+		// LOOK §3, finish A: the path variant renders the SAME laneless
+		// single stroke (the future finish must keep both branches one look
+		// when a gate flips a wire flag).
+		when LINK_FINISH == .A_SOLID {
+			draw_path_band(v, &path, band, col)
 		}
 
 		// junction shaping: a count>1 bundle draws the FAN — thin stubs from
@@ -992,11 +1044,11 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 		if (v.route_wires || v.wire_anchors) && count > 1 {
 			a_world := node_world(topo, sa, v.tile_px)
 			b_world := node_world(topo, sb, v.tile_px)
-			band_w := band_world(v, tier, int(count))
+			band_w := band // the covenant-capped width (LOOK §3 — the fan matches the drawn ribbon)
 			apex_a, anchors_a := end_apex(v, topo, bundles, u32(bi), 0, b_world, band_w)
 			apex_b, anchors_b := end_apex(v, topo, bundles, u32(bi), 1, a_world, band_w)
 			for anc in anchors_a {
-				stub_w := band_world(v, anc.tier, 1) * 0.6 // the member's own narrow read
+				stub_w := min(band_world(v, anc.tier, 1), band) * 0.6 // the member's own narrow read, covenant-capped
 				stub_col := tier_pipe_color(v, anc.tier)
 				if recede_bundle {
 					stub_col = crisis_recede(v, desat, stub_col)
@@ -1004,7 +1056,7 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 				draw_fan_stub(v, anc.pos, apex_a, stub_w, stub_col)
 			}
 			for anc in anchors_b {
-				stub_w := band_world(v, anc.tier, 1) * 0.6
+				stub_w := min(band_world(v, anc.tier, 1), band) * 0.6
 				stub_col := tier_pipe_color(v, anc.tier)
 				if recede_bundle {
 					stub_col = crisis_recede(v, desat, stub_col)
@@ -1141,6 +1193,91 @@ draw_health_ring :: proc(v: ^View, lvl: pp.Congestion_Level, node_id: u32, c: rl
 	draw_text_c(v, glyph, x, y, fs, col)
 }
 
+// --- LOOK §1: the dusk dial (city-lights-from-orbit) ------------------------
+// [ADOPTED 2026-08-26 user ruling] "2 — pure shrink, LIGHTS COMING ON" at
+// DISTRIBUTION; "2 — shrink + dusk glow" at CORE: a small warm light under
+// each settlement (the toward-space metaphor — dusk falls as you pull
+// away). The dial, not a switch: the alphas below are the tunable intensity
+// (the ruling keeps glow intensity an implementation dial). The intimate
+// ACCESS diorama stays dark (alpha 0 — nothing glows at boot). The DC reads
+// COOL blue against the warm settlement field (the mock's cool-blue anchor).
+// State travels up the ladder (§1): a congested building's light shifts
+// warm-amber (the minimal honest encoder — the node's own health level
+// blends the dot toward the state token; the full estate encoder stays a
+// PARKED fork). Static dots (§8 quiet-at-rest — no animation to pin;
+// reduced-motion is inherently satisfied).
+DUSK_WARM :: rl.Color{255, 214, 120, 255}
+DUSK_DC :: rl.Color{120, 190, 255, 255}
+DUSK_ALPHA :: [3]u8{0, 120, 200} // warm settlement dots per rung
+DUSK_DC_ALPHA :: [3]u8{0, 140, 210} // the DC's cool dot per rung
+// the dot radius as a fraction of the building's CURRENT drawn footprint.
+// The read is the HALO AROUND the silhouette (our blit trims to the content
+// bbox — the mock's under-dot proportion only peeked because its paste
+// carried transparent padding): the radius exceeds half the footprint so
+// the dot rings the building at every altitude. Footprint-relative keeps
+// the read across rungs AND rides the L4 base changes automatically;
+// ACCESS is 0 — nothing draws.
+DUSK_DOT_HOUSE_F :: [3]f32{0, 0.75, 0.90} // warm halo vs the house footprint
+DUSK_DC_HOST_F :: [3]f32{0, 0.75, 0.90} // the DC's cool halo vs the host footprint
+DUSK_STATE_MIX :: f32(0.5) // the warm-amber shift strength (congested -> state token)
+
+// dusk_dot_color — the dot's ink for a node this healthy: the base dial
+// color, blended toward the state token by DUSK_STATE_MIX when the node is
+// congested/critical (the minimal state-up encoder). Pure — pinned.
+dusk_dot_color :: proc(p: ^Palette, base: rl.Color, lvl: pp.Congestion_Level) -> rl.Color {
+	if lvl == .None {
+		return base
+	}
+	token := p.state_congested
+	if lvl == .Red {
+		token = p.state_critical
+	}
+	return rl.Color{
+		u8(f32(base.r) * (1 - DUSK_STATE_MIX) + f32(token.r) * DUSK_STATE_MIX),
+		u8(f32(base.g) * (1 - DUSK_STATE_MIX) + f32(token.g) * DUSK_STATE_MIX),
+		u8(f32(base.b) * (1 - DUSK_STATE_MIX) + f32(token.b) * DUSK_STATE_MIX),
+		255,
+	}
+}
+
+// draw_dusk_dot — the under-sprite light (a FILL — rlsw-safe; the 7.1
+// field note: line alpha is inert in the software renderer, fills blend).
+// Drawn BEFORE the sprite so the glow peeks around the silhouette (the
+// mock's recipe: the dot under the shrunken building reads as the glow
+// halo). Alpha 0 (ACCESS) draws nothing. The dot rides the spawn reveal's
+// fade + the crisis recede like every other node accent.
+draw_dusk_dot :: proc(v: ^View, c: rl.Vector2, role: pp.Terminal_Role, lvl: pp.Congestion_Level, reveal_fade: f32, recede: f32) {
+	rung := int(v.zoom_rung)
+	is_dc := role == .Content_Host
+	alphas := DUSK_ALPHA
+	radii := DUSK_DOT_HOUSE_F
+	base := DUSK_WARM
+	if is_dc {
+		alphas = DUSK_DC_ALPHA
+		radii = DUSK_DC_HOST_F
+		base = DUSK_DC
+	}
+	a := f32(alphas[rung])
+	if a <= 0 {
+		return
+	}
+	a *= clamp01(reveal_fade) * crisis_recede_scale(recede)
+	if a <= 0 {
+		return
+	}
+	col := dusk_dot_color(v.palette, base, lvl)
+	col.a = u8(a)
+	foot := sprite_house_target(v)
+	if is_dc {
+		foot = sprite_host_target(v)
+	}
+	r := radii[rung] * foot
+	if r <= 0 {
+		return
+	}
+	rl.DrawCircleV(c, r, col)
+}
+
 // draw_building — the terminal sprite draw (7.1 pipeline). Role -> sprite
 // index + footprint (5.11: the class analogues — see sprite_index_building).
 // The fallback below is the pre-7.1 primitive path (belt-and-braces when the
@@ -1162,17 +1299,15 @@ draw_health_ring :: proc(v: ^View, lvl: pp.Congestion_Level, node_id: u32, c: rl
 draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2, health: pp.Congestion_Level, reveal_scale: f32 = 1.0, reveal_fade: f32 = 1.0, recede: f32 = 0.0) {
 	fam := terminal_family(v, role)
 	chip_visible := health == .None
-	// v2-dublin-map-beautify (amendment #2): on the Dublin board the
-	// terminal renders as a STREET-ALIGNED BLOCK (the approved mock's
-	// grammar — buildings ON streets, no floating sprites); the type chip
-	// rides the block. The sprite path stays for the procedural map.
-	if v.map_source == u8(pp.Map_Source.Dublin) && v.board != nil {
-		top_y := dublin_node_block_draw(v, c, fam, reveal_scale, recede)
-		if chip_visible {
-			draw_type_chip(v, role, c, top_y, fam, reveal_scale, reveal_fade, recede)
-		}
-		return
-	}
+	// LOOK §1: the dusk dot UNDER the form (every altitude above ACCESS;
+	// every building path — sprite, Dublin block, primitive fallback — the
+	// light is the settlement's, not the sprite's).
+	draw_dusk_dot(v, c, role, health, reveal_fade, recede)
+	// LOOK §4 (2026-08-26 user ruling): REAL Blender sprites ONLY — no
+	// primitive blocks, on BOTH maps. The Dublin street-aligned block path
+	// retires: the sculpted sprite reads on the board with its family wash
+	// held ~55% LIGHTER than the retired Dublin fill (DUBLIN_WASH_SCALE —
+	// the sculpting must read through the recolor).
 	if v.sprites.ok {
 		idx := sprite_index_building(id, role)
 		target := sprite_house_target(v) * reveal_scale
@@ -1184,7 +1319,11 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 		dst, ok := sprite_blit_dst(&v.sprites, idx, c, target)
 		sprite_blit(&v.sprites, idx, c, target, shadow_for_role(role), {255, 255, 255, u8(255 * clamp01(reveal_fade))})
 		if ok {
-			draw_family_wash(v, dst, fam, reveal_fade, recede)
+			wash := fam
+			if v.map_source == u8(pp.Map_Source.Dublin) && v.board != nil {
+				wash.a = u8(f32(fam.a) * DUBLIN_WASH_SCALE)
+			}
+			draw_family_wash(v, dst, wash, reveal_fade, recede)
 			if chip_visible {
 				draw_type_chip(v, role, c, dst.y, fam, reveal_scale, reveal_fade, recede)
 			}
@@ -1297,6 +1436,13 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 	}
 }
 
+// DUBLIN_WASH_SCALE — the LOOK §4 family-wash strength on the Dublin board:
+// ~55% LIGHTER than the retired Dublin block fill (the solid family color
+// the street-aligned blocks painted), so the Blender sculpting reads
+// through the recolor. The procedural map keeps the full token wash (the
+// shipped node-clarity look — the fill comparison is Dublin's own).
+DUBLIN_WASH_SCALE :: f32(0.45)
+
 // terminal_family — the role's hue-family token (Q2a). The token's ALPHA byte
 // is the wash strength (draw_family_wash uses it as-is): residential → warm
 // terracotta, small_biz → cool stone, campus → brick, content_host → deep
@@ -1748,6 +1894,21 @@ router_tier_family :: proc(v: ^View, port_capacity: i32) -> rl.Color {
 	return p.router_tier_basic
 }
 
+// TIER_RING_FLOOR — the LOOK §4 minimum SCREEN-SPACE stroke (the mock's D1
+// bump): the ring never thins below ~2px on the screen, whatever the
+// altitude (the tier read survives at the thumbnail; token hues unchanged).
+TIER_RING_FLOOR :: f32(2.0)
+
+// TIER_RING_FACTOR — the scale-proportional component above the floor
+// (the shipped 0.055 tile factor; the ring fattens as the camera closes in).
+TIER_RING_FACTOR :: f32(0.055)
+
+// tier_ring_thickness — the ONE derivation (draw_tier_ring is the only
+// consumer; the floor pin lives in look_l4_test).
+tier_ring_thickness :: proc(v: ^View) -> f32 {
+	return max(TIER_RING_FLOOR, v.tile_px * v.scale * TIER_RING_FACTOR)
+}
+
 // draw_tier_ring — the thin tier-colored ring just outside the puck (the
 // Q2b bird's-eye tier marker). Concentric circle lines fake the stroke
 // (DrawCircleLinesV has no thickness — the health-ring pattern); full-alpha
@@ -1757,7 +1918,7 @@ draw_tier_ring :: proc(v: ^View, c: rl.Vector2, dst: rl.Rectangle, tier: rl.Colo
 	ring := crisis_recede(v, recede, tier)
 	ring.a = 255
 	r := min(dst.width, dst.height) * 0.5 * 1.10
-	th := max(1.0, v.tile_px * v.scale * 0.055)
+	th := tier_ring_thickness(v)
 	for k in 0..<i32(th) {
 		rl.DrawCircleLinesV(c, r - f32(k), ring)
 	}
@@ -1884,9 +2045,7 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 				// would drift off a bent ribbon).
 				bnd := bundles.pipe_bundle[ps]
 				caps := bundle_lane_caps_view(topo, bundles, flow, bnd)
-				tier := bundles.bundle_tier[bnd]
-				count := bundles.bundle_count[bnd]
-				width := band_width(v, tier, int(count)) - 2.0 * lane_gutter(v) * v.scale
+				width := link_width_capped(v, topo, bundles, bnd) * v.scale - 2.0 * RIDER_GUTTER * v.scale
 				bands := lane_bands(caps, width)
 				if int(lane) < 3 && bands.widths[lane] > 0 {
 					// lateral offset in the path's tangent frame
@@ -1919,11 +2078,11 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 				hi_id := bundles.bundle_hi[bnd]
 				los, lok := pp.node_slot(topo, lo_id)
 				his, hok := pp.node_slot(topo, hi_id)
-				tier := bundles.bundle_tier[bnd]
-				count := bundles.bundle_count[bnd]
-				// 7.1: riders sit in the WIDENED band's lane markings (the band
-				// minus the two canvas gutters — mirrors draw_bundles exactly).
-				width := band_width(v, tier, int(count)) - 2.0 * lane_gutter(v) * v.scale
+				// LOOK §3: riders sit in the covenant-capped stroke's lattice
+				// (the width minus the two rider gutters — mirrors
+				// draw_bundles exactly; the lattice itself is the parked
+				// rider-layout fork, unchanged by the laneless ruling).
+				width := link_width_capped(v, topo, bundles, bnd) * v.scale - 2.0 * RIDER_GUTTER * v.scale
 				if lok && hok && width > 0 {
 					bx := node_screen(v, topo.node_pos[his]).x - node_screen(v, topo.node_pos[los]).x
 					by := node_screen(v, topo.node_pos[his]).y - node_screen(v, topo.node_pos[los]).y
@@ -2110,7 +2269,7 @@ draw_selection :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, sel:
 	if !oka || !okb { return }
 	a := node_screen(v, topo.node_pos[sa])
 	b := node_screen(v, topo.node_pos[sb])
-	halo := band_width(v, bundles.bundle_tier[bi], int(bundles.bundle_count[bi])) + 6 * v.scale // 7.1: the selection halo hugs the WIDE band
+	halo := link_width_capped(v, topo, bundles, bi) * v.scale + 6 * v.scale // LOOK §3: the selection halo hugs the covenant-capped stroke
 	// 7.5 shipped verdict: both flags off = the pre-7.5 inline halo (byte-for-
 	// byte); the routed/anchor variants follow the drawn path.
 	if !v.route_wires && !v.wire_anchors {
@@ -2142,16 +2301,14 @@ tier_pipe_color :: proc(v: ^View, tier: u16) -> rl.Color {
 }
 
 tier_pipe_width :: proc(v: ^View, tier: u16) -> f32 {
-	// v2-scale-depth: standard 5.5 → 7.4 (band 11.2 → 15.0px at fit). The
-	// ladder keeps its 1:1.57:2.43 ratio but caps WIDE below the house
-	// footprint (band 21.3px < house 21.6px — a pipe must never dwarf the
-	// node it serves; the r1 review finding).
-	switch v.catalogs.pipe_tiers[tier].id {
-	case "narrow": return 4.5
-	case "standard": return 7.4
-	case "wide": return 10.5
-	}
-	return 6.0
+	// LOOK §3: the laneless ladder's base stroke for this tier at the view's
+	// zoom rung (world px — no band factor; hue carries the tier). Kept as
+	// the endpoint-blind accessor for the drag ghost (assist — its halo adds
+	// the glow margin); the bundle draws go through link_width_capped.
+	if int(tier) < len(v.catalogs.pipe_tiers) {
+		return link_base_world(v.zoom_rung, v.catalogs.pipe_tiers[tier].id)
+	}
+	return link_base_world(v.zoom_rung, "standard")
 }
 
 // unit circle, 16 points (k * 22.5 deg), correctly-rounded decimal constants —
diff --git a/app/render/wire_path.odin b/app/render/wire_path.odin
index 13e5a5c..632e331 100644
--- a/app/render/wire_path.odin
+++ b/app/render/wire_path.odin
@@ -604,7 +604,9 @@ insert_bend :: proc(path: ^Wire_Path, o: Obstacle) -> bool {
 wire_paths_compute :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles) -> [dynamic]Wire_Path {
 	paths := make([dynamic]Wire_Path, 0, max(1, int(bundles.n)), context.temp_allocator)
 	for bi in 0..<int(bundles.n) {
-		band := band_world(v, bundles.bundle_tier[bi], int(bundles.bundle_count[bi]))
+		// the covenant width: the drawn path's clearances must match the
+		// CAPPED stroke (a clamped bundle detours for the width it DRAWS)
+		band := link_width_capped(v, topo, bundles, u32(bi))
 		append(&paths, wire_path_compute(v, topo, bundles, u32(bi), band))
 	}
 	return paths
@@ -716,10 +718,13 @@ wire_path_point :: proc(p: ^Wire_Path, t: f32) -> (pos, tangent: rl.Vector2) {
 	return p.pts[p.n-1], {1, 0}
 }
 
-// band_world — the bundle's band width in WORLD px (the drawn-width basis for
-// detour clearances; mirrors band_width's screen formula ÷ scale).
+// band_world — the bundle's drawn width in WORLD px (the detour-clearance
+// basis + the fan-stub width). LOOK §3: mirrors the laneless ladder's
+// UNCAPPED width for endpoint-blind callers; the endpoint-aware consumers
+// (wire_paths_compute, the fan stubs) thread link_width_capped instead so
+// the flags-on render obeys the covenant exactly where it bites.
 band_world :: proc(v: ^View, tier: u16, count: int) -> f32 {
-	return (tier_pipe_width(v, tier) + f32(max(0, count - 1)) * BUNDLE_EXTRA_WIDTH) * 2.2
+	return link_width_world(v, tier, count)
 }
 
 // draw_path_band — draw a thick polyline along the path (each segment a
@@ -737,37 +742,3 @@ draw_path_band :: proc(v: ^View, p: ^Wire_Path, width: f32, col: rl.Color) {
 	last := wire_to_screen(v, p.pts[p.n-1])
 	rl.DrawCircleV(last, width * 0.5, col)
 }
-
-// draw_path_offset_band — draw a thick polyline LATERALLY OFFSET from the
-// path by `lateral` world px (the lane-stripe walk: each segment's endpoints
-// offset along its own normal, round caps at every waypoint). ONE helper for
-// all three lane stripes so they ride the SAME ribbon (3.3 canon preserved).
-draw_path_offset_band :: proc(v: ^View, p: ^Wire_Path, lateral: f32, width: f32, col: rl.Color) {
-	for i in 0..<p.n - 1 {
-		a, b := p.pts[i], p.pts[i+1]
-		d := b - a
-		l := rl.Vector2Length(d)
-		if l <= 0.0001 {
-			continue
-		}
-		nx, ny := -d.y / l, d.x / l
-		wa := rl.Vector2{a.x + nx * lateral, a.y + ny * lateral}
-		wb := rl.Vector2{b.x + nx * lateral, b.y + ny * lateral}
-		sa := wire_to_screen(v, wa)
-		sb := wire_to_screen(v, wb)
-		rl.DrawLineEx(sa, sb, width, col)
-		rl.DrawCircleV(sa, width * 0.5, col)
-	}
-	// the last waypoint's cap (the final segment's normal)
-	if p.n >= 2 {
-		a, b := p.pts[p.n-2], p.pts[p.n-1]
-		d := b - a
-		l := rl.Vector2Length(d)
-		if l > 0.0001 {
-			nx, ny := -d.y / l, d.x / l
-			wb := rl.Vector2{b.x + nx * lateral, b.y + ny * lateral}
-			sb := wire_to_screen(v, wb)
-			rl.DrawCircleV(sb, width * 0.5, col)
-		}
-	}
-}
diff --git a/goldens/a11y_deutan/30000ms.png b/goldens/a11y_deutan/30000ms.png
index 8febfcc..2ac079e 100644
Binary files a/goldens/a11y_deutan/30000ms.png and b/goldens/a11y_deutan/30000ms.png differ
diff --git a/goldens/a11y_deutan/65000ms.png b/goldens/a11y_deutan/65000ms.png
index 3b53da7..0af03fc 100644
Binary files a/goldens/a11y_deutan/65000ms.png and b/goldens/a11y_deutan/65000ms.png differ
diff --git a/goldens/a11y_protan/30000ms.png b/goldens/a11y_protan/30000ms.png
index 8febfcc..2ac079e 100644
Binary files a/goldens/a11y_protan/30000ms.png and b/goldens/a11y_protan/30000ms.png differ
diff --git a/goldens/a11y_protan/65000ms.png b/goldens/a11y_protan/65000ms.png
index 3b53da7..0af03fc 100644
Binary files a/goldens/a11y_protan/65000ms.png and b/goldens/a11y_protan/65000ms.png differ
diff --git a/goldens/a11y_reduced/30000ms.png b/goldens/a11y_reduced/30000ms.png
index d0d5fd0..284328f 100644
Binary files a/goldens/a11y_reduced/30000ms.png and b/goldens/a11y_reduced/30000ms.png differ
diff --git a/goldens/a11y_reduced/65000ms.png b/goldens/a11y_reduced/65000ms.png
index a3aebf9..a88e327 100644
Binary files a/goldens/a11y_reduced/65000ms.png and b/goldens/a11y_reduced/65000ms.png differ
diff --git a/goldens/a11y_scale/30000ms.png b/goldens/a11y_scale/30000ms.png
index 9480893..3b66fb0 100644
Binary files a/goldens/a11y_scale/30000ms.png and b/goldens/a11y_scale/30000ms.png differ
diff --git a/goldens/a11y_scale/65000ms.png b/goldens/a11y_scale/65000ms.png
index 0ab8add..590a856 100644
Binary files a/goldens/a11y_scale/65000ms.png and b/goldens/a11y_scale/65000ms.png differ
diff --git a/goldens/a11y_tritan/30000ms.png b/goldens/a11y_tritan/30000ms.png
index 7d2fc49..ee7e9d0 100644
Binary files a/goldens/a11y_tritan/30000ms.png and b/goldens/a11y_tritan/30000ms.png differ
diff --git a/goldens/a11y_tritan/65000ms.png b/goldens/a11y_tritan/65000ms.png
index 3713cd4..9a51dbd 100644
Binary files a/goldens/a11y_tritan/65000ms.png and b/goldens/a11y_tritan/65000ms.png differ
diff --git a/goldens/advance_block_legacy/15000ms.png b/goldens/advance_block_legacy/15000ms.png
index b2ea711..050f0d2 100644
Binary files a/goldens/advance_block_legacy/15000ms.png and b/goldens/advance_block_legacy/15000ms.png differ
diff --git a/goldens/advance_block_legacy/60000ms.png b/goldens/advance_block_legacy/60000ms.png
index a4ac83d..a6a1f23 100644
Binary files a/goldens/advance_block_legacy/60000ms.png and b/goldens/advance_block_legacy/60000ms.png differ
diff --git a/goldens/advance_block_sla/15000ms.png b/goldens/advance_block_sla/15000ms.png
index 50da7dc..6fcd680 100644
Binary files a/goldens/advance_block_sla/15000ms.png and b/goldens/advance_block_sla/15000ms.png differ
diff --git a/goldens/advance_block_sla/60000ms.png b/goldens/advance_block_sla/60000ms.png
index 65dfb07..4c797ae 100644
Binary files a/goldens/advance_block_sla/60000ms.png and b/goldens/advance_block_sla/60000ms.png differ
diff --git a/goldens/advance_fire/15000ms.png b/goldens/advance_fire/15000ms.png
index 1c5330c..30b2f95 100644
Binary files a/goldens/advance_fire/15000ms.png and b/goldens/advance_fire/15000ms.png differ
diff --git a/goldens/advance_fire/60000ms.png b/goldens/advance_fire/60000ms.png
index 837b59d..a09ae69 100644
Binary files a/goldens/advance_fire/60000ms.png and b/goldens/advance_fire/60000ms.png differ
diff --git a/goldens/bundle/02550ms.png b/goldens/bundle/02550ms.png
index 2696cc5..58402b7 100644
Binary files a/goldens/bundle/02550ms.png and b/goldens/bundle/02550ms.png differ
diff --git a/goldens/bundle/02850ms.png b/goldens/bundle/02850ms.png
index df32b9f..275ab7f 100644
Binary files a/goldens/bundle/02850ms.png and b/goldens/bundle/02850ms.png differ
diff --git a/goldens/demolish/01050ms.png b/goldens/demolish/01050ms.png
index a659d65..feff00a 100644
Binary files a/goldens/demolish/01050ms.png and b/goldens/demolish/01050ms.png differ
diff --git a/goldens/demolish/01250ms.png b/goldens/demolish/01250ms.png
index bbdf248..1ba8663 100644
Binary files a/goldens/demolish/01250ms.png and b/goldens/demolish/01250ms.png differ
diff --git a/goldens/demolish/01300ms.png b/goldens/demolish/01300ms.png
index 759f545..bb450c9 100644
Binary files a/goldens/demolish/01300ms.png and b/goldens/demolish/01300ms.png differ
diff --git a/goldens/demolish/03000ms.png b/goldens/demolish/03000ms.png
index 0fb4d4e..58402b7 100644
Binary files a/goldens/demolish/03000ms.png and b/goldens/demolish/03000ms.png differ
diff --git a/goldens/demolish_bundle/01100ms.png b/goldens/demolish_bundle/01100ms.png
index fbf6b93..11c185f 100644
Binary files a/goldens/demolish_bundle/01100ms.png and b/goldens/demolish_bundle/01100ms.png differ
diff --git a/goldens/demolish_bundle/01500ms.png b/goldens/demolish_bundle/01500ms.png
index 4107e79..5be1e4b 100644
Binary files a/goldens/demolish_bundle/01500ms.png and b/goldens/demolish_bundle/01500ms.png differ
diff --git a/goldens/demolish_bundle/03000ms.png b/goldens/demolish_bundle/03000ms.png
index 0fb4d4e..58402b7 100644
Binary files a/goldens/demolish_bundle/03000ms.png and b/goldens/demolish_bundle/03000ms.png differ
diff --git a/goldens/demolish_node/01250ms.png b/goldens/demolish_node/01250ms.png
index b21f753..ec6b588 100644
Binary files a/goldens/demolish_node/01250ms.png and b/goldens/demolish_node/01250ms.png differ
diff --git a/goldens/demolish_node/01450ms.png b/goldens/demolish_node/01450ms.png
index 2106deb..f272191 100644
Binary files a/goldens/demolish_node/01450ms.png and b/goldens/demolish_node/01450ms.png differ
diff --git a/goldens/demolish_node/02100ms.png b/goldens/demolish_node/02100ms.png
index f76aca6..36cce07 100644
Binary files a/goldens/demolish_node/02100ms.png and b/goldens/demolish_node/02100ms.png differ
diff --git a/goldens/demolish_node/04000ms.png b/goldens/demolish_node/04000ms.png
index f76aca6..36cce07 100644
Binary files a/goldens/demolish_node/04000ms.png and b/goldens/demolish_node/04000ms.png differ
diff --git a/goldens/draw/02500ms.png b/goldens/draw/02500ms.png
index 0fb4d4e..58402b7 100644
Binary files a/goldens/draw/02500ms.png and b/goldens/draw/02500ms.png differ
diff --git a/goldens/dublin_board/30000ms.png b/goldens/dublin_board/30000ms.png
index c25c0e9..f97977a 100644
Binary files a/goldens/dublin_board/30000ms.png and b/goldens/dublin_board/30000ms.png differ
diff --git a/goldens/dublin_board/90000ms.png b/goldens/dublin_board/90000ms.png
index ec407c8..4f6b6c0 100644
Binary files a/goldens/dublin_board/90000ms.png and b/goldens/dublin_board/90000ms.png differ
diff --git a/goldens/ecmp/01250ms.png b/goldens/ecmp/01250ms.png
index b43e229..0ccffba 100644
Binary files a/goldens/ecmp/01250ms.png and b/goldens/ecmp/01250ms.png differ
diff --git a/goldens/ecmp/01350ms.png b/goldens/ecmp/01350ms.png
index 2fadca4..492b849 100644
Binary files a/goldens/ecmp/01350ms.png and b/goldens/ecmp/01350ms.png differ
diff --git a/goldens/ecmp/03000ms.png b/goldens/ecmp/03000ms.png
index 4c80382..5f89784 100644
Binary files a/goldens/ecmp/03000ms.png and b/goldens/ecmp/03000ms.png differ
diff --git a/goldens/ecmp_cost/01150ms.png b/goldens/ecmp_cost/01150ms.png
index 2c1f522..1fba750 100644
Binary files a/goldens/ecmp_cost/01150ms.png and b/goldens/ecmp_cost/01150ms.png differ
diff --git a/goldens/ecmp_cost/01450ms.png b/goldens/ecmp_cost/01450ms.png
index 028b88e..2010ecd 100644
Binary files a/goldens/ecmp_cost/01450ms.png and b/goldens/ecmp_cost/01450ms.png differ
diff --git a/goldens/era_advance/10000ms.png b/goldens/era_advance/10000ms.png
index a90032b..2d60340 100644
Binary files a/goldens/era_advance/10000ms.png and b/goldens/era_advance/10000ms.png differ
diff --git a/goldens/era_advance/55000ms.png b/goldens/era_advance/55000ms.png
index 12a4d32..0ca3c61 100644
Binary files a/goldens/era_advance/55000ms.png and b/goldens/era_advance/55000ms.png differ
diff --git a/goldens/estate_surge/25000ms.png b/goldens/estate_surge/25000ms.png
index f74a6e0..ce7b7ac 100644
Binary files a/goldens/estate_surge/25000ms.png and b/goldens/estate_surge/25000ms.png differ
diff --git a/goldens/estate_surge/75000ms.png b/goldens/estate_surge/75000ms.png
index 8d807ef..a06b02a 100644
Binary files a/goldens/estate_surge/75000ms.png and b/goldens/estate_surge/75000ms.png differ
diff --git a/goldens/flow/02100ms.png b/goldens/flow/02100ms.png
index c9c3cdf..feff00a 100644
Binary files a/goldens/flow/02100ms.png and b/goldens/flow/02100ms.png differ
diff --git a/goldens/flow/02150ms.png b/goldens/flow/02150ms.png
index 16eae74..11c185f 100644
Binary files a/goldens/flow/02150ms.png and b/goldens/flow/02150ms.png differ
diff --git a/goldens/flow/02250ms.png b/goldens/flow/02250ms.png
index 9b289be..ea5f1fe 100644
Binary files a/goldens/flow/02250ms.png and b/goldens/flow/02250ms.png differ
diff --git a/goldens/forecast_preview/30000ms.png b/goldens/forecast_preview/30000ms.png
index 0deef85..eb122c2 100644
Binary files a/goldens/forecast_preview/30000ms.png and b/goldens/forecast_preview/30000ms.png differ
diff --git a/goldens/forecast_preview/31000ms.png b/goldens/forecast_preview/31000ms.png
index 0a3e892..e93a822 100644
Binary files a/goldens/forecast_preview/31000ms.png and b/goldens/forecast_preview/31000ms.png differ
diff --git a/goldens/forecast_preview/32000ms.png b/goldens/forecast_preview/32000ms.png
index 8fdd415..a31a235 100644
Binary files a/goldens/forecast_preview/32000ms.png and b/goldens/forecast_preview/32000ms.png differ
diff --git a/goldens/forecast_preview/33000ms.png b/goldens/forecast_preview/33000ms.png
index 121daff..93fc941 100644
Binary files a/goldens/forecast_preview/33000ms.png and b/goldens/forecast_preview/33000ms.png differ
diff --git a/goldens/forecast_shift/01300ms.png b/goldens/forecast_shift/01300ms.png
index c889b0b..f42e72d 100644
Binary files a/goldens/forecast_shift/01300ms.png and b/goldens/forecast_shift/01300ms.png differ
diff --git a/goldens/forecast_shift/02800ms.png b/goldens/forecast_shift/02800ms.png
index 27c39ca..eca11a4 100644
Binary files a/goldens/forecast_shift/02800ms.png and b/goldens/forecast_shift/02800ms.png differ
diff --git a/goldens/growth/01500ms.png b/goldens/growth/01500ms.png
index 7c44735..e2cab9a 100644
Binary files a/goldens/growth/01500ms.png and b/goldens/growth/01500ms.png differ
diff --git a/goldens/growth/15000ms.png b/goldens/growth/15000ms.png
index 2839d54..09f4634 100644
Binary files a/goldens/growth/15000ms.png and b/goldens/growth/15000ms.png differ
diff --git a/goldens/growth/45000ms.png b/goldens/growth/45000ms.png
index d45cbd8..37b8aae 100644
Binary files a/goldens/growth/45000ms.png and b/goldens/growth/45000ms.png differ
diff --git a/goldens/growth/88000ms.png b/goldens/growth/88000ms.png
index a5afb46..9967971 100644
Binary files a/goldens/growth/88000ms.png and b/goldens/growth/88000ms.png differ
diff --git a/goldens/health_lose/05000ms.png b/goldens/health_lose/05000ms.png
index 201d31a..d248a42 100644
Binary files a/goldens/health_lose/05000ms.png and b/goldens/health_lose/05000ms.png differ
diff --git a/goldens/health_lose/21000ms.png b/goldens/health_lose/21000ms.png
index e87055a..cdb2256 100644
Binary files a/goldens/health_lose/21000ms.png and b/goldens/health_lose/21000ms.png differ
diff --git a/goldens/health_lose/23000ms.png b/goldens/health_lose/23000ms.png
index 73a5ffe..d2045b9 100644
Binary files a/goldens/health_lose/23000ms.png and b/goldens/health_lose/23000ms.png differ
diff --git a/goldens/health_win/150500ms.png b/goldens/health_win/150500ms.png
index 6803201..6713af6 100644
Binary files a/goldens/health_win/150500ms.png and b/goldens/health_win/150500ms.png differ
diff --git a/goldens/health_win/30000ms.png b/goldens/health_win/30000ms.png
index 46dd139..dd587e6 100644
Binary files a/goldens/health_win/30000ms.png and b/goldens/health_win/30000ms.png differ
diff --git a/goldens/health_win/75000ms.png b/goldens/health_win/75000ms.png
index 648e041..8e03cfb 100644
Binary files a/goldens/health_win/75000ms.png and b/goldens/health_win/75000ms.png differ
diff --git a/goldens/juice/30000ms.png b/goldens/juice/30000ms.png
index d0d5fd0..284328f 100644
Binary files a/goldens/juice/30000ms.png and b/goldens/juice/30000ms.png differ
diff --git a/goldens/juice/65000ms.png b/goldens/juice/65000ms.png
index b53e0e1..4ff330f 100644
Binary files a/goldens/juice/65000ms.png and b/goldens/juice/65000ms.png differ
diff --git a/goldens/legacy_decay/15000ms.png b/goldens/legacy_decay/15000ms.png
index 1c5330c..30b2f95 100644
Binary files a/goldens/legacy_decay/15000ms.png and b/goldens/legacy_decay/15000ms.png differ
diff --git a/goldens/legacy_decay/60000ms.png b/goldens/legacy_decay/60000ms.png
index 837b59d..a09ae69 100644
Binary files a/goldens/legacy_decay/60000ms.png and b/goldens/legacy_decay/60000ms.png differ
diff --git a/goldens/legacy_modernized/15000ms.png b/goldens/legacy_modernized/15000ms.png
index 1c5330c..30b2f95 100644
Binary files a/goldens/legacy_modernized/15000ms.png and b/goldens/legacy_modernized/15000ms.png differ
diff --git a/goldens/legacy_modernized/60000ms.png b/goldens/legacy_modernized/60000ms.png
index 1f36745..29b0b3c 100644
Binary files a/goldens/legacy_modernized/60000ms.png and b/goldens/legacy_modernized/60000ms.png differ
diff --git a/goldens/lose/03000ms.png b/goldens/lose/03000ms.png
index 0458045..0f4af74 100644
Binary files a/goldens/lose/03000ms.png and b/goldens/lose/03000ms.png differ
diff --git a/goldens/node_health/00050ms.png b/goldens/node_health/00050ms.png
index 6f6429c..1e432c8 100644
Binary files a/goldens/node_health/00050ms.png and b/goldens/node_health/00050ms.png differ
diff --git a/goldens/node_health/10000ms.png b/goldens/node_health/10000ms.png
index 82ec465..951cfd0 100644
Binary files a/goldens/node_health/10000ms.png and b/goldens/node_health/10000ms.png differ
diff --git a/goldens/node_health/20000ms.png b/goldens/node_health/20000ms.png
index 2933365..4e71d7e 100644
Binary files a/goldens/node_health/20000ms.png and b/goldens/node_health/20000ms.png differ
diff --git a/goldens/pause/65000ms.png b/goldens/pause/65000ms.png
index abfdba9..dc25f24 100644
Binary files a/goldens/pause/65000ms.png and b/goldens/pause/65000ms.png differ
diff --git a/goldens/pause/80000ms.png b/goldens/pause/80000ms.png
index e21df65..df2988e 100644
Binary files a/goldens/pause/80000ms.png and b/goldens/pause/80000ms.png differ
diff --git a/goldens/place/02500ms.png b/goldens/place/02500ms.png
index 0026eb9..523c211 100644
Binary files a/goldens/place/02500ms.png and b/goldens/place/02500ms.png differ
diff --git a/goldens/place/03000ms.png b/goldens/place/03000ms.png
index 0026eb9..523c211 100644
Binary files a/goldens/place/03000ms.png and b/goldens/place/03000ms.png differ
diff --git a/goldens/qos/01000ms.png b/goldens/qos/01000ms.png
index 0890840..49a14f2 100644
Binary files a/goldens/qos/01000ms.png and b/goldens/qos/01000ms.png differ
diff --git a/goldens/qos/65000ms.png b/goldens/qos/65000ms.png
index 62b94e4..3c52358 100644
Binary files a/goldens/qos/65000ms.png and b/goldens/qos/65000ms.png differ
diff --git a/goldens/qos_auto/01000ms.png b/goldens/qos_auto/01000ms.png
index 0890840..49a14f2 100644
Binary files a/goldens/qos_auto/01000ms.png and b/goldens/qos_auto/01000ms.png differ
diff --git a/goldens/qos_auto/06000ms.png b/goldens/qos_auto/06000ms.png
index c11877d..7cd6b95 100644
Binary files a/goldens/qos_auto/06000ms.png and b/goldens/qos_auto/06000ms.png differ
diff --git a/goldens/qos_contention/01000ms.png b/goldens/qos_contention/01000ms.png
index b395444..9751419 100644
Binary files a/goldens/qos_contention/01000ms.png and b/goldens/qos_contention/01000ms.png differ
diff --git a/goldens/qos_contention/03000ms.png b/goldens/qos_contention/03000ms.png
index ff922aa..3c9dd36 100644
Binary files a/goldens/qos_contention/03000ms.png and b/goldens/qos_contention/03000ms.png differ
diff --git a/goldens/qos_contention/10000ms.png b/goldens/qos_contention/10000ms.png
index 9f1dcf6..f36d31c 100644
Binary files a/goldens/qos_contention/10000ms.png and b/goldens/qos_contention/10000ms.png differ
diff --git a/goldens/qos_emphasis/01000ms.png b/goldens/qos_emphasis/01000ms.png
index 0890840..49a14f2 100644
Binary files a/goldens/qos_emphasis/01000ms.png and b/goldens/qos_emphasis/01000ms.png differ
diff --git a/goldens/qos_emphasis/05000ms.png b/goldens/qos_emphasis/05000ms.png
index 51ddc0a..160c564 100644
Binary files a/goldens/qos_emphasis/05000ms.png and b/goldens/qos_emphasis/05000ms.png differ
diff --git a/goldens/qos_emphasis/12000ms.png b/goldens/qos_emphasis/12000ms.png
index 95cfaba..12ab5d9 100644
Binary files a/goldens/qos_emphasis/12000ms.png and b/goldens/qos_emphasis/12000ms.png differ
diff --git a/goldens/qos_manual/01000ms.png b/goldens/qos_manual/01000ms.png
index 0890840..49a14f2 100644
Binary files a/goldens/qos_manual/01000ms.png and b/goldens/qos_manual/01000ms.png differ
diff --git a/goldens/qos_manual/06000ms.png b/goldens/qos_manual/06000ms.png
index c0dbf58..a17ee4c 100644
Binary files a/goldens/qos_manual/06000ms.png and b/goldens/qos_manual/06000ms.png differ
diff --git a/goldens/router_ceiling/02500ms.png b/goldens/router_ceiling/02500ms.png
index bcd0552..224b399 100644
Binary files a/goldens/router_ceiling/02500ms.png and b/goldens/router_ceiling/02500ms.png differ
diff --git a/goldens/router_ceiling/03500ms.png b/goldens/router_ceiling/03500ms.png
index bcd0552..224b399 100644
Binary files a/goldens/router_ceiling/03500ms.png and b/goldens/router_ceiling/03500ms.png differ
diff --git a/goldens/router_tiers/02500ms.png b/goldens/router_tiers/02500ms.png
index d531eb2..9c45c5b 100644
Binary files a/goldens/router_tiers/02500ms.png and b/goldens/router_tiers/02500ms.png differ
diff --git a/goldens/router_tiers/03500ms.png b/goldens/router_tiers/03500ms.png
index d531eb2..9c45c5b 100644
Binary files a/goldens/router_tiers/03500ms.png and b/goldens/router_tiers/03500ms.png differ
diff --git a/goldens/sla/01000ms.png b/goldens/sla/01000ms.png
index 6dd3f0b..55cc846 100644
Binary files a/goldens/sla/01000ms.png and b/goldens/sla/01000ms.png differ
diff --git a/goldens/sla/04000ms.png b/goldens/sla/04000ms.png
index dbf5189..81e1e28 100644
Binary files a/goldens/sla/04000ms.png and b/goldens/sla/04000ms.png differ
diff --git a/goldens/sla/10000ms.png b/goldens/sla/10000ms.png
index 446cebd..2438b35 100644
Binary files a/goldens/sla/10000ms.png and b/goldens/sla/10000ms.png differ
diff --git a/goldens/spawn_feel/03600ms.png b/goldens/spawn_feel/03600ms.png
index 7dc3dad..64b70db 100644
Binary files a/goldens/spawn_feel/03600ms.png and b/goldens/spawn_feel/03600ms.png differ
diff --git a/goldens/spawn_feel/03900ms.png b/goldens/spawn_feel/03900ms.png
index 2c27973..a503117 100644
Binary files a/goldens/spawn_feel/03900ms.png and b/goldens/spawn_feel/03900ms.png differ
diff --git a/goldens/spawn_feel/04000ms.png b/goldens/spawn_feel/04000ms.png
index 895a15e..f4705cc 100644
Binary files a/goldens/spawn_feel/04000ms.png and b/goldens/spawn_feel/04000ms.png differ
diff --git a/goldens/spawn_feel/04100ms.png b/goldens/spawn_feel/04100ms.png
index 525fe37..8163eaa 100644
Binary files a/goldens/spawn_feel/04100ms.png and b/goldens/spawn_feel/04100ms.png differ
diff --git a/goldens/spawn_feel/04250ms.png b/goldens/spawn_feel/04250ms.png
index 72de172..da9c3da 100644
Binary files a/goldens/spawn_feel/04250ms.png and b/goldens/spawn_feel/04250ms.png differ
diff --git a/goldens/spawn_feel/04400ms.png b/goldens/spawn_feel/04400ms.png
index cf6b641..8b9012a 100644
Binary files a/goldens/spawn_feel/04400ms.png and b/goldens/spawn_feel/04400ms.png differ
diff --git a/goldens/spawn_feel/07600ms.png b/goldens/spawn_feel/07600ms.png
index f1241d2..ceaf24f 100644
Binary files a/goldens/spawn_feel/07600ms.png and b/goldens/spawn_feel/07600ms.png differ
diff --git a/goldens/spawn_feel/07900ms.png b/goldens/spawn_feel/07900ms.png
index 5a19435..0d5a6d9 100644
Binary files a/goldens/spawn_feel/07900ms.png and b/goldens/spawn_feel/07900ms.png differ
diff --git a/goldens/spawn_feel/08000ms.png b/goldens/spawn_feel/08000ms.png
index 4c67822..513cca6 100644
Binary files a/goldens/spawn_feel/08000ms.png and b/goldens/spawn_feel/08000ms.png differ
diff --git a/goldens/surge/119500ms.png b/goldens/surge/119500ms.png
index 27d52ec..0c7c63b 100644
Binary files a/goldens/surge/119500ms.png and b/goldens/surge/119500ms.png differ
diff --git a/goldens/surge/149000ms.png b/goldens/surge/149000ms.png
index 59fe5bd..e789244 100644
Binary files a/goldens/surge/149000ms.png and b/goldens/surge/149000ms.png differ
diff --git a/goldens/surge/170000ms.png b/goldens/surge/170000ms.png
index 50f3ac5..e0e4277 100644
Binary files a/goldens/surge/170000ms.png and b/goldens/surge/170000ms.png differ
diff --git a/goldens/surge/30000ms.png b/goldens/surge/30000ms.png
index 7bd2d67..42790c7 100644
Binary files a/goldens/surge/30000ms.png and b/goldens/surge/30000ms.png differ
diff --git a/goldens/surge/65000ms.png b/goldens/surge/65000ms.png
index feaecb9..ec35489 100644
Binary files a/goldens/surge/65000ms.png and b/goldens/surge/65000ms.png differ
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
index 5e8ad72..3a0a706 100644
Binary files a/goldens/terminal_types/05000ms.png and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
index f54d4d7..8b762d0 100644
Binary files a/goldens/terminal_types/30000ms.png and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/warn/01500ms.png b/goldens/warn/01500ms.png
index 6e7ee58..9cee0b6 100644
Binary files a/goldens/warn/01500ms.png and b/goldens/warn/01500ms.png differ
diff --git a/goldens/warn/45000ms.png b/goldens/warn/45000ms.png
index 49a2c3f..6a0bda7 100644
Binary files a/goldens/warn/45000ms.png and b/goldens/warn/45000ms.png differ
diff --git a/goldens/warn/65000ms.png b/goldens/warn/65000ms.png
index ab1648a..c9908f1 100644
Binary files a/goldens/warn/65000ms.png and b/goldens/warn/65000ms.png differ
diff --git a/goldens/win/02300ms.png b/goldens/win/02300ms.png
index bbdf248..1ba8663 100644
Binary files a/goldens/win/02300ms.png and b/goldens/win/02300ms.png differ
diff --git a/harness/demo.odin b/harness/demo.odin
index 372c0f6..57a1208 100644
--- a/harness/demo.odin
+++ b/harness/demo.odin
@@ -186,6 +186,7 @@ Demo :: struct {
 	growth_on:          bool,    // 5.1: `growth on` — the director's map growth (run setup, like the fixture)
 	advance_gate_on:    bool,    // 6.2: `advance gate on` — the era-advance modernization gate (run setup; disabled = the 6.1 mechanics, byte-identical)
 	map_source:         u8,      // v2-dublin-board: `map dublin` / `map procedural` — the named map input (run setup, like the seed; 0 = procedural — the zero value, every legacy demo stays byte-identical)
+	zoom:               f32,     // LOOK §1: `zoom <z>` — the pinned camera altitude for this demo's captures (view-only run setup, like a11y; 1.0 = the fit, the zero value — every legacy demo stays byte-identical)
 
 	captures:           [dynamic]i64, // T2 capture times (ms)
 	win_goal:           u32, // 1.4: packets to deliver for a WIN (0 = win/lose disabled)
@@ -629,6 +630,20 @@ parse_demo :: proc(name: string, text: string) -> (Demo, string) {
 			case:
 				return {}, fmt.tprintf("bad map value %q (want dublin|procedural): %s", fields[1], line)
 			}
+		case "zoom":
+			// zoom <z> — LOOK §1: pin the capture altitude (the effective
+			// camera zoom; 1.0 = the fit). VIEW-ONLY run setup (the a11y
+			// precedent): the sim, the action log, and the T1/replay hashes
+			// never see it — the run path derives the view transform + the
+			// ladder rung from it before capturing.
+			if len(fields) < 2 {
+				return {}, fmt.tprintf("bad zoom (want: zoom <f32>): %s", line)
+			}
+			z, okz := strconv.parse_f32(fields[1])
+			if !okz || !(z >= 1.0 && z <= 4.0) { // the NaN-rejecting band test (z < 1.0 is false for NaN)
+				return {}, fmt.tprintf("bad zoom %q (want 1.0..4.0 — the camera band): %s", fields[1], line)
+			}
+			d.zoom = z
 		case "advance":
 			// advance gate on — the 6.2 era-advance modernization gate (run
 			// setup, like growth on / health on: re-created identically on
@@ -671,6 +686,12 @@ parse_demo :: proc(name: string, text: string) -> (Demo, string) {
 	if d.growth_on && d.era == 0 {
 		return {}, "growth on requires an era >= 1 (era 0 is the legacy director-inactive mode — growth would be inert and bless a no-growth golden)"
 	}
+	// LOOK: the zoom directive's zero value is 0.0 — normalize the ABSENT
+	// directive to the fit (1.0) so the run path never sees zoom 0 (an
+	// explicit `zoom 0` is rejected above; only the struct zero lands here).
+	if d.zoom == 0 {
+		d.zoom = 1.0
+	}
 	return d, ""
 }
 
diff --git a/harness/palcheck.odin b/harness/palcheck.odin
index 9814223..36d5d04 100644
--- a/harness/palcheck.odin
+++ b/harness/palcheck.odin
@@ -1,12 +1,14 @@
 package main
 
 // palcheck.odin — Story 7.1's PALETTE-PRESENCE gate (Perkins r1 W2): a
-// committed, mechanical scan that the §2 look-book palette is OBJECTIVELY
-// present in what ships. The pre-PR scratch pixel-scan was disposable and it
-// MISSED the B1 sprite-crop bug (house bodies absent while roofs rendered) —
-// this gate would have caught it: it scans the BLESSED juice goldens for the
-// exact canon hexes (house bodies AND roofs, the host, the LED green, the
-// play-marking) + renders a zoomed frame to pin the full-alpha lane read +
+// committed, mechanical scan that the the shipped look-book palette is
+// OBJECTIVELY present in what ships. The pre-PR scratch pixel-scan was
+// disposable and it MISSED the B1 sprite-crop bug (house bodies absent while
+// roofs rendered) — this gate would have caught it: it scans the BLESSED
+// juice goldens for the exact canon hexes (house bodies AND roofs, the host,
+// the LED green, the play-marking) + renders zoomed frames to pin the LOOK
+// laneless single stroke (no lane-stripe tokens, the covenant width at
+// pixels — section 2) +
 // checks the crisis banner's drawn border sits ON the crisis_banner_rect the
 // alerts-as-nav hit-test uses (the single-source rule, mechanically).
 //
@@ -213,6 +215,20 @@ TIER_RING_MID := rl.Color{47, 168, 158, 255}
 TIER_RING_HIGH := rl.Color{139, 123, 216, 255}
 LED_GREEN := rl.Color{77, 137, 113, 255}   // the basic puck's LED washed with steel (0.40)
 LANE_AMBER := rl.Color{224, 138, 46, 255}
+
+// LOOK §1 dusk-dial predicted blends — the dial dot color (DUSK_WARM /
+// the DC cool / the amber shift) alpha-composited over the LAND tint
+// (239,228,186 — the fixture's underlay; see the spawn comment below) at
+// the per-rung dial alphas. The pixel scan counts the
+// PREDICTED blend (the T2 predicted-blend craft), so a dial-alpha change
+// fails here with a cause, not as a silent count drift.
+DUSK_WARM_BLENDS := [3]rl.Color{
+	{255, 214, 120, 255}, // ACCESS: alpha 0 — nothing draws (the dark diorama)
+	{247, 221, 155, 255}, // DIST: warm at alpha 120 over the land tint
+	{251, 217, 135, 255}, // CORE: warm at alpha 200 over the land tint
+}
+DUSK_DC_BLEND_CORE := rl.Color{141, 197, 243, 255} // the DC cool at alpha 210 over the land tint
+DUSK_AMBER_BLEND_CORE := rl.Color{245, 203, 114, 255} // the amber-shifted dot at alpha 200 over the land tint
 STATE_CRITICAL := rl.Color{232, 69, 69, 255}
 
 // MAP_IDENTITY_PIN — the FNV-1a-64 over the seed-7 map cells (world 1040x780,
@@ -233,6 +249,35 @@ check :: proc(ok: bool, name: string, n: int) {
 
 // count_exact — exact-color pixels in an rl.Image (normalized: the caller
 // flips + swizzles before passing).
+// measure_color_run — the longest contiguous vertical run of pixels within
+// `tol` of `col` at screen column x (the stroke-width measurement for a
+// horizontal wire crossing that column; the longest run ignores stray AA
+// pixels). Returns found=false when no pixel of the family is on the column.
+measure_color_run :: proc(img: rl.Image, col: rl.Color, x: int) -> (run: f32, found: bool) {
+	if x < 0 || x >= int(img.width) {
+		return 0, false
+	}
+	px := rl.LoadImageColors(img)
+	defer rl.UnloadImageColors(px)
+	best, cur: int = 0, 0
+	for y in 0..<int(img.height) {
+		i := y * int(img.width) + x
+		c := px[i]
+		if abs(i32(c.r) - i32(col.r)) <= 30 && abs(i32(c.g) - i32(col.g)) <= 30 && abs(i32(c.b) - i32(col.b)) <= 30 {
+			cur += 1
+			if cur > best {
+				best = cur
+			}
+		} else {
+			cur = 0
+		}
+	}
+	if best == 0 {
+		return 0, false
+	}
+	return f32(best), true
+}
+
 count_exact :: proc(img: rl.Image, col: rl.Color) -> int {
 	px := rl.LoadImageColors(img)
 	defer rl.UnloadImageColors(px)
@@ -384,23 +429,26 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 	// wall band (below); a top-crop kills the hip cap (the HOST_ROOF pin).
 	roof_names := [4]string{"house roof coral", "house roof gold", "house roof sage", "house roof sky"}
 	for i in 0..<4 {
-		check(count_exact(calm, HOUSE_ROOFS[i]) > 45, roof_names[i], count_exact(calm, HOUSE_ROOFS[i]))
+		check(count_exact(calm, HOUSE_ROOFS[i]) > 10, roof_names[i], count_exact(calm, HOUSE_ROOFS[i])) // LOOK §1 re-pin: the blessed corpus renders at the CORE rung (roof flecks measured 28/28/22/14; floor ~50% keeps the crop canary)
 	}
 	// 1b. the host roof + the wall-band canary (bilinear — tolerance) + LEDs +
 	// the puck's dark hardware tone.
-	check(count_exact(calm, HOST_ROOF) > 90, "host roof", count_exact(calm, HOST_ROOF))
+	check(count_exact(calm, HOST_ROOF) > 10, "host roof", count_exact(calm, HOST_ROOF)) // LOOK §1 re-pin (measured 20)
 	// the bottom-content canary — the play-marking is DELETED by design
 	// (docs/silhouette-spec.md §1, the silhouette rework); its canary job
 	// moves to the washed FRONT WALL BAND (the sprite's bottom half — a
 	// bottom-cropping blit loses it the way the B1 crop once lost the
 	// marking). v2-blender-sculpt: measured 881 px near-tol on the re-blessed
 	// frame -> floor 500 (~57%).
-	check(count_near(calm, HOST_WALL, 6) > 500, "host wall band (B1 canary)", count_near(calm, HOST_WALL, 6))
+	check(count_near(calm, HOST_WALL, 6) > 65, "host wall band (B1 canary)", count_near(calm, HOST_WALL, 6)) // LOOK §1 re-pin (measured 134; the bottom-crop canary survives at ~50%)
 	// D-2 (v2-arch-egress S3) re-pin: the doubled streaming serialization
 	// shifts one puck's 30s congestion level (a calm LED pair reads 5 px on
 	// the re-blessed frame, was 6) — floor 4 keeps the canary (a broken LED
 	// render reads 0) without coupling to a single pixel of AA.
-	check(count_exact(calm, LED_GREEN) > 4, "puck LEDs", count_exact(calm, LED_GREEN))
+	// LOOK §1/L4 re-pin: the LED exact hex vanished in the CORE-rung bilinear
+	// resample (sub-pixel LEDs) — the canary moves to the tone band (measured
+	// 19 px at tol 24; floor ~40% keeps the broken-LED-reads-0 canary)
+	check(count_near(calm, LED_GREEN, 24) > 8, "puck LEDs (tone band)", count_near(calm, LED_GREEN, 24))
 	check(count_near(calm, rl.Color{86, 98, 116, 255}, 12) > 200, "puck hardware tone", count_near(calm, rl.Color{86, 98, 116, 255}, 12))
 
 	// 1e. the 5.11 class-analogue sprites (the #65 canon set — Perkins r1 W1):
@@ -418,8 +466,11 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		return 2
 	}
 	defer rl.UnloadImage(term)
-	check(count_exact(term, SMALL_BIZ_TAN) > 85, "small_biz sprite (5.11 office)", count_exact(term, SMALL_BIZ_TAN))
-	check(count_exact(term, CAMPUS_BRICK) > 75, "campus sprite (5.11 campus)", count_exact(term, CAMPUS_BRICK)) // real-ladder re-bless re-pin: the re-blessed terminal_types frame renders 81 brick px (was 100+)
+	check(count_exact(term, SMALL_BIZ_TAN) > 30, "small_biz sprite (5.11 office)", count_exact(term, SMALL_BIZ_TAN)) // LOOK §1 re-pin (measured 60)
+	// LOOK §4 re-pin: the campus brick hex collapsed to 1 exact px at the
+	// CORE-rung resample (the 1.22 base shrank the sprite ~20%) — the canary
+	// moves to the tone band (measured 87 px at tol 12; floor ~45%)
+	check(count_near(term, CAMPUS_BRICK, 12) > 40, "campus sprite (5.11 campus, tone band)", count_near(term, CAMPUS_BRICK, 12)) // real-ladder re-bless re-pin: the re-blessed terminal_types frame renders 81 brick px (was 100+)
 	// v2-node-clarity Q2a: the TYPE-CHIP pins — the chips' glyphs draw the
 	// family tokens at FULL alpha (the washes composite at the token alpha,
 	// so the pure hexes appear only in the chips). A missing chip (the
@@ -436,14 +487,14 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 	// near-tol — the ring is a 1-2px stroke at fit, antialiased by the
 	// harness render). The terminal_types golden carries a mid router (the
 	// demo's hub); the router_tiers golden carries all three tiers.
-	check(count_exact(term, PUCK_MID_BODY) > 100, "mid puck tier wash renders", count_exact(term, PUCK_MID_BODY))
-	check(count_near(term, TIER_RING_MID, 8) > 40, "mid tier ring renders", count_near(term, TIER_RING_MID, 8))
+	check(count_exact(term, PUCK_MID_BODY) > 25, "mid puck tier wash renders", count_exact(term, PUCK_MID_BODY)) // LOOK §1 re-pin (measured 52)
+	check(count_near(term, TIER_RING_MID, 8) > 18, "mid tier ring renders", count_near(term, TIER_RING_MID, 8)) // LOOK §1 re-pin (measured 36 — the ring floor now holds it at 2px, L4 will re-measure)
 	tiers_g, okt := load_frame("goldens/router_tiers/02500ms.png")
 	if !okt {
 		fmt.eprintln("palcheck: cannot load the router_tiers golden (re-bless first)")
 		fails += 1
 	} else {
-		check(count_near(tiers_g, TIER_RING_BASIC, 8) > 40, "basic tier ring renders", count_near(tiers_g, TIER_RING_BASIC, 8))
+		check(count_near(tiers_g, TIER_RING_BASIC, 8) > 18, "basic tier ring renders", count_near(tiers_g, TIER_RING_BASIC, 8)) // LOOK §1 re-pin (measured 36)
 		check(count_near(tiers_g, TIER_RING_HIGH, 8) > 40, "high tier ring renders", count_near(tiers_g, TIER_RING_HIGH, 8))
 		rl.UnloadImage(tiers_g)
 	}
@@ -537,42 +588,163 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		check(h3 != h1, fmt.aprintf("map seed sensitivity (seed 8 %016x != seed 7)", h3), int(h3))
 	}
 
-	// --- 2. the zoomed lane read (the app-layer lane_detail reveal) ---------
+	// --- 2. LOOK §3: the laneless single stroke + the covenant width (live) --
+	// The laneless ruling, pinned at PIXELS: (a) NO lane-stripe token renders
+	// anywhere in the world frame (the 3.3 spatial-lane stripes are gone —
+	// queues are ingress/egress on ROUTERS, the road doesn't gossip; a
+	// reintroduced stripe fails the zero-count), (b) the tier HUES carry the
+	// link (copper narrow + gold wide — tier ID stays mandatory at a glance),
+	// (c) the measured stroke width equals the ruled ladder table at the
+	// ACCESS rung, and again at the CORE rung (the rung tables actually key
+	// the draw — a rung-deaf draw fails one of the two measurements), and
+	// (d) the scale covenant holds at pixels: measured stroke <= LINK_RATIO_CAP
+	// x the live house footprint. The table-level pins live in look_l1_test;
+	// these are the draw-path truth (the tie-deconflect craft: exact-color
+	// counting over the rlsw readback).
 	{
 		state: pp.Run_State
 		pp.run_init(&state, 7, cat.hash, cat.balance.logic_hz)
 		res, _ := pp.node_type_index(cat, "residential")
 		host, _ := pp.node_type_index(cat, "content_host")
 		rtm, _ := pp.node_type_index(cat, "router_mid")
-		pp.topology_spawn_node(&state.topology, res, {4, 15}, cat)
-		pp.topology_spawn_node(&state.topology, rtm, {12, 15}, cat)
-		pp.topology_spawn_node(&state.topology, host, {20, 15}, cat)
-		narrow, _ := pp.pipe_tier_index(cat, "narrow")
+		// ON THE LAND (seed 7's map is water+islands — the dusk-blend
+		// predictions composite over the LAND tint (239,228,186); a water
+		// underlay would shift every predicted byte): house (21,2) - router
+		// (25,2) - host (29,4); the standard wire is horizontal at tile y=2.
+		pp.topology_spawn_node(&state.topology, res, {21, 2}, cat)
+		pp.topology_spawn_node(&state.topology, rtm, {25, 2}, cat)
+		pp.topology_spawn_node(&state.topology, host, {29, 4}, cat)
+		standard, _ := pp.pipe_tier_index(cat, "standard")
 		wide, _ := pp.pipe_tier_index(cat, "wide")
-		re1, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = 0, b = 1, tier = narrow}}, cat)
+		re1, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = 0, b = 1, tier = standard}}, cat)
 		re2, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = 1, b = 2, tier = wide}}, cat)
+		// real WFQ weights (an express-heavy pipe would have painted a fat
+		// amber stripe pre-LOOK — the laneless zero-count must run against a
+		// fixture that WOULD draw them, not a default-pipe vacuous pass)
 		pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Set_Weights{pipe = re1.id, weights = {4, 2, 1}}}, cat)
-		// 08-19: the DEFAULT pipe is 100% Standard (no Express stripe) — the
-		// oracle's amber presence needs an explicit player-engineered Express
-		// weight on the wide pipe too (express_heavy, a real panel preset).
 		pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Set_Weights{pipe = re2.id, weights = {4, 2, 1}}}, cat)
 		for t in u64(1)..=120 {
 			pp.step(&state, t, {}, cat)
 			clear(&state.events)
 		}
-		// zoom into the narrow pipe (lane_detail on — the full lane read)
-		view.scale *= 2.6
-		view.off_x = f32(view.win_w) / 2 - f32(8) * view.tile_px * view.scale
-		view.off_y = f32(view.win_h) / 2 - f32(15) * view.tile_px * view.scale
-		view.lane_detail = true
-		rl.BeginDrawing()
-		rnd.draw_world(&view, &state.topology, &state.bundles, &state.flow, &state.crisis, 120, {}, -1, -1, state.seed)
-		rl.EndDrawing()
-		img := rl.LoadImageFromScreen()
-		normalize(&img)
-		n := count_exact(img, LANE_AMBER)
-		rl.UnloadImage(img)
-		check(n > 1000, "zoomed lane stripes (full alpha)", n)
+		steel := view.palette.pipe_steel // the STANDARD tier's token (the shipped hue map)
+		gold := view.palette.pipe_fiber
+		sv_scale, sv_ox, sv_oy := view.scale, view.off_x, view.off_y
+		sv_rung := view.zoom_rung
+		defer {
+			view.scale = sv_scale
+			view.off_x = sv_ox
+			view.off_y = sv_oy
+			view.zoom_rung = sv_rung
+		}
+		// the wire: house (21,2) -> router (25,2), exactly horizontal at
+		// tile y=2; the scan column sits at the midpoint (tile x=23). The
+		// host (the DC anchor) sits at (29,4).
+		// LOOK §1 legs: ACCESS (z 2.6) / DISTRIBUTION (z 1.4) / CORE (z 1.0).
+		zs := [3]f32{2.6, 1.4, 1.0}
+		roof_counts: [3]int
+		for leg in 0..<3 {
+			z := zs[leg]
+			fit := rnd.camera_fit(&view)
+			view.scale = fit * z
+			view.zoom_rung = rnd.zoom_rung_of(z)
+			view.off_x = f32(view.win_w) / 2 - f32(23) * view.tile_px * view.scale
+			view.off_y = f32(view.win_h) / 2 - f32(2) * view.tile_px * view.scale
+			rl.BeginDrawing()
+			rnd.draw_world(&view, &state.topology, &state.bundles, &state.flow, &state.crisis, 120, {}, -1, -1, state.seed)
+			rl.EndDrawing()
+			img := rl.LoadImageFromScreen()
+			normalize(&img)
+			// (a) laneless: zero lane-stripe tokens in the frame
+			n_amber := count_exact(img, LANE_AMBER)
+			check(n_amber == 0, fmt.aprintf("laneless frame (leg %d: no express-stripe amber)", leg), n_amber)
+			// (b) tier hues present (the wide gold wire is long enough to
+			// count even at the fit)
+			n_gold := count_near(img, gold, 30)
+			check(n_gold > 400, fmt.aprintf("tier hue renders (leg %d: gold wide wire)", leg), n_gold)
+			// (c) the covenant width at the scan column: the contiguous run
+			// of steel-family pixels crossing the horizontal standard wire
+			runs, found := measure_color_run(img, steel, int(view.win_w) / 2)
+			check(found, fmt.aprintf("standard stroke present at the scan column (leg %d)", leg), 0)
+			expected := rnd.link_base_world(view.zoom_rung, "standard") * view.scale
+			// tol 1.0 (measured residuals +-0.8): tight enough that a
+			// rung-deaf draw fails — always-ACCESS misses DIST by 1.29px,
+			// always-CORE misses ACCESS by 2.4px (the edge-case-hunter's
+			// overstated-claim fix: tol 2.0 let always-ACCESS pass all legs)
+			check(abs(runs - expected) <= 1.0,
+				fmt.aprintf("stroke width == ladder table (leg %d: measured %.1f px vs table %.1f px)", leg, runs, expected),
+				int(runs * 10))
+			// (d) the covenant at pixels: the measured stroke never exceeds
+			// LINK_RATIO_CAP x the live house footprint (the draw path, not
+			// just the tables)
+			house_px := rnd.sprite_house_target(&view)
+			check(runs <= rnd.LINK_RATIO_CAP*house_px + 1.0,
+				fmt.aprintf("covenant at pixels (leg %d: stroke %.1f <= cap %.1f)", leg, runs, rnd.LINK_RATIO_CAP*house_px),
+				int(runs * 10))
+			// (e) LOOK §1 the toward-space shrink, MEASURED: the house
+			// footprint presence (the washed roof hex) drops monotonically
+			// down the ladder — nothing swaps for a symbol, everything just
+			// gets smaller (a symbol swap or a rung-deaf target fails the
+			// monotone chain or the honesty ratio).
+			roof_counts[leg] = count_near(img, HOUSE_ROOFS[0], 8)
+			rl.UnloadImage(img)
+		}
+		check(roof_counts[0] > 200, "house presence at ACCESS (intimate sprites)", roof_counts[0])
+		check(roof_counts[0] > roof_counts[1] && roof_counts[1] > roof_counts[2],
+			fmt.aprintf("toward-space shrink is monotone (%d > %d > %d)", roof_counts[0], roof_counts[1], roof_counts[2]), roof_counts[2])
+		check(roof_counts[0] >= 5*roof_counts[2],
+			fmt.aprintf("the shrink is HONEST (access %d vs core %d — the ladder factor, not AA noise)", roof_counts[0], roof_counts[2]), roof_counts[0])
+		// (f) LOOK §1 the dusk dial at pixels: the intimate ACCESS diorama is
+		// DARK; the warm settlement dots come on at DISTRIBUTION and burn at
+		// CORE; the DC anchor glows COOL (the predicted canvas blends of the
+		// dial alphas — the dot peeks around the silhouette, the mock's
+		// recipe). A dial flip or a rung-deaf alpha fails the chain.
+		for leg in 0..<3 {
+			fit := rnd.camera_fit(&view)
+			view.scale = fit * zs[leg]
+			view.zoom_rung = rnd.zoom_rung_of(zs[leg])
+			view.off_x = f32(view.win_w) / 2 - f32(23) * view.tile_px * view.scale
+			view.off_y = f32(view.win_h) / 2 - f32(2) * view.tile_px * view.scale
+			rl.BeginDrawing()
+			rnd.draw_world(&view, &state.topology, &state.bundles, &state.flow, &state.crisis, 120, {}, -1, -1, state.seed)
+			rl.EndDrawing()
+			img := rl.LoadImageFromScreen()
+			normalize(&img)
+			n_warm := count_near(img, DUSK_WARM_BLENDS[leg], 3)
+			if leg == 0 {
+				check(n_warm == 0, "the intimate ACCESS diorama is dark (no dusk glow)", n_warm)
+			} else {
+				check(n_warm > 0, fmt.aprintf("dusk lights leg %d (the predicted warm blend)", leg), n_warm)
+			}
+			if leg == 2 {
+				n_dc := count_near(img, DUSK_DC_BLEND_CORE, 4)
+				check(n_dc > 0, "the DC anchor glows COOL at CORE (the predicted blue blend)", n_dc)
+			}
+			rl.UnloadImage(img)
+		}
+		// (g) LOOK §1 state travels up: a CONGESTED building's light shifts
+		// warm-amber (the minimal honest encoder — the node's health level
+		// blends the dot toward the state token; a deleted shift renders the
+		// pure warm blend and fails here).
+		{
+			state.crisis.node_health[0] = pp.Congestion_Level.Amber // the house (slot 0)
+			fit := rnd.camera_fit(&view)
+			view.scale = fit * 1.0
+			view.zoom_rung = .Core
+			view.off_x = f32(view.win_w) / 2 - f32(23) * view.tile_px * view.scale
+			view.off_y = f32(view.win_h) / 2 - f32(2) * view.tile_px * view.scale
+			rl.BeginDrawing()
+			rnd.draw_world(&view, &state.topology, &state.bundles, &state.flow, &state.crisis, 120, {}, -1, -1, state.seed)
+			rl.EndDrawing()
+			img := rl.LoadImageFromScreen()
+			normalize(&img)
+			n_shift := count_near(img, DUSK_AMBER_BLEND_CORE, 4)
+			check(n_shift > 0, "a congested building's light shifts warm-amber (the predicted blend)", n_shift)
+			n_pure := count_near(img, DUSK_WARM_BLENDS[2], 3)
+			check(n_pure == 0, "the shifted light is NOT the pure warm blend (the shift is real)", n_pure)
+			state.crisis.node_health[0] = pp.Congestion_Level.None // restore
+			rl.UnloadImage(img)
+		}
 		pp.run_destroy(&state)
 	}
 
@@ -669,6 +841,7 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 			"tie preview arms the split node (ECMP diamond)", len(prev.split_nodes))
 		// zoom onto the split node + render the REAL glow path on paper canvas
 		view.scale = 3.0
+		view.zoom_rung = .Access // companion for the scale set (z 3.0 is Access; the rung-keyed widths stay coherent)
 		view.off_x = f32(view.win_w) / 2 - f32(4) * view.tile_px * view.scale
 		view.off_y = f32(view.win_h) / 2 - f32(15) * view.tile_px * view.scale
 		rl.BeginDrawing()
@@ -880,11 +1053,11 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 	// A bypass anywhere on the draw path (factor zeroed, predicate always
 	// involved, mix deleted) fails (a) or (c) — the mutation leg proves it.
 	{
-		sv_scale, sv_laned, sv_rm := view.scale, view.lane_detail, view.reduced_motion
+		sv_scale, sv_rung7, sv_rm := view.scale, view.zoom_rung, view.reduced_motion
 		sv_ox, sv_oy := view.off_x, view.off_y
 		defer {
 			view.scale = sv_scale
-			view.lane_detail = sv_laned
+			view.zoom_rung = sv_rung7
 			view.reduced_motion = sv_rm
 			view.off_x = sv_ox
 			view.off_y = sv_oy
@@ -928,7 +1101,7 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		pp.crisis_trigger(&state, 1000, 0, 0, .Saturated_Bundle, state.bundles.pipe_bundle[psa], pp.PORT_DIR_LO_TO_HI, 0, 10)
 		// camera: both pipes on screen, bands wide enough for clean sampling
 		view.scale = 2.0
-		view.lane_detail = false
+		view.zoom_rung = .Access // scale 2.0 absolute over the fit ~0.92 -> z ~2.2 (the ACCESS rung)
 		view.reduced_motion = false
 		view.off_x = f32(view.win_w) / 2 - f32(8) * view.tile_px * view.scale
 		view.off_y = f32(view.win_h) / 2 - f32(18) * view.tile_px * view.scale
@@ -1103,35 +1276,29 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 			view.map_source = u8(pp.Map_Source.Dublin)
 			view.board = bd
 			rnd.dublin_render_ensure(&view)
-			// The EMPIRICAL composites (measured on this renderer, then
-			// pinned): rlsw renders the block's DrawTriangle fill OPAQUE —
-			// the fam token's alpha byte (204) is inert on this surface, so
-			// the recede's RGB MIX carries the whole effect: the involved
-			// block reads the PURE family RGB; the receded block reads the
-			// crisis_recede mix (fam*0.35 + canvas*0.65, u8-truncated —
-			// ±1 in g/b from the f32 mix, tolerance 6). The frontage edge
-			// line (a=90, blended) lands near the receded mix too — hence
-			// the generous window + the exact-one-side-zero shape.
+			// LOOK §4 re-pin: REAL SPRITES render on the Dublin board (the
+			// street-aligned block path retired). The scan targets the
+			// MEASURED washed-sprite body composites on this fixture (c0 =
+			// house_0 coral under the family wash, c2 = house_2 sage under
+			// its receded wash — the §7 fixture's id%4 variants). The recede
+			// twin retires with the blocks (the recede mechanism is
+			// map-agnostic, pinned on the procedural legs above; the Dublin
+			// wash STRENGTH is unit-pinned in look_l4_test).
 			paper := rl.Color{237, 226, 200, 255}
-			fam := view.palette.residential_family
-			raw_blk := rl.Color{fam.r, fam.g, fam.b, 255}
-			rec_blk := rnd.crisis_recede(&view, 1.0, fam)
+			washed_coral := rl.Color{204, 83, 74, 255} // c0: house_0 body under the wash (measured 302 px)
+			washed_sage := rl.Color{107, 189, 105, 255} // c2: house_2 body under the receded wash (measured 238 px)
 			rl.BeginDrawing()
 			rl.ClearBackground(paper)
 			rnd.draw_nodes(&view, &state.topology, &state.crisis, 1100, 1.0)
 			rl.EndDrawing()
 			img := rl.LoadImageFromScreen()
 			normalize(&img)
-			// generous windows (the street-aligned block sits within ~20px of
-			// the node center; the chip glyph rides ~29px ABOVE it — the up
-			// window covers both; the wide probe measured 113 px per
-			// composite on exactly this fixture, interior-only ≈ 41)
-			n_blk_inv := scan_box(img, int(c0.x), int(c0.y), 20, 32, 18, raw_blk, 6)
-			n_blk_non_raw := scan_box(img, int(c2.x), int(c2.y), 20, 32, 18, raw_blk, 6)
-			n_blk_non_rec := scan_box(img, int(c2.x), int(c2.y), 20, 32, 18, rec_blk, 6)
-			check(n_blk_inv >= 60, fmt.aprintf("dublin: involved block keeps the raw family fill (%d px)", n_blk_inv), n_blk_inv)
-			check(n_blk_non_rec >= 60 && n_blk_non_raw == 0,
-				fmt.aprintf("dublin: non-involved block recedes (receded %d / raw %d px — deleting the block recede renders raw and fails here)", n_blk_non_rec, n_blk_non_raw), n_blk_non_rec)
+			// tight sprite-body windows (the node center +-10px; the chip
+			// rides ~29px ABOVE and is excluded on purpose)
+			n_spr_inv := scan_box(img, int(c0.x), int(c0.y), 10, 10, 10, washed_coral, 6)
+			n_spr_non := scan_box(img, int(c2.x), int(c2.y), 10, 10, 10, washed_sage, 6)
+			check(n_spr_inv >= 100, fmt.aprintf("dublin: the involved terminal renders as a SPRITE (washed coral %d px)", n_spr_inv), n_spr_inv)
+			check(n_spr_non >= 100, fmt.aprintf("dublin: the non-involved terminal renders as a SPRITE (washed sage %d px)", n_spr_non), n_spr_non)
 			rl.UnloadImage(img)
 			view.map_source = sv_ms
 			view.board = sv_bd
diff --git a/harness/run.odin b/harness/run.odin
index 8beb46f..ad2ed91 100644
--- a/harness/run.odin
+++ b/harness/run.odin
@@ -314,6 +314,24 @@ run_demo :: proc(name: string, save: bool, cat: ^pp.Catalogs, rc: ^Render_Ctx, s
 	// previous demo must never announce a spawn in this one).
 	rnd.spawn_fx_reset(&rc.view.spawn_fx)
 
+	// LOOK §1: the demo's pinned capture altitude (view-only run setup —
+	// the a11y/map precedent: T1 + replay never see a byte). Reset to the
+	// fit (undoing the previous demo's zoom), then derive the transform +
+	// the ladder rung from THIS demo's directive. zoom 1.0 (absent) = the
+	// fit view — the same transform every legacy demo captured.
+	rnd.view_refit(&rc.view)
+	zoom := demo.zoom
+	if zoom < 1.0 { // the absent-directive zero value normalizes to the fit
+		zoom = 1.0
+	}
+	rc.view.zoom_rung = rnd.zoom_rung_of(zoom)
+	if zoom != 1.0 {
+		fit := rnd.camera_fit(&rc.view)
+		rc.view.scale = fit * zoom
+		rc.view.off_x = (f32(rc.view.play_w) - rc.view.world_w * rc.view.scale) / 2
+		rc.view.off_y = (f32(rc.view.win_h) - rc.view.world_h * rc.view.scale) / 2
+	}
+
 	state: pp.Run_State
 	defer pp.run_destroy(&state)
 	pp.run_init(&state, demo.seed, cat.hash, cat.balance.logic_hz)

--- SPEC / CONTEXT ---

## Spec file 1: the PR body (the claims under review)
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



## Spec file 2: the job briefing (the L1-L4 design-lock contracts)
# Briefing — packet-plumber-v2-look-zoom-language (LOOK implementation, ruled half)

Skill to execute: **bmad-quick-dev** (implementation; step-04 review layers
MANDATORY). THE SPEC IS LAW — read FIRST, cite section numbers in every
story, never re-open a ruled fork:

`_bmad-output/implementation-artifacts/look-node-legibility/LOOK-SPEC.md`
(DESIGN LOCKS = `[ADOPTED 2026-08-26 user ruling]`; companion evidence in
the same dir + `link-vocab-redesign/HANDOFF.md`).

## Repo / workspace facts

- Repo: `/Users/moses/code/packet-plumber` (Odin `dev-2026-08` + raylib 6.0).
- Base: **v2** (head resolved by Silas at release — this job is SERIALIZED
  behind arch-egress-migration; shared render surface + the D7 reads
  contract it ships). Worktree on branch
  `packet-plumber-v2-look-zoom-language`; main checkout untouched.
- Read `project-context.md` + the [LOOK] canon first. Field notes: the
  tie-deconflect set (mutation-leg/palcheck craft), 4.2-surge-crisis.

## SCOPE FENCE (the pause-and-spec ruling)

- **IN:** the DESIGN LOCKS only — §1 zoom ladder, §2 camera, §3 scale
  covenant + laneless links, §4 node ladder (ruled rows only).
- **OUT (parked forks — NO work, not even preliminary):** link finish
  fork 1b's B/C variants beyond the switch (below), router queue encoder,
  tier-ring final spec beyond the mocked floor, quiet-board PRODUCTION
  swap (the candidate stays staged; current board ships), packet shapes,
  HUD occlusion, the state-up-ladder encoder's final form (ship the
  minimal honest version the spec names: congested estate lights shift
  warm-amber; tune at the gate).

## The law you implement (story ladder — one commit per story, green between)

1. **L1 — scale covenant + laneless links (§3, the root complaint):**
   links NEVER exceed ~⅓–½ node size at any tier (measure + pin: a
   width/node-size ratio test at every rung); strip the 3-lane strokes —
   single solid stroke, TIER HUE mandatory (copper/steel/gold family,
   CVD-verified per spec). Finish fork 1b is OPEN: ship finish **A**
   (solid tier-colored stroke — Sally's rec) behind a compile-time
   constant (`LINK_FINISH :: .A_SOLID`) so the future ruling flips ONE
   constant, never a rewrite (the wire-aesthetics byte-cheap-reversal
   doctrine; flags-off/current-golden equivalence proofs per story).
2. **L2 — the zoom ladder (§1):** toward-space shrink ONLY (no symbol
   swaps, no halos/circles); DISTRIBUTION ≈0.62 buildings + dusk lights
   dial (small, dim, glow intensity a tunable constant); CORE ≈0.42 warm
   flecks + glow dots (city-lights-from-orbit), DC cool blue, links stay
   the visible skeleton at min stroke weight. Stepped tables, no
   transcendentals; state travels up (minimal warm-amber shift per spec).
3. **L3 — camera auto-breath (§2):** pullback keyed to the estate-seed
   event (growth canon already emits it); wheel ALWAYS overrides; breath
   resumes only on next seed; boot lands INTIMATE. Extends the shipped
   zoom-tier machinery — view-layer only. Reduced-motion PINS the breath
   (7.3/E9.2 doctrine) and the light animations.
4. **L4 — node ladder (§4 ruled rows):** building scale ladder (home 1.00
   · biz 1.10 · campus 1.22 · DC 1.35 @ ACCESS; puck 1.05), REAL Blender
   sprites only, family wash ≈55% lighter than Dublin fill; router tier
   rings get the ≈2px SCREEN-SPACE stroke floor (token hues unchanged) —
   the spec's D1 bump, confirming the earlier-session carry at the gate.

## Testing standard (the house bar)

- **Mutation leg per story** (RED-then-GREEN in the report): L1 ratio-law
  break + lane-stripe reintroduction must FAIL (palcheck live-render, the
  tie-deconflect craft); L2 rung scales (measure pixels per rung); L3
  breath (seed event → pullback asserted; wheel-override asserted); L4
  ladder ratios + ring floor.
- T2 goldens: heavy deliberate churn — re-bless per story with the
  rung-by-rung inventory in the PR body; L1 must prove flags-off
  equivalence where the switch allows it.
- Full suite green per story: core, app, app/render, palcheck. Remote CI
  billing-block = note once (local ground truth).

## PR / ledger

- ONE PR to v2, title `look(zoom-language): the ruled half — scale
  covenant, laneless links, toward-space ladder, breathing camera`.
- Body: story ladder, spec section citations, mutation proofs, golden
  re-bless inventory, parked-fork fence statement.
- `ledger set packet-plumber-v2-look-zoom-language in-review "<url>"` THEN
  `ledger pr ...` (both steps). Perkins r1 via sensor at stable head.

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider), `--thinking max`.
- Mega-minions: pin explicitly.

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: look-zoom-language
- base: v2 (head at release)
- branch: packet-plumber-v2-look-zoom-language
- model: zai-coding-cn/glm-5.3
- pr_review: 1 (the [LOOK] canon surface — full Perkins)
- blocked_by: packet-plumber-v2-arch-egress-migration (release = its merge
  close-out + fresh head)


## Spec file 3: LOOK-SPEC.md (the user-ratified design language — the spec these locks implement)
# LOOK SPEC — the Packet Plumber zoom-language revamp (ruled half)

Author: Sally (bmad-agent-ux-designer), interactive session 2026-08-26 with Moses.
Status: **the ruled sections are DESIGN LOCKS** (`[ADOPTED 2026-08-26 user ruling]`);
the open forks are listed for the next session. Companion evidence:
`measurements_*.json`, `kyle-findings.md`, `report.html`, `zoom-ladder.html`,
`direction-ruling.md` (earlier MM-STYLE ruling — folded below), and the sibling
`link-vocab-redesign/HANDOFF.md` (encoding inventory + CVD record).

North star (user): *"the zoomed-out look AND the zoomed-in look must both be
aesthetically pleasing — colorful, pull your attention"* — the streamer-thumbnail
test. Mini Metro / Mini Motorways are the reference family.

---

## 1 · THE ZOOM LADDER (all three rungs RULED)

**One metaphor, boot to thumbnail: toward space.** Nothing ever swaps for a
symbol; everything just gets smaller; the links stay visible at every
altitude; dusk lights come on progressively as you pull away. No halos, no
circles, no diagrammatic replacement (circles explicitly rejected — "ugly,
don't fit in").

| Rung | Name | What the player sees | Ruling |
|---|---|---|---|
| 🔍 | **ACCESS** (intimate start) | Real building sprites + router pucks at ONE honest scale (building ≈ basic puck ≈ 1.05 tiles); thin solid links; the game opens here — a tidy diorama; first nodes pleasing to the eye | ✅ landed (mock verified: "intimate and tidy") |
| 🌆 | **DISTRIBUTION** (mid) | Buildings just smaller (≈0.62 tiles in mock), crisp; dusk lights beginning under settlements (small, dim); links + routers carry structure; NO estate halos | ✅ [ADOPTED] "2 — pure shrink, lights coming on" |
| 🌐 | **CORE** (far / thumbnail) | Altitude shrink: houses ≈0.42 tiles = tiny warm flecks, each with a warm glow dot (city-lights-from-orbit); DC a cool blue glow; links stay visible as the skeleton (min stroke weight); router pucks small but solid | ✅ [ADOPTED] "2 — shrink + dusk glow" |

- **Glow is a dial, not a switch** — intensity tunable at implementation.
- **Estate grouping at mid/far comes from REAL adjacency** (estates are the
  spawn canon: `growth_groups` clusters 3–5, then new areas seed) + the light
  pattern — never from drawn blobs.
- **State travels up the ladder**: congestion/health must read at every
  altitude (a congested estate's lights shift warm-amber; the exact encoder is
  OPEN, §4).

## 2 · THE CAMERA (RULED)

- **The map breathes out on its own** as new areas seed (auto-pullback keyed
  to the estate-seed event — the growth canon already emits it). The player's
  wheel ALWAYS overrides (grab-back honored); the auto-breath resumes only on
  the next seed event. Boot lands INTIMATE (access view), not the fit.
  ✅ [ADOPTED] — extends the shipped pullback/zoom-tier machinery
  (`DEFAULT_ZOOM` doctrine; camera work is view-layer only).

## 3 · THE SCALE COVENANT + LINK LANGUAGE (scale law RULED; finish OPEN)

- **One ratio law at every tier: links never exceed ~⅓–½ of node size**
  (the MM observation, measured in their frames; PP today breaks it at
  56–67% — the root complaint). Mocked ladder honors it end to end.
  ✅ (MM-STYLE, ruled earlier)
- **Links are single solid laneless strokes** — no lane stripes in the world
  (queues are ingress/egress on ROUTERS, user ruling; the road doesn't
  gossip). Tier hue stays mandatory at a glance (copper/steel/gold family).
  ✅ (Fork-1 direction, ruled in the sibling session)
- **OPEN — Fork 1b, the finish:** (A) solid tier-colored stroke vs (B) neutral
  asphalt band + dashed tier marking vs (C) asphalt + solid marking. Mocked in
  `link-vocab-redesign/strips/fork1b-*.png`; CVD-verified; NOT yet ruled.

## 4 · THE NODES (scale ladder RULED; encoders OPEN)

- **Building scale ladder (real assets):** home 1.00 · biz 1.10 · campus 1.22
  · DC 1.35 tiles at ACCESS (puck = 1.05); shrink honestly from there.
  Real Blender-sculpted sprites only — no primitive blocks (user: "we have
  real assets"). Family wash ≈55% lighter than the Dublin fill so the
  sculpting reads. ✅ (ruled with MM-STYLE)
- **Router tier rings:** minimum screen-space stroke (≈2px floor) — the
  mock's D1 bump; token hues unchanged. Carried from the earlier session;
  confirm at implementation gate.
- **OPEN — router queue encoder** (r1 port ticks / r2 rim arcs / r3 doorstep
  chip — all mocked in `link-vocab-redesign`, KYLE-checked; reads were mocked
  over d1 strokes and should be re-judged on the final road).
- **OPEN — tier-ring final spec** (stroke factor 0.055→0.06+floor mocked).

## 5 · THE BOARD (asset candidate BUILT; production ruling OPEN)

- **The quiet board:** the Dublin geometry regenerated WITHOUT roads — paper,
  water, coast, parks only (real Blender render, paper palette, flat
  emission, top-down ortho 2080×1560). On the record page (§4) and on disk:
  `strips/quiet_board.png`; generator `.scratch/quiet_board_build.py` (Blender
  MCP executed). **The network owns the ink.** User leans yes ("the map for
  Dublin looks noisy with the roads… I'm thinking we might need a new asset
  in Blender without the roads") — formal ruling pending next session.
- Estate "clearings" (subtle ground treatment under clusters) — optional
  accent, not ruled.

## 6 · THE PACKETS (OPEN)

9-class shape vocabulary + 5 CVD-anchor colors — fully specced and CVD-verified
in `link-vocab-redesign/HANDOFF.md` §4 F7/F8. Not yet ruled; next session.

## 7 · HUD / FRAME (findings carried, not yet designed)

- Weather panel can sit ON a router at focus zoom; health card can cover
  map-top nodes (measured finding S7). The revamp's frame pass (quieter
  chrome, occlusion rules) is queued.

## 8 · CRAFT CONTRACTS (standing — apply to whatever ships)

From `link-vocab-redesign/HANDOFF.md` §8, still binding: §10.4 no
transcendentals (pinned tables; dash patterns are integer math);
deterministic/golden-stable (pure function of tick+state); reduced-motion
inert; never color alone (shape/position/width redundancies); quiet-at-rest;
byte-identical flags-off until the deliberate re-bless. **All LOD/camera/glow
work is [LOOK]-layer only — the sim (ODN-3, per-(bundle,lane) queues,
FORGE #4) is untouched; queue state MOVES to router surfaces, never
recomputed.** Implementation heists serialize behind crisis-duck (shared
render surface); `pr_review=1`; goldens re-blessed deliberately.

## 9 · SIM UNTOUCHED — the boundary (verbatim from the handoff)

SIM UNTOUCHED — ODN-3, per-(bundle,lane) queues, FORGE #4: all stand. This is
the [LOOK] layer ONLY. If a future gate wants the sim migrated too, that
ESCALATES as its own architecture job — never silently.

---

### Artifact index (this directory unless noted)
- `zoom-ladder.html` + `strips/ladder_final_ruled.png` — the ruled ladder, visual record
- `strips/quiet_board.png` — the no-roads board candidate (Blender, real)
- `storyboard.py`, `.scratch/quiet_board_build.py` — generators (scratch, never committed)
- `design-log.md` — every [ADOPTED] ruling, in order, verbatim
- Sibling: `../link-vocab-redesign/` (HANDOFF.md, encoding-table.md, captures, strips)

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT CONTRACT (your deliverable) ---

When your analysis is complete, IMMEDIATELY write your final JSON array — and nothing else — to this exact path:

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-look-zoom-language/r1/edge.json

The FILE is the deliverable, not your final chat message. Write the file NOW, compactly, without re-reading your work. A valid empty answer is the two-byte file: []
