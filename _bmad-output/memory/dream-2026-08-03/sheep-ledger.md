# Sheep findings — ledger events

Material: 200 events scanned (full `ledger events 200` window, 2026-07-31T18:46Z → 2026-08-03T10:50Z), 23 jobs shown, since marker 2026-08-01T10:44:57Z.

## Candidate patterns

### P1. Provider incidents arrive in 3 distinct classes, each with its own recovery move
- Sightings:
  - righttenantry-form-stepper-f1, 2026-08-01T17:42:49Z — "provider stall (kimi-coding timeouts x4, stopReason:error)… sent 'continue', pane back to working within 30s" (transient stall → `continue`).
  - righttenantry-refcheck-rc1-2, 2026-08-01T19:30:58Z — "provider refusal mid-turn ('model refused to complete the request', stopReason:error verified in session jsonl…). Sent 'continue', pane back to working in <30s" (refusal class → `continue`).
  - righttenantry-form-save-resume-f3-perkins-r2, 2026-08-02T10:10:21Z — "RETRY dispatched 10:15Z on same sha 11fcaa3 (first attempt died mid-round on account-wide kimi-coding 403 at ~05:14Z…). Dead panes swept (7 lenses + Perkins), stale worktree re-added. Briefing amended: regenerate all lens verdicts from THIS run. Quota evidence of recovery: finlit p6 active 10:01Z. Second failure -> blocked + escalate." (quota wall → full retry sweep, NOT `continue`).
  - righttenantry-form-save-resume-f3-perkins-r2, 2026-08-02T12:28:59Z — "fleet-recovery: connection-error wave blocked lead + 7 lenses mid-round; 'continue' x9 per doctrine — all back to working (Gru revived Silas the same way). Reviewed sha verified unchanged" (connection wave → mass `continue` + sha verification).
  - finlit-gdd-v1, 2026-08-03T10:04:32Z — "Third provider incident today: 05:14Z quota 403, 12:0xZ connection wave, 22:4xZ connection wave." (all three classes in one day).
