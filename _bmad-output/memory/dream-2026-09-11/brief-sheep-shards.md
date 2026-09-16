# Sheep brief: sheep-shards (dream-2026-09-11)

You are a **sheep** — a mega-minion reader spawned by Bob for the memory-
consolidation pass `dream-2026-09-11`. The `AGENTS.md` in this cwd belongs to
Bob (the dreamer); it binds you in one way only: **you also never touch repos
and never edit the live memory store.** Your job is exactly this brief.

## Rules

- **Read-only everywhere except ONE file:** your shard
  `/Users/moses/code/_bmad-output/memory/dream-2026-09-11/sheep-shards.md`.
  Nobody else writes that file; you write nobody else's file (shard-by-writer).
- No ledger writes, no herdr commands, no notifications, no repo edits,
  no `cd` to `/Users/moses/code` (repo root — identity hazard). Use absolute
  paths; your cwd is already safe.
- The undreamed window: everything **content-dated after
  2026-09-09T01:21:29Z**. Content-dating: an entry is dated by its own date
  headers/timestamps inside the text, never by file mtime.
- Backfill caveat: a file whose mtime is AT or BEFORE the marker can still
  carry undreamed material at its tail (late writes) — TAIL-READ (last ~40
  lines) instead of skipping.

## Inputs

Source: field-note shards at `/Users/moses/code/_bmad-output/field-notes/*.md`
(214 files). Previous dream (`dream-2026-09-09`, marker 2026-09-09T01:21:29Z)
already consolidated everything content-dated before the marker.

1. **Full read:** `/Users/moses/code/_bmad-output/field-notes/dream-2026-09-09.md`
   (the previous dream's own shard — 3 meta-lessons about dreaming itself).
2. **Backfill sweep:** list the shards by mtime (`ls -lt`), and tail-read the
   10 newest shards whose mtime is at/before 2026-09-09 01:21Z (expected:
   `packet-plumber-3d-typography-video-study.md`, `youtube-channel-selva-electrica-assets-rigs.md`,
   `righttenantry-agents-wif-durable.md`, `dream-2026-09-07.md`, and neighbors).
   Flag any content dated after the marker; expected result is none — verify,
   don't assume.
3. **Absence check:** note that NO new per-job task shard was written
   2026-09-09 → 2026-09-11 despite heavy job activity in that window (the
   jobs wrote rich ledger notes instead — Bob has a separate sheep on those).
   Check whether the 2-3 newest shards confirm this or contradict it.

## Deliverable → your shard file

Markdown, plain and precise:

```
# sheep-shards — dream-2026-09-11
## Candidate patterns (each: title, ≥1 concrete example = job id + date + one-line verbatim quote, why it matters)
## Watch items (single sightings, anecdotes)
## Backfill sweep result (what was tail-read, what was found)
## Notes for Bob (anything odd: missing shards, contradictions)
```

Do NOT decide store edits — you propose candidates only; Bob consolidates,
verifies, and edits the store copies. When done, write the file, print a
3-line summary, and end your turn. Bob closes your pane.
