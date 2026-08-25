# Briefing — packet-plumber-v2-viscomm-crisis-duck (viscomm audit finding C)

Skill to execute: **bmad-quick-dev** (step-04 review layers MANDATORY before
reporting done). Briefing is self-contained if the skill is absent.

## USER DESIGN RULING (2026-08-25, the parked question — now answered)

Crisis-time hierarchy via **desaturation of the non-involved network** during
an active crisis. When everything screams, nothing reads as urgent — this
change makes the crisis zone the ONLY saturated thing on the board.

## Repo / workspace facts

- Repo: `/Users/moses/code/packet-plumber` (Odin `dev-2026-08` + raylib 6.0).
- Base branch: **v2** (head resolved by Silas at release — this job is
  SERIALIZED behind gauge-telegraph; same render surface, the viscomm
  row-note precedent). Work ONLY in the worktree; NEVER touch the main
  checkout (user branch).
- Read `/Users/moses/code/packet-plumber/project-context.md` first — ODN
  rules and [LOOK] canon govern.
- Field notes (read): `_bmad-output/field-notes/packet-plumber-v2-viscomm-tie-deconflect.md`
  (render-test + palcheck + mutation-leg craft), and
  `packet-plumber-v2-4.2-surge-crisis.md` (crisis engine truth).

## The design (canon-anchored)

The v2-network-pop ruling made the network the hero via saturation contrast:
vibrant pipes on a calm desaturated paper board. This change REUSES that
exact mechanism, dynamically: during crisis, invert the allocation —
non-involved network elements recede toward the board's calm register, so
the crisis elements own the saturation budget.

1. **Crisis state source (deterministic, already serialized):**
   `state.crisis.active` — array of `Active_Crisis` (core/crisis.odin:42+).
   Each carries the canonical `(bundle_lo, bundle_hi)` bottleneck NODE PAIR.
   No new game-state. RENDER-SIDE ONLY — never alter crisis semantics,
   triggers, or resolve hysteresis.
2. **Involvement predicate (seed definition — refine against the model):**
   involved = the crisis bundle pair's edge(s) + pipes/nodes on the affected
   path (the surge class's route). Everything else = non-involved. If the
   model already marks involvement more precisely, prefer its own predicate;
   name your final predicate in the PR.
3. **Desaturation math:** linear mix of the pipe/node color toward the
   board's desaturated register (a fixed calm target color or per-color gray
   mix) by a constant factor (e.g. mix 60-75% toward calm). Plain arithmetic
   lerp — NO transcendentals in draw paths (§10.4). If the transition is
   eased, use a PULSE16-style stepped table (view.odin:762 pattern),
   tick-driven + deterministic.
4. **Byte-identical when inert (the wire-aesthetics standard):** with ZERO
   active crises, every render is BYTE-IDENTICAL to pre-change. Prove it:
   flags-off/inert harness run, zero-diff vs pre-change capture. This is the
   contract that the desat touches crisis states ONLY.
5. **Crisis-frame goldens:** enumerate which goldens capture crisis states;
   regenerate ONLY those, deliberately (capture_frame construction). List
   them in the PR body. Non-crisis goldens: zero-diff, no regeneration.
6. **Reduced-motion (7.3 / E9.2):** transition easing is pinned — under
   reduced-motion the desat applies instantly (a static color mix, not an
   animation; the static desat itself is NOT gated — only its transition).
7. **CVD / a11y modes:** diff the CVD mode tables (the tie lesson: overrides
   can silently reintroduce collisions). Crisis separation must survive
   under CVD modes — verify with a palcheck pair: crisis-involved vs
   non-involved DURING crisis (must differ in the mode tables), and remember
   tools/derive_a11y_palettes.py needs a comment-stripped palette.json copy.

## Testing standard (non-negotiable)

- **Mutation leg on the DRAW PATH:** deleting the desat branch (crisis
  renders fully saturated) MUST fail a test — palcheck-style live render
  (ClearBackground + draw_world with a crisis state constructed via
  crisis_trigger or a fixture Active_Crisis + LoadImageFromScreen), sample
  non-involved pipe pixels mid-crisis: desaturated vs the saturated
  baseline. RED-then-GREEN runs in your report.
- **Inert zero-diff proof** (item 4) in your report.
- Deliberate-fail probe on any NEW test case before trusting green.
- Full suite green: `odin test app` (46), `odin test app/render` (83+),
  `odin test core` (crisis suite), palcheck.

## PR / ledger

- One PR to base **v2**. Title prefix `viscomm(crisis):`.
- `ledger set packet-plumber-v2-viscomm-crisis-duck in-review "<PR url>"`
  THEN `ledger pr packet-plumber-v2-viscomm-crisis-duck <PR url>` (both
  steps — the pr field arms the PR watcher).
- Perkins r1 arms via the sensor at your stable CI-green head.

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider — k3 403, flash 402),
  `--thinking max`.
- Any mega-minion: pin `zai-coding-cn/glm-5.3` explicitly in the spawn
  prompt (bare pi misroutes).

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: viscomm-crisis-duck
- base: v2 (head resolved at release)
- branch: packet-plumber-v2-viscomm-crisis-duck
- model: zai-coding-cn/glm-5.3
- pr_review: 1 (LOOK canon surface)
- blocked_by: packet-plumber-v2-viscomm-gauge-telegraph (release = its merge
  close-out; same render surface, the viscomm serialization precedent)
