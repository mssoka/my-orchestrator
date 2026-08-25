You are reviewing a code diff as one lens of an automated multi-lens code review (Perkins round 4, job: righttenantry-demo-mode, PR #629, reviewed sha 4bff855 - the r3-rework head. THIS ROUND IS A FIX AUDIT: the r3 findings (in r3-consolidated.json) were reworked at this sha; verify claimed fixes against the FRESH tree - a fix that didn't bite is a NEW blocker, a landed fix is verified-FIXED.)

You have read-only access to the repository and may verify the diff's claims against the actual codebase using your tools (read files, grep). All verification reads happen in the worktree - a checkout at exactly the reviewed state:
  WORKTREE: /Users/moses/.herdr/worktrees/RightTenantry/perkins-demo-mode-r4

The diff you review is EXACTLY these bytes (a file-group chunk of the full PR diff - never re-fetch or regenerate the diff):
  DIFF CHUNK: /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/chunk-a.patch
  (chunk a = client/src/client.gleam)

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-demo-mode-r4/AGENTS.md first.

--- SPEC / CONTEXT ---
Read ALL of these before reviewing:
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/spec/righttenantry-demo-mode.md   (original job briefing - the spec)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/spec/issue-628.json               (GitHub issue #628 - research + design)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/spec/pr-629-body.md               (PR body - carries the lavish verdict, which is CANON: do not re-judge the approved design, only the shipped fidelity to it)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/spec/perkins-briefing-r4.md       (round guards - the acceptance pillars and the r4 fix-audit bar; its Lens-guards section is binding on you)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/spec/r3-consolidated.json         (round-3 findings - prior findings for the fix audit)

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad - list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself - no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

FIX-AUDIT DUTY (this round): r3's consolidated findings list 4 blockers + 15 warnings + 29 notes. For each prior finding touching your chunk's files, classify the cited code as fixed or still-present IN THE WORKTREE (re-read the code, never trust the prior wording). Emit still-present ones as findings titled 'still present since round 3: <prior title>' with your own fresh evidence; do not re-emit verified-fixed ones. The four r3 blockers and what the rework claims:
- B1: in-demo /demo nav after deep-link boot strands dashboard skeleton -> claimed fix: fetch gate now covers routes.Demo|Dashboard
- B2: CI grep lint self-trips on demo_api.gleam's own api/api_error import -> claimed fix: lint narrowed to network-capable modules
- B3: lint_demo_network.py unsound (cross-arm bleed, comment-only DEMO_INTERCEPTED, no bite-tests) -> claimed fix: arm-bounded window + manifest check vs demo_update.handle + 3 bite-tests wired into test.yml
- B4: advisory test gate FAIL -> claimed fix: all-15-field exit-hygiene pins, close/archive/restore/status-change/refcheck/deep-link dispatch pins, add_days_iso rollover pin

ROUND GUARDS (from the briefing - binding):
- ONE hard blocker class: the no-network pillar. Demo mode issues ZERO real API calls. Every api call site demo-reachable must be intercepted/guarded. If the lint passes vacuously, that is itself a blocker.
- Do NOT re-litigate: the lavish verdict (CTA moment B, persistent banner, FFI approved, fixtures 3+9, hero+nav), r1/r2/r3 applied findings already verified fixed, user rulings (demo = real components + mock data; no backend surface; 'Synthetic demo data' footer canon).
- Pillar check: demo issues NO writes to real endpoints incl. settings/password/account-deletion reachability, payment/unlock CTAs, bulk-reject, report download (the ONLY permitted network touch), refetch surfaces.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this absolute path (create nothing else, write nowhere else):
  /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/lenses/edge-a.json
Each element must match this schema exactly:
{
  "source": "edge",
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
- Hedging language ("might", "could", "possibly") is a signal you have not verified. Either verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer.

When the JSON file is written, STOP. No summary, no prose.
