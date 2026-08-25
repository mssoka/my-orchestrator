# v2 UX: readable HUD font (bundled Open Sans) + resizable window — fixes USER REPORT 2026-08-15

Fixes the two user-reported defects (ruling-grade): *"the font is hard to read"* and *"i cant seem to be able to resize the window. prototype could"*.

- **Font:** v2 rendered the raylib **DEFAULT bitmap font** — pixelated/stair-stepped at every HUD size on the light canvas (verified in captures). Replaced with a **bundled Open Sans Regular** (SIL OFL 1.1), loaded via `rl.LoadFontEx` by BOTH the app and the harness (same committed file → same atlas → T2 captures stay bit-exact on every platform).
- **Window:** the prototype's `SetConfigFlags({.WINDOW_RESIZABLE})` was missing in v2. Restored + a **minimum clamp of 1152×648** so the HUD can't collapse. Resize is **presentation-only**: the sim, serialization, replay, and the harness capture path are untouched (no LOG_VERSION change; T1 hashes byte-identical).

## Before / after — the font

Side-by-side 3× close-ups (left = raylib default, right = Open Sans):

| Surface | Before / after |
|---|---|
| Title + run hints (top-left) | ![title](docs/captures/v2-ux-font-resize/font_closeup_title.png) |
| Hardware tray chips (11px → 14px) | ![tray](docs/captures/v2-ux-font-resize/font_closeup_tray.png) |
| SLA gauges (bottom-left) | ![sla](docs/captures/v2-ux-font-resize/font_closeup_sla.png) |

Full frames: ![before](docs/captures/v2-ux-font-resize/before_run_1280.png) → ![after](docs/captures/v2-ux-font-resize/after_run_1280.png)

## Window resize

| Size | Capture |
|---|---|
| Default 1280×720 (paused: chip + weather + QoS + banner) | ![1280](docs/captures/v2-ux-font-resize/after_paused_1280.png) |
| ~1600×900 | ![1600x900](docs/captures/v2-ux-font-resize/after_resize_1600x900.png) |
| Min clamp 1152×648 | ![min](docs/captures/v2-ux-font-resize/after_resize_min_1152x648.png) |
| Non-16:9 drag 1280×800 | ![1280x800](docs/captures/v2-ux-font-resize/after_resize_1280x800.png) |

**Resize approach — adapt layout (camera-fit), not letterbox:** the view already re-fits on `IsWindowResized` (GL5.2 `aspect=expand` doctrine — wider/taller windows reveal more map). What was broken: the app-layer HUD anchored to the `WIN_W`/`WIN_H` **constants**, so after a resize the mode label + SLA gauges floated mid-screen. All HUD anchors now read the live `view.win_w`/`view.win_h` (single source — updated by `view_compute`).

**Min clamp: 1152×648** — the narrowest width where the top band fits without overlap: the health card (460px centered, right edge `W/2+230`) must clear the forecast panel (left edge `W−260`) ⇒ W > 980; the pause chip needs the gap too. At the clamp the gap is ~76px.

**Pause edge-chip (5.3-ux) survives resize:** the chip is now gap-adaptive — two lines when the gap ≥ 104px, a single 14px "PAUSED" line when tighter; it never overlaps the health card or the weather report (seam-verified at 1280, 1600, 1152, 1280×800).

## Size + contrast audit (light-canvas palette)

