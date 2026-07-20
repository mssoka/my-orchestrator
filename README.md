# Orchestrator root (`~/code`)

Multi-repo workspace run by a single pi **mayor** session. The mayor receives
intent, dispatches work to sub-agents in Herdr worktrees, relays their
questions, tracks them in a SQLite ledger, and never implements or merges
itself.

- Operating procedure: [docs/orchestration-playbook.md](docs/orchestration-playbook.md)
- Interactive explainer (open in a browser):
  [docs/orchestration-explained.html](docs/orchestration-explained.html)

## Architecture at a glance

```
 you ──► mayor pi session (cwd = this root)
         │  .pi/extensions/mayor.ts        standing orders + startup checklist
         │  .pi/extensions/mayor-watch.ts  polls Herdr, wakes mayor on changes
         │
         ├──► Herdr  workspaces/tabs/panes + git worktrees
         │      └──► sub-agent pi sessions (one per job, in a worktree)
         │             ├── BMAD skills (bmad-quick-dev, Paige, …)
         │             ├── bin/ledger set …      self-reports status ──┐
         │             └── gh pr create ──► human reviews & merges   │
         │                                                           ▼
         └──► _bmad-output/orchestrator.db ◄────────────────── SQLite ledger
              (jobs + job_events, via bin/ledger)
```

| Component | Role |
|---|---|
| **pi mayor session** | Orchestrator. Runs only in this root; the extensions below are project-local so repo/worktree sessions are unaffected. |
| **`.pi/extensions/mayor.ts`** | Enforces standing orders: injects them into the system prompt every turn, fires the startup checklist, re-grounds after compaction. |
| **`.pi/extensions/mayor-watch.ts`** | Watcher. Every 30s diffs `herdr agent list` against ledger-tracked panes; when one stops (idle/done/blocked) or vanishes, injects a message that wakes the mayor. |
| **Herdr** | Terminal multiplexer + runtime for agents. Provides workspaces/tabs/panes, agent status detection, `herdr wait`, notifications, and git worktree management. |
| **BMAD skills** | `bmad-*` skills (installer-managed per repo, symlinked into `~/.pi/agent/skills/`). Sub-agents execute with `bmad-quick-dev`; specialist personas (e.g. Paige the tech writer) handle copy/docs. |
| **SQLite ledger** | `_bmad-output/orchestrator.db` — durable job state across Herdr restarts. Two tables: `jobs` (current state) and `job_events` (audit trail of every transition). Accessed via `bin/ledger`. |
| **`bin/ledger`** | Python3-stdlib CLI used by the mayor, by sub-agents (self-reporting), and by mayor-watch. Concurrency-safe (WAL + busy timeout). |
| **Briefings** | `_bmad-output/briefings/<job-id>.md` — the job contract a sub-agent reads at launch. |
| **`gh` / `glab`** | Sub-agents push their branch and open PRs targeting the repo's base branch. The human merges. |

## How a job flows

1. **Intake** — mayor resolves repo + base branch, asks only blocking questions.
2. **Briefing** — written to `_bmad-output/briefings/<job-id>.md`.
3. **Dispatch** — `herdr worktree create`, pane moved into the orchestrator
   workspace, worktree bootstrapped (`_bmad` copy, `.env` symlinks),
   `bin/ledger add <job-id> …` (status `dispatched`), pi launched, handover
   message sent.
4. **Work** — sub-agent runs bmad-quick-dev. On every status change it
   self-reports: `bin/ledger set <job-id> <status> "<note>"`.
5. **Clarify relay** — if it halts with numbered questions, mayor-watch sees
   the pane go idle and wakes the mayor, who pastes the questions to you
   verbatim and relays your answers back.
6. **Review** — sub-agent pushes, opens a PR, reports `in-review`, fires
   `herdr notification show`. You review and merge. **The mayor never merges.**
7. **Close-out** — after your ack: panes closed, PR merged → worktree +
   branch removed, `bin/ledger set <job-id> done "<result>"`.

Ledger statuses: `dispatched → clarifying → working → in-review → done`
(`blocked` any time).

## Daily ops

```bash
bin/ledger                       # active jobs
bin/ledger all                   # including done
bin/ledger show <job-id>         # one job + its event history
bin/ledger events [n]            # recent transitions across all jobs
bin/ledger set <id> <status> "note"   # transition (also appends job_events)
bin/ledger pr <id> <url>         # record PR URL
bin/ledger backup                # SQL dump → _bmad-output/backups/

herdr agent list                 # live agent statuses across workspaces
herdr pane read <pane> --source recent-unwrapped --lines 120
herdr pane run <pane> "<message>"     # send input to an agent
```

