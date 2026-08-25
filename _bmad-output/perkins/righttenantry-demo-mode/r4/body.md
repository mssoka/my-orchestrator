## 🤖 Perkins automated review — round 4 of 3
*(loop-until-APPROVED — rounds continue until APPROVED)*

**Job:** righttenantry-demo-mode · **Reviewed sha:** `4bff855` · **Reviewers:** 21/21 lens runs completed (7 lenses × 3 chunks)
**Verification:** 232/238 findings confirmed against the code — 6 discarded as false-positive

**Model note:** wave a + blind-b on kimi-coding/k3; k3 billing-403 killed six wave-b lenses mid-flight; the glm-5.3 retry hit the 429/1302 wave; standard recovery (one continue per pane) on restored k3 quota. All 21 lens runs completed — no degraded layers.

### Fix audit (r3 → r4)

| r3 finding | Status | Evidence |
|---|---|---|
| **B1** /demo nav after deep-link boot strands skeleton | ✅ **fixed** | Fetch gate now covers `routes.Demo, NotAsked \| routes.Dashboard, NotAsked` (client.gleam:5158-5179, effect + Loading both); in-demo `/demo` re-nav goes through `handle_browser_change` (:489); regression pin `demo_deep_link_boot_state_test` drives BrowserChangedUrl `/demo` with NotAsked → Loading. |
| **B2** CI grep lint self-trips on demo_api's `api/api_error` import | ✅ **fixed** | Grep narrowed to network-capable modules (`api_helpers`, `^import api/(vacancy|…)_api`); block run **verbatim on this tree: GREEN**; `api_error` documented as an allowed shared type. |
| **B3** lint structurally unsound (cross-arm bleed, comment-only manifest, no bite-tests) | ⚠️ **fixed-with-residue** | Arm-bounded window + depth-qualified guard, manifest subset check vs `demo_update.handle`, 4 bite-tests wired into test.yml:155 — ran them: 4/4 bite, clean tree passes. **Residue promoted to new Blocker 1** (below). |
| **B4** advisory test gate FAIL | ⚠️ **fixed-with-residue** | All-15-field exit pins (both exits), close/archive/restore/status-change/mark-read dispatch pins, refcheck store-level pins, deep-link boot pin, rollover pin — all real; client suite re-run: **611 passed, no failures**. **Residue → new Blocker 2** (below). |

r3 warnings: fixed — exit-hygiene full pin, store-threading pins (close/archive/restore/status/mark-read), §8.3 substitute validation, scoring_status pending, remindable/followup derivation. Partial — refcheck coverage (store-level only), DEMO_BRANCHED_HELPERS branches (added but dead — see W15). Still present — session clobber, dirty-edit exit order, Ok-unconditional mutations, mark_opened, id collision, reminder no-ops, Declan household.

### Blockers (2)

**1. The no-network lint still passes vacuously on the fn-helper path.** `DEMO_BRANCHED_HELPERS` skips verification for 8 fns (`lint_demo_network.py:166-167`) while the comment (:114-118) claims they're "verified by the arm scan like any other scope" — no such verification runs. Perkins experiment: deleting the skip makes the lint **FAIL** on `client.gleam:7591`+`7609` (`reference_checks_api.correct_reference`/`substitute_reference`, scope `<fn:save_refcheck_edit>`) because that fn guards on `case saving.demo_mode` — invisible to the textual matcher, which only knows `model.demo_mode`/`updated_model.demo_mode` (a comment containing the substring would also satisfy it). Worse: the r4-added demo branches in `fire_refcheck_slot_action`/`fire_refcheck_call_action`/`save_refcheck_edit` are **dead code** — `demo_update.handle` intercepts their trigger messages (`UserChoseRefcheckAction` immediate kinds, `UserConfirmedRefcheckAction`, `UserSavedRefcheckEdit`) before `update_inner` ever runs them in demo, so the "branch" defense is illusory; the real defense is interception, which the manifest doesn't claim for those triggers. No bite-test covers helper-scope vacuousness. Under this round's hard rule (a lint that passes vacuously = blocker, r3-B3 class): **blocker**. Fix: match any `*.demo_mode` receiver in `demo_guard_in_same_scope`, delete the skip (or verify those fns via the interception manifest), delete the dead branches, add the missing bite-test.

