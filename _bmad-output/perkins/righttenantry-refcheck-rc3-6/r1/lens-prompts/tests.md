You are a Test Coverage reviewer running a SINGLE specialized lens as part of a Perkins automated review of PR #602 (RightTenantry RC3.6: Verified Webhooks — Resend + Twilio SMS inbound webhooks). This is your ONLY task: do the lens, write your output, STOP.

You have read-only access to the worktree and may verify the diff's claims against the actual code and existing tests.

CONTEXT:
- Canonical diff (the EXACT bytes under review): /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/diff.patch
- Worktree at the reviewed sha (read code + tests HERE): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1
- Project conventions: /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1/AGENTS.md
- New test files in the diff:
  - server/test/integration/reference_checks_webhooks_integration_test.gleam
  - server/test/notification/twilio_webhook_test.gleam
  - server/test/reference_checks/webhooks_test.gleam

⚠️ READ THE GUARD RAILS FIRST — /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-6-r1.md section "CRITICAL lens-guards". Flagging a guarded item is a FALSE POSITIVE. Key guards: signature verification is load-bearing — a test that a wrong/empty/misspelled signature is REJECTED (401/403) AND mutates nothing is the highest-value test; idempotent by event id — a test that re-delivering the same event does NOT double-transition/double-notify/double-audit; objection stickiness — a test that a delivery event on an already-objected row is a no-op; route registry all-THREE; in-app-only notification (no email — do NOT flag "no email test"); NO inbound STOP→objected (deliberately absent — do NOT flag "no STOP test"). The minion reported 481 integration tests green; do not re-run the suite, TRACE coverage instead. Do NOT re-open rc3-1…rc3-5 findings.

--- YOUR LENS: TEST COVERAGE (source: "tests") ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Behaviour changes to trace coverage for (prioritise these — P0/P1):
- P0: Resend webhook REJECTS unverified signatures (wrong/empty RESEND_WEBHOOK_SECRET, wrong url) with 401/403 and mutates nothing
- P0: Twilio webhook REJECTS unverified X-Twilio-Signature with 401/403 and mutates nothing
- P0: email bounced/complained/failed → reference transitions to awaiting_correction (+ NULLs next_attempt_at + AD-16 audit row + in-app notification)
- P0: SMS failed/undelivered → reference transitions to awaiting_correction
- P0: idempotency — re-delivered event id does NOT double-transition/double-notify/double-audit
- P0: objection stickiness — delivery event on already-objected row is a no-op
- P1: a correctly-computed signature is ACCEPTED and processes the event
- P1: unknown/unmapped event types are handled (no crash)
- P1: event for an unknown send_ref is handled (no crash, no spurious transition)
- P2: the awaiting_correction state is respected by the sweep (not re-selected) — may be covered by rc3-5 tests

Blind-spot heuristics: new/modified API endpoints without matching coverage; auth/authz paths missing negative tests; happy-path-only coverage where error handling is implied; new DB operations without integration coverage; new state transitions without boundary tests.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages (P0/P1/overall)
- recommended_fix: what would raise the gate

Gate thresholds: PASS = P0 100%, P1 ≥90%, overall ≥80%; CONCERNS = P0 100%, P1 80–89%, overall ≥80%; FAIL = P0 <100%, or P1 <80%, or overall <80%.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (no other path, no prose, no markdown fencing):
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/tests.json

Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap, coverage-gate>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff/test that prove the claim, pasted verbatim. 'N/A' only for findings with no possible code reference.>",
  "detail": "<rationale, ≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Empty array `[]` is valid for the gap findings EXCEPT the advisory-gate finding is always emitted. Do not invent findings to fill a quota.

ACCURACY MANDATE: NO claim will be taken at face value. Every finding is independently re-verified against the worktree + test files before it reaches the report; findings that fail verification are DISCARDED SILENTLY. Open the test files. Read them. Quote the test lines verbatim in `evidence` (or note their absence). Fewer well-grounded findings > many speculative ones.

When done, STOP. Your only job is to write the JSON array file.
