# LENS: Security (source: `security`)

You are reviewing a code diff. Read-only repository access for verification.

--- REPOSITORY / WORKTREE ---
Worktree: `/Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-boundary-gate-slot-clear-r1`
Canonical diff: `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-slot-clear/r1/diff.patch`

--- PROJECT CONVENTIONS ---
Python + Google ADK production agent. Compliance gates audit LLM-generated prose for protected-ground (PII/bias) references before it ships. State slots carry review verdicts + telemetry stamps. No new endpoints/routes/handlers in this diff.

--- SPEC / CONTEXT ---
- `/Users/moses/code/_bmad-output/briefings/perkins-righttenantryagents-boundary-gate-slot-clear-r1.md`
- `/Users/moses/code/_bmad-output/briefings/righttenantryagents-boundary-gate-slot-clear.md`
The diff adds two `ctx.session.state.pop(<key>, None)` lines (one per gate loop) + regression tests. Intent: clear the prior attempt's dirty review slot so a state-prop failure on a clean final attempt can't fail-close on stale data.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

For THIS diff specifically consider: could clearing the review slot let unaudited/protected-ground prose ship (a compliance-bypass / data-exposure risk)? Does the fix weaken any fail-closed guarantee? Could a stale/dirty review ever reach a consumer that ships prose? Does the test logging expose any sensitive data?

--- OUTPUT ---
ONE valid JSON array. Schema:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ, verbatim; 'N/A' only for no-code-reference findings>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}
Output contract: ONLY the JSON array. `[]` is valid and expected for a pure state-hygiene diff.
ACCURACY MANDATE: every finding re-verified against the actual code; unverified DISCARDED silently. Quote exact lines. No hedging.

--- FILE-OUTPUT CONTRACT ---
Write your final JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-slot-clear/r1/security.json`
Then stop.
