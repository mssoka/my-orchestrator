#!/usr/bin/env python3
"""Generate the 35 Perkins lens prompts for packet-plumber-v2-3.3-contention r1 (5 chunks)."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.3-contention-r1"
SHA = "ffc9b7b"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): {OUT}/spec/job-briefing.md
  - Story 3.3 card: {OUT}/spec/stories-v2.md (Story 3.3 card ~line 275; slice-3 framing above it)
  - Implementation spec (the minion's own frozen spec — acceptance matrix + code map): {OUT}/spec/spec-3-3-contention.md (the diff's first file; identical to the worktree copy)
  - Architecture invariants: {OUT}/spec/odin-architecture-v1.md — ODN-3 QoS-inside-Flow (~line 474), ODN-11 save = seed + action log (~line 687), §11.7 edge-case table (line 1592; E7/E9/E10/E22 at ~1604-1619), §6.2 per-link buffering (line ~964)
  - Canon commits (BOTH MERGED INTO BASE v2 — reviewed as canon, not as this PR's findings): {OUT}/spec/canon-2e3acab.patch (spatial lanes) + {OUT}/spec/canon-8ece056.patch (no auto lanes + lane-speed)"""

SCOPE_C1 = """v2 Story 3.3 — node serialization + contention drop ladder (the contention half of the QoS differentiator): `qos_serialize` (pure) computes the per-window WRR budget — each ready lane gets its WFQ allocation floored to 1 unit when zero (E7 — no starvation under continuous Express), skipped-when-empty (work-conserving gap-fill); per-bundle cyclic-WRR service windows repeat until the bundle capacity is consumed (a LONE packet in ANY lane gets full capacity — light-demo transits pinned unchanged); E9 admission ladder (a packet joining a full (bundle, lane) queue sheds the NEWEST packet of the LOWEST-priority non-empty lane, walking BE→S→E; the arriving packet drops when it IS the target); E22 pool backstop (at pool_max_packets the spawn-side ladder sheds over the in-flight pool, lowest-priority lane first, strict-priority: an Express resident never pays for a Standard arrival). Drops emit Packet_Dropped{class, reason} events (EVENT_TAG_PACKET_DROPPED = 4, payload serialized ONLY for the new tag — append-only, pre-3.3 event bytes unchanged). LOG_VERSION stays 3, no new commands, ZERO new serialized state (queues/lanes/budgets all DERIVED). New balance.json keys: lane_queue_packets (6) + pool_max_packets (512), fail-fast validated ≥ 1, folded into catalog_hash.
Files in THIS chunk (chunk 1 of 5 — core+data): core/catalog.odin (new balance keys + validation), core/catalog_test.odin, core/demand_test.odin, core/determinism_test.odin, core/ecmp_test.odin, core/flow.odin (the serialization service + drop ladders — the heart), core/qos.odin (qos_serialize), core/qos_test.odin (E7/E9-21-combos/E22/double-shed/lone-packet pins), core/serialize.odin (tag-conditional Packet_Dropped payload), core/types.odin (Drop_Reason, EVENT_TAG_PACKET_DROPPED), data/balance.json, data/palette.json. Chunks 2-5 (spec/app/harness/demos/goldens) are SEPARATE lens waves — do not review them here."""

SCOPE_C2 = """v2 Story 3.3 — the app/harness/docs wave (chunk 2 of 5): the spatial-lane canon render (app/render/view.odin — bundle_lane_caps_view, Lane_Bands, lane_bands, three painted lane strokes per pipe with width = WFQ share, packets laterally offset into their lane riding end-to-end AT LANE SPEED: Express streaks / Standard cruises / Best-effort crawls; a zero-share lane draws no stroke; app/render/palette.odin + data/palette.json lane colors), the harness demo directive lowering (harness/demo.odin, harness/run.odin), the new launchable demos/qos_contention.dem (pipe 0 oversubscribed ~2.4×), and the implementation spec _bmad-output/implementation-artifacts/spec-3-3-contention.md (frozen spec — the diff's first file). Chunks 1 (core), 3/4/5 (goldens) are SEPARATE lens waves — do not review them here."""

SCOPE_C3 = """v2 Story 3.3 — the LIGHT-demo goldens wave (chunk 3 of 5): goldens/boot|bundle|demolish|draw|ecmp|flow|lose|place (.t1 + .log.bin + .png). The re-bless has THREE documented reasons (see the re-bless guard): (a) catalog_hash header drift — new balance.json keys; (b) the canon T2 repaint — all pipe demos' pixels re-blessed (spatial lanes); (c) genuine contention shifts ONLY in qos/qos_emphasis/ecmp (NOT in these light demos). For THIS chunk: the light demos must show ZERO sim change — their .t1 hash-line shifts must be EXACTLY the catalog_hash header line, no per-tick line shifts (demolish's severance event stream stays silent-cull, bundle/draw/flow/place/win keep their transits, lose keeps its loss). T2 pixels re-blessed by canon for every pipe demo. Verify each manifest's hash consistency."""

