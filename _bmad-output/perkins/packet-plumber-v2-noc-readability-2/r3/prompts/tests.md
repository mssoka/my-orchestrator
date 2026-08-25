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
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY your JSON array — no prose, no markdown fencing, no preamble — to this exact absolute path using your file-writing tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r3/tests.json
then stop. `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.
Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
