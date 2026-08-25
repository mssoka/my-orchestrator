Read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.2-ecmp/r1/_shared_header.md` first — it has your inputs, lens-guards, output contract, accuracy mandate. This file adds only your lens brief + output path.

LENS — SECURITY: OWASP-oriented review of the diff. NOTE the domain: this is a deterministic game-simulation routing module (`package core`, pure functions, no network/auth/secrets/IO/serialization of user input) — so the realistic surface is narrow. Still check: unsafe integer handling (overflow in `int(offset)+int(pick)` indexing `hops` — out-of-bounds read?), any input that reaches the hash unvalidated, any secret/credential/log leak, unsafe defaults, deserialization of untrusted data (there is none expected — flag if any appears). If the surface is genuinely clean, `[]` is the correct + honest answer.

Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.2-ecmp/r1/security.json` (source:"security"). Stop after writing.
