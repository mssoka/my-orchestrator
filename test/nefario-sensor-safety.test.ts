/**
 * nefario-watch sensor-safety suite (packet B + narrow R02/R04 surfaces).
 *
 * Loads the REAL extension (no reimplementation), fakes only the
 * ExtensionAPI boundary (pi.exec / pi.sendMessage / setInterval). The
 * debris path checks run against the REAL filesystem on os.tmpdir()
 * scratch directories (including literally-named `$(...)`/backtick/
 * newline paths — N07 proves no shell ever interprets them).
 *
 * Covers the 2026-09-12 audit's selected sensor findings:
 *   N04 herdr failure is UNKNOWN, not an empty inventory
 *   N05 correct GitHub status endpoint/schema (summary.json), multi-incident,
 *      partial recovery, evidence-based clear, invalid ≠ recovery
 *   N07 debris paths never cross a shell boundary (fs.statSync)
 *   N08 live-owner exemption on EVERY debris branch; ownership queries fail
 *      closed; real unowned debris still surfaces (detection-only)
 *   R02 APPROVED alert is an observation, never an unqualified merge verdict
 *   R04 bare-number PRs use an explicit canonical --repo or are skipped
 *
 * Run: node --experimental-strip-types test/nefario-sensor-safety.test.ts
 * (Node >= 22.6; companion to test/nefario-watch-conflict.test.ts).
 */
