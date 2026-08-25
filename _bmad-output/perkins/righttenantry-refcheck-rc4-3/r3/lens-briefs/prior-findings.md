# PRIOR FINDINGS — r2 review 4920836185 @ 0fdbf93 (NEEDS CHANGES) — FIX AUDIT LIST

Classify each against the CURRENT worktree (`111e221`): FIXED (silent) or STILL PRESENT / WRONG FIX (finding, original severity, title prefixed `STILL PRESENT (r2): `). The r2 locations were pre-rework; the rework moved/added code (`get_reference_call_by_id.sql`, `mark_awaiting_correction.sql`, `sweep_test.gleam` is NEW, the stale-bounce gate moved into SQL). Find the current home of each concern before classifying.

## The implementing minion's claimed fix map (r2 -> r3) — leads, verify yourself:

- **BLOCKER** -> delivery-failure/wrong-person paths are now `taken_over_at`-aware (failure find/guards stand down taken-over rows).
- **W1 (r2 W1 = r1 W3 format-mix)** -> the stale-bounce comparison moved INTO SQL as typed `timestamptz >= timestamptz` (same-day inversion structurally impossible) + new test `same_day_stale_bounce_stands_down_test` pins the exact case r1/r2 got wrong.
- **W2-W8** -> correction clears the previous referee's session state (`form_opened_at`/`draft_answers`); resend's `effective()` applies the corrected-only rule; identical-trio substitute rejected (400) + empty prefill; queued rows offer take-over; history-row re-submit with different details -> 409; route-guarded late-response drop (toast + refetch).
- **N1-N15** -> spec artifacts fixed; substitute reuses the shared idempotent insert (predicate in ONE place; concurrent double-submits resolve); per-slot re-arm (no re-arm on declined); correction form behind a button; fraud stamp only on REAL inserts; authz negatives pinned; notification pins; sweep effective-contact unit tests + route-reset pin; duplicate name caption gone; Escape closes the menu; N18 pronouns kept gender-neutral per the rc4-2 W5 precedent — FLAGGED FOR THE HUMAN'S CALL (do NOT file as a defect — deliberate deviation).

### 0-BLOCKER [take-over] (sources: edge)
- **Title:** Failure paths ignore taken_over_at: a bounce/wrong-person on a landlord-handled row re-enters the correction loop or exhausts it, killing the §8.6 late-completion transition and dead-ending the row
- **r2 location:** server/src/reference_checks/sql/find_reference_call_by_send_ref.sql (WHERE status IN queued/contact_initiated, no taken_over_at); mark_awaiting_correction.sql:17-20; exhaust_reference_call.sql:29-30; complete_reference_call.sql (WHERE status='contact_initiated')
- **r2 evidence:** find_reference_call_by_send_ref.sql: 'WHERE rc.status IN (\'queued\', \'contact_initiated\')' — no taken_over_at filter; mark_awaiting_correction.sql: 'WHERE id = $1 AND status IN (\'queued\', \'contact_initiated\')' — no taken_over_at; exhaust_reference_call.sql: 'WHERE id = $1 AND status IN (\'que...

