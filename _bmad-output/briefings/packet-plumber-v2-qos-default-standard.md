# Briefing: QoS unconfigured default — 100% Standard lane

**Job id:** packet-plumber-v2-qos-default-standard
**Repo:** packet-plumber

## Task

User report (2026-08-19, verbatim): "in networking when no queue is configured,
all traffic should be on the standard queue and would take 100% of the capacity.
And that should be the auto. Everything on standard and 100% until we start
implementing QoS."

This is CANON, not a new decision — the implementation has drifted from it:

- GDD M2: "all traffic starts on Standard and the player actively engineers QoS
  — the player owns every call."
- Assignment-driven auto-reservation ladder: "1 class queue used = 100% ·
  2 = 70/30 · 3 = 50/30/20" (data-driven in `balance.json`). With ZERO player
  assignments there is exactly one class queue in play (Standard) → 100%.

Find where the unconfigured/default allocation diverges (suspect: a default
weight preset — e.g. the 50/30/20 — being applied to pipes with no player
assignment, or the ladder keyed off available lanes instead of *used* lanes)
and fix it so:

1. A pipe with NO player QoS configuration carries ALL traffic on the
   **Standard** lane at **100%** of capacity. Express and Best-effort carry
   nothing until the player assigns a type to them.
2. The auto-ladder engages ONLY from the player's first type→lane assignment
   (1 used = 100%, 2 used = 70/30, 3 used = 50/30/20 — from `balance.json`,
   no hardcoded splits).
3. Default state survives save/load, era advance, and pipe upgrade/tier
   changes (no silent re-split).

## Acceptance

- Headless test: fresh pipe, zero assignments → 100% Standard allocation;
  oversubscribed demand → Standard-lane packets use the full capacity (no
  reservation held for unused lanes).
- Test: first assignment flips that pipe to the ladder rung; removing all
  assignments returns to 100% Standard.
- Full local suite (`bin/local-ci` or equivalent) green; goldens re-blessed
  ONLY if the fix legitimately changes pinned behavior (fold-only re-bless
  discipline — say so in the PR body if so).
- PR body names the divergence root cause.

## Skills policy

- Workflow: **bmad-quick-dev** (implementation).
- Mega-minions (if spawned): bmad-review-adversarial-general /
  bmad-review-edge-case-hunter for self-review.

## Model policy

- Minion: pi default (ops tier — deepseek/deepseek-v4-flash).
- Mega-minions: same.

## Review

- `pr_review: true` — gameplay/canon-surface code (QoS allocation semantics);
  the 2026-08-12 scope guard applies. Perkins round on the PR head.
- No lavish needed — code fix, PR directly.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: v2-qos-default-standard
- base: v2
- pr_review: 1
