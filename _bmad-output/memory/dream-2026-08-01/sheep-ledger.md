# Sheep findings — ledger events (since 2026-07-30T00:34:49Z)

Source: `bin/ledger events 200` (full coverage of the window; oldest returned
events predate the marker by ~6 days). Jobs active in-window:
form-completion-ps, form-funnel-w0 (+perkins-r1/r2), refcheck-rc1-1
(+perkins-r1), refcheck-rc2-1 (+perkins-r1), refcheck-v1-epics,
refcheck-v1-sprint-plan, refcheck-v1-{architecture,ux,pitch} close-outs,
finlit-{game-brief,prototype,visual-mock,bugfix-event-messages,
tutor-economy-fix}, kids-finlit-game-brainstorm close-out, dream-2026-08-01.

## Candidate patterns

### Lavish in-browser review is the standing pre-PR gate for docs — and it produces real rulings [STRONG]
- Evidence: finlit-game-brief, 2026-07-31T15:11:27Z: "lavish review done — 1 annotation round landed: OQ3 RULED — LLM tutor = child-initiated '?' help button"
- Evidence: righttenantry-refcheck-v1-ux, 2026-07-30T01:12:24Z: "lavish review complete — 2 feedback rounds applied + pushed to PR #550 … ALL 11 open questions decided and locked into §15"
- Evidence: righttenantry-refcheck-v1-epics, 2026-07-31T19:33:34Z: "lavish review COMPLETE — user reviewed, 'looks good.', Send & End, ZERO annotations"
- Evidence: finlit-game-brief + righttenantry-refcheck-v1-epics, 2026-07-31T10:28:06Z: "user requested lavish review NOW (retroactive per new standing policy)" — the policy's birth event, applied retroactively to already-open PRs
- Evidence: righttenantry-form-completion-ps, 2026-07-31T15:59:23Z: "evidence gathered; 8 numbered questions served via lavish" — clarify questions also flow through lavish
- Class hint: convention

### Perkins automated review loop catches real blockers; rework → re-review closes within hours [STRONG]
- Evidence: righttenantry-form-funnel-w0-perkins-r1, 2026-08-01T01:55:31Z: "CHANGES_REQUESTED (round 1): 1 blocker (security-definer view inbound_email_sender_state bypasses RLS — anon key can read per-vacancy enquirer emails), 9 warnings, 15 notes — 28/29 verified"
- Evidence: righttenantry-form-funnel-w0, 2026-08-01T09:54:38Z: "Perkins r1 rework complete (sha 7bb5824): blocker fixed (view recreated security_invoker=on + REVOKE FROM anon/authenticated…) all 9 warnings addressed … Perkins r2 re-reviewing"
- Evidence: righttenantry-refcheck-rc1-1-perkins-r1, 2026-08-01T01:21:23Z: "APPROVED (round 1): 0 blockers, 2 warnings, 8 notes — 16/16 verified, 7/7 lenses"
- Evidence: righttenantry-refcheck-rc2-1-perkins-r1, 2026-08-01T00:48:27Z: "APPROVED (round 1): 0 blockers, 3 warnings, 7 notes — 13/13 verified, 7/7 lenses"
- Class hint: process

### Perkins "BANKED / FOLD INTO FUTURE BRIEFINGS" items are systematically recycled into downstream work [STRONG]
- Evidence: righttenantry-refcheck-rc2-1, 2026-08-01T00:51:35Z: "FOLD INTO FUTURE BRIEFINGS: (1) RC2.3 — A6 re-enable (skipped→queued) must restore next_attempt_at=now() (update_reference_call_status.sql:12 ELSE preserves NULL; 3 lenses agreed)"
- Evidence: righttenantry-refcheck-rc1-1, 2026-08-01T01:24:18Z: "BANKED: (1) deploy gate stands — nothing past develop before RC1.2 … (2) XFF trust note (security lens): client_ip first-hop comment wrong under Cloudflare"
- Class hint: process

