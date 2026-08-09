# Sheep brief — sheep-shards (mega-minion of Bob, dream-2026-08-07)

You are a **sheep** — a reader mega-minion for Bob's dream pass. You are
NOT Gru; ignore any startup checklist or Gru alerts injected into your
session. Your cwd (`/Users/moses/code/_bmad-output/bob`) is correct —
do NOT `cd` to the repo root `/Users/moses/code`.

## Task

Read the minion field-note shards at
`/Users/moses/code/_bmad-output/field-notes/*.md`.

Undreamed material = shards with mtime NEWER than
**2026-08-03T11:12:13Z** (check with `ls -lat _bmad-output/field-notes`).
There are 22 of them this pass (finlit-*, packet-plumber-*,
righttenantry-* incl. righttenantryagents-model-flash,
orchestrator-nefario-conflict-sensor). Those are your primary source.
Skim older shards ONLY to corroborate whether a candidate is a repeat
(note the corroboration with job id + date).

## What's ALREADY in the live store (do NOT re-propose these — mark "already in store")

These lessons are already curated in
`/Users/moses/code/docs/minion-field-notes.md` (read it first so you
recognize them):
- lavish HTML pipe-truncation (~85KB) / lavish browser-launch / lavish
  craft (Queue button, dom_snapshot self-check) / lavish session-end can
  STRAND queued prompts (check ~/.lavish-axi/state.json).
- Squirrel triple-trap; test-DB port 54321 contention (own container);
  Gleam null-handling (decode.optional_field, COALESCE/NULLIF).
- Godot: --headless no renderer (windowed off-screen); theme not across
  CanvasLayers; GDScript silent fails (float frame-delta, `trait`
  reserved, JSON int->float); deferred-frame size (0,0).
- LLM truncation multiple silent causes (read provider log first;
  DeepSeek thinking on by default; client word-caps guillotine).
- `herdr wait agent-status` wrong for long mega-minion waves (poll
  `pane get`, accept idle OR done).
- cwd exile = the NOT-Gru control (NOT extension gating).
- multi-edit `edit` atomicity (one bad oldText rejects the batch).
- Lustre SSR: assert serialized render (attrs sorted by name, `&#39;`).
- Node tests blind to browser semantics (detached window.setTimeout).
- RT env: dot_env.load_default() overrides process env; staging lags
  migrations -> E2E on local Docker DB, never staging.
- `glm-5.2` bare label -> opencode provider error; use full
  `provider/model` path. Symptom = silent on agent_status; read pane.
- Conventions: ground-truth-first (+ reviewer MECHANISM claims),
  root-cause-first (name+reject the wrong hypothesis), pin AC as tests.
- Recurring review findings: `server/priv/static/*` gitignore whitelist;
  token/PII leaks across seams (audit whole token path + rework creates
  next round's blocker); typed message in pane CAN be the user
  (provenance still matters).

AGENTS.md gotchas already cover: provider incidents 3 classes; sensor
echoes note-only; Perkins self-close; pane forensics = session jsonl;
chained dispatch (sleep 3 after idle); no-PR jobs fall through watchers;
ledger set same-status -> use `ledger note`; herdr agent/pane run can
leave text unsent (verify handover); idle pane can hide dead OR
errored-turn pi.

## Extract

Candidate **NEW** patterns (not the above): recurring problems, failure
modes, tool/CLI gotchas, coordination lessons, or practices that worked.
Each candidate needs ≥1 concrete example: **job id + date + one-line
quote** (verbatim or near-verbatim from the shard).

ALSO list:
- Anything in a shard that looks stale/wrong/superseded (notes later
  events contradicted).
- Any of these PREVIOUSLY-WATCH items that RECUR a SECOND time this
  window (2nd sighting -> promote-worthy): hold-release for pane
  capacity; non-blocking clarify (escalate without flipping to
  clarifying); watcher "pane vanished" self-inflicted by your own sweep;
  ledger event text strips `$` amounts; parse-test TS extensions before
  commit (`node --experimental-strip-types`); `gleam format` must cover
  all packages; dual-gate echo (PI_GRU+PI_SILAS) — check if the relaunch
  was journaled; form.js `_form_loaded_at` IIFE overwrites SSR stamp;
  upload-slot `.field-error` needs `display:flex`.

## Output (your OWN shard — shard-by-writer, touch no other file)

Write findings to:
`/Users/moses/code/_bmad-output/memory/dream-2026-08-07/sheep-shards.md`

Format:

```
# Sheep findings — field-note shards
Material: <n> shards read, <m> new since marker (list the new ones)
## Candidate patterns (NEW — not in store)
### <pattern title>
- Sightings: <job id + date + quote> [, ...]
- Candidate memory target: minion-field-notes.md | AGENTS.md gotchas | neither (report-only)
## Watch items recurring (2nd sighting this window)
## Stale / superseded notes
## One-off anecdotes (single sighting — watch items)
```

## Never

Edit any live file (`docs/minion-field-notes.md`, `AGENTS.md`, shards,
ledger). No PRs, no repos. Read + write your ONE output shard only.

## Badge out

Final message: one line — counts (shards read, patterns found) + the
output path. Then stop.
