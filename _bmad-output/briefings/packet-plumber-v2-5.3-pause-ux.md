# Briefing — packet-plumber-v2-5.3-pause-ux (user report: pause overlay defeats pause-and-plan)

- **Job id:** `packet-plumber-v2-5.3-pause-ux`
- **Repo:** packet-plumber · **Base:** `v2` @ 7b56485 · **Slug:** `v2-5.3-pause-ux`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (gameplay-surface rendering + GDD canon amendment).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.3-pause-ux <url>` yourself.
- **First step:** file the GitHub issue yourself (labels: `bug`, `priority:medium`)
  capturing the user report below, then close it with the PR (`Fixes #N`).
- **CI:** green (billing fixed). Full local suite must pass regardless.

## Mission — fix the pause overlay (USER REPORT 2026-08-14, ruling-grade)

**User's words:** "when pause, 1. it dims the whole map, 2. the text is right in the
middle of the page. the whole point of pausing is to be able to think and link nodes.
those 2 things hinder that. you can see the prototype as an e.g."

**Ground truth:** the prototype (`/Users/moses/code/packet-plumber-prototype-ref`,
read-only reference) shows paused with **NO overlay at all** — sim frozen, map at
full brightness, no dim, no center text. That is the desired behavior baseline.

**The defect (v2 `app/main.odin:242-250`):** paused draws a full-screen dim veil
(`DrawRectangle` full-viewport, alpha 130) + a 48px "PAUSED" dead-center + a centered
hint line. Both sabotage pause-and-plan: the dim makes the map hard to read, the
center text sits exactly where the player is trying to think and link.

**The fix:**

1. **No full-screen dim.** The paused world renders at full brightness — identical
   to the running world (minus stepping). Delete the veil rectangle entirely (do
   NOT keep a "subtle" dim — prototype shows none).
2. **Indicator out of the play area.** Replace the center block with a SMALL,
   unobtrusive paused indicator in a screen-edge position (e.g. a compact "PAUSED —
   P/Space to resume" chip top-left or top-right, sized like other HUD chips —
   follow existing HUD chip styling in `draw_hud`). It must not overlap the map's
   interactive area more than any existing HUD element does. If the HUD already has
   a status area, prefer integrating there over a new floating element.
3. **Pause-and-plan stays fully live:** draw/place/demolish/QoS fast-paths unchanged
   (r1 pinned these — no regression). The change is presentation-only.
4. **Canon amendment:** the current overlay was justified as "the GDD canon
   indicator" (see the code comment + the 5.3 story/GDD text). Amend the GDD/architecture
   line(s) that specify dim+center to the new design (full-brightness world, edge
   chip indicator, prototype-aligned) so canon and code agree — the PR ships the
   ruling.

**Acceptance:**

1. Paused rendering: no veil, no centered text; world at full brightness; edge-chip
   indicator visible + styled consistently with the HUD.
2. All 5.3 pause-and-plan behaviors re-verified (edit fast-path live while paused —
   the existing pause tests must stay green; add/adjust an app-level test pinning
   the new overlay position if the harness supports it).
3. Goldens: if any golden captures a paused frame with the old overlay, update it
   DELIBERATELY and list it in the PR body (rendering change is intended; sim-level
   goldens must NOT shift — determinism spine untouched).
4. GDD/story canon line amended in the same PR.
5. Full local suite green (`make test-all` or the repo's equivalent); PR body shows
   before/after rationale + `Fixes #N` (the issue you filed).

**Scope guard:** the pause overlay presentation + its canon line ONLY. No changes to
pause toggle keys, stepping/accumulator logic, edit fast-paths, QoS, or anything
5.7-telemetry touches.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.3-pause-ux
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
