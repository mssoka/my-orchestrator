# sheep-ledger — candidate patterns (dream-2026-08-27)

Source: ledger events, window 2026-08-25T09:58:22Z → 2026-08-27T10:03Z (last-dream
marker forward). Depth rows pulled: packet-plumber-v2-arch-egress-migration,
packet-plumber-v2-look-node-legibility-diag, orchestrator-checkpr-review-recency.

## C1 — Minion self-swept its own pane mid-badge-out (pane-vanish class; "never close your own pane")
- Evidence: packet-plumber-v2-arch-egress-migration 2026-08-26 — "the pane VANISHED mid-badge-out (agent was closing its mega-minions after committing everything — all S1-S5 + review fold committed, suites green; no PR/ledger yet; likely self-swept its own pane in cleanup). Recovery: fresh pane w85:p1W in the SAME worktree handed a completion-only contract (push, PR per brief, ledger steps, field notes, notification; explicit DO-NOT-close-panes). Lesson candidate: minions must NEVER close their own pane."
- Evidence: packet-plumber-v2-arch-egress-migration 2026-08-26 — "the 5-story ladder + review fold shipped after the pane-vanish recovery; recovery minion completed push/PR/ledger-both-steps/field-notes/notification (shown:true)" (recovery fully succeeded).
- Note: NEW incident class. All work was committed but PR/ledger/notification steps died with the pane. Recovery = fresh pane in the SAME worktree + completion-only contract. Briefings should carry an explicit DO-NOT-close-panes clause for minions that do cleanup sweeps.

## C2 — Interactive design sessions (Sally): idle-await is the contract, alerts are halts/settle-echoes
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 — "INTERACTIVE HALT (correct behavior post-amendment): Sally presented fork #1 of 5 … Awaiting USER in-pane answers (direct-to-pane legit); idle-await is the contract. Settle/escalation per interactive doctrine."
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 14:10Z — "settle echo of the 12:59 interactive halt … pre-classified, no action."
- Evidence: packet-plumber-v2-link-vocab-redesign 2026-08-26 14:12Z/14:20Z — "INTERACTIVE HALT (Sally presenting fork 1 of the bake-off IN-PANE) … Awaiting USER fork ruling in pane (direct-to-pane legit). User actively driving; no escalation."
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 14:14Z — "No ops action; no escalation (user demonstrably present)."
- Note: NEW session shape (user ruling, mid-flight amendment): design minions (Sally persona, bmad-agent-ux-designer) ask forks in-pane and idle-await user rulings; [ADOPTED user ruling] recorded per fork. Watcher alerts on these rows are interactive halts or their settle echoes — not stalls; escalate only when the user is absent. A "PROCESS RESET (user, in-pane): no decisions without the user; earlier rulings revisitable not void" can restart the fork ladder mid-session.

## C3 — Design-session consolidation: session-merge with HANDOFF.md + preserved artifact dirs
- Evidence: packet-plumber-v2-link-vocab-redesign 2026-08-26 14:30Z — "SESSION-MERGED (user ruling: single Sally, Gru relay): link-vocab session handed off (HANDOFF.md verified in implementation-artifacts/link-vocab-redesign/) and merged into node-legibility … lavish page :4387 stays reachable (server survived the pane close)."
- Evidence: packet-plumber-v2-viscomm-shape-vocab 2026-08-26 07:24Z — "FOLDED into link-vocab-redesign — same user ruling gate (one [LOOK] decision, not two): the 7 unshaped packet classes get affordance-led shape proposals riding the link-language bake-off."
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 14:30Z — "SCOPE EXPANDED (user ruling: single Sally): this session now owns the FULL look language … HANDOFF.md is the entry point for the merged threads."
- Note: NEW convention: parallel design sessions consolidate into ONE session by user ruling; the durable handoff medium = HANDOFF.md + artifact dirs under implementation-artifacts/; the lavish server survives the source pane's close (pages stay reachable).

## C4 — Stray out-of-band pane input (human keystrokes into an agent pane) = errored-turn, external input
- Evidence: packet-plumber-v2-link-vocab-redesign 2026-08-26 12:54Z — "a stray /dedi (out-of-band pane input) opened pi's skill-navigator mid-lavish-poll, aborting the poll; page + server were INTACT … C-c exited the navigator; one continue resumed the turn. Classification: errored-turn (external input), recovered; NOT a provider incident."
- Note: NEW incident flavor: typed commands landing in a live agent pane (skill-navigator hijacks the turn). Recovery = C-c the navigator + one continue; verify artifacts/server intact before blaming the agent or provider.

