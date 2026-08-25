## 🤖 Perkins automated review — round 5
**Job:** packet-plumber-v2-font-overhaul · **Reviewed sha:** 3e62101 · **Reviewers:** 6/7 completed (codebase lens 429-failed twice — degraded; findings exist, so the degraded guard does not bar a verdict)
**Verification:** 17/17 lens findings confirmed against the code — 0 discarded as false-positive

**Fix audit (r4 → this head):** the round's headline fixes are REAL.
- **B1 FIXED, mutation-proven on this head by Perkins:** gate 10 is now a genuine dual-render diff (overlay OFF vs ON through the shared normalized frame proc — flip + BGRA→RGBA applied). Mutation re-run: `draw_noc_overlay` removed → **0 changed pixels → gate FAILS (exit 1)**; healthy path → **54,000 changed pixels → OK**. The verb bites exactly on the never-draws wiring regression it was built for.
- **W2 fixed:** readable-but-undecodable fallback, `MemAlloc` failure, and post-merge completeness gap all fail loud now (residual leak notes below).
- **W5 fixed — verified text-only:** every text draw site uses `ink_soft_text`; shapes (spawn rings, card borders, bar tracks, chip hairlines) keep pre-fold `ink_soft` [92,98,106], pinned byte-exact; the 7.2:1 ruling rides a real WCAG contrast-ratio test (rel-luminance math, text ≥7:1, shape lighter) — passed natively. T1/replay byte-identical; goldens re-blessed.
- **W3 verified:** gate 10's script compiles the `PP_SW_AUDIO` app build (`set -euo pipefail` + green run proves it). **W6 fixed** (zero truncation-claim comments remain). **W7 fixed** (`demo_replay_setup` shared by all three verbs).
- **Mechanical guards, run natively by Perkins on this head:** 13/13 gates · 236/236 core · 57/57 render · 48/48 harness · T1+replay byte-identical. Vision caveat (non-k3): pixel checks mechanical only; aesthetic calls deferred to the k3 re-check.

### Blockers (0)
None.

### Warnings (5)
1. **Sub-floor sizes vs the body's own claim** — `node_health.odin:107` trace at 12px and `main.odin:655` "P/Space to resume" at 13px sit under the Sizes row's "14px floor" (only NOC 12px labels are a disclosed exception). Raise to 14 or amend the row.
2. **gallery_arm still quietly captures with the baseline font on a failed candidate load** (`gallery.odin:101-108`, stderr-only) — contradicting the body's "The gallery's quiet-fallback lie is impossible now." The fail-loud lives in the shipped loader; the gallery tool that produced the original incident still continues. Exit non-zero or tag the captures "baseline".
3. **"Gate counts consistent (13 everywhere)" is false** — `ci-local.sh` header line 6 and usage line 31 still say "10 gates" (fourth generation of this drift). Derive all sites from `${#GATES[@]}`.
4. **NOC brightened tokens (NOC_TXT_DIM/NOC_LABEL/NOC_LABEL_DIM) unpinned** — the landed contrast pin covers `ink_soft_text` only; the NOC overlay is PP_DEBUG-gated and invisible to goldens. Extend the pin to the NOC tokens vs the dark plate.
5. **The ⚠ fallback story is theoretical end-to-end** — no shipped string draws U+26A0 (r4 F9) and no automated test draws a non-ASCII glyph through the merged-atlas draw path (only the manual font-check specimen does). One rlsw pixel probe would close the AC mechanically.

### Notes (15)
Merge-path error-return leaks (the two old paths + the new completeness return free nothing/partial — "leaks closed" claim is overbroad; callers exit, so impact nil) · font_test teardown still leaks glyph arrays/recs/bitmaps (only the guard atlas was freed) · PR body says "render suite 56/56 (incl. the 4 font pins)" — actual 57/57 + 5 pins · `overlay_pixels_frame` re-inlines the swizzle instead of calling `swizzle_rb` (same file already calls it) · NOC 12px label vs rule at y+13 (1px clearance; uppercase so cosmetic — k3 to confirm) · font_check "same recipe as load_font_file" comment (it's plain `LoadFontEx`, no merge/4px padding) · header SemiBold weight unpinned · merge secondary branches untested · SW-audio app build compiled-but-never-run · **advisory test gate: PASS** (upgraded from r4 CONCERNS) · carry-forwards unchanged from r4: exit-path gate local-only, 15px/15px chip leading, A/B body-only swap, app-surface pixel tests, project-context globals pointer.

### Reviewer agreement
Merge-path leaks (blind+edge) · font_test teardown (blind+edge) — both note-class.

**Verdict:** READY TO MERGE

The r4 blocker is genuinely dead (mutation-proven on this head), every mechanical guard is green natively, and the residual set is doc/claim accuracy + debug-tooling coverage — nothing functional on the shipped path. Merge-order LAST still applies (golden storm; final re-bless on the settled head with Silas).

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
