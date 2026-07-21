/**
 * nefario-watch — idle/blocked detection for minions + PR merge detection.
 *
 * Project-local (loads only when cwd is /Users/moses/code, i.e. the Gru
 * session). Polls `herdr agent list` every 30s, diffs the agent_status of
 * every ledger-tracked pane (SQLite ledger, non-done jobs with a pane_id),
 * and injects a message into this session when one transitions to
 * idle/done/blocked or vanishes.
 *
 * Why: a pi agent halted at its prompt (e.g. quick-dev step-01 clarify)
 * reports `idle`, which no human notification reliably reaches Gru — the
 * minion's `herdr notification show` only toasts the human. This extension
 * is the machine channel: the injected message triggers a turn, and Gru
 * reads the transcript, classifies, updates the ledger, and relays.
 *
 * Alert policy (pane watcher):
 * - Alert only on TRANSITIONS into idle/done/blocked (no repeats while a
 *   pane stays put; a relayed answer flips it back to working → re-arms).
 * - Pane vanishing (Herdr restart, manual close) alerts once.
 * - At session_start: silent snapshot, plus a one-time catch-up digest
 *   (deliverAs nextTurn — no turn triggered) for any pane already stopped
 *   while its ledger status says it should be running.
 * - The Gru pane itself and untracked panes are ignored by construction
 *   (diff is driven by the ledger's pane_id list).
 *
 * PR watcher (every 5 min): polls `gh pr view` for ledger jobs in
 * 'in-review' with a recorded PR. On MERGED: wakes Gru to run close-out
 * (pull base, remove worktree/branch, close pane, ledger done). On CLOSED
 * unmerged: wakes Gru to ask the user. Terminal states alert once per job;
 * Gru owns every ledger transition — this extension only detects.
 *
 * CI sensor (same 5-min tick): for OPEN in-review PRs, inspects
 * statusCheckRollup and wakes Gru when any check completes with a failing
 * conclusion (FAILURE/TIMED_OUT/STARTUP_FAILURE/ACTION_REQUIRED; StatusContext
 * FAILURE/ERROR). Alerts once per head sha — a new push re-arms, and checks
 * returning green re-arms too. CANCELLED is ignored (superseded runs are
 * normal when pushing repeatedly).
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const GRU_DIR = "/Users/moses/code";
const DB = "/Users/moses/code/_bmad-output/orchestrator.db";
const LEDGER_HELPER = "/Users/moses/code/bin/ledger";
const POLL_MS = 30_000;
const PR_POLL_MS = 300_000;

const STOPPED = new Set(["idle", "done", "blocked"]);
/** Ledger statuses where a stopped pane is expected — no catch-up alert. */
const SETTLED = new Set(["clarifying", "in-review", "blocked", "done"]);

interface TrackedJob {
	id: string;
	pane_id: string | null;
	status: string;
}

interface ReviewJob {
	id: string;
	pr: string | null;
	pane_id: string | null;
}

