---
title: 'Packet Plumber — Stories v2 (vertical-slice, from-scratch)'
project: 'packet-plumber'
date: '2026-08-11'
author: 'Moses (via packet-plumber-sprint-replan-v2 minion)'
version: 'v2'
status: 'lavish sign-off 2026-08-11 (slice structure APPROVED: 1A shape, 2B headless-first 1.1, 3A keep era slice 6)'
supersedes: '_bmad-output/planning-artifacts/sprints/stories-v1.md (horizontal, Godot/GDScript + BFS/RR-LB)'
workflow: 'gds-sprint-planning (re-plan) + lavish (slice-structure review)'
---

# Packet Plumber — Stories v2

> **What this document is.** The buildable story cards for Packet Plumber's vertical-slice
> build, written one card per story with **Given/When/Then acceptance criteria**, each
> mapped to an architecture system (S1–S8 + harness) and pinned to at least one edge-case
> contract `[E#]` (arch §11.7). The **slice sequence + slice-level rationale** lives in
> `sprint-plan-v2.md`; this file expands each story into an independently-completable,
> minion-sized card. **It re-decides nothing** — forge locks `[FORGE #n]`, GDD design
> `[GDD §]`, architecture decisions `[ODN-n]`, the routing ruling `[RR]` (lavish 2026-08-10),
> and the six-mechanics ruling (decision-log 2026-08-10) are cited, never reopened.
>
> **Card format:** each story carries — **Slice**, **Epic(s)**, **Goal**, **Given/When/Then**
> acceptance criteria, **Architecture system(s)**, **Edge-case contracts**, **Golden** (the
> replay-equality / visual contract), and **Launchable increment** (what you can run + see
> after the story lands). **Notation:** `[Arch S#]` = architecture system; `[ODN-n]` =
> architecture decision; `[E#]` = edge-case contract; `[RR]` = routing ruling; `[GDD-inv]`
> = GDD-pinned invariant. MVP = slices 1–7 (epics E1–E9) — the full game's core, ending at
> the **fun-test gate** (the content greenlight, decision-log 2026-08-17); slice 8+ = the
> six mechanics (post-fun-gate); slice N = E10 + the carried-forward E11 features (no
> rebuild — v2 IS the full-game build).

> **Fresh-minion-per-story.** Each story is sized for one fresh minion (bmad-create-story →
> bmad-dev-story); Gru dispatches one at a time as the prior merges. A minion badges out its
> own field-note shard per story — the learning loop depends on this granularity.

---

## Slice 1 — Walking skeleton → thinnest playable thing

*The determinism spine + minimal fresh harness live in story 1.1 (headless — lavish choice
2B); the first runnable `app.bin` lands in 1.2; slice 1 ends at the thinnest playable loop.*

### Story 1.1 — Walking skeleton (headless spine + harness)

- **Slice:** 1 · **Epic(s):** S0 (foundation) · **Systems:** core scaffold, Rng `[ODN-9]`,
  save/log `[ODN-11]`, harness `[ODN-17]`.
- **Goal.** The pure `package core` scaffold + the seeded-RNG with pinned test vectors + the
  state-hash + the binary action-log, and the golden-image harness skeleton (software-raylib
  build, T1 manifest compare, the replay gate, one trivial `boot.dem`) — all **headless**, no
  window yet. The determinism spine + replay-equality contract **proven** before any window.

**Given/When/Then:**
- **Given** the Odin `package core` scaffold (`Run_State`, `step` no-op, `state_hash`,
  `log_read`/`log_write`), the owned `Rng` (splitmix64 → PCG32 XSH-RR, ~40 lines, constants
  in source), and the harness skeleton (`tools/build_raylib_sw.sh` software renderer + memory
  platform; T1 manifest path `goldens/<demo>.t1`; the replay gate over `log.bin`);
- **When** `odin test core` runs the Rng test vectors and the replay-equality test, and
  `odin run harness -- run boot` replays the trivial `boot.dem` (seed, empty map, N ticks,
  capture);
- **Then** the Rng's first 8 outputs match the pinned vectors `[ODN-9]`; re-stepping
  `(seed, action_log)` twice yields **byte-identical** `state_hash` sequences `[E10, ODN-10]`;
  `package core` compiles to an object file with **no `vendor:*`/`core:os`/`core:time`**
  symbols `[ODN-1]`; the harness's T1 manifest for `boot.dem` matches on re-run; the replay
  gate reproduces the manifest from the action log alone, and **rejects** catalog/logic_hz
  drift `[ODN-11]`.

- **Edge-case contracts:** `[E10]` (replay determinism). **Golden:** T1 manifest for
  `boot.dem` (per-tick FNV-1a-64 hashes, incl rng + events).
- **Launchable increment:** `odin run harness -- run boot` green + `odin test core` green —
  the headless spine + harness foundation. (No window yet — deliberate, lavish choice 2B;
  first runnable `app.bin` in 1.2.)

### Story 1.2 — Window + static render + draw one pipe

- **Slice:** 1 · **Epic(s):** E1.1, E1.2 · **Systems:** Topology (S1 minimal), Command_Bus,
  Input (mouse) `[ODN-12]`, render passes 1–4 (camera-fit, map, pipes, nodes).
- **Goal.** The first runnable `app.bin`: a 1280×720 window rendering a hardcoded static
  fixture (1 source, 1 router, 1 sink), and mouse drag-draw with snap-to-node that creates a
  pipe via the validated Command_Bus + the edit fast-path.

**Given/When/Then:**
- **Given** the static map fixture and the Topology SOA model (node/pipe arrays, adjacency,
  integer-grid positions), the Command_Bus (snap-to-node inclusive at radius, validate-then-
  apply), and the edit fast-path (apply this frame, log `apply_tick = next`);
- **When** the player drags from the source toward the router (within the snap radius) and
  releases, then repeats router→sink;
- **Then** two pipes are created and **appear instantly** (same frame); a self-loop drag
  (node→itself) is rejected with `.Self_Loop` `[E3]`; a terminal↔terminal drag is rejected
  with `.Terminal_To_Terminal` `[E26]`; a span-exceeding drag is rejected; replay applies all
  log entries for tick N before stepping N → **live and replay see identical state at every
  step boundary** `[ODN-2]`; pipe/node ids are monotonic, never recycled `[E11]`; the
  re-rendered frame matches the T2 pixel golden.

- **Edge-case contracts:** `[E3]` self-loop, `[E4]` snap inclusive, `[E11]` monotonic ids,
  `[E26]` terminal-pair. **Golden:** T1 (drawn topology in the hash → replay-equality) + T2
  (the drawn-pipe frame).
- **Launchable increment:** `odin run app` opens the window, shows the map, and you can drag
  source→router→sink and watch the pipes appear. (First playable `app.bin`.)

### Story 1.3 — One packet flows (per-hop forwarding, you see it move)

- **Slice:** 1 · **Epic(s):** E1.4 · **Systems:** Flow (S2 trivial), per-hop forwarding
  table, render pass 5 (packets).
- **Goal.** A packet spawns from a trivial hardcoded demand and **travels source→router→sink
  along the drawn graph**, forwarded per-hop via a forwarding table — the locked routing model
  in its trivial single-path form (no ECMP/bundles yet, but **no spawn-cached BFS route, no
  LB** either).

**Given/When/Then:**
- **Given** the Flow step (spawn from hardcoded demand, advance by bandwidth-units/tick,
  deliver at sink), a forwarding table per junction `(junction, dst) → next hop` computed by a
  deterministic SPF (insertion-order tie-breaks), and packet-dot rendering at lerped positions
  between snapshots;
- **When** the packet advances each tick toward the sink;
- **Then** the packet visibly travels source→router→sink (the dot moves between snapshots);
  the forwarding table is **rebuilt only on a topology-changing Command, synchronously inside
  the tick** (4-rule spine rule 1) `[ODN-10]`; the packet's path is captured in the state hash
  → replay-equality holds `[E10]`; on a demolish that severs the path, the packet re-forwards
  at the next junction (no stale spawn-time route) `[E29, RR]`.

