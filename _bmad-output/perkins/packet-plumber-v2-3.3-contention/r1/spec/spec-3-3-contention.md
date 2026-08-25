---
title: 'Story 3.3 — Node serialization + contention drop ladder'
type: 'feature'
created: '2026-08-13'
status: 'in-review'
review_loop_iteration: 0
baseline_commit: 2e3acab77e1edebd779f3a2f1c998df2907cced2
context:
  - '{project-root}/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Pipes have no serialization: every on-edge packet advances at the full bundle capacity each tick (unlimited parallel channels), so there is no queueing, no contention, and no drop — the QoS differentiator's second half (the serialization visual + contention drops) is missing.

**Approach:** Add the 3.3 half of ODN-3 inside `flow_step`: per-bundle, per-lane bounded queues with lane-ordered serialization service (Express → Standard → Best, work-conserving gap-fill + a WRR floor — E7, no starvation), the E9 drop ladder (BE → Standard → Express) when a lane queue is full, and the E22 pool-exhaustion backstop (global in-flight cap, drops the lowest-priority lane first). Drops emit `Packet_Dropped{class, reason}` events. All 3.3 state is DERIVED (no new Packet fields, no new serialized Flow_State fields). Plus the **spatial-lane canon (user ruling 2026-08-12, base 2e3acab)**: every pipe renders THREE painted lane strokes (width = WFQ allocation share) and every packet rides IN its lane (lateral offset) end-to-end — the serialization visual at nodes + the T2 goldens show packets in lanes. This supersedes 3.2's length-segment stripes and the default-pipe-unchanged render rule: **all** pipe-containing T2 goldens re-bless by canon (documented).

## Boundaries & Constraints

