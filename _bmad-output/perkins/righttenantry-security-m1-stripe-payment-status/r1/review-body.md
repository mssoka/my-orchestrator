## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)
**Job:** righttenantry-security-m1-stripe-payment-status · **Reviewed sha:** `6054a3d` · **Reviewers:** 7/7 completed
**Verification:** 12/13 findings confirmed against the code — 1 discarded as false-positive

### Blockers (0)

None.

### Warnings (2)

**1. `checkout.session.async_payment_failed` is unhandled — a failed delayed payment leaves the row pending forever** · `[blind, edge, acceptance]` · `server/src/payment/webhook_handler.gleam:302-330`
The new state machine settles `PendingPayment` via `async_payment_succeeded` but has no arm for its documented failure twin — it hits the silent unknown-event arm (unclaimed, unlogged, no `fail_payment`, no audit, no notification), and `checkout.session.expired` can't fire for an already-completed session. Reachable for pre-deploy in-flight async sessions the idempotency-tag bump itself acknowledges exist. Fail-closed, so no wrongful unlock — but no terminal transition and no ops signal.
*Fix: route `checkout.session.async_payment_failed` through `handle_checkout_failed` in the router case block.*

**2. A 100%-off promo redemption completes with `payment_status="no_payment_required"` — the gate strands the order permanently** · `[blind, edge]` · `server/src/payment/webhook_handler.gleam:412`
`allow_promotion_codes=true` is preserved, and the code's own contract documents 100% promos as legitimate (`amount_total: 0` is deliberately accepted). Stripe's session `payment_status` enum is `paid`/`unpaid`/`no_payment_required` — a $0 session completes as `no_payment_required` and **nothing follows it** (no async settle, no expired). The gate claims the event and the vacancy stays locked forever, info log only. Pre-deploy this order completed at €0 and unlocked; note this is **not** transitional — card-only doesn't prevent $0 sessions via promo code.
*Fix: treat `no_payment_required` with `amount_total == 0` as terminal success (the €0 amount path already exists), or drop `allow_promotion_codes`; minimally, document that 100%-off codes must never be created.*

### Notes (7)

- **Stripe Dashboard checklist missing the new event subscription** · `deployment/README.md:152-159` — the settle arm only works if the webhook endpoint subscribes `checkout.session.async_payment_succeeded`; the repo's out-of-band checklist documents exactly this dependency class (ToS URL entry) but wasn't extended. One bullet fixes it.
- **MalformedMetadata reasons hardcode `checkout.session.completed`** · `webhook_handler.gleam:575-596` — the `arm` threads through claim/error logs but not these three in-tx reason strings; an async settle failing metadata validation logs contradictory labels.
- **Missing `payment_status` consumed at info level only** · `webhook_handler.gleam:441-457` — fail-closed is right, but a Stripe payload-shape change dropping the field on real paid sessions would strand landlords behind an info log. Consider a Sentry warning event for the structurally-missing case (the consent-absent branch already fires one for a comparable anomaly).
- **`"processing"` isn't a valid session-level `payment_status`** · `payment_integration_test.gleam:649` — Stripe's enum is `paid`/`unpaid`/`no_payment_required`; delayed methods complete as `unpaid`. The fixture is harmless belt-and-braces (gate treats all non-paid identically, and `unpaid` + `missing` cover reality) but the handler doc comments repeat the `processing` claim — worth correcting.
- **Extension SKU never driven through the gate with a non-paid status** · `payment_integration_test.gleam:608` — all pending fixtures hardcode `vacancy_unlock`; one extension-SKU pending case would close the secondary axis.
- **`async_payment_succeeded` only tested with `paid`** · `payment_integration_test.gleam:788` — its non-paid branch is shared and transitively covered, but an arm-specific fixture would pin it.
- **Advisory test gate: PASS** — P0 100% / P1 100% / overall ≥80%. Non-vacuity verified: the pending fixtures assert locked + pending + no-audit + no-burst (they fail if the gate is removed), and the settle test drives the full cycle — unlock, completed row, audit, notification, real `ai_analysis` burst row, replay idempotency — unstubbed.

### Reviewer agreement
Both warnings are multi-source (2–3 independent lenses each) — highest-confidence findings in the report.

**Guard verification (issue #625 acceptance):** gate bites on all four states (processing/unpaid/missing fixtures non-vacuous) ✓ · settle cycle real, end-to-end, no new SQL ✓ · card-only holds — `payment_method_types[0]=card` pinned by tripwire, wallets unaffected, `consent_v3_card_only` consumed in the idempotency-key header ✓ · fail-closed default ✓ · no scope creep into #626 ✓

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha._
