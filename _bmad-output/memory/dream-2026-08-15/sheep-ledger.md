# Sheep findings — ledger (dream 2026-08-15)

Window: 2026-08-13T16:26:29Z → 2026-08-15T16:31Z. Source: `bin/ledger events` (full window, 3 dumps) + `ledger show` on 12 key rows + read-only sqlite on `orchestrator.db`. **60 job rows** with activity (41 packet-plumber, 17 RightTenantry, 2 dream).

## Jobs with activity since marker

| Job(s) | Repo | Status | PR | One-line |
|---|---|---|---|---|
| routing-bandwidth-cost (+r1) | PP | done | #37 | Dijkstra routing shipped; r1 APPROVED; 1 connection-error continue (firewall class) |
| routing-forecast-shift (+r1, r2) | PP | done | #39 | CR→rework→r2 APPROVED; CI billing-block noted per round |
| routing-readability-assist (+r1) | PP | done | #40 | r1 APPROVED; self-close note URL truncated (`review-1`) |
| bundle-reprice-pin (+r1) | PP | done | #38 | W1 test-only pin; **minion self-created row, missing fields** (Silas filled) |
| opening-five-min-story | PP | done | #41 | Sophia interactive docs session, pr_review=0, merged |
| v2-4.2-surge-crisis (+r3, r4) | PP | done | #36 | r3 CR at cap → **r4 = user cap override (U1)** → APPROVED |
| hud-warning-overlap-fix (+r1) | PP | done | #42 | mid-job user PAUSE ruling (no transition), then option-C resume; r1 APPROVED |
| v2-4.3-network-health (+r1) | PP | done | #43 | r1 APPROVED; **pr NULL self-report gap — Silas fixed** |
| v2-5.5-demolish-input (+r1, +skip-5c577fa) | PP | done | #44 | r1 APPROVED; canon base-sync head move → **skip-row**, not a round |
| v2-5.6-router-tiers (+r1) | PP | done | #45 | held behind canon 5f51236 landing; r1 APPROVED |
| v2-5.3-pause-anywhere (+r1) | PP | done | #46 | r1 dispatch interrupted by Silas restart → serialize-held, recovered; **pr NULL gap — fixed** |
| v2-5.7-runtime-telemetry (+r1, r2, r3) | PP | done | #47 | 3-round loop CR→CR→APPROVED at cap-3; r2 hit 429/1302 on glm-5.3 |
| v2-5.3-pause-ux (+r1, r2) | PP | done | #49 | r1 APPROVED; r2 (base-merge delta) MOOT on pre-verdict merge |
| v2-5.8-qos-panel (+r1) | PP | done | #50 | clarifying→lavish rulings→APPROVED; self-close URL truncated |
| v2-5.1-map-growth (+r1) | PP | done | #51 | APPROVED; "Main-checkout trap recovered clean" |
| v2-ux-font-resize (+r1) | PP | done | #52 | APPROVED 23/24, merged; pane-watcher echo pre-classified |
| v2-5.2-node-health | PP | **dispatched** | — | queued: pane live, release gated on chain; QUEUE note re visibility job |
| surge-explainer | PP | done | NO-PR | lavish artifact APPROVED by user; mid-flight USER REFRAME relayed |
| terminology-audit | PP | **working** | — | Phase-1 no-PR lavish decision table, waiting on user verdict |
| refcheck-followup-607 (canonical, +r1, r2) | RT | done | #610 | CR→APPROVED; canonical row for the phantom below |
| **refcheck-followup-607 (phantom)** | RT | done | #610 | **minion self-created WRONG id** (dropped repo prefix); duplicate tracked 19h, closed to silence PR watcher |
| refcheck-local-test | RT | done | NO-PR | interactive user session; ~15 settle echoes; RESPAWN-TRIGGER note |
| refcheck-rc4-4 | RT | done | #609 | merged, RC4 series complete (context from before marker) |
| ctr-metadata-619 | RT | done | #620 | copy-only, pr_review=0 human review, merged |
| refcheck-611-panel-persist (+r1, r2) | RT | done | #616 | r1 CR→r2 APPROVED; **first glm-5.3 round** (08-14 13:33Z flip) |
| refcheck-612-emdash-prose (+r1) | RT | done | #614 | r1 MOOT — pre-verdict merge |
| refcheck-613-615 (+r1) | RT | done | #618 | r1 APPROVED; Perkins discarded 2 out-of-scope re-litigations |
| refcheck-verification-rerun | RT | done | NO-PR | 4/4 fixes verified live; respawn of local-test per trigger note |
| refcheck-bughunt2 | RT | done | NO-PR | 1 bug filed #621; user BATCHED ruling recorded as done→done note |
| dream-2026-08-13 / dream-2026-08-15 | root | done / working | — | prior pass closed 16:26:33Z (4s after marker); current pass |

