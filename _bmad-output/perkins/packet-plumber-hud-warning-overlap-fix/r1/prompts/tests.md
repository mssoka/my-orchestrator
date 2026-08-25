# Test Coverage lens — packet-plumber-hud-warning-overlap-fix r1

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

NOTE: the diff above is reproduced from the canonical diff bytes at /Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/diff.patch — the identical bytes every lens reviews. You may re-read that file to double-check any line.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Context specific to this review (verify, do not assume):
- The change is render-path only: a HUD `draw_text` anchor moved from a fixed position to the drag cursor. There is no new behavior to unit-test at the core level; the established test surface is `odin test core` (pure sim) + the golden harness (`tools/harness.sh run` — T1 state hashes + T2 pixel goldens) + the replay gate.
- The job briefing's AC3 says: "Collision sweep (prove in the PR body)… — a regression test if practical, a documented sweep otherwise." The PR body documents a sweep. Assess whether a regression test IS practical here (e.g. a harness demo that drives an invalid drag and captures a T2 pixel golden showing the rejection AT the cursor — is the capture path able to do that? check how harness demos drive input: harness/demos + harness/goldens.odin).
- Check whether any harness demo drives an invalid drag today; if none does, the rejection draw is untested at the golden layer — classify per the severity ladder, but remember the lens-guard: goldens MUST NOT shift, and no T2 capture shows the rejection (verified by Perkins: 18/18 PASS byte-exact).
- Perkins local verification: `odin test core` 136/136, harness 18/18 PASS.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Write ONLY a valid JSON array to your output file: /Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/tests.json

No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota (except the mandatory advisory-gate finding, which is always emitted).

Each element MUST match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap, golden-gap, coverage-gate>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance. Therefore: open the file, read the relevant lines, do not guess from filenames or assume from similar-looking code. The `evidence` field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue — either verify it and report it crisply, or do not report it. Prefer fewer, well-grounded findings over many speculative ones. Accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
