# Briefing: orchestrator-dashboard-active-filter

## Task
The dashboard's **Minions** and **Mega-minions** sections currently list every
descendant session including finished/inactive (`ready`, storage-only) ones.
Filter them to show **only active minions/mega-minions** — the user ruling:
"can the dashboard then show only active minions/megaminions?" Auto-closing was
considered and rejected (storage-only agents cost disk only; resumability is a
feature); the FILTER is the fix.

## Context
- Repo: `/Users/moses/code/dsh-client-plugin-orchestrator-dashboard`, branch
  `add/orchestrator-dashboard` — **resolve the fresh HEAD first** (the Perkins
  bridge lands before you start; rebase-free: branch off the bridge's pushed
  head). PR #1 OPEN — fold onto the branch, never merge.
- Data: minions = `useSessions(s => s.subagentsByParent[sessionId])`; each
  entry carries `activity` (e.g. `running` / inactive) and the catalog shows
  "ongoing activity when any counted descendant is running". Mega-minions =
  `subagentsByParent[minion.id]` (depth-2).
- The Perkins bridge (same repo, immediately prior) may have changed
  `src/client/index.js` and the host half — read the current file state, do not
  assume the pre-bridge shape.

## Requirements
1. **Minions section**: only entries with live activity (self or any descendant
   running). Inactive rows hidden — NOT just dimmed.
2. **Mega-minions**: only minions with live children render an expandable row;
   a minion whose mega-minions all finished shows no mega-minion children.
3. **Counters stay honest**: header counts (e.g. "3 minions") must reflect the
   ACTIVE count; if a "hidden inactive" indicator is trivial (e.g. "+2 done"),
   include it — otherwise omit counts for hidden rows entirely. Never show a
   count of things not listed.
4. **Empty state**: when nothing is active, render a clear "no active minions"
   state — never a blank panel.
5. Rebuild (`npm run build`), `verify-scan.js` green, bundle purity + design
   tokens as before; the Perkins section and the other live sections must keep
   working (the bridge landed first — verify it still renders).
6. A **browser-refresh alone** must suffice to see the change once the host has
   the new rev hashed at boot — but note the activation step honestly in the
   report (refresh if the host already booted the new bundle, else restart).

## Constraints
- NEVER restart/kill the running `:3080` host; isolated spare-port boot only
  for verification (fetch boot graph + bundle HTTP 200 + served rev == on-disk
  hash), killed after.
- No `~/.dsh` edits needed for this job (loader row + symlink already exist).
- Commit + push to `add/orchestrator-dashboard` only.

## Definition of done
- Filter implemented per the requirements, pushed; isolated-boot verification
  output included (bundle served at the new rev).
- 4-lens review (blind-adversarial: does the filter hide something actively
  running? edge-case: all-inactive, mixed, race at settle time; verification-gap:
  is the active-detection actually exercised?; acceptance vs this brief), findings
  folded.
- Ledger self-report transitions (below).

## Model policy
Minion + lenses on this session's default provider; no unset model lines.

## Standing orders
Self-report via
`/Users/moses/code/dsh-orchestrator-setup/bin/ledger set orchestrator-dashboard-active-filter <status> "<note>"`.
Commit, push, fold onto PR #1 (never merge).
