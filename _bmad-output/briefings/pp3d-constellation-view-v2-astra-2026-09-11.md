# PP3D — constellation view v2 (Astra @ xhigh)

## Latest user ruling — 2026-09-12, reference question RESOLVED

**The CURRENT PP3D planet is the visual/content reference, not an Odin/Dublin board.**
Read `/Users/moses/code/_bmad-output/briefings/pp3d-constellation-same-live-planet-ruling-2026-09-12.md`.
Preserve that same planet's look, water bodies, boats, land, greenery, every asset and
running animation; only flatten its spatial presentation. No replacement map,
Odin golden, reskin or static reconstruction. The user answered in Gru chat; do not
ask them to repeat the answer in Lavish. This supersedes all earlier Odin-framing
language. The OpenAI hold was lifted by the user's confirmation on 2026-09-12.

## Original authority (hold release now satisfied)

User ruling 2026-09-11: the GLM constellation attempt (PR #26, closed unmerged) is
DISCARDED; the lane is REASSIGNED to **Astra @ xhigh** (the 3D vision-capable native
multimodal model) once OpenAI tokens return. **Release trigger: the user confirms
OpenAI tokens returned** (the quota-hold lift). Everything below is the full updated
requirements set — the v2 worker starts here, not from scratch.

## The feature (unchanged canon)

The flattened constellation view for **ALL levels** (GDD D5b): the tiny planet becomes
flat — an **exact copy of the tiny planet, split open and flattened** (shared flatness
morph 0..1 over planet + all surface content, one scene/one state), a HUD toggle
(planet ⇄ flat), and the transition = **a smooth zoom-out carrying the flatten morph**
(clean easing, interruptible/reversible mid-morph). Architecture in
`scenes/levels/level_base.tscn` + shared view-mode plumbing (reuse/extend the
`flow_view` pattern).

## The v2 look requirements (user look-review 2026-09-11, verbatim specifics)

1. **Water present in the flat read** — the globe's oceans/water bodies must exist in
   the flat map (the GLM attempt shipped waterless flat maps).
2. **No starfield/space around the flat map** — flat mode must not read as a map
   floating in space.
3. **Same-world flat framing** — frame the flattened CURRENT PP3D planet so it reads
   as a flat map without surrounding space, while preserving its existing visual
   treatment. No Odin/Dublin framing reference or imported 2D map style; the user's
   2026-09-12 ruling explicitly selects the current planet itself.

## Proven assets from the GLM attempt (reuse; commits visible in closed PR #26)

- The **seam-cut** flat-map approach — numerically twin-verified (r3: 0 seam-straddling
  faces, watertight f=0, shell deviation 3.6e-15; widest non-polar span 2.4380 ≤ 2.5).
- The **soup-index synthesis** for SurfaceTool-built meshes (r2 blocker fix — Nil
  ARRAY_INDEX emptied the re-emit).
- The **SphereMesh water-boot restoration** + ArrayMesh.add_surface_from_arrays
  correction + float32 tolerances (the 4000117 fix cycle).
- The **wall-clock poll** (B2 fix) and the morph-cache geometry pins.
- The **lane-2 execution-green evidence**: focused + full suite PASS 0 failures at
  `4000117`; 4 same-state captures (committed in the PR's `captures/` +
  `VISION-EXACT-COPY-FINDINGS.md`).
- Astra itself is natively multimodal — the v2 worker verifies its own flat renders
  directly (no separate vision route needed).

## Known polish queue (from the GLM attempt's artifacts — carry as candidates)

- Jagged sawtooth spikes at the right map edge (cloud geometry clipping the board).
- Flat gray coastal slabs (unfinished terrain meshes).
- Stray gray circle blobs on open water.
- Board-edge/frame treatment so the paper-map framing feels deliberate.
- Uneven content density (empty open water, featureless gray regions).

## Verification expectations (Astra-era)

- Numeric-twin seam/cache discipline carries over (the r3/r4 method is the standard).
- The windowed capture-class discipline (import precondition, ≤900s, receipts,
  display-awake requirement — the frame_post_draw lesson).
- The exact-copy check: Astra reads its own renders directly (multimodal), same-state
  captures globe ⇄ flat.
- Focused + full suite green (the #29 pin = the one tolerated failure until its
  follow-up lands).

## Bounds

- Astra @ xhigh (the model policy resumes at lift). No kimi/glm on this lane.
- pr_review=1, focused PR to main, user merges. All-levels canon amendment (D5b) rides
  the v2 PR.
- The GLM-attempt artifacts (issue #25 notes, the closed PR #26, the vision findings)
  are reference material — the v2 worker does not re-derive them.
