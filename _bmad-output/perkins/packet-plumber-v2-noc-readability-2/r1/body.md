## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-noc-readability-2 · **Reviewed sha:** 826f54d · **Reviewers:** 7/7 completed
**Verification:** 23/24 findings confirmed against the code — 1 discarded as false-positive

Mechanical checks run by the reviewer in the detached worktree: `odin test app/render` 70/70 green, `odin test app` 40/40 green; zero remaining `NOC_PANEL_X/Y/H` references; `NOC_LOG_CAP` 256 unchanged; no bare font-size literals in `noc_overlay.odin` (the ladder discipline holds); column math recomputed by hand (84px pitch vs 76px 7-digit width; 120px name clearance vs 97px max shipped name); visible-row math (720−116−10)/24 = 24 ✓. The 48/48 golden harness + e2e OFF frame + 94,320px smoke are Docker-gated and carried as minion-supplied evidence (PR body) — code paths are consistent with those claims. KYLE PASS 5/5 carried as the job's own vision-gate evidence per this round's standing orders.

### Blockers (1)

**B1 — Settings-row NOC dismissal desyncs `play_w`** · `app/main.odin:1144-1147` · [codebase, architecture]
`SETTINGS_ROW_NOC` clears `overlay_on = false` but never calls `view_set_rail` — unlike `effect_overlay` (main.odin:1071-1076). `play_w` stays `win_w−524` with no rail drawn: camera fit, zoom/pan clamps, crisis banner, settings modal, mode label and captions all keep using the shrunk playfield, and D is dead while `noc_enabled=false` — the only recovery is a window resize. Breaks the diff's own documented invariant ("play_w == win_w when the overlay is off"). One-line fix + an app-layer pin test.

### Warnings (7)

**W1 — Bottom-band anchor collision under D** · `app/render/tray.odin:48` + `app/main.odin:1595-1601` · [architecture]
The tray still centers on `win_w` ([384,896] at 1280, 5 chips) while the mode label/nudge re-anchor to `play_w` (anchor 436) — the label text now renders over tray chips 2-3 (pre-PR it anchored at 960, clear of the tray). ~140px of tray also floats on the rail plate, clipping the last content row. One anchor regime for the whole bottom band, please.

**W2 — Armed upgrade-preview card covers the rail's header/DROPS rows** · `app/render/forecast.odin:107-156` + `noc_overlay.odin:337` · [acceptance, edge]
`NOC_CONTENT_Y=116` clears health (74) + forecast (~104 at the shipped 1-row max), but the R4 preview card (variable height, up to ~12 rows → bottom ≈ 400px, drawn after the rail) extends far below it during `preview_active` + D — exactly the crisis moment a player opens the rail. Cap the card, drop the content start, or document the accepted occlusion.

**W3 — `NOC_PANEL_W_SCALE` is a dead constant** · `app/render/noc_overlay.odin:332-333` · [acceptance, architecture, blind — agreement ×3]
`NOC_PANEL_W :: 360 * 14 / 10` — flipping the documented tunable changes nothing; the scale is documentation, not derivation. Hard rule 2's "panel-width scale" is half-honored (value 504 correct). Derive from the scale or add a build-check pin.

**W4 — Harness overlay verbs never re-derive `scale/off_x` after `view_set_rail`** · `harness/overlay.odin:76-79,230` + `harness/goldens.odin:89` · [edge]
`render_setup` computes the camera once (win_w-centered); the verbs flip `play_w` only — the D-on harness captures render the world at the full-window fit extending under the rail, while the code comment claims "the world fits LEFT of the rail". App frame ≠ harness frame (the PR's "world's right edge at x=755" matches the app path, where `camera_update` re-derives). The overlay-pixels diff gate stays valid (both frames share the stale camera).

**W5 — App-layer fit-to-rail wiring unpinned** · `app/main.odin:635,1075,1146` · [tests]
No test asserts `play_w` after the D-toggle, the resize re-apply, or the settings dismissal (the render-layer fit IS pinned by `camera_fit_respects_the_rail`; the lens's "no camera test with the rail on" was corrected against that). B1 shipped exactly on this uncovered path. Pin all three app-layer transitions.

**W6 — `play_w` re-anchoring has zero coverage** · `app/render/settings_panel.odin:55` et al. · [tests]
`settings_panel_rect` (a pure helper, exactly like the tested `crisis_card_width`), the audio caption, and the mode label/nudge anchors are untested — contract-critical now that two anchor regimes coexist (see W1).

**W7 — Column math untested** · `app/render/noc_overlay.odin:686-696` · [tests]
The 18px tabular arithmetic checks out by hand but nothing pins it; a future ladder tweak can silently re-break it. One test: column pitch ≥ 7-digit width at `NOC_SIZE_BODY`, name clearance ≥ longest shipped name.

### Notes (10)

- **N1** The world→rail→HUD draw-order contract is exercised but never asserted anywhere. [tests]
- **N2** Headline drop counters shrink 22→18 (spec-letter compliant — the ruling's ladder puts counters at 18 — but the old headline emphasis is gone and the PR table lists old counters as "14–15px", omitting the 22). Consider a headline rung ≥ title in a future pass. [blind]
- **N3** `font_check` verb still renders the OLD draw order with no fit-to-rail — its font-inspection captures diverge from the app's D-on frame. `harness/font_check.odin:191-201` [acceptance]
- **N4** Generic `View` hardcodes overlay geometry (`view_set_rail` binds `NOC_RAIL_W`). `view.odin:437` [architecture]
- **N5** Rail content-column left edge derived twice (`noc_panel_x` vs `noc_panel_rect().x + NOC_PLATE_PAD` — same value, two sources). [architecture]
- **N6** PR-body precision: "play_w == win_w in the harness" (the overlay verbs set the rail on — the sentence is true only of the golden path); "plate at x=757" vs constant 756; "content first row y=120" vs `NOC_CONTENT_Y` 116. [blind]
- **N7** `NOC_PANEL_MARGIN` comment says "inset from the window edge" — the plate is flush; the content is inset. [blind]
- **N8** `overlay_on` with `stats_valid` false shrinks the playfield with zero rail pixels until the first stepped tick (transient). [edge]
- **N9** Row-density pins are indirect — the visible-row test duplicates the production formula; `noc_panel_rows`/`NOC_ROWS_*` have no direct test. [tests]
- **N10** Advisory test gate: **CONCERNS** (lens input FAIL corrected by verification — render layer well-pinned; app-layer wiring/re-anchoring/columns uncovered).

### Reviewer agreement
- **B1** settings-dismissal `play_w` desync — codebase + architecture (independently confirmed by the reviewer's own read)
- **W2** upgrade-preview occlusion — acceptance + edge
- **W3** dead `NOC_PANEL_W_SCALE` — acceptance + architecture + blind (×3)

**Verdict:** NEEDS CHANGES

One confirmed blocker with a one-line fix, plus a tight cluster of geometry/coverage warnings (W1/W2/W4 share the "which surfaces follow play_w / what clears the rail" root). The ladder, rail geometry, row density, and zero-drift discipline all verified clean — the reflow itself is solid.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
