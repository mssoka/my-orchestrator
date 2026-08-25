## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)
**Job:** righttenantry-demo-mode · **Reviewed sha:** `c54c3c5` · **Reviewers:** 7/7 completed (28 lens runs across 4 diff chunks; 4 lenses re-run on deepseek-v4-flash after kimi k3 quota)
**Verification:** 36/37 findings confirmed against the code — 1 discarded as false-positive (breadcrumb "links to real routes" — the links carry demo ids and resolve in-demo).

**MAJOR REWORK** — the two acceptance pillars fail: demo mode issues real network calls on the happy path, and three core demo flows (report download, create/edit vacancy, several refetch surfaces) are functionally broken.

### Blockers (8)

1. **Demo report download always fails** — two independent bugs. `string.drop_start(analysis_id, 3)` maps `"an-aoife"` → `"aoife"`, but the baked PDFs are keyed `"a-aoife"` (`demo_store.report_filenames`); and `uri.parse("/static/demo/…")` yields `host: None`, so `gleam_http request.from_uri` returns `Error` before any fetch. The real `report_api.download` uses `rsvp.parse_relative_uri` for exactly this reason. Every demo download 404s/errors — the headline CTA-moment surface and acceptance item 1. *(acceptance, architecture, blind, codebase, edge, security)* — `client/src/demo/demo_api.gleam:515-560`

2. **Demo mutations discard the mutated store** — all four demo branches in `client.gleam` do `let #(next, eff) = demo_api.…` then `let _ = next`. Create-vacancy, draft/active save, and mark-opened mutate nothing; the stale store re-renders after the response refetch. `demo_update.gleam` does this correctly everywhere else (`demo_store: Some(next)`), so these four sites are the anomalies. Create/edit vacancy is acceptance item 1. *(blind, edge, architecture, codebase)* — `client/src/client.gleam:2537, 5959, 6161, 6275`

3. **Bulk-reject fires a real POST from demo** — `UserClickedMarkAllRejected` / `UserClickedMarkSelectedRejected` are neither intercepted by `demo_update` nor demo-branched in `update_inner`, so "Mark all/selected as rejected" issues a real `application_api.bulk_reject_applications` write from demo. `demo_api.bulk_reject_applications` exists but is never wired. *(edge, security, blind)* — `client/src/client.gleam:4841, 4862`

4. **Unlock CTA and extend button fire real payment calls** — v-harbour is `is_paid: false` with 1 pending application, so the leaderboard renders the unlock CTA; clicking it falls through to real `payment_api.check_consent`. The designed "why pay" demo moment ends in a 401 error toast. Extend button reachable after closing a demo vacancy. *(security, edge)* — `client.gleam:3649-3655, 3845-3853`; `leaderboard_view.gleam:628`; `vacancy_detail.gleam:405`

5. **`refetch_refcheck_effect` has no demo branch** — after any demo refcheck row action, the response handler refetches via the real `application_api.fetch_application_detail` (401), which sets `application_detail: Failure(...)` — the demo applicant detail page is replaced by an error page. *(edge)* — `client.gleam:7089-7097`

6. **Restore refetches archived via the real API** — `ApiReturnedRestoreVacancy(Ok)` calls `vacancy_api.fetch_archived` with no demo branch; in demo this 401s and the archived list renders Failure. *(edge)* — `client.gleam:3427-3438`

7. **Opening the notification bell fires a real fetch and blanks demo notifications** — `UserToggledNotificationDropdown` opens via `notification_api.fetch_notifications` (no demo branch); the 401 sets `notifications: Failure("Couldn't load notifications")`, wiping the seeded demo bell on first open. *(edge)* — `client.gleam:4298-4310`

8. **Settings/profile/password/account-deletion writes reachable in demo** — typing `/settings` in demo exposes profile save, password change, notification prefs and **account deletion**, all firing real `settings_api` writes with `csrf_token: "demo-csrf-token"`. If a logged-in landlord enters demo their session cookie rides along; the bogus CSRF token is the only barrier. Violates "demo issues NO writes to real endpoints". *(security, edge, acceptance)* — `client.gleam:4442, 4494, 4559, 4718, 4783`

### Warnings (15)

