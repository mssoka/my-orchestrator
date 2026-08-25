# SPEC BUNDLE — packet-plumber-v2-5.1-map-growth (PR #51, reviewed sha ef858e8)

## PART 1 — Job briefing (the implementing minion's spec)

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

## PART 2 — Story 5.1 card (stories-v2.md)

### Story 5.1 — Deterministic map growth + spawn validity

- **Slice:** 5 · **Epic(s):** E3.1, E3.2 · **Systems:** Topology growth (S1), director
  `[ODN-7]`.
- **Goal.** Nodes appear over time (Mini Motorways model), deterministically from the seed;
  growth proceeds outward from the router mesh; every spawned terminal is connectable.
- **Status:** implemented 2026-08-15 — PR open (the director's map-growth branch
  `growth.odin`, ODN-7: one terminal per 6 s window from the executed tick, TERMINALS only
  — routers never director-spawned, the 3.5 amendment — biased outward from the
  player-placed router mesh; E31 spawn validity with bounded rejection sampling from the
  same rng stream; growth fully seed-derived — NO action-log entries, NO LOG_VERSION bump;
  the `growth.dem` T1+T2 goldens, replay byte-identical, existing goldens unshifted).

**Given/When/Then:**
- **Given** the director's `plan_pressure` (seeded) driving map growth via Topology;
- **When** new nodes spawn over time;
- **Then** the same seed → **identical map-growth timeline**; growth proceeds **outward from
  the player-placed router mesh** (terminals spawn; **routers are NEVER director-spawned —
  the player places them, story 3.5**); every spawned terminal is
  connectable-within-span + min separation, else **rejection-sampled from the same rng
  stream** (deterministic) `[E31]`; replay is byte-identical.

- **Edge-case contracts:** `[E31]` spawn-validity. **Golden:** T1 + T2 of a growing map.
- **Launchable increment:** nodes appear over time, the map grows.

### Story 5.2 — Node health states

## PART 3 — Architecture refs (odin-architecture-v1.md)

### §6.1 S1 — Topology (growth/E31 paragraph + canon + distance metric)
  ```odin
  Node_Kind :: enum u8 { Terminal, Junction }
  Topology :: struct {
      // nodes (parallel arrays; index = slot)
      node_kind:  [dynamic]Node_Kind,
      node_type:  [dynamic]u16,        // index into node_types catalog
      node_pos:   [dynamic][2]i32,     // integer grid — ADR-10 carried
      node_gen:   [dynamic]u32,        // generation for monotonic ids (E11)
      // pipes
      pipe_a, pipe_b:   [dynamic]u32,
      pipe_tier:        [dynamic]u16,  // index into pipe_tiers catalog
      pipe_weights:     [dynamic][3]i32, // lane WFQ weights (integer — ODN-3)
      pipe_lb_mode:     [dynamic]Lb_Mode,  // [PROTO] round-robin/weighted per-pipe LB; [FULL] deleted — parallel pipes BUNDLE (derived from adjacency at table-build)
      pipe_legacy:      [dynamic]bool,
      adjacency:        [dynamic][dynamic]u32, // node slot -> incident pipe slots
  }
  ```
  Positions are `[2]i32` grid coords (integer → determinism). Ids are
  `{slot, gen}` — monotonic, never recycled (E11). Adjacency is array-based;
  **no maps are iterated anywhere in core** (ODN-10).
- **Topology canon from the art pivot (now load-bearing data, not just pixels):**
  **terminals connect via routers only — never terminal-to-terminal** (look-book
  D11 / amendment A6). The Command_Bus rejects terminal↔terminal draws
  (`Edit_Error.terminal_to_terminal`); terminals are leaves, routers are the
  interconnect. This was locked *after* GL5.2 was written — the Odin build
  inherits it as a first-class edit rule.
