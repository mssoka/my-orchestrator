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
diff --git a/app/render/look_l1_test.odin b/app/render/look_l1_test.odin
index 38f22b3..9fbd921 100644
--- a/app/render/look_l1_test.odin
+++ b/app/render/look_l1_test.odin
@@ -249,6 +249,53 @@ single_strokes_sit_in_the_covenant_band :: proc(t: ^testing.T) {
 	}
 }
 
+// --- the congested-emphasis floor (A1, 2026-08-27 user ruling) ---------------
+
+@(test)
+congestion_halo_floor_is_the_ruled_a1_band :: proc(t: ^testing.T) {
+	// viscomm-audit restore option A1: the emphasis floor is tuned within the
+	// blessed 10-14 world-px band (the appendix's envelope; a value outside
+	// it is an unruled retune and fails HERE before it can shift a golden).
+	testing.expect(t, CONGESTION_HALO_FLOOR_WORLD >= 10.0 && CONGESTION_HALO_FLOOR_WORLD <= 14.0,
+		"the congested-halo floor left the A1 envelope (10-14 world px)")
+}
+
+@(test)
+congested_halo_width_law_floors_at_every_rung :: proc(t: ^testing.T) {
+	// the A1 law: halo = max(classic +5 bump, floor) in screen px. At every
+	// rung the congested halo must clear the floor (the read the audit
+	// demanded), never shrink below the classic bump (emphasis is
+	// ADDITIVE — a floor below the bump would THIN a fat bundle's halo).
+	// Representative band values = the covenant stroke at each rung
+	// (standard tier: 3.5 world @ Core/Distribution, 4.5 @ Access; screen
+	// = world x scale with scale = fit x zoom per rung).
+	pairs := [6]struct {
+		band, scale: f32,
+		rung:         string,
+	}{
+		{3.5, 1.0, "Core fit"},
+		{3.5, 1.4, "Distribution"},
+		{4.5, 2.0, "Access rest"},
+		{6.0, 1.0, "Core wide backbone"},
+		{9.0, 2.0, "Access fat bundle (pre-clamp)"},
+		{24.0, 1.0, "clamped fat ribbon (well over the floor)"},
+	}
+	for p in pairs {
+		w := congested_halo_width(p.band, p.scale)
+		expect_f32(t, w, max(p.band + 5.0 * p.scale, CONGESTION_HALO_FLOOR_WORLD * p.scale))
+		testing.expectf(t, w >= CONGESTION_HALO_FLOOR_WORLD * p.scale - 1e-4,
+			"congested halo %.2f at %s sits under the floor (a deleted floor fails here)", w, p.rung)
+		testing.expectf(t, w >= p.band + 5.0 * p.scale - 1e-4,
+			"congested halo %.2f at %s thinned below the classic +5 bump (the floor must be additive)", w, p.rung)
+	}
+	// the read at the three rungs (the audit's table, restored): floor
+	// engages at Core fit (8.5 -> 12) and Distribution (11.9 -> 16.8);
+	// Access keeps its classic bump only when it clears the floor.
+	expect_f32(t, congested_halo_width(3.5, 1.0), 12.0)
+	expect_f32(t, congested_halo_width(3.5, 1.4), CONGESTION_HALO_FLOOR_WORLD * 1.4)
+	expect_f32(t, congested_halo_width(4.5, 2.0), 24.0) // max(9+10, 24) at scale 2 — LITERALS, not the law restated
+}
+
 // --- helpers -------------------------------------------------------------------
 
 // look_l1_set_puck_bboxes — hand-set the puck content widths (the sprite
