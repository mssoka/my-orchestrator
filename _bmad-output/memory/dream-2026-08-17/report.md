# Dream report — 2026-08-17

Material: 13 shards, 4 journal entries (gru 08-16 + 08-17, silas 08-16 +
08-17, plus post-marker tails of gru 08-14 + silas 08-15), 272 ledger events
across 33 job ids (15 minion/dream rows + 18 Perkins round rows), since
2026-08-15T17:01:46Z.

Ops incident during the pass: the 5.9-r1 close-out lens sweep (~17:09–17:14Z)
killed two of Bob's sheep panes (p1ZZ sheep-shards, p1Z0 sheep-ledger-events)
— pane ids adjacent to the round's lens panes p1ZQ–p1ZX. sheep-shards' output
survived (written 17:09:20Z, ~8s before the kill); sheep-ledger-events died
mid-turn and was re-dispatched (p102) at no data loss. This incident is
itself the confirming sighting for P7.

## Proposals

### P1 — Worktree trap: `repo_root` param misleads; pin the worktree path once
- Target: `docs/minion-field-notes.md` (addendum to the 2026-08-07 worktree
  entry) · Class: auto
- Change: append — the briefing's `repo_root` names the MAIN checkout and
  reads like a work path (treat as repo identity); pin the worktree path once
  after the pwd/branch check and use it for every file-tool path AND every
  bash `cd`; recovery = cp byte-identical into the worktree, cmp-verify,
  rebuild + gates there, restore main.
