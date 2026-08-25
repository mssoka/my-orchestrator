## 🤖 Perkins automated review — round 4 of 3 (loop-until-APPROVED)

**Job:** packet-plumber-v2-7.3-accessibility-core · **Reviewed sha:** `848b481a0106c1d0f82fe8e9f01f270630d5b6e5` (head of `v2-7.3-accessibility-core`, base `v2`) · **Reviewers:** 14/14 lenses (2 chunks × 7, model zai-coding-cn/glm-5.3, all valid JSON, zero failed layers) · **Verification:** 56/56 raw findings re-verified against the worktree — 0 rejected; merged/deduped to 32 unique (Perkins re-ran the full local gate itself).

### r3 blocker fix-audit (fix-audit round)

- **B1 settings-test race — FIXED and BITES.** `tmp_settings_path` now derives a per-call nanosecond-unique path (no shared counter, no shared mutable state), and gate 2 gained a `for i in 1 2 3` repeat leg. Perkins re-ran `odin test app` **8/8 full runs green** (the r3 failure mode was schedule-dependent — this is the round's sharpest bar) and the full `tools/ci-local.sh --mac`: **all 10 gates PASS**.
- **B2 UI-swallow fall-through — FIXED.** `mouse.odin` restores the base-v2 gate exactly: `if ui {swallowed} else if panel_open {modal} else {tray/node/Begin_Draw}` — a press swallowed by the QoS panel / crisis banner / SLA rows / popover can no longer run tray hit-tests or node snap. (No automated pin — warning-tier residual.)
- **B3 SLA/pool scaling — FIXED.** Anchors, row pitch, `sla_row_rect`, the pool call site, and the gauge's internal bar all hud()-scale. Geometry re-verified at ×1.25: pool label clears the SLA header by ~8.75px; row pitch == font height (no self-overlap). Residual: the SHEDDING tag inside the gauge stays raw (new warning below).
- **B4 test-gate pins — PARTIALLY FIXED (see blocker).** (a) **Fixed + bites**: the settings hit-test is now ONE shared `input.settings_press` (app + parity delegate to it) and parity asserts ≥1 `on_settings_adjust` per device — neutralizing the adjust dispatch fails gate 10. (b) **Half**: `odin test app/audio` landed in gate 2; the workflow mirror did not (carried warning). (c) **Half**: `settings_startup_apply` pins startup-apply; **the pause-on-open flip has zero coverage — this round's blocker**. (d) **Fixed**: QoS scaled-geometry test at every scale step.

### BLOCKERS (1)

1. **Pause-on-open is unpinned — deleting the `Run→Paused` flip in `effect_settings` ships CI-green** — `app/main.odin:736-747` + `harness/parity.odin:212-218`. Parity replaces the app effect hooks with counters (`panel_opens >= 1` asserts the hook *fires*, never that the run *pauses*); no test drives `effect_settings`. The r3 B4 demand was "one startup-apply **and** one pause-on-open assert" — only startup landed. This is the same unpinned-stated-behavior class as the r2 delta-0 no-op. *Fix: one headless test (extract the open/close effect path the `a11y_apply` way, or an exec-level assert that opening flips Run→Paused and closing leaves it Paused).*

### WARNINGS (13) — condensed

- **Workflow mirror still broken** (carried W5, widened): `ci.yml` runs only `odin test core` while gate 2 now runs core + 3× app + render + audio + harness.
- **Compiled `.pyc` tracked** (`tools/__pycache__/…cpython-313.pyc`) — carried from r3.
- **Parity never runs under any a11y mode/scale** (W14, since r1); **×1.25 + 1152×648 min-window AC exercised nowhere** (W15); **reduced/scale goldens have no presence oracle**.
- **Harness capture banner_y raw vs app hud()-scaled** (W6); **QoS panel internal draw partially raw** (bar, queue-depth label, reject toast — extends W2); **SHEDDING tag raw inside the scaled pool gauge** (new — renders on the bar at ×1.25+); **`demolish_button_rect` nil-view fallback still called by parity**.
- **S cannot close the panel with a pipe selected** (footer copy false, W3); **settings chip hit-test live at Game_Over — invisible modal** (carried); **AUDIO row never persisted** despite the "every change lands in the settings file" claim (W7); **modes never restyle host/router tokens** (W8, unruled).

### NOTES (18) — condensed

Key-buffer [10] vs 11-12 keys; vacuous `hud_zero_scale`; `sla_row_rect` x/width unscaled; misplaced doc comment; Brettel-vs-Machado citation mix; chip text ignores motion-only; `parse_mode_table` roofs_set-before-validate; PR body "25/25" vs 27; `crisis_card_width` hardcoded 230/10; crisis swell bypasses `pulse_read`; palcheck pr[0]-value threshold; `modal_blocks_world` never asserts selection-intact; `panel_adjust_row` recorded but unasserted; Machado matrices duplicated Python/Odin, script in no gate; `Demo.a11y_palette` u8 ordinal coupling; orphaned "// 16. pause" comment; gate-2 label drift; unused helpers in the derivation script.

### Reviewer agreement

Both tests lenses (both chunks) independently blocker-levelled the pause-on-open gap; four lenses converged on the `.pyc`; three on the workflow mirror.

### Verdict

**NEEDS CHANGES — 1 blocker.** Three of four r3 blockers are cleanly fixed and mechanically verified biting (8/8 race-free runs, gate restored, geometry corrected); B4 landed 3 of its 4 demanded pins. Land the pause-on-open assert and this is approve-shaped — the warning deck is carried debt, none merge-blocking on its own.

_Address findings and push — I re-review automatically on the new sha._
