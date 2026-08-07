# /Users/moses/code — orchestrator root

Multi-repo workspace. Orchestration is handled by two pi sessions at
this directory root: **Gru** (CEO — user interface, launched `PI_GRU=1 pi`,
enforced by `.pi/extensions/gru.ts`) and **Silas** (COO — all operations,
launched `PI_SILAS=1 pi`, pane label `silas`, enforced by
`.pi/extensions/silas.ts` + `nefario-watch.ts`) — not by this file.

Naming: **Gru** = CEO (user interface), **Silas** = COO (operations),
**minion** = dispatched task agent,
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
  `_bmad-output/gru-journal/`, Silas journal
  `_bmad-output/silas-journal/`. Concurrency = shard-by-writer (no locks).

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
- **Silas: a deliverable is not reported until it reaches Gru's input.**
  Text in Silas' own pane output is thinking-out-loud — Gru only sees
  what arrives via `herdr pane run <gru-pane> "[SILAS] ..."`. Every
  completed ops task (PRs opened, close-outs, dispatches) ends with that
  one-line message carrying the deliverables (URLs, pane ids). (2026-08-01:
  research PRs #559/#560 went unreported; Gru relayed the URLs himself.)
- **Silas: minions never split into identity tabs.** Dispatch step 3:
  the `gru` and `silas` tabs carry their owner only — minion panes go to
  a dedicated minions tab or a new tab labeled `<job-id>`; after any
  accidental split, move the minion out AND relabel the identity tab
  back to its bare owner name. (2026-08-01: form-stepper-f1 launched as
  a split of the silas tab; t2 kept 'silas+form-stepper-f1' after the
  move until relabeled.)
- **A pi launched with cwd=`/Users/moses/code` IS Gru** — gru.ts guards on
  `ctx.cwd` alone, so the session gets the startup checklist as a user
  message + Gru standing orders every turn, and its session file lands in
  Gru's own session dir. Dream passes launch Bob with
  `cd ~/.herdr/bob-home && pi`; never hand a non-Gru agent a pane rooted at
  the orchestrator root. (2026-08-01: dream-2026-08-01 + 3 sheep ran as
  pseudo-Grus; Bob caught it himself mid-dream.)
- **A raw backtick in an extension's template literal kills the whole
  extension at load** (ParseError — the pane boots to a dead prompt with
  only "Failed to load extension" on screen). STANDING_ORDERS strings in
  gru.ts/silas.ts are template literals: escape every inline `code` span
  as \\`. (2026-08-01: Silas' first launch died on gru.ts:41 — four
  unescaped pairs.)
- **Provider incidents come in 3 classes with different recoveries
  (2026-08-02/03).** Transient stalls, mid-turn refusals, and
  connection-error waves all leave a LIVE pi with `stopReason:"error"` in
  the session jsonl — `herdr pane run <pane> "continue"` revives them (one
  continue per pane, no loops; a fleet wave = one continue per pane, then
  verify any reviewed sha is unchanged). An account-wide quota 403 is
  different: panes are DEAD and `continue` does nothing — sweep the dead
  panes, re-add the worktree at the same sha, re-dispatch the SAME round
  row with a regenerate-everything amendment (stale partial lens JSONs
  contaminate the verdict), and take another job's activity as evidence
  the quota lifted. Second failure -> `blocked` + escalate. (2026-08-02:
  quota 403 killed Perkins r2 mid-round — retry run clean, 21/21 lens
  verdicts regenerated; same day a connection wave blocked 9 panes, all
  revived with continue x9.) 2026-08-07 addendum: glm-5.2 is a 4th class —
  it fails at LAUNCH (bare label → opencode provider, no key) AND mid-turn
  (429 rate-limit); `continue` may revive a 429 once but it re-429s — the
  durable fix is a MODEL REDIRECT to deepseek, not continue (the full path
  `zai-coding-cn/glm-5.2` auths where the bare label fails). Also `PI_MODEL`
  env silently overrides the dispatched `--model` — when model provenance
  matters (e.g. a Perkins-reviewed sha), check `PI_MODEL` / the session
  jsonl, don't trust the dispatch label. And a quota-403 that kills a round
  at STARTUP (dispatched-pending, no mid-work lens JSON) is continue-
  revivable once the quota returns — lighter than the full sweep+regenerate
  doctrine, which is for panes that died MID-WORK.
- **Review/Perkins/cap sensors re-fire already-acted events — expect one
  stale echo per action (2026-08-01/02).** Silas relays/escalates/
  dispatches at round close-out; the sensor tick lands seconds-to-minutes
  later and re-alerts the same review/sha/cap. Distinct from settle
  transitions: answer every echo with a same-status `ledger note`
  ("already relayed — no double X"), never a second action. Durable dedup
  (round row + full-sha note written the SAME minute as the dispatch) is
  what silences per-tick re-alerts; when two sensors race (review-sensor
  vs pane-watcher), relay on whichever arrives FIRST and note-only the
  twin. (2026-08-02: three races in one day on PR #563 alone.)
- **Perkins can self-close its round row (2026-08-02).** Closing the
  Perkins pane writes `working -> done` before Silas' close-out
  `set done`, which then no-ops (same-status) and eats the verdict
  detail. Write the verdict as a pre-emptive `ledger note` at close-out
  instead of discovering the loss later. 2026-08-07 addendum: self-close is
  now the NORM (10/10 rounds this window closed clean, 0 lens leftovers) —
  capture the verdict at/before close-out every time. Two new post-failure
  flavors: if Perkins completes the analysis but dies pre-POST, Silas posts
  the review from the complete artifacts (`body.md` + `consolidated.json`) —
  no re-run; if the token mint fails, the review posts via fallback-comment
  automatically. And deepseek rounds self-close the ROW reliably but leave
  the WORKTREE + lens panes behind more than kimi did — always verify +
  sweep worktree / branch / lenses at close-out, don't assume.
- **Ground truth for pane forensics is the session jsonl, not env
  scraping (2026-08-01/03).** The bash tool's env is NOT a proxy for a
  pane's pi process env (PI_GRU/PI_SILAS are invisible to it). Which
  extensions are armed = the jsonl's entry types (`custom_message` =
  extension-injected; `message` role=user = typed). A worktree's session
  dir holds the minion's AND its mega-minions' sessions (shared cwd) —
  identify the live pane's file via `herdr pane get <pane>` agent_session,
  never by newest mtime.
- **Never yield a turn between `herdr wait idle` and the handover
  (2026-08-06).** The dispatch boot sequence — `herdr pane run <pane>
  "pi"` → `herdr wait agent-status <pane> --status idle` → `herdr pane
  run <pane> "<handover>"` — is ONE continuous flow; the `wait`
  succeeding IS the green light (nothing left to verify before handing
  over). A minion at idle with no handover is dead time (blank pane,
  zero progress). PREVENTION: chain all FOUR in a single bash `&&` command —
  `herdr pane run <pane> "pi"` && `herdr wait agent-status <pane>
  --status idle --timeout 90000` && **`sleep 3`** && `herdr pane run
  <pane> "<handover>"`. The `sleep 3` AFTER idle is REQUIRED, not
  optional: `wait --status idle` returns the instant pi reports idle,
  but the TUI's input handler isn't always ready to accept keystrokes
  at that exact moment — without the sleep, the chained handover types
  into a not-yet-ready TUI and Enter is lost (buffer sits unsent; pane
  stays idle with an empty session). SEEN TWICE on 2026-08-06
  (agent-model-flash + RT-Agents: both chained dispatches left the
  minion idle until `send-keys enter` recovered them; the non-chained
  csp dispatch with a natural gap did NOT hit it). Then verify delivery
  as a SEPARATE post-step (working within ~30s, else `herdr pane
  send-keys <pane> enter` for a stuck buffer) — sleep + verify together
  make it reliable.
  (2026-08-06: cost-analysis minion sat blank ~30s after boot because
  Silas ended the turn after the `wait` instead of chaining straight to
  the handover; user spotted it.)
- **A no-PR job (analysis / lavish+md+script deliverables / in-repo commits
  with NO merge) falls through BOTH watchers (2026-08-07).** The pane
  watcher only tracks NON-done jobs — the instant the minion runs `ledger
  set <id> done`, the job becomes done -> untracked -> the pane's
  working->done/idle transition fires NO alert; and the PR watcher has no
  PR/merge to catch. So the completion can go unseen indefinitely. The
  INTENDED durable completion signal for no-PR jobs is the briefing-
  mandated `herdr notification show "<id>" --body "..."` on finish — NOT
  ledger reconciliation, NOT the watchers. Two failure modes to
  distinguish when a no-PR completion slips: (a) NOTIFICATION-SENSOR gap
  — the minion fired the notification but Silas missed it; (b) MINION-
  COMPLIANCE gap — the minion skipped the notification step. VERIFY by
  checking the minion's session jsonl for a `cli:notification:show`
  RESULT (not just the command string in its text) — 0 results = the
  minion didn't execute it (compliance gap). (2026-08-07: righttenantry-
  gcp-cost-analysis — minion CONSTRUCTED `herdr notification show
  "gcp-cost-analysis"` but did NOT execute it [0 cli:notification:show
  results] -> compliance gap; the deliverable still reached the user via
  Gru's independent check, so no harm, but the signal was missed at the
  source.) No-PR jobs must NEVER rely on pane/PR watchers alone.
- **`ledger set <id> in-review "<url>"` does NOT populate the `pr` field
  (2026-08-07).** `set` updates only `status` + writes the note to an event
  row; the `pr` column is set ONLY by `ledger pr <id> <url>`. So a minion
  that self-reports in-review with the URL in the note leaves `pr` NULL →
  the PR watcher silently skips it. Don't confuse this with the lossy-
  table-view gotcha: VERIFY with `ledger show <id>` first (the table lies),
  and if `pr` is genuinely empty, follow the transition with `ledger pr`.
  (The packet-plumber crew now runs `ledger pr` itself — the lesson
  propagated. 2026-07-21 was the inverse false-positive: Gru wrote
  redundant `ledger pr` on a field that WAS set, read from the table.)
- **Killing a stuck / 403-dead pi: typed `exit` fails, C-c isn't uniform
  (2026-08-07).** `exit` typed into a dead pi does nothing; C-c sometimes
  leaves the TUI alive. Reliable path: `herdr pane process-info --pane <p>`
  → `kill <pid>` (the `node` pid) from bash → the pane drops to a shell;
  then verify the session-file state before relaunching. (Seen across the
  2026-08-04 quota-403 + glm dead-pane sweep.)
- **Serialize-hold for pane capacity: pre-create the round row to dedup the
  sensor (2026-08-07).** When the valve is near capacity, hold the next
  Perkins round behind an in-flight one: pre-create its ledger row (status
  `dispatched`, full sha in the note) so the Perkins sensor doesn't re-fire
  on the tick, then release when another round's close-out frees panes
  (trigger = the in-flight round's close-out). Now standard ops (≥5
  sightings 08-03..08-05) but undocumented.
- **Launching Gru with BOTH PI_GRU=1 AND PI_SILAS=1 duplicates watcher
  alerts (confirmed journaled 2026-08-01, unfiled).** Both extensions fire
  in Gru's pane → alerts echo. Recovery: relaunch Gru as
  `env -u PI_SILAS PI_GRU=1 pi` (PI_SILAS unset). Distinct from the
  cwd-gate gotcha — this is the env-var gate.
- **"Moot on merge" is NOT the default for a mid-flight Perkins round
  (2026-08-07).** A normal terminal merge of an APPROVED PR → sweep the
  in-flight round as moot, no re-dispatch. But a DELIBERATE pre-verdict
  merge (user merges to peek) → let r1 continue to verdict on the merged
  sha as an FYI review (NO rework loop unless the user says so; real
  findings become follow-up notes); a fresh post-merge AUDIT round may be
  dispatched (FYI-only, COMMENTED, no cap implication) and its blockers
  become NEW jobs, not rework of the merged PR. When unsure: sweep fast +
  re-dispatch (costs one worktree add).
- **In-repo (no-worktree) follow-up jobs: Gru's fresh dispatch = the prior
  pane is free (2026-08-07).** An in-repo follow-up needs the repo's working
  tree free, so Gru dispatching the next job IS the signal the prior pane is
  done being used → close that pane + sync the base FIRST (avoids the
  GDD→architecture working-tree conflict hit on packet-plumber). In-repo
  pane creation = `herdr tab create --cwd <repo>` (no worktree create);
  close-out closes the pane BEFORE deleting the branch (the pane shares the
  working tree).
