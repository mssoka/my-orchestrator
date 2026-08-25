You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read project-context.md at the repository root (your cwd) for the full convention doc. Key conventions for this diff: Odin language, @(test) procs with testing.expect; this repo's PR convention bans em-dashes in test names/strings (comments are exempt); the repo is a game (Packet Plumber) with packages core/ (pure sim), app/ (game + tests), app/render/, harness/.

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

--- SPEC / CONTEXT ---
--- SPEC: PR #98 body (the user-authored PR under review — this IS the spec) ---
## What
Makes the camera RESTING-HOME wiring mutation-visible. Three new tests drive the REAL routing paths — start_run, effect_cancel, and the deselect else-branch of camera_set_selection — NOT a bare camera_set_default(&app) call. Removing any of the three camera_set_default(app) routing calls (main.odin:972/:1135/:1800) now turns the suite RED.

## Why
PR #97 established camera_set_default as the resting home, but the existing resting-home test calls camera_set_default directly (self-referential), so the wiring was mutation-invisible. Confirmed by deep-dive before this change.

## Verify
- odin test app: 46 green (43 baseline +3).
- odin test core: 261 green (unchanged). odin test app/render: 81 green (unchanged).
- Mutation-visibility proven: removing the routing call at start_run/:972, effect_cancel/:1135, and deselect/:1800 each fails the corresponding new test; all three removed = 3 failures. Legacy camera_set_default_homes_on_the_source_cluster stays green throughout.

Test-only change; camera logic, goldens, tools/ untouched. INTENDED for review; human merges.

--- SPEC: the PR #97 r1 B1 finding this PR fixes (review 5012533699) ---
B1 — Resting-home wiring unpinned (mutation-invisible call sites). app/main.odin:972,1135,1800. The headline behavior (resting home on boot/run-reset/deselect/ESC) is pinned only at the callee — pullback_test.odin:393 calls camera_set_default directly. Zero tests drive effect_cancel, start_run, or the selection-diff deselect (grep: comments only). Reverting any call site to camera_set_fit passes the entire suite (385 tests + 49 demos — the harness never runs app camera wiring). Fix: app-package tests driving the real entry points, asserting cam_zoom_to == DEFAULT_ZOOM / home anchor.

--- SCOPE NOTE (round scoping — do not violate) ---
This PR is a fix-forward for B1 ONLY. PR #97's B2/W1-W5 findings were that round's scope and are deliberately NOT addressed here; do not report them as blockers of THIS PR. The PR is TEST-ONLY: the diff must touch ONLY test files.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).

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
- Write ONLY your JSON array to the output file named below. No prose, no markdown fencing, no preamble in that file.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE OUTPUT (mandatory): write ONLY your JSON array to this exact absolute path (do not derive or alter it):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pr98-b1-wiring-pin/r1/acceptance.json
Then stop. Your turn ends after the file is written.
