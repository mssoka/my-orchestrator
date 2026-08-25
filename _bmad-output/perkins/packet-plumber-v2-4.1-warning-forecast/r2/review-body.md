## 🤖 Perkins automated review — round 2 of 3

**Job:** packet-plumber-v2-4.1-warning-forecast · **Reviewed sha:** `2a972bd` · **Reviewers:** 7/7 completed (5 chunks × 7 lenses, 35/35 outputs valid, no failed layers)
**Verification:** 17/17 findings confirmed against the code — 0 discarded as false-positive. Perkins re-ran the badge-out independently: core 104 ✓, harness 14/14 ✓, drift 97/97 ✓, lint 5/5 ✓, app builds ✓.

### r1 fix audit (the CHANGES_REQUESTED set @ 9820a55)

| r1 | Fix | Status |
|---|---|---|
| **B1** (blocker — test gate) | +7 tests: node easing Red→Amber/Amber→None, two-pipe parallel-bundle replication, exact 69/70/89/90/91 boundaries + router 75/150% + residential 600% pins, dead-node silence + resident cull, stuck+healthy mixture + E29 drop-back, tag-conditional event bytes, eval purity | ✅ fixed |
| W1 (pulse 16× slow) | advance-per-tick math: amber 1 entry/tick = 1.25 Hz, red 2 = 2.5 Hz @ 20 Hz; comments corrected | ✅ fixed |
| W2 (leads dead config) | HUD legend now reads all three leads | ⚠️ see warning below — displayed, but the caption over-promises |
| W3 (negative u64 wrap) | i32 parse + `> 0` validation BEFORE the u64 cast; negative rows added | ✅ fixed |
| W4 (partial block → permanent Amber) | missing keys default −1 (load error) + amber ≥ 1; rows added | ✅ fixed |
| W5 (qos 1 s cause-list) | PR body's re-bless proof lists it | ⚠️ in PR body only — the spec's own Golden bullet still omits it (note 1) |
| W6 (router/residential pins) | covered by the boundary test | ✅ fixed |
| N1 HUD instruction · N2 SURGE hardcode · N3 lose spec contradiction · N4 dump-walker | reworded / catalog-id label with bounds guards / cause-doc added / state-parameterized with layout-verified section skip | ✅ all fixed |
| N5 smaller gaps · N6 event bytes · N7 blob consistency | boundaries/dead-node/mixture/E29/purity + byte-tail test; the relief-frame negative proof still holds at head | ✅ fixed — except N5's era-3 session-config pin sub-item (note 9) |

### Blockers (0)

### Warnings (1)

- **r1 W2 fix consumed the leads, but the HUD legend now promises reaction windows the sim does not enforce** — `app/main.odin:552-553` renders "node strain ~30s to critical · node critical ~10s · pipe ~20s to saturation" from the 600/200/400-tick config. Nothing enforces those windows: `strain_level` (core/warnings.odin:69-72) is a pure percent mapping with no time component, and warn.dem's own golden stream goes Node_Strained @1 → Node_Critical @2 — **one tick**, not ~30 s. The leads remain display-only; the caption asserts a FORGE #3 reaction window that doesn't exist. Either gate the Amber→Red escalation by the lead (real semantics) or reword the caption to honest config semantics ("warning leads (GDD targets): 30s/10s/20s").

### Notes (10)

1. **Spec's Golden bullet omits qos/01000ms.png** — the PR body's cause-list includes it (W5), but spec-4-1-warning-forecast.md:33/95 still names only the 65 s capture. Add it.
2. **node-slot scan duplication** — warnings.odin's node-load loop re-walks what core/topology.odin:89-94 `node_slot` already provides.
3. **Unused `core:fmt` import** in core/catalog_test.odin:13 (zero uses).
4. **jint i64→i32 narrowing** (core/catalog.odin:733-741): a JSON value ≥ 2^32 with a small residue wraps to a valid small positive and passes the r2 fail-fast — the W3 sibling path for positive overflow. Contrived; realistic classes are closed.
5. **N2 label-fallback bounds untested** — era 0 / era OOB / sp_index OOB paths in forecast.odin have no pin.
6. **W2 legend untested** — harness captures exclude the HUD, so the legend has no automated cover.
7. **warn T2 content pins** — the r2 re-bless (label + pulse phase) is pixel-identity-pinned only; content verified by narrative + unit pins (acceptable for PROTO).
8. **qos 65 s T2 content pin** — same gap; the re-bless cause is documented.
9. **Era-3 session constants unpinned** — APP_ERA/WIN_GOAL/LOSE_TICK_CAP (main.odin:32-34) were r1 N5's sub-item; still no automated pin despite the N5/N6 "extras" claim.
10. **Advisory test gate: PASS** — 104 core / 14 harness / 97 drift / lint 5/5; P0 100%, P1 ≥ 90%; remaining gaps are P3-level.

### Reviewer agreement

The W2-honesty warning was filed independently by the blind + acceptance lenses and re-verified by Perkins. Notes 2 and 4 are two-lens agreements (architecture+codebase, edge+security).

**Verdict:** READY TO MERGE

The r1 blocker and 5 of 6 warnings landed correctly; the remaining warning is a caption-honesty gap on the FORGE #3 surface — non-blocking, fold it into the next push or carry it as a 4.2 input. The golden discipline held: the r2 re-bless set is exactly the documented warn-3 + qos-65s, the negative proof is intact (harness 14/14 at the new pulse phases), and every r1 event/byte/replay pin is green.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
