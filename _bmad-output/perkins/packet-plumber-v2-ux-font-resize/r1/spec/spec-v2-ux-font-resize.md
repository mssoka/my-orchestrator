---
title: 'v2 UX: readable HUD font + resizable window'
type: 'bugfix'
created: '2026-08-15'
status: 'in-progress'
baseline_commit: '87b7374'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** USER REPORT 2026-08-15 (ruling-grade): "the font is hard to read" + "i cant seem to be able to resize the window. prototype could". v2 renders the raylib DEFAULT bitmap font (pixelated/blocky at HUD sizes — verified: title+instructions run half-hidden under the centered Network Health card at 1280×720) and the window is fixed-size (no `FLAG_WINDOW_RESIZABLE`, unlike the prototype).

**Approach:** (1) Bundle a high-legibility OFL font (Open Sans Regular, instanced static) as a repo asset; load via `rl.LoadFontEx` in BOTH the app and the harness (deterministic — rlsw rasterizes the same file); route all HUD text through `rl.DrawTextEx(v.font, …, spacing 1)`. Raise HUD text minimums to ~14px and darken state-colored TEXT for contrast. (2) Restore resize: `SetConfigFlags({.WINDOW_RESIZABLE})` + `SetWindowMinSize` before init (prototype pattern); HUD math moves off `WIN_W/WIN_H` constants onto the live `view.win_w/win_h`; camera-fit already reveals more map (GL5.2 aspect=expand); pause edge-chip becomes gap-adaptive. Resize is presentation-only — never touches sim/serialization/replay; harness captures stay fixed 1280×720.

## Boundaries & Constraints

**Always:**
- Font is a BUNDLED asset (no system-font reads — platform-deterministic). ASCII text only (lint gate 6).
- Resize must never touch sim state, serialization, LOG_VERSION, or the harness capture path (T1 hashes + T2 captures stay 1280×720).
- T1 goldens must NOT shift. T2 goldens shift ONLY from the font/size/contrast fold — deliberate, listed, re-blessed.
- Render determinism: no transcendentals; font atlas from the committed file via the same raylib path in app + harness.
- Full local suite green (`tools/harness.sh run` = 28 demos) + lint gates.

