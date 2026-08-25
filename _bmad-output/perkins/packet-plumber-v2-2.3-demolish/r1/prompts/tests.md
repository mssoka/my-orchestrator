# Perkins lens prompt — tests (round 1)

**You are the `tests` lens. Your assigned `source` tag is `tests`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.3-demolish/r1/tests.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF (review exactly these bytes, 1025 lines): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.3-demolish/r1/diff.patch
- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha 8a652dd): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.3-demolish-r1
- SPEC / CONTEXT:
  - Perkins briefing (your charter + lens-guards): /Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-2.3-demolish-r1.md
  - Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-2.3-demolish.md
  - Story 2.3 card + slice-2 exit: /Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/sprints/stories-v2.md (read the "Story 2.3" section ~line 199, and "Slice 2 exit")
  - Architecture invariants: /Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md — esp. edge-case table E1/E2/E27/E29 (~line 1600), the routing 4-rule spine (~line 661, rule 1 = table rebuild on topology change), §6.1 E27 junction-batch (~line 900), §6.2 E29 auto-migration (~line 972), ODN-1 (core-engine-free, §~410), ODN-9/10/11 determinism.

## The PR (scope)
Story 2.3 — Demolish + severance under bundles + automatic migration (closes slice 2). Adds: Cmd_Demolish_Pipe / Cmd_Demolish_Node (validate→apply, action-logged, replay-deterministic); tombstones entities (alive=false, ids monotonic never recycled E11); bumps Topology.gen so the forwarding table + bundle view rebuild next step (rule 1). Files: core/{types,topology,flow,serialize}.odin, core/{demolish,flow}_test.odin, harness/{demo,run}.odin, demos/demolish.dem, goldens/{demolish.t1,demolish.log.bin}.

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- E29 AUTO-MIGRATION IS STRUCTURAL (the story's whole point). NO cached route on a packet — a demolish → table rebuild (rule 1) → in-flight packets re-forward at the NEXT JUNCTION with zero special-casing. The ABSENCE of a `route[]` / spawn-cached path is CORRECT, not a defect. A cached-route/spawn-time-route path (or per-packet pre-computed reroute) = a REAL blocker (the prototype's BFS sneaking back). flow.odin Packet struct has NO route field — verify this.
- GRACEFUL SHRINK, NOT A HARD CUT [E1]. A bundle-member demolish reduces POOLED capacity (re-derive on rebuild; cap = sum of survivors); traffic continues. ONLY full-bundle-loss (all members gone) drops the route. bundles_rebuild re-derives from LIVE pipes only — this is correct.
- .Terminal_Demolish [E2]. Terminal nodes can't be demolished — rejected with the typed error. validate_demolish_node checks is_terminal.
- JUNCTION DEMOLISH = ATOMIC BATCH [E27]. Incident pipes first (slot order == pipe-id order, since ids are monotonic + appended in slot order — VERIFIED correct), each per E1, THEN the vertex — ONE topology_apply_edit call, gen bumps ONCE. This is correct; do not flag the single gen bump.
- DEMOLISH IS A LOGGED COMMAND. Applied via validate→apply, recorded in the action log, replay-reapplied at its tick (like draw). A demolish that mutates state outside the action-log/replay path = a determinism break.
- DETERMINISM (ODN-9/10/11). A demolish mid-traversal replays byte-identical (T1); the post-demolish frame is deterministic. The flow's "pipe vanished mid-traversal → drop back to departure node (at_node, NOT p.src) + re-forward" path is what 2.3 makes LIVE.
- BIDIRECTIONAL-DRAW CARRY-FORWARD — test_reverse_draw_is_bidirectional (draw both pipes reversed, assert delivery) must be present + real + passing. It is in the diff.
- T2 PIXELS DEFERRED per the rlsw-harness gap (documented carry-forward, NOT a defect). demolish.dem pins post-demolish state via T1 hashes + the replay gate. Do NOT flag "T2 pixel not verified" as a blocker.
- CORE ENGINE-FREE (ODN-1) — zero engine/raylib imports in package core. Em-dashes are FINE in Packet-Plumber copy (the RT CI ban does NOT apply to PP).
- The base is `v2` (slice 1 + 2.1 bundles + 2.2 ECMP IN), NOT main. The prototype is REFERENCE-ONLY (its routing was NOT the locked model). Do NOT re-open 1.1–2.2 findings (merged, Perkins-verified) — carry-forward only.

## Legitimate findings here WOULD be
- A cached-route / spawn-time-route path (violates E29; the prototype's BFS sneaking back) — blocker.
- A hard cut on a bundle-member demolish (traffic stops when the pool should shrink) — blocker [E1].
- A terminal demolish accepted (or the typed error missing) — blocker [E2].
- A junction demolish that's non-atomic / wrongly ordered / non-deterministic / bumps gen per-entity — blocker [E27].
- A determinism break (a demolish mid-traversal replays differently; the re-forward not in the hash path; the demolish not action-logged; an Odin `map` iteration in core) — blocker.
- The bidirectional-draw carry-forward missing or fake — finding.
- An engine/raylib type leaking into `package core` (ODN-1) — blocker.
- A bug visible in the diff, an unhandled edge path, a serialization round-trip gap, a real coverage gap.
- A replay/log-read regression (the new command tags 2/3; truncation/unknown-tag rejection still holds).

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

Test-coverage analysis via traceability. For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Behaviours to trace (the demolish contracts): E2 terminal rejected; E27 junction atomic batch (incident-pipe order + trivial-no-incident case); E1 graceful shrink + full-bundle-loss drops; E29 re-forward at departure (not origin) + reroute-via-survivor delivery; E11 ids monotonic/never-recycled; missing/dead target typed rejections (.Missing_Pipe/.Missing_Node); replay byte-identical over a demolish mid-traversal (the T1 keystone); binary round-trip of the new tags (truncation/unknown-tag rejection); the bidirectional-draw carry-forward; the cull of packets stranded at a tombstoned node.

Blind-spot checks: is the E27 incident-pipe ORDER actually asserted (not just the count)? Is the E29 departure-vs-origin distinction asserted with the real node ids? Does any test exercise a demolish of a node with >2 incident pipes (a non-trivial batch)?

Finally, emit ONE additional finding for the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"; severity: PASS→note, CONCERNS→warning, FAIL→blocker
- detail: rationale with coverage read; recommended_fix: what would raise the gate.
Gate thresholds: PASS = P0 100%, P1 >=90%, overall >=80%; CONCERNS = P0 100%, P1 80–89%, overall >=80%; FAIL = P0 <100%, or P1 <80%, or overall <80%.
`source` = "tests".

## DONE
Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.3-demolish/r1/tests.json` and stop. Do not fix anything. Do not run the interactive fix flow.