diff --git a/app/render/view.odin b/app/render/view.odin
index 0d76aa5..55707b3 100644
--- a/app/render/view.odin
+++ b/app/render/view.odin
@@ -661,6 +661,11 @@ fceil :: proc(f: f32) -> i32 {
 
 // --- LOOK §3: the scale covenant + the laneless link language (ruled) ----
 //
+// [AMENDED 2026-08-27, viscomm-audit A1 user ruling] the congested-emphasis
+// layer (CONGESTION_HALO_FLOOR_WORLD, lvl != .None halos only) is TELEGRAPH
+// emphasis, NOT a covenant change — the covenant caps the STROKE; calm
+// boards stay byte-identical.
+//
 // [ADOPTED 2026-08-26 user ruling] Links are SINGLE SOLID LANELESS strokes
 // (the 3.3 spatial-lane stripes are superseded — queues are ingress/egress
 // on ROUTERS, the road doesn't gossip), and ONE ratio law holds at every
@@ -699,6 +704,27 @@ LINK_RATIO_CAP :: f32(0.5)
 // nodes before the covenant clamp even engages).
 LINK_EXTRA_W :: [3]f32{2.0, 1.5, 1.25} // [Access, Distribution, Core]
 
+// CONGESTION_HALO_FLOOR_WORLD — the congested-state emphasis floor (world
+// px; viscomm-audit restore option A1, USER RULING 2026-08-27): a link's
+// CONGESTION HALO never renders thinner than this, however thin the
+// covenant stroke under it has become. This is a TELEGRAPH-layer floor, not
+// a geometry change — the covenant (LINK_RATIO_CAP) caps the STROKE and is
+// untouched; calm boards (lvl == .None) draw byte-identical (the halo only
+// exists when lvl != .None). Restores the pre-L1 read where a congesting
+// link visibly widened under its recolor: the L1 laneless ruling thinned
+// the strokes 3.6-5.1x under the (code-identical) halo, collapsing the
+// telegraph's canvas ~4-6x (viscomm-regression-audit F4/R1).
+CONGESTION_HALO_FLOOR_WORLD :: f32(12.0)
+
+// congested_halo_width — the A1 emphasis law, ONE derivation for both
+// draw_bundles branches (a restated copy drifts the look between the
+// blessed inline path and the routed variant): the halo keeps the classic
+// +5 world-px emphasis bump, floored at CONGESTION_HALO_FLOOR_WORLD so the
+// emphasis stays legible at every rung altitude.
+congested_halo_width :: proc(band_screen, scale: f32) -> f32 {
+	return max(band_screen + 5.0 * scale, CONGESTION_HALO_FLOOR_WORLD * scale)
+}
+
 // link_base_world — the single-stroke base width for (rung, tier id)
 // (world px; tier id keyed, catalog-order-immune). ACCESS/DISTRIBUTION are
 // uniform across tiers (hue carries the tier — the ruled mock); CORE
@@ -1001,7 +1027,7 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 					u8(f32(raw.b) * 0.57 + f32(halo.b) * 0.43),
 					255,
 				}
-				w := band + 5.0 * v.scale
+				w := congested_halo_width(band, v.scale)
 				rl.DrawLineEx(a, b, w, halo)
 				rl.DrawCircleV(a, w * 0.5, halo)
 				rl.DrawCircleV(b, w * 0.5, halo)
@@ -1078,7 +1104,7 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 				u8(f32(raw.b) * 0.57 + f32(halo.b) * 0.43),
 				255,
 			}
-			w := band + 5.0 * v.scale
+			w := congested_halo_width(band, v.scale)
 			draw_path_band(v, &path, w, halo)
 		}
 	}
