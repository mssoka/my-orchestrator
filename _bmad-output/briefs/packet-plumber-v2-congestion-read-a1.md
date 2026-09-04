# Briefing: packet-plumber-v2-congestion-read-a1

Implementation job — USER-RULED restore (option A1 of the viscomm
regression audit). READ THE AUDIT FIRST:
`_bmad-output/implementation-artifacts/packet-plumber-v2-viscomm-regression-audit/viscomm-regression-audit.md`
— especially the R1 row, the "Rulings received" section, the A1
appendix, and the evidence register. It is your spec.

## Context

- Audit verdict (HIGH confidence): no viscomm effect silently severed by
  #105 — but R1, the LINK CONGESTION READ, is DEGRADED: the telegraph
  mechanisms (halo + level flicker + outline swell + ring pulses) are
  INTACT at both commits, while the L1 scale covenant (eb2e766) thinned
  the strokes under the signal 3.6–5.1×, so a congesting link barely
  widens any more.
- USER RULING 2026-08-27 (lavish session, on record): **R1 → RESTORE via
  option A1** (congested-state width emphasis).
- **R2 lane stripes and R3 Dublin blocks are LEAVE** (standing
  recommendation, no ruling) — DO NOT restore, reference, or widen scope
  toward them. A2 (ladder retune) / A3 / A4 are OUT too.

## Scope — A1 exactly

In `draw_bundles` (BOTH branches), for `lvl != .None`:

- Draw the halo at `max(band + 5×scale, congestion_floor×scale)` with
  `congestion_floor ≈ 10–14 world px` — tune within that band for the
  clearest read; OR bump the halo offset to `+8..+10×scale` for red.
  The appendix blesses both variants — pick the one that reads best at
  all three zoom rungs and re-blesses cleanest (or combine, if that is
  what the read needs — stay within the appendix's described envelope).
- Code anchors @ 03dd6f8: `view.odin:994` / `:1071` (halo draws),
  `:769` (`link_width_capped`).
- **Calm-board geometry stays BYTE-IDENTICAL** (covenant caps the STROKE;
  the telegraph layer is emphasis — that is the no-conflict rationale;
  your gates must keep it true).
- No sim/log bytes (ODN-1-safe).

## Gates — mutation-leg standard (a pin that can't fail is vacuous)

- A congested-width gate that FAILS when the emphasis is deleted
  (delete-the-bump leg RED, then GREEN).
- A calm-board covenant pin that stays GREEN (calm links byte-identical
  — the flags-off/calm proof).
- Re-bless the congestion-bearing goldens per the appendix risk list:
  warn ×3, juice/a11y@65s ×6, surge/estate_surge if engaged; palcheck §7
  involved-non-recede legs re-pinned to the new expectations.
- Motion-strip evidence: congested-link width series BEFORE vs AFTER
  (the audit's strip method, T1-hash-verified timelines) — the deliverable
  proof that the READ is back at every rung.

## Skills policy

- `bmad-build` (step 04 review swarm MANDATORY — never skip; adversarial
  + edge hunters).

## Model policy

- Minion: zai-coding-cn/glm-5.3-flash, --thinking max. Mega-minions
  inherit the same pin (natively multimodal; vision inline).

## PR + Perkins

- pr_review=1 (canon-surface visual code). PR vs `v2`.
- `bin/check-pr-ready` before close-out; verdict posts as the
  perkins-review bot.
- CI note: GH-Actions billing block may show 5s runs / zero logs /
  "payments failed" — that signature is note-only, reruns are useless;
  local gates are the merge ground truth.

## Constraints

- mechanics-quinn (idle design session) holds the packet-plumber main
  checkout — you run in a worktree; never touch its surface or pane.
- bash 3.2 on this machine — no arrays in scripts.
- Doc hygiene: ONE line in the repo's LOOK-SPEC noting the A1 amendment
  (congested emphasis layer ≠ covenant change) — no essays.
- Lane stripes / Dublin blocks / ladder retune: OUT OF SCOPE, flag only.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-congestion-read-a1
- base: v2 (Silas resolves the fresh head at dispatch)
- model: zai-coding-cn/glm-5.3-flash --thinking max
- github_issue: (none)
- pr_review: 1
