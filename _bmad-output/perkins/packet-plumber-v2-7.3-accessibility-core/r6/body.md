## 🤖 Perkins automated review — round 6 of 3

- **Job:** packet-plumber-v2-7.3-accessibility-core
- **Reviewed sha:** `fe233c075599c55841e7040a4a5ea7ee5dbba0f0` (headRefOid re-fetched pre-post: unchanged)
- **Reviewers:** 14/14 completed (7 lenses × 2 chunks: chunk-app 2,574 + chunk-rest 8,767 lines; model zai-coding-cn/glm-5.3), 0 retries, no failed layers
- **Verification:** 71 raw lens findings → 38 confirmed unique (5 rejected as false-positive, 1 kept [unverified]); every survivor re-read against the reviewed worktree by Perkins, plus 2 scratch-worktree revert checks and 42 pristine `odin test app` runs

### Fix audit (r5 → r6)

- **r5 blocker 1 — FIXED, and the fix BITES.** The r6 delta adds the two exec-level legs the r5 briefing demanded (`settings_effect_wiring_pauses_on_open`, `settings_chip_click_pauses_end_to_end` — the a11y_apply precedent: construct App+Input, drive `effect_settings` itself). Perkins ran the mandated revert check in a scratch worktree: deleting the Run→Paused flip in `effect_settings` now **FAILS** `odin test app` (2 tests). The r4 failure mode is closed.
- **Carried spot-checks:** ui-swallow gate, SLA/pool hud() scaling, and linear_to_srgb/palcheck all hold at this sha (palcheck all green, min dists 51.3/54.7/43.0). The settings-test race does **not** hold — see blocker 1.
- **r3 Game_Over chip warning is FIXED at this sha** (mouse_map + touch_map both early-return at Game_Over; pad Y is mode-gated) — dropped from the warning list.

### BLOCKERS (2)

1. **Settings-test temp-path race NOT closed** [acceptance + perkins, carried since r3] — `app/settings_test.odin:27-36` (`tmp_settings_path`). The lens-guard demands repeated full `odin test app` runs stay green; they do not. Perkins reproduction at this sha: **1 failure in 30 pristine runs** (`main.settings_truncated_defaults` — "failed its checksum — defaults" on a shared `/tmp/pp-settings-test-<ns>` path); the acceptance lens independently saw 2/10. macOS's clock returns identical nanosecond values for back-to-back calls, so parallel tests land on one path and `os.remove` deletes another test's fixture. Gate 2 runs the suite 3× per `ci-local` → ~10–15% flake per full local CI pass. *Fix: add pid/atomic-counter/random suffix to the temp path; never `os.remove` a path a parallel test may own.*
2. **`effect_settings_adjust` has zero exec-level coverage — the r5 trap, adjust twin** [tests + perkins, NEW] — `app/main.odin:750-773`. Perkins revert check: deleting the palette apply, the `ui_scale` apply, AND `settings_save` from the adjust body ships **18/18 green**. The pure helpers are pinned; the wiring is not — the exact class r4/r5 blocked on, one proc over. *Fix: an exec-level leg per row (the chip-click test pattern), with a path-injected `settings_save_at` assert.*

### WARNINGS (15)

Carried (verified still present at this sha): tracked `.pyc` (r3) · ci.yml mirror runs only `odin test core` vs 5-suite gate 2 (r2) · harness crisis `banner_y` raw vs app hud-scaled (r2) · AUDIO mute row never persisted (r2) · `demolish_button_rect` nil-view fallback exercised by parity (r3) · S cannot close the panel with a pipe selected vs footer copy (r2) · QoS panel raw proportion-bar/labels (r2-family) · SHEDDING tag raw inside scaled pool gauge (r4) · parity never runs under any a11y mode/scale (r1) · x1.25 + 1152×648 min-window unexercised (r2) · modes never restyle host/router tokens (r2) · palcheck has no reduced/scale presence oracle (r1) · palcheck threshold keyed on `pr[0]` value-equality (r1).
New at r6: **in-progress drag survives a panel open/close** (S collectible mid-drag; `Toggle_Settings` never cancels — a release after close commits the draw at the new cursor) · Settings_Navigate row-wrap boundaries untested at exec level.

### NOTES (36)

31 carried (doc/comment drift, dead code, oracle-rigor, coupling, hygiene families from r1–r5) + 5 new minor (predictable `.tmp` save path, demo-parser trailing tokens, `a11y` parser untested, deutan/protan mode tables byte-identical in palette.json — confirm intended, small doc/comment nits). Full machine-readable detail in `consolidated.json` (r6).

### Reviewer agreement

Multi-source confirmations: the `.pyc` artifact (5 sources), ci.yml mirror, banner_y, mute persistence, demolish fallback, S-ownership, parity/a11y coverage gaps, palcheck oracle routing (2–4 sources each). Both blockers were independently reproduced by Perkins with mechanical revert/flake checks — not lens-word taken on trust. (The acceptance lens's blocker-1 evidence cited impossible line numbers — the claim was nonetheless real and was confirmed by direct reproduction with a corrected location.)

### Mechanical gates (Perkins-run at this sha)

- `tools/ci-local.sh --mac`: 10/10 PASS (gate 2 incl. 3× `odin test app` — flake did not trigger this pass)
- palcheck: all green · input parity 27/27 (gate 10)
- Revert check 1: pause flip deleted → 2 tests FAIL ✅ (r5 fix bites)
- Revert check 2: adjust apply/persist gutted → 18/18 green ❌ (blocker 2)

### Verdict

**NEEDS CHANGES** — 2 blockers. The r5 fix landed and provably bites; but the test-suite flake the r5 spot-check cleared is demonstrably alive, and the adjust twin of the just-fixed wiring trap is unpinned.

_Address findings and push — I re-review automatically on the new sha._
