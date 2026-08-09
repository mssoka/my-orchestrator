## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-form-stepper-f1 · **Reviewed sha:** `a8b2cf9` · **Reviewers:** 7/7 completed (2 waves: diff 3,444 lines > 3,000 → chunk 1 `_bmad-output`/`scripts`/`.gitignore`, chunk 2 `server/`)
**Verification:** 22/31 findings confirmed against the code — 7 discarded as false-positive; 2 advisory test-gate FAILs demoted into W1 (mechanical P1-percentage thresholds the repo's test philosophy disavows — the substantive gap is kept as a warning)

_Heads-up on process: reviewed `a8b2cf9`; head is now `61fd8959` (docs-only commit adding the spec's Suggested Review Order — no code change). A fresh round will follow on the next push anyway._

### Blockers (2)

**B1 — The stepper silently breaks the whole form-bug-hunt E2E suite (all 57 scenarios)** [codebase]
`form_stepper.js:324` hides sections 2–8 on initial paint; `.claude/skills/form-bug-hunt/` fills fields via Playwright in document order with zero stepper awareness (0 matches for `step-continue`/`stepper` across the skill), and Playwright refuses fills into hidden sections. The apply form's only E2E defense — consent capture, anti-fraud honeypot/timing, whitelist enforcement, all defended invariants — goes dark the next time anyone runs bug-hunt against the form, and the breakage isn't disclosed in the PR body or `deferred-work.md`.
*Fix:* teach the harness to drive the stepper (click `data-testid=step-continue-<id>` per section, satisfying gating) or add a supported stepper-off test hook; get one canonical scenario green before merge. This also gives the stepper its missing E2E coverage (see W1).

**B2 — Per-file-only upload preflight block dead-ends the documents step with zero visible message** [edge]
One >5MB phone photo under the 22MB aggregate (common from phone cameras; 80% mobile traffic): `form.js` sets `data-preflight-blocked` but `showBanner` is aggregate-only, and the per-file inline error stays `display:none` (`form.css:339`). The new Continue hold (`form_stepper.js:425-435`) then looks for a `documents-section-error` banner that doesn't exist and silently does nothing — the applicant is stuck at the document wall with no explanation, on exactly the cohort this PR is for. The `deferred-work.md` entry's mitigation claim ("the aggregate banner (visible) carries the message") is wrong for per-file-only blocks.
*Fix:* pull the deferred one-line `form.js` fix into this PR (`showInlineError` sets `style.display="flex"`; `clearInlineError` resets), or have the hold reveal `.field-error[data-preflight-error]` spans when no banner exists; correct the deferred-work sentence.

### Warnings (4)

**W1 — ~250 lines of stepper DOM wiring have zero executable coverage; the claimed bug-hunt E2E pass doesn't exist** [tests, acceptance, blind]
Unpinned: the `form.js` probe/bail, the preflight hold, `markInvalid` server-message preservation (three r1 fixes for named r0 regressions), the analytics-truth synthetic `input` dispatch (the W0 funnel bridge), `rt:form-step-changed` firing, chrome/nav, anchor click routing. The test header claims this wiring "is covered by the bug-hunt/manual E2E pass" but no such scenario exists, and the deferral isn't recorded in `deferred-work.md` (the apply_analytics precedent). Both advisory test gates output FAIL (P0 ~100%, P1 ~35–45%); per AGENTS.md, tests defend named regressions — these named fixes ship unprotected.
*Fix:* export the probe/hold/preservation predicates for node tests (the `resolveAnchorTarget` pattern) and/or record the DOM-glue deferral in `deferred-work.md` with the header claim corrected; the B1 harness fix would cover the click paths end-to-end.

**W2 — The `documents.gleam` upload-slot error visibility fix (`display:flex`) has no SSR pin** [tests]
Named r1 regression fix (invisible server-rendered upload errors); reverting the one-line fix fails no test (`grep display:flex server/test/` = 0).
*Fix:* render `view_form_with_errors` with a `landlord_ref_primary` error and assert the upload slot's field-error span carries `style="display:flex"`.

**W3 — Radio-group error anchors resolve to a non-focusable wrapper div; `focus()` silently no-ops** [blind]
`resolveFieldElement` falls back to the `data-testid` wrapper (`div.radio-options`, no tabindex) for radio groups; the anchor click handler's `target.focus()` no-ops. Step switch + scroll still work — degrades, doesn't break — but "switch step, then focus" never focuses radio fields on the error path.
*Fix:* focus the first visible radio/input inside a non-focusable wrapper (or set `tabindex=-1` first, the legend pattern used elsewhere in the file).

**W4 — E2E scenario content stale after F4** [codebase]
Distinct from B1 (harness mechanics): `listing-source-tamper.yaml`'s inject eval throws on the removed select (its defended surface — the server whitelist — still exists; rewrite as a raw POST); `employed-with-rental-history.yaml` fills the removed `listing_source` plus the address quartet now inside a closed `<details>` (Playwright-refused); `apply-form-label-invariants.yaml` still lists `listing_source` in its visibility sweeps.
*Fix:* drop `listing_source` from happy-path form_data, open the address `<details>` before filling, rewrite the tamper scenario as a raw POST, update the label-invariants sets.

### Notes (6)

- **N1** [blind, codebase] Test header still says anchor routing is E2E-only, but the file ends with `resolveAnchorTarget` unit suites — reword (resolution unit-pinned; only the click wiring is E2E). `scripts/js-tests/form_stepper.test.js:1-9`
- **N2** [edge, acceptance] Header's run command `node --test scripts/js-tests/` fails MODULE_NOT_FOUND on the repo's Node 22 (reproduced); only the Makefile glob works (52/52). Same stale line pre-exists in `apply_analytics.test.js`.
- **N3** [codebase, tests] Committed `review-form-stepper-f1/` artifacts freeze the pre-fix r0 state unlabeled — `diff.txt:1097` shows the r0 anchor bug fixed in shipped code (`form_stepper.js:514`). Add a sha/round header or resolution markers.
- **N4** [architecture] Applicant-form strings now split across `copy.gleam` and `form_copy.gleam`, each claiming sole ownership; `situation.gleam` imports both. Document the division or move `address_cluster_summary` into `form_copy.gleam`.
- **N5** [blind] Synthetic `new Event("input", …)` is bare while the same file uses `root.CustomEvent` — harmless in browsers, pattern consistency only.
- **N6** [blind] `.stepper-nav:empty` is unreachable — every nav row gets ≥1 button whenever the stepper activates. Drop or comment as defensive.

### Reviewer agreement

N1 (blind+codebase), N2 (edge+acceptance), N3 (codebase+tests), W1 (tests+acceptance+blind) — all independently confirmed during verification.

**What checked out clean:** all integration hooks exist and match (`data-first-error-field`, `data-apply-page` markers, `__rtRecomputeSubmitDisabled`, `data-preflight-blocked`, `gdpr-consent`, `documents-section-error`, `legend.section-title` ×8); scoring inputs provably untouched (`current_address/city/county/eircode` kept, same names, still optional; `listing_source` is not a scorer input and stays accepted handler-side — expand-then-contract done right); no-JS fallback genuinely intact (SSR renders 8 visible fieldsets, zero stepper chrome, `novalidate` single POST); `apply_analytics.js` byte-untouched with the duplicated gating helpers in sync; F3-SEAM comment intact; `.gitignore` whitelist entry present; CI green on the reviewed sha; security and acceptance lenses found nothing.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
