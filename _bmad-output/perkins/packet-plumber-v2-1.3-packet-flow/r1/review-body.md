## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-1.3-packet-flow · **Reviewed sha:** 6265802 · **Reviewers:** 7/7 completed
**Verification:** 5/7 reviewer findings survived code re-verification — 2 discarded as false-positive

Independent verification I ran myself (not the lenses'): `odin test core` → **20/20 pass**; the 4 lint gates (core purity / no globals / no map-iteration / no dropped errors) **green**; `odin build app` **clean**; the software-renderer harness (`tools/harness.sh`, rlsw built from source) → **boot/flow/draw all green**; standalone `harness replay flow` → **60 ticks bit-for-bit (ODN-11)**; the 3 new flow PNGs are real frames (33–38 non-black colors each — not the all-black GPU-renderer trap).

**Lens-guard check (all hold):** per-hop forwarding is structural — the `Packet` struct has **no `route[]` field**, there is **no `compute_route`** and **no BFS-on-packet** (`routing_rebuild`'s BFS builds the *forwarding table*, next-hop-per-dst, which is correct, not the banned per-packet route); the table is rebuilt only on `Topology.gen` change (4-rule-spine rule 1, synchronous in-tick); the id-0 sentinel is handled via the explicit `on_edge` flag + a +1 id scheme; flow demand is run-setup re-created identically in **both** the live (`lower_spawns`) and replay (`replay_hashes`) paths; the routing table is correctly **not** serialized (it is derived from the Topology, which is). 1.3 stays single-path — no ECMP, no bundles (deferred). Core stays engine-free.

### Blockers (0)
None.

### Warnings (0)
None.

### Notes (4)

**N1 — `spawn_tick` proc is dead code; `lower_spawns` inlines the identical tick formula** `[blind, codebase]`
`harness/demo.odin` adds `spawn_tick(s, hz) = floor(at_ms*hz/1000)` (no +1) but **no caller exists** (grep: zero callers — only the unrelated `Packet.spawn_tick` field). `harness/run.odin:lower_spawns` duplicates the exact same expression inline. The two formulas **agree**, so there is no current determinism bug — but this is a latent divergence hazard on the replay-identical-demand invariant. *Fix:* have `lower_spawns` call `spawn_tick(&s, hz)`, or delete the unused proc.

**N2 — defensive severance branch resets to `p.src` (original source), not the lost edge's departure node** `[architecture]`
`core/flow.odin:119-126` — the on-edge `if !ok` (lost-pipe) branch sets `p.at_node = p.src`. `p.src` is never reassigned anywhere in `flow_step`, so for a multi-hop packet this teleports it back to the **original spawn source**, contradicting the branch's own comment ("drop back to the departure side of the lost edge"). **Unreachable in 1.3** (pipes are never removed → `pipe_slot` always succeeds), so no functional impact now — but it pre-implements slice-2.3 severance incorrectly. *Fix:* drop the branch, or reset to the `p.edge` endpoint that isn't `p.heading`.

**N3 — demand `src`/`dst` ids are not validated for liveness** `[edge]`
`flow_seed_demand` and the demo `spawn` parse accept any `u32` id with no live-node check. A typo'd id spawns a packet at a non-existent node; `routing_next_hop` then returns `ok=false` forever → a silent ghost packet that never delivers / never visibly renders. Not triggered by current valid inputs (`src==dst` *is* handled — marked delivered at spawn). *Fix:* validate at the lowering boundary (`lower_spawns` / app seed) where the Topology is available.

**N4 — Advisory test gate: PASS (8/8 traced behaviours covered)** `[tests]`
The 5 new `@(test)` funcs pin per-hop source→sink, rule-1 table rebuild, no-cached-route re-forward (E29), flow replay byte-identical (E10), unroutable-waits-then-flows (E28); the `flow.dem` T2 golden covers the mid-traversal render; `Packet_Arrived`+cull and the id-0 path are transitively exercised. P0 4/4, P1 4/4, overall 8/8 = 100%. ECMP/QoS/SLA/demolish correctly out of scope. *Optional later:* a dedicated id-0 `@(test)`.

### Reviewer agreement
- **`spawn_tick` dead code + duplicated tick formula** — flagged independently by `blind` + `codebase` (highest-confidence signal in the round).

### Rejected as false-positive (2)
- *blind:* "`load_demo_spawns`'s unused `perr` is a hard Odin compile error (build-breaking)" — **empirically false**: `odin build harness` (incl. `-strict-style`) exits 0 with no warning; Odin permits the unused second value of a multi-return binding, and the lenient parse is the documented intent.
- *blind:* "keystone hash-variation assertion cites a 'serialized tick field' absent from the diff" — **false**: `serialize.odin:73` (`w_u64(&w, state.tick)`) + `step.odin:28` (`state.tick = tick`) serialize and advance the tick each step, which is exactly why the hashes vary; the comment is accurate (the lens read only the diff hunk).

### Verdict: **READY TO MERGE**
0 blockers, 0 warnings. The load-bearing invariants hold and are independently verified (per-hop forwarding, rule-1 rebuild, id-0 handling, engine-free core, replay-determinism over the flow). Tests, lint, app build, and the software-renderer harness are all green. The 4 notes are non-blocking cleanups.

---
_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
