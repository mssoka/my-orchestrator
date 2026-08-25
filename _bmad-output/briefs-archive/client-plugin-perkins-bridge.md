# Briefing: orchestrator-dashboard-perkins-bridge

## Task
Make the dashboard's **Perkins section live**. Today it renders as "deferred"
because Perkins round/job data lives server-side in the orchestrator ledger
(SQLite) and no browser-reachable hook exists. Build the **host-side bridge**:
a host half that reads the ledger and a browser half that renders it, shipped in
the SAME package (`dsh-client-plugin-orchestrator-dashboard`), folded onto the
open PR #1 branch `add/orchestrator-dashboard`.

## Context
- Repo: `/Users/moses/code/dsh-client-plugin-orchestrator-dashboard` (branch
  `add/orchestrator-dashboard`, remote `mssoka/dsh-client-plugin-orchestrator-dashboard`,
  PR #1 OPEN — do NOT merge).
- Current state: `lib/index.js` is a **no-op host half** (`export function apply() {}`);
  `lib/client.js` is the built browser bundle (rev `d90e91b9a0f5`, registers the
  `details` slot at `priority: -1`); `src/client/index.js` is the browser source;
  `scripts/build-client.js` wraps it into the lazy-CJS `__ModuleLoader__` format;
  `scripts/verify-scan.js` replicates the host `dsh.client` discovery offline.
  The Perkins section in `src/client/index.js` is labelled deferred — find it.
- **Ledger (the data source):** SQLite at
  `/Users/moses/code/dsh-orchestrator-setup/_bmad-output/orchestrator.db`.
  CLI: `/Users/moses/code/dsh-orchestrator-setup/bin/ledger` (read its head for
  the schema/usage; `ledger show <id>`, `ledger events`). Job rows: `id, repo,
  status (dispatched/clarifying/working/in-review/blocked/done), pr, pr_review,
  started_at, result, note` + `job_events` history. **Perkins round rows are ids
  matching `<job-id>-perkins-rN`.** Read with the sqlite3 CLI read-only
  (`sqlite3 -readonly`); NEVER write the DB from the plugin.
- **The proven out-of-tree host-plugin example:** `orchestrator-nefario` at
  `~/.dsh/profiles/node_modules/orchestrator-nefario/` (symlinked package +
  loader row in `~/.dsh/profiles/web/cordis.patch.yml`). It is the ONLY known
  working external host plugin in this profile — read its source to learn how a
  host half registers, receives config, and (critically) whether/how it exposes
  anything to the browser.
- **Browser↔host RPC lead:** shipped code calls `ctx.remote.pluginInventory.list()`
  from the browser (see `dsh-client-ui-settings-plugin-inventory` in the npx
  cache `/Users/moses/.npm/_npx/1e7f6d9597241db0/node_modules/@deepseek-ai/`).
  Trace how a host plugin declares a remote that the browser can call — that is
  the sanctioned bridge shape. Read `dsh-client-runtime`, `api-remotes`
  references, and the webserver package as needed.

## Approach (investigate, then commit to ONE)
1. **Preferred:** host half declares a remote (e.g. `orchestratorLedger`) exposing
   a read method (job rows + perkins round rows + recent events, JSON-safe); the
   browser Perkins section calls it and renders live.
2. **Fallback (only if remotes are provably unreachable for out-of-tree plugins):**
   the host half snapshots ledger rows to a file the webserver can serve under
   `/plugins/...`, and the browser fetches it — with staleness labelled honestly.
   If NEITHER works, report BLOCKED with evidence; do not fake data.

## Constraints
- **Never restart or kill the running `:3080` host.** Verify with an isolated
  `dsh web --no-open --port <spare>` boot (the prior round proved this works),
  plus `scripts/verify-scan.js`. Node-half changes activate on the USER's next
  restart — say so in the report.
- Read-only on the ledger DB. No writes to `~/.dsh` except if a loader-row/config
  change is REQUIRED for the host half — keep it reversible, back up first, and
  report exactly what changed.
- Do not modify the shipped `dsh-web-frontend` bundle or installed packages.
- Keep the existing four live sections working; bundle purity (react +
  react/jsx-runtime + public ctx surfaces only); styles via `var(--dsw-*)` tokens.
- Rebuild via `npm run build`; `verify-scan.js` must pass; the served rev must
  match the on-disk hash.

## Definition of done
- Perkins section renders live round/job data from the ledger (or an honestly
  labelled fallback), verified by an isolated live boot (HTTP 200 + the data path
  exercised) — not just prose.
- Changes committed + pushed to `add/orchestrator-dashboard` (folds onto PR #1),
  never merged.
- Review: run the 4 lenses (blind-adversarial, edge-case, verification-gap,
  acceptance) as spawned reviewer subagents before reporting done; fold findings.

## Model policy
Minion + lens subagents run on this session's default provider (deepseek); no
bare/`unset` model lines anywhere. Mega-minion allowance: ≤10, close them all.

## Standing orders
Self-report transitions via
`/Users/moses/code/dsh-orchestrator-setup/bin/ledger set orchestrator-dashboard-perkins-bridge <status> "<note>"`.
Commit, push, open/fold PR (never merge). Report honestly — a labelled deferred
section is acceptable; fake live data is not.