(Round rows folded into parent lines; each rN row itself reached done with a recovered-as-note verdict — **11/11 self-closed verdicts captured, zero lost**.)

## Candidate patterns

### C1 — Standing GitHub-Actions ACCOUNT BILLING block: CI red-looking but not a code failure
- Suggested target: AGENTS.md gotchas (provider-incidents sibling) or playbook 'When Perkins fires'
- Evidence: packet-plumber-routing-readability-assist (2026-08-13T23:51:06Z): "CI #40: NOT a code failure — GitHub Actions BILLING block ('recent account payments have failed / spending limit needs increase'); runner never started…; rerun won't help; escalated to user". Recurs ×6 PRs (#39 00:15Z, #41 00:05Z+00:21Z, #42 01:55Z, #43 02:11Z, #44 07:35Z "standing" — all 08-13/08-14).
- Evidence: routing-forecast-shift-perkins-r2 (2026-08-14T00:13:01Z): "CI-billing caveat: local verification = ground truth" — rounds dispatched anyway.
- Why it matters: a billing block looks like CI-red, which the unstable-target hold keys on — the doctrine that emerged (runner-never-started ≠ red; Perkins verifies locally at the sha; one escalation, then note-only "same billing block") prevented 6 wrongful holds. Not codified anywhere yet.
- ×6 sightings (one incident window).

### C2 — Minion self-created ledger rows: wrong-id phantom + missing-fields flavor
- Suggested target: AGENTS.md gotchas (Pane/ledger-id hygiene section)
- Evidence: refcheck-followup-607 (2026-08-14T13:27:23Z): "DUPLICATE/phantom row — minion self-created with the WRONG id (dropped the righttenantry- prefix) at 18:36:07Z; tracked the job in parallel with righttenantry-refcheck-followup-607 (the canonical row…)… closed to silence the PR watcher."
- Evidence: packet-plumber-bundle-reprice-pin (2026-08-13T23:09:42Z): "row existed (minion self-created 23:09Z, missing fields) — pane/tab/worktree/briefing filled by Silas; pr_review=1 intact."
- Why it matters: codified gotchas cover ORCHESTRATOR hand-typed ids; this is the MINION side creating rows Silas must reconcile (one ran 19h as a duplicate, feeding the PR watcher). Related to codified pane/job-id hygiene but a distinct actor.
- ×2 sightings (same day, both benign only because Silas noticed).

### C3 — `pr` NULL self-report gap persists — including the PP crew that had "started" self-setting
- Already codified (AGENTS.md ledger gotcha, 08-13 addendum: crew-level + Silas verify-and-set). Recurrence only, but note the regression data point.
- Evidence: righttenantry-refcheck-followup-607 (2026-08-13T18:59:52Z): "self-report gap (claimed in-review+pr but row stayed working/NULL) — fixed via set+pr".
- Evidence: packet-plumber-v2-4.3-network-health (2026-08-14T02:09:59Z): "in-review self-reported; pr field NULL (self-report gap) — fixed via ledger pr".
- Evidence: packet-plumber-v2-5.3-pause-anywhere (2026-08-14T13:28:42Z): "pr field NULL (gap) — fixed".
- ×3 sightings this window; the PP crew regressed after the 08-11 "crews self-set it" note — verify-and-set remains the only reliable guard.

### C4 — Dispatch interrupted by orchestrator restart: staged-but-unlaunched row → serialize-hold recovery
- Suggested target: AGENTS.md gotchas (Dispatch & handover) or playbook serialize-hold section
- Evidence: packet-plumber-v2-5.3-pause-anywhere-perkins-r1 (2026-08-14T14:05:34Z): "SERIALIZE-HELD: dispatch incomplete from prior session (row+worktree @ 9ae8612 staged 13:28Z; pane/briefing never launched before the Silas restart 13:58Z). Held behind righttenantry-refcheck-611-panel-persist-perkins-r2 close-out… then write briefing + launch."
- Why it matters: a `dispatched` row does not mean a dispatched minion — a restart between row-add and pane-launch orphans the staging (row + worktree exist, nothing running). Serialize-hold absorbed it cleanly here; worth naming as a recognized failure shape. New flavor of the codified serialize-hold/release-trigger family.
- ×1 sighting (recovered without loss).

### C5 — Durable routing notes on non-working rows (QUEUE / BATCHED / RESPAWN-TRIGGER) to survive context turnover
- Suggested target: docs/orchestration-playbook.md (release-trigger section extension)
- Evidence: packet-plumber-v2-5.2-node-health (2026-08-15T11:05:10Z): "QUEUE (Gru, 08-15): on 5.2 MERGE -> release the VISIBILITY job (user-ordered…)… TENET ON RECORD: 'if players need a manual, the design failed'".
- Evidence: righttenantry-refcheck-bughunt2 (2026-08-15T08:59:57Z): "USER RULING…: issue #621… is BATCHED — NO solo minion. It rides the next RT batch… Routing survives context turnover via this note."
- Evidence: righttenantry-refcheck-local-test (2026-08-14T16:16:11Z): "RESPAWN TRIGGER = PR #618 merged… -> re-run reference_checks scenarios, fresh dispatch" — and it fired: verification-rerun dispatched 08-14T18:55:19Z "RESPAWN of refcheck-local-test (user ruling)".
- Why it matters: release triggers are codified for held Perkins rounds; this window generalizes them to QUEUED jobs, batched user rulings on done rows, and respawn triggers — all executed correctly across context turnover (the respawn fired as written). Codification candidate for the general practice.
- ×3 sightings, one full trigger→fire cycle.

### C6 — Self-close event notes carry truncated review URLs; the recovery note is the URL source of truth
- Suggested target: AGENTS.md gotchas (one-line extension of "Never guess review-URL anchor ids")
- Evidence: packet-plumber-v2-5.8-qos-panel-perkins-r1 (2026-08-15T00:43:19Z): working→done note ends "…pull/50#pullrequestreview-" (anchor cut); recovered note 00:43:58Z carries the real id 4942164141.
- Evidence: packet-plumber-routing-readability-assist-perkins-r1 (2026-08-14T00:16:00Z): "…pull/40#pullrequestreview-1" (mangled anchor); recovered verdict 00:20:31Z has 4932656755.
- Why it matters: anything downstream reading the self-close EVENT (not the recovery note) gets a wrong/broken review URL — same blast radius as a guessed anchor. One line in the existing gotcha covers it.
- ×2 sightings.

### C7 — Perkins mechanics healthy this window (already codified, discipline holding — one line each)
- Self-close = 100% of rounds (11/11), every verdict recovered as a pre-emptive/next-minute note, `set done` no-opped where raced — already codified as the norm (08-07 addendum); zero verdict losses, zero worktree/lens/branch leftovers recorded in events.
- Skip-row for a pure base-sync head move (v2-5.5-demolish-input-perkins-skip-5c577fa, 2026-08-14T09:05:35Z: "round SKIPPED: PURE BASE-SYNC head… PR's own diff unchanged… r1 APPROVED content unchanged") — already codified ('Round-budget ops' skip-row policy); clean instance.
- Cap-3 + U1 user-cap-override (v2-4.2-surge-crisis r4, "minion unaware of the override (per doctrine)"; 5.7 "loop closed at cap-3") — already codified (playbook 'User cap override').
- glm-5.3 reasoning-tier flip (first round righttenantry-refcheck-611-panel-persist-perkins-r2, 2026-08-14T13:33:20Z "**FIRST glm-5.3 round** (launch verified on zai-coding-cn/glm-5.3)") — already codified (playbook model table, user ruling 2026-08-14, supersedes 08-12 v4-pro).
- 429 code 1302 burst on ZAI glm-5.3 mid-round, one continue revived (5.7-r2, 2026-08-14T20:41:14Z: "5th glm-5.3 round today — cumulative usage") — 1302-vs-1308 doctrine already codified (08-13 addendum); NEW data point: the ZAI burst limit binds at ~5 rounds/day cumulative on the reasoning tier — worth one line when next codifying provider limits.
- Connection-error/office-firewall class: ×2 clean one-continue recoveries (4.2-r4 08-13T17:58Z, bandwidth-cost-r1 08-13T22:56Z) — already codified (08-13).
- pr_review column: all 23 code-review jobs carry pr_review=1 (sqlite) — the 08-12 sensor-blindness class did NOT recur; sweep fallback unexercised.

### C8 — Interactive user sessions are a settle-echo firehose (minor)
- Already codified in essence (settle transitions = noise); new flavor worth one line.
- Evidence: righttenantry-refcheck-local-test — ~15 note-only events 08-14T08:05→13:27, e.g. 11:20:53Z "settle echo (working->idle): interactive session turn boundary; no action".
- Why it matters: every user turn in an interactive pane fires the watcher; classification note each time is correct but pure tax — a candidate for watcher-side suppression of interactive-flagged panes.
- ×15 sightings (one session).

## Health summary (for Bob's consolidation)

Two live rows at pass time: `packet-plumber-terminology-audit` (working, lavish verdict pending) and `packet-plumber-v2-5.2-node-health` (dispatched, chain-queued). Strongest new pattern: **C1 (CI billing block ≠ CI red)** — it recurred ×6, forced a doctrine call each time, and is nowhere in the stores.
