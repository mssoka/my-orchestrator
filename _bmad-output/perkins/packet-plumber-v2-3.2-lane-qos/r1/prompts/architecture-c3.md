# Perkins lens prompt — architecture (chunk 3 of 3 — goldens, round 1)

**You are the `architecture` lens. Your assigned `source` tag is `architecture`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/architecture-c3.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — chunk 3 of 3 — goldens, 4604 lines, 23 files (review exactly these bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/chunk3.patch
- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha 7c07a80): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.2-lane-qos-r1
- SPEC / CONTEXT (read the sections named; full files):
  - Perkins briefing (your charter + lens-guards): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/spec/job-briefing.md
  - Story 3.2 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/spec/stories-v2.md (the Story 3.2 card ~line 255; slice-3 framing above it)
  - Implementation spec (the minion's own frozen spec — acceptance matrix + code map): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/spec/spec-3-2-lane-qos.md
  - Architecture invariants: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/spec/odin-architecture-v1.md — ODN-3 QoS-inside-Flow (~line 474), ODN-5 data-driven catalogs (~line 522), ODN-11 save = seed + action log (~line 687), §11.7 edge-case table (line 1592; E5/E6/E8 at ~1600-1606, E10 at ~1609)
  - GDD: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/spec/gdd.md — M2 packet types & QoS lanes (all traffic starts Standard; player engineers QoS; 3 lanes by design, DiffServ-faithful)


## The PR (scope)
v2 Story 3.2 — 3-lane QoS + emphasis dial (the goldens wave). Chunk 3 of 3: the golden-manifest wave — T1 hash manifests (.t1), binary replay logs (.log.bin), and the NEW T2 PNG captures for qos_emphasis. Context: adding lane_presets to balance.json changed the folded catalog_hash for EVERY demo (c59e720ff6ac3fb4 → c403567796188e5b), and the new sparse QoS state sections ride the T1 state hash — so ALL 9 legacy .t1/.log.bin goldens were RE-BLESSED, deliberately, through ODN-11's defined gate (see the re-bless guard — Perkins independently verified the proof; do NOT re-flag it). The new qos_emphasis golden (goldens/qos_emphasis.t1, .log.bin, 01000ms/05000ms/12000ms.png) pins the emphasis-dial demo (demos/qos_emphasis.dem: seed 3003, run 15000ms = 300 ticks @20Hz, era 3, fixture qos; emphasis express_heavy at 3000ms + streaming→Express override on pipe 1; best_effort_heavy at 9000ms; captures at 1000/5000/12000ms).

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- **🚨 THE ODN-11 RE-BLESS — PROVEN, DO NOT AUTO-FLAG.** The story's rule says "existing goldens must not shift — if one does, STOP and flag, do not re-bless". The minion DID re-bless all 9 existing demos' .t1/.log.bin (catalog_hash c59e720ff6ac3fb4 → c403567796188e5b) — deliberately, through ODN-11's defined gate, and Perkins has INDEPENDENTLY VERIFIED the two-part proof at 7c07a80: (a) T2 pixels — no existing PNG changed in the diff AND `harness run` passes all 9 existing demos' T2 checks byte-identical against the unchanged PNGs; (b) reconstruction — a sandbox splice-proof replayed all 9 OLD logs with the NEW code forcing the OLD catalog_hash into the run state and reproduced every old .t1 hash bit-for-bit (incl. qos.dem's 1500 ticks). Zero sim behavior changed. A re-bless WITHOUT a real proof, or with evidence of drift, would be a BLOCKER — here it is NOT a finding.
- **🚨 [E5]/[E6]/[E8] EDGE CONTRACTS — load-bearing.** All-zero weights → catalog default preset [E5]; a never-drop class lane is FLOORED and a zeroing edit that would floor it is REJECTED [E6] (bus-side rejection test-pinned — Perkins neutralized the guard and test_qos_bus_rejections_e6 went red); largest-remainder distribution passes [E8]. A missing/broken edge contract = a blocker.
- **WEIGHT-ONLY [ODN-3] — demand is NOT an input.** The allocator takes lane weights only; a demand input sneaking into the lane resolution = a real defect. QoS procs live INSIDE Flow (not a peer system) — do NOT flag "QoS not a separate system" (established 3.1 guard).
- **REPLAY DETERMINISM [E10] + LOG_VERSION.** LOG_VERSION stays 2 — the new wire tags 4/5 are ADDITIVE per the merged 2.3 precedent (core/demolish_test.odin:413 documents the convention: "LOG_VERSION stays 2 — the new tags are ADDITIVE (an old draw-only log still parses)"). Old logs parse under the new code (verified: the splice proof reads them); an old binary rejects a new log cleanly (unknown tag → parse failure, verified at base). Do NOT flag "no LOG_VERSION bump". Do NOT flag "3.5's version collision" — the 3.5-vs-3.2 version collision at merge time is a merge-order concern (Silas flagged it), NOT a defect in this PR (3.5 is unmerged; this PR's base is pre-3.5 v2).
- **ZERO SIM BEHAVIOR CHANGE — VERIFIED** (the splice proof above + drift suite + demo gates at 7c07a80). A sim-behavior change riding the re-bless would be a blocker — it does not exist here.
- **DATA-DRIVEN BALANCE [ODN-5].** Lane weights/presets live in data/balance.json (lane_presets + default_lane_preset), wired through the existing catalog pattern. A hardcoded weight where the catalog/balance file should decide = a real defect. All-zero presets are REJECTED at catalog load (a content bug — the E5 fallback is the allocator's guard, not a dial position); that rejection is the design, not a gap.
- **E6 FLOOR OVERSELl IS DEFINED.** qos_apply_floor may oversell the sum by a quantum per floored lane; capacity exhaustion is the defined truncation; both are documented in the spec's Design Notes + pinned in qos_test.odin. Do NOT flag it.
- **3.2 SCOPE ONLY.** 3.3 (qos_serialize, contention drops) and 3.4 (SLA) are separate stories — do NOT flag "serialization/drops/SLA not implemented". `flow.lane_caps` being consumed only by the readout/render in 3.2 is the design ("3.3's serialization consumes it").
- **The spec-3-2-lane-qos.md "existing goldens unchanged" line** refers to behavioral stability (sparse serialization = zero QoS bytes on default runs; pixel-identical default renders). The catalog_hash shift is ODN-11's DEFINED re-bless trigger (balance.json content added) — see the first guard. Do NOT flag the docs' wording as a spec violation.
- **No re-open of 3.1 findings** (merged + Perkins-approved) **or 3.5's** (approved, unmerged — not in this base) — carry-forward only. The base is `v2` (slices 1–2 + 3.1; the harness #29 Demo_Replay single-source + era-in-log-header semantics are in base).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **Possible bmad-tooling quirk (context, not a finding):** the minion's edits briefly mis-resolved to the main checkout; Silas syncs it. Review the PR content as-is at the sha.

## Legitimate findings here WOULD be
- **A .t1 whose header doesn't match its demo** (ticks ≠ run_ms × logic_hz/1000; wrong seed; the qos_emphasis.t1 not era-3 — note: era rides the .log.bin header, not the .t1).
- **catalog_hash inconsistency** — every demo's .t1 MUST carry the SAME new hash (c403567796188e5b); a demo that DIDN'T change its catalog_hash is a stale bless; a demo with a DIFFERENT hash is an inconsistency.
- **A hash-manifest line count ≠ the header's ticks.**
- **Legacy goldens whose hash lines DIDN'T change** even though catalog_hash + the QoS sections changed (a stale/incomplete re-bless hides a real divergence) — or legacy demos whose seeds/ticks changed (they must not; all 9 legacy manifests keep their old seed/ticks/demo names).
- **The qos_emphasis golden incomplete**: .log.bin missing, .t1 missing, fewer than 300 hash lines, captures at 1000/5000/12000ms absent.
- **Binary .log.bin files that shrank to 0** or are missing for any demo with a .t1.
- Note: PNG pixel content is NOT reviewable from this diff (binary); the qos_emphasis PNGs being new + existing demos' PNGs NOT re-captured is EXPECTED and verified (the default render is byte-identical). Do not flag "no PNGs changed".

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
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation, ODN-3 QoS-inside-Flow, ODN-5 data-driven catalogs, ODN-13 no globals, ODN-10 arrays-only)?
- Will it create technical debt or make future changes harder (3.3 serialization / 3.4 SLA build directly on this)?
- Does complexity match the problem? Any premature abstraction?

`source` = "architecture".

## DONE
Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/architecture-c3.json` and stop. Do not fix anything. Do not run the interactive fix flow.
