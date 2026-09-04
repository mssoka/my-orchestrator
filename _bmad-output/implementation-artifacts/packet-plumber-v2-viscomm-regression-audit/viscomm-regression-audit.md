# Case File: packet-plumber-v2-viscomm-regression-audit

**Job:** packet-plumber-v2-viscomm-regression-audit · READ-ONLY forensic audit, no code changes, no PR.
**Question:** after PR #105 (look-zoom-language, merge `03dd6f8`), some viscomm video effects LOOK LOST. Per effect: INTACT / DEGRADED / LOST / FLAG-GATED, with mechanical evidence and the exact severing commit+hunk.
**Skill:** gds-investigate discipline (evidence-graded findings); bmad-build renderer waived per the standing 2026-08-21/23 ruling.

## Hand-off Brief

No viscomm effect's code path was silently severed by #105. All four prime suspects were cleared mechanically: the sprites-only Dublin switch, the view.odin rewrite, the L3 reduced-motion pin, and the flag defaults each leave every lane effect reachable. What actually happened splits three ways: (1) every animated pulse mechanism (node rings, crisis outline swell, congested-link level flicker) is byte-verifiably ALIVE at both commits; (2) two visual surfaces were DELIBERATELY retired by the 2026-08-26 LOOK-SPEC rulings (lane stripes, Dublin street blocks) — lost-by-ruling, not lost-by-bug; (3) the link congestion telegraph — the user's named keep candidate — is DEGRADED in READ, not in mechanism: its recolor/flicker code is identical at both commits, but the stroke under it went from 16–23 px ribbons to 3.5–6 px ladder strokes (fit) and 33–55 px to 9 px at the resting zoom, collapsing the telegraph's canvas area ~4–6×. Confidence: HIGH (code traces at both commits + 200 strip frames + pixel measurements + green test gates).

## Case Info

