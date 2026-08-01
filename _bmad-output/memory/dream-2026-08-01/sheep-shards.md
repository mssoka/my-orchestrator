# Sheep findings — field-note shards (11 files, since 2026-07-30T00:34:49Z)

## Candidate patterns

### Squirrel (gleam SQL codegen) traps: staging clobber, regen churn, type limits [STRONG]
- Evidence: righttenantry-form-funnel-w0, 2026-07-31: "run_squirrel.sh sources .env and clobbers your override — run ... gleam run -m squirrel directly after make test-db-up (never let it point at staging), and revert the formatter churn"
- Evidence: righttenantry-refcheck-rc1-1, 2026-07-31: "run_squirrel.sh points at staging, which doesn't have unmerged migrations; and every regen re-emits a whitespace-only change to server/src/ai/sql.gleam — revert that file after each run"
- Evidence: righttenantry-refcheck-rc2-1, 2026-07-31: "Squirrel types ALL cast expressions non-Option ... and can't codegen timestamptz results at all — nullable non-text columns must be COALESCE(x::text, '') with NULLIF($n,'') on writes"
- Class hint: tooling trap

### Test-DB port 54321 contention across sibling worktrees [STRONG]
- Evidence: righttenantry-refcheck-rc1-1, 2026-07-31: "Test-DB port 54321 is contended across worktrees: run your own container (docker run -d --name rt-<job>-test-db -p 5432X:5432 postgres:16-alpine) and pass TEST_DB_PORT"
- Evidence: righttenantry-refcheck-rc2-1, 2026-07-31: "make test-db-up port 54321 can be occupied by a sibling minion's container — run your own postgres:16-alpine on 54322 + TEST_DB_PORT=54322 scripts/reset-test-db.sh"
- Class hint: tooling trap

### Godot headless is not a renderer — windowed-off-screen for captures, headless only for import/test gates [STRONG]
- Evidence: finlit-prototype, 2026-07-31: "godot --headless --check-only <project> is NOT a valid invocation and hangs for 120s+; the working headless gate is godot --headless --path <dir> --import then --quit-after 600"
- Evidence: finlit-visual-mock, 2026-07-31: "Screenshot rig: --headless has no renderer (blank PNGs); run windowed with --position -3000,-3000 to stay off the user's screen — rendering still works"
- Evidence: finlit-bugfix-event-messages, 2026-07-31: "--headless = dummy renderer (viewport.get_texture().get_image() returns NULL) — captures must run WINDOWED"
- Class hint: tooling trap

### Godot theme propagation is tree/CanvasLayer-scoped [STRONG]
- Evidence: finlit-visual-mock, 2026-07-31: "theme does NOT propagate across a CanvasLayer — popups under PopupLayer render default-white text unless you hand them the theme (card.theme = theme in _open_popup)"
- Evidence: finlit-bugfix-event-messages, 2026-07-31: "theme propagation is tree-scoped, so scene-instantiating color tests must add dynamically built cards INTO the tree (or hand the node the theme like _open_popup does)"
- Class hint: tooling trap

### GDScript/Godot fails silently — no error, no warning [STRONG]
- Evidence: finlit-prototype, 2026-07-31: "trait is a RESERVED word in GDScript; ... JSON.parse turns ALL ints into floats, so save-load needs an explicit re-cast pass before array indexing"
- Evidence: finlit-prototype, 2026-07-31: "theme_override_constants/separation is tscn-serialization syntax only — at runtime use add_theme_constant_override()"
- Evidence: finlit-bugfix-event-messages, 2026-07-31: "var x := 60 (int) then x -= delta silently TRUNCATES each frame (−1/frame) — no error, no warning; any var receiving frame deltas must be explicitly float-typed"
- Class hint: tooling trap

### Godot deferred frame semantics bite same-frame code [STRONG]
- Evidence: finlit-visual-mock, 2026-07-31: "styling/animating a node the same frame it's add_childed gives size == (0,0) — juice pivots must await resized; and get_child(i) right after a rebuild hits queue_free'd nodes"
- Evidence: finlit-bugfix-event-messages, 2026-07-31: "await process_frame inside SceneTree._initialize() deadlocks — drive frames from _process; _ready is DEFERRED to the first iteration when add_child happens in _initialize"
- Class hint: tooling trap

### LLM (DeepSeek) output truncation — diagnose from the provider log + client config; causes are silent and multiple [STRONG]
- Evidence: finlit-prototype, 2026-07-31: "deepseek-v4-flash has THINKING ON BY DEFAULT and it silently eats max_tokens (kid answers truncate mid-sentence) — send \"thinking\": {\"type\": \"disabled\"}"
- Evidence: finlit-tutor-economy-fix, 2026-08-01: "check user://tutor_llm_log.jsonl FIRST — this one was finish_reason: stop on every call; the CLIENT-side word-cap was the guillotine, not max_tokens/thinking. And 'trim at sentence boundary' must be abbreviation-aware"
- Class hint: tooling trap

