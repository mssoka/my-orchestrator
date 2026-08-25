# Perkins lens prompt — tests (chunk 2 of 10 — small goldens + new ecmp_cost, 915 lines, 15 files, round 1)

**You are the `tests` lens. Your assigned `source` tag is `tests`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/tests-c2.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — chunk 2 of 10 — small goldens + new ecmp_cost (915 lines, 15 files) (review exactly these bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/c2.patch
- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha 32a1b65): /Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-bandwidth-cost-r1
- SPEC / CONTEXT (read the sections named; full files):
  - Perkins briefing (your charter + lens-guards): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/spec/job-briefing.md
  - Canon (the user ruling that drives this job — PROBLEM DEFINITION, SUCCESS CRITERIA, RECOMMENDED SOLUTION): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/spec/problem-solution-2026-08-13.md
  - Frozen implementation spec (the minion's own spec — acceptance matrix + code map): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/spec/spec-routing-bandwidth-cost.md (the diff's second file; identical to the worktree copy)
  - Architecture invariants: /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/spec/odin-architecture-v1.md — the routing spine (~line 666), ODN-9/ODN-10 determinism rules, §6.2 the locked routing model + the new capacity-cost model (~line 964), §10.2/§10.3 the golden-harness contract
  - GDD routing section: /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/spec/gdd.md (the one-line player rule ~line 231)


## The PR (scope)
v2 Job A — capacity-cost routing, chunk 2 of 10 — the small-goldens wave: goldens/boot|bundle|demolish|draw|ecmp|ecmp_cost (.t1 + .log.bin + the 2 NEW PNGs goldens/ecmp_cost/01150ms.png + 01450ms.png). Every re-bless is the MECHANICAL catalog_hash fold: adding `cost` to pipe_tiers.json changes cat.hash (8da858ab04b113db -> 0a6324230ab9dcba), which rides every per-tick state hash (byte 33 of the canonical dump) + the .log.bin header (8 bytes at offset 18). For THESE demos the re-bless must show ONLY: the catalog_hash header line + every per-tick hash line + the 8 .log.bin header bytes — NOTHING else (no seed/ticks drift, no added/removed tick lines). ecmp_cost is NEW (all files new). The PNGs are binary — not reviewable line-by-line; their existence + new-file status is the reviewable fact. Chunks c1 (code) and c3-c7 (other goldens) are SEPARATE lens waves.

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- **🚨 LOAD-BEARING — Dijkstra correctness + determinism (the one hard blocker).** (a) The algorithm must be Dijkstra over integer pipe costs: cheapest-first, array-backed, NO map iteration [ODN-10], NO floats, NO rng draws in routing; equal-cost condition `dist[v] + cost(pipe) == dist[u]`; the ECMP set = the neighbors satisfying it; `routing_equal_cost_hops` (offset, count) shape unchanged. (b) A wrong shortest-path (path cost != sum of tier costs) or a nondeterministic tie-break = a blocker. (c) The table stays a pure function of Topology, rebuilt only on topology change (rule 1), NOT serialized (rule 3) — the T1 hash is unchanged in WHAT it covers (the catalog_hash fold below is the only serialization delta).
- **🚨 LOCKED — do not flag as defects:** `ecmp_pick`/`ecmp_hash` (pure identity hash, spine rule 2 — unchanged by design); the table being derived-not-serialized; the forward pass reusing `(offset, count)` + `ecmp_pick`; static (never dynamic) costs; congestion avoidance being the player's job (QoS/engineering) — NOT routing's. The mixed-tier bundle pricing at its fattest member (min member cost) is the documented design — do not flag the pricing rule itself; flag only an INCONSISTENCY between pricing and the ECMP condition.
- **🚨 GOLDEN-DISCIPLINE — the splice proof is the claim to verify, and Perkins has ALREADY verified it mechanically (all 16 demos: the new golden is reproducible at this sha, and folding the OLD catalog_hash into the new dump's FNV reproduces the OLD golden exactly — fold-only, zero behavior shift; .log.bin diffs = exactly the 8 header bytes).** Do NOT file "every per-tick hash line changed" as a finding — that IS the fold. DO file: a re-bless beyond the fold (a demo whose non-hash lines changed — seed/ticks/demo name), a hash-line numbering gap/dupe/reorder, a missing .log.bin, a catalog_hash header inconsistent with 0a6324230ab9dcba, an existing golden whose header did NOT change (stale bless), or an existing T2 PNG changed (only ecmp_cost's PNGs are new files — any OTHER PNG in the diff = a real finding).
- **ODN-5 — the `cost` field:** integer, validated `cost >= 1` at catalog load (zero-cost edges would break the per-hop progress guarantee — reject at load; the minion claims fail-fast rows for 0/negative/missing/decimal). A zero/negative cost slipping load = a blocker.
- **The four core test contracts (must be pinned):** mixed-tier diamond picks the fat path as a UNIQUE next hop (no ECMP when costs differ); different-tier equal-sum tie -> ECMP set of 2 (S->R1 standard(10)+R1->D fast(5)=15 vs S->R2 fast(5)+R2->D standard(10)=15 TRUE tie); re-step determinism (byte-identical); ladder read from data (a data change moves behavior — ODN-5 wiring proof). A missing or broken pin = a finding.
- **Demo:** `demos/ecmp_cost.dem` captures the fat-path unique hop mid-flight AND the true different-tier tie split; `expect hash stable`. NEW golden files only.
- **Scope guard:** Job A ONLY — capacity-cost routing + the canon docs. NOT 4.3, NOT the other crisis archetypes, NOT Job B (readability assist) or Job C (forecast-shift) content, NO new player commands (LOG_VERSION stays 3 — a bump without a flag = flag it). Do not demand features B/C will add.
- **BASE = `v2`** (slices 1–3 + harness + 4.1 + 4.2 in — the 4.2 crisis engine is merged; carry-forward only; do NOT re-open 4.2 findings).
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical. The Dijkstra must be insertion-order deterministic on every target (no map iteration, no float, no rng).

