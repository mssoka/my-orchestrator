# viscomm(crisis): desaturate the non-involved network during crisis (audit finding C)

## What

The user's parked design ruling (2026-08-25), answered: crisis-time hierarchy
via **desaturation of the non-involved network**. When everything screams,
nothing reads as urgent — during an active `Saturated_Bundle` crisis, every
non-involved pipe band, packet, and node accent recedes toward the board's
calm register (a 65% mix toward the canvas paper at full engagement), so the
**crisis zone is the only saturated thing on the board**. This is the
v2-network-pop mechanism (vibrant network on calm paper) inverted
dynamically: under crisis, the non-involved network joins the paper.

## The mechanism (render-side only, ODN-1)

- **Factor** — `crisis_desat_factor` (app/render/crisis.odin): a PURE
  function of the serialized crisis rows + the tick (no app-fed View state —
  unlike the gauges, the harness capture path must render it, so crisis
  goldens carry the desat). Engage eases over 16 ticks from the EARLIEST
  active `Saturated_Bundle` onset via the pinned `CRISIS_FADE16` table
  (PULSE16 pattern, compile-time pins); resolve SNAPS back to 0 — the color
  flood is the "you fixed it" relief read, and it guarantees resolved
  captures return to canon bytes exactly.
- **Involvement (the final predicate)** — a bundle is involved iff it is the
  named canonical `(bundle_lo, bundle_hi)` pair of an active
  `Saturated_Bundle` row (the B1-stable identity, never the compaction-prone
  slot); a node iff it is an endpoint; a packet iff it rides an involved
  bundle or sits at an involved node. **`Pool_Exhaustion` carves no zone**
  (map-wide: the whole network IS the flaw — desaturating it would mute the
  packet-pile evidence of the crisis; the banner + the pool gauge's SHEDDING
  tag carry it). The dublin@90s golden caught this empirically: era-3 growth
  fires a pool crisis there, and the first cut receded everything.
