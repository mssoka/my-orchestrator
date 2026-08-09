## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-guarantor-checkbox-desync · **Reviewed sha:** 279a661 · **Reviewers:** 7/7 completed
**Verification:** 4/4 findings confirmed against the code — 0 discarded as false-positive

### Fix audit — round 1 warning (W1)

**FIXED, verified empirically.** The missed fixture migration is in: `co_applicant_empty_first_name_skips_only_guarantor_errors_test` now uses a **retired** primary, the dead `guarantor_missing_fields_error` constant is removed from `form_copy.gleam` (only a doc-comment reference remains), and the vacuous assertion is replaced with **two live negative pins** ("A guarantor is required", "Your guarantor's full name." — both confirmed live copy from `guarantor_required_error_*` and `application_handler.gleam:661`). I mutation-checked it myself on the round worktree: flipping the fixture back to student makes exactly that test fail (379 passed / 1 failure); at the reviewed sha the full integration suite passes **380/380**.

### Blockers (0)

### Warnings (0)

### Notes (7)
1. **Misnamed test** — `optional_path_posted_uncheck_roundtrips_test` (guarantor_section_test.gleam:106) fixtures a **student** — a REQUIRED cohort — contradicting its name/comment. The pin itself is live (student + guarantor data → re-render stays unchecked; the old default-check would have re-marked it), and the true optional-uncheck case is pinned by `retired_values_render_optional_with_hint_cohort_test` (line 71). Rename/refix the comment only. [blind]
2. **Assertion asymmetry** — `unemployed_values_render_required_test` (line 65) omits the `_guarantor_fields_open` + no-pretick pins its student sibling has; a regression in the unemployed fields-open path would pass undetected. [blind]
3. **Cohort flip wipes filled guarantor fields** — still present since round 1. Switching student→employed closes the fields div and `clearInputsWithin` wipes the six filled guarantor values (form.js). The uncheck itself is user-ruled; the data wipe is a state-loss side effect. Skip clearing when the cohort (not the box) drives the close, or document. [r1 carry]
4. **Requirement row fires for filled-but-malformed** — still present since round 1. A required cohort with a malformed field (e.g. bad guarantor email) still leads the banner "A guarantor is required — …" though one was provided. Partial-fill is now explicitly pinned as intended (6-error test); the malformed branch reads odd but is the same line. [r1 carry]
5. **Rule triplicated with no cross-boundary agreement test** — still present since round 1. `guarantor_required` (handler) ⇔ `guarantor_cohort` (view) ⇔ `computeGuarantorCohort` (JS) each carry "MUST STAY IN SYNC" and are pinned independently, but no single test asserts agreement across all three for the full status matrix — a one-sided drift would pass all suites. [r1 carry]
6. **Declared-required notices / retired-hint / checkbox-gate render contract is E2E-only** — still present since round 1. The notice `data-testid`s + gate `data-condition` wiring are asserted only by bug-hunt scenarios, which are not in CI (verified: no bug-hunt reference in `.github/workflows/`). The ahead-notes already have SSR pins in `form_view_test.gleam` — same pattern would close this. [r1 carry + tests]
7. **Advisory test gate: PASS** — P0 100%, P1 ~92%, overall ~94%. [tests]

### Reviewer agreement
No multi-source agreement set this round. The tests lens independently re-found r1's note 6 (render contract E2E-only), and both blind findings were confirmed against the worktree verbatim. Fix audit and all carry-forwards re-verified at the reviewed sha — including a full 380/380 integration run and a live mutation check of the W1 fix.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