- **Edge-case contracts:** `[E10]` replay, `[E29]` auto-migration. **Golden:** T1 (the
  packet's path in the hash) + T2 (packet mid-traversal frame); forwarding-table-rebuild-on-
  topology-change unit test.
- **Launchable increment:** run the app; the packet visibly travels the route you drew.

### Story 1.4 — Win/lose stub (the thinnest feedback loop)

- **Slice:** 1 · **Epic(s):** E6 (stub) · **Systems:** App mode FSM `[ODN-13]`, game-over/
  retry flow.
- **Goal.** The thinnest loop: deliver N packets → WIN; tick cap with <N delivered → LOSE
  (Error 404 stub); retry resets. No SLA meter, no surge yet — the skeleton the real win/lose
  (slice 4) grows onto.

**Given/When/Then:**
- **Given** the App mode FSM (`Boot/Run/Game_Over`) and a hardcoded session (deliver-N win,
  tick-cap lose);
- **When** the player delivers N packets (or hits the tick cap with <N);
- **Then** a WIN (or LOSE/Error 404) toast appears and the app transitions to `Game_Over`;
  retry creates a **fresh run context** in a fresh arena (no state leakage) `[ODN-13]`; the
  game-over frame matches the T2 golden; the terminal-event barrier emits exactly one terminal
  event per run `[E17]`.

- **Edge-case contracts:** `[E17]` terminal barrier. **Golden:** T1 + T2 of the game-over
  frame; retry-restores-clean-state test.
- **Launchable increment:** run the app, play the trivial loop, see WIN or LOSE, retry.

**→ Slice 1 exit:** the thinnest playable thing, golden'd end-to-end. The determinism spine
+ harness + replay-equality are **proven** (1.1) and the game is **runnable + playable**
(1.2–1.4).

---

## Slice 2 — Routing the locked way: per-hop forwarding + ECMP + bundles

*The locked full-game routing model `[RR]` — redundancy becomes active capacity the moment a
second pipe is drawn. The locked model was present trivially in slice 1; slice 2 exercises it
(ECMP across equal-cost; bundles across parallel pipes).*

### Story 2.1 — Parallel-pipe bundles (cap = sum)

- **Slice:** 2 · **Epic(s):** E1.5, E1.4 · **Systems:** Topology bundles (S1), render bundle
  viz.
- **Goal.** Parallel pipes between a node pair **bundle into one pooled-capacity link** (cap =
  sum of members), derived from adjacency at table-build. The "pop bigger" merge juice when
  pipes join a bundle.

**Given/When/Then:**
- **Given** the Topology derives bundles (all pipes between a node pair = one pooled link) and
  computes the bundled capacity as a **static sum at table-build time** (4-rule spine rule 3);
- **When** the player draws a second pipe parallel to an existing one between the same pair;
- **Then** the two pipes **bundle into one pooled link** (cap = sum) with a merge "pop"
  animation; the routing sees one fat edge per pair (no LB — round-robin/weighted LB are
  **deleted**, grep-gated absent) `[RR]`; the bundle-capacity-equals-sum unit test passes;
  the bundled-link frame matches the T2 golden.

- **Edge-case contracts:** bundle cap = sum `[RR, ODN-10]`. **Golden:** T1 (bundle state in
  the hash) + T2 (the merge-pop frame).
- **Launchable increment:** draw a parallel pipe → watch it bundle into a fatter pooled link.

### Story 2.2 — ECMP across equal-cost next hops

- **Slice:** 2 · **Epic(s):** E1.4 · **Systems:** Flow ECMP (S2) `[ODN-9/10]`.
- **Goal.** Among N equal-cost next hops, the pick is a **pure hash** `splitmix64(src, dst,
  class, pkt_id) mod N` — deterministic per packet (flow affinity, no intra-flow reordering),
  no sim-rng draw, no map iteration in the hot path (4-rule spine rule 2).

**Given/When/Then:**
- **Given** a forwarding table that exposes equal-cost next-hop sets and the ECMP hash;
- **When** the player draws a diamond topology with two equal-cost paths and packets flow;
- **Then** packets **deterministically spread** across the two equal-cost paths via the hash;
  the **same packet always takes the same path** on every replay (flow affinity, no intra-flow
  reordering); re-running `(seed, action_log)` yields **byte-identical per-packet paths**
  `[E10, ODN-10]`; the ECMP-determinism unit test passes.

- **Edge-case contracts:** `[E10]` replay, `[RR]` ECMP hash. **Golden:** T1 (per-packet paths
  in the hash) + T2 (packets split across paths).
- **Launchable increment:** draw a diamond topology → watch packets ECMP-spread
  deterministically.

### Story 2.3 — Demolish + severance under bundles + automatic migration

- **Slice:** 2 · **Epic(s):** E1.3, E1.4 · **Systems:** Topology demolish (S1), Flow reroute
  (S2).
- **Goal.** Demolishing a pipe of a bundle **shrinks the pool gracefully** (only full-bundle-
  loss drops the route) `[E1, RR]`; terminal-demolish forbidden; junction demolish = atomic
  batch; route migration is automatic (re-forward at the next junction, no stale routes).

**Given/When/Then:**
- **Given** a bundled link (2 pipes) carrying traffic and the demolish/reroute logic;
- **When** the player demolishes one pipe of the bundle (and, separately, attempts a
  terminal/junction demolish);
- **Then** the bundle's capacity shrinks (graceful), traffic continues (no hard cut) — only
  **full-bundle-loss drops** the route `[E1, RR]`; a terminal-node demolish is rejected with
  `.Terminal_Demolish` `[E2]`; a junction demolish is an **atomic batch** (incident pipes
  first in edge-id order, each per E1, then the vertex) `[E27]`; in-flight packets **re-forward
  at the next junction** (no stale spawn-time routes) `[E29]`; replay is byte-identical.

- **Edge-case contracts:** `[E1]` severance-under-bundles, `[E2]` terminal-forbidden, `[E27]`
  junction-batch, `[E29]` auto-migration. **Golden:** T1 + T2 of the post-demolish state.
- **Launchable increment:** demolish a bundled pipe → watch capacity shrink gracefully,
  traffic reroute.

**→ Slice 2 exit:** the locked routing is real and exercised. Redundancy is active capacity;
ECMP spreads deterministically; demolish is graceful under bundles. The routing that makes
Packet Plumber a *routing* game is in place.

---

## Slice 3 — QoS: packet types + lanes (the differentiator)

*Packets have needs; the player engineers priority `[FORGE #4]`. Email + streaming, all
starting on Standard. QoS procs live **inside** Flow (not a peer system) `[ODN-3]`.*

### Story 3.1 — Packet types + demand-pairing data

- **Slice:** 3 · **Epic(s):** E2.1, E2.4 · **Systems:** catalogs `[ODN-5]`, Flow spawn,
  director `[ODN-7]`.
- **Goal.** The `packet_types` catalog (email + streaming) and the demand-pairing data
  (`DemandPlan`/`DemandSpec`/`SetPiece`, carried from v1 §3, Odin-native): per-source-class
  demand with typed source/sink selectors + WEIGHTED_RANDOM dst selection (seeded).

**Given/When/Then:**
- **Given** the catalogs (email: low/low/low; streaming: med/med/high) and the
  `scripted_plan_demand` director (read-only topology view in, `DemandPlan` out);
- **When** the flow spawns packets each tick per the demand plan;
- **Then** two packet types flow with distinct shapes/icons (never color alone); the `(class,
  src, dst)` spawn sequence is **byte-identical** across runs for a fixed seed `[E10]`; the dst
  distribution over many packets matches the sink `demand_weight`s ± tolerance (the v1 §3.3
  pinned test); catalogs are integer-only for sim values + fail-fast validated at load
  `[ODN-5]`.

- **Edge-case contracts:** `[E10]` replay, dst-selection determinism. **Golden:** T1 + T2 of
  two packet types flowing.
- **Launchable increment:** run the app; two packet types (distinct shapes) flow with demand.

### Story 3.2 — 3-class-queue QoS + emphasis dial

- **Slice:** 3 · **Epic(s):** E2.2 · **Systems:** QoS `[ODN-3]`, emphasis-dial UI.
- **Goal.** Each pipe carries 3 class queues (Express/Standard/Best-effort); bandwidth partitions by
  integer WFQ weights via a single "priority emphasis" dial → weight presets. All traffic
  starts Standard; the player promotes/demotes.

**Given/When/Then:**
- **Given** the `qos_allocate` proc (integer WFQ, largest-remainder, E→S→B tie order) and the
  emphasis dial (maps to weight presets in `balance.json`);
- **When** the player sets a pipe's emphasis (e.g. express-heavy);
- **Then** the pipe's **three painted lane strokes' widths + packet distribution** visibly
  change (spatial lanes — packets ride in their lane, user ruling 2026-08-12); **no traffic
  auto-assigns: every type rides Standard until the player categorizes it** (per-type, with
  per-pipe override); allocation is **weight-only** (demand is not an input) `[ODN-3]`;
  all-zero weights → the catalog default preset `[E5]`; a never-drop class lane is
  **floored** and the zeroing edit is rejected `[E6]`; the largest-remainder distribution
  test passes `[E8]`.

- **Edge-case contracts:** `[E5]` all-zero fallback, `[E6]` never-drop floor, `[E8]`
  largest-remainder. **Golden:** T2 of lane proportions changing (painted lane widths +
  packet lane-positions).
- **Launchable increment:** set a pipe's emphasis → watch the three painted lanes' widths
  and the packets riding them change.

### Story 3.3 — Node serialization + contention drop precedence

- **Slice:** 3 · **Epic(s):** E2.3 · **Systems:** QoS serialize, Flow contend/drop.
- **Goal.** At each node, packets serialize by lane (Express → Standard → Best), work-
  conserving with gap-fill + a WRR floor (no starvation); under contention, drops by the full
  ladder BE → Standard → Express.

**Given/When/Then:**
- **Given** `qos_serialize` (work-conserving gap-fill + WRR floor: ≥1 slot per non-empty lane
  per window) and the contention drop logic;
- **When** a pipe is oversubscribed;
- **Then** packets visibly queue and exit in lane order at nodes (the serialization visual),
  **riding their painted pipe lane end-to-end at lane speed** (spatial lanes, user ruling
  2026-08-12: 3 lane strokes per pipe, packets laterally offset into their lane; **Express
  fastest, Best-effort slowest**); there is **no starvation** under continuous Express
  `[E7]`; drops occur by the full ladder BE → Standard → Express `[E9]`; pool-exhaustion
  drops the lowest-class queue first `[E22]`.

- **Edge-case contracts:** `[E7]` no-starvation, `[E9]` drop precedence, `[E22]` pool. **Golden:**
  T2 of the queue + drops (packets visible in their lanes end-to-end).
- **Launchable increment:** oversubscribe a pipe → watch best-effort drop first, see the
  queue serialize by lane.

### Story 3.4 — Per-class SLA

- **Slice:** 3 · **Epic(s):** E2.4 · **Systems:** SLA accumulators (inside Flow) `[ODN-3]`.
- **Goal.** Per-class SLA accumulators (delivered/dropped/total_latency_ms/demand_seen) fed
  inside `flow_step`; breach crossing is attributable to a class.

**Given/When/Then:**
- **Given** the SLA accumulators as fields of `Flow_State` (no `state.sla` peer) `[ODN-3]`;
- **When** packets are delivered/dropped and latency accrues;
- **Then** per-class SLA gauges read correctly; latency is tracked in **integer ms** (sub-tick
  resolution) `[ODN-2, m16]`; a **zero-demand tick is neutral** `[E24]`; a breach crossing is
  detectable and attributable to a class.

- **Edge-case contracts:** `[E24]` zero-demand-neutral, `[ODN-2]` ms-latency. **Golden:** T1
  (SLA state in the hash).
- **Launchable increment:** see per-class SLA gauges update as traffic flows.

### Story 3.5 — Node placement: the router toolbox (restore from prototype)

- **Slice:** 3 · **Epic(s):** E2.1, E3.1 · **Systems:** Command_Bus `[ODN-12]`, Topology
  (S1), tray view (S2).
- **Goal.** The player **places junctions (routers)** from a hardware tray to design the
  network; **terminals are never player-placed** — the director spawns them (5.1). Port
  `Cmd_Place_Router` + the tray + placement mode from the prototype
  (`origin/odin-prototype`: `app/main.odin` placing-state + tray chips,
  `core/command.odin` `Cmd_Place_Router`, tray render in `app/render/hud.odin`), which the
  v2 vertical-slice fixture dropped. *(GDD canon: the build/redesign cadence and
  topology-flaw crises presume a player-designed network; the prototype proved placement;
  the 1.2 fixture + 5.1 passive growth silently removed it — restored here, user ruling
  2026-08-12.)*

**Given/When/Then:**
- **Given** the hardware tray (link chips: draw tier; **router chips: arm placement**) and
  the Command_Bus validate→apply path (edit fast-path `[ODN-2]`);
- **When** the player picks a router chip (click again/ESC/right-click cancels) and clicks
  the map;
- **Then** a junction spawns, validated (span + min-separation from existing nodes, no
  overlap, placement area rules); the edit lands immediately (fast-path) and is recorded
  in the action log — `LOG_VERSION` bump per the story-1.2 precedent (`serialize.odin`
  command-kind switch) so **same seed + same commands → identical map** `[E10]`; placed
  routers are connectable by the existing drag-draw; junction **port limits** (GDD: basic
  4 / mid 8 / high 16) apply to what connects after placement.

- **Edge-case contracts:** `[E10]` replay, `[ODN-2]` fast-path, port limits. **Golden:** T2
  of placing a router + drawing a pipe to it.
- **Launchable increment:** run the app → place routers from the tray, connect them,
  demolish and redesign.

**→ Slice 3 exit:** the differentiator is live. Two packet types, player-engineered QoS,
visible serialization, contention drops, attributable SLA, **player-placed network design
(3.5)**.

---

## Slice 4 — The surge-survival fun loop (win/lose closes)

*The earliest fun-test — the gate question ("is surviving a bandwidth surge fun?") becomes
askable. Reached through three prior playable slices. `[FORGE #3]`*

### Story 4.1 — Warning signs + forecast

- **Slice:** 4 · **Epic(s):** E4.1, E3.4 · **Systems:** Crisis warnings (S4), forecast UI.
- **Goal.** Strain metrics from Topology + Flow → warning signs (🟡/🔴 node, pipe congestion,
  demand forecast) with lead times; a forecast "weather report" panel (the P3 fairness
  surface — color never sole encoder).

**Given/When/Then:**
- **Given** the congestion metrics + the warning-sign system + the forecast panel;
- **When** congestion rises toward a threshold;
- **Then** warnings **derive from measurable congestion** (utilization vs throughput) and carry
  lead times `[FORGE #3]`; node health transitions fire on defined thresholds and a 🔴 node is
  always traceable to a measured congestion; the forecast names incoming SetPieces with a
  countdown; color is never the sole encoder (icon + shape + outline).

- **Edge-case contracts:** `[FORGE #3]` fair/predictable. **Golden:** T1 + T2 of the forecast
  + warning state.
- **Launchable increment:** see the forecast + congestion telegraph before trouble.

### Story 4.2 — Surge SetPiece + Crisis Engine (root-cause, fair)

- **Slice:** 4 · **Epic(s):** E4.2, E4.3 · **Systems:** Crisis Surge (S4) `[ODN-4]`, director.
- **Goal.** The Surge archetype: a forecast 10× demand spike that cascades into saturation if
  the player is unprepared. Fires on schedule from the seed. Every crisis carries a structured
  `root_cause` (ref to the topology flaw) + a `preventive_redesign`.

**Given/When/Then:**
- **Given** the Surge SetPiece (in `crises.json`) + the Crisis Engine (downstream of flow,
  read-only topology view) `[ODN-4, REVIEW M1]`;
- **When** the surge SetPiece activates on schedule;
- **Then** the surge fires on schedule from the seed (deterministic); **no crisis without a
  resolvable root cause** + preventive redesign; **no crisis on a healthy within-capacity
  topology** `[AC-E13]`; one crisis per root-cause per activation (dedup, re-trigger only
  after `Crisis_Resolved`) `[E13]`; the Director never reads crisis state (structural —
  read-only view in) `[ODN-7, REVIEW M1]`.

- **Edge-case contracts:** `[AC-E13]` root-cause/fair, `[E13]` dedup. **Golden:** T1 +
  event-stream golden (`Crisis_Triggered{Surge}` within the scheduled window).
- **Launchable increment:** the surge hits on cue; you can see WHY (the root cause).

### Story 4.3 — Network Health meter + win/lose/retry

- **Slice:** 4 · **Epic(s):** E6.1, E6.2, E6.3, E6.4 · **Systems:** Network Health (S5),
  win/lose/retry flow.
- **Goal.** The aggregate loss condition: a Network Health meter drains on SLA breach (grace
  countdown), recharges when healthy, empties → Error 404 → run over. Win = uptime ≥ 90%
  through the surge. Retry restores a clean state. No-soft-lock guaranteed.

**Given/When/Then:**
- **Given** the Network Health meter (drain/grace/recharge) + the win/lose thresholds;
- **When** an active class's SLA breaches (sustained);
- **Then** a grace countdown starts; drain = **max(severity) + per-tick cap** (never instant)
  `[E16]`; SLA hysteresis (enter/exit thresholds), re-breach during active grace = no-op
  `[E30]`; the meter recharges when healthy; empty meter → `Run_Lost` (Error 404); the
  terminal-event barrier skips the rest of the tick after `Run_Lost` — **one terminal event
  per run** `[E17]`; **win fires at uptime ≥ 90%** through the surge; retry creates a fresh
  run context (no leakage); the **no-soft-lock property test passes** `[FORGE #3]`.

- **Edge-case contracts:** `[E16]` drain, `[E17]` terminal barrier, `[E30]` hysteresis,
  no-soft-lock. **Golden:** T1 + T2 of win + lose frames; no-soft-lock property test.
- **Launchable increment:** play the full surge-survival loop — predict, survive or drain,
  win/lose, retry.

**→ Slice 4 exit: THE FUN-TEST LOOP.** The gate question can be asked. Reached through slices
1–3, each independently playable.

---

## Slice 5 — Growing map + health telegraph + input parity

*The Mini Motorways feel: a growing map, telegraphed trouble, pause-and-plan, the same game
on touch + controller.*

### Story 5.1 — Deterministic map growth + spawn validity

- **Slice:** 5 · **Epic(s):** E3.1, E3.2 · **Systems:** Topology growth (S1), director
  `[ODN-7]`.
- **Goal.** Nodes appear over time (Mini Motorways model), deterministically from the seed;
  growth proceeds outward from the router mesh; every spawned terminal is connectable.
- **Status:** implemented 2026-08-15 — PR open (the director's map-growth branch
  `growth.odin`, ODN-7: one terminal per 6 s window from the executed tick, TERMINALS only
  — routers never director-spawned, the 3.5 amendment — biased outward from the
  player-placed router mesh; E31 spawn validity with bounded rejection sampling from the
  same rng stream; growth fully seed-derived — NO action-log entries, NO LOG_VERSION bump;
  the `growth.dem` T1+T2 goldens, replay byte-identical, existing goldens unshifted).

**Given/When/Then:**
- **Given** the director's `demand_plan` (seeded) driving map growth via Topology;
- **When** new nodes spawn over time;
- **Then** the same seed → **identical map-growth timeline**; growth proceeds **outward from
  the player-placed router mesh** (terminals spawn; **routers are NEVER director-spawned —
  the player places them, story 3.5**); every spawned terminal is
  connectable-within-span + min separation, else **rejection-sampled from the same rng
  stream** (deterministic) `[E31]`; replay is byte-identical.

- **Edge-case contracts:** `[E31]` spawn-validity. **Golden:** T1 + T2 of a growing map.
- **Launchable increment:** nodes appear over time, the map grows.

### Story 5.2 — Node health states

- **Slice:** 5 · **Epic(s):** E3.3, E3.4 · **Systems:** Topology (S1), Crisis (S4).
- **Goal.** Node health states (🟢 healthy → 🟡 congested → 🔴 critical) driven by utilization
  vs throughput; readable at a glance (icon + outline, never color alone).

**Given/When/Then:**
- **Given** the health-state model + the readability canon;
- **When** utilization crosses thresholds;
- **Then** health transitions fire on defined thresholds; a 🔴 node is always traceable to a
  measurable congestion; state is readable without color (icon + outline + pulse).

- **Edge-case contracts:** health-on-thresholds, 🔴 traceable. **Golden:** T2 of health
  states.
- **Launchable increment:** watch nodes telegraph trouble (🟡→🔴) under load.
- **Status:** implemented 2026-08-16 — PR open (the per-node health layer `core/node_health.odin`
  beside the 4.3 health module: the never-serialized tri-state `crisis.node_health` derived
  per tick from the un-forwardable pile vs the node's throughput ceiling — the balance
  `warnings` 70/90 thresholds shared with the 4.1 congestion, coherence by construction; a
  transit-inclusive "utilization" was measured and REJECTED — the health_win fan's routers
  hold 0–3 transit packets (75–225%) mid-surge with the meter at 100, so any transit-queue
  measure makes the healthy map scream. The surface: the existing ring + glyph + pulse
  telegraph now reads the health state (pixels unchanged — the arrays measure identically),
  plus the hover TRACEABILITY card (state name + util % / load / throughput — the numbers
  that put a node red). Derive-don't-record: node_health never enters the save format (the
  serializer writes only node_congestion/pipe_congestion/forecast/active), proven by replay identity
  + a byte-dump negative control; no LOG_VERSION bump. The `node_health.dem` T1+T2 goldens
  (amber pin @t1, red host + growth-born red @t200, host resolution @t400 — growth-born
  nodes included, 5.1 coherence); existing suite unshifted (28/28 + the new demo green).
  The 3 node_health T2s were re-blessed after the #52 Open Sans font merge (deliberate
  presentation-only fold — the font swap shifted the HUD text bands; T1 + replay logs
  byte-identical, the world-pass telegraph pixels unchanged).
  Traceability numbers + transitions pinned by `node_health_test.odin`; the app's hover
  card is capture-safe (app-layer only).)

