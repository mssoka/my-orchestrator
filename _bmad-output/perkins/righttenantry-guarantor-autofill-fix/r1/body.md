## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-guarantor-autofill-fix · **Reviewed sha:** `c350efa` · **Reviewers:** 7/7 completed
**Verification:** 3/4 findings confirmed against the code — 1 discarded as false-positive

### Blockers (1)

1. **Headline acceptance criterion is not met in Chrome: guarantor name/email still don't autofill — the shipped spec's AC and the original briefing's acceptance are contradicted by the PR's own verification table** *(acceptance)*
   - Location: `_bmad-output/implementation-artifacts/spec-guarantor-autofill-fix.md:63` vs PR-body verification table
   - The spec AC states: *"when the guarantor section is opened … and an autofill suggestion is clicked in a real Chromium, then `guarantor_name` / `guarantor_phone` / `guarantor_email` populate."* The PR's own real-browser table says: *"Guarantor name / email | not filled | still suppressed by Chrome's 9-per-type cap (10th NAME_FULL / 11th EMAIL instance …)".* The user-reported bug named exactly that name/phone/email trio; 2 of the 3 remain broken in the browser the reporter uses. The spec's Design Notes acknowledge the cap, so the spec contradicts itself — the fix as shipped does not satisfy the acceptance criteria as written.
   - The code change itself is correct and complete at the attribute layer (verified: cap counting in Chromium `form_filler.cc` is per-`FieldType` with no trigger-field exemption, so `tel`/`tel-national` genuinely are separate buckets, and no alternative token exists for full-name/email). The gap is the acceptance contract, not the mapping.
   - Fix: renegotiate the contract explicitly — carve the Chrome-capped name/email fields out of spec AC #1 and the manual-check section (with the cap rationale), state the residual in the title/description, and obtain explicit human sign-off on the partial fix — or scope the co-applicant-card de-duplication (the real lever) as a follow-up.

### Warnings (0)

### Notes (2)

1. **Spec task list's partition doesn't match the code** *(blind)* — the spec promises `employer_ref_name` as an exact-table entry and an `_amount` suffix rule; the code resolves both via other branches (`_name` suffix / `amount` exact) with identical outputs. Update the spec to match the implementation (or add the defensive rules).
2. **`tel-national` is pinned only at the pure-function level** *(tests)* — no co-applicant section-render assertion exists (`grep -rn 'tel-national' server/test/` matches only `form_fields_test.gleam`; there is no `situation_section_test.gleam`). P3 defense-in-depth: mapping logic and the generic render path are pinned, so this is optional. Advisory test gate: **PASS** (P0 100%, P1 ~90-95%).

### Reviewer agreement

No finding was reported by two or more lenses. The blocker was independently confirmed by my own verification pass (spec AC text, PR-body table, Chromium `form_filler.cc` `kTypeValueFormFillingLimit` semantics).

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
