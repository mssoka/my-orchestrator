## 🤖 Perkins automated review — round 3 of 3

**Job:** righttenantry-mobile-layout-1 · **Reviewed sha:** `0f94e043a50851ecbd9bb82d1ec752f75823338f`
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests) — no failed layers
**Verification:** 33/34 findings survived code re-verification against the reviewed worktree — 1 discarded as false-positive. Local client suite re-run in the reviewed worktree: **640 passed, no failures** (GitHub Actions remains billing-blocked; local suite is ground truth).

### Fix audit (r2 blockers)

- **B1 (demo arm bypass) — FIXED.** `notification_target_path` + `resolve_application_vacancy` moved to the neutral `client/src/helpers/notification_nav.gleam`; both arms import it (real arm `client.gleam:4415`, demo arm `demo_update.gleam:567`); no orphan copies; vacancy-typed demo clicks now navigate; helper pinned in both modes.
- **B2 (late leaderboard response) — FIX LANDED BUT REGRESSED COLD BOOT.** The messages now carry the vacancy id and guard on `leaderboard_vacancy_id` with a real negative regression test — **but the guard's set-sites missed the two cold-boot fetch paths** (blocker 1), and the Error arm bypasses the guard (warning 1).

### BLOCKERS (1)

1. **Cold-boot deep link to VacancyDetail/VacancyHandoff silently drops the leaderboard response** [edge, architecture] — `client/src/client.gleam:1046-1090` (session restore) and `5839-5934` (enter_demo / demo_entry_effects) dispatch `fetch_leaderboard(id, ApiReturnedLeaderboard(id, …))` but never set `leaderboard_vacancy_id` (initial `None`, `model.gleam:644`). `modem.init` does not dispatch at boot (per the init comments), so `handle_browser_change` — the only boot-reachable set-site — never fires. The new guard at `2081-2112` then compares against `None` and drops the legitimate response: **refreshing the browser on `/vacancies/<id>` (or deep-linking into a demo vacancy) leaves the leaderboard stuck at NotAsked forever.** Live-product regression introduced by the B2 fix. *Fix:* set `leaderboard_vacancy_id: Some(id)` (and `leaderboard: Loading`) in both cold-boot model updates alongside the fetch.

### WARNINGS (3)

1. **`ApiReturnedLeaderboard` Error arm ignores the vacancy-id guard** [blind, edge, acceptance, architecture, codebase] — `client.gleam:2101-2111`: `Error(err), _ ->` flips the current board to `Failure` regardless of tag, so a late error from vacancy A clobbers vacancy B's board. Guard it like the Ok arm (the refresh handler already drops late errors).
2. **vacancy_detail pb-28 compare-bar padding still untested** *(still present since round 1)* [edge, acceptance, architecture, codebase, tests] — only application_detail's pb-28 is pinned.
3. **Filter pill shrink-0 (fix 3) still has no test** *(still present since round 1)* [edge, acceptance, architecture, codebase, tests] — only the stepper's shrink-0 is pinned.

### NOTES (9)

- Demo-arm navigation not revert-pinned (`modem.push` opaque — acceptable test-boundary limitation; the arm's helper call is code-verified).
- Rejected/auto-closed stepper rails still lack `md:justify-end` *(since r1)*.
- `let _ = notifications` discard in demo tests *(since r1, repeated in new test)*.
- `leaderboard_vacancy_id` set-sites not update-level pinned *(since r1 — prescient: the missed set-sites are this round's blocker)*.
- vacancy_detail empty `class("")` when not comparing *(since r1, harmless)*.
- Demo banner comment drift (~32px vs ~30-32px) *(since r1)*.
- Unvalidated `entity_id` interpolated into route path *(since r2, no change required)*.
- Redundant `leaderboard_vacancy_id` re-set in the guarded success arm (harmless).
- Demo test comment describes the r2 arm, not the arm this diff removed (trivial).
- Advisory test gate: **PASS** (P0 pins landed and bite).

### Reviewer agreement

- Late leaderboard Error response bypasses the vacancy guard (5 sources).
- vacancy_detail pb-28 untested (5 sources); filter-pill shrink-0 untested (5 sources).
- Cold-boot fetch paths never set `leaderboard_vacancy_id` (2 sources, Perkins-verified against init/boot flow).

### Verdict: NEEDS CHANGES

One blocker: the B2 guard regresses cold boot on vacancy detail — a refresh of `/vacancies/<id>` never loads the leaderboard. One-line-per-site fix (set the tag at the two cold-boot fetch dispatch sites), plus the Error-arm guard.

_Address findings and push — I re-review automatically on the new sha._
