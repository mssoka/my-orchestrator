## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-5.6-router-tiers · **Reviewed sha:** 4d637e7 · **Reviewers:** 7/7 lenses × 11 chunks = 77/77 completed (big-diff policy: 27,226-line canonical diff split into 1 code chunk + 10 golden chunks)
**Verification:** 30/44 lens findings survived code re-verification — 14 discarded as false-positive (chunk-slice artifacts + pre-existing patterns). All findings mechanically re-verified against the worktree at the reviewed sha.

### Lens-guard checks (load-bearing) — all PASS

- **Kind-split placement separation** ✓ — `placement_valid` (core/topology.odin:329-348) splits by node kind: router↔router `router_router_sep_tiles`, router↔terminal `router_terminal_sep_tiles`; terminals never block beyond the snap floor. **Data-driven** from balance.json `placement` block (fail-fast `jint_strict`, ≥1, snap-floor invariant), NOT hardcoded.
- **`PLACEMENT_MIN_SEP_TILES` actually removed** ✓ — grep-verified: only historical mentions in comments; no residual blanket-separation path.
- **Tier correctness** ✓ — mid=8/high=16 in node_types.json; `ports_available` reads `port_capacity`; the tray's generic `tray_router_types` + chip-click arms the correct `type_idx` into `Cmd_Place_Router` (verified by reading app/main.odin:394-399,513); demos place mid/high through the same command path and replay byte-identically.
- **No LOG_VERSION bump** ✓ — stays 3; no new command kinds (verified serialize.odin).
- **Golden discipline** ✓ — mechanically proven (byte-level, like the A splice proof): all 22 `.log.bin` diffs = exactly 8 bytes at offset 17-24 (the hash field); all 22 `.t1` = catalog_hash + tick lines ONLY (every tick shifted, zero non-hash lines changed); **zero T2 pixel drift on old captures** (no old PNGs in the diff); 4 new captures are new files (router_ceiling, router_tiers × 02500/03500ms).
- **No economy** ✓ — absent, as expected (tiers free; upgrade deferred to 8.6).
- **Scope** ✓ — tiers + placement-separation only; 5.5 demolish surface, routing/crisis, HUD, canon docs untouched.
- **Local ground truth** ✓ (CI is account-billing-blocked): `odin test core` 157/157; `harness run` 24/24 demos; `drift-check` 167/167 rejected; `preview-check` 7/7; `lint.sh` all gates green.

### Blockers (0)

### Warnings (4)

- **W1 — test geometry (blind):** `test_mid_high_port_ceilings` spawns the 9th house of the high-router loop on the router's own tile (i=8 → {20,26}; core/placement_test.odin:300-303) — zero-span pipe, two live nodes on one tile, contradicting the test's own "max span 16" comment. The 17th-pipe `.Router_Ports_Full` assertion is unaffected. *Fix: offset the router or stagger the row, correct the comment.*
- **W2 — tray arming unpinned (tests ×4 chunks):** chip → `type_idx` → `Cmd_Place_Router` is generic and reads correct, but zero automated coverage — demos place by name, app/ has no tests. A chip arming the wrong tier would ship silently (the lens-guard defect class). *Fix: pure-proc unit test for the chip-index→type_idx mapping, or a harness tray-click scenario.*
- **W3 — placement ghost untested (tests):** `draw_place_ghost` tier-scaling (view.odin:650-658) never exercises — every harness capture renders with `drag={}`. *Fix: pin `router_tier_scale` 1.0/1.15/1.30 in a unit test.*
- **W4 — Advisory test gate: CONCERNS (tests):** P0 100% (separation boundaries, terminal floor, tier ceilings 9th/17th, placement, replay E10, catalog fail-fast rows — all unit-pinned + 4 new T2s); P1 ~80% (W2+W3 gaps). Overall ≥80%.

### Notes (8)

- **N1 — outer-ring comment drift (blind, acceptance, architecture, codebase):** view.odin:473-481 comment claims 180°/alternating single-LED geometry; code uses `(i*stride+4)%16` = 90° with both rings fully populated. The rendered double ring satisfies A3; only the comment is wrong. Fix the comment.
- **N2 — ceiling-reject T2 substitution (acceptance, tests):** the briefing asked for T2 of the ceiling reject; delivered T2 pins the full-ceiling state (a rejected command cannot ride a demo action log — replay_error). Disclosed in PR body + demo comment; reject pinned by unit test. No action.
- **N3 — ladder gate justification (architecture):** core pins the canon 4/8/16 junction ladder with a render-geometry justification (catalog.odin:364-368). Canon-correct gate; consider leading the comment with M3/ODN-5 instead of the LED ring.
- **N4 — lenient `jint` for `port_capacity` (codebase):** the new ladder gate validates a jint-truncated value (8.9 → 8 passes) while the placement seps use `jint_strict` (catalog.odin:346,366). Align with the integer-only bar.
- **N5 — i32 multiply in snap-floor check (edge, security):** catalog.odin:801 `sep * tile_px` can wrap on extreme tunables (fail-safe direction dominates; accept-side bypass needs a ~65k-px tile). One i64 cast matches the PR's own topology.odin convention.
- **N6 — `max(1,sep)` clamp untested (tests):** topology.odin:336-339 zero-value `Balance{}` branch has no pin.
- **N7 — `draw_nodes` bounds guard untested (tests):** view.odin:319-323 defensive `continue` has zero coverage. Documented defensive code; acceptable.
- **N8 — tunables pinned against embedded mirrors (tests):** unit tests mirror 4/2 rather than loading data/balance.json (determinism_test.odin:48); the harness catalog-hash gate catches a retune, so this is a unit-level blind spot only.

### Reviewer agreement

- **N1** — 4 independent lenses (blind, acceptance, architecture, codebase) — highest-confidence finding, cosmetic.
- **N5** — 2 lenses (edge, security).
- **N2** — 2 lenses (acceptance, tests).
- **W2** — tests lens across 4 chunks.

**Verdict: READY TO MERGE** (0 blockers; all load-bearing guards verified PASS at the reviewed sha).

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
