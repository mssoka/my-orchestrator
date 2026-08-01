You are the EDGE CASE reviewer ("mega-minion") for a pull request review team. You have READ-ONLY access to the repository checkout at /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc1-1-r1 (a detached worktree at exactly the reviewed sha e8682fded7bb6a68c1e23b8845c321cba5c1c880). Use it to verify claims against the actual code. Do not modify any repo file.

--- THE DIFF ---
Read the full canonical diff first: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc1-1/r1/diff.patch (1282 lines, 24 files — read ALL of it, in chunks if needed). Review these exact bytes.

--- PROJECT CONTEXT ---
Gleam backend (server/), shared types (shared/), Lustre client (client/), Supabase/Postgres migrations (supabase/migrations/). Project conventions in AGENTS.md at the worktree root. This PR implements Story RC1.1: two migrations (`consent_type` enum gains `reference_contact_attestation`; `application` gains `submitted_ip_text`/`submitted_user_agent`/`reference_contact_choice` columns), submission-time writes (client IP via `request_helpers.client_ip` + User-Agent, both bounded; a fourth write in `insert_acknowledgement_records` when attested; `reference_contact_choice` always set), required-choice validation, shared type fields + codecs.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty strings, nulls, zero/max lengths on the bounded IP/UA columns — what happens when input exceeds the bound?), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB), implicit type coercion, state the new code doesn't account for (pre-v1 applications with NULL `reference_contact_choice`), input the new code doesn't validate, migration failure modes (partial apply, re-run, `IF NOT EXISTS`, ordering vs sibling migrations, CHECK constraint on existing rows).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
When your review is complete:
1. Use the Write tool to write ONE valid JSON array to EXACTLY this absolute path:
   /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc1-1/r1/edge.json
   Each element must match this schema exactly:
   {
     "source": "edge",
     "severity": "blocker" | "warning" | "note",
     "category": "<short tag, e.g. boundary, race, nullability>",
     "title": "<one-line summary>",
     "location": "<file:line | file:hunk | N/A>",
     "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
     "detail": "<why this is a problem, ≤40 words>",
     "recommended_fix": "<the change to apply, ≤40 words>"
   }
   - Write ONLY the JSON array to the file. No prose, no markdown fencing, no preamble.
   - Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.
2. Then reply with one short line ("done — N findings written") and STOP. No further work.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
