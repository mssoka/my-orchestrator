#!/usr/bin/env python3
"""Generate the 21 Perkins lens prompts for packet-plumber-v2-3.2-lane-qos r1 (3 chunks)."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.2-lane-qos-r1"
SHA = "7c07a80"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): {OUT}/spec/job-briefing.md
  - Story 3.2 card: {OUT}/spec/stories-v2.md (the Story 3.2 card ~line 255; slice-3 framing above it)
  - Implementation spec (the minion's own frozen spec — acceptance matrix + code map): {OUT}/spec/spec-3-2-lane-qos.md
  - Architecture invariants: {OUT}/spec/odin-architecture-v1.md — ODN-3 QoS-inside-Flow (~line 474), ODN-5 data-driven catalogs (~line 522), ODN-11 save = seed + action log (~line 687), §11.7 edge-case table (line 1592; E5/E6/E8 at ~1600-1606, E10 at ~1609)
  - GDD: {OUT}/spec/gdd.md — M2 packet types & QoS lanes (all traffic starts Standard; player engineers QoS; 3 lanes by design, DiffServ-faithful)"""

SCOPE_C1 = """v2 Story 3.2 — 3-lane QoS + emphasis dial (OPENS the QoS differentiator): per-class lanes (E→S→B) with a WEIGHT-ONLY integer-WFQ allocator (demand is NOT an input) living INSIDE Flow [ODN-3]; all-zero weights fall back to the catalog default preset [E5]; a never-drop class lane is floored and a zeroing edit that would floor it is REJECTED [E6]; the largest-remainder distribution test passes [E8]. New pure procs in core/qos.odin (qos_allocate / qos_lane_of / qos_pipe_weights / qos_pipe_never_drop / qos_apply_floor / qos_pipe_caps); Topology-owned per-pipe data (pipe_weights + flat lane-override list, purged on demolish); new logged commands Cmd_Set_Emphasis + Cmd_Set_Lane (validate→apply in topology.odin); SPARSE + absent-when-empty QoS sections in the T1 state writer (serialize.odin); the derived per-pipe lane_caps buffer rebuilt in flow_step on gen change (flow.odin — NEVER serialized); balance.json lane_presets loading + fail-fast validation (catalog.odin); the E5/E6/E8 test pins + sparse-contract pin + replay byte-identity pin (qos_test.odin, catalog_test.odin, determinism_test.odin).
Files in THIS chunk (chunk 1 of 3 — core): core/catalog.odin, core/catalog_test.odin, core/determinism_test.odin, core/flow.odin, core/qos.odin (NEW), core/qos_test.odin (NEW), core/serialize.odin, core/topology.odin, core/types.odin. Chunks 2 (app/harness/data/docs) and 3 (goldens) are SEPARATE lens waves — do not review them here."""

SCOPE_C2 = """v2 Story 3.2 — 3-lane QoS + emphasis dial (the app/harness/data wave). Chunk 2 of 3: the emphasis-dial UI (app/main.odin: pipe hit-testing, selection, right-click dial cycle, per-class lane keys 1/2+E/S/B, the lane-proportions readout + rejection toast), the lane-stripe render + selected-pipe halo (app/render/view.odin, palette.odin + data/palette.json), the balance.json lane_presets data (balanced 1:1:1 / express_heavy 4:2:1 / best_effort_heavy 1:2:4), the new qos_emphasis.dem demo (the T2 "lane proportions changing" golden), the harness emphasis/lane demo directives + lowering (harness/demo.odin, run.odin), and the doc artifacts (_bmad-output: spec-3-2-lane-qos.md, epic-2-context.md, deferred-work.md + .gitignore). Chunks 1 (core) and 3 (goldens) are SEPARATE lens waves — do not review them here."""

SCOPE_C3 = """v2 Story 3.2 — 3-lane QoS + emphasis dial (the goldens wave). Chunk 3 of 3: the golden-manifest wave — T1 hash manifests (.t1), binary replay logs (.log.bin), and the NEW T2 PNG captures for qos_emphasis. Context: adding lane_presets to balance.json changed the folded catalog_hash for EVERY demo (c59e720ff6ac3fb4 → c403567796188e5b), and the new sparse QoS state sections ride the T1 state hash — so ALL 9 legacy .t1/.log.bin goldens were RE-BLESSED, deliberately, through ODN-11's defined gate (see the re-bless guard — Perkins independently verified the proof; do NOT re-flag it). The new qos_emphasis golden (goldens/qos_emphasis.t1, .log.bin, 01000ms/05000ms/12000ms.png) pins the emphasis-dial demo (demos/qos_emphasis.dem: seed 3003, run 15000ms = 300 ticks @20Hz, era 3, fixture qos; emphasis express_heavy at 3000ms + streaming→Express override on pipe 1; best_effort_heavy at 9000ms; captures at 1000/5000/12000ms)."""

