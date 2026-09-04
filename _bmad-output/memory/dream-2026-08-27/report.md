# Dream report — 2026-08-27

Material: 11 field-note shards (7 post-marker full + 4 gap-window tail), 7 journal
files (gru 08-24 tail, 08-25, 08-25-pi-restoration-handover 240L; silas 08-24 tail,
08-25, 08-26, 08-27), ledger events 2026-08-25T09:58:22Z → 2026-08-27T10:03Z
(~380 dense lines + 3 depth rows) — since marker 2026-08-25T09:58:22Z.
3 sheep (shards / journals / ledger), glm-5.3 +thinking max, all badged out and
panes closed by Bob. 74 raw candidates → 23 proposals (all **auto**; 2 flagged
for Gru visibility), 19 watch items, 8 pruned classes.

**Marker-scope note for Silas:** the marker jumped 08-23T19:22:40Z → 08-25T09:58:22Z
inside commit 5b5de85 WITHOUT a Bob pass in between (DSH interlude; the interlude's
rulings were ported directly into AGENTS.md by 65f8c0b, which the marker advance
encodes). The gap window 08-23T19:22Z → 08-25T09:58Z therefore got only
tail-read coverage this pass (gru/silas 08-24 tails + the 4 gap shards). The
sheep found nothing contradicted, but if a gap-window anomaly ever surfaces, that
window is the soft spot.

**Flag for Gru (auto-applied, user-ruling encoders — veto path):** P9 (interactive
design-session doctrine), P10 (evidence-first look chain) both encode fresh user
rulings from 08-26 into ops gotchas. They read as standard gotcha appends but
deserve a glance.

## Proposals

### P1 — Fold-collision close-out law
- Target: store/AGENTS.md · Class: auto
- Change: NEW bullet after the "Verify merge/deploy state by commit-containment"
  bullet (Ledger section).
- Evidence: PR #102 merge close-out 2026-08-26 ~19:10Z — "ff blocked by (a)
  modified deferred-work.md, (b) 9 untracked originals colliding with the fold's
  now-tracked paths... the stashed copy proved STALE (missing the fix-minion's 6
  deferral lines) → took tracked HEAD" + PR #103 close-out same day ~20:05Z —
  "08-26 arch dir collision = aside-verify-drop again, byte-identical, clean".
- Reasoning: folding untracked artifacts into a PR (the sanctioned preserve-first
  move) structurally leaves duplicate originals in the main checkout; the NEXT
  merge collides. Expect it, resolve stash+aside+verify-byte-identical+drop, and
  never assume stash-newer-is-superset (disproven same day).

### P2 — MEGA-DIFF protocol + bash-3.2 wave-spawn note (Perkins section)
- Target: store/AGENTS.md · Class: auto
- Change: NEW bullets inserted before the "### Ledger" heading.
- Evidence: PR #96 2026-08-24 — "BIG DIFF 84,831L (gh pr diff API 20k-capped →
  git diff origin/v2...refs/pr-96 saved; chunking mandatory)"; egress r1
  2026-08-26 — "gh pr diff 406'd (>20000-line API cap — FIRST occurrence) →
  canonical diff generated locally (54356 lines, substitution disclosed);
  two-class protocol = full lens waves on CODE chunks, mechanical
  bulk-verification on goldens/docs"; egress r1 close — "14 lens runs 0 failed,
  51k bulk lines mechanically verified". bash-3.2: tie-deconflect r2 08-25 —
  "bash-3.2 assoc-array bug collapsed wave-1 into one pane (agent
  self-recovered)"; gauge-telegraph r1 + crisis-duck r1 dispatch notes carry the
  wave note proactively.
- Reasoning: >20k-line PRs are now routine on PP v2; the protocol (local
  canonical diff + disclosed substitution + code-vs-bulk split + r2
  fix-delta-weighted spot-checks) is the proven review path. bash-3.2 wave
  collapse loses a wave silently unless briefed.

