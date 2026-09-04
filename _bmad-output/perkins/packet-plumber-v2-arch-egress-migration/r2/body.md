# Perkins r2 — fix-audit: APPROVED ✅

**PR:** #104 (base v2) · **Reviewed sha:** `c9adb37df225395fa333e8b58bba9bc627755763` (head re-verified unchanged before posting) · **Model:** zai-coding-cn/glm-5.3 · **Verdict rule:** 0 blockers → APPROVE

**Diff disclosure (canonical-diff substitution, same as r1):** `gh pr diff` 406s on this PR (>20 000-line cap); the reviewed diff is `git diff 7ad48f9..c9adb37` at the exact merge-base — 54 796 lines. Chunking: core chunk (core/ 19 files + tools/lint.sh + harness/palcheck.odin, 2 884 lines) + app chunk (app/ 7 files, 421 lines) each ran the FULL 7-lens wave; goldens (70 files, 51 274 lines) verified MECHANICALLY — the r1→r2 delta commit `c9adb37` touches **zero** golden files, so the r1-verified per-story re-bless inventory (all six rows EXACT, set-equality proven) carries forward unchanged.

**CI caveat (standing ruling):** remote CI billing-blocked; local suite is ground truth, run by Perkins at the sha — core 280/280, app 49/49, app/render 100/100, `tools/harness.sh palcheck` all green, lint 8/8 gates. Worktree porcelain EMPTY after all mutation legs. (Invocation note: `odin run harness -- palcheck` without the sw-renderer shadow fails 17 capture checks in a headless pane — the sanctioned path is `tools/harness.sh palcheck`; not a code defect.)

**Vision caveat (non-k3 round):** pixel verification mechanical only; aesthetic verdicts deferred for k3.

---

## 1. Fix audit — every r1 finding re-read at c9adb37 (the round's lead)

| r1 | Severity | Status | Evidence |
|---|---|---|---|
| B1 QoS panel direction-row overflow | blocker | **FIXED** | Three stacked lines (label/fwd/rev) from pure helpers (`qos_panel_rows/qos_qd_row/qos_qd_line_y/qos_qd_lane_x`); panel rows +3; geometry pin at every scale step. **Mutation re-run (Perkins): pitch 34→200 → RED ×6 scale steps.** |
| B2 AV-7 max-never-sum unpinned | blocker | **FIXED** | `test_pipe_congestion_max_never_sum`: 5 fwd + 1 rev, amber@1/cleared@9 + explicit Pipe_Critical-never belt. **Mutation re-run: max→sum → RED (Pipe_Critical fired ticks 1+9 — the exact discriminator).** |
| B3 AV-4 util MAX unpinned (2 seams) | blocker | **FIXED** | Asymmetric 60/30 windows + both-saturated phase at BOTH seams (`stats.odin:233` row + `port_util_pct` reads). **Mutation re-run: sum → RED ×2 ("got 90" / "got 200").** |
| B4 residency regression pins ×2 | blocker | **FIXED** | Layout-reset pin (same-count renumber + REAL next tick) + staleness-fold pin (idle tick+W+1 reads 0, in-window control reads 7). **Mutations re-run: guard dropped → "7 phantom packet-ticks" RED; fold dropped → "frozen stale sum" RED.** |
| W1 residency.win dual bookkeeping | warning | **FIXED** | `win` deleted everywhere — struct field, init/destroy, layout, record pass, read guard (now `r.keys`), shadow_clone list. Grep: zero references. |
| W2 packet_bandwidth unbounded multiplicand | warning | **FIXED** | 1..4096 bound at load (catalog.odin:868) with the wrap-math comment. |
| W3 >4096 rejection unpinned | warning | **FIXED** | Both branches pinned: demand 4097 + bandwidth 0/−5/4097 rows in catalog_test. |
| N1 NOC id gutter too narrow | note | **FIXED** | Gutter 52→74, pitch 104→96, bar 64→60, measured bare-pair fallback; zero pixel drift (fixtures single-digit). |
| N3/N4/N5 stale comments | note | **FIXED** | S1 staging comment rewritten (ladder completed); transit_ticks docs merged; crisis scan comment re-keyed. |
| N6 self-comparing expect_value | note | **FIXED** | Two-reads-agree stability pin with comment. |
| N9 lint gate 8 scope | note | **FIXED** | Scans `app/ harness/` now. |
| N2 orphaned undirected twins | note | **still present — BY DESIGN** | Spine-authorized legacy view; now explicitly documented at the twins (retire with the render heists). |
| N7 drive-by palette-string edit | note | **still present — disclosed** | Cosmetic; PR-body-disclosed. |
| N8 lint gate 8 vs LB-gate deviations | note | **still present — not claimed** | No comment-stripping/Ada_Case bypass; note stands. |
| N10 panel+NOC draw surfaces untested | note | **PARTIALLY FIXED** | Panel half: B1 geometry pin landed. NOC half: still uncovered → carried as W-new-3 below. |

**All 4 blockers fixed with independently re-run RED mutation legs; W1–W3 and the claimed notes all verified in code.** The vacuous-pin class is closed.

## 2. New findings (verified against the worktree; every finding re-read)

### BLOCKERS (0)

None.

### WARNINGS (3)

