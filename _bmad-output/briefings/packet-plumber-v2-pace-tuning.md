# packet-plumber-v2-pace-tuning

## Task

Two feel fixes from the user's live play session (2026-08-21 ~23:5xZ),
both already ruled in direction — implement, don't re-litigate:

1. **Packet pace → Mini Motorways car pace.** Packets currently move
   so fast they're hard to follow. Target: MM-car-calibrated motion —
   calm, deliberate, followable at a glance; a packet crossing a
   typical route segment takes SECONDS, not a fraction of a second.
   Ballpark calibration: overall transit speeds reduced ~2.5–4× from
   current; if a packet crosses the board in under ~1.5s it is still
   too fast. No gameplay-semantics change — same routing, same
   delivery rules, only the time axis stretches.
2. **Terminal spawn cadence ↓.** Terminals pop up too frequently.
   Reduce spawn rate roughly 2× and add spacing so clusters don't
   burst; keep whatever difficulty ramp exists but shifted down.

## Rules (hard)

1. Expose pace as NAMED tunables (single pace-scale knob + terminal
   spawn interval), not scattered magic numbers — the user will
   fun-test and we will iterate on the knobs.
2. Calibrate honestly: measure current packet transit time (a quick
   headless sim run or test harness log), apply the scale, measure
   again; PR body shows before/after numbers.
3. Do NOT touch routing semantics, serialization, packet contracts,
   or LOG_VERSION — time axis + spawn interval only.
4. Visual/aesthetic surface (how routers/terminals LOOK) is OUT of
   scope — a separate design-audit job owns that; don't drift there.
5. Fun-test gate: merge ≠ done. The user plays `odin run app` after
   merge; expect a follow-up tuning round on the knobs.

## Acceptance

- Both knobs exist, named, with the MM-calibrated defaults applied.
- Before/after transit-time + spawn-interval numbers in the PR body.
- Local test suite green.
- pr_review: 1 (gameplay-surface; Perkins round before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max. Mega-minions (if any): same.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-pace-tuning
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with packet-plumber-v2-design-audit (that job audits
  v2@head from its own worktree; your branch stays unmerged until its
  Perkins verdict)
