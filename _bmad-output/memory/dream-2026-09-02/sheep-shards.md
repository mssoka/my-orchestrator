# Sheep shard — sheep-shards (dream-2026-09-02)

Sources read (post-marker 2026-08-31T22:13:41Z only):
`field-notes/pp-playtest-fun.md`, `field-notes/pp-funfix-118-124.md`,
`field-notes/dream-2026-08-31.md`. Dedup greps run read-only against
`/Users/moses/code/AGENTS.md` and `/Users/moses/code/docs/minion-field-notes.md`.

## Candidates

- **PP demo evidence: unblessed demos FAIL `harness run`; `harness save` in a
  sandbox copy blesses AND still writes `--stats-out` even for failing runs —
  save-then-run is the only path that also replay-verifies your evidence.**
  Example: pp-playtest-fun, 2026-09-01 (r2) — "Unblessed strategy demos FAIL
  `harness run` (no-manifest T1) — but `harness save` in a sandbox copy
  blesses AND still writes the `--stats-out` stream even for failing runs;
  save-then-run is the only path that also replay-verifies your evidence.
  Sandbox copy = `rsync -a --exclude .git --exclude _bmad` (~300 MB, carries
  the gitignored rlsw shadow)."
  Proposed target: minion-facing craft (`docs/minion-field-notes.md`).
  Already-recorded check: PARTIAL overlap, new facet — field-notes line ~499
  records "`harness input-parity save` is a SEPARATE verb from `harness save
  <demo>`" (re-bless verb enumeration), and line ~650 records "rsync the repo
  to /tmp (exclude _bmad)" as a READ-ONLY crash-repro recipe (box-crash
  08-24/25). Neither records the save-then-run evidence path nor that `save`
  emits `--stats-out` on failing runs. NEW.

- **PP topology authoring: the 4-port router cap IS the topology floor — count
  endpoints BEFORE authoring minimal meshes; span = integer-Euclidean-rounded
  (isqrt + half-up), max 14 standard / 16 mid / 18 wide.** (Two independent
  sources, same window.)
  Examples: pp-playtest-fun, 2026-09-01 (r2) — "a 3-router spine for 13 nodes
  needs 14 ports and every short draw fails validation as a replay_error
  latch (ODN-11) with no message naming the cause; count endpoints before
  authoring minimal meshes. Span metric is integer-Euclidean-rounded (isqrt +
  half-up), max 14 standard / 18 wide." AND pp-funfix-118-124, 2026-09-01 —
  "bisect rejections by (a) counting router ports FIRST (4/router; spine
  links count), (b) computing spans (`span_between` = integer Euclidean;
  standard 14 / mid 16 / wide 18)".
  Proposed target: minion-facing craft.
  Already-recorded check: the silent-reject CLASS is recorded — field-notes
  ~line 822 "adding pipes to a full router silently rejects
  (Router_Ports_Full → replay_error latched — swap or size the fixture)" and
  "a narrow pipe draw is silently REJECTED (max_span 10)". NOTE the recorded
  `max_span 10` predates/disagrees with the new 14/16/18 numbers — flag as a
  numeric-contract refresh, plus the author-time pre-count procedure is NEW.

- **PP demo-authoring trap: `sed`-renumbering spawn ids leaves dangling draw
  endpoints — rewrite the whole demo instead.** replay_error latches with NO
  reason named; ordered bisect = ports → spans → id renumber.
  Example: pp-funfix-118-124, 2026-09-01 — "replay_error latches with NO
  reason named (#123) — … (c) `sed`-renumbering spawn ids leaves dangling
  draw endpoints — rewrite the whole demo instead."
  Proposed target: minion-facing craft (merges naturally with the previous
  bullet as one "PP demo validation traps" entry).
  Already-recorded check: silent-reject/vacuity class recorded (field-notes
  ~line 830: "a draw to a NONEXISTENT node id is silently REJECTED
  (`replay_error` latched, no test checks it → guard with `!replay_error`") —
  the sed-renumber dangling-endpoint flavor and the fix-by-rewrite guidance
  are NEW facets.

- **PP observability: the v3 stats CSV has NO lifecycle events (breach
  latches, grace chips, Run_Won invisible) — ground truth = blessed HUD
  capture PNGs read directly via glm-5.3-flash native vision; stats math
  alone misleads.**
  Example: pp-playtest-fun, 2026-09-01 (r2) — "a win with 1801/1801
  SLA-flagged window ticks looks like a breach that should have drained."
  Proposed target: minion-facing craft.
  Already-recorded check: zero "stats"-CSV hits in the store. NEW. Also
  independently corroborates the AGENTS.md vision gotcha's glm-5.3-flash
  native-multimodal ruling (HUD PNGs read inline, no KYLE detour).

- **PP worktree bootstrap: `_bmad` is fully git-ignored →
  `ln -s <repo_root>/_bmad _bmad` from the worktree before any bmad-build
  step; render_skill.py lives at the ORCHESTRATOR's
  `/Users/moses/code/_bmad/scripts/` (the PP main repo's `_bmad/scripts/`
  does NOT carry it).**
  Example: pp-funfix-118-124, 2026-09-01 — "PP worktree bootstrap missed
  `_bmad` (fully git-ignored) — `ln -s <repo_root>/_bmad _bmad` from the
  worktree before any bmad-build step."
  Proposed target: minion-facing craft (PP crew convention); briefing
  templates could also carry it (orchestrator-ops secondary).
  Already-recorded check: ADJACENT but new — field-notes line ~551 records
  "SECOND root cause in the PP repo — `_bmad/scripts/` has NO render_skill.py
  (only memlog.py/resolve_*.py)" (the bmad-build waiver saga), and AGENTS.md
  records the RT `rsync --exclude='_bmad'` main-checkout copy gotcha. The
  PP-worktree symlink bootstrap step + the orchestrator-root location of
  render_skill.py are NEW.

- **PP PR convention: ALWAYS `gh pr create --base v2` — never assume the
  remote HEAD default.** (Silas ops ruling after #125 was opened vs main and
  retargeted.)
  Example: pp-funfix-118-124, 2026-09-01 — "PP PRs ALWAYS `gh pr create
  --base v2` (Silas ops ruling after #125 was opened vs main and retargeted)
  — the dispatch briefing names no base; don't assume the remote HEAD
  default."
  Proposed target: minion-facing craft (crew convention); also an
  orchestrator-ops candidate — dispatch briefings SHOULD name the base so the
  ruling stops being tribal knowledge.
  Already-recorded check: zero hits for "base v2" / "--base" in either store
  file. NEW.

- **Dream craft: small windows still earn sheep — 2 sheep cross-verified the
  fun-test squad window in ~5 min; the ledger sheep's independent DB count
  (27 events / 7 jobs) caught that #118/#124 fix rows don't exist yet
  (context, not a gap — issues-first intake, rows mint at dispatch).**
  Example: dream-2026-08-31 (Bob) — "Small windows still earn sheep."
  Proposed target: watch item (single sighting; Bob/dream-procedure lesson —
  belongs to the playbook 'Dreaming' section or template if it recurs). The
  "independent DB count cross-verifies journal claims" technique rides it.
  Already-recorded check: the dream template mandates "Sheep, one per source"
  but carries no minimum-window guidance. NEW as a watch item.

- **Dream craft: content-dating (U1) earned its keep — silas-08-28.md's
  post-marker mtime (22:29) held ZERO post-marker content (backfilled entry
  pre-dated the marker); tail-read confirmed and skipped without re-mining.**
  Example: dream-2026-08-31 (Bob).
  Proposed target: none — corroboration only.
  Already-recorded check: ALREADY RECORDED —
  `_bmad-output/briefings/_template-dream.md` line 39 carries "Content-dating
  (user-approved 2026-08-29, U1 APPROVED)". This is a confirmation sighting,
  not a new pattern.

- **Notification-gap false-claim flavor: verify `cli:notification:show`
  toolResults, never the minion's report (fun CLAIMED shown:true without
  executing — the new worst case).**
  Example: dream-2026-08-31 (Bob) — "the false-claim flavor (fun CLAIMED
  shown:true without executing) is the new worst case; verify toolResults,
  never the minion's report."
  Proposed target: none — corroboration only.
  Already-recorded check: ALREADY RECORDED verbatim in AGENTS.md, the
  2026-08-31 addendum to the no-PR-watcher gotcha — "fun's completion report
  CLAIMED `shown:true` without ever executing (0 `cli:notification:show`
  results in its session jsonl — a false claim, worse than a skip). Silas
  fired all three himself (shown:true verified)… Silas verify-and-fire on
  EVERY no-PR completion is the only reliable guard."

## Summary

| # | Pattern | Sources | Proposed target | Store status |
|---|---------|---------|-----------------|--------------|
| 1 | save-then-run replay-verifies demo evidence (`--stats-out` on fails) | pp-playtest-fun 09-01 | minion-field-notes | NEW (adjacent to save-verbs + rsync recipes) |
| 2 | count router ports/spans BEFORE authoring meshes (4/router, 14/16/18) | fun 09-01 + funfix 09-01 | minion-field-notes | NEW facet; recorded max_span 10 number looks stale |
| 3 | sed-renumber spawn ids → dangling endpoints; rewrite the demo | pp-funfix-118-124 09-01 | minion-field-notes (merge w/ #2) | NEW facet on recorded silent-reject class |
| 4 | v3 stats CSV blind to lifecycle events; HUD PNGs = ground truth | pp-playtest-fun 09-01 | minion-field-notes | NEW |
| 5 | PP worktree `ln -s <repo>/_bmad _bmad` bootstrap; render_skill.py at orchestrator root | pp-funfix-118-124 09-01 | minion-field-notes (+briefing template) | NEW (adjacent to waiver saga + RT rsync gotcha) |
| 6 | PP PRs always `--base v2` | pp-funfix-118-124 09-01 | minion-field-notes (+briefing template) | NEW |
| 7 | small windows still earn sheep; independent DB count cross-verifies | dream-2026-08-31 | watch item (dream procedure) | NEW as watch item |
| 8 | content-dating tail-read skip | dream-2026-08-31 | — | ALREADY RECORDED (template line 39) |
| 9 | notification false-claim: verify toolResults | dream-2026-08-31 | — | ALREADY RECORDED (AGENTS.md 08-31 addendum) |