**2. Advisory test gate: FAIL — the demo entry transition has zero dispatch-level coverage.** Both existing "entry" tests hand-build the demo model (`demo_entry_shows_dashboard_test`, and the r4 deep-link pin starts from a hand-built `demo_mode: True` model). No test drives `client.update` on a **non-demo** model with `BrowserChangedUrl(/demo)` (the landing-CTA path, client.gleam:488) or the boot `is_demo_route` path (:227). The feature's front door — seeding, auth swap, NotAsked resets, and the Error arm (route desync, r3 note) — is unpinned; a revert stays green. P0 < 100% → gate FAIL (narrower than r3's, still failing). Fix: one dispatch test per entry path (CTA nav + deep-link boot), asserting `demo_mode`, seeded store, swapped auth, and dashboard `NotAsked → Loading`.

### Warnings (16)

1. **still present since r3:** entering demo clobbers a live landlord session (auth + CSRF, no stash/restore); exit downgrades auth to NotAsked. (10 lenses agree)
2. **still present since r3:** demo exit from a dirty edit page clears demo state *before* the unsaved-changes guard fires. (7 lenses)
3. **still present since r3:** vacancy/status mutations return `Ok` unconditionally — nonexistent ids report success. (6 lenses)
4. **still present since r3:** `mark_opened` doc claims idempotent Submitted→UnderReview but applies to any status. (6 lenses)
5. **still present since r3:** `create_vacancy` ids are 8-char slugs with no uniqueness check — identical names collide. (6 lenses)
6. **still present since r3:** `send_reminder`/`remind_applicant`/`send_bulk_invite` discard the mutated store (`let _ = next`) and return canned counts contradicting the seeded awaiting list. (7 lenses)
7. **still present since r3 (stronger framing):** Declan's household income (650k) violates the fixtures header's now-explicit invariant ("equals primary income + income sources + co-applicants"; his primary is 350k, co-applicants 0). (5 lenses)
8. **NEW:** post-exit browser Back to a demo deep link fires a **real api read with a fixture id** — `is_demo_route` is consulted at boot (:227) but not in BrowserChangedUrl's `_, False` arm (:487-499). Read-only 404, but asymmetric with refresh-on-same-URL.
9. **NEW:** `ApiReturnedPolicyRefresh` lacks the demo guard its `EXEMPT_ARMS` comment claims — an in-flight background `/me` response landing after demo entry overwrites demo auth/csrf with the real landlord's (contrast `ApiReturnedSession`, which has the guard at :1024).
10. **NEW:** demo `?payment=success`/`?extended=success` arms return bare `modem.replace(...)` and discard the accumulated `eff` (real arms batch `[eff, …]`) — crafted demo URLs strand the detail+leaderboard skeleton.
11. **NEW:** demo mark-all-read leaves the badge/dropdown stale — no optimistic `unread_count: 0` (real arm sets it), `ApiReturnedMarkAllRead(Ok)` is a no-op, and the r4 pin is vacuous (`demo_model()` starts at 0).
12. **NEW:** Grace's baked-PDF flag is arithmetically wrong — "Income covers only 58% of the rent requirement" when income/rent = 240000/245000 = **98%**. User-facing scoring claim in a shipped demo artifact.
13. **still present since r3 (partial):** demo dispatch arms remain unpinned — refcheck (`UserSavedRefcheckEdit`/`UserConfirmedRefcheckAction`/`UserChoseRefcheckAction`), single mark-read, edit deep-link boot (`get_for_edit`), awaiting/comparison/scoring/report/load-more request arms, mark-opened threading, and the new defensive guards. All existing refcheck dispatch tests run non-demo models.
14. **NEW:** three r4-fixed store behaviours are revert-green — scoring `in_progress=pending` (conformance pins only the zero-pending vacancy), remindable/followup derivation (no pins).
15. **NEW:** dead demo branches shipped in the three refcheck helpers — unreachable duplication of `demo_update`'s live logic; drift between the two implementations is invisible.
16. **NEW:** `reset_demo` swallows seed failure (`Error(_) -> #(model, effect.none())`) — a dead click with no feedback.

