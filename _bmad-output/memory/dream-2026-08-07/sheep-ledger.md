# Sheep findings — ledger events
Material: 402 events scanned since 2026-08-03T11:12:13Z (the 500-event set,
lines 1–402; the dream-2026-08-03 close-out at 11:12:24Z is the window's left
edge), 56 distinct jobs active in window, 7 shown in detail
(`righttenantryagents-model-flash`, `righttenantry-gcp-cost-analysis`,
`packet-plumber-setup-brief`, `righttenantry-form-e2e-pass`,
`righttenantry-draft-grace-period`, `righttenantry-oauth-posthog-fix`,
`righttenantry-csp-posthog-allowlist`). READ-ONLY — no ledger mutation, no
repo touched.

## Candidate patterns (NEW — not in gotchas)

### glm-5.2 is a 4th provider-incident class — two failure modes, durable fallback = provider switch to deepseek
Distinct from the gotcha's 3 classes (transient stalls / mid-turn refusals /
connection-error waves → `continue`; quota 403 → sweep + re-dispatch). glm-5.2
fails two new ways, and `continue` is NOT the durable fix — a model redirect is.
- **(a) Launch-time auth failure** — bare label `glm-5.2` resolves to the
  `opencode` provider → "No API key found for opencode" → pane never boots.
  Recovery: re-dispatch on an authed model (deepseek). User guard: escalate,
  don't improvise.
- **(b) Mid-turn 429 rate-limit** — pane boots + runs, turn dies mid-task.
  Recovery: one `continue` may revive it, but it re-429s; durable fallback is a
  deepseek relaunch.
- Auth nuance: the full-path label `zai-coding-cn` auths where bare `glm-5.2`
  fails — so glm-5.2 *can* run (finlit-sprint-plan-v1 built on it), but routing
  is flaky/expiring.
- Sightings:
  - `finlit-e2-1` 2026-08-04T23:42:35Z — *"LAUNCH FAILED 23:40Z: glm-5.2
    resolves to 'opencode' provider — 'No API key found for opencode'. The model
    doesn't resolve at launch (user guard: escalate, don't improvise)."*
  - `finlit-e2-7` 2026-08-04T23:42:35Z — *"LAUNCH FAILED 23:40Z: same
    glm-5.2/opencode auth failure as e2-1."*
  - `finlit-e2-1` 2026-08-04T23:43:27Z — *"RE-DISPATCHED on deepseek-v4-flash
    23:50Z (user: redirect, don't troubleshoot glm auth)."*
  - `finlit-e2-7` 2026-08-05T00:29:50Z — *"GLM 429'd mid-run (rate limit — 3rd
    glm sighting); fell back to deepseek."*
  - `finlit-e2-7` 2026-08-05T18:50:31Z — *"glm-5.2 429 (rate limit, 4th glm
    sighting) killed the rebase turn... One 'continue' revived it 18:46Z —
    working. Watch for re-429; deepseek relaunch is the fallback."*
- Candidate memory target: **AGENTS.md gotchas** (extend the "Provider
  incidents come in 3 classes" bullet to a 4th — glm-5.2 auth/429, fallback =
  deepseek redirect, not continue; + the `zai-coding-cn`-vs-bare-label auth
  nuance).

### PI_MODEL env can silently override the dispatched model
A minion dispatched on deepseek ran on glm-5.2 because `PI_MODEL` env won; the
only signal was the minion's own self-report in the close-out note. Distinct
from glm-5.2 failing — here it *succeeded*, just not on the intended model.
- Sighting: `orchestrator-nefario-conflict-sensor` 2026-08-05T09:45:04Z —
  *"NOTE: ran on glm-5.2 (zai-coding-cn) despite deepseek dispatch — PI_MODEL
  env override; glm-5.2 full-path auth worked (unlike bare label -> opencode)."*
