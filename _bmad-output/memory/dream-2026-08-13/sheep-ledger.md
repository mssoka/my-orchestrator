# Sheep findings — ledger events (dream 2026-08-13)

Window: 2026-08-11T16:06:54Z → 2026-08-12T11:58:52Z (~200 events, `ledger events 400`).

## Candidate patterns

### C1 — glm-5.2 429 taxonomy: 1302 burst vs 1308 5-hour hard cap (and the dual-provider-down state)
- Suggested target: AGENTS.md gotchas → Provider incidents
- Evidence:
  - righttenantry-refcheck-rc3-6-perkins-r1 2026-08-11T20:47:45Z: "glm-5.2 account rate-limit 429 (code 1302): 7 lenses + orchestrator + pp-2.1 minion = ~9 concurrent glm calls tripped the burst limit; lenses still churning (working), orchestrator's turn blocked after 3 retries. Recovering with one continue after the burst settles"
  - righttenantry-refcheck-rc3-7 2026-08-11T21:13:00Z: "(Pattern: 9+ concurrent glm panes = guaranteed 429 — the board is at the glm-concurrency ceiling.)"
  - packet-plumber-v2-3.1-packet-types 2026-08-12T00:27:18Z: "glm-5.2 5-HOUR USAGE CAP REACHED (429 code 1308 — NEW class, NOT the 1302 burst): '已达到 5 小时的使用上限。您的限额将在 2026-08-12 09:00:47 重置'. Account-wide ZAI/glm cap exhausted by today's 5 Perkins rounds + 8 dispatches; NO continue-recovery (hard wall until 09:00:47Z)."
  - packet-plumber-v2-3.1-packet-types 2026-08-12T06:00:03Z: "Auto-resumed (verified genuinely progressing — editing core/catalog.odin, no 429s): the fleet's idle glm panes backed off the rolling 5h-window usage enough to free capacity ahead of the 09:00:47Z full reset."
- Why it matters: 1308 is a new failure class with a DIFFERENT recovery (block + timed auto-resume, no continue) than 1302 (one continue after burst settles); kimi billing-403 + glm 1308 together = both providers down → hard wall. ×4 sightings.

### C2 — Echo discipline validated end-to-end: pre-emptive settle/verdict notes classify the echo BEFORE it fires; review-sensor, PR-watcher, and pane-watcher all twin each other
- Suggested target: AGENTS.md gotchas (reinforcement — already documented; evidence shows it works)
- Evidence:
  - righttenantry-refcheck-rc3-5-perkins-r2 2026-08-11T16:26:33Z: "Stale echo (16:06:46Z working->done): already closed out this turn — row done, pSE closed, worktree removed, verdict APPROVED escalated to Gru. No double-action."
  - packet-plumber-v2-1.3-packet-flow-perkins-r1 2026-08-11T17:00:22Z: "Review-sensor echo of APPROVED review 4908698116: twin to the pane-watcher alert actioned last turn (round closed out + merge-ready escalated to Gru). Note-only — no double escalation."
  - packet-plumber-v2-2.3-demolish 2026-08-11T23:52:05Z: "PR-watcher MERGED echo (23:49:48Z): already closed out last turn (merge gh-verified via the 3.1 base; ledger done, v2 synced b0b9e0a, worktree+branch removed, pV6 closed). Note-only — no double close-out."
  - packet-plumber-v2-3.1-packet-types 2026-08-12T08:52:27Z: "settle echo (done->idle 08:52:23Z): note-only — classified at 08:30Z (r2 rework @ a980194 pushed clean, pane parked-dead). No new content; no action."
- Why it matters: ×12 sightings, zero double actions — the note-at-close-out + note-only-echo loop is now routine and reliable; no new writing needed, just keep it.

### C3 — Serialize-hold lifecycle mechanics: release-trigger taxonomy, sha-refresh at release, user parallel-override
- Suggested target: playbook (serialize-holds / Perkins dispatch)
- Evidence:
  - righttenantry-refcheck-rc3-7 2026-08-11T22:12:02Z: "r1 SERIALIZE-HELD row pre-created (sha 2bf2577 dedup). No double-action."
  - packet-plumber-v2-3.1-packet-types 2026-08-12T08:29:13Z: "Perkins r2 auto-refires on new head — round row pre-created + SERIALIZE-HELD."
  - packet-plumber-v2-3.1-packet-types-perkins-r2 2026-08-12T09:26:14Z: "RELEASED (trigger: #604 r1 close-out + #28 CI green 4/4)"
  - packet-plumber-v2-3.1-packet-types-perkins-r2 2026-08-12T09:22:09Z: "sha refreshed: a980194 -> abe578b00c13c468331c2c0fc33caa4ae435f7c1 (rebase landed 09:21Z). Release on #604 r1 close-out; re-verify head at release."
  - packet-plumber-v2-3.2-lane-qos 2026-08-12T11:40:38Z: "RELEASED (verdict gate OPEN — #30 r1 APPROVED 4916019621): dispatched ... (fresh sha at release)"
  - righttenantry-refcheck-rc4-2-perkins-r1 2026-08-12T11:19:50Z: "RELEASED EARLY — PARALLEL OVERRIDE (user 11:1xZ): no serialization — both rounds concurrent on deepseek (no cap history)."
