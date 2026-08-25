## Perkins automated review — round 1 / Job: packet-plumber-v2-viscomm-tie-deconflict / Reviewed sha: 4b3a887 / Reviewers: 7/7 completed / Verification: 16/18 confirmed, 1 discarded (1 kept [unverified] speculative)

## Code Review Report

**Diff source:** branch diff v2 @ 9622ef5…PR head 4b3a887, 6 files, +200 −16
**Spec:** packet-plumber-v2-viscomm-tie-deconflict briefing (AC: tie exits the amber warning family; dashed ring never reads as the solid congestion telegraph)
**Reviewers:** 7/7 completed
**Verification:** 16/18 reviewer findings survived code re-verification — 1 discarded as false-positive, 1 kept as [unverified] speculative

### BLOCKERS (1)

**1. Shape mutation leg is vacuous against the actual draw path: reverting draw_tie_mark to a solid ring passes CI** [acceptance] — `app/render/palette_polish_test.odin:164-185`, `app/render/assist.odin:505-509`

The dashed-ring test pins only the `tie_dash_on` predicate and the `TIE_DASH_SEG`/`TIE_DASH_COUNT` constants; nothing pins that `draw_tie_mark`'s draw loop actually consults the predicate. Replacing the dashed loop with the old solid `DrawCircleLinesV` ring (leaving `tie_dash_on` intact) fails no test — the guarded shape can be deleted silently.

*Independently mutation-proven at review time (twice): deleting the `if !tie_dash_on(i) { continue }` guard at assist.odin:507-509 → `odin test app/render` 83/83 PASS.*

**Recommended fix:** pin the draw path itself — factor the per-segment draw enumeration into a pure proc that `draw_tie_mark` consumes, and assert the drawn-segment set equals `{i : tie_dash_on(i)}` — so removing the dash modulation from the draw path breaks the count assertion.

### WARNINGS (6)

**1. Verification was run on a comment-stripped copy, not the shipped palette.json** [blind] — `_pr_body_viscomm_tie.md:64-67`

The derive tooling (`tools/derive_a11y_palettes.py:97`, bare `json.load`) cannot parse `data/palette.json` (the `//` comments added by the font overhaul break strict JSON — reproduced: `Expecting property name enclosed in double quotes: line 11 column 39`). The a11y numbers in this PR were produced on a private comment-stripped copy that is not in the diff, so they are unreproducible from these bytes. *Fix:* strip `//` comments inside the script and re-run it against the shipped file; commit reproducible output.

**2. New route_tie violet is only 14.0° from router_tier_high (below the 15° node-signal canon); both are node-centered rings on routers** [codebase] — `app/render/palette_polish_test.odin:158`

The PR claims "≥ 62° from every tier" but the hue test's `tiers` array covers pipe tiers only (`pipe_copper/steel/fiber`). Router tier rings are also node rings drawn on routers — exactly where ECMP split nodes are. Recomputed with the repo's own `hue_degrees`: route_tie 264.35° vs router_tier_high 250.32° = **14.03° < 15°**; Machado tritan-sim distance 21.9 < T_SIGNAL 48 (deutan 52.8 / protan 94.5 pass). *Fix:* add the three `router_tier_*` tokens to the tiers array; shift route_tie hue (toward blue/magenta) to clear 15° from router_tier_high.

**3. a11y oracle has no route_tie-vs-state_congested pair — the finding-A collision class remains unguarded under CVD mode tables** [codebase] — `harness/palcheck.odin:96-106`

