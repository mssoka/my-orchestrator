# Briefing: packet-plumber-sprint-replan-v2

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`, base `main`).
- **Deliverable:** a **from-scratch, vertical-slice Sprint Plan v2** (+ stories-v2) that supersedes the horizontal sprint-plan-v1. **DOCS deliverable → lavish review loop BEFORE the PR opens.**
- **Model:** `zai-coding-cn/glm-5.2` (kimi down; sprint planning is capable-tier design work — glm-5.2 produced v1).
- **Perkins:** OFF (`pr_review=0`) — docs. Review surface = lavish.
- **Skills:** **`gds-sprint-planning`** (the re-plan workflow) + **`lavish`** (REQUIRED — serve the plan, foreground-poll, iterate before PR). Read the lavish playbooks first.

## Mission — why

**Decision (user): build Packet Plumber from scratch.** The merged prototype (#17) is buggy and crash-prone; rather than patch it, we rebuild clean. The prototype code is preserved as **reference-only** at `~/code/packet-plumber-prototype-ref` (mine it for the harness design + what worked, avoid what crashed — do NOT copy its code). The **canon docs (GDD/arch/epics/decision-log) are the spec** — they're locked and good (locked routing model: per-hop forwarding + ECMP across equal-cost paths + parallel-pipe bundles; the six mechanics).

The existing **sprint-plan-v1 + stories-v1 are HORIZONTAL** (S0 spine → S1 routing → S2 topology → ... → S4 finally playable) and were drafted without reconciling against the prototype code. **Supersede them** with a **vertical-slice** plan.

## The vertical-slice mandate (the core requirement)

**Every story ships a launchable `app.bin` increment + a golden** — the user must be able to run the game and *see gameplay* after each story (or at minimum each epic). Contrast with v1's horizontal layers where nothing is playable until S4.

- **Slice 1 = the thinnest playable thing** (e.g. draw one pipe, one packet flows source→sink, you see it move, win/lose stub). Determinism spine + a minimal fresh harness + a window + input, end-to-end, however thin.
- **Each subsequent story adds depth while staying launchable** — never a horizontal "foundation" sprint that produces no playable game.
- **A golden per slice** (replay-equality) — the determinism contract rides from slice 1.
- Sequence **MVP-fun-test-first**: the surge-survival fun loop reachable as early as possible (v1 had this right at "S4" — preserve the *goal*, change the *structure* to get there via playable slices).

## From-scratch specifics

- **Fresh build** (a new branch at build time — not this planning job's concern; the plan just sequences the build).
- **Locked routing from the first routing slice** — per-hop forwarding + ECMP (`splitmix64(src,dst,class,pkt) mod N`) + parallel-pipe **bundles** (cap = sum; **round-robin/weighted LB is deleted**). **No BFS legacy** — the prototype's BFS does not carry over.
- **Harness rebuilt fresh**, *designed from* the prototype's harness reference (`~/code/packet-plumber-prototype-ref/harness/`, `goldens/`) — its replay-equality + golden-capture design was solid; rebuild it clean, don't copy the buggy code.
- **The six GDD mechanics** (strain-heatmap, bespoke crisis thresholds, failure-teaches-counter, emergent clutch, costly fallback, interconnected upgrades) — sequence them as later vertical slices, not slice 1.

## Inputs (read)
1. **Canon:** `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` + `epics.md`; `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (the per-hop/ECMP/bundles model + ODN determinism rules); `docs/routing-explorer.html` (the decision rationale).
2. **To supersede:** `_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md` + `stories-v1.md` (horizontal — replace with vertical slices; mark v1 superseded).
3. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/` — `harness/`, `goldens/` (harness design to reuse as design), `core/` (what the sim did, what to avoid).
4. `project-context.md`.

## Deliverable
- **`sprint-plan-v2.md`** + **`stories-v2.md`**: vertical-slice, from-scratch, locked-routing, MVP-fun-test-first. Each story = launchable increment + golden + canon-system map + headless test contract. Cite prototype-reference lessons where relevant.
- Mark sprint-plan-v1 / stories-v1 as **superseded** (don't delete — point to v2).
- **Lavish review** of the slice structure before any PR (the user signs off the vertical-slice shape first).

## Verify (the plan's done-bar)
- [ ] Every story is a **launchable** increment (an `app.bin` you can run + see gameplay), with a golden.
- [ ] Slice 1 is the thinnest playable thing; the surge-survival fun loop is reachable early.
- [ ] Locked routing (per-hop/ECMP/bundles) from the first routing slice; no BFS; RR/weighted LB absent.
- [ ] Harness + determinism spine in slice 1 (rebuilt fresh, designed from the prototype reference).
- [ ] v1 marked superseded.
- [ ] lavish sign-off captured before PR.

## Self-report (do not skip)
- `bin/ledger set packet-plumber-sprint-replan-v2 working` at start (`clarifying` if you halt)
- `bin/ledger set packet-plumber-sprint-replan-v2 in-review "PR <url>"` when PR opens
- `herdr notification show "sprint-replan-v2" --body "<one-line>"` on finish
- Final message: the vertical-slice structure summary, slice-1 definition, how it supersedes v1, PR URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: sprint-replan-v2 · base: main
- model: zai-coding-cn/glm-5.2 · pr_review: 0 · github_issue: (none)
