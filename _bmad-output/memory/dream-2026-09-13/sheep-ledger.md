# sheep-ledger shard — dream-2026-09-13

Reader: sheep-ledger. Scope: `ledger show` on all 25 census job rows (the
26th active row is `dream-2026-09-13` itself — not a job lane, excluded).
Marker 2026-09-11T02:10:37Z. All quotes verbatim from ledger notes/events.

## Candidates

### C1 — Wrong-scene capture invocation: boot the scene the runner is attached to
- Job/date: packet-plumber-3d-l1-intro-flow, 2026-09-11
- Quote: "ROOT CAUSE of the three 900s wedges: MY invocation loaded res://scenes/main.tscn (per the briefing/pVE proposal) - but the runner is attached to l1_arpanet.tscn (the project main scene); three runs booted a runnerless scene."
- Job/date: packet-plumber-3d-lighthouse-staging-fix, 2026-09-11
- Quote: "the three 900s wedges during the verification round were the WRONG-SCENE artifact (my invocation error), NOT a harness defect - pVE fail-loud harness verified working end-to-end (19s, all beats, exit 0) once the correct scene loads."
- Pattern: PP3D capture entries must invoke the scene the capture runner is bound to (the project main scene), never a briefing-named scene; wrong-scene boots produce silent wedges that masquerade as harness/engine defects and burn 900s grant entries (2 independent lanes same window).

### C2 — Display asleep = zero frames: frame-gated harnesses wedge silently; caffeinate is the standing wrapper
- Job/date: packet-plumber-3d-lighthouse-staging-fix, 2026-09-11
- Quote: "at ~03:50 local the display is ASLEEP - macOS delivers zero frames - and the frame-gated waits can never fire (the harness's own timeout is frame-gated too: silent wedge, no CAPTURE_FAIL print) ... FIX: run with the display awake (caffeinate -dimsu wrapper + the existing one-line window warning)"
- Job/date: packet-plumber-3d-inventory-dock, 2026-09-11
- Quote: "windowed capture-l1 baseline repro: exit 0, all 15 shots ... (caffeinate -dimsu, 900s bound, import precondition run"
- Pattern: windowed capture runs need display awake — caffeinate -dimsu + a one-line "don't close the pop-up" warning is now the codified capture wrapper; frame-gated timeouts can't self-report under display sleep.