import { strict as assert } from "node:assert";
import { mkdtempSync, mkdirSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import nefarioWatch from "../.pi/extensions/nefario-watch.ts";

const SHA1 = "1111111111111111111111111111111111111111";
const PR = "https://github.com/acme/demo/pull/7";

interface GhShape {
	state: string;
	headRefOid: string;
	mergeable?: string | null;
	mergeStateStatus?: string | null;
	baseRefName?: string;
	statusCheckRollup?: unknown[];
	reviews?: Array<{
		id: string;
		state: string;
		author: { login: string } | null;
		body: string;
	}>;
}

interface World {
	jobs: Array<Record<string, unknown>>; // pane-watcher rows
	reviewJobs: Array<Record<string, unknown>> | null; // in-review rows (null → parse as "[]")
	roundRows: Array<{ id: string; worktree: string; repo_root: string | null }>;
	liveRows: Array<{ worktree: string }> | { error: number };
	/** Pane-tick `herdr agent list` responses (liveStatuses): a static
	 * result, or a queue consumed in order (clamped at the last entry).
	 * ONLY the pane tick's inventory reads this — see the herdr handler. */
	paneTickHerdr: { code: number; stdout: string } | Array<{ code: number; stdout: string }>;
	herdrAgents: { code: number; stdout: string }; // PR-tick `herdr agent list` (debris inventory)
	gitWorktree: { code: number; stdout: string };
	gh: GhShape;
	summary: { code: number; stdout: string };
}

class FakePi {
	sent: Array<{ content: string; opts: unknown }> = [];
	startHandler: (() => Promise<void>) | null = null;
	execLog: Array<{ cmd: string; args: string[] }> = [];
	/** Which tick invoked the current herdr call — "start" during
	 * session_start (pane tick first, then PR tick), "pane"/"pr" for
	 * explicit tick invocations. Used ONLY to route `herdr agent list`. */
	phase: "start" | "pane" | "pr" = "start";
	private startPaneInventoryDone = false;
	private paneTickCalls = 0;
	private w: World;

	constructor(w: Partial<World> = {}) {
		this.w = {
			jobs: [],
			reviewJobs: null,
			roundRows: [],
			liveRows: [],
			paneTickHerdr: { code: 0, stdout: JSON.stringify({ result: { agents: [] } }) },
			herdrAgents: { code: 0, stdout: JSON.stringify({ result: { agents: [] } }) },
			gitWorktree: { code: 0, stdout: "" },
			gh: baseGh(),
			summary: {
				code: 0,
				stdout: JSON.stringify({
					status: { indicator: "none", description: "All Systems Operational" },
					components: [],
					incidents: [],
				}),
			},
			...w,
		};
	}

	get world(): World {
		return this.w;
	}

	on(evt: string, h: unknown) {
		if (evt === "session_start") this.startHandler = h as () => Promise<void>;
	}

	async exec(
		cmd: string,
		args: string[],
		_opts?: unknown,
	): Promise<{ code: number; stdout: string; stderr: string }> {
		this.execLog.push({ cmd, args: [...args] });
		const w = this.w;
		if (cmd === "sqlite3") {
			const sql = args[2] ?? "";
			if (sql.includes("parent")) {
				return { code: 0, stdout: JSON.stringify([]), stderr: "" };
			}
			if (sql.includes("DISTINCT worktree")) {
				// debris live-ownership query (N08)
				if (typeof w.liveRows === "object" && "error" in w.liveRows)
					return { code: w.liveRows.error, stdout: "", stderr: "sqlite exploded" };
				return { code: 0, stdout: JSON.stringify(w.liveRows), stderr: "" };
			}
			if (sql.includes("'%-perkins-r%'" ) && sql.includes("status = 'done'")) {
				// debris done-round rows
				return { code: 0, stdout: JSON.stringify(w.roundRows), stderr: "" };
			}
			if (sql.includes("status != 'done'")) {
				// pane watcher rows
				return { code: 0, stdout: JSON.stringify(w.jobs), stderr: "" };
			}
			if (sql.includes("status = 'in-review'")) {
				return { code: 0, stdout: JSON.stringify(w.reviewJobs ?? []), stderr: "" };
			}
			return { code: 0, stdout: "[]", stderr: "" };
		}
		if (cmd === "herdr") {
			// Route by subcommand — the tests must control each production
			// call site deterministically:
			//   · `herdr tab list` (stuckCheck labels) → empty tab list
			//   · `herdr pane get <id>` (stuckCheck pane info) → null session
			//     so stuck candidates are skipped deterministically
			//   · `herdr agent list`: the PANE TICK's liveStatuses reads
			//     world.paneTickHerdr; every agent-list inside the PR tick
			//     (roundDebrisCheck inventory, stuckCheck liveStatuses) reads
			//     world.herdrAgents. During session_start the pane tick runs
			//     FIRST — its inventory is the first agent-list call.
			if (args[0] === "tab" && args[1] === "list") {
				return { code: 0, stdout: JSON.stringify({ result: { tabs: [] } }), stderr: "" };
			}
			if (args[0] === "pane" && args[1] === "get") {
				return {
					code: 0,
					stdout: JSON.stringify({
						result: { pane: { pane_id: args[2] ?? "?", cwd: "/tmp", agent_session: null } },
				}),
					stderr: "",
				};
			}
			if (args[0] === "agent" && args[1] === "list") {
				const paneRoute =
					this.phase === "pane" ||
					(this.phase === "start" && !this.startPaneInventoryDone);
				if (this.phase === "start" && paneRoute) this.startPaneInventoryDone = true;
				if (paneRoute) {
					const src = this.w.paneTickHerdr;
					const r = Array.isArray(src)
						? src[Math.min(this.paneTickCalls, src.length - 1)]
						: src;
					this.paneTickCalls++;
					return { code: r.code, stdout: r.stdout, stderr: r.code ? "herdr exploded" : "" };
				}
				const a = this.w.herdrAgents;
				return { code: a.code, stdout: a.stdout, stderr: a.code ? "herdr exploded" : "" };
			}
			throw new Error("unexpected herdr subcommand: " + args.join(" "));
		}
		if (cmd === "git") {
			// worktree list --porcelain
			return { code: w.gitWorktree.code, stdout: w.gitWorktree.stdout, stderr: w.gitWorktree.code ? "git exploded" : "" };
		}
		if (cmd === "gh") {
			if (args[0] === "api") {
				return { code: 0, stdout: JSON.stringify([]), stderr: "" };
			}
			return { code: 0, stdout: JSON.stringify(w.gh), stderr: "" };
		}
		if (cmd === "bash") {
			return { code: 0, stdout: "BASELINE\n", stderr: "" }; // dreamCheck
		}
		if (cmd === "curl") {
			return { code: w.summary.code, stdout: w.summary.stdout, stderr: "" };
		}
		throw new Error("unexpected exec: " + cmd + " " + args.join(" "));
	}

	sendMessage(msg: { content: string }, opts: unknown) {
		this.sent.push({ content: msg.content, opts });
	}
}

const intervalCallbacks: Array<() => void> = [];
function captureIntervals() {
	const real = globalThis.setInterval;
	(globalThis as unknown as { setInterval: unknown }).setInterval = ((
		cb: () => void,
	) => {
		intervalCallbacks.push(cb);
		return intervalCallbacks.length;
	}) as typeof globalThis.setInterval;
	return {
		restore() {
			globalThis.setInterval = real;
		},
	};
}

function baseGh(over: Partial<GhShape> = {}): GhShape {
	return {
		state: "OPEN",
		headRefOid: SHA1,
		mergeable: "MERGEABLE",
		mergeStateStatus: "CLEAN",
		baseRefName: "main",
		statusCheckRollup: [],
		reviews: [],
		...over,
	};
}

/** Boot + session_start → returns [paneTick, prTick] callbacks (the
 * captured interval callbacks, phase-tagged so herdr routing stays
 * deterministic under explicit invocation). */
async function start(pi: FakePi): Promise<[() => void, () => void]> {
	process.env.PI_SILAS = "1";
	nefarioWatch(pi as never);
	assert.ok(pi.startHandler, "session_start handler registered");
	const before = intervalCallbacks.length;
	await pi.startHandler({}, { cwd: "/Users/moses/code" });
	assert.equal(intervalCallbacks.length, before + 2, "two intervals registered");
	const rawPane = intervalCallbacks[before] as () => void;
	const rawPr = intervalCallbacks[before + 1] as () => void;
	return [
		() => {
			pi.phase = "pane";
			rawPane();
		},
		() => {
			pi.phase = "pr";
			rawPr();
		},
	];
}

async function sleep(ms: number): Promise<void> {
	return new Promise((r) => setTimeout(r, ms));
}

function summaryPayload(over: Record<string, unknown> = {}): string {
	return JSON.stringify({
		status: { indicator: "none", description: "All Systems Operational" },
		components: [],
		incidents: [],
		...over,
	});
}

async function run() {
	const ints = captureIntervals();
	const scratchDirs: string[] = [];
	const all: string[] = [];
	try {
		// ── N04: herdr failure is UNKNOWN, not empty inventory ───────────
		{
			const agents = JSON.stringify({
				result: { agents: [{ pane_id: "w1:p1", agent_status: "working" }] },
			});
			const pi = new FakePi({
				jobs: [{ id: "job-a", pane_id: "w1:p1", status: "working" }],
				paneTickHerdr: { code: 0, stdout: agents },
			});
			const [paneTick] = await start(pi);
			await sleep(30);
			assert.equal(pi.sent.length, 0, "n04a: healthy first sample silent");

			pi.world.paneTickHerdr = { code: 1, stdout: "" };
			await paneTick();
			await sleep(30);
			const health = pi.sent.map((s) => s.content).filter((c) => c.includes("SENSOR HEALTH"));
			assert.equal(health.length, 1, "n04b: one health note on tool failure");
			assert.match(health[0], /herdr-inventory/, "n04b: names the failure kind");
			assert.equal(
				pi.sent.filter((s) => s.content.includes("no longer has a detected agent")).length,
				0,
				"n04b: NO false gone alert synthesized",
			);

			await paneTick();
			await sleep(30);
			assert.equal(
				pi.sent.length,
				1,
				"n04c: repeated failure within 30min is rate-limited (no second note)",
			);

			pi.world.paneTickHerdr = { code: 0, stdout: agents };
			await paneTick();
			await sleep(30);
			assert.equal(
				pi.sent.filter((s) => s.content.includes("status change")).length,
				0,
				"n04d: recovery after tool error invents NO gone→working transitions",
			);
			all.push("N04 herdr-failure=UNKNOWN + rate-limit + no false transitions: ok");
		}

		// ── N04 positive control: successful empty inventory = real gone ──
		{
			const good = JSON.stringify({
				result: { agents: [{ pane_id: "w1:p1", agent_status: "working" }] },
			});
			const pi = new FakePi({
				jobs: [{ id: "job-a", pane_id: "w1:p1", status: "working" }],
				paneTickHerdr: { code: 0, stdout: good },
			});
			const [paneTick] = await start(pi);
			await sleep(30);
			assert.equal(pi.sent.length, 0, "n04e setup: healthy first sighting silent");
			pi.world.paneTickHerdr = {
				code: 0,
				stdout: JSON.stringify({ result: { agents: [] } }),
			};
			await paneTick();
			await sleep(30);
			assert.equal(
				pi.sent.filter((s) => s.content.includes("no longer has a detected agent")).length,
				1,
				"n04e: successful empty inventory still alerts real disappearance",
			);
			all.push("N04 successful-empty still detects disappearance: ok");
		}

		// ── N05: correct endpoint/schema + incidents + recovery ───────────
		{
			const pi = new FakePi();
			const [, prTick] = await start(pi);
			await sleep(30);
			assert.equal(pi.sent.length, 0, "n05a: all-clear baseline silent");

			(pi.world as never as { summary: { code: number; stdout: string } }).summary = {
				code: 0,
				stdout: summaryPayload({
					status: { indicator: "major", description: "Partial outage" },
					incidents: [
						{ id: "i1", name: "Incident One", status: "investigating", impact: "major" },
						{ id: "i2", name: "Incident Two", status: "identified", impact: "minor" },
					],
					components: [
						{ id: "c1", name: "Actions", status: "major_outage" },
						{ id: "c2", name: "Git Operations", status: "operational" },
					],
				}),
			};
			await prTick();
			await sleep(30);
			const adv = pi.sent.map((s) => s.content);
			assert.equal(adv.length, 1, "n05b: major indicator + incidents fire ONE advisory");
			assert.match(adv[0], /Incident One/, "n05b: first incident listed");
			assert.match(adv[0], /Incident Two/, "n05b: BOTH incidents listed (multi-incident)");
			assert.match(adv[0], /Actions=major_outage/, "n05b: affected component listed");
			assert.match(adv[0], /Do NOT assume Git/, "n05b: no git-green assumption");
			assert.doesNotMatch(adv[0], /git ops GREEN/, "n05b: old git-green claim gone");

			await prTick();
			await sleep(30);
			assert.equal(pi.sent.length, 1, "n05c: same state deduped");

			// partial recovery: i2 resolves out
			(pi.world as never as { summary: { code: number; stdout: string } }).summary = {
				code: 0,
				stdout: summaryPayload({
					status: { indicator: "minor", description: "Monitoring" },
					incidents: [{ id: "i1", name: "Incident One", status: "monitoring", impact: "major" }],
				}),
			};
			await prTick();
			await sleep(30);
			assert.equal(pi.sent.length, 2, "n05d: partial recovery re-advises");
			assert.match(pi.sent[1].content, /Incident One/, "n05d: remaining incident named");

			// full recovery → evidence-based clear
			(pi.world as never as { summary: { code: number; stdout: string } }).summary = {
				code: 0,
				stdout: summaryPayload(),
			};
			await prTick();
			await sleep(30);
			assert.equal(pi.sent.length, 3, "n05e: full recovery clears");
			assert.match(pi.sent[2].content, /no unresolved incidents/, "n05e: clear is evidence-based");

			// invalid payload is NOT a recovery (no clear without evidence)
			(pi.world as never as { summary: { code: number; stdout: string } }).summary = {
				code: 0,
				stdout: summaryPayload({
					status: { indicator: "minor" },
					incidents: [{ id: "i1", name: "Incident One", status: "monitoring" }],
				}),
			};
			await prTick();
			await sleep(30);
			assert.equal(pi.sent.length, 4, "n05f: re-advisory after clear is possible");
			(pi.world as never as { summary: { code: number; stdout: string } }).summary = {
				code: 0,
				stdout: JSON.stringify({ page: { id: "x" }, status: { description: "?" } }),
			};
			await prTick();
			await sleep(30);
			assert.equal(pi.sent.length, 4, "n05g: invalid schema skipped — NOT treated as recovery");
			all.push("N05 summary.json schema + incidents + recovery: ok");
		}

		// ── N05 regression: the OLD endpoint's shape (status.json-only with
		//    a major indicator and no incidents field) must not be silently
		//    clear — the new reader fetches summary.json and validates it.
		{
			const pi = new FakePi({
				summary: {
					code: 0,
					stdout: JSON.stringify({
						page: { id: "kctbh9vrtdwd", name: "GitHub" },
						status: { indicator: "critical", description: "Major" },
					}),
				},
			});
			const [, prTick] = await start(pi);
			await sleep(30);
			assert.equal(pi.sent.length, 0, "n05h: schema-invalid payload produces NO message (skip, not clear)");
			all.push("N05 invalid payload ≠ recovery: ok");
		}

		// ── N07: no shell interpretation of debris paths ──────────────────
		{
			const root = mkdtempSync(join(tmpdir(), "nefario-n07-"));
			scratchDirs.push(root);
			// a directory whose NAME is literal shell metacharacters
			const evilName = 'evil$(printf INERT)`id`;"quote" space\nnewline';
			const evilDir = join(root, evilName);
			mkdirSync(evilDir);
			const pi = new FakePi({
				roundRows: [{ id: "demo-perkins-r1", worktree: evilDir, repo_root: root }],
				gitWorktree: { code: 0, stdout: `worktree ${root}\n` },
			});
			const [, prTick] = await start(pi);
			await sleep(50);
			const debrisAlerts = pi.sent.filter((s) => s.content.includes("PERKINS ROUND DEBRIS"));
			assert.equal(debrisAlerts.length, 1, "n07a: real existing dir with metachar name still surfaces");
			assert.match(debrisAlerts[0].content, /Detection-only/, "n07a: detection-only wording");
			assert.ok(existsSync(evilDir), "n07a: the literal directory still exists");
			// Core N07 proof: the path BYTES never cross into any bash argv
			// (bash itself is legitimately used elsewhere — quota probe,
			// dreamCheck — the defect was existence checks via shell
			// interpolation, so that's what must be proven absent).
			const evilFrag = evilName.slice(0, 12);
			const bashWithBytes = pi.execLog.filter(
				(e) => e.cmd === "bash" && e.args.join(" ").includes(evilFrag),
			);
			assert.equal(
				bashWithBytes.length,
				0,
				"n07b: no bash argv ever carries the path bytes (existence is pure fs.statSync)",
			);
			const existenceScripts = pi.execLog.filter(
				(e) => e.cmd === "bash" && e.args.join(" ").includes("[ -d"),
			);
			assert.equal(
				existenceScripts.length,
				0,
				"n07b: no shell existence-test scripts at all",
			);
			all.push("N07 fs.statSync existence, zero shell path bytes: ok");
		}

		// ── N07: unexpected path roots skipped ────────────────────────────
		{
			const pi = new FakePi({
				roundRows: [{ id: "demo-perkins-r2", worktree: "relative/path", repo_root: "/FAKE" }],
			});
			const [, prTick] = await start(pi);
			await sleep(50);
			assert.equal(
				pi.sent.filter((s) => s.content.includes("PERKINS ROUND DEBRIS")).length,
				0,
				"n07c: relative path is not actionable — no cleanup instruction",
			);
			all.push("N07 relative/invalid roots skipped: ok");
		}

		// ── N08: live-owner exemption + fail-closed ownership ─────────────
		{
			const root = mkdtempSync(join(tmpdir(), "nefario-n08-"));
			scratchDirs.push(root);
			const wt = join(root, "round-wt");
			mkdirSync(wt);

			// done old row + LIVE new row sharing the same worktree → exempt
			const pi = new FakePi({
				roundRows: [{ id: "demo-perkins-r1", worktree: wt, repo_root: root }],
				liveRows: [{ worktree: wt }],
				gitWorktree: { code: 0, stdout: `worktree ${root}\nworktree ${wt}\n` },
			});
			const [, prTick] = await start(pi);
			await sleep(50);
			assert.equal(
				pi.sent.filter((s) => s.content.includes("PERKINS ROUND DEBRIS")).length,
				0,
				"n08a: done row sharing a LIVE round's worktree is NOT a cleanup candidate",
			);
			all.push("N08 live-owner exemption on done-row branch: ok");

			// live-ownership query fails → no candidates, health note
			const pi2 = new FakePi({
				roundRows: [{ id: "demo-perkins-r1", worktree: wt, repo_root: root }],
				liveRows: { error: 1 },
				gitWorktree: { code: 0, stdout: `worktree ${root}\nworktree ${wt}\n` },
			});
			const [, prTick2] = await start(pi2);
			await sleep(50);
			assert.equal(
				pi2.sent.filter((s) => s.content.includes("PERKINS ROUND DEBRIS")).length,
				0,
				"n08b: failed live-ownership query manufactures NO candidates",
			);
			assert.equal(
				pi2.sent.filter((s) => s.content.includes("debris-live-ownership")).length,
				1,
				"n08b: fail-closed surfaces as a health note",
			);
			all.push("N08 ownership-query failure fails closed: ok");

			// registry query fails → no ORPHAN HUSK manufacture
			const pi3 = new FakePi({
				roundRows: [{ id: "demo-perkins-r1", worktree: wt, repo_root: root }],
				gitWorktree: { code: 128, stdout: "" },
			});
			const [, prTick3] = await start(pi3);
			await sleep(50);
			assert.equal(
				pi3.sent.filter((s) => s.content.includes("ORPHAN HUSK")).length,
				0,
				"n08c: failed registry query does not manufacture ORPHAN HUSK",
			);
			assert.equal(
				pi3.sent.filter((s) => s.content.includes("debris-registry")).length,
				1,
				"n08c: registry failure surfaces as health note",
			);
			all.push("N08 registry failure fails closed: ok");

			// positive control: real unowned registered debris still surfaces
			const pi4 = new FakePi({
				roundRows: [{ id: "demo-perkins-r1", worktree: wt, repo_root: root }],
				gitWorktree: { code: 0, stdout: `worktree ${root}\nworktree ${wt}\n` },
			});
			const [, prTick4] = await start(pi4);
			await sleep(50);
			const alerts4 = pi4.sent.filter((s) => s.content.includes("PERKINS ROUND DEBRIS"));
			assert.equal(alerts4.length, 1, "n08d: real unowned debris still surfaces");
			assert.doesNotMatch(alerts4[0].content, /ORPHAN HUSK/, "n08d: registered, not husk");
			all.push("N08 real unowned debris still surfaces: ok");
		}

		// ── R02: APPROVED alert is an observation, not a merge verdict ────
		{
			const pi = new FakePi({
				reviewJobs: [
					{ id: "demo-fix", pr: PR, pane_id: "w1:p1", pr_review: 0 },
				],
				gh: baseGh({ reviews: [] }),
			});
			const [, prTick] = await start(pi);
			await sleep(30);
			assert.equal(pi.sent.length, 0, "r02a: baseline silent");
			pi.world.gh = baseGh({
				reviews: [{ id: "rv1", state: "APPROVED", author: { login: "perkins-review[bot]" }, body: "lgtm" }],
			});
			await prTick();
			await sleep(30);
			const rv = pi.sent.filter((s) => s.content.includes("REVIEW APPROVED"));
			assert.equal(rv.length, 1, "r02b: APPROVED review alerts");
			assert.match(rv[0].content, /OBSERVED review event/, "r02b: framed as observation");
			assert.match(rv[0].content, /not a merge-readiness verdict/, "r02b: explicitly not a merge verdict");
			assert.match(rv[0].content, /verify independently/, "r02b: carries verify-before-merge provenance");
			assert.doesNotMatch(rv[0].content, /merge when ready/, "r02b: old unqualified merge wording gone");
			all.push("R02 APPROVED-as-observation wording: ok");
		}

		// ── R04: bare-number PR identity in the sensor ────────────────────
		{
			// full-slug repo column → explicit --repo
			const pi = new FakePi({
				reviewJobs: [
					{ id: "demo-fix", pr: "7", pane_id: "w1:p1", pr_review: 0, repo: "acme/demo" },
				],
			});
			const [, prTick] = await start(pi);
			await sleep(30);
			const prViews = pi.execLog.filter((e) => e.cmd === "gh" && e.args[0] === "pr" && e.args[1] === "view");
			assert.ok(prViews.length >= 1, "r04a: gh pr view called");
			assert.ok(
				prViews.every((e) => e.args.includes("--repo") && e.args.includes("acme/demo")),
				"r04a: bare number always carries explicit --repo acme/demo",
			);
			// review alert on a bare-number PR uses the canonical URL
			pi.world.gh = baseGh({
				reviews: [{ id: "rv9", state: "CHANGES_REQUESTED", author: { login: "human" }, body: "fix" }],
			});
			await prTick();
			await sleep(30);
			const cr = pi.sent.filter((s) => s.content.includes("REVIEW CHANGES_REQUESTED"));
			assert.equal(cr.length, 1, "r04b: bare-number review alert fires (was silently consumed)");
			assert.match(cr[0].content, /https:\/\/github\.com\/acme\/demo\/pull\/7/, "r04b: canonical URL constructed");
			// V2: the per-review anchor lookup queries the CANONICAL repo path
			// (owner/repo transposition in the synthetic match array would
			// otherwise degrade anchors silently)
			const apiCalls = pi.execLog.filter((e) => e.cmd === "gh" && e.args[0] === "api");
			assert.ok(
				apiCalls.some((e) => typeof e.args[1] === "string" && e.args[1].startsWith("repos/acme/demo/pulls/7/reviews")),
				"r04d: bare-number review anchoring queries repos/acme/demo/pulls/7/reviews",
			);
			all.push("R04 bare-number explicit --repo + canonical review URL: ok");

			// shortname repo → sensing skipped, no ambient gh call, health note
			const pi2 = new FakePi({
				reviewJobs: [
					{ id: "demo-fix2", pr: "9", pane_id: "w1:p2", pr_review: 0, repo: "demo" },
				],
			});
			const [, prTick2] = await start(pi2);
			await sleep(30);
			const prViews2 = pi2.execLog.filter((e) => e.cmd === "gh" && e.args[0] === "pr" && e.args[1] === "view");
			assert.equal(prViews2.length, 0, "r04c: NO gh pr view for unresolvable bare number");
			const notes = pi2.sent.filter((s) => s.content.includes("bare-pr-identity"));
			assert.equal(notes.length, 1, "r04c: one rate-limited identity health note");
			assert.match(notes[0].content, /ambient-repo lookup refused/, "r04c: refusal reason stated");
			all.push("R04 unresolvable bare number skipped (no ambient lookup): ok");
		}

		// ── V1: a failed PR-tick inventory must not kill PR-tick alerting ──
		// (stuckCheck consumes the typed union; co-present alerts still deliver)
		{
			const pi = new FakePi({
				jobs: [{ id: "job-a", pane_id: "w1:p1", status: "working" }],
				herdrAgents: { code: 1, stdout: "" },
				reviewJobs: [{ id: "demo-fix", pr: PR, pane_id: "w1:p1", pr_review: 0 }],
				gh: baseGh({ state: "MERGED" }),
			});
			const [, prTick] = await start(pi);
			await sleep(50);
			assert.equal(
				pi.sent.filter((s) => s.content.includes("PR MERGED")).length,
				1,
				"v1a: co-present PR-tick alert still delivers under a failed PR-tick inventory",
			);
			assert.equal(
				pi.sent.filter((s) => s.content.includes("debris-pane-inventory")).length,
				1,
				"v1b: the inventory failure surfaces as a health note (no crash, no silence)",
			);
			all.push("N04 typed union holds across ALL liveStatuses callers: ok");
		}

		// ── B15: orphan lens pane branch (removed-worktree cwd) + N07 skip ──
		{
			const root = mkdtempSync(join(tmpdir(), "nefario-orph-"));
			scratchDirs.push(root);
			const gone = join(root, "repo", "perkins-round-x"); // never created — swept
			const pi = new FakePi({
				herdrAgents: {
					code: 0,
					stdout: JSON.stringify({
						result: { agents: [{ pane_id: "w1:p9", agent_status: "idle", cwd: gone }] },
					}),
				},
			});
			const [, prTick] = await start(pi);
			await sleep(50);
			assert.equal(
				pi.sent.filter((s) => s.content.includes("ORPHAN LENS PANE")).length,
				1,
				"orph-a: pane at a removed perkins worktree surfaces (detection-only)",
			);
			all.push("N08 orphan lens pane branch covered: ok");

			// a relative perkins-ish cwd is UNKNOWN — never a cleanup instruction
			const pi2 = new FakePi({
				herdrAgents: {
					code: 0,
					stdout: JSON.stringify({
						result: { agents: [{ pane_id: "w1:p8", agent_status: "idle", cwd: "x/perkins-y" }] },
					}),
				},
			});
			const [, prTick2] = await start(pi2);
			await sleep(50);
			assert.equal(
				pi2.sent.filter((s) => s.content.includes("ORPHAN LENS PANE")).length,
				0,
				"orph-b: relative perkins-ish cwd gets NO cleanup instruction",
			);
			all.push("N07 orphan branch skips non-meaningful paths: ok");
		}

		console.log("ALL PASS\n" + all.map((a) => "  ✓ " + a).join("\n"));
	} finally {
		ints.restore();
		for (const d of scratchDirs) rmSync(d, { recursive: true, force: true });
	}
}

run().catch((err) => {
	console.error(err);
	process.exit(1);
});
