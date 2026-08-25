#!/usr/bin/env python3
"""Generate the 14 Perkins lens prompts for packet-plumber-v2-3.1-packet-types r2."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r2"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.1-packet-types-r2"
SHA = "abe578b"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards, ROUND 2): {OUT}/spec/perkins-briefing-r2.md
  - Job briefing (the implementing minion's spec): {OUT}/spec/job-briefing.md
  - Story 3.1 card + slice-3 framing: {OUT}/spec/stories-v2.md (slice-3 framing ~line 228, the Story 3.1 card ~line 233)
  - v1 demand model (the design being ported): {OUT}/spec/sprint-plan-v1.md §3 (lines 126-332 — §3.1 PressurePlan/DemandSpec/SetPiece structure, §3.2 typed source→sink mapping, §3.3 the WEIGHTED_RANDOM dst-selection rule + its pinned test, §3.4 player visibility)
  - Architecture invariants: {OUT}/spec/odin-architecture-v1.md — ODN-1 core-engine-free (~line 410), ODN-3 QoS-inside-Flow (~line 474), ODN-5 catalogs integer-only + fail-fast (~line 522), ODN-7 director seam read-only (~line 558), ODN-9 owned PRNG (~line 600), §11.7 edge-case table (line 1592; E10 at ~1609)
  - GDD: {OUT}/spec/gdd.md — M2 packet types & QoS lanes (~line 155; the roster + "color never the sole encoding"), M3 topology & nodes (~line 205; the ECMP hash splitmix64(src,dst,class,pkt_id) mod N)"""

PRIOR = """## ROUND 2 — prior-findings fix audit (r1 review, 13/13 confirmed, ALL addressed at abe578b — VERIFY, don't re-open)
This is round 2 of the SAME PR. The r1 review (4914400407, NEEDS CHANGES) filed 13 confirmed findings; the minion claims every one is fixed. Your job is to VERIFY each fix landed correctly and find NEW issues only. A fix that did NOT land (or landed wrong) = a finding. Do NOT re-open a fixed finding as new. The r1 map (finding -> claimed fix):
1. [P0 blocker] zero error-path tests for the fail-fast catalog loaders -> table-driven negative suite core/catalog_test.odin (test_catalogs_load_failfast: bad JSON/unknown shape/color/era/lane/weight/tick rows, one per rule, asserting the NAMED Catalog_Error).
2. color_rgba element guard tested `!ok` not `!okc` (silent 0) -> `if !okc || n < 0 || n > 255` at the color_rgba loop.
3. set-piece tick fields u64-wrapped negative JSON (start_tick -5 => ~2^64, surge never fires) -> i32 validated (st < 0 || dt < 1 || fl < 0) BEFORE the u64 casts.
4. default_lane truncated to u8 BEFORE the >2 check (256/257/258 wrap into valid lanes, both loaders) -> lane range-checked as i32 before `u8(lane)` cast, both sites.
5. Packet_Type.demand_weight had no range validation -> `if dw < 0` reject in packet_types; demand entries reject demand_weight < 1.
6. weighted_pick_excluding untested (weighting + all-excluded path) -> core/demand_test.odin test_weighted_pick_excluding: determinism, excluded-never-picked, all-excluded => ok=false, zero-weight exclusion.
7. drift matrix had no era-byte tamper class -> harness/drift.odin bad_era mutation (byte 16, 0<->3) with a DIVERGENCE assertion (diverge flag: gate accepts but re-sim must not reproduce the manifest; seq_equal).
8. duplicate demand era rows silently last-wins + leaked arrays -> `seen: [64]bool` duplicate-era fail-fast ("duplicate era row").
9. jint truncates json.Float (2.9 => 2) on the new 3.1 fields -> jint_strict (Float => ok=false) used for ALL new 3.1 sim fields (packet_types + demand entries + set-pieces + era).
10. T2 fail strings temp-allocated (freed per-tick free_all => garbage FAIL output) -> check_golden appends fmt.aprintf (default allocator) strings.
11. load_demo_qos_fixture leaked demolishes -> the loader is GONE: qos_fixture folded into #29's Demo_Replay single-source refactor (demo_apply_setup applies fixture + spawns + session in live AND replay identically; per-piece loaders dropped). run.odin:308 `delete(demo.demolishes)` frees the rest.
12. weighted_pick doc comment claimed zero/negative weights "still count toward the total" -> comment now says "never picked and does NOT count toward the total".
13. qos.dem was the only demo missing `expect hash stable` -> demos/qos.dem now carries it.
Round-2 verified ground truth at abe578b (already re-run): odin test core 61/61, harness run 9/9 (incl. qos era-3 1500-tick bit-for-bit), drift-check 62/62 mutations rejected, lint 5/5."""

