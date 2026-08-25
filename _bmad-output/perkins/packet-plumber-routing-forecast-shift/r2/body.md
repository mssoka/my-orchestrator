## 🤖 Perkins automated review — round 2 of 3
**Job:** packet-plumber-routing-forecast-shift · **Reviewed sha:** d930de8 · **Reviewers:** 7/7 completed
**Verification:** 19/22 findings survived code re-verification (11 unique after dedup) — 3 discarded as false-positive

### Fix-audit (r1 findings → d930de8): 11/11 fixed

- **B1 (r1 blocker) — FIXED and proven to BITE.** `forecast_summarize` + `preview_next_tier` are pure core procs with `@(test)` pins; the new `forecast_preview.dem` harness golden renders a NON-nil `Upgrade_Preview` through the app's real `draw_forecast_panel`/`draw_upgrade_preview`. Non-vacuity proven empirically at the sha: an unpatched `harness save` reproduces the blessed goldens byte-identically, and a nil-forced mutation changes all 4 capture PNGs — the card's pixels are genuinely pinned, so a card regression turns the harness red.
- **W1** pair-honest attract (`pipe_other`) + `test_forecast_attract_non_representative_parallel` ✓ · **W2** labels now say "routes" ✓ · **W3** scratch sized by `len(pipe_tier)`, seam asserts the length match ✓ · **W4** aggregation pure+pinned + dense/empty card goldens ✓ (narrow residual below) · **N1** seam assert ✓ · **N2** shared `draw_panel_card` ✓ · **N3** commit-leg descope documented in the PR body ✓ · **N4** `disarm_preview` frees on all six disarm paths ✓ · **N5** attract-on-split/`old_pipe`/same-cost-different-tier pins ✓ · **N6** card height exact ✓.
- **r1 guards HELD:** helper pure; honest-prediction pin intact; wiring real; LOG_VERSION 3; existing goldens unshifted.
- **Local verification (CI billing-blocked — ground truth at the sha):** `odin test core` **135/135** · harness **18/18** demos green · drift-check **125/125** rejected · lint all gates green · app builds.

### Blockers (0)

### Warnings (2)

1. **App-side preview lifecycle (update_preview / disarm_preview / U-key) has zero automated coverage** [tests] — `app/main.odin:564-597`. B1's terms are met (render + aggregation + next-tier decision pinned and biting), but `update_preview`'s own logic — gen-freshness memoization, the five disarm conditions, buffer ownership — runs only in the untested app; the harness reimplements arming and bypasses `app/main.odin`, so a stale-preview or leak regression there would pass CI. **Fix:** extract the should-recompute/should-disarm decision into a pure core proc with `@(test)` pins, leaving app code a thin call.
2. **Advisory test gate: CONCERNS** [tests] — improved from FAIL (r1). P0 100% (helper, purity, determinism, honest-prediction pin, golden discipline). P1 ~85-90%: the remaining gap is the app-side lifecycle seam (warning 1).

### Notes (9)

1. **unknown at-verb hint omits "preview"; preview error paths have no negative demo** [acceptance, architecture, codebase, tests, blind] — `harness/demo.odin:361`. Add `|preview` to the want-list; optionally a negative demo (dead pipe / illegal tier).
2. **forecast_preview.dem header mislabels capture times, weather state, and a merge target** [acceptance, codebase, blind] — `demos/forecast_preview.dem:19-29`. Header says 1300ms (captures are 30000-33000ms), claims "weather shows NOW" at 31000ms (surge starts tick 1200, run ends 670 — only countdown), and labels the merge target "node 1" where the blessed text names node 5.
3. **forecast.odin comments still claim "the harness never builds" an Upgrade_Preview** [codebase] — `app/render/forecast.odin:18-19, 33-34` — stale after the B1 fix.
4. **harness save mode swallows preview-capture failures** [edge, architecture] — `harness/run.odin:313-317`. A failed preview directive skips the capture golden yet save returns true; the next `run` catches the missing golden, so it's bless-then-catch, not silent forever.
5. **Preview directives out of time order arm the wrong preview** [edge] — `harness/run.odin:131` — last-in-list wins, not latest-in-time.
6. **preview verb truncates u64 pipe ids to u32 unchecked** [security] — `harness/demo.odin:355-359` — extends the pre-existing draw/spawn pattern.
7. **Two full Dijkstra rebuilds run inside the render pass** [architecture] — `app/main.odin:643` — memoized per (gen, pipe, tier); consider recompute at edit moments or note the scale budget.
8. **Singular-verb and overflow-tail render branches pixel-unpinned** (W4 residual, narrowed) [tests] — `app/render/forecast.odin:199` — all four goldens render count==2 rows with overflow 0; the counting IS pinned in core, only the pixel text branches remain.
9. **Empty-weather (rows==0) preview layout branch never captured** [tests] — `app/render/forecast.odin:100-103` — all captures fall inside the surge forecast window.

### Reviewer agreement

- unknown at-verb hint omits "preview" [5 sources]
- forecast_preview.dem header mislabels captures/weather/merge target [3 sources]
- harness save swallows preview-capture failures [2 sources]

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
