## 🤖 Perkins automated review — round 2 (cap lifted — loop until approved)

**Job:** righttenantry-demo-mode · **Reviewed sha:** `1c2a6a9` · **Reviewers:** 21/21 lens runs completed (7 lenses × 3 diff chunks; zero failures)
**Verification:** 36/39 distinct findings confirmed against the code — 3 discarded as false-positive

### Fix audit (r1 → r2, re-derived against the fresh tree)

**r1 blockers: 7 of 8 verified-FIXED in source** (B1 download+test ✓, B2 store-threading ✓, B3 bulk-reject ✓, B4 unlock/extend ✓, B5 refcheck refetch ✓, B6 restore refetch ✓, B7 bell ✓, B8 settings/billing ✓) — **but B2's fix class has no biting pin** (blocker 5). Pillar 1 (no real network from demo) **holds**: every api call site in `client.gleam` was individually re-verified guarded/intercepted/exempt-with-reasoning; the structural lint runs clean on the tree and **fails on a synthetic unguarded call** (bite-tested). Pillar 2 holds for endpoints (no real writes reachable, settings interception is total) **but breaks at the exit boundary** (blocker 1).

**Warning folds: 7 of 12 landed** (URL arms ✓, approval post-mutation store ✓, PDF synthetic footer ✓ on all 8 PDFs, Aoife co-applicant ✓, Sara 72% ✓, prebake env-override ✓, billing ✓). Did **not** land: edit deep-link payload (→ blocker 4), reset navigates home (→ W1), all 9 analytics fire (→ W2), real-person fixture swap client-side (→ blocker 3), closes_at symptom (→ W3), substitute contact (→ W4), copy.gleam banner message (→ W5).

### Blockers (5)

**1. Exiting the demo leaks demo data into the real product.** Both demo exits (`BrowserChangedUrl` public-route arm, `UserClickedLogout` demo arm) clear only `demo_mode`/`demo_store`/`auth` — `vacancies` stays `Success(demo data)` and the Dashboard refetch gates on `NotAsked`, so **after demo exit → signup → /dashboard, a real new landlord sees v-maples/v-harbour as their vacancies until a hard reload.** The demo's own conversion path. `client.gleam:486-503`, `demo_update.gleam` logout arm. *(edge + Perkins, verified end-to-end)*

**2. Deep-link demo entry strands the dashboard.** Boot on `/vacancies/v-maples` (shared URLs are a core entry) leaves `vacancies: Loading` forever; `enter_demo` sets Loading, `demo_entry_effects` never resolves it for detail boots, and the sidebar `/dashboard` refetch arm matches only `routes.Dashboard, NotAsked` — Loading falls through → **permanent skeleton on the demo's most basic navigation**. `client.gleam:5795-5799`, `5164-5176`, `shell.gleam:85`. *(blind + Perkins, verified)*

**3. 'Grace Kelly' is still on the demo UI (still present since round 1).** The r1 #19 fix renamed the **PDF** to Gráinne Foley but the client fixture (`demo_fixtures.gleam:93`) still renders **Grace Kelly** — rejected + eviction + CCJs — on the public leaderboard, and now **mismatches its own downloadable report** for the same id `a-grace` (the pdf_prebake header even claims "same names"). Real-person adverse data on a public marketing page; the fix didn't bite at its r1-cited location. *(6 lenses + Perkins, verified verbatim)*

