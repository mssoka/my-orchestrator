# Briefing — dsh-dashboard-perkins-cap (UI: cap the Perkins done-rows)

Skill: bmad-quick-dev (if absent from your catalog, follow this brief — it is
self-contained). Model note: DSH session default; pin explicitly on any
mega-minion spawn and record it.

## Repo

/Users/moses/code/dsh-client-plugin-orchestrator-dashboard
Branch: add/orchestrator-dashboard (PR #1 is OPEN from this branch — your push
folds onto it; do NOT open a new PR). Work directly in this checkout (it is
the plugin's own repo, not the orchestrator root).

## Problem (user ruling 2026-08-25)

The dashboard's Perkins section renders `rounds.slice(0, 10)` regardless of
status (src/client/index.js, PerkinsRows, ~line 174) — done rounds accumulate
and eat the right column. User: "i don't think we need to see more than 2 done
reviews, or if we need to see the done ones."

## Task

In PerkinsRows:
1. Add a module-level constant `PERKINS_DONE_SHOWN = 2` (one-line flip to 0
   later if the user rules done-rounds out entirely).
2. Split rounds: OPEN rounds (status !== "done") always all shown; DONE rounds
   capped at the PERKINS_DONE_SHOWN most recent.
3. Ordering: verify what the host snapshot returns (check the query in
   lib/index.js — if rounds are not newest-first, sort client-side by
   started_at desc before capping; numericTime() helper exists).
4. The overflow line becomes: `+ <N> older done rounds (bin/ledger for full
   history)` — only when done rounds were hidden. Keep row keys stable, keep
   the header/status row and the empty/loading/error states untouched.
5. Keep open rounds' relative order and their status tags/dots as-is.

## Verify (all must pass)

```bash
node scripts/build-client.js
node scripts/verify-scan.js
node scripts/verify-client-harness.cjs
```

## Deliverable

Single commit on add/orchestrator-dashboard, push to origin. Message:
"perkins: cap done rounds at 2 in dashboard (open rounds always shown)".

Ledger self-report: /Users/moses/code/dsh-orchestrator-setup/bin/ledger
- Row id: dsh-dashboard-perkins-cap (Gru pre-registers it).
- `ledger set dsh-dashboard-perkins-cap working "reading PerkinsRows"` at start.
- On push: `ledger set dsh-dashboard-perkins-cap done "pushed <short-sha> onto PR #1 branch; verify green"` (this is a no-PR job folding onto PR #1 — the done + note IS the completion signal).
- Final message: commit sha, verify results, the ordering you found (host-side
  or client-side sort).

Note: the user must restart `dsh web` to see the new bundle (rev hashed at
boot) — mention nothing in the PR, just report it back.
