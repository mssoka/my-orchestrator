You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your working directory IS the reviewed worktree (a detached checkout at the reviewed state) — read files here. You are a reviewer: do NOT modify, create (except your one output JSON), or fix anything in the repository.

--- PROJECT CONVENTIONS ---
none

--- DIFF ---
diff --git a/_bmad-output/implementation-artifacts/deferred-work.md b/_bmad-output/implementation-artifacts/deferred-work.md
index 0eee7d9..13f6362 100644
--- a/_bmad-output/implementation-artifacts/deferred-work.md
+++ b/_bmad-output/implementation-artifacts/deferred-work.md
@@ -1,5 +1,8 @@
 # Deferred work
 
+- source_spec: `packet-plumber-v2-congestion-read-a1` (viscomm-audit A1, doc-hygiene defer)
+  summary: add the A1 amendment line ("congested emphasis layer ≠ covenant change") to look-node-legibility/LOOK-SPEC.md when that file lands in git — it is untracked in the main checkout today, so the amendment lives in the tracked LOOK §3 canon comment (view.odin) and the PR body.
+  evidence: adversarial r1 finding 10; the untracked spec surface disagrees by silence until the line is mirrored into the ruled doc.
 - source_spec: `_bmad-output/implementation-artifacts/spec-3-2-lane-qos.md`
   summary: draw_bundles rescans every pipe for every bundle per frame (O(bundles × pipes)) to sum lane caps + detect non-default emphasis
   evidence: review finding (Blind Hunter #5, low) — fine at demo/game scale today (dozens of bundles × hundreds of pipes ≈ tens of thousands of float compares/frame); the derived-bundles view already walks members once per gen change, so folding the caps sum + a non-default flag into Bundles at bundles_rebuild is the natural future fix when the render cost ever matters.
diff --git a/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z1.0.png b/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z1.0.png
new file mode 100644
index 0000000..59f9b94
Binary files /dev/null and b/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z1.0.png differ
diff --git a/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z1.4.png b/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z1.4.png
new file mode 100644
index 0000000..e6bf081
Binary files /dev/null and b/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z1.4.png differ
diff --git a/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z2.0.png b/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z2.0.png
new file mode 100644
index 0000000..9556a35
Binary files /dev/null and b/_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z2.0.png differ
diff --git a/app/render/look_l1_test.odin b/app/render/look_l1_test.odin
index 38f22b3..8751354 100644
--- a/app/render/look_l1_test.odin
+++ b/app/render/look_l1_test.odin
@@ -249,6 +249,27 @@ single_strokes_sit_in_the_covenant_band :: proc(t: ^testing.T) {
 	}
 }
 
+// --- the congested-link pulse (A1 as amended, 2026-08-28 user ruling) --------
+
+@(test)
+congestion_pulse_law_is_the_ruled_envelope :: proc(t: ^testing.T) {
+	// A1 as amended: sizes stay exactly as v2 (no floor, no bump — the width
+	// line in draw_bundles is the untouched v2 law); the READ is a pure
+	// pulse. The pins: the trough IS the classic 4.1 blend share (byte-exact
+	// v2 color at the pulse floor), the peak clears it by a clearly visible
+	// swing, and the reduced-motion seam pins the share at the PEAK (the
+	// most legible static reading — the pulse_read convention).
+	expect_f32(t, CONGESTION_PULSE_TROUGH_SHARE, 0.43)
+	testing.expect(t, CONGESTION_PULSE_PEAK_SHARE > CONGESTION_PULSE_TROUGH_SHARE + 0.2,
+		"the pulse swing is too shallow to read (peak must clear the trough by > 0.2 of state share)")
+	testing.expect(t, CONGESTION_PULSE_PEAK_SHARE <= 1.0, "the peak share exceeds full state color")
+	v: View
+	v.reduced_motion = false
+	expect_f32(t, congestion_pulse_share(&v, 8, 0), CONGESTION_PULSE_PEAK_SHARE) // PULSE16[8] == 1.0
+	v.reduced_motion = true // the a11y pin: the envelope freezes at the peak
+	expect_f32(t, congestion_pulse_share(&v, 0, 0), CONGESTION_PULSE_PEAK_SHARE)
+}
+
 // --- helpers -------------------------------------------------------------------
 
 // look_l1_set_puck_bboxes — hand-set the puck content widths (the sprite
diff --git a/app/render/view.odin b/app/render/view.odin
index 0d76aa5..526a6b7 100644
--- a/app/render/view.odin
+++ b/app/render/view.odin
@@ -538,7 +538,7 @@ draw_world :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp
 	// per frame from the serialized crisis rows + the tick (the pure seam in
 	// crisis.odin — the harness renders it from sim state alone, no feeding).
 	desat_f := crisis_desat_factor(v, crisis, tick)
-	draw_bundles(v, topo, bundles, flow, crisis, desat_f, paths[:])
+	draw_bundles(v, topo, bundles, flow, crisis, desat_f, paths[:], tick)
 	// v2-spawn-feel: the PLACEMENT feedback — the pulse band over the pipes
 	// near a just-landed terminal (after the pipes, before the nodes — the
 	// highlight reads as "this node just joined the network").
@@ -661,6 +661,11 @@ fceil :: proc(f: f32) -> i32 {
 
 // --- LOOK §3: the scale covenant + the laneless link language (ruled) ----
 //
+// [AMENDED 2026-08-28, viscomm-audit A1 user ruling as amended] congested
+// PULSE emphasis, sizes unchanged — the congested halo's intensity
+// oscillates (pure pulse); link sizes stay exactly as v2 has them; the
+// covenant is untouched and calm boards stay byte-identical.
+//
 // [ADOPTED 2026-08-26 user ruling] Links are SINGLE SOLID LANELESS strokes
 // (the 3.3 spatial-lane stripes are superseded — queues are ingress/egress
 // on ROUTERS, the road doesn't gossip), and ONE ratio law holds at every
@@ -699,6 +704,42 @@ LINK_RATIO_CAP :: f32(0.5)
 // nodes before the covenant clamp even engages).
 LINK_EXTRA_W :: [3]f32{2.0, 1.5, 1.25} // [Access, Distribution, Core]
 
+// CONGESTION_PULSE_TROUGH_SHARE / CONGESTION_PULSE_PEAK_SHARE — the
+// congested-link pulse law (viscomm-audit R1, AMENDED by user ruling
+// 2026-08-28, refined to GLOW ONLY — option A of glow/stroke/both):
+// link SIZES stay exactly as v2 has them (no width bump, no floor, no
+// width oscillation — geometry never moves); the READ is a pure pulse in
+// the telegraph layer's BRIGHTNESS: the halo margin's state-color SHARE
+// oscillates between the classic 4.1 resting blend and the peak share,
+// while the stroke core keeps the STEADY classic recolor (the split
+// render: pulsing glow pass, steady core pass over it). The envelope
+// rides the house pulse_read seam (16-tick cycle at 1.25 Hz, per-bundle
+// phase; reduced-motion pins to the PEAK — the most legible static
+// reading, the a11y convention). The covenant (LINK_RATIO_CAP) and the
+// calm board are untouched: the pulse exists only when lvl != .None.
+CONGESTION_PULSE_TROUGH_SHARE :: f32(0.43)
+CONGESTION_PULSE_PEAK_SHARE :: f32(0.75)
+
+// congestion_pulse_share — the pulse envelope for one bundle this tick
+// (ONE derivation for both draw_bundles branches — a restated copy drifts
+// the look between the blessed inline path and the routed variant).
+congestion_pulse_share :: proc(v: ^View, tick: u64, bi: u32) -> f32 {
+	return CONGESTION_PULSE_TROUGH_SHARE +
+		(CONGESTION_PULSE_PEAK_SHARE - CONGESTION_PULSE_TROUGH_SHARE) * pulse_read(v, tick, bi, 1)
+}
+
+// congested_halo_blend — the congested halo's color at a state share:
+// raw tier color pulled `share` of the way to the state token (the 4.1
+// recolor math generalized from the fixed 0.43 to the pulsing share).
+congested_halo_blend :: proc(raw, state_col: rl.Color, share: f32) -> rl.Color {
+	return rl.Color{
+		u8(f32(raw.r) * (1.0 - share) + f32(state_col.r) * share),
+		u8(f32(raw.g) * (1.0 - share) + f32(state_col.g) * share),
+		u8(f32(raw.b) * (1.0 - share) + f32(state_col.b) * share),
+		255,
+	}
+}
+
 // link_base_world — the single-stroke base width for (rung, tier id)
 // (world px; tier id keyed, catalog-order-immune). ACCESS/DISTRIBUTION are
 // uniform across tiers (hue carries the tier — the ruled mock); CORE
@@ -934,7 +975,7 @@ bundle_congestion_level :: proc(topo: ^pp.Topology, bundles: ^pp.Bundles, crisis
 	return .None
 }
 
-draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, desat: f32, paths: []Wire_Path) {
+draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, desat: f32, paths: []Wire_Path, tick: u64) {
 	p := v.palette
 	for bi in 0..<int(bundles.n) {
 		lo, hi := bundles.bundle_lo[bi], bundles.bundle_hi[bi]
@@ -988,23 +1029,29 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 				rl.DrawCircleV(a, band * 0.5, col)
 				rl.DrawCircleV(b, band * 0.5, col)
 			}
-			// 4.1 pipe-congestion halo (pre-7.5 inline)
+			// 4.1 pipe-congestion halo (pre-7.5 inline) — AMENDED 2026-08-28,
+			// refined to GLOW ONLY: the halo margin's brightness PULSES while
+			// the stroke core keeps the STEADY classic recolor — geometry never
+			// moves (both passes constant v2 widths; the width line is the
+			// untouched v2 law). Phase seeded by bundle id so sibling links do
+			// not pulse in lockstep. Draw order: glow pass first, the steady
+			// core over it.
 			lvl := bundle_congestion_level(topo, bundles, crisis, u32(bi))
 			if lvl != .None {
 				halo := p.state_congested
 				if lvl == .Red {
 					halo = p.state_critical
 				}
-				halo = rl.Color{
-					u8(f32(raw.r) * 0.57 + f32(halo.r) * 0.43),
-					u8(f32(raw.g) * 0.57 + f32(halo.g) * 0.43),
-					u8(f32(raw.b) * 0.57 + f32(halo.b) * 0.43),
-					255,
-				}
+				share := congestion_pulse_share(v, tick, u32(bi))
 				w := band + 5.0 * v.scale
-				rl.DrawLineEx(a, b, w, halo)
-				rl.DrawCircleV(a, w * 0.5, halo)
-				rl.DrawCircleV(b, w * 0.5, halo)
+				glow := congested_halo_blend(raw, halo, share)
+				rl.DrawLineEx(a, b, w, glow)
+				rl.DrawCircleV(a, w * 0.5, glow)
+				rl.DrawCircleV(b, w * 0.5, glow)
+				core := congested_halo_blend(raw, halo, CONGESTION_PULSE_TROUGH_SHARE)
+				rl.DrawLineEx(a, b, band, core)
+				rl.DrawCircleV(a, band * 0.5, core)
+				rl.DrawCircleV(b, band * 0.5, core)
 			}
 			continue
 		}
