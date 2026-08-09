## 🤖 Perkins automated review — round 2 of 3

**Job:** righttenantry-per-applicant-remind · **Reviewed sha:** b48b581 · **Reviewers:** 7/7 completed
**Verification:** 3/4 findings confirmed against the code — 1 discarded as false-positive
**Prior-round fix audit:** r1 W1 (allowlist) **addressed** · r1 W3 (validation tests) **addressed** · r1 W2 (copy-paste) **deferred-follow-up, not-folded** · r1 W4 (test-gate) **PASS — P1 lifted 87.5% → 100%**

### Blockers (0)

None.

### Warnings (0)

None.

### Notes (3)

1. **[coverage-gate] Advisory test gate: PASS (r1 W4 resolved)** — `server/test/integration/awaiting_integration_test.gleam:831`. P0 100%; P1 8/8 = 100% (was 7/8 = 87.5% in r1). The three new `rejects_*` tests close the only BAD_BODY gap and each exercises a distinct branch (decode Error / empty email / invalid email), each asserting 400 + zero stamps on both stamp columns — real tests, not tautologies.

2. **[copy] Both-zero per-applicant toast asserts "already had both reminders" but 0,0 also covers applied-since-load** — `client/src/copy.gleam:513`. Spec matrix maps APPLIED_SINCE_LOAD to `{0,0}`/200; in that race the toast is technically imprecise. Transient toast in a defensive race the doc comment already acknowledges; the bulk 0,0 arm ("Everyone's already had their reminders.") is equally ambiguous. Optional: vaguer copy ("No reminder needed."); consistent with the bulk pattern either way.

3. **[coverage-gap] `wisp.require_json` no-body/non-JSON 400 path untested for remind-applicant** — `server/src/inbound_email/inbound_handler.gleam:668`. The new malformed-body test posts valid JSON `{}`, so it hits the decode Error arm rather than require_json's rejection. Framework guard, symmetric with the bulk endpoint (also untested there). Optional follow-up; not required for the gate.

### Reviewer agreement

No finding was independently reported by two lenses this round. The one warning (stage-2 applied-sender guard "missing" from `mark_followup_for_sender.sql`) was **rejected as a false positive** on verification: the applied-sender exclusion lives in the `inbound_email_sender_state` view — the single home of the rule, consumed by both bulk and per-applicant stage-2 SQL (the SQL header comment states this) — and is pinned by `followup_excludes_applied_enquirers_test` (`awaiting_integration_test.gleam:431`). An applied enquirer has no view row, so no stamp, no send; the mirror remains exact.

**Verdict:** READY TO MERGE

_Fix-audit confirms both fold-ins: W1's allowlist arm is correct and complete (pattern matches the variant, wired end-to-end to the reaccept modal, no parallel allowlist missed), W3's tests genuinely exercise the 400 branches and bite. No-regression: fold-in touches exactly the two intended files, backend mirror exact, re-enquiry edge still pinned, no em-dashes in user-facing copy; all suites green at this sha (server unit 1221, integration 393 incl. the 3 new tests, client 463). W2 + N1 remain deliberately deferred (tracked follow-up)._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
