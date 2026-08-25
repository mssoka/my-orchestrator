You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your current working directory IS the exact reviewed state — trust it.

--- PROJECT CONVENTIONS ---
Read project-context.md at the repo root first (Odin + raylib game: pure integer-only core, view-layer-only floats, arena discipline, golden-image harness with zero-drift doctrine, named-constant rules).

--- DIFF ---
The canonical unified diff — the exact bytes under review (read this file, never regenerate the diff):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r3/diff.patch

--- SPEC / CONTEXT ---
The spec this diff must satisfy (the authoritative acceptance criteria):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-noc-readability-2.md
The implementation's own claims (PR body — treat as claims to audit, not truth):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r3/pr-body.md

--- PRIOR ROUND (re-review / fix-audit round 3) ---
The previous round's consolidated findings live at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r3/prior-consolidated.json
Round 2 verdict was NEEDS CHANGES with: B1' (per-class header collision "loss"/"SLA" + window-clipped "/3s"), W1' (demolish popover occluded by rail, button clickable), W2' (forecast preview rail re-anchor untested), W3' (resize re-apply unpinned), W4' (rail-on app camera threading untested), W5' (rail plate owns wheel but not clicks), W6' (advisory gate CONCERNS), N1'-N7' notes (incl. N6' stale LIVE PR body). The fix commit under review claims ALL of these fixed (header right-aligned at noc_col anchors + SLA clearance; popover clamps to play_w; plate swallows presses; new pins; live PR body refreshed). Treat prior findings as context — report NEW defects you find; do not re-report a prior finding unless the claimed fix is defective (in which case report it as a defect in the fix, with fresh evidence).

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Key spec invariants to audit (from the briefing): the ladder must be a NAMED tunable triplet (header 20 / body 18 / labels 15, all at-or-above the 14px floor) with named width scale — no magic numbers; the panel docks FAR RIGHT as a full-height rail and the rail NEVER covers the HUD top-band; width +~40% with recomputed tabular column math (right-aligned 18px numerals); ring buffer 256 unchanged with wheel scroll; zero golden drift (48/48, view-layer only, zero sim writes, hash-equal streams); tests updated (panel rect expectations, visible-row math); KYLE legibility gate evidence + captures in the PR body.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY your JSON array — no prose, no markdown fencing, no preamble — to this exact absolute path using your file-writing tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r3/acceptance.json
then stop. `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.
Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