- Common discipline: verify `stopReason:error` in the session jsonl before acting; ledger status stays `working`; escalate on second failure. The quota-403 class is the only one needing a sweep+re-dispatch (dead panes closed, worktree re-added, briefing amended to regenerate lens verdicts, recovery evidenced via another job's activity).
- Candidate memory target: AGENTS.md gotchas (extends the existing 2026-08-01 errored-turn entry into a 3-class taxonomy with the quota-wall sweep procedure).

### P2. Sensor-vs-write races: review/perkins sensors re-alert seconds-to-minutes after Silas already acted — classify, note "no double X", move on
- Sightings (6+ in 2 days):
  - righttenantry-form-save-resume-f3, 2026-08-02T13:37:58Z — "13:35Z Perkins-sensor r3 alert on 8789054 = stale echo of my proactive r3 dispatch… No double dispatch. Third sensor-vs-write race today — pattern documented."
  - righttenantry-form-save-resume-f3, 2026-08-02T03:16:56Z — "review-sensor CHANGES_REQUESTED alert = r1 review 4836863940 ALREADY relayed to w1T:p1Y at Perkins round close-out… No double relay."
  - righttenantry-form-save-resume-f3, 2026-08-02T15:17:36Z — "sensor cap-3 'human review needed' alert = ALREADY escalated to Gru with the full context… seconds prior. No double escalation."
  - righttenantry-refcheck-rc1-2, 2026-08-01T20:23:41Z — "review-sensor APPROVED alert = review 4835656981 ALREADY escalated to Gru at Perkins round close-out (same tick as the held-r2 release)."
  - righttenantry-form-stepper-f1, 2026-08-01T21:22:04Z — "21:21Z sensor tick = two stale echoes, no action."
- Root cause visible in the record: Silas relays/escalates/dispatches at round close-out; the sensor tick lands after and re-fires the same review/sha. Handled by writing the row/note in the same minute (durable dedup) and answering every echo with a same-status note, never a second action.
- Candidate memory target: AGENTS.md gotchas (distinct from the existing settle-transition entry — this is the review/perkins/cap sensor echo class).

### P3. Perkins rounds can self-close (pane close writes done) → same-status set collision eats the verdict; pre-emptive verdict note is the insurance
- Sightings:
  - righttenantry-form-save-resume-f3-perkins-r2, 2026-08-02T13:27:37Z — "VERDICT (re-recorded after a same-status set collision): NEEDS CHANGES (1B) on 11fcaa3…"
  - righttenantry-form-save-resume-f3-perkins-r3, 2026-08-02T15:04:04Z — "If the done-set above hit a same-status no-op (Perkins self-close), this note carries the verdict."
- Existing gotcha covers `set` same-status refusal + `note` workaround; the new wrinkle is the *cause* (Perkins self-close on pane shutdown) and the practice of writing the verdict note pre-emptively at close-out rather than discovering the loss later.
- Candidate memory target: AGENTS.md gotchas (amend the existing same-status entry).

### P4. Perkins skip rows preserve the 3-round cap and silence per-tick re-alerts (sha-scoped dedup)
- Sightings:
  - righttenantry-form-stepper-f1-perkins-skip-61fd895, 2026-08-01T19:23:05Z — "round SKIPPED: head delta is docs-only… Skip preserves the 3-round cap and silences per-tick re-alerts via durable sha dedup."
  - righttenantry-form-stepper-f1-perkins-skip-b13c974, 2026-08-01T21:19:27Z — "round SKIPPED before dispatch: r2 (on 7ac11fe) found 2 REAL blockers… burning the FINAL round 3 on it guarantees a stale CHANGES_REQUESTED. Rework relayed to minion; r3 reviews the fix push."
  - Payoff sighting: righttenantry-form-stepper-f1-perkins-r3 row note — "round 3 (FINAL) — dispatched proactively on the r2-fix push (merge candidate); b13c974 skip-row preserved the cap for this" → APPROVED 0B.
- Candidate memory target: minion-field-notes.md (orchestration practice that demonstrably worked).

### P5. Rework-loop dynamics: every Perkins round's rework can introduce the next round's blocker; token/PII leakage recurred across seams
- Sightings:
  - righttenantry-form-stepper-f1 arc (PR #561): r1 "2B/4W/6N" (2026-08-01T19:20) → r2 "2 new blockers both in reworked E2E suite" (2026-08-01T21:19:50Z — the r1 *rework* created them) → r3 "APPROVED (FINAL round)… fix audit 5 fixed/15 carried/1 absorbed" (2026-08-01T22:17:34Z).
  - righttenantry-form-save-resume-f3 arc (PR #563): r1 "B1: continue-link token URLs trust X-Forwarded-Host (PII token exfil vector)" (2026-08-02T03:15) → r2 "B1 detached-window.setTimeout debounce break (empirical)" + "r1: 28 fixed, 11 carried" (2026-08-02T13:27) → r3 "B1: PostHog autocapture leaks raw data-resume-token from <body> past the URL scrub" (2026-08-02T15:04).
  - Recurring finding class: token/PII exfiltration surfaced in a *different seam* each round (URL generation → analytics DOM scrape) — scrub-in-one-place findings imply audit-the-whole-token-path.
- Candidate memory target: minion-field-notes.md.

### P6. Cap mechanics worked end-to-end: cap-3 → 'human review needed' escalation; override only by explicit user ruling
- Sightings:
  - righttenantry-form-save-resume-f3-perkins-r3, 2026-08-02T15:04:04Z — "CAP REACHED: new sha escalates 'human review needed'."
  - righttenantry-form-save-resume-f3, 2026-08-02T15:17:03Z — "CAP: human review needed — escalated to Gru with merge recommendation."
  - righttenantry-form-save-resume-f3-perkins-r4 row note, 2026-08-03T10:03:38Z — "EXPLICIT USER CAP-OVERRIDE (verbatim: 'one more perkins round on #563', via Gru 2026-08-02; sets no precedent, cap stays 3)."
  - Contrast (clean convergence): righttenantry-form-stepper-f1, 2026-08-01T22:17:05Z — "Perkins r3 (FINAL): APPROVED — READY TO MERGE, 0B/6W… Escalated to Gru: merge when ready."
- Candidate memory target: minion-field-notes.md.

### P7. Proactive next-round dispatch on the fix push (with prior_findings handed over) — works, but is the cause of P2 races
- Sightings:
  - righttenantry-form-save-resume-f3, 2026-08-02T03:46:17Z — "Perkins r2 dispatched proactively — pane w1T:p2V, prior_findings=r1."
  - righttenantry-form-save-resume-f3, 2026-08-02T13:37:29Z — "FINAL Perkins r3 dispatched proactively — pane w1T:p48, prior_findings=r2, timer-seam real-browser verification instructed."
  - righttenantry-form-stepper-f1, 2026-08-01T21:26:58Z — "r3 (FINAL) dispatched proactively — pane w1T:p1E, prior_findings=r2 consolidated, rebase+wiring in scope."
- Precondition visible in the record: round row + matching full-sha note written the same minute, so later sensor ticks dedup silently (see P2).
- Candidate memory target: minion-field-notes.md.

### P8. Hold-release for pane capacity: pre-create the round row as `dispatched` to dedup the sensor, attach pane/worktree only at execution
- Sightings:
  - righttenantry-form-stepper-f1-perkins-r2 row note — "DISPATCH HELD for pane capacity: rc1-2's Perkins r1 mid-flight (~16 panes; +8 would breach the ~20 valve — playbook Perkins Concurrency: serialize). Row pre-created dispatched to dedup the sensor; pane/worktree attached at execution."
  - righttenantry-form-stepper-f1-perkins-r2, 2026-08-01T20:22:26Z — "hold released 20:25Z (rc1-2 r1 closed, capacity freed): pane w1T:pY/tA, worktree detached @ 7ac11fe."
  - righttenantry-form-stepper-f1, 2026-08-01T21:26:58Z — "Valve: ~16 panes peak."
- Candidate memory target: minion-field-notes.md.

### P9. Queue-next notes on the parent row + user sequence-flips, executed cleanly at merge gates
- Sightings:
  - righttenantry-form-stepper-f1, 2026-08-01T15:48:28Z — "QUEUED on merge close-out: dispatch righttenantry-form-save-resume-f3… if this job is blocked/killed, escalate to Gru instead of dispatching C."
  - righttenantry-form-stepper-f1, 2026-08-01T18:41:37Z — "SEQUENCE CHANGE (user ruled, 2026-08-01): prior 'dispatch rc1-2 in parallel at B-merge' note SUPERSEDED. New order: (1) rc1-2 dispatched NOW on plain develop (fixes the unsubmittable-develop trap); (2) #561 merge HOLDS…"
  - righttenantry-form-stepper-f1, 2026-08-01T20:44:05Z — "GATE LIFTED: rc1-2 merged (4e7c3c9). Rebase relay sent to w1T:p3… Rebase blowup → minion HALTs with numbered questions → escalate to Gru."
  - Payoff: righttenantry-form-save-resume-f3, 2026-08-02T00:03:00Z dispatched at the #561-merge gate; #561 rebased (b13c974) and merged 2026-08-02T00:00:03Z with the attestation wiring in.
- Candidate memory target: minion-field-notes.md.

### P10. Banked seams/handoffs between jobs demonstrably get consumed by successors
- Sightings:
  - righttenantry-refcheck-rc1-2, 2026-08-01T19:45:26Z — "Stepper-rebase note banked: reference_attestation.validate_choice(values) @ reference_attestation.gleam:44 is the single owner of the attestation rule — lift into References-step gating as-is."
  - righttenantry-form-save-resume-f3, 2026-08-02T01:54:31Z — "Built on the rt:form-step-changed seam exactly as handed off."
  - righttenantry-refcheck-rc2-1, 2026-08-01T00:51:35Z — "FOLD INTO FUTURE BRIEFINGS: (1) RC2.3 — A6 re-enable (skipped→queued) must restore next_attempt_at=now()…"
  - righttenantry-refcheck-rc1-1, 2026-08-01T01:24:18Z — "BANKED: (1) deploy gate stands… (2) XFF trust note (security lens): client_ip first-hop comment wrong under Cloudflare… fold into RC5.2 hardening."
- Candidate memory target: minion-field-notes.md.

### P11. Round close-out formula: verify review posted, 0 lens leftovers, pane closed, worktree removed, verdict noted — then relay rework
- Sightings:
  - righttenantry-form-save-resume-f3-perkins-r3, 2026-08-02T15:04:04Z — "round closed out 15:05Z: review verified posted, 0 lens leftovers, pane closed, worktree removed."
  - righttenantry-form-save-resume-f3-perkins-r2, 2026-08-02T13:27:37Z — "21/21 lens verdicts regenerated, 0 retries, 0 lens leftovers. Round closed out 13:30Z (pane p3H + worktree gone); rework relayed to f3 minion (working)."
  - righttenantry-form-stepper-f1, 2026-08-01T21:20:42Z — "r2 closed out (pane+worktree gone, 0 lens leftovers). 2-blocker rework relayed to w1T:p3 (working)."
- Candidate memory target: minion-field-notes.md (unless already verbatim in the playbook — then report-only).

### P12. Lavish rulings loop for DOCS deliverables: review posted → user rules in-browser → verdict relayed to the pane → PR only after
- Sightings:
  - finlit-gdd-v1, 2026-08-01T20:40:43Z — "USER RULINGS received via lavish session finlit-gdd-rulings.html (ended by user): Q1 Legacy Score APPROVE; Q2 reroll HOLD… Relayed to minion w1T:p6 (working). lavish-wake scratch pane w1T:p16 closed after drain."
  - righttenantry-refcheck-privacy-draft, 2026-08-02T10:05:10Z — "lavish verdict applied 3/3 (secrets scrub, comment-only marker, scope patch); committed ebeaa33 locally; holding push+PR for verdict relay per briefing."
  - righttenantry-refcheck-v1-epics, 2026-07-31T19:33:34Z — "lavish review COMPLETE — user reviewed, 'looks good.', Send & End, ZERO annotations; PR #553 stands as pushed."
- Candidate memory target: neither (report-only — already encoded in project instructions; record shows it working as designed).

## One-off anecdotes (single sighting — watch items)

- **Skip-row dedup needs the full 40-char sha.** righttenantry-form-stepper-f1, 2026-08-01T21:20:42Z — "b13c974 skip-rowed (fixed full-sha after a format slip — dedup needs sha=<full40>)". Single sighting but a mechanical trap with zero cost to record — strong AGENTS.md gotcha candidate despite n=1.
- **Watcher 'pane vanished' can be self-inflicted by your own cleanup.** righttenantry-form-save-resume-f3-perkins-r2, 2026-08-02T10:10:43Z — "watcher 'pane vanished' on w1T:p2V = SELF-INFLICTED: that was the quota-dead first-attempt pane I closed during the retry sweep; row already re-pointed to the retry pane w1T:p3H."
- **Ledger event text strips `$` amounts.** finlit-tutor-economy-fix, 2026-08-01T01:42:27Z — "Duplex was 0 vs 4+/tick wages (~2.5 ticks!); rebalance Cart 50/Duplex ,000" — prices mangled (currency signs lost). Don't rely on $ figures in ledger notes; keep them in PR bodies.
- **Provider instability trend:** finlit-gdd-v1, 2026-08-03T10:04:32Z — "Third provider incident today: 05:14Z quota 403, 12:0xZ connection wave, 22:4xZ connection wave." Watch whether kimi-coding waves cluster daily.
- **Gleam format must cover all packages.** righttenantry-refcheck-rc2-1, 2026-07-31T22:21:19Z — "CI red→green — minion had formatted server but not shared/; fix d340be2 (gleam format shared)."
- **In-flight at scan time:** righttenantry-form-save-resume-f3-perkins-r4 (working since 2026-08-03T10:05:55Z, user cap-override round on d3f7700), finlit-gdd-v1 (working, rulings applied), righttenantry-refcheck-privacy-draft (working, holding push+PR for verdict relay), dream-2026-08-03 (this pass).
