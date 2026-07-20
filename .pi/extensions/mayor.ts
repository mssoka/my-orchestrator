/**
 * Mayor (orchestrator) hook for /Users/moses/code.
 *
 * Project-local extension: pi only loads it when cwd is this directory, so it
 * applies to the orchestrator and never to task sub-agents — they run in
 * worktrees under ~/.herdr/worktrees with their own cwd.
 *
 * Duties:
 * 1. session_start (startup/new): send the AGENTS.md startup checklist as a
 *    real user message, so it actually executes (read playbook + ledger,
 *    reconcile with live Herdr state) instead of sitting as passive context.
 * 2. before_agent_start: append short mayor standing orders to the system
 *    prompt on every turn. The system prompt is rebuilt each turn, so this
 *    survives compaction, which only summarizes message history.
 * 3. session_compact: queue a re-grounding message for the next turn — job
 *    details lived in message history and may have been summarized away.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const MAYOR_DIR = "/Users/moses/code";
const PLAYBOOK = "/Users/moses/code/docs/orchestration-playbook.md";
const LEDGER = "/Users/moses/code/_bmad-output/orchestrator-jobs.yaml";

const STANDING_ORDERS = `
## Mayor standing orders (enforced by .pi/extensions/mayor.ts)

You are the orchestrator for ${MAYOR_DIR}; you dispatch, you do not implement.
- Playbook: ${PLAYBOOK}
- Job ledger: ${LEDGER} — update it on every status transition.
- On your first action of a session, and after any compaction: read the
  playbook and ledger, and reconcile the ledger against live Herdr state
  (\`herdr agent list\`, \`herdr pane list --workspace w7\`).
- Never implement in a main checkout; dispatch into Herdr worktrees.
- Never merge PRs. Max 3 concurrent task panes unless the user says otherwise.
`;

const STARTUP_CHECKLIST =
  `Mayor startup checklist: read ${PLAYBOOK} and ${LEDGER}, then reconcile ` +
  "the ledger against live Herdr state (`herdr agent list`, " +
  "`herdr pane list --workspace w7`). Reply with a short readiness report: " +
  "active jobs, blocked jobs needing relay, free pane slots. If the ledger " +
  "is empty and nothing is running, say so in one line.";

const REGROUND =
  "This session was just compacted — job details from message history may " +
  `be stale or summarized away. Re-read ${LEDGER} and reconcile against ` +
  "`herdr agent list` before continuing any orchestration work.";

export default function mayor(pi: ExtensionAPI) {
	pi.on("session_start", async (event, ctx) => {
		if (ctx.cwd !== MAYOR_DIR) return;
		// "new" starts a fresh transcript, so re-kick. "resume"/"fork" keep
		// their history — the per-turn standing orders are enough there.
		if (event.reason === "startup" || event.reason === "new") {
			await pi.sendUserMessage(STARTUP_CHECKLIST);
		}
	});

	pi.on("before_agent_start", async (event, ctx) => {
		if (ctx.cwd !== MAYOR_DIR) return;
		return { systemPrompt: event.systemPrompt + "\n" + STANDING_ORDERS };
	});

	pi.on("session_compact", async (_event, ctx) => {
		if (ctx.cwd !== MAYOR_DIR) return;
		// Queued for the next prompt; does not interrupt or trigger a turn.
		pi.sendMessage(
			{ customType: "mayor-reground", content: REGROUND, display: true },
			{ deliverAs: "nextTurn" },
		);
	});
}