diff --git a/goldens/a11y_deutan/30000ms.png b/goldens/a11y_deutan/30000ms.png
index 2ac079e..daf8d1f 100644
Binary files a/goldens/a11y_deutan/30000ms.png and b/goldens/a11y_deutan/30000ms.png differ
diff --git a/goldens/a11y_deutan/65000ms.png b/goldens/a11y_deutan/65000ms.png
index 0af03fc..dff5204 100644
Binary files a/goldens/a11y_deutan/65000ms.png and b/goldens/a11y_deutan/65000ms.png differ
diff --git a/goldens/a11y_protan/30000ms.png b/goldens/a11y_protan/30000ms.png
index 2ac079e..daf8d1f 100644
Binary files a/goldens/a11y_protan/30000ms.png and b/goldens/a11y_protan/30000ms.png differ
diff --git a/goldens/a11y_protan/65000ms.png b/goldens/a11y_protan/65000ms.png
index 0af03fc..dff5204 100644
Binary files a/goldens/a11y_protan/65000ms.png and b/goldens/a11y_protan/65000ms.png differ
diff --git a/goldens/a11y_reduced/30000ms.png b/goldens/a11y_reduced/30000ms.png
index 284328f..69e214f 100644
Binary files a/goldens/a11y_reduced/30000ms.png and b/goldens/a11y_reduced/30000ms.png differ
diff --git a/goldens/a11y_reduced/65000ms.png b/goldens/a11y_reduced/65000ms.png
index a88e327..687d21b 100644
Binary files a/goldens/a11y_reduced/65000ms.png and b/goldens/a11y_reduced/65000ms.png differ
diff --git a/goldens/a11y_scale/30000ms.png b/goldens/a11y_scale/30000ms.png
index 3b66fb0..57c29fd 100644
Binary files a/goldens/a11y_scale/30000ms.png and b/goldens/a11y_scale/30000ms.png differ
diff --git a/goldens/a11y_scale/65000ms.png b/goldens/a11y_scale/65000ms.png
index 590a856..e5cedfd 100644
Binary files a/goldens/a11y_scale/65000ms.png and b/goldens/a11y_scale/65000ms.png differ
diff --git a/goldens/a11y_tritan/30000ms.png b/goldens/a11y_tritan/30000ms.png
index ee7e9d0..0a01773 100644
Binary files a/goldens/a11y_tritan/30000ms.png and b/goldens/a11y_tritan/30000ms.png differ
diff --git a/goldens/a11y_tritan/65000ms.png b/goldens/a11y_tritan/65000ms.png
index 9a51dbd..f895f9c 100644
Binary files a/goldens/a11y_tritan/65000ms.png and b/goldens/a11y_tritan/65000ms.png differ
diff --git a/goldens/advance_block_sla/15000ms.png b/goldens/advance_block_sla/15000ms.png
index 6fcd680..4e3bf09 100644
Binary files a/goldens/advance_block_sla/15000ms.png and b/goldens/advance_block_sla/15000ms.png differ
diff --git a/goldens/advance_block_sla/60000ms.png b/goldens/advance_block_sla/60000ms.png
index 4c797ae..4d63f91 100644
Binary files a/goldens/advance_block_sla/60000ms.png and b/goldens/advance_block_sla/60000ms.png differ
diff --git a/goldens/advance_fire/60000ms.png b/goldens/advance_fire/60000ms.png
index a09ae69..c9c77dd 100644
Binary files a/goldens/advance_fire/60000ms.png and b/goldens/advance_fire/60000ms.png differ
diff --git a/goldens/health_lose/21000ms.png b/goldens/health_lose/21000ms.png
index cdb2256..763ce63 100644
Binary files a/goldens/health_lose/21000ms.png and b/goldens/health_lose/21000ms.png differ
diff --git a/goldens/health_lose/23000ms.png b/goldens/health_lose/23000ms.png
index d2045b9..55eba94 100644
Binary files a/goldens/health_lose/23000ms.png and b/goldens/health_lose/23000ms.png differ
diff --git a/goldens/juice/30000ms.png b/goldens/juice/30000ms.png
index 284328f..69e214f 100644
Binary files a/goldens/juice/30000ms.png and b/goldens/juice/30000ms.png differ
diff --git a/goldens/juice/65000ms.png b/goldens/juice/65000ms.png
index 4ff330f..a3a2653 100644
Binary files a/goldens/juice/65000ms.png and b/goldens/juice/65000ms.png differ
diff --git a/goldens/legacy_decay/60000ms.png b/goldens/legacy_decay/60000ms.png
index a09ae69..c9c77dd 100644
Binary files a/goldens/legacy_decay/60000ms.png and b/goldens/legacy_decay/60000ms.png differ
diff --git a/goldens/pause/65000ms.png b/goldens/pause/65000ms.png
index dc25f24..aac8f95 100644
Binary files a/goldens/pause/65000ms.png and b/goldens/pause/65000ms.png differ
diff --git a/goldens/pause/80000ms.png b/goldens/pause/80000ms.png
index df2988e..850eeb1 100644
Binary files a/goldens/pause/80000ms.png and b/goldens/pause/80000ms.png differ
diff --git a/goldens/qos/65000ms.png b/goldens/qos/65000ms.png
index 3c52358..e5443bc 100644
Binary files a/goldens/qos/65000ms.png and b/goldens/qos/65000ms.png differ
diff --git a/goldens/qos_contention/01000ms.png b/goldens/qos_contention/01000ms.png
index 9751419..f8331dd 100644
Binary files a/goldens/qos_contention/01000ms.png and b/goldens/qos_contention/01000ms.png differ
diff --git a/goldens/qos_contention/03000ms.png b/goldens/qos_contention/03000ms.png
index 3c9dd36..d45d581 100644
Binary files a/goldens/qos_contention/03000ms.png and b/goldens/qos_contention/03000ms.png differ
diff --git a/goldens/qos_contention/10000ms.png b/goldens/qos_contention/10000ms.png
index f36d31c..2bd1747 100644
Binary files a/goldens/qos_contention/10000ms.png and b/goldens/qos_contention/10000ms.png differ
diff --git a/goldens/qos_emphasis/12000ms.png b/goldens/qos_emphasis/12000ms.png
index 12ab5d9..4f43eac 100644
Binary files a/goldens/qos_emphasis/12000ms.png and b/goldens/qos_emphasis/12000ms.png differ
diff --git a/goldens/sla/01000ms.png b/goldens/sla/01000ms.png
index 55cc846..a400a6c 100644
Binary files a/goldens/sla/01000ms.png and b/goldens/sla/01000ms.png differ
diff --git a/goldens/sla/04000ms.png b/goldens/sla/04000ms.png
index 81e1e28..49f386e 100644
Binary files a/goldens/sla/04000ms.png and b/goldens/sla/04000ms.png differ
diff --git a/goldens/sla/10000ms.png b/goldens/sla/10000ms.png
index 2438b35..88cd60b 100644
Binary files a/goldens/sla/10000ms.png and b/goldens/sla/10000ms.png differ
diff --git a/goldens/surge/30000ms.png b/goldens/surge/30000ms.png
index 42790c7..ce63e9c 100644
Binary files a/goldens/surge/30000ms.png and b/goldens/surge/30000ms.png differ
diff --git a/goldens/surge/65000ms.png b/goldens/surge/65000ms.png
index ec35489..d54f1f2 100644
Binary files a/goldens/surge/65000ms.png and b/goldens/surge/65000ms.png differ
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
index 3a0a706..9095768 100644
Binary files a/goldens/terminal_types/05000ms.png and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
index 8b762d0..e7cb8f5 100644
Binary files a/goldens/terminal_types/30000ms.png and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/warn/45000ms.png b/goldens/warn/45000ms.png
index 6a0bda7..cfd7de1 100644
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
index 36d5d04..be9153c 100644
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
@@ -1307,6 +1320,170 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		pp.run_destroy(&state)
 	}
 
