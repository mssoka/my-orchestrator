# Packet Plumber — Routing Canon Amendment

**Review gate before the PR.** The `routing-explorer` lavish session converged — you LOCKED the full-game routing model. This page is the doc amendment that captures it. **Annotate anything that mis-states your decision;** when it's right, Send & End and I open the PR.

> **Source of truth for the rationale:** `docs/routing-explorer.html` (your 8-section / 7-annotation-round exploration, preserved in-repo by this same PR). Every "why" below is mined from it.

---

## 1. The locked model (5 decisions, written faithfully)

| # | Decision | One-liner |
|---|---|---|
| 1 | **Per-hop forwarding at each junction — INTERNAL** | Players draw pipes; **no router-config CLI**. Each junction forwards per-packet. *Supersedes the spawn-time pre-calculated BFS route.* |
| 2 | **ECMP across equal-cost paths** | Seeded hash `splitmix64(src, dst, class, pkt_id) mod N` over the equal-cost next-hop set. Deterministic per packet (flow affinity). |
| 3 | **Parallel pipes BUNDLE into one pooled-capacity link** | Capacity = **sum** of bundled pipes. **DELETES round-robin / capacity-weighted LB entirely.** Redundancy = **active capacity** (no idle failover). |
| 4 | **Determinism HOLDS (ODN-9/10, 4-rule)** | Forwarding table rebuilt only on topology-change/sync; ECMP = pure hash (no map iteration, no rng draw in hot path); bundled cap = static sum at table-build. *As deterministic as the BFS it replaces.* |
| 5 | **Juice** | "Pop bigger" merge animation when pipes bundle + a Suno SFX thunk, re-fired each time a pipe joins a bundle. |

---

## 2. Decisions & rationale (the WHY — also goes in the PR)

- **Per-hop + ECMP over BFS** — dissolves the entire class of "stale route after topology change" bugs (route migration becomes automatic) and makes redundancy structural rather than a special-case reroute. ECMP is real-router behavior; kept byte-replay-identical via a pure per-packet hash (no sim-rng draw → same packet always takes the same path).
- **Bundles over LB** — under the old model a 2nd parallel pipe was *insurance* (idle until severance), so it felt like wasted ports. Bundling makes redundancy **active capacity the moment you build it**. It also deletes an entire mechanic (basic-vs-smart, RR-vs-weighted) → less cognitive load, and concentrates the player's budget on **QoS** (the game's real differentiator, FORGE #4), not LB.
- **What bundles cost (accepted):** erases the "basic-RR wastes the fiber" teaching moment + the smart-router upgrade path (M4) + a player skill lever (LB-mode choice). Merging ≈ optimal LB, so it deletes the failure mode (copper saturating while fiber idles) that created puzzle tension. Your call — recorded, not re-litigated.
- **Determinism** — the explorer's own 4-rule checklist proves per-hop+ECMP is as deterministic as BFS-by-insertion-order; pinned into ODN-9/10.
- **NOT built here.** Tier-cost routing (the old "shortest-path-by-tier-cost" intent) and clean-span degradation stay **full-game TODOs** — flagged, not solved. A future full-game build job ports the code; **this is docs-only.**

---

## 3. Prototype vs full-game framing

