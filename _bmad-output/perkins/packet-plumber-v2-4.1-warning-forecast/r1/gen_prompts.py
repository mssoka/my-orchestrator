#!/usr/bin/env python3
"""Generate the 35 Perkins lens prompts for packet-plumber-v2-4.1-warning-forecast r1 (5 chunks)."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.1-warning-forecast-r1"
SHA = "9820a55"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): {OUT}/spec/job-briefing.md
  - Story 4.1 card: {OUT}/spec/stories-v2.md (Story 4.1 card at line 362; slice-4 framing above it)
  - Implementation spec (the minion's frozen spec — acceptance matrix + code map + the RE-BLESS cause-docs): {OUT}/spec/spec-4-1-warning-forecast.md — copy the diff's first file (identical to the worktree copy at _bmad-output/implementation-artifacts/spec-4-1-warning-forecast.md); the re-bless documentation lives in "Boundaries" + "Design Notes"
  - Architecture invariants: {OUT}/spec/odin-architecture-v1.md — ODN-11 save = seed + action log (~line 687), §11.7 edge-case table (line 1592; E9/E10 at ~1608-1609), §6.x per-link buffering + lane bound (line ~964), T1 hash contract (line ~1353), the golden-stability rule (~line 1397)"""

SCOPE_C1 = """v2 Story 4.1 — the warning/forecast system (the fun loop's telegraph, slice-4 opener): `core/warnings.odin` (NEW — `warning_evaluate` runs INSIDE core.step AFTER flow_step, BEFORE win_lose_eval; node strain = Σ bandwidth of packets that FAILED a forward attempt (`Packet.waiting_ticks >= 1` — a NEW serialized field incremented in flow.odin's forward pass when no route exists, cleared on every successful forward/drop-back; fresh spawns + fresh transit arrivals have 0 and NEVER strain — the no-flicker contract) ÷ `node_types[].throughput_units`; pipe pressure = the FULLEST lane queue's depth on the bundle vs its E9 bound (`lane_queue_packets × packet_bandwidth` — a lone packet 17% healthy, a lane at its bound 100% = dropping; levels replicate to every member pipe); forecast = era set-pieces in `[start_tick - forecast_lead_ticks, start_tick + duration_ticks)` with exact countdowns — a PURE read of the schedule, never fires anything (4.2's job). `Crisis_State` on `Run_State` (node_strain/pipe_strain/forecast — ALL DERIVED per tick, rebuilt identically on replay). `Warning_Raised`/`Warning_Cleared` events (tags 6/7, payload = sign + target, serialized TAG-CONDITIONALLY — append-only, pre-4.1 event bytes unchanged). serialize.odin gains the warnings section (absent-when-empty) + `waiting_ticks` rides the per-packet T1 hash. LOG_VERSION stays 3, no new commands. balance.json `warnings` block (70/90 ladder, 600/200/400-tick leads, fail-fast validated). The app: era-3 sandbox (goal 0 / cap 0 — win/lose is 4.3's), health rings + !/!! glyphs + pinned pulse table (never color alone), pressure halos, the WEATHER REPORT panel (`app/render/forecast.odin` — zero pixels when empty), harness capture signature gains crisis + tick + the panel. demos/warn.dem (NEW — the launchable golden) + demos/lose.dem tweak. `_bmad-output/implementation-artifacts/` = epic-4 context + the frozen implementation spec (read the re-bless cause-docs!).
Files in THIS chunk (chunk 1 of 5 — code+docs+data+demos+harness): _bmad-output/implementation-artifacts/{epic-4-context.md, spec-4-1-warning-forecast.md}, app/{main.odin, render/forecast.odin, render/palette.odin, render/view.odin}, core/{catalog.odin, catalog_test.odin, determinism_test.odin, flow.odin, qos_test.odin, serialize.odin, step.odin, types.odin, warnings.odin (NEW), warnings_test.odin (NEW)}, data/balance.json, demos/{lose.dem, warn.dem (NEW)}, harness/{goldens.odin, run.odin}. Chunks 2-5 (the goldens) are SEPARATE lens waves — do not review them here."""

