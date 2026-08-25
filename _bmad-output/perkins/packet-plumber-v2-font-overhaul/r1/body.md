## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-font-overhaul · **Reviewed sha:** `47ebd0f` · **Reviewers:** 7/7 completed
**Verification:** 60/60 findings confirmed against the code — 0 discarded as false-positive (3 severity-demoted per the round's user rulings; deduped to 22)

**Mechanical guards (run on the reviewed sha):** 11/11 local CI gates green · T1/replay byte-identical (0 `.t1`/`.log.bin` touched; replay + stats streams bit-for-bit; input parity green; 48 demos) · golden drift pixel-analyzed: 152,844 px = text bands + 22,086 disclosed ink_soft swaps (14.5%) — **zero** pipe/packet/building/map-geometry drift · ⚠ merged-atlas pins pass incl. negative control · PP_DEBUG gating verified compile-out. Family/size-hierarchy/ink_soft folds treated as ruled-on — not re-litigated.

### Blockers (2)

**B1 — Fail-loud font guard is dead code; the silent raylib-default fallback is still possible** — `app/render/view.odin` (`font_from_glyphs`/`load_font_file`); guards at `app/main.odin:317` + `harness/goldens.odin:76`
Every load failure (missing TTF, unreadable bytes, empty glyph set, failed atlas) is coerced to `rl.GetFontDefault()` *before* the guards — and the default font passes `IsFontValid`, so the `os.exit(2)` refusal path can never fire. This is exactly the lens-guard bar ("the silent-fallback lie is impossible") and the PR's own claimed lesson ("a missing font asset must NEVER render silently in the raylib default"). `palcheck.odin` has no guard at all. *Fix: make the loader report failure (or detect the default) and refuse in app + harness + palcheck; pin it with a test that a missing asset actually exits.*

**B2 — PR body (and committed `_pr_body_font_overhaul.md`) carries the WRONG job's content** — the blender-silhouettes PR body, including that job's Perkins verdict and a now-false "No goldens touched" claim (this diff rewrites 111 goldens)
The merge surface would permanently record another job's body. Missing from the PR surface as a result: the hash-equal T1/replay proof (job rule 5), the re-bless cause documentation, and the before/after header evidence pointers — all of which exist in the commit message and `docs/captures/v2-font-overhaul/` and just need to be on the body. *Fix: rewrite the PR body from the commit message + captures; fix or drop the committed `_pr_body` file.*

### Warnings (5)

**W1 — noc-e2e `TakeScreenshot` moved BEFORE `EndDrawing`** — `app/main.odin:668-699`. Regresses the pinned unflushed-batch lesson (stale-frame captures on GPU builds); three comment layers now state the opposite of the code (incl. a nonexistent "EndTextureMode"). Debug-only, no golden/gate impact. *Move the block after the flush; fix the comments.*
**W2 — `glyph_probe` indexes the compacted glyph array by codepoint position** — `harness/font_check.odin:53-72`. For a font lacking U+26A0 (the exact negative case the probe exists for), `f.glyphs[95]` over-reads an unchecked multi-pointer — the ⚠ verdict prints garbage. The authoritative pin (`font_test.odin`, value-keyed) is correct. *Look up by value / `GetGlyphIndex`.*
**W3 — font-check baseline probes `assets/fonts/open_sans_regular.ttf` — deleted by this same diff** — `harness/font_check.odin:158`. The baseline leg always fails-to-load on the settled head. *Point it at a committed font or make it optional.*
**W4 — `run_demo_to_ms` added as the "shared" driver while `overlay_check` keeps its identical inline loop** — `harness/overlay.odin:83-96` vs `157-190` (+ duplicated comment block). Two copies will drift. *Rewire overlay_check onto the shared proc.*
**W5 — NOC mono pairing has zero automated coverage** — no T2 golden or gate ever draws `draw_noc_overlay`; the tabular-steadiness acceptance rests on manual captures only. *Add a PP_DEBUG-gated pin (frame hash or `MeasureTextEx` width-steadiness on `font_mono`).*

### Notes (15)

1. Specimen canvas still draws the pre-08-23 ladder (22/30/14/12 vs shipped 24/32/15/13) — `font_check.odin` `draw_specimen`.
2. Stale comments teach removed behavior: rune→byte truncation (`crisis.odin:105`), deleted `load_hud_font` (`font_check.odin`, `goldens.odin:62`), "raised to 14px" (now 15).
3. `font_merge_fallback` leaks the fallback glyph *array block* (`fg`) — one small block per font per init; image-data ownership is correct.
4. `missing[8]rune` cap silently drops fallback coverage beyond 8 gaps — make it fail loudly per the loader doctrine.
5. `palette.odin` code fallbacks still carry the old ink_soft `{92,98,106}` (JSON-unreadable path silently reverts the 7.2:1 fold).
6. Score line: goal>0 branch at 17px, twin else branch left 16px — `app/main.odin:1300`.
7. Settings row: label 15px, value chip 14px — `settings_panel.odin:131`.
8. NOC class rows mix 15px (name/SLA) with 14px counters — deliberate emphasis or partial bump, worth a call.
9. `gallery: Gallery` package-level mutable global (debug-only) — app/ precedent is proc-local; document or hang it on App.
10. `PP_SW_AUDIO` has no in-repo producer — the SW gallery app build is irreproducible from the repo; wire it into `build_raylib_sw.sh` or the gallery doc.
11. Gallery stage machine retries forever on unmet conditions — add a frame budget.
12. [Demoted per the approved high-contrast fold] ink_soft also recolors non-text surfaces (card outlines, bar tracks, chip borders, node rings) — the commit's "every diff bbox is a text band" overstates; pixel analysis confirms **no unexplained** drift. Reword the cause note.
13. Title 22→24 SemiBold vs the retained "clears the health card" no-overlap comment — captured widths fine; min-clamp width worth a spot-check.
14. `palcheck` loads fonts with no refusal check — fold into the B1 fix.
15. PP_DEBUG tooling is compile-gate-only (nothing runs gallery/font-check behaviorally in CI) — optional smoke leg.

### Reviewer agreement
Dead-guard B1: 6 lenses · noc-e2e ordering W1: 7 · wrong PR body B2: 5 · glyph_probe W2: 4 · deleted baseline W3: 4 · driver duplication W4: 4 · fg-leak N3: 4.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
