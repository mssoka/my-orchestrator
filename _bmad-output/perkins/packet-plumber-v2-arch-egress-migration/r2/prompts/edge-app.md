You are a lens agent in a headless code-review round. Your pane's cwd is a detached worktree at EXACTLY the reviewed state. Read-only review: do NOT edit any file, do NOT run git write commands, do NOT create branches or commits.

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- HOW TO LOAD YOUR INPUTS (do this first) ---
1. DIFF: read the file /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r2/app.diff — this is the canonical diff for your chunk (app chunk of the round).
2. PROJECT CONVENTIONS: read /Users/moses/code/packet-plumber-wt-egress-r2/project-context.md (13KB — the repo's agent instructions).
3. SPEC / CONTEXT: read ALL THREE spec files:
   - /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r2/pr-body.md (the PR body)
   - /Users/moses/code/_bmad-output/briefs/packet-plumber-v2-arch-egress-migration.md (the implementing minion's briefing)
   - /Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/architecture/architecture-egress-qos-2026-08-26/ARCHITECTURE-SPINE.md (the ratified architecture spine — it is LAW)
4. Your lens brief follows. Execute exactly it.

--- PROJECT CONVENTIONS ---
(loaded from /Users/moses/code/packet-plumber-wt-egress-r2/project-context.md above — Odin dev-2026-08 + raylib 6.0; core is pure/integer-only/deterministic; arena discipline; golden harness discipline)

--- DIFF ---
(loaded from /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r2/app.diff above — app chunk)

--- SPEC / CONTEXT ---
(loaded from the three spec files above)

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT (overrides the "return" wording above — headless mode):
Write ONLY your JSON array to this exact absolute path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r2/edge-app.json — create the file with that exact name (do not derive or invent another path), containing ONLY the JSON array (no prose, no fencing). Then state the path you wrote and stop. Your deliverable is the FILE, not your reply text. Use source value "edge" for every finding.