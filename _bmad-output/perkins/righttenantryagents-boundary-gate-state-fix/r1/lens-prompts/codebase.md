You are lens 'codebase' in a Perkins automated code review (round 1 of 3).

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
Reality check against the actual codebase. Verify by reading files, not assuming:
- Do files, functions, types, imports referenced in the diff exist and match?
  (e.g. read_review_verdict, _stamp_review_verdict, STATE_COMPLIANCE_REVIEW_VERDICT,
   _run_attempt_dims, _judge_kind, finalize_*_gate signatures.)
- Are naming conventions / style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere?
- Are new constants/imports available (STATE_COMPLIANCE_REVIEW_VERDICT in constants.py)?
- Are there existing tests this diff likely breaks? Name them.
- Does it leave orphan code?
CRITICAL: grep for ANY remaining ctx.state.get(...) read of a CHILD output_key in
the gate code or the finalize callbacks — that would be the same bug, unfixed.
Also confirm the STATE_PIPELINE_ERROR reads still use ctx.state.

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
  /Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1/codebase.json
Do not write anything else anywhere. Do not post to GitHub. Do not edit any file
in the worktree. After writing the JSON file, you are done.
