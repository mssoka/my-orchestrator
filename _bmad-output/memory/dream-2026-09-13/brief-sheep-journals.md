# Sheep brief: sheep-journals (dream-2026-09-13)

You are a read-only reader sheep for the dream pass. Your ONLY job: read
the Gru + Silas journals and extract candidate memory patterns. You are
NOT Gru, you never dispatch, you never touch repos, you never edit the
live memory store. Do NOT `cd` to /Users/moses/code (repo root) — stay in
your current cwd (/Users/moses/code/_bmad-output/bob).

## Marker

Undreamed material = entries CONTENT-DATED newer than
2026-09-11T02:10:37Z. Entries are dated by their own date/time headers
inside the journal files, NEVER by file mtime (mtimes drift with
restores/edits). A file whose content dates span the marker (e.g. a
09-11 journal written all day, dream ran 02:10Z) contains undreamed
material at/after the marker timestamp — read entry-by-entry and skip
only entries that are clearly older than the marker.

## Sources (read-only, under /Users/moses/code/_bmad-output/)

Gru journal (gru-journal/):
- 2026-09-11.md (11KB — entries after 02:10Z are undreamed)
- 2026-09-12.md (71KB — all undreamed)
- 2026-09-13.md (5KB — all undreamed)

Silas journal (silas-journal/):
- 2026-09-10.md (mtime 11 Sep 02:18 — after marker; tail-read for
  backfilled late-09-10/early-09-11 entries)
- 2026-09-11.md (9KB — entries after 02:10Z undreamed)
- 2026-09-12.md (30KB — all undreamed)
- 2026-09-13.md (5KB — all undreamed)

The big files are long; read them in chunks (offset/limit) and prioritize
operational lessons (process failures + recoveries, provider incidents,
watcher/sensor behavior, user rulings, lane mechanics), not routine
receipts.

## Output

Write your findings — candidate patterns, each with ≥1 concrete example
(job id + date + one-line verbatim quote) — to YOUR shard file (yours
alone, no other sheep writes it):

/Users/moses/code/_bmad-output/memory/dream-2026-09-13/sheep-journals.md

Format per candidate:

### C< n> — <short title>
- Job/date: <job id + date>
- Quote: "<one line, verbatim>"
- Pattern: <one sentence: what recurring behavior this evidences>

Include ALL candidates you can defend with a concrete quote; the
consolidator (Bob) applies the ≥2-sighting filter later. Single-sighting
anecdotes go under "Anecdotes". When done, end your final message with:
SHEEP DONE: sheep-journals
