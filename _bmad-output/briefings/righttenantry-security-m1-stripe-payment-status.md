# Briefing — righttenantry-security-m1-stripe-payment-status (fix-now, audit M-1)

- **Job id:** `righttenantry-security-m1-stripe-payment-status`
- **Repo:** RightTenantry · **Base:** `develop` @ fresh head at dispatch (audit
  sha 17d5f32; Silas resolves current) · **Slug:** `security-m1-stripe-payment-status`
- **GitHub issue:** #625 (the finding, citations, and acceptance live there —
  read it first). Carry `github_issue=625` into the ledger row.
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — a
  well-specified payment-path fix with citations). Any mega-minion you spawn
  launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (web app, Gleam); `project-context.md` /
  AGENTS.md for code conduct. No lavish gate.
- **Perkins:** `pr_review: 1` (payment-path canon surface). **Loop ruling
  (user, 2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr righttenantry-security-m1-stripe-payment-status <url>` yourself.
- **Prior art (from the audit, read these):**
  `_bmad-output/implementation-artifacts/righttenantry-security-audit/security-audit-report.md`
  §M-1 + §L-4/L-7/L-8/L-9 (payment-cluster findings — CONTEXT ONLY, do not
  build them); the codebase's own redaction/verification discipline
  (`redact_token_route`, `secure_compare` patterns) is the quality bar.

## Mission — gate the Stripe unlock webhook on payment truth (issue #625)

**The gap:** `server/src/payment/webhook_handler.gleam:313-380`
(`handle_checkout_completed`) processes `checkout.session.completed` without
checking `payment_status`. Async payment methods (SEPA/Boleto/Klarna —
`payment_method_types` unrestricted in `stripe_client.gleam`) fire the event
with `payment_status: "processing"`/`"unpaid"`; the handler unlocks the
vacancy + fires burst AI scoring before funds settle.

**Fix (either or both, prefer 1 + 2 together):**

1. Gate the unlock path on `payment_status == "paid"`: anything else =
   pending — ack 200 (Stripe must not retry-storm), leave the vacancy locked,
   payment row in a waiting state, deterministic. Settle via
   `payment_intent.succeeded` (add handler if absent) or a second completed
   event carrying `paid`.
2. Restrict `payment_method_types` to `["card"]` at session creation
   (`stripe_client.gleam`) so completed ⇒ paid going forward.

**Acceptance (from issue #625):**

1. Unlock path provably refuses `processing`/`unpaid` completed events —
   test fixtures for EACH state (processing, unpaid, paid).
2. Pending path: vacancy stays locked, payment row waiting, ack 200,
   deterministic — then settles correctly on the succeed path (test).
3. Card-only happy path unregressed (existing suite green + new fixtures).
4. `make test` (test-shared + test-client + test-server + test-js) green —
   local suite is the merge ground truth (CI billing-blocked, ruling
   2026-08-16).
5. PR body: which remediation arms shipped, the pending-state machine, fixture
   list, citations (issue #625, audit report §M-1), and explicitly what was
   NOT built (L-4/L-7/L-8/L-9 stay in the #626 batch).

**Scope guard:** the payment_status gate + method restriction ONLY. L-4
(metadata cross-check), L-7 (refund/dispute), L-8 (signature rotation), L-9
(amount verification), L-5/L-18 — all tracked in #626, all OUT of scope. If
the fix wants to touch the AI burst-scoring trigger beyond
unlock-gating, STOP and flag in the PR.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: security-m1-stripe-payment-status
base: develop
model: deepseek/deepseek-v4-flash
pr_review: 1
github_issue: 625
```
