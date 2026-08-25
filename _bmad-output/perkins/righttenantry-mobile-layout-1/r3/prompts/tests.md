You are reviewing a code diff in the RightTenantry repo. You have read-only access to the repository worktree and may verify the diff's claims against the actual codebase using your tools. Do NOT modify, build, or write any repo file. The ONLY file you may write is your output JSON at the path given below.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r3/AGENTS.md for project conventions.

--- DIFF ---
The canonical diff is at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r3/diff.patch - read it fully with the read tool. Review exactly these bytes; do not re-generate or re-fetch the diff.

--- WORKTREE (verification) ---
/Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r3 is a checkout at exactly the reviewed state (sha 0f94e043a50851ecbd9bb82d1ec752f75823338f). Every verification read happens here. Your cwd is already this worktree.

--- SPEC / CONTEXT ---
Read both:
- /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md (original job spec: 5 mobile UX fixes + acceptance criteria)
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-mobile-layout-1-r3.md (round-3 reviewer briefing; the "Lens-guards" section names what each round-2 blocker fix must satisfy)

--- PRIOR ROUND (this is a FIX-AUDIT round, round 3) ---
The round-2 consolidated findings are at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r2/consolidated.json. Round 2 ended NEEDS CHANGES with 2 blockers (B1: demo click arm bypasses notification_target_path - vacancy-typed demo clicks no-op; B2: late ApiReturnedLeaderboard response re-fabricates a wrong vacancy id), 2 warnings (vacancy_detail pb-28 untested; filter-pill shrink-0 untested), 6 notes. This diff is the fix for those.
Do NOT re-report r2 findings as new. If an r2 finding's fix is MISSING or insufficient, report it as a finding titled "<original title> (still present since round 2)" with severity at least as high as round 2.
Do NOT re-litigate: the r2 blocker fixes themselves (audit that they LANDED and BITE), the client-side resolution choice (user-approved), or the 5-fix list.

--- ROUND-3 HARD BLOCKER CLASS (carried) ---
The notification deep-link contract: BOTH entity types (vacancy AND application) navigate + mark read; no fabricated vacancy ids (real AI-failure notifications carry only the application id); vacancy behavior unchanged.

--- ROUND-3 LENS-GUARDS (from the r3 briefing - verify each BITES) ---
- B1 (r2) fix: the helper (with resolve_application_vacancy) must be moved into a NEUTRAL module both arms import; the demo arm must CALL it; BOTH arms must be pinned by tests. Verify vacancy-typed demo clicks now NAVIGATE (the r1/r2 miss was demo clicks no-op'ing) and the real arm still routes through the same helper (no contract drift).
- B2 (r2) fix: the plain leaderboard response message ApiReturnedLeaderboard (and the page variant) must carry the vacancy id and apply only on match (like the refresh handler's vacancy_detail_request_id). Verify the exact r2 repro: VacancyDetail(A) fetch in flight -> navigate to B -> A's response lands -> A's rows must NOT tag as B, and the resolver must not fabricate.
- Also check: the neutral-module move didn't break the real arm; the demo arm's pins are real (revert-style: a wrong path must fail a test); no regression on the demo r1-r5 gauntlet classes; r2 warnings (vacancy_detail pb-28 test, filter-pill shrink-0 test) and notes status.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage.

Round-3 specifics you MUST check by reading the test files in the worktree (client/test/client_test.gleam, client/test/demo/demo_flow_test.gleam, and any new test module for the neutral helper):
- B1 (r2) fix pins: both the real arm AND demo arm route through the helper, with REAL tests (revert-style: a wrong target path or a demo vacancy no-op must fail a test). Confirm the demo vacancy-navigation test actually drives UserClickedNotification through demo_update, not just the helper in isolation.
- B2 (r2) fix regression test: a late ApiReturnedLeaderboard carrying vacancy A's id while the route/tag is B must NOT apply A's rows, and the resolver must not resolve. Read the test and confirm it asserts the negative, not just construction.
- r2 warnings: vacancy_detail pb-28 test, filter-pill shrink-0 test - did they land this round or are they still absent?
- The demo r1-r5 gauntlet classes must not regress (demo_flow_test).
- The claimed suite count (637+ at round 2) - count the tests added in this diff and sanity-check.

Blind-spot heuristics: new state transitions without boundary tests, happy-path-only coverage, new message fields without mismatch-case tests.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale
Gate thresholds: PASS: P0 100%, P1 >=90%, overall >=80%; CONCERNS: P0 100%, P1 80-89%; FAIL: P0 <100% or P1 <80% or overall <80%.

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r3/tests.json
Each element must match this schema exactly:
{
  "source": ""tests"",
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

When done, reply with one line: "DONE tests <n> findings".
