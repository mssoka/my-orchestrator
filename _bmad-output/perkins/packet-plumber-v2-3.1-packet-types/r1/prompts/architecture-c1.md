# Perkins lens prompt — architecture (chunk 1 — code+catalogs, round 1)

**You are the `architecture` lens. Your assigned `source` tag is `architecture`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/architecture-c1.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — chunk 1 of 2 — code + catalogs, 1387 lines, 16 files (review exactly these bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/chunk1.patch
- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha 37f5581): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.1-packet-types-r1
- SPEC / CONTEXT (read the sections named; full files):
  - Perkins briefing (your charter + lens-guards): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/spec/job-briefing.md
  - Story 3.1 card + slice-3 framing: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/spec/stories-v2.md (slice-3 framing ~line 228, the Story 3.1 card ~line 233)
  - v1 demand model (the design being ported): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/spec/sprint-plan-v1.md §3 (lines 126-332 — §3.1 PressurePlan/DemandSpec/SetPiece structure, §3.2 typed source→sink mapping, §3.3 the WEIGHTED_RANDOM dst-selection rule + its pinned test, §3.4 player visibility)
  - Architecture invariants: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/spec/odin-architecture-v1.md — ODN-1 core-engine-free (~line 410), ODN-3 QoS-inside-Flow (~line 474), ODN-5 catalogs integer-only + fail-fast (~line 522), ODN-7 director seam read-only (~line 558), ODN-9 owned PRNG (~line 600), §11.7 edge-case table (line 1592; E10 at ~1609)
  - GDD: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/spec/gdd.md — M2 packet types & QoS lanes (~line 155; the roster + "color never the sole encoding"), M3 topology & nodes (~line 205; the ECMP hash splitmix64(src,dst,class,pkt_id) mod N)


## The PR (scope)
v2 Story 3.1 — Packet types + the demand director (OPENS SLICE 3, the QoS differentiator). Two packet types (email low/low/low + streaming med/med/high) with distinct shapes/icons (never color alone — accessibility), spawned per a demand plan via the `scripted_plan_pressure` director, with SEEDED WEIGHTED-RANDOM destination selection. Replaces slice 1's trivial 1-packet `flow_seed_demand` with the real demand model (ported Odin-native from v1 §3: PressurePlan/DemandSpec/SetPiece). New `packet_types` catalog + `demand` catalog; the director emits a PressurePlan per era with typed source/sink selectors + weighted dst; flow_step spawns per spec inside the deterministic rng stream. Stories 3.2 (lanes), 3.3 (contention), 3.4 (SLA) build on this.
Files in THIS chunk (chunk 1 of 2 — code + catalogs): core/catalog.odin, core/demand.odin (NEW — the director), core/demand_test.odin (NEW — the §3.3 pins), core/determinism_test.odin (test-catalog extension), core/flow.odin (spawn path + weighted_pick), core/serialize.odin (class rides the T1 hash), app/main.odin, app/render/view.odin (per-class SHAPE render), harness/{catalogs,demo,drift,run}.odin (era + qos-fixture plumbing), data/{packet_types,demand,node_types}.json, demos/qos.dem (NEW). Chunk 2 (the goldens) is a SEPARATE lens wave — do not review it here.

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- **🚨 DISTINCT SHAPES, NOT COLOR ALONE — THE accessibility invariant.** email + streaming MUST be visually distinguishable by SHAPE/icon (color is secondary). A render that differentiates by color alone = a REAL blocker. (email=circle, streaming=triangle is the intended design.)
- **🚨 SPAWN DETERMINISM [E10] — load-bearing.** The (class, src, dst) spawn sequence must be byte-identical for a fixed seed. The dst selection is seeded WEIGHTED_RANDOM using the run's RNG INSIDE the deterministic stream (no new/unseeded draw; no map-iter in the spawn/dst path; array-indexed). A determinism break = a blocker. The §3.3 dst-distribution pinned test + the era-3 QoS golden (bit-for-bit replay) must be REAL.
- **CATALOGS INTEGER-ONLY + FAIL-FAST [ODN-5].** Sim values are integers; the loaders validate + FAIL FAST on bad data (NO silent defaults on malformed JSON). A silent-default path or a non-integer sim value = a real defect.
- **DIRECTOR READ-ONLY ON TOPOLOGY [ODN-7].** scripted_plan_pressure takes a read-only view and EMITS a PressurePlan — no topology mutation. A director that mutates topology (or reads crisis state) = a blocker.
- **QOS PROCS INSIDE FLOW [ODN-3]** — QoS procs live inside Flow (not a peer system). Do NOT flag "QoS not a separate system" — that's the design (3.1 sets up the data; 3.2 adds lanes).
- **round_robin DELIBERATELY DROPPED (routing-ruling lens-guard).** Load-balancing (round-robin/weighted-LB) is BANNED by the locked routing model — weighted-random dst selection IS the design. Do NOT flag "missing round-robin" or Demand_Selection having a single variant — its absence is correct. (ECMP 2.2 is a hash; the director's weighted-random is a spawn-time dst pick — both deliberate.)
- **T2 PIXEL FIDELITY DEFERRED per the rlsw gap (documented carry-forward, NOT a defect).** T2 is structurally/hash-verified (the era-3 QoS golden replays bit-for-bit); the pixel re-diff is the harness mini-story's job. Do NOT flag "T2 pixel not verified".
- **APP ERA-0 UNTIL THE ERA-FSM STORY (flagged, NOT a defect).** The app still runs era 0 (director inactive in the app; the render supports per-class shapes and the era-3 GOLDEN demonstrates both types). Do NOT flag "app doesn't spawn streaming / show era 3".
- **flow_seed_demand LEGACY PATH KEPT (the "keep both" decision).** The trivial slice-1 path stays for existing demos + the determinism test (no rng draw). Do NOT flag "legacy path not removed / dead code".
- **CARRIED DATA, NOT YET CONSUMED (by design).** Packet_Type.latency_tol_ms / max_loss_pct / bandwidth_demand / default_lane and Demand_Entry.default_lane / demand_weight are validated catalog data consumed by 3.2/3.3/3.4 — do NOT flag them as "unused fields". Packet_Shape has 9 variants but only Circle/Triangle render (the rest are later-era data) — do NOT flag the unrendered variants.
- **CORE ENGINE-FREE (ODN-1)** — the packet_types catalog + director live in `package core`; zero engine/raylib imports there (the shape/icon render lives in app/render). An engine type leaking into `package core` = a blocker.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–2 complete), not main. **The prototype is REFERENCE-ONLY** (mine its DESIGN; the logic was rebuilt clean).
- **Do NOT re-open 1.1–2.3 findings** (merged, Perkins-verified) — carry-forward only.

