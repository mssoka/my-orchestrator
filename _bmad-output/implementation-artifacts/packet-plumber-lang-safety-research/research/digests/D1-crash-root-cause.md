# D1 — The crash, root-caused (FACTS, measured this run)

## The evidence chain

1. **User crashes (given)**: 2 × macOS `.ips` (21:11, 21:14 2026-08-28), SIGABRT,
   `___BUG_IN_CLIENT_OF_LIBMALLOC_POINTER_BEING_FREED_WAS_NOT_ALLOCATED`
   from Odin `runtime::_heap_free` (heap_allocator_unix.odin). App frames lost
   to the abort path.
2. **Faithful repro (this run, /tmp/pp-repro @ v2 3960644)**: scripted real-input
   playtest (`PP_SPAWN_E2E` driver in a /tmp copy — repo untouched): place
   router → wait for growth spawns → real drag-press/move/release connections.
   Abort trap 6 at the first spawn-connection window; fresh `.ips` signature
   IDENTICAL to the user's two.
3. **Stack captured under lldb (-debug build, breakpoint malloc_error_break)**:
   ```
   #4  runtime::_heap_free                      heap_allocator_unix.odin:37
   #9  runtime::delete_dynamic_array
   #10 core::box_destroy        box.odin:44     delete(b.pieces)
   #11 core::run_destroy        types.odin:621
   #12 render::spawn_fx_predict spawn_fx.odin:303   <- shadow := clone; defer run_destroy(&shadow)
   #13 main::main               main.odin:882       <- per-frame spawn telegraph
   ```
4. **Root cause (code-verified)**: `shadow_clone` (app/render/spawn_fx.odin)
   deep-clones every `[dynamic]` section of `Run_State` **except the Box**.
   #107 added `Box_State{pieces, spools: [dynamic]u32}` and `start_run` now
   calls `box_enable` (arrays grow on the live run). The shadow's struct-copy
   carries the LIVE run's array headers (data ptr + allocator). Odin dynamic
   arrays store their allocator in the header, so `run_destroy(&shadow)` →
   `box_destroy` → `delete(shadow.box.pieces)` is a VALID heap free **of the
   live run's buffer** — silent. The live run runs on dangling box pointers
   (HUD reads box counts every frame = UAF reads). A later telegraph
   re-predict (spawn window or topology-gen bump — every connection bumps
   gen) or resize frees the dangling pointer again → libmalloc abort.
5. **RED→GREEN proof (mutation-leg standard)**: unpatched build aborts (above);
   +2 lines in `shadow_clone` (`c.box.pieces = clone_dyn(...)`,
   `c.box.spools = clone_dyn(...)`) → scripted playtest connects 8 spawn
   buildings (5+ requirement), clean exit 0, no crash.

## Why "3rd connection" (user) vs "1st" (repro)

The class is deterministic (every box-on run with a telegraph window frees the
live box storage at the FIRST predict); the ABORT timing rides heap-reuse
variance — the abort lands on the first free() of a pointer malloc has since
re-registered. User hit it on connect 3; the scripted repro on connect 1.
Same site, same signature.

## This is the THIRD instance of a known recurring class

In-code comments in the SAME proc document the prior two:
- v2-network-units: the tx window ring — "a shadow that skipped it would carry
  the LIVE state's data pointers and corrupt it on resize/delete".
- v2-arch-egress S5: the residency ledger — "the same shadow-steps + destroy
  pattern … (the spawn_feel heap-abort, caught at run_destroy)".
- #107 the Box — same shape, missed again.

The class: **add a `[dynamic]` field to `Run_State` → forget `shadow_clone` →
the telegraph predictor frees/corrupts live memory.** No structural guard
(exhaustiveness test, arena for the shadow, or copy-derive-by-construction)
exists; each instance was caught by crash, not by test.

## Why every existing safety net missed it (measured)

| Net | Coverage of this path | Why it missed |
|---|---|---|
| 13-gate local CI (incl. `box on` demo `box_spine.dem`) | harness NEVER calls `spawn_fx_predict` (grep: 0 refs in harness/) | telegraph predict is APP-only surface (main.odin:882) |
| Unit suites (spawn_fx_test shadow round-trip etc.) | runs box-OFF (len-0 arrays → delete no-op) | no "shadow_clone clones EVERY dynamic field" invariant test |
| Perkins r1–r5 on #107 | economy/serialization semantics of the Box | miss is cross-file: types.odin (new fields) × render/spawn_fx.odin (clone list) |
| Playtest (the user) | full app, box-on | CAUGHT IT — the only net that exercises the real combination |

## POST-RUN CONFIRMATION — PR #108 (box-crash-third-spawn), r1 APPROVED (review 5055486548), 2026-08-28 late

The fix PR landed the SAME root cause independently (its Perkins r1 consolidated
verdict CONFIRMS the mechanism above verbatim, and DISCONFIRMS the original
briefing's capacity-2→4 grow hypothesis: `box_grow` sizes once at box_enable,
idempotent after — no mid-play grow). Additions beyond this digest:

- **Mutation gate run by Perkins with the tracked allocator**: removing the 3
  fix lines → RED (both new tests fail + tracked-allocator bad-frees at
  box.odin:44-45 across a 5-spawn-window leg); restore → GREEN (117/117 render
  tests). NOTE: this is exactly the D5/Phase-1 tooling recommendation — the
  Tracking_Allocator caught the class deterministically at the .ips site.
- **Class sweep COMPLETE at that sha**: 55 run_destroy deletes vs 53 clone_dyn
  + 2 by-design zeroed (action_log/events, asserted nil). No stragglers.
- **New landed guards**: `test_spawn_fx_shadow_clone_box_owns_every_array`
  (pins EVERY owned Run_State array to a private buffer — 57 arrays / 8 destroy
  groups) + `test_spawn_fx_predict_box_economy_leg` (the playtest as a gate:
  5 spawn windows crossed with the box verbs). = this report's Phase-1 item 1,
  landed better than proposed.
- **A 4th sibling surfaced during the fix**: the predict loop leaked
  `batch` (per-shadow-tick command scratch) one alloc per tick — LEAK class,
  not corruption; also fixed in #108 (`delete(batch)`).
- **Residual debt named by Perkins (their W1/W2/W3)**: the alias gate's
  len==0 skip leaves 15/57 pins vacuous in-fixture (fixture doesn't enable
  health/advance-gate/lane cmds); the mirror + checklist are still MANUAL;
  recommendation to move shadow_clone (or a field-inventory invariant) into
  core. = this report's Phase-1 refinements + Phase-3, still open.

## Bug-space taxonomy (for the falsify-the-premise mapping)

What the bug IS:
- a **stale-alias lifetime bug** (shallow struct copy sharing owned heap
  buffers), i.e. a use-after-free / double-free class
- enabled by Odin's **manual memory discipline** (explicit clone lists +
  explicit run_destroy) with **no language-level guard** on struct copies
  of owning structs — Odin copies are shallow by design and nothing marks
  `Run_State` as owning/non-copyable.

What it is NOT:
- not an allocator mismatch per se (all frees went through the correct
  heap allocator — Odin's stored-allocator headers handled that);
- not a logic error in the Box economy (box.odin itself is clean — arrays
  via make/resize/delete, no raw frees);
- not a concurrency bug (single-threaded).
