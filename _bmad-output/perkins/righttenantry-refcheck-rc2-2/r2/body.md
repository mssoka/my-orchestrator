## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-refcheck-rc2-2 · **Reviewed sha:** a55481e · **Reviewers:** 7/7 completed
**Verification:** 12/13 findings confirmed — 1 rejected as false-positive
**Prior-round fix audit:** r1 B1 (leaderboard viewed arm) **addressed** — `"viewed" -> application.Viewed` now sits in the correct handler (`application_list_handler.gleam:90`) and is pinned by the new `list_endpoint_renders_viewed_status_test` integration test. All 8 r1 warnings/notes also fixed (reducer arm, comparison-CTA test, pill/sort/400-body pins, comment drifts; N6 addressed by the r1-approved status_pill-pin proxy).

### Blockers (1)
1. **CI format gate fails on the reviewed head** — `server/test/integration/application_integration_test.gleam:342-343` (the new `list_endpoint_renders_viewed_status_test`) is unformatted: the `let assert Ok(entry) =` binding is split across two lines where gleam format wants it joined. Repo-wide `gleam format --check` fails on exactly this file, and the CI run for this sha fails the mandatory "Format, Lint, Unit Test & Build" job at the format step — the PR cannot merge as-is. (4 reviewer lenses + lead verification.)
   → Run `gleam format server/test/integration/application_integration_test.gleam`, commit, push.

### Warnings (2)
1. **No client-unit test for the reducer's `"viewed"` arm** (`client/src/client.gleam:3129`) — the `ApiReturnedStatusUpdate` case has a silent `_ -> app.status` fallback and zero client tests dispatch it for any status; a regressed arm would not fail compilation. One small test lifts the advisory gate to PASS.
2. **Advisory test gate: CONCERNS** — P0 100%, P1 ≈85%, overall ≈87%. All six r1 coverage gaps are closed; only the reducer test above stands between here and PASS.

### Notes (4)
1. Stale test name `comparison_page_cta_contact_button_only_on_shortlisted_test` now also covers Viewed (comment updated, name not) — `client_test.gleam:3546`.
2. `focus_index_for_status` still omits `"submitted"` — pre-existing and unreachable (only caller passes PATCH-returned statuses; `parse_status` can never return `submitted`); latent drift, not a live defect.
3. Orphaned closing paren carried forward in the `status_from_string` doc comment (`shared/src/shared/application.gleam:203`).
4. Integration tests use raw SQL string interpolation (test-only, seed-generated UUIDs; production uses Squirrel parameterized queries).

### Reviewer agreement
The CI format-gate blocker was reported independently by 4 of 7 lenses (acceptance, architecture, codebase, tests) and confirmed by direct lead verification (CI log + local `gleam format --check`). The stale-test-name note was reported by 2 lenses (blind, acceptance). Edge tracer found zero unhandled paths; the deliberate decisions (sweep-nudge exclusion, Contact-CTA merge, pill recolour, additive migration) are all confirmed intact.

**Verdict:** NEEDS CHANGES

_Fix-audit of B1 (viewed leaderboard arm); the deliberate decisions (sweep-nudge exclusion, Contact-CTA merge, pill recolour) are confirmed intact._
