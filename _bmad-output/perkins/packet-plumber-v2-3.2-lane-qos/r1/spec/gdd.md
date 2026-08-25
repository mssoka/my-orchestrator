---
title: 'Packet Plumber — Game Design Document'
game_type: puzzle
platforms: ['Steam (PC/Mac)', 'Mobile (Android/iOS)']
genre: 'Top-down 2D routing puzzle with crisis-management and light-progression layers'
created: 2026-08-05
updated: 2026-08-05
version: v1
status: approved (lavish review 2026-08-05) — v1
author: Moses
source_forge: '_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md'
source_brief: '_bmad-output/planning-artifacts/briefs/brief-Packet-Plumber-2026-08-05/brief.md'
---

# Packet Plumber — Game Design Document

**Game Type:** Puzzle (primary; hybrid with simulation/strategy management layers) · **Complexity:** Medium · **Target Platforms:** Steam PC/Mac (mouse + controller), Mobile (touch) — the **same game**, input-agnostic, **landscape-only** on every platform `[FORGE #6]` `[RULING — user, 2026-08-05]`.

> **Vision.** The internet is breaking. YOU are the only thing standing between civilization and "Error 404." Fix the pipes. Route the packets. Save the internet. `[FORGE #1]`

This document is the canonical design reference. It expands the forge's eight locked decisions and the sealed brief into buildable design; it does not re-decide anything either locked. Forge locks are cited `[FORGE #n]`; brief-locked items `[BRIEF]`. Provenance of every GDD-level elaboration lives in `decision-log.md`.

---

## Executive Summary

### Core Concept

Packet Plumber is a top-down routing puzzle where the player is a network engineer keeping the internet alive. The player **draws pipes** between nodes, **routes packets by type** through dedicated priority lanes, **predicts fair crises** from readable warning signs, and **upgrades infrastructure** as the internet itself evolves across historical eras. It pairs the routing-puzzle satisfaction of Mini Metro / Mini Motorways with the crisis-management personality of Two Point Hospital, wrapped in real-world stakes every player has felt.

The pitch sells the **experience** — the visceral panic of "the WiFi is down" and the hero role of fixing it — not the mechanics. Real networking concepts (bandwidth, QoS, redundancy, failure cascades) are the secret educational byproduct, never the sales line `[FORGE #1]`.

### Target Audience

- **Primary (broad, reachable):** anyone who has felt an outage — i.e., everyone with a phone. Drawn by the universal fantasy, not technical interest. Nintendo model: approachable surface, rewarding depth.
- **Secondary (load-bearing):** network engineers and the technically curious. The packet-type / QoS model is the authenticity check that keeps the game honest rather than a baby puzzle; they are the early word-of-mouth `[BRIEF]`.
- **Playtest mandate:** both audiences, explicitly — the accessibility/depth balance is the design's most delicate surface (forge weak point #3).

### Unique Selling Points (USPs)

1. **Packet types + QoS lanes.** Mini Motorways cars are identical; Packet Plumber packets have *personalities and needs*. Every route is a trade-off, not just a connection `[FORGE #4]`.
2. **Era progression + infrastructure lifecycle.** The internet *evolves*; old infrastructure obsoletes and must be modernized or it suffocates the player. Mini Motorways is timeless and static; Packet Plumber *grows* `[FORGE #4]`.
3. **The empty quadrant.** No game combines routing-puzzle satisfaction + crisis-management personality + real-world internet stakes everyone recognizes. Packet Plumber owns that intersection `[BRIEF]`.

---

## Goals and Context

### Project Goals

