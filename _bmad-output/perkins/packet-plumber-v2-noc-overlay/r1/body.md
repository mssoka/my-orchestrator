## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-noc-overlay · **Reviewed sha:** f963399 · **Reviewers:** 7/7 completed
**Verification:** 36/36 findings confirmed against the code — 0 discarded as false-positive

### Independent mechanical re-verification (the hard bar)
- **T1 byte-identity, overlay ON**: re-ran `overlay-check qos_contention 12000ms` — sidecar payload cmp-equal to `goldens/qos_contention.t1`. ✅
- **Golden harness**: 46/46 demos green (plain build). Zero golden churn; no `core/`, `goldens/`, or `data/*.json` files touched. ✅
- **E2E key-toggle (the D lesson)**: re-ran `tools/run-dev.sh --e2e` — `bin/noc-e2e-{on,off}.png` came out **sha256-identical to the committed captures**. Pixel-diff: 236,593 px = 233,120 in the 376×620 panel card + 3,473 px of ordinary game motion (see W8). ✅
- **T2 confinement**: overlay run vs blessed 10000 ms frame: 233,120 px in-card + 5,855 px heat tints outside — matches the PR claim exactly. ✅
- **Tests in gate**: `odin test app/render` (26) + `app/input` (5) green without the define — the 11 feed + 2 key-chain tests run in gate 2; gate 9 compiles the PP_DEBUG surfaces. ✅

### Blockers (0)
None.

### Warnings (8)
1. **Scroll clamp strands the drop-log tail** — `noc_panel_rows` undercounts the draw pass by 3 rows (hash row, ratio line, crisis pool line); `clamp(scroll, 0, total−visible)` can never reach the last rows when content exceeds the 50-row viewport — the log is the last section. *[blind·codebase·edge·acceptance·architecture]* `app/render/noc_overlay.odin:383`
2. **run-dev.sh `--stats-out` pass-through is dead** — ARGS collected but never forwarded to the app; when set, the build line gets one empty-string arg instead (`"${ARGS[@]+}"`, verified: argc=1). Documented usage cannot work. *[blind·edge·acceptance·architecture]* `tools/run-dev.sh:34,38,41`
3. **overlay-check `.t1` sidecar only byte-matches for full-length, pause-free captures** — paused wall ticks are skipped while the blessed golden hashes them (the "paused state STABLE" pin). Reproduced: `pause` demo → 1810 vs 2000 hashes; a 10000 ms partial → 200 vs 240. The PR's own proof (qos_contention, full length) is valid — the verb just needs a guard. *[edge·acceptance·architecture]* `harness/overlay.odin:85`
4. **Rejection accounting is lossy** — the latch runs only while the panel is ON (N hidden rejections collapse to ≤1 on reveal; drops catch up via events, rejections don't) and dedups on (tick, kind). *[blind·edge]* `app/main.odin:492`
5. **Out-of-roster class drop double-counts** — reason bucket **and** `drop_other` both increment, so E9+E22+other can exceed the event count and inflates the ratio. Unreachable with the current roster and pinned as the anomaly signal — but the "total" line then misreports the anomaly it surfaces. *[blind·architecture]* `app/render/noc_overlay.odin:136`
6. **`/3s` rate freezes after quiet periods** — rings roll only inside drop folding; after ≥60 dropless ticks the readout keeps the frozen pre-quiet window. Spec matrix says "rates = last 60 ticks only". *[blind]* `app/render/noc_overlay.odin:noc_feed_fold_drop`
7. **draw_panel_card forked** — spec's "SHARE, never fork" Always-constraint; the inline copy already drifted (fill α 230 vs 235, border α 60 vs 40). *[blind·acceptance]* `app/render/noc_overlay.odin:438`
8. **PR-body exactness claim overstated** — "differs by exactly the panel rect (233,120 px)": measured 3,473 px also differ outside the card (the sim advanced 120 frames between the ON/OFF captures). The proof itself reproduced byte-identically; only the wording is wrong. *[perkins]* PR body, proof 3

### Notes (11)
1. Conditional measure/draw drift: `sel_pipe` counted +4 but draws 0–4; empty-state placeholder rows uncounted; class-roster filter skipped in measure. *[blind·edge]*
2. Stale "F-key" comment at the draw gate — the toggle is D everywhere else. `app/main.odin:589` *[blind·codebase·architecture]*
3. Shipped spec artifact still says `inject Key_Press{.F}` / "F toggles the panel" in Tasks/Verification, contradicting its own D ruling. `spec-noc-overlay.md:72,109` *[blind·codebase]*
4. Drop-log stale slots: out-of-range ids render "map-wide" (the E22 label) instead of the promised "gone"; occupied renumbered slots misanchor pipe/endpoints/lane. `app/render/noc_overlay.odin:654` *[blind·edge]*
5. `Noc_Feed.crisis_last_cause` written, never read. `app/render/noc_overlay.odin:129` *[blind]*
6. Wheel scroll truncates fractional deltas — trackpads can't scroll the log. `app/main.odin:596` *[blind]*
7. `PP_NOC_E2E` truthiness: `=0` also arms the scripted drive. `app/main.odin:327` *[security]*
8. The rejection dedup latch (tick‖kind) is the feed path's only untested branch. `app/main.odin:492` *[tests]*
9. Scroll-clamp row-agreement invariant untested (PP_DEBUG-gated, unreachable by gate-2). *[tests]*
10. Rejection-kind label map (17 Edit_Error cases) untested. `app/render/noc_overlay.odin:626` *[tests]*
11. **Advisory test gate: PASS** — P0 100% (feed + key-chain pins verified in-gate), P1 ~90%, overall >80%. *[tests]*

### Reviewer agreement
Five lenses independently confirmed the scroll-clamp undercount (W1); four confirmed the run-dev pass-through (W2) and the sidecar scope (W3); three confirmed the stale F-comment (N2). All 36 findings survived code re-verification — none discarded.

**Reviewed `f963399`, head now `aae7bc9` — a fresh round will follow on the new sha.**

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
