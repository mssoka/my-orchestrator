---
title: 'Packet Plumber — Sprint Plan v1'
project: 'packet-plumber'
date: '2026-08-10'
author: 'Moses (via packet-plumber-sprint-plan-v1 minion)'
version: 'v1'
status: '⛔ SUPERSEDED 2026-08-11 by sprint-plan-v2.md (vertical-slice, Odin-native, locked routing) — kept for provenance; do not build from this document'
workflow: 'gds-create-epics-and-stories'

# Source documents (this plan sequences them; it re-decides nothing)
gdd: '_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md'
epics: '_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/epics.md'
architecture: '_bmad-output/planning-artifacts/architecture/architecture-v1.md'
sprint_plan_inputs: '_bmad-output/planning-artifacts/sprint-plan-inputs.md'
stories: '_bmad-output/planning-artifacts/sprints/stories-v1.md'
project_context: 'project-context.md'

stepsCompleted: [1, 2, 3, 4]
---

# Packet Plumber — Sprint Plan v1

> ⚠️ **SUPERSEDED 2026-08-11** by **`sprint-plan-v2.md`** (in this directory).
> This v1 plan is **horizontal** — a dead S0 foundation sprint → subsystem layers
> (S1 routing → S2 topology → S3 QoS) → fun loop only at S4 — and is **doubly stale**:
> drafted in **Godot/GDScript** (`RefCounted`, `AC-FinLT`, `scripts/core/`) against the
> **GL5.2 Godot** architecture (`architecture-v1.md`), and on the **reversed** routing
> (BFS + round-robin/weighted-LB). v2 rebuilds the sequence as **vertical slices**
> (every story launchable + a golden) onto the **locked Odin + Raylib** stack
> (`odin-architecture-v1.md`) and the **locked routing** (per-hop forwarding + ECMP +
> bundles — lavish 2026-08-10). **Kept for provenance; do not build from this document.**
> See `sprint-plan-v2.md` §1 (v1→v2 at a glance) and §7 (decisions & rationale).

> **What this document is.** Step 7 of the Packet Plumber setup flow — the last
> doc gate before the prototype build. It takes the GDD's eleven epics and:
>
> 1. **carves the MVP slice** — the email→streaming fun-test prototype, sequenced
>    first so fun is tested as cheaply as possible;
> 2. **defines the demand-pairing data** the architecture left as a flagged
>    follow-up (`PressurePlan` structure, typed source→sink mapping, the
>    destination-selection rule, and player-visibility — **§3**);
> 3. **sequences buildable stories MVP-first** (sprints S0→S6) with every MVP
>    story mapped to an architecture system + a headless test contract.
>
> The full Given/When/Then story cards live in **`stories-v1.md`**; this plan
> sequences them. The forge/brief/GDD/architecture locks are **not** reopened —
> citation tags (`[FORGE #n]`, `[BRIEF]`, `[GDD §]`, `[ADR-n]`) trace every
> choice.

---

## 1. Executive summary

**The mission.** Get a *testable* fun prototype fastest. The MVP is a **juiced
graybox** (not polished) whose only job is to answer: *is drawing pipes, managing
packet types, and upgrading to survive a bandwidth surge fun for hours, not
minutes?* `[FORGE weak #1]` The full game (eras 4–6, all 9 packet types,
leaderboards, AI stress-test) is **post-fun-gate** work, sequenced after.

**The plan in one breath.** Build the **determinism spine + MVP data** first
(S0), then the routing verb (S1), topology+mouse (S2), packet types+QoS (S3),
**the surge-survival fun-test loop** (S4 — the loop closes here), one era
transition (S5), and just-enough juice + accessibility + input parity (S6 → MVP
done). Every MVP story maps to an architecture system (S1–S8) and a headless
test; the architecture's 25 edge-case contracts (§10.5) seed most acceptance
criteria. The full game (E10) is content + impl swaps on the same Core
(`[ADR-16]`); production (E11) is a fresh rebuild on this spine after the gate.

**Sequencing principle.** *Playability after every sprint* — each sprint delivers
a testable vertical slice, so the game is playable + testable from S1 and the
fun-test loop is reachable by S4 (the earliest possible fun signal).

### Sprint map

| Sprint | Goal | Epic(s) | Playable increment after | Fun-test? |
|---|---|---|---|---|
| **S0** | Determinism spine + MVP catalogs + demand data + tests | S0 (foundation) | headless sim ticks deterministically; replay-equality green | — |
| **S1** | Draw + flow (graybox routing) | E1 | draw a network, watch packets flow | — |
| **S2** | Growing map + health states + mouse | E3 (minimal) + E7(mouse) + pause | nodes grow, health telegraphs, mouse draw | — |
| **S3** | Two packet types + QoS (the differentiator) | E2 | route 2 classes, feel the trade-off | — |
| **S4** | Surge + win/lose (**the fun-test loop**) | E4 + E6 | **survive the streaming surge; win/lose/retry** | ✅ **earliest** |
| **S5** | One era transition (modernization) | E5 | experience the internet evolving | ✅ deeper |
| **S6** | Juice + accessibility + input parity (**MVP done**) | E8 + E9 + E7(touch/ctrl) | feels+sounds like saving the internet; all inputs | ✅ **MVP fun-test** |

