# Dream report — 2026-08-29

Material: 7 field-note shards (6 full + dream-2026-08-27 tail-read, marker
boundary −86s), 7 journal files (gru: pi-restoration-handover, 08-27-evening,
08-29; silas: 08-27, 08-28, 08-29 full + 08-26 tail-read), ledger events
2026-08-27T10:29:07Z → 2026-08-29T21:30:44Z (200-event window complete + 9
`ledger show` depth reads) — since marker 2026-08-27T10:29:05Z.
3 sheep (shards / journals / ledger), kimi-coding/k3 +thinking max (k3
double-probed UP at dispatch; modelId verified per pane), all badged out and
panes closed by Bob. 44 raw candidates → 22 proposals (19 **auto**, 3
**user-ack**), 13 watch items, 6 pruned classes.

Window arcs: the viscomm trilogy close-outs + regression-audit → A1 pulse arc;
The Box heist (PR #107, 5 Perkins rounds, mega-diffs both ways); the
3rd-spawn crash + fix (PR #108, fun-test gate first fire); shape-vocab +
lang-safety rulings; skills dedup sweep; two Silas restarts (herdr outage +
pre-dream hygiene); the youtube-channel creative lane (out of scope, pruned).

**Flag for Gru (auto-applied, user-ruling encoders — veto path):** P5
(ruling-supersedes-APPROVED) and P6 (interactive close-shape) encode fresh
user rulings/behaviors from 08-28/29 into ops gotchas. They read as standard
gotcha appends but deserve a glance.

## Proposals

### P1 — Flash-tier Perkins rounds: connection deaths ~1×/round + blind-lens truncation canary (budget, don't alarm)
- Target: store/AGENTS.md (Perkins round-ops bullet, as 2026-08-29 addendum
  items (g)+(h)) · Class: auto
- Change: dated addendum appended after the r2-fix-audit addendum
  ("…egress r2: 3 rejected, disclosed."). Text in the store copy.
- Evidence: silas 08-28 ~14:2xZ — "4th connection-class round death today —
  all salvaged via durable artifacts… flash long-context lens waves die
  ~1x/round mid-wave; one continue + disk state = full recovery every time"
  (5 deaths <24h: #106 r1/r2, #107 r1/r3/r4/r5); #107 r5 18:58Z — "main died
  …before any lens JSON landed (only diff patches saved); ONE continue
  revived it — the wave restarts from the saved canonical diffs". Blind
  truncation ×7 rounds / 4 jobs / 2 days: look-zoom r1 ("blind lens failed
  both attempts (flash long-context truncation) — the diff was read by all 6
  remaining lenses"), #107 r1 (output-cap 2x), r3 (3x), r4+r5 (retry-once →
  7/7), box-crash r1 (2x).
- Reasoning: the flash tier now runs every round; quantifying the expected
  death rate + the retry-once-fresh-pane/6-lens-degraded playbook stops both
  over-reaction (re-dispatch) and under-disclosure (faked 7/7).

### P2 — Sweep completeness hardening: moot sweeps leak LENSES, close-outs leak MAINS; culls spare USER SPACE
- Target: store/AGENTS.md (close-out-drift bullet, 2026-08-29 addendum) ·
  Class: auto
- Change: dated addendum after the W3-overnight addendum. Enumeration for
  merge close-outs AND moot sweeps: row + worktree + branch + MAIN pane +
  every lens pane, cwd-exact; bare-shell no-agent panes = user terminals,
  never swept.
- Evidence: silas 08-28 ~19:3xZ — "w85:t1K held SEVEN orphaned lens panes —
  from #106's r2 (moot-swept mid-flight; I closed the row + worktree but
  missed its live lens panes)… a moot round sweep must close LENS PANES
  TOO"; silas 08-29 ~00:5xZ — "DEBRIS p3V (#106 r1 main — round swept but
  pane survived), DEBRIS p5E (#107 r5 main — same miss)… round close-outs
  must close the MAIN pane too — two sweeps today missed their own mains".
  User-space: w8D/w8E classified USER TERMINALS 08-27, p63 spared 08-28.
- Reasoning: the doctrine existed and still leaked ×3 in one day — the moot
  path and the main pane are the two named holes; the lens wave outlives
  the main, and the main outlives a sloppy sweep.

### P3 — A blocker carried 2+ rounds = a pipeline defect; review BYTES not claims
- Target: store/AGENTS.md (Perkins round-ops bullet, addendum item (i)) ·
  Class: auto
- Change: dated addendum item appended with P1's.
- Evidence: #107 r4 18:02Z — "B2 CARRIED (11 named goldens still stale
  pre-#106 bytes; census 116/117 swapped, ZERO warm bytes absorbed — the
  claimed one-machine settle unsupportable against committed bytes)"; relay
  "bytes-not-claims, find the re-bless pipeline defect" + "carried-blocker
  pattern flag (2 rounds same B2/B3 = pipeline defect, not luck)"; r5
  briefing — "B2 carried 3 rounds — blob-forensics the 11 named goldens
  FIRST, bytes not claims"; r5 verdict — "B2 ANSWERED — 86/117
  byte-identical to #106 warm bytes, 0.00% swap-signature".
- Reasoning: the carry count is the signal that changes the review shape —
  claim-check → byte-forensics vs the merged tree + an explicit escalation
  flag. Proven end-to-end (r3→r4 carried, r5 closed in bytes).

### P4 — MEGA-DIFF fix-deltas are mega too (blob forensics = the mechanical leg)
- Target: store/AGENTS.md (MEGA-DIFF protocol bullet, 2026-08-29 addendum) ·
  Class: auto
- Change: dated addendum after "…2 waves each).": the r2-spot-check default
  yields when the rework push is re-bless-dominated; two-class applies to
  the fix-delta; byte-claim blockers get blob forensics, not spot-check.
- Evidence: #107 r4 dispatch 13:54Z — "FIX-DELTA 88825L = mostly the
  ONE-MACHINE golden corpus re-settle; MEGA-DIFF chunking: full lens on code
  chunk, mechanical blob verification on PNG bulk (convention census +
  black-frame scan + pulse-presence)"; r5 dispatch 18:38Z — "FIX-DELTA
  88689L… do the 11 named goldens NOW byte-match the merged tree
  (blob-forensics FIRST)"; r4 verdict — "651L code chunk full lens wave; 88k
  T1 re-bless mechanical (fold-check PASS)".
- Reasoning: a mega-diff PR's rework is dominated by the re-blessed corpus;
  treating an 88k fix-delta as a spot-check under-verifies exactly where the
  carried blockers live.

### P5 — A USER RULING supersedes an APPROVED verdict (moot-by-ruling); the amend-and-relay cadence at full speed
- Target: store/AGENTS.md (user-reversal bullet, 2026-08-29 addendum) ·
  Class: auto (flagged for Gru glance — encodes the 08-28 rulings)
- Change: dated addendum after "…fix-job trigger ride the row."
- Evidence: silas 08-28 ~08:3xZ — "#106 merge HELD (no keystroke on
  df14785; the r1 APPROVED is superseded)… r1's APPROVED on the width
  implementation is now moot-by-ruling — the loop does its job; the width
  re-bless inventory (33 PNGs) is throwaway, the pulse rework re-blesses
  again"; ~09:0xZ — "4 user rulings across 2 PRs, all mid-flight, all
  amend-and-relay — zero re-dispatches" (era-1 default / local-goldens
  canon / saves disposable / glow-only pulse).
