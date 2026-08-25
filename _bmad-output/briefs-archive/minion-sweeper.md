# Briefing: orchestrator-minion-sweeper

## Task
Automate the closing of **inactive minions / mega-minions**. The user ruling:
"this is an orches so it should be automated." Build a host-side plugin
(`orchestrator-minion-sweeper`) that periodically closes minion sessions that
are provably inactive — so stale `ready` (storage-only) agents stop
accumulating in the registry without Gru manually sweeping.

## Context
- **Pattern to copy:** `~/.dsh/profiles/node_modules/orchestrator-nefario/` —
  the ONE proven out-of-tree host plugin in this profile. Read its source for:
  package layout (node half `lib/index.js` with a real `apply(ctx)`), how it
  receives config from the loader row, how it runs a timer (`pollMs`), how it
  sees sessions, and how it logs. Mirror its shape exactly.
- **Loader registration:** symlink into `~/.dsh/profiles/node_modules/` + a
  loader row in `~/.dsh/profiles/web/cordis.patch.yml` (see the existing
  `orchestrator-nefario` row for the format). Back up the yml first; keep every
  `~/.dsh` edit reversible and report it.
- **What a minion IS here:** every dispatched subagent (minion) and every
  subagent it spawned (mega-minion) is a session in DSH storage
  (`~/.dsh/sessions/--Users-moses-code--/...`). Agent registry statuses:
  `running` (live turn), `idle` (loaded, between turns — may be waiting on
  children), `ready` (STORAGE-ONLY, no process, resumable). "Inactive" =
  storage-only, i.e. `ready`.
- **Session deletion mechanism (investigate, prefer safest):** the web UI's
  session browser can delete sessions — trace the RPC it uses (shipped
  `dsh-client-ui-workspace` in the npx cache
  `/Users/moses/.npm/_npx/1e7f6d9597241db0/node_modules/@deepseek-ai/`) and
  whether a host plugin can call the same underlying storage API. Fallback:
  direct storage prune (delete the session's storage entry). Never invent a
  third mechanism.

## Sweep gates (ALL must hold — hard invariants, no heuristics past these)
1. **Storage-only only.** Every agent in the target session's tree must be
   `ready` (no live process anywhere in it). If ANY is `running` or `idle` → skip.
   An `idle` agent may be waiting on children it spawned — never close it.
2. **Never the orchestrator's own session.** Never close the Gru session
   (identify via config `preserve` list + never the newest active session).
   Mega-minions close WITH their parent's tree, never alone.
3. **Age threshold.** Last activity older than `ttlHours` (default 24).
4. **Every close is logged** to `_bmad-output/sweeper.log` (id, age, reason,
   mechanism) — one line per close, plus a per-sweep summary line.
5. **Config knobs** on the loader row (mirror nefario's `config:` shape):
   `ttlHours` (default 24), `pollMs` (default 300000), `dryRun` (default false),
   `preserve` (session-id list, always including Gru's).

## Doctrine note (why the hard gates)
The old pi-world rule was "cleanup sensors = detection-only" — auto-clean
burned the crew twice killing wrong panes by id-proximity. This sweeper is
sanctioned BECAUSE the gates are structural (storage-only + age + preserve
list), not label/id-proximity based, and it never touches a live process. Keep
it that way: if any gate cannot be evaluated deterministically, SKIP the
session and log the skip.

## Constraints
- **NEVER restart or kill the running `:3080` host.** Verify with an isolated
  `dsh web --no-open --port <spare>` boot against a COPY of the storage (or a
  sacrificial session), killed after.
- Read-only on the ledger DB if you consult it at all. No writes to `~/.dsh`
  beyond the reversible loader-row + symlink, reported exactly.
- New repo `/Users/moses/code/orchestrator-minion-sweeper` (private remote,
  `mssoka/orchestrator-minion-sweeper`), committed + pushed, branch `main`.
  Do NOT touch the dashboard repo (a sibling job owns its branch).
- Host-half changes activate on the USER's next `dsh web` restart — say so.

## Definition of done
- Sweeper plugin implementing the gates, timer-driven, config-driven, logged.
- **Proven in an isolated boot**: a sacrificial session created, swept (closed)
  by the plugin, log line written; an `idle`/`running` case and the preserve
  case proven SKIPPED. Real close exercised — not prose.
- README: gates, config, activation (restart), revert steps.
- Review: 4 lenses (blind-adversarial, edge-case, verification-gap, acceptance)
  as spawned subagents; fold findings. Adversarial lens MUST attack the gates
  (can any gate be bypassed? can it close a live session?).
- Ledger self-report transitions (standing orders below).

## Model policy
Minion + lenses on this session's default provider; no unset model lines.

## Standing orders
Self-report via
`/Users/moses/code/dsh-orchestrator-setup/bin/ledger set orchestrator-minion-sweeper <status> "<note>"`.
Commit, push (no PR needed for a fresh repo main, or open one — your call,
never merge). Report honestly; a skipped-session log is success, not failure.
