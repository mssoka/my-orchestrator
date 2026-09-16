# Dream report — 2026-09-11

Material: **1 shard file (3 meta-entries) + 6 journal files (gru 09-09/10/11, silas 09-09/10/11; ~310KB) + 572 ledger events / 41 jobs** since **2026-09-09T01:21:29Z**, through the pass cutoff 2026-09-11T02:33Z. Plus 10 shard backfill tails (zero post-marker material) and 09-08 journal tails (pre-marker, nothing undreamed).

| 🧠 Result | Count / disposition |
|---|---|
| Source readers | 3 sheep (shards / journals / ledger); all shards delivered; all 3 panes closed |
| Candidate patterns | 26 raw → 12 distinct survivors |
| Accepted proposals | **13: 12 auto + 1 user-ack** applied to `store/` (+3 template/ops user-acks, NOT store) |
| Watch items | **17**, not promoted |
| Verification pass | adversarial lens (bmad-review successor, rubric-only — legacy alias dangling, see U2); every cited quote grepped verbatim in source; patches reproduction-tested on scratch baselines (byte-identical) |
| Live state | Live `AGENTS.md` + `docs/minion-field-notes.md` + `last-dream` untouched by Bob |

## Patches (apply order)

- `auto.patch` (12 edits: P1–P10 AGENTS.md, P11–P12 minion-field-notes) — Silas applies directly at close-out.
- `user-ack-AGENTS.patch` (1 edit: the Cadence paragraph) — hold for user ack.
- `all-proposals.patch` = both, for reference. `auto.patch` + `user-ack.patch` applied in order to `baseline/` reproduce `store/` byte-for-byte (verified).

---

## Proposals — AUTO (applied to store copies)

### P1 — HOLD INTERLUDE: OpenAI plan-cap = 5th cap flavor; GLM interim chain; identity pins invalid
- **Target:** `AGENTS.md` CURRENT MODEL POLICY banner · **Class: auto** (status sync of a user-ruled, duration-limited regime; precedent: prior cap flavors added as auto)
- **Change:** appended a dated HOLD INTERLUDE block after the GPT-chain banner: windowed plan cap (~09-15), glm-5.3 @ max interim (flash @ high for Silas), image-gen exempt, Astra reserved; in-place identity revives; watchman/relaunch pins INVALID until lift; ~3 concurrent glm round mains = launch-burst tax; policy-file pointer (`memory/openai-quota-hold-glm-interim-2026-09-10.md`); GPT base resumes at lift.
- **Evidence:** gru-09-10:203 "User ruling: OpenAI limit hit — finish Perkins on glm-5.3…"; :204 "Silas died on the cap mid-turn… revived him IN-PLACE"; :198 "watchman pins invalid until lift"; ledger (storyboard 11:05) "window ~2026-09-15… continue = waste, parked"; main-suite-r2 1302 bursts 23:25-23:38Z.
- **Reasoning:** the cap taxonomy is the store's most-consulted table; the 5th flavor rode the PRIMARY chain for the first time and invalidated every identity pin — future sessions reading the 09-07 banner cold would dispatch GPT models into a dead account.

### P2 — Stale "Luna @ max" lines → xhigh (user ruling 09-09, PR24 merged)
- **Target:** `AGENTS.md` banner + Vision section + 09-09 thinking addendum · **Class: auto** (stale fix)
- **Change:** all three "Luna max" mentions corrected to xhigh with the ruling + PR24 provenance noted.
- **Evidence:** gru-09-09:188 user verbatim "let's make silas model luna be on xhigh as well. rather than on max."; :438 PR24 merged (close-out receipt); :208 vision-read SKILL line folded as 6e647a8.
- **Reasoning:** canon moved (PR24) while the memory store didn't; a future relaunch would boot Silas on max against merged canon.