## Legitimate findings here WOULD be
- **A color-only differentiation** (no distinct shape/icon per packet type) — a blocker (accessibility).
- **A spawn/dst determinism break** (unseeded or extra RNG draw; map-iter in the hot path; the weighted-random not inside the deterministic stream; a temp-allocator/draw-order bug that desyncs replay) — a blocker [E10].
- **A silent-default catalog path** (malformed JSON → default instead of fail-fast) or a non-integer sim value — a real defect [ODN-5].
- **A director that mutates topology** (or reads Run_State/crisis state) — a blocker [ODN-7].
- **An engine type leaking into `package core`** (ODN-1) — a blocker.
- **The §3.3 dst-distribution test missing/fake** (the pinned test) — or the era-3 QoS golden not actually replay-pinned.
- **An `odin test` / `odin build` / harness failure at 37f5581.**
- A catalog validation gap (out-of-range/negative value accepted that the ODN-5 fail-fast bar should reject).
- An era/log-header plumbing bug (replay not re-creating the run identically).
- A real bug visible in the diff: wrong volume/window math, off-by-one in the surge window, self-loop leaks, histogram overflow, allocator misuse with a behavioral consequence.

## OUTPUT CONTRACT (follow exactly)
Write ONLY a valid JSON array to your output file (named below). No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
Each element MUST match this schema exactly:
{
  "source": "<your assigned source value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase; do not reconstruct from memory.>",
  "detail": "<why this is a problem, <=40 words; for acceptance findings quote the violated spec phrase>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer.

## YOUR LENS BRIEF

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation, ODN-7 director seam)?
- Will it create technical debt or make future changes harder (3.2 lanes / 3.3 contention / 3.4 SLA build directly on this)?
- Does complexity match the problem? Any premature abstraction?

`source` = "architecture".

## DONE
Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/architecture-c1.json` and stop. Do not fix anything. Do not run the interactive fix flow.
