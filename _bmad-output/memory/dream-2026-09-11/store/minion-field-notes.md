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
  failure the author's eyes missed). 2026-08-27 addendum
  (dream-2026-08-27; dublin-map-beautify): the HTML at
  `.lavish/<name>.html` must reference images as `<dir>/img/...` — a
  bare `img/...` path surfaces as 8 fatal artifact-asset-unavailable
  failures IN THE POLL OUTPUT (not user feedback); read poll failures
  before interpreting user silence, repair + re-poll. 2026-08-29
  addendum (dream-2026-08-29; viscomm-regression-audit): decision
  menus = per-row RADIO forms + one Queue button each — a clean
  per-row ruling arrived as a single tagged keep-leave prompt (R1
  restore-via-A1); a Send-&-End session delivers the final feedback
  once on the next poll (no extra polling rounds after it).
  2026-09-09 addendum (dream-2026-09-09; Selva assets/rigs WIP +
  full-song-storyboard, 09-08): technical completion is not the
  viewing handoff. The finished movie was buried in technical chatter;
  the storyboard browser opened before its poll existed. For a
  requested visual handoff, verify the exact artifact and agreed
  viewing/review path, then say READY TO WATCH/REVIEW conspicuously.
  Browser-open alone does not prove active feedback monitoring; check
  the owning poll or supported wake path. Open a player only when
  requested/authorized; otherwise provide a clear usable link/path.
  Opening, watching and artistic approval are three different claims.
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
  2026-08-11 addendum (dream-2026-08-11; refcheck-rc3-4/-rc3-5): two more
  Squirrel type facets. (a) Squirrel emits its OWN `<Type>` inside each
  `<module>/sql.gleam`, mirroring the PG enum SEPARATE from `shared.*` —
  status args to the sql fns must be `sql.<Variant>` (the trigger
  module's), NOT the shared variants (type mismatch → "Expected
  sql.<Type>"). (b) When two PG enums SHARE constructor names
  (`reference_call_status` + `reference_call_outcome` both have
  `ManualRecorded`/…), Gleam forbids duplicate constructors in one module
  → pass shared-constructor enum params as STRING +
  `NULLIF($n,'')::<enum>` cast, NEVER a bare `$n::<enum>` (Squirrel emits
  the conflicting type → "Duplicate definition").
  2026-08-13 addendum (dream-2026-08-13; rc3-7 + rc4-4): regen also churns
  `application/sql.gleam` formatting hunks unrelated to new columns —
  VERIFY EACH HUNK before keeping (rc4-4 reverted one); `ai/sql.gleam`
  whitespace → revert the whole file.
- 2026-07-31 (refcheck-rc1-1 ∥ refcheck-rc2-1): test-DB port 54321 is
  contended across sibling worktrees — run your own container
  (`docker run -d --name rt-<job>-test-db -p 5432X:5432 postgres:16-alpine`)
  and pass `TEST_DB_PORT` to `scripts/reset-test-db.sh`.
  2026-08-13 addendum (rc1-1-grapheme-fix + rc4-4): the Makefile
  HARDCODES 54321; as of 08-13 sibling worktrees owned
  54321/54326/54327/54332-34 — grab a free port and pass
  `TEST_DATABASE_URL=postgresql://test:test@localhost:<port>/righttenantry_test`
  to `gleam test -- --tag integration` (after `TEST_DB_PORT=<port> bash
  scripts/reset-test-db.sh`).
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
  2026-08-13 addendum (dream-2026-08-13; 2.3-demolish): nested-code
  batches need EXACT tab depth — a 5-edit batch to a 3-level-deep switch
  was rejected silently (all 5 lost) because one oldText was indented 3
  tabs, not 4. Re-read the exact depth of nested code before authoring
  batch oldText. 2026-08-17 addendum (dream-2026-08-17;
  packet-plumber-surge-explainer + v2-5.9-demand-caps — ×2): a
  DUPLICATE oldText inside one batch fails the WHOLE batch silently —
  dedupe targets before submitting; after ANY multi-edit, re-grep every
  hunk to confirm it landed — a silent whole-batch rejection leaves the
  tree looking edited while nothing applied (5.9 debugged phantom
  behavior for a round before noticing). 2026-08-27 addendum
  (dream-2026-08-27; arch-latency-egress-queue-model): literal two-char
  `\n` sequences in target text (mermaid labels) must be `\\n` ESCAPED in
  edit oldText — a raw `\n` silently becomes a newline, the match fails,
  and the whole multi-edit call atomically no-ops (same failure shape as
  the tab-depth class).
- 2026-08-03 (dream-2026-08-03; RightTenantry crew — refcheck-rc1-2,
  form-save-resume-f3, refcheck-privacy-draft): assert Lustre's SERIALIZED
  render, never view-source assumptions — attributes render SORTED BY NAME
  with empty-valued ones bare (`checked`, `required`); apostrophes come back
  as `&#39;` (houdini escape); verbatim page copy can contain your assertion
  substring (pin `checked data-testid="..."`, not a bare `checked`).
  2026-08-13 addendum (dream-2026-08-13; rc4-2 r1 B2 + rc4-3): the SOURCE
  side mirrors it — an empty-string attribute VALUE serializes as a
  PRESENT attribute: writing `attribute("disabled", "")` ships a
  permanently-disabled button. Omit the attribute instead
  (`list.append(attrs, case busy {True -> [attribute("disabled","true")]
  False -> []})`).
- 2026-08-03 (dream-2026-08-03; form-save-resume-f3 Perkins r2/r3): Node
  tests are blind to browser-runtime semantics — a detached
  `window.setTimeout` debounce passed every Node test (no brand-check) and
  threw `Illegal invocation` in any real browser. Timer/DOM seams get an
  empirical real-browser verification, not just suite-green. 2026-08-11
  addendum (dream-2026-08-11; refcheck-rc3-4 r1→r2→r3, the "#599 r2
  lesson" — now a standing Perkins lens-guard on #21/#174/#22): a
  client-populated hidden field (e.g. `_focus_seconds`) ships in HTML but
  is NEVER populated unless page-specific JS wires a submit listener; a
  `simulate.form_body` integration test PASSES while prod stays broken
  (always 0). Fix = wire a page-specific submit seam + drive the BROWSER
  path in a node test (not the simulator) + prove it bites (neutralize →
  red). (`instanceof Node` is blind under node — use
  `Object.prototype.toString.call(o)` for a host-object guard that needs
  no browser shim.)
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
  main checkout). 2026-08-11 addendum (dream-2026-08-11;
  righttenantry-refcheck-rc3-5 + rc3-3/-rc3-4; Gru-named field-note
  candidate): the bmad tooling (`create-story`/`dev-story`) resolves the
  repo root to the CANONICAL checkout (`/Users/moses/code/<repo>`) instead
  of the worktree cwd — a worktree minion's edits to tracker/spec/SOURCE
  land in the main checkout, not its worktree (rc3-5: `sweep.gleam` + 5
  `sweep_*.sql` landed entirely in the main checkout; the worktree was
  clean). After edits, `git status` in YOUR cwd and confirm they landed
  in your worktree; commit/push/PR from the worktree only. OPS close-out:
  the main-checkout dirty files block `pull --ff-only` — recover with
  stash→pull→pop, or (when the merge brings a committed copy) revert to
  HEAD; sync a misdirected live story byte-identical into the worktree
  (`cmp`-verified) and commit from there.
  2026-08-13 addendum (dream-2026-08-13; 2.2-ecmp — 3rd sighting): the
  trap extends to the GATES — odin test/lint/harness cd'd to the main
  checkout too and passed against the WRONG tree (edits AND tests both
  misdirected). After edits, `git status` from cwd BEFORE trusting a
  green test run. 2026-08-17 addendum (dream-2026-08-17; PP
  v2-5.4-input-parity + v2-7.2-audio-juice — 4th/5th sightings): the
  briefing's `repo_root` param ACTIVELY misleads — it names the MAIN
  checkout (ledger show prints it) and reads like a work path; treat it
  as repo IDENTITY, never a working path. Pin the worktree path ONCE
  after the pwd/branch check and use it for EVERY file-tool path AND
  every bash `cd` (7.2 did the whole job at the main checkout via
  absolute paths + cds — the expensive one). Recovery: cp changed
  files byte-identical into the worktree, `cmp`-verify, rebuild + run
  the gates there, restore main.
- 2026-08-09 (dream-2026-08-09; orchestrator-docs-ua1-ua2,
  orchestrator-perkins-ops-codify, righttenantry-refcheck-rc3-2 +
  packet-plumber-setup 08-06): `gh pr create --body "$(cat <<'EOF'…)`
  keeps breaking — backticks get command-SUBSTITUTED (`node_modules:
  command not found`), a trailing `| tail` breaks the quoting, apostrophe-
  heavy bodies EOF early (a wrong test count shipped and needed a
  `gh pr edit`). Always `--body-file <file>`; grep-verify any counts the
  body claims before pushing.
- 2026-08-11 (dream-2026-08-11; righttenantryagents-boundary-gate-state-fix
  + -slot-clear — 2 jobs, Perkins-verified): ADK `ctx.state` is a per-node
  SNAPSHOT, not live — a child `output_key` write (via `run_node`) lands on
  the live `ctx.session.state` but is absent from the node's `ctx.state`
  snapshot → `ctx.state.get(child_key)` returns `None` right after
  `run_node`. The RightTenantry convention (`agent.py:263`/:396) is raw
  `ctx.session.state` for ALL cross-node gate state — when editing ADK
  Workflow gates, read child output via `ctx.session.state`, NEVER
  `ctx.state`. The InMemory `_Recorder` harness CAN'T reproduce this
  (stubs share the live dict) — build a divergent fake ctx (stale
  `State({},{})` snapshot + live `session.state` dict) and assert the gate
  reads through `ctx.session.state`. Also: `output_key` write is
  conditional (skipped on empty-chunk/schema-fail/tool-call-only) but the
  judge's `after_agent_callback` ALWAYS fires → a clean attempt can leave
  the PRIOR dirty review in the slot while stamping clean; the per-attempt
  slot `pop` is necessary hygiene, not paranoia.
- 2026-08-11 (dream-2026-08-11; packet-plumber-v2-1.2-window-draw-pipe +
  -1.3-packet-flow — 2 stories): T2 pixel goldens need the rlsw SOFTWARE
  renderer via `tools/harness.sh` — `odin run harness` links the stock GPU
  `vendor:raylib` and renders a SOLID BLACK frame headless (no GPU context)
  — the raylib analog of the 2026-07-31 Godot headless trap. Headless
  capture path: `rl.InitWindow` + `LoadImageFromScreen` (no display); port
  the prototype's `goldens.odin` (flip + BGRA→RGBA swizzle) verbatim. The
  SW raylib build (`tools/build_raylib_sw.sh`) takes ~40s + a github clone
  — kick it off in the BACKGROUND before coding.
  2026-08-13 addendum (dream-2026-08-13; 4.2-surge-crisis + 2.2-ecmp +
  harness-ecmp-demo — 3 jobs): build the harness ONLY via
  `tools/harness.sh` — a bare `odin build harness` links the stock GPU
  raylib and produces R/B-SWAPPED golden frames (921600/921600 pixel
  diffs that look like a render bug, aren't); rlsw is GITIGNORED → ABSENT
  in a fresh worktree → point the build at the main checkout's shadow
  (`ODIN_ROOT=<main>/tools/raylib-sw/shadow odin build harness
  -out:bin/harness`). Odin `fmt.tprintf` uses the TEMP allocator —
  in-loop strings that must outlive the tick iteration need
  `fmt.aprintf` (T2 failure strings were blank garbage the first time
  that path ran), and JSON literals need `{{`/`}}`.
  2026-08-15 addendum (dream-2026-08-15; 5.3-pause-ux + silas 08-14
  chip-placement — ×2): app-layer UI (overlays, HUD chips) is INVISIBLE
  to T2 goldens (captures are world+forecast+health+banner only) — zero
  golden-shift does NOT verify an overlay change; the app's own frame
  needs a scratch replica (ODIN_ROOT=<main>/tools/raylib-sw/shadow +
  LoadImageFromScreen) + a PROGRAMMATIC pixel-scan (PIL) for overlap
  truth — vision models misjudge absolute coordinates; never eyeball a
  collision claim.
  2026-08-21 addendum (dream-2026-08-21; packet-plumber-ue-slice-1
  Perkins r1/r2): EVIDENCE-grade screenshots are claims, not truth — a
  vision read described a 'mid-traversal' frame whose pixels contained
  ZERO dot color (a vision hallucination trusted by the minion = the
  r1 'fabricated evidence' blocker); durable rule: pixel-scan rendered
  evidence (4 positions × 12 frames) + a COMMITTED mechanical geometry
  gate with a NEGATIVE CONTROL (verify-capture-geometry.py — the old
  frame fails it by 37px, re-captured frames pass). Never re-bless
  evidence on a vision claim alone.
  2026-08-19 addendum (dream-2026-08-19; v2-7.1-visual-juice +
  v2-5.11-terminal-types — ×2): REBUILD `bin/harness` (and any local
  binary) BEFORE bless and AFTER any rebase — a stale build silently
  blesses OLD code (7.1: CI caught a color-only stale bless; 5.11: a
  pre-rebase harness had no map.odin → background-less frames; rebuilt
  + amended with force-with-lease). New mechanical proofs: `cmp -l`
  every `.log.bin` vs HEAD expecting ONLY the version-field bytes
  (5.10: exactly 8 bytes @ 18..25); `harness fold-check
  <prev-catalog-hash> <prev-tick1>` proves a fold-only shift
  (qos-default-standard).
  2026-08-23 addendum (dream-2026-08-23; look-polish + spawn-feel +
  font-overhaul + noc-readability-2 — ×4): new dual-render facets —
  (a) LINE primitives render alpha as OPAQUE in rlsw (fills only — a
  translucent effect must be fill geometry, never
  DrawCircleLines/DrawLineEx; ×2: look-polish + spawn-feel); (b)
  hand-built fans/quads must wind CCW in screen space (rlgl backface
  culling, front = CCW — renders NOTHING in BOTH renderers
  otherwise); (c) SW-build app traps: macOS PLATFORM_MEMORY GetTime()
  returns 0 → a SetTargetFPS busy-wait spins FOREVER in EndDrawing
  (skip the limiter in SW builds); the raylib-sw shadow has NO raudio
  (gate app audio behind `when #config(PP_SW_AUDIO,false)`); (d) the
  GPU app path lies TWICE — the compositor freezes the GL front
  buffer for occluded windows (TakeScreenshot repeats frames) AND
  RenderTexture readbacks carry glyph-coverage alpha + atlas-RGB
  leak — the SW framebuffer (LoadImageFromScreen + flip + r/b
  swizzle) is the ONLY reliable capture; (e) harness debug verbs: the
  ms arg needs the suffix (`overlay-check surge 3000ms`, not `3000`)
  and overlay captures must set the same view flags as the app
  (`view_set_rail(true)`) or the capture misrepresents it (×2).
  2026-08-29 addendum (dream-2026-08-29; mechanics-the-box + its
  r3/r4/r5 rounds — the trap RECURRED 08-28 despite this entry): the
  SILENT flavor — NEVER bless T2 goldens with `odin run harness`
  directly: the direct build links stock vendor:raylib whose
  readback is R/B-SWAPPED (BGRA); the frames RENDER, the T2 compare
  is self-consistent, the suite goes GREEN, and only a blob-level
  census exposes every frame swapped. Symptoms: palcheck raster
  legs fail with 0 px of EVERY canon hex; 'stale' goldens that
  re-bless to byte-identical wrong frames; a black frame where the
  reference is warm. T1/fold-check stay valid (sim hashes are
  render-independent) — exactly why the T1-only sweep misses it.
  Bless + verify T2 ONLY via tools/harness.sh (rlsw shadow,
  warm-correct RGBA). Cross-machine blessing SPLITS a corpus (two
  machines, swapped conventions: census 116/117 vs 1 warm) — after
  ANY cross-machine merge, re-bless the ENTIRE corpus from ONE
  machine and run the full T2 loop TWICE; a 'one-machine settle'
  claim is verified against the MERGED TREE's warm bytes (a minion
  machine agreeing with itself absorbs zero). T2/palcheck are
  ENVIRONMENT-BOUND on a given machine: before chasing a raster
  regression, re-bless the BASE in a scratch worktree — if base
  reproduces the fail (03dd6f8 re-blessed = the 61-fail exactly),
  it's the render environment, not the diff; disclose and let the
  human/CI rule the golden source of truth.
- 2026-08-11 (dream-2026-08-11; packet-plumber-v2-1.3-packet-flow +
  -1.1-walking-skeleton — 2 stories): the PP-v2 determinism spine — the
  replay gate re-creates run-setup (fixture) but NOT flow demand by
  default; flow demand is run-setup (NOT in the action log), so any new
  run-setup added to the sim (spawn intents, director plans) must be
  threaded through `replay_hashes` in BOTH the live (`lower_spawns`) and
  replay paths, or ODN-11 replay diverges at tick 1. (The spine's `step`
  is a heartbeat — one owned-RNG draw/tick folded into a `tick_nonce`
  state field — tying the RNG into the step path so replay-equality is
  non-vacuous.)
- 2026-08-13 (dream-2026-08-13; PP v2 golden discipline — 1.4/2.1/2.2/
  3.2/3.5/4.1, ×6 sightings): (a) catalog edits are GOLDEN-POISONED —
  `cat.hash` folds every catalog byte, so any balance.json/node_type
  change re-blesses ALL `.t1`/`.log.bin` — wire new rules as core consts
  until a legitimate re-bless; (b) T1-dump additions must be
  ABSENT-WHEN-EMPTY (a zero count still shifts every default-run hash);
  (c) a re-bless is deliberate + PROVEN or it's a Perkins finding —
  byte-verify every `.log.bin` differs ONLY in the version field, splice
  the OLD catalog_hash into the new state dump (fnv must equal the
  blessed tick-1 golden), cause-document every shift; (d) prefer DERIVED
  state (bundles, routing tables) over serialized — derived state keeps
  all goldens byte-valid.
- 2026-08-13 (dream-2026-08-13; PP sim-truth traps — 3.4-sla + 4.2-surge,
  ×3 sightings): (a) `record_run` clears `state.events` EVERY TICK (ODN-14
  drain) — an end-of-run event scan is vacuous; collect the stream while
  stepping; (b) breach RATIOS are not monotone — later deliveries dilute
  the ratio below tolerance, so transition-style exits fire falsely:
  latches must be sticky-Enter by contract ("monotone" applies to the
  counter, never the ratio); (c) carry ADMISSION-TIME truth in events
  (the shed bundle) + resolve hysteresis, or trigger/resolve pairs
  chatter every few ticks on marginal networks.
- 2026-08-13 (dream-2026-08-13; rc4-3 + rc4-4 + the rc4-3 r1–r5 B1 saga —
  ×2 jobs): when a one-cycle correction/retry loop exists, the
  CORRECTION INSTANT segments everything downstream — reset the attempt
  counter + capability token on re-queue (a corrected row at count 1
  dead-ends the co-nudge step forever), gate post-loop failures on
  `corrected_at` (stale/redelivered pre-correction events must stand
  down, never fabricate a fraud signal), and segment send batches by the
  corrected_at boundary (batch index alone mislabels the re-invite as
  "Reminder N").
- 2026-08-13 (dream-2026-08-13; rc1-1-grapheme-fix, rc3-7, rc4-4 — ×3
  flavors): DB-stored text ≠ app text — (a) Gleam `string.slice` counts
  GRAPHEMES, Postgres `length()` counts CODEPOINTS → codepoint-bounded
  slicing is the only cut that satisfies a DB CHECK for multi-codepoint
  headers (ZWJ emoji: 1 grapheme = 7 codepoints); (b) `jsonb::text` adds
  a space after `:` → substring-contains on STORED fraud_signals fails —
  parse + decode the field (unit tests pass because they check gleam's
  compact `json.to_string` output; integration reads Postgres); (c) the
  timestamp space-vs-T mix (see Recurring review findings) — pin with
  server-real fixtures.
- 2026-08-13 (dream-2026-08-13; rc4-2, rc4-3, rc4-4 — ×3 jobs):
  Gleam/Lustre trap cluster — (a) an EMPTY-STRING attribute value is a
  PRESENT boolean attribute (`attribute("disabled", "")` ships
  permanently-disabled buttons — omit when enabled); (b) gleam 1.15.1
  REJECTS `++ [list-literal]` ("operator has no value on its right
  side") — use `list.append`/spread; (c) `list.all([])` is vacuously
  True — check emptiness BEFORE the all-terminal branch; (d) a
  case-clause body starting with `let` is a parse error unless braced;
  no function calls in clause guards; no list `..` spread in this Gleam
  version; (e) `decode.optional_field` is the `use`-callback 4-arg form
  (the field decoder is Decoder(t) of the DEFAULT's type).
- 2026-08-17 (dream-2026-08-17; PP v2-5.4-input-parity,
  v2-5.5-demolish-input, local-ci-suite — ×3): gate-harness FALSE
  GREENS — (a) derive gate counts from the list length
  (`${#GATES[@]}`), never a literal: the 9th local-CI gate was
  UNREACHABLE for a full review round while run_gates capped at 8;
  (b) missing-binary/bad-arg paths must exit nonzero under `!`
  negation (a 127→`!`→0 false-green on the r3-N7 bad-arg leg — guard
  with `[ -x ]`); (c) success is asserted on the produced ARTIFACT,
  never just the rc (pinned odin EXITS 0 on a failed windows
  cross-link); (d) Dockerfile RUN steps default to /bin/sh (dash) —
  `set -o pipefail` fails hard; bash 3.2 needs the
  `"${arr[@]+"${arr[@]}"}"` empty-array guard.
- 2026-08-17 (dream-2026-08-17; packet-plumber-traffic-model-design +
  righttenantry-refcheck-621-reminder-hint — ×2): briefing source
  material / test suites can live UNTRACKED in the main checkout or on
  a SIBLING branch (the reference_checks bughunt scenario suite lives
  on `origin/rt-refcheck-bughunt2`, NOT develop) — check there before
  concluding they're missing; copy in untracked, don't commit.
- 2026-08-18/19 (dream-2026-08-19; packet-plumber-background-maps,
  v2-5.12-aggregation-groups, wire-aesthetics — 3 jobs): Odin lifetime
  traps — the TEMP ARENA frees wholesale: never per-slice `delete` an
  arena value (aborts); a `defer` inside an `if` runs at the
  IF-BLOCK's end, not the proc's — a silent use-after-free that PASSES
  tests (freed memory not yet reused); `delete()` on a string LITERAL
  aborts — clone first.
  2026-08-19/21 addendum (dream-2026-08-21; wire-aesthetics badge-out
  backfill + 6.2-advance-trigger): unused multi-return `X, t, ok := f()`
  compiles clean (don't chase it as an error); indexing a CONSTANT needs
  a local copy ('Cannot index a constant'); `#partial switch` for
  unhandled enum cases; `inc[:]` to pass a dynamic as slice. And a
  temp-allocated path held across `replay_hashes`' per-tick `free_all`
  read garbage → `accepted=false` → a VACUOUS 'rejected (OK)' — re-log
  at the site after frees; treat any 'rejected (OK)' verdict as suspect
  until re-derived.
- 2026-08-19 (dream-2026-08-19; v2-5.11-terminal-types +
  v2-6.1-era-definition — 2 jobs, 3 facets): serialized STATE is a
  contract surface — layout/order changes are API changes. Append new
  catalog entries at the END (node_types.json array order is
  T1-visible); load new cross-ref catalogs LAST (load order is
  test-contract); log headers must carry the RUN-SETUP (start) era or
  replay validates against the wrong era and latches replay_error.
- 2026-08-18/19 (dream-2026-08-19; v2-5.10-narrow-access +
  v2-qos-default-standard — ×2): changing a default or catalog value
  is NEVER one-line — budget the ripple. A tier bump re-times every
  dependent test (scratch-instrument, print, re-pin — never guess);
  grep for setups relying on the OLD default (stale lane-only tests
  sat green at E7-floor rates, testing the wrong premise).
- 2026-08-21 (dream-2026-08-21; packet-plumber-v2-6.3-upgrade-lifecycle +
  6.2-advance-trigger — 2 jobs): PP fixture traps — (a) MIRROR-FIXTURE
  rule: a new struct field must land in EVERY fixture builder that
  constructs the struct (test_catalog's `make_era_row` lacked the decay
  factor → default 0 → silently zeroed every era-1+ pipe's capacity;
  the whole suite collapsed) — grep every constructor site when adding
  a field; (b) a global mechanics change (era-3 decay) silently shifts
  TUNED fixtures into marginal regimes (attribution chatter) — re-stage
  engine-mechanic tests on the tier that preserves their staging; at
  era 3 STANDARD is legacy too; (c) `harness input-parity save` is a
  SEPARATE verb from `harness save <demo>` — a catalog_hash fold
  re-bless that skips it fails gate 10 on 'catalog drift' (enumerate
  the save verbs before any re-bless).
- 2026-09-01 (dream-2026-09-02; pp-funfix-118-124 + pp-playtest-fun
  — the fun-test loop): PP demo-authoring + evidence craft.
  (a) PRs ALWAYS `gh pr create --base v2` — the repo default is main
  = permanently DIRTY vs the wrong lane (#125, recovered via `gh pr
  edit --base v2`; no rebase when the branch descends from
  origin/v2); never assume the remote HEAD default. (b) Unblessed
  demos FAIL `harness run` (no-manifest T1) — `harness save` in a
  sandbox copy (`rsync -a --exclude .git --exclude _bmad`, ~300 MB,
  carries the gitignored rlsw shadow) blesses AND still writes the
  `--stats-out` stream even for failing runs; save-then-run is the
  only path that also replay-verifies your evidence. (c) replay_error
  latches with NO reason named (#123) — bisect: router ports FIRST
  (4/router; spine links count — a 3-router spine for 13 nodes needs
  14 ports), then spans (`span_between` = integer-Euclidean isqrt
  half-up; ACTIVE tiers 14 standard / 16 mid / 18 wide), and NEVER
  `sed`-renumber spawn ids (dangling draw endpoints — rewrite the
  whole demo). (d) The v3 stats CSV has NO lifecycle events (breach
  latches, grace chips, Run_Won invisible — a win with 1801/1801
  SLA-flagged ticks LOOKS like a breach that should have drained):
  ground truth = blessed HUD capture PNGs read inline (glm-5.3-flash
  native vision), never stats math alone.
- 2026-09-01 (dream-2026-09-02; gru-journal video lane + the pi
  lens-turn sibling): a tool/bridge CALL timeout ≠ job failure —
  long server-side jobs (Cycles renders, generations, batch runs)
  finish anyway; CHECK THE OUTPUT ARTIFACT before retrying or
  declaring failure (bridge-timeout Cycles renders landed
  server-side; pi lens turns that hit 500s still wrote findings to
  disk). 2026-09-09 addendum (dream-2026-09-09; Selva assets/rigs
  09-07 + blender-sculpt 08-23): existence is NOT completion — a
  partial render or stale file can survive a failed producer. Bind
  outputs to the attempt/source receipt, verify freshness, expected
  completeness and producer result plus the job's semantic gates
  before publishing. Preserve partials as diagnostics; never splice
  timed-out attempts into a claimed complete proof. Check whether
  the producer is still running before retrying.
- 2026-08-20 (dream-2026-08-21; packet-plumber-ue-bootstrap + -slice-1 —
  the UE repo cluster): ue-mcp bridge ops — `ue-mcp init` is pty-only:
  deploy via the package's `dist/deploy-cli.js` then REBUILD (a stale
  editor shows 'Incompatible or missing module'); the bridge port.json
  goes STALE on editor restarts — rewrite it from
  `Saved/UE_MCP_Bridge/instances/<pid>.json`; kill old editors by pid
  (pkill misses them); stale `Binaries/Mac/*.dylib` pile up and the
  editor loads the HIGHEST version — a full wipe+relink produces an
  INCOMPATIBLE stamp, so keep at least one old dylib. The editor
  rewrites DefaultEngine.ini on every boot (AndroidFileServer section)
  — disable the plugin, don't fight the file. `npx -y ue-mcp <uproject>`
  boots engine-free (27 tools); a repo-root `.mcp.json` (stdio) is the
  pi wiring that works.
- 2026-08-21 (dream-2026-08-21; packet-plumber-ue-slice-1 — Perkins
  r1/r2 blockers live here): UE widget lifecycle traps — each fails
  SILENTLY: build a C++-only UUserWidget tree in `RebuildWidget()`
  (NativeConstruct runs after the Slate widget exists — RootWidget set
  there renders nothing); the UMG canvas is DPI-SCALED — the widget
  geometry (e.g. 1896x1081) is the layout truth, NOT the game viewport
  (1280x730); pre-create widget pools in a layout pass (runtime
  AddChildToCanvas in NativeTick never paints; every ClearWorld pairs
  with a pool rebuild); `FSlateRoundedBoxBrush` ImageSize defaults to
  ZERO (set it explicitly or the brush is invisible); Enhanced Input
  runtime actions are created in the CONTROLLER CONSTRUCTOR
  (SetupInputComponent runs before BeginPlay — constructing them
  elsewhere = dead mouse input, the r1 blocker); test-module headers
  live in `Public/` with the API macro; qualify `PP::FIntPoint` in
  engine-side files.
- 2026-08-20 (dream-2026-08-21; packet-plumber-ue-bootstrap):
  engine-free verification spine — prove a port BYTE-EXACT against
  reference vectors BEFORE the engine exists (engine-header-free
  headers + a standalone test main: spine_check.cpp vs the Odin
  vectors); engine-gated CI gates SKIP-with-reason, never false-green,
  with a NAMED LIFT-CONDITION (the r1 exemption lifted at r2 when
  UE 5.8.1 turned out INSTALLED — real gates ran, 7/7 + the first
  engine-golden 3-way). Missing heavyweight dependency ≠ blocked
  verification: isolate the logic, verify what's verifiable, name
  what isn't.
- 2026-08-21 (dream-2026-08-21; orchestrator-night-watchman +
  -hardening — 2 jobs): bmad-build (6.11.0, fresh from the 08-20
  upstream update 585166c) render FAILED on that install — `ambiguous
  config token implementation_artifacts` (modules.bmm + modules.gds
  both define it; the skill's step files consume
  `{{.implementation_artifacts}}`). No in-repo fix existed then (config.toml
  is installer-managed; a custom override still leaves 2 matches).
  Sanctioned path (Silas ruling 08-21 06:10Z): skill WAIVED —
  self-contained briefing + the waiver carried as a canon note in the
  PR body; avoid naming bmad-build in briefings until upstream
  dedupes the token. 2026-08-22/23 addendum (dream-2026-08-23 — ×4
  more jobs): SECOND root cause in the PP repo — `_bmad/scripts/` has
  NO render_skill.py (only memlog.py/resolve_*.py); same waiver path
  (pace-tuning, motion-readability, camera-zoom, noc-player-toggle).
  estate-spawning proved it transiently FIXABLE in place (temp
  disambiguated the bmm/gds dup keys, config restored byte-equal) —
  the waiver remained the standing path at that time.
  2026-09-09 supersede (dream-2026-09-09; Selva assets/rigs +
  my-orchestrator-bmad-build-config-unblock-pp3d, 09-07): the local
  equivalent-config ambiguity waiver is RETIRED by the installed
  v6.12.0 repair (PR #23); Selva rendered successfully and PP3D
  independently resumed the rendered workflow with 14/14 output
  hashes verified. The patch accepts duplicate keys ONLY when all
  resolve identically; conflicts/missing config still HALT. Follow
  docs/playbook-annex.md's mixed-module patch entry and
  docs/bmad-renderer-short-config-patch.md (hash-gated check after
  updates). A missing renderer in another checkout is a DISTINCT
  failure, not proof this repair applies there. Check the current
  dispatched worktree under the skill's invocation contract; do not
  inherit a historical waiver by assumption.
  2026-09-10/11 addendum (dream-2026-09-11; ≥4 jobs ×3 days): the
  `ambiguous implementation_artifacts` HALT class PERSISTS past the
  6.12 repair — it is CROSS-MODULE (implementation_artifacts defined
  in BOTH modules.bmm and modules.gds; the 6.12 duplicate-key repair
  did not cover it). The launcher exits 1 / HALTs (planet-life-
  router-legibility ×3 halts incl. a renderer attempt that 'failed
  before launch'; gemini-storyboard-skill — 'User live-pilot approval
  is recorded but does not bypass this gate'; main-suite-red-fix
  touched-then-restored during qualified-token binding; test-parse-
  hotfix), and the skill forbids source fallback, so minions halt and
  wait. Sanctioned recovery (proven ≥2 jobs: gemini-storyboard
  internal unblock, test-parse-hotfix 'gate passed via job-local
  qualified-token binding'): snapshot the installed skill into a
  job-local copy, qualify ONLY the two shorthand tokens to full
  `{{config.modules.bmm.*}}` names, prove reverse byte-equality, run
  ONE corrected official renderer bootstrap — canonical/shared config
  untouched, no raw fallback. Root fix owed at the orchestrator root
  config (dream-2026-09-11 dispatch recommendation).
- 2026-08-20 (dream-2026-08-21; righttenantry mobile-form-hunt +
  mobile-layout-1 — 2 jobs): front-end/env traps — (a) debug flex/CSS
  geometry by walking the ANCESTOR chain in the DOM, never by reading
  classes (a `min-w-0` on the rail did nothing while its wrapper was a
  content-sized flex item of an `items-center` column — the fix needed
  BOTH); `shrink-0` on pills/stops is the root-cause fix for rail
  truncation (`text-overflow: ellipsis` permanently clips mid-word);
  (b) agent-browser `eval` returns array-wrapped DOUBLE-encoded JSON
  (`["<json-string>"]` — parse in a loop, not one json.loads);
  `set viewport W H 3` gives DPR3; (c) fresh RT worktrees bootstrap
  only the ROOT `.env` — `server/.env` must be recreated or the server
  panics 'DATABASE_URL not set' (and `dot_env.load_default()`
  overrides process env, so env vars alone can't redirect it).
- 2026-08-23 (dream-2026-08-23; blender-sculpt + playbook-diet — 2 jobs):
  a pipe/script wrapper silently no-ops — `blender -b -P … | grep`
  masked the exit code AND the traceback (two "determinism-proof"
  runs had crashed on a bad API call while `cmp` compared STALE
  files) — capture rc UN-PIPED, then prove output FRESHNESS
  (mtimes/expected new values) before believing a byte-compare;
  scripted rewrites corrupt invisibly (a `tr '\n' ' '` inside a
  rewritten heredoc became a literal newline; heredoc + triple-quoted
  Python with embedded quotes self-terminates) — byte-check the
  generated artifact (grep the exact token) or use exact-match edit
  tools. Sibling of the AGENTS.md herdr no-pipes rule — the class is
  ANY wrapper, not just herdr.
- 2026-08-23 (dream-2026-08-23; noc-player-toggle + dream-2026-08-21
  Bob — ×2): edit-tool batches are ATOMIC — one bad oldText rejects
  every edit in the batch. Special chars are the silent killers: an
  em-dash in oldText failed a WHOLE batch while the block was
  verifiably present; store-copy anchors WRAP differently than the
  in-context rendering. Grep the exact anchor bytes in the TARGET file
  before authoring the batch (watch for phantom leading spaces on
  wrapped lines), use minimal ASCII-only anchors, and use a scripted
  replace for punctuation-heavy regions.

- 2026-08-25 (packet-plumber-v2-viscomm-crisis-duck + tie-deconflict;
  dream-2026-08-27): the masked-rc trap bit THREE times in one job —
  `odin build ... | head` and `2>/dev/null` both hide build failures and
  re-run a STALE bin/harness (once "confirming" a mutation leg that
  hadn't compiled, once "passing" palcheck). The captured rc must bind
  the BUILD's rc, not the pipe's; REBUILD before trusting any binary
  run; a deliberate-fail probe is the cheap proof that the harness
  actually executes the new test before trusting a green run.
- 2026-08-24/25 (packet-plumber-v2-dublin-map-beautify + gauge-telegraph;
  dream-2026-08-27, 2 shards consolidated): Odin proc literals do NOT
  capture enclosing scope/locals (palcheck render/count closures ×2;
  seg-grid builder ×1) — write file-level helper procs with EXPLICIT
  params (pass struct pointers), never inline `proc` values over
  loop/config locals.
- 2026-08-24..26 (packet-plumber v2 crew — node-legibility,
  dublin-spawn-director, arch-egress-migration, tie-deconflict;
  dream-2026-08-27): Odin fmt/syntax micro-traps, the silent ones are
  the killers — literal `{`/`}` in format strings need `{{`/`}}` (a
  stray single `}` renders literally, breaking emitted JSON silently);
  NO `%-3d` left-justify flags (renders value×100 garbage silently —
  plain `%d` only); `geom += str` is illegal (use an appendf helper
  with `fmt.aprintf`); NO `var x T` (use `x: T`); `for p in [4][2]i32{...}`
  array LITERALS need a named var first (for-in over array literals is
  still a syntax error); `import` keyword mandatory per import line;
  NO `#error` directive — the compile-time assert idiom is `when <bad>
  { BROKEN :: 1 / 0 }` (constant division by zero, proven by a
  mutation leg); `odin test app` runs ONLY the app package's tests —
  render pins live under `odin test app/render`.
- 2026-08-26 (packet-plumber-v2-arch-egress-migration; dream-2026-08-27,
  2 incidents on record): EVERY new step()-touched dynamic array must be
  added to spawn_fx.odin's shadow_clone clone list AND its flow_init
  mirror (capacity-1) — the shadow silently aliases the LIVE run's
  pointers and the abort surfaces FAR AWAY at run_destroy
  (malloc_error_break backtrace finds it; the tx-ring comment in the
  same proc is the prior incident). Grep the clone list whenever a
  step()-touched dynamic array is added.
  2026-08-29 addendum (dream-2026-08-29; box-crash-third-spawn +
  lang-safety-research — the class RECURRED on the #107 Box arrays):
  the rule grows a PIN-LINE half — every new Run_State dynamic array
  adds a clone line AND a pin line in
  test_spawn_fx_shadow_clone_box_owns_every_array: the box-ON
  fixture + raw_data pointer pins make a missed field CI-visible
  (box-OFF fixtures hide it — nil headers delete harmlessly; skip
  only raw_data==nil in the pin, len==0 hides allocated backings).
  Odin dynamic arrays carry their ALLOCATOR in the header — a missed
  clone field alias-frees the LIVE buffers silently (the 3rd-spawn
  SIGABRT: destroy freed them, topology.gen re-predict freed them
  AGAIN). Forensics that work: grep the repro surface for by-value
  dynamic-array/struct copies feeding a destroy (`clone := src^` +
  `run_destroy(&shadow)` was the whole bug); `odin test` beats
  libmalloc for localizing (bad free @ file:line call sites) — but
  its bad frees are REPORTED not fatal and temp_allocator frees are
  leak-invisible, so a mutation gate pins OWNERSHIP directly
  (pointer compares), never allocator abort/leak behavior; a macOS
  .ips loses the stack above _heap_free — a -debug build + lldb
  `breakpoint set -n malloc_error_break` recovers the full Odin
  stack in one run; core:mem Tracking_Allocator's bad_free_callback
  (file:line) catches the class DETERMINISTICALLY. READ-ONLY repro
  recipe: rsync the repo to /tmp (exclude _bmad) + an env-gated
  frame-script driver in app/main.odin copying the PP_NOC_E2E
  pattern (append Device_Events after polls, before dispatch_frame)
  — drove real drag-connects, caught the crash RED, proved the fix
  GREEN (8 connects).
- 2026-08-28 (packet-plumber-v2-mechanics-the-box +
  -look-zoom-language — 2 jobs): Odin/harness semantic traps. (a) a
  `case:` in a `#partial switch` swallows EVERYTHING after it — a
  case inserted below the default silently never runs (a demolish
  refund priced zero and tests mostly passed): keep special cases
  ABOVE the default; grep `case:` adjacency in review. (b) never
  price a charge/refund from POST-apply topology —
  pipe_slot/node_slot SKIP DEAD entities and fall back to slot 0
  (tombstone-then-price refunds the wrong tier/span or nothing):
  validate snapshots the pre-edit facts into a small struct, price
  from the snapshot; a refund test demolishing id 0 MASKS the bug
  (slot 0 = the accidental right answer) — always demolish a
  NON-ZERO id. (c) the demo-directive zero-value trap: a numeric
  Demo field with '1.0 = default' semantics still zero-inits (zoom 0
  → scale = fit*0 → the map grid loop drew ~forever, a 2.5h silent
  'suite run') — normalize absent-directive numerics AT PARSE TAIL +
  belt the run site; a hung `harness run` with an EMPTY log = sample
  the process, look for an unbounded render loop. (d) needle/patch
  craft: `replace1`'s 4th arg is a COUNT not an occurrence index;
  retuning a fixture value silently no-ops old needles (verify each
  row still fails-for-the-right-reason); loader messages carry
  EM-DASHES (a hyphen want-substring fails contains() — copy
  want-strings from the loader source); field alignment differs per
  helper (a copied-alignment needle matches a DIFFERENT helper's
  block — a patch that 'applies' but greps empty no-oped; verify by
  grepping the INSERTED comment).
- 2026-09-04 (dream-2026-09-04; packet-plumber-3d e1/e2/asset-scout —
  the Godot 4.7.1 lane opens): editor surface is its OWN failure
  class, orthogonal to game-run — off-screen editor windows (macOS
  -3000) freeze to a 2x2 viewport texture (capture
  EditorInterface.get_editor_viewport_3d(0) instead, and reposition
  the editor camera: its default pose sits INSIDE a radius-8
  planet); non-@tool scripts on scene nodes are PLACEHOLDER instances
  in the editor; `look_at_from_position` takes GLOBAL coords and
  aim-at-X must place the camera on X's SIDE, not the antipode —
  ALWAYS verify pose changes with a SCREENSHOT, not transform
  asserts. SceneTree `-s` suites: nodes added during _initialize
  aren't in the tree yet (run on first process_frame; never .free()
  RefCounted; null-guard every load() or a pre-quit crash hangs the
  engine forever); GDScript has no %e and `var x := get_setting()`
  (INFERENCE_ON_VARIANT) errors by default; @warning_ignore honors
  STATEMENT level only; icosphere Kahler tables are CW = back-facing
  in Godot. Fresh clones need `godot --headless --import` FIRST or
  classes are missing. Bursty packet admission needs persistent
  deficit CREDIT (banked reserve) or big packets starve on per-tick
  allowances.
- 2026-09-04 (dream-2026-09-04; asset-scout): keywalled-API scouting
  fallbacks — Poly Pizza embeds full search JSON in
  window.__SERVER_APP_STATE__ with GLBs at static.poly.pizza/<uuid>.glb
  (search-page JSON + curl = a complete free API; tri counts via
  HTTP-range fetch of the GLB JSON chunk); Sketchfab's public model
  API returns thumbnails at thumbnails.images[].url (NOT .urls).
  Authoring scales LIE (0.08x–25x) — normalize by MEASURED world bbox
  (glTF accessor min/max × node-transform walk) and carry the factor
  in a PP3D_NormalizedScale root node.
- 2026-09-04 (dream-2026-09-04; gdd-v1 + rta-prod-scale-to-zero): the
  ledger transition order is `bin/ledger pr <id> <url>` FIRST, then
  `set in-review` — the guard refuses the reverse (loud, no harm,
  guaranteed re-run); both crews hit it the same day.
- 2026-09-04 (dream-2026-09-04; gdd-v1): pi's `edit` tool is ATOMIC
  across the whole edits[] array — one failed oldText silently
  rolls back ALL edits in the call (a 4-edit apply lost 3 of 4;
  caught by re-grep). Re-grep after every multi-edit apply; keep
  oldText minimal so a miss is diagnosable.
- 2026-09-07 (dream-2026-09-07; gdd-amend-alive-planet +
  gdd-amend-cumulative, "×3 now"): `gh pr create --body "$(cat
  <<'EOF' …)"` dies on quoting with apostrophe/backtick-rich
  markdown even when carefully quoted — write the body to a temp
  file and pass `--body-file` on the FIRST attempt, not the second.
- 2026-09-07 (dream-2026-09-07; l1-topology-font + scene-refactor):
  the godot MCP LSP is NOT ground truth — it serves the MAIN
  checkout root (worktree files analyze as outsiders: phantom
  "hides a global script class" / "not declared" for NEW classes)
  and holds the PRE-MOVE class cache after refactors (140 phantom
  diagnostics citing old paths; res:// existence checks lag new
  files). Ground truth = the on-disk
  `.godot/global_script_class_cache.cfg` + per-file `--check-only
  --script`; `pkill -f "godot.*--lsp"` forces a fresh spawn (0
  real diagnostics after).
- 2026-09-07 (dream-2026-09-07; l1-topology-font + scene-refactor):
  Godot editor-viewport captures — control the environment and pick
  the right gate: macOS occlusion throttling freezes WINDOWED
  captures (identical frames; fullscreen puts the window on an
  active Space; CONTENT_SCALE_MODE_CANVAS_ITEMS+EXPAND keeps true
  proportions), and PNG md5 is NOT a determinism gate (the editor
  viewport drifts ±1px with window/dock layout — same-code renders
  gave 3 md5s). Gate on a structural pixel diff (12× downscale +
  blur, grayscale): noise floor max≈1, real composition change
  reads max 110+.
- 2026-09-07 (dream-2026-09-07; model-single-source + tf-in-ci):
  bmad-build can't render where the repo-local `_bmad` lacks
  `_bmad/scripts/render_skill.py` (older installs; bmad-quick-dev
  is GONE from the canonical home) — the waiver path: read the
  skill's step files / `review-prompts/*.md` directly from the
  skill dir (template placeholders like `{workflow.review_layers}`
  stay unresolved — improvise the named layer from the playbook's
  lens list) + a waiver note in the PR body; a self-contained
  briefing carries the rest.
- 2026-09-07 (dream-2026-09-07; tf-in-ci r1/r2 + prod-deploy triage
  09-05/06): GCP IAM claims are verified against the provider or
  not made — predefined-role MEMORY is wrong in both directions
  (bigquery.viewer and resourcemanager.projectIamViewer DON'T
  exist; roles/aiplatform.viewer carries specialistPools.update =
  WRITE), so gcloud-verify every roles/* string's existence AND
  full permission list before it reaches tfvars, and read IAM
  bindings via `gcloud ... get-iam-policy --format=json` parsed
  programmatically (text output collapses compound principalSets —
  a phantom missing grant sends the user on a wrong-fix chase). A
  rerun failing AFTER a fix's timestamp means the fix was WRONG,
  not absent.
- 2026-09-07 (dream-2026-09-07; RTA #185 + wif-durable + #190,
  09-05/06): a new-CI maiden-voyage RED is a bootstrap-ORDERING
  issue until proven otherwise (user-owed applies/variables, not a
  workflow code fix — check the bootstrap checklist FIRST), and
  `gh pr checks` renders CANCELLED runs as fail lines — check the
  run conclusion field before triaging (#190's 'failing' check = a
  cancelled 3s concurrency-noise run).

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
  commit. 2026-08-11 addendum (dream-2026-08-11; 4 new claim-types, one
  job each): (a) STALE-STACK planning doc — a recent DATE ≠ current stack
  (v1 sprint-plan dated post-Odin-pivot but drafted in Godot/GDScript
  citing the superseded `architecture-v1.md`, not `odin-architecture-v1.md`);
  (b) WRONG IDENTIFIER/state-key — briefing named `STATE_FINAL_OUTPUT`
  (the scrubber payload), not `STATE_FINAL_COMPLIANCE_REVIEW` (the gate's
  review slot); (c) WRONG MECHANISM — "register each route in ALL three
  registries" rests on a per-arm model; the registries are PREFIX-matched
  (one arm covers any depth); (d) NAMESPACE COLLISION + SUPERSEDED-vs-LIVE
  doc — two "E" namespaces (arch edge-cases E1–E32 vs GDD epics E1–E11).
  Grep the briefing's named identifier/mechanism/citation against disk
  BEFORE the first commit. 2026-08-13 addendum (dream-2026-08-13; rc3-6,
  rc4-4, 2.2-ecmp, harness-ecmp-demo, rc4-1 — ×5 sightings): three new
  claim-types — (a) grep the ARCHITECTURE AMENDMENTS REGISTER for
  amended behaviour before trusting a briefing AC (rc3-6's "inbound
  STOP→objected" was dead: the 08-08 amendment + shipped stop-link route
  + Twilio one-way sender); (b) grep DB ENUM MIGRATIONS, not the
  briefing, for emitted sets (rc4-4: FIVE codec variants live, the
  briefing named four); (c) CARRY-FORWARD claims about repo state rot
  within a day ("T2 unverified until the rlsw harness exists" — the
  harness existed and worked). 2026-08-17 addendum (dream-2026-08-17;
  packet-plumber-traffic-model-design, -surge-explainer,
  righttenantry-analytics-568-617 — ×3): the rule binds DOC AUTHORING
  too — a design/spec doc cites the SHIPPED call sites + data files as
  ground truth, not plan refs or catalog comments (the GDD M1 tier
  table was STALE vs the shipped catalogs 5/15/40; "Plan §5" had NO
  plan doc on disk — cite meta/dispatch.gleam:18-22; `bandwidth_demand`
  loaded into the catalog but NOT consumed by the flow pass — verify
  per-class transit claims against serve_bundle_lane). Divergence →
  flag the drift IN the deliverable, never silently follow the doc.
  2026-08-20 addendum (dream-2026-08-21; righttenantry-demo-polish-1/-2
  + mobile-layout-1): 'real-app twin' comparisons must NAME THE
  SURFACE — production was 36 commits behind staging and two
  successive parity verdicts were wrong (component-level parity is
  blind to a stale deploy; matching the stale prod would have
  REGRESSED the #615 guarantee) — grep the DEPLOYED bundle: it is the
  runtime truth. And when a briefing premise claims 'no producer
  exists', grep BROADER paths (`/server/src/ai/`, not just the named
  module — `ai_notifications.gleam` outside `notification/` did emit
  the 'nonexistent' event).
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
  disproof). 2026-08-13 addendum (dream-2026-08-13; rc4-1 + 3.3-contention,
  both repos): the pre-PR self-review earns its cost on CODE PRs too —
  an edge-case-hunter self-review before the PR paid off 4 real fixes on
  rc4-1 (vacuous strip guard, hooks-vs-wire divergence, non-forward-
  tolerant decoder, corrupt-row read); the 2-hunter swarm caught the
  spatial-lane mirroring bug on 3.3 — both before Perkins saw the PR.
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
  leave the gap. 2026-08-11 addendum (dream-2026-08-11; routing-canon-amend,
  gdd-mechanics-amend): (d) ASCII-box edits MUST be width-preserving
  (`span, LB)`→`span,bndl)` kept 13 chars — a width-shift breaks diagram
  alignment); (e) pre-emptive NO-OVERLAP placement under an open sibling
  PR — grep the sibling's hunks, place inserts outside them → clean
  auto-merge; (f) for an append-only decision-log, a mid-job sibling-merge
  conflict resolves as DUAL-APPEND (keep both), not pick-a-side; (g)
  disambiguate same-letter namespaces + superseded-vs-live docs before
  editing (qualify a bare "E1"). 2026-08-15 addendum (dream-2026-08-15;
  5.3-pause-ux — 1 sighting, facet completion): (h) a presentation-only
  ruling still earns a canon amendment in the SAME PR (GDD +
  art-direction + story-card status line) — grep the ruling's canon line
  first and STATE THE RULING SOURCE (user ruling date + job id) in the
  amendment so canon and code can never drift undetected.
- 2026-08-09 (dream-2026-08-09; righttenantry-csp-posthog-allowlist 08-06
  + per-applicant-remind 08-08): prove a new test/guard actually BITES —
  negative control: flip one assertion (or inject the violation), confirm
  exactly the expected failure at your path, revert. Terse runners
  (gleeunit's dots) and no-op-via-byte-diff both pass silently otherwise.
  2026-08-11 addendum (dream-2026-08-11; refcheck-rc3-4 — see the Node-blind
  addendum above): the negative-control proof now extends to MASKING tests
  — a fix can be INERT (value ships but JS never populates it) while a
  `simulate.form_body` test MASKS it (drives the simulator, not the
  browser); neutralize the fix and confirm the browser-path test goes red.
  2026-08-13 addendum (dream-2026-08-13; rc4-1 + rc1-1): two new failure
  modes — (a) assert BOTH forms of a JSON-string-embedded payload: the
  ESCAPED wire form (`\"referee_ip\"`) is what ships, so a
  `string.contains(body, "\"referee_ip\"")` assertion is vacuously green
  while the IP is on the wire — assert both forms + neutralize → red;
  (b) grep the file AFTER a python-replace negative-control revert — an
  inline-arg call survived the first revert and silently kept the fix.
- 2026-08-13 (dream-2026-08-13; 3.4-sla, 4.2-surge, 4.1-warning ×2 — ×4
  sightings, both repos): reported success LIES — verify by OBSERVABLE
  effect, not return values: a narrow pipe draw is silently REJECTED
  (max_span 10 — narrow since DISABLED; active tiers 14/16/18, see
  the 2026-09-01 entry) → zero events (spawn narrow-tier nodes ≤10 tiles apart);
  adding pipes to a full router silently rejects (Router_Ports_Full →
  replay_error latched — swap or size the fixture); Odin
  `strings.replace` returns replaced=true while the doc holds the old
  substring (raw-string newline mismatch — pin single-line anchors or
  byte-verify); test-catalog `Balance` fields must mirror
  data/balance.json (zeroed thresholds = every node red at tick 1,
  silently shifting every dump). 2026-08-17 addendum (dream-2026-08-17;
  PP v2-5.2/5.4/5.5/5.9/visibility/local-ci-suite — ×6): any assertion
  whose PRECONDITION can silently not-happen is vacuous — a draw to a
  NONEXISTENT node id is silently REJECTED (`replay_error` latched, no
  test checks it → guard with `!replay_error` + verify ids from spawn
  returns); Odin `make([dynamic]T, 0, N)` has LENGTH 0 (a
  `p.class < len(counts)` guard silently writes nothing); a re-shaped
  pin must be mutation-PROVEN (deleting `&& !esc_cancelled` passed
  20/20 — a pin that can't fail isn't a pin; verify the mutation flips
  the scenario red).
  2026-08-19 addendum (dream-2026-08-19; 5.12-aggregation, 6.1-era,
  5.11-terminal-types — ×3): three new vacuity flavors — a
  concentration pin needs a CREDIT-RICH fixture (800/800 permille WITH
  and WITHOUT the weight = a starved gate, vacuous); never HAND-APPEND
  engine-managed states (`Active_Crisis` auto-resolves — the deferral
  window silently collapsed on a hand-appended row); window-scoped
  counts must count inside the SURGE WINDOW only (the bound formula's
  W, not the whole run).
  2026-08-19/21 addendum (dream-2026-08-21; 7.3 r2→r7, 6.2-r2,
  demo-polish-2-r2, mobile-layout-1 — ≥7 sightings, the #1 Perkins
  blocker genus): the pin must bite at the WIRING level, not the
  helper level (7.3-r5: the pin guarded the pure proc; deleting the
  effect_settings flip passed 16/16) — every fix ships a pin that
  FAILS when the fix is reverted (briefings now carry the bar
  verbatim); a `collects` assertion that never asserts is vacuous
  (6.2-r2 collected the Era_Advanced tick, asserted nothing); a
  shared-path race closes by KILLING the dependency (pid/atomic/
  random suffix — macOS returns IDENTICAL nanoseconds back-to-back;
  7.3's race survived r3→r6 and only r7's ns+crypto-random + ≥5
  consecutive pristine runs closed it); fix-chains migrate surfaces
  (a rename fixed in one artifact survived in two others for 2 rounds
  — grep ALL surfaces, not the reported one).
  2026-08-27 addendum (dream-2026-08-27; crisis-duck, tie-deconflict,
  dublin-spawn-director, arch-egress-migration): compact craft list —
  grep every NEW expect for `|| true` (a vacuous pin wearing a
  seatbelt, shipped AGAIN 08-26); capture the "before" value BEFORE
  mutating the fixture (never re-derive it inside the assertion after);
  `pop()` removes the LAST row — removing a SPECIFIC fixture row needs
  swap-remove; a clamp/max util needs an ASYMMETRIC fixture (60/30 —
  saturated both-directions fixtures cannot discriminate max from
  sum); pin the DRAW PATH / call site, not the pure predicate (a
  pure-proc pin is bypassable where it's called); pin the EXCLUSION
  (eligibility), not the derived ratio.
  2026-08-29 addendum (dream-2026-08-29; look-zoom-language,
  mechanics-the-box, box-crash-third-spawn — ×3 jobs): the lineage
  keeps mutating — (i) FIXTURE-ZERO-DATA vacuity: Views reading
  sprite bboxes must hand-set them (zero bboxes → every router
  endpoint's drawn size 0 → the covenant cap zeroes → the whole
  sweep passes crushed at cap 0); (ii) HELPER-LEVEL vacuity: a
  fail-fast reject helper omitting ONE catalog source dies in an
  EARLIER file and the 'wrong file' branch returns without checking
  — every row green forever; audit by mutating ONE expectation to
  nonsense (green suite = dead table), and fixing the helper exposes
  the stale expectations (~40 — want = the loader MESSAGE substring,
  copied from loader source, never the key name); (iii)
  allocator-behavior-dependent mutation gates are
  vacuous-by-construction (`odin test` bad frees are
  reported-not-fatal, temp_allocator frees leak-invisible) — pin
  ownership via pointer compares.
- 2026-08-17 (dream-2026-08-17; PP merge train #55–#62 — ×5 jobs):
  merge-train hygiene on a multi-PR base — send the rebase relay
  BEFORE the rework push lands so the fix-audit reviews ONE clean head
  (7.2: relay sent before the B1 fix push → r2 APPROVED on 1b96bea);
  grep the sibling PR's hunks for disjointness and expect ZERO
  conflicts (7.2, 5.4 ×2, visibility, doctrine — all clean); a
  merge-order ruling (#59 first, #60 rebases) beats a conflict.
- 2026-08-22/23 (dream-2026-08-23; blender-silhouettes +
  blender-sculpt + look-polish — ×3): determinism evidence — compare
  DECODED PIXELS, never file bytes (Blender 5.2 re-renders are
  pixel-deterministic; md5 diffs were PNG-encoder metadata only —
  strip tEXt/iTXt/zTXt chunks post-render, the wall-clock Date tEXt
  is the only mover); a no-op re-render is golden-safe (pipeline
  validation = render + pixel-compare, no re-bless); the per-commit
  re-bless loop pays when EVERY commit carries the triple-verify
  (cmp -l every .log.bin/.t1 vs HEAD; diff-bbox pixel scans matching
  PREDICTED blend colors ±0; palcheck re-pins with measured floors).
- 2026-08-21/22 (dream-2026-08-23; noc-overlay D-key saga +
  playbook-diet clarify halt — ×2 arcs): a clarify ruling is the
  START of the decision, not the end — expect AMENDMENT on first
  contact with evidence (D-key: Q1-Q4 rulings → root-cause amendment
  "the D never worked" → FINAL: one key, one panel, zero dead code)
  and the final ruling often SHRINKS scope while ADDING an acceptance
  proof ("a render function never called is not a feature" — the E2E
  key-toggle capture). When the user asks mid-flight "should this be
  a skill instead", a reasoned keep-as-dispatched recommendation can
  itself be the ruling (diet clarify halt).

- 2026-08-24..26 (dream-2026-08-27; crisis-duck, dublin-map-beautify,
  arch-latency-egress-queue-model): verification must bind to an
  INDEPENDENT anchor — three self-confirmation flavors: stale
  captions (enumerate crisis state AT THE CAPTURE TICK, never from demo
  comments — golden predictions came from 4.2-era captions), a verify
  that compares the same buggy output to itself (the bake's --verify
  PASSED on broken output; polygonize returned nothing for a round),
  and documented-but-unconsumed knobs (bandwidth_demand loaded but
  UNWIRED — never cite a catalog knob in a formula without grepping
  consumers; "documented in the loader comment" ≠ consumed). Anchor to
  capture-time state dumps, second derivations, consumer greps.
  2026-09-09 addendum (dream-2026-09-09; PP3D typography study
  09-08 + Selva assets/rigs 09-07): name the FINAL representation
  being certified. Record decoded capture dimensions and source SHA
  before cropping/normalization (1600x450 media is not 1600x900
  font-pixel compliance evidence). Contact/scale checks observe
  evaluated world-space geometry, the exact side/part and enabled
  modifier order; saved/reopened or appended timeline behavior is
  checked separately from manual sliders. Intermediate images,
  comments and formulas remain useful diagnostics, not substitutes
  for the final contract.
- 2026-08-24/26 (dream-2026-08-27; dublin-map-beautify,
  look-node-legibility-diag — both exactly 7-round mock loops): the
  user iterates on MOCKS fast (~10min rounds) — keep the mock tool
  PARAMETERIZED per direction, regenerate strips in ONE command, and
  KYLE-verify each round before replying; rulings land from the lavish
  gallery. One-command regeneration is what makes the loop cheap.
- 2026-08-27/28 (packet-plumber-v2-viscomm-regression-audit,
  -congestion-read-a1, -look-zoom-language — 3 jobs): PP
  visual-evidence craft. (a) 'did effect X die' audits resolve
  MECHANICALLY: `harness motion-strip` + a fixed-pixel time-series
  (link centerline color per frame) proves static-vs-animated + the
  phase in one strip; per-era worktree goldens are FREE before/after
  evidence (each worktree's goldens/ = its own era's blessed render
  — compare those first). (b) a user's 'it used to pulse' memory can
  be PERCEPTION of static code (the 4.1 halo never pulsed — the read
  came from level-flicker + ribbon mass): trace the MECHANISM and
  the CANVAS separately or audit the wrong thing. (c) stride the
  evidence harness FIRST (bin/harness_before from HEAD + view-only
  extension), THEN mutate — before-strips → change → re-bless →
  after-strips made every claim checkable in ONE worktree. (d) a
  band-measure palcheck leg returning exactly your scan half-window
  count (2·half+1) is measuring ALONG the feature, not across it —
  assert a predicted pixel count from the draw's own math (dump the
  column) before trusting the leg. (e) trimmed-blit hides
  under-sprite decoration (DrawTexturePro blits the content bbox
  tight): the read is a HALO (radius > 0.5× footprint), and
  predicted blend scans need the TRUE underlay color — probe with
  the correct fit offset (OX=(win−world×fit)/2; seed-7 land tint
  (239,228,186), not canvas). (f) palcheck render-only fixtures:
  `crisis.pipe_congestion` is len 0 until warnings_update runs —
  resize() + explicitly zero grown slots to .None; E26 rejects
  terminal→terminal pipes in fixtures (mirror §7: terminal→router).
- 2026-09-04 (dream-2026-09-04; asset-scout + dream-2026-09-02's
  max_span case): MEASURE, don't trust metadata or competing quotes
  — third-party asset scales and remembered contract numbers are
  unreliable in both directions; re-derive from the source (canon
  JSON, measured world bbox carried in explicit scene metadata like
  PP3D_NormalizedScale), never pick a winner between two claims
  (max_span 10-vs-14/16/18 resolved against data/pipe_tiers.json —
  10 was the DISABLED tier).
- 2026-09-07 (dream-2026-09-07; gdd-amend-alive-planet +
  gdd-amend-levels): column-aligned markdown (ASCII boxes, tables)
  — build replacement lines in python and ASSERT display width
  (east-asian-aware; emoji count 2) BEFORE issuing the edit, and
  re-render the region after (an inserted clarifier paragraph
  silently orphaned an M5 table split; pad math inner=65 vs real 64
  made every line 70).
- 2026-09-07 (dream-2026-09-07; gdd-amend-alive-planet +
  gdd-amend-cumulative): a canon amendment greps the OLD phrasings
  repo-wide BEFORE editing (caught the tutorial-seed +
  L1-remediation stragglers the section-level plan missed) and
  DATE-STAMPS the supersede note at EVERY site the old claim lives
  (D5's retirement clause had propagated to 4 sites) — an undated
  site reads as current canon.
- 2026-09-07 (dream-2026-09-07; gdd-amend-cumulative / -era-planets
  / -levels): scope-guard courtesy — touch ONLY the files the
  briefing names; ADJACENT-surface finds get flagged for a ruling
  (decision log + PR body, or an in-page lavish decision form),
  never silently fixed (the README stale comment rode the PR by
  user ruling, zero cross-lane conflict). A user ask satisfied from
  the repo's own canon records does NOT break the guard.
- 2026-09-07 (dream-2026-09-07; gdd-amend-levels + era-costume
  ladder): lavish decision forms that parse — per-row radios + ONE
  Queue button produce machine-parseable tagged rulings (D1-D5
  arrived clean); pair every form with a pros/cons explainer when
  the options aren't self-evident (the user asked "explain this,
  pros and cons" on exactly the two forms that lacked one).

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
- 2026-08-11 (dream-2026-08-11; righttenantry refcheck-rc3-2/-rc3-3/-rc3-4
  — ≥3 sightings): the "registry-omission" blocker class — adding a POST
  route means registering it in EVERY access-control/observability
  registry the codebase maintains (RT: `is_public_path`, CSRF allowlist,
  `redact_token_route`). Missing one is a recurring Perkins blocker (csrf
  arm absent → route 403s; redact arm absent → token leak in logs). When
  adding ANY route, enumerate every registry and arm each; the lesson is
  now baked into RT briefings by name ("the rc3-3 csrf-registry lesson").
  2026-08-13 addendum (dream-2026-08-13; rc3-6): which arms apply is
  PER-ROUTE-FAMILY — a NEW top-level path family (`/webhooks/*` vs
  `/api/v1/webhooks/*`) needs its OWN registry arms; the existing
  `["api","v1","webhooks",..]` CSRF prefix did NOT cover it (a missing
  arm 403s). Verify each registry against disk per route family.
- 2026-08-13 (dream-2026-08-13; rc4-2 r2 W4 + rc4-3 r2 W3 + rc4-4 — ×3
  rounds, ×3 jobs): timestamp FORMAT-MIX — PG `::text` renders
  timestamps with a SPACE separator, app code stamps RFC3339 `T`; space
  (0x20) < 'T' (0x54), so string compares/sorts INVERT same-day events
  (evening before morning). Normalize space→T before comparing/sorting,
  and pin with a fixture the server ACTUALLY sends (rc4-2's pin fed a
  never-sent format — Perkins r2 caught the wrong fix).
- 2026-08-13 (dream-2026-08-13; rc4-3 r4 B1 + #36 r2 B1 — ×2 blockers,
  both repos): a fix whose regression test is VACUOUS or ABSENT is still
  a blocker even when the mechanism is real by inspection — fix-audits
  must verify the test pins the ORIGINAL failure mode and drives the
  REAL route (rc4-3 r4: the backstop test called the dead SQL directly,
  never the POST route; #36 r2: the demolish-and-renumber test was
  absent — every resolve fixture preserved slot order). The passing
  fix: drive the real route + pin the mechanism + neutralize → red.
- 2026-08-23 (dream-2026-08-23; the PP v2 NOC surface r1-r3 + font r3 +
  sound r2 — ×3 review crafts): (a) ship every pin with its MUTATION
  LEG unprompted (delete-the-call / flip-the-default /
  mutate-the-pixels) — Perkins now treats a vacuous gate as a BLOCKER
  and mutation-verifies fixes independently (noc-toggle r2:
  delete-dismissal fails, default-flip fails 3 tests, ROW_COUNT->4
  wraps+fails; font r5: gate-10 rebuilt dual-render, 0px mutated vs
  54k healthy). (b) fix-folds REGRESS THEMSELVES on shared
  chrome/input surfaces — each CHANGES_REQUESTED fold was genuinely
  good yet exposed the adjacent interaction bug (stuck-panel → play_w
  desync → header collision → tray-chip dead zone); budget multiple
  rounds for a shared surface and carry the class LINEAGE in the fold
  briefing so the minion greps the whole surface, not the named lines.
  (c) the PR body + fold claims are AUDITABLE artifacts — a prose
  claim the code doesn't back is a BLOCKER (font r3 fictitious N11
  dead-retries field; font r1 B2 wrong body), a stale body is a note
  (noc-readability-2 N6': r1 text on the live PR — one `gh pr edit`);
  re-audit your own PR body against the final head before each round.

- 2026-08-26 (packet-plumber-v2-arch-egress-migration; dream-2026-08-27;
  generalizes the estate-r3 B1 slot-renumber class): index-keyed derived
  state must RESET on regeneration — a same-count bundle renumber
  (demolish+draw in one batch) silently inherits the dead pair's history
  unless derived-ring layouts reset on Topology.gen (hunter-probed at
  120 phantom ticks). Incremental maintenance on renumberable indexes
  inherits dead entries' state.
- 2026-08-25 (packet-plumber-v2-viscomm tie-deconflict + gauge-telegraph;
  dream-2026-08-27, 2 jobs): palette pins must check ALL variant
  surfaces — CVD mode tables can silently reintroduce a base-palette
  collision you just fixed (route_tie remapped to pale amber
  RGB-IDENTICAL to state_congested's remap — always diff the mode tables
  too), and UI often draws the darkened `state_*_text` VARIANTS, not the
  raw state colors (a pixel pin against the raw color reads 0 px and
  looks like a geometry bug). Sibling: tools/derive_a11y_palettes.py
  cannot parse palette.json inline `//` comments — run it on a
  comment-stripped copy.
- 2026-08-25/26 (packet-plumber-v2 crisis-duck + tie-deconflict;
  dream-2026-08-27): render-surface realities defeat pixel gates — rlsw
  renders DrawTriangle FILLS opaque (an alpha-only "recede" on a
  hand-built triangle surface is a no-op); street-oriented quads are
  BACKFACE-CULLED for some windings (a fill-changing mutation stays
  pixel-inert because THE FILL NEVER RENDERS there — probe with
  distinct-color dumps before trusting any block-surface gate); when a
  highlight OWNS the surface, pin the NEIGHBOR surface (crisis outline
  overdraws the whole band — non-recede pinned one layer out); and
  palcheck sections may do full LIVE-RENDER analysis checks (ClearBackground
  + draw + LoadImageFromScreen) without touching goldens — the
  golden-capture path never invoking assists does NOT apply to analysis
  renders.

- 2026-08-28 (dream-2026-08-29; mechanics-the-box r3/r4 +
  box-crash-third-spawn — ×3): FLAG-ON coverage ships at ZERO unless
  explicitly gated — ruling wiring (era-1 start + 6.2 gate) had ZERO
  coverage (r3 B4); the debug-override leg shipped RED (the era row
  asserted ==1 under PP_DEBUG where =3 is the sanctioned override —
  gate the assertion on !PP_DEBUG, both builds 52/52); and a
  flag-gated feature had ZERO exercising demos (the 3rd-spawn
  SIGABRT: box-on × telegraph-lead existed only in the user's
  playtest). A ruling that changes shipped defaults needs its wiring
  covered in EVERY configuration the gates build (default AND debug
  override); a feature flag needs ≥1 flag-ON demo/gate (the
  env-gated frame-script driver pattern covers it headless).
- 2026-09-04 (dream-2026-09-04; tie-deconflict 08-25 +
  rta-prod-scale-to-zero + e2 harness — cross-lane, ≥3 sightings):
  PROVE THE RED before trusting green — a deliberate-fail probe is
  the cheap way to confirm a test binary actually executes your new
  test; a negative control (revert the value → suite MUST fail)
  proves a regex/guard actually guards; and on Godot the abort class
  needs abort-must-FAIL mutation legs (aborted coroutines still
  yield int on 4.7.1 — PASS can print over a crashed test; count
  printed checks vs check() calls to catch PHANTOM checks). No
  green is trusted without a witnessed red.
- 2026-09-09/10 (dream-2026-09-11; PP3D observation lane + Selva
  process-identity, cross-job): IDENTITY/FACTS GUARDS — pin locale,
  normalize fields, persist rejection evidence. A process-identity
  guard false-fired on LOCALE drift (host LANG=en_GB.UTF-8 vs MCP
  LANG absent → ps lstart 'Thu10Sep' vs 'ThuSep10' across PIDs); fix
  = per-ps-child LC_ALL=C on BOTH producer and consumer + fresh
  expectations. Siblings: a facts-equality guard that conflated a
  180-line terminal-output blob with policy refused on the operator's
  own progress (exclude ordinary output semantically); an identity
  monitor aborted WITHOUT persisting rejected ps rows (cause UNKNOWN
  — persist rejected operands for forensics); and readiness
  sequencing: ALL host prep first, THEN the fresh receipt → immediate
  launch (an idle-pass report after signing expires the receipt it
  reports). Any guard string-comparing whole live process state or
  embedding terminal output will false-fire.
- 2026-09-04 (dream-2026-09-04; tie-deconflict r2 + e1 + e2): GATE ON
  THE REAL OUTPUT SURFACE, not the predicate — a pure-proc pin is
  bypassable at the call site (render tests passed under the
  bypass; the palcheck pixel scan of the REAL render was the gate
  that failed); pose/geometry claims verify by SCREENSHOT; flow
  claims by white-box probe against the live admission path.
  Predicates verify the mechanism; the artifact is the acceptance.
- 2026-09-04 (dream-2026-09-04; tie-deconflict + rta-prod-scale-to-zero,
  cross-repo): A VALUE LIVES IN ≥2 PLACES — production values get
  mirrored into test pins and override/compat tables, and the
  mirror detonates later on an UNRELATED PR (a11y mode tables
  silently reintroduced a fixed palette collision; RT's
  test_concurrency.py pin left develop RED after a tfvars flip,
  CI-blind via path filter, detonating on the #177 promote). Before
  flipping any config value: grep the test suite AND all
  override/mode tables for the old value; flip them together or not
  at all, and prove with a negative control.

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
dispatch's model. 2026-08-19 addendum (dream-2026-08-19;
v2-7.3-accessibility-core): the briefing/ledger model line can also be
provider-DEAD at dispatch (the `deepseek/deepseek-v4-flash` line was
402-balance-dead; Silas launched on glm-5.3 despite the ledger's flash
field). Check `PI_MODEL` + the session jsonl's modelId before trusting
ANY model attribution — briefing, ledger field, or dispatch label.