## C5 — Silent spawn-time failure on dispatch (pane boots, agent never starts)
- Evidence: silas-perkins-r1-completion 2026-08-25 15:04Z — "silent spawn-time failure (no ledger write, no artifacts, no PR activity) — re-dispatched fresh on same row; ground state verified clean before retry."
- Evidence: dsh-dashboard-perkins-cap 2026-08-25 15:04Z — "silent spawn-time failure (no ledger write, no commits) — re-dispatched fresh on same row; repo verified clean at 5e9f6cc." (both rows in the same 15:02Z dispatch batch)
- Note: NEW dispatch failure class, batch-correlated (two panes of one batch): no error, no ledger write, nothing happens. Recovery = verify ground state clean (repo/tree untouched) + fresh re-dispatch on the SAME row.

## C6 — W3 spawn-turn stall, overnight variant: parks ~11h until the next alert window
- Evidence: packet-plumber-v2-arch-egress-migration-perkins-r2 2026-08-26T21:41Z/08-27T08:59Z — "spawn-turn stall after setup (app.diff/core.diff/prompts written, wave never launched — the documented W3 class; needed a nudge but overnight timing parked it ~11h with zero progress) … RESUMED ~08:5xZ (cache-miss 678m = fresh turn wake; source unconfirmed). Lesson: overnight stalls park until the next alert window — 11h dead time cost."
- Note: W3 class (main's spawn-turn ends mid-lens-wave, no error) now has an overnight flavor: the one-continue nudge is cheap but nobody is awake to fire it. Future Silas: check stalled-round rows at wake-up/startup sweep, don't wait for the alert window.

## C7 — glm-only quota regime: 1302 bursts + 1308 walls strike MULTI-PANE; probe-only timing; hold can park recovery for hours
- Evidence: packet-plumber-v2-arch-latency-egress-queue-model 2026-08-26 07:35Z — "1308 5-hour hard-cap wall killed the pane mid-turn (stated reset 19:22:01 — lie-prone, probe-only); rolling window freed within ~1min (double probe OK) → one continue revived."
- Evidence: packet-plumber-v2-link-vocab-redesign 2026-08-26 07:35Z — "same 1308 hard-cap wave (struck arch + link-vocab together); probe-flip revive with one continue."
- Evidence: packet-plumber-v2-viscomm-crisis-duck-perkins-r1 2026-08-26 07:04Z — "the 00:41Z 1302 burst killed the main mid-wave-spawn; probe-DOWN hold parked recovery ~6.4h … Wave state at recovery: all 7 lens panes done but ZERO lens JSONs on disk (spawn_wave logged prompt-seen=0 ×5 — briefs never landed before the burst)."
- Evidence: packet-plumber-v2-viscomm-crisis-duck-perkins-r1 2026-08-26 07:17Z — "second 1302 burst — struck AFTER chunk-1 completed (7/7 -c1.json on disk) while spawning chunk-2 … Chunked round rides the episodic-burst regime: expect wave completion despite main supervision gaps — lens JSONs are the durable signal."
- Evidence: packet-plumber-v2-arch-egress-migration-perkins-r1 2026-08-26 20:59Z — "1302 burst killed the main in setup (~5min in); probe OK after the standard wait → one continue."
- Evidence: packet-plumber-v2-arch-latency-egress-queue-model 2026-08-26 12:29Z — "1302 burst killed the main mid-lavish-skill-load … Probe false-negative re-probed OK → one continue revived."
- Note: Extends the documented burst taxonomy: (a) waves strike MULTIPLE panes at once (arch + link-vocab together); (b) a probe-DOWN hold legitimately parks an owed continue for ~6.4h — recovery resumes on the probe flip, not the clock; (c) a burst at wave-spawn time leaves lens panes "done" with ZERO JSONs (prompt-seen=0) — ground truth for wave state is lens JSONs ON DISK, never pane status.

## C8 — Connection-error waves: kill mains mid-wave/mid-verdict-post; 6/7-degraded lens disclosure extends to this class
- Evidence: packet-plumber-v2-viscomm-crisis-duck-perkins-r2 2026-08-26 15:48Z — "connection-error wave killed the main mid-c2-wave (after a 3600s lens wait; c1 6/7 JSONs durable — edge-c1 missing, c2 panes gone unread). Probe chatty-OK false-read → one continue … re-driving the wave (retry-then-degraded per skill)."
- Evidence: packet-plumber-v2-viscomm-crisis-duck-perkins-r2 2026-08-26 17:07Z — "edge-c1 lost to a connection wave, disclosed degraded (coverage re-proven via direct verification)."
- Evidence: packet-plumber-v2-viscomm-tie-deconflect-perkins-r2 2026-08-25 18:17Z — "connection-error wave killed the main MID-VERDICT-POST (all 7 lenses complete + consolidated.json) — one continue delivered per doctrine."
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-26 13:28Z — "connection/timeout wave mid-B1-fix — pane self-recovered (auto-retry, working again); no continue needed."
- Note: Connection-class (not 1302/1308) provider waves recur across the window. The 08-23 429-degraded-lens doctrine ("6/7 valid when findings were produced or coverage re-proven — disclosed, never faked") now exercised on connection-class loss too. Durable lens JSONs + consolidated.json again salvage verdicts even when the main dies mid-post.

## C9 — MEGA-DIFF protocol: `gh pr diff` 406s above ~20k lines; local canonical diff + two-class review
- Evidence: packet-plumber-v2-arch-egress-migration-perkins-r1 2026-08-26 — "MEGA-DIFF 54356L (gh pr diff 406'd >20k cap — canonical diff generated locally git diff 7ad48f9..1e9c783, substitution disclosed in brief + verdict); two-class protocol = full 7-lens waves on CODE chunks, mechanical bulk-verification on goldens/docs (T1 re-bless inventory cross-check + D6 replay proof)."
- Evidence: packet-plumber-v2-viscomm-crisis-duck-perkins-r1 2026-08-26 — "BIG-DIFF CHUNKING mandated — 3142L > 3000 threshold" (r2: "3270L", 2 chunked waves each).
- Note: NEW tooling limit + protocol: gh's diff API caps ~20k lines (406) — generate the canonical diff locally with `git diff <base>..<head>` and DISCLOSE the substitution. Diffs >3000L chunk into multiple 7-lens waves; goldens/docs bulk gets mechanical verification, not lenses. Rides alongside recurring lens-JSON repair chores (blind.json tab/control-char repairs: pr98 r1 08-25, egress r2 08-27 "blind-app JSON control-char repaired").

## C10 — Vacuous-pin blocker class still dominates; r2 fix-audits now re-run mutation legs independently
- Evidence: packet-plumber-v2-arch-egress-migration-perkins-r1 2026-08-26 — "4 blockers … the vacuous-gate class dominates (3/4)" (B2 AV-7 max-never-sum, B3 AV-4 util max, B4 residency pins — all mutation-proven).
- Evidence: packet-plumber-v2-viscomm-crisis-duck-perkins-r1 2026-08-26 — "B1: Dublin street-block recede mutation-vacuous (delete = full corpus green; needs a zone-crisis map_source fixture leg)."
- Evidence: packet-plumber-v2-arch-egress-migration-perkins-r2 2026-08-27 — "B1-B4 ALL FIXED with Perkins re-run RED mutation legs (B2 sum->Pipe_Critical; B4a 7 phantom ticks; B4b frozen 7; B3 got-90/got-200; B1 pitch RED x6)."
- Evidence: packet-plumber-v2-viscomm-gauge-telegraph-perkins-r1 2026-08-25 — "Perkins independently re-ran the mutation leg (gauge_read := raw → palcheck §6 FAILS ×2 + render suite FAIL; restored green, porcelain empty)."
- Note: Recurrence of the dream-2026-08-23 class (gate that can't fail = blocker; fix = mutation leg). NEW standard visible: r2 fix-audit rounds re-run the r1 mutation legs RED-then-GREEN INDEPENDENTLY as the acceptance proof, and verification passes also REJECT lens findings ("3 REJECTED after verification … 2 vacuous-coverage claims disproven by mutation").

## C11 — Advisory findings route as a batch GitHub issue folded onto the current PR (#101 pattern)
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-25 21:30Z — "advisory batch issue #101 opened (r2 warnings W3 jcol coverage + W1/W2 stale _pr_body_tie mirror) — EXECUTION FOLD: rides THIS PR per the amended Folded-advisories brief section; close #101 when crisis-duck ships."
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-26 19:02Z — "merged via PR #102 … #101 advisories (W3 pin, W1/W2 mirror) carried in the PR."
- Note: NEW routing convention (extends the issues-first audit doctrine): prior-round advisories become ONE batch issue, executed as a fold on the next PR of the owning lane, closed when that PR ships — not a separate job.

## C12 — Stranded-artifact hygiene fold: verbatim chore commit, preserve-first
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-25 23:43Z — "hygiene fold (Gru ruling): 8 uncommitted main-checkout _bmad-output artifacts … COPIED into the worktree + amendment relayed — ride the PR as a separate verbatim chore commit (preserve-first)." (shipped as chore commit 8c482ec)
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-25 23:43Z — "branch packet-plumber-v2-pr97-b1-wiring-pin (local+remote, fully merged) flagged redundant — deletion awaits USER word, do not delete."
- Note: NEW convention: uncommitted orchestrator-side artifacts stranded in a main checkout fold onto the in-flight PR as a SEPARATE verbatim chore commit (never reworded/reformatted); redundant-branch deletion is USER-gated, never Silas-initiated.

## C13 — check-pr-ready stale-CR false block → per-reviewer latest-verdict semantics (PR #15)
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 20:22Z — "r2 APPROVED … r1 CR superseded by the same bot's newer APPROVED (check-pr-ready flags the stale CR — tool recency gap, fix in flight)."
- Evidence: orchestrator-checkpr-review-recency 2026-08-25 20:24Z — "PR #15: check-pr-ready per-reviewer latest-verdict semantics — fixes the stale-CR false block (first hit PP #99 r2); live-verified NOT READY→READY rc=0; ops-tooling, pr_review=0 per doctrine."
- Note: NEW ops-tooling fix class: merge-readiness gating must evaluate each reviewer's LATEST verdict, not any verdict on the head. Observed state at dream time: PR #15 still open (row in-review) — fine, user merges ops PRs.

## C14 — Whole-lane abandonment by user ruling (DSH interlude): done-unmerged close-outs, sensor skip-notes
- Evidence: dsh-client-plugin-orchestrator-dashboard 2026-08-25 16:2xZ — "ABANDONED by user ruling: no longer using that orchestration. PR #1 CLOSED unmerged @77783f1 (work preserved on add/orchestrator-dashboard). perkins round on head 77783f1 = SKIP (superseded by this ruling — note-skip if the sensor fires)."
- Evidence: orchestrator-dashboard-perkins-bridge / dsh-dashboard-perkins-cap / orchestrator-dashboard-active-filter 2026-08-25 17:07Z — all "abandoned with the plugin interlude (user ruling 08-25) … No reopen, no re-dispatch"; cap work "shipped onto the abandoned branch — work lands nowhere; closed with the plugin abandonment."
- Evidence: orchestrator-minion-sweeper 2026-08-25 10:46Z — "CANCELLED by user ruling — auto-close adds risk without benefit … No residue: no repo, no loader row, no symlink, no sweep executed."
- Note: Moot-on-ABANDONMENT mirror of moot-on-merge: user closing a lane (PR closed unmerged) closes ALL riding rows as done-unmerged with work preserved on-branch; pre-work rows cancel with an explicit zero-residue check; any armed Perkins round on the abandoned head gets a note-skip.

## C15 — bash-3.2 wave-spawn collapse (macOS): lens wave folds into one pane; agent self-recovers
- Evidence: packet-plumber-v2-viscomm-tie-deconflect-perkins-r2 2026-08-25 — "bash-3.2 assoc-array bug collapsed wave-1 into one pane (agent self-recovered, relaunched 7 rooted lenses)."
- Evidence: packet-plumber-v2-viscomm-gauge-telegraph-perkins-r1 2026-08-25 21:32Z — dispatch note carries "bash-3.2 indexed-array wave note" proactively.
- Note: NEW technical gotcha: the lens-wave spawn script's assoc arrays break under macOS bash 3.2 — all lenses land in ONE pane. Detection = wave collapse at spawn; recovery observed = agent self-recovers (relaunches 7 rooted lenses); prevention = carry the note in round briefings / avoid assoc arrays in wave scripts.

## C16 — Docs-spine loop: lavish ratification gate BEFORE the PR; ratified content committed verbatim; pr_review=0
- Evidence: packet-plumber-v2-arch-latency-egress-queue-model 2026-08-26 12:40Z — "RATIFIED at the lavish gate (4/4 rulings, user verdict 'looks good') … Spine final (8 ADs) + 30-entry memlog + 3-lens review gate folded; Named follow-up: D-2 bandwidth_demand loaded-but-unwired — a BALANCE decision, not silent."
- Evidence: packet-plumber-v2-arch-latency-spine-docs 2026-08-26 12:43Z — "lavish EXEMPTION explicit — content ratified in-session 4/4: commit ratified spine+memlog+reviews verbatim … pr_review=0 — NO Perkins round on this docs PR (ratified content, ops/docs class)"; settle: "diff -r byte-identical … both pr steps run."
- Note: NEW canonical shape for architecture-spine work: ratify at a lavish gate FIRST, then a docs minion PRs the ratified artifacts VERBATIM (byte-identity is the acceptance check), lavish exemption + no Perkins. Balance-relevant discoveries found mid-arch (e.g. D-2 unwired demand) become NAMED stories in the implementing job's brief — never silent behavior changes.

## C17 — Design evidence → spec → implementation chain; user-play reports spawn read-only evidence jobs
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 00:19Z — "user report 01:12 local: 'i can barely see the nodes even when zoomed in' — first play on v2: READ-ONLY evidence job … main checkout, NO branch/worktree, captures + KYLE pixel measurements + lavish gate; parallel-safe (no edits). FIX-job routing (durable): user rules a direction → serialized fix heist blocked_by=…"
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 19:05Z — "DESIGN SESSION CONCLUDED: LOOK-SPEC.md (fix-job ready) + design-log.md (rulings in user's words) + direction-ruling + KYLE findings + measurements + captures preserved at implementation-artifacts/look-node-legibility/."
- Evidence: packet-plumber-v2-look-zoom-language 2026-08-27 09:38Z — "dispatched at fresh head 088cf00 … Scope per staged brief: L1-L4 DESIGN LOCKS; parked forks fenced out; Sally artifacts (LOOK-SPEC + design-log) are the spec inputs."
- Note: NEW end-to-end convention: user play feedback → read-only evidence job (parallel-safe, no branch) → interactive ruling session → durable spec artifacts (spec + design-log with rulings in the USER's words) → implementation heist briefed FROM those artifacts with parked forks explicitly fenced out.

## C18 — Row hygiene gaps persist: pr_review column 0 despite briefing; round-row self-create; typo'd round-row id
- Evidence: packet-plumber-v2-viscomm-gauge-telegraph 2026-08-25 21:26Z — "pr_review column was 0 (briefing said 1 — the 08-12 class again) → SQL-fixed on this row AND crisis-duck before it bit."
- Evidence: packet-plumber-v2-viscomm-gauge-telegraph-perkins-r1 2026-08-25 21:32Z — "Perkins self-created row (Silas pre-add missing)."
- Evidence: packet-plumber-v2-viscomm-tie-deconflect-perkins-r2 2026-08-25 — round row id is "tie-deconflect" while the parent job is "tie-deconflict" (typo'd round id; dedup relies on the parent=/sha= note fields instead).
- Note: Recurrence of documented classes ~2 weeks on: verify-and-fix `pr_review` COLUMN at every in-review transition; Silas pre-adds round rows (exact `<job-id>-perkins-rN`) before dispatch; a typo'd round id silently breaks id-based dedup — the parent=/sha= note fields saved it here.

## C19 — Silas as round-completion agent (durable artifacts salvage); watchman caught a Gru death mid-window
- Evidence: silas-perkins-r1-completion 2026-08-25 16:05Z — "Silas relaunched 15:53Z by user (watchman flagged Gru dead 15:54Z; Gru back 16:00Z); executing per briefing — lens wave artifacts validated (18 findings parse OK), verifying independently then posting verdict."
- Evidence: silas-perkins-r1-completion 2026-08-25 16:10Z — "verdict NEEDS CHANGES posted on PR #99 via perkins-review app; independently re-verified load-bearing findings incl. live mutation probe; worktree clean at 4b3a887."
- Note: The documented salvage path (complete artifacts → verdict posted by a completion agent) exercised end-to-end on a round orphaned by an orchestrator-context loss; the night-watchman's Gru-death detection + user relaunch also worked as designed. Future Silas: a dispatched completion-contract row is the sanctioned shape for dying-mid-round salvage.

## Observed state notes (not candidates)
- orchestrator-checkpr-review-recency: row `in-review`, PR #15 open (ops PR awaits user merge) — not stale, just open.
- egress-migration-perkins-r2 close-out: "The 'round 3 pending' tick in the same alert = stale sensor echo (loop closed at APPROVED — no r3)" — echo pre-classified, consistent with doctrine.
- Billing-block CI signature recurred note-only ~5×/day (runs 32970176204/32987842900/98334058791 — 3-6s, zero logs) across #103/#104; standing ruling held every time, local ground truth gated all merges. No new doctrine needed.
- The whole viscomm→arch→look belt (gauge-telegraph ← tie-deconflict; crisis-duck ← gauge-telegraph; egress-migration ← crisis-duck; look-zoom-language ← egress-migration) ran on paneless blocked_by rows with named merge-close-out release triggers, each release resolving a fresh head — the documented trigger-graph default, zero misfires in-window.
