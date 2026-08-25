You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-form-hunt-r1/AGENTS.md — it is the project's standing instructions (conventions). Capture it as your conventions context.

--- DIFF ---
The exact diff bytes are saved at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-form-hunt/r1/diff.patch (unified diff, PR #633, reviewed commit 109006f on top of develop 82ac223). Read that file. Review exactly those bytes — never regenerate the diff via git.

--- SPEC / CONTEXT ---
This PR implements the user-approved fixes from a mobile form bug hunt. Two spec documents:
1. /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-form-hunt.md — the original job briefing (the hunt's mission + method; the hunt itself was report-only, no code changes).
2. /Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-form-hunt-r1/_bmad-output/implementation-artifacts/mobile-form-hunt/notes/findings.md — the committed hunt findings (1 bug B1, 7 tap-target findings T1–T7, 13 notes) with a "POST-REVIEW: approved fixes implemented" section listing exactly which fixes the user approved. That POST-REVIEW list is the acceptance contract for this PR.
Read both.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Write ONE valid JSON array — and NOTHING else — to the file:
/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-form-hunt/r1/$lens.json
Use your write tool with exactly that absolute path. Do not derive, relocate, or rename it. Then stop.

Each element must match this schema exactly:
{
  "source": "$lens",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array in the output file. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
