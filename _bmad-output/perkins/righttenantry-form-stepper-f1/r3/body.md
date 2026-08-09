## 🤖 Perkins automated review — round 3 of 3 (FINAL)

**Job:** righttenantry-form-stepper-f1 · **Reviewed sha:** 8f2faf0 · **Reviewers:** 7/7 completed (2 waves, chunked diff: 4,907 lines)
**Verification:** 26/33 lens findings confirmed against the code — 7 discarded as false-positive, 0 kept as [unverified]

### Fix audit (round 2 → this push)

Re-read every r2 finding against this sha:

- **Fixed (5):** B1 (boundary scenario now posts `{MOVE_IN_DATE_TOO_FAR}` instead of the always-valid `{MOVE_IN_DATE}`), B2 (listing-source-tamper asserts the post-F4 error-summary row — label + message verified against `error_summary.gleam:154` / `application_handler.gleam:436`), W4 (bug-hunt landing/workflows scenarios carry `reference_contact_choice`), N1 (`new root.Event(...)` at form_stepper.js:536), N12 (`listing_source_options` deliberate-keep now documented in the comment).
- **Still present (15):** W1, W2, W3, W5, N2, N3, N4, N5, N6, N7, N8, N9, N10, N13, N14 — carried below.
- **Absorbed (1):** N11 folds into new warning W-NEW2 (same root cause, worse manifestation).

### Blockers (0)

None. Both r2 blockers verified fixed; no new blocker found by any lens.

### Warnings (6)

1. **W-NEW1 — `{MOVE_IN_DATE_TOO_FAR}` is undocumented in SKILL.md's substitution contract** [blind+edge+acceptance+architecture+codebase+tests] — `desired-move-in-date-too-far-future.yaml:23` uses the new template, but SKILL.md step 4 (:172) defines only `{MOVE_IN_DATE}` and :278 still claims both boundary scenarios "pin literal dates on purpose". Left literal, the fill fails or posts a non-date — the parse-failure branch the scenario disclaims — and the 12-month upper bound loses its E2E pin (unit test still covers it). The r2 B1 fix landed the scenario; the harness contract didn't follow. **Fix:** document the template (today + 13 months) in step 4 + template-keys section; correct :278.
2. **W-NEW2 — Stepper preflight-hold dead-ends when the blocking upload slot is hidden/cleared after the block** [edge] (absorbs r2 N11) — `form.js` clears/hides file inputs without a change event and `evaluate()` only re-runs on file-input change; the stale `data-preflight-blocked` then holds Continue on the documents step while scrolling to an error span inside the hidden slot. Applicant-facing dead-end with the stepper shipping default-on. **Fix:** dispatch change/`evaluate()` on hide-or-clear, and/or have the hold ignore hidden messages.
3. **W1 (still present since r2)** — form.js `display:flex` preflight fix has no pin that fails on revert; `client_block` asserts textContent only.
4. **W2 (still present since r2)** — analytics-truth synthetic `input` dispatch unpinned at any level; silent W0 funnel corruption if it breaks.
5. **W3 (still present since r2)** — stepper error re-render + preflight-hold choreography pinned only at predicate level; the sole stepper E2E covers the pristine path only.
6. **W5 (still present since r2)** — `apply-form-soak.yaml` missed the `stepper=off` sweep; clicks a submit button the stepper hides, recorded nowhere.

### Notes (18)

**New (7):** N-NEW1 spec frontmatter `review_loop_iteration: 0` alongside a documented r0→r2 loop [blind] · N-NEW2 deferred-work.md:552 records a phantom staleness — label-invariants already ticks consent before empty-submit [acceptance+codebase] · N-NEW3 visited-only segment coloring unpinned [tests] · N-NEW4 SKILL.md heading says RC1.1, bullets say RC1.2 [blind] · N-NEW5 `two_pass` step 18 re-navigates to `$NAV_URL` without the stepper carve-out [blind] · N-NEW6 same-section anchor click dispatches `rt:form-step-changed` with unchanged index [edge] · N-NEW7 stepper gating mirror guarded only by a KEEP-IN-SYNC comment [architecture].

**Carried, still present since r2 (11):** N2 (stale review-order anchors — re-reported by 3 lenses), N3 (spec's form.js "DO NOT EDIT" vs the approved one-liner), N4 (hunter reports lack resolution banners), N5 (diff.txt r0 snapshot sha misattribution), N6 (F3-SEAM checkbox overclaim), N7 ("no-op guards" overclaim), N8 (duplicated DOM harness), N9 ("all 7 sections"), N10 (BSD-only `date -v+90d`), N13 (`#field-listing_source` dangling anchor), N14 (hardcoded gating strings).

### Reviewer agreement

- **W-NEW1** — six of seven lenses independently (blind, edge, acceptance, architecture, codebase, tests): the undocumented template is the highest-confidence signal in this report.
- **N2 re-report** — acceptance + architecture + codebase.
- **N-NEW2** — acceptance + codebase (quoted lines + git history).

**Verdict:** READY TO MERGE — both r2 blockers verified fixed, zero blockers remain. The warnings are real but non-gating: W-NEW1 is a two-line SKILL.md doc fix worth landing before the next form-bug-hunt run; W-NEW2/W1–W3/W5 are coverage and edge-path items with named fixes.

_This was the final automated round (3 of 3) — the human takes over from here._
