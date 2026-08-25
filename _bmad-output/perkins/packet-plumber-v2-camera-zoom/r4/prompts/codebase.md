You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. You are a REVIEW LENS: you never fix, never push, never merge — findings only.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/diff.patch
  (the canonical diff under review — 22 files, 2682 lines; the two docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha af26d8a — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/job-briefing.md
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/perkins-briefing-r4.md

--- ROUND CONTEXT (round 4 — FIX AUDIT) ---
Round 4 of PR #89. Round 3 found 2 blockers + 8 warnings + 14 notes; head af26d8a claims all folded. Prior findings: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/consolidated.json (still-present prior items are carry-forwards, not new discoveries).

--- YOUR LENS (source tag: codebase) ---

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Round-specific reality checks (verify each in the worktree):

- The camera_fit move (N1): app/render/camera.odin defines `camera_fit` (package render) and app/main.odin's local copy is REMOVED — grep package main for any remaining bare `camera_fit(` call or definition (a leftover would be a compile error — the code must build; verify anyway), and confirm every former caller now says `rnd.camera_fit` (camera_update, pullback_feed, camera_zoom_at, effect_pan) and view_compute calls the package-local one.
- The `defer free(ictx.view)` additions (N6/N7 fold): read cam_test_ctx in app/input/camera_input_test.odin — is the View allocated with `new(...)` (free is correct) or `make(...)` (would need delete)? Are ALL tests that use cam_test_ctx covered — count the cam_test_ctx call sites vs the 6 added defers; any test missed? Does destroy(&ictx) ALSO free the view (double-free risk — read the destroy proc)?
- touch.odin's header (N7): does the new wording match types.odin's Pan comment + exec.odin's routing (no contradictions left anywhere — grep for "no-op" mentions of Pan)?
- ci.yml ↔ ci-local.sh gate 9 parity: read both files; the ci-local gate 9 command is `odin build app -define:PP_DEBUG=true -out:app-debug.bin && odin build harness -define:PP_DEBUG=true -out:bin/harness-debug && odin test app -define:PP_DEBUG=true -out:bin/app-debug-test` — is the ci.yml PP_DEBUG step the SAME three commands, in the same workflow position (before the stats-check step)?
- PR-body counts vs reality (r3 N3 flagged this drift TWICE): the body's Verification section claims "4 camera-math tests + 4 input wiring tests + 4 pullback tests + 2 settings tests" — count the actual @(test) procs in app/render/camera_test.odin, app/input/camera_input_test.odin, app/pullback_test.odin, app/settings_test.odin in the worktree and reconcile (the r4 commit ADDED 3 pullback tests + 1 more — the claim should now read 9 + 7 + 10 + 2 if the r3 reality was 9 + 7 + 7 + 2).
- The capture assets: docs/captures/v2-camera-zoom/zoom-00-fit.png and zoom-01-zoomed-panned.png — `shasum -a 256` both; the PR body claims shas "63524a77" (fit) and "3b28c414" (zoomed). The zoomed png CHANGED in this round (72755 → 72584 bytes in the diff) — if the body still cites the OLD sha for the NEW bytes, that is a stale-claim finding (mechanical, hash-based — quote both).
- Orphan sweep: anything defined in the diff but unreferenced (e.g. NOC_ROW_H, Wheel_Target enum members, camera_newest_terminals callers), anything referenced but undefined.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/codebase.json

Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not push. You are a reviewer.

ACCURACY MANDATE: every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Open the file, read the lines, paste them verbatim in `evidence`. Hedging ("might", "could") means you have not verified — drop it. Accuracy > volume.
