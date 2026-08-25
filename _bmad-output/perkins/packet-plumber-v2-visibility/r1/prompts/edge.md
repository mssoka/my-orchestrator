You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

MANDATORY FIRST READS (in this order):
1. The canonical diff: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-visibility/r1/diff.patch — review EXACTLY these bytes. Never re-fetch or regenerate the diff (no `gh pr diff`, no `git diff`).
2. Project conventions: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1/project-context.md
3. The spec (the original job briefing — this is what the diff is meant to do): /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-visibility.md
4. Context: the implementation spec at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1/_bmad-output/implementation-artifacts/spec-v2-visibility.md and the PR body at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1/_pr_body.md

Your worktree (ALL verification reads happen here — a detached checkout at exactly the reviewed sha 857516479dbcc7116933417b37fe893d6ba89ad7): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1

--- ROUND-SPECIFIC GUARDS (from the review owner — these bound your lens) ---
- The ONE hard blocker is the determinism spine: T1 byte-identical, zero T2 shift. All five new surfaces must be app-layer in `draw_hud`, never in the harness capture path (the harness T2 capture calls only `draw_world` + `draw_forecast_panel` + `draw_health_meter` + `draw_crisis_banner` — never `draw_hud`). Any golden/T1/T2 change in this diff is a BLOCKER. No LOG_VERSION bump, no serialization change — a wire-format or version change is a BLOCKER.
- Verify specifically: (a) the "why-dropped" split always sums to the gauge's drop N (the 2.3 severed-cull drops an SLA drop with NO drop event and NO Drop_Site — the split must name that residual or it undercounts); (b) drop-site markers anchor on the canonical (lo,hi) node pair, not the renumbered bundle slot (bundle slots renumber on every topology change); (c) the claim that T2-invisible app-layer rendering was verified PROGRAMMATICALLY (scratch pixel-scan of gauge fill / SHEDDING tag / marker anchors), not eyeballed — check the PR body and spec for that evidence.
- Do NOT re-litigate: the 08-15 terminology rulings (congestion / drop precedence / lane-split — canon amendment is section-additive); the merged 5.2 node-health tri-state surface; the font-resize T2-fold discipline precedent; the post-rebase rename adoption hunks (state_strain -> state_congested — the terminology canon, already merged to base via #55).
- The GDD decision-log canon amendment is intentionally additive (legibility in-game is a design requirement; invisible chokepoints are defects) — verify it landed additively; it is not a defect.

--- YOUR LENS ---

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code does not account for, input the new code does not validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. determinism, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

FILE-OUTPUT CONTRACT (mandatory):
- Write the JSON array — and ONLY the JSON array — to this exact absolute path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-visibility/r1/edge.json
- No prose, no markdown fencing, no preamble in the file. An empty array `[]` is valid and expected when you find nothing.
- After writing the file, STOP. Your final chat message is one line: "wrote /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-visibility/r1/edge.json (<n> findings)". Do not fix anything, do not open PRs, do not edit repo files.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
