## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-form-copy-revision · **Reviewed sha:** 52b69d2 · **Reviewers:** 21/21 completed (7 lenses × 3 chunks)
**Verification:** 12/14 findings confirmed against the code — 2 discarded as false-positive (4 duplicates merged → 9 unique)

### Blockers (0)

### Warnings (1)

1. **Error-summary labels and join both use colons, producing double-colon rows** [architecture] — `server/src/application/form_pages.gleam:515`, `error_summary.gleam:177`
   Labels changed `"Guarantor — name"` → `"Guarantor: name"` while `join_label_message` joins with `": "`, so every reference/guarantor/co-applicant error row renders `"Guarantor: name: Your guarantor's full name."` on the public /apply error summary. The old em-dash join never collided. Fix: space-join when the label already contains a colon (extend the `?`/`!` case), or pick a different internal separator.

### Notes (8)

1. **Prep-block item 6 pinned only by non-distinguishing substrings on the form surface** [tests] — `form_view_test.gleam:375-378`. `"one visit"` and `"Complete applications are reviewed first"` both also matched the *removed* one-visit paragraph (the latter also renders in the trust slot), so a revert of item 6 on the form passes CI. The email surface is pinned distinctly (`email_client_test:550-553`) — mirror it on the form test (`save as you go` / no `doesn't save your progress`).
2. **`movement_indicator_none_test` hyphen assertion is vacuous** [blind+edge+codebase+tests — 4-lens agreement] — `client_test.gleam:1782`. After the em-dash → hyphen swap, `contains("-")` is satisfied by the `movement-none` testid and `text-slate text-sm` classes; deleting `html.text("-")` would still pass. Pin the text node (`>-<`).
3. **`no_em_dash_test` comment claims a global copy ban but can only reach toast/page strings** [blind] — `copy_test.gleam:303-307`. `for_each_copy` covers only `copy.toast`/`copy.page`; server-side copy, most emails, legal pages, static JS and inline component literals are unpinned, and there's no repo-wide CI grep lint. Narrow the comment or add the lint.
4. **KEEP-IN-SYNC comment claims checklist item 6 ALSO lives in `form_draft.js`, but it doesn't** [blind] — `form_copy.gleam:115-118`. The item 6 line lives in `form_copy.gleam` + the email mirror; `form_draft.js` holds only the continue-button strings. Comment rewritten in this PR now over-claims.
5. **`join_label_message` space-join branch (`?`/`!` labels) has no test** [tests] — `form_pages.gleam:515-521`. The True branch exists only for the listing_source label; no test renders that error.
6. **`empty_to_dash` now returns a hyphen, not a dash: misleading name** [blind] — `audit_report.gleam:391`. The `"-"` placeholder itself is deliberate (documented in the PR body); only the function name/doc comment are stale.
7. **`no_em_dash_test` checks the same U+2014 character twice (redundant `||`)** [blind] — `copy_test.gleam:309`. The `\u{2014}` escape and literal are identical; harmless dead duplication.
8. **Spec artifact's verification rg commands miss a literal em-dash in priv/static JS and shared/src** [blind] — `spec-form-copy-revision.md:91-92`. The escaped/entity scan doesn't match the literal character and the literal scan is scoped to `.gleam` in two roots. Current tree is clean (remaining hits are comments/logs), so doc accuracy only.

### Reviewer agreement
- 4 lenses (blind, edge, codebase, tests) independently confirmed the vacuous movement_indicator assertion — highest-confidence signal, noted above.
- Acceptance verified independently: `rg "\u2014|&mdash;"` over user-facing copy = 0 hits (remaining em-dashes are code comments, SQL comments, JS comments, test names, or developer-facing logs — all within the PR's disclosed doctrine); en-dash date range "Equal Status Acts 2000–2018" correctly kept; the 6 checklist items + student trigger note verbatim on all surfaces; no-JS item-6 trade-off disclosed in the PR body.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
