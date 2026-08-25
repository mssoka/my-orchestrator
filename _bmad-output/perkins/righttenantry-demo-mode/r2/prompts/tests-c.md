You are reviewing a code diff as one lens of an automated multi-lens code review (Perkins round 2, job: righttenantry-demo-mode, PR #629, reviewed sha 1c2a6a9 - the rework head addressing round-1 blockers).

You have read-only access to the repository and may verify the diff's claims against the actual codebase using your tools (read files, grep). All verification reads happen in the worktree - a checkout at exactly the reviewed state:
  WORKTREE: /Users/moses/.herdr/worktrees/RightTenantry/perkins-demo-mode-r2

The diff you review is EXACTLY these bytes (a file-group chunk of the full PR diff - never re-fetch or regenerate the diff):
  DIFF CHUNK: /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r2/chunk-c.patch

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-demo-mode-r2/AGENTS.md first.

--- SPEC / CONTEXT ---
Read ALL of these before reviewing:
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r2/spec/righttenantry-demo-mode.md   (original job briefing - the spec)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r2/spec/issue-628.json               (GitHub issue #628 - research + design)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r2/spec/pr-629-body.md               (PR body - carries the lavish verdict, which is CANON: do not re-judge the approved design, only the shipped fidelity to it)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r2/spec/perkins-briefing-r2.md       (round guards - the acceptance pillars and the r2 fix-audit bar)
- /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r2/spec/r1-consolidated.json         (round-1 findings - prior findings for the fix audit)

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

THIS IS ROUND 2 - a fix-audit. r1's coverage-gate finding (spec/r1-consolidated.json id 36: download path + boot path untested, no /demo E2E scenario) must be re-audited against the FRESH tree - the rework claims report_download_test pins the download. Check the new tests actually bite: a test that passes vacuously (asserts nothing, mocks the thing under test away) is a finding. The structural lint (scripts/lint_demo_network.py + the workflow wiring) must be verified REAL: read its logic and confirm a demo-branch-to-real-api-call would actually FAIL it.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this absolute path (create nothing else, write nowhere else):
  /Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r2/lenses/tests-c.json
Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP.

ACCURACY MANDATE - this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY - they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination - drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume - an empty array is a fine and honest answer when nothing is wrong.