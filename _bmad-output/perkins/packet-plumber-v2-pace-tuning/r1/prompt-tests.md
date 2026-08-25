You are a code-review lens running HEADLESS. You have read-only access to the repository at the reviewed state (a detached checkout at exactly the reviewed commit) and may verify the diff claims against the actual codebase using your tools (read files, grep). Work autonomously; do not ask questions.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-pace-tuning-r1/project-context.md (the repo conventions doc). The project is an Odin-language game (Packet Plumber v2): deterministic fixed-timestep sim core + raylib app; catalogs (balance.json, packet_types.json) are the single source of tunables; goldens + replay gates enforce determinism; ODN rules (integer-only sim, no wall-clock in sim, etc.) as documented there.

--- DIFF (the canonical bytes you review) ---
The unified diff is saved at: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pace-tuning/r1/code-chunk.patch (2,265 lines — the CODE chunk of a chunked review: core/, app/, data/, repo root; the goldens/ corpus chunk is excluded and verified mechanically by the CI replay gate instead). Read that file. Review exactly these bytes.

--- SPEC / CONTEXT ---
The spec is the original job briefing: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-pace-tuning.md
Round context + user rulings (what NOT to re-litigate) : /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pace-tuning/r1/context-guards.md
Read both.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified catalog loader fields without matching fail-fast coverage (terminal_spawn_interval_ticks / terminal_min_sep_tiles: missing-key, non-integer, zero, negative)
- Behavior changes where the test pin was WEAKENED or an assertion REMOVED rather than re-derived (compare old vs new test bodies in the diff — e.g. assertions dropped, == relaxed to <=, ==0 relaxed to ratio checks; judge whether each weakening is honestly justified by the documented pace shift or hides a regression)
- Happy-path-only coverage where error handling is implied
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80–89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

Context: the local CI suite (10 gates incl. the golden replay gate) is claimed 10/10 green and is being re-run mechanically by the orchestrator — treat that as bulk evidence, focus your traceability on the diff itself.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. pacing, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use N/A ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array to this exact file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pace-tuning/r1/tests.json (create/overwrite it). Do not derive or guess the path; it is given verbatim here.
- The file must contain ONLY the JSON array (no prose, no markdown fencing, no preamble).
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, stop. Your final message: one line stating the file was written and how many findings.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
- User rulings in the round context (4x pace magnitude, golden re-bless deliberate, fun-test gate user-held) are settled: findings contradicting them are invalid.
