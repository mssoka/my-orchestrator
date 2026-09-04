You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- REPOSITORY ---
The checkout at /Users/moses/code/packet-plumber-wt-egress-r1 is the reviewed state (detached @ 1e9c783 — exactly the reviewed sha). Verify every claim against THIS tree. READ-ONLY: do not modify any file, do not run state-changing git commands (checkout/reset/commit). You MAY run read-only commands (odin test is allowed IF you need it; prefer reading).

--- PROJECT CONVENTIONS ---
Read /Users/moses/code/packet-plumber-wt-egress-r1/project-context.md first for conventions. Key facts: Odin language; deterministic 20 Hz integer-tick network sim; pure core (ODN-1); integer-only delays (ODN-2); versioned binary save LOG_VERSION=6 (ODN-11); golden-image test harness (ODN-17).

--- DIFF ---
The diff chunk under review (the app/ wiring + harness + tools (reads contract surfaces, NOC overlay, qos panel, lint gate) — 8 files, ~289 diff lines): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r1/diff-app.patch
Read that file COMPLETELY — it is the diff under review. The full PR spans several chunks; anchor findings in this chunk's hunks, but read the whole repo freely for context.

--- SPEC / CONTEXT ---
Read all three:
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r1/pr-body.md
- /Users/moses/code/_bmad-output/briefs/packet-plumber-v2-arch-egress-migration.md
- /Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/architecture/architecture-egress-qos-2026-08-26/ARCHITECTURE-SPINE.md
(The spine is LAW — the migration must implement AD-1..AD-8.)

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this absolute path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-arch-egress-migration/r1/security-app.json
The file must contain ONLY the JSON array (no prose, no markdown fencing, no preamble). Then stop.
Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- ONLY the JSON array in that file. No prose, no fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.