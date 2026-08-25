# Briefing — packet-plumber-routing-explorer

**Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` section
"Minion standing orders" FIRST. They apply in full. Highlights: speak minion when
the user chats you in-pane; artifacts stay plain; self-report every ledger
transition (`bin/ledger set <id> <status> "<note>"`); badge out a field-note
shard; never merge; work only in your worktree on branch `<slug>`.

## The job (what to build)

Build an **interactive HTML artifact** that explains and lets the user explore the
**packet-routing model** of Packet Plumber — both how it works *today* in the merged
prototype (PR #17) and the design alternatives the user is weighing. Serve it via
**`lavish`** so the user can annotate it in-browser with their questions, then
**foreground-poll** and iterate. The user has explicitly said *"I have loads of
questions"* — this is an exploratory learning + architecture-decision surface, and
**the user drives the questions via lavish annotations**, not you up front.

### Why
The user is learning the routing sim AND deciding the full-game architecture: keep
the current pre-calculated BFS + parallel-pipe LB + reactive failover, or move to a
router-decision model (per-hop forwarding based on src/dst, with ECMP across
equal-cost paths), or even implement a lite IS-IS / BGP control plane. They need to
*see* the trade-offs interactively before they decide.

### Must cover (build a v1 addressing ALL of these; the user will dig deeper via annotations)

1. **BFS explained, visually + step-by-step.** An animated/walkable diagram of
   `compute_route` (`core/flow.odin`): BFS over the adjacency graph, the `bfs_prev`
   walk-back, insertion-order determinism. Let the user step through a BFS expansion
   on a small topology and see the chosen path appear.

2. **Interactive simulation — "set values, see the path taken."** A small editable
   topology (place terminals / routers / pipes; pick pipe tiers; set junction type
   basic vs smart/LB; set per-class demand). On run, show: which path each packet
   takes, per-pipe load, drops, accrued latency, per-class SLA. This must be
   **faithful to the real prototype** behavior:
   - BFS shortest path (fewest hops), one path per packet, computed at spawn.
   - Parallel pipes between the same node pair: **round-robin** at basic junctions
     (`rr_next`), **capacity-weighted** (highest-tier, RR tiebreak) at smart/LB
     junctions (`pick_pipe`, `lb_weighted`).
   - QoS lane scheduling (Express→Standard→Best, work-conserving gap-fill) is
     bandwidth-on-a-pipe, NOT path selection — show it but keep it distinct from
     routing.
   - Severance reroute (E1): demolished pipe → re-BFS from the packet's current
     node, or drop `.Severance`.
   - Integer-only, deterministic ticks (ODN-10) — note where the sim draws `rng`.

3. **Parallel-pipe load-balancing demo.** Side-by-side: round-robin (basic) vs
   capacity-weighted (smart) across 2–3 parallel pipes. Show how a wide-fiber +
   narrow-copper bundle behaves under each (the GDD §M3 motivation: RR wastes the
   fiber while copper saturates).

4. **ECMP exploration (proposed, not yet implemented).** A toggle that simulates
   **equal-cost multi-path** across *disjoint* equal-cost routes (today BFS takes the
   insertion-first path only). Let the user compare: current single-path vs ECMP
   hash/per-packet split across N equal-cost paths. Show the load-distribution and
   reordering implications. Clearly label this as **proposed / not in the prototype**.

5. **Design-alternative: router-decision model (proposed).** Today the route is
   **pre-calculated at packet spawn** and held until severance. Explore the
   alternative: **routers make a per-hop forwarding decision based on (src, dst)**
   (a forwarding/lookup at each junction), with ECMP at equal-cost branches — i.e.
   packets aren't committed to a full path at spawn; each router picks the next hop.
   Show how this changes behavior (live load-aware forwarding, automatic use of
   redundant paths, no stale routes after topology changes) vs the spawn-time route.

6. **"Implement a simple IS-IS / BGP?" — a reasoned section, not a build.** Survey
   what a *lite* link-state (IS-IS/OSPF-style) or path-vector (BGP-style) control
   plane would mean for this game: what it buys (real route computation, policy,
   convergence), what it costs (complexity, determinism, sim-tick expense), and
   whether the gameplay depth justifies it vs the simpler "BFS + LB + failover"
   core. Ground it in what's actually fun/legible per the GDD pillars (P1 routing
   satisfaction, P2 packet-type trade-offs). Give a recommendation but frame it as a
   decision the user makes.

7. **Performance impact analysis.** Compare the routing strategies on **sim-tick
   cost and determinism**, grounded in the actual model (integer ticks, per-run
   route slab, arrays-only no-map-iteration ODN-10):
   - Pre-calculated BFS at spawn (current): O(V+E) once per packet, route cached.
   - Per-hop router-decision + ECMP: a forwarding lookup per packet per hop — what's
     the per-tick cost at PROTO scale (≤64 nodes, packet pool cap) and at full-game
     scale? Determinism implications (ECMP hash must be seeded — ODN-9/10).
   - Lite IS-IS/BGP: periodic route recomputation + convergence — cost cadence.
   Give concrete-ish numbers/Big-O, not vibes. Flag any strategy that threatens the
   determinism spine (the Odin core's load-bearing invariant).

8. **Failover during spikes.** A scenario player: ramp demand into a **spike**, with
   **redundant links as failovers** (the current model — redundancy is insurance, not
   active splitting). Show: how a single path saturates and drops, how a redundant
   failover path catches severance/saturation, recovery latency, and the no-soft-lock
   guarantee (GDD: "always a way to reroute"). Contrast with how the same spike looks
   under the ECMP / router-decision models (redundancy used *actively* from the
   start). This is the user's "how does that impact during spikes?" question — answer
   it with the sim, not prose alone.

### Quality bar
- **Interactive + easy to understand.** The user is learning; favor clear visuals,
  sliders/inputs, live-updating diagrams, plain-language explanations beside the
  technical detail. Avoid a wall of text.
- **Faithful to the real code.** Every "current behavior" claim must match
  `core/flow.odin` + `core/topology.odin` + the catalogs in `data/`. Cite the
  function/file. Anything proposed (ECMP, router-decision, IS-IS/BGP) is clearly
  labeled **proposed**, not as-if-already-built.
- **Use the `frontend-design` skill's quality bar** for the UI — polished,
  readable, not generic-AI-looking.
- Read the design docs for intent, and flag where the prototype diverges (e.g.
  architecture §6.2 says "shortest-path-by-tier-cost with seeded tie-break", but the
  code is plain BFS-by-hops; E29 "route migration at node boundaries" is described
  but the code keeps routes fixed until severance). Surface these gaps in the
  artifact — they're part of the decision.

## Repo map
- **Repo:** `packet-plumber` · **root:** `/Users/moses/code/packet-plumber` ·
  **base:** `main` · **slug:** `routing-explorer`
- **Routing code (read these):**
  - `core/flow.odin` — `compute_route` (BFS), `pick_pipe` + `rr_next` (parallel-pipe
    LB), `advance` (QoS serve + severance reroute), `Packet` struct (the cached route).
  - `core/topology.odin` — graph, `pipes_between`, `neighbors`, junction LB flags
    (`node_lb_weighted`), port limits, severance on demolish.
  - `core/qos.odin` — lane allocation (bandwidth-on-a-pipe, NOT routing).
- **Catalogs:** `data/packet_types.json`, `data/pipe_tiers.json`,
  `data/node_types.json`, `data/balance.json`, `data/demand.json`.
- **Design docs:** `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`
  (§M2 QoS lanes, §M3 junction LB, §M5 crises/redundancy, the "Redundancy &
  load-balancing" para), and
  `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (§6.2 S2 flow
  sim: routing strategy line, E28 unroutable, E29 route migration).
