#!/usr/bin/env python3
"""Generate the Perkins lens prompts for packet-plumber-routing-bandwidth-cost r1 (10 chunks x 7 lenses)."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-bandwidth-cost-r1"
SHA = "32a1b65"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): {OUT}/spec/job-briefing.md
  - Canon (the user ruling that drives this job — PROBLEM DEFINITION, SUCCESS CRITERIA, RECOMMENDED SOLUTION): {OUT}/spec/problem-solution-2026-08-13.md
  - Frozen implementation spec (the minion's own spec — acceptance matrix + code map): {OUT}/spec/spec-routing-bandwidth-cost.md (the diff's second file; identical to the worktree copy)
  - Architecture invariants: {OUT}/spec/odin-architecture-v1.md — the routing spine (~line 666), ODN-9/ODN-10 determinism rules, §6.2 the locked routing model + the new capacity-cost model (~line 964), §10.2/§10.3 the golden-harness contract
  - GDD routing section: {OUT}/spec/gdd.md (the one-line player rule ~line 231)"""

SCOPE_C1 = """v2 Job A — capacity-cost routing (the 2026-08-13 canon amendment), chunk 1 of 10 — the spec/docs/core/data/demos wave. The PR replaces the locked routing model's unit-weight BFS with Dijkstra over STATIC per-tier integer pipe costs (data/pipe_tiers.json `cost` ladder 20/10/5 — narrow 5 u/s -> 20, standard 15 -> 10, wide 40 -> 5; NEVER dynamic utilization; flows prefer fat pipes; congestion avoidance stays the player's job). Equal END-TO-END cost -> ECMP (pure identity hash, UNCHANGED); unequal -> the fatter path wins. `routing_equal_cost_hops` API shape unchanged; the routing table stays DERIVED + NOT serialized into the T1 hash; `flow.odin`'s forward pass untouched (same (offset, count) lookup + ecmp_pick). Files in THIS chunk: _bmad-output/implementation-artifacts/{deferred-work.md, spec-routing-bandwidth-cost.md} (the frozen spec), _bmad-output/planning-artifacts/architecture/odin-architecture-v1.md (canon docs), gdd decision-log.md + gdd.md (player rule), core/catalog.odin (Pipe_Tier.cost field + jint_strict + cost>=1 validation), core/catalog_test.odin (tier reject rows), core/determinism_test.odin (test_catalog costs), core/routing.odin (BFS->Dijkstra — THE heart), core/routing_cost_test.odin (NEW — the 4 pins), core/step.odin (rebuild call site + cat), data/pipe_tiers.json (the ladder), demos/ecmp_cost.dem (NEW — two compact diamonds). Chunks c2-c7 (goldens) are SEPARATE lens waves — do not review them here."""

SCOPE_C2 = """v2 Job A — capacity-cost routing, chunk 2 of 10 — the small-goldens wave: goldens/boot|bundle|demolish|draw|ecmp|ecmp_cost (.t1 + .log.bin + the 2 NEW PNGs goldens/ecmp_cost/01150ms.png + 01450ms.png). Every re-bless is the MECHANICAL catalog_hash fold: adding `cost` to pipe_tiers.json changes cat.hash (8da858ab04b113db -> 0a6324230ab9dcba), which rides every per-tick state hash (byte 33 of the canonical dump) + the .log.bin header (8 bytes at offset 18). For THESE demos the re-bless must show ONLY: the catalog_hash header line + every per-tick hash line + the 8 .log.bin header bytes — NOTHING else (no seed/ticks drift, no added/removed tick lines). ecmp_cost is NEW (all files new). The PNGs are binary — not reviewable line-by-line; their existence + new-file status is the reviewable fact. Chunks c1 (code) and c3-c7 (other goldens) are SEPARATE lens waves."""

SCOPE_C3 = """v2 Job A — capacity-cost routing, chunk 3 of 10 — goldens/flow|lose|place (.t1 + .log.bin). Same mechanical catalog_hash fold as every re-blessed demo (old hash 8da858ab04b113db -> new 0a6324230ab9dcba): ONLY the catalog_hash header line, the per-tick hash lines, and the 8 .log.bin header bytes may shift. No seed/ticks drift, no tick-line count change, no added/removed lines. Chunks c1-c2 and c4-c7 are SEPARATE lens waves."""

