# Lens: Security (Perkins r1 — packet-plumber-v2-2.1-bundles)

OWASP-oriented security review of the diff. This is a **single-player offline puzzle game in Odin/raylib** (no network endpoints, no auth, no DB, no user-uploaded content in this change) — calibrate your expectations. Still check:
- Any new input parsed without validation at a system boundary
- Unsafe integer arithmetic that could overflow/wrap into a security-relevant state (index OOB → OOB read/write, signedness confusion)
- Deserialization/log-format issues (the action log is little-endian binary — ODN-11)
- Secrets/tokens/credentials handled unsafely (none expected; flag if present)
- Unsafe defaults, missing bounds, array index derived from untrusted-ish input
- Any path/command/asset injection vector introduced

## Inputs
- **Diff:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/diff.patch`
- **Worktree (verify here):** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.1-bundles-r1`
- **Context:** `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-2.1-bundles-r1.md` (lens-guards) and worktree `project-context.md`.

## ⚠️ Lens-guards (prevent false positives)
- This is an offline single-player game. There are **no auth/authz/CSRF/session/network surfaces** in this diff — do not invent them. Flag only what the diff actually introduces.
- Integer widths (u32/u16) are deliberate (ODN-10 integer-only sim). A genuine OOB index (e.g. indexing `pipe_bundle`/`bundle_*` past their length) IS worth flagging; a mere u32↔int cast that stays in range is not.
- `NO_BUNDLE`/sentinel patterns are intentional, not "magic number" smells.
- Do not flag the no-LB design, the derived/serialized bundle state, em-dashes, or the `v2` base.

## OUTPUT
Write ONLY a valid JSON array to: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/security.json`
Schema:
```
{ "source":"security", "severity":"blocker"|"warning"|"note", "category":"<tag>",
  "title":"<one-line>", "location":"<file:line|hunk|N/A>",
  "evidence":"<exact lines READ from worktree/diff, verbatim>",
  "detail":"<≤40 words>", "recommended_fix":"<≤40 words>" }
```
ONLY the JSON array in the file. `[]` is valid and LIKELY (offline game, small diff) — accuracy > volume. When done: "security lens done — N findings".
