# Briefing: packet-plumber-routing-canon-amend

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`, base `main`).
- **Deliverable:** amend the canonical **GDD + architecture** markdown to reflect the user's **LOCKED full-game routing decisions**. This is a DOCS deliverable → **lavish review loop BEFORE the PR opens**.
- **Model:** `zai-coding-cn/glm-5.2` (kimi down; doc amendment is capable-tier work — the decisions are MADE, you write them faithfully, you don't design them).
- **Perkins:** OFF (`pr_review=0`) — this is a docs PR, not code. The review surface is the lavish loop (the user amends in-browser before PR).
- **Skills:** `lavish` (REQUIRED — serve amended docs, foreground-poll, iterate before PR) + `gds-gdd` (GDD amendment workflow). Read the lavish playbooks first (`npx -y lavish-axi playbook <id>`).

## Mission — why

The routing-explorer lavish session **converged**: the user LOCKED the full-game routing model. The canonical docs (GDD §M3/§M5, architecture §6.2/§6.3, ODN-9/10, E29, E1) still describe the **old** model (BFS + round-robin/weighted parallel-pipe LB). Amend them to match the locked decisions — precisely, because ODN-9/10 and the routing model are load-bearing invariants. The lavish review is the gate: the user signs off the exact wording before any PR.

## The LOCKED full-game routing decisions (write these faithfully)

1. **Per-hop forwarding at each junction — INTERNAL, not player-facing.** Players draw pipes; there is NO router-config CLI. Each junction makes a per-packet forwarding decision. (Supersedes the spawn-time pre-calculated BFS route.)

2. **ECMP across equal-cost paths** via a seeded hash `splitmix64(src, dst, class, pkt_id) mod N` over the equal-cost next-hop set. Deterministic per packet.

3. **Parallel pipes BUNDLE into one pooled-capacity link** (capacity = **sum** of the bundled pipes' capacities). This **DELETES the round-robin / capacity-weighted LB mechanic entirely.** Redundancy = **active capacity** (a bundled redundant pipe always contributes its bandwidth to the pool — no idle failover).

4. **Determinism HOLDS (ODN-9/10, 4-rule):**
   - Forwarding table rebuilt **only on topology-change/sync** (never per-packet/per-tick).
   - ECMP is a **pure hash** (splitmix64) — no map iteration, no `rng` draw in the hot path.
   - Bundled capacity is a static sum at table-build time.
   - Net: as deterministic as the BFS it replaces.

5. **Juice (capture in GDD):** a **"pop bigger" merge animation** when pipes bundle into a pooled link + a **Suno SFX** thunk (re-triggered each time a pipe joins a bundle).

## Docs to amend (specific changes)

- **GDD §M3 (junction LB):** the round-robin (basic) / bandwidth-weighted (smart) LB modes are **DELETED**. Replace with **bundling**: parallel pipes between a node pair merge into one pooled-capacity link (cap = sum). The "smart-junction LB modernization unlock" is gone. Junctions now forward (decision 1) rather than load-balance.
- **GDD §M5 (crises / redundancy):** redundancy is now **active capacity**, not passive failover insurance. Adjust the single-point-of-failure / severance framing: a lost bundled pipe reduces pool capacity, it doesn't cut the route (only full-bundle-loss drops).
- **Architecture §6.2 (S2 routing):** replace "shortest-path-by-tier-cost" with **per-hop forwarding + ECMP hash**. The route is no longer pre-calculated at spawn; each junction forwards per-packet. Mark the current BFS prototype as `[PROTO]`, the per-hop+ECMP model as the full-game target.
- **Architecture §6.3 (QoS):** **UNCHANGED** — QoS is bandwidth-on-a-pipe (lane scheduling), orthogonal to routing. State this explicitly so no one conflates the two.
- **ODN-9/10 (determinism):** add the **forwarding-table + ECMP-hash rules** (the 4-rule above). Affirm determinism is preserved.
- **E29 (route migration):** now **automatic via per-hop forwarding** — no stale spawn-time routes; topology changes propagate via table rebuild at the next sync. In-flight packets re-forward at the next junction.
- **E1 (severance):** **softens under bundles** — a severed bundled pipe shrinks the pool (graceful), not a hard route cut; only full-bundle-loss drops the packet.

## Gaps — NOTE as full-game TODO, do NOT solve

- **Tier-cost routing** (the architecture's old "by-tier-cost" intent) — not in this decision; flag as a future option.
- **Clean-span** (span-based throughput degradation) — unchanged, still a TODO.

## Prototype vs full-game framing
The merged prototype (PR #17) implements **BFS + parallel-pipe LB (round-robin/weighted)** in `core/flow.odin` / `core/topology.odin`. The docs must record this as the `[PROTO]` implementation and the per-hop+ECMP+bundles model as the `[FULL]` target — don't pretend the prototype already does it. A future full-game build job will port the code; THIS job is docs-only.

## Source material (read)
1. **The exploration artifact** (the reasoning + comparisons behind these decisions): `/Users/moses/code/_bmad-output/routing-explorer.html` (Silas is preserving a copy out of the worktree). Mine it for the "Decisions & rationale" prose.
2. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — §M3, §M5 (the sections you amend).
3. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — §6.2, §6.3, ODN-9/10, E1, E29.
4. **`core/flow.odin` + `core/topology.odin`** — the current BFS+LB prototype (so you describe the gap accurately).

## Flow
1. Read the source material; extract the rationale from the exploration artifact.
2. Amend the GDD + architecture per the changes above (precise on ODN-9/10 + the routing model).
3. **Serve the amended docs via lavish** (the diff / the amended sections); foreground-poll for the user's in-browser annotations; iterate until they Send & End.
4. Only after lavish sign-off: commit, push, open PR targeting `main`. **Never merge.**
5. Badge out a field-note shard.

## Acceptance
- GDD §M3/§M5 + arch §6.2/§6.3/ODN-9/10/E29/E1 amended to the locked decisions; QoS §6.3 marked unchanged; gaps noted as TODOs; prototype-vs-fullgame framing clear.
- A "Decisions & rationale" block in the PR (and/or the arch) capturing WHY (per-hop+ECMP chosen over BFS; bundles chosen over LB) — sourced from the exploration.
- lavish sign-off captured before PR.
- No code changes (docs-only).

## Self-report
- `bin/ledger set packet-plumber-routing-canon-amend working` at start (`clarifying` if you halt)
- `bin/ledger set packet-plumber-routing-canon-amend in-review "PR <url>"` when PR opens
- `herdr notification show "routing-canon-amend" --body "<one-line>"` on finish

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: routing-canon-amend · base: main
- model: zai-coding-cn/glm-5.2 · pr_review: 0 · github_issue: (none)
