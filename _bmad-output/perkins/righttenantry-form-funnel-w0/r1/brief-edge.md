You are reviewing a code diff. You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r1) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line.

--- SPEC / CONTEXT ---
This diff implements "Wave 0 instrumentation + Wave 1a honest-expectation copy pack" for a Gleam (Lustre client + Wisp server) rental application form, with PostHog analytics and Resend email tracking. Read these spec files at your cwd if you need context:
- _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md
- _bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/edge.json

Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, race, error-path>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: the file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble. Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. Accuracy > volume — an empty array is a fine and honest answer when nothing is wrong.

After writing the file, reply with one line: count of findings written. Then stop.
