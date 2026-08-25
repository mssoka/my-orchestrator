# Briefing: <job-id>

## Task
<one-paragraph statement of intent, in the user's words where possible>

## Context
- Repo: `<repo>` → worktree cwd of this pane (branch `<slug>`, base `<base>`)
- Relevant areas: <files/modules/docs the orchestrator identified, if any>
- Constraints: <non-goals, things not to touch, conventions>

## Definition of done
- <bullet list incl. tests/build passing>
- PR opened against `<base>` with summary + test plan

## Model policy
- This pane was launched as `<pi-launch-command>` — stay on that model.
- Mega-minion panes you spawn (max 10 concurrent): launch them with
  `<sub-pane-launch-command>` (plain `pi` if no model was specified); close
  every one when done ("badge out").

## Standing orders
Follow /Users/moses/code/docs/orchestration-playbook.md § "Minion standing
orders": use the bmad-quick-dev skill; clarify questions halt for relay
(lavish session when practical); internal checkpoints are pre-approved;
close any panes you spawn; self-report
transitions via `/Users/moses/code/bin/ledger set <job-id> <status> "<note>"`;
notify via `herdr notification show "<job-id>"` when blocked or done; commit,
push, open PR (never merge); PR description includes a "Decisions &
rationale" section.

## Review policy (MANDATORY — do not report `done` without completing this)
- Full copy of the change; before reporting `done` you MUST run **step 04**
  (bmad-build) as written: construct the diff from `baseline_commit`, and
  execute the review layers — **blind-adversarial, edge-case-hunter,
  verification-gap, acceptance-vs-spec** — **as spawned reviewer subagents**,
  then classify/triage. Verification (tests/green CI) is NOT a substitute for
  this review.
- `baseline_commit: <base>` (the commit the diff is measured against).
- Reviewer allowance: spawn the four review layers as subagents; a layer is
  the reviewer's own. One layer per reviewer subagent, run in parallel.
- Perkins opt-in: `pr_review: <0|1>` — set **1** for large/risky changes
  (a new Perkins round is then required + tracked). The orchestrator sets this
  at dispatch.
- Record the review in the ledger (via the Orchestrator): the job must be in
  `in-review` with a posted verdict (APPROVED with no open CHANGES_REQUESTED)
  BEFORE the Orchestrator runs `bin/check-pr-ready <job-id>` at close-out.

## Review loop (docs only)
This is a DOCS deliverable: run a lavish review loop BEFORE opening the PR
(build → serve → poll → apply annotations → then PR). Code keeps the
regular PR pattern.
