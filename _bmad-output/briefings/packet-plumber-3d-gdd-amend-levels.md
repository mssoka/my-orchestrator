# Briefing: packet-plumber-3d-gdd-amend-levels

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Amend the 3D GDD + epics for the levels-as-planets pivot** (user ruling,
2026-09-04). This is a DOCS-ONLY amendment to THIS repo's canon:
`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/`
(gdd.md, epics.md, decision-log.md — amend in place per the skill's update
flow; keep a supersede trail in the decision log).

**Scope guard: this repo ONLY.** No other project (PP-Odin included) is
read or touched. The 2D game's canon is not yours.

## The pivot (user rulings, verbatim)

- "Maybe we should have levels. so the eras could be levels. or eras could
  have multiple levels and the levels are other planets. like a rocketship
  takes them to another planet. I think that's cleaner than having to cramp
  multiple links into one map/planet."
- "So we have an era. and then levels within that era."
- "The first level would actually be sending the first message on the
  internet. like arpa."
- "Basically there is no qos, or link bundling at the first level. we then
  start adding techs and complexity as we progress."

## What the amendment must deliver

1. **Campaign structure in the GDD**: Era → Levels → Planets. Each level is
   its own tiny planet (bounded node counts, one clean idea per level);
   the rocketship is the progression fiction between planets. Motivation
   on record: clutter reduction + tiny-stays-beautiful + native fit with
   the little-planet aesthetic.
2. **Level 1 — ARPANET (1969), fully specified**: the four real nodes
   (UCLA, SRI, UCSB, Utah); draw the first link; send the first message —
   the historical beat: they tried "LOGIN", the system crashed after
   **"LO"** — the crash is the level's scripted first crisis. No QoS, no
   bundling, no classes: one link, one packet, one target.
3. **Tech-unlock ladder**: map every existing mechanic (pipe tiers,
   parallel bundles, packet classes, QoS lanes, SLA tracking, crisis
   types, node types) to the level/era where it UNLOCKS. E2's systems are
   the engine; levels gate which mechanics are live (data-driven flags,
   canon already supports subsets). The ladder is the onboarding spine —
   roughly one new mechanic per level.
4. **Historical era ladder (sketch)**: email (1971) → TCP/IP → DNS → the
   web → streaming era → …; each era = a planet cluster, each level one
   clean beat. Sketch through the E1–E9 MVP window; mark post-gate eras
   as content.
5. **Epics reconciliation**: E3 (topology/growth) reshapes into
   level-design + planet variety; E5 (eras) becomes the campaign spine;
   E6 (win/lose) becomes per-level targets + era finales. E1/E2 already
   built = the engine (mark them "done, engine" in the matrix). Keep the
   fun-test gate doctrine, determinism, pause-and-plan, accessibility,
   no-rebuild.
6. **Decision log**: the pivot rulings verbatim + what supersedes what
   (single-map sprawl → campaign; complexity-at-start → unlock ladder).

## Gate

**Lavish review BEFORE the PR opens** (standing DOCS policy): present the
amended GDD/epics as a lavish session — the user rules the campaign
structure, the ARPANET level, and the tech ladder in-page. Apply
annotations, then open the PR.

## Environment notes

- Base: origin/main @ 674bda8 (E2 merged — the sim exists; reference it
  as the engine the ladder unlocks into).
- The USER is refreshing `_bmad` in the main checkout around now — if
  skill/config reads look odd mid-flight, wait a beat and re-read.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`** (natively multimodal — the
little-planet reference frames remain the look canon).

## Skills policy

Workflow: **`gds-gdd`** (update/amend flow) + **`gds-create-epics-and-stories`**
(epics reconciliation). **`lavish`** for the review gate.

## Perkins

`pr_review=0` — docs/lavish deliverable; the lavish loop is the review.

## Dispatch parameters

```
job_id:    packet-plumber-3d-gdd-amend-levels
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      gdd-amend-levels
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 0
notes:     Worktree from origin/main (674bda8). _bmad symlink bootstrap
           (user may be refreshing the main checkout's _bmad — benign).
```