SCOPE_C4 = """v2 Job A — capacity-cost routing, chunk 4 of 10 — goldens/qos (.t1 3011 lines + .log.bin). The LONGEST single golden. Same mechanical catalog_hash fold (8da858ab04b113db -> 0a6324230ab9dcba): ONLY the catalog_hash header line, the per-tick hash lines, and the 8 .log.bin header bytes may shift. qos.dem traffic is all standard-tier single-path — its ROUTING behavior is unchanged by the cost model (unit-weight BFS and 20/10/5 Dijkstra agree on single-path graphs), so its per-tick shifts must be pure catalog-hash fold. Verify: header fields, tick count 1500 == hash-line count, per-tick line numbering continuous 1..1500, no gaps/dupes/reorders. Chunks c1-c3 and c5-c7 are SEPARATE lens waves."""

SCOPE_C5 = """v2 Job A — capacity-cost routing, chunk 5 of 10 — goldens/qos_contention|qos_emphasis|sla (.t1 + .log.bin). Same mechanical catalog_hash fold (8da858ab04b113db -> 0a6324230ab9dcba): ONLY the catalog_hash header line, the per-tick hash lines, and the 8 .log.bin header bytes may shift. These are contention/lane demos — their routing is single-path or standard-tier, so the fold must be pure. Verify per-demo: header fields (demo/seed/logic_hz/tick counts 240/300/240), hash-line numbering continuous, no gaps/dupes. Chunks c1-c4 and c6-c7 are SEPARATE lens waves."""

SCOPE_C6 = """v2 Job A — capacity-cost routing, chunk 6 of 10 — goldens/surge (the .log.bin + a FRAGMENT of surge.t1 — see the CHUNK NOTE at the top of the fragment: surge.t1 is 8014 lines / 4000 ticks, split mid-hunk across c6a/c6b/c6c/c6d; THIS chunk covers the tick range named in its note). Same mechanical catalog_hash fold (8da858ab04b113db -> 0a6324230ab9dcba): ONLY the catalog_hash header line, the per-tick hash lines, and the 8 .log.bin header bytes may shift. surge.dem traffic is standard-tier (the 4.2 surge demo) — its routing behavior is unchanged by the cost model, so its per-tick shifts must be pure catalog-hash fold. Verify within the fragment: tick numbering continuous across the covered range, no gaps/dupes, all 4000 ticks accounted for across the four fragments. Chunks c1-c5 and c7 are SEPARATE lens waves."""

SCOPE_C7 = """v2 Job A — capacity-cost routing, chunk 7 of 10 — goldens/warn|win (.t1 + .log.bin; warn.t1 is 3011 lines). Same mechanical catalog_hash fold (8da858ab04b113db -> 0a6324230ab9dcba): ONLY the catalog_hash header line, the per-tick hash lines, and the 8 .log.bin header bytes may shift. warn is the 4.1 forecast demo (standard-tier traffic — routing unchanged), win is a light demo. Verify: header fields, tick counts (1500/60) == hash-line counts, numbering continuous, no gaps/dupes. Chunks c1-c6 are SEPARATE lens waves."""

