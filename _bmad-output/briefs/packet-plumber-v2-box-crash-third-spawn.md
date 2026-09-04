# Briefing: packet-plumber-v2-box-crash-third-spawn (URGENT)

BUG FIX — user's playtest (the fun-test gate on merged #107) is BLOCKED:
the game crashes when connecting the THIRD spawn building. Top priority;
the user is waiting to play.

## The evidence (in hand)

- TWO macOS crash reports, minutes apart (user reproduced twice):
  - `~/Library/Logs/DiagnosticReports/app.bin-2026-08-28-211134.ips`
  - `~/Library/Logs/DiagnosticReports/app.bin-2026-08-28-211400.ips`
- Signature (both): SIGABRT / Abort trap 6,
  `___BUG_IN_CLIENT_OF_LIBMALLOC_POINTER_BEING_FREED_WAS_NOT_ALLOCATED`
  raised from Odin `runtime::_heap_free` (heap_allocator_unix.odin).
  The app-level caller frames are lost to the abort path — you must
  reproduce to get the true stack.
- Repro: launch app.bin from merged v2 HEAD (396064b), connect spawn
  buildings — crash on the third connection.
- Timing: POST-#107-merge. The Box (typed pieces, spools, caps,
  promotion, teardown/resplice returns, era/milestone refill structures)
  is the prime suspect surface.

## Leading hypothesis (verify, do not assume)

The THIRD spawn is the tell: a dynamic array at capacity 2 growing to 4
— the grow/realloc path double-frees or frees an unallocated pointer
(stale capacity tracking, freed old buffer kept in a slice header,
manual free of a runtime-managed allocation). Audit every Box-owned
dynamic collection that grows on spawn connection: placed-piece arrays,
spool/ledger entries, refill-dot queues, per-spawn economy state.
Siblings to check: teardown/resplice return paths (piece returns to the
Box), and any `free`/`delete` on reslice.

## Method

1. Reproduce headlessly: script the repro in the sim/harness (connect 3
   spawns; the harness speaks scenarios). If headless doesn't trigger
   it, reproduce via app.bin under Odin's debug allocator
   (`-debug` build flags / ODIN allocator checks) to catch the invalid
   free AT THE CALL SITE with a real stack.
2. Fix the invalid free at its root (allocator discipline — no
   double-free, no freeing non-owned pointers; prefer runtime-managed
   growth over manual free/realloc).
3. Regression gate: a test/sim leg that connects >= 5 spawns across
   place/promote/teardown/resplice cycles — MUST crash (or fail the
   allocator check) RED before the fix and pass GREEN after
   (mutation-leg standard: the gate has to be able to fail).
4. Verify both user .ips signatures are explained by the root cause
   (same site or say why not).
5. Sweep the WHOLE Box surface for the same pattern (every manual free
   adjacent to growable state) — fix class-mates in the same PR, listed
   explicitly.

## Ops

- URGENT lane: the user is mid-playtest; fast correct beats slow
  perfect, but the regression gate is NOT optional.
- PR vs v2 (fresh head at dispatch), pr_review=1 (canon surface:
  economy/serialization semantics). check-pr-ready before close.
- CI billing-block signature (5s run / zero logs) = note-only; local
  gates are ground truth.
- bash 3.2 — no arrays in scripts.
- Perkins brief carries: crash reports paths, repro, this hypothesis.

## Skills policy

- `bmad-build` (step 04 review swarm MANDATORY).

## Model policy

- Minion: zai-coding-cn/glm-5.3-flash, --thinking max; mega-minions
  same pin.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-box-crash-third-spawn
- base: v2 (fresh head at dispatch — currently 396064b)
- model: zai-coding-cn/glm-5.3-flash --thinking max
- github_issue: (none)
- pr_review: 1