### P3 — pr_review/dedup family addendum (user-PR blindness, pre-add rows, batch sweep, typo ids)
- Target: store/AGENTS.md (inside the `pr_review` LEDGER KEY bullet) · Class: auto
- Change: dated addendum paragraph appended to the bullet.
- Evidence: #98 gap 2026-08-25 — "user-authored branches carry no job row → no
  pr_review=1 → sensor blind. Handed Silas full package: register row
  (pr_review=1) + dispatch Perkins r1" (+ #97 08-24, spec = PR body, user's
  COMMENTED ≠ verdict); gauge-telegraph 08-25 — "pr_review COLUMN was 0 though
  the briefing said 1 → SQL-fixed on this row AND crisis-duck (same latent
  gap)"; round-row pre-adds — "Round row PRE-ADDED by me this time (dispatched +
  parent=/sha= in note) so sensor dedup holds" (gauge r1 08-25, egress r1/r2
  08-26); "ledger add chokes on sha= (not a column)" 08-25; tie-deconflect r2
  round row typo'd id (parent=/sha= notes saved dedup).
- Reasoning: consolidates this window's four facets of the documented 08-12
  class into the existing bullet: register user PRs, pre-add round rows AT
  DISPATCH, sweep the batch when one fires, and treat parent=/sha= notes as the
  durable dedup keys (typo-proof).

### P4 — glm-only regime addendum (1308 early-free, parked continues, zero-JSON waves, connection-class)
- Target: store/AGENTS.md (inside the Provider incidents bullet, after the 1302
  taxonomy) · Class: auto
- Change: dated addendum appended.
- Evidence: 1308 cluster-stop 08-26 07:35Z — "rolling window freed within ~1min
  (double probe OK) → one continue each revived both... stated reset times lie,
  probe-only decides"; probe-DOWN hold — "the 00:41Z 1302 burst killed the main
  mid-wave-spawn; probe-DOWN hold parked recovery ~6.4h... all 7 lens panes done
  but ZERO lens JSONs on disk (spawn_wave logged prompt-seen=0 ×5)";
  connection-class: crisis-duck r2 08-26 15:48Z — "connection-error wave killed
  the main mid-c2-wave (c1 6/7 JSONs durable)... one continue → re-driving the
  wave"; tie-deconflect r2 08-25 — wave killed main MID-VERDICT-POST, artifacts
  salvaged; self-recovery: crisis-duck 08-26 13:28Z — "pane self-recovered
  (auto-retry)... no continue needed" + 14:15Z triple-transient note-only.
- Reasoning: extends the documented taxonomy with four exercised rules: 1308
  frees early (double-probe, never wait), an owed continue legitimately parks
  under a probe-DOWN hold (resume on flip), wave-state ground truth = lens JSONs
  ON DISK never pane status (prompt-seen=0 class), and connection-class waves
  get the same one-continue + degraded-lens disclosure as 429s — while pi
  auto-retry now makes some transients zero-action.

### P5 — W3 overnight-stall flavor
- Target: store/AGENTS.md (inside the Close-out drift + W3 bullet) · Class: auto
- Evidence: egress-migration r2 2026-08-26T21:41Z → 08-27T08:59Z — "spawn-turn
  stall after setup... overnight timing parked it ~11h with zero progress;
  RESUMED ~08:5xZ (cache-miss 678m = fresh turn wake). Lesson: overnight stalls
  park until the next alert window."
- Reasoning: the documented one-continue nudge is cheap but needs someone awake;
  the startup/wake-up sweep must check stalled-round rows rather than waiting
  for the alert window.

### P6 — Interactive design-session doctrine (FLAGGED)
- Target: store/AGENTS.md (new bullet in the sensors/Perkins insert block) · Class: auto (flag)
- Evidence: node-legibility-diag 2026-08-26 — "INTERACTIVE HALT (correct
  behavior post-amendment): Sally presented fork #1 of 5... idle-await is the
  contract" + "settle echo of the 12:59 interactive halt — pre-classified" +
  "PROCESS RESET (user, in-pane): no decisions without the user; earlier rulings
  revisitable not void"; link-vocab 08-26 — "Awaiting USER fork ruling in pane
  (direct-to-pane legit). User actively driving; no escalation"; pause-and-spec
  close — "LOOK-SPEC.md (fix-job ready) + design-log.md (rulings in user's
  words)".
