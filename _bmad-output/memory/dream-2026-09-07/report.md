# Dream report — 2026-09-07

Material: 9 field-note shards (8 job shards dated 09-05/06 + the
gdd-amend-levels backfill written 09-05 01:46, content-dated 09-04 — the
late-written class), 3 journal files mined (gru 09-04 lines 161-307 backfill
POSITIVE — 09-05 content at the tail; gru 09-06 full; silas 09-03 lines
185-627, entries 09-05 00:1xZ → 09-07 00:1xZ), 321 ledger events across 42
jobs (`ledger show` on 11 heavy rows), since 2026-09-05T00:09:06Z.

Sheep: 3 (shards / journals / ledger), all kimi-coding/k3, provenance
verified (modelId=k3 ×3 in session jsonls), shards on disk, all panes
closed at their finish.

The window: the **PP3D look-lane belt** (alive-planet 6-round loop + hard
user correction → merged; l1-look-parity LEAN SWAP merged #16; l1-refine-1
PR #17 with Perkins r1/r2 both CHANGES_REQUESTED; alive-planet-fold parked
then folded as riders), the **RTA modernization chain** completing
(38-sweep → single-source → tf-in-ci #183 R3 → wif-durable #186, the
bootstrap chicken-egg resolved by user-hand gcloud), the **k3 weekly cap
ending** (restored 09-06 ~09:4xZ; a 5h-wall flavor surfaced mid-window),
**Silas' COO model ruling** (deepseek-v4-flash always, + the PI_MODEL=k3
leak root-caused and hardened), 4 GDD-amend doc lanes with lavish gates,
3 Silas self-edit micro-PRs.

## Proposals — AUTO (applied to store copies; live mirror + commit are
Silas' close-out per this briefing)

### A1 — k3 5h-cap mid-round retry + the glm-only 1302 spawn tax
- Target: `AGENTS.md` (Provider incidents, dated addendum) · Class: auto
- Change: new addendum — the 5-HOUR wall lands BETWEEN probe and wave;
  mid-round cap death = sweep + preserve attempt-1 artifacts
  (`<round>-attempt1-k3-403/`) + RETRY THE SAME ROW on glm-5.3 at the same
  sha (attempt-N, never rN+1, VISION CAVEAT rides); freed windows RE-CAP
  ~90 min → route long rounds to glm proactively; under glm-only load 1302
  is a ~1-per-spawn tax on the round MAIN (dies post-spawn, lenses
  survive) — classify by transcript, ONE continue per dead pane, never a
  re-dispatch.
- Evidence: alive-planet r4 15:10:49Z + r6 18:03:51Z (both mid-round cap
  deaths, same-row retries); tf-in-ci r1 13:22Z etc. (~1 continue/round
  across 5+ rounds); 21:47Z quota flip.
- Reasoning: the 09-04 addendum covers the weekly cap; the 5h flavor +
  attempt-N mechanics + spawn-tax frequency were learned expensively this
  window and change dispatch/recovery decisions on the next cap.

### A2 — the QUOTA-FLIP injector joins the stale-echo family
- Target: `AGENTS.md` (Watchers — stale-echo gotcha, dated addendum)
  · Class: auto
- Change: probe flips re-fire already-acted events; same-status note with
  the sha + action verbatim, never a second action.
- Evidence: alive-planet 15:49:02Z + 16:47:32Z; tf-in-ci 15:50:31Z sensor
  race; router-family 02:02:51Z; perkins-r6 18:48:19Z (×7 window-wide).
- Reasoning: the 08-01/02 echo doctrine didn't name the quota-probe
  injector (added 08-18); naming it stops a future flip from triggering a
  double dispatch.

### A3 — CLAIMED-BUT-DIDN'T-LAND is a first-class fix-audit hunt leg;
constant EXTRACTION can silently INVERT
- Target: `AGENTS.md` (Perkins round ops, dated addendum) · Class: auto
- Change: fold commits claimed pins get grep + mutation verified ("the pin
  must be IN THE SUITE, not the commit message"); every extracted constant
  needs a value pin — the suite cannot see an inversion.
- Evidence: alive-planet r3/r4/r5/r6 (river-width pin claimed 4 rounds,
  never written); tf-in-ci r2 (header + tripwire both false); l1-refine-1
  r2 (ISLET_TOP_FRAC 0.38→0.62 inverted, suite green).
- Reasoning: extends the vacuous-pins/mutation-leg canon with the two new
  failure mechanisms that actually produced this window's blockers.

### A4 — the user-play gate hardens into round ops (HOLD note + merge click
ratifies)
- Target: `AGENTS.md` (Perkins round ops, dated addendum-b) · Class: auto
- Change: (a) USER PLAY/LOOK SESSION IN PROGRESS → HOLD note on the row,
  no sweeps/pane closes until the user reports done (Perkins runs
  mechanical-only in parallel); (b) the user's merge click ratifies a
  disclosed aesthetic deviation.
