You are reviewing a code diff (round 2 of an automated review loop). You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r2 — a detached worktree at exactly the reviewed sha 7bb582443d3844d6d349d0144b4caab42c81f196) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line (~5100 lines).

--- ROUND 2 CONTEXT ---
This PR was reviewed once already (round 1). R1 findings on your lens (the head commit claims "test pins" addressed them — verify each):
1. Resend tags array + both new reminder subject lines untested (spec requires tags on every applicant email) — email_client.gleam
2. data-section-id SSR emission on all 8 sections had zero server-side assertions
3. Stage-1 self-heal clear untested; no aged-stamp (>10 min) negative test on either clear
4. Send-failure → stamp-clear wiring ran in background against empty key, never asserted (awaiting_integration_test.gleam:645)
5. Advisory test gate was CONCERNS.
Verify the new tests actually exist AND actually assert the claimed behavior (read them — a test that can't fail is not coverage). Then do a fresh coverage pass over the whole diff.

--- SPEC / CONTEXT (read if you need intent) ---
1. /Users/moses/code/_bmad-output/briefings/righttenantry-form-funnel-w0.md — the original job briefing (Acceptance section: "unit tests on payload shapes + the submit/error disambiguation").
2. _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md (at your cwd) — the frozen implementation spec, incl. the Tests execution checklist and Verification section.

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
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/tests.json

Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: the file must contain ONLY the JSON array. No prose, no fencing, no preamble. Empty array `[]` is valid. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames or assume.
- The `evidence` field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it.
- Hedging language ("might", "could", "possibly") means you have not verified — either verify and report crisply, or drop it.
- Prefer fewer, well-grounded findings over many speculative ones. Accuracy > volume.

After writing the file, reply with one line: count of findings written. Then stop.
