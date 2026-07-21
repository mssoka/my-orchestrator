# Orchestration Playbook

How the pi orchestrator (**Gru**) dispatches and tracks work across the repos
in `/Users/moses/code` using Herdr + the BMAD quick-dev workflow.

Setting up a new machine? See `README.md` ("Setting up a new machine").

Read this at the start of any orchestration session. Minion briefings link
here for standing orders.

**Naming theme (Despicable Me):**

- **Gru** — the orchestrator pi session (formerly "mayor")
- **minion** — a dispatched task agent, one per job (formerly "sub-agent")
- **mega-minion** — a specialist helper a minion spawns, e.g. a review swarm
  (formerly "sub-sub-agent" / "child pane")

## Roles

- **Gru (orchestrator)** — the pi session in the orchestrator Herdr workspace
  (currently `wA`, label "code" — ids are ephemeral, re-resolve at session
  start). Receives user intent, runs intake, writes briefings, dispatches
  minions, relays clarify Q&A, tracks progress, closes out jobs.
- **Minion (task agent)** — a `pi` agent in a named pane in the orchestrator
  workspace, one per job, working in a git worktree of the target repo. May
  spawn its own mega-minions via the herdr skill and must close them when
  done.

## Durable state

- Job ledger: **SQLite** at `/Users/moses/code/_bmad-output/orchestrator.db`,
  accessed via the helper `/Users/moses/code/bin/ledger` (python3, stdlib
  only). `ledger` lists active jobs; `ledger all|show <id>|events|json` for
  reads; `ledger add <id> k=v ...` and `ledger set <id> <status> [note]` for
  writes. Every write appends to `job_events` (audit trail). `ledger backup`
  dumps SQL to `_bmad-output/backups/`. The old `orchestrator-jobs.yaml` is
  retired (pointer file only).
- Briefings: `/Users/moses/code/_bmad-output/briefings/<job-id>.md`
- The ledger is the source of truth across Herdr restarts. Update it on every
  status transition.

## Intake (Gru)

1. **Resolve repo.** Auto-detect: any directory under `/Users/moses/code`
   containing `.git`. Match the user's name case-insensitively; if ambiguous,
   list candidates and ask. No allow-list — the user owns all repos.
2. **Resolve base branch.** `develop` if it exists (RightTenantry repos),
   else the remote HEAD default (`main`/`master`).
3. **Ask only blocking questions** (usually 0–3). Detailed requirements
   gathering is delegated to the minion via bmad-quick-dev's step-01
   clarify — do not duplicate it.
4. **Escalation.** If the user says "full bmad" / "run the bmad method", or
   the request is clearly multi-goal or large, propose the full flow
   (bmad-prd → bmad-architecture → bmad-create-epics-and-stories) instead of
   quick-dev. Default is always quick-dev.
5. **Model (optional, never blocking).** If the user names a model for the
   minion (or for its mega-minions), record it in the ledger as `model`
   and pass it at launch (Dispatch step 6); put it in the briefing's Model
   policy. Unset means pi's default model resolution — do not ask about it.

## Dispatch (exact sequence)

Slug = kebab-case derived from intent. Job id = `<repo>-<slug>`.

1. Write briefing to `_bmad-output/briefings/<job-id>.md` (template below).
2. Fetch the base and create the worktree **from `origin/<base>`**, so a
   stale local base branch never affects the work:
   ```bash
   git -C <repo_root> fetch origin <base>     # skip if the repo has no remote
   herdr worktree create --cwd <repo_root> --branch <slug> --base origin/<base> \
     --label <job-id> --no-focus --json
   ```
   (No remote → fall back to `--base <base>`.)
   Parse `result.root_pane.pane_id` and `result.worktree.path`
   (`~/.herdr/worktrees/<repo>/<slug>`). Note: this also auto-opens a
   source-repo workspace — leave it, it is handy for main-checkout access.
