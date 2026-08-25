## 🤖 Perkins automated review — round 4

**Job:** packet-plumber-v2-spawn-feel · **Reviewed sha:** `9c0f11e` · **Reviewers:** 7/7 completed
**Verification:** 28/30 findings confirmed against the code — 2 discarded as false-positive (details below)

### Fix audit (r1 blockers — both verified FIXED on the true settled head)

- **B1 (pipe-highlight unit mix) — FIXED.** `spawn_fx_draw_highlight` now compares pure tile units both sides (`rad := f32(SPAWN_HIGHLIGHT_RADIUS_TILES)`, comment cites the r1 finding). Pixel-verified: the r1→post-fix golden delta on `spawn_feel/04000ms` is a 305×6 band at x 656–960, y 357 — exactly the documented removed far-pipe band; all non-highlight frames byte-identical.
- **B2 (vacuous predictor pin) — FIXED, genuinely non-vacuous.** The pending command is now a legal router place at (13,6)@t77 with a materialization assert (3 junctions), `!replay_error`, predict==actual, an anti-vacuity assert (no-pending prediction must land elsewhere), and a negative leg (out-of-separation place rejected on both sides, prediction still matches).

**Rebase delta (post-#82/#83):** `sprite_blit` takes both #83's `Shadow_Spec` and the reveal `tint`; the router puck keeps `shadow_for_puck()` with the default WHITE tint → ink identity (`spec.ink×255/255`) — both callers verified, #83 shadow geometry intact. Golden audit (mechanical): r1→fix delta = the B1 band + #82 trail rings only (both documented); fix→r4 = the global #83 scale/shadow change (~674k px whole-map) with the telegraph ring centroid at **(351.5, 263.5) byte-identical across all three golden generations** and the reveal envelope consistent (04100's +96px bump is the ring burst at max radius, same shape as r1's accepted curve; envelope math is unit-pinned). No undocumented drift found.

**Suites (all run by Perkins at the reviewed sha):** `odin test core` 236/236 (2 pre-existing bad frees, both in untouched `health_test.odin`) · `odin test app/render` 53/53 (0 bad frees) · harness **48/48 demos green** · ci-local **11/11 gates green**.

### Blockers (0)

None. The remaining findings are non-blocking hygiene/coverage items, most carried from r1.

### Warnings (8)

1. **[still present since round 1]** Reduced-motion disables the pipe highlight entirely, contradicting the documented "steady band" (file header, proc comment, PR body §reduced-motion) — `app/render/spawn_fx.odin:434-437` [blind, acceptance, architecture]. Draw the band at fixed alpha under `reduced_motion`, or correct the three comments.
2. **[still present since round 1]** Type-chip hairline fade reintroduces the rlsw line-alpha trap — `app/render/view.odin:1232-1233` [blind, edge]. `out.a = u8(255 * fade)` on `DrawRectangleLinesEx`: goldens capture the hairline solid while the GPU app fades it (8-tick divergence per spawn). Keep the hairline full-alpha, or draw it as filled rects.
3. **[still present since round 1]** `spawn_fx_init`/`spawn_fx_destroy` are dead code; `reveals` latches the ambient allocator and is never freed — `app/render/spawn_fx.odin:92-100,146` [blind, security, architecture, codebase]. Empirical: `+++ leak 192B @ spawn_fx.odin:146`; the render suite carries 3,794 tracker leak lines. Wire the lifecycle into the View, or delete the pair and document latch-on-append.
4. **[still present since round 1]** `shadow_clone` completeness guard can't catch a future non-serialized dynamic field (a miss aliases live memory; `run_destroy` would free it) — `shadow_clone`. Re-verified complete field-for-field at r4 (all 50 `[dynamic]` fields across the 7 sub-structs; rebases added none). Residual-risk warning stands.
5. **[still present since round 1]** Reveal-buffer `>4` trim has no test — `spawn_fx.odin:153` [tests]. Feed tests assert len 1/2; spawn_feel.dem spawns exactly 4 nodes, so the trim never executes anywhere.
6. **[still present since round 1]** Reduced-motion telegraph/highlight branches untested; `a11y_reduced.dem` has no `growth on` — `spawn_fx.odin:336,434` [tests]. The W1 divergence is invisible to the suite.
7. **[since round 1, elevated]** Topology-gen re-predict leg + app-side feed/predict glue untested — `spawn_fx.odin:282`, `app/main.odin:485-487` [tests]. Nothing bumps `topology.gen` mid-window; the feed-before-`audio_mark` ordering has no coverage (a swap silently no-ops the feature live while goldens stay green).
8. **[since round 1, elevated]** `sfx_fixture` ≠ the harness/growth.dem fixture; its seed draw 1→3 (~22.6 tiles > max_span 14) is silently rejected → pipe-less test topology, and the recipe's second draw (0→1) is missing — `spawn_fx_test.odin:66-77` [codebase]. Harness fixture is (8,15)/(20,15)/(32,15) (`harness/catalogs.odin:53-55`). Pins hold fixture-independently; B2's rework keeps this below blocker.

### Notes (14)

- PR body Verification section is stale post-rebases (22/22, 47/47, 10/10 vs its own rebase sections' 48/48 + 11/11; measured here: 53/53 render) — `_pr_body_spawn_feel.md:170-175` [acceptance]
- PR body still mis-describes `node_health/20000ms` as carrying "the ring burst" (at t400 the capture's predict targets window 480, lead 80 > 10 → no telegraph that frame) — `:95-96` [carried r1]
- `sfx_load_cat`'s allocator parameter is declared but unused — `spawn_fx_test.odin:36-62` [carried r1]
- Telegraph guard wraps u64 at `T - SPAWN_LEAD_TICKS` when interval < 10 (catalog floor is `>= 1`, `catalog.odin:842`; unreachable at the shipped 80-tick cadence) — `spawn_fx.odin:330` [blind, edge; carried r1]
- `interval - 5` u64 wrap hangs the predict test if the catalog fails to load (zeroed interval) — `spawn_fx_test.odin:166-170` [edge]
- `sfx_load_cat`'s `read1` prints then drops the read error → misleading symptoms on IO failure — `:47-52` [edge]
- Unreachable dedup-reset branch in `spawn_fx_predict` (lead never grows within a window) — `spawn_fx.odin:262-265` [carried r1]
- `_ = before` edit residue in the feed test — `spawn_fx_test.odin:296-297` [carried r1]
- `spawn_feel.dem` capture comments misstate the reveal math: 4100ms (t82) claims "scale ~0.75, fade ~0.8"; actual envelope at age 2 is scale 0.494, fade 0.409 — `demos/spawn_feel.dem:19-20` [blind; arithmetic Perkins-verified]
- B2 negative-leg comment says "2 tiles"; (13,10)→(12,10) is 1 tile (mechanism unaffected — still under the 4-tile floor) — `spawn_fx_test.odin:236-240` [blind; Perkins-verified]
- #83 tint path / shadow ink-ratio fade is pinned only by composite goldens — no isolated unit pin for `ink×alpha/255` — `sprites.odin:225-231` [tests]
- Predictor's `next_node_id`-delta API surface still permits the pending-place + rejecting-plan misuse (theoretical; both callers pass only already-applied commands) — [carried r1]
- Bad frees: exactly 2, both pre-existing in `health_test.odin:877/910` (untouched by this PR) — [carried r1, re-verified]
- Render package owning the Run_State deep copy + `pp.step` in the view layer — documented accepted risk per the PR decision table; settled ruling, not re-litigated — [carried r1]

### Rejected as false-positive (2)

- "run_destroy on a temp-allocator shadow clone repeats the bad-free pattern" (blind) — the claimed effect does not reproduce: render suite shows **0 bad frees** (verified) and a scratch-allocator delete probe runs clean; the real leak is already warning #3.
- "ordered_remove without a core:containers import" (blind) — `ordered_remove` is a builtin (`base/runtime/core_builtin.odin:222`); the suite compiles and runs green.

### Reviewer agreement

Highest-confidence multi-source findings: warning #1 [blind+acceptance+architecture], warning #2 [blind+edge], warning #3 [blind+security+architecture+codebase], the u64-wrap note [blind+edge].

**Advisory test gate: FAIL** (advisory only, folded per the r1 precedent — P0 100%, P1 ~94%, overall ~77% on the P2 gaps in warnings #5–#7; raising it needs the trim test + reduced-motion pins + gen-repredict leg + an app-glue smoke).

**Vision caveat (non-k3 round):** pixel verification was MECHANICAL only (byte/hash/capture-diff); aesthetic verdicts remain deferred for the k3 re-check.

### Verdict: READY TO MERGE

Both r1 blockers are fixed and pixel-verified; the two rebases integrated cleanly; every claimed suite count reproduced locally; zero blockers remain. The 8 warnings + 14 notes are non-blocking follow-ups (most carried from r1's review).

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
