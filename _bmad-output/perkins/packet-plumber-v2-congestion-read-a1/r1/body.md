## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-congestion-read-a1 · **Reviewed sha:** df147854 · **Reviewers:** 7/7 completed
**Verification:** 20/21 reviewer findings confirmed against the code — 1 discarded as false-positive; consolidated to **13 unique** (7 cross-lens duplicates merged)

**Verdict basis — independent mutation + mechanical verification (not trusted from the PR):**
- **Delete-the-bump mutation leg: RED then GREEN, re-run independently.** Deleting the A1 floor from `congested_halo_width` fails the unit law test ×6 (8.5/10.5/14.5/11/19 under floor; 14.5≠24) and palcheck §8 legs (a)/(b)/(d) at exactly the predicted 19px-vs-floor-24. Restored → 116/116 render tests + palcheck all green; worktree byte-identical to the reviewed sha after restore. The gates are non-vacuous: §8's premise pin proves the floor dominates the +5 bump at the fixture rung (19 < 21).
- **Calm covenant holds in both mutation states:** §8(c)/(e) halo/cap leak legs 0px in calm + routed-calm, corpus **49/49 byte-exact** (T1+T2+replay — every un-re-blessed golden byte-identical, ODN-1 sim/log untouched).
- **Suites:** app/render 116/116 (incl. the 2 new A1 pins) · app 51/51 · core 280/280 · palcheck all green.
- **The READ is measurably back at every rung** (strip CSVs, 50/50 frames each): congested-link width 8→12px @z1.0, 10→16px @z1.4, 18→22px @z2.0; the juice telegraph now oscillates 7↔14px where before was static 7.
- **Re-bless scope is honest:** PIL pixel-diffs of the re-blessed PNGs vs base `03dd6f8` — warn@45s is ONE 279×12 link band; juice/qos_contention/surge/pause/a11y_reduced diffs (265–2110px) all confined to thin link-corridor bands = the A1 emphasis layer only. No HUD/node/full-frame churn. (This also **rejects** the blind lens's "calm byte-identity unverified" concern — the corpus + §8 leak legs prove it.)

### Blockers (0)
None.

### Warnings (6)
1. **[blind+edge+architecture+acceptance] Palcheck §8 routed legs (d)+(e) index `pipe_congestion` without the `testing_lvl_ok` guard** — `harness/palcheck.odin:1461-1490`. A premise-broken fixture panics at (d) instead of failing clean (the resize is gated identically), masking the summary. Wrap (d)+(e) like (a)–(c).
2. **[blind+codebase+acceptance] `look_l1_test` feeds world-px band values into `congested_halo_width`'s screen-px parameter** — `app/render/look_l1_test.odin:271-302`. The draw site passes screen px (`link_width_capped(...) * v.scale`); the test's pairs + comments use the world reading (its own "max(9+10, 24)" doesn't match the (4.5, 2.0) call). Numerically insensitive today (the floor dominates every pair; the z1.0 pair is exactly faithful) — the law pin holds, but the stated interpretation will mislead the next retune. Pass `world × scale`.
3. **[architecture] Zoom band 1.0..4.0 restated as literals in three parsers** — `harness/main.odin:212`, `harness/motion_strip.odin:114`, `harness/demo.odin:643` — while `CAM_ZOOM_MIN/MAX` exist in `app/render/camera.odin` and the harness already imports the render package. Derive the three guards from the constants.
4. **[codebase] §8 end-cap leak scan can never fail** — `harness/palcheck.odin:1455`. The cap circle (~12px radius) draws at the node center in the bundles pass; the node sprite (drawn after, ≥ ~40px tall at ACCESS z2) covers it entirely — the scan is vacuous by geometry. Scan outside the sprite footprint or drop the sub-scan. (The section's load-bearing legs are live — mutation-proven above.)
5. **[tests] Motion-strip capture-altitude behavior has zero automated coverage** — the `zoom=` override parse/band/duplicate-token validation in `main.odin:204-215` + `apply_capture_zoom` have no unit tests (grep-verified). Small parse-path test closes it.
6. **[tests] Advisory test gate: CONCERNS** — P0 (the A1 law) is heavily covered; the motion-strip override gap is P2 → CONCERNS, not FAIL.

### Notes (7)
1. **[security+blind]** Out-of-band `zoom=` override silently ignored in `run_motion_strip` while the CLI caller usage-errors the same value — reachable only by a future non-CLI caller; align or document the sentinel.
2. **[architecture+blind]** The 0.57/0.43 blend is restated in both `draw_bundles` branches (and again in §8's `halo_blend`) despite the diff's own ONE-derivation doctrine for the width — hoist a draw-side blend helper. (§8's copy may stay as an independent measurement oracle.)
3. **[blind]** §8 `testing_lvl_ok := ok_ps && found_bi` omits `perr8 == .None` which its own premise check asserts — a pipeless fixture would fail confusingly (never false-pass). Fold it in.
4. **[acceptance]** Doc-hygiene constraint met by substitution: LOOK-SPEC.md is untracked so the PR can't carry the line; the amendment is on the tracked LOOK §3 canon + deferred-work routes the mirror. Acceptable — land the mirror when the file is tracked.
5. **[tests]** §8(e) routed-calm pins leak-only, not width — asymmetric vs the inline calm pin. Add the width scan.
6. **[codebase]** Three §8 continuation comments carry an extra tab — cosmetic.
7. **[blind]** `measure_color_run`'s contract comment is orphaned above the inserted `scan_col_v` — move it back.

### Reviewer agreement
- **§8 routed-branch unguarded index** — 4 of 7 lenses (blind, edge, architecture, acceptance) independently flagged it. Highest-confidence finding of the round; test-harness robustness only.
- **The law-test units mislabel** — 3 lenses (blind, codebase, acceptance).
- Both are fix-in-follow-up grade; neither touches the shipped render path.

**Verdict: READY TO MERGE** — 0 blockers. The A1 emphasis floor is real, tuned inside the ruled 10–14px envelope (12.0), byte-additive to the calm covenant (mutation-proven both ways), ODN-1-safe at corpus scale, and the congested READ is measurably restored at every zoom rung. Address the warnings (the §8 guard + the units comments first) in a follow-up fold — I re-review automatically on the new sha.

_CI note: the verify legs show the billing-block signature (runners never started) — note-only per standing ruling; the local suites above are the merge ground truth._

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