### Story 5.3 — Pause-anywhere

- **Slice:** 5 · **Epic(s):** E7.4 · **Systems:** RunController.
- **Goal.** Pause freezes the sim deterministically; crises tick only unpaused (fairness +
  accessibility — pause-and-plan works, even mid-crisis). *(Dispatched early — user order
  2026-08-14: pause-and-plan is needed for router placement + link upgrades. Key: **P /
  Space**.)*
- **Status:** implemented 2026-08-14 — PR open (P / Space toggle in Run; the edit fast-path
  pause-aware apply-tick lowering `[ODN-2]`; the `pause.dem` T1 golden — the sim frozen across
  the mid-crisis pause window as one repeated state hash, resume from the exact tick, replay
  byte-identical). **Presentation ruling 2026-08-14 (user, `v2-5.3-pause-ux`):** the paused
  overlay is now NO overlay — full-brightness world (no dim veil, no centered PAUSED text;
  prototype-aligned), with a small edge chip indicator ("PAUSED — P/Space to resume") in the
  top HUD band; GDD + art-direction canon lines amended accordingly.

**Given/When/Then:**
- **Given** the pause control + the run controller;
- **When** the player pauses (even mid-crisis);
- **Then** stepping freezes deterministically (no drift on resume); the edit fast-path still
  applies edits while paused `[ODN-2]`; resume continues from the exact tick.

