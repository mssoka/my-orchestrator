# LENS: acceptance (source tag: `acceptance`) — Perkins r3 refcheck

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing verification, output contract).

Audit the delta against the spec + the r2 blocker B2-r2's contract. The delta's STATED purpose (commit msg + code comments) is: wire the review-submit `_focus_seconds` so it is no longer inert (the r1 W1 defect / r2 blocker B2-r2), WITHOUT breaking the form-page path or preventing the native review POST.

Verify against the worktree + spec:
- Does `initReviewSubmit` satisfy B2-r2's requirement: the review form's submit POST now carries a real `_focus_seconds` derived from the page clock (not the hardcoded "0")? Read both the JS seam AND `server/src/reference_checks/form_pages.gleam` `view_review` (the rendered hidden field + form) to confirm the selector chain resolves end-to-end.
- Does the seam preserve the **no-preventDefault** contract (review submit is a native POST — AD-3's no-JS degradation doctrine: the form must remain fully usable without JS)?
- Is the form-page path (per-question autosave via `onSubmit`) UNTOUCHED by the seam (the briefing says it must be — no per-question autosave leaking onto the review page, no review logic leaking onto the form page)? Confirm `initBrowser` still bails on the review page and `initReviewSubmit` still bails on the form page.
- Do the 4 Node tests actually assert the acceptance criteria of B2-r2 (populate from page clock, native POST preserved, off-page no-op, whole-second floor)? Or do any assert something weaker/tautological?
- Scope drift: does the delta change anything beyond the seam + its tests? (It must not.)

For each finding, reference the violated AC or contract in `detail`.

**OUTPUT:** write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/acceptance.json`. `source` must be `"acceptance"`. `[]` is valid.
