## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-form-nojs-submit-fix · **Reviewed sha:** e938f27 · **Reviewers:** 7/7 completed
**Verification:** 2/4 findings confirmed against the code — 2 discarded as false-positive

### Blockers (0)

None.

### Warnings (0)

None. One blind-lens warning ("probe contradicts its own false-positive claim") was discarded on verification: Lustre SSR sorts attributes by name (`vattr.gleam:100`), so a `data-disabled-*` attribute renders *before* `data-testid`, outside the test's probe window — the pin's comment is accurate.

### Notes (2)

1. **Fixtures `mkdir -p` has no automated regression pin** (P3 dev tooling) — `generate-fixtures.sh:28`. No CI/suite runs the script; any regression fails loudly via `set -e` at the next bug-hunt preflight. Consistent with the repo's named-regression testing philosophy; the suggested CI smoke step is optional.
2. **Advisory test gate: PASS** — P0 100% (new SSR pin exercises the real serialized render path), P1 ~100% (`validate_form_missing_consent_test` at `application_handler_test.gleam:156` + the `unticked-consent` force-submit E2E), overall ≥95%.

A second blind-lens note ("form.js init behavior asserted but not shown in the diff") was also discarded: `form.js:23-48` was verified in the worktree — the consent-gate IIFE runs `refresh()` at init and `__rtRecomputeSubmitDisabled` keys only off the two gate markers, never the pre-existing attribute — and the mechanism is documented in this PR's own Decisions section.

### Reviewer agreement

No multi-source findings. Independent lenses converged on clean: edge, acceptance, security, architecture, and codebase all returned zero findings. The deliberate inversion (SSR enabled / JS disables on init) was verified against `form.js` and the three render call sites (`form_view.gleam`, `form_pages.gleam` ×2); server-side consent/attestation/timing/honeypot enforcement is untouched and remains the authoritative gate. The disclosed accepted-risk corner (pre-defer sub-2s scripted spam) stands as documented judgment — not human-reachable.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