### 1-WARNING [exhaustion] (sources: blind, edge, acceptance, security, architecture, codebase, tests)
- **Title:** STILL PRESENT (r1 W3): stale-bounce gate is format-mixed — same-day redelivered pre-correction bounces still exhaust the corrected row and fabricate referee_contact_invalid
- **r2 location:** server/src/reference_checks/webhooks.gleam:297-305 (compare); server/src/reference_checks/sql/find_reference_call_by_send_ref.sql:40-42 (matched_send_at/corrected_at)
- **r2 evidence:** webhooks.gleam: 'let genuine_failure = case row.matched_send_at { "" -> True; at -> case row.corrected_at { "" -> True; corrected -> string.compare(at, corrected) != order.Lt } }' — at is RFC3339 (sweep now_iso()/to_rfc3339: '2026-08-12T08:00:00Z'), corrected is Postgres ::text ('2026-08-12 08:05:00...

### 2-WARNING [correction] (sources: architecture, security, blind)
- **Title:** Correction clears the token but leaves form_opened_at + draft_answers live — the wrong person's draft answers rehydrate into the corrected referee's form and the co-nudge is suppressed forever
- **r2 location:** server/src/reference_checks/sql/correct_reference_call.sql:32-34 (SET list); server/src/reference_checks/form_handler.gleam:162 (GET decodes row.draft_answers); server/src/reference_checks/sweep.gleam:706-715 (co_nudge gate)
- **r2 evidence:** correct_reference_call.sql: 'form_token = NULL, form_token_expires_at = NULL' — no form_opened_at/draft_answers clearing; form_handler.gleam:162: 'let draft = questions.decode_draft(row.draft_answers)' (the corrected referee's fresh token rehydrates the stored draft); sweep.gleam co_nudge_should_fir...

### 3-WARNING [late-response] (sources: security, codebase, tests)
- **Title:** STILL PRESENT (r1 W8): late-response guard is partial — a stale ApiReturnedRefcheckAction still toasts on unrelated pages because application_detail survives navigation and the id-match guard never checks the route
- **r2 location:** client/src/client.gleam:3522-3559 (handler), 6584-6596 (find_refcheck_call), 651 (detail reset only on entering the detail route)
- **r2 evidence:** find_refcheck_call: 'case model.application_detail { Success(detail) -> ... }' — the guard searches the RETAINED detail; BrowserChangedUrl sets 'application_detail: Loading' only in the 'routes.ApplicationDetail(vid, aid) ->' branch; the success arm unconditionally 'add_toast(cleared, toast_copy, To...

### 4-WARNING [correction] (sources: edge)
- **Title:** STILL PRESENT (r1 W4): the resend path's effective() lacks the correction_cycles gate — a cleared channel falls back to the proven-dead snapshot address on the referee's expired-link resend
- **r2 location:** server/src/reference_checks/form_handler.gleam:716-724 (effective helper), 682-714 (send_invite_to_effective_contact)
- **r2 evidence:** fn effective(corrected: Option(String), snapshot: Option(String)) -> Option(String) { case corrected, snapshot { Some(c), _ -> Some(c); None, s -> s } }' — no correction_cycles input; sweep.gleam:709-732 has the corrected-only rule the resend path does not share.

### 5-WARNING [substitution] (sources: codebase)
- **Title:** Substitute edit-trio prefills the terminal referee's own contact and the server accepts an identical trio — one-click re-invite of an objected/unreachable person routes around the Art 21 hard stop and the exhaustion stamp
- **r2 location:** client/src/client.gleam:6680-6695 (prefill_refcheck_edit); client/src/components/reference_panel.gleam:1000-1011 (view_edit_trio prefill); server/src/reference_checks/sql/substitute_reference_call.sql (INSERT has no contact-difference guard)
- **r2 evidence:** prefill_refcheck_edit: '#(reference_panel.effective_name_value(call), reference_panel.effective_email_value(call), reference_panel.effective_phone_value(call))' — the terminal row's OWN contact; substitute_reference_call.sql INSERT 'SELECT application_id, ref_slot, owner_label, $3, NULLIF($4,''), NU...

### 6-WARNING [take-over] (sources: acceptance)
- **Title:** Queued rows never offer 'Take over manually' although A7/AC2 include queued in the take-over set and the server hook can_take_over is True for queued rows
- **r2 location:** client/src/components/reference_panel.gleam:485-507 (overflow_actions), 570-595 (Queued row detail); server/src/application/application_detail_handler.gleam:1108 (can_take_over includes Queued); server/src/reference_checks/sql/take_over_reference_call.sql:29 (guard includes 'queued')
- **r2 evidence:** overflow_actions: 'Queued -> [RefcheckStart, RefcheckSkip]' — no RefcheckTakeOver arm; compute_hooks_decoded: 'can_take_over: status == Queued || status == ContactInitiated || status == Unreachable'; take_over_reference_call.sql: 'AND status IN (\'queued\', \'contact_initiated\', \'unreachable\')'

### 7-WARNING [substitution] (sources: edge)
- **Title:** Substitute 'existing' idempotent no-op silently drops a NEW trio: re-substituting the history row with changed details returns 200 and discards the typed referee
- **r2 location:** server/src/reference_checks/actions_handler.gleam:363-366 (how='existing' -> Ok(new_row.id), no trio write); server/src/reference_checks/sql/substitute_reference_call.sql:44-55 (any live non-terminal successor)
- **r2 evidence:** actions_handler: '"existing" -> Ok(new_row.id)' — the typed trio is never written; substitute_reference_call.sql second SELECT: 'AND rc.status NOT IN (\'form_completed\', \'unreachable\', \'refused\', \'objected\', \'manual_recorded\', \'failed\', \'completed\', \'partial\')' — skipped/awaiting_corr...

### 8-WARNING [coverage-gate] (sources: tests)
- **Title:** Advisory test gate: CONCERNS
- **r2 location:** server/test/integration/reference_checks_actions_integration_test.gleam; client/test/components/reference_panel_test.gleam
- **r2 evidence:** P0 guards pinned (B1 double-pin incl. negative control, substitute idempotence, take-over sweep exclusion, one-cycle guard, W3 both routes at handler level); P1/P2 gaps: no authz negatives (non-owning 404, archived 422), W9 route-reset unpinned, substitute fraud stamp untested, wrong-person notifica...

### 9-NOTE [copy-verbatim] (sources: acceptance, edge)
- **Title:** STILL PRESENT (r1 N18): take-over confirm body uses 'they' not §7.7's 'he'; the §7.4 start confirm likewise uses 'them' not 'her' — verbatim guard not fully met
- **r2 location:** client/src/copy.gleam:811-815 (refcheck_start_confirm), 826-831 (refcheck_take_over_confirm_body)
- **r2 evidence:** refcheck_take_over_confirm_body: 'If they complete the form anyway, it still shows up here.' vs UX §7.7 'If he completes the form anyway, it still shows up here.'; refcheck_start_confirm: 'We\'ll email and text them the form now.' vs §7.4 'We\'ll email and text her the form now.'

### 10-NOTE [spec-drift] (sources: codebase, architecture, tests)
- **Title:** STILL PRESENT (r1 N8/N9): the PR's own spec artifacts drift from the code — item 6 omits corrected_name, item 5 claims ONE additive column while the migration ships two (corrected_name + corrected_at), the Files list names update_application_referee_trio.sql which does not exist, and the effective-contact rule documented is the pre-W4 one
- **r2 location:** _bmad-output/implementation-artifacts/spec-rc4-3-row-actions.md:79-84, 187-189; supabase/migrations/20260812140000_reference_call_corrected_name.sql:1-18
- **r2 evidence:** spec item 6: 'additive detail keys: taken_over_at, contact_name, contact_email, contact_phone, corrected_email, corrected_phone, correction_cycles' — no corrected_name; item 5: 'ONE additive column: corrected_name TEXT' — the migration adds corrected_at too; Files: 'sql/update_application_referee_tr...

### 11-NOTE [maintainability] (sources: architecture, codebase)
- **Title:** STILL PRESENT (r1 N10): the live-slot ON CONFLICT predicate is maintained in three SQL files (plus the migration's partial index) — byte-consistent today, drift-prone tomorrow
- **r2 location:** server/src/reference_checks/sql/substitute_reference_call.sql:37-46; insert_reference_call_if_absent.sql:28-35; insert_reference_call_skipped.sql:24-29; supabase/migrations/20260731222000_create_reference_call.sql:138-140
- **r2 evidence:** Three files carry the identical 'ON CONFLICT (application_id, ref_slot, owner_label) WHERE status NOT IN (\'form_completed\', \'unreachable\', \'refused\', \'objected\', \'manual_recorded\', \'failed\', \'completed\', \'partial\')' predicate, mirroring the migration's partial index.

### 12-NOTE [scope] (sources: blind, architecture, acceptance, tests)
- **Title:** Per-slot 'Start this check now' re-arms EVERY queued row of the application — the slot filter is ignored and the re-arm also fires on the suppressed (declined) start path; the re-arm is effectively inert because queued rows are always already due
- **r2 location:** server/src/reference_checks/trigger.gleam:527-540 (run_start_action); server/src/reference_checks/sql/rearm_queued_reference_calls.sql:9-13
- **r2 evidence:** rearm_queued_reference_calls.sql: 'WHERE application_id = $1 AND status = \'queued\'::reference_call_status AND taken_over_at IS NULL' — no slot filter; run_start_action calls it unconditionally after run_create_checks_slot Ok(_) — including the Ok(Suppressed) declined path.

### 13-NOTE [client-state] (sources: edge, architecture, blind)
- **Title:** Single-slot refcheck_edit: a second action choice (or any action success) silently discards another row's in-progress typed trio values; Cancel resets the trio but never closes it
- **r2 location:** client/src/model.gleam:375-376 (single Option(RefcheckEdit)); client/src/client.gleam:3454-3472, 3543-3544 (UserEditedRefcheckTrio / success clearing); client/src/components/reference_panel.gleam:960-1010 (always-open correction trio)
- **r2 evidence:** UserChoseRefcheckAction Substitute arm: 'refcheck_edit: Some(prefill_refcheck_edit(...))' — overwrites any open edit; success arm: 'Model(..model, refcheck_edit: None, refcheck_confirm: None, ...)' — clears the OTHER row's edit; view_correction_surface renders the trio unconditionally.

### 14-NOTE [concurrency] (sources: edge)
- **Title:** STILL PRESENT (r1 N11): a truly concurrent substitute double-submit can still return 409 instead of the documented 200 idempotent no-op
- **r2 location:** server/src/reference_checks/sql/substitute_reference_call.sql:36-55
- **r2 evidence:** The UNION ALL's second SELECT runs under the statement snapshot taken before the concurrent INSERT committed; under READ COMMITTED the 'NOT EXISTS (SELECT 1 FROM inserted)' + successor SELECT can miss the just-committed row, yielding 0 rows -> Error(NotSubstitutable) -> 409.

### 15-NOTE [substitution] (sources: blind, codebase)
- **Title:** Substitute idempotent no-op re-stamps creation fraud on the existing successor — a full overwrite that can wipe submission-time form_session in a narrow double-submit race
- **r2 location:** server/src/reference_checks/actions_handler.gleam:414-421; server/src/reference_checks/sql/stamp_creation_fraud_signals.sql:15
- **r2 evidence:** actions_handler: 'Ok(new_id) -> { trigger.stamp_creation_fraud_for(config, app_uuid, landlord_uuid, vacancy_uuid, [new_id]) ... }' — runs for how='existing' too; stamp_creation_fraud_signals.sql: 'SET fraud_signals = $2::jsonb' — full overwrite with form_session: null.

### 16-NOTE [coverage] (sources: tests)
- **Title:** STILL PRESENT (r1 N13, partial): the client's ?slot= wire format for per-row start has no test (the server 400 branch is pinned)
- **r2 location:** client/src/api/reference_checks_api.gleam:56-70; server/test/integration/reference_checks_actions_integration_test.gleam:1138 (start_with_invalid_slot_returns_400_test)
- **r2 evidence:** start_check builds '?slot=' <> s — no client test asserts the URL; the server-side invalid-slot 400 is pinned.

### 17-NOTE [coverage] (sources: tests)
- **Title:** Substitution creation-fraud stamping (r1 N1 fold) has no test — the successor row's fraud_signals are never asserted
- **r2 location:** server/src/reference_checks/actions_handler.gleam:414-421; server/test/integration/reference_checks_actions_integration_test.gleam:668-811
- **r2 evidence:** No assertion reads fraud_signals on the substituted successor in the substitute tests.

### 18-NOTE [coverage] (sources: tests)
- **Title:** No authz negatives on the new action endpoints: non-owning-landlord 404 and archived-vacancy 422 are untested for take-over/correct/substitute
- **r2 location:** server/src/reference_checks/actions_handler.gleam:547-573; server/test/integration/reference_checks_actions_integration_test.gleam:1166-1300
- **r2 evidence:** The HTTP happy-path test passes a REAL owning landlord now (r1 N3 fixed); no test drives a foreign landlord's call id or an archived vacancy through the new arms.

### 19-NOTE [coverage] (sources: tests)
- **Title:** Wrong-person exhaustion leg pins status + audit but not the in-app notification
- **r2 location:** server/test/integration/reference_checks_actions_integration_test.gleam:1079-1136
- **r2 evidence:** wrong_person_route_exhausts_corrected_row_test asserts status and audit count only; the webhook leg asserts notification_bodies.

### 20-NOTE [coverage] (sources: tests)
- **Title:** W4 effective-contact rule (cleared channel stays absent after correction) has no sweep-level test, and the W9 route-change reset has no pin
- **r2 location:** server/src/reference_checks/sweep.gleam:709-732; client/src/client.gleam:666-675; client/test/client_test.gleam
- **r2 evidence:** No sweep test drives a corrected row with one cleared channel; no client test navigates away and asserts refcheck_confirm/edit/menu are None.

### 21-NOTE [copy] (sources: blind)
- **Title:** Take-over confirm renders the referee's name twice (the §7.7 body already interpolates it; a caption line repeats it)
- **r2 location:** client/src/components/reference_panel.gleam:853-865
- **r2 evidence:** view_take_over_confirm renders 'html.text(copy.refcheck_take_over_confirm_body(name))' AND 'html.text(name)' as a separate line.

### 22-NOTE [a11y] (sources: acceptance)
- **Title:** Overflow menu declares role=menu/menuitem but has no keyboard contract — no Escape-to-close, no arrow-key navigation
- **r2 location:** client/src/components/reference_panel.gleam:692-760
- **r2 evidence:** The menu div carries role/aria attributes and buttons; no keydown handling for Escape/arrows exists on the menu container.

### 23-NOTE [defensive] (sources: blind)
- **Title:** update_trio's unknown-slot arm fabricates a bogus pog.UnexpectedArgumentCount error (unreachable — ref_slot comes from the DB enum)
- **r2 location:** server/src/reference_checks/actions_handler.gleam:601-620
- **r2 evidence:** '_ -> Error(pog.UnexpectedArgumentCount(expected: 5, got: 0))' — a squirrel-query-shaped error for a slot value that cannot occur.