### P3 — PP3D bounded-run grants & the execution-RED catch net (NEW gotcha)
- **Target:** `AGENTS.md` Perkins section tail · **Class: auto** (gotcha append; the regime is already user-ruled — this records it)
- **Change:** new bullet: run-word grants (entry budgets, headless-only, ≤300s/entry — captures need ~900s, receipts, quiescence, named stop conditions; stop-on-surprise > checklist; extensions = new disclosed grants; exhaustion = stop-and-report) + the catch-net evidence: static-only review ships execution-RED (PR22 4-round APPROVED → red; #27 merged-unverified → green-confirm caught it; #31 deadlock found only by execution); merged-unverified debt owes a green-confirm; execution-found fixes on an APPROVED head = legitimate new delta (r5-after-skip-row).
- **Evidence:** gru-09-10:38 "second proof that static-only review ships red — the user's 'run' call vindicated"; grant doc ledger events 18:33:05Z (SHA 8cd9577b); ledger 23:44:02Z green-confirm FAIL; 01:18:50Z "#31… both logs byte-identical (101 lines)"; 01:26:27Z r5 dispatch; ≥5 jobs honored stop conditions (test-parse-hotfix 18:34Z, main-suite-red-fix 22:44Z/22:50Z, l1-intro-flow 00:59Z/01:18Z, constellation 00:41Z).
- **Reasoning:** a whole execution-permission regime matured in 3 days across ≥5 jobs; every element is reusable the next time a lane wants to "just run the tests".

### P4 — Godot fresh-worktree environment: import FIRST; sidecars load-bearing; pins measure the committed tree (NEW gotcha)
- **Target:** `AGENTS.md` Dispatch & handover (RT/PP worktree-bootstrap block) · **Class: auto**
- **Change:** new bullet: `--headless --import` precondition; untracked `.import` sidecars can be required import remaps (deleting 11 "orphans" = 10 SCRIPT ERRORs + 49 failures; "present = pin red; absent = ambient red", PP3D #29); never blanket-delete; environment red ≠ diff red (don't code-fix degraded worlds); environment-sensitive pins scope to committed tree (#29 passes pristine, bites used checkouts).
- **Evidence:** gru-09-10:26 "the 11 sidecars were load-bearing import remaps… Gru's (a) cleanup call was wrong; RESTORE ordered"; silas-09-10:71 restore verified; ledger 22:36:30Z "No loader found… ttf/glb need importers"; constellation runbook 00:18:54Z "the #28 lesson"; intro-main-fix 00:15:08Z "PASSES on a pristine tree".
- **Reasoning:** ≥3 jobs hit environment-vs-diff misattribution; the minion that code-fixed environment red called it "vacuous greens over degraded worlds" — the exact failure the store's phantom-check family guards against, now with the environment flavor.

### P5 — my-orchestrator root pull past PR #28 deletes 1237 tracked skill files (NEW gotcha)
- **Target:** `AGENTS.md` Dispatch & handover · **Class: auto**
- **Change:** new bullet: NEVER pull the live root past my-orchestrator PR #28 without an aside copy of `.agents/skills`; the PR-body restore recipe is itself the r1 BLOCKER (stale bytes under 29-file drift + pull refusal) — restore from an aside copy (issue mssoka/my-orchestrator#29); naming trap: my-orchestrator #26/#28/#29 ≠ PP3D #26/#28/#29.
- **Evidence:** gru-09-10:136 verbatim STANDING WARNING; :155 merge-time caveat; silas-09-10:38; collision-fix r1 12:32:59Z blocker text; merge event 12:39:00Z "do NOT pull the live root past the #28 merge without an aside copy".
- **Reasoning:** the very next root sync executes this trap; the store's "orchestrator root is never free" doctrine needed its concrete landmine.

### P6 — Perkins verdict posting: mssoka fallback-comment is STRUCTURAL; mint flake = one manual retry (addendum)
- **Target:** `AGENTS.md` Perkins close-out gotcha (token-mint text) · **Class: auto** (status update of the owed-fix claim)
- **Change:** 2026-09-10 addendum: mssoka repos have no perkins-token installation + own-PR approve block → formal APPROVE structurally impossible; comment carries full verdict (×2 rounds). solarity mint can flake — ONE manual retry proven (r4 formal 5168444639). Owed fix row dispatched 14:34Z 09-10 (`orchestrator-perkins-token-mint-retry-fix`) — flagged possibly orphaned 09-11; verify alive.
- **Evidence:** ledger 11:49:56Z (storyboard r1 fallback reasoning verbatim); 12:32:59Z (collision r1, PR-27 precedent); 14:35:23Z (mint retry success); gru-09-11 watch note on the orphaned row.
- **Reasoning:** the store said "tooling owes a fix task" — stale twice over (structural-not-transient on mssoka; fix now has a row that may itself need a nudge).

### P7 — Blocked rows are not PR-watched: containment-check siblings at merge close-outs (NEW gotcha)
- **Target:** `AGENTS.md` Ledger section · **Class: auto**
- **Change:** new bullet: sibling BLOCKED rows of the same repo get `git merge-base --is-ancestor` checks at merge close-outs.
- **Evidence:** ledger 11:17:43Z (l1-arpanet PR #11 merged 09-05, reconciled 09-10 "per user census ruling"); 11:18:43Z (e2-flow-qos PR #4 merged 09-04, same); playbook-consolidation 08-29 empty row closed as dup.
- **Reasoning:** 5-6-day staleness only a user census caught; the guard is one command at a step that already runs.

### P8 — `$`-expansion sibling of the backtick class (addendum)
- **Target:** `AGENTS.md` Extensions backtick gotcha · **Class: auto**
- **Change:** 2026-09-09/10 sibling: `$` in herdr payloads shell-eats dollar amounts ("paid /bin/bash" = literal $0; "US$5" mangled ×2; '//bin/bash' fragment); single-quote payloads; correct with argv-safe literal note preserving history.
- **Evidence:** gru-09-09:386; gru-09-10:220, :343 (verbatim, ×3 across 2 days).
- **Reasoning:** same hazard class, third surface; money amounts in relays are load-bearing.

### P9 — Lane-scale mothball: provider-cap holds use the handoff-then-close shape (addendum)
- **Target:** `AGENTS.md` interactive-design close-shape (08-29 addendum) · **Class: auto** (one-line flavor note)
- **Change:** 2026-09-10 lane-scale flavor: durable handoff in implementation-artifacts (never worktree-only, hash-verified BEFORE pane close), row → blocked = paused-by-hold, worktree intact, resume = fresh glm minion from the handoff doc.
- **Evidence:** ledger 17:13:51Z/52Z (Selva ×2 lanes, handoffs 49f31ada/3b600ef6, "user close ruling" + "Astra won't be back for days").
- **Reasoning:** the existing close-shape doctrine generalized from design gates to provider caps — one line so the next hold doesn't re-derive it.

### P10 — Standing Blender access + concurrency reversal (two one-line policy pointers, addenda)
- **Target:** `AGENTS.md` Shared Blender gotcha + GPU-contention caveat · **Class: auto** (recording durable user rulings with policy files)
- **Change:** Blender: verbatim standing ruling "no permission needed… I'll rather get notified when i need to review an output please" + escalation nuance + policy-file pointer; live-state forensics core still applies. Contention: verbatim reversal "pleasse dont do that. my system can handle both" — PP3D play + Selva native run CONCURRENT; no play-done prerequisite; policy-file pointer; perf claims still caveat.
- **Evidence:** gru-09-10:293 (Blender ruling verbatim); :365 (concurrency reversal verbatim); both policy files exist at `memory/*-2026-09-10.md`.
- **Reasoning:** two durable user rulings with policy files the store never pointed at; without them the next session re-runs the permission ceremony Gru was explicitly told to stop.

### P11 — BMad `ambiguous implementation_artifacts` HALT persists past 6.12; qualified-token binding is the sanctioned recovery (addendum)
- **Target:** `docs/minion-field-notes.md` tooling traps (BMad entry) · **Class: auto**
- **Change:** 2026-09-10/11 addendum: the halt is CROSS-MODULE (bmm+gds both define it — 6.12's duplicate-key repair didn't cover it); ≥4 jobs ×3 days halted; sanctioned recovery = job-local qualified-token binding + reverse byte-equality + ONE corrected official renderer bootstrap, canonical untouched. Root fix owed (see U3).
- **Evidence:** gru-09-09:122 (pMY halt), :336 (renderer attempt failed); silas-09-10:15 (gemini core blocked); ledger 16:15Z (test-parse "gate passed via job-local qualified-token binding"), 19:02Z (main-suite touched-then-restored).
- **Reasoning:** the 09-09 store entry said the waiver was retired by 6.12 — true for duplicate keys, but the cross-module class kept halting lanes for 3 days; each minion rediscovered the recovery.

### P12 — Identity/facts guards: pin locale, normalize, persist rejection evidence (NEW tooling-trap entry)
- **Target:** `docs/minion-field-notes.md` tooling traps · **Class: auto**
- **Change:** new entry: locale drift false-fire (LANG=en_GB vs absent → ps lstart format) fixed by LC_ALL=C on producer+consumer; facts-equality guards must semantically exclude ordinary terminal output; persist rejected operands (a monitor abort left cause UNKNOWN); sequence host-prep-then-fresh-receipt (idle-pass reports expire the receipt they report).
- **Evidence:** gru-09-10:338-342 (locale, verbatim + green proof); gru-09-09:106 (facts conflation "CONFIRMS ONLY p2 recent output changed during its own polling"); gru-09-09:89 (785.94s-old receipt vs 180s bound).
- **Reasoning:** cross-job (PP3D observation + Selva identity) class: any guard string-comparing whole live state will false-fire; the fixes are cheap and general.

## Proposals — USER-ACK

### U1 — User communication cadence: milestones, not paperwork (applied to store copy, held for ack)
- **Target:** `AGENTS.md` Reporting-format area (new Cadence paragraph) · **Class: user-ack** (communication policy)
- **Change:** routine hash/byte/finalization receipts stay ledger/evidence/batched, NOT repeated user relays; milestones = "actual defects closed, verified usable assets, rendered shots — not escalating preparation paperwork"; repeated "where are we?" questions are the symptom of receipt-spam.
- **Evidence:** gru-09-09:158 user PROCESS ACK verbatim ("well as long as there is real progress being made…"); the window's repeated status questions (music-video ×2, "anything pending on me").
- **Reasoning:** generalizes a user ruling from the Selva lane to all user-facing reporting — exactly the kind of persona/cadence change the briefing routes through user ack.

### U2 — Dream-craft fixes (template + playbook — NOT store copies; for Silas/Gru to apply)
- **Target:** `_bmad-output/briefings/_template-dream.md` + playbook 'Dreaming' section · **Class: user-ack**
- **Change:** (a) ledger intake = read-only timestamp census + per-job `ledger show`, NEVER latest-N alone (×2 dreams: dream-09-09 omitted 216 rows; this dream's 200-window omitted ~370); (b) the template's verification-pass line STILL names `bmad-review-adversarial-general` — the alias dangles (symlink → missing dir, verified 09-11; second sighting): either repair the root alias or repoint the template at the installed `bmad-review` adversarial lens (this pass used the successor as rubric and disclosed it, per the honest shape); (c) patch discipline is now standard: keep auto/user-ack patches separate + reproduction-test on scratch baselines (dream-09-09 lesson, reused verbatim here — PASS).
- **Evidence:** dream-2026-09-09 shard lines 1-3; my own verified symlink check + intake census this pass.

### U3 — DISPATCH RECOMMENDATION (not a doc edit): BMad root-config fix
- Make `implementation_artifacts` unambiguous at the orchestrator root (or extend the renderer to full-name resolution) — ≥4 job-halts across 3 days; the job-local binding is a workaround, not a fix. Suggested row: paneless, glm-5.3, touches only the root `_bmad` config.

### U4 — PROCESS FLAG (not a doc edit): field-notes shard lane silent 09-09 → 09-11
- Zero per-job task shards written in 3 days of heavy activity (~20 jobs) while ledger notes got rich — either re-brief the badge-out shard mandate or bless ledger-notes as the shard lane (dreams currently eat well from both; the shard lane was the richer source historically). Gru/Silas decision.

## Watch items (anecdotes — tracked, not proposed)

| 👀 | Observation | Why it stays a watch |
|---|---|---|
| W1 | DONE-on-still: Silas set overall Selva row DONE on a completed still/proposal ×2 (09-09); corrected to BLOCKED-for-look | 1 lane, 1 day; correct terminal shape recorded in lane canon |
| W2 | Frozen-boundary machinery: versioned rebinding (no in-place edits of frozen briefs), monotonic deadline reads (1800s diff, not wall clock), per-SHA ticket renewal | all 3 from the Selva native-verification lane, 2 days |
| W3 | Retained reviewer sessions refuse out-of-original-scope assignments → clean-session replacement in SAME panes | 1 lane (PP3D reviewers, 09-09); thinking-level sibling already store (P4/09-09) |
| W4 | Routed-but-unresolved issues stay OPEN — the ISSUE is the work item, the ROW only the receipt (issues/2 closed-then-reopened) | 1 sighting; complements issues-first intake |
| W5 | Gemini paid-lane pattern: exact model pin, row ceilings, hard-stop+escalate, per-batch receipts, dogfood-before-scale (found the reserve-pin flaw) | 1 lane; artifacts carry the canon |
| W6 | Numerical false-contact at 2µm tolerances: engine native nearest ≠ actual; independent binary64 verifier + RETAIN THE WITNESS before refusal | 1 lane (S47), generalizable kernel noted |
| W7 | Selva Blender endpoint switch (59538→41430) cause UNKNOWN, silent | 1 sighting, procedurally resolved |
| W8 | Post-approval r5 fix-audit shape: execution-found fixes on an APPROVED head re-arm review as a new delta | first clean instance 09-11 01:26 (folded into P3's tail; watch for recurrence) |
| W9 | Sensor wrong-repo-root false reads ×2 (round-debris "husk" labels) | 1 day, 1 sensor; sensor-doctrine-sync territory |
| W10 | Perkins round spec-path ENOENT: spec path must resolve in the ROUND's tree | 1 sighting (router-legibility r1) |
| W11 | Heredoc handover parse failure → file-pattern fallback | 1 sighting; already the standard practice |
| W12 | Double-rebase under a fast merge belt: prepared rebase went stale before PR recomputed (#27+#28 within ~30 min); verify live base right before push | confirms push-hold doctrine; wrinkle seen once |
| W13 | PP3D shutdown investigation (#23): NO holder/root cause; 73 ObjectDB/61 orphan StringNames owner UNKNOWN — archived, NOT fixed; do not let any store text imply resolution | open question |
| W14 | oEmbed title/channel verify ≠ watched-video evidence | 1 sighting |
| W15 | Review-URL anchor loss new flavor: wrong-review query eats the id from done-events (×2) | known class; new flavor noted for the standing rule |
| W16 | Ledger hygiene otherwise the cleanest window read: `pr` column 100% self-set, zero phantom rows, overclaims self-corrected against immutable receipts | positive signal, no action |
| W17 | Stray keystrokes in live/dead panes (a /thinking in a dead zsh; a cap-failed user-typed lens launch in the trail) | known class, 2 benign sightings |

## Pruned / rejected candidates (with why)

- **Frozen-boundary discipline as a standalone gotcha** (SJ#8): all evidence from one lane's native-verification machinery → W2.
- **DONE-on-still as a gotcha** (SJ#6): ×2 same lane/day → W1; lane canon carries the correct shape.
- **Gemini lane canon into the store** (SJ#15): lane canon lives in implementation-artifacts + briefings; only the generalizable paid-lane pattern noted (W5).
- **Numerical false-contact as a store entry** (SJ#13): single-lane; the witness-retention kernel is real — needs a second sighting.
- **Push-hold/rebase-delta, moot-on-merge, mega-diff chunking, 1302 one-continue, watcher pre-classification, self-close sweeps** (SL "confirms existing doctrine" list): fresh recurrence without new mechanism — no new text (double-rebase wrinkle → W12).
- **Static-only-ships-red as separate from the grant regime** (SJ#2 vs SL#1): merged into one gotcha (P3) — they are one catch net; splitting would duplicate.
- **Provider-generic cap doctrine as a new section** (SJ pruning #6): folded into P1's interlude block — the taxonomy line, not a new section.
- **Blender permission-ceremony pruning** (SJ pruning #3): the gotcha's core (live-state forensics) survived the window intact; the standing-access ruling is ADDITIVE (P10), not a deletion.
- **Watchman-pin rewrite** (SJ pruning #5): covered by P1's invalid-until-lift line; no separate edit.
- **Thinking-level launch verification** (SJ#9 sibling): already store (dream-09-09 P4); no re-add.
- **Saga detail** (PP3D editor-shutdown chain, Selva CHARGE quality ladder, board canon): per both sheep's notes — lane canon stays in artifacts; the store takes the ops residue only.

## In flight at dream dispatch (post-marker, next dream's window)

`packet-plumber-3d-lighthouse-staging-fix` (#31 boot deadlock), `packet-plumber-3d-constellation-view-perkins-r5` (execution-found delta), PP3D PR #30 user-merge-pending (last main-green gate), lanes 2-3 released pending #30. The OpenAI hold is STILL LIVE — P1's interlude text is duration-limited by design; Silas should re-check the hold state at close-out and strike the interlude when the quota returns.
