You are reviewing a code diff. You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r1) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line.

--- SPEC / CONTEXT ---
This diff adds PostHog funnel analytics (client JS + Gleam/Lustre) to a rental application form, Resend email open/click tracking, a two-stage reminder email series with new SQL + migrations, and copy changes. Key stated constraints: no PII (emails, names, field values) in any analytics event — field KEYS only; analytics must honor the existing consent gate; spam honeypot/timing fake-confirmation must not fire the confirmation event. Skim _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md at your cwd if useful.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers (note any new HTTP route, e.g. inbound-email webhook or reminder-send paths)
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages; check PostHog key handling, Resend API key use)
- Data exposure (sensitive fields in responses, logs, analytics events, or client-visible state — PII in event payloads is a spec violation AND a security finding)
- Injection vectors (SQL — check the new .sql files and sql.gleam changes; XSS — check new HTML/copy rendering and JS; command; path traversal; SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection on new state-changing routes
- Session or cookie handling gaps; tracking-privacy issues (anon id design, consent bypass)

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/security.json

Each element must match this schema exactly:
{
  "source": "security",
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
