#!/usr/bin/env python3
"""Generate the 7 Perkins lens prompt files (r2 FIX-AUDIT, packet-plumber v2-5.7-runtime-telemetry)."""
import os

R = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2"
P = os.path.join(R, "prompts")
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r2"
DIFF = os.path.join(R, "diff.patch")
SPEC = os.path.join(R, "spec")

GUARDS = """- [FIX-AUDIT, round 2 of 3] This is a re-review after the r1 NEEDS-CHANGES rework. r1 found 2 blockers (B1 P0 record-math pins, B2 advisory gate FAIL), 10 warnings (W1-W10), 11 notes (N1-N11); the r2 push claims ALL blockers and warnings fixed plus notes N1/N2/N4/N5/N6/N7/N9. Your job: audit the DELTA (the r1-fix commits) and find NEW regressions the rework introduced. Do NOT re-litigate what r1 verified green (the determinism spine, the pause goldens, the CSV-over-JSONL decision, metric definitions) — carry-forward only. But DO verify claimed fixes are real where your lens naturally reads that code: a fix that does not actually change behavior, or that introduces a new problem while closing the old one, is a NEW finding.
- [LOAD-BEARING] The determinism contract. The stats stream must be DERIVED ONLY from the existing deterministic state/event stream: NO wall-clock timing, NO render sampling, NO new nondeterminism. The one-CSV-serializer byte-identity contract (harness == app) and replay-identity (live == replay) must STILL hold at this sha. The overlay stays golden-safe: compile-excluded from non-PP_DEBUG builds, off by default, unreachable from capture. Any new nondeterminism, serializer divergence, or golden shift = a blocker.
- Faithful shaping, no invented metrics: the Stats_Record shapes EXISTING counters from core/flow.odin — verify no double-counting, no invented metric, derived values match the state they summarize.
- Delegated decisions documented, not re-litigated: CSV-over-JSONL, per-sim-tick emission, D-row aggregation per (pipe,class,reason) via map-free find-or-append (deterministic — do not flag the absence of a map as a defect), write-at-exit stream buffering — these are documented decisions; do NOT re-open them unless the r2 code breaks the contract.
- Base = v2 — 5.3 pause + 5.5/5.6 + 5.7-r1 state; carry-forward only. The sibling 5.3-pause-ux job (presentation-only overlay change in app/main.odin) may merge mid-round — its file set is carry-forward, not this PR's concern.
- Scope guard: telemetry export + overlay only — no new capture semantics, no event-stream shape changes."""

SCHEMA = """{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}"""

ACCURACY = """Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong."""

PRIOR = """--- PRIOR ROUND (r1) — fix-audit context ---
r1 verdict: NEEDS CHANGES (36 confirmed findings: 2 blockers, 10 warnings, 11 notes). The r2 push claims:
- B1 fixed: test_stats_derivation_congested now value-pins the class rows (loss_pct == dropped*100/(delivered+dropped), avg_latency_ms == total_latency_ms/delivered, the flow.sla accumulator mapping, the sla_breach latch copies).
- B2 fixed (gate raised): D-row accounting (offered == carried + drops*bandwidth), 2-member parallel-pipe bundle replication, shared stats_emit path, CI wiring (-define:PP_DEBUG=true build + stats-check steps).
- W1/W2 fixed: app rejects a dangling --stats-out (exit 2, mirroring the harness); unwritable path exits 1 per the spec I/O matrix.
- W3 fixed: PR-body excerpt is now the VERBATIM tick-21 stream (no fabricated D row).
- W4 fixed: seed-column claim corrected (sim_hash folds the seed).
- W5 fixed: AC5 checkbox ticked. W6 fixed: D rows aggregate per (pipe,class,reason) via map-free find-or-append.
- W7/W8 fixed: D-row accounting + 2-member bundle replication pinned in stats_test.
- W9 fixed: stats_emit is the ONE emission proc; harness drivers AND the app loop call it.
- W10 fixed: CI builds with PP_DEBUG + runs stats-check (pause, qos_contention).
- Notes picked up: N1 (CI stats-check), N2 (streams under gitignored bin/), N4 (overlay-check fails loud on zero stepped ticks), N5 (demo_destroy extracted), N6 (usage string), N7 (overlay_on comment), N9 (header comment).
- Claimed verification: 164 core tests (158+6), lint 6/6, 25/25 demos goldens byte-identical, stats-check byte-identical on pause/qos_contention/surge/health_lose, both app builds, CI YAML valid.
Audit these claims where your lens reads that code. A claimed fix that is cosmetic, incomplete, or regressive is a finding. r1's full consolidated findings: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/consolidated.json"""

