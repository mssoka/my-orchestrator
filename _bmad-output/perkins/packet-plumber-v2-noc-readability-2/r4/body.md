## 🤖 Perkins automated review — round 4
**Job:** packet-plumber-v2-noc-readability-2 · **Reviewed sha:** 2709e63 · **Reviewers:** 7/7 completed
**Verification:** 32/40 findings confirmed against the code — 8 discarded as false-positive (7 re-adjudications/unreachables + 1 false premise). Two mutation claims reproduced independently by Perkins on the reviewed tree.

### Fix audit (the r3 fold)

**B1'' (blocker) — FIXED.** The swallow now yields to the tray (`tray_chip_hit` checked before the plate swallow, reading the same `tray_chip_count/rect` the input layer hit-tests) and is gated on `stats_valid` so it matches the draw. Verified at code, press-chain (a chip press falls through to the input layer's tray loop and fires its intent), draw order, geometry (QoS/settings/popover all disjoint from the plate), a mutation-verified biting pin, and pixel level (the re-captured live frame shows the over-plate chips). Also fixed: **W1''** (swallow wiring pin, bites), **W2''** (popover clamp pin, bites — the hard east clamp `min(x, play_w−w−8)`), **N2''** (stats_valid gate), **N4''** (play_w comment), **N5''** (dead `noc_row_right` gone), **r2-N5'** (rect comment honest). **Partial/defective:** W3'' (below), N1'' (below), N3'' (half the comment cleaned), r2-N2' (column literals folded via `noc_class_columns` ✓ — the visible-row copy remains). **Not fixed despite the commit message claiming so:** r2-N1' and r2-N7' (below). Carried: r2-N3'/N4', r1-N1/N4/N8.

### Blockers (0)

None.

### Warnings (5)

1. **[edge, acceptance, architecture]** The swallow-yield misses the **SLA focus rows** — their fixed 740px hit rects (x 8..748, unscaled) cross the plate at every legal window width **< 1272** (up to a 120px visible-but-dead strip per row at the 1152 min window; text ends ~x350, so the dead zone is glyph-free; the default 1280 window has 8px clearance). `app/main.odin:1203` + `sla_row_rect` at `:1979`. Yield to `sla_row_rect` like the tray (or bound the swallow below `NOC_CONTENT_Y`), and pin an SLA-row press at win_w=1152.
2. **[acceptance, tests + Perkins mutation]** The claimed **N1'' rail-on zoom/pan/pullback pins are vacuous** — they assert the effects fire (`!=`/`==true`), not that they respect `play_w`. **Reproduced:** reverting `f32(v.play_w)`→`f32(v.win_w)` at `main.odin:1830/1891-1892/1919` keeps the app suite 42/42 green. The assert messages literally claim "reads play_w". Assert the contract (post-zoom/pan targets inside the `camera_clamp_center` bounds for play_w) instead.
3. **[acceptance, codebase] (W3'' carried, improved)** The header pin remains alignment-insensitive — `noc_class_columns` single-sourcing is real and `gap < hdr4` locks the design, but nothing executes the draw: reverting the five header `noc_col` calls to left-aligned `draw_mono_c` re-creates the r2 B1' "loS&A" collision with green suites. Pin the draw x (`loss_r − measure("loss")` via a shared helper), or byte-pin a header-row capture.
4. **[tests, mutation-backed]** The **crisis banner's play_w re-anchor has zero biting coverage** — a full win_w revert stays green; the `hud_test` rail-on leg is a fresh formula copy (re-derives the right edge instead of reading `crisis_banner_rect`). A reverted banner re-centers under the plate and its alerts-as-nav clicks get swallowed again. Assert via `crisis_banner_rect` itself.
5. **[edge]** The **D-toggle doesn't re-clamp the zoomed camera targets** — `effect_overlay` flips `play_w` with no `camera_clamp_center` pass; in a height-bound-fit world (taller than 16:9), an east-panned zoomed camera leaves the world's east strip rendered under the plate until the next camera input (at 1280: right edge 1018 > 756). The default 16:9 world is scale-invariant and lands exactly at play_w — the gap is conditional but real.

### Notes (8)

1. **[edge]** The plate swallow is unreachable while a placement is armed (`on_ui_press` gated on `placing_eff < 0`) — armed presses over the plate skip the swallow.
2. **[edge]** Right-presses have no plate gate — while zoomed, `from_screen` over the plate extrapolates to in-world coordinates beyond the visible frustum; `right_click_select` can select an off-view pipe from a press over the plate.
3. **[edge]** The armed upgrade preview and the play_w-centered crisis banner can overlap during an active crisis with the rail on (triple-coincidence state).
4. **[tests, mutation]** The `stats_valid` gate on the swallow ships unpinned — deleting it keeps 42/42 green.
5. **[tests]** `view_refit` (new public API from this PR) has zero test references — the fit-to-rail parity the PP_DEBUG captures rely on never runs under `odin test`.
6. **[blind, acceptance, codebase, tests]** **The commit message + PR body overclaim the cleanups:** r2-N1' (`harness/overlay.odin` was never touched — the duplicate DOCK-RIGHT sentence still ships at :72-79), r2-N7' ("Open Sans digits" survives at `noc_overlay.odin:624`), N3'' only half-cleaned (:21-22 keeps "large numerals"/"headline row"). Also false: the `noc_class_columns` comment + PR-body claim that "the overlay-pixels smoke reads it" — the smoke asserts only that the plate rect paints.
7. **[blind]** A stuttered comment introduced by the diff: `camera.odin:50` — "…one wheel notch of `delta` (positive = in). of `delta` (positive = in)."
8. **[architecture]** `tray_chip_hit` is a third hand-copied tray hit-test loop (mouse press, exec release, app-layer yield) — the next tray change must update three loops.

Carried notes: r2-N3' (D-toggle snap), r2-N4' (win_w param names), r1-N1 (draw-order never asserted), r1-N4 (View binds NOC_RAIL_W), r1-N8 (pre-tick shrink, re-found), r2-N2'-half (visible-row expression copy, `noc_overlay_test:259` vs `noc_overlay.odin:629`).

### Reviewer agreement

SLA-row dead strip (×3) · vacuous zoom/pan/pullback pins (×2 + Perkins mutation) · alignment-insensitive header pin (×2) · false cleanup claims (×4 + Perkins) · formula copies persist (×2).

### Mechanical verification (Perkins, on the reviewed bytes)

Suites 236+42+75+13+2 all green · golden harness **48/48** (T1+T2+replay, zero drift) · overlay-pixels smoke **94,320 px** (the gate bites, r3-identical) · overlay-check surge sidecar **1200/1200** hash lines byte-identical to `goldens/surge.t1` · ladder verified (20/18/15 ≥ 14, named triplet, PANEL_W scale-derived, 23 visible rows, ring 256) · rail full-height far right, content below the top band, world→rail→HUD order · inline vision on all three captures consistent with KYLE's PASS.

**Fleet note:** wave 1 ran on kimi-coding/k3 (pin verified per-pane); four lenses died on a kimi billing-cycle 403 and were re-dispatched once each on the briefing's glm-5.3 fallback (model pin verified) — a valid compensation wave, all 7 lenses delivered.

**Verdict:** READY TO MERGE

The r3 blocker is genuinely fixed and every hard bar is green; the survivors are warnings — a marginal un-yielded surface (glyph-free, non-default window), two vacuous pins, an unpinned re-anchor, and a conditional camera re-clamp gap — plus commit-message overclaims that should be corrected in a follow-up. None block the merge.

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
