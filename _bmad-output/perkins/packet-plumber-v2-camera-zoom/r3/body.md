## 🤖 Perkins automated review — round 3
**Job:** packet-plumber-v2-camera-zoom · **Reviewed sha:** 9094f45 · **Reviewers:** 7/7 completed
**Verification:** 28/28 findings confirmed against the code — 0 discarded as false-positive

### Fix audit (r2 → r3)

**All three r2 blockers folded in code** — B1's center clamp is real and the off-center floor pin's fixture is genuine (cy=585 is exactly the 2.0 bottom clamp; district inclusion asserted at convergence). B2's policy is pinned and routed. B3's composition pins exist. **But both fixes at the seams introduced new blockers** (below), the W5 fold is one of them, and the advisory gate lands at CONCERNS, not PASS: the W4 pin turned out vacuous (the router is placed *before* the seed, so the kind filter is never traversed — the exact r2 skew mode is untested), and the wheel clamp band / effect_pan values / ease-rate band are unpinned. W1–W7 otherwise genuinely folded (W4's code is correct — the terminals-only/junctions-only doctrine verified in core); N1 half-folded (view_compute still carries its own fit copy), N6/N7 partially (View heap leak, touch.odin stale header), N11 clean.

Mechanical gates on this head: 11/11 native CI (incl. input parity 27/27), fast container 1-2, harness 48/48 demos green with T1/T2/replay byte-identical — zero golden drift confirmed.

### Blockers (2)

**B1 — effect_pan clamps the pan target at the LIVE zoom, not `cam_zoom_to`** (`app/main.odin` effect_pan; blind+edge agree). The stored targets converge at `cam_zoom_to` but are validated at the eased `cam_zoom`, and `camera_update` never re-clamps. A drag during any zoom-out ease — including the 1.5–2 s pullback window, the most natural moment to grab the map — converges with the viewport past the world edge: from live 2.0 → target 1.0, a pan to cy=585 (valid at 2.0) converges showing world y ∈ [195, 975]: a 195px cut-off band plus void, the exact r2-B1 failure shape via the pan path. Mirror case: a drag during a zoom-IN ease at the fit clamps at 1.0, pinning the target to the world center and silently destroying the wheel's off-screen-center zoom-to-point anchor. *Fix: pass `cam_zoom_to` to `camera_clamp_center` (keep the live zoom for the delta conversion per W5); add a mid-ease pan value pin.*

**B2 — release-build wheel dead-zone via the ungated D-key** (`app/input/mouse.odin:173` + `app/main.odin:964/1704). `effect_overlay`'s comment claims "the toggle + the draw are compile-gated" — only the draw is; `mouse.odin` has zero PP_DEBUG gates, so a release build can set `overlay_on` (invisible). The ungated `camera_wheel_policy` then returns `.Noc_Scroll` over the 360×600 panel rect (~23% of the window) and `effect_zoom`'s PP_DEBUG-gated body compiles to a bare return: **the wheel silently dies over a quarter of the map with no visible cause**. *Fix: compile-gate the D mapping (or the Toggle_Overlay exec case) under PP_DEBUG.*

### Warnings (8)

1. **The W4 pin is vacuous** — the interleaved-router test places the router *before* the seed; the newest-terminal walk takes the seed without traversing the junction, so deleting the Terminal filter keeps the test green. Swap the spawn order.
2. **The pullback-yield test writes the real settings dotfile** — `settings_save_app` on a zeroed App (override "") falls back to `~/.pp-settings.bin`; the app7 toggle leg persists `auto_pullback=false` to the dev's actual file every native run, violating the proc's own "a test must never touch it" invariant. Inject a temp path.
3. **8-id cap on the spawn walk** — a 9+ spawn frame hits `found != n_spawns` and silently skips the pullback (unreachable via current data: interval 80 ≫ the 5-tick frame cap, but interval is balance.json data).
4. **The W7 exclusion rests on an unstated data invariant** — correctness needs `terminal_spawn_interval_ticks` > max ticks/frame; at interval ≤ 5 the frame window diverges from plan-time classification (false SEEDs). Assert or derive from the interval.
5. **Wheel clamp band [1.0, 4.0] unpinned on the wheel path** — clamp-removal regressions pass every test (the existing test deliberately sidesteps the clamp).
6. **effect_pan has zero value assertions** — the W5 fold's live-zoom conversion and the clamp application (exactly the B1 seam) are untested.
7. **Ease-rate band weakly pinned** — a 0.14-rate regression (0.66 s, outside the ruled ~1.5–2 s band) passes the "still in flight after 30 frames" assertion.
8. **Advisory test gate: CONCERNS** — P0 100%, P1 ≈87% (34/39), overall ≈86%. The four gaps above are the delta to PASS.

### Notes (14)

Stale-latch guard can synthesize a release every frame while placement is armed (clear the latch in the guard branch itself); `camera_pullback_target`'s "clamp is a no-op for a zoom-out" comment contradicted by its own B1 pin; **PR-body test counts stale (4+4+4 vs actual 9+7+7+2 — third round of drifted counts, 3 reviewers)**; start_run's latch reset still unpinned (r2 W10 asked); the fit derivation still duplicated in `view_compute` (N1 half-folded, comment overclaims); touch.odin header still calls Pan "a deliberate no-op"; `cam_test_ctx` leaks its heap View; five ungated NOC constants vs the comment's "four"; the Pan executor has no draw guard (touch two-finger pan fires mid-draw); wheel residue pre-charges across NOC-scroll/modal consumption (≤1 notch early, never spontaneous); `camera_newest_terminals` has no direct unit pin (edges + ordering); the "second SEED mid-ease retargets" PR claim unpinned; the poll wheel seam is an acceptable untested raylib boundary; the W4 pin's id comments say 6/7, actual 3/4.

### Reviewer agreement
- **effect_pan live-zoom clamp** — blind + edge independently (B1).
- **PR-body count drift** — blind + acceptance + tests (N3).
- **Fit still duplicated in view_compute** — architecture + codebase (N5).

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
