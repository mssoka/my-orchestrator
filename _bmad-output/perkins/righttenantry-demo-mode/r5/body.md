## 🤖 Perkins automated review — round 5 of 3

**Job:** righttenantry-demo-mode · **Reviewed sha:** `2330189` (head of `demo-mode`, base `develop`) · head unchanged at post time.
**Reviewers:** 7/7 lenses × 3 chunks = 21/21 completed (glm-5.3, two 429-wave recoveries, none degraded).

### Fix audit (r4 → r5) — both blockers FIXED, all 12 claimed warning folds verified landed

- **B1 (lint vacuous on the fn-helper path): FIXED.** `DEMO_BRANCHED_HELPERS` skip deleted — no skip list remains. Guard matcher now accepts any-receiver `case <x>.demo_mode` as a case *statement* at equal-or-shallower depth (comments can't satisfy it); the three fn-helpers are verified via `FN_INTERCEPTED_TRIGGERS`, itself checked against `DEMO_INTERCEPTED`, itself checked against `demo_update.handle`. The r4 dead demo branches in the refcheck helpers are gone. I ran the lint (clean) and **all 8 bite-tests personally — every one bites**; trigger lists are complete (audited all 8 call sites' enclosing arms).
- **B2 (demo entry unpinned): FIXED.** Both entry paths pinned through `client.update` on a **non-demo** model (landing-CTA nav + `is_demo_route` deep-link boot), asserting demo_mode, seeded store, mock-landlord auth swap, and NotAsked→Loading / request-id. The pins bite.
- **Warning folds:** W1 stash/restore (pinned both ways), W8 Back-re-entry, W9 PolicyRefresh guard, W10 eff batching, W11 optimistic unread, W12 Grace 98% + PDFs re-baked (verified in the commit's file stat), W13/W14 pins, W15 dead-branch deletion, W16 reset seed-failure exit, 15-field exit pin, audit-trigger derivation — **all verified in code, none re-litigated**.
- **Local suites re-run (CI billing-blocked):** shared 119 / client 621 / server 1527+549 skipped — all green.

### BLOCKERS (0)

None. The no-network pillar holds: the lint mechanism genuinely bites, demo-seeded responses can't trigger the policy-refetch path (demo errors are `internal_error` only), and every demo-reachable request arm is intercepted or guarded.

### WARNINGS (14) — top items

1. **[NEW, acceptance+blind] `update()`'s policy-refetch wrapper can fire a real `/me` from demo mode** — an in-flight real 428 landing after demo entry batches `auth_api.check_session` with no demo guard (`client.gleam:286-297`); the lint can't see it because `update()`'s own demo-dispatch `case` masks the call site (positional matcher) and `auth_api` isn't in `API_MODULES`. Same in-flight class as r4's W9; response side is already guarded. Fix: skip the refetch when `next_model.demo_mode`.
2. **[NEW, blind] ESA fixture copy** — harbour vacancy `requirements`: "Sea view. **Single professional preferred.**" Civil status is an Equal Status Acts ground; discriminatory-ad-adjacent copy in the public demo. Reword (e.g. "Sea view.").
3. **[NEW, blind] `RefcheckEditCorrect` discards the typed corrections** — demo `apply_refcheck("correct")` only bumps `correction_cycles`; the real `correct_reference` POSTs the typed name/email/phone. A landlord correcting a typo sees the stale contact persist.
4. **[NEW, blind] `enter_demo` omits `payment_polling`/`scoring_generation` resets** that `handle_browser_change` performs — real in-flight scoring/policy responses can transiently write real data into demo surfaces (chains die via interception; narrow race).
5. **[NEW, tests] W10 payment/extended demo arms have zero coverage** — reverting the eff batching stays green.
6. **Carried since r4 (not re-counted):** dirty-edit exit clears demo state before the unsaved-changes guard (6 lenses); dispatch arms still partially unpinned (refcheck trio, single mark-read, mark-opened threading, edit deep-link boot); comparison ids/sweep dismissals write real web storage; Ok-unconditional store mutations; `mark_opened` doc vs behaviour; create_vacancy id collisions (doc claims the opposite); reminders are canned no-ops; Declan household-income invariant; W11's model-level pin stays vacuous (store half bites).

### NOTES (91)

Unchanged carried tail (fixture arithmetic, PDF/fixture drift, lint trust residuals like EXEMPT_ARMS prose and the manifest's capitalized-line matcher, doc/placement nits, render-coverage gaps) plus small new ones: design artifact claims a fetch-spy test that doesn't exist (the lint+bite-tests are the real mechanism), PDF freshness guard, O'Sullivan PDF email differs from fixture, `clear_demo_state` leaves toasts, bulk_reject audit trigger hardcodes `leaderboard_select`, demo notification click drops entity navigation.

### Reviewer agreement

43 findings confirmed by ≥2 independent lenses (max 7: create_vacancy ids, reminders no-op). All four solo "new" warnings were independently re-verified by me against the tree before reporting.

**Verification:** 105/109 lens findings survived re-verification — 4 discarded as false-positive (W8-unpinned claim: the B2 deep-link pin drives exactly that arm; single-read unread parity holds via the shared response handler; Back-to-protected staying in demo is sandbox-by-design with no network; deep-link NotAsked-vs-Loading was adjudicated in r3-B1).

### Verdict

**READY TO MERGE — 0 blockers.** The r4 blockers both bit-fixed and verified; the no-network pillar is mechanically enforced and locally proven. The 14 warnings (2 compliance/fidelity, 2 narrow in-flight races, 10 carried polish) are follow-up material, none gating.

_Address findings and push — I re-review automatically on the new sha._