- Why it matters: release triggers now span three kinds (pane-freed close-out | close-out + CI green | verdict gate OPEN for a held JOB), held rounds re-verify/refresh sha at release when the head moved, and the user can override serialization on a cap-free provider (deepseek). ×6 sightings.

### C4 — Model-restoration flip-flop: probe evidence is not recovery evidence; even a Gru-confirmed flip-back gets superseded by the user within a minute
- Suggested target: AGENTS.md gotchas → Provider incidents
- Evidence (3 events in 1 minute):
  - righttenantry-refcheck-rc4-1-perkins-r1 2026-08-12T08:38:31Z: "FLIP-BACK CONFIRMED (Gru, 08:47Z): releases on kimi-coding/k3 (model restored). Release discipline: probe kimi first (1-token k3 call) — 200 = release on kimi; 403 = revert to deepseek + release + re-hold the next."
  - righttenantry-refcheck-rc4-1-perkins-r1 2026-08-12T08:39:14Z: "SUPERSEDES flip-back (user override 08:5xZ): kimi probes were a FALSE DAWN — NO recovery. Releases on deepseek/deepseek-v4-flash (model restored). Do NOT flip to k3 until the user EXPLICITLY says so; kimi 200 = unconfirmed (08-11 lesson)."
  - righttenantry-refcheck-rc4-1-perkins-r1 2026-08-12T08:37:38Z: "USER RULING 2026-08-12 (no kimi top-up): held round RELEASES ON deepseek/deepseek-v4-flash (model field updated). Watch: if kimi recovers before release, still deepseek (ruling stands until Silas reports kimi OK)."
- Why it matters: the kimi recovery premise is unreliable mid-cycle (recurring theme); codify: releases stay on deepseek until an EXPLICIT user statement, probe-before-release is the only sanctioned kimi test.

### C5 — Mid-round kimi 403 "light doctrine": zero lens JSONs → same-row recovery via /model deepseek + continue, with explicit mm-launch model flags
- Suggested target: AGENTS.md gotchas → Provider incidents
- Evidence:
  - packet-plumber-v2-harness-ecmp-demo-perkins-r1 2026-08-12T08:35:59Z: "KIMI 403 MID-ROUND (08:29-08:34Z): billing-cycle quota exhausted again (morning top-up consumed by the 3.1 r1 round + fan-out start). Zero lens JSONs landed (setup artifacts only: diff.patch + prompts) — light doctrine. Recovery: 7 dead lens panes closed; /model deepseek/deepseek-v4-flash + continue in pWJ (08:35Z) with explicit mm-launch guidance (pi --model deepseek/deepseek-v4-flash, never bare pi / never glm-5.2). Main pane resumed working on deepseek. Same row (r1, not rN+1); sha f90351da unchanged. Fallback if mm relaunch spawns kimi: sweep + redispatch."
- Why it matters: extends the written 403 doctrine with a middle class — setup-artifacts-only means NO regenerate, NO re-dispatch, in-pane model switch; the fan-out relaunch must pin --model (bare `pi` inherits kimi).

### C6 — Parked-dead is a recoverable state: rework/rebase delivered by relaunching pi in the parked pane; sibling in-flight merges pre-warned at dispatch
- Suggested target: AGENTS.md gotchas (pane forensics) or playbook (dispatch notes)
- Evidence:
  - righttenantry-refcheck-rc4-1 2026-08-12T08:14:26Z: "Pane pVV agent exited post-completion (parked-dead; relaunch on demand for rework)."
  - packet-plumber-v2-3.1-packet-types 2026-08-12T09:15:35Z: "MERGE CONFLICT (09:14:57Z): #28 DIRTY — base v2 moved (#29 merged). pi relaunched in pVT (was parked-dead) + rebase relayed (fetch origin v2 && rebase, resolve, push --force-with-lease; then self-report in-review). Verified in jsonl; pVT working."
  - packet-plumber-v2-3.2-lane-qos 2026-08-12T11:40:38Z: "NOTE: #30 (3.5) APPROVED but UNMERGED — if it merges mid-work, rebase onto the new v2 (LOG_VERSION/command/main.odin overlap)."
- Why it matters: rework after completion and merge-conflict recovery both flow through parked-pane relaunch (session file preserves context); dispatch notes now pre-warn of sibling-PR rebase overlap — a cheap, codifiable standard. ×3 sightings.

