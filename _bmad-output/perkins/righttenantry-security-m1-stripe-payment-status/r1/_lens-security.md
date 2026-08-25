# Lens: Security (source: `security`)

Read your shared context first: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/_shared.md` — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `security`. Your output path is: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/security.json`

--- YOUR LENS ---

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a payment-path diff (Stripe webhook + checkout session creation), so additionally trace:
- Webhook authenticity: does the new `checkout.session.async_payment_succeeded` arm inherit the same signature verification + event-id claim/idempotency as `checkout.session.completed`? (It must — no new unauthenticated surface.)
- Can a crafted event (attacker-controlled `payment_status`, missing field, null, non-string) reach the unlock path? The gate must fail CLOSED — verify the decode + `option.unwrap(payment_status, "")` + `case payment_status { "paid" -> ... _ -> pending }` chain actually closes every non-"paid" value including empty string, null, absent, and case variants like "Paid".
- The PendingPayment branch claims the event then acks 200 with only a log line — is anything sensitive logged? Is there any way the claim-without-process state can be abused (event-id squatting on a future settle)?
- DoS/abuse: unauthenticated webhook spam creating unbounded `processed_stripe_event` rows via the pending path (each unique event id claims a row) — was that already the pre-existing shape for every arm (then not a regression), or does the new arm widen it?
- `checkout_session_form_body`: parameter injection via the new form fields; secrets in the idempotency-key hash path.
