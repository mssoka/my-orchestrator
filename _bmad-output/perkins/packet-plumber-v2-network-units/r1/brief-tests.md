# Lens task — TEST COVERAGE (source: tests)

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the repository worktree at exactly the reviewed state — verify against it, not against any other checkout.

--- PROJECT CONVENTIONS ---
Read project-context.md in the worktree root (the project's conventions file) and apply it (notably: `odin test` for the pure core; the golden-image harness in harness/ + tools/harness.sh for scripted scenarios; everything testable headless, is).

--- DIFF ---
The canonical diff (review EXACTLY these bytes — read it first, in full):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-network-units/r1/diff.patch
(unified diff, 984 lines)

--- SPEC / CONTEXT ---
The binding spec (the original job briefing — read it):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-network-units.md

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

Specific behaviours to trace in this diff: the tx-ring record/window procs in core/bundles.odin (tick-keyed slots, stale-slot reset, rebuild zeroing, defensive bounds) — is there ANY direct test of bundle_tx_record/bundle_tx_window semantics (window expiry, slot reuse at W-boundary, rebuild reset)? The honest util_pct in stats.odin (windowed) — what pins it beyond the two re-pinned stats tests? units.odin formatters/formulas — covered by the new units_test? The display changes (noc_overlay, tray, node_health) — what covers them (noc row-count pins, golden harness)?

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
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap, coverage-gate>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing (except the advisory gate finding, which is always emitted).
- Do not invent findings to fill a quota.

FILE-OUTPUT CONTRACT (headless override — authoritative): do NOT print the JSON as your reply. Write ONLY the JSON array (no prose, no fencing) to EXACTLY this absolute path with your write tool, then stop:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-network-units/r1/tests.json

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
