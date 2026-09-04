# D5 — Odin: hardening THIS codebase (cited + measured)

## Language facts (roadmap honesty)

- **Odin will NOT get Rust-style ownership/borrow checking.** The designer's
  position is on record: gingerBill, "The Fatal Flaw of Ownership Semantics"
  (2020) — ownership semantics are "a linear value hierarchy of
  responsibility" that "cannot express non-linear problems"; his recommended
  alternative is subsystems handing out INDICES/HANDLES (with generation
  numbers), POD structs, and allocators. [O2]
- **core:mem doc states it directly**: "unlike Rust, in Odin the memory
  ownership model is not strict." Allocators are the language-level safety
  tool. [O1]
- **Odin 1.0 ("Odin 2027") is scheduled for January 2027, RC late Dec 2026**:
  full language spec + backward-compatibility commitment — a stability
  milestone, not a safety-model change (manual memory + custom allocators
  stays the model). [O3]

## The tool that catches tonight's class deterministically: Tracking_Allocator

core:mem ships `Tracking_Allocator`: wraps any backing allocator, records
every live allocation (map[rawptr] → entry with size/alignment/location),
and on `Free` of a pointer it does not own fires a **bad_free_callback with
the Source_Code_Location of the offending free** (a panic callback is
bundled: `tracking_allocator_bad_free_callback_panic`). [O1]

Mapping to tonight: wrapping the run's allocator (debug/CI builds) makes the
shadow's `delete(shadow.box.pieces)` — a free of the LIVE run's pointer —
abort AT THE FIRST OFFENSE with file:line, instead of a heap-reuse-lottery
SIGABRT three connections later. The harness leg: run the sim corpus +
predict path under `context.allocator = tracking` nightly.

## Structural guards for the recurring class (3 instances and counting)

The class: "new `[dynamic]` field on Run_State, `shadow_clone` not updated."
Guards, cheapest first (all Odin-native):

1. **Exhaustiveness test**: a unit test that reflects over a fully-grown
   Run_State (every array grown to nonzero len, filled with a magic byte
   pattern), runs shadow_clone + run_destroy on it, and asserts every live
   buffer's contents untouched + no bad frees under a tracking allocator.
   Catches ANY future un-cloned field at CI time, mechanically. (Odin
   `any`/reflect makes the field-walk feasible; even a hand-maintained
   field list in the TEST is strictly better than the clone list alone —
   two lists that must agree beat one list that silently rots.)
2. **Arena the shadow**: `shadow_clone` onto a scratch arena +
   `arena_free_all` instead of run_destroy — the destroy path DISAPPEARS
   (no per-array deletes to mismatch). This is the fix-shape the codebase's
   own comments keep re-discovering; Odin's mem docs recommend exactly this
   for frame-scope temporaries. [O1]
3. **Convention pins** (cheap, partial): a "new dynamic field" checklist
   item in the PR template naming the 4 places to touch (types.odin,
   shadow_clone, serialize, run_destroy); a Perkins lens addition that
   greps PR diffs for `[dynamic]` additions to Run_State and flags the
   clone list.

## Where the manual frees live (measured, D2)

232 delete sites (0 raw frees — the codebase is uniformly dynamic-array
disciplined); the sim's lifetime is concentrated in run_destroy +
per-proc defers; app uses per-frame temp-arena free_all (10 sites). The
spawns/predict/audio/hud app surface is where lifetime bugs have ACTUALLY
landed (all 3 instances) — hardening effort should aim there, not at the
(already clean) sim.

## Odin's compensating virtues (why "stay" is not defeat)

- The determinism spine is compile-adjacent-fact TODAY (owned PRNG,
  integer-only, T1/T2 goldens) — the harness caught every sim regression
  this era; tonight's miss is an app-layer gap, not a language failure.
- Odin 1.0 in Jan 2027 de-risks the toolchain bet (spec + compat). [O3]
- The bug took ~2h to root-cause WITH the toolchain at hand (lldb + debug
  build + scripted repro) — the language's debuggability (no hidden
  control flow, plain arrays) is part of why.
