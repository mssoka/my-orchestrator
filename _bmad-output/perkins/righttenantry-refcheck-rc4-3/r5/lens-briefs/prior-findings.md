# ROUND-5 FIX AUDIT — r4 findings vs the r4-rework (ccc0ff6), with the r5 mandates

Round 5 is a VERIFY round: the r4 review (NEEDS CHANGES @ df0ea22) had 1 blocker + 2
warnings + 19 notes. The rework (ccc0ff6, commit "fix(refcheck): RC4.3 r4 — wrong-person
TOCTOU wired, legacy co-nudge exclusion, per-row edit dict, sweep guards") claims ALL
closed. Claims are leads, NOT proof. For each item, re-read the cited code in the CURRENT
worktree and classify FIXED (say nothing) / STILL PRESENT / WRONG FIX (emit a finding with
the ORIGINAL severity, title prefixed `STILL PRESENT (r4): `, location = current file:line,
evidence = the current lines).

## 🚨 (a) B1 — THE r4 BLOCKER (the round's #1 question). Closed ONLY if all three hold:

1. **WIRING:** `mark_awaiting_correction_wrong_person` is WIRED into `apply_wrong_person`
   (server/src/reference_checks/form_handler.gleam) and the unguarded
   `update_reference_call_status` call is GONE from the wrong-person path (grep for any
   residual caller on that path).
2. **BOTH BACKSTOPS** in the guarded SQL: `taken_over_at IS NULL` AND `correction_cycles = 0`
   (server/src/reference_checks/sql/mark_awaiting_correction_wrong_person.sql) — and the
   generated sql.gleam matches byte-for-byte.
3. **THE RACE PIN:** `wrong_person_taken_over_race_stands_down_test`
   (server/test/integration/reference_checks_actions_integration_test.gleam ~1734) drives the
   wrong-person POST ROUTE on a taken-over row (303, status untouched, no audit) AND calls
   the guarded SQL directly (0 rows on the taken-over row; a control without takeover
   returns 1 row + awaiting_correction). Neutralizing the taken_over_at guard must turn it
   red. A vacuous or route-bypassing pin = the blocker NOT closed.
   The r2/r3/r4 dead-end scenario (take-over racing the UPDATE yanks a landlord-handled row
   into awaiting_correction) must be STRUCTURALLY IMPOSSIBLE at ccc0ff6.

## 🚨 (b) W1 — legacy co-nudge exclusion (r4 warning). Closed ONLY if:

- The find's EXISTS leg excludes BOTH kind-tagged AND legacy untagged co-nudge entries —
  batch-shape predicate: single-email batch with no sms sibling at the same `at`
  (server/src/reference_checks/sql/find_reference_call_by_send_ref.sql).
- ALL timestamp subqueries (matched_send_at, send_is_post_correction, send_is_malformed)
  carry the same exclusion.
- A legacy entry's bounce must NOT exhaust the corrected row or fabricate
  `referee_contact_invalid`. Sanity: genuine referee sends always append an sms sibling
  (delivered OR skipped) at the same `at` — so genuine sends are never masked (check the
  sweep's outcomes_to_json writes every channel outcome with one shared `at`).

## 🚨 (c) W2 — the pin must BITE (r4 warning). Closed ONLY if:

- The co-nudge fixture in `co_nudge_bounce_stands_down_test` is LEGACY-shaped (untagged
  single-email entry) with a POST-correction timestamp — deleting the batch-shape exclusion
  from the SQL would turn it red (the entry would match, send_is_post_correction=true,
  exhaust).
- The producer side is pinned: the sweep integration suite asserts the `"kind": "co_nudge"`
  tag lands in the attempts log (server/test/integration/reference_checks_sweep_integration_test.gleam).

## (d) N1–N19 — each fixed as claimed, OR carried with a REAL documented justification:

| # | r4 note (abridged) | r5 claim |
|---|---|---|
| N1 | edit-open overwrites another row's typed trio | FIXED — per-row edit dict (client.gleam / model.gleam / reference_panel.gleam) |
| N2 | Escape-to-close menu div never focused | FIXED — tabindex="-1" + autofocus on the menu div (confirm_modal pattern) |
| N3 | spec-rc4-3 still names deleted substitute_reference_call.sql + "one additive column" | FIXED — spec now names the shared insert + TWO columns |
| N4 | substitution response reference_call_id decoded, never consumed | CARRIED — "informational; the detail refetch carries the real state" (verify the justification exists in code comments) |
| N5 | §8.3 first sentence renders twice | FIXED — duplicate heading/body removed |
| N6 | no_em_dash_test checks the same char twice | FIXED — one check |
| N7 | trio_matches_row snapshot basis silently drops typed referee | FIXED — effective basis (corrected ?? snapshot) |
| N8 | malformed-at inconsistent: '' short-circuit exhausts; prefix-shaped malformed raises | FIXED — send_is_malformed gate stands the event down (walk the NULL-at / present-but-malformed paths) |
| N9 | genuine post-correction fallback-leg failure can no longer match | CARRIED — pre-correction-only fallback is a deliberate trade-off (verify the SQL comment documents it) |
| N10 | verify_vacancy_active DB Error falls into catch-all → action runs | FIXED — Error arm → db_failure 500 |
| N11 | webhooks exhaust_row '_' arm swallows DB Error | FIXED — Error arm → Sentry capture |
| N12 | view_edit_trio inlines literal 'Cancel' | FIXED — copy.refcheck_edit_cancel + pinned in refcheck_action_strings |
| N13 | overflow_actions has no Objected arm | FIXED — Objected → Substitute on can_substitute_referee |
| N14 | refcheck_action_strings omits correct_details | FIXED — added to the list |
| N15 | client dispatch/pins incomplete (substitute-save, start-confirm, export, prefill-level) | FIXED — 3 new client tests (dispatch × 2 + export). CHECK: prefill-level pins (UserChoseRefcheckAction → empty/effective prefill) and the "fires nothing" assertions — added or not? |
| N16 | sweep_mark_failed taken_over guard unpinned | FIXED — sweep_mark_failed_respects_taken_over_test |
| N17 | action-success clears confirm for ANY row | FIXED — confirm clear scoped to call_id |
| N18 | no-edit fallback prefills terminal referee's own trio for Substitute | FIXED — kind-based fallback: Substitute → empty |
| N19 | test-hygiene residue (unused eff, fieldless Model(..model.initial()), base_hooks re-declare, unreachable SQL CASE arm) | FIXED — CHECK each sub-item: client_test.gleam ~6413, reference_panel_test.gleam ~1533, find SQL fallback arm |

## (e) DO NOT RE-LITIGATE (settled — no findings from these):

r1 B1/B2/B3, r2 blocker, r3 blocker, r4's verified-fixed list (W6, N4-fixed, N8-client,
N11-resend, W2-partial, W4, N13, N15, N16, N21), and r4's 7 rejected false-positives
(unused import / doc-vs-SQL / `?slot=` degradation / sweep-exclusion clock / detail-payload
sentinel / stand-down silence / schema-migration checks). The gender-neutral pronouns stay
FLAGGED FOR THE HUMAN — not a finding. FLAG NEW findings ONLY beyond the audit items.

## Lens-guards that remain load-bearing (verify, don't assume):

1. **TAKE-OVER [A7]**: guarded on queued/contact_initiated/unreachable ONLY; late form
   completion still transitions (§8.6); sweep exclusions pinned.
2. **CORRECT [AD-7/A1] ONE-CYCLE**: awaiting guard IS the rule; snapshot immutable;
   cycles=1; re-arm; audit.
3. **SUBSTITUTE IDEMPOTENCE [AD-16]**: double-submit returns the existing successor, no
   duplicate audit; audit carries old + new ids.
4. **EXHAUSTION LIVE**: second failure → unreachable + referee_contact_invalid at BOTH the
   delivery webhooks AND the wrong-person route, with audit + in-app notification.
5. **EXPAND-ONLY MIGRATION**: corrected_name + corrected_at, nothing destructive.
6. **AR-RC13**: client refetches after every action; renders server-computed hooks.
7. **⋯ MENU WIRED**: actions actually dispatch (do NOT flag "menu unwired").
8. **INLINE CONFIRMS, NEVER MODALS**.
9. **COPY VERBATIM + em-dash ban** in implementer-authored user-facing strings.
10. **TIMELINE SORT**: if the timeline/attempt-log composition is touched, the RFC3339-vs-
    `::text` format-mix = a finding.
11. **a11y + AC testids** on menu/confirms/rows; keyboard operable.
12. **base = develop** (RC4.1 + RC4.2 merged — carry-forward only).
