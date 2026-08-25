## 🤖 Perkins automated review — round 3 (loop-until-APPROVED)
**Job:** packet-plumber-v2-7.3-accessibility-core · **Reviewed sha:** `70e3e91` · **Reviewers:** 14/14 completed (2 chunks × 7 lenses)
**Verification:** 59/61 reviewer findings survived code re-verification — 2 discarded as false-positive; consolidated to 45 unique (4 blockers / 19 warnings / 22 notes). Plus a mechanical battery: palcheck, 27/27 parity, 4 test binaries, golden identity r2→r3, derivation-script re-run.

### Fix audit — the four r2 blockers

- **B1 (delta-0 no-op): FIXED.** `adjust_step` (0→+1) sits at the adjust site; wiring traced for every device (touch tap → `on_ui_press` → `settings_click` → adjust; Enter/pad A → `Settings_Activate` → exec → adjust); pinned by `settings_adjust_step_normalizes` + composed cycle tests. Residual: the click-site call itself has no automated pin — see blocker 4.
- **B2 (QoS editor geometry): FIXED.** The weight draw now derives label/value positions from the same scaled rects as the hit-tests (value centered between −/+ at every step — verified geometrically at ×1.25/×1.50). No automated pin yet (W-tier).
- **B3 (linear_to_srgb): FIXED in both copies.** Correct inverse (×12.92 below linear 0.0031308; `1.055·c^(1/2.4)−0.055` above) in the script AND the oracle; palcheck re-measures in the corrected space and stays green with the pinned min distances (51.3/54.7/43.0); the poison pair still FAILS the oracle (bite verified); the script re-run reproduces all pairs passing.
- **B4 (test gate): scenarios LANDED and bite** (modal-blocks-world + S-ownership, 27/27 green — re-run). **But the gate itself is now red at this sha** — see blocker 1.

### Blockers (4)

**1. `ci-local` gate 2 is RED at the reviewed sha — the settings tests race on a shared temp path under Odin's parallel `@(test)` runner.** `app/settings_test.odin:15-23`: `settings_test_seq += 1` is a non-atomic package global; concurrent tests collide on one path (run logs show 5 tests on `test-8` in one run, `test-5`/`test-7` in another). **`odin test app` failed 10/10 full runs locally** (`settings_truncated_defaults`, `settings_motion_out_of_range_defaults`); the two pass 5/5 in isolation. The r3 push's 13th test moved the parallel schedule into permanent collision. The PR's "10/10" claim is false at this sha — the merge ground-truth gate is broken. *Fix: unique paths without shared mutable state (or single-thread the suite), plus a repeat-run leg in gate 2.*

**2. UI-swallowed left presses fall through to the world path (regression vs base `v2`).** `app/input/mouse.odin:273-282`: base v2 gated the whole world path with `if ui {…} else {tray…node…Begin_Draw}`; the 7.3 rework split it — only `panel_open` suppresses now. A press swallowed by the **QoS panel, crisis banner, SLA rows, or demolish popover** (`ui=true`, panel closed) still runs the tray hit-tests (`Select_Tier`/`Arm_Placement`) and the node snap → **`Begin_Draw`** — a click on the QoS panel over a node starts a pipe drag. The comment right there still claims "a panel click never deselects, never starts a drag". *Fix: restore the `ui` gate over the world path.*

**3. The SLA/pool gauge block never scaled — the PR's own claim ("thread through every HUD surface: … SLA/pool gauges") is false, and the AC "chrome stays legible at each step" is violated.** `app/main.odin:1396-1404` (row pitch raw 16px, hit rect raw 740×18) + `:1537` vs `app/render/visibility.odin:72-96` (`draw_pool_gauge` at raw `win_h−118`, `draw_text_c` never hud-scales). At **×1.25** the scaled SLA header (`win_h−hud(96)`, hud(16)=20px) renders **on top of the POOL gauge label**; at **×1.50** the hud(16)=24px rows self-overlap on the 16px pitch and the 18px rects miss their own text. Carried as a warning since r1 — escalated now on the new ×1.25 collision + the false PR claim. *Fix: hud() the pool call site, row pitch, anchors, and `sla_row_rect`.*

**4. Advisory test gate: FAIL (P0 coverage).** (a) `settings_click → effect_settings_adjust` has **zero automated coverage** — deleting the adjust call passes CI today (the parity twin re-implements the hit-test and models no adjust: exactly the hole the r2 delta-0 no-op shipped through); (b) `app/audio`'s 7 tests (the caption seam) run in **no CI gate**; (c) startup application of persisted settings + pause-on-open unpinned; (d) the QoS scaled geometry (this round's B2 fix) has no pin. *Fix: drive the click-site in a test, add `odin test app/audio` to gate 2 + the workflow, one startup/pause assert.*

### Warnings (19)

