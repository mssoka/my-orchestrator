Security review of the diff. This is a deterministic offline Odin game sim (no network, no user-supplied secrets, no DB) — adapt the OWASP lens to what actually exists here:
- Input validation at system boundaries (demo file parsing — the harness `place` verb: string parsing, bounds, integer parse failures, allocator lifetimes / string clones)
- Binary log deserialization safety (log_read: length-prefixed records, bounds sanity, version/era/tag rejection, truncation/trailing detection, allocation bounds before make)
- Unsafe deserialization / malformed input handling in the action log reader
- Index-out-of-range risks in new code (tray chip indices, catalog type_idx lookups, rts buffer bounds, tile coords)
- Denial of service / resource exhaustion via malformed demo files or logs (huge counts, huge coords, integer overflow in apply_tick math)
- Integer overflow in new arithmetic (apply_tick = at_ms*hz/1000, sep2 = 7*7, span math, tray layout math)
- Anything that could crash, panic, or corrupt state from untrusted-looking input (demos are repo-owned but the log reader is a replay gate — malformed logs must reject cleanly, never panic)
Only report real, code-anchored issues. This is not a web app — skip web-specific checks that don't apply.
