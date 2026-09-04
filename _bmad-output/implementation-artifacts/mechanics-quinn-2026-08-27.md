# Mechanics Session Record — Quinn × Moses — 2026-08-27

**Job:** packet-plumber-v2-mechanics-quinn (interactive design conversation, read-only, no code)
**Persona:** Dr. Quinn (bmad-cis-agent-creative-problem-solver)
**Mode:** In-pane interactive rulings (P9 doctrine — idle-await contract)
**Subject:** Resource scarcity for routers/links; difficulty "hard but not too much"; chess-like decision quality
**Provenance note:** Quinn's original process died immediately after the opening turn (before any user answer); this session is the recovery — the recovered opening was re-presented verbatim, then all rulings flowed live.

---

## The diagnosis (shared frame)

Shipped v2 has a **one-sided difficulty ledger**: the react layer (congestion, QoS triage, crises, health) is fully burdened; the build layer is priced at zero (free routers, free pipes). The topology only asks "*where?*" — never "*whether?*" or "*which, at the expense of what?*". The user's instinct ("we shouldn't have unlimited routers and links") was ratified as a real structural hole.

The core contradiction named (TRIZ): **scarcity must bind the builder without taxing the tinkerer** — draw stays fluid (FORGE #2, not-Factorio), every draw costs something wanted elsewhere, Eras 1–2 stay calm (discovery curve sacred), no-soft-lock survives ("always available, never free").

Chess vocabulary adopted as the shared language: **material** (build stock), **tempo** (build order vs surge clock), **position** (topology + QoS, already shipped), **sacrifice** (teardown/refund).

---

## Rulings (in order)

1. **[ADOPTED 2026-08-27 user ruling]** — Failure feelings **1 + 2 + 3 together** (planning regret + build-order pressure + economic triage beside QoS triage), with **chess-like** decision quality. Reversibility explicitly accepted by the user as the safety net. (Ache 4, modernization squeeze, remains excluded — later-era seasoning at most.)

2. **[ADOPTED 2026-08-27 user ruling]** — **[I] The Box.** Discrete pieces, **no income**. Stock: routers + pipe units; tier-weighted pricing (illustrative: fiber 2/tile, standard 1/tile — superseded in form by ruling 6). Refills only at **era advance + score milestones**. Teardown returns pieces fully. Prices visible from the start, but Era 1 budget fat enough to be felt-not-counted. Rationale: chess is *allocation, not generation*; finite material between refills makes every draw weighty. Rollback ladder noted: Box → hybrid trickle → full meter (loosening).

3. **[ADOPTED 2026-08-27 user ruling]** — **[β] The Cap.** Each era sets a **stock ceiling**; milestone refills **restore to the cap**, never past it; era advance **raises the cap**. Banking structurally impossible; "spend it or it's gone" pushes commitment (chess temperament). Designer knows max material in play per era → the scarcity ladder and the difficulty curve become the same tunable curve. Supporting rule (**crazyhouse**): milestone = pieces-return moment; era = new-bigger-set moment.

4. **[ADOPTED 2026-08-27 user ruling]** — **[ii] Swap promotion, typed pieces.** The Box holds routers **by tier** (1G / 40G / 100G — knights-and-bishops grammar, not generic pieces). Upgrade = spend the higher-tier piece, **the lower-tier piece returns to the Box**. This materializes the GDD's "upgrade costs the tier delta" with zero arithmetic, and lifetime cost of place-cheap-then-promote equals place-big-first (no bait-and-switch). The promotion piece competes with new-site placement (router-side OR-choice). **You can only place tiers you hold** — flagged as the single biggest behavioral change vs shipped free tiering; ruled in with eyes open. Rollback ladder: free → swap (canon) → absorb-no-return (harsh).

5. **[ADOPTED 2026-08-27 user ruling]** — **[M4] Clock + Ledger ("gaining tempo").** Refill dots arrive on a **clock spine** (known worst-case schedule); **deliveries accelerate the next dot** (pull it closer), bounded by a floor and ceiling on the swing. Chess rationale: strong play earns *time*, not material. The Cap defuses snowballing (acceleration converts to timing, not dominance — can't refill past ceiling). No-soft-lock is structural: the clock floor is "always available"; acceleration is "never free."

6. **[ADOPTED 2026-08-27 user ruling]** — **[P2] Typed spools.** Pipe stock is **two spools — standard and fiber** — each counted in tile-units; drawing drains the matching spool 1/tile. **No cross-spool conversion**; teardown/resplice returns tiles to the matching spool. Zero arithmetic anywhere in the Box (matches router grammar; FORGE #2 tripwire respected). Cross-tier tradeoff preserved through scarcity of the fiber spool, not conversion math. New era dial: **spool mix per restore** (Era 1 mostly standard; Era 3 leans fiber).

7. **[ADOPTED 2026-08-27 user ruling]** — **[E3] Fat with authored brushes.** Eras 1–2 caps generous, but restore cadence tuned so an expansive builder **gently contacts the ceiling once or twice per Era-2 phase, under zero pressure**, each brush self-resolving as a dot lands moments later. Doctrine on record: **the first "no" must land on a greedy-but-safe player** — the brush is the economy's entire tutorial, learned by consequence in the diorama (same doctrine as QoS), no popup. Companion rule: **the squeeze is a slope, not a step** — Era 3's advance raises the cap generously; the bind arrives mid-era as demand growth outruns restore growth.

---

## The consolidated mechanism (one paragraph)

**The Box, capped per era, refilled by tempo.** The player holds typed pieces — 1G/40G/100G routers, standard/fiber spools — against an era-defined ceiling. Drawing drains spools per tile; placing costs a router piece of the chosen tier; promoting swaps pieces (lower returns); teardown returns everything (cannibalize-and-redeploy is always available, never free — the surge runs while you rebuild). Dots restore to cap on a known clock, accelerated by delivery performance; era advance raises the cap and shifts spool mix. Era 1–2: fat caps, authored gentle brushes, economy teaches itself. Era 3+: demand growth outruns restore growth; every draw is material off the board; the box starts saying no when it matters.

## Guardrails carried forward (binding on the heist)

- **FORGE #2 / not-Factorio:** the moment a player must do *arithmetic* (not glance) to place, the design has drifted. Counts small, prices integer, HUD glanceable.
- **No-soft-lock ("always available, never free"):** clock floor + full teardown refund + piece returns hold at every tuning. Never gate the floor on performance.
- **Discovery curve:** Eras 1–2 stay calm; economy lessons arrive as authored brushes, never as pressure.
- **LOOK ruling family:** calm-at-green must survive — scarcity should never make a healthy grid feel visually anxious.
- **Difficulty = the era ladder:** cap growth vs demand growth is THE calibration curve; no step-functions at era boundaries (slope inside the era).

## Rollback dial map (the user's "we can always roll it back", made concrete)

| Dial | Loose | Canon (current) | Tight |
|---|---|---|---|
| Economy breathing | Box (adopted) | — | hybrid trickle → full meter |
| Promotion | free | **swap** | absorb (no return) |
| Milestone diet | — | **clock+ledger** | pure clock (max determinism) |
| Pipe grammar | single pool (arithmetic) | **typed spools** | — |
| Era-1 sleep | fat & flat | **authored brushes** | subsidy (rejected: price changes break legibility) |

## Open questions → heist calibration material (NOT conversation-settled)

1. **Numbers:** cap sizes per era (routers by tier, spool units), dot cadences, acceleration floor/ceiling bounds, spool mixes per era.
2. **Brush tuning:** Era-2 brush frequency targets; ensuring first-"no" lands on greedy-safe play.
3. **Era-3 slope:** cap growth vs demand growth curves — needs sim calibration against the real ladder (1G/40G/100G) and spawn/estate growth (7.x).
4. **Ledger diet specifics:** what exactly counts as a "delivery" for acceleration (per-packet? per-SLA satisfied?); how bounds are exposed on the HUD.
5. **HUD/legibility design** (Sally's lane): typed-piece counters, next-dot progress, brush feedback, first-"no" moment framing.
6. **Migration/compat:** interaction with existing port caps and tier gating; what happens to in-flight saves with free-built unlimited webs.
7. **Crisis interaction (4.2):** does crisis performance feed acceleration? (Probably: crisis drops deliveries → dots slow — verify this doesn't create a death-spiral seam the floor must absorb.)
8. **Validation:** a mutation-leg-style gate for the economy (e.g., brush-frequency test, first-no timing test) so the tutorial-by-consequence is provable, not vibes.

## Session artifacts

- This record: `_bmad-output/implementation-artifacts/mechanics-quinn-2026-08-27.md`
- Ledger: `packet-plumber-v2-mechanics-quinn` (noted at close; no PR — conversation job, pr_review=0)
