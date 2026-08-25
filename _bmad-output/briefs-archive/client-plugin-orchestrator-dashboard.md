# Briefing: dsh-client-plugin-orchestrator-dashboard

## Task
Add a **right-hand orchestrator dashboard panel** to the DSH Web GUI (the app at
`http://127.0.0.1:3080`, run by `node .../@deepseek-ai/dsh web`) that surfaces the
live orchestration state the user cares about. The user's words: *"I want the UI
dashboard on the right with those details."* Panel must show (all five):
1. **Minions** — dispatched task agents with status (working/inactive), parent↔child.
2. **Mega-minions** — specialist helpers a minion spawned (depth below a minion).
3. **Perkins** — active/last `perkins-review` rounds (`<job-id>-perkins-rN`: in
   flight / verdict / APPROVED | CHANGES_REQUESTED | INFO_ONLY).
4. **Jobs** — background jobs in flight (producer kind, status, elapsed).
5. **Any other useful signal** — session count, running agents, goal/objective
   status, token/quota, a compact activity feed (best-effort; pick what a live
   hook provides and label what's synthetic).

## Context
- **This is a build of a runtime *client-plugin* for the DSH web app — the plugin is
  the deliverable, and the panel must actually appear in the running GUI when the
  plugin is loaded.** It is NOT a packet-plumber/game change.
- The web app is a **cordis slot system**. `dsh-client-ui-layout` owns a
  three-column `AppFrame` (`sidebar` / `conversation` / `details`). **The right-hand
  surface to inject into is the `details` column.**
- A client-plugin is a **`dsh.client` browser half** packaged as a lazy-CJS factory
  bundle: `window.__ModuleLoader__.load({id, factory})` registers it; bodies run at
  materialization. The host scans enabled Loader entries for web `dsh.client`
  packages, hashes each built bundle into the boot graph, and serves it under
  `/plugins`. Registration is via a cordis contribution using **`ctx.slots.inject()`**.
- Reference packages (read their README + built JS in the npx cache
  `/Users/moses/.npm/_npx/1e7f6d9597241db0/node_modules/@deepseek-ai/*`):
  `dsh-client-ui-layout` (details slot), `dsh-client-ui-subagent`
  (`subagentsByParent` via `useSessions`), `dsh-client-ui-jobs` (`jobsBySession`),
  `dsh-client-runtime`, `dsh-client-modules`, `@deepseek-ai/dsh-client-hmr`,
  `dsh-client-ui-settings-plugins` / `-inventory` (the plugins UI).
- Perkins round data lives on the orchestrator's **ledger**
  (`/Users/moses/code/_bmad-output/orchestrator.db`, CLI `bin/ledger`), not in the
  web UI. A "Perkins" panel row that shows live round state likely needs a
  host-side/data bridge — implement the BEST available from the browser, and if
  nothing is live, label it clearly (see Constraints) rather than inventing it.
- Web app state/config: `/Users/moses/.dsh` (profiles, settings.yaml).

## Constraints (non-goals)
- Do NOT modify the shipped minified `dsh-web-frontend` bundle or the installed
  packages in the npx cache (read them only as reference).
- Do NOT destructively edit `~/.dsh` settings or restart the running dsh server
  without reporting exactly what you changed and keeping it reversible.
- If a live data hook for a section (esp. Perkins) is not reachable from the
  browser, render that section in a clearly-labelled best-effort/deferred state
  and SAY SO — do not fake data.
- Style with the existing design tokens (match `dsh-client-ui-*` conventions);
  do NOT import shipped UI chrome as values (the bundle-purity gate).

## Definition of done
- **Feasibility FIRST**: prove an external client-plugin can be built in this
  environment, discovered + loaded by the host, and injected into the `details`
  column. If that can't be shown, report BLOCKED with the exact reason — do not
  fake a plugin.
- If feasible: produce a clean buildable plugin (new repo, e.g.
  `/Users/moses/code/dsh-client-plugin-orchestrator-dashboard`) that renders the
  five-section dashboard in the `details` column, with the load/reload steps
  documented so it can be verified in the running GUI.
- `pr_review: 1` (large/risky — it's an extension of the harness UI): the reviewer
  (Perkins) is required + tracked before close-out.
- Commit + push the plugin repo; do NOT merge.

## Review policy (MANDATORY)
`baseline_commit: <n/a — new repo>`. Run the review layers (blind-adversarial,
edge-case-hunter, verification-gap, acceptance) as spawned reviewer subagents
before reporting done; record the verdict in the ledger.

## Standing orders
Follow the orchestrator playbook "Minion standing orders": use the bmad-build
skill; clarify questions halt for relay; close any panes you spawn; self-report
transitions via `bin/ledger set dsh-client-plugin-orchestrator-dashboard <status>`;
commit, push, open PR (never merge). This is a CODE deliverable — keep the regular
PR pattern, no lavish loop.

## Model policy
Stay on the model this pane was launched with. Spawn mega-minion reviewer
subagents as needed (max 10 concurrent); close every one when done ("badge out").
