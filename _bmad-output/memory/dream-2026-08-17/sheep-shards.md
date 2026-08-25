# sheep-shards — candidate patterns from 13 field-note shards (dream-2026-08-17)

Sheep: sheep-shards. Window: shards newer than 2026-08-15T17:01:46Z. Per the
dream brief: patterns already codified in AGENTS.md / minion-field-notes are
flagged as RECURRENCE-ONLY (note the count, don't re-propose the text).

---

## 1. WORKTREE TRAP — editing the MAIN checkout instead of the dispatched worktree (STRONG, 2 shards, self-reported 3rd+ sighting)

- packet-plumber-v2-5.4-input-parity, 2026-08-16: "WORKTREE TRAP (again, 3rd+
  sighting): I edited the MAIN checkout (`/Users/moses/code/packet-plumber`)
  via absolute paths while dispatched to the worktree."
- packet-plumber-v2-7.2-audio-juice, 2026-08-17: "Worktree-trap, THE expensive
  one: I did the whole job with file-tool paths + bash `cd`s at the MAIN
  checkout … the briefing's `repo_root` param reads like a work path."
- Both propose the same fix, worth codifying verbatim as the rule:
  `pwd` + `git branch --show-current` FIRST, then pin the worktree path ONCE
  and use it for EVERY file-tool path AND every bash `cd`. New nuance from
  7.2: briefing params named `repo_root` actively mislead — treat them as
  "repo identity", never as a working path. Recovery recipe (cp changed files
  byte-identical into worktree, `cmp`-verify, rebuild + CI there, restore
  main) is consistent across both.

## 2. Multi-edit `edit` batches reject ATOMICALLY and SILENTLY on one bad oldText (STRONG, 2 shards)

- packet-plumber-surge-explainer, 2026-08-15: "a duplicate oldText
  (accidentally included twice) fails the WHOLE batch silently — dedupe
  targets."
- packet-plumber-v2-5.9-demand-caps: "The multi-edit atomic trap hit again
  (crisis_test batch): ONE ambiguous oldText rejected all 5 edits — … I
  debugged phantom behavior for a round before noticing."
- Candidate rule: before batching edits, verify each oldText's file AND
  uniqueness; after any multi-edit, re-grep to confirm every hunk landed —
  a silent whole-batch rejection leaves the tree looking "edited" while
  nothing applied.

## 3. Vacuous-green / silent no-op APIs — a pin that can't fail isn't a pin (STRONG, 4+ shards, two flavors)

Flavor A — mutation-prove every pin:
- v2-5.5-demolish-input: "my first negative-control mutation (`if false`) was
  vacuous — a pin that can't fail isn't a pin; the second (`if true`) proved
  both button scenarios bite. Always verify a mutation actually flips the
  scenario red."
- v2-5.4-input-parity, 2026-08-17: "re-shaped pins must be mutation-proven:
  … deleting `&& !esc_cancelled` passed 20/20."
- v2-5.2-node-health: replay identity "can't prove absence from the save
  format" — needs a byte-dump negative control too.

Flavor B — silent no-op APIs make tests pass vacuously:
- v2-5.9-demand-caps: "A draw to a NONEXISTENT node id is silently rejected
  (replay_error latched, no test checks it) — … the W5 transit pin passed
  VACUOUSLY." Fix: `!replay_error` guards + verify ids from spawn returns.
- v2-visibility: "`make([dynamic]T, 0, N)` has LENGTH 0 — a
  `p.class < len(counts)` guard silently writes nothing."
- local-ci-suite, 2026-08-16: "pinned odin … EXITS 0 on a failed windows
  cross-link … a gate must check the produced artifact, never just the rc."
- Meta-pattern worth one codified entry: any assertion whose precondition can
  silently not-happen (rejected command, empty collection, exit-0-without-
  artifact) needs an explicit guard on the precondition, and every pin needs
  a mutation that proves it can go red.

## 4. Gate-harness integrity — false greens from the harness itself (STRONG, 3 shards)

