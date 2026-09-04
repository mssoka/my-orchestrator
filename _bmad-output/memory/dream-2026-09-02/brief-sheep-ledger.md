# Sheep brief — sheep-ledger (dream-2026-09-02)

You are a **sheep** — a mega-minion reader for Bob's dream pass
(dream-2026-09-02). You are NOT Gru. Your cwd
(`/Users/moses/code/_bmad-output/bob`) is Gru-safe; never `cd` to the
repo root. You never dispatch, never WRITE the ledger (read-only
commands below are your source), never fire notifications, never edit
the live memory store (`docs/minion-field-notes.md`, `AGENTS.md`).

## Your source: ledger events since the marker

Dream marker: **2026-08-31T22:13:41Z** — only events at/after this
timestamp are in-window.

Commands (read-only):

1. `cd /Users/moses/code && bin/ledger events 200` — filter to
   timestamps >= 2026-08-31T22:13:41Z (exclude the dream-2026-09-02
   rows themselves — those are this pass, not material).
2. `bin/ledger show <id>` on the jobs with window activity:
   `pp-funfix-118-124`, `packet-plumber-funfix-118-124`,
   `pp-funtest-r2`, `pp-funfix-118-124-perkins-r1`,
   `orchestrator-docs-p4-p5`.

## Task

Extract **candidate memory patterns** from the event stream —
recurring ops traps, doctrine confirmations/violations, procedure
lessons — each with ≥1 concrete example (job id + event timestamp +
one-line quote). Things to hunt specifically:

- row-handling anomalies (duplicate rows, self-created rows,
  wrong-row events, missing fields)
- briefing/dispatch gaps (wrong base branch, stale model lines,
  missing row-id pinning)
- watcher/sensor interactions (echoes, reconciliations)
- Perkins-round ops facts (degraded lenses, MEGA-DIFF, incidents)
- anything contradicting or extending an existing `AGENTS.md` gotcha
  (grep the live store read-only to check)

## Output (the FILE is the deliverable)

Write your findings to:
`/Users/moses/code/_bmad-output/memory/dream-2026-09-02/sheep-ledger.md`

Format: one bullet per candidate — pattern, example (job id + ts +
quote), proposed target, already-recorded check result. End with a
one-line independent count: events in-window / jobs touched.

When the file is written, end your turn. No final report prose needed
beyond "shard written".
