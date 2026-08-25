## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-6.3-upgrade-lifecycle · **Reviewed sha:** `9bce5ba` (base `95a62ad` = origin/v2 post-6.2) · **Reviewers:** 14/14 completed (7 lenses × 2 chunks — the 76.5k-line diff chunked: source 1.7k + the new golden pair 2.8k lens-read; the ~72k lines of golden re-pins verified **mechanically** per the standing orders)
**Verification:** 19/23 reviewer findings confirmed against the code — 4 discarded as false-positive, 2 demoted after empirical check; 0 unverified

**Mechanical ground truth (re-run at the reviewed sha):** `tools/ci-local.sh --mac` **10/10** (incl. gate 4 golden harness — both new demos replay bit-for-bit at 1400 ticks; drift-check rejects all 322 mutations; input parity 27/27) · `harness fold-check` **PASS** (boot tick-1 splice == pre-re-bless tick-1 — the shift is the catalog fold alone) · all 43 modified `.log.bin` same-size, differing **only** at byte 4 (version 5→6) + bytes 17–24 (catalog hash) · all 18 era-0/1 `.t1` + `advance_block_legacy` fold-shaped (only `catalog_hash` + tick-hash lines differ) · **42 changed T2 frames all era-≥2 demos; era-0/1 T2s byte-identical** · pixel-diff on advance_fire 60000ms: 0.60% of pixels, world-space bbox only; vision-read (qwen) confirms structure unchanged, traffic-density deltas only — the one flagged tint resolves to the **pre-existing 4.1 congestion halo** engaging on the decayed pipe (sim-state-driven, render code untouched) · 228/228 core tests, 9 new contracts · the draw-era rejection argument **verified sound** (GDD M1 "baseline legacy" tier + the fold-shaped `advance_block_legacy` golden pin the tier predicate — not re-opened).

**The measurability contract holds:** the golden pair is genuinely twinned — stats streams identical through tick 600, diverging exactly at 601 (tier 1→2, cap 7→40); end-state **decayed 172 delivered / 671 dropped vs modernized 846 / 0**; the 15000ms captures are byte-identical, the 60000ms captures differ. Decay is real sim behavior (bundle caps + lane caps fold `pipe_effective_capacity`, the only non-test `capacity_units` reader), deterministic, replay-identical.

### Blockers (0)

None. The determinism/replay spine and the decay measurability contract both verified sound.

### Warnings (3)

**W1 — The cross-test's era-1 "documented split" pin is a no-op `continue`; nothing anywhere pins the era-1 legacy predicate** `[blind, acceptance, codebase, tests]` — `core/legacy_test.odin:316-319` asserts nothing; the in-test comment ("pinned explicitly so it can never silently drift") and the PR body repeat the claim. The only era-1 pin (`pipe_effective_capacity(cat,1,na)==10`) is predicate-insensitive (factor 1000 → 10 either way); all 6.2 gate tests and every advance demo run era 2 — if the predicate stopped naming era-1 narrows legacy (the 1→2 gate bar), zero tests/goldens fail. *Fix: assert the split in place (expect `era_pipe_is_legacy(cat,1,na)` + the capacity pin side by side).*

**W2 — `test_crisis_settled_scan` staging comment contradicts its own 6.3 re-pin** `[blind]` — `core/crisis_test.odin:498` says "the first streaming shed lands on bundle 2" while the pin at :566-575 asserts bundle 0 ("now bundle 0, tick ~20"). The pin passes; the staging comment is wrong prose that will mislead the next rate-sensitive retune. *Fix: rewrite the staging comment to the pinned dynamic.*

**W3 — The golden pair's T1 manifests diverge from tick 1 via the action-log fold; "only the legacy state differs" is false for ticks 1–600** `[architecture + mechanical]` — the 4 `Cmd_Set_Pipe_Tier` entries ride the (pre-existing) action-log section of the state hash, so both manifests differ from tick 1 although behavior is identical pre-fire (byte-identical 15000ms captures). T1 alone cannot show *when* behavior diverges — the measurability evidence actually lives in the identical-through-600 stats streams, the 15000/60000ms capture contrast, and the GWT unit test. Misdiagnosis risk for a future re-bless audit. *Fix: one doc line in `legacy_modernized.dem` (+ PR-body amendment) naming where the contrast evidence lives.*

### Notes (9)

- **N1** `pipe_effective_capacity`: `raw × permille` unguarded u32 — `capacity_units` has no upper bound at load (only >0); authoring data ≥ ~4.3M would wrap against the ODN-5 bar `[security, edge]`. Compute in u64 or bound at load.
- **N2** demo `modernize <pipe>`: u64→u32 narrowing unchecked — the weights verb's own fixed pattern ("fail loud at parse") not followed; ids ≥ 2³² silently retarget `[security, edge]`.
- **N3** `testing.expectf(nil, …)` in the GWT test's `build()` — empirically still bites (Odin fails on logged errors), but thread `t` for honesty `[blind]`.
- **N4** `pipe_effective_capacity`: redundant second `era_row` lookup + unreachable-false `ok` guard (dead branch on the hot path) `[blind]`.
- **N5** `validate_set_pipe_tier` checks catalog range only, no era-unlock — mirrors `validate_draw`'s shape (consistent canon: unlock = content availability); worth documenting as a deliberate seam `[blind]`.
- **N6** `legacy_decay.dem` is directive-identical to `advance_fire.dem` (all golden artifacts byte-match the 6.2 golden) — defensible as the story-named pair; document the twinning so future retunes sync consciously `[architecture]`.
- **N7** LOG_VERSION 5→6 lacks the dedicated old-version rejection leg (the placement 2→3 precedent) — same reject path as the generic version=99 pin, convention only `[tests]`.
- **N8** The pair's twin property (identical seed/topology/demand) is prose-only — no machine check cross-compares the demos; a future one-sided .dem edit would silently un-twin while both stay green `[tests]`.
- **N9** Advisory test gate: **PASS** — P0 100% (replay spine, GWT contrast), P1 ~95% (era-1 pin partial per W1), overall ~96% `[tests]`.

### Reviewer agreement
W1 `[blind, acceptance, codebase, tests]` (4 independent lenses) · N1 `[security, edge]` · N2 `[security, edge]` · W3 `[architecture + Perkins' mechanical pass]`.

**Verdict: READY TO MERGE**

The one hard blocker class (determinism/replay spine + decay measurability) is verified sound end-to-end; the 3 warnings are documentation/test-hygiene (a vacuous pin claimed as real, a contradictory comment, an overstated evidence claim) — advisory fold-in candidates, none merge-blocking.

_Address findings and push — I re-review automatically on the new sha._
