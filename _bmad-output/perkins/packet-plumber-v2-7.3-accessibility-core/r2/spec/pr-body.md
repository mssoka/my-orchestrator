# Story 7.3 — Accessibility core (colorblind palettes, reduced-motion, scaling, captions, settings panel)

Implements GDD E9.1–E9.3 / stories-v2 Story 7.3 — the a11y floor. **Pure View [ODN-1]**: the sim never sees a byte of it. `core/` untouched, no snapshot fields, no LOG_VERSION, no catalog edits.

- **CI: `tools/ci-local.sh` 10/10** (incl. the extended palcheck oracle).
- **Golden proof:** all 35 pre-existing demos byte-identical (T1 + T2 + replay); the 5 new a11y demos' `.log.bin` + every state hash are byte-identical to `juice.dem` — only the demo-name header line differs. a11y is pure presentation, proven not asserted.

## The three colorblind palettes (deutan / protan / tritan)

Simulator-derived (Machado et al. 2009 severity-1.0 matrices, sRGB→linear→matrix→back) by the committed **`tools/derive_a11y_palettes.py`** — the derivation record. Signal pairs re-separated under each deficiency (lightness + the residual discriminable axis; Okabe-Ito-style anchors); shipped as first-class **`data/palette.json` `modes`** tables (partial — absent tokens keep the canon base; the base palette is untouched byte-for-byte). **`harness/palcheck.odin` re-simulates the SHIPPED tables** and enforces pairwise separation under each deficiency — a future token edit that re-collides fails CI, not playtesters (measured min sim-dist: deutan 51.3 / protan 54.7 / tritan 43.0 vs the pinned 40–48 thresholds).

### The state triad (the classic green/amber/red trap) under each mode

| Token | Canon | Deutan | Protan | Tritan |
|---|---|---|---|---|
| state_healthy | `55,214,122` | `0,118,132` (deep teal) | `0,118,132` | `16,138,74` (dark green) |
| state_congested | `242,181,68` | `242,213,120` (pale amber) | `242,213,120` | `240,204,96` |
| state_critical | `232,69,69` | `168,44,24` (dark brick) | `168,44,24` | `168,44,24` |

L-separated (the axis that survives every deficiency) + the residual axis: deutan/protan read teal-vs-brick on blue-yellow; tritan reads green-vs-red on red-green. **All 16 signal/map token pairs verified per mode.**

### Non-color channel inventory (never-color-alone is now TESTABLE [ODN-1])

| State / machine | Non-color channel (pre-existing) | 7.3 addition |
|---|---|---|
| Node congestion (5.2/7.1) | ring glyph `!`/`!!` + pulse-rate (3 encoders) | pulse becomes static under reduced-motion; the ring + glyph + banner carry it |
| Crisis (4.2) | banner card + `!!` glyph + bottleneck OUTLINE shape | outline pulse static under reduced-motion (readability contract) |
| Packet types (3.1) | per-class SHAPE (circle/triangle) primary; catalog `color_rgba` secondary | class colors remapped at DRAW time under a mode (`mode_class_color`) — the catalog is never edited (cat.hash golden-poison) |
| LANES (3.3) | lane speeds (per-mille motion) + stroke position | lane COLORS remapped per mode |
| Ghost ok/bad | grey vs red + the validation state | ghost colors remapped per mode |
| Map tokens (7.4) | water/coast/park | remapped per mode + palcheck pins them (presence + the negative leg) |

## Reduced-motion (E9.2)

The shipped motion inventory is the PULSE16 ring pulse + the crisis-outline swell (both tick-derived). Reduced-motion pins both to a **static full width** (`pulse_read` — the single seam every animated pulse consumer routes through). Crisis readability survives on the already-static channels: the `!!` glyph, the banner card + text, ring presence + color. Packet movement + lane speeds are gameplay readouts and are NOT disabled (GDD E9.2: "disable flash/shake" — no flash/shake exists in v2 to disable beyond the pulse; documented).

**Golden:** `a11y_reduced` pins the crisis moment static — banner + outline + ring all render (vision-verified).

## UI/gauge scaling (E9.3 — user ruling: ×1.00/×1.25/×1.50)

`View.ui_scale` + `hud()/hud_f()` (the scaled-int helpers, single-source with hit-tests) thread through every HUD surface: health card, crisis banner, forecast panel, tray, QoS panel, caption strip, settings panel/chip, run HUD, SLA/pool gauges, assist label, popover, node-health card. At ×1.00 `hud()` returns the constants exactly — the blessed goldens are byte-identical (proven by the suite). **Golden:** `a11y_scale` pins the ×1.50 chrome (vision-verified: HUD visibly larger, world unchanged).

## Captions (E9.3 — completion over the 7.2 seam)

The 7.2 seam (`Caption` + dwell + crisis-priority) already captions every alert; captions stay live while muted (the a11y contract). 7.3 completes the surface: the caption strip scales with the knob and the coverage audit confirms every 7.2 alert kind (crisis stings + arrival clicks) captions. No new alert kinds.

## The settings panel + persistence (user rulings 2026-08-19: PANEL + disk + 3 steps)

