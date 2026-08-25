You are lens 'edge' in a Perkins automated code review (round 1 of 3).

--- PROJECT CONVENTIONS ---
PROJECT CONVENTIONS (RightTenantryAgents):
- Python + google-adk==2.2.0. Production ADK agent code on a paying-user path.
- Codebase convention (documented in comments at tenant_scorer/agent.py:263 & :396):
  cross-agent / child-output_key state MUST be read via ctx.session.state (the
  raw live session dict), NOT ctx.state (a State wrapper whose _value is a
  snapshot captured at Context construction — stale if session.state is
  reassigned during a child run_node). The repair keys already follow this.
- Compliance gates are remediation-first, NON-retryable on exhaustion (issue #156):
  a deterministic content violation surfaces to the caller without triggering
  Gleam's full-pipeline retry. Fail-closed-on-missing-review is the safety
  invariant: never ship unaudited prose.
- First-error-wins: never overwrite a STATE_PIPELINE_ERROR a sibling already set.
- Logging uses structured event names (e.g. 'compliance.review_completed',
  'boundary_gate.exhausted') queried in BigQuery/Sentry — these strings are a
  stable observable contract.

--- DIFF (read it with your read tool) ---
Canonical diff file: /Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1/diff.patch

--- SPEC / CONTEXT (read with your read tool) ---
  Perkins briefing (your reviewer instructions + lens-guards): /Users/moses/code/_bmad-output/briefings/perkins-righttenantryagents-boundary-gate-state-fix-r1.md
  Job briefing (the fix spec + acceptance criteria): /Users/moses/code/_bmad-output/briefings/righttenantryagents-boundary-gate-state-fix.md
  GitHub issue #172 (the bug): read via `gh issue view 172 --repo solarity-services/RightTenantryAgents --json title,body`

--- WORKTREE (for verification reads) ---
Worktree at the reviewed sha: /Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-boundary-gate-state-fix-r1
Read files here to verify every claim. The venv is at /Users/moses/code/RightTenantryAgents/.venv (source it for pytest).

--- YOUR LENS ---
You are a pure path tracer. Do NOT comment on whether code is good or bad —
list ONLY unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly
reachable from the diff hunks. Derive edge classes from the changed code itself.
Examples: boundary conditions (empty lists, nulls, zero counts, max sizes),
concurrent/race conditions, unhandled error paths in new code, external service
unavailability, off-by-one errors, implicit type coercion, state the new code
doesn't account for, input the new code doesn't validate, type-shape assumptions
(e.g. State vs dict, .get on a non-dict).

For each path, determine whether the diff handles it. Report ONLY unhandled paths
that lack an explicit guard. No editorializing.

ACCURACY MANDATE — the most important instruction:
NO claim you make will be taken at face value. Every finding is independently
re-verified against the actual codebase before it reaches the report. Findings
that fail verification are DISCARDED SILENTLY.
- Open the file. Read the relevant lines. Do not guess from filenames.
- The 'evidence' field must contain the EXACT lines you read (verbatim). A
  finding without locatable evidence is a hallucination — drop it.
- Hedging ('might','could','possibly') means you haven't verified. Verify or drop.
- Prefer fewer, well-grounded findings. An empty array [] is a fine, honest answer.

OUTPUT SCHEMA — return ONE valid JSON array. Each element:
{
  "source": "<your source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ, verbatim. 'N/A' ONLY for findings with no possible code reference>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}
Output contract: ONLY the JSON array. No prose, no markdown fencing, no preamble.
Empty array [] is valid and expected when nothing is wrong. Do NOT invent findings.

FILE-OUTPUT CONTRACT:
Write ONLY your final JSON array to this exact path (use your write tool), then STOP:
  /Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1/edge.json
Do not write anything else anywhere. Do not post to GitHub. Do not edit any file
in the worktree. After writing the JSON file, you are done.
