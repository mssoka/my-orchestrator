/**
 * nefario-watch conflict sensor — end-to-end harness.
 *
 * Loads the REAL extension (no reimplementation), fakes only the
 * ExtensionAPI boundary (pi.exec / pi.sendMessage / setInterval), and
 * drives it through its real lifecycle: session_start (which runs the
 * pane-watcher tick + the initial PR tick) and the captured 5-min PR-tick
 * callbacks. The simulated "conflict" is a fake `gh pr view` response —
 * the sensor logic, dedup maps, alert text, and sendMessage delivery all
 * run for real.
 *
 * Run: node --experimental-strip-types test/nefario-watch-conflict.test.ts
 * (Node >= 22.6; repo has no package.json — this is the parse+behavior
 * gate for .pi/extensions/nefario-watch.ts).
 */
import { strict as assert } from "node:assert";
import nefarioWatch from "../.pi/extensions/nefario-watch.ts";

const SHA1 = "1111111111111111111111111111111111111111";
const SHA2 = "2222222222222222222222222222222222222222";
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

interface JobShape {
	id: string;
	pr: string;
	pane_id: string;
	pr_review: number;
}

class FakePi {
	sent: Array<{ content: string; opts: unknown }> = [];
	startHandler: (() => Promise<void>) | null = null;
	private gh: GhShape;
	private jobs: JobShape[];
	private rounds: Array<{ id: string; status: string; note: string | null }>;
	constructor(
		gh: GhShape,
		jobs: JobShape[],
		rounds: Array<{ id: string; status: string; note: string | null }>,
	) {
		this.gh = gh;
		this.jobs = jobs;
		this.rounds = rounds;
	}

	on(evt: string, h: unknown) {
		if (evt === "session_start") this.startHandler = h as () => Promise<void>;
	}

	async exec(
		cmd: string,
		args: string[],
		_opts?: unknown,
	): Promise<{ code: number; stdout: string; stderr: string }> {
		if (cmd === "sqlite3") {
			const sql = args[2] ?? "";
			if (sql.includes("parent")) {
				// perkinsRounds: SELECT ... WHERE parent = ... AND id LIKE ...
				return { code: 0, stdout: JSON.stringify(this.rounds), stderr: "" };
			}
			if (sql.includes("status != 'done'")) {
				// pane watcher: SELECT ... WHERE status != 'done' ...
				return { code: 0, stdout: "[]", stderr: "" };
			}
			// inReviewJobs: SELECT ... WHERE status = 'in-review' ...
			return { code: 0, stdout: JSON.stringify(this.jobs), stderr: "" };
		}
		if (cmd === "gh") {
			if (args[1] === "api") {
				// reviewUrls: repos/<o>/<r>/pulls/<n>/reviews
				return {
					code: 0,
					stdout: JSON.stringify([
						{ node_id: "rv2", html_url: PR + "#pullrequestreview-2" },
					]),
					stderr: "",
				};
			}
			return { code: 0, stdout: JSON.stringify(this.gh), stderr: "" };
		}
		if (cmd === "herdr") {
			return {
				code: 0,
				stdout: JSON.stringify({ result: { agents: [] } }),
				stderr: "",
			};
		}
		if (cmd === "bash") {
			// dreamCheck: BASELINE — never alerts in tests, never touches disk.
			return { code: 0, stdout: "BASELINE\n", stderr: "" };
		}
		throw new Error("unexpected exec: " + cmd + " " + args.join(" "));
	}

	sendMessage(msg: { content: string }, opts: unknown) {
		this.sent.push({ content: msg.content, opts });
	}
}

/** Patch setInterval to capture (not schedule) callbacks. */
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

const JOB: JobShape = {
	id: "demo-fix",
	pr: PR,
	pane_id: "w1:p1",
	pr_review: 0,
};

function baseGh(over: Partial<GhShape> = {}): GhShape {
	return {
		state: "OPEN",
		headRefOid: SHA1,
		mergeable: "MERGEABLE",
		mergeStateStatus: "CLEAN",
		baseRefName: "develop",
		statusCheckRollup: [],
		reviews: [],
		...over,
	};
}

/** Boot the extension and run session_start; returns the freshly
 * registered 5-min PR-tick callback (each start registers exactly two:
 * the 30s pane tick, then the 5-min PR tick). */
async function start(pi: FakePi): Promise<() => void> {
	process.env.PI_SILAS = "1";
	nefarioWatch(pi as never);
	assert.ok(pi.startHandler, "session_start handler registered");
	const before = intervalCallbacks.length;
	await pi.startHandler({}, { cwd: "/Users/moses/code" });
	assert.equal(intervalCallbacks.length, before + 2, "two intervals registered");
	return intervalCallbacks[intervalCallbacks.length - 1];
}

async function sleep(ms: number): Promise<void> {
	return new Promise((r) => setTimeout(r, ms));
}

