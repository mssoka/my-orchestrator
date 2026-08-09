## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-per-applicant-remind · **Reviewed sha:** c6868b8 · **Reviewers:** 7/7 completed
**Verification:** 5/6 findings confirmed against the code — 1 discarded as false-positive

### Blockers (0)

None.

### Warnings (4)

1. **[policy-gate] `ApiReturnedApplicantReminder` omitted from `msg_triggered_policy_reaccept`** — `client/src/client.gleam:391-438`. The bulk sibling `ApiReturnedReminder(Error(e)) -> check(e)` is allowlisted; the new response falls through to `_ -> False`. A policy-reaccept 428 from the per-applicant endpoint shows an error toast instead of surfacing the reaccept modal. Fix: add `ApiReturnedApplicantReminder(Error(e)) -> check(e)` beside the existing arm.

2. **[duplication] `handle_remind_applicant` copy-pastes ~110 lines of `handle_remind_applicants`' scaffolding** — `server/src/inbound_email/inbound_handler.gleam:722-830`. Only the two mark calls differ (extra email arg); transaction body, `valid_recipients`, `clear_rejected_stamps`, spawn, response and error arms are character-identical. The mirror is exact today, but a future atomicity/response change must be hand-synced twice — drift risk on the load-bearing stamp+send contract. Fix: extract a shared transaction core taking the two stamp calls plus a shared spawn+respond tail.

3. **[coverage-gap] Request-validation 400 branches untested** — `server/src/inbound_email/inbound_handler.gleam:667-694`. `require_json`, body-decode, empty-email and invalid-email branches all return 400 and none has a test (every integration call site passes a valid email). Fix: add empty-email, invalid-email, and malformed/missing-body cases asserting 400.

4. **[coverage-gate] Advisory test gate: CONCERNS** — P0 happy paths 100% (stage1/stage2/scoping/row-gating/cross-tenant/closed-vacancy/re-enquiry all pinned). P1 ~87.5%: only the BAD_BODY branches hold the gate under the 90% PASS line. Clearing warning 3 lifts this to PASS.

### Notes (1)

1. **[duplication] Awaiting-refetch block duplicated verbatim** between the bulk and per-applicant success handlers (`client/src/client.gleam:2845-2858` & `2887-2902`). Extract a `refetch_awaiting(model)` helper.

### Reviewer agreement

No finding was independently reported by two lenses (round 1, fresh eyes).

**Verdict:** READY TO MERGE

_Per-applicant Remind button (gate-respecting, no force-remind — user-confirmed); reuses the bulk email plumbing by design. Endpoint is a faithful mirror: same one-transaction stamp → validate → un-stamp → commit, same owner/closed-vacancy 404s, per-sender SQL is the bulk WHERE plus one email predicate, and the view's transaction-stable cadence gate provably suppresses stage-2 in the same transaction where stage-1 stamps (re-enquiry edge pinned by test). All warnings are non-blocking; happy to see them addressed in a follow-up._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
