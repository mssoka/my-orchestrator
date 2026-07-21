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

## Gru gotchas (field notes, learned the hard way)

- **`bin/ledger` table view is lossy.** `ledger` / `ledger all` show only
  `id, status, pane_id, github_issue, started_at, result` — no `pr`,
  `worktree`, `briefing`, etc. Never declare a field "missing" from the
  table view; verify with `ledger show <id>` or `ledger json` first.
  (2026-07-21: Gru falsely reported PRs as unrecorded and wrote redundant
  `ledger pr` entries — they had been set at the `in-review` transition.)
- **`ledger events` takes a count, not a job id.** Per-job event history:
  `ledger show <id>`.
- **`herdr agent send` does not submit.** It types text into the pane's
  input buffer and leaves it there unsent. To deliver a prompt or
  follow-up, use `herdr pane run <pane> "<text>"` (sends text + Enter
  together). If text is already stuck in a buffer, submit it with
  `herdr pane send-keys <pane> enter`. The playbook's clarify-relay
  section still names `agent send` — treat that as a doc bug; use
  `pane run`.
