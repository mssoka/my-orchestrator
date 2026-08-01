You are reviewing a code diff. You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r1) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line.

--- SPEC / CONTEXT ---
This diff adds PostHog funnel analytics, Resend email tracking, a two-stage reminder series (new SQL + migrations), and copy pack edits to a Gleam (Lustre client + Wisp server) app. Skim _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md at your cwd if useful.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match (check every new function call has a definition; every renamed/moved symbol updated everywhere; Gleam types line up)?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages — check gleam.toml / package.json / Makefile changes) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
- Is apply_analytics.js actually served/loaded by the pages that need it (check how static assets are referenced in form_pages/form_view)?
- Do the new SQL files match the queries invoked from sql.gleam, and do the migrations match the SQL the code expects (column names, view names)?

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/codebase.json

Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings with no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
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
