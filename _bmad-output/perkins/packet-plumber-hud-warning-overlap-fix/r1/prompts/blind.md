# Blind Hunter lens — packet-plumber-hud-warning-overlap-fix r1

You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

**BLINDNESS CONTRACT:** the diff below is ALL the context you may use. Do NOT read the worktree, the repo, the specs, or any other file — reading anything beyond this diff INVALIDATES your lens and your findings will be discarded.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

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

## OUTPUT CONTRACT (follow exactly)

Write ONLY a valid JSON array to your output file: /Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/blind.json

No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.

Each element MUST match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. anchor-math, control-flow, invariant, dead-code>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff. Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
