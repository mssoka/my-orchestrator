# /Users/moses/code — orchestrator root

Multi-repo workspace. Orchestration (dispatching minions, tracking jobs)
is handled exclusively by the pi **Gru** session at this directory root,
enforced by `.pi/extensions/gru.ts` — not by this file.

Naming: **Gru** = orchestrator, **minion** = dispatched task agent,
**mega-minion** = specialist helper a minion spawns. See README.md.

- Playbook: `docs/orchestration-playbook.md`
- Job ledger: SQLite at `_bmad-output/orchestrator.db` (CLI: `bin/ledger`)

If you are an agent session anywhere else (a repo under this directory, a
worktree, etc.): you are **not** Gru. Do not dispatch minions
or track jobs. Work the repo in front of you; if asked to orchestrate, point
the user at the Gru session in `/Users/moses/code`.
