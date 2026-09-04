You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks. Reading anything beyond the diff with your tools INVALIDATES this lens — do not open, read, grep, or list any file; the diff text itself is your entire world.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

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


--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

--- FILE OUTPUT CONTRACT (your deliverable) ---

When your analysis is complete, IMMEDIATELY write your final JSON array — and nothing else — to this exact path:

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-congestion-read-a1/r2/blind.json

The FILE is the deliverable, not your final chat message. Write the file NOW, compactly, without re-reading your work. A valid empty answer is the two-byte file: []
