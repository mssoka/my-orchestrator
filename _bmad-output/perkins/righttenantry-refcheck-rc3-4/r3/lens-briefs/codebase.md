# LENS: codebase (source tag: `codebase`) — Perkins r3 refcheck

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing verification, output contract).

Reality-check the delta against the actual codebase. VERIFY BY READING FILES, not by assuming:
- Do the selectors the seam relies on actually exist in the rendered HTML? Read `server/src/reference_checks/form_pages.gleam` `view_review`: confirm it emits `attribute("data-testid", "reference-review-form")` on the `<form>` AND an input with `attribute.name("_focus_seconds")` + `attribute("data-focus-seconds", "")`. If either is missing/mismatched, the seam binds nothing (inert — the exact r2 defect resurfacing).
- Does the test's fake DOM (`reviewEnv()`) faithfully model the real seam contract? Check: the fake `reviewForm.querySelector("[data-focus-seconds]")` returns the focusField; the real seam does `form.querySelector("[data-focus-seconds]")`. Check: the fake `document.querySelector("[data-testid='reference-review-form']")` returns the form; the real seam matches. A fake DOM that doesn't match the real selector chain would make the test pass while the real code fails — the masking anti-pattern.
- Does the fake `Date`/clock model match how the real seam reads time (`env.Date ? env.Date.now() : Date.now()`)? The fake supplies `Date: { now: () => now }` and the test advances `now` — confirm the seam reads through `env.Date.now()` (it does).
- Does `_initReviewSubmit` exist in the module's `api` export object (so `require(...)` exposes it to the test)? Confirm the export key matches the test's `referenceForm._initReviewSubmit`.
- Are there OTHER review-submit forms or `[data-focus-seconds]` fields in the codebase the seam might accidentally bind (or fail to bind)? grep `data-focus-seconds` and `reference-review-form` across `server/src`.
- Does the seam leave orphan code or break an existing export? (Check the `api` object still exports `_initBrowser` etc.)
- Is the test file's `require("../../server/priv/static/reference_form.js")` path correct from `scripts/js-tests/`?

**OUTPUT:** write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/codebase.json`. `source` must be `"codebase"`. `[]` is valid.
