# RECORD — Packet Shape Vocabulary · the design conversation (quinn pattern)

**Job:** packet-plumber-v2-viscomm-shape-vocab · Sally (bmad-agent-ux-designer) × Moses · 2026-08-28
**Mode:** interactive design conversation, read-only on the repo (v2 HEAD `c6d7351`), idle-await contract, pane stays open (amendment-ready)
**Question (audit finding D):** 7 of 9 packet classes lack a shape vocabulary — packets read as color/motion only; shape does not yet carry meaning. Trigger: the era-progression wave (PR #107, the Box) in Perkins review.
**Status:** **CONVERSATION CONCLUDED — the vocabulary is DEFERRED by user ruling.** No shapes adopted; nothing to implement. This record is the evidence base + ruling trail for the session that eventually builds the vocabulary.

---

## 1 · Rulings (verbatim, in order)

1. **[USER ANNOTATION 2026-08-28, lavish session 0ca4c461]** — *"what if they are all the same pill shape but different colours. the different shapes seems noisy."*
   (annotated on the Voice "A · Pill" card of the ruling menu). Opened the SILHOUETTE-COUNT FORK: S1 uniform body / S2 three temperament families / S3 nine shapes. Sally rendered all three through the real renderer (`captures/fork-sheet.png`) and answered with the measured CVD wall (appendix A).

2. **[ADOPTED 2026-08-28 user ruling — VERBATIM]** — *"i think grouping is worse then individual colours. but we can go with the existing shapes and colours for now. we shouldn't get too bugged down on that for now."*

   **Interpretation stated back (amendable — the pane stays open):**
   - **DEFER the shape vocabulary.** Existing shapes and colours stand: email = circle (slate), streaming = triangle (deep blue); the 7 gap classes keep the circle fallback. No new silhouettes are built now.
   - **S2 (three temperament families) is REJECTED as an organizing principle** — "grouping is worse than individual colours": when the vocabulary is eventually built, per-class individual identity (colours and/or shapes) is the preferred direction. This also disfavours the grouped-family reading of the roster; the individual per-class menu remains the honest shape of that future decision.
   - **"not too bugged down for now"** — the deferral is deliberate de-scoping, not a rejection of the evidence. The measured wall (appendix A) and the candidate geometry (appendix B) are preserved for the session that picks this up.

3. **[ADOPTED 2026-08-28 user ruling — PROCESS RESET 2026-08-26, carried]** — the canon art-direction §5.1 roster shapes were treated as EVIDENCE, not decisions; nothing in this conversation was decided without Moses. (No per-class A/B rulings were requested; the menu is superseded by the deferral.)

**Consequence check (why the deferral is safe):** PR #107's era progression lands with **no new packet classes** — the era rosters at HEAD are `foundations={email}`, `email_web={email}`, `streaming_surge={email,streaming}` (data/eras.json). Both live classes already carry their shipped shapes. The 7 gap classes are era-4+ content; nothing ships unshaped.

**Recommended re-trigger (for the successor session):** the first story wave that actually introduces a **third packet class** (first era-4 content: gaming/banking/voice) re-opens the vocabulary with this record as its spec input. The original trigger (era-progression wave) fired before any class actually landed — noted for trigger calibration.

---

## 2 · What stands (the whole spec, given the deferral)

| Class | Era | Shape (unchanged) | Colour (unchanged) | Renderer path |
|---|---|---|---|---|
| Email | 1 | circle | slate `#5A6270` | `draw_packet_shape` .Circle |
| Streaming | 3 | triangle (apex up) | deep blue `#1E4A98` | `draw_packet_shape` .Triangle |
| 7 gap classes | 4–6 | **circle fallback** (unchanged; `#partial switch` default) | n/a (not in catalog) | fallback arm |

No code change, no golden re-bless, no catalog edit. The audit finding D remains factually open (7 of 9 unshaped) — deferred, not resolved.

---

## 3 · Parked forks (explicitly fenced out of the successor's scope unless re-ruled)

- **S1 uniform body** (the same-pill proposal) — parked, not rejected; Moses's later comparison ("grouping is worse than individual colours") ranks individual identity above grouping but does not re-adopt S1.
- **S2 three temperament families** — REJECTED as an organizing principle (ruling 2).
- **S3 nine-shape roster build** — parked with the deferral; the canon §5.1 roster shapes remain evidence-only.
- **Per-class A/B menu rulings** (web/gaming/banking/voice/multicast/iot/ai candidates) — superseded by the deferral; the candidate cards + rationale below survive as reference material for the future session.
- **Fork 8 class colour system** (5 CVD anchors × lightness bands) — separate lane, still open, unaffected.
- Size grammar (canon size=bandwidth), icon channel ([LATER]), per-shape glint offsets, AI blob morph motion — open calibration questions, untouched.

---

## 4 · Evidence base (preserved for the successor session)

All artifacts under `_bmad-output/implementation-artifacts/packet-plumber-v2-shape-vocab-2026-08-28/`:

- **`captures/vocab-sheet.png`** — 9 classes × 2–3 candidates × 3 LOOK-SPEC zoom rungs (CORE r≈9.7 / DISTRIBUTION 13.6 / ACCESS 19.4 px) + single-file rider strips, rendered through the real render package (rlsw) at v2 HEAD. **Pixel-verified: all 42 candidate×rung cells populated** (PIL, per-class colour counts); vision screened, measurement decided.
- **`captures/fork-sheet.png`** — the silhouette-count fork strip (S1 nine pills / S2 three families / S3 nine shapes) at DISTRIBUTION size.
- **`page/shape-vocab-menu.html`** — the lavish ruling menu (session `0ca4c4611859c357`), with per-class candidate cards (affordance rationale + look-fit), the constraint audit, and the fork section carrying the verbatim annotation.
- **`vocab-capture/`** — the scratch capture tool (READ-ONLY; built against repo `core` + `app/render`; run from repo root). Pinned vertex tables for the canon shapes that don't render yet: RSQ12 (rounded square), HEX6 (flat-top hexagon), PILL16 (stadium), STAR10, BLOB16 — §10.4-clean, plus the prior session's draw_shape_ext (diamond/square/octagon/ring/chevron/tridot/gear) carried verbatim.
- Per-class crops under `page/crops/`.

### A · The measured CVD wall (why "just use colours" thins out)

Instruments: the repo's own Machado 2009 severity-1.0 simulator (`tools/derive_a11y_palettes.py`) + the palcheck signal gate (pairwise distance ≥ 48).

- **Canon §5.1 roster, as committed:** 4 of 108 mode-pairs fail the gate — gaming↔iot **12.1** (tritan; same colour to a tritan player), banking↔multicast **32.7** (deutan), gaming↔ai **44.5** (deutan), banking↔multicast **46.4** (protan).
- **Search, pure geometry** (distance only): 9 well-separated colours exist — best worst-pair ~77.
- **Search under the game's colour law** (also clear of reserved warm-danger amber/red, pipe-tier copper/steel/gold, ink, canvas): candidate pool 6000→896; best 9-colour worst-pair ~**50 against a gate of 48** — zero margin. The full prior-session search (aesthetic bands included) capped at **~5 anchors** — hence "5 CVD anchors × lightness bands" (Fork 8).
- **Precise form of the claim:** nine-way colour is not arithmetically impossible; it is **impossible to carry with margin under the game's whole colour law**. Identity riding colour alone (S1) sits on the thinnest axis; any silhouette axis (3 families or 9 shapes) is vision-independent and removes the load.

### B · Candidate geometry (reference; nothing adopted)

The candidate set per class (canon §5.1 A-options + prior-session B-options), with pinned tables, affordance rationale, and rung verification, lives on the lavish page (§3, per-class cards). Summary of the A-side (canon): web=rounded_square, gaming=diamond, banking=hexagon, voice=pill, multicast=star, iot=tiny_square (0.72×), ai=blob — each verified at all three rungs. Constraint notes that survive the deferral: voice-ring collides with the telegraph-ring family; hexagon≈octagon twins at CORE; tridot faint but countable at CORE; web-B(diamond) exclusive with gaming-A(diamond).

### C · Craft notes for future scratch renders (new findings this session)

- **rlsw winding cull:** `DrawTriangle` fans with positive cross-product (CCW-math vertex order, y-down screen) are silently culled — reverse fan order (v[j], v[i], center). The prior session's blank `shape-sheet.png` on disk (0 non-canvas pixels, verified) is consistent with this class of failure.
- **rlsw readback:** framebuffer is bottom-up **BGRA** — normalize exactly as the T2 goldens spine does: `ImageFlipVertical` + R/B swizzle (port of `harness/goldens.odin` `swizzle_rb`).
- The bundled HUD font lacks `—`/`·` glyph coverage in draw_text paths (renders `?`) — evidence sheets should use ASCII or the page carries the typography.

---

## 5 · Session trail

- 2026-08-28 ~14:0xZ — Phase 1 evidence closed (inventory + renderer verification + constraint audit); Phase 2 menu served (lavish `0ca4c4611859c357`, notification shown:true).
- 2026-08-28 ~14:1xZ — user annotation collected (poll); fork rendered + served (notification shown:true).
- 2026-08-28 ~14:3xZ — CVD measurement run in-pane (canon roster failures + margin-collapse searches); page updated to the precise claim.
- 2026-08-28 — **ruling: DEFER** (verbatim in §1). Record closed; pane open (amendment-ready). Ledger transitions: Silas. No PR (design conversation, pr_review=0).
