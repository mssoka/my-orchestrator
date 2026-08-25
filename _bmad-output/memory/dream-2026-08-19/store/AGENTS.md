# /Users/moses/code — orchestrator root

Multi-repo workspace. Orchestration is handled by two pi sessions at
this directory root: **Gru** (CEO — user interface, launched `PI_GRU=1 pi`,
enforced by `.pi/extensions/gru.ts`) and **Silas** (COO — all operations,
launched `PI_SILAS=1 pi`, pane label `silas`, enforced by
`.pi/extensions/silas.ts` + `nefario-watch.ts`) — not by this file.

Naming: **Gru** = CEO (user interface), **Silas** = COO (operations),
**minion** = dispatched task agent,
**mega-minion** = specialist helper a minion spawns, **Bob** = the
dreamer minion (periodic memory consolidation). See README.md.

Voice: Gru speaks to the user **in character** (Despicable Me) — see the
playbook's "Gru persona (voice)"; **minions speak minion** when the user
chats with them directly in their panes ("Minion persona (voice)").
Persona is for user-facing chat only; briefings, ledger notes, code,
and PR text stay plain and precise.

Reporting format: when presenting data the user must absorb — updates,
boards, statuses, comparisons — **always use rich markdown tables with
emojis** so they stand out from the surrounding text and catch the eye.
Prose carries the story; tables carry the data.

Review loop: DOCS deliverables (bmad docs, reports, specs, plans — never
code) get a lavish in-browser review **before the PR opens**; clarify
questions go through lavish too when practical (the user answers in the
browser). Code keeps the regular PR pattern. **Exemption:** small/targeted
doc edits (a focused amendment, a one-section fix, a canon touch-up) skip
lavish and open the PR directly — when that's the intent, the briefing says
so explicitly ("lavish not needed, PR directly"), NEVER the ambiguous
"lavish optional" (which parked a minion ~7h on 2026-08-08).

- Playbook: `docs/orchestration-playbook.md`
- Job ledger: SQLite at `_bmad-output/orchestrator.db` (CLI: `bin/ledger`)
- Memory: playbook section 'Memory system' — curated minion lessons
  `docs/minion-field-notes.md`, per-job shards
  `_bmad-output/field-notes/<job-id>.md`, Gru journal
  `_bmad-output/gru-journal/`, Silas journal
  `_bmad-output/silas-journal/`. Concurrency = shard-by-writer (no locks).

If you are an agent session anywhere else (a repo under this directory, a
worktree, etc.): you are **not** Gru. Do not dispatch minions
or track jobs. Work the repo in front of you; if asked to orchestrate, point
the user at the Gru session in `/Users/moses/code`.

## Gru gotchas (field notes, learned the hard way)

### Dispatch & handover

- **`herdr agent send` does not submit.** It types text into the pane's
  input buffer and leaves it there unsent. To deliver a prompt or
  follow-up, use `herdr pane run <pane> "<text>"` (sends text + Enter
  together). If text is already stuck in a buffer, submit it with
  `herdr pane send-keys <pane> enter`. The playbook's clarify-relay
  section still names `agent send` — treat that as a doc bug; use
  `pane run`.
- **`herdr pane run` can ALSO leave text unsent** when the target agent is
  mid-startup (typed into a not-yet-ready TUI, Enter lost). ALWAYS verify
  handover delivery after sending: read the pane (`herdr pane read`) or
  check the session file exists
  (`ls ~/.pi/agent/sessions/ | grep <slug>`). Stuck buffer →
  `herdr pane send-keys <pane> enter`. (2026-07-31: two handovers sat
  unsubmitted; the user spotted both.)
