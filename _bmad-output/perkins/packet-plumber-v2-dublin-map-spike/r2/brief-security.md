# Lens brief — SECURITY (r2)

You are reviewing a code diff. You have read-only access to the repository (your cwd IS the reviewed worktree) and may verify the diff's claims against the actual codebase using your available tools. Do not modify any file.

--- PROJECT CONVENTIONS ---
Read project-context.md in the repo root (governs code conduct). tools/ scripts are offline dev tooling, not game runtime code. This repo is a deterministic offline game; the diff adds two offline dev tools + a data asset.

--- DIFF ---
The canonical diff file (903 lines; ONE line inside it — L50 — is a single ~3.9 MB JSON asset line; NEVER cat that line raw, slice it with sed/python3):

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r2/diff.patch

Diff map: L1-13 .gitignore; L15-23 .memlog.md (append-only log); L25-42 new field-notes md; L44-50 new data/maps/dublin.json (entire asset = ONE line, L50, valid JSON — analyze via python3 reading the diff file, extracting L50, stripping the leading '+', json.loads); L52-87 nine new binary PNG stubs; L88-685 new tools/osm_extract.py (593 lines); L687-903 new tools/render_dublin_preview.py (211 lines).

--- SPEC / CONTEXT ---
The job briefing (context for what this diff is meant to do):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-dublin-map-spike.md

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Scope reality: this diff has no endpoints, no auth, no secrets. The real attack-surface-adjacent surface is: osm_extract.py fetching from third-party Overpass mirrors (TLS handling, response trust, cache file writes, the User-Agent string), file path handling (--out/--cache args), the 3.9 MB committed JSON asset as future game input (does it contain anything the game should not trust — huge coordinates, weird strings, personal data), and render_dublin_preview.py loading font/asset files. Report what is genuinely there; do not pad with boilerplate web-app findings that do not apply to offline dev tooling.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. tls, supply-chain>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
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
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT (mandatory) ---
Write your JSON array — and NOTHING else — to this exact absolute path (do not derive or guess any other path):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r2/security.json
Use your file-writing tool to create that file containing exactly the JSON array. After the file is written, stop. Do not do anything else.
