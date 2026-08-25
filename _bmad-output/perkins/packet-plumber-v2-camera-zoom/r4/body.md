## 🤖 Perkins automated review — round 4

**Job:** packet-plumber-v2-camera-zoom · **Reviewed sha:** `af26d8a` · **Reviewers:** 7/7 completed
**Verification:** 56/59 lens findings confirmed against the code — 2 discarded as false-positive, 1 kept as [unverified]

**Round turbulence (disclosed):** glm-5.3 rate-limited mid-wave (1302 burst, then a 5-hour usage cap 1308). Architecture/acceptance/edge were re-driven once each per the review contract; all three delivered. No lens pane was re-rooted or re-modeled.

### Fix audit (r3 CHANGES_REQUESTED @`9094f45` → fold commit `af26d8a`)

| prior | verdict |
|---|---|
| **B1** pan clamped at the LIVE zoom | **FIXED** — `effect_pan` converts at the live zoom (W5 intact) and clamps at `cam_zoom_to`. Both mid-ease mirrors pinned and verified to **bite**: mirror 1 (2.0→1.0): old code yields 702, new pins 468 (the fit floor); mirror 2 (1.0→2.0): old pins 832, new preserves the anchor 700. The re-captured zoomed E2E png is the mechanical manifestation. |
| **B2** release wheel dead-zone | **FIXED** — `effect_overlay` toggle is PP_DEBUG-gated (release permanently false; `noc_key_test` survives via its own recording hook); the `.Noc_Scroll` branch falls through to a zoom when compiled out (traced in both builds); when-branched build pins in the effect test; gate 9 runs `odin test app -define:PP_DEBUG=true` in **both** ci-local.sh and ci.yml — 34 app tests green in both legs. |
| **W1** vacuous router pin | **FIXED** — the seed now spawns first (id 3), the router after (id 4): the walk must skip the NEWER router; the old count walk-back fails this test. |
| **W5/W6/W7** advisory band pins | **FIXED** — wheel band [1.0,4.0] pin (+20/−20 notches), exact pan-value leg (520−100/(fit·2)=455), ease-rate band [90,150] frames (verified to discriminate: rate 0.14 would converge ~44f). |
| **W2/W3/W4** | **STILL PRESENT** (carried as warnings below). |
| **N1/N2/N3/N4/N8/N9/N10/N11/N12/N14** | **STILL PRESENT** (carried). **N5/N6/N7 FIXED** (camera_fit single-source in render; 6/6 fixture frees, no double-free; touch header reworded). **N13** accepted-documented. |
| **W8** advisory gate | **STILL CONCERNS** (P0 100%, P1 ~86% — the retarget + overlay-gate + walk-edge + start_run pins are the gaps). |

### Mechanical evidence on this head (run by me, not assumed)

- **11/11 native gates PASS** — release counts: core 236, app 34 (×3), render 61, input 12, audio 10, harness 2.
- **48/48** golden demos PASS (T1+T2+replay — zero drift). **27/27** input parity. Fast container leg (gates 1-2) PASS.
- **Both-build claim VERIFIED**: gate 9's PP_DEBUG app leg is 34 green; I additionally ran the legs the gates don't cover — render 61, input 12, core 236 all green under `-define:PP_DEBUG=true`.
- **Captures (mechanical only — k3 caveat):** the PP_CAM_E2E drive re-run at `af26d8a` reproduces the fit capture **byte-identical** (63524a77 ✓ matches the body). The zoomed capture is **not** byte-reproducible run-to-run (fresh 5b191b7e vs committed 9c1f806f, 0.21% pixel noise — sub-tick animation; no aesthetic verdict).

### Blockers (0)

—

### Warnings (6)

