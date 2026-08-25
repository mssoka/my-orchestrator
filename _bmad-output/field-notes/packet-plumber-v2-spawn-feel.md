# packet-plumber-v2-spawn-feel — field notes

- Odin render work: rlgl ENABLES backface culling with front = CCW — any
  hand-built triangle fan/quad (annulus rings, highlight bands) must wind CCW
  in screen space or it renders NOTHING in both the rlsw captures AND the GPU
  app; and the rlsw software renderer ignores LINE alpha (fills only) — a
  fading ring must be filled geometry, never DrawCircleLines/DrawLineEx.
- NEVER build the harness with a bare `odin build harness` — the rlsw shadow
  link requires `tools/harness.sh` (ODIN_ROOT=.../raylib-sw/shadow); a stock
  build links GPU raylib, the BGRA swizzle then corrupts EVERY capture (R/B
  swap + black first frame) and the suite "fails" with misleading full-frame
  diffs.
- Predicting the next growth-window spawn is a SHADOW CLONE + ≤10-step
  replay (deterministic sim — bit-exact); the clone must deep-copy every
  Run_State array (routing/bundles/flow/crisis/health/era_gate) — pinned by a
  hash round-trip test. Pending commands (apply_tick in (tick, window]) must
  be replayed by the shadow or demo draws mid-window diverge the telegraph.
