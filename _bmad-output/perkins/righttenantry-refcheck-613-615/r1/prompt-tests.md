You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Work in /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-613-615-r1 (a checkout at exactly the reviewed state).

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-613-615-r1/AGENTS.md (repo project instructions: brand voice, no-em-dash ruling, code style, invariants — note its rule: tests defend named regressions; coverage percentages / tier ladders / "every function needs a test" rules are NOT useful here).

--- DIFF ---
The exact diff under review is saved at /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/diff.patch (unified diff, 763 lines). Read it FIRST. Every reviewer reviews these identical bytes; never regenerate or re-derive the diff.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/issue-613.json — GitHub issue #613 (stepper label ambiguity)
- /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/issue-615.json — GitHub issue #615 (toasts hidden behind consent banner)
- /Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-613-615.md — original job briefing
- The worktree also contains the implementing spec: _bmad-output/implementation-artifacts/spec-613-615-bug-hunt-ux-fallout.md

--- REVIEW GUARDS (from the Perkins briefing; treat as binding spec) ---
- #613 scope is LABEL AND USER-FACING COPY ONLY: DB enum stays `viewed`; refcheck trigger logic untouched; `vacancy.viewed_at` untouched.
- ONE user-facing term everywhere: "Viewing held"; copy tests pin the new wording.
- #615: consent banner must remain visible AND clickable; `consent.js` untouched. Toast visibility during the consent window must be proven by the evidence artifact (DOM geometry + screenshots + clickability, desktop/mobile/degenerate).
- The degenerate-corner trade-off (320x480 + expanded customize panel) is a documented, user-flagged decision — do NOT re-litigate.
- No em dashes in any user-facing copy.
- Scope: the two fixes only.

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

Context for classification: this is a UX copy + CSS-positioning change (client-only). The repo's own convention (AGENTS.md) says tests defend NAMED regressions, not coverage quotas — weigh gaps accordingly: a missing test matters when a named regression could silently recur (e.g. label reverting to "Viewed", toast position regressing under the banner), not for its own sake.

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (do not derive or guess any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/tests.json

Each element must match this schema exactly:
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

Output contract: the file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble. Empty array `[]` is valid and expected when you find nothing (but the advisory gate finding is always present). Do not invent findings to fill a quota. After writing the file, print "LENS COMPLETE: tests" and stop.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
