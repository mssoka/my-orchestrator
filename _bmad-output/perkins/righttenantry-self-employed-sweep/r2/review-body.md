## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-self-employed-sweep · **Reviewed sha:** `55ee07f` · **Reviewers:** 7/7 completed
**Verification:** 6/8 findings confirmed against the code — 2 discarded as false-positive
**Fix audit (round 1):** 2/13 fixed (stale checklist PDF regenerated — pdftotext clean; count-cap message swept) · 11 still present, carried below

### Blockers (0)

The r1 blocker is fixed: the committed `tenant-vetting-checklist.pdf` now carries the scoped reference sentence ("…and an employer — or a client, accountant, or business contact if the applicant is self-employed. Then actually contact them.") and the count-cap message reads "One employer / business reference per adult — that's four at most."

### Warnings (4)

1. **Referee contact-trio labels unswept in the client SPA** (architecture) — `client/src/pages/comparison/common_facts.gleam:76` shows `employer_ref_name` as "Employer reference" and `client/src/pages/application_detail_data.gleam:280` as "Employer", while this PR's audit PDF prints the same trio as "Employer / business reference". The disclosed left-untouched list names the form surfaces (`references.gleam`, `situation.gleam`) but not these landlord-dashboard mirrors — either sweep them or add them to the disclosure.
2. **Landlord checklist HTML view sentence unasserted** (tests, still present since round 1) — `tenant_vetting_checklist_view.gleam:103` changed (mission item 3) but `grep "Ask for references" server/test/` is empty; every other W1a surface got a pin. Add a `string.contains` assertion for the ruled sentence.
3. **`upload_required_message` copy unasserted** (tests, still present since round 1) — `application_handler.gleam:964/969` ruled strings pinned by error key only (`e.0`), never message text.
4. **Advisory test gate: CONCERNS** — P0 100%, P1 100%; overall copy-assertion coverage ≈55% (checklist HTML, both PDF templates, count-cap and upload-required messages lack text pins).

### Notes (8)

5. **Count-cap rejection message unasserted** (tests, new) — `employer_ref_over_cap_is_rejected_test` submits exactly the 4 whitelisted fields (the 5th is whitelist-dropped), so `PrecheckRejected` + the new ruled message never execute under test. Add a 5-files-on-`employer_ref_primary` case.
6. **PDF template copy verified only by smoke** (tests, still present since r1) — `audit_report.typ:1044` + `tenant-vetting-checklist.typ:74` compile/file-exists only; the stale-PDF blocker shipped green in r1 for exactly this reason.
7. **num_occupants duplicate-key test fixture** (r1) — `application_handler_test.gleam:148` appends a dead `#("num_occupants", "2")`; first-match-wins keeps "1".
8. **`evidence_humanize` employer_name-only label** (r1, scope-confirmed deliberate).
9. **"Self-healing" doc-comment tension** (r1) — `evidence_humanize.gleam:158`; historical analyses keep the old label permanently.
10. **Four-item checklist duplicated verbatim** (r1) — `email_client.gleam:264/267` vs `form_view.gleam:149/152`; two consecutive sweep PRs had to edit both.
11. **Stale "Employer reference" doc comments** (r1) — `document_upload.gleam:103/346`.
12. **Co-applicant banner labels unpinned** (r1) — `error_summary_test.gleam:100-102` curated-only.

### Reviewer agreement

No multi-lens agreement this round (edge/acceptance/security/codebase clean). Both blind-lens findings were rejected on verification: the `employer_name` mapping exists at `error_summary.gleam:151` (via merged #573), and the "employed or self-employed" negative guard is a discriminating fragment of the exact pre-ruling sentence — the swap was required because "employer, if you" now matches the scoped copy.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
