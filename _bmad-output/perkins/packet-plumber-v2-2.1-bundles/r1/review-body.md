## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-2.1-bundles · **Reviewed sha:** cb497ab · **Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 5/6 reviewer findings survived code re-verification — 1 discarded as false-positive; 0 kept as unverified

### Blockers (0)
None.

### Warnings (0)
None. (One blind-lens `warning` was filed but **rejected as a false positive** — see the audit note at the bottom.)

### Notes (5)

**N1 — Merge "pop" is an instant width change, not an animated tween** *(acceptance)* — `app/render/view.odin:137`
The Story 2.1 AC says *a merge "pop" animation*; the implementation is an instant static width change (`width = tier_width + f32(count-1)*BUNDLE_EXTRA_WIDTH`, no tween/time). This is acceptable for slice 2 — the "pop" read (a fatter pooled link forming) is satisfied and golden-verified, and animated juice is slice 7 (Story 7.1). Flagged only so the AC-vs-impl wording is on the record. **No change needed for 2.1.**

**N2 — Unused loop binder `i`** *(codebase/convention)* — `core/bundles_test.odin:197` (`bundle_leg_transit`)
`for i in 0..<parallel_pipes` — the body doesn't reference `i`; the project idiom for an unused range binder is `for _ in` (e.g. `rng_test.odin`). Compiles clean (`odin test core` = 36/36; CI doesn't run `-vet`). Optional: `for _ in 0..<parallel_pipes`.

**N3 — Defensive fallback branch (`cap == 0`) has no direct test** *(tests/coverage-gap)* — `core/flow.odin:140-143` + `core/bundles.odin:159-165`
The primary lookup is FULL via `test_bundle_resolves_via_representative_pipe`. The `if cap == 0 { cap = <own tier cap> }` fallback is exercised by no test; `step()` always rebuilds bundles before `flow_step`, so a live pipe's pooled cap is never 0 (defensive-only, unreachable in normal flow). Optional: a unit test injecting a stale `Bundles` (`pipe_bundle = NO_BUNDLE`). No bar to merge.

**N4 — `f32(count-1)` would garble the frame IF a bundle row ever had `count == 0`** *(defensive-coding; unreachable today)* — `app/render/view.odin:draw_bundles`
`count` is `u32`; `count-1` wraps to `0xFFFFFFFF` if `count == 0`. A bundle row is only minted when ≥1 live pipe is found and `bundle_count` is bumped in the same pass, so `count ≥ 1` for every iterated row — unreachable by construction. Optional hardening: `f32(max(count,1)-1)` or an assert so a future invariant break surfaces as a clean failure.

**N5 — Advisory test gate: PASS** *(tests)*
P0 100% (static-sum, mixed-tier-sum, representative-resolves, no-LB behavioral pin, T1 determinism — all FULL); P1 100% (lone-pipe, rebuild-on-change, W1 restart, W2 LOSE-replay, render T2, lookup); overall 10/10 behaviors FULL. Pixel T2 match: harness wiring confirmed correct (`capture_frame → draw_world` both thread `bundles`; `run_demo` passes `&state.bundles`).

### Reviewer agreement
No multi-source findings (nothing reported by ≥2 lenses).

### Independently verified by Perkins (the load-bearing invariants)
- **No load balancing** — lint gate 5 (`tools/lint.sh`) **catches** a planted `lb_weighted`/`round_robin` pattern and **passes clean** on the real code; a comment-stripped grep of all non-test `core/*.odin` finds zero LB identifiers. The flow consumes `bundle_capacity_for_pipe` (the pooled cap) and serves it whole. ✓
- **Static sum at table-build (rule 3)** — capacity is folded once in `bundles_rebuild` into `bundle_cap`; the flow reads that static value, never recomputes per-packet. ✓
- **Determinism** — `state_writer` (`core/serialize.odin`) deliberately does **NOT** serialize `bundles`/`bundles_gen`/`routing`/`routing_gen` (explicit comment: mirrors the routing table — "hashing it would bind replay to the table-build algorithm"). So slice-1 goldens stay byte-identical, and bundles re-derives deterministically on replay. `Packet.edge` stays a pipe id. ✓
- **Restart safety** — `run_init` does `state^ = {}`, zeroing `bundles_gen`/`routing_gen`, so no stale-gen bug on retry. ✓
- **ODN-1 core purity** — no `vendor:`/`core:os`/`core:time`/raylib imports in `core/`. ✓
- **W1/W2 carry-forwards (from 1.4 Perkins r1)** — `test_app_layer_restart_cycle` (W1: full WIN cycle → restart with fresh seed → assert clean → re-playable) and `test_lose_loop_replay_byte_identical` (W2: a losing run replays byte-identical including the terminal frame) are present, real, and passing. ✓
- **`odin test core` = 36/36 green.** All `draw_world`/`capture_frame` callers updated for the new `bundles` param. ✓

> Verification scope note: the T2 **pixel** match (`goldens/bundle/*.png`) requires the software-raylib harness build (no prebuilt `rlsw` shadow in the worktree), so the pixel bytes weren't independently re-diffed this round. The determinism **property** is fully unit-tested green (`test_parallel_pipe_draw_replays_byte_identical` + the harness wiring is confirmed correct), and the committed `goldens/bundle.t1` manifest + demo are consistent. The pixel re-diff can run in a later round if you want belt-and-braces.

### Audit note — rejected false positive
The **blind** lens filed a `warning`: *"lint.sh gate 5 echoes `$HITS` instead of `$LB_HITS` on failure."* **Rejected.** Both the canonical `diff.patch` (line 987) and the worktree `tools/lint.sh:42` show `echo "$LB_HITS"` — the **correct** variable. The lens pattern-matched gates 1–4 (which use `$HITS`) onto gate 5. Empirically confirmed: planting `lb_weighted` in `core/bundles.odin` made the gate print `core/bundles.odin:168:lb_weighted :: proc(){}` (the actual LB match), which could only come from echoing `$LB_HITS`.

**Verdict:** READY TO MERGE — 0 blockers, 0 warnings; all load-bearing invariants (no-LB, static sum, determinism, core purity, W1/W2 carry-forwards) independently verified; the 5 notes are advisory/optional.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