---

## 2. The MVP slice (the fun-test gate)

The MVP is **carved explicitly** so the fun question is testable as cheaply as
possible. From the forge + GDD, the MVP slice is:

| Dimension | MVP scope | Full game (later) |
|---|---|---|
| **Era arc** | **One transition: Email → Streaming** (eras 1–3) | 6 eras |
| **Packet types** | **2: email + streaming** | 9 |
| **Map** | **4–6 nodes**, one map | ~20–30 nodes |
| **Core actions** | draw pipes, upgrade pipes, designate priority lanes, set junction policy | + valves, reservoirs, overlays |
| **QoS control** | single "priority emphasis" dial per pipe → weight preset | full per-lane WFQ weights + dedicated-pipe premium |
| **Crisis** | **Surge archetype** (forecast 10× spike), fair + recoverable | 5 archetypes + V2 AI auditor |
| **Win/lose** | uptime ≥ 90% through the ≈90 s surge = win | open-ended run, Network Health meter, leaderboards |
| **LB** | round-robin (basic junctions) | + bandwidth-aware weighted (smart junctions) |
| **Economy** | action/capacity budget, no currency | score + SLA contracts/currency |
| **Leaderboard** | `LocalOnlyLeaderboard` no-op stub | `HttpLeaderboard` + backend (v1.0 dep) |
| **Save** | snapshot fast-resume (action-log canonical from day one) | seed + action-log validation |
| **Art/audio** | graybox + just-enough juice (colored rects/emoji, Suno SFX stings) | full custom Blender art + full soundtrack |
| **Accessibility** | core set (colorblind, reduced-motion, scaling, captions) | + optional advisor hints |
| **Input** | mouse (S2) → + touch + controller (S6) | same three |

**The carve-out invariant (architecture §12):** everything in the MVP column is
achievable **without touching** the Full-game column, and the Full-game column is
**content + impl swaps on the same Core** — never a re-architecture. That is what
makes the prototype safe to build *and* discard (`[FORGE #7]`).

**What "passing the fun gate" means (the gate definition):** the MVP playtest —
would players (both engineers and non-engineers, `[GDD § Target Audience]`)
choose to play a second run? Run length and fail→retry rate are the leading
indicators. On pass → greenlight E10 content and trigger E11 (fresh production
rebuild). On fail → iterate (data-driven catalogs make retuning fast, `[ADR-5]`).

> **MVP ≠ public demo.** The MVP is the *private* fun-test (graybox+juice). A
> public **demo** (polished, Steam page / wishlists) is a separate, later
> artifact cut from the full game. `[epics.md Build staging]`

---

## 3. Demand-pairing data definition (the flagged deliverable)

> **Why this section exists.** The architecture models `Packet {src, dst, route}`
> and the `PressurePlan` mechanism (`CrisisDirector.plan_pressure → PressurePlan`,
> consumed by `PacketFlow.step`), but left the `PressurePlan` **data structure**
> and the **demand-pairing content** undefined — flagged in
> `sprint-plan-inputs.md` as the sprint-plan phase's job. The mechanism is sound;
> this section defines the **content/data** + the **destination-selection rule**
> + **player visibility**. It is tunable per-era content driven through the
> architecture's existing mechanism — **not** an architecture change.

> **Terminology — sink vs destination (they are different).** A **source / sink**
> is a terminal *role*: a **source** originates traffic, a **sink** terminates it
> (a terminal can be both — Residential originates email *and* terminates
> streaming). A **destination (`dst`)** is the *specific packet endpoint* the
> selection rule (§3.3) picks from the eligible sink set for one packet. The
> architecture's `Packet {src, dst, route}` uses `dst` (per-packet); the
> GDD/architecture call terminals "source and/or sink" (role) `[GDD § M3, Arch
> §6.1]`. §3 uses both terms consistently: a `DemandSpec` names the **sink set**
> (role) and the rule chooses the **destination** (`dst`).

### 3.1 `PressurePlan` structure (DECIDED)

**Decision: a `PressurePlan` carries a tick + a list of `DemandSpec`s + a list of
active `SetPiece`s — each `DemandSpec` is a *per-source-class demand entry* with a
typed source set, a typed sink set, a destination-selection rule, and a volume
curve.** (Hybrid of the two options in `sprint-plan-inputs.md` §1: it is per-source
demand volume **plus** an explicit selection rule, not hard-coded src→dst pairs —
keeping it tunable per-era and map-agnostic.)

