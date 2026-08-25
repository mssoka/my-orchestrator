# Briefing — packet-plumber-v2-5.1-map-growth (story 5.1 — deterministic map growth + spawn validity)

- **Job id:** `packet-plumber-v2-5.1-map-growth`
- **Repo:** packet-plumber · **Base:** `v2` @ 2e4f145 (post-5.8) · **Slug:** `v2-5.1-map-growth`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (gameplay + canon-surface: routing/topology semantics,
  possibly serialization).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.1-map-growth <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 5.1
  (in the repo). Read it + the sprint-plan-v2 §5.1 row + the 3.5 amendment commit
  (9a5a35b) BEFORE designing. Architecture refs: arch §S1 (Topology), `[ODN-7]`
  (director seam), `[E31]` (spawn validity), `[ODN-6]` (portable-core re-sim).
- **CI:** green. Full local suite must pass.

## Mission — implement story 5.1 (the map must GROW)

**The goal (GDD Mini Motorways model):** nodes appear over time, deterministically
from the seed; growth proceeds outward from the player-placed router mesh; every
spawned terminal is connectable. This is the biggest gameplay hole in v2 — the map
is currently static.

**Hard requirements (all load-bearing, all pinned by the card):**

1. **Determinism is the spine.** Same seed → IDENTICAL map-growth timeline. Growth
   derives from the seed + executed tick (the rng stream), NEVER wall-clock time.
   Replay stays byte-identical: a replayed run grows the same map at the same ticks
   with zero logged input. Prove it: T1 (record/replay hash identity on a growing
   map) + T2 goldens of a growing map.
2. **Spawn validity `[E31]`:** every spawned terminal is connectable-within-span +
   min separation from existing nodes/pipes; invalid candidates are
   **rejection-sampled from the same rng stream** (deterministic — no wall-time
   retry loops).
3. **Routers are NEVER director-spawned** (3.5 amendment, commit 9a5a35b): growth
   spawns TERMINALS only, biased outward from the player-placed router mesh; the
   player places every router. If the growth model ever wants a router, it wants a
   redesign of this story — flag, don't invent.
4. **Director seam `[ODN-7]`:** drive growth via `plan_pressure` at the existing
   director seam — no new god-object. If the seam needs extending, extend it
   minimally + document.
5. **Serialization decision, made explicitly:** does growth state enter the replay
   log / save format? If growth is fully seed-derived, it should NOT need log
   entries (derive, don't record) — but if any growth parameter is run-scoped
   (non-seed), it must serialize with a LOG_VERSION bump (5.8 just moved 3→4;
   follow that exact discipline + golden-fold pattern). State the decision + proof
   in the PR body either way.
6. **Camera/render:** new nodes must be visible on the existing canvas (5.2's
   health telegraph is LATER — plain nodes now, no health styling).

**Acceptance:**

1. The card's Given/When/Then verified: seed-identical growth timeline (pinned by
   test), outward-from-mesh bias, terminals-only spawns, E31 validity, replay
   byte-identity.
2. New goldens: growing-map T1 + T2 (byte-stable); existing goldens unshifted
   (static-map demos unchanged unless a demo is deliberately migrated to growth —
   list any such).
3. Full local suite green; PR body carries: the serialization decision + proof,
   the E31 rejection-sampling design, and demo/golden inventory changes.
4. Story card status line updated in the same PR (the 5.3 pattern).

**Scope guard:** map growth ONLY. No health states (5.2), no touch/controller
(5.4), no new packet types, no economy. Demos/goldens updates only as required by
growth.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.1-map-growth
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
