You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/diff.patch
  (the canonical diff under review — 18 files, 2435 lines; the docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha 9094f45 — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/job-briefing.md (the job briefing — the spec; there is NO GitHub issue for this job)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/perkins-briefing-r3.md (the round briefing — its 'Lens-guards' section is part of the spec: the fix-audit targets + the user rulings on what NOT to re-litigate)

--- YOUR LENS (source tag: acceptance) ---

Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Round context (this is round 3 — a fix round). The r2 review (3 blockers + 10 warnings + 11 notes) claimed folds in the fix commit. Your audit priorities:

1. THE FIX-AUDIT BAR: the round briefing's 'Lens-guards' names the three r2 blockers as the fix-audit targets. Verify each fold ACTUALLY satisfies the r2 finding, not just cosmetically:
   - B1: does the off-center floor test (`camera_pullback_floor_pins_an_off_center_camera` in app/render/camera_test.odin) genuinely reproduce the r2 failure mode — a camera panned to the BOTTOM clamp at high zoom floor-clamping to 1.0 and ending centered? Check the fixture numbers against the clamp math in the worktree (world 1040x780, win 1280x720, fit = 720/780).
   - B2: is the NOC wheel-ownership policy truly ONE pinned decision (noc_panel_hit + camera_wheel_policy + the effect_zoom routing pins in pullback_test.odin)? Any branch left unpinned?
   - B3: the claimed composition pins — 7 yield clears (pullback_test.odin `pullback_yields_to_every_user_camera_input`), touch-pan deltas (`two_finger_pan_delivers_the_exact_screen_deltas`), latch lifecycle/stale predicate (`pan_latch_lifecycle_pins_stale_guard_and_modal_clear`), the modal strand (W1). Do the pins exist AND would they fail if the behavior regressed (non-vacuous)?
2. The PR body's fold table (in the diff, `_pr_body_camera_zoom.md`) vs the actual code — every "FIXED" claim must map to real hunks. N5/N8/N9/N10 are claimed as documented-divergences/out-of-scope rather than fixed — check those rulings against the r2 findings' substance.
3. Delta-introduced violations: does any fix hunk violate a spec rule (view-layer only; no gameplay-semantics change; harness golden safety; font/AA at zoom extremes — briefing scope item 6)?

NOT re-litigatable (user rulings — do NOT file these as findings): wheel zoom-to-point + drag pan as the input model; the [1.0 fit, 4.0] clamp band + conflict-free design; the auto-pullback on growth SEED (the mid-flight ruling itself); the zero-golden-drift hard bar (the harness pins the default camera by construction).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/acceptance.json

Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. spec-violation, coverage-gap>",
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

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is an fine and honest answer when nothing is wrong.
