## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-rc2-2 · **Reviewed sha:** dc1e08f · **Reviewers:** 7/7 completed
**Verification:** 15/16 findings confirmed against the code — 1 discarded as false-positive

### Blockers (1)

**B1 — Leaderboard list endpoint coerces `viewed` status to Submitted** — [server/src/vacancy/application_list_handler.gleam:86-95](server/src/vacancy/application_list_handler.gleam#L86-L95) · sources: edge, codebase

The GET `/api/v1/vacancies/:id/applications` handler (router.gleam:415) maps the DB status string to the shared enum with a case that has no `"viewed"` arm. A viewed row hits the `unknown ->` fallback, logs `"Unknown application status: viewed"` on every leaderboard load, and coerces the entry to `application.Submitted` — so a viewed applicant renders as a slate **Submitted** pill at sort rank 0 on the main triage surface, not a navy Viewed pill at rank 3.

```gleam
let status = case row.status {
  "submitted" -> application.Submitted
  "under_review" -> application.UnderReview
  "shortlisted" -> application.Shortlisted
  "approved" -> application.Approved
  "rejected" -> application.Rejected
  "auto_closed" -> application.AutoClosed
  unknown -> {
    wisp.log_warning("Unknown application status: " <> unknown)
    application.Submitted
  }
}
```

Violates AC4 ("leaderboard rows and any status filters render `viewed` without breaking"). Fix: add `"viewed" -> application.Viewed` between the shortlisted and approved arms, matching `parse_status` and the shared codec. This arm is why the PR's own client-side `status_rank` work is invisible end-to-end.

### Warnings (2)

**W1 — `ApiReturnedStatusUpdate` reducer keeps old status for `viewed`** — [client/src/client.gleam:3124-3133](client/src/client.gleam#L3124-L3133) · sources: edge, acceptance, architecture, codebase (4-lens agreement)

The single funnel for every status PATCH maps the response slug with a case that gained arms for every other status this PR but not `"viewed"` — it falls to `_ -> app.status`. After a successful PATCH to viewed, the local model keeps the old status: the stepper flashes the prior step as current while the immediate detail refetch corrects it, and if that refetch fails the UI stays stale until reload. Every other string→variant map in this PR (shared codec, server `parse_status`, stepper `decode_status`) gained the arm.

```gleam
let updated_status = case new_status {
  "under_review" -> application.UnderReview
  "shortlisted" -> application.Shortlisted
  "approved" -> application.Approved
  "rejected" -> application.Rejected
  "auto_closed" -> application.AutoClosed
  _ -> app.status
}
```

Fix: add `"viewed" -> application.Viewed` (or replace the bespoke decoder with `application.status_from_string`, which already handles all seven values).

**W2 — Comparison CTA Viewed→Contact merge has zero coverage; existing negative invariant is stale** — [client/src/pages/comparison/column_headers.gleam:132](client/src/pages/comparison/column_headers.gleam#L132) · source: tests

`comparison_page_cta_contact_button_only_on_shortlisted_test` (client_test.gleam:3518) seeds only Submitted/UnderReview/Rejected and documents "the Contact CTA testid … is exposed only on the Shortlisted column" — now false. Removing `| application.Viewed` from either comparison surface would fail no test. Add a Viewed detail to the comparison test asserting `comparison-cta-contact-<id>` and `dock-contact-<id>` render, and refresh the stale comment.

### Notes (7)

- **N1 — Stale doc comment** `/// Slug for a pipeline index (0..3)` — status_stepper.gleam:134, now 0..4 (sources: architecture, codebase)
- **N2 — Stale count comment** "mirroring the 4-arm `parse_status`" — application_detail_handler_test.gleam:184, now 5-arm (source: codebase)
- **N3 — status_pill recolour unpinned** — UnderReview→navy, Shortlisted→amber, Approved→teal have no render test; a silent revert passes CI (source: tests)
- **N4 — 400 message not body-asserted** — invalid-status integration test asserts only the error code, never that the message lists `viewed` (source: tests)
- **N5 — status_rank Viewed position unexercised** — `sort_by_status_asc_test` seeds no Viewed/Approved and its comment still says "Approved (3) → Rejected (4)" (source: tests)
- **N6 — Viewed render arms unpinned** — stepper `stop_tone` and detail-header `view_status_pill` navy arms have no render assertions (source: tests)
- **N7 — Advisory test gate: CONCERNS** — P0 100%, P1 ≥90%, overall ≈75%; the comparison-CTA test (W2) plus pill-recolour pins lift it past 80% (source: tests)

### Reviewer agreement

Two findings carry multi-lens agreement: **B1** (edge + codebase, independently quoted from the same handler) and **W1** (edge + acceptance + architecture + codebase). The stale-doc-comment pair (N1) is dual-source. One blind-lens finding (a missing sql.gleam decoder arm) was discarded as a false positive — Squirrel decodes statuses as strings via shared `status_from_string`, which already carries `viewed`.

### Verdict
**NEEDS CHANGES** — 1 blocker, 2 warnings, 7 notes.

_Additive 'viewed' status (RC2.2); sweep-nudge/bulk-reject exclusion + Contact-CTA merge + pill recolour are deliberate decisions._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