- **Artifact location:** your choice of a sensible path in the worktree (e.g.
  `tools/routing-explorer/index.html` or `_bmad-output/routing-explorer.html`).
  `lavish` is file-path-keyed — keep the artifact at one stable path for the whole
  session.

## Env / bootstrap
- Worktree bootstrapped by Silas (env files + `node_modules` symlinked if present —
  this is an Odin repo, so `node_modules` likely N/A; the artifact is standalone
  HTML/CSS/JS, no build step required).
- No external API keys needed. The artifact is self-contained (vanilla JS; a tiny
  inline sim is fine — do NOT wire it to the Odin core; reimplement the routing logic
  in JS faithfully for the explainer).

## Verify (your done-bar, before you badge out)
- [ ] Artifact served via `lavish`; session open at the artifact path.
- [ ] All 8 topics above are present and interactive.
- [ ] Every "current behavior" element matches the real code (you've re-read the
      cited functions); proposed alternatives are labeled.
- [ ] Performance section gives concrete cost/determinism reasoning, not vibes.
- [ ] Foreground-poll running; you've applied at least one round of the user's
      annotations (or are actively polling when you hand back).
- [ ] `herdr notification show "packet-plumber-routing-explorer" --body "<status>"`
      fired (this is a **no-PR job** — the notification is the completion signal; the
      watchers will NOT catch it).

