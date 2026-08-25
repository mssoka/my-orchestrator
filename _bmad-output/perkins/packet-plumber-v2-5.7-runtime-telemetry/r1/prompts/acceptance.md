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
Audit the diff against the spec and context docs above. Identify:
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
6. PR body carries the story card 5.7 + a sample stream excerpt from a congested run (verify via `gh pr view 47 --json body` if needed, or trust the committed _pr_body.md in the diff).
Also audit the overlay content list against arch §7.6 and the briefing's Part B list, and the canon §7.2 constraints (core never touches stdout; sink-injected logging). Your `source` value is "acceptance".

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/acceptance.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens acceptance complete — N findings written".