GUARDS = """- **🚨 LOAD-BEARING — Dijkstra correctness + determinism (the one hard blocker).** (a) The algorithm must be Dijkstra over integer pipe costs: cheapest-first, array-backed, NO map iteration [ODN-10], NO floats, NO rng draws in routing; equal-cost condition `dist[v] + cost(pipe) == dist[u]`; the ECMP set = the neighbors satisfying it; `routing_equal_cost_hops` (offset, count) shape unchanged. (b) A wrong shortest-path (path cost != sum of tier costs) or a nondeterministic tie-break = a blocker. (c) The table stays a pure function of Topology, rebuilt only on topology change (rule 1), NOT serialized (rule 3) — the T1 hash is unchanged in WHAT it covers (the catalog_hash fold below is the only serialization delta).
- **🚨 LOCKED — do not flag as defects:** `ecmp_pick`/`ecmp_hash` (pure identity hash, spine rule 2 — unchanged by design); the table being derived-not-serialized; the forward pass reusing `(offset, count)` + `ecmp_pick`; static (never dynamic) costs; congestion avoidance being the player's job (QoS/engineering) — NOT routing's. The mixed-tier bundle pricing at its fattest member (min member cost) is the documented design — do not flag the pricing rule itself; flag only an INCONSISTENCY between pricing and the ECMP condition.
- **🚨 GOLDEN-DISCIPLINE — the splice proof is the claim to verify, and Perkins has ALREADY verified it mechanically (all 16 demos: the new golden is reproducible at this sha, and folding the OLD catalog_hash into the new dump's FNV reproduces the OLD golden exactly — fold-only, zero behavior shift; .log.bin diffs = exactly the 8 header bytes).** Do NOT file "every per-tick hash line changed" as a finding — that IS the fold. DO file: a re-bless beyond the fold (a demo whose non-hash lines changed — seed/ticks/demo name), a hash-line numbering gap/dupe/reorder, a missing .log.bin, a catalog_hash header inconsistent with 0a6324230ab9dcba, an existing golden whose header did NOT change (stale bless), or an existing T2 PNG changed (only ecmp_cost's PNGs are new files — any OTHER PNG in the diff = a real finding).
- **ODN-5 — the `cost` field:** integer, validated `cost >= 1` at catalog load (zero-cost edges would break the per-hop progress guarantee — reject at load; the minion claims fail-fast rows for 0/negative/missing/decimal). A zero/negative cost slipping load = a blocker.
- **The four core test contracts (must be pinned):** mixed-tier diamond picks the fat path as a UNIQUE next hop (no ECMP when costs differ); different-tier equal-sum tie -> ECMP set of 2 (S->R1 standard(10)+R1->D fast(5)=15 vs S->R2 fast(5)+R2->D standard(10)=15 TRUE tie); re-step determinism (byte-identical); ladder read from data (a data change moves behavior — ODN-5 wiring proof). A missing or broken pin = a finding.
- **Demo:** `demos/ecmp_cost.dem` captures the fat-path unique hop mid-flight AND the true different-tier tie split; `expect hash stable`. NEW golden files only.
- **Scope guard:** Job A ONLY — capacity-cost routing + the canon docs. NOT 4.3, NOT the other crisis archetypes, NOT Job B (readability assist) or Job C (forecast-shift) content, NO new player commands (LOG_VERSION stays 3 — a bump without a flag = flag it). Do not demand features B/C will add.
- **BASE = `v2`** (slices 1–3 + harness + 4.1 + 4.2 in — the 4.2 crisis engine is merged; carry-forward only; do NOT re-open 4.2 findings).
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical. The Dijkstra must be insertion-order deterministic on every target (no map iteration, no float, no rng)."""

LEGIT_C1 = """- **A Dijkstra correctness bug**: a wrong shortest path (dist values not equal to the true min cost path sum), the equal-cost condition wrong (`dist[v] + cost(pipe) != dist[u]` test malformed, or a neighbor with a CHEAPER-than-min member mis-priced), the ECMP set missing a true equal-cost neighbor or including a non-equal one, an empty ECMP set for a reachable node, a nondeterministic tie-break (map iteration, float compare, rng draw, order-dependent extraction), a mixed-tier bundle edge priced inconsistently with the per-pipe relaxation (the same edge must price at the same cost in both places), the representative-pipe recording breaking insertion-order stability.
- **An ODN-5 validation gap**: `cost` missing/0/negative/decimal slipping the load (jint_strict wrong-typed -> 0 -> must reject; decimals must reject); the reject rows not pinned; an out-of-bounds pipe_tier index reaching `cat.pipe_tiers[...]` (the draw path validates — verify).
- **A spine breach**: the routing table serialized into the T1 hash (it must stay derived); rebuild on a non-topology change; `ecmp_pick`/`ecmp_hash` modified; LOG_VERSION bumped; a new player command; `flow.odin` forward pass modified.
- **A broken/missing test pin**: any of the four contracts (fat-path unique, true different-tier tie ECMP 2, re-step determinism, ladder-read-from-data) absent or asserting the wrong thing.
- **A spec/code contradiction**: the frozen spec's line "edge cost = representative pipe's tier cost" vs the implemented MIN-member bundle pricing (decision-log/arch/code agree on min-member — if the spec wording contradicts the code, that is a doc-accuracy note); the canon docs (arch §6.2, GDD rule) contradicting the implemented model.
- **The ecmp_cost.dem authoring**: bad tier names, draws that don't match the described diamonds (A: wide/wide vs narrow/narrow; B: standard+wide vs wide+standard), capture times not matching the comments, spans exceeding narrow's max 10.
- **A real bug visible in the diff**: an index/type error, a leak introduced by the new code (the new failfast rows add catalogs_load error-path leaks — pre-existing pattern), the i32 dist overflow with pathological cost values (documented + deferred in deferred-work.md — note-level, not a blocker)."""

