# Issue #625 — Security M-1 (fix-now): Stripe unlock webhook ignores payment_status — vacancy unlocks before funds settle

(GitHub issue solarity-services/RightTenantry#625, dumped 2026-08-18)

## Finding M-1 (fix-now) — Stripe unlock webhook trusts event shape more than payment truth

**Source:** full-codebase adversarial security audit, 2026-08-18 @ `develop` 17d5f32 (0 Critical / 8 Medium / 25 Low / 14 Info). Full report + 7 lens dossiers: `_bmad-output/implementation-artifacts/righttenantry-security-audit/` (orchestrator workspace).

**Where:** `server/src/payment/webhook_handler.gleam:313-380` (`handle_checkout_completed`) — verified by absence: `payment_status` appears nowhere in the file; the event router dispatches `checkout.session.completed` directly. Related: `stripe_client.gleam` does not restrict `payment_method_types`.

**The gap:** `checkout.session.completed` is processed without checking `payment_status`. With async payment methods (SEPA direct debit, Boleto, Klarna — not restricted at session creation), Stripe fires the event with `payment_status: "processing"` or `"unpaid"`. The handler unlocks the vacancy + fires burst AI scoring immediately; funds may settle later or fail entirely (SEPA chargebacks arrive days later) — leaving an unlocked vacancy with no settled payment. The unlocked vacancy is also keyed from event metadata rather than cross-checked against the payment row (L-4), and there is no refund/dispute handling (L-7) to walk an unlock back.

**Remediation (either or both):**
1. Gate the unlock path on `payment_status == "paid"` — treat anything else as pending (ack 200, wait for `payment_intent.succeeded` or a second completed event).
2. Restrict `payment_method_types` to `["card"]` at session creation so completed ⇒ paid.

**Acceptance:**
- Unlock path provably refuses `processing`/`unpaid` completed events (test fixtures for each state).
- Pending-payment path leaves the vacancy locked and the payment row in a waiting state, deterministically.
- No regression on the card-only happy path (existing tests green + new fixture coverage).
- Local test suite is the merge ground truth (CI billing-blocked; see ruling 2026-08-16).

**Related batch items** (tracked separately in the batch issue): L-4 metadata cross-check, L-7 refund/dispute handling, L-8 signature rotation window, L-9 amount verification.
