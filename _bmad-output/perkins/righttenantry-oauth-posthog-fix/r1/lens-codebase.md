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


--- YOUR LENS (source: codebase) ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
Focus extra attention on: the email/password path in auth_handler.gleam (process_signup / handle_login) — does complete_oauth_flow's identify+capture mirror it faithfully (same posthog_client calls, same attribution.first_touch_set_once shape, same consent-independence)? The Squirrel codegen (sql.gleam) — does the is_new decode match the SQL's RETURNING order and bool type? The cookie attribute split (identify_cookie_attributes vs sentinel_cookie_attributes) — are ALL former bridge_cookie_attributes call sites updated, none left with the old 10s path? Grep the whole repo for `bridge_cookie_attributes`, `identify_cookie_max_age`, `Max-Age=10` to confirm no stragglers.
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{{
  "source": "codebase",
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

FILE OUTPUT: write ONLY the JSON array (same content) to {OUT}/codebase.json (absolute path — the exact filename given in your lens brief), then stop. Do not print anything else to stdout.

ACCURACY MANDATE — this is the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.
Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.