- Reasoning: a user-ruled session shape (Sally persona + interactive mode):
  watcher alerts on these rows are halts or their settle echoes, never stalls;
  escalate only when the user is absent; the pause-and-spec output (design-locks
  spec + user-word design-log + parked forks) turns a user-gated session into
  durable spec for the next heist.

### P7 — Evidence-first look chain (FLAGGED)
- Target: store/AGENTS.md (addendum inside the User mid-flight reversals bullet,
  after the designed-gate/LOOKS-primary text) · Class: auto (flag)
- Evidence: node-legibility-diag dispatch 2026-08-26 00:19Z — "SECOND complaint
  on this axis... READ-ONLY evidence job... main checkout, NO branch/worktree,
  captures + KYLE pixel measurements + lavish gate; parallel-safe"; session
  close 19:05Z — "LOOK-SPEC.md + design-log.md + direction-ruling + KYLE
  findings preserved at implementation-artifacts/look-node-legibility/";
  look-zoom release 08-27 — "Sally artifacts (LOOK-SPEC + design-log) are the
  spec inputs... parked forks fenced out".
- Reasoning: repeat play-feedback on one visual axis is systemic — the chain
  (read-only evidence job → interactive ruling session → durable spec artifacts
  → implementation heist briefed FROM the artifacts with forks fenced out)
  generalizes the 08-20/21 designed-gate doctrine to the look lane.

### P8 — Fold routings addendum (advisory batch issue + stranded-artifact chore commit)
- Target: store/AGENTS.md (addendum inside the issues-first text, moot-on-merge
  bullet) · Class: auto
- Evidence: crisis-duck 2026-08-25 21:30Z — "advisory batch issue #101 opened —
  EXECUTION FOLD: rides THIS PR... close #101 when crisis-duck ships" (closed
  at #102 merge 08-26); hygiene fold 08-25 23:43Z — "8 uncommitted main-checkout
  artifacts COPIED into the worktree — ride the PR as a separate verbatim chore
  commit (preserve-first)" (chore 8c482ec) + "branch deletion awaits USER word".
- Reasoning: two fold shapes complete the issues-first family: prior-round
  advisories = one batch issue folded onto the lane's next PR; stranded
  orchestrator artifacts = verbatim chore commit on the in-flight PR; redundant
  merged branches are USER-gated, never Silas-deleted.

### P9 — Trigger-graph release conventions
- Target: store/AGENTS.md (addendum inside the Trigger graph (P2) section) · Class: auto
- Evidence: crisis-duck auto-release 08-26 00:36Z — "first hands-off release
  through the graph since the pi restoration — brief staged, ruling relayed,
  graph did the rest"; look-zoom release 08-27 09:38Z — "released at fresh head
  088cf00... blocked_by cleared"; mid-flight crossing 08-26 19:15Z — "the
  release authorization crossed my close-out escalation mid-flight — verified
  single dispatch (one row/pane/worktree)"; "briefing column backfilled after
  the re-check caught it empty" (paneless row).
- Reasoning: at-scale conventions beyond the 08-23 addendum: stage the briefing
  BEFORE release; paneless held rows need a briefing-column backfill check;
  when a release crosses an in-flight escalation, verify single dispatch.

### P10 — herdr/watchman transition-read addendum (false-done, case-drift, stray input)
- Target: store/AGENTS.md (addendum inside the Silent pi deaths/night-watchman
  bullet) · Class: auto
- Evidence: restoration — "herdr agent-wait false-negatived BOTH boots
  (registration race)"; silas 08-25 01:30Z — "herdr reported agent_status=done
  on w85:p1 while the pi process was alive+idle... NO relaunch" (the due
  escalation doubled as the functional probe); watchman case-drift 08-25 —
  "config expects tab label `Gru` (capital), live tab is `gru` — permanent miss.
  Fix e5838c1: exact match first, unique case-insensitive second, ambiguity
  still warns"; stray input 08-26 12:54Z — "a stray /dedi opened pi's
  skill-navigator mid-lavish-poll, aborting the 3500s poll; q/escape
  insufficient — C-c cleared it; one continue resumed".
