# /Users/moses/code — orchestrator root

Multi-repo workspace. Orchestration (dispatching sub-agents, tracking jobs)
is handled exclusively by the pi **mayor** session at this directory root,
enforced by `.pi/extensions/mayor.ts` — not by this file.

- Playbook: `docs/orchestration-playbook.md`
- Job ledger: `_bmad-output/orchestrator-jobs.yaml`

If you are an agent session anywhere else (a repo under this directory, a
worktree, etc.): you are **not** the orchestrator. Do not dispatch sub-agents
or track jobs. Work the repo in front of you; if asked to orchestrate, point
the user at the mayor session in `/Users/moses/code`.
