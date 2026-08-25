You are reviewing a code diff as one lens of an automated multi-lens code review (Perkins round 5, job: righttenantry-demo-mode, PR #629, reviewed sha 2330189 - the r4-rework head. THIS ROUND IS A FIX AUDIT: the r4 findings (in r4-consolidated.json: 2 blockers + 16 warnings + 40 notes) were reworked at this sha; verify claimed fixes against the FRESH tree - a claimed fix that didn't bite is a NEW blocker, a landed fix is verified-FIXED and must NOT be re-emitted.)

You have read-only access to the repository and may verify the diff's claims against the actual codebase using your tools (read files, grep). All verification reads happen in the worktree - a checkout at exactly the reviewed state:
  WORKTREE: /Users/moses/.herdr/worktrees/RightTenantry/perkins-demo-mode-r5

The diff you review is EXACTLY these bytes (a file-group chunk of the full PR diff - never re-fetch or regenerate the diff):
  DIFF CHUNK: /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/chunk-c.patch
  (chunk c = everything else (components shell/breadcrumb/demo_banner, landing, model, msg, router, copy, demo_fixtures, demo_analytics + FFI, tests, scripts/lint_demo_network*.py, pdf_prebake + FFI + baked PDFs, routes, test.yml, .gitignore, mock html, field-notes))
--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-demo-mode-r5/AGENTS.md first.
--- SPEC / CONTEXT ---
Read ALL of these before reviewing:
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/spec/righttenantry-demo-mode.md   (original job briefing - the spec)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/spec/issue-628.json               (GitHub issue #628 - research + design)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/spec/pr-629-body.md               (PR body - carries the lavish verdict, which is CANON: do not re-judge the approved design, only the shipped fidelity to it)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/spec/perkins-briefing-r5.md       (round guards - binding on you)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/spec/r4-consolidated.json         (round-4 findings - the fix-audit target)
--- FIX-AUDIT DUTY (this round) ---
The r4 head commit (2330189) claims, per its message:
- B1 (r4 blocker): the no-network lint's DEMO_BRANCHED_HELPERS skip is DELETED; every helper fn is now verified by (a) an equal-or-shallower-depth `case <receiver>.demo_mode` guard matched as a case STATEMENT for ANY receiver (model/updated_model/saving, incl. multi-subject cases), or (b) FN_INTERCEPTED_TRIGGERS manifest verification (fn reachable only from messages demo_update.handle intercepts; trigger set checked against DEMO_INTERCEPTED so drift fails). The r4-added demo branches in fire_refcheck_slot_action/fire_refcheck_call_action/save_refcheck_edit were DEAD CODE and are deleted. New bite-tests 4-7 (unlisted unguarded helper fails, comment mention fails, any-receiver guard passes, non-intercepted fn trigger fails).
- B2 (r4 blocker): demo ENTRY now has dispatch-level pins - both paths (landing-CTA /demo nav + is_demo_route deep-link boot) driven through client.update on a NON-demo model, asserting demo_mode, seeded store, swapped mock-landlord auth, dashboard NotAsked -> Loading.
- Warning folds claimed: W1 enter_demo stashes real auth+csrf (demo_saved_auth/demo_saved_csrf), nav-exit restores via clear_demo_state, logout drops stash - pinned both ways; W8 post-exit browser Back to a demo deep link re-enters demo (is_demo_route consulted in the nav arm); W9 ApiReturnedPolicyRefresh gets the same demo guard as ApiReturnedSession; W10 ?payment=success/?extended=success demo arms batch accumulated route-fetch eff; W11 demo mark-all-read sets unread_count: 0 optimistically; W12 Grace baked-PDF flag arithmetic fixed (240000/245000 = 98%) + PDFs re-baked; W13 dispatch pins for load-more/comparison/awaiting/scoring request arms; W14 scoring in_progress=pending pinned on v-harbour + remindable/followup pinned on v-maples; W15 dead refcheck-helper demo branches deleted; W16 reset_demo seed-failure exits to landing with brand-voice toast; via-nav exit pin asserts all 15 cleared fields; change_status audit trigger derives from event kind.

For each r4 finding touching YOUR chunk's files (see r4-consolidated.json), re-read the cited code IN THE WORKTREE and classify fixed / still-present. Emit still-present ones titled 'still present since round 4: <prior title>' with FRESH evidence of your own. Never re-emit verified-fixed ones. A fix CLAIMED but not actually biting is a NEW blocker (severity blocker, title prefixed 'claimed-fix did not bite:').
--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift - changes not asked for by the spec

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).

--- ROUND GUARDS (from the briefing - binding) ---
- ONE hard blocker class: the no-network pillar. Demo mode issues ZERO real API calls; the lint (scripts/lint_demo_network.py + bite-tests) is the mechanism and MUST bite - a vacuously-passing lint is a blocker (the r3-B3/r4-B1 class). Verify the mechanism, not just the green run.
- Also verify the W1 session stash/restore pin (nav-exit restores real auth+csrf; logout drops) - pinned both ways.
- Flag for verification: W8 post-exit Back re-entry via is_demo_route (code-checkable); W9 ApiReturnedPolicyRefresh demo guard; W10 payment/extended arms eff batching; W11 optimistic unread_count; W12 Grace PDF 98% (was 58%) + re-baked assets; the 8 lint bite-tests actually fail on synthetic violations.
- CI note: GitHub Actions is billing-blocked today. Local suite is ground truth (shared 119 / client 621 / server 1527+549 claimed).
- Do NOT re-litigate: the lavish verdict (CTA moment B persistent banner, FFI approved, fixtures 3+9, hero+nav entry) + applied r1-r4 findings verified fixed; user rulings (demo = real components + mock data, no backend surface, synthetic-footer canon).


--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this absolute path (create nothing else, write nowhere else):
  /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/lenses/acceptance-c.json
Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE - the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output.
- Hedging language ("might", "could", "possibly") is a signal that you have not verified. Either verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer.

When the JSON file is written, STOP. No summary, no prose.
