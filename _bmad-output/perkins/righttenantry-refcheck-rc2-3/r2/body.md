## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-refcheck-rc2-3 · **Reviewed sha:** 5d405b6 · **Reviewers:** 7/7 completed
**Verification:** 9/9 findings confirmed — 0 false-positive
**Prior-round fix audit:** r1 B1 (test gate / HTTP handler coverage) **ADDRESSED** — advisory gate now **PASS**

### Fix audit (r1 findings, re-read against 5d405b6)

| r1 finding | Status | Evidence |
|---|---|---|
| **B1** Advisory test gate FAIL | **FIXED** | 9 HTTP-level handler tests (happy 200, cross-tenant 404 ×2, archived 422, unknown-slot 400, mid-flight 409, re-enable round-trip) + 2 e2e viewed-PATCH tests through the real `handle_update_status → maybe_trigger_reference_checks` hook (creates-rows asserts 2 rows + 2 `reference_call_created` audits; declined-suppression asserts 0). Tests lens re-gates **PASS** (P0 100%, P1 ~90%, overall >80%). |
| W1 skip-racing viewed-trigger | **FIXED** | `create_skipped_slot` re-reads the slot on 0-row ON CONFLICT: 200 only if it ended up `skipped`, else branded 409. Matches `transition_to_skipped`. |
| W2 hook never exercised | **FIXED** | e2e viewed-PATCH test drives the real handler + hook in production wiring. |
| W3 handlers zero coverage | **FIXED** | All three handlers called directly; negatives present (asymmetric — see N3 below). |
| W4 `trigger_test.gleam` absent | **FIXED (spec amendment)** | Change Log records the fold-in into the integration suite — the alternative r1 offered. |
| W5 count contract | **FIXED** | `Created(count)` = actual inserts; double-trigger pins `Created(count: 0)`. |
| N1 re-enable vacancy link | **FIXED** | `do_re_enable` gates on `get_application_reference_data` with `vacancy_uuid`. |
| N2/N3 error swallowing | **FIXED** | Both `find_*_for_slot` return `Result(..., pog.QueryError)`; callers surface 500. |
| N4 terminal-status duplication | still present | Note; deferred, acceptable. |
| N5 parse_app_uuids duplicate | still present | Note; explicitly out of scope per r1. |

### Blockers (0)

### Warnings (3)

- **W1 — `create_skipped_slot`'s 0-row re-read maps `find_live_row_for_slot` DB errors into 409** [blind+edge] · `trigger.gleam:516-534` — the `_` catch-all swallows `Error(_)` into 409 "This reference changed state", while `do_skip` maps the same helper's error to a branded 500. Inconsistent with the r2 Result-typing fix's own intent. Fix: explicit `Error(_) → 500` arm before the catch-all.
- **W2 — `verify_vacancy_active` DB error bypasses the archived-vacancy guard** [edge+architecture] · `trigger.gleam:763-782` — `_ -> action()` runs the mutation on `Error` (and on `Ok([])`), skipping the 422 guard; `handle_open` (`application_detail_handler.gleam:332`) was restructured to split exactly this call (Error → 500). Requires a mid-request DB blip; one-line fix mirroring `handle_open`.
- **W3 — the 0-row/409 race-guard branches have no deterministic test** [tests] — W1's fix is the highest-stakes delta change and no test forces the conflict path; a regression restoring the lying 200 `skipped:true` would pass CI. Extract the re-read decision into a pure helper, or pre-insert a queued row to force the conflict.

### Notes (4)

- **N1** `create_one_slot` / `create_one_skipped_slot` near-duplicate scaffolds (~35 differing lines: insert query + audit event) [architecture] — DRY nicety; fine to defer until a third slot-kind appears.
- **N2** `find_live_row_for_slot` / `find_skipped_row_for_slot` duplicate the list+filter scaffold, differing only in the status predicate [architecture].
- **N3** Per-handler negative coverage is asymmetric; the changelog's "(happy + cross-tenant 404 + archived 422 + unknown-slot 400 + mid-flight-skip 409)" is the union, not per-handler: `handle_skip` lacks cross-tenant/archived, `handle_re_enable` lacks archived/unknown-slot. Shared precheck code is covered via the other handlers [tests].
- **N4** Advisory test gate: **PASS** [tests].

### Reviewer agreement
Two findings confirmed by two independent lenses each: the re-read error-swallow (blind + edge) and the `verify_vacancy_active` bypass (edge + architecture). Both are verified against the worktree and share a common root: catch-all `_` arms on `Result`-returning reads where the sibling code splits `Error` explicitly. No lens reported the deliberate decisions (no-migration, fail-open trigger, idempotency, nothing-sent, unit-suite fold-in) as defects.

**Verdict:** READY TO MERGE

_Fix-audit of B1 (HTTP handler + trigger dispatcher test coverage) confirmed addressed — gate PASS, e2e pins the headline AC through the real hook; the deliberate decisions confirmed intact. 3 warnings (error-path catch-alls + race-guard test gap) and 4 notes are non-blocking; the two catch-all warnings share a one-line `Error → 500` fix each if you want them folded in before merge._
