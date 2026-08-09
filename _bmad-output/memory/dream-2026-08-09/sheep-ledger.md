# sheep-ledger findings — dream-2026-08-09

Marker: 2026-08-07T11:43:30Z. Scanned `ledger events 400` (boundary at
dream-2026-08-07 close) + `ledger show` on 14 jobs + `ledger json`.

## Jobs with post-marker activity (one line each)

35 real rows (excl. dream-2026-08-09 itself, incl. 1 phantom — see P9):

- packet-plumber-sprint-plan-v1 — lavish-gated; user approved via DIRECT PANE CHAT not Send&End (08-07 15:34); PR #4 merged 16:33.
- orchestrator-docs-ua1-ua2 — dream UA1+UA2 docs PR #4 merged 08-07 20:17. Happy path.
- orchestrator-perkins-ops-codify — 3 Perkins-ops patterns codified, PR #5 merged 08-07 20:32. Happy path.
- righttenantry-per-applicant-remind (+perkins r1/r2) — r1 APPROVED 4W → W1/W3 fold-in → r2 APPROVED; PR #586 merged 08-07 20:32. Perkins DOUBLE-POSTED identical APPROVED reviews (18:47 note, benign).
- packet-plumber-prototype-build (+perkins r1) — PR #11 merged 08-08 17:58; Perkins r1 CHANGES_REQUESTED landed 18:06 POST-MERGE; FYI close-out 08-09 07:16 (3B incl. 2 headless-reproduced bugs; findings routed to Odin prototype + foundation-audit, no rework).
- packet-plumber-foundation-audit — RECALLED before launch 08-08 15:18: dispatched off origin/main with NO game code (prototype stranded on local branch). 17 min alive. Re-dispatch precondition (#11 merged) now MET — no re-dispatch row exists post-marker. DROPPED-THREAD RISK.
- righttenantry-refcheck-ad5-amend / ad6-stoplink-amend — chained arch-doc amendments (#592, #593), rebase conflict resolved cleanly. Happy path.
- righttenantry-refcheck-rc2-3 (+perkins r1/r2) — r1 CHANGES_REQUESTED (B1 = test gate, zero HTTP/e2e coverage of headline AC) → fix → r2 APPROVED; #591 merged 08-08 20:01.
- righttenantry-refcheck-rc2-2 (+perkins r1/r2/r3) — 3-round arc: leaderboard viewed-arm → CI FORMAT GATE → APPROVED; #590 merged 08-08 09:26. Also user manual→dev-auto→manual flip killed minion w1T:pF1 (00:07→00:09).
- packet-plumber-prototype-iterate-1 — PR #12 merged 08-08 20:01; note: macOS offscreen windows freeze compositor → movie-mode captures used.
- packet-plumber-blender-art — churn: BlenderMCP :9876 died on read_factory_settings (blocked 23:56) → user DIRECTION CHANGE blocked 00:24 (abstract→literal buildings, reopens FORGE #5) → LIGHT-canvas lavish verdict 00:53 → 2 PR feedback rounds → #9 merged 08-08 10:10.
- packet-plumber-art-direction / art-direction-amend / light-cascade / narrative-messaging — canon docs (#7/#8/#10/#5), lavish-gated, all merged. Happy path; light-cascade = the cascade job from the blender-art LIGHT verdict (3 canon docs reconciled).
- packet-plumber-odin-vs-godot-lavish — lavish verdict 08-08 20:37 REVERSED the locked Godot engine choice ("move to Odin, own it end-to-end"); escalated, not executed by minion; #13 merged.
- packet-plumber-odin-architecture — KILLED mid-lavish 08-08 23:19 (user MODEL OVERRIDE deepseek→kimi, draft discarded, ~1h glm wall hold) → SAME ROW resurrected done→dispatched 23:26 → kimi draft + 2-hunter swarm → #15 merged 08-09 00:41.
- packet-plumber-port-limits-canon / forge6-desktop-first-amend — Odin-pivot follow-on canon (#14, #16). Happy path.
- righttenantry-refcheck-rc3-1 (+perkins r1) — r1 APPROVED 0B; #594 merged 08-08 23:36. Sensor echo note: Perkins left the round row at 'working' — Silas closed manually.
- righttenantry-refcheck-rc3-2 (+perkins r1) — r1 APPROVED via FALLBACK-COMMENT (token-mint shell $? bug); #595 merged 08-09 09:07.
- righttenantryagents-model-flash — done→done note 08-08 23:36: staging behavioral gate resolved; N2/N3 follow-ups still tracked.
- packet-plumber-odin-prototype — in flight (dispatched 08-09 00:50; harness goldens 6/6 green 10:41).
- righttenantry-refcheck-rc3-3 — in flight (dispatched 08-09 09:12).

## Candidate patterns

### P1. User mid-flight overrides (process/direction/model/engine) kill in-flight minions; each reversal spawns a canon-cascade job
- Sightings: righttenantry-refcheck-rc2-2 (08-08 00:07→00:09) — "switched manual -> bmad-dev-auto per user… REVERTED: user 2nd thought… original minion w1T:pF1 was killed in the switch attempt" (84s flip).
- packet-plumber-blender-art (08-08 00:24) — "DIRECTION CHANGE (user): wants literal beautiful building art… Re-opens art-direction v1 S6 + possibly [FORGE #5] 'no realism'".
- packet-plumber-odin-architecture (08-08 23:19) — "KILLED for kimi re-dispatch (user MODEL OVERRIDE)… deepseek draft discarded. ~1h hold accepted."
- packet-plumber-odin-vs-godot-lavish (08-08 20:37) — lavish verdict "let's move to Odin" reverses the LOCKED Godot choice → re-plan intake.
- Cascades observed: LIGHT verdict → packet-plumber-light-cascade (3 canon docs); buildings → art-direction-amend; Odin → odin-architecture + forge6-desktop-first-amend + port-limits inheritance notes.
- Why it matters: 4 reversals in 2 days, each killing or blocking work and each requiring a reconciliation job; lavish gates are where locked decisions actually get decided — locks ("FORGE #5", engine choice) are provisional until the lavish verdict lands.
- Already in memory? No. (Lavish gating is documented as flow; reversal→cascade as a recurring cost is not.)

### P2. Perkins late-round blockers are PROCESS gates, not logic — minions don't run CI gates locally pre-push
- Sightings: rc2-2-perkins-r2 (08-08 07:22) — "B1 = CI format gate FAILS… 'gleam format --check' fails; PR can't merge" (4-lens agreement).
- rc2-3-perkins-r1 (08-08 16:00) — "B1 = advisory test gate FAIL: headline AC… has no automated pin; 3 HTTP handlers + trigger dispatcher ZERO direct test coverage".
- per-applicant-remind-perkins-r1 (08-07 18:45) — "W4 advisory test-gate CONCERNS (P1 ~87.5%)".
- Why it matters: 3 different jobs, 2 days, same class — a burned Perkins round each time on something a pre-PR checklist (format --check + gate self-check) catches for free.
- Already in memory? No.

### P3. Perkins arcs are SHORTENING as codified ops bed in (3→2→1 rounds); proactive dispatch + fix-audit is the stable shape
- Sightings: rc2-2 = 3 rounds (08-08); rc2-3 = 2 rounds (08-08); per-applicant-remind = r1 APPROVED+fold-in+r2 (08-07); rc3-1, rc3-2 = single-round APPROVED (08-08/09).
- rc2-2-perkins-r3 note (08-08 08:22): "r3 was dispatched PROACTIVELY at ~07:29Z per round-budget ops… round row + full sha written before this tick."
- Why it matters: the 08-07 codified patterns (default-armed, fold-in r2, fresh-session board-check — orchestrator-perkins-ops-codify PR #5) show measurable effect within a day; every round closes with an explicit fix-audit of the prior round's B/W items.
- Already in memory? Partially: serialize-hold/pre-created round row gotcha (08-07); the convergence trend + fold-in effectiveness is new evidence.

### P4. Pre-verdict merges recur — FYI verdicts on merged shas find REAL bugs and need an explicit routing target
- Sightings: packet-plumber-prototype-build-perkins-r1 (merged 08-08 17:58, verdict 18:06, FYI close-out 08-09 07:16) — "46 findings (3 blockers…), 62/63 verified, 2 reproduced headless (ghost-pipe demolish bug, ADR-11 replay divergence). NO rework loop… findings feed the Odin prototype + the foundation-audit."
- righttenantryagents-model-flash (08-07 07:16 + 08-08 23:36) — merged as-is, N1–N4 tracked, staging behavioral gate closed a day later, N2/N3 still open.
- Why it matters: first two clean sightings of the 08-07 "moot on merge" doctrine; FYI rounds reproduce real bugs headless — high value, but only because findings were explicitly routed to named follow-ups. Without a named intake they evaporate.
- Already in memory? Partially: "Moot on merge" gotcha (2026-08-07) states the doctrine; these are confirming sightings + the routing-target requirement.

### P5. Sensor stale echoes continue at steady rate — note-only, never re-act
- Sightings: packet-plumber-gdd-v1 (08-07 00:25), packet-plumber-narrative-messaging (08-07 20:59), per-applicant-remind (08-07 18:47), rc2-2-perkins-r3 (08-08 08:22), rc3-1 (08-08 21:00) — all "already closed out / no second action".
- Why it matters: 5 sightings across 3 days; the dedup doctrine (round row + note at dispatch minute) holds — every echo was answered note-only, zero double actions.
- Already in memory? Yes (2026-08-01/02 echo gotcha) — durability confirmation only.

### P6. Perkins self-close is NOT uniform: pane can close with the round row left at 'working'
- Sightings: righttenantry-refcheck-rc3-1 (08-08 21:00 note) — "the r1 round APPROVED verdict was ALREADY closed out… (the round row was left at 'working' by this Perkins -> I set done + clear-pane…)".
- Why it matters: the 08-07 addendum says self-close is the NORM (10/10) — this is a counter-sighting; row state at pane close is inconsistent, so close-out must VERIFY the row, not assume either way.
- Already in memory? Partially: refine the self-close gotcha (both flavors now sighted).

### P7. Token-mint failure has a recurring named cause: shell $? bug → fallback-comment
- Sightings: rc3-2-perkins-r1 (08-09 00:36 + 07:16) — "Token-mint hiccup (shell $? bug) -> fallback-comment not formal approve."
- Why it matters: fallback works, but APPROVED-by-comment ≠ formal approve (branch protection / review-count semantics differ); the $? bug is fixable — worth a minion task on the Perkins tooling, not just tolerance.
- Already in memory? Partially: existing gotcha covers "token mint fails → fallback-comment automatically"; the shell-$? root cause is new.

### P8. Ledger row resurrection: done → dispatched reuses one row for kill + re-dispatch
- Sightings: packet-plumber-odin-architecture (08-08 23:19 working→done "KILLED", 23:26 dispatched→working same row; worktree renamed …/odin-architecture-kimi).
- Why it matters: the killed deepseek attempt and the kimi run share one event log — forensics blur (status went done→dispatched, which the same-status guard doesn't forbid); a fresh row per re-dispatch keeps rounds auditable.
- Already in memory? No.

### P9. Phantom job id in the event stream
- Sightings: 08-09 07:14:44 event for "perkins-packet-plumber-prototype-build-r1 — pane closed"; `ledger show` → "no such job". Real row is packet-plumber-prototype-build-perkins-r1 (closed 07:16). Job-id variant of the 08-08 pane-id typo pattern (hand-typed id, later corrected).
- Why it matters: event stream retains the wrong id forever; id-from-output piping (never retype) applies to job ids too.
- Already in memory? Partially: 2026-08-08 pane-id gotcha — extend to job ids.

## Singletons (interesting but seen once)

- **S1 Dispatch-dependency violation / dropped thread**: packet-plumber-foundation-audit RECALLED 08-08 15:18 ("dispatched off origin/main which has NO game code… Re-dispatch AFTER the prototype game-code PR merges"). PR #11 merged 08-08 17:58 and the FYI verdict (08-09 07:16) explicitly routes findings to "the foundation-audit" — but NO re-dispatch row exists post-marker. Precondition met, thread dropped. Flag to Bob/Gru.
- **S2 Out-of-band approval via direct pane chat**: sprint-plan-v1 (08-07 15:34) — "APPROVED by user via direct pane chat… not lavish Send&End. Out-of-band per field-note protocol but provenance unambiguous." New flavor beyond the lavish state.json provenance notes (memory lines ~218–228 cover stale lavish verdicts, not pane-chat approvals).
- **S3 BlenderMCP infra**: bpy.ops.wm.read_factory_settings reloads the addon and kills its :9876 listener (blender-art 08-07 23:56); recovery = user restarts the server thread; minion rebuilt "without factory reset" after.
- **S4 macOS capture quirk**: "macOS offscreen windows freeze their compositor" → movie-mode captures as the workaround (prototype-iterate-1 08-08 19:41).
- **S5 Perkins double-post**: 2 identical APPROVED reviews, same sha/content (per-applicant-remind 08-07 18:47) — "benign, likely a retry"; flagged, not investigated.

## Churned jobs worth a transcript look (if any pane might still exist)

All listed panes are closed (pane-closed events present); transcripts would be
in each worktree's session dir if retained:

1. **packet-plumber-blender-art** — richest churn: infra block + user direction reversal + lavish verdict cascade + 2 PR feedback rounds. Worktree: ~/.herdr/worktrees/packet-plumber/packet-plumber-blender-art.
2. **packet-plumber-odin-architecture** — kill + row resurrection + model override mechanics. Worktree: ~/.herdr/worktrees/packet-plumber/odin-architecture-kimi.
3. **righttenantry-refcheck-rc2-2** — the 84s dev-auto flip that killed w1T:pF1 (how the switch/revert was executed).
4. **packet-plumber-foundation-audit** — 17-min recalled dispatch (what the minion saw before the hold).