**4. Demo edit deep-link still boots an empty form (r1 #11 fold did not land).** `demo_entry_effects` has **no VacancyEdit arm**; `init` never dispatches `BrowserChangedUrl`, so refresh on `/vacancies/v-maples/edit` sets `vacancy_edit_id` but never fires `demo_api.get_for_edit` — the form renders empty and save shows validation errors. `client.gleam:5823-5853`. *(5 lenses + Perkins, verified)*

**5. P0 demo wiring is unpinned — advisory gate: FAIL.** No test dispatches a demo create/edit/publish/bulk-reject through `client.update` and asserts the store changed: `demo_flow_test` covers request/response/reset/exit only, `fixtures_conformance_test` mutates the store directly. **Reverting any B2 store-threading fix to `let _ = next` keeps all 597 client tests green and the lint clean.** All three tests lenses independently failed the gate; the round's bar is "verified-fixed with a biting test/lint." `client/test/demo/demo_flow_test.gleam`. *(tests ×3 + acceptance + Perkins)*

### Warnings (11)

1. **Reset from a non-dashboard page still strands on a permanent skeleton** — `reset_demo` seeds dashboard Success (that case is fixed) but detail/archived/comparison go `NotAsked` with no refetch and no navigation; "reset navigates home" fold did not land. *(5 lenses)*
2. **Surface analytics are vacuous** — `demo_application_open`/`demo_comparison_open` are wired to messages **no production code dispatches**; `demo_vacancy_open`/`demo_archived_open` only fire from error-retry buttons that never render in the error-free demo. 4 of 9 events never fire; deliverable 7 unmet.
3. **Created demo vacancies render 'Closes today'** — the `closes_at = now + validity_days` fix is computed but nothing consumes it; views branch on `days_remaining`, which is a hardcoded id map returning **0** for created vacancies. The "Create your vacancy" moment produces a closed-looking card.
4. **Substitute edit still discards the typed referee contact** — dispatch now distinguishes substitute/correct (half of r1 #22), but `apply_refcheck`'s substitute branch just nulls the contacts instead of applying the typed ones.
5. **Banner message still inlined** — `copy.demo_banner_message` ships **unused** while `demo_banner.gleam:33` inlines the identical string (r1 #15 half-landed).
6. **Structural lint soundness gaps** — reproduced a vacuous pass: an unguarded `payment_api` call in a fresh arm **passes** when an unrelated arm's `model.demo_mode` guard sits within the 35-line window (arm boundaries ignored); the workflow grep doesn't ban `import api/*` inside `demo/`; `DEMO_INTERCEPTED` is hand-synced with `demo_update.handle` (nothing verifies it); helper-mediated calls (`poller.tick_effects` wraps 3 real api modules) are lint-invisible and their arms are absent from the manifest; 4 helpers are allowlisted as "demo-branched" but contain no demo branch (`dispatch_status_update` — demo-safe today only via caller interception). Pillar 1 holds **today**; the pin is weaker than claimed.
7. **Navigating to /demo re-seeds the store**, silently discarding in-session demo mutations (unconditional `enter_demo` on every `routes.Demo` URL change) — only refresh/reset should wipe.
8. **Refcheck re-enable/take-over show "Referee substituted"** — demo fires `re_enable`/`take_over` (underscores); the shared toast matcher expects `re-enable`/`take-over` (hyphens) → wrong fallback copy.
9. **`add_days_iso` does a single month rollover** — validity ≥ ~43 days yields impossible dates (`2026-09-33`).
10. **pdf_prebake still exits 0 when PDFs fail** and swallows mkdir errors (r1 #20 half-landed; env override did land).
11. **Entering demo clobbers a live session; exit downgrades auth to NotAsked** — a logged-in landlord who hand-types /demo loses their SPA session view until reload (adjacent to blocker 1; same transition-hygiene root).

### Notes (20)

Comparison-ids/sweep-nudges still write real web storage (r1 #24) · visibilitychange doc still misplaced (r1 #27) · zero-caller exports shipped (`demo_api.check_session`, `all_fixture_jsons`, `decode_checked`, `result_to_seed_error`, `capture_with_props`) · pdf_prebake unused imports · `download_timeout`/`store_of` duplicated (r1 #31) · Marta still 5-of-6 category keys (r1 #32 — re-verified) · reference name/email mismatch + Aoife PDF phone vs UI (r1 #33) · reminders/bulk-invite mutate nothing, hardcoded counts contradict the awaiting list · `demo_not_in_demo_toast` id convention collides with `add_toast` · dead `routes.Demo` arm in `view_protected_page` · `id_suffix` 8-char truncation collides ids for same-prefix names · `fetch_leaderboard_page` ignores its page param (latent; load-more hidden in demo today) · store-side `mark_opened` lacks a status guard (latent) · demo boot skips visibility-refresh listener + hydrations for the tab lifetime · latent policy-modal → real `accept_policy` POST if an authed `/demo` link ever appears (`server_policy_version` survives `enter_demo`; lint exempt-comment is false for this path) · FFI `can_capture()` runs outside the try/catch (violates documented fail-open) · `report_download_test` doesn't pin asset presence or the store-side id contract · `demo_requests_are_intercepted_test` can't distinguish demo from real dispatch; header claims bug-hunt coverage that doesn't exist · compiler warnings on new code (unused `eff`, unused `gleam/option`) · PDF flag strings em-dash-drift from the client store copy (pdf_prebake outside lint scope).

### Reviewer agreement

Multi-lens confirmed (highest confidence): **blocker 3** (6 lenses), **blocker 4** (5 lenses), **warning 1** (5 lenses), **warning 3** (4 lenses), **blocker 5** (4 lenses incl. all three tests lenses), **warning 6** (7 lenses, incl. two reproduced bite-tests). Rejected as false-positive: security-b's "policy-gate `check_session` fires in demo" (demo errors are always `internal_error`, never 428 — unreachable); acceptance-c's breadcrumb carry-forward (r1's exact case is fixed; link-back labels accurately name the destination); blind-b's rejection-refetch inconsistency (demo mirrors the real flow exactly).

**Verdict: MAJOR REWORK NEEDED**

The r1 blocker fixes are genuinely in and pillar 1 held up under adversarial re-verification — the rework was substantive. But the round's bar (folds land, pins bite) is missed in five places, two **new** mode-transition bugs landed (one of which puts fake vacancies on a real customer's dashboard), and the real-person name is still live on the public UI.

_Address findings and push — I re-review automatically on the new sha._
