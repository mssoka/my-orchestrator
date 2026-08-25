You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

ISOLATION RULE: reading any file beyond the diff below INVALIDATES your lens. Do not read, grep, or ls anything. The diff is your entire universe.

--- DIFF ---
diff --git a/app/pullback_test.odin b/app/pullback_test.odin
index 2d3adde..218e3bb 100644
--- a/app/pullback_test.odin
+++ b/app/pullback_test.odin
@@ -502,6 +502,75 @@ camera_set_default_homes_on_the_source_cluster :: proc(t: ^testing.T) {
 	testing.expect(t, app.pullback == false, "the home return clears an in-flight pullback")
 }
 
+// ---------------------------------------------------------------------------
+// PR #97 B1 — the RESTING-HOME WIRING pins (mutation-visible). The camera's
+// resting home is routed through THREE camera_set_default(app) call sites, and
+// the legacy test above only proves camera_set_default itself (it calls it
+// directly), so a removal of any ROUTING call went unnoticed. These tests drive
+// the REAL routing path — start_run (main.odin:972), effect_cancel
+// (main.odin:1135), and the deselect else-branch of camera_set_selection
+// (main.odin:~1800) — NOT a bare camera_set_default(&app) call, so that any
+// removal of a routing call turns the suite RED. NOTE: start_run clears pullback
+// via its destroy-then-reinit run-init independent of the camera routing, so
+// start_run_wiring_homes_on_the_source_cluster pins ONLY the routing (the
+// DEFAULT_ZOOM + source-cluster-home asserts) — it does NOT claim to pin
+// pullback-clear. The effect_cancel and deselect tests ARM pullback=true first
+// and do pin the clear.
+// ---------------------------------------------------------------------------
+
+@(test)
+start_run_wiring_homes_on_the_source_cluster :: proc(t: ^testing.T) {
+	app: App
+	pullback_test_app(&app)
+	defer pp.run_destroy(&app.state)
+	defer pp.catalogs_destroy(&app.cat)
+	app.run_live = true // the fixture already run_init'd State — take the clean destroy-then-reinit path
+	app.cat.balance.logic_hz = 20 // the boot wiring reads logic_hz for run_init
+	start_run(&app, 42)
+	testing.expect(t, app.cam_zoom_to == rnd.DEFAULT_ZOOM, "start_run routes the camera to the 2.0 cluster-default home")
+	testing.expect(t, app.cam_wx_to == app.home_wx && app.cam_wy_to == app.home_wy, "start_run homes the camera on the source cluster")
+}
+
+@(test)
+effect_cancel_wiring_homes_on_the_source_cluster :: proc(t: ^testing.T) {
+	app: App
+	pullback_test_app(&app)
+	defer pp.run_destroy(&app.state)
+	defer pp.catalogs_destroy(&app.cat)
+	app.cam_zoom = 4.0
+	app.cam_zoom_to = 4.0
+	app.cam_wx = 999
+	app.cam_wx_to = 999
+	app.cam_wy = 999
+	app.cam_wy_to = 999
+	app.pullback = true
+	effect_cancel(&app, &app.input)
+	testing.expect(t, app.cam_zoom_to == rnd.DEFAULT_ZOOM, "effect_cancel routes the camera to the 2.0 cluster-default home")
+	testing.expect(t, app.cam_wx_to == app.home_wx && app.cam_wy_to == app.home_wy, "effect_cancel homes the camera on the source cluster")
+	testing.expect(t, app.pullback == false, "effect_cancel's home return clears a pullback")
+}
+
+@(test)
+deselect_wiring_homes_on_the_source_cluster :: proc(t: ^testing.T) {
+	app: App
+	pullback_test_app(&app)
+	defer pp.run_destroy(&app.state)
+	defer pp.catalogs_destroy(&app.cat)
+	app.input.sel_node = -1
+	app.input.sel_pipe = -1
+	app.cam_zoom = 4.0
+	app.cam_zoom_to = 4.0
+	app.cam_wx = 999
+	app.cam_wx_to = 999
+	app.cam_wy = 999
+	app.cam_wy_to = 999
+	app.pullback = true
+	camera_set_selection(&app) // nothing selected -> the deselect else-branch homes
+	testing.expect(t, app.cam_zoom_to == rnd.DEFAULT_ZOOM, "a deselect routes the camera to the 2.0 cluster-default home")
+	testing.expect(t, app.cam_wx_to == app.home_wx && app.cam_wy_to == app.home_wy, "a deselect homes the camera on the source cluster")
+	testing.expect(t, app.pullback == false, "a deselect's home return clears a pullback")
+}
+
 @(test)
 pullback_eases_no_snap_and_converges :: proc(t: ^testing.T) {
 	app: App

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

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. [] is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose evidence cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in evidence. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

FILE OUTPUT (mandatory): write ONLY your JSON array to this exact absolute path (do not derive or alter it):
__LENSFILE__
Then stop. Your turn ends after the file is written.