- Evidence: l1-look-parity 19:59:22Z (play-session hold); l1-arpanet
  18:12:59Z; alive-planet 19:03:42Z (merge = aesthetic ruling); art-
  integration (fresnel ratified at merge).
- Reasoning: the E1 precedent (play = look verdict) now has operational
  teeth; without the HOLD note a close-out can sweep a worktree the user
  is actively looking at.

### A5 — HELD round on a CONFLICTING/rebasing PR: dead-sha verbatim +
close-by-FRESH-CENSUS
- Target: `AGENTS.md` (unstable-target hold gotcha, dated addendum)
  · Class: auto
- Change: pre-create the HELD row with the pre-rebase sha named DEAD
  verbatim + release trigger; mid-round head-move sweeps close by fresh
  cwd-matched CENSUS (never remembered ids — orphaned lens processes
  persist at dead cwds), then re-create the round main + verify modelId.
- Evidence: router-family r1 01:33:48Z (43516f3 DEAD → 859e2e1 APPROVED);
  alive-planet r1 23:04:14Z (fa21cf3 → d7edd8a); wif-durable r1
  11:53:18Z; silas journal "3 incidents now" on census sweeps.
- Reasoning: the 08-11 hold doctrine meets the force-push flavor; the
  census rule fixes the remembered-id drift that orphaned waves.

### A6 — held rows are the AMENDMENT SURFACE; predecessor rows carry the
successor note
- Target: `AGENTS.md` (Orchestration upgrades — trigger graph, dated
  addendum) · Class: auto
- Change: fold user rulings + Perkins-warning scope into the staged
  briefing DURING the hold; release RE-READS the amended briefing +
  re-resolves the head; each predecessor row carries its successor's note.
- Evidence: model-single-source 09:32/10:19/12:24Z; tf-in-ci 13:33Z; RTA
  3-link chain in one day; l1-look-parity v2 LEAN-SWAP rewrite mid-hold.
- Reasoning: makes the trigger graph the amendment path (no kill-and-
  redispatch), with the release step that makes amendments land.

### A7 — relay delivery grep races the session FLUSH
- Target: `AGENTS.md` (deliverable-relay gotcha, dated addendum)
  · Class: auto
- Change: a 0-hit grep seconds after a relay is a pre-flush miss — wait +
  re-grep before resending; a resend double-queues.
- Evidence: silas journal ×3 — "first grep ran pre-flush (0 hits), second
  found it in BOTH sessions" (09-05); "never resend on a pre-flush miss"
  (09-06 19:0xZ); "first grep 0 = flush race, second 1" (09-06 19:3xZ).
- Reasoning: the 08-22/23 relay-verification doctrine gains its false-
  negative rule; without it, verification itself causes duplicate relays.

### A8 — KYLE corroborates USER SCREENSHOT CRITIQUES before relay
- Target: `AGENTS.md` (KYLE gotcha, dated addendum) · Class: auto
- Change: on look lanes, KYLE evidence-grades the user's visual report
  before the amendment is relayed — the amendment carries both.
- Evidence: alive-planet hard correction 09-05 ("not sure the references
  were looked at" → KYLE verified barren-water-world/clipping/
  desaturated); L1 look session 09-06 (SRI slab float+tilt, tipped ring,
  11px captions).
- Reasoning: the standing KYLE-screening canon + this window's shape =
  the two-layer contract (user's eye reports, KYLE grades, amendment
  carries both).

### A9 — env model vars beat setModel pins; errored turns revert to the
env model
- Target: `AGENTS.md` (Model dispatch gotcha, dated addendum) · Class: auto
- Change: identity-pane relaunches clear PI_MODEL/PI_PROVIDER and pin
  --model; a live /model correction reverts on the next errored turn.
- Evidence: gru 09-06 — silas.ts set flash 11:47:20, leaked PI_MODEL=k3
  overrode 11:47:27; the 12:05Z correction reverted at 12:07Z.
- Reasoning: the playbook carries the hardening; AGENTS.md carries the
  mechanism (the gotchas are the persona-facing memory). One-paragraph
  cost, prevents re-diagnosis.

