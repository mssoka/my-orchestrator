## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-self-employed-copy-fix · **Reviewed sha:** e7bab72 · **Reviewers:** 7/7 completed
**Verification:** 8/9 findings confirmed against the code — 1 discarded as false-positive

Diff reviewed: 395 lines, 15 files (canonical `gh pr diff 573` bytes). The copy contract itself is clean: all five checklist surfaces carry the verbatim ruling with per-file escape conventions correct (`&mdash;` in email HTML, literal `—`/`\u{2019}` in SSR), the `employer_name` field name/id is untouched everywhere (scorer contract intact), the stale-copy sweep is clean, and the spec's guardrails (referee-slot surfaces, evidence-excerpt split, landlord .typ checklist) are properly disclosed in deferred-work rather than silently left. Findings below are pin-test gaps and one error-path copy decision — none block the contract.

### Blockers (0)
None.

### Warnings (4)

1. **Inline validation messages still say "employer's name" on the error path** — `server/src/application/application_handler.gleam:491,800` [edge]
   The required-empty messages are `"Your employer\u{2019}s name, please."` (primary) and `"Their employer\u{2019}s name."` (co-applicant). A sole trader who blanks the relabeled field is re-asked for "Your employer's name" — the framing the ruling removed, on the most common error path. The spec's I/O matrix pins only the error-summary label, and this split is not disclosed in deferred-work. Fix: reword to match the ruling (e.g. "Your employer or business name, please."), or add a deferred-work entry recording the split.
2. **Co-applicant form label "Their employer / business name" has no pinning test** — `server/src/application/form_sections/situation.gleam:348` [tests]
   The only test-tree match for "Their employer" is a comment. A revert passes the whole suite. The rendered page in `work_income_employer_label_test` already includes the cards — one `string.contains` assertion pins it.
3. **Client detail-page employer labels unpinned; co-applicant card line (:438) never rendered in tests** — `client/src/pages/application_detail_data.gleam:82,438` [tests]
   Zero "Employer" assertions in `client/test/`; all four fixtures set `co_applicants: []`, so the :438 card line never renders. Reverting both client hunks passes the client suite. Fix: assert the label in an existing success test + one fixture with a populated co-applicant.
4. **Comparison fact-row label exercised but unpinned** — `client/src/pages/comparison/common_facts.gleam:67` [tests]
   `comparison_page_two_columns_test` renders the row with `employer_name: Some("Test Co")` but asserts only grid structure and names. One `string.contains("Employer / business name")` pins it.

_Advisory test gate: **CONCERNS**_ — P0 100% (7/7 pinned surfaces: all five checklist surfaces assert the new clause AND reject the old phrasing against rendered output; primary label + error-summary pinned both directions). Residual gaps are the landlord-facing label surfaces in warnings 2–4; fixing them moves the gate to PASS.

### Notes (2)

1. **Spec marks the Tests task unchecked although the diff ships exactly that work** — `_bmad-output/implementation-artifacts/spec-self-employed-copy-fix.md:72` [blind, acceptance]
   `- [ ] Tests — …` contradicts the commit's own content (strengthened assertions on all four email surfaces + prep block, new auto-reply test, new label tests). Flip to `[x]` so the spec of record reflects the shipped state.
2. **Audit-PDF field-line label is compile-verified but text-unpinned** — `server/priv/templates/audit_report.typ:912` [tests]
   `audit_report_test.gleam` renders with `employer_name: Some("Stripe Dublin")` but asserts only valid-PDF bytes. Acceptable as compile-verified (CI runs real typst); a text-read assertion on the template would pin the label.

### Reviewer agreement
- The spec-checkbox inconsistency was found independently by **blind** and **acceptance** — highest-confidence signal, trivial fix.

**Verdict:** READY TO MERGE — zero blockers; the copy contract, scorer field-name invariance, and disclosure discipline all hold. The warnings are cheap pin-tests plus one error-path copy decision worth a ruling (fix or defer explicitly).

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