def shared_header():
    return f"""You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository (you may run read-only builds/tests if cheap, but never edit files).

--- PROJECT CONVENTIONS ---
Read {WT}/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: {DIFF} (2220 lines, unified format, PR #47 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff.

--- WORKTREE (your verification source) ---
{WT} — a checkout at exactly the reviewed sha (86ef8f8b479f1f10a82ab04951d4097959057797). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): {SPEC}/job-briefing.md — note especially the Mission and the numbered Acceptance criteria (1-6) and the Scope guard.
- Story 5.7 card: {SPEC}/stories-v2.md — the section "### Story 5.7 — Runtime telemetry (stats stream + debug overlay)".
- Architecture canon §7.2 Logging / §7.4 Event system / §7.6 Debug / dev tools: {SPEC}/odin-architecture-v1.md, lines 1146-1200.
- Implementation spec committed in the PR: {WT}/_bmad-output/implementation-artifacts/spec-5-7-runtime-telemetry.md (also visible in the diff).

{PRIOR}

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
{GUARDS}
"""

def output_block(lens):
    return f"""--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{SCHEMA}

{ACCURACY}

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
{R}/{lens}.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens {lens} complete — N findings written"."""

LENSES = {
    "edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Context for this codebase: the relevant boundary classes include — integer division/rounding on the integer-only sim paths (loss%, utilization%, avg latency; integer division by zero when delivered==0 or demand==0), zero-capacity or zero-demand pipes/bundles in stats math, the D-row find-or-append aggregation loop (first row, repeated reasons, a reason mix within one tick), CSV escaping of string fields that can contain commas/quotes, --stats-out error paths (dangling token, duplicate flag, unwritable path, exit codes), first-tick vs later-tick accumulation windows, per-class rows for classes with zero demand, and the PP_DEBUG=false compile-exclusion paths. Your `source` value is "edge".""",

    "acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

The six Acceptance criteria from the job briefing, for direct audit:
1. `harness run <demo> --stats-out <path>` writes the stream; two runs of the same demo produce byte-identical files (pinned by test).
2. The app writes the same stream with the same flag; replay-identical.
3. `D` toggles the overlay live; every element renders with real numbers (per-pipe readout on select, per-class table, congestion heat, global line, live event tail).
4. Overlay never shifts goldens (default off; captures unchanged).
5. Full local suite green (core tests, lint, harness suite, both app builds — you may run read-only builds/tests from the worktree if cheap, or verify statically).
6. PR body carries the story card 5.7 + a sample stream excerpt from a congested run — r2 claims the excerpt is now the VERBATIM tick-21 stream (r1 W3: it was fabricated). Verify: the PR body's excerpt must match the real artifact byte-for-byte. The committed _pr_body.md is in the diff; the real stream you can produce by running the harness from the worktree read-only (tools/harness.sh run qos_contention --stats-out /tmp/pp-r2-audit.csv, or read the harness) — or verify internal consistency (prose vs rows).
Also audit the fix claims against the spec's I/O matrix (dangling --stats-out -> usage error; unwritable path -> eprintln + exit 1) and the overlay content list against arch §7.6. Your `source` value is "acceptance".""",

    "security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is an offline desktop game (Odin + raylib) — calibrate to the real boundary surface present in the diff: the `--stats-out <path>` CLI flag (path handling, file overwrite, error handling on unwritable paths, exit codes), file I/O in harness/app (r1 N2 flagged predictable /tmp paths; r2 claims streams moved under gitignored bin/ — verify no predictable-path or collision issue remains), the debug overlay's compile gate (accidental shipping of debug tooling to players in non-PP_DEBUG builds), and any injection into the sim state from the new code paths. Do not invent web-tier concerns that have no surface here. Your `source` value is "security".""",

    "architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Architecture-specific questions for this diff: does core/stats.odin keep the core pure (no vendor:*, no os/time imports, no I/O — serialization-to-bytes ok, file writing NOT ok in core)? Is the ONE-CSV-serializer + ONE-emission-proc structure real after the r2 refactor (r1 W9: the app loop duplicated the harness loop; r2 claims a shared stats_emit proc both drivers call — verify the call graph: every emission site goes through it, and no duplicated event-mark/hash logic remains)? Is the D-row find-or-append aggregation deterministic (no map iteration) and does it preserve row order stability (same input -> same output bytes)? Is the overlay compile-gated per arch §7.6 rather than runtime-gated? Does the stats record derivation respect the layering (derived from Run_State/flow state, not from the renderer)? Your `source` value is "architecture".""",

    "codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Codebase-specific checks: do the counters/stats fields referenced in core/stats.odin exist in core/flow.odin / core/types.odin with matching names and semantics? Does the harness share the serializer AND the emission proc with the app (find the call graph — harness/run.odin, harness/stats.odin, app/main.odin)? Is demo_destroy (r2 N5) actually extracted and used at all teardown sites (run_demo, load_demo_replay, overlay_check)? Are the demos referenced by the new tests present in the demos/ dir? Does the overlay render code live consistently with the existing render modules? Is the PR-body excerpt (W3 fix) consistent with the actual serializer output format (row legend vs emitted columns)? Your `source` value is "codebase".""",

    "tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

P0 for this diff: the stats stream byte-identity (live == replay pin), the shared-serializer/emission-proc contract (harness == app output), the golden-safety of the overlay (compile-exclusion + default-off), and the CSV correctness of the record math (loss%, utilization, avg latency, per-class aggregation, D-row aggregation). Verify the claimed pins exist and actually assert the values (read the test files in the worktree — core/stats_test.odin, harness/). CRITICAL fix-audit checks (r1 B1/W7/W8): do the new class-row assertions pin loss_pct == dropped*100/(delivered+dropped), avg_latency_ms == total_latency_ms/delivered, the flow.sla accumulator mapping, the sla_breach latches, the D-row accounting equality (offered == carried + drops*bw), and the 2-member bundle replication? A pin that asserts the WRONG formula (e.g. mirrors a buggy implementation, or asserts tautologies like x == x) is worse than no pin — read the assertions against the derivation code in core/stats.odin and against core/flow.odin's counters.

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

Your `source` value is "tests".""",
}

BLIND = f"""You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
Read the diff IN FULL from exactly this path: {DIFF} (2220 lines, unified format). This file is ALL the context you have. You have NO codebase access for this review — do not open, read, grep, or list any other file or directory. Reading anything beyond the diff file invalidates your lens: your entire value is fresh eyes with zero framing. (The only other file you may touch is your output file named below.)

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{SCHEMA.replace('<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>', '"blind"')}

{ACCURACY}

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
{R}/blind.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens blind complete — N findings written"."""

def main():
    os.makedirs(P, exist_ok=True)
    for lens, brief in LENSES.items():
        path = os.path.join(P, f"{lens}.md")
        with open(path, "w") as f:
            f.write(shared_header() + "\n--- YOUR LENS ---\n" + brief + "\n\n" + output_block(lens))
        print("wrote", path)
    with open(os.path.join(P, "blind.md"), "w") as f:
        f.write(BLIND)
    print("wrote", os.path.join(P, "blind.md"))

if __name__ == "__main__":
    main()