- **The mix** — plain-arithmetic lerp toward `palette.canvas`
  (`CRISIS_DESAT_MIX = 0.65`, the briefing's 60-75% range), no
  transcendentals (§10.4). A canvas mix, not a gray mix: gray pipes would
  read COLDER than the warm board and stick out the other way; hue families
  survive at reduced chroma. Alpha-layer accents (family washes, tier
  markers, chip glyphs) fade via the alpha twin (`crisis_recede_scale`).
- **What NEVER recedes**: the state triad / warning halos / health rings /
  the crisis outline / the banner (the telegraph family stays live
  mid-crisis — never color alone), the drag ghost, selection/spawn/route
  assist surfaces, and the router LED (the alive semantic, sub-pixel). Only
  the network IDENTITY colors recede: tier bands + casings + lane stripes,
  packet bodies (+ their derived outlines/glints/trails), family washes +
  chip glyphs, router tier washes/rings, and the Dublin street blocks.
- **Reduced-motion (7.3/E9.2)**: the TRANSITION is pinned — the factor reads
  1.0 while any zone crisis is active (the static desat itself is NOT gated;
  only its ramp is motion), exactly like `pulse_read` pins PULSE16.

## Byte-identical when inert (the wire-aesthetics standard)

Zero active zone crises ⇒ factor exactly 0 and every recede is a guarded
passthrough. Proven by the full corpus: **43 demos untouched, zero `.t1` /
`.log.bin` drift** (T1 state hashes byte-identical — the change never
touches the sim), every calm frame byte-identical.

## Golden re-bless (deliberate, cause-documented)

Exactly **6 crisis-carrying T2 frames**, all the juice scene @65s with
`Saturated_Bundle` pair (10,12) triggered at tick 1281 — the capture at tick
1300 sits past the 16-tick ramp, fully engaged:

| golden | cause |
|---|---|
| `goldens/juice/65000ms.png` | non-involved network receded (43,692 px) |
| `goldens/a11y_{deutan,protan,tritan}/65000ms.png` | same frame under each CVD mode table (43,688 px) |
| `goldens/a11y_reduced/65000ms.png` | same frame, reduced-motion (43,656 px) |
| `goldens/a11y_scale/65000ms.png` | same frame at the ×1.50 UI scale (43,692 px — the demo IS the juice scene scaled; r1 W1: the row was missing) |

The calm `30000ms` frames re-saved **byte-identical** (git shows only the
65s PNGs modified). `surge`/`estate_surge` captures are inert on the current
head — no active crisis at any capture tick (verified by capture-time crisis
dump; the 08-24 real-ladder re-pin shifted those timelines — the same drift
`juice.dem` was re-pinned against). Their stale captions are logged in
deferred-work, not silently re-tuned here (that would be a T1-visible demo
change outside this render-only PR).

## Testing standard (mutation-proven)

- **palcheck section 7** (the live draw-path pin — the tie/gauge lesson: a
  predicate pin is bypassable at the call site, guard what RENDERS): renders
  the REAL `draw_world` with an active crisis (the row built via the
  engine's own `crisis_trigger`, bundles rebuilt explicitly — derived state)
  and pixel-scans: (a) a non-involved band reads the receded mix with the
  RAW tier hex ABSENT; (b) the involved zone's non-recede is pinned on the
  type-chip glyph surface (the crisis outline overdraws the named band by
  design — verified neither raw nor receded tier hex is visible there);
  (c) a non-involved rider recedes; (d) mid-ramp sits at the
  table-predicted mix (three-way: neither raw nor full); (e) reduced-motion
  pins full at the same mid-ramp tick.
- **CVD oracle**: `a11y_separation_check` gains the involved-vs-receded pair
  per pipe tier per mode (the pair is affine in sim space — separates
  wherever the tier separates from the paper).
- **Mutation legs, RED-then-GREEN**: (1) factor bypassed to 0 → all five
  section-7 checks FAIL; (2) over-broad predicate (everything involved) →
  section-7 fails; (3) the W3 amber default flip → the new palette test
  fails with the exact expected bytes.
- **Unit pins** (palette_polish_test): factor purity (inert/pool-only/
  ramp/overlap/reduced), recede byte-identity at f=0, the exact shipped
  mixes per tier, involvement predicates (incl. reversed-pair + pool rows),
  the W3 stripped-JSON route_tie default.

## Folded advisories — PR #99 r2 warnings (issue #101)

- **W3** (the real one): `palette_load`'s inline jcol default for
  `route_tie` had ZERO coverage (Perkins mutation-proven vacuous). New test
  `route_tie_inline_load_default_is_pinned` pins the loaded default
  `{186,94,232,235}` on the stripped-JSON path + the fallback palette.
- **W1**: `_pr_body_viscomm_tie.md` refreshed from the r1 values
  (`#965EE8`/264°/"≥62°") to the shipped r2 bytes (`#BA5EE8` @ 280°, 29.7°
  from `router_tier_high`); the a11y table recomputed FROM THE SHIPPED BYTES
  (the r1 numbers described the pre-shift violet) with the
  `route_tie`-vs-`pipe_steel` deutan residual (~17.4, a pair not in the
  oracle) flagged alongside its shape-encoder rationale (dashed-info vs
  solid-tier/solid-warning — never color alone).
- **W2**: the same mirror's "pre-existing, out of scope" derive-script note
  now records the r2 fix (`strip_jsonc_comments` runs on the shipped bytes).

## Verify (all green, from the worktree root)

| command | result |
|---|---|
| `odin test app` | 48/48 |
| `odin test app/render` | 100/100 (94 + 6 new; r1 table said 99 — stale) |
| `odin test core` | 261/261 |
| `tools/lint.sh` | all gates green |
| `tools/harness.sh palcheck` | all green (incl. section 7 + the CVD crisis pairs) |
| `tools/harness.sh run` | 49/49 demos green post-bless |
| `tools/ci-local.sh --native` | 13/13 gates |

## Decisions & rationale

- **Canvas-mix over gray-mix** — the board's calm register IS the warm
  paper; gray would read colder than the board. Hue families survive at
  reduced chroma, so tier identity degrades gracefully rather than
  vanishing.
- **Pool_Exhaustion recedes nothing** — map-wide flaw = the whole network is
  the zone; receding it would desaturate the packet-jam evidence. Caught
  empirically by the dublin@90s golden before it shipped wrong.
- **Snap-back on resolve (no down-ramp)** — the relief read + the
  byte-identity contract holds at every resolved capture (surge@119500ms
  stays blessed; a down-ramp would have re-blessed 3 more frames and left
  partial desat lingering in "resolved" states).
- **The pure-factor derivation (vs gauge-style fed state)** — the T2 capture
  path must render the desat from sim rows alone; app-fed display state is
  invisible to goldens by construction (the pkt_interp/gauge precedent
  inverts here deliberately).
- **Ramped engage, 16 ticks** — an instant full desat at trigger would flash
  the whole board; the ease reads as one motion ("the board goes quiet")
  while the crisis chrome (banner/outline, already at full strength) owns
  the instant. `CRISIS_FADE16` is its own table (not a reuse of the gauge
  `EASE16`) so a future gauge retune cannot shift crisis timing.
- **Rejected: desaturating warning halos on non-involved pipes** — warm =
  danger is the telegraph canon; a mid-crisis amber elsewhere on the board
  is REAL information that must stay legible (never color alone).

## Review round 1 (the 2-hunter swarm, folded)

bmad-review adversarial + edge-case lenses over the full diff, read-only,
both verifying against disk + re-running the gates. Folded:

- **BLOCKER (both hunters)**: the reduced-motion pin sat ABOVE the pool
  carve-out in `crisis_desat_factor` — a pool-only crisis under
  reduced-motion desaturated the whole map (latent in every golden: the
  reduced-mode frame is a zone crisis, the pool frame isn't
  reduced-mode). Fixed (the pin moved below the carve-out) + unit-pinned
  (`reduced motion + pool-only crisis carves no zone`).
- **WARNING**: congestion halos on non-involved bundles blended from the
  RECESDED tier color (~37% drag toward canvas) — contradicting the
  never-recede telegraph contract. Both draw branches now blend the halo
  from the raw tier color.
- **WARNING**: the involved-rider non-recede had no draw-level pin (the
  on-edge rider is outline-covered by design). `crisis_packet_involved`
  extracted (ONE resolution chain, unit-pinned end-to-end) + at-node
  doorstep rider legs in palcheck §7 (clear of the outline end-caps).
- **Accepted + pinned**: the earliest-resolve dip — when the earliest of
  overlapping zone crises resolves inside another's ramp, the pure
  rows+tick derivation re-bases (a partial-relief read; a monotone hold
  needs view state, which the capture-path contract forbids). Documented
  in the spec's Design Notes + pinned in the factor purity test.
- **Notes applied**: receded riders dim their glints (the sparkle field
  fought the desat); the CVD oracle gains the effective packet-class
  recede pairs; §7 saves/restores the shared view + premise-pins its
  geometry math; the "affine in sim space" comment reworded to the
  empirical-threshold truth.
- The 6 crisis goldens re-blessed for the halo/glint deltas (same cause
  as the primary re-bless, +2,072 px/frame on top).

## Perkins r1 fold (CHANGES_REQUESTED → this push)

- **B1 (blocker) — the Dublin block recede was mutation-vacuous.** No
  Dublin demo renders a ZONE crisis (dublin_board captures pool-only, where
  the carve-out zeroes the factor), so nothing gated the block recede.
  Fixed with a palcheck §7f leg: the §7 fixture rendered under
  `map_source=Dublin` with the zone crisis live, pixel-scanning the block
  surface — involved keeps the family fill (113 px), non-involved recedes
  (111 px), and the exact-one-side-zero shape catches every render-path
  bypass. **RED-then-GREEN**: deleting the whole block recede (or the edge
  line alone) flips the leg. The probe also surfaced two renderer facts,
  now load-bearing in the code: rlsw renders the block's triangle fill
  OPAQUE (the fill recede rides the RGB mix, not the alpha twin — the
  alpha-only first cut was inert in the goldens path), and the fill
  triangles are backface-culled for some street orientations (a
  PRE-EXISTING winding bug, deferred-work entry — the blessed dublin
  goldens carry the missing fills; fixing it is its own golden-churn job).
- **W1**: the 6th re-blessed golden row (`a11y_scale@65s`) added to the
  table above. **N1**: render-test count corrected (100, not 99).
- **W2**: the chain test destroys its Catalogs (leak noted by Perkins,
  gone). **W3**: `scan_col` guards both axes. **N6**: §7's
  reduced_motion toggle joins the save/defer set.
- **N2**: the Dublin frontage edge recede rides the RGB mix (measured:
  line/triangle alpha is unreliable in rlsw). **N7**: the desat doc block
  relocated; `draw_crisis_banner`'s doc is adjacent to its proc again.
- **N8**: the basis-switch dip pin is now genuinely two-row — and in
  fixing it, two pin bugs surfaced and died (a `pop()` that removed the
  wrong row; a `<` comparison re-derived after the fixture mutation).
- **N13**: the derivation comment names reduced_motion as a settings flag
  (harness-visible), not app-fed display state.
- No golden drift in this fold (dublin is pool-only at its captures;
  factor 0 = byte-identical passthrough — corpus 49/49, goldens clean).

Review: Perkins arms at the stable CI-green head (pr_review=1 — LOOK canon
surface). Issue #101 closes at review (closes-none here per the batch
convention).

## Canon note: bmad-build skill waiver (standing, Silas ruling 2026-08-21)

This job ran the bmad-build workflow from its plain step files (the
self-contained briefing path): `_bmad/scripts/render_skill.py` is absent in
this repo and the renderer HALTs on the ambiguous `implementation_artifacts`
config token (bmm + gds both define it — the documented upstream breakage).
The waiver is standing until the upstream dedupe lands; the workflow's
step structure (clarify → plan → implement → **review layers** → present)
was followed manually, with the mandatory step-04 review executed as the
2-hunter mega-minion swarm recorded above.

