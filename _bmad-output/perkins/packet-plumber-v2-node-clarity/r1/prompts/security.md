You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read `/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-node-clarity-r1/project-context.md` — that file's content IS the PROJECT CONVENTIONS block below.

--- DIFF ---
The diff under review is the exact bytes of `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r1/diff.patch` — read that file; its content IS the DIFF block. (1240 lines, unified format. The long `goldens/**` section is binary PNG re-blesses — expected and documented in the spec/PR body; judge the text hunks on their merits.)

--- SPEC / CONTEXT ---
Read these two files; together their content IS the SPEC / CONTEXT block:
1. `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-node-clarity.md` — the job briefing (THE spec: task, hard rules, acceptance).
2. `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r1/pr-body.md` — the PR body (the implementer's claims and the documented deviations D1–D7).

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
Return ONE valid JSON array. Each element must match this schema exactly:
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
- Write your JSON array to the file `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r1/security.json` — that file must contain ONLY the JSON array (no prose, no markdown fencing, no preamble). Then reply with one short line confirming the write, and stop.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
