You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- CANONICAL DIFF ---
Read /Users/moses/code/_bmad-output/perkins/righttenantry-oauth-posthog-fix/r1/diff.patch
Review EXACTLY these bytes. Never re-fetch or regenerate the diff (no `gh pr diff`, no `git diff`, no fetching PR data). Do not read the PR page or issue tracker.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-oauth-posthog-fix-r1/AGENTS.md

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/righttenantry-oauth-posthog-fix.md

--- ROUND CONTEXT (Perkins round-1 briefing; load-bearing surfaces to verify independently) ---
This is an analytics-tracking (PostHog) PR on the Google OAuth callback path of a Gleam/Wisp server + Lustre SPA. Claims:
1. PostHog threaded through the OAuth chain (router.gleam -> handle_oauth_callback -> process_oauth_callback -> complete_oauth_flow).
2. Server-side identify_with_set_once (email $set) + capture of signup_completed (first OAuth sign-in) or login_succeeded (returning), distinguished atomically via a new `(xmax = 0) AS is_new` insert-flag in the upsert's RETURNING.
3. Identify-bridge cookie rt_landlord_id lifetime 10s -> 60s; sentinels (rt_landlord_external_id, rt_ph_reset) deliberately stay at 10s.
4. Reset-arm now also clears rt_landlord_id in the inline analytics snippet.
Surfaces to verify independently:
- `(xmax = 0) AS is_new` atomicity: is the first-vs-returning distinction genuinely atomic (no TOCTOU vs a pre-check SELECT)? Does it codegen to Bool? Is signup_completed vs login_succeeded selected with the right polarity? A wrong polarity = wrong event for every OAuth sign-in.
- 4-place inline-snippet contract: the analytics bridge snippet lives in BOTH Makefile (build-client) and Dockerfile perl chains, each with its own substring-pin guard list. Any snippet change must hit all 4 (2 chains + 2 guards). Verify the reset-arm change (document.cookie="rt_landlord_id=; Max-Age=0; Path=/; SameSite=Lax";rtPhId=null) landed in all 4 and the guard pins are substrings UNIQUE to the changed arm.
- Cookie-lifetime contract: rt_landlord_id (identify, 60s) vs the two sentinels (10s) is pinned in test assertions + build guards + doc comments. Verify no sentinel accidentally widened and no narrowing of the identify cookie.
- Identify/capture correctness: identify fires with the landlord row.id + email (same shape as email/password path); capture is consent-independent firing matching the email/password path. Anonymous->identified merge must stay possible (the identify cookie is the only client-side merge link).
- Scope discipline: login_succeeded is OAuth-scoped by design (email/password deliberately skips it). Cross-provider login_succeeded on email path, no first-touch attribution on OAuth (UTM dies in redirect), and cross-provider returning = new signup are DISCLOSED follow-ups, NOT gaps — treat as notes/acknowledged-limitations unless the implementation contradicts the disclosure.


--- YOUR LENS (source: tests) ---
Test coverage analysis via traceability.
For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap
Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests
Test level mix (unit/integration/E2E): flag mismatches as findings.
Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate
Gate thresholds: PASS: P0 100%, P1 >=90%, overall >=80% | CONCERNS: P0 100%, P1 80-89%, overall >=80% | FAIL: P0 <100%, or P1 <80%, or overall <80%.
Round-specific: the OAuth funnel tests (oauth_first_signin_fires_identify_and_signup_completed_test, oauth_returning_signin_fires_login_succeeded_test) drive complete_oauth_flow with a fabricated token against the real DB — assess whether the is_new polarity, the identify/capture order, the 60s cookie, and the reset-arm snippet change each have adequate coverage (the snippet change is only covered by grep-guard pins, not runtime tests — assess that gap).
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings with no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

FILE OUTPUT: write ONLY the JSON array (same content) to {OUT}/tests.json (absolute path — the exact filename given in your lens brief), then stop. Do not print anything else to stdout.

ACCURACY MANDATE — this is the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.
Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.