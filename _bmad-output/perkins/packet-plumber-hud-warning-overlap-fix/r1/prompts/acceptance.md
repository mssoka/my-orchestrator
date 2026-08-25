# Acceptance Auditor lens — packet-plumber-hud-warning-overlap-fix r1

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
Read the shared context file at /Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/prompts/common_context.md — it contains the PR scope, the acceptance criteria (quoted below), the critical lens-guards, and what legitimate findings look like. It is binding for this review.

Acceptance criteria (verbatim from the job briefing):
1. Dragging an invalid link (e.g. terminal→terminal, span-exceeds-tier, self-loop) shows the red rejection AT the cursor — never at (12, 76).
2. The strain legend row renders clean at (12, 76) with no occlusion, in every run-mode state.
3. Collision sweep (prove in the PR body): enumerate ALL fixed-position `draw_text` y anchors in `app/main.odin` run mode (36, 56, 76, 96/114/132/156 selected-pipe block, bottom-left SLA rows, bottom-right assist rows) and show none overlap — a regression test if practical, a documented sweep otherwise.
4. Game-over mode untouched; the QoS toast (12, 156) untouched.
5. `odin test` + `harness run` green; **goldens MUST NOT shift** (verify no T2 capture shows the rejection; any shift = STOP and flag).

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Verification checklist you MUST perform in the worktree (each is a claim to confirm or refute):
- AC1: is the rejection draw call's anchor now `i32(cur.x)+12, i32(cur.y)-14` (cursor) and is the old `12, 76` rejection call GONE from the codebase? Grep for `12, 76` in app/main.odin — what remains at that anchor?
- AC2: is the strain legend still at `12, 76` and is `(12, 76)` now exclusively its anchor? (Any other draw targeting that exact anchor = a finding.)
- AC3: the PR body's sweep table — read the PR body (gh pr view 42 --repo solarity-services/Packet-Plumber) and check the enumerated fixed anchors against the ACTUAL `draw_text` calls in app/main.odin's draw_hud. Any fixed anchor omitted from the sweep or any overlap the sweep misses = a finding.
- AC4: game-over block + the QoS toast at `12, 156` — confirm the diff does not touch them (git show b3b8ded -- app/main.odin vs its parent).
- AC5: local suite — Perkins already ran `odin test core` (136/136) and `tools/harness.sh run` (18/18 PASS, byte-exact goldens) at the sha. You may re-verify if cheap, but do not re-run the full harness needlessly. Check whether any harness demo drives an invalid drag (a T2 golden that captures the rejection would have shifted — confirm none did).
- Lens-guards: ONE block in app/main.odin, no core/ touches, LOG_VERSION still 3 (core/serialize.odin), no new commands, no game-over/QoS-toast edits, em-dashes OK, missing win/lose UI is NOT a finding (in-flight 4.3 owns it).

--- OUTPUT ---
Write ONLY a valid JSON array to your output file: /Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/acceptance.json

No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.

Each element MUST match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. ac-violation, scope-drift, sweep-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words; reference the violated AC/constraint verbatim>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance. Therefore: open the file, read the relevant lines, do not guess from filenames or assume from similar-looking code. The `evidence` field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue — either verify it and report it crisply, or do not report it. Prefer fewer, well-grounded findings over many speculative ones. Accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