GUARDS = """- **🚨 THE ODN-11 RE-BLESS — PROVEN, DO NOT AUTO-FLAG.** The story's rule says "existing goldens must not shift — if one does, STOP and flag, do not re-bless". The minion DID re-bless all 9 existing demos' .t1/.log.bin (catalog_hash c59e720ff6ac3fb4 → c403567796188e5b) — deliberately, through ODN-11's defined gate, and Perkins has INDEPENDENTLY VERIFIED the two-part proof at 7c07a80: (a) T2 pixels — no existing PNG changed in the diff AND `harness run` passes all 9 existing demos' T2 checks byte-identical against the unchanged PNGs; (b) reconstruction — a sandbox splice-proof replayed all 9 OLD logs with the NEW code forcing the OLD catalog_hash into the run state and reproduced every old .t1 hash bit-for-bit (incl. qos.dem's 1500 ticks). Zero sim behavior changed. A re-bless WITHOUT a real proof, or with evidence of drift, would be a BLOCKER — here it is NOT a finding.
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
- **Possible bmad-tooling quirk (context, not a finding):** the minion's edits briefly mis-resolved to the main checkout; Silas syncs it. Review the PR content as-is at the sha."""

LEGIT_C1 = """- **A broken edge contract**: [E5] all-zero fallback wrong/missing, [E6] floor not applied or zeroing edit not rejected on some path, [E8] distribution math wrong (remainder/tie-order bug, sum != capacity) — a blocker.
- **A demand input in the lane resolution / allocation** (weight-only violated) — a blocker [ODN-3].
- **A determinism break [E10]**: an unseeded draw in the QoS paths, non-deterministic serialization (unordered walk of a map; a section whose presence depends on non-serialized state), a purge/override path that diverges between live and replay, a missed state_hash caller, a sparse-section inconsistency (a default pipe serializing QoS bytes; section ordering unstable).
- **Integer overflow in the allocator math** (i64 sums/remainders — e.g. c*w_i overflowing i64 for in-domain weights; caps truncation), or an index-out-of-bounds reachable in qos_pipe_caps/qos_lane_of/qos_pipe_never_drop (pipe_tier/pipe_slot/class indices).
- **A hardcoded weight/preset where balance.json should decide** — a real defect [ODN-5].
- **A catalog validation gap** in the new lane_presets loader (out-of-range/negative/duplicate accepted that the ODN-5 fail-fast bar should reject; a narrowing cast before range check).
- **An E6 validation inconsistency**: validate_set_emphasis and validate_set_lane resolving never-drop bindings differently than flow_step (the guard and floor must agree on which lane is protected).
- **An `odin test` / `odin build` / harness failure at 7c07a80** (Perkins ran these green — if you find a failure, it is a blocker; re-run to confirm before filing).
- **A real bug visible in the diff**: wrong floor-budget math, override-list purge bug, gen-trigger miss (lane_caps not rebuilt when it should), apply without validate assumptions broken."""

LEGIT_C2 = """- **A dial/UI logic bug**: cycle_emphasis wrapping/index math, pipe_hit point-to-segment errors, selection staleness, the readout showing stale data (using flow.lane_caps instead of fresh qos_pipe_caps is EXPLICITLY designed — do not flag it), a rejection toast never clearing.
- **A live-vs-replay divergence in the app edit path**: the app's fast-path apply + logged command (apply_tick = app.tick + 1) — a mismatch between what the app applies and what the log records would break replay determinism.
- **A harness directive bug**: intent_apply_tick_raw math vs the draw/demolish convention (intent_apply_tick), emphasis/lane lowering errors (unknown preset/class/lane not failing loudly), the fixed group-order (draws → demolishes → emphasis → lanes) creating a same-tick hazard the docs don't cover, a leak in the new delete paths (demo.emphasis/demo.lanes in the loaders).
- **A data bug in balance.json/palette.json**: a preset outside 0..MAX_WEIGHT, duplicate weights/id, a default_lane_preset that doesn't resolve, a palette key missing its fallback, lane colors identical to an existing semantic color (color is never the sole encoder).
- **A demo bug**: qos_emphasis.dem authoring errors (pipe ids vs draw order, capture times vs directive times, era/fixture mismatches).
- **A docs/scope drift**: the implementation spec or deferred-work claiming something the code does not do (or the code doing something the frozen spec forbids — e.g. touching 3.5 placement files, hardcoded weights, new peer systems, maps/globals/float sim state in core).
- **An `odin build` failure** at 7c07a80 (app + harness — Perkins built both green)."""

