# Lens brief — TEST COVERAGE (source: `tests`) — Perkins round 4, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4/project-context.md first — the project's rules for agents.

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4 is checked out at exactly the reviewed state — verify against it.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md (the job briefing — this IS the spec).

--- ROUND CONTEXT (r4) ---
Round 4 after B1/B2 fixes and two rebases. The r1 test gate FAILED on: the vacuous pending-commands pin (B2 — now reworked: a legal ROUTER PLACE pending command with anti-vacuity + negative legs — audit whether the rework is genuinely non-vacuous: does the anti-vacuity assert (no-pending prediction != with-pending) actually pin that the shadow consumed the slice? can it pass vacuously?), reduced-motion paths untested, and the highlight radius unpinned (B1 — is the 8-tile bound NOW pinned by any test? check whether test coverage for the radius exists; if not, that's a continuing gap).

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

Specific traceability wanted this round:
- B1's tile-unit radius fix → is there ANY pin (unit test or golden-level assert) that would catch a reintroduced unit mix?
- B2's reworked pending test → materialization assert, anti-vacuity assert, negative leg — all genuinely exercising what they claim?
- The #83 merge (sprite_blit spec+tint) → any test/pin covering the tint path or the shadow ink-ratio fade?
- The catalog diameter-guard boundary rows (48 accept, 49/50/51 reject) + the decimal jint_strict row → complete?
- The reveal-buffer >4 trim (r1 gap — still untested?).
- Reduced-motion branches of ring/reveal/highlight (r1 gap — still untested?).
- App-side glue (feed call site ordering vs audio_mark advance, predict dedup + topology-gen re-predict) — covered anywhere?

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
  "category": "<short tag, e.g. coverage-gap, vacuous-test>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/tests.json
An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
