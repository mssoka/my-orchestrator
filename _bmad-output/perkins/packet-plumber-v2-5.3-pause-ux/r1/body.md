## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-5.3-pause-ux · **Reviewed sha:** `57eeda7` · **Reviewers:** 7/7 completed
**Verification:** 12/13 findings confirmed against the code — 1 discarded as false-positive

**Scope & guards checked first:** the diff touches `app/main.odin` presentation + 3 canon lines + the PR body only — no `core/`, no `harness/`, no `data/`, no goldens. The stepping gate, paused bundle-view refresh, glow/preview surface, and demolish-popover liveness are untouched (verified by diff + re-read, not by claim). Locally re-verified at the sha: **158 core tests pass, 25/25 demos goldens byte-identical (no re-bless), lint all gates, `odin build app` clean.** Canon lines (GDD §UI&Navigation + art-direction §8.1 + story 5.3 card) match the code: full-brightness world, edge chip, tray-chip styling byte-identical to `draw_tray`'s idiom.

### Blockers (0)

None.

### Warnings (3)

1. **Pause chip overlaps the forecast panel whenever window width < 1220px** — `app/main.odin:260` [blind, edge]
   Chip right edge `win_w/2+360` collides with the forecast card's left edge `win_w−250` below 1220px. The window is freely resizable (`IsWindowResized` handler at :205, no min-size clamp), and at sub-1220 the panel (drawn later in `draw_hud`) paints over the chip — during a crisis pause, exactly the pause-and-plan moment. Default 1280 is collision-free (verified: health backdrop ends `win_w/2+230`, chip starts `+240`, forecast starts `−250`).
   *Fix:* clamp `chip.x = min(win_w/2+240, win_w−250−124)`.

2. **Paused presentation change has zero automated coverage; achievable headless geometry pin skipped** — `app/main.odin:253-264` [blind, tests]
   The chip geometry is bespoke and untested — an off-screen or overlapping chip passes the green suite (warning #1 is exactly such a bug no test caught). Pause *behavior* is well covered (`core/pause_test.odin`, `pause.dem` T1/T2 — all re-verified green); the PR's argument that the harness cannot capture the app overlay without shifting every T2 golden is correct. A pure-proc geometry unit test is still achievable outside the harness.
   *Fix:* extract the chip rect into a pure proc; unit-test non-overlap vs health card + forecast panel across `win_w` values.

3. **Advisory test gate: CONCERNS** [tests] — P0 pause-determinism fully covered; the only gap is the presentation-layer geometry (warning #2's pin raises it to PASS).

### Notes (6)

1. **Three "under the veil" comments survive the veil's removal** — `app/main.odin:193,220,238` [architecture, codebase]. Stale wording; reword to "while paused".
2. **Third copy of the tray-chip bg literal** `{238,230,210,255}` — `app/main.odin:261` vs `draw_tray` at `:1283,:1297` [codebase]. Style is consistent (byte-identical); hoist a shared constant.
3. **Chip x hand-derives private card constants** (health `card_w=440+pad`, forecast `card_w=230+pad`) with no single source — `app/main.odin:260` [architecture]. Changing either card silently breaks the gap math; export the extents or a `top_band_gap()` helper.
4. **Chip drawn inline in main()'s loop** while all other persistent HUD chrome lives in `draw_hud`/render — `app/main.odin:251-265` [architecture]. Inherited from the old overlay's slot; consider moving into `draw_hud`.
5. **Opaque chip can cover the demolish popover's button** in a narrow top-of-screen geometry — popover clamps `y≥8`; a pipe popover at `y∈[8,22)` with x in the chip band puts its bottom button partly under the chip (drawn after) — `app/main.odin:236-241` vs `:251-265` [edge]. Visual only (the chip has no hit region; the button still works). Drawing the chip before the popover fixes it.
6. **"Edits stay live while paused" affordance hint deleted** with no replacement — the new chip says only "P/Space to resume" [blind]. The always-on HUD hint still teaches controls. Recorded for the product ledger, not a request to restore center text.

### Reviewer agreement
- Chip/forecast overlap below 1220px — **blind + edge** (independently derived geometry)
- Zero coverage of chip geometry — **blind + tests**
- Stale "under the veil" comments — **architecture + codebase**

**Verdict:** READY TO MERGE

All findings are advisory: the user-report fix itself (no dim, no center text, edge chip, canon agreement, golden-safety) is correct and fully verified at the reviewed sha. Warnings 1–2 are worth a follow-up commit, not a rework.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
