You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.8-qos-panel-r1/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/lens-diff.patch (2599 lines, unified format, PR #50 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff. The PR also re-blessed goldens; their summarized surface is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/golden-manifest.txt (the full binary diff is Perkins-verified mechanically — do not re-derive it).

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.8-qos-panel-r1 — a checkout at exactly the reviewed sha (ea1026d7fd67667bca6e576baada50f7ecba1d46). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/spec/job-briefing.md — note especially the Mission (the user-ruled design points 1-6), the numbered Acceptance criteria (1-7) and the Scope guard.
- Story 5.8 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/spec/stories-v2.md — the section "### Story 5.8 — QoS panel + assignment-driven auto-reservation" (~line 604).
- Architecture canon: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/spec/odin-architecture-v1.md — ODN-3 QoS decision + player surface (~line 474), §6.3 S3 QoS lane model (~line 1008), the E-contract glossary table (~line 1620-1640: E5 all-zero-weights default, E6 never-drop, E7 WRR floor, E8 largest-remainder, E9 drop ladder, E10 replay determinism).
- Implementation spec committed in the PR: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.8-qos-panel-r1/_bmad-output/implementation-artifacts/spec-5-8-qos-panel.md (also visible in the diff).
--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [LOAD-BEARING] Serialization + replay equality [E10]: the Cmd_Set_Emphasis payload evolution (preset u16 → weights [3]i32, SAME serialized tag, LOG_VERSION 3→4) must hold replay equality BY CONSTRUCTION — the auto-ladder and the manual editor both write through the ONE command; a v3 log must be rejected by the v4 reader. Any divergence between live and replay = a blocker.
- [LOAD-BEARING] The golden fold is Perkins-verified mechanical (byte-level): pre-existing .log.bin differ only at the version byte + catalog_hash; qos_emphasis.log.bin record bytes are exactly the documented payload evolution with preset→weights equivalence; all pre-existing PNGs byte-identical. Do not re-derive; flag only code paths that could hide semantic drift in a FUTURE re-bless.
- Ladder semantics exact: in-play lanes = assigned lanes ∪ Standard (Standard always reserved, canon-safe); streaming→Express alone = 70/30; + email→Best-effort = exactly 50/30/20; untouched pipes keep the default preset (no-QoS goldens byte-stable). A wrong split or a Standard-lane regression = a blocker.
- Never-drop safety: E6 — future non-Standard defaults can't break the auto path (never-drop by construction); no cycle deadlock on zeroed lanes. Verify both.
- Manual editor: presets + ±5 nudges, derived AUTO/MANUAL mode, revert-to-auto; the silent manual-tune clobber on lane assignment is gated on the pre-edit derived mode.
- Base = v2 — includes 5.3 pause + 5.3-pause-ux + 5.7 telemetry (5.7 touched app/main.odin emission/overlay paths). Carry-forward only; do NOT re-open settled findings.
- Scope guard: QoS panel + auto-reservation + the payload evolution ONLY — no new command kinds, no unrelated gameplay changes, nothing 5.7-telemetry or 5.3-pause owns.
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

Behaviour changes to trace (the PR's claimed coverage: 167 core tests, lint, 27 harness demos green): (1) qos_auto_weights pure proc — ladder row selection by in-play lane count, assigned ∪ Standard semantics, [100]/[70,30]/[50,30,20] splits, untouched-pipe default preset (look in core/qos_test.odin); (2) Cmd_Set_Emphasis payload evolution — bus validation of raw weights (negative/zero/huge, never-drop lane zeroing E6), v3-log rejection by the v4 reader, round-trip write→parse (core/qos_test.odin, core/determinism_test.odin, catalog/hash tests); (3) ladder + presets fail-fast validation in core/catalog.odin (malformed rows, wrong lengths, non-descending) — core/catalog_test.odin; (4) E6 never-drop by construction on the AUTO path (future non-Standard defaults) — is there a test; (5) zeroed-lane cycle deadlock guard — is there a test; (6) the derived AUTO/MANUAL clobber gate (assignment after manual tune must NOT silently clobber when pre-edit mode was MANUAL) — where is that tested; (7) UI/panel behavior — what's the project's UI test story (the golden-image harness IS the UI test: qos_auto + qos_manual demos with T2 captures — is a clobber-gate/revert-to-auto scenario captured anywhere); (8) ±5 nudge bounds and preset quick-set math. The suite commands are `odin test core`, `tools/lint.sh`, `tools/harness.sh run` — you may READ test files and run `odin test core` if useful, but NEVER run `tools/harness.sh save` (it would re-bless goldens — that is a forbidden mutation for you).

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".
