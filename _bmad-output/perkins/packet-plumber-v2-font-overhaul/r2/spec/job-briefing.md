# packet-plumber-v2-font-overhaul

## Task

Replace the raylib default font with a real, readable typeface across
the whole UI. User ruling (2026-08-22): "the current font in general is
hard to read — we need a font overall, esp the headers, generally hard
to read." Context: v2-ux-font-resize (2026-08-15) resized sizes and
audited contrast but kept the raylib default FAMILY — the resize was
the band-aid; this is the cure.

## Rules (hard)

1. **User picks the family.** Propose 3–4 candidates (suggested:
   Atkinson Hyperlegible — accessibility king; Nunito or Quicksand —
   rounded, MM-adjacent warmth; IBM Plex Sans — + its Plex Mono
   sibling for the NOC panel; Inter — the safe modern default). Render
   an A/B gallery of each candidate on the SAME screens (headers,
   HUD chips, health panel, QoS panel, NOC dashboard, crisis banner,
   title) via lavish — KYLE grades each on readability verdicts
   (remote glm-4.6v is back; local glm-4.6v-flash is the fallback),
   the USER picks at the lavish review. Never ship un-reviewed.
2. **OFL or equivalent license only** — verify and document per
   candidate (all four suggestions are OFL).
3. **Headers are the headline fix** (user's explicit callout) — title
   screens, panel headers, the crisis banner get real weight/size
   hierarchy. Body and labels follow the established 2026-08-15 sizing
   minimums (12→14px floor) unless a candidate demands re-tuning —
   justify any size changes in the PR.
4. **Mono pairing**: the NOC panel (PR #85) needs tabular numerals —
   if the picked family has no mono sibling, pair a dedicated mono
   (IBM Plex Mono / JetBrains Mono — OFL). The NOC readability ruling
   (2026-08-22) is canon for the panel.
5. **View-layer only** — text is rendering; determinism untouched.
   T1/T2/replay streams must stay byte-identical (hash-equal proof in
   PR body). Raylib font loading: LoadFontEx with anti-aliasing (or
   SDF if quality demands — justify).
6. **Golden storm expected** — every text-bearing golden changes.
   Document the cause (font family swap) on the re-bless; do NOT touch
   gameplay goldens beyond text pixels (palette/layout unchanged).
   Non-ASCII glyphs: verify the candidate covers what the game uses
   (the raylib default broke on ⚠ — the new font must not regress;
   test it).
7. **Merge order: LAST among the current wave** — the golden storm
   collides with every in-flight PR (#82, #84, scale-depth, #85).
   Work starts now in the worktree; the FINAL re-bless + push happen
   on the settled head after those merge. Coordinate with Silas.

## Acceptance

- Lavish A/B gallery (before/after per screen, all candidates) with
  KYLE readability verdicts per candidate; user's pick recorded.
- Headers visibly stronger (before/after side-by-side in PR body).
- ⚠ / non-ASCII glyph test passes (no raylib-default regression).
- T1/T2/replay hash-equal.
- NOC panel renders in the mono pairing, tabular-figure steady.
- All re-blessed goldens cause-documented; PR lands LAST in the wave.
- pr_review: 1.

## Skills policy

bmad-quick-dev; lavish for the A/B gallery; KYLE (glm-4.6v, local
4.6v-flash fallback) for readability verdicts.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-font-overhaul
- base: v2 (fresh head at dispatch; final re-bless rebases to the
  settled head)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- merge order: LAST (after #82, #84, scale-depth, #85) — work now,
  final push on the settled head
