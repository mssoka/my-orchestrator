## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-3.5-node-placement
**Reviewed sha:** 666b082
**Reviewers:** 7/7
**Verification:** 16/22 lens findings survived code re-verification (0 discarded, 0 speculative; 6 deduped into shared sources)
**Failed layers:** none
**Verdict:** READY TO MERGE

### Blockers (0)

None.

### Warnings (1)

1. **Placement release after a tray-chip arm click is judged against a stale `app.press` — arming can drop an unintended router** *(agreement: blind, codebase, security, edge, acceptance)*
   - `app/main.odin:199-225,282` — `app.press` is written ONLY in the map-press branch (`if app.placing >= 0 { app.press = ...; return }`). The chip-arm branch (215-222) sets `app.placing = tidx`, `app.drag = {}` and returns without touching `app.press`; `start_run` (148) never resets it either. On the release frame of that arming click, `else if app.placing >= 0` runs, `IsMouseButtonReleased(.LEFT)` is true, and `moved := Vector2Distance(mouse, app.press) > 6` is measured against the stale press — if a previous placement press sat within 6px of the chip (the map's bottom rows render under the tray strip at 720p), a router drops at the tile under the chip with no fresh map press. v2 has no demolish UI, so the drop is permanent for the run.
   - Not a canon violation: the drop still flows through `topology_apply_edit` → `validate_place` (junction-only, bounds, min-sep), is logged, and replays — so no validation hole, no determinism break.
   - Fix: reset `app.press` to an out-of-window sentinel when arming/cancelling (chip toggle, ESC/right-click, tier select, `start_run`), or add a `press_valid` flag so only a fresh map press enables the release-time commit.

### Notes (15)

1. `mouse_tile` truncates toward zero — clicks 1–26px into the left/top letterbox margin place at tile 0 (green ghost, in-map drop) while the right/bottom margins reject; asymmetric off-map handling. *(edge, tests)*
2. Demo `place` verb narrows `i64` parse results to `i32` with no range check — out-of-range positions wrap silently instead of failing loud. *(security, edge)*
3. `demo.places` dynamic array is never `delete`d in `run_demo`'s defer; `load_demo_replay` frees neither the array nor its clones. *(security)*
4. `lower_intents` appends kind-grouped, not time-ordered — a same-tick draw-before-place would apply the draw against the not-yet-placed node (fails loud, not silent; `place.dem` uses distinct ticks so it's safe). *(edge)*
5. `Span_Exceeds_Tier` rejection label still hardcodes "standard tier" though the tray now selects the tier. *(blind)*
6. `Unknown_Node_Type` has no `reject_label` case — falls to the generic label (unreachable from the app; test/harness-only). *(blind)*
7. `Router_Ports_Full` hint suggests "upgrade" — no upgrade command exists in v2 (prototype-only, later story). *(architecture)*
8. `PLACEMENT_MIN_SEP_TILES` hard-coded in core instead of balance.json — deviation documented in-code with a sound cat.hash rationale and an explicit deferral. *(architecture)*
9. Placement-mode authority duplicated (`App.placing` vs `Drag_State.placing`) with manual sync at 5+ sites — correct today, drift-prone for future paths. *(architecture)*
10. `tray_router_types` silently truncates a junction roster past 8 types (ODN-5 fail-fast tension; dormant with the current 1 junction type). *(codebase)*
11. Off-map validation tests exercise only the x-axis; y-bounds untested. *(tests)*
12. No junction-to-junction draw test — the two-endpoint port check (`!ports_available(sa) || !ports_available(sb)`) is never pinned with both ends as junctions. *(tests)*
13. App-layer placement input paths (tray arm/cancel, ESC/right-click, movement guard, chip swallow) have zero automated coverage — the exact seam the warning above lives in. *(tests)*
14. `place.dem` header comment says "T2 captures: 1250ms (t25)" but the directives capture at 2500ms/3000ms; both PNGs are byte-identical (settled topology — golden still correctly pins the placed router + new pipe, pixel-verified). *(tests)*
15. Advisory test gate: **PASS** — P0 100%, P1 ~95%, overall ~90%; negative controls bite (69/69 drift rejections, 10/10 demos green, 70/70 core tests).

### Verification notes (Perkins)

- Canon [5.1]: terminals never placable — `validate_place` returns `.Not_A_Junction`, tray filters junction kinds, test pins it. No director-spawned router path anywhere in the diff.
- Replay [E10] + re-bless: all 9 pre-existing `.log.bin` goldens differ from base by **exactly one byte** (char 5: version field `0x02`→`0x03`, verified via `cmp -l`); every pre-existing `.t1` manifest and T2 PNG is byte-untouched; the version-2 rejection is pinned by test; `place` replays byte-identical.
- Zero catalog changes: 0 files under `data/` in the diff; `port_capacity` (basic 4) pre-exists in `node_types.json`.
- Command bus [ODN-2]: placement flows through `topology_apply_edit` validate→apply; no bypass.
- Suites at `666b082`: `odin test core` 70/70 (9 new placement tests), `odin build app` clean, harness 10/10 demos (incl. `place`), drift-check 69/69 mutations rejected, lint gates green.

**Verdict:** READY TO MERGE — the placement port is faithful, replay-safe, and canon-clean; one genuine input-state warning (stale `app.press` on chip-arm release) and a set of polish notes, none of which block.

---

*Address findings and push — a fresh round will re-review the new head. Perkins reviews only; the implementing minion owns the fixes.*
