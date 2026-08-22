/**
 * Gru (CEO) hook for /Users/moses/code.
 *
 * Project-local extension, active ONLY when the session is launched
 * `PI_GRU=1 pi` with cwd /Users/moses/code (env opt-in — the P9 gate;
 * cwd alone never activates it, so dream panes and sheep stay clean).
 *
 * Gru is the CEO: the user interface. He owns intake, briefing
 * authorship, dispatch DECISIONS, and escalations. ALL operations
 * (watcher alerts, ledger transitions, close-outs, relays, Perkins
 * rounds, dream dispatches) belong to Silas, the COO — a second session
 * launched `PI_SILAS=1 pi` (pane label `silas`, see silas.ts); the
 * nefario-watch sensors are gated to Silas, not Gru.
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
import { GRU_STANDING_ORDERS, GRU_STARTUP_CHECKLIST } from "./generated/role-blocks";

const GRU_DIR = "/Users/moses/code";
const PLAYBOOK = "/Users/moses/code/docs/orchestration-playbook.md";
const LEDGER_HELPER = "/Users/moses/code/bin/ledger";
const LEDGER_DB = "/Users/moses/code/_bmad-output/orchestrator.db";
const SKILLS_DIR = "/Users/moses/code/.agents/skills";

// STANDING_ORDERS + STARTUP_CHECKLIST are GENERATED — single source:
// docs/orchestration-playbook.md 'Role standing orders (paste-block
// source)'; regenerate with bin/gen-role-blocks. Never edit the
// generated module by hand. REGROUND below is session-recovery
// plumbing (single copy, no drift surface) — deliberately inline.


const REGROUND =
  "This session was just compacted — job details from message history may " +
  `be stale or summarized away. Run \`${LEDGER_HELPER}\` (read-only — ` +
  "Silas owns transitions) and check `herdr agent list` for the `silas` " +
  "pane before continuing. You are Gru (CEO): user interface only — " +
  "operations stay with Silas.";

export default function gru(pi: ExtensionAPI) {
	pi.on("session_start", async (event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		if (process.env.PI_GRU !== "1") return;
		// "new" starts a fresh transcript, so re-kick. "resume"/"fork" keep
		// their history — the per-turn standing orders are enough there.
		if (event.reason === "startup" || event.reason === "new") {
			await pi.sendUserMessage(GRU_STARTUP_CHECKLIST);
		}
	});

	pi.on("before_agent_start", async (event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		if (process.env.PI_GRU !== "1") return;
		return { systemPrompt: event.systemPrompt + "\n" + GRU_STANDING_ORDERS };
	});

	pi.on("session_compact", async (_event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		if (process.env.PI_GRU !== "1") return;
		// Queued for the next prompt; does not interrupt or trigger a turn.
		pi.sendMessage(
			{ customType: "gru-reground", content: REGROUND, display: true },
			{ deliverAs: "nextTurn" },
		);
	});
}