- Candidate memory target: **AGENTS.md gotchas** (provider/model subsection) —
  when model provenance matters (e.g. Perkins-reviewed sha), don't trust the
  dispatch label; check `PI_MODEL` / the session jsonl. Single sighting → could
  be a watch item, but cheap to note alongside the glm-5.2 bullet above.

### Merged-mid-round → FYI verdict + optional fresh post-merge audit (no cap, no rework loop)
When the user merges a PR deliberately mid-Perkins-round (pre-verdict): the
in-flight round continues to verdict as an **FYI review** (no rework loop
unless the user says so; real findings become follow-up notes). A **fresh
post-merge audit round** may then be dispatched (FYI-only, no cap implication,
COMMENTED mode) — and its blockers become **new jobs**, not rework of the
merged PR. This is the clean playbook for "user merged before Perkins spoke."
- Sightings:
  - `righttenantry-form-e2e-pass` 2026-08-03T13:42:02Z — *"USER merged #564
    deliberately mid-Perkins-round (13:37:12Z, pre-Perkins verdict). Per Gru:
    r1 CONTINUES to verdict on the merged sha as an FYI review — NO rework loop
    unless the user says otherwise; real findings become follow-up notes."*
  - `righttenantry-form-e2e-pass` 2026-08-03T13:42:37Z — *"merged pre-verdict
    by user; post-merge audit round dispatched (fresh, FYI-only, no cap
    implication)."*
  - `righttenantry-form-e2e-pass` 2026-08-03T15:00:51Z — *"POST-MERGE AUDIT
    findings (FYI, no rework loop): B1 — no-JS fallback renders the only submit
    button unconditionally disabled... Escalated to Gru."* → this B1 spawned
    `righttenantry-form-nojs-submit-fix` (the next job in the thread).
- Candidate memory target: **AGENTS.md gotchas** (extend the Perkins/round-
  budget doctrine) or **playbook round-budget ops** — the merged-mid-round case
  + the audit-finding-becomes-new-job rule.

### Perkins post-failure recoveries (3 flavors) — self-close is now the NORM
Extends the gotcha "Perkins can self-close its round row." This window shows
self-close is expected (10 "0 lens leftovers / self-closed clean" events), and
two NEW recovery flavors when Perkins fails to *post*:
- **(a) Perkins completes analysis but dies pre-post → Silas posts from the
  complete artifacts** (body.md + consolidated.json), no re-run needed.
  - `righttenantry-guarantor-autofill-fix-perkins-r1` 2026-08-05T15:57:13Z —
    *"round completed analysis but Perkins died pre-post (relaunch mid-close-
    out). Silas posted the review from the complete artifacts (body.md +
    consolidated.json)."*
- **(b) Perkins token-mint fails → review posted via fallback-comment** (PR
  comment instead of a formal review). Recovery is automatic, not a re-run.
  - `righttenantry-guarantor-autofill-fix-perkins-r1` 2026-08-05T13:17:25Z —
    *"review posted via fallback-comment (token mint failed); 1 blocker 0
    warnings 2 notes; verdict NEEDS CHANGES."*
- **(c) Self-close clean (0 lens leftovers) is now standard** — every r1/r2/r3
  this window self-closed; Silas's close-out `set done` no-ops (same-status) and
  the verdict rides on the "if no-oped" note. (10 sightings; e.g.
  guarantor-checkbox-desync r2/r3, e2-1 r1, e2-7 r1, csp-enforce r1,
  form-copy-revision r1, guarantor-autofill r2.) Confirms + strengthens the
  existing gotcha rather than replacing it.
- Candidate memory target: **AGENTS.md gotchas** (extend the Perkins-self-close
  bullet with the two post-failure recovery flavors; reaffirm self-close is the
  norm so the verdict must be captured at/before close-out — already stated, now
  load-bearing).