Herdr workspace/pane ids (`wA`, `w7`, …) are **ephemeral across restarts** —
re-resolve with `herdr agent list`; never trust ids from an old session.

---

## Setting up a new machine

Replicates this setup from scratch. (This section replaced
`docs/mayor-setup-guide.md`.)

Target state:

```
<root>/                              # e.g. ~/code — contains all repos
├── .pi/extensions/mayor.ts          # standing orders (enforcement)
├── .pi/extensions/mayor-watch.ts    # sub-agent watcher
├── bin/ledger                       # ledger CLI
├── .agents/skills/bmad-*            # BMAD skills (fresh install, step 2)
├── _bmad/                           # BMAD project config (fresh install)
├── AGENTS.md / CLAUDE.md            # slim pointers only
├── README.md                        # this file
├── docs/orchestration-playbook.md   # operating procedure
├── _bmad-output/
│   ├── orchestrator.db              # ledger DB — NOT tracked, machine-local
│   ├── backups/                     # SQL dumps — NOT tracked
│   └── briefings/_template.md       # briefing template
└── <repo1>/ <repo2>/ ...            # repos, each with .git and its own _bmad/
```

### 1. Prerequisites

- Node 22+ and pi: `npm i -g @earendil-works/pi-coding-agent` (setup used pi 0.80.x)
- Herdr ≥ 0.7.4
- `git`, `sqlite3` (macOS built-in), python3 (stdlib only), plus `gh` and/or `glab`
- LLM provider credentials configured for pi

### 2. Clone the meta repo, install BMAD fresh

The root is itself a git repo with a whitelist `.gitignore` tracking only
the orchestrator system files:

```bash
git clone git@github.com:mssoka/my-orchestrator.git <root>
```

Tracked: `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`,
`bin/ledger`, `.pi/extensions/`, `_bmad-output/` (briefing template only —
the DB and backups are deliberately untracked machine-local state).

Then install BMAD in the root and **once in each repo** (required: dispatch
does `cp -R <repo_root>/_bmad <worktree>/_bmad`):

```bash
cd <root>
npx bmad-method@latest install   # reference: v6.10.0, modules core + bmm + tea + cis
```

`_bmad/` and `.agents/skills/` are installer-managed and not tracked;
`_bmad/custom/` overrides don't travel — re-answer installer prompts or copy
`config.toml` / `config.user.toml` by hand. Create each repo's `.env` files
by hand (never in git); dispatch symlinks them into worktrees, so jobs that
need env can't run until they exist.

### 3. Fix hardcoded paths

```bash
cd <root>
rg -l '/Users/moses/code' .pi docs AGENTS.md _bmad-output bin \
  | xargs sed -i '' 's|/Users/moses/code|<root>|g'
```

Verify by hand: `MAYOR_DIR`/`PLAYBOOK`/`LEDGER_*` in `.pi/extensions/mayor.ts`
and `.pi/extensions/mayor-watch.ts`, root refs in
`docs/orchestration-playbook.md`, `_bmad-output/briefings/_template.md`,
`AGENTS.md`, and the `DB` path at the top of `bin/ledger`.

### 4. Make skills visible to pi

```bash
mkdir -p ~/.pi/agent/skills
for d in <root>/.agents/skills/bmad-*; do ln -sfn "$d" ~/.pi/agent/skills/; done
ln -sfn ~/.agents/skills/herdr ~/.pi/agent/skills/herdr
```

### 5. Launch and smoke-test

1. Inside Herdr, `cd <root>` and run `pi`. The workspace you launch in
   becomes the orchestrator workspace — no id is hardcoded anywhere; the
   mayor re-resolves it via `herdr agent list` each session.
2. `session_start` fires: the startup checklist arrives as a user message →
   the mayor reads the playbook, runs `bin/ledger`, reconciles against
   `herdr agent list`, and replies with a readiness report.
3. Confirm the system prompt contains "Mayor standing orders" (injected
   every turn, survives compaction) and that mayor-watch loaded without
   errors (it silently snapshots on `session_start`).
4. Optional: dispatch one tiny job end-to-end to validate worktree creation,
   pane moves, briefing handoff, self-reporting, and watcher alerts.

### 6. Notes

- The extensions only fire when `cwd` is exactly the root — sessions in
  repos or worktrees never orchestrate (by design).
- Mayor never implements in main checkouts and never merges PRs; max 3
  concurrent task panes unless the user says otherwise.
- The old YAML ledger (`orchestrator-jobs.yaml`) is retired; the DB is
  created on first `bin/ledger` run. Back up with `bin/ledger backup`.
- If the harness ever changes (Claude Code, Codex, …), port the extensions;
  the trimmed `AGENTS.md`/`CLAUDE.md` stay as-is.