- **Edge-case contracts:** pause freezes stepping deterministically. **Golden:** T1 (paused
  state stable).
- **Launchable increment:** pause-and-plan works, even mid-crisis.

### Story 5.4 — Touch + controller parity

- **Slice:** 5 · **Epic(s):** E7.1, E7.3 · **Systems:** Input parity `[ODN-12]`.
- **Goal.** The same game on touch + controller, via the intent layer (new device mappings
  onto the same intents; parity by construction `[FORGE #6]`).
- **Status:** implemented 2026-08-16 — PR #57 open, in review (the `app/input` intent layer:
  raw device
  events → typed `Intent` → one shared validated-Command executor; mouse behavior preserved
  exactly, touch (drag-draw/tap-select/two-finger-pan) + controller (node-select/aim-confirm/
  tier-class-cycle) map onto the same intents; `harness input-parity` — the T1 across-inputs
  golden: scripted device-event frames assert mouse == touch == controller command + hash
  streams, blessed as `goldens/input_parity_*.t1`; no `LOG_VERSION` bump — inputs are never
  serialized; Perkins r1-r3 review rounds folded — 22 parity scenarios green). **Scope flag:**
  two-finger pan maps to the `Pan` intent but the camera-fit view
  has no pan state — a deliberate no-op, flagged per `[§18 OQ-1]` (camera work is a later
  story, not this one).

