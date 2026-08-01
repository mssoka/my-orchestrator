# Orchestrator root (`~/code`)

Multi-repo workspace run by a single pi **Gru** session. Gru receives
intent, dispatches work to minions in Herdr worktrees, relays their
questions, tracks them in a SQLite ledger, and never implements or merges
itself.

Naming theme (Despicable Me): **Gru** = the orchestrator, **minion** = a
dispatched task agent (one per job), **mega-minion** = a specialist helper a
minion spawns (e.g. a review swarm), **Perkins** = the automated PR-review
agent (posts verdicts as the `perkins-review` GitHub App), **Bob** = the
dreamer minion (periodic memory consolidation; his per-source readers are
**sheep**),
**nefario-watch** = the watcher gadget. Gru also *speaks* in character
to the user (playbook: "Gru persona (voice)") — artifacts like briefings
and ledger notes stay plain.

- Operating procedure: [docs/orchestration-playbook.md](docs/orchestration-playbook.md)
- Interactive explainer (open in a browser):
  [docs/orchestration-explained.html](docs/orchestration-explained.html)
- Kid-friendly explainer (how the crew works, made for sharing):
  [docs/how-gru-and-minions-work.html](docs/how-gru-and-minions-work.html)

## The crew 🍌

| | | |
|:---:|:---:|:---:|
| ![Gru](docs/images/crew/gru.png) | ![Minions](docs/images/crew/minion.webp) | ![Dr. Nefario](docs/images/crew/nefario.webp) |
| **Gru** — the boss with the plan | **The Minions** — the builders | **Dr. Nefario** — the watcher |
| ![Perkins](docs/images/crew/perkins.webp) | ![Bob](docs/images/crew/bob.webp) | ![Human](docs/images/crew/human.webp) |
| **Perkins** — the inspector | **Bob** — the dreamer | **The Human** — the final yes |

_One brain plans, many hands build. Plan first, build second. (Character
images are movie stills used inside this private project — not for
redistribution; keep the repo private.)_

## Architecture at a glance

```
 you ──► Gru pi session (cwd = this root)
         │  .pi/extensions/gru.ts        standing orders + startup checklist
         │  .pi/extensions/nefario-watch.ts  polls Herdr, wakes Gru on changes
         │
         ├──► Herdr  workspaces/tabs/panes + git worktrees
         │      └──► minion pi sessions (one per job, in a worktree)
         │             ├── BMAD skills (bmad-quick-dev, Paige, …)
         │             ├── bin/ledger set …      self-reports status ──┐
         │             └── gh pr create ──► human reviews & merges   │
         │                  (opt-in) Perkins reviews the PR first:    │
         │                  7-lens mega-minion swarm → verdict posted │
         │                  as perkins-review[bot] → rework / approve │
         │                                                           ▼
         └──► _bmad-output/orchestrator.db ◄────────────────── SQLite ledger
              (jobs + job_events, via bin/ledger)
```

| Component | Role |
|---|---|
| **Gru pi session** | Orchestrator. Runs only in this root; the extensions below are project-local so repo/worktree sessions are unaffected. |
| **`.pi/extensions/gru.ts`** | Enforces standing orders: injects them into the system prompt every turn, fires the startup checklist, re-grounds after compaction. |
| **`.pi/extensions/nefario-watch.ts`** | Watcher with five sensors. Every 30s diffs `herdr agent list` against ledger-tracked panes; every 5 min polls `gh` for in-review PRs: merge detection, CI failure sensing, review sensing (approve/changes relay), and the Perkins sensor (dispatches review rounds for `pr_review=1` jobs). Injects a message that wakes Gru. Detects only — Gru owns all ledger transitions. |
| **Herdr** | Terminal multiplexer + runtime for agents. Provides workspaces/tabs/panes, agent status detection, `herdr wait`, notifications, and git worktree management. |
| **BMAD skills** | `bmad-*` skills (installer-managed per repo, symlinked into `~/.pi/agent/skills/`). Minions execute with `bmad-quick-dev`; specialist personas (e.g. Paige the tech writer) handle copy/docs. |
| **SQLite ledger** | `_bmad-output/orchestrator.db` — durable job state across Herdr restarts. Two tables: `jobs` (current state) and `job_events` (audit trail of every transition). Accessed via `bin/ledger`. |
| **`bin/ledger`** | Python3-stdlib CLI used by Gru, by minions (self-reporting), and by nefario-watch. Concurrency-safe (WAL + busy timeout). |
| **`bin/perkins-token`** | Mints short-lived GitHub App installation tokens for Perkins (RS256 JWT via `openssl`, per-installation 0600 cache). `gh` here authenticates as the human and GitHub rejects formal reviews on your own PRs, so Perkins posts as its own actor: `perkins-review[bot]`. |
| **Briefings** | `_bmad-output/briefings/<job-id>.md` — the job contract a minion reads at launch. |
| **`gh` / `glab`** | Minions push their branch and open PRs targeting the repo's base branch. The human merges. |