LEGIT_G = """- **A re-bless beyond the fold**: a non-hash line changed (demo name, seed, logic_hz, tick count), a hash-line numbering gap/dupe/reorder within the fragment, a tick line added/removed (the line count must equal the header's ticks), a catalog_hash header value other than 0a6324230ab9dcba, an OLD golden whose catalog_hash header did NOT change (stale bless), a .log.bin missing for a demo that has a .t1 (or vice versa).
- **For c2**: any PNG diff entry OTHER than the two NEW goldens/ecmp_cost/*.png files (an existing T2 changed = a real finding).
- **For c4/c7**: the big .t1s' tick numbering continuity across the whole file (1500/3011 lines).
- **For c6a-d**: continuity across the four fragments (ticks 1-4000 exactly once each); the fragment's CHUNK NOTE tick range must match the lines it covers.
- **Do NOT file**: per-tick hash lines changing (that IS the verified catalog_hash fold), the catalog_hash header changing (the fold), .log.bin binary diffs (Perkins verified exactly 8 header bytes per demo)."""

OUTPUT_CONTRACT = """Write ONLY a valid JSON array to your output file (named below). No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
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
}"""

ACCURACY = """ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer."""

BRIEFS = {
"blind": """You are a cynical, jaded reviewer with zero patience for sloppy work. BLINDNESS RULE: the diff file is ALL the context you may use. Do NOT read the worktree, the specs, or any other file — reading anything beyond the diff INVALIDATES your lens. Assume problems exist; be skeptical; look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (the comments / commit message)

Your `evidence` MUST be exact diff lines pasted verbatim from the diff file. `source` = "blind".""",

"edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), off-by-one errors, integer overflow/truncation in the new cost math, unhandled error paths in new code (the catalog reject rows), state the new code doesn't account for (unreachable nodes, dead pipes, zero nodes, tier index bounds, mixed-tier bundles), input the new code doesn't validate (cost magnitudes).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing. `source` = "edge".""",

"acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec (Job B/C content, new commands, LOG_VERSION bumps, 4.2 re-opens)

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). `source` = "acceptance".""",

"security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling
- Data exposure
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a single-player desktop game core (Odin) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories will not apply; the realistic surface here is the JSON-catalog boundary (the new `cost` field loader: jint_strict semantics, integer-overflow/coercion at parse — a crafted pipe_tiers.json) and the demo-parser tier-name resolution. `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules (e.g. routing now reading Catalogs — justified? clean?)
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (ODN-1 core purity, ODN-5 data-driven catalogs, ODN-10 arrays-only, ODN-13 no globals)?
- Will it create technical debt or make future changes harder (Jobs B/C build on this cost model)?
- Does complexity match the problem? Any premature abstraction?

`source` = "architecture".""",

"codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (jint_strict, pipe_tier_index, node_slot, pipe_other, routing_equal_cost_hops signatures)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
- Are all routing_rebuild call sites updated for the new `cat` parameter (exactly one caller — step.odin)?

`source` = "codebase".""",

"tests": """Test coverage analysis via traceability.

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

`source` = "tests".""",
}

TEMPLATE = """# Perkins lens prompt — @LENS@ (@CHUNKDESC@, round 1)

**You are the `@LENS@` lens. Your assigned `source` tag is `@LENS@`. Your output file is `@OUTFILE@`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — @CHUNKDESC2@ (review exactly these bytes): @DIFFPATH@
@WTLINE@@SPECLINE@

