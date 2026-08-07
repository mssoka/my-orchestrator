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
  panes (never act on them — relays and ledger writes are Gru's). Amended
  2026-08-03: the operative control is cwd exile — non-Gru agents launch from
  their own home (Bob: `_bmad-output/bob`; see the AGENTS.md gotcha) — the
  "you are NOT Gru, ignore the startup checklist" brief line remains
  belt-and-braces (4 panes bit in one morning; each burned a turn producing
  a Gru readiness report).

- 2026-08-03 (dream-2026-08-03; RightTenantry crew — form-save-resume-f3,
  refcheck-privacy-draft + finlit-bugfix-event-messages + Gru addendum):
  multi-edit `edit` calls are ATOMIC per call — one oldText mismatch rejects
  EVERY edit in the batch (survivors lost silently; caught only by compile).
  Re-apply survivors individually; if a formatter ran between attempts
  (`gleam format` reflows split strings) re-read the file before re-issuing —
  never re-fire a stale batch. Verify multi-line oldText line-break positions
  with grep before submitting batches.
- 2026-08-03 (dream-2026-08-03; RightTenantry crew — refcheck-rc1-2,
  form-save-resume-f3, refcheck-privacy-draft): assert Lustre's SERIALIZED
  render, never view-source assumptions — attributes render SORTED BY NAME
  with empty-valued ones bare (`checked`, `required`); apostrophes come back
  as `&#39;` (houdini escape); verbatim page copy can contain your assertion
  substring (pin `checked data-testid="..."`, not a bare `checked`).
- 2026-08-03 (dream-2026-08-03; form-save-resume-f3 Perkins r2/r3): Node
  tests are blind to browser-runtime semantics — a detached
  `window.setTimeout` debounce passed every Node test (no brand-check) and
  threw `Illegal invocation` in any real browser. Timer/DOM seams get an
  empirical real-browser verification, not just suite-green.
- 2026-08-03 (dream-2026-08-03; form-stepper-f1, form-funnel-w0,
  refcheck-rc1-1/rc2-1): RightTenantry env traps generalize beyond Squirrel —
  `dot_env.load_default()` overrides the PROCESS env at runtime (to repoint a
  local dev server, replace the `server/.env` symlink with an edited
  gitignored copy); staging lags unmerged develop migrations (submissions
  500 on `submitted_ip_text`) — E2E against a local Docker DB + seeded
  vacancy, never staging.
- 2026-08-07 (dream-2026-08-07; righttenantry form-e2e-pass, form-resume-
  progress-fix, form-nojs-submit-fix, self-employed-copy-fix/-sweep — 5
  jobs, one notes "4/5 mega-minions hit the same three traps independently"):
  agent-browser's `click` silently no-ops on JS-driven controls (below-fold
  elements, emulated-mobile sticky-bar overlap, `type=button`+JS-validated
  stepper buttons) and the re-snapshot then reads STALE state. Reliable
  recipe across all sightings: `eval scrollIntoView({behavior:'instant'})` →
  `eval el.click()` (or click the `label[for=]`), then read state from the
  DOM; `fill` can't set `input[type=date]` (set `.value` + dispatch
  `input`/`change`); radios/checkboxes need `checked=true` + dispatched
  events. Also: the DEFAULT agent-browser session is SHARED machine-wide —
  a sibling minion's drive hijacks mid-scenario; always `--session <job-id>`.
- 2026-08-07 (dream-2026-08-07; righttenantry csp-posthog-allowlist,
  csp-enforce-allowlist, form-resume-progress-fix, draft-grace-period — 4
  jobs): fresh RT worktrees ship NO `node_modules` (worktree bootstrap
  copies only git-tracked files), so `make build` fails on `tailwindcss:
  command not found` — and `make test` never surfaces it (js-tests run on
  bare node). Fix by scope: `ln -s <repo_root>/node_modules node_modules`
  (gitignored, never committed), or `npm ci`, or skip with `make build-
  server` + `make test-server` for server-only work.