- Reasoning: the reversal doctrine stopped at "locked decisions provisional
  until the lavish gate" — 08-28 proved the gate extends past Perkins: the
  verdict blessed the spec, the user rules the spec; prior inventories go
  throwaway without complaint.

### P6 — Interactive sessions: the close shape, the main-checkout HOLD, the dead-pi salvage
- Target: store/AGENTS.md (interactive-design-sessions bullet, 2026-08-29
  addendum) · Class: auto (flagged for Gru glance)
- Change: dated addendum with three lettered facets (a/b/c).
- Evidence: (a) user-ordered cull 08-29 01:48Z closed quinn + shape-vocab —
  "record durable… future amendments = new session launched from the
  record" (supersedes "PANE STAYS OPEN by design"); (b) viscomm audit
  dispatch 08-27 19:43Z — "DETACHED at 03dd6f8 (main checkout HELD by
  mechanics-quinn — the audit must build at two commits and a HEAD move
  under quinn is the catastrophic class)"; (c) quinn 08-27 19:55Z — "pi
  died ~18:36Z right after its OPENING TURN COMPLETED… 44min dead;
  recovered: extracted the composed opening to …-opening-recovered.md,
  relaunched same pane, chained handover VERIFIED".
- Reasoning: the doctrine covered the session's life but not its death or
  its end — the record-as-amendment-surface close, the checkout-hold
  constraint on parallel forensics, and the salvage-composed-content-first
  recovery are the three missing shapes.

