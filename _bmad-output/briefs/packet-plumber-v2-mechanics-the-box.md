# Briefing: packet-plumber-v2-mechanics-the-box

Implementation heist — USER-AUTHORIZED 2026-08-27 ("go"), from the
ratified design record. THE RECORD IS YOUR SPEC — read it FIRST and keep
it open:
`_bmad-output/implementation-artifacts/mechanics-quinn-2026-08-27.md`
All 7 rulings are [ADOPTED user rulings]. You implement them; you do not
re-litigate them. Numbers are tuned against the sim, NEVER invented in
conversation.

## What you are building (the consolidated mechanism, from the record)

**The Box, capped per era, refilled by tempo.** Typed pieces — 1G/40G/
100G routers, standard/fiber spools — against an era-defined ceiling.
Drawing drains spools 1/tile; placing costs a router piece of the chosen
tier; promoting swaps pieces (lower-tier returns); teardown returns
everything. Dots restore to cap on a known clock spine, accelerated by
deliveries (floor+ceiling bounds); era advance raises the cap and shifts
spool mix. Era 1-2: fat caps, authored gentle brushes. Era 3+: demand
growth outruns restore growth — the box starts saying no when it matters.

## Staging (dependency order; staged commits, one PR unless it explodes)

- **L1 — The Box + The Cap (rulings 2+3):** typed inventory model, era
  ceiling, refills restore-TO-cap (never past), era advance raises cap +
  shifts spool mix, no banking, full teardown refund. Everything else
  hangs off this.
- **L2 — Placement + promotion grammar (rulings 4+6):** placing costs a
  piece of the chosen tier; only tiers you hold are placeable; promotion
  = swap (higher spent, lower returns); typed spools drain 1/tile, no
  cross-spool conversion, resplice returns to the matching spool. ZERO
  arithmetic anywhere (counts small, prices integer).
- **L3 — Refill diet (ruling 5):** clock spine + delivery acceleration
  with floor/ceiling bounds. The clock floor IS the no-soft-lock
  guarantee — never gate the floor on performance.
- **L4 — Era 1-2 sleep + authored brushes (ruling 7):** fat caps; brush
  cadence tuned so the first "no" lands on a greedy-but-SAFE player under
  zero pressure, self-resolving as a dot lands; Era-3 squeeze is a slope
  inside the era, never a step at the boundary.
- **L5 — Sim calibration pass (the record's open questions 1-4, 7):**
  cap sizes per era, dot cadences, acceleration bounds, spool mixes,
  Era-3 slope curves, delivery-definition for acceleration — TUNED
  AGAINST THE SIM HARNESS with the runs as evidence. Crisis interaction
  (Q7): verify crisis→slower-dots doesn't death-spiral — the floor must
  absorb it; prove with a sim run.
- HUD: MINIMAL glanceable layer only (typed-piece counters + next-dot
  progress — FORGE #2 requires glanceable). Sally's full legibility
  polish lane is a FOLLOW-UP job, out of scope; flag it in the PR.

## Guardrails — BINDING, copied verbatim from the record

- **FORGE #2 / not-Factorio:** the moment a player must do *arithmetic*
  (not glance) to place, the design has drifted. Counts small, prices
  integer, HUD glanceable.
- **No-soft-lock ("always available, never free"):** clock floor + full
  teardown refund + piece returns hold at EVERY tuning. Never gate the
  floor on performance.
- **Discovery curve:** Eras 1-2 stay calm; economy lessons arrive as
  authored brushes, never as pressure. No popups — tutorial by
  consequence (same doctrine as QoS).
- **LOOK ruling family:** calm-at-green must survive — scarcity must
  never make a healthy grid feel visually anxious. Existing look/palcheck
  gates stay green.
- **Difficulty = the era ladder:** cap growth vs demand growth is THE
  calibration curve; no step-functions at era boundaries.

## Gates — mutation-leg standard (record's open question 8 is mandatory)

- An **economy gate that can FAIL**: brush-frequency test, first-"no"
  timing test (the record names both) — delete-the-cap and mutate-the-
  floor legs must turn them RED, then GREEN.
- No-soft-lock pin: floor present at every tuning; mutating the floor
  away fails a test.
- Sim corpus: this is a MECHANICS change — sim/log bytes WILL change;
  re-bless per harness doctrine, disclose the re-bless inventory in the
  PR. Look/palcheck calm-board gates re-run green.

## Ruling discipline mid-heist

The 7 rulings are USER rulings. If one itches (design-level conflict
found in code), the path is: flag to Gru → user amends via the
mechanics-quinn record (pane stays open) → amendment relayed to you.
NEVER minion initiative on a ruling. The rollback dial map is for TUNING
within a ruling, not for reversing one. Saves/compat (record Q6): v2 is
a dev build — treat saves as disposable, build NO migration system, flag
the choice in the PR for the user to confirm.

## Skills policy

- `bmad-build` (step 04 review swarm MANDATORY — adversarial + edge
  hunters; never skip).

## Model policy

- Minion: zai-coding-cn/glm-5.3-flash, --thinking max. Mega-minions
  inherit the same pin.

## PR + Perkins

- pr_review=1 (gameplay canon surface: economy semantics, placement
  grammar). PR vs `v2`, staged L1-L5 commits.
- MEGA-DIFF protocol if the diff exceeds ~20k lines: local canonical
  diff + disclosure + chunked lens waves.
- `bin/check-pr-ready` before close-out; verdict posts as perkins-review
  bot. CI billing-block signature (5s run / zero logs / payments failed)
  = note-only, reruns useless; local gates are the merge ground truth.

## Constraints

- congestion-read-a1 (render lane) is in flight in a sibling worktree —
  your surfaces are sim/economy; do not touch render/look code beyond
  what the minimal HUD needs. Merge-order/rebase is Silas' call.
- bash 3.2 — no arrays in scripts.
- The tuned numbers + sim evidence live in the PR body (durable,
  Perkins-reviewable), mirroring how the record demands they be settled.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-mechanics-the-box
- base: v2 (Silas resolves the fresh head at dispatch)
- model: zai-coding-cn/glm-5.3-flash --thinking max
- github_issue: (none)
- pr_review: 1
