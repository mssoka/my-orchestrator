# Briefing — packet-plumber-routing-bandwidth-cost (Job A: capacity-cost routing)

- **Job id:** `packet-plumber-routing-bandwidth-cost`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `routing-bandwidth-cost`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (canon-surface, determinism-critical — the v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2`. Rebase onto origin/v2 if it moves mid-work; clean-rebase hygiene
  (`git diff --check` before force-with-lease).

## Canon source (READ FIRST)

`/Users/moses/code/_bmad-output/problem-solution-2026-08-13.md` — the problem-solving session
artifact recording the user's ruling (2026-08-13) that drives this job. Read the PROBLEM
DEFINITION, SUCCESS CRITERIA, and RECOMMENDED SOLUTION sections before writing code. This
briefing is the condensed mission; the artifact is the canon.

## Mission (Job A — bandwidth-aware routing cost, the canon amendment)

The locked routing model (canon #18, routing ruling lavish 2026-08-10; `core/routing.odin`,
architecture §6.2) selects next hops by hop-count BFS only. **User ruling 2026-08-13:** path
cost = STATIC pipe capacity (the tier, fixed at draw time — never dynamic utilization);
intent = traffic engineering, "flows prefer fat pipes"; congestion avoidance stays the
player's job (QoS + engineering). Equal end-to-end cost → ECMP (pure hash, unchanged);
unequal → the fatter path wins. Players must be able to read this from the map.

**Recommended design (S2, from the artifact):** explicit per-tier integer `cost` in
`data/pipe_tiers.json`, initial ladder **20/10/5** (basic 5 → 20 · standard 15 → 10 ·
fast 40 → 5). Round numbers, halving pattern, near-inverse — player-summable.

**Acceptance (condensed — the artifact is canonical):**

1. **Data (ODN-5):** `cost` field added to `data/pipe_tiers.json` per tier (20/10/5),
   integer, validated `cost >= 1` at catalog load (zero-cost edges would break the
   per-hop progress guarantee — reject at load).
2. **Core:** `routing_rebuild` in `core/routing.odin` — unit-weight BFS becomes
   **Dijkstra over integer pipe costs** (cost per pipe = its tier's `cost` via
   `Topology.pipe_tier` → catalog). Array-backed cheapest-first with insertion-order
   tie-breaks — NO map iteration (ODN-10), NO floats, NO rng draws in routing.
   Equal-cost condition becomes `dist[v] + cost(pipe) == dist[u]`; the ECMP set is the
   neighbors satisfying it. `routing_equal_cost_hops` API shape (offset, count) unchanged.
3. **KEEP LOCKED — do not touch:** `ecmp_pick`/`ecmp_hash` (pure identity hash, spine
   rule 2); rebuild-only-on-topology-change (rule 1 — static weights ⇒ automatic, still a
   pure function of Topology); table stays DERIVED, NOT serialized into the T1 hash
   (rule 3); `flow.odin`'s forward pass (same `(offset, count)` lookup + `ecmp_pick`).
4. **Core tests (`@(test)`):** (a) mixed-tier diamond picks the fat path as a UNIQUE next
   hop (no ECMP when costs differ); (b) different-tier equal-sum tie → ECMP set of 2
   (with 20/10/5: S→R1 standard(10) + R1→D fast(5) = 15 vs S→R2 fast(5) + R2→D standard(10)
   = 15 — a TRUE tie across different tiers); (c) re-step determinism (byte-identical);
   (d) ladder read from data (a data change moves behavior — proves ODN-5 wiring).
5. **Demo:** new `demos/ecmp_cost.dem` — mixed-tier diamond; captures pin the fat-path
   unique hop mid-flight AND a true different-tier tie split; `expect hash stable`.
   NEW golden files only. **Existing demos are all standard-tier → unit-cost paths
   identical to today's → existing goldens MUST NOT shift.** If any existing golden
   shifts, STOP and flag — do not re-bless without proof.
6. **Canon docs in the SAME PR:** architecture `odin-architecture-v1.md` §6.2 routing
   model — replace hop-count language with the capacity-cost model (data-driven integer
   ladder, ECMP = equal END-TO-END cost, spine rules 1-3 restated unchanged); GDD routing
   section — the one-line player rule: "packets take the fattest route; equal cost splits
   by hash" + a note that assist features (flow preview, glow, forecast) arrive in
   follow-up jobs. Docs = canon touch-up documenting a user ruling made live 2026-08-13 —
   **lavish NOT needed, PR directly.**
7. **Scope guard:** routing cost ONLY. NOT the readability package (Job B: assist tiers /
   glow / tie cue), NOT the forecast flow-shift prediction (Job C) — separate jobs. NO new
   player commands; LOG_VERSION stays unless truly required (flag first). No per-class
   routing preferences (full-game idea, scope-guarded out).

**Verify:** `odin test` green (core/demos/lint), harness green, determinism re-step
byte-identical, new pins pass on all CI targets, existing goldens unchanged (diff-bundle
first if any shift), launchable increment in the PR body (mixed-tier map where the fat
path visibly wins + a true tie).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: routing-bandwidth-cost
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
