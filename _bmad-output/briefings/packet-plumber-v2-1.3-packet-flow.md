# Briefing: packet-plumber-v2-1.3-packet-flow

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (`eb23577` — 1.1 spine + 1.2 window/draw/topology are IN). **PR targets `v2`.**
- **Story:** stories-v2 **Story 1.3 — One packet flows (per-hop forwarding, you see it move)**.
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON**. Self-review: bmad-review-edge-case-hunter (determinism over the flow, the per-hop decision).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **bmad-quirk heads-up:** the create-story/dev-story tooling has been mis-resolving edits to the main checkout instead of the worktree (rc3-5 hit it). **Verify every edit lands in YOUR worktree** (`git status` from your cwd) and commit/push/PR from the worktree only.

## Mission

Make a **packet flow source→router→sink and watch it move** — the first routing. This is the story where the **locked routing model lands in code**: **per-hop forwarding at each junction** (the router decides the next hop per-packet), **NOT BFS, NOT a pre-calculated spawn-time route.** For 1.3 it's a single path (one packet, source→router→sink) — ECMP across equal-cost paths + parallel-pipe bundles come in later slices; 1.3 establishes the per-hop forwarding foundation the locked model builds on.

## Carry-forwards
- **1.1** — determinism spine (`Run_State`, `step`, `state_hash`, `Rng`, action-log) + harness. The flow MUST be replay-determinate (recorded actions reproduce byte-identical packet motion).
- **1.2** — window + render + the `Topology` (node + pipe data model) + `Command_Bus`. The packet flows ALONG the pipes the player drew; the render shows it moving.
- **The locked routing model** (canon #18): per-hop forwarding (internal, not player-facing), ECMP via seeded `splitmix64(src,dst,class,pkt) mod N` across equal-cost paths, parallel-pipe **bundles** (cap = sum; RR/weighted LB deleted). **For 1.3: per-hop forwarding on a single path** — the forwarding-DECISION shape is per-hop (a junction function that picks the next hop), even though there's only one path to pick here. Do NOT introduce BFS or a spawn-time route cache.

## The story (from stories-v2 Story 1.3 — read the full card)
- **Slice 1 · Epic E1.4 · Systems:** Flow (S2 trivial), per-hop forwarding.
- **Goal:** a packet spawns at a source, the router forwards it per-hop along the drawn pipe(s) to the sink, and you **see it move** across the render. Trivial flow (one packet, one path), but the forwarding is the per-hop decision model.

## From-scratch mandates
- **Fresh code on `v2`** — prototype is **reference-only** at `~/code/packet-plumber-prototype-ref` (mine `core/flow.odin` for the flow-sim DESIGN — progress/bandwidth/vis — but its routing was BFS; you build per-hop, not BFS).
- **Per-hop forwarding, not BFS.** The packet has no pre-computed `route[]`; each junction it reaches decides the next hop. (The prototype's `compute_route` BFS + cached `route` is explicitly NOT the model — do not port it.)
- **Determinism holds** — the per-hop decision + packet motion route through the action-log + state-hash; replay-equality over a flow sequence.

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 1.3 (full card).
2. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — S2 Flow, the **per-hop forwarding + ECMP/bundles model** (the locked routing — §6.2 as amended by canon #18), ODN-9/10/11 (determinism).
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — E1.4 (flow simulation).
4. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/core/flow.odin` (flow-sim mechanics to reuse as design — NOT its BFS routing).

## Verify
- A packet flows source→router→sink and you see it move in the window.
- Forwarding is **per-hop** (no BFS, no spawn-time route) — the junction decides the next hop.
- Replay-equality holds over the flow (recorded actions reproduce byte-identical motion); golden captured.
- `odin test` + `odin run harness` green; core still engine-free.
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-1.3-packet-flow working` at start
- `bin/ledger set packet-plumber-v2-1.3-packet-flow in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-1.3-packet-flow <url>`
- `herdr notification show "pp-v2-1.3" --body "<one-line>"` on finish
- Final message: the per-hop flow summary, the determinism result, whether 1.4 (win/lose stub) is next (closes slice 1).

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-1.3-packet-flow · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: (none)
- **PR target: v2**
