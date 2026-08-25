# sheep-ledger-events — dream-2026-08-17

Source: `bin/ledger events 500`, filtered to events newer than the
last-dream marker `2026-08-15T17:01:46Z` → **272 events across 33 job ids**
(15 minion/dream rows + 18 Perkins round rows), plus `ledger show` on every
active id. Window: 2026-08-15T17:04Z → 2026-08-17T17:13Z. All packet-plumber
v2 work (PRs #53–#62), 2 RightTenantry jobs (PRs #623/#624), dream rows.

---

## 1. Billing-block CI noise: standing ruling held across ~15 alerts, 8+ jobs — classification signature is stable

The 08-16 ruling ("billing no longer gates merges; local suite = ground truth")
was applied uniformly all window. Every recurrence handled note-only with the
SAME classification signature: run fails in 3–5s, runner never started, no
logs, annotation "account payments failed / spending limit".

- packet-plumber-v2-5.5-demolish-input, 2026-08-17T08:44Z: "CI alert 08:43Z on
  #59 = billing-block recurrence on sha 55d1b66 (run 32011353765 fails in 5s,
  runner never started) — note-only per 08-16 ruling; local suite = ground
  truth (minion: 9/9)."
- Recurrences (2+ jobs = STRONG): #55 terminology (08-16 10:04Z), #56
  visibility (×3), #57 5.4 (×4), #58 local-ci (×2), #60 7.2 (×5, incl. 3
  doc-only shas), #61 doctrine, #62 5.9, RT #623 + #624 ("account-wide since
  ~09:13Z", develop baseline failing same).
- Sub-pattern: ONE escalation per incident, then note-only — "No rerun
  (useless on this class), no relay, no re-escalation — one escalation already
  sent" (v2-visibility 08-16 10:07Z).
- Counter-example that the reflex must stay classification-based, not
  blanket: 5.2-node-health had a REAL CI red pre-billing (see §9). The
  signature check (runner never started vs golden diff bundles) is what
  separates them.

## 2. NEW: billing-boundary misdiagnosis — Perkins is LOCAL, billing blocks GH Actions only

Both a minion AND Silas briefly concluded the billing block had stopped
Perkins. Self-corrected in ~2 min, but the confusion reached an escalation +
PR comment first.

- packet-plumber-full-game-doctrine, 2026-08-17T10:03Z: "the minion's 10:01
  notification claimed 'BLOCKER: billing likely blocking Perkins review' —
  MISDIAGNOSIS: Perkins r1 has been live on #61 since 09:44 (pane w1T:p1Z5,
  kimi k3, local — the GitHub billing block affects GH Actions runners only,
  not Perkins)."
- Same job, 10:03:50Z, Silas correcting his own 10:01 note: "my
  Perkins-blocked-by-billing call was a misdiagnosis — Perkins r1 IS live on
  #61… Billing blocks GH Actions runners (CI) only; Perkins unaffected."
- Lesson: incident context bleeds across boundaries. Under a GH-wide outage,
  verify which substrate a process actually rides (Perkins = local pi panes)
  before declaring it blocked — and expect MINIONS to misdiagnose this too
  (their notifications feed Silas' first take).

## 3. NEW class: GitHub platform incident (08-17 13:40Z) — proactive advisory fan-out, "retry beats alert", no holds

A real GitHub-side outage (distinct from billing AND from model-provider
incidents). Gru fanned one advisory to every in-flight pane pre-classifying
the expected noise.

- packet-plumber-v2-7.2-audio-juice, 2026-08-17T15:17Z: "ADVISORY (Gru,
  15:15Z): GitHub incident live since 13:40Z — API/PRs/Issues/Actions MAJOR
  outage, webhooks partial, ~20% web+API error rate; GIT GREEN. API flakes /
  sensor gaps / webhook lag = incident noise (retry beats alert); Perkins
  local verification unaffected; merges stay user-side with retry guidance.
  No holds."
- Recurrence: identical advisory written to 3 job rows in the same minute
  (7.1-visual-juice, 7.2-audio-juice, full-game-doctrine — 15:17:03Z ×3).
  Pattern: ONE advisory fanned to ALL in-flight jobs, then a follow-up
  classification on the next alert ("merge retries may lag webhooks",
  7.2 15:20Z).

