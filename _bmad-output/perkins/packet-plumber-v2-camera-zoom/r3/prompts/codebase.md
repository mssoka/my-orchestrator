You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/diff.patch
  (the canonical diff under review — 18 files, 2435 lines; the docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha 9094f45 — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/job-briefing.md (the job briefing — the spec; there is NO GitHub issue for this job)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/perkins-briefing-r3.md (the round briefing — its 'Lens-guards' section is part of the spec: the fix-audit targets + the user rulings on what NOT to re-litigate)

--- YOUR LENS (source tag: codebase) ---

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Round context (round 3, fix commit 9094f45). Codebase-fit targets to verify:
- The W4 fold claims the terminal-filtered walk (`camera_newest_terminals`) is exact because "growth spawns are terminals ONLY, fast-path placements are junctions ONLY" — verify that doctrine in core/ (the growth director + apply_place): is there ANY terminal spawn path that bypasses NODE_SPAWNED, or any junction-with-event path that would corrupt the n-spawn→ids mapping? Compare with the spawn_fx.odin walk it diverges from (N5 ruling: intentional divergence — check the two still don't need to share the fix).
- The ungated noc_panel_hit + camera_wheel_policy + NOC_PANEL_* constants (B2 fold): verify nothing else in the PP_DEBUG block referenced them in ways the ungating breaks (e.g. duplicate definitions, ordering), and that `rl` (vendor:raylib) import in noc_overlay.odin is legal ungated (check what the file already imported).
- The N1 fold: camera_update now calls camera_fit(v) — verify view_compute (app/render/view.odin) also derives from the same expression, i.e. the triplication is actually reduced to one source or whether view.odin still carries its own copy.
- The N11 fold: App.auto_pullback deleted — grep for any remaining reader of a mirrored field (draw_hud snapshot, effect_settings_adjust, pullback_feed) and confirm they all read app.a11y.auto_pullback.
- The v1-settings compat claim: settings_save_at writes 7 bytes v2 — verify the save path matches the loader's v2 layout byte-for-byte (payload order palette/motion/scale/pullback + checksum).
- The touch two-finger pan (touch.odin) — the diff's exec routing claims touch Pan reaches on_pan; verify touch.odin actually emits Pan intents with screen deltas (the W9 pin drives Device_Events directly, so the real touch_map path is untested — is touch.odin's emission in the worktree consistent with what the executor expects?).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/codebase.json

Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. orphan, duplication>",
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
