You are lens 'tests' in a Perkins automated code review — round 2 of 3 (FIX-AUDIT).

Round 1 reviewed sha 39443b2 (CHANGES_REQUESTED: B1 blocker + W1/W2 warnings + 6 notes).
Round 2 reviews sha b1ebd96: the rework claims B1 (telemetry event-name restored), W1
(producer-path tests), W2 (violation_count hardening). Core fix unchanged. Suite claim:
2049 passed (r1 was 2041 green + 1 failed = the B1 typo; r2 = 2041 + 1 restored + 7 new
W1/W2 = 2049).

--- PROJECT CONVENTIONS (RightTenantryAgents) ---
- Python + google-adk==2.2.0. Production ADK agent code on a paying-user path.
- Cross-agent / child-output_key state MUST be read via ctx.session.state, NOT ctx.state.
- Compliance gates remediation-first, NON-retryable; fail-closed-on-missing-review.
- Structured event names are a stable BQ/Sentry contract.

--- DIFF (read it with your read tool) ---
Canonical diff file: /Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r2/diff.patch

--- SPEC / CONTEXT (read with your read tool) ---
  Perkins r2 briefing (lens-guards): /Users/moses/code/_bmad-output/briefings/perkins-righttenantryagents-boundary-gate-state-fix-r2.md
  Job briefing (the fix spec + ACs): /Users/moses/code/_bmad-output/briefings/righttenantryagents-boundary-gate-state-fix.md
  GitHub issue #172: `gh issue view 172 --repo solarity-services/RightTenantryAgents --json title,body`

--- WORKTREE (for verification reads + RUN the tests) ---
Worktree at the reviewed sha: /Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-boundary-gate-state-fix-r2
Run: `cd <worktree> && uv run pytest tests/unit -q` (venv is present). You may also run a
single test file: `uv run pytest tests/unit/test_gate_state_marshalling.py -q`.

--- YOUR LENS ---
Test coverage analysis via traceability. For each behaviour change in the diff, trace to a
test (new or existing). Classify FULL / PARTIAL / NONE. Emit one finding per gap with:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

FIX-AUDIT FOCUS (verify each, quoting the test lines):
- B1: does test_unparseable_review_emits_failed_rollup assert the RESTORED event name
  'compliance.review_unparseable' (not 'review_unparsable')? RUN it to confirm it passes.
- W1: do test_clean_review_stamps_passed_verdict / test_dirty_review_stamps_failed_verdict_with_count
  / test_unparsable_review_stamps_failed_verdict (boundary) and test_clean_final_review_stamps_passed_verdict
  / test_unparsable_final_review_stamps_failed_verdict (final) drive the REAL
  log_boundary_compliance_review / log_final_compliance_review callbacks (not hand-seeded
  stamps) and assert the stamp fields (judge_kind, run_id, attempt, passed, parseable,
  violation_count)? Are they REAL (RUN them) or tautological?
- W2: do test_passed_true_with_violations_still_fail_closes (BOTH gates) actually cover the
  inconsistent-stamp direction? Does the clean path
  (test_none_review_with_clean_stamp_does_not_abort) still pass? RUN the new test file.
- Are any new tests skipped, xfailed, or asserting trivially (e.g. asserting a constant
  equals itself)? Is the 2049-passed claim real (RUN the unit suite)?

Finally, emit ONE advisory gate finding: title "Advisory test gate: PASS|CONCERNS|FAIL",
category "coverage-gate", severity note(PASS)/warning(CONGERNS)/blocker(FAIL), detail with
coverage rationale. Gate: PASS = P0 100% & P1>=90% & overall>=80%; FAIL = P0<100% or P1<80%.

ACCURACY MANDATE — the most important instruction:
NO claim you make will be taken at face value. Every finding is independently
re-verified against the actual codebase before it reaches the report. Findings that
fail verification are DISCARDED SILENTLY.
- Open the file. Read the relevant lines. Do not guess from filenames. RUN the tests.
- The 'evidence' field must contain the EXACT lines you read (verbatim) or the pytest output.
- Hedging ('might','could','possibly') means you haven't verified. Verify or drop.
- Prefer fewer, well-grounded findings. An empty array [] is a fine, honest answer.

OUTPUT SCHEMA — return ONE valid JSON array. Each element:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ or pytest output, verbatim>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}
Output contract: ONLY the JSON array. No prose, no markdown fencing, no preamble.
Empty array [] is valid and expected when nothing is wrong. Do NOT invent findings.

FILE-OUTPUT CONTRACT:
Write ONLY your final JSON array to this exact path (use your write tool), then STOP:
  /Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r2/tests.json
Do not write anything else anywhere. Do not post to GitHub. Do not edit any file in the
worktree (you may RUN pytest, which is read-only). After writing the JSON file, you are done.
