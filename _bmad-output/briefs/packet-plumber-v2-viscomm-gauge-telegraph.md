# Briefing — packet-plumber-v2-viscomm-gauge-telegraph (viscomm audit finding B)

Skill to execute: **bmad-quick-dev** (step-04 review layers MANDATORY before
reporting done). Briefing is self-contained if the skill is absent.

## Repo / workspace facts

- Repo: `/Users/moses/code/packet-plumber` (Odin `dev-2026-08` + raylib 6.0).
- Base branch: **v2** @ fresh head `0b893ee` (post-#99-merge). Silas creates
  the worktree; work ONLY there; NEVER touch the main checkout (it sits on a
  user branch).
- Read `/Users/moses/code/packet-plumber/project-context.md` first — ODN
  rules and [LOOK] canon govern.
- Field notes (read both): `_bmad-output/field-notes/packet-plumber-v2-viscomm-tie-deconflect.md`
  — they carry the render-test + palcheck + mutation-leg craft you MUST reuse.

## Task: gauges must telegraph, not snap (audit finding B)

Health / pool / SLA gauges currently snap value-to-value. When values move
fast (drain, refill, SLA decay) the player reads a strobe, not a level.
Animate the transitions so the gauge TELEGRAPHS its motion:

1. **Eased display-value, raw truth.** Keep the underlying metric values
   untouched (never alter SLA/health/pool SEMANTICS — render-side only).
   Each gauge carries a display value that eases toward the raw value.
2. **PULSE16-style stepped table, NO transcendentals** (§10.4 canon — see
   `PULSE16 :: [16]f32` at `app/render/view.odin:762` for the pattern, and
   view.odin:1601 for the render-side-table idiom). Define an EASE16-style
   envelope table; index by tick-derived integer phase. No sin/cos/pow/exp
   in draw paths — compile-time enforceable via the `when <bad> { BROKEN ::
   1 / 0 }` idiom if practical.
3. **Deterministic + tick-driven** — animation phase advances from game
   tick, never wall-clock; identical ticks render identical frames
   (golden-safe by construction; zero golden churn expected — if a golden
   legitimately must move, STOP and flag: that is a canon decision).
4. **Reduced-motion** — the 7.3 (E9.2) reduced-motion setting pins PULSE16
   effects (view.odin:94); the gauge easing MUST respect the same setting
   (snap immediately under reduced-motion).
5. **Chunk-flash guard for big jumps** — on a large instantaneous delta
   (e.g. pool drained by event), a single-frame flash/chunk cue is allowed
   ONCE, then ease — the cue is table-driven and deterministic like the rest.

## Testing standard (the r1/r2 lesson — non-negotiable)

- **Mutation leg on the DRAW PATH:** deleting/bypassing the easing (display
  value := raw value) MUST fail a test. A predicate-only pin is bypassable
  (the r1 vacuous-gate burn). Guard what renders: palcheck-style live-render
  checks (ClearBackground + draw the gauge + LoadImageFromScreen, sample the
  fill geometry/pixels mid-ease) or equivalent draw-path assertions — per
  the field notes, palcheck can do live renders without touching goldens.
- Prove RED-then-GREEN: run with the easing deleted (tests RED), restored
  (GREEN). Both runs in your report.
- Deliberate-fail probe on any NEW test binary/case before trusting green
  (field note: cheap confirmation the test actually executes).
- Full suite green: `odin test app` (46), `odin test app/render` (83+ incl.
  your new tests), palcheck.

## PR / ledger

- One PR to base **v2**. Title prefix `viscomm(gauge):`.
- `ledger set packet-plumber-v2-viscomm-gauge-telegraph in-review "<PR url>"`
  THEN `ledger pr packet-plumber-v2-viscomm-gauge-telegraph <PR url>` (the
  pr field arms the PR watcher — both steps, always).
- Perkins r1 arms via the sensor at your stable CI-green head.

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider — k3 403, flash 402),
  `--thinking max`.
- Any mega-minion: pin `zai-coding-cn/glm-5.3` explicitly in the spawn
  prompt (bare pi misroutes).

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: viscomm-gauge-telegraph
- base: v2 (head 0b893ee)
- branch: packet-plumber-v2-viscomm-gauge-telegraph
- model: zai-coding-cn/glm-5.3
- pr_review: 1 (render-path change on a canon surface — viscomm series keeps review)
