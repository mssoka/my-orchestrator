# D6 — Godot: what managed memory buys and costs here (cited)

## The memory model (Godot 4.7 stable docs)

- `RefCounted`-derived objects: "automatically released when no longer in
  use" — no manual free; cycles LEAK unless broken with weakref (documented).
  C# note: RefCounted objects under .NET are GC-delayed ("remain in memory
  for a while"). [G1]
- `Object`/`Node` (non-refcounted): manual `free()`/`queue_free()` — the
  engine's own docs + ecosystem guides flag leaked orphans as the classic
  Godot memory bug (remove_child without queue_free etc.). [G1, G2]

Mapping to tonight's bug: the shallow-copy-then-destroy pattern is
UNREPRESENTABLE in GDScript for RefCounted data (assignment of a
RefCounted/resource is by-reference with a refcount bump; "destroying the
copy" is not an operation the script can perform — the buffer lives while
the original references it). The same DESIGN (clone state, step it forward,
throw it away) exists and is idiomatic (`.duplicate()`, deep-copy flags) and
the bug class it can still have: shallow `duplicate()` without
DUPLICATE_USE_INSTANCING where you wanted deep — which is a LOGIC bug
(stale data read), not memory corruption; plus dangling signal connections
and orphan leaks, which Godot's debugger object-count panel surfaces.

So: Godot closes the memory-corruption PORTION (invalid free / UAF / heap
corruption) for script-level state, at the cost of GC/refcount semantics
(cycle leaks, C# GC pauses) — and engine-level C++ bugs remain possible
outside your control.

## What Godot costs THIS project (measured against the repo)

- **The determinism spine must be rebuilt on faith.** The current spine is
  in-repo fact: owned PCG32, integer-only math, binary action log, T1 hash,
  T2 pixel goldens via the rlsw SOFTWARE renderer (bit-exact, no GPU). [D3,
  PR #15] Godot's renderer is GPU-first; the bake-off already flagged
  GDScript determinism as "fought, not native" (float math in engine types,
  RefCounted/Vector2i portability, finding m6: server re-sim aspirational).
  A Godot port re-verifies determinism rather than inheriting it — and the
  148-golden corpus does not transfer (new renderer = full re-bless, and
  the drift gate's byte-exactness premise weakens).
- **58k LOC rewrite with the sim at risk of semantic drift** — the one
  thing the Odin pivot bought (determinism as compile-fact + harness-first)
  is the thing a Godot move spends. The bake-off's verdict stands on this
  axis and tonight changed nothing about it: the crash was NOT in the sim.
- **What Godot genuinely buys** (unchanged since the bake-off): editor
  iteration, scene tooling, polish loop, shipping-to-everywhere, agent
  tooling; and script-level memory safety for app-layer state — the axis
  tonight exposed. The polish-loop edge was already partially absorbed by
  the look-polish lane (#75); the memory-safety edge is NEW information
  for the record.

## Honest net

Godot = the same "would have prevented tonight's corruption" as Rust for
this bug shape, PLUS tooling, MINUS the determinism spine (the project's
crown jewel and the reason Odin won the bake-off). The bake-off record
remains the controlling argument unless the goal moves.
