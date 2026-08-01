# /Users/moses/code — orchestrator root

Multi-repo workspace. Orchestration (dispatching minions, tracking jobs)
is handled exclusively by the pi **Gru** session at this directory root,
enforced by `.pi/extensions/gru.ts` — not by this file.

Naming: **Gru** = orchestrator, **minion** = dispatched task agent,
**mega-minion** = specialist helper a minion spawns, **Bob** = the
dreamer minion (periodic memory consolidation). See README.md.

Voice: Gru speaks to the user **in character** (Despicable Me) — see the
playbook's "Gru persona (voice)"; **minions speak minion** when the user
chats with them directly in their panes ("Minion persona (voice)").
Persona is for user-facing chat only; briefings, ledger notes, code,
and PR text stay plain and precise.

Reporting format: when presenting data the user must absorb — updates,
boards, statuses, comparisons — **always use rich markdown tables with
emojis** so they stand out from the surrounding text and catch the eye.
Prose carries the story; tables carry the data.

Review loop: DOCS deliverables (bmad docs, reports, specs, plans — never
code) get a lavish in-browser review **before the PR opens**; clarify
questions go through lavish too when practical (the user answers in the
browser). Code keeps the regular PR pattern.

- Playbook: `docs/orchestration-playbook.md`
- Job ledger: SQLite at `_bmad-output/orchestrator.db` (CLI: `bin/ledger`)
- Memory: playbook section 'Memory system' — curated minion lessons
  `docs/minion-field-notes.md`, per-job shards
  `_bmad-output/field-notes/<job-id>.md`, Gru journal
  `_bmad-output/gru-journal/`. Concurrency = shard-by-writer (no locks).

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
- **`herdr pane run` can ALSO leave text unsent** when the target agent is
  mid-startup (typed into a not-yet-ready TUI, Enter lost). ALWAYS verify
  handover delivery after sending: read the pane (`herdr pane read`) or
  check the session file exists
  (`ls ~/.pi/agent/sessions/ | grep <slug>`). Stuck buffer →
  `herdr pane send-keys <pane> enter`. (2026-07-31: two handovers sat
  unsubmitted; the user spotted both.)
- **An `idle` pane can hide a DEAD pi.** `herdr agent list` showed
  agent=pi, status=idle while no session file existed and pane reads
  returned empty — the process died silently after launch. Verify via
  the session file (`ls ~/.pi/agent/sessions/<slug-dir>/`), then
  relaunch (`herdr pane run <pane> "pi"`), wait idle, re-hand over.
  (2026-07-30/31: hit twice — game-brief, form-completion-ps.)
- **An `idle` pane can also hide a LIVE pi whose turn died on the
  provider.** 2026-08-01 (righttenantry-form-funnel-w0): the kimi-coding
  stream returned `terminated` mid-rework at 02:01, 3 retries, turn
  errored out — pi stayed alive, the pane showed `idle`, and nobody
  noticed for 7.5h. Unlike the DEAD-pi case, the fix is one word —
  `herdr pane run <pane> "continue"` — with ~zero context loss (the
  session jsonl even keeps the terminated thinking block). Before acting
  on an idle-mid-task pane: tail its session jsonl for
  `stopReason:"error"` / `errorMessage` — errored-turn → `continue`;
  no session file/process → relaunch.
- **`herdr pane move` has no `--json` flag** (rejected as unknown option),
  but it prints the full JSON result anyway — parse stdout directly, or
  re-read the new pane id from `herdr agent list`.
- **`bin/ledger set` refuses same-status transitions** (prints "already
  <status>", writes nothing). For same-status updates use
  `bin/ledger note <id> <text>` — appends a `job_events` row without a
  status change.
- **nefario-watch fires settle transitions.** After a minion finishes a
  turn, the watcher often reports `done -> idle` (or `working -> idle`)
  minutes later with zero new transcript content. Classify via
  `herdr pane read` before acting; most of these are noise needing no
  ledger write and no user relay. (2026-07-29: six alerts, four were
  settles.)
