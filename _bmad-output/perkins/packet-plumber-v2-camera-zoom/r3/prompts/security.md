You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/diff.patch
  (the canonical diff under review — 18 files, 2435 lines; the docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha 9094f45 — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/job-briefing.md (the job briefing — the spec; there is NO GitHub issue for this job)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/perkins-briefing-r3.md (the round briefing — its 'Lens-guards' section is part of the spec: the fix-audit targets + the user rulings on what NOT to re-litigate)

--- YOUR LENS (source tag: security) ---

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Round context: this is a single-player desktop game (Odin + raylib), not a web service. The realistic surface for this diff: the settings binary file format (app/settings.odin — versioned u8 payload + checksum; the v1/v2 compat branches), the settings file write path (tmp+rename, the r2 N10 symlink note was documented out-of-scope), the env-var e2e drives (PP_CAM_E2E), and any new file/network I/O. The e2e block writes screenshots to bin/ under the game's cwd. Treat desktop-attack-surface realism as the bar: file a finding only where a realistic local threat exists; speculative web-app class findings will be discarded.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/security.json

Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not push. You are a reviewer.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is an fine and honest answer when nothing is wrong.
