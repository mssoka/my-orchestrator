# Problem Solving Session: Bandwidth-Aware Routing Cost in Packet-Plumber

**Date:** 2026-08-13
**Problem Solver:** Moses
**Problem Category:** technical — routing-algorithm design under locked-canon + golden-harness determinism constraints

---

## 🎯 PROBLEM DEFINITION

### Initial Problem Statement

Bandwidth is not taken into account in the routing cost. PP's routing picks paths by hop count only — a 5-unit basic pipe and a 40-unit fast pipe are "equal cost" — so fat capacity never attracts traffic and skinny paths can jam while fat paths idle.

### Refined Problem Statement

The locked routing model (canon #18, routing ruling lavish 2026-08-10; `core/routing.odin`, architecture §6.2) selects next hops by **hop-count BFS only**: pipe tier / `capacity_units` (5/15/40) plays NO role in path selection. The gap between current and desired state: capacity-blind routing strands throughput on low-capacity paths while high-capacity paths sit underused. The desired state: bandwidth participates in path cost — while preserving (i) byte-identical T1 replay goldens (`expect hash stable`), (ii) the 4-rule spine (or a deliberate, user-ruled canon amendment), (iii) integer-only, array-stable computation (ODN-9/10).

### Problem Context

- **Current model:** one BFS per destination → `dist[*]` = hop count; equal-cost set = neighbors with `dist[v] == dist[u] - 1`; the pick is a **pure hash** `splitmix64(src, dst, class, pkt_id) mod N` (flow affinity — never a sim-rng draw).
- **4-rule spine (canon #18):** (1) table rebuilt ONLY on topology change, synchronously in tick; (2) ECMP tie-break = pure hash of packet identity; (3) derived table is NOT serialized into the T1 state hash (Topology is; hashing derived state would bind replay to table-build algorithm); (4) integer-only, array-only (ODN-10).
- **Capacity data:** `pipe_tiers.json` — basic 5 / standard 15 / fast 40 `capacity_units`; packets consume `bandwidth_demand × packet_bandwidth` units per edge (transit ticks = ceil(demand×30 / capacity)).
- **The tension:** dynamic cost (live utilization) changes every tick → collides with rule 1 (rebuild only on topology change) and would drag derived state into the T1 hash. Static cost (tier capacity) is a pure function of Topology → spine intact.
- **Canon process:** the routing model is a LOCKED ruling — any change to cost semantics is a canon amendment (user ruling + docs update), not a silent refactor.

### Success Criteria

1. **User ruling (2026-08-13):** cost = STATIC pipe capacity (the tier) — never dynamic utilization. Intent = traffic engineering: "flows prefer fat pipes." Congestion avoidance stays the PLAYER's job (QoS lanes + pipe engineering) — that's the game.
2. **User ruling (2026-08-13):** equal-cost semantics by capacity — `j1→(5)j2` + `j1→(5)j3` must ECMP; `j1→(5)j2` + `j1→(10)j3` must use the 10 (not equal cost). Players must be able to READ this from the map (tier is visible).
3. Replay determinism holds: same `(seed, action_log)` → byte-identical T1; `expect hash stable` still green.
4. The 4-rule spine is respected, OR canon #18 is amended by explicit user ruling with architecture/GDD docs updated.
5. Golden harness green; new regression pins cover the capacity-cost cases at the lowest layer.
6. Core purity intact: integer-only, no map iteration, no per-packet rebuilds in the hot path.

---

## 🔍 DIAGNOSIS AND ROOT CAUSE ANALYSIS

### Problem Boundaries (Is/Is Not)

- **IS:** next-hop / path selection cost at a junction — `routing_rebuild`'s BFS treats every live pipe as weight 1 (hop count), so capacity never steers traffic. Manifests in `flow.odin`'s forward pass (pick among the equal-cost set).
- **IS NOT:** the ECMP pick itself — the pure hash `splitmix64(src,dst,class,pkt_id) mod N` stays untouched. **IS NOT** dynamic congestion — user-ruled out (player's job). **IS NOT** QoS lane allocation (orthogonal canon — "Orthogonal to routing", routing ruling). **IS NOT** draw cost (money) or per-edge transit speed (transit already charges capacity: `ceil(30×demand / capacity_units)` — only path CHOICE ignores it).
- **Occurs WHEN:** any topology with parallel/multi-path alternatives of differing tiers (a mixed-tier diamond). **Does NOT occur:** single-path graphs — `count == 1`, the pick is moot.
- **WHO is affected:** the player — skinny paths jam while fat parallels idle, and routing depth is missing (tier choice should matter); the golden harness — old goldens encode hop-count outcomes (ecmp.dem alternation).

### Root Cause Analysis

**Five Whys:**

1. Why don't flows prefer fat pipes? → The routing table's cost model never includes capacity.
2. Why not? → `routing_rebuild` is a unit-weight BFS — every live pipe contributes exactly 1 hop.
3. Why unit weights? → Canon #18 specced hop-count shortest path at 2.2, matching the prototype's BFS-per-source model.
4. Why was hop count specced? → Determinism-simplicity: unit weights are trivially integer-stable (ODN-10) and replay-safe; the golden harness pinned hop-count outcomes.
5. Root cause: **the cost model was specced for determinism, not for capacity-awareness.** The capacity data existed all along (`pipe_tiers.json`, ODN-5) — it was simply never wired into the SPF weight. Not a bug; an underspecified design dimension of canon #18 surfacing as gameplay shallowness.

### Contributing Factors

- ODN-10 (integer-only) made unit-weight BFS the easy, safe choice at 2.2 — a float Dijkstra would have been rejected outright.
- `pipe_tiers.json` carries `capacity_units` but `routing.odin` never reads it — the ODN-5 single-source existed; the consumer was never built.
- `ecmp.dem` + `ecmp_test.odin` pin hop-count behavior (2-hop/1-hop diamond, hash alternation) — goldens encode the old cost model, so any cost change needs deliberate re-bless review.
- The routing ruling explicitly separated QoS from routing ("Orthogonal to routing") — lane allocation was the designed bandwidth lever; path cost was left un-designed.

### System Dynamics

- **The table is derived from Topology** (4-rule spine rule 3) — so STATIC weights keep every determinism invariant intact: rebuild-on-topology-change still correct, T1 hash untouched (Topology serialization already includes tiers), pick still pure identity hash.
- **Player-facing loop:** tier becomes a routing-relevant signal the player can read (visible pipe tiers) — fat-pipe preference becomes predictable, learnable, engineerable. Capacity-blindness is what made routing shallow.
- **Golden-harness ripple:** scenarios with mixed-tier multi-path topologies WILL change paths (and thus delivered-tick/drop outcomes) → those goldens need deliberate review + re-bless; the T1 hash CODE doesn't change, the VALUES do.

{{system_dynamics}}

---

## 📊 ANALYSIS

### Force Field Analysis

**Driving Forces (Supporting Solution):**

- 🟢 **User ruling already in hand** (2026-08-13): static capacity cost, "flows prefer fat pipes" — the direction is locked, momentum exists.
- 🟢 **The SPF structure already exists** — `routing_rebuild`'s BFS is Dijkstra with unit weights; the upgrade touches ONE function + tests, not the architecture.
- 🟢 **Capacity data already exists** — `pipe_tiers.json` (ODN-5 single-source); only the consumer is missing.
- 🟢 **Static weights preserve the entire determinism spine** — table stays a pure function of Topology → T1 hash untouched, replay byte-identical.
- 🟢 **Gameplay depth gain** — routing becomes a readable, engineerable player decision (visible tiers steer flow).
- 🟢 **Canon has an amendment path** — the routing ruling is amendable by explicit user ruling + docs update (the user IS the ruling body here).

**Restraining Forces (Blocking Solution):**

- 🔴 **Canon #18 is LOCKED** — cost-semantics change requires deliberate docs amendment (architecture §6.2, GDD routing sections) in the SAME job, not a silent refactor.
- 🔴 **Goldens encode hop-count outcomes** — `ecmp.dem`, `ecmp_test.odin`, and any mixed-tier T1 scenario change behavior → deliberate re-bless review (goldens are reviewed like code).
- 🔴 **Discipline traps** — float weights, map iteration, or dynamic state reads would violate ODN-9/10; careless implementation is the main technical risk.
- 🔴 **Sequencing vs in-flight work** — 4.2-surge-crisis (#36, pane p14C) is mid-flight on the same repo touching core/flow; a core/routing change needs cross-job coordination (flag → Silas routes; never act across the boundary).
- 🔴 **Player-communication burden** — the rule must be readable from the map (tier visuals exist; the *routing signal* meaning must be documented in GDD/look-book).

### Constraint Identification

**REAL constraints (non-negotiable):**

1. **Static weights only** (user ruling) — cost is a pure function of Topology, never of run state.
2. **Integer-only** (ODN-10) — no floats in cost math; exact division via LCM-REF or explicit integer cost fields.
3. **Array-only iteration** (ODN-10) — the Dijkstra priority queue is array-backed with insertion-order tie-breaks; no map iteration.
4. **Rebuild only on topology change** (spine rule 1) — automatic once weights are static.
5. **Pick stays the pure identity hash** (spine rule 2) — `ecmp_pick` untouched.
6. **Table stays derived, not T1-hashed** (spine rule 3) — automatic.
7. **ODN-5 single-source** — costs come from data catalogs, never hardcoded in `routing.odin`.
8. **Harness green + deliberate re-bless** — mixed-tier scenarios re-blessed and reviewed like code.
9. **Canon documentation** — architecture §6.2 + GDD routing text updated in the same job as the ruling.
10. **Perf at tick scale** — rebuild stays cheap (N small; same order as the current N-BFS).
11. **FUN-FACTOR requirements (user, 2026-08-13):** (a) **readability** — the player must be able to predict routing by looking at the map; (b) **upgrade-relief loop** — tier upgrades must produce visible, satisfying flow shifts; (c) **teachability** — the rule fits one line ("packets take the fattest route; ties split"); (d) **no hidden traps** — an upgrade must never invisibly backfire (thundering herd onto the fat pipe); (e) **progressive divergence** — early game ≈ hop-count intuition; the divergence arrives with the tier ladder, not at minute zero.

**ASSUMED constraints (bustable):**

- ❌ "Dijkstra needs a fancy priority queue" — at this graph size a simple array scan is fine; O(N²) is irrelevant.
- ❌ "Equal-cost means same tier" — FALSE: different pipes tie on end-to-end sum (worked example: 3+8 vs 8+3).
- ❌ "REF must be LCM-derived in code" — optional: an explicit per-tier cost field in `pipe_tiers.json` removes the REF cascade entirely.
- ❌ "Hop count must matter" — open knob: pure inverse-capacity vs a per-hop penalty.

**Primary constraint (TOC):** NOT technical — the change is small. The binding constraint is **canon-process discipline + golden re-bless review + sequencing against in-flight #36**.

### Key Insights

1. **This is a weight upgrade inside an existing SPF, not a new routing architecture** — risk surface = `routing_rebuild` + tests + goldens.
2. **Determinism survives BY CONSTRUCTION** — static weights make spine rules 1/2/3 hold automatically; only canon #18's cost SEMANTICS change (amendment, user-ruled here).
3. **The game rule becomes one line the player can read:** "packets take the fattest route; ties split by hash."
4. **The real design freedom is the cost function shape:** pure inverse-capacity (LCM-REF) vs explicit designer costs vs capacity + per-hop penalty. That's the Step 5 generation space.
5. **Cross-job impact is real:** #36 touches core/flow in flight — sequence the routing change behind it (or serialize-hold), flag to Silas; never edit across the job boundary.
6. **FUN IS A FIRST-CLASS CONSTRAINT (user, 2026-08-13).** The cost model generates the game's core loop: predict → build → watch flows shift → adapt. Readability beats mathematical purity; the upgrade-relief loop is the payoff; hidden traps (a fat pipe attracting ALL traffic and jamming — the thundering herd) would make upgrades feel like punishment. The 4.1 strain telegraph + forecast panel are the natural surfaces for making the magnet effect legible.

---

## 💡 SOLUTION GENERATION

### Methods Used

1. **Morphological Analysis** — decompose the design into independent parameters (cost function shape × where cost lives × player-facing readability × tie-split behavior × teaching curve) and explore combinations.
2. **Assumption Busting** — challenge "equal-cost means same tier", "REF must be LCM", "hop count must matter", "Dijkstra needs a fancy queue".
3. **Lateral Thinking (provocations)** — "what if capacity were GRAVITY?", "what if the player draws the routes?", "what if packets negotiate?" — to surface wild alternatives and then kill them cheaply.
4. **Failure Mode Analysis (fun-lens)** — enumerate how each option could make the game LESS fun (thundering herd, opacity, randomness-feeling splits) and engineer preventions.

### Generated Solutions

**P1 — Cost function shape (the core knob):**

| # | Option | Costs (5/15/40) | Pros | Cons |
|---|---|---|---|---|
| S1 | Pure inverse-capacity, LCM-REF | 24 / 8 / 3 | Mathematically exact inverse proportionality; "capacity × cost = 120" is elegant | Numbers feel arbitrary to a player (24? 8? 3?); REF cascade on new tiers |
| S2 | Explicit designer costs in `pipe_tiers.json` | e.g. 24/8/3 OR a tuned ladder like 20/10/5, 100/30/10 | Design freedom; readability-tunable (round numbers); NO REF cascade; ODN-5 clean | Designer must choose well — the ladder IS the game balance |
| S3 | Inverse-capacity + per-hop penalty (cost = REF/cap + H) | 24+1 / 8+1 / 3+1 | Hop count still matters — shorter fat paths beat longer fat paths; ties on sum keep ECMP | Two knobs to tune and explain; slightly less pure |
| S4 | Tier-rank step costs (ordinal) | 3 / 2 / 1 (or 1/2/3) | Simplest to read; no magnitude math | Treats 5→15 same as 15→40 — the 8× fatness of fast is invisible |

**P2 — Where the cost lives:** explicit `cost` field per tier in `pipe_tiers.json` (ODN-5, recommended with S2) vs computed `REF ÷ capacity` in code (needed for S1).

**P3 — Player-facing readability (the fun gate):**

| # | Option | Note |
|---|---|---|
| R1 | Existing tier visuals only | Minimum; risky for the cognitive-load concern |
| R2 | **Flow preview while drawing** — the ghost shows which path packets will take before the pipe commits | The `docs/routing-explorer.html` is already a prototype of this! |
| R3 | Post-draw route glow — the current winning path lights up | Cheap, satisfying feedback for the upgrade-relief loop |
| R4 | **Forecast-panel integration** — the 4.1 forecast predicts the flow shift an upgrade will cause (the magnet effect made legible) | Turns the thundering-herd trap into a readable prediction |

**P4 — Tie-split behavior:** keep the LOCKED pure hash (T1, evenly spreads ties) + optional visual indicator that both paths are equal-cost (T2, clarity-only, no behavior change).

**P5 — Teaching curve:** one-line rule on the map/help ("packets take the fattest route; equal cost splits"); early-game topologies where fat ≈ short; divergence introduced with the tier ladder.

### Creative Alternatives

- **W1 — Capacity as gravity:** pipes emit an attraction field; packets drift toward fat pipes. (Equivalent to SPF mathematically, but visualizable as a field — rejected: same behavior, new complexity.)
- **W2 — Per-class routing preferences:** gaming prefers latency, streaming prefers volume — per-class cost vectors. (Compelling full-game idea; SCOPE-GUARDED OUT — interacts with SLA/era content, not this change.)
- **W3 — Player-drawn route policy per router:** the player pins next-hops manually. (Rejected — management-heavy, Factorio smell, fights the draw-and-react core [FORGE #2].)
- **W4 — Continuous-flow model:** packets as water streams, capacity = pipe width. (Rejected — a full sim rewrite; the packet model is the game.)
- **W5 — Bandwidth auctions:** packets bid for capacity. (Rejected — over-engineered; QoS lanes already cover priority [FORGE #4].)

---

## ⚖️ SOLUTION EVALUATION

### Evaluation Criteria

Weighted criteria — fun is a first-class gate (user ruling 2026-08-13):

| # | Criterion | Weight | Why |
|---|---|---|---|
| C1 | **Fun: readability** (player predicts routing by looking) | 25% | user ruling — "players need to be aware"; the fun gate |
| C2 | **Determinism compliance** (spine rules, ODN-9/10, goldens) | 20% | non-negotiable |
| C3 | **Fun: upgrade-relief loop** (satisfying flow shifts, no hidden traps) | 15% | core-loop payoff |
| C4 | Implementation cost/risk | 10% | target: one function + data + tests |
| C5 | Canon surface (docs amendment burden) | 10% | #18 amendment size |
| C6 | Balance-tunability (data-driven PDCA) | 10% | playtest iteration speed |
| C7 | Robustness (new tiers, overflow, cascades) | 10% | era progression adds tiers |

### Solution Analysis

**Decision Matrix (scores 1-5, weighted):**

| Criterion (weight) | S1 LCM-REF | S2 designer costs | S3 +hop penalty | S4 ordinal ranks |
|---|---|---|---|---|
| C1 readability (25%) | 2 — 24/8/3 ugly | **5** — 20/10/5 sums in-head | 3 — two knobs | 4 — simplest |
| C2 determinism (20%) | 5 | 5 | 5 | 5 |
| C3 upgrade loop (15%) | 4 — exact inverse | 4 — near-inverse | 4 | 2 — magnitude invisible |
| C4 impl cost (10%) | 4 | **5** — data field + read | 4 | 5 |
| C5 canon surface (10%) | 3 | 3 | 3 | 3 |
| C6 tunability (10%) | 2 — REF locks ladder | **5** — per-tier dial | 3 | 3 — ordinal only |
| C7 robustness (10%) | 3 — REF cascade | **5** — no REF at all | 3 | 5 |
| **Weighted total** | **3.30** | **4.65** 🏆 | 3.65 | 3.90 |

### Recommended Solution

**S2 — explicit per-tier integer `cost` in `pipe_tiers.json`**, initial ladder **20/10/5** (halving pattern, near-inverse, player-summable) — plus the readability package:

- **R2 flow preview while drawing** (ghost shows the path packets will take; `docs/routing-explorer.html` is the prototype) — **ENHANCED (user, 2026-08-13): R2a optional live cost-sum assist with graduation tiers** — full assist (live sum + winning-path glow, DEFAULT for beginners) → partial (glow only) → off (pros); a gentle post-N-draws graduation nudge, never forced. Converts readability from mental ARITHMETIC to PERCEPTION; the toggle is the mastery progression; answer-reveal risk (follow-the-glow triviality) mitigated by the tiered toggle + showing ONE number (best-path total or delta), never a candidate spreadsheet.
- **R3 post-draw route glow** (the winning path lights up — the upgrade-relief payoff),
- **R4 forecast-panel flow-shift prediction** (4.1 defuses the thundering-herd trap),
- **T2 equal-cost visual cue** (both tied paths marked; the pure hash T1 stays LOCKED).

### Rationale

- **Determinism is IDENTICAL to S1** — static integers from JSON are a pure function of Topology; spine rules 1/2/3 hold by construction. The sim cannot tell the difference between S1's and S2's integers.
- **The only thing S1 has over S2 is exact inverse proportionality — invisible to players** (costs are compared, never felt) and recoverable any time by setting the JSON to 24/8/3 with zero code change.
- **S4's simplicity is its only argument** — and it throws away fast's 8× fatness (the upgrade payoff the loop needs).
- **Confidence:** high on determinism + implementation; **RAISED from MEDIUM to HIGH on fun-readability** (user ruling 2026-08-13): the live cost-sum assist converts the "players sum 2-3 numbers" assumption into an engineered perception feature — perception not computation; the remaining fun risk shifts to the answer-reveal trap, mitigated by the graduation toggle + single-number display. The playtest gate still arbitrates S2 vs S4 ladder values.
- **Concern carried:** thundering-herd — a fat pipe magnetizing all traffic; mitigated by R4 + the existing 4.1 telegraph; watch in playtest.

---

## 🚀 IMPLEMENTATION PLAN

### Implementation Approach

**Phased rollout under PDCA** — the sim change first (smallest verifiable slice), review, then the readability package, then playtest arbitration:

- **PLAN** = this session's artifact (`_bmad-output/problem-solution-2026-08-13.md`) — the canon source for the ruling.
- **DO (Job A)** — the core routing-cost change: data field + Dijkstra + tests + mixed-tier demo + canon docs.
- **CHECK** — Perkins review (pr_review=1) + harness green + determinism re-step + deliberate golden re-bless review.
- **DO (Jobs B ∥ C — user ruling 2026-08-13: PARALLEL after A merges)** — Job B: readability package (app layer): R2a assist tiers + R3 glow + T2 tie cue. Job C: R4 forecast flow-shift prediction (extends the 4.1 forecast). **Shape locked: A → B ∥ C.** B and C both consume A's cost model (acceptance validity — built against hop-count routing they'd preview wrong paths); they touch disjoint layers (B: `app/render`+`app/ui`; C: forecast + predictive helper) — Silas verifies file-disjointness at dispatch; the two PRs merge sequentially, ready-first.
- **ACT** — playtest gate (future milestone): A/B the ladder values (S2 vs S4 feel) and the assist-graduation tuning.

### Action Steps

**Job A — core routing cost (canon amendment job):**

1. **Canon ruling write-up** — from this artifact: cost = static tier capacity; semantics "flows prefer the fattest route, ties split by hash"; initial ladder 20/10/5; fun constraints (readability, upgrade-relief, no hidden traps).
2. **Data (ODN-5)** — add `cost` field to `pipe_tiers.json` (20/10/5).
3. **Core** — `routing_rebuild`: BFS → Dijkstra over integer pipe costs (array-backed cheapest-first with insertion-order tie-breaks — ODN-10, no map iteration); equal-cost condition becomes `dist[v] + cost(pipe) == dist[u]`.
4. **Keep locked** — `ecmp_pick` pure hash untouched; rebuild-only-on-topology-change (static weights ⇒ automatic); table stays derived (NOT in T1 hash).
5. **Core tests (`@(test)`)** — (a) mixed-tier diamond picks the fat path as a unique next hop; (b) different-tier equal-sum tie → ECMP set of 2 (the 3+8 vs 8+3 case); (c) re-step determinism; (d) cost ladder read from data.
6. **Demo + goldens** — new `ecmp_cost.dem` (mixed-tier diamond, captures pinning the fat-path preference + a true tie); NEW golden files only — existing demos are all standard-tier, so unit-weight paths are preserved and existing goldens should stay green (VERIFY; if any existing golden shifts, deliberate re-bless review).
7. **Canon docs in the same PR** — architecture §6.2 cost model + GDD routing text (one-line rule + assist-feature note). Lavish exemption: this is a canon touch-up documenting a ruling the user made LIVE in this session — brief explicitly ("lavish not needed, PR directly").
8. **Review** — `pr_review: true` (Perkins opt-in; determinism-critical, canon-surface).

**Job B — readability package (app layer, after A merges):**

- R2a live cost-sum assist with graduation tiers (full → glow-only → off; DEFAULT full for beginners; graduation nudge after N draws, N data-driven, never forced).
- R3 post-draw route glow; T2 equal-cost visual cue (both tied paths marked).
- Reference: `docs/routing-explorer.html` (the existing preview prototype).
- STRICT: view-only — reads the table, never feeds state (ODN-12); determinism untouched by construction.

**Job C (candidate split)** — R4 forecast flow-shift prediction ("this upgrade attracts everything") — extends the merged 4.1 forecast panel; defuses the thundering-herd trap.

### Timeline

**Milestones (no time estimates — sequencing gates only):**

- **M1** Job A PR opens (pr_review=1).
- **M2** Perkins approves → merge.
- **M3** Jobs B and C open IN PARALLEL (both from A's merged base; file-disjointness verified by Silas).
- **M4** B and C merge sequentially (ready-first).
- **M5** Playtest gate (future) — arbitrates ladder + assist tuning (PDCA Act).

**Sequencing constraint:** #36 (4.2-surge-crisis) is in flight touching core/flow + goldens. Job A is a **parallel-safe candidate** — `routing.odin` is untouched by #36 and goldens are NEW files — BUT Silas verifies golden-file overlap at dispatch; any overlap → serialize-hold behind #36's merge (cross-job flag, never act across the boundary).

### Resource Requirements

- Minion worktree per job (packet-plumber, base `develop`); Job A/B/C briefings reference this artifact as the canon source.
- Perkins rounds on `deepseek/deepseek-v4-pro` (model policy); minions on flash.
- `docs/routing-explorer.html` as the R2a prototype reference.
- Skills: `bmad-quick-dev` for implementation; review via Perkins (pr_review flag).

### Responsible Parties

- **Gru** — briefings (this artifact → Job A/B/C), canon ruling record.
- **Silas** — dispatch, sequencing verification vs #36, close-outs, golden-overlap check.
- **Minions** — implementation per job.
- **Perkins** — adversarial review rounds (v4-pro).
- **Moses** — playtest-gate arbitration (ladder + assist tuning).

---

## 📈 MONITORING AND VALIDATION

### Success Metrics

**Sim-correctness metrics (automated, PR-time):**

| # | Metric | Target | How measured | Frequency |
|---|---|---|---|---|
| M1 | Re-step determinism | 100% byte-identical T1 | pinned `(seed, log)` ×2 unit test + harness tier-1 | every CI run |
| M2 | Harness green | all tiers green | `harness run` | before any merge |
| M3 | New pins hold cross-target | 100% | `ecmp_cost.dem` + core fat-path/tie/ladder `@(test)`s on the CI matrix (OS × arch) | every PR |
| M4 | Canon-compliance review | 0 blockers | Perkins rounds (pr_review=1) | at review |
| M5 | Golden discipline | zero UNREVIEWED golden changes | diff-bundle-first doctrine — read before re-bless | every bless |

**Gameplay-success metrics (playtest gate, future milestone):**

| # | Metric | Target | Evidence |
|---|---|---|---|
| M6 | Readability (fun gate) | near-100% correct path prediction with assist ON; assist-off baseline for comparison | scripted mixed-tier prediction quiz |
| M7 | Upgrade-relief loop | players observe flow shifting to the fat pipe; no "upgrade made it worse" confusion | observed-play sessions + R4 forecast legibility |
| M8 | No hidden traps | zero unexplained-routing reports — every surprise traceable to the cost ladder + tie rule | playtest debriefs |
| M9 | Learning arc | assist-off adoption GROWS across sessions (graduation without force) | assist-mode telemetry (opt-in) |

### Validation Plan

- **Layer 0 — PR-time:** core `@(test)` + determinism re-step + harness T1/T2 on CI. Evidence the math is integer-stable.
- **Layer 1 — review:** Perkins reads the diff + runs headless reproductions (35-run style) — adversarial validation of the canon change.
- **Layer 2 — demo-level:** `ecmp_cost.dem` captures pin both states (fat-path unique hop mid-flight + true 3+8 vs 8+3 tie split) — human-readable, replayable evidence.
- **Layer 3 — playtest gate:** scripted A/B (S2 ladder vs S4 feel; assist on/off readability; thundering-herd scenario with R4 on/off) — the PDCA Act phase.
- **Cross-target:** the existing CI matrix proves byte-replay across OS × arch; the pinned seed vectors ARE the conformance test.

### Risk Mitigation

| Risk | Prevention | Detection | Plan B |
|---|---|---|---|
| Dijkstra leaks nondeterminism (map iter, float, rng tie-break) | ODN-10 review lens + pinned tests + Perkins | CI determinism suite | revert to unit weights — the change is one function; git history is the fallback |
| Existing goldens shift more than expected (a demo mixes tiers unknowingly) | diff-bundle-first: read before re-bless | every shift explained in the PR description | unexplained diff → STOP, investigate before blessing |
| Thundering herd makes upgrades feel punishing | R4 forecast + 4.1 telegraph surface it; ladder spacing softens the magnet | playtest frustration reports | tune the ladder (JSON-only change) or strengthen R4 |
| Answer-reveal trivializes routing | graduation nudge + tiered toggle | assist-off adoption rate | reconsider default/gating if adoption stalls at ~0 |
| Sequencing conflict with #36 (golden overlap) | Silas verifies overlap at dispatch; serialize-hold if needed | #36 golden changes | hold Job A behind #36's merge |
| Canon docs drift from implementation | docs in the SAME PR; Perkins lens checks doc/code agreement | review | fix docs, re-review |

### Adjustment Triggers

1. **Any determinism-test failure → block merge.** Non-negotiable.
2. **Unexplained golden diff → stop + investigate** before any re-bless.
3. **Playtest readability below target → tune the ladder numbers (JSON-only)** before touching design.
4. **Thundering-herd frustration in playtest → strengthen R4/telegraph; consider a softer ladder.**
5. **Assist-off adoption ≈ 0 across sessions → rethink the default assist state or the gating.**
6. **Perkins blockers on the canon job → normal rework loop** (fix → fix-audit → re-approve).

---

## 📝 LESSONS LEARNED

### Key Learnings

1. **In a determinism-locked system, classify the change by what its new input depends on.** Static (Topology-derived) inputs are FREE — the entire determinism spine survives by construction. Dynamic (Run_State-derived) inputs are EXPENSIVE — they fight every spine rule. Classify FIRST, design second.
2. **Readability beats mathematical purity in games** — but data-driven design (the JSON cost field) means purity is reclaimable at zero code cost. The debate becomes a data debate.
3. **Fun belongs in the evaluation matrix with real weights** (readability carried 25% and flipped the winner from S1 to S2) — never as afterthought prose.
4. **The "big scary change" was a weight upgrade inside an existing SPF** — the BFS was already Dijkstra with unit costs. Before designing a solution, check whether the current structure already IS the target structure.
5. **Math teach-ins belong inside the session.** The LCM/Dijkstra explanations happened where they were needed (13⅓ story turned "design freedom" from jargon into a concrete trade-off), and the user learned the math he'll need to review the PR.
6. **The user's assist-toggle idea converted the riskiest assumption into an engineered feature** — perception, not computation. The best solution of the session came from the user, mid-checkpoint. Facilitation's job is to make room for that.

### What Worked

- Diagnosis before solutions — the Is/Is-Not pass surfaced the key insight (transit already charges capacity; only path CHOICE ignores it) that sharpened everything after.
- Treating the locked canon as a constraint to engineer around, not a wall — static weights made spine rules 1/2/3 hold automatically.
- The two scoping questions (static vs dynamic; traffic engineering vs congestion avoidance) collapsed the solution space instantly.
- Keeping the artifact current at every checkpoint — it became the canon source and the briefing seed.
- Bundling tightly-coupled steps (2-3, fun+5) to preserve the user's momentum while honoring the checkpoint cadence.

### What to Avoid

- Don't start a session with solution-shaped framing — the urge to propose designs in the opening message was real; diagnosis discipline caught it.
- Don't leave cascade-type concerns (the REF/tier interaction) to be discovered in a Q&A detour — surface them proactively in the constraints step.
- Don't let fun-factor criteria enter at solution generation — they belong in the evaluation criteria from Step 1.
- Don't discover cross-job sequencing (#36/#606) at dispatch time — it belongs in the implementation plan.

---

_Generated using BMAD Creative Intelligence Suite - Problem Solving Workflow_
