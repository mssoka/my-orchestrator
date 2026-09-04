# D3 — The engine bake-off record (why Odin won, what's changed since)

Sources: PR #13 body + `_bmad-output/design-analysis/odin-vs-godot-devils-advocate.md`
(durable), PR #15 body (the pivot architecture), FORGE #6 amendment (PR #16).
All read from disk this run.

## The record (2026-08-08 era)

1. **Godot was the LOCKED choice.** GL5.2 Godot architecture existed; a Godot
   prototype validated the surge slice (including an on-disk "unwinnable-house"
   bug that later shaped E31 spawn validity).
2. **PR #13 was an explicit devil's-advocate steelman of Odin — analysis, not a
   decision.** Four pillars: (1) determinism spine native in Odin, fought in
   GDScript; (2) server re-sim trivial vs aspirational in GDScript (finding m6);
   (3) it's a data-oriented simulation, not a scene graph; (4) PP doesn't need
   most of what Godot sells. The pivot enabler was the user's LLM-coding
   reframe ("LLMs code, so building-the-engine tax is removed").
3. **The doc's own final weighting TILTED BACK TO GODOT for the near-term
   launch** ("polish + Steam-first"): "Godot is the pragmatic launch tool;
   Odin (or the hybrid) is the architectural option to revisit when server
   validation + scale become real." Honest concessions: mobile, agent
   tooling/MCP, editor iteration speed.
4. **The USER overrode the tilt**: "ok.. let's move to Odin. let's own it end
   to end." → PR #15 pivot architecture (Odin dev-2026-08 + raylib 6.0):
   pure-Odin sim core (owned PRNG PCG32, integer-only, SOA pools), golden
   harness FIRST-CLASS (T1 hash goldens + T2 pixel goldens via the rlsw
   software renderer — bit-exact pixels, no GPU/display in CI), desktop-first
   (Steam), mobile deferred (Odin toolchain rough edges, odin-lang/Odin#6759).

## What the record got right (verified since, on disk)

- The determinism spine shipped AS SPEC'd: 50 demos, 148 goldens, T1 hash +
  drift gate + replay parity, all green in local CI tonight. The sim is clean
  under the crash — replay/box/econ suites pass; the bug is NOT in the sim.
- The harness-first doctrine is why the sim has ~2x its LOC in tests (22.7k
  test LOC vs 11.2k core) and why Perkins rounds could verify 5 rounds on #107.

## What the record UNDER-weighted (tonight's evidence)

- **Memory-safety discipline in the app layer was not a weighed axis.** The
  bake-off argued determinism, data layout, shipping, tooling — nobody priced
  "manual lifetime discipline across a 57-dynamic-field state tree, cloned by
  hand-maintained lists in a render predictor." That cost is now real and
  RECURRING (3 instances of the same class; tonight's shipped to the user).
- **The app layer's testability gap.** The pivot built a world-class SIM
  harness; the app-only surface (telegraph predictor, input effects, HUD
  strings, audio feed) has no headless leg — ~5,700 LOC run only under the
  user's cursor. The bake-off's "you don't need what Godot sells" skipped the
  fact that Godot's editor/tooling partially TESTS the presentation layer
  (scenes, signals, in-editor simulation), which Odin+raylib replaced with...
  nothing for app-layer effects.
- **The polish-loop concession was real but was absorbed**: PR #75 (Odin look
  polish to the MM bar) shows the loop CAN run on Odin — at the cost of a
  look-polish lane of jobs (sustained LLM effort replacing the editor).

## Arguing with the record honestly (for a re-open)

A re-open motion must claim one of:
(a) a PILLAR failed (determinism/sim fitness) — **tonight is NOT that**: the
    spine held; the crash is app-layer lifetime, which the bake-off never
    weighed on either side (GDScript's refcounting would have made the same
    bug unrepresentable — but so would a 20-line Odin guard);
(b) the LLM-coding reframe weakened (engine-ownership tax now exceeds LLM
    coding capacity) — partially arguable: the recurring clone-class + 232
    delete sites are exactly the "tax" the reframe claimed LLMs absorb, and
    an LLM DID write the bug AND miss it in 5 review rounds;
(c) the goal moved (mobile/editor/shipping-first again) — no evidence; the
    project is mid-v2 on desktop per FORGE #6 as amended.
