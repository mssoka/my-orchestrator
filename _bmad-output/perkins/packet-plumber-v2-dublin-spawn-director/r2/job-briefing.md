# packet-plumber-v2-dublin-spawn-director

## Task

Stage 2, job 1 of the Dublin arc (user directive 2026-08-24: "game
play and node spawn must match the decisions made for the map
beautify"). The 7-round lavish mock gate's rulings are CANON — this
job makes node spawning implement them on the real board.

## Source of truth (read FIRST — the approved mock)

- The mock-gate artifact + round history:
  `.lavish/dublin-mock-gate.html` and the round notes in the
  dublin-map-beautify worktree/PR #95 body — the APPROVED state
  (Round 7) carries the rulings: the density level the user blessed
  (1-in-6 or 1-in-9 — READ THE APPROVED MOCK, do not assume), the
  zoom-band topology model (zoomed-out backbone / zoomed-in dense
  play), cluster/district shapes, building conformity
  (street-aligned blocks).
- PR #95's implementation of the board (base head).

## Scope

1. **District spawn-director**: growth SEED/ATTACH weighted by
   district (real neighborhoods as estate anchors — the cluster
   shapes from the approved mock); district caps from the mock's
   density ruling; spawns draw from street-adjacent candidates
   conforming to the mock's building-block model.
2. **Zoom-band interplay** (spawn side only): the mock's backbone vs
   dense-play topology — spawns respect the band model (backbone
   districts seed sparser, dense-core districts richer), matching the
   approved zoom behavior.
3. **Determinism**: map id + spawn-director state are pinned inputs
   (replays hash); old runs pin old behavior; document LOG_VERSION
   impact if any.
4. Streets-constrain-pipes and last-mile draw are OUT OF SCOPE
   (stage-2 jobs 2/3).

## Rules (hard)

1. Sim-surface change: full determinism suite; golden re-bless
   cause-documented; dual-run (old maps pin).
2. The mock's approved state is the acceptance reference — KYLE
   compares live spawn behavior against the approved mock visuals.
3. Named tunables (district weights, caps, density) — the user
   fun-tests and iterates.
4. pr_review: 1.

## HOLD / release

- HELD, PANELESS behind PR #95's merge close-out (stage 2 builds on
  the beautified board). Release = fresh v2 head, then dispatch.

## Skills policy

bmad-quick-dev; KYLE for the mock-match gate.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v (remote; local
fallback).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-dublin-spawn-director
- base: v2 (fresh head at release — post-#95)
- model: deepseek-v4-flash
- worktree: yes (at release)
- pr_review: 1
- blocked_by: packet-plumber-v2-dublin-map-beautify (#95 merge
  close-out)
