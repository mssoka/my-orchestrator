## 🤖 Perkins automated review — round 5 of 3

- **Job:** packet-plumber-v2-7.3-accessibility-core (Story 7.3: accessibility core)
- **Reviewed sha:** `12166ea0c7ff00e106f8f8da538dbd5151123e33`
- **Reviewers:** 4/7 completed (chunk-app: blind, security, architecture, codebase). edge/acceptance/tests failed twice (incl. one retry each) — zai-coding-cn/glm-5.3 provider 5h quota exhausted (429, resets 2026-08-20 07:07). The chunk-rest wave (goldens/harness/tools/docs) was not dispatchable for the same reason. **Degraded round** — flagged for Gru.
- **Verification:** 26/37 lens findings survived code re-verification (3 rejected as false-positive; 0 speculative). Perkins ran the full mechanical suite locally.

### Mechanical gates (local suite = ground truth; GH Actions billing-blocked)
- `tools/ci-local.sh --mac`: **10/10 gates PASS** (gate 2 incl. core + 3× `odin test app` + render + audio + harness)
- `odin test app`: **16/16 GREEN** · input parity **27/27** · palcheck **all green** (min sim-dist 51.3/54.7/43.0)
- Carried r3/r4 fixes spot-verified at this sha: settings-test nanosecond paths, ui-swallow base-v2 shape, SLA/pool hud() scaling, corrected linear_to_srgb in both copies — all hold.

### BLOCKERS (1)

1. **The r4 blocker is NOT closed — the pause pin guards the helper, not the wiring** [architecture, codebase, perkins] — `app/main.odin:736-743` + `app/settings_test.odin:210-229`. r5 extracted `settings_pause_effect` and unit-pinned it, but **no test drives `effect_settings` itself**; parity still replaces the app effects with a recorder that only counts `panel_opens >= 1`. The r5 briefing's hard requirement was: *deleting the flip in effect_settings must FAIL CI.* I ran the revert-style check mechanically in a scratch worktree at this sha: deleted the flip → **`odin test app`: 16/16 still GREEN.** The behavior regresses CI-silent — the exact r4 failure mode. **Fix:** add the exec/effect-level leg the briefing demanded (the `a11y_apply` precedent): construct App+Input, call `effect_settings`, assert open flips Run→Paused and close leaves it Paused — not only the pure proc. *(still present since round 4)*

### WARNINGS (13) — all carried, re-verified at this sha
pycache tracked (r3) · ci.yml mirror runs only `odin test core` (r2) · parity never runs under any a11y mode/scale (r1) · ×1.25 + 1152×648 min-window unexercised (r2) · harness banner_y raw vs app hud() (r2) · S can't close panel with a selection, footer copy false (r2) · settings chip opens an invisible modal at Game_Over (r3) · AUDIO row never persisted despite contract comment (r2) · QoS panel internal geometry partially raw · SHEDDING tag raw inside scaled pool gauge (r4) · demolish_button_rect nil-view fallback called by parity (r3) · modes never restyle host/router tokens vs frozen Always clause (r2) · reduced/scale goldens lack a presence oracle (r1)

### NOTES (22)
Key buffer [10] vs 12 collectible (r2) · sla_row_rect x/width raw (r4) · settings header "4 bytes" vs actual 6 · step_of dead in production · closed-panel nav-key emission (benign dead) · unbounded dotfile read · hud_zero_scale inline emulation (r2) · tmp_settings_path comment on wrong proc (r4) · Brettel-vs-Machado citation drift (r4) · chip text ignores reduced-motion-only (r4) · parse_mode_table roofs_set order (r1) · PR body "25/25" vs shipped 27 (r3) · crisis 230/10 coupling (r4) · crisis swell duplicates the seam (r1) · palcheck threshold keyed on color value (r1) · modal_blocks_world selection assert missing (r3) · panel_adjust_row unasserted (r4) · Machado duplication Python/Odin (r1) · demo ordinal coupling (r1) · orphaned "// 16. pause" comment (r2) · gate-2 label drift (r2) · dead helpers in derive script (r4)

### Reviewer agreement
The blocker was independently flagged by **two lenses** (architecture, codebase) and confirmed by my mechanical revert check — highest-confidence signal. demolish nil-view fallback (4 sources) and ci.yml mirror / banner_y / AUDIO persistence (3 sources each) also multi-source.

### Verdict
**NEEDS CHANGES** — the single r4 blocker (pause-on-open pin must bite on the wiring) is still present; everything else green.

_Address findings and push — I re-review automatically on the new sha._