**Given/When/Then:**
- **Given** the intent layer + touch (drag-draw, tap-select, two-finger pan) + controller
  (node-select, aim/confirm, tier/class cycling) mappings;
- **When** the player draws/selects via touch or controller;
- **Then** the resulting Commands are **the same shapes** as mouse `[ODN-12]`; landscape-only
  framing is a camera-fit decision (desktop-first launch) `[§18 OQ-1]`.

- **Edge-case contracts:** `[ODN-12]` input parity. **Golden:** T1 (same Command stream across
  inputs).
- **Launchable increment:** play on touch + controller, same as mouse.

### Story 5.5 — Demolish input surface (restore from prototype)

- **Slice:** 5 · **Epic(s):** E7.2, E7.4 · **Systems:** Input surface `[ODN-12]` (mechanic: 2.3).
- **Goal.** The demolish MECHANIC (2.3 — `Cmd_Demolish_Pipe`/`Cmd_Demolish_Node`, merged #27)
  finally reachable from the input surface: click-select a pipe or junction on every left
  release, see a demolish popover + the X/DEL key, and watch the topology respond
  (bundle shrink, atomic junction batch). The missing third step of 3.5's launchable
  ("place routers, connect them, demolish and redesign").
- **Status:** implemented 2026-08-17 — PR open, in review (the demolish surface rides the 5.4 intent
  layer: release-based click-select (junction → pipe → clear on every left release), the demolish
  popover button + X/DEL, the shared `popover_demolish_hit` positive path pinned (W1-r4 — junction
  button → `Cmd_Demolish_Node`, pipe twin → `Cmd_Demolish_Pipe`, mouse == touch == pad on the node
  leg), the controller leg (dpad select → X confirm), the CLI arg-validation leg pinned (r3-N7),
  `pipe_anchor` single-sourced in render (N2-r4 fold); existing commands only — no new command
  kinds, no `LOG_VERSION` bump, replay byte-identical; the 2.3 demos/goldens (`demolish_bundle`,
  `demolish_node`) carry the T1+T2 pins).

**Given/When/Then:**
- **Given** the release-based click-select surface (prototype Perkins r2 B2 pattern: node
  → pipe → clear, on EVERY left release);
- **When** the player selects a pipe or junction and demolishes it (popover button or
  X/DEL);
- **Then** the EXISTING `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node` submits through the
  validated edit fast-path + action log (replay byte-identical `[E10]`; **no new command
  kinds, no `LOG_VERSION` bump**); a pipe demolish shrinks its bundle gracefully (traffic
  continues — only full-bundle-loss drops the route `[E1]`); a junction demolish runs the
  atomic batch (incident pipes in edge-id order, then the vertex `[E27]`); terminals never
  show a demolish affordance (`.Terminal_Demolish` mirrored in the UI `[E2]`); demolish is
  disabled while placing (no collision with the 1/2 lane keys, the right-click dial, or
  placement mode).

- **Edge-case contracts:** `[E1]` `[E2]` `[E10]` `[E27]` `[E29]`. **Golden:** T1 + T2 of
  pipe-demolish under a bundle (capacity shrink) + T1 + T2 of the junction-demolish batch
  (the E27 batch ORDER is pinned by the core's 2.3 tests — the golden pins the batch's
  end state); existing goldens MUST NOT shift (app-layer-only change).
- **Launchable increment:** build a net, demolish a pipe of a bundle (watch the capacity
  shrink), demolish a whole junction (atomic batch).
- **Assumption:** no economy — no refund, no inventory (the prototype's "refund banked"
  copy does NOT apply; refunds land with the economy story).
- **Slice:** 5 · **Epic(s):** E1.3, E1.4 · **Systems:** Input `[ODN-12]`, Topology demolish (S1).
- **Goal.** The 2.3 demolish mechanic was core-built and tested but never reachable in play —
  restore the prototype's select→demolish interaction: click-select a pipe/junction (on every
  left release), demolish via a popover button and/or X/DEL; rejects surface the existing
  error strings; no refund copy (no economy yet).

**Given/When/Then:**
- **Given** a selected pipe/junction and the existing logged `Cmd_Demolish_*` commands;
- **When** the player demolishes (button or X/DEL);
- **Then** a bundle shrinks gracefully `[E1]`; a junction demolish is the atomic batch `[E27]`;
  terminals never show the affordance `[E2]`; replay is byte-identical `[E10]`.

- **Edge-case contracts:** `[E1]` `[E2]` `[E27]` `[E29]`. **Golden:** T2 pipe-demolish under a
  bundle + T2 junction batch.
- **Launchable increment:** demolish a bundled pipe → capacity shrinks gracefully; demolish a
  whole junction.

### Story 5.6 — Router tiers (mid/high) + placement separation

- **Slice:** 5 · **Epic(s):** E2.1, E3.1 · **Systems:** Catalogs `[ODN-5]`, Topology (S1), tray (S2).
- **Goal.** Canon (M3: 4/8/16 ports) promised router tiers; only `router_basic` shipped. Create
  `router_mid` (8 ports) + `router_high` (16) in `node_types.json` (the tray auto-chips), with
  capacity-scaled visuals (A3), free placement until the economy story `[ASSUMPTION]`.
  `[ASSUMPTION: throughput 80/160 (2× per tier, matching the 2× port ladder); era_introduced 3
  (the capacity-planning era — GDD is silent on tier eras, metadata only)]`. Plus the
  placement-separation rework (*user ruling 2026-08-14*): router↔router 4 tiles, router↔terminal
  snap floor + margin (~2) — data-driven in `balance.json`, playtest-tunable; terminals never
  block router placement.

**Given/When/Then:**
- **Given** the three router chips + kind-split placement validation;
- **When** the player places mid/high routers and draws to them;
- **Then** port ceilings enforce per tier (4/8/16 — `.Router_Ports_Full` at the right count);
  router↔router under 4 tiles rejects while router↔terminal at the floor accepts; replay is
  byte-identical `[E10]`; goldens re-bless only on a provable catalog-hash fold (4.3 discipline).

- **Edge-case contracts:** `[E10]`, port limits, kind-split separation. **Golden:** T2 mid+high
  placement, T2 8/16-port ceiling.
- **Launchable increment:** place a mid router, fill 8 ports, watch the 9th reject.

### Story 5.7 — Runtime telemetry (stats stream + debug overlay)

- **Slice:** 5 · **Epic(s):** E10-support · **Systems:** Logging `[§7.2]`, Events `[ODN-14]`, Debug
  tools `[§7.6]`.
- **Goal.** Realize arch §7.2/§7.6 (canon-specified, never scheduled): a deterministic per-tick
  stats stream (`--stats-out`, CSV or JSONL, replay-pinned) + a compile-gated debug overlay (`D`
  key, `-define:PP_DEBUG=true`): per-pipe readout, per-class table, congestion heat, global
  line, live event tail. Derived from existing deterministic state only — never wall-clock.

**Given/When/Then:**
- **Given** a live run (or a harness demo) + a PP_DEBUG build;
- **When** `D` toggles the overlay / the stream flag writes;
- **Then** the overlay shows real numbers (demand vs capacity, drops by class + reason,
  utilization heat); two runs of the same log produce byte-identical stream files (pinned);
  goldens never capture the overlay (default off).

- **Edge-case contracts:** replay-identical stream. **Golden:** stream byte-equality pin;
  existing goldens untouched.
- **Launchable increment:** run a congested demo — watch utilization + drops live, diff the
  stream across replays.

### Story 5.8 — QoS panel + assignment-driven auto-reservation