- Reasoning: three facets of one law — around transitions and edge cases herdr's
  status/wait/label reads lie in BOTH directions: process + session file is
  ground truth; label resolution needs the case-insensitive ladder; human
  keystrokes landing in a live pane are an incident class (C-c, not q/escape).

### P11 — r2 fix-audit independently re-runs mutation legs
- Target: store/AGENTS.md (addendum inside the vacuous-pin (d) text) · Class: auto
- Evidence: gauge-telegraph r1 08-25 — "Perkins independently re-ran the mutation
  leg (gauge_read := raw → palcheck §6 FAILS ×2; restored green)"; crisis-duck
  r2 08-26 — "B1 fix mutation-verified 3/3 RED + restore green"; egress r2
  08-27 — "B1-B4 ALL FIXED with Perkins re-run RED mutation legs... 3 REJECTED
  after verification (blind avail==0 misread + 2 vacuous-coverage claims
  disproven by mutation)".
- Reasoning: the fix-audit acceptance standard hardens: r2 rounds re-run r1's
  mutation legs RED-then-GREEN INDEPENDENTLY, and the verification pass now
  also rejects lens findings (vacuous-coverage disproven by mutation).

### P12 — KYLE ranks perceptually; measurement decides
- Target: store/AGENTS.md (addendum inside the Vision=KYLE bullet) · Class: auto
- Evidence: node-legibility-diag 08-26 — "vision (KYLE) corroborates but ranks
  colors perceptually (called dark-ring variant 'wrong' where WCAG said best
  contrast — both true: contrast vs board ≠ separation from the dark puck rim)";
  remedy — "emit geometry.json anchors FROM the renderer, then PIL-measure
  against them"; dublin-map 08-24 — KYLE narrowed the look, byte/pixel gates
  decided.
- Reasoning: extends the vision-screening law: contrast-vs-board and
  separation-from-adjacent-dark-surface are DIFFERENT axes; verdicts anchor in
  renderer-emitted geometry + programmatic measurement, KYLE corroborates.

### P13 — masked-rc / stale-binary trap
- Target: store/minion-field-notes.md (Tooling traps append) · Class: auto
- Evidence: crisis-duck 08-25 — "the masked-rc trap bit THREE times in one job:
  `odin build ... | head` and `2>/dev/null` both hide build failures and re-run
  a STALE bin/harness (once 'confirming' a mutation leg that hadn't compiled)";
  tie-deconflict 08-25 — "a deliberate-fail probe is the cheap way to confirm a
  test binary actually executes your new test".
- Reasoning: rc must bind the BUILD's rc not the pipe's; rebuild before trusting
  any binary; a deliberate-fail probe proves the harness runs the new test.

### P14 — Odin procs do not capture enclosing scope (consolidate 2 shards)
- Target: store/minion-field-notes.md (Tooling traps append) · Class: auto
- Evidence: gauge-telegraph 08-25 (bitten twice: palcheck render/count closures);
  dublin-map-beautify 08-24 (seg-grid builder).
- Reasoning: recurring PP trap; fix idiom = file-level helper procs with
  explicit params / struct pointers. Sheep noted two shards carry it — one
  consolidated store entry.

### P15 — Verification binds to an independent anchor
- Target: store/minion-field-notes.md (Conventions append) · Class: auto
- Evidence: crisis-duck 08-25 — "enumerate crisis state AT THE CAPTURE TICK,
  never from demo comments" (stale 4.2-era captions); dublin-map 08-24 — "the
  bake's --verify PASSED because it compared the same buggy output twice";
  arch-latency 08-26 — "bandwidth_demand is catalog-loaded but UNWIRED — never
  cite a catalog knob in a formula without grepping consumers".
- Reasoning: three self-confirmation flavors (stale captions, self-comparing
  verify, documented-but-unconsumed); anchor to independent sources —
  capture-time state dumps, second derivations, consumer greps.

### P16 — Mock-loop craft: parameterize + KYLE per round
- Target: store/minion-field-notes.md (Conventions append) · Class: auto
- Evidence: node-legibility 08-26 — "the user iterates on MOCKS fast (7 rounds,
  ~10 min) — keep the mock tool parameterized per-direction, regenerate strips
  in one command, KYLE-verify each round"; dublin-map 08-24 — "the mock gate
  evolved the design 7 rounds in one lavish session".
