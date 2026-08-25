# PRIOR FINDINGS — r3 review 4922512522 @ 111e221 (NEEDS CHANGES) — r4 VERIFY-DON'T-REOPEN LIST

Round 4 is a user-approved cap-override round (round 4 of 3). Standing orders:

- **(a) THE r3 TOCTOU BLOCKER must be CONFIRMED CLOSED at `df0ea22`** — this is the round's #1 verification. Two conditions, both mandatory: (1) the wrong-person awaiting UPDATE **as executed by the handler** must carry the `taken_over_at IS NULL` backstop — a dedicated guarded SQL mirroring `mark_awaiting_correction` wired into the wrong-person POST path (NOT just a file that exists, NOT just a Gleam read-time check); (2) a **take-over-racing-wrong-person-POST integration test** must exist and bite — it must drive the actual POST route (or at minimum the exact handler transition) such that neutralizing the backstop turns it red. A missing/weak backstop or a vacuous race pin = a blocker. A test that calls the guarded SQL function directly while the handler uses a DIFFERENT unguarded UPDATE is vacuous.
- **(b) AUDIT the r3 partials** — W6, N4, N5, N8-client, N14, N8/N9-spec, N11-resend-pin — each either fixed or explicitly carried with a reason.
- **(c) DO NOT re-litigate settled findings.** r1 B1/B2/B3, r2 blocker, W1–W12, N1–N18 that Perkins verified FIXED in r2/r3 stay closed. N1 pronouns (gender-neutral "they/them" vs §7.7's "he") is a DELIBERATE deviation FLAGGED FOR THE HUMAN — do NOT file it as a defect.
- **FLAG NEW findings ONLY** (plus the still-present/not-fixed audit items above).

Classification instructions: re-read the cited code in the CURRENT worktree (`/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r4`, detached at `df0ea22`):
- **FIXED** → say nothing.
- **STILL PRESENT or WRONG FIX** → emit a finding with the ORIGINAL severity, title prefixed `STILL PRESENT (r3): `, location = current file:line, evidence = the current code.
- r3 findings whose fix is claimed by the r3-rework commit (`df0ea22`: "wrong-person TOCTOU backstop, co-nudge/failure-path exclusions, sweep terminal guards" + the test additions `per_slot_rearm_and_declined_no_rearm_test`, `resend_effective_contact_*_test`, `fallback_leg_stale_bounce_stands_down_test`, `co_nudge_bounce_stands_down_test`, `sweep_terminal_writers_respect_taken_over_test`, `wrong_person_awaiting_sql_has_taken_over_backstop_test`): verify the fix is REAL and WIRED (a test that pins a dead/unused code path is not a fix). If not wired → `STILL PRESENT (r3): ` finding.

## The r3 findings (consolidated @ 111e221):

### BLOCKER [take-over] (sources: edge, security, acceptance, blind, architecture, codebase)
- **Title:** the wrong-person leg's taken-over stand-down is read-time only — `update_reference_call_status` has no `taken_over_at` guard, so a take-over landing between the token read and the UPDATE still yanks a landlord-handled row into `awaiting_correction` and dead-ends it (TOCTOU)
- **r3 location:** server/src/reference_checks/form_handler.gleam:1235-1254 (apply_wrong_person); server/src/reference_checks/sql/update_reference_call_status.sql:23-24
- **r3 evidence:** `case row.taken_over_at != "" { True -> wisp.redirect(to: "/reference/" <> token) ... False -> sql.update_reference_call_status(config.db, id_uuid, sql.AwaitingCorrection, "", "contact_invalid", sql.ContactInitiated)` — update_reference_call_status.sql `WHERE id = $1 AND status = $5::reference_call_status` (no taken_over_at clause). Contrast mark_awaiting_correction.sql `AND taken_over_at IS NULL` and take_over_reference_call.sql (writes ONLY taken_over_at + next_attempt_at, status stays 'contact_initiated').
- **r4 mandate:** the executed wrong-person UPDATE must carry the backstop (the dedicated guarded SQL `mark_awaiting_correction_wrong_person.sql` EXISTS in the PR — verify the handler actually CALLS it) AND a take-over-racing-wrong-person-POST integration test must drive the real POST path and bite when the backstop is neutralized. Missing backstop in the executed path or a vacuous pin = blocker.

### WARNING [exhaustion] — r3 W2 "fallback leg" (sources: acceptance, edge)
- **Title:** Stale-bounce gate bypassable via the contact-fallback leg: matched_send_at='' hardcoded genuine — a redelivered PRE-correction bounce whose envelope equals a correction-retained channel exhausts the corrected row and fabricates referee_contact_invalid
- **r3 location:** server/src/reference_checks/webhooks.gleam:297-298; server/src/reference_checks/sql/find_reference_call_by_send_ref.sql:33-55
- **Claimed r3-rework fix:** `fallback_leg_stale_bounce_stands_down_test` + "failure-path exclusions". Verify the fallback leg no longer treats unmatched-send-ref envelopes as genuine post-correction.

### WARNING [exhaustion] — r3 W3 "co-nudge" (sources: edge)
- **Title:** A bounce of the APPLICANT's co-nudge email exhausts a corrected row and fabricates referee_contact_invalid — the attempts-log containment matches the co-nudge entry and the typed gate classifies it as genuine
- **r3 location:** server/src/reference_checks/sweep.gleam:351-394 (step_co_nudge); server/src/reference_checks/sql/find_reference_call_by_send_ref.sql:38-50
- **Claimed r3-rework fix:** `co_nudge_bounce_stands_down_test` + kind-tagged co-nudge exclusion in the delivery-failure find. Verify the exclusion is wired (the find must exclude applicant-addressed sends).

### WARNING [take-over] — r3 W4 "sweep terminal guards" (sources: edge, security)
- **Title:** sweep_terminal / sweep_mark_failed lack the taken_over_at write guard — a take-over racing the T+144h terminalization lands on a landlord-handled row and kills the §8.6 late-completion form link
- **r3 location:** server/src/reference_checks/sql/sweep_terminal.sql:30-32; server/src/reference_checks/sql/sweep_mark_failed.sql:21-22
- **Claimed r3-rework fix:** "sweep terminal guards" + `sweep_terminal_writers_respect_taken_over_test`. Verify both SQL writers now carry `AND taken_over_at IS NULL`.

### WARNING [take-over] — r3 W6 "queued take-over dead control" (PARTIAL at r3 — audit item)
- **Title:** queued-row take-over is a dead control — overflow_actions offers RefcheckTakeOver on Queued rows but row_detail's Queued arm never renders view_take_over_confirm; choosing it sets an invisible confirm that can't be confirmed or dismissed
- **r3 location:** client/src/components/reference_panel.gleam:485-507 (overflow_actions) vs 597-613 (row_detail Queued arm)
- **Audit:** does the Queued arm of row_detail now render view_take_over_confirm (pending RefcheckConfirmTakeOver)? If the menu entry exists but no confirm surface renders → STILL PRESENT.

### NOTE [coverage] — r3 N4 "per-slot re-arm unpinned" (PARTIAL at r3 — audit item)
- **Title:** per-slot re-arm (r2 N4 fix) and declined no-re-arm are in code but unpinned — no test asserts only the requested slot re-arms or that the suppressed start path skips the re-arm
- **r3 location:** server/src/reference_checks/sql/rearm_queued_reference_calls.sql:16-18; server/src/reference_checks/trigger.gleam:530-558
- **Claimed r3-rework fix:** `per_slot_rearm_and_declined_no_rearm_test`. Verify the test exists and asserts both halves.

### NOTE [client-state] — r3 N5 "single-slot edit discard" (PARTIAL at r3 — audit item)
- **Title:** single-slot refcheck_edit — a second row's action choice or any action success still discards another row's in-progress typed trio
- **r3 location:** client/src/client.gleam:3385-3398 (overwrite), 3552-3561 (unconditional success clear)
- **Audit:** is the success-clear/edit-open now scoped to the acting call_id, or is the discard explicitly carried with a reason?

### NOTE [coverage] — r3 N8-client "?slot= wire untested" (STILL PRESENT at r3 — audit item)
- **Title:** the client's ?slot= wire format for per-row start has no test — the server 400 branch is pinned, the client URL building is not
- **r3 location:** client/src/api/reference_checks_api.gleam:56-70
- **Audit:** client/test/api/reference_checks_api_test.gleam is NEW in this PR — verify it now pins the slot URL building.

### NOTE [a11y] — r3 N14 "Escape unreachable" (PARTIAL at r3 — audit item)
- **Title:** Escape-to-close is wired to the menu div, which never receives focus after clicking ⋯ — the natural click-then-Escape flow does nothing
- **r3 location:** client/src/components/reference_panel.gleam:732-737
- **Audit:** is the keydown handler now on the ⋯ button (or autofocus moves into the menu)? A handler on a sibling div that never receives focus is unreachable.

### NOTE [spec-drift] — r3 N8/N9-spec (PARTIAL at r3 — audit item)
- **Title:** the PR's spec artifacts drift — spec-rc4-3-row-actions.md line 73 still names substitute_reference_call.sql (deleted), line 232 still claims ONE additive column (the migration ships corrected_name + corrected_at), epic-RC4-context.md documents the pre-W4 effective-contact rule
- **r3 location:** _bmad-output/implementation-artifacts/spec-rc4-3-row-actions.md:73,232; _bmad-output/implementation-artifacts/epic-RC4-context.md:21,29
- **Audit:** are those three drift spots fixed in the PR's own artifact hunks (both files are in the diff)?

### NOTE [coverage] — r3 N11-resend-pin (PARTIAL at r3 — audit item)
- **Title:** the resend-leg effective() corrected-only rule (r2 W4 fix) has no pin — sweep helpers are tested, the form_handler resend send is not
- **r3 location:** server/src/reference_checks/form_handler.gleam:710-716
- **Claimed r3-rework fix:** `effective` made `pub` + `resend_effective_contact_pre/post_correction_test` in server/test/reference_checks/form_handler_test.gleam. Verify the tests exist and assert the corrected-only rule.

### NOTE [coverage] — r3 N12 "client wiring pins" (open at r3)
- **Title:** take-over/correct/substitute client wiring pins are missing — only Start/Skip choices are handler-tested at the client level
- **r3 location:** client/test/client_test.gleam (ApiReturnedRefcheckAction section)
- **Check:** did the r3-rework add client dispatch tests? If still absent, it stays open — but per round-4 rules file ONLY if you judge it NEW-worthy or verify it as still-present (low bar: note).

### NOTE [robustness] — r3 N13 "exhaust_wrong_person swallows DB error" (open at r3)
- **Title:** exhaust_wrong_person swallows a DB error on the guarded exhaustion UPDATE into a silent redirect
- **r3 location:** server/src/reference_checks/form_handler.gleam:1355-1359
- **Claimed r3-rework fix:** the `_` arm split into 0-row → redirect / Error → log + sentry. Verify in the current code.

### NOTE [robustness] — r3 N14sql "send_is_post_correction unguarded cast"
- **Title:** send_is_post_correction casts untrusted jsonb text to timestamptz unguarded — a malformed 'at' raises and drops the whole delivery-failure event
- **r3 location:** server/src/reference_checks/sql/find_reference_call_by_send_ref.sql:38-50
- **Claimed r3-rework fix:** this SQL was rewritten (57 changed lines in df0ea22). Verify the cast is guarded or the subquery restructured.

### NOTE [test-quality] — r3 N15 "fixed absolute timestamp fixture"
- **Title:** stale_pre_correction_failure_stands_down_test uses a fixed absolute timestamp ('2026-08-01T08:00:00Z') — clock-dependent
- **r3 location:** server/test/integration/reference_checks_actions_integration_test.gleam:944-1003
- **Check:** converted to now()-relative?

### NOTE [client-state] — r3 N16 "export toast unguarded"
- **Title:** AppCompletedRefcheckExport toasts unconditionally — a clipboard result settling after navigation lands 'Attempt log copied' on an unrelated page
- **r3 location:** client/src/client.gleam:3519-3530
- **Check:** route guard added?

### NOTE [dead-code] — r3 N17 "substitute returned id discarded"
- **Title:** substitution's returned reference_call_id is decoded but never consumed
- **r3 location:** client/src/api/reference_checks_api.gleam action_result_decoder; client/src/client.gleam:3550-3560
- **Check:** resolved (field dropped or used)?

### NOTE [test-quality] — r3 N18 "no_em_dash_test duplicate disjunct"
- **Title:** no_em_dash_test checks the same character twice ('\u{2014}' and '—' are both U+2014)
- **r3 location:** client/test/copy_test.gleam:354-363
- **Check:** cleaned?

### NOTE [copy] — r3 N19 "correction surface duplicate §8.3 sentence"
- **Title:** correction surface renders the §8.3 sentence twice + heading/body deviate from spec verbatim copy
- **r3 location:** client/src/components/reference_panel.gleam:932-985; client/src/copy.gleam:843-847
- **Check:** deduplicated / aligned?

### NOTE [substitution] — r3 N20 "trio_matches_row inconsistent name basis"
- **Title:** trio_matches_row compares the submitted NAME against the snapshot while email/phone compare against the effective — inconsistent basis between the two no-op detectors
- **r3 location:** server/src/reference_checks/actions_handler.gleam:703-721
- **Check:** aligned to effective name?

### NOTE [defensive] — r3 N21 "one-cycle SQL backstop missing"
- **Title:** mark_awaiting_correction's WHERE matches a corrected row — the AD-7 cycle cap rests solely on Gleam call-site gates
- **r3 location:** server/src/reference_checks/sql/mark_awaiting_correction.sql:17-20
- **Claimed r3-rework fix:** `AND correction_cycles = 0` added (the diff shows it — verify in the worktree).

### NOTE [coverage-gate] — r3 N22 "Advisory test gate: PASS"
- **r3 verdict:** PASS at 111e221. The r3-rework adds ~312 integration test lines + client tests — re-evaluate the gate at df0ea22 with the r4 mandate in mind: the gate canNOT be PASS if the wrong-person race pin is vacuous (that is P0 territory).

### N1 pronouns — DO NOT FILE
The gender-neutral "they/them" (vs §7.7's "he"/§7.4's "her") is a deliberate deviation kept across rounds — FLAGGED FOR THE HUMAN'S CALL, NOT a defect. Say nothing.

## Settled — verified FIXED, do NOT reopen:
r1 B1 (cadence re-arm on correct: attempt_count reset + form_token rotation), B2 (disabled attribute serialization), B3 (client-side hook re-derivation / AR-RC13); r2 blocker (taken-over stand-down on the WEBHOOK failure paths — find/mark_awaiting_correction/exhaust all gained `taken_over_at IS NULL`; the r3-rework keeps them), W1 (same-day typed stale-bounce gate + same_day_stale_bounce_stands_down_test), W2 (correction clears form_opened_at + draft_answers), W3 (route-guarded late-response drop), W4 (resend effective corrected-only rule — the sweep-level half), W5 (identical-trio 400 + empty prefill), W7 (history-row re-submit 409), W8 (coverage-gate CONCERNS → resolved), W12 and the remaining verified-fixed W/N items from r2's fix audit. Only the r3 items above are in play.