- **Span (modernization constraint).** Tier max-span enforced at edit;
  junctions are repeaters (routing through one resets the span budget)
  `[GDD § M3]`; clean-span degradation is the `wear` curve ([LATER] depth;
  PROTO enforces the hard max). **Parallel pipes bundle** into one
  pooled-capacity link (cap = sum of members) `[GDD § M1, M3]` — there is
  **no LB mode in the full game**. `[PROTO: PR #17 still uses round-robin /
  capacity-weighted LB per pipe; the full-game port replaces it with bundles
  + per-hop forwarding — routing ruling, lavish 2026-08-10.]`
- **Deterministic map growth + spawn validity.** New nodes appear over time
  (Mini Motorways model); spawn timing + placement come from `plan_pressure`
  (ODN-7) drawing the seeded rng, applied by Topology — reproducible from the
  seed. Growth proceeds **outward from the router mesh** (routers co-spawn
  with/alongside terminals — the lesson the Godot prototype paid for: its
  director once spawned a house 20+ tiles from every router, unwinnable
  demand). **Spawn-validity contract (E31 — pinned test, tied to the
  no-soft-lock rule):** every spawned terminal must be connectable — within
  some available tier's span of an existing or co-spawned router — else the
  director re-places it by rejection sampling from the *same* rng stream
  (deterministic). Placement also enforces a minimum node separation and
  never overlaps (snap disambiguation, E4, depends on it). Whether routers are
  additionally *player-placeable* (a Command with cost) is a [LATER] tool
  decision; PROTO's routers are director-spawned.
- **Distance metric (pinned).** All span/cost/snap math uses **integer
  Euclidean²** — `dx*dx + dy*dy <= span*span`; no `sqrt` anywhere in core
  (exact, cheap, identical on every target). One metric serves span
  validation, draw cost (length × tier), and the snap radius (E4).
- **Junction demolish (E27).** Demolishing a junction is an **atomic batch**:
  its incident pipes are demolished first (in edge-id order — deterministic),
  each per E1 (reroute-or-drop), then the vertex is removed — one `apply_all`
  transaction, so replay cannot diverge on ordering.

### ODN-6 — Leaderboard seam (portable-core re-sim)
#### ODN-6 — Leaderboard service seam (the m6 payoff, upgraded honestly)

