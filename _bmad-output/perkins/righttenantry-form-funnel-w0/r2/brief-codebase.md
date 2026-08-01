You are reviewing a code diff (round 2 of an automated review loop). You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r2 — a detached worktree at exactly the reviewed sha 7bb582443d3844d6d349d0144b4caab42c81f196) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line (~5100 lines).

--- ROUND 2 CONTEXT ---
This PR was reviewed once already (round 1); the head commit ("fix: Perkins r1 — RLS-safe sender-state view, single stage-2 gate, test pins") claims to fix the r1 findings. Review the whole diff fresh against the real codebase.

--- SPEC / CONTEXT (read if you need intent) ---
1. /Users/moses/code/_bmad-output/briefings/righttenantry-form-funnel-w0.md — the original job briefing.
2. _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md (at your cwd) — the frozen implementation spec, incl. Code Map.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
- The project uses Gleam + Squirrel codegen for SQL. The spec says Squirrel must be regenerated after the migration/SQL changes — check the generated sql.gleam files in the diff are consistent with the .sql files (column lists, decoder shapes).

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/codebase.json

Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: the file must contain ONLY the JSON array. No prose, no fencing, no preamble. Empty array `[]` is valid. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames or assume.
- The `evidence` field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it.
- Hedging language ("might", "could", "possibly") means you have not verified — either verify and report crisply, or drop it.
- Prefer fewer, well-grounded findings over many speculative ones. Accuracy > volume.

After writing the file, reply with one line: count of findings written. Then stop.
