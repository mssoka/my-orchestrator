# Lens: security (Security) — Perkins r1

**OUTPUT FILE:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/security.json`

First read the common context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/_lens_common.md`

## Your lens
Security review of the diff. This is a single-player offline game simulation
core (Odin) — there are no network endpoints, auth, or untrusted input at this
layer. Calibrate accordingly: real findings here would be things like
- Unsafe parsing of the demo file (`harness/demo.odin`) that could read
  out-of-bounds / crash on a malformed `.dem` (the harness reads demo files from
  disk — a corrupt demo is the closest thing to untrusted input)
- Integer overflow in the new u32/u64 math (`need = n*n`, `progress_units`,
  `next_packet_id`) that could wrap to a dangerous value
- Any path that could read/write out of bounds in the new arrays (`r.next[idx]`,
  `f.packets[i]`, the BFS scratch arrays sized `[n]`)
- The replay/log path (`log_read`) accepting a hostile binary without the
  defined rejection

If nothing applies (likely — this is a pure sim core), return `[]`. Do NOT
invent OWASP web findings that don't map to this code.

## Output
Write ONE valid JSON array to your OUTPUT FILE (source = `"security"`). `[]` is
valid and expected here. Accuracy > volume. Then print `LENS DONE: security`
and stop.
