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
- Helper panes you spawn: launch them with `<sub-pane-launch-command>`
  (plain `pi` if no model was specified); close them when done.

## Standing orders
Follow /Users/moses/code/docs/orchestration-playbook.md § "Sub-agent standing
orders": use the bmad-quick-dev skill; clarify questions halt for relay;
internal checkpoints are pre-approved; close any panes you spawn; notify via
`herdr notification show "<job-id>"` when blocked or done; commit, push, open
PR (never merge).