```gdscript
# Core types — RefCounted, integer-tick math (ADR-10), seeded-RNG driven (ADR-9)

class_name PressurePlan extends RefCounted
var tick: int                         # the logic tick this plan is for
var entries: Array[DemandSpec]        # base per-era demand (always active)
var set_pieces: Array[SetPiece]       # forecast events (the Surge) active this tick

class_name DemandSpec extends RefCounted
var class_id: StringName              # packet type (email, streaming, ...)
var source_selector: TerminalSelector # WHICH terminals originate it (typed by role)
var sink_selector: TerminalSelector   # the eligible sink set (typed by role)
var selection_rule: SelectionRule     # how dst is chosen from the sink set (§3.3)
var volume_units_per_tick: int        # base demand volume (can be a curve over the era window)
var default_lane: int                 # Express/Standard/Best-effort start lane (DECIDED: Standard, game-wide — resolves GDD Open Q6, §8 decision 7)
var demand_weight: int                # relative weight for this spec vs siblings (tunable)

class_name TerminalSelector extends RefCounted
var node_role: StringName             # e.g. "residential", "content_host", "financial_hub"
var cardinality: int                  # -1 = all matching; n = pick n (seeded) — usually -1 (all)

class_name SelectionRule extends RefCounted
var mode: int                         # WEIGHTED_RANDOM (MVP) | NEAREST_HOPS | ROUND_ROBIN
var weight_by: StringName             # "node_demand_weight" (per-terminal weight) | "uniform"

class_name SetPiece extends RefCounted  # a forecast event (the Streaming Surge)
var id: StringName                    # e.g. "streaming_surge"
var class_id: StringName              # the class it amplifies
var multiplier: int                   # 10× for the Surge
var start_tick: int
var duration_ticks: int
var forecast_lead_ticks: int          # how far ahead the forecast warns (15–60 s, GDD M5)
```

**Why this shape (and not explicit src→dst pairs):**
- **Tunable per-era content** — an era's demand is catalog data (`eras.demand_signature`
  materializes into `DemandSpec`s), not code. New era = new data. `[ADR-5]`
- **Map-agnostic** — `source_selector`/`sink_selector` are typed by **node role**
  ("all Content-host terminals"), not hard node-ids, so the same demand works on
  any seeded map. The demand says *what kind* of traffic flows; the player's drawn
  topology decides *how* it routes.
- **Determinism-friendly** — every random choice (which terminals, which dst) is
  seeded via `rng` passed into `plan_pressure` (ADR-7/9/10). The whole spawn
  sequence reproduces from `(seed, era, tick)`.
- **Seam-compatible** — it flows through the `CrisisDirector.plan_pressure` seam
  the architecture already designed; the V2 `AiAuditorDirector` will produce
  `PressurePlan`s with the same shape (it just chooses *which* demand to
  amplify based on topology analysis). `[ADR-7]`

**Worked scenario — one tick of the Streaming Surge (MVP).** It's tick 600;
the surge SetPiece is active. `ScriptedDirector.plan_pressure(topology, era3,
600, rng)` returns roughly:

```gdscript
PressurePlan {
  tick: 600,
  entries: [
    # base era-3 demand (always on)
    DemandSpec{ class=email,     source=Residential,  sink=Residential,  volume=2, default_lane=STANDARD, selection=WEIGHTED_RANDOM },
    DemandSpec{ class=streaming, source=ContentHost,  sink=Residential,  volume=8, default_lane=STANDARD, selection=WEIGHTED_RANDOM },
  ],
  set_pieces: [ SetPiece{ id="streaming_surge", class=streaming, multiplier=10, start=600, forecast_lead=… } ],  # active this tick
}
```

For each `DemandSpec` this tick, `PacketFlow` spawns packets (every pick seeded →
deterministic):
- **email** (volume 2): pick a **source** terminal from all Residential
  (seeded); pick each packet's **`dst`** from all Residential (WEIGHTED_RANDOM,
  seeded) → e.g. `Residential#3 → Residential#7`. (A Residential terminal is
  **both** a source and a sink — person-to-person email.)
- **streaming** (volume 8, **×10 surge = 80 this tick**): pick the **source**
  from Content-host (the single YouTune host); pick each packet's **`dst`** from
  Residential (WEIGHTED_RANDOM, seeded) → **80 streaming packets fan out
  Content-host → many Residential sinks** — the flood the player must have wide
  capacity for.

So the player **sees** the demand-line Content-host→Residential pulse + the surge
forecast (§3.4); the player **decides** how to route (which pipes, what capacity,
which lanes) — the demand names *what kind* of traffic flows and *where it wants
 to go*; it never dictates the route. (Replay the same seed → byte-identical
spawn sequence `[AC-E10]`.)

### 3.2 Typed source→sink mapping per era (CONFIRMED + adjusted)

Confirmed/adjusted from the proposed baseline in `sprint-plan-inputs.md` §2,
grounded in the GDD M2 packet roster + M3 node types. **Only Email and Streaming
are MVP**; the rest are full-game content (defined now so the schema is proven
end-to-end).

