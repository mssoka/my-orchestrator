You are reviewing a code diff in the RightTenantry repo. You have read-only access to the repository worktree and may verify the diff's claims against the actual codebase using your tools. Do NOT modify, build, or write any repo file. The ONLY file you may write is your output JSON at the path given below.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r2/AGENTS.md for project conventions.

--- DIFF ---
The canonical diff is at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r2/diff.patch - read it fully with the read tool. Review exactly these bytes; do not re-generate or re-fetch the diff.

--- WORKTREE (verification) ---
/Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r2 is a checkout at exactly the reviewed state (sha 3acbf6ba72268bee91462230d480358f8b86799e). Every verification read happens here.

--- SPEC / CONTEXT ---
Read both:
- /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md (original job spec: 5 mobile UX fixes + acceptance criteria)
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-mobile-layout-1-r2.md (round-2 reviewer briefing; the "Lens-guards" section names what each round-1 blocker fix must satisfy)

--- PRIOR ROUND (this is a FIX-AUDIT round) ---
The round-1 consolidated findings are at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r1/consolidated.json. Round 1 ended NEEDS CHANGES with 2 blockers (B1: stale-leaderboard fabricated vacancy id; B2: no navigation pin for vacancy-typed notifications), 2 warnings, 4 notes. This diff is the fix for those.
Do NOT re-report r1 findings as new. If an r1 finding's fix is MISSING or insufficient, report it as a finding titled "<original title> (still present since round 1)" with severity at least as high as round 1.
Do NOT re-litigate: the client-side resolution choice (loaded leaderboard + leaderboard_vacancy_id tag, else graceful no-op), the user-approved 5-fix list, or the existence of the r1 fixes themselves unless they failed to land.

--- ROUND-2 HARD BLOCKER CLASS ---
The notification deep-link contract: BOTH entity types (vacancy AND application) navigate + mark read; no fabricated vacancy ids (application resolution must require leaderboard_vacancy_id == route vid); vacancy behavior unchanged. A pure notification_target_path/3 routing decision must exist and BOTH the real arm (client.gleam) and demo arm (demo_update.gleam) must route through it, with real tests pinning it (a wrong target path must fail a test).

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (notification_target_path in client.gleam, leaderboard_vacancy_id in model.gleam, demo_update.gleam call sites)
- Are naming conventions and style consistent?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in location.)
- Are new dependencies available?
- Are there existing tests this diff likely breaks? (Name them in location.) The client suite was 632 green at round 1 and is claimed 637 green now - sanity-check that test count delta matches the new tests in the diff.
- Does it leave orphan code - functions, exports, types no longer referenced?

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r2/codebase.json
Each element must match this schema exactly:
{
  "source": ""codebase"",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract: the file contains ONLY the JSON array. No prose, no fencing, no preamble. [] is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE - the most important instruction in this prompt: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Open the file. Read the relevant lines. The evidence field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly") is a signal you have not verified - either verify and report crisply, or do not report. Prefer fewer, well-grounded findings over many speculative ones.

When done, reply with one line: "DONE codebase <n> findings".
