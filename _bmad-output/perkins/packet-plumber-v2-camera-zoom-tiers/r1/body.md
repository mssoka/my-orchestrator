## Perkins review — r1 (glm-5.3) — REQUEST CHANGES

**Verdict: NEEDS CHANGES** — 2 blockers, 5 warnings, 4 notes. The substance of the change is verified sound at the sha; both blockers are test-coverage gates on the feature's own headline behavior, not functional defects.

**Vision caveat (non-k3 round):** pixel verification is MECHANICAL only — 49-demo golden harness byte-comparison, palcheck, sprite bbox math. Aesthetic verdicts (block legibility, puck-vs-block feel at 2.0x) are deferred for the k3 re-check; never faked here.

### Verified at the sha (mechanical, all green)

| Claim | Check | Result |
|---|---|---|
| A: `DEFAULT_ZOOM=2.0`, cluster home, `camera_set_default` at boot/reset/deselect/ESC | source read + `odin test app` (43) | ✅ |
| A: focus 2.3/2.6 unchanged, manual wheel-out floor 1.0 intact (`camera_zoom_at` clamp) | source read | ✅ |
| A: pullback floor = `DEFAULT_ZOOM`, B1 center-clamp preserved | `odin test app/render` (81) + math read | ✅ |
| B: `DUBLIN_NODE_BLOCK_L/W` 0.55/0.30 | source read (aesthetics deferred) | ✅ |
| C: puck base 1.05, cap 1.30; shipped ratios 1.136/1.273 ≤ 1.27 < cap | `assets/sprites/sprites.json` parsed | ✅ |
| D: T1 untouched — core 261 green, 0 `.t1` files in diff | `odin test core` | ✅ |
| D: T2 re-bless — 113 goldens deliberate | `tools/harness.sh run`: **49/49 demos green** | ✅ |
| palcheck green (floors untouched — see W2) | `harness palcheck` at sha | ✅ |

### BLOCKERS (2)

**B1 — Resting-home wiring unpinned (mutation-invisible call sites).** `app/main.odin:972,1135,1800`. The headline behavior (resting home on boot/run-reset/deselect/ESC) is pinned only at the callee — `pullback_test.odin:393` calls `camera_set_default` directly. Zero tests drive `effect_cancel`, `start_run`, or the selection-diff deselect (grep: comments only). Reverting any call site to `camera_set_fit` passes the entire suite (385 tests + 49 demos — the harness never runs app camera wiring). Fix: app-package tests driving the real entry points, asserting `cam_zoom_to == DEFAULT_ZOOM` / home anchor.

**B2 — Advisory test gate: FAIL.** P0 100% (all math + sim immunity pinned and green above); P1 ~45% — 0/4 resting triggers wired, vacuous puck cap (W4), sub-default band unpinned (W1). P1 < 80% → FAIL. Fix: B1's three wiring tests + W4's cap pin + W1's band pin lifts the gate to PASS.

### WARNINGS (5)

- **W1 — Auto-pullback inert at/below DEFAULT_ZOOM** *(blind+edge+acceptance+architecture+codebase+tests — 6-lens agreement)*. `camera.odin:221-232`: for zoom in [1.0, 2.0) (reachable wheel-out), `z_to` floors to 2.0 ≥ zoom → `active=false` — distant districts trigger nothing (the old 1.0 floor eased out to reveal them). At exactly 2.0 it's the documented accepted tradeoff; below 2.0 it's an undocumented dead band. Neither band has a failing-capable pin. Fix: pin `active=false` at zoom 1.5/2.0 with a far district + one doc sentence (or ease up to the default).
- **W2 — PR body palcheck claim is false** *(5-lens agreement + Perkins-verified)*. The PR body (the declared spec) says "palcheck floors re-pinned"; no palcheck change exists in the diff and the commit message says "floors had margin — no re-pin needed". Verified: `harness palcheck` green at the sha with untouched floors. Fix: amend the PR body sentence to the commit's truth.
- **W3 — `camera_set_fit` orphaned with a misleading comment** *(4-lens agreement)*. `main.odin:1741-1751`: zero call sites remain; the "explicit OUT LIMIT" role actually lives in `camera_zoom_at`'s `CAM_ZOOM_MIN` clamp (`main.odin:1991`). Fix: delete the proc or reword to past tense.
- **W4 — `PUCK_GROWTH_MAX` cap is vacuous today** *(codebase+tests)*. Shipped ratios 1.136/1.273 < 1.30 → deleting the `min()` clamp changes zero pixels and fails zero tests. Disclosed as future-proofing, but unpinned (the font-r5 gate-10 mutation-leg shape). Fix: unit pin with a synthetic bbox ratio > 1.30 clamping to exactly 1.30.
- **W5 — Tier ladder "non-overlapping by construction" is unenforced.** `main.odin:1778/1794/1819` hold literals 2.3/2.6; the ladder test compares against its own literals. Editing 2.3 → 1.9 inverts the ladder and fails nothing. Fix: hoist `FOCUS_ZOOM_NODE`/`FOCUS_ZOOM_LINK` constants; make code + test read them.

### NOTES (4)

- **N1** — PR body "48/48 green" T1 count is stale; the harness reports 49 demos (the 49th landed before this PR). Substance true (0 `.t1` files changed).
- **N2** — Dublin block growth (B) is pixel-pinned only; the block-vs-puck legibility ratio (the directive's actual complaint) has no unit pin.
- **N3** — `camera_cluster_center` is a whole-topology centroid; its "source cluster" contract holds only at the post-seeding call instant. Rename or accept fixture ids explicitly.
- **N4** — The new cluster-center test leaks (bare Topology, no `run_destroy` teardown; spawn appends allocate). Hygiene only — odin tolerates leaks.

### Reviewer agreement

6 lenses independently confirmed W1; 5 confirmed W2; 4 confirmed W3. Multi-lens findings were re-verified against the worktree — all 24 raw findings survived verification (0 rejected as hallucination).

---

*Perkins round r1 · model glm-5.3 (k3 cycle-capped; probe-verified) · lenses: blind/edge/acceptance/security/architecture/codebase/tests (7/7 completed, 0 failed) · mechanical verification: core 261, app 43, render 81, harness 49/49, palcheck green, sprite ratios parsed from sidecar.*
