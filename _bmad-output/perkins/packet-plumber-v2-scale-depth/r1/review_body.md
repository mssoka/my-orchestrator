## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-scale-depth · **Reviewed sha:** a257ca9 · **Reviewers:** 7/7 completed
**Verification:** 20/23 findings confirmed against the code — 3 discarded as false-positive

**Mechanical gates (re-run on the reviewed worktree):** ci-local 10/10 green · palcheck all green (a11y oracle min sim-dist 53.5–54.8; MAP_IDENTITY_PIN `d03ebf02…` observed == re-blessed) · blur gate GREEN (min pair 21.1°, saturation width 0.271) · **all T1 manifests + `.log.bin` byte-identical to `v2`** (zero non-PNG golden changes — sim truth untouched, fold-check trivially satisfied) · code surface = exactly `app/render/{map,palette,sprites,view}.odin` + `data/palette.json` (additions only) + `harness/palcheck.odin` + `tools/derive_a11y_palettes.py`; `core/` untouched. Lens-guard ratios verified in code: house 0.90 / sbiz 1.10 / host 1.15 / campus 1.40 tiles, band 15.0 px (house:band 1.44×), per-footprint shadows with fixed (2,3) offset, ink 12–18%, map water 26.0% / paper+land 53.3% measured.

### Blockers (0)

None.

### Warnings (3) — advisory coverage gaps, none block this merge

1. **Scale-ratio invariants lack a durable test** `app/render/view.odin:1388` [tests] — house:band 1–2×, wide < house, role ordering live only in PR-body numbers + re-blessable goldens; a future constants edit could silently break the MM calibration behind a legitimate-looking re-bless. → add a render unit test asserting the ratios from the live procs.
2. **Edge-water distribution measured by no committed gate** `app/render/map.odin:79` [tests] — the border ~45% / interior ~30% acceptance metric is PR-body-only; the identity pin catches generator changes but not distribution drift. → harness leg on seed 7 pinning border/interior bands.
3. **Thumbnail gate is manual-only** [tests] — hard rule 3's 427×240 check ran by hand (band 5.0 px, house 7.2 px reported); no committed tool unlike `blur_gate.py`. → commit a `thumbnail_gate.py` mirroring it.

### Notes (11)

- **Spec-artifact drift:** the internal plan doc pins narrow 4.7 / wide 11.4; code ships 4.5 / 10.5 (wide capped under the house footprint — rationale documented in PR body + code comment, but the artifact wasn't amended). `_bmad-output/implementation-artifacts/spec-v2-scale-depth.md:63`
- **Stale comment:** `tier_pipe_width` claims the ladder "keeps its 1:1.57:2.43 ratio"; shipped values are 1:1.64:2.33. `app/render/view.odin:1389` *(4 reviewers)*
- **Dead constant:** `MAP_LAND_LEVEL` referenced nowhere after the edge-bias rework (kept "as the reference base" per comment). `app/render/map.odin:69` *(3 reviewers)*
- **Park share 7.55%** vs the PR's own ~8–10% accent band (measured 69,570/921,600 px; MM 9–11%). Cosmetic miss of an approximate band. *(2 reviewers)*
- **PR-body numeric:** "paper+land 59.0%" doesn't reproduce — exact-color measurement gives 53.3% (water 26.0% and park 7.55% do reproduce). State the measurement basis or correct the number; the paper-dominant direction holds.
- **A11y oracle narrowed:** canvas pairs dropped as `land` becomes the map reference — no live regression (dropped pairs passed pre-change with unchanged colors; land+canvas hexes pinned by exact-color floors + T2). Optionally pin land-vs-canvas as a documented sub-threshold pair (~14 sRGB, by design).
- **Pre-existing:** deutan/protan a11y goldens are byte-identical to each other before and after this PR (old blobs both `fcb0e96`) — the mode goldens may not actually apply per-mode tables; out of scope, flag to the a11y/harness owner.
- **Unannotated:** unknown-tier fallback 4.5 → 6.0 (recentered with the ladder; deserves its comment line).
- **Robustness:** positional `Shadow_Spec` literals (`{0.60, 0.35, 36}`) allow silent rx/ry transposition; use named fields. `app/render/sprites.odin:190`
- **Boundary:** grid loop hangs if `v.scale == 0` — pre-existing class (old loop hung likewise on `win_h==0`), marginally widened by the `<=` bound; add an early return. `app/render/view.odin:223`
- **Advisory test gate: PASS** — deterministic-sim surface fully covered by the byte-identical T1/replay; view layer covered by 102 re-blessed T2 frames + palcheck floors + blur gate.

### Reviewer agreement
Stale ladder comment (blind+acceptance+architecture+codebase) · dead `MAP_LAND_LEVEL` (blind+architecture+codebase) · park-share band (blind+acceptance).

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