### Lavish craft: question-page design, truncation-safe artifact builds, dom_snapshot self-check [STRONG]
- Evidence: righttenantry-form-completion-ps, 2026-07-31: "Moses answers lavish question pages well when each question has its own Queue button + a 'which rulings I need most' summary in the poll --agent-reply; he ended both sessions cleanly with Send & End after ~2 exchanges"
- Evidence: righttenantry-refcheck-v1-epics, 2026-07-31: "npx -y marked --gfm -o .lavish/_body.html <file>.md (writes to file, no pipe truncation), then a python file-write wrapper for the brand CSS/hero — 88KB artifact, tail verified, no truncation (confirms the 2026-07-29 curated trap)"
- Evidence: righttenantry-refcheck-v1-sprint-plan, 2026-07-31: "lavish-axi poll DOM snapshot exposed a Mermaid render failure my own eyes never saw ... Read the dom_snapshot on poll return, not just the prompts; it's the only self-check of what the user actually saw"
- Class hint: interaction

### Ground-truth-first: verify against disk / repo / logs, not session context or assumptions [STRONG]
- Evidence: finlit-game-brief, 2026-07-31: "Mega-minions re-reviewing a file the parent just edited can report STALE findings from session context (2 this run) — verify every finding against disk before applying"
- Evidence: righttenantry-refcheck-v1-epics, 2026-07-31: "check the actual status enum + stepper component in the repo before spec'ing a trigger story (client/src/components/status_stepper.gleam, shared/src/shared/application.gleam)"
- Evidence: finlit-tutor-economy-fix, 2026-08-01: "check user://tutor_llm_log.jsonl FIRST"
- Class hint: convention | review finding

### Gleam decode brittleness around null/missing data [STRONG]
- Evidence: righttenantry-form-funnel-w0, 2026-07-31: "gleam decode.subfield + decode.optional does NOT tolerate missing keys (the whole decode fails) — for back-compat payloads use decode.optional_field(..., default, ...)"
- Evidence: righttenantry-refcheck-rc2-1, 2026-07-31: "nullable non-text columns must be COALESCE(x::text, '') with NULLIF($n,'') on writes, or you ship decode-failures/''-in-index bugs (house ai/sql.gleam has the latent instance)"
- Class hint: tooling trap

## Anecdotes (single sightings)
- finlit-game-brief, 2026-07-31: `herdr wait agent-status --status done` can time out even when the mega-minion finished — panes in a watched tab complete as `idle`, not `done`; poll `herdr pane get` and accept either. (Minion-side herdr lesson; AGENTS.md Gru gotchas don't cover this one.)
- finlit-game-brief, 2026-07-31: gds-create-game-brief's `.decision-log.md` is a dotfile — confirm with `git status` before committing ("only the new artifact" verify bar).
- finlit-visual-mock, 2026-07-31: deterministic stills recipe — `set_process(false)` freezes game timers; seed states via the pure economy API, never clicks.
- finlit-bugfix-event-messages, 2026-07-31: a failed edit in a multi-edit `edit` call fails the WHOLE call atomically — re-check the file.
- finlit-bugfix-event-messages, 2026-07-31: `.tres`/`.tscn` colors store 6-decimal truncations vs exact /255 from `Color("#hex")` — assert with `is_equal_approx`, never `==`.
- finlit-tutor-economy-fix, 2026-08-01: "theoretical max wage" math must include the parents allowance (+$1/drop) — couch-only math left a $0 doctrine margin; edge hunter caught it (price $1,800→$2,000).
- finlit-tutor-economy-fix, 2026-08-01: repricing an economy silently REVALUES old saves — bump the save schema version and let corrupt-recovery absorb them, or you fabricate wealth-climb.
- righttenantry-form-completion-ps, 2026-07-31: worktree `.env` points at the STAGING Supabase; prod is a different project — use `./deployment/db.sh prod -c "..."` (psql `-v` doesn't survive the wrapper, inline literals). (Same staging-contamination theme as the Squirrel pattern.)
- righttenantry-form-completion-ps, 2026-07-31: read-only prod funnel queries at aggregate level are fast and safe — do them EARLY; they reframed the whole session before any lavish round-trip.
- righttenantry-form-funnel-w0, 2026-07-31: `server/priv/static/*` is gitignored with a per-file exception list — new static assets need a `!path` exception or they silently never deploy (caught only by the review swarm).
- righttenantry-refcheck-rc1-1, 2026-07-31: extending `shared/application.Application` ripples into full-literal fixtures across client+server tests — grep `application.Application(` and `GetApplicationDetailRow(` before claiming done.
- righttenantry-refcheck-rc2-1, 2026-07-31: integration `truncate_all` is a fixed table list — any new table without a FK to a truncated parent must be added or tests leak rows.
- righttenantry-refcheck-v1-epics, 2026-07-31: two same-day "final" design docs contradicted each other in 4+ places — diff them BEFORE writing stories; the UX §15 decisions record is the tiebreaker only where it explicitly names the decision.
- righttenantry-refcheck-v1-sprint-plan, 2026-07-31: feature-line sprint trackers sit beside the canonical file as `sprint-status-<slug>.yaml` — bmad-sprint-planning's fixed `status_file` path needs overriding; story keys keep the epic prefix (`rc1-1-...`).
- righttenantry-refcheck-v1-sprint-plan, 2026-07-31: `_bmad/scripts/memlog.py` is per-worktree shared and append-only — never prune another job's entries, just append with `--workspace . --text`.

_Stale check: no shard contradicted an existing curated note; one re-confirmed the 2026-07-29 lavish pipe-truncation trap (refcheck-v1-epics evidence above)._
