You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read the project conventions file at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.12-aggregation-groups-r1/project-context.md

--- DIFF ---
Read the canonical diff file at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.12-aggregation-groups/r1/diff-code.patch
(The full PR diff also contains goldens/ binary + state-dump re-bless data that is verified mechanically by the orchestrator, not by lenses. Review exactly the code diff bytes above.)

--- WORKTREE (verify claims here) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.12-aggregation-groups-r1

--- SPEC / CONTEXT ---
Read these spec files:
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.12-aggregation-groups/r1/spec-briefing.md (original job briefing + the estates ruling)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.12-aggregation-groups/r1/spec-story-card.md (story card 5.12 — Given/When/Then + status line)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.12-aggregation-groups/r1/spec-pr-body.md (PR body — what shipped + re-bless cause chain)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.12-aggregation-groups/r1/spec-perkins-guards.md (round-1 review guards — the acceptance canon)

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, off-by-one errors, implicit type coercion, state the new code does not account for, input the new code does not validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Write ONE valid JSON array to this exact path (and nowhere else):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.12-aggregation-groups/r1/edge.json
Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not run tests that mutate state.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code.
- The evidence field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it.
- Hedging language ("might", "could", "possibly") is a signal you have not verified. Either verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer.
