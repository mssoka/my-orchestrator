# sheep-journals findings — dream-2026-08-09

Sources read: gru-journal/2026-08-08.md (1 entry), silas-journal/2026-08-08.md
(56 entries, whole), silas-journal/2026-08-07.md (38 entries; harvested the
~31 post-marker ones, 11:43Z dream close-out treated as borderline-at-marker).

## Candidate patterns

### Fresh-minion-per-story beats bmad-dev-auto for learning-driven sprints (USER DECISION)
- Sightings: gru 2026-08-08 (only entry) — "the fresh-minion-per-story pattern
  is what feeds the learning/memory loop… The auto-loop would churn through
  stories efficiently but skip the learning". Sprint execution = Gru manual
  dispatch, one fresh minion per story (create-story → dev-story, one PR each);
  bmad-dev-auto reserved for mechanical work / fun-test prototypes where
  per-story learning isn't the goal ("the FinLit pattern; RT follows the same").
- Why it matters: this is a standing user ruling on how ALL product sprints
  are orchestrated; any future "just loop dev-auto" instinct contradicts it.
- Already in memory? No. (Playbook may not have it either — check.)

### Transient "blocked" alerts self-recover — classify by transcript + pane age before acting
- Sightings: silas-08-08 01:5xZ — THREE blocked alerts (light-cascade,
  blender-art, prototype, all >5.5h old) = "TRANSIENT cache-miss/rebill
  noise… 'Cache miss after ~330m idle -> re-billed'… recovered to working.
  NOT real blockers" (~884k tokens re-billed, cost spike not ops-actionable);
  silas-08-08 12:04Z — rc2-3 blocked at ~2.3h old = "a brief pi/provider
  stall, recovered cleanly", PR opened 17 min later, no action.
- Rule Silas derived: a `blocked` alert on a >5h minion with a "Cache miss
  after Xm idle" line = transient cache-expiry; read the transcript first;
  they recover to working on their own. Distinct from the errored-turn class
  (stopReason:"error" → needs `continue`) — these need NOTHING.
- Why it matters: prevents false escalations + useless `continue` spam; the
  cache-miss variant also explains sudden token cost spikes.
- Already in memory? Partially: the provider-incidents gotcha covers
  errored-turn classes needing `continue`; the self-recovering blocked-alert
  class (and the >5h cache-miss signature) is NOT there.

### `/model <provider>/<model>` switches a RUNNING pi mid-session, preserving context
- Sightings: silas-08-08 23:1xZ (odin-architecture model saga) — "Sent
  `/model kimi-coding/k3` to the RUNNING pi -> the pi SWITCHED the model
  MID-SESSION preserving context… NO kill, no relaunch, no loss. (Big
  unlock: model corrections don't have to restart a minion.)"
- Why it matters: model mis-dispatches are fixable in place; kills the
  kill-and-relaunch reflex (which loses context/work).
- Already in memory? No.

### Provider-name ≠ model: `kimi-coding` is a PROVIDER, the model label is `kimi-coding/k3`
- Sightings: silas-08-08 23:1xZ — "bare label 'kimi-coding' -> FAILED (pane
  died: 'kimi-coding' is a PROVIDER with a key in auth.json, NOT a model)";
  same entry: `moonshotai/kimi-k3` "WRONG PROVIDER (routed via openrouter,
  not the direct kimi-coding provider)"; user correction: use
  `kimi-coding/k3`. Sibling of the glm-5.2 bare-label bug (in store
  2026-08-04) — same failure shape, different provider.
- Also: silas-08-08 23:5xZ — pi's defaultProvider is now kimi-coding
  (settings.json), so unset-model dispatches resolve to kimi-coding/k3
  ("unset-model dispatches now default to kimi for coding"). Flip side of
  the in-store `PI_MODEL` env-override gotcha: know what UNSET resolves to.
- Why it matters: two dispatch labels that LOOK right both fail/misroute;
  only the direct provider's `provider/model` path works.
- Already in memory? Partially: glm-5.2 bare-label entry exists (field-notes
  + AGENTS.md 4th-incident-class addendum); the provider-name-as-label class
  and the defaultProvider resolution are new.

