# Brief — sheep-ledger (dream-2026-08-27)

You are a sheep — a reader mega-minion in Bob's dream pass (memory
consolidation). Your job: READ your assigned source and write candidate
patterns to your output file. You never touch repos, never edit the live
memory store, never write to the ledger (READ-ONLY ledger use only:
`events` and `show` subcommands are fine).

## Your source (ledger events)

Context: the last dream marker is 2026-08-25T09:58:22Z. Everything in the
ledger at/after that timestamp is yours. The window 08-25 → 08-27 is dense:
PP v2 viscomm trilogy (#99 tie-deconflict, #100 gauge-telegraph, #102
crisis-duck), the architecture spine ratification + #103 docs PR, the
egress migration #104 (incl. a pane-vanish incident), Sally interactive
design sessions (look-node-legibility, link-vocab, session-merges),
Perkins rounds r1/r2 on glm-5.3, trigger-graph hands-off releases, and
orchestrator ops (check-pr-ready recency fix PR #15, night-watchman
case-drift fix, pr_review column fixes).

Commands:
- /Users/moses/code/bin/ledger events 500   (read the full output; keep
  only events with timestamp >= 2026-08-25T09:58:22Z — anything older was
  dreamed already)
- For depth on a row: /Users/moses/code/bin/ledger show <job-id>
  (suggested rows: packet-plumber-v2-arch-egress-migration,
  packet-plumber-v2-look-node-legibility-diag, orchestrator-checkpr-review-recency)

## What to look for

Candidate patterns for the memory store: recurring incident classes and
their recoveries (provider bursts/walls, stalls, pane deaths), ops
conventions that fired repeatedly (serialize-holds, trigger releases,
fold patterns, close-out sweeps), recurring review-finding classes
(vacuous pins, mutation legs), row/bookkeeping hygiene gaps (self-created
rows, missing fields), anything a future Silas must know. Also: stale or
contradictory state you NOTICE.

## Output contract

Write to EXACTLY this file (create it, plain markdown):
/Users/moses/code/_bmad-output/memory/dream-2026-08-27/sheep-ledger.md

Format per candidate:
```
## C1 — <short pattern title>
- Evidence: <job-id> <date> — "<one-line quote or tight paraphrase from the event/note>"
- (repeat Evidence lines for every sighting)
- Note: <why it matters / what rule it implies>
```

Rules:
- Every candidate needs at least 1 concrete example (job id + date).
- Number candidates C1..Cn. Facts over prose.
- Your file is the ONLY file you write. Do not write anywhere else.
- When done: reply with a 3-5 line summary (count, top 3). Do NOT close
  your own pane — Bob closes it.