+	// --- 8. the congested-emphasis floor (A1, 2026-08-27 user ruling) ------
+	// viscomm-audit restore option A1: a congesting link's HALO never draws
+	// thinner than CONGESTION_HALO_FLOOR_WORLD, however thin the covenant
+	// stroke under it (the telegraph layer is emphasis, not geometry — the
+	// covenant caps the STROKE and is untouched). The mutation legs run at
+	// DEV time (delete the floor from congested_halo_width -> (a)/(b) go
+	// RED at exactly the old band+5 widths; restore -> GREEN). The CALM leg
+	// (c) is the covenant companion: without congestion the stroke draws at
+	// exactly the capped band and NO halo exists — a floor that leaks into
+	// calm draws fails it. Live analysis frames like section 7 — the golden
+	// capture path never renders this fixture.
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
+			// .None (mirroring warnings' own re-init) so a fixture extension
+		// can never measure allocator garbage.
+		testing_lvl_ok := ok_ps && found_bi
+		if testing_lvl_ok && int(ps8) >= len(state.crisis.pipe_congestion) {
+			old_len := len(state.crisis.pipe_congestion)
+			resize(&state.crisis.pipe_congestion, int(ps8) + 1)
+			for i in old_len..<len(state.crisis.pipe_congestion) {
+				state.crisis.pipe_congestion[i] = .None
+			}
+		}
+		view.scale = 2.0
+		view.zoom_rung = .Access // scale 2.0 absolute — the §7 camera (bands wide, clean sampling)
+		view.reduced_motion = false
+		view.off_x = f32(view.win_w) / 2 - f32(8) * view.tile_px * view.scale
+		view.off_y = f32(view.win_h) / 2 - f32(12) * view.tile_px * view.scale
+		mid8 := rnd.node_screen(&view, {8, 12})  // the band's midpoint column
+		capa8 := rnd.node_screen(&view, {4, 12}) // an END-CAP column (the halo's endpoint circle — a mid-column-only scan can't see a cap leak)
+		floor_px := int(rnd.CONGESTION_HALO_FLOOR_WORLD * view.scale) // 24 px at scale 2
+		band_px := int(rnd.link_width_capped(&view, &state.topology, &state.bundles, bi8) * view.scale)
+		check(testing_lvl_ok && perr8 == .None,
+			fmt.aprintf("section-8 premise: the fixture resolves (pipe err %v, bundle found %v)", perr8, found_bi), int(ps8))
+		// the mutation-premise pin: the delete-the-bump leg can only FAIL when
+		// the floor DOMINATES the classic +5 bump at this rung — a future
+		// ladder raise that pushes band+5·scale past the floor bound would
+		// silently vacate legs (a)/(b) (the pin that can't fail is vacuous).
+		check(band_px + int(5.0 * view.scale) < floor_px-3,
+			fmt.aprintf("section-8 premise: the floor dominates the +5 bump here (bump %d vs floor bound %d — a ladder raise just vacated the mutation legs; move the fixture to a thinner rung)", band_px + int(5.0 * view.scale), floor_px-3), band_px)
+
+		// the shared file-scope scan_col_v does the measuring (§7 parity —
+		// a vertical cut at the band midpoint, clear of the end-caps).
+
+		// the draw's own blend math — the palette tokens are the source of
+		// truth (never hardcoded hexes here; a palette retune re-derives).
+		steel8 := view.palette.pipe_steel
+		halo_blend :: proc(raw, state_col: rl.Color) -> rl.Color {
+			return rl.Color{
+				u8(f32(raw.r) * 0.57 + f32(state_col.r) * 0.43),
+				u8(f32(raw.g) * 0.57 + f32(state_col.g) * 0.43),
+				u8(f32(raw.b) * 0.57 + f32(state_col.b) * 0.43),
+				255,
+			}
+		}
+		render8 :: proc(view: ^rnd.View, state: ^pp.Run_State) -> rl.Image {
+			rl.BeginDrawing()
+			rl.ClearBackground(rl.Color{237, 226, 200, 255})
+			rnd.draw_world(view, &state.topology, &state.bundles, &state.flow, &state.crisis, 100, {}, -1, -1, state.seed)
+			rl.EndDrawing()
+			img := rl.LoadImageFromScreen()
+			normalize(&img)
+			return img
+		}
+
+		// (a) AMBER: the halo clears the floor at the draw path
+		if testing_lvl_ok {
+			state.crisis.pipe_congestion[ps8] = .Amber
+			img := render8(&view, &state)
+			want := halo_blend(steel8, view.palette.state_congested)
+			n_amber := scan_col_v(img, int(mid8.x), int(mid8.y), floor_px, want, 10)
+			check(n_amber >= floor_px - 3 && n_amber <= floor_px + 6,
+				fmt.aprintf("congested halo clears the A1 floor (measured %d px, floor %d, band %d — a deleted floor measures ~band+5·scale and fails)", n_amber, floor_px, band_px), n_amber)
+			rl.UnloadImage(img)
+		}
+
+		// (b) RED: the same floor, the critical blend
+		if testing_lvl_ok {
+			state.crisis.pipe_congestion[ps8] = .Red
+			img := render8(&view, &state)
+			want := halo_blend(steel8, view.palette.state_critical)
+			n_red := scan_col_v(img, int(mid8.x), int(mid8.y), floor_px, want, 10)
+			check(n_red >= floor_px - 3 && n_red <= floor_px + 6,
+				fmt.aprintf("critical halo clears the A1 floor (measured %d px, floor %d)", n_red, floor_px), n_red)
+			rl.UnloadImage(img)
+		}
+
+		// (c) CALM: no congestion -> the stroke at exactly the capped band,
+		// zero halo pixels (the covenant companion — the floor never leaks
+			// into a calm board's draw)
+		if testing_lvl_ok {
+			state.crisis.pipe_congestion[ps8] = .None
+			img := render8(&view, &state)
+			amber8 := halo_blend(steel8, view.palette.state_congested)
+			red8 := halo_blend(steel8, view.palette.state_critical)
+			n_stroke := scan_col_v(img, int(mid8.x), int(mid8.y), floor_px, steel8, 10)
+			n_halo_leak := scan_col_v(img, int(mid8.x), int(mid8.y), floor_px, amber8, 10) + scan_col_v(img, int(mid8.x), int(mid8.y), floor_px, red8, 10)
+			n_cap_leak := scan_col_v(img, int(capa8.x), int(capa8.y), floor_px, amber8, 10) + scan_col_v(img, int(capa8.x), int(capa8.y), floor_px, red8, 10)
+			check(n_stroke >= band_px - 3 && n_stroke <= band_px + 3 && n_halo_leak == 0 && n_cap_leak == 0,
+				fmt.aprintf("calm stroke draws at exactly the covenant band (stroke %d px, band %d, halo leak %d, end-cap leak %d — a floor leak fails here)", n_stroke, band_px, n_halo_leak, n_cap_leak), n_stroke)
+			rl.UnloadImage(img)
+		}
+
+		// (d)+(e): the ROUTED branch — the "ONE look" invariant is a PIN,
+		// not a comment. The routed call site (draw_path_band) must measure
+			// the same floored width (delete-the-bump on EITHER call site fails
+		// here), and the routed CALM draw must stay halo-free.
+		{
+			sv_rw := view.route_wires
+			defer view.route_wires = sv_rw
+			view.route_wires = true
+
+			state.crisis.pipe_congestion[ps8] = .Amber
+			img := render8(&view, &state)
+			want := halo_blend(steel8, view.palette.state_congested)
+			n_routed := scan_col_v(img, int(mid8.x), int(mid8.y), floor_px, want, 10)
+			check(n_routed >= floor_px - 3 && n_routed <= floor_px + 6,
+				fmt.aprintf("routed halo clears the A1 floor (measured %d px, floor %d — a routed-branch drift or deleted floor fails here)", n_routed, floor_px), n_routed)
+			rl.UnloadImage(img)
+
+			state.crisis.pipe_congestion[ps8] = .None
+			img2 := render8(&view, &state)
+			n_routed_leak := scan_col_v(img2, int(mid8.x), int(mid8.y), floor_px, want, 10)
+			check(n_routed_leak == 0,
+				fmt.aprintf("routed calm draw stays halo-free (leak %d px — a floor leak into the routed branch fails here)", n_routed_leak), n_routed_leak)
+			rl.UnloadImage(img2)
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
## Spec file 1: the job briefing (the claims under review)
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


## Spec file 2: the viscomm regression audit — THE ACCEPTANCE CRITERIA (R1 row, "Rulings received", Appendix A1, evidence register)
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
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

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

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-congestion-read-a1/r1/acceptance.json

The FILE is the deliverable, not your final chat message. Write the file NOW, compactly, without re-reading your work. A valid empty answer is the two-byte file: []
