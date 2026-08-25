## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-611-panel-persist · **Reviewed sha:** 2b482d5 · **Reviewers:** 7/7 completed
**Verification:** 7/7 findings confirmed against the code — 0 discarded as false-positive

The fix itself is correct and verified: all three `text_input` call sites now dispatch `UserEditedRefcheckTrio` keyed by `call.reference_call_id`, matching every `refcheck_edit` consumer (view read, update write, save, cancel, prefill) — no residual slot-keyed path remains, per-row isolation holds by UUID, testids intentionally unchanged, em-dash + AR-RC13 lint gates pass, and the local suite is green at the sha (shared 136, client 572/572, server unit suite passed, client bundle + server compile clean, format idempotent). The pin test bites on the old code (dict assertion fails with the slot-keyed payload). The one blocker is test-completeness on the save half.

### Blockers (1)

**B1 — Stale-save half of #611 unpinned: the pin test proves typed→dict→render but never drives Save.** [blind, edge, architecture, tests — 4-way agreement]
`client/test/client_test.gleam:6739-6802`
The new pin asserts the dict write under `rc-1` and the re-rendered value, then stops. The existing save tests (`refcheck_save_resend_dispatches_test` 6593, `refcheck_substitute_save_dispatches_test` 6646) assert only `refcheck_action_inflight`/`saving` flags, never payload values. `save_refcheck_edit` builds the request from that same dict entry (`correct_reference(vid, aid, call, name, email, phone, …)`, `client.gleam:6816-6829`), so the chain is transitively safe today — but a future re-key of the save path would silently stale-save with no test failing, which is precisely the #611 harm class (burned correction cycle + success toast on the OLD contact). The round's lens-guard explicitly demands the stale-save reproduction be pinned: "typed value … → save persists the NEW value, not the stale one".
Fix: extend the pin — after `simulate.input`, dispatch the trio save (e.g. `simulate.click` on `refcheck-edit-save-landlord_ref`, or `simulate.message` with `UserSavedRefcheckEdit("rc-1")`) and assert `saving == True` with the entry retaining the TYPED values.

### Warnings (2)

**W1 — Substitute trio + refetch/reorder survival unexercised (acceptance #2, guard's reorder/refetch clause).** [edge, acceptance, tests]
`client/test/client_test.gleam:6739-6802`
The pin drives only one `AwaitingCorrection` row in `RefcheckEditCorrect` mode, with no refetch step. The substitute arm shares `view_edit_trio` so it's structurally covered and the PR evidences live substitute verification, but no automated test would fail on a substitute-only or refetch regression. Add a sibling simulate test: `Objected` call with `can_substitute_referee: True` seeded `RefcheckEditSubstitute` (empty prefill), type into the trio, assert the dict write under `reference_call_id`; optionally dispatch the refetch with a reordered call list and assert the typed edit survives.

**W2 — Name/phone branches of `UserEditedRefcheckTrio` untested; `_ -> edit` fallback swallows silently.** [tests]
`client/src/client.gleam:3481-3485`
The diff changed the name and phone dispatch-key lines (`reference_panel.gleam:1110,1124`), but only the email path is typed in any test. A mistyped field literal would hit `_ -> edit` and drop keystrokes — the #611 swallow class — with no test failing. While extending the pin (B1), also `simulate.input` into `refcheck-edit-name-landlord_ref` and `refcheck-edit-phone-landlord_ref` and assert both dict writes.

### Notes (4)

**N1 — Re-render assertion string-matches serialized HTML.** [blind] `client_test.gleam:6797` — substring match on `element.to_string` couples the test to Lustre attribute serialization. Prefer `lustre/dev/query` to read the element's `value` attribute.

**N2 — Formal /bug-hunt scenario re-run (issue AC 3) not evidenced in the PR.** [acceptance] — the issue requires `/bug-hunt reference_checks panel-correct` and `panel-substitute` to pass. The PR evidences a live-browser repro with DB proof, but not the scenario re-run (the `reference_checks` scenario dir is not present at this sha). Re-run both scenarios and cite the result, or state in the PR why the live repro supersedes it.

**N3 — Briefing's "fail loud" runtime requirement not implemented — deviation accepted.** [acceptance] — the diff touches only the view and the test. The PR's instrumentation falsified the runtime-swallow premise (events dispatch; the bug was a dict-key mismatch), and the pin test is the durable app-side guard. Deviation is evidence-backed and documented; no action required.

**N4 — Testids remain slot-keyed (guard-required unchanged); same-slot testid collision is a documented pre-existing deferral.** [blind] — `reference_panel.gleam:1110-1124` testid lines are unchanged per the guard (bug-hunt selectors depend on them). Two rows sharing a `ref_slot` (terminal old row + substitute successor) collide on testids — test-selection exposure only; the dict side is now per-call correct. Predates this fix; revisit only with coordinated bug-hunt scenario updates.

### Reviewer agreement

- **B1** (4 sources: blind, edge, architecture, tests) — save-chain unpinned. Highest-confidence finding; the only thing between this PR and approval.
- W1 (3 sources: edge, acceptance, tests) — substitute/refetch coverage.
- Security and codebase lenses: clean.

### Verdict: NEEDS CHANGES

**Advisory test gate: FAIL → would PASS once B1/W1/W2 land** (P0 100% — the keyed-typing pin bites on the old code; P1 currently ~25%: save-payload chain, substitute arm, name/phone, refetch unpinned).

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