SCOPE_C1 = """v2 Story 3.1 — Packet types + the demand director (OPENS SLICE 3, the QoS differentiator). Two packet types (email low/low/low + streaming med/med/high) with distinct shapes/icons (never color alone — accessibility), spawned per a demand plan via the `scripted_plan_pressure` director, with SEEDED WEIGHTED-RANDOM destination selection. Replaces slice 1's trivial 1-packet `flow_seed_demand` with the real demand model (ported Odin-native from v1 §3: PressurePlan/DemandSpec/SetPiece). New `packet_types` catalog + `demand` catalog; the director emits a PressurePlan per era with typed source/sink selectors + weighted dst; flow_step spawns per spec inside the deterministic rng stream. Stories 3.2 (lanes), 3.3 (contention), 3.4 (SLA) build on this.
ROUND-2 CONTEXT: this round's diff is the r1 diff REBASED onto v2 with #29 merged (the harness Demo_Replay single-source refactor is now BASE, not this PR). The qos_fixture folds into demo_apply_setup (seeds identically in live + replay); the superseded per-piece loaders (load_demo_spawns/session/qos_fixture) are dropped; era rides the log header; fixture on|off|qos merged into one directive; ecmp/demolish captures re-blessed for the catalog-hash fold + class-0 render.
Files in THIS chunk (chunk 1 of 2 — code + catalogs): core/catalog.odin, core/catalog_test.odin, core/demand.odin (the director), core/demand_test.odin (the §3.3 pins), core/determinism_test.odin (test-catalog extension), core/flow.odin (spawn path + weighted_pick), core/serialize.odin (class rides the T1 hash), app/main.odin, app/render/view.odin (per-class SHAPE render), harness/{catalogs,demo,drift,run,goldens}.odin (era + qos-fixture plumbing), data/{packet_types,demand,node_types}.json, demos/qos.dem (NEW). Chunk 2 (the goldens) is a SEPARATE lens wave — do not review it here."""

SCOPE_C2 = """v2 Story 3.1 — Packet types + the demand director (the goldens wave). This chunk (chunk 2 of 2) is the golden-manifest wave: T1 hash manifests (.t1), binary replay logs (.log.bin), and T2 PNG captures. The code + catalogs were chunk 1 (a separate lens wave) — do NOT review code here. Context: adding the packet_types + demand catalogs changed the folded catalog_hash for EVERY demo, and the new Packet.class byte rides the T1 state hash — so ALL legacy .t1/.log.bin goldens were re-blessed, and flow/ecmp/demolish PNGs re-captured (class-0 = email renders as grey circle). The NEW qos golden (goldens/qos.t1, qos.log.bin, qos/{01000ms,65000ms}.png) pins the era-3 two-packet-types run (demos/qos.dem: seed 3003, run 75000ms = 1500 ticks @20Hz, era 3, capture at 1000ms + 65000ms; the streaming_surge window is [60s,150s) = ticks [1200,3000) — the run ends mid-surge at tick 1500).
ROUND-2 CONTEXT: T2 pixel debt is CLOSED — the harness re-diff ran (bundle/flow/draw/win/lose matched bit-for-bit; ecmp/demolish first-blessed) and #29 was Perkins-APPROVED. The goldens here are the blessed contract; do NOT re-litigate their pixel content. A golden CHANGE in THIS PR (vs the r1 diff's goldens) would be a finding; the files as-is are blessed."""

