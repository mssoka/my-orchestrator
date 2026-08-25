You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your tools. Your cwd IS the reviewed worktree (/Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r4) - verify against files here, never against any other checkout. Project conventions live in AGENTS.md at the worktree root; read it.

--- DIFF ---
The diff is at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r4/diff.patch - read it fully with the read tool.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-mobile-layout-1-r4.md (r4 fix-audit briefing)
- /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md (original job briefing: 5 fixes + acceptance criteria)

--- ROUND-4 CONTEXT (fix-audit round) ---
Round 3 had ONE blocker: cold-boot fetch paths (session-restore ApiReturnedSession VacancyDetail arm, and enter_demo / demo_entry_effects) never set leaderboard_vacancy_id, so the late-response guard dropped legitimate responses. Also W1: the ApiReturnedLeaderboard Error arm ignored the vacancy-id guard. This round's diff is the SAME PR at a new sha containing the r3 fix. Do NOT re-litigate the fix list or the user-approved client-side resolution choice. DO audit whether the r3 fixes actually LANDED and BIT. Priorities: (a) the cold-boot set-sites are complete - grep ALL fetch_leaderboard call sites; none may be missing the tag; (b) the Error arm now respects the guard; (c) no live-product regression from the notification deep-link contract (both entity types navigate + mark read; no fabricated vacancy ids; vacancy behavior unchanged).

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code - functions, exports, types no longer referenced after this change?
Also: grep ALL call sites of fetch_leaderboard and confirm every dispatch that should set leaderboard_vacancy_id does set it - report any site that pairs a fetch with no tag as a blocker.

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r4/codebase.json
Each element must match this schema exactly:
{
  "source": "codebase",
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

When done, reply with one line: "DONE codebase <n> findings".
