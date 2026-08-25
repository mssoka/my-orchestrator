You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository (you may run read-only builds/tests if cheap, but never edit files).

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r2/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/diff.patch (2220 lines, unified format, PR #47 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r2 — a checkout at exactly the reviewed sha (86ef8f8b479f1f10a82ab04951d4097959057797). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/spec/job-briefing.md — note especially the Mission and the numbered Acceptance criteria (1-6) and the Scope guard.
- Story 5.7 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/spec/stories-v2.md — the section "### Story 5.7 — Runtime telemetry (stats stream + debug overlay)".
- Architecture canon §7.2 Logging / §7.4 Event system / §7.6 Debug / dev tools: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/spec/odin-architecture-v1.md, lines 1146-1200.
- Implementation spec committed in the PR: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r2/_bmad-output/implementation-artifacts/spec-5-7-runtime-telemetry.md (also visible in the diff).

--- PRIOR ROUND (r1) — fix-audit context ---
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
Audit these claims where your lens reads that code. A claimed fix that is cosmetic, incomplete, or regressive is a finding. r1's full consolidated findings: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/consolidated.json

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [FIX-AUDIT, round 2 of 3] This is a re-review after the r1 NEEDS-CHANGES rework. r1 found 2 blockers (B1 P0 record-math pins, B2 advisory gate FAIL), 10 warnings (W1-W10), 11 notes (N1-N11); the r2 push claims ALL blockers and warnings fixed plus notes N1/N2/N4/N5/N6/N7/N9. Your job: audit the DELTA (the r1-fix commits) and find NEW regressions the rework introduced. Do NOT re-litigate what r1 verified green (the determinism spine, the pause goldens, the CSV-over-JSONL decision, metric definitions) — carry-forward only. But DO verify claimed fixes are real where your lens naturally reads that code: a fix that does not actually change behavior, or that introduces a new problem while closing the old one, is a NEW finding.
- [LOAD-BEARING] The determinism contract. The stats stream must be DERIVED ONLY from the existing deterministic state/event stream: NO wall-clock timing, NO render sampling, NO new nondeterminism. The one-CSV-serializer byte-identity contract (harness == app) and replay-identity (live == replay) must STILL hold at this sha. The overlay stays golden-safe: compile-excluded from non-PP_DEBUG builds, off by default, unreachable from capture. Any new nondeterminism, serializer divergence, or golden shift = a blocker.
- Faithful shaping, no invented metrics: the Stats_Record shapes EXISTING counters from core/flow.odin — verify no double-counting, no invented metric, derived values match the state they summarize.
- Delegated decisions documented, not re-litigated: CSV-over-JSONL, per-sim-tick emission, D-row aggregation per (pipe,class,reason) via map-free find-or-append (deterministic — do not flag the absence of a map as a defect), write-at-exit stream buffering — these are documented decisions; do NOT re-open them unless the r2 code breaks the contract.
- Base = v2 — 5.3 pause + 5.5/5.6 + 5.7-r1 state; carry-forward only. The sibling 5.3-pause-ux job (presentation-only overlay change in app/main.odin) may merge mid-round — its file set is carry-forward, not this PR's concern.
- Scope guard: telemetry export + overlay only — no new capture semantics, no event-stream shape changes.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is an offline desktop game (Odin + raylib) — calibrate to the real boundary surface present in the diff: the `--stats-out <path>` CLI flag (path handling, file overwrite, error handling on unwritable paths, exit codes), file I/O in harness/app (r1 N2 flagged predictable /tmp paths; r2 claims streams moved under gitignored bin/ — verify no predictable-path or collision issue remains), the debug overlay's compile gate (accidental shipping of debug tooling to players in non-PP_DEBUG builds), and any injection into the sim state from the new code paths. Do not invent web-tier concerns that have no surface here. Your `source` value is "security".

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

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/security.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens security complete — N findings written".