LEGIT_C3 = """- **A .t1 whose header doesn't match its demo** (ticks ≠ run_ms × logic_hz/1000; wrong seed; the qos_emphasis.t1 not era-3 — note: era rides the .log.bin header, not the .t1).
- **catalog_hash inconsistency** — every demo's .t1 MUST carry the SAME new hash (c403567796188e5b); a demo that DIDN'T change its catalog_hash is a stale bless; a demo with a DIFFERENT hash is an inconsistency.
- **A hash-manifest line count ≠ the header's ticks.**
- **Legacy goldens whose hash lines DIDN'T change** even though catalog_hash + the QoS sections changed (a stale/incomplete re-bless hides a real divergence) — or legacy demos whose seeds/ticks changed (they must not; all 9 legacy manifests keep their old seed/ticks/demo names).
- **The qos_emphasis golden incomplete**: .log.bin missing, .t1 missing, fewer than 300 hash lines, captures at 1000/5000/12000ms absent.
- **Binary .log.bin files that shrank to 0** or are missing for any demo with a .t1.
- Note: PNG pixel content is NOT reviewable from this diff (binary); the qos_emphasis PNGs being new + existing demos' PNGs NOT re-captured is EXPECTED and verified (the default render is byte-identical). Do not flag "no PNGs changed"."""

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

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability, off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing. `source` = "edge".""",

"acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). `source` = "acceptance".""",

"security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a single-player desktop game core (Odin) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories will not apply; the realistic surface here is unsafe deserialization / missing validation at the JSON-catalog + replay-log + demo-parser boundaries (the demo parser's strconv paths, the log_read tag switch, the lane_presets loader) and integer-overflow/coercion at parse. `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation, ODN-3 QoS-inside-Flow, ODN-5 data-driven catalogs, ODN-13 no globals, ODN-10 arrays-only)?
- Will it create technical debt or make future changes harder (3.3 serialization / 3.4 SLA build directly on this)?
- Does complexity match the problem? Any premature abstraction?

`source` = "architecture".""",

"codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

`source` = "codebase".""",

"tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

The P0 critical paths here: the E5/E6/E8 edge contracts (each must be test-pinned — E6 has TWO faces: the floor AND the bus rejection), weight-only allocation [ODN-3], replay byte-identity with the new commands [E10], the sparse-serialization golden-stability pin, the catalog fail-fast validation for lane_presets [ODN-5], and the qos_emphasis golden (T1 + T2 + replay gate).

Blind-spot heuristics to check:
- New/modified behavior without matching coverage
- Happy-path-only coverage where error handling is implied (e.g. lane_presets fail-fast cases — are they TESTED?)
- New state transitions without boundary tests

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

`source` = "tests".""",
}

TEMPLATE = """# Perkins lens prompt — @LENS@ (@CHUNK@, round 1)

**You are the `@LENS@` lens. Your assigned `source` tag is `@LENS@`. Your output file is `@OUTFILE@`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — @CHUNKDESC@ (review exactly these bytes): @DIFFPATH@
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

def build(lens, chunk):
    info = {
        "c1": ("chunk 1 of 3 — core", 1224, 10, "chunk1.patch"),
        "c2": ("chunk 2 of 3 — app+harness+data+docs", 1088, 14, "chunk2.patch"),
        "c3": ("chunk 3 of 3 — goldens", 4604, 23, "chunk3.patch"),
    }[chunk]
    desc, lines, files, patch = info
    diffpath = f"{OUT}/{patch}"
    chunkdesc = f"{desc}, {lines} lines, {files} files"
    outfile = f"{OUT}/{lens}-{chunk}.json"
    if lens == "blind":
        wtline = ""
        specline = ""
    else:
        wtline = f"- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha {SHA}): {WT}\n"
        specline = f"- SPEC / CONTEXT (read the sections named; full files):\n{SPEC_BLOCK}\n"
    scope = {"c1": SCOPE_C1, "c2": SCOPE_C2, "c3": SCOPE_C3}[chunk]
    legit = {"c1": LEGIT_C1, "c2": LEGIT_C2, "c3": LEGIT_C3}[chunk]
    t = TEMPLATE
    t = t.replace("@LENS@", lens)
    t = t.replace("@CHUNK@", desc)
    t = t.replace("@OUTFILE@", outfile)
    t = t.replace("@CHUNKDESC@", chunkdesc)
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
for chunk in ("c1", "c2", "c3"):
    for lens in ("blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"):
        p = f"{OUT}/prompts/{lens}-{chunk}.md"
        with open(p, "w") as f:
            f.write(build(lens, chunk))
        print(p, os.path.getsize(p))