- **Never yield a turn between `herdr wait idle` and the handover
  (2026-08-06).** The dispatch boot sequence — `herdr pane run <pane>
  "pi"` → `herdr wait agent-status <pane> --status idle` → `herdr pane
  run <pane> "<handover>"` — is ONE continuous flow; the `wait`
  succeeding IS the green light (nothing left to verify before handing
  over). A minion at idle with no handover is dead time (blank pane,
  zero progress). PREVENTION: chain all FOUR in a single bash `&&` command —
  `herdr pane run <pane> "pi"` && `herdr wait agent-status <pane>
  --status idle --timeout 90000` && **`sleep 3`** && `herdr pane run
  <pane> "<handover>"`. The `sleep 3` AFTER idle is REQUIRED, not
  optional: `wait --status idle` returns the instant pi reports idle,
  but the TUI's input handler isn't always ready to accept keystrokes
  at that exact moment — without the sleep, the chained handover types
  into a not-yet-ready TUI and Enter is lost (buffer sits unsent; pane
  stays idle with an empty session). SEEN TWICE on 2026-08-06
  (agent-model-flash + RT-Agents: both chained dispatches left the
  minion idle until `send-keys enter` recovered them; the non-chained
  csp dispatch with a natural gap did NOT hit it). Then verify delivery
  as a SEPARATE post-step (working within ~30s, else `herdr pane
  send-keys <pane> enter` for a stuck buffer) — sleep + verify together
  make it reliable.
  (2026-08-06: cost-analysis minion sat blank ~30s after boot because
  Silas ended the turn after the `wait` instead of chaining straight to
  the handover; user spotted it.)
  2026-08-19 addendum (dream-2026-08-19; wire-aesthetics-perkins-r1 +
  this dream's own sheep boots — ×3): herdr 0.8.0 RENAMED the wait —
  `herdr wait agent-status <pane> --status idle` is GONE ("unknown
  command: wait"); the 0.8.0 form is `herdr agent wait <pane> --until
  idle --timeout 90000`, and it RACES pi registration on fresh panes
  (`agent_not_found` while the agent entry doesn't exist yet) — sleep
  ~10 BEFORE the wait (the post-idle sleep 3 still stands). And NO
  PIPES on the wait: `... agent wait ... 2>&1 | tail -1 && ...` masks
  the wait's failure exit code (tail returns 0), so the `&&` chain
  CONTINUES into a not-ready pane — the pipe-masked variant is what
  launched a Perkins round on a bare `pi` mid-chain (→ defaultProvider,
  wrong model). Corrected chain: sleep 10-12 for registration →
  un-piped `herdr agent wait` → sleep 3 → handover → verify working.
- **`herdr pane move` has no `--json` flag** (rejected as unknown option),
  but it prints the full JSON result anyway — parse stdout directly, or
  re-read the new pane id from `herdr agent list`. Same for
  `herdr tab create` (2026-08-08) and `herdr pane split`
  (dream-2026-08-15; verified still true on herdr 0.8.0,
  dream-2026-08-17 — no `--json` flag, the raw stdout IS the JSON;
  capture key `result.pane.pane_id`).
- **Silas: minions never split into identity tabs.** Dispatch step 3:
  the `gru` and `silas` tabs carry their owner only — minion panes go to
  a dedicated minions tab or a new tab labeled `<job-id>`; after any
  accidental split, move the minion out AND relabel the identity tab
  back to its bare owner name. (2026-08-01: form-stepper-f1 launched as
  a split of the silas tab; t2 kept 'silas+form-stepper-f1' after the
  move until relabeled.)
- **Silas: a deliverable is not reported until it reaches Gru's input.**
  Text in Silas' own pane output is thinking-out-loud — Gru only sees
  what arrives via `herdr pane run <gru-pane> "[SILAS] ..."`. Every
  completed ops task (PRs opened, close-outs, dispatches) ends with that
  one-line message carrying the deliverables (URLs, pane ids). (2026-08-01:
  research PRs #559/#560 went unreported; Gru relayed the URLs himself.)
  2026-08-19 addendum (dream-2026-08-19; v2-6.1-era-definition
  close-out): sighting #3 — the close-out executed but the escalation
  never reached Gru's input (re-escalated 08:13Z). The relay step is
  still the failure point.
- **A pi launched with cwd=`/Users/moses/code` IS Gru** — gru.ts guards on
  `ctx.cwd` alone, so the session gets the startup checklist as a user
  message + Gru standing orders every turn, and its session file lands in
  Gru's own session dir. Dream passes launch Bob with
  `cd ~/.herdr/bob-home && pi`; never hand a non-Gru agent a pane rooted at
  the orchestrator root. (2026-08-01: dream-2026-08-01 + 3 sheep ran as
  pseudo-Grus; Bob caught it himself mid-dream.)
- **Launching Gru with BOTH PI_GRU=1 AND PI_SILAS=1 duplicates watcher
  alerts (confirmed journaled 2026-08-01, unfiled).** Both extensions fire
  in Gru's pane → alerts echo. Recovery: relaunch Gru as
  `env -u PI_SILAS PI_GRU=1 pi` (PI_SILAS unset). Distinct from the
  cwd-gate gotcha — this is the env-var gate.
- **In-repo (no-worktree) follow-up jobs: Gru's fresh dispatch = the prior
  pane is free (2026-08-07).** An in-repo follow-up needs the repo's working
  tree free, so Gru dispatching the next job IS the signal the prior pane is
  done being used → close that pane + sync the base FIRST (avoids the
  GDD→architecture working-tree conflict hit on packet-plumber). In-repo
  pane creation = `herdr tab create --cwd <repo>` (no worktree create);
  close-out closes the pane BEFORE deleting the branch (the pane shares the
  working tree). 2026-08-09 addendum: the ORCHESTRATOR ROOT is the
  permanent exception — its tree is Gru+Silas' LIVE home and is never
  free, so orchestrator-root jobs ALWAYS run in a worktree even when the
  briefing says "no worktree" (both 08-07 UA follow-ups deviated
  correctly; a root branch switch would move Gru's HEAD under him). When
  a sibling minion holds a repo's main checkout on its own branch,
  close-out's `pull --ff-only` can't run — sync the base with
  `git fetch origin <base>:<base>` (updates the ref without touching the
  tree; 4 uses on packet-plumber 08-07/08).
- **User mid-flight reversals kill in-flight work and spawn canon-cascade
  jobs (2026-08-07..08, 4 sightings).** The 84s manual->dev-auto->manual
  flip killed rc2-2's minion pF1; the blender-art LIGHT verdict
  redirected the art direction (light-cascade + art-direction-amend
  followed); a lavish verdict REVERSED the locked Godot engine choice
  (odin-architecture + forge6 + port-limits followed). Ops rules: locked
  decisions (FORGE locks, engine choice) are PROVISIONAL until the user
  reacts to something concrete at a lavish gate — expect reversals
  there; prefer in-place correction over kill-and-redispatch when the
  reversal is a setting (`/model`, a relayed redirect); every direction
  reversal needs an explicitly ROUTED cascade job, not an orphan
  thread. 2026-08-13 addendum (dream-2026-08-13): the healthy mid-flight
  path is AMEND the canon docs + RELAY to the in-flight minion so the
  PR ships the ruling (spatial-lane canon 2e3acab/8ece056 relayed to
  3.3 pZ8; both PRs carried the canon) — and when GDD/architecture/
  stories diverge, the prototype's MAIN branch is the ground truth to
  diff against (the router-placement miss: prototype had
  Cmd_Place_Router + tray intact; the v2 replan dropped it).
- **Cross-job impact = flag, never act across the boundary
  (2026-08-07/08, 2 sightings).** A minion that spots ANOTHER job's
  file/decision being wrong flags it in its PR, out of scope
  (art-direction flagged the prototype's packet_types.json color
  mismatch, uncommitted; blender-art's A1-A7 trail was richer than
  light-cascade's scope) — Silas surfaces it, Gru relays the scope
  decision, the OWNING minion applies it. This two-layer relay is how
  multi-minion canon stays consistent without minions editing each
  other's files.
- **RT main-checkout worktree bootstrap: `cp -r` cycles on the
  self-referencing `_bmad` symlink — `rsync --exclude='_bmad'` is the
  standard copy (2026-08-13, ×2 same evening; recurs on every RT
  dispatch from the main checkout).**

### Provider incidents

- **Provider incidents come in 3 classes with different recoveries
  (2026-08-02/03).** Transient stalls, mid-turn refusals, and
  connection-error waves all leave a LIVE pi with `stopReason:"error"` in
  the session jsonl — `herdr pane run <pane> "continue"` revives them (one
  continue per pane, no loops; a fleet wave = one continue per pane, then
  verify any reviewed sha is unchanged). An account-wide quota 403 is
  different: panes are DEAD and `continue` does nothing — sweep the dead
  panes, re-add the worktree at the same sha, re-dispatch the SAME round
  row with a regenerate-everything amendment (stale partial lens JSONs
  contaminate the verdict), and take another job's activity as evidence
  the quota lifted. Second failure -> `blocked` + escalate. (2026-08-02:
  quota 403 killed Perkins r2 mid-round — retry run clean, 21/21 lens
  verdicts regenerated; same day a connection wave blocked 9 panes, all
  revived with continue x9.) 2026-08-07 addendum: glm-5.2 is a 4th class —
  it fails at LAUNCH (bare label → opencode provider, no key) AND mid-turn
  (429 rate-limit); `continue` may revive a 429 once but it re-429s — the
  durable fix is a MODEL REDIRECT to deepseek, not continue (the full path
  `zai-coding-cn/glm-5.2` auths where the bare label fails). Also `PI_MODEL`
  env silently overrides the dispatched `--model` — when model provenance
  matters (e.g. a Perkins-reviewed sha), check `PI_MODEL` / the session
  jsonl, don't trust the dispatch label. And a quota-403 that kills a round
  at STARTUP (dispatched-pending, no mid-work lens JSON) is continue-
  revivable once the quota returns — lighter than the full sweep+regenerate
  doctrine, which is for panes that died MID-WORK. 2026-08-09 addendum:
  a 5th class needs NO action — a `blocked` alert on a >5h-old minion
  whose transcript shows "Cache miss after ~Xm idle -> re-billed" is
  transient cache-expiry noise: it recovers to working on its own (3
  panes in one 08-08 batch + rc2-3, whose PR opened 17 min later).
  Classify by transcript + pane age BEFORE acting; `continue`-spamming
  these is waste. Distinct from the errored-turn class
  (stopReason:"error" -> exactly one `continue`). 2026-08-11 addendum
  (the kimi-quota-403 saga): with kimi quota-down all billing cycle,
  **glm-5.2 is the sanctioned Perkins fallback** — the 08-07 "redirect
  glm-5.2 → deepseek" doctrine is superseded when KIMI is the down
  provider (glm-5.2 is then the recovery TARGET, not redirect-away-from).
  A **first-turn 403** (no lenses/artifacts) recovers via mid-pane `/model
  zai-coding-cn/glm-5.2` + `continue` — pane recovers to working, NO
  re-dispatch, NO regenerate (lighter than the mid-work-403
  sweep+regenerate doctrine, which still applies when partial lens JSONs
  exist). 2026-08-12 supersede (user ruling, playbook 388fbfb):
  **glm-5.2 is RETIRED from review/reasoning duty — the Perkins
  failover is deepseek/deepseek-v4-flash.** kimi k3 403 during a round →
  first-turn: mid-pane `/model deepseek/deepseek-v4-flash` + `continue`;
  mid-work: sweep + redispatch on deepseek — NEVER glm-5.2 (benchmark:
  k3 69 / deepseek 53 / glm 44; deepseek always-live). 2026-08-12-late
  supersede (user ruling, playbook a96d36b): **kimi k3 RETIRED entirely —
  the reasoning tier is `deepseek/deepseek-v4-pro`** (Gru/Perkins/Bob);
  flash stays for ops/coding (Silas/minions/mega-minions); interim if
  v4-pro is unavailable = flash. Perkins round panes AND lenses launch
  on v4-pro; Bob's dreams route v4-pro. The "kimi is back up" premise is UNRELIABLE mid-cycle (403
  recurred within ~12 min of an apparent recovery). A 403-killed round is
  a RETRY on the SAME row (not rN+1); sweep ALL dead panes, fresh worktree
  @ same sha, regenerate ALL lens JSONs (discard 3-byte empties — they
  contaminate the verdict), carry prior findings forward. A pane-watcher
  `gone->done` echo right after a 403 is the transient pre-recovery
  flicker — note-only. 2026-08-13 addendum (dream-2026-08-13):
  (a) 429 error CODES matter — 1302 burst (one continue revives) vs
  1308 5-hour hard cap (account-wide wall, continue = waste; self-heals
  as panes idle — block + note the reset time, no continue-spam).
  (b) Dual-provider-down → HOLD regime: no new dispatches,
  minimum-effort watcher ops, light close-outs — deepseek + openrouter
  are the always-live spares; the pi probe one-liner clears PI_* env
  first (`env $(env|grep '^PI_'|sed 's/=.*//;s/^/-u /'|tr '\n' ' ') pi
  --model <p>/<m> -p --no-session -nt "Reply OK"`); auth.json keys use
  `{"type":"api_key","key":"sk-..."}` (the field is `key`).
  (c) NEW CLASS — recurring "Connection error / Retry failed after 3
  attempts" on deepseek = CHECK NETWORK with the user before provider
  blame: 2026-08-13's two waves on BOTH v4-pro and v4-flash were the
  office FIREWALL (user-confirmed; hotspot fixed it). One continue per
  pane still clears each wave meanwhile; do NOT loop continues.
  2026-08-14 supersede (user ruling, dream-2026-08-15): **the reasoning
  tier is `zai-coding-cn/glm-5.3`** (Gru/Perkins/Bob — GLM 5.3 released,
  "back on top"; playbook Model policy updated + committed);
  `deepseek/deepseek-v4-pro` = interim fallback if ZAI errors; flash
  unchanged for ops/coding. Verified end-to-end 08-14: authed + routes
  via the env-cleared probe; a "glm-4.7" self-report was model
  HALLUCINATION — the session jsonl's modelId is the ground truth, and a
  "ZAI balance 0" conclusion was a WRONG-ENDPOINT curl — verify new
  models THROUGH pi (probe + session jsonl), never raw API curls or the
  reply's self-named id; bare glm labels still misroute (full path
  mandatory). Model flips apply to NEW dispatches only — an in-flight
  round completes on its launched model (5.3-r1 stayed v4-pro,
  sanctioned). 9 glm-5.3 Perkins rounds 08-14/15, all clean; one 1302
  burst (one continue). 2026-08-16 supersede (user ruling): **kimi k3 is
  BACK — the reasoning tier returns to `kimi-coding/k3`** (Gru/Perkins/Bob;
  supersedes the 08-14 glm-5.3 ruling); interim fallbacks in order:
  glm-5.3 → deepseek-v4-pro → flash. VERIFIED 08-16 via env-cleared probe
  + session jsonl (modelId=`k3`, stopReason=`stop`). The 08-12 lesson
  stands — "kimi is back" is UNRELIABLE mid-cycle (403 recurred ~12 min
  after an apparent recovery): probe before the first round routes to it;
  a kimi round 403 mid-work → sweep + redispatch on glm-5.3/v4-pro.
  Model flips apply to NEW dispatches only (in-flight fleet stays flash).
  (d) 2026-08-14 sibling class — GitHub Actions BILLING block looks like
  CI-red but the runner NEVER started ("recent account payments have
  failed / spending limit"): rerun useless, NOT code instability, NOT a
  hold trigger — dispatch rounds anyway (Perkins verifies locally at the
  sha = ground truth), ONE escalation to the user, then note-only per PR
  ("same billing block"), and retire the briefing caveat line once
  fixed (×6 PRs 08-13/14; fixed via #618 green checks).
  2026-08-16 SUPERSEDE (user ruling): billing NO LONGER GATES MERGES —
  local/integration tests (the local-ci-suite replica) are the merge
  ground truth; the billing caveat is RETIRED from PR bodies/briefings
  (note-only if it recurs; no escalation needed per recurrence — the
  ruling IS the standing answer; minions note it in PR bodies once, not
  per-PR). Both RT PRs #624/#623 merged same day while billing-blocked,
  ruling satisfied a posteriori. 2026-08-17 addenda
  (dream-2026-08-17): (a) the billing block kills GH-ACTIONS RUNNERS
  ONLY — Perkins verifies LOCALLY (pi panes + harness at the sha) and
  is UNAFFECTED; a slow/missing Perkins review is NOT billing
  evidence (a minion AND Silas both misdiagnosed it on #61 08-17 —
  the misdiagnosis reached an escalation + PR comment). Verify which
  substrate a process rides before declaring it blocked. (b) A GitHub
  PLATFORM outage is its own incident class (08-17 13:40Z–:
  API/PRs/Issues/Actions MAJOR, webhooks partial, ~20% errors, GIT
  GREEN) — ONE advisory fanned to all in-flight rows pre-classifying
  the noise (API flakes / sensor gaps / webhook lag = incident noise,
  retry beats alert), NO holds, Perkins local verification
  unaffected; merges stay user-side — when the web merge is down the
  local-merge+push CLI recipe unblocks (#61 + #60 merged 8s apart;
  webhook alerts lagged ~4 min).
  2026-08-19 supersede (user ruling, morning; playbook 7e889ec):
  **v4-pro is BANNED from the reasoning tier (cost) — the reasoning
  chain is kimi k3 → zai-coding-cn/glm-5.3 → HOLD** (park; NO reasoning
  dispatches while both are down; mid-work rounds PARK until a probe
  flips a trusted provider back — never a v4-pro continue). Supersedes
  the 08-12 v4-pro failover, the 08-16 'k3 → glm-5.3 → v4-pro → flash'
  order, the 08-17 'reasoning = v4-pro' line, and the 08-18
  'emergency-only' framing. During a both-down HOLD the user holds
  MERGES too, and any verdict completed on a fallback model mid-hold
  is an INFORMATIONAL record only — no follow-up round rides it (5.11
  r4 precedent 08-18; hold lifted 23:23Z on the k3 probe-flip).
  flash stays ops/coding. 2026-08-19 addendum — NEW incident class:
  deepseek **402 Insufficient Balance** = an ACCOUNT wall (billing,
  not quota/rate — a user top-up fixes it; waiting does not). It killed
  the always-live ops spare midday 08-19 (demo-mode + 7.3 turns errored
  402; the probe confirmed flash AND v4-pro dead account-wide) → user
  flipped ALL ops to glm-5.3 (playbook af06ff3), reverted to flash the
  same evening when the balance returned (playbook b2f51d9; in-flight
  panes STAY on their launched model — the glm ops interlude is
  retired). Recovery per errored pane: `/model <ops fallback>` +
  continue, once. 2026-08-18/19 addendum — probe doctrine hardened
  (×4): probe at EVERY reasoning dispatch (k3 flickered
  22:35→01:41→02:41→03:40 in one night — 'back' is never durable); a
  freed rolling window is NOT headroom (glm's 03:47Z early-reset window
  re-capped in ~4h under one round's lens load); the cap MESSAGE's
  stated reset time lies (claimed 17:54Z vs actual 12:48Z); and a
  single probe-DOWN row with an empty error can be a transient false
  read — re-probe once before acting on it. 2026-08-19 addendum —
  1302 CONCENTRATION: with k3 cycle-capped, ALL reasoning rides glm
  and the account 1302-bursts EPISODICALLY (fleet-wide wave 17:53Z:
  QoS-r1 + demo-mode-r4 + 7.3-r1 + dream panes together) — one
  continue per errored pane clears it, hold NEW glm dispatches until
  the wave settles, escalate only if continues stop clearing.
- **Model dispatch & correction ops (2026-08-09).** Only a
  `provider/model` path naming an AUTHED provider works: bare
  `kimi-coding` fails (it's a PROVIDER with a key in auth.json, not a
  model — the label is `kimi-coding/k3`); `moonshotai/kimi-k3` MISROUTES
  via openrouter. (Minion-facing glm instance lives in field-notes.)
  Model corrections don't need a kill: `/model <provider>/<model>` typed
  to a RUNNING pi switches it MID-SESSION, context preserved (observed
  08-08 odin saga; pi README: `/model` = Switch models) — the
  kill-and-relaunch reflex discarded the odin deepseek draft for
  nothing. A model WALL shouldn't stall a dispatch: launch on the proven
  fallback + flag Gru (Silas 08-08: deepseek vs a 1h kimi wall; Gru
  ratified "deepseek for docs, kimi for code after the wall") — and
  accept a user mid-run override reversal. pi's defaultProvider is now
  kimi-coding, so UNSET-model dispatches resolve to kimi-coding/k3 (the
  flip side of the `PI_MODEL`-override gotcha: know what "unset" means).
  2026-08-13 addendum (dream-2026-08-13): briefing model lines are
  LOAD-BEARING for mega-minion spawns — the code-review skill pins NO
  model on lens launches, and bare `pi` resolves to defaultProvider
  (kimi-coding — a RETIRED provider since 08-12, so an unset dispatch
  silently lands on retired kimi/k3). Name the model for minion AND
  mega-minions explicitly in every briefing; template model lines rot
  (the dream template's "unset" meant retired-kimi at the 08-13
  dispatch — override required).
  2026-08-19 supersede (user ruling, wire-aesthetics r1 / PR #70):
  defaultProvider is now deepseek/deepseek-v4-flash — an UNSET or
  bare-`pi` Perkins ROUND launch now runs the WHOLE round on flash
  (wire-aesthetics r1 closed APPROVED 0-blockers on flash — the verdict
  was SANCTIONED on the row as a one-off: it stood on in-tree code
  verification, no k3 re-review. NOT a precedent). PROVENANCE RULING:
  pin `--model <provider>/<model>` explicitly at every Perkins
  round-MAIN launch (the 08-13 lesson covered lens briefings; this
  extends it to the round pane itself) and verify the session modelId
  after every launch.
- **Serialize concurrent Perkins BURSTS (2026-08-11; models renamed 2026-08-12; SUPERSEDED 2026-08-16).**
  **2026-08-16 USER RULING: FULL THROTTLE on all providers — the serialize-on-quota
  doctrine below is LIFTED.** Dispatch rounds as needed, no holding behind
  in-flight rounds for capacity; a 429 wave = standard recovery (one continue
  per pane) + a note, never a hold. Pane-capacity judgment stays Silas'
  (workspace under the ~20 safety valve); review-target stability (08-11)
  still gates (don't dispatch a sha about to be force-pushed). Historical
  context (retained for the record): A Perkins round =
  ~8 concurrent lens panes (glm-5.2 historically; now kimi k3, deepseek-v4-flash fallback); two rounds
  (or a round + a fanned-out
  mega-minion wave) concurrently trip an account rate-limit 429 (a
  13-pane glm-5.2 429 wave 08-09). SERIALIZE the bursts (one fan-out at a
  time); defer/stagger a job's mega-minions entirely until an in-flight
  Perkins round closes (trigger = the round's close-out). Sibling to the
  pane-capacity serialize-hold — same dedup, different gate (model-quota
  vs pane-count). 2026-08-14 addendum (dream-2026-08-15): the gate is
  PER-PROVIDER — deepseek carries the user's 08-12 parallel-rounds
  override (two concurrent rounds ran clean; parallel across DIFFERENT
  providers is fine), but ZAI/glm-5.3 serializes one fan-out at a time:
  a 1302 burst hit the 5th glm-5.3 round of the day (5.7-r2 08-14
  20:45Z; one continue revived; ~5 rounds/day cumulative is the observed
  burst ceiling — serialize the rest of that day's glm fan-outs).
  2026-08-17 addendum (dream-2026-08-17): full throttle HELD on kimi
  k3 — the first 3-concurrent-round k3 burst (08-16 18:40Z) plus a
  2-round burst (08-17: 5.5-r1 + 7.2-r1) ran with ZERO 429s; don't
  re-litigate the serialize reflex on k3. 2026-08-19 addendum (user
  rulings, wire-aesthetics r1 + demo-mode r3): the ~20-pane VALVE is
  ADVISORY too — "dont hold... let them all run" (21 panes flew clean;
  record valve-pressure as a row note and DISPATCH — the valve surfaces
  pressure, it no longer gates). Real contention resolves by BUSINESS
  PRIORITY (user ruling 08-19, playbook 0d70ff5): RT first over PP for
  panes/quota/Perkins/dispatch windows; the PP belt is merge-gated and
  self-paces at minion speed — batch PP merge relays, no urgency
  framing.

### Watchers, sensors & Perkins rounds

- **nefario-watch fires settle transitions.** After a minion finishes a
  turn, the watcher often reports `done -> idle` (or `working -> idle`)
  minutes later with zero new transcript content. Classify via
  `herdr pane read` before acting; most of these are noise needing no
  ledger write and no user relay. (2026-07-29: six alerts, four were
  settles.) 2026-08-09 addendum: a sibling noise class on FRESH
  dispatches — `gone -> idle (ledger dispatched)` fires when the watcher
  polls a new pane mid-boot (shell -> pi registration) before the minion
  self-reports working (4 sightings 08-06..08-08: agent-model-flash,
  per-applicant-remind, prototype-iterate-1, rc3-2). A fresh dispatch's
  first alert is usually the boot, not a problem. 2026-08-11 addendum:
  Silas now pre-emptively writes a "settle (working->done after clean
  completion): <summary>" note at close-out to classify the inevitable
  settle echo BEFORE it fires — the note IS the classification, so the
  echo that follows is note-only (and doubles as the human-readable
  completion summary: PR + suite counts + what was proven). Standard,
  not optional (5 sightings this window). 2026-08-17 addendum
  (dream-2026-08-17): two more noise flavors — (a) a herdr SERVER
  RESTART (the 0.8.0 upgrade 08-16 09:14Z) makes the watcher fire
  "pane no longer has a detected agent" for EVERY tracked pane —
  FALSE ALARM: pane ids survive, pi processes survive (verify via
  lsof on the pane cwd BEFORE any relaunch; 5 jobs noted, zero action
  needed); (b) a dead-pi RELAUNCH produces the same gone→idle alert
  as a fresh dispatch — the classification key is alert-ts ==
  new-session-file ts (5.4, 08-17 00:52Z). Sibling close-out hygiene
  from the same census: worktree removal does NOT kill spawned
  processes — 3 stuck core.bin (removed worktree) spinning ~3.5 cores
  + 2 orphaned beam.smp dev servers found; sweep orphan processes at
  census/close-out.
- **Review/Perkins/cap sensors re-fire already-acted events — expect one
  stale echo per action (2026-08-01/02).** Silas relays/escalates/
  dispatches at round close-out; the sensor tick lands seconds-to-minutes
  later and re-alerts the same review/sha/cap. Distinct from settle
  transitions: answer every echo with a same-status `ledger note`
  ("already relayed — no double X"), never a second action. Durable dedup
  (round row + full-sha note written the SAME minute as the dispatch) is
  what silences per-tick re-alerts; when two sensors race (review-sensor
  vs pane-watcher), relay on whichever arrives FIRST and note-only the
  twin. (2026-08-02: three races in one day on PR #563 alone.)
  2026-08-17 addendum (dream-2026-08-17): two new echo flavors —
  (a) the Perkins sensor re-fires on an ALREADY-APPROVED same sha (a
  no-op re-review): classify stale, NO round dispatch; only a NEW sha
  earns a round under the loop ruling (×4 jobs: 5.5 09:13Z, 5.9
  17:13Z, traffic-model r3, doctrine); (b) a DOC-ONLY head move under
  an in-flight round earns NO new round — record the skip-row
  decision at close-out (skip if APPROVED per the #585 precedent;
  superseded by the fix push if CHANGES_REQUESTED — 7.2 08-17,
  executed as written across 3 doc-only commits).
- **Perkins can self-close its round row (2026-08-02).** Closing the
  Perkins pane writes `working -> done` before Silas' close-out
  `set done`, which then no-ops (same-status) and eats the verdict
  detail. Write the verdict as a pre-emptive `ledger note` at close-out
  instead of discovering the loss later. 2026-08-07 addendum: self-close is
  now the NORM (10/10 rounds this window closed clean, 0 lens leftovers) —
  capture the verdict at/before close-out every time. Two new post-failure
  flavors: if Perkins completes the analysis but dies pre-POST, Silas posts
  the review from the complete artifacts (`body.md` + `consolidated.json`) —
  no re-run; if the token mint fails, the review posts via fallback-comment
  automatically. And deepseek rounds self-close the ROW reliably but leave
  the WORKTREE + lens panes behind more than kimi did — always verify +
  sweep worktree / branch / lenses at close-out, don't assume.
  2026-08-09 addenda: NOT uniform — rc3-1's pane closed with the round
  row left at `working` (Silas set done + clear-pane manually): VERIFY
  the row state at close-out, don't assume either direction. The deepseek
  leftover drifted too — 08-08 rounds left NO lens panes (clean
  badge-outs on #590/#591/#594/#595); the new residual is the lingering
  ROUND PANE itself (pHT swept 08-09). Sweep list: worktree / branch /
  round pane / lenses. Token-mint root cause diagnosed: a shell `$?` bug
  (rc3-2 r1) — fallback-comment posts, but APPROVED-by-comment != formal
  approve (branch-protection/review-count semantics differ); the Perkins
  tooling wants a fix task, not just tolerance.
  2026-08-17 addendum (dream-2026-08-17): close-sweeps scope to the
  round's OWN pane ids (from the round row / launch record) — NEVER
  id-proximity or label. Lens tabs share generic labels (near-miss
  08-17 09:15Z: the 5.5-r1 close-loop found 7 same-labeled mm-*-r1
  panes and almost killed the sibling 7.2-r1's 4 IN-FLIGHT lenses —
  relayed STOP; doctrine-r1 held the same line 10:25Z), and
  non-Perkins panes created after a round get ADJACENT ids
  (CONFIRMED KILL 08-17 17:09Z: the 5.9-r1 close-out lens sweep
  killed dream-2026-08-17's sheep panes p1ZZ/p1Z0 — adjacent to lens
  panes p1ZQ–p1ZX; one sheep's shard survived by ~8s, the other died
  mid-turn and was re-dispatched).
- **Serialize-hold for pane capacity: pre-create the round row to dedup the
  sensor (2026-08-07).** When the valve is near capacity, hold the next
  Perkins round behind an in-flight one: pre-create its ledger row (status
  `dispatched`, full sha in the note) so the Perkins sensor doesn't re-fire
  on the tick, then release when another round's close-out frees panes
  (trigger = the in-flight round's close-out). Now standard ops (≥5
  sightings 08-03..08-05) but undocumented. 2026-08-11 addendum: now
  standard CROSS-REPO (RT ↔ PP), not just same-repo pane capacity (≥4
  fresh sightings). The held round's briefing NAMES the in-flight round
  it's behind ("SERIALIZE-HELD behind perkins-v2-1.2-window-draw-pipe-r1")
  and the RELEASE trigger (the in-flight round's close-out); the held pane
  stays dispatched (sensor dedup'd) until release. 2026-08-13 addendum
  (dream-2026-08-13): release triggers now span three kinds — (a) the
  in-flight round's close-out; (b) close-out + CI green; (c)
  verdict-gate OPEN for a held JOB (3.2 released when #30 r1 APPROVED).
  Held-row hygiene at release: RE-VERIFY the head — refresh the row sha
  when the head moved during the hold (3.1 r2: a980194 → abe578b after
  a rebase) and take the fresh sha at release; a dirty base (sibling
  merged mid-hold) = rebase via parked-pane relaunch + relay, not a
  fresh dispatch. 2026-08-17 addendum (dream-2026-08-17;
  7.1-visual-juice): the hold mechanics now cover a plain MINION
  dispatch held behind a merge close-out — PANELESS row (no
  pane/worktree until release), named release trigger on the row
  ("release = the 5.5 MERGE CLOSE-OUT; early dispatch = guaranteed
  rebase collisions on the shared chrome/draw surface"), model field
  + pr_review carried on the row, release = resolve the fresh head
  THEN dispatch (7.1 released @ 388e316 post-#59-merge, fired on
  cue). The 08-16 billing+serialize day also produced a 6-DEEP held
  round chain (refcheck ← terminology ← … ← local-ci) with position
  notes on the rows — all released cleanly.
- **"Moot on merge" is NOT the default for a mid-flight Perkins round
  (2026-08-07).** A normal terminal merge of an APPROVED PR → sweep the
  in-flight round as moot, no re-dispatch. But a DELIBERATE pre-verdict
  merge (user merges to peek) → let r1 continue to verdict on the merged
  sha as an FYI review (NO rework loop unless the user says so; real
  findings become follow-up notes); a fresh post-merge AUDIT round may be
  dispatched (FYI-only, COMMENTED, no cap implication) and its blockers
  become NEW jobs, not rework of the merged PR. When unsure: sweep fast +
  re-dispatch (costs one worktree add). 2026-08-09 addendum: the first
  two clean sightings landed (prototype-build r1 verdict 18 min
  post-merge — 3 blockers incl. 2 headless-reproduced REAL bugs;
  model-flash N-series tracked a day past merge) — and both worked ONLY
  because findings got an explicit routing target (Odin prototype +
  foundation-audit, named follow-up rows). Without a named intake, FYI
  findings evaporate: every FYI/audit close-out names its routing target.
  2026-08-19 addendum (dream-2026-08-19; righttenantry-security-audit,
  user ruling 08-18): the named-intake shape for AUDIT findings is
  ISSUES-FIRST — "create github issues for them first": one fix-now
  issue (RT #625 = M-1) + one batch issue (RT #626 = M-2..M-8 + Low +
  Info), and the fix-now job's briefing is SCOPE-GUARDED against the
  batch items so it cannot eat them (M-1 shipped r1 APPROVED + merged
  as #627 same day). Generalizes to any audit/heist output.
- **A no-PR job (analysis / lavish+md+script deliverables / in-repo commits
  with NO merge) falls through BOTH watchers (2026-08-07).** The pane
  watcher only tracks NON-done jobs — the instant the minion runs `ledger
  set <id> done`, the job becomes done -> untracked -> the pane's
  working->done/idle transition fires NO alert; and the PR watcher has no
  PR/merge to catch. So the completion can go unseen indefinitely. The
  INTENDED durable completion signal for no-PR jobs is the briefing-
  mandated `herdr notification show "<id>" --body "..."` on finish — NOT
  ledger reconciliation, NOT the watchers. Two failure modes to
  distinguish when a no-PR completion slips: (a) NOTIFICATION-SENSOR gap
  — the minion fired the notification but Silas missed it; (b) MINION-
  COMPLIANCE gap — the minion skipped the notification step. VERIFY by
  checking the minion's session jsonl for a `cli:notification:show`
  RESULT (not just the command string in its text) — 0 results = the
  minion didn't execute it (compliance gap). (2026-08-07: righttenantry-
  gcp-cost-analysis — minion CONSTRUCTED `herdr notification show
  "gcp-cost-analysis"` but did NOT execute it [0 cli:notification:show
  results] -> compliance gap; the deliverable still reached the user via
  Gru's independent check, so no harm, but the signal was missed at the
  source.) No-PR jobs must NEVER rely on pane/PR watchers alone.
  2026-08-15 addendum (dream-2026-08-15): BOTH flavors have now been
  seen — bughunt2 was the SENSOR-gap flavor (minion DID fire
  `cli:notification:show` ×2 at 00:22Z, verified in its session jsonl;
  the completion was still unseen for 8.5h and surfaced only via a
  user/Gru relay). The notification alone is NOT sufficient: reconcile
  no-PR non-done rows at every board sweep. Also: PRESERVE no-PR
  deliverables (reports, regression suites) to
  `_bmad-output/implementation-artifacts/` BEFORE the worktree sweep —
  the local-test precedent lost untracked artifacts to the sweep; the
  bughunt suite was swept twice and re-created a 3rd time before
  preservation became standard (08-14/15, ×4 sightings).
  2026-08-19 addendum (dream-2026-08-19; wire-aesthetics): a THIRD gap
  flavor — `herdr notification show` itself returns `shown:false` when
  the notification relay is busy (the ledger + watcher caught it).
  Verify `shown:true` in the result; never assume the fire-and-forget
  landed.
- **A Perkins fix-audit round is HELD on an UNSTABLE review target
  (2026-08-11).** Deferred when the PR head is still MOVING (minion
  iterating CI fixes / active A/B) AND/OR CI is RED — the harness
  verification can't run on a red/unstable CI. Hold for the STABLE sha
  (CI green + r1 blockers addressed + minion done iterating). The review
  sensor RE-FIRES on every new commit while the head moves — those are
  echoes (note-only), not new work. Sibling to serialize-hold (which gates
  on pane/model capacity); this gates on review-TARGET stability.
  2026-08-13 addendum (dream-2026-08-13): CI PENDING ≠ CI RED — the
  hold gates on RED only; a fresh r1 dispatch is OK on 4/5 pass + 1
  pending ("UNSTABLE=pending, not red" — #36 r1 08-13, #28 08-12).
  Treating pending as red needlessly blocks fresh rounds.
- **Perkins round ops: empty-lens standing trigger, push-hold
  discipline, vision caveat (2026-08-18/19, dream-2026-08-19).**
  (a) USER RULING (5.11-terminal-types arc): if acceptance/architecture
  lenses come back 3-byte-empty a THIRD straight generation → INTERVENE
  per the empty-lens doctrine (sweep those lens panes + regenerate) —
  and a g-wave COMPENSATION verdict counts as valid (5.11 r3 delivered
  a valid 7/7 verdict on 51/71 findings; no sweep needed). (b) While a
  round is IN FLIGHT the minion folds LOCALLY and HOLDS the push until
  the verdict posts (5.11 r1-fold 790325a; 7.1 fold d9db462) — the
  pushed fresh head then re-arms the next round as an explicit DELTA
  review (5.11 r2 = rebase-delta), never contamination of the in-flight
  one. (c) On any non-k3 round the briefing carries the VISION CAVEAT
  verbatim: pixel verification MECHANICAL only (byte/hash/capture-
  diff), aesthetic verdicts deferred for the k3 re-check, never faked
  (7.1/5.10/5.11/background-maps briefings, ×6).
- **Perkins-branch anomaly: `perkins-*` BRANCHES where only a DETACHED
  worktree should exist (2026-08-11, audit-flagged).** Perkins rounds use
  DETACHED worktrees (`git worktree add --detach <sha>`; dedup is
  ledger-ROW-based). Yet `perkins-*` branches appeared as merged debris
  (3 branches / 2 repos: perkins-odin-prototype-r1/r2 +
  perkins-refcheck-rc3-3-r1) — a dispatch is using `herdr worktree create
  --branch` (the regular-minion path) where `--detach` is correct, OR a
  Perkins minion created the branch. Harmless when caught (merged +
  recoverable from main; `branch -D`), but a dispatch-mechanics
  inconsistency. **Root cause inferred, not confirmed** — audit target:
  grep dispatch history / Perkins round setups for `--branch` where
  `--detach` was correct.

### Ledger

- **`bin/ledger` table view is lossy.** `ledger` / `ledger all` show only
  `id, status, pane_id, github_issue, started_at, result` — no `pr`,
  `worktree`, `briefing`, etc. Never declare a field "missing" from the
  table view; verify with `ledger show <id>` or `ledger json` first.
  (2026-07-21: Gru falsely reported PRs as unrecorded and wrote redundant
  `ledger pr` entries — they had been set at the `in-review` transition.)
  2026-08-09 addendum: `ledger json` is lossy the OTHER way — it shows
  only NON-DONE jobs (verified: 4 rows, 0 done); done round rows drop
  out — query the DB for those. Perkins round-row ids are
  `<job-id>-perkins-rN`, NOT `perkins-<job>-rN` — a wrong guess breaks
  dedup lookups.
- **`ledger events` takes a count, not a job id.** Per-job event history:
  `ledger show <id>`.
- **`bin/ledger set` refuses same-status transitions** (prints "already
  <status>", writes nothing). For same-status updates use
  `bin/ledger note <id> <text>` — appends a `job_events` row without a
  status change.
- **`ledger set <id> in-review "<url>"` does NOT populate the `pr` field
  (2026-08-07).** `set` updates only `status` + writes the note to an event
  row; the `pr` column is set ONLY by `ledger pr <id> <url>`. So a minion
  that self-reports in-review with the URL in the note leaves `pr` NULL →
  the PR watcher silently skips it. Don't confuse this with the lossy-
  table-view gotcha: VERIFY with `ledger show <id>` first (the table lies),
  and if `pr` is genuinely empty, follow the transition with `ledger pr`.
  (The packet-plumber crew now runs `ledger pr` itself — the lesson
  propagated. 2026-07-21 was the inverse false-positive: Gru wrote
  redundant `ledger pr` on a field that WAS set, read from the table.)
  2026-08-11 addendum: the durable fix is in flight — the briefing
  template now carries an explicit `ledger pr <id> <url>` instruction,
  and the RT + PP crews are starting to run it themselves (rc3-4 #599,
  v2-1.1 #21 "minion set the pr field — 2nd job in a row"). BUT it is
  NOT universal — the RTA crew still produced a NULL `pr` on self-report
  (#173, #597) this window. Silas still VERIFYs `pr` on every in-review
  transition (`ledger show`, not the lossy table); don't relax
  verification just because most crews now self-set it. 2026-08-13
  addendum (dream-2026-08-13): 3 more sightings 08-12/13 (3.2-lane-qos,
  rc1-1-grapheme-fix, rc4-4 #609 — Silas: "SELF-REPORT GAP again: pr
  field NULL on in-review (the RTA-crew pattern)"). The gap is
  crew-level and persistent — Silas verify-and-set on every in-review
  transition remains the only reliable guard. 2026-08-15 addendum
  (dream-2026-08-15): ×3 more this window (refcheck-followup-607,
  v2-4.3 #43, v2-5.3-pause-anywhere #46) — the PP crew REGRESSED after
  the 08-11 "crews self-set it" trend; verify-and-set stays mandatory.
  (The `pr_review` COLUMN, by contrast, was healthy: all 23 code-review
  jobs this window carried 1.)
- **Verify merge/deploy state by commit-containment, never by grepping a
  single file (2026-08-11).** Two false-negative traps: (a) grepping a
  single file for the change gives a FALSE NEGATIVE if you grep the wrong
  file (or the change lives elsewhere) — the RTA #172 vetting was safe to
  re-process but a wrong-file grep said otherwise; (b) checking
  `--merged`/ancestry BEFORE pulling lies — a stale local base predates
  the merge. Use `git merge-base --is-ancestor <commit> <branch>` AFTER
  `pull --ff-only` (or `git fetch origin <base>:<base>` when the tree is
  held). Commit-containment is immune to both traps.
- **Minions can SELF-CREATE ledger rows — wrong-id phantoms +
  missing-fields flavors (2026-08-14, ×2).** `refcheck-followup-607`
  (repo prefix dropped) ran 19h as a DUPLICATE of the canonical
  `righttenantry-refcheck-followup-607` row, feeding the PR watcher
  post-merge; `bundle-reprice-pin` self-created with missing fields
  (Silas filled pane/tab/worktree/briefing). When a watcher re-fires on
  a merged PR or a job seems untracked, check for a minion-created
  phantom row — reconcile to ONE canonical id.
  2026-08-17 addendum (dream-2026-08-17; the 5.5 job row + 5.5-r1
  round row — ×2): re-dispatching a DONE job id is a row RESET
  (UNIQUE conflict on add) — NULL the stale `pr` field FIRST (a stale
  #44 would have tripped the PR watcher at in-review), update
  worktree/pane/tab/model, clear result, and OVERWRITE the note
  column — a reset leaves the OLD round's note text
  ("sha=23e1704… v4-pro") describing the superseded round.
  2026-08-19 addendum (dream-2026-08-19; v2-6.2-advance-trigger-
  perkins-r1): the self-create class is still live — the round row
  self-created at `working` with pane/tab/worktree/model/pr EMPTY
  (Silas filled post-hoc). Verify-and-fill on every round row stays
  the guard.
- **Durable routing lives on ledger rows, not in agent context
  (2026-08-14/15, ×3 + one full fire cycle).** QUEUE / BATCHED /
  RESPAWN-TRIGGER decisions are written as notes on the OWNING row
  (even done rows) so they survive session restarts and context
  turnover — the #618-merge respawn trigger fired exactly as written
  across a Silas restart (verification-rerun dispatched 08-14 18:55Z);
  #621's "rides the next RT batch" ruling and the 5.2 visibility-queue
  note ride their rows the same way.

### Pane forensics

- **An `idle` pane can hide a DEAD pi.** `herdr agent list` showed
  agent=pi, status=idle while no session file existed and pane reads
  returned empty — the process died silently after launch. Verify via
  the session file (`ls ~/.pi/agent/sessions/<slug-dir>/`), then
  relaunch (`herdr pane run <pane> "pi"`), wait idle, re-hand over.
  (2026-07-30/31: hit twice — game-brief, form-completion-ps.)
- **An `idle` pane can also hide a LIVE pi whose turn died on the
  provider.** 2026-08-01 (righttenantry-form-funnel-w0): the kimi-coding
  stream returned `terminated` mid-rework at 02:01, 3 retries, turn
  errored out — pi stayed alive, the pane showed `idle`, and nobody
  noticed for 7.5h. Unlike the DEAD-pi case, the fix is one word —
  `herdr pane run <pane> "continue"` — with ~zero context loss (the
  session jsonl even keeps the terminated thinking block). Before acting
  on an idle-mid-task pane: tail its session jsonl for
  `stopReason:"error"` / `errorMessage` — errored-turn → `continue`;
  no session file/process → relaunch. 2026-08-17 addendum
  (dream-2026-08-17; v2-5.2-node-health, verified 08-15 + 08-16 — ×2
  days): the INVERSE trap — an 18-20h minion is not automatically a
  stall: 5.2's ~20h was REAL DESIGN WORK (probed the sim, chose the
  stuck-pile measure SHARED with 4.1 — coherence over invention).
  Verify session-file mtime/toolUse GROWTH before classifying; the
  check precedes any continue/revive reflex.
- **Ground truth for pane forensics is the session jsonl, not env
  scraping (2026-08-01/03).** The bash tool's env is NOT a proxy for a
  pane's pi process env (PI_GRU/PI_SILAS are invisible to it). Which
  extensions are armed = the jsonl's entry types (`custom_message` =
  extension-injected; `message` role=user = typed). A worktree's session
  dir holds the minion's AND its mega-minions' sessions (shared cwd) —
  identify the live pane's file via `herdr pane get <pane>` agent_session,
  never by newest mtime.
- **Killing a stuck / 403-dead pi: typed `exit` fails, C-c isn't uniform
  (2026-08-07).** `exit` typed into a dead pi does nothing; C-c sometimes
  leaves the TUI alive. Reliable path: `herdr pane process-info --pane <p>`
  → `kill <pid>` (the `node` pid) from bash → the pane drops to a shell;
  then verify the session-file state before relaunching. (Seen across the
  2026-08-04 quota-403 + glm dead-pane sweep.)

### Extensions

- **A raw backtick in an extension's template literal kills the whole
  extension at load** (ParseError — the pane boots to a dead prompt with
  only "Failed to load extension" on screen). STANDING_ORDERS strings in
  gru.ts/silas.ts are template literals: escape every inline `code` span
  as \\`. (2026-08-01: Silas' first launch died on gru.ts:41 — four
  unescaped pairs.) Sibling (2026-08-13 relay slip, dream-2026-08-15):
  backticks inside a DOUBLE-QUOTED `herdr pane run` payload are eaten
  by bash command substitution — the relay arrives with blank code
  spans and a corrupted recipe. Single-quote the whole payload or drop
  the backticks. (Class promotion: 1 direct sighting + the 08-01
  template-literal sibling — same hazard, second surface.)
- **Pane ids: never manually retype or `$(...)` subshell them — pipe the
  move/create output to a variable and use it literally (2026-08-08).** A
  mistyped `pane_id` in `ledger add` (pHE vs pH6, pHK vs pH7) makes the
  pane watcher track a wrong/phantom pane -> a false `gone -> idle` alert
  later; the real minion is fine. FIX via `sqlite3 ... UPDATE jobs SET
  pane_id='<real>' [tab_id='<real>'] WHERE id='<job>'`. PATTERN that
  stops it: `PANE=$(herdr pane move ... --json | python3 -c
  "import sys,json; print(json.load(sys.stdin)['result']['move_result']
  ['pane']['pane_id'])")` then `pane_id=$PANE tab_id=$TAB` in the ledger
  add — never hand-type the id. 5 slips in one session (2026-08-08).
  2026-08-09 addenda: a 6th slip happened the same day, AFTER the gotcha
  was written — documentation alone doesn't stop the slip; the
  variable-capture habit is the only fix. The rule covers JOB ids too (a
  hand-typed phantom `perkins-<job>-r1` event id lives in the stream
  forever). New race: right after a move to a NEW tab, `herdr agent list`
  lags a beat (StopIteration) — get tab_id from `herdr tab list` by
  label. And a mangled move-output subshell caused a DUPLICATE worktree
  create — capture once, never re-parse. 2026-08-13 addendum
  (dream-2026-08-13): a workspace MOVE mutates the pane id (w4T:p1 →
  w1T:pXM — the pre-move id becomes a phantom the watcher chases) —
  re-capture the id post-move and correct the ledger row (×5 on
  08-12/13: pXM, pZ8, pZD, p0V, p16W). herdr JSON parse keys: split
  result = `result.pane` (NOT split_result); move's tab =
  `move_result.created_tab` — wrong keys leave orphan panes (pWH,
  08-12). 2026-08-15 clarification (dream-2026-08-15): PLAIN tab moves
  do NOT mutate pane ids (08-14 tAX decongestion moved 10 mega-minions
  across tabs, zero ledger corrections needed) — only WORKSPACE moves
  do; don't over-correct after a tab move.
  2026-08-19 addendum (dream-2026-08-19; demo-mode-perkins-r4 +
  7.3-perkins-r1 — ×2): herdr 0.8.0 `tab create --cwd <dir>` does NOT
  pin the workspace — the r4 tab landed in a stray leftover workspace
  (w6H) and needed a move; the 08-18 "--cwd lands directly in w1T"
  observation does NOT hold on 0.8.0. Pass `--workspace` EXPLICITLY on
  tab create; the 0.8.0 tab-create JSON returns the new pane under
  `root_pane`.

- **Never guess review-URL anchor ids (2026-08-11, ×2 sightings).** A
  guessed anchor id writes a WRONG review URL into the permanent ledger
  (the review-sensor alert gives the id, pane-done alerts don't).
  Fetch it: `gh api repos/<owner>/<repo>/pulls/<n>/reviews --jq
  '.[-1].id'` — first, never guess. 2026-08-15 addendum
  (dream-2026-08-15): self-close EVENT notes truncate the review anchor
  (`#pullrequestreview-` / `-1`) — the recovered-as-note verdict written
  at close-out carries the real id; never read the URL off the
  self-close event (×2: qos-panel 5.8, readability-assist).

- **`pr_review` is a LEDGER KEY, not a note string (2026-08-12, ~11h of sensor blindness).** The Perkins sensor's gate is `job.pr_review === 1` read from the COLUMN. Writing "pr_review 1" into the `ledger add` note leaves the column at its 0 default and the review-sensor silently skips the job — 5 jobs blind (~11h: 3.3/3.4/4.1/rc1-1/rc4-3/rc4-4/4.2, every Perkins round in that window was a manual/held dispatch; only 3.2 fired because its row was SQL-fixed at 12:16Z). ALWAYS pass `pr_review=<n>` as an add-key when the briefing mandates it. VERIFY the column after add (`sqlite3 ... SELECT pr_review`), don't trust the note. Sensor-down fallback: at every minion completion/settle, sweep in-review pr_review=1 jobs — no round row carrying the current head sha + head stable → dispatch manually, never wait on the sensor.
  2026-08-13 addendum (dream-2026-08-13): manual/held dispatch is what
  MASKED the ~11h outage (everything ran manually, so the dead sensor
  was invisible — the only auto-fired round was the one SQL-fixed row).
  The sweep fallback executed cold on 08-13 (rc4-4 #609 r1 dispatched
  proactively at 13:50Z: head stable + no round row) — PROVEN; keep
  sweeping at every completion/settle, never trust the sensor alone.
- **Vision is explicit + local by doctrine (2026-08-18,
  dream-2026-08-19).** NO silent auto-delegation: vision.json's silent
  lmstudio fallback ran 15+ invisible delegations in one day under a
  lying log identity (deleted same day). Vision reads route explicitly
  to `lmstudio/qwen3.8-27b-mlx@4bit` via `bin/vision-read` (user
  test-ruled: decisively more accurate; ~2-3.5 min/image — an empty
  reply mid-reasoning ≠ failure). pi gates image attachment on the
  model's declared `input` types — any local-model registration in
  models.json needs `input: ["text","image"]` or the tool silently
  degrades.

## Orchestration upgrades (user-approved 2026-08-18)

- **Quota probe (P1):** `bin/quota-probe [model]` — env-cleared pi probe of
  the reasoning provider, writes `_bmad-output/memory/quota-regime.json`.
  Silas runs it BEFORE every Perkins-round/dream dispatch + hourly under
  heavy use (the nefario-watch staged tick does the hourly half); the
  regime file is the record — no more 403 surprises. Probe-FLIP injects
  one line.
- **Lens-spawn rooting (P1):** the code-review skill's headless spawn
  template pins `--cwd <worktree>` on the lens tab FOREVER (the 08-18
  mis-rooted-lens class: a wave created without --cwd rooted at the
  orchestrator root — Gru-contamination + dead panes). A lens pane whose
  cwd is not the round worktree is mis-rooted: close + relaunch.
  FIRST FIRE 08-18 (5.11-terminal-types r1): an 8-pane lens wave landed
  at the orchestrator root — user-flagged; all 8 closed,
  relaunch-with-`--cwd` relayed, one idle root pi swept, zero harm.
- **GitHub-status sensor (P1):** nefario-watch ticks status.json; on an
  incident it injects the auto-classification advisory ONCE (API/webhook
  flakes = incident noise, note-only; git green; merges user-side via the
  CLI-merge recipe) + a cleared line. Staged in the extension — active
  after the next Silas relaunch.
- **Trigger graph (P2):** `blocked_by` (comma-separated, AND semantics) +
  `coordinate_with` (parallel handshake, never blocks) columns; `ledger
  queue` shows the hold list + READY SET; auto-release check at EVERY
  close-out (release = resolve the fresh head, then dispatch).
  Verified in production 08-18/19: `blocked_by` release fired (5.12 ←
  5.11-types done, 23:26Z); the deferred registry auto-surfaced the
  parked security-audit at the 12:48Z probe-flip (`deferred:glm` lifted
  → resumed — the durable RESUME-TRIGGER row note rode the park);
  `coordinate_with` exercised in the #67 rebase handshake
  (background-maps ↔ 5.11). Ops: graph keys are NOT `ledger add` keys
  — set via sqlite3 UPDATE post-add; a `ledger queue` DEFERRED READY
  SET line can echo stale after a resume (note-only).
- **Sensor-doctrine sync (P2, standing rule):** ANY doctrine amendment
  task must grep the sensor/watcher configs (`.pi/extensions/*.ts`) for
  the retired doctrine being amended — the cap-3 echo class lived in
  nefario-watch.ts after the playbook retired it (fixed 08-18).
- **Ledger guard (P2):** `ledger set <id> in-review` refuses without a PR
  URL (in the note or via `ledger pr` first) — kills the NULL-pr
  self-report class.
- **Playbook consolidation (P3):** rides the NEXT dream (Model policy +
  Perkins sections rewrite; supersede history → changelog appendix).