1. **Prove the fun** — the MVP prototype exists solely to answer: *is drawing pipes, managing packet types, and upgrading to survive a bandwidth surge fun for hours, not minutes?* (forge weak point #1, the top risk).
2. **Sell the experience** — a capsule/trailer that triggers "I want to fix THAT" before play (Tyroller appeal doctrine).
3. **Ship one polished game, cross-platform** — Steam + mobile, the same game, single launch, no early access `[FORGE #7]`.

### Background and Rationale

The concept was hardened through a structured forge session (8 locked decisions, 6 explicit rejections) before any build investment. The forge's commercial thesis: routing puzzles are proven fun (Mini Metro/Motorways) but lightly contested at this depth; the crisis + packet-personality + internet-fantasy layers are what Packet Plumber owns. See `decision-log.md` and the forge report for full provenance.

Sibling project FinLit (`/Users/moses/code/kids-finlit-game`) shares the engine pipeline and is the source of carried engine traps; Packet Plumber prototypes tighter and tests quicker.

---

## Core Gameplay

### Game Pillars

Four pillars — each game-defining, distinct, and specific enough to steer decisions. Pillars 1, 2, 4 are the brief's load-bearing commitments; Pillar 3 elevates the forge-locked crisis model (#3) to close the Draw+**React** loop's traceability (see `decision-log.md`).

| # | Pillar | What it steers |
|---|---|---|
| **P1** | **Routing-puzzle satisfaction** — the Mini Metro/Motorways pleasure of drawing a clean, efficient, self-healing network where every packet arrives on time. | Draw feel, snap precision, flow legibility, optimization depth. |
| **P2** | **Packet-type trade-offs** — not all packets are equal; allocating each pipe's bandwidth across priority lanes makes every route a meaningful choice. (Differentiator #1 `[FORGE #4]`.) | QoS model, priority lanes, per-link bandwidth allocation, the decision space at every pipe and junction. |
| **P3** | **Readable, fair crisis triage** — predict the next crisis from warning signs and react in time; "I should have seen this coming," never random `[FORGE #3]`. | Warning-sign system, crisis archetypes, failure fairness, time pressure. |
| **P4** | **Era-progression modernization** — the internet evolves, old infrastructure obsoletes, and the player must upgrade or suffocate. (Differentiator #2 `[FORGE #4]`.) | Era list, infrastructure lifecycle, upgrade economy, the metaphor boundary. |

A mechanic that serves no pillar is scope creep — surface it. Traceability chain: Vision → Pillars → Core Loop → Mechanics & Systems → Development Epics (each link audited in `epics.md`).

### Core Gameplay Loop

The loop has two interleaved modes — a **build/redesign** cadence between crises and a **triage** cadence during them.

```
        ┌─────────────────────────────────────────────────────────┐
        │  1. ASSESS  — read the live topology: node strain gauges, │
        │     pipe pressure, the demand forecast ("weather report"),│
        │     and which packet types are generating load.           │
        │  2. DRAW / UPGRADE — lay new pipes between nodes (snap to │
        │     nodes, no pixel precision), upgrade pipe tiers,       │
        │     designate priority lanes, set junction triage policy. │
        │  3. DESIGNATE PRIORITY — bind pipes/lanes to traffic      │
        │     classes; choose who gets capacity when it is scarce.  │
        │  4. PACKETS FLOW — the simulation routes traffic by the   │
        │     player's pipes + policy; dots stream, gauges react.   │
        │  5. PREDICT — warning signs climb (🟡 strained → 🔴 crit); │
        │     the forecast names the incoming surge/failure.        │
        │  6. REACT — reroute, open redundancy, reprioritize, patch │
        │     leaks/cool junctions — to relieve the strain before   │
        │     failure.                                             │
        │  7. SURVIVE & EARN — clear the surge, restore SLA uptime, │
        │     bank the era's reward, advance / modernize.           │
        └───────────────────────┬─────────────────────────────────┘
                              (loops; eras layer new packet types,
                               nodes, and infrastructure on top)
```

- **Between crises (redesign mode):** the player optimizes for efficiency and redundancy — the puzzle layer (P1). Failure state here is *slow drift* toward a future crisis.
- **During crises (triage mode):** the player prioritizes and reroutes under time pressure — the crisis layer (P3). Failure state here is *fast SLA collapse*.
- **The loop's reward:** visible relief (gauges recover, packets flow clean, the alert clears) + era progression (new content, modernization). The fantasy payoff — "I kept the internet alive" — is delivered every cycle. **Clutch compounds at the peak (*user-ratified addition, lavish review 2026-08-10*):** recovery is tuned to *cascade* during a crisis — one well-placed reroute, or one pipe added to a straining bundle (restoring pooled capacity after a graceful severance shrink), unblocks a whole chain of flows at once, so the player *feels* a satisfying clutch emerge from their own constraints (the Ball Pit fire-rate-accelerates-into-the-moment principle). The bundle model produces these moments naturally: a partial bundle loss is a graceful capacity shrink the player can clutch back — only full-bundle-loss truly drops a route (M5). *(Full-game `[FULL]` feel design; the prototype's severance-only reroute approximates the cascade.)*

**Player action → outcome → reward → motivation to repeat:** act (draw/reroute) → outcome (flow improves or crisis averted) → reward (uptime restored, alert cleared, era advances) → motivation (a bigger/different demand is forecast).

### Win/Loss Conditions

The full game is an **open-ended run** — one growing map (the internet), not discrete levels; eras advance *within* the run as you hit SLA milestones (M4). Defined to be **testable** (pinned as regression contracts per `project-context.md`):

| Scope | "Win" | Lose |
|---|---|---|
| **A run (full game)** | **No fixed end** — a run is a survival/score chase (Mini Motorways lineage). Score = survival time + highest era reached + uptime % + crises survived. Beat your best; daily/weekly seeded runs feed leaderboards. | The **Network Health** meter empties — the internet goes dark, **Error 404** — run ends (see below). |
| **Era advance (in-run gate)** | Sustain SLA uptime ≥ 95% across active classes for the era's milestone window AND modernize all in-service legacy pipes → the internet **evolves**: new packet types/nodes appear, the map grows, infrastructure ages, demand rises. The run continues at higher difficulty. | (No separate loss — failing to sustain blocks the advance; the run continues at the current era until you recover.) |
| **MVP prototype** | Survive the streaming-era surge: hold SLA uptime ≥ 90% through the surge window (≈ 90 s) `[ASSUMPTION: prototype tuning]`. | Uptime collapses below the threshold during the surge → fail → retry. |

**The Network Health meter (the loss mechanic).** A single health bar = aggregate internet health (overall SLA uptime across active traffic classes). It **drains** whenever any class's SLA is breached (a readable crisis is biting — you saw it coming, P3) and **recharges** when uptime is healthy. A breach starts a **grace countdown** (the Mini Motorways fail-timer, at internet scale): recover — reroute / upgrade / reprioritize — before it expires and the meter stabilizes; let it expire and the meter takes a hit; if the meter empties, **Error 404**, run over. Hard-SLA classes (banking never-drops) drain it *fast* (short grace) — a critical service failing is a big hit — but never instant, so it's always telegraphed. Fair (forge #3): the meter drains only on *visible* strain, with a recoverable grace window, no random death. A single run varies by survival depth — early failures ~15 min, skilled late-era runs 60+ min — and escalating era demand eventually outpaces infrastructure (the natural endless-run curve); total playtime is hours across many replayed runs.

**No soft-locks (anti-pattern, `project-context.md`):** there is always a way to reroute or upgrade out of a crisis — the meter is recoverable until it empties. A true dead-end is a design bug, not a difficulty feature.

**Costly always-available escape — the no-soft-lock guarantee (*user-ratified addition, lavish review 2026-08-10*).** No-soft-lock is *guaranteed*, not merely hoped-for: an **emergency load-shed** is always available — from any junction the player can force-shed low-priority traffic (and, pushed further, force-reroute) to keep the hard-SLA classes alive when no spare capacity or clean reroute exists. It always works — you can always *drop* traffic — and it always **costs**: the shed traffic **drops**, real oversubscription (tail-drop under congestion, what a NOC leans on in a crisis; traffic volume does not fatigue a cable, but queues fill and packets fall), so shedding Best-effort (then Standard) breaches those classes' SLAs and drains the uptime/score. The escape preserves tension by design — it *buys survival at the price of drops*, never a free win, so a crisis you shed your way out of leaves the score bruised. `[NOTE FOR DESIGNER: the shed threshold and score-cost curve are a playtest call; the invariant is "always available, never free."]` *(Full-game `[FULL]`; the MVP has no escape — its single surge is survivable by design.)*

**Error 404 post-mortem — failure teaches the specific counter (P3, *user-ratified addition, lavish review 2026-08-10*).** The loss screen is a lesson, not a wall: at **Error 404** the game names *what* breached and *where* — the junction that overloaded, the bundle that lost its last link, the class whose SLA collapsed first — and the **specific counter** that would have held: "the Banking class failed at junction X; a second bundled pipe there, or an alternate route via Y, would have kept it alive." Because every crisis traces to a preventable topology flaw (M5 fairness), there is always a concrete lesson to name. This is the player-assistance surface that makes failure *educational* (see Player Assistance) and turns "I should have seen this coming" into "next time I will" `[FORGE #1 — the educational byproduct, made active at the loss surface]`. *(Full-game `[FULL]`; the MVP shows a plain fail → retry.)`*

---

## Game Mechanics

### Primary Mechanics

#### M1 — Draw-between-nodes (P1, primary) `[FORGE #2]`

The player draws pipes between nodes; pipes **snap to nodes** (Mini Metro / Mini Motorways model — no pixel precision). Drawing is the core verb.

- **Pipe tiers** (capacity = bandwidth; `[ASSUMPTION: prototype tuning]`):

  | Tier | Capacity (units/s) | Clean span / max (tiles) | Era introduced | Notes |
  |---|---|---|---|---|
  | Narrow (copper) | 10 | ~3 / ~5 | Era 1 | Cheapest; baseline legacy; short-range |
  | Standard (coax/broadband) | 25 | ~6 / ~9 | Era 2 | Workhorse; mid-range |
  | Wide (fiber) | 50 | ~12 / ~18 | Era 3 | First high-capacity; long-haul |
  | Backbone (dark fiber) | 120 | ~25 / ~40 | Era 5 | Data-center scale; very long-haul |

- **Distance / span limits** (real-link fidelity, reinforces P4 — *user-driven addition, lavish review*): each tier has a **max span** — a hard cutoff beyond which a pipe cannot be drawn — mirroring real links (copper is short-range, fiber is long-haul). Inside the max sits a softer **clean span**: beyond it, throughput degrades and latency rises, telegraphed by the same wear-indicator surface M5 crises use (full-game depth layer; the MVP enforces the hard max at minimum). As the map grows and nodes spread apart, legacy narrow pipes literally cannot span the new distances — so the player must upgrade to a higher tier **or** route through an intermediate junction (junctions act as repeaters, resetting the span budget — see M3). Distance limits turn era modernization from flavor into a concrete topology constraint, and make the educational byproduct mechanical `[FORGE #1]`.

- **Upgrade lifecycle (P4 differentiator):** a pipe drawn in an early era becomes **legacy** in a later era — its effective throughput decays (maintenance burden rises) and it cannot serve high-bandwidth packet types. The player must **modernize** (pay upgrade cost → tier up) or demolish-and-redraw. Legacy pipes are never free to ignore; this is what makes era progression *pressure*, not just scenery `[FORGE #4]`.
- **Cost model:** drawing a pipe costs proportional to length × tier; upgrading costs the tier delta. Full economy (currency, contracts) is full-game scope (`Could`, `[BRIEF]`); the MVP uses a simple budget/action cap.
- **Redundancy & bundled pipes:** multiple pipes can connect the same node pair — and parallel pipes **bundle into one pooled-capacity link** whose capacity is the **sum** of the bundled pipes' capacities (*routing-model ruling, lavish 2026-08-10 — supersedes the prior round-robin / weighted-LB decision; see decision-log*). Bundling makes redundancy **active capacity** the moment it is built: a second pipe adds bandwidth now (used in spikes), not idle insurance held in reserve for a failure. There is **no load-balancing mode** — no round-robin, no capacity-weighted split — because the bundle is one fat link, so the question of "how traffic splits across parallel pipes" does not arise. See M3.

#### M2 — Packet types & QoS lanes (P2, the core differentiator) `[FORGE #4]`

Not all packets are equal. Each packet type is defined by four attributes:

| Attribute | Meaning | Player-facing |
|---|---|---|
| **Latency tolerance** | Max end-to-end delay before the class's SLA degrades | "Gaming needs the FAST pipe." |
| **Loss tolerance** | Max packet-drop rate before the class's SLA degrades | "Banking can't drop." |
| **Bandwidth demand** | Volume of flow the class generates | "Streaming is a flood." |
| **Priority weight** | Default **priority lane** (Express / Standard / Best-effort) the type rides | Set/overridden per-pipe by the player. |

**Packet roster** (color is **never** the sole encoding — see Accessibility; icon + shape reinforce `[ASSUMPTION: roster sizing]`):

| Type | Color | Latency | Loss | Bandwidth | Appears (era) | SLA failure effect |
|---|---|---|---|---|---|---|
| 📧 Email / Browsing | ⬜ White/grey | High (can wait) | High (can drop) | Low | 1 | Delayed delivery (low penalty) |
| 🌐 Web (rich media) | 🟫 Brown | Medium | Medium | Medium | 2 | Pages stall |
| 🔵 Streaming | 🔵 Blue | Medium (can buffer) | Medium | **High** | 3 (MVP) | Video stutters — mass user annoyance |
| 🟢 Gaming | 🟢 Green | **Low** (can't lag) | **Low** (can't drop) | Low, bursty | 4 | Lag spike — rage-quit wave |
| 🟡 Banking / Secure | 🟡 Gold | Medium | **None** (never drops) | Low | 4 | Transaction fail — critical |
| 🟣 Voice / Video call | 🟣 Purple | Low | Low | Medium | 4 | Call drops |
| 🟠 Multicast / Broadcast | 🟠 Orange | Medium | Medium | High (1→many) | 5 | Stream to many fails |
| 🔵 IoT / Telemetry | 🔵 Cyan | High | Medium | Tiny × huge volume | 5 | Aggregate sensor loss |
| 🌸 AI / adaptive traffic | 🌸 Pink | Adaptive | Medium | High, self-shaping | 6 | Shaping collapses |

**The QoS model — link-level priority lanes** (*real QoS, made readable* — reworked per lavish review). Real networking does QoS on the LINK, not by physically separating pipes per class: a single link's bandwidth is partitioned across class **queues** (CBQ / WFQ / DiffServ). Packet Plumber uses the same model — each PIPE carries a small number of **priority lanes**, and the player allocates the pipe's bandwidth across them. This keeps the topology clean (one pipe per link, Mini Motorways clarity) while putting the QoS decision exactly where the internet puts it.

**Three priority lanes** (DiffServ-style — group, don't proliferate; the 9 packet types collapse onto 3 lanes):

| Lane | DiffServ analog | Recommended types | Guarantee |
|---|---|---|---|
| **Express** | Expedited Forwarding | Banking, Gaming | Lowest latency + lowest/zero loss (highest priority) |
| **Standard** | Assured Forwarding | Streaming, Voice/Video, Web | Bandwidth-assured; may buffer |
| **Best-effort** | Default | Email, IoT, AI/adaptive | Fills spare capacity; drops first |

These are the *natural* lanes per type — not the starting state. At the start of play **all traffic sits on Standard** (the neutral middle); the player engineers QoS by *promoting* what matters to Express and *demoting* what can wait to Best-effort (see Discovery below). The player can also override a type's lane per-pipe. Lanes are bounded to 3 by design — readable, and faithful to how DiffServ actually groups traffic.

**The player's QoS levers:**

1. **Pipe capacity** — which tier to draw/upgrade (M1). A bigger pipe has more bandwidth to allocate across its lanes.
2. **Per-pipe lane allocation** — for each pipe, allocate its bandwidth across the 3 lanes (WFQ-style weights — e.g., 50% Express / 30% Standard / 20% Best-effort). This is the core QoS decision, on the link where real QoS lives. **Nothing auto-allocates:** all traffic starts on Standard and the player actively engineers QoS — promoting what can't drop/lag (Banking/Gaming → Express) and demoting what can wait (Email/IoT → Best-effort). The player owns every call. MVP exposes this as a single "priority emphasis" dial per pipe; full per-lane WFQ weights are a depth layer. (Best-effort-as-default is the harder, more realistic variant — Open Questions.)
3. **Node serialization is automatic** — there is no junction "LB mode" or manual triage policy to set (*routing-model ruling, lavish 2026-08-10*): parallel pipes bundle into one pooled link (M1/M3) and each junction forwards per-packet (M3). The serialization order you *see* at a node (Express → Standard → Best, gap-filling) is the automatic consequence of the per-pipe lane weights in lever #2 — the player engineers QoS on the links, and the nodes serialize the result.
4. **Dedicated pipe (premium reservation)** — for a hard guarantee, dedicate an entire pipe to one class. Costly; used sparingly. (The earlier "dedicated pipe per class" idea survives as this top-tier option, not the default.)

**Trade-off — the heart of P2.** Allocating bandwidth to a lane *steals* it from the others: a high-Express allocation on a busy pipe starves Best-effort, so Email/IoT drop first. When demand exceeds a pipe's capacity, contention drops by lane (Best-effort first); per-class loss/latency accumulates, and crossing the SLA threshold costs reputation/uptime. Every allocation is a choice about who suffers first. This is the mechanic that bridges the engineer/non-engineer audiences (forge weak point #3): the surface is "give the fast lane more room," the depth is real link-level QoS.

**Readability — see the decision AND the consequence.** Flow within a pipe shows as colored packet dots whose **proportion** reflects the lane allocation (a pipe 70% Standard shows mostly blue streaming dots); the topology stays clean even as QoS gets deep, and redundancy is a deliberate **bundled link** (parallel pipes merge into one pooled-capacity pipe with a visible *pop*, M1), obvious rather than buried in class-spaghetti. At each node, the player sees the **consequence** of prioritization as **serialization**: packets ingress/egress by lane priority — Express first, then Standard, then Best-effort. It is **work-conserving with gap-filling**: when no higher-priority packet is ready, the next lane fills the gap, so lower-priority traffic slips through *between* the higher-priority packets rather than being fully starved — a Best-effort packet visibly *waits* while Express/Standard flow, but moves in their gaps (consistent with the no-soft-lock fairness rule). The pipe shows the *allocation* (the decision); the node shows the *serialization* (the result). Together they make 'who gets bandwidth, who waits' legible at a glance.

**Discovery & onboarding (the experience).** QoS is never auto-applied and never front-loaded as a tutorial — it is *discovered through consequence*. Era 1-2 (email, low demand): everything on Standard works fine. Era 3 (the streaming surge): Standard saturates, the Banking/Gaming SLAs start failing, and the player discovers they must triage — promote what can't drop/lag, demote what can wait. That 'I should have prioritized the bank' moment is the QoS insight and the fair-crisis insight (P3) at once. Pipe scarcity (capacity is finite and costly) makes the engineering mandatory, not optional — wasting Standard on email while streaming starves is punished. This turns QoS from an optimization into the core verb, and is the secret educational byproduct made active `[FORGE #1]`.

#### M3 — Topology & nodes (P1, P4)

**Topology terminology** (used consistently throughout — *clarified per lavish review*):

- **Pipe** — the *link/edge*; carries bandwidth. Connects two nodes; has a tier (capacity, M1) and a span (distance, M1).
- **Node** — any vertex a pipe connects to. Two kinds:
  - **Terminal node** — a traffic source and/or sink; a *location* (a neighborhood, a brand's servers, a data center). Traffic originates or terminates here. Residential, Content host, Gaming server, Financial hub, Data center, and CDN cache are terminals.
  - **Junction (router)** — a routing node where pipes meet; it **forwards** traffic per-packet toward each packet's destination (M3) and doubles as a repeater (resets the pipe span budget, M1). The player does **not** configure a junction — there is no router-config UI; forwarding is internal (M3). A junction is not itself a source or sink.

So: **junctions are nodes** (the routing kind, i.e. the routers); **terminal nodes are the locations** (DCs, neighborhoods, brands); **pipes are the links** between them.

The map **grows over time** (Mini Motorways model): new nodes (brands, neighborhoods, data centers) appear, demanding connection.

| Kind | Node type | Role | Throughput | Appears (era) |
|---|---|---|---|---|
| Terminal | Residential | Email/browsing source/sink | 5 u/s | 1 |
| Terminal | Content host | Streaming source (YouTune, Glitch) | 40 u/s | 3 (MVP) |
| Terminal | Gaming server | Low-latency source | 15 u/s | 4 |
| Terminal | Financial hub | Banking source (never-drop) | 8 u/s | 4 |
| Terminal | Data center | High-capacity hub location | 150 u/s | 5 |
| Terminal | CDN cache | Reservoir/buffer location — stores packets, smooths surges | buffers up to 60 u/s | 5 |
| Junction (router) | Router / junction | Forwards traffic per-packet; repeater (resets pipe span budget); finite ports (tier-scaled — see below) | scales with tier | 1 |

- **Parallel pipes bundle; junctions forward** (*routing-model ruling, lavish 2026-08-10 — supersedes the prior round-robin / weighted-LB decision; see decision-log*): when parallel pipes connect a node pair they **bundle into one pooled-capacity link** whose capacity is the **sum** of the members — there is **no load-balancing mode** (round-robin and bandwidth-weighted LB are deleted; the merged prototype, PR #17, still implements them as the `[PROTO]` step). Bundling makes redundancy **active capacity**: a second pipe adds bandwidth the moment it is built, used in spikes rather than held idle as failover insurance. Each junction then **forwards per-packet** toward the destination — an internal decision (players draw pipes; there is **no router-config UI**), choosing among equal-cost next hops via a **deterministic ECMP hash** `splitmix64(src, dst, class, pkt_id) mod N` so the same packet always takes the same path. Forwarding is not player-facing and not a junction "smartness" tier — all junctions forward. *(Juice: a pipe joining a bundle triggers a **"pop bigger" merge animation** + a Suno SFX thunk, re-fired each time a pipe joins — routing ruling.)*

- **Junction port limits** (*prototype-proven addition — experiment #12, canonized by user ruling 2026-08-08*): a junction has a **finite port count** that scales with its tier — **basic = 4 ports, mid = 8, high = 16** — matching the capacity-scaled router visual (more ports = bigger router). **One port per connected pipe:** every pipe drawn to a junction occupies one port on that junction (a pipe between two junctions occupies one port on each; parallel pipes between the same node pair each occupy their own port), and a full junction accepts no more pipes — the player must free a port (demolish a pipe) or route through another junction. **Ports are generic** — no uplink-vs-user port-type distinction; the bandwidth distinction lives in pipe tiers (M1), so ports stay simple. Terminal nodes are *not* port-limited (a location accepts whatever connects to it) — the limit is a junction property, and upgrading a junction raises its port count (basic → mid → high tier; M4). **Design intent:** a clean, intuitive topology constraint — "this router has 4 ports, choose wisely" — that forces meaningful routing decisions *without* frustration; the prototype experiment proved it fun (topology decisions, not busywork).

**Node health states** (the primary warning surface, M5): 🟢 healthy → 🟡 strained (approaching capacity) → 🔴 critical (imminent failure). A node reaching 🔴 is the player's alarm.

#### M4 — Era progression & infrastructure lifecycle (P4) `[FORGE #4]`

The internet evolves across six eras **within a single open-ended run** — there is one internet (one growing map), not six levels. Each era: (a) introduces new packet types/nodes, (b) raises aggregate demand, (c) flags prior-era infrastructure as legacy. **Era-advance trigger (in-run gate):** sustain SLA uptime ≥ 95% for the era's milestone window AND modernize all in-service legacy pipes → the internet evolves to the next era *and the run continues* at higher difficulty (it does not end a level). The MVP exercises exactly one advance (Email → Streaming).

| Era | Name | Packet types active | Signature demand | Metaphor fidelity |
|---|---|---|---|---|
| 1 | **Foundations (ARPANET)** | Email | Low volume, few nodes; the tutorial era | Literal (L1–3) |
| 2 | **Email & Web (dial-up → broadband)** | Email, Web | Calm optimization; the "build cleanly" era | Literal (L1–4) |
| 3 | **The Streaming Surge** *(MVP ends here)* | + Streaming | Bandwidth explosion 10×; QoS becomes essential | Literal (L1–4) |
| 4 | **Real-Time (always-on)** | + Gaming, Banking, Voice/Video | Multi-priority triage; never-drop + low-latency | Literal (L1–4) |
| 5 | **The Cloud Era** | + Multicast, IoT | Data centers, CDN reservoirs, massive scale | Literal + reservoir abstraction |
| 6 | **Software-Defined Edge** | + AI/adaptive | Overlays: secure tunnels, programmable reroute, self-shaping demand | **Abstracted** (see below) |

**The modernization ladder compounds (P4, *user-ratified addition, lavish review 2026-08-10*).** Upgrades are tuned so each unlock *desires* the next rather than sitting as an isolated purchase: a wider pipe (M1) exposes a junction's port ceiling, pushing a junction upgrade to a higher-port tier (more bundled links in and out); the fatter pooled bundle then makes per-pipe QoS lane tuning (M2) pay off, which in turn makes a redundant bundled link worthwhile — redundancy is **active capacity** the moment it is built (it rides demand spikes, never idle failover insurance). The chain runs **pipe → junction → QoS → redundancy**, and legacy decay (M1) keeps every rung moving. Modernization is a satisfying chain, not a checklist `[ASSUMPTION: full-game tuning — exact upgrade costs and couplings are prototype-time]`. *(Full-game `[FULL]`; the MVP exercises a single pipe-tier upgrade.)*

**Metaphor boundary (addresses forge weak point #2).** The plumbing metaphor (pipes / pressure / leaks / valves) maps cleanly to OSI layers 1–4 (physical → transport). Eras 1–4 stay strictly in that band — honest, not forced, because pipes/flow/pressure *is* how bandwidth works conceptually. Era 5 adds CDN-as-reservoir (still pipe-honest). **Era 6 deliberately abstracts** the layer where literal plumbing strains (VPN/VLAN/SDN/VXLAN, AI traffic shaping): a VPN is a *secure tunnel overlay* the player draws over the map; SDN is *programmable rerouting* (re-prioritize without redrawing); AI traffic is *adaptive demand* that shapes itself to spare capacity. These are represented as **gameplay mechanics**, not literal layer-fidelity — the era list stops literal plumbing before the metaphor breaks, and modern tech is *represented* (still fun, still honest about the concept) rather than faked. The full-game scope decision (where the campaign literally ends vs. sequel territory) is an Open Question.

**Post-launch expansion candidate — interplanetary / space networking (DTN).** Beyond Era 6, the metaphor extends cleanly to *interplanetary* communications via Delay-Tolerant Networking. The regime change creates genuinely NEW mechanics rather than stretching the Earth metaphor: **light-minute propagation** = packets with long, visible travel times (plan-ahead routing); **intermittent connectivity** = links open only in alignment / line-of-sight windows (schedule the traffic); **store-and-forward bundling** = packets cached at relay nodes until a window opens (the CDN-reservoir idea promoted to core transport); **high error rates** = redundancy + retransmission matter more. Grounded in real space-networking standards (CCSDS Blue Books, ECSS SpaceWire, IETF DTN bundle protocol). Flagged as a post-launch expansion — only if the game is successful.

#### M5 — Crisis model: fair and predictable (P3) `[FORGE #3]`

Crises are the **consequence** of a topology flaw the player should have designed around — never random. Every crisis is foreshadowed by readable warning signs with a lead time, and every crisis has a topology-flaw root cause the player could have prevented.

**Warning-sign system (the fairness contract):**

| Indicator | Meaning | Lead time to failure |
|---|---|---|
| Node 🟡 strained | Approaching capacity | ~30 s `[ASSUMPTION: prototype tuning]` |
| Node 🔴 critical | Imminent overload/fire | ~10 s |
| Pipe pressure climbing | Saturation incoming | ~20 s |
| Demand forecast ("weather report") | A surge/failure is N seconds out | 15–60 s |
| Legacy pipe wear indicator | Degradation incoming | long (era-scale) |

**Five crisis archetypes** (each a design consequence, each preventable):

| Archetype | Root cause (preventable) | Warning | Failure |
|---|---|---|---|
| **Saturation** | Built too little capacity / no bundled redundancy for demand | Pressure climbing, nodes 🟡 | Mass packet drops; SLA collapse |
| **Single-point-of-failure** | One junction carries critical load with no alternate route around it | Junction 🔴 | Junction overload/fire → all routes through it fail |
| **Degradation** | Left legacy pipes in service under new-era load | Wear indicator, falling throughput | Pipe burst / throughput collapse |
| **Surge** *(MVP)* | No spare capacity / redundancy for a forecast demand spike | Demand forecast (viral event, 10× spike) | Cascade saturation across the map |
| **Severance** | A whole link-bundle lost (no alternate route) | Link marked vulnerable / timed event | Cut one pipe of a bundle → pool capacity shrinks (graceful); only **full-bundle-loss** drops the route |

**Fairness rules (pinned as test contracts):**

1. Every crisis has a warning sign with lead time ≥ the player's reaction window.
2. Every crisis has at least one topology redesign that would have prevented it.
3. No crisis is RNG-spawned onto a healthy topology — a crisis always traces to a measurable strain that was visible.
4. The player can always recover (no soft-locks) — reroute, upgrade, or reprioritize out.

The V2 **AI stress-test system** (deferred — full-game replayability, forge weak point #4) is an *auditor* that analyzes the player's topology, finds the exploitable weakness, and pressures *that* — fairly, because it attacks a real flaw, never a random one.

**Demand director — bespoke per-era crisis rhythm (P3, *user-ratified addition, lavish review 2026-08-10*).** Crisis pacing is **hand-tuned per era**, not a flat difficulty curve: a demand director scripts each era's surges to an authored rhythm — a tension peak climbing through staged thresholds (the Hades 2 wave-gate principle: 50 / 70 / 90%), broken by an *earned* breath where gauges recover and the player banks the era's reward. The rhythm kills dead time (a lull is always about to break) and makes the breath *relieving* rather than empty. Each era's signature demand (M4) gets its own cadence — the streaming surge is a single 10× wall, the real-time era is rapid multi-class triage, the cloud era is long sustained pressure. This is the *pacing* layer of the crisis model: crises stay *fair* (every spike forecast, every flaw preventable, per the fairness rules) while their *timing* is authored for feel. `[ASSUMPTION: prototype tuning — per-era threshold curves and breath windows are authored at balance time.]` *(Full-game `[FULL]`; the MVP ships one fixed surge set-piece.)*

### Controls and Input

**Cross-platform same-game doctrine `[FORGE #6]`:** draw-between-nodes is input-agnostic — one game, three inputs, identical play.

| Action | Touch (mobile) | Mouse (PC) | Controller |
|---|---|---|---|
| Draw pipe | Drag node→node | Drag node→node | Select node (A) → aim stick → confirm (A) |
| Upgrade pipe | Tap pipe → tier | Click pipe → tier | Highlight → (Y) cycle tier |
| Designate priority lane | Tap pipe → class | Click pipe → class | Highlight → bumper cycle class |
| Set junction policy | Tap junction → order | Click → order | Highlight → d-pad reorder |
| Pan map | Two-finger drag | Edge-scroll / drag | Stick |
| Pause | Pause button | Space / Esc | Start |

- **Draw snap radius:** generous (no pixel precision) — the intent is honored, not the exact path `[FORGE #2]`.
- **Pause anytime** — the player can pause to assess/redesign without time pressure; crises tick down only while unpaused. This is core to accessibility and to the "fair" crisis model (the player always has time to *think*).

---

## Puzzle-Specific Design

*Game-type: puzzle (medium complexity). The puzzle genre guide's required subsections — solution space, player assistance, difficulty ramp, tutorialization — are documented here. The game's simulation/strategy layers (long-tail balance, end-state, pacing) are folded into Progression & Balance and Level Design.*

### Core Puzzle Mechanics

- **Primary puzzle mechanic:** route packets from sources to sinks by drawing a pipe graph, under the constraint that each packet class has needs (M2) and capacity is finite (M1).
- **Supporting mechanics:** per-pipe lane allocation, junction triage policy, upgrade/modernization, redundancy.
- **Mechanic interactions:** capacity × demand × priority = the live optimization surface. Every redesign changes the flow.
- **Constraint systems:** per-pipe capacity, per-node throughput, per-class SLA thresholds, era time limits, upgrade budget.

### Solution Space

The puzzle is **constructive and open** (like Mini Motorways), not single-solution: many valid topologies clear an era; the player optimizes for uptime, efficiency, and crisis-resilience rather than finding *the* answer. The solution space is guaranteed solvable by construction — the era is beatable with the infrastructure it unlocks, provided the player modernizes; an unbeatable state is a design bug (no soft-locks). Difficulty scales demand, not solution existence.

### Player Assistance

- **No hint system in the core loop** — the warning signs (M5) *are* the guidance; a separate hint layer would undercut the "I should have seen this coming" pillar (P3). `[NOTE FOR DESIGNER: an optional, toggle-off "advisor" hint layer for the most casual players is a Could-tier accessibility option to playtest.]`
- **Undo / redesign:** pipes are freely redrawn/re-tiered within budget; no punishment for tearing up a bad route (redesign is the game).
- **Pause-and-plan:** pause anytime to read the topology and redesign without pressure.
- **Tutorial integration:** Era 1 (Foundations) is the tutorial — one packet type (email), low stakes, teaches draw + flow; Era 2 introduces priority; Era 3 (the MVP) introduces the surge and QoS under pressure. See Tutorialization.
- **Strain-trace persistence — failure teaches the map (P3, *user-ratified addition, lavish review 2026-08-10*).** The topology *remembers*: pipes and junctions that dropped packets or breached SLA keep a subtle persistent mark across the run (**on by default** — the always-visible layer), and a toggleable **demand-vs-capacity heatmap overlay** (a focus mode, off by default) shows where load has repeatedly outstripped supply (the Lonely Mountain Snow Riders death-leaves-tracks principle). Repeated runs build a mental model of the map's strain points, so failure is *educational*, not punishing. This is a **warning-surface extension**, never a hint layer: it shows *where* strain has lived, never *what to do about it* — the call stays the player's, preserving P3's "I should have seen this coming." See UI & Navigation for the heatmap focus mode. *(Full-game `[FULL]`; the MVP shows live strain only.)*
- **Error 404 post-mortem** (cross-ref Win/Loss) — the named-counter lesson at the loss screen is the run-end instance of this educational surface.

### Difficulty Ramp

| Stage | What's introduced | Player skill tested |
|---|---|---|
| Tutorial (Era 1) | Draw, flow, one class | Basic routing |
| Early (Era 2) | Multiple classes, priority policy | Triage basics |
| Mid (Era 3, MVP end) | Streaming surge, capacity planning, redundancy — **QoS discovered** (Standard saturates → player learns to promote/demote lanes) | Crisis prediction (P3) + the QoS insight |
| Core (Era 4) | Never-drop + low-latency classes simultaneously | Multi-priority triage under pressure |
| Late (Era 5) | Scale, CDN reservoirs, multicast | Long-tail balance, big-topology readability |
| Endgame (Era 6) | Abstracted overlays, adaptive demand | System-level redesign, modernization discipline |

Demand (packet spawn rate, node count, surge magnitude) scales within and across eras; complexity (new packet types, new crisis archetypes) scales at era boundaries. `[ASSUMPTION: prototype tuning — per-era curves are ballpark; see Numerical Design.]`

### Level Structure

- **Unit of play:** a **run** — one open-ended, growing map (the internet) you keep alive until the Network Health meter empties (Error 404). Eras are NOT levels; they advance *within* a run as you hit SLA milestones. A single run varies by survival depth — early failures ~15 min, skilled late-era runs 60+ min (6 eras × ~8–12 min milestone). **Total playtime is hours** across many replayed runs (daily/weekly, score-chasing, leaderboards); the MVP is a bounded ~3–5 min surge slice `[ASSUMPTION: prototype tuning]`.
- **Structure:** one internet; the six eras are the in-run escalation arc, unlocked as you sustain uptime + modernize (M4).
- **Unlock progression:** era advances unlock new packet types, node types, pipe tiers, and tools (priority lanes, valves, reservoirs).
- **Replayability is core, not bonus:** each run differs by seed; daily/weekly seeded runs + leaderboards + score-chasing + challenge modes give hours of playtime (see Replayability).

### Tutorialization

Just-in-time, diegetic through the alert system: the first time a mechanic is relevant, an in-world alert teaches it ("⚠️ YOU_TUNE traffic is climbing — draw a wider pipe."). No separate tutorial mode; Era 1 is the gentle on-ramp. Satirical brand alerts carry the teaching, reinforcing the experience (Tyroller) and the humor (Two Point Hospital lineage).

### Replayability

- **Score-chasing (the meta):** survival time + highest era reached + uptime % + crises survived — beat your best across runs; this IS the progression (no linear campaign end).
- **Daily Challenge (global leaderboard):** every day the whole world gets the SAME seed (map + demand script) and competes on one global board — one shot per day (the fair-comparison core, à la Mini Motorways).
- **Weekly Challenge (global leaderboard):** same seed all week, unlimited attempts, top-spot chase.
- **Modifiers:** daily/weekly challenges add rule twists (double pipe budget, no-upgrades, surge-every-30s) to keep the rotation fresh (Mini Motorways-style).
- **All-time / free-play board:** best score on standard (non-challenge) runs — less fair (map variance), mitigated with milestone seeds.
- **Friend leaderboard:** Steam friends + mobile — the social motivation layer.
- **Score-distribution histogram:** show where your score sits globally (Mini Metro-style).
- **Era-reached board (our unique dimension):** "how far did the internet evolve" — a leaderboard category Mini Motorways can't offer, plus per-era boards and "most crises survived."
- **Challenge modes (solo):** no-upgrade, zero-drop, speed-clear variants.
- **The V2 AI stress-test** (full-game): generates fresh, fair pressure from your topology — high replayability, scoped carefully (forge weak point #4).

---

## Progression and Balance

### Player Progression

- **Intra-run:** the player's "progression" is a *better topology* + era advancement — more capacity, smarter priority, more redundancy, pushing the internet further along the era arc. Upgrades **compound** along the modernization ladder (M4: pipe → junction → QoS → redundancy), so skill growth is *feeling which rung to climb next*. The skill the player grows is *network engineering intuition* (the secret educational byproduct `[FORGE #1]`).
- **Era unlocks (in-run content):** each era advance unlocks new packet types, node types, pipe tiers, and tools. The unlock tree is the era arc itself (M4).
- **Meta:** score-chasing across runs (survival, era reached, uptime, crises) + optional cosmetic pipe skins; no linear campaign.

### Difficulty Curve

Demand and complexity scale together (see Difficulty Ramp). The curve is tuned so each era introduces *one* major new system and lets the player consolidate before the next — no double-difficulty-spikes at a boundary. **Within each era, the spike cadence is hand-authored** (the demand director, M5) — bespoke per-era thresholds with an earned breath between peaks, never a flat ramp. `[ASSUMPTION: prototype tuning — per-era spawn curves are tunable; the curve *shape* (introduce → consolidate → surge) and its *rhythm* (peak → breath → peak) are the design invariants.]`

### Economy and Resources

| Scope | Economy | Notes |
|---|---|---|
| **MVP** | **No currency.** Budget = an action/capacity allowance per run; win = survive the surge (SLA). `[FORGE MVP scope]` | Keeps the prototype focused on the fun-test question. |
| **Full game** | **Score is core** (survival time + era reached + uptime % + crises survived — the open-run meta). **SLA contracts + currency** remain Could-tier: brands offer SLA contracts (meet uptime X% → paid; fail → penalty/loss) that fund upgrades, adding stakes. `[BRIEF Could-tier]` | Score-chasing + seeded runs + leaderboards are the core loop; contracts/currency are an optional stakes layer. |

### Monetization

*Researched per lavish review (2026); final model confirmed post-playtest (forge validation-first doctrine). Per-platform pricing is explicitly supported — Google Play added "buy once, play anywhere" AND separate per-platform pricing (Mar 2026); Steam enforces no hard price parity. Mini Motorways itself is free on Apple Arcade / ~$10 on Steam — same game, different model per platform.*

**Recommended model (pending playtest confirmation):**

| Platform | Model | Notes |
|---|---|---|
| **Steam (PC/Mac)** | **Premium B2P ~$8–12**, no ads. Optional **cosmetic IAP** (pipe skins, node themes, alert voice packs). Post-launch **paid DLC/expansions** (DTN expansion, era packs). | The Mini Metro/Motorways band; preserves the premium "save the internet" feel. |
| **Mobile (Android/iOS)** | **Freemium** (preferred for reach): free download + free slice (first 1–2 eras) + **"unlock full game" IAP (~$4–6)** + optional cosmetics + **optional rewarded ads** (watch → extra daily attempt / continue). *Alternative:* premium B2P (~$3–6) for brand simplicity over reach. | Free slice doubles as a perpetual playtest funnel (synergy with the forge's free-prototype doctrine). Rewarded-only ads; forced ads cheapen the feel. |
| **Web (deferred)** | If pursued: free, ad-supported, or a browser demo as a funnel. | Not a launch revenue path. |

**Hard rule — no pay-to-win, ever.** All monetization is cosmetic or full-game-unlock; never a gameplay advantage. This keeps cross-platform leaderboards fair (the leaderboard backend treats all players equally regardless of payment) and honors the fair-play forge pillar (#3).

**Open (post-playtest):** mobile freemium-vs-premium (reach vs brand simplicity); exact price points; cosmetic-IAP-at-launch vs post-launch timing.

---

## Run & Progression Framework

*(Adapted from the template's "Level Design Framework" — an open-ended-run game has runs, not levels.)*

### Run Structure

- **The run:** one open-ended, growing map (the internet) — not a sequence of levels. Eras advance *within* the run as SLA milestones are hit (M4); the run ends only when the Network Health meter empties (Win/Loss).
- **Map growth:** organic, Mini Motorways-style — nodes (brands, neighborhoods, data centers) appear over time and spread apart, driving the modernization pressure (legacy pipes can't span the new distances, M1).
- **Fresh seed per run (variety without AI):** each new main run rolls a FRESH procedural seed — new map layout, node-placement timing, and demand timeline — so re-runs never repeat the same challenges (the Mini Motorways model; no AI needed for variety). **Daily/Weekly Challenges are separate competitive modes** that FIX the seed so everyone faces the same map + demand + modifiers and competes globally (Replayability).
- **Surge set-pieces:** each era climaxes in a forecast, time-limited demand spike the player must survive (the MVP *is* the Era-3 streaming surge set-piece).

### Era Progression (in-run, not linear levels)

The six eras (M4) are the in-run escalation arc, advancing as you sustain uptime + modernize. There is no fixed campaign endpoint — the run is a survival/score chase; reaching later eras and higher scores is the goal. `[NOTE FOR DESIGNER: branching era paths / non-linear advancement is a Could-tier post-launch consideration, out of v1 scope.]`

---

## Numerical Design — Tuning Targets

*Ballpark prototype-starting values. Precise balance is a later iteration (`project-context.md` defers exact numbers to prototype time). All values are tunables in a single data source once balance work begins.*

| Parameter | Value | Note |
|---|---|---|
| Pipe capacity — Narrow / Standard / Wide / Backbone | 10 / 25 / 50 / 120 u/s | M1 |
| Pipe clean span / max — same tiers | ~3/5, ~6/9, ~12/18, ~25/40 tiles | M1 (tile size set at prototype) |
| Node throughput — Residential / Content / Gaming / Financial / Data center | 5 / 40 / 15 / 8 / 150 u/s | M3 |
| CDN reservoir buffer | up to 60 u/s | M3, Era 5 |
| Router port count — basic / mid / high | 4 / 8 / 16 | M3 (prototype-proven, experiment #12) |
| SLA uptime — era-advance threshold | ≥ 95% | per-class, sustained, to advance the era in-run |
| Network Health meter — breach drain | drains while any class < 90% uptime; recharges when healthy | grace countdown before the meter takes a hit |
| Network Health meter — empty | 0% → Error 404, run over | the loss condition (Win/Loss) |
| MVP surge win | uptime ≥ 90% through ≈ 90 s window | MVP win condition |
| Crisis warning lead times | strained 30 s / critical 10 s / pressure 20 s / forecast 15–60 s | M5 |
| Era milestone window (sustain to advance) | ~8–12 min per era, in-run | `[ASSUMPTION: prototype tuning]` |
| Run length (single run, until Error 404) | ~15–60+ min — varies by survival depth (early fail → late-era clear; 6 eras × ~8–12 min milestone) | total playtime = HOURS across many runs `[ASSUMPTION: prototype tuning]` |
| MVP surge slice | ~3–5 min | `[ASSUMPTION: prototype tuning]` |
| Streaming surge magnitude | 10× baseline demand | forge/addendum |
| Demand spawn rate base | scales linearly with era; surge = 10× spike | tunable |
| Draw snap radius | generous (no pixel precision) | M1 / Controls |
| Target framerate | 60 fps sustained | Technical Specs |
| Map size — MVP | 4–6 nodes | `[FORGE MVP]` |
| Map size — late eras | ~20–30 nodes | `[ASSUMPTION: prototype tuning]` |
| Latency SLA — Gaming class | end-to-end < 80 ms equivalent (in-sim ticks) | M2 |
| Loss SLA — Banking class | 0 drops (never) | M2 |

---

## Art and Audio Direction

### Art Style

**Mini Motorways clean-minimalist, 2D top-down** `[FORGE #5]`. Not realistic geography — a readable systems diagram with personality.

- **Scene:** a stylized, abstracted top-down map of nodes (routers/junctions/data centers/brands) connected by glowing pipes carrying colored packet traffic, on a dark (night) backdrop.
- **Palette:** dark background; glowing pipe colors; **node health color = green 🟢 → yellow 🟡 → red 🔴**. Packet-type colors per M2 roster.
- **Packet visualization:** colored dots flowing along pipes (blue = streaming volume, green = fast bursty gaming, gold = secure banking, white/grey = low-priority email). Flow speed reads as latency; dot density reads as bandwidth. **Within a pipe**, the dot color *proportion* reflects the lane allocation; **at each node**, dots exit by lane priority (Express → Standard → Best-effort), with lower-priority packets slipping through the *gaps* between higher-priority ones (work-conserving — they wait, but still progress, never fully starved) — the consequence of prioritization made visual (real router output-queue serialization).
- **Crisis juice:** leak spray (packets fountaining from a burst pipe), router blink-to-red, pressure-glow on over-saturated pipes, screen-edge alert flash (reducible — Accessibility), and a **clutch-resolution swell** — when a cascade unblocks (a reroute or bundle restore clears a chain of flows at once, see Core Gameplay Loop), a relief cue (audio swell + gauge-recovery bloom) sells the comeback.
- **UI chrome:** minimal — gauges (node strain, pipe pressure), the demand forecast, active alerts with satirical brand copy. Landscape 1280×720 reference; the viewport scales so wider/taller screens reveal more map (a routing-game advantage) `[RULING — user, 2026-08-05]`.
- **No purchased assets before the playtest gate** — placeholder art = colored rects + emoji + system shapes (single-polished-launch doctrine; the prototype is reference, not shippable) `project-context.md`.

### UI & Navigation

*The internet's state density is higher than Mini Motorways (each pipe: tier + 3-lane allocation + span + health; each node: type + health + policy; plus 9 packet types, the Network Health meter, the demand forecast, alerts). Mini Motorways' minimalism is the foundation; the higher density forces the additions below.* `[research: Mini Motorways GDC 'Wuselfaktor' + 'marrying complexity and minimalism']`

**Inherited from Mini Motorways (the foundation):**

- **The map IS the UI** — near-zero chrome; all state lives on the elements (color, glow, flowing dots). Minimalism carries the complexity.
- **Camera pan + zoom** (drag/scroll, pinch) is the primary navigation for a growing map — zoom out for overview, in for detail. Input-agnostic.
- **State read from the flow (Wuselfaktor):** congestion = dots piling up; a pipe's lane allocation = the color *proportion* of its dots; node health = glow color; degradation = the wear indicator. The player reads the network at a glance, not from HUD numbers.
- **Pause-to-plan**; color + icon + glow coding (accessibility: color never the sole encoder).

**Additions for our higher state density:**

- **Progressive disclosure:** lane allocation, tier details, and junction policy appear ONLY when a pipe/node is selected (a contextual popover/radial near it — Mini Motorways' upgrade-radial model). The default view stays a clean topology + flow + health.
- **Filter / focus modes:** toggles isolate a view — "only strained/critical nodes," "only Express lanes," "highlight one packet type's flow," "only degrading/legacy pipes," and a **strain-history / heatmap overlay** (where load has repeatedly outstripped supply — see Player Assistance). Essential with 9 types + lanes; without filters a large map is noise. (The modes double as low-vision aids — Accessibility.)
- **Alerts as navigation:** clicking an alert ("⚠️ BANKING dropping — Node X") pans the camera to the problem. Alerts double as a jump-to-problem nav system on a large map.
- **Minimap / overview:** a corner minimap (click-to-jump) for sprawling late-era maps (~20–30 nodes); Mini Motorways' smaller maps don't need one, ours likely do.
- **Consistent contextual controls:** select → popover (upgrade tier / allocate lanes / set policy / designate lane) — same interaction everywhere, input-agnostic (touch / mouse / controller).

### Audio and Music

**Custom/original exclusively — Suno-generated, owned outright by Moses** `project-context.md` `[BRIEF]`. This satisfies the streamer-monetization rule (Thomas Brush doctrine): Suno output is not registered to Content-ID fingerprint databases, so streamers monetize let's-plays without copyright flags. Every in-game track is a **paid-tier** generation (commercial rights); the soundtrack is a candidate parallel DistroKid release.

- **Mood:** urgency-driven — ambient beds between crises, pressure-riser stings as warning signs climb, alert stings on crisis trigger, satisfying resolution cues on fix/flow-restore.
- **Reactive SFX (Brush "every input gets an answer"):** pipe-draw, packet-arrival (per-class variants — 3–4 each), leak-patch, junction-cool, era-transition fanfare. Never ship silence.
- **Crisis alerts:** the satirical brand-down voice/sting ("⚠️ YOU_TUNE: DOWN — 2.3B users affected") is signature audio.

---

## Accessibility

- **Colorblind-safe by design.** Color is **never** the sole encoder: packet types carry **icon + shape** in addition to color; node states carry **icon + outline** in addition to the green/yellow/red glow. Ship Deuteranopia / Protanopia / Tritanopia palette toggles.
- **Reduced-motion option** — disable screen-edge flash and screen shake; crises still readable via gauges + icons + audio.
- **Pause anytime** — no real-time-pressure-only design; the player can always stop to think (core to the fair-crisis model).
- **Scaling** — UI/gauge scaling for small screens and low vision; readable at a glance on phone and monitor `[FORGE #5]`.
- **Input alternatives** — full touch / mouse / controller parity (Controls); no input-dependent mechanics `[FORGE #6]`.
- **Subtitles/captions** — all audio alerts captioned on screen.
- **Dual-audience balance** (forge weak point #3) — the approachable surface (the metaphor) and the depth (real QoS) are the same game; an optional advisor hint layer (Could; assumed off by default `[ASSUMPTION: advisor hints]`) is the safety valve for the most casual players. Playtest both audiences explicitly.

---

## Technical Specifications

*GDD-level: performance, platform, asset budgets. Architecture/engine system design is `gds-game-architecture`'s job — no engine-implementation specifics here.*

### Performance Requirements

| Target | Requirement | Measurement |
|---|---|---|
| Framerate | **60 fps sustained** (baseline, every target device) + **optional 120 fps / unlocked toggle** on capable high-refresh devices (common in 2026) — off by default on mobile (battery/heat), available as a preference. 60 is the smooth-playable target; 120 is a cosmetic premium-feel for 120Hz displays (no gameplay advantage). | measured over a 10-minute run with a late-era node count |
| Load time | Run load < 3 s on target phone | cold start to interactive |
| Memory | within a 2021 mid-range phone budget (define the concrete device budget at prototype time — Open Question) | peak during a late-era surge |

The simulation updates on discrete ticks/events rather than continuously, so a busy late-era map holds 60 fps — a readability and fairness requirement (the player must read a live topology smoothly).

### Platform-Specific Details

- **Steam PC/Mac** (Windows, macOS) — mouse + controller; landscape.
- **Mobile** (Android, iOS) — touch; **landscape-only** `[RULING — user, 2026-08-05]`.
- **Same game** on all — no separate mobile build, no separate feature set `[FORGE #6]`.
- **Web** — deferred but kept viable by the chosen renderer; not a launch platform.
- **No console.** `[BRIEF]`

### Online Services (leaderboard)

- **Global leaderboard service — a v1.0 launch dependency.** Daily, weekly, all-time, and friend leaderboards (Replayability) require a lightweight online backend: accounts/auth, score submission, validation, storage, cross-platform (Steam + mobile). **Cheat-resistance via seed determinism:** because a seeded run is deterministic from its seed, the service validates each submitted run against the seed (re-simulate or action-log check), so no heavy anti-cheat is needed. The simulation MUST be deterministic from a seed — which is also what makes seeded daily/weekly runs fair in the first place. (The build/buy/host + account-model decisions are `gds-game-architecture` + production's job; this states the requirement.) **MVP: no leaderboard** (fun-test only).

### Asset Requirements

- **Prototype (fun-test):** placeholder art — colored rects + emoji + system shapes; 2D top-down. **No custom or purchased assets before the playtest gate** (single-polished-launch doctrine; the prototype is reference, not codebase) `project-context.md`. Carry just-enough juice (colored packet dots, leak spray, crisis alert) to prove the *concept*, not custom art.
- **Full game (post-playtest): custom, OWNED assets** — no purchased or licensed art (matches the Suno-audio ownership doctrine). Governed by a **cohesive Mini Motorways-style art bible** (palette, line weight, material treatment, lighting) applied to every asset — homogeneity comes from the art bible, not the tool.
- **Candidate art pipeline:** Blender (model in 3D → render orthographic / top-down to 2D sprites for consistent lighting, material, perspective; or Grease Pencil for pure 2D), driven via MCP for AI-assisted production. All assets share one render pipeline → inherently cohesive. The 2D-game constraint stands (`[FORGE #5]`): Blender is a 2D-asset pipeline here, not a 3D game. *(Specific tooling / render setup is `gds-game-architecture` + production's job; this states the asset strategy.)*
- **Audio:** Suno-owned music + reactive SFX library (per-class variants).

---

## Development Epics

*Epic summary here; high-level stories and traceability in `epics.md`. Each epic delivers playable value and maps to pillars/mechanics.*

| Epic | Delivers | Pillars | MVP? |
|---|---|---|---|
| **E1 — Core Routing Engine** | Draw-between-nodes, snap, packet-flow simulation, pipe graph | P1 | ✅ |
| **E2 — Packet Types & QoS** | Two MVP packet types (email + streaming), priority lanes, junction triage, SLA tracking | P2 | ✅ |
| **E3 — Topology & Nodes** | Node types, map growth, node health states | P1, P3 | ✅ |
| **E4 — Crisis Model** | Warning signs, the five archetypes, fair-failure logic | P3 | ✅ (Surge archetype) |
| **E5 — Era Progression & Lifecycle** | MVP Email→Streaming transition, upgrade/degradation | P4 | ✅ (one transition) |
| **E6 — Win/Lose & SLA** | Uptime tracking, survive-the-surge win, lose/retry | — | ✅ |
| **E7 — Cross-Platform Input** | Touch / mouse / controller parity, draw snap | — | ✅ |
| **E8 — Art & Audio Juice** | Mini Motorways visual, Suno audio, reactive SFX | P1, P3 | partial (enough to prove concept) |
| **E9 — Accessibility** | Colorblind, scaling, reduced-motion, captions | — | ✅ (core) |
| **E10 — Full-Game Scope** | Remaining eras (4–6), remaining packet types, contracts/currency economy, V2 AI stress-test | P2, P4 | ❌ (full game) |
| **E11 — Production Rebuild** | Fresh codebase after the fun gate — prototype is reference only, code discarded; rebuild on the production architecture | — | ❌ (post-fun-gate) |

---

## Success Metrics

### Technical Metrics

- 60 fps sustained on target desktop + 2021 mid-range phone over a 10-min run.
- Run load < 3 s on target phone.
- Zero crash-soft-locks (the no-soft-lock invariant is a test contract).

### Gameplay Metrics

- **The fun gate (top metric):** MVP playtest — would players play again? Target: majority of both test audiences (engineers + non-engineers) choose to play a second run. Run length and fail→retry rate are leading indicators.
- **Run-reach distribution** (full game): how far runs get (which era players reach before Error 404) surfaces tuning/pacing problems and the difficulty ceiling.
- **Skill growth:** players measurably improve at predicting crises across runs (fewer unforced SLA failures over time) — proof the educational byproduct lands.
- **Appeal:** capsule/trailer "I want THAT" reaction pre-play (Tyroller) — qualitative playtest signal.
- **Replay retention:** runs-per-player and return rate — the open-run model's success = players chasing "one more run" (forge weak-point #1, fun-for-50-hours).

---

## Out of Scope

**Cut for v1.0 (the polished launch):**

- **Factorio-style construction sim** — material selection, production chains, zoning `[FORGE rejection]`. Draw + React is the mechanic.
- **Random / unfair crises** — every crisis is a design consequence `[FORGE #3, rejection]`.
- **Real brand names** — satire only (YouTune, Amazoom, Goggle, Glitch; Netflix/Discord kept) `[FORGE rejection]`.
- **Early access** — single polished launch `[FORGE #7]`.
- **A separate mobile version** — one game, input-agnostic `[FORGE #6]`.
- **Console platforms** `[BRIEF]`.

**Deferred to post-launch / full-game (Could-tier):**

- The full era arc (eras 4–6), remaining packet types (gaming/banking/voice/multicast/IoT/AI), data centers/CDN, and Era 6 overlay abstractions. (MVP = eras 1–3, email→streaming.)
- SLA contracts + currency economy (score-chasing, daily/weekly seeded runs, and leaderboards are CORE to the open-run model, not deferred).
- Challenge modes (no-upgrade, zero-drop) and cosmetic pipe skins.
- The **V2 AI stress-test system** (scoped carefully when reached — forge weak point #4).
- Web platform (kept viable, not launched).
- **Post-launch expansion candidate — interplanetary / space networking (DTN):** a regime change (light-minute latency, intermittent link windows, store-and-forward bundling) that adds new mechanics, not a reskin. Grounded in CCSDS / ECSS SpaceWire / IETF DTN. Only if the game is successful.

---

## Risks & Open Questions

### Risks (carried from the forge, addressed in this GDD)

| # | Risk | How the GDD addresses it |
|---|---|---|
| 1 | **The fun question is unproven** (top risk) | The GDD defines the fun-testable loop precisely (M1–M6, the loop diagram, the MVP win condition); the MVP exists solely to test it. The prototype must carry *just enough* juice to prove the whole concept, not only the loop `[BRIEF risk #5]`. |
| 2 | **The plumbing metaphor breaks at higher layers** (VPN/VLAN/SDN) | The era list stops literal plumbing at layers 1–4 (Eras 1–4); Era 5 adds reservoir abstraction; Era 6 *abstracts* modern tech as gameplay mechanics (secure-tunnel overlay, programmable reroute, adaptive demand). Metaphor boundary documented (M4). |
| 3 | **Engineer / non-engineer audience split** | The QoS + packet-type model is the bridge (approachable surface, real depth); dual-audience playtest mandate; optional advisor hint layer (Could). |
| 4 | **The V2 AI stress-test is ambitious** | Out of MVP; scoped as post-launch replayability; design-sketched as a fair auditor, not built here. |
| 5 | **Prototype methodology** — graybox may under-sell a feel-driven game | MVP stays graybox-defensible (routing fun is mechanic-driven) but carries enough juice (crisis alert, colored dots, leak spray) to prove the concept, not just the loop `[BRIEF risk #5]`. |

### Open Questions

1. **Monetization** — documented in the Monetization section (Steam premium + mobile freemium-or-premium, no pay-to-win, per-platform pricing OK). Post-playtest sub-decisions: mobile freemium-vs-premium, exact price points, cosmetic-IAP-at-launch timing.
2. **Single-player vs co-op** — **single-player for v1.0** (genre norm: Mini Motorways & Mini Metro are single-player; forge doctrine; tight scope). Co-op (two engineers on one shared internet) is a **post-launch Could-tier experiment** — neat fantasy but scope-heavy (real-time shared-topology netcode + conflict resolution). `[BRIEF]`
3. **Concrete phone perf budget** — not the framerate (60, decided); this means **naming the target device class** (e.g., iPhone 12 / Galaxy S21 / Pixel 6 — a 2021 mid-range phone) so the **memory and thermal** budgets are concrete (≤X MB RAM, sustained 60 fps without thermal throttle over a 10-min run). Pinned at prototype via on-device profiling.
4. **Where the literal-plumbing campaign ends vs sequel territory** — does v1.0 ship through Era 6, or stop at Era 4/5 with later eras as DLC/sequel? `[NOTE FOR DESIGNER]`
5. **Optional advisor hint layer** — include the Could-tier casual-player hints in v1.0, or keep the loop pure? Playtest decides.
6. **QoS default lane** — all traffic starts on Standard (gentler, chosen); Best-effort is the harder, more-realistic variant (the internet's native default). Decide at prototype based on how punishing the discovery curve feels.
7. **Leaderboard backend** — in-scope for v1.0 (requirement in Technical Specifications → Online Services). Open: build-vs-buy-vs-host + cross-platform account model + **validation strategy** (lean lightweight: action-log structural checks + statistical anomaly detection + optional spot-check re-sim — vs full per-submission re-simulation, which would need a portable sim core). Tech stack is `gds-game-architecture` + production's call.

### Assumptions Index

Every `[ASSUMPTION: ...]` inline tag, collected:

- **Prototype tuning** — all Numerical Design values (capacities, spawn rates, thresholds, era durations, node counts) are prototype-starting ballparks, not final balance.
- **Roster sizing** — the 9-type roster is the full-game set; the MVP ships 2 (email + streaming) per forge scope.
- **Advisor hints** — assumed *off* by default (Could-tier), pending playtest.

---

*End of GDD v1. Epic detail and traceability: `epics.md`. Provenance: `decision-log.md`. Next downstream: `gds-game-architecture`. Human review of this document runs via lavish before the PR opens.*
