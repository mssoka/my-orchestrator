## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-7.3-accessibility-core · **Reviewed sha:** `3fa0703b8368bec7bed91ffee27a34d43bcf4584` (head of `v2-7.3-accessibility-core`, base `v2`)

**Reviewers:** 14/14 lens runs completed (7 lenses × 2 chunks — `app/` and harness+tools+demos+data; big-diff policy, goldens byte-verified mechanically and summarized). Model note: kimi k3 hit its billing-cycle cap mid-round — 6 lenses re-dispatched once on `zai-coding-cn/glm-5.3` (sanctioned fallback, ruling 08-17); one lens JSON repaired in place (raw tabs in evidence strings; findings cross-confirmed by 3 independent lenses).

**Verification:** 54/59 reviewer findings survived code re-verification — 5 discarded as false-positive/unreachable, 2 demoted; every survivor re-read at its cited lines in the round worktree. **Mechanical gates (Perkins, at this sha):** `tools/ci-local.sh --mac` **10/10 green** · palcheck **bite-test PASS** (poisoned deutan pair → `FAIL a11y separation (deutan; min sim-dist 0.0)`, exit 1 — restored after) · derive script **re-emits the shipped mode tables exactly** (JSON-identical) · all 5 a11y `.log.bin` **sha256-identical to juice.log.bin**, `.t1` state hashes identical except the `demo <name>` header · 20/20 goldens entries are **new files** (no pre-existing golden touched; ×1.00 identity holds) · **no `core/`, no LOG_VERSION, no catalog edits** (byte-checked) · vision-read (qwen3.8-27b): a11y_reduced crisis frame **PASS** (static banner + full-width outline + glyphs — never-color-alone holds), a11y_scale ×1.50 HUD-grows/world-unchanged **PASS**, forecast occlusion flagged (→ B4).

The presentation-only discipline and the palette derivation are in excellent shape — the blockers are all in the new input/settings/scaling surface, not the a11y core.

### 🔴 BLOCKERS (6)

**B1 — Keyboard settings-panel surface is dead** (`app/input/mouse.odin:76-95` vs `119-157`) · [edge + codebase + Perkins trace]
The phase-1 keys buffer collects only P/Space/D/T/M/Esc; S/↑/↓/←/→/Enter fall to `case:` and are never collected, so the whole panel-open key branch **and** `case .S → Toggle_Settings` are unreachable. Keyboard cannot open, navigate, adjust, or close the panel. The panel footer "S / tap chip to close" and the PR's "keyboard (S, arrows, Enter, Esc)" are false as shipped, and `input_parity_settings_panel`'s keyboard leg passes **vacuously** (S,Down,Enter,S never open the panel; it asserts only "ends closed" + empty commands).
⚠️ **Fix hazard:** phase-2 still maps raw-event S → `Set_Lane(Standard)` when a pipe is selected — merely adding S to the collection switch makes one keypress open the panel AND silently reassign the selected class's QoS lane (three lenses tripped on exactly this). Resolve S ownership in the same change.

**B2 — Touch can only step UI scale UP** (`app/main.odin:769-773` + row-tap `delta 0`) · [acceptance + Perkins]
Row taps deliver delta 0 → `step=+1`, clamped at 150%. Keyboard ←/→ and pad D-pad ←/→ have ±1; **no touch path emits −1**. A touch-only player reaching 150% is stuck there — and it persists to `~/.pp-settings.bin` across relaunch. Palette wraps (recoverable); scale clamps (not).

**B3 — Settings persistence: zero automated coverage** (`app/settings.odin`, new 132-line file) · [tests ×2 + Perkins grep]
No test in the repo references `settings_load`/`settings_save`/`scale_of`/`step_of`. The corrupt/truncated/foreign-version/checksum/range → defaults contract (spec I/O matrix; briefing flag-for-verification) is entirely unpinned. Repo doctrine: "everything testable headless, is."

