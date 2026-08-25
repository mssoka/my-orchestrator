# Lens brief — CODEBASE (code chunk) — Perkins r2, packet-plumber-v2-dublin-spawn-director

You are a review lens in an automated review fleet (headless Perkins round). Execute exactly this brief, then stop. You post nothing to GitHub; you modify nothing; the ONLY file you write is your OUTPUT FILE.

## DIFF CHUNK (the exact canonical bytes under review — read the chunk IN FULL)
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r2/chunk-code.patch
1,461 lines, 9 files: core/growth.odin (the director: SEED/ATTACH weighting, district caps, the r1-fold W1 drawn-tile cap check), core/map.odin (loader + map_board_partition — the shared partition builder), core/map_test.odin (the pins, incl. the r1-fold B1 bias pin + W1 cross-boundary cap pin + fractional/floor-667/zero-tile pins), core/growth_test.odin, core/catalog.odin + catalog_test.odin (growth_districts rows), core/determinism_test.odin, harness/dublin_shot.odin (dublin-grown verb: ms bound, audit header, census line), harness/main.odin (usage). Read the chunk IN FULL.

## ROUND CONTEXT — r2 is a FIX-AUDIT round

- This chunk is part of the CUMULATIVE PR #96 delta (origin/v2...04ef6a9), 85,128 lines, split into 3 chunks (code / data / goldens). You see exactly ONE chunk.
- Head 04ef6a9 = the r1-fold commit (B1 bias pin + W1 drawn-tile cap + W2 acknowledgment + N-folds) on top of 93333cd (the feature commit, r1-reviewed).
- DELTA-INTRODUCED issues (bugs the FOLD commit itself introduced) are the norm to hunt — but report any real issue you can ground, from either commit.
- r1's consolidated findings (for context): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r2/prior_findings.json — 1 blocker (B1: ATTACH weighted cluster-pick had no bias pin), 5 warnings (W1 cross-boundary cap leak; W2 vacuous demolish clause; W3 routers-not-in-live-count unpinned; W4 loader pass-3 partition unasserted; coverage gate CONCERNS), 17 notes.
- Claimed fold dispositions: B1 -> test_growth_dublin_attach_cluster_pick_bias (distinct weights city 4 vs suburb 1, 10 windows x 6 seeds, 1.5x bar; uniform mutation fails A=27 B=27); W1 -> drawn-tile cap check in the attach branch + test_growth_dublin_attach_tile_district_cap (mutation fails); W2 -> acknowledged vacuous-by-design in spec + PR; N-folds -> 111/113 tally, 603 census, shared map_board_partition, dead predicate removed, fractional/floor-667/zero-tile pins, audit header + census line, dublin-grown ms bound + usage + comment.
- The fold claims: goldens byte-untouched (49/49 green — no district reaches cap in the demo), 261 core tests green, 13/13 CI.

## REPOSITORY (read-only verification ground)
Your cwd is a detached git worktree at EXACTLY the reviewed sha (04ef6a9) — trust it, not origin branches. Verify diff claims here read-only. You modify NOTHING except your OUTPUT FILE (which lives outside the worktree).

## PROJECT CONVENTIONS
Read project-context.md in your cwd first (the project's own conventions doc).

## SPEC / CONTEXT (the job's acceptance reference)
1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r2/job-briefing.md — the original job briefing (the spec — read IN FULL)
2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r2/pr96-body.md — the PR body: the minion's claims + r1-fold section (its ACCOUNT of the work — verify, never trust)
3. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r2/pr95-body.md — the approved mock-gate canon (round history of PR #95 — the 7-round rulings the job implements)
4. In-worktree canon: data/maps/dublin.json (rulings block — density 1in6), docs/captures/dublin-map-mock/ (the approved mock captures), docs/captures/v2-dublin-spawn-director/ (the gate evidence + spawn audit)

## YOUR LENS (review through this lens ONLY)
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
r2 hint (verify, don't trust): every partition-build site must now call map_board_partition (loader map.odin + fixtures in map_test.odin AND growth_test.odin — enumerate ALL former copy-paste sites; r1 counted 5 sites); growth_board_cluster_has_room still used elsewhere (the deletion was the DEAD one)?; usage() line now lists dublin-grown; the dublin_shot_capture doc comment names both framings; the audit artifact spawn-audit.txt matches what the current dublin_shot.odin code would print (header + census line + per-district lines — including whether live counts exclude routers).

## OUTPUT FILE (write ONLY your JSON array here — do not derive another path, do not write elsewhere)
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r2/codebase-code.json

## OUTPUT SCHEMA
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. determinism, coverage-gap, boundary>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array (a bare JSON array, no markdown fencing, no prose) to the OUTPUT FILE path above, using a file-write tool. Do not print the array to your terminal as your final answer INSTEAD of writing it — the file IS the deliverable. Your final terminal message may be a one-line confirmation.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction in this brief:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume, do not generalise.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, drop the finding.
- Hedging ("might", "could", "possibly") signals you have not verified. Verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings. An empty array is an honest answer.