The merged prototype (**PR #17**) implements **BFS + parallel-pipe LB (round-robin / greedy-capacity) + severance-only reroute** in `core/flow.odin` / `core/topology.odin`. The docs now record this as **`[PROTO]`** and the per-hop+ECMP+bundles model as the **`[FULL]`** target — nothing pretends the prototype already does it.

| | `[PROTO]` (PR #17, today) | `[FULL]` (locked target) |
|---|---|---|
| Route | one-shot BFS cached on packet at spawn | per-hop forwarding at each junction |
| Parallel pipes | round-robin (basic) / greedy-capacity (smart) | **bundle** → one pooled-capacity link (cap = sum) |
| Equal-cost paths | first insertion-order wins | **ECMP** hash `splitmix64(...) mod N` |
| Route migration | only on severance (E1) re-BFS | **automatic** — re-forward at next junction |
| Player configures junctions? | (n/a — but LB mode was a planned lever) | **no** — forwarding is internal, no router CLI |

---

## 4. The amendments — key reversals (was → now)

### GDD §M3 — the LB bullet → "Parallel pipes bundle; junctions forward"

> **was:** *"Junction load-balancing (LB) … Basic junctions → round-robin … Smart junctions → bandwidth-aware weighted LB … Smart LB is a node-tier / era unlock (M4) … Round-robin is the MVP default; weighted LB is full-game depth."*
>
> **now:** parallel pipes **bundle into one pooled-capacity link** (cap = sum) — **no LB mode** (round-robin & weighted LB deleted; PR #17 still does them as `[PROTO]`). Redundancy = **active capacity**. Each junction **forwards per-packet** (internal; **no router-config UI**) via deterministic **ECMP hash** `splitmix64(src, dst, class, pkt_id) mod N`. All junctions forward (no "smartness" tier). *Juice: "pop bigger" merge animation + Suno SFX thunk on each pipe joining a bundle.*

### GDD §M1 — "Redundancy & load-balancing" → "Redundancy & bundled pipes"

> **was:** *"…basic junctions do round-robin … smart junctions do bandwidth-aware weighted LB … round-robin is the MVP default, weighted LB a modernization unlock."*
>
> **now:** parallel pipes **bundle into one pooled-capacity link** (cap = sum); redundancy is **active capacity**, not idle insurance; **no LB mode** (round-robin/weighted deleted). *(Supersedes the prior LB decision; see decision-log.)*

### GDD §M2 — lever #3 "Junction priority policy + LB" → "Node serialization is automatic"

> **now:** no junction "LB mode" or manual triage policy to set; parallel pipes bundle + junctions forward; the node serialization you *see* (Express→Standard→Best) is the automatic consequence of the per-pipe lane weights (lever #2).

### GDD §M5 — crisis table reframed to active capacity

| Archetype | was | now |
|---|---|---|
| **Saturation** | "no load-balancing for demand" | "no **bundled redundancy** for demand" |
| **Single-point-of-failure** | "no **failover** path" | "no **alternate route** around it" |
| **Severance** | "Link cut → traffic lost unless rerouted" | "Cut one pipe of a bundle → pool **shrinks (graceful)**; only **full-bundle-loss** drops the route" |

### Architecture §6.2 (S2) — routing model rewritten

> **was:** *"route along the graph (through junctions, honoring LB modes)"* … *"Route computation: deterministic shortest-path-by-tier-cost with seeded tie-break (ODN-9/10)."* … Packet struct `route: Route_Handle` (cached) … *"Route migration (E29): in-flight packets keep their computed route until the next node…"*
>
> **now:** **[PROTO]** = one-shot BFS cached at spawn + parallel-pipe LB (`pick_pipe`); **[FULL]** = **per-hop forwarding + ECMP + bundles**: each junction holds a forwarding table `(junction,dst)→next-hop` rebuilt **only on a topology-changing Command, synchronously inside the tick**; equal-cost pick = pure `splitmix64` hash; parallel pipes **bundle** (cap = sum) → one fat edge, **no LB**. **E29 now automatic** (re-forward at next junction; no stale routes).

### Architecture §6.3 (S3 QoS) — **UNCHANGED**, stated explicitly

> **new bullet:** QoS is **unchanged** — bandwidth-on-a-pipe (lane scheduling) is **orthogonal** to routing (next-hop selection). A bundled link carries the pooled capacity with the same 3 lanes; ECMP decides *which* link, lane weights decide *what rides first*.

### Architecture ODN-9 / ODN-10 — the 4-rule determinism spine

> **ODN-9:** ECMP next-hop = **pure `splitmix64` hash** (reuses splitmix64 as a *finalizer*, **NOT** a draw from the sim rng) → same packet, same path, zero rng-state dependence. Carved out from the "ties → rng" corollary.
>
> **ODN-10:** new **"Routing determinism"** block — the 4 rules: (1) forwarding table rebuilt on topology-change only, inside the tick; (2) ECMP = pure hash, no map iteration in the hot path; (3) bundled cap = static sum at table-build; (4) pinned by the existing replay golden.

### Architecture edge-case table — E1 & E29

| | was | now |
|---|---|---|
| **E1** (severance) | "reroute or drop w/ severance" | + "**under bundles, demolishing one pipe of a bundle shrinks the pool (graceful), not a hard cut — only full-bundle-loss drops**" |
| **E29** (route migration) | "re-route at node boundaries only; E1 is the exception" | "**automatic under per-hop forwarding** — no stale spawn-time routes; re-forward at next junction. E1 is the (now-only) forced-reroute exception" |

### Architecture §18 — new Review Ruling #5

> *Routing model → RULED: per-hop forwarding + ECMP + bundled parallel pipes (lavish 2026-08-10).* Full prose of the ruling, the 4-rule determinism, QoS-orthogonal note, E1/E29 consequences, and the deferred TODOs.

### Decision-log — new dated supersession entry (history preserved)

> Appended `## 2026-08-10 — Routing model reversed…` — records the lavish source, the 5 locked decisions, **what it reverses** (the prior junction-LB decision), what it does NOT change (QoS), where it's applied, prototype-vs-fullgame, and the deferred TODOs. **The old LB decision is left intact as history** (superseded, not rewritten).

---

## 5. Lighter-touch edits (full list, for completeness)

| Location | Change |
|---|---|
| GDD §M3 terminology (junction) | "sets priority policy + LB mode" → "**forwards** per-packet; not configured by the player (no router-config UI)" |
| GDD §M3 node table | junction role "Merge/split/valve; sets priority policy + LB mode" → "Forwards traffic per-packet" |
| GDD §M3 port-limits | dropped "smart LB = mid/high tiers" tie-in → "basic → mid → high tier (M4)" |
| GDD §M2 readability | "redundancy is a deliberate parallel pipe" → "deliberate **bundled link** (parallel pipes merge … with a visible *pop*)" |
| Epics E1.4 | "load-balances across parallel pipes" → "forward per-packet (ECMP); parallel pipes **bundle**" + `[PROTO]` note |
| Epics E1.5 | "load-balance; insurance" → "**bundle** (active capacity); only full-bundle-loss drops" |
| Epics E1 test-contracts | "parallel pipes load-balance" → "parallel pipes bundle into pooled capacity" |
| Epics E2.3 | "Junction priority + LB (round-robin/weighted)" → "Junction forwarding + QoS serialization (no LB mode)" |
| Arch §6.1 struct | `pipe_lb_mode` field → `[PROTO]`-only comment; `[FULL]` bundles derived from adjacency |
| Arch §6.1 "Span/LB" bullet | → "Span" bullet: bundles, no LB in full game + `[PROTO]` note |
| Arch §6.1 responsibility | "Owns … junction LB mode" → "Owns … parallel-pipe **bundles**" |
| Arch §5.1 ODN-9/10 rows | + ECMP-hash / forwarding-table / bundled-cap phrases |
| Arch §8.1 catalog | `lb_mode_capable` annotated `[PROTO]`-only |
| Arch §8.2 data model | Pipe drops `lb`; Route slab marked `[PROTO]`-only |
| Arch §15.1 coverage | "M3 … / LB" → "M3 … / bundles" |
| Arch §4 ASCII (×2) | box "span, LB"→"span,bndl" (width-preserving); tree "route (junction LB modes…)"→"forward (per-hop + ECMP…)" |

---

## 6. Judgment calls — please confirm (annotate if you disagree)

1. **`architecture-v1.md` (the GL5.2 / Godot arch) is NOT amended.** It's the *superseded pre-pivot* technical design (the Odin arch footer names it "the prior technical design = GL5.2"). Its LB references are an accurate historical record of the Godot-era intent. The **Odin** arch (`odin-architecture-v1.md`) is the live canon and IS amended. *(If you'd rather I add a one-line "superseded — see Odin arch §18" pointer there, say so.)*
2. **`decision-log.md`: appended a supersession entry rather than rewriting history.** The old junction-LB decision stays intact (it happened); the new entry records the reversal. This matches the project's amendment pattern.
3. **`epics.md` was brought into scope** (not in the briefing's explicit list): E1.4/E1.5/E2.3 + E1 test-contracts said "load-balance" — leaving them would be a silent internal contradiction a future reader hits. Amended to match, with `[PROTO]` notes.
4. **`node_types.json` catalog:** annotated `lb_mode_capable` as `[PROTO]`-only. Did **not** add a `port_capacity` field the doc omitted (it exists in the code, but adding it is out of routing scope).
5. **QoS lane WRR-floor refs (arch L479/L999) left intact** — that's QoS *lane serialization* (ODN-3), a different axis from routing; not LB. Correctly preserved.

---

## 7. Acceptance checklist

- [x] GDD §M1/§M2/§M3/§M5 + epics amended to bundling + per-hop + ECMP
- [x] Arch §6.1/§6.2 amended; §6.3 QoS marked **unchanged / orthogonal**
- [x] ODN-9/10 carry the 4-rule determinism spine (ECMP = pure hash, not rng)
- [x] E1 softens under bundles; E29 automatic via per-hop
- [x] Gaps (tier-cost, clean-span) noted as full-game TODOs, not solved
- [x] Prototype (`[PROTO]`, PR #17) vs full-game (`[FULL]`) framing clear throughout
- [x] `docs/routing-explorer.html` preserved in-repo as canonical reference
- [x] Decisions & rationale block (sourced from the exploration) — §2 above + PR

*When this reads right to you, **Send & End** — I commit, push, and open the PR targeting `main` (Perkins OFF; docs-only). Annotate anything to iterate.*
