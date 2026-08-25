## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-3.2-lane-qos · **Reviewed sha:** `7c07a80` · **Reviewers:** 21/21 completed (7 lenses × 3 chunks — diff 6912 lines exceeded the big-diff threshold: chunk 1 core 1224 lines/10 files, chunk 2 app+harness+data+docs 1088 lines/14 files, chunk 3 goldens 4604 lines/23 files; findings merged before verification)
**Verification:** 21/22 unique findings confirmed against the code (34 raw lens reports deduped) — 1 discarded as false-positive, 0 kept as [unverified]

**Ground truth at `7c07a80` (verified independently this round):** `odin test core` **69/69 green** (incl. the E5/E6/E8 pins, the sparse-serialization pin, the replay byte-identity pin) · `harness run` **10/10 green** — all 9 pre-existing demos' T1 + replay gate + **T2 pixel goldens pass byte-identical against their UNCHANGED PNGs**, plus the new `qos_emphasis` golden (T2 captures visually show the proportions changing: none → amber-heavy express → green-heavy best-effort) · `harness drift-check` **69/69 mutations rejected** · `tools/lint.sh` **5/5 gates green** · `odin build` app + harness **green**. Base-commit sanity: `harness run` at `9a5a35b` 9/9 green (old goldens honest).

**The ODN-11 re-bless — PROVEN, independently.** The minion's two-part proof checks out at the byte level: (a) **T2 pixels** — zero existing PNGs changed in the diff AND the new render code passes all 9 existing demos' T2 checks against the old PNGs; (b) **reconstruction** — a sandbox splice-proof (old log + new code + OLD catalog_hash forced into the run state) reproduced every old `.t1` hash bit-for-bit across all 9 pre-existing demos, including `qos.dem`'s 1500 ticks. All 10 manifests carry the identical new `catalog_hash c403567796188e5b`; the `.t1`/`.log.bin` shift is exactly the deliberate balance.json content binding — **zero sim behavior changed**. The old binary also rejects a new-format log cleanly (unknown tag → parse failure), and the new code reads old logs fine. This is the defined ODN-11 gate, not a silent re-bless — NOT a finding (per the round lens-guard).

### Blockers (0)

None. The load-bearing contracts all hold: **E5** (all-zero → catalog default preset, pinned), **E6** (never-drop lane floored in `flow_step` + the zeroing edit rejected at the bus — the rejection is test-pinned: neutralizing the guard turns `test_qos_bus_rejections_e6` red), **E8** (largest-remainder, E→S→B tie order, sum == capacity sweep), **weight-only [ODN-3]** (no demand input anywhere in the lane resolution), **replay determinism [E10]** (LOG_VERSION 2 consistent with the merged 2.3 additive-tag convention; drift suite green), **data-driven balance [ODN-5]** (presets in balance.json, hardcoded-weight-free).

### Warnings (2)

1. **QoS rejection toast is gated on pipe selection, but the right-click dial path never selects — a rejected dial move on an unselected pipe is silent, contradicting the code's own "never silent" intent** · 4-lens agreement (architecture, blind, codebase, edge) · `app/main.odin:453-497` (+ `:198-209`, `:388-393`). The toast draws inside `if app.sel_pipe >= 0`, while right-click cycles the hit pipe without selecting it — an E6 rejection there sets `last_reject` but no toast renders. Unreachable today (the shipped catalog has no never-drop class; banking is era-4 content), but the comment at `:493` explicitly promises "a rejected dial/lane edit is never silent". *Fix:* draw the toast outside the selection gate (or select the hit pipe on right-click).
2. **App emphasis-dial interaction logic (`pipe_hit`, dial wrap, lane keys, toast) has zero automated coverage** · `tests` · `app/main.odin:316, :368, :400`. The story's launchable increment is the dial + keys + readout; the wrap math and point-to-segment hit-test are real logic exercised by no test at any level (the repo has no app-layer test harness; core invariants are pinned, this is the glue). *Fix:* extract the pure dial/hit-test math for a unit pin, or add a harness input-level demo.

### Notes (19)

