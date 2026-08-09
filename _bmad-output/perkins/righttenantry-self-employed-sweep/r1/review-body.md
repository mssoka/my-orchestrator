## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-self-employed-sweep · **Reviewed sha:** cb24a52 · **Reviewers:** 7/7 completed
**Verification:** 13/16 findings confirmed against the code — 3 discarded as false-positive, 0 kept as [unverified] · 1 blocker added by the verification pass itself (found while confirming a test-coverage warning)

### Blockers (1)

**1. The served landlord-facing checklist PDF still carries the pre-sweep sentence** [verification + tests]
`server/priv/static/templates/tenant-vetting-checklist.pdf` — linked from the guides page (`tenant_vetting_checklist_view.gleam:23` `pdf_path`) and served as a static asset.

Spec item 3 amends the landlord-facing vetting checklist. The `.typ` source and the HTML page got the scoped sentence, but the **committed PDF was never regenerated** — `pdftotext` of the artifact at the reviewed sha still prints:

> Ask for references from the current and previous landlord, and an employer. Then actually contact them.

Nothing regenerates it: no Makefile/CI step, and the Dockerfile installs typst only for runtime audit-report generation (the PDF was last committed in `2f2c186` alongside the original `.typ`). Landlords downloading/printing the checklist get exactly the incoherent copy this sweep exists to remove — and `rg` can't see it because the surface is binary.
**Fix:** `typst compile` the amended `tenant-vetting-checklist.typ` and commit the regenerated PDF; verify with `pdftotext` that the scoped sentence is present.

### Warnings (3)

1. **`upload_required_message` ruled copy has no text assertion** [tests] — `application_handler.gleam:964,969`. `validate_files_presence` tests pin error *keys* only (`e.0 == "employer_ref_primary"`, test:783); `grep "Upload an employer" server/test/` is empty. A typo in the ruled strings ships green. Extend the employer_ref branch to assert `e.1` (primary + ordinal fallback).
2. **`tenant-vetting-checklist.typ` has zero test contact** [tests] — never compiled (the typst-CLI pattern exists only for `audit_report.typ`) and never content-asserted; `checklist_pdf_is_committed_test` only checks the committed PDF is readable bits. This is exactly how the blocker above shipped green. Add a compile check or source-content assertion.
3. **Advisory test gate: CONCERNS** [tests] — P0 100% (form paths fully pinned); P1 ~85%; overall ~78% (13/20 surfaces FULL, 5 PARTIAL, 2 NONE), just under the 80% PASS line. Raising it: the two pins above + HTML checklist sentence assertion + co-applicant banner-label pins.

### Notes (9)

1. **[edge + acceptance — reviewer agreement]** Count-cap rejection on the same Documents step keeps the old term: `document_upload.gleam:167` *"One employer reference per adult — that's four at most."* (applicant-facing via `application_handler.gleam:1452`). Reachable only via crafted multi-file posts, and not in your disclosed left-untouched list. Copy is user-ruled, so: get a ruling or add it to the disclosed list.
2. **[edge]** New validation test appends a duplicate `num_occupants` — `list.key_find` first-match-wins keeps the fixture's `"1"`, so the 2-adult household never exists (`application_handler_test.gleam:148`). Assertions are unaffected; use `list.key_set("num_occupants", "2")` for fixture honesty.
3. **[blind]** Only `employer_name` gets the explicit label; `employer_letter_signatory` still humanises to "Employer letter signatory" (`evidence_humanize.gleam:166,216`). Consistent with item 2's one-field scope — confirm deliberate.
4. **[blind]** `display_label_for_key` doc comment says stored analyses both "keep the old label on re-render" and are "self-healing" — a row that keeps the old label never heals; the population does. Reword.
5. **[architecture]** The four-item applicant checklist is duplicated verbatim between `email_client.gleam` (HTML) and `form_view.gleam` (SSR) — second consecutive sweep PR editing both. Worth a follow-up hoist into `copy.gleam`; not this PR's scope.
6. **[codebase]** Stale `/// Employer reference` doc comments at `document_upload.gleam:103,346` — sibling module doc in `documents.gleam` was updated; these weren't. Internal-only.
7. **[tests]** HTML checklist page sentence unasserted — `content_test.gleam` renders the view but pins only og/tracking snippets.
8. **[tests]** Audit-PDF labels covered at compile level only (`%PDF-` magic + non-empty bytes) — defensible floor; a source-grep pin is the cheap upgrade.
9. **[tests]** Co-applicant `employer / business reference document` banner labels covered only by the drift test (curated ≠ fallback), not exact-text pins.

### Reviewer agreement
The count-cap message (note 1) was found independently by the edge-case and acceptance lenses. Everything else is single-source but was re-verified line-by-line against the worktree.

**Discarded as false-positive (3):** "test asserts a label change not in the diff" (the `employer_name` label landed via merged #573, present in your base — diff-only artifact); a wording objection to the ruled "if you're working" sentence (verbatim user ruling — out of bounds, and the second clause is the sole-trader route); "'daft auto-reply' is a typo" (it's the daft.ie auto-reply — domain term, not a typo).

**Verdict:** NEEDS CHANGES — one blocker: regenerate and commit the landlord-facing checklist PDF so spec item 3 actually reaches the downloadable artifact.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