- `?payment=success` / `?extended=success` URL arms fire real network in demo (poll + pixel + `vacancy_api.get_detail`) — crafted URL, unguarded.
- `/billing` in demo fires a real `settings_api.fetch_billing_history` (no demo branch).
- Refresh/deep-link on `/vacancies/v-*/edit` boots demo but never loads the edit payload (blank form, `vacancy_edit_id` stays `""`).
- `UserConfirmedApproval` refetches the leaderboard from the **pre-mutation** store (`store_of(model)` instead of `store_of(updated)`) — approved applicant stays under-review; rejection/backward transitions don't refetch at all.
- Reset demo from a non-dashboard page strands the page on a permanent spinner (all surfaces → `NotAsked`, only notifications refetched, no route change).
- **6 of 9 demo analytics events are defined but never fired** (vacancy/application/comparison/archived opens, report download, create open) — deliverable 7 requires surface + download capture.
- Landlord-facing copy hardcoded in `demo_banner.gleam` / `shell.gleam` instead of `copy.gleam` (AGENTS.md violation).
- **Baked PDFs lack the canon-required "Synthetic demo data — not a real applicant." footer** (lavish `demo-flow-design.html` §3) and instead carry production GDPR/confidential boilerplate — misleading on a public marketing asset.
- Sara Walsh affordability flag says "31% of stated income" but the numbers give 72% (€2,450 / €3,400).
- Aoife co-applicant story lost — row has `co_applicant_count: 1` (+€2,400 household) but `to_report_data` passes `co_applicants: []`, so the PDF shows the count with no detail.
- Fixture uses a real person's name ("Grace Kelly") attached to a rejected/eviction/CCJ story — fails the "obviously synthetic, no real persons" spot-check.
- `pdf_prebake main()` ignores its documented CLI argument and exits 0 on failure (documented `gleam run -m demo/pdf_prebake -- server/priv` only works from `server/`).
- **CI no-network lint is heuristic** — it only greps `client/src/demo/` for `rsvp`/`api_helpers`/`gleam/fetch`; the fall-through calls above live in `client.gleam` and pass it, `import api/vacancy_api` in a demo module passes it, and a JS FFI passes it. The pillar-2 "proof" is prose, not a complete mechanism.
- Demo substitute-reference save dispatches as `"correct"` — a substitute behaves as a correction and the typed referee details vanish.
- `create_vacancy` sets `closes_at = created_at` (ignores `validity_days`) — a newly-created demo vacancy renders as closing/closed immediately.

### Notes (13)

- Demo comparison ids + sweep-nudge dismissals write to real sessionStorage/localStorage — small "refresh = reset" exceptions.
- Demo logout fires the `demo_reset` PostHog event (conflates exit with reset).
- Duplicate `gleam/uri` import in `client.gleam` (lines 43-44).
- Stale doc comment — the visibilitychange-listener doc now sits on `handle_browser_change`.
- Six `demo_api` refcheck mirror wrappers (incl. `substitute_reference`) are orphaned; several fixture helpers unused.
- `pdf_prebake.gleam` ships four unused imports + a dead `str_opt` helper.
- Demo breadcrumb home segment labelled "Dashboard" but links to `/demo`.
- `download_timeout` duplicated between `client.gleam` and `demo_update.gleam`.
- Marta's `category_scores` omits `rental_history` (5 keys vs 6 elsewhere).
- Employer reference name/email mismatch (Rachel O'Brien / `roberts@finlaydigital`).
- Demo notification click doesn't close the dropdown (real arm does).
- Mock dashboard counts in the design artifact contradict the fixture table (8 scored vs "6 of 8").
- Advisory test gate: **CONCERNS** — P0 pillars have non-prose pins, but the download path (the one permitted network touch) and the boot path are untested, and no `/demo` E2E scenario exists.

### Reviewer agreement

Highest-confidence findings (≥3 independent lenses, all code-verified): the report-download failure (6 lenses), the discarded-store mutations (4), the no-network fall-through class as a whole (4+), and the stale-store approval refetch (4).

### What passed

- **Live-path inertness holds** — the real `client/src/api/*` modules are untouched by the diff; the ~20 demo branches are all `case model.demo_mode` guarded and inert when `False`; `shared/routes` change is additive (Demo constructor).
- **No new backend surface** — `server/src/demo/pdf_prebake.gleam` is a dev-time CLI, not a route; no Stripe/email/AI endpoint is added. Guard 6 holds.
- **PDFs are static** — 8 committed assets in `server/priv/static/demo/`, served as static files; zero per-call AI cost. Guard 7 holds.
- **Chrome + CTA honor the verdict** — persistent banner, reset button, "Create your vacancy →" CTA at moment B, hero + nav entry, demo renders the real view components. (Except the missing synthetic footer — see W.)

**Verdict:** MAJOR REWORK NEEDED

_Address findings and push — I re-review automatically on the new sha._