SCOPE_C4 = """v2 Story 3.3 — the qos.dem golden wave (chunk 4 of 5): goldens/qos.log.bin + goldens/qos.t1 (3011 lines — the longest golden) + 2 PNGs. qos.dem is a LONG fixture demo (65000ms) where CONTENTION GENUINELY ENGAGES: with 3.3's serialization, per-tick T1 shifts beyond the catalog_hash header are EXPECTED and documented as reason (c). Verify: the header carries the new catalog_hash (same as every other demo), per-tick shifts are plausibly contention-driven (lane-ordered serialization changing crossing times), PNGs re-blessed by canon (spatial lanes), the .t1 line count matches the header's tick count, and no shift looks like an E7 starvation or E9/E22 inversion."""

SCOPE_C5 = """v2 Story 3.3 — the new-demo + qos_emphasis/win goldens wave (chunk 5 of 5): goldens/qos_contention.* (NEW — the launchable: pipe 0 oversubscribed ~2.4×, T1 253 lines, T2 captures at 1000/3000/10000ms), goldens/qos_emphasis.* (T1 611 lines, captures at 1000/5000/12000ms — contention shifts expected here too), goldens/win.* (light demo — zero sim change beyond the catalog_hash header + canon T2). Verify: qos_contention goldens are complete (.log.bin + .t1 + all 3 PNGs), the new manifest carries the SAME catalog_hash as every other demo, its T1 line count == header ticks, drops are visible in the T1 (Packet_Dropped events with class+reason), and win.t1 shows only the header shift (light demo)."""

GUARDS = """- **🚨 THE ODN-11 RE-BLESS — THE load-bearing invariant (verify the REASONS, don't auto-flag).** The minion re-blessed goldens DELIBERATELY with THREE documented reasons: (a) catalog_hash header drift — new balance.json keys (the 3.2 precedent); (b) the canon T2 repaint — all pipe demos (spatial lanes); (c) genuine contention shifts in qos/qos_emphasis/ecmp. VERIFY each reason holds at the byte level: the light demos (non-contention) must show ZERO sim change (only the catalog_hash header line shifts in their .t1), and the re-bless must be documented in the PR/spec (it is — spec-3-3-contention.md documents all three). A re-bless whose documented reason doesn't hold, or evidence of unaccounted drift (a light demo with per-tick shifts, a silent PNG change) = a BLOCKER.
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
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha."""

LEGIT_C1 = """- **An E9 ladder error**: a shed that hits the wrong lane/priority (not the lowest-priority non-empty), a shed that removes the OLDEST instead of NEWEST, a drop when a shed was possible (arrival dropped though a lower-priority non-empty lane existed), the arriving packet joining when it should drop — a blocker.
- **An E22 priority inversion**: a Standard/Best arrival evicting an Express resident (or any lower-class arrival evicting a higher-class resident) — a blocker. The pool ladder must walk BE→S→E over in-flight packets and never evict a higher class.
- **An E7 starvation**: the WRR floor missing/skipped-when-non-empty, a lone packet NOT getting full capacity, gap-fill not work-conserving (capacity left idle while a lane has ready packets) — a blocker.
- **A determinism break [E10]**: an unordered walk (map iteration), a non-deterministic splice (order-preserving removal violated), a duplicate splice index removing the wrong packet (the double-shed pin exists — a missing `exclude`/`drops` guard), unseeded state, a serialized field sneaking in (new Packet/Flow_State fields, LOG_VERSION bump without the documented tag-conditional mechanism), event payload bytes written for OLD tags.
- **A serialization inconsistency**: Packet_Dropped payload written for the wrong tag or class/reason layout mismatch between write and read (w_u16 class then w_u8 reason — reader must match), event emission inside a loop that double-counts.
- **An integer bug**: budget math overflow, lane_caps sum/cast errors (u64→f32→u32 narrowing), `lane` index out of bounds (u8 lane vs [3] arrays), queue count vs lane_queue_packets off-by-one.
- **A catalog validation gap**: lane_queue_packets/pool_max_packets accepting 0/negative; the new keys missing from balance.json error paths; fail-fast violated.
- **An `odin test` / `odin build` / harness failure at ffc9b7b** (Perkins ran these green — core 84, demos 12, drift 83, lint 5/5 — if you find a failure, it is a blocker; re-run to confirm before filing).
- **A real bug visible in the diff**: wrong serve_bundle_lane budget accounting, flow_remove_at index errors, lane_pipe_setup mis-resolution, bundle_of_pipe returning a wrong bundle."""

LEGIT_C2 = """- **A canon render violation** (2e3acab/8ece056): missing lane strokes, stroke width not ∝ WFQ share, no lateral packet offset, lane speed not mapped (Express fastest / Best slowest), auto-assigned lanes anywhere, a zero-share lane drawing a stroke (should draw none — base pipe shows through), a queued packet NOT in its lane — a blocker.
- **A harness directive bug**: new directive lowering errors (unknown class/lane/pipe not failing loudly), intent_apply_tick math, leaks in the new delete paths, the demos/qos_contention.dem authoring (pipe 0 oversubscribed ~2.4×: pipe ids vs draw order, capture times vs directives, era/fixture).
- **A data bug in balance.json/palette.json**: lane_queue_packets/pool_max_packets missing or out of range, palette lane keys missing fallbacks, lane colors identical to an existing semantic color (color is never the sole encoder).
- **A docs/scope drift**: the implementation spec claiming something the code does not do, or the code doing something the frozen spec forbids (e.g. new player commands, LOG_VERSION bump, 3.4 SLA work, severance-drop events, per-class bandwidth_demand, LB mechanics).
- **An `odin build` failure** at ffc9b7b (app + harness — Perkins built both green)."""