### Coverage-gap & guard-pin-uniqueness — recurring Perkins finding classes
Two flavors of the same defect: a change isn't *locked* because the
assertion/guard exists for siblings but not for the changed component.
- **(a) Model-assertion coverage-gap** — agents that lack a per-agent
  `model==X` assertion test their siblings have, so a model switch isn't pinned.
  - `righttenantryagents-model-flash-perkins-r1` 2026-08-07T01:03:24Z — *"N3
    coverage-gap (3 of 5 Pro agents lack per-agent model-assertion tests their
    siblings have)"*; merged 07:16 — *"N3 highest-value follow-up... locks the
    switch; cheap follow-up PR."*
- **(b) Guard-pin not unique** — a guard/pin isn't unique → a regression isn't
  pinned to the right adjacency; stays an OPEN FOLLOW-UP post-merge.
  - `righttenantry-oauth-posthog-fix-perkins-r1` 2026-08-05T18:46:57Z — *"W1
    substantive: reset-arm guard pin not unique -> regression not pinned"*
    (fix: "pin rt_ph_reset→rt_landlord_id adjacency in both guard lists"); done
    19:04 — *"W1... remains an OPEN FOLLOW-UP."*
- Candidate memory target: **minion-field-notes.md** (minion-facing Perkins-
  finding taxonomy: when adding/changing a component, mirror the siblings'
  assertion tests; make every guard/pin uniquely identify its target). Brief
  names both as rework-loop dynamics this window.

### Co-touch / file-overlap check at PR merge → conditional rebase heads-up
When a PR merges, Silas checks file-overlap with adjacent in-flight minions on
the same base and relays a rebase-develop heads-up ONLY on overlap; no overlap
→ no-op (avoids spurious rebases). Working practice, 3 sightings.
- `righttenantry-form-resume-progress-fix` 2026-08-03T17:10:11Z — *"CO-TOUCH
  WATCH: nojs-submit-fix (w1T:p6Q) dispatched 15:50Z, adjacent surfaces (form
  submit/review_consent + fixtures). First PR to merge -> Silas relays a
  rebase-develop heads-up to the other's pane."*
- `righttenantry-draft-grace-period` 2026-08-03T18:39:19Z — *"co-touch check at
  #569 merge: no overlap (retention SQL vs stepper JS) — no action."*
- `righttenantry-form-nojs-submit-fix` 2026-08-03T18:39:19Z — *"co-touch check
  at #569 merge: zero file overlap (569=form_stepper.js/js-tests;
  570=review_consent.gleam/form_view_test/fixtures) — no rebase heads-up
  needed; mid-flight r1 on e938f27 unaffected."*
- Candidate memory target: **AGENTS.md gotchas** (Silas ops practice) or
  **playbook** (dispatch/close-out section). Pairs naturally with round-budget
  ops.

### No-op confirmation via byte-diff (for changes claimed no-op, esp. security controls)
For a change asserted to be a no-op (notably on a security control like CSP),
confirm at BYTE level: production source minus comment lines is byte-identical
to origin/base; the follow-up push touches ZERO production bytes (git diff =
test file only). Pair with a negative-control invariant test that "bites."
- `righttenantry-csp-posthog-allowlist-perkins-r1` 2026-08-06T02:22:10Z —
  *"no-op confirmed at byte level: csp.gleam minus comment lines is
  byte-identical to origin/develop; all directive values + nonce case
  untouched."*
- `righttenantry-csp-posthog-allowlist-perkins-r2` 2026-08-06T03:06:14Z — *"r2
  push touches ZERO production bytes (git diff b37c2d7..67cc7e4 = test file
  only); the invariant test bites (negative-control verified)."* (r1 N1 had
  flagged the missing absence-invariant test; r2 folded it in.)
- Candidate memory target: **minion-field-notes.md** (minion-facing: how to
  evidence a no-op for Perkins — byte-diff the production file + add a
  negative-control invariant test). Brief explicitly names "no-op confirmations
  via byte-diff" as a practice that worked.