### C7 — Fix-audit round contract: prior_findings=consolidated.json, verify every B/W/N + delta pass, carry notes forward, round budget tracked, huge diffs chunked
- Suggested target: playbook (Perkins rounds)
- Evidence:
  - righttenantry-refcheck-rc3-7-perkins-r2 2026-08-11T23:43:14Z: "Fix-audit (prior_findings=r1/consolidated.json; verify B1+W1-W4+N1-N8)."
  - righttenantry-refcheck-rc3-7-perkins-r2 2026-08-12T00:02:08Z: "r2 FIX-AUDIT APPROVED: B1 correctly fixed (stamp overwrite scoped to created_ids + 2 regression tests), W1-W4 + N1-N8 verified (N3 carried), load-bearing invariants hold ... Round budget 2 of 3 used."
  - righttenantry-refcheck-rc3-5-perkins-r2 2026-08-11T16:05:25Z: "r2 APPROVED (0 blockers) — B1+W1-W5 all FIXED + verified; N2 incidental ... 4 new notes + 8 carried."
  - packet-plumber-v2-3.1-packet-types-perkins-r2 2026-08-12T10:00:33Z: "14/14 reviewers (7 lenses x 2 chunks, diff 4620 lines), 11/12 unique confirmed, 1 carry-forward FP, 0 unverified."
- Why it matters: the r2 fix-audit shape is now standardized across repos (verify-each-finding + delta + carry-forward + budget cap); 4620-line diffs get per-lens chunking. ×3 sightings.

### C8 — Lens-loss tolerance: verdicts proceed at 6/7 lenses when one stalls or 429s; recovery via low-concurrency re-wave
- Suggested target: playbook (Perkins rounds)
- Evidence:
  - righttenantry-refcheck-rc3-5-perkins-r2 2026-08-11T16:13:51Z: "6/6 new findings confirmed, 0 rejected; 6/7 lenses — architecture didn't finish, judged sufficient not degraded."
  - righttenantry-refcheck-rc3-5-perkins-r2 2026-08-11T16:05:25Z: "6/7 lenses (architecture stuck >22min, concerns covered)."
  - packet-plumber-v2-1.4-win-lose-stub-perkins-r1 2026-08-11T19:43:27Z: "glm-5.2 7/7 lenses (recovered a 429 + slow-find churn via 2-concurrent re-wave)."
- Why it matters: round completion no longer blocks on a stuck lens — "sufficient not degraded" judgment + staggered 2-concurrent re-wave is the working recovery. ×3 sightings.

### C9 — Pane ids re-scope on workspace moves (w1T: prefix); ledger row corrected at dispatch
- Suggested target: AGENTS.md gotchas (Ledger / pane ids)
- Evidence:
  - packet-plumber-v2-3.5-node-placement 2026-08-12T10:20:01Z: "dispatched: pane w1T:pXK (tab t7N; id re-scoped on workspace move — ledger corrected). Handover verified."
  - righttenantry-refcheck-rc4-2 2026-08-12T10:23:13Z: "dispatched: pane w1T:pXM (tab t7P; id re-scoped on workspace move — ledger corrected). Handover verified."
- Why it matters: new gotcha class — moving a pane to another workspace mutates its pane_id (w1T: scope); the ledger pane_id must be re-captured post-move or the watcher tracks a phantom. ×2 sightings same morning.

### C10 — pr_review "standing bar": repo-level policy decides when Perkins applies; Gru corrects 0→1 at in-review
- Suggested target: playbook (Perkins dispatch) or AGENTS.md gotchas (pr_review key)
- Evidence:
  - packet-plumber-v2-3.5-node-placement 2026-08-12T11:18:16Z: "CORRECTION (Gru 11:1xZ): pr_review 0 -> 1 — the v2 standing bar applies (new command kind + LOG_VERSION bump). Perkins r1 on #30 head 666b082 dispatched; r1 verdict gates the 3.2 release."
- Why it matters: beyond the documented column-vs-note trap, there's now a per-repo standing-bar policy (v2: new command kind or LOG_VERSION bump → Perkins mandatory); catching misses is Gru-correction, not sensor work.

### C11 — External-data gate re-checks: blocked jobs on external publication holds get scheduled re-checks with a dispatch action
- Suggested target: playbook (blocked jobs)
- Evidence:
  - righttenantry-dublin-rents-q2-2026 2026-08-12T07:14:17Z: "GATE RE-CHECK 2026-08-12 (user ruling: FULL HOLD, option B — all in one PR when Daft Q2 2026 lands): Daft.ie Q2 2026 Rental Report NOT yet published ... ACTION: re-check Daft report ~2026-08-19; when live -> bump issue to priority:high per #529 and dispatch."
- Why it matters: blocked-by-external-data jobs get a dated re-check + pre-planned dispatch action, so the hold doesn't evaporate.

### C12 — Briefing-amendment drift: minions catch superseded briefing ACs at dev-story step-01 → lavish clarify (A/A/A), then proceed
- Suggested target: docs/minion-field-notes.md
- Evidence:
  - righttenantry-refcheck-rc3-6 2026-08-11T18:43:56Z: "4 open questions at dev-story step-01 (briefing AC#2 superseded by 2026-08-08 amendment; correction-flow scope; awaiting_correction notification). Presenting in lavish, halting."
  - packet-plumber-v2-3.1-packet-types 2026-08-11T23:59:32Z: "halted with 3 confirm-Qs in lavish (.lavish/pp-v2-3.1-clarify.html) — fixture / SetPiece scope / T2 pixels"
- Why it matters: briefings referencing ACs later amended produce predictable step-01 clarifies — cheap to catch if dispatchers diff briefing ACs against post-date amendments. ×2 sightings.
