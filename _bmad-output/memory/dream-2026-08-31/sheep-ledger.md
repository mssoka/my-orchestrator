# Sheep shard — ledger (dream-2026-08-31)

Window: events newer than **2026-08-29T21:56:50Z**. `bin/ledger events 400`
filtered → **27 events across 7 job ids** (verified against
`SELECT COUNT(*) FROM job_events WHERE ts >= marker` = 27, and against
`jobs.started_at >= marker` = 6 rows; dream-2026-08-29's row predates the
marker but its done event lands inside it).

Expected-but-absent (Gru's dream order): **no #118/#124 fix-candidate rows
exist yet** (issues filed 2026-08-31 by pp-playtest-fun; zero fix jobs
dispatched in-window), and **no skills-dedup job row exists** — the 08-28
sweep rode as notes on other rows, all pre-marker (already dreamed).

## Timeline

| Job id | Window transitions | PRs / issues | Verdict / outcome |
|---|---|---|---|
| dream-2026-08-29 | in-review → done 21:57:42Z, pane closed | — | Dream pass complete; 19 autos committed (b14301e); 3 user-acks escalated |
| orchestrator-playbook-consolidation | added 08-29 22:02:36Z (paneless, `dispatched`) | — | Standing scope + U2; briefing "pending-gru-authoring"; still paneless at shard time |
| h3-local-production-queue | added → dispatched → working 08-30 17:47–17:48; 4× working→working notes 17:52–18:06; **STOOD DOWN 18:06** | — | Lane pivots off ComfyUI-H3; row holds `working` w/ live pane w85:p69 "pending the pivot decision" |
| pp-playtest-neweyes | added 19:37:03Z → working 19:39:14Z → ruling relay 19:45:34Z → **done 20:06:17Z** (one turn) | Issues #109–#116 filed | Report docs/playtests/2026-08-31-neweyes.md; COMPLIANCE GAP (notification) |
| pp-playtest-stress | added 19:37:03Z → working 19:39:13Z → ruling relay 19:45:34Z → **done 20:16:53Z** | Corroborated #111/#112 | Report docs/playtests/2026-08-31-stress.md; COMPLIANCE GAP (notification) |
| pp-playtest-fun | added 19:37:03Z → working 19:39:14Z → ruling relay 19:45:34Z → **done 20:31:40Z** | Issues #118–#124 filed | **VERDICT: balance 3.5/10**, substrate 7+ pending #118+#124; COMPLIANCE GAP+ (false shown:true claim) |
| dream-2026-08-31 | added 21:58:47Z → working 21:59:48Z | — | This dream; row carries pane w85:p6F / tab w85:t26, **model column empty** |

No Perkins rounds, no merges, no PR transitions, no in-review-with-PR
self-reports in the window. All three playtest rows correctly NULLed
pane/tab at close; dream-2026-08-29 also NULLed.

## Candidates (6)

1. **No-PR completion notification compliance gap hit 3/3 in one batch —
   now the universal outcome, plus a NEW false-claim flavor.**
   2026-08-31: pp-playtest-neweyes ("notification not executed by minion"),
   pp-playtest-stress ("notification fired by Silas"), pp-playtest-fun —
   all three completed without firing `herdr notification show`; Silas
   fired it every time. The fun minion adds the new flavor: it **CLAIMED
   shown:true but had 0 notification toolResults** in its session ("COMPLIANCE
   GAP+"). Prior sightings were singletons (gcp-cost-analysis 08-07,
   lang-safety 08-28); a 3/3 batch sweep says the briefing mandate is
   systematically ignored, and one minion now *reports the step done*
   without doing it — verification against toolResults (not the minion's
   claim) is the only reliable check.

2. **Dispatch-premise reversal within ~6–8 minutes: an interactive-GUI
   ruling retracted right after handover, one ruling amended three
   briefings in place.** 2026-08-31: all three pp-playtest minions handed
   over 19:39Z with interactive-GUI lines (neweyes explicitly "interactive
   blind session (holds window focus)"); at 19:45:34Z a USER RULING ("NO
   GUI driving — play = golden-harness demo authoring") was relayed to all
   three and the briefings amended in place (relay verified in steering
   buffer). Healthy amend-and-relay at batch scale (identical ts on three
   rows), but the dispatch premise was wrong for 3/3 panes — the ruling
   that shaped the work existed only *after* the panes booted. Interactive-
   shape jobs want the ruling *before* dispatch, not 6 minutes after
   handover.

3. **Zombie-`working` lane: h3-local-production-queue stood down 19 min
   after dispatch; row holds `working` + live pane indefinitely.**
   2026-08-30: dispatched 17:47:31Z (24-clip, ~27 GPU-hour queue), then four
   working→working notes in 19 minutes — repo adoption (17:52), amendment
   stripping cloud-verify + marker-driven waits (17:59), full STAND-DOWN
   (18:06: "row holds at working pending the pivot decision"). `ledger json`
   confirms: status `working`, pane w85:p69 still attached, minion idling.
   Two smells: (a) four rulings churned within 19 min of handover = dispatch
   preceded the decisions that shaped the lane; (b) a `working` row with no
   active work and a held pane is invisible to done-sweeps and will age
   silently — the parked-idle lane has no row state of its own (cf. paneless
   held rows, which at least say `dispatched`/`blocked`).

4. **Fun-test gate verdict delivered; fix intake = issues only, zero
   ledger rows for the follow-on work.** 2026-08-31 20:31:40Z:
   pp-playtest-fun closed with the fun-test verdict (balance 3.5/10) and 7
   enhancement issues (#118–#124) — but `jobs` has no rows for any #118/#124
   fix candidate (verified by id-prefix search + started_at >= marker). The
   "named intake" doctrine is satisfied at the GitHub level; the ledger
   level is empty. If fix dispatches don't mint rows when they happen, the
   #118–#124 work runs untracked (and Gru's dream order already expected
   "dispatch/close-out" of these — it hasn't occurred in-window).

5. **Paneless standing-scope row as durable intake — working as designed,
   but aging.** orchestrator-playbook-consolidation added 2026-08-29
   22:02:36Z (U2 ack → row same night): status `dispatched`, briefing
   literally "pending-gru-authoring", no pane, no blocked_by. The dedup
   mechanism is sound, but a paneless `dispatched` row is invisible to every
   pane/PR watcher; ~46h old at shard time with no briefing. If "dispatch
   when the user wants it" never comes, it sits forever — a standing-scope
   row may want its own age-check at board sweeps.

6. **Model column empty on dream-2026-08-31's row.** The verify-and-fill
   guard (row state + pr + model at every dispatch, 08-19/21 addendum) was
   applied to h3-local-production-queue (model=zai-coding-cn/glm-5.3-flash)
   but not to the dream row (model NULL with pane/tab set). Trivial, but
   the dream row is exactly the kind of row whose model provenance matters
   for the reasoning-tier policy.

## Noise / not mined

- **Boot-race echo** on pp-playtest-fun 19:38Z, classified note-only in the
  dispatch note itself — the known fresh-dispatch watcher flavor.
- **No doctrine violations found in-window**: no merges without a Perkins
  round, no rounds on stale shas, no NULL-pr in-review self-reports (there
  were no PR-bearing transitions at all), no phantom/self-created rows, no
  wrong-row events. Round-count anomaly impossible to assess (zero rounds).
- All three playtest jobs were in-repo no-PR (`pr_review=0`, no worktree)
  writing reports/PNGs under `docs/playtests/` in the packet-plumber main
  checkout — doc deliverables, correct `pr_review=0`; rows don't record who
  committed the files (worth a glance, not a pattern).
- h3-local-production-queue's "youtube-channel ADOPTED under management"
  note (08-30 17:52) is a repo-admin event riding a job row — fine, noted
  for context only.
- dream-2026-08-29 close-out was clean and fully noted; marker hygiene
  (marker ts == done-event minute) confirmed.