### Quota-403 on a parked / dispatched-pending pane → revivable via `continue` (lighter than the sweep doctrine)
Refinement of the existing quota-403 gotcha. If the round **died at startup**
(pane never got past boot — still dispatched-pending, errored turn is the boot
read) rather than **mid-work**, the pane is NOT dead: once the quota lifts, a
single `continue` on the parked pane resumes the errored turn cleanly — "Same
effect as a re-dispatch; row stays pointed, no sqlite needed." The full
sweep + re-add-worktree + re-dispatch-SAME-round doctrine is for panes that
died MID-WORK (where stale partial lens JSONs contaminate the verdict).
- Sighting: `righttenantry-draft-grace-period-perkins-r1` 2026-08-03T20:16:35Z
  → 20:19:14Z — *"19:40Z: round died at startup on the account-wide quota 403
  (second incidence, ~18:49Z). Row stays dispatched-pending"* … then *"19:50Z
  quota restored (user purchased extra tokens). Round REVIVED via 'continue' on
  the parked pane (w1T:p7M) seconds before Gru's order — its errored turn
  resumed cleanly... Same effect as a re-dispatch; row stays pointed at p7M, no
  sqlite needed."*
- Candidate memory target: **AGENTS.md gotchas** (refine the existing
  provider-incidents/quota-403 bullet: distinguish startup-death =
  continue-revivable-once-quota-returns vs mid-work-death = full sweep +
  regenerate-everything).

### Wrong-repo / no-knob clarify (model-flash arc) — halt + re-dispatch, reframe scope with data
When a task's knob doesn't live in the dispatched repo, the minion halts for
re-dispatch to the correct repo rather than flailing — and frames the scope
decision with external data (here: Pro→Flash reframed as an UPGRADE, not a
downgrade, via Artificial Analysis numbers).
- `righttenantry-agent-model-flash` 2026-08-06T13:00:27Z — *"BLOCKER: model
  selection lives in RightTenantryAgents, not RightTenantry. RightTenantry is a
  pure ADK client (no model knob). Also: 5 agents pinned to Pro in Terraform —
  switching ALL to Flash = Pro->Flash downgrade on risk_scorer + both compliance
  judges. Need Gru re-dispatch + user scope decision."*
- `righttenantry-agent-model-flash` 2026-08-06T13:40:14Z — *"No change in RT
  (correct — pure ADK client, no model knob). Re-dispatched to
  RightTenantryAgents (Q1=A). Resolved: ALL agents -> gemini-3.6-flash... an
  UPGRADE per Artificial Analysis 50v46/33% cheaper/faster."* → completed as
  `righttenantryagents-model-flash`, Perkins r1 APPROVED 0B/0W/4N, merged
  2026-08-07.