async function run() {
	const ints = captureIntervals();
	try {
		const all: string[] = [];

		// ── 1. Conflict sensor: alert, dedup, re-arm ─────────────────────
		{
			const pi = new FakePi(
				baseGh({
					mergeable: "CONFLICTING",
					mergeStateStatus: "DIRTY",
				}),
				[JOB],
				[],
			);
			const tick = await start(pi);
			let alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "c1: initial CONFLICTING alert fires");
			assert.match(alerts[0], /demo-fix: MERGE CONFLICT —/, "c1: job named");
			assert.match(alerts[0], /#7/, "c1: PR number in alert");
			assert.match(alerts[0], /rebase onto develop/, "c1: base branch");
			assert.match(alerts[0], /force-push/, "c1: relay instruction");
			assert.match(alerts[0], /w1:p1/, "c1: pane id present");
			all.push("c1 initial alert: ok");

			// Same state re-poll → no re-alert.
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "c2: same-state re-poll silent");
			all.push("c2 same-state dedup: ok");

			// Conflict resolved → no alert, but re-arms.
			pi.gh = baseGh();
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "c3: clean state silent");
			all.push("c3 clean silent: ok");

			// Conflict again → second alert (transition-based dedup).
			pi.gh = baseGh({
				mergeable: "CONFLICTING",
				mergeStateStatus: "DIRTY",
			});
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 2, "c4: re-conflict alerts again");
			all.push("c4 re-conflict re-alert: ok");
		}

		// ── 2. Merge sensor unregressed ──────────────────────────────────
		{
			const pi = new FakePi(baseGh({ state: "MERGED" }), [JOB], []);
			const tick = await start(pi);
			let alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "m1: MERGED alert fires");
			assert.match(alerts[0], /PR MERGED/, "m1: merge text");
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "m2: terminal alert once");
			all.push("merge sensor: ok");
		}

		// ── 3. CI sensor unregressed (once per sha, re-arm on green) ────
		{
			const pi = new FakePi(
				baseGh({
					statusCheckRollup: [
						{ status: "COMPLETED", conclusion: "FAILURE", name: "build" },
					],
				}),
				[JOB],
				[],
			);
			const tick = await start(pi);
			let alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "ci1: failing check alerts");
			assert.match(alerts[0], /CI FAILING/, "ci1: ci text");
			assert.match(alerts[0], /build/, "ci1: check named");
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "ci2: same sha no re-alert");
			pi.gh = baseGh(); // green — re-arm
			await tick();
			await sleep(30);
			pi.gh = baseGh({
				headRefOid: SHA2,
				statusCheckRollup: [
					{ status: "COMPLETED", conclusion: "FAILURE", name: "build" },
				],
			});
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 2, "ci3: new failing sha alerts again");
			all.push("ci sensor: ok");
		}

		// ── 4. Review sensor unregressed (silent baseline, new alerts) ──
		{
			const pi = new FakePi(
				baseGh({
					reviews: [
						{ id: "rv1", state: "CHANGES_REQUESTED", author: { login: "human" }, body: "fix it" },
					],
				}),
				[JOB],
				[],
			);
			const tick = await start(pi);
			let alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 0, "rv1: first sighting baselined silently");
			pi.gh = baseGh({
				reviews: [
					{ id: "rv1", state: "CHANGES_REQUESTED", author: { login: "human" }, body: "fix it" },
					{ id: "rv2", state: "APPROVED", author: { login: "human" }, body: "lgtm" },
				],
			});
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "rv2: new review alerts");
			assert.match(alerts[0], /REVIEW APPROVED by human/, "rv2: review text");
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "rv3: same reviews no re-alert");
			all.push("review sensor: ok");
		}

		// ── 5. Perkins sensor unregressed (in-memory + durable dedup) ───
		{
			const perkinsJob: JobShape = { ...JOB, pr_review: 1 };
			const pi = new FakePi(baseGh(), [perkinsJob], []);
			const tick = await start(pi);
			let alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "pk1: pending round alerts");
			assert.match(alerts[0], /Perkins review pending/, "pk1: perkins text");
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "pk2: in-memory suppress re-alert");
			pi.rounds = [
				{ id: "demo-fix-perkins-r1", status: "done", note: "sha=" + SHA1 },
			];
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 1, "pk3: durable round row dedups");
			pi.gh = baseGh({ headRefOid: SHA2 }); // new sha — durable dedup gone
			await tick();
			await sleep(30);
			alerts = pi.sent.map((s) => s.content);
			assert.equal(alerts.length, 2, "pk4: new sha dispatches next round");
			all.push("perkins sensor: ok");
		}

		console.log("ALL PASS\n" + all.map((a) => "  ✓ " + a).join("\n"));
	} finally {
		ints.restore();
	}
}

run().catch((err) => {
	console.error(err);
	process.exit(1);
});