SCOPE_C2 = """v2 Story 4.1 — the warn.dem golden wave (chunk 2 of 5): goldens/warn.{log.bin, t1, 01500ms.png, 45000ms.png, 65000ms.png} — ALL NEW (warn.dem is the 4.1 launchable: era 3 + fixture qos + draws + lane categorization + a 30 s-delayed router->host pipe so streaming packets pile at the host). The .t1 (1513 lines) pins the forecast rows + the WHOLE warning event stream (E10): the demo narrative (demos/warn.dem, in chunk 1 — the goldens' .t1 header comments + the .dem comments cross-reference) pins host Node_Strained @1 / Node_Critical @2 (75%/150% of the 80 u/s host), red until the 30 s draw opens the route, forecast panel from 30 s (600-tick lead) with countdown 300 @45 s, surge fires at 60 s (streaming x10) → panel reads NOW, pipe 0 saturates under email load → red/amber pressure halo. Captures: 1500 ms (strain telegraph, no panel yet), 45000 ms (countdown + red pressure), 65000 ms (surge ACTIVE NOW). Verify the T1's warning events match the narrative ticks exactly, the header carries the SAME catalog_hash as every other demo, and the captures are at the right times."""

SCOPE_C3 = """v2 Story 4.1 — the qos.dem golden wave (chunk 3 of 5): goldens/qos.{log.bin, t1, 01000ms.png, 65000ms.png}. qos.t1 is 3011 lines (1500 ticks @20 Hz = 75 s) — a LONG fixture demo whose re-bless is cause-documented: (a) catalog_hash fold (mechanical — the warnings block in balance.json folds into every manifest + log header); (b) the per-tick hash bytes shift in EVERY .t1 because `waiting_ticks` rides the per-packet T1 hash AND catalog_hash bytes ride inside the hash stream (mechanical — the whole .t1 is a deliberate re-bless); (c) the 65 s capture gains the forecast panel + surge strain (qos runs the era-3 streaming surge schedule — panel visible in the T2). Verify: header hash == the SAME bd13d5dfba445d80 as every other demo; ticks 1500; the 01000ms.png is a NO-strain frame (early qos — should be pixel-identical to base) vs the 65000ms.png which may carry the panel/rings; no per-tick line looks like an E9/E22 inversion or E7 starvation regression (spot-check the T1's Packet_Dropped + Warning event stream around the surge)."""

SCOPE_C4 = """v2 Story 4.1 — the LIGHT-demo goldens wave (chunk 4 of 5): goldens/boot|bundle|demolish|draw|ecmp|flow|lose|place|win (.t1 + .log.bin; lose/03000ms.png is in the diff). The re-bless has TWO documented causes: (a) catalog_hash fold — the balance.json warnings block shifts EVERY .t1 hash line + .log.bin header (mechanical; the hash bytes ride inside the stream); (b) waiting_ticks bytes in per-packet serialization (mechanical — the field rides the T1 hash). The NEGATIVE PROOF: boot/draw/flow/win/bundle/ecmp/place/demolish T2s (PNGs) are byte-identical — NONE of their PNGs may appear in this diff; lose/03000ms.png is the ONE documented T2 shift in this chunk (lose.dem's own stuck packet — the demo's scenario IS the strain: the residential telegraphs 🔴, cause-documented in the implementation spec). Verify: zero per-tick .t1 lines that look like BEHAVIORAL drift beyond the fold+field bytes (can't re-derive hashes by hand — instead verify the manifest STRUCTURE: header fields, tick counts, seed/demo names, hash consistency); PNGs exactly {lose/03000ms.png} — nothing else; .log.bin headers re-blessed (3-4 line diffs = binary header bytes)."""

SCOPE_C5 = """v2 Story 4.1 — the contention/era-3 goldens wave (chunk 5 of 5): goldens/qos_contention.* (3 PNGs), goldens/qos_emphasis.* (3 PNGs), goldens/sla.* (01000ms.png + 04000ms.png — NOTE sla/10000ms.png is NOT in the diff: the relief frame — zero strain at 10 s — is the NEGATIVE PROOF inside the shifted demo). Cause-documented T2 shifts: sla + qos_contention (the saturated router row gains rings/halos at strained captures), qos_emphasis (era-3 load — gains rings if its captures strain). Verify: the shifted PNG set is EXACTLY the documented set (sla/10000ms.png + all qos_contention/qos_emphasis PNGs at captures that DON'T strain must stay byte-identical — absent from the diff); the .t1 header catalog_hash == bd13d5dfba445d80; manifest structure consistent (ticks, seeds, demo names); .log.bin re-blessed headers only."""

