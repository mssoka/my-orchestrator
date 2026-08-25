# Edge Case lens — packet-plumber-hud-warning-overlap-fix r1

You are reviewing a code diff. You have read-only access to the repository at the worktree `/Users/moses/.herdr/worktrees/packet-plumber/perkins-hud-warning-overlap-fix-r1` (detached at sha `b3b8ded` — verify all claims against THIS checkout, never origin) and may verify the diff's claims against the actual codebase using your available tools.

--- DIFF ---
diff --git a/app/main.odin b/app/main.odin
index 15250df..1bef316 100644
--- a/app/main.odin
+++ b/app/main.odin
@@ -826,15 +826,18 @@ draw_hud :: proc(app: ^App) {
 		}
 	}
 
-	// the cost readout on the drag ghost. Job B: in Full mode with a live
-	// route preview, the render draws the ONE route number instead (never two
-	// numbers at the cursor); Glow_Only shows no numbers at all; Off keeps the
-	// pre-Job-B readout.
+	// the cost/rejection readout on the drag ghost. Job B: in Full mode with
+	// a live route preview, the render draws the ONE route number instead
+	// (never two numbers at the cursor); Glow_Only shows no numbers at all;
+	// Off keeps the pre-Job-B readout. The rejection (invalid draw) anchors
+	// at the cursor too — mutually exclusive with the cost label by
+	// construction (valid vs invalid) — so it never collides with the
+	// strain-legend row at (12, 76).
 	if app.drag.active && app.drag_to != 0 {
+		cur := rnd.to_screen(&app.view, app.drag.wx, app.drag.wy)
 		if app.drag.valid != .None {
-			draw_text(app, reject_label(app.drag.valid), 12, 76, 16, rl.Color{200, 60, 60, 255})
+			draw_text(app, reject_label(app.drag.valid), i32(cur.x)+12, i32(cur.y)-14, 16, rl.Color{200, 60, 60, 255})
 		} else if app.assist_mode == .Off || (app.assist_mode == .Full && !(app.preview_live && app.preview.ok)) {
-			cur := rnd.to_screen(&app.view, app.drag.wx, app.drag.wy)
 			label := fmt.tprintf("cost %d", app.drag.cost)
 			draw_text(app, label, i32(cur.x)+12, i32(cur.y)-14, 16, p.ink)
 		}
--- END DIFF ---

--- SPEC / CONTEXT ---
Read the shared context file at /Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/prompts/common_context.md — it contains the PR scope, the acceptance criteria, the critical lens-guards, and what legitimate findings look like. It is binding for this review.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Relevant surfaces to trace (examples, not a fixed checklist): the hoisted `cur := rnd.to_screen(...)` now executes for BOTH branches (previously only the cost branch) — any new unhandled path from that? Cursor near the screen edges (text clipped at 0 or WIN_W/WIN_H)? `app.drag.wx/wy` values at the drag's start vs during drag (is the anchor still the drag ghost position the cost readout used — same semantics)? `app.drag.valid` enum values (does `.None`-checking cover all invalid states? is the rejection label correct per invalid reason)? The drag block's condition `app.drag.active && app.drag_to != 0` vs the rejection branch. NOTE the lens-guard: the rejection showing only while dragging an invalid link and the cost label only when valid (mutual exclusion) is the DESIGNED fix — verify it holds, do not re-litigate the cursor-anchor choice itself.

--- OUTPUT ---
Write ONLY a valid JSON array to your output file: /Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/edge.json

No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.

Each element MUST match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, off-by-one, state, clipping>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance. Therefore: open the file, read the relevant lines, do not guess from filenames or assume from similar-looking code. The `evidence` field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue — either verify it and report it crisply, or do not report it. Prefer fewer, well-grounded findings over many speculative ones. Accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
