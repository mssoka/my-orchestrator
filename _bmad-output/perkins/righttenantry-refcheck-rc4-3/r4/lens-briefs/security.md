# LENS: security (source tag: `security`) — Perkins r4 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/prior-findings.md` (the r4 FIX AUDIT list — you own the security-class items: the r3 TOCTOU BLOCKER, r3 W2 fallback-leg, r3 W4 sweep-terminal guards, r3 N13 exhaust error swallow).

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

**Round 4 — VERIFY-DON'T-REOPEN: FIRST classify each prior security-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r3): `). Then hunt NEW issues.**

**Round-specific checks:**

1. **THE r3 TOCTOU BLOCKER — the round's #1 mandate.** The wrong-person route's awaiting transition must carry the `taken_over_at IS NULL` backstop in the EXECUTED path (see _shared.md for the full mandate). A spoofed/redelivered wrong-person POST (the public form is token-gated but tokens can be shared/forwarded) must NOT be able to yank a landlord-handled row into `awaiting_correction`. If `apply_wrong_person` still executes `update_reference_call_status` (unguarded on taken_over_at), the race is open — a state-corruption vector. Verify in the worktree.
2. **Ownership + authorization (AD-14 / AC5).** Every new action endpoint (take-over, correct, substitute, start/skip) ownership-checked: landlord owns the application/vacancy the row belongs to. The app↔vacancy precheck (`verify_application_in_vacancy.sql`) must still hold for all action arms.
3. **Pre-state guards (AD-14).** Conditional UPDATEs (`WHERE id=$1 AND status=<expected>`) on every transition; 0-row-result stands down gracefully; no read-then-write without a guard.
4. **Stale-bounce gates (r3 W2/W3).** The fallback leg pre-correction-only rule and the co-nudge exclusion must not create a new hole: can a GENUINE failure be masked (e.g. an attacker-supplied send_ref that lands in the fallback leg post-correction → the row never exhausts → the referee is re-contacted forever)? Balance: stand-down vs genuine-detection.
5. **Substitute idempotency + authz.** Row-id guessing across landlords; successor row ownership; double-submit re-audit; identical-trio 400; history-row re-submit 409; creation-fraud stamp only on REAL inserts.
6. **Public form paths touched** (form_handler, webhooks, wrong-person route): token-gated by construction; webhook handlers must verify provider signatures (svix/Twilio) — a failure event must NOT be forgeable to flip rows to `unreachable` + `referee_contact_invalid`.
7. **The `?slot=` per-row start param.** Unknown/foreign slot values rejected; no cross-tenant start/skip via crafted slot.
8. **Data exposure.** New payload keys (`taken_over_at`, `corrected_at`, `correction_cycles`, corrected trio) — landlord-only behind the same auth; nothing leaks to the applicant-facing routes or logs. New error strings must not leak raw internals.
9. **Client-side.** New API calls (reference_checks_api.gleam) — CSRF/cookie handling consistent; error responses wrapped in brand copy, never raw server errors.

For each finding, verify against the worktree: read the handler, the SQL, the router arm, the webhook verifier. Quote exact lines in `evidence`.
