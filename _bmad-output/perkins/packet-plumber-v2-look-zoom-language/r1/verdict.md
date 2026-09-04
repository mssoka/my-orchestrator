# Perkins r1 — look(zoom-language) PR #105 — APPROVED (0 blockers)

**Reviewed sha:** d5dd5a6798508c2a15541da168ff040ba5ca90cd (base v2, merge-base 088cf00) · **Model:** zai-coding-cn/glm-5.3-flash · **Mode:** full 7-lens wave, headless

**Verification:** 20 raw findings from 6 completed lenses → every one re-verified against the worktree → 0 rejected, 0 unverifiable → 16 after dedupe (10 warnings, 6 notes, 0 blockers). failed_layers: **blind** (both attempts truncated pre-write — glm-5.3-flash long-context truncation; degraded, disclosed; the diff itself was read by all six remaining lenses).

## Verdict: APPROVED — READY TO MERGE

0 blockers. The four design-lock stories implement the ruled LOOK-SPEC faithfully; every load-bearing claim in the PR body reproduced clean under my own runs.

## Round-main independent verification (all run by me at the sha)

| Claim | My result |
|---|---|
| Golden re-bless inventory | ✅ 110 (L1) + 113 (L2) + 113 (L4) PNGs, exact per commit |
| Zero `.t1`/`.log.bin` drift | ✅ empty per-commit AND cumulative vs 088cf00 |
| `harness run` 49/49 | ✅ my own run green |
| 468 unit tests | ✅ core 280 + app 51 + app/render 114, my own runs green |
| palcheck all green | ✅ my own run — every LOOK §1-§3 pixel leg passed (laneless zero-counts ×3 rungs, width==table ×3, covenant-at-pixels ×3, shrink monotone 2427>285>67, dusk 0/258/118, warm-amber state shift) |
| Mutations M3/M6/M8 | ✅ re-run RED→GREEN: clamp bypass → 2 covenant tests RED; feed gate deleted → `reduced_motion_pins_the_breath` RED; floor 2.0→1.0 → `tier_ring_floor_is_two_screen_px` RED (got 1.32 want 2). Restored green, `git status --porcelain` empty |
| Pixel reads (inline vision) | ✅ growth/45000ms + dublin_board/30000ms + 3× crops: laneless solid strokes, ~2px tier rings, dusk glow ringing silhouettes, sprites-only Dublin + light family wash, gold CORE backbone |
| Constants vs claims | ✅ LINK_RATIO_CAP 0.5, rung tables, TIER_RING_FLOOR/FACTOR, DUBLIN_WASH_SCALE 0.45, DEFAULT_ZOOM 2.0, LINK_FINISH single-arm compile seam — all as claimed |
| Parked-fork fence | ✅ no board/packet-shape/HUD/queue-encoder surface touched (file list + board golden shift only from the node ladder) |

## Warnings (10)

1. **[architecture+acceptance+edge] Assist route-glow path geometry from the UNCAPPED width** — `assist.odin:435-441`: the glow's *width* rides `link_width_capped` but its `wire_path_compute` call passes `band_world`; the drawn ribbon (`wire_paths_compute`) uses the capped band. Where the clamp bites, glow and stroke follow different polylines. Flags-on path only (7.5 ships OFF).
2. **[edge] Fan-stub unit confusion** — `view.odin:1047-1064`: screen-px `band` passed to world-px `end_apex`; `stub_w = min(world, screen)*0.6` then scaled again in `draw_fan_stub`. Correct at scale 1.0, wrong elsewhere (fan only, flags-on, count>1).
3. **[edge+architecture] Covenant cap collapses to 0 on the sprite-fallback path** — `sprites.odin:297-306` + `view.odin:744-757`: `node_draw_size_world` has no primitive branch (unlike `puck_rim_world`/`building_foot_world`), so on the documented load-failure path any router-ended bundle draws zero-width. The PR's deferred line ("ignores the rung tables") understates it.
4. **[tests] wire_path_test fixtures are the vacuous cap-0 class** — `sprites.ok=false` ⇒ `link_width_capped` returns 0 ⇒ `wire_paths_compute` unit-exercised only at zero width; the de-vacuated-bbox fix landed in look_l1_test but not here.
5. **[tests] Covenant consumer reversion unpinned — mutation-proven this round** — I reverted the crisis outline to `band_world`: 114 tests + palcheck ALL GREEN. The M-legs pin the derivation, not its consumers.
6. **[tests] zoom directive guard edges untested** — happy path rides `dublin_board.dem`'s golden (green in my run); NaN/out-of-band legs + rung derivation have no direct test.
7. **[tests] camera_update→zoom_rung wiring line untested** — `pullback_test` never asserts `zoom_rung`; palcheck/harness set the rung directly, bypassing the wiring.
8. **[codebase] draw_bundles header still teaches the retired 3.3 three-lane canon as current law** — the diff retired the stripes but left the superseded ruling's doc above the laneless code.
9. **[architecture] zoom_rung stored on View though derivable** — three write sites (all currently consistent, verified); a drift trap for future zoom paths.
10. **[tests] Advisory test gate: CONCERNS** — P0/P1 mutation-pinned + pixel-gated; the concerns are the P2 gaps above. None gate this merge.

## Notes (6)

band_width dead + stale ONE-definition doc · node_draw_size_world parallels the clearance helpers ×2 without their fallback · dusk-dot radius uses the house footprint for all non-DC roles (doc says live footprint) · PR body's stale ±2px tolerance (shipped gate is ±1.0) · `draw_bundles` discards its `flow` param · count_exact doc stranded above measure_color_run.

## Reading list for the fix round (non-blocking)

The four flagged-on-code warnings (1-3, 8) are one coherent follow-up: thread the capped band through the assist/fan consumer surfaces, give `node_draw_size_world` the primitive branch, rewrite the draw_bundles header. The five coverage gaps (4-7 + gate) are one test-only follow-up. Neither gates the merge; the canon surface (LOOK-SPEC locks) is fully honored.

— Perkins r1, glm-5.3-flash, 2026-08-27. CI billing-block noted once per standing ruling: remote CI is not the gate; local ground truth (above) is.
