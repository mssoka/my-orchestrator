# Lens: CODEBASE FIT (source: `codebase`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/prompts/_preamble.md` in full and internalize the lens-guards + the fix-audit scope.

Reality check against the actual codebase at `5576ccb`. Verify by reading files in the worktree, NOT by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

## Fix-audit priority — N3, N4, N7, N8 (the r1 codebase notes)

- **N3 (stale comments).** r1: the webhooks module doc + a test comment still named the removed `claim_webhook_event` as the idempotency mechanism. **Verify FIXED:** read `webhooks.gleam` module doc (top of file) + `reference_checks_webhooks_integration_test.gleam` around the `resend_redelivery_is_idempotent_test` — both now attribute idempotency to find/mark live-status scoping (`WHERE status IN ('queued','contact_initiated')`), NOT to the claim. The inline `apply_delivery_failure` comments were already fixed in r1; confirm they stayed fixed.
- **N4 (orphaned claim_webhook_event.sql).** r1: zero callers but `.sql` + generated fn remained. **Verify FIXED:** `sql/claim_webhook_event.sql` is DELETED; the generated `claim_webhook_event` fn + `ClaimWebhookEventRow` type are GONE from `sql.gleam`. Grep the whole worktree for `claim_webhook_event` — should be ZERO matches (no callers, no definition). Also confirm no NEW orphan code: `fraud_inputs.gleam` fns all have callers; nothing in `fraud.gleam` is unreferenced.
- **N7 (effective_contact Some("") mis-documented).** r1: the comment claimed corrected="" falls back to snapshot, but code returned None. **Verify FIXED:** read `fraud_inputs.gleam::effective_contact` — for `Some("")` it now does `opt_nonempty("") → None → snapshot` (falls back to snapshot, matching the SQL `NULLIF(corrected,'')` convention). The behavior matches the doc now.
- **N8 (stamp directive TEXT vs JSONB).** r1: the `stamp_creation_fraud_signals` SQL directive said `TEXT` but the generated fn took `Json`. **Verify FIXED:** `sql/stamp_creation_fraud_signals.sql` directive now says `fraud_signals: JSONB` (consistent with the `arg_2: Json` signature + `pog.text(json.to_string(arg_2))`). Squirrel-regen consistency holds.

Each correctly addressed → FIXED (do NOT re-file).

## Delta pass — codebase fit of the new module + the B1 changes

- **`fraud_inputs.gleam` new module** — verify every fn it defines has at least one caller in `trigger.gleam` or `form_handler.gleam` (no orphan fns). Verify its imports (`pog`, `sql`, `fraud`, `youid/uuid`, `gleam/int`, `gleam/list`, `gleam/option`) are all used.
- **Squirrel regen consistency.** `sql.gleam` is generated. Verify: `claim_webhook_event` + `ClaimWebhookEventRow` fully removed; the new fns (`count_cross_application_contact_reuse`, `get_application_reference_contacts`, `stamp_creation_fraud_signals`, `stamp_referee_contact_invalid`) match their `.sql` files (param count, embedded SQL text, `::text` casts). Spot-check the `get_form_context_by_form_token` decoder column ordering (the amended fields `applicant_email`…`completion_seconds` at decode.field(24..29), then `landlord_display_name`/`origin_domain` at 30/31) matches the SELECT order.
- **`result.gleam` field change** (`focus_seconds: Int` → `fraud_signals: json.Json`) — verify ALL callers updated: `form_handler.gleam::save_submit`, `sweep.gleam::step_terminal`, `result_test.gleam::ctx`. Any missed caller = a finding (it would not compile, but verify anyway).
- **Existing tests likely to break:** any other test constructing `StructureContext` or reading `get_form_context_by_form_token` rows. (r1 flagged `result_test.gleam` updated in diff — confirm no other slipped through.)

Verify each claim by reading the actual files.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/codebase.json`, using `source: "codebase"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
