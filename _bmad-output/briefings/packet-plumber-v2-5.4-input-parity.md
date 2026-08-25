# Briefing — packet-plumber-v2-5.4-input-parity (story 5.4 — touch + controller parity)

- **Job id:** `packet-plumber-v2-5.4-input-parity`
- **Repo:** packet-plumber · **Base:** `v2` @ post-#53/#54 merge head (Silas resolves the
  exact sha at dispatch; journal base pull recorded @ e7fa548) · **Slug:** `v2-5.4-input-parity`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (gameplay + canon surface — ODN-12 input contract, FORGE #6).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.4-input-parity <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 5.4
  (relative to `/Users/moses/code/packet-plumber`). Read it + `sprint-plan-v2.md` §5.4
  row BEFORE designing.
- **CI:** green. Full local suite must pass.

## Mission — implement story 5.4 (touch + controller parity via the intent layer)

**The goal:** the same game on touch + controller, via an **intent layer** — new device
mappings onto the same intents, parity by construction `[FORGE #6]`. The story card's
Given/When/Then: touch (drag-draw, tap-select, two-finger pan) + controller
(node-select, aim/confirm, tier/class cycling) produce **the same Command shapes as
mouse** `[ODN-12]`. Landscape-only framing is a camera-fit decision (desktop-first
launch) `[§18 OQ-1]` — you are NOT shipping mobile; you are making the intent layer
so mobile stays additive.

**Current state (investigate first, don't reinvent):** raw raylib input is handled
directly in `app/main.odin` — `rl.IsKeyPressed` / `rl.IsMouseButtonPressed` /
`rl.IsMouseButtonReleased` / `rl.GetMouseX/Y` at the call sites (placement, drag,
release-based click-select "node → pipe → clear", demolish X/DELETE, lane keys
E/S/B via `set_lane_key`, ESC/RIGHT cancel). There is **no intent layer yet** — this
story introduces the `raw device event → Intent → validated Command` seam the
architecture's ODN-12 row specifies (`core:types`/`core:step` Command surface is the
validated boundary; snap-to-node happens in the bus, i.e. the intent stage, not the
core).

**Hard requirements (all pinned by the card):**

1. **Intent layer + mappings.** One intent stage: raw raylib device events → typed
   `Intent` → validated `Command`. Mouse is the first mapping and must preserve the
   current behavior EXACTLY (no regressions to placement/drag/click-select/demolish/
   lane keys — the 5.5 story depends on the release-based click-select surface).
   Then touch mappings (drag-draw, tap-select, two-finger pan) and controller
   mappings (node-select, aim/confirm, tier/class cycling) onto the SAME intents.
   Parity is BY CONSTRUCTION: all three devices feed one validated-command path —
   there is no per-device command production to drift.
2. **T1 golden — same Command stream across inputs.** The harness must prove
   mouse/touch/controller produce identical Commands. Feed **scripted (synthetic)
   device-event frames** through each mapping — the T1 test does NOT need a physical
   touchscreen or gamepad; it drives the mappings with recorded event streams and
   asserts the emitted Command sequence equals the mouse's. (Physical-device
   validation is manual/optional — note it in the PR if you tried a controller.)
3. **Determinism discipline (the family spine).** The intent layer lives in the
   presentation side; the core sees only validated Commands as today. Inputs are
   never serialized — the action log records Commands, unchanged → **no `LOG_VERSION`
   bump**, replay byte-identical `[E10]` (prove it in the PR body: a replayed run
   shows the same action stream). No wall-clock, no randomness in the mappings.
4. **Existing suite unshifted.** All existing tests + goldens pass unchanged. New
   T1 across-inputs golden added. Any T2 change (e.g. on-screen input hints) is a
   DELIBERATE fold, listed in the PR.

**Acceptance:**

1. Card's Given/When/Then verified: touch + controller Commands == mouse Commands
   (pinned by the new T1 golden); landscape framing handled per `[§18 OQ-1]` (a
   camera-fit decision — if it needs camera work, FLAG it in the PR, don't build it).
2. New T1 golden across inputs; existing suite unshifted; full local suite green.
3. PR body carries: the intent-layer shape (types + stage home), the mapping tables
   (device → Intent → Command for all three devices), the parity-by-construction
   proof, the no-LOG_VERSION proof, citations `[ODN-12]` / `[FORGE #6]` / `[§18 OQ-1]`.
4. Story card status line updated in the same PR (the established pattern).

**Scope guard:** input parity ONLY. No new mechanics, no balance changes, no rendering
overhaul beyond input affordances, NO mobile/toolchain work (desktop-first launch per
the 2026-08-08 lavish ruling — the intent layer's whole point is that mobile stays
additive, not that it ships here). No GDD/canon changes unless a mapping forces a
one-line decision-log note.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.4-input-parity
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