1. **`b.lane_presets` leaks on every balance.json fail-fast rejection** (make before any reject return; `cat.balance = b` only on success) · 2-lens agreement (blind, codebase) · `core/catalog.odin:480-549`. Error-path-only (catalog failure aborts startup); same class as the loader's pre-existing error-path leaks. *Fix:* free before the reject returns.
2. **No preset-count bound before u16 narrowing** — >65535 presets silently wrap `default_preset_idx`/`preset_index` · 2-lens agreement (edge, security) · `core/catalog.odin:540, :626-631`. The loader bounds VALUES but not the row COUNT. *Fix:* reject `len > u16::MAX` at load.
3. **`default_lane_preset` absent or non-string silently falls back to preset 0** instead of fail-fast · 2-lens agreement (acceptance, edge) · `core/catalog.odin:534-536, :644-647`. The spec's I/O matrix lists "missing default | rejected at load"; an unknown-string value IS rejected, so the fallback is inconsistent. *Fix:* require the field, `json.String`, resolvable id.
4. **New emphasis/lane demo directives truncate pipe ids u64→u32** with no range check — an id ≥ 2³² silently targets a different (possibly live) pipe · 2-lens agreement (security) · `harness/demo.odin:258-277`. The bus's `.Missing_Pipe` can't catch a wrapped id. *Fix:* range-check before the cast.
5. **`intent_apply_tick_raw` is a third copy of the floor(at_ms·hz/1000)+1 apply-tick formula** (and shares its unbounded multiply) · 3-lens agreement (blind, codebase, security) · `harness/run.odin:85-87`. A future timing-convention change must be made in three places. *Fix:* reuse the shared helper.
6. **Harness emphasis/lane directive error paths are untested** (happy-path only; the harness has no unit-test structure) · 2-lens agreement (tests) · `harness/demo.odin:258-282`, `harness/run.odin:57-76`.
7. **Advisory test gate: PASS** · 3-lens agreement (tests) · P0 100%, P1 100%, overall ~85% (shortfalls: app glue + directive errors).
8. **Lane-proportions readout can display percentages that don't sum to 100** (default balanced = 33/33/33 = 99%) · acceptance · `app/main.odin:514`. Cosmetic; the readout is the story's visible deliverable.
9. **`pipe_hit` radius hardcoded at 10 world px** while the sibling interaction radius (`snap_radius`) is data-driven in balance.json · architecture · `app/main.odin:319`. *Fix:* move to balance.json.
10. **Lane-stripe render consumes `flow.lane_caps`, one tick stale after a fast-path edit** — stripes and the fresh `qos_pipe_caps` readout can disagree for one 50ms frame · blind · `app/render/view.odin` + `app/main.odin:466-468`. Transient; the comment documents the readout side of the choice.
11. **Spec Design Notes list two `qos_emphasis.dem` captures; the demo records a third (12000ms)** — the frozen spec under-describes the golden · blind · `spec-3-2-lane-qos.md` vs `demos/qos_emphasis.dem:27-29`.
12. **`check_reject_balance`'s file assertion is weaker than the sibling `check_reject`** — a wrong-file rejection silently passes the rule check · codebase · `core/catalog_test.odin:209-221`. Unreachable today (sibling fixtures fixed-valid).
13. **OS window title still reads "v2 story 1.2"** while the HUD banner was updated to 3.2 · codebase · `app/main.odin:77`. Stale since 1.4; the diff touched the sibling line.
14. **Demo parse-error paths leak the new emphasis/lanes arrays** (same as the pre-existing sibling arrays' pattern) · edge · `harness/demo.odin:128-129`.
15. **Node-demolish lane-override purge (`apply_demolish_node`) has no test** — only the pipe-demolish purge is pinned · tests · `core/topology.odin:283-287`.
16. **`lane_presets` fail-fast: the "preset display_name empty" branch has no test row** (11 of 12 branches pinned) · tests · `core/catalog.odin:490-492`.
17. **`lane_presets` loader positive path unasserted** — parsed values + the absent-default fallback (idx 0) are unpinned; all QoS tests bypass the loader via `test_catalog` · tests · `core/catalog_test.odin:86-105`.
18. **E6 never-drop interactions are pinned only through banking's DEFAULT lane** — override-resolved bindings (acceptance AND rejection) untested · tests · `core/qos_test.odin:21-31, :116-120, :138-159`.
19. **E6 floor is pinned at proc level only** — a floored value is never asserted end-to-end through `flow_step` into `lane_caps` (the white-box test calls `qos_pipe_caps` directly) · tests · `core/qos_test.odin:108-115`.

### Reviewer agreement

The 4-lens convergence on the toast-gating defect (architecture, blind, codebase, edge — all traced the same right-click → `cycle_emphasis` → `last_reject` → gated-draw chain) is the round's highest-confidence signal; the 3-lens convergence on the `intent_apply_tick` duplication family is second. The ODN-5 validation surface is in far better shape than round 3.1 (11 of 12 negative rows pinned; the survivors are count/type-narrowing nits), and every load-bearing contract held under independent byte-level verification. Rejected as false-positive after code verification: the `or_continue` silent-skip note (established house pattern in every loader since 1.2 — the identical finding was rejected in round 3.1).

**Verdict:** READY TO MERGE

The QoS differentiator opens on a verified spine: the re-bless is proven (bit-for-bit splice proof, pixel-identical T2), the E5/E6/E8 contracts are pinned and bite, the allocator is weight-only inside Flow, and replay determinism holds across the new commands. The 2 warnings + 19 notes are polish items (UI toast gating, app-glue coverage, small validation/leak/docs nits) — none block merge.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