- Evidence: packet-plumber-v2-5.4-input-parity (08-16, "I edited the MAIN
  checkout via absolute paths while dispatched to the worktree"),
  v2-7.2-audio-juice (08-17, "the briefing's repo_root param reads like a
  work path" — did the whole job at the main checkout).
- Reasoning: 4th/5th sightings of the codified trap with a NEW trigger
  (param naming); the ledger's own `repo_root` display normalizes the wrong
  path.

### P2 — Multi-edit batches: duplicate oldText kills the batch; re-grep after
- Target: `docs/minion-field-notes.md` (addendum to the 2026-08-03 atomicity
  entry) · Class: auto
- Change: append — a DUPLICATE oldText in one batch fails the whole batch
  silently (dedupe targets); after any multi-edit re-grep every hunk to
  confirm it landed.
- Evidence: packet-plumber-surge-explainer (08-15, "a duplicate oldText …
  fails the WHOLE batch silently"), v2-5.9-demand-caps (08-16, "ONE ambiguous
  oldText rejected all 5 edits — I debugged phantom behavior for a round").
- Reasoning: the codified entry covers stale/old-text mismatch; the
  duplicate-target and post-batch verify-grep flavors recurred twice this
  window and cost a full debugging round.

### P3 — Vacuous-green pins: guard the silently-not-happening precondition
- Target: `docs/minion-field-notes.md` (addendum to the 2026-08-13 "reported
  success LIES" entry) · Class: auto
- Change: append — any assertion whose precondition can silently not-happen
  is vacuous: draw-to-nonexistent-id silently rejected (guard
  `!replay_error` + verify spawn-return ids), Odin `make([dynamic]T,0,N)` has
  LENGTH 0, re-shaped pins must be mutation-proven ("a pin that can't fail
  isn't a pin").
- Evidence: ×6 shards — v2-5.2-node-health, v2-5.4-input-parity ("deleting
  `&& !esc_cancelled` passed 20/20"), v2-5.5-demolish-input, v2-5.9-demand-caps
  ("the W5 transit pin passed VACUOUSLY"), v2-visibility, local-ci-suite.
- Reasoning: strongest cross-shard signal of the window; bridges the
  negative-control and observable-effect entries with the concrete API traps.

### P4 — Gate-harness false greens (new tooling-trap entry)
- Target: `docs/minion-field-notes.md` (new bullet, Tooling traps) ·
  Class: auto
- Change: new entry — derive gate counts from the list length never a literal
  (the 9th local-CI gate was unreachable for a full review round);
  missing-binary/bad-arg paths must exit nonzero under `!` (the 127→`!`→0
  false-green); assert the produced artifact, never just the rc; Dockerfile
  RUN is dash; bash 3.2 empty-array guard.
- Evidence: v2-5.4-input-parity (08-17), v2-5.5-demolish-input (08-17),
  packet-plumber-local-ci-suite (08-16).
- Reasoning: the local-ci-suite is now the merge ground truth (08-16 ruling)
  — false greens in the harness itself are the highest-blast-radius bug
  class; three independent sightings this window.

### P5 — Ground-truth-first binds doc authoring too
- Target: `docs/minion-field-notes.md` (addendum to the 2026-07-31/08-01
  ground-truth-first convention) · Class: auto
- Change: append — design/spec docs cite SHIPPED call sites + data files,
  not plan refs or catalog comments (GDD M1 tiers stale vs catalogs 5/15/40;
  "Plan §5" has no plan doc — cite meta/dispatch.gleam:18-22;
  `bandwidth_demand` loaded but not consumed); divergence → flag the drift in
  the deliverable.
- Evidence: packet-plumber-traffic-model-design, -surge-explainer,
  righttenantry-analytics-568-617 (all 08-16).
- Reasoning: extends the codified briefing-distrust rule to the artifacts
  minions WRITE; three jobs hit doc-vs-shipped drift in one day.

### P6 — Source material can live untracked / on a sibling branch
- Target: `docs/minion-field-notes.md` (new bullet, Tooling traps) ·
  Class: auto
- Change: new entry — check the main checkout for untracked files and sibling
  branches before concluding briefing sources/suites are missing (the
  refcheck bughunt suite lives on `origin/rt-refcheck-bughunt2`, NOT
  develop); copy in untracked, don't commit.
- Evidence: traffic-model-design (08-16), refcheck-621-reminder-hint (08-16).
- Reasoning: two jobs burned time on "missing" material that existed off the
  dispatched base.

### P7 — Perkins close-sweeps scope to OWN pane ids (CONFIRMED KILL)
- Target: `AGENTS.md` (addendum to "Perkins can self-close its round row") ·
  Class: auto
- Change: append — close-sweeps take the round's own pane ids from the round
  row/launch record, never id-proximity or label: lens tabs share generic
  labels (5.5-r1 near-miss on 7.2-r1's in-flight lenses, STOP relayed;
  doctrine-r1 held the line), and non-Perkins panes created after a round get
  ADJACENT ids (5.9-r1 close-out killed dream sheep p1ZZ/p1Z0, adjacent to
  lens panes p1ZQ–p1ZX).
- Evidence: 5.5-r1 close-out 08-17 09:15Z (near-miss, Silas journal);
  doctrine-r1 10:25Z (held); 5.9-r1 close-out 17:09Z (CONFIRMED KILL — Bob's
  own sheep, this pass).
- Reasoning: full throttle makes concurrent rounds the norm, so colliding
  labels/ids are guaranteed; this window produced a near-miss AND an actual
  kill on the same day.

### P8 — Billing block kills GH Actions runners ONLY (Perkins unaffected)
- Target: `AGENTS.md` (addendum to the provider-incidents billing block) ·
  Class: auto
- Change: append — Perkins verifies LOCALLY (pi panes + harness at the sha);
  a slow/missing Perkins review is NOT billing evidence; verify which
  substrate a process rides before declaring it blocked.
- Evidence: packet-plumber-full-game-doctrine 08-17 10:01–10:03Z — BOTH the
  minion ("BLOCKER: billing likely blocking Perkins review") AND Silas
  misdiagnosed; the misdiagnosis reached an escalation + PR comment before
  self-correction.
- Reasoning: incident context bleeds across boundaries; two independent
  actors made the same wrong call within 2 minutes.

### P9 — Watcher noise: herdr restart + dead-pi relaunch; orphan-process sweep
- Target: `AGENTS.md` (addendum to "nefario-watch fires settle
  transitions") · Class: auto
- Change: append — (a) a herdr server restart fires "pane no longer has a
  detected agent" for every tracked pane: FALSE ALARM, pane ids + pi
  processes survive (verify via lsof before any relaunch); (b) a dead-pi
  relaunch produces the same gone→idle alert as a fresh dispatch
  (classification key: alert-ts == new-session-file ts); plus close-out
  hygiene: worktree removal does NOT kill spawned processes — sweep orphan
  core.bin/beam.smp at census.
- Evidence: herdr 0.8.0 restart 08-16 09:14Z (5 jobs noted, zero action);
  5.4 revival 08-17 00:52Z; 3 stuck core.bin spinning ~3.5 cores + 2 orphaned
  beam.smp found at the 08-16 census.
- Reasoning: two new watcher-noise flavors with concrete classification
  keys, plus a resource-leak sweep with measured cost.

### P10 — Sensor echoes: same-sha-APPROVED re-fire + doc-only head churn
- Target: `AGENTS.md` (addendum to "Review/Perkins/cap sensors re-fire") ·
  Class: auto
- Change: append — (a) a re-fire on an already-APPROVED same sha is a no-op
  re-review: classify stale, no dispatch (only a NEW sha earns a round under
  the loop ruling); (b) a doc-only head move under an in-flight round earns
  NO round — record the skip-row decision at close-out (skip if APPROVED per
  the #585 precedent; superseded by the fix push if CHANGES_REQUESTED).
- Evidence: ×4 jobs for (a) — 5.5 09:13Z, 5.9 17:13Z, traffic-model r3
  08-16, doctrine 08-17; (b) 7.2 08-17 executed as written across 3 doc-only
  commits (517a13a → 7482fb4 → adfcb19).
- Reasoning: both flavors recurred and both have crisp decision rules; they
  extend the codified echo doctrine without changing it.

### P11 — Re-dispatching a done job id = row RESET: NULL `pr` first
- Target: `AGENTS.md` (addendum to the phantom-row Ledger gotcha) ·
  Class: auto
- Change: append — on a reset, NULL the stale `pr` field FIRST (a stale PR
  trips the PR watcher at in-review), update worktree/pane/tab/model, clear
  result, and OVERWRITE the note column (a reset leaves the old round's note
  text behind).
- Evidence: the 5.5 job-row reset (08-17 08:15Z) + the 5.5-r1 round-row
  reset (08:40Z) — stale note ("sha=23e1704… v4-pro") verified still on the
  reset row.
- Reasoning: redelivery dispatches are now a real flow (see W5); two resets
  in one morning exposed both failure modes.

### P12 — Serialize-hold covers held MINION dispatches (paneless rows)
- Target: `AGENTS.md` (addendum to the serialize-hold gotcha) · Class: auto
- Change: append — the hold mechanics now cover a plain minion dispatch held
  behind a merge close-out: paneless row, named release trigger, model +
  pr_review carried on the row, release = resolve fresh head THEN dispatch;
  plus the 08-16 6-deep held round chain (all released cleanly).
- Evidence: 7.1-visual-juice held 08:22Z → released 09:34Z @ 388e316 (fired
  on cue); the 08-16 chain (refcheck ← terminology ← … ← local-ci, ×6).
- Reasoning: the codified gotcha covers held Perkins rounds and verdict-gate
  job releases; the merge-close-out-triggered paneless dispatch is the third
  mechanic, proven end-to-end.

### P13 — An 18–20h minion is not automatically a stall
- Target: `AGENTS.md` (addendum to the pane-forensics errored-turn gotcha) ·
  Class: auto
- Change: append — the inverse trap: verify session-file mtime/toolUse
  GROWTH before classifying a long-running minion as stalled; the check
  precedes any continue/revive reflex.
- Evidence: v2-5.2-node-health ~20h — verified alive twice independently
  (user-asked census 08-15; badge-out 08-16: "the ~20h was REAL DESIGN WORK
  … coherence over invention").
- Reasoning: the codified traps are all about dead panes looking alive; the
  mirror (live pane looking stalled) now has two-days-verified doctrine.

### P14 — GitHub platform outage = its own incident class
- Target: `AGENTS.md` (addendum to the provider-incidents gotcha) ·
  Class: auto
- Change: append — GH platform outage (API/PRs/Issues/Actions degraded, GIT
  green): ONE advisory fanned to all in-flight rows pre-classifying noise
  (retry beats alert), no holds, Perkins unaffected; merges user-side via the
  local-merge+push CLI recipe when the web is down.
- Evidence: 08-17 13:40Z outage — advisory on 3 job rows 15:17Z; #61 + #60
  merged locally 8s apart during the incident; webhook alerts lagged ~4 min.
- Reasoning: a whole platform class distinct from both model-provider
  incidents and the billing block; the executed doctrine is proven.

### P15 — Full throttle held on kimi k3 (confirmation line)
- Target: `AGENTS.md` (addendum to the serialize-BURSTS gotcha's 08-16
  supersede) · Class: auto
- Change: append — the first 3-concurrent-round k3 burst (08-16) + a 2-round
  burst (08-17) ran with zero 429s; don't re-litigate the serialize reflex
  on k3.
- Evidence: silas journal 08-16 18:40Z (3 concurrent k3 rounds clean);
  08-17 (5.5-r1 + 7.2-r1 concurrent, clean).
- Reasoning: prevents a future session from reviving retired serialize
  doctrine against the 08-16 ruling.

### P16 — `herdr pane split` has no `--json` flag either
- Target: `AGENTS.md` (extend the pane-move `--json` gotcha) · Class: auto
- Change: extend the existing line to `pane split` (capture key
  `result.pane.pane_id`); verified still true on herdr 0.8.0 during this
  pass.
- Evidence: dream-2026-08-15's own shard (the capture chain dies on
  `--json`); re-verified against `herdr pane split --help` on 0.8.0 today.
- Reasoning: mirror of the codified move/tab-create gotcha; one-line
  completion.

### P17 — Merge-train hygiene: rebase relay BEFORE the rework push
- Target: `docs/minion-field-notes.md` (new bullet, Conventions) ·
  Class: auto
- Change: new entry — on a multi-PR base, send the rebase relay before the
  rework push lands so the fix-audit reviews one clean head; grep sibling
  hunks for disjointness and expect zero conflicts; a merge-order ruling
  beats a conflict.
- Evidence: ×5 jobs on the #55–#62 train — 7.2 (relay before B1 push → r2
  APPROVED on one clean head 1b96bea), 5.4 ×2, visibility, doctrine.
- Reasoning: 8 PRs on base v2 in ~30h made this a daily mechanic; the
  proactive relay is what kept every rebase at zero conflicts.

### U1 — Playbook: codify loop-until-APPROVED (the cap-3 doctrine is retired)
- Target: `docs/orchestration-playbook.md` (the two "Cap: 3 automated
  rounds" lines + the cap-override clause) · Class: user-ack
- Change: USER RULING 08-17 (~00:58Z, #57): "go more rounds. until we have
  an approval." — replace the cap-3 doctrine with loop-until-APPROVED:
  minion pushes the rN-blocker fix → stability gate (settled head + local
  suite green + minion done iterating; billing CI is not a gate) → dispatch
  rN+1 fix-audit with prior_findings=rN → repeat until APPROVED. Note that
  fix-audit rounds finding DELTA-introduced blockers is the norm, not a
  failure (the 5.4 arc: r1 2B → r2 2 new delta blockers → r3 1 → r4
  APPROVED 0B).
- Evidence: the ruling itself (5.4, then extended to ALL new jobs via the
  08-17 standing authorization); every subsequent dispatch ran uncapped
  (5.5, 7.2 r1+r2, 5.9, doctrine); traffic-model finished under the OLD
  regime (the contrast pair).
- Reasoning: the playbook still says "Cap: 3 automated rounds" in two places
  with only a named-override clause — doctrine on disk contradicts the
  operating reality since 08-17.

### U2 — Playbook/Gru standing orders: codify the 08-17 STANDING AUTHORIZATION
- Target: `docs/orchestration-playbook.md` (Gru standing orders / dispatch
  doctrine) · Class: user-ack
- Change: USER RULING 08-17 (~08:2xZ): "dont wait foe me.. keep going." —
  Gru briefs + dispatches the queue WITHOUT per-step user acks;
  loop-until-APPROVED extends to new jobs; the MERGE ritual is UNCHANGED
  (the user merges); the authorization is countermand-able at any time.
- Evidence: gru journal 2026-08-17; the day's execution (7.1 held-then-
  released, 5.5 redispatch, doctrine dispatch — all without per-step acks;
  merges still user-side: #59, #60, #61).
- Reasoning: high-value governance ruling that currently lives ONLY in the
  Gru journal; a session restart loses it.

### U3 — Playbook Model policy: capability routing (vision jobs)
- Target: `docs/orchestration-playbook.md` (Model policy section) ·
  Class: user-ack
- Change: add one line — visual jobs (look-book canon, T2 pixel goldens,
  before/after re-bless) launch on a native-vision model — kimi-coding/k3 as
  of 08-17; the override writes the ledger row model field AND the briefing,
  and a deferred/held dispatch must carry the `--model` flag at release.
- Evidence: 7.1-visual-juice ruling 08-17 08:28Z ("we need a model with
  native vision"); row model field updated + briefing updated + release
  carried the flag (Silas journal + ledger).
- Reasoning: the model policy routes by role and provider-health only;
  capability (vision) is a third axis with one ruling on record and more
  visual jobs coming (7.1 Phase A/B).

## Watch items (anecdotes — tracked, not proposed)

- W1 — `git checkout <file>` restores from the INDEX, silently wiping
  uncommitted mutation fixes (v2-5.4, 08-17: "I killed my r3 mouse.odin fix
  that way"). `cp` a backup BEFORE mutating for a mutation test. Pairs with
  the P3 mutation discipline; promote on recurrence.
- W2 — PR-event CI builds the branch MERGED into base: a T2 blessing on a
  stale base passes locally + on the push-event run, fails ONLY on the
  PR-event run; a same-sha green twin run is the signature (v2-5.2-node-health
  #54, 08-16 — root-caused, fixed via clean v2 merge + deliberate re-bless;
  the merge-base check is now badged practice). One incident; promote on
  recurrence.
- W3 — deepseek 402 Insufficient Balance mid-round kills only the LENS waves
  (the chief pane on another provider survives): sweep + redispatch the
  LENSES, not the round — probe first (terminology-audit r1, 08-16 13:00Z;
  recovered 112/112 on glm-5.3 → APPROVED). A 4th provider-failure flavor
  (402 balance ≠ 403 quota ≠ 429 burst); one incident.
- W4 — preserve-to-_bmad-output collides at the next pull when a later PR
  commits the same path (traffic-model close-out, 08-16: untracked artifact
  copy vs PR #53's committed copy → pull --ff-only abort; resolved by
  byte-compare + remove). Close-out checklist: pull-fail → check untracked
  artifact collisions first.
- W5 — a refactor can silently un-ship a MERGED story (5.5: the 08-14 #44
  surface rode the pre-5.4 input path; the 5.4 refactor made it vestigial).
  Redelivery needs prior_findings=none + a RESET round row (P11) + a ruling
  that the old PR is "superseded, not re-litigated". One incident.
- W6 — Perkins self-close + orchestrator death = orphaned `working` round row
  (08-17 00:50Z: r3 posted its verdict 00:04Z and self-closed; old Silas died
  before close-out; row sat working overnight). Respawn catch-up should
  reconcile non-done round ROWS against posted reviews, not just panes.
- W7 — lavish-gated 2-phase visual direction (7.1 ruling 08-17): Phase A =
  style probe (2–3 treatments rendered as REAL game frames via the game's own
  draw code) behind a lavish HARD GATE → Phase B = implement. Generalizable
  for subjective visual work; one job, still in flight.
- W8 — tool updates silently change agent-facing contracts (lavish-axi
  0.1.52, 08-17: layout issues file PASSIVELY, self_paint_warning new): the
  on-disk skill went stale — synced from the npx cache (committed 0f1b916) +
  deltas relayed mid-flight. Watch skill versions on tool update notices.
- W9 — env-only API keys (asset ruling 08-17): ELEVENLABS_API_KEY lives in
  ~/.zshrc, NEVER in repo/logs/PR; new panes inherit it, RUNNING panes
  predate it (relaunch to pick it up).
- W10 — the `ledger set` same-status-drops-note warning is buried in the
  playbook's review-sensor section; minions hit it at self-report time —
  belongs in the self-report/standing-orders section too
  (full-game-doctrine shard; playbook edit, would be user-ack).
- W11 — cross-lane T2 re-bless FYI: when sibling lanes both re-bless frames,
  call out whose frames land at push (7.1 on #62's 29-frame re-bless, 08-17).
- W12 — PP-repo Odin language traps are accumulating (slice literals backed
  on the caller's stack; relative imports resolve from package root; constant
  arrays unindexable by variable; truncating f32→int const cast is a compile
  error; `odin test` needs clang) — candidates for a PP-repo Odin-gotchas
  section rather than global field notes.

## Pruned / rejected candidates (with why)

- Billing-block classification recurrence (×15 alerts, 8+ jobs, incl. RT
  #623/#624): the 08-16 ruling held perfectly with one stable signature
  (3–5s fail, runner never started, no logs) — already codified; no edit.
- Review swarms earn their cost (v2-5.4, v2-visibility — ×2 positive):
  codified 2026-08-07/08-13; recurrence only.
- Re-bless cause-chain discipline (×5 jobs, now a named Perkins guard):
  codified 2026-08-13 golden-discipline entry; only the lane-to-lane facet is
  new → W11.
- Cross-lane overlap flag → user ruling → canon addendum (7.2 lane ruling,
  08-17): the codified two-layer flag pattern working as designed; the canon
  itself lives in PP docs (via #61) — no memory edit.
- glm-5.3 1302 burst 2nd sighting (traffic-model r1, 08-16): the one-continue
  doctrine held verbatim; no edit.
- pr-field self-set held all window (PP crew ×3, RT crew clean; zero NULL-pr
  incidents in 272 events): the verify-and-set guard found nothing to fix —
  positive confirmation, no edit.
- No pane-id slips, phantom rows, or minion-created rows this window: the
  08-14/15 hygiene classes did not recur — noted, no edit.
- Explainer correction-on-record + "design notes are TASKS" ruling (08-15
  ~16:45Z): inside the previous dream's window boundary; minor; rejected.
- Respawn: the extension checklist beats the handover (08-17 00:47Z): single
  sighting, minor — the respawn doctrine already works; rejected.
- R7 (lane ruling), R8 (full-game doctrine), R9 (asset licensing): project
  canon for packet-plumber, already cascaded into the PP docs via #61 —
  memory-store edits would duplicate canon; only the generalizable env-key
  rule kept (W9).