GUARDS = """- **🚨 THE ODN-11 RE-BLESS — verify the CAUSE-DOCUMENTATION, don't auto-flag.** Re-blessed deliberately: (a) catalog_hash fold — mechanical (new balance.json warnings block folds into EVERY .t1 hash line + .log.bin header, because catalog_hash bytes ride INSIDE the T1 hash stream); (b) waiting_ticks rides the per-packet T1 hash (4 new bytes per in-flight packet per tick — mechanical; the field is documented in serialize.odin); (c) T2 telegraph shifts — cause-documented PER DEMO in the implementation spec (sla + qos_contention + qos_emphasis + qos 65s + lose; boot/draw/flow/win/bundle/ecmp/place/demolish T2s byte-identical — the negative proof). VERIFY the negative proof (those demos' PNGs absent from the diff) + the cause-docs. A re-bless with an unaccounted shift (a negative-proof demo's PNG in the diff, a relief frame shifting, a zero-traffic demo's T2 moving) = a BLOCKER.
- **🚨 THE NO-FLICKER CONTRACT — load-bearing.** Node strain uses `Packet.waiting_ticks` (a NEW serialized field — packets that FAILED a forward attempt; incremented in flow.odin's forward pass when no route exists, cleared on every successful forward / E29 drop-back / delivery). A HEALTHY transit must NEVER strain: a fresh spawn or fresh transit arrival that forwards next tick has waiting_ticks 0. A flicker (a healthy node flashing a warning) or a strain signal without a real backlog = a blocker. Also: `waiting_ticks` is NEW SERIALIZED STATE — LOG_VERSION must stay 3 and old-log acceptance stays intact [E10]; the action-log FORMAT must be unchanged (the field rides the T1 state hash — the writer-only canonical dump — NOT the log records). A log-format change or LOG_VERSION bump = a blocker.
- **PIPE PRESSURE vs [E9].** Pressure = fullest lane queue depth on the bundle ÷ its E9 bound (`lane_queue_packets × packet_bandwidth`). A lane at its bound = 100% = the ladder is dropping. A pressure computation disconnected from the real E9 bound (wrong bound, wrong lane, off-by-one at the bound) = a real defect.
- **FORECAST READS THE SCHEDULE, NEVER FIRES.** The forecast derives from era set-pieces in [start−lead, start+duration) with exact countdowns — it must be PURE (no state mutation beyond the derived rows, no events, no side effects, no win/lose interaction). A forecast that mutates state or fires events = a blocker.
- **EVENTS TAGS 6/7 + SIGN/TARGET.** Warning_Raised/Cleared with sign+target, tag-conditional payload like the 3.3/3.4 events (bytes written ONLY for tags 6/7 — append-only); replay byte-identity pinned (warnings_test replay test + the T1). A broken tag or a payload written unconditionally (breaking pre-4.1 event byte-identity) = a real defect.
- **NEVER COLOR ALONE.** Health rings + !/!! glyphs + tick-derived pulse (pinned 16-step table, no transcendentals) — the warning render must be distinguishable without color (art-direction §6.1). A color-only warning render = a blocker.
- **WEATHER REPORT PANEL — ZERO PIXELS WHEN EMPTY.** The panel is shared app/harness and renders nothing when no warnings are active (golden-stability). A panel that draws pixels while empty = a real defect.
- **ERA-3 SANDBOX (goal/cap 0 — win/lose is 4.3's).** The app session intentionally has no win/lose. Do NOT flag "win/lose not implemented" — 4.3 owns it. The launchable must still be launchable + the demos honest.
- **No re-open of slice-1..3.4 findings** (merged + Perkins-approved) — carry-forward only.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–3 + 3.5 + 3.2–3.4 + canon). demand.odin / routing.odin / qos.odin / win_lose.odin are BASE files — read-only context, not review targets.
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha."""

