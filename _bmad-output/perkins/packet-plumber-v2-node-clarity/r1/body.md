## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-node-clarity · **Reviewed sha:** c133048 · **Reviewers:** 7/7 completed
**Verification:** 19/19 findings confirmed against the code — 0 discarded as false-positive

Orchestrator's mechanical spot-checks: blur gate independently reproduced **GREEN** (min pair 22.6°, band 0.289, exit 0); additions-only tokens verified (7 new keys, zero edits to existing values); token-key collision with #77 checked — **none**; `router_tier_scale` untouched (comments only); washed palcheck pins recomputed by formula (α=184/255, u8 truncation) — all match.

### Blockers (0)
None.

### Warnings (5)
1. **Tier basic/high hue pairs unguarded — basic sits ~7° from the host family** [acceptance, tests] — the gate samples only `router_mid` and the token test pins 5 anchors; `router_tier_basic` (214.3°) vs `host_family` (207.3°) = **7.0°** at token level (basic wash over the puck body lands ~213°, 5.6° from the drawn host signature 210.3°). "All 10 pairs ≥15°" is true for the gate's 5 types; the basic-router↔host pair is unmeasured and likely under the bar (shape/ring/size carry it per E9.1). Fix: add basic/high (+ a host) to the gate capture or the token anchors, or pin ring+size as the accepted separator for tiers.
2. **D7's "clean merge in either order" is false as written** [acceptance] — token keys don't collide with #77 (verified: #77 adds `lane_*`/`packet_*` keys only), but both PRs replace the identical `_comment` line with different text → textual conflict in `data/palette.json` either order. Trivial to resolve (concatenate the appendages) — rebase whichever lands second and soften the D7 wording.
3. **Blur gate + sat-band criterion have no automated guard** [tests] — ci-local's 10 gates don't run `tools/blur_gate.py`, and the token test deliberately excludes saturation. A future token tune + deliberate T2 re-bless could regress the band silently. Fix: wire `python3 tools/blur_gate.py` into ci-local (PIL present; runs green here in <1s).
4. **Advisory test gate: CONCERNS** [tests] — P0 100% (gate reproduced GREEN; washes/chips/rings palcheck-pinned; tokens unit-pinned), P1 ~85% (tier basic/high pairs + sat band unguarded), overall >90%.
5. **blur_gate.py setup errors masquerade as gate red** [edge] — an out-of-frame sample (wrong-size image, changed view fit) raises unhandled → exit 1, indistinguishable from a measured failure despite the documented exit-2 contract. Fix: guard `getpixel` / assert 1280×720, exit 2.

### Notes (12)
1. Unused `v: ^View` parameter on `draw_family_wash`/`draw_family_wash_disc` [blind]
2. Wash alignment implicit — `sprite_index_puck`/`sprite_puck_target` computed twice per router; `sprite_blit` vs `sprite_blit_dst` drift would be silent [blind, architecture]
3. `tools/__pycache__` .pyc deletion not listed in the PR body's Files section [blind]
4. palcheck LED floor halved >10 → >5 without a stated count (measured here: exactly 10 washed-LED px in the calm golden — the floor is honest at measurement; state the number) [blind]
5. PR body says "4% inset"; the disc wash uses a 6% radius inset (0.94) [blind]
6. blur_gate: `--sigma`/`--out` with a missing value silently ignored; unknown args accepted [edge]
7. `draw_type_chip` lacks the `fam.a==0` guard its sibling washes have — a `.None`-role terminal would draw an empty paper chip [edge]
8. palcheck LED/hardware pins bake the pre-POP `router_led` composite — #77's LED change ([46,139,87]→[0,205,90]) breaks them at wave merge until the documented reconciliation re-pins [acceptance]
9. "Reuse the tray icons" overstated — the tray identifies by text labels; the chips invent a new (reasonable) glyph language [acceptance]
10. blur_gate hardcodes a Python mirror of the Odin view fit — no cross-check if the fit changes [architecture]
11. wash+chip epilogue duplicated at all three `draw_building` fallback exits [architecture]
12. No pin asserts chips are SUPPRESSED under health rings (D5) — only presence pins exist [tests]

### Reviewer agreement
- **Tier basic/high hue-coverage gap** — acceptance + tests independently (Warning 1)
- **Wash/blit duplicated-geometry coupling** — blind + architecture independently (Note 2)

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