## Legitimate findings here WOULD be
- **A re-bless beyond the fold**: a non-hash line changed (demo name, seed, logic_hz, tick count), a hash-line numbering gap/dupe/reorder within the fragment, a tick line added/removed (the line count must equal the header's ticks), a catalog_hash header value other than 0a6324230ab9dcba, an OLD golden whose catalog_hash header did NOT change (stale bless), a .log.bin missing for a demo that has a .t1 (or vice versa).
- **For c2**: any PNG diff entry OTHER than the two NEW goldens/ecmp_cost/*.png files (an existing T2 changed = a real finding).
- **For c4/c7**: the big .t1s' tick numbering continuity across the whole file (1500/3011 lines).
- **For c6a-d**: continuity across the four fragments (ticks 1-4000 exactly once each); the fragment's CHUNK NOTE tick range must match the lines it covers.
- **Do NOT file**: per-tick hash lines changing (that IS the verified catalog_hash fold), the catalog_hash header changing (the fold), .log.bin binary diffs (Perkins verified exactly 8 header bytes per demo).

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

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

The P0 critical paths here: the Dijkstra correctness (fat-path unique hop; the TRUE different-tier equal-sum tie -> ECMP set of 2; equal-cost condition exactness), the ODN-5 validation (cost 0/negative/missing/decimal all reject), re-step determinism over the cost model, the ladder-read-from-data wiring, the mixed-tier bundle min-cost pricing (is there a pin? the four contracts do NOT cover a mixed-tier BUNDLE — only mixed-tier paths), and the i32 overflow guard (documented as deferred).

Blind-spot heuristics to check:
- New/modified behavior without matching coverage (e.g. a node with parallel mixed-tier pipes to a neighbor — no test)
- Happy-path-only coverage where error handling is implied (the reject rows — are they TESTED? yes, catalog_test.odin)
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

`source` = "tests".

## DONE
Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/tests-c2.json` and stop. Do not fix anything. Do not run the interactive fix flow.
