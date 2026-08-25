## 🤖 Perkins automated review — round 2
**Job:** packet-plumber-v2-noc-overlay · **Reviewed sha:** `aae7bc9` · **Reviewers:** 7/7 completed
**Verification:** 37/38 findings confirmed against the code — 1 discarded as false-positive

### Round-1 fix audit (re-review)
- **FIXED — W1 scroll clamp:** the measure pass was rewritten (3 header rows, ratio + pool crisis rows counted, empty-state fallbacks counted, queue rows capped to match the draw's 8-row break). The drop-log tail is now reachable.
- **SUPERSEDED BY RULING — W7 draw_panel_card fork:** the readability ruling mandates the dark plate; sharing the light card would contradict it.
- **Still present (advisory):** W2 run-dev `--stats-out` dead pass-through · W3 overlay-check sidecar pause/partial divergence · W4 rejection latch gated on `overlay_on` · W5 `drop_other` double-count · W6 `/3s` freeze after quiet · W8 PR-body "exactly" wording · notes N2/N3/N5/N13/N14.

### Hard-bar verification (mechanical, this round)
- **T1 byte-identity with overlay ON:** `overlay-check qos_contention 12000ms` sidecar is **full-file cmp-equal** to `goldens/qos_contention.t1` (5086 bytes, 240/240 hashes) — the readability pass did not touch the stream.
- **Panel confinement:** e2e ON/OFF re-run differs by **exactly 233,120 px in-card** (the unchanged 376×620 plate rect) + 3,659 px of ordinary game motion outside.
- **Gates:** golden harness 46/46 · ci-local **10/10** · app/render 27/27 (incl. the new canon-ladder pin) · app/input 5/5 · core 236/236.
- **Delta scope:** no `core/`, `goldens/`, or `data/*.json` changes since r1 — view layer, captures, docs only.

### Blockers (0)
None.

### Warnings (10)
1. **Canon numbers restated as literals** — `noc_queue_rows` + the queue predicate hardcode `util_pct >= 70` and the label hardcodes `"(6)"` while the neighboring bars derive `pipe_amber_pct`/`lane_queue_packets` from the catalog (ODN-5; the pass's own ruling #4). A balance tune silently desyncs row selection from bar colors. *(blind, edge, acceptance, architecture, codebase, tests)*
2. **`noc_row_right` is dead code** — defined, never called; the ledger rule is implemented by `noc_col`. Orphaned by this diff against the file's own "zero dead code" banner. *(blind, architecture, codebase)*
3. **Type-ladder self-violation** — 22px headline numerals in 16px rows (glyph boxes overlap the next row's slot by ~6px) and off-ladder 12px text (class columns, lane letters, hash) vs the header's own "≥14px body, 10px labels" ruling. Geometry confirmed; the legibility verdict is deferred to the k3 visual re-check. *(blind)*
4. **run-dev.sh `--stats-out` pass-through still dead** (r1 W2) — `ARGS` never forwarded; the build line takes a stray empty-string arg when set. *(blind, edge, architecture, codebase)*
5. **overlay-check sidecar still diverges for paused/partial captures** (r1 W3) — paused wall ticks unhashed, truncation unguarded; the shipped full-length proof is cmp-equal (verified), the verb itself remains trap-prone. *(acceptance, blind)*
6. **Rejections while the overlay is OFF still never counted** (r1 W4) — the latch + scan are `overlay_on`-gated. *(edge)*
7. **`drop_other` still double-counts** out-of-roster class + unknown reason (r1 W5) — the "total" line can exceed the event count on the exact anomaly it surfaces. *(edge, acceptance)*
8. **`/3s` rate still freezes after quiet periods** (r1 W6) — rings roll only on drop events; no tick-driven roll at draw time. *(perkins)*
9. **PR-body e2e claim overstates** (r1 W8, evolved) — "differs by exactly the panel rect" elides 3,659 outside px; and the captures are not byte-reproducible (the drive is frame-scripted but the sim accumulator runs on wall-clock `GetFrameTime()`, so the tick landing at capture-frame N drifts run-to-run — r1's byte-identical re-run was scheduling luck). The `.t1` sidecar is the byte-proof; the PNGs are illustrative. Suggest: "the panel card rect (233,120 px) + ~3.5k px of ordinary game motion". *(perkins)*
10. **Advisory test gate: CONCERNS** — P0 100% (feed pins, key-chain, stream-neutrality gates, new `noc_level` pin), but the PP_DEBUG-gated UI surfaces (log-line resolution, rejection latch, measure/draw agreement) remain unreachable by gate-2 tests. The `noc_level` extraction pattern this diff established is the fix template. *(tests)*

### Notes (12)
- Residual measure/draw drift: `sel_pipe` counts +4 phantom rows when `pipe_slot` fails (blank scroll tail, safe direction) — the r1 −3 constant and fallback rows are fixed. *(blind, architecture, codebase, tests)*
- `main.odin:588` comment still says "F-key debug surface" (shipped toggle is D). *(4 lenses)*
- Spec artifact still says `Key_Press{.F}` / "F toggles" (lines 73, 112). *(perkins)*
- `PP_NOC_E2E=0` still arms the drive (any non-empty value). *(edge)*
- Dead crisis fields: `crisis_last_cause` written-never-read; `crisis_last_class` now rendered-never (the pass dropped `cls %d` from the Saturated_Bundle line while the test still pins it). *(blind, perkins)*
- Wheel scroll still truncates fractional deltas (trackpads do nothing). *(perkins)*
- README "release builds carry zero overlay code" vs the header's "inert ~13 KB feed struct" — say "zero overlay draw surface". *(blind)*
- The readability header's own acceptance #7 (KYLE visual-verification) has no verdict artifact — explicitly deferred to the k3 re-check per the vision caveat; not a blocker on a non-k3 round. *(blind)*
- e2e drive reports success even if captures were never written (no existence check). *(edge)*
- The e2e proof + AC3 sidecar-cmp are human-run by design — automating them (a gate 11) would lock the hard acceptance into CI. *(tests, advisory)*
- `noc_log_line` resolution (map-wide/gone/renumbered) still untested — pure-over-params, extractable like `noc_level`. *(tests)*
- Rejection dedup latch still untested. *(tests)*

### Reviewer agreement
Six lenses independently converged on the canon-restatement warning (70/6 literals); four converged on the run-dead pass-through and the F-key comment; three on the `noc_row_right` orphan. Highest-confidence items are listed first in each tier.

**Verdict: READY TO MERGE**

The readability pass is view-layer only and every hard bar survived it mechanically: T1 byte-identity with the overlay ON (full-file cmp-equal), exact plate-rect confinement (233,120 px), 46/46 goldens, 10/10 ci-local, 27/27 render tests. All findings are advisory (tooling, doc drift, consistency, gated-test coverage); nothing touches the sim, the stream, or normal-run pixels.

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
