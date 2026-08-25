## 🤖 Perkins automated review — round 5 of 3
**Job:** righttenantry-refcheck-rc4-3 · **Reviewed sha:** ccc0ff6 · **Reviewers:** 7/7 completed
**Verification:** 22/71 findings confirmed against the code — 12 discarded as false-positive

### Blockers (0)

None. The r4 blocker is closed — verified in the worktree, all three requirements:

- **B1 CLOSED.** `apply_wrong_person` (form_handler.gleam:1255) executes `mark_awaiting_correction_wrong_person`; the unguarded `update_reference_call_status` call is gone from the wrong-person path. The guarded SQL carries BOTH backstops (`taken_over_at IS NULL` AND `correction_cycles = 0`). The race pin `wrong_person_taken_over_race_stands_down_test` drives the real POST route (303, status untouched, zero audit) AND calls the SQL directly (0 rows on the taken-over row + a 1-row control). The r2/r3/r4 dead-end scenario is structurally impossible at ccc0ff6.
- **W1 CLOSED.** The legacy co-nudge exclusion (kind tag OR single-email batch with no sms sibling at the same `at`) rides all four legs of the find (matched_send_at, send_is_post_correction, send_is_malformed, EXISTS). Genuine referee sends always carry an sms sibling (delivered/skipped/failed) at one shared `at`, so they are never masked.
- **W2 CLOSED.** The co-nudge fixture is legacy-shaped with a post-correction timestamp — deleting the exclusion turns it red; the producer-side `"kind": "co_nudge"` tag is pinned in the sweep integration suite.
- **N1–N19:** N4 and N9 carried with real, documented justifications (verified in code). The rest fixed as claimed, with the residue listed below.

### Warnings (1)

1. **NEW (blind+acceptance+architecture+codebase): the r2 W1 typed-compare gate lost its pins.** Both stale-bounce fixtures (`stale_pre_correction_failure_stands_down_test` :944, `same_day_stale_bounce_stands_down_test` :1450) seed a single-email entry the new batch-shape exclusion removes BEFORE the gate — the stand-down now runs via the 0-row path, and the `send_is_post_correction` timestamptz compare is never exercised. Breaking the gate would not turn these red (the r5 delta added an sms sibling to the *genuine* fixture but not the two stale ones). Add an sms sibling at the same `at` to both fixtures, as was done for `genuine_post_correction_failure_exhausts_test`.

### Notes (18)

**Fix-audit residue (note-level, not blocking):**
1. N15 partial — the three new dispatch tests assert only the inflight marker; prefill-level pins (UserChoseRefcheckAction → substitute-empty / corrected-override) and the "fires nothing" effect assertions remain missing.
2. N19 partial — unused `eff` bindings (4 sites), the fieldless `model.Model(..model.initial())` update, and the `base_hooks` shadow in `objected_row_substitute_surface_test` remain (the SQL CASE arm was fixed).
3. N8 partial — present-but-malformed `at` stands down, but a *missing* at key still exhausts via the `''` short-circuit (NULL regex → COALESCE false), and the branch has no test. Phantom today (every writer stamps `at`), but the claimed consistency is incomplete.
4. N7 residue — `effective_value` in actions_handler lacks the `correction_cycles >= 1 → corrected-only` arm the sweep and panel have: a corrected row with a cleared channel resurrects the snapshot in the substitute compare (the panel prefills `''` post-correction), so SameReferee can miss on that edge. Untested either way.
5. N1/N17 unpinned — no two-row test; the success-path test starts from an already-clean fixture (only the toast count can fail).
6. N2/N13 unpinned — no view test for the Objected menu arm, the take-over hook-negative, or the tabindex/autofocus Escape contract.
7. N3 third spot — spec-rc4-3:352's summary still names only `corrected_name TEXT` (the migration adds `corrected_at` too).
8. N5 leaves `refcheck_correction_heading/body` dead — referenced only by the em-dash scan list.
9. N11 pattern one branch over — `apply_delivery_failure`'s `mark_awaiting_correction` `_` arm still swallows DB errors as a silent stand-down.

**New observations (all verified, none blocking):**
10. `verify_application_in_vacancy` DB errors fall into the 404 catch-all ("Application not found") — fail-safe but misreported; the N10 fix covered only the sibling vacancy-active check.
11. The kind-tag consumer exclusion arm is unpinned — the W2 fixture was swapped to the legacy shape, so no test exercises `e ? 'kind'` with a tagged entry.
12. After a substitution, the retained history row keeps a live substitute affordance (status-based hook); saving the successor's trio there 200-no-ops with a "Substituted" success toast, a different trio 409s — a UX dead-end.
13. Slot-scoped data-testids (`refcheck-row-<slot>` etc.) collide when a history row and its successor share a slot — latent E2E selector ambiguity (no current scenario targets them).
14. Skip / re-enable (immediate-fire) leaves a pending same-row confirm armed — it goes invisible after the refetch but survives in the model.
15. `no_forbidden_words_test` scans only toast/page arms — the RC4.3 consts bypass the error/failed/retry ban scan (no current violations; latent).
16. The three action POST router arms and the N10/N11 error arms are untested at the route level (handler-level only); the API-wire tests pin URLs only.
17. Exhaust UPDATE, stamp, audit and notify are separate statements — a process crash after the UPDATE commits loses `referee_contact_invalid` (the re-delivered event finds 0 live rows). Documented best-effort posture; accept or wrap in one transaction.
18. A substitute no-op returns 200 `substituted:true` when the slot's live occupant is a SKIPPED successor with the same trio (`is_terminal` omits skipped) — the re-substitute is a silent no-op.

### Reviewer agreement

The typed-compare warning carries 4-source agreement (blind, acceptance, architecture, codebase). The B1/W1/W2 closures and the N4/N9 carries were independently verified against the worktree by the conductor; the lenses' two "genuine email-only sends are excluded" warnings were verified FALSE (the sweep always appends an sms sibling, skipped included, at one shared `at`).

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._ (Round-5 note: the human already overrode the cap for this round; the one warning + 18 notes are advisory — no rework is required for merge.)
