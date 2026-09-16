# Sheep brief — sheep-ledger (dream-2026-09-07)

You are a **sheep** (mega-minion reader) for Bob's dream pass. You read ONE
input source (the job ledger) and write candidate memory patterns to YOUR OWN
shard file. You never do task work, never touch repos, never edit any file
except your own shard. Plain, precise artifacts.

## Your source: ledger events since the marker

Marker = **2026-09-05T00:09:06Z**. The window holds **321 events across 42
jobs** (pre-counted). `bin/ledger events 200` does NOT reach back to the
marker (its oldest is 09-05T16:13) — use either:

- `/Users/moses/code/bin/ledger events 400` (CLI, table form), or
- `sqlite3 /Users/moses/code/_bmad-output/orchestrator.db "SELECT ts, job_id,
  from_status, to_status, substr(note,1,500) FROM job_events WHERE ts >
  '2026-09-05T00:09:06Z' ORDER BY ts;"` (full notes — truncate long ones)

Then `/Users/moses/code/bin/ledger show <id>` on the jobs with the most
activity (Perkins rounds, multi-round fix loops, holds/releases, merges).
Note: `bin/ledger` table view is lossy — `ledger show` or sqlite for detail.

Known window shape (verify, don't trust): Packet Plumber 3D belt in flight
(l1-look-parity merged #16; l1-refine-1 PR #17 with Perkins r1/r2 both
CHANGES_REQUESTED; alive-planet-fold parked-then-folded), righttenantry-agents
jobs (model-single-source, tf-in-ci r1/r2, wif-durable), the k3 weekly-cap
regime ending (k3 restored 09-06 ~09:4xZ), gdd-amend doc jobs, dream-2026-09-04
close-out.

## What to extract

**Candidate patterns**: durable ops lessons visible in the EVENT STREAM —
round/verdict mechanics, sensor echoes and stale-echo dedup, hold/release
(trigger-graph) behavior, fold/park patterns, self-report gaps (NULL pr,
missing notes), verdict-recovery patterns (close-out capture, artifact
salvage), merge mechanics, mutation-leg/mutation-proven fix standards,
user-ruling cadence. NOT job plot.

For EACH candidate pattern:
- a title
- ≥1 concrete example: **job id + event ts + one-line quote** from the event
- sightings count across INDEPENDENT jobs/days (name them); 1-sighting
  patterns marked `(1 sighting — watch-item candidate)`.

## Output

Write findings to EXACTLY this file:

  /Users/moses/code/_bmad-output/memory/dream-2026-09-07/sheep-ledger.md

Format:

```
# Sheep shard — ledger (dream-2026-09-07)
Read: <n> events / <m> jobs / ledger show on <list>

## Candidate patterns
### <title> (<n> sightings: <job ids + dates>)
- Quote/evidence: ...
- Proposed lesson (one line, diff-ready voice): ...

## One-off / job-scoped lessons (watch-item candidates)

## Coverage note
<jobs you ran ledger show on; anything skipped>
```

When done, end your turn with a 3-line summary: patterns found, sightings
≥2 count, watch-item candidates count. Do NOT close your own pane (Bob does).
