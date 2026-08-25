# Briefing: packet-plumber-v2-3.1-packet-types

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (slices 1–2 complete: spine, window, flow, win/lose, bundles, ECMP, demolish). **PR targets `v2`.**
- **Story:** stories-v2 **Story 3.1 — Packet types + demand-pairing data**. **Opens slice 3** ("QoS: packet types + lanes — the differentiator").
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON**. Self-review: bmad-review-edge-case-hunter (spawn determinism, weighted-random dst selection, catalog validation).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **bmad-quirk heads-up:** verify every edit lands in YOUR worktree (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Add **packet types + the demand director** — the data foundation for QoS. Two packet types (**email** + **streaming**) with distinct shapes/icons (never color alone — accessibility), spawned per a demand plan via the `scripted_plan_pressure` director, with **seeded weighted-random destination selection**. This replaces slice 1's trivial 1-packet `flow_seed_demand` with the real demand model (ported Odin-native from v1 §3). Slice 3's later stories (3.2 lanes, 3.3 contention, 3.4 SLA) build on this.

## The story (from stories-v2 Story 3.1 — read the full card)
- **Slice 3 · Epics E2.1, E2.4 · Systems:** catalogs `[ODN-5]`, Flow spawn, director `[ODN-7]`.
- **Goal:** the `packet_types` catalog (email: low/low/low; streaming: med/med/high) + the demand-pairing data (`PressurePlan`/`DemandSpec`/`SetPiece`, carried from v1 §3, Odin-native): per-source-class demand with typed source/sink selectors + **WEIGHTED_RANDOM** dst selection (seeded).
- **Then:** two packet types flow with **distinct shapes/icons** (never color alone); the `(class, src, dst)` spawn sequence is **byte-identical** across runs for a fixed seed `[E10]`; the dst distribution over many packets matches sink `demand_weight`s ± tolerance (the v1 §3.3 pinned test); catalogs are **integer-only** for sim values + **fail-fast validated** at load `[ODN-5]`.

## Carry-forwards
- **Slices 1–2** (all in v2) — the flow, topology, routing, bundles, ECMP, demolish this grows onto.
- **`flow_seed_demand`** (slice 1's trivial 1-packet demand) — 3.1 supersedes it with the `PressurePlan` director (the real demand model). Keep the old path working for existing demos/tests until the director covers them, OR migrate the demos (your call — note it).
- **v1 §3** (the demand model: `PressurePlan`/`DemandSpec`/`SetPiece`) — port Odin-native. The v1 design lives in the sprint-plan-v1 + the prototype reference.

## From-scratch mandates (load-bearing)
- **Distinct shapes, not color alone** — email + streaming must be visually distinguishable by SHAPE/icon (accessibility; color is secondary). A Perkins lens-guard checks the render isn't color-only.
- **Spawn determinism `[E10]`** — the `(class, src, dst)` spawn sequence is byte-identical for a fixed seed. The dst selection is **seeded WEIGHTED_RANDOM** (uses the run's RNG, NOT a new draw — keep it inside the deterministic RNG stream; no map-iter in the hot path, same discipline as ECMP).
- **Catalogs integer-only + fail-fast `[ODN-5]`** — sim values are integers; the catalog loader validates + fails fast on bad data (no silent defaults on malformed JSON).
- **Director is read-only on topology `[ODN-7]`** — `scripted_plan_pressure` takes a read-only topology view, emits a `PressurePlan` (no mutation).
- **QoS procs live inside Flow `[ODN-3]`** — not a peer system (slice 3's framing; 3.1 sets up the data, 3.2 adds the lane logic).
- **No engine types in `package core`** (ODN-1); the shape/icon render lives in `app/render`.
- **Golden:** T1 + T2 of two packet types flowing (T2 structural/hash-verified — pixel deferred per the rlsw-harness gap; flag in your final message).

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 3.1 (full card, line 233) + the slice-3 framing (line 228).
2. **`_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md`** — §3 (the demand model: `PressurePlan`/`DemandSpec`/`SetPiece`, §3.3 the dst-distribution pinned test) — the v1 design to port.
3. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — `[ODN-5]` (catalogs: integer, fail-fast), `[ODN-7]` (director: read-only topology → plan), `[ODN-3]` (QoS inside Flow), `[E10]` (replay), §11.7 headless-test contract.
4. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — E2.1 (packet types), E2.4 (demand/pacing).
5. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/` (mine its packet-type shapes/icons + demand model; rebuild the logic clean).
6. **Existing catalogs:** `data/node_types.json`, `data/pipe_tiers.json`, `data/balance.json` — the load pattern + `catalogs_load` to mirror for `packet_types`.

## Verify
- Two packet types (email + streaming) flow with distinct shapes/icons (not color alone).
- `(class, src, dst)` spawn sequence byte-identical across runs for a fixed seed `[E10]`; dst distribution matches `demand_weight`s ± tolerance (the v1 §3.3 test).
- Catalog integer-only + fail-fast on bad JSON `[ODN-5]`; director read-only on topology `[ODN-7]`.
- `odin test` + `odin run harness` green; core still engine-free; existing demos/tests still pass (or migrated cleanly).
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-3.1-packet-types working` at start
- `bin/ledger set packet-plumber-v2-3.1-packet-types in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-3.1-packet-types <url>`
- `herdr notification show "pp-v2-3.1" --body "<one-line>"` on finish
- Final message: the packet-types summary, the spawn-determinism + weighted-random verification, whether 3.2 (3-lane QoS) is next.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-3.1-packet-types · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: (none)
- **PR target: v2** · descriptive tab label `pp-v2-3.1-packet-types`
