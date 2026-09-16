# Briefing: pp3d-game-shell-1 — title/boot flow, era-planet level select, scores, persistence, pause, crash freeze, arrows

## Context

Full design consult completed with the user (2026-09-15/16, plan-before-heist
ruling honored — every fork below is USER-RULED). The world model is LOCKED:
**Era = planet identity; Level = a fresh instance of that era's planet, one
scenario.** Connections reset per level; replay any completed level; era/level
N+1 locked until N complete. Eras run 2-4 levels; live per-level thumbnails;
one-off worlds are "eras of size 1" (future, e.g. DTN moon). The GDD's
continuous one-planet run stays vaulted as a future endless mode — do NOT
implement it now. A short canon note (docs/) records the model (small
targeted doc edit, no lavish).

Platform canon: PC + mobile + TV/console EQUALLY. Hold regime: glm-5.3 @ max.

## Workstreams (all user-ruled)

### WS1 — Title screen + boot flow
- Boot → **Title screen**: game title + **PLAY** (console "press any button"
  wake norm acceptable), minimal. Once a save with progress exists: PLAY
  becomes/reorders to **CONTINUE** (deep-drops into the current/next
  incomplete level) with **LEVELS** beside it. Settings placeholder NOT built
  (future). One save slot, no profiles.

### WS2 — Level select home (the era-planet page)
- The LEVELS page groups by **era**: one slowly-rotating planet thumbnail per
  era (Earth-rotation feel — gentle, looping), levels listed within.
- **Thumbnails are LIVE renders** of the actual level worlds (SubViewport of
  the real level planet at its manifest seed) — same era palette shared,
  each level tile showing its own scenario (sites, lit state). No bespoke
  thumbnail art.
- Today's content: **Era 1 group with L1 (unlocked/complete state per save)
  + a locked "LEVEL 2" slot** (dim, lock glyph, gated until L1 complete —
  and its content is future work regardless). No further placeholder slots.
- Selecting a level → its scene (fresh instance, connections reset).
- Controller/touch/mouse parity throughout (focus navigation, tap targets).

### WS3 — Level-complete flow (replaces FLY ON)
- On win: **score panel** shows the level's stats prominently (packets
  carried · links up — the existing stats; a real scoring system is a
  separate future issue, do not invent one).
- Two choices: **HOME** (to the level select) and **NEXT** (proceeds to the
  next incomplete level; disabled/hidden-with-reason when none exists — for
  L1 now, HOME is the path).
- **REMOVE the FLY ON button, the fueled-rocket graphic, and the "Next
  planet" teaser text** — the rocket-hop metaphor is retired canon.

### WS4 — Persistence
- Save to the user data dir: completed levels (per era), era/level unlock
  state, best stats per level. One save slot. Survives restart (probe it).
- Corrupt/missing save = clean start, never a crash (fail-safe load).

### WS5 — Pause (Mini Motorways semantics, user-researched) + LO-crash freeze
- **ONE "network suspended" machinery powers both pause and the scripted
  LO-crash freeze** (build once, use twice).
- **Pause**: network time stops (packets halt in place, queues freeze);
  **ambient life keeps breathing** (deer/sheep/dolphins/clouds animate on);
  **building/editing connections stays LIVE while paused** (MM semantics:
  plan and build with time stopped). Resume on the same input.
  - Inputs: keyboard conventional (Space), controller conventional
    (Start/Options per platform conventions — mapped action, not a literal
    button index), touch = a pause affordance consistent with the HUD zone
    map (device-parity; keep it clear of the top-right scores cluster).
  - Paused state is clearly indicated (subtle, not a modal wall).
  - Auto-pause at decision moments = FUTURE candidate, not built now.
- **LO-crash freeze (user playtest bug)**: when the first transmit fails,
  packet motion HALTS DEAD — the stalled LOGIN letters freeze in place (no
  crawl/jitter), nothing moves in the cables; motion resumes ONLY on
  RETRANSMIT. Ambient life continues (world alive, network died).

### WS6 — Arrow keys (dual binding, GUI-focus-wins)
- Arrows join WASD as **camera orbit** when no GUI element holds focus.
- When a card/menu/button holds focus, arrows **navigate the highlight**
  (LEFT/RIGHT already cycle; extend naturally with UP/DOWN) — GUI focus
  wins, identical grammar to Enter (gh-39). No context where a key does
  both at once.

## Acceptance

1. PR vs origin/main (base `main`, pr_review=1). Playable b43 export from
   the FINAL branch tree, central-preserved, WITH the codified export
   contract: named-asset containment hash + boot receipt (stderr clean)
   BEFORE Start.command ships.
2. Discriminators (probe-first, fails-pre-fix receipts), EXPECTED_CHECKS
   triple, mutation legs RED-then-GREEN:
   - pause: packets frozen (position-pin across frames) while ambient nodes
     animate (position-pin shows motion); build verbs live during pause;
     fails pre-fix;
   - LO-crash: stalled letters' screen positions pinned dead post-crash;
     zero packet motion until retransmit; fails pre-fix;
   - arrows: camera moves on arrow input with no GUI focus; highlight moves
     (camera does NOT) when a card owns focus; fails pre-fix;
   - level select: locked LEVEL 2 unlaunchable by any input; L1 relaunch =
     fresh instance (no carried connections); fails pre-fix;
   - persistence: unlock state survives a quit/restart cycle (probe with a
     temp user dir); corrupt save fails safe; fails pre-fix;
   - FLY ON/rocket/teaser: grep-pinned absent from scenes + code paths.
3. Captures under the bounded-run grant terms (headless ≤300s standard,
   ~900s windowed captures with caffeinate -dimsu + awake screen,
   receipt+hash per entry, quiescence, stop-on-surprise): title → levels →
   L1 flow; completion panel; pause with frozen packets + living ambient;
   crash freeze → retransmit resume.
4. No scope creep: no era-2 art, no scoring system, no settings page, no
   endless mode. L1 gameplay itself unchanged beyond the completion flow.

## Skills policy

- Workflow: `bmad-build` (the upstream replacement for bmad-quick-dev,
  removed 2026-08-20 in 585166c0; renders via the repo facade
  `_bmad/scripts/render_skill.py`).
- Review layers (bmad-build step 04): `bmad-review` (adversarial lens) +
  `bmad-review-edge-case-hunter`.

## Model policy

Hold regime: `zai-coding-cn/glm-5.3` @ max. Look verdict = user play on b43.

## Dispatch parameters

- repo: packet-plumber-3d
- repo_root: /Users/moses/code/packet-plumber-3d
- slug: pp3d-game-shell-1
- base: origin/main @ fdd2634
- model: zai-coding-cn/glm-5.3 @ max
- pr_review: 1
- PR base branch: main
