# sheep-journals — dream-2026-08-19 input (read-only pass)

Marker: 2026-08-17T17:47:09Z. Sources: gru-journal 2026-08-17 (post-17:47Z only), 2026-08-18, 2026-08-19; silas-journal 2026-08-17 (post-17:47Z only), 2026-08-18, 2026-08-19. Everything below is new since the last dream. Pre-marker 08-17 material (cap-lift loop, standing authorization, GitHub outage class, lavish 0.1.52 sync, mis-rooted lens wave) was already consolidated by dream-2026-08-17 — not re-proposed.

## Candidates

### C1 - v4-pro BANNED from the reasoning tier; chain is k3 → glm-5.3 → HOLD; park, never substitute
- flags: NEW USER RULING (08-19 morning, on record) · SUPERSEDES the 08-12 "v4-pro interim fallback", the 08-16 fallback order "glm-5.3 → deepseek-v4-pro → flash", the 08-17-night "reasoning = v4-pro" ruling, and every "mid-work 403 → /model v4-pro + continue" line
- target: AGENTS.md-gotchas (Provider incidents supersede chain; playbook Model policy already committed 7e889ec/af06ff3)
- class: auto (user ruling on record — document verbatim)
- evidence: model-policy window 08-17 evening→08-19, Gru journal: "v4-pro BANNED from reasoning tier (cost). Chain: k3 -> glm-5.3 -> HOLD (both down = no reasoning dispatches; mid-work rounds PARK until a probe flips a trusted provider back — no v4-pro continue)"; rationale 08-18: "I trust them more for reasoning"; Silas 08-19: "v4-pro zero duties (not even mechanical)". Live state at dream dispatch: k3 cycle-capped (17:47Z 08-19), glm-5.3 carrying, dream/Bob on glm-5.3.
- why: the AGENTS.md model-policy supersede chain ends at 08-16 and still names v4-pro as a sanctioned fallback/recovery target — that doctrine is retired; the trust axis (kimi/glm verdicts trusted, v4-pro too expensive) is the standing rule.

### C2 - deepseek 402 Insufficient Balance = account wall (NEW incident class) + ops-tier flip mechanics
- flags: NEW INCIDENT CLASS (402 ≠ 403/429: balance, not quota/rate — user top-up fixes it, waiting does not) · NEW USER RULING (ops flip to glm-5.3, then back to flash)
- target: AGENTS.md-gotchas (Provider incidents)
- class: auto (rulings on record)
- evidence: righttenantry-demo-mode p268, 08-19: "p268's turn errored 09:26:21Z `402 Insufficient Balance` (deepseek account-level — probe confirmed DOWN)"; the 402 also killed the r3-verdict relay delivery mid-flight; user: "switch all deepseek flash to glm5.3 now. so all ops is glm."; evening revert: "deepseek balance restored... ops/coding tier returns to deepseek/deepseek-v4-flash; the glm-5.3 ops interlude... is RETIRED. In-flight panes STAY on glm."
- why: a 402 looks like a provider incident but is a billing wall — recovery is /model <ops fallback> + continue once per errored pane (fleet wave), flip silas.ts auto-set + playbook, leave in-flight panes on their launched model, and surface the top-up to the user instead of retry loops.

### C3 - Probe doctrine hardened: probe at EVERY dispatch; recoveries flicker; freed rolling windows are not headroom; single DOWN readings can be false
- flags: extends the 08-12/08-16 "kimi back is unreliable" guard from first-dispatch to every-dispatch
- target: AGENTS.md-gotchas (Provider incidents)
- class: auto
- evidence: k3 fickle cycle 08-18/19 night, Gru: "22:35 back -> 01:41 flicker -> billing 403 mid-wave -> 03:40 back. Probe-at-dispatch is load-bearing, not ceremony."; glm window, Gru 08-19: "the early reset 03:47Z window burned through under lens load in ~4h — durable lesson: a freed rolling window is NOT headroom; glm re-caps fast under a round"; probe beats the cap message, Silas 08-18: "cap message said 17:54:28Z, reality 12:48Z; probe = ground truth"; false-negative, Silas 08-19: "hourly regime probe wrote k3 ok:false @08:10:28Z (transient, empty error) — sanctioned re-probe OK".
- why: probe-before-every-dispatch (not just post-recovery), treat early cap resets as no headroom, and re-probe once before acting on a lone empty-error DOWN row — the regime file is the record but a single row can lie in both directions.

