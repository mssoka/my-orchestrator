## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-draft-grace-period · **Reviewed sha:** ca0e3b9 · **Reviewers:** 7/7 completed
**Verification:** 7/9 findings confirmed against the code — 2 discarded as false-positive

### Blockers (0)
None.

### Warnings (2)

1. **Re-close grace pin test never stamps `closed_notified_at`, so it passes even if `extend_vacancy` drops the NULL-clear it claims to guard** [blind] — `server/test/integration/draft_integration_test.gleam:743-780`
   `extend_vacancy.sql:41` does clear the stamp today (verified), and in production auto-closed rows do get stamped (`mark_vacancy_close_notified.sql`), so the stale-stamp scenario the test's doc comment describes is real. But `auto_close_with_closes_at` never sets `closed_notified_at` and the seed leaves it NULL — so every assertion in `extend_clears_close_stamp_so_reclose_gets_fresh_grace_test` (including the `COALESCE(closed_notified_at::text, '') = ''` check) passes with the NULL-clear dropped. The doc comment's "If a future edit drops that NULL-clear, this test fails" overclaims, and the PR body's Review-pass section repeats the claim. *Fix:* stamp `closed_notified_at` explicitly in the first close, old enough to exceed 7 days at the second sweep; seed the draft after the first sweep so a stale stamp would actually delete it.

2. **Active-but-expired vacancy (status not `closed`, `closes_at` past) lost its draft-sweep pin in the test rewrite** [blind + tests] — `server/test/integration/draft_integration_test.gleam:586-635`
   The old suite pinned deletion for a still-active vacancy with `closes_at` past; both new helpers force `status='closed'`. Neither the in-grace survival (active, `closes_at` 3d past) nor the documented ≥7-day lifecycle-outage deletion of an active-but-expired vacancy is pinned — a future edit adding a status condition to the time-based branch would ship green. *Fix:* add two cases: status left `'active'` with `closes_at` 3d past (survives) and 8d past (swept via the time-based branch).

### Notes (4)

- **Stale field doc** [codebase] — `server/src/retention/retention_job.gleam:108-111`: the `RunSummary.application_drafts_expired` doc still says "drafts die at vacancy close", contradicting the amended sweep comment ~200 lines below in the same file. Reword to the 7-day grace semantic.
- **Exact 7-day threshold unpinned** [tests] — all assertions use 1/3/8-day offsets, so any constant in (3d, 8d] passes. The briefing's acceptance criteria specified exactly these brackets and the daily sweep cadence already fuzzes the boundary, so this is optional: bracket with e.g. 6d23h (survives) / 7d1h (deleted) if you want the parameter pinned tightly.
- **Archived + long-expired sweep behavior unpinned** [tests] — the amended SQL comment newly documents that the time-based branch sweeps an archived vacancy with `closes_at` >7d past, but only archived+unexpired survival is pinned. Pre-existing behavior, disclosed in the PR body; a one-case pin would match the new documentation.
- **Advisory test gate: PASS** [tests] — P0/P1 coverage ~100%; residual gaps are the P2/P3 items above. Verified during consolidation.

**Discarded as false-positive (2):** "closes_at NOT NULL contradicts the dropped IS NOT NULL guard" — the column is `TIMESTAMPTZ NOT NULL` (initial schema:54), the old guard was dead. "Continue-link email still frames the expiry promise as vacancy close" — the email promises link *functionality* ("This link works until the vacancy closes"), which stays literally true (the link renders the closed page once closed); it never disclosed a deletion period, and the deletion-timing copy (erasure confirm) was correctly updated.

### Reviewer agreement
- Active-but-expired draft-sweep pin lost in the rewrite (blind + tests) — see Warning 2.

**Verdict:** READY TO MERGE

The core predicate change is correct and well-tested: close-moment derivation (`closes_at` for time-based, `closed_notified_at` for manual with a sound `COALESCE` fallback) verified against `close_vacancy.sql`, `extend_vacancy.sql`, and the schema; the 3d-survives/8d-deleted and close-extend-resume-submit acceptance criteria are pinned by integration tests; the disclosed judgment calls (archive-shield semantics, earliest-anchor edge) are documented honestly in the SQL comments. The two warnings are test-hardening gaps, not defects.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
