# Briefing — packet-plumber-v2-7.1-visual-juice (story 7.1 — visual juice, light-canvas polish)

- **Job id:** `packet-plumber-v2-7.1-visual-juice`
- **Repo:** packet-plumber · **Base:** `v2` @ post-5.5-merge head (HELD — Silas
  resolves the exact sha at release; see the hold note below) ·
  **Slug:** `v2-7.1-visual-juice`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-v2-5.5-demolish-input` merge close-out (5.5 adds the demolish
  popover chrome; this job polishes the same chrome surface — dispatching early
  guarantees rebase collisions). Record the hold on the row.
- **Model policy:** `kimi-coding/k3` (USER RULING 2026-08-17 — this is a VISION job:
  applying the look-book canon, judging T2 pixel goldens, and reviewing re-bless
  before/afters all need a model with native vision). Any mega-minion you spawn
  launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter). **`lavish` is
  MANDATORY: the style-direction deliverable goes through a lavish in-browser
  review gate BEFORE any full implementation — the user works with you directly
  in the browser (pick / blend / annotate / send back). Clarify questions also
  go through lavish when practical.**
- **Perkins:** `pr_review: 1` (view/canon art surface). **Loop ruling (user,
  2026-08-17, "keep going"):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-7.1-visual-juice <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 7.1
  (relative to `/Users/moses/code/packet-plumber`). Read it + `sprint-plan-v2.md` §7
  row BEFORE designing.
- **Canon (AMENDED — user ruling 2026-08-17: "those are ugly; use the Mini
  Motorways style for reference"):** the look-book's PALETTE (`look-book-v1.md`
  §2 hex tokens) and SHAPE LANGUAGE (literal buildings, round router pucks,
  packet personalities, tiered pipes) STAND. The 8 reference renders are
  DEMOTED: they anchor composition + shape language ONLY — never surface
  treatment (no 3D materials, bevels, bloom, gradients, drop shadows). The
  surface-style target is **Mini Motorways flat-2D minimalism**: flat solid
  colors, crisp clean roads/pipes, simple geometric silhouettes, generous
  whitespace, pastel-on-cream, zero texture noise. Your model has native
  vision — fetch 3–5 Mini Motorways gameplay screenshots (web) into the
  worktree for study (reference only, do NOT commit them), and read the
  look-book renders for composition only. Record this amendment as a
  one-section addition in `look-book-v1.md` in the same PR (canon stays
  durable + diff-able). **No Blender MCP, no re-rendering.**
- **CI:** GitHub Actions is org-billing-blocked — note-only; the LOCAL suite is
  ground truth. `tools/ci-local.sh` (9 gates) must pass; keep it green.

## Mission — implement story 7.1 (visual juice, light-canvas polish)

**The goal:** the light-canvas canon (warm-cream map, colored packet dots, node
health colors, leak spray) in the **Mini Motorways flat-2D style** (see the canon
amendment above), plus UI chrome (gauges, forecast, alerts) with progressive
disclosure + filter/focus + alerts-as-nav. **This pass SETS the production visual
direction** — v2 graduated to the full-game build (user ruling 2026-08-17); the
lavish-chosen direction IS the game's look.

**THE SHAPE OF THE JOB — two phases, lavish-gated (user ruling 2026-08-17):
"I need to work with the minion; present the options via lavish before
proceeding."**

**Phase A — style options + lavish gate (NO full implementation yet):**
1. Study: the look-book palette + shape language; 3–5 fetched Mini Motorways
   reference screenshots (worktree-only, never committed); the current game's
   rendered frame.
2. Build a **style probe**: 2–3 candidate surface treatments applied to the
   SAME representative game frame (a busy mid-game moment with pipes, packets,
   a strained node, chrome) — rendered as REAL frames from the game's own draw
   code (headless frame dump behind a probe flag; NOT mockups from other
   tools). Candidates explore the flat-MM space within palette + shape
   constraints (e.g. pipe treatment variants, packet glyph variants, chrome
   weight). Keep the probe cheap — it is thrown away after the verdict.
3. Present via **lavish**: candidates side-by-side against an MM reference,
   each with a one-paragraph rationale + the palette/shape fidelity notes.
   The user picks, blends, annotates, or sends back — iterate the probe until
   a verdict lands. **HARD GATE: do NOT start Phase B before the lavish
   verdict.** Report the verdict verbatim in your next self-report.

**Phase B — implement the chosen direction:** the hard requirements below, with
"the chosen direction" substituted wherever surface treatment is concerned.

**Hard requirements (Phase B, all pinned by the card):**

1. **Palette per look-book, surface per the lavish verdict.** Apply the §2 hex
   tokens exactly; node health states stay readable; the leak-spray
   affordance where canon specifies; shape language per the renders
   (buildings vs pucks). Surface treatment = the user's lavish-chosen
   direction — where an old render implies 3D/glow/bloom/bevel, flat wins.
   Note each adoption in the PR.
2. **View purity `[ODN-1]`.** The View reads ONLY snapshots — polish must never
   perturb the sim. No new snapshot fields without a deliberate, documented reason;
   replay byte-identical `[E10]`.
3. **Chrome with progressive disclosure.** Gauges / forecast / alerts get
   filter/focus + alerts-as-nav per the card — consistent with the 5.5 demolish
   popover's chrome idiom (it just landed; match its patterns, don't invent a
   second chrome language).
4. **Never-color-alone.** Packet type and node state stay readable without color
   (icon/shape/outline companions) — 7.3 builds the full a11y modes; you hold the
   baseline contract in everything you touch.
5. **Camera-fit.** The viewport scales so wider/taller screens reveal more map.
6. **Goldens.** New T2 of the juiced frame; existing goldens re-bless ONLY where
   the juice provably changes pixels — each re-bless listed in the PR with
   before/after (the 4.3 re-bless discipline). `tools/ci-local.sh` 9/9.

**Acceptance:**

1. **Phase A gate passed:** lavish verdict recorded verbatim in the PR body (+
   the look-book amendment section); the chosen direction is what shipped.
2. Card's Given/When/Then verified; `[ODN-1]` view purity + never-color-alone held.
3. New T2 juiced-frame golden; deliberate re-blesses documented; local suite green.
4. PR body carries: canon citations (look-book sections + the amendment), the
   MM style references studied, the lavish session link, the chrome idiom notes
   (vs the 5.5 popover), the re-bless list with before/after, the camera-fit
   behavior.
5. Story card status line updated in the same PR (the established pattern).

**Scope guard:** visual juice ONLY. No new mechanics, no balance changes, no
core/snapshot changes, no a11y MODES (7.3), no audio (7.2), no asset
regeneration, no re-rendering of the old canon renders. The Phase-A probe is
disposable — do not productize it. No GDD/canon changes beyond the one-section
look-book amendment named above.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-7.1-visual-juice
base: v2
model: kimi-coding/k3
pr_review: 1
```