- Reasoning: two jobs, both exactly 7-round mock loops; one-command regeneration
  + per-round KYLE verification is what makes the loop cheap; rulings land from
  the gallery.

### P17 — Mutation-leg craft facets
- Target: store/minion-field-notes.md (addendum to the vacuity cluster) · Class: auto
- Evidence: crisis-duck 08-26 — "`|| true` inside an expect is a vacuous pin
  wearing a seatbelt (shipped one AGAIN)" + "never re-derive the 'before' value
  inside an assertion AFTER mutating" + "`pop()` removes the LAST row —
  swap-remove to remove a specific crisis"; egress 08-26 — "a clamp-at-100 util
  needs an ASYMMETRIC fixture (60/30) — a saturated fixture cannot discriminate
  max from sum"; tie-deconflict r2 08-25 — "the pin covered the PREDICATE, not
  the draw path — a pure-proc pin is bypassable at the call site"; dublin-spawn
  08-24 — "pin the exclusion not the ratio".
- Reasoning: the minion-facing complement to P11 — a compact craft list
  extending the mutation-leg law.

### P18 — shadow_clone clone-list is a per-story trap
- Target: store/minion-field-notes.md (Tooling traps append) · Class: auto
- Evidence: egress-migration 08-26 — "EVERY new step()-touched dynamic array
  must be added to spawn_fx.odin's clone list AND its flow_init mirror — the
  shadow silently aliases LIVE pointers and the abort surfaces far away at
  run_destroy (tx-ring comment = prior incident)".
- Reasoning: symptom (far-away abort) disjoint from cause; grep the clone list
  whenever a step()-touched dynamic array is added. Two incidents on record.

### P19 — Index-keyed derived state must reset on regeneration
- Target: store/minion-field-notes.md (Recurring review findings append) · Class: auto
- Evidence: egress-migration 08-26 — "Same-count bundle renumber silently
  inherits the dead pair's history unless derived-ring layouts reset on
  Topology.gen — the B1 slot-renumbering class generalizes to every ring keyed
  by a regenerated index (hunter-probed at 120 phantom ticks)".
- Reasoning: generalizes the estate-r3 B1 class; incremental maintenance on
  renumberable indexes inherits dead entries.

