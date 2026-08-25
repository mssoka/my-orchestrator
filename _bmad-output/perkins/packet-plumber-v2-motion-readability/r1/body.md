## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-motion-readability · **Reviewed sha:** `a57b68c` · **Reviewers:** 7/7 completed
**Verification:** 22/23 findings confirmed against the code — 1 discarded as false-positive

> ⚠️ Reviewed `a57b68c`, head now `451911b` (the v2 base moved — PR #77 network-pop merged underneath; the motion commit content is unchanged). A fresh round will follow on the new sha once findings are addressed.

**What I verified clean (the hard bar):** view-layer only — zero `core/` files touched, `LOG_VERSION` untouched, `pkt_interp` lives purely in View; identity guards cover every teleport class (spawn → no-row snap, sever drop-back + ECMP reroute → anchor-mismatch snap, delivery → skip, pause/catch-up → tick-gap snap); harness defaults `interp_alpha=1.0` everywhere so goldens are snapshot-exact by construction; reduced-motion pins echoes off with the glide staying (code-level). The measurement is honest — I regenerated both strips at the reviewed sha and they are **byte-identical** to the PR's, reproducing `21/24→10/24 holds, 30.6→11.2px` verbatim. Suite green: 46/46 demos (T1+T2+replay), `odin test app/render` 13/13. The one rejected finding claimed the PR's numbers were arithmetically impossible — they are not (the AFTER window legitimately includes the arrival glide + doorstep phase).

### Blockers (2)

1. **Sub-tick interpolation core has zero automated coverage** [tests] — `app/render/view.odin:1306`. The round's central invariant (identity-guarded snap, no ghost packets) is enforced by no gate: motion-strip is in no CI run, and T1/T2/replay all render at alpha=1.0 so the interp path never executes under test. `hud_test.odin` / `wire_path_test.odin` / `palette_polish_test.odin` prove `@(test)` in app/render is established convention with an existing CI gate. → Add `app/render/motion_test.odin`: `interp_continuous`'s four continuous kinds + every teleport snap + row-roll alpha endpoints.
2. **Advisory test gate: FAIL** [tests] — P0 (interp + identity guard) 0% automated; P1 snapshot-exact default 100%; overall ≈43%. Same fix as B1 flips this to PASS.

### Warnings (4)

3. **`measure_packet_motion.py` ZeroDivisionError on an all-holds after-dir** [blind, edge] — `:72` guards only `b_steps`; empty `a_steps` crashes. Guard both.
4. **`zip(before, after)` silently truncates on frame-count mismatch** [blind, edge] — `:64`; mismatched dirs pair positionally while the stats use full lengths. Compare lengths/names; exit 2 on mismatch.
5. **`render_strip_frame` ignores `rl.ExportImage` failure and still counts the frame** [edge] — `harness/motion_strip.odin:196`; a failed write still prints "N frame(s)" and exits 0. Every sibling verb checks the bool (goldens.odin:146, map_preview.odin:117, overlay.odin:122, wire_preview.odin:108).
6. **Reduced-motion echo-off gate is unreachable by every automated gate** [codebase, tests] — `app/render/view.odin:1349`; golden captures render at alpha=1.0 so `trail_n` is always 0 — the `!reduced_motion` branch never evaluates under test. Unit-assert the predicate or gate a motion-strip a11y_reduced interp run.

### Notes (11)

7. Lost packet track counts as a "hold" in the measurement (centroid-miss → disp 0.0) [blind] — `tools/measure_packet_motion.py:51-60`.
8. `demos/motion.dem` comment says "no arrivals" but ~10 of 24 AFTER frames are post-arrival by its own timeline [blind] — `demos/motion.dem:9-11`.
9. Trail ring shift path hardcodes capacity 3 (`trail[2]`) vs the length-generic append path [blind] — `app/render/view.odin:332`.
10. motion-strip silently ignores a 6th arg that isn't exactly `snapshot` (typo → interp mode runs) [blind, edge] — `harness/main.odin:150`.
11. `render_strip_frame`'s `cat` parameter is dead [blind] — `harness/motion_strip.odin:186`.
12. measure tool: missing dir / stray non-PNG → raw traceback [edge] — `tools/measure_packet_motion.py:25`.
13. Literal AC says "100 ms" strips, but 100 ms is tick-aligned and steps identically before/after; the 17 ms evidence substitution is correct but documented only in field notes — amend the acceptance wording [acceptance].
14. Echo ring duplicates the live packet shape geometry in a second `#partial switch` — extract a shared `draw_packet_shape` [architecture] — `app/render/view.odin:1357`.
15. `run_motion_strip` is a third hand-copied demo setup/driver orchestration (after run_demo, overlay_check) — extract shared helpers so strips can't drift off the blessed timeline [architecture, codebase] — `harness/motion_strip.odin:59-133`.
16. Prime render drops `capture_frame`'s image without `UnloadImage` (~3.5MB × ~17 primes per invocation; short-lived CLI, but every other call site unloads) [codebase] — `harness/motion_strip.odin:146`.
17. `packet_interp_prune` bound + run-start reset have no coverage (fold into B1's test) [tests] — `app/render/view.odin:186-198`.

### Reviewer agreement
Blind+Edge independently converged on the measurement-tool robustness pair (W3/W4) and the CLI arg validation (N10); Architecture+Codebase converged on the orchestration duplication (N15); Codebase+Tests converged on the unreachable reduced-motion gate (W6).

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