- **R4-W1** *(5 reviewers — still present since r3)* — the `pullback_yields` app7 leg still writes the dev's real `~/.pp-settings.bin` on every native test run (both build legs; mechanically re-proven: mtime moved, v2 file with pullback OFF). `app/pullback_test.odin:281-287` — set a temp `settings_path_override`.
- **R4-W2** *(5 reviewers — still present since r3)* — `pullback_feed` caps the spawn→id mapping at `ids[8]`; a 9+ spawn frame silently skips the pullback. Data-inert today (interval 80 vs the 5-tick frame cap) but the interval is balance data. `app/main.odin:1646-1649`.
- **R4-W3** *(3 reviewers — still present since r3)* — the same-window exclusion's correctness depends on `terminal_spawn_interval_ticks > ticks-per-frame`; nothing asserts it. `app/main.odin:1654-1655`.
- **R4-W4** *(2 reviewers — escalated evidence drift)* — the PR body's capture evidence is provably stale at `af26d8a`: the cited zoomed sha `3b28c414` matches no committed bytes (committed: `9c1f806f`), "byte-identical across the addition" is now false, the 61.4%/61.7% pixel-diff figures describe superseded bytes (mechanically ~66% now), and the r4 re-capture (the B1 clamp moved the settle) is unclaimed. `_pr_body_camera_zoom.md:135,139,148-149`.
- **R4-W5** *(3 reviewers — still present since r3, escalated)* — the body's "a second SEED mid-ease retargets it" has no test; an early-out-when-armed regression passes every gate. `app/main.odin` pullback_feed.
- **R4-W6** *(tests — [unverified] advisory)* — advisory test gate: **CONCERNS** (P0 100%, P1 ~86%, overall ~87%; the P1 gaps are the retarget pin, the overlay release no-op pin, direct walk-edge pins, and the start_run latch-reset pin).

### Notes (17)

*Still present since r3:* **N1** stale-latch guard re-synthesizes a release every frame with placement armed (3 reviewers) · **N2** `camera_pullback_target` comment contradicts its own floor pin (585→390) · **N3** pin counts still claim 4+4+4+2 vs actual 9+7+10+2 (4th generation; 4 reviewers) · **N4** `start_run` latch reset untested (3) · **N5** noc_overlay "four constants" miscount (2) · **N6** Pan executor no draw guard (3) · **N7** wheel residue pre-charge (3) · **N8** `camera_newest_terminals` no direct unit pins (3) · **N9** fixture-id comments still say id 6/7, actual 3/4 (3).

*New this round:* **N10** `camera_zoom_step` doc comment has a duplicated tail (3 reviewers) · **N11** the new pins' comments cite the wrong fixture's numbers — y-band "[195,585]" (real [234,702]), x-band "[278,762]" (real [416,1248], contradicted by the same test's own assertion), ease "~1.78/~119f" (real ~2.13/~116f), and mirror 1's drag direction is backwards (3) · **N12** the B2 root-cause gate is unpinned — no test calls `effect_overlay`, so deleting the PP_DEBUG gate passes both CI legs · **N13** the expected 4.0-band-edge e2e proof doesn't exist as an artifact (the CAM_E2E drag deliberately avoids the edge; the mid-ease mirrors do bite) · **N14** ci-local.sh still says "all 10 gates" (11 entries) · **N15** `types.odin` "PP_DEBUG builds only" is stale post-fold (mapping ungated, effect gated) · **N16** `effect_zoom`'s `#partial` forfeits exhaustiveness on the fully-cased 3-member `Wheel_Target` · **N17** `PP_CAM_E2E` env string one-shot leak.

### Reviewer agreement

The five-source agreements are the three still-present r3 warnings (W1/W2/W3 above); the stale-counts note has four. Two blind-lens findings were **rejected in verification** (the "moves buffer overflow" — an explicit `moves_n < len(moves)` guard exists at mouse.odin:134; the "deselect doesn't clear pullback" — the fall-through calls `camera_set_fit`, which clears it).

**Verdict: READY TO MERGE**

Both r3 blockers are genuinely fixed with pins that bite; the mechanical evidence (11/11 gates, 48/48 zero-drift, both-build test legs, capture reproduction) holds on this head. The six warnings are data-inert/hygiene/evidence-accuracy items that do not block merge — but W4's stale mechanical claims in the evidence section deserve a doc touch-up whenever convenient, and W1's real-HOME write should not survive another round.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
