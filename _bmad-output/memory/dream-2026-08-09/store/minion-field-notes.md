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
  `NULLIF($n,'')` on writes. 2026-08-08 addendum (per-applicant-remind,
  refcheck-rc2-2): regen churns BOTH `application/sql.gleam` AND
  `ai/sql.gleam`; `gleam format` is the canonical arbiter of what stays
  (it reverted a bogus pog.array hunk) — revert ALL churn not yours.
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
  `--quit-after 600`. 2026-08-08 addendum (packet-plumber-prototype-build/
  -iterate-1): `-32000` is OUTSIDE the renderable desktop (viewport never
  clears) — `-3000,-3000` stands; macOS offscreen windows FREEZE their
  compositor (captures repeat the first frame forever — diff frame hashes
  to detect); movie mode (`--write-movie --fixed-fps`, frames via ffmpeg)
  is the reliable path for anything sequence/verification-grade — windowed
  offscreen is for one-shots.
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
  with grep before submitting batches. 2026-08-09 addendum (dream-2026-08-09;
  packet-plumber crew, refcheck-rc3-2): check each oldText's TARGET FILE in
  cross-file batches (one aimed at the wrong file rejected both silently);
  after a sed/python bulk rename, grep the renamed tokens — it silently
  creates NEW stale texts (`harness//`, misaligned diagrams); for fragile
  multi-site blocks a short python script with unique-substring
  `.replace()` anchors + asserts beats the edit tool.
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
  scratch importers INSIDE the worktree. 2026-08-08 addendum
  (orchestrator-docs-ua1-ua2, orchestrator-perkins-ops-codify): a briefing
  that says "no worktree, work in the root" can still arrive AS a standard
  worktree dispatch — ground truth = your pane's cwd (`pwd` +
  `git branch --show-current` FIRST, before any git or edits; one minion
  hit `fatal: branch already used by worktree` running git against the
  main checkout).
- 2026-08-09 (dream-2026-08-09; orchestrator-docs-ua1-ua2,
  orchestrator-perkins-ops-codify, righttenantry-refcheck-rc3-2 +
  packet-plumber-setup 08-06): `gh pr create --body "$(cat <<'EOF'…)`
  keeps breaking — backticks get command-SUBSTITUTED (`node_modules:
  command not found`), a trailing `| tail` breaks the quoting, apostrophe-
  heavy bodies EOF early (a wrong test count shipped and needed a
  `gh pr edit`). Always `--body-file <file>`; grep-verify any counts the
  body claims before pushing.

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
  2026-08-09 addendum (dream-2026-08-09; 5 sightings): the claim types keep
  diversifying — proper nouns vs canon (briefing's `RTenTRY` vs canon
  `RTenantry`, committed before Gru caught it), migration state (briefing's
  "ADD VALUE skipped" was already done), CI-guard EXISTENCE (banned
  em-dashes "CI-guarded", no such guard on disk), PR/sha citations (#169
  had no r2 to fold in), MCP tool inventory (no `capture_screenshot`).
  Grep any briefing-supplied proper noun against canon BEFORE the first
  commit.
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
- 2026-08-09 (dream-2026-08-09; packet-plumber art-direction-amend,
  forge6-desktop-first-amend, port-limits-canon + righttenantry
  refcheck-ad5/-ad6 amends — 4+2+3 sightings, 2 repos): canon-doc
  AMENDMENT craft — (a) grep-bound the FULL blast radius (every occurrence
  of the reversed statement, HEADINGS/siblings of the named target,
  downstream docs citing `FORGE #<n>`) — guessed section numbers are
  always wrong and a missed heading leaves a silent internal
  contradiction; (b) MATCH the doc's own house style (its dash rule, its
  established amendment format) — grep for `—` first, don't invent a new
  register; (c) surface judgment calls + out-of-scope consequences
  explicitly (conservative resolve + one-line flag in the PR's Decisions
  & rationale) — never silently drop, silently expand scope, or silently
  leave the gap.
- 2026-08-09 (dream-2026-08-09; righttenantry-csp-posthog-allowlist 08-06
  + per-applicant-remind 08-08): prove a new test/guard actually BITES —
  negative control: flip one assertion (or inject the violation), confirm
  exactly the expected failure at your path, revert. Terse runners
  (gleeunit's dots) and no-op-via-byte-diff both pass silently otherwise.

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
  drain-then-exit, or check state.json after exit. 2026-08-09 addendum
  (dream-2026-08-09; packet-plumber-narrative-messaging,
  packet-plumber-blender-art): the exact ground-truth path is
  `~/.lavish-axi/state.json` → `sessions.<id>.chat[].text` — verify it
  BEFORE acting on any load-bearing verdict (2 more confirmations).
- 2026-08-03 (finlit-architecture-v1 gate-drill): a typed message in a
  minion pane CAN be the user talking directly (they do that — e.g. a
  bare 'approved' at a lavish gate). Provenance still matters: an
  out-of-band verdict gets VERIFIED via Gru before acting on it (Silas'
  halt was correct protocol; the confirmation came back within the
  hour). If the user answers you directly in your pane, note it in your
  ledger self-report so the orchestrator doesn't chase a phantom.
  (2nd sighting 2026-08-07, packet-plumber-sprint-plan-v1: a lavish-gate
  APPROVED arrived via direct pane chat, not Send&End — provenance
  unambiguous, acted on after the same protocol.)
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
- 2026-08-09 (dream-2026-08-09; refcheck-rc2-2 Perkins r2, refcheck-rc2-3
  Perkins r1, per-applicant-remind Perkins r1 — 3 jobs, 2 days): Perkins
  late-round blockers are increasingly PROCESS gates, not logic — a CI
  `gleam format --check` failure, a headline AC with zero test pin. Each
  burns a full review round on what a pre-push checklist catches for free:
  run the repo's CI gates LOCALLY before opening/updating the PR (format
  --check + the gate self-checks), and pin headline ACs per the
  durable-tests convention.

## glm-5.2 bare-label routing bug (2026-08-04, 2 independent sightings)

The bare model label `glm-5.2` resolves to the `opencode` provider in pi,
which has NO API key configured — panes error at launch: "No API key found
for opencode." The sprint-plan minion and the e2-1 review swarm both hit
this independently. The full provider-qualified path `zai-coding-cn/glm-5.2`
resolves correctly (sprint-plan ran fine on it). **Always use the full
`provider/model` path in briefings and dispatch commands, never the bare
label.** If a minion falls back to another model on its own (e.g. deepseek),
that's the symptom — check the pane for the opencode error.

2026-08-09 generalization (dream-2026-08-09; the kimi-coding saga, Silas
journal 08-08): the rule is bigger than glm — only a `provider/model`
path naming an AUTHED provider works. Bare `kimi-coding` fails too (it's
a PROVIDER with a key in auth.json, not a model — the model label is
`kimi-coding/k3`), and `moonshotai/kimi-k3` MISROUTES via openrouter
instead of the direct kimi-coding provider. Also: pi's defaultProvider is
now kimi-coding (settings.json), so UNSET-model dispatches resolve to
kimi-coding/k3 — know what "unset" resolves to before assuming a
dispatch's model.
