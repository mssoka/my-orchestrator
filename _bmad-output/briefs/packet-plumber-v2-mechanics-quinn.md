# Briefing — packet-plumber-v2-mechanics-quinn (interactive design conversation — NO code)

Skill to execute: **bmad-cis-agent-creative-problem-solver (Dr. Quinn)** —
FULL persona activation per the skill's steps (resolve customization →
activation steps → adopt persona → persistent facts → greet by name). Stay
in character throughout; the user chats with Quinn DIRECTLY in this pane.

## INTERACTIVE MODE (P9 doctrine — the law)

The user rules in conversation, in-pane. Present approaches as options with
your lean + why; record every ruling as `[ADOPTED 2026-08-27 user ruling]`.
Idle awaiting the user's answer = correct behavior — never answer for the
user, never run long monologues past a decision point.

## Summon reason (from the user, verbatim intent)

"interactive conversation about the game mechanics, how to make the fun
hard but not too much. especially relating to resources — we shouldn't
have unlimited routers and links."

## Context to ground the conversation (READ the GDD FIRST)

- `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`
  — esp: the **cost model** (§ "Cost model: drawing a pipe costs
  proportional to length × tier; upgrading costs the tier delta; full
  economy = full-game scope, MVP uses a simple budget/action cap"),
  **span limits** (distance/span per tier, junctions as repeaters), the
  **no-soft-lock escape** ("always available, never free"), the QoS
  **trade-off heart**, and the **discovery curve** (Era 1-2 calm → Era 3
  streaming surge forces triage).
- `project-context.md` + the shipped v2 reality: placement is currently
  FREE/unlimited (routers cost nothing, pipes cost nothing — only port
  caps + the real-ladder tiers + eras constrain). The GDD's economics are
  designed-but-unshipped.
- Balance state: `game/data/balance.json` (via the catalog loaders),
  demand caps (5.9), real-ladder 1G/40G/100G, crisis system 4.2,
  spawn/estate growth 7.x.
- FORGE locks (game pillars — read the forge dir's lock list; anything
  contradicting a lock is surfaced, not silently proposed).

## The conversation space (Quinn's map — not a quiz)

- Where the difficulty SHOULD live: the shipped game's tension is
  congestion/QoS; the user suspects RESOURCE scarcity (routers/links)
  should join it. Probe: what failure feeling are we buying — planning
  regret? Build-order pressure? Economic triage alongside QoS triage?
- Candidate mechanisms from the GDD + fresh: build budgets (per-era
  capital? income from SLAs?), per-tier costs, span limits, upgrade
  costs, maintenance/legacy decay, land/right-of-way limits, router
  count caps, opportunity-cost mechanics.
- The calibration question the user named: hard but not TOO hard —
  no-soft-lock must survive (the escape doctrine), calm-at-green must
  survive (the LOOK ruling family), and the discovery curve (Era 1-2
  stays a gentle diorama) must not be crushed by early scarcity.
- How any ruling would ride the era ladder (scarcity that grows with
  eras = the difficulty curve itself).

## Scope fence

- READ-ONLY: no code, no doc edits, no golden runs. This is a
  conversation; you may read anything in the repo for grounding.
- On conclusion (user says so / session naturally ends): write the
  session record — options explored, `[ADOPTED]` rulings, open questions —
  to `_bmad-output/implementation-artifacts/mechanics-quinn-2026-08-27.md`,
  then `ledger note packet-plumber-v2-mechanics-quinn <summary>` +
  `herdr notification show "packet-plumber-v2-mechanics-quinn" --body
  "session record written" --body` (verify shown:true). No PR.

## Model policy

- Minion: `zai-coding-cn/glm-5.3-flash`, `--thinking max`.

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: mechanics-quinn
- base: v2 (read-only; no branch, no worktree — in-repo conversation)
- model: zai-coding-cn/glm-5.3-flash
- pr_review: 0 (no code — conversation + session record)
