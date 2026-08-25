# Lens: Architecture (Perkins r1 — packet-plumber-v2-2.1-bundles)

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (core vs app vs harness; ODN-1)?
- Will it create technical debt or make future changes harder (esp. for stories 2.2 ECMP and 2.3 demolish)?
- Does complexity match the problem? Any premature abstraction?

## Inputs
- **Diff:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/diff.patch`
- **Worktree (verify here — read the surrounding core/*.odin to judge fit):** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.1-bundles-r1`
- **Spec/context:**
  - `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-2.1-bundles-r1.md` (lens-guards)
  - Worktree `project-context.md` (ODN-1/9/10/11/13/14/18; layered architecture)
  - Worktree `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` — esp. **ODN-1** (core purity), **ODN-10** (no map iteration; integer-only; forwarding table rebuilt on topology-change), the **4-rule spine** (~lines 643–690), §6.1/§6.2 topology+routing, and the `pipe_lb_mode` PROTO→FULL deletion note (~line 860).

## Architecture invariants to check (these ARE the spec — flag violations, not compliance)
- **ODN-1:** `core/` imports only `core:*`; no `vendor:*`, no `core:os`/`core:time`, no raylib. `bundles.odin` is in `package core`.
- **ODN-10:** no `map` iteration in core (arrays/slices/`#soa` only); integer-only sim math; ties → seeded rng.
- **Derived-view discipline:** the `Bundles` struct should be a pure derived view over `Topology`, rebuilt on topology-change (gen bump) exactly like the routing table — NOT serialized, NOT rebuilt per-packet/per-tick.
- **Layering:** the view (`app/render`) and harness must NOT mutate sim state; they read derived bundles via pointer.
- **No LB:** the routing/flow must consume the bundle as one pooled edge, no round-robin/weighted per-pipe pick.

## ⚠️ Lens-guards (DO NOT flag — these are correct by design)
- **The Bundles struct being DERIVED (rebuilt, not serialized) is the architecture** — mirrors the routing table. Do not flag "should serialize bundles" or "should persist bundle_gen."
- **NO LB is the locked model.** Pooling is correct. (A stray LB mechanic sneaking in WOULD be a blocker.)
- **`Packet.edge` = representative pipe id** is by design.
- The **2.3 severance** concern is a documented carry-forward for story 2.3, not a 2.1 defect. But if you see the design making 2.3 needlessly hard (a legitimate forward-looking note), that's a `note`, not a blocker.
- Don't re-open 1.1–1.4; don't flag em-dashes / the `v2` base.

## OUTPUT
Write ONLY a valid JSON array to: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/architecture.json`
Schema:
```
{ "source":"architecture", "severity":"blocker"|"warning"|"note", "category":"<tag, e.g. coupling, layering, debt>",
  "title":"<one-line>", "location":"<file:line|hunk|N/A>",
  "evidence":"<exact lines READ from worktree/diff, verbatim>",
  "detail":"<≤40 words>", "recommended_fix":"<≤40 words>" }
```
ONLY the JSON array in the file. `[]` is valid. Accuracy > volume. When done: "architecture lens done — N findings".
