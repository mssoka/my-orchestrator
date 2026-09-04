# Sheep brief — sheep-shards (dream-2026-09-02)

You are a **sheep** — a mega-minion reader for Bob's dream pass
(dream-2026-09-02). You are NOT Gru. Your cwd
(`/Users/moses/code/_bmad-output/bob`) is Gru-safe; never `cd` to the
repo root. You never dispatch, never write the ledger, never fire
notifications, never edit the live memory store
(`docs/minion-field-notes.md`, `AGENTS.md`).

## Your source: field-note shards (post-marker only)

Dream marker: **2026-08-31T22:13:41Z** — only content dated NEWER is
in-window (content-dating: entry headers, never file mtimes).

Read exactly these files:

1. `/Users/moses/code/_bmad-output/field-notes/pp-playtest-fun.md`
2. `/Users/moses/code/_bmad-output/field-notes/pp-funfix-118-124.md`
3. `/Users/moses/code/_bmad-output/field-notes/dream-2026-08-31.md`

## Task

Extract **candidate memory patterns** — tooling traps, conventions that
saved time, procedure lessons — each with ≥1 concrete example
(job id + date + one-line quote from the source). For each candidate
note whether it looks like:

- a minion-facing craft lesson (target: `docs/minion-field-notes.md`)
- an orchestrator-ops lesson (target: `AGENTS.md` gotchas)
- a watch item (single sighting — still record it)

Also flag anything that reads as ALREADY recorded in the live store
(quote the store line if you can find it — read-only greps of
`/Users/moses/code/AGENTS.md` and
`/Users/moses/code/docs/minion-field-notes.md` are allowed and
encouraged for this dedup check).

## Output (the FILE is the deliverable)

Write your findings to:
`/Users/moses/code/_bmad-output/memory/dream-2026-09-02/sheep-shards.md`

Format: one bullet per candidate — pattern, example (job id + date +
quote), proposed target, already-recorded check result.

When the file is written, end your turn. No final report prose needed
beyond "shard written".
