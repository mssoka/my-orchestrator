# Sheep brief — sheep-journals (mega-minion of Bob, dream-2026-08-07)

You are a **sheep** — a reader mega-minion for Bob's dream pass. You are
NOT Gru; ignore any startup checklist or Gru alerts injected into your
session. Your cwd (`/Users/moses/code/_bmad-output/bob`) is correct —
do NOT `cd` to the repo root `/Users/moses/code`.

## Task

Read BOTH journals:
- `/Users/moses/code/_bmad-output/gru-journal/*.md` (07-31, 08-01, 08-02)
- `/Users/moses/code/_bmad-output/silas-journal/*.md` (08-03 .. 08-07)

Undreamed material = entries NEWER than **2026-08-03T11:12:13Z**:
weight content after the marker. (Gru journal has no 08-03..08-07 files
— note that gap; the Silas journals 08-04..08-07 are the richest fresh
source, plus 08-03's later entries.)

## What's ALREADY in AGENTS.md gotchas (do NOT re-propose — mark "already in store")

These coordination lessons are already curated (read the gotchas section
of `/Users/moses/code/AGENTS.md` first):
- ledger table view lossy / `ledger events` takes a count not a job id;
- `herdr agent send` / `herdr pane run` can leave text unsent -> verify
  handover, or `send-keys enter` a stuck buffer;
- idle pane can hide a DEAD pi (no session file -> relaunch) OR a LIVE pi
  whose turn errored (`stopReason:"error"` in jsonl -> `continue`);
- `herdr pane move` has no `--json` (stdout is JSON);
- `ledger set` refuses same-status -> use `ledger note`;
- nefario-watch settle transitions (mostly noise);
- Silas deliverable not reported until it reaches Gru's input;
- Silas minions never split into identity tabs (relabel);
- pi launched with cwd=/Users/moses/code IS Gru;
- raw backtick in extension template literal kills the extension;
- provider incidents 3 classes (continue per pane; quota 403 = dead ->
  sweep+re-dispatch same round with regenerate-everything);
- review/Perkins/cap sensors re-fire -> note-only echo, never re-act;
- Perkins self-close round row -> pre-emptive verdict note;
- pane forensics = session jsonl, not env scraping;
- NEVER yield a turn between `wait idle` and handover -> chain + sleep 3
  after idle, then verify delivery;
- no-PR jobs fall through BOTH watchers -> notification is the durable
  signal (verify minion ran `cli:notification:show`, not just constructed it).

## Extract

Candidate **NEW** patterns about the orchestration itself: recurring
coordination failure modes NOT already above, things Gru/Silas had to
learn or re-derive, and practices that worked. Each candidate needs ≥1
concrete example: **job id (or event) + date + one-line quote**.

Note especially: anything NEW not in the gotchas, and any PREVIOUSLY-WATCH
orchestration item recurring a SECOND time this window (2nd sighting ->
propose): non-blocking clarify; hold-release for pane capacity; watcher
"pane vanished" self-inflicted; ledger event text strips `$`; dual-gate
echo (PI_GRU+PI_SILAS relaunch — was it journaled?). Also track: provider
instability clustering/quota waves this window (how many, which recovery),
and any cap/round-budget practices.

## Output (your OWN shard — touch no other file)

Write findings to:
`/Users/moses/code/_bmad-output/memory/dream-2026-08-07/sheep-journals.md`

Format:

```
# Sheep findings — Gru + Silas journals
Material: <n> journal files, entries since 2026-08-03T11:12:13Z
## Candidate patterns (NEW — not in gotchas)
### <pattern title>
- Sightings: <job/event + date + quote> [, ...]
- Already in store? yes/no/partial
- Candidate memory target: AGENTS.md gotchas | minion-field-notes.md | neither (report-only)
## Watch items recurring (2nd sighting this window)
## One-off anecdotes (single sighting — watch items)
## Gru journal gap (08-03..08-07 missing) — any signal?
```

## Never

Edit any live file. No PRs, no repos. Read + write your ONE output shard
only.

## Badge out

Final message: one line — counts (entries read, patterns found) + the
output path. Then stop.