The old tables passed every gate while simulated tie-vs-congested distance was 0.0 (the old pale-amber route_tie remap was RGB-identical to congested's deutan/protan remap — re-verified by recomputation). The new test pins only base/fallback bytes; re-adding a route_tie remap to `modes` still passes CI. *Fix:* add `append(&pairs, [2]rl.Color{p.route_tie, p.state_congested})` to `a11y_separation_check`, and the same pair to `pair_list` in `tools/derive_a11y_palettes.py`.

**4. Shape pin tests tie_dash_on in isolation, not its use inside draw_tie_mark — deleting the call site renders a solid ring with tests green** [edge] — `app/render/assist.odin:505-509`

The dashed-ring test only evaluates `tie_dash_on(0..SEGS)` directly. Removing the `if !tie_dash_on(i) { continue }` guard yields a solid warning-shaped ring while all tests still pass (same empirical mutation as the blocker). *Fix:* pin the call-site linkage — factor a pure segment enumeration the test consumes.

**5. Palcheck separation oracle omits the state_congested vs route_tie pair under CVD modes** [tests] — `harness/palcheck.odin:96-106`

The exact gestalt pair this PR de-conflicts (tie vs congested) is not in the runtime CVD oracle. Re-adding a route_tie remap colliding with congested's pale-amber remap passes palcheck. *Fix:* same pair addition as W3 (they are one fix in two oracles).

**6. [unverified] Advisory test gate: CONCERNS** [tests]

No P0 gaps. P1 behaviour changes: hue change FULL (byte pins + tier loop + mutation proof), dash-pattern FULL (predicate pin, mutation-proven), CVD de-conflict PARTIAL → ~83%. Derive-script tool change (P3) has no direct test; overall ~80%. Raising the oracle pairs (W3/W5) and pinning mode-table route_tie absence lifts P1 to ≥ 90% and the gate to PASS.

### NOTES (10)

1. **derive_a11y_palettes.py can no longer regenerate the shipped modes tables from data/palette.json** [acceptance] — `tools/derive_a11y_palettes.py:182-193`. Spec says the script "owns the modes output"; after this change the tables are only reproducible via a hand-stripped copy. *Fix:* follow-up to strip `//` comments (or JSONC-tolerant parsing).
2. **Dashed-ring quad geometry duplicated verbatim from draw_ring_annulus instead of parameterizing it** [architecture] — `app/render/assist.odin:504-519` vs `app/render/spawn_fx.odin:384-402`. Table lookup, `j` wrap, CCW winding, two `DrawTriangle` calls — copy-pasted with only a dash predicate added. *Fix:* extend `draw_ring_annulus` with an optional segment predicate.
3. **Code comment hard-codes '6 dashes' / '30 deg' that depends on SPAWN_RING_SEGS = 36** [blind] — `app/render/assist.odin` (constants at :476-477). The annotations silently become false if `SPAWN_RING_SEGS` changes. *Fix:* drop the hard-coded numbers or add a compile-time assert.
4. **PR body claims a 225° hue distance, which is impossible on a 360° hue wheel** [blind] — `_pr_body_viscomm_tie.md:21-22`. Circular hue distance caps at 180°; 264° − 39° wraps to **135°** (recomputed: 134.62°). The stated margin overstates the actual separation almost twofold. *Fix:* state the wrapped distance in the PR body and any doc repeating the claim.
5. **derive_a11y_palettes.py cannot run against the shipped palette.json (// comments), so the derivation this diff edits is not reproducible** [codebase] — `tools/derive_a11y_palettes.py:97`. Pre-existing (font-overhaul added the comments) and disclosed in the PR body, but this diff edits the script's derivation logic. *Fix:* regex prefilter before `json.load`.
6. **draw_tie_mark re-implements the draw_ring_annulus quad-fan geometry instead of sharing it** [codebase] — `app/render/assist.odin:504-519`. The winding/culling lesson now lives in two copies in the same package. *Fix:* single-source via the extended `draw_ring_annulus`.
7. **draw_tie_mark omits the degenerate-radius/alpha guard its own precedent draw_ring_annulus carries** [edge] — `app/render/assist.odin:501-503` vs `spawn_fx.odin:385-387`. The precedent early-returns on `r_out <= 0 || r_in < 0 || col.a == 0`; the copy has no such guard. *Fix:* replicate the guard or call the shared helper.
8. **Warm-family classifier is weaker than a numeric hue-separation pin for route_tie vs state_congested** [tests] — `app/render/palette_polish_test.odin:152-155`. Only a boolean channel-ordering classifier pins AC3's separation; a magenta congested (~280°) stays within ~16° of the violet tie while passing. *Fix:* explicit `hue_degrees` delta ≥ 90° expectation, mirroring the pipe-tier loop.
9. **derive_a11y_palettes.py anchor removal and modes-table route_tie absence are untested** [tests]. No test pins that the shipped modes tables omit route_tie or that the derive script no longer emits it. *Fix:* palcheck presence assertion — `palette_apply_mode` leaves route_tie bytes unchanged across all three modes.
10. **draw_tie_mark draw path (annulus geometry, winding, caption) has no render-level test** [tests] — `app/render/assist.odin:505-519`. Shape coverage pins only the pure predicate and constants. Acceptable under the goldens-exclude-assists doctrine, but unverified. *Fix:* optional harness assist-draw check on r_in/r_out bounds under extreme `v.scale`.

### Reviewer Agreement

No multi-source merges (dedupe on title+location produced zero merges; all 18 titles distinct). Convergent evidence without formal agreement: the blocker (acceptance) and W4 (edge) describe the same vacuous-shape gap from the coverage and call-site angles; W3 (codebase) and W5 (tests) describe the same missing CVD oracle pair from the table and oracle sides.

### Rejected (1)

- "`pale` anchor in derive_a11y_palettes.py likely orphaned by this diff" [blind] — false positive: `pale` is still consumed by `remap["state_congested"] = pale` (tools/derive_a11y_palettes.py:161); the deleted route_tie remap line was never its only consumer. The state_congested remap sits outside the diff, invisible to the blind lens.

### Verdict

**NEEDS CHANGES**

One blocker: the shape mutation leg is vacuous against the actual draw path (solid-ring revert passes CI — proven twice by independent mutation probes); plus the 14.0° route_tie↔router_tier_high hue collision and the missing tie-vs-congested CVD oracle pair leave the exact de-conflict this PR exists to guarantee unguarded against regression.
