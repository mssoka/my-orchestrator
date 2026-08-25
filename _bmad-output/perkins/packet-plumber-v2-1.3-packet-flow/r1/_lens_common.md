# Perkins r1 lens — common context (read this first)

You are ONE lens in an automated PR-review swarm (Perkins round 1). You write
ONLY a JSON array of findings to your output file and then stop. You do NOT fix,
push, or merge. You review.

## Hard inputs (read these from disk)
- **Canonical diff (review EXACTLY these bytes):**
  `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/diff.patch`
- **Worktree (verify findings against this checkout, at exactly the reviewed sha 6265802):**
  `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-1.3-packet-flow-r1`
- **Spec files:**
  - This briefing: `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-1.3-packet-flow-r1.md` (READ THE LENS-GUARDS — they prevent false positives)
  - Job briefing: `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-1.3-packet-flow.md`
  - Story 1.3: `_bmad-output/planning-artifacts/sprints/stories-v2.md` (search "Story 1.3")
  - Architecture: `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (§6.2 S2 Flow; the 4-rule spine ~line 661; ODN-9/10/11 ~line 397)
  - Project conventions: `project-context.md` in the worktree root

## What this PR is
Packet-Plumber v2 Story 1.3: **per-hop packet forwarding** (the locked routing
model, canon #18) in its trivial single-path form. A packet spawns from a
hardcoded demand, is forwarded **per-hop** at each junction via a forwarding
table `(node,dst)→next hop` (rebuilt only on topology change — 4-rule spine
rule 1), and delivers at the sink. New files: `core/routing.odin`,
`core/flow.odin`, `core/flow_test.odin`. Modified: `core/step.odin`,
`core/types.odin`, `core/topology.odin`, `core/serialize.odin`, the render
(`app/render/view.odin`, `palette.odin`), the harness (`harness/run.odin`,
`demo.odin`, `drift.odin`, `goldens.odin`), `data/*.json`, and a new
`demos/flow.dem` + goldens.

## ⚠️ LENS-GUARDS — these are NOT findings (flagging them = false positive)
- **PER-HOP FORWARDING, NOT BFS, NOT a spawn-time route cache** is THE
  requirement (canon #18). The `Packet` struct MUST have NO `route[]` field;
  each junction consults the fresh table. Do NOT flag "missing route
  computation" / "should cache the route" — that absence is correct. A BFS-on-
  packet or a `compute_route` or a cached `route` sneaking IN would be a real
  blocker; the ABSENCE is not. (Note: `routing_rebuild` uses BFS to BUILD THE
  FORWARDING TABLE — next hop per dst — which is correct and NOT the banned
  per-packet BFS.)
- **1.3 = SINGLE PATH only.** ECMP (`splitmix64 mod N`) + parallel-pipe
  **bundles** are LATER slices, explicitly out of scope. Do NOT flag "missing
  ECMP" or "missing bundles."
- **Determinism is load-bearing.** Packet motion + demand ride the T1 hash;
  replay reproduces byte-identically. Flow demand is run-setup (NOT in the
  action log) and is re-created identically in BOTH the live (`lower_spawns`)
  and replay (`replay_hashes`) paths. A replay divergence over the flow is a
  blocker.
- **The id-0 sentinel** is a known trap: PP node/pipe ids are 0-based. An
  explicit `on_edge: bool` flag (and a +1 id scheme in the routing table) is
  the correct fix — do NOT flag its presence; flag a 0-sentinel bug if one
  exists (a packet on pipe/node id 0 mis-located).
- **T2 pixel goldens use the rlsw SOFTWARE renderer** (`tools/harness.sh`).
  `odin run harness` with the stock GPU `vendor:raylib` renders solid black
  headless. An all-black golden is a renderer-setup gap, NOT a logic bug.
- **Em-dashes are fine in Packet-Plumber copy** (the RT CI ban does not apply).
- **The base is `v2`, not `main`.** Do not flag the base.
- **Do NOT re-open 1.1/1.2 findings** (merged, verified).

## Legitimate finding categories here
- A BFS-on-packet / spawn-time route cache sneaking in (canon #18 violation) — blocker.
- A determinism break over the flow (replay divergence; un-logged RNG; demand
  not re-created in one of the two paths) — blocker.
- A 0-sentinel bug (on-edge/at-node keyed on a 0 id) — real defect.
- A non-per-hop decision (route pre-decided at spawn; "junction" not deciding).
- A packet that doesn't visibly move source→router→sink, or a wrong path.
- Core not engine-free (flow logic entangled with rendering).
- A real `odin test` / `odin build` / `harness` failure.

## Output contract (MANDATORY)
Write ONLY a JSON array to your assigned output file (see your lens file). No
prose, no markdown fencing. `[]` is a valid, honest answer when nothing is
wrong. Do NOT invent findings to fill a quota.

Each finding element MUST match EXACTLY:
```json
{
  "source": "<your assigned source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' only for findings with no possible code reference.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```

## ACCURACY MANDATE
No claim you make is taken at face value. Every finding is re-verified against
the actual code before it reaches the report; unverified findings are discarded
silently. So: open the file, read the lines, paste them verbatim in `evidence`.
Hedging ("might"/"could") signals you haven't verified — either verify and
report crisply, or drop it. Accuracy > volume.
