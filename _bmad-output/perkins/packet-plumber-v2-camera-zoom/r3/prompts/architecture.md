You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/diff.patch
  (the canonical diff under review — 18 files, 2435 lines; the docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha 9094f45 — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/job-briefing.md (the job briefing — the spec; there is NO GitHub issue for this job)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/perkins-briefing-r3.md (the round briefing — its 'Lens-guards' section is part of the spec: the fix-audit targets + the user rulings on what NOT to re-litigate)

--- YOUR LENS (source tag: architecture) ---

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Round context: this is round 3 — the r2 review's architecture findings were N1 (fit derivation triplicated — claimed fixed via camera_fit ONE source) and N11 (App.auto_pullback mirror — claimed fixed, the field deleted). The fix commit ADDED: camera_wheel_policy + noc_panel_hit hoisted OUT of the PP_DEBUG gate in noc_overlay.odin (four constants + two tiny procs ungated, 'the noc_level precedent'), the terminal-filtered camera_newest_terminals walk (W4), the same-window exclusion parameters on camera_spawn_is_seed (W7), and the wheel accumulator state on Input (W2). Audit those additions' architectural soundness with fresh eyes: does the ungating create a new leak of debug-surface concerns into release builds? Does the W7 window-exclusion API (two extra params, half-open id ranges) fit the layer, or is it feed-specific knowledge leaking into a pure predicate?

Architecture invariants to verify (from the project context — verify, do not assume):
- ODN-1 (core/ is pure — vendor:raylib only in app/; the sim never sees the camera). No core/ file may change; the SEED classification stays DERIVED on the view side.
- ODN-12 (the intent layer: device event → map → intent → executor → app effect hook). Policy (NOC-panel hit, modal block, clamps) lives in the app effect; the mapping carries raw data only; pure math lives in app/render/camera.odin (no App, no View, no raylib state).
- ODN-13 (no globals — everything off App/Input): the pullback state on App, the latch/accumulator on Input, NOT package globals.
- The "one consumer" rule for the wheel: effect_zoom owns the policy; no other GetMouseWheelMove reader in the app path.
- §10.4 no-transcendentals on the rasterized path (camera math: repeated multiplication, no pow).
- The harness-immunity architecture: pullback_feed + camera_update run ONLY in the app frame loop; the harness capture path never calls them.
- The zero-per-frame-heap-churn rule in the input poll (fixed move buffers; no per-frame allocations in the new poll code).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/architecture.json

Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coupling, layering>",
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