## How a job flows

1. **Intake** — Gru resolves repo + base branch, asks only blocking questions.
2. **Briefing** — written to `_bmad-output/briefings/<job-id>.md`.
3. **Dispatch** — `herdr worktree create`, pane moved into the orchestrator
   workspace, worktree bootstrapped (`_bmad` copy, `.env` symlinks),
   `bin/ledger add <job-id> …` (status `dispatched`), pi launched, handover
   message sent.
4. **Work** — minion runs bmad-quick-dev. On every status change it
   self-reports: `bin/ledger set <job-id> <status> "<note>"`.
5. **Clarify relay** — if it halts with numbered questions, nefario-watch sees
   the pane go idle and wakes Gru, who pastes the questions to you
   verbatim and relays your answers back.
6. **Review** — minion pushes, opens a PR, reports `in-review`, fires
   `herdr notification show`. **The Gru never merges.**
7. **Perkins (opt-in)** — for jobs dispatched with `pr_review=1`, the
   Perkins sensor wakes Gru, who dispatches a review round: 7 lenses fan
   out as mega-minions (blind, edge, acceptance, security, architecture,
   codebase, tests), findings are re-verified against the code and
   consolidated, and the verdict posts as a `perkins-review[bot]` GitHub
   review. Request-changes relays to the minion (its push re-triggers
   Perkins; cap 3 rounds, then you're called in); approve notifies you.
   You review and merge either way.
8. **Close-out** — after your ack: panes closed, PR merged → worktree +
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
bin/perkins-token --check        # validate the Perkins GitHub App identity

herdr agent list                 # live agent statuses across workspaces
herdr pane read <pane> --source recent-unwrapped --lines 120
herdr pane run <pane> "<message>"     # send input to an agent
```

Herdr workspace/pane ids (`wA`, `w7`, …) are **ephemeral across restarts** —
re-resolve with `herdr agent list`; never trust ids from an old session.

---

## Memory

Gru has **state** (the ledger) and **procedure** (the playbook); the
memory system adds **lessons** and **episodes** so nothing learned dies
with a session, a compaction, or a worktree. Pi sessions themselves
remember nothing across restarts — these files are the brain.

| Layer | Path | Writer | Remembers |
|---|---|---|---|
| **Ledger** | `_bmad-output/orchestrator.db` | Gru + minions via `bin/ledger` | job state + full event audit trail |
| **Curated field notes** | `docs/minion-field-notes.md` | **Gru only** | durable minion lessons, promoted from shards |
| **Field-note shards** | `_bmad-output/field-notes/<job-id>.md` | the job's minion | what bit THIS job — ≤3 one-liners at badge-out |
| **Gru journal** | `_bmad-output/gru-journal/<yyyy-mm-dd>.md` | **Gru only** | episodes: what happened, decisions, open loops |
| **Gotchas** | `AGENTS.md` | **Gru only** | Gru's own curated traps |
| **Minion memlog** | `<worktree>/_bmad/scripts/memlog.py` | the minion | in-job scratchpad — commits with the branch, travels into the PR |
| **Briefings + PR "Decisions & rationale"** | `_bmad-output/briefings/`, GitHub | Gru / minions | handoff memory — a fresh minion takes over cold |

**Rituals:**

- **Startup rehydration (Gru):** playbook + `bin/ledger` + `herdr agent
  list` reconcile + the last few journal entries
  (`ls -t _bmad-output/gru-journal | head -3`). Enforced by
  `.pi/extensions/gru.ts`.
- **Wind-down (Gru):** append to today's journal — what happened,
  decisions, open loops.
- **Gotcha discipline (Gru):** every fumble becomes an AGENTS.md gotcha
  or a field note, same session.
- **Badge-out (minion):** write your shard
  (`_bmad-output/field-notes/<job-id>.md`). Minions also READ the curated
  notes at job start (standing orders) — born fresh, but briefed.
- **Consolidation (Gru):** promote durable shard lessons into
  `docs/minion-field-notes.md`; prune stale entries.

### Concurrency — by avoidance, not locks

Many agents write at once (10+ minions, each with up to 10 mega-minions).
The design makes contention impossible rather than managing it:

1. **Shard by writer.** Each minion writes only its own
   `field-notes/<job-id>.md` — no two writers ever share a file. Even a
   10-mega-minion swarm has ONE writer: the parent (helpers report
   in-pane; the parent rolls their lessons into its shard).
2. **Single-writer curated files.** Only Gru edits the curated notes,
   AGENTS.md, the playbook, and the journal. Minions never touch shared
   docs; they read the curated notes at start (read-only is free).
3. **Shared mutable state lives in SQLite, not files.** The ledger
   serializes writers (WAL + `PRAGMA busy_timeout=5000`) — that is why
   statuses are rows, not markdown.
4. **Atomic-append discipline (fallback).** If a shared append-only file
   is ever introduced: single-line entries, one `>>` (O_APPEND) write
   each — atomic on local APFS for small writes. Multi-line shared writes
   would need a `mkdir` mutex (portable; macOS has no `flock`). Prefer
   rules 1–3.

**Replicating this elsewhere:** the durable pieces are (a) one SQLite
store with a tiny CLI that everything reports through, (b) a per-job
shard directory writers can't collide in, (c) one curated lessons file
with a single owner, (d) a daily journal, (e) two rituals — rehydrate at
startup, journal at wind-down — injected into the agent's system prompt
so they survive compaction. No vector stores, no daemons: files you can
read, diff, and trust.

### Dreaming (periodic consolidation)

Every couple of days the **dream sensor** (in `nefario-watch.ts`, 5-min
tick) notices undreamed material — field-note shards or journal entries
newer than `_bmad-output/memory/last-dream` — and wakes Gru, who
dispatches **Bob**, the dreamer minion (one pane, no repo, ledger id
`dream-<yyyy-mm-dd>`; briefing: `_bmad-output/briefings/_template-dream.md`).
Bob clones the mutable memory into
`_bmad-output/memory/dream-<yyyy-mm-dd>/store/` (never edits the live
store), fans out one **sheep** per input source (shards / journal /
ledger events / churned transcripts), then consolidates: patterns with
≥2 independent sightings become **proposals** — each with target file,
the change, evidence (job ids + dates), reasoning, and a risk class
(**auto** = Gru applies; **user-ack** = the human decides). Anecdotes
become *watch items*, not edits. Gru applies auto-class edits, relays
the rest, writes the `last-dream` marker (completion, never dispatch),
and commits as `dream <date>: …`. Same concurrency rules as the live
memory: cloned store + per-sheep shards, zero locks. Full procedure:
playbook 'Dreaming (periodic memory consolidation)'.

---

## Setting up a new machine

Replicates this setup from scratch. (This section replaced
`docs/gru-setup-guide.md`.)

Target state:

```
<root>/                              # e.g. ~/code — contains all repos
├── .pi/extensions/gru.ts          # standing orders (enforcement)
├── .pi/extensions/nefario-watch.ts    # minion watcher
├── bin/ledger                       # ledger CLI
├── bin/perkins-token                # Perkins' GitHub App token minter
├── .agents/skills/bmad-*            # BMAD skills (fresh install, step 2)
├── _bmad/                           # BMAD project config (fresh install)
├── AGENTS.md / CLAUDE.md            # slim pointers only
├── README.md                        # this file
├── docs/orchestration-playbook.md   # operating procedure
├── _bmad-output/
│   ├── orchestrator.db              # ledger DB — NOT tracked, machine-local
│   ├── backups/                     # SQL dumps — NOT tracked
│   ├── field-notes/<job-id>.md      # minion lesson shards (see § Memory)
│   ├── gru-journal/<yyyy-mm-dd>.md  # Gru episodic journal (see § Memory)
│   ├── memory/last-dream + dream-*/ # Bob's marker + dream passes (§ Memory)
│   └── briefings/_template.md       # briefing template
└── <repo1>/ <repo2>/ ...            # repos, each with .git and its own _bmad/
```

Plus machine-local secrets **outside** the root: `~/.config/perkins/`
(GitHub App private key + config — never in git).

### 1. Prerequisites

- Node 22+ and pi: `npm i -g @earendil-works/pi-coding-agent` (setup used pi 0.80.x)
- Herdr ≥ 0.7.4
- `git`, `sqlite3` (macOS built-in), python3 (stdlib only), `openssl` CLI
  (macOS built-in — `bin/perkins-token` signs JWTs with it), plus `gh`
  and/or `glab`
- LLM provider credentials configured for pi

### 2. Clone the meta repo, install BMAD fresh

The root is itself a git repo with a whitelist `.gitignore` tracking only
the orchestrator system files:

```bash
git clone git@github.com:mssoka/my-orchestrator.git <root>
```

Tracked: `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`,
`bin/` (`ledger`, `perkins-token`), `.pi/extensions/`, `_bmad-output/`
(briefings, templates, artifacts — only the DB and backups are
deliberately untracked machine-local state).

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

Verify by hand: `MAYOR_DIR`/`PLAYBOOK`/`LEDGER_*` in `.pi/extensions/gru.ts`
and `.pi/extensions/nefario-watch.ts`, root refs in
`docs/orchestration-playbook.md`, `_bmad-output/briefings/_template.md`,
`AGENTS.md`, and the `DB` path at the top of `bin/ledger`.
(`bin/perkins-token` has no hardcoded root — it reads
`~/.config/perkins/config`.)

### 4. Perkins: GitHub App identity (optional, ~20 min)

Needed only if you want automated PR review. `gh` on the machine
authenticates as you, and GitHub rejects formal reviews on your own PRs
(422) — so Perkins posts as its own actor via a GitHub App.

1. GitHub → (org or user) Settings → Developer settings → GitHub Apps →
   New. Name e.g. `perkins-review`; homepage any URL; **webhook: Active
   unchecked** (the watcher polls — nothing POSTs to you); no
   callback/setup URLs, no OAuth/device flow.
2. Repository permissions: **Pull requests: read & write**, **Contents:
   read** (Metadata: read is auto-added). No org/account permissions, no
   event subscriptions.
3. Visibility: *Only on this account* covers that account's repos; choose
   *Any account* if the app must also serve repos under a second account
   you own — each installation is separate, with its own installation id
   and config line.
4. Generate a private key → save as `~/.config/perkins/app-key.pem`,
   `chmod 600`.
5. Install the app (selected repositories) and note the **installation
   id** from the installation URL. Note the **app id** from the app's
   settings page.
6. Write `~/.config/perkins/config` (`chmod 600`):
   ```
   app_id=<app id>
   key_path=/Users/<you>/.config/perkins/app-key.pem
   installation_id_<account-login>=<installation id>
   ```
   (one `installation_id_<login>` line per installed account).
7. Validate: `bin/perkins-token --check` lists the repos each
   installation can see.

Without this, everything else works — Perkins rounds just can't post
formal reviews (they fall back to PR comments via your own `gh` auth).

### 5. Make skills visible to pi

```bash
mkdir -p ~/.pi/agent/skills ~/.claude/skills
for d in <root>/.agents/skills/*; do ln -sfn "$d" ~/.pi/agent/skills/; done
# code-review / review-plan / herdr also live in the repo — link them for Claude Code too:
for s in code-review review-plan herdr; do ln -sfn <root>/.agents/skills/$s ~/.claude/skills/$s; done
ln -sfn <root>/.agents/skills/herdr ~/.agents/skills/herdr
```

(The repo's `.agents/skills/` is git-tracked and self-contained: bmad-*,
gds-*, lavish, code-review, review-plan, herdr. Skills your other projects
use but orchestration doesn't — adk-*, sentry-*, etc. — stay in
`~/.agents/skills` / `~/.claude/skills` untouched.)

### 6. Launch and smoke-test

1. Inside Herdr, `cd <root>` and run `pi`. The workspace you launch in
   becomes the orchestrator workspace — no id is hardcoded anywhere; the
   Gru re-resolves it via `herdr agent list` each session.
2. `session_start` fires: the startup checklist arrives as a user message →
   Gru reads the playbook, runs `bin/ledger`, reconciles against
   `herdr agent list`, and replies with a readiness report.
3. Confirm the system prompt contains "Gru standing orders" (injected
   every turn, survives compaction) and that nefario-watch loaded without
   errors (it silently snapshots on `session_start`).
4. Optional: dispatch one tiny job end-to-end to validate worktree creation,
   pane moves, briefing handoff, self-reporting, and watcher alerts.

### 7. Notes

- The extensions only fire when `cwd` is exactly the root — sessions in
  repos or worktrees never orchestrate (by design).
- Gru never implements in main checkouts and never merges PRs; max 10
  Gru-dispatched task panes unless the user says otherwise; minions may
  fan out max 10 concurrent child panes each (closed before the parent
  finishes).
- The old YAML ledger (`orchestrator-jobs.yaml`) is retired; the DB is
  created on first `bin/ledger` run. Back up with `bin/ledger backup`.
- Perkins is opt-in per job (`pr_review=1` at dispatch — Intake step 7 in
  the playbook); cap 3 automated rounds per PR, then the human is called
  in. Full spec: `docs/perkins-pr-review-plan.md`.
- If the harness ever changes (Claude Code, Codex, …), port the extensions;
  the trimmed `AGENTS.md`/`CLAUDE.md` stay as-is.