**Decision.** `Leaderboard_Service` is a struct of proc pointers (Odin's
native interface idiom — §11.5): `submit`, `fetch_board`, `poll`. PROTO binds
a no-op local impl. Production binds an HTTP client (`core:net` or a vendored
HTTP lib — a production decision, not this doc's).

**The upgrade the pivot buys:** GL5.2's validation strategy was *lean* because
full re-sim needed a portable core it didn't have (`[REVIEW m6]`). Here the
core is portable by construction — the server validator can **compile the same
`package core`** into the backend (any language hosting it via C-ABI, or a
small Odin validator service). Full per-submission re-sim becomes cheap and
bit-exact; the lean-vs-full validation decision moves from "constrained by
portability" to a pure cost/ops choice at production time. The submission
payload carries `(seed, era_progress, modifiers, action_log_summary, score)`
— `modifiers` included from day one (`[REVIEW m14]` carried).


### ODN-7 — CrisisDirector seam (plan_pressure)
#### ODN-7 — CrisisDirector seam as a proc field (carried, de-boilerplated)

All crisis *pressure* (demand timeline + surge scheduling + map growth) flows
through one proc pointer on the run config:

```odin
Run_Config :: struct {
    seed:          u64,
    modifiers:     []Modifier_Id,          // daily/weekly twists; [] for standard
    plan_pressure: proc(topology: Topology_Snapshot, era: Era_State,
                        tick: u64, rng: ^Rng) -> Pressure_Plan,
    // ^ read-only view in, plan out; pure w.r.t. sim state — the M1 rule
    // ("the Director must never read crisis state") is structural, not discipline.
    leaderboard:   Leaderboard_Service,    // ODN-6
}
```

PROTO binds `scripted_plan_pressure` (data-driven demand timeline — for PROTO
the surge curve lives in `crises.json` + `balance.json`; `eras.json` takes
over when the Era layer lands — seeded). V2 binds the AI auditor `[FORGE weak #4]`
behind the same field. GL5.2 needed an abstract-base-class convention +
`assert(false, "override me")` to fake this (`[REVIEW M4]`); Odin's proc
pointers make it one line, type-checked, zero ceremony. (GL5.2's own m12
observation — the seam earns its place in the architecture while the prototype
impl stays trivial — carries over exactly.)


## PART 4 — The 3.5 amendment (commit 9a5a35b — user ruling 2026-08-12; SUPERSEDES the arch doc's 'routers co-spawn / PROTO routers director-spawned' text)

9a5a35b7a31ea65aaf7f9f28d8d48324450ecfa3
stories-v2: restore player node placement — story 3.5 (router toolbox) + amend 5.1 (routers never director-spawned, player-placed)
GDD canon presumes a player-designed network (build/redesign cadence, topology-flaw
crises, port limits); the prototype proved Cmd_Place_Router + tray; the v2 vertical-slice
fixture dropped it and 5.1's passive 'routers co-spawn' contradicted the loop. User ruling
2026-08-12: terminals spawn, the player places routers.

@@ -403,7 +435,8 @@ on touch + controller.*
 - **Given** the director's `plan_pressure` (seeded) driving map growth via Topology;
 - **When** new nodes spawn over time;
 - **Then** the same seed → **identical map-growth timeline**; growth proceeds **outward from
-  the router mesh** (routers co-spawn with/alongside terminals); every spawned terminal is
+  the player-placed router mesh** (terminals spawn; **routers are NEVER director-spawned —
+  the player places them, story 3.5**); every spawned terminal is
   connectable-within-span + min separation, else **rejection-sampled from the same rng
   stream** (deterministic) `[E31]`; replay is byte-identical.
 

## PART 5 — Perkins round-1 lens-guards (review context — prevents false positives)


## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — determinism spine.** Growth derives ONLY from the seed + the
  executed tick (the rng stream): NO wall-clock timing, NO wall-time retry loops, NO
  hidden nondeterminism (e.g. hash-map iteration order, environment-dependent
  geometry). Same seed → IDENTICAL growth timeline; replay stays byte-identical (a
  replayed run grows the same map at the same ticks with zero logged input). The
  growth_flip drift class proves a growth-toggled replay diverges loudly. Any
  nondeterministic path = a blocker.
- **🚨 Derive-don't-record integrity:** growth must NOT need log entries (no
  LOG_VERSION bump) — verify the replay byte-identity holds WITHOUT growth entries
  (if any run-scoped growth parameter was serialized, that's a LOG_VERSION question
  and must follow the 5.8 3→4 discipline). The topology section of the T1 hash
  carries the growth state.
- **E31 validity exact:** every spawn in-bounds + min-separated (integer distance)
  + connectable-within-span of a junction (14 era 1 / 18 era 3); rejection sampling
  bounded (8 attempts) from the SAME rng stream — a spawn that violates E31 or a
  wall-clock retry = a blocker.
- **Routers NEVER director-spawned** (3.5 amendment, 9a5a35b): growth spawns
  TERMINALS ONLY; a director-spawned router = a blocker (the amendment is
  load-bearing canon).
- **Golden stability:** all 27 pre-existing demos' goldens byte-identical/unshifted;
  growth tuning in core consts (NOT balance.json — a catalog edit = golden-poisoned
  = a blocker); the new growth goldens byte-stable.
- **Base = `v2`** — includes the full shipped line (5.5/5.6/5.3/5.7/5.3-ux/5.8).
  Carry-forward only; do NOT re-open settled findings (the 5.8 golden-fold discipline
  and the 5.7 determinism contract are settled).
- **Scope guard:** map growth ONLY — no health states (5.2), no touch/controller
  (5.4), no new packet types, no economy.
