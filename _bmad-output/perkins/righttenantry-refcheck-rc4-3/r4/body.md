## 🤖 Perkins automated review — round 4 of 3 (cap overridden by the user)

**Job:** righttenantry-refcheck-rc4-3
**PR:** #606 → `develop`
**Reviewed sha:** df0ea22
**Reviewers:** 7/7 (35 lens runs — 7 lenses × 5 diff chunks)
**Verification:** 22/156 raw findings survived code re-verification — 7 rejected as false-positive

### Round-4 mandate result

**(a) THE r3 TOCTOU BLOCKER — NOT CLOSED.** ❌

- The executed wrong-person awaiting UPDATE still has **no `taken_over_at IS NULL` backstop**: `apply_wrong_person` (form_handler.gleam:1249-1258) still executes `update_reference_call_status`, whose WHERE is only `id = $1 AND status = $5::reference_call_status`. A take-over committing between the token read and the UPDATE still matches (take-over never changes status) — the landlord-handled row is yanked into `awaiting_correction` and dead-ends permanently.
- The dedicated guarded SQL `mark_awaiting_correction_wrong_person.sql` **was authored but never wired**: zero callers outside the generated `sql.gleam` module. It ships as dead code.
- The race pin `wrong_person_awaiting_sql_has_taken_over_backstop_test` **calls the dead SQL function directly** — it never drives the wrong-person POST route. Removing the backstop from the executed path (or unwiring the SQL entirely, as shipped) leaves the test green. **Vacuous.**
- The guarded SQL also lacks the `correction_cycles = 0` backstop its sibling `mark_awaiting_correction` gained (r3 N21) — the mirror is incomplete.

Per the standing orders — "a missing/weak backstop or a vacuous race pin = a blocker" — this is the round's blocker.

**(b) r3 partials audit:** W6 **FIXED** (queued arm renders the take-over confirm) · N4 **FIXED + pinned** · N5 **PARTIAL** (success-clear scoped; edit-open overwrite remains) · N8-client **FIXED** (wire-format test) · N14 **STILL PRESENT** · N8/N9-spec **PARTIAL** (2 of 3 spots remain) · N11-resend-pin **FIXED**. Also verified fixed in the rework: r3 W2 (fallback pre-correction-only), W4 (sweep terminal guards, `sweep_mark_failed` half unpinned), N13, N15, N16, N21. The gender-neutral pronouns stay **flagged for the human**, not a finding.

### Blockers (1)

**B1 — STILL PRESENT (r3): the wrong-person awaiting UPDATE as executed still lacks the `taken_over_at` backstop — the dedicated guarded SQL ships unwired (dead), and the race pin is vacuous** [edge, acceptance, security, architecture, codebase, tests, blind]
`server/src/reference_checks/form_handler.gleam:1249-1258` · `server/src/reference_checks/sql/update_reference_call_status.sql:23-24` · `server/src/reference_checks/sql/mark_awaiting_correction_wrong_person.sql` · `server/test/integration/reference_checks_actions_integration_test.gleam:1729-1765`

`apply_wrong_person`'s False arm still executes `sql.update_reference_call_status(...)`, whose WHERE has no `taken_over_at IS NULL` clause. The guarded query exists in the PR but no handler calls it; the "race" test drives the dead SQL function directly, never the POST route — so the exact r2/r3 dead-end scenario is still reachable and unpinned.

**Fix:** wire `mark_awaiting_correction_wrong_person` into `apply_wrong_person` (delete the unguarded call), add `AND correction_cycles = 0` to the SQL, and replace the direct-SQL test with a POST-route race test that turns red when the backstop is neutralized.

### Warnings (2)

**W1 — STILL PRESENT (r3 W3 partial): legacy untagged co-nudge entries still match the delivery-failure find** [edge, blind] — the `kind`-tag exclusion is forward-only; pre-deploy attempts logs carry no tag, so a bounce of the *applicant's* address on a legacy corrected row still exhausts it and fabricates `referee_contact_invalid`. `server/src/reference_checks/sql/find_reference_call_by_send_ref.sql:82-98`

**W2 — The r3 W3 pin is vacuous** [tests, blind] — `co_nudge_bounce_stands_down_test`'s fixture timestamps are pre-correction, so the typed stale-bounce gate stands the event down even if the kind exclusion were deleted; the producer-side tag write is also unpinned. The guard against fabricated fraud signals must be pinned by a test that bites.

