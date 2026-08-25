You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r1/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/diff.patch (1865 lines, unified format, PR #47 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r1 — a checkout at exactly the reviewed sha (6b0949765340f1233e31b498bccfea73b4ca9f5e). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/spec/job-briefing.md — note especially the Mission and the numbered Acceptance criteria (1-6) and the Scope guard.
- Story 5.7 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/spec/stories-v2.md — the section "### Story 5.7 — Runtime telemetry (stats stream + debug overlay)" (~line 580).
- Architecture canon §7.2 Logging / §7.4 Event system / §7.6 Debug / dev tools: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/spec/odin-architecture-v1.md, lines 1146-1200.
- Implementation spec committed in the PR: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r1/_bmad-output/implementation-artifacts/spec-5-7-runtime-telemetry.md (also visible as the first file of the diff).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [LOAD-BEARING] The determinism contract. The stats stream must be DERIVED ONLY from the existing deterministic state/event stream: NO wall-clock timing, NO render sampling, NO new nondeterminism. Any wall-clock/render-sampled value in the emitted stream = a blocker (it breaks the determinism spine story 5.3 just pinned). The one-CSV-serializer-shared-by-harness-and-app is the byte-identity contract — verify it holds (same code path both sides), and replay-identity (live == replay) must hold (the `stats-check` pin).
- [LOAD-BEARING] Golden-safety of the overlay. The overlay must be compile-excluded from every non-PP_DEBUG build (harness never defines it), off by default, and unreachable from the capture path — all 24+ pre-existing goldens + the 5.3 pause goldens must be byte-identical. A leak of overlay output into the golden/capture path = a blocker.
- Faithful shaping, no invented metrics: the Stats_Record shapes EXISTING counters (per-pipe offered/carried/dropped by class + Drop_Reason, utilization; per-class demand/delivered/dropped/loss%/avg latency/SLA; global tick/gen/sim-hash/score/meter from core/flow.odin) — verify no double-counting, no invented metric, and the derived values match the state they claim to summarize (spot-check against the sim).
- Delegated decisions documented, not re-litigated: CSV-over-JSONL (byte-determinism + diffability), per-sim-tick emission, metric definitions — the minion documented the rationale in the PR. Verify the choices honor the determinism contract; do NOT re-open them unless a choice breaks the contract.
- Base = v2 — includes 5.5/5.6/5.3 (pause, 7b56485). Carry-forward only; do NOT re-open settled findings (the pause determinism spine is settled/verified — this diff must not weaken it).
- Scope guard: telemetry export + overlay only — no new capture semantics, no changes to the existing event-stream shape, no QoS gameplay changes (5.8 is a separate held job).

--- YOUR LENS ---
Test coverage analysis via traceability.

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

P0 for this diff: the stats stream byte-identity (live == replay pin), the shared-serializer contract (harness == app output), the golden-safety of the overlay (compile-exclusion + default-off), and the CSV correctness of the record math (loss%, utilization, avg latency, per-class aggregation). Verify the claimed pins exist and actually assert byte-identity (read the test files in the worktree — core/stats_test.odin, harness/).

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

Your `source` value is "tests".

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".