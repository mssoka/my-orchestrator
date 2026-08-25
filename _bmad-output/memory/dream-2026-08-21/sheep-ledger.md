# sheep-ledger shard — dream-2026-08-21

Window: 2026-08-19T18:27:41Z (prior dream close) → 2026-08-21T18:31Z (this dream's dispatch, read live).
294+ events at first read (more landed mid-read — ledger is live; folded in). 44 distinct job rows read via `ledger show`.
Context note: dream-2026-08-19's U2 consolidation scope already names the model-policy chain (v4-pro ban, 402, probe hardening, 1302, valve) — L2/L3 below overlap it; kept with the NEW mechanics on top.

## Candidate patterns

**L1 — Perkins round mains fail the badge-out step reliably: self-close eats the verdict / main "hangs post-post" — recovered-at-close-out is now the NORM, not the exception.**
Evidence: `packet-plumber-ue-bootstrap-perkins-r2` 08-20 "VERDICT (recovered at close-out — self-close left result empty)"; `packet-plumber-ue-slice-1-perkins-r1/r2/r3` 08-21 all "verdict recovered (self-close...)"; `righttenantry-demo-polish-2-perkins-r1` "(Round main hung post-post; close-out by Silas.)"; `-r2` "(Main badging hung; close-out by Silas.)". ~8 sightings in 48h, ~2/3 of all rounds. Silas's pre-emptive verdict-note doctrine saves the data every time, but the round main itself never lands `result`. Matters: the Perkins tooling's badge-out step is systematically broken (token-mint/badging path) — a fix task candidate, not just tolerance; expect to reconstruct verdicts from review artifacts at every close-out until fixed.

**L2 — k3 fickle cap defeats probe-at-dispatch: 403 re-hits ~5 min after an OK probe; the durable recovery is mid-round `/model glm-5.3` + one continue — proven ≥5× this window.**
Evidence: `packet-plumber-v2-6.2-advance-trigger-perkins-r2` 08-20 07:43 "k3 403 re-hit (cycle cap flapped ~5 min after an OK probe) -> /model zai-coding-cn/glm-5.3 + continue (recovered, working)"; same phrasing on `righttenantry-demo-polish-2-perkins-r1` ("the fickle-k3 class"), `7.3-r2` 08-19 19:16, `demo-polish-2-perkins-r2` ("k3 403 mid-round -> lenses re-dispatched on glm"). Lesson: the probe is a dispatch-time gate, NOT a round-long guarantee — briefings for rounds on k3 should pre-authorize the mid-round flip (model + one continue, no re-dispatch) so no recovery time is lost when it flaps.

**L3 — Park/resume regime matured and is 3/3 reliable: rows carry a named RESUME TRIGGER; glm's cap-message reset time LIES (window freed ~11h EARLY) — only the probe decides.**
Evidence: `7.3-perkins-r5` 08-19 21:44 "PARKED (reasoning HOLD): glm 1308 5-hour cap hit 21:43Z (reset 08-20 07:07:22Z); k3 also cycle-capped; v4-pro BANNED... Row stays working"; 21:53 "USER INTEL... RESUME TRIGGER = k3 probe-flip at/after 00:00Z OR glm 1308 reset 07:07Z, whichever first"; `demo-polish-2-perkins-r3` 08-20 14:07 "HOLD LIFTED (user: glm back; probe OK ~09:50Z — the rolling window freed EARLY vs the 20:43Z estimate)". Both parked r3 rounds + the parked r1s resumed clean on the trigger. Confirms + extends the 08-19 "reset-time lies" hardening: park rows MUST carry the trigger + probe cadence; never schedule a resume off the provider's stated time.

**L4 — The vacuous-pin genus is the #1 blocker source across ALL repos: "fix without a biting regression pin" — helper-pins that don't prove wiring, collects that never assert, zero-pin fixes. Perkins's revert-style check catches it round after round.**
Evidence: `7.3-perkins-r4` 08-19 "pause-on-open UNPINNED (deleting the Run->Paused flip in effect_settings ships CI-green; parity asserts the hook FIRES, never that the run PAUSES)"; `7.3-perkins-r5` "pause pin guards the helper, NOT effect_settings wiring (deleting the flip still passes 16/16)"; `6.2-perkins-r2` 08-20 "test... VACUOUS (collects the Era_Advanced tick but never asserts... the same vacuity genus as r1 B2)"; `demo-polish-2-perkins-r2` "the r1 fix shipped with ZERO regression pins (re-dropping the statements fails no test)"; `7.3-perkins-r6` "effect_settings_adjust ZERO exec coverage (the r5 trap's ADJUST twin)". ≥7 sightings, several carried ACROSS rounds (r4→r5→r6 same hole). Durable lesson for every fix briefing: each fix ships a pin that FAILS when the fix is reverted ("BITES"), at the WIRING level (exec/effect site), not the helper level — and Perkins should keep asking for the revert-control proof.

**L5 — Lens fleets launched on the WRONG MODEL (bare-pi default = k3) while the round main rode glm — user-spotted ×2 in one hour; root cause fixed in the code-review skill (model pin now mandatory).**
Evidence: `packet-plumber-v2-6.2-advance-trigger-perkins-r3` 08-20 14:24 "the tHM lens fleet launched on k3 (bare-pi default) while the main rode glm — k3 cycle-capped. Lens shells dead (their pis 403'd pre-park...) ROOT CAUSE fixed: code-review skill MODEL PIN made mandatory"; `demo-polish-2-perkins-r3` same ts "the tHP lens fleet (7 panes...) launched on k3 (bare-pi default)... ALL 7 switched to glm-5.3 + continue (modelId verified)". Extends the 08-19 PROVENANCE RULING (pin round-MAIN) to LENS launches — the skill fix landed, so verify it holds at the next wave. Note the dead-k3-lens-shells disposition: debris the main sweeps, NOT a re-dispatch (JSONs already durable).

**L6 — NEW incident class: whole-MACHINE REBOOT mid-flight (08-20 17:59Z) — per-class triage worked; durable lens JSONs salvaged the in-flight round.**
Evidence: `packet-plumber-ue-bootstrap-perkins-r1` 08-20 18:09 "REBOOT RECOVERY 17:59Z (machine reboot killed main + 2 lenses mid-round...). 5/7 lens JSONs durable in _bmad-output/perkins/.../r1/ + diff.patch + pr.json; tests+security regenerating. Round RELAUNCHED same row same sha 836f44e"; `righttenantry-demo-dev-verify` "pi DEAD post-reboot... user-interactive/parked — no auto-relaunch"; `6.2` 06:18 wedged-pi kill ("hung turn frozen ~13.4h silent; orphan core.bin spinning 99.9% CPU killed; continue/send-keys inert"). Reboot triage recipe: (a) Perkins round → relaunch same row same sha, regenerate only missing lenses; (b) interactive/parked minion → wait for user; (c) wedged pi + orphan process → kill pid, fresh relaunch + full handover. The incremental-write of lens artifacts to _bmad-output is what made (a) cheap — worth stating as the reason the pattern exists.

**L7 — The night-watchman false-death cascade (08-21): an out-of-pi liveness watchdog is itself an incident source — boot-race false deaths + wrong-tier relaunch + identity-tab split; hardened same-day.**
Evidence: `orchestrator-night-watchman-hardening` row note: "09:16Z FALSE silas death — pane p1Y6 mid-boot, session file not yet visible; watchman typed its relaunch command into the LIVE booting pane (queued in buffer, delivered as stray user msg 90 min later). (2) 09:52Z REAL gru death... relaunched a fresh Gru-class pi on FLASH (defaultProvider, wrong tier; k3 needed) and SPLIT the gru tab"; PR #7 merged 11:01Z with "boot-race grace + BOOTING liveness; identity-tab single-pane guard; live-agent no-op; k3→glm-5.3 model pin w/ probe; cross-tick verify". Durable: any automated relauncher must inherit ALL manual-dispatch rules (model pin, never split identity tabs, verify loop) — and session-file liveness has a boot RACE (absent file ≠ dead on a fresh pane). This bit the watchdog within 19h of it going live.

**L8 — Billing-block 'log not found' CI echoes are the highest-volume noise class: ~15 note-only events in 48h across every in-review PR — the ruling holds, but the sensor re-fires on every push.**
Evidence: `righttenantry-mobile-layout-1` 08-19 23:56 "CI alert... 'log not found' — billing-block recurrence, note-only; local suite = ground truth" (identical on demo-mode, 7.3, polish-1/2, 6.2, 6.3, form-hunt, PP-UE #1). Plus minion-side misclassification: `demo-polish-1` 21:43 "GitHub Actions runner infra outage... Re-run when runners recover" — the minion recommended a rerun the standing ruling calls useless. Candidate fix: teach the sensor the signature (5s run / zero logs / 'payments failed') to auto-note or mute, and carry the signature in minion briefings so they stop proposing reruns.

**L9 — Wrong-environment parity verdicts: "real-app twin" comparisons must name WHICH surface — production was 36 commits behind and made two successive minions report wrong verdicts.**
Evidence: `righttenantry-demo-polish-2` 08-20 06:51 "production bundle = pre-#615...; production is 36 commits behind (main Aug-10)" (demo matched current code; prod was stale — polish-1's "verified-parity" was right against staging, wrong against the user's actual experience); `06:57` "polish-1's real-twin verdict wrong again — the toast pattern". Sibling: `packet-plumber-ue-slice-1-perkins-r1` 08-21 B2 "FABRICATED evidence — slice1-3-packet-mid-traversal.png has zero #3E7CB1 pixels, vision-read 'NO dots'" → minion 11:46 "the r1 frame was a vision hallucination I failed to pixel-check — owned" → fix added `verify-capture-geometry.py` with a 37px negative control ("the OLD frame fails it"). Two lessons: (a) parity briefings pin the exact compared surface (prod vs staging vs branch head + its sha); (b) vision-derived evidence requires a committed mechanical gate with a negative control, never vision alone.

**L10 — Trigger-graph release discipline is proven at scale: 4/4 held rows released exactly at merge close-outs with fresh heads resolved — the whole PP v2 belt completed through it.**
Evidence: `packet-plumber-v2-6.3-upgrade-lifecycle` 08-20 15:13 "RELEASED at #71's merge close-out (trigger-graph; blocked_by 6.2 done): worktree from origin/v2 @95a62ad post-merge"; `packet-plumber-ue-architecture-slice-map` 22:47 "TRIGGER-GRAPH RELEASE @ #1's merge close-out: fresh main head @07aec12"; 6.2 released at #69's close-out 08-19. Chain 6.1→6.2→6.3→merge→"THE BELT IS COMPLETE — the FUN-TEST GATE is now LIVE (user decision)". Positive confirmation worth recording: the P2 upgrade is now the default belt mechanism, zero misfires this window; the fun-test gate itself is a NEW user-held milestone type (merge ≠ done; the gate is the user's play session).

**L11 — Row-hygiene gaps persist + a NEW wrong-ROW flavor: rounds writing events onto the PREVIOUS round's row (not just self-created wrong-id rows).**
Evidence: `packet-plumber-v2-7.3-accessibility-core-perkins-r4` 23:12:02Z shows "done -> working r5 fix-audit of 12166ea" — the r5 round's self-report landed on the r4 ROW (the canonical r5 row has its own events), and earlier "(Row was accidentally flipped working by the r5 round's self-report at 21:39:32Z — restored to done.)". Self-created-with-empty-fields also steady: `righttenantry-mobile-form-hunt` "Row self-created by the minion (P12) — fields filled by Silas"; `orchestrator-night-watchman` "Phantom row night-watchman (self-created wrong id) deleted". Also: `model` column empty on several round rows (`form-hunt-perkins-r1`, `bootstrap-perkins-r2`, `slice-1-perkins-r2/r3`) even while the note says "provenance verified (modelId=glm-5.3)" — provenance is being verified but not WRITTEN to the column. Guard remains verify-and-fill; add "write the model to the row" to it.

**L12 — The W3 spawn-turn stall is now named and scripted: round main's spawn-turn ends mid-lens-wave leaving it at prompt; one continue-nudge after the wave collects+posts. 3 clean sightings.**
Evidence: `righttenantry-demo-mode-perkins-r5` 08-19 19:48 "round main (p2AX) spawn-turn ended mid-lens-wave (6 lenses working, W3-flavored pattern) — main at prompt; will continue-nudge once the lenses finish"; `7.3-perkins-r3` 19:59 "W3-style: main spawn-turn ended, 7 lenses done/idle, no review -> continue-nudge -> main WORKING (collect/consolidate/post)"; `bootstrap-perkins-r1` 08-20 17:24 "17:23Z W3 pattern... Continue-nudge when the wave finishes." No error involved (toolUse stops only) — classify by "main idle + lenses working" and nudge once; don't wait for an alert to force it.

## Census — distinct jobs read (44)

| job id | what happened |
|---|---|
| dream-2026-08-19 | prior dream; close = the marker; user-ack U1–U3 executed 18:32Z (tooling fixes committed) |
| righttenantry-demo-mode | demo landing PR #629; 5-round gauntlet (r1 8B→r5 0B); merged 08-19 20:43Z |
| -demo-mode-perkins-r4 | CR 2B (vacuous lint skip + unpinned entry); 21/21 lenses through k3-cap + glm-429 waves |
| -demo-mode-perkins-r5 | APPROVED on glm (2 429 recoveries); W3 stall handled; loop closed |
| packet-plumber-v2-7.3-accessibility-core | a11y floor PR #72; 7-round loop (r1 6B→r7 0B); merged 08-20 06:19Z |
| -7.3-perkins-r2 | CR 4B (delta-0 no-op, linear_to_srgb wrong in BOTH twins, test gate ~78% fail) |
| -7.3-perkins-r3 | CR 4B (ci-local RED at sha — shared temp-path race; PR claim false) |
| -7.3-perkins-r4 | CR 1B (pause unpinned); row self-created (P12); later contaminated by r5's writes |
| -7.3-perkins-r5 | DEGRADED 4/7 lenses (glm 1308 mid-wave); CR 1B helper-pin-not-wiring; parked/resumed |
| -7.3-perkins-r6 | CR 2B (race persists — macOS identical-nanoseconds; adjust zero exec coverage) |
| -7.3-perkins-r7 | APPROVED; race closed ns+crypto-random, 10 pristine runs |
| righttenantry-mobile-layout-1 | 5 mobile fixes PR #631; 4-round loop (r1 2B→r4 0B); merged 08-20 06:19Z |
| -mobile-layout-1-perkins-r1 | CR 2B (fabricated vacancy id; unpinned vacancy nav); parked→k3-flip |
| -mobile-layout-1-perkins-r2 | CR 2B (demo arm bypass; late-response re-fabrication) |
| -mobile-layout-1-perkins-r3 | CR 1B (cold-boot deep-link drops leaderboard — LIVE-PRODUCT regression from r2 fix) |
| -mobile-layout-1-perkins-r4 | APPROVED 9/9; loop closed |
| righttenantry-demo-polish-1 | 6-fix parity polish PR #630; r1 APPROVED 0B; merged 08-19 23:30Z |
| -demo-polish-1-perkins-r1 | parked round; k3 flip post-midnight; APPROVED |
| righttenantry-demo-dev-verify | interactive verify minion; checklist green; pi dead post-reboot; done 08-21 09:19Z |
| righttenantry-demo-polish-2 | 3-fix follow-up PR #632; 3-round loop; merged 08-20 16:37Z; prod-stale root cause |
| -demo-polish-2-perkins-r1 | CR 1B (5/8 PDFs missing statements); main hung post-post |
| -demo-polish-2-perkins-r2 | CR 1B (zero regression pins); main badging hung |
| -demo-polish-2-perkins-r3 | parked/resumed; lens fleet wrong-model (user-spotted); APPROVED |
| righttenantry-mobile-form-hunt | self-created row; report-only hunt → user-approved fixes PR #633; merged 08-20 22:46Z |
| -mobile-form-hunt-perkins-r1 | APPROVED (2×429 retries; 1527 suite independently reproduced) |
| packet-plumber-v2-6.2-advance-trigger | era advance gate PR #71; 3-round loop; merged 08-20 15:12Z; wedged-pi kill mid-loop |
| -6.2-perkins-r2 | CR 1B (vacuous test); k3 flap→glm mid-round |
| -6.2-perkins-r3 | parked/resumed; lens fleet wrong-model; APPROVED |
| packet-plumber-v2-6.3-upgrade-lifecycle | released at #71 close-out; PR #74 r1 APPROVED; merged 08-20 17:42Z — BELT COMPLETE, fun-test gate live |
| -6.3-perkins-r1 | APPROVED round 1 (decay contract verified; false-DOWN probe corrected by re-probe) |
| packet-plumber-ue-bootstrap | NEW repo; UE 5.8 scaffold PR #1; spine contract user-approved; r1 6B→r2 APPROVED; merged 08-20 22:46Z |
| -bootstrap-perkins-r1 | reboot recovery mid-round (5/7 lens JSONs durable); CR 6B; verdict recovered |
| -bootstrap-perkins-r2 | APPROVED (engine found installed → real gates ran; first engine-golden 3-way) |
| packet-plumber-ue-architecture-slice-map | held row released at #1 merge; lavish-gated; 3 post-done user-ruling folds (LOOKS primary); merged #2 |
| orchestrator-night-watchman | bmad-build render failure → skill waived by Silas ruling; PR #6 merged 08-21 08:22Z |
| orchestrator-night-watchman-hardening | incident-followup for the watchman cascade; PR #7 6/6 fixes merged 11:01Z |
| packet-plumber-ue-slice-1 | MM-look vertical slice PR #3; r1 CR 2B (incl. fabricated evidence) → r2 CR 1B (road anchor) → r3 APPROVED |
| -slice-1-perkins-r1 | CR 2B (dead PIE input; fabricated screenshot); verdict recovered |
| -slice-1-perkins-r2 | CR 1B (road ribbon Width/2 vs Length/2); verdict recovered |
| -slice-1-perkins-r3 | APPROVED 21/21 lenses; glm 1302 burst mid-review survived (one continue); verdict recovered |
| packet-plumber-v2-look-polish | ODIN-focus look polish dispatched 08-21 18:28Z (in flight at read; UE slice-2 PARKED per user) |
| righttenantry-dublin-rents-q2-2026 | long-hold external gate (Daft.ie Q2 report); periodic re-check, next ~08-25 |
| dream-2026-08-21 | this dream (parent Bob) |

## No-pattern observations (one-offs worth a watch item)

- **Re-litigating-user-design triage** works: `mobile-layout-1-perkins-r1` "8/12 verified — 2 re-litigating-user-design rejected, 2 dup-merged" — reviewers proposing changes to user-approved design get rejected at consolidation, not relayed.
- **Sibling port clobber**: `righttenantry-mobile-form-hunt` 07:34 "this job's make run server REPLACED the demo-dev-verify server on :4000 (same env, newer code)" — two minions sharing one repo checkout env can silently swap each other's live server. Watch for repeat before canonizing.
- **Engine-gate honesty paid off**: bootstrap r1 documented "engine-gated gates not-yet-runnable = documented, not a defect" → rework found UE 5.8.1 INSTALLED and ran them for real (7/7, first engine-golden 3-way). Document-don't-fake, then verify for real when possible.
- **bmad-build skill render failure on the 08-20 upstream update** (6.11.0): ambiguous config token `implementation_artifacts` (bmm + gds both define it) → CLARIFY HALT → Silas waived the skill, briefing self-contained; PR body carries it as a canon note. First sighting; if the next bmad-build job hits it too, it's a standing upstream bug to route around.
- **Lens waves are growing**: slice-1 r3 ran 21/21 lenses with a 14-pane wave — the 1302-burst exposure per round grows with lens count; the one-continue recovery held, but wave size is a new variable in the concentration doctrine.
- **Grace-Kelly style fix-chains** (rename lands in one artifact, survives in another for 2 more rounds: PDF→client fixture→demo UI) — the "fix the SPEC not one instance" lesson; arguably part of L4 but shows fix-audits must grep ALL surfaces, not the reported one.
- **launchd agent bootstrapped pre-merge** (night-watchman): pre-merge ticks exit-78 (self-heal) + ONE launchctl kickstart needed post-merge — deploy-order detail for launchd-backed deliverables.