### Deploy gates + counsel flags travel as explicit risk-class signals in ledger notes and PR text [STRONG]
- Evidence: righttenantry-refcheck-rc1-1, 2026-07-31T22:14:33Z: "FLAG: choice now mandatory server-side — safe on develop, do NOT merge to staging before RC1.2 (radio UI)"
- Evidence: righttenantry-refcheck-rc2-1, 2026-07-31T22:15:49Z: "Flag for counsel/RC5.2: objection log has no application_id index (contract-literal §4.1) — DPC lookup would seq-scan"
- Evidence: righttenantry-refcheck-rc2-1, 2026-08-01T00:51:35Z: "Counsel flag already noted (objection log app_id index) for RC5.2" — flag persists across events/days
- Class hint: process

### Test pins + contract-literal acceptance criteria as durable regression guards [STRONG]
- Evidence: righttenantry-refcheck-rc2-1, 2026-07-31T22:15:49Z: "Tests 1092 server/93 shared/438 client/329 integration incl. 8 durable DB-level AC pins"
- Evidence: righttenantry-form-funnel-w0, 2026-08-01T09:51:40Z: "tags/subject + section-ids + clear-window + outcome-wiring test pins"
- Evidence: finlit-tutor-economy-fix, 2026-08-01T01:42:27Z: "LOAN_MODEL OPM contract pinned. 241/241 tests"
- Evidence: finlit-bugfix-event-messages, 2026-07-31T20:32:24Z: "201/201 tests (+38 regression, verified RED pre-fix)"
- Class hint: convention

### Root-cause-first bugfixing, with the wrong hypothesis explicitly named and rejected [STRONG]
- Evidence: finlit-bugfix-event-messages, 2026-07-31T20:32:24Z: "Bug 1 root cause: _tick_remaining inferred INT from TICK_SECONDS:=60, -= delta truncated to -1s/frame → '60s tick' fired every ~60 frames"
- Evidence: finlit-tutor-economy-fix, 2026-08-01T01:42:27Z: "truncation root cause: CLIENT-side 80-word trim guillotined mid-word (finish_reason was 'stop' — NOT max_tokens/thinking)"
- Class hint: convention

### Pre-PR review swarms (mega-minions) are routine, with findings counts reported [STRONG]
- Evidence: finlit-game-brief, 2026-07-31T09:45:14Z: "adversarial review pass (26 findings, 24 applied)"
- Evidence: finlit-prototype, 2026-07-31T18:30:00Z: "Review swarm fixed popup soft-lock + ~20 patches"
- Evidence: finlit-bugfix-event-messages, 2026-07-31T20:31:15Z: "both bugs root-caused+fixed, 201/0 green, 3-hunter review pass"
- Evidence: righttenantry-form-funnel-w0, 2026-07-31T21:44:13Z: "2 adversarial rounds"
- Class hint: process

### gru.ts startup checklist misfires into non-Gru pi panes rooted at /Users/moses/code [STRONG]
- Evidence: dream-2026-08-01, 2026-08-01T10:06:10Z: "handover received in-pane (startup checklist misfired here first)"
- Evidence (second sighting, this reader): sheep-ledger's own pane, 2026-08-01 ~10:12Z — the Gru startup checklist was auto-injected into this non-Gru pane (cwd /Users/moses/code); the user had to send a "you are NOT Gru … it is not meant for you" override before the brief could run
- Class hint: tooling trap

### User engages directly in minion panes — clarify answers and mid-flight scope amendments land in-pane, no Gru relay [STRONG]
- Evidence: righttenantry-form-completion-ps, 2026-07-31T16:14:00Z: "user engaged directly in-pane — minion posted 8 session questions in lavish … No Gru relay needed"
- Evidence: righttenantry-form-completion-ps, 2026-07-31T18:55:51Z: "user sub-question in-pane ('we dont need JS for this?') answered by minion"
- Evidence: finlit-prototype, 2026-07-31T17:10:26Z: "user scope amendment — real LLM behind tutor.gd seam (DeepSeek deepseek-v4-flash…) Relayed + delivered in-pane"
- Evidence: righttenantry-refcheck-v1-epics, 2026-07-31T08:56:06Z: "clarify answered (all recs accepted) + trigger moved shortlist->viewed per user 2026-07-31" — mid-flight amendment absorbed as A5
- Class hint: interaction

