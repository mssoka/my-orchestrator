# Lens brief — ACCEPTANCE (code chunk) — Perkins r1, packet-plumber-v2-dublin-spawn-director

You are a review lens in an automated review fleet (headless Perkins round). Execute exactly this brief, then stop. You post nothing to GitHub; you modify nothing; the ONLY file you write is your OUTPUT FILE.

## DIFF CHUNK (the exact canonical bytes under review)
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r1/chunk-code.patch
1,705 lines, 19 files: core/*.odin implementation + tests (catalog, growth, map + their test files, determinism_test), data/balance.json, demos/dublin_board.dem, harness verbs (dublin_shot, main), docs/captures gate evidence + the spec artifacts under _bmad-output/. Read the chunk IN FULL.

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
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec
For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).
Canon anchors for this round (verify against these, do not trust the PR body's summary of them): data/maps/dublin.json rulings block (density_default 1in6); docs/captures/dublin-map-mock/ (the approved round-7 mock captures); the job-briefing scope (district spawn-director, zoom-band spawn side, determinism; streets-constrain-pipes + last-mile draw are OUT OF SCOPE).

## OUTPUT FILE (write ONLY your JSON array here — do not derive another path, do not write elsewhere)
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r1/acceptance-code.json

## OUTPUT SCHEMA + ACCURACY MANDATE
{
  "source": "acceptance",
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