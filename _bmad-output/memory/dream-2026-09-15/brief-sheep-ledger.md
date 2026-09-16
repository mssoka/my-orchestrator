# Sheep brief — sheep-ledger (dream-2026-09-15)

You are a reader sheep for the dream pass. Your ONLY job: read the ledger
dump below and write candidate patterns to your shard. You do NOT edit any
other file, never touch repos, never dispatch anything, never write to the
live ledger DB.

## Source

/Users/moses/code/_bmad-output/memory/dream-2026-09-15/ledger-dump.txt —
`bin/ledger show` output for the 12 jobs with ledger activity since the
marker 2026-09-13T03:03:31Z:

- packet-plumber-3d-constellation-view-v2-perkins-r2
- youtube-channel-selva-electrica-assets-rigs
- packet-plumber-3d-constellation-view-v2
- youtube-channel-selva-mlx-ai-production
- packet-plumber-3d-l1-spawn-awareness-37
- youtube-channel-selva-electric-loom
- packet-plumber-3d-l1-spawn-awareness-37-perkins-r1 / r2 / r3
- youtube-channel-thumbnail-ctr-research-20260914
- packet-plumber-3d-pp3d-playtest-fixes-1
- packet-plumber-3d-pp3d-playtest-fixes-1-perkins-r1

Each block has the full row (status, dates, model, pr, briefing path) plus
the complete event history with timestamps and notes.

## Output (YOUR file only — nobody else writes it)

Write your findings to:
/Users/moses/code/_bmad-output/memory/dream-2026-09-15/sheep-ledger.md

Format — a list of candidate patterns, each with:

### <candidate pattern title>
- Evidence: <job id + event timestamp + a VERBATIM one-line quote from a
  ledger note (copy exactly — do not paraphrase; quotes will be
  grep-verified)>
- Sighting count: <n> (<where>)
- Why it matters: <one line — what a future session would do differently>

Hunt for: recurring status-transition shapes, repeated close-out/sweep
behaviors, PR/review loop patterns, row-hygiene gaps (missing pr field,
stale pane pointers), repeated blockers and their resolutions, model/
provider routing decisions, timestamps that show process discipline or its
absence. Each candidate needs at least one concrete example. Single
sightings are still worth recording (mark them "single sighting").

If you want more context on a specific job, you may READ
`/Users/moses/code/bin/ledger show <id>` output (read-only) — but never
write. When done, write the shard file and end your turn with a one-line
summary (no dispatch, no notifications — Bob handles those).
