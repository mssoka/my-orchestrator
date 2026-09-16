# sheep-shards shard — dream-2026-09-15

Reader sheep: sheep-shards. Sources per brief (marker 2026-09-13T03:03:31Z):
dream-2026-09-13.md read fully (3 entries, written minutes after the marker
per brief — post-marker); tail-reads of 3 named shards + the 10 newest-by-mtime
other .md files in field-notes/. Additional verification: `grep -l -E
'2026-09-1[345]' *.md` across the WHOLE field-notes dir matches ONLY
dream-2026-09-13.md — no late appends exist anywhere in the store.

## Candidate patterns

### Grep-verify every verbatim quote before it enters a dream proposal
- Evidence: dream-2026-09-13, header `2026-09-13` — "sheep-quote fidelity check pays — 4 of ~30 shard quotes failed verbatim grep (paraphrase); one candidate (row-staleness) dropped for lack of verbatim primary evidence, two re-quoted from ledger verbatim before promotion. Grep EVERY quote before it enters a proposal."
- Sighting count: 1 (dream-2026-09-13 post-marker; ~13% failure rate on its own pass — 4/~30)
- Why it matters: sheep/bob prompts must run each Evidence quote through grep against the source file before promotion; a paraphrased quote silently invalidates the candidate (this shard's quotes below were copied from a fresh read, same discipline).

### Census the merged base before adding canon/store pointers
- Evidence: dream-2026-09-13, header `2026-09-13` — "check origin/main BEFORE adding canon pointers — the 09-12 autonomy/factory rulings were already codified (PRs #34/#35); a store addendum would duplicate at root activation. Census the merged base, then decide no-edit."
- Sighting count: 1 (dream-2026-09-13; sibling of the AGENTS.md "MERGED ≠ DELIVERED ≠ ACTIVATED" class — activation lag makes merged-but-unseen canon look absent)
- Why it matters: before writing any "add X to the memory store" proposal, grep origin/main (not the live checkout) for X — duplication at root activation is the failure this avoids.

### Dream intake keys on job_events timestamps (not started_at) + pre-dump for the sheep
- Evidence: dream-2026-09-13, header `2026-09-13` — "the job_events-ts census (not started_at) recovered 9 active rows a started_at window drops — 3rd consecutive dream; keep keying intake on event timestamps, and pre-dump to the file for the sheep."
- Sighting count: 3 (dream-2026-09-13 post-marker; pre-marker corroboration in dream-2026-09-11 header `2026-09-11` — "pre-dump the post-marker ledger events read-only to a file for the sheep (sqlite SELECT > txt); the latest-200 window again missed ~370 interval rows" and dream-2026-09-09 header `2026-09-09` — "read-only timestamp census + per-job show recovered 414 non-self events across 25 jobs without treating event rows as independent sightings")
- Why it matters: three consecutive dreams lost rows to the latest-200/started_at windows — the standing intake shape is: read-only job_events timestamp census + per-job `ledger show`, dumped to a file for the sheep BEFORE spawning them.

## Negative results (tail-reads, nothing after marker)

- tail-read wire-aesthetics.md: nothing after marker (latest entry 2026-08-19).
- tail-read righttenantryagents-model-flash.md: nothing after marker (entries undated; file mtime 25 Aug 16:49 — pre-marker by months). NOTE: brief's filename resolved exactly; a sibling file righttenantry-agent-model-flash.md (hyphenated, different content) also exists — do not conflate.
- tail-read youtube-channel-selva-assets-rigs.md: nothing after marker (latest entry 2026-09-07).
- 10 newest-other tail-reads — dream-2026-09-11.md (09-11), dream-2026-09-09.md (09-09), packet-plumber-3d-typography-video-study.md (09-08), dream-2026-09-07.md (09-07), righttenantry-agents-wif-durable.md (09-06), packet-plumber-3d-l1-topology-font.md (09-05), packet-plumber-3d-gdd-amend-alive-planet.md (09-05), righttenantry-agents-tf-in-ci.md (09-05), packet-plumber-3d-gdd-amend-era-planets.md (09-05), righttenantry-agents-model-single-source.md (09-05): nothing after marker in any.
- Whole-store grep for `2026-09-1[345]` across all field-notes/*.md: matches only dream-2026-09-13.md → zero late appends store-wide; the 09-13/14/15 window left no other shard traces (the selva/PP3D activity of 09-12..14 has not yet been badge-outed into shards — a possible intake gap for a future pass, not a defect of this one).
