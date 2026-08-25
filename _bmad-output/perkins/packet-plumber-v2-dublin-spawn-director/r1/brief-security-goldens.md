# Lens brief — SECURITY (goldens chunk) — Perkins r1, packet-plumber-v2-dublin-spawn-director

You are a review lens in an automated review fleet (headless Perkins round). Execute exactly this brief, then stop. You post nothing to GitHub; you modify nothing; the ONLY file you write is your OUTPUT FILE.

## DIFF CHUNK (the exact canonical bytes under review)
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r1/chunk-goldens.patch
83,126 lines, 102 files: 51 re-blessed .t1 golden captures (full text diffs — the catalog_hash fold claim says every byte of catalog_hash-anchored content shifts), 49 .log.bin golden logs (binary 'files differ' stubs — byte-level claims are verified elsewhere; you verify the SHAPE), 2 re-blessed dublin_board PNGs (binary stubs). This is RE-BLESS DATA, not hand-written code. Method: read the first ~300 lines to learn the .t1 shape, enumerate EVERY file boundary (grep '^diff --git' on the chunk file), then sample hunk interiors across several .t1 files (e.g. a11y, growth, surge, dublin_board) and diff-compare what changed vs what did not. The determinism claims to audit (from the PR body, section 'Determinism'): (1) catalog_hash folds every balance.json byte so all 51 .t1 re-blesses are legitimate and uniform in cause; (2) 49/49 .log.bin differ ONLY in the 8 catalog-hash header bytes; (3) 117/119 T2 PNGs pixel-identical (i.e. exactly 2 PNGs change — check the count); (4) the 2 dublin_board T2s changed because the board branch's SEED draw went 1 -> <=2 draws + cluster pick became weighted. You can verify t1 content in the worktree read-only (the .t1 files at HEAD) and compare against the chunk's '---' side via git show if needed.

## REPOSITORY (read-only verification ground)
Your cwd is a detached git worktree at EXACTLY the reviewed sha (93333cd) — trust it, not origin branches. Verify diff claims here read-only.

## PROJECT CONVENTIONS
Read project-context.md in your cwd first (the project's own conventions doc).

## SPEC / CONTEXT (the job's acceptance reference)
1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r1/job-briefing.md — the original job briefing (the spec — read IN FULL)
2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r1/pr96-body.md — the PR body: the minion's claims + canon table (its ACCOUNT of the work — verify, never trust)
3. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r1/pr95-body.md — the approved mock-gate canon (round history of PR #95)
4. In-worktree canon: data/maps/dublin.json (rulings block — density 1in6), docs/captures/dublin-map-mock/ (the approved mock captures), docs/captures/v2-dublin-spawn-director/ (the new gate evidence + spawn audit)

## YOUR LENS (review through this lens ONLY)
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
This is an offline deterministic game engine (Odin); focus on what applies: asset parsing at load boundaries, unsafe deserialization of capture/log files, path handling in harness verbs, data exposure in logs.

## OUTPUT FILE (write ONLY your JSON array here — do not derive another path, do not write elsewhere)
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r1/security-goldens.json

## OUTPUT SCHEMA + ACCURACY MANDATE
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. determinism, coverage-gap, boundary>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array (a bare JSON array, no markdown fencing, no prose) to the OUTPUT FILE path below, using a file-write tool. Do not print the array to your terminal as your final answer INSTEAD of writing it — the file IS the deliverable. Your final terminal message may be a one-line confirmation.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction in this brief:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume, do not generalise.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, drop the finding.
- Hedging ("might", "could", "possibly") signals you have not verified. Verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings. An empty array is an honest answer.