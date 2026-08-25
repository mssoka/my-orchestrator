# LENS: security (source tag: `security`) — Perkins r2 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/lens-briefs/prior-findings.md` (the FIX AUDIT list — you own the security-class items: W1 em-dashes, W3 stale-bounce gate, W8 late-response guard, W10 app↔vacancy precheck).

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

**This is round 2 of a re-review: FIRST classify each prior security-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r1): `). Then hunt NEW issues.**

**Round-specific checks (this PR adds a landlord actions surface — server/src/reference_checks/actions_handler.gleam + router arms):**

1. **Ownership + authorization (AD-14 / AC5).** Every new action endpoint (take-over, correct, substitute, start/skip via RC2.3) must be ownership-checked: the authenticated landlord must own the application/vacancy the row belongs to — not just the row id. Check how the handler resolves the row → application → vacancy → landlord-owner chain. A row-id-only check (no ownership join) = a blocker-class authz gap. Verify against the SQL (do the UPDATEs join through `application` → `vacancy` → landlord?). The r1 W10 fix: the new `verify_application_in_vacancy.sql` must bind path `vacancy_id` to path `application_id` so a same-owner cross-vacancy mismatch cannot 200.
2. **Pre-state guards (AD-14).** Are the transitions conditional UPDATEs (`WHERE id=$1 AND status=<expected>`)? A handler that reads state then updates without the guard allows race/abuse (double correction, take-over from terminal states). 0-row-result must stand down gracefully.
3. **Substitute idempotency + authz.** The substitute CTE creates a new row — can a landlord substitute a row in ANOTHER landlord's application (row-id guessing)? Is the successor row created with the same ownership? Does double-submit re-audit (audit spam / duplicate rows)? The new creation-fraud stamping on substituted rows (r1 N1) — is it actually applied?
4. **The public form paths touched** (form_handler, webhooks, wrong-person route): token-gated by construction (capability token ~288-bit); exhaustion at webhooks must verify provider signatures (svix/Twilio) — the webhook handler must NOT be callable unauthenticated to flip rows to `unreachable` (a DoS/state-corruption vector). The r1 W3 stale-bounce gate (`corrected_at`) — a spoofed/redelivered pre-correction failure must stand down, not fabricate a `referee_contact_invalid` fraud signal.
5. **The `?slot=` per-row start param** on the RC2.3 endpoint: unknown/foreign slot values — rejected or ignored? Can a landlord start/skip a row they don't own via a crafted slot?
6. **Data exposure.** The detail payload now carries `corrected_email`/`corrected_phone`/`taken_over_at`/`correction_cycles` (additive keys) — anything sensitive leaking to the wrong caller? The referee contact chips are landlord-only (already established) — new keys must stay behind the same auth. The r1 W8 late-response guard: a stale `ApiReturnedRefcheckAction` must not toast/refetch on an unrelated page (route check in the id-match guard).
7. **Client-side.** New API calls (reference_checks_api.gleam) — CSRF/cookie handling consistent with existing api patterns? Error responses not leaking raw server errors into user-facing copy (brand voice)?

For each finding, verify against the worktree: read the handler, the SQL, the router arm, the webhook verifier. Quote exact lines in `evidence`.
