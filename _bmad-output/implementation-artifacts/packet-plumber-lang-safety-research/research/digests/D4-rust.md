# D4 — Rust: what it would and would not have prevented (cited)

## The falsify-the-premise core: tonight's bug in Rust semantics

Tonight's bug = shallow struct copy aliasing owned heap buffers + a destroy of
the copy (double free / use-after-free). In safe Rust this is UNREPRESENTABLE
at compile time — not caught at runtime, not "a panic instead": it does not
compile.

- The Rust Book ch.4 (ownership rules: "Each value has an owner; only one
  owner at a time; owner dropped at scope end") states the exact case: two
  values sharing one heap buffer "will both try to free the same memory —
  known as a double free error"; assignment MOVES ownership and the compiler
  rejects use of the moved-from value (error E0382). The shadow-clone pattern
  (`shadow := clone of state; defer destroy(shadow)`) translates to either
  `let shadow = state.clone()` (deep clone, one owner each — the destroy is
  the shadow's own drop, harmless) or `let shadow = &state` (borrow —
  destroying through it is a compile error). There is no spelling that
  compiles into tonight's bug without `unsafe` or raw pointers + `Clone`
  misuse that clones handles but not data (an explicit, reviewable `unsafe`
  or a hand-written `Clone` impl — both visible in diff review).
  [R1: doc.rust-lang.org/book/ch04-01]
- CAVEAT (honesty): this covers SAFE Rust's default data types. A port that
  wraps wgpu/raylib FFI, uses `unsafe` renderer interop, or hand-rolls
  `Clone` impls re-opens a narrower version of the hole. The class Rust
  closes here is the default-shaped one — exactly the shape tonight's bug
  had.

## What Rust does NOT close (the inversion, per the briefing)

- Logic bugs (spool arithmetic, era caps, game rules) — identical exposure.
- Determinism hazards — Rust does not fix float non-determinism or hash-map
  iteration order; the repo's integer-only/array-only discipline must be
  REPLICATED by convention (it is convention in Rust too, not a type-system
  fact — no compile error orders your map iteration).
- Leak-shaped bugs (growing buffers never freed) — safe Rust leaks happily
  (`mem::forget`, Rc cycles); Odin leaks happily. Same exposure.
- The "shadow steps the sim forward" DESIGN (predict-by-cloning) — the same
  architecture exists in Rust; it just can't alias (the clone is forced to be
  real, which is a real perf cost the Odin bug accidentally skipped paying).
- Races: single-threaded game — no exposure either way today; safe Rust WOULD
  close data races if multithreading arrives (Send/Sync), Odin would not.

## Idiomatic gamedev Rust today (what a port re-choices)

- Bevy 0.19 (2026-06-19; 0.19.1 patch 2026-08-12): ECS data-driven, active
  (6th birthday Aug 2026, ~7M crates.io downloads). Still pre-1.0: breaking
  changes ship in every minor (~quarterly cadence historically). [R2, R5]
- The custom renderer (8,850 LOC on raylib, 92 rl.* procs) has no direct
  port: raylib bindings exist in Rust but the idiomatic stack is wgpu (or
  Bevy's renderer) — i.e., the port REWRITES the render layer, not rebinding
  it. [R2]
- Port friction documented by Bevy's own docs: "compile times can be quite
  long" — the official fast-compiles book page exists because iteration
  speed is a known tax; rendering crates ≈75% of Bevy compile time
  (bevyengine/bevy#23642, Apr 2026). The PP loop (odin build app ≈ seconds
  today; 50-demo golden harness per CI run) would feel this directly. [R3, R4]

## Port cost in THIS repo's terms (measured, D2)

- ~58k LOC Odin total (11.2k sim + 15.6k app + 8.8k render + 8.8k harness);
  sim ports semantically 1:1 (pure, integer-only — the discipline maps);
  app/render is a REWRITE on a new stack; harness needs a new software
  renderer story (rlsw has no Rust equivalent in-repo — pixel goldens would
  need re-blessing against a new renderer, a corpus event).
- Test corpus: 22.7k LOC of Odin tests + 50 demos + 148 goldens re-home onto
  Rust test infra; demos/goldens are data (portable); the T1 hash spine is
  portable BY SPEC (owned PRNG, integer-only) — replay parity is provable
  across languages, which is the one big de-risker of any port.
