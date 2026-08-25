# Spec — Traffic Model: Access Tier, Bounded Demand, Aggregation, Terminal Diversity

- **Job:** `packet-plumber-traffic-model-design` · branch `pp-traffic-model-design` (base `v2`)
- **Status:** design spec — lavish review BEFORE the PR; story cards + GDD amendment accompany it
- **Source (the ruling):** user ruling 2026-08-15 — the surge-explainer §Section B design notes are
  **tasks to be done**: the traffic model gains realism so congestion lives where it does in real
  networks. Primary source artifact: `surge-explainer.html` §B (the "Your design — narrow as
  residential access" block, with the 1G/40G/100G → u/tick math).
- **Scope guard:** design docs + story cards ONLY. No code, no balance.json changes, no
  implementation — those are the story cards' jobs (cards at the bottom of this file's family:
  stories-v2.md slice 5B).

---

## 1. The problem, one line

**Today an endpoint can be its own chokepoint** — the demand director spawns map-wide volume with
no per-terminal gate, so on a small map a single residential (throughput 5 u/s = 0.167 packets/tick)
can be asked to source 4/tick, and packets drop at its own spawn (pool E22) and its own
serialization (queue E9). In real networks that never happens: one FTTH subscriber cannot congest
their own drop. **Congestion is an aggregation event.** This spec turns that sentence into four
mechanics (the four threads), each a story card.

Ground truth (shipped, verified in code):

| Fact | Value | Where |
|---|---|---|
| Packet transit cost | 30 u/hop, **flat for every class** (`bandwidth_demand` loaded, not consumed) | `core/flow.odin:405`, `data/packet_types.json` |
| Pipe tiers | narrow 5 / standard 15 / wide 40 u/s; routing cost 20/10/5 | `data/pipe_tiers.json` |
| Residential node throughput | 5 u/s (= 0.167 pkts/tick) | `data/node_types.json` |
| Era-3 demand | email 4/tick + streaming 2/tick = 6 arrivals/tick = 180 u/s | `data/demand.json` |
| Director spawn | typed source/sink selectors → seeded weighted-random pick, `effective_volume` per spec | `core/flow.odin:600+`, `core/demand.odin` |
| Pool cap (E22) | 512 in-flight; ladder shed BE→S→E; arrival self-drops when lowest candidate | `core/flow.odin:476` |
| Lane bound (E9) | 6/lane; same ladder at admission | `core/flow.odin:710` |
| Map growth (5.1) | one terminal / 120 ticks, TERMINALS only, E31 validity, rejection-sampled, seed-derived | `core/growth.odin` |

The GDD's M1 table still shows aspirational tiers (narrow 10 / standard 25 / wide 50 / backbone 120);
the **shipped catalog is the ground truth this spec and its cards target** (5/15/40). Flagging the
discrepancy once here; the cards and the GDD M6 amendment use the shipped numbers.

---

## 2. The real-world scale math (cited from the explainer)

1 u = the transit work of one 1500-byte frame crossing one hop. At 20 Hz logic:

| Line rate | Packets/sec | u/tick |
|---|---|---|
| 1 G (FTTH drop) | 83,333 pps | **4,167** |
| 40 G (metro) | 3.33 M pps | **166,667** |
| 100 G (core) | 8.33 M pps | **416,667** |

Ratios **1 : 40 : 100** — the FTTH ladder. The 512-packet pool ≈ 768 KB ≈ 6 ms of 1-Gbps line rate:
**real-router buffer scale** (a packet count, independent of the unit scale). The catch the design
must hold: today's demand (6–24 pkts/tick ≈ 1.4–5.8 Mbps aggregate) is 100–1,000× below a single
1-G link — **nothing would ever congest at literal scale**. The sim is playable because its tiers
(5/15/40 u/s) compress the ratio scale ~1,000× and the demand saturates them.

