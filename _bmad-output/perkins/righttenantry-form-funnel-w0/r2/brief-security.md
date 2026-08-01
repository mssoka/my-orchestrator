You are reviewing a code diff (round 2 of an automated review loop). You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r2 — a detached worktree at exactly the reviewed sha 7bb582443d3844d6d349d0144b4caab42c81f196) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line (~5100 lines).

--- ROUND 2 CONTEXT ---
This PR was reviewed once already (round 1). Round 1's headline finding was a BLOCKER on your lens: the new view `inbound_email_sender_state` was created `security_definer` (or without `security_invoker`), bypassing RLS and exposing enquirer emails via the public anon key (supabase/migrations/20260731213000_add_inbound_email_sender_state_view.sql:22). The head commit claims "RLS-safe sender-state view". VERIFY this fix rigorously: read the migration as it now stands, check Postgres version semantics for views (security_invoker requires PG15+; check what the project targets and what other migrations do), check grants on the view, and check every consumer of the view. Then continue a fresh security pass over the whole diff.

--- SPEC / CONTEXT (read if you need intent) ---
1. /Users/moses/code/_bmad-output/briefings/righttenantry-form-funnel-w0.md — the original job briefing.
2. _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md (at your cwd) — the frozen implementation spec (note the consent/PII constraints in Boundaries & Constraints).

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state) — applicant emails/names are PII; PostHog events must carry field KEYS only, no values
- Injection vectors (SQL, XSS, command, path traversal, SSRF) — note new raw SQL files and any HTML email template interpolation of user-controlled data
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
- The stable anon id design (localStorage key `rt_apply_did:<short_code>`) — consent withdrawal must remove it; no cross-vacancy identity

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/security.json

Each element must match this schema exactly:
{
  "source": "security",
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