### C4 - Dispatch-chain rewrite: no pipes on the wait, herdr 0.8.0 `agent wait --until`, sleep before the wait, pin the model on Perkins round launches
- flags: NEW BUG CLASS (2 sightings, one full round affected) · AMENDS the 08-06 chained-dispatch gotcha (stale `herdr wait agent-status` syntax) and extends the 08-13 briefing-model-lines lesson to round launches themselves
- target: AGENTS.md-gotchas (Dispatch & handover)
- class: auto
- evidence: packet-plumber-wire-aesthetics-perkins-r1 + 6.2 r1, Silas 08-19: "my launch chain `herdr agent wait ... 2>&1 | tail -1 && sleep 3 && herdr pane run <handover>` — the PIPE MASKS the wait's failure exit code (tail returns 0), so the && chain CONTINUES even when the agent isn't ready"; compound: "herdr 0.8.0 renamed the command (`herdr agent wait --until idle`, not the playbook's `herdr wait --status`)"; "bare `pi` launch resolves to defaultProvider = deepseek-v4-flash — a Perkins judgment round MUST launch `pi --model kimi-coding/k3` explicitly"; consequence: "wire-aesthetics r1 (p28F) ran ENTIRELY on flash (single inline review, no lens tab spawns, closed APPROVED 0B — verdict stands on code verification, but off-chain model + no 7-lens fan-out)" (flash-APPROVED sanctioned on the row); registration race: "herdr agent wait races pi registration on fresh panes — sleep 10 before the wait"; corrected chain proven: "sleep 12 for registration + un-piped agent wait — FULL-CHAIN-OK first try".
- why: the documented chain in the gotchas is stale and pipe-fragile — rewrite it (un-piped `herdr agent wait <pane> --until idle --timeout 90000`, sleep 10–12 before the wait, explicit full-path `--model` on round launches, verify session modelId after every launch).

### C5 - A mid-flight /model on a WORKING pane ends the current turn — pair it with a continue
- flags: refines the 08-08 "model corrections don't need a kill" gotcha
- target: AGENTS.md-gotchas (Model dispatch & correction ops)
- class: auto
- evidence: packet-plumber-v2-6.2-advance-trigger r1 (p28Y), Silas 08-19: "p28Y ended CLEANLY (stop:stop) 09:25:34Z — my mid-flight /model interruption consumed the turn; the round stranded mid-verification, only diff.patch saved, no post"; recovery: "continue sent 12:49Z → round WORKING... The recovery arc held: stranded round (my /model interruption) → continue → complete verdict."
- why: /model mid-turn is not free — the switch terminates the in-flight turn; always follow it with an explicit continue/instruction or the pane sits idle-looking with the work stranded.

### C6 - NEW stall class: round main clean-stops AFTER its lens wave (everything on disk, no consolidation, no post)
- flags: NEW INCIDENT CLASS (distinct from error-stop wedge: STOP:stop, not STOP:error)
- target: AGENTS.md-gotchas (Perkins round ops / pane forensics)
- class: auto
- evidence: terminal-assets-5.11 r1, Silas 08-18 04:55Z: "its turn ended 00:18Z right after the blind lens wrote (STOP:stop), all 7 lens panes finished + JSONs on disk, but no consolidation/post (no review on #65) — pi alive + idle for 4.5h... NEW LESSON SHAPE: a round can stall AFTER its lens wave with everything on disk — the round main's done→idle with lens panes done + no review = the stall signature"; recovery: one continue-nudge with the security-retry/degraded-guard instruction.
- why: an idle round main with completed lenses and no posted review is NOT settle noise — it's a recoverable stall; one continue with the retry instruction revives it without re-running the wave.

### C7 - Kimi cycle-403 landing mid-session wedges the turn loop (continues inert; model-switch + continue revives)
- flags: NEW FAILURE MODE flavor of the quota-403 class
- target: AGENTS.md-gotchas (Provider incidents / pane forensics)
- class: auto
- evidence: packet-plumber-v2-7.1-visual-juice, Silas 08-17 18:45Z: "7.1's turn wedged at 18:39 (STOP:error on the Blender MCP connect failure; continue + send-keys inert, messages recorded but unprocessed). ROOT CAUSE: kimi k3 cycle quota exhausted... the turn-loop wedge is the new failure mode when the limit lands mid-session. REVIVED via /model <fallback> + continue"; recovery target is now glm-5.3 per C1 (never v4-pro).
- why: when continues and send-keys both go inert on a live pane, suspect a mid-session quota wall — the durable fix is the model switch plus continue, not more continues.

