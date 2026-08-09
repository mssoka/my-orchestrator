## 🤖 Perkins automated review — round 3 of 3

**Job:** righttenantry-guarantor-checkbox-desync · **Reviewed sha:** `117ac6e` · **Reviewers:** 7/7 completed
**Verification:** 2/2 findings confirmed against the code — 0 discarded as false-positive

### Rebase audit (r2 `279a661` → r3 `117ac6e`)

- PR diff vs its base is **content-preserving**: comparing the r2 diff (vs pre-#574 base) with the r3 diff (vs post-#574 base) shows only blob-index, hunk-offset, and #574 self-employed-sweep context-line differences — zero semantic drift in the PR's own bytes.
- Canonical `gh pr diff` is byte-identical to `git diff 9df9b2e..117ac6e`.
- CI on the reviewed sha: **all green** — Format/Lint/Unit/Build, Integration Tests, Terraform fmt+validate, Migration safety.

### Fix audit (prior findings)

- W1 fix (retired fixture migration + live negative pins + dead string removal): **verified in place** — integration & GDPR fixtures migrated student→retired, `guarantor_missing_fields_error` constant gone, pins assert live copy.
- r2 notes: all 3 still present (see Notes) — plus 3 carry-forward notes from r1 (cohort-flip data wipe, requirement-row-on-malformed phrasing, triplicated rule without a full-matrix agreement test).
- r2 advisory gate PASS: reconfirmed.

### Blockers (0)

None.

### Warnings (0)

None.

### Notes (2)

1. **[tests] Stepper step-level block for guarantor is E2E-only** — `form_stepper.test.js` pins generic `findInvalidControls` gating (visible/required/hidden-wrapper rules) and `guarantor_section_test.gleam` pins the SSR preconditions, but the composition (required cohort → Continue held at the Guarantor step) is asserted only by the manual bug-hunt scenario `stepper/guarantor-required-at-step.yaml`, which is not CI. (P2 gap)
2. **[tests] Advisory test gate: PASS** — P0 100% (persistence null-out + attestation pinned end-to-end; force_required cohort matrix; both silent ticks killed and pinned); P1 ~90%, overall >80%. No gate action required.

### Carry-forward notes (not new)

- `optional_path_posted_uncheck_roundtrips_test` fixtures student (a REQUIRED cohort), contradicting its name/comment — pin is live, misleading label only (r2 N1).
- `unemployed_values_render_required_test` lacks the `_guarantor_fields_open` + no-pretick asserts its student sibling has (r2 N2).
- Required-notices / retired-hint / checkbox-gate render contract unit-unpinned; ahead-notes are pinned (r2 N3).
- Cohort flip wipes filled guarantor fields via `clearInputsWithin` (r1); requirement row leads the banner for malformed-as-well-as-missing guarantor fields (r1); required-cohort rule triplicated across handler/view/JS with no single full-matrix agreement test (r1).

### Reviewer agreement

No multi-source findings this round. Six lenses (blind, edge, acceptance, security, architecture, codebase) returned clean; tests lens produced the 2 notes above. The codebase lens hit a provider rate-limit on first dispatch and was re-run once per policy — succeeded clean.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