**Ask First:** (none — judgment calls below are delegated by the briefing and documented in the PR's Decisions & rationale)

**Never:** No new HUD surfaces; no visibility/gauge work; no 5.2 health-ring changes; no input-parity work; no system fonts; no render-target letterboxing (adapt layout instead); no LOG_VERSION bump.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Resize to 1600×900 | window event | world re-fits (camera-fit), HUD re-anchors (win_w/win_h), no overlap | view_compute on IsWindowResized (existing) |
| Resize to non-16:9 (1280×800) | window event | taller view, HUD bands stay clear, pause chip adapts to gap | same path |
| Min clamp (1152×648) | user drags smaller | window clamps; top band (health card + forecast) + QoS + pause chip do not overlap | SetWindowMinSize |
| Font file missing at load | LoadFontEx fails | fall back to GetFontDefault (belt+braces; file is committed so unreachable in practice) | IsFontValid check |

</frozen-after-approval>

## Code Map

- `app/main.odin` -- window init (flags + min size), `draw_text` (→ DrawTextEx with the app font), HUD math (WIN_W/WIN_H → view dims), title/instructions copy, pause chip position, temp `--shots` capture code (REVERT before PR)
- `app/render/view.odin` -- `View.font` field, `draw_text_c` (→ DrawTextEx), `load_hud_font()` (render package — shared by app + harness)
- `app/render/palette.odin` -- derived `state_strain_text`/`state_critical_text` (darkened, for TEXT only)
- `app/render/forecast.odin` `health.odin` `crisis.odin` -- state-colored text → text variants; health-chip + banner sizes ≥14px
- `app/qos_panel.odin` -- text sizes ≥14px
- `app/render/tray.odin` + `app/main.odin` draw_tray -- chip label sizes ≥14px
- `harness/goldens.odin` -- `render_setup` loads the font (deterministic capture)
- `assets/fonts/open_sans_regular.ttf` + `assets/fonts/OFL.txt` -- bundled asset + license
- `goldens/**` -- deliberate T2 re-bless (inventory in PR)

## Tasks & Acceptance

**Execution:**
- [ ] `assets/fonts/` -- add Open Sans Regular (OFL 1.1) + OFL.txt -- bundled deterministic asset
- [ ] `app/render/view.odin` -- View.font + load_hud_font() + draw_text_c→DrawTextEx -- one font source
- [ ] `harness/goldens.odin` -- render_setup loads font -- deterministic T2 text
- [ ] `app/main.odin` -- init flags/min-size; draw_text→DrawTextEx; HUD math centralization; title+instructions copy; pause chip gap-adaptive; remove temp --shots/F12 code
- [ ] `app/render/palette.odin` -- text variants for state colors -- contrast
- [ ] `app/render/forecast|health|crisis.odin`, `app/qos_panel.odin`, tray -- sizes ≥14px + text variants
- [ ] `goldens/` -- deliberate T2 re-bless for text-bearing demos; T1 verified unshifted
- [ ] `_pr_body.md` (new file, NOT the tracked one) -- before/after screenshots + font/license + contrast table + resize approach + min clamp + golden inventory + Decisions & rationale

**Acceptance Criteria:**
- Given the app window, when it launches, then HUD text renders in the bundled font with nothing below ~14px at 1280×720 and no top-band overlap (title/instructions clear the health card).
- Given the app window, when the user drags any corner, then the window resizes (world re-fits; HUD re-anchors), and at 1280×720 / ~1600×900 / min clamp 1152×648 / a non-16:9 drag the pause edge-chip + QoS panel + weather report do not overlap.
- Given `tools/harness.sh run`, then all 28 demos pass; T1 hashes byte-identical to pre-change; every re-blessed T2 is listed in the PR body.
- Given the PR, then it carries before/after screenshots (font close-ups at HUD sizes; resize at default/1600×900/min/non-16:9), the font choice + license, the contrast numbers, the min-clamp value, the golden inventory, and a Decisions & rationale section.

## Spec Change Log

## Design Notes

- **Font**: Open Sans (SIL OFL 1.1) instanced to static Regular via fonttools (variable → static, 130KB). Strong x-height + open counters; the prototype's own font story (system TTF candidates) proves TTF-at-64px + DrawTextEx works in both GPU + rlsw. Atlas generation (stb_truetype) is deterministic given the file + same raylib; verified by re-running the harness after re-bless.
- **HUD text sizing**: every draw_text/draw_text_c size < 14 raised to ≥14 at 1280×720 (tray 11→14, pause chip 12/10→14/12, health chips 12→14, crisis redesign 12→14, QoS preset chips 12→14). Debug overlay (PP_DEBUG-only) untouched.
- **Contrast**: ink {51,65,79} on canvas {232,221,194} ≈ 9.9:1 (pass). ink_soft {106,112,120} ≈ 4.1:1 — darkened to ~{96,102,110} (≈5:1) for secondary text. state_strain/state_critical used AS TEXT ≈ 1.7–2.2:1 (fail) — new derived `*_text` variants (≈55% darkened) for text only; telegraph colors unchanged for rings/outlines/shapes.
- **Resize**: `SetConfigFlags({.WINDOW_RESIZABLE})` + `SetWindowMinSize(1152, 648)` before InitWindow (prototype pattern). HUD anchors move to `app.view.win_w/win_h` (single source — view_compute already updates them on IsWindowResized). Min clamp = the narrowest width where the top band fits: health card (460 centered) right edge `W/2+230` < forecast left `W-260` ⇒ W > 980; pause chip needs the gap ⇒ 1152 keeps a ~76px chip slot → adaptive chip (two-line at ≥104px gap, single-line "PAUSED" below).
- **Title/instructions overlap** (pre-existing at 1280): the 22px title + 16px hint extend under the centered card (measured to x≈869 > card left 411). Fix: shorten title to "Packet Plumber - v2" and hints to ≤~45 chars so they clear the card's left edge at min width too.

## Verification

**Commands:**
- `tools/lint.sh` -- expected: "lint: all gates green" (ASCII gate 6 covers the new strings)
- `ODIN_ROOT=/Users/moses/code/packet-plumber/tools/raylib-sw/shadow odin build harness -out:bin/harness -debug && ./bin/harness run` -- expected: 28 demos green; T1 unchanged; T2 fold = only the listed text-bearing demos
- `./bin/harness run` twice after re-bless -- expected: identical (determinism)
- `odin build app` -- expected: compiles; `./app.bin --shots <dir> --shots-resize` captures at 1280×720, 1600×900, 1152×648, 1280×800 (temp code, reverted before PR)
- `git diff --stat` + `git status` -- expected: temp `--shots`/F12 code absent; no accidental commits

**Manual checks (if no CLI):**
- Screenshots: font close-ups at HUD sizes; resize states with pause chip + QoS panel + weather report; verify no overlap by pixel scan (PIL) at default + min + non-16:9.