| Packet type | Source terminal(s) | Sink terminal(s) | Flow shape | Era | MVP? | Rationale / adjustment |
|---|---|---|---|---|---|---|
| 📧 Email | Residential | Residential | many↔many (P2P) | 1 | ✅ | Confirmed — person-to-person; low volume. |
| 🌐 Web (rich media) | Content host | Residential | one→many | 2 | ❌ | **Adjusted** from "Residential→Residential": web pages are *served* from hosts to residential users. |
| 🔵 Streaming | Content host | Residential | one→many (HIGH) | 3 | ✅ | Confirmed — the MVP surge source. |
| 🟢 Gaming | Gaming server | Residential (+ server↔server mesh) | one→many, low-latency | 4 | ❌ | Confirmed. |
| 🟡 Banking / Secure | Financial hub | Financial hub (+ Residential) | hub↔hub, **never-drop** | 4 | ❌ | Confirmed. |
| 🟣 Voice / Video | Residential / Content host | Residential | peer-ish, low-latency | 4 | ❌ | **Added** (proposed baseline omitted it) — call traffic is bidirectional peer. |
| 🟠 Multicast / Broadcast | Content host | many Residential | one→many broadcast | 5 | ❌ | Confirmed. |
| 🔵 IoT / Telemetry | Residential (devices) | Data center | many→one | 5 | ❌ | Confirmed. |
| 🌸 AI / adaptive | Data center | Residential (self-shaping) | adaptive | 6 | ❌ | **Added** — Era-6 adaptive demand (reshapes to spare capacity, `[Arch §13.2]`). |

**The MVP demand catalog (what S0.4 ships):**
- `DemandSpec` — Email: `source=Residential, sink=Residential, volume=low,
  default_lane=Standard, selection=WEIGHTED_RANDOM`.
- `DemandSpec` — Streaming: `source=Content_host, sink=Residential, volume=high,
  default_lane=Standard, selection=WEIGHTED_RANDOM`.
- `SetPiece` — Streaming Surge: `class=streaming, multiplier=10×,
  forecast_lead=~15–60 s` (the Era-3 climax the player must survive).

### 3.3 Destination-selection rule (DECIDED + pinned)

**Decision: when a source spawns a packet, its `dst` is chosen by
**WEIGHTED_RANDOM** over the eligible sink set — a deterministic, seeded
weighted-random pick, weighted by each terminal's `demand_weight`, with
equal-weight ties broken by the seeded `rng`.**

**Why WEIGHTED_RANDOM (and not nearest / round-robin / load-balanced):**
- **Routing is the player's job, not demand's.** In this abstracted topology,
  "distance" is hop-count along the *player-drawn* pipes — a consequence of the
  player's design, not a property of demand. `NEAREST_HOPS` would make dst a
  function of the player's topology (collapsing demand to "the closest sink"),
  which hides the routing puzzle (P1) and fights determinism (the "nearest" sink
  changes as the player redraws). Demand should be **content-driven** (a streaming
  packet goes to *a residential user*); the player decides *how* it gets there.
- **Fair + legible** — the eligible sink set is typed and visible (the player sees
  "Content host → Residential" demand); individual packet destinations are
  non-trivial, but in aggregate (law of large numbers) the load distributes
  proportionally to sink weights — load-balanced **in expectation** without
  forcing it per-packet.
- **Tunable** — `demand_weight` per terminal (e.g., a bigger residential block
  attracts proportionally more traffic) is era content, not code.
- **Deterministic** — the seeded `rng` drives the pick + the tie-break, so the
  whole spawn sequence is reproducible (`[ADR-9/10, AC-E10]`).

**`ROUND_ROBIN` (cycle sinks in order) is the deterministic-but-boring variant** —
left in the `SelectionRule.mode` enum for content designers who want perfectly
even distribution for a specific era, but **WEIGHTED_RANDOM is the MVP default**
(richer, more realistic traffic).

