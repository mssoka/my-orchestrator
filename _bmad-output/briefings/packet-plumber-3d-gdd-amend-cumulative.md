# Briefing: packet-plumber-3d-gdd-amend-cumulative

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Targeted GDD v2 clarity amendment** — two user rulings (2026-09-05) that
sharpen the campaign canon. SMALL doc edit: **lavish not needed, open the
PR directly** (canon touch-up exemption — this briefing says so explicitly).

## Ruling 1 — cumulative traffic (make it explicit doctrine)

User's words: "every era adds a new traffic type/tech. but i'm not sure if
it's clear that it is cumulative. so we still get traffic from the previous
eras in addition to the new traffic/packets/tech we are introducing. there
is no internet that just does streaming. and forgets email. we still send
email and ftp even on the current internet."

Amend:
- In the M2 level-gating paragraph (and the era table's framing): add the
  **cumulative-traffic doctrine** — every era's levels carry the FULL
  accumulated traffic/tech mix plus the new introduction; nothing retires
  (email and FTP ride alongside streaming forever); complexity compounds
  by era — deeper QoS trade-offs, heavier loads, richer crisis mixes.
- Reflect it in the era ladder table (one clarifying line above/below the
  table: the "new" column is ADDITIVE, not replacement).

## Ruling 2 — restore the in-level constellation view (supersedes D5's retirement clause)

User's words: "we need it in-level as well for more advanced levels that
layers traffic type and gets more complex."

Amend:
- **D5's between-levels campaign map re-scope STANDS** (constellation as
  the rocketship map — unchanged).
- **The in-level whole-topology mode UN-RETIRES**: a player-triggerable
  in-level view (the constellation/flattening treatment applied to the
  CURRENT planet) returning for **advanced-era levels** — motivated by
  cumulative-traffic complexity (layered types + compounding load), not
  node count (the ≤16-node far-side argument that retired it). Early-era
  levels don't need it; later eras layer enough traffic that reading the
  spinning globe alone stops being kind.
- Update: the M3 constellation paragraph's retirement sentence, Open
  Question 9's resolution (append the supersede), `epics.md` E10.7 (split:
  campaign map stays E10.7; in-level topology view returns as its own
  story scoped to advanced-era levels — suggest E8/E10 placement per the
  epics' own structure), traceability matrix cell, and a decision-log
  entry carrying both rulings verbatim + the supersede chain
  (D5 2026-09-04 → D5a 2026-09-05).

## Acceptance

1. Both doctrines stated explicitly (quote-worthy lines a fresh minion
   could implement from).
2. Supersede trail intact: decision-log entry, dated, both rulings verbatim.
3. No other canon touched. PR body: "Decisions & rationale" = the two
   rulings. Suite untouched (docs-only — verify the docs-pinning tests
   still pass if any reference the amended sections).

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**.

## Skills policy

Workflow: **`gds-gdd`** (update flow). NO lavish (stated above).

## Perkins

`pr_review=0` — docs deliverable, direct PR.

## Dispatch parameters

```
job_id:    packet-plumber-3d-gdd-amend-cumulative
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      gdd-amend-cumulative
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 0
notes:     Worktree from origin/main. _bmad symlink bootstrap. PARALLEL
           LANE: scene-refactor (code) — disjoint files (docs vs code).
```
