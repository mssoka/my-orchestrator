You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the repo root at the reviewed state — verify against it. READ-ONLY: do not edit, create, or delete any file in the repo (your ONLY write is the output JSON file named below).

--- PROJECT CONVENTIONS ---
Read the conventions doc at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r5/project-context.md
(Odin + raylib game: pure core, integer sim, golden-harness testing, fail-loud error doctrine.)

--- DIFF ---
The canonical diff under review is saved at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r5/diff.patch
Read that file — those are the exact bytes under review (base v2 → head 3e62101). Do NOT regenerate the diff with git; review exactly these bytes.

--- SPEC / CONTEXT ---
Read the original job briefing (it IS the spec for this diff):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-font-overhaul.md
Settled user rulings carried by the spec (do NOT flag these): the IBM Plex Sans family pick is USER-CHOSEN (twice-gated, not re-litigatable); the golden-image churn is expected and cause-documented; merge order LAST is by design; the audio-seam WRAPPER DESIGN was ruled behavior-preserving in review round 2; OFL-only licensing for fonts is the rule.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

(This is an offline Odin/raylib game — most web classes do not apply; report only what genuinely applies: untrusted input paths (demo files, font/asset files, CLI args), path handling, memory safety of FFI boundaries, unsafe deserialization of catalog/demo data.)

--- OUTPUT ---
Write ONLY your JSON array to this exact file path (do not derive or guess another):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r5/security.json
Then stop. Your final message must be one line: "security done".

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
- ONLY the JSON array in the file. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