### Model walls: don't stall a dispatch on a walled model — launch on the proven fallback + flag
- Sightings: silas-08-08 20:5xZ — kimi walled until 21:57Z, odin-architecture
  launched on deepseek "to avoid a 1h stall on this substantial deliverable;
  flagged to Gru (re-run on kimi after the wall if preferred)"; 21:0xZ — Gru
  ratified it as a directive ("deepseek for docs, kimi for code after the
  wall"); 23:1xZ — user then overrode mid-run ("kimi for ALL coding" → killed
  the deepseek run, re-dispatched post-wall).
- Why it matters: model preference is negotiable against latency, but the
  override + flag path (and accepting a user reversal mid-run) is the ops
  pattern, not an ad-hoc call.
- Already in memory? No.

### Pane-id gotcha needs a HABIT change, not just documentation (+ tab_id races)
- Sightings: silas-08-08 23:4xZ — "I JUST recorded the gotcha… and slipped
  IMMEDIATELY after… the gotcha alone doesn't stop the slip — I must actually
  CHANGE the pattern" (6th slip, pHQ vs pHP, fixed via sqlite); 20:26Z —
  move subshell mangling caused a DUPLICATE worktree create attempt (new
  failure mode); 23:5xZ + 00:21Z(Aug 9) — variable-capture pattern WORKS,
  but "the tab query raced (StopIteration on the not-yet-registered agent
  list) -> got tab_id from `herdr tab list` by label… the agent list lags a
  beat after a new-tab move."
- Why it matters: confirms the stored gotcha isn't self-enforcing; adds the
  tab-list-by-label fallback as part of the working pattern.
- Already in memory? Yes (AGENTS.md Extensions, 2026-08-08, "5 slips").
  Needs amendment: 6th slip post-documentation, habit-change note, tab_id
  race + fallback.

### `herdr tab create` also has no --json flag (prints JSON anyway)
- Sightings: silas-08-08 11:46Z(Aug 9 entry) — "herdr tab create takes NO
  --json flag but prints JSON anyway — parse stdout".
- Why it matters: sibling of the stored `pane move` gotcha; same parse-stdout
  rule applies to tab create.
- Already in memory? Partially: pane-move variant stored; tab-create not.

