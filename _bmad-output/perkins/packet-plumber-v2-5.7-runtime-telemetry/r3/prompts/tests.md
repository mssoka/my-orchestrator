You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository or worktree (you may run read-only builds/tests if cheap, but never edit files; probes requiring mutation must copy to /tmp first).

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r3/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/diff.patch (2342 lines, unified format, PR #47 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff. The fix-audit delta (r2-sha 86ef8f8 -> r3-sha 4749470, 496 lines) is available at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/delta-r2-r3.patch for pinpointing the rework.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r3 — a checkout at exactly the reviewed sha (47494702c1a460ddc281f1381a7489111881d70d). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/spec/job-briefing.md — note especially the Mission and the numbered Acceptance criteria (1-6) and the Scope guard.
- Story 5.7 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/spec/stories-v2.md — the section "### Story 5.7 — Runtime telemetry (stats stream + debug overlay)".
- Architecture canon §7.2 Logging / §7.4 Event system / §7.6 Debug / dev tools: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/spec/odin-architecture-v1.md, lines 1146-1200.
- Implementation spec committed in the PR: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r3/_bmad-output/implementation-artifacts/spec-5-7-runtime-telemetry.md (also visible in the diff).

--- PRIOR ROUND (r2) — fix-audit context ---
r2 verdict: NEEDS CHANGES (22 confirmed findings: 2 blockers R2-B1/B2, 4 warnings R2-W1..W4, 10 notes R2-N1..N10; 7/7 lenses completed). Full r2 findings: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/consolidated.json — read it for exact locations/evidence of each prior finding. The r3 rework push (ONE commit, the delta) claims:
- R2-B1 fixed: discriminating pin in core/stats_test.odin — (a) assert no two rec.drops rows share (pipe,class,reason); (b) the known tick-12 tuple (pipe 1, class 1, reason 0, count 2) asserted verbatim (fixture-probed first: era-3 director demand produces the count-2 aggregation).
- R2-B2 fixed: advisory gate now passes (aggregation shape pinned + non-vacuous bundle loads + harness PP_DEBUG CI line).
- R2-W1 fixed: bundle-replication pin computes MID-FLIGHT at tick 3 (not the drained tick-20): member loads asserted identical AND non-zero (carried=30, util=100).
- R2-W2 fixed: CI PP_DEBUG gate compiles the harness too (odin build harness -define:PP_DEBUG=true) — covers overlay.odin + the overlay-check dispatch.
- R2-W3 fixed: --stats-out "" (unset shell var) is a usage error, exit 2, in BOTH CLIs (flag-seen tracked separately from the value); all four error shapes claimed verified live (dangling/duplicate/empty/flag-shaped -> exit 2; valid -> exit 0).
- R2-W4 fixed: the app loop calls free_all(context.temp_allocator) once per frame; the per-step state_hash no longer grows the temp arena unboundedly at 20 Hz.
- Notes: N1 (PR body 555KB -> 369,452 B), N2 (harness rejects "-"-prefixed path tokens), N3 (app*.bin gitignored), N4 (dead captures deleted), N5 (fmt_tmp shim dropped), N6 (builder comment corrected), N7 (draw_heat_tints guards node_slot ok), N9 (literal CSV row of each kind pinned). Not claimed: R2-N8 (CLI error paths untested — check whether it persists as a carry-forward note), R2-N10/N3-stream-buffering + overlay_check duplication remain documented decisions.
- Claimed verification: 165 core tests (158+7), lint 6/6, 25/25 demos goldens byte-identical, stats-check byte-identical x4 demos, app + harness build in plain AND PP_DEBUG variants, CI YAML valid, .gitignore covers the CI binary.
Audit these claims where your lens reads that code — the delta diff (r2-sha..r3-sha, 496 lines) is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/delta-r2-r3.patch — but review the FULL canonical diff; a claimed fix that does not bite, or that introduces a new problem while closing the old one, is a NEW finding.

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [FIX-AUDIT, round 3 of 3 — FINAL automated round] This is a re-review of the r2-rework push (one commit on top of r2's reviewed sha). r2 found 2 blockers (R2-B1 aggregation-shape pin gap, R2-B2 advisory gate FAIL), 4 warnings (R2-W1 vacuous bundle pin, R2-W2 harness PP_DEBUG CI gap, R2-W3 empty-token silent-off, R2-W4 unbounded temp arena), 10 notes (R2-N1..N10). The r3 push claims ALL of them addressed. Your job: audit the DELTA and verify each claimed fix BITES — a fix that is cosmetic, asserts a tautology, or trades the old gap for a new one is a finding. Do NOT re-litigate what r1/r2 verified green (determinism spine, pause goldens, CSV-over-JSONL decision, metric definitions, D-row aggregation semantics, non-vacuous value pins from r2) — carry-forward only via the prior consolidated.json.
- [LOAD-BEARING, carried] The determinism contract: the stats stream is derived ONLY from existing deterministic state — NO wall-clock, NO render sampling, NO new nondeterminism. The one-CSV-serializer byte-identity contract (harness == app) and replay-identity (live == replay) must hold at this sha. The overlay stays golden-safe (compile-excluded from non-PP_DEBUG builds, off by default, unreachable from capture). Any new nondeterminism or a golden shift = a blocker. R2-W4's free_all(context.temp_allocator) must not affect determinism NOR destroy data that must outlive the frame (the whole-session stream buffer!) — temp arena is scratch, not state; verify the stream buffer lives OUTSIDE the temp arena.
- [ROUND 3/3 precision] After this round the human takes over. Be precise about what is a genuine blocker vs. advisory: a blocker must be a defect a reasonable maintainer would block merge on (broken contract, wrong behavior, coverage gap on the P0 critical path), not a stylistic or theoretical concern. Warnings/notes are for everything else.
- Delegated decisions documented, not re-litigated: CSV-over-JSONL, per-sim-tick emission, D-row aggregation per (pipe,class,reason) via map-free find-or-append, write-at-exit stream buffering (whole-session stream held in memory — documented decision r1-N3/r2-N10), overlay_check stepping/composition duplication (documented r1-N8/r2-N10). Do NOT re-open these unless the r3 code breaks their contract.
- Base = v2 — 5.3 pause + 5.5/5.6 + the 5.7 line; carry-forward only; do NOT re-open settled findings.
- Scope guard: telemetry export + overlay only. The sibling 5.3-pause-ux job (PR #49, presentation-only overlay change in app/main.odin) may merge mid-round — its file set is carry-forward, not this PR's concern; do not flag its presentation-path changes as this PR's regressions unless the 5.7 telemetry/overlay contracts break.

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

P0 for this diff: the stats stream byte-identity (live == replay pin), the shared-serializer/emission-proc contract (harness == app output), the golden-safety of the overlay (compile-exclusion + default-off), and the CSV correctness of the record math. CRITICAL r3 fix-audit checks — read the assertions in core/stats_test.odin against the derivation in core/stats.odin and counters in core/flow.odin:
(R2-B1) Does the test now (a) assert no two rec.drops rows share (pipe,class,reason) — i.e. a uniqueness walk over the rows — AND (b) pin the tick-12 tuple (pipe 1, class 1, reason 0, count 2) verbatim? Both halves must bite: (a) without (b) tolerates a wrong count; (b) without (a) tolerates duplicate shapes elsewhere. Sanity-check the fixture actually produces that tuple (read the fixture setup; r2's probe confirmed 'D pipe=1 class=1 reason=0 count=2' at tick 12 of the congested fixture).
(R2-W1) Is the bundle-replication record now computed at a MID-FLIGHT tick (tick 3 per the claim) with member loads asserted identical AND non-zero (carried==30, util==100)? A pin that compares records computed post-drain (tick 20) or that omits the non-zero assertion is still vacuous.
(R2-N9) Are literal CSV rows of each kind (header, S, P, C, D, G) pinned string-for-string?
(R2-N8 carry-forward) Are the --stats-out CLI error paths (exit 2 dangling/duplicate/empty/flag-shaped; exit 1 unwritable) covered by TESTS, or only verified live? Classify the residual gap honestly.
(R2-W4) Is there any test or probe covering the app's per-frame free_all not corrupting the stream (or is it verified only by reasoning)?

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".