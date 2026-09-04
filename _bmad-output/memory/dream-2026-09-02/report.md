# Dream report — 2026-09-02

Material: 3 shards (pp-playtest-fun, pp-funfix-118-124, dream-2026-08-31),
3 journal files (gru 2026-09-01; silas 2026-09-01; silas 2026-08-31
post-marker entries) + 3 backfill tail-reads (gru 08-31, silas 08-29,
silas 08-30 — zero post-marker content, confirmed not re-mined),
34 ledger events across 5 jobs (independent count by sheep-ledger),
since 2026-08-31T22:13:41Z.

Sheep: 3 (shards / journals / ledger), all k3, provenance verified
(modelId=k3 ×3), shards on disk, panes closed.

The window: the fun-test re-test aftermath (3.5 → gate-YES arc, issues
#126-#128, r2 comments on #119/#121/#122), the docs-p4-p5 PR (#16,
still OPEN), the video-lane records (gru 09-01: PLATA O PLOMO style
ruling, asset-library day, CHARGE ruling), the skills-swap completion
(verified: packet-plumber/.agents now empty — the SWAP-NOW
REMOVE-LATER deferred trigger fired at lane close).

## Proposals

### P1 — PP PRs always `--base v2`; wrong-base recovery = retarget, not rebase
- Target: `AGENTS.md` (new gotcha, Dispatch & handover) · Class: auto
- Change: new bullet after the RT-bootstrap gotcha — `gh pr create`
  silently targets the repo default; on the v2-lane repo that's main =
  permanently DIRTY vs the wrong lane; recovery = `gh pr edit --base
  v2` (no rebase when the branch descends from origin/v2); briefings
  NAME the base.
