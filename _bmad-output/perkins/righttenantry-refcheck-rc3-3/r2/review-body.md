## 🤖 Perkins automated review — round 2 of 3 (fix-audit)

**Job:** righttenantry-refcheck-rc3-3 · **Reviewed sha:** `84f5b94` (r1 was `a0b6910`) · **Reviewers:** 22/28 completed (c1 7/7 · c2 7/7 · c3 7/7 · c4 1/7 — test-files chunk scoped to the test-quality lens; the other 6 lenses on pure test files were deliberately omitted as near-zero value, test quality having been assessed by tests-c1/c2/c3 which directly reviewed the test code)

**r1 audit:** 1/1 blockers FIXED · 11/11 warnings FIXED, 0 still open (carried) · notes folded into the rework (key notes verified fixed: `restore_form_token` guard, `month_year` canonicalization, brand-header dedup, read-side tests, slot renderer tests)

**Verification:** 14/14 findings confirmed against the code — 0 discarded as false-positive

### Fix-audit summary (the priority deliverable)

- **B1 (blocker) — VERIFIED FIXED.** `csrf.should_skip` now has `["reference", ..] -> True` (`csrf.gleam:110`) + a `csrf_test` pin **with a session cookie** (`csrf_test.gleam:101`) + two router-stack integration tests through the full `router.handle_request` + `rt_session` asserting **303 + answer persisted (not 403)** + the AC7 typo-deep-link 404 test. A session-carrying referee no longer loses their answer.
- **W1–W11 — ALL FIXED** (code-traced + test-executed, not commit-message claims). Notable: W2 input retention via a new `prefill_override` param; W4 PUT error contract pinned across 404/409/400/bot-200; W6 cap raised to 11d (> 10d TTL) with a dedicated test; W7 resend audit pinned via an injected `delivered_send` seam asserting remint + audit row + token death.
- **Fifth-registry-gap hunt (priority focus) — NONE FOUND.** All four path-branching registries carry `/reference`: `csrf.should_skip`, `is_public_path`, `redact_token_route`, the router table (5 arms incl. catch-all). `is_policy_gate_exempt` is correctly scoped to authenticated `/api/v1` routes (the `/reference` route is public — `session_middleware` never runs for it). CSP is global. **Independently confirmed by `security-c2` and `security-c3`, both of which returned `[]`.**
- **Em-dash check — NONE in user-facing copy.** Every em-dash detected is in developer comments/docstrings; zero inside any string literal rendered to users. r1's zero-em-dash verification holds.

### Blockers (0)

None.

### Warnings (2)

1. **Resend POST abuse posture (AD-15 fake-success) handler branch is unpinned** — `form_handler.gleam:524-529`. The answer-POST bot path *is* tested (`honeypot_filled_post_saves_nothing_test`); the resend bot path is not (every resend test sends an empty `_website`). The honeypot guard defends token remint — a regression dropping it would let bots trigger remints and pass CI. *Fix: mirror the answer-path honeypot test for `POST /resend`.*

2. **Complete-draft review-screen GET dispatch untested at handler level** — `form_handler.gleam:164-171` (`_, None, None -> view_review`). This is the server-side destination of the W1 desktop-nav fix. `view_review` is unit-tested but no integration test seeds a complete draft and GETs the bare URL to assert `reference-review` renders; the resume test only covers the partial-draft case. *Fix: add an integration test filling every draft key, GET bare URL, assert review renders.*

### Notes (12)

- `form_handler.get_value` duplicates `application_handler.get_form_value`, omitting the trim (drift hazard) — `form_handler.gleam:876`
- `questions.question_count` is orphan dead code (form_handler inlines `list.length`) — `questions.gleam:346`
- Resend rollback conflates `Ok(0-row)` with success in a narrow concurrent-takeover race (retry form can strand on a dead old_token; outcome is a truthful-ish 404, not data loss) — `form_handler.gleam:639`
- Resend POST form duplicated verbatim in `view_expired` + `view_resend_failed` (differ only in testids + label) — `form_pages.gleam:296/336`
- `is_expired` (`<=`) and `remint_form_token` guard (`<`) disagree at the exact expiry boundary — unreachable via human click latency, code-smell only — `get_form_context_by_form_token.sql:19` / `remint_form_token.sql:18`
- `ChoiceWithOther` 'other' text field rendered but never pinned; no end-to-end POST of an 'other' answer — `form_question_pages.gleam`
- `?q=<answered-id>` pre-fill GET dispatch only unit-tested (`clamp_current`), not integration-pinned — `form_handler.gleam:173`
- Resend guarded-write 0-row stand-down (AD-14) branch untested — `form_handler.gleam:576`
- Handler error branches untested: POST unknown-token, `bad_request` question, PUT malformed-JSON — `form_handler.gleam:284/354/431`
- Spec File List omits `csrf.gleam` (the B1 fix file), `csrf_test.gleam`, and `reference_form_wiring.test.js` (all in the diff) — `spec-rc3-3…md`
- `clamp_current` `last_question_id` fallback masked by its own dedicated test (uses a valid answered id, never hits the fallback) — `form_handler_test.gleam:364`
- `resend_audit_details` no-PII assertions vacuous (fixture detail carries no `@`/`+353`, so absence assertions always pass) — `form_handler_test.gleam:229`

### Reviewer agreement

No finding was flagged by 2+ independent lens types. The two warnings both came from the `tests` lens (the resend-abuse warning fired on both the c1 and c2 chunks — same lens type, so not a reviewer-agreement signal, but notable that two independent passes of the same lens landed on it).

### Verdict

**READY TO MERGE**

r1's blocker and all 11 warnings are genuinely fixed (verified by code trace + test execution, not commit-message claims). No fifth registry gap exists — the security lens ran clean on both registry-touching chunks. No em-dashes in copy. 22 fresh-context lenses across the 19-file rework surfaced **0 blockers**: 2 coverage-gap warnings on *already-correct* behavior (the abuse guard and review dispatch both work; they're just unpinned) and 12 notes (DRY/consistency/coverage polish). The defended invariants — csrf registry completeness, silent-drop abuse posture, token-state truthfulness, no-JS first-class path — all hold. The two warnings are worth closing in a follow-up but do not block this fix-audit.

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