export default function nefarioWatch(pi: ExtensionAPI) {
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
								`ledger says '${job.status}' — likely stopped while ` +
								"Gru was down.",
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
					customType: "nefario-watch",
					content:
						"[nefario-watch] status change on ledger-tracked job(s):\n" +
						alerts.join("\n") +
						"\nFor each: `herdr pane read <pane> --source recent-unwrapped " +
						"--lines 120`, classify (clarify halt vs finished vs error), " +
						`update the ledger (\`${LEDGER_HELPER} set <job-id> <status> ` +
						'"<note>"`), and relay to the user anything needing an answer.',
					display: true,
				},
				initial
					? { deliverAs: "nextTurn" } // digest rides the first prompt; no turn
					: { deliverAs: "followUp", triggerTurn: true }, // wake Gru
			);
		} finally {
			ticking = false;
		}
	}

	// ── PR watcher: detect merges of in-review jobs ─────────────────────
	let prTimer: ReturnType<typeof setInterval> | null = null;
	let prTicking = false;
	/** job_id -> last gh pr state seen (OPEN / MERGED / CLOSED / ...). */
	const prStates = new Map<string, string>();
	/** job_id already alerted for a terminal state — alert once, ever. */
	const prAlerted = new Set<string>();
	/** job_id -> head sha already CI-alerted on (deleted when checks recover). */
	const ciAlerted = new Map<string, string>();

	async function inReviewJobs(): Promise<ReviewJob[]> {
		const r = await pi.exec(
			"sqlite3",
			[
				"-json",
				DB,
				"SELECT id, pr, pane_id FROM jobs WHERE status = 'in-review' AND pr IS NOT NULL",
			],
			{ timeout: 5000 },
		);
		if (r.code !== 0 || !r.stdout.trim()) return [];
		try {
			return JSON.parse(r.stdout) as ReviewJob[];
		} catch {
			return [];
		}
	}

	interface PrInfo {
		state: string;
		headSha: string | null;
		/** Names of checks that completed with a failing conclusion. */
		failing: string[];
	}

	const FAIL_CONCLUSIONS = new Set([
		"FAILURE",
		"TIMED_OUT",
		"STARTUP_FAILURE",
		"ACTION_REQUIRED",
	]);

	async function prInfo(url: string): Promise<PrInfo | null> {
		const r = await pi.exec(
			"gh",
			["pr", "view", url, "--json", "state,headRefOid,statusCheckRollup"],
			{ timeout: 20_000 },
		);
		if (r.code !== 0) return null; // gh missing/offline/rate-limited — skip
		try {
			const j = JSON.parse(r.stdout);
			const state = j?.state;
			if (typeof state !== "string") return null;
			const failing: string[] = [];
			for (const c of j?.statusCheckRollup ?? []) {
				// Two shapes: CheckRun {name,status,conclusion} and
				// StatusContext {context,state}. Skip in-flight CheckRuns.
				if (c?.status !== undefined && c.status !== "COMPLETED") continue;
				const bad =
					(typeof c?.conclusion === "string" &&
						FAIL_CONCLUSIONS.has(c.conclusion)) ||
					c?.state === "FAILURE" ||
					c?.state === "ERROR";
				if (bad) failing.push(c.name ?? c.context ?? "unknown");
			}
			return {
				state,
				headSha: typeof j?.headRefOid === "string" ? j.headRefOid : null,
				failing,
			};
		} catch {
			return null;
		}
	}

	async function prTick(initial: boolean): Promise<void> {
		if (prTicking) return;
		prTicking = true;
		try {
			const jobs = await inReviewJobs();
			const alerts: string[] = [];
			for (const job of jobs) {
				if (!job.pr) continue;
				const info = await prInfo(job.pr);
				if (info === null) continue;
				prStates.set(job.id, info.state);
				const terminal = info.state === "MERGED" || info.state === "CLOSED";
				if (!terminal) {
					// CI sensor: alert once per head sha while checks fail.
					if (info.failing.length === 0) {
						ciAlerted.delete(job.id); // recovered/pending — re-arm
					} else if (ciAlerted.get(job.id) !== (info.headSha ?? "")) {
						ciAlerted.set(job.id, info.headSha ?? "");
						alerts.push(
							`- ${job.id}: CI FAILING — ${job.pr}` +
								(job.pane_id ? ` (pane ${job.pane_id})` : "") +
								` — failed check(s): ${info.failing.join(", ")}. ` +
								"Investigate: `gh run list --repo <repo> --branch <slug>`, " +
								"`gh run view <run-id> --repo <repo> --log-failed`. Infra " +
								"flake → `gh run rerun <run-id> --repo <repo> --failed`; " +
								'real failure → relay to the minion: `herdr pane run <pane> "<failure summary + instruction>"`.',
						);
					}
					continue;
				}
				if (prAlerted.has(job.id)) continue;
				prAlerted.add(job.id);
				if (info.state === "MERGED") {
					alerts.push(
						`- ${job.id}: PR MERGED — ${job.pr}` +
							(job.pane_id ? ` (pane ${job.pane_id})` : "") +
							". Run close-out (ledger FIRST, pane LAST — playbook " +
							"'Close-out'): `" +
							`${LEDGER_HELPER} set ${job.id} done "<result>"\` + clear-pane, ` +
							"`git -C <repo> pull --ff-only origin <base>`, remove worktree " +
							"+ branch, close the pane.",
					);
				} else {
					alerts.push(
						`- ${job.id}: PR CLOSED UNMERGED — ${job.pr}. Ask the user: ` +
							"abandon (close job + clean up) or reopen/fix?",
					);
				}
			}
			if (alerts.length === 0) return;
			pi.sendMessage(
				{
					customType: "nefario-watch",
					content:
						"[nefario-watch] PR/CI alert on in-review job(s):\n" +
						alerts.join("\n"),
					display: true,
				},
				initial
					? { deliverAs: "nextTurn" }
					: { deliverAs: "followUp", triggerTurn: true },
			);
		} finally {
			prTicking = false;
		}
	}

	pi.on("session_start", async (_event, ctx) => {
		if (ctx.cwd !== GRU_DIR) return;
		if (timer) return; // idempotent — one watcher per session
		await tick(true);
		timer = setInterval(() => {
			void tick(false);
		}, POLL_MS);
		await prTick(true);
		prTimer = setInterval(() => {
			void prTick(false);
		}, PR_POLL_MS);
	});

	pi.on("session_shutdown", async () => {
		if (timer) {
			clearInterval(timer);
			timer = null;
		}
		if (prTimer) {
			clearInterval(prTimer);
			prTimer = null;
		}
	});
}