3. Move the pane into the orchestrator workspace (currently `wA`). Panes
   first, tabs on overflow: if the target tab already has 2 panes (or would
   go below ~100 cols/pane), use a new tab; otherwise split the current tab:
   ```bash
   herdr pane move <pane> --tab <orch-tab> --split right --no-focus      # panes first
   herdr pane move <pane> --new-tab --workspace <orch-ws> --label <job-id> --no-focus  # overflow
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
   - Tell the minion in the briefing which env files were linked.
5. Record the job in the ledger (status `dispatched`):
   ```bash
   /Users/moses/code/bin/ledger add <job-id> repo=<repo> repo_root=<root> \
     slug=<slug> base=<base> worktree=<path> pane_id=<pane> tab_id=<tab> \
     briefing=<briefing-path> github_issue=<n>   # model=<m> if set
   ```
6. Launch pi and hand over — append `--model <model>` when the job has one
   in the ledger, otherwise launch plain:
   ```bash
   herdr pane run <pane> "pi --model <model>"   # or plain "pi" when unset
   herdr wait agent-status <pane> --status idle --timeout 60000
   herdr pane run <pane> "Read /Users/moses/code/docs/orchestration-playbook.md section 'Minion standing orders' and the briefing at <briefing-path>, then begin."
   ```

## Minion standing orders

(Also pasted into every briefing. Formerly "Sub-agent standing orders" —
older briefings use that name; this is the same section.)

- Use the **bmad-quick-dev** skill for the work. Follow its step files
  exactly, with two orchestration overrides:
  1. **Step-01 clarify**: ask your numbered questions, then HALT. Gru
     relays answers from the user. Do not proceed on guesses.
  2. **Internal approval checkpoints** (e.g. spec approval in step-02):
     pre-approved by the user — proceed without halting. Only halt for
     genuine blockers (missing access, contradictory requirements,
     destructive operations).
- Work entirely inside this pane's cwd (the worktree) on branch `<slug>`.
- You may spawn your own mega-minions with the herdr skill
  (`herdr pane split --current ...`). Launch them per the briefing's Model
  policy (`pi --model ...` when it names one). **Max 10 concurrent
  mega-minion panes** (batch larger swarms). You MUST close every pane you
  create before finishing ("badge out").
- Treat env files as read-only. If the task genuinely requires changing
  env values, replace the symlink with a copy first
  (`rm .env && cp <repo_root>/.env .env`), edit the copy, and call the
  change out in the PR description. **Never commit env files or secrets.**
- When blocked or finished, run:
  `herdr notification show "<job-id>" --body "<one-line status>"`
- **Self-report every status transition** to the ledger as it happens:
  `/Users/moses/code/bin/ledger set <job-id> <status> "<one-line note>"`
  (e.g. `clarifying` when you halt with questions, `working` once answers
  arrive, `in-review` when the PR opens). Gru's watcher reads this; do not
  skip it.
- On completion: commit on `<slug>`, `git push -u origin <slug>`, open a PR
  targeting `<base>` (`gh pr create --base <base>`; `glab mr create` for
  GitLab). End your final message with: summary, files changed, PR URL.
  **Never merge the PR** — the human reviews it. If the repo has no remote,
  leave the branch local and say so.
- The PR description must carry a **"Decisions & rationale"** section:
  load-bearing choices, rejected alternatives, anything flagged for legal
  review — so a fresh minion can take over review rounds cold.

## Tracking (Gru)

- Dashboard: `herdr agent list` and `/Users/moses/code/bin/ledger`.
- **nefario-watch** (`.pi/extensions/nefario-watch.ts`) has two sensors:
  1. **Pane watcher (30s):** diffs `herdr agent list` against ledger-tracked
     panes; injects a message when one transitions to `idle`/`done`/`blocked`
     (or vanishes). On such a message: read the transcript (`herdr pane read
     <pane> --source recent-unwrapped --lines 120`), classify (clarify halt
     vs finished vs error), update the ledger, relay to the user.
  2. **PR watcher (5 min):** polls `gh pr view` for jobs in `in-review` with
     a recorded PR. On MERGED: run close-out (which now includes pulling the
     base). On CLOSED-unmerged: ask the user (abandon vs reopen/fix).
  nefario-watch only DETECTS — it never writes the ledger. **Transition
  ownership:** merges are performed only by the human on GitHub; every ledger
  transition (including `in-review  done` at close-out) is performed by Gru
  after verifying.
- Manual wait/inspect: `herdr wait agent-status <pane> --status done --timeout N`.
  Treat `idle` and `done` as completed; `blocked` needs input.
- **Clarify relay**: when a minion halts with numbered questions
  (quick-dev step-01), paste them verbatim to the user, then send the reply
  with `herdr agent send <pane> "<answers>"` (or the user answers directly
  in the pane).
- Ledger statuses: `dispatched → clarifying → working → in-review → done`
  (`blocked` any time). Minions self-report via `bin/ledger set`; Gru
  verifies and owns `done`.

## Close-out (after the user acks the summary, or nefario-watch reports the PR merged)

1. `herdr pane close <pane>` for the minion and any leftover mega-minion
   panes; close the tab if empty.
2. PR merged → sync the local base branch, then remove the worktree and
   branch:
   ```bash
   git -C <repo_root> pull --ff-only origin <base>   # main checkout sits on <base>
   git -C <repo_root> worktree remove --force <worktree_path>
   git -C <repo_root> branch -D <slug>
   ```
   `--ff-only` never mangles a diverged/dirty checkout — if it fails, report
   it to the user instead of forcing. PR still open → keep worktree + branch,
   ledger stays `in-review`.
3. Ledger → `done` with one-line result + PR URL:
   `bin/ledger set <job-id> done "<result>" && bin/ledger clear-pane <job-id>`
   (record the PR via `bin/ledger pr <job-id> <url>`).
4. `herdr notification show "done: <job-id>"`.

Note: `herdr worktree remove` only works while the workspace is rooted at
the worktree; since panes are moved into the orchestrator workspace, cleanup
is the manual git sequence above.

Note: Herdr workspace/pane ids (`wA`, `w7`, ...) are ephemeral across Herdr
restarts — re-resolve them with `herdr agent list` at session start and
update the ledger's `pane_id` fields; never trust ids from an old session.

### In-review panes and slot contention

Keep in-review panes open by default — the same minion can take review
feedback with full context. **Reclaim on contention**: when Gru needs a
slot for a new dispatch and none is free, close the oldest in-review panes
first (worktrees/branches stay; review rounds go to a fresh minion with the
PR + branch + briefing as context — the PR's "Decisions & rationale"
section is what makes this safe). Also close in-review panes that have sat
unacked for > 3 days (mention it in the readiness report).

## Concurrency

Two tiers, both policy (Herdr itself enforces no limit):

- **Minions (Gru-dispatched task jobs): max 10 panes** by default; ask the
  user before exceeding.
- **Mega-minions (minion-spawned helpers): max 10 concurrent child panes
  per minion** (e.g. the 7-perspective code-review swarm fits in one wave).
  Mega-minion panes do NOT count against the 10-job cap — they are bursty
  and short-lived — but every one must be closed before its minion finishes.
- **Safety valve:** if total agent panes in the orchestrator workspace
  exceed ~20, pause new dispatches and check with the user.

## Skills availability

All `bmad-*` skills are symlinked into `~/.pi/agent/skills/`, so pi agents
see them from any cwd (including worktrees). The herdr skill is already
global. `_bmad` project config is copied into each worktree at dispatch.