- **Slice:** 5 · **Epic(s):** E2.2 · **Systems:** QoS `[ODN-3]`, tray/panel UI (S2).
- **Goal.** Make QoS legible (*user ruling 2026-08-14*): a per-pipe QoS panel replaces the
  invisible emphasis dial — per-type lane rows, the resulting split with numbers, manual weight
  override. Auto-reservation (default): the split follows type→class-queue assignments from a fixed
  ladder (1 lane = 100 · 2 = 70/30 · 3 = 50/30/20; data-driven `balance.json`, playtest-tunable).
  The type→class-queue call stays player-owned; only the split auto-follows. Manual pipes marked +
  revertible.

**Given/When/Then:**
- **Given** a selected pipe + lane assignments;
- **When** the player assigns a type to a lane (or edits weights manually);
- **Then** the split updates per the ladder (visible immediately; lane widths reflect it); node
  serialization uses the split; replay is byte-identical `[E10]`; goldens with QoS edits
  re-bless per the 4.3 discipline.

- **Edge-case contracts:** `[E10]`, E8 allocation. **Golden:** T2 50/30/20 assignment + T2 manual
  override.
- **Launchable increment:** assign streaming→Express — Express widens to 50% and serialization
  follows.

**→ Slice 5 exit:** the Mini Motorways feel — growing map, telegraphed trouble, pause, three
inputs, placeable router tiers, demolish-and-redesign, a telemetry X-ray, legible QoS.

---

## Slice 5B — Traffic realism: the honest congestion model (access tier + bounded demand)

*The Section B design threads (user ruling 2026-08-15): congestion lives where it does in real
networks — at aggregation points, never at endpoints. Source: `surge-explainer.html` §B (the
1G/40G/100G → u/tick math) + `spec-traffic-model.md`. Design spec: `_bmad-output/implementation-
artifacts/spec-traffic-model.md`. Sequencing rationale (post-slice-5 systems cluster, before the
slice-6 era transition + the slice-7 playtest gate) lives in that spec §5 — each card is sized for
one fresh minion, dispatched in order 5.9 → 5.12 (the invariant first, the payoff last).*

### Story 5.9 — Per-terminal demand caps (endpoints never self-congest)

- **Slice:** 5B · **Epic(s):** E2.1, E3.1 · **Systems:** flow `[ODN-3]` (flow.odin §1b spawn pass;
  `Flow_State` home beside `lane_caps`), catalogs `[ODN-5]`.
- **Goal.** The demand director bounds each terminal's spawn RATE via a per-terminal **spawn
  accumulator in integer milli-packet units** (fixed-point — spawns are integer per tick
  `core/flow.odin:646` AND the state paths are integer-only ODN-10, `core/catalog.odin:675`
  `parse_integers = true` + `jint_strict`): cap is **throughput-relative and uniform** —
  `accrue_milli = cap_fraction_permille × throughput_units ÷ packet_bandwidth` (proposed
  `cap_fraction_permille = 500`: residential ≈ 0.083 pkts/tick = 2.5 u/s, 50% of its 5 u/s;
  content_host ≈ 1.33 long-run = 40 u/s, 50% of its 80). Endpoints never self-congest; spawn drops
  become aggregation drops. (Perkins r1 B1/B2 + r2 fix-audit: the explainer's 0.2 pkts/tick is
  unenforceable as a per-tick compare, exceeds the residential's own throughput, and a fractional
  balance value would fail-fast at load — corrected here.)

**Given/When/Then:**
- **Given** the flow.odin §1b spawn pass and a per-terminal milli-credit accumulator
  (`spawn_credit_milli[terminal_slot]` in **Flow_State beside `lane_caps`** — updated IN PLACE
  (accrue + consume), derived, never serialized (the `lane_caps` precedent, `core/flow.odin:85`);
  T1 surface = the resulting `(class, src, dst)` spawn stream; accrue 1000-free integer
  `cap_fraction_permille × throughput ÷ packet_bandwidth` milli/tick; spawn costs 1000; pickable
  while `credit_milli >= 1000`; type-relative `MAX_CREDIT_MILLI = 1000 × max(1, ceil(cap))`);
- **When** a spec's volume would assign more spawns to one terminal than its cap this tick;
- **Then** the capped terminal is **ineligible for source picks** (eligible set = credit-gated
  subset; the pick keeps ONE rng draw per pick `[ODN-10]`) and the volume lands on other terminals;
  no endpoint can ever self-congest (source demand ≤ the fraction × its own forwarding capacity, so
  the endpoint's lane never fills from its own spawns — no E9 shed at its own access, no 600% congestion
  flicker; residential's ceiling 1 means NO burst — the pre-5.10 latency guard, a burst-2 through
  the 5 u/s access would serialize the 2nd packet in 12 ticks = 600 ms > email's 500 ms
  `latency_tol_ms`); the (class, src, dst) spawn sequence is byte-identical for a fixed seed `[E10]`;
  **a credit-gated skip is NOT a demand event** (never reaches `sla_count_demand`) while a
  pool-dropped arrival IS — the `demand_seen == delivered + dropped + live` invariant (E24) holds
  under both paths (pinned at `sla_test.odin:88`, `sla_check_invariant`); the era-3 demand profile +
  5.1 growth pacing + surge multiplier are **re-validated together** so the MVP surge still lands
  (silent non-landing is a fail, not a feature).

- **Pinned acceptances — QUANTITATIVE (Perkins r1 W9/W10 + r2 W6/W7):** (W9) **post-cap
  surge-lands** — on a known seed, the surge window's streaming spawn count ≥ the re-tuned expected
  volume × 0.95 (tolerance) while per-terminal spawns ≤ cap × window + burst allowance and credit ≤
  MAX_CREDIT (never silently zeroed); (W10) **one-subscriber-at-cap zero-drop** — on a known seed,
  over a W-tick window: every terminal's spawns ≤ ceil(cap × W) + burst allowance, credit ≤
  MAX_CREDIT, a single residential sourcing at cap shows **zero drops at its own access lane** and
  no E9 shed at its endpoint, AND end-to-end transit ≤ its class latency tolerance (the W5 guard);
  (W7) **unit-test re-pin surface named** — `core/demand_test.odin` (per-tick volume + spawn-
  histogram pins, e.g. the `effective_volume` surge pin) + `core/flow_test.odin` (per-spec spawn
  counts) + `core/determinism_test.odin` (byte-identical replay under caps) are RE-PINNED to the
  capped volumes, with positive (cap honored) + negative (no unbounded burst) assertions — not just
  the golden re-bless. **Sink-side scope (W6):** the invariant is source-side; sink concentration
  stays bounded by the weighted-random dst distribution + E9 at the access lane (a sink-side admit
  accumulator is a documented balance-time option). **Director-only scope (N9):** the legacy §1a
  `flow_seed_demand` path is exempt (fixed src/dst fixture).
- **Edge-case contracts:** `[E10]` replay, `[E24]` SLA accounting under credit-gated skips (pin:
  `sla_test.odin:88`), E22 pool unchanged. **Golden:** T1 (spawn sequence shift — **deliberate,
  cause-documented re-bless** per the 4.3 discipline; byte-verify `.log.bin` differs only in the
  version field, splice the old catalog_hash, cause-document); existing goldens unshifted at the
  const level.
- **Launchable increment:** run the app on a small map — no residential is ever the drop site FROM
  ITS OWN SPAWNS (source-side, director-spawned demand); drops (if any) sit at the
  aggregation/uplink, not the endpoint's spawn.
- **Status:** implemented 2026-08-17 — PR open (the per-terminal spawn-credit accumulator
  `core/flow.odin` §1b — credit-gated eligible set, one rng draw per pick; `cap_fraction_permille`
  500 in balance.json; era-3 re-tune (email 4→1, streaming 2→1, growth interval 120→40) so the
  ×10 surge lands as an aggregation event; W7/W9/W10 pins + E24 credit-skip pin; deliberate
  golden re-bless with the fold-only byte-proof).

### Story 5.10 — Narrow as residential access (the access tier)

