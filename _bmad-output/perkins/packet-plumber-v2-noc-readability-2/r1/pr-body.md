# NOC dashboard readability — round 2: the 20/18/15 ladder + the full-height right rail

The 2026-08-23 user verdict (THIRD STRIKE): "still so hard to read — bigger fonts please" + the DOCK-RIGHT ruling. KYLE's live-screen assessment: **1.5–2× needed** — the old ladder's labels (12px) sat BELOW the game's own 14px floor (the 2026-08-15 font-resize minimum). This PR fixes it properly: a new tunable ladder, a full-height docked rail, and re-computed column math for the 18px numerals.

## The new ladder (the tunable triplet — every panel size is ONE of these constants)

| Rung | Constant | Size | Old | Δ |
|---|---|---|---|---|
| Header / title | `NOC_SIZE_TITLE` | **20px** | 14px | +43% |
| Body / counters | `NOC_SIZE_BODY` | **18px** | 14–15px | +29% |
| Labels | `NOC_SIZE_LABEL` | **15px** | 12–13px | +25% (at-or-above the 14px floor — the exact failure the user called out) |

Panel width: `NOC_PANEL_W` = **504** (= 360 × `NOC_PANEL_W_SCALE` 1.4 — the panel-width scale ruling), `NOC_ROW_H` = 24 (seats the 18px body). All named constants in `app/render/noc_overlay.odin` — no magic numbers (hard rule 2).

## The DOCK-RIGHT resolution (fit-to-rail, documented)

The ruling delegated the choice: **fit-to-rail** (the camera fit math respects the rail) — the camera math is clean (one derivation, `camera_fit`), so the world always stays fully visible:

- The panel is a **full-height rail docked at the far right** (`noc_panel_rect`: x = win_w − NOC_RAIL_W, y 0..win_h; NOC_RAIL_W = 524). NOC-wall style.
- **`View.play_w`** — the playfield width: `win_w` when D is up, `win_w − NOC_RAIL_W` while D is on (`view_set_rail`). `camera_fit`/`camera_update`/zoom/pan/pullback all read it — the world fits LEFT of the rail. play_w == win_w when the overlay is off, so **every non-D path is byte-identical** (zero golden drift, proven below).
- **The rail never covers the top-band HUD cards**: the draw order flips to world → rail → HUD — the health card, forecast panel, pause chip and crisis banner paint OVER the plate; the rail's own content starts below the top band (`NOC_CONTENT_Y` = 116 — the health card bottom 74, forecast ~104). The crisis banner + settings modal + mode label + audio caption re-anchor to `play_w` (they stay inside the playfield, never under the rail).
- The wheel policy: the rail's whole plate owns the wheel (log scrolls there; map zooms elsewhere) — the pinned `camera_wheel_policy` decision, now rect-based.

## Row density (the ruling: fewer visible rows at bigger text is CORRECT)

Ring buffer stays 256 (`NOC_LOG_CAP`). Visible rows: 24 at 1280×720 (was 37) — the wheel scroll handles the rest. Per-section caps are named constants shared by the measure + draw (8 classes / 6 queues / 6 pipes / 6 events / 10 log) — the row-for-row agreement the scroll clamp needs.

## Column math (recomputed for 18px tabular numerals)

The per-class ledger is a right-anchored block filling the 504px rail: name left; del/drop/loss/rate right-aligned at FIXED right edges (18px Plex Mono digit ≈ 10.8px → 7-digit counters get 76px + breathing per column). Right-aligned tabular figures, zebra drop log, dark plate — all kept per the 08-22 readability ruling.

## Verification

- **KYLE (glm-4.6v) legibility verdict on a live capture: PASS** — graded the real-run capture (D pressed in a real windowed play): labels readable ✓, numbers steady ✓, hierarchy clear ✓, docked right full-height ✓, top-band HUD visible ✓. Also PASS on the deterministic surge capture (headline counters, per-class table, queue bars). Before/after captures below.
- **Zero golden drift: 48/48 harness green** — T1 hashes + T2 software pixels + replay gate byte-identical (the rail is runtime-gated; the capture path never presses D; play_w == win_w in the harness). The overlay `.t1` sidecars byte-match the blessed goldens (AC3: overlay is stream-neutral).
- **Local CI: 13/13 gates green** (incl. the PP_DEBUG overlay smoke — 94,320 changed pixels inside the rail rect, the W5 wiring proof — + the drift-rejection negative test, input parity, stats replay).
- e2e OFF frame: zero rail pixels (no D → no panel). Fit-to-rail mechanically verified: world's right edge at x=755, plate at x=757, content first row at y=120.

## Captures

| | Before | After |
|---|---|---|
| Real run (D on) | [before-old-panel.png](docs/captures/v2-noc-readability-2/before-old-panel.png) | [after-rail-real-run.png](docs/captures/v2-noc-readability-2/after-rail-real-run.png) |
| Congested (qos_contention) | — | [after-rail-qos-contention.png](docs/captures/v2-noc-readability-2/after-rail-qos-contention.png) |
| Estate surge (90s) | — | [after-rail-estate-surge.png](docs/captures/v2-noc-readability-2/after-rail-estate-surge.png) |

## Decisions & rationale

- **Fit-to-rail over rail-overlays** — the ruling's preferred branch; the camera math is a single derivation (camera_fit) so threading play_w through it is clean; the whole map stays visible while D is on (an ops dashboard that hides part of the network would fail its purpose). Documented here as the ruling required.
- **Top band over the plate, not re-anchored** — the top band cards (health 460 + forecast 250 + title ~180 = ~890px) geometrically cannot fit in the shrunken playfield (756px at 1280), so they keep their win_w anchors and paint over the plate; the rail content starts below them. This is the literal reading of "the rail NEVER covers the HUD chips' top band".
- **24px rows / 24 visible rows** — the 18px body needs breathing; fewer visible rows is the ruling's explicit call; the wheel scrolls.
- **The 15px label rung** — KYLE's 1.5× band on labels is 18px; the ladder's label rung is the ruling's exact 15px, at-or-above the 14px floor (the user's stated minimum). Hierarchy is preserved by the 20/18/15 step + color + small-caps.
- **`NOC_PANEL_W` = 504 via int math** (`360 * 14 / 10`) — the float const `360 * 1.4` truncates to 503 in Odin const arithmetic; the scale constant is documented alongside.
- **bmad-build waiver (canon note, Silas ruling 2026-08-21 06:10Z)**: the skill's renderer fails on this install (`ambiguous config token implementation_artifacts` — modules.bmm + modules.gds both define it; no in-repo fix exists). Sanctioned path: self-contained briefing (the dispatch's briefing is the spec) + this waiver carried in the PR body.