### P20 — Odin fmt/syntax micro-traps
- Target: store/minion-field-notes.md (Tooling traps append) · Class: auto
- Evidence: node-legibility 08-26 ({{}} escaping, appendf, per-line import);
  dublin-spawn 08-24 (NO %-3d — silent value×100 garbage; `x: T` not `var x T`);
  egress 08-26 (for-in over array literals = syntax error); tie-deconflict
  08-25 (no #error directive — `when <bad> { BROKEN :: 1/0 }` idiom; `odin test
  app` ≠ `odin test app/render`).
- Reasoning: the silent ones (%-3d, missing {{}}) produce garbage with NO
  compile error — the killer class.

### P21 — Palette pins must check ALL variant surfaces
- Target: store/minion-field-notes.md (Recurring review findings append) · Class: auto
- Evidence: tie-deconflict 08-25 — "CVD mode tables remapped route_tie to pale
  amber RGB-identical to state_congested's remap — a11y overrides silently
  reintroduce a collision you just fixed; diff the mode tables too" +
  derive-script can't parse palette.json `//` comments; gauge-telegraph 08-25 —
  "the bar FILL + pct draw the darkened state_*_text variants — pixel pins
  must match the text variant or they read 0 px".
- Reasoning: the drawn color is often NOT the base palette entry — check CVD
  mode tables and text-variant darkening before writing pixel pins.

### P22 — Render-surface realities defeat pixel gates
- Target: store/minion-field-notes.md (Recurring review findings append) · Class: auto
- Evidence: crisis-duck 08-26 — "rlsw renders DrawTriangle FILLS opaque — an
  alpha-only 'recede' on a hand-built triangle surface is a no-op" +
  "street-oriented quads are BACKFACE-CULLED for some windings — a
  fill-changing mutation stays pixel-inert; probe with distinct-color dumps" +
  "when the highlight owns the surface, pin the neighbor surface"; tie
  -deconflict 08-25 — "palcheck sections can do full live-render checks without
  touching goldens — analysis renders may invoke assists where golden captures
  may not".
- Reasoning: before trusting a pixel gate, confirm the surface actually renders;
  overdrawn targets → pin an adjacent clear surface; analysis renders have
  wider license than golden captures.

### P23 — One-line addenda bundle (edit-escaping, .env symlink, lavish asset paths)
- Target: store/minion-field-notes.md (multi-edit entry addendum; lavish craft
  entry addendum) + store/AGENTS.md (RT bootstrap bullet addendum) · Class: auto
- Evidence: arch-latency 08-26 — "mermaid label strings contain LITERAL \n — in
  edit oldText they must be \\n-escaped (a raw \n silently becomes a newline,
  the match fails, the whole multi-edit call atomically no-ops)";
  righttenantry-dublin-rents 08-24 — "worktree bootstrap missed `server/.env ->
  ../.env` — without it `make run` panics 'DATABASE_URL not set'";
  dublin-map 08-24 — "lavish HTML must reference images as <dir>/img/... — bare
  img/... fails as 8 fatal artifact-asset-unavailable failures (the poll
  returns them, not user feedback)".
- Reasoning: three single-sighting facets of ESTABLISHED multi-sighting families
  (multi-edit atomicity, RT worktree bootstrap, lavish craft) — one-line
  addenda each.

## Watch items (anecdotes — tracked, not proposed)

1. **Pane-vanish mid-badge-out ("minions NEVER close their own pane")** —
   egress-migration 08-26 20:46Z, single sighting but STRONG: work intact, only
   PR/ledger/notification lost; recovery = fresh pane, same worktree,
   completion-only contract. Silas's row note already carries the lesson;
   promote on 2nd sighting (likely soon — it's a briefing-clause fix).
2. **Merged-over-CHANGES_REQUESTED fix-forward lifecycle** — #97→#98 arc
   (08-24/25): user merges own PR over CR → live-on-base blockers → fix-forward
   pin PR closes the loop. Single arc; pairs with P3's user-PR facet.
3. **DSH orchestrator fit criterion** (user-level): mid-turn interruptibility +
   never-starved user lane is THE load-bearing property; DSH failed both.
   Durable homes: pi-restoration handover + dsh-orchestrator-setup/AGENTS.md.
   Candidate user-ack canon line if the experiment question ever recurs.
4. **Restoration/move checklist**: verify ledger DB by SCHEMA not path
   (empty-shell DB found), canonical symlink set incl. docs/, symlinked homes
   split journal state — one real exercise 08-25.
5. **check-pr-ready per-reviewer latest-verdict law** — stale-CR false block on
   #99 r2; FIXED in PR #15 (open, user merges ops PRs). Single sighting;
   generalizes to any future review-state gate.
6. **Lens findings read during the round's OWN mutation window are timing
   artifacts** — egress r2 (1 rejected, disclosed). Expect recurrence in
   mutation-heavy rounds.
7. **palcheck needs the harness.sh shadow path in headless panes** (egress r2
   invocation note) — carry in PP round briefings.
8. **Recorded revisit triggers pay verbatim days later** — 08-23 egress-qos
   withdrawal re-opened exactly as written on 08-26 (render-side re-frame).
9. **Coaching-vs-Fast must be named in load-bearing architecture briefings**
   ( Gru process note, spine session).
10. **Loaded-but-unwired config → NAMED story routing** — D-2 arc (found by
    reality lens → named balance decision → shipped S3 with disclosure). Single
    arc; rides P15's consumer-grep facet.
11. **Silent spawn-time failure, batch-correlated** — two panes of one 15:02Z
    08-25 batch: no error, no ledger write; verify ground state + re-dispatch
    same row.
12. **protocol_mismatch = transient client/server skew; the following restart
    renumbered the workspace prefix (w1T→w85) with pane ids surviving** — don't
    chase phantom panes; expect historical pane prefixes in old rows.
13. **Diff at the MERGE-BASE before believing "deleted files" blockers** —
    egress r1 ("deletes the spine" was a merge-base artifact). Single sighting.
14. **Enumerate existing payload slots before declaring a serialization bump**
    (arch-latency: Event.direction reuse kept LOG_VERSION 6). Single.
15. **Scratch rlsw capture recipe is PER-BINARY** (warmup frames, present lag,
    flip/swizzle differ even on the same shadow) — calibrate each capture
    binary against known tokens + anchors.
16. **node:sqlite DatabaseSync {readOnly:true} is the sanctioned ledger read
    path** (sqlite3 CLI rc=14) — for anything reading orchestrator.db
    externally.
17. **Docs-spine loop: lavish ratify-first → verbatim-commit docs PR,
    pr_review=0** — spine #103 arc; second occurrence would canonize.
18. **Recipe bag (single sightings, job shards retain detail)**: PIL no
    alpha-blend on draw; module-level def shadowing a library import; typst
    six-pattern byte-identity normalization + place() semantics; Blender pure
    ShaderNodeEmission sRGB→linear hex-exact recipe; RT og-card orphan-test
    pinning + rsvg pipeline; static demo mesh bounds growth claims; map-bake
    geometry (touches-vs-contains, STRtree, sea polygonize).
19. **herdr pane resize --amount is a FLOAT fraction** (live discovery this
    pass: integer amounts clamp to layout extremes; 0.27 moved the split
    cleanly; verify with pane layout) — sheep-tab/lens-tab layout maintenance.

## Pruned / rejected candidates (with why)

- **Backtick-eaten relay, 3rd sighting** (08-25) — no NEW rule; the AGENTS.md
  Extensions entry + generator facet already cover it. Reinforcement only.
- **Billing-block CI at ~5×/day** — standing 08-16/08-19 rulings held every
  time (note-only, local ground truth); no new doctrine; volume noted.
- **Erlang rebind/fun-per-chain micro-trap** — single sighting, too micro for
  the curated store; the RT shard retains it.
- **DSH loader-entry-fatal gotcha** — lane closed by user ruling; DSH-era
  rulings live in dsh-orchestrator-setup/AGENTS.md by design.
- **Map-bake geometry specifics** — tool-local; the dublin shard retains; bake
  revisit unlikely mid-v2.
- **bmad-build render waiver** — already documented standing path
  (dream-2026-08-21/23); the gauge shard merely cites it.
- **Silas completion-agent salvage + watchman Gru-death catch** (08-25) — both
  AS-DESIGNED exercises of documented paths (durable-artifact salvage,
  night-watchman kill test); no new rule.
- **W1/W2/W5 self-report gaps from the DSH-era rows** — subsumed by P3's
  addendum (batch sweep + pre-add).

## Housekeeping notes for Silas (not proposals)

- `orchestrator-dashboard-perkins-bridge.md` is mis-titled (3 lines of DSH
  dashboard tech notes, zero Perkins content) — rename or fold at next touch.
- Round-row id typo lineage: `tie-deconflect-perkins-r2` (parent is
  `-deconflict`); r2 artifacts dir was created under the typo then moved — the
  note-vs-dir mismatch is recorded on the row; consider a one-time SQL fix if
  any tooling ever greps round ids.
- r1 note on tie-deconflect said "lite" lens set but 7 lens JSONs exist (full
  set) — read artifacts, not notes, for that round.
- Stale dsh-orchestrator-setup paths in briefs-archive/ are archival; do not
  resurrect.
- Bob's own row this pass: model/pane/tab fields verified set; briefing column
  points at the template (not a dated copy) — cosmetic only.

## Proposed store state

Both store copies carry all 23 proposals applied (diff-ready):
- store/AGENTS.md — P1-P12 (new bullets + addenda inside existing bullets)
- store/minion-field-notes.md — P13-P23
