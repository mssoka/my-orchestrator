## 🤖 Perkins automated review — round 2
**Job:** packet-plumber-v2-estate-spawning · **Reviewed sha:** f843b3d · **Reviewers:** 7/7 completed
**Verification:** 15/16 findings confirmed against the code — 1 discarded as false-positive

### Fix audit (rebase delta vs r1 APPROVED 26eb4e5)
- **Rebase is clean — mechanically proven.** Tree diff `26eb4e5..f843b3d` (103 files, +142/−29) is exactly #77's network-pop palette content: the `palette.odin` / `palette_polish_test.odin` / `palette.json` / `design-analysis/pop` hunks are **byte-identical** to #77's own diff; 86/93 delta goldens are **blob-identical** to #77's re-renders; the 7 conflict frames (`growth` ×3, `node_health` ×2, `terminal_types` ×2 — exactly the re-bless commit's file set) are fresh merged-tree renders differing from both parents. Zero `.t1`/`.log.bin`/routing/serialization/LOG_VERSION changes.
- **Estate substance untouched.** All six estate code+balance hunks in this PR are byte-identical to the r1-APPROVED round.
- **Re-bless honest — reproduced this round:** `odin test core` 232/232 · `tools/harness.sh run` **45/45** demos green · `input-parity` **27/27** · fold-check **PASS** (catalog_hash `0db1a08de26124e6`, tick-1 splices to prev `4eaa272171fac065`) · T1/`.log.bin` byte-unchanged vs r1 (palette is render-only). The 7 re-rendered T2 frames verified mechanically only — aesthetic verdicts deferred for the k3 re-check per standing orders.
- **Prior findings: 0/13 fixed, all still-present** — expected (code byte-identical; PR body unedited). r1's 3 warnings stay fix-on-follow-up tier per the 08-21/08-22 rulings; none block.

### Blockers (0)

### Warnings (4)
1. **`new_area_seed_tiles` parsed via `jint`** — decimals truncate, >i32 wraps, no fail-fast (sibling keys use `jint_strict`). `core/catalog.odin:895` — *still present since r1* [edge, security]
2. **134 `bad free` per `odin test core` run** — `make([]i32, n, context.temp_allocator)` + `defer delete` in `strict_spawn_class`. `core/growth_test.odin:527-528,556-557` — *still present since r1, reproduced live this round* [acceptance, codebase]
3. **PR body still claims "draw order/counts per attempt unchanged"** — growth.odin documents the one live-member anchor-pick draw-count change (dead-slot collision case). PR body lines 20-21 — *still present since r1* [r1 blind, orchestrator-verified]
4. **NEW: `!node_alive` disjunct of the live-terminal anchor guard untested** — no growth test demolishes a node; the fixture pins only the router `node_kind` disjunct. A regression dropping the alive check passes every test. `core/growth.odin:646` [tests]

### Notes (12)
1. Diameter guard bound `w²+h²` is looser than achievable spacing — sub-diameter floors can silently stall growth (r2 edge adds the terminal-occupancy case: seed 40 loads, max reachable dist ≈34). `core/catalog.odin:1014-1018` — *since r1* [acceptance, edge, security]
2. Spec Design Notes lines 85/87 contradict their own NOT-changed carve-out (draw counts). — *since r1* [blind]
3. Cap-8 capture shows 0 SEED events — PR sentence overstates ("before seeding a new area"). `spawn-audit-after-cap8.txt` — *since r1* [blind]
4. Fixture discards `rt` then re-fetches `router_basic`. `core/growth_test.odin:850-856` — *since r1* [blind]
5. SEED annulus draw duplicated verbatim in both branches. `core/growth.odin:694-721` — *since r1* [architecture]
6. `growth_attach_radius_ok` couples a pure distance test to `^Topology`+slot. `core/growth.odin:335-341` — *since r1* [architecture]
7. No accept-side boundary row (49 on 40×30) for the diameter bound; parsed value never asserted. `core/catalog_test.odin:720-721` — *since r1* [tests]
8. `growth_seed_sep_ok` degenerate guard (min_dist < 1) unpinned while the attach sibling is pinned. `core/growth_test.odin:783` — *since r1* [tests]
9. **NEW:** Spec line 70 says the cap demo is "(8→5)" while the decision log (1062), PR body, and capture say 5→8 — same demo, opposite arrows. [blind]
10. **NEW:** `Group_Cluster_View` dead-slot id-0 sentinel hazard documented only at the consumer, not the type doc. `core/growth.odin:121-127` vs `631-632`. [architecture]
11. **NEW:** New predicates re-inline i64 dist² math instead of the pinned `dist2` helper (`core/topology.odin:101`) — style-consistent with siblings. [codebase]
12. PR body omits the build-provenance line the briefing expected (substance independently reproduced). — *since r1* [perkins-mechanical]

Advisory test gate: **PASS** (P0 100%, P1 ~92%, overall ~90%).

### Reviewer agreement
- **Warnings 1 & 2** each independently re-derived by two fresh lenses this round (plus their r1 sources) — highest confidence.
- Warning 4 is new-single-source but orchestrator-verified by direct grep (no demolition anywhere in `core/growth_test.odin`).
- Rejected: blind's "diff ships neither goldens nor captures" — false against the canonical diff (99 goldens + 11 captures present, 45/45 replay green); a chunk artifact of lens isolation.

**Verdict:** READY TO MERGE

The r1-approved substance is byte-identical on the rebased tree; the delta vs the approved head is exactly #77's palette content and the re-bless is mechanically honest (45/45 + 27/27 + fold-check PASS + T1/log unchanged). All four warnings are hygiene/accuracy tier — well-suited to the follow-up tier, none block the spatial-policy release.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
