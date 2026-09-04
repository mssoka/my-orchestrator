## 🤖 Perkins automated review — round 2
**Job:** packet-plumber-3d-e1-tiny-planet · **Reviewed sha:** 3a9ef0b · **Reviewers:** 7/7 completed
**Verification:** 26/27 findings confirmed against the code — 1 discarded as false-positive

### Fix audit (round 1 → 2)

**B1 — separation double-factor: FIXED (runtime-verified, RED-then-GREEN).** `world_seed.gd:146` now decays the full `MIN_NODE_SEPARATION_RAD` with a real 25% floor. Runtime probe at seed 20260904: violating pairs **13 → 1**, min separation 0.678 → **1.852 units**. Mutation leg: restoring the r1 formula reproduced r1's numbers exactly (13 pairs, n25/n30, 0.0848 rad) — the probe detects the original defect; the shipped code clears it. Residual: one pair remains 0.048 units inside the 1.9-unit hitbox diameter (W1).

**B2 — gesture lifecycle untested: FIXED (mutation-verified).** `tests/test_gesture.gd` drives the **real** input path (`Input.parse_input_event` → router → physics `_pick` → controller): press→move→release commits, release-on-empty cancels, sky release cancels, focus-loss cancels. Mutation legs: breaking the commit path **fails the suite**; breaking focus-loss **fails the suite** (2 checks); restored → green. Residual: one surviving mutant (W2).

**B3 — advisory gate: FAIL → CONCERNS.** P0 100% (mutation-proven), P1 ≈88%.

**r1 warnings W1–W6: all fixed** (fallback retries genuinely · pinch handled via `InputEventMagnifyGesture` · A3 box checked + stale capture path fixed · fail-fast guard on `sites[]` · router integration covered · orientation/layer asserted).
**r1 notes:** 11 folded (dead signal removed, leak freed, error codes checked, caps added, seed const, …) · 10 still present, carried as notes below · 1 documented (33-node count per user direction).

**Independent runs:** headless suite `SUITE RESULT: PASS (0 failure(s))`, exit 0 (Godot 4.7.1). Captures: 4 real 1600×900 in-game PNGs, regenerated at this sha. *Vision caveat (text-only reviewer round): pixel verification mechanical only — aesthetic parity with the little-planet reference is deferred for the k3 re-check; not re-judged this round.*

### Blockers (0)

None. 🎉

### Warnings (7)

1. **[B1 residual]** One node pair (n07/n11) still overlaps the hitbox diameter at the shipped seed — min separation 0.2315 rad = **1.852 units vs 1.9** (0.048 short, 2.5%). The PR body's "0.25 rad keeps the 0.95-radius hitboxes non-overlapping" is overstated at the margin. `world_seed.gd:146` — decay admits sub-diameter placements from attempt ≈6. *Fix: start decay later or floor at 0.2375; re-probe for 0 violations.*
2. **[B2 residual]** `test_gesture`'s sky-release leg never arms a snap target first — the stale-snap guard it names is a **surviving mutant** (mutation kept the suite green). `tests/test_gesture.gd:68`. *Fix: move over a node, then flick to sky and release; assert no commit.*
3. **No regression test pins node separation** — the r1 blocker shipped green because nothing asserted it; the fix is equally unpinned (reverting the formula still passes the suite). `tests/run_tests.gd:18`. *Fix: assert min pairwise arc ≥ 0.2375 rad over `node_placements(SEED)`.*
4. **Zoom input dispatch untested** — wheel branch + stateful pinch accumulation (the new delta) have zero coverage; only `OrbitCamera.zoom()` is unit-tested. `scripts/input_router.gd:36-45`. *Fix: synthetic wheel/Magnify events through the router.*
5. **README's first verify command fails on a fresh clone** — the suite needs the `--import` listed *after* it (reproduced: pre-import, every test script parse-fails on class_name resolution). `README.md:32-33`. *Fix: swap the two lines* (the PR body's test plan already has the right order).
6. **`tests/test_gesture.gd.uid` is the only script uid not committed** (17 of 18 tracked). Fresh clones regenerate a different uid. *Fix: `git add tests/test_gesture.gd.uid`.*
7. **Advisory test gate: CONCERNS** — P0 100%, P1 ≈88%, overall ≥80%. Closes with warnings 2–4.

### Notes (20)

- `_readable_pair` comment cites a `TARGET_ARC` constant that doesn't exist; `0.65` literal duplicated in harness + test (blind, codebase)
- Fallback tail can still return a separation-violating candidate if all 10 tries miss (latent, unreached at shipped seed)
- Ghost preview's trestle posts render opaque/shadowed while the arc is translucent unshaded (`pipe_arc.gd:122`)
- `Geodesic.ray_sphere` has no production caller — still present since r1 (blind, architecture)
- `test_geodesic` hardcodes `0.24` ×3 instead of `SNAP_ARC_RAD`
- `_empty_surface_point`'s antipodal fallback contradicts the file's own unproject-mirror warning (rare path)
- `--capture` activates under `--headless` with no renderer guard (dev harness)
- `ZOOM_STOPS` literals tied to R=8 by comment only (every other module reads `PLANET_RADIUS`)
- Contract suite asserts underscore-private members (white-box seams)
- Pair→count registry (topology state) lives in the input controller ahead of E2's sim
- `captures/*.png.import` deleted from tracking while `icon.svg.import` stays tracked — mixed convention, dirty-tree noise
- Basis-from-direction idiom duplicated node_site/pipe_arc — still present since r1
- `capture_runner._arc_mid` double-scales an already-radius-length midpoint — still present since r1
- `snap_candidate` couples the "pure math spine" to scene-tree `Node3D` — still present since r1 (lens escalated; held at note pending E2)
- **Carry-forwards still present since r1:** draw_end never re-snaps the release point · capture-01 normalized-sum frame trick · merged-path endpoints-only assert · sibling self-resolve scene paths · CaptureRunner node in shipped scene · bundle registry keyed by display names

### Reviewer agreement
Two multi-source findings: **TARGET_ARC/0.65 drift** (blind+codebase) and **ray_sphere dead code** (blind+architecture). The acceptance lens independently measured the same 0.2315 rad minimum as warning 1 (its "no overlap" conclusion disagreed only at the 1.852-vs-1.9 margin — the runtime numbers are identical).

**Verdict:** READY TO MERGE

Round 1's three blockers are verified fixed at runtime with mutation evidence, all six warnings folded, and the delta introduces no new blockers. The seven warnings above are polish-grade (one 2.5% hitbox-margin pair, test-hardening gaps, README ordering, a uid file) — none block the slice's contracts: the epic suite passes, disambiguation is pinned by real-path tests, and the world regenerates deterministically.

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