## 4. Perkins sensor stale-echo: two dedup flavors, both handled — NEW same-sha-APPROVED flavor codified

Known echo class, but the window codified a second flavor: the sensor
re-firing on an ALREADY-APPROVED sha.

- Flavor A (dispatch race, known): packet-plumber-v2-7.2-audio-juice,
  2026-08-17T09:39Z: "Perkins-sensor echo @ 09:38Z (dispatch-round-2 on
  1b96bea) = the sensor racing my dispatch — r2 ALREADY LIVE on this exact
  sha… No double dispatch." (sha-in-row-note dedup).
- Flavor B (same-sha APPROVED re-fire, NEW ruling): v2-5.5-demolish-input,
  2026-08-17T09:13Z: "Perkins-sensor re-fire @ 09:13Z on 55d1b66 = STALE
  ECHO — r1 ALREADY APPROVED this exact sha… No round 2 dispatch (no-op
  re-review of an approved head). A NEW sha would legitimately earn r2 per
  the loop ruling."
- Recurrence (STRONG, 8+ jobs): 5.9 ("Sensor round-2 echo @ 2314a22 = stale
  (same-sha APPROVED) — no dispatch", 08-17 17:13Z), traffic-model r3
  (08-16 01:24Z), doctrine (08-17 10:23Z), plus review-sensor verdict echoes
  on #56, #57, #58, #61, #623, #624 — all "already relayed… no double
  escalation".

## 5. Doctrine shift mid-window: Perkins cap-3 → CAP-LIFTED loop-until-APPROVED (user ruling 08-17)

The window contains BOTH regimes. 5.4 exhausted the old cap ("Cap 3/3 spent —
human takes over", 08-17 00:53Z), the user lifted it 5 min later, and every
subsequent dispatch ran uncapped.

- packet-plumber-v2-5.4-input-parity, 2026-08-17T00:58Z: "USER RULING…:
  Perkins CAP LIFTED for this job — keep running rounds until APPROVED. Loop:
  minion pushes r3-blocker fix → #57 head stable (stability gate: settled
  head + local suite green + minion done iterating; CI = billing block, not
  a gate) → dispatch r4 fix-audit on the fresh sha (prior_findings=r3) →
  repeat until APPROVED."
- Recurrence (STRONG): cap-lift carried into 5.5 redispatch ("cap-3 lifted —
  rounds run UNTIL APPROVED", 08-17 08:11Z), 7.2 r1+r2, 5.9 r1, doctrine r1.
  traffic-model-design finished under the OLD regime ("3 Perkins rounds,
  cap-3 clean", 08-16 08:48Z) — the contrast pair.
- Sub-pattern: fix-audit rounds keep finding DELTA-INTRODUCED blockers —
  iteration is the norm, not failure. 5.4: r1 2B → r2 "fix delta introduced 2
  new same-frame parity deltas" (08-16 23:05Z) → r3 "1 delta-introduced
  blocker (Press_Anchor chord swallow reset on ESC frames)" (08-17 00:52Z) →
  r4 APPROVED 0B. Each round carries prior_findings=rN/consolidated.json and
  mutation-proves the prior blocker fixed.

## 6. NEW mechanic: doc-only head churn under an in-flight round → skip-row decision recorded at close-out

Three superseding user asset-contract rulings pushed 3 doc-only commits while
7.2's r1 was reviewing 84b46cc. Silas' rule: doc-only heads get NO round.

- packet-plumber-v2-7.2-audio-juice, 2026-08-17T08:48Z: "Head moved under
  in-flight r1 (reviewing 84b46cc). Skip-row decision for 517a13a at r1
  close-out: doc-only no-op → skip-row if APPROVED (the #585 precedent);
  superseded by the fix push if CHANGES_REQUESTED." Doc trail 517a13a →
  7482fb4 → adfcb19, each verified "DOC-ONLY… byte-level".
- Close-out executed as written, 09:29Z: "r2 will fire on the FIX sha — the
  doc-only head adfcb19 gets NO round (sensor echo classified; skip per the
  08:48Z note decision)."
- Note the sensor interplay: each doc-only push ALSO fired a billing-block CI
  alert (08:48, 08:58, 09:03Z) — two noise classes stacking on one push.

## 7. NEW: watcher idle alerts on lavish-wait states + long-poll aborts; state.json is the verdict ground truth

Minions parked in lavish user-feedback loops generate working→idle alerts
that look like stalls. Two jobs, plus a poll-abort timeout trap.

- packet-plumber-v2-7.1-visual-juice, 2026-08-17T15:15Z: "pane-watcher
  working→idle @ 15:15Z = lavish-loop WAIT state (expected): … long-polls
  lavish-axi for the user's artifact annotations… Pi alive + idle while
  polling. No status change, no escalation — user-driven review loop."
- Poll-abort trap (2 jobs = recurrence): 7.1 08-17 14:27Z "the minion's
  102-min artifact poll was aborted ('Operation aborted' — wake-callback path
  not yet live)"; terminology-audit 08-15 20:22Z "Poll aborted @~64min (no
  annotations), minion re-polling (prompts: 0)".
- Ground-truth recovery: terminology-audit 08-15 23:31Z — "SILAS
  GROUND-TRUTH…: verified the verdict WAS queued — lavish state.json session
  36b4f1ff33e248bd status=ended (ended_by user), 4 pending prompts; the
  minion's earlier poll died on a harness timeout BEFORE collecting
  (prompts:0 was stale)." → poll output lies after an abort; read
  state.json.
- Sibling: user verdicts also arrive via DIRECT PANE CHAT, bypassing the
  artifact — traffic-model 08-16 00:08Z "'proceed'… Lavish gate passed
  out-of-band; provenance unambiguous (user in minion pane)" (also
  terminology Phase 1 "'proceed' via pane chat").

## 8. Serialize-holds extended: 6-deep Perkins chain (08-16) + HELD minion dispatch with merge-close-out release (08-17)

Known Perkins serialize-hold, two extensions this window.

- Chain depth: 08-16 ~10:00Z the billing-block + glm-serialize produced a
  6-deep held chain with position notes on the rows: refcheck r1
  "SERIALIZE-HELD behind analytics r1 (kimi serialize)"; terminology r1
  "SERIALIZE-HELD (2nd in chain after refcheck r1)"; 5.4 "r1 held in chain
  (5th)"; local-ci "Perkins r1 held (6th in chain)". All released cleanly.
- NEW flavor — holding a MINION dispatch (not a Perkins round) behind a
  merge: v2-7.1-visual-juice 08-17 08:22Z "HELD — do NOT dispatch on
  receipt. RELEASE TRIGGER: the packet-plumber-v2-5.5-demolish-input MERGE
  CLOSE-OUT (5.5 adds the demolish popover chrome; 7.1 polishes the same
  chrome/draw surface — early dispatch = guaranteed rebase collisions)" →
  released 09:34Z "RELEASED @ 388e316 (post-#59-merge head — trigger: 5.5
  close-out)". The dedup row + named trigger + fresh-base-at-release pattern
  applied to a plain dispatch.

## 9. PR-event CI builds branch-MERGED-into-base — golden drift red that is NOT billing noise

The counter-example keeping §1 honest: a real CI failure caused by base
movement, pre-billing-block.

- packet-plumber-v2-5.2-node-health, 2026-08-16T00:53Z: "CI FAILURE…
  node_health.dem T2 goldens fail on BOTH ubuntu+macos… NOTE: a same-sha
  parallel run (31917973370) PASSED — nondeterministic across runs,
  deterministic within."
- Root cause + lesson, 01:02Z: "the PR-event CI builds the branch merged into
  origin/v2 (#52's Open Sans swap), which my pre-merge blessing didn't cover;
  fixed by merging origin/v2 + a deliberate presentation-only T2 fold
  (T1+replay byte-identical)." Minion badged: "check merge-base vs
  origin/base before blessing."

## 10. Deliberate re-bless cause-chain discipline: now standard + Perkins-guarded (5 jobs)

The re-bless pattern (deliberate + documented + byte-proof of the untouched
surface) recurred constantly and is now a named Perkins guard.

- v2-5.9-demand-caps-perkins-r1, 2026-08-17T16:16Z dispatch guards: "4.3
  re-bless cause chain, lane awareness (pre-juice frames)" — verified in
  verdict: "re-bless cause chain sound, 7.1 lane needs NO further T2 churn."
- Recurrence (STRONG): 5.2 (deliberate 3-PNG T2 fold, T1 byte-identical),
  5.4 ("input_parity manifests deliberately re-blessed for the catalog_hash
  fold", 08-16 18:00Z), terminology ("deliberate T1 re-bless (splice-proven),
  T2 byte-identical", 08-16 09:04Z), 7.1 cross-lane FYI ("#62 shipped a
  deliberate 29-frame T2 re-bless — my juiced re-bless lands on MY frames at
  push", 08-17 16:55Z — the lane-to-lane re-bless callout is new).

## 11. Rebase-cascade ops on a multi-PR base: merge-order rulings + proactive rebase relays

8 PRs (#53–#62) on base v2 in ~30h → constant dirty-base events, handled by
guard notes, user merge-order rulings, and relays sent BEFORE the push.

- Merge-order ruling, v2-7.2-audio-juice 08-17 09:34Z: "#59 landed FIRST (v2
  @ 388e316) — 7.2 (#60) is the SECOND PR: its app/input overlap
  (types/exec/poll) must rebase-resolve onto the new v2… pre-emptive rebase
  relay queued to the minion."
- Proactive relay, v2-7.1-visual-juice 08-17 15:28Z: "v2 MOVED @ 18781a4
  (#60 7.2 + #61 doctrine merged 15:24Z) — your branch (388e316) is now
  BEHIND v2; rebase onto origin/v2 before/with your push… the rebase relay
  is standard."
- Recurrence (STRONG): 5.4 rebased ×2 (post-#55 rename adoption 2f5027a;
  post-#56/#58 conflict resolution d91109e), visibility 8575164, doctrine
  ddf8f28, 7.2 1b96bea ("rebase onto v2 @ 388e316 resolved ZERO conflicts —
  disjoint hunks verified" — verify disjointness, then expect clean).

## 12. Cross-lane overlap flag → user ruling → canon addendum (two-layer flag pattern working)

- v2-7.2-audio-juice, 2026-08-17T08:43Z: "FLAG: 7.2 touched
  app/input/{types,exec,poll}.odin — the sibling 5.5 lane's files (M-mute via
  intent layer, an optional feature); overlap noted in the r1 briefing;
  escalated to Gru for the scope decision."
- Ruling 3 min later (08:46Z, both rows): "A — ACCEPT the input-touch; the
  M-mute intent stays… ADDENDUM (Gru): the 7.2 lane guard was over-broad —
  post-5.4 the intent layer is the ONLY legal home for a runtime key;
  audio-side key additions through app/input are acceptable going forward."
  Flag → escalate → rule → note on BOTH sibling rows, no rework.

## 13. NEW noise class: herdr server restart = watcher "panes vanished" FALSE ALARM

- 5 jobs, identical note, 2026-08-16T09:43Z: "herdr 0.8.0 restart transition
  (2026-08-16 09:14Z): watcher saw panes vanish — FALSE ALARM. New server
  restored session; pane ids unchanged; pi processes survived (verified live
  + mid-work). No status/pane changes." (5.4, visibility, terminology,
  refcheck-621, analytics-568-617.)
- Response pattern: verify pi processes alive BEFORE any relaunch; pane ids
  survive a server restart.

## 14. Provider incidents: NEW deepseek-402-mid-round flavor (lens waves lost, chief survives); glm-5.3 1302 2nd sighting

- packet-plumber-terminology-audit-perkins-r1, 2026-08-16T13:00Z: "PROVIDER
  INCIDENT: deepseek 402 Insufficient Balance mid-round (waves g13/g14 lost,
  arch-g11+codebase-g12 retries lost). Sweeping + redispatching 16 lens runs
  on fallback zai-coding-cn/glm-5.3 per provider-incident doctrine (probe
  first)." Recovery confirmed 14:02Z: "112/112 lens outputs… APPROVED".
  New: a 402 BALANCE failure (not 403 quota / 429 burst) hitting only the
  lens provider mid-round; the round pane itself kept working — sweep +
  redispatch the LENSES, not the round.
- traffic-model-design-perkins-r1, 2026-08-16T00:15Z: "INCIDENT: 429 code
  1302 burst (ZAI glm-5.3) again — 2nd this window… ONE continue revived the
  round pane (working); 7 lenses idle (round re-drives them). No spam."
  Doctrine held verbatim.
- Model provenance note: all 08-17 rounds ran kimi-coding/k3 (post-08-16
  "kimi is BACK" ruling) including fix-audits; 08-16 rounds ran glm-5.3 /
  v4-pro. The 5.5 r1 row's note still says "v4-pro" from 08-14 — stale
  provenance text on a REUSED row (see §15).

## 15. Round-row RESET+REDISPATCH on story redelivery — reused rows carry stale note text

- packet-plumber-v2-5.5-demolish-input-perkins-r1, 2026-08-17T08:40Z:
  "RESET + REDISPATCH (r1 for the NEW PR #59 @ 55d1b66): the 08-14 r1
  reviewed the superseded #44 code — replaced. Fresh r1, prior_findings=none…
  Sensor-dedup sha note."
- Hygiene wrinkle: the row's `note` field still reads "sha=23e1704… round 1
  of 3. PROACTIVE dispatch (sweep rule)… v4-pro." — the OLD round's text.
  Reset works for dedup/status but leaves the note column describing the
  superseded round unless explicitly overwritten.

## 16. NEW (product level): a refactor can silently un-ship a MERGED story → redelivery job

- packet-plumber-v2-5.5-demolish-input, 2026-08-17T08:11Z: "REDISPATCH
  (2026-08-17): story re-delivered on the intent layer — the 08-14 #44
  surface rode the pre-5.4 input path; the 5.4 refactor replaced it
  (popover_demolish_hit positive path vestigial, W1-r4). Base v2 @ e07265b
  (post-#57)."
- Lesson: when a refactor replaces an input/draw surface, check whether any
  ALREADY-MERGED story rode the old surface; the redelivery dispatch needs
  prior_findings=none + a RESET round row + a ruling that the old PR is
  "superseded, not re-litigated".

## 17. User mid-flight ruling velocity: 5 rulings in-window, all absorbed in place (no kill-and-redispatch)

Known pattern, high-frequency confirmation this window. Routing = relay to
minion + note on row (+ row-field/briefing amendment when the ruling is a
setting).

- Asset contract ×3 superseding refinements in ~16 min on 7.2 (08:47 "SFX =
  ElevenLabs; music/ambience = Suno only-if-needed" → 08:55 "music =
  ElevenLabs Music OR Suno" → 09:02 "FINAL… music=Suno Premier; ElevenLabs
  Music set aside") — each relayed direct, doc-only pushes, skip-row absorbs
  the head churn (§6).
- Model override, v2-7.1-visual-juice 08-17 08:28Z: "launch on
  kimi-coding/k3, NOT flash — native vision required… Row model field
  updated to kimi-coding/k3 (briefing already updated by Gru). Release…
  MUST launch --model kimi-coding/k3." New detail: the override writes BOTH
  the ledger row model field AND the briefing; the deferred dispatch must
  carry the flag.
- Plus the cap-lift ruling (§5) and the lane ruling (§12).

## 18. Boot-noise flavor: dead-pi REVIVAL produces the same gone→idle alert as a fresh dispatch

- packet-plumber-v2-5.4-input-parity, 2026-08-17T00:53Z: "pane-watcher
  gone→idle @ 00:52:30Z = boot noise from the pi relaunch (dead-pi revival,
  same instant as the new session file 00-52-30-602Z); verified working +
  mid-relay. No status change, no escalation."
- Classification key: alert timestamp == new session-file timestamp. Same
  minute, same pane — it's the relaunch, not a new problem.

## 19. Positive confirmations (absences worth recording)

- **pr-field self-set held all window** (PP crew): 7.2 "self-set ledger
  pr ✓" (08-17 08:43Z), 5.5 "self-set ledger pr ✓, notification fired"
  (08:40Z), 5.9 "self-set ledger pr ✓" (16:17Z). Zero NULL-pr incidents in
  272 events — the verify-and-set guard found nothing to fix. (RT crew also
  clean: #623/#624 pr set at open.)
- **Settle echoes** (known class) kept arriving and were all classified
  note-only — incl. a ~7h-late one (5.4, 08-17 08:02Z, "~7h after the 01:04
  completion") and parked-in-review minions awaiting human merge (×6 jobs).
- **Perkins self-close + verdict-recovered-as-note** continued as the norm
  (traffic-model r1/r2/r3, terminology r1: "round self-closed (Perkins) —
  verdict recovered as note", 08-16 17:54Z).
- **No pane-id slips, no phantom rows, no minion-created rows** observed in
  the window — the 08-14/15 hygiene classes did not recur.
