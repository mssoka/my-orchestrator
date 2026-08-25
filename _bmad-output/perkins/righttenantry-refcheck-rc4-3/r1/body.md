## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc4-3 · **Reviewed sha:** ace27b1 · **Reviewers:** 7/7 completed
**Verification:** 33 findings confirmed against the code — 5 lens claims rejected as false-positive after re-reading the worktree (sweep already uses effective email/phone; substitute INSERT relies on an existing schema default `queued`; the ON CONFLICT predicate matches `idx_reference_call_live`; the detail-payload sentinel is live, not vacuous; `correction_cycles` is NOT NULL so no NULL arithmetic).

Chunking: 6718 diff lines → 4 chunks (server/src, server/test, client, shared+supabase+spec) → one full lens wave per chunk.

### Blockers (3)

1. **Correction re-queues the row into a cadence dead-end — the corrected referee never receives the fresh invite** [edge]
   `server/src/reference_checks/sql/correct_reference_call.sql` resets status/`next_attempt_at`/`correction_cycles` but **not `attempt_count`**. The sweep (`sweep.gleam:255-268`) dispatches on `attempt_count` (0→T0, 1→co-nudge, 2→reminder1…); a corrected row that failed at T0 has `attempt_count=1`, so the sweep runs `step_co_nudge` — sending the **applicant** a co-nudge every 15-minute tick forever — while `sweep_advance` requires `status='contact_initiated'` and the corrected row is `queued`, so every advance 0-rows → StoodDown. The row never advances, never terminalizes, and the corrected referee is never re-invited (AC3's "re-queues… the sweep owns the fresh invite" is broken; exhaustion can never fire because no fresh invite is ever sent). `correct_requeues_with_corrected_contact_and_audits_test` asserts row fields only — it never runs the sweep afterward, so the dead-end is unpinned.
   *Fix: reset `attempt_count = 0` (and mint a fresh `form_token`) in `correct_reference_call.sql`; add a sweep-after-correct integration test pinning the T0 invite to the corrected contact.*

2. **RC4.3 confirm/save buttons are always disabled — the action surface is unusable in the browser** [blind]
   `client/src/components/reference_panel.gleam:769-771, 829-831, 994-996` use `attribute("disabled", case busy { True -> "disabled"; False -> "" })`. In Lustre an **empty string is a present boolean attribute** (`vattr.to_string_tree`: `Attribute(name:, value: "", ..) -> " " <> name`; the reconciler does `setAttribute(node, "disabled", "")`) — so the "enabled" state still renders `disabled=""`, which disables the control. The codebase's established pattern (`sweep_nudge_banner`, `unlock_consent_modal`, `attribute.disabled/1`) omits the attribute entirely when enabled. Every confirm (Start check, Take over) and the Save & resend / Save & send invite buttons ship permanently disabled; the client tests pass because they assert the busy case only (`inflight_disables_confirm_buttons_test`) and dispatch messages model-level.
   *Fix: use the codebase pattern — `case busy { True -> [attribute("disabled", "true")] False -> [] }` — and add a test asserting the enabled state renders without the attribute.*

3. **AR-RC13 regression: substitute action legality is re-derived client-side from status; the shipped `hooks.can_substitute_referee` is never read** [architecture, codebase]
   The server computes and ships `can_substitute_referee` (`application_detail_handler.gleam:1101`, `Objected || Unreachable`), but `client/src/components/reference_panel.gleam` never reads it — `overflow_actions` (line 467-476) derives `Unreachable -> [RefcheckTakeOver, RefcheckSubstitute]` from status and `row_detail` renders `view_substitute_surface` in the Objected/Unreachable case arms. The only client hook read is `can_record_manual` (line 135). This is exactly the RC4.2 r1 `is_terminal` re-derivation pattern the briefing names as a blocker — the panel re-implements the server's rule instead of rendering the hook.
   *Fix: gate the substitute affordance on `call.hooks.can_substitute_referee` (and mirror any other action legality into server hooks).*

### Warnings (12)

1. **Em-dashes in 5 implementer-authored success toasts + em-dash joins in the attempt-log export** [acceptance, architecture, codebase, edge, security] — `copy.gleam:874-884` (`refcheck_toast_started/re_enabled/taken_over/corrected/substituted`) and `build_attempt_log_text` (`client.gleam:6772-6793`, `" — "` joins) violate the RT em-dash ban; `no_em_dash_test` scans only `toast(code, ctx)`/`page(code, ctx)`, never the refcheck consts (the RC4.2 r2 pin gap, live again).
2. **Exhaustion notification names the REPLACED referee** [architecture, codebase, blind] — `notify_reference_correction_exhausted` interpolates `row.contact_name` — the raw snapshot — from `find_reference_call_by_send_ref.sql`/`get_form_context_by_form_token.sql`, which never coalesce `corrected_name`. After a correction that changed the name, "Couldn't reach {stale name}" is announced at both exhaustion routes.
3. **Stale/redelivered failure events defeat the one-cycle exhaustion gate** [security, architecture] — `find_reference_call_by_send_ref` matches any historical `delivered` send_ref in the append-only `attempts` log; a corrected row is live again (`queued`), so a duplicate/redelivered bounce of the **pre-correction** send hits `correction_cycles >= 1` → `exhaust_row` → `unreachable` + a fabricated `referee_contact_invalid` stamp on a contact that was never re-tried.
4. **Clearing one channel in the correction reverts to the failed snapshot contact** [edge] — `correct_reference_call.sql` does `corrected_email = NULLIF($4,'')`; if the landlord clears the failed email (keeping phone), `corrected_email` becomes NULL and the sweep's `effective_email` falls back to the **original failed** `contact_email` — re-sending to the dead address (AD-7's never-re-contact rule).
5. **Failed correct/substitute leaves the edit-trio save button permanently disabled** [blind, codebase, edge] — the `ApiReturnedRefcheckAction` Error branch clears `refcheck_action_inflight` but not `refcheck_edit.saving`; typing never resets `saving`, so the button stays disabled until Cancel + reopen.
6. **Per-row "Start this check now" is a silent no-op on existing queued rows** [edge] — the RC2.3 start API is an idempotent insert (`insert_reference_call_if_absent` → ON CONFLICT DO NOTHING); a queued row already exists, so the call returns 200 `started:true` with nothing created, nothing sent, no re-arm — while the toast claims "the invite goes out now".
7. **Overflow-menu choices open surfaces invisible when the row is collapsed** [blind, codebase] — confirms/edit render only inside `case is_expanded`; `UserChoseRefcheckAction` never expands the row, so on a collapsed row (the default) choosing Start/Take over/Substitute closes the menu and shows nothing.
8. **Late-response guard claimed in comment but missing** [blind, security] — `fire_refcheck_slot_action`'s comment promises an id-match guard; `ApiReturnedRefcheckAction` has no route check, so a stale response toasts + refetches on whatever page the landlord is on.
9. **RC4.3 panel state does NOT reset on route change** [acceptance, blind, codebase, tests] — `model.gleam:370-377` documents "All reset on route change" for the four new fields; `BrowserChangedUrl`'s ApplicationDetail arm resets `refcheck_expanded`/`explainer_open`/`report_download_loading` only. A pending confirm/edit (typed referee PII) leaks across applicants.
10. **Path `vacancy_id` never bound to the path `application_id`** [blind, security, codebase, edge] — a same-owner cross-vacancy id passes the ownership prechecks, the application-trio UPDATE then silently 0-rows, and correct/substitute still return 200 + audit with the app trio stale (also bypasses the archived-vacancy 422).
11. **Audit registry: `OldReferenceCallId`/`NewReferenceCallId` never added to `all_non_pii`** [architecture, codebase] — `audit_log_schema.gleam` gets the variants + wire strings + test arms, but the const ends at `RefSlot`; the new `schema_variants_cover_registry_test` arms are dead code and the documented "schema tests fail until done" guard silently passes.
12. **Second-failure exhaustion pinned only at the SQL layer** [acceptance, tests ×4] — `second_failure_exhausts_to_unreachable_with_signal_test` drives `rc_sql.exhaust_reference_call` directly; neither the delivery-webhook branch (`webhooks.gleam:285`) nor the wrong-person branch (`form_handler.gleam:1217`) is handler-tested, so the audit + in-app notification side effects of both live routes are unpinned.

