# packet-plumber-v2-motion-readability

## Task

Packets currently render at 20 Hz quantized positions — NO sub-tick
interpolation (code-verified in app/render/view.odin draw_packets /
core/flow.odin packet_progress_frac: packets only move when the sim
ticks, so on a 60 Hz display they jump in 50 ms steps). The user's
original complaint "packets move too fast to follow" + the visual-read
side: the jumpiness is a view-layer artifact, fixable without touching
sim speed (the pace job owns speed).

1. **Sub-tick interpolation (the core fix)**: view-layer lerp between
   the last two snapshot positions using the render-frame's fractional
   progress — packets glide smoothly between ticks. This is the
   look-book's own promise (motion canon).
2. Optional (verify against captures): short motion trails — 2–4-frame
   fading echo per packet, MM-style "consistent speed" read (MM
   image_01/03/05/07); trail = the packet color at low alpha.
3. Size + glint tuning: packets are r≈8 px at fit; +15% (~9.2 px) with
   the existing glint; verify readability on the dense-core and
   corridor crops.

## Rules (hard)

1. View-layer only (ODN-1: view never writes back to sim state). The
   interpolation reads snapshots; the sim's 20 Hz truth is untouched.
   LOG_VERSION untouched.
2. T2-safe: capture at the pinned sha before/after to prove the motion
   read changed without altering sim behavior (goldens re-bless only if
   a capture tick legitimately moves; document cause).
3. Don't change packet SPEED — that's the parallel pace-tuning job's
   knob. This job is about how motion READS (smoothness, trail, size).
4. Measure: frame-to-frame packet displacement at 60 Hz before (steps)
   vs after (continuous) — PR body shows the delta.

## Acceptance

- Sub-tick interpolation live; packets glide between ticks (motion
  strip captures at 100 ms show continuous progression, no 50 ms jumps).
- Trails/size tuned if they help; no regression on dense-core
  readability.
- Local test suite green; goldens documented.
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-motion-readability
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave (view-layer; merge order =
  wave's final re-bless)
- source of truth: kyle-design-directions.md §4 + design-audit.html Q3
