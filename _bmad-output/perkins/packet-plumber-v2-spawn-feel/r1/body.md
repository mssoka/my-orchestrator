## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-spawn-feel · **Reviewed sha:** 1c1d408 · **Reviewers:** 7/7 completed
**Verification:** 28/30 findings confirmed against the code — 2 discarded as false-positive

Perkins mechanical pre-pass (all verified in the round worktree): `odin test core` 236/236 · `odin test app/render` 22/22 (repo-root cwd) · harness 47/47 incl. replay gate · ci-local 10/10 · bad-frees now exactly 2, both pre-existing in untouched `health_test.odin` · spawn-sequence pixel audit confirms ring@3600 → grow → pop@4000 → monotonic reveal settle → second beat@8000 · scope confined to spawn_fx + wiring + the estate folds (no serialization/LOG_VERSION/sim-semantics changes) · `shadow_clone` is field-for-field complete today.

### Blockers (2)

**B1 — Pipe-highlight radius mixes units: tile-space dx/dy tested against `8 × tile_px` — every pipe on the map pulses** · `[blind, edge, tests]` · `app/render/spawn_fx.odin` `spawn_fx_draw_highlight`
```odin
rad := f32(SPAWN_HIGHLIGHT_RADIUS_TILES) * v.tile_px   // 8×26 = 208
dx := f32(mid[0]) - f32(r.pos[0])                       // TILE units
if dx * dx + dy * dy > rad * rad { continue }
```
The guard compares tile-unit distance² against (208)² — no pipe on a 40×30 map is excluded. Golden-verified: `spawn_feel/04000ms.png` pulses pipe 1→3 whose midpoint sits **9.8 tiles** from the spawn (intended bound: 8, "the estate radius + margin" per your own comment). Every spawn flashes the whole network's pipes instead of the neighborhood; the behavior is baked into the re-blessed goldens. Fix: drop `* v.tile_px` (compare tile units) and re-bless the spawn_feel captures.

**B2 — The pending-commands predictor pin is vacuous: its draw is span-invalid and is rejected identically on both sides** · `[tests]` · `app/render/spawn_fx_test.odin` `test_spawn_fx_predict_pending_commands`
```odin
pending := []pp.Command{{kind = pp.Cmd_Draw_Pipe{a = 0, b = 3, tier = 1}, apply_tick = 77}}
```
Node 0 (10,10) → node 3 (34,15) spans **25** (rounded euclidean) > standard's `max_span` **14** → `Span_Exceeds_Tier` — the draw never materializes on the live side or the shadow side, so "the pending draw must move the prediction exactly like the live sim" asserts a tautology. Same root cause silently rejects `sfx_fixture`'s own 1→3 pipe (span 23), so the whole test file runs on a pipe-less topology. Fix: use the real harness fixture positions — res (8,15), rt (20,15), host (32,15), placed router (34,15) — where 1→3 is span-exact 14 = valid; assert the pipe exists after apply.

### Warnings (6)

**W1 — Reduced-motion disables the pipe highlight entirely, contradicting the documented "steady band"** · `[blind]` · `spawn_fx_draw_highlight` — the file header and PR body promise "the highlight is steady" (E9.2, the pulse_read presence-not-motion precedent); the code `return`s. Ring and reveal keep their static readings — the highlight alone loses presence. Draw the steady band instead.
**W2 — Type-chip hairline fade reintroduces the rlsw line-alpha trap during the reveal** · `[blind]` · `draw_type_chip` — `out.a = u8(255 * fade); rl.DrawRectangleLinesEx(...)`: the software renderer ignores line alpha, so captures render the hairline solid through the 8-tick reveal while the GPU app fades it — app and goldens diverge per spawn. The pre-change code deliberately kept this line full-alpha. Keep it 255 or use filled rects.
**W3 — `spawn_fx_init`/`spawn_fx_destroy` are dead code; `reveals` latches the ambient allocator on first append and is never freed — 3,318 tracker leak lines added to the render suite** · `[blind, security, codebase, architecture]` — the same tracker-noise class this PR's growth_test fold cleaned out of core, now added to render. Wire init/destroy into the View lifecycle or delete them.
**W4 — `shadow_clone` completeness guard cannot catch future non-serialized dynamic fields; a miss frees live sim memory** · `[architecture]` — the round-trip pin covers only hash-visible state; a future missed `[dynamic]` field leaves the clone aliasing the live array and `run_destroy(&shadow)` deletes the **live** buffer. Today the clone is complete (verified field-for-field). Extend the pin or name the contract.
**W5 — Reveal-buffer `> 4` trim boundary has no test** · `[tests]` — the unbounded-growth guard for pause/catch-up bursts is unexercised.
**W6 — Reduced-motion telegraph ring and highlight paths untested** · `[tests]` — only the reveal's pin exists, which is why W1's doc/code divergence is invisible to the suite.

### Notes (11)

1. **PR body mis-describes the node_health 20000ms re-bless as carrying "the ring burst"** · `[acceptance]` — at t400 the harness predict targets window 480 and the t400 telegraph was never predicted; the frame carries reveal + highlight only. The re-bless itself remains justified (cause documented otherwise correctly).
2. **Highlight = neighborhood pipes vs the spec's "connecting pipe"** · `[acceptance]` — documented, defensible interpretation (a fresh spawn has no pipes); superseded in practice by B1.
3. **`sfx_fixture` is not "the growth.dem recipe" it claims** · `[acceptance, tests]` — different base positions + the silently-rejected pipe (see B2); the pins still hold but the comment lies.
4. **`sfx_load_cat` declares an `allocator` parameter the body never uses** · `[security, codebase]`.
5. **Predictor's `next_node_id`-delta spawn detection would telegraph a pending `Cmd_Place_Router`** · `[codebase]` — theoretical today (both callers pass only applied commands); API-surface risk.
6. **Dedup-reset branch in `spawn_fx_predict` is unreachable** · `[blind]` — dead defensive code.
7. **Pointless `_ = before` no-op in the feed test** · `[blind]`.
8. **Telegraph timeline guard wraps when `terminal_spawn_interval_ticks < 10`** · `[blind, edge]` — unreachable at the shipped 80-tick cadence; a modded-catalog edge.
9. **Bad-free fix is unverifiable by test; the 2 remaining bad frees are confirmed pre-existing** (`health_test.odin` 877/910, untouched by this diff) · `[tests]`.
10. **App-side predict glue (Run-mode gate, per-frame dedup, topology-gen re-predict) has no automated coverage** · `[tests]` — goldens cover the harness force path only.
11. **Render package now owns a field-by-field `Run_State` deep copy and executes `pp.step` in the view layer** · `[architecture]` — documented, deliberate trade-off per the PR body's decision table (core-side prediction rejected as a sim-semantics change); recorded as accepted risk, not re-litigated.

### Reviewer agreement
- **B1 radius bug**: blind + edge + tests, independently — plus Perkins' golden pixel evidence.
- **W3 dead init/destroy**: all four of blind/security/codebase/architecture.
- **Note 8 underflow edge**: blind + edge. **Note 3 fixture**: acceptance + tests. **Note 4**: security + codebase.
- Tests-lens advisory gate: FAIL (P0 drivers = B1/B2 + W5/W6 — folded above, not double-counted).

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