**Pinned headless test (the decision's contract):**
```
Given a fixed seed and a PressurePlan with N DemandSpecs over ticks 0..T,
When the flow spawns packets,
Then the (class_id, src, dst) spawn sequence is byte-identical across runs,
And the dst distribution over many packets matches the sink demand_weights ± tolerance,
And equal-weight ties resolve via the seeded rng (never container order).  [AC-E10]
```

### 3.4 Player visibility (DECIDED)

**Decision: the player sees source→destination demand via (a) typed source/sink
icons on terminals, (b) faint colored demand-lines from a DemandSpec's source-
region to its sink-region, and (c) a forecast "weather report" panel that names
incoming SetPieces (the surge). Color is never the sole encoder.**

| Element | How it shows demand | Accessibility |
|---|---|---|
| **Terminal icons** | Each terminal shows an **icon + shape** for its role (🏠 Residential, 🎬 Content host, 🏦 Financial, 🖥️ Data center) — the player sees *who generates* and *who receives*. | Icon+shape (never color alone) `[UX-DR4]` |
| **Demand lines** | Each active `DemandSpec` renders a faint **colored demand-line** from its source terminals' region to its sink terminals' region, tinted by packet-type color, with a width/density hint at volume. | Dashed/pattern style + the type icon at endpoints; colorblind palettes apply `[UX-DR4]` |
| **Forecast panel** | A "weather report" lists active demand + **incoming SetPieces** (the surge) with a countdown + the affected demand highlighted — this is the P3 fairness contract (every crisis foreshadowed `[FORGE #3]`). | Captioned; readable without color `[UX-DR5]` |
| **Filter modes** | "Highlight one packet type's flow" isolates a class's demand-lines + flowing dots — essential with 9 types. `[UX-DR2]` | Doubles as a low-vision aid |

**Why this works for the routing puzzle (P1):** the player sees the *demand
shape* (where traffic wants to go) separately from their *drawn routes* (how
they've chosen to carry it) — the gap between the two is the puzzle. A streaming
demand-line fanning Content-host → Residential, plus a forecast surge marker,
tells the player "build wide capacity here, now" before the surge hits.

**Crisis legibility tie-in (P3):** the Surge SetPiece appears in the forecast
panel with a lead time, and the affected demand-line pulses — so when the surge
fires and saturates, the player can say "I should have seen this coming"
(`[FORGE #3]`). The `CrisisEngine`'s `root_cause` (§10.1.3) points at the
specific under-provisioned link, closing the predict→react loop.

---

## 4. The MVP-first sprint sequence

> Each sprint: a **goal**, the **stories** (full cards in `stories-v1.md`), the
> **playable increment** it delivers, and its **exit criteria** (the headless
> tests that must pass to close the sprint). Build order follows `epics.md`'s
> *MVP build order* + the architecture's §15.4 first-steps.

### S0 — Foundation: determinism spine + MVP data + demand data + tests

**Goal.** Build the things every MVP story depends on, once, first: the pure
Simulation Core, the seeded-RNG + integer-math discipline, the MVP data catalogs,
the `PressurePlan` demand data (§3), the `ScriptedDirector`, and the headless
test harness. This is what makes the rest independently completable and the MVP
safe to iterate + discard (`[ADR-16]`).

**Stories:** S0.1 Core scaffold · S0.2 RNG + integer math · S0.3 MVP catalogs ·
**S0.4 PressurePlan + demand data (§3)** · S0.5 ScriptedDirector · S0.6 test
harness + replay-equality + parse gate.

**Playable increment:** none yet (infra) — but a **headless sim that ticks
deterministically from a seed** exists, and the fun-risk iteration loop
("change a number, test the loop") is live.

**Exit criteria (headless tests green):**
- Parse gate: no `Node` in `scripts/core/`; `--import` + `--quit-after 600`
  exit 0. `[AC-FinLT]`
- No-global-RNG grep gate; replay-equality: re-step `(seed, [])` twice →
  byte-identical `SimSnapshot` `[AC-E10]`; save mid-grace round-trips `[AC-E12]`.
- Sim slow-mo never skips ticks `[AC-E21]`; batch edits are validate-all-then-
  apply `[AC-E23]`.
- `plan_pressure` determinism (same `(seed, era, tick)` → identical
  `PressurePlan`); dst-selection determinism (§3.3 pinned test).

### S1 — E1 Core Routing Engine (draw + flow, graybox)

**Goal.** The primary verb: draw pipes that snap, and a flow simulation that
routes traffic sources→sinks along the player's graph.

**Stories:** E1.1 node+pipe model · E1.2 draw (snap, cost) · E1.3 upgrade/
demolish · E1.4 flow (sources→sinks, pooled packets) · E1.5 redundancy +
round-robin LB.

**Playable increment:** *draw a network and watch packets flow* (graybox — the
verb is testable).

**Exit criteria:** snap inclusive at boundary `[AC-E4]`; self-loop rejected
`[AC-E3]`; flow reaches all connected sinks; demolish-in-transit reroute/drop
`[AC-E1]`; terminal-demolish forbidden `[AC-E2]`; round-robin evenness; ids
monotonic `[AC-E11]`.

### S2 — E3 Topology & Nodes (minimal) + E7 mouse + pause

**Goal.** The growing map + the warning surface + the first input modality.

**Stories:** E3.1 MVP node types · E3.2 deterministic map growth · E3.3 node
health states · E7.2 mouse input · E7.4 pause-anywhere.

**Playable increment:** *nodes appear over time, the map grows, health states
telegraph trouble, mouse drawing works, pause-and-plan works.*

**Exit criteria:** seed → identical map-growth timeline `[AR7]`; health
transitions fire on thresholds + 🔴 traceable to measured strain `[FR11]`; mouse
→ same Command shape as other modalities `[ADR-12]`; pause freezes stepping
deterministically.

### S3 — E2 Packet Types & QoS (the differentiator)

**Goal.** Packets have needs; the player sets priority. Email + streaming, all
starting on Standard.

**Stories:** E2.1 packet-class definition · E2.2 per-pipe lane allocation
(emphasis dial) · E2.3 junction priority + serialization + contention drop ·
E2.4 per-class SLA tracking.

**Playable increment:** *route two traffic classes and feel the trade-off* —
promote streaming, demote email, watch contention drop best-effort first.

**Exit criteria:** integer partition weight-only + no-vanish `[AC-E8]`; all-zero
fallback `[AC-E5]`; never-drop-lane floor `[AC-E6]`; no-starvation under
continuous Express `[AC-E7]`; drop ladder Best→Std→Express `[AC-E9]`;
pool-exhaustion drops lowest-priority first `[AC-E22]`; ms-latency +
zero-demand-neutral `[AC-E24]`.

### S4 — E4 Surge + E6 Win/Lose (THE fun-test loop closes)

**Goal.** Fair, predictable crises + the stakes. MVP ships the Surge. **This is
the earliest fun-test.**

**Stories:** E4.1 warning signs · E4.2 Surge SetPiece · E4.3 fair-failure
(root-cause) · E6.1 SLA uptime · E6.2/3 Network Health + win/lose/retry · E6.4
no-soft-lock.

**Playable increment:** ***predict a surge from the forecast and survive it;
win or lose and retry.*** The fun-test loop is now playable end-to-end (the
gate question can be asked, even before juice/era).

**Exit criteria:** warnings carry lead times + derive from measurable strain;
no crisis without a resolvable root cause + no crisis on a healthy topology
`[AC-E13]`; surge set-piece fires on schedule from the seed; win/lose fire on
the 90% threshold; drain = max(severity) + cap `[AC-E16]`; signal precedence
`[AC-E17]`; no-soft-lock property test passes.

### S5 — E5 Era Progression (one transition: modernization)

**Goal.** Modernization pressure — the internet evolves; old infrastructure
obsoletes.

**Stories:** E5.1 era definition (Email→Streaming) · E5.2 advance trigger ·
E5.3 upgrade lifecycle (legacy decay).

**Playable increment:** *experience the internet evolving and modernize* —
legacy pipes decay, the advance requires modernization, demand-pairing data
(§3) wires the new era's demand.

**Exit criteria:** advance requires SLA ≥ 95% + modernize all legacy + no active
crisis `[AC-E15]`; active crisis blocks advance; no mid-crisis spawn `[AC-E14]`;
legacy decay measurable; unmodernized pipes block advance.

### S6 — E8 Juice + E9 Accessibility + E7 input parity (MVP done)

**Goal.** *Just-enough juice* to prove the **concept** (not just the loop),
core accessibility, and input parity across touch + controller.

**Stories:** E8.1 visual juice · E8.2 UI chrome (progressive disclosure,
filters, alerts-as-nav) · E8.3 audio juice · E9.1 colorblind-safe · E9.2/3
reduced-motion + scaling + captions · E7.1/3 touch + controller parity.

**Playable increment:** ***the MVP is complete*** — a juiced graybox that feels
and sounds like saving the internet, accessible, playable on mouse/touch/
controller. **The fun-test can now be run in full.**

**Exit criteria:** View reads only the snapshot; crisis events drive matching
juice; packet type/node state never color-alone `[UX-DR4]`; reduced-motion
disables flagged effects + crises stay readable `[UX-DR5]`; SFX variant pick is
cosmetic-only `[ADR-9 exception]`; touch + controller produce the same Command
shapes as mouse + landscape enforced on mobile `[FR13]`.

**→ On S6 exit, the MVP is feature-complete for the fun-test. Run the playtest
(both audiences). Pass → greenlight E10 + trigger E11. Fail → iterate via the
data catalogs (`[ADR-5]`).**

---

## 5. Traceability — story → architecture system → headless test

Every MVP story maps to an architecture system and at least one headless test
contract. (Architecture system refs: S1 TopologyGraph, S2 PacketFlow, S3
QoSEngine, S4 CrisisEngine, S5 NetworkHealth, S6 EraStateMachine, S7 Economy,
S8 Leaderboard seam, + View/Input/Audio/CommandBus.)

| Story | Arch system | Key test contract(s) |
|---|---|---|
| S0.1 | S1–S8 skeleton, SimDriver | parse gate (no Node in core) `[AC-FinLT]` |
| S0.2 | RNG, ADR-10 | no-global-RNG gate; replay-equality `[AC-E10]` |
| S0.3 | catalogs (ADR-5) | catalog round-trip; no balance literal |
| **S0.4** | PressurePlan (ADR-7) | **dst-selection determinism (§3.3)** |
| S0.5 | CrisisDirector seam (ADR-7) | plan_pressure determinism |
| S0.6 | test harness, save (ADR-11) | replay-equality; parse gate |
| E1.1 | S1 TopologyGraph | id monotonic `[AC-E11]`; span-limit |
| E1.2 | CommandBus, ADR-12 | snap inclusive `[AC-E4]`; self-loop `[AC-E3]` |
| E1.3 | S1, S7 | demolish-in-transit `[AC-E1]`; terminal-forbidden `[AC-E2]` |
| E1.4 | S2 PacketFlow | flow reaches connected sinks; pooled data `[ADR-8]` |
| E1.5 | S1 (LB) | round-robin evenness |
| E3.1 | S1 | MVP node types only; junction forwards |
| E3.2 | S1 + director (ADR-7) | seed → identical growth |
| E3.3 | S1, S4 | health on thresholds; 🔴 traceable |
| E7.2 | Input, ADR-12 | input-agnostic Command shape |
| E7.4 | RunController | pause freezes stepping deterministically |
| E2.1 | S2 | MVP classes; default lane = Standard |
| E2.2 | S3 QoSEngine | partition `[AC-E8]`; fallback `[AC-E5]`; floor `[AC-E6]` |
| E2.3 | S3 | no-starvation `[AC-E7]`; drop ladder `[AC-E9]`; pool `[AC-E22]` |
| E2.4 | S2 | ms-latency; zero-demand-neutral `[AC-E24]` |
| E4.1 | S4 CrisisEngine | warnings from measurable strain; lead times |
| E4.2 | S4 + director | surge fires on schedule from seed |
| E4.3 | S4, §10.1.3 | root-cause; no healthy-topology crisis `[AC-E13]` |
| E6.1 | S2 | uptime aggregation; zero-demand-neutral |
| E6.2/3 | S5 NetworkHealth | win/lose thresholds; drain `[AC-E16]`; precedence `[AC-E17]` |
| E6.4 | S5 | no-soft-lock property test |
| E5.1 | S6 EraStateMachine | advance loads unlocks; no mid-crisis spawn `[AC-E14]` |
| E5.2 | S6 | advance gate; active-crisis block `[AC-E15]` |
| E5.3 | S6, S1 | legacy decay measurable |
| E8.1 | View, ADR-8 | View reads only snapshot; juice on events |
| E8.2 | UI | input-agnostic popovers/filters/alert-nav |
| E8.3 | Audio, ADR-15 | SFX variant cosmetic-only |
| E9.1 | View | never color-alone `[UX-DR4]` |
| E9.2/3 | View/Settings | reduced-motion; crises stay readable |
| E7.1/3 | Input, ADR-12 | same Commands as mouse; landscape enforced |

---

## 6. Headless-test strategy

**The rule (project-context mandate + `[ADR-1]`):** every design invariant is a
regression test at the lowest layer against the pure Simulation Core — no
renderer needed. The architecture's §10.5 edge-case contracts (`E1`–`E25`) + the
GDD-pinned invariants (fairness, no-soft-lock, snap precision) are the seeds;
each MVP story's acceptance criteria reference the contract(s) it must honor.

**Test layers:**
1. **Pure-logic unit tests** (the bulk) — instantiate a Core system, step it,
   assert. Fully headless; backends take path overrides (never touch real
   `user://`). `[NFR3]`
2. **Replay-equality** — re-step `(seed, action_log)` twice, assert
   byte-identical `SimSnapshot` (the determinism + leaderboard-validation
   contract). `[AC-E10, ADR-11]`
3. **Property/invariant tests** — no-soft-lock (a reachable dead-end fails),
   no-crisis-on-healthy-topology, no-starvation, fairness rules. `[§10.1.3]`
4. **Scene tests** (where a node must exist) — add dynamic nodes INTO the tree,
   drive frames from `_process` (never `await process_frame` in `_initialize`,
   `[FinLT]`).

**Determinism gates the leaderboard** — because a seeded run is deterministic, the
(v1.0) backend validates submissions by re-sim/structural-action-log checks with
no heavy anti-cheat (`[GDD § Online Services]`). The replay-equality test is what
keeps that contract honest.

**The MVP runs headless for the fun-test too** — a seeded, reproducible run proves
fun via a deterministic surge-survival scenario, not just "looks right in the
editor." `[briefing MVP testability]`

---

## 7. Full-game + production outline (post-fun-gate)

Sequenced **after** the MVP passes the fun gate. The full game (E10) is content +
impl swaps on the same Core; production (E11) is a fresh rebuild on this spine.

### E10 — Full-Game Scope (content + impl swaps)
- **E10.1** remaining packet types (gaming/banking/voice/multicast/IoT/AI — new
  catalog data). `[GDD § M2]`
- **E10.2** eras 4–6 (real-time triage; cloud scale + CDN reservoirs; Era-6
  overlay mechanics — VPN/SDN/AI as data + small mechanics, **no new core
  system** `[Arch §13.2]`).
- **E10.3** economy (score core + Could-tier SLA contracts/currency; no-pay-to-
  win).
- **E10.4** V2 AI stress-test (`AiAuditorDirector` — the seam is already designed
  `[ADR-7]`; only the impl is new).
- **E10.5** replayability (daily/weekly seeded runs + leaderboards; swap
  `LocalOnlyLeaderboard` → `HttpLeaderboard` + backend, a v1.0 dep `[ADR-6]`).
  Pin the full-game leaderboard contracts then: offline outbox on no-network
  `[AC-E19]`, non-blocking toast + retryable/terminal on backend reject
  `[AC-E20]`, and run/challenge modifiers carried in the submission + reproduced
  in validation `[AC-E25]`.

### E11 — Production Rebuild (fresh codebase, `[FORGE #7]`)
- **E11.1** carry forward design + tuning catalogs + lessons; discard prototype
  GDScript.
- **E11.2** rebuild on the production architecture in a **new repo** (decided,
  lavish review 2026-08-07) — fresh code on this spine.
- **E11.3** port + expand the proven slice to production quality; **test
  contract:** the production build reproduces the prototype's proven fun before
  content scaling.

---

## 8. Decisions & open questions (for review)

> These are this plan's **load-bearing design calls** — flagged for the lavish
> review so they can be confirmed/adjusted. Rejected alternatives are named so a
> reviewer (or a fresh minion) can take over cold.

### Decisions made by this plan (confirm/adjust)

1. **`PressurePlan` = tick + `DemandSpec[]` + `SetPiece[]`; each `DemandSpec` is
   per-source-class demand (typed source/sink selectors + selection rule +
   volume curve) — not hard-coded src→dst pairs.** Rejected: explicit pair list
   (not tunable, not map-agnostic). `[§3.1]`
2. **Destination-selection = WEIGHTED_RANDOM over the eligible sink set, weighted
   by terminal `demand_weight`, seeded, ties by `rng`.** Rejected: NEAREST_HOPS
   (hides the routing puzzle — distance is a player-topology consequence, not a
   demand property); ROUND_ROBIN is left as a designer-selectable mode but is
   not the default (too uniform). `[§3.3]`
3. **Player-visibility = terminal role icons + faint colored demand-lines +
   forecast panel (color never sole encoder).** `[§3.4]`
4. **Sprint S0 (foundation) is a first-class sprint** — the determinism spine,
   MVP catalogs, demand data, and test harness are built once, first, so every
   feature story is independently completable. (The skill's template has no
   "foundation epic"; this plan adds S0 because the architecture's §15.4 first-
   steps are cross-epic enabling work the MVP cannot skip.)
5. **Mouse-first input (S2), touch + controller parity in S6** — the fun-test
   runs on mouse; full input parity (still MVP per E7) is sequenced late so it
   doesn't block the earliest fun signal (S4).
6. **Full-game (E10) + production (E11) stories are coarse** — detailed when the
   campaign is greenlit; each maps to the same systems (no re-architecture).
7. **QoS default lane = Standard — same in MVP and full game** (resolves GDD
   Open Q6, which the GDD deferred to prototype). All traffic starts on
   **Standard**; the player engineers QoS by **promoting** what can't drop/lag
   (→Express) and **demoting** what can wait (→Best-effort). The *default lane*
   is shared (no MVP-only default) — but the **MVP is still the carved fun-test
   slice** (§2/§4): its QoS *control surface* is the simpler single "priority
   emphasis" dial (vs the full game's raw WFQ weights `[Arch §12/§13.3]`), and
   its content is the Email→Streaming subset. Only the default lane is the same
   in both — the MVP is NOT the full game. Best-effort-as-default (the internet's
   native default — sharper, promote-only discovery) was considered and **not
   chosen**; Standard's two-directional promote+demote is the decided default.
   Applied in §3.1/§3.2 + story E2.1.

### Open questions (deferred, not blocking the MVP)

1. **Exact surge tuning:** the 10× multiplier, 90 s window, and 90% win threshold
   are `[ASSUMPTION: prototype tuning]` ballparks — retune via the data catalogs
   during S4 playtesting.
2. **Demand-line rendering density:** faint demand-lines scale with volume; the
   exact visual (single line vs fan, opacity curve) is an S6 art call.
3. **`demand_weight` sourcing:** per-terminal weight defaults to uniform in the
   MVP; per-terminal sizing (bigger residential blocks = more weight) is era-
   content data to author during full-game content work.

---

## 9. Acceptance (briefing checklist)

- [x] Sprint plan at `_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md`
  (+ stories file per the skill's structure: `stories-v1.md`).
- [x] The 11 GDD epics broken into buildable stories, **MVP-first sequenced**
  (email→streaming prototype stories first; S0→S6, fun-test loop closes at S4).
- [x] Every MVP story maps to an architecture system + is headless-testable
  (§5 traceability; `[AC-E#]` contracts on every card).
- [x] The **demand-pairing data fully defined** — `PressurePlan` structure (§3.1)
  + typed source→sink mapping per era (§3.2) + destination-selection rule (§3.3)
  + player visibility (§3.4).
- [x] The MVP slice is clearly carved (§2 — the fun-test gate).
- [ ] After user approval: commit, push, open PR targeting main. **Never merge.**

---

_Source of truth for locked design = the forge; for the design narrative = the
brief + GDD; for code conduct = `project-context.md`; for the buildable
translation = the architecture; for the buildable **story cards** =
`stories-v1.md`; for the **sequence + demand data** = this document. Human review
of this document runs via **lavish** before the PR opens._
