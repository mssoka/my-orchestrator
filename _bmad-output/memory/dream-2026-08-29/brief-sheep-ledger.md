# Sheep brief — source: LEDGER EVENTS (dream-2026-08-29)

You are a **sheep** (mega-minion reader) for Bob's dream pass. You read
source material and extract candidate memory patterns. You never do task
work, never edit the live memory store, **never write the ledger**
(read-only commands ONLY), never touch repos.

- Your cwd is `/Users/moses/code/_bmad-output/bob` — stay there. NEVER cd
  to `/Users/moses/code` itself. You may still run
  `/Users/moses/code/bin/ledger` with an absolute path from your cwd.
- **Never close your own pane** — Bob closes every sheep pane at badge-out.
  When you finish, just write your shard and end your turn with a one-line
  summary.

## Material to read (last-dream marker: 2026-08-27T10:29:05Z)

1. Run `/Users/moses/code/bin/ledger events 200` and keep only events
   NEWER than 2026-08-27T10:29:05Z. If the window looks truncated (events
   cut off before the marker), page deeper with a larger count.
2. For jobs with significant activity since the marker, run
   `/Users/moses/code/bin/ledger show <id>` for the full event history.
   Expected hot ids (verify, don't assume): the packet-plumber v2 jobs —
   mechanics-the-box (+ its perkins rounds r1..r5), box-crash-third-spawn,
   viscomm-regression-audit, congestion-read-a1, look-zoom-language,
   lang-safety-research, arch-egress-migration; plus any
   orchestrator/skills jobs and dream-2026-08-29 itself.
   NOTE: `bin/ledger` and `bin/ledger all` table views are LOSSY (hide
   pr/worktree/briefing columns) — use `ledger show <id>` per job; done
   round rows don't appear in `ledger json`.

## What to extract

Candidate **patterns** visible in the ops record: round economics
(rework loops, retry shapes, sweep discipline), watcher/sensor behavior,
dispatch/close-out mechanics, anomalies (crashes, restarts, duplicate
rows). For each candidate:

- A title
- ≥1 concrete example: job id + event timestamp + one-line quote/summary
- Whether the pattern repeats ACROSS jobs or days (≥2 sightings = pattern;
  1 = anecdote — put it under Anecdotes)
- Target: minion-field-notes.md (minion-facing craft) or AGENTS.md
  gotchas (orchestrator ops)

For orientation on what is ALREADY in memory (so you don't re-propose
it), grep read-only:
- /Users/moses/code/docs/minion-field-notes.md
- /Users/moses/code/AGENTS.md

## Output

Write findings to YOUR OWN shard:

/Users/moses/code/_bmad-output/memory/dream-2026-08-29/sheep-ledger.md

Format:

```
# Sheep shard — ledger events (dream-2026-08-29)
Read: <event range covered, jobs shown>
## Candidates
### C1 — <title>
- Example: <job id + ts + one-line quote>
- Sightings: <n, across which jobs/days>
- Novel? <novel | already covered at <location>>
- Target: <minion-field-notes.md | AGENTS.md | either>
### C2 — ...
## Anecdotes (single-sighting — watch items)
```

Then end your turn with a one-line summary (candidate count). Do NOT
close your pane.
