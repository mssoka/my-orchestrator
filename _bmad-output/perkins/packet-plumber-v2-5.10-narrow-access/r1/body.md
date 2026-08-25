## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)

**Job:** packet-plumber-v2-5.10-narrow-access · **Reviewed sha:** `421a1a3` · **Reviewers:** 7/7 completed
**Verification:** 20/23 findings confirmed against the code — 3 discarded as false-positive

**The contracts — verified directly (the card's pinned acceptances as acceptance audit):**

- **The value + the math ✅** — `narrow.capacity_units` 5 → **10** in `data/pipe_tiers.json` `[ODN-5]`, the ONLY data change; playtest-tunable stays true. Headroom re-verified from live catalogs: cap = 500‰ × residential 5 u/s = **2.5 u/s**; post = 10/2.5 = **4.0×** (4000‰ — the top of the card's ~3–4× band, and the GDD M1 aspirational narrow 10 reconciles); pre = 5/2.5 = **2.0×**. Transit: ceil(30/10) = 3 ticks/hop → 2-hop = 300 ms ≤ email's 500 ms (the W5 guard the rebalance lifts; pre-5.10 narrow = 600 ms).
- **The untouched list ✅ verified by diff** — routing-cost ladder 20/10/5 unchanged; spans 8/10 + 10/14 + 14/18 unchanged (`span_exceeds_tier` contract untouched); `cost_per_tile` 5/12/30 unchanged; standard 15 + wide 40 unchanged; the 2026-08-13 capacity-cost ruling stands. `core/flow.odin` is **comment-only**. No view/UI files, no node_types/demand.json (no 5.11/5.12 creep), `serialize.odin` untouched → correctly **no LOG_VERSION bump** (no new commands). Scope guard honored: the narrow capacity value only.
- **The honest-signal pins ✅ bite (non-vacuous)** — W10 re-pinned to NARROW legs: zero drops at the access lane, no E9 shed, avg ≤ 500 ms, `delivered > 0`, `per_term >= 40` — under narrow 5 this fixture fails on transit (600 ms > 500), so the pin genuinely distinguishes pre/post. The NEW `test_w11_aggregation_congests_shared_link` asserts zero narrow-bundle drops + drops > 0 + both classes deliver + `!replay_error` — the zero-access-drop half (the honest 4.1 signal proper) is pinned and live. One under-pinned half → warning 1 below.
- **Replay + the deliberate re-bless (4.3) ✅ byte-verified by me, independently** — all **31 `.log.bin` differ from base ONLY at bytes 17..24** (the 8-byte `catalog_hash` field: `7dbddfc189670ba0 → 66c4324a06058860`) — action logs behaviorally identical; all **33 `.t1`** changed only the catalog_hash line + per-tick hashes (counts == the ticks header — the fold cascades through every state hash); **boot's era-0 splice proof reproduced from scratch** (re-ran tick 1 under the new catalogs: FNV = `6c24e9cec592aece` = the new golden; old-hash spliced at bytes 33..40 → `c4ad25131a858304` = the OLD golden exactly — fold-only, byte-proven); **T2 partition exact**: 15 frames, all in the 6 narrow-pipe demos (`ecmp_cost` ×2, `forecast_shift` ×2, `forecast_preview` ×4, `health_lose` ×3, `pause` ×2, `surge` ×2), every other demo's frames byte-identical; re-pin ripples (crisis first-shed 0→2, health windows, sla comments) cause-documented.
- **Local suite ✅ independently re-run at the reviewed sha: 9/9 gates green** (GitHub Actions billing-block + incident is not a signal, per dispatch) — incl. gate 4 (golden T1+T2+**replay gate [E10]**) and gate 2's 192 core tests carrying the new pins.
- **7.1 lane ✅** — the lane note is in your PR body; no finding below requires further T2 churn (all fixes are test asserts/comments).

### Blockers (0)

None. The value + math, the untouched list, both honest-signal pins, and the re-bless cause chain all check out — the r1 hard gates hold.

### Warnings (3)

1. **W11 never pins the shed to the shared uplink bundle** [blind, edge, acceptance, tests — **4 of 7 lenses, the top agreement signal**] — `core/demand_test.odin` (`test_w11_aggregation_congests_shared_link`, asserts ~700): `drops > 0` is global and only the 12 narrow bundles are excluded, so a drop set landing on the **host's wide drop (pipe 12)** would pass the test. The card's req 3 is "the **shared link** (not the access drop) congests"; your PR body measures 293/293 at the shared bundle — pin it: resolve `bundle_of_pipe(&s, 13)` after the run and assert `by_bundle[shared] > 0` (or `== drops`).
2. **Crisis settled-scan header narrates the OLD (a)-vs-(b) staging** [codebase] — `core/crisis_test.odin:462-467` still says "trigger tick is STREAMING-DROP-FREE and the first streaming shed (a few ticks later) is on bundle 1", contradicting the 5.10 re-pin it sits above (first shed bundle **2** at tick **25**, before the 1200 trigger; (b) would name 2). The in-body 5.10 comment is authoritative; refresh the header to match.
3. **E16 max-not-sum header cites the pre-5.10 overlap band** [codebase] — `core/health_test.odin:428-430`: "band [~145, ~204] … the ~204 death" vs the 5.10 re-pin numbers in the same test ([~407, ~457], death ~457). One-paragraph header refresh.

### Notes (8)

1. **`core/catalog.odin:190` "~2× access headroom" is now 4×** [architecture, codebase] — pre-existing line made stale by this change (the "half its 5 u/s" half is still right).
2. **`core/routing_cost_test.odin:233/291/295` "(5+40)" prose + the expectf failure message** [architecture, codebase] — the assertion live-reads the catalog (passes at 10+40=50); the prose is stale.
3. **`demos/ecmp_cost.dem:26` "narrow (5) = 6 ticks/edge"** [codebase] — now 3 ticks/edge (the goldens were re-blessed under the new transit; the narrated math lags).
4. **`demos/audio.dem:14` "serializes deliveries ~1 per 6 ticks"** [codebase] — now ~1 per 3.
5. **`health_catalog_fast_grace`'s 380 is dead** [architecture, codebase] — its only caller (the E16 test) overrides to 200 before any step; set the helper to 200 (and fix its doc) or drop the inline override.
6. **W11 port-budget comment undersells rb** [architecture] — "6 res + uplink = 7 ≤ 8 per side" is ra only; rb = 6 + host wide + uplink = **8/8 exactly** (no spare — a future rb leg would be rejected).
7. **Health re-pin "tick 411" annotations off by one** [blind] — `240+170` lands at tick 410 (the pre-pin twin `230+180` said "tick 410"; the sibling comments use plain sums). Two spots.
8. **Advisory test gate: PASS** [tests] — P0 behaviors all carry direct pins incl. non-vacuity guards; the W11 location pin (warning 1) is the last P1 gap.

### Reviewer agreement

The W11 location gap (warning 1) drew **4 of 7 lenses independently** — the highest-confidence signal this round, and a one-line fix. The catalog.odin headroom prose, the routing_cost_test prose, and the dead 380 each drew 2 lenses.

**Verdict:** READY TO MERGE

The contracts hold — the warnings are polish (one test-assert hardening + a doc-narrative sweep of pre-5.10 numbers), none block. Address them in a follow-up commit at your discretion; they do not require another round.

_Address findings and push — I re-review automatically on the new sha._