### A10 — Silas self-edit lanes (pr_review=0, receipt contract)
- Target: `AGENTS.md` (Dispatch & handover, new bullet) · Class: auto
- Change: record the shape: verbatim content from the ruled source, receipt
  contract verified in the diff, self-test for tooling changes, sensor-
  blind close-out (sweep wt+branch; pull --ff-only on live main), PR
  bodies from a FILE never a heredoc.
- Evidence: orchestrator #17 (deepseek pin), PP3D #15 (parked eras), RTA
  #187 (deferred-wif note) — all 09-06, verified in silas journal 499/
  535/543.
- Reasoning: a new standing execution shape used 3× in one day; recording
  it makes the next one checklist-grade.

### A11 — never guess PR NUMBERS (row `pr` field first)
- Target: `AGENTS.md` (anchor-id gotcha, sibling line) · Class: auto
- Change: one line — a guessed #9 vs the row's #180 sent a verify to the
  wrong PR; read the row's `pr` field first.
- Evidence: silas 09-05 ~09:5xZ.
- Reasoning: same family as never-guess-anchor-ids; cheap and permanent.

### A12 — lens-tab resize semantics sharpened (ratio DELTA)
- Target: `AGENTS.md` (lens-tab doctrine, dated addendum) · Class: auto
- Change: --amount is a ratio DELTA on the boundary adjacent to the
  addressed pane edge; 7-pane ladder evened 7×31-32 in one pass, live
  round untouched.
- Evidence: 09-06 startup ops (perkins-r2-lenses ladder 6/1/7/14/27/55/
  110, user-flagged).
- Reasoning: sharpens the 08-23 empirical-semantics note with the precise
  rule, halving future resize iterations.

### Field-note promotions (minion-field-notes.md) — 10 entries
- Target: `docs/minion-field-notes.md` (6 Tooling traps + 4 Conventions)
  · Class: auto