### P7 — Live-tree dedup under open sessions: SWAP-NOW, REMOVE-LATER (a deferred trigger keyed on a never-closing pane is broken)
- Target: store/AGENTS.md (NEW bullet, Dispatch & handover) · Class: auto
- Change: new bullet after the RT worktree-bootstrap bullet.
- Evidence: skills dedup 08-28: finlit (stale Jul-28 snapshot, 71
  only-in-repo entries) + UE (byte-clean subset, 6 real dirs) rm'd after
  census-to-ledger + zero-live-pane verification; packet-plumber main
  checkout 08-29 00:47Z — "stale Aug-5 moved to .agents/skills.stale-aug5 +
  symlink to canonical in its place — Sally's live session keeps resolving
  through the link, zero breakage… The deferred-trigger conflict (Sally
  pane never closes by design) is dissolved by the swap"; the LAST-close
  trigger fired at the 08-29 cull (final rm incl. the symlink).
- Reasoning: the swap makes the stale content inert NOW (zero disruption to
  live sessions) and degrades the deferred trigger to disk noise; the
  trigger keyed on an open-by-design pane would never have fired.

### P8 — External input is also SELF-inflicted: placeholder `pane run` in dispatch chains
- Target: store/AGENTS.md (08-27 (c) human-keystrokes bullet, clause
  addendum) · Class: auto
- Change: dated clause appended.
- Evidence: silas 08-28 ~00:25Z — "SLIP OWNED: my launch chain carried a
  stray `pane run w85:p3R 'placeholder...'` — literal junk landed as user
  input in the LIVE A1 minion pane (the 08-26 external-input class,
  self-inflicted)… one bad target in a && chain types into a live agent."
- Reasoning: the existing class covered human keystrokes; the operator's
  own && chain is the second source — cheap clause, same classification.

### P9 — Gru: ground pending-claims and ambiguous acks against live state before reporting or acting
- Target: store/AGENTS.md (NEW bullet, Dispatch & handover) · Class: auto
- Change: new bullet.
- Evidence: gru 08-27-evening — "check pane/lavish state before telling the
  user what is pending — both 'pending' prompts were already answered
  (stale-board ×2 one night)"; silas 08-28 ~09:55Z + ~14:2xZ — two bare
  user "go" relays grounded in Gru's session before acting (Sally already
  held the pill question) → continue-acknowledgment, no new dispatch, one
  confirm queued.
- Reasoning: "pending" is a claim about pane/lavish state; lavish rulings
  land without a pane signal, so a stale board misreports the user to their
  face. Weakest-evidence proposal (single night/day per flavor) — included
  on cost asymmetry; veto if it reads anecdotal.

### P10 — `herdr pane resize --amount` is a FLOAT fraction (0–1)
- Target: store/AGENTS.md (lens-tab layout doctrine bullet, clause) ·
  Class: auto
- Change: clause inserted after the empirical-resize parenthesis.
- Evidence: dream-2026-08-27 shard — "herdr pane resize --amount is a FLOAT
  fraction (0-1): integer amounts clamp the split to extremes (0.1/0.6
  ratios observed) — 0.27 moved the boundary cleanly; verify with
  `herdr pane layout` after each call".
- Reasoning: replaces an empirically-derived hole in the existing doctrine
  with the concrete fact.

### P11 — Fun-test gate FIRST FIRE: the CI-invisible crash class (confirmation clause)
- Target: store/AGENTS.md (trigger-graph bullet, fun-test line, clause) ·
  Class: auto