GUARDS = """- **🚨 DISTINCT SHAPES, NOT COLOR ALONE — THE accessibility invariant.** email + streaming MUST be visually distinguishable by SHAPE/icon (color is secondary). A render that differentiates by color alone = a REAL blocker. (email=circle, streaming=triangle is the intended design.)
- **🚨 SPAWN DETERMINISM [E10] — load-bearing.** The (class, src, dst) spawn sequence must be byte-identical for a fixed seed. The dst selection is seeded WEIGHTED_RANDOM using the run's RNG INSIDE the deterministic stream (no new/unseeded draw; no map-iter in the spawn/dst path; array-indexed). A determinism break = a blocker. The §3.3 dst-distribution pinned test + the era-3 QoS golden (bit-for-bit replay) must be REAL.
- **CATALOGS INTEGER-ONLY + FAIL-FAST [ODN-5].** Sim values are integers; the loaders validate + FAIL FAST on bad data (NO silent defaults on malformed JSON). A silent-default path or a non-integer sim value = a real defect.
- **DIRECTOR READ-ONLY ON TOPOLOGY [ODN-7].** scripted_plan_pressure takes a read-only view and EMITS a PressurePlan — no topology mutation. A director that mutates topology (or reads crisis state) = a blocker.
- **QOS PROCS INSIDE FLOW [ODN-3]** — QoS procs live inside Flow (not a peer system). Do NOT flag "QoS not a separate system" — that's the design (3.1 sets up the data; 3.2 adds lanes).
- **round_robin DELIBERATELY DROPPED (routing-ruling lens-guard).** Load-balancing (round-robin/weighted-LB) is BANNED by the locked routing model — weighted-random dst selection IS the design. Do NOT flag "missing round-robin" or Demand_Selection having a single variant — its absence is correct. (ECMP 2.2 is a hash; the director's weighted-random is a spawn-time dst pick — both deliberate.)
- **T2 PIXEL DEBT CLOSED — goldens VERIFIED + blessed by the merged harness (#29, now in base v2).** Do NOT re-litigate golden pixel content — the harness re-diff ran and #29 was Perkins-APPROVED. A golden CHANGE in THIS PR would be a finding; golden files as-is are the blessed contract.
- **DEMO_REPLAY SINGLE-SOURCE FOLD (from #29's merge — base, NOT this PR).** Run setup now flows through #29's Demo_Replay single-source refactor; this PR's qos_fixture folds into it (demo_apply_setup seeds identically in live + replay). Do NOT flag 'qos fixture not loaded separately' — the fold is the merged design.
- **ERA RIDES THE LOG HEADER — load-bearing (drift-pin semantic).** Replay applies header.era; the log is authoritative, NOT the demo file. The drift bad_era divergence pin depends on exactly this. Do NOT flag 'era not in the demo file' — that's the design.
- **APP ERA-0 UNTIL THE ERA-FSM STORY (flagged, NOT a defect).** The app still runs era 0 (director inactive in the app; the render supports per-class shapes and the era-3 GOLDEN demonstrates both types). Do NOT flag "app doesn't spawn streaming / show era 3".
- **flow_seed_demand LEGACY PATH KEPT (the "keep both" decision).** The trivial slice-1 path stays for existing demos + the determinism test (no rng draw). Do NOT flag "legacy path not removed / dead code".
- **CARRIED DATA, NOT YET CONSUMED (by design).** Packet_Type.latency_tol_ms / max_loss_pct / bandwidth_demand / default_lane and Demand_Entry.default_lane / demand_weight are validated catalog data consumed by 3.2/3.3/3.4 — do NOT flag them as "unused fields". Packet_Shape has 9 variants but only Circle/Triangle render (the rest are later-era data) — do NOT flag the unrendered variants.
- **CORE ENGINE-FREE (ODN-1)** — the packet_types catalog + director live in `package core`; zero engine/raylib imports there (the shape/icon render lives in app/render). An engine type leaking into `package core` = a blocker.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–2 complete), not main. **The prototype is REFERENCE-ONLY** (mine its DESIGN; the logic was rebuilt clean).
- **Do NOT re-open 1.1–2.3 findings** (merged, Perkins-verified) — carry-forward only. Do NOT re-open r1 findings either (see the fix-audit block — verify the fix, don't re-file)."""

