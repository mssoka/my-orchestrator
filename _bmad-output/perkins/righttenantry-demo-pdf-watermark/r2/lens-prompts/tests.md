# Lens brief: Test Coverage — round 2 (source: `tests`)

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd is the reviewed worktree — every verification read happens here.

--- PROJECT CONVENTIONS ---
Read ./AGENTS.md at the repo root for project conventions.

--- DIFF ---
Read the canonical diff from this exact path (unified diff, 740 lines) — review exactly these bytes:
/Users/moses/code/_bmad-output/perkins/righttenantry-demo-pdf-watermark/r2/diff.patch

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/righttenantry-demo-pdf-watermark/r2/job-briefing.md
- PR body (producer survey + decisions): /Users/moses/code/_bmad-output/perkins/righttenantry-demo-pdf-watermark/r2/pr-body.json
- Prior round findings (r1 consolidated — this round is a fix-audit): /Users/moses/code/_bmad-output/perkins/righttenantry-demo-pdf-watermark/r2/prior_findings.json

This is round 2 of a fix-audit loop. The r1 test-gate verdict was FAIL (blocker B2), aggregating B1 (handler watermark flag unasserted at runtime) and W2 (committed demo bytes unpinned). The r1-fix commit claims: (1) new integration test `pdf_real_mode_route_serves_unwatermarked_report_test` pinning the handler's served bytes against both watermark=False and watermark=True renders; (2) new unit test `committed_demo_pdfs_match_fresh_rebake_test` pinning all 8 committed demo PDFs against a fresh watermarked re-bake. Verify these pins actually assert what they claim — and audit the rest of coverage honestly.

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

FILE-OUTPUT CONTRACT (overrides the "return" wording above): write ONLY your JSON array to this exact absolute path — do not derive, guess, or compute a different one:
/Users/moses/code/_bmad-output/perkins/righttenantry-demo-pdf-watermark/r2/tests.json
Then stop. Do not run any further commands.
