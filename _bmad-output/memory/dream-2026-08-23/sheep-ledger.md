# SHEEP-LEDGER shard — dream-2026-08-23

Marker: 2026-08-21T18:49:59Z. Sources: `bin/ledger events 700` (full post-marker stream read end-to-end), `bin/ledger queue`. Read-only; no writes performed.

The window is dominated by ONE story: the Packet-Plumber v2 design wave (15 PRs merged in ~30h under a GH-Actions billing block, a both-providers-down HOLD, and ~30 Perkins rounds), plus an orchestrator-repo tooling burst (PRs #8–#14). Candidates below; singleton vs 2+ called out per section.

## Material summary (jobs with post-marker activity)

- **dream-2026-08-21** — boundary event: done 18:50:06Z, "16 auto proposals… marker written 18:49:59Z" (the marker itself).
- **orchestrator-playbook-consolidation-u2** — PR #8 merged 08-21 20:12Z; model policy single-voiced (k3→glm-5.3→HOLD); KYLE rename rode as post-merge follow-ups.
- **packet-plumber-v2-look-polish (+perkins-r1)** — PR #75 user-merged PRE-verdict 08-21 20:12Z; r1 completed as FYI on the merged PR (READY TO MERGE, posted as comment).
- **orchestrator-playbook-diet** — PR #9 merged 08-21 23:32Z; playbook 1,337→713 core + 597 annex; lavish gate; clarify-halt (skill pivot?) ruled keep-as-dispatched.
- **orchestrator-vision-tooling** — PR #10 merged 08-22 00:17Z; bin/vision-read re-pointed to glm-4.6v; flagged missing skill symlink + stale lmstudio refs.
- **orchestrator-night-watchman-hardening** — PR #11 merged 08-22 00:17Z; launchd PATH fix; TOOL-BROKEN vs provider-DOWN probe class.
- **orchestrator-role-skills** — PR #12 merged 08-22 00:27Z; role-blocks generator (paste-blocks + gen-role-blocks + drift check); Gru post-#12 direct-push canon window confirmed (14c76d5).
- **silas-ghstatus-test-stub** — PR #13 merged 08-22 00:27Z; FakePi githubstatus curl stub.
- **silas-round-debris-sensor** — PR #14 merged 08-23 10:37Z; 7th nefario-watch sensor, detection-only (done-round worktrees/panes + orphan lenses), planted-husk validated.
- **packet-plumber-v2-design-audit** — no-PR job done 08-22 05:03Z; lavish report + notification shown:true; MM press-kit refs dropped at `_local-refs/mm/` by user ruling (IP guardrail).
- **packet-plumber-v2-pace-tuning (+r1)** — PR #76 merged 08-22 15:01Z; pace 4x + spawn 2x; fun-test gate OPENED; merge was the release trigger for the 7-job wave.
- **packet-plumber-v2-network-pop (+r1)** — PR #77 merged 08-22 16:36Z; APPROVED 0 blockers (verdict recovered from self-close).
- **packet-plumber-v2-node-clarity (+r1,r2)** — PR #78 merged 08-22 18:01Z; r2 = rebase-delta after #77 collision.
- **packet-plumber-v2-blender-silhouettes (+r1-r3)** — PR #79 merged 08-22 19:16Z; r3 parked under HOLD then MOOT on merge.
- **packet-plumber-v2-estate-spawning (+r1-r3)** — PR #80 merged 08-22 19:21Z; r3 re-targeted ×2 then moot on merge.
- **packet-plumber-v2-sound-immediacy (+r1,r2)** — PR #81 merged 08-22 18:06Z; acceptance lens 429-degraded, guarded.
- **packet-plumber-v2-motion-readability (+r1-r4)** — PR #82 merged 08-22 23:26Z; user-caught "NEVER APPROVED" correction; r4 APPROVED execution-verified.
- **packet-plumber-v2-scale-depth (+r1,r2)** — PR #83 merged 08-22 23:31Z; r2 confirmation moot on merge.
- **packet-plumber-v2-noc-overlay (+r1,r2)** — PR #85 merged 08-22 23:26Z; D-key ruling saga (clarify → amendment → FINAL ruling).
- **packet-plumber-v2-spawn-feel (+r1-r4)** — PR #84 merged 08-23 06:23Z; last wave rebase; r4 flipped glm→k3 mid-round after 1308.
- **packet-plumber-v2-ambience (+r1,r2)** — PR #86 merged (post-08-23 08:20Z); B1 = ffmpeg non-determinism caught by Perkins.
- **packet-plumber-v2-font-overhaul (+r1-r6)** — PR #87 merged 08-23 15:43Z MERGE-LAST; r6 superseded by final rebase, swept deliberately (no r7 vs imminent merge).
- **packet-plumber-v2-blender-sculpt (+r1,r2)** — PR #88 merged 08-23 09:09Z; lavish look gate; r2 moot (merged before confirmation posted).
- **packet-plumber-v2-camera-zoom (+r1-r4)** — PR #89 merged 08-23 14:11Z; r4 round main self-flipped k3 mid-wave.
- **packet-plumber-v2-dublin-map-spike (+r1-r3)** — PR #90 merged 08-23 14:12Z; lavish gate APPROVED (density 1in6).
- **packet-plumber-v2-noc-player-toggle (+r1-r3)** — PR #91 merged 08-23 14:38Z on the r3-reviewed head; r3 moot mid-review.
- **packet-plumber-v2-noc-readability-2 (+r1-r3)** — IN FLIGHT: PR #92; r1/r2/r3 all CHANGES_REQUESTED; minion folding B1'' (tray-chip dead zone) at 18:49Z.
- **packet-plumber-v2-flow-focus** — dispatched 08-23 10:16Z, RECALLED ~11:1xZ ("was a QUESTION, not a directive"), row blocked on `user-design-exploration(?)`, swept with groundwork harvested.
- **dream-2026-08-23** — Bob dispatched 08-23 18:54Z (k3, provenance verified).
- Queue at read time: 15 done rows READY (whole v2 belt complete); only flow-focus blocked.

## Candidate patterns

### 1. Fix-folds regress themselves — the NEXT fix-audit round is the catch (2+ sightings)

Sightings:
- packet-plumber-v2-noc-readability-2, 2026-08-23 18:48Z: "NEW B1'': the W5' plate press-swallow DEADENS the two rightmost tray chips that paint over the plate — swallow (main.odin:1201) runs before the tray hit-test" — the r2 fold's own W5' fix regressed the tray; "the new blocker is the W5' fix's own regression (same surface-ownership class)".
- packet-plumber-v2-noc-readability-2, 2026-08-23 18:09Z: "r1 fold fully verified fixed; the new blocker is in the header row of the legibility evidence itself" — B1' header collision ('loS&A' overlap + clipped /3s) introduced by the fold's own evidence table.
- packet-plumber-v2-camera-zoom, 2026-08-23 10:20Z (partial): r3 B1 "effect_pan live-zoom clamp bug (drag during pullback ease = past-world-edge + void)" — bug in the mid-flight-ruling pullback feature added after PR open.

Generalizes: a fold is not safe because Perkins verified the intent — the fix-audit loop must keep re-firing until a round posts APPROVED, because each fold can introduce its own regression on the same surface. The loop worked exactly as designed (3 rounds, each verifying the prior fold + catching a new one).

### 2. Vacuous pins are the dominant blocker class; "mutation-proven" is the fix standard (2+, ~5 sightings)

Sightings:
- packet-plumber-v2-font-overhaul, 2026-08-23 10:28Z: "B1 gate-10 VACUOUS (mutation-proven: passes with overlay never drawn, 775>=500 from background; verb skips flip+swizzle overlay.odin:106-107)".
- packet-plumber-v2-camera-zoom, 2026-08-23 10:20Z: "W4 pin vacuous (router-before-seed — code correct, pin wrong)".
- packet-plumber-v2-spawn-feel, 2026-08-22 21:51Z: "B2 vacuous predictor pin (out-of-span fixture = tautology; use in-span + negative case)".
- packet-plumber-v2-motion-readability, 2026-08-22 21:21Z: "activation unpinned (interp_alpha default param — dropping the arg passes every gate)".
- Fix standard shown working: noc-player-toggle r2 13:38Z "B1 dismissal FIXED (mutation re-run fails), W1 boot defaults FIXED (flip fails 3 tests), W2 nav leg FIXED (ROW_COUNT->4 wraps+fails)"; font r5 12:43Z "gate-10 dual-render diff MUTATION-PROVEN (0 px mutated -> gate FAILS exit 1; 54k healthy)".

Generalizes: a pin/gate that cannot be made to FAIL by deleting/mutating the thing it guards is not a pin — minions should ship every pin with its mutation leg (delete-the-call / mutate-the-pixels / flip-the-default) unprompted; Perkins treats "mutation re-run fails" as the acceptance evidence.

### 3. Post-HOLD review-record audit before any merge — USER-CAUGHT miss (2+ sightings)

Sightings:
- packet-plumber-v2-motion-readability, 2026-08-22 19:20Z: "CORRECTION (user-caught, 19:2xZ): #82 is NOT APPROVED — single review on the PR = r1 CHANGES_REQUESTED @a57b68c… Minion's fix fold (0c030d75) + rebase (1a65db38) were NEVER verified — no r2 posted. STRUCK from merge-ready until APPROVED lands on the CURRENT head."
- packet-plumber-v2-estate-spawning, 2026-08-22 19:20Z: "AUDIT PASS: r1 (5000566578 16:25Z) + r2 (5000695134 17:37Z) APPROVED both verified on GitHub — claims stand." — the same audit applied clean elsewhere.
- Companion mechanic (2+): parked rounds targeting stale shas at HOLD lift — motion-r2 19:20Z "SWEEP AT PROBE FLIP (Gru ruling): do NOT resume this parked round — it targeted stale sha 3635de0 and never posted… dispatch a FRESH round on CURRENT head"; estate-r3 19:20Z "r3 parked worktree targets be7c0fa — STALE vs the current estate head 0fb1e90… do NOT resume the be7c0fa worktree".

Generalizes: after a HOLD (or any park), before merging anything: audit each PR's actual GitHub review record (not minion claims, not ledger notes), and never RESUME a parked round whose target sha went stale — sweep + fresh dispatch on the current head. The one time the audit was skipped a never-approved PR reached the merge-ready list and the user caught it.

### 4. USER RULING: parked vision rounds wait for k3 — do NOT resume on glm (1 ruling, applied to 2 rows)

Sightings:
- packet-plumber-v2-font-overhaul-perkins-r5 + camera-zoom-perkins-r4, 2026-08-23 10:58Z (identical text ×2): "RESUME TRIGGER UPDATED (user ruling 08-23 ~11:0xZ): WAIT for kimi k3 (cycle refresh ~1h) — do NOT resume on glm. Resume = k3 probe OK -> continue p2Z0 (k3 sees images natively — vision caveat lifts). The hourly nefario-watch probe auto-catches the k3 flip + alerts; resume then."
- Corollary, noc-readability-2 2026-08-23 17:28Z: "k3 BACK UP (17:28:42Z flip, probe-verified OK 17:3xZ) — the next round (r2…) routes to kimi/k3 primary (vision INLINE, no caveat); glm-5.3 remains fallback."

Generalizes: for rounds with visual evidence, "any reasoning provider up" is NOT the resume condition — the resume trigger is the provider whose VISION the round needs; a glm resume buys a mechanical-only verdict. Probe flips route new dispatches to k3 immediately.

### 5. glm 1302 bursts: new flavors — burst-at-launch, mid-burst-continue, post-reset cycling (2+, ~15 sightings)

Sightings:
- Burst AT LAUNCH (fresh pane, tiny session): dublin-r3 2026-08-23 09:13Z "1302 burst at launch 09:12Z (session 2.9KB)"; dublin-r1 08:47Z "1302 burst at launch 08:47Z (session 2.9KB — errored very early)".
- Continue landing mid-burst doesn't clear — wait, one more: blender-silhouettes-r2 2026-08-22 16:22Z "1302 burst persisted 16:21Z (second continue needed — first landed mid-burst, account saturated by the 4-round glm fleet)… Doctrine held: no spam, waited, one more continue."
- Post-reset cycling: scale-depth-r1 2026-08-22 20:39Z "1302 burst 20:39Z (post-reset cycling) — one continue cleared" (×3 across 20:38–20:44 right after a 1308 window freed).
- Concurrency attribution via probe: camera-r4/font-r5 2026-08-23 12:22Z "1302 wave x2 (12:20/12:21Z) — both providers probe OK (no wall): CONCURRENCY bursts (3 rounds x lens waves)… waves subside as lens waves complete."
- Depth noted in tokens: camera-r3 10:11Z "1302 re-errored 10:11Z (180k tokens — deep)".

Generalizes: 1302 concentration under a capped primary now has a taxonomy: launch-bursts (harmless, one continue), mid-burst continues (continue once, wait, continue once more — never spam), post-1308-reset cycling (expected, clears), and probe-verified concurrency bursts (no hold, waves subside as lens waves finish). The probe distinguishes burst from wall every time.

### 6. Golden-storm merge waves: planned merge order, settled head, merge-last job (2+, ~20 relay/resolve events)

Sightings:
- Wave posture (7 rows), 2026-08-22 15:01Z: "WAVE POSTURE encoded (Gru ruling 01:5xZ): PANELESS until #76 merge; blocked_by + named release trigger on row; wave order per ruling." — released on cue at the #76 merge 15:01Z, all 7 working by 15:08Z.
- Domino relays: spawn-feel 2026-08-22 23:26Z "CONFLICT RELAYED 23:26Z: base moved (#82+#85 merged) — rebase origin/v2 + force-with-lease; r3 auto-fires on the fresh sha." (same shape for scale-depth, estate, node-clarity, blender-silhouettes, dublin, font ×3, noc-player-toggle).
- Combined-baseline regen discipline: spawn-feel 23:29Z "goldens regenerated on the combined baseline (diff scope = exactly #82's trail rings; spawn-feel content byte-identical pre/post)".
- Settled head + merge-last: font 2026-08-23 06:23Z "MERGE-LAST GO (Gru relay): settled head formed — all 10 wave PRs merged, v2=339e173. Rebase onto settled head + FINAL re-bless (golden storm cause-documented)"; GRU RULING 14:41Z "THIS IS THE LAST MOVE — no more base moves after… Goldens SHOULD hold… re-bless ONLY if a diff proves otherwise (cause-documented)".
- Completion record: font 2026-08-23 15:48Z "THE 2026-08-22/23 v2 DESIGN WAVE IS COMPLETE (#76 pace, …, #87 font LAST)."

Generalizes: a multi-PR wave on a shared golden-bearing base is orchestrable end-to-end: paneless blocked_by holds → release at the trigger merge → per-merge conflict relays (rebase + force-with-lease + re-verify) → rebase-delta Perkins rounds → declared merge order with one MERGE-LAST job that rebases once onto the settled head with a cause-documented final re-bless. Golden re-blesses are only legitimate with a named cause and a diff scope that matches it exactly.

### 7. Sweep-stale + fresh round — never re-target an in-flight round's sha (2+, 6 sightings)

Sightings:
- spawn-feel 2026-08-22 23:29Z: "SWEPT 23:29Z — targeted stale 5404b3d (head moved to 8033ba1 post-rebase); replaced by fresh r3 @8033ba1" (again 23:40Z r3→r4).
- camera-zoom 2026-08-23 08:40Z: "SWEPT 08:40Z — targeted stale 6a7c903 (mid-flight pullback push moved head to bd3b142); fresh r2 @bd3b142".
- dublin-map-spike 2026-08-23 09:11Z: "SWEPT 09:11Z — targeted stale bd394fc (2nd rebase moved head to 6be06dc); fresh r3 @6be06dc".
- font-overhaul 2026-08-23 09:14Z: "SWEPT 09:14Z — targeted stale 0166c3f (3rd rebase moved head to abec50b); fresh r3 @abec50b".

Generalizes: a head move during a round (rebase or fold push) = sweep the stale round + dispatch a FRESH round at the new head (carrying prior findings); a round never "re-targets". Cost is one worktree add; verdicts always land on the true head.

### 8. Moot-on-merge at scale — including merged-on-the-reviewed-head (2+, 5 sightings)

Sightings:
- noc-player-toggle-r3 2026-08-23 14:38Z: "MOOT ON MERGE — PR #91 merged 14:38:06Z while r3 was mid-review on 29addf4 (the merged head); the terminal merge moots the round (08-07 doctrine: no re-dispatch)."
- blender-silhouettes-r3 2026-08-22 19:16Z: "MOOT 19:16Z — PR #79 MERGED while r3 was parked under the HOLD (user merged; safe: stage-1 pipeline PR, zero sprite changes)… r1+r2 verdicts (APPROVED) stand as the review record."
- blender-sculpt-r2 2026-08-23 09:10Z: "MOOT 09:09Z — PR #88 MERGED before the confirmation posted (r1 APPROVED stood)".
- scale-depth 2026-08-22 23:31Z: "PR #83 merged (user merged; r2 confirmation round moot — no dispatch needed…)".
- estate-spawning-r3 2026-08-22 20:32Z: "MOOT 20:3xZ — PR #80 MERGED (0fb1e90) before the fresh-head round dispatched; merge accepted the r1+r2-approved substance".

Generalizes: confirmation/delta rounds around an APPROVED substance are disposable — when the user merges, sweep without re-dispatch and let the prior APPROVED verdicts stand as the record. Note the safe-merge qualifier recorded each time (prior APPROVED exists / merged head == reviewed head / zero substance change).

### 9. Perkins polices prose-vs-code truth: fictitious-claim + stale-PR-body blockers (2+, 4 sightings)

Sightings:
- font-overhaul-r3, 2026-08-23 09:50Z: "B1 FICTITIOUS N11 fold (dead retries field — literal-claims violation; fix: implement budget or delete+retract)… N10 unfixed+aggravated (fabricated doc claim)… 3 not-folded-despite-claim (N9/N10/N15)".
- font-overhaul-r1, 2026-08-23 08:50Z: "B2 WRONG PR BODY (blender-silhouettes content + false 'no goldens touched') — rewrite from commit + captures".
- noc-readability-2-r2, 2026-08-23 18:08Z: "N6' = LIVE PR BODY STALE (r1 text — one gh pr edit)" — and the minion fixed it same-hour: 18:14Z "N6' PR body refreshed via gh pr edit".
- sound-immediacy-r2, 2026-08-22 18:01Z: "W1 PARTIAL (pr_body.md:17 still claims 'ALL FOUR kinds fire' — minion reword)".

Generalizes: review findings now routinely include the PR body and fold-claims as auditable artifacts — a claim in prose that the code doesn't back is a BLOCKER (fictitious fold), and a stale PR body is at least a note. Minions: re-audit your own PR body against the final head before each round; Silas: "claims stand" audits (pattern 3) catch the same class at the merge gate.

### 10. 429-degraded lenses tolerated under a guard — never faked (2+, 3 sightings)

Sightings:
- font-overhaul-r5, 2026-08-23 12:43Z: "6/7 lenses (codebase 429-failed x2, degraded — findings exist so guard passes), 17/17 confirmed 0 discarded".
- sound-immediacy-r1, 2026-08-22 16:51Z: "6/7 lenses (acceptance 429-degraded; spec-AC covered by direct guard verification: all four kinds fire, <=1 frame drain, ci-local 10/10)".
- blender-silhouettes-r2, 2026-08-22 16:46Z: "6/7 lenses (architecture 429-degraded x2, findings present so no degraded-guard trigger)".

Generalizes: a lens that 429s twice degrades the round to 6/7 only if (a) the lens produced findings before dying OR (b) its coverage is re-proven by direct guard verification — the degradation is disclosed in the verdict every time. Three APPROVED/NEEDS-CHANGES verdicts shipped this way; no re-dispatch was needed.

### 11. USER RECALL: a question is not a directive — over-eager dispatch (singleton)

Sightings:
- packet-plumber-v2-flow-focus, 2026-08-23 10:18Z: "RECALLED by user (08-23 11:1xZ, via Gru): was a QUESTION, not a directive — over-eager dispatch. PARKED: design exploration first (problem-solver skill with the user NOW). Row parked (blocked); pane + worktree swept at badge-out."
- Harvest-on-sweep done right, 10:19Z: "Minion's badge-out left useful design groundwork for the problem-solver session: (1) data source exists zero-sim-work… (2) spawn_fx.odin is the token/math canon… (3) extension seams already in place… Field-notes shard written."
- Queue encodes the non-job blocker: `packet-plumber-v2-flow-focus blocked - user-design-exploration(?)`.

Generalizes: dispatch needs a directive check — a user musing/question routed through Gru is intake, not a job. On recall: park the row (blocked with a non-job trigger key), sweep the panes, but harvest and record whatever groundwork the minion already produced so the design session inherits it.

### 12. Perkins pane debris at wave scale: user-flagged 45→3 sweep → sensor shipped same day (2 linked sightings)

Sightings:
- font-overhaul (row carrying the ops note), 2026-08-23 06:26Z: "PANE SWEEP 06:3xZ (user flag): 45->3 pi panes. Closed 42 Perkins leftovers (motion r1-r3, spawn-feel r1-r3, estate r3-moot, blender r1/r3, sound r1 lens/round panes + merged scale-depth minion p2S9) — all rounds had posted verdicts (done/moot/swept); own-pane-id scoping per the 08-17 rule. KEPT: gru p1, silas p1Y6, font-overhaul p2TS (working)."
- silas-round-debris-sensor, 2026-08-23 10:38Z: "PR #14 MERGED 2b744c6 (10:37:16Z) — 7th nefario-watch round-debris sensor LIVE (deploys on next Silas relaunch); detection-only: done-round worktrees/panes + orphan lens panes; validated tsc + harness (baseline 0, planted husk caught)."

Generalizes: a Perkins-heavy wave leaks round/lens panes faster than close-outs sweep them (~42 in 30h); the manual census + own-pane-id scoping rule holds as the fallback, and the fix pattern is: user flags → manual sweep → detection-only sensor job within hours. Detection-only first (no auto-kill) is the sanctioned sensor shape.

### 13. bmad-build skill rendering broken in the PP repo — waiver is the standing path (2+, 4 sightings)

Sightings:
- pace-tuning, 2026-08-21 23:57Z: "skill waived (bmad-build config-token break, Silas ruling 08-21); self-contained briefing; started recon".
- motion-readability, 2026-08-22 15:04Z: "bmad-build render broken in-repo (no render_skill.py) — waived per field-notes; reading view/flow code".
- camera-zoom, 2026-08-23 08:08Z: "bmad-build waived (render script missing per 08-21 ruling)".
- estate-spawning (fixed it transiently), 2026-08-22 15:08Z: "bmad-build rendered (temp disambiguated bmm/gds dup keys, config restored byte-equal); canon read in progress".

Generalizes: the PP repo's bmad-build bootstrap is chronically broken (missing render script / config-token / duplicate skill keys); minions proceed on self-contained briefings per the 08-21 waiver without stalling — but this is recurring tooling debt (4 jobs in the window) that keeps spending briefing text on a workaround; one job proved it fixable in-place (dup keys).

### 14. Pre-authorized mid-round model flips — now incl. round-main SELF-flip and flip-to-the-UP-primary (2+, 4 sightings)

Sightings:
- font-r6, 2026-08-23 14:44Z: "k3 403 cycle cap mid-wave 14:43Z (fickle-k3 — flap after OK probe) — PRE-AUTHORIZED MID-ROUND FLIP executed: /model zai-coding-cn/glm-5.3 + ONE continue… Vision caveat applies for the remainder (mechanical only; k3's native-vision lens work already done)."
- camera-r4, 2026-08-23 12:40Z: "Round turbulence disclosed (glm 1302+1308 mid-wave, lenses re-driven once each). Round main flipped itself k3 mid-wave (pre-authorized envelope)."
- spawn-feel-r4, 2026-08-22 23:52Z: "1308 cap hit 23:51Z… k3 probe OK 23:5xZ — mid-round /model kimi-coding/k3 + ONE continue per the provider-wall doctrine (never continue-spam on 1308; sanctioned flip to the UP reasoning primary)."
- blender-sculpt-r1, 2026-08-23 08:25Z: "k3 403 mid-round (billing cycle cap; review did NOT post — submitted then errored). glm-5.3 probe OK — mid-round /model … + ONE continue… Same round, same sha 0137f92; posts on glm."

Generalizes: the mid-round flip envelope now covers three cases: capped-primary→fallback (k3→glm, with the vision caveat for the remainder), fallback→primary when the primary re-probes UP (glm→k3), and the round main flipping ITSELF inside the pre-authorized envelope — each disclosed in the verdict, each continuing on the same sha with no re-dispatch.

### 15. Orchestrator self-improvement burst: pr_review=0 docs/tooling gate stack (2+, 7 PRs)

Sightings:
- playbook-diet, 2026-08-21 23:28Z: "LAVISH GATE PASSED — user reviewed in-browser ('all good', no changes…)… pr_review=0 verified. pr field SET by minion."
- role-skills, 2026-08-22 00:14Z: "Byte-identical proof: 4 emitted blocks === pre-change runtime values… pr_review=0 (drift+load tests = merge ground truth)"; and 00:29Z "GRU post-#12 direct-push CONFIRMED… Generated-artifact mechanism proven end-to-end on the first real post-merge playbook edit."
- Consolidation-u2, 2026-08-21 19:50Z: "CONFLICT-SENSOR: #8 DIRTY — base moved (origin/main gained bd2e550… user pushed)… Rebase relayed to minion (verify upstream copy wins, keep consolidation edits, re-grep acceptance)" — user direct-pushes to main race in-flight docs PRs; the fold keeps upstream's copy on conflict lines.
- vision-tooling routing, 2026-08-22 00:07Z: "(1) MISSING SYMLINK = real, ONE link — FIXED as direct ops now… (2) stale lmstudio refs… = GRU-OWNED, not a job: 2-line canon touch-up pushed DIRECT after role-skills merges (their worktree owns the playbook until then)."

Generalizes: orchestrator-repo docs/tooling PRs run a distinct gate stack — lavish in-browser review for docs, drift-check + load tests for generated artifacts, pr_review=0 (no Perkins) — and Gru owns a post-merge direct-push window for small canon touch-ups so they don't spawn jobs; worktree ownership of a file (e.g. the playbook) determines who may push what, when.

### 16. Minion self-report compliance is now the norm (2+, 6+ sightings)

Sightings:
- node-clarity 2026-08-22 15:31Z: "pr field SET by minion. Perkins r1 dispatched (glm-5.3)." (same on scale-depth 19:35Z, look-polish 20:09Z, role-skills, night-watchman, vision-tooling).
- font-overhaul 2026-08-23 14:23Z: "Rebase complete 4688d3d (minion self-report, notif shown:true)" (shown:true also 10:36Z, design-audit 05:03Z, camera-zoom 10:29Z).
- motion-readability 2026-08-22 19:25Z: "Minion awaits the fresh Perkins round = approval gate (correctly internalized the corrected doctrine)."
- spawn-feel 2026-08-22 19:54Z: "Aesthetic verdict deferred (vision model rate-limited — noted in PR). pr field SET by minion." — caveat disclosure by the minion itself.

Generalizes: the 08-11/08-18 guard stack (briefing-mandated `ledger pr`, notification shown:true verification, pre-emptive settle notes) has stuck — self-reports in this window arrived complete and Silas' notes read as verification, not gap-filling. Keep the verify step; the failure mode has shifted from missing fields to over-trusting claims (pattern 3).

### 17. OPS GOTCHA: escape = interrupt, ctrl+c = clear-editor — never escape on a WORKING pane (singleton)

Sightings:
- look-polish (Silas self-report), 2026-08-21 19:48Z: "INTERRUPT BLIP (my ops error, recovered): my escape send-key to clear the duplicate relay was pi's app.interrupt (NOT a buffer-clear) → aborted the minion's in-flight turn mid-work (stopReason=aborted…)… LESSON: escape = interrupt, ctrl+c = clear-editor-first — buffer cleanup on a WORKING pane needs ctrl+c, never escape."

Generalizes: buffer hygiene on a working pane is ctrl+c only; escape aborts the turn. Self-recorded with the fix; recovery was clean because both relays had been internalized pre-abort — still, a stray send-keys class worth one standing line.

### 18. TOOLING: `gh pr diff` has a >20k-line API cap — reconstruct via git (singleton)

Sightings:
- pace-tuning-r1, 2026-08-22 01:32Z: "diff reconstructed byte-exact via git (gh pr diff > 20k-line API cap — stats match +39263/-38890)".

Generalizes: giant-diff PRs (golden re-blesses) silently exceed the gh API diff cap; Perkins' fallback is git reconstruction with a stats cross-check — a round can still verify byte-exact on a 40k-line diff.

### 19. _local-refs IP guardrail: user-directed reference drops supersede briefing no-fetch clauses (singleton)

Sightings:
- design-audit, 2026-08-22 00:27Z: "GRU RELAY 01:26Z: MM press-kit refs DROPPED at _local-refs/mm/Mini-Motorways-images/ (9 jpgs, official dinopoloclub press kit, user-directed fetch — README.txt documents source/date). Supersedes the briefing rule-3 no-fetch clause BY USER RULING; guardrail amendment relayed to p2KZ: refs NEVER enter repos (local-only, _local-refs stays untracked)."
- User-side fulfillment recorded earlier on look-polish 2026-08-21 19:48Z: "MM refs drop pending at /Users/moses/code/_local-refs/mm/ — IP guardrail, never committed".

Generalizes: the reference-frame workflow is: user fetches/drops real reference material into untracked `_local-refs/`, the guardrail (never committed, never in repos) is relayed as an explicit amendment with the drop, and a README.txt in the drop documents source+date. Briefing no-fetch clauses yield to user rulings, not to minion initiative.

### 20. Rulings evolve at clarify gates — amend, root-cause, then FINAL with an E2E acceptance addition (2+ sightings)

Sightings:
- noc-overlay D-key saga, 2026-08-22: Q1-Q4 rulings 20:10Z ("Q1 OPTION A (new F-key panel… SHARE helpers via extraction, never fork — N15 anti-pattern)") → RULING AMENDMENT 20:16Z ("'the D never worked' — D NOT sacred… ACCEPTANCE ADDITION: end-to-end proof F-key works in a REAL game run (capture on/off) — a render function never called is not a feature") → KEY RULING FINAL 20:30Z ("D KEY stays as the NOC toggle… F = fallback ONLY if root-cause proves the D binding itself is broken. Final shape: one key (D), one panel (NOC), zero dead code").
- playbook-diet clarify halt, 2026-08-21 20:32Z: user asked in-pane "would this be better as a skill?" → minion recommended keep-as-dispatched → "the clarify-halt question… was implicitly ruled keep-as-dispatched" (lavish Q1 23:28Z).
- Aesthetic picks as gates: font-overhaul 07:18Z "USER PICK: IBM Plex Sans (lavish)"; blender-sculpt 08:06Z "user APPROVED round-2 look"; dublin 08:38Z "lavish gate APPROVED (density 1in6)".

Generalizes: a clarify ruling is the START of the decision, not the end — expect amendment on first contact with evidence (root-cause), and the final ruling often shrinks scope back (F→D) while ADDING an acceptance proof (E2E key-toggle capture). "A render function never called is not a feature" is a quotable acceptance standard for any UI-wiring job.

### 21. Both-providers-down HOLD executed at scale: park with named triggers, defer with target shas, resume on probe (2+, 5 rows)

Sightings:
- PARK ×3, 2026-08-22 18:29Z (identical on blender-silhouettes-r3, motion-r2, estate-r3): "PARKED 18:29Z — HOLD regime (BOTH reasoning providers down: k3 403 billing cap + glm-5.3 1308 5h cap, stated reset 08-23 03:58:50Z — estimate only). RESUME TRIGGER = probe flip (k3 or glm OK) then ONE continue; never v4-pro continue. Panes/worktrees stay."
- DEFER ×2 with targets: scale-depth 19:36Z "Perkins r1 STILL DEFERRED: probe 19:36Z confirms glm 1308 (reset est 03:58Z) + k3 403 — HOLD in force; dispatch r1 @a257ca9 at flip"; spawn-feel 19:57Z same shape "dispatch r1 @1c1d408 at flip".
- Resume executed exactly as written: noc-player-toggle-r1 2026-08-23 12:16Z "RELEASED from HOLD @ k3 probe OK 12:15Z — dispatched @c9a40b6 (head unchanged during hold), kimi-coding/k3, provenance verified (sole modelId k3)".
- 1308-times-lie reconfirmed ×3: font-r5/camera-r4 10:47Z "reset claimed 19:40Z — stated times LIE, probe decides"; spawn-feel-r4 23:52Z "reset est 09:31:51Z — estimate only".

Generalizes: the HOLD playbook is fully mechanical now — park in place (panes/worktrees stay), write RESUME TRIGGER + probe cadence on the row, defer fresh dispatches with the target sha recorded, resume on probe flip only (never stated reset times, never v4-pro), and re-verify head staleness at lift (pattern 3). All 5 rows in this window resumed or were cleanly swept.

## Standing doctrine re-confirmed at volume (no amendment needed)

- **GH-Actions billing block = note-only, no rerun, local tests are ground truth** — ~20 events across every PR in the wave, signature quoted identically each time ("2-3s runs, zero logs, 'log not found'"); minions now pre-classify in their own PR bodies (motion-readability 16:14Z: "NOTE: GH CI runners blocked by ACCOUNT BILLING (runners never started, not a code failure) — local 10-gate suite fully green") — the 08-19 briefing-signature fix worked. UNSTABLE-merge-state gloss added: "PR MERGEABLE (state UNSTABLE = billing-block CI only)" (×4).
- **Sensor-echo dedup** — ~8 echoes answered with same-status notes ("Review-sensor echo… already fully handled… No second relay" 18:09Z; "the alert fired pre-row-creation; row now dedups" 10:59Z).
- **Recovered verdicts (self-close empty-result)** — ×4 (network-pop r1, pace-tuning r1, look-polish r1, estate r1 "recovered via artifacts + PR"); font-r4 verdict "RECOVERED from artifacts".
- **Pre-emptive settle classification** — standard on every completion (~15 settle notes, all "zero new content" classified in advance).
- **Provenance pins on every dispatch** — model + "+ thinking max, provenance verified" on minion dispatches; "sole modelId k3" on reasoning releases; Bob's dream dispatch pinned k3.
- **Vision caveat on non-k3 rounds** — verified present verbatim in briefings (pace-tuning r1 01:11Z "VISION CAVEAT VERIFIED present (x2…)"), honored in verdicts (network-pop "pixel aesthetics deferred per vision caveat"), lifted on k3 return.
- **Fickle-k3 flap class** — ×2 (camera-r4/font-r5 12:20Z "flapped ~5min after OK probe — the 08-19/20 class"; font-r6 14:44Z) — pre-authorized flip executed per briefing both times.

DONE (sheep-ledger, 21 candidates)