**Always:**
- Service model = **cyclic WRR windows** per bundle per tick: walk lanes E→S→B; each ready lane is entitled to its WFQ budget (Σ member `lane_caps`) per window, floored to 1 unit when its budget is 0 (E7 — ≥1 slot per non-empty lane per window); a lane with no queued packets is skipped (work-conserving — the pipe is never idle while a packet waits); windows repeat until the bundle capacity is consumed or no packet is ready. A lone packet in ANY lane gets the full capacity per tick (light-demo transits unchanged).
- Lane FIFO within a queue = **array order** (spawn order; documented deviation from strict join order — deterministic, no extra serialized state).
- The queue, the bounds, and the service are **per bundle** (parallel pipes pool — members' `lane_caps` sum; a packet's lane resolves from ITS representative pipe via `qos_lane_of`).
- **E9 admission ladder:** when a packet would join a (bundle, lane) queue at `lane_queue_packets` (full), shed the NEWEST packet of the lowest-priority NON-EMPTY lane (walk BE→S→E); the arriving packet itself drops when it is the shed target (its lane is the lowest non-empty). The shed packet is spliced from the array (order-preserving); the arriving packet joins. `lane_queue_packets` + `pool_max_packets` are `balance.json` keys (data-driven, fail-fast validated ≥ 1, folded into catalog_hash).
- **E22 spawn guard** inside `flow_spawn`: at `pool_max_packets`, the same ladder over in-flight packets (lane = on-edge → `qos_lane_of(its pipe)`, else class `default_lane`); the arriving packet drops when its lane is the shed target.
- Drops emit `EVENT_TAG_PACKET_DROPPED` with `{class u16, reason u8}` (`Queue_Overflow` / `Pool_Exhaustion`); the event payload serializes **only for the new tag** (append-only; old runs' event bytes unchanged). LOG_VERSION stays 3, no new commands.
- Determinism spine: array-only walks, integer math, no new serialized fields; existing light demos' T1 stays byte-identical (catalog_hash header re-bless is the only T1 shift). T2 pixels re-bless across all pipe demos — the spatial-lane canon repaints every pipe (3 lane strokes) + every on-edge packet (lateral lane offset); a deliberate, documented re-bless, not a drift.
- **Spatial-lane render (canon 2e3acab):** each pipe (bundle) paints 3 lateral lane strokes perpendicular to its direction — stroke widths = Σ member `lane_caps` / total × pipe width (a zero-share lane draws no stroke — a missing stripe; the bands abut, so the base/core do not peek through); packets on a pipe draw laterally offset into their lane's band center (`qos_lane_of(p.edge, class)`); queued packets (on-edge, progress 0) therefore pile at the node in lane order — the serialization visual. At-node packets (no pipe yet) stay centered. Band layout is a pure function of (caps, width) — deterministic.

**Ask First:** none — queue bounds + pool cap values are delegated ("tunables are YOUR call", data-driven).

**Never:** No new Packet fields (golden stability). No new serialized Flow_State fields (ditto). No 3.4 SLA, no severance-drop event (the 2.3 silent cull stays silent — demolish.dem's event stream must not change), no new player commands, no per-class `bandwidth_demand` (catalog field stays unused — flag in the PR), no LB mechanics (lint gate 5), no silent golden re-bless: if an existing golden shifts for a reason other than documented contention, STOP and flag.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | one packet on a pipe (any lane) | full capacity per tick — transit unchanged from 3.2 | n/a |
| E7 floor | budget {0,0,0} lane ready, capacity left | 1 unit per window for the ready lane while capacity remains | n/a |
| E7 no-starvation | caps {9,4,2}, continuous Express arrivals | Standard + Best still receive their budgets every window | n/a |
| E9 ladder | lane full; lower-priority lane non-empty | shed that lane's NEWEST packet (Queue_Overflow event), admit the arrival | n/a |
| E9 self-shed | lane full; it IS the lowest non-empty | the arriving packet drops (Queue_Overflow) — queue stays at bound | n/a |
| E22 pool | pool at `pool_max_packets`; spawn arrives | the ladder sheds the lowest-priority non-empty lane's newest; the arrival is admitted ONLY when that target is STRICTLY lower priority than its own lane, else the arrival drops (the inversion guard — an Express resident never pays for a Standard arrival) | n/a |
| Replay | run with drops, re-sim from the action log | identical drop events + queue state — byte-identical hashes (E10) | replay gate rejects divergence |

## Code Map

- `core/qos.odin` -- `qos_serialize` (pure per-window budget + E7 floor)
- `core/flow.odin` -- the serialization service (cyclic WRR windows per bundle), the E9 admission ladder, the E22 spawn guard, drop splicing + events
- `core/types.odin` -- `Drop_Reason`, `Event.class/reason`, `EVENT_TAG_PACKET_DROPPED`
- `core/serialize.odin` -- tag-conditional event payload in `state_writer`
- `core/catalog.odin` + `data/balance.json` -- `lane_queue_packets` + `pool_max_packets` parse/validate
- `core/determinism_test.odin` -- test-catalog defaults for the new keys
- `core/flow_test.odin` + `core/qos_test.odin` -- E7/E9/E22 pins
- `app/render/view.odin` -- the spatial-lane render: 3 lateral lane strokes per bundle (width = allocation share) + per-packet lateral lane offset (shared band-layout helper); replaces 3.2's length-segment stripes
- `harness/demo.odin` + `harness/run.odin` -- optional `spawn ... <class>` field (legacy demand, class defaults to email)
- `demos/qos_contention.dem` (NEW) -- the launchable oversubscription demo

## Tasks & Acceptance

**Execution:**
- [x] `data/balance.json` -- add `lane_queue_packets` (6) + `pool_max_packets` (512) -- the data-driven bounds (ODN-5)
- [x] `core/catalog.odin` -- parse + fail-fast validate the two keys (≥ 1) -- ODN-5
- [x] `core/qos.odin` -- `qos_serialize` (per-window budget: E7 floor, clamp to remaining) -- the pure ODN-3 proc
- [x] `core/types.odin` -- `Drop_Reason`, `Event` payload fields, `EVENT_TAG_PACKET_DROPPED` -- the drop record
- [x] `core/flow.odin` -- forward-pass admission (E9 ladder, splice drops, events) + the per-bundle cyclic WRR service + the E22 spawn guard -- the story's heart
- [x] `core/serialize.odin` -- tag-conditional drop payload in `state_writer` -- golden stability
- [x] `core/determinism_test.odin` -- test-catalog defaults (lane_queue_packets 6, pool_max_packets 512)
- [x] `core/qos_test.odin` -- E7/E9/E22 pins + replay-with-drops pin (the contracts landed here, the QoS contract home; `flow_test.odin` stayed unmodified)
- [x] `core/catalog_test.odin` -- fail-fast rows for the new keys
- [x] `app/render/view.odin` -- the spatial-lane render: `bundle_lane_caps` helper + 3 lateral lane strokes per bundle (always, width = share) + packet lateral offset by lane (queued packets pile by lane at nodes) -- the canon visual
- [x] `harness/demo.odin` + `harness/run.odin` -- optional spawn class (back-compat: defaults to email)
- [x] `demos/qos_contention.dem` (NEW) -- oversubscribe a pipe with email(BE)/streaming(E) traffic; captures show the queue + BE-first drops WITH packets in lanes
- [x] Golden pass -- run ALL demos; re-bless deliberately: new demo blessed; catalog_hash header re-bless (T1) + full T2 re-bless for pipe demos (spatial-lane canon repaint); any further per-tick T1 shift documented (expected: ecmp/qos/qos_emphasis where contention engages)

**Acceptance Criteria:**
- Given `qos_serialize` + the cyclic service, when a pipe carries multi-lane traffic, then packets exit in lane order with no starvation under continuous Express (E7); a lone packet in any lane crosses at full capacity.
- Given a full (bundle, lane) queue, when a new packet would join, then the E9 ladder sheds the lowest-priority non-empty lane's newest packet; the arrival drops when it is the shed target; every emptiness combo is pinned.
- Given the pool at `pool_max_packets`, when a spawn arrives, then E22 drops the lowest-priority lane first; every drop emits `Packet_Dropped{class, reason}` and the run replays byte-identically (E10).
- Given the new `qos_contention.dem`, when run through the harness, then its T1 + T2 goldens are blessed deliberately; existing demos' T1 hashes shift ONLY where contention genuinely engages (documented) + the catalog_hash header re-bless; T2 pixels re-bless across all pipe demos (the spatial-lane canon repaint, documented).
- Given the app, when a pipe is oversubscribed, then best-effort packets visibly drop first, the queue exits in lane order, and packets ride their painted lane end-to-end (the launchable increment).

## Spec Change Log

- 2026-08-12 (mid-work canon, user ruling): base moved to `2e3acab` (spatial lanes —
  three painted lane strokes per pipe, packets ride their lane) then `8ece056` (no
  auto-assigned lanes — every type rides Standard until the player categorizes; lane
  speed = priority — motion is a per-lane readout). Amendments: the render became a
  first-class deliverable (view.odin strokes + lateral offsets + lane-speed fraction),
  `default_lane` is pinned to Standard at catalog load (the sim never assigns lanes),
  all pipe-containing T2 goldens re-bless by canon, and the spec body above was updated
  in place. The service model, bounds, ladders, and T1-stability mechanism are
  unchanged by the canons.

- 2026-08-12 (step-04 review swarm, 2 hunters): (a) E22's shed rule was
  `shed_lane != arrive_lane` — priority-inverting (an Express resident could pay for a
  Standard arrival); corrected to STRICTLY-lower-priority-only (`shed_lane > arrive_lane`)
  + a pin (Case C). (b) The Packet_Arrived event moved to the cull pass — the same-tick
  event stream is spawn-ordered again (the 2.x single-pass order), so event ordering can
  never shift a T1 on its own. (c) Zero-share-lane wording corrected: the bands abut, so
  no base/core peek-through (comments + spec). (d) `lower_spawns` now propagates an
  unknown-class error like `lower_nodes` (was a silent demand truncation). KEEP: the
  cyclic-WRR service, the derived-state golden mechanism, the E9 ladder + pending-drop
  exclusion, the ascending-sort splice, per-bundle queues, the spatial-lane render.

## Design Notes

- **Cyclic WRR windows are the work-conserving gap-fill.** One window = one E→S→B walk; each ready lane gets its WFQ budget (floor 1 when zero); empty lanes are skipped so their budget flows to the next ready lane in the walk. Windows repeat until the bundle's capacity is consumed. This is why a lone packet in ANY lane gets the full capacity (the prototype's downward-only carry starved a lone Express packet — rejected). Known, documented bias: when Best is empty, its budget flows to the next window's Express head (Express-favored), never starving Standard/Best (the floor).
- **Golden-stability mechanism (mirrors 3.2's sparse serialization):** all 3.3 state is derived — queue membership is `(on_edge, edge)`, lanes are `qos_lane_of`, budgets are `lane_caps` + `qos_serialize`. No Packet fields, no Flow_State serialized fields, no new commands (LOG_VERSION stays 3). The drop event payload writes only for the new tag. T1 shifts ONLY when packets genuinely share a pipe (ecmp's 2-apart spawn pairs if the ECMP hash collides them; qos/qos_emphasis era-3 traffic saturates) — that shift IS the story, documented in the PR.
- **Spatial lanes (canon 2e3acab):** the band layout (three lateral strokes + per-lane band centers) is a pure function of (Σ member `lane_caps`, pipe width) — shared by draw_bundles (strokes) + draw_packets (packet offset). Replaces 3.2's length-proportional segments. 3.2's default-pipe-unchanged rule is superseded: strokes draw on every pipe (a balanced pipe = three equal strokes). The base tier-color pipe draws underneath (a zero-share lane shows the base — "demoted to nothing").
- **Splice, don't flag:** a dropped packet is removed from `f.packets` (order-preserving shift, collected indices applied descending after the forward pass) — no `delivered` misuse, no new fields. Arrivals still increment `score`; drops never do.
- **Lane of a queued packet** = `qos_lane_of(t, cat, p.edge, p.class)` (its own representative pipe — per-pipe overrides hold per member of a bundle). At-node packets use the class `default_lane` for the E22 ladder only.
- **Demo:** `qos_contention.dem` — fixture qos + 0-1/1-2/3-1/4-1 draws; `lane` overrides put email on Best-effort + streaming on Express on pipe 0; ~50ms spawn bursts both ways 0↔2 oversubscribe pipe 0; captures show the pile + BE-first drops, packets visibly in their lanes. The `spawn <class>` extension is harness-only (run setup rides both live + replay paths — safe).

## Verification

**Commands:**
- `odin test core -debug` -- all suites green incl. the new E7/E9/E22 pins
- `tools/lint.sh` -- all 5 gates green
- `tools/harness.sh run` -- all demos PASS (T1 + T2 re-blessed deliberately per the canon + contention documentation)
- `tools/harness.sh save qos_contention` -- bless the new golden, then `tools/harness.sh run` again -- PASS
- `tools/harness.sh drift-check` -- every mutation rejected
- `odin build app` + run -- oversubscribe a pipe → best-effort drops first, the queue exits by lane