- v2-5.4-input-parity, 2026-08-17: "gate loops must derive their count from
  the list length (${#GATES[@]}), never a literal: the 9th local-CI gate …
  was unreachable for a full review round while run_gates capped at 8."
- v2-5.5-demolish-input: "the r3-N7 gate leg (bad-arg -> exit 2, `[ -x ]`
  guard against the 127->`!`->0 false-green)."
- local-ci-suite: exit-code-vs-artifact trap (quoted above) + "Dockerfile RUN
  steps default to /bin/sh (dash) — `set -o pipefail` fails hard" and bash
  3.2 empty-array `"${arr[@]+"${arr[@]}"}"`.
- Candidate rule: every gate harness audit checks (a) gate enumeration is
  derived, not literal; (b) missing-binary/missing-arg paths exit nonzero
  under `!`/negation; (c) success is asserted on the artifact, not the rc.

## 5. Shipped code/data is ground truth; docs, comments, and plan refs drift (STRONG, 3 shards)

- packet-plumber-traffic-model-design: "The GDD M1 tier table … is STALE vs
  the shipped catalogs (5/15/40) — design specs must cite the shipped
  data/*.json as ground truth and flag the drift."
- packet-plumber-surge-explainer: "`bandwidth_demand` is loaded into the
  catalog … but NOT consumed by the flow service pass — verify per-class
  transit claims against serve_bundle_lane, not the catalog comment."
- righttenantry-analytics-568-617: "'Plan §5' … has NO plan doc on disk —
  cite the code call sites (meta/dispatch.gleam:18-22) instead."
- Candidate rule: when a spec/GDD/comment/plan-section makes a behavioral or
  numeric claim, cite and verify against the shipped call site or data file;
  if they diverge, flag the drift in the deliverable, never silently follow
  the doc.

## 6. Billing-block CI diagnosis — verify the mechanism before escalating (RECURRENCE + new refinement)

- packet-plumber-full-game-doctrine, 2026-08-17: "GH Actions account-billing
  failure masquerades as a CI failure: jobs 'fail' in ~4s with NO logs … the
  truth is in `gh run view`'s ANNOTATIONS." Already codified in AGENTS.md
  (2026-08-14/16 rulings) — RECURRENCE-ONLY for that part.
- NEW refinement, not yet codified: "It kills GH-ACTIONS RUNNERS ONLY:
  Perkins runs locally via pi panes and is UNAFFECTED — I misdiagnosed a slow
  r1 as billing-blocked from a timing coincidence; a missing Perkins review
  is NOT billing evidence, verify the mechanism or ask Silas before
  escalating." Worth a one-line addendum to the billing gotcha.

## 7. `ledger set` same-status no-op DROPS the note — doc-placement complaint (RECURRENCE + placement fix)

- packet-plumber-full-game-doctrine, 2026-08-17: "`ledger set <job>
  <same-status> \"note\"` is a silent no-op that DROPS the note … the
  playbook's warning is buried in the review-sensor section, not the
  self-report bullet."
- The rule is codified in AGENTS.md; the actionable delta is PLACEMENT:
  minions hit it at self-report time, so the warning belongs in the
  self-report/standing-orders section too, not only the sensor section.

## 8. `herdr pane split` has no `--json` flag — raw stdout IS the JSON (RECURRENCE, extends codified gotcha)

- dream-2026-08-15: "`herdr pane split` has NO `--json` flag — the RAW stdout
  IS the JSON (`result.pane.pane_id`); with `--json` it prints nothing and
  the capture chain dies (mirror of the pane-move `--json` gotcha)."
- AGENTS.md codifies move/tab-create; extend the same line to `pane split`.
  Also confirms `split` output key is `result.pane` (matches the 08-13
  "split result = result.pane" addendum).

## 9. `git checkout <file>` restores from INDEX — mutation-restore trap (single shard, high value)

- v2-5.4-input-parity, 2026-08-17: "MUTATION-RESTORE TRAP: `git checkout
  <file>` restores from the INDEX (last commit), silently wiping uncommitted
  fixes — I killed my r3 mouse.odin fix that way … `cp file /tmp/backup`
  BEFORE mutating for a mutation test; never `git checkout` a file with
  uncommitted work."
- Pairs with pattern 3 (mutation testing is now standard); the restore half
  needs the same codification.

## 10. PR-event CI checks out the MERGE, not the branch — bless on fresh base (single shard, PP T2-specific but general mechanism)

- v2-5.2-node-health: "The PR-event GitHub Action checks out the MERGE of the
  branch into origin/v2 — NOT the branch alone. A T2 blessing on a stale base
  … passes locally + on the push-event run, then fails ONLY on the PR-event
  run." Fix: `git fetch origin <base>` + merge before blessing; "a
  presentation fold like a font swap re-blesses EVERY text-bearing demo's
  T2s."
- General lesson: push-event green ≠ PR-event green; before blessing
  golden/snapshot artifacts, verify `git merge-base` vs origin/<base> is
  current.

## 11. Review swarms earn their cost (RECURRENCE, 2 shards — positive signal)

- v2-5.4-input-parity, 2026-08-16: "review-swarm paid off (blind hunter
  caught 2 real same-frame divergences from the old handle_input)."
- v2-visibility: "Review swarms earn their cost: both hunters independently
  caught the severed undercount; the edge hunter caught the bundle-slot
  misanchor."
- Not a new rule — but two independent positive datapoints for the
  code-review swarm pattern this window.

## 12. Smaller single-shard items (note-only, repo/tool-specific)

- Odin language traps (v2-5.4: slice literals backed on CALLER's stack —
  heap-build test data outliving `free_all`; v2-7.2: relative imports resolve
  from PACKAGE ROOT; constant arrays unindexable by variable; truncating
  constant f32→int cast is a compile error; local-ci-suite: `odin test`
  needs clang for the test-runner link). Candidate for a PP-repo Odin-gotchas
  section rather than global field notes.
- Untracked/off-branch verification fixtures: traffic-model-design ("Source
  material can live as UNTRACKED files in the MAIN checkout … absent from the
  worktree") + refcheck-621 ("The reference_checks bug-hunt scenario suite
  lives on `origin/rt-refcheck-bughunt2`, NOT develop — copy it in …
  untracked, don't commit"). Weak recurrence: check main checkout / sibling
  branches for untracked briefing sources and suites before concluding
  they're missing.
- agent-browser evals share one global scope (refcheck-621): "wrap every
  eval in an IIFE `(() => { ... })()`, and `return` at the top level is a
  SyntaxError."
- Fixture DB seed generations (refcheck-621): "The fixture DB has TWO seed
  generations (a dead one … sorts FIRST in the leaderboard … silently breaks
  every scenario; delete it before running." Sandbox fixture state is part of
  the repro environment.
- Docker layer-order bake (local-ci-suite): COPY tools/ → RUN
  build_raylib_sw.sh → COPY . + .dockerignore exclusion = 33s warm vs 1m06s
  cold. PP-infra-specific.
- Rebase-relay surgical-hunk placement works (full-game-doctrine, 2026-08-17):
  "placed stories-v2.md hunks clear of sibling 5.5/7.2 status lines → rebased
  onto v2@#59 with ZERO conflicts … verified the sibling card byte-identical
  before `--force-with-lease`." Positive confirmation of the relay pattern.
- Bob-process notes (dream-2026-08-15 shard): grep session jsonl for
  `cli:notification:show` RESULTS to classify sensor-vs-compliance; sheep
  briefs naming the marker + "already codified → recurrence only" gave
  3 sheep / 0 re-proposals. Both are dream-process improvements, Bob-side.

---

## Cross-shard recurrence summary (strong signals)

| Pattern | Shards | Sightings |
|---|---|---|
| Worktree trap (main-checkout edits) | 5.4, 7.2 | 2 (+ self-reported 3rd+) |
| Multi-edit atomic silent rejection | surge-explainer, 5.9 | 2 |
| Vacuous-green pins / silent no-op APIs | 5.2, 5.4, 5.5, 5.9, visibility, local-ci-suite | 6 |
| Gate-harness false greens | 5.4, 5.5, local-ci-suite | 3 |
| Shipped code/data > docs/comments/plans | traffic-model, surge-explainer, analytics | 3 |
| Review swarms pay off (positive) | 5.4, visibility | 2 |
| Off-branch/untracked source material | traffic-model, refcheck-621 | 2 |
