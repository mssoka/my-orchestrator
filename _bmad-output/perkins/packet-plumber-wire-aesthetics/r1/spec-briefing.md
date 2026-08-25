# Briefing — packet-plumber-wire-aesthetics (canon: wire routing + junction shaping)

- **Job id:** `packet-plumber-wire-aesthetics`
- **Repo:** packet-plumber · **Base:** `v2` @ post-background-maps + post-5.12
  merge head (HELD — Silas resolves the exact sha at release; see the hold note
  below) · **Slug:** `wire-aesthetics`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-background-maps` merge close-out AND the
  `packet-plumber-v2-5.12-aggregation-groups` merge close-out (both landed —
  the map and the estates placement this job composes with). Record the hold on
  the row.
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — mechanical
  render work; the aesthetic verdict is the USER's at the lavish gate, no
  native-vision dependency). Any mega-minion you spawn launches with the same
  model — name it explicitly at every spawn.
- **Skills policy:** `gds-quick-dev` (view-layer work);
  **`lavish` is MANDATORY — present the wire/junction styles for the user's
  in-browser verdict BEFORE the PR** (side-by-side routed-vs-straight on a real
  busy map; iterate on annotations). `project-context.md` for code conduct.
- **Perkins:** `pr_review: 1` (every-frame view surface + possible cost-rule
  interaction). **Loop ruling (user, 2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-wire-aesthetics <url>` yourself.
- **CANON CONTEXT:** the approved light-canvas language (7.1: tier-band pipes,
  two-tone roofs, flat-MM); look-book D9 map (background-maps job); 5.12 estate
  placement. This job is the third layer of the bird's-eye picture: the WIRES.
- **Lane note:** this is view-lane; if slice-6 era work is in flight at
  release, files stay disjoint (era = core+catalogs) — note the T2 handshake
  both ways per the 4.3 discipline.
- **CI:** billing-blocked GH Actions — the LOCAL suite is ground truth;
  `tools/ci-local.sh` (10 gates incl. palcheck) must pass.

## Mission — implement wire aesthetics (routing that avoids ugly crossings + junction shaping)

**The goal (user ruling 2026-08-17 night, "want it"):** the network LOOKS
engineered, not scribbled — (1) pipe draw-paths subtly detour to avoid
crossing other pipes and clipping nodes; (2) routers present well: anchors
spread evenly around the disc, bundles render as ONE ribbon that fans open at
each end. Presentation-only, deterministic, no gameplay change.

**Hard requirements:**

1. **PIPE ROUTING (view-only detours).** The drawn path from A to B may bend
   (rounded-corner or bezier detours per the 7.1 tier-band language) to avoid:
   crossing other pipes (prefer sliding alongside), clipping node/terminal
   sprites, hugging the map edge. The GRAPH is unchanged — connect/anchor/cap
   semantics identical. Deterministic from topology (same map → same paths,
   seed-independent where possible, seed-derived only if unavoidable — document
   which).
2. **COST RULE IMMUNITY (the load-bearing guard).** Pipe cost = length × tier
   measured on the LOGICAL segment (straight A-B geometry) — the drawn detour
   must NEVER change what the player pays or any gameplay value. Pin it: a
   test asserting identical costs/simulation for identical topology regardless
   of routing changes; T1 state-hash + replay byte-identical `[E10]`.
3. **JUNCTION SHAPING.** Router anchor points allocate angles evenly around
   the puck (n pipes → clean spread; the 4-pipe ✕/＋ reads at a glance);
   bundles (parallel pipes, node-pair) render as ONE ribbon that fans open at
   each end — capacity-scaled width per the 7.1 tier bands.
4. **Graceful degradation.** When a detour would be longer/uglier than the
   crossing (small maps, dense cores), prefer the STRAIGHT line — the router
   must not zigzag into absurdity; name the threshold heuristic (data-driven
   if tunable). Edge cases: crossing is sometimes the RIGHT look (terminal
   stubs); demo maps must stay readable.
5. **LAVISH GATE (before the PR):** side-by-side routed-vs-straight on a real
   busy map moment (5.12 estates + a dense core) + junction close-ups (anchor
   spread, ribbon fan). The user picks/annotates; iterate until an explicit
   approve. HARD GATE.
6. **Goldens.** Full T2 re-bless — deliberate, cause-documented; T1 + replay
   byte-identical (prove both in the PR).
7. **Canon fold:** add §Story 7.5 (wire aesthetics, slice-7 view lane) + a
   decision-log note (user ruling: "lean on nice aesthetics") in the same PR.

**Acceptance:**

1. Lavish verdict recorded verbatim in the PR body (the approved style is what
   shipped).
2. Cost-immunity + determinism pins green; T1/replay byte-identical;
   `tools/ci-local.sh` 10/10.
3. PR body: the routing algorithm (detour heuristic + degradation threshold),
   the anchor-allocation scheme, the ribbon rendering, the re-bless cause
   chain, citations (7.1 gate verdict + look-book).

**Scope guard:** wire DRAW aesthetics ONLY. No gameplay rule changes (FORGE #2
redesign-freedom untouched — crossings never punished), no core/sim changes,
no new node/terminal art, no map changes (background-maps owns the terrain).
If the routing wants terrain awareness (rivers), that is a named follow-up —
FLAG, don't build.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: wire-aesthetics
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
