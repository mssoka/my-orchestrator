# LENS: security (source tag: `security`) — Perkins r5 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/_shared.md`
FIRST (shared context, inputs, lens-guards, output contract), then
`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/prior-findings.md`
(the r5 FIX AUDIT list — you own the security-class items: B1 TOCTOU, W1 legacy co-nudge,
N10 vacancy-check error, N11 exhaust-row error swallow).

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

**Round 5 — VERIFY-DON'T-REOPEN: FIRST classify each prior security-class finding against
the current worktree (fixed = silent; still present/wrong fix = finding with original
severity, title prefixed `STILL PRESENT (r4): `). Then hunt NEW issues.**

**Round-specific checks:**

1. **B1 TOCTOU — the round's #1 mandate.** The wrong-person route's awaiting transition must
   carry the `taken_over_at IS NULL` backstop in the EXECUTED path (see _shared.md). A
   spoofed/redelivered wrong-person POST (the public form is token-gated but tokens can be
   shared/forwarded) must NOT be able to yank a landlord-handled row into
   `awaiting_correction`. Verify `apply_wrong_person` executes
   `mark_awaiting_correction_wrong_person` (both backstops), the 0-row arm redirects with
   no transition/audit, and the read-time arms stand down.
2. **Ownership + authorization (AD-14 / AC5).** Every action endpoint ownership-checked;
   the app↔vacancy precheck holds for all arms. N10: a DB error on the vacancy check must
   NOT fall through to `action()` (verify the Error arm → 500).
3. **Pre-state guards (AD-14).** Conditional UPDATEs on every transition; 0-row stands down
   gracefully; no read-then-write without a guard.
4. **Stale-bounce gates (W1/W2).** The legacy co-nudge batch-shape exclusion must not create
   a new hole: can a GENUINE failure be masked? (Check: the sweep always appends an sms
   sibling — delivered or skipped — at the same `at`, so genuine referee email sends are
   never single-email batches.) The fallback legs remain pre-correction only.
5. **Substitute idempotency + authz.** Row-id guessing across landlords; successor row
   ownership; double-submit re-audit; identical-trio 400 (N7: effective basis — a stale
   re-submit of the pre-correction trio must NOT 200-no-op and silently drop the typed
   referee); history-row re-submit 409.
6. **Public form paths touched** (form_handler, webhooks, wrong-person route): token-gated by
   construction; webhook handlers must verify provider signatures — a failure event must NOT
   be forgeable to flip rows to unreachable + referee_contact_invalid.
7. **The `?slot=` per-row start param.** Unknown/foreign slot values rejected; no
   cross-tenant start/skip via crafted slot.
8. **Data exposure.** New payload keys (taken_over_at, corrected_at, corrected_* trio,
   correction_cycles) — landlord-only; nothing leaks to the applicant-facing routes or
   logs. New error strings must not leak raw internals (check `db_failure`'s message vs the
   log line).
9. **Client-side.** New API calls — CSRF/cookie handling consistent; error responses wrapped
   in brand copy, never raw server errors.

For each finding, verify against the worktree: read the handler, the SQL, the router arm,
the webhook verifier. Quote exact lines in `evidence`.
