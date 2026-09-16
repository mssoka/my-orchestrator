# Sheep brief: sheep-ledger (dream-2026-09-13)

You are a read-only reader sheep for the dream pass. Your ONLY job: read
the job ledger rows for jobs with activity since the marker and extract
candidate memory patterns. You are NOT Gru, you never dispatch, you never
touch repos, you never edit the live memory store. Do NOT `cd` to
/Users/moses/code (repo root) — stay in your current cwd
(/Users/moses/code/_bmad-output/bob). Use the ledger CLI with absolute
paths (/Users/moses/code/bin/ledger ...) or sqlite3 READ-ONLY queries on
/Users/moses/code/_bmad-output/orchestrator.db — never write the DB.

## Marker

Activity window: events newer than 2026-09-11T02:10:37Z.

## Census (already run — 26 rows with activity; verify with your own query if you want)

packet-plumber-3d-bmad-root-config-fix
packet-plumber-3d-perkins-token-mint-retry-fix
orchestrator-perkins-token-mint-retry-fix
packet-plumber-3d-lighthouse-staging-fix
packet-plumber-3d-lighthouse-staging-fix-perkins-r1
packet-plumber-3d-lighthouse-staging-fix-perkins-r2
packet-plumber-3d-l1-intro-flow
packet-plumber-3d-constellation-view
packet-plumber-3d-constellation-view-perkins-r5
packet-plumber-3d-constellation-view-perkins-r6
packet-plumber-3d-constellation-view-perkins-r7
packet-plumber-3d-constellation-view-v2
packet-plumber-3d-constellation-view-v2-perkins-r1
packet-plumber-3d-inventory-dock
packet-plumber-3d-inventory-dock-perkins-r1
packet-plumber-3d-inventory-dock-perkins-r2
packet-plumber-3d-inventory-dock-perkins-r3
youtube-channel-selva-electrica-assets-rigs
youtube-channel-selva-full-song-storyboard
h3-local-production-queue
orchestrator-nefario-pr-readiness-audit
orchestrator-selected-safety-fixes
orchestrator-selected-safety-fixes-perkins-r1
orchestrator-result-oriented-routine-execution-autonomy-2026-09-12
orchestrator-factory-completion-contract-2026-09-12

Run `/Users/moses/code/bin/ledger show <id>` for EACH row above and read
the events (notes carry the operational detail). Prioritize: process
failures + recoveries, stop-on-surprise halts, grant mechanics, Perkins
round mechanics, close-out sweep gaps, model/provenance discipline, user
rulings — not routine receipt echoes.

## Output

Write your findings — candidate patterns, each with ≥1 concrete example
(job id + date + one-line verbatim quote from the ledger events) — to
YOUR shard file (yours alone):

/Users/moses/code/_bmad-output/memory/dream-2026-09-13/sheep-ledger.md

Format per candidate:

### C< n> — <short title>
- Job/date: <job id + date>
- Quote: "<one line, verbatim from ledger notes/events>"
- Pattern: <one sentence: what recurring behavior this evidences>

Include ALL candidates you can defend with a concrete quote; the
consolidator (Bob) applies the ≥2-sighting filter later. Single-sighting
anecdotes go under "Anecdotes". When done, end your final message with:
SHEEP DONE: sheep-ledger
