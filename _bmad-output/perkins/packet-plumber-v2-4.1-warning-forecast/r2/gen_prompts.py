#!/usr/bin/env python3
"""Generate the 35 Perkins lens prompts for packet-plumber-v2-4.1-warning-forecast r2 (5 chunks).

Round 2 = re-review: the r1 findings (CHANGES_REQUESTED @ 9820a55) are claimed fixed at head
2a972bd. Lenses: (1) verify the r1 fixes landed (a missing/wrong fix IS a new finding —
category r1-fix-regression), (2) hunt NEW defects, (3) do NOT re-open r1 findings as new.
"""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r2"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.1-warning-forecast-r2"
SHA = "2a972bd"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards + r1 findings map): {OUT}/spec/perkins-briefing-r2.md
  - Job briefing (the implementing minion's spec): {OUT}/spec/job-briefing.md
  - Story 4.1 card: {OUT}/spec/stories-v2.md (Story 4.1 card at line 362; slice-4 framing above it)
  - Implementation spec (the minion's frozen spec — acceptance matrix + code map + the RE-BLESS cause-docs): {OUT}/spec/spec-4-1-warning-forecast.md (identical to the worktree copy)
  - Architecture invariants: {OUT}/spec/odin-architecture-v1.md — ODN-11 save = seed + action log (~line 687), §11.7 edge-case table (line 1592; E9/E10 at ~1608-1609), §6.x per-link buffering + lane bound (line ~964), T1 hash contract (line ~1353), the golden-stability rule (~line 1397)
  - Prior findings (r1 consolidated.json — ALREADY FILED, do not re-open): {OUT}/spec/prior-findings-r1.json"""

SCOPE_C1 = """v2 Story 4.1 — the warning/forecast system (the fun loop's telegraph, slice-4 opener): `core/warnings.odin` (NEW — `warning_evaluate` runs INSIDE core.step AFTER flow_step, BEFORE win_lose_eval; node strain = Σ bandwidth of packets that FAILED a forward attempt (`Packet.waiting_ticks >= 1` — a NEW serialized field incremented in flow.odin's forward pass when no route exists, cleared on every successful forward/drop-back; fresh spawns + fresh transit arrivals have 0 and NEVER strain — the no-flicker contract) ÷ `node_types[].throughput_units`; pipe pressure = the FULLEST lane queue's depth on the bundle vs its E9 bound (`lane_queue_packets × packet_bandwidth` — a lone packet 17% healthy, a lane at its bound 100% = dropping; levels replicate to every member pipe); forecast = era set-pieces in `[start_tick - forecast_lead_ticks, start_tick + duration_ticks)` with exact countdowns — a PURE read of the schedule, never fires anything (4.2's job). `Crisis_State` on `Run_State` (node_strain/pipe_strain/forecast — ALL DERIVED per tick, rebuilt identically on replay). `Warning_Raised`/`Warning_Cleared` events (tags 6/7, payload = sign + target, serialized TAG-CONDITIONALLY — append-only, pre-4.1 event bytes unchanged). serialize.odin gains the warnings section (absent-when-empty) + `waiting_ticks` rides the per-packet T1 hash. LOG_VERSION stays 3, no new commands. balance.json `warnings` block (70/90 ladder, 600/200/400-tick leads, fail-fast validated). The app: era-3 sandbox (goal 0 / cap 0 — win/lose is 4.3's), health rings + !/!! glyphs + pinned pulse table (never color alone), pressure halos, the WEATHER REPORT panel (`app/render/forecast.odin` — zero pixels when empty), harness capture signature gains crisis + tick + the panel. demos/warn.dem (NEW — the launchable golden) + demos/lose.dem tweak.
ROUND 2 (this round): the r1 rework is folded in — app/main.odin (HUD instruction + the leads-legend consuming balance.json's warning leads), app/render/forecast.odin (panel labels rows by the set-piece's CATALOG id), app/render/view.odin (pulse rates corrected: advance=1 amber → 1.25 Hz, advance=2 red → 2.5 Hz), core/catalog.odin (fail-fast hardened: missing keys default -1, amber >= 1, leads i32-validated > 0 before the u64 cast), core/catalog_test.odin + core/warnings_test.odin (+7 new pins: node easing Red→Amber/Amber→None, multi-member bundle replication, exact 69/70/89/90/91 boundaries + router 75/150 + residential 600, dead-node silence, stuck+healthy mixture + E29 drop-back, event byte layout, eval purity), core/qos_test.odin (the dump-walker state-parameterized), harness/{goldens,run}.odin (capture signature gains era), the spec's lose.dem contradiction fixed.
Files in THIS chunk (chunk 1 of 5 — code+docs+data+demos+harness): _bmad-output/implementation-artifacts/{epic-4-context.md, spec-4-1-warning-forecast.md}, app/{main.odin, render/forecast.odin, render/palette.odin, render/view.odin}, core/{catalog.odin, catalog_test.odin, determinism_test.odin, flow.odin, qos_test.odin, serialize.odin, step.odin, types.odin, warnings.odin (NEW), warnings_test.odin (NEW)}, data/balance.json, demos/{lose.dem, warn.dem (NEW)}, harness/{goldens.odin, run.odin}. Chunks 2-5 (the goldens) are SEPARATE lens waves — do not review them here."""

SCOPE_C2 = """v2 Story 4.1 — the warn.dem golden wave (chunk 2 of 5): goldens/warn.{log.bin, t1, 01500ms.png, 45000ms.png, 65000ms.png} — ALL NEW (warn.dem is the 4.1 launchable: era 3 + fixture qos + draws + lane categorization + a 30 s-delayed router->host pipe so streaming packets pile at the host). The .t1 (1513 lines) pins the forecast rows + the WHOLE warning event stream (E10): host Node_Strained @1 / Node_Critical @2 (75%/150% of the 80 u/s host), red until the 30 s draw opens the route, forecast panel from 30 s (600-tick lead) with countdown 300 @45 s, surge fires at 60 s (streaming x10) → panel reads NOW, pipe 0 saturates under email load → red/amber pressure halo. Captures: 1500 ms (strain telegraph, no panel yet), 45000 ms (countdown + red pressure), 65000 ms (surge ACTIVE NOW). ROUND 2: all 3 PNGs were re-blessed AGAIN at this sha, cause-documented: (a) the ring pulse-rate fix changed every visible ring's phase (amber advance 1, red advance 2 — the r1 rates were 16x slow); (b) the panel label changed from "SURGE xN" to the set-piece's catalog id. Verify: the T1's warning events match the narrative ticks exactly, the header carries the SAME catalog_hash as every other demo (bd13d5dfba445d80), and the captures are at the right times."""

SCOPE_C3 = """v2 Story 4.1 — the qos.dem golden wave (chunk 3 of 5): goldens/qos.{log.bin, t1, 01000ms.png, 65000ms.png}. qos.t1 is 3011 lines (1500 ticks @20 Hz = 75 s) — a LONG fixture demo whose re-bless is cause-documented: (a) catalog_hash fold (mechanical); (b) `waiting_ticks` rides the per-packet T1 hash (mechanical); (c) the 1 s capture gains E9-bound red pressure halos (~tick 8-20, review r1 W5 — now listed in the PR body's cause-list); (d) the 65 s capture gains the panel + surge strain (era-3 schedule). ROUND 2: the 65000ms.png was re-blessed AGAIN at this sha (panel label + ring pulse phase — cause-documented in the PR body); the 01000ms.png is NOT in the r2 re-bless set (its halos have no ring phase and no panel — should be byte-identical to its r1 state). Verify: header hash == bd13d5dfba445d80; ticks 1500; no per-tick line looks like an E9/E22 inversion or E7 starvation regression (spot-check the Packet_Dropped + Warning event stream around the surge)."""

SCOPE_C4 = """v2 Story 4.1 — the LIGHT-demo goldens wave (chunk 4 of 5): goldens/boot|bundle|demolish|draw|ecmp|flow|lose|place|win (.t1 + .log.bin; lose/03000ms.png is in the diff). The re-bless has TWO documented causes: (a) catalog_hash fold — the balance.json warnings block shifts EVERY .t1 hash line + .log.bin header (mechanical); (b) waiting_ticks bytes in per-packet serialization (mechanical). The NEGATIVE PROOF: boot/draw/flow/win/bundle/ecmp/place/demolish T2s (PNGs) are byte-identical — NONE of their PNGs may appear in this diff; lose/03000ms.png is the ONE documented T2 shift in this chunk (lose.dem's own stuck packet — the residential telegraphs 🔴, cause-documented; the r1 N3 spec contradiction about lose is fixed at head). Verify: zero per-tick .t1 lines that look like BEHAVIORAL drift beyond the fold+field bytes (verify manifest STRUCTURE: header fields, tick counts, seed/demo names, hash consistency); PNGs exactly {lose/03000ms.png} — nothing else; .log.bin headers re-blessed (3-4 line diffs = binary header bytes)."""

SCOPE_C5 = """v2 Story 4.1 — the contention/era-3 goldens wave (chunk 5 of 5): goldens/qos_contention.* (3 PNGs), goldens/qos_emphasis.* (3 PNGs), goldens/sla.* (01000ms.png + 04000ms.png — NOTE sla/10000ms.png is NOT in the diff: the relief frame — zero strain at 10 s — is the NEGATIVE PROOF inside the shifted demo). Cause-documented T2 shifts: sla + qos_contention (the saturated router row gains rings/halos at strained captures), qos_emphasis (era-3 load — gains rings if its captures strain). ROUND 2: the ring pulse-rate fix changed every visible ring's phase, yet the r2 delta re-blessed ONLY warn (3 PNGs) + qos 65s — the minion claims these captures render pixel-identical at the new pulse phases (Perkins verified: `tools/harness.sh run` green at 2a972bd, 14/14). Verify: the shifted PNG set is EXACTLY the documented set (sla/10000ms.png + all qos_contention/qos_emphasis PNGs must stay byte-identical — absent from the diff); the .t1 header catalog_hash == bd13d5dfba445d80; manifest structure consistent (ticks, seeds, demo names); .log.bin re-blessed headers only."""

GUARDS = """- **🚨 THE ODN-11 RE-BLESS — verify the CAUSE-DOCUMENTATION, don't auto-flag.** Re-blessed deliberately: (a) catalog_hash fold — mechanical (new balance.json warnings block folds into EVERY .t1 hash line + .log.bin header); (b) waiting_ticks rides the per-packet T1 hash (mechanical); (c) T2 telegraph shifts — cause-documented PER DEMO (sla + qos_contention + qos_emphasis + qos 1s + qos 65s + lose; boot/draw/flow/win/bundle/ecmp/place/demolish T2s byte-identical — the negative proof); (d) ROUND-2 re-bless — warn (3 PNGs: ring pulse phase + panel label) + qos 65s (panel label), cause-documented in the PR body. VERIFY the negative proof + the cause-docs. A re-bless with an unaccounted shift = a BLOCKER.
- **🚨 THE NO-FLICKER CONTRACT — load-bearing.** Node strain uses `Packet.waiting_ticks` (a NEW serialized field). A HEALTHY transit must NEVER strain. A flicker or a strain signal without a real backlog = a blocker. Also: `waiting_ticks` is NEW SERIALIZED STATE — LOG_VERSION must stay 3 and old-log acceptance stays intact [E10]; the action-log FORMAT must be unchanged. A log-format change or LOG_VERSION bump = a blocker.
- **PIPE PRESSURE vs [E9].** Pressure = fullest lane queue depth on the bundle ÷ its E9 bound (`lane_queue_packets × packet_bandwidth`). A lane at its bound = 100% = the ladder is dropping. A pressure computation disconnected from the real E9 bound (wrong bound, wrong lane, off-by-one at the bound) = a real defect.
- **FORECAST READS THE SCHEDULE, NEVER FIRES.** The forecast must be PURE (no state mutation beyond the derived rows, no events, no side effects, no win/lose interaction). A forecast that mutates state or fires events = a blocker.
- **EVENTS TAGS 6/7 + SIGN/TARGET.** Warning_Raised/Cleared with sign+target, tag-conditional payload (bytes written ONLY for tags 6/7 — append-only); replay byte-identity pinned. A broken tag or a payload written unconditionally = a real defect.
- **NEVER COLOR ALONE.** Health rings + !/!! glyphs + tick-derived pulse — the warning render must be distinguishable without color. A color-only warning render = a blocker.
- **WEATHER REPORT PANEL — ZERO PIXELS WHEN EMPTY.** A panel that draws pixels while empty = a real defect.
- **ERA-3 SANDBOX (goal/cap 0 — win/lose is 4.3's).** Do NOT flag "win/lose not implemented" — 4.3 owns it.
- **No re-open of slice-1..3.4 findings** (merged + Perkins-approved) — carry-forward only.
- **No re-open of the r1 4.1 findings** (below) — they are ALREADY FILED. Verify their fixes landed instead.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–3 + 3.5 + 3.2–3.4 + canon). demand.odin / routing.odin / qos.odin / win_lose.odin are BASE files — read-only context, not review targets.
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha."""

LEGIT_C1 = """- **A healthy-transit strain (flicker)** — a blocker (the no-flicker contract).
- **A LOG_VERSION bump or an action-log format change** from waiting_ticks — a blocker [E10]. Old-log acceptance unchanged.
- **A forecast that fires/mutates** — a blocker.
- **A pressure computation disconnected from the E9 bound** — a real defect.
- **A color-only warning render** — a blocker (accessibility).
- **The WEATHER REPORT panel drawing pixels while empty** — a real defect.
- **An event-payload bug**: tags 6/7 payload written unconditionally, sign/target serialized in the wrong order, one event per transition violated, or a transition that clears the wrong sign (e.g. Amber→None clearing Node_Critical instead of Node_Strained).
- **A waiting_ticks bookkeeping bug**: increment on a path that isn't a failed attempt, missing clear on success, strain counted from delivered/on_edge packets, or strain attributed to the wrong node slot.
- **An integer bug**: `nload × 100 / throughput` overflow/order, u32→i64 narrowing, slot-index vs node-id confusion.
- **A catalog validation gap**: the r2 fail-fast (missing keys → -1, amber >= 1, leads i32-checked pre-cast) rejecting something legal, or missing a rejection it claims (a negative lead slipping through, a partial block loading silently).
- **A determinism break [E10]**: an unordered walk, a non-deterministic transition baseline, resize() semantics mishandled.
- **An r1 fix that did NOT land or landed WRONG** (see the r1 findings map below) — category "r1-fix-regression". Perkins verified the badge-out green (104 core / 14 harness / 97 drift / lint 5/5 / app builds) — a claimed-fixed item that is actually missing/wrong is exactly what this lens must catch.
- **An `odin test` / `odin build` / harness failure at 2a972bd** (Perkins ran these green — if you find a failure, re-run to confirm before filing; a confirmed failure is a blocker)."""

LEGIT_C2 = """- **The warn.t1 event stream NOT matching the demo narrative** (Node_Strained @1, Node_Critical @2, red until the 30 s draw, forecast from 30 s with countdown 300 @45 s, NOW @60 s, pipe 0 pressure) — verify via the warning events visible in the T1's manifest comments/context and by cross-checking the pinned test values in core/warnings_test.odin + the implementation spec's I/O matrix. A mismatch = a real defect.
- **A header inconsistency**: catalog_hash != bd13d5dfba445d80, ticks != 1500, seed/demo name mismatch (warn/4243).
- **A capture-frame error**: capture times not at 1500/45000/65000 ms, or a PNG missing from the golden set (warn needs all 3).
- **The demo not being launchable/honest**: the .dem directives contradict the narrative (draw times, era, fixture), or the log.bin missing/empty."""

LEGIT_C3 = """- **qos.t1 header inconsistency**: catalog_hash != bd13d5dfba445d80, ticks != 1500, demo name/seed mismatch (qos/3003).
- **A per-tick line that suggests behavioral drift beyond the documented causes**: e.g. Packet_Dropped stream changes that look like an E9/E22 inversion or E7 starvation — a blocker.
- **A shift OUTSIDE the r2 documented set**: the 65000ms.png re-bless is documented (panel label + pulse); the 01000ms.png must NOT have re-blessed again in r2 (it is in the full PR diff — from r1's halos — but its r1→r2 delta must be absent). An undocumented r2 shift = a blocker.
- **A stale/incomplete re-bless**: hash lines identical to the old blessed hash despite the fold."""

LEGIT_C4 = """- **A negative-proof PNG in the diff**: boot/draw/flow/win/bundle/ecmp/place/demolish PNGs must be byte-identical (absent). The ONLY documented T2 shift in this chunk is lose/03000ms.png. Anything else = unaccounted drift = a blocker.
- **A .t1 header mismatch**: demo name, seed, or tick count changed (they must NOT — only the hash lines + catalog_hash header line re-bless); catalog_hash != bd13d5dfba445d80.
- **A stale .log.bin** (a log.bin with NO diff despite the fold = stale bless = inconsistency).
- **A light demo whose .t1 didn't shift at all** — a stale bless hides a real divergence."""

LEGIT_C5 = """- **A shift OUTSIDE the documented set**: any qos_contention/qos_emphasis/sla PNG that changed without a cause-doc (sla/10000ms.png — the relief frame — MUST be absent from the diff). Unaccounted = a blocker.
- **A .t1 header inconsistency**: catalog_hash != bd13d5dfba445d80, tick/seed/demo-name drift.
- **A drop-stream inversion in the T1s**: Express dropped while Standard/Best in flight in the same bundle queue (E22), or starvation windows (E7) — a blocker.
- **Stale .log.bins** (unchanged binary despite the fold) or missing golden files."""

PRIOR = """## R1 FINDINGS — ALREADY FILED, DO NOT RE-OPEN (verify the fixes instead)

Perkins r1 (CHANGES_REQUESTED @ 9820a55) filed 1 blocker + 6 warnings + 7 notes. The r2 rework claims ALL addressed. A fix that is MISSING or WRONG at this sha = a NEW finding (category "r1-fix-regression"). The claims (from the PR body):

- **B1 (blocker, test gate)** — fixed via 7 new tests in core/warnings_test.odin: (g) test_node_strain_easing_partial_relief — node Red→Amber easing (CLEARED Node_Critical while strained persists) + Amber→None (CLEARED Node_Strained) via the dst-split partial-relief path; (h) test_pipe_pressure_multi_member_bundle — a two-pipe parallel bundle replicates the pressure level to BOTH member slots + one raise/clear event pair PER MEMBER; (i) test_strain_ladder_boundaries_and_pins — exact 69/70/89/90/91 boundaries on strain_level + the router 75/150% + residential 600% + host 37/75/112% math + integration pins; (j) test_warning_dead_node_silent — demolished node reads None with NO phantom cleared event + resident packets culled; (k) test_stuck_mixture_and_e29_dropback_clear — a waiting-0 packet is never counted beside a real pile + the E29 drop-back re-tries fresh; (l) test_event_payload_byte_layout + test_warning_evaluate_idempotent_and_pure — tag-conditional bytes + eval purity.
- **W1 (pulse 16x slow)** — fixed: pulse_factor advances TABLE ENTRIES per tick (amber advance=1 → 16-tick cycle = 1.25 Hz; red advance=2 → 8-tick cycle = 2.5 Hz); the comments' math corrected. Verify the rates are actually 1.25/2.5 Hz at 20 Hz logic.
- **W2 (leads dead config)** — fixed: the app HUD legend now consumes all three balance leads as seconds (strained ~30 s / critical ~10 s / pipe ~20 s at logic_hz). Verify the legend's claims are HONEST — do the displayed windows correspond to anything the sim enforces? (The r1 fix options were "consume with real semantics" OR "strike the claims" — a caption that promises a reaction window the sim doesn't honor would be a new finding, not a re-open.)
- **W3 (negative lead u64 wrap)** — fixed: leads parse as i32 and validate > 0 BEFORE the u64 cast; negative rows added to the fail-fast test. Verify.
- **W4 (partial warnings block → permanent Amber)** — fixed: missing keys default to -1 (a partial block is a load error) + amber >= 1 required. Verify.
- **W5 (qos/01000ms.png missing from the cause list)** — the PR body's Golden re-bless proof now lists it ("qos: 1s capture gains the pressure halos — review r1 W5"). Verify the PR body does; note if the spec file's own Golden bullet still omits it.
- **W6 (router/residential ladder pins)** — covered by (i). Verify.
- **N1 (sandbox HUD "deliver a packet to win")** — app/main.odin reworded. Verify.
- **N2 (panel hardcodes "SURGE")** — app/render/forecast.odin now labels rows by the set-piece's CATALOG id via era + sp_index. Verify the lookup bounds (era-1 indexing, sp_index vs the era's set-piece array) are correct.
- **N3 (lose.dem spec contradiction)** — the spec's Design Notes + Verification lists now exclude lose with the cause-doc. Verify.
- **N4 (dump-walker latent misparse)** — qos_first_word_after_topology now state-parameterized and skips the SLA + warnings sections; a strained-dump walk case added. Verify the walker's section-skip matches the writer's layout exactly.
- **N5/N6/N7 (smaller coverage gaps)** — covered by (i)(j)(k)(l) + test_warning_replay_byte_identical. Verify nothing was silently dropped."""

OUTPUT_CONTRACT = """Write ONLY a valid JSON array to your output file (named below). No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
Each element MUST match this schema exactly:
{
  "source": "<your assigned source value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag — use 'r1-fix-regression' for a missing/wrong r1 fix>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase; do not reconstruct from memory.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}"""

ACCURACY = """ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer."""

LENSES = {
    "blind": {
        "header": """**You are the `blind` lens. Your assigned `source` tag is `blind`. Your output file is `{json_out}`.**

You are ONE lens in a Perkins automated PR-review swarm (round 2 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent.

## Your inputs (READ THESE)
- CANONICAL DIFF — chunk {chunk} of 5 ({chunk_desc}, {chunk_lines} lines): {patch_file}""",
        "brief": """You are a cynical, jaded reviewer with zero patience for sloppy work. BLINDNESS RULE: the diff file is ALL the context you may use. Do NOT read the worktree, the specs, or any other file — reading anything beyond the diff INVALIDATES your lens. Assume problems exist; be skeptical; look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (the comments / commit message)
- An r1 fix claimed in the diff comments that is NOT what the comment says

Your `evidence` MUST be exact diff lines pasted verbatim from the diff file. `source` = "blind".""",
    },
    "edge": {
        "brief": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, off-by-one errors, implicit type coercion (u64/i32 casts — the r2 catalog fail-fast does several), state the new code doesn't account for, input the new code doesn't validate, era-1 indexing bounds (the r2 panel label lookup), pulse-table indexing (the r2 advance math).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.""",
    },
    "acceptance": {
        "brief": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria (story 4.1's Given/When/Then + the job briefing's condensed acceptance)
- Deviations from spec intent (the FORGE #3 lead-time surface, the P3 fairness surface)
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec (4.1 is telegraph ONLY: no crisis firing, no win/lose, no new player commands — LOG_VERSION 3)
- An r1 finding whose claimed fix contradicts the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).""",
    },
    "security": {
        "brief": """OWASP-oriented security review of the diff. Identify:
- Missing input validation at system boundaries (the balance.json JSON parsing + the warnings-block fail-fast)
- Unsafe type-cast handling (u64(i32) wrap — the r2 fix claims this is closed; verify no OTHER cast path has the same trap)
- Data exposure (sensitive fields in responses, logs, or client-visible state — low-stakes here, but check)
- Unsafe deserialization, insecure defaults
- The dump writer/reader pair: any buffer over-read or length confusion in the r2 state-parameterized walker or the event-payload writer""",
    },
    "architecture": {
        "brief": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (Odin idioms §11.5: proc-pointer tables, tagged unions, arrays-only, no map iteration in core, integer sim, balance numbers in data/)?
- Does the r2 rework respect the deterministic-core spine (ODN-10/ODN-11/E10 — pulse math must stay integer + virtual-time derived; the HUD legend must stay view-side; the catalog fail-fast must stay load-time)?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries (core purity — no vendor imports; the render reads balance leads from the catalog, not re-stated)?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?""",
    },
    "codebase": {
        "brief": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (e.g. the r2 panel-label lookup reads cat.demand.eras[era-1].set_pieces[sp_index].id — does that field exist, is the indexing right? does pulse_factor's new signature match ALL its callers? does draw_forecast_panel's new era parameter match all call sites — app + harness?)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change? (e.g. the OLD pulse step semantics, the old forecast label strings)""",
    },
    "tests": {
        "brief": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- The r2 fail-fast branches in core/catalog.odin — is EVERY new rejection row covered (missing-key default, amber 0, negative leads, lead 0)?
- The r2 panel-label lookup bounds (era 0, era out of range, sp_index out of range) — covered?
- The r2 pulse math (advance 1/2, phase wraparound at & 15) — covered?
- The r2 dump-walker section-skip (SLA present, warnings present, both absent) — covered?
- The +7 warnings tests themselves — do they assert the CLAIMED events (easing, replication, boundaries, dead-node silence)?

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
- FAIL: P0 <100%, or P1 <80%, or overall <80%""",
    },
}

LENS_ORDER = ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]

CHUNK_DESCS = {
    "c1": "code+docs+data+demos+harness (21 files)",
    "c2": "warn.dem goldens (5 files)",
    "c3": "qos.dem goldens (4 files)",
    "c4": "light-demo goldens — negative proof (19 files)",
    "c5": "contention/era-3 goldens sla+qos_contention+qos_emphasis (14 files)",
}

SCOPES = {"c1": SCOPE_C1, "c2": SCOPE_C2, "c3": SCOPE_C3, "c4": SCOPE_C4, "c5": SCOPE_C5}
LEGITS = {"c1": LEGIT_C1, "c2": LEGIT_C2, "c3": LEGIT_C3, "c4": LEGIT_C4, "c5": LEGIT_C5}

os.makedirs(f"{OUT}/prompts", exist_ok=True)
for cname in ["c1", "c2", "c3", "c4", "c5"]:
    chunk_lines = len(open(f"{OUT}/{cname}.patch").read().splitlines())
    for lens in LENS_ORDER:
        json_out = f"{OUT}/{lens}-{cname}.json"
        patch_file = f"{OUT}/{cname}.patch"
        cfg = LENSES[lens]

        if lens == "blind":
            parts = [
                cfg["header"].format(json_out=json_out, chunk=cname[1:], chunk_desc=CHUNK_DESCS[cname], chunk_lines=chunk_lines, patch_file=patch_file),
                "\n## The PR (scope)\n", SCOPES[cname],
                "\n## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)\n", GUARDS,
                "\n## Legitimate findings here WOULD be\n", LEGITS[cname],
                "\n## " + PRIOR,
                "\n## " + ACCURACY,
                "\n## YOUR LENS BRIEF\n", cfg["brief"],
                f"\n## OUTPUT CONTRACT\n{OUTPUT_CONTRACT}\n\n## DONE\nWrite your JSON array to `{json_out}` and stop. Do not fix anything. Do not run the interactive fix flow.\n",
            ]
        else:
            parts = [
                f"""**You are the `{lens}` lens. Your assigned `source` tag is `{lens}`. Your output file is `{json_out}`.**

You are ONE lens in a Perkins automated PR-review swarm (round 2 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha (2a972bd).

## Your inputs (READ THESE)
- CANONICAL DIFF — chunk {cname[1]} of 5 ({CHUNK_DESCS[cname]}, {chunk_lines} lines, review exactly these bytes): {patch_file}
- Worktree (verify every claim by READING files here — {WT}):
  - {OUT}/spec/perkins-briefing-r2.md (your charter)
  - {OUT}/spec/job-briefing.md
  - {OUT}/spec/stories-v2.md (Story 4.1 at line 362)
  - {OUT}/spec/spec-4-1-warning-forecast.md (the minion's frozen spec — acceptance + code map + re-bless cause-docs)
  - {OUT}/spec/odin-architecture-v1.md (ODN-11 ~line 687, §11.7 line 1592, E9/E10 ~1608-1609, §6.x lane bound ~964, T1 contract ~1353, golden rule ~1397)
  - {OUT}/spec/prior-findings-r1.json (r1 findings — ALREADY FILED)

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

## The PR (scope)
""",
                SCOPES[cname],
                "\n## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)\n", GUARDS,
                "\n## Legitimate findings here WOULD be\n", LEGITS[cname],
                "\n## " + PRIOR,
                "\n## " + ACCURACY,
                "\n## YOUR LENS BRIEF\n", cfg["brief"],
                f"\n## OUTPUT CONTRACT\n{OUTPUT_CONTRACT}\n\n## DONE\nWrite your JSON array to `{json_out}` and stop. Do not fix anything. Do not run the interactive fix flow.\n",
            ]
        prompt = "\n".join(parts)
        open(f"{OUT}/prompts/{lens}-{cname}.md", "w").write(prompt)

print("wrote 35 prompts to", f"{OUT}/prompts/")