### C3 — Static-only review ships execution-RED: invented (non-compiling) APIs through APPROVED rounds
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "cycle1 aborted (2 parse errors: invented ArrayMesh.add_surface -> add_surface_from_arrays x3 sites; PackedByteArray.hash() -> global hash())" — after "r3 APPROVED ... r4 APPROVED rebase-delta"
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "THREE engine-level defect classes found by execution and fixed (invented add_surface API, ambient re-seeding via water-boot face set, 64x64 headless viewport HUD pointer theft)"
- Pattern: another confirmed sighting of the catch-net doctrine (PR #22/#27 precedents): four static APPROVED rounds passed code that never compiled; only grant-released execution found it — merged-UNVERIFIED lanes owe the green-confirm entry.

### C4 — Fail-closed on unexpected diagnostics even at rc0; grant boundaries/amendments are user-blessed
- Job/date: packet-plumber-3d-constellation-view-v2, 2026-09-12
- Quote: "counted import 1/1 returned rc0 in 85.121s but unexpected diagnostics outside #29 ... Leak cause NOT established; do not waive as #29. No further native probes."
- Job/date: packet-plumber-3d-lighthouse-staging-fix, 2026-09-11
- Quote: "GRANT-BOUNDARY QUESTION for user: bless a WINDOWED capture entry (<=900s) to test the fix for real, or send back to pVE for a headless-runnable fail-loud."
- Pattern: stop-on-surprise includes rc0-with-unexpected-diagnostics (no warning waivers without established cause); when grant bounds can't exercise the real verification path, the boundary question escalates to the user and extensions land as blessed, receipted new entries.

### C5 — Shared _bmad symlink leaks CSVs into Godot translation import; local .gdignore facade fixes it
- Job/date: packet-plumber-3d-constellation-view-v2, 2026-09-12
- Quote: "locale warnings come from importing bmad-help.csv/tooling CSVs via pre-existing _bmad symlink"
- Job/date: packet-plumber-3d-constellation-view-v2, 2026-09-12
- Quote: "real local _bmad contains OWN .gdignore and 12 top-level forwards ... Shared target non-following manifest242 entries byte/metadata unchanged"
- Pattern: Godot worktrees that carry the `_bmad` symlink (the bootstrap gotcha) ingest its CSVs as translations producing locale-warning diagnostics; the sanctioned repair is a local facade dir (own .gdignore + forwards) leaving the shared target byte-identical.

### C6 — Never dispatch Perkins rounds during an active fix-and-push cycle; one delta at the stable head
- Job/date: packet-plumber-3d-constellation-view-perkins-r5, 2026-09-11
- Quote: "my dispatch raced pS8 push cycle: 482aec7 -> 40001174 landed mid-round; verdict NEEDS CHANGES posted per contract with BOTH blockers ALREADY ADDRESSED"
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "NO round dispatch until the branch STABILIZES (lane-2 execution converges: suite green + captures done); then ONE delta review at the FINAL head ... The r5 stale-sha round is the lesson (my dispatch raced the pushes)"
- Job/date: packet-plumber-3d-constellation-view-perkins-r6, 2026-09-11
- Quote: "2 blockers BOTH ALREADY FIXED at 482aec7+ per the verdict's own note (the lane-2 fix cycles landed mid-review"
- Pattern: ≥3 sightings in one lane: rounds dispatched onto a moving head are wasted work qualified "already addressed"; hold the row and fire ONE delta review at the converged stable head.

### C7 — Pre-PR manifest-bound review of an immutable candidate; rework runs as a separate branch
- Job/date: packet-plumber-3d-constellation-view-v2-perkins-r1, 2026-09-12
- Quote: "pre-PR independent review; acceptance bound to manifest and entry-17 actual evidence; no fix/push/PR/merge."
- Job/date: packet-plumber-3d-constellation-view-v2-perkins-r1, 2026-09-12
- Quote: "USER STARTING SEPARATE r2 working-source rework; r1 remains immutable candidate-01/source + detached review worktree at HEAD39d82d0 ... do not rewrite history or treat r1 as r2 approval."
- Pattern: new review shape on the Astra lane: review a source-manifest-bound candidate BEFORE any PR exists; the reviewed candidate stays immutable and user rework proceeds separately (r1 verdict "MAJOR REWORK NEEDED", 9 blockers, no GitHub review event).

### C8 — User look ruling reverses aesthetic direction; failed attempt closes unmerged with a held successor row
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "USER LOOK RULING (flat-mode REDESIGN relayed to pS8, in-branch): flat map ruled UGLY" ... then "LANE REASSIGNED (user ruling 2026-09-11): GLM attempt CLOSED UNMERGED (PR #26, lessons preserved in the close comment), v2 HELD row packet-plumber-3d-constellation-view-v2 carries the Astra reassignment (release = user confirms OpenAI tokens)"
- Pattern: vision-lane aesthetic verdicts are user-gated; a superseded attempt closes UNMERGED with preserved lessons, and the successor rides a HELD row keyed on an explicit release trigger (provider/token confirmation) — not a resume of the discarded branch.

### C9 — Grant release chains: post-merge main green-confirm gates the lane's suite/capture entries
- Job/date: packet-plumber-3d-l1-intro-flow, 2026-09-10
- Quote: "Run-grant lane-3 release chain (user order): #28 merges -> main full-suite green-confirm entry -> GREEN CONFIRM releases your suite+capture entries"
- Job/date: packet-plumber-3d-l1-intro-flow, 2026-09-10
- Quote: "DISCLOSURE RECORDED: branch suite execution was NEVER verified (run-grant lane 3 held) - the merged intro tests now sit on main unexecuted; the post-#28-merge main full-suite green-confirm may trip on them, in which case the fix loop re-engages on main"
- Pattern: known merged-UNVERIFIED debt doctrine, executed as explicit release chains across lanes (2 and 3) keyed on a main green-confirm entry the user ordered.

### C10 — 300s suite-calibrated bound too short for captures; 900s windows are blessed extensions
- Job/date: packet-plumber-3d-l1-intro-flow, 2026-09-11
- Quote: "capture sub-entry HIT THE 300s BOUND mid-boot (exit 124; no captures produced; world generation + 13-beat script needs a longer window)"
- Job/date: packet-plumber-3d-lighthouse-staging-fix, 2026-09-11
- Quote: "GRANT EXTENSION BLESSED (user, 2026-09-11 ~03:5xZ): ONE windowed capture entry (<=900s) on MERGED MAIN ... capture-class standing shape (windowed allowed; receipted, stop-on-surprise, self-closing bound)"
- Pattern: capture-class entries need ~900s (boot+world-gen eats 300s); the extension is a user-blessed standing shape with windowed allowed + the one-line window warning (see C2).

### C11 — User play finds live-input defects; captures must exercise the FULL gesture path with a fails-pre-fix discriminator
- Job/date: packet-plumber-3d-inventory-dock, 2026-09-11
- Quote: "dock drag drops never installed. Root cause: target acquisition measured ONLY the host ground-point projection (90px); the user's natural drops — visible building body at oblique angles (20-210px off) and especially the EMPTY LANDING SPOT (~554px off at street zoom) — silently cancelled ... Landing-spot pin labeled fails-pre-fix (the discriminator)."
- Job/date: packet-plumber-3d-inventory-dock, 2026-09-11
- Quote: "The never-exercised path also closed: capture 8c now performs the FULL gesture press->drag->drop->install (verified in-run + l1-08c2 drop frame vision-verified wired)"
- Pattern: live-input acquisition bugs live only on the real user gesture; capture scripts that shortcut the gesture never see them — the fix standard is a capture that performs the full gesture plus a discriminator pin that fails pre-fix.

### C12 — Authority attribution discipline: HUMAN RULING vs Gru/CEO application vs agent-origin reports
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-13
- Quote: "ATTRIBUTION CORRECTION 2026-09-13: the prior event labeled HUMAN RULING 2026-09-13 was Gru/CEO operational application of the existing 2026-09-12 human factory/autonomy ruling, not a new human-origin instruction ... future records label this Gru/CEO application and reserve HUMAN RULING for verified human-origin instructions."
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-12
- Quote: "the <=15min saved-evidence diagnosis is a Gru-scoped internal follow-up under the existing recovery objective, not a separately issued user authorization ... must not be represented as a new user run-word."
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-12
- Quote: "no-local-humanoid=ordinary-procurement was Gru applying the existing user factory/autonomy ruling, not a fresh direct user statement about cast assets."
- Pattern: 3 corrections in one lane-window: authority labels must distinguish verified human rulings from Gru/CEO applications of an existing ruling from minion self-reports; corrections preserve the mistaken records and supersede authority via side files (AUTHORITY-CORRECTION json).

### C13 — An ASSISTANT toolcall relayed via `herdr pane run` masquerades as user input (false cross-job stop)
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-13
- Quote: "pYQ session event9157beb9 at00:03:26.359Z was an ASSISTANT bash toolcall herdr pane run w85:p2 carrying PP3D closeout text; Herdr TUI injection made it appear role=user. It was PP3D-scoped and did not authorize pYR kill."
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-13
- Quote: "prior Selva stop was an orchestrator routing error, not human authority; restore the existing pYR saved session in the same pane/tree and resume ordinary source-bound rig intake/fit work."
- Pattern: relayed text landing in a pane is indistinguishable from typed user input; an urgent-looking cross-pane directive must be traced to its originating session event (role + pane routing) BEFORE killing panes — the false stop killed the Selva owner's pi; recovery restored the same pane/session in place with the false STOP preserved and its authority superseded.

### C14 — Result-oriented routine execution autonomy + factory completion contract (user rulings, canon PRs #34/#35)
- Job/date: orchestrator-result-oriented-routine-execution-autonomy-2026-09-12, 2026-09-12
- Quote: "routine import -> focused -> full <=300s entries, in-scope repair/retests, and matched visual/play verification are autonomous within the finite batch in the current execution/autonomy brief; no per-entry approval treadmill."
- Job/date: orchestrator-factory-completion-contract-2026-09-12, 2026-09-12
- Quote: "USER FACTORY CONTRACT: defined+briefed+assigned owns through verified completion; beginning/end user touchpoints; no midpoint approvals."
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-12 (in action)
- Quote: "IN-SCOPE RED + AUTONOMOUS RETRY: first asset-proof native attempt ... stopped before save/render because Image.has_data was checked before lazy pixel decode ... pYR corrected the validation and is retrying within the same original <=1800s proof allocation; no approval request."
- Pattern: the bounded-run approval treadmill is relaxed by durable user ruling into result-oriented autonomy: stop on RED, repair/retest in fresh bounded allocations (never reuse a closed allocation, never unchanged replay), escalate only real blockers/budget/scope; user touchpoints compress to beginning/end. Canon landed via Silas micro-PRs #34/#35.

### C15 — Silas self-edit canon lanes continue (Luna model, ruling docs under _bmad-output/memory)
- Job/date: orchestrator-result-oriented-routine-execution-autonomy-2026-09-12, 2026-09-12
- Quote: "Silas self-edit micro-PR: user ruling at _bmad-output/memory/result-oriented-routine-execution-autonomy-2026-09-12.md persisted to playbook, generated role guard, and AGENTS.md in isolated worktree; lavish not needed; PR direct; live root untouched."
- Pattern: the standing self-edit lane shape (pr_review=0, no lavish, direct PR, live root untouched) now runs on gpt-5.6-luna; user rulings durable at `_bmad-output/memory/<ruling>-<date>.md` before PR.

### C16 — Merged ≠ activated: live-root activation is a separate, user-gated sequence
- Job/date: orchestrator-selected-safety-fixes, 2026-09-12
- Quote: "PR #33 is contained in merged a59cf6d0, but live root remains vision-read-skill-cleanup at 0bdfcf8c with 33 tracked skill edits ... Safe future sequence only: make and verify an aside copy of .agents/skills; reconcile root-config commit and dirty-tree hashes without discard; activate/reload nefario-watch at an ops-safe checkpoint between sensor cadences and not mid-round; run bin/test-model-policy on the live root"
- Pattern: orchestrator tooling fixes merged to main are "deployment-pending" until explicitly activated on the dirty live root — aside-copy first, ops-safe checkpoint between sensor cadences, post-activation verification; no activation claimed at merge.

### C17 — Verification/debug harness timer leaks wedge the waiting pi; kill the exact owned chain only
- Job/date: orchestrator-selected-safety-fixes, 2026-09-12
- Quote: "Session had no growth since 15:21:49 while pi waited on its child bash PID 50124 running /tmp/n04-debug.mjs PID 50127; debug harness leaked real setInterval timers and never returned. Killed only exact pYY pi PID 43202 and its owned command chain; worktree and source edits preserved. Relaunching same pane ... and full-context handover"
- Pattern: a child harness that never returns (leaked timers) wedges the pane with NO provider error; classify via session-growth + child-process forensics, kill only the exact owned chain, relaunch same pane with full-context handover.

### C18 — Per-PR independent reviewer model override (durable user ruling) pins round main AND every lens
- Job/date: orchestrator-selected-safety-fixes, 2026-09-12
- Quote: "INDEPENDENT REVIEWER MODEL OVERRIDE (user ruling 2026-09-12, durable): the Perkins round + every lens for THIS PR runs zai-coding-cn/glm-5.3 at max — NO Astra fallback, no default GPT-chain round spawn."
- Job/date: orchestrator-selected-safety-fixes-perkins-r1, 2026-09-12
- Quote: "Apply exactly one continue to pYZ only after the current lens wave settles; no re-dispatch and no Astra/model fallback under the user ruling."
- Pattern: the GPT-chain model policy yields to explicit per-PR user overrides; the override pins the round main and every lens, and holds THROUGH 1302 bursts (one continue after wave settle, no fallback).

### C19 — Pre-verdict user merge → FYI post-merge round on the exact pre-merge target, canonical diff preserved
- Job/date: orchestrator-selected-safety-fixes-perkins-r1, 2026-09-12
- Quote: "USER RULING CORRECTION: this is a pre-verdict merge, not an approved terminal merge. Recover and finish the already-commissioned r1 as FYI post-merge on exact pre-merge target 7b823c9d ... using preserved canonical 3585-line diff ... Existing chunk-1 arrays are preserve-first; run missing chunk-2 seven-lens wave, verify/consolidate, and post one FYI comment on merged PR #33 (not approve/request-changes)."
- Pattern: the pre-verdict-merge doctrine with mega-diff chunking: recover the commissioned round against the EXACT pre-merge target/base with preserved canonical chunks (never regenerate against merged main), preserve-first arrays, one FYI comment — no formal review event, no fix loop.

### C20 — Orphaned paneless dispatched rows sit for days; verify pickup, supersede-and-redispatch
- Job/date: orchestrator-perkins-token-mint-retry-fix, 2026-09-10 → 09-11
- Quote: "SUPERSEDED: verified orphaned (no pane, never picked up in ~34h); re-dispatched as packet-plumber-3d-perkins-token-mint-retry-fix on a fresh worktree"
- Job/date: packet-plumber-3d-perkins-token-mint-retry-fix, 2026-09-11
- Quote: "RE-DISPATCH of the orphaned row (created 09-10 14:34Z, never picked up)"
- Pattern: paneless "no pane — pickup as a small tooling job" rows have no watcher coverage and can sit ~34h unnoticed; dispatched rows need aliveness verification, and the re-dispatch leaves the original row as a SUPERSEDED marker (with a wrong-prefix id caveat noted on the row).

### C21 — perkins-token mint flake closed by bounded retry (PR #31); the manual-retry workaround is retired
- Job/date: packet-plumber-3d-perkins-token-mint-retry-fix, 2026-09-11
- Quote: "bin/perkins-token mint flaked at PR22-r4 close (silent empty token), succeeded on manual retry 15 min later - add bounded mint retry (1-2 attempts + short backoff) + loud failure logging BEFORE the comment fallback; fallback stays last resort."
- Pattern: the owed tooling fix from the 09-10 fallback-comment finding shipped and merged — 1-2 auto retries + ~30s backoff + loud per-attempt stderr before the comment fallback; the sim suite caught a first-draft bug pre-commit.

### C22 — Briefing premises can be wrong about tree state (tracked vs untracked); preservation commits make live fixes durable
- Job/date: packet-plumber-3d-bmad-root-config-fix, 2026-09-11
- Quote: "the pW3 root-config fix was UNCOMMITTED on 4 tracked bmad-build files (fragile - the briefing premise 'untracked' was wrong for these files); committed locally on the vision-read-skill-cleanup branch"
- Pattern: verify tracked/untracked reality at execution instead of trusting the briefing; live canonical config fixes get committed (even local-only on an existing branch) so they survive.

### C23 — Root pull refusals remain the #28 landmine class; safe sync via `git fetch origin main:main`
- Job/date: packet-plumber-3d-perkins-token-mint-retry-fix, 2026-09-11
- Quote: "the root pull refusal during this close-out is the #28 landmine class (the root carries local branches + the pW3 fix) - documented, not an error"
- Job/date: orchestrator-factory-completion-contract-2026-09-12, 2026-09-12
- Quote: "Live orchestrator root is dirty on vision-read-skill-cleanup, so safe root-preserving sync used git fetch origin main:main (not pull/switch)"
- Pattern: the live root stays on its dirty Gru branch; close-outs sync refs with fetch-into-branch, never pull/switch — recurring standing trap, now with the standing recipe.

### C24 — Watcher/settle pre-classification notes on every transition are standard operating procedure
- Job/date: orchestrator-nefario-pr-readiness-audit, 2026-09-12
- Quote: "NEFARIO-WATCH 2026-09-12 13:46:39Z working->done classified FINISHED closeout, not clarify/error ... Same-status note used; no reopen or duplicate dispatch."
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "ECHOES 09:50-10:09Z (four watcher ticks racing the lane-reassignment close-out): pS8 pane transitions + no-agent-detected + the PR-closed-unmerged question = MY OWN close-out actions landing"
- Pattern: ≥8 sightings across every lane this window: same-status classification notes answer watcher/settle echoes (finished closeout vs clarify halt vs settle noise vs own-actions) — no second action ever.

### C25 — Lavish embedded iframes cannot reach loopback media; load-token URLs are transient
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-08
- Quote: "In the embedded iframe, clicking the visible Chorus 1 seek control left the Song position slider at 0 after 1.5s and produced no media request to audio server 4388; embedded seek/highlight/listening path therefore remains UNVERIFIED ... Lavish accepts only the current in-memory artifact load token/revision and a later load supersedes it; it is not a durable/public fallback."
- Pattern: lavish embedded review can't verify media interactions against a loopback server (sandbox boundary); the direct route works only with the current in-memory load token — media-linked lavish artifacts need a different verification path than embedded clicks.

### C26 — Lavish sessions ended_by=user are read-only; partial verdicts hold the row; verdicts preserved verbatim from state.json
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-09
- Quote: "f576... is now actually status=ended, ended_by=user, pending_prompts=2 ... same-session feedback cannot be consumed while the user-ended review is closed; do not reopen/reload, create a new session, or fabricate a PR."
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-09
- Quote: "story-verdict: Approve the creative story and cast only; actual caption alignment/timing is still open."
- Pattern: lavish gate lifecycle: a user-ended session with pending prompts still yields its verdicts (read from state.json verbatim, UID-tagged); verdicts can be PARTIAL (component gates: story approved, timing open) — the row holds, reopening requires explicit authority.

### C27 — Dependency installs get dry-run guards that abort BEFORE download; installer issues ≠ ABI findings
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-08
- Quote: "Setup stopped after 2.892s: uv dry-run proposed duplicate torch/numpy despite inherited packages; guard aborted before dependency install/model download. Installer issue, not ABI finding. NO RETRY honored"
- Pattern: local ML dependency setup under a user grant runs a dry-run guard first; abort-before-download preserves the budget and the finding is classified installer-vs-ABI honestly; no retry without authorization.

### C28 — Paid-generation lanes: spend ceilings with per-batch guards, hard-stop escalation, multi-pass canon lock with explicit supersessions
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-10
- Quote: "Ceiling US0 TOTAL for the entire board effort (0.277 spent; expansion est 4-7; HARD STOP + escalate if projection exceeds)"
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-10
- Quote: "CEILING DECISION WITH USER per hard-stop rule: full 52-shot re-population ~USD3.5 exceeds USD1.10 headroom - keep arc-aware mix OR small ceiling bump"
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-10
- Quote: "CANON LOCKED - FULL BOARD USER-APPROVED 2026-09-10 ... INHABITED city with cumbia/sonidero dancers where music plays (SUPERSEDES old no-crowds avoidance; early night quieter per arc)"
- Pattern: image-board production runs ceiling-guarded batches with per-image receipts/hashes, escalates the ceiling decision to the user at projection-exceed, preserves every pass (board-v1/v2), and locks canon at final approval with explicit supersession of prior creative constraints.

### C29 — User-initiated shared-Blender MCP toggles are expected events, not faults; restart_clearance receipts gate restarts
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-07
- Quote: "user manually enabled Blender MCP, then deliberately disabled it; fresh read-only blender_get_scene_info failed with Could not connect to Blender. Treat as expected intentional disablement, not provider/crash fault. Do not re-enable, restart Blender/addon"
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-07
- Quote: "Parent explicitly sets restart_clearance=false because live GUI render/bake/composite and unsaved state cannot be verified while MCP is intentionally disabled."
- Pattern: the 2026-09-09 shared-Blender forensics doctrine operating at scale: intentional user toggles produce connection failures that must not trigger retries/restarts; explicit clearance receipts (with jobs/playback/dirty state) gate any restart, and a newer explicit clearance supersedes an older withheld one.

### C30 — Parked/hold lanes don't need live panes; state-on-disk + documented hold + startup reconciliations
- Job/date: h3-local-production-queue, 2026-09-06
- Quote: "the pane DIED COMPLETELY (no herdr registration, zero node processes ...) Lane state fully preserved on disk ... The pane slot isn't recreated now: the lane is parked on a user-ruled hold, and idle-await doesn't need a live pane slot."
- Job/date: h3-local-production-queue, 2026-09-12
- Quote: "STARTUP RECONCILIATION 2026-09-12: no pane/process present; documented local H3 stand-down and Metal-native pivot hold remain in force ... trigger remains explicit pivot ruling."
- Pattern: rows parked on user-ruling holds tolerate complete pane death across days; reconciliations clear stale pointers and re-affirm the named resume trigger instead of recreating panes.

### C31 — Handover via file pattern when heredoc/shell quoting dies
- Job/date: packet-plumber-3d-l1-intro-flow, 2026-09-10
- Quote: "handover delivered via file pattern (first heredoc attempt died on shell parse - pane+launch unaffected)"
- Pattern: long/complex handovers survive shell-parse failures by writing the handover to a file and pointing the pane at it (single sighting here, matches the prompts-to-files craft law).

### C32 — /thinking xhigh in-place correction (max recorded at launch)
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-08
- Quote: "session JSONL initially recorded max at 19:05:02.286Z; in-place /thinking xhigh produced thinking_level_change xhigh at 19:11:17.014Z in same session/model/pane, no restart/kill/redispatch."
- Pattern: the 2026-09-09 launch-envelope doctrine executed: verify thinkingLevel after launch, correct in-place with a durable receipt when the envelope recorded `max`.

### C33 — $-expansion corruption corrected by argv-safe literal notes preserving history
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-10
- Quote: "LITERAL NOTE CORRECTION from approved pilot brief: live pilot allowance is US$5 TOTAL shared across both jobs ... historical shell-corrupted US//bin/bash wording is preserved as history and superseded by this literal record."
- Pattern: the 09-10/11 $-expansion class handled correctly: a literal correction note supersedes the corrupted amount while preserving the corrupted wording as history.

### C34 — Piped log tails lose the diagnostic head; request instrumented full-log reruns
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "PROCESS GAP OWNED: my invocation piped 'tail -30' so the log head (test output, first-error context, any earlier diagnostics) is lost; no rerun per stop-on-surprise ... REQUEST: authorize ONE instrumented rerun of the same suite command with full log capture (tee to file)"
- Pattern: verification entries must tee full logs (never tail-pipe); when the head is lost, the stop-on-surprise discipline converts to a static-analysis follow-up + an explicit instrumented-rerun request.

### C35 — Green control-worktree runs attribute post-rebase suite failures
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "all attributed via green origin/main control run: ambient re-seeding (water boot mesh face-set change -> SphereMesh restored + analytic morph grid), 64px headless viewport GUI consumption ... Control worktree /tmp/pp3d-main-control (origin/main) used for attribution only."
- Pattern: when a branch suite goes red after rebasing onto moved main, run the same suite on a clean origin/main control worktree to attribute each failure to merged-state vs branch defect before fixing.

### C36 — Suite runners abort silently on mid-suite runtime errors (no summary line)
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "the runner's await chain aborted mid-suite (a runtime error inside a test's run_all kills the coroutine silently, no summary)"
- Pattern: a Godot suite that exits 0/short-runtime with NEITHER per-script prints NOR the summary line = aborted coroutine, not a pass — the phantom-check counting discipline extended to the runner level (check for the 'SUITE RESULT:' line, not just exit codes).

### C37 — No-op re-dispatch lands on an already-done round; re-purpose the session as the next round
- Job/date: packet-plumber-3d-constellation-view-perkins-r5, 2026-09-11
- Quote: "round COMPLETE (no-op re-dispatch consumed: this session was launched with the stale r5 payload — r5 review was already posted ... ledger had been done; working-flip corrected). Proceeding as the r6 session."
- Pattern: a late re-dispatch can boot a fresh pane with a stale payload against a DONE row; recover by consuming it as the next round's session instead of a second pane.

### C38 — Backlog-only issue intake receipts (user-ruled no-work fences)
- Job/date: packet-plumber-3d-constellation-view-v2, 2026-09-12
- Quote: "BACKLOG INTAKE ONLY 2026-09-12: PP3D issues #34 ... User explicitly says no minion/implementation/design/native work, no fold into constellation, no resume of other stops, and no active dispatch rows required."
- Pattern: rapid user issue-filing (PP3D #34-#41 in one morning) receipts each as backlog-only with explicit no-dispatch/no-fold/no-ack-relay fences on the active row — intakes don't become work without a dispatch.

### C39 — Central no-PR evidence archive (_bmad-output/no-pr-evidence/) with hash-verified tarballs
- Job/date: packet-plumber-3d-constellation-view-v2, 2026-09-12
- Quote: "No-PR evidence centrally preserved: /Users/moses/code/_bmad-output/no-pr-evidence/packet-plumber-3d-constellation-view-v2/20260912-import-01/evidence.tar.gz SHA256 90452684...; cmp verified byte-identical to worktree archive."
- Pattern: no-PR halt evidence now preserves to a dedicated central archive (beyond implementation-artifacts) with SHA256 + cmp parity; concurrent writers avoid overwriting each other (parent-seal child dirs).

### C40 — Stuck-pane false positives on legitimate lavish polls; pane-screen advancement beats session-jsonl staleness during long turns
- Job/date: youtube-channel-selva-full-song-storyboard, 2026-09-09
- Quote: "pNS alert is legitimate user-facing foreground poll for NEW review 679eda53006944a5, not a wedged pane ... Interactive await is the contract; do not continue, kill, relaunch, close, or duplicate relay."
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-07
- Quote: "Session JSONL has not flushed beyond the 21:48:10 terminated event yet, but visible process activity confirms a long active recovery/generation, not a wedged pane. No second continue"
- Pattern: classify stuck-pane alerts by pane-read + live PIDs + poll ownership; during long turns the pane screen advances while the session jsonl lags — spend at most ONE continue, never a second while visibly advancing.

### C41 — Truthful wall-deadline closeouts: ALLOCATION WALL RED ≠ execution GREEN; no retrospective timeliness claims
- Job/date: youtube-channel-selva-electrica-assets-rigs, 2026-09-13 (quoting user directive)
- Quote: "Overall ALLOCATION WALL RED, NOT executionGREEN. No more native/source work ... Preserving/sealing late evidence now with actual timestamp, noretrospectivetimelinessclaim."
- Pattern: a wall-deadline miss is reported RED even when every entry executed green; late evidence is sealed with actual timestamps — honest-result reporting over deadline laundering (the user's own verbatim standard, worth canonizing).

### C42 — Vision unavailable → escalate, never fake; user routes glm-5.3-flash probe-proven
- Job/date: packet-plumber-3d-constellation-view, 2026-09-11
- Quote: "VISION UNAVAILABLE — escalated, not faked: Astra quota-exhausted, Sol quota-exhausted, local fallback connection-error." → "VISION EXACT-COPY CHECK COMPLETE (glm-5.3-flash route, user-routed 09-11 after k3 out; probe-proven on constellation-01)"
- Pattern: under the OpenAI hold, exact-copy vision checks halted honestly until the user routed a probe-proven glm-5.3-flash; vision verdicts are never fabricated while the route is down (matches the vision caveat doctrine).

## Anecdotes (single sighting, minor)

- **Godot banner vs README version**: "Godot 4.7.2 banner versus README4.7.1 is documentation/version mismatch, not runtime failure or engine drift/downgrade" (constellation-v2, 09-12).
- **Supervisor killpg EPERM + honest timing correction**: "supervisor unexpectedly raised PermissionError EPERM at os.killpg(pid,0) ... First brief relay overstated immediate timing; this correction preserves history" (constellation-v2, 09-12) — bounded-run supervisors must tolerate the process-group-already-gone case; relays get corrected with history preserved.
- **Review URL placeholder "None"**: "review URL: https://github.com/solarity-services/Packet-Plumber-3D/pull/33#pullrequestreview- None" (inventory-dock-perkins-r2, 09-11) — the placeholder-is-record-loss class recurred.
- **PI env stale pane ids**: "Actual Herdr current stable pane returned w85:pYQ (PI env w9T:p1 stale)" (constellation-v2, 09-12).
- **Single-account repos can't assign reviewers**: "Reviewer request not assignable: single-account repo (collaborators: mssoka only) — the user's capture review is the gate per dispatch" (inventory-dock, 09-11).
- **Wrong-prefix row id on re-dispatch**: "row id carries a packet-plumber-3d prefix from the re-dispatch - the fix is ORCHESTRATOR tooling" (pp3d-perkins-token-mint-retry-fix, 09-11).
- **Receipt race on helper session creation**: "first receipt read raced session creation before first prompt persisted; subsequent on-disk read now verifies" (selva-assets-rigs, 09-07).
- **Preserve-first close-out at scale**: "copied all 4,664 untracked files ... (134,536 KB) ... rsync dry-run confirmed byte/file parity" (selva-full-song-storyboard, 09-12).
- **Marker reconciliation to authoritative on-disk SHA**: "authoritative current STAGE-01-COMPLETE.json SHA89a986..., not earlier stale relay 4c9d8095" (storyboard, 09-09).
- **READY SET containing already-done rows**: "Queue checked; READY SET contains already-done historical rows, no new release dispatched" (factory-contract, 09-12).
- **Audit→fix routing**: readiness audit's "9 selected IDs ... all deferred to separately commissioned fix proposal" (nefario-pr-readiness-audit → selected-safety-fixes, 09-12) — the named-intake discipline for audit findings.
- **Design leanings recorded honestly in canon**: "user's leaning recorded honestly — network-engineer fantasy may favor more deliberate placement, deferred to playtest evidence" (inventory-dock, 09-12).
- **bmad-build review HALT workaround**: "no subagent facility in minion runtime: 3 standalone reviewer prompts materialized at _bmad-output/implementation-artifacts/review/..." (constellation-view, 09-10) — minions can't spawn subagents; reviewer prompts become files for separate sessions (2nd sighting of the class in this window, also inventory-dock).
- **Loopback audio server at resume**: "Board asset route repaired via existing loopback :4388 service; session/page HTTP 200 and artifact_failures cleared" (storyboard, 09-12) — lavish artifacts referencing _local-refs need the loopback pane alive at resume.
- **1302 burst killed a reporting turn mid-batch; one continue after settle** (storyboard, 09-10) — standard doctrine sighting under glm-only load.