LEGIT_C3 = """- **A light-demo .t1 with PER-TICK shifts** (beyond the catalog_hash header line) — the light demos must show ZERO sim change; a per-tick shift here = unaccounted drift = a blocker. (Exception: ecmp is a CONTENTION demo — its shifts are documented reason (c); in THIS chunk it must still show ONLY header + documented contention shifts.)
- **A .t1 whose header doesn't match its demo** (ticks ≠ run_ms × logic_hz/1000; wrong seed; wrong demo name).
- **catalog_hash inconsistency** — every demo's .t1 MUST carry the SAME new hash; a demo that DIDN'T change its catalog_hash is a stale bless; a demo with a DIFFERENT hash is an inconsistency.
- **A hash-manifest line count ≠ the header's ticks.**
- **Legacy goldens whose hash lines DIDN'T change** even though catalog_hash changed (a stale/incomplete re-bless hides a real divergence) — or legacy demos whose seeds/ticks changed (they must not).
- **Binary .log.bin files that shrank to 0** or are missing for any demo with a .t1.
- Note: PNG pixel content is NOT reviewable from this diff (binary); the PNGs being re-blessed is EXPECTED (canon repaint). Do not flag "PNGs changed" per se — flag only if a LIGHT demo's PNG is absent where it should exist."""

LEGIT_C4 = """- **qos.t1 header**: same new catalog_hash as all other demos; tick count == header ticks; seed/demo name match qos.dem.
- **Per-tick shifts plausibly contention-driven**: serialization reorders crossings (lane-ordered exit), drops appear as Packet_Dropped events with class+reason — shifts consistent with E9/E22/E7 behavior are EXPECTED (reason c); shifts that look like STARVATION (a lane going idle while others run for a long window), an INVERSION (Express dropped while Standard/Best in flight), or a lane count exceeding lane_queue_packets per (bundle, lane) = a blocker.
- **A stale/incomplete re-bless**: qos.t1 hash lines identical to the old blessed hash despite the documented contention (would mean the golden wasn't actually re-blessed at this sha)."""

LEGIT_C5 = """- **The qos_contention golden complete**: .log.bin + .t1 (253 lines) + ALL 3 PNGs (1000/3000/10000ms) present; header carries the SAME catalog_hash; T1 line count == header ticks; Packet_Dropped events visible in the T1 (drops are the demo's whole point — pipe 0 oversubscribed ~2.4×).
- **qos_emphasis.t1**: same hash consistency; contention shifts documented (reason c); captures at 1000/5000/12000ms present.
- **win.t1 (light demo)**: only the catalog_hash header shift + canon T2 — NO per-tick shifts (a light demo; win has no contention).
- **Drop semantics in the T1s**: a Packet_Dropped stream that drops Express while Standard/Best packets are in the same bundle queue = E22 inversion = a blocker."""

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

This is a single-player desktop game core (Odin) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories will not apply; the realistic surface here is unsafe deserialization / missing validation at the JSON-catalog + replay-log + demo-parser boundaries (the new balance keys lane_queue_packets/pool_max_packets loaders, the log_read tag switch for EVENT_TAG_PACKET_DROPPED) and integer-overflow/coercion at parse. `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation, ODN-3 QoS-inside-Flow, ODN-5 data-driven catalogs, ODN-13 no globals, ODN-10 arrays-only)?
- Will it create technical debt or make future changes harder (3.4 SLA builds directly on this)?
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
        "c1": ("chunk 1 of 5 — core+data", 1202, 12, "c1.patch"),
        "c2": ("chunk 2 of 5 — spec+app+harness+demos", 1050, 6, "c2.patch"),
        "c3": ("chunk 3 of 5 — light-demo goldens", 1348, 32, "c3.patch"),
        "c4": ("chunk 4 of 5 — qos golden", 3020, 4, "c4.patch"),
        "c5": ("chunk 5 of 5 — contention/emphasis/win goldens", 1029, 13, "c5.patch"),
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
    scope = {"c1": SCOPE_C1, "c2": SCOPE_C2, "c3": SCOPE_C3, "c4": SCOPE_C4, "c5": SCOPE_C5}[chunk]
    legit = {"c1": LEGIT_C1, "c2": LEGIT_C2, "c3": LEGIT_C3, "c4": LEGIT_C4, "c5": LEGIT_C5}[chunk]
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
for chunk in ("c1", "c2", "c3", "c4", "c5"):
    for lens in ("blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"):
        p = f"{OUT}/prompts/{lens}-{chunk}.md"
        with open(p, "w") as f:
            f.write(build(lens, chunk))
        print(p, os.path.getsize(p))
