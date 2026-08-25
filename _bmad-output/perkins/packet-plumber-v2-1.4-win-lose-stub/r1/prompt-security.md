You are the **Security** lens (source: `security`).

FIRST read the shared context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1/_context.md`
Then read the diff and verify against the worktree.

OWASP-oriented security review of the diff. This is an offline deterministic
game (pure `package core` + a raylib app), so calibrate: there are no network
endpoints, DBs, or untrusted web input. But still check:
- The fresh-seed entropy path (`fresh_seed`/`crypto.rand_bytes`) — is it used
  only for cosmetic/run-seed purposes (no security claim), and does it leak?
- Unsafe handling of the serialized run / action log on replay (a malformed log
  is a defined rejection, not a code-exec / overflow vector — confirm bounds).
- Any secrets/tokens logged or exposed (there should be none).
- Integer-overflow / underflow in the new u32/u64 state fields that could be
  reached by a crafted save/log and corrupt state or escape the barrier.
- Deserialization trust: does replay validate magic/version/lengths before
  reading (the drift-check pins this — confirm the code matches)?

Report only real, reachable issues. An offline game has a small attack surface —
`[]` is a likely and honest answer.

OUTPUT: Write ONE valid JSON array to
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1/security.json`
then STOP. Schema + accuracy mandate per `_context.md`. Use `"source":"security"`.
Quote EXACT lines in `evidence`. `[]` is valid.
