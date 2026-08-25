You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. You are a REVIEW LENS: you never fix, never push, never merge — findings only.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/diff.patch
  (the canonical diff under review — 22 files, 2682 lines; the two docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha af26d8a — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/job-briefing.md (the job briefing — the spec; there is NO GitHub issue for this job)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/perkins-briefing-r4.md (the round briefing — its 'Lens-guards' section is part of the spec: fix-audit targets + user rulings on what NOT to re-litigate)

--- ROUND CONTEXT (round 4 — FIX AUDIT) ---
Round 4 of PR #89. Round 3 (CHANGES_REQUESTED @9094f45) found 2 blockers — R3-B1: effect_pan clamped the pan TARGET at the LIVE zoom (targets converge at cam_zoom_to; camera_update never re-clamps); R3-B2: the ungated D-key set overlay_on in release builds, and the Noc_Scroll branch then dead-zoned the wheel — plus 8 warnings (incl. the vacuous W4 router pin, unpinned wheel band / pan values / ease-rate band) and 14 notes. Head af26d8a claims ALL folded. The prior findings live at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/consolidated.json
(report a still-present prior item as a carry-forward, not as a brand-new discovery)
NOT re-litigatable (user rulings — never flag as violations): wheel zoom-to-point + drag pan as the gesture set; the [1.0 fit, 4.0] clamp band + conflict-free design; the auto-pullback feature (mid-flight ruling, folded as ruled); zero golden drift (the harness pins the default camera).

--- YOUR LENS (source tag: edge) ---

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Round-specific paths (from the round briefing — walk these mechanically, plus any others you derive):

- effect_pan (B1 fold — the TARGET-zoom clamp): mid-ease composition — the delta converts at the LIVE zoom (cam_zoom) while the clamp validates at cam_zoom_to; walk BOTH mirrors (zoom-out ease live 2.0→target 1.0: the fit-floor pin; zoom-in ease live 1.0→target 2.0: the anchor preservation). A pan arriving the SAME frame the pullback retargets cam_zoom_to (order of writes); successive pans mid-ease (each re-clamps at the CURRENT cam_zoom_to — target moves under the ease); pan at cam_zoom_to == 1.0 exactly (pan is claimed a no-op at the fit floor — verify the clamp actually pins, incl. the wx axis while wy wants to move); float equality at the clamp boundary (target exactly at band edge ± conversion epsilon); dx/dy = 0,0 (the mirror-2 pin relies on a zero-delta pan re-clamping — is a 0,0 pan reachable from real input?).
- effect_zoom (B2 fold — the fall-through): trace the `when #config(PP_DEBUG, false)` INSIDE the `#partial switch` case .Noc_Scroll in BOTH builds — release: the case body compiles empty, control exits the switch, the zoom body below runs (verify the actual control flow — the zoom body is after the switch, reachable); debug: scroll + return. delta SIGN at the noc_scroll write (max(0, noc_scroll - i32(delta)) — a fractional delta truncates toward zero; a negative delta over the panel); noc_scroll already 0 (clamped); the policy's precedence (pointer over panel + modal open — which case wins).
- effect_overlay (B2 fold — the gated toggle): release D-key → the Toggle_Overlay intent still fires + routes to a no-op effect (any other consumer of the intent? the executor's recording hook? anything that reads overlay_on in release builds — the wheel policy takes it as an arg); PP_DEBUG builds unchanged.
- The W4 walk (seed-then-router): the newest-first walk starts at the NEWEST id (the router) and must skip it via the kind filter — walk the ids: router id consumed with NO event; the seed OLDER with the event; a second router after the seed; the seed as the OLDEST id inside the window (found == n at the last probe); >8 spawn events in one slice (the ids: [8]u32 cap — found != n_spawns -> return: r3 W3 carry-forward — still present?); terminals that died between event and feed; window_lo/window_hi when n_spawns == 1.
- The ease-rate pin loop: `for app.pullback && frames < 300` — non-convergence paths (rate regressed → exits with pullback armed → the !pullback expect fails: good); camera_update's pullback-clear predicate (zoom == zoom_to && wx == wx_to && wy == wy_to — float equality: can it stall just-off or clear early on partial convergence?).
- The wheel-band pin (effect_zoom delta ±20): camera_zoom_step integer-notch repeated multiply (1.25^20, 1.25^-20 — precision at the clamp boundary; clamp() at exactly CAM_ZOOM_MIN/MAX); the test's state coupling (the band legs leave cam_zoom_to at 1.0 before the pan leg resets to 2.0 manually).
- Carry-forward edges from r3 (verify still-present or fixed): W2 (the pullback_yields app7 leg drives effect_settings_adjust on a zeroed App → real-HOME settings write), W3 (the [8]u32 cap), W4 (same-window exclusion vs terminal_spawn_interval_ticks), N10 (wheel residue pre-charge when consumed as Noc_Scroll/Blocked).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/edge.json

Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not push. You are a reviewer.

ACCURACY MANDATE — the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
