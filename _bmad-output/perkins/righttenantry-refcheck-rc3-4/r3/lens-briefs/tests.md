# LENS: tests (source tag: `tests`) — Perkins r3 refcheck

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing verification, output contract).

Test-coverage analysis via traceability for the delta. THE CRITICAL QUESTION (the r2 lesson): **are the 4 new Node tests GENUINE browser-path tests, or a `simulate.form_body` mask that bypasses the broken client?** This is the load-bearing verification — verify by reading the test file AND cross-referencing how the seam is actually invoked.

For each of the 4 new tests in `scripts/js-tests/reference_form_wiring.test.js` (the "RC3.4 review-submit _focus_seconds wiring" block):
1. `review submit populates _focus_seconds from the page clock` — does it call `referenceForm._initReviewSubmit(env)` (the real seam) and invoke the bound submit listener (`t.reviewForm._onSubmit(...)`) with a fake clock advanced 8s, then assert `focusField.value === "8"`? REAL browser-path drive, not `simulate.form_body`?
2. `review submit does not prevent the native POST` — does it pass an event with a `preventDefault()` spy and assert `event.prevented === false`? Is that assertion meaningful (the listener must actually NOT call it)?
3. `initReviewSubmit is a no-op off the review page` — does it give an env whose `document.querySelector` returns null and assert the seam doesn't throw / binds nothing? Real negative case?
4. `review _focus_seconds floors to whole seconds` — does it advance 5_999ms and assert `"5"` (real `Math.floor` exercise)?

Flag as findings:
- Any test that would pass even if the seam were inert (tautology / mask).
- Any test whose fake DOM does NOT match the real selector contract (so it tests a fiction).
- Missing coverage: is there a test that the seam does NOT fire on the form page (`reference-form-page`), or that `initBrowser` still bails on the review page? (The "no-op off the review page" test partially covers the inverse — assess.)
- The r1 server-side integration test (`focus_seconds_reported_flows_into_the_result_test`) — is it still present as the persistence pin, with the Node test as the browser-path pin? (Both should coexist; neither replaced.)

Also emit ONE advisory-gate finding: title `"Advisory test gate: PASS|CONCERNS|FAIL"`, category `"coverage-gate"`. For this delta: P0 = the seam binds+populates+no-preventDefault (the 4 tests cover happy + 3 negative cases) → likely PASS; weigh whether P1 ≥90%.

**OUTPUT:** write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/tests.json`. `source` must be `"tests"`. `[]` is valid (but the advisory-gate finding should always be present).