LEGIT_C1 = """- **A color-only differentiation** (no distinct shape/icon per packet type) — a blocker (accessibility).
- **A spawn/dst determinism break** (unseeded or extra RNG draw; map-iter in the hot path; the weighted-random not inside the deterministic stream; a temp-allocator/draw-order bug that desyncs replay) — a blocker [E10].
- **A silent-default catalog path** (malformed JSON → default instead of fail-fast) or a non-integer sim value — a real defect [ODN-5].
- **A director that mutates topology** (or reads Run_State/crisis state) — a blocker [ODN-7].
- **An engine type leaking into `package core`** (ODN-1) — a blocker.
- **The §3.3 dst-distribution test missing/fake** (the pinned test) — or the era-3 QoS golden not actually replay-pinned.
- **An `odin test` / `odin build` / harness failure at abe578b.**
- **An r1 fix that did NOT land or landed wrong** (see the fix-audit block) — verified per-fix.
- A NEW catalog validation gap (out-of-range/negative value accepted that the ODN-5 fail-fast bar should reject) NOT covered by r1.
- A NEW era/log-header plumbing bug (replay not re-creating the run identically) — note the fold into demo_apply_setup touched run setup.
- A real NEW bug visible in the diff: wrong volume/window math, off-by-one in the surge window, self-loop leaks, histogram overflow, allocator misuse with a behavioral consequence."""

LEGIT_C2 = """- **A .t1 whose header doesn't match its demo** (ticks ≠ run_ms × logic_hz/1000; wrong seed; the qos.t1 not era-3 or missing the era in its log header — note: era rides the .log.bin header, not the .t1).
- **catalog_hash inconsistency** — every demo's .t1 must fold the SAME new catalogs (packet_types + demand added); a demo that DIDN'T change its catalog_hash is suspicious (stale bless).
- **A hash-manifest line count ≠ the header's ticks.**
- **The qos golden missing or not actually new** (qos.t1/qos.log.bin must exist as new files with 1500 ticks + 2 captures' worth of pinned state).
- **Legacy goldens whose hash lines DIDN'T change** even though the Packet.class byte + catalog_hash changed (a stale/incomplete re-bless hides a real divergence) — or legacy demos whose seeds/ticks changed (they must not).
- **Binary .log.bin files that shrank to 0 or are missing** for any demo with a .t1.
- ROUND 2: compare the r1 goldens against this diff's goldens — the ONLY expected changes are the qos golden (new) + flow/ecmp/demolish PNG re-captures. A .t1/.log.bin that changed since r1 for a non-qos demo = a finding (the code between r1 and r2 changed only via the #29 fold, which is run-setup, not action-log — the .log.bin action streams must be byte-identical to r1's).
- Note: PNG pixel content is NOT reviewable from this diff (binary), and the blessed contract covers it — do NOT flag pixel content. PNG files changing for flow/ecmp/demolish/ + qos/ being new is expected; boot/bundle/draw/win/lose NOT re-capturing PNGs is EXPECTED (verify against the .t1 hash changes)."""

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

