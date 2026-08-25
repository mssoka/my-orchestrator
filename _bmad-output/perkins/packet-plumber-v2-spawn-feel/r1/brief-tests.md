# Lens brief — TEST COVERAGE (source: `tests`) — Perkins round 1, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1/project-context.md first — the project's rules for agents. Testing model: `odin test` for the pure core + app/render unit tests (`@(test)` procs); the golden-image harness (`harness/`, `tools/harness.sh`) for scripted demo scenarios — T1 per-tick state-hash manifests + T2 pixel goldens + a replay gate; `tools/ci-local.sh` gates for CI parity.

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1 is checked out at exactly the reviewed state — verify against it.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md (the job briefing — this IS the spec). Its acceptance includes: "Local suite green" and "Spawn capture sequence (pre→pop) shows: telegraph ring → reveal scale/fade → pipe highlight".

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

Specifically trace (verify against the actual test files, don't trust the diff's claims):
- The 7 claimed new spawn-fx pins in app/render/spawn_fx_test.odin — do they exist, do they pin the load-bearing behaviors (clone round-trip hash, predict==actual, pending-commands, negatives, feed walk-back, reveal math, dedup)?
- The reveal-bounds cap (`len(fx.reveals) > 4` trim) — tested?
- The reduced-motion paths (static ring, instant reveal, steady highlight) — tested? The draw procs themselves (`spawn_fx_draw_telegraph`/`draw_ring_annulus`/`spawn_fx_draw_highlight`) are pixel-tested via goldens only — is spawn_feel.dem's capture set sufficient to exercise the ring geometry, the reveal transform, AND the pipe highlight (which window/tick does each capture land on)?
- The catalog folds: decimal 10.5 rejection row, boundary 48 accept row, 49/50/51 reject rows — present in core/catalog_test.odin? Was the previously-missing boundary assertion actually added?
- The bad-free fix (growth_test strict_spawn_class) — is there anything asserting the bad-free count (or is it unverifiable by test — a note if so)?
- harness/run.odin wiring (feed before clear, predict per capture, reset per demo) — covered by the 47-demo harness run? Which gate would catch a regression in the feed slice ordering?
- The claimed "236/236 core, 22/22 render, 47/47 demos, 10/10 gates" — these are claims; the coverage lens judges the GAP between behavior and test, not whether the suite passes.

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
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/tests.json
An empty array `[]` is NOT expected from this lens (the advisory gate is mandatory). Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
