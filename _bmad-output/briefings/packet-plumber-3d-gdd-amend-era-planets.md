# Briefing: packet-plumber-3d-gdd-amend-era-planets

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Amend the GDD's Campaign Structure: planet per ERA (area), not per level**
(user ruling, 2026-09-05 — "B"). Levels refresh the same planet. This is a
**substantial canon change** (Campaign Structure + Core Concept rewrites)
→ **lavish review BEFORE the PR opens** — the user rules the shape in-page.

## The ruling (user discussion, verbatim anchors)

- "What do you think about… each area will be a different planet instead of
  each level being a different planet."
- "For each level we just refresh the existing planet — so level 2 will
  start afresh, we say congratulations we finished level 1, something along
  those lines, and then we say level 2: refresh map with nodes spawning."
- Gru's comparison was presented (planet-per-level vs planet-per-era);
  the user ruled: **"B."**

## What changes in the GDD

1. **Structure:** **Era = one planet** (the era's world — rich biomes, deep
   character, ~6 planets across the MVP window instead of 14 thin ones).
   **Level = a refresh of that planet**: fresh map seed, nodes spawning per
   the authored script, new wedges/mechanic-nodes unlocking where the
   level's new idea lives. "Level 2 — the network grows."
2. **The between-level beat:** the refresh card ("Congratulations — the
   network grows" → fresh map, nodes spawning). **The rocketship = the ERA
   transition** (cluster launch at era finales) — rare enough to thrill.
3. **Historical resonance (on record as motivation):** the internet is ONE
   network that grows — L1's four nodes → L2 spawns new sites on the SAME
   planet (what ARPANET actually did); the era finale's launch = the
   cutover to a new epoch.
4. **Level manifest framework gains:** era-planet identity + refresh delta
   (spawn script, unlocked wedges/mechanic nodes) as manifest fields.
5. **Untouched (say so explicitly):** bounded node counts per level ·
   one-clean-idea-per-level · per-level determinism (seed + authored
   script) · cumulative traffic (D5a) · the tech-unlock ladder ·
   **L1's spec is IDENTICAL under both models** (state this; the in-flight
   L1 job is unaffected).
6. Sweep the document for level-per-planet language: Core Concept ("each
   level is its own small, hand-holdable planet" → era-phrasing; "a pocket
   full of worlds" → "a pocket of worlds you know"), USP #3, the Why-
   levels-as-planets motivation, Campaign Structure (Era → Levels →
   Planets), the rocketship paragraph, Win/Lose's "the rocketship waits,"
   the era ladder table framing, epics.md's E5/E10 cells as needed.
7. **Decision log:** the B ruling verbatim + the comparison presented +
   the supersede chain (2026-09-04 campaign ruling's per-level clause →
   2026-09-05 era-planets ruling).

## Gate

**Lavish BEFORE PR**: present the restructured campaign canon in-page
(the new structure diagram/table + the refresh beat + what's untouched);
apply the user's annotations; then open the PR.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`** (natively multimodal).

## Skills policy

Workflow: **`gds-gdd`** (update) + **`lavish`** (the gate).

## Perkins

`pr_review=0` — docs/lavish deliverable.

## Dispatch parameters

```
job_id:    packet-plumber-3d-gdd-amend-era-planets
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      gdd-amend-era-planets
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 0
notes:     Worktree from origin/main. _bmad symlink bootstrap. PARALLEL
           LANE: l1-arpanet (code) — docs vs code disjoint; L1 spec is
           identical under the new model (briefing states it).
```