- Candidate memory target: **minion-field-notes.md** (minion-facing: when the
  knob isn't in your repo, halt + name the correct target + reframe scope with
  evidence; don't fabricate a change in the wrong repo).

## Perkins round dynamics this window (per job)

| Job | Rounds this window | Final verdict | Notes |
|---|---|---|---|
| righttenantry-form-save-resume-f3 | r1 1B → r2 1B → r3 1B → **r4 (USER-OVERRIDDEN cap, advisory)** | APPROVED r4 (0B/3W/20N+56 carried) | User overrode the cap to force a 4th advisory round after 3 consecutive blockers; r4 = fix-audit full marks. PR #563 merged 11:37Z. |
| righttenantry-form-e2e-pass | r1 (MOOT, merged mid-round) → **post-merge audit** (FYI, no cap) | NEEDS CHANGES 1B/4W/17N (audit) | User merged #564 pre-verdict; r1 re-ran as FYI on merged sha; audit B1 (no-JS submit disabled) → spawned form-nojs-submit-fix. |
| righttenantry-form-nojs-submit-fix | r1 | APPROVED 0B/0W/2N | Held for capacity until #569's r1 closed (valve discipline). |
| righttenantry-form-resume-progress-fix | r1 | APPROVED 0B/1W/5N | #569. |
| righttenantry-draft-grace-period | r1 | APPROVED 0B/2W/4N | r1 quota-403-killed at startup → revived via continue on parked pane. |
| righttenantry-form-copy-revision | r1 | APPROVED 0B/1W/8N | 102-file change; ran on glm-5.2 after relaunch; W1 double-colon follow-up. |
| righttenantry-csp-enforce-allowlist | r1 | APPROVED 0B/1W/2N | #578. |
| righttenantry-csp-posthog-allowlist | r1 (0B/0W/2N) → r2 (0B/0W/1N) | APPROVED r2 | No-op doc comment; r2 folded r1-N1 absence-invariant test. Byte-diff no-op confirmed both rounds. |
| righttenantry-oauth-posthog-fix | r1 | APPROVED 0B/2W/4N | W1 guard-pin-uniqueness stayed OPEN FOLLOW-UP post-merge. |
| righttenantry-guarantor-checkbox-desync | r2 (0B/0W/7N) → r3 (0B/0W/2N FINAL) | APPROVED r3 | r3 re-dispatched codebase lens once after a 429. |
| righttenantry-guarantor-autofill-fix | r1 (NEEDS CHANGES 1B) → r2 (0B/0W/1N) | APPROVED r2 | r1 Perkins died pre-post → Silas posted from artifacts; r1 review via fallback-comment (token mint failed). User ruling [A] partial-fix; skip-row on pre-amendment sha. |
| righttenantryagents-model-flash | r1 | APPROVED 0B/0W/4N | N3 coverage-gap = highest-value follow-up. |
| finlit-e2-1 | r1 | APPROVED 0B/4W/7N | Built on deepseek after glm auth redirect. |
| finlit-e2-7 | r1 (0B/3W/10N) → r2 (MOOT) | APPROVED r1 / moot r2 | r2 swept mid-flight when #11 merged (64cc487); glm 429 killed rebase turn, continue revived. |

**Recurring finding classes this window:** CSP no-op (csp-enforce, csp-posthog
×2 rounds) → resolved by byte-diff + absence-invariant test; guard-pin
uniqueness (oauth W1) → stayed open; model-assertion coverage-gap
(model-flash N3) → follow-up; cross-provider funnel / first-touch attribution
(oauth open Qs) → flagged, not blockers. **Round-count shape:** most jobs
closed in r1; the multi-round arcs (f3 ×4, csp-posthog ×2, guarantor-autofill
×2, guarantor-checkbox ×3) were driven by either a real blocker chain (f3) or
fold-in of advisory findings (csp, autofill). Perkins self-close clean (0 lens
leftovers) in **10/10** rounds — now the default, not the exception.

## Provider incidents this window (class + recovery)

| Class | When | Jobs hit | Recovery |
|---|---|---|---|
| **glm-5.2 launch-auth (bare label → opencode, no key)** | 2026-08-04 23:40Z | finlit-e2-1, finlit-e2-7 | Pane closed; re-dispatched on deepseek-v4-flash 23:50Z (user: redirect, don't troubleshoot). |
| **glm-5.2 mid-turn 429 rate-limit** | 2026-08-05 00:2xZ, 18:38Z | finlit-e2-7 (×2) | One `continue` revived (18:46Z); durable fallback = deepseek relaunch. |
| **glm-5.2 opencode-auth spawning review swarm** | 2026-08-05 00:13Z | finlit-e2-1 | Minion fell back to deepseek correctly (2nd independent sighting). |
| **PI_MODEL override (deepseek dispatch → glm-5.2 run)** | 2026-08-05 09:41Z | orchestrator-nefario-conflict-sensor | No recovery needed (succeeded via zai-coding-cn full-path); provenance noted. |
| **quota 403 (2nd incidence), round died at STARTUP** | 2026-08-03 ~18:49Z | righttenantry-draft-grace-period-perkins-r1 | Row held dispatched-pending; on quota restore (user bought tokens, 19:50Z) `continue` on parked pane resumed cleanly — lighter than the full sweep doctrine (no mid-work lens JSON to contaminate). |
| **quota 403 wave (carry-over from pre-marker 08-03 morning)** | pre-11:12Z | (finlit-sprint-plan-v1 turn died mid-build) | finlit-sprint-plan-v1 pane+worktree HELD for resume-via-continue; user then PAUSED the job (deploy focus). |

Note: the gotcha's existing 3 classes (stalls/refusals/connection-waves →
continue; quota 403 mid-work → sweep + regenerate) all still apply; the NEW
additions are glm-5.2 (auth + 429 → deepseek redirect) and the
quota-403-at-startup → continue-on-parked-pane refinement.

## Watch items recurring (2nd sighting this window)

- **Perkins self-close clean (0 lens leftovers)** — 10 sightings this window;
  now the default. Strengthens the existing gotcha; the load-bearing corollary
  (capture verdict at/before close-out, since the close-out `set done` will
  no-op) was exercised correctly every time via the "if no-oped" note.
- **Sensor echoes handled note-only (doctrine working)** — many clean
  handlings: packet-plumber-setup-brief (01:06 PR-merge echo), finlit-juice-
  checklist (08-03 18:19 merge echo), oauth-posthog-fix-perkins-r1 (18:59
  pane-watcher echo), csp-posthog-allowlist-perkins-r2 (02:57 Perkins-sensor
  echo), form-resume-progress-fix (18:28 review-sensor echo), form-nojs-submit-
  fix (08-03 20:16 review-sensor echo). Every one = note-only, no double
  action. Confirms the gotcha; no new lesson.
- **glm-5.2 failures** — 5+ sightings (see provider-incidents table + candidate
  pattern). Past watch threshold; promoted to a candidate gotcha above.

## One-off anecdotes (single sighting — watch items)

- **finlit-architecture-v1 unverified-verdict gate-drill (2026-08-03
  17:55–18:05Z):** a typed `approved` at 17:55:31Z of UNVERIFIED origin → PR #7
  opened on it → minion halted pre-further-action → Gru said no verdict relayed
  → confirmed via session-jsonl ground truth as **user-direct-in-pane** (legit).
  *"VERDICT CONFIRMED 18:30Z: the 17:55 'approved' was the USER typing directly
  into the minion pane."* Recovery = halt on unverified verdict, confirm
  provenance via the jsonl. Ties to the "ground truth = session jsonl" gotcha
  but is a distinct incident class (verdict provenance, not pane forensics).
  Watch.
- **packet-plumber repo moved mssoka → solarity mid-job (2026-08-06 00:56Z):**
  remote re-pointed at user direction mid-setup-brief; old PR closed, re-opened
  at canonical, stray `mssoka/packet-plumber` repo deleted by user (confirmed
  404). One-off; the durable bit = update the `pr` field + close/reopen on the
  new remote + flag the stray for user cleanup.
- **Analysis jobs at the orchestrator root run from a Gru-safe SUBDIR.**
  `righttenantry-gcp-cost-analysis` note: *"Pane cwd=_bmad-output/billing
  (Gru-safe SUBDIR — gru.ts/nefario-watch guard on cwd===/Users/moses/code, so
  root cwd would pseudo-Gru the minion)."* This is the affirmative counterpart
  to the "never hand a non-Gru agent a pane rooted at the orchestrator root"
  gotcha — reinforces it with the working practice (use a subdir). Worth a
  one-line add to that gotcha.
- **gcp-cost-analysis no-PR compliance gap — ALREADY IN STORE.** The gotcha
  (added 2026-08-07) already captures it exactly: *"minion CONSTRUCTED `herdr
  notification show` but did NOT execute it [0 cli:notification:show results] ->
  compliance gap."* Event-stream cross-check is consistent — the gcp-cost-
  analysis events list deliverables (dashboard + md + parse_costs.py) but no
  notification-execution text; the definitive check is the jsonl (0
  `cli:notification:show` results), already done. Not re-proposed.