- 2026-08-07 (dream-2026-08-07; orchestrator-nefario-conflict-sensor — 2nd
  sighting of the parse-test-strip-types watch item): Node 22
  `--experimental-strip-types` REJECTS TS constructor parameter properties
  (`private x: T` in a ctor signature — "not supported in strip-only mode";
  declare the field explicitly + assign in the body) and can't run a file
  with non-erasable runtime enums / `const enum` (use plain `const` Sets).
  Parse-test any `.ts` extension with this flag before commit — the
  preventive practice for the in-store backtick-kills-extension gotcha.
- 2026-08-07 (dream-2026-08-07; finlit-e2-7, orchestrator-nefario-conflict-
  sensor): relative paths surprise in worktrees — relative-path edit/write
  tools + `git` resolved to the MAIN checkout, not the worktree (one `git
  commit` landed on local `main`; recovered via stash + branch move); ESM
  relative imports resolve against the SCRIPT's directory, not `cwd`.
  ALWAYS use absolute worktree paths for file tools and git, and keep
  scratch importers INSIDE the worktree.

## Conventions that saved time

- 2026-07-31/08-01 (finlit-game-brief, refcheck-v1-epics,
  tutor-economy-fix): ground-truth-first — verify mega-minion review
  findings against DISK before applying (stale session-context findings
  recur, 2 in one run); check the real enums/components in the repo before
  spec'ing against them; read the provider log before theorizing about LLM
  behavior. 2026-08-03 addendum (refcheck-rc1-2): this extends to reviewer
  MECHANISM claims — two independent hunters hallucinated
  native-browser-validation blockers from `required` attributes on a form
  that carries `novalidate` on both the GET and the error re-render. Verify
  the mechanism exists against the actual element/runtime before crediting
  the finding. 2026-08-07 addendum (dream-2026-08-07; righttenantryagents-
  model-flash, packet-plumber-setup-brief, righttenantry-csp-posthog-allowlist,
  righttenantry-agent-model-flash): this extends to the BRIEFING itself — a
  briefing's stated "current state", file paths, and rationales can be STALE
  (forensics pre-date a merged PR — PR #164 had already moved the model tier)
  or just WRONG (a security-control mechanism that disk + vendor docs
  disprove). Before trusting a briefing's premise, `grep`/`find` disk for the
  real current state and verify any stated mechanism against disk + vendor
  docs — escalate rather than improvise on a stale/wrong instruction.
- 2026-07-31/08-01 (finlit-bugfix-event-messages, tutor-economy-fix):
  root-cause-first — in PR/ledger notes, name the wrong hypothesis
  explicitly and reject it ("int truncation, NOT a 60s timer bug";
  "client word-cap, NOT max_tokens/thinking") so review rounds don't
  re-litigate it.
- 2026-07-31/08-01 (refcheck-rc2-1, form-funnel-w0, tutor-economy-fix):
  pin acceptance criteria as durable TESTS at the lowest layer (8 DB-level
  AC pins; LOAN_MODEL OPM contract pinned) — they survive review rounds,
  Perkins lenses, and refactors.
- 2026-08-07 (dream-2026-08-07; packet-plumber-architecture-v1,
  finlit-architecture-v1, finlit-gdd-amendments): on a high-stakes doc every
  downstream agent reads, a 2-hunter review swarm (adversarial-general +
  edge-case-hunter) EARNS its ~2-pane cost — it catches real contradictions
  the author is blind to (spine data-flow direction, locked-pillar
  violations, unbuildable seams, superseded-citation overclaims). Verify
  every finding against disk before applying. Budget an R2 / self-review
  pass after applying R1 — R1 fixes introduce their OWN bugs (a defective
  rounding formula written to fix R1; the GDD's own example was the
  disproof).

## Recurring review findings

- 2026-08-03 (dream-2026-08-03; form-funnel-w0, form-stepper-f1,
  form-save-resume-f3): `server/priv/static/*` is git-ignored with a
  per-file `!` whitelist — a new static asset deploys as a DEAD script tag
  while SSR pins (which only assert the tag) stay green. Caught ONLY by
  review all three times. Adding a static asset: whitelist it in
  `.gitignore` in the same PR.
- 2026-08-03 (dream-2026-08-03; form-stepper-f1 + form-save-resume-f3
  Perkins arcs): token/PII leaks recur across SEAMS, not rounds —
  X-Forwarded-Host in generated URLs one round, PostHog autocapture scraping
  the raw token from `<body>` the next. A scrub-in-one-place finding means
  audit the WHOLE token path (URL generation, DOM/analytics, headers, logs)
  in the same fix. And each round's rework can introduce the NEXT round's
  blocker (r1's E2E rework created r2's 2 blockers) — full-suite re-run +
  a regression pin per fix.
- Supabase security-definer views bypassing RLS (Perkins r1 blocker on PR
  #556, 2026-08-01) — single sighting, still watching.
- 2026-08-03 (righttenantry-refcheck-privacy-draft; lavish): a lavish
  session-end can STRAND queued-but-undelivered prompts — the user's
  verdict ('Approve — open the PR') sat in ~/.lavish-axi/state.json
  (session prompts, by uid) while the poll exited on session-end having
  delivered only the earlier rulings. Before declaring "no verdict was
  given", check state.json's session prompts as ground truth. Wake-poll
  corollary: a poll that exits on session-end may miss the final queue —
  drain-then-exit, or check state.json after exit.
- 2026-08-03 (finlit-architecture-v1 gate-drill): a typed message in a
  minion pane CAN be the user talking directly (they do that — e.g. a
  bare 'approved' at a lavish gate). Provenance still matters: an
  out-of-band verdict gets VERIFIED via Gru before acting on it (Silas'
  halt was correct protocol; the confirmation came back within the
  hour). If the user answers you directly in your pane, note it in your
  ledger self-report so the orchestrator doesn't chase a phantom.
- 2026-08-04 (finlit e2-1/e2-7 dispatch): the bare model label 'glm-5.2'
  resolves to the 'opencode' provider (no API key configured) and errors
  at launch; the FULL path 'zai-coding-cn/glm-5.2' is what worked for the
  sprint-plan minion. Use the full provider-qualified path for glm
  dispatches, or fix the routing. The error is silent on the agent_status
  (pane shows idle with the pi UI up) — read the pane's visible content
  for the 'No API key found for opencode' red text; the session jsonl
  won't exist (pi never processed a turn).
- 2026-08-07 (dream-2026-08-07; righttenantryagents-model-flash Perkins r1
  N3, righttenantry-oauth-posthog-fix Perkins r1 W1): two flavors of an
  under-locked change recur as Perkins findings — (a) COVERAGE-GAP: a
  changed component lacks the per-component assertion test its siblings
  have (3 of 5 Pro agents had no `model==X` test → the switch wasn't
  pinned); (b) GUARD-PIN NOT UNIQUE: a substring-pin guard isn't unique to
  its target adjacency → a regression isn't pinned (reset-arm guard). When
  adding/changing a component, mirror the siblings' assertion tests and
  make every guard/pin uniquely identify its target.

## glm-5.2 bare-label routing bug (2026-08-04, 2 independent sightings)

The bare model label `glm-5.2` resolves to the `opencode` provider in pi,
which has NO API key configured — panes error at launch: "No API key found
for opencode." The sprint-plan minion and the e2-1 review swarm both hit
this independently. The full provider-qualified path `zai-coding-cn/glm-5.2`
resolves correctly (sprint-plan ran fine on it). **Always use the full
`provider/model` path in briefings and dispatch commands, never the bare
label.** If a minion falls back to another model on its own (e.g. deepseek),
that's the symptom — check the pane for the opencode error.