- **Slice:** 5B · **Epic(s):** E3.1 · **Systems:** catalogs `[ODN-5]` (pipe_tiers), topology (S1).
- **Goal.** Narrow's canon role is the **last-mile access drop**, sized so ONE subscriber's traffic
  never congests it: narrow `capacity_units` 5 → **~8–10** (proposed start; playtest-tunable) with
  the routing-cost ladder (20) untouched — cost is moot on a single-path access link, and the
  2026-08-13 capacity-cost ruling is unchanged between routers (flows still prefer fat pipes).
  **Decoupled from 5.9 (Perkins r1 B2):** 5.9's cap is sized against the NODE's throughput, so its
  zero-drop acceptance holds at the CURRENT narrow (5 u/s); this rebalance adds access-layer
  headroom on top.

**Given/When/Then:**
- **Given** a residential wired to its aggregation point by one narrow pipe, with bounded per-terminal
  demand (5.9);
- **When** the residential's own traffic flows (base or surge);
- **Then** the narrow access link carries it with **~2× headroom pre-5.10 and ~3–4× post-5.10**
  (cap ≈ 2.5 u/s vs narrow 5, then 8–10 u/s) — the access link never congests from the one
  subscriber; congestion appears only where flows **aggregate** onto shared standard/wide links; a
  congested narrow now genuinely signals an undersized access link (the honest 4.1 reading); replay
  is byte-identical `[E10]`; the tier change folds `cat.hash` → the slice's **deliberate re-bless**
  (proven discipline).

