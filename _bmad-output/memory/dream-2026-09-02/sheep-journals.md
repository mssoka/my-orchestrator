# Sheep shard — sheep-journals (dream-2026-09-02)

Sources: gru-journal/2026-09-01.md, silas-journal/2026-09-01.md,
silas-journal/2026-08-31.md (post-marker ≥ 22:13:41Z only: the ~22:2xZ
dream close-out + the ~00:1xZ +1d funfix dispatch). Pre-marker 08-31
entries (playtest squad ×4 + dream dispatch) read for context only —
already dreamed by dream-2026-08-31.

Already-recorded checks grepped against `/Users/moses/code/AGENTS.md`
and `/Users/moses/code/docs/minion-field-notes.md` (read-only).

## NEW lessons

- **Wrong-base PR recovery = `gh pr edit --base`, not rebase (when the true
  base hasn't moved).** Example: funfix #125, 2026-09-01 ~00:5xZ — "The
  funfix minion opened #125 vs MAIN (gh pr create default-branch miss) =
  permanently DIRTY vs the wrong lane; origin/v2 had NOT moved (61ea014 =
  the branch base). Fixed by retargeting (gh pr edit --base v2):
  OPEN+MERGEABLE, no rebase needed." Two halves: (a) minion craft — on a
  non-default-base lane, `gh pr create` MUST carry `--base <lane>`
  explicitly (the minion was informed of the rule); (b) orchestrator
  recovery — a wrong-base PR where the true base never moved is a
  retarget, not a rebase/re-dispatch. Proposed target:
  `docs/minion-field-notes.md` (the --base rule) + `AGENTS.md` Ledger/PR
  gotchas (the retarget recovery). Check: **MISS** both stores (no
  "wrong-base", "--base", "retarget", "default-branch" hits). NEW.

- **Handovers for PR jobs must PIN the self-report ledger row id.**
  Example: funfix duplicate-row catch, 2026-09-01 ~07:5xZ — "my dispatch
  row packet-plumber-funfix-118-124 sat stale at working|w85:p6K, while
  the MINION self-created pp-funfix-118-124 and ran the whole live
  lifecycle on it… ROOT: I briefed the minion without pinning its
  self-report ROW ID — it invented the short name." Prescription (Silas',
  verbatim): "your ledger row is <id> — self-report THAT id" goes in
  every PR-job handover (no-PR handovers already carry "Silas owns
  transitions"). Proposed target: `AGENTS.md` — extends the 08-14
  self-create gotcha (line ~1103) with the preventive prescription; the
  existing entry only says "reconcile to ONE canonical id" after the
  fact. Check: **PARTIAL HIT** — the self-create CLASS is recorded
  (AGENTS.md 1103–1120); the row-id-pinning-in-handover prescription is
  absent ("self-report THAT" no hit). NEW facet / addendum to the
  existing gotcha.

- **Downscale review images BEFORE reading them into context.**
  Example: gru-journal 2026-09-01, Blender lesson #13 — "full 1920×1080
  PNGs 413 the harness and bloat context to compaction (960×540
  review_small.png is plenty for staging verdicts)." Cross-lane: any
  agent reading its own screenshots/renders/captures with the read tool
  should emit a downscaled review copy first — full-res images both 413
  the harness and burn context toward compaction. Proposed target:
  `docs/minion-field-notes.md` (craft). Check: **MISS** ("downscale",
  "413" — no hits). NEW. (Sibling to the KYLE/vision craft in AGENTS.md,
  but that covers verdict quality, not the reader's own context cost.)

- **A tool/bridge timeout is a CALL timeout, not a job failure — check
  the output artifact before assuming.** Example: gru-journal 2026-09-01,
  Blender lesson #11 — "Bridge timeouts ≠ failure — long Cycles renders
  finish server-side; check the output file before assuming."
  Cross-lane: long server-side jobs (renders, generations, batch runs)
  complete despite the MCP/tool call timing out; verify via the artifact
  before retrying or declaring failure. Proposed target:
  `docs/minion-field-notes.md` (craft). Check: **PARTIAL** — AGENTS.md
  ~1363 has the lens-turn flavor ("long turns hit 500s / timeouts…
  findings land on disk even when the final message errors"), same
  shape, different substrate; the generalized minion rule is not in
  field-notes. NEW (field-notes), sibling already in AGENTS.md.

- **Acquired assets are session-state until persisted — save IMMEDIATELY,
  and know which save is ground truth.** Example: gru-journal 2026-09-01,
  lessons #1/#2 — "Downloads are session-state; open_mainfile discards
  unsaved imports. The Muwanga desk and the Sanyo recorder each vanished
  TWICE this way… never open_mainfile between a download and its save"
  + "Bridge saves are unreliable; the user's GUI Ctrl+S is ground
  truth." Cross-lane form: imports into a live tool session are volatile
  until an explicit persist; never run a destructive context switch
  between acquisition and save; when the programmatic save is flaky,
  identify and use the ground-truth persistence action. Proposed target:
  `docs/minion-field-notes.md` (tool/asset craft). Check: **MISS**
  ("session-state", "Ctrl+S" — no hits). NEW, moderately Blender-shaped;
  journal is the primary home, extract the generalized rule only.

## Watch items (single sightings)

- **Named slots/registries can silently hold the WRONG content — verify
  contents before building on them.** gru-journal 2026-09-01, lesson #17 —
  "A library slot can silently hold the WRONG asset — A_sedan was my
  hand-built box all along; the real Chrysler had been eaten to 2 orphan
  meshes. Verify a slot's materials/contents before staging from it."
  Generalizes (branches, worktrees, registry rows, library slots): names
  lie, contents are ground truth — sibling spirit to "ground
  pending-claims against live state" (AGENTS.md). Proposed target:
  `docs/minion-field-notes.md` as a watch line. Check: **MISS** (the
  field-notes "slot" hits are unrelated ADK/pipe-slot entries).

- **Bob row hygiene: a dream row hitting `in-review` is a wrong
  transition.** silas-journal 2026-08-31 ~22:2xZ — "Bob stray in-review
  corrected." Dreams are no-PR jobs; the row should go working → done.
  Single sighting, thin — watch item for the dream template (if the
  template's badge-out tells Bob to set in-review, that's the root).
  Proposed target: `AGENTS.md` dream-ops, watch only. Check: **MISS**
  ("Bob stray", "in-review corrected" — no hits).

## User-ruling / policy items (user-ack class — Gru/user territory)

- **Video-lane ruling cluster (2026-09-01/02, all user): PLATA O PLOMO
  style ruling, CHARGE ruling, FOCUS LOCK.** Realistic CGI over
  cartoon-lead (audience grounds: "cartoon-proportioned leads read as
  kids' content at thumbnail size"); then CHARGE supersedes it:
  "CHARGE (Blender Studio open movie) is the BASELINE… EEVEE is
  sanctioned — craft (lighting, acting, grade) beats engine" + "FOCUS
  LOCK: the first two scenes ONLY… until the user unlocks." These are
  lane rulings; the gru-journal IS their durable home (per brief scope).
  Two forms with cross-lane value worth surfacing to Gru/user:
  (a) the quality bar anchored to a NAMED REFERENCE ARTIFACT ("X is the
  baseline") — a ruling form that terminates abstract look debates
  (echoes the 08-20 pixel-first LOOKS-primary ruling);
  (b) FOCUS LOCK as a user-imposed scope mechanism — a minion lane
  stays locked on named deliverables until the user unlocks.
  Proposed target: user-ack / Gru territory (lane canon); no store edit
  from the dream. Check: **MISS** ("CHARGE", "FOCUS LOCK" — no hits;
  expected, lane-scoped).

- **ASSETS-FIRST + IMPACT AUDIT (user rulings, standing, video lane).**
  gru-journal 2026-09-01 lessons #19/#18 — "search Sketchfab/Polyhaven
  for an existing asset BEFORE building anything… Every hand-built piece
  is a failure of search, not a shortcut" + "after ANY placement change,
  run a pairwise bbox overlap check against neighbors BEFORE
  rendering/committing." Lane-scoped rulings with generalizable forms
  (search-before-build ≈ existing-libs-first; mutation-audit in a shared
  space). Proposed target: user-ack (lane canon in journal); optionally
  one generalized field-notes line if Gru ratifies. Check: **MISS**.

- **Asset licensing policy recorded (video lane).** gru-journal
  2026-09-01 — "Polyhaven = CC0 (no attribution); Sketchfab = CC-BY →
  attribution registry owed for the video description; NC licenses
  skipped (monetized channel)." Policy item for any asset-sourcing lane
  on a monetized surface: license registry + NC exclusion. Proposed
  target: user-ack / lane canon (journal is home). Check: **MISS**
  ("licens", "attribution" — no pattern hits).

- **P4 from dream-2026-08-31 (video-lane routing facts crossing the
  youtube-scope line) is still user territory.** silas-journal
  2026-08-31 ~22:2xZ escalated it; nothing in-window shows a user ruling
  on it. P5 (self-notify checklist-gate) by contrast has LANDED — see
  confirming items. Proposed target: none (Gru tracks). Check: "youtube"
  MISS in AGENTS.md — video-lane routing lives in the journal.

## Confirming sightings (already recorded — no new lesson)

- **Fun-test loop closed end-to-end (first full cycle).** silas-journal
  2026-09-01: #125 r1 APPROVED (~01:4xZ, mutation-tested: "grace
  400->900, revert experiment death 51.65->26.65s") → user merged
  e50e9a8 07:33Z → pp-funtest-r2 RELEASED per the trigger graph
  (~07:45Z, paneless held row, blocked_by=funfix-118-124, release = PR
  merge) → gate YES on both (~08:3xZ: "era-3 WINNABLE-WITH-GOOD-PLAY
  (5/7 runs won)… HEALTH RECOVERABLE (trough 46% -> heal 100% -> win)").
  Extends the fun-test gate record (AGENTS.md ~1415 + the 08-31 squad
  addendum) past "issues filed → fix-first-then-re-test" to the actual
  fix→merge→re-test→gate-YES closure. **HIT** (existing doctrine) —
  worth an addendum line recording the loop's first completed cycle and
  that the re-test leg encodes cleanly as a standard held row.

- **P5 self-notify checklist gate: FIRST FIRE — WORKED.** silas-journal
  2026-09-01 ~08:3xZ — "Self-notify EXECUTED with pasted shown:true -
  the P5 checklist gate worked first try" (pp-funtest-r2 handover).
  Updates the 08-31 addendum's "compliance gap is the DEFAULT… Silas
  verify-and-fire is the only reliable guard" (AGENTS.md ~888–894): the
  checklist-gate form is now field-proven once; verify-and-fire stays
  until more fires accumulate. **PARTIAL HIT** (the need was recorded;
  the success is new evidence) — addendum line.

- **MEGA-DIFF on the funfix delta (93,959L corpus re-bless).**
  silas-journal 2026-09-01 ~00:5xZ/~01:4xZ — canonical local diff +
  chunked lens waves; "code chunk 737L full-lens, bulk mechanical… 6/7
  lenses (blind disclosed), 19/19 confirmed." Third sighting of the
  re-bless-heavy mega-delta class. Also: r1 itself mutation-tested the
  acceptance claims' load-bearing numbers (not just r2 fix-audits) —
  marginal extension of the mutation standard. **HIT** (AGENTS.md
  982–999, 928–945, blind canary ~955). Note-only.

- **Briefing model line stale again.** silas-journal 2026-08-31 ~00:1xZ —
  "flash verified (brief deepseek line stale — corrected)" on the funfix
  dispatch. Another "template model lines rot" sighting (AGENTS.md
  ~543). **HIT.** Note-only; reinforces the dispatch-time model check.

- **Pane id re-captured post-move.** silas-journal 2026-08-31 ~00:1xZ —
  "pane w85:p6K (id re-captured post-move)". Existing workspace-move
  gotcha (AGENTS.md ~1277). **HIT.** Note-only.

- **Dream close-out ran clean (14 min, k3, marker 22:13:41Z, P1–P3
  autos committed).** silas-journal 2026-08-31 ~22:2xZ. Standard cadence
  record. **HIT** (no new pattern).

## Scope note

The gru-journal 2026-09-01 19-item Blender craft list + the rig-war
recipes (CloudRig pipeline, numpy distance-field skinning, GLTF pose
craft) are the VIDEO LANE's own durable craft record — the journal is
their home per the brief; only items with cross-lane value were
extracted above (downscale-before-read, timeout≠failure,
session-state saves, wrong-slot verification, and the generalizable
ruling forms).
