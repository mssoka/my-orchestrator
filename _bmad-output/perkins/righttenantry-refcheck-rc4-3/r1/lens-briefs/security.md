# LENS: security (source tag: `security`) — Perkins r1 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract).

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

**Round-specific checks (this PR adds a landlord actions surface — server/src/reference_checks/actions_handler.gleam + router arms):**

1. **Ownership + authorization (AD-14 / AC5).** Every new action endpoint (take-over, correct, substitute, start/skip via RC2.3) must be ownership-checked: the authenticated landlord must own the application/vacancy the row belongs to — not just the row id. Check how the handler resolves the row → application → vacancy → landlord-owner chain. A row-id-only check (no ownership join) = a blocker-class authz gap. Verify against the SQL (do the UPDATEs join through `application` → `vacancy` → landlord?).
2. **Pre-state guards (AD-14).** Are the transitions conditional UPDATEs (`WHERE id=$1 AND status=<expected>`)? A handler that reads state then updates without the guard allows race/abuse (double correction, take-over from terminal states). 0-row-result must stand down gracefully.
3. **Substitute idempotency + authz.** The substitute CTE creates a new row — can a landlord substitute a row in ANOTHER landlord's application (row-id guessing)? Is the successor row created with the same ownership? Does double-submit re-audit (audit spam / duplicate rows)?
4. **The public form paths touched** (form_handler, webhooks, wrong-person route): token-gated by construction (capability token ~288-bit); exhaustion at webhooks must verify provider signatures (svix/Twilio) — the webhook handler must NOT be callable unauthenticated to flip rows to `unreachable` (a DoS/state-corruption vector).
5. **The `?slot=` per-row start param** on the RC2.3 endpoint: unknown/foreign slot values — rejected or ignored? Can a landlord start/skip a row they don't own via a crafted slot?
6. **Data exposure.** The detail payload now carries `corrected_email`/`corrected_phone`/`taken_over_at`/`correction_cycles` (additive keys) — anything sensitive leaking to the wrong caller? The referee contact chips are landlord-only (already established) — new keys must stay behind the same auth.
7. **Client-side.** New API calls (reference_checks_api.gleam) — CSRF/cookie handling consistent with existing api patterns? Error responses not leaking raw server errors into user-facing copy (brand voice)?

For each finding, verify against the worktree: read the handler, the SQL, the router arm, the webhook verifier. Quote exact lines in `evidence`.