### Merge rhythm: PRs accumulate "Awaiting human merge", the human merges in bursts, close-out completes same day [STRONG]
- Evidence: 2026-07-30T01:23:50Z: three simultaneous done transitions — "PR #550 merged", "PR #551 merged", "PR #552 merged" (refcheck v1 design trio)
- Evidence: 2026-07-31 burst: seven merged-and-done transitions in one day — finlit PRs #1 (16:21:37Z), #2 (18:46:29Z), #3 (20:36:32Z), #4 (21:01:28Z); RightTenantry PRs #554 (19:06:27Z), #553 (19:36:40Z), #555 (21:11:43Z)
- Class hint: process

### Parallel jobs on one repo coordinate merge order via PR notes + keep-both rebase doctrine [STRONG]
- Evidence: finlit-visual-mock, 2026-07-31T20:26:08Z: "Merge-dance note: its chip restyle incidentally fixes top-bar contrast (bugfix owns it) — recommend bugfix rebases onto mock branch"
- Evidence: finlit-bugfix-event-messages, 2026-07-31T20:50:48Z: "rebase onto merged mock (PR #3) DONE — conflicts in street.gd (3 hunks) + deferred-work resolved per keep-both doctrine: theme is now the single color source … Force-pushed 459cd28 — MERGEABLE/CLEAN"
- Class hint: process

### Visual evidence convention for taste-checks: before/after captures, windowed rig when headless can't render [STRONG]
- Evidence: finlit-visual-mock, 2026-07-31T20:26:08Z: "before/after capture pairs in docs/visual-mock/"
- Evidence: finlit-bugfix-event-messages, 2026-07-31T20:32:24Z: "Windowed capture rig (headless has no renderer)"
- Evidence: finlit-visual-mock, 2026-07-31T20:36:32Z: "before/after captures in docs/visual-mock/ — art-direction evidence for Moses"
- Class hint: convention

## Anecdotes (single sightings)

- righttenantry-form-funnel-w0, 2026-08-01T09:54:38Z: "Minion pi crashed 02:01 mid-rework, revived by Gru nudge" — pi process death mid-job; manual Gru revival (resonates with the known dead-pi gotcha).
- righttenantry-refcheck-rc2-1, 2026-07-31T22:21:19Z: "CI red→green — minion had formatted server but not shared/; fix d340be2 (gleam format shared)" — repo-wide format check, not just the touched package.
- righttenantry-refcheck-v1-epics, 2026-07-31T19:33:34Z: "Field-notes shard updated with the working marked --gfm -o file-write recipe (confirms pipe-truncation trap)" — lavish pipe-buffer trap already promoted to a shard.
- righttenantry-refcheck-rc1-1, 2026-07-31T22:14:33Z: "Test DB left running :54323 for review rounds" — intentional, but a stale-resource risk if the job dies.
- finlit-tutor-economy-fix, 2026-08-01T01:42:27Z: "OPEN for user: save schema v1→v2 resets Debug Street save (ratify?); frozen-matrix ellipsis row superseded (ratify?)" — ratify-questions embedded in PR notes for the human.
- righttenantry-form-completion-ps, 2026-07-31T16:14:00Z: "user delivered funnel report via 'Herald' agent (/Users/moses/Downloads/apply-funnel-888a-2026-07-31.html — PostHog EU…)" — external data handoff lands in ~/Downloads, outside any repo.
- righttenantry-refcheck-v1-epics, 2026-07-31T19:38:41Z: "user priority call — refcheck BUILD paused … Focus: application-form completion work" — then RC1.1 ∥ RC2.1 dispatched 2026-07-31T21:14:08Z, ~1.5h later. Priority oscillation inside a single day.
- righttenantry-dublin-rents-q2-2026: zero events in-window; blocked since 2026-07-22 awaiting the external Daft.ie Q2 report — stale watch item (10 days frozen).
