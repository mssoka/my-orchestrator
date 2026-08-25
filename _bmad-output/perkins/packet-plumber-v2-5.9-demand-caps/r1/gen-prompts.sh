#!/bin/bash
# gen-prompts.sh — emit the 7 lens briefs for perkins r1 (packet-plumber-v2-5.9-demand-caps)
set -eu
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.9-demand-caps-r1
P=$OUT/prompts
mkdir -p "$P"

read -r -d '' SHARED_HEAD <<'EOF' || true
You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.9-demand-caps-r1/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); events, not callbacks (ODN-14); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1/lens-diff.patch (1465 lines, unified format, PR #62 of solarity-services/Packet-Plumber, base branch v2 @ 18781a4, story 5.9 "per-terminal demand caps"). These exact bytes are the review target — never re-fetch or regenerate the diff. The PR also re-blessed 93 golden files; their summarized surface is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1/golden-manifest.txt — Perkins has ALREADY byte-verified the re-bless mechanically (all 31 .log.bin differ ONLY in the 8-byte catalog_hash field at bytes 17..24; the PNG set is exactly the 29 cause-documented frames incl. the growth/05500ms.png→01500ms.png rename; catalog_hash rides inside every per-tick state hash via core/serialize.odin:111 so every .t1 line shifting is the mechanical fold). Do NOT re-derive golden bytes and do NOT run the test suite (Perkins ran tools/ci-local.sh: 9/9 gates green at the reviewed sha) — review CODE.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.9-demand-caps-r1 — a checkout at exactly the reviewed sha (2314a22c9ffd4de4591c1690ffa2477a8862d0e4). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins briefing (the r1 guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1/spec/perkins-briefing-r1.md
- Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1/spec/job-briefing.md
- Story 5.9 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1/spec/stories-v2.md — the section "### Story 5.9 — Per-terminal demand caps" at line 686 (its pinned acceptances W9/W10/W7/W6/N9 are CONTRACTS written from prior Perkins rounds, not guidance).
- Design spec (the user ruling 2026-08-15 — the accumulator design IS the ruling; do not re-litigate it): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1/spec/spec-traffic-model.md — §Thread 2 at line 111.
- Architecture canon: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1/spec/odin-architecture-v1.md — ODN-10 integer-only state paths, ODN-5 catalog single-source + fail-fast, E10 replay byte-identity, E22 pool backstop, E24 SLA accounting identity (the E-contract glossary ~line 1600).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [THE ONE HARD BLOCKER CLASS — the accumulator honors its contracts]: `spawn_credit_milli[terminal_slot]` in `Flow_State` beside `lane_caps`; updated IN PLACE in flow.odin §1b; derived + NEVER serialized (the lane_caps precedent); integer-only (ODN-10, jint_strict at catalog load); accrue = cap_fraction_permille × throughput ÷ packet_bandwidth milli/tick; spawn costs 1000; pickable while credit >= 1000; MAX_CREDIT_MILLI = 1000 × max(1, ceil(cap)) type-relative. cap_fraction_permille = 500 in balance.json (1..1000 fail-fast). A violation of ANY of these = a blocker.
- [Credit-gated eligibility]: over-cap terminals ineligible for source picks; eligible set = the live credit-gated subset (rebuilt per pick — consumption moves terminals out mid-tick); ONE rng draw per pick [ODN-10] preserved (the gating filters BEFORE the draw — no rejection sampling); the legacy §1a `flow_seed_demand` fixture path is EXEMPT (N9) — do not flag its uncapped spawning.
- [E24 invariant]: a credit-gated skip is NOT a demand event (never reaches sla_count_demand); a pool-dropped arrival IS; demand_seen == delivered + dropped + live under BOTH paths (the pin lives at sla_test.odin:88 `sla_check_invariant`, called per tick by sla_record_run — Perkins verified it is real and exercised by the new E24 test; your job is to find any PATH that breaks it, e.g. a spawn/drop that misses its accounting).
- [Quantitative acceptances W9/W10 must be NON-VACUOUS]: W9 (seed 4243, era 3 + growth + ×10 surge window [1200,3000): ≥ expected×0.95 streaming spawns in the window, per-terminal spawns ≤ cap×window + burst, credit ≤ MAX_CREDIT, ≥8 growth-born hosts); W10 (one-subscriber-at-cap zero-drop at its own access + transit ≤ class tolerance). The minion claims a fixture fix (the W10 sink draw previously referenced a nonexistent node id — silently rejected → vacuous pin) + `!replay_error` guards. A vacuous pin here is blocker-class: verify the W10 fixture wires real pipes (sla_draw to real node ids), delivers > 0, and the sourcing res actually sources ~50 emails over 600 ticks.
- [Re-pins are structural, not golden re-blesses]: demand_test + flow_test + determinism_test carry POSITIVE (cap honored) + NEGATIVE (no unbounded burst) assertions. crisis/health/node_health/stats collateral re-pins are cause-commented and preserve test INTENT (several crisis tests raise the cap to 1000 to exercise the ENGINE at full-rate arrival — documented; the cap's own pins are W9/W10). Flag a re-pin that silently WEAKENS a test's contract.
- [Surge re-validation TOGETHER]: era-3 demand profile (email 4→1, streaming 2→1) + growth pacing (GROWTH_INTERVAL_TICKS 120→40) + the ×10 surge multiplier are re-validated as a unit in test_w9_surge_lands_under_caps — silent surge non-landing is a fail. Eras 1/2 volumes are intentionally UNCHANGED (dormant in the MVP; the era-FSM story owns them) — do not flag.
- [Re-bless discipline — Perkins-verified mechanically]: do not re-derive. Flag only code paths that could hide semantic drift in a FUTURE re-bless.
- [Lane awareness]: this branch lands PRE-juice frames; the sibling 7.1 re-blesses T2 on top. Flag any finding whose fix would force 7.1's rebase into conflict (i.e. anything requiring ANOTHER T2 golden churn beyond the documented set).
- [What NOT to re-litigate]: the spec-traffic-model Section B ruling (the accumulator design itself); the W6 sink-side admit accumulator (documented balance-time option — out of scope); 5.10's narrow-access resize (the NEXT card); the 4.2/5.1 era profile semantics beyond the owned re-tune; the E9 sink concentration design; prior approved rounds' ground (5.4 intent layer, 5.5 demolish, 7.2 audio, the doctrine reframe).
- The base is `v2`. Files NOT in the diff are read-only context.
EOF

read -r -d '' SCHEMA <<'EOF' || true

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
EOF

file_contract () {
  cat <<EOF

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
$OUT/$1.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens $1 complete — N findings written".
EOF
}

# ---------- blind ----------
cat > "$P/blind.md" <<EOF
You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

ISOLATION CONTRACT — this is a BLIND review: the two files named in this section are the ONLY things you may read. Reading anything else (repository files, specs, docs, prior reviews) invalidates your lens. Do not explore any directory. Do not open any other file. Your tools are to be used ONLY on these two files:

1. The diff (read it FIRST and IN FULL): $OUT/lens-diff.patch (1465 lines, unified format; PR #62 of solarity-services/Packet-Plumber, base branch v2; title "Story 5.9 — Per-terminal demand caps (endpoints never self-congest)"). These exact bytes are the review target.
2. The golden-change manifest (the PR also re-blessed 93 golden files; their surface is summarized here): $OUT/golden-manifest.txt

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed — e.g. a comment that still cites the OLD value after a re-tune)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

Context you may infer from the diff itself only: this is an Odin-language deterministic game (pure integer sim core \`core/\`, raylib app layer, golden-image harness). The PR adds a per-terminal spawn-credit accumulator (integer milli-packet units) gating the demand director's source picks, a \`cap_fraction_permille\` balance field, an era-3 demand re-tune (email 4→1, streaming 2→1), a growth-interval re-tune (120→40), and collateral test re-pins. Your \`source\` value is "blind".
$SCHEMA
$(file_contract blind)
EOF

# ---------- edge ----------
cat > "$P/edge.md" <<EOF
$SHARED_HEAD

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Classes this diff suggests (verify each in the worktree, then walk PAST them to the ones nobody listed): boundary conditions (empty eligible set, zero accrual, credit exactly at threshold, u32 clamp boundary), integer division/truncation edges, node-slot vs node-id confusion, dead-terminal slots with stale credit, growth-born nodes mid-tick, the credit-consumed-but-dst-pick-failed path, the pool-dropped arrival path vs the credit-gated skip path (E24 accounting on BOTH), era transitions (0→3), catalog values at the 1..1000 range edges.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing. Your \`source\` value is "edge".
$SCHEMA
$(file_contract edge)
EOF

# ---------- acceptance ----------
cat > "$P/acceptance.md" <<EOF
$SHARED_HEAD

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in \`detail\` (quote the exact phrase from the spec when possible).

Audit map (walk every item; cite evidence from the worktree, not just the diff):
1. The accumulator contracts (the LENS-GUARDS' hard blocker class — walk EVERY clause: home, in-place update in §1b, derived/never-serialized, integer-only + jint_strict, the accrue formula, the 1000 cost, the >= 1000 pickable threshold, MAX_CREDIT_MILLI type-relative, 500 in balance.json with 1..1000 fail-fast).
2. Credit-gated eligibility (live subset, ONE rng draw per pick, §1a exempt per N9).
3. The E24 invariant (skip ≠ demand event; pool-drop IS; the sla_test.odin pin non-vacuous).
4. W9 (test_w9_surge_lands_under_caps — the ≥0.95×expected land, the per-terminal envelope, the ≥8 hosts crowd, the burst ceiling) and W10 (test_w10_residential_at_cap_zero_drop — the fixture fix REAL: real node ids drawn, !replay_error guarded, delivered > 0, the sourcing res actually sources ~50, avg transit ≤ 500 ms).
5. The re-pins (demand_test EMAIL_CAPPED_800/STREAM_CAPPED_800 exact + bounds; flow_test per-spec counts + max_per_tick ≤ 2; determinism_test test_caps_replay_byte_identical — POSITIVE + NEGATIVE, not golden re-blesses).
6. The surge re-tune trio as a unit (demand.json era-3 4→1/2→1 + growth 120→40 + ×10 preserved) and the claimed reasoning (1/tick lands on ~12 residentials; 10/tick surge on ~15 hosts with 2× headroom).
7. The story card status line updated in the same PR (stories-v2.md hunk in the diff).
8. PR-body claims you can check from the worktree (the accrue numbers 83/1333, the W9 numbers 18001/17100/2401, the W10 numbers 46/51/90/250ms, the re-bless cause chain vs the golden-manifest.txt).
9. Scope guard: source-side caps ONLY — no sink-side admit accumulator (W6), no catalog rebalance beyond the cap fraction + the owned surge re-tune, no 5.10 narrow-access resize, no UI.
Your \`source\` value is "acceptance".
$SCHEMA
$(file_contract acceptance)
EOF

# ---------- security ----------
cat > "$P/security.md" <<EOF
$SHARED_HEAD

--- YOUR LENS ---
OWASP-oriented security review of the diff, scaled to what this codebase is: a single-player deterministic sim with JSON catalogs — the realistic classes here are: unsafe deserialization (the jint_strict catalog load — can a crafted/malformed balance.json slip a value past validation? a decimal, a huge integer, a wrong type?), integer overflow/truncation at trust boundaries (the i64 intermediate in spawn_credit_accrue_milli; u32 narrowing; catalog values near i32 max), fail-fast gaps (a missing/zero/negative cap_fraction_permille silently disabling the invariant the code comments call "the honest-fraction invariant"), and denial-of-determinism (any path where catalog input desynchronizes live vs replay). Also the standard checklist where applicable: input validation at system boundaries, unsafe defaults, data exposure. This is an offline game — do NOT invent web/OWASP findings (no auth, no network, no injection surface exists); an empty array is an honest answer. Your \`source\` value is "security".
$SCHEMA
$(file_contract security)
EOF

# ---------- architecture ----------
cat > "$P/architecture.md" <<EOF
$SHARED_HEAD

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions? (The claimed precedent is lane_caps — a derived, never-serized [dynamic] buffer on Flow_State, rebuilt in lockstep with node slots, grown append-only. Verify spawn_credit_milli ACTUALLY mirrors that pattern: init/destroy/allocation discipline, slot-parallel indexing, arena ownership.)
- Does it introduce unnecessary coupling between modules? (flow.odin §1b now reads catalog balance + node types via the accrue procs — same surface as the existing demand director?)
- Is there a simpler alternative with the same outcome? (The design is user-ruled — do not propose a different design; judge only the implementation's internal economy.)
- Does it respect module boundaries? (core purity ODN-1; the accumulator lives in core/flow.odin; tests in core/*_test.odin; data in data/*.json.)
- Will it create technical debt? (The collect_terminals 3-tuple return; the eligible-set scratch rebuilt per pick — O(slots) per packet per tick; dead slots keeping stale credit; the growth/demand re-tune's interaction with eras 1/2 left dormant.)
- Does complexity match the problem? Any premature abstraction?
Your \`source\` value is "architecture".
$SCHEMA
$(file_contract architecture)
EOF

# ---------- codebase ----------
cat > "$P/codebase.md" <<EOF
$SHARED_HEAD

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (spot-check: weighted_pick, weighted_pick_excluding, scripted_plan_demand, effective_volume, flow_try_spawn, sla_count_demand, sla_live, sla_record_run, qa_fixture, topology_spawn_node, sla_draw, node_slot, spawn_histogram, tick_class_count, jint_strict, EVENT_TAG_PACKET_DROPPED, replay_error, win_latency — the names the diff's tests call must exist with the signatures the diff assumes)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in \`location\`.)
- Are there existing tests this diff likely breaks that it does NOT update? (grep the suite for era-3 volume assumptions "4/tick", "2/tick", GROWTH_INTERVAL_TICKS 120, "5500ms" — any consumer the diff missed; check demos/*.dem comments for stale numbers the diff's own comment-pass skipped)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
- Do the test-catalog mirrors (determinism_test test_catalog) actually mirror data/balance.json + data/demand.json's new values?
Your \`source\` value is "codebase".
$SCHEMA
$(file_contract codebase)
EOF

# ---------- tests ----------
cat > "$P/tests.md" <<EOF
$SHARED_HEAD

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

The behaviour surface to trace: (a) the accrue math + MAX_CREDIT ceiling (test_credit_accrue_and_max); (b) the credit-gated eligible set incl. the LIVE rebuild mid-tick (which test proves consumption mid-tick moves a terminal OUT of the eligible set?); (c) the credit-gated skip ≠ demand event + pool-drop IS (test_sla_credit_gated_skip_not_demand_e24); (d) replay byte-identity under caps (test_caps_replay_byte_identical); (e) W9/W10 quantitative acceptances; (f) the catalog fail-fast rows (5 negative rows); (g) the collateral re-pins (crisis/health/node_health/stats — each re-pin must preserve intent: does the re-pinned assertion still bite, or was it softened into vacuity? e.g. health_test's latency guard wrapped in \`if win_delivered > 0\`); (h) the §1a exemption (N9 — is there a pin that the legacy fixture path stays UNGATED?); (i) era-0 inertness (test_era0_legacy_no_rng_draws).

Blind-spot heuristics to check:
- New state transitions (credit accrual → eligible → consume → ineligible) without boundary tests at exactly 1000
- Happy-path-only coverage where error handling is implied (dst-pick-fails-after-credit-consumed)
- The dead-terminal-slot stale-credit path (demolish a terminal mid-credit — any test?)

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
Your \`source\` value is "tests".
$SCHEMA
$(file_contract tests)
EOF

echo "prompts written:"; ls -la "$P"