### C8 - k3-cap concentration: all reasoning on glm → episodic fleet-wide 1302 bursts; one continue each, throttle new glm load
- flags: NEW capacity interplay (single-provider concentration under a capped primary); the 08-14 glm serialize ceiling resurfaces
- target: AGENTS.md-gotchas (Provider incidents / Perkins bursts)
- class: auto
- evidence: QoS-r1 + demo-mode-r4 + 7.3-r1 + dream panes, Silas 08-19 17:53Z: "k3 cycle-capped -> ALL reasoning on glm... glm account 1302 account-rate-limit burst hit every pane (17:53-17:54Z...)... The wave is EPISODIC, not a hard wall: every pane recovers on one continue, then trips again minutes later (fleet-wide glm account ceiling under the k3 cap). Recovery loop works; no new glm work until it settles"; escalation gate: "Gru flag held unless continues stop clearing (then: account ceiling + drain/priority decision)".
- why: when the primary reasoning provider is capped, glm inherits the whole fleet and 1302s in waves — one continue per errored pane, hold NEW glm dispatches until the wave settles, escalate only if continues stop clearing.

### C9 - Lens-fleet rotation on mid-round provider flip: sweep/re-model the capped provider's lens panes
- flags: NEW doctrine candidate (proposed by Gru after user sighting; not yet codified)
- target: AGENTS.md-gotchas (Perkins round ops)
- class: auto
- evidence: righttenantry-demo-mode-perkins-r3, Gru 08-19: "user spotted glm-labeled mm panes — resolved as r3 launch provenance (lenses launched 03:47Z on glm pre-cap); post-1308 the fleet rotated: old glm panes swept, fresh lenses p282-p287 verified on k3; survivor p27T idle -> sweep-or-remodel note... New doctrine candidate: sweep/re-model capped-provider lens panes when a round flips provider mid-round."
- why: a mid-round provider flip orphans the old provider's lens panes (idle survivors burn pane count and confuse forensics) — close-out and mid-round sweeps should rotate them with the round, scoping to the round's own pane ids per the 08-17 P7 rule.

### C10 - herdr 0.8.0 tab create can land in a stray workspace — pass explicit --workspace; capture post-move pane id
- flags: supersedes the 08-18 "tab create --cwd lands directly in w1T, no move needed" observation (which did not hold)
- target: AGENTS.md-gotchas (Extensions / pane ids)
- class: auto
- evidence: righttenantry-demo-mode-perkins-r4 (tab tG5) + 7.3-r1 (p299), Silas 08-19: "the tab create landed in w6H — a leftover source workspace — moved into w1T, post-move id captured"; fix: "pane w1T:p299 created DIRECTLY in w1T (explicit --workspace flag — fixed the w6H landing from the r4 tab)"; also note the 0.8.0 tab-create returns `root_pane` key.
- why: --cwd alone does not pin the workspace on 0.8.0 — a leftover source workspace can capture the new tab; explicit --workspace + post-move id capture keeps the ledger row pointing at a real pane.

### C11 - User-in-pane model experimentation: flag degradation risk, never reverse, restore only per ruling — and ask if the experiment is still live
- flags: NEW pattern (direct-to-pane user model switches mid-job)
- target: AGENTS.md-gotchas (pane forensics)
- class: auto
- evidence: 6.2 (p281) + 7.3 (p296) + demo-mode (p268), Silas 08-19: "p296 followed p281: abort x2 + /model qwen3.8-27b 16:40:56Z, ~30s apart — deliberate user experimentation with the local qwen... flagged to Gru with the restore command; no reversal by me (user is in the pane)"; restore executed per the stay-on-glm ruling; Gru: "OPEN: user never confirmed whether the qwen experiment was finished — if it was still live, the restore undid it; ask."
- why: when the user drives a pane directly (aborts + /model), ops response is a provenance/degradation flag only (65k window vs 1000%+ context) — reversal is the user's call, and ambiguous experiment state gets an explicit ask, not an assumption.

