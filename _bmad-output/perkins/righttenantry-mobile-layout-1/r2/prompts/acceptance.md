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
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift - changes not asked for by the spec

This is a FIX-AUDIT round. Verify EACH round-1 blocker fix BITES, exactly per the round-2 briefing Lens-guards:
- B1: the leaderboard must be tagged with the vacancy id it was fetched for (leaderboard_vacancy_id set on fetch/response) and resolve_application_vacancy must require it to equal the route vid (or leaderboard reset on the other vacancy-scoped route entries). Verify the exact r1 repro in the actual code: client/src/client.gleam handle_browser_change + resolve_application_vacancy. Real AI-failure notifications carry only the application id (server/src/ai/ai_notifications.gleam) - the resolver must not fabricate a vacancy id from a stale source.
- B2: a pure notification_target_path/3 routing decision (vacancy -> /vacancies/<vid>, application -> resolved app detail, others/unknown -> None) must pin BOTH entity types + the no-op cases; the real AND demo click arms must BOTH route through it. Verify by reading client.gleam and client/src/demo/demo_update.gleam that both call the same helper.
- Also audit the r1 warnings/notes in the prior consolidated.json: fixed or still present.

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r2/acceptance.json
Each element must match this schema exactly:
{
  "source": ""acceptance"",
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

When done, reply with one line: "DONE acceptance <n> findings".