**B4 — ×1.50: crisis banner occludes the forecast panel** (`crisis.odin:crisis_banner_rect` vs `forecast.odin:64`) · [Perkins geometry + vision-read; blind's unscaled-y family]
At ×1.50/1280×720 the banner spans x 415–985, the forecast panel starts at x 962 → **23px overlap**; "WEATHER REPORT / streaming_surge ×10 NOW" renders behind the banner (none at ≤1.25). E9.3 "chrome stays legible at each step" fails at the knob's own max step, in the crisis moment both surfaces exist for.

**B5 — ×1.25/×1.50: QoS action row overlaps and mis-hits** (`app/qos_panel.odin:77-82` + hit order `230-243`) · [acceptance + architecture + Perkins]
Slot 0 scales, slot 1 (Revert) stays unscaled: at ×1.50 slot 0 spans x 30–210 vs slot 1 x 148–238 — **62px of Revert sits inside slot 0's hit rect, and slot 0 is hit-tested first**: clicking most of the visible Revert button opens the weight editor / reverts-to-auto instead. 27px already at ×1.25. Preset chips + nudge rects unscaled too (smallest hit targets exactly when users need them larger).

**B6 — Advisory test gate: FAIL** · [tests ×2]
P0: negative legs missing (palcheck separation oracle — verified it bites, but nothing in CI proves it). P1 ≈60%: scaling ~55% (×1.25 unpinned, scaled hit-tests unexercised), settings-panel input ~65% (shallow/vacuous parity), persistence 0%. Overall ≈67% — all three FAIL clauses trip.

### 🟡 WARNINGS (8)

**W1 — SLA gauges: scaled text on unscaled 16px pitch + 18px hit rects** (`app/main.odin:1397-1405` vs `1615`) — rows overlap ~4px at ×1.25, ~8px at ×1.50; focus-row hit drifts. [codebase + Perkins]
**W2 — draw_hud top-left + game-over blocks: scaled fonts on unscaled y anchors** (title y=10 / hint y=36 / score y=56 / toast y=68 vs retry y=104) — overlap at ×1.50. [blind + Perkins]
**W3 — Demolish popover: width scales, height (64/92) + text don't** — at ×1.25+ the pipe-popover button rides up over the title. [edge + architecture + Perkins]
**W4 — ×1.25 step unpinned; no hit-test/parity run at any scale >1.00; spec's "1152×648 AC-pinned" checkbox has no exercising path** (harness renders 1280×720 only). [tests ×2 + edge + Perkins]
**W5 — The 25/25 parity scenarios never run under any a11y mode** — "full input parity holds under every mode" is construction-argued only; ui_scale is the real residual risk (chip rect is mode-dependent). [tests ×2 + edge]
**W6 — input_parity_settings_panel is shallow: `panel_row` captured, never asserted; legs end on divergent rows (kbd/pad 1, touch 0)** — PR's "identical end input-state" overstates; Settings_Activate's effects run nowhere. [6 lens runs]
**W7 — palcheck separation oracle has no committed negative leg** (verified it bites at this sha — a neutered oracle would still pass CI silently). [tests ×2 + architecture]
**W8 — Muted-audio captions ("muted ≠ silent") not pinned despite the spec's "pin it"** (no mute case in audio_test). [tests + Perkins]

### 🔵 NOTES (18)

1. pulse_read billed as the ONE motion seam; crisis.odin hand-rolls a second gate (phase math differs — couldn't call it verbatim). [architecture + codebase]
2. Unused `import "core:strings"` in palette.odin (build is green — the "build fails" claim was false). [blind]
3. `step_of` + `PALETTE_MODE_COUNT` dead exports. [codebase]
4. Settings chip shows no reduced-motion indicator text. [acceptance]
5. `demolish_button_rect` nil-default view = opt-out second source (no nil callers today). [architecture]
6. parse_mode_table sets `roofs_set` before validating elements — malformed entry → opaque **black** roof (corrected from the lens's "transparent"). [edge]
7. Settings checksum is an additive u8 sum — sum-preserving corruption passes (fail-visible doctrine accepts; optional CRC8). [edge]
8. Derive script dead helpers (scale_lum/mix). [blind]
9. Spec drift: intent names (Settings_Toggle vs Toggle_Settings), "0.99 mid-envelope" vs shipped 1.0 full pin, `a11y <mode>[,<mode>]` comma verb unimplemented. [blind + codebase]
10. Chip/SLA bottom-left adjacency — the planned 3rd gauge row collides at ×1.25+. [codebase]
11. start_run never resets panel_open/panel_row (unreachable today; defense-in-depth). [architecture]
12. Panel open + placement armed (pad Y + mouse): ui-press gated on placing<0 → modal rows dead for mouse until ESC (touch unaffected). [edge]
13. `_pr_body.md` committed tracked at repo root. [blind]
14. Orphaned "// 16. pause" comment above the settings scenario. [blind]
15. Caption strip / chip / panel never enter T2 capture (by design — capture-stability). [tests]
16. No presence scans for a11y_reduced/a11y_scale goldens; a11y demo-verb parse-error legs untested. [tests]
17. palcheck threshold picked by pr[0] color-value equality, not pair identity — fragile. [blind + edge + architecture]
18. QoS hint still advertises S as a lane key ("[1/2 + E/S/B]") — accurate today, but the panel footer and PR claim S opens settings; resolve with B1. [blind]

### Reviewer agreement (independently converged)

- **Keyboard-dead panel surface / S ownership**: edge + codebase (+ blind/acceptance/architecture's collision variants, absorbed into B1)
- **Settings persistence 0% coverage**: tests ×2 · **QoS action-row overlap**: acceptance + architecture
- **panel_row never asserted / divergent legs**: 6 lens runs · **parity-under-modes unexercised**: tests ×2 + edge
- **palcheck negative leg**: tests ×2 + architecture · **pr[0] threshold fragility**: blind + edge + architecture · **popover partial scaling**: edge + architecture

**Rejected as false-positive/unreachable (5):** "unused strings import fails the build" (CI green), "panel opens at Game_Over / invisible modal eats retry" (all mappers gate Game_Over first), "S dual-dispatches as shipped" ×3 variants (phase-1 S is unreachable — that *is* B1; the dual-dispatch is latent in the fix, folded into B1's hazard), "pad opens panel at Game_Over / retry carries panel_open" (unreachable), "derivation script ≠ shipped tables" (mechanically disproven — exact match).

### Verdict

**MAJOR REWORK — 6 blockers (2 functional dead surfaces, 1 trapping input path, 1 AC-violating occlusion, 1 mis-hit cluster, 1 coverage-gate FAIL) + 8 warnings.** The a11y palette core, derivation, goldens, and presentation-only discipline are solid and verified green — the rework is concentrated in the settings-panel input surface (B1/B2), the ×1.25+ chrome geometry (B4/B5 + W1-W3), and the missing pinned legs (B3/B6).

_Address findings and push — I re-review automatically on the new sha._
