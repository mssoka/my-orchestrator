## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-form-stepper-f1 · **Reviewed sha:** `7ac11fe` · **Reviewers:** 7/7 completed (2 chunk waves)
**Verification:** 38/40 findings confirmed against the code — 2 discarded as false-positive (0 kept as [unverified])

> **Head moved mid-review:** reviewed `7ac11fe`, head is now `b13c974` (post-#562 rebase + the RC1.2 gating wiring, which was deliberately out of scope this round) — a fresh round will follow on the new sha.

### Round-1 fix audit (re-review — verified against the code, not the PR body)

All 12 round-1 findings re-checked at `7ac11fe`:

- **B1 fixed** — harness is stepper-aware: `stepper=off` suite default + `stepper: true` key + gating drive instructions (SKILL.md:95,131-139,165,254); canonical `stepper-happy-path.yaml` added; `stepperOffInSearch` unit-pinned.
- **B2 fixed** — `showInlineError` sets `display:flex` (form.js:436), `clearInlineError` resets (:447).
- **W1 fixed** — test header rewritten; activation/`stepper=off`/probe/hold/preservation/focus predicates exported and unit-pinned; DOM choreography deferred to the canonical E2E.
- **W2 fixed** — SSR pin at form_view_test.gleam:535-553 (`display:flex` on the upload-slot error span).
- **W3 fixed** — `focusTargetFor` focuses the first inner control / `tabindex=-1` fallback (form_stepper.js:204-225).
- **W4 fixed** — tamper scenario rewritten to `tamper_hidden_inputs`; happy-path dropped `listing_source`; address-cluster documented; label-invariants updated.
- **N1, N2, N3, N4, N6 fixed** — headers corrected, diff.txt r0-snapshot banner, copy division documented, dead CSS rule removed.
- **N5 still present** — bare `new Event(` at form_stepper.js:518 (carried forward as note N1 below).

### Blockers (2)

1. **Boundary scenario `desired-move-in-date-too-far-future` neutralized — `{MOVE_IN_DATE}` can never trigger the `validation_error` it asserts** [all 7 lenses] — `.claude/skills/form-bug-hunt/scenarios/validation/desired-move-in-date-too-far-future.yaml:24`. The staleness sweep replaced the pinned literal (`2030-01-01`) with the today+90d template, contradicting SKILL.md:279's own carve-out ("Only the boundary-validation scenarios … pin literal dates on purpose") and the scenario's yearly-maintenance note. The submission is valid → confirmation; the scenario fails every run and the 12-month upper bound (application_handler.gleam:1114) loses its E2E pin. **Fix:** restore a literal out-of-window date in this one scenario.
2. **`listing-source-tamper` asserts a `field-listing_source-error` span that F4 removed — scenario can never pass** [edge+acceptance+architecture] — `scenarios/validation/listing-source-tamper.yaml:19` + SKILL.md:206's assertion rule ("each `expected_error_fields:` entry has its `field-{name}-error` span populated"). `grep field-listing_source server/src/` = 0 matches. The `tamper_hidden_inputs` rework converted the injection but left the assertion pointing at a deleted span. **Fix:** assert the rejection via the error-summary row text instead, or add a summary-field assertion mode for unrendered fields.

### Warnings (5)

1. **form.js per-file preflight visibility fix (r1 B2) ships with no pin that fails on revert** [tests] — form.js:436. SKILL.md:207's `client_block` asserts the span is *populated* (textContent), which the buggy code also did; no js-tests cover form.js. Same class as r1 W2, which was then pinned SSR-side. **Fix:** assert visibility in `client_block`, or pin `showInlineError`/`clearInlineError` in js-tests.
2. **Analytics-truth synthetic input dispatch (W0 funnel bridge) unpinned at any level** [tests] — form_stepper.js:518. The dispatch lives in unexported choreography; no unit or E2E assertion reaches it. The AC's diff-verifiable part holds (apply_analytics.js untouched, section ids SSR-pinned); the new bridge behavior has zero coverage — silent funnel corruption if it breaks. **Fix:** export a predicate, or assert the captured event list after a gated advance in the canonical scenario.
3. **Stepper error re-render + preflight-hold choreography pinned only at predicate level** [tests] — the sole `stepper: true` scenario is a happy path; start-at-first-error, error-summary click-through routing, and the documents-step hold have no executable wiring coverage (pure functions only). **Fix:** add a `stepper: true` scenario that submits invalid, clicks an error-summary link, and asserts step switch + focus.
4. **bug-hunt `landing/*` scenarios submit without mandatory `reference_contact_choice`** [acceptance] — the sweep touched these files (`?stepper=off`) but left out the RC1.1 injection; every submitting landing scenario bounces on "Choose one option to continue." Recorded in deferred-work.md:553 as rc2-1 scope, but the defended consent/anti-fraud E2E stays dark meanwhile. **Fix:** apply the flow-step-12 injection to landing/workflows now, or land rc2-1 before the next bug-hunt run.
5. **Soak workflow missed by the `stepper=off` sweep** [architecture] — `workflows/apply-form-soak.yaml:300` clicks `submit-application` directly via `${SOAK_APPLY_URL}` with no `stepper=off`; breaks on staging once this deploys. Recorded nowhere. **Fix:** append `stepper=off` when resolving the soak URL.

### Notes (14)

1. **still present since round 1:** bare `new Event(` at form_stepper.js:518 vs `root.CustomEvent` two functions away.
2. Spec's Suggested Review Order cites stale form_stepper.js line numbers — 4 of 6 anchors land on unrelated code (spec:112-127) [4 lenses].
3. Spec boundary says form.js "DO NOT EDIT"; the branch edits it — deviation recorded only in deferred-work.md:549 (the edit followed r1 B2's own recommendation; amend the spec line).
4. `blind-hunter.md` still presents 11 r0 findings in present tense — diff.txt got the resolution banner, the hunter report didn't.
5. diff.txt header misattributes the r0 snapshot to `a8b2cf9` (embedded diff is the pre-squash state — no `.gitignore` fix).
6. Spec task claims form_view_test.gleam pins the `F3-SEAM` substring — it's a Gleam doc comment, unreachable via SSR HTML; no such pin exists.
7. Spec claims "no-op guards" unit-tested — only `shouldActivate` is pinned; the form-absent / <2-sections bails are unexported.
8. `el()` minimal-DOM helper copy-pasted across both js-test files (DRY rule) — extract `dom-stub.js`.
9. `apply-form-structure` still describes "all 7 sections" at an 8-section sha; guarantor section unchecked.
10. SKILL.md's `{MOVE_IN_DATE}` example uses BSD-only `date -v+90d` (note the GNU form for Linux runners).
11. Narrow trap: oversized file hidden by the employment-status toggle keeps submit/Continue held with the error span invisible (no re-evaluate on toggle).
12. `listing_source_options` is dead production code kept alive only by its own parity test.
13. Error summary anchors `listing_source` rows to `#field-listing_source`, which no longer exists (tamper path only).
14. Applicant-facing strings hardcoded in form_stepper.js (`GATING_MESSAGE`, `REVIEW_HINT_STEPPER`) instead of SSR data attributes (the form.js `data-per-file-message` pattern).

### Reviewer agreement

- **B1 (date scenario)** — reported by **all seven lenses**, the strongest signal in this review.
- **B2 (tamper span)** — edge + acceptance + architecture.
- Notes 2, 3, 4, 6 — each confirmed by 2-4 independent lenses.

**Verdict:** NEEDS CHANGES

The r1 rework is genuinely strong — 11 of 12 findings verifiably fixed with real pins. But the reworked E2E suite ships two scenarios that deterministically fail on every run (both one-line content fixes), which is exactly the class of problem round 1 sent back.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