- **Edge-case contracts:** `[E10]` replay, capacity-cost ruling untouched, span rules unchanged
  (`span_exceeds_tier` at edit — no contract change; no E-tag exists for the span rule in arch §11.7). **Golden:** T1/T2 re-bless (cause-documented, the slice boundary's legitimate re-bless).
- **Launchable increment:** run the app — a single residential on a narrow never drops its own
  traffic; stress appears when many homes share a link.

### Story 5.11 — Diverse terminal types (schools, offices, homes)

- **Slice:** 5B · **Epic(s):** E3.1, E2.1 · **Systems:** catalogs `[ODN-5]` (node_types), director
  `[ODN-7]` (source_role selectors), growth (5.1 type pick).
- **Goal.** The terminal roster gains class analogues — residential / small-biz / campus — each with
  a **different, bounded demand profile** (volume, per-terminal cap =
  `cap_fraction_permille × throughput ÷ packet_bandwidth`, uniform; throughput); a campus emits far more than a home. Roster entries are catalog data
  (`node_types.json`), but a **new terminal role is a CODE change (Perkins r1 W7 — `Terminal_Role`
  is a closed enum `core/catalog.odin:22`): this card names the touch points** — the enum gains a
  variant + `role_from_name` (`core/catalog.odin:1011`) + the `collect_terminals` role selector
  (`core/flow.odin`) + the growth type-pick (`core/growth.odin`). Distinct shape/icon per type
  (never color alone `[E9.1]`).

**Given/When/Then:**
- **Given** the extended `node_types.json` roster (new `terminal_role`s + per-type cap/profile
  fields) and the demand specs whose source/sink selectors resolve against it;
- **When** the director spawns and growth (5.1) places terminals of the new types;
- **Then** each type emits its own bounded profile (campus >> home in volume and cap); the director's
  typed selectors resolve against the new types (era-gated); growth spawns the new types per its
  era gating, every spawn satisfying E31 validity + the 5.6 placement separation; the type is
  readable without color; replay is byte-identical `[E10]`; catalog fold → the slice's deliberate
  re-bless.

- **Edge-case contracts:** `[E10]` replay, `[E31]` spawn validity per type, `[E9.1]` never-color-
  alone. **Golden:** T1/T2 re-bless + a T2 frame with all three types visible.
- **Launchable increment:** run the app — homes trickle, campuses flood; the terminal roster reads
  as a spectrum.

### Story 5.12 — Aggregation groups (congestion lives at the shared uplink)

- **Slice:** 5B · **Epic(s):** E3.2, E4.2 · **Systems:** growth (5.1 group-bias draw), director
  `[ODN-7]` (group-scoped demand weight), crisis Surge (S4).
- **Goal.** The payoff: terminals cluster into groups (neighborhood analogues) whose flows share one
  player-built uplink — the honest choke. The demand director weights group-scoped demand; the ×10
  surge is an **aggregation event** at the group uplink. **Explicit conflict resolution:** the group
  bias is a **soft preference inside the E31 validity envelope** (bias draw first, E31 validity on
  the biased candidate, rejection-sampling unchanged); the uplink is never forced — the player wires
  it. E31 stays the hard contract.

**Given/When/Then:**
- **Given** a group-bias growth draw (spawn near an existing cluster member within a group radius;
  proposed 3–8 members, radius **~4–6 tiles** — Perkins r1 W5: the radius must exceed
  `GROWTH_MIN_SEP_TILES = 3` (`core/growth.odin:76`), the E31 packing floor — playtest-tunable) and
  a group-scoped demand weight;
- **When** aggregate demand from a cluster rises (base or the ×10 surge);
- **Then** the shared uplink — not any member terminal, not any access drop — is where congestion
  appears; every spawned terminal still satisfies E31 (connectable-within-span, min-separated,
  in-grid) and growth stays fully seed-derived (no log entries, derive-don't-record); the surge
  stresses the group uplink (the crisis engine's `preventive_redesign` — "add a parallel pipe or a
  higher tier on the spike's path" — now names the group uplink); replay is byte-identical `[E10]`;
  deliberate re-bless at the slice boundary.

- **Edge-case contracts:** `[E10]` replay, `[E31]` hard floor preserved (group bias never violates
  it), `[E9]`/`[E22]` unchanged. **Golden:** T1/T2 re-bless + a T2 frame of a clustered topology
  under surge (drops at the uplink).
- **Launchable increment:** run the app — a handful of homes share one uplink; the surge saturates
  the shared link, and the player's router/tier/bundle/QoS call on it decides who lives.

**→ Slice 5B exit:** the traffic model is honest — endpoints never self-congest (5.9), access is
real last-mile (5.10), terminals read as a spectrum (5.11), and congestion lives where it does in
real networks — at the shared uplink the player builds (5.12). The slice-6 era transition and the
slice-7 playtest gate exercise the honest aggregation model from the start. **(One deliberate,
cause-documented golden re-bless lands at this slice's boundary — the traffic-model change is
precisely the "legitimate re-bless" event the 4.3 discipline reserves for.)**

---

## Slice 6 — One era transition: Email → Streaming (modernization)

*The GDD MVP (E1–E9) includes E5 (lavish choice 3A: keep slice 6). A minimal single-
transition stub on the reserved `[LATER]` seam `[ODN-16, §6.6]`.*

### Story 6.1 — Era definition (Email→Streaming data)

- **Slice:** 6 · **Epic(s):** E5.1 · **Systems:** Era FSM (S6) `[ODN-16]`.
- **Goal.** Era data (Era 2→3: per-era packet types, demand signature, infrastructure) loaded
  from `eras.json`; the era FSM advances the active era.

**Given/When/When/Then:**
- **Given** the `eras.json` catalog + the era FSM;
- **When** an era advance fires;
- **Then** the new era's unlocks load (streaming becomes available, new demand signature);
  catalog data is integer-only + fail-fast validated `[ODN-5]`; no mid-crisis demand spawn
  `[E14]`.

- **Edge-case contracts:** `[E14]` no-mid-crisis spawn. **Golden:** T1 of the era-advanced
  state.
- **Launchable increment:** the internet evolves — new traffic appears.

### Story 6.2 — Advance trigger

- **Slice:** 6 · **Epic(s):** E5.2 · **Systems:** Era FSM (S6).
- **Goal.** Advance requires sustaining SLA ≥ 95% across active classes for the milestone
  window **and** modernizing all in-service legacy pipes **and** no active crisis.

**Given/When/Then:**
- **Given** the advance gate;
- **When** the player meets (or fails) the advance conditions;
- **Then** advance fires only when all three conditions hold; an active crisis **blocks**
  advance `[E15]`; unmodernized legacy pipes block advance.

- **Edge-case contracts:** `[E15]` advance-blocked-on-crisis. **Golden:** T1 of the advance.
- **Launchable increment:** meet the gate → the era advances.

### Story 6.3 — Upgrade lifecycle (legacy decay)

- **Slice:** 6 · **Epic(s):** E5.3 · **Systems:** Era FSM (S6), Topology (S1).
- **Goal.** Pipes become legacy in later eras; effective throughput decays; modernize (tier
  up) or demolish.

**Given/When/Then:**
- **Given** the legacy-decay model;
- **When** an era advances and leaves pipes legacy;
- **Then** legacy decay is **measurable** (effective throughput decays); modernizing (tier up)
  or demolishing restores full throughput; the metaphor-boundary rules hold (Eras 1–4 literal,
  Era 6 abstracted) `[GDD § M4]`.

- **Edge-case contracts:** legacy-decay measurable. **Golden:** T1 of decayed vs modernized
  throughput.
- **Launchable increment:** watch legacy pipes decay; modernize or suffocate.

**→ Slice 6 exit:** modernization congestion is felt — the internet evolves, you must keep up.

---

## Slice 7 — Juice + accessibility (the fun-test gate)

*Core accessibility, input parity, and the juice pass that sets the production look
(full-game doctrine, decision-log 2026-08-17). **The full game's core (E1–E9) is complete;
the fun-test gate runs in full.***

### Story 7.1 — Visual juice (light-canvas polish)

- **Slice:** 7 · **Epic(s):** E8.1, E8.2 · **Systems:** View polish `[ODN-1]`.
- **Goal.** The light-canvas canon (warm-cream map, glowing pipes, colored packet dots, node
  health colors, leak spray) at just-enough quality; UI chrome (gauges, forecast, alerts) with
  progressive disclosure + filter/focus + alerts-as-nav.

**Given/When/Then:**
- **Given** the view layer + the look-book palette;
- **When** the game renders;
- **Then** the View reads **only snapshots** (never perturbs the sim) `[ODN-1]`; crisis events
  drive matching juice; packet type/node state are never color-alone; the viewport scales so
  wider/taller screens reveal more map (camera-fit).

- **Edge-case contracts:** `[ODN-1]` view-reads-snapshot, never-color-alone. **Golden:** T2 of
  the juiced frame.
- **Launchable increment:** the game feels like saving the internet.

### Story 7.2 — Audio juice (1–2 stings)

- **Slice:** 7 · **Epic(s):** E8.3 · **Systems:** Audio (minimal) `[ODN-15]`.
- **Goal.** 1–2 Suno stings (crisis alert + arrival click) with variant selection from the
  **app-owned cosmetic rng** (determinism-neutral).

**Given/When/Then:**
- **Given** the raudio layer + the cosmetic rng;
- **When** a crisis fires (or a packet arrives);
- **Then** a sting plays; the SFX variant pick draws from the **app-owned cosmetic rng only**
  (never the sim rng) `[ODN-15]`; every audio alert is captioned on-screen.

- **Edge-case contracts:** `[ODN-15]` cosmetic rng. **Golden:** T1 (audio events don't perturb
  the sim hash).
- **Launchable increment:** the game sounds like saving the internet (just enough).
- **Status:** implemented 2026-08-17 — PR open (the app audio module `app/audio` — crisis
  sting + arrival click via raudio, variants from the app-owned cosmetic rng `[ODN-15]`,
  procedural placeholders behind the `assets/audio` drop-in contract, alert captions;
  the `audio` T1 determinism golden: consumer interleaved live vs the no-consumer replay
  gate, byte-identical).

### Story 7.3 — Accessibility core

- **Slice:** 7 · **Epic(s):** E9.1, E9.2, E9.3 · **Systems:** View a11y.
- **Goal.** Colorblind-safe (Deuteranopia/Protanopia/Tritanopia palettes; icon+shape for
  packets, icon+outline for node states), reduced-motion (disable flash/shake; crises stay
  readable), scaling + captions.

**Given/When/Then:**
- **Given** the accessibility settings;
- **When** a player enables a colorblind palette / reduced-motion / scaling;
- **Then** every state/machine is readable **without color**; reduced-motion disables flagged
  effects **and crises stay readable**; UI/gauge scaling works; all audio alerts are
  captioned; full input parity holds.

- **Edge-case contracts:** never-color-alone, reduced-motion-preserves-crisis-readability,
  captions. **Golden:** T2 under each a11y mode.
- **Launchable increment:** the game is playable by colorblind, motion-sensitive, and
  low-vision players.

**→ Slice 7 exit: the FUN-TEST GATE (the E1–E9 core is complete).** Run the playtest (both
audiences). **Pass → greenlight slice 8+ + content; fail → iterate via the data catalogs
`[ODN-5]`.** The gate greenlights content scaling on this codebase — it never triggers a
rebuild (decision-log 2026-08-17).

---

## Slice 8+ — The six GDD mechanics (post-fun-gate · coarse)

*The six mechanics the user ratified (decision-log 2026-08-10), each at its natural home,
bundle-consistent, no tenet contradiction. Full Given/When/Then cards land post-fun-gate
(the playtest may reorder them). All carry `[FULL]` scope except the post-mortem's specific-
counter layer (which is `[FULL]` over the MVP's plain retry).*

- **8.1 Congestion-heatmap persistence** — Player Assistance (persistent breach-marks) + UI
  filter/focus (toggleable demand-vs-capacity heatmap overlay). *Invariant:* a warning/
  teaching surface, never a hint system.
- **8.2 Bespoke per-era crisis thresholds** — M5 (a "demand director" authoring crisis
  timing for feel) + difficulty rhythm invariant. *Invariant:* every spike forecast, every
  flaw preventable (crises stay fair).
- **8.3 Error-404 specific-counter post-mortem** — Win/Loss (a loss screen that teaches the
  specific counter) + Player Assistance cross-ref. *Invariant:* reinforces P3 ("I should have
  seen this coming").
- **8.4 Emergent clutch from constraints** — Core loop (reward/cascade) + crisis juice
  (resolution swell). *Invariant:* a tuned sim property (leans on bundle/severance dynamics),
  not a scripted event.
- **8.5 Costly always-available fallback** — Win/Loss "no soft-locks": the escape is an
  emergency **load-shed**, cost = **drops** (shed traffic → SLA breach → uptime/score drain),
  NOT cable-wear. *Invariant:* "always available, never free" — it **guarantees** no-soft-lock.
- **8.6 Interconnected upgrades** — M4 (compound modernization ladder) + Player Progression.
  *Invariant:* makes P4 modernization a chain, not scenery.

---

## Slice N — Full-game content (E10) + the carried-forward E11 features · coarse

- **E10 (content + impl swaps):** remaining packet types (gaming/banking/voice/multicast/
  IoT/AI); eras 4–6 (real-time triage; cloud scale + CDN reservoirs; Era-6 overlay mechanics
  — VPN/SDN/AI as data + small procs, **no new core system** `[arch §13.2]`); economy (score
  core + Could-tier SLA contracts/currency; no-pay-to-win); V2 AI stress-test
  (`AiAuditorDirector` behind the existing seam `[ODN-7]`); replayability (daily/weekly seeded
  runs + leaderboards — the **portable-core re-sim validation** story `[ODN-6]`; pin the
  leaderboard contracts then: offline outbox `[E19]`, non-blocking toast + retryable/terminal
  on reject `[E20]`, modifiers in submission + reproduced in validation `[E25]`).
- **E11's features (production polish) — the rebuild epic is SUPERSEDED (user ruling
  2026-08-17; decision-log):** v2 *is* the full-game build, so "discard prototype + rebuild"
  is gone entirely (completing the earlier "partially absorbed" reading). What lands here,
  on this codebase: the leaderboard backend, deterministic-seed run validation `[ODN-6]`,
  the Blender-MCP asset pipeline, full custom art/audio + accessibility at production
  quality. **Test contract:** the proven fun holds as content scales on this codebase
  `[FORGE #7 — satisfied by design]`.

---

_Source of truth for locked design = the forge; for the game = the GDD + decision-log; for
technical structure = the Odin architecture; for code conduct = `project-context.md`; for the
**slice sequence + slice-level rationale** = `sprint-plan-v2.md`; for the **buildable story
cards** = this document. Human review of the slice structure ran via **lavish** (2026-08-11,
APPROVED: 1A shape, 2B headless-first 1.1, 3A keep era slice 6) before the PR opened._
