## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-guarantor-checkbox-desync · **Reviewed sha:** e83032b8 · **Reviewers:** 7/7 completed
**Verification:** 5/8 lens findings confirmed against the code — 3 discarded as false-positive, plus 1 additional finding raised during the mandatory verification pass

### Blockers (0)

### Warnings (1)
1. **`co_applicant_empty_first_name_skips_only_guarantor_errors_test` fixture falsified by the new required-cohort policy** [codebase] · `server/test/integration/application_integration_test.gleam` (~1861)
   The primary applicant fixture is `employment_status=student` — a REQUIRED cohort under the 2026-08-04 policy — with no guarantor fields. The error re-render now carries the requirement row + 6 primary guarantor errors, contradicting the test's stated "zero guarantor copy on the re-render" intent. It still passes only because its load-bearing assertion checks `guarantor_missing_fields_error` — a copy string that is dead (unused in src) and can never appear. The sibling fixtures in `gdpr_integration_test.gleam` and `draft_integration_test.gleam` were migrated student→retired; this one was missed. The test now gives false confidence that the co-applicant alignment behavior is pinned.
   *Fix:* migrate the primary to `retired` (skips employer trio AND keeps guarantor optional), same as the sibling fixtures.

### Notes (5)
1. **Cohort flip after filling silently unchecks the box and wipes filled guarantor fields** [verification pass] · `server/priv/static/form.js` (clear-on-hide) + `guarantor.gleam` gate/fields divs
   Optional applicant ticks the box + fills the 6 fields, then picks student (required): the engine hides the checkbox gate and `clearInputsWithin` unchecks the box; switching back to employed closes the fields div and wipes the filled values. The old code preserved the tick and the data across cohort changes (auto-tick / default-check). The checkbox no longer reflects "the applicant's actual last action" in this compound path. Narrow, no submission corruption — the applicant sees the cleared state before submitting.
2. **Requirement row fires for filled-but-malformed guarantor fields** [edge] · `application_handler.gleam:571-578`
   A required cohort that names a guarantor but with a malformed email/income still leads the banner with "A guarantor is required — …" though one was provided. Partial-fill is pinned by test as intended; the malformed branch reads odd.
3. **Required-cohort rule triplicated (handler / view mirror / JS mirror) with no cross-boundary agreement test** [architecture]
   `guarantor_required` (handler), `guarantor_cohort`+`guarantor_cohort_is_required` (view), `computeGuarantorCohort` (JS) each carry "MUST STAY IN SYNC"; each side is self-pinned but no test would fail on a one-sided drift (e.g. adding a cohort to the handler only).
4. **Guarantor-step required notices + retired hint lack unit render pins** [tests]
   The declared-required notices (`guarantor-required-notice-*`) and the retired hint are only asserted by bug-hunt E2E scenarios — no SSR/unit pins (grep confirms zero).
5. **Advisory test gate: PASS** [tests] — cohort matrix, persistence + attestation integration pin, 6 scenarios incl. stepper step-block and both optional round-trips. P0 100%.

### Reviewer agreement
No multi-source findings this round (each confirmed finding has a single lens source). The highest-confidence item is the warning, verified against the worktree fixture + assertions.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