| | |
|---|---|
| BEFORE | `088cf00` (merge of #104 — parent of the #105 branch) |
| AFTER | `03dd6f8` (merge of #105 — v2 HEAD) |
| Range | 5 commits: eb2e766 (L1), 33b4bbd (L2), e47d0e2 (L3), 5910ccd (L4), d5dd5a6 (review fold) |
| Diff surface | app/: 13 files, +1067/−407 — view.odin (+473/−402), dublin.odin (−165), wire_path.odin (−47+…), sprites/camera/crisis/assist/main + 3 new test files |
| Builds | rlsw SW harness built at BOTH commits (`ODIN_ROOT=<main>/tools/raylib-sw/shadow`); AFTER corpus run **49/49 demos green** (byte-faithful to the blessed goldens) |
| Gates | palcheck all green BOTH commits (93 PASS lines AFTER vs 70 BEFORE — the look legs are the delta); `odin test app/render` 114 + `odin test app` 51 green at AFTER |
| Captures | `captures/before|after/` (era goldens), `captures/strip_before|after/{warn,warn_early,juice}/` (50 frames each, 50 ms cadence, T1-hash-verified timelines) |

## Method

1. **Inventory** from the video's 7 effect classes, the design-audit artifacts (findings A/B/C), the five PR bodies (`_pr_body_*.md`), and the look_l1/l2/l4 + palette_polish + pullback tests.
2. **Path trace BEFORE vs AFTER**: full proc inventory of view.odin; every draw call site grepped at both commits; the complete view/wire_path/sprites/camera/dublin/assist/crisis/main diffs walked hunk by hunk.
3. **Mechanical proof**: rlsw builds at both commits; `motion-strip` captures (warn 44.0–46.5 s, warn 1.0–3.5 s, juice 64.0–66.5 s; 50 frames each side); PIL pixel measurement (colors, thicknesses, per-frame oscillation); golden-corpus diff.
4. Vision (native multimodal) used for screening only; every verdict below rests on pixel numbers or code identity.

## Findings (evidence-graded)

### F1 — Gauge telegraph (count-up lerp + chunk flash) — **INTACT** (Confirmed)

- #100's surfaces: `app/render/gauge.odin`, `app/render/health.odin` — **zero diff lines** in 088cf00..03dd6f8. The #105 diffstat does not touch them; `draw_health_meter`'s tick param and the app feed wiring (main.odin) are unchanged.
- Mechanical: palcheck §6 draw-path legs green at AFTER — "mid-ease fill sits at the EASE16-predicted edge (212 px vs raw 182)", same for pool; ghost/reduced-motion legs PASS.
- Verdict: the video's count-up-lerp and flash-before-drain classes are fully live. HUD **counters** were never lerped by design (truth channels stay RAW per #100) — that is spec-faithful, not a regression.

### F2 — Crisis desaturation (attention-via-contrast, #102) — **INTACT** (Confirmed)

- `crisis_desat_factor` + `crisis_recede*` untouched (the only crisis.odin diff in range is the outline-width covenant hunk, d5dd5a6). `draw_world` still derives `desat_f` once per frame and threads it through bundles/nodes/packets (view.odin:540 AFTER).
- Mechanical: juice@65s (zone crisis, fully engaged) has **0 vivid network-token pixels at BOTH commits** (tolerance 28 on copper/steel/gold); calm@30s vivid ink 23,771 px (BEFORE) vs 7,252 px (AFTER) — the delta is the thinner ladder, not the desat.
- palcheck §7a–f all green at AFTER (raw-absent, involved non-recede, rider recede, mid-ramp three-way, reduced-motion pin, Dublin leg).
- Dublin nuance: the STREET-BLOCK recede surface retired with the blocks (F9); the recede mechanism itself is map-agnostic and now rides the sprite family wash (`draw_family_wash(..., recede)` unchanged, `DUBLIN_WASH_SCALE` 0.45 applied before the recede alpha math). The §7f leg was re-pinned in #105 to sprite-presence with the comment "the recede mechanism is map-agnostic, pinned on the procedural legs above".

### F3 — Tie de-conflict (#99) — **INTACT** (Confirmed)

- `data/palette.json` untouched in range (`route_tie` stays `#BA5EE8` @ 280°); `tie_dash_on` / `tie_dash_segments` / `draw_tie_mark` unchanged (assist.odin's only range-diffs are two width derivations moved to `link_width_capped` + the ghost-halo 2.2× fix, both review-fold items).
- `draw_route_glow` call sites (main.odin:752/756) identical at both commits.

### F4 — **LINK CONGESTION PULSE** (restore-candidate #1, user-named) — mechanisms **INTACT**, read **DEGRADED** (Confirmed, both halves)

**The mechanisms are alive — identical code, identical dynamics:**
- The 4.1 congestion halo draw is **byte-identical** at both commits in BOTH branches (inline view.odin:916–930 BEFORE / 994–1008 AFTER; routed 1017–1031 / 1071–1085): `halo = raw×0.57 + state×0.43`, `w = band + 5×scale`, drawn over the stroke. No pulse envelope existed on it at either commit — the halo is a recolor, by code.
- The **level flicker** (the visible "pulsating"): warn strip, router→host link centerline, x=780 — BOTH commits step `(99,115,166)` (steel×red) → `(104,163,166)` (steel×amber) at exactly 44.4 s, then back — the congestion level crossing thresholds re-tints the link, identically phased.
- The **crisis outline swell** (PULSE16 red stroke on the crisis bundle's member pipes — the one true pulsating-link effect): juice strip red-ink oscillates with the same 16-tick period and phase at both commits — BEFORE 4367→5148→4367 px, AFTER 2175→2867→2175 px.
- The **node health rings** (1.25 Hz amber / 2.5 Hz red): warn-early strip, red ink cycles with the 8-tick period at both commits — BEFORE [919,897,927,965,964,1001,964,945], AFTER [588,566,596,634,633,670,633,614]; ring radius base `s×0.95` unchanged; `!!` glyph + double ring confirmed visually at both (captures/crops/host_pulse_*.png).

**What degraded is the canvas the telegraph paints on (severed by eb2e766, L1):**

| measure | BEFORE (088cf00) | AFTER (03dd6f8) | ratio |
|---|---|---|---|
| standard link @ fit zoom 1.0 (CORE) | 7.4×2.2 = 16.3 px + 4.5 casing | 3.5 px single stroke | **4.7× thinner** |
| wide link @ fit | 10.5×2.2 = 23.1 px + casing | 6.0 px | **3.9× thinner** |
| standard @ boot zoom 2.0 (ACCESS) | 32.6 px + casing = 41.6 | 9.0 px | **3.6× thinner** |
| wide @ boot zoom 2.0 | 46.2 px + casing = 55.2 | 9.0 px (ACCESS uniform) | **5.1× thinner** |
| congested recolor area @ fit (per link length) | 21.3 px × L | 8.5 px × L | **~6× less ink** |
| calm-board vivid link ink (juice@30s) | 23,771 px | 7,252 px | ~31% |

The L1 laneless ruling removed the ×2.2 band factor, the casing, and the lane stripes, and imposed the 0.5×-node covenant. Every pulse mechanism survived; the fat glowing ribbon the user remembers — the thing that made congesting links READ as pulsating — is now a thin stroke with the same recolor math on ~1/4–1/6 the area. **This is a perceptual regression of the telegraph's salience, not a severed code path.** Severing commit: `eb2e766` (L1: "the scale covenant + the laneless link ladder") — hunks: `BUNDLE_EXTRA_WIDTH/CASING_OVERHANG/casing_color` deletion + `band_width` re-derivation (`tier+extra)×2.2 → link_width_world×scale`) + the inline/routed draw rewrites in `draw_bundles`.

### F5 — Node telegraph (rings + glyphs + pulse) — **INTACT** (Confirmed)

- `draw_health_ring` unchanged in range (pulse_read seam, radius base, advance rates 1/2 table-entries per tick, glyphs). `draw_nodes` still calls it for every `lvl != .None` node; the crisis recede never touches rings (telegraph family).
- Mechanical: the 8-tick red pulse cycle measured at both commits (F4); `!!` + double-ring crops visually identical except the node size under them (the L4 ladder).

### F6 — Crisis outline swell — **INTACT** (thinner by ruling) (Confirmed)

- `draw_crisis_outlines` swell code unchanged (PULSE16, phase `(tick+bundle)%16`, reduced-motion pin). Still called from draw_world:550. The ONLY range change is the width basis: `band_width(...) → link_width_capped(...)×scale` (d5dd5a6 — the adversarial hunter's fold: the outline must hug the capped stroke). Swell oscillation verified in the juice strips (F4). Ink count ~55% of BEFORE — direct consequence of the thinner host stroke, by ruling.

### F7 — Packet affordance (trails, glints, rider lattice, involvement pins) — **INTACT** (Confirmed)

- `pkt_interp`/`TRAIL_FADES`/`trails_active`/glint code identical both commits. The #102 "packet chain pins" = the `crisis_packet_involved` one-resolution-chain pin — untouched.
- The rider lattice width now derives from `link_width_capped` (was `band_width − 2×lane_gutter`): riders compress toward the centerline on thin strokes — documented in the #105 body as the covenant's natural fallout ("Fork 2 is open/parked"). Shape/behavior unchanged.

### F8 — Camera breath / pullback — **INTACT by default; pinned under reduced-motion (deliberate, L3)** (Confirmed)

- The L3 change is exactly scoped: `pullback_feed` gains an early return under `a11y.reduced_motion`, and `set_reduced_motion` freezes in-flight breath targets (e47d0e2 + the edge-case-hunter blocker fold in d5dd5a6). With reduced_motion OFF (the default), pullback behavior is byte-identical: feed keys on estate seeds, wheel overrides, `auto_pullback` default ON (settings.odin untouched). `pullback_test` (new) green.
- No collateral pinning: gauges (#100), pulse surfaces (7.3), desat ramp (#102) already had their own reduced-motion seams BEFORE #105; L3 added only the camera pin. Suspect (c) cleared.
- Known pre-existing issue documented + deferred in #105 (NOT a regression): the N11 auto-pullback toggle shares the latent ease-continues behavior mid-toggle.

### F9 — Dublin street blocks (+ their crisis recede + frontage) — **LOST-BY-RULING (deliberate)** (Confirmed)

- Severed by `5910ccd` (L4 "sprites-only Dublin", the 2026-08-26 user ruling): `dublin_node_block_draw`, `dublin_node_street`, the seg grid + cache, `dublin_screen_tile` deleted wholesale (−165 lines; "a render function never called is not a feature").
- What carries the block's jobs now: Blender sprites on BOTH maps + family wash at `DUBLIN_WASH_SCALE` 0.45; crisis recede rides the wash (F2); type chip unchanged. palcheck §7f re-pinned to sprite presence (involved washed-coral / non-involved washed-sage, both ≥100 px). Dublin@90s before/after: same board, rings, banner; 0.86% pixels changed.
- The block-specific recede twin (§7f's old alpha-twin scan) retired WITH the surface — the mechanism survives on the wash; no orphaned contract.

### F10 — Lane stripes + lane-detail reveal (7.1) — **LOST-BY-RULING (deliberate)** (Confirmed)

- Severed by `eb2e766` (L1 laneless): the lane-stripe walks deleted in BOTH draw_bundles branches; `draw_path_offset_band` deleted; `lane_detail` field removed entirely (zero references remain); `lane_express/standard/best_effort` palette tokens now have ZERO consumers (dead data, kept for palette compat).
- Supersession is explicit in the PR body and LOOK-SPEC §3 ("queues are ingress/egress on ROUTERS; the road doesn't gossip"). The lane-cap DATA seam survives (`bundle_lane_caps_view` still computed for riders), so a future reversal has a live data source.

### F11 — The #105 additions themselves — **PRESENT + PINNED** (Confirmed)

- Dusk dial (L2): warm dots under settlements, cool DC anchor, alphas {0,120,200}/{0,140,210} — visible in AFTER warn@45s (mauve halo around the host) and Dublin@90s (orange settlement glows); "ACCESS dark at rest" leg PASS.
- Node ladder (L4: 1.00/1.10/1.22/1.35) + rung shrink (1.00/0.62/0.42 etc.): "toward-space shrink is monotone (2427 > 285 > 67)" PASS; sprite/body pins PASS.
- Ring floor (L4): `max(2.0, 0.055×tile_px×scale)` — floor pin green (M8 mutation-proven in-PR).
- Covenant + laneless at pixels: palcheck §2 legs green at all three rungs (stroke == table ±1 px; laneless zero-count; covenant ≤ cap).

### Prime suspects — clearance summary

| suspect | verdict |
|---|---|
| (a) sprites-only Dublin severed viscomm draws on the old vector path | The only resident was the block draw's own recede/wash/chip — all re-hosted on the sprite path (F2/F9). Nothing else lived there. |
| (b) view.odin rewrite skips overlay layers | draw_world order intact (map→telegraph→bundles→highlight→nodes→packets→crisis outlines→ghosts→selection); route_glow/health/forecast/HUD call sites unchanged; corpus 49/49. |
| (c) L3 reduced-motion pin gates more than the breath | The pin is two scoped additions (feed gate + target freeze). All other effects had pre-existing seams. Default-off flag → default behavior unchanged. |
| (d) flag lattice defaults gate an effect off | No flag defaults changed in range (route_wires/wire_anchors off, reduced_motion off, auto_pullback on — both commits). `lane_detail` was deleted, not gated. |

## KEEP/LEAVE decision menu (the deliverable's final section)

Per row: added-by PR → status → evidence → if lost/degraded: severing commit + minimal restore hook (described, NOT implemented) → recommendation. **The user rules keep-vs-leave per row.**

| # | Effect (video class) | Added by | Status | Evidence | If lost/degraded: severance + restore hook | Recommendation |
|---|---|---|---|---|---|---|
| R1 | **Link congestion pulse** (distinct telegraphs / idle-motion read) | pre-lane (4.1/7.5), built around by #99 | **DEGRADED (read) — mechanisms INTACT** | Code-identical halo + level flicker + outline swell + ring pulses at both commits (F4 strips); stroke under the signal 3.6–5.1× thinner; recolor ink ~6× less | Severed by `eb2e766` (L1). Restore hook (emphasis, not geometry): give congested links a **min-width floor or a congested width bump** — e.g. `w = max(band, congestion_floor)` in the halo draw, or raise the halo offset for lvl≠None. ~8–10 congestion-bearing goldens re-bless (warn/juice/a11y@65s). No ruling conflict: it emphasizes, it does not un-thin the calm board. | **KEEP the mechanisms** (they are correct and ruling-compliant). If the old READ is wanted back: restore option A1 (below) — cheapest, reversible. |
| R2 | Lane stripes + lane-detail reveal (gestalt/QoS read) | #7.1-era (3.3 canon) | **LOST-BY-RULING** (deliberate supersession) | F10; lane tokens zero consumers; caps data seam alive | `eb2e766`. Restore hook: re-add the 3-stripe walk in both draw_bundles branches behind a `lane_stripes` view flag DEFAULT-OFF (golden-neutral while off), fed by the surviving `bundle_lane_caps_view`. Needs the 2026-08-26 laneless ruling explicitly reversed. | **LEAVE** — the laneless ruling is recorded and fresh (08-26); the thin-stroke language is the adopted look. Revisit only if the user reverses the ruling. |
| R3 | Dublin street blocks + block recede (gestalt/affordance on the real map) | #95 (amendment #2) | **LOST-BY-RULING** (deliberate supersession) | F9; §7f re-pinned to sprites; wash recede carries the crisis read | `5910ccd`. Restore hook: reinstate `dublin_node_block_draw` + seg grid behind a map/flag gate; the deleted code is recoverable from git. Conflicts with the sprites-only ruling; re-blesses Dublin goldens. | **LEAVE** — the sprite path carries the same information (family wash + chip + recede) with better sculpting; the ruling is recorded. |
| R4 | Gauge telegraph (count-up lerp + chunk flash) | #100 | **INTACT** | F1: files untouched; palcheck §6 legs green | — | **KEEP** (no action). |
| R5 | Crisis desat (contrast hierarchy) | #102 | **INTACT** | F2: 0 vivid px at crisis peak both; §7 green | — | **KEEP** (no action). |
| R6 | Tie de-conflict (distinct telegraphs) | #99 | **INTACT** | F3: palette + dash code untouched | — | **KEEP** (no action). |
| R7 | Node telegraph rings/glyphs/pulse (idle-motion) | 5.2/7.3 | **INTACT** | F5: 8-tick pulse cycle measured both commits | — | **KEEP** (no action). |
| R8 | Crisis outline swell | 4.2/7.x | **INTACT** (thinner by the covenant) | F6: 16-tick swell both commits | — | **KEEP** (no action). |
| R9 | Packet affordance: trails/glints/rider lattice | 2.1/#102 | **INTACT** (lattice narrower) | F7: code identical; width follows the covenant | — | **KEEP** (no action). |
| R10 | Camera breath (idle-motion) | pre-#105 | **INTACT by default**; pinned under reduced-motion (deliberate E9.2) | F8: scoped pin; default-off flag | — | **KEEP** (no action). |
| R11 | Dusk dial / node ladder / ring floor / covenant (gestalt) | #105 | **NEW — present + pinned** | F11: palcheck §2 + look tests + visible in captures | — | **KEEP** (no action). |

**Ranking of restore candidates (lost/degraded only):**
1. **Link congestion READ** (R1) — user-named; degraded-not-lost; cheapest restore (A1 below), no ruling conflict.
2. **Lane stripes** (R2) — lost-by-ruling; a flag-gated restore is golden-neutral while off but requires reversing a 2-day-old recorded ruling.
3. **Dublin blocks** (R3) — lost-by-ruling; lowest value — the sprite path supersedes the block's jobs cleanly.

## Rulings received (lavish review loop, 2026-08-27)

The user reviewed the HTML artifact and ruled via the KEEP/LEAVE menu, then ended the session:

- **R1 (link congestion READ) — RESTORED via option A1** (congested-state width emphasis). USER RULING ON RECORD 2026-08-27. This audit does NOT implement: A1 routes to a follow-up fix job (see Appendix A1 for the described hook: congested-state halo min-width/bump, ~8–10 congestion-bearing goldens re-bless, palcheck §7 re-pin, ODN-1-safe).
- **R2 (lane stripes) / R3 (Dublin blocks) / R4–R11 (intact rows) — no ruling queued**; the session closed with only R1's answer. The menu defaults (LEAVE / LEAVE / KEEP all) therefore stand as this report's recommendations, not user-confirmed rulings.

## Appendix: restore options (ranked, with risk — described, NOT implemented)

- **A1. Congested-link emphasis (restores the pulse READ; recommended if the user wants R1 back).** In `draw_bundles` (both branches), for `lvl != .None` draw the halo at `max(band + 5×scale, congestion_floor×scale)` with `congestion_floor ≈ 10–14 world px`, or bump the halo offset to `+8..+10×scale` for red. Effect: a congesting link visibly widens/warms again at every altitude — the "pulse" read returns without touching calm-board geometry or the covenant (the covenant caps the STROKE; the telegraph layer is emphasis). Risk: LOW-MED — re-bless the congestion-bearing goldens (warn ×3, juice/a11y@65s ×6, surge/estate_surge if engaged); palcheck §7 involved-non-recede legs may need re-pinned expectations; no sim/log bytes (ODN-1 safe).
- **A2. Ladder retune (partial band-factor return).** Raise `link_base_world` tables (e.g. ACCESS 4.5→7, CORE 3.5→5) or reintroduce a mild pooled-growth step. Restores overall link presence (R1 + general "links look lost" read) but softens the ruled scale covenant and re-blesses EVERY golden (all 49 demos have links). Risk: MED-HIGH — full corpus re-bless + the ruling itself; only with the user reversing the LOOK-SPEC widths.
- **A3. Lane stripes behind a default-off flag.** Restores the QoS lane read for zoomed play. Risk: LOW while off (byte-neutral), but contradicts the recorded laneless ruling and re-adds a surface the 08-26 ruling explicitly superseded; the caps data seam survives so implementation is a re-walk, not a rebuild.
- **A4. Dublin blocks return.** Risk: MED (Dublin golden churn, ruling reversal); information value already covered by sprites — not recommended.

## Evidence register

- Builds: rlsw harness at both commits (ODIN_ROOT → main checkout's shadow, read-only); AFTER corpus 49/49 green; palcheck green both (93/70 PASS lines).
- Strips: `harness motion-strip` warn 44000–46500/50 ms, warn 1000–3500/50 ms, juice 64000–66500/50 ms — both commits, T1-hash-verified timelines, 300 frames in `captures/strip_*/`.
- Key measurements: link centerline color series (steel×red → steel×amber at 44.4 s BOTH); link thickness 20 px vs 8 px const; ring-red 8-tick cycles; crisis-red 16-tick cycles; vivid-token counts (23,771/7,252 calm; 0/0 crisis); Dublin diff 0.86%.
- Severing commits: lane stripes `eb2e766`; Dublin blocks `5910ccd`; crisis-outline covenant `d5dd5a6`; halo draw: NO change in range.
- Code citations (AFTER @ 03dd6f8): view.odin:522 (draw_world), :994/:1071 (halo draws), :1161 (draw_health_ring), :769 (link_width_capped), :884 (PULSE16); crisis.odin:138 (crisis_desat_factor), :341 (draw_crisis_outlines), :384-390 (covenant hunk); assist.odin:494 (tie_dash_on); sprites.odin:244-306 (rung tables); camera.odin:259-306 (rungs); main.odin:1199 (set_reduced_motion), :1912 (pullback_feed). BEFORE equivalents at 088cf00 cited in F4/F9.