### Occupied working tree at close-out: `git fetch origin <base>:<base>` (no checkout)
- Sightings: silas-08-07 20:56Z — "close-out's `pull --ff-only` can't run
  there — use `git fetch origin <base>:<base>` to update the local base ref
  without switching the working tree"; silas-08-08 00:46Z, 09:34Z, 11:44Z —
  reused 3× for packet-plumber main ("main tree occupied by the prototype
  minion"). DIFFERENT DAYS (08-07 + 08-08), 4+ applications.
- Why it matters: in-repo close-outs while a sibling minion holds the tree
  are routine; this is THE canonical sync move for them.
- Already in memory? No. (Complements the 2026-08-07 in-repo follow-up
  gotcha, which doesn't cover the sync mechanics.)

### New dead-agent class: the PANE VANISHES (not idle, not errored) → relaunch + sqlite re-point
- Sightings: silas-08-07 00:0xZ(Aug 8) — rc2-2 pane w1T:pF1 "no longer has a
  detected agent", `herdr pane get` = None, session tail plain (no
  stopReason:error) = "terminal/pi crash (dead-pane class), NOT
  continue-revivable -> relaunch in a new pane + re-point the ledger pane_id
  (sqlite UPDATE; CLI has no set-pane)". Recovery confirmed working.
- Why it matters: third pane-forensics class alongside DEAD-pi (no session
  file) and LIVE-pi-errored (continue); each has a different recovery.
  Also establishes "CLI has no set-pane → sqlite UPDATE" as the re-point
  tool (same fallback used for pane-id slips).
- Already in memory? Partially: pane-forensics section has the two other
  classes; the vanished-pane class + sqlite re-point are not recorded.

### Boot-transition watcher noise: `gone -> idle (ledger dispatched)` on fresh dispatches
- Sightings: silas-08-08 23:45Z — rc3-2 pane "registering as a pi agent at
  boot (gone/shell -> idle/pi), captured by the watcher's poll before the
  minion self-reported working… Same boot-transition pattern as
  agent-model-flash, per-applicant-remind, prototype-iterate-1. No action."
  (4 sightings named, spanning 08-06..08-08.)
- Why it matters: another settle-noise sibling to classify away; a fresh
  dispatch's first alert is usually the boot, not a problem.
- Already in memory? Partially: the settle-transitions gotcha covers
  done/working -> idle noise; the boot-transition gone -> idle class on
  NEW dispatches isn't spelled out.

### Lens-guards in Perkins briefings hold across rounds (validated at scale)
- Sightings: silas-08-07 18:43Z (#586 r1 "Lens-guard held"), 20:06Z (r2 held,
  deferred W2 not flagged); silas-08-08 00:59Z (#590 r1 "lens-guard held…
  it's a genuine AC4 violation, not a deliberate-decision false-positive"),
  08:29Z (r3, 1 blind-lens FP rejected), 18:36Z (#591 r2 held), 23:36Z
  (#594 r1 "all 4 lens-guards held"). DIFFERENT DAYS, ~6 rounds.
- Pattern: name the deliberate decisions as DON'T-FLAG in the round briefing;
  Perkins then spends its findings on real gaps (rc2-2's missing leaderboard
  viewed-arm, rc2-3's test-gate hole) instead of relitigating intent.
- Why it matters: this is the practice that keeps Perkins signal high as
  round count scales (13 rounds in one session); worth stating as doctrine,
  not just habit.
- Already in memory? No (the playbook's Perkins section has ops patterns;
  lens-guard-as-standard-briefing-content isn't in the store copies).

### Perkins round-row naming + `bin/ledger json` only shows non-done jobs
- Sightings: silas-08-08 07:11Z(Aug 9) — "Round-row naming: <job>-perkins-r1
  (e.g. righttenantry-refcheck-rc3-2-perkins-r1), NOT perkins-<job>-r1.
  bin/ledger json shows only non-done jobs (the done round rows drop out —
  query the DB for them)"; ~09:1xZ(Aug 9) — leftover Perkins round pane
  w1T:pHT "self-closed its row but lingered" → swept at reconcile.
- Why it matters: wrong row-name guesses break dedup lookups; trusting
  `ledger json` for done rounds loses them (extends the lossy-table gotcha
  from the table view to the json view).
- Already in memory? Partially: lossy-table-view gotcha exists; the
  json-view variant + row naming convention + lingering round PANE
  (vs worktree/lenses) are new.

### lavish-default rule: lavish gates big visual/creative deliverables, NOT targeted edits
- Sightings: silas-08-07 20:1xZ/20:2xZ — perkins-ops-codify parked ~7h
  asking lavish-vs-direct on an optional-lavish briefing; Gru: "a minion
  should DEFAULT to direct PR for targeted edits and only lavish when the
  deliverable is big/visual… future briefings [say] 'lavish not needed, PR
  directly'"; 20:50Z — narrative minion lavish-gated correctly on a
  mandated creative deliverable ("the lavish-default rule held");
  silas-08-08 00:5xZ — art-direction-amend dispatched direct-PR per the
  rule ("targeted doc edits PR directly, no lavish halt").
- Why it matters: 'lavish optional' phrasing causes multi-hour ambiguity
  halts; the rule + explicit briefing phrasing eliminates them. Silas
  flagged it "worth codifying (future dream candidate)" — this is that.
- Already in memory? No. (AGENTS.md root says DOCS get lavish review before
  PR — the targeted-edit exemption refines it.)

### Cross-job impact = flag to Gru/Silas, never act across the boundary; relay loop converges canon
- Sightings: silas-08-07 21:12Z/21:2xZ — art-direction minion flagged the
  prototype's packet_types.json color mismatch "in PR, not committed (out of
  scope)"; Silas relayed → prototype applied it (owns the file); silas-08-08
  08:15Z/08:2xZ — blender-art's A1-A7 trail richer than light-cascade's
  scope → Silas coordination flag → Gru scope-expansion relay → "the canon
  reconciliation now captures everything". DIFFERENT DAYS, same loop.
- Why it matters: the two-layer relay (minion flags, Silas surfaces, Gru
  relays scope) is how multi-minion canon stays consistent without minions
  editing each other's files.
- Already in memory? No.

### Creative-iteration loop: render → user reacts → relay → re-render; `continue` on the approved default is safe
- Sightings: silas-08-07 00:21Z(Aug 8) — minion stated intent to proceed on
  approved option (a) but its turn ended; Silas sent `continue` = "honoring
  the minion's own committed plan on the approved default, not a Silas
  content decision"; 00:3xZ — user then redirected to buildings: "the
  renders gave them something to react to. The continue kept the minion
  productive while the user reviewed… No regret on the judgment call";
  00:4xZ — "the minion renders options -> user reacts -> Silas relays the
  refinement -> minion re-renders. The canon converges visually."
- Why it matters: long creative jobs stall at every turn boundary awaiting
  input; this legitimizes `continue` when the minion already committed to
  the user-approved default, keeping the loop hot.
- Already in memory? No.

### Verify the target exists on the base branch BEFORE dispatching an audit/review
- Sightings: silas-08-08 13:0xZ — foundation-audit "dispatched off
  origin/main which has NO game code (the prototype S0-S4 is stranded on the
  local packet-plumber-prototype-build branch). RECALL was TRIVIAL — the pi
  was NEVER launched (the HOLD landed before the chained launch)… verify the
  branch is merged — or dispatch off the BRANCH (not main)."
- Why it matters: an audit of absent code is a wasted round; and HOLD-before-
  launch makes recalls zero-cost (dispatch = worktree+move+ledger, launch
  LAST).
- Already in memory? No. (Adjacent to briefing-can-be-stale, but this is a
  dispatch-precondition check.)

### Don't flip ops process on an ambiguous user remark — confirm first (the MISREAD calibration)
- Sightings: silas-08-07 16:0xZ + CORRECTION entry — user said "i merged
  it.. i should wait for normal trigger"; Silas journaled it as a process
  directive (stop gh-polling), then reversed: "It was the USER reflecting on
  THEIR OWN process… NOT an instruction to Silas. The user explicitly
  GREENLIT my normal process INCLUDING proactive gh-verification."
- Why it matters: a misread "directive" nearly changed merge-detection ops
  session-wide; ambiguous user chat needs a confirm before process flips.
- Already in memory? Partially: the 2026-08-03 provenance entry covers
  user-talks-in-minion-pane verification; the self-reflection-misread flavor
  (in Gru's own pane) is new.

### Orchestrator-root jobs must run in WORKTREES (root tree is Gru+Silas' live home)
- Sightings: silas-08-07 12:0xZ — both UA follow-ups deviated from "no
  worktree" briefings to worktrees: "a pi at cwd=/Users/moses/code IS Gru…
  an in-repo branch switch would move the root's HEAD under them" (Gru p1 +
  silas pCS LIVE in the root).
- Why it matters: the in-repo-follow-up gotcha (2026-08-07, in store) says
  in-repo is fine for REPOS with a free tree; the orchestrator root is the
  permanent exception — its tree is never free.
- Already in memory? Partially: cwd-gate gotcha covers pseudo-Gru; the
  worktree-mandate-for-root-jobs operational rule isn't stated.

### Dream auto-apply guard: grep the store for concurrent live edits before copying store → live
- Sightings: silas-08-07 11:43Z (BORDERLINE — the marker entry itself) —
  "applying dream autos via store-copy -> live is safe IF you verify the
  store is current with any concurrent live edits first (grep your own
  recent gotchas in the store); blind copy can clobber. The diff-check
  before copy is the guard." Verified-in-practice: post-copy grep confirmed
  Silas' session gotchas survived.
- Why it matters: this is the close-out procedure for EVERY dream pass
  (including today's); without the check, a same-day Silas gotcha can be
  clobbered by a stale store copy.
- Already in memory? No.

### Enum/status additions: grep the WHOLE tree for string→enum maps, not just the domain module
- Sightings: silas-08-08 01:5xZ (rc2-2 minion lesson) — "status-enum
  additions must grep the WHOLE server tree for case row.status /
  string->enum maps, not just the application module (r1 B1 was a third copy
  in vacancy/application_list_handler that the r1 grep missed)"; corroborated
  by 00:59Z (the B1 itself: leaderboard handler had no 'viewed' arm → coerced
  to Submitted).
- Why it matters: minion-level implementation lesson; duplicated decode sites
  are the recurring defect class when extending enums.
- Already in memory? No (specific to RT but generalizes to any multi-site
  codec).

## Singletons (interesting but seen once)

- silas-08-08 00:4xZ(Aug 9): toolchain pre-flight for new-stack dispatches —
  Odin + raylib absent on the host; Silas `brew install odin raylib` BEFORE
  the minion builds ("The minion builds on a ready toolchain"). Check
  toolchain presence at dispatch time for first-of-kind stacks.
- silas-08-07 23:56Z: BlenderMCP trap — `bpy.ops.wm.read_factory_settings()`
  with the addon loaded KILLS the :9876 listener (deadlock; needs user
  addon-toggle); clear scenes via `bpy.data.objects.remove` loop + purge.
  Silas: "Will bite any future Blender-MCP job — worth a durable record."
  (Also: Blender 5.2 dropped Eevee bloom → Compositor Glare node.)
- silas-08-07 11:43Z: Gru-journal-gap flag — Gru had NO journal 08-03..08-07;
  dream passes should flag identity-journal gaps (they starve the journal
  sheep).
- silas-08-08 15:24Z: Perkins on a full-prototype-sized diff — "headless
  mode chunks it". Informational; large-diff rounds are chunkable.
- silas-08-08 19:42Z: Godot movie-mode screenshots on macOS hit compositor
  gotchas (minion noted; details in the prototype-iterate-1 shard, not the
  journal).
- silas-08-08 12:40Z: minion caught Gru's briefing typo ('RTenTRY' vs canon
  'RTenantry'), corrected globally + force-pushed BEFORE the PR opened —
  briefing-can-be-wrong (P3, in store) working as intended; also rc2-3
  12:04Z ("briefing's ADD VALUE 'skipped' was STALE — verified on disk
  first"). Two more P3 corroborations.
- silas-08-07 17:56Z→18:16Z(08-08): conflict sensor caught PR #593 DIRTY
  after same-doc amend #592 merged first; rebase + force-push-with-lease
  relayed → merged. "The exact scenario it was built for." Sensor validated
  end-to-end once.
- silas-08-08 07:11Z(Aug 9): token-mint hiccup (shell $? bug) → review
  posted as fallback-comment, not formal approve — corroborates the stored
  token-mint-failure addendum.

## Stale/contradicted memory candidates (with where)

- AGENTS.md gotcha "Perkins can self-close its round row… deepseek rounds
  self-close the ROW reliably but leave the WORKTREE + lens panes behind
  more than kimi did": NOT contradicted but drifting — on 08-08 all deepseek
  rounds closed with "NO lens panes left (clean badge-out)" (r1/r2/r3 #590,
  r2 #591, r1 #594, r1 #595); the new residual is the lingering ROUND PANE
  itself (w1T:pHT swept 09:1xZ Aug 9), not lens panes. Worth rewording the
  sweep list to "worktree / branch / round pane / lenses".
- AGENTS.md gotcha "`herdr pane move` has no `--json` flag": CONFIRMED and
  now EXTENDED — `herdr tab create` behaves the same (silas-08-08 11:46Z).
  Merge the two.
- Field-notes glm-5.2 bare-label entry + AGENTS.md 4th-incident-class:
  extended by the kimi-coding saga — the general rule is "only a
  provider-qualified `provider/model` path that matches an AUTHED provider
  works; bare labels and wrong-provider paths both fail" (bare kimi-coding =
  provider-not-model; moonshotai/kimi-k3 = routes via openrouter).
- No outright contradictions found. The "in-review = wait for the sensor,
  don't poll" idea was self-corrected within the 08-07 journal (MISREAD
  entry) and never reached memory — good.