- **New modal panel** (`app/render/settings_panel.odin`, popover pattern: layout owned in render, single-source rects, app hit-tests): COLORBLIND PALETTE (off/deutan/protan/tritan cycle), REDUCED MOTION, UI SCALE (100/125/150%), AUDIO (the 7.2 mute surfaced — discoverable a11y). **Pause-on-open** (the a11y-first choice — no surprise un-pause on close; the pause chip shows state). ASCII labels (lint gate 6).
- **Input parity by construction**: new intents (`Toggle_Settings`, `Settings_Navigate`, `Settings_Activate`) mapped across keyboard (S, arrows, Enter, Esc), controller (Y, D-pad, A, B), and touch (chip + row taps via the shared ui-press seam). The panel is MODAL — world inputs are suppressed while open (mouse/touch/pad gated). Parity pinned: the new `input_parity_settings_panel` scenario drives all three devices → identical (empty) command streams + identical end input-state. **25/25 parity scenarios green.**
- **Disk persistence** (`app/settings.odin`): tiny versioned binary (`~/.pp-settings.bin`, magic + version + checksum, defaults on ANY failure — never a crash). App-side only; the first persistent-settings home (later settings land here too).

## Goldens

5 new demos (the juice scene under each mode — `a11y_deutan/protan/tritan/reduced/scale`) + fresh blessed T2 dirs + `.t1`/`.log.bin`, cause-documented. Existing goldens byte-identical. **Before/after evidence (vision-verified):**

- `_bmad-output/planning-artifacts/art-renders/a11y-7.3-deutan-montage.png` — base vs deutan (calm + crisis)
- `_bmad-output/planning-artifacts/art-renders/a11y-7.3-modes-montage.png` — protan/tritan/reduced/×1.50 crisis frames

## Decisions & rationale

- **Palette derivation = simulation + re-separation, not eyeball tuning** — the tables are canon data (committed script + the palcheck oracle keeps them honest). Any future token edit that re-collides fails CI.
- **Reduced-motion pins the pulse to full static width** (max legibility, deterministic + golden-stable), not an average — a constant ring reads better than a frozen mid-pulse.
- **Packet class colors remap at draw time, never in the catalog** — `packet_types.json` bytes fold `cat.hash` (golden-poison); the draw-time remap is presentation-only [ODN-1].
- **The settings panel pauses the game on open** (a11y-first) and stays paused after close (explicit resume — no surprise un-pause). Popover pattern for parity + hit-test single-source.
- **Settings file: versioned binary over JSON** (ODN-11's JSON-int-trap doctrine, consistency with the save canon); HOME-dotfile (launch-cwd independent); gitignored; checksum-guarded.
- **Deliberate non-goals (follow-ups):** settings-panel is the surface (hotkeys ALSO exist as shortcuts); no difficulty options, control remapping, localization, TTS/screen-reader, packet-glyph font pass (the catalog `icon` field stays [LATER]).
- **Model note:** the briefing's `deepseek/deepseek-v4-flash` line is dead (402 — playbook 08-19 ruling); the job + its mega-minion ran on `zai-coding-cn/glm-5.3`.
- **Process note:** the gds-quick-dev step-02 spec ran ~1700 tokens (over the 1600 guidance) — [K]eep, per the story = one PR canon + the shared palette/settings/golden seams.

## Scope guard

The a11y FLOOR only. Sim untouched — the entire change is `app/`, `harness/`, `data/palette.json`, `tools/`, `demos/`, `goldens/`, + docs. No snapshot fields, no LOG_VERSION, no catalog edits (verified: `git diff --stat core/` is empty).

## r1 → r2 rework (Perkins review 4975373360 — 6 blockers, all resolved)

- **B1 (keyboard surface dead):** the phase-1 key collection now gathers S/arrows/Enter (the chain previously died at `case:`). S is collected ONLY with no pipe selected — with a selection S keeps its Standard-lane meaning, and the executor's `sel_pipe` gate makes the two paths mutually exclusive (a same-frame S can never open the panel AND reassign a lane). The parity keyboard leg now bites (row-1 assertion).
- **B2 (touch scale stuck at 150%):** the scale row is now a WRAPPING CYCLE (100→125→150→100) via `cycle_scale` — a touch-only player can always get back; no clamped dead end.
- **B3 (zero settings-persistence coverage):** `app/settings_test.odin` pins the WHOLE contract — round-trip, missing/truncated/foreign-version/bad-magic/bad-checksum/out-of-range → defaults, plus scale_of/step_of and the cycle helpers (12 tests, in gate 2).
- **B4 (×1.50 banner occludes the forecast):** `crisis_card_width` clamps the centered banner to clear the forecast's left edge (10px gutter); the banner text scales proportionally so the title never overflows. Unit-pinned (`hud_test`) + vision-verified on the re-blessed `a11y_scale` golden (banner x370-900, forecast at x910, no overlap, text unclipped).
- **B5 (QoS action-row overlap/mis-hit):** slot 1 (Revert), the preset chips and the nudge rects now scale through hud() like slot 0 — the hit rects can no longer overlap at ×1.25/×1.50 (single source with the draw).
- **B6 (test gate):** the palcheck oracle's NEGATIVE leg ships (`harness/a11y_oracle_test.odin` — a poisoned token pair FAILS the oracle; the clean tables pass — the gate bites); `app/render/hud_test.odin` pins the ×1.0 identity (the golden byte-identity hinge), the ×1.25/×1.50 rounding, the zero-scale guard and the banner clamp; the parity settings scenario asserts the row-1 focus on every device (non-vacuous). All four test binaries run in CI gate 2.