## The PR (scope)
@SCOPE@

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
@GUARDS@

## Legitimate findings here WOULD be
@LEGIT@

## OUTPUT CONTRACT (follow exactly)
@CONTRACT@

@ACCURACY@

## YOUR LENS BRIEF

@BRIEF@

## DONE
Write your JSON array to `@OUTFILE@` and stop. Do not fix anything. Do not run the interactive fix flow.
"""

CHUNKS = {
    "c1": ("chunk 1 of 10 — spec+docs+core+data+demos", 921, 13, "c1.patch", SCOPE_C1, LEGIT_C1),
    "c2": ("chunk 2 of 10 — small goldens + new ecmp_cost", 915, 15, "c2.patch", SCOPE_C2, LEGIT_G),
    "c3": ("chunk 3 of 10 — flow/lose/place goldens", 450, 6, "c3.patch", SCOPE_C3, LEGIT_G),
    "c4": ("chunk 4 of 10 — qos golden", 3014, 2, "c4.patch", SCOPE_C4, LEGIT_G),
    "c5": ("chunk 5 of 10 — contention/emphasis/sla goldens", 1602, 6, "c5.patch", SCOPE_C5, LEGIT_G),
    "c6a": ("chunk 6a of 10 — surge golden fragment (ticks 1-1000)", 2015, 2, "c6a.patch", SCOPE_C6, LEGIT_G),
    "c6b": ("chunk 6b of 10 — surge golden fragment (ticks 1001-2000)", 2001, 1, "c6b.patch", SCOPE_C6, LEGIT_G),
    "c6c": ("chunk 6c of 10 — surge golden fragment (ticks 2001-3000)", 2001, 1, "c6c.patch", SCOPE_C6, LEGIT_G),
    "c6d": ("chunk 6d of 10 — surge golden fragment (ticks 3001-4000)", 2001, 1, "c6d.patch", SCOPE_C6, LEGIT_G),
    "c7": ("chunk 7 of 10 — warn/win goldens", 3148, 4, "c7.patch", SCOPE_C7, LEGIT_G),
}

def build(lens, chunk):
    desc, lines, files, patch, scope, legit = CHUNKS[chunk]
    diffpath = f"{OUT}/{patch}"
    chunkdesc = f"{desc}, {lines} lines, {files} files"
    chunkdesc2 = f"{desc} ({lines} lines, {files} files)"
    outfile = f"{OUT}/{lens}-{chunk}.json"
    if lens == "blind":
        wtline = ""
        specline = ""
    else:
        wtline = f"- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha {SHA}): {WT}\n"
        specline = f"- SPEC / CONTEXT (read the sections named; full files):\n{SPEC_BLOCK}\n"
    t = TEMPLATE
    t = t.replace("@LENS@", lens)
    t = t.replace("@CHUNKDESC@", chunkdesc)
    t = t.replace("@CHUNKDESC2@", chunkdesc2)
    t = t.replace("@OUTFILE@", outfile)
    t = t.replace("@DIFFPATH@", diffpath)
    t = t.replace("@WTLINE@", wtline)
    t = t.replace("@SPECLINE@", specline)
    t = t.replace("@SCOPE@", scope)
    t = t.replace("@GUARDS@", GUARDS)
    t = t.replace("@LEGIT@", legit)
    t = t.replace("@CONTRACT@", OUTPUT_CONTRACT)
    t = t.replace("@ACCURACY@", ACCURACY)
    t = t.replace("@BRIEF@", BRIEFS[lens])
    return t

os.makedirs(f"{OUT}/prompts", exist_ok=True)
manifest = []
for chunk in ("c1", "c2", "c3", "c4", "c5", "c6a", "c6b", "c6c", "c6d", "c7"):
    for lens in ("blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"):
        p = f"{OUT}/prompts/{lens}-{chunk}.md"
        with open(p, "w") as f:
            f.write(build(lens, chunk))
        manifest.append([chunk, lens, p, f"{OUT}/{lens}-{chunk}.json"])
        print(p, os.path.getsize(p))

import json
with open(f"{OUT}/brief-manifest.json", "w") as f:
    json.dump(manifest, f, indent=1)
print("manifest:", len(manifest), "briefs")
