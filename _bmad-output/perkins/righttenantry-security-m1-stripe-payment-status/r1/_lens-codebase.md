# Lens: Codebase Fit (source: `codebase`)

Read your shared context first: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/_shared.md` — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `codebase`. Your output path is: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/codebase.json`

--- YOUR LENS ---

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specific fit checks for this diff:
- `checkout_session_form_body` is `@internal pub` — does the Gleam project use this visibility pattern elsewhere for test-pinned internals? Does `create_checkout_session` now call it with EXACTLY the same arguments/behaviour as the old inline list (no dropped field, no reordered encode semantics — compare the old diff hunk against the new function body field by field)?
- The idempotency tag `consent_v3_card_only` — confirm it flows through `checkout_idempotency_key` (or equivalent) into the actual `Idempotency-Key` header on `POST /v1/checkout/sessions`, and that no OTHER caller of the old tag string remains (grep `consent_v2_promo`).
- `decode.optionally_at` usage for `payment_status` — is that the established decode pattern in this file for optional nested fields (compare with `consent_terms` / `amount_total` decoders just above)?
- `sql.claim_stripe_event(tx, event_id, arm)` — does the SQL layer accept a free-form event_type label, and do the round's claims about "no new SQL" hold (check `server/src/payment/sql/` for any new .sql file vs reuse)?
- Test helpers: `build_event_body_with_options` now delegates to `build_event_body_full`; check every existing caller of the old helper still compiles/serves, and `build_event_with_consent` got the `payment_status` field added — are there OTHER event-body builders in the test suite (or other test files posting `checkout.session.completed`) that did NOT get a payment_status default and would now silently take the pending path (which would be a behaviour flip, not a compile error)?
- `count_audit_for_event`, `count_payment_notifications`, `count_processed_event`, `test_db.seed_payment` — do these helpers exist with these signatures?
