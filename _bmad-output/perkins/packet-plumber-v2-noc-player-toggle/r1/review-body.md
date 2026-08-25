## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-noc-player-toggle · **Reviewed sha:** c9a40b6 · **Reviewers:** 7/7 completed
**Verification:** 12/14 findings confirmed against the code — 2 discarded as false-positive, 0 kept as [unverified]

The fold itself is verified solid: genuinely runtime-gated (zero residual `PP_DEBUG` code in `app/`), harness immunity holds by construction (`draw_noc_overlay` reachable only from the PP_DEBUG-gated harness verb; goldens untouched), all three build shapes compile, suites green on the reviewed sha (core 236 / app 26 / render 52 / input 5 / audio 18 / harness 2), both key mutations re-run by me and confirmed to fail the suite, and the e2e pixel-scan re-measured from the committed captures (panel region: **0.0%** dark OFF / **97.9%** dark ON — matches the PR body's 0.0%/98.5%). Inline visual check (k3): the OFF capture is a clean normal frame; the ON capture shows the full panel. One reachable state-machine defect in the new knob, plus coverage gaps.

### Blockers (1)

**1. Disabling NOC via the settings row while the panel is open leaves it stuck ON — drawn, scanned, undismissable** `[blind, edge, acceptance, architecture, tests]` — app/main.odin:635 / :520 / :891-895 / :946-951

Reachable sequence: press **D** (panel up) → **S** → activate "NOC PANEL (D)" → OFF → close. The row case flips only `noc_enabled` (:951); the draw gate (:635) and feed scan (:520) check only `overlay_on`; and `effect_overlay` (:893) now no-ops — so the panel keeps rendering, the per-frame feed scan keeps running, and the player cannot dismiss the surface they just disabled (D is dead until the row is re-enabled). Contradicts the README ("turns the feature off entirely") and the PR body's removal claim ("D becomes a no-op, zero pixels in every frame"). Five lenses converged on this independently.
**Fix:** in the `SETTINGS_ROW_NOC` case, clear the panel when disabling — `app.noc_enabled = !app.noc_enabled; if !app.noc_enabled { app.overlay_on = false }` (or gate draw + scan on `app.overlay_on && app.noc_enabled`), and pin disable-while-visible in `app/noc_toggle_test.odin`.

### Warnings (3)

**1. Boot defaults unpinned — the "default ON" pin asserts the test helper's own assignment** `[blind, tests]` — app/main.odin:296-297, app/noc_toggle_test.odin:24-27. `noc_default_app()` sets `noc_enabled = true` and the test expects it — deleting `app.noc_enabled = true` from `main()` ships the feature dead with a green suite (the D-lesson launch-path trap class this diff itself cites). **Fix:** factor boot defaults into a testable proc main() calls, or a CI leg running `PP_NOC_E2E=1` on the plain build.

**2. `SETTINGS_ROW_COUNT` 4→5 unpinned — no test reaches the row through the real nav/click path** `[tests]` — app/render/settings_panel.odin:20. Functionally correct (verified: nav wrap exec.odin:61 and the click hit-test exec.odin:738-739 both derive from the constant), but reverting the constant to 4 silently unships the row with a green suite. **Fix:** input-layer leg driving `Settings_Navigate` to row 4 (or a synthetic click on `settings_row_rect(4)`) asserting the adjust hook fires.

**3. Advisory test gate: CONCERNS** `[tests]` — P0 100%, P1 ~85% (boot default, row reachability, disable-while-visible unpinned), overall ≥80%. Adding the three pins above raises the gate to PASS.

### Notes (2)

**1. The self-exiting e2e drive now compiles into every build behind only `PP_NOC_E2E`** `[blind, security]` — app/main.odin:338. Spec-consistent (run-dev.sh `--e2e` requires it in the normal build; documented in the PR body as "env-gated, not compile-gated"). Hardening observation only (CWE-489 class): a stray env var hijacks a run into scripted D presses + self-exit; the boot-time env string is never freed (one-shot, pre-existing pattern).

**2. NOC-row presentation beyond the label helper unpinned** `[tests]` — settings_panel.odin:173-176 + the `noc_enabled` snapshot wiring in draw_hud. Cosmetic; consistent with the four pre-existing rows.

### Reviewer agreement
- **Stuck-panel blocker:** blind + edge + acceptance + architecture + tests (5 lenses — highest confidence)
- **Boot-default pin gap:** blind + tests
- **e2e-in-release note:** blind + security

**Verdict:** NEEDS CHANGES

One blocker: the headline new knob misbehaves in a trivially reachable sequence. The fix is small (one conditional clear + a pin); everything else about the fold verified clean, including mutation-proof, pixel-scan, and harness-immunity re-checks done directly on the reviewed sha.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
