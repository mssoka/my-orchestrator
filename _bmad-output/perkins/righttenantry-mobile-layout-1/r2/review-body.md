## 🤖 Perkins automated review — round 2 of 3

- **Job:** righttenantry-mobile-layout-1
- **Reviewed sha:** `3acbf6ba72268bee91462230d480358f8b86799e`
- **Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests)
- **Verification:** 22/24 lens findings survived code re-verification — 2 discarded as false-positive (one re-litigated the user-approved client-side resolution; one compared the test-count claim against the full-PR diff instead of the round delta)
- **Local suite:** client 637 passed, no failures (GitHub Actions is billing-blocked account-wide; local suite is ground truth)

### Fix audit (round 1 → round 2)

- **B1 (stale-leaderboard fabricated vacancy id):** the tag + guard fix LANDS for the exact r1 repro, with a real regression test (`resolve_application_vacancy_refuses_stale_leaderboard_test`) — but a residual race remains (blocker 2 below).
- **B2 (vacancy navigation pin):** `notification_target_path/3` LANDS and pins both entity types in the real arm — but the demo arm does not route through it (blocker 1 below).
- Both r1 warnings (vacancy_detail pb-28 test, filter-pill shrink-0 test) and all four r1 notes are still present.

### BLOCKERS (2)

1. **Demo click arm bypasses `notification_target_path` — vacancy-typed demo clicks still no-op** *(still present since round 1)* — `client/src/demo/demo_update.gleam:555-582` [edge, acceptance, architecture, codebase, tests, blind]. The round-2 contract requires BOTH arms to route through the shared helper. The demo arm re-implements the application branch inline and has no vacancy branch, so vacancy-typed demo notifications never navigate and the two routing contracts can drift. The helper already prefers the demo store — move it (with `resolve_application_vacancy`) into a neutral module both arms can import, call it from the demo arm, and pin both arms. (Advisory test gate: FAIL.)

2. **Late `ApiReturnedLeaderboard` response re-fabricates a wrong vacancy id (B1 residual race)** — `client/src/client.gleam:2077-2092`, `msg.gleam:203` [edge, acceptance, architecture]. The plain leaderboard response message carries no vacancy id and the handler applies `Success` unconditionally. Sequence: VacancyDetail(A) fetch in flight (tag A) → navigate to VacancyDetail(B) (tag flips to B) → A's response lands → A's entries tagged as B. The resolver guard then passes for route B and an A-application notification resolves to the fabricated B — the exact class B1 was meant to kill, plus the leaderboard visibly shows A's rows on B's page. The refresh handler already guards via `vacancy_detail_request_id`; the plain handler needs the same: carry the vacancy id on `ApiReturnedLeaderboard` (and the page variant) and apply only on match.

### WARNINGS (2)

1. **vacancy_detail `pb-28` compare-bar padding still untested** *(still present since round 1)* — `client/src/pages/vacancy_detail.gleam:106-110` [acceptance, tests]. Only application_detail's padding is pinned; a revert on vacancy_detail goes uncaught.
2. **Filter-pill `shrink-0` (fix 3) still has no test** *(still present since round 1)* — `client/src/components/leaderboard_view.gleam:407` [acceptance, tests].

### NOTES (6)

- Rejected/auto-closed stepper rails still lack `md:justify-end` that the pipeline rail gained *(still present since round 1)* — `status_stepper.gleam:210 vs 321, 381`.
- `demo_flow_test` still binds `notifications` then discards with `let _` — the read-row contract is pinned only via the unread count; the new deep-link test repeats the pattern *(still present since round 1)*.
- `notification_target_path` interpolates an unvalidated vacancy id into the route — low impact (server-generated ids), worth a doc-comment note.
- `leaderboard_vacancy_id` set-sites are not directly pinned — tests construct the tag manually rather than driving the fetch/navigation transitions.
- `vacancy_detail` renders `class=""` when no comparison is active — harmless.
- Demo banner comment says ~32px while the test comment says ~30-32px — trivial drift.

### Reviewer agreement

- Demo-arm bypass / vacancy no-op: **6 of 7 lenses** (edge, acceptance, architecture, codebase, tests, blind).
- `ApiReturnedLeaderboard` race: **3 lenses** (edge, acceptance, architecture).
- Both warnings and the stepper note: 2 lenses each.

### Verdict

**NEEDS CHANGES** — B1's fix lands for the r1 repro but leaves an unguarded response race; B2's helper lands for the real arm but the demo arm never adopted it.

_Address findings and push — I re-review automatically on the new sha._
