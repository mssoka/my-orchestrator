# sheep-ledger

Material: 132 events in window, 18 distinct jobs (2026-09-02T22:38:03Z → 2026-09-04T23:58Z; excludes dream-2026-09-04's own dispatch events). Dominated by the packet-plumber-3D repo birth + epic belt (11 of 18 jobs incl. 6 Perkins rounds) plus one RT fix lane and one RT small feature.

## Candidates

### 1. The "E1 shape" is now a reusable epic-exit template: Perkins loop → APPROVED → user merges → USER-PLAY GATE (merge ≠ done), gate metric written up-front
- **Evidence**: e1-tiny-planet 04:33:19Z "Perkins loop CLOSED at R2 (APPROVED @ 3a9ef0b). Next: USER MERGES, then A6 USER-PLAY GATE — merge ≠ done. GATE METRIC (up-front): user runs godot --path <repo>… rules on… snap-honors-intent… fun verdict"; e1 09:47:50Z in-review→blocked "row HELD on the A6 USER-PLAY GATE"; e1 10:32:13Z blocked→done "PASSED-WITH-NOTES… done rides the user ruling"; e2-flow-qos 21:29:17Z same shape "row HELD on the A4 USER-PLAY GATE (merge != done, E1 shape)".
- **Why it recurs**: every PP3D epic belt link now ends in a user-play gate; the up-front metric note is what makes the blocked-hold legible to any Silas/Gru session and makes verdict-routing (notes → folded/deferred/new lanes) mechanical. Implies: keep writing the gate metric at loop close, never at gate time.

### 2. Fix-audit loops close in ≤3 rounds; delta-introduced blockers are healthy, carried ones would be pipeline defects
- **Evidence**: e1: r1 CHANGES_REQUESTED (3 blockers: dead separation floor, gesture lifecycle untested, gate roll-up) → r2 APPROVED with "mutation reproduces r1 exactly". e2: r1 (1 blocker, grammar zero coverage) → r2 "r1 B1 VERIFIED FIXED w/ 5 mutation legs" + 2 NEW blockers explicitly tagged "delta-introduced" → r3 APPROVED "every canon surface mutation-proven (grammar 5-leg, nil-crash repro, anti-vacuous gate 3-leg)". e2 14:33:23Z: "NO carried-blocker flag: blocker count 1->2 is delta + a real harness defect catch, loop healthy."
- **Why it recurs**: the bot-skip rule (fix push auto-re-triggers rN+1 with prior_findings) makes each round cheap, so Perkins iterates to approval fast. The delta-vs-carried classification is the health signal — implies it stays in every relay note.

### 3. Mutation-leg proof is the accepted fix standard; suite-growth-with-pins is the fix-audit currency
- **Evidence**: e2-perkins-r3 15:27:52Z "B1 Nil-crash: FIXED mutation-proven (re-typing reproduces the crash AND the EXPECTED_CHECKS gate converts it to 'ran 23, expected 26' -> SUITE FAIL where r2 printed PASS)"; e2-perkins-r2 14:32:54Z "B1 grammar: FIXED, 5 mutation legs RED-then-GREEN, +28 checks all substantive (no padding)"; suite grew 142→170→185 across rounds with "12/12 EXPECTED_CHECKS pins"; art-integration r1 briefing line "tri-cap non-vacuous".
- **Why it recurs**: Perkins independently re-runs mutations (doesn't trust claims), and counts check-substance to catch padding. Implies: fix PRs should ship their own red-then-green evidence and per-file check-count pins.

### 4. Vacuous-gate / phantom-check catches remain the top blocker class in homegrown harnesses
- **Evidence**: e2-perkins-r2 14:32:54Z "B2 run_tests.gd:43-49 harness false-green — 'if result is int' guard useless (aborted coroutines still yield int on 4.7.1), SUITE RESULT: PASS printed over the crashed test = vacuous exit-0 gate over the abort class it was folded to catch"; "3/5 checks PHANTOM (dead null guard beneath)". Fix shape (r3): "completed flag + EXPECTED_CHECKS + final-line guard".
- **Why it recurs**: every new Godot lane hand-rolls a runner and repeats the same false-green shapes. Implies: the EXPECTED_CHECKS/completion-flag triple should be copy-forwarded into the next PP3D epic's harness from day one.

### 5. k3 WEEKLY 7-DAY CAP = new provider incident class; recovery = full sweep + regenerate on glm-5.3 + vision caveat; user ruled the re-check debt absorbable
- **Evidence**: e1-perkins-r2 04:06:30Z "attempt 1 died mid-wave on kimi k3 WEEKLY 7-DAY CAP (403, probe-confirmed DOWN; new incident class - not 1302/1308)… ALL 8 panes swept… FULL wave regeneration on zai-coding-cn/glm-5.3… VISION CAVEAT in force"; attempt-1 artifacts preserved at r2-attempt1-k3-403/. USER RULING e1 09:18:23Z "'we are out of kimi' — NO plan upgrade; k3 stays out until its 7-day window self-resets… NO k3 aesthetic re-check owed for E1 — the A6 USER-PLAY GATE IS the look verdict for slice 1; later visual lanes route KYLE (glm-5.3-flash)".
- **Why it recurs**: weekly cap is calendar-bound, not load-bound — mid-flight rounds will keep hitting it until it resets. Implies: mid-work k3 death on the weekly cap = the 403 sweep+regenerate doctrine (like quota-403), and the user-play gate can absorb owed aesthetic re-checks by ruling.

### 6. Probe false-reads persist (chatty-OK strict-matcher false-DOWN); dispatch proceeds on reply-content evidence
- **Evidence**: e2-perkins-r1 12:08:54Z "bin/quota-probe returned DOWN x3 on chatty replies ('OK — I'm ready to help...') = the strict ^OK$ matcher false-DOWN class (08-20/08-27) — provider functionally UP (instant coherent replies, no error codes), dispatch proceeded on re-probe evidence"; r2 pre-add 13:42:29Z "glm-5.3 UP (chatty-OK probe reads expected — read reply content, not the matcher verdict)"; art-r1 "glm-5.3 probed strict-OK".
- **Why it recurs**: bin/quota-probe's ^OK$ matcher still not hardened. Implies: a probe-DOWN verdict on a coherent non-empty reply is a re-probe-first trigger (already doctrine for gates); a sensor/tooling fix to the matcher remains owed.

### 7. Connection-class main deaths ≈1×/round on long waves: ONE continue, wave resumes from durable artifacts — never re-dispatch
- **Evidence**: rt-643-perkins-r1 00:56:36Z "main died 4x errored turns (connection class) before any lens JSON landed (diff.patch + prompts staged); ONE continue revived it (verified working) - the wave restarts from the saved canonical diff"; (same-shape prior: pp-funfix-118-124-perkins-r1 01:05:25Z "6th today", pre-window).
- **Why it recurs**: flash-tier long-context lens waves die at a steady rate. Implies: budget it, classify by transcript before spending continues, durable diff.patch/lens JSONs are the salvage substrate.

### 8. 1302 bursts mid-wave: single-continue + in-wave lens retry (burst ≠ wall)
- **Evidence**: e2-perkins-r3 15:27:52Z "Survived a 1302 burst mid-wave via single-continue recovery"; art-integration-r1 23:33:05Z "7/7 completed (security lens delivered on its in-wave retry after the 1302 burst emptied gen-1)"; rt-643-r1 "edge re-dispatched once after 1302 burst + dead generation"; e2-r1 "arch retried both waves: 429 / hung probe".
- **Why it recurs**: bursts are episodic under load; the probe distinguishes burst from wall. Implies: retry the individual lens on a fresh pane; a lens pane "done" with zero JSON = regenerate that lens only (wave-state ground truth = JSONs on disk).

### 9. Sensor stale-echo taxonomy grew a loop-terminal flavor: approval kills the loop, no rN+1 is owed
- **Evidence**: 4+ in window, all answered note-only: e1 03:41:22Z + e2 13:44:03Z ("tick raced the rN pre-add — ALREADY dispatched, single row verified"); e2 15:32:53Z "sensor 'dispatch r4 on e224804' echo = STALE — r3 reviewed EXACTLY sha=e224804… loop-until-APPROVED is TERMINAL on approval, no r4 exists or is owed"; e1-r2 04:07:57Z "'pane gone' alert… = SWEEP ECHO — p70 was the attempt-1 main I closed myself".
- **Why it recurs**: sensors re-fire on ticks racing pre-adds, sweeps, and loop closure. Implies: pre-add rows with full-sha notes remain the dedup; new rule-worth noting: an APPROVED verdict terminates review-arming on that sha permanently.

### 10. Lavish gate IS the review for creative/design lanes (pr_review=0)
- **Evidence**: asset-scout 11:52:30Z "lavish pick session WAS the review (2 user rounds steered junction + link language); no Perkins per pr_review=0"; 10:48:30Z "lavish contact-sheet live (33 candidates…) — HALT until user picks"; 11:22:39Z "SPEC LOCKED via lavish gate… Verdicts verified in ~/.lavish-axi/state.json"; gdd-v1 "2 lavish rounds pre-PR"; gdd-amend-levels 21:50:57Z "lavish review gate opened at .lavish/gdd-amend-levels.html".
- **Why it recurs**: pick/design decisions need user taste in-browser, not lens verdicts. Implies: creative lanes dispatch with pr_review=0 + a lavish halt gate; verdicts durable via state.json.

### 11. Amend-and-relay stays the only mid-flight correction path — including gate moves
- **Evidence**: asset-scout 10:35:35Z Gru amendment "DROP the wifi-router direction ENTIRELY" + 10:35:54Z Silas detail amendment, 19s apart, minion kept working (no re-dispatch); e2 22:38:54Z "GATE AMENDMENT (user ruling via Gru): E2 play gate DEFERRED — the user will play LEVEL 1 (post-pivot ARPANET) instead of the raw E2 sandbox… NO re-dispatch, no rework: the row just waits".
- **Why it recurs**: user reversals land mid-flight constantly; relays + row-notes are cheaper than kills. New facet: gates themselves are amendable (trigger moves to a later artifact) because the metric is up-front — deferral is free.

### 12. FYI post-merge verdict → named fix-PR lane; row holds open on a dependency; Perkins-skip on instruction-executing fix PRs is a documented judgment call
- **Evidence**: rt-agents-prod-scale-to-zero 11:59:15Z "PR #176 MERGED (user click 11:52Z, pre-verdict). Perkins r1 FYI verdict CHANGES_REQUESTED post-merge: B1 REAL + LIVE — test_concurrency.py pins min_instances==1, unit suite RED on develop… Fix relayed to the open minion… Row HOLDS OPEN until the fix PR lands — the promote path depends on it"; 12:04:32Z "No Perkins round on #178: test-only change executing Perkins' own fix instruction, suite-verified (documented judgment call)".
- **Why it recurs**: pre-verdict merges keep happening (user peeks); findings stay real and live on the base. Implies: FYI verdicts need a fix lane + a dependency hold; the Perkins-skip rationale must be written down when used (watch for scope creep of that exemption).

### 13. Held-round pre-create on unstable targets with named release triggers — executing cleanly
- **Evidence**: e1-perkins-r1 01:44:43Z "HELD - review target UNSTABLE (e1 minion mid internal self-review…). RELEASE TRIGGER: minion settles… AND head stable ~10min -> re-resolve FRESH sha" → released 02:33:04Z "fresh sha=9fad932 HEAD of PR #2 verified".
- **Why it recurs**: minions self-review-swarm before settling; dispatching at a moving head wastes a worktree. Implies: hold + fresh-sha-at-release remains standard.

### 14. Close-out capture is fully standardized: verdict-as-note with lens/confirmed/rejected counts + fetched review URL + sweep inventory
- **Evidence**: every round in window (rt-643-r1, rt-zero-r1, e1-r1/r2, e2-r1/r2/r3, art-r1) carries a done→done close-out note: e.g. art-r1 23:33:05Z "7/7 completed…, 23/24 confirmed (1 rejected), 0 blockers, 10 warnings… Review: …pullrequestreview-5118650123. Sweeping (wt + pAR; lens panes self-closed)". Lens panes now ROUTINELY self-close; sweeps list shrank to main pane + worktree.
- **Why it recurs**: self-close eats verdict detail (known); the pre-emptive note is the record. Implies: keep capturing at close-out; note the improvement — lens-pane leakage, the 08-29 leak class, did not recur in this window.

### 15. pr-field verify-and-set still needed — crews mostly self-set, one NULL slipped through
- **Evidence**: art-integration 23:09:39Z "pr field was NULL on self-report (verify-and-set executed)". All other in-review transitions in window (gdd-v1, e1, e2, asset-scout, rt-643, rt-zero) carried a same-minute `pr:` event.
- **Why it recurs**: the briefing line mostly works but not universally. Implies: verify-and-set on every in-review transition stays mandatory (7/8 self-set this window; 1 gap caught).

## Watch items

- **Blind-lens false-positive trio on a small view diff**: rt-643-r1 "3 blind false-positives rejected (helpers exist, imports pre-exist)" — blind over-flags on 396L view diffs; the verification pass is the guard. Watch the FP rate if blind keeps degrading/truncating.
- **Godot fresh-clone class-cache**: e2-r1 "fresh-clone needs --import first" — headless suite in a fresh worktree must run `godot --headless --import` before tests or classes are missing. Copy-forward into PP3D harness docs.
- **Authoring scales lie**: asset-scout "authoring scales lied 0.08x-25x" — every external asset needs world-bbox measurement + rescale; CC0/CC-BY filter + ATTRIBUTION.md + shared-Blender zero-saves ritual worked clean.
- **KYLE screening drove a spec deviation needing user ratification**: art-integration "frozen spec said dithered-alpha glass; KYLE proved dither=TV-static at tube pixel sizes -> fresnel alpha-blend shipped instead (disclosed + test-pinned) — ratify or reverse at merge". Vision screening as spec-amendment driver; ratification item parked on the merge. Also "KYLE rounds = screening not evidence" now standard briefing language.
- **rt-zero CI blind spot**: "pr-checks paths exclude deployment/**" — terraform/deployment paths have zero CI; found only by a Perkins round. Candidate for a paths fix.
- **Regex false-pass hazard**: rt-zero W2 "comment matched before assignment, flip-back would falsely pass, mechanically verified" — test regexes must be line-anchored (fix: line-anchored helpers).
- **Mid-session model flip provenance**: gdd-v1 "session jsonl records a mid-session flip to kimi-coding/k3… row model column left as-dispatched, flip noted; benign" — flips now happen for doc-authoring upgrades; row-vs-jsonl divergence noted but not reconciled.
- **h3 lane parked on a decision**: 09-03 23:54:39Z "pane idle = the DOCUMENTED hold… pending the Metal-native pivot decision; resume trigger = Gru's pivot ruling" — a lane sitting idle awaiting a Gru ruling; don't let it sit past the next pivot conversation.
- **e1 gate verdict routing**: PASSED-WITH-NOTES routed scope cleanly (editor-preview → E2, world-scale → E3, art → asset-scout lane) — the "notes" half of a gate verdict is a dispatch queue; confirm each landed (all three did this window).
- **rt-643 mandate-verification style**: verdict listed mandate legs individually ("11/11 guide routes carry shared CTA… copy byte-exact, client untouched (+243/−0, no client/ paths)") — per-mandate PASS lines make small-feature reviews auditable; good shape to keep.
