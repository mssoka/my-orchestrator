## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-box-crash-third-spawn · **Reviewed sha:** 444334d · **Reviewers:** 6/7 completed (blind lens failed twice on output-length — degraded, disclosed below)
**Verification:** 12/12 findings confirmed against the code — 0 discarded as false-positive

### Root cause — independently verified (the urgent leg)
The fix's mechanism is **confirmed against both .ips signatures**; the briefing's leading hypothesis (2→4 grow/realloc) is **disconfirmed** — `box_grow` sizes once at `box_enable` and is idempotent after (`node_types` count is fixed), so there is no mid-play grow. The real chain, verified byte-level: `shadow_clone`'s `clone := src^` value-copy left `box.pieces`/`box.spools` headers aliasing the LIVE buffers **including the live heap allocator in the header** — so the shadow's `run_destroy`→`box_destroy`→`delete` freed the live buffers (predict #1) even though the clone ran on `temp_allocator`. Each connection bumps `topology.gen` → mid-lead re-predict → the second aliased destroy frees the same block again → libmalloc `POINTER_BEING_FREED_WAS_NOT_ALLOCATED` SIGABRT. The "third connection" timing is the second post-enable predict landing on a connection-triggered re-predict. The class was CI-invisible because **zero golden demos run box-on** (nil headers delete harmlessly) — the playtest was the only box-on × telegraph-lead surface.

### Mutation gate — re-run by Perkins (RED→GREEN, machine-proven)
- **RED:** reverted `shadow_clone` to the pre-#108 non-owning state → both new tests FAIL (`box.pieces`/`box.spools` alias pins) + tracked-allocator `bad free @ box.odin:44-45 box_destroy()` — the .ips site class — across the leg's 5 spawn windows (the `spawns >= 5` assertion held; RED achieved with ≥5 spawns in play).
- **GREEN:** restored → 117/117 render tests, both gates green.

### Class sweep — complete
All 55 `run_destroy` deletes accounted for: 53 `clone_dyn` lines + 2 by-design zeroed (`action_log`/`events`, asserted nil in the test). Every dyn-array element type is scalar/fixed (no nested dyn/ptr → no nested-alias stragglers); `board: ^Map_Board` is read-only caller-owned (zero writes in core). The Box arrays were the only #107-added members of the missed-field class — both fixed.

### No-regression — full local sweep GREEN
13/13 `ci-local --mac` gates (purity, core/app/render/input/audio/harness tests, app build, golden harness bit-for-bit, palcheck, drift-check, preview-check, motion-pixel, PP_DEBUG builds+smoke, font-guard, stats replay-identity, input parity) + `econ-check` (all 4 box scenarios hold). `fold-check` subsumed: the delta touches only `app/render/spawn_fx.{odin,_test.odin}` — no golden or catalog bytes moved. CI billing-block signature note-only per standing ruling.

### Blockers (0)
None.

### Warnings (3) — none merge-gating; the crash is fixed and gated
1. **[security+edge+acceptance+architecture+tests — full agreement]** `sfx_no_alias`'s `len==0` skip leaves **15/57 pins vacuous** in-fixture (health ×9 + era_gate ×5 + `pipe_lane_over` ×1 — the fixture never enables those systems) and cannot catch empty-but-allocated aliases (the exact crash class). The skip is load-bearing (two correctly-cloned empty arrays are both nil → false fail without it) — grow the fixture instead. *Follow-up candidate.*
2. `shadow_clone` remains a hand-maintained mirror in the view layer — the structural root of this class; now test-guarded, still manual.
3. The alias gate is a comment-synced checklist, not an automatic invariant (reflection walk or core-owned clone would close it with #2).

### Notes (5)
- The economy-leg comments overstate: pre-fix the leg **fails the w1 alias pin** (bad frees under the tracked allocator); the SIGABRT is the app-heap behavior (Perkins mutation run evidence).
- u64 window-math wrap if `terminal_spawn_interval_ticks` ever drops ≤ 5 (shipped catalog: 80) — latent only.
- AC wording: the leg performs 1 literal connect + 4 other gen-bumping edits across 5 windows; every edit re-predicts, and the teeth are mutation-proven — substantively compliant with the mandated "place/promote/teardown/resplice" leg.
- `delete(batch)` has no direct test (no-op under the temp allocator; `free_all` per frame covers the app).
- Advisory test gate: **PASS**.

### Reviewer agreement
The len==0 vacuous-pin finding was independently filed by **5 of 6 lenses** (security, edge, acceptance, architecture, tests) — highest-confidence signal in this review.

**Degraded disclosure:** the blind lens failed twice (`stopReason: length` — mechanical output-window ceiling, no-tool single-shot). The remaining 6 lenses + the four mandate legs above covered the diff surface; no verdict weight rests on the missing lens.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