**Design shape (the explainer's own — cited as the SOURCE, with the r1 correction applied below):**
narrow = the last-mile drop to a residential, sized so ONE
subscriber's traffic never congests it — narrow ≈ **8–10 u/s** (0.27–0.33 pkts/tick per edge) and a
residential emitting ~**0.2 pkts/tick** (its share of 6/tick across ~30 terminals) fits with
**~1.5× headroom**; the access link stops being the choke. Congestion appears where it should: when
many residentials' flows aggregate onto a metro/backbone link (standard 15 / wide 40), and the ×10
surge is an **aggregation event** — every subscriber streaming one event saturates the shared core,
not the access drops. **[Perkins r1 B2 — the operative value is NOT the explainer's 0.2:** 0.2
pkts/tick ≈ 6 u/s exceeds the residential node's own throughput (5 u/s = 0.167 pkts/tick), so the
canon cap is throughput-relative (Thread 2): residential ≈ 0.083 pkts/tick at
  `cap_fraction_permille` 500,
with the access link's headroom computed from it.]

---

## 3. The four threads (each = one mechanic = one story card)

### Thread 1 — Narrow as residential access (the access tier)

**Mechanic (Given/When/Then):**
- **Given** a residential terminal connected by a single narrow pipe to its aggregation point;
- **When** that residential's own traffic (bounded per Thread 2) flows;
- **Then** the narrow access link **never** congests from the one subscriber — its headroom vs the
  per-terminal cap is ≥ ~2× (pre-5.10) and ~3–4× (post-5.10) — and congestion appears only where
  many subscribers' flows **aggregate** onto shared links (standard/wide).

**Real-world rationale:** real FTTH — a 1-G drop does not congest from your own streaming; congestion
lives where many subscribers share a link. The 1 : 40 : 100 u/tick ratio makes narrow/standard/wide
the access/metro/core tiers of the same topology.

**Balance levers (data-driven per canon):**
- `data/pipe_tiers.json` → narrow `capacity_units` 5 → **~8–10** (proposed starting point;
  playtest-tunable). `cost` stays 20 — the routing-cost ladder is **moot on access links** (a single
  path; the ladder only matters between routers where alternatives exist — the capacity-cost ruling
  2026-08-13 is untouched; between routers, flows still prefer fat pipes).
- **5.9-vs-5.10 decoupling (Perkins r1 B2 note):** the per-terminal cap (Thread 2) is sized against
  the NODE's own throughput, so story 5.9 is self-consistent at the CURRENT narrow (5 u/s) — its
  zero-drop acceptance does not depend on this rebalance; the narrow rebalance adds access-layer
  headroom on top (the explainer's ~1.5× target is comfortably exceeded post-5.10).
- Optional: narrow `display_name`/canon role → "access" flavor (wording is the terminology audit's
  lane — cards do not rename; they add canon role via the GDD M6 entry).

**Determinism constraints:** pure catalog change → `cat.hash` folds every catalog byte → **legitimate
deliberate re-bless** of T1/T2 goldens (the 4.3 discipline: byte-verify `.log.bin` differs only in
the version field, splice the old catalog_hash, cause-document). No new commands → **no LOG_VERSION
bump**.

**Canon interactions:** E22 pool — unchanged (the pool still backstops the map; it no longer sheds
endpoint self-congestion because there is none); E9 lane bounds — unchanged; 4.1 congestion — a congested
narrow now *genuinely* means an undersized access link (honest diagnosis, the readability payoff);
5.8 QoS — access links carry the same 3 lanes; aggregation (Thread 3) is where the lane call matters.

### Thread 2 — Per-terminal demand caps (endpoints never self-congest)

**Mechanic (Given/When/Then):**
- **Given** a live terminal of role R and the demand director's spawn pass for a spec;
- **When** the director's volume would assign more spawns to one terminal than its per-terminal cap
  this tick;
- **Then** the capped terminal is **ineligible for source picks** and the volume lands on other
  terminals (or waits) — **no endpoint can ever be asked to source more than a fraction of its own
  forwarding capacity**, so no endpoint self-congests.

**Why it's the load-bearing invariant:** everything else in this spec assumes "endpoints never
self-congest". Without it, a small map makes the endpoint the chokepoint (drops at spawn E22 + at
serialization E9 at its own drop) — the exact noise the surge explainer diagnosed at 10:04.
**Scope (Perkins r2 N9):** the invariant applies to **director-spawned demand** (flow.odin §1b, the
real demand model); the LEGACY path (flow.odin §1a `flow_seed_demand` — the slice-1 trivial
fixture used by legacy demos/tests) is exempt by design (fixed src/dst, no director).

**Enforcement mechanism (Perkins r1 B1 + r2 fix-audit B1 — spawns are INTEGER per tick,
`core/flow.odin:646` `for k in 0..<vol`, AND the state paths are INTEGER-ONLY (ODN-10,
odin-architecture-v1.md:398/:1236; `balance.json` loads with `parse_integers = true` +
`jint_strict`, `core/catalog.odin:675` — a fractional cap would fail-fast at catalog load):**
a per-terminal **spawn accumulator in integer milli-packet units** (fixed-point):
- **Credit:** `spawn_credit_milli[terminal_slot]` — integer milli-packets; a source spawn costs
  **1000**; a terminal is **pickable only while `credit_milli >= 1000`** (eligible set =
  credit-gated subset — no per-tick fractional compare anywhere).
- **Accrual:** `accrue_milli = cap_fraction_permille × throughput_units ÷ packet_bandwidth`
  (integer division, ODN-10) each tick, per live terminal. `balance.json` holds
  `cap_fraction_permille` (int; proposed **500** = 50.0%). Residential: 500×5÷30 = **83 milli/tick**
  (0.083 pkts/tick = 1 spawn per ~12 ticks); content_host: 500×80÷30 = **1333 milli/tick**
  (1.333 pkts/tick); a 150 u/s campus: 2500 milli/tick (2.5 pkts/tick).
- **Burst ceiling (type-relative — Perkins r2 W4):** `MAX_CREDIT_MILLI(type) = 1000 × max(1,
  ceil(cap))` with `ceil(cap) = (accrue_milli + 999) ÷ 1000` — sized so EVERY type can achieve
  its cap long-run (no silent clamp for high-throughput types: a campus at 2.5 pkts/tick gets
  ceiling 3, not a fixed 2). Residential: ceiling 1 → **no burst** — the pre-5.10 latency
  constraint (Perkins r2 W5: a burst-2 through the 5 u/s access serializes the 2nd packet in
  12 ticks = 600 ms > email's `latency_tol_ms` 500) is avoided by construction.
- **State home (Perkins r2 W2):** `spawn_credit_milli` lives in **Flow_State beside `lane_caps`**
  (`core/flow.odin:96`), **updated in place** by the flow.odin §1b spawn pass (accrue + consume) —
  NOT demand.odin, which is structurally stateless (`scripted_plan_pressure(cat, era, tick)` takes
  no `Run_State`; `Pressure_Plan` is scratch, destroyed per tick).
- **T1 hash surface:** the accumulator is **derived state** — the `lane_caps` precedent
  (`core/flow.odin:85` "NEVER serialized, deterministic") — never serialized; its T1 surface is the
  resulting `(class, src, dst)` spawn stream, already in the hash (the slice's deliberate re-bless
  covers the shifted stream). If a future story makes it run-scoped, that parameter serializes with
  a LOG_VERSION bump — the standard caveat.
- Determinism: the accrue is a pure function of tick; the eligible set is derived; the pick keeps
  the **ONE rng draw per pick** discipline (ODN-10) — replay is byte-identical. No new commands.
- (The simpler "1 spawn per N ticks, N = ceil(1/cap)" integer form is the degenerate case at
  MAX_CREDIT 1; the milli-credit accumulator is the general form and the one specified.)

**Balance lever — the cap value is THROUGHPUT-RELATIVE, uniformly (Perkins r1 B2 — the explainer's
0.2 pkts/tick ≈ 6 u/s EXCEEDS the residential node's throughput 5 u/s = 0.167 pkts/tick and the
pre-5.10 narrow service rate, so a capped residential would backlog and E9-shed at its OWN access
lane — the noise M6 exists to kill; and "content_host caps AT its throughput" was inconsistent
with "residential caps at a fraction"):**
- `cap(type) = cap_fraction_permille × throughput_units(type) ÷ (packet_bandwidth × 1000)`
  (the integer fixed-point form of `CAP_FRACTION × throughput ÷ packet_bandwidth`) — a fraction of
  the type's OWN throughput, applied **uniformly to every type**, so the invariant holds by
  construction: source demand ≤ the fraction × the terminal's own forwarding capacity → the
  endpoint's lane never fills from its own spawns, no E9 shed at its own access, no 600% congestion
  flicker.
- Proposed start `cap_fraction_permille = 500` (50%): residential ≈ **0.083 pkts/tick (2.5 u/s)** —
  50% of its 5 u/s throughput, ~2× headroom vs the pre-5.10 narrow (5 u/s), ~3–4× post-5.10
  (8–10 u/s); content_host ≈ **1.33 pkts/tick long-run (40 u/s)** — 50% of its 80 u/s (burst ≤
  2/tick via its type-relative ceiling 2). Playtest-tunable; `balance.json` holds
  `cap_fraction_permille`.
- The cap is a **hard bound on the variance**, not the average: the weighted-random pick already
  shares volume; the cap stops small-map concentration (the MVP's 4–6-node map is the pathological
  case).
- **Headroom is computed from the NODE throughput** (the binding constraint — the access link is
  sized on top of it in Thread 1 / story 5.10).

**Consequence the cards must carry (explicit, not hidden — Perkins r1 W9/W10 + r2 W6 pins):** with
throughput-relative caps the era-3 script (email 4/tick + streaming 2/tick, ×10 surge) **cannot
land on the current 4–6-node map** — email needs ~48 residentials at cap 0.083, the ×10 surge needs
~15 content_hosts at cap 1.33. Card 5.9 **owns the re-tune**: the era-3 demand profile + 5.1 growth
pacing + surge multiplier are **re-validated TOGETHER** so the MVP surge still lands as an
aggregation event. The invariant is canon; the values are playtest tuning. If "growth congestion"
silently becomes "the surge never lands", that is a fail, not a feature. **The pins are
QUANTITATIVE (r2 W6 — "zero-drop" alone is satisfiable by any rate ≤ throughput):** W9 pins the
RATE — on a known seed, the surge window's streaming spawn count ≥ the re-tuned expected volume ×
0.95 (tolerance) while per-terminal spawns ≤ cap × window + burst allowance and credit ≤
MAX_CREDIT; W10 pins the same rate envelope on the at-cap scenario (spawns ≤ ceil(cap × W) + burst
allowance over a W-tick window on a known seed) AND the zero-drop-at-own-access assertion AND
end-to-end transit ≤ the class latency tolerance (r2 W5's burst-latency guard).

**Sink side (Perkins r1 W6):** the M6 invariant is **source-side by scope** — a terminal is never
ASKED to source beyond its cap. Sink-side concentration (many packets delivered to one residential)
remains bounded by the weighted-random dst distribution + the existing E9 admission at the access
lane (a residential receiving more than its line carries is a legitimate, telegraphed congestion
site — the 4.1 lane telegraph makes it readable, not the endpoint mystery M6 removes). A
sink-side admit accumulator is a documented balance-time option if playtest shows sink-drop noise.

**Determinism constraints:** `cap_fraction_permille` lives in `balance.json` (→ the slice's
legitimate re-bless). Spawn sequence changes (the (class, src, dst) stream shifts with the
eligible-set gating) → **deliberate re-bless**, cause-documented. All seed-derived; **no
wall-clock**. No new commands → no LOG_VERSION bump.

**SLA-accounting seam (must be pinned by the card — Perkins r2 N1: the pin home is
`sla_test.odin:88`, `sla_check_invariant`):** a capped spawn is **skipped before
`flow_try_spawn`** — it is NOT a demand event (never reaches `sla_count_demand`); a pool-dropped
arrival IS (it counts demand then drops). The invariant `demand_seen == delivered + dropped + live`
(E24) must hold under both paths — pinned there.

**Canon interactions:** E22 — spawn drops become aggregation drops, never endpoint self-drops (the
pool cap 512 stays); E9 — admission shed at the shared uplink, not the endpoint; 4.1 — a residential
node no longer shows congestion from its own spawns (congestion on a terminal = undersized access, honest);
5.1 growth — growth lowers per-terminal load (more terminals share the volume; the cap is the floor
that keeps it honest on small maps).

### Thread 3 — Aggregation groups (congestion lives at the shared uplink)

**Mechanic (Given/When/Then):**
- **Given** a cluster of nearby terminals (a neighborhood analogue) whose flows share one
  player-built uplink;
- **When** aggregate demand from the cluster rises (base or the ×10 surge);
- **Then** the shared uplink — not any member terminal and not any access drop — is where congestion
  appears, and the player's router/tier/bundle/QoS decisions on that uplink are what relieve it.

**Real-world rationale:** the honest choke is "a handful of residentials sharing one uplink". The ×10
surge is an **aggregation event** — every subscriber streaming one event saturates the shared core.

**Balance levers:**
- Growth (5.1) gains a **group-bias term** in the placement draw: a spawned terminal is drawn near an
  existing cluster member (a group radius + a group-size cap), so clusters actually concentrate.
- The demand director gains a **group-scoped weight**: members of the same group share an uplink
  target (flows from a cluster land on the cluster's aggregation point), so the surge stresses the
  group uplink.
- Proposed starting shape: 3–8 terminals per group; group radius **~4–6 tiles** (Perkins r1 W5 —
  the radius must exceed `GROWTH_MIN_SEP_TILES = 3` (`core/growth.odin:76`), the E31 packing floor,
  or members cannot pack inside it; radius ≥ 4 is the smallest coherent value, 4–6 keeps clusters
  tight). Data-driven (balance.json) at the legitimate re-bless; core consts until then (the growth
  precedent — 5.1's tuning lives as consts for exactly this reason).

**Conflict resolution — growth-spawn validity (E31) vs group placement (EXPLICIT):**
- E31 (hard contract, untouched): every spawned terminal is (a) connectable-within-span of a live
  junction, (b) min-separated from nodes AND pipe segments, (c) inside the grid; invalid candidates
  rejection-sample from the rng stream within a bounded budget.
- **Resolution:** the group bias is a **soft preference inside the E31 validity envelope** — the
  bias draw runs first, the E31 validity test runs on the biased candidate, and rejection-sampling
  (which can land outside the group) is unchanged. A group never forces a placement that violates
  E31, and E31 never re-routes a group. **The uplink itself is never forced** — the player wires it
  (the group concentrates *demand*; the player builds the fat pipe). This keeps E31 byte-stable in
  contract while making clusters emergent from the seed.
- Rejected alternative (recorded): demand-side-only grouping (no topology bias) would concentrate
  flows without a shared link — the "congestion" would smear across whichever routes exist and the
  honest aggregation picture never forms.

**Determinism constraints:** groups are derived from the seed (growth placement draws + the type
pick) + the live topology — fully seed-derived, no wall-clock, no log entries (growth is already
log-free; the bias extends the same derive-don't-record rule). T1 shifts (spawn sequence + topology)
→ deliberate re-bless.

**Canon interactions:** 5.1 growth (the bias extends the growth draw — the card must keep
"existing goldens unshifted" provable at the growth-const level and cause the single deliberate
re-bless at the slice boundary); 4.2 surge (the surge = the aggregation event; crisis engine's
`preventive_redesign` copy already says "add a parallel pipe or a higher tier on the spike's path" —
now that path is the group uplink); 5.8 QoS (lane assignment at the group uplink is the lever);
E31 (hard floor preserved, above).

### Thread 4 — Diverse terminal types (schools, offices, homes)

**Mechanic (Given/When/Then):**
- **Given** the terminal roster carrying multiple class analogues (residential / small-biz / campus);
- **When** the director and growth spawn/weight terminals;
- **Then** each type emits a **different, bounded demand profile** (volume, per-terminal cap,
  throughput) — a campus emits far more than a home — and the type is readable without color.

**Real-world rationale:** schools, universities, and data centers emit far more than a home; the
terminal roster is the honest spectrum. The roster entries are catalog data (`node_types.json`), but
**a NEW terminal role is a code change (Perkins r1 W7 — `Terminal_Role` is a closed enum
`core/catalog.odin:22`), not pure data:** the enum gains a variant + `role_from_name`
(`core/catalog.odin:1011`) + the `collect_terminals` role selector (`core/flow.odin`) + the growth
type pick (`core/growth.odin`). Card 5.11 names these touch points explicitly.

**Balance levers:** `data/node_types.json` — new entries (e.g. `small_biz`, `campus`) with
`terminal_role`, `throughput_units`, `demand_weight`, `era_introduced`, and the per-type cap/profile
fields Thread 2 introduces (cap = `cap_fraction_permille × throughput ÷ packet_bandwidth`, uniform). Distinct shapes/icons (never
color alone — the a11y invariant, E9.1).

**Determinism constraints:** catalog data → `cat.hash` fold → deliberate re-bless. New types respect
E31 spawn validity + the 5.6 placement separation. The growth type-pick and the director's
source_role selectors are rng/topology-derived — deterministic.

**Canon interactions:** 5.1 growth (which types growth spawns, and when — era gating); demand
director (source_role selectors resolve against the new types); E31 (validity applies per type);
5.6 placement (terminals never block router placement — holds for every new type).

**Related-but-out-of-scope (flagged, not a fifth thread):** `bandwidth_demand` (streaming's ×2) is
loaded but **not consumed** — every packet costs the flat 30 u/hop. Thread 4 makes per-class transit
cost meaningful, but wiring `bandwidth_demand` is a separate balance decision (it changes every
transit-time number and the ECMP/economics); it is deliberately left for a future decision, named
here so nobody mistakes the omission for an oversight.

---

## 4. Interaction matrix (the four threads × existing canon)

| Canon | Thread 1 (access) | Thread 2 (caps) | Thread 3 (groups) | Thread 4 (types) |
|---|---|---|---|---|
| **E22 pool (512)** | unchanged | spawn drops become aggregation drops, never endpoint self-drops | unchanged (aggregation shed at the uplink) | unchanged |
| **E9 lane bound (6)** | unchanged | admission shed at the shared uplink, not the endpoint | the shared uplink is where the shed fires | unchanged |
| **4.1 congestion** | congested narrow = honest undersized-access signal | residential congestion = undersized access, not own spawns | congestion localizes to the group uplink/router | per-type throughput feeds the ring |
| **5.1 growth (E31)** | access tier is the growth target's natural link | growth lowers per-terminal load; cap keeps small maps honest | **group bias inside the E31 envelope (explicit resolution)** | growth type-pick + era gating |
| **5.8 QoS** | access links carry 3 lanes | — | the group uplink is where lane assignment matters most | — |
| **Capacity-cost routing (2026-08-13)** | cost ladder moot on access (single path); untouched between routers | — | — | — |
| **4.2 surge** | — | surge lands only via the re-tune (W9: post-cap surge-lands pin; needs ≥(20÷cap) terminals) | the surge IS the aggregation event | — |
| **SLA accounting (E24)** | — | **credit-gated skip ≠ demand event; pool-drop IS — pin both** | — | per-type profiles feed SLA |

**Sink side (W6 scope):** the caps column covers SOURCE-side demand; sink-side concentration is
bounded by the weighted-random dst distribution + E9 at the access lane (see Thread 2).

**Determinism spine:** every thread is seed-derived (rng draws from `state.rng`), topology-derived,
or catalog data — no wall-clock anywhere; replay stays byte-identical with **one deliberate,
cause-documented re-bless** at the slice boundary (all four threads shift the (class, src, dst)
spawn stream and/or the catalog hash). No new command kinds → **no LOG_VERSION bump**. New tuning
values follow the growth precedent (core consts → balance.json at the legitimate re-bless).

**Naming disambiguation (Perkins r1 W8):** this design's M6 block is a primary GDD mechanic in the
M1–M6 series — it is **NOT** one of the six post-fun-gate mechanics (stories-v2 slice 8+, 8.1–8.6);
the six remain post-fun-gate and untouched. **Catalog reconciliation (Perkins r1 W4):** the GDD M1
tier table (narrow 10 / standard 25 / wide 50 / backbone 120) is the aspirational full-game ladder;
the SHIPPED catalog (5/15/40) is the current ground truth this design and its cards target — the
reconciliation is the balance gate (a catalog retune is a data change, golden-discipline re-bless
included).

---

## 5. Sequencing proposal — story cards in stories-v2

**Proposal: a new slice between 5 and 6 — "Slice 5B — Traffic realism", stories 5.9–5.12** (story
numbers continue slice 5's sequence; no existing card renumbered).

| Card | Thread | Order rationale |
|---|---|---|
| **5.9 — Per-terminal demand caps** | 2 | The invariant everything else assumes ("endpoints never self-congest"). Smallest, surgical; unblocks the honest surge. |
| **5.10 — Narrow as residential access** | 1 | Sizing + canon role; its headroom math needs 5.9's bounded demand. |
| **5.11 — Diverse terminal types** | 4 | Profiles need the cap machinery (5.9) + the access canon (5.10) to mean anything. |
| **5.12 — Aggregation groups** | 3 | The payoff — congestion lives at the shared uplink; needs caps + access + diversity. |

**Why not the alternatives (each rejected with reason):**
- **Fold into slice 6 (era transition):** rejected — slice 6 is the E5 era-FSM/modernization epic;
  these threads are E2.1/E3.1/E3.2 demand+topology work (the slice-5 systems cluster's natural
  completion). Folding muddles the epic mapping and bloats an already-tight slice.
- **Post-fun-gate (slice 8+):** rejected — the slice-7 playtest gate must measure the **honest**
  congestion model ("why is my endpoint dropping packets?" must be a readable statement about the
  network — the fun-test question). Testing the current endpoint-self-congestion noise would
  validate the wrong game.
- **Renumber as slice 6 (shifting era transition to 7):** rejected — destructive renumbering of
  shipped references for zero gain; 5.9–5.12 keeps the story ids monotonic.
- **"Post-5.4" strictly (before 5.5–5.8):** rejected — the threads depend on 5.1 growth + 5.8 QoS
  (merged); 5.4 input parity is orthogonal. Slotting after the slice-5 cluster (post-5.8) satisfies
  the briefing's "post-5.4" intent with the real dependency order.

**Gate ordering:** landing 5B before slice 6/7 means the era-transition story and the playtest
exercise the honest aggregation model from the start, and the deliberate golden re-bless batches at
the 5B boundary instead of interleaving with slice-6/7 churn.

**Sprint-plan note:** `sprint-plan-v2.md`'s slice map gains a 5B row at ratification (included in
this job's PR so the plan and the stories don't contradict).

---

## 6. Deliverables in this job

1. This design spec (lavish-reviewed, in the artifact).
2. Story cards 5.9–5.12 appended to `stories-v2.md` (existing card format).
3. GDD amendment: a new **M6 — Traffic realism** mechanics block (section-additive, after M5,
   before Controls) + a decision-log entry (append-only) — no terminology rewrites, no edits to
   existing GDD text (the coordination constraint: the p1P8 terminology audit serializes behind
   this job's GDD edits; Silas serializes the PRs).
4. `sprint-plan-v2.md` slice-map row (5B).
5. The lavish artifact presenting all of it; the PR opens only after approval.
