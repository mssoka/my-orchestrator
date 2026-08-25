# Perkins lens prompt — security (chunk 1 of 5 — code+docs+data+demos+harness, round 1)

**You are the `security` lens. Your assigned `source` tag is `security`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/security-c1.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — chunk 1 of 5 — code+docs+data+demos+harness, 1676 lines, 21 files (review exactly these bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/c1.patch
- WORKTREE (verify every claim against the actual code here — your ground truth, detached at sha 9820a55): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.1-warning-forecast-r1
- SPEC / CONTEXT (read the sections named; full files):
  - Perkins briefing (your charter + lens-guards): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/spec/job-briefing.md
  - Story 4.1 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/spec/stories-v2.md (Story 4.1 card at line 362; slice-4 framing above it)
  - Implementation spec (the minion's frozen spec — acceptance matrix + code map + the RE-BLESS cause-docs): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/spec/spec-4-1-warning-forecast.md — copy the diff's first file (identical to the worktree copy at _bmad-output/implementation-artifacts/spec-4-1-warning-forecast.md); the re-bless documentation lives in "Boundaries" + "Design Notes"
  - Architecture invariants: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/spec/odin-architecture-v1.md — ODN-11 save = seed + action log (~line 687), §11.7 edge-case table (line 1592; E9/E10 at ~1608-1609), §6.x per-link buffering + lane bound (line ~964), T1 hash contract (line ~1353), the golden-stability rule (~line 1397)


## The PR (scope)
v2 Story 4.1 — the warning/forecast system (the fun loop's telegraph, slice-4 opener): `core/warnings.odin` (NEW — `warning_evaluate` runs INSIDE core.step AFTER flow_step, BEFORE win_lose_eval; node strain = Σ bandwidth of packets that FAILED a forward attempt (`Packet.waiting_ticks >= 1` — a NEW serialized field incremented in flow.odin's forward pass when no route exists, cleared on every successful forward/drop-back; fresh spawns + fresh transit arrivals have 0 and NEVER strain — the no-flicker contract) ÷ `node_types[].throughput_units`; pipe pressure = the FULLEST lane queue's depth on the bundle vs its E9 bound (`lane_queue_packets × packet_bandwidth` — a lone packet 17% healthy, a lane at its bound 100% = dropping; levels replicate to every member pipe); forecast = era set-pieces in `[start_tick - forecast_lead_ticks, start_tick + duration_ticks)` with exact countdowns — a PURE read of the schedule, never fires anything (4.2's job). `Crisis_State` on `Run_State` (node_strain/pipe_strain/forecast — ALL DERIVED per tick, rebuilt identically on replay). `Warning_Raised`/`Warning_Cleared` events (tags 6/7, payload = sign + target, serialized TAG-CONDITIONALLY — append-only, pre-4.1 event bytes unchanged). serialize.odin gains the warnings section (absent-when-empty) + `waiting_ticks` rides the per-packet T1 hash. LOG_VERSION stays 3, no new commands. balance.json `warnings` block (70/90 ladder, 600/200/400-tick leads, fail-fast validated). The app: era-3 sandbox (goal 0 / cap 0 — win/lose is 4.3's), health rings + !/!! glyphs + pinned pulse table (never color alone), pressure halos, the WEATHER REPORT panel (`app/render/forecast.odin` — zero pixels when empty), harness capture signature gains crisis + tick + the panel. demos/warn.dem (NEW — the launchable golden) + demos/lose.dem tweak. `_bmad-output/implementation-artifacts/` = epic-4 context + the frozen implementation spec (read the re-bless cause-docs!).
Files in THIS chunk (chunk 1 of 5 — code+docs+data+demos+harness): _bmad-output/implementation-artifacts/{epic-4-context.md, spec-4-1-warning-forecast.md}, app/{main.odin, render/forecast.odin, render/palette.odin, render/view.odin}, core/{catalog.odin, catalog_test.odin, determinism_test.odin, flow.odin, qos_test.odin, serialize.odin, step.odin, types.odin, warnings.odin (NEW), warnings_test.odin (NEW)}, data/balance.json, demos/{lose.dem, warn.dem (NEW)}, harness/{goldens.odin, run.odin}. Chunks 2-5 (the goldens) are SEPARATE lens waves — do not review them here.

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- **🚨 THE ODN-11 RE-BLESS — verify the CAUSE-DOCUMENTATION, don't auto-flag.** Re-blessed deliberately: (a) catalog_hash fold — mechanical (new balance.json warnings block folds into EVERY .t1 hash line + .log.bin header, because catalog_hash bytes ride INSIDE the T1 hash stream); (b) waiting_ticks rides the per-packet T1 hash (4 new bytes per in-flight packet per tick — mechanical; the field is documented in serialize.odin); (c) T2 telegraph shifts — cause-documented PER DEMO in the implementation spec (sla + qos_contention + qos_emphasis + qos 65s + lose; boot/draw/flow/win/bundle/ecmp/place/demolish T2s byte-identical — the negative proof). VERIFY the negative proof (those demos' PNGs absent from the diff) + the cause-docs. A re-bless with an unaccounted shift (a negative-proof demo's PNG in the diff, a relief frame shifting, a zero-traffic demo's T2 moving) = a BLOCKER.
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
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha.

## Legitimate findings here WOULD be
- **A healthy-transit strain (flicker)**: a node warning while its stuck backlog is empty, or a strain signal from a packet that forwards next tick — a blocker (the no-flicker contract).
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
- **An `odin test` / `odin build` / harness failure at 9820a55** (Perkins ran these green — core 97, demos 14 incl. warn.dem, drift 97, lint 5/5 — if you find a failure, re-run to confirm before filing; a confirmed failure is a blocker).

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

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a single-player desktop game core (Odin) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories will not apply; the realistic surface here is unsafe deserialization / missing validation at the JSON-catalog boundary (the new balance.json `warnings` block loader + the set-piece `forecast_lead_ticks` parse in catalog.odin) and integer-overflow/coercion at parse (percent math, tick math, u32 targets). `[]` is an honest answer. `source` = "security".

## DONE
Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/security-c1.json` and stop. Do not fix anything. Do not run the interactive fix flow.
