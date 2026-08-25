## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-estate-spawning · **Reviewed sha:** 26eb4e5 · **Reviewers:** 6/7 completed — failed: `codebase` (429-rate-limited twice, original + one retry; proceeded degraded with findings present)
**Verification:** 14/14 findings confirmed against the code — 0 discarded as false-positive, 0 kept as [unverified]

**Mechanical gate (independently reproduced by the orchestrator):** `odin test core` 232/232 PASS · `tools/harness.sh run` **45/45 demos green** (full re-bless replay gate) · `harness fold-check dfe3e342b56679fb 4eaa272171fac065` **PASS** (tick-1 shift = catalog fold alone) · spawn audits re-counted: before **7/19 strays (37%)** → after **0 strays** (12 ATTCH + 1 SEED), final t1760 = **three 5-member estates**; cap-8 variant grows clusters to 8 with 0 strays · `LOG_VERSION` untouched, no routing/serialization files in the diff, `terminal_spawn_interval_ticks` stays 80 · spatial-lane canon (2e3acab/8ece056) untouched — supersession properly flagged in the GDD decision-log. Lens-guards: all three hard bars PASS.

### Blockers (0)

None.

### Warnings (3)

1. **`new_area_seed_tiles` parsed via `jint`, not `jint_strict`** — `core/catalog.odin:895`. A decimal value (`10.5`) silently truncates; an out-of-i32-range integer wraps. Sibling tunables (`cap_fraction_permille`, `placement.*`, terminal keys) use `jint_strict` for exactly this (ODN-10 integer-only bar). Fix: parse strict + add a decimal rejection row.
2. **134 `+++ bad free` per `odin test core` run from the new `strict_spawn_class` helper** — `core/growth_test.odin:527-529,556-558`: `make([]i32, n, context.temp_allocator)` + `defer delete(...)` is an invalid free every call (temp allocator owns the memory). Tests still exit 0, so CI stays green while the tracker output drowns — masking genuine sim-code allocation regressions. (2 more bad frees pre-exist in untouched `health_test.odin`.) Fix: drop the two `defer delete` lines or allocate from `context.allocator`.
3. **PR body draw-count claim contradicts the code** — the body says "draw order/counts per attempt unchanged — the rng interleaving shifts only through acceptance", but `growth.odin` documents exactly ONE draw-count change vs 5.12 introduced by this PR's dead-slot collision guard (the member pick's `rng_range` flips drawn→SKIPPED in the collision case). On the determinism contract, the docs should agree. Fix: add the carve-out parenthetical.

### Notes (10)

1. **[3-reviewer agreement]** Seed-floor diameter guard uses `w²+h²` but the grid's widest achievable spacing is `(w-1)²+(h-1)²` — `core/catalog.odin:1016`. On the 40×30 map, `new_area_seed_tiles: 49` loads clean yet can never be cleared (max dist² = 2362 < 49² = 2401) → deterministic silent growth stall — the exact failure the guard exists to prevent. Sub-diameter span-unreachable floors (e.g. 45) stall the same way. Fix: reject when seed² > (w-1)²+(h-1)².
2. Spec Design Notes (lines 85/87) repeat the "draw counts unchanged / no rng draws" claim that the same spec's NOT-changed section carves out — internal inconsistency.
3. Cap-8 demo claim "grows estates to 8 **before seeding a new area**" — the cited capture has 11 spawns, all ATTCH, **zero SEED events** through t1760. The cap-8 mid-run seed is test-pinned (`test_groups_estates_strict` cap-8 leg), so the behavior is proven — the sentence just overstates this artifact.
4. Fixture test discards `topo_setup`'s `rt` via `_ = rt` then re-fetches `router_basic` — dead-variable workaround in new code.
5. SEED-family annulus draw duplicated verbatim in two branches of `growth_plan_demand` (`growth.odin:694-703` / `714-723`) — this PR had to edit both identically; extract a shared proc.
6. `growth_attach_radius_ok` takes `^Topology` + slot but is a pure two-point distance test — the signature forces a topology fixture in the unit test.
7. No accept-side boundary row for the diameter bound (49 on 40×30) and the parsed `new_area_seed_tiles` value is never asserted — only reject rows (50/51) exist.
8. `growth_seed_sep_ok`'s fail-closed degenerate guard (`min_dist < 1`) is untested while the sibling attach predicate's zero case is pinned — asymmetric guard coverage.
9. Advisory test gate: **PASS** (P0 100%, P1 ~95%, overall ~92% — the strict audit pins at both caps, opt-in mix, fixture collision, E31, loader rows).
10. PR body omits the bmad-build workflow provenance line the briefing expected (3 review layers, 10 patch fixes re-verified) — the verification substance is present and was reproduced; provenance narrative only.

### Reviewer agreement
- **Diameter-guard bound defect** — independently reported by `acceptance`, `edge`, and `security` (merged; the highest-confidence finding of the round).
- The bad-free warning was independently reproduced by the orchestrator's own `odin test core` run before the tests lens reported it.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