### C12 - Audit intake doctrine: issues-first, fix-now vs batch split, fix jobs scope-guarded against the batch
- flags: NEW USER RULING ("create github issues for them first") — generalizes beyond this audit
- target: AGENTS.md-gotchas (new small entry near the audit/FYI routing material) or playbook
- class: auto (directive on record)
- evidence: righttenantry-security-audit → RT #625/#626 → righttenantry-security-m1-stripe-payment-status, Gru 08-18: "user 'create github issues for them first': RT #625 = M-1 fix-now (Stripe payment_status unlock webhook — full citations, acceptance, both remediation arms); RT #626 = batch M-2..M-8 + 25 Low + 14 Info"; M-1 briefing "scope-guarded against the #626 batch items"; M-1 closed r1 APPROVED + merged same day.
- why: audit findings route to GitHub issues BEFORE any fix dispatch (fix-now issue + batch issue), and the fix-now job is scope-guarded so it cannot eat batch items — this is the durable intake shape for future audit/heist outputs.

### C13 - Business priority ruling: RT is the priority business; PP belt merge-gated and self-pacing
- flags: NEW USER RULING (portfolio-level)
- target: playbook (Concurrency, already amended 0d70ff5) — AGENTS.md pointer optional
- class: auto (ruling on record)
- evidence: 08-18/19 night, Gru: "RT is the priority business, PP is not... Ops doctrine: RT wins contested resources (panes/quota/Perkins/dispatch windows)"; clarification: "PP is NOT killed and NOT rushed — the belt runs at minion pace; user's merge keystrokes happen at their leisure (belt is merge-gated, so it self-paces)... no urgency framing on PP merge relays; batch them."
- why: capacity conflicts now resolve RT-first while the PP belt runs autonomously to the fun-test gate — worth one line in the orchestrator memory so future holds/serializations don't default to PP-first or add urgency framing.

### C14 - Valve/serialize-holds are advisory under full throttle: "let them all run"
- flags: NEW USER RULING · QUALIFIES the serialize-hold-for-pane-capacity gotcha ("Pane-capacity judgment stays Silas'" now means: propose, but user override is standing)
- target: AGENTS.md-gotchas (Serialize-hold for pane capacity — amend)
- class: auto (ruling on record)
- evidence: packet-plumber-wire-aesthetics-perkins-r1, Gru/Silas 08-19: "User: 'dont hold... let them all run.'... the 08-16 full-throttle ruling extends to valve-pressure holds; note on the wire-aesthetics row so the sensor doesn't re-hold"; executed: "Both rounds in flight (RT r3 + PP r1) — 21 panes, valve overridden per user ruling."
- why: pane-count valve holds no longer gate by default — record the hold as a row note and dispatch; the valve is a signal to surface, not a blocking rule, unless the user says otherwise.

