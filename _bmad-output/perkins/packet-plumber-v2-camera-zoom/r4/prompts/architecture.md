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
Round 4 of PR #89. Round 3 found 2 blockers (R3-B1 pan clamped at live zoom; R3-B2 ungated D-key overlay toggle → release wheel dead-zone) + 8 warnings + 14 notes. Head af26d8a claims all folded. Prior findings: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/consolidated.json (still-present prior items are carry-forwards, not new discoveries).
NOT re-litigatable (user rulings): the gesture set; the [1.0, 4.0] clamp band; the auto-pullback feature; zero golden drift.

--- YOUR LENS (source tag: architecture) ---

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Round-specific architecture questions (from the round briefing — judge these, plus your own):

- The B2 gate placement: the fold gates `effect_overlay` (the effect) under `when #config(PP_DEBUG, false)` while the D-key MAPPING (app/input/mouse.odin) still emits Toggle_Overlay in release and the executor still routes it to a no-op. r3's suggested alternatives were gating the mapping or the exec case. Evaluate the CHOSEN point: does a release build still carry dead intent-routing (D → Toggle_Overlay → no-op)? Is that consistent with the codebase's other debug-gate precedents (noc_level, NOC_PANEL_* geometry ungated / behavior gated)? Is any OTHER writer of overlay_on left ungated (grep every `overlay_on` write in the worktree)?
- The `when #config(PP_DEBUG, false)` INSIDE a `#partial switch` case body (effect_zoom's .Noc_Scroll): per-build case bodies where release compiles to an EMPTY case + a fall-through comment. Is the construct the clearest expression of "release must never dead-zone"? Would a restructure (e.g. the policy returning .Zoom when the overlay can't exist in release) be simpler? Does the comment carry the invariant for the next reader?
- The N1 fold (camera_fit moved from main to render/rnd): ONE derivation now lives in app/render/camera.odin consumed by view_compute + camera_update + pullback_feed + camera_zoom_at + effect_pan. Import direction sound (main already imports rnd; render never imports main)? Any remaining inline fit derivation anywhere (grep for `min(` on win/world ratios)?
- Comment-integrity sweep of the r4-touched comments (r3 found the fixture-id comment disease — N14; audit the NEW comments' claims against the code's actual math):
  - app/render/camera.odin: the camera_zoom_step comment now reads "...(positive = in). of `delta` (positive = in)." — a duplicated tail introduced by the move hunk. Verify in the worktree.
  - app/pullback_test.odin pan_clamps mirror 1: the comment claims live-2.0 band "[195, 585]" — compute the REAL band from the fixture (world 64×36 tiles × 26px = 1664×936 px, win 1280×720, fit = 0.7692; at zoom 2.0 the y-band is world_h/2 ± (win_h/2)/(fit·2)) and check the comment.
  - mirror 2: the comment claims the anchor 700 "valid at 2.0: [278, 762]" while the same test asserts the band as [416, 1248] — at least one is wrong; compute the real band (world_w/2 ± (win_w/2)/(fit·2)) and flag the contradiction.
  - tools/ci-local.sh: the header + usage still say "all 10 gates" — the GATES array now has 11 entries (count them).
- ci-local.sh ↔ .github/workflows/ci.yml parity discipline (the repo rule: "the workflow is the spec; never edit one without the other") — the gate-9 edit added the PP_DEBUG test leg to BOTH: verify same command, same position.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/architecture.json

Each element must match this schema exactly:
{
  "source": "architecture",
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
