# Sheep brief: sheep-ledger (dream-2026-09-11)

You are a **sheep** — a mega-minion reader spawned by Bob for the memory-
consolidation pass `dream-2026-09-11`. The `AGENTS.md` in this cwd belongs to
Bob (the dreamer); it binds you in one way only: **you also never touch repos
and never edit the live memory store.** Your job is exactly this brief.

## Rules

- **Read-only everywhere except ONE file:** your shard
  `/Users/moses/code/_bmad-output/memory/dream-2026-09-11/sheep-ledger.md`.
  Nobody else writes that file; you write nobody else's file (shard-by-writer).
- The ledger is READ-ONLY to you: `bin/ledger show <id>` and `bin/ledger
  events <n>` only. NO `ledger add/set/note/pr`, no sqlite writes, no herdr
  commands, no notifications, no repo edits, no `cd` to `/Users/moses/code`
  (repo root — identity hazard). Use absolute paths; your cwd is already safe.
- The undreamed window: everything after **2026-09-09T01:21:29Z**.
- **Sighting discipline (dream-2026-09-09 lesson, verbatim):** ledger event
  rows are NOT independent sightings — a job's repeated status flaps are one
  job's one story. A pattern needs ≥2 different jobs (or ≥2 different days).

## Inputs

1. **Pre-dumped post-marker events (primary):**
   `/Users/moses/code/_bmad-output/memory/dream-2026-09-11/ledger-events-since-marker.txt`
   — 572 pipe-delimited rows `ts|job_id|from->to|note`, everything since the
   marker, dream rows excluded. This is your main corpus.
2. **Live cross-check:** `/Users/moses/code/bin/ledger events 200` (newest
   rows; catch anything after the dump was taken at ~2026-09-11T02:33Z).
3. **Per-job deep dives** (`/Users/moses/code/bin/ledger show <id>`) on the
   churn-heaviest rows — recommended list (event counts since marker):
   - `youtube-channel-selva-electrica-assets-rigs` (161)
   - `packet-plumber-3d-planet-life-router-legibility` (136) + its r1-r4 rows
   - `youtube-channel-selva-full-song-storyboard` (45)
   - `packet-plumber-3d-constellation-view` (23) + r1-r5
   - `packet-plumber-3d-main-suite-red-fix` (20) + r1-r2
   - `orchestrator-gemini-storyboard-skill` (19) + r1
   - `packet-plumber-3d-l1-intro-flow` (15) + r1-r3
   - `orchestrator-silas-luna-xhigh` (10)
   - `packet-plumber-3d-test-parse-hotfix` (9) + r1
   - `packet-plumber-3d-shutdown-investigation-glm` (9)
   - `packet-plumber-3d-intro-main-fix` (8) + r1
   - `orchestrator-skill-collision-worktree-fix` (6) + r1
   - `orchestrator-blender-standing-access-2026-09-10` (6)
   - `my-orchestrator-dream-2026-09-09-u1` (5)
   - `packet-plumber-3d-lighthouse-staging-fix` (2), `packet-plumber-3d-l1-arpanet` (2)
   Read `ledger show` for at least the top 8; skim the rest from the dump.

## What to hunt for

1. **Recurring process shapes:** loops that converged cleanly (multi-round
   Perkins arcs), loops that leaked (panes/worktrees left behind, rows left
   open), repeated recovery moves (continues, sweeps, re-dispatches).
2. **Repeated failure/recovery signatures across DIFFERENT jobs** (e.g. the
   bounded-run grant discipline, stop-on-surprise, rebase+push-hold, moot-on-
   merge sweeps, grant-entry exhaustion) — each with job ids + dates.
3. **Ledger hygiene signals:** self-report gaps (NULL `pr` on in-review),
   wrong-row events, phantom rows, notes that claimed things the tool result
   disproved.
4. **Anything counting ≥2 distinct jobs that would make a good store gotcha.**

## Deliverable → your shard file

Markdown, plain and precise:

```
# sheep-ledger — dream-2026-09-11
## Candidate patterns (each: title, ≥2 distinct-job examples = job id + date + one-line quote, why it matters)
## Watch items (single-job anecdotes worth tracking)
## Ledger hygiene findings
## Notes for Bob
```

Do NOT decide store edits — you propose candidates only; Bob consolidates,
verifies, and edits the store copies. When done, write the file, print a
3-line summary, and end your turn. Bob closes your pane.
