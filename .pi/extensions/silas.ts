/**
 * Silas (COO) hook for /Users/moses/code.
 *
 * Project-local extension, active ONLY when the session is launched
 * `PI_SILAS=1 pi` with cwd /Users/moses/code (env opt-in — the P9 gate;
 * cwd alone never activates it).
 *
 * Silas Ramsbottom = chief operating officer of the orchestration. He owns
 * every operational duty so Gru (launched `PI_GRU=1 pi`, pane label `gru`)
 * stays a clean user interface:
 *   - nefario-watch alerts (gated to this session): classify + act
 *   - ALL ledger transitions (set/note/clear-pane/pr)
 *   - close-outs (merge → pull base → torch worktree/branch → close pane)
 *   - CI triage + relays, review relays, Perkins round dispatch/close-out
 *   - dream (Bob) dispatch + close-out, dispatch mechanics on Gru's handoff
 *
 * Duties:
 * 1. session_start (startup/new): send the Silas startup checklist as a
 *    real user message, so it actually executes.
 * 2. before_agent_start: append the standing orders to the system prompt
 *    on every turn (survives compaction).
 * 3. session_compact: queue a re-grounding message for the next turn.
 *
 * Escalations to Gru: `herdr pane run <gru-pane> "[SILAS] <one-liner +
 * decision needed>"` — resolve the Gru pane by label `gru` via
 * `herdr agent list`. See playbook section 'Silas (COO)'.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { SILAS_STANDING_ORDERS, SILAS_STARTUP_CHECKLIST } from "./generated/role-blocks";

const GRU_DIR = "/Users/moses/code";
const PLAYBOOK = "/Users/moses/code/docs/orchestration-playbook.md";
const LEDGER_HELPER = "/Users/moses/code/bin/ledger";

// STANDING_ORDERS + STARTUP_CHECKLIST are GENERATED — single source:
// docs/orchestration-playbook.md 'Role standing orders (paste-block
// source)'; regenerate with bin/gen-role-blocks. Never edit the
// generated module by hand. REGROUND below is session-recovery
// plumbing (single copy, no drift surface) — deliberately inline.


const REGROUND =
  "This session was just compacted — job details from message history may " +
  `be stale or summarized away. Run \`${LEDGER_HELPER}\` and reconcile ` +
  "against `herdr agent list` before continuing any operations work. You " +
  "are Silas (COO): you own operations; escalate user decisions to the " +
  "pane labeled `gru`.";

export default function silas(pi: ExtensionAPI) {
	pi.on("session_start", async (event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		if (process.env.PI_SILAS !== "1") return;
		if (event.reason === "startup" || event.reason === "new") {
			// Silas ALWAYS runs on deepseek/deepseek-v4-flash (user ruling
			// 2026-09-06: API billing = no session limits; the COO must be
			// available to coordinate — availability is the point of the
			// ruling). Supersedes the 08-27 glm-5.3-flash COO pin (which
			// stays the minion/mega-minion ops default, untouched by this
			// ruling — COO-only). Reasoning tier stays kimi k3 primary.
			// Fallback if deepseek 402s (balance wall): glm-5.3-flash interim
			// + escalate to the user for a top-up (per the policy doc).
			const model = ctx.modelRegistry.find("deepseek", "deepseek-v4-flash");
			if (model) {
				const ok = await pi.setModel(model);
				if (!ok) ctx.ui.notify("Silas: no API key for deepseek/deepseek-v4-flash — staying on the current model", "error");
			} else {
				ctx.ui.notify("Silas: deepseek/deepseek-v4-flash not in the model registry — staying on the current model", "error");
			}
			await pi.sendUserMessage(SILAS_STARTUP_CHECKLIST);
		}
	});

	pi.on("before_agent_start", async (event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		if (process.env.PI_SILAS !== "1") return;
		return { systemPrompt: event.systemPrompt + "\n" + SILAS_STANDING_ORDERS };
	});

	pi.on("session_compact", async (_event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		if (process.env.PI_SILAS !== "1") return;
		pi.sendMessage(
			{ customType: "silas-reground", content: REGROUND, display: true },
			{ deliverAs: "nextTurn" },
		);
	});
}
