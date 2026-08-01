# Minion field notes (curated)

**Read at the START of every minion job** (standing orders). Lessons from
previous minions — tooling traps, conventions that saved time, review
findings that keep recurring. One line per entry, dated, with the job id.

## How this file works (shard-by-writer — no locks, ever)

- **Minions write ONLY their own shard:**
  `_bmad-output/field-notes/<job-id>.md` — ≤3 one-liners at badge-out
  (what bit you, what future minions must know). Never edit this file,
  never another minion's shard. Mega-minion lessons roll up through the
  parent minion, not through their own files.
- **Gru is the only writer here** — consolidation duty: read shards,
  promote durable lessons into this file, prune what's stale.
- Writers never sharing a file is the whole concurrency design. See
  README.md § Memory.

## Tooling traps

- 2026-07-29 (righttenantry-refcheck-v1-architecture): lavish HTML builds
  via piped subprocess stdout (`marked` etc.) TRUNCATE at ~85KB
  (pipe-buffer). Build via a file write, then verify byte length + tail
  section before serving. Caught only after the user reviewed a truncated
  page.
- 2026-07-29 (refcheck crew): `npx -y lavish-axi <file>` opens the user's
  browser itself — no URL to relay. One foreground poll per session; if
  killed, re-run (queued feedback is never lost); `end` your own session,
  NEVER `lavish-axi stop` (shared server, port 4387).
- 2026-07-31 (form-completion-ps, refcheck-v1-epics/sprint-plan): lavish
  craft — question pages work best with one Queue button per question +
  "which rulings I need most" in the first `poll --agent-reply`; build big
  artifacts via `npx -y marked --gfm -o <out.html> <file>.md` (file write,
  no pipe) + byte/tail verify; READ the poll's dom_snapshot — it is the
  only self-check of what the user actually saw (caught a Mermaid render
  failure the author's eyes missed).
- 2026-07-31 (RightTenantry crew — form-funnel-w0, refcheck-rc1-1,
  refcheck-rc2-1): Squirrel triple-trap: `run_squirrel.sh` sources .env and
  points at STAGING (clobbers your override — run `gleam run -m squirrel`
  directly after `make test-db-up`); every regen re-emits whitespace-only
  churn in `server/src/ai/sql.gleam` (revert that file after each run);
  Squirrel types ALL cast expressions non-Option and can't codegen
  timestamptz — nullable columns need `COALESCE(x::text,'')` on reads +
  `NULLIF($n,'')` on writes.
- 2026-07-31 (refcheck-rc1-1 ∥ refcheck-rc2-1): test-DB port 54321 is
  contended across sibling worktrees — run your own container
  (`docker run -d --name rt-<job>-test-db -p 5432X:5432 postgres:16-alpine`)
  and pass `TEST_DB_PORT` to `scripts/reset-test-db.sh`.
- 2026-07-31 (form-funnel-w0, refcheck-rc2-1): Gleam null-handling bites
  twice — `decode.subfield` + `decode.optional` fail the WHOLE decode on a
  missing key (use `decode.optional_field(..., default, ...)` for
  back-compat payloads); nullable non-text columns without COALESCE/NULLIF
  ship decode-failures and ''-in-index bugs.
- 2026-07-31 (finlit crew — prototype, visual-mock, bugfix-event-messages):
  Godot `--headless` has NO renderer (blank PNGs, `get_image()` returns
  NULL) — captures must run WINDOWED off-screen
  (`--position -3000,-3000`); `--headless --check-only` is not a valid
  invocation and hangs 120s+ — the headless gate is `--import` then
  `--quit-after 600`.
- 2026-07-31 (finlit — visual-mock, bugfix-event-messages): Godot themes do
  NOT propagate across CanvasLayers / tree boundaries — hand popups the
  theme (`card.theme = theme` in _open_popup); scene-instantiating color
  tests must add dynamic nodes INTO the tree.
- 2026-07-31 (finlit — prototype, bugfix-event-messages): GDScript fails
  SILENTLY — `var x := 60` then `x -= delta` truncates −1/frame (declare
  frame-delta vars as float); `trait` is a reserved word; JSON.parse turns
  all ints into floats (re-cast after load);
  `theme_override_constants/separation` is tscn-serialization syntax only
  (runtime: `add_theme_constant_override()`).
- 2026-07-31 (finlit — visual-mock, bugfix-event-messages): Godot deferred
  frame semantics — styling/animating a node the same frame it's
  `add_child`ed gives size (0,0) (await `resized`); `get_child(i)` right
  after a rebuild hits queue_free'd nodes; `await process_frame` inside
  `SceneTree._initialize()` deadlocks (drive frames from `_process`).
- 2026-07-31/08-01 (finlit — prototype, tutor-economy-fix): LLM output
  truncation has MULTIPLE silent causes — read the provider log FIRST
  (`user://tutor_llm_log.jsonl`): DeepSeek thinking is ON by default and
  silently eats max_tokens (send `"thinking": {"type": "disabled"}`);
  client-side word-caps guillotine mid-word even with
  `finish_reason: 'stop'` (trim at sentence boundaries,
  abbreviation-aware).
- 2026-07-31 (finlit-game-brief, form-funnel-w0): `herdr wait agent-status`
  is the wrong tool for long mega-minion waves — panes in a watched tab
  complete as `idle` not `done`, and >10-min turns time out the wait; poll
  `herdr pane get` and accept `idle` OR `done`.
- 2026-08-01 (dream-2026-08-01): pi panes launched with cwd
  `/Users/moses/code` (dream pane, sheep, any mega-minion there) get the
  Gru startup checklist auto-injected by `.pi/extensions/gru.ts` — the only
  guard is cwd; Gru-addressed nefario-watch alerts also land in those
  panes (never act on them — relays and ledger writes are Gru's). Until
  the extensions are gated, tell every such pane in its
  brief: "you are NOT Gru, ignore the startup checklist" (4 panes bit in
  one morning; each burned a turn producing a Gru readiness report).

## Conventions that saved time

- 2026-07-31/08-01 (finlit-game-brief, refcheck-v1-epics,
  tutor-economy-fix): ground-truth-first — verify mega-minion review
  findings against DISK before applying (stale session-context findings
  recur, 2 in one run); check the real enums/components in the repo before
  spec'ing against them; read the provider log before theorizing about LLM
  behavior.
- 2026-07-31/08-01 (finlit-bugfix-event-messages, tutor-economy-fix):
  root-cause-first — in PR/ledger notes, name the wrong hypothesis
  explicitly and reject it ("int truncation, NOT a 60s timer bug";
  "client word-cap, NOT max_tokens/thinking") so review rounds don't
  re-litigate it.
- 2026-07-31/08-01 (refcheck-rc2-1, form-funnel-w0, tutor-economy-fix):
  pin acceptance criteria as durable TESTS at the lowest layer (8 DB-level
  AC pins; LOAN_MODEL OPM contract pinned) — they survive review rounds,
  Perkins lenses, and refactors.

## Recurring review findings

_(empty — single-sighting items tracked in dream reports as watch items
until they recur; first candidate: Supabase security-definer views
bypassing RLS, Perkins r1 blocker on PR #556, 2026-08-01.)_