This is a single-player desktop game core (Odin) with JSON catalogs + a replay harness — most OWASP categories will not apply; the realistic surface here is unsafe deserialization / missing validation at the JSON-catalog + replay-log boundaries and integer-overflow/coercion at parse. `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation, ODN-7 director seam)?
- Will it create technical debt or make future changes harder (3.2 lanes / 3.3 contention / 3.4 SLA build directly on this)?
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

The P0 critical paths here: spawn determinism [E10] (same seed → byte-identical (class,src,dst)), the §3.3 weighted-dst distribution pin, catalog fail-fast validation [ODN-5] (NEGATIVE tests — the r1 P0 blocker was the zero error-path suite; it must now be real and complete), the surge window boundaries, era-0 legacy no-rng-draw, the era-3 QoS golden replay (bit-for-bit). ROUND 2: verify the r1 fixes are TESTED (the new fail-fast rows, the weighted_pick_excluding suite, the bad_era drift divergence) and that the negative suite covers every fail-fast rule in catalog.odin (a rule with no negative row = a gap).

Blind-spot heuristics to check:
- New/modified behavior without matching coverage
- Happy-path-only coverage where error handling is implied
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

TEMPLATE = """# Perkins lens prompt — @LENS@ (@CHUNK@, round 2)

**You are the `@LENS@` lens. Your assigned `source` tag is `@LENS@`. Your output file is `@OUTFILE@`.**

You are ONE lens in a Perkins automated PR-review swarm (round 2 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — @CHUNKDESC@ (review exactly these bytes): @DIFFPATH@
@WTLINE@@SPECLINE@

## Round 2 — prior-findings fix audit
@PRIOR@

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
    c1 = chunk == "c1"
    diffpath = f"{OUT}/chunk1.patch" if c1 else f"{OUT}/chunk2.patch"
    lines = 1805 if c1 else 2815
    files = 18 if c1 else 30
    chunkdesc = f"chunk {'1 of 2 — code + catalogs' if c1 else '2 of 2 — goldens'}, {lines} lines, {files} files"
    outfile = f"{OUT}/{lens}-{chunk}.json"
    if lens == "blind":
        wtline = ""
        specline = ""
    else:
        wtline = f"- WORKTREE (verify every claim against the actual code here — this is your ground truth, detached at sha {SHA}): {WT}\n"
        specline = f"- SPEC / CONTEXT (read the sections named; full files):\n{SPEC_BLOCK}\n"
    scope = SCOPE_C1 if c1 else SCOPE_C2
    legit = LEGIT_C1 if c1 else LEGIT_C2
    guards = GUARDS if c1 else "\n".join(l for l in GUARDS.split("\n") if not l.startswith("- **🚨 DISTINCT SHAPES"))
    t = TEMPLATE
    t = t.replace("@LENS@", lens)
    t = t.replace("@CHUNK@", "chunk 1 — code+catalogs" if c1 else "chunk 2 — goldens")
    t = t.replace("@OUTFILE@", outfile)
    t = t.replace("@CHUNKDESC@", chunkdesc)
    t = t.replace("@DIFFPATH@", diffpath)
    t = t.replace("@WTLINE@", wtline)
    t = t.replace("@SPECLINE@", specline)
    t = t.replace("@PRIOR@", PRIOR)
    t = t.replace("@SCOPE@", scope)
    t = t.replace("@GUARDS@", guards)
    t = t.replace("@LEGIT@", legit)
    t = t.replace("@CONTRACT@", OUTPUT_CONTRACT)
    t = t.replace("@ACCURACY@", ACCURACY)
    t = t.replace("@BRIEF@", BRIEFS[lens])
    return t

os.makedirs(f"{OUT}/prompts", exist_ok=True)
for chunk in ("c1", "c2"):
    for lens in ("blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"):
        p = f"{OUT}/prompts/{lens}-{chunk}.md"
        with open(p, "w") as f:
            f.write(build(lens, chunk))
        print(p, os.path.getsize(p))
