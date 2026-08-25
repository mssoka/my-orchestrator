## 🤖 Perkins automated review — round 4 of 3

**Job:** righttenantry-mobile-layout-1 · **Reviewed sha:** `98601499c26627490a630bf06591c0978cbcc6ad`
**Reviewers:** 7/7 completed (kimi-coding/k3 lens mega-minions) · **Verification:** 9/9 findings survived code re-verification, 0 discarded
**Client suite (local, CI billing-blocked):** 643 passed, no failures

### Fix audit (r3 → r4)

- **r3 BLOCKER (cold-boot leaderboard drop): FIXED.** Session-restore arm (`client.gleam:1088-1102`) and `enter_demo` (`5920-5928`) both set `leaderboard: Loading` + `leaderboard_vacancy_id: Some(id)` alongside the cold-boot fetch. Set-site audit across all `fetch_leaderboard` call sites: every cold-boot dispatch pairs with the tag. Demo side pinned by `demo_cold_boot_deep_link_tags_leaderboard_test`.
- **r3 W1 (Error arm ignores guard): FIXED.** `ApiReturnedLeaderboard` Error arm now guarded (`client.gleam:2107`), pinned by stale/matching error tests.
- **Notification deep-link contract: holds.** Both entity types navigate + mark read through the shared `notification_nav` helper (real + demo arms); no fabricated vacancy ids; vacancy behavior unchanged.
- Carried r1/r2 items spot-verified: stale-leaderboard regression test, neutral-module routing, demo arm through shared helper — all hold.

### BLOCKERS (0)

None.

### WARNINGS (5)

1. **`ApiReturnedLeaderboardPage` Error arm ignores the vacancy-id guard** — `client.gleam:2164-2167` [blind]. A late page *error* from vacancy A clears `leaderboard_loading_more` on vacancy B. The plain handler's Error arm was fixed in r3; the page handler's wasn't. Minor (spinner stops early; B's response still lands).
2. **Live session-restore cold-boot tag unpinned** — `client.gleam:1088-1102` [tests]. The r3 fix is verified-landed and the demo side is pinned, but no `ApiReturnedSession(Ok)` test asserts the tag on a real `VacancyDetail` boot — the exact class the r3 blocker escaped through.
3. **`ApiReturnedLeaderboardPage` guard untested** — `client.gleam:2130-2168` [tests]. No test references the message; a revert of the guard (or its Error arm) fails nothing.
4. **`vacancy_detail` pb-28 compare-bar padding still untested** — `pages/vacancy_detail.gleam:106-111` *(still present since round 1)*. `application_detail`'s equivalent is now pinned; this one isn't.
5. **Filter pill `shrink-0` still untested** — `components/leaderboard_view.gleam:407` *(still present since round 1)*.

### NOTES (5)

- **[approved-design]** Live application-notification deep link no-ops unless the owning vacancy's leaderboard is on screen — the documented, user-approved client-side resolution trade-off; the click still marks read. Not re-litigated.
- Post-mutation leaderboard refetch (approve / bulk-reject, real + demo) is silently dropped when cold-booted directly onto an application detail page (tag `None`). Self-heals on next vacancy visit; impact limited to sweep-nudge banner freshness.
- `md:justify-end` on the pipeline rail but not the rejected/auto-closed rails *(still present since round 1)*.
- Redundant `Error` fallback arm in `ApiReturnedLeaderboard` (subset of the catch-all below it) — harmless.
- Advisory test gate: **CONCERNS** — new P0 guards landed and bite; pin coverage on the newest guards is thin.

### Reviewer agreement

No multi-source duplicates beyond the carried/notes merges above; 1 lens finding demoted (tests lens's blocker → warning: fix verified-landed, not in the r4 hard-blocker class).

### Verdict

**APPROVED** — the r3 blocker fix landed and bites on both cold-boot paths; no live-product regression. The warnings are test-pinning gaps plus one minor guard residual — worth a fast follow, not merge-blocking.

_Address findings and push — I re-review automatically on the new sha._
