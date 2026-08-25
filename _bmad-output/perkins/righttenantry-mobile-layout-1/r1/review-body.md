## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-mobile-layout-1 · **Reviewed sha:** `2879deefdfe2d26e95f59ba788a3a2e4ae1d94e7`
**Reviewers:** 7/7 completed · **Verification:** 8/12 reviewer findings survived code re-verification (2 rejected as re-litigating user-approved design, 2 merged duplicates)
**Local ground truth (CI billing-blocked):** client suite **632 passed, no failures**; built Tailwind CSS contains `pb-28`, `overflow-x-auto`, `shrink-0`, `min-h-[44px]`.

The five fixes all bite: pb-28 on both detail pages, scroll-rail steppers (all three), shrink-0 filter pills, 44px demo targets, and the application deep-link with demo+live resolution and both entity types marking read. Two blockers hold the contract short of the bar.

### BLOCKERS (2)

1. **Stale leaderboard can resolve a fabricated vacancy id** [edge] — `client/src/client.gleam:6918` (`resolve_application_vacancy`) + `:6887` (`get_vacancy_id`).
   `handle_browser_change` resets `leaderboard` to `Loading` only on `VacancyDetail`/`VacancyHandoff` entry — `VacancyEdit`, `Comparison`, and deep-linked `ApplicationDetail` entry leave a stale `Success` behind, and `get_vacancy_id` returns `Some(id)` for all of them. Sequence: visit `VacancyDetail(A)` (leaderboard `Success(A)`) → navigate to `/vacancies/B/edit` or `/vacancies/B/compare` (URL or back-nav) → click a real application notification belonging to A → resolver returns `Some(B)` → navigates to `/vacancies/B/applications/<aid-of-A>`. That is the fabricated-vacancy-id case the hard-blocker guard names and the resolver's own doc comment claims to avoid — and real application-typed notifications exist (`server/src/ai/ai_notifications.gleam:56`, AI-failure notifications carry only the application id).
   **Fix:** tag the leaderboard with the vacancy id it was fetched for (`leaderboard_vacancy_id` set alongside the fetch/response) and require it to equal the route vid in `resolve_application_vacancy`; or reset `leaderboard` on the other vacancy-scoped route entries too.

2. **No navigation (click → route) pin for vacancy-typed notifications** [tests, acceptance] — `client/test/client_test.gleam:4953`.
   The hard-blocker class requires a navigation test (click → route) for BOTH entity types. The application side pins the routing decision via `resolve_application_vacancy`; the vacancy side asserts only `show_notification_dropdown == False` despite "keeps_navigating" in the test name, and no other test pins vacancy notification click → `/vacancies/<vid>`. Advisory test gate: FAIL on this pin alone.
   **Fix:** extract the vacancy path construction into a pure helper (mirroring the resolver) and pin it, so both entity types have a routing-decision test.

### WARNINGS (2)

1. **`vacancy_detail` pb-28 padding untested** [tests] — `client/src/pages/vacancy_detail.gleam:104`. Fix 1 requires pb-28 on BOTH pages; only `application_detail` is pinned (`client_test.gleam:5022-5043`). Mirror the test for `vacancy_detail`.
2. **Filter-pill `shrink-0` (fix 3 root-cause) untested** [tests] — `client/src/components/leaderboard_view.gleam:407`. The only `shrink-0` pin is the stepper's; a revert of the pill class would go uncaught. Add a `leaderboard_view` render test.

### NOTES (4)

1. **Demo arm still never navigates vacancy-typed notifications; comment overclaims parity** [blind] — `demo_update.gleam:551-575`. Pre-existing gap (unchanged by this diff), but the "same behaviour the real arm now has" comment is only true for `application`. Add the vacancy branch or narrow the comment.
2. **Rejected/auto-closed stepper rails lack `md:justify-end`** [blind] — `status_stepper.gleam:210` vs `:321`, `:381`. Previously identical; the pipeline rail now right-aligns on desktop while siblings don't. Align or comment.
3. **`let _ = notifications` in the demo deep-link test** [blind] — `demo_flow_test.gleam:626`. The "marks the row read" contract is pinned only via unread count; assert the row's `is_read` directly or destructure `#(_, unread)`.
4. **Deep-link logic duplicated between real and demo arms** [architecture] — `demo_update.gleam:555` vs `client.gleam:4398`. A neutral helper module would keep the route contract single-sourced.

### Reviewer agreement

The missing vacancy navigation pin was caught independently by **tests** and **acceptance** — highest-confidence finding alongside the edge lens's fabricated-id trace.

**Rejected during verification (false positives):** "silent no-op on unresolved click" and "resolver only consults on-screen leaderboard" — both restate the user-approved graceful-degradation design and are out of scope per the briefing.

### Verdict

**NEEDS CHANGES** — 2 blockers: the fabricated-vacancy-id resolution path (hard-blocker class) and the missing vacancy-side navigation pin.

_Address findings and push — I re-review automatically on the new sha._
