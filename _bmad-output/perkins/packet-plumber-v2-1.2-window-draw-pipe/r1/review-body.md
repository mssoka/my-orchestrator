## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-1.2-window-draw-pipe
**Reviewed sha:** `8509fc2` (head unchanged at post time — no mid-review drift)
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests) — no failed layers
**Verification:** 41 raw findings → **3 discarded as false-positive** → **23 surviving** (deduped to **2 warnings, 21 notes**), of which **6 carry multi-reviewer agreement**. Every finding was re-verified against the code at the reviewed sha.

### Lens-guard verification (the load-bearing invariants — all hold)

| Guard | Result |
|---|---|
| **Replay-equality over draw** (E10) | ✅ `test_replay_byte_identical` now records a **2-pipe draw sequence** and replays byte-identically (non-vacuous: asserts `pipe_count==2` on both live + replay, hash-equality, no `replay_error`). `state_writer` serializes the Topology (nodes+pipes, alive flags) so a drawn pipe changes the hash. The app fast-path applies-then-logs-`apply_tick=next`; it converges with the pure-log path at every step boundary (draw fires after `step(T)` in `handle_input` → belongs to `T+1`'s pre-step application). |
| **ODN-1 core engine-free** | ✅ `core/` imports only `core:encoding/json` + `core:fmt`; no `vendor:raylib`/`core:os`/`core:time`. `tools/lint.sh` gate 1 green. raylib lives only in `app/` + `harness/`. |
| **ODN-10 integer / no map-iteration** | ✅ Parallel-array SOA, linear lookups, integer `dist2`/`isqrt`. lint gate 3 green; no maps iterated in core. |
| **T2 pixel golden is REAL** | ✅ `compare_images` is byte-exact (`pa[i] != pb[i]` per pixel; dimension mismatch → fail). Golden `goldens/draw/02500ms.png` present; `tools/harness.sh run` green. |
| **W1 negative test ACTUALLY in CI** | ✅ `.github/workflows/ci.yml` step "W1 drift-rejection negative test" → `tools/harness.sh drift-check`; `drift_check` asserts the gate **rejects** each mutation (accept → fail). **11/11 rejected across boot+draw.** The #599-r2 gap is closed — it's a CI step, not local-only. |
| **From-scratch, not a copy** (LG#7) | ✅ 1.2 `view.odin` (260 lines) is structurally distinct from the reference Odin tree's `view.odin` (441 lines); topology is a smaller fresh minimal implementation. No wholesale copy. |

**Gates run at `8509fc2` — all green:** `tools/lint.sh` (4/4) · `odin test core` (15/15) · `odin build app -out:app.bin` (1.38 MB) · `tools/harness.sh run` (boot + draw PASS) · `tools/harness.sh drift-check` (11/11 rejected).

### Blockers (0)
None. The window, the static map, the draw-one-pipe interaction, the T1+T2 goldens, and the W1 CI gate are all real and working. No engine leak in core; no draw path bypasses the action-log; the golden is byte-exact; W1 bites in CI.

### Warnings (2)

**W1 — Catalog fail-fast contract (ODN-5) is incomplete.** `catalogs_load`'s PROTO cross-check validates only `residential` + `router_basic`, but the fixture also requires `content_host` and the `'standard'` tier — neither is checked, and the app/harness `seed_fixture`/`pipe_tier_index` calls **discard the `ok`** and silently fall back to index 0. The file header promises "missing required content abort"; today it would silently spawn a wrong-type node / draw at tier 0 if either were removed from `data/`. *Data is correct now, so not a live break* — but the fail-fast contract has a real hole. *(blind, edge, codebase, acceptance, architecture)*
→ Add `content_host` + `standard` to the cross-check; surface the lookup `ok` instead of `_`.

**W2 — The app layer (this story's deliverable) is the least-verified part.** `app.bin` compiles + links but **no test runs it**; `snap_node`, the edit fast-path timing, and the app's fixture positions are exercised only by a human, and `load_catalogs`/`seed_fixture` are duplicated between `app/main.odin` and `harness/catalogs.odin` with **no shared contract**, so app↔harness divergence is structurally undetectable. The verified replay-equality path is the **harness** (pure action-log); the app's own glue is coverage debt on the new playable surface. (Mitigating: the app's GPU build can't run headless in CI, and the rlsw harness is the designed headless proxy sharing core+render — so this is understood, not negligence.) *(tests, codebase, architecture, blind)*
→ Extract the shared fixture into one place both call, and/or add a headless smoke that drives the app's Command_Bus/snap path through the same core the harness verifies.

### Notes (21 — grouped; full detail + evidence in `consolidated.json`)

**W1/drift-coverage (3 lenses):** the W1 negative test covers header/parse/tag/truncation classes only — valid-parse *payload* (hash-level) drift isn't generated, and `drift_check` discards the replayed hashes. LG#5 is satisfied; this is a coverage *extension*, not a gap. — *span metric:* `span_between`'s round-half-up branch is never exercised (all test/demo spans are perfect squares) and the rounded-span compare is slightly more permissive than the documented "compare squares" convention (no live impact — fixture spans are exactly 12; golden blessed on actual behavior). — *drift truncation:* the truncation mutation lacks the `len(src)>0` guard the other 5 have → would crash (not clean-reject) on a 0-byte log (latent; blessed logs are 33/71 bytes).

**Catalog robustness (2 lenses):** `jint` narrows `json.Integer` (i64)→i32 with an unchecked cast (could wrap into range; catalogs are checked-in data, so defense-in-depth). — `dist2` widens to i64 *after* the i32 subtraction (overflow at ≥2³¹ grid span; theoretical only on a 40×30 map).

**Cosmetic / app-only (blind):** `draw_text` truncates runes to `u8` → the em-dash in the window title renders as a garbage byte. — The fiber "glowing inner core" draws `pipe_fiber` over `pipe_fiber` (no-op glow; `palette.json`'s `pipe_core` is never read; latent — fixture draws `standard`, never `wide`). — `draw_ghost` shows green even with no snap target (slightly misleading preview). — `Draw_Intent.tier`'s "default standard" comment is unimplemented (parser requires the field). — `App.res_id/rt_id/host_id` are write-only dead fields. — `main` never calls `run_destroy` (moot — OS reclaims on exit; inconsistent with the defer pattern).

**Boundary / authoring-safety (edge):** T2 capture times quantizing to tick 0 or past the last tick are silently skipped (demo still passes). — Draw intents beyond `run_ms` become inert dead log records (silently accepted). — `self-loop` drag is pre-filtered before validation, so `.Self_Loop` never surfaces in the UI (functionally correct, no feedback). — `node_slot_raw`'s slot-0 fallback is a latent trap if a caller ever skips `validate_draw` (unreachable on the current path).

**Security (defense-in-depth, local dev tool):** demo names flow unsanitized into golden/tmp paths — path traversal is CLI-reachable (`harness run|save <name>`), not from the CI `demos/` listing.

**Architecture / forward-looking:** `step` applies commands one-by-one, not the arch §6.1/E23 atomic batch (no multi-command batch exists in 1.2; relevant when demolish lands). — Demos lower to Commands directly, bypassing the app's Input/Command_Bus (arch §10.3 same-path-as-mouse); the core `topology_apply_edit` path IS shared.

**Tests:** "a rejected draw mutates nothing" is asserted for 3/5 rejections (unknown-tier + missing-node omit the `pipe_count==0` check). — E11's never-recycled-on-demolish half is untestable in 1.2 (no demolish; the `alive=false` serialization path is dead until then). — **Advisory test gate: CONCERNS** (the tests lens rated FAIL by counting app fast-path/snap as untested P0; re-triaged — the E10 *mechanism* is verified, the app-binary gap is the GPU/CI constraint captured in W2).

**From-scratch (positive):** lens-guard #7 verified clean — recorded for traceability.

### Reviewer agreement (multi-source, highest confidence)
The two warnings (W1: 5 lenses; W2: 4 lenses) and the drift-class/span-metric/drift-truncation/jint notes (2 lenses each) are the cross-validated signal — prioritize these.

**Verdict: READY TO MERGE**

Every load-bearing lens-guard holds and all five gates are green at the reviewed sha; this is a solid first playable `app.bin` on a proven determinism spine. The 2 warnings are real but do not violate any spine invariant — they're worth folding into 1.3 (catalog hardening + a headless app-path smoke), not blockers for this slice. (No routing is expected — 1.3 by design.)

---
*Perkins r1 of 3. Address findings and push to `v2`; mention `@solarity-services` for a fresh round. Full evidence + the 3 rejected false-positives live in `_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/consolidated.json`.*
