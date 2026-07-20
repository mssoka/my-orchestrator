/**
 * mayor-watch — idle/blocked detection for orchestrator sub-agents.
 *
 * Project-local (loads only when cwd is /Users/moses/code, i.e. the mayor
 * session). Polls `herdr agent list` every 30s, diffs the agent_status of
 * every ledger-tracked pane (SQLite ledger, non-done jobs with a pane_id),
 * and injects a message into this session when one transitions to
 * idle/done/blocked or vanishes.
 *
 * Why: a pi agent halted at its prompt (e.g. quick-dev step-01 clarify)
 * reports `idle`, which no human notification reliably reaches the mayor —
 * the sub-agent's `herdr notification show` only toasts the human. This
 * extension is the machine channel: the injected message triggers a turn,
 * and the mayor reads the transcript, classifies, updates the ledger, and
 * relays.
 *
 * Alert policy:
 * - Alert only on TRANSITIONS into idle/done/blocked (no repeats while a
 *   pane stays put; a relayed answer flips it back to working → re-arms).
 * - Pane vanishing (Herdr restart, manual close) alerts once.
 * - At session_start: silent snapshot, plus a one-time catch-up digest
 *   (deliverAs nextTurn — no turn triggered) for any pane already stopped
 *   while its ledger status says it should be running.
 * - The mayor pane itself and untracked panes are ignored by construction
 *   (diff is driven by the ledger's pane_id list).
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const MAYOR_DIR = "/Users/moses/code";
const DB = "/Users/moses/code/_bmad-output/orchestrator.db";
const LEDGER_HELPER = "/Users/moses/code/bin/ledger";
const POLL_MS = 30_000;

const STOPPED = new Set(["idle", "done", "blocked"]);
/** Ledger statuses where a stopped pane is expected — no catch-up alert. */
const SETTLED = new Set(["clarifying", "in-review", "blocked", "done"]);

interface TrackedJob {
	id: string;
	pane_id: string | null;
	status: string;
}

export default function mayorWatch(pi: ExtensionAPI) {
	let timer: ReturnType<typeof setInterval> | null = null;
	let ticking = false;
	/** job_id -> last observed agent_status ("gone" when the pane vanished). */
	const last = new Map<string, string>();

	async function trackedJobs(): Promise<TrackedJob[]> {
		const r = await pi.exec(
			"sqlite3",
			[
				"-json",
				DB,
				"SELECT id, pane_id, status FROM jobs WHERE status != 'done' AND pane_id IS NOT NULL",
			],
			{ timeout: 5000 },
		);
		if (r.code !== 0 || !r.stdout.trim()) return [];
		try {
			return JSON.parse(r.stdout) as TrackedJob[];
		} catch {
			return [];
		}
	}

	/** pane_id -> agent_status for every detected agent. */
	async function liveStatuses(): Promise<Map<string, string>> {
		const r = await pi.exec("herdr", ["agent", "list"], { timeout: 8000 });
		const m = new Map<string, string>();
		if (r.code !== 0) return m;
		try {
			const env = JSON.parse(r.stdout);
			for (const a of env?.result?.agents ?? []) {
				if (a?.pane_id && a?.agent_status) m.set(a.pane_id, a.agent_status);
			}
		} catch {
			// herdr output changed shape — skip this tick
		}
		return m;
	}

	async function tick(initial: boolean): Promise<void> {
		if (ticking) return; // a slow herdr/sqlite call must not stack ticks
		ticking = true;
		try {
			const [jobs, live] = await Promise.all([trackedJobs(), liveStatuses()]);
			const alerts: string[] = [];

			for (const job of jobs) {
				const pane = job.pane_id;
				if (!pane) continue;
				const cur = live.get(pane);
				const prev = last.get(job.id);

				if (cur === undefined) {
					// Tracked pane not in agent list: closed, or Herdr restarted
					// and ids changed. Alert once per disappearance.
					if (prev !== undefined && prev !== "gone") {
						alerts.push(
							`- ${job.id} (${pane}): pane no longer has a detected agent ` +
								`(was '${prev}', ledger '${job.status}'). Herdr may have ` +
								"restarted — re-resolve pane ids and update the ledger.",
						);
					}
					last.set(job.id, "gone");
					continue;
				}

				if (prev === undefined) {
					// First sighting. On the startup pass, catch transitions that
					// happened while this session was down.
					last.set(job.id, cur);
					if (initial && STOPPED.has(cur) && !SETTLED.has(job.status)) {
						alerts.push(
							`- ${job.id} (${pane}): '${cur}' at session start while ` +
								`ledger says '${job.status}' — likely stopped while the ` +
								"mayor session was down.",
						);
					}
					continue;
				}

				if (cur !== prev) {
					last.set(job.id, cur);
					if (STOPPED.has(cur)) {
						alerts.push(
							`- ${job.id} (${pane}): ${prev} → ${cur} (ledger: '${job.status}')`,
						);
					}
				}
			}

			if (alerts.length === 0) return;

			pi.sendMessage(
				{
					customType: "mayor-watch",
					content:
						"[mayor-watch] status change on ledger-tracked job(s):\n" +
						alerts.join("\n") +
						"\nFor each: `herdr pane read <pane> --source recent-unwrapped " +
						"--lines 120`, classify (clarify halt vs finished vs error), " +
						`update the ledger (\`${LEDGER_HELPER} set <job-id> <status> ` +
						'"<note>"`), and relay to the user anything needing an answer.',
					display: true,
				},
				initial
					? { deliverAs: "nextTurn" } // digest rides the first prompt; no turn
					: { deliverAs: "followUp", triggerTurn: true }, // wake the mayor
			);
		} finally {
			ticking = false;
		}
	}

	pi.on("session_start", async (_event, ctx) => {
		if (ctx.cwd !== MAYOR_DIR) return;
		if (timer) return; // idempotent — one watcher per session
		await tick(true);
		timer = setInterval(() => {
			void tick(false);
		}, POLL_MS);
	});

	pi.on("session_shutdown", async () => {
		if (timer) {
			clearInterval(timer);
			timer = null;
		}
	});
}
