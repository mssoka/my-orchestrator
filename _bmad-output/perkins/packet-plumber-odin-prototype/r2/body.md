## 🤖 Perkins automated review — round 2 of 3 (fix-audit)

**Job:** packet-plumber-odin-prototype · **Reviewed sha:** `ea678a8` (r1 was `0118cc0`) · **Reviewers:** 41/49 lens runs completed (7 chunks × 7 lenses; chunk-e 6/7 and chunk-f 1/7 — rate-limit + low-value binary/deletion content)
**r1 audit:** **2/2 blockers FIXED** · 7/20 warnings fixed, **13 still open** (carried) · notes mostly carried (a few fixed)
**Verification:** 16 distinct findings confirmed against the code across 136 raw — 3 rejected as false-positive (the capacity-LB "deviation", load_hud_font "dangling", and "CI never runs replay")

### The determinism spine — the ONE hard blocker — holds ✅

Re-verified empirically at `ea678a8`: **43/43** core tests, **6/6** app/run tests, **7/7** harness demos green on macOS, **surge_basics replay 3000/3000 ticks bit-for-bit** (tag-7 `Place_Router` round-trips through the replay gate), lint 4/4, app builds + 20s `--soak` clean. **CI is green on ubuntu-latest AND macos-latest** at this sha — the `-ffp-contract=off` T2 fix (c052208) is applied uniformly to all 5 rlsw modules; cross-platform pixel parity is real.

### r1 fix-audit — what landed

**Blockers (both fixed):**
- ✅ **B1** `app.bin` — untracked + `.gitignore`'d.
- ✅ **B2** UI-dead demolish — `handle_click_select` now runs on **every** left release; pipe + router demolish reachable again.

**Warnings fixed (7):** W1 T1 fingerprint (`in_breach` + `healthy_streak`, goldens re-blessed) · W6 triage labels name-resolved via `triage_map` · W7 allocator ownership (no more SIGABRT) · W8 hint UAF → `app.hint_buf[256]` · save_diff_bundle cross-allocator `UnloadImage` · W4 node-health zero-coverage (real test) · W5 queue-overflow zero-coverage (real test).

**Warnings still open (13, carried — not merge gates):** W2 WRR-floor still vacuous (`{100,1,1}` > `MAX_WEIGHT=64` silently rejected; `submit_c` now discards the error entirely) · W3 severance-reroute still can't distinguish (`_ = sev_drops_before`) · harness `save` blesses failed demos · `demolish node` `fields[2]` OOB · `crises.json` dead data · `jint` i64→i32 truncation + unknown keys · neutral-tick max drain · `pick_dst` arena allocs · `nearest_pipe` untested · grace-countdown draws static `!` · grace-reset test vacuous · `draw_and_reject.dem` header (now references the *removed* budget) · stale committed r1 review docs.

### Blockers (0)

None. The spine holds and the r1 blockers are closed.

### Warnings (6 new)

1. **Tapping a router tray chip can place a stray router on release** — the release branch has no tray hit-test, so a chip tap (press arms `placing`, release over the chip, `!moved`) submits a `Place_Router` at the chip's world tile and consumes stock. *Flagship interaction; demolish refunds it, so no soft-lock.* `app/main.odin:266-289`.
2. **Demolishing the bootstrap router refunds stock never charged** → one free `router_mid` per run. `bootstrap_map` spawns the mid without decrementing inventory; demolish does `+= 1` unconditionally. `core/run.odin:55-66` + `core/topology.odin:325`.
3. **E9 drop ladder not implemented as spec'd** — per-lane queue shed (newest-first within a lane) instead of the cross-lane BE→Standard→Express ladder; a premium packet can drop while best-effort survives. QoS otherwise works. Reframes the r1 W4 residual. `core/flow.odin:451-456`.
4. **Run bootstrap splits allocators → per-restart heap leak; `flow_init` sets `context.allocator` without restoring.** Topology maps + flow/director arrays land on the caller heap; `run_context_destroy` frees only the arena. Re-opens the W7 class the r1 fix stopped (crash gone, leak remains). `core/run.odin:77-101`, `core/flow.odin:83-84`.
5. **Hardware grants + `Ev_Stock_Arrived` have no direct assertion** — the inventory economy's only resupply is pinned solely by the opaque `surge_basics` T1 golden; `stock_arrived` isn't even in the harness event vocabulary. Flagged by the tests lens on 5 chunks. `core/run.odin:152-166`, `harness/demo_parse.odin:283`.
6. **Right-click during placement cancels placement AND cycles the hovered pipe's priority** (one click, two effects; the cycle lands in the action log). `app/main.odin:187-203`.