@@ -1065,21 +1112,22 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 			}
 		}
 
-		// 4.1 pipe-congestion halo (the routed/anchor variant follows the path)
+		// 4.1 pipe-congestion halo (the routed/anchor variant follows the
+		// path) — AMENDED 2026-08-28, refined to GLOW ONLY: the SAME split as
+		// the inline branch (pulsing glow pass + steady classic core; ONE
+		// derivation — the two branches must stay one look).
 		lvl := bundle_congestion_level(topo, bundles, crisis, u32(bi))
 		if lvl != .None {
 			halo := p.state_congested
 			if lvl == .Red {
 				halo = p.state_critical
 			}
-			halo = rl.Color{
-				u8(f32(raw.r) * 0.57 + f32(halo.r) * 0.43),
-				u8(f32(raw.g) * 0.57 + f32(halo.g) * 0.43),
-				u8(f32(raw.b) * 0.57 + f32(halo.b) * 0.43),
-				255,
-			}
+			share := congestion_pulse_share(v, tick, u32(bi))
 			w := band + 5.0 * v.scale
-			draw_path_band(v, &path, w, halo)
+			glow := congested_halo_blend(raw, halo, share)
+			draw_path_band(v, &path, w, glow)
+			core := congested_halo_blend(raw, halo, CONGESTION_PULSE_TROUGH_SHARE)
+			draw_path_band(v, &path, band, core)
 		}
 	}
 }
