## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc3-6 · **Reviewed sha:** `6751de1` · **Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 15/16 reviewer findings confirmed against the code — 1 discarded as false-positive. 1 four-source-agreement finding demoted blocker -> warning (see below: the idempotency invariant holds via find/mark live-status scoping + the passing redelivery test).
**CI at `6751de1`:** GREEN (Migration safety, Format/Lint/Unit/Build, Integration Tests, Terraform). Em-dash check: clean.

### Blockers (0)
None.

### Warnings (1)

**W1 — Idempotency claim result is discarded; the claim gates nothing (dead defense-in-depth layer) + misleading comments** `blind` `security` `edge` `architecture`
`server/src/reference_checks/webhooks.gleam:237-262` (`apply_delivery_failure`, step 1)
The `case sql.claim_webhook_event(...)` is a discarded expression (Gleam has no early return): every branch yields `Nil`, then step 2 (`find` + `mark`) runs unconditionally. The "Stand down" / "a crash mid-handler never double-applies" comments overstate what the claim does.

**Not a blocker because the idempotency invariant still holds** — verified: `find_reference_call_by_send_ref` and `mark_awaiting_correction` are both scoped `WHERE status IN ('queued','contact_initiated')`, so a re-delivered event (row now `awaiting_correction`) finds 0 rows and no-ops, never reaching `mark`. `resend_redelivery_is_idempotent_test` (line 123) posts the same svix-id twice and asserts `audit_count == 1` + `notification_count == 1` — it passes (CI green). The claim is a redundant/dead layer, not a live dedup gate.
Fix: remove the dead claim and correct the comments to describe the actual mechanism (find/mark live-status scoping), or keep it as an observability hook and document that it does **not** gate. Do **not** make it early-return on 0 rows — that would turn a crash-after-claim-before-mark into a lost transition (at-most-once); the current fall-through gives better completion semantics.

### Notes (8)

**N1 — AC8 says entity_id = vacancy, but the notification uses the `reference_call` entity** `blind` `acceptance`
`notification_dispatch.gleam:531` calls `dispatch(..., "reference_call", reference_call_id)` — which **mirrors** the sibling `dispatch_reference_notification` (`notify_reference_unreachable` etc., also `reference_call`). The spec self-contradicts: AC8/Dev Note 3 say "entity_id = vacancy (mirror notify_reference_unreachable)", but `notify_reference_unreachable` itself uses `reference_call`. The minion mirrored the existing consistent pattern. No live breakage; confirm which entity the vacancy-panel badge groups on for RC4.3 and align the spec.

**N2 — Missing-signature (missing-header) rejections log but don't capture to Sentry** `blind`
`webhooks.gleam:71-75` (svix `extract_headers` Error) + `:141-145` (missing `X-Twilio-Signature`) only `log_warning`; the bad-signature path **does** capture (`ResendWebhookSignatureFailed`/`TwilioWebhookSignatureFailed`). AC3 says "captured to Sentry" for "missing signature". Minor observability gap on a less-suspicious path.

**N3 — AC3's Twilio replay-window/timestamp clause is unaddressed** `acceptance`
`twilio_webhook.verify_signature` takes no timestamp. Twilio's signing model has no signed timestamp (HMAC over url+sorted params), so replay is mitigated by the idempotency layer instead. The Resend/svix path does have a 5-min replay window. Literal AC3 text for Twilio is unmet; consider amending AC3 to reflect idempotency-based replay protection.

**N4 — `terminal_reason` slug `email_failed` diverges from spec AC1 example + the SQL docstring `delivery_failed`** `acceptance`
`webhooks.gleam:393` stamps `email_failed` for `email.failed`; spec AC1 and the new `mark_awaiting_correction.sql` docstring both say `delivery_failed`. No live consumer (rc3-7's fraud signal isn't built), but reconcile the slug before rc3-7 reads `terminal_reason`.

**N5 — `notify_reference_awaiting_correction` Result discarded via `ignore_result`; comment claims "captured"** `edge`
`webhooks.gleam:299-318`. `dispatch()` does `log_warning` on error (not Sentry), then `ignore_result` swallows it. The "a failure here is captured" comment overstates it (logged, not Sentry'd). Best-effort is intended (AC8) — soften the comment or add a capture.

**N6 — New `query_error_to_string` is a byte-identical copy of `notification_dispatch.debug_query_error` (3rd copy in `ai/scoring_gate.gleam`)** `architecture` `codebase`
`webhooks.gleam:475`. RT AGENTS.md: "DRY: extract helpers when logic repeats 2+ places". The minion acknowledged it (the existing one is private). Extract a public shared stringifier and replace the three copies.

**N7 — Twilio `Disabled`-config branch (AC7) has no test** `tests`
`webhooks.gleam:141-145` (`sms_client.Disabled -> reject_forbidden()`). Documented AC7 behaviour, untested. Add a unit test asserting 403 + no state change with `config.twilio = Disabled`.

**N8 — Twilio redelivery idempotency untested (only Resend redelivery is tested)** `tests`
`resend_redelivery_is_idempotent_test` (line 123) covers the shared path; the Twilio-specific `event_id = MessageSid:status` construction + redelivery has no test. Add a Twilio redelivery test mirroring the Resend one.

### Reviewer agreement
- **W1 (idempotency claim discarded)** — 4 independent reviewers (`blind`, `security`, `edge`, `architecture`) flagged the same code. Highest-confidence signal of the round; the code observation is correct, the severity was corrected on verification (no double-apply).
- **N1 (entity_id)** — `blind` + `acceptance`.
- **N6 (query_error duplication)** — `architecture` + `codebase`.

**Advisory test gate: PASS** (P0 100%: signature-rejection both webhooks, bounce/failure -> awaiting_correction both channels, idempotency, objection stickiness; P1 >=90%; overall >=80%). N7/N8 are minor Twilio gaps that don't drop the gate.

**Rejected (1):** blind's "AC1 lists `email.complaint`, classifier handles `email.complained`" — the code matches Resend's real event type (`email.complained`); the spec text is the typo. (The related slug concern is N4.)

### Verdict
**READY TO MERGE** — 0 blockers. Signature verification is load-bearing and correctly enforced (unverified webhook mutates nothing; both verifiers reject wrong/missing signatures with 401/403; `crypto.secure_compare` used). The idempotency invariant holds (verified via find/mark live-status scoping + the passing redelivery test). CI is green. The 1 warning + 8 notes are non-blocking quality/consistency items for the implementing minion to fold in.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
