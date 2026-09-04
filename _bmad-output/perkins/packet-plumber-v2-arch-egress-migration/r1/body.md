# Perkins r1 — arch(egress): store-and-forward queue migration — MAJOR REWORK (4 blockers; all fixes small)

**Reviewed sha:** `1e9c783e7a088d48e44d6bd5f67873e0109d8454` (head re-fetched pre-post: unchanged)
**Model:** zai-coding-cn/glm-5.3 · **Diff:** 54,356 lines (MEGA-DIFF protocol)
**CANONICAL-DIFF SUBSTITUTION DISCLOSED:** the GitHub API 406'd on size (>20,000-line cap); the reviewed diff is `git diff 7ad48f9..1e9c783` generated locally at the exact merge-base (verified: merge-base == `7ad48f9`, byte-exact reconstruction of the saved canonical diff).

## Chunk map (deterministic split)

| Chunk | Files | Lines | Treatment |
|---|---|---|---|
| `core/` sim source | 17 | 2,577 | full 7-lens wave |
| `app/`+`harness/`+`tools/` | 8 | 289 | full 7-lens wave |
| goldens (26 `.t1` + 44 png) + docs | 72 | 51,404 | MECHANICAL bulk verification (below) |

All 14 lens runs (7 lenses × 2 code chunks) completed; **0 failed layers**. 33 raw findings → 1 rejected (timing artifact: a lens read `flow.odin` during this round's own ~40s S3-mutation verification window; final tree verified clean) → 32 verified → 20 unique after dedupe/merge. Every finding independently re-verified against the worktree at the sha.

## Local ground truth (billing-block CI disclosed once — standing ruling)

All gates run locally by this reviewer at the reviewed sha: `odin test core` **276/276** · `odin test app` **48/48** · `odin test app/render` **100/100** · palcheck **green** · lint **8/8 gates** (incl. the new gate 8) · harness T1 **49/49 bit-for-bit** · `stats-check` live==replay byte-identical (spawn_feel / qos_contention / estate_surge) · `drift-check` **353/353 rejected**. Worktree `git status --porcelain` **EMPTY** after all mutation legs.

## Independent mutation verification (the house bar)

- **S3 leg (mandated):** unwire `bandwidth_demand` → **RED** — 6 tests fail incl. `test_demand_wiring_streaming_transit_16_ticks` (which even names the mutation: "got 9 — the demand-unwired mutation reads 9"). Restore → green. ✅
- **S2 leg (mandated):** collapse the direction split (pool the serve budget) → **RED** — `test_full_duplex_direction_independence` fails with the exact PR-body signature "6/12 arrived — the shared-budget collapse". Restore → green. ✅
- **D6 proof:** LOG_VERSION stays 6; **0/49** `.log.bin` action logs changed across the branch; 49/49 replay bit-for-bit; `stats-check` byte-identical incl. spawn_feel; action-log round-trip test green. ✅
- **4.2 crisis hysteresis:** `CRISIS_RESOLVE_MARGIN :: u32(2)` verbatim-unchanged (comment-only diff hunks); margin tests pass in the 276. ✅
- **Four vacuous-pin mutations** (B2–B4 below): each passes the entire 276-test suite → blocker class per the standing bar.

## Bulk verification (goldens — MECHANICAL, zero anomalies)

Per-story re-bless inventory vs actual commit history — **every number EXACT**: S1 `t1=0/png=0`, S2 `16/19`, S3 `24/43`, S4 `23/6`, S5 `0/0`, swarm-fold `0/0`. Set equality holds: the union of per-story re-bless sets == the final changed set (26 `.t1`) — **no golden changed outside the inventory**. 49−16=33 untouched at S2 as claimed. The serialized crises section is untouched (`w_crises_section` zero diff hunks); the +1 direction byte rides the existing tag-conditional `Event.direction` slot on regenerated events only — consistent with AD-6's enumerated exemptions.

## Spine compliance (AD-1..AD-8)

AD-1/2 (port identity, derived encoding) ✅ · AD-3 (three integer terms; F2 identity pinned `(a)+(b)+(c)=delivery−spawn`, (b)=7) ✅ · AD-4 (E9 per-(port,lane) bound-6, `Packet_Dropped.target` stays bundle id, cooldown gains direction) ✅ · AD-5 (full-duplex budgets, tx ring per (bundle,direction)) ✅ · AD-6 (LOG_VERSION 6, all derived) ✅ · AD-7 reads contract **structurally shipped, pins incomplete → B1–B3** · AD-8 (era/growth/ECMP untouched) ✅. Lint gate 8 enforces AD-1's negative space.

## BLOCKERS (4)

### B1 — QoS panel per-direction depth row overflows the 300px plate (~130–160px, unclipped) `[acceptance, architecture, codebase, edge]`
`app/qos_panel.odin:404-423` — plate right edge x=312 (`QOS_PANEL_W :: 300`); the row starts after the ~154px label, then consumes 142px per direction (30 + 3×34 + 10): dir 1 ends ≈326, dir 2 ≈470. `draw_text` → `rl.DrawTextEx` with **no scissor**. `draw_qos_panel` draws whenever a pipe is selected — every panel-open frame paints UI onto the map. (T2 goldens never draw the panel, so the corpus doesn't catch it — this exact seam is N10.) 4 independent lenses converged; verified mechanically (geometry, not aesthetics — vision caveat n/a).
**Fix:** reflow within the plate (two stacked rows / compact columns / wider plate) + a geometry pin.

### B2 — AV-7 max-never-sum rollup UNPINNED (warnings) `[blind, tests]` — mutation-proven
`core/warnings.odin:236-240` — mutating `max(lo,hi)` → `lo+hi` **passes all 276 tests**. `test_pipe_congestion_lane_bound` loads only one direction (max==sum there). A ratified AD-7/AV-7 rule with zero failing mutation = blocker per the house bar.
**Fix:** bidirectional-load fixture pinning the pipe level to the WORSE port.

### B3 — AV-4 util MAX-over-directions UNPINNED (stats + read fn) `[tests]` — mutation-proven
`core/stats.odin:233` + `core/egress_test.odin:591-593` — mutating `row.util_pct = max(u_lo,u_hi)` → sum **passes all 276 tests** (the pinned fixture's reverse port reads 0 in-window, so sum==max); `port_util_pct`'s only assertion is the pre-traffic zero — the comment names "saturated reads 100, never 200" but never asserts it.
**Fix:** both-directions-saturated fixture: per-direction 100, never a pair-200; a stats row where both directions are non-zero in-window.

### B4 — Residency ledger regression pins MISSING for both swarm-claimed fixes `[tests, blind]` — mutation-proven ×2
`core/flow.odin:809-811` (layout reset) + `:906-910` (staleness fold) — dropping the `layout_gen==topo_gen` guard **passes the suite** (the same-count renumber leak the swarm says it fixed regresses silently); dropping the read-time staleness fold **passes the suite** (idle keys would read frozen sums — the exact defect the PR claims folds at read). The tx ring has `test_bundle_tx_window_expiry_and_reuse`; the residency ledger's mirror is absent.
**Fix:** mirror the tx-ring test: topology-edit → ledger resets; idle > window → reads 0.

## WARNINGS (4)

- **W1** `[blind, architecture]` — `residency.win` rolling-sum maintained per packet-tick but **never read** (reads walk raw slots) — dual bookkeeping that can silently drift. Delete it or consume it (ODN-18).
- **W2** `[edge, blind, security]` — the u32 wrap guard bounds `bandwidth_demand` (1..4096) but **`packet_bandwidth` has only a `>0` check** — the other multiplicand in `demand × packet_bandwidth` is unbounded at the catalog seam (`core/flow.odin:601`).
- **W3** `[tests]` — the new `bw > 4096` rejection branch has **no test** (the `<1` branch is tested; grep `4096` in catalog_test: zero matches).
- **W4** `[tests]` — Advisory test gate: **CONCERNS** (P0 100%, P1 ~85–89% — the gaps are exactly B2–B4 + W2/W3; landing them flips the gate to PASS).

## NOTES (11)

N1 NOC `R<router>><peer>` label vs the ~46–52px gutter at 2–3-digit node ids `[architecture, edge]` · N2 orphan undirected twins (spine-authorized legacy view — retirement set for the heists) `[architecture, codebase]` · N3 stale S1 staging comment · N4 stacked duplicate `transit_ticks` doc · N5 comment refs deleted `crisis_find_saturated_bundle` · N6 tautological self-comparing `expect_value` (egress_test:202) · N7 em-dash drive-by (disclosed ✓) · N8 lint gate 8 vs LB-gate precedent (no comment-strip/Ada_Case/self-test — empirically verified) · N9 gate 8 scans `app/` only (harness/ seam) · N10 QoS-panel + NOC-row draw surfaces have no automated coverage (B1's seam) · N11 advisory gate PASS (app chunk).

## Reviewer agreement (multi-source, highest confidence)

**B1 (4 sources)** · W2 (3 sources) · B2, B4, W1, N1, N2 (2 each).

## Verdict

**MAJOR REWORK** — 4 blockers (1–3 → request-changes; 4+ → major rework, mechanical threshold). Honesty note: all four fixes are small (one panel reflow + three regression pins — no architectural rework); the substance of the migration (S1–S5, spine compliance, golden discipline, D6 proof) verifies clean end-to-end, including both mandated mutation legs and the full bulk inventory. Fix B1–B4 (+ W3 while you're in the catalog tests) and this should approve in r2.

*— Perkins r1, glm-5.3, 14/14 lenses, 0 failed layers. Vision caveat (non-k3 round): pixel verification mechanical only; no aesthetic verdicts (none were needed — B1 is geometry).*