diff --git a/goldens/a11y_deutan/30000ms.png b/goldens/a11y_deutan/30000ms.png
index 2ac079e..dfe11b3 100644
Binary files a/goldens/a11y_deutan/30000ms.png and b/goldens/a11y_deutan/30000ms.png differ
diff --git a/goldens/a11y_deutan/65000ms.png b/goldens/a11y_deutan/65000ms.png
index 0af03fc..30edffb 100644
Binary files a/goldens/a11y_deutan/65000ms.png and b/goldens/a11y_deutan/65000ms.png differ
diff --git a/goldens/a11y_protan/30000ms.png b/goldens/a11y_protan/30000ms.png
index 2ac079e..dfe11b3 100644
Binary files a/goldens/a11y_protan/30000ms.png and b/goldens/a11y_protan/30000ms.png differ
diff --git a/goldens/a11y_protan/65000ms.png b/goldens/a11y_protan/65000ms.png
index 0af03fc..30edffb 100644
Binary files a/goldens/a11y_protan/65000ms.png and b/goldens/a11y_protan/65000ms.png differ
diff --git a/goldens/a11y_reduced/30000ms.png b/goldens/a11y_reduced/30000ms.png
index 284328f..0b22338 100644
Binary files a/goldens/a11y_reduced/30000ms.png and b/goldens/a11y_reduced/30000ms.png differ
diff --git a/goldens/a11y_reduced/65000ms.png b/goldens/a11y_reduced/65000ms.png
index a88e327..5c3475c 100644
Binary files a/goldens/a11y_reduced/65000ms.png and b/goldens/a11y_reduced/65000ms.png differ
diff --git a/goldens/a11y_scale/30000ms.png b/goldens/a11y_scale/30000ms.png
index 3b66fb0..11d7a66 100644
Binary files a/goldens/a11y_scale/30000ms.png and b/goldens/a11y_scale/30000ms.png differ
diff --git a/goldens/a11y_scale/65000ms.png b/goldens/a11y_scale/65000ms.png
index 590a856..9f440ca 100644
Binary files a/goldens/a11y_scale/65000ms.png and b/goldens/a11y_scale/65000ms.png differ
diff --git a/goldens/a11y_tritan/30000ms.png b/goldens/a11y_tritan/30000ms.png
index ee7e9d0..bd6872c 100644
Binary files a/goldens/a11y_tritan/30000ms.png and b/goldens/a11y_tritan/30000ms.png differ
diff --git a/goldens/a11y_tritan/65000ms.png b/goldens/a11y_tritan/65000ms.png
index 9a51dbd..d490f6f 100644
Binary files a/goldens/a11y_tritan/65000ms.png and b/goldens/a11y_tritan/65000ms.png differ
diff --git a/goldens/advance_block_sla/15000ms.png b/goldens/advance_block_sla/15000ms.png
index 6fcd680..4dc6a5c 100644
Binary files a/goldens/advance_block_sla/15000ms.png and b/goldens/advance_block_sla/15000ms.png differ
diff --git a/goldens/advance_block_sla/60000ms.png b/goldens/advance_block_sla/60000ms.png
index 4c797ae..a65fae8 100644
Binary files a/goldens/advance_block_sla/60000ms.png and b/goldens/advance_block_sla/60000ms.png differ
diff --git a/goldens/health_lose/21000ms.png b/goldens/health_lose/21000ms.png
index cdb2256..a771b13 100644
Binary files a/goldens/health_lose/21000ms.png and b/goldens/health_lose/21000ms.png differ
diff --git a/goldens/health_lose/23000ms.png b/goldens/health_lose/23000ms.png
index d2045b9..a02edc0 100644
Binary files a/goldens/health_lose/23000ms.png and b/goldens/health_lose/23000ms.png differ
diff --git a/goldens/juice/30000ms.png b/goldens/juice/30000ms.png
index 284328f..7f5415b 100644
Binary files a/goldens/juice/30000ms.png and b/goldens/juice/30000ms.png differ
diff --git a/goldens/juice/65000ms.png b/goldens/juice/65000ms.png
index 4ff330f..c5c6109 100644
Binary files a/goldens/juice/65000ms.png and b/goldens/juice/65000ms.png differ
diff --git a/goldens/qos_contention/01000ms.png b/goldens/qos_contention/01000ms.png
index 9751419..b6bb1e3 100644
Binary files a/goldens/qos_contention/01000ms.png and b/goldens/qos_contention/01000ms.png differ
diff --git a/goldens/qos_contention/03000ms.png b/goldens/qos_contention/03000ms.png
index 3c9dd36..71c5709 100644
Binary files a/goldens/qos_contention/03000ms.png and b/goldens/qos_contention/03000ms.png differ
diff --git a/goldens/qos_contention/10000ms.png b/goldens/qos_contention/10000ms.png
index f36d31c..b7f18f5 100644
Binary files a/goldens/qos_contention/10000ms.png and b/goldens/qos_contention/10000ms.png differ
diff --git a/goldens/qos_emphasis/12000ms.png b/goldens/qos_emphasis/12000ms.png
index 12ab5d9..7e30e7e 100644
Binary files a/goldens/qos_emphasis/12000ms.png and b/goldens/qos_emphasis/12000ms.png differ
diff --git a/goldens/sla/01000ms.png b/goldens/sla/01000ms.png
index 55cc846..65ad6a1 100644
Binary files a/goldens/sla/01000ms.png and b/goldens/sla/01000ms.png differ
diff --git a/goldens/sla/04000ms.png b/goldens/sla/04000ms.png
index 81e1e28..addfecd 100644
Binary files a/goldens/sla/04000ms.png and b/goldens/sla/04000ms.png differ
diff --git a/goldens/sla/10000ms.png b/goldens/sla/10000ms.png
index 2438b35..8f546d5 100644
Binary files a/goldens/sla/10000ms.png and b/goldens/sla/10000ms.png differ
diff --git a/goldens/surge/30000ms.png b/goldens/surge/30000ms.png
index 42790c7..a8e0490 100644
Binary files a/goldens/surge/30000ms.png and b/goldens/surge/30000ms.png differ
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
index 3a0a706..13ca8d7 100644
Binary files a/goldens/terminal_types/05000ms.png and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
index 8b762d0..f342a7e 100644
Binary files a/goldens/terminal_types/30000ms.png and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/warn/45000ms.png b/goldens/warn/45000ms.png
index 6a0bda7..5a46742 100644
Binary files a/goldens/warn/45000ms.png and b/goldens/warn/45000ms.png differ
diff --git a/harness/goldens.odin b/harness/goldens.odin
index 1410cd3..2b8ea4b 100644
--- a/harness/goldens.odin
+++ b/harness/goldens.odin
@@ -98,6 +98,27 @@ render_setup :: proc(rc: ^Render_Ctx, cat: ^pp.Catalogs) {
 
 // --- T2 capture -----------------------------------------------------------------
 
+// apply_capture_zoom — the LOOK §1 capture-altitude transform, ONE
+// derivation for every capture path (run's demo `zoom` directive and
+// motion-strip's `zoom=<f>` evidence override share this; a restated copy
+// drifts a rung). zoom < 1.0 normalizes to the fit (the absent-directive
+// zero value). VIEW-ONLY run setup (the a11y/map precedent): the sim, the
+// action log, and the T1/replay hashes never see a byte of it.
+apply_capture_zoom :: proc(rc: ^Render_Ctx, zoom_in: f32) {
+	rnd.view_refit(&rc.view)
+	zoom := zoom_in
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
+}
+
 // Render the world pass headless and read back normalized RGBA pixels. The
 // drag state defaults to {} (no active drag) — the golden frame is a settled
 // drawn-pipe state, not a mid-drag preview. 4.1: the capture ALSO draws the
diff --git a/harness/main.odin b/harness/main.odin
index 86e970e..b67873b 100644
--- a/harness/main.odin
+++ b/harness/main.odin
@@ -189,13 +189,33 @@ main :: proc() {
 	// evidence. Deterministic: the sim steps on the same tick grid; alpha is
 	// a pure function of the wall ms.
 	if verb == "motion-strip" {
-		if len(rest) < 5 || len(rest) > 6 {
+		if len(rest) < 5 || len(rest) > 7 {
 			usage()
 		}
-		// Perkins r1 N10: only the exact token `snapshot` selects snapshot
-		// mode — a typo'd 6th arg is a usage error, never a silent interp run.
-		if len(rest) == 6 && rest[5] != "snapshot" {
-			usage()
+		// the optional trailing args, ONE walk (a second loop would drift):
+		// the exact token `snapshot` selects snapshot mode (Perkins r1 N10 —
+		// a typo'd arg is a usage error, never a silent interp run);
+		// `zoom=<f32>` is the capture-altitude evidence override (the LOOK §1
+		// per-rung strips). A duplicate zoom= token is a usage error, never a
+		// last-one-wins overwrite (a strip captured at an unintended altitude
+		// silently invalidates the width evidence).
+		snapshot_mode := false
+		strip_zoom: f32 = 0
+		for kw in rest[5:] {
+			if kw == "snapshot" {
+				snapshot_mode = true
+			} else if strings.has_prefix(kw, "zoom=") {
+				if strip_zoom != 0 {
+					usage()
+				}
+				z, okz := strconv.parse_f32(kw[5:])
+				if !okz || !(z >= 1.0 && z <= 4.0) { // the NaN-rejecting band test (demo-parser parity)
+					usage()
+				}
+				strip_zoom = z
+			} else {
+				usage()
+			}
 		}
 		cat: pp.Catalogs
 		if e := load_catalogs(&cat); e != "" {
@@ -206,7 +226,7 @@ main :: proc() {
 		rl.InitWindow(1280, 720, "pp-motion-strip")
 		rc: Render_Ctx
 		render_setup(&rc, &cat)
-		code := run_motion_strip(rest[0], rest[1], rest[2], rest[3], rest[4], len(rest) == 6 && rest[5] == "snapshot", &cat, &rc)
+		code := run_motion_strip(rest[0], rest[1], rest[2], rest[3], rest[4], snapshot_mode, &cat, &rc, strip_zoom)
 		rl.CloseWindow()
 		pp.catalogs_destroy(&cat)
 		os.exit(int(code))
@@ -453,7 +473,7 @@ main :: proc() {
 }
 
 usage :: proc() {
-	fmt.eprintln("usage: harness run|save [demo...] [--stats-out <path>] | replay <demo> <log.bin> | drift-check | preview-check | stats-check <demo> | input-parity [save] | palcheck | map-preview <seed> [out.png] | dublin-shot [outdir] | dublin-grown [outdir] [ms] | wire-preview [outdir] | motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot] | motion-pixel")
+	fmt.eprintln("usage: harness run|save [demo...] [--stats-out <path>] | replay <demo> <log.bin> | drift-check | preview-check | stats-check <demo> | input-parity [save] | palcheck | map-preview <seed> [out.png] | dublin-shot [outdir] | dublin-grown [outdir] [ms] | wire-preview [outdir] | motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot] [zoom=<f>] | motion-pixel")
 	when #config(PP_DEBUG, false) {
 		fmt.eprintln("       PP_DEBUG: overlay-check <demo> <ms>")
 		fmt.eprintln("       PP_DEBUG: overlay-pixels <demo> <ms>")
diff --git a/harness/motion_strip.odin b/harness/motion_strip.odin
index 1d4db01..3cf612d 100644
--- a/harness/motion_strip.odin
+++ b/harness/motion_strip.odin
@@ -6,8 +6,13 @@ package main
 // after proof that packets GLIDE between the 20 Hz snapshots instead of
 // stepping in 50 ms jumps.
 //
-// Usage: harness motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot]
+// Usage: harness motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot] [zoom=<f>]
 //   - exports frames at start_ms, start_ms+step_ms, ... < end_ms
+//   - the capture ALTITUDE defaults to the demo's own pinned `zoom`
+//     directive (the golden path's transform; 1.0 = the fit when absent);
+//     `zoom=<f32>` (1.0..4.0) overrides it for per-rung evidence — the
+//     applied altitude is echoed in the summary line so archived strips
+//     self-describe what altitude they rendered at
 //   - `snapshot` forces alpha=1.0 — the pre-INTERPOLATION render (the
 //     snapshot positions at the capture ms; the +15% packet size applies in
 //     both modes — only the glide differs)
@@ -37,6 +42,7 @@ run_motion_strip :: proc(
 	snapshot: bool,
 	cat: ^pp.Catalogs,
 	rc: ^Render_Ctx,
+	zoom_override: f32 = 0,
 ) -> int {
 	start_ms, ok_s := strconv.parse_i64(start_ms_s, 10)
 	end_ms, ok_e := strconv.parse_i64(end_ms_s, 10)
@@ -98,6 +104,18 @@ run_motion_strip :: proc(
 	a11y_reset(rc)
 	apply_demo_a11y(rc, &demo)
 
+	// LOOK §1: the capture altitude. Default = the demo's own pinned `zoom`
+	// directive (the golden path's transform — strips render what the
+	// goldens render); `zoom=<f>` (the evidence override, 1.0..4.0 — the
+	// same NaN-rejecting band test as the demo parser) re-altitudes the
+	// strip for per-rung width evidence. View-only either way: the T1 drift
+	// net below still pins the stepped timeline to the blessed manifest.
+	strip_zoom := demo.zoom
+	if zoom_override >= 1.0 && zoom_override <= 4.0 {
+		strip_zoom = zoom_override
+	}
+	apply_capture_zoom(rc, strip_zoom)
+
 	hz := cat.balance.logic_hz
 	tick_ms := i64(1000) / i64(hz)
 	mkdir_p(outdir)
@@ -215,8 +233,8 @@ run_motion_strip :: proc(
 		fmt.eprintln("motion-strip: no frames rendered (window outside the demo run?)")
 		return 2
 	}
-	fmt.printf("motion-strip: %s %s %dms..%dms step %dms -> %d frame(s) (%s)\n",
-		demo_name, mode, start_ms, end_ms, step_ms, frames, outdir)
+	fmt.printf("motion-strip: %s %s %dms..%dms step %dms zoom %.2f -> %d frame(s) (%s)\n",
+		demo_name, mode, start_ms, end_ms, step_ms, strip_zoom, frames, outdir)
 	return 0
 }
 
diff --git a/harness/palcheck.odin b/harness/palcheck.odin
index 36d5d04..8c5a2f3 100644
--- a/harness/palcheck.odin
+++ b/harness/palcheck.odin
@@ -253,6 +253,30 @@ check :: proc(ok: bool, name: string, n: int) {
 // `tol` of `col` at screen column x (the stroke-width measurement for a
 // horizontal wire crossing that column; the longest run ignores stray AA
 // pixels). Returns found=false when no pixel of the family is on the column.
+// scan_col_v — count pixels in a VERTICAL scan crossing the row `cy` that
+// sit within tol of col (a vertical cut through a horizontal band measures
+// its thickness). ONE scanner shared by §7 and §8 — a restated copy drifts
+// the measurement convention between sections.
+scan_col_v :: proc(img: rl.Image, cx, cy, half: int, col: rl.Color, tol: i32) -> int {
+	px := rl.LoadImageColors(img)
+	defer rl.UnloadImageColors(px)
+	n: int = 0
+	if cx < 0 || cx >= int(img.width) {
+		return 0
+	}
+	for dy in -half..=half {
+		yi := cy + dy
+		if yi < 0 || yi >= int(img.height) {
+			continue
+		}
+		p := px[yi * int(img.width) + cx]
+		if abs(i32(p.r) - i32(col.r)) <= tol && abs(i32(p.g) - i32(col.g)) <= tol && abs(i32(p.b) - i32(col.b)) <= tol {
+			n += 1
+		}
+	}
+	return n
+}
+
 measure_color_run :: proc(img: rl.Image, col: rl.Color, x: int) -> (run: f32, found: bool) {
 	if x < 0 || x >= int(img.width) {
 		return 0, false
@@ -1111,21 +1135,10 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		mb := rnd.node_screen(&view, {8, 21}) // bundle B midpoint (non-involved)
 		// scan_col — count pixels in a vertical column crossing a horizontal
 		// band that sit within `tol` of `col` (the band interior; casing rims
-		// sit outside the scan half-width).
+		// sit outside the scan half-width). The SHARED file-scope scan_col_v
+		// (§8 uses the same scanner — one measurement convention).
 		scan_col :: proc(img: rl.Image, cx, cy, half: int, col: rl.Color, tol: i32) -> int {
-			px := rl.LoadImageColors(img)
-			defer rl.UnloadImageColors(px)
-			n := 0
-			if cx < 0 || cx >= int(img.width) { return 0 } // W3 (Perkins r1): both axes guarded (the scan_box guard, mirrored)
-			for dy in -half..=half {
-				yi := cy + dy
-				if yi < 0 || yi >= int(img.height) { continue }
-				p := px[yi * int(img.width) + cx]
-				if abs(i32(p.r) - i32(col.r)) <= tol && abs(i32(p.g) - i32(col.g)) <= tol && abs(i32(p.b) - i32(col.b)) <= tol {
-					n += 1
-				}
-			}
-			return n
+			return scan_col_v(img, cx, cy, half, col, tol)
 		}
 		// scan_box — count pixels in an anisotropic window around a node
 		// center (the chip zone sits ABOVE the sprite: tall upper half).
@@ -1307,6 +1320,225 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		pp.run_destroy(&state)
 	}
 
+	// --- 8. the congested-link pulse (A1 as amended + refined, 08-28) ------
+	// viscomm-audit R1 as AMENDED + REFINED (glow only): link sizes stay
+	// exactly as v2 (no width bump, no floor, NO width oscillation); the
+	// READ is a pure pulse in the glow margin's brightness — the halo's
+	// state-color SHARE oscillates between the classic 4.1 blend (trough)
+	// and the peak share through the house pulse_read seam, while the
+	// stroke core keeps the STEADY classic recolor (split render). The
+	// legs pin the DRAW PATH (the mutation legs run at DEV time):
+	//   delete-the-pulse (freeze the share at the trough) -> (a)/(b)/(d)
+	//   measure 0 px at the predicted PEAK color and (h) finds the peak
+	//   render indistinguishable from the trough -> RED; restore -> GREEN.
+	//   (c)/(e) are the calm covenant companions (a floor-or-pulse leak into
+	//   a calm board's draw fails them); (f) pins the trough at the classic
+	//   blend; (g) pins reduced-motion at the peak (the a11y convention).
+	// Live analysis frames like section 7 — the golden capture path never
+	// renders this fixture.
+	{
+		sv_scale8, sv_rung8, sv_rm8 := view.scale, view.zoom_rung, view.reduced_motion
+		sv_ox8, sv_oy8 := view.off_x, view.off_y
+		defer {
+			view.scale = sv_scale8
+			view.zoom_rung = sv_rung8
+			view.reduced_motion = sv_rm8
+			view.off_x = sv_ox8
+			view.off_y = sv_oy8
+		}
+		state: pp.Run_State
+		pp.run_init(&state, 8, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		res8, _ := pp.node_type_index(cat, "residential")
+		rtb8, _ := pp.node_type_index(cat, "router_basic")
+		std8, _ := pp.pipe_tier_index(cat, "standard")
+		na := pp.topology_spawn_node(&state.topology, res8, {4, 12}, cat)
+		nb := pp.topology_spawn_node(&state.topology, rtb8, {12, 12}, cat)
+		pe, perr8 := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = na, b = nb, tier = std8}}, cat)
+		ps8, ok_ps := pp.pipe_slot(&state.topology, pe.id)
+		pp.bundles_rebuild(&state.bundles, &state.topology, cat, state.era)
+		// the fixture's single live bundle index (never assume 0 — a packing
+		// change would silently measure a dead slot's zero width)
+		bi8: u32 = 0
+		found_bi := false
+		for b in 0..<len(state.bundles.bundle_count) {
+			if state.bundles.bundle_count[b] > 0 {
+				bi8 = u32(b)
+				found_bi = true
+				break
+			}
+		}
+		// render-only fixture: the draw-side level the warning pass writes
+		// for a congested pipe is pinned DIRECTLY on the crisis view-state —
+		// this section pins the DRAW PATH, not the producer (the corpus's
+		// congestion demos exercise warnings_update end-to-end; their T2
+		// diffs are the producer-path proof). Grown slots are zeroed to
+		// .None (mirroring warnings' own re-init) so a fixture extension
+		// can never measure allocator garbage.
+		testing_lvl_ok := ok_ps && found_bi
+		if testing_lvl_ok && int(ps8) >= len(state.crisis.pipe_congestion) {
+			old_len := len(state.crisis.pipe_congestion)
+			resize(&state.crisis.pipe_congestion, int(ps8) + 1)
+			for i in old_len..<len(state.crisis.pipe_congestion) {
+				state.crisis.pipe_congestion[i] = .None
+			}
+		}
+
+		view.scale = 2.0
+		view.zoom_rung = .Access // scale 2.0 absolute — the §7 camera (bands wide, clean sampling)
+		view.reduced_motion = false
+		view.off_x = f32(view.win_w) / 2 - f32(8) * view.tile_px * view.scale
+		view.off_y = f32(view.win_h) / 2 - f32(12) * view.tile_px * view.scale
+		mid8 := rnd.node_screen(&view, {8, 12})  // the band's midpoint column
+		capa8 := rnd.node_screen(&view, {4, 12}) // an END-CAP column (a mid-column-only scan can't see a cap leak)
+		band_px := int(rnd.link_width_capped(&view, &state.topology, &state.bundles, bi8) * view.scale)
+		check(testing_lvl_ok && perr8 == .None,
+			fmt.aprintf("section-8 premise: the fixture resolves (pipe err %v, bundle found %v)", perr8, found_bi), int(ps8))
+
+		// the pulse ticks (bundle phase = bi*5, advance 1: tick % 16 == 8 is
+		// the PULSE16 peak (factor 1.0); % 16 == 0 is the trough (factor
+		// 0.04, the table never reaches 0)). The renders use the REAL seam
+		// (view.reduced_motion honored) — a deleted or retabled pulse fails
+		// the predicted-color legs here.
+		peak_tick: u64 = 1000 // % 16 == 8
+		trough_tick: u64 = 992 // % 16 == 0
+
+		// the draw's own blend via the palette tokens, but the SHARE anchors
+		// to the RULED CONSTANTS at the pinned phase ticks — never through
+		// congestion_pulse_share itself (a prediction that routes through the
+		// proc under test mutates with the mutation and self-confirms; the
+		// anchor here is the ruled 0.43/0.75 + the pinned PULSE16 phase).
+		steel8 := view.palette.pipe_steel
+		halo_blend8 :: proc(raw, state_col: rl.Color, share: f32) -> rl.Color {
+			return rl.Color{
+				u8(f32(raw.r) * (1.0 - share) + f32(state_col.r) * share),
+				u8(f32(raw.g) * (1.0 - share) + f32(state_col.g) * share),
+				u8(f32(raw.b) * (1.0 - share) + f32(state_col.b) * share),
+				255,
+			}
+		}
+		peak_share8 :: f32(rnd.CONGESTION_PULSE_PEAK_SHARE) // PULSE16[8] == 1.0 at tick % 16 == 8
+		trough_share8 :: f32(rnd.CONGESTION_PULSE_TROUGH_SHARE) +
+			(rnd.CONGESTION_PULSE_PEAK_SHARE - rnd.CONGESTION_PULSE_TROUGH_SHARE) * 0.04 // PULSE16[0], the table floor, at tick % 16 == 0
+		peak_amber := halo_blend8(steel8, view.palette.state_congested, peak_share8)
+		peak_red := halo_blend8(steel8, view.palette.state_critical, peak_share8)
+		trough_amber := halo_blend8(steel8, view.palette.state_congested, trough_share8)
+		core_amber := halo_blend8(steel8, view.palette.state_congested, f32(rnd.CONGESTION_PULSE_TROUGH_SHARE)) // the STEADY stroke core (exact trough share, any tick)
+		core_red := halo_blend8(steel8, view.palette.state_critical, f32(rnd.CONGESTION_PULSE_TROUGH_SHARE))
+		glow_px := int(5.0 * view.scale) // the glow margin's thickness at this scale (halo extent minus the stroke core)
+
+		// vacuity premise: the peak and trough predictions must differ by
+		// more than 2x the scan tolerance on SOME channel — otherwise the
+		// pulse legs cannot discriminate a deleted pulse (check the strongest
+		// channel, the red one: steel r=0 vs amber 242 / red 232).
+		chan_gap := abs(i32(peak_amber.r) - i32(trough_amber.r))
+		chan_gap = max(chan_gap, abs(i32(peak_amber.g) - i32(trough_amber.g)))
+		chan_gap = max(chan_gap, abs(i32(peak_amber.b) - i32(trough_amber.b)))
+		check(chan_gap > 20,
+			fmt.aprintf("section-8 premise: peak vs trough predictions differ by %d (min 21) — a flattened pulse envelope vacates the legs", chan_gap), int(chan_gap))
+
+		render8 :: proc(view: ^rnd.View, state: ^pp.Run_State, tick: u64) -> rl.Image {
+			rl.BeginDrawing()
+			rl.ClearBackground(rl.Color{237, 226, 200, 255})
+			rnd.draw_world(view, &state.topology, &state.bundles, &state.flow, &state.crisis, tick, {}, -1, -1, state.seed)
+			rl.EndDrawing()
+			img := rl.LoadImageFromScreen()
+			normalize(&img)
+			return img
+		}
+
+		// (a) AMBER at the peak tick: the predicted pulsing color is on the
+		// wire at exactly the untouched v2 width (band + 5*scale — the
+		// sizes-unchanged pin rides the same scan).
+		if testing_lvl_ok {
+			state.crisis.pipe_congestion[ps8] = .Amber
+			img := render8(&view, &state, peak_tick)
+			n_glow := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, peak_amber, 10)
+			n_core := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, core_amber, 10)
+			check(n_glow >= glow_px - 3 && n_glow <= glow_px + 3 && n_core >= band_px - 3 && n_core <= band_px + 3,
+				fmt.aprintf("glow-only split at peak: pulsing margin %d px (want %d) + steady core %d px (want band %d) — a pulse on the CORE, a width move, or a deleted pulse fails here", n_glow, glow_px, n_core, band_px), n_glow)
+			rl.UnloadImage(img)
+		}
+
+		// (b) RED at the peak tick: the same law, the critical blend
+		if testing_lvl_ok {
+			state.crisis.pipe_congestion[ps8] = .Red
+			img := render8(&view, &state, peak_tick)
+			n_red := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, peak_red, 10)
+			n_core_red := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, core_red, 10)
+			check(n_red >= glow_px - 3 && n_red <= glow_px + 3 && n_core_red >= band_px - 3 && n_core_red <= band_px + 3,
+				fmt.aprintf("critical glow split at peak: margin %d px (want %d) + steady core %d px (want band %d)", n_red, glow_px, n_core_red, band_px), n_red)
+			rl.UnloadImage(img)
+		}
+
+		// (c) CALM: no congestion -> the stroke at exactly the capped band,
+		// zero halo pixels anywhere on the scan columns (a pulse-or-floor
+		// leak into a calm board's draw fails here)
+		if testing_lvl_ok {
+			state.crisis.pipe_congestion[ps8] = .None
+			img := render8(&view, &state, peak_tick)
+			n_stroke := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 8, steel8, 10)
+			n_halo_leak := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 8, peak_amber, 10) + scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 8, peak_red, 10)
+			n_cap_leak := scan_col_v(img, int(capa8.x), int(capa8.y), band_px + 8, peak_amber, 10) + scan_col_v(img, int(capa8.x), int(capa8.y), band_px + 8, peak_red, 10)
+			check(n_stroke >= band_px - 3 && n_stroke <= band_px + 3 && n_halo_leak == 0 && n_cap_leak == 0,
+				fmt.aprintf("calm stroke draws at exactly the covenant band (stroke %d px, band %d, halo leak %d, end-cap leak %d — a pulse leak fails here)", n_stroke, band_px, n_halo_leak, n_cap_leak), n_stroke)
+			rl.UnloadImage(img)
+		}
+
+		// (d)+(e): the ROUTED branch — the "ONE look" invariant is a PIN,
+		// not a comment. The routed call site must render the SAME pulsing
+		// color at the SAME untouched width, and the routed CALM draw must
+		// stay halo-free.
+		{
+			sv_rw := view.route_wires
+			defer view.route_wires = sv_rw
+			view.route_wires = true
+
+			state.crisis.pipe_congestion[ps8] = .Amber
+			img := render8(&view, &state, peak_tick)
+			n_routed := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, peak_amber, 10)
+			n_routed_core := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, core_amber, 10)
+			check(n_routed >= glow_px - 3 && n_routed <= glow_px + 3 && n_routed_core >= band_px - 3 && n_routed_core <= band_px + 3,
+				fmt.aprintf("routed glow split at peak: margin %d px (want %d) + steady core %d px (want band %d) — a routed-branch drift or deleted pulse fails here", n_routed, glow_px, n_routed_core, band_px), n_routed)
+			rl.UnloadImage(img)
+
+			state.crisis.pipe_congestion[ps8] = .None
+			img2 := render8(&view, &state, peak_tick)
+			n_routed_leak := scan_col_v(img2, int(mid8.x), int(mid8.y), band_px + 8, peak_amber, 10)
+			check(n_routed_leak == 0,
+				fmt.aprintf("routed calm draw stays halo-free (leak %d px — a pulse leak into the routed branch fails here)", n_routed_leak), n_routed_leak)
+			rl.UnloadImage(img2)
+		}
+
+		// (f) TROUGH: at the trough tick the halo sits within a whisker of
+		// the classic 4.1 blend (the table's 0.04 floor) — the pulse's
+		// resting color is the untouched v2 recolor. ALSO: the PEAK color
+		// must be ABSENT here (the oscillation actually moved).
+		if testing_lvl_ok {
+			state.crisis.pipe_congestion[ps8] = .Amber
+			img := render8(&view, &state, trough_tick)
+			n_trough := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, trough_amber, 8)
+			n_peak_at_trough := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, peak_amber, 8)
+			check(n_trough >= band_px + glow_px - 4 && n_peak_at_trough == 0,
+				fmt.aprintf("trough renders the classic-blend color (trough %d px, peak color %d px — a phase-less or flattened pulse fails here)", n_trough, n_peak_at_trough), n_trough)
+			rl.UnloadImage(img)
+		}
+
+		// (g) REDUCED MOTION: the envelope pins at the PEAK (the pulse_read
+		// convention — the most legible static reading), deterministic at
+		// ANY tick.
+		if testing_lvl_ok {
+			view.reduced_motion = true
+			state.crisis.pipe_congestion[ps8] = .Amber
+			img := render8(&view, &state, trough_tick)
+			n_rm := scan_col_v(img, int(mid8.x), int(mid8.y), band_px + 12, peak_amber, 10)
+			check(n_rm >= glow_px - 3,
+				fmt.aprintf("reduced motion pins the glow at peak (measured %d px of the peak color at the trough tick)", n_rm), n_rm)
+			rl.UnloadImage(img)
+			view.reduced_motion = false
+		}
+	}
+
 	if fails > 0 {
 		fmt.printfln("palcheck: %d check(s) FAILED", fails)
 		return 1
diff --git a/harness/run.odin b/harness/run.odin
index ad2ed91..5b8ee9c 100644
--- a/harness/run.odin
+++ b/harness/run.odin
@@ -315,22 +315,10 @@ run_demo :: proc(name: string, save: bool, cat: ^pp.Catalogs, rc: ^Render_Ctx, s
 	rnd.spawn_fx_reset(&rc.view.spawn_fx)
 
 	// LOOK §1: the demo's pinned capture altitude (view-only run setup —
-	// the a11y/map precedent: T1 + replay never see a byte). Reset to the
-	// fit (undoing the previous demo's zoom), then derive the transform +
-	// the ladder rung from THIS demo's directive. zoom 1.0 (absent) = the
-	// fit view — the same transform every legacy demo captured.
-	rnd.view_refit(&rc.view)
-	zoom := demo.zoom
-	if zoom < 1.0 { // the absent-directive zero value normalizes to the fit
-		zoom = 1.0
-	}
-	rc.view.zoom_rung = rnd.zoom_rung_of(zoom)
-	if zoom != 1.0 {
-		fit := rnd.camera_fit(&rc.view)
-		rc.view.scale = fit * zoom
-		rc.view.off_x = (f32(rc.view.play_w) - rc.view.world_w * rc.view.scale) / 2
-		rc.view.off_y = (f32(rc.view.win_h) - rc.view.world_h * rc.view.scale) / 2
-	}
+	// the a11y/map precedent: T1 + replay never see a byte). ONE derivation
+	// with motion-strip's override (apply_capture_zoom). zoom 1.0 (absent)
+	// = the fit view — the same transform every legacy demo captured.
+	apply_capture_zoom(rc, demo.zoom)
 
 	state: pp.Run_State
 	defer pp.run_destroy(&state)


--- SPEC / CONTEXT ---
## Spec file 0: the 2026-08-28 USER RULINGS that AMEND the briefing (THEY SUPERSEDE the briefing's A1 width language wherever they conflict — the width emphasis was REVERTED on this branch)

# Perkins round: packet-plumber-v2-congestion-read-a1-perkins-r2

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/106 (number 106)
**Reviewed sha:** 75fb2169fef76b89630975b0540e852032e35e78 (re-fetch headRefOid before posting; if moved, post anyway + note)
**Repo root:** /Users/moses/code/packet-plumber · **Your cwd:** your detached round worktree at exactly the reviewed sha
**Spec:** the original job briefing /Users/moses/code/_bmad-output/briefs/packet-plumber-v2-congestion-read-a1.md AS AMENDED by user rulings (see below); audit report at /Users/moses/code/_bmad-output/implementation-artifacts/packet-plumber-v2-viscomm-regression-audit/viscomm-regression-audit.md
**Round dir:** /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-congestion-read-a1/r2/
**prior_findings:** /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-congestion-read-a1/r1/consolidated.json — THIS IS A FIX-DELTA ROUND: fix-audit first (verify each r1 finding resolved or explicitly superseded by the user rulings below), then delta review of the new work.
**Model:** zai-coding-cn/glm-5.3-flash (natively multimodal — captures read INLINE; pixel measurements decide). Bash 3.2 — NO arrays in wave scripts.

## USER RULINGS that define the acceptance criteria (they supersede the r1 shape)

1. Link sizes stay EXACTLY as v2 shipped them — NO width bump, NO min-width floor. The r1-approved width emphasis is REVERTED on this branch.
2. The read returns as a PURE PULSE, GLOW ONLY (user-confirmed option A of glow/stroke/both): halo/brightness oscillates; stroke geometry NEVER moves.
3. Calm board stays byte-identical. LOOK-SPEC line: "congested pulse emphasis, sizes unchanged".
4. Acceptance bar: the read must be VISIBLE at thin strokes — mechanical proof = intensity-over-time strips + congested-corridor captures; the USER EYEBALL (committed peak-vs-trough crops) is the final gate at review.

## Your r2 mandates (the fix-delta legs — re-run RED-then-GREEN INDEPENDENTLY)

- Verify the r1 width emphasis is actually GONE (sizes == v2 baseline; no floor) — a leftover bump is a blocker.
- Re-run the delete-the-pulse mutation leg YOURSELF: deleting the glow pulse must turn its gate RED (minion claims RED ×4: inline/red/routed + reduced-motion), restore GREEN.
- Glow-only split pins: margin == 5×scale, core == band exactly, on inline/red/routed legs — geometry must not move.
- Calm covenant: corpus calm demos byte-identical + palcheck §8 calm/end-cap/routed-calm legs.
- Intensity series (NOT width): envelope span and cadence on congested links at the three rungs (minion claims 0.440–0.750 span 0.310, 1.25 Hz, 3 clean cycles).
- Re-bless delta SCRUTINY: r1 re-blessed 33 demos, this round claims 14 — the disclosed reason is "steady core barely moves at trough". Verify the delta is exactly the disclosed set and nothing else drifted (corpus 49/49, sim bytes pristine).
- The eyeball-gate crops must exist in the PR (frames/glow_peak-vs-trough_warn_z{1.0,1.4,2.0}.png) and match the captured runs.
- Carry forward any r1 findings NOT resolved by the rework (the 6 warnings / 7 notes from r1: resolved, still open, or superseded — say which per item).

CI context: the PR's GitHub Actions "verify" runs show the billing-block signature (log not found, 0 steps) — note-only, NOT a gate; local gates are the merge ground truth.

Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-congestion-read-a1-perkins-r2 working` at start; final message = verdict + review URL + findings counts. Round row already exists — work it, do not create one.

---

## Standing orders (paste verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job
  briefing** and **GitHub issue** (your spec), and your cwd — a detached
  worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first:
  `gh pr diff <pr>` →
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>/diff.patch`.
  Every lens reviews these identical bytes. (Absolute path — the round
  worktree is destroyed at close-out, so artifacts live in the
  orchestrator's `_bmad-output`.) **[r2 fix-delta note: the FULL PR diff
  df14785..75fb216 is only ~614 lines — save it canonically; the r1 bulk
  was already verified last round.]**
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (here: no issue; use the briefing + the
  rulings in this briefing), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` (fix audit
  first, carry-forward markers). The headless mode owns: pane mechanics
  (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output
  contract + existence check, one retry per failed lens, big-diff
  chunking, the mandatory verification pass, consolidation, and writing
  `consolidated.json`. Its verdict thresholds are yours below.
  **Lens-spawn rooting (user-approved 2026-08-18):** the headless spawn
  template pins `--cwd <worktree>` on every lens tab FOREVER — a lens
  pane whose cwd is not the round worktree is mis-rooted: close +
  relaunch with `--cwd`.
  **Empty-lens doctrine (2026-08-18/19):** acceptance/architecture
  lenses back 3-byte-EMPTY a THIRD straight generation → sweep those
  lens panes + regenerate (intervene — an empty-lens verdict never
  ships); a g-wave COMPENSATION verdict (a subset of lenses delivering a
  valid verdict) counts as valid.
  Visual checks (goldens, sprites): verify MECHANICALLY first
  (byte/hash/capture-diff); your model is natively multimodal — vision
  is INLINE for screening, but pixel measurements decide, never a bare
  visual impression. Never fake a measurement.
  You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT
    approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then
  review — never run gh with an empty GH_TOKEN (a failed command
  substitution would fall through to the ambient `mssoka` credential and
  422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>)` —
     capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache
     warnings to stderr, which would corrupt the token and make a good
     mint look like a failure.
  2. Check for an EMPTY token, NOT `$?` (an intervening command can
     clobber `$?`, and a `2>&1` capture makes it lie — the 2026-08-09
     rc3-2 round posted a fallback-comment instead of a formal approve
     on exactly this):
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment
     <pr> --body-file <body.md>`, note `fallback-comment` in your ledger
     note, and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr>
     --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N>
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  The loop runs until an APPROVED verdict._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.


## Spec file 1: the job briefing (the original A1 claims — READ TOGETHER WITH Spec file 0, which amends it)
# Briefing: packet-plumber-v2-congestion-read-a1

Implementation job — USER-RULED restore (option A1 of the viscomm
regression audit). READ THE AUDIT FIRST:
`_bmad-output/implementation-artifacts/packet-plumber-v2-viscomm-regression-audit/viscomm-regression-audit.md`
— especially the R1 row, the "Rulings received" section, the A1
appendix, and the evidence register. It is your spec.

## Context

- Audit verdict (HIGH confidence): no viscomm effect silently severed by
  #105 — but R1, the LINK CONGESTION READ, is DEGRADED: the telegraph
  mechanisms (halo + level flicker + outline swell + ring pulses) are
  INTACT at both commits, while the L1 scale covenant (eb2e766) thinned
  the strokes under the signal 3.6–5.1×, so a congesting link barely
  widens any more.
- USER RULING 2026-08-27 (lavish session, on record): **R1 → RESTORE via
  option A1** (congested-state width emphasis).
- **R2 lane stripes and R3 Dublin blocks are LEAVE** (standing
  recommendation, no ruling) — DO NOT restore, reference, or widen scope
  toward them. A2 (ladder retune) / A3 / A4 are OUT too.

## Scope — A1 exactly

In `draw_bundles` (BOTH branches), for `lvl != .None`:

- Draw the halo at `max(band + 5×scale, congestion_floor×scale)` with
  `congestion_floor ≈ 10–14 world px` — tune within that band for the
  clearest read; OR bump the halo offset to `+8..+10×scale` for red.
  The appendix blesses both variants — pick the one that reads best at
  all three zoom rungs and re-blesses cleanest (or combine, if that is
  what the read needs — stay within the appendix's described envelope).
- Code anchors @ 03dd6f8: `view.odin:994` / `:1071` (halo draws),
  `:769` (`link_width_capped`).
- **Calm-board geometry stays BYTE-IDENTICAL** (covenant caps the STROKE;
  the telegraph layer is emphasis — that is the no-conflict rationale;
  your gates must keep it true).
- No sim/log bytes (ODN-1-safe).

## Gates — mutation-leg standard (a pin that can't fail is vacuous)

- A congested-width gate that FAILS when the emphasis is deleted
  (delete-the-bump leg RED, then GREEN).
- A calm-board covenant pin that stays GREEN (calm links byte-identical
  — the flags-off/calm proof).
- Re-bless the congestion-bearing goldens per the appendix risk list:
  warn ×3, juice/a11y@65s ×6, surge/estate_surge if engaged; palcheck §7
  involved-non-recede legs re-pinned to the new expectations.
- Motion-strip evidence: congested-link width series BEFORE vs AFTER
  (the audit's strip method, T1-hash-verified timelines) — the deliverable
  proof that the READ is back at every rung.

## Skills policy

- `bmad-build` (step 04 review swarm MANDATORY — never skip; adversarial
  + edge hunters).

## Model policy

- Minion: zai-coding-cn/glm-5.3-flash, --thinking max. Mega-minions
  inherit the same pin (natively multimodal; vision inline).

## PR + Perkins

- pr_review=1 (canon-surface visual code). PR vs `v2`.
- `bin/check-pr-ready` before close-out; verdict posts as the
  perkins-review bot.
- CI note: GH-Actions billing block may show 5s runs / zero logs /
  "payments failed" — that signature is note-only, reruns are useless;
  local gates are the merge ground truth.

## Constraints

- mechanics-quinn (idle design session) holds the packet-plumber main
  checkout — you run in a worktree; never touch its surface or pane.
- bash 3.2 on this machine — no arrays in scripts.
- Doc hygiene: ONE line in the repo's LOOK-SPEC noting the A1 amendment
  (congested emphasis layer ≠ covenant change) — no essays.
- Lane stripes / Dublin blocks / ladder retune: OUT OF SCOPE, flag only.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-congestion-read-a1
- base: v2 (Silas resolves the fresh head at dispatch)
- model: zai-coding-cn/glm-5.3-flash --thinking max
- github_issue: (none)
- pr_review: 1


## Spec file 2: the viscomm regression audit — the original acceptance criteria (R1 row, "Rulings received", Appendix A1, evidence register)
# Case File: packet-plumber-v2-viscomm-regression-audit

**Job:** packet-plumber-v2-viscomm-regression-audit · READ-ONLY forensic audit, no code changes, no PR.
**Question:** after PR #105 (look-zoom-language, merge `03dd6f8`), some viscomm video effects LOOK LOST. Per effect: INTACT / DEGRADED / LOST / FLAG-GATED, with mechanical evidence and the exact severing commit+hunk.
**Skill:** gds-investigate discipline (evidence-graded findings); bmad-build renderer waived per the standing 2026-08-21/23 ruling.

## Hand-off Brief

No viscomm effect's code path was silently severed by #105. All four prime suspects were cleared mechanically: the sprites-only Dublin switch, the view.odin rewrite, the L3 reduced-motion pin, and the flag defaults each leave every lane effect reachable. What actually happened splits three ways: (1) every animated pulse mechanism (node rings, crisis outline swell, congested-link level flicker) is byte-verifiably ALIVE at both commits; (2) two visual surfaces were DELIBERATELY retired by the 2026-08-26 LOOK-SPEC rulings (lane stripes, Dublin street blocks) — lost-by-ruling, not lost-by-bug; (3) the link congestion telegraph — the user's named keep candidate — is DEGRADED in READ, not in mechanism: its recolor/flicker code is identical at both commits, but the stroke under it went from 16–23 px ribbons to 3.5–6 px ladder strokes (fit) and 33–55 px to 9 px at the resting zoom, collapsing the telegraph's canvas area ~4–6×. Confidence: HIGH (code traces at both commits + 200 strip frames + pixel measurements + green test gates).

## Case Info

| | |
|---|---|
| BEFORE | `088cf00` (merge of #104 — parent of the #105 branch) |
| AFTER | `03dd6f8` (merge of #105 — v2 HEAD) |
| Range | 5 commits: eb2e766 (L1), 33b4bbd (L2), e47d0e2 (L3), 5910ccd (L4), d5dd5a6 (review fold) |
| Diff surface | app/: 13 files, +1067/−407 — view.odin (+473/−402), dublin.odin (−165), wire_path.odin (−47+…), sprites/camera/crisis/assist/main + 3 new test files |
| Builds | rlsw SW harness built at BOTH commits (`ODIN_ROOT=<main>/tools/raylib-sw/shadow`); AFTER corpus run **49/49 demos green** (byte-faithful to the blessed goldens) |
| Gates | palcheck all green BOTH commits (93 PASS lines AFTER vs 70 BEFORE — the look legs are the delta); `odin test app/render` 114 + `odin test app` 51 green at AFTER |
| Captures | `captures/before|after/` (era goldens), `captures/strip_before|after/{warn,warn_early,juice}/` (50 frames each, 50 ms cadence, T1-hash-verified timelines) |

## Method

1. **Inventory** from the video's 7 effect classes, the design-audit artifacts (findings A/B/C), the five PR bodies (`_pr_body_*.md`), and the look_l1/l2/l4 + palette_polish + pullback tests.
2. **Path trace BEFORE vs AFTER**: full proc inventory of view.odin; every draw call site grepped at both commits; the complete view/wire_path/sprites/camera/dublin/assist/crisis/main diffs walked hunk by hunk.
3. **Mechanical proof**: rlsw builds at both commits; `motion-strip` captures (warn 44.0–46.5 s, warn 1.0–3.5 s, juice 64.0–66.5 s; 50 frames each side); PIL pixel measurement (colors, thicknesses, per-frame oscillation); golden-corpus diff.
4. Vision (native multimodal) used for screening only; every verdict below rests on pixel numbers or code identity.

## Findings (evidence-graded)

### F1 — Gauge telegraph (count-up lerp + chunk flash) — **INTACT** (Confirmed)

- #100's surfaces: `app/render/gauge.odin`, `app/render/health.odin` — **zero diff lines** in 088cf00..03dd6f8. The #105 diffstat does not touch them; `draw_health_meter`'s tick param and the app feed wiring (main.odin) are unchanged.
- Mechanical: palcheck §6 draw-path legs green at AFTER — "mid-ease fill sits at the EASE16-predicted edge (212 px vs raw 182)", same for pool; ghost/reduced-motion legs PASS.
- Verdict: the video's count-up-lerp and flash-before-drain classes are fully live. HUD **counters** were never lerped by design (truth channels stay RAW per #100) — that is spec-faithful, not a regression.

### F2 — Crisis desaturation (attention-via-contrast, #102) — **INTACT** (Confirmed)

- `crisis_desat_factor` + `crisis_recede*` untouched (the only crisis.odin diff in range is the outline-width covenant hunk, d5dd5a6). `draw_world` still derives `desat_f` once per frame and threads it through bundles/nodes/packets (view.odin:540 AFTER).
- Mechanical: juice@65s (zone crisis, fully engaged) has **0 vivid network-token pixels at BOTH commits** (tolerance 28 on copper/steel/gold); calm@30s vivid ink 23,771 px (BEFORE) vs 7,252 px (AFTER) — the delta is the thinner ladder, not the desat.
- palcheck §7a–f all green at AFTER (raw-absent, involved non-recede, rider recede, mid-ramp three-way, reduced-motion pin, Dublin leg).
- Dublin nuance: the STREET-BLOCK recede surface retired with the blocks (F9); the recede mechanism itself is map-agnostic and now rides the sprite family wash (`draw_family_wash(..., recede)` unchanged, `DUBLIN_WASH_SCALE` 0.45 applied before the recede alpha math). The §7f leg was re-pinned in #105 to sprite-presence with the comment "the recede mechanism is map-agnostic, pinned on the procedural legs above".

### F3 — Tie de-conflict (#99) — **INTACT** (Confirmed)

- `data/palette.json` untouched in range (`route_tie` stays `#BA5EE8` @ 280°); `tie_dash_on` / `tie_dash_segments` / `draw_tie_mark` unchanged (assist.odin's only range-diffs are two width derivations moved to `link_width_capped` + the ghost-halo 2.2× fix, both review-fold items).
- `draw_route_glow` call sites (main.odin:752/756) identical at both commits.

### F4 — **LINK CONGESTION PULSE** (restore-candidate #1, user-named) — mechanisms **INTACT**, read **DEGRADED** (Confirmed, both halves)

**The mechanisms are alive — identical code, identical dynamics:**
- The 4.1 congestion halo draw is **byte-identical** at both commits in BOTH branches (inline view.odin:916–930 BEFORE / 994–1008 AFTER; routed 1017–1031 / 1071–1085): `halo = raw×0.57 + state×0.43`, `w = band + 5×scale`, drawn over the stroke. No pulse envelope existed on it at either commit — the halo is a recolor, by code.
- The **level flicker** (the visible "pulsating"): warn strip, router→host link centerline, x=780 — BOTH commits step `(99,115,166)` (steel×red) → `(104,163,166)` (steel×amber) at exactly 44.4 s, then back — the congestion level crossing thresholds re-tints the link, identically phased.
- The **crisis outline swell** (PULSE16 red stroke on the crisis bundle's member pipes — the one true pulsating-link effect): juice strip red-ink oscillates with the same 16-tick period and phase at both commits — BEFORE 4367→5148→4367 px, AFTER 2175→2867→2175 px.
- The **node health rings** (1.25 Hz amber / 2.5 Hz red): warn-early strip, red ink cycles with the 8-tick period at both commits — BEFORE [919,897,927,965,964,1001,964,945], AFTER [588,566,596,634,633,670,633,614]; ring radius base `s×0.95` unchanged; `!!` glyph + double ring confirmed visually at both (captures/crops/host_pulse_*.png).

**What degraded is the canvas the telegraph paints on (severed by eb2e766, L1):**

| measure | BEFORE (088cf00) | AFTER (03dd6f8) | ratio |
|---|---|---|---|
| standard link @ fit zoom 1.0 (CORE) | 7.4×2.2 = 16.3 px + 4.5 casing | 3.5 px single stroke | **4.7× thinner** |
| wide link @ fit | 10.5×2.2 = 23.1 px + casing | 6.0 px | **3.9× thinner** |
| standard @ boot zoom 2.0 (ACCESS) | 32.6 px + casing = 41.6 | 9.0 px | **3.6× thinner** |
| wide @ boot zoom 2.0 | 46.2 px + casing = 55.2 | 9.0 px (ACCESS uniform) | **5.1× thinner** |
| congested recolor area @ fit (per link length) | 21.3 px × L | 8.5 px × L | **~6× less ink** |
| calm-board vivid link ink (juice@30s) | 23,771 px | 7,252 px | ~31% |

The L1 laneless ruling removed the ×2.2 band factor, the casing, and the lane stripes, and imposed the 0.5×-node covenant. Every pulse mechanism survived; the fat glowing ribbon the user remembers — the thing that made congesting links READ as pulsating — is now a thin stroke with the same recolor math on ~1/4–1/6 the area. **This is a perceptual regression of the telegraph's salience, not a severed code path.** Severing commit: `eb2e766` (L1: "the scale covenant + the laneless link ladder") — hunks: `BUNDLE_EXTRA_WIDTH/CASING_OVERHANG/casing_color` deletion + `band_width` re-derivation (`tier+extra)×2.2 → link_width_world×scale`) + the inline/routed draw rewrites in `draw_bundles`.

### F5 — Node telegraph (rings + glyphs + pulse) — **INTACT** (Confirmed)

- `draw_health_ring` unchanged in range (pulse_read seam, radius base, advance rates 1/2 table-entries per tick, glyphs). `draw_nodes` still calls it for every `lvl != .None` node; the crisis recede never touches rings (telegraph family).
- Mechanical: the 8-tick red pulse cycle measured at both commits (F4); `!!` + double-ring crops visually identical except the node size under them (the L4 ladder).

### F6 — Crisis outline swell — **INTACT** (thinner by ruling) (Confirmed)

- `draw_crisis_outlines` swell code unchanged (PULSE16, phase `(tick+bundle)%16`, reduced-motion pin). Still called from draw_world:550. The ONLY range change is the width basis: `band_width(...) → link_width_capped(...)×scale` (d5dd5a6 — the adversarial hunter's fold: the outline must hug the capped stroke). Swell oscillation verified in the juice strips (F4). Ink count ~55% of BEFORE — direct consequence of the thinner host stroke, by ruling.

### F7 — Packet affordance (trails, glints, rider lattice, involvement pins) — **INTACT** (Confirmed)

- `pkt_interp`/`TRAIL_FADES`/`trails_active`/glint code identical both commits. The #102 "packet chain pins" = the `crisis_packet_involved` one-resolution-chain pin — untouched.
- The rider lattice width now derives from `link_width_capped` (was `band_width − 2×lane_gutter`): riders compress toward the centerline on thin strokes — documented in the #105 body as the covenant's natural fallout ("Fork 2 is open/parked"). Shape/behavior unchanged.

### F8 — Camera breath / pullback — **INTACT by default; pinned under reduced-motion (deliberate, L3)** (Confirmed)

- The L3 change is exactly scoped: `pullback_feed` gains an early return under `a11y.reduced_motion`, and `set_reduced_motion` freezes in-flight breath targets (e47d0e2 + the edge-case-hunter blocker fold in d5dd5a6). With reduced_motion OFF (the default), pullback behavior is byte-identical: feed keys on estate seeds, wheel overrides, `auto_pullback` default ON (settings.odin untouched). `pullback_test` (new) green.
- No collateral pinning: gauges (#100), pulse surfaces (7.3), desat ramp (#102) already had their own reduced-motion seams BEFORE #105; L3 added only the camera pin. Suspect (c) cleared.
- Known pre-existing issue documented + deferred in #105 (NOT a regression): the N11 auto-pullback toggle shares the latent ease-continues behavior mid-toggle.

### F9 — Dublin street blocks (+ their crisis recede + frontage) — **LOST-BY-RULING (deliberate)** (Confirmed)

- Severed by `5910ccd` (L4 "sprites-only Dublin", the 2026-08-26 user ruling): `dublin_node_block_draw`, `dublin_node_street`, the seg grid + cache, `dublin_screen_tile` deleted wholesale (−165 lines; "a render function never called is not a feature").
- What carries the block's jobs now: Blender sprites on BOTH maps + family wash at `DUBLIN_WASH_SCALE` 0.45; crisis recede rides the wash (F2); type chip unchanged. palcheck §7f re-pinned to sprite presence (involved washed-coral / non-involved washed-sage, both ≥100 px). Dublin@90s before/after: same board, rings, banner; 0.86% pixels changed.
- The block-specific recede twin (§7f's old alpha-twin scan) retired WITH the surface — the mechanism survives on the wash; no orphaned contract.

### F10 — Lane stripes + lane-detail reveal (7.1) — **LOST-BY-RULING (deliberate)** (Confirmed)

- Severed by `eb2e766` (L1 laneless): the lane-stripe walks deleted in BOTH draw_bundles branches; `draw_path_offset_band` deleted; `lane_detail` field removed entirely (zero references remain); `lane_express/standard/best_effort` palette tokens now have ZERO consumers (dead data, kept for palette compat).
- Supersession is explicit in the PR body and LOOK-SPEC §3 ("queues are ingress/egress on ROUTERS; the road doesn't gossip"). The lane-cap DATA seam survives (`bundle_lane_caps_view` still computed for riders), so a future reversal has a live data source.

### F11 — The #105 additions themselves — **PRESENT + PINNED** (Confirmed)

- Dusk dial (L2): warm dots under settlements, cool DC anchor, alphas {0,120,200}/{0,140,210} — visible in AFTER warn@45s (mauve halo around the host) and Dublin@90s (orange settlement glows); "ACCESS dark at rest" leg PASS.
- Node ladder (L4: 1.00/1.10/1.22/1.35) + rung shrink (1.00/0.62/0.42 etc.): "toward-space shrink is monotone (2427 > 285 > 67)" PASS; sprite/body pins PASS.
- Ring floor (L4): `max(2.0, 0.055×tile_px×scale)` — floor pin green (M8 mutation-proven in-PR).
- Covenant + laneless at pixels: palcheck §2 legs green at all three rungs (stroke == table ±1 px; laneless zero-count; covenant ≤ cap).

### Prime suspects — clearance summary

| suspect | verdict |
|---|---|
| (a) sprites-only Dublin severed viscomm draws on the old vector path | The only resident was the block draw's own recede/wash/chip — all re-hosted on the sprite path (F2/F9). Nothing else lived there. |
| (b) view.odin rewrite skips overlay layers | draw_world order intact (map→telegraph→bundles→highlight→nodes→packets→crisis outlines→ghosts→selection); route_glow/health/forecast/HUD call sites unchanged; corpus 49/49. |
| (c) L3 reduced-motion pin gates more than the breath | The pin is two scoped additions (feed gate + target freeze). All other effects had pre-existing seams. Default-off flag → default behavior unchanged. |
| (d) flag lattice defaults gate an effect off | No flag defaults changed in range (route_wires/wire_anchors off, reduced_motion off, auto_pullback on — both commits). `lane_detail` was deleted, not gated. |

## KEEP/LEAVE decision menu (the deliverable's final section)

Per row: added-by PR → status → evidence → if lost/degraded: severing commit + minimal restore hook (described, NOT implemented) → recommendation. **The user rules keep-vs-leave per row.**

| # | Effect (video class) | Added by | Status | Evidence | If lost/degraded: severance + restore hook | Recommendation |
|---|---|---|---|---|---|---|
| R1 | **Link congestion pulse** (distinct telegraphs / idle-motion read) | pre-lane (4.1/7.5), built around by #99 | **DEGRADED (read) — mechanisms INTACT** | Code-identical halo + level flicker + outline swell + ring pulses at both commits (F4 strips); stroke under the signal 3.6–5.1× thinner; recolor ink ~6× less | Severed by `eb2e766` (L1). Restore hook (emphasis, not geometry): give congested links a **min-width floor or a congested width bump** — e.g. `w = max(band, congestion_floor)` in the halo draw, or raise the halo offset for lvl≠None. ~8–10 congestion-bearing goldens re-bless (warn/juice/a11y@65s). No ruling conflict: it emphasizes, it does not un-thin the calm board. | **KEEP the mechanisms** (they are correct and ruling-compliant). If the old READ is wanted back: restore option A1 (below) — cheapest, reversible. |
| R2 | Lane stripes + lane-detail reveal (gestalt/QoS read) | #7.1-era (3.3 canon) | **LOST-BY-RULING** (deliberate supersession) | F10; lane tokens zero consumers; caps data seam alive | `eb2e766`. Restore hook: re-add the 3-stripe walk in both draw_bundles branches behind a `lane_stripes` view flag DEFAULT-OFF (golden-neutral while off), fed by the surviving `bundle_lane_caps_view`. Needs the 2026-08-26 laneless ruling explicitly reversed. | **LEAVE** — the laneless ruling is recorded and fresh (08-26); the thin-stroke language is the adopted look. Revisit only if the user reverses the ruling. |
| R3 | Dublin street blocks + block recede (gestalt/affordance on the real map) | #95 (amendment #2) | **LOST-BY-RULING** (deliberate supersession) | F9; §7f re-pinned to sprites; wash recede carries the crisis read | `5910ccd`. Restore hook: reinstate `dublin_node_block_draw` + seg grid behind a map/flag gate; the deleted code is recoverable from git. Conflicts with the sprites-only ruling; re-blesses Dublin goldens. | **LEAVE** — the sprite path carries the same information (family wash + chip + recede) with better sculpting; the ruling is recorded. |
| R4 | Gauge telegraph (count-up lerp + chunk flash) | #100 | **INTACT** | F1: files untouched; palcheck §6 legs green | — | **KEEP** (no action). |
| R5 | Crisis desat (contrast hierarchy) | #102 | **INTACT** | F2: 0 vivid px at crisis peak both; §7 green | — | **KEEP** (no action). |
| R6 | Tie de-conflict (distinct telegraphs) | #99 | **INTACT** | F3: palette + dash code untouched | — | **KEEP** (no action). |
| R7 | Node telegraph rings/glyphs/pulse (idle-motion) | 5.2/7.3 | **INTACT** | F5: 8-tick pulse cycle measured both commits | — | **KEEP** (no action). |
| R8 | Crisis outline swell | 4.2/7.x | **INTACT** (thinner by the covenant) | F6: 16-tick swell both commits | — | **KEEP** (no action). |
| R9 | Packet affordance: trails/glints/rider lattice | 2.1/#102 | **INTACT** (lattice narrower) | F7: code identical; width follows the covenant | — | **KEEP** (no action). |
| R10 | Camera breath (idle-motion) | pre-#105 | **INTACT by default**; pinned under reduced-motion (deliberate E9.2) | F8: scoped pin; default-off flag | — | **KEEP** (no action). |
| R11 | Dusk dial / node ladder / ring floor / covenant (gestalt) | #105 | **NEW — present + pinned** | F11: palcheck §2 + look tests + visible in captures | — | **KEEP** (no action). |

**Ranking of restore candidates (lost/degraded only):**
1. **Link congestion READ** (R1) — user-named; degraded-not-lost; cheapest restore (A1 below), no ruling conflict.
2. **Lane stripes** (R2) — lost-by-ruling; a flag-gated restore is golden-neutral while off but requires reversing a 2-day-old recorded ruling.
3. **Dublin blocks** (R3) — lost-by-ruling; lowest value — the sprite path supersedes the block's jobs cleanly.

## Rulings received (lavish review loop, 2026-08-27)

The user reviewed the HTML artifact and ruled via the KEEP/LEAVE menu, then ended the session:

- **R1 (link congestion READ) — RESTORED via option A1** (congested-state width emphasis). USER RULING ON RECORD 2026-08-27. This audit does NOT implement: A1 routes to a follow-up fix job (see Appendix A1 for the described hook: congested-state halo min-width/bump, ~8–10 congestion-bearing goldens re-bless, palcheck §7 re-pin, ODN-1-safe).
- **R2 (lane stripes) / R3 (Dublin blocks) / R4–R11 (intact rows) — no ruling queued**; the session closed with only R1's answer. The menu defaults (LEAVE / LEAVE / KEEP all) therefore stand as this report's recommendations, not user-confirmed rulings.

## Appendix: restore options (ranked, with risk — described, NOT implemented)

- **A1. Congested-link emphasis (restores the pulse READ; recommended if the user wants R1 back).** In `draw_bundles` (both branches), for `lvl != .None` draw the halo at `max(band + 5×scale, congestion_floor×scale)` with `congestion_floor ≈ 10–14 world px`, or bump the halo offset to `+8..+10×scale` for red. Effect: a congesting link visibly widens/warms again at every altitude — the "pulse" read returns without touching calm-board geometry or the covenant (the covenant caps the STROKE; the telegraph layer is emphasis). Risk: LOW-MED — re-bless the congestion-bearing goldens (warn ×3, juice/a11y@65s ×6, surge/estate_surge if engaged); palcheck §7 involved-non-recede legs may need re-pinned expectations; no sim/log bytes (ODN-1 safe).
- **A2. Ladder retune (partial band-factor return).** Raise `link_base_world` tables (e.g. ACCESS 4.5→7, CORE 3.5→5) or reintroduce a mild pooled-growth step. Restores overall link presence (R1 + general "links look lost" read) but softens the ruled scale covenant and re-blesses EVERY golden (all 49 demos have links). Risk: MED-HIGH — full corpus re-bless + the ruling itself; only with the user reversing the LOOK-SPEC widths.
- **A3. Lane stripes behind a default-off flag.** Restores the QoS lane read for zoomed play. Risk: LOW while off (byte-neutral), but contradicts the recorded laneless ruling and re-adds a surface the 08-26 ruling explicitly superseded; the caps data seam survives so implementation is a re-walk, not a rebuild.
- **A4. Dublin blocks return.** Risk: MED (Dublin golden churn, ruling reversal); information value already covered by sprites — not recommended.

## Evidence register

- Builds: rlsw harness at both commits (ODIN_ROOT → main checkout's shadow, read-only); AFTER corpus 49/49 green; palcheck green both (93/70 PASS lines).
- Strips: `harness motion-strip` warn 44000–46500/50 ms, warn 1000–3500/50 ms, juice 64000–66500/50 ms — both commits, T1-hash-verified timelines, 300 frames in `captures/strip_*/`.
- Key measurements: link centerline color series (steel×red → steel×amber at 44.4 s BOTH); link thickness 20 px vs 8 px const; ring-red 8-tick cycles; crisis-red 16-tick cycles; vivid-token counts (23,771/7,252 calm; 0/0 crisis); Dublin diff 0.86%.
- Severing commits: lane stripes `eb2e766`; Dublin blocks `5910ccd`; crisis-outline covenant `d5dd5a6`; halo draw: NO change in range.
- Code citations (AFTER @ 03dd6f8): view.odin:522 (draw_world), :994/:1071 (halo draws), :1161 (draw_health_ring), :769 (link_width_capped), :884 (PULSE16); crisis.odin:138 (crisis_desat_factor), :341 (draw_crisis_outlines), :384-390 (covenant hunk); assist.odin:494 (tie_dash_on); sprites.odin:244-306 (rung tables); camera.odin:259-306 (rungs); main.odin:1199 (set_reduced_motion), :1912 (pullback_feed). BEFORE equivalents at 088cf00 cited in F4/F9.


--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

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

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-congestion-read-a1/r2/security.json

The FILE is the deliverable, not your final chat message. Write the file NOW, compactly, without re-reading your work. A valid empty answer is the two-byte file: []
