## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-2.2-ecmp · **Reviewed sha:** `a1c6e64` (head unchanged mid-review) · **Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 4/4 unique findings confirmed against the code — 0 discarded as false-positive; 1 raw duplicate merged into the reviewer-agreement note below.

**Load-bearing lens-guards — all verified GREEN** (the 4-rule determinism spine):
- ✅ **Pure hash, no sim-rng (rule 2):** `ecmp_pick = splitmix64(src,dst,class,pkt_id) mod N`. `ecmp_hash` calls `splitmix64` on a *local* u64; `splitmix64` (`core/rng.odin:33`) is pure (mutates only its `^u64`). Grep for `rng_next`/`rng_range`/`state.rng` in `routing.odin`/`flow.odin` → clean (sole match is an asserting comment). Pinned behaviorally by `test_ecmp_pick_is_pure_no_sim_rng` (flow run vs no-flow run end bit-identical `rng.state`/`inc`).
- ✅ **No map iteration in the hot path:** equal-cost set is array-indexed (`hops[offset + hash % count]`); `Routing_Table` uses flat `hop_offset`/`hop_count` + packed `hops`. No map types anywhere in `routing.odin`/`flow.odin`.
- ✅ **Flow affinity:** `ecmp_pick` is pure in `(src, dst, class=0, pkt_id)` → same packet → same path every replay. Pinned by `test_ecmp_flow_affinity_same_packet_same_path`.
- ✅ **Determinism (E10/ODN-9/10):** routing table stays DERIVED (rebuilt from Topology, not serialized into T1); per-packet path fields ride the hash. `test_ecmp_replay_byte_identical` passes.
- ✅ **Core engine-free (ODN-1):** `routing.odin`/`flow.odin`/`ecmp_test.odin` are `package core`, zero engine imports.
- ✅ **Backward-compat (count==1):** reproduces slice-1/2.1 single-hop (`hash % 1 == 0`); `43/43` core tests pass at `a1c6e64`, no re-bless needed.
- ℹ️ T2 pixel-harness gap is the documented carry-forward (mini-story recommendation), not a defect — not counted here.

### Blockers (0)
None.

### Warnings (0)
None.

### Notes (3) — advisory, non-blocking
- **N1 (reviewer agreement: blind + architecture) — stale doc comment.** `routing_next_hop`'s doc lists its callers as "(tests, `routing_has_path`)", but this same diff reroutes `routing_has_path` to call `routing_equal_cost_hops` directly (`core/routing.odin`). Real `routing_next_hop` callers are now tests only (`flow_test.odin:82,86`, `ecmp_test.odin:88`). *Fix:* drop "`routing_has_path`" from the parenthetical (e.g. "callers: tests only").
- **N2 (tests) — 3+-way ECMP untested.** Every ECMP test uses the 2-way diamond; `ecmp_pick` is never called with `n>=3` and no 3+-way junction is built. The `% n` path is identical by construction for any `n`, so this is a confidence gap, not a correctness risk. *Fix (optional):* add a `count==3` test (three equal-cost middles) asserting all 3 hops pack into `hops[]` and `ecmp_pick` distributes across all 3 buckets.
- **N3 (tests) — `next_packet_id` determinism asserted only transitively.** Flow affinity across two runs presumes identical packet ids (`ecmp_test.odin:207-208` comment), but no `expect` asserts it directly — a packet-id regression would surface as an affinity/replay failure, not a localized one. *Fix (optional):* add `testing.expect(t, a.flow.packets[0].id == b.flow.packets[0].id)`.

### Reviewer agreement
- **N1** was flagged independently by two lenses (**blind** + **architecture**) — higher confidence.

### Test coverage gate: PASS
P0 5/5 = 100% (pure-hash/no-rng, no-perturbation, affinity, replay `[E10]`, count==2+1 AC) · P1 3/3 = 100% (spread, end-to-end split, `next_packet_id` transitive) · overall 11/12 = 91.7% (only 3-way ECMP untested — N2). All thresholds met.

**Verdict:** READY TO MERGE — 0 blockers, 0 warnings. The ECMP implementation is correct, deterministic, and well-tested; the three notes are minor polish the implementing minion may fold in pre-merge at their discretion (not required).

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