### Notes (40)

Carry-forwards re-verified at this sha: demo writes to real web storage (comparison ids, sweep-nudges) · latent policy-modal `accept_policy` POST (UserAcceptedPolicy exempted, not intercepted) · analytics undercount on deep-link boots · comparison deep link consumes persisted real localStorage ids · seed-failure route desync · edit-boot empty first frame · boot skips visibility listener/hydrations · dead `routes.Demo` arm in `view_protected_page` · `download_timeout`/`store_of` duplication · `demo_not_in_demo_toast` id convention · zero-caller exports (`demo_store.notifications`, `result_to_seed_error`) · `status_from_slug` coercion · `fetch_leaderboard_page` ignores page · report_download doesn't pin baked-asset presence · demo_flow_test header claims nonexistent bug-hunt coverage; intercepted-test can't distinguish demo from real dispatch · pdf_prebake CLI-arg docs vs env switch · Aoife's PDF phone still hidden · Marta's 5-of-6 category scores · design mock still carries 'Grace Kelly' · unused `eff` in client_test · copy.gleam constant placement · policy doc block detached onto `clear_demo_state` · enter_demo skips full navigation reset (focus trap/polling).

New this round: maples/harbour `created_at + validity_days ≠ closes_at` (36d/31d; Sunningdale's 30d is right) · `change_status` hardcodes `"trigger":"manual"` even for `status_auto_changed` · demo_update header overstates the CI ban (file-level fetch/rsvp exemption) · CI fetch ban exempts all of demo_api.gleam, not just `download` · `EXEMPT_ARMS` trusts comments over code (17 arms) · manifest matcher over-counts capitalized body lines as handled (theoretical) · dead `routes.Dashboard` arms in enter_demo/demo_entry_effects · `for_edit` reports `updated_at: created_at`; update never bumps timestamps · `store_of` None fallback re-seeds per call without write-back · `seed_error_from_result` discards the DecodeError · pdf_prebake/client fixture duplication with no consistency check · demo_analytics props documented but hardcoded `{}` · via-nav exit pin asserts 12 of 15 fields · shell/breadcrumb demo chrome has no render coverage · `before` bound-and-discarded in the create test · pdf_prebake unused imports.

### Reviewer agreement

Multi-lens confirmed (highest confidence): session clobber (10 lenses) · reminder no-ops (7) · dirty-edit exit order (7) · Ok-unconditional mutations (6) · mark_opened (6) · id collision (6) · Declan household invariant (5) · refcheck dispatch pins partial (5) · lint fn-helper vacuousness (3 + Perkins experiment).

**Rejected as false-positive (6):** `int_to_string` wrapper (symbol doesn't exist) · Sunningdale draft/archived inconsistency (seed patches `archived_at`) · negative-validity malformed dates (shared 1-30 validation gates it) · approval-vs-rejection leaderboard asymmetry (demo mirrors the real flow exactly — third consecutive reject) · tests-c "gate PASS" (chunk-incomplete view) · one manifest-matcher framing (kept as note instead).

### Verdict

**NEEDS CHANGES** — the four r3 blockers all bit (gate widened, bite-tests real, suite green at 611), but the lint still has one vacuous-pass vector (fn-helper skip + dead branches) and the demo's front door (entry transition) remains unpinned.

_Address findings and push — I re-review automatically on the new sha._