- **W-new-1 · QoS queue-depth block text sizes are raw 14, not hud-scaled** `[acceptance, architecture]` — `app/qos_panel.odin:431,439,448`. Every sibling panel surface passes `rnd.hud(&app.view, 1x)` for size (7 sites); the qd block passes literal `14`. Identical at the default scale (hud(k)=k at 1.0) but mis-scales vs the rest of the panel at non-default UI scales; at small scales positions compress (pitch 34→~25) while text width stays 14 px — column collision risk the B1 position pin cannot see. Fix: `rnd.hud(&app.view, 14)` at the three sites.
- **W-new-2 · Q-row CSV literal unpinned** `[tests]` — `core/stats_test.odin` (`test_stats_csv_literal_rows` pins G/C/P/D only; producer `stats.odin:372`). The Q row is the NEW row kind this migration adds; a column swap in its printf passes every test (live and replay carry the same wrong bytes) — exactly the guard class the literal-pins test exists for.
- **W-new-3 · NOC queue-row re-key ships untested** `[tests]` — `noc_queue_id_label` + the N1 gutter constants (`NOC_Q_LANES_X/PITCH/BAR_W`, `NOC_Q_LABEL_MAX` fallback) have no automated pin (draw-level surface, no golden draws the NOC section). Carries r1-N10's NOC half forward.

### NOTES (13)

1. Spine names `egress_port_of(packet)`; code ships the resolution decomposed (`port_dir_of_packet` + `egress_router_of_port` + `bundle_of_pipe`) `[acceptance, architecture]` — naming-convention deviation only; the twins the spine DOES name (`port_lane_count/ready/caps`) all exist.
2. Spine Determinism row says the serve pass enumerates "(bundle slot asc, **heading asc**)"; the pinned order is dir-ascending = heading node-id DESCENDING for dir 0 `[acceptance]` — non-load-bearing under independent budgets (the spine's own words); a one-word spine/comment alignment.
3. `bundle_tx_window` lacks the composite-index guard its write twin `bundle_tx_record` has (dir ≥ 2 would read OOB) `[blind]` — unreachable via current callers (all pass PORT_DIR_* constants); consistency nit.
4. `serialize.odin` comment "old logs replay unchanged" is format-compat only — old contended logs replay to numerically different outcomes (S2/S3/S4 disclosures) `[blind]` — wording nit; the file's own 4.2 precedent paragraph shows the intended convention.
5. `qos_qd_lane_x` comment references phantom symbol `qos_qd_x0` `[architecture, codebase]`.
6. `noc_pipe_rate` doc still references the deleted compact variant + the queue rows' rate block that this migration dropped `[architecture]`.
7. Queue rows drop the line-rate glyph — documented in-code (AD-1: ports paint depth; rate stays on pipe rows) but it IS a visual change beyond "minimal mechanical" — flag to the link-vocab render heists `[acceptance]`.
8. `noc_queue_rows` vs the draw loop diverge at `amber_pct==0` (count predicate guards, draw predicate doesn't) `[blind]` — pre-existing shape carried into the re-keyed code; unreachable at game canon (70).
9. Bare-form NOC id fallback never width-checked at draw (the full form is measured; the fallback isn't) `[edge, blind]` — needs 4-digit router ids to overrun; unrealistic at current scale.
10. QoS panel fwd/rev labels bind positionally to the core enum order (`dirs[0]`↔`PORT_DIR_LO_TO_HI`) — an enum reorder silently swaps the labels `[tests]`.
11. r1-N7 carry-forward: drive-by punctuation edit in `palette_polish_test` (disclosed).
12. r1-N2 carry-forward: orphaned undirected twins (documented legacy; retire with the render heists).
13. Advisory test gates: **PASS** both chunks (P0 100 %, P1 ≥ 95 %; mutation legs proven per story + re-proven by this round).

### Reviewer Agreement (multi-source)

W-new-1 (acceptance+architecture), notes 1, 5, 9 (each 2 independent lenses).

## 3. Verification record

- **Lens wave:** 14/14 valid (7 lenses × 2 chunks; 2 panes revived once after a 429-1302 burst — disclosed; blind-app's JSON had a control-char artifact, repaired by strict-tolerant parse, content intact). 24 raw findings → **3 rejected as false-positive after code re-verification** (blind "zero-unit serviced" — the `avail==0` loop break makes the mechanism impossible; tests "shed-ladder cross-direction unpinned" — Perkins mutation to bundle-wide scanning FAILS a test, discriminator exists; tests "crisis resolve dir-keying unpinned" — wrong-dir mutation fails 10 tests). 21 survived.
- **Perkins mutation legs (all RED→restore→green; porcelain empty at end):** B2 max→sum ✅ · B4a guard-drop ✅ · B4b fold-drop ✅ · B3 sum ✅×2 · B1 pitch ✅ · W1-probe bundle-wide ✅(fails) · W2-probe wrong-dir ✅(fails ×10).
- **Local gates at c9adb37:** core 280/280 · app 49/49 · render 100/100 · palcheck (harness.sh) all green · lint 8/8 · `git status --porcelain` EMPTY.

## 4. Verdict

**APPROVE.** All four r1 blockers are fixed with non-vacuous, mutation-proven pins; the warnings/notes folds verified in code; zero new blockers. The three new warnings (hud-scale the qd text, pin the Q-row literal, pin the NOC gutter) are small test/style follow-ups — none block the merge; they route naturally to the render heists or a follow-up sweep.
