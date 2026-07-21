/**
 * Gru (orchestrator) hook for /Users/moses/code.
 *
 * Project-local extension: pi only loads it when cwd is this directory, so it
 * applies to the orchestrator and never to minions — they run in worktrees
 * under ~/.herdr/worktrees with their own cwd.
 *
 * Duties:
 * 1. session_start (startup/new): send the AGENTS.md startup checklist as a
 *    real user message, so it actually executes (read playbook + ledger,
 *    reconcile with live Herdr state) instead of sitting as passive context.
 * 2. before_agent_start: append short standing orders to the system prompt on
 *    every turn. The system prompt is rebuilt each turn, so this survives
 *    compaction, which only summarizes message history.
 * 3. session_compact: queue a re-grounding message for the next turn — job
 *    details lived in message history and may have been summarized away.
 *
 * Naming theme (Despicable Me): Gru = orchestrator, minions = task agents he
 * dispatches, mega-minions = specialist helpers a minion spawns. See README.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const GRU_DIR = "/Users/moses/code";
const PLAYBOOK = "/Users/moses/code/docs/orchestration-playbook.md";
const LEDGER_HELPER = "/Users/moses/code/bin/ledger";
const LEDGER_DB = "/Users/moses/code/_bmad-output/orchestrator.db";

const STANDING_ORDERS = `
## Gru standing orders (enforced by .pi/extensions/gru.ts)

You are Gru, the orchestrator for ${GRU_DIR}; you dispatch, you do not implement.
- Playbook: ${PLAYBOOK}
- Job ledger: SQLite at ${LEDGER_DB} — query via \`${LEDGER_HELPER}\`
  (active jobs), update on every status transition via
  \`${LEDGER_HELPER} set <job-id> <status> "<note>"\`.
- On your first action of a session, and after any compaction: read the
  playbook, run \`${LEDGER_HELPER}\`, and reconcile against live Herdr state
  (\`herdr agent list\`). Herdr workspace/pane ids are ephemeral across
  restarts — re-resolve them; never trust ids from an old session.
- nefario-watch (nefario-watch.ts) injects a message when a ledger-tracked pane
  transitions to idle/done/blocked — read the transcript, classify, update
  the ledger, relay to the user.
- Never implement in a main checkout; dispatch minions into Herdr worktrees.
- Never merge PRs. Max 10 minions (dispatched task panes) unless the user
  says otherwise; each minion may fan out max 10 mega-minions (child panes,
  not counted against the 10; must be closed before its minion finishes).
`;

const STARTUP_CHECKLIST =
  `Gru startup checklist: read ${PLAYBOOK} and run \`${LEDGER_HELPER}\`, ` +
  "then reconcile the ledger against live Herdr state (`herdr agent list`). " +
  "Reply with a short readiness report: active jobs, blocked jobs needing " +
  "relay, free pane slots. If the ledger is empty and nothing is running, " +
  "say so in one line.";

const REGROUND =
  "This session was just compacted — job details from message history may " +
  `be stale or summarized away. Run \`${LEDGER_HELPER}\` and reconcile ` +
  "against `herdr agent list` before continuing any orchestration work.";

export default function gru(pi: ExtensionAPI) {
	pi.on("session_start", async (event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		// "new" starts a fresh transcript, so re-kick. "resume"/"fork" keep
		// their history — the per-turn standing orders are enough there.
		if (event.reason === "startup" || event.reason === "new") {
			await pi.sendUserMessage(STARTUP_CHECKLIST);
		}
	});

	pi.on("before_agent_start", async (event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		return { systemPrompt: event.systemPrompt + "\n" + STANDING_ORDERS };
	});

	pi.on("session_compact", async (_event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		// Queued for the next prompt; does not interrupt or trigger a turn.
		pi.sendMessage(
			{ customType: "gru-reground", content: REGROUND, display: true },
			{ deliverAs: "nextTurn" },
		);
	});
}