- Change (Tooling traps): (F1) gh pr `--body-file` FIRST — heredoc quoting
  dies on apostrophe/backtick-rich markdown (alive-planet "×3 now" +
  cumulative); (F2) godot MCP LSP not ground truth — main-checkout-rooted
  + stale pre-move cache; disk cache + pkill-respawn (l1-topology-font +
  scene-refactor); (F3) editor-viewport captures — occlusion throttling →
  fullscreen; md5 NOT a determinism gate (±1px dock drift) → structural
  pixel diff w/ noise floor (same 2 jobs); (F4) bmad render-waiver path —
  read step files/review-prompts directly when render_skill.py absent,
  improvise placeholders, waiver note in PR (model-single-source +
  tf-in-ci); (F5) GCP IAM verify-or-don't-claim — role memory wrong both
  directions, viewer≠read-only, --format=json reads, rerun-after-fix-
  timestamp = fix was wrong (tf-in-ci r1/r2 + prod triage, 2 days);
  (F6) maiden-voyage CI red = bootstrap-ordering first; cancelled renders
  as fail in gh pr checks (RTA #185/#190 + wif, 2 days).
- Change (Conventions): (F7) column-aligned markdown — python-build +
  width-assert BEFORE, re-render after (alive-planet + levels); (F8)
  canon amendments grep OLD phrasings + date-stamp supersede at EVERY
  site (alive-planet + cumulative); (F9) scope-guard courtesy — adjacent
  finds flagged for a ruling, never silently fixed (×3 gdd-amends);
  (F10) lavish decision forms — per-row radios + one Queue button +
  pros/cons explainers (levels + era-costume).
- Reasoning: every entry is a cross-job (≥2 sightings) minion-craft
  lesson; the two Godot capture/LSP pairs and the two gh-body-file
  sightings each cost a real failure to learn.

## Watch items (anecdotes — tracked, not proposed)

- **Fresh-checkout reproduction is the arbiter of breakage claims** —
  l1-refine-1's stale .godot cache manufactured "deleting textures breaks
  4 glb imports" evidence; Perkins' fresh-checkout repro disproved it; the
  minion's retraction was honest and the purge shipped. Strongest
  single-sighting candidate this window — promote at its 2nd sighting.
- **Mutation-test craft on macOS** — BSD sed has no `0,/re/` (silently
  mutates nothing) and `git checkout --` nuked real unstaged edits
  (model-single-source). python replace + cp backup + diff-verify.
- **Godot @tool placeholder-instance trap** — editor-hint paths construct
  via .new(); caught only by pixel forensics (scene-refactor).
- **Godot 4.7 silent input failures** — FontVariation fourcc keys;
  project.godot `;` not `#` (l1-topology-font).
- **TF invariant tests strip whole-line comments** before substring
  asserts (wif-durable); unanchored strips corrupt HCL strings.
- **Pre-commit linters run after message-drafting** — run the hook's
  linter on touched files BEFORE committing (wif-durable, ruff F541).
- **python repr() for exact edit anchors** when rendered views
  mis-transcribe inline-code/dash runs (era-planets).
- **Frame atlas as durable look canon** — 1fps atlas + HTML grid, citation
  -grade amendments (alive-planet lane, 3 applications; single lane).
- **Priority inversion: park-by-sweep / un-park-by-fold** — mid-work lane
  parked (nothing committed lost), scope folded as named riders into the
  successor ("one heist, one round") (PP3D 09-06).
- **Rows "HOLDS until X merges" need board-sweep reconciliation** — the
  PR watcher misses the dependent merge; prod-scale-to-zero's close-out
  was ~2 days late.
- **CI-fix PRs are self-proving; paths-filters exempt the fix PR from the
  workflow it fixes** (ci-concurrency-fix #191).
- **Minion divergence from the dispatch prescription** — endorse-in-
  escalation with veto offered (wif-durable custom-role route).
- **Early-turn abort at boot (stopReason=aborted)** — one continue,
  nothing more (alive-planet-fold 19:04:59Z).
- **Full pane death with lane state on disk = zero-loss** (h3 queue;
  confirms the 08-30/31 marker-file lane contract).
- **Parallel same-repo lanes: name the cross-lane precedence rule for
  shared files up front** (topology-font + alive-planet RADIUS caveat,
  both 09-05 — thin, same-day).
- **User shepherds panes during a Silas outage** — stray keystrokes + a
  user /model flip on a round main; reconcile provenance at startup.
- **PRUNE MANDATE offered by Gru, unruled** (09-04 late) — dreams would
  propose compaction candidates at the same ≥2-sighting bar; cuts stay
  user-ack. Bob-relevant: awaiting the user's ruling.
- **Chatty-OK matcher (U3, dream-09-04) still burning** — 5+ false-read
  re-probes this window; the content-aware matcher fix stays OWED.
- **Bob close-out hygiene recurring** — the stray in-review self-report
  corrected at close-out is "the recurring Bob pattern"; keep the
  completion-gate checklist (commit + PUSH).

## Pruned / rejected candidates (with why)

- **herdr agent wait syntax** — canon since dream-2026-08-19 (0.8.0
  rename); two shards re-discovered it this window. The only new fact
  (`--until done` fires only in background panes) doesn't merit an
  append. Signal: the skill doc still names the dead form — that's a
  doc-side fix, not a memory fix.
- **Review-anchor discipline held** — the 09-02 fetch-the-anchor doctrine
  operated as written ×2 (router-family, scene-refactor); confirmations
  with zero new rule.
- **PI_MODEL leak + COO deepseek ruling (the bulk)** — durable execution
  already landed in the playbook's Silas section 09-06 (verified in the
  live playbook before writing this); only the mechanism (A9) earns an
  AGENTS.md line.
- **User = aesthetic verdict (core doctrine)** — canon via the E1
  precedent (dream-09-04); only the HOLD-note + merge-ratifies operational
  facets earned A4.
- **1302/auto-retry base doctrine** — canon (08-19/08-27/08-29); only the
  glm-only frequency + main-dies-lenses-survive signature earned their
  lines inside A1.
- **Trigger-graph base mechanics** — canon (orchestration upgrades);
  only amendments-ride-held-row + successor-note earned A6.
- **pr-field self-set streak** — the 08-11→09-04 guard trajectory held
  (10+ gap-free); the verify-and-set guard stays, nothing new to add
  beyond A11's sibling line.
- **RTA WIF principalSet trap + GCS pre-1.10 locking** — real but
  repo-family-scoped terraform facts; they live in the RTA shards +
  tripwire tests; F5 carries the generalizable verify-or-don't-claim
  lesson they instantiate.
- **Least-privilege maiden-voyage audit + repo-truth≠deployed-truth** —
  RTA-arc-scoped (3 sightings, one chain); folded narratively into F5/F6's
  evidence, not promoted standalone.

## Application status

Store copies edited: AGENTS.md +12 dated addenda (A1-A12, ~110 lines);
minion-field-notes.md +10 entries (F1-F10, ~80 lines). Live store NOT
touched (this briefing's mandate: store copies only — Silas close-out
applies autos to the live files, writes the marker, and commits). All 3
sheep badged out + panes closed. Verified: no pane from this dream remains
(w85:pJ9/pJA/pJB closed; only Bob's pane w85:pJ8 lives until close-out).