### Notes (clusters)

- **Budget-system remnants** (orphaned by the inventory ruling): `default_budget` + `cost_per_tile` in data, "budget" in demo/HUD/test comments, `project-context.md` + `node_types.json` still describe the removed game/budget systems. A canon refresh is owed.
- **Catalog validation (ODN-5):** negative grant/stock/tick values accepted (`u64` wrap can drive the tray negative); unknown terminal-role strings silently `.None`; `json.Object` maps iterated in core catalog load (ODN-10-letter, determinism-benign). Catalog jarr leaks still print.
- **Test hygiene:** WRR-floor + severance + grace-reset still can't distinguish their claims; action-log roundtrip covers 2-of-7 tags; hardcoded `direct := u32(2)`; `tlogf` is a silent no-op; `submit_c` swallows errors.
- **Harness tooling:** save blesses failures · demolish-node OOB · replay `bare=false` hardcoded · `check_golden` leaks `img` on mismatch branches · `write_file`/`write_log` dup · demo-name into paths unsanitized · `place_router` coord coercion · `parse_expect` within-clause tolerance · CI double `tar -xzf`.
- **Logic/design:** empty-meter can end WON (win evaluated before lose; spec-silent on precedence) · multi-hop-per-tick / 0-latency delivery depends on pipe slot order · placement (euclidean²) vs growth (manhattan) spacing metrics differ despite the "shared" E31 comment.
- **Dead code/state:** `state_dump`/`PCG32_INC`/`TICK_SECONDS`/`run_destroy`; `App.mode`/`press_valid`/`cosmetic_rng`/`autopilot_wired` write-only; `synth_sting`/`forecast_copy` ignore params; demo autopilot policy ships in `core/testkit.odin` whose header still says "NOT used by the game".
- **Supply chain:** CI downloads the Odin tarball with no checksum; raylib still a mutable tag. **Memory:** `snapshot_write` re-clones the inventory tray per frame without freeing the prior clone. **Coverage residuals:** `place_router` has no demo-grammar E2E; autopilot relay/port-reserve unasserted; catalog negative branches + snap_node E4 + triage_map untested. **T1 format:** `growth_pool` serialized without a length prefix.
- *(14 more note-level r1 items carried verbatim — see `consolidated.json#carried_forward_r1_notes`.)*

### Reviewer agreement

The grants/`Ev_Stock_Arrived` coverage gap was flagged independently by 5 lens-chunks; the allocator-split warning by 2 lenses (architecture + blind); the budget-remnant cluster by 4. Multi-source findings surfaced first above.

**Verdict:** **READY TO MERGE** — 0 blockers; both r1 blockers fixed; the determinism spine verified intact cross-platform. The 13 carried r1 warnings + 6 new warnings (2 in the inventory feature) + notes are prototype-rigor items for the next iteration, not merge gates — Odin is ruled in.

_Adress the warnings and push — I re-review automatically on the new sha. After round 3, the human takes over._

---
<sub>Round 2 fix-audit. 41/49 lens runs (chunk-e 6/7, chunk-f 1/7 — rate-limit + binary/deletion content). Head unchanged at `ea678a8` throughout. Full artifact: `_bmad-output/perkins/packet-plumber-odin-prototype/r2/consolidated.json`.</sub>