1. **`.pyc` committed** — `tools/__pycache__/derive_a11y_palettes.cpython-313.pyc` tracked (added in this push); un-gitignored. [7 lenses]
2. **Invisible chip hit-target at Game_Over** *(corrected from a rejected blocker)* — the chip/panel are never drawn at Game_Over (`draw_hud` early-returns) but `on_ui_press` isn't mode-gated: a mouse/touch click on the invisible chip opens an invisible modal that routes pad A to a settings adjust (persists to disk, no visual). Keyboard is safe (R/Enter → Retry before settings keys); B closes it blind.
3. **ci.yml mirror drift** — gate 2 runs 4 binaries locally, the workflow still `odin test core` (r2-W5, carried).
4. **S dead as panel-close while a pipe is selected** — footer "S / tap chip to close" false in that state (r2-W3, carried).
5. **Settings hit-test in 3 hand-synced copies**; parity twin models no adjust (r2-W4, carried — feeds blocker 4).
6. **Derivation-script docstring claims a numeric search that doesn't exist** — the tables are hand-set constants verified by simulation; the "derivation record" overstates its method (simulate+verify half is real — re-ran, all pairs pass).
7. **`hud_zero_scale…` test vacuous** — re-implements the guard inline, never calls `view_compute` (r2-W9, carried).
8. **Muted-captions contract unpinned** ("muted ≠ silent"; r2-W16, carried).
9. **`app/audio` tests in no gate** (standalone action; also in blocker 4).
10. **×1.25 has no golden/hit leg; 1152×648 min-window AC exercised nowhere** (r2-W15, carried).
11. **QoS scaled geometry unpinned** (this round's fix — inspection-verified only).
12. **Popover height/title text unscaled** — button rides over the title at ×1.25+ (r1-W13, carried).
13. **Run-HUD/game-over raw y anchors with scaled fonts** — rows crowd at ×1.50 (r1-W12, carried).
14. **Host/router tones never restyled per mode** vs the spec's frozen "ALL of the view" clause — needs tokens or a cause amendment (r2-W8, carried).
15. **`demolish_button_rect` nil-view unscaled twin** — parity calls THAT branch; latent until parity runs scaled.
16. **Audio row never persisted** (comment claims it does) — mute resets on relaunch (r2-W7, carried).
17. **QoS queue-depth row fully raw** (r2-W2 family, carried).
18. **Harness `banner_y` raw vs app hud-scaled** — the ×1.50 golden under-pins the app's banner (r2-W6, carried).
19. **Parity never runs under any mode/scale** — "parity holds under every mode" stays construction-argued (r1-W14, carried).

### Notes (22)

Key-buffer [10] vs 11 collectible keys (silent drop on an absurd chord) · health-card backdrop clips 5px at ×1.50 (raw y=10 + scaled pad) · node-health card x unclamped · PR-body drift ("25/25" vs 27; "byte-for-byte" is value-for-value) · `_pr_body.md` tracked · 5 demo copies inherit juice's duplicated directive line · spec-7-3 name/verb drift · palcheck threshold keyed on color-value equality (not pair identity) · `roofs_set` set before element validation (BLACK, not base, on malformed) · dead symbols (`core:strings` import, `PALETTE_MODE_COUNT`, prod-dead `step_of` + false doc, `hud_s` comment, "4 bytes" header) · orphaned `// 16.` comment · no presence scans for reduced/scale goldens + parser negative tests · panel-open-while-placing kills mouse rows until ESC · `pulse_read` "ONE seam" claim false (crisis inlines a second gate) · unbounded settings-file read · modal-blocks-world check doesn't assert selection-intact · Machado constants duplicated script/oracle with no gate leg · a11y state triple-mirrored · additive u8 settings checksum · `Demo.a11y_palette` u8 ordinal coupling · gate-2 label drift.

### Reviewer agreement

The settings-test race was independently reported by 7 lenses (acceptance/codebase/edge/tests × both chunks) and mechanically confirmed by Perkins (10/10 failing runs). The SLA/pool scaling by 4 lenses + Perkins geometry check. The `.pyc` by 7 lenses. The ui-swallow fallthrough was caught by one lens and confirmed against base `v2` by Perkins — single-source but code-anchored and diff-verified.

**Verdict: MAJOR REWORK NEEDED** — 4 blockers: the merge gate is red (test race), an input regression vs base (UI-swallow fallthrough), the SLA/pool scaling AC violation with a false PR claim, and the P0 coverage gate. The r2 fixes themselves are genuinely in (B1–B3 clean; B4's scenarios bite) — the rework is the gate + the regressions around it.

_Address findings and push — I re-review automatically on the new sha (loop-until-APPROVED)._

<details><summary>Mechanical battery (this round)</summary>

- `tools/ci-local.sh --mac`: **gate 2 FAIL** (`odin test app` 2/13 — the race); gates 3-10 not reached (stop-on-fail)
- Binaries in isolation: core 205 ✓ · app/render 11 ✓ · harness 2 ✓ (oracle poison bite ✓) · app flaky ✗
- `tools/harness.sh palcheck`: all green (51.3/54.7/43.0) · `input-parity`: 27/27 ✓
- Goldens r2→r3: zero bytes changed; a11y log.bin ≡ juice; t1 differs on the demo-name line only
- Derivation script re-run: all pairs pass under the corrected codec
- r2→r3 delta: 9 files, +159/−15

</details>
