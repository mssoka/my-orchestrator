# packet-plumber-lang-safety-research — field notes (2026-08-28)

- Odin crash forensics: macOS libmalloc aborts lose the stack above
  `_heap_free` in the .ips — a -debug build + `breakpoint set -n
  malloc_error_break` under lldb recovers the full Odin stack in one run.
- READ-ONLY repro recipe that works: rsync the repo to /tmp (exclude
  _bmad), env-gate a frame-script driver in app/main.odin copying the
  PP_NOC_E2E injection pattern (append Device_Events after polls, before
  dispatch_frame) — drove real drag-connects and caught the box crash
  RED, then proved the 2-line fix GREEN (8 connects) same evening.
- Odin dynamic arrays carry their allocator in the header (lldb frame:
  mem_free_with_size reads it) — a missed field in shadow_clone alias-frees
  the LIVE buffers silently; the class is caught deterministically by
  core:mem Tracking_Allocator (bad_free_callback carries file:line), not
  by waiting for the abort.