LEGIT_C1 = """- **A healthy-transit strain (flicker)**: a node warning while its stuck backlog is empty, or a strain signal from a packet that forwards next tick — a blocker (the no-flicker contract).
- **A LOG_VERSION bump or an action-log format change** from waiting_ticks (the field must ride the T1 state hash only) — a blocker [E10]. Old-log acceptance (version check + reader) unchanged.
- **A forecast that fires/mutates**: the forecast writing events, touching flow/win-lose state, or any side effect beyond the derived rows — a blocker.
- **A pressure computation disconnected from the E9 bound**: wrong bound units, wrong lane (not the fullest), off-by-one at the bound, pressure not replicating to member pipes — a real defect.
- **A color-only warning render**: a node/pipe warning state encoded ONLY by color (no ring shape, no glyph, no pulse) — a blocker (accessibility).
- **The WEATHER REPORT panel drawing pixels while empty** — a real defect (golden-stability).
- **An event-payload bug**: tags 6/7 payload written unconditionally (breaking pre-4.1 event byte-identity), sign/target serialized in the wrong order vs the reader, one event per transition violated (double events on a single boundary), or a transition that skips the level that ended (e.g. Amber→None clearing Node_Critical instead of Node_Strained).
- **A waiting_ticks bookkeeping bug**: increment on a path that isn't a failed attempt, missing clear on success, strain measured from on_edge/delivered packets, waiting_ticks counting toward the wrong node slot.
- **An integer bug**: `nload × 100 / throughput` overflow/order, u32→i64 narrowing, slot-index vs node-id confusion (the events carry node IDs; the arrays are slot-ordered).
- **A catalog validation gap**: amber/red ladder or lead-time fail-fast rows missing/uncovered, warnings block absent from balance.json error paths.
- **A determinism break [E10]**: an unordered walk (map iteration, pointer iteration), a non-deterministic transition baseline (the prior tick's levels must be read in place before overwrite), resize() semantics mishandled (new slots None, shrink truncation).
- **An `odin test` / `odin build` / harness failure at 9820a55** (Perkins ran these green — core 97, demos 14 incl. warn.dem, drift 97, lint 5/5 — if you find a failure, re-run to confirm before filing; a confirmed failure is a blocker)."""

LEGIT_C2 = """- **The warn.t1 event stream NOT matching the demo narrative** (demos/warn.dem's golden-verified stream: host Node_Strained @1, Node_Critical @2, red until the 30 s draw, forecast from 30 s with countdown 300 @45 s, NOW @60 s, pipe 0 pressure) — the T1 lines encode the hash, not the events, so verify via the warning events visible in the T1's manifest comments/context and by cross-checking the pinned test values in core/warnings_test.odin + the implementation spec's I/O matrix. A mismatch = a real defect.
- **A header inconsistency**: warn.t1's catalog_hash != bd13d5dfba445d80 (the same hash every other demo carries), ticks != 1500, seed/demo name mismatch (warn/4243).
- **A capture-frame error**: capture times not at 1500/45000/65000 ms, or a PNG missing from the golden set (warn needs all 3).
- **The demo not being launchable/honest**: the .dem directives contradict the narrative (draw times, era, fixture), or the log.bin missing/empty."""

LEGIT_C3 = """- **qos.t1 header inconsistency**: catalog_hash != bd13d5dfba445d80, ticks != 1500, demo name/seed mismatch (qos/3003).
- **A per-tick line that suggests behavioral drift beyond the documented causes**: e.g. Packet_Dropped stream changes that look like an E9/E22 inversion (Express dropped while Standard/Best in flight) or E7 starvation (a lane idle for a long window while others run) — a blocker.
- **The 01000ms.png changing when it should be a no-strain frame** (early qos is pre-saturation — its pixels should be unchanged from base) — vs the 65000ms.png which may legitimately carry the panel + rings (documented cause (c)).
- **A stale/incomplete re-bless**: hash lines identical to the old blessed hash (afe505119369d195) despite the fold (would mean the golden wasn't actually re-blessed at this sha)."""

LEGIT_C4 = """- **A negative-proof PNG in the diff**: boot/draw/flow/win/bundle/ecmp/place/demolish PNGs must be byte-identical (absent). The ONLY documented T2 shift in this chunk is lose/03000ms.png. Anything else = unaccounted drift = a blocker.
- **A .t1 header mismatch**: demo name, seed, or tick count changed (they must NOT — only the hash lines + catalog_hash header line re-bless); catalog_hash != bd13d5dfba445d80.
- **A stale .log.bin** (3-4 line diff = binary header re-bless; a log.bin with NO diff despite the fold = stale bless = inconsistency).
- **A light demo whose .t1 didn't shift at all** (hash lines identical to afe505119369d195-era values) — a stale bless hides a real divergence."""

