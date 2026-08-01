## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc2-1 · **Reviewed sha:** d340be2 · **Reviewers:** 7/7 completed
**Verification:** 13/13 findings confirmed against the code — 0 discarded as false-positive

This is a clean schema-foundation PR. The acceptance auditor (full spec: issue #548, epics RC2.1, architecture §4.1 as amended by A1/A2/A6/A7/A8, §6.4) and the codebase-fit lens both returned **zero findings** — the migration, enums, indexes, TEXT+CHECK deviations, no-`correction_token` (A1), `draft_answers` (A2), `taken_over_at` (A7), skipped-occupies-slot (A6), four notification types (A8), FK-free objection log, and RLS posture all match the contract as verified. The touches to `server/src/ai/sql.gleam` / `server/src/notification/sql.gleam` are mechanical Squirrel codegen regeneration for the new enum values; `test_db.gleam` adds the two new tables to `truncate_all` — both appropriate.

### Blockers (0)

None.

### Warnings (3)

1. **A6 re-enable path cannot restore `next_attempt_at`** — `server/src/reference_checks/sql/update_reference_call_status.sql:12` `[blind, edge, architecture]`
   Entering `'skipped'` NULLs `next_attempt_at` (deliberate), but the guarded update's `ELSE` branch only *preserves* it — so `skipped → queued` re-enable (contracted in the epics: "re-enable moves `skipped → queued` with `next_attempt_at = now()` (A6)", and named in this query's own docstring) leaves the row `queued` with a NULL clock, outside the sweep's partial index, forever unswept. No shipped primitive re-arms it cleanly (`append_reference_call_attempt` would also record a phantom attempt + bump `attempt_count`).
   *Fix:* add a `next_attempt_at` parameter (`''` = preserve) to the guarded update, or ship a dedicated re-enable query stamping `now()` — and flag it in the RC2.3/RC5 handoff so re-enable doesn't reuse this query as-is.

2. **`get_reference_call_by_form_token` ships with zero test coverage** — `server/src/reference_checks/sql/get_reference_call_by_form_token.sql` `[blind, tests]`
   New DB operation without integration coverage; nothing pins the WHERE semantics or the COALESCE-column row mapping.
   *Fix:* integration test — insert a call, set `form_token` via raw query, assert lookup returns the row and an unknown token returns none.

3. **`list_reference_calls_for_application` ships with zero test coverage** — `server/src/reference_checks/sql/list_reference_calls_for_application.sql` `[blind, tests]`
   The `ORDER BY created_at, id` contract and the application filter are unpinned; later sweep/panel stories will rely on them.
   *Fix:* integration test with two calls on one application plus one foreign, asserting order and exclusion.

### Notes (7)

1. **`status_only_transition_preserves_outcome_test` never tests what its name claims** — `server/test/integration/reference_checks_integration_test.gleam:210` `[blind]` — the only `''`-outcome transition runs while outcome is still NULL; no status-only transition runs *after* a recorded outcome, so the COALESCE-preserve property is unexercised. Fire a status-only transition post-outcome, or rename the test.
2. **`form_token` stored and looked up in plaintext** — migration:105 `[security]` — consistent with the spec's own design (architecture §4.1, dsar/erase convention; ~288-bit entropy, service_role-only, RLS deny-all), so advisory only: hashing at rest (keyed digest, hash-before-lookup) is cheapest now, before RC3.x token issuance lands.
3. **`append_reference_call_attempt` guard tested happy-path only** — integration test:275 `[tests]` — the AD-14 guard's negative path (wrong expected status → zero rows, attempts unchanged) is untested, unlike the sibling update guard which has a negative test.
4. **`reference_*` notification types pinned only as migration text** — schema_migration_test:142 `[tests]` — the file-grep proves the `ALTER TYPE`s exist, not that the enum accepts the values or that the regenerated encoder arms map correctly. One DB-level insert/select would pin it.
5. **Decode-error paths untested for the four TEXT+CHECK decoders** — shared/test/reference_call_test.gleam:203 `[tests]` — only status/outcome decoders have unknown-value rejection tests; ref_slot/owner_label/channel/objection_channel have round-trips but no negative pins.
6. **`updated_at` trigger asserted only as DDL text** — schema_migration_test:114 `[tests]` — no integration test observes `updated_at` advancing on an update, so a dropped/no-op trigger would slip through.
7. **Advisory test gate: PASS** `[tests]` — P0 (migration-from-reset, codegen, codec round-trips) 100%; P1 (AC DB behaviors) 100%; overall ≥80%. Warnings 2–3 above would lift residual P2 gaps.

### Reviewer agreement

Highest-confidence findings first: **Warning 1** was caught independently by three lenses (blind, edge, architecture); **Warnings 2–3** by two each (blind, tests). The empty acceptance and codebase results are themselves an agreement signal: two independent spec/convention audits found no deviation from the RC2.1 contract.

**Verdict:** READY TO MERGE

Zero blockers; the warnings are forward-looking (re-enable primitive gap, test coverage for later stories) rather than defects in this story's acceptance criteria. Worth addressing Warning 1 before the skip/re-enable story builds on these primitives.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
