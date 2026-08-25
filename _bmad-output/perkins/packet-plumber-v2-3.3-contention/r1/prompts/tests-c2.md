# Perkins lens prompt — tests (chunk 2 of 5 — spec+app+harness+demos, round 1)

**You are the `tests` lens. Your assigned `source` tag is `tests`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/tests-c2.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — chunk 2 of 5 — spec+app+harness+demos, 1050 lines, 6 files (review exactly these bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/c2.patch
- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha ffc9b7b): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.3-contention-r1
- SPEC / CONTEXT (read the sections named; full files):
  - Perkins briefing (your charter + lens-guards): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/spec/job-briefing.md
  - Story 3.3 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/spec/stories-v2.md (Story 3.3 card ~line 275; slice-3 framing above it)
  - Implementation spec (the minion's own frozen spec — acceptance matrix + code map): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/spec/spec-3-3-contention.md (the diff's first file; identical to the worktree copy)
  - Architecture invariants: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/spec/odin-architecture-v1.md — ODN-3 QoS-inside-Flow (~line 474), ODN-11 save = seed + action log (~line 687), §11.7 edge-case table (line 1592; E7/E9/E10/E22 at ~1604-1619), §6.2 per-link buffering (line ~964)
  - Canon commits (BOTH MERGED INTO BASE v2 — reviewed as canon, not as this PR's findings): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/spec/canon-2e3acab.patch (spatial lanes) + /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/spec/canon-8ece056.patch (no auto lanes + lane-speed)


## The PR (scope)
v2 Story 3.3 — the app/harness/docs wave (chunk 2 of 5): the spatial-lane canon render (app/render/view.odin — bundle_lane_caps_view, Lane_Bands, lane_bands, three painted lane strokes per pipe with width = WFQ share, packets laterally offset into their lane riding end-to-end AT LANE SPEED: Express streaks / Standard cruises / Best-effort crawls; a zero-share lane draws no stroke; app/render/palette.odin + data/palette.json lane colors), the harness demo directive lowering (harness/demo.odin, harness/run.odin), the new launchable demos/qos_contention.dem (pipe 0 oversubscribed ~2.4×), and the implementation spec _bmad-output/implementation-artifacts/spec-3-3-contention.md (frozen spec — the diff's first file). Chunks 1 (core), 3/4/5 (goldens) are SEPARATE lens waves — do not review them here.

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- **🚨 THE ODN-11 RE-BLESS — THE load-bearing invariant (verify the REASONS, don't auto-flag).** The minion re-blessed goldens DELIBERATELY with THREE documented reasons: (a) catalog_hash header drift — new balance.json keys (the 3.2 precedent); (b) the canon T2 repaint — all pipe demos (spatial lanes); (c) genuine contention shifts in qos/qos_emphasis/ecmp. VERIFY each reason holds at the byte level: the light demos (non-contention) must show ZERO sim change (only the catalog_hash header line shifts in their .t1), and the re-bless must be documented in the PR/spec (it is — spec-3-3-contention.md documents all three). A re-bless whose documented reason doesn't hold, or evidence of unaccounted drift (a light demo with per-tick shifts, a silent PNG change) = a BLOCKER.
- **🚨 SPATIAL-LANE CANON (2e3acab + 8ece056 — BOTH MERGED INTO BASE v2, user rulings 2026-08-12).** Three painted lane strokes per pipe; stroke width = WFQ allocation share; packets ride IN their lane (lateral offset) end-to-end AT LANE SPEED (Express streaks, Standard cruises, Best-effort crawls). **NO auto-assigned QoS lanes** — every packet type rides Standard until the player categorizes it (per-type/per-pipe override); the game NEVER assigns lanes; default pipe = all traffic on Standard (plain router). A render that assigns lanes, lacks the lane strokes, or mis-maps lane position/speed = a real defect. Do NOT flag "uncategorized packets are all on Standard" — that's the design.
- **🚨 [E9] CONTENTION LADDER — load-bearing.** A full lane queue sheds the lowest-priority NON-EMPTY lane's NEWEST packet (walk BE→S→E); the arriving packet drops when it IS the target. All 21 combos must be test-pinned. A shed that hits the wrong lane/priority, or a drop when a shed was possible = a blocker.
- **🚨 [E22] POOL BACKSTOP — strict-priority rule.** An Express resident NEVER pays for a Standard arrival (the inversion catch). A priority inversion (lower-class arrival evicting a higher-class resident) = a blocker.
- **[E7] NO-STARVATION FLOOR.** Work-conserving gap-fill; a lone packet in ANY lane crosses at full capacity. Starvation under continuous Express = a blocker. The light demos' transits unchanged (pinned) — verify the pins are real.
- **SERIALIZATION / REPLAY [E10].** LOG_VERSION stays 3 (events are tag-conditional; zero new serialized state). Same seed + same commands → identical map; Packet_Dropped events replay byte-identically. A serialization change that bumps state shape (or breaks old-log acceptance) WITHOUT the documented mechanism = a blocker.
- **Zero new serialized state (claimed).** Queues/lanes/budgets are DERIVED — verify no hidden serialized field crept in (no new Packet fields, no new Flow_State fields).
- **No re-open of 3.1/3.2 findings** (merged + Perkins-approved; 3.2's re-bless proven independently) — carry-forward only. The canon commits are IN BASE (reviewed as canon, not as this PR's findings).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–3 + harness + 3.5 + 3.2 + both canon commits).
- **E29 severance semantics preserved exactly** — demolish's silent cull stays silent (no severance Packet_Dropped event); do NOT flag "demolish drops are silent".
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha.

## Legitimate findings here WOULD be
- **A canon render violation** (2e3acab/8ece056): missing lane strokes, stroke width not ∝ WFQ share, no lateral packet offset, lane speed not mapped (Express fastest / Best slowest), auto-assigned lanes anywhere, a zero-share lane drawing a stroke (should draw none — base pipe shows through), a queued packet NOT in its lane — a blocker.
- **A harness directive bug**: new directive lowering errors (unknown class/lane/pipe not failing loudly), intent_apply_tick math, leaks in the new delete paths, the demos/qos_contention.dem authoring (pipe 0 oversubscribed ~2.4×: pipe ids vs draw order, capture times vs directives, era/fixture).
- **A data bug in balance.json/palette.json**: lane_queue_packets/pool_max_packets missing or out of range, palette lane keys missing fallbacks, lane colors identical to an existing semantic color (color is never the sole encoder).
- **A docs/scope drift**: the implementation spec claiming something the code does not do, or the code doing something the frozen spec forbids (e.g. new player commands, LOG_VERSION bump, 3.4 SLA work, severance-drop events, per-class bandwidth_demand, LB mechanics).
- **An `odin build` failure** at ffc9b7b (app + harness — Perkins built both green).

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

The P0 critical paths here: the E7 no-starvation floor (WRR budget + lone-packet full-capacity), the E9 drop ladder (ALL 21 emptiness combos pinned; wrong-lane shed / wrong-priority target / drop-when-shed-possible), the E22 pool backstop (strict-priority rule — Express resident never pays for a Standard arrival; double-shed duplicate-splice-index pin), replay byte-identity with Packet_Dropped events [E10], the tag-conditional serialization pin (pre-3.3 event bytes unchanged), the light-demo transit pins (E7 floor keeps light demos byte-identical), the new balance.json keys' fail-fast validation, and the qos_contention golden (T1 + T2 + replay gate).

Blind-spot heuristics to check:
- New/modified behavior without matching coverage
- Happy-path-only coverage where error handling is implied (e.g. the new balance keys' fail-fast cases — are they TESTED?)
- New state transitions without boundary tests (queue-full boundary at exactly lane_queue_packets)

Test level mix: flag mismatches as findings.

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
Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/tests-c2.json` and stop. Do not fix anything. Do not run the interactive fix flow.