- Change: clause appended after "…the PP v2 belt is parked on it)."
- Evidence: box-crash-third-spawn 08-28/29 — user playtest crashed on the
  3rd spawn connection; "class CI-invisible because zero golden demos run
  box-on (playtest was the only box-on × telegraph-lead surface)"; .ips in
  hand → URGENT dispatch → PR #108 → r1 APPROVED → merged in ~3.5h.
- Reasoning: the milestone type's first live validation — a user-play gate
  is the named coverage surface for CI-blind feature lanes; future belt
  planning weighs the gate on this evidence.

### P12 — Falsify-the-premise briefings + the cross-job evidence relay
- Target: store/AGENTS.md (NEW bullet, Dispatch & handover) · Class: auto
- Change: new bullet.
- Evidence: box-crash 08-29 00:18Z — "loop closed at r1 with the briefed
  hypothesis disconfirmed on evidence" (2→4-grow disproved: box_grow
  idempotent; real chain = shadow_clone value-copy aliasing the LIVE
  allocator → double-free at topology.gen re-predict); lang-safety
  08-28 20:25Z dispatch — "lead question = falsify-the-premise", answered
  23:45Z "on the REAL crash root cause (folded in via steering relay)" —
  the sibling job's Perkins verdict relayed INTO the live research lane as
  primary evidence mid-flight (22:18Z, deferred-not-lost verified).
- Reasoning: names a briefing shape that produced two clean deliverables in
  one day — hypothesis + mandated falsification, with disconfirmation
  treated as a first-class result; and the verdict→research relay is the
  positive sibling of cross-job-flag.

### P13 — T2/rlsw addendum: the SILENT BGRA flavor, cross-machine splits, base-reproduction control
- Target: store/minion-field-notes.md (T2/rlsw entry, 2026-08-29 addendum) ·
  Class: auto
- Change: dated addendum after the 2026-08-23 addendum (dual-render facets).
  Leads with NEVER bless T2 via `odin run harness` directly (the silent
  self-consistent-green trap + symptom list + T1-sweep invisibility);
  cross-machine split rule (re-bless ALL from ONE machine, T2 loop ×2;
  settle claims verified vs merged-tree warm bytes); environment-bound
  control (re-bless the BASE in a scratch worktree before blaming the diff).
