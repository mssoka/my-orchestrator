## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)

**Job:** packet-plumber-background-maps · **Reviewed sha:** `2773dd2` · **Reviewers:** 4/7 completed
**Verification:** 5/7 findings confirmed against the code — 2 discarded as false-positive

> **Reviewer note (transparency):** 3 lenses (`edge`, `codebase`, `tests`) failed on the fallback model's 5-hour usage cap (code 1308; one retry each per headless contract). Compensated with mechanical verification: the seven r1 guards below were each pinned by an independent check, not by eye.

### The r1 contracts — all hold (mechanically verified)
- **Presentation-only `[ODN-1]`** ✅ `map.odin` imports only `vendor:raylib`, writes only `View` fields; the seed flows read-only at all 5 `draw_world` call sites; `core/` diff is empty; `palette.json` deliberately unhashed (`core/catalog.odin:984`).
- **Seeded + deterministic** ✅ the FNV pin `0xADC46DEEF414FD5A` (seed-7 cells) was **independently reproduced** by a from-scratch Python reimplementation of the generator — the pin binds every constant (non-vacuous); seed 8 → a different hash.
- **Palcheck map oracle** ✅ section 1d scans the **blessed** `goldens/juice/30000ms.png` with floor counts + margin (water>200K vs ~460K, land>150K vs ~246K, park>50K vs ~87K, coast>4K vs ~7.4K) — a removed map collapses all four.
- **Style fidelity** ✅ shipped seed-1234 render (`tools/harness.sh map-preview 1234`, rlsw) is **byte-identical** to the approved candidate B — 0/921,600 pixels differ. What shipped is exactly what was approved ("Map style verdict: pick B (seed 1234)").
- **Re-bless (76 PNGs, full T2)** ✅ `tools/ci-local.sh --mac` **10/10 green** (T1 hashes + T2 pixels + replay byte-identical); zero `.t1`/`.log.bin` diffs; fold-only spot-check: changed pixels = old cream background → water/park/coast + alpha-blend AA edges, sprite-core colors 100% byte-identical.
- **Canon folds** ✅ Story 7.4 card + the D9 decision-log entry + look-book §2/§7 are consistent with the doctrine reframe (#61).
- **No scope creep** ✅ the map is presentation-only; `harness map-preview <seed>` is harness-side only.

### Warnings (2)

1. **[blind] Stale header comment in `app/render/map.odin:41-42`.** The art-tuning block still opens "Thresholds: 0.46 → ~60% land" while the shipped constant is `MAP_LAND_LEVEL :: 0.38` (the inline note records the 0.46→0.38 retune). The tuning record in code is self-contradictory. *Fix: update the header to describe the shipped 0.38 threshold.*

2. **[architecture] `harness/map_preview.odin:71-72` — the juice fixture's QoS weights drifted.** The preview hardcodes `{9,1,0}` / `{1,1,8}`, but `demos/juice.dem:47-48` uses the `express_heavy` / `best_effort_heavy` presets which resolve to `[4,2,1]` / `[1,2,4]` (`data/balance.json`), and `{9,1,0}/{1,1,8}` appear nowhere else in the repo. The header's "lifted verbatim so the preview == the shipped golden's scene minus the map" claim is false — the preview renders a different lane emphasis than the shipped juice scene. (Map itself unaffected — fidelity stamp above is on the map.) *Fix: resolve presets by name like `harness/run.odin:83-84` does (`pp.preset_index` → `lane_presets[idx].weights`), or parse `demos/juice.dem` with a seed override.*

### Notes (3)

1. **[blind]** Re-bless cause-doc says "the map changes every frame" — the map is seed-static + cached; it's *present on* every frame, not varying. Reword to avoid implying non-determinism.
2. **[blind]** `MAP_COAST_RADIUS :: 1` but its comment says "a 2px sand band" (leftover from the abandoned radius-2). State the actual 1-px band.
3. **[architecture]** `harness/palcheck.odin` section labels are out of file order after the 7.4 insertions (`1d` before `1c`; `--- 3 ---` before `--- 2 ---`). Renumber sequentially on the next touch.

### Reviewer agreement
No multi-source findings (the four surviving lenses landed on disjoint surfaces; two cross-claims were rejected as false-positives during verification).

**Verdict:** READY TO MERGE

_0 blockers. The two warnings (a stale comment + a dev-tool fixture drift) and three notes are non-blocking — please fold them into the next PR or a quick follow-up; I re-review automatically on the new sha._
