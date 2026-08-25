# LENS: security (source tag: `security`) — Perkins r3 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/prior-findings.md` (the FIX AUDIT list — you own the security-class items: the r2 BLOCKER (failure-path stand-down on taken-over rows), r2 W1 (stale-bounce), r2 W3 (route-guarded late-response drop), r2 N6 (concurrent substitute), r2 N7 (fraud re-stamp on idempotent no-op), r2 N10 (authz negatives)).

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

**This is round 3 of a re-review: FIRST classify each prior security-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r2): `). Then hunt NEW issues.**

**Round-specific checks (this PR adds a landlord actions surface — server/src/reference_checks/actions_handler.gleam + router arms):**

1. **Ownership + authorization (AD-14 / AC5).** Every new action endpoint (take-over, correct, substitute, start/skip via RC2.3) must be ownership-checked: the authenticated landlord must own the application/vacancy the row belongs to — not just the row id. Check how the handler resolves the row → application → vacancy → landlord-owner chain. The app↔vacancy precheck (`verify_application_in_vacancy.sql` binding path `vacancy_id` to path `application_id`) must still hold.
2. **Pre-state guards (AD-14).** Are the transitions conditional UPDATEs (`WHERE id=$1 AND status=<expected>`)? A handler that reads state then updates without the guard allows race/abuse (double correction, take-over from terminal states). 0-row-result must stand down gracefully.
3. **THE r2 BLOCKER — failure paths vs take-over.** The delivery-failure (`find_reference_call_by_send_ref.sql`) and wrong-person route must stand down taken-over rows: a redelivered/spoofed failure event must NOT be able to yank a landlord-handled row into `awaiting_correction` or exhaust it to `unreachable` + `referee_contact_invalid` (state corruption on a row the landlord is actively handling).
4. **Stale-bounce gate (r2 W1).** The gate moved into SQL as typed `timestamptz >= timestamptz` — a redelivered PRE-correction failure must stand down, not fabricate a `referee_contact_invalid` fraud signal. Verify the SQL comparison is genuinely typed (no lexical `::text` compare) and NULL-safe.
5. **Substitute idempotency + authz.** The substitute CTE creates a new row — can a landlord substitute a row in ANOTHER landlord's application (row-id guessing)? Is the successor row created with the same ownership? Does double-submit re-audit (audit spam / duplicate rows)? **The r2 W5/W7 guard rails: identical-trio → 400; history-row re-submit with different details → 409 (no silent drop of the new trio). The r2 N7: the idempotent no-op must NOT re-stamp creation fraud on the existing successor (a full overwrite wiping submission-time `form_session`).** The creation-fraud stamp must apply only on REAL inserts.
6. **The public form paths touched** (form_handler, webhooks, wrong-person route): token-gated by construction (capability token ~288-bit); exhaustion at webhooks must verify provider signatures (svix/Twilio) — the webhook handler must NOT be callable unauthenticated to flip rows to `unreachable` (a DoS/state-corruption vector).
7. **The `?slot=` per-row start param** on the RC2.3 endpoint: unknown/foreign slot values — rejected or ignored? Can a landlord start/skip a row they don't own via a crafted slot?
8. **Data exposure.** The detail payload now carries `corrected_email`/`corrected_phone`/`taken_over_at`/`correction_cycles` (additive keys) — anything sensitive leaking to the wrong caller? The referee contact chips are landlord-only (already established) — new keys must stay behind the same auth. **The r2 W3 fix: a stale `ApiReturnedRefcheckAction` must be dropped unless the current route is the same `ApplicationDetail` — no toast/refetch on unrelated pages (route check in the id-match guard).**
9. **Client-side.** New API calls (reference_checks_api.gleam) — CSRF/cookie handling consistent with existing api patterns? Error responses not leaking raw server errors into user-facing copy (brand voice)?

For each finding, verify against the worktree: read the handler, the SQL, the router arm, the webhook verifier. Quote exact lines in `evidence`.