- Evidence: pp-funfix-118-124 2026-09-01T00:45:08Z (#125 opened vs
  main, retargeted by Silas, OPEN+MERGEABLE in one edit) +
  2026-09-01T00:50:48Z ("standing rule: packet-plumber PRs always
  --base v2") + the pp-funfix shard. All three sheep flagged it
  independently.
- Reasoning: the trap is structural (gh defaults to the repo default
  branch) and the briefing carried no base — not recording it
  guarantees a repeat; the recovery half (retarget ≠ rebase) saves a
  needless rebase/re-dispatch next time.

### P2 — Self-create gotcha: the CANONICAL-FLIP flavor + pin the row id in the handover
- Target: `AGENTS.md` (addendum to the 2026-08-14 self-create gotcha)
  · Class: auto
- Change: 2026-09-02 addendum — minion looked up the SHORT id, found
  nothing, self-created (its "dispatch add was missing" claim was
  FALSE — the row existed as `packet-plumber-funfix-118-124`), ran the
  ENTIRE lifecycle on it; the stale dispatch row fed a post-merge
  watcher echo. New sub-facts: self-created rows default `base: main`
  on a v2-lane repo; the durable fix is dispatch-side — the handover
  pins "your ledger row is <id> — self-report THAT id".
- Evidence: pp-funfix-118-124 2026-09-01T00:08:38Z +
  packet-plumber-funfix-118-124 2026-09-01T07:43:09Z (reconciled per
  the 08-14 doctrine) + silas-journal 09-01 ~07:5xZ (root cause named).
  3rd sighting of the class (08-14 ×2, this).
- Reasoning: the class keeps recurring with new flavors; the
  prevention (row id in the handover) is dispatch-side and cheap.

### P3 — Fun-test loop: first FULL cycle closed (gate YES)
- Target: `AGENTS.md` (addendum to the fun-test gate block) · Class: auto
- Change: one dated addendum — fix PR #125 r1-APPROVED + merged
  (e50e9a8) → held re-test row released on cue → GATE YES on both
  metrics vs the 3.5/10 baseline; #126-#128 + r2 comments on
  #119/#121/#122; the working shape = gate metric defined up-front in
  the held row's note, release = the fix PR's merge.
- Evidence: pp-funtest-r2 2026-09-01T07:39:59Z (released) +
  2026-09-01T08:19:59Z (done, gate YES: 5/7 surge wins, 46%→100%→win).
- Reasoning: the 08-31 addendum ended at "fix-first-then-re-test" as
  INTENT; the first completed cycle + the shape that worked is the
  durable template for future fun-test loops.

### P4 — Self-notify checklist gate: field-proven ×2 the next window
- Target: `AGENTS.md` (addendum to the 2026-08-31 compliance-gap
  addendum) · Class: auto
- Change: dated addendum — both window completions self-notified with
  the PASTED `shown:true` (2/2 vs 0/3 the day before); the gate rides
  PR #16; verify-and-fire stays until the trend holds past its merge.
- Evidence: pp-funtest-r2 2026-09-01T08:19:59Z ("Self-notify EXECUTED
  shown:true pasted") + orchestrator-docs-p4-p5 2026-08-31T23:45:14Z
  ("notification gate EXECUTED with shown:true pasted").
- Reasoning: the 08-31 addendum closes on "compliance gap is the
  DEFAULT" — the very next window contradicts the default under the
  new form; future readers need the trend state, not the despair.

### P5 — Review-URL gotcha: the EMPTY-anchor flavor
- Target: `AGENTS.md` (addendum to "Never guess review-URL anchor
  ids") · Class: auto
- Change: dated addendum — a close-out wrote "r1 posted as formal
  review: ." (URL missing entirely); a placeholder is record-loss —
  FETCH the review id at close-out and write the full URL.
- Evidence: pp-funfix-118-124-perkins-r1 2026-09-01T01:29:27Z (empty
  URL in the working note; done note "review: posted-on-PR-125").
- Reasoning: 5th flavor of the anchor-loss family (guessed ×2,
  truncated ×2, empty ×1); the permanent ledger lost the anchor.

### P6 — Model lines rot in HAND-AUTHORED briefings too
- Target: `AGENTS.md` (addendum to the model-dispatch gotcha's 08-13
  addendum) · Class: auto
- Change: dated addendum — the funfix brief named deepseek ops four
  days after the 08-27 retirement; the dispatch-time correction layer
  caught it; verify the model line at dispatch even on same-day
  briefs.
- Evidence: packet-plumber-funfix-118-124 2026-08-31T23:54:22Z (MODEL
  NOTE) + pp-funfix-118-124 2026-09-01T00:08:38Z (minion-side
  correction).
- Reasoning: the recorded rot flavors were template-inherited; this
  proves hand-authorship is no protection — the dispatch-time verify
  is the only net.

### P7 — Flash-era Perkins: blind retry can fail on a PROVIDER ERROR; hunk-verification compensation; mutation checks reach DOC surfaces
- Target: `AGENTS.md` ((j) append to the 2026-08-29 flash-era
  addendum) · Class: auto
- Change: (j) — the blind-lens single retry can fail on a provider
  error (not just truncation) — same 6/7 DEGRADED-DISCLOSED close;
  "line-by-line hunk verification" is a named, disclosed compensation;
  mutation checks now reach doc surfaces (demo header 'pre-fix this
  mesh died' FALSE by mutation; tuning-table measured-effect citation
  disproven) — bytes-not-claims extends to docs.
- Evidence: pp-funfix-118-124-perkins-r1 2026-09-01T01:05:25Z (4x
  connection deaths, one continue) + 2026-09-01T01:29:27Z (blind
  degraded: length cap THEN provider error on retry; W4/W1 quotes).
- Reasoning: extends the recorded canary protocol with the failure
  mode it didn't name, and banks the compensation technique + the
  doc-surface mutation standard while they're fresh.

### P8 — Worktree-bootstrap class goes cross-repo: PP misses `_bmad` entirely
- Target: `AGENTS.md` (addendum to the RT `_bmad` bootstrap gotcha)
  · Class: auto
- Change: dated addendum — a PP `git worktree add` worktree misses
  `_bmad` ENTIRELY (fully gitignored): `ln -s <repo_root>/_bmad
  _bmad` before any bmad-build step; render_skill.py lives at the
  ORCHESTRATOR root's `/Users/moses/code/_bmad/scripts/`.
- Evidence: pp-funfix-118-124 2026-09-01 (shard) + the recorded RT
  class (08-13 ×2 rsync; 08-27 server/.env) + field-notes line ~551
  (the render_skill.py waiver saga).
- Reasoning: same class ("bootstrap misses untracked support dirs"),
  new mechanism (worktree add vs copy) — the gotcha now names both.

### P9 — PP demo-authoring + evidence craft (shard promotion)
- Target: `docs/minion-field-notes.md` (new dated entry) · Class: auto
- Change: one 2026-09-01 entry — (a) PRs always `--base v2`;
  (b) unblessed demos FAIL `harness run` — `harness save` in a
  sandbox copy (`rsync -a --exclude .git --exclude _bmad`, ~300 MB)
  blesses AND writes `--stats-out` even on failing runs = the only
  replay-verified evidence path; (c) replay_error latches with NO
  reason named (#123) — bisect ports-first (4/router; spine links
  count) → spans (integer-Euclidean; ACTIVE tiers 14/16/18) → never
  `sed`-renumber spawn ids (rewrite the whole demo); (d) the v3 stats
  CSV has NO lifecycle events — blessed HUD PNGs read inline
  (glm-5.3-flash native vision) are ground truth, stats math alone
  misleads.
- Evidence: pp-funfix-118-124 2026-09-01 (shard ×3 lines) +
  pp-playtest-fun 2026-09-01 r2 (shard ×3 lines) — two independent
  jobs in the same loop hitting the same harness family. Span numbers
  VERIFIED against `data/pipe_tiers.json` (14/16/18 active; the
  recorded 10 = the DISABLED narrow tier).
- Reasoning: the fun-test loop is the recurring PP surface; these are
  the exact traps its next minion hits (demo authoring, evidence
  verification, rejection bisect).

### P10 — Stale-guard the recorded `max_span 10`
- Target: `docs/minion-field-notes.md` (inline annotation) · Class: auto
- Change: "(max_span 10)" → "(max_span 10 — narrow since DISABLED;
  active tiers 14/16/18, see the 2026-09-01 entry)". No prune — the
  line is factually right for the disabled narrow tier.
- Evidence: `data/pipe_tiers.json` _comment (narrow REMOVED from the
  default catalog per the 2026-08-23 ruling; DISABLED SPEC
  max_span 10) + active tiers 14/16/18.
- Reasoning: a minion sizing a fixture off the old line sizes it
  wrong against the current catalog; the parenthetical redirects.

### P11 — A tool/bridge CALL timeout ≠ job failure — check the artifact
- Target: `docs/minion-field-notes.md` (new dated entry) · Class: auto
- Change: one 2026-09-01 line — long server-side jobs (Cycles
  renders, generations, batch runs) finish despite the call timing
  out; CHECK THE OUTPUT ARTIFACT before retrying or declaring
  failure (bridge-timeout renders landed server-side; pi lens turns
  that hit 500s still wrote findings to disk).
- Evidence: gru-journal 2026-09-01 lesson #11 (video lane) + the
  recorded pi lens-turn sibling (AGENTS.md vision/KYLE craft:
  "findings land on disk even when the final message errors").
- Reasoning: cross-substrate pattern (render bridges, agent turns);
  the cost of missing it is duplicate renders/jobs.

## Watch items (anecdotes — tracked, not proposed)

- **Downscale review images BEFORE reading them into context** —
  gru-journal 09-01 lesson #13: full 1920×1080 PNGs 413 the harness +
  bloat context to compaction (960×540 is plenty). One lane (video);
  generalizes to any agent reading its own captures. Recur-check next
  dream; a second lane earns the field-notes line.
- **Acquired assets are session-state until persisted** — save
  IMMEDIATELY after a download; never a destructive context switch
  between acquisition and save; know which save is ground truth (the
  user's GUI Ctrl+S when the bridge save is flaky). One lane.
- **Named slots/registries can silently hold the WRONG content** —
  A_sedan held a hand-built box, not the Chrysler; verify contents
  before building on a name. One lane.
- **Small windows still earn sheep** — 2nd dream corroboration
  (08-31: the ledger sheep's independent count caught missing rows;
  09-02: the ledger sheep caught the empty review anchor + the false
  "dispatch add was missing" claim the journals missed). The dream
  template mandates sheep-per-source but carries no minimum-window
  guidance — watch for a third; a template line then.

## Pruned / rejected candidates (with why)

- **Video-lane ruling clusters** (PLATA O PLOMO style ruling, CHARGE
  baseline + EEVEE sanctioned, FOCUS LOCK, ASSETS-FIRST, IMPACT
  AUDIT, asset licensing policy): lane canon — the gru-journal IS
  their durable home (Gru authored them there 09-01/02). Zero
  cross-lane orchestration mechanism; no store edit from the dream.
- **Bob-row "in-review corrected" (08-29 + 08-31)**: NOT a defect
  pattern — the dream template itself mandates `in-review "report at
  <path>"` at badge-out; the corrections are Silas close-out
  normalization. No change.
- **Content-dating tail-read skip; notification false-claim
  verify-toolResults; pane-id re-capture post-move; MEGA-DIFF on the
  funfix delta (93,959L); dream close-out cadence; lavish-exempt
  small-docs path; NULL-pr self-report hygiene**: all CONFIRMATIONS of
  recorded doctrine — no edit.
- **docs-p4-p5 field-note shard** (managed-repos "recorded vs
  committed" + the notification paste-shape): lives inside PR #16's
  branch, not the live field-notes dir — it enters a future dream
  window when the PR merges.

## Ops notes for close-out (not proposals)

- **PR #16 (orchestrator-docs-p4-p5, the P4/P5 user-ack from
  dream-2026-08-31) is still OPEN** — video-lane routing facts +
  self-notify checklist gate + its field-note shard all ride it.
  P4/P6 above deliberately avoid duplicating its content.
- **Skills-swap final step VERIFIED executed** — packet-plumber/.agents
  is an empty dir (symlink + stale-aug5 both removed at the 08-29 lane
  close); the SWAP-NOW REMOVE-LATER deferred trigger fired as written.
- **PP briefing template** could carry `--base v2` (Silas/Gru
  territory; P1 covers the doctrine).