### Notes (19)

**N1** STILL PRESENT (r3 N5): the edit-open choice arms still unconditionally discard another row's typed trio — `client/src/client.gleam:3383-3401`. [blind, edge, acceptance, codebase, tests]
**N2** STILL PRESENT (r3 N14): Escape-to-close keydown sits on the unfocusable menu div — click-⋯-then-Escape still does nothing. `client/src/components/reference_panel.gleam:743-751`. [edge, acceptance, architecture, codebase, tests]
**N3** STILL PRESENT (r3 N8/N9-spec, 2 of 3): spec still names deleted `substitute_reference_call.sql` (line 73) and claims "One additive column" (line 232); the epic-RC4-context rule is fixed. [acceptance, edge, architecture, codebase, tests]
**N4** STILL PRESENT (r3 N17): substitution's returned `reference_call_id` still decoded and discarded. [edge, acceptance, architecture, codebase]
**N5** STILL PRESENT (r3 N19): the §8.3 sentence renders twice when the correction form opens. [blind, acceptance, codebase]
**N6** STILL PRESENT (r3 N18 partial): `no_em_dash_test`'s main loop still checks U+2014 twice; only the second arm was cleaned. [architecture, codebase, acceptance, tests]
**N7** STILL PRESENT (r3 N20, carried-with-reason but leaves a hole): snapshot-basis `trio_matches_row` — a corrected successor re-submitted with its original trio returns 200 and silently drops the typed referee. [architecture]
**N8** NEW: malformed-`at` handling inconsistent — an `at`-less delivered entry exhausts a corrected row via the `matched_send_at == ""` short-circuit, while a prefix-shaped malformed `at` passes the prefix-anchored regex and raises; untested. [edge, blind, security, architecture, tests]
**N9** NEW: a genuine post-correction fallback-leg failure (crash-mid-tick send) can no longer match the find — the blanket fallback-disable loses the `referee_contact_invalid` stamp for a real failure. [edge]
**N10** NEW: `run_action_with_prechecks` treats a DB error on `verify_vacancy_active` as "not archived" — `_ -> action()` runs the action. [blind]
**N11** NEW: `webhooks.exhaust_row`'s `_` arm swallows a DB error on the exhaustion UPDATE — the class r3 N13 fixed in the form-handler leg remains in the webhook leg. [tests]
**N12** NEW: inline literal `"Cancel"` in `view_edit_trio` (copy.gleam rule). [blind]
**N13** NEW: `overflow_actions` has no Objected arm — the PR's own spec menu mapping promises "Objected → Substitute referee" in the overflow. [blind]
**N14** NEW: `refcheck_action_strings()` omits `refcheck_action_correct_details` — one RC4.3 action string escapes the em-dash pin. [architecture, codebase]
**N15** NEW: client pins incomplete — substitute-save + start-confirm dispatch arms unpinned; prefill logic unpinned (tests inject edit state); export handler (incl. the r3 N16 route guard) untested; validation "fires nothing" claims unasserted. [security, tests, codebase, blind]
**N16** NEW: r3 W4 pin drives `sweep_terminal` only — `sweep_mark_failed`'s guard unpinned. [tests]
**N17** NEW: action-success clears `refcheck_confirm` for ANY row (only `refcheck_edit` is call-scoped). [blind]
**N18** NEW: `view_edit_trio`'s no-edit fallback would prefill the terminal referee's own contact for Substitute — dead today, latent W5 hole. [blind]
**N19** NEW (hygiene): unused `eff` bindings, fieldless record update, re-declared hooks record, unreachable `correction_cycles >= 1` CASE arm. [blind]

### Rejected as false positives (7)

Unused import (it IS used) · take-over doc-vs-SQL mismatch (doc matches SQL) · `?slot=` unknown-key degradation (documented back-compat; unknown values 400-pinned) · sweep-exclusion test not making the row due (it uses a 2099 clock) · detail-payload sentinel vacuous (the fixture seeds the sentinel as the actual form_token) · stand-down silence (normal path, deliberate) · schema-migration file checks (the family's design).

### Verdict

**NEEDS CHANGES** — the r3 TOCTOU blocker is not closed: the backstop is authored but unwired, and the race pin is vacuous. One blocker, two warnings (co-nudge exclusion forward-only + vacuous pin), nineteen notes.

Address findings and push — the relay will schedule a fresh Perkins round.
