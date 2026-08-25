## 🤖 Perkins automated review — round 4

**Job:** packet-plumber-v2-font-overhaul · **Reviewed sha:** `082effb` · **Reviewers:** 7/7 completed
**Verification:** 22/33 findings confirmed against the code (11 duplicates merged across lenses) — 0 discarded as false-positive
**Mechanical guards (run natively by Perkins on this head):** 13/13 local CI gates · core 236/236 · render 56/56 · harness 48/48 (T1+T2+replay) · plus mutation bite-tests on both new gates (below).

### Fix audit of 082effb's claims (the literal-claims bar)

- **B1 (r3) FIXED for real** — `GALLERY_MAX_RETRIES :: 600` exists, `retries` is monotonic (never reset; every wait re-arm costs a retry on its next active frame), the abort prints the stage name. ✅
- **B2 (r3) FIXED** — `audio_close_device()` in both seam branches (no-op SW / `rl.CloseAudioDevice` HW), called unconditionally at the end of `audio_destroy`. ✅
- **F3/N10 FIXED** — the SW gallery producer command is documented in `gallery.odin`'s header; the seam comment's pointer is now true. ✅ (new residual angle → W3)
- **F4 FIXED** — body names the post-#88 base + the combined re-bless cause. ✅ (new staleness → W4)
- **F9/N1, F11/N13, F14, F17, F18 FIXED** ✅ · **F10/N9 fixed in claimed scope** ✅
- **F5 PARTIAL** (→ N-residual) · **F8/N2 PARTIAL a third time** (→ W6) · **F13 PARTIAL with an overbroad claim** (→ W2)
- **F6 + F12/N15 NOT FIXED** — the fix (gate 10) is inert (→ **B1 below**)

### Blockers (1)

**B1 — Gate 10 (overlay-pixels) is vacuous: mutation-proven unable to fail on the never-draws wiring regression it was built to catch — the W5/F6+N15 fold is not real.** `harness/overlay.odin:239-252` · sources: orchestrator-mutation, tests, codebase, blind
I mutated the code in an isolated copy (removed `draw_noc_overlay` from `overlay_pixels_check` — the exact regression the gate guards) and ran the gate: **it still passes — 775 dark samples ≥ the 500 threshold, vs 5193 healthy.** The background map/forecast band alone clears the threshold, so a wiring regression that never draws stays green. Compounding: the verb skips the flip+swizzle every other readback applies (`overlay.odin:106-107`), so it samples the vertically-mirrored band (y 24–624 vs the panel's 96–696) — the region math is unproven even in the healthy path. r3's F6 warned this gap twice; the commit claims it closed ("asserting the panel rect actually paints"). Gate 11 (font-guard), by contrast, **bites properly** — I neutered the exit-2 refusal and it failed as designed. **Fix:** render the frame twice (overlay on/off), assert the *diff* inside the panel rect exceeds a floor (or assert text-band pixels specifically), apply the flip+swizzle, and re-verify with this mutation.

### Warnings (6)

- **W2** Readable-but-undecodable fallback (or merge `MemAlloc` failure) still silently ships a ⚠-less atlas — `fg == nil || ng == 0` and `merged == nil` return ok (`view.odin:1411-1421`); only the missing-*file* path fails loud. The commit's "never a silent warning-less atlas" is overbroad. [acceptance, architecture, edge]
- **W3** The `PP_SW_AUDIO` seam branch (16 stub procs) is compiled by **no automated gate** — signature drift stays green until a manual gallery build. One compile leg closes it. [tests]
- **W4** Three contradictory gate counts: `ci-local.sh` usage lines say 10, the header says 13, **the PR body says 11/11** — and the 2 new gates are local-only while the header claims step-for-step ci.yml parity. [blind, codebase]
- **W5** `ink_soft` darkening ([92,98,106]→[66,72,80]) repaints **non-text gameplay pixels** — spawn rings (`spawn_fx.odin:365`), health card border + bar track (`health.odin:45,67`) — against Rule 6's "palette/layout unchanged" letter; the body's "22,086 px ink_soft swaps" disclosure doesn't enumerate the non-text surfaces. [acceptance]
- **W6** N2 partial a **third** time: the truncation claims remain false — `font_check.odin:96-97` and `noc_overlay.odin:42` still say `draw_text_c` "truncates every rune to a byte" after this diff made it raw-UTF-8. [blind, acceptance, codebase]
- **W7** Three verbatim copies of the ~25-line demo-replay setup block beside the shared `run_demo_to_ms` this diff factored — the drift class that already bit once (the W2 comment). [architecture]

### Notes (15)

N-residual exit path (app/palcheck wrappers untested, gate local-only) · ⚠ drawn by no shipped string (the fallback pipeline guards a theoretical glyph — calibrates W2's practical harm) · font_test pins leak recs/glyphs (guard discards its atlas) · `overlay_pixels_check` never frees `LoadImageColors` · merge nil-paths leak the main glyph set · gallery header "30px" vs shipped 32px toasts · `usage()` omits `overlay-pixels` · `FONT_GLYPH_PADDING=4` misattributed as raylib's default (raylib sets 0) · health chips 15px/15px zero leading · `build_probe_set` re-implements `font_codepoints()` · contrast ratios unpinned · A/B tooling body-only swap *(since r3)* · app text surfaces golden-less *(since r3)* · advisory gate: CONCERNS · project-context "No globals" without the gallery carve-out pointer.

### Reviewer agreement

B1 vacuous gate (4 sources — incl. mechanical mutation proof) · W2 corrupt-fallback silent (3) · W6 truncation comments (3) · font-test leaks (3) · W4 stale counts (2).

**Verdict:** NEEDS CHANGES

_Non-k3 round: pixel verification mechanical only (byte/hash/capture-diff/mutation); aesthetic verdicts deferred for the k3 re-check._

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
