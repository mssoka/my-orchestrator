# Briefing: righttenantryagents-review-pr-164

First: read `/Users/moses/code/docs/orchestration-playbook.md` section
**"Minion standing orders"** — they apply in full (work only in your
worktree, env read-only, ledger self-report, mega-minion rules,
notification on halt/finish) except where this briefing overrides.

## Task

Run an **independent multi-lens review** of PR **#164** in
`solarity-services/RightTenantryAgents` using the **code-review** skill at
`~/.pi/agent/skills/code-review/SKILL.md` (read it first; follow Steps 1–4).

PR: https://github.com/solarity-services/RightTenantryAgents/pull/164
(head `compliance-analytics-model-pin` → `develop`; 33 files, +842/−122).
What it does: pins `COMPLIANCE_REPAIR_MODEL=gemini-3.6-flash` in terraform,
sweeps flash 3.5→3.6, and adds `run_id`/`attempt`/`max_attempts`/
`remediated`/`parseable` dims to `compliance.review_completed` telemetry.

Your worktree is checked out **at the PR head** (branch `review-pr-164`
from `origin/compliance-analytics-model-pin`) so every reviewer can verify
against the real post-PR files.

### Skill Step 1 bindings (pre-answered — do not halt for these)

- **Diff source**: PR mode — `gh pr diff 164 --repo solarity-services/RightTenantryAgents`.
  ~960 changed lines, under the 3000-line threshold — proceed without chunking.
- **Spec** → `{review_mode} = "full"` (all 7 lenses incl. Acceptance Auditor):
  `_bmad-output/implementation-artifacts/spec-compliance-analytics-model-pin.md`
  (in your worktree). Context docs:
  `_bmad-output/implementation-artifacts/deferred-work.md` (same dir) and the
  original build briefing at
  `/Users/moses/code/_bmad-output/briefings/righttenantryagents-compliance-analytics-model-pin.md`.
- **Project conventions**: `GEMINI.md` / `CLAUDE.md` / `README.md` in the
  worktree root, whichever exist.

## Orchestration overrides (adapt the skill to pi)

1. **Fan-out mechanism.** The skill says "Agent tool,
   `subagent_type: general-purpose`" — pi has no Agent tool. Spawn the 7
   reviewers as **mega-minion panes** via the herdr skill: `herdr pane split`,
   launch plain `pi` in each, `herdr wait agent-status <pane> --status idle`,
   then `herdr pane run <pane> "<prompt>"`. Fire **all 7 lenses in one wave**
   (blind, edge, acceptance, security, architecture, codebase, tests) — 7 is
   within your max-10 mega-minion budget. Each pane gets the skill's prompt
   block **verbatim** (shared block + its lens brief; **Blind Hunter gets the
   diff only** — instruct it to not read repo files). Collect each pane's JSON
   output via `herdr pane read <pane> --source recent-unwrapped --lines 200`.
   **Close every mega-minion pane before you finish** (badge out — standing
   orders).
2. **No Step 5.** Do NOT run the interactive fix flow. No edits, no commits,
   no pushes, no `gh pr review --request-changes`. Steps 1–4 produce the
   report; the human decides what happens next.
3. **Deliverable.** (a) Post the consolidated Step-4 report as a **COMMENTED
   review** on the PR:
   `gh pr review 164 --repo solarity-services/RightTenantryAgents --comment --body-file <file>`.
   Prepend exactly one line to the body:
   `🤖 Automated 7-lens swarm review (code-review skill) commissioned by the maintainer — every finding re-verified against the PR head.`
   (b) End your final message with the full report + verdict so Gru can
   relay it.
4. **Ledger.** `/Users/moses/code/bin/ledger set righttenantryagents-review-pr-164 working "<note>"`
   when you start. On finish:
   `herdr notification show "righttenantryagents-review-pr-164" --body "<one-line verdict>"`.
   Do not set `done` — Gru owns that.

## Acceptance criteria

- 7 lenses fired (any failure recorded in `failed_layers`, no silent drops).
- **Skill Step 3b re-verification is mandatory** — every finding confirmed
  against the actual files at the PR head before it reaches the report;
  rejected findings discarded silently.
- Report posted as a COMMENTED review on PR #164, and repeated in your
  final message with the verdict line.

## Repo map

RightTenantryAgents: ADK multi-agent pipeline under `tenant_scorer/`
(agents, callbacks incl. telemetry callbacks, gate loops in pipeline nodes),
`deployment/terraform/` (model pins: `variables.tf`, `service.tf`),
`tests/` (unit + integration), `README.md` (analytics contract at :483).

## Env / bootstrap

- Worktree: `/Users/moses/.herdr/worktrees/RightTenantryAgents/review-pr-164`
- `_bmad` copied from the main checkout; spec + deferred-work present under
  `_bmad-output/implementation-artifacts/`.
- This repo has no root `.env` files — none linked. You are reviewing, not
  deploying: you should not need secrets. If you find you do, HALT and ask.

## Verify

- `gh pr view 164 --repo solarity-services/RightTenantryAgents --json reviews`
  shows your COMMENTED review.
- Optional: `make test`/`make lint` if a finding depends on test behaviour —
  read-only runs only.

## Model policy

Unset — pi default resolution for you and all mega-minions (launch plain `pi`).

## Skills policy

- **Your workflow skill: `code-review`** (`~/.pi/agent/skills/code-review/SKILL.md`)
  — Steps 1–4 with the overrides above.
- **Mega-minions**: no separate skill — each runs the code-review skill's
  per-lens prompt block verbatim (blind / edge / acceptance / security /
  architecture / codebase / tests), per override 1.
