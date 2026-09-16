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
			// Silas ALWAYS runs on openai-codex/gpt-5.6-luna @ xhigh thinking.
			// User ruling 2026-09-09 keeps Luna as the COO model and
			// supersedes the 2026-09-07 Luna/max current pin. Historical max
			// incidents remain historical. Set at launch (`session_start` ->
			// pi.setModel + pi.setThinkingLevel), no manual /model; notifies if
			// missing or unkeyed, and hardened at relaunch: bin/night-watchman
			// clears PI_MODEL/PI_PROVIDER and pins --model
			// openai-codex/gpt-5.6-luna --thinking xhigh. No silent legacy
			// fallback — if Luna is unavailable the current model stays + an
			// error notifies (availability escalates to the user). Reasoning
			// tier (Gru/Bob/Perkins) = astra xhigh per 'Model policy'.
			const model = ctx.modelRegistry.find("openai-codex", "gpt-5.6-luna");
			if (model) {
				const ok = await pi.setModel(model);
				if (!ok) {
					ctx.ui.notify("Silas: no auth for openai-codex/gpt-5.6-luna — staying on the current model", "error");
				} else {
					await pi.setThinkingLevel("xhigh");
				}
			} else {
				ctx.ui.notify("Silas: openai-codex/gpt-5.6-luna not in the model registry — staying on the current model", "error");
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
