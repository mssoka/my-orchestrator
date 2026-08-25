## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-4.1-warning-forecast
**Reviewed sha:** `9820a55` (head unchanged at post time)
**Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests — 5 chunked waves, 35 lens runs, 0 failed layers)
**Verification:** 14/14 findings re-verified against the worktree at `9820a55`; test suites independently re-run: `odin test core` 97/97, harness 14/14 demos (incl. `warn.dem`), drift-check 97/97 rejections, lint 5/5, `odin build app` green.

**Guard verdicts (the load-bearing ones):**
- ✅ **ODN-11 re-bless cause-docs hold.** The fold is mechanical (catalog_hash + `waiting_ticks` bytes ride the T1 stream — every `.t1` shifts by construction, structure verified: zero seed/tick/demo drift in any manifest). T2 shifts are exactly the cause-documented set — verified at the blob level: boot/draw/flow/win/bundle/ecmp/place/demolish PNGs are **absent** from the diff (negative proof holds), `sla/10000ms.png` is byte-identical pre/post (relief-frame proof), and the sla/qos_contention captures that shifted are mutually consistent (shared fixture scene). One gap: qos's 1 s capture shift is real but unlisted in the per-demo cause list (W4).
- ✅ **No-flicker contract holds structurally.** `waiting_ticks` increments only on a failed forward attempt (flow.odin), clears on every successful forward / E29 drop-back / delivery; fresh spawns and healthy transits never strain. Healthy-transit test pins it; zero-traffic neutrality holds.
- ✅ **LOG_VERSION stays 3.** `waiting_ticks` rides the T1 state hash (writer-only canonical dump) — the action-log format is byte-unchanged; old-log acceptance intact (version check + reader untouched).
- ✅ **Forecast is pure.** Reads the era set-piece schedule only; emits no events, mutates nothing beyond the derived rows; `[start−lead, start+duration)` countdown pins tested.
- ✅ **Pressure reads the real E9 bound** (`lane_queue_packets × packet_bandwidth`; lone packet 17% healthy, lane at bound 100% = dropping), replicated per member pipe (untested for multi-member bundles — B1).
- ✅ **Events tags 6/7, sign+target, tag-conditional payload** — append-only, pre-4.1 event bytes unchanged (verified by reading; no dedicated byte-layout regression pin — N5).
- ✅ **Never color alone.** Ring shape + `!`/`!!` glyph + pinned pulse table — triple-redundant (though the pulse runs 16× slower than the documented rate — W1).
- ✅ **WEATHER REPORT panel draws zero pixels when empty** (early return; golden-stable).
- ✅ **Era-3 sandbox** (goal 0 / cap 0 / era 3) launchable and honest; win/lose correctly absent (4.3's).

### Blockers (1)
1. **Advisory test gate: FAIL — the warning-event ladder is half-unpinned** *(tests)* — the node strain-ladder's Red→Amber easing and Amber→None transitions have no test (only None→Amber, Amber→Red, Red→None are pinned; the pipe twin covers its full ladder), and pipe-pressure replication to member pipes of a multi-member bundle is exercised by no test or demo (all scenarios + `warn.dem` use single-member bundles). Router 75%/150% and residential 600% pins, exact 69/70/89/90/91 boundaries, and the dead-node path are also uncovered. The warning-event stream is the story's core contract; the cleared-sign semantics on the easing path must be pinned. *Fix: add the node easing + Amber→None tests, a two-pipe parallel-bundle pressure-replication test, the router/residential ladder pins, and the exact-boundary pins.*

### Warnings (6)
1. **Health-ring pulse runs 16× slower than documented** *(5 lenses: acceptance/architecture/blind/codebase/edge)* — delivered 0.078 Hz (amber, step=16) / 0.156 Hz (red, step=8) vs the 1.2/2.5 Hz pinned in the code comments and epic-4-context.md; the red-rate comment's own math (2 ticks/step = 2.5 Hz) is internally wrong. The motion encoder of the triple-redundant telegraph is effectively static (12.8 s cycle).
2. **balance.json warning lead times (600/200/400) are dead config** *(architecture/blind/edge)* — parsed, validated, folded into catalog_hash, never consumed; the spec's "the UI reads the leads from here for the telegraph" is false. The amber stage is the only operational lead.
3. **Negative lead-time JSON values wrap through `u64()` and defeat the "leads > 0" fail-fast** *(security/edge/blind/architecture)* — `u64(i32(-1))` = 2^64−1 passes the `== 0` check.
4. **A partial warnings block (missing amber keys) defaults to 0 and makes every healthy node permanently Amber** *(security/architecture)* — legal-but-bad data silently breaks the absent-when-empty contract.
5. **qos/01000ms.png shift missing from the per-demo cause list** *(7 lenses)* — the re-bless is honest (verified: E9-bound red pressure halos at tick 20), but the spec enumerates only qos's 65 s capture; the 1 s capture is unlisted.
6. **Router/residential strain-ladder pins untested** *(tests)* — only the content_host ladder is pinned; the story's own Design-Notes numbers (75%/150%/600%) have no unit test.

### Notes (7)
1. Run-HUD still instructs "deliver a packet to win" in the goal-0 sandbox where winning is impossible (4.3's) *(acceptance/codebase)*.
2. Forecast panel hardcodes "SURGE" for every set-piece row — future non-surge set-pieces mislabeled *(architecture)*.
3. Frozen spec self-contradiction: Design Notes + Verification list `lose` among pixel-identical demos while its own Boundaries cause-doc shifts lose.dem (the code follows the cause-doc) *(codebase)*.
4. `qos_first_word_after_topology` walker doesn't skip the SLA (3.4)/warnings (4.1) sections — latent misparse on any strained dump *(tests)*.
5. Tag-conditional event byte-layout has no dedicated regression pin (masked by the full re-bless) *(tests)*.
6. Smaller coverage gaps: exact 69/70/89/90/91 boundaries, dead-node-slot never-warns path, demolished-node resident packets, stuck+healthy mixture, E29 drop-back clear, forecast-purity assert, era-3 session pin *(tests)*.
7. Four re-blessed captures (sla 1 s/4 s, qos_contention 1 s/10 s) byte-identical to each other pre/post — verified positive (shared fixture scene), not a defect *(blind)*.

**Verdict:** NEEDS CHANGES — the implementation is verified-correct on every load-bearing contract (re-bless, no-flicker, LOG_VERSION 3, forecast purity, E9-bound pressure, tags 6/7, accessibility, empty panel, era-3 sandbox) with all suites green; the request is for test coverage that pins the warning-event contract's remaining branches (B1) plus the telegraph/validation/doc deltas (W1–W6).

Address findings and push — a fresh round will re-verify at the new head.
