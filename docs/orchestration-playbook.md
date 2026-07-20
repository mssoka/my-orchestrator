# Orchestration Playbook

How the pi orchestrator (mayor) dispatches and tracks work across the repos in
`/Users/moses/code` using Herdr + the BMAD quick-dev workflow.

Read this at the start of any orchestration session. Sub-agent briefings link
here for standing orders.

## Roles

- **Orchestrator** — the pi session in the `code` Herdr workspace. Receives
  user intent, runs intake, writes briefings, dispatches sub-agents, relays
  clarify Q&A, tracks progress, closes out jobs.
- **Task sub-agent** — a `pi` agent in a named pane in the `orchestrator`
  Herdr workspace (`w7`), one per job, working in a git worktree of the
  target repo. May spawn its own throwaway sub-agents via the herdr skill
  and must close them when done.

## Durable state

- Job ledger: `/Users/moses/code/_bmad-output/orchestrator-jobs.yaml`
- Briefings: `/Users/moses/code/_bmad-output/briefings/<job-id>.md`
- The ledger is the source of truth across Herdr restarts. Update it on every
  status transition.

## Intake (orchestrator)

1. **Resolve repo.** Auto-detect: any directory under `/Users/moses/code`
   containing `.git`. Match the user's name case-insensitively; if ambiguous,
   list candidates and ask. No allow-list — the user owns all repos.
2. **Resolve base branch.** `develop` if it exists (RightTenantry repos),
   else the remote HEAD default (`main`/`master`).
3. **Ask only blocking questions** (usually 0–3). Detailed requirements
   gathering is delegated to the sub-agent via bmad-quick-dev's step-01
   clarify — do not duplicate it.
4. **Escalation.** If the user says "full bmad" / "run the bmad method", or
   the request is clearly multi-goal or large, propose the full flow
   (bmad-prd → bmad-architecture → bmad-create-epics-and-stories) instead of
   quick-dev. Default is always quick-dev.

## Dispatch (exact sequence)

Slug = kebab-case derived from intent. Job id = `<repo>-<slug>`.

1. Write briefing to `_bmad-output/briefings/<job-id>.md` (template below).
2. Create the worktree:
   ```bash
   herdr worktree create --cwd <repo_root> --branch <slug> --base <base> \
     --label <job-id> --no-focus --json
   ```
   Parse `result.root_pane.pane_id` and `result.worktree.path`
   (`~/.herdr/worktrees/<repo>/<slug>`). Note: this also auto-opens a
   source-repo workspace — leave it, it is handy for main-checkout access.
3. Move the pane into the orchestrator workspace (`w7`). Panes first, tabs
   on overflow: if the target tab already has 2 panes (or would go below
   ~100 cols/pane), use a new tab; otherwise split the current tab:
   ```bash
   herdr pane move <pane> --tab <w7-tab> --split right --no-focus      # panes first
   herdr pane move <pane> --new-tab --workspace w7 --label <job-id> --no-focus  # overflow
   ```
   Re-read the new pane id from the JSON response. Rename the pane
   (`herdr pane rename <pane> <job-id>`) and tab (`herdr tab rename`).
4. **Worktree bootstrap** (worktrees only get git-tracked files):
   - If `<worktree>/_bmad` is missing and `<repo_root>/_bmad` exists:
     `cp -R <repo_root>/_bmad <worktree>/_bmad`
   - **Env files** (gitignored, so absent from the worktree): **symlink**
     them from the main checkout — single source of truth, no drift, no
     secret copies left behind:
     ```bash
     for f in <repo_root>/.env <repo_root>/.env.*; do
       [ -f "$f" ] && ln -sf "$f" "<worktree>/$(basename "$f")"
     done
     ```
     Env files in subdirectories: list them explicitly in the briefing and
     symlink the same way. Gitignore rules apply in the worktree too, so the
     symlinks are never committed.
   - Tell the sub-agent in the briefing which env files were linked.
5. Record the job in the ledger (status `dispatched`).
6. Launch pi and hand over:
   ```bash
   herdr pane run <pane> "pi"
   herdr wait agent-status <pane> --status idle --timeout 60000
   herdr pane run <pane> "Read /Users/moses/code/docs/orchestration-playbook.md section 'Sub-agent standing orders' and the briefing at <briefing-path>, then begin."
   ```

## Sub-agent standing orders

(Also pasted into every briefing.)

- Use the **bmad-quick-dev** skill for the work. Follow its step files
  exactly, with two orchestration overrides:
  1. **Step-01 clarify**: ask your numbered questions, then HALT. The
     orchestrator relays answers from the user. Do not proceed on guesses.
  2. **Internal approval checkpoints** (e.g. spec approval in step-02):
     pre-approved by the user — proceed without halting. Only halt for
     genuine blockers (missing access, contradictory requirements,
     destructive operations).
- Work entirely inside this pane's cwd (the worktree) on branch `<slug>`.
- You may spawn your own sub-agents with the herdr skill
  (`herdr pane split --current ...`). You MUST close every pane you create
  before finishing.
- Treat env files as read-only. If the task genuinely requires changing
  env values, replace the symlink with a copy first
  (`rm .env && cp <repo_root>/.env .env`), edit the copy, and call the
  change out in the PR description. **Never commit env files or secrets.**
- When blocked or finished, run:
  `herdr notification show "<job-id>" --body "<one-line status>"`
- On completion: commit on `<slug>`, `git push -u origin <slug>`, open a PR
  targeting `<base>` (`gh pr create --base <base>`; `glab mr create` for
  GitLab). End your final message with: summary, files changed, PR URL.
  **Never merge the PR** — the human reviews it. If the repo has no remote,
  leave the branch local and say so.

## Tracking (orchestrator)

- Dashboard: `herdr agent list` and `herdr pane list --workspace w7`.
- Wait/inspect: `herdr wait agent-status <pane> --status done --timeout N`,
  then `herdr pane read <pane> --source recent-unwrapped --lines 120`.
  Treat `idle` and `done` as completed; `blocked` needs input.
- **Clarify relay**: when a sub-agent halts with numbered questions
  (quick-dev step-01), paste them verbatim to the user, then send the reply
  with `herdr agent send <pane> "<answers>"` (or the user answers directly
  in the pane).
- Ledger statuses: `dispatched → clarifying → working → in-review → done`
  (`blocked` any time).

## Close-out (after the user acks the summary)

1. `herdr pane close <pane>` for the sub-agent and any leftover child panes;
   close the tab if empty.
2. PR merged → remove the worktree and branch:
   ```bash
   git -C <repo_root> worktree remove --force <worktree_path>
   git -C <repo_root> branch -D <slug>
   ```
   PR still open → keep both, ledger stays `in-review`.
3. Ledger → `done` with one-line result + PR URL.
4. `herdr notification show "done: <job-id>"`.

Note: `herdr worktree remove` only works while the workspace is rooted at
the worktree; since panes are moved into `w7`, cleanup is the manual git
sequence above.

## Concurrency

Max 3 active task panes by default; ask the user before exceeding.

## Skills availability

All `bmad-*` skills are symlinked into `~/.pi/agent/skills/`, so pi agents
see them from any cwd (including worktrees). The herdr skill is already
global. `_bmad` project config is copied into each worktree at dispatch.
