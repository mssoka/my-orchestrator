# Field notes — packet-plumber-v2-5.7-runtime-telemetry

- 2026-08-14: Odin `-define:PP_DEBUG=true` flips `when #config(PP_DEBUG, false)` — verified
  with a compile probe before building the gate; the harness/app overlay gate rests on it, and
  the plain harness build carries ZERO overlay bytes (goldens can't shift by construction).
- 2026-08-14: temp-allocator trap in a stats-pin verb — `fmt.tprintf` paths passed as a deferred
  write target get recycled by the harness's per-tick `free_all(temp)` → garbage paths. Deferred
  write paths must be `fmt.aprintf` (default allocator) + deleted.
- 2026-08-14: per-tick stats derivation must read the per-tick drop-site scratch (drop_sites)
  right after step — it's cleared at the TOP of the next flow_step, so a paused-wall-tick record
  would be a lie; the stream emits per STEPPED sim tick, which is also what keeps live == replay
  (pause schedule is run setup).
