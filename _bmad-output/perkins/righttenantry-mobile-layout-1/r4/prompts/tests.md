You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your tools. Your cwd IS the reviewed worktree (/Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r4) - verify against files here, never against any other checkout. Project conventions live in AGENTS.md at the worktree root; read it.

--- DIFF ---
The diff is at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r4/diff.patch - read it fully with the read tool.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-mobile-layout-1-r4.md (r4 fix-audit briefing)
- /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md (original job briefing: 5 fixes + acceptance criteria)

--- ROUND-4 CONTEXT (fix-audit round) ---
Round 3 had ONE blocker: cold-boot fetch paths (session-restore ApiReturnedSession VacancyDetail arm, and enter_demo / demo_entry_effects) never set leaderboard_vacancy_id, so the late-response guard dropped legitimate responses. Also W1: the ApiReturnedLeaderboard Error arm ignored the vacancy-id guard. This round's diff is the SAME PR at a new sha containing the r3 fix. Do NOT re-litigate the fix list or the user-approved client-side resolution choice. DO audit whether the r3 fixes actually LANDED and BIT. Priorities: (a) the cold-boot set-sites are complete - grep ALL fetch_leaderboard call sites; none may be missing the tag; (b) the Error arm now respects the guard; (c) no live-product regression from the notification deep-link contract (both entity types navigate + mark read; no fabricated vacancy ids; vacancy behavior unchanged).

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified handlers without matching coverage
- Happy-path-only coverage where error handling is implied
- New state transitions without boundary tests
Pay special attention: the session-restore cold-boot set-site (ApiReturnedSession VacancyDetail/Handoff arm in client.gleam) - is it pinned by a test? The demo cold-boot set-site is pinned by demo_cold_boot_deep_link_tags_leaderboard_test; check whether the real session-restore path has an equivalent pin.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 >=90%, overall >=80%; CONCERNS: P0 100%, P1 80-89%, overall >=80%; FAIL: P0 <100%, or P1 <80%, or overall <80%.

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r4/tests.json
Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings with no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract: the file contains ONLY the JSON array. No prose, no fencing, no preamble. [] is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE - the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Therefore: open the file, read the relevant lines. Hedging language ("might", "could", "possibly") means you have not verified - verify and report crisply, or drop it. Prefer fewer, well-grounded findings. An empty array is a fine and honest answer.

When done, reply with one line: "DONE tests <n> findings".
