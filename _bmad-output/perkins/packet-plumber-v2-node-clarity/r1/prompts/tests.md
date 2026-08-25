You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read `/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-node-clarity-r1/project-context.md` — that file's content IS the PROJECT CONVENTIONS block below.

--- DIFF ---
The diff under review is the exact bytes of `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r1/diff.patch` — read that file; its content IS the DIFF block. (1240 lines, unified format. The long `goldens/**` section is binary PNG re-blesses — expected and documented in the spec/PR body; judge the text hunks on their merits.)

--- SPEC / CONTEXT ---
Read these two files; together their content IS the SPEC / CONTEXT block:
1. `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-node-clarity.md` — the job briefing (THE spec: task, hard rules, acceptance).
2. `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r1/pr-body.md` — the PR body (the implementer's claims and the documented deviations D1–D7).

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

Context for this repo's test architecture: unit tests are Odin `@(test)` procs (e.g. `app/render/palette_polish_test.odin`), the golden-image harness (`harness/`, including `harness/palcheck.odin` pixel-pin checks) is the visual regression layer, and `tools/blur_gate.py` is a measurement gate. The palcheck pin counts (46 checks claimed) and the golden re-bless (45 demos) are part of the coverage story — trace the new draw-layer behaviours (family wash, type chip, tier ring, health-threading reorder in draw_nodes) to their pin/test coverage and classify gaps honestly.

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
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Write your JSON array to the file `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r1/tests.json` — that file must contain ONLY the JSON array (no prose, no markdown fencing, no preamble). Then reply with one short line confirming the write, and stop.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
