## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-rc2-3 · **Reviewed sha:** 109ec5d · **Reviewers:** 7/7 completed
**Verification:** 14/15 findings confirmed against the code — 1 discarded as false-positive

### Blockers (1)

1. **Advisory test gate: FAIL** — the story's headline AC ("when the status PATCH succeeds, `reference_call` rows are created") has no automated pin through the real hook. P0 business rules (slot selection, no-contact skip, declined suppression, pre-v1, ON CONFLICT idempotency, audit-on-create) are well pinned at DB level, but P1 is largely NONE: the three new HTTP handlers (`handle_start`/`handle_skip`/`handle_re_enable`), the router arms, the ownership/archived prechecks, slot validation, and the `maybe_trigger_reference_checks` dispatcher have zero direct test coverage (grep of `server/test/` for callers: none). The production wiring could break and CI stays green. *Fix: HTTP-level integration tests for the three handlers (happy 200 + cross-tenant 404 + archived 422 + unknown-slot 400 + mid-flight-skip 409) and one end-to-end viewed-PATCH-creates-rows test.*

### Warnings (5)

1. **Skip racing a concurrent viewed-trigger returns 200 `skipped: true` while the slot is actually `queued`** (`trigger.gleam` ~508/569-573). `do_skip`'s before-trigger path treats a 0-row insert as success without re-reading the slot; if the viewed trigger commits a queued row between `find_live_row_for_slot` and the insert, the conflict yields 0 rows → 200 — but the row is queued and the sweep will contact the referee. The landlord's exclusion is silently lost. `transition_to_skipped` handles the same race correctly (0 rows → 409). *Fix: on 0-row insert, re-read the slot's live status; anything other than `skipped` → branded 409.*
2. **HTTP handlers have zero direct coverage** (tests + blind + acceptance agree): every test calls `run_create_checks`/`do_skip`/`do_re_enable` directly; the spec I/O-matrix rows (unknown slot → 400, mid-flight → 409, not-owner → 404, archived → 422) are implemented but untested.
3. **`maybe_trigger_reference_checks` Viewed-only dispatch never exercised** — RC2.2's `patch_status_to_viewed_writes_audit_row_test` seeds an app with no referee trios, so the trigger creates nothing and asserts nothing about `reference_call`.
4. **Spec-mandated unit file `server/test/reference_checks/trigger_test.gleam` absent** (spec Tasks list names it; behaviours are covered by the integration suite, so this is a deliverable gap — ship it or amend the spec's task list).
5. **`CreateOutcome.Created` count contradicts its doc** — doc says "rows actually inserted (0 when every slot already had a live row)"; impl returns `list.length(eligible)`. The double-trigger test codifies `Created(count: 2)` with 0 inserts. No functional impact today (callers discard it) but misleading for RC3.5/RC4.x.

### Notes (5)

1. `do_re_enable` skips the app↔vacancy relationship check that `do_skip`/`handle_update_status` perform — with a mismatched URL vacancy_id the archived-vacancy guard checks the wrong vacancy (landlord's own rows only; low impact).
2. `find_live_row_for_slot` swallows list-query DB errors as `None` → `do_skip` takes the wrong branch (wrong 200 or a 500 that masks the read failure).
3. `find_skipped_row_for_slot` swallows list-query DB errors as `None` → `do_re_enable` returns a wrong 404 on transient DB failure.
4. Terminal-status set is hand-copied into 4 layers (migration index, 2 ON CONFLICT predicates, `is_terminal`) — all match today, but only the migration copy is pinned by `schema_migration_test`.
5. `parse_app_uuids` near-duplicates the private `with_three_uuids` helper (third copy of the triple-parse; promote when a fourth caller appears).

### Reviewer agreement

Three-source agreement on the missing `trigger_test.gleam` deliverable and the untested HTTP handler layer (blind + acceptance + tests); the skip-race (edge) and count-contract (blind) findings were independently confirmed against the worktree.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._

_RC2.3 trigger story: auto-create on viewed + manual start/skip APIs; post-commit fail-open + idempotent INSERT ON CONFLICT (deliberate); no migration (skipped enum already in RC2.1). Core logic is solid and well pinned at DB level — the gaps are the unverified production wiring (hook + HTTP layer) and one concurrency race in skip._