## Model policy
- **Model: `zai-coding-cn/glm-5.2`** (capable tier). This is design + non-trivial
  interactive-coding work that would normally run on the frontier tier (kimi k3),
  but **kimi is down this cycle** (quota 403) and the user has approved glm-5.2 for
  ongoing work. glm-5.2 is proven capable (the odin r2 review ran a full 8-pane round
  to APPROVED on it). If Gru redirects you to kimi mid-job (quota refreshed), switch
  via `/model` — context is preserved.
- **Mega-minions** (if you spawn any — optional, e.g. to parallelize a couple of the
  interactive modules): also `zai-coding-cn/glm-5.2`, max 10 concurrent, badge them
  all out before you finish.

## Skills policy
- **`lavish`** (REQUIRED) — the artifact is the deliverable; serve it in-browser and
  foreground-poll for the user's annotations. Open the lavish playbooks first:
  `npx -y lavish-axi playbook <id>`. End YOUR session with `npx -y lavish-axi end
  <path>`; NEVER `lavish-axi stop`.
- **`frontend-design`** — build the interactive UI to a polished, easy-to-understand
  bar (diagrams, value-setters, live path visualization). Avoid generic AI aesthetics.
- **`bmad-quick-dev`** — the implementation workflow for building the artifact.
- **Clarify override:** DO NOT halt for step-01 clarify questions. The user is
  *asking* the questions, via lavish annotations — build a comprehensive v1 covering
  all 8 topics, serve it, and let the annotations drive iteration. Only halt for a
  genuine blocker (missing access, a contradiction you can't resolve).
- **Optional:** if you want a sanity-check on the performance/design-alternative
  reasoning before serving, spawn one `bmad-review-adversarial-general` mega-minion
  on that section (glm-5.2). Not required.

## No-PR note
This is an exploration artifact. **Do not open a PR** unless Gru tells you to. The
artifact stays live via the lavish session while iterating. When the exploration
converges, Gru decides whether to commit it (to a branch / `docs` / `tools`). Your
finish signal is the `herdr notification show` call above + a self-report `ledger set
… working "<serving lavish, polling for annotations>"` while you poll.

## Dispatch parameters
- **repo:** packet-plumber
- **repo_root:** /Users/moses/code/packet-plumber
- **slug:** routing-explorer
- **base:** main
- **model:** zai-coding-cn/glm-5.2
- **pr_review:** 0  (no-PR exploration artifact; Perkins OFF)
- **github_issue:** (none)