**Size minimums:** every player-facing HUD text raised to ≥14px effective at 1280×720 — tray chips 11→14, health-meter chips 12→14, crisis redesign 12→14, QoS preset chips/buttons 12/13→14, pause chip 12/10→14/12 (the hint stays 12 — a 14px hint's descenders would clip the 38px chip from the 5.3 ruling). The PP_DEBUG dev overlay (D key) keeps its 12–13px sizes — dev tool, not player-facing.

**Contrast (WCAG relative-luminance, on canvas {232,221,194}):**

| Color | Used for | Ratio | Verdict |
|---|---|---|---|
| ink {51,65,79} | primary text | 7.7:1 | AAA |
| ink_soft {106,112,120} → **{92,98,106}** | secondary text | 3.7 → 4.6:1 | AA |
| state_strain {242,181,68} as TEXT | → **strain_text** {121,90,34} | 1.4 → 4.7:1 | AA |
| state_critical {232,69,69} as TEXT | → **critical_text** {116,34,34} | 2.9 → 7.8:1 | AAA |
| state_healthy {55,214,122} as TEXT | → **healthy_text** {27,107,61} | 1.7 → 5.8:1 | AA |
| win toast {50,160,80} | → {44,134,66} (30px large) | 2.5 → 3.4:1 | AA-large |
| reject/lose red {200,60,60} | → {184,52,52} | 3.7 → 4.4:1 | ≈AA (alarm) |

The telegraph state colors themselves are **unchanged** for rings/outlines/shapes (the never-color-alone canon carries them with glyphs); only TEXT draws use the darkened `*_text` variants (derived in `palette.odin`, no data churn).

## Layout fixes (overlaps exposed by the resize work)

- The 58-char title + 88-char hint ran **half-hidden under the centered health card** at 1280×720 (pre-existing). Shortened to "Packet Plumber - v2" + compact hints that clear the card's left edge at the min clamp too.
- The strain-legend line overlapped the crisis banner during active crises (pre-existing). Now gated on no-active-crisis — the banner + rings carry the telegraph while a crisis runs.
- The game-over toast overlapped the meter card at the min clamp; moved below the card band (y 68+ / hint 104+).
- Health card 52→54px tall (seats the 14px chips).

## Golden inventory — the deliberate T2 fold

The font swap + size/color changes are an **intended visual change**: 24 T2 PNGs re-blessed across 9 demos (every text-bearing capture: forecast/weather panels, health meter, crisis banner, health-ring glyphs). **T1 state-hash goldens + replay logs are byte-identical** (font is presentation-only — verified: zero `.t1`/`.log.bin` diffs). The harness captures stay fixed 1280×720 (render_setup unchanged) — resize code cannot shift them.

Updated: `goldens/forecast_preview/{30000,31000,32000,33000}ms.png` · `goldens/growth/{15000,45000,88000}ms.png` · `goldens/health_lose/{05000,21000,23000}ms.png` · `goldens/health_win/{30000,75000,150500}ms.png` · `goldens/lose/03000ms.png` · `goldens/pause/{65000,80000}ms.png` · `goldens/qos/65000ms.png` · `goldens/surge/{30000,65000,119500,149000}ms.png` · `goldens/warn/{01500,45000,65000}ms.png`

Full local suite green: `tools/harness.sh run` = **28/28 demos** (run twice — deterministic), `tools/lint.sh` all gates green.

## Decisions & rationale

- **Font = Open Sans (OFL 1.1)** — instanced to a static Regular via fonttools from the Google Fonts variable file (130KB, committed at `assets/fonts/open_sans_regular.ttf` + `OFL.txt`). Chosen for unambiguous license + strong x-height + open counters (screen-legibility design); bundled (no system-font reads) so the harness atlas is platform-deterministic. Rejected: system TTFs (the prototype's placeholder doctrine — non-deterministic across machines), variable font (static instance removes axis ambiguity).
- **No letterboxing** — the project canon (GL5.2 aspect=expand) already reveals more map on resize; letterbox would contradict it.
- **Min clamp 1152×648** — documented math above; a smaller clamp would force HUD overlap.
- **Pause hint stays 12px** — a 14px second line's descenders clip the 38px chip (5.3 ruling's height); the "PAUSED" line is the primary read at 14px.
- **Debug overlay sizes unchanged** — PP_DEBUG-only dev tool.
- **Synthetic crisis-state captures** — the resize screenshots inject a forecast row + active crisis (paused — the sim never steps) to exercise the weather report + banner together at every size; this is the acceptance's worst case.
- **No new HUD surfaces, no visibility/gauge work, no 5.2 health-ring changes, no input-parity work** — scope guard respected.