- Evidence: the-box shard 08-28 — "NEVER bless T2 goldens with `odin run
  harness` directly… the suite goes green, and NOTHING looks wrong until a
  blob-level census finds every frame carrying the swapped convention";
  "two machines blessing the same corpus… splits the corpus (116/117
  swapped vs 1 warm)"; "the pristine base (03dd6f8) re-blessed locally
  reproduces palcheck 61-fail exactly… if base reproduces, it's the render
  environment, not your diff". Recurred 08-28 despite the existing entry —
  prominence fix, not just coverage.
- Reasoning: the live entry covers only the LOUD flavor (black frame, loud
  R/B diffs); 08-28's silent flavor green-washed a whole corpus through 2
  Perkins rounds.

### P14 — shadow_clone/Odin invalid-free forensics: the pin-line half + deterministic catchers + the read-only repro recipe
- Target: store/minion-field-notes.md (08-26 shadow_clone entry, 2026-08-29
  addendum) · Class: auto
- Change: dated addendum after "…Grep the clone list whenever a
  step()-touched dynamic array is added."
- Evidence: box-crash shard 08-28 — "EVERY new Run_State dynamic array must
  add a clone line AND a pin line… box-ON fixture + raw_data pointer pins
  (box-OFF fixtures hide it… len==0 hides allocated backings)"; "grep the
  repro surface for by-value dynamic-array/struct copies feeding a destroy
  — `clone := src^` + `run_destroy(&shadow)` was the whole bug"; "`odin
  test` bad frees are REPORTED not fatal… pin ownership directly (pointer
  compares)". lang-safety shard 08-28 — "a -debug build + `breakpoint set
  -n malloc_error_break` under lldb recovers the full Odin stack in one
  run"; "Odin dynamic arrays carry their allocator in the header… caught
  deterministically by core:mem Tracking_Allocator (bad_free_callback
  carries file:line)"; the rsync-/tmp + env-gated frame-driver repro recipe
  (caught RED, proved GREEN, 8 connects).
- Reasoning: the class RECURRED on the #107 Box arrays exactly as the 08-26
  entry predicted; the pin-line half is what makes the next miss CI-visible
  instead of playtest-visible.

### P15 — Vacuity lineage: fixture-zero-data, helper-level, allocator-behavior flavors
- Target: store/minion-field-notes.md (vacuous-pin lineage bullet,
  2026-08-29 addendum) · Class: auto
- Change: dated addendum after the 2026-08-27 compact-craft addendum.
- Evidence: look-zoom shard 08-27 — "zero bboxes… zeroes the covenant cap
  and VACUATES the whole sweep (it passed crushed at cap 0)"; the-box shard
  08-28 — "a per-file reject helper that omits ONE catalog source… every
  row passes forever… fixing the helper exposed ~40 stale expectations
  (want = the MESSAGE substring)" + "audit by MUTATING one expectation to
  nonsense"; box-crash shard 08-28 — "a mutation gate must pin ownership
  directly (pointer compares), never depend on allocator abort/leak
  behavior".
- Reasoning: the #1 Perkins blocker genus added three repeatable shapes in
  two days, each with its mutation-audit recipe.

### P16 — Odin/harness semantic traps (#partial switch order, post-apply pricing, demo-directive zero-value, needle craft)
- Target: store/minion-field-notes.md (NEW dated bullet, Tooling traps) ·
  Class: auto
- Change: new bullet after the shadow_clone bullet.
- Evidence: the-box shard 08-28 — "a case inserted below the default
  silently never runs (a demolish refund priced zero and the tests still
  mostly passed)"; "pipe_slot/node_slot SKIP DEAD entities and fall back to
  slot 0… always demolish a non-zero id in refund tests"; "replace1's 4th
  arg is a COUNT… loader messages carry EM-DASHES… verify by grepping the
  inserted comment". look-zoom shard 08-27 — "zoom 0 drove scale = fit*0
  and the map grid loop drew ~forever (2.5h silent 'suite run')… a hung
  harness run with an empty log = sample the process".
- Reasoning: four distinct traps, two jobs, each already paid for once (one
  as a shipped-zero refund, one as a 2.5h silent hang).

### P17 — PP visual-evidence craft (motion-strip audits, per-era goldens, perception-vs-mechanism, harness_before-first, ALONG-feature signature, trimmed-blit halos)
- Target: store/minion-field-notes.md (NEW dated bullet, Conventions that
  saved time) · Class: auto
- Change: new bullet at the section end.
- Evidence: regression-audit shard 08-27 — "'did effect X die' audits
  resolve mechanically with harness motion-strip + a fixed-pixel
  time-series… per-era worktree goldens are free BEFORE/AFTER evidence";
  "the 4.1 congestion halo never pulsed… trace the MECHANISM and the CANVAS
  separately"; congestion-a1 shard 08-28 — "stride the evidence harness
  FIRST (bin/harness_before from HEAD)… made every A1 claim mechanically
  checkable without a second worktree"; "a band-measure leg returning
  exactly your scan half-window count is measuring ALONG the feature";
  look-zoom shard 08-27 — "The read is a HALO: radius > 0.5× footprint…
  probe map-preview with the correct fit offset".
- Reasoning: the audit→A1→pulse arc ran clean on these recipes (three jobs,
  two days); they are the repeatable craft for the whole look lane.

### P18 — FLAG-ON coverage ships at ZERO unless explicitly gated
- Target: store/minion-field-notes.md (NEW dated bullet, Recurring review
  findings) · Class: auto
- Change: new bullet at the section end.
- Evidence: #107 r3 08-28 — "ruling-1 wiring (era-1 start + 6.2 gate) ZERO
  coverage" (blocker 4); #107 r4 — "era-wiring row ships PP_DEBUG RED —
  gate the ==1 assertion on !PP_DEBUG (=3 is the sanctioned override)";
  box-crash r1 — "class CI-invisible because zero golden demos run box-on".
- Reasoning: three flavors in one day of the same gap — a ruling that
  changes shipped defaults needs wiring coverage in EVERY build
  configuration; a feature flag needs ≥1 flag-ON gate.

### P19 — Lavish decision menus: per-row radio forms + Send-&-End mechanics
- Target: store/minion-field-notes.md (lavish craft bullet, 2026-08-29
  addendum clause) · Class: auto
- Change: clause appended after "…repair + re-poll."
- Evidence: regression-audit shard 08-27 — "per-row radio forms + one Queue
  button each collected a clean per-row ruling (R1 restore-via-A1 arrived
  as a single tagged keep-leave prompt); a Send-&-End session delivers the
  final feedback once on the next poll".
- Reasoning: the input-side complement to the existing per-question Queue
  craft; the decision-menu shape produced the cleanest ruling intake of the
  window. Single-sighting but a direct continuation of a well-covered
  entry.

### U1 — Dream doctrine: date sources by CONTENT, never mtimes; a marker jump without a dream row = a coverage-gap window
- Target: playbook 'Dreaming' section + `_bmad-output/briefings/_template-dream.md`
  (Bob-facing) · Class: **user-ack** (playbook/template edit)
- Change: add to the dream pass inputs step: "Date every source by CONTENT
  (shard headers, journal dates, git log) — never by mtime: a git
  checkout/restore normalizes every mtime to the same minute. A marker that
  advanced WITHOUT a corresponding dream row flags a coverage-gap window —
  tail-read that window explicitly."
- Evidence: the 08-25 pi-restoration normalized ~200 files to one mtime
  minute (observed again this pass: every pre-08-26 shard reads 25 Aug
  16:49); dream-2026-08-27 shard — "a git checkout/restore normalizes every
  mtime to the same minute"; dream-2026-08-27 report's marker-scope note
  (the 08-23→08-25 marker jump inside 5b5de85 with no Bob pass = the DSH
  gap window, tail-read only).
- Reasoning: the marker/mtime filter is structurally blind after a restore;
  this pass's own file selection would have been wrong on mtimes alone.

### U2 — Playbook staleness: Model policy defaultProvider paragraph + VISION ROUTING section
- Target: playbook 'Model policy' final paragraph + 'VISION ROUTING'
  section · Class: **user-ack**
- Change: retire the "defaultProvider = deepseek (→ v4-flash)… briefings
  ALWAYS name deepseek/deepseek-v4-flash… Silas pinned to v4-flash by
  silas.ts" paragraph (superseded by the 08-27 ops flip to
  zai-coding-cn/glm-5.3-flash — the same section's own "Execution —
  glm-5.3-flash (ops tier since 2026-08-27)" paragraph already contradicts
  it; deepseek flash is also 402-balance-dead since 08-25 per
  quota-regime.json); sync VISION ROUTING with the 08-27 doctrine
  (glm-5.3-flash natively multimodal = inline vision, KYLE ops pin moved to
  it, glm-4.6v demoted to fallback) — AGENTS.md + vision-read SKILL.md
  carry the amendment (3085281), the playbook does not.
- Evidence: silas 08-27 ~12:45Z — "ALL NEW dispatches ride glm-5.3-flash…
  Config synced by Gru (bf09e39)"; ~13:0xZ — "flash reads images INLINE…
  KYLE 4.6v unchanged for evidence-grade work"; journals sheep verified the
  playbook text unchanged.
- Reasoning: a self-contradicting canonical section is worse than a missing
  one — minions briefed from the stale paragraph launch on a dead provider.

### U3 — Briefing template standing orders: add the own-pane exclusion (carried watch item, template gap verified)
- Target: `_bmad-output/briefings/_template.md` standing orders · Class:
  **user-ack**
- Change: amend "close every pane you spawn ('badge out')" with "— never
  your OWN pane; badge out by reporting, not by closing".
- Evidence: the 08-26 migration pane-vanish (minion self-swept its own pane
  at badge-out; work survived, recovery dispatch needed) —
  dream-2026-08-27 watch item #1 ("promote on 2nd sighting"); NO 2nd
  failure this window, but the journals sheep verified the template STILL
  lacks the clause (it only rides ad hoc in hand-authored briefs — this
  dream's own sheep briefs carried it).
- Reasoning: the failure cost is a full recovery dispatch; the fix is one
  template line; the gap is verified standing. Veto if the user prefers to
  wait for the 2nd failure.

## Watch items (anecdotes — tracked, not proposed)

1. **PR-body/commit over-claims = a serial Perkins warning class** (#107
   r3 ×3, r4 ×4 serial, r5 W4b — 1 job / 1 day): once an over-claim lands,
   Perkins re-verifies EVERY prose claim next round; the PR body becomes a
   verify-target. Graduates to field-notes on a 2nd job.
2. **Committed eyeball-crop evidence IN the PR** (#106 08-28: peak/trough
   corridor crops at 3 zoom rungs committed for the user eyeball gate; the
   user merged on it pre-r2) — the delivery vehicle for visual-gate PRs.
3. **Silas journal heredoc+fallback eats notes silently** (08-29 pre-dream
   hygiene: a typo'd path `2028-08-28.md` exited 0, the fallback never
   fired, the r3-recovery note lost ~13h) — verify journal writes landed
   (ls + tail); sibling of the rc-un-piped class.
4. **Deferred trigger keyed on a SIM EVENT** (shape-vocab: "defer to first
   era-4 third-class wave — auto re-trigger") — a new trigger substrate
   beyond merge/pane/probe; watch how it gets sensed.
5. **A named trigger released EARLY by user ruling** ("RELEASE NOW —
   merge-waiting defeats its own trigger", shape-vocab 08-28): the wait can
   defeat the trigger's purpose.
6. **User-ordered per-job MODEL EXCEPTION** (lang-safety on glm-5.3 PRO
   incl. every spawn, explicitly not flash): the exception path exists by
   user order; the spawn-pin discipline still applies.
7. **PR-body DESIGN FLAGS as the async ruling intake** (the-box: 3 flags in
   the PR body, all ruled ~2h later, folded into the rework push) — no
   session needed; sibling of lavish menus + in-pane forks.
8. **Minion self-model-switch → status flicker burst + cache re-bill**
   (look-zoom 08-27 14:12Z: idle/done/idle in 1min, 246k re-bill) —
   classify, no action; watch recurrence on every self-switch.
9. **Interactive-lane dead pis have NO watchman coverage during a herdr
   outage** (quinn 47min dead 08-27; minion panes unwatched by design) —
   the salvage recipe is promoted (P6c); the detection gap stays open.
10. **Picker-wedge recovery**: Esc+redo recovers a relay/dialog race
    in-pane (silas 08-27).
11. **`.gitignore` trailing-slash doesn't match the `_bmad` symlink**
    (the-box 08-28: `git add -A` staged the symlink; add a bare `_bmad`
    line too) — bites once per repo.
12. **harness `stats-check` needs `mkdir -p bin` in a fresh worktree**
    (the-box 08-28).
13. **PNG de-filter channel-stride must match the color type** (ch=4 RGBA
    vs 3 RGB — a step-3 walk fabricates phantom diffs; use PIL when
    available; the-box 08-28).

## Pruned / rejected candidates (with why)

- **youtube-channel creative-lane craft** (gru 08-29: Blender 5.2 gotchas,
  Seedance retention doctrine, Higgsfield MCP token crack, song-structure
  skill) — OUT OF SCOPE for orchestration memory; that lane is Gru-direct
  (not in managed-repos) and its craft belongs to the youtube-channel
  repo's own docs.
- **Sheep handovers via brief-FILES** (dream-2026-08-27 shard) — already
  covered by the KYLE spawn-craft law (prompts to FILES); this dream ran
  3/3 clean on it again (confirmation only).
- **k3-return double-probe habit / watchman riding the herdr outage /
  sensor-echo twins / moot+rebase sweeps / notification compliance gap 3rd
  sighting / shadow_clone class recurrence** — all already-covered
  doctrine, freshly confirmed; no edit.
- **arch-egress-migration ledger activity** — pre-marker (merged 08-27
  09:37Z), dreamed last pass; excluded.
- **C21 palcheck render-only fixtures** as a standalone entry — folded as
  one clause into P17 instead (single sighting, same family).
- **Gru-flash native vision as session force-multiplier** — already the
  08-27 vision doctrine; the youtube lane is a confirmation, not a pattern.

## Notes for Silas (not memory proposals)

- managed-repos.txt comment block mentions "youtube
  (isaacharrisholt/youtube)" which no longer exists under ~/code — one-line
  hygiene fix at close-out (gru 08-29, Stale).
- U1–U3 await the user's ruling via Gru; the store copies carry ONLY the
  19 auto proposals, diff-ready.