### C15 - Deferred-registry is live (#6 reversal): deferred:<provider> tags + probe auto-surface; graph keys set via sqlite3 after add
- flags: NEW MECHANISM FIRST-FIRE (reference case) · corrects the AGENTS.md upgrades note that listed #6 as declined
- target: AGENTS.md-gotchas (Orchestration upgrades section — amend; ledger hygiene)
- class: auto (#6 approval was a user ruling, on record)
- evidence: righttenantry-security-audit, Silas 08-18 12:55Z: "the 12:48Z probe confirmed glm-5.3 BACK UP... → the parked security-audit (deferred:glm) surfaced LIFTED → RESUMED on zai-coding-cn/glm-5.3... the mechanism fired IMMEDIATELY (reference case)"; Gru 08-17 night: "#6 DEFERRED-REGISTRY APPROVED (user, night): the previously-declined #6 is now wanted"; hygiene: "the ledger CLI's add-key list lacks blocked_by/coordinate_with — set via sqlite3 UPDATE after add"; echo flavor: "the queue's DEFERRED READY SET line for security-audit is a stale echo (already resumed + escalated)".
- why: the upgrades note in AGENTS.md is stale on #6, and two small ops facts (sqlite3 UPDATE for graph keys; DEFERRED lines can echo stale) belong with the ledger gotchas so the new tooling isn't misread on first use.

### C16 - Vision doctrine: no silent auto-delegation; explicit local vision on qwen3.8-27b-mlx@4bit; pi models.json needs input:["text","image"]
- flags: NEW USER-DRIVEN DOCTRINE (test-ruled: "more accurate wins, we wait") · NEW pi-level gotcha (models.json input gate)
- target: AGENTS.md-gotchas (model/tooling section; the vision-read skill already carries ops detail)
- class: auto (ruling + test on record)
- evidence: 08-18, Silas: "vision.json DELETED (was kimi-k3 primary + silent lmstudio/gemma fallback; audit log proved 15+ invisible lmstudio delegations on 08-18, all fallback=true, lying log identity 'kimi-coding/lmstudio/...')"; test: "QWEN DECISIVELY MORE ACCURATE... 4-bit: 127s+215s... 4× faster, same accuracy. VISION = lmstudio/qwen3.8-27b-mlx@4bit"; gate gotcha: "pi gates image attachment on the model's declared input types; the models.json qwen entries lacked `input: ['text','image']`"; patience: "~2-3.5 min/image (empty reply mid-reasoning ≠ failure)"; bin/vision-read + skill shipped.
- why: silent vision fallback lied in the logs for a day before being caught — vision is now explicit/local by doctrine, and any future local model registration must declare image input or the read tool silently degrades.

### C17 - After a rebase, rebuild locally-built harness/binaries before re-blessing (stale-build trap)
- flags: minion-facing lesson (Perkins-adjacent)
- target: docs/minion-field-notes.md
- class: auto
- evidence: packet-plumber-v2-5.11-terminal-types, Silas 08-18 13:00Z: "the minion caught its own STALE-HARNESS trap (bin/harness built pre-rebase had no map.odin → background-less frames; rebuilt, amended a2dc66e→11c6cf6 with corrected frames, force-with-lease)".
- why: a pre-rebase local build silently produces wrong golden frames after the tree moves — rebuild harness/binaries post-rebase and amend rather than blessing stale output.

## ANECDOTE (one-offs — record, don't codify)

- **A1 — minion canonized its own drift in a code comment.** packet-plumber-v2-qos-default-standard, 08-19: "root cause: 5.8 drifted — balanced [1,1,1] (~33/33/33) applied as the pipe default at apply_draw... (documented as canon in balance.json comment)". A drift written up as canon in-tree survived to user report; worth a field-notes line if the class recurs, else anecdote.
- **A2 — quota-probe arg-guard.** 08-19: "Regime file had a bogus '--help' probe row 03:53Z — quota-probe arg-guard, noted to Silas as hygiene." Tool hygiene only.

## Reinforcements (existing gotchas held — no new candidate)

- **Escalation gap recurrence** (6.1 close-out 08-19 executed but "never escalated... Re-escalated to Gru 08:13:58Z") — the 08-01 "deliverable not reported until it reaches Gru's input" gotcha, sighting #3.
- **P7 lens-sweep scoping held**: 5.11-r1 close-out 08-18 closed "its 10 properly-rooted lens panes (tab tES, P7-safe: own-pane-scoped)".
- **Pre-emptive verdict note on empty self-close**: wire-aesthetics r1 08-19 "row self-closed by Perkins (empty result — verdict recovered as pre-emptive note per the standing gotcha)".
- **Degraded-guard + mechanical compensation proven**: 5.11 g-wave "compensation delivered valid 7/7 verdict (51/71 findings) — no sweep, doctrine worked"; #67 APPROVED on 5/7 lenses + independent mechanical verification.
- **Template model-line rot again**: dream-2026-08-19 briefing "AMENDED Model policy... the template's v4-pro fallback BANNED per the 08-19 morning ruling" — the 08-13 lesson recurred within 6 days.
- **Full-path + provenance verification now standard practice**: QoS p29H and 7.3-r1 p299 launches 08-19 both "provenance verified (sole modelId)". The pr-field discipline held (M-1: "pr field self-set (discipline held)").

## Supersede summary (for the consolidation pass)

1. v4-pro as reasoning fallback/interim/recovery-target: RETIRED (C1) — purge from the 08-12/08-16/08-17 supersede chains' operative guidance.
2. `herdr wait agent-status <pane> --status idle` chained form in the 08-06 dispatch gotcha: REWRITE (C4) — 0.8.0 syntax + no pipes + pre-wait sleep + pinned round models.
3. Serialize-hold-for-pane-capacity as a default gate: QUALIFIED to advisory (C14).
4. "herdr 0.8.0 tab create --cwd lands directly in w1T (no move step)": SUPERSEDED (C10) — explicit --workspace required.
5. AGENTS.md upgrades note "#6 deferred-verdict registry declined": STALE (C15) — approved 08-17 night, implemented 08-18.