LEGIT_C5 = """- **A shift OUTSIDE the documented set**: any qos_contention/qos_emphasis/sla PNG that changed without a cause-doc (e.g. sla/10000ms.png — the relief frame — MUST be absent from the diff; a qos_emphasis capture that does not strain must stay byte-identical). Unaccounted = a blocker.
- **A .t1 header inconsistency**: catalog_hash != bd13d5dfba445d80, tick/seed/demo-name drift.
- **A drop-stream inversion in the T1s**: Express dropped while Standard/Best in flight in the same bundle queue (E22), or starvation windows (E7) — a blocker.
- **Stale .log.bins** (unchanged binary despite the fold) or missing golden files."""

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

This is a single-player desktop game core (Odin) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories will not apply; the realistic surface here is unsafe deserialization / missing validation at the JSON-catalog boundary (the new balance.json `warnings` block loader + the set-piece `forecast_lead_ticks` parse in catalog.odin) and integer-overflow/coercion at parse (percent math, tick math, u32 targets). `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation purity, ODN-3 QoS-inside-Flow, ODN-5 data-driven catalogs, ODN-11 save = seed + action log, ODN-13 no globals, ODN-10 arrays-only)?
- Will it create technical debt or make future changes harder (4.2's Crisis Engine lands on the same event seam)?
- Does complexity match the problem? Any premature abstraction?

`source` = "architecture".""",

"codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (e.g. `bundle_lane_count`, `Forecast_Entry`, `sp.forecast_lead_ticks` in core/demand.odin + core/catalog.odin, `crisis_make`/`crisis_destroy` wiring in run_init/run_destroy)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

`source` = "codebase".""",

"tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

The P0 critical paths here: the no-flicker contract (a healthy transit never strains — the transit-arrival case specifically, the documented reason the spawn-tick exclusion alone was insufficient), the strain math pins (70/90 ladder, 1 stuck packet on a router = amber 75%, 2 = red 150%, residential any = red 600%), pipe pressure vs the E9 bound (lone packet 17% healthy, lane at bound 100% = dropping, pressure replicating to member pipes), one-event-per-transition (None→Amber, Amber→Red, Red→Amber, Red→None, Amber→None — the cleared sign must name the level that ENDED), the forecast window boundaries (before lead / in window countdown / active 0 + NOW / after end), the forecast's purity (never fires), replay byte-identity with warning events + forecast rows [E10], the tag-conditional event serialization pin (pre-4.1 event bytes unchanged), LOG_VERSION stays 3, the zero-traffic neutrality (E24 — no events, no section bytes), the era-3 sandbox session (goal 0/cap 0), the new balance.json warnings fail-fast rows, and the warn.dem golden (T1 + T2 + replay gate).

Blind-spot heuristics to check:
- New/modified behavior without matching coverage (e.g. is there a test for the transition Red→Amber easing? for the forecast 'after end' row absence? for the dead-node-slot never-warns path? for a demolished node's resident packets?)
- Happy-path-only coverage where error handling is implied (fail-fast rows — tested?)
- New state transitions without boundary tests (strain exactly at 69/70/89/90/91; lane at exactly the bound)

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
        "c1": ("chunk 1 of 5 — code+docs+data+demos+harness", 1676, 21, "c1.patch"),
        "c2": ("chunk 2 of 5 — the new warn.dem goldens", 1529, 5, "c2.patch"),
        "c3": ("chunk 3 of 5 — the qos.dem golden", 3020, 4, "c3.patch"),
        "c4": ("chunk 4 of 5 — light-demo goldens (the negative proof)", 1437, 19, "c4.patch"),
        "c5": ("chunk 5 of 5 — contention/era-3 goldens (sla/qos_contention/qos_emphasis)", 1626, 14, "c5.patch"),
    }[chunk]
    desc, lines, files, patch = info
    diffpath = f"{OUT}/{patch}"
    chunkdesc = f"{desc}, {lines} lines, {files} files"
    outfile = f"{OUT}/{lens}-{chunk}.json"
    if lens == "blind":
        wtline = ""
        specline = ""
    else:
        wtline = f"- WORKTREE (verify every claim against the actual code here — your ground truth, detached at sha {SHA}): {WT}\n"
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
