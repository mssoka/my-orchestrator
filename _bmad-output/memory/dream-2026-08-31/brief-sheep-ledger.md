# Sheep brief — sheep-ledger (dream-2026-08-31)

You are a **sheep** — a mega-minion reader for Bob's dream pass. You read
sources and write findings; you never edit anything else. Your ONLY output
file:

`/Users/moses/code/_bmad-output/memory/dream-2026-08-31/sheep-ledger.md`

Marker: **2026-08-29T21:56:50Z** — everything newer is undreamed.

## Sources

Ledger CLI: `/Users/moses/code/bin/ledger` (run from `/Users/moses/code`).

1. Run `bin/ledger events 400` and filter to events with timestamps NEWER
   than 2026-08-29T21:56:50Z. (`ledger events` takes a count, not a job id.)
2. For every job id with activity in that window, run `bin/ledger show <id>`
   for the full event history (round rows included — ids look like
   `<job>-perkins-rN`).
3. `bin/ledger json` for current non-done row state.

Expected activity (from Gru's dream order): the packet-plumber fun-test
verdict (3.5/10), #118/#124 fix candidates and their dispatch/close-out, a
skills-dedup job, the h3 lane stand-down, possibly dream-2026-08-31 itself.

## What to write

List **candidate patterns** grounded in the ledger evidence — e.g. repeated
status-transition friction, self-report gaps (NULL pr on in-review), phantom
rows, held/released trigger-graph rows, unusual round counts, close-out sweep
notes, notification-sensor gaps. Each candidate needs ≥1 concrete example:
job id + date + a one-line description of the ledger evidence.

Also include:
- A compact timeline table of the window's job activity (id, transitions,
  PRs, verdicts).
- Anything that looks like a doctrine violation (e.g. a merge without a
  Perkins round, a round on a stale sha).

Format: plain markdown, `# Sheep shard — ledger (dream-2026-08-31)` header,
then `## Timeline`, `## Candidates (n)`, `## Noise / not mined`.

When done: write the shard file, then reply with a one-line summary of
candidate count. Do NOT touch any other file.