### Notes (18)

1. Substituted rows skip the rc3-7 creation-time fraud screening the trigger applies to every created row [architecture].
2. Takeover audit callsite duplicates the canonical Tier-2 fail-open helper instead of reusing it [architecture].
3. Take-over/substitute HTTP wiring never tested; direct-handler legs pass a mismatched landlord uuid, so the 200/409s prove only that the handlers ignore the landlord [acceptance].
4. `terminal_reason`-clearing assertion in the correct test is vacuous — the fixture never set one [acceptance].
5. `refcheck_toast_action_failed` defined but never used (error path routes through `copy.toast(code, CtxRefcheckAction)`) [acceptance, blind, codebase].
6. `RefcheckCorrect` overflow-menu arm unreachable and mislabeled 'Substitute referee' [blind].
7. Hardcoded error string in `client.gleam`'s export path while success toast uses a `copy.gleam` const [blind].
8. Spec item 6 omits `corrected_name` from the additive shared-keys enumeration, contradicting the migration + code in the same diff [blind].
9. Spec Files list names files that don't exist under that name and miscounts new vs edited SQL [codebase].
10. Substitute SQL duplicates the idempotent insert instead of reusing it — the live-slot ON CONFLICT predicate is now maintained in three places [codebase].
11. Concurrent substitute double-submit can 409 instead of the documented 200 idempotent no-op (READ COMMITTED visibility window) [edge].
12. Sweep claim/advance guards lack a `taken_over_at` re-check: a take-over landing between the due-SELECT and the send still delivers one message [edge, tests].
13. Invalid `?slot=` → 400 branch and the client's `?slot=` wire format are untested [tests].
14. Detail payload integration test doesn't assert the RC4.3 wire fields (`taken_over_at`/`corrected_*`/`correction_cycles`/contact trio) [tests].
15. `schema_migration_test` `amended_columns_present_test` not extended with `corrected_name`/`correction_cycles` [tests].
16. `correction_cycles` is the only new detail key decoded without null tolerance (defensive — server never emits null) [blind, edge].
17. Fraud-signal stamp failure is log-only in the wrong-person path but Sentry-captured in the webhook path [blind].
18. Take-over confirm body drops the referee's name from the §7.7 sentence (name renders on its own line; "he"→"they" matches the W5 gender-neutral ruling) — deviation from the "verbatim" claim, not from the user's information [acceptance].

### Reviewer agreement

Multi-lens findings (highest confidence): em-dash toasts/export (5 lenses), exhaustion notification stale name (3), webhook replay (2), AR-RC13 substitute re-derivation (2), stuck-saving (3), collapsed-row invisibility (2), route-change reset (4), vacancy-id mismatch (4), audit registry (2), exhaustion call-site coverage (5).

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
