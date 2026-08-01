You are reviewing a code diff. You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r1) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line.

--- SPEC / CONTEXT ---
This diff adds PostHog funnel analytics (scripts/js-tests/apply_analytics.test.js tests server/priv/static/apply_analytics.js), Resend email tracking, a two-stage reminder series, and copy pack edits. The spec requires: unit tests on payload shapes + the submit/error/reload disambiguation for the confirmation event; reminder send machinery tested. Skim _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md at your cwd if useful.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints or handlers (application_handler, inbound_handler, vacancy_handler changes) without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied (e.g. Resend send failure clearing its stamp — claimed self-healing; is it tested?)
- New DB operations (new SQL files, sender-state view) without integration coverage
- New state transitions (reminder stage 1 → stage 2) without boundary tests
- Analytics: consent gate on/off, PII exclusion, anon id persistence, submit-vs-error-vs-reload disambiguation, section abandon derivation — tested?
- Do the new JS tests actually run in CI / make test (check Makefile and package.json wiring)?

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
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/tests.json

Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap, coverage-gate>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings with no possible code reference (e.g. a missing test). Